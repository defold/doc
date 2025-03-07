---
title: 显示 2D 图片
brief: 本教程介绍了如何使用 sprite 组件显示 2D 图片和动画.
---

#  Sprites

Sprite 组件可以是屏幕上显示的简单图片或者逐帧动画.

![sprite](images/graphics/sprite.png)

Sprite 组件使用 [图集](/manuals/atlas) 或者 [瓷砖图源](/manuals/tilesource) 进行图像显示.

## Sprite 属性

除了 *Id*, *Position* 和 *Rotation* 还有如下属性:

*Image*
: 如果着色器有单个采样器, 该属性叫做 `Image`. 否则, 每个槽都以材质中的纹理采样器命名.
  每个槽是指该 sprite 用于纹理采样器的图集或者瓷砖图源资源.

*DefaultAnimation*
: sprite的默认动画. 动画信息取自第一个图集或者瓷砖图源.

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

## 材质属性

Sprite 可以覆盖当前分配材质中的顶点属性, 并将从组件传递到顶点着色器 (更多信息参见 [材质教程](/manuals/material/#attributes)).

材质中指定的属性将在检查器中显示为常规属性, 并且可以在单个 Sprite 组件上设置. 如果任何属性被覆盖, 它将显示为被覆盖的属性, 并存储在磁盘上的 sprite 文件中:

![sprite-attributes](../images/graphics/sprite-attributes.png)

::: sidenote
自定义属性自从 Defold 1.4.8 版本可用!
:::

## 相关项目配置

在 *game.project* 文件里有些关于Sprite的 [设置项目](/manuals/project-settings#sprite).

## 多纹理 sprites

当一个 sprite 使用多个纹理时有些问题需要注意.

### 动画

动画数据 (fps, 帧名) 目前取自第一个纹理. 我们把它叫做 "驱动动画".

驱动动画的图片 id 用来查找其他纹理所用图片.
所以确保纹理间的帧 id 匹配是很重要的.

比如你的 `diffuse.atlas` 有一个 `run` 动画如下:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

那么帧 id 就是 `run/hero_run_color_1` 这难以在比如 `normal.atlas` 里找到:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

所以我们在 [图集](/manuals/material/) 里使用 `Rename patterns` 来重命名它们.
在相应图集里设置 `_color=` 和 `_normal=`, 然后你就能在两个图集里得到这样的帧名:

```
run/hero_run_1
run/hero_run_2
...
```

### UVs

UVs 取自第一个纹理. 因为只有一套顶点, 我们不能保证
如果第二个纹理有更多 UV 坐标或者有不同形状都能匹配得当.

所以要记住, 确保图片有足够相似的形状, 否则您可能会遇到纹理渗色.

每个纹理中图像的尺寸可以不同.
