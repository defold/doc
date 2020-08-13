---
title: 调试原生扩展
brief: 本教程介绍了一些调试包含原生扩展程序应用的方法.
---

# 调试原生扩展

开发原生扩展程序的时候总会碰到这样那样的问题，比如在编译服务器上编译不通过或者应用里扩展程序无效等等.

## 报错调试

通常一旦原生扩展程序在编译服务器上报错, 服务器控制台会给出所有的错误信息. 包括错误类型和哪个文件哪一行出的错. 同时 `log.txt` 日志文件也会被保存在编译文件夹当中.

## 运行时调试

一旦原生扩展的程序代码出了问题, 有一下途径可以找到问题所在.

* Using a debugger
* Using print debugging
* Analyzing a crash log
* Symbolicating a callstack

### 使用调试器

当你的代码出现问题时, 有一些方法可以找到问题的根源.

最普通的就是使用 `调试器`.
调试可以让你在代码中步进, 设置 `断点` 而且能在崩溃时冻结运行.

各个平台都有一些调试器.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* XCode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

各个工具可以用来调试特定平台应用:

* Visual studio - Windows + platforms supporting gdbserver (E.g. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + platforms supporting gdbserver
* XCode -  macOS, iOS
* Android Studio - Android
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (via lldb)


### 打印调试信息

有些时候, 需要在代码里加入 printf() 声明.
之后, 你就可以从设备上获取日志文件来分析它.

注意 Defold 的debug编译版本默认只输出 dmLog* 函数结果.

#### [Android](/manuals/extensions-debugging-android)

在 Android 上, 获取日志最简单办法是通过终端的 `adb`.
还可以在 Android Studio 里使用 `console`, 这俩是一样的.

如果你从 Android 日志中获得了跟踪堆栈, 你可能要使用 [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) 来进行解析.

#### [iOS](/manuals/extensions-debugging-ios)

在 iOS 中, 你要使用 iTunes 或者 XCode 来观察设备日志.

### Defold 崩溃日志

当 Defold 引擎硬崩溃时会保存一个 `_crash` 文件.
它包含了关于系统和崩溃的信息.

你可以使用 [crash module](https://www.defold.com/ref/crash/) 来读取这个文件.

建议你读取这个文件, 收集信息然后放送到自己适用的服务器上来归集数据.


#### Android

adb 可以显示此文件在哪 (不同设备保存位置不同)

如果应用是 [可调试的](https://www.defold.com/manuals/project-settings/#android), 可以这样获取崩溃日志:

```
	$ adb shell "run-as com.defold.adtest sh -c 'cat /data/data/com.defold.adtest/files/_crash'" > ./_crash
```

##### iOS

在 iTunes 中, 你可以 view/download 应用容器.

在 `XCode -> Devices` 窗口中, 也可以选择崩溃日志


### Symbolication

如果你从 `_crash` 文件或者日志文件获得了调用堆栈, 就可以开始解析它.
也就是把各个调用堆栈的地址转化为文件名和代码行, 这样有助于找到出问题的原因.

#### 获取正确的引擎

使调用堆栈匹配正确的引擎是很重要的.
否则很容易让你调试到不正确的地方.

而且, 如果编译时使用了原生扩展, 确保添加了 [--with-symbols](https://www.defold.com/manuals/bob/) 选项
以便从编译服务器获取所需信息. 比如, 可以在 iOS/macOS 的编译文件 `build.zip` 里找到 `dmengine.dSYM` 文件夹.

Android/Linux 可运行文件已经包含了调试信息.

还有, 你要持有引擎的完整版.
这样有助于分析调试文件的调用堆栈.


#### Android

1. 从 build 文件夹获取

	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]

1. 解压缩:

	$ unzip dmengine.apk -d dmengine_1_2_105

1. 找到调用堆栈地址

	也就是分析前的调用堆栈, 类似这样

	#00 pc 00257224 libmy_game_name.so

	其中 *00257224* 就是地址

1. 解析地址

    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_

#### iOS

1. 如果使用了原生扩展, 服务器会提供解析文件 (.dSYM) 给你 (使用 bob.jar 加 "--with-symbols" 选项)

	$ unzip <project>/build/arm64-darwin/build.zip
	# 可以解压出 Contents/Resources/DWARF/dmengine

1. 如果未使用原生扩展, 下载解析文件:

	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM

1. 使用载入地址进行解析

	如果, 简单的输入调用堆栈地址不管用 (即 载入地址 0x0)

		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4

	# 直接输入载入地址也不管用

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4

	把载入地址加到地址里就管用了:

		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
