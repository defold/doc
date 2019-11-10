---
title: 适配游戏图像到不同的屏幕尺寸
brief: 本教程解释了如何适配游戏和图像到不同的屏幕尺寸.
---

# 介绍

当适配游戏和图像到不同的屏幕尺寸时，要考虑一些事情:

* 这是个低分辨率的像素对齐的复古游戏还是高分辨率的现代游戏?
* 不同屏幕全屏模式下玩的时候游戏应该如何应对?
  * 玩家应该在高分辨率屏幕中看到更多的游戏内容还是图像自适应缩放来显示同样多的内容?
* 要是屏幕的长宽比跟在game.project中设置的不一样游戏该怎么办?
  * 玩家看到更多的游戏内容? 还是显示黑边? 还是重新调整GUI大小?
* 你需要什么样的菜单和屏幕gui组件，他们怎么适应各种屏幕大小与方向?
  * 当屏幕方向改变，菜单和屏幕gui组件应该改变布局还是不管什么方向都不动?

本手册将探讨这些事情然后提供建议.


## 内容渲染的方法如何改变

Defold 渲染脚本提供整个渲染管线的全部控制. 渲染脚本控制着显示什么，怎么显示以及显示的顺序. 默认渲染脚本总是显示 *game.project* 文件里定义的长，宽的一块区域, 不管窗口缩放和屏幕大小匹配. 如果窗口大小，比例改变，将会造成内容的拉伸. 有些游戏可能能接受, 但通常当屏幕分辨率或比例改变，应该适当让游戏内容显示的多些或少些, 或者至少在不改变窗口比例的条件下缩放游戏内容. 要改变内容拉伸的现象详情请见 [Render manual](https://www.defold.com/manuals/render/#default-view-projection).


## 复古/8比特图像

复古/8比特图像游戏模拟了老式游戏机或者低分辨率低调色盘的电脑游戏. 比如任天堂红白机 (NES) 就是分辨率 256x240 的, Commodore 64 是 320x200 的， Gameboy 是 160x144 的, 这些屏幕分辨率赶不上当前屏幕的零头. 为了在当今高分辨率屏幕上模拟这种风格的游戏需要把屏幕缩放好几倍. 一个简单的方法是先显示低分辨率图像然后再在渲染时放大. 这在Defold中使用渲染脚本就能做到，[固定映射](/manuals/render/#fixed-projection) 可以设置一个合适的放大值.

比如使用这个瓷砖图集和角色 ([source](https://ansimuz.itch.io/grotto-escape-game-art-pack)) 来模拟一个8位 320x200 分辨率游戏:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

在 *game.project* 文件中设置分辨率 320x200  然后编译，游戏看起来是这样:

![](images/screen_size/retro-original_320x200.png)

对于现代分辨率屏幕来说窗口也太小了! 把窗口拖动放大到 1280x800 还舒服些:

![](images/screen_size/retro-original_1280x800.png)

现在窗口感觉好多了，我们还需调整图像，因为太小了难以看清游戏内容. 我们用渲染脚本来设置一个固定放大的映射:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

结果会变成这样:

![](images/screen_size/retro-zoomed_1280x800.png)

好多了. 窗口和图像都可以, 但是仔细看会发现一个明显的问题:

![](images/screen_size/retro-zoomed_linear.png)

图像模糊了! 因为GPU渲染纹理时放大了图形采样. 默认 *game.project* 文件里 Graphics 部分设置是 *linear*:

![](images/screen_size/retro-settings_linear.png)

现在改成 *nearest* 试试:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

现在我们的游戏图像是像素对齐的了. 还可以想想其他办法, 比如在*game.project*的sprite里关闭 sub-pixels:

![](images/screen_size/retro-subpixels.png)

当Subpixels选项关闭后所有 sprites 就不会渲染在半个像素上而是永远像素对齐.

## 高分辨率图像

处理高分辨率图像我们需要使用复古游戏不同的方法. 做位图时就要做成高分辨率屏幕下 1:1 大小的图.

同样也需要更改渲染脚本. 这次我们需要按原始比例显示图像:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

这样就确保了游戏像 *game.project* 设置的那样始终显示等比的内容, 如果宽高比与设置不符，游戏边缘可能会显示出额外的内容.

在 *game.project* 文件中可以设置设计时屏幕宽和高.

### 高分辨率视网膜屏幕

想要支持高分辨率视网膜屏幕可以在 *game.project* 文件里打开这个选项:

![](images/screen_size/highdpi-enabled.png)

选中这个选项就打开了高分辨率后台缓冲. 游戏会以设置好的宽高双倍比例渲染, 但是游戏分辨率不变. 也就是说游戏内容是1倍大小的就照常显示. 但是如果内容是双倍大小再在游戏里缩小为1倍的话就是高清渲染了.


## 创建可适配性 GUI

系统的 GUI 组件由各种元素组成, 或称作 [节点](/manuals/gui/#node-types), 虽然看起来很简单却能创造出从按钮到复杂的菜单和弹框等各种界面. GUI 可以设计成自动适配屏幕尺寸和方向的. 比如让节点保持在屏幕顶部, 底部或边上而不改变自身的大小. 也可以设置成对于不同屏幕尺寸和方向自动调整节点关系大小与形态.

### 节点属性

gui中的节点包含锚点, 横轴纵轴以及一个调整模式.

* 锚点定义了节点的中心.
* 锚点模式控制着当屏幕边界或者其父节点边界在适配物理屏幕时拉伸的话，节点自身在水平和垂直方向位置如何修改.
* 调整模式控制着当屏幕边界或者其父节点边界在适配物理屏幕时，节点自身该怎样做.

详情请见 [GUI手册](/manuals/gui/#node-properties).

### 布局

Defold支持GUI在手机上自动适配屏幕方向. 此功能让你能把GUI设计成适配各种各样屏幕比例和方向的. 也可以用来创建特定设备上的界面布局. 详情请见 [GUI 布局手册](/manuals/gui-layouts/)


## 测试不同的屏幕尺寸

Debug 菜单有用来模拟特定设备分辨率或者自定义分辨率的选项. 当应用运行时你可以通过选择 <kbd>Debug->Simulate Resolution</kbd> 然后从列表中选择一个模拟设备. 运行中的应用会自动缩放来测试游戏运行在不同分辨率和屏幕比例的设备上的样子.

![](images/screen_size/simulate-resolution.png)
