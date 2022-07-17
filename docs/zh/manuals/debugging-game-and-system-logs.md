---
title: 调试 - 游戏和系统日志
brief: 本教程介绍了获取游戏和系统日志的方法.
---

# 游戏和系统日志

游戏日志保存了引擎的所有输出, 包括原生扩展和脚本代码上的输出. 用 [print()](/ref/stable/base/#print:...) 和 [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) 函数就能在日志里留下游戏输出. 可以使用原生扩展 [dmLog](/ref/stable/dmLog/) 下的函数读写日志文件. 各种文本阅读编辑器都能打开日志文件.

系统日志是由操作系统提供的, 也许会对调试游戏有所帮助. 系统日志可以记录应用崩溃时的调用堆栈和内存不足等信息.

::: 注意
游戏日志只会在 debug 模式的编译版本中出现. 发布版本会去掉所有日志输出.
:::

## 用编辑器查看游戏日志

当在编辑器本地或者连接了 [mobile 开发版应用](/manuals/dev-app) 运行游戏时, 所有日志输出都能做编辑器控制台看到:

![Editor 2](images/editor/editor2_overview.png)

## 用控制台查看游戏日志

当使用控制台启动游戏时, 日志文件也会打印在当前控制台上. 在 Windows 和 Linux 控制台上直接打游戏可执行文件名即可. 在 macOS 控制台上要打 .app 文件里面的游戏引擎名:

```
$ > ./mygame.app/Contenst/MacOS/mygame
```

## 不同平台的日志读取

### HTML5

绝大多数浏览器都提供了显示日志输出的控制台.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - 菜单 > 更多工具 > 开发者工具
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - 工具 > 网络开发者 > 网络控制台
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - 开发 > 显示JavaScript控制台

### Android

可以使用 Android Debug Bridge (ADB) 工具来查看游戏和系统日志.

:[Android ADB](../shared/android-adb.md)

  工具安装好之后, 通过 USB 连接你的设备, 启动控制台, 输入:

```txt
$cd <path_to_android_sdk>/platform-tools/
$adb logcat
```

设备会把所有日志信息打印在当前控制台上, 包含游戏输出信息.

要想只查看 Defold 输出的日志信息, 可以这么输入:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:DLIB: SSDP started (ssdp://192.168.0.97:58089, http://0.0.0.0:38637)
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialised sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

可以使用 [控制台工具](https://support.apple.com/guide/console/welcome/mac) 读取游戏和系统日志. 可以使用 LLDB 调试器连接设备上运行的游戏. 调试前确保设备上存有该应用的 “Apple Developer Provisioning Profile”. 从编辑器的打包对话框那里提供档案文件 (只能在 macOS 平台上打包 iOS 应用).

需要一个叫做 [ios-deploy](https://github.com/phonegap/ios-deploy) 的工具才能进行调试. 命令如下:

```txt
ios-deploy --debug --bundle <path_to_game.app> # 注意: 不是 .ipa 文件
```

它会把应用安装到设备上, 启动应用并且把 LLDB 调试器连接到应用上. 如果不熟悉 LLDB, 请参考 [LLDB 基础教程](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## 从日志文件中读取日志信息

如果你在 "game.project" 文件里打开了 *Write Log* 项, 所有游戏输出都会被记录到硬盘上, 保存为 "log.txt" 文件. 下面介绍了从设备上获取日志文件的方法:

iOS
: 把设备连接到安装有 macOS 和 Xcode 的电脑上.

  启动 Xcode 选择 <kbd>Window ▸ Devices and Simulators</kbd>.

  在列表中选择你的设备, 然后在 *Installed Apps* 列表中选择你的游戏应用.

  点击列表下方的齿轮图标选择 <kbd>Download Container...</kbd>.

  ![download container](images/debugging/download_container.png){srcset="images/debugging/download_container@2x.png 2x"}

  容器被下载解压之后就可以在 *Finder* 中看到了. 右键单击容器选择 <kbd>Show Package Content</kbd>. 找到 "log.txt", 一般位于 "AppData/Documents/".

Android
: "log.txt" 的获取取决于操作系统版本和制造商. 这里有一个简单的 [步骤教程](https://stackoverflow.com/a/48077004/129360).
