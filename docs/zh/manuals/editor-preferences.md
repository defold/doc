---
title: 编辑器配置
brief: 可以通过设置窗口修改编辑器配置.
---

# 编辑器配置

可以通过设置窗口修改编辑器配置. 选择菜单栏 <kbd>File -> Preferences</kbd> 即可打开设置窗口.

## General

![](images/editor/preferences_general.png){srcset="images/editor/preferences_general@2x.png 2x"}

Load External Changes on App Focus
: 当编辑器获得焦点时扫描外部文件改变.

Open Bundle Target Folder
: 打包结束后自动打开输出文件夹.

Enable Texture Compression
: 开启编译 [纹理压缩](/manuals/texture-profiles).

Escape Quits Game
: 用 <kbd>Esc</kbd> 键关闭正在运行的编译好的游戏.

Track Active Tab in Asset Browser
: 在 *编辑器* 面板编辑的文件自动在资源浏览器 (也叫 *Asset* 面板) 中选中.

Path to custom keymap
: [自定义快捷键](/manuals/editor-keyboard-shortcuts) 配置文件的绝对路径.


## Code

![](images/editor/preferences_code.png)

Custom Editor
: 自定义编辑器的绝对路径. 在 macOS 上应指向 .app 内的可执行程序 (比如 `/Applications/Atom.app/Contents/MacOS/Atom`).

Open File
: 自定义编辑器开启时要打开的文件的表达式. 其中 `{file}` 在开启时会被真实文件名代替.

Open File at Line
: 自定义编辑器开启时要打开的文件以及指定光标放置的行数. 表达式 `{file}` 在开启时会被真是文件名代替, 而 `{line}` 被行号代替.

Code editor font
: 代码编辑器里要使用的系统上已安装的字体名称.


### 使用 Visual Studio Code 打开脚本文件

![](images/editor/preferences_vscode.png)

要从 Defold 编辑器里直接用 Visual Studio Code 打开脚本文件, 必须配置下列可执行文件地址:

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

 配置打开指定文件和指定行号的参数:

- 打开文件: `. {file}`
- 打开到行: `. -g {file}:{line}`

其中 `.` 符号代表打开整个项目, 而不是指定文件.


## 扩展

![](images/editor/preferences_extensions.png)

Build Server
: 编译包含 [原生扩展](/manuals/extensions) 项目时使用的编译服务器的 URL. 可以在编译服务器的请求 URL 中加入用户名和验证令牌. 使用格式举例: `username:token@build.defold.com`. 在使用用户自己的编译服务器并开启认证时, 任天堂 Switch 编译需要这种用户认证 ([更多信息详见编译服务器文档](https://github.com/defold/extender/blob/dev/README_SECURITY.md)). 其中用户名和密码可以用系统环境变量 `DM_EXTENDER_USERNAME` 和 `DM_EXTENDER_PASSWORD` 来设置.

Build Server Headers
: 编译原生扩展时向服务器发送的额外的 header. 在使用 CloudFlare 服务或类似服务编译扩展时是很必要的.

## 工具

![](images/editor/preferences_tools.png)

ADB path
: 配置 [ADB](https://developer.android.com/tools/adb) 命令行工具的路径. 如果系统中安装了 ADB, 则 Defold 编辑器会使用它来安装和运行 Android APK 包到指定设备. 默认情况下, 编辑器会检查 ADB 是否安装在了默认位置, 如果需要手动指定路径则需配置该选项.

ios-deploy path
: 配置 [ios-deploy](https://github.com/ios-control/ios-deploy) 命令行工具的路径 (仅适用于 macOS). 与 ADB 路径类似, Defold 编辑器会使用该工具安装和运行 iOS 包到连接好的 iPhone 上. 默认情况下, 编辑器会检查 ios-deploy 是否安装在了默认位置, 如果需要手动指定路径则需配置该选项.