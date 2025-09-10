---
title: Defold 中的原生代码调试
brief: 本手册解释了如何在 Defold 中调试原生代码。
---

# 原生代码调试

Defold 经过充分测试，在正常情况下应该很少崩溃。然而，无法保证它永远不会崩溃，特别是当您的游戏使用原生扩展时。如果您遇到崩溃或原生代码行为不符合预期的问题，有几种不同的解决方法：

* 使用调试器逐步执行代码
* 使用打印调试
* 分析崩溃日志
* 符号化调用堆栈


## 使用调试器

最常见的方法是通过 `调试器` 运行代码。它允许您逐步执行代码，设置 `断点`，如果发生崩溃，它将停止执行。

每个平台都有几种调试器。

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

每个工具可以调试特定平台：

* Visual studio - Windows + 支持 gdbserver 的平台（例如 Linux/Android）
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + 支持 gdbserver 的平台
* Xcode -  macOS, iOS ([了解更多](/manuals/debugging-native-code-ios))
* Android Studio - Android ([了解更多](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (通过 lldb)


## 使用打印调试

调试原生代码的最简单方法是使用 [打印调试](http://en.wikipedia.org/wiki/Debugging#Techniques)。使用 [`dmLog` 命名空间](/ref/stable/dmLog/) 中的函数来观察变量或指示执行流程。使用任何日志函数都会在编辑器的 *控制台* 视图和 [游戏日志](/manuals/debugging-game-and-system-logs) 中打印输出。


## 分析崩溃日志

如果 Defold 引擎发生硬崩溃，它会保存一个 `_crash` 文件。崩溃文件将包含有关系统以及崩溃的信息。[游戏日志输出](/manuals/debugging-game-and-system-logs) 将写入崩溃文件所在的位置（它根据操作系统、设备和应用程序而变化）。

您可以使用 [崩溃模块](https://www.defold.com/ref/crash/) 在后续会话中读取此文件。建议您读取文件，收集信息，将其打印到控制台，然后将其发送到支持收集崩溃日志的 [分析服务](/tags/stars/analytics/)。

::: important
在 Windows 上，还会生成一个 `_crash.dmp` 文件。此文件在调试崩溃时很有用。
:::

### 从设备获取崩溃日志

如果崩溃发生在移动设备上，您可以选择将崩溃文件下载到您自己的计算机并在本地解析它。

#### Android

如果应用是 [可调试的](/manuals/project-settings/#android)，您可以使用 [Android Debug Bridge (ADB) 工具](https://developer.android.com/studio/command-line/adb.html) 和 `adb shell` 命令获取崩溃日志：

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

在 iTunes 中，您可以查看/下载应用程序容器。

在 `Xcode -> Devices` 窗口中，您也可以选择崩溃日志。


## 符号化调用堆栈

如果您从 `_crash` 文件或 [日志文件](/manuals/debugging-game-and-system-logs) 获取调用堆栈，您可以对其进行符号化。这意味着将调用堆栈中的每个地址转换为文件名和行号，这反过来有助于找出根本原因。

重要的是，您必须将正确的引擎与调用堆栈匹配，否则很可能会让您调试错误的内容！使用 [`--with-symbols`](https://www.defold.com/manuals/bob/) 标志与 [bob](https://www.defold.com/manuals/bob/) 捆绑，或者从编辑器的捆绑对话框中选中 "Generate debug symbols" 复选框：

* iOS - `build/arm64-ios` 中的 `dmengine.dSYM.zip` 文件夹包含 iOS 构建的调试符号。
* macOS - `build/x86_64-macos` 中的 `dmengine.dSYM.zip` 文件夹包含 macOS 构建的调试符号。
* Android - `projecttitle.apk.symbols/lib/` 捆绑输出文件夹包含目标架构的调试符号。
* Linux - 可执行文件包含调试符号。
* Windows - `build/x86_64-win32` 中的 `dmengine.pdb` 文件包含 Windows 构建的调试符号。
* HTML5 - `build/js-web` 或 `build/wasm-web` 中的 `dmengine.js.symbols` 文件包含 HTML5 构建的调试符号。


::: important
非常重要的一点是，您必须为您发布的每个公共版本保存调试符号，并且您知道调试符号属于哪个版本。如果您没有调试符号，您将无法调试任何原生崩溃！此外，您应该保留引擎的未剥离版本。这样可以最好地对调用堆栈进行符号化。
:::


### 将符号上传到 Google Play
您可以 [将调试符号上传到 Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems)，以便在 Google Play 中记录的任何崩溃都将显示符号化的调用堆栈。将 `projecttitle.apk.symbols/lib/` 捆绑输出文件夹的内容压缩。该文件夹包含一个或多个具有架构名称的子文件夹，如 `arm64-v8a` 和 `armeabi-v7a`。


### 符号化 Android 调用堆栈

1. 从您的构建文件夹中获取引擎

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. 解压到一个文件夹：

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. 查找调用堆栈地址

	例如，在未符号化的调用堆栈中，它可能看起来像这样

	`#00 pc 00257224 libmy_game_name.so`

	其中 *`00257224`* 是地址

4. 解析地址

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

注意：如果您从 [Android 日志](/manuals/debugging-game-and-system-logs) 获取堆栈跟踪，您可能可以使用 [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) 对其进行符号化

### 符号化 iOS 调用堆栈

1. 如果您正在使用原生扩展，服务器可以为您提供符号（.dSYM）（将 `--with-symbols` 传递给 bob.jar）

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# 它将产生一个 Contents/Resources/DWARF/dmengine
```

2. 如果您没有使用原生扩展，下载原始符号：

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. 使用加载地址进行符号化

	出于某种原因，简单地放入调用堆栈中的地址不起作用（即加载地址 0x0）

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# 直接指定加载地址也不起作用

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	将加载地址添加到地址中起作用：

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
