---
title: Defold 中的原生代码调试
brief: 本教程介绍了在 Defold 中调试原生代码的方法.
---

# 原生代码调试

Defold 几经测试鲜有崩溃情况出现. 但是崩溃这种事谁能保证永远避免, 尤其是游戏中还使用了原生扩展代码的情况下. 要是游戏崩溃或者原生代码出错请从下面几方面入手检查:

* 使用调试器调试代码
* 使用 print 函数检查代码
* 分析崩溃日志
* 调用堆栈代码文件映射


## 使用调试器

首先推荐使用 `调试器`. 使用它步进代码, 设置 `断点` 最重要的是游戏崩溃时会自动暂停.

不同平台调试器有很多.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

每个工具可以调试的应用如下:

* Visual studio - Windows + platforms supporting gdbserver (比如 Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + platforms supporting gdbserver
* Xcode -  macOS, iOS ([详见](/manuals/debugging-native-code-ios))
* Android Studio - Android ([详见](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


## 使用 print 函数

调试最简单的方法就是使用 [print 函数](http://en.wikipedia.org/wiki/Debugging#Techniques). 位于 [dmLog 命名空间](/ref/stable/dmLog/) 下的 print 函数可以用来检查变量值或者用来检查程序执行流程. 它可以在 *控制台* 视图和 [游戏日志](/manuals/debugging-game-and-system-logs) 中输出数据.


## 崩溃日志分析

崩溃时, Defold 引擎保存了一个 `_crash` 日志文件. 其中包含了系统信息与崩溃信息. 其存放位置参考 [游戏日志输出](/manuals/debugging-game-and-system-logs) (不同设备, 系统, 位置不同).

可以使用 [崩溃模块](https://www.defold.com/ref/crash/) 帮助分析这个文件. 推荐你阅读, 收集信息, 打印信息到控制台, 然后把信息发送到 [第三方分析服务](/tags/stars/analytics/) 上去.

::: important
在 Windows 上还有个 `_crash.dmp` 文件被创建. 这个文件在调试崩溃时很有用.
:::

### 从设备上获取崩溃日志

手机上的崩溃日志可以下载到本地以便查看.

#### Android

如果应用是 [可调式的](/manuals/project-settings/#Android), 就可以使用 [Android Debug Bridge (ADB) 工具](https://developer.android.com/studio/command-line/adb.html) 和 `adb shell` 命令得到崩溃日志:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

在 iTunes 里, 可以下载 app 容器.

在 `Xcode -> Devices` 窗口中也能获取到崩溃日志.


## 调用堆栈代码文件映射

从 `_crash` 文件或者 [日志文件](/manuals/debugging-game-and-system-logs), 都可以进行代码文件映射. 即把调用堆栈里的每个地址映射到文件名和代码行, 利于寻找代码的问题.

注意引擎版本要选择正确. 不然映射会错乱. 使用 [bob](https://www.defold.com/manuals/bob/) 编译时命令行加入 [--with-symbols](https://www.defold.com/manuals/bob/) 或者在编辑器打包对话框里点选 "Generate debug symbols":

* iOS - 在 `build/arm64-ios` 下的 `dmengine.dSYM.zip` 中包含有 iOS 编译用 debug symbols.
* macOS - 在 `build/x86_64-macos` 下的 `dmengine.dSYM.zip` 中包含有 macOS 编译用 debug symbols.
* Android - 在打包输出目录 `projecttitle.apk.symbols/lib/` 下包含有各架构编译用 debug symbols.
* Linux - 可执行文件本身包含 debug symbols.
* Windows - 在 `build/x86_64-win32` 下的 `dmengine.pdb` 中包含有 Windows 编译用 debug symbols.
* HTML5 - 在 `build/js-web` 或 `build/wasm-web` 下的 `dmengine.js.symbols` 中包含有 HTML5 编译用 debug symbols.


::: important
对于游戏的每个发布版本一定要保留一套对应的调试数据. 不然的话原生扩展上线以后出错误就没法调试! 为了方便查看调用堆栈, 也要保存好对应的游戏引擎.
:::


### 把 symbols 上传到 Google Play
可以 [上传 debug symbols 到 Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) 以便让 Google Play 上的崩溃日志显示可读的调用堆栈. 详情请见 [原生代码调试教程](/manuals/debugging-native-code).


### Android调用堆栈映射

1. 从编译文件夹下找到引擎文件

	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]

1. 解压引擎:

	$ unzip dmengine.apk -d dmengine_1_2_105

1. 找到地址

	例如下面这个文件

	`#00 pc 00257224 libmy_game_name.so`

	其中 *00257224* 就是地址

1. 映射地址

    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_

注意: 要是从 [Android 日志](/manuals/debugging-game-and-system-logs) 获取的调用堆栈数据, 可能需要使用 [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) 进行地址解析

### iOS 调用堆栈映射

1. 如果使用了原生扩展, 服务器会为你提供映射数据 (.dSYM) 文件 (使用 bob.jar 连同 `--with-symbols` 参数)

	$ unzip <project>/build/arm64-darwin/build.zip
	# 文件会被解压到 Contents/Resources/DWARF/dmengine

1. 如果没用原生扩展, 直接下载映射文件:

	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM

1. 地址映射

	不能直接使用堆栈里的地址 (比如载入地址 0x0)

		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4

	# 也不能作为参数加入载入地址

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4

	二者相加才可以:

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
