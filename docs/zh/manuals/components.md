---
title: 游戏对象组件
brief: 本手册提供了组件概览及其使用方法.
---

# 组件

:[组件](../shared/components.md)

## 组件类型

Defold 支持以下组件类型：

* [Collection factory](/manuals/collection-factory) - 生成集合
* [Collection proxy](/manuals/collection-proxy) - 加载和卸载集合
* [Collision object](/manuals/physics) - 2D 和 3D 物理
* [Camera](/manuals/camera) - 更改游戏世界的视口和投影
* [Factory](/manuals/factory) - 生成游戏对象
* [GUI](/manuals/gui) - 渲染图形用户界面
* [Label](/manuals/label) - 渲染一段文本
* [Mesh](/manuals/mesh) - 显示3D网格（具有运行时创建和操作功能）
* [Model](/manuals/model) - 显示3D模型（带有可选动画）
* [Particle FX](/manuals/particlefx) - 生成粒子
* [Script](/manuals/script) - 添加游戏逻辑
* [Sound](/manuals/sound) - 播放声音或音乐
* [Sprite](/manuals/sprite) - 显示2D图像（带有可选翻页动画）
* [Tilemap](/manuals/tilemap) - 显示瓦片网格

可以通过扩展添加其他组件：

* [Rive model](/extension-rive) - 渲染Rive动画
* [Spine model](/extension-spine) - 渲染Spine动画


## 启用和禁用组件

游戏对象的组件在游戏对象创建时被启用。如果您希望禁用组件，可以通过向组件发送[`disable`](/ref/go/#disable)消息来完成：

```lua
-- 禁用与此脚本在同一游戏对象上的id为'weapon'的组件
msg.post("#weapon", "disable")

-- 禁用'enemy'游戏对象上id为'shield'的组件
msg.post("enemy#shield", "disable")

-- 禁用当前游戏对象上的所有组件
msg.post(".", "disable")

-- 禁用'enemy'游戏对象上的所有组件
msg.post("enemy", "disable")
```

要再次启用组件，您可以向组件发送[`enable`](/ref/go/#enable)消息：

```lua
-- 启用id为'weapon'的组件
msg.post("#weapon", "enable")
```

## 组件属性

Defold组件类型都有不同的属性。编辑器中的[属性面板](/manuals/editor/#the-editor-views)将显示[大纲面板](/manuals/editor/#the-editor-views)中当前选定组件的属性。请参考不同组件类型的手册以了解有关可用组件属性的更多信息。

## 组件位置、旋转和缩放

可视组件通常具有位置和旋转属性，大多数情况下还具有缩放属性。这些属性可以从编辑器中更改，并且在几乎所有情况下都不能在运行时更改（唯一的例外是精灵和标签组件缩放，可以在运行时更改）。

如果您需要在运行时更改组件的位置、旋转或缩放，您可以修改组件所属游戏对象的位置、旋转或缩放。这会产生副作用，即游戏对象上的所有组件都会受到影响。如果您希望只操作附加到游戏对象的多个组件中的一个，建议将相关组件移动到单独的游戏对象，并作为该组件原本所属的游戏对象的子游戏对象添加。

## 组件绘制顺序

可视组件的绘制顺序取决于两个方面：

### 渲染脚本谓词
每个组件都被分配一个[材质](/manuals/material/)，每个材质有一个或多个标签。渲染脚本反过来定义多个谓词，每个谓词匹配一个或多个材质标签。渲染脚本[谓词在渲染脚本的*update()*函数中逐个绘制](/manuals/render/#render-predicates)，匹配每个谓词中定义的标签的组件将被绘制。默认渲染脚本首先在一个通道中绘制精灵和瓦片地图，然后在另一个通道中绘制粒子效果，两者都在世界空间中。然后渲染脚本将继续在屏幕空间中的单独通道中绘制GUI组件。

### 组件z值
所有游戏对象和组件都使用vector3对象表示的位置定位在3D空间中。当您以2D查看游戏的图形内容时，X和Y值确定对象在"宽度"和"高度"轴上的位置，而Z位置确定对象在"深度"轴上的位置。Z位置允许您控制重叠对象的可见性：Z值为1的精灵将出现在Z位置0的精灵前面。默认情况下，Defold使用允许Z值在-1和1之间的坐标系：

![model](images/graphics/z-order.png)

匹配[渲染谓词](/manuals/render/#render-predicates)的组件一起绘制，它们绘制的顺序取决于组件的最终z值。组件的最终z值是组件本身的z值、它所属的游戏对象的z值以及任何父游戏对象的z值之和。

::: sidenote
多个GUI组件的绘制顺序**不是**由GUI组件的z值决定的。GUI组件绘制顺序由[gui.set_render_order()](/ref/gui/#gui.set_render_order:order)函数控制。
:::

示例：两个游戏对象A和B。B是A的子对象。B有一个精灵组件。

| 内容     | Z值 |
|----------|-----|
| A        | 2   |
| B        | 1   |
| B#sprite | 0.5 |

![](images/graphics/component-hierarchy.png)

使用上述层次结构，B上精灵组件的最终z值为2 + 1 + 0.5 = 3.5。

::: important
如果两个组件具有完全相同的z值，则顺序是未定义的，您可能会遇到组件来回闪烁或组件在一个平台上以一种顺序渲染而在另一个平台上以另一种顺序渲染的情况。

渲染脚本为z值定义了近裁剪面和远裁剪面。任何z值超出此范围的组件都不会被渲染。默认范围是-1到1，但[可以轻松更改](/manuals/render/#default-view-projection)。当近和远限制为-1和1时，Z值的数值精度非常高。在处理3D资源时，您可能需要在自定义渲染脚本中更改默认投影的近和远限制。有关更多信息，请参见[渲染手册](/manuals/render/)。
:::

:[组件最大数量优化](../shared/component-max-count-optimizations.md)