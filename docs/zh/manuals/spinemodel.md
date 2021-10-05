---
title: Defold 中的 Spine 模型组件
brief: 本教程介绍了在Defold中如何创建 SpineModel 组件.
---

# Spine 模型

SpineModel 组件用于把 _Spine_ 骨骼动画在 Defold 中呈现出来.

## 创建 Spine Model 组件

选择一个游戏对象:

方法一 直接创建组件(<kbd>右键点击</kbd> 游戏对象选择 <kbd>Add Component ▸ Spine Model</kbd>)

方法二 先创建文件 (在 *资源* 浏览器中 <kbd>右键点击</kbd>, 在上下文菜单中选择 <kbd>New... ▸ Spine Model</kbd>), 再在游戏对象上 <kbd>右键点击</kbd> , 选择 <kbd>Add Component File</kbd>).

## Spine Model *属性*:

除了常见的 *Id*, *Position* 和 *Rotation* 属性外, 还有 Spine Model 的特有属性:

*Spine scene*
: 设置先前创建的 Spine Scene.

*Blend Mode*
: 默认混合模式是 `Alpha`, 想用别的可以修改这个属性.

*Material*
: 如果想要使用自定义材质显示Spine模型, 在此指定.

*Default animation*
: 设置Spine模型默认的动画.

*Skin*
: 如果模型包含皮肤的话,这里可以设置Spine模型的默认皮肤.

此时就可以在编辑器里看到Spine模型了:

![编辑器中的Spine模型](images/spinemodel/spinemodel.png){srcset="images/spinemodel/spinemodel@2x.png 2x"}

### 混合模式
:[blend-modes](../shared/blend-modes.md)

## 运行时操作

有一系列方法可以在运行时修改Spine模型 (参见 [API文档](/ref/spine/)).

### 运行时动画

Defold 提供强大的运行时控制动画的功能, 参见 [spine 动画教程](/manuals/spine).

### 修改属性

Spine模型可以使用 `go.get()` 和 `go.set()` 方法修改其属性:

`animation`
: 当前Spine模型动画 (`hash`) (只读). 使用 `spine.play_anim()` 方法来更改播放动画 (参见 [spine 动画教程](/manuals/spine)).

`cursor`
: 标准化动画头 (`number`).

`material`
: Spine模型材质 (`hash`). 可使用 `go.set()` 修改. 参见 [这个例子的 API 用法](/ref/spine/#material).

`playback_rate`
: 动画播放速率 (`number`).

`skin`
: 当前组件的皮肤 (`hash`).

## 材质常量

{% include shared/material-constants.md component='spine' variable='tint' %}

`tint`
: 3D网格颜色 (`vector4`). 四元数 x, y, z, 和 w 分别对应红, 绿, 蓝和不透明度.

## 相关项目配置

在 *game.project* 文件里有些关于Spine模型的 [设置项目](/manuals/project-settings#spine).
