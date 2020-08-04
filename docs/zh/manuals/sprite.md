---
title: 显示 2D 图片
brief: 本教程介绍了如何使用 sprite 组件显示 2D 图片和动画.
---

#  Sprites（精灵）

Sprite 组件可以是屏幕上显示的简单图片或者逐帧动画.

![sprite](images/graphics/sprite.png){srcset="images/graphics/sprite@2x.png 2x"}

Sprite 组件使用 [图集](/manuals/atlas) 或者 [瓷砖图源](/manuals/tilesource) 进行图像显示.

## Sprite 属性

除了 *Id*, *Position* 和 *Rotation* 还有如下属性:

*Image*
: 此sprite所使用的图集或者瓷砖图源资源.

*DefaultAnimation*
: 此sprite的默认动画.

*Material*
: 此sprite的渲染材质.

*Blend Mode*
: 此组件渲染时使用的混合模式.

# 运行时操作

运行时可以使用各种各样的函数和属性 (参见 [API 文档](/ref/sprite/))来控制Sprite. 函数:

* `sprite.play_flipbook()` - 在sprite组件上播放动画.
* `sprite.set_hflip()` 和 `sprite.set_vflip()` - 翻转Sprite动画.

还可以使用 `go.get()` 和 `go.set()` 来控制Sprite:

`cursor`
: 初始化动画播放头 (`number`).

`playback_rate`
: 动画播放速率 (`number`).

`scale`
: Sprite缩放 (`vector3`).

`size`
: Sprite大小 (`vector3`) (只读).
