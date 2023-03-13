---
title: 显示 2D 图片
brief: 本教程介绍了如何使用 sprite 组件显示 2D 图片和动画.
---

#  Sprites

Sprite 组件可以是屏幕上显示的简单图片或者逐帧动画.

![sprite](images/graphics/sprite.png){srcset="images/graphics/sprite@2x.png 2x"}

Sprite 组件使用 [图集](/manuals/atlas) 或者 [瓷砖图源](/manuals/tilesource) 进行图像显示.

## Sprite 属性

除了 *Id*, *Position* 和 *Rotation* 还有如下属性:

*Image*
: sprite所使用的图集或者瓷砖图源资源.

*DefaultAnimation*
: sprite的默认动画.

*Material*
: sprite的渲染材质.

*Blend Mode*
: 组件渲染时使用的混合模式.

*Size Mode*
: 如果设置为 `Automatic` 则编辑器会自动为 sprite 设置尺寸. 如果设置为 `Manual` 则可以手动设置尺寸.

*Slice 9*
: 设置在更改 sprite 大小时, 保留其周围边缘纹理的像素大小.

:[Slice-9](../shared/slice-9-texturing.md)

### 混合模式
:[blend-modes](../shared/blend-modes.md)

# 运行时操作

运行时可以使用各种各样的函数和属性 (参见 [API 文档](/ref/sprite/))来控制Sprite. 函数:

* `sprite.play_flipbook()` - 在sprite组件上播放动画.
* `sprite.set_hflip()` 和 `sprite.set_vflip()` - 翻转Sprite动画.

还可以使用 `go.get()` 和 `go.set()` 来控制Sprite:

`cursor`
: 初始化动画播放头 (`number`).

`image`
: sprite图 (`hash`). 可以通过 `go.set()` 方法使用图集或者瓷砖图集资源来修改此属性. 请参考 [这个例子的 API 文档](/ref/sprite/#image).

`material`
: sprite材质 (`hash`). 可以通过 `go.set()` 方法使用材质资源来修改此属性. 请参考 [这个例子的 API 文档](/ref/sprite/#material).

`playback_rate`
: 动画播放速率 (`number`).

`scale`
: Sprite缩放 (`vector3`).

`size`
: Sprite大小 (`vector3`). 只有 sprite 的 size-mode 设置为 manual 时可以更改.

## 材质常量

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: 3D网格颜色 (`vector4`). 四元数 x, y, z, 和 w 分别对应红, 绿, 蓝和不透明度.

## 相关项目配置

在 *game.project* 文件里有些关于Sprite的 [设置项目](/manuals/project-settings#sprite).
