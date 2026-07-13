---
title: 编辑器概述
brief: 本手册概述 Defold 编辑器的外观和工作方式，以及如何在其中导航。
---

# 编辑器概述

编辑器允许您以高效方式浏览和操作游戏项目中的所有文件和文件夹。编辑文件时会打开合适的编辑器，并在单独视图中显示该文件的所有相关信息。

## 启动编辑器

运行 Defold Editor 时，会看到项目选择和创建界面。点击选择您想执行的操作：

MY PROJECTS
: 这里显示最近打开的项目，方便您快速访问。这是启动界面的默认视图。

  如果您之前没有打开过任何项目（或已移除全部项目），它会显示两个按钮：您可以点击 `Open From Disk…` 通过系统文件浏览器查找并打开项目，或点击 `Create New Project` 按钮，此时界面会切换到 `TEMPLATES` 标签页。

  ![my projects](images/editor/start_no_projects.png)


  如果您之前打开过项目，这里会像下图一样显示项目列表：

  ![my projects](images/editor/start_my_projects.png)

TEMPLATES
: 包含空的或几乎空的基础项目，用于快速开始针对特定平台或使用特定扩展的新 Defold 项目。


TUTORIALS
: 包含带引导教程的项目，可用于学习、游玩和修改，如果您想跟随教程，可以从这里开始。


SAMPLES
: 包含用于展示特定用例的项目。

  ![New project](images/editor/start_templates.png)

创建新项目后，它会存储在本地磁盘，您所做的任何编辑都会保存在本地。

您可以在[项目设置手册](https://www.defold.com/manuals/project-setup/)中了解不同选项的更多信息。

## 编辑器语言

在启动界面左下角可以看到语言选择器，可从当前可用的本地化语言中选择。编辑器内部也可通过 `File ▸ Preferences ▸ General ▸ Editor Language` 访问此设置。

![Languages](images/editor/languages.png)

## 编辑器面板 {#the-editor-views}

Defold Editor 被划分为一组面板或视图，用于显示特定信息。

![Editor 2](images/editor/editor_overview.png)

### 1. Assets 面板
以树结构列出项目中的所有文件和文件夹，对应磁盘上的相同结构。点击并滚动可浏览列表。所有面向文件的操作都可以在此视图中完成：

   - <kbd>Left Mouse Click</kbd> 选择任意文件或文件夹，按住 <kbd>⇧ Shift</kbd> 可扩展选择，按住 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> 可选择/取消选择点击项。
   - <kbd>Double Mouse Click</kbd> 文件可在该文件类型的专用编辑器中打开。
   - <kbd>Drag and Drop</kbd> 可将磁盘其他位置的文件添加到项目，或将项目中的文件和文件夹移动到新位置。
   - <kbd>Right Mouse Click</kbd> 打开 _Context Menu_，可创建新文件或文件夹、重命名、删除、跟踪文件依赖等。

在平台支持的情况下，通过 *Assets* 面板删除的文件和文件夹会移到系统废纸篓或回收站。如果不支持移到废纸篓，或移动失败，编辑器将永久删除该项目。

### 2. Scene Editor 面板 {#the-scene-editor}

双击集合、游戏对象或可视组件文件会打开 *Scene Editor*，它是用于构建和编辑场景的可视化编辑器。脚本文件和其他非可视资源会改为在各自专用编辑器中打开。

![Scene Editor](images/editor/2d_scene.png)

Scene Editor 提供的一些核心功能：

- [2D 和 3D 场景导航](/manuals/scene-editing/#2d-and-3d-scene-orientation)，包含正交和透视摄像机模式
- [变换工具](/manuals/scene-editing/#manipulating-objects)，用于移动、旋转和缩放对象
- [Free Camera Mode](/manuals/scene-editing/#free-camera-mode)，用于第一人称 3D 导航
- [网格设置](/manuals/scene-editing/#grid-settings)，可配置大小、平面和外观
- [可见性过滤器](/manuals/scene-editing/#visibility-filters)，用于切换组件类型和辅助线

更多内容请阅读 [Scene Editor 手册](/manuals/scene-editing/)。

### 3. Outline 面板

此视图以层级树结构显示当前正在编辑的文件内容。Outline 会反映编辑器视图，并允许您对条目执行操作：

   - <kbd>Left Mouse Click</kbd> 选择条目，按住 <kbd>⇧ Shift</kbd> 可扩展选择，按住 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> 可选择/取消选择点击项。
   - <kbd>Drag and drop</kbd> 移动条目。将一个游戏对象拖放到集合中的另一个游戏对象上，可创建父子关系。
   - <kbd>Right Mouse Click</kbd> 打开 _Context Menu_，可添加条目、删除所选条目等。

可以点击列表中元素右侧的小 `👁` 眼睛图标，切换游戏对象和可视组件的可见性。

![Outline](images/editor/outline.png)

### 4. Properties 面板

此视图显示与当前所选条目相关的属性，例如 Id、URL、Position、Rotation、Scale，以及其他组件特定属性和脚本自定义属性。

您也可以 <kbd>Drag</kbd> `↕` 上下箭头并移动鼠标，来更改给定数值属性。

![Properties](images/editor/properties.png)

### 5. Tools 面板

此视图有多个标签页。

*Console* tab : 显示游戏运行时的错误、警告、信息等引擎输出，或您主动打印的内容，

*Build Errors* : 显示构建过程中的错误，

*Search Results* : 如果点击 `Keep Results`，这里会显示对整个项目搜索（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>）的结果

*Curve Editor* : 用于在[粒子编辑器](/manuals/particlefx/)中编辑曲线。

Tools 面板也用于与集成调试器交互。更多内容请阅读[调试手册](/manuals/debugging/)。

### 6. Changed Files 面板

如果您的项目使用分布式版本控制系统 Git，此视图会列出项目中已修改、添加或删除的文件。通过定期同步项目，可以让本地副本与项目 Git 仓库中存储的内容保持一致，从而便于团队协作，并在出现问题时避免丢失工作。您可以在[版本控制手册](/manuals/version-control/)中了解 Git 的更多信息。此视图中可以执行一些面向文件的操作：

   - <kbd>Left Mouse Click</kbd> - 选择指定文件，按住 <kbd>⇧ Shift</kbd> 可扩展选择，按住 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> 可选择/取消选择点击项。如果选择了单个已更改文件，可以点击 `Diff` 查看差异。可以点击 `Revert` 撤销所有所选文件中的更改。
   - <kbd>Double Left Mouse Click</kbd> 文件可打开该文件视图。编辑器会像 Assets 视图中一样，在合适的编辑器中打开文件。
   - <kbd>Right Mouse Click</kbd> 文件可打开弹出菜单，从中打开差异视图、还原该文件的所有更改、在文件系统中查找文件等。

### 菜单栏

在编辑器视图顶部（或 Mac 的系统菜单栏）可以找到菜单栏，包含 6 个菜单：`File`、`Edit`、`View`、`Project`、`Debug`、`Help`。它们的功能会在各手册中说明。

### 状态栏

编辑器底部栏有一条窄区域显示状态，例如：
- 当有新更新可用时，会显示一个可点击按钮 `Update Available`，请查看本手册后面的“更新编辑器”章节。
- 构建或打包时，进度会显示在这里。

## 面板大小和可见性

可以在编辑器中 <kbd>Dragging</kbd> 上述 6 个面板之间的分隔边界，调整面板大小。

可以通过 `View` 菜单中的选项或给定快捷键切换面板可见性：
- `Toggle Assets Pane`（<kbd>F6</kbd>）切换 Assets 和 Changed Files 面板的可见性
- `Toggle Changed Files` 单独切换 Changed Files 面板的可见性
- `Toggle Tools Pane`（<kbd>F7</kbd>）切换 Tools 面板的可见性
- `Toggle Properties Pane`（<kbd>F8</kbd>）切换 Outline 和 Properties 面板的可见性

![Panes Visibility](images/editor/editor_panes.png)

在 `View` 菜单中，您也可以切换或更改其他可见性相关设置，例如 Grid、Guides、Camera，或将视图适配到选择（`Frame Selection` 或 <kbd>F</kbd> 键），以及在默认 2D 和 3D 视图之间切换（`Realign Camera` 或 <kbd>.</kbd> 键）。其中许多功能也可以从工具栏或快捷键访问。

## 标签页

如果打开了多个文件，每个文件都会在编辑器视图顶部显示一个独立标签页。同一面板中的标签页可以移动；<kbd>Drag and Drop</kbd> 它们即可在标签栏内交换位置。您还可以：

- 在标签页上 <kbd>Right Mouse Click</kbd> 打开 _Context Menu_，
- 点击 `Close`（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>）关闭单个标签页，
- 点击 `Close Others` 关闭除所选标签页以外的所有标签页，
- 点击 `Close All`（<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>）关闭活动面板中的所有标签页，
- 选择 `➝| Open As`，使用非默认编辑器，或使用 `File ▸ Preferences ▸ Code ▸ Custom Editor` 中设置的关联外部工具。请在[首选项手册](/manuals/editor-preferences)中查看更多信息。

![Tabs](images/editor/tabs_custom.png)

## 并排编辑

可以并排打开 2 个编辑器视图。

- <kbd>Right Mouse Click</kbd> 要移动的编辑器标签页，并选择 `Move to Other Tab Pane`。

![2 panes](images/editor/2-panes.png)

您也可以使用标签页菜单中的 `Swap with Other Tab Pane` 在面板之间移动指定标签页，或使用 `Join Tab Panes` 合并为单个面板。

## 创建新的项目文件 {#creating-new-project-files}

要创建新的资源文件，可以选择 `File ▸ New…`，然后从菜单中选择文件类型，或使用上下文菜单：

在 `Assets` 浏览器中的目标位置 <kbd>Right Mouse Click</kbd>，然后选择 `New… ▸ [file type]`：

![create file](images/editor/create_file.png)

为新文件输入合适的 *Name*，并可根据需要更改 *Location*。包含文件类型后缀的完整文件名会显示在对话框的 *Preview* 下：

![create file name](images/editor/create_file_name.png)

## 模板

可以为每个项目指定自定义模板。为此，请在项目根目录中创建名为 `templates` 的新文件夹，并添加带有所需扩展名、名为 `default.*` 的新文件，例如 `/templates/default.gui` 或 `/templates/default.script`。此外，如果这些文件中使用了 `{{NAME}}` 标记，它会被文件创建窗口中指定的文件名替换。

如果某种文件类型有可用模板，每当创建该类型的新文件时，它都会用 `templates` 中对应文件的内容初始化。


![Templates](images/editor/templates.png)

## 将文件导入项目

要向项目添加资源文件（图像、声音、模型等），只需将它们拖放到 *Assets* 浏览器中的正确位置。这会在项目文件结构中的所选位置创建这些文件的_副本_。请阅读[如何导入资源的手册](/manuals/importing-assets/)了解更多信息。

![Import files](images/editor/import.png)

## 更新编辑器

连接互联网时，编辑器会自动检查更新。检测到更新时，项目选择界面左下角或编辑器窗口右下角会显示蓝色可点击链接 `Update Available`。

![Update from project selection](images/editor/update_start.png)
![Update from Editor](images/editor/update_available.png)

点击 `Update Available` 可点击链接以下载并更新。会弹出带信息的确认窗口，点击 `Download Update` 继续。

![Update Editor popup](images/editor/update.png)

您会在底部状态栏看到下载进度：

![Download progress](images/editor/download_status.png)

更新下载完成后，蓝色链接会变为 `Restart to Update`。点击它可重启并打开更新后的编辑器。

![Restart to update](images/editor/restart_to_update.png)

## 首选项

您可以在 `Preferences` 窗口中修改编辑器设置。要打开它，请点击 `File ▸ Preferences…`，或使用快捷键 <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

更多细节请阅读[首选项手册](/manuals/editor-preferences)

![Preferences](images/editor/preferences.png)

## 编辑器日志 {#editor-logs}
如果您遇到编辑器问题并需要报告问题（`Help  ▸ Report Issue`），最好提供编辑器自身的日志文件。要在系统浏览器中打开日志位置，请点击 `Help ▸ Show Logs`。

更多内容请阅读[获取帮助手册](/manuals/getting-help/#getting-help)。

![Show Logs](images/editor/show_logs.png)

编辑器日志文件可以在这里找到：

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` 或 `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` 或 `~/.local/state/Defold`

如果编辑器从终端/命令提示符启动，也可以在编辑器运行时访问编辑器日志。使用以下命令启动编辑器：

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## 编辑器服务器

编辑器打开项目时，会在随机端口上启动一个 Web 服务器。该服务器可用于从其他应用程序与编辑器交互。端口会写入 `.internal/editor.port` 文件。

服务器会在 `http://localhost:$(cat .internal/editor.port)/openapi.json` 提供 OpenAPI 规范。这是代理式工作流的一个有用的最小起点。

此外，编辑器可执行文件带有命令行选项 `--port`（或 `-p`），允许在启动期间指定端口，例如::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## 编辑器安装元数据

编辑器启动时，会将启动器和安装路径的信息写入一个已知位置。第三方 IDE 集成和其他工具可以使用这些信息查找已安装的 Defold 编辑器：

| OS      | 位置 |
|---------|------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

该文件包含一个 JSON 数组，每个已知安装对应一个对象：

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## 编辑器样式

可以通过自定义样式改变编辑器外观。请阅读[编辑器样式手册](/manuals/editor-styling)了解更多信息。

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
