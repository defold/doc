---
title: 编辑器首选项
brief: 您可以从首选项窗口修改编辑器的设置。
---

# 编辑器首选项

您可以从首选项窗口修改编辑器的设置。首选项窗口通过 <kbd>File -> Preferences</kbd> 菜单打开。

## 通用

![](images/editor/preferences_general.png)

Load External Changes on App Focus
: 当编辑器获得焦点时启用外部更改扫描。

Open Bundle Target Folder
: 启用打包过程完成后打开目标包文件夹。

Enable Texture Compression
: 为编辑器进行的所有构建启用[纹理压缩](/manuals/texture-profiles)。

Escape Quits Game
: 使用 <kbd>Esc</kbd> 键关闭正在运行的游戏构建。

Track Active Tab in Asset Browser
: 在*编辑器*面板中选定标签页中编辑的文件将在资源浏览器（也称为*资源*面板）中被选中。

Lint Code on Build
: 构建项目时启用[代码检查](/manuals/writing-code/#linting-configuration)。此选项默认启用，但如果大型项目的代码检查耗时过长，可以禁用。

Engine Arguments
: 当编辑器构建和运行时，将传递给dmengine可执行文件的参数。
每行使用一个参数。例如：
```
--config=bootstrap.main_collection=/my dir/1.collectionc
--verbose
--graphics-adapter=vulkan
```


## 代码

![](images/editor/preferences_code.png)

Custom Editor
: 外部编辑器的绝对路径。在macOS上，它应该是.app内部可执行文件的路径（例如 `/Applications/Atom.app/Contents/MacOS/Atom`）。

Open File
: 自定义编辑器用于指定要打开哪个文件的模式。模式 `{file}` 将被要打开的文件名替换。

Open File at Line
: 自定义编辑器用于指定要打开哪个文件以及在哪个行号打开的模式。模式 `{file}` 将被要打开的文件名替换，`{line}` 将被行号替换。

Code editor font
: 在代码编辑器中使用的系统安装字体名称。

Zoom on Scroll
: 在代码编辑器中滚动时按住Cmd/Ctrl按钮是否更改字体大小。


### 在Visual Studio Code中打开脚本文件

![](images/editor/preferences_vscode.png)

要从Defold编辑器直接在Visual Studio Code中打开脚本文件，必须通过指定可执行文件的路径来设置以下设置：

- MacOS: `/Applications/Visual Studio Code.app/Contents/MacOS/Electron`
- Linux: `/usr/bin/code`
- Windows: `C:\Program Files\Microsoft VS Code\Code.exe`

设置这些参数以打开特定文件和行：

- Open File: `. {file}`
- Open File at Line: `. -g {file}:{line}`

这里的 `.` 字符是必需的，用于打开整个工作区，而不是单个文件。


## 扩展

![](images/editor/preferences_extensions.png)

Build Server
: 构建包含[原生扩展](/manuals/extensions)的项目时使用的构建服务器的URL。可以向URL添加用户名和访问令牌以进行构建服务器的身份验证访问。使用以下表示法指定用户名和访问令牌：`username:token@build.defold.com`。Nintendo Switch构建以及运行启用了身份验证的自己的构建服务器实例时需要身份验证访问（[请参阅构建服务器文档](https://github.com/defold/extender/blob/dev/README_SECURITY.md)了解更多信息）。用户名和密码也可以设置为系统环境变量`DM_EXTENDER_USERNAME`和`DM_EXTENDER_PASSWORD`。

Build Server Username
: 用于身份验证的用户名。

Build Server Password
: 用于身份验证的密码，将加密存储在首选项文件中。

Build Server Headers
: 构建原生扩展时发送到构建服务器的额外标头。对于使用CloudFlare服务或类似服务的扩展器很重要。

## 工具

![](images/editor/preferences_tools.png)

ADB path
: 安装在此系统上的[ADB](https://developer.android.com/tools/adb)命令行工具的路径。如果系统上安装了ADB，Defold编辑器将使用它将打包的Android APK安装并运行到连接的Android设备上。默认情况下，编辑器检查ADB是否安装在已知位置，因此只有当ADB安装在自定义位置时才需要指定路径。

ios-deploy path
: 安装在此系统上的[ios-deploy](https://github.com/ios-control/ios-deploy)命令行工具的路径（仅与macOS相关）。与ADB路径类似，Defold编辑器将使用此工具将打包的iOS应用程序安装并运行到连接的iPhone上。默认情况下，编辑器检查ios-deploy是否安装在已知位置，因此只有当您使用自定义安装的ios-deploy时才需要指定路径。

## 键映射

![](images/editor/preferences_keymap.png)

您可以配置编辑器快捷键，既可以添加自定义快捷键，也可以删除内置快捷键。在快捷键表格中的单个命令上使用上下文菜单来编辑快捷键，或双击/按<kbd>Enter</kbd>打开新的快捷键弹出窗口。

一些快捷键可能有警告：它们使用橙色显示。将鼠标悬停在快捷键上以查看警告。典型警告包括：
- 可输入快捷键：所选快捷键可在文本输入中输入。确保该命令在代码编辑/文本输入上下文中处于关闭状态。
- 冲突：同一快捷键分配给多个不同的命令。确保在调用快捷键时最多启用一个命令，否则编辑器将以未定义的方式执行分配的命令之一。