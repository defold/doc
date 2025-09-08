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
: 如果您想创建一个新的 Defold 项目，请点击此选项，然后选择您是否希望基于基本模板创建项目（来自*From Template*标签页），是否想要按照教程操作（*From Tutorial*标签页），或者尝试其中一个示例项目（*From Sample*标签页）。

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

*Properties* 面板
: 这个视图显示出当前选中物体的属性, 比如位置, 旋转, 动画等等.

*Tools* 面板
: 这个视图分为几个组. *Console* 组显示游戏输出和报错信息. 旁边是显示 *编译错误*, *查找结果* 和编辑粒子曲线数据时用到的 *曲线编辑器*. 同时工具面板也负责与调试器进行交互.

*Changed Files* 面板
: 如果你的项目使用 Git 做版本控制, 这个视图会列出项目中被修改, 添加或者删除的文件. 同步机制会把你的本地项目文件与 Git 托管项目进行同步, 这种机制方便团队合作开发, 而且云端备份可以保证项目不易损坏丢失. 关于 Git 详见 [版本控制教程](/manuals/version-control/). 相关操作:

   - <kbd>双击</kbd> 文件显示版本区别窗口. 同样, 编辑器会根据文件类型选择合适的显示窗口.
   - <kbd>右键点击</kbd> 文件弹出的上下文菜单中, 可以进行显示版本区别窗口, 回退文件的更改, 打开文件系统浏览器显示文件位置等操作.

## 同时编辑

如果同时打开了多个文件, 编辑器视图上方就会出现多个标签. 要想两个视图对照着同时进行编辑工作. <kbd>右键点击</kbd> 想要移动的视图标签, 然后选择 <kbd>Move to Other Tab Pane</kbd>.

![2 panes](images/editor/2-panes.png)

使用视图标签还可以让两个视图交换位置或者把多个面板合为一组.

## 场景编辑器

双击集合文件或者游戏对象文件就会打开 *场景编辑器*:

![Select object](images/editor/select.png)

选择物体
: 在主视图中点选可以选中单个物体. 框选可以选中绿色方框套住的多个物体. 被选中的物体则在 *大纲* 视图中被高亮显示.

  大纲中还可以:

  - <kbd>点击左键拖拉</kbd> 框选中多个物体.
  - <kbd>单击</kbd> 选中单个物体.

  按住 <kbd>Shift</kbd> 或 <kbd>⌘</kbd> (Mac) / <kbd>Ctrl</kbd> (Win/Linux) 键可以在已选中物体的基础上增选物体.

移动工具
: ![Move tool](images/editor/icon_move.png){.left}
  使用 *移动工具* 来移动物体. 移动工具位于场景编辑器右上角的工具栏内, 快捷键是 <kbd>W</kbd>.

  ![Move object](images/editor/move.png)

  被选中的物体会显示出坐标轴 (方块和箭头). 拖拽绿方块可以在屏幕空间内任意移动这个物体, 拖拽箭头则是让这个物体在 X, Y 或 Z 轴上进行移动. 拖拽别的方块则可以让这个物体在 X-Y 平面上 (在3D视图中可见) 移动或者在 X-Z , Y-Z 平面上移动.

旋转工具
: ![Rotate tool](images/editor/icon_rotate.png){.left}
  使用 *旋转工具* 来旋转物体. 旋转工具位于场景编辑器右上角的工具栏内, 快捷键是 <kbd>E</kbd>.

  ![Move object](images/editor/rotate.png)

  旋转工具的坐标轴显示为圆形. 拖拽橙色的圆可以在屏幕空间内任意旋转这个物体, 可以沿着 X, Y 和 Z 轴旋转. 因为 X 和 Y 轴的位置关系, 在2D视图上仅显示为穿过物体的两条线.

缩放工具
: ![Scale tool](images/editor/icon_scale.png){.left}
  使用 *缩放工具* 来缩放物体. 缩放工具位于场景编辑器右上角的工具栏内, 快捷键是 <kbd>R</kbd>.

  ![Scale object](images/editor/scale.png)

  缩放工具坐标轴显示为一组方块. 拖拽中间的方块可以将物体等比缩放 (包括Z轴). 同样也可以沿着 X, Y 和 Z 轴方向, 以及 X-Y , X-Z 和 Y-Z 平面上进行缩放.

可见性过滤
: 各种组件类型的可视性开关, 包括边界框和基准线.

  ![Visibility filters](images/editor/visibilityfilters.png)


## 创建新的项目文件

要创建新的资源文件，可以选择<kbd>文件 ▸ 新建...</kbd>，然后从菜单中选择文件类型，或者使用上下文菜单：

在*资源*浏览器中的目标位置<kbd>右键单击</kbd>，然后选择<kbd>新建... ▸ [文件类型]</kbd>：

![create file](images/editor/create_file.png)

为新文件键入合适的名称。包含文件类型后缀的完整文件名显示在对话框的*路径*下：

![create file name](images/editor/create_file_name.png)

可以为每个项目指定自定义模板。为此，请在项目根目录中创建一个名为`templates`的新文件夹，并添加名为`default.*`的新文件，并带有所需的扩展名，例如`/templates/default.gui`或`/templates/default.script`。此外，如果在这些文件中使用了`{{NAME}}`标记，它将被文件创建窗口中指定的文件名替换。

## 向项目添加资源文件

要向项目添加资源 (图片, 声音, 模型等) 文件, 只需把文件拖放到 *资源* 浏览器里适当的位置上. 这样做实际上是把文件系统中的资源文件 _拷贝_ 到项目中来. 详情请见 [导入资源教程](/manuals/importing-assets/).

![Import files](images/editor/import.png)

## 编辑器更新

编辑器自动检查更新. 检测到新版本的话就会在编辑器右下角或者项目选择视图里显示出来. 点击即可自动更新.

![Update from project selection](images/editor/update-project-selection.png)

![Update from editor](images/editor/update-main.png)

## 配置

可以 [通过设置窗口](/manuals/editor-preferences) 修改编辑器配置.

## 键盘快捷键

键盘快捷键及自定义方法详见 [键盘快捷键教程](/manuals/editor-keyboard-shortcuts).

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

当编辑器打开项目时，它会在随机端口上启动一个Web服务器。该服务器可用于从其他应用程序与编辑器交互。从1.11.0版本开始，端口被写入`.internal/editor.port`文件中。

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
