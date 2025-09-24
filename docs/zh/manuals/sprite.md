---
title: 显示 2D 图片
brief: 本手册介绍了如何使用 sprite 组件显示 2D 图片和动画。
---

# 精灵（Sprites）

精灵（Sprite）组件是显示在屏幕上的简单图片或翻页动画。

![sprite](images/graphics/sprite.png)

精灵（Sprite）组件可以使用[图集](/manuals/atlas)或[瓷砖图源](/manuals/tilesource)作为其图形资源。

## 精灵属性

除了 *Id*、*Position* 和 *Rotation* 属性外，还有以下组件特定属性：

*Image*
: 如果着色器有单个采样器，此字段命名为 `Image`。否则，每个槽位以材质中的纹理采样器命名。
  每个槽位指定精灵在该纹理采样器上使用的图集或瓷砖图源资源。

*Default Animation*
: 精灵使用的默认动画。动画信息取自第一个图集或瓷砖图源。

*Material*
: 用于渲染精灵的材质。

*Blend Mode*
: 渲染精灵时使用的混合模式。

*Size Mode*
: 如果设置为 `Automatic`，编辑器将自动设置精灵的大小。如果设置为 `Manual`，您可以手动设置大小。

*Slice 9*
: 设置为在调整精灵大小时保留精灵纹理边缘的像素大小。

:[Slice-9](../shared/slice-9-texturing.md)

### 混合模式
:[blend-modes](../shared/blend-modes.md)

## 运行时操作

您可以通过多种不同的函数和属性在运行时操作精灵（请参阅[API 文档了解用法](/ref/sprite/)）。函数：

* `sprite.play_flipbook()` - 在精灵组件上播放动画。
* `sprite.set_hflip()` 和 `sprite.set_vflip()` - 设置精灵动画的水平翻转和垂直翻转。

精灵还有许多可以使用 `go.get()` 和 `go.set()` 操作的不同属性：

`cursor`
: 归一化的动画游标（`number`）。

`image`
: 精灵图像（`hash`）。您可以使用图集或瓷砖图源资源属性和 `go.set()` 来更改此属性。请参阅[API 参考中的示例](/ref/sprite/#image)。

`material`
: 精灵材质（`hash`）。您可以使用材质资源属性和 `go.set()` 来更改此属性。请参阅[API 参考中的示例](/ref/sprite/#material)。

`playback_rate`
: 动画播放速率（`number`）。

`scale`
: 精灵的非均匀缩放（`vector3`）。

`size`
: 精灵的大小（`vector3`）。只有当精灵的大小模式设置为手动时才能更改。

## 材质常量

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: 精灵的颜色色调（`vector4`）。vector4 用于表示色调，其中 x、y、z 和 w 分别对应红色、绿色、蓝色和 alpha 色调。

## 材质属性

精灵可以覆盖当前分配材质中的顶点属性，并将从组件传递到顶点着色器（请参阅[材质手册了解更多详情](/manuals/material/#attributes)）。

材质中指定的属性将在检查器中显示为常规属性，并且可以在单个精灵组件上设置。如果任何属性被覆盖，它将显示为被覆盖的属性，并存储在磁盘上的精灵文件中：

![sprite-attributes](../images/graphics/sprite-attributes.png)

## 项目配置

*game.project* 文件中有一些与精灵相关的[项目设置](/manuals/project-settings#sprite)。

## 多纹理精灵

当精灵使用多个纹理时，有一些注意事项。

### 动画

动画数据（fps、帧名称）目前取自第一个纹理。我们将其称为"驱动动画"。

驱动动画的图像 ID 用于在另一个纹理中查找图像。
因此，确保纹理之间的帧 ID 匹配非常重要。

例如，如果您的 `diffuse.atlas` 有一个 `run` 动画，如下所示：

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

那么帧 ID 将是 `run/hero_run_color_1`，这不太可能在 `normal.atlas` 中找到：

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

因此，我们在[图集](/manuals/material/)中使用`重命名模式`来重命名它们。
在相应的图集中设置 `_color=` 和 `_normal=`，您将在两个图集中得到如下帧名：

```
run/hero_run_1
run/hero_run_2
...
```

### UV

UV 取自第一个纹理。由于只有一组顶点，如果次级纹理有更多 UV 坐标或不同形状，我们无法保证良好的匹配。

这一点很重要，因此请确保图像具有足够相似的形状，否则您可能会遇到纹理渗色。

每个纹理中图像的尺寸可能不同。
