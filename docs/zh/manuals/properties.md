---
title: Defold 中的属性
brief: 本教程介绍了 Defold 中各种属性的使用以及属性动画的制作方法.
---

# 属性

Defold 对于游戏对象, 组件和 GUI 节点暴露了很多可读可写可用作动画的属性. 分为以下各种类型:

* 游戏对象变化 (位置, 旋转和缩放) 和组件属性 (比如 sprite 的 pixel size 或者碰撞对象的 mass)
* Lua 脚本属性 (详情请见 [脚本属性教程](/manuals/script-properties))
* GUI 节点属性
* shaders 和 材质文件里的着色器常量 (详情请见 [材质教程](/manuals/material))

这些属性, 有的用一般函数访问, 有的用特定的函数访问. 大多数都能用于动画. 引擎提供的属性动画功能比(在 `update()` 函数里自己做动画更方便, 而且性能更好.

组合类属性 `vector3`, `vector4` 还有 `quaternion` 包含其子属性 (`x`, `y`, `z` 和 `w`). 可以用属性名加点 (`.`) 来访问. 比如, 设置位置的x子属性:

```lua
-- Set the x positon of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

`go.get()`, `go.set()` 和 `go.animate()` 函数第一个参数是游戏对象引用, 第二个参数是属性id. 游戏对象或者组件的引用可以是字符串, hash 或者 URL. URL 引用详情请见 [定位教程](/manuals/addressing). 属性id是属性名字符串或者hash:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

对于 GUI 节点, 访问属性需要特定函数并且需要提供节点引用作为第一个参数:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
```

## 游戏对象属性和组件属性

所有游戏对象属性和一些组件属性可以在运行时进行读写. 使用 [`go.get()`](/ref/go#go.get) 函数读取属性, 使用 [`go.set()`](/ref/go#go.set) 函数写入属性. 很多属性都可以使用 [`go.animate()`](/ref/go#go.animate) 函数制作属性动画. 还有一小部分属性是只读的.

`get`{.mark}
: 表示可以使用 [`go.get()`](/ref/go#go.get) 读取.

`get+set`{.mark}
: 表示可以使用 [`go.get()`](/ref/go#go.get) 读取并且可以使用 [`go.set()`](/ref/go#go.set) 写入. 数值类型的属性可以使用 [`go.animate()`](/ref/go#go.animate) 制作属性动画.


*游戏对象属性*

| 属性        | 描述                                   | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | 游戏对象的位置坐标. | `vector3`      | `get+set`{.mark} |
| *rotation* | 游戏对象的旋转, 以四元数表示.  | `quaternion` | `get+set`{.mark} |
| *euler*    | 游戏对象的旋转, 以欧拉角表示. | `vector3` | `get+set`{.mark} |
| *scale*    | 游戏对象的非等比缩放, 以向量表示. 比如在 x 和 y 方向放大2倍, 就是 vmath.vector3(2.0, 2.0, 0) | `vector3` | `get+set`{.mark} |

::: sidenote
对于位移专用的函数也是有的; 即 `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()` 和 `go.set_scale()`.
:::

*SPRITE 组件属性*

| 属性   | 描述                            | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | sprite 原始尺寸 --- 从图集图片而定的尺寸. | `vector3` | `get`{.mark} |
| *image* | sprite 纹理路径hash. | `hash` | `get`{.mark}|
| *scale* | sprite 非等比缩放. | `vector3` | `get+set`{.mark}|
| *material* | sprite 使用的材质. | `hash` | `get+set`{.mark}|
| *cursor* | 动画播放头位置 (取值范围 0--1). | `number` | `get+set`{.mark}|
| *playback_rate* | 逐帧动画播放速率. | `number` | `get+set`{.mark}|

*COLLISION OBJECT 组件属性*

| 属性   | 描述                            | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | 碰撞对象的质量. | `number` | `get`{.mark} |
| *linear_velocity* | 碰撞对象当前的线性速度. | `vector3` | `get`{.mark} |
| *angular_velocity* | 碰撞对象当前的旋转速度. | `vector3` | `get`{.mark} |
| *linear_damping* | 碰撞对象当前的线性阻尼. | `vector3` | `get+set`{.mark} |
| *angular_damping* | 碰撞对象当前的旋转阻尼. | `vector3` | `get+set`{.mark} |

*MODEL (3D) 组件属性*

| 属性   | 描述                            | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | 当前动画.                | `hash`          | `get`{.mark}     |
| *texture0* | 模型的纹理路径hash. | `hash` | `get`{.mark}|
| *cursor*  | 当前动画播放头 (取值范围 0-1). | `number`   | `get+set`{.mark} |
| *playback_rate* | 当前动画播放速率. 即播放速度倍数. | `number` | `get+set`{.mark} |
| *material* | 模型所用材质. | `hash` | `get+set`{.mark}|

*LABEL 组件属性*

| 属性   | 描述                            | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | 文本标签的缩放. | `vector3` | `get+set`{.mark} |
| *color*     | 文本标签的颜色. | `vector4` | `get+set`{.mark} |
| *outline* | 文本标签的轮廓. | `vector4` | `get+set`{.mark} |
| *shadow* | 文本标签的阴影. | `vector4` | `get+set`{.mark} |
| *size* | 文本标签的大小. 如果开启换行的话文本标签大小会被约束. | `vector3` | `get+set`{.mark} |
| *material* | 文本标签所用材质. | `hash` | `get+set`{.mark}|
| *font* | 文本标签所用字体. | `hash` | `get+set`{.mark}|


## GUI 节点属性

GUI 节点也有属性, 但是要使用特定的读写函数. 每个属性都有对应的 get- 和 set- 函数. 还有一系列预定义常量可以用于属性动画. 引用属性可以使用属性名字符串, 或者属性名字符串hash.

* `position` (或 `gui.PROP_POSITION`)
* `rotation` (或 `gui.PROP_ROTATION`)
* `scale` (或 `gui.PROP_SCALE`)
* `color` (或 `gui.PROP_COLOR`)
* `outline` (或 `gui.PROP_OUTLINE`)
* `shadow` (或 `gui.PROP_SHADOW`)
* `size` (或 `gui.PROP_SIZE`)
* `fill_angle` (或 `gui.PROP_FILL_ANGLE`)
* `inner_radius` (或 `gui.PROP_INNER_RADIUS`)
* `slice9` (或 `gui.PROP_SLICE9`)

注意颜色属性是一个 vector4 分别对应 RGBA 值:

`x`
: 红色

`y`
: 绿色

`z`
: 蓝色

`w`
: 透明度

*GUI 节点属性*

| 属性   | 描述                            | 类型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | 节点颜色.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | 节点轮廓.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | 节点位置. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | 节点旋转, 以三轴欧拉角表示. | `vector3` | `gui.get_rotation()` `gui.set_rotation()` |
| *scale* | 节点缩放, 以三轴缩放倍数表示. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | 节点阴影. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | 界定非等比大小. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | 饼图填充角, 以逆时针角度表示. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | 饼图内半径. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *slice9* | 九宫格节点四边距. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
