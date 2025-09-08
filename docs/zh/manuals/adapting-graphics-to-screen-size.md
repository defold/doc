---
title: 适配游戏图像到不同的屏幕尺寸
brief: 本教程解释了如何适配游戏和图像到不同的屏幕尺寸.
---

# 介绍

当适配游戏和图像到不同的屏幕尺寸时, 要考虑一些事情:

* 这是个低分辨率的像素对齐的复古游戏还是高分辨率的现代游戏?
* 不同屏幕全屏模式下玩的时候游戏应该如何应对?
  * 玩家应该在高分辨率屏幕中看到更多的游戏内容还是图像自适应缩放来显示同样多的内容?
* 要是屏幕的长宽比跟在game.project中设置的不一样游戏该怎么办?
  * 玩家看到更多的游戏内容? 还是显示黑边? 还是重新调整GUI大小?
* 你需要什么样的菜单和屏幕gui组件, 他们怎么适应各种屏幕大小与方向?
  * 当屏幕方向改变, 菜单和屏幕gui组件应该改变布局还是不管什么方向都不动?

本教程将探讨这些事情然后提供建议.


## 内容渲染的方法如何改变

Defold 渲染脚本提供整个渲染流程的控制. 渲染脚本控制着显示什么, 怎么显示以及显示的顺序. 默认渲染脚本总是显示 *game.project* 文件里定义的长, 宽的一块区域, 不管窗口是否缩放或实际屏幕分辨率是否匹配。 如果窗口大小, 比例改变, 将会造成内容的拉伸. 有些游戏可能能接受, 但通常当屏幕分辨率或比例改变, 应该适当让游戏内容显示的多些或少些, 或者至少在不改变窗口比例的条件下缩放游戏内容. 要改变内容拉伸的现象详情请见 [渲染手册](/manuals/render/#default-view-projection)。


## 复古/8比特图像

复古/8比特图像游戏模拟了老式游戏机或者低分辨率低调色盘的电脑游戏. 比如任天堂红白机 (NES) 就是分辨率 256x240 的, Commodore 64 是 320x200 的,  Gameboy 是 160x144 的, 这些屏幕分辨率赶不上当前屏幕的零头. 为了在当今高分辨率屏幕上模拟这种风格的游戏需要把屏幕缩放好几倍. 一个简单的方法是先显示低分辨率图像然后再在渲染时放大. 这在Defold中使用渲染脚本就能做到, [固定投影](/manuals/render/#fixed-projection) 可以设置一个合适的放大值。

比如使用这个瓷砖图源和角色 ([source](https://ansimuz.itch.io/grotto-escape-game-art-pack)) 来模拟一个8位 320x200 分辨率游戏:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

在 *game.project* 文件中设置分辨率 320x200  然后编译, 游戏看起来是这样:

![](images/screen_size/retro-original_320x200.png)

对于现代分辨率屏幕来说窗口也太小了! 把窗口拖动放大到 1280x800 还舒服些:

![](images/screen_size/retro-original_1280x800.png)

现在窗口感觉好多了, 我们还需调整图像, 因为太小了难以看清游戏内容. 我们用渲染脚本来设置一个固定放大的映射:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
同样的结果也可以通过将[相机组件](/manuals/camera/)附加到游戏对象上，勾选*正交投影*并将*正交缩放*设置为4.0来实现：

![](images/screen_size/retro-camera_zoom.png)
:::

这将产生以下结果：

![](images/screen_size/retro-zoomed_1280x800.png)

好多了. 窗口和图像都可以, 但是仔细看会发现一个明显的问题:

![](images/screen_size/retro-zoomed_linear.png)

图像模糊了! 因为GPU渲染纹理时放大了图形采样. 默认 *game.project* 文件里 Graphics 部分设置是 *linear*:

![](images/screen_size/retro-settings_linear.png)

现在改成 *nearest* 试试:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

现在我们的游戏图像是像素对齐的了. 还可以想想其他办法, 比如在*game.project*的精灵(sprite)里关闭子像素(Subpixels)：

![](images/screen_size/retro-subpixels.png)

当子像素(Subpixels)选项关闭后所有精灵(sprites)就不会渲染在半个像素上而是永远像素对齐。

## 高分辨率图像

处理高分辨率图像我们需要使用复古游戏不同的方法. 做位图时就要做成高分辨率屏幕下 1:1 大小的图.

同样也需要更改渲染脚本. 这次我们需要按原始比例显示图像:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

这样就确保了游戏像 *game.project* 设置的那样始终显示等比的内容, 如果宽高比与设置不符, 游戏边缘可能会显示出额外的内容.

在 *game.project* 文件中可以设置设计时屏幕宽和高.

### 高DPI设置和视网膜屏幕

如果你还希望支持高分辨率的视网膜屏幕，可以在*game.project*文件的Display部分启用此功能：

![](images/screen_size/highdpi-enabled.png)

这将在支持高DPI的显示器上创建一个高DPI的后台缓冲区。游戏将以设置好的宽高双倍分辨率渲染，但宽度和高度设置仍将是脚本和属性中使用的逻辑分辨率。这意味着所有测量值保持不变，任何以1x比例渲染的内容看起来都一样。但是，如果你导入高分辨率图像并将它们缩放到0.5x，它们在屏幕上将是高DPI的。


## 创建自适应GUI

创建GUI组件的系统由许多基本构建块或[节点](/manuals/gui/#节点类型)组成，虽然看起来非常简单，但可以用来创建从按钮到复杂菜单和弹出窗口的任何内容。您创建的GUI可以配置为自动适应屏幕大小和方向的变化。例如，您可以让节点锚定在屏幕的顶部、底部或侧面，节点可以保持其大小或拉伸。节点之间的关系以及它们的大小和外观也可以配置为在屏幕大小或方向变化时发生变化。

### 节点属性

GUI中的每个节点都有一个枢轴点、水平和垂直锚点以及调整模式。

* 枢轴点定义节点的中心点。
* 锚点模式控制当场景边界或父节点边界被拉伸以适应物理屏幕大小时，节点的垂直和水平位置如何改变。
* 调整模式设置控制当场景边界或父节点边界被调整以适应物理屏幕大小时，节点会发生什么变化。

您可以在[GUI手册](/manuals/gui/#节点属性)中了解更多关于这些属性的信息。

### 布局

Defold支持GUI在移动设备上自动适应屏幕方向变化。通过使用此功能，您可以设计一个能够适应各种屏幕尺寸和方向以及宽高比的GUI。也可以创建匹配特定设备型号的布局。您可以在[GUI布局手册](/manuals/gui-layouts/)中了解更多关于此系统的信息。


## 测试不同的屏幕尺寸

调试菜单包含一个选项，用于模拟特定设备型号分辨率或自定义分辨率。当应用程序运行时，您可以选择<kbd>Debug->Simulate Resolution</kbd>并从列表中选择一个设备型号。运行的应用程序窗口将调整大小，您将能够看到您的游戏在不同分辨率或不同宽高比下的外观。

![](images/screen_size/simulate-resolution.png)
