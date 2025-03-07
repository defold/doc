---
title: 编辑器概述
brief: 本教程介绍了 Defold 编辑器的外观和用法, 以及切换导航方法.
---

# 编辑器概述

编辑器在布局排版, 切换导航上设计得尽量让游戏开发更有效率. 编辑各个视图里的文件时都会有适当的编辑器自动弹出以方便使用.

## 打开编辑器

打开 Defold 编辑器, 首先呈现的是一个项目选择和新建窗口. 通过点选上面的按钮可以:

Home
: 显示最近编辑的项目以便快速打开. 这是默认视图.

New Project
: 创建新的项目, 然后会让你 (从 *Template* 窗口) 选择是否需要基于模板创建新项目, 还可以选择是否要参考 (*Tutorial* 窗口) 里的教程, 或者学习 (*Sample* 窗口) 里的示例项目.

  ![new project](images/editor/new_project.png)

  新建项目完成后所有项目文件都保存在了本地硬盘上.

详情请见 [项目设立教程](https://www.defold.com/manuals/project-setup/).

## 编辑器面板

Defold 编辑器被划分为许多面板, 或称视图, 以展示和编辑数据.

![Editor 2](images/editor/editor2_overview.png)

*Assets* 面板
: 展示项目的所有文件. 点选和滚动鼠标滚轮可以在面板上滑动. 在这个视图上可以做的操作有:

   - <kbd>双击</kbd> 文件会根据文件类型启动相应的编辑器打开文件.
   - <kbd>拖放</kbd> 文件可以向项目中添加资源或者移动资源到想要的位置.
   - <kbd>右键单击</kbd> 会弹出 _上下文菜单_ , 可以用来进行新建文件/文件夹, 重命名, 删除, 查看文件依赖等操作.

*Editor* 面板

: 中间的视图显示当前打开的文件. 所有可视视图都可以进行如下操作:

- 平移: <kbd>Alt + 鼠标左键</kbd>.
- 缩放: <kbd>Alt + 鼠标右键</kbd> 或者使用鼠标滚轮.
- 旋转: <kbd>Ctrl + 鼠标左键</kbd>.

场景视图右上角的工具栏里也有这些功能按钮: *平移*, *旋转* 和 *缩放*, 以及 *摄像机透视* 和 *可见性过滤*.

![toolbar](images/editor/toolbar.png)

*Outline* 面板
: 这个视图以一个树形结构展示当前打开文件的内容. 大纲树的内容与场景视图内容是一一对应的, 可以方便操作:
   - <kbd>单击</kbd> 选中一个物体. 按住 <kbd>Shift</kbd> 或 <kbd>Option</kbd> 键可以进行多选.
   - <kbd>拖放</kbd> 移动物体. 在集合里把一个游戏对象拖放到另一个游戏对象上可以建立父子关系.
   - <kbd>右键单击</kbd> 弹出 _上下文菜单_ 以便进行添加, 删除选中的物体等操作.

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


## 新建文件

新建资源文件有两种方法, 通过点选菜单栏 <kbd>File ▸ New...</kbd> 按钮, 或者使用上下文菜单:

在 *资源* 浏览器目标位置 <kbd>右键单击</kbd> , 选择 <kbd>New... ▸ [file type]</kbd> 按钮:

![create file](images/editor/create_file.png)

为新文件取一个有意义的名字. 完整文件名包括类型扩展名会显示在 *路径* 对话框内:

![create file name](images/editor/create_file_name.png)

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
使用编辑器时如果遇到了麻烦可以 [向我们汇报](/manuals/getting-help/#获得帮助), 并且连同编辑器日志一起上报. 编辑器日志存放路径如下:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` 或 `~/Library/Application Support/Defold`
  * Linux: `~/.Defold`

如果用命令行启动编辑器那么日志会显示在控制台上. 例如从 macOS 终端启动 Defold 编辑器:

```
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```


## 常見問題
:[Editor FAQ](../shared/editor-faq.md)
