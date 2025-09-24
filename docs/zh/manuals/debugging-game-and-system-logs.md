---
title: 调试 - 游戏和系统日志
brief: 本手册解释了如何读取游戏和系统日志。
---

# 游戏和系统日志

游戏日志显示了引擎、原生扩展和游戏逻辑的所有输出。您可以从脚本和Lua模块中使用[print()](/ref/stable/base/#print:...)和[pprint()](/ref/stable/builtins/?q=pprint#pprint:v)命令在游戏日志中显示信息。您可以使用[`dmLog`命名空间](/ref/stable/dmLog/)中的函数从原生扩展写入游戏日志。游戏日志可以从编辑器、终端窗口、使用平台特定工具或从日志文件中读取。

系统日志由操作系统生成，它可以提供帮助您定位问题的附加信息。系统日志可以包含崩溃的堆栈跟踪和低内存警告。

::: important
游戏日志只会在调试构建中显示信息。在发布构建中，日志将完全为空。
:::

## 从编辑器读取游戏日志

当您从编辑器本地运行游戏或连接到[移动开发应用](/manuals/dev-app)时，所有输出将显示在编辑器的控制台窗格中：

![Editor 2](images/editor/editor2_overview.png)

## 从终端读取游戏日志

当您从终端运行Defold游戏时，日志将显示在终端窗口本身中。在Windows和Linux上，您在终端中键入可执行文件的名称来启动游戏。在macOS上，您需要从.app文件内启动引擎：

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## 使用平台特定工具读取游戏和系统日志

### HTML5

可以使用大多数浏览器提供的开发者工具读取日志。

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - 菜单 > 更多工具 > 开发者工具
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - 工具 > Web开发者 > Web控制台
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - 开发 > 显示JavaScript控制台

### Android

您可以使用Android调试桥（ADB）工具查看游戏和系统日志。

:[Android ADB](../shared/android-adb.md)

安装并设置好后，通过USB连接设备，打开终端并运行：

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

设备随后会将所有输出转储到当前终端，以及来自游戏的任何打印信息。

如果您只想查看Defold应用程序输出，请使用此命令：

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:DLIB: SSDP started (ssdp://192.168.0.97:58089, http://0.0.0.0:38637)
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

您有多种选择可以在iOS上读取游戏和系统日志：

1. 您可以使用[控制台工具](https://support.apple.com/guide/console/welcome/mac)读取游戏和系统日志。
2. 您可以使用LLDB调试器附加到设备上运行的游戏。要调试游戏，它需要使用包含您要调试的设备的"Apple Developer Provisioning Profile"进行签名。从编辑器打包游戏，并在打包对话框中提供配置文件（iOS打包仅在macOS上可用）。

要启动游戏并附加调试器，您需要一个名为[ios-deploy](https://github.com/phonegap/ios-deploy)的工具。通过在终端中运行以下命令来安装和调试您的游戏：

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # 注意: 不是 .ipa 文件
```

这将在您的设备上安装应用程序，启动它并自动将LLDB调试器附加到它。如果您是LLDB的新手，请阅读[LLDB入门](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html)。


## 从日志文件读取游戏日志

如果您在*game.project*中启用*Write Log*设置，任何游戏输出都将写入磁盘，到一个名为"`log.txt`"的文件中。以下是在设备上运行游戏时如何提取文件的方法：

iOS
: 将设备连接到安装了macOS和Xcode的计算机上。

  打开Xcode并转到<kbd>Window ▸ Devices and Simulators</kbd>。

  在列表中选择您的设备，然后在*Installed Apps*列表中选择相关的应用程序。

  单击列表下方的齿轮图标并选择<kbd>Download Container...</kbd>。

  ![download container](images/debugging/download_container.png)

  容器提取后，它将显示在*Finder*中。右键单击容器并选择<kbd>Show Package Content</kbd>。找到文件"`log.txt`"，它应该位于"`AppData/Documents/`"中。

Android
: 提取"`log.txt`"的能力取决于操作系统版本和制造商。这里有一个简短的简单的[逐步指南](https://stackoverflow.com/a/48077004/]129360)。
