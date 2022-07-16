---
title: Debugging native code in Defold
brief: This manual explains how to debug native code in Defold.
---

# Debugging native code

Defold is well tested and should very rarely crash under normal circumstances. It is however impossible to guarantee that it will never crash, especially if your game uses native extensions. If you run into problems with crashes or native code that doesn't behave as expected there are a number of different ways forward:

* Use a debugger to step through the code
* Use print debugging
* Analyze a crash log
* Symbolicate a callstack


## Use a debugger

The most common way is to run the code via a `debugger`. It let's you step through the code, set `breakpoints` and it will stop the execution if you get a crash.

There are several debuggers for each platform.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Each tool can debug certain platforms:

* Visual studio - Windows + platforms supporting gdbserver (E.g. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + platforms supporting gdbserver
* Xcode -  macOS, iOS ([learn more](/manuals/debugging-native-code-ios))
* Android Studio - Android ([learn more](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


## Use print debugging

The simplest way to debug your native code is to use [print debugging](http://en.wikipedia.org/wiki/Debugging#Techniques). Use the functions in the [dmLog namespace](/ref/stable/dmLog/) to watch variables or indicate the flow of execution. Using any of the log functions will print to the *Console* view in the editor and to the [game log](/manuals/debugging-game-and-system-logs).


## Analyze a crash log

The Defold engine saves a `_crash` file if it does a hard crash. The crash file will contain information about the system as well as the crash. The [game log output](/manuals/debugging-game-and-system-logs) will write where the crash file is located (it varies depending on operating system, device and application).

You can use the [crash module](https://www.defold.com/ref/crash/) to read this file in the subsequent session. It is recommended that you read the file, gather the information, print it to the console and send it to an [analytics services](/tags/stars/analytics/) that supports collection of crash logs.

::: important
On Windows a `_crash.dmp` file is also generated. This file is useful when debugging a crash.
:::

### Getting the crash log from a device

If a crash happens on a mobile device you can chose to download the crash file to your own computer and parse it locally.

#### Android

If the app is [debuggable](/manuals/project-settings/#android), you can get the crash log using the [Android Debug Bridge (ADB) tool](https://developer.android.com/studio/command-line/adb.html) and the `adb shell` command:

```
	$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

In iTunes, you can view/download an apps container.

In the `Xcode -> Devices` window, you can also select the crash logs


## Symbolicate a callstack

If you get a callstack from either a `_crash` file or a [log file](/manuals/debugging-game-and-system-logs), you can symbolicate it. This means translating each address in the callstack into a filename and line number, which in turn helps when finding out the root cause.

It is important that you match the correct engine with the callstack, otherwise it's very likely to send you debugging the incorrect things! Use the flag [`--with-symbols`](https://www.defold.com/manuals/bob/) when bundling with [bob](https://www.defold.com/manuals/bob/) or check the "Generate debug symbols" checkbox from the bundle dialog in the editor:

* iOS - the `dmengine.dSYM.zip` folder in `build/arm64-ios` contains the debug symbols for iOS builds.
* macOS - the `dmengine.dSYM.zip` folder in `build/x86_64-darwin` contains the debug symbols for macOS builds.
* Android - the `projecttitle.apk.symbols/lib/` bundle output folder contains the debug symbols for the target architectures.
* Linux - the executable contain the debug symbols. 
* Windows - the `dmengine.pdb` file in `build/x86_64-win32` contains the debug symbols for Windows builds.
* HTML5 - the `dmengine.js.symbols` file in `build/js-web` or `build/wasm-web` contains the debug symbols for HTML5 builds.

::: important
It is very important that your save the debug symbols somewhere for each public release you make of your game and that you know which release the debug symbols belong to. You will not be able to debug any native crashes if you do not have the debug symbols! Also, you should keep an unstripped version of the engine. This allows for the best symbolication of the callstack.
:::


### Uploading symbols to Google Play
You can [upload the debug symbols to Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) so that any crashes logged in Google Play will show symbolicated call stacks. Zip the contents of the `projecttitle.apk.symbols/lib/` bundle output folder. The folder includes one or more sub folders with architecture names such as `arm64-v8a` and `armeabi-v7a`.


### Symbolicate an Android callstack

1. Get the engine from your build folder

	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]

1. Unzip to a folder:

	$ unzip dmengine.apk -d dmengine_1_2_105

1. Find the callstack address

	E.g. in the non symbolicated callstack it could look like this

	#00 pc 00257224 libmy_game_name.so

	Where *00257224* is the address

1. Resolve the address

    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_

Note: If you get hold of a stack trace from the [Android logs](/manuals/debugging-game-and-system-logs), you might be able to symbolicate it using [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Symbolicate an iOS callstack

1. If you are using Native Extensions, the server can provide the symbols (.dSYM) for you (pass `--with-symbols` to bob.jar)

	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine

1. If you're not using Native Extensions, download the vanilla symbols:

	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM

1. Symbolicate using load address

	For some reason, simply putting the address from the callstack doesn't work (i.e. load address 0x0)

		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4

	# Neither does specifying the load address directly

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4

	Adding the load address to the address works:

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
