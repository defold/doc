---
title: Defold 3D网格
brief: 本手册介绍了如何在您的游戏中运行时创建3D网格。
---

# 网格组件

Defold 的核心是一个3D引擎。即使您只使用2D材质，所有渲染也都是以3D方式完成的，但会正交投影到屏幕上。Defold允许您通过在集合中运行时添加和创建3D网格来利用完整的3D内容。您可以构建纯3D的游戏，只使用3D资源，或者您可以根据需要混合3D和2D内容。

## 创建网格组件

网格组件的创建方式与任何其他游戏对象组件一样。您可以通过两种方式完成：

- 通过在 *Assets* 浏览器中右键点击一个位置并选择 <kbd>New... ▸ Mesh</kbd> 来创建*网格文件*。
- 通过在 *Outline* 视图中右键点击游戏对象并选择 <kbd>Add Component ▸ Mesh</kbd> 来直接将组件嵌入到游戏对象中。

![Mesh in game object](images/mesh/mesh.png)

创建网格后，您需要指定多个属性：

### 网格属性

除了 *Id*、*Position* 和 *Rotation* 属性外，还存在以下组件特定属性：

*Material*
: 用于渲染网格的材质。

*Vertices*
: 描述每个流的网格数据的缓冲文件。

*Primitive Type*
: 线条、三角形或三角形带。

*Position Stream*
: 此属性应为*位置*流的名称。该流会自动作为输入提供给顶点着色器。

*Normal Stream*
: 此属性应为*法线*流的名称。该流会自动作为输入提供给顶点着色器。

*tex0*
: 设置此属性为网格要使用的纹理。

## 编辑器操作

有了网格组件后，您可以使用常规的*场景编辑器*工具自由编辑和操作组件和/或封装的游戏对象，按照您的喜好移动、旋转和缩放网格。

## 运行时操作

您可以使用Defold缓冲区在运行时操作网格。下面是一个使用三角形带创建立方体的示例：

```Lua

-- 立方体
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- 创建带有位置流的缓冲区
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- 获取位置流并写入顶点
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- 将带有顶点的缓冲区设置到网格上
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

有关如何使用网格组件的更多信息，包括示例项目和代码片段，请参阅[论坛公告帖子](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137)。

## 视锥体剔除

网格组件由于其动态特性以及无法确定位置数据的编码方式，因此不会自动剔除。为了剔除网格，需要使用6个浮点数将网格的轴对齐边界框设置为缓冲区上的元数据（AABB最小/最大）：

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## 材质常量

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: 网格的颜色色调（`vector4`）。vector4用于表示色调，其中x、y、z和w分别对应红色、绿色、蓝色和alpha色调。

## 顶点局部空间与世界空间

如果网格材质的顶点空间设置为局部空间，数据将按原样提供给您的着色器，您将必须在GPU上像往常一样变换顶点/法线。

如果网格材质的顶点空间设置为世界空间，您必须提供默认的"位置"和"法线"流，或者您可以在编辑网格时从下拉菜单中选择它。这样引擎就可以将数据转换到世界空间，以便与其他对象进行批处理。
