---
title: Debugging extensions
brief: This manual describes some ways to debug an application containing native extensions.
---

# Debugging extensions

When you develop a native extension you typically run into either problems when compiling the extension on the build server or when the extension code in an application.

## Debugging build problems

When a native extension fails to build the console usually shows all of the errors generated on the build server. You can see what kind of error it is and in which file and line number. The entire build log is also stored in a file `log.txt` in your build folder.

## Debugging run-time problems

When you get a particularly troublesome issue in your code, there are several ways to find the root cause.

* Using a debugger
* Using print debugging
* Analyzing a crash log
* Symbolicating a callstack

### Using a debugger

The most common way is to run the code via a `debugger`. It let's you step through the code, set `breakpoints` and it will stop the execution if you get a crash.

There are several debuggers around for each platform.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* XCode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

And each tool can debug certain platforms:

* Visual studio - Windows + platforms supporting gdbserver (E.g. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + platforms supporting gdbserver
* XCode -  macOS, iOS
* Android Studio - Android
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


### Print debugging

In certain cases, one might want to add `printf()` statements to the code. Afterwards, you can get the logs from your device and analyze them.

Note that Defold by default only prints using dmLog* functions in the debug build.

#### [Android](/manuals/extensions-debugging-android)

On Android, the simplest way to get the log is to run `adb` in the terminal. You can also see the `console` inside Android Studio, which is the same thing.

If you get hold of a stack trace from the Android logs, you might be able to symbolicate it using [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

#### [iOS](/manuals/extensions-debugging-ios)

On iOS, you need to open either iTunes or XCode to view the device logs.


### Defold Crash Log

The Defold engine saves a `_crash` file when it does a hard crash. It will contain information about the system as well as the crash.

You can use the [crash module](https://www.defold.com/ref/crash/) to read this file in the subsequent session.

You are adviced to read the file, gather information and send it to a server of choice to aggregate the data.


#### Getting the crash log from a device

##### Android

The adb output says where it is located (different location on different devices)

If the app is [debuggable](https://www.defold.com/manuals/project-settings/#android), you can get the crash log like so:

```
	$ adb shell "run-as com.defold.adtest sh -c 'cat /data/data/com.defold.adtest/files/_crash'" > ./_crash
```

##### iOS

In iTunes, you can view/download an apps container.

In the `XCode -> Devices` window, you can also select the crash logs


### Symbolication

If you get a callstack from either a `_crash` file or a log file, you can start symbolicate it.
This means translating each address in the callstack into a filename and line number, which in turn helps
when finding out the root cause.

#### Get correct engine

It is important that you match the correct engine with the callstack.
Otherwize it's very likely to send you debugging the incorrect things.

Also, if you are building with native extensions, be sure to add the flag [--with-symbols](https://www.defold.com/manuals/bob/)
so that you get all the needed data from the build server. For instance, in the `build.zip` you'll find the `dmengine.dSYM` folder for iOS/macOS builds.

Android/Linux executables already contain the debug symbols.

Also, you should keep an unstripped version of the engine.
This allows for the best symbolication of the callstack.

#### Android

1. Get it from your build folder

	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]

1. Unzip to a folder:

	$ unzip dmengine.apk -d dmengine_1_2_105

1. Find the callstack address

	E.g. in the non symbolicated callstack on Crash Analytics, it could look like this

	#00 pc 00257224 libmy_game_name.so

	Where *00257224* is the address

1. Resolve the address

    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_

#### iOS

1. If you are using Native Extensions, the server can provide the symbols (.dSYM) for you (pass "--with-symbols" to bob.jar)

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
