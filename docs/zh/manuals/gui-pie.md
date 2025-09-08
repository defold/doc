---
title: GUI饼状图节点在Defold中
brief: 本手册解释了如何在Defold GUI场景中使用饼状图节点。
---

# GUI饼状图节点

饼状图节点用于创建圆形或椭圆形对象，范围从普通圆形到饼形和方形环形。

## 创建饼状图节点

在*Outline*中的*Nodes*部分<kbd>右键点击</kbd>并选择<kbd>Add ▸ Pie</kbd>。新的饼状图节点被选中，您可以修改其属性。

![创建饼状图节点](images/gui-pie/create.png)

以下属性是饼状图节点特有的：

Inner Radius
: 节点的内半径，沿X轴表示。

Outer Bounds
: 节点外边界的形状。

  - `Ellipse` 将节点扩展到外半径。
  - `Rectangle` 将节点扩展到节点的边界框。

Perimeter Vertices
: 用于构建形状的分段数，表示为完全环绕节点360度周长所需的顶点数。

Pie Fill Angle
: 饼状图应填充多少。表示为从右侧开始的逆时针角度。

![属性](images/gui-pie/properties.png)

如果在节点上设置了纹理，纹理图像将平铺应用，纹理的角与节点边界框的角相对应。

## 运行时修改饼状图节点

饼状图节点响应任何通用的节点操作函数，用于设置大小、轴心、颜色等。还存在一些仅适用于饼状图节点的函数和属性：

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
