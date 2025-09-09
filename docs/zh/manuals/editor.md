---
title: 编辑器概述
brief: 本手册提供了 Defold 编辑器的外观和工作方式的概述，以及如何在其中导航。
---

# 编辑器概述

编辑器允许您以高效的方式浏览和操作游戏项目中的所有文件。编辑文件会调出合适的编辑器，并在单独的视图中显示文件的所有相关信息。

## 启动编辑器

当您运行 Defold 编辑器时，会看到一个项目选择和创建界面。点击选择您想要执行的操作：

Home
: 点击显示您最近打开的项目，以便您可以快速访问它们。这是默认视图。

New Project
: 如果您想创建一个新的 Defold 项目，请点击此选项，然后选择您是否希望基于基本模板创建项目（来自 *来自模板* 标签页），是否想要按照教程操作（*来自教程* 标签页），或者尝试其中一个示例项目（*来自示例* 标签页）。

  ![new project](images/editor/new_project.png)

  当您创建一个新项目时，它会存储在您的本地驱动器上，您所做的任何编辑都会在本地保存。

您可以在[项目设置手册](https://www.defold.com/manuals/project-setup/)中了解有关不同选项的更多信息。

## 编辑器面板

Defold 编辑器被划分为许多面板, 或称视图, 以展示和编辑数据.

![Editor 2](images/editor/editor2_overview.png)

*Assets* 面板
: 展示项目的所有文件. 点选和滚动鼠标滚轮可以在面板上滑动. 在这个视图上可以做的操作有:

   - <kbd>双击</kbd> 文件会根据文件类型启动相应的编辑器打开文件.
   - <kbd>拖放</kbd> 文件可以向项目中添加资源或者移动资源到想要的位置.
   - <kbd>右键单击</kbd> 会弹出 _上下文菜单_ , 可以用来进行新建文件/文件夹, 重命名, 删除, 查看文件依赖等操作.

### 编辑器面板
中心视图显示当前打开的文件在该文件类型的编辑器中。所有可视化编辑器都允许您更改摄像机视图：

- 平移：<kbd>Alt + 鼠标左键</kbd>。
- 缩放：<kbd>Alt + 右键</kbd>（三键鼠标）或 <kbd>Ctrl + 鼠标键</kbd>（单键鼠标）。如果您的鼠标有滚轮，可以使用它来缩放。
- 3D旋转：<kbd>Ctrl + 鼠标左键</kbd>。

在场景视图的右上角有一个工具栏，您可以在其中找到对象操作工具：*移动*、*旋转*和*缩放*，以及*2D模式*、*摄像机透视*和*可见性过滤器*。

![toolbar](images/editor/toolbar.png)

### 大纲面板
此视图显示当前正在编辑的文件内容，但是以分层树结构的形式。大纲反映了编辑器视图，允许您对项目执行操作：
   - <kbd>单击</kbd>选择一个项目。按住<kbd>Shift</kbd>或<kbd>Option</kbd>键可以扩展选择。
   - <kbd>拖放</kbd>移动项目。将游戏对象拖放到集合中的另一个游戏对象上可以使其成为子对象。
   - <kbd>右键单击</kbd>打开_上下文菜单_，您可以从中添加项目、删除选中的项目等。

可以通过单击列表中元素右侧的小眼睛图标来切换游戏对象和可视化组件的可见性（Defold 1.9.8及更新版本）。

![toolbar](images/editor/outline.png)

### Properties面板
此视图显示与当前所选项目相关联的属性，如位置、旋转、动画等。

### Tools面板
此视图有几个标签。*控制台* 标签显示游戏运行时产生的任何错误输出或您有意打印的内容。控制台旁边是包含 *构建错误*、*搜索结果* 和 *曲线编辑器* 的标签，后者用于在粒子编辑器中编辑曲线。Tools 面板还用于与集成调试器交互。

### Changed Files面板
如果你的项目使用 Git 做版本控制, 这个视图会列出项目中被修改, 添加或者删除的文件. 同步机制会把你的本地项目文件与 Git 托管项目进行同步, 这种机制方便团队合作开发, 而且云端备份可以保证项目不易损坏丢失. 关于 Git 详见 [版本控制教程](/manuals/version-control/). 相关操作:

   - <kbd>双击</kbd> 文件显示版本区别窗口. 同样, 编辑器会根据文件类型选择合适的显示窗口.
   - <kbd>右键点击</kbd> 文件弹出的上下文菜单中, 可以进行显示版本区别窗口, 回退文件的更改, 打开文件系统浏览器显示文件位置等操作.

## 同时编辑

如果同时打开了多个文件, 编辑器视图上方就会出现多个标签. 可以并排打开2个编辑器视图。<kbd>右键单击</kbd>想要移动的编辑器标签并选择<kbd>移动到另一个标签面板</kbd>。

![2 panes](images/editor/2-panes.png)

您还可以使用标签菜单交换两个面板的位置并将它们合并为单个面板。

## 场景编辑器

双击集合或游戏对象文件会打开*场景编辑器*：

![Select object](images/editor/select.png)

### 选择对象
点击主窗口中的对象来选择它们。编辑器视图中围绕对象的矩形将高亮显示为绿色，以指示选择了哪个项目。所选对象也在*大纲*视图中高亮显示。

  您还可以通过以下方式选择对象：

  - <kbd>单击并拖动</kbd>以选择选择区域内的所有对象。
  - <kbd>单击</kbd>大纲视图中的对象。

  按住<kbd>Shift</kbd>或<kbd>⌘</kbd>(Mac)/<kbd>Ctrl</kbd>(Win/Linux)键的同时单击以扩展选择。

### 移动工具
![Move tool](images/editor/icon_move.png){.left}
要移动对象，请使用*移动工具*。您可以在场景编辑器右上角的工具栏中找到它，或按<kbd>W</kbd>键。

![Move object](images/editor/move.png)

所选对象显示一组操纵器（方块和箭头）。单击并拖动绿色中心方块手柄可在屏幕空间中自由移动对象，单击并拖动箭头可沿X、Y或Z轴移动对象。还有一些方形手柄用于在X-Y平面中移动对象，以及（如果在3D中旋转相机可见）用于在X-Z和Y-Z平面中移动对象。

### 旋转工具
![Rotate tool](images/editor/icon_rotate.png){.left}
要旋转对象，请通过在工具栏中选择它或按<kbd>E</kbd>键来使用*旋转工具*。

![Move object](images/editor/rotate.png)

该工具由四个圆形操纵器组成。一个橙色操纵器在屏幕空间中旋转对象，以及围绕X、Y和Z轴中的每一个旋转的操纵器。由于视图垂直于X轴和Y轴，因此圆仅显示为穿过对象的两条线。

### 缩放工具
![Scale tool](images/editor/icon_scale.png){.left}
要缩放对象，请通过在工具栏中选择它或按<kbd>R</kbd>键来使用*缩放工具*。

![Scale object](images/editor/scale.png)

该工具由一组方形手柄组成。中心一个在所有轴（包括Z）中均匀缩放对象。每个X、Y和Z轴还有一个手柄用于缩放，以及一个用于在X-Y平面、X-Z平面和Y-Z平面中缩放的手柄。

### 可见性过滤器
切换各种组件类型以及边界框和指南的可见性。

![Visibility filters](images/editor/visibilityfilters.png)

## 创建新的项目文件

要创建新的资源文件，可以选择<kbd>文件 ▸ 新建...</kbd>，然后从菜单中选择文件类型，或者使用上下文菜单：

在*资源*浏览器中的目标位置<kbd>右键单击</kbd>，然后选择<kbd>新建... ▸ [文件类型]</kbd>：

![create file](images/editor/create_file.png)

为新文件键入合适的名称。包含文件类型后缀的完整文件名显示在对话框的*路径*下：

![create file name](images/editor/create_file_name.png)

可以为每个项目指定自定义模板。为此，请在项目根目录中创建一个名为`templates`的新文件夹，并添加名为`default.*`的新文件，并带有所需的扩展名，例如`/templates/default.gui`或`/templates/default.script`。此外，如果在这些文件中使用了`{{NAME}}`标记，它将被文件创建窗口中指定的文件名替换。

## 导入文件到项目

要向项目添加资源文件（图像、声音、模型等），只需将它们拖放到*资源*浏览器中的正确位置。这将在项目文件结构的选定位置创建文件的副本。阅读更多关于[如何在手册中导入资源](/manuals/importing-assets/)的信息。

![Import files](images/editor/import.png)

## 更新编辑器

编辑器将自动检查更新。当检测到更新时，它将在编辑器窗口的右下角和项目选择屏幕上显示。按可用更新链接将下载并更新编辑器。

![Update from project selection](images/editor/update-project-selection.png)

![Update from editor](images/editor/update-main.png)

## 首选项

您可以从[首选项窗口](/manuals/editor-preferences)修改编辑器的设置。

## 编辑器日志
如果您在使用编辑器时遇到问题并需要[报告问题](/manuals/getting-help/#getting-help)，最好提供编辑器本身的日志文件。编辑器日志文件可以在以下位置找到：

  * Windows: `C:\Users\ **您的用户名** \AppData\Local\Defold`
  * macOS: `/Users/ **您的用户名** /Library/Application Support/` 或 `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` 或 `~/.local/state/Defold`

如果编辑器是从终端/命令提示符启动的，您也可以在编辑器运行时访问编辑器日志。要从终端在macOS上启动编辑器：

```
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## 编辑器服务器

当编辑器打开项目时，它会在随机端口上启动Web服务器。该服务器可用于从其他应用程序与编辑器交互。从1.11.0版本开始，端口被写入`.internal/editor.port`文件中。

此外，从1.11.0版本开始，编辑器可执行文件有一个命令行选项`--port`（或`-p`），允许在启动时指定端口，例如：
```shell
# 在Windows上
.\Defold.exe --port 8181

# 在Linux上：
./Defold --port 8181

# 在macOS上：
./Defold.app/Contents/MacOS/Defold --port 8181
```

## 常见问题
:[Editor FAQ](../shared/editor-faq.md)
