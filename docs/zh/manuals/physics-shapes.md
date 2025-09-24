---
title: 碰撞形状
brief: 碰撞组件可以使用多个基本形状或单个复杂形状。
---

# 碰撞形状

碰撞组件可以使用多个基本形状或单个复杂形状。

### 基本形状
基本形状有 *盒形*、*球形* 和 *胶囊形*。您可以通过<kbd>右键单击</kbd>碰撞对象并选择<kbd>Add Shape</kbd>来添加基本形状：

![Add a primitive shape](images/physics/add_shape.png)

## 盒形
盒形具有位置、旋转和尺寸（宽度、高度和深度）：

![Box shape](images/physics/box.png)

## 球形
球形具有位置、旋转和直径：

![Sphere shape](images/physics/sphere.png)

## 胶囊形
胶囊形具有位置、旋转、直径和高度：

![Sphere shape](images/physics/capsule.png)

::: important
胶囊形仅在启用3D物理时受支持（在*game.project*文件的物理部分配置）。
:::

### 复杂形状
复杂形状可以由瓦片地图组件创建或由凸包形状创建。

## 瓦片地图碰撞形状
Defold包含一项功能，允许您轻松为瓦片地图使用的瓦片源生成物理形状。[瓦片源手册](/manuals/tilesource/#tile-source-collision-shapes)解释了如何向瓦片源添加碰撞组以及将瓦片分配给碰撞组（[示例](/examples/tilemap/collisions/)）。

要向瓦片地图添加碰撞：

1. 通过<kbd>右键单击</kbd>游戏对象并选择<kbd>Add Component File</kbd>将瓦片地图添加到游戏对象。选择瓦片地图文件。
2. 通过<kbd>右键单击</kbd>游戏对象并选择<kbd>Add Component ▸ Collision Object</kbd>向游戏对象添加碰撞对象组件。
3. 不要向组件添加形状，而是将*Collision Shape*属性设置为*瓦片地图*文件。
4. 像往常一样设置碰撞对象组件的*属性*。

![Tilesource collision](images/physics/collision_tilemap.png)

::: important
请注意，这里的*Group*属性**不**使用，因为碰撞组已在瓦片地图的瓦片源中定义。
:::

## 凸包形状
Defold包含一项功能，允许您从三个或更多点创建凸包形状。

1. 使用外部编辑器创建凸包形状文件（文件扩展名`.convexshape`）。
2. 使用文本编辑器或外部工具手动编辑文件（见下文）
3. 不要向碰撞对象组件添加形状，而是将*Collision Shape*属性设置为*凸包形状*文件。

### 文件格式
凸包文件格式使用与其他所有Defold文件相同的数据格式，即protobuf文本格式。凸包形状定义了包的点。在2D物理中，点应以逆时针顺序提供。在3D物理模式中使用抽象点云。2D示例：

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

上面的示例定义了一个矩形的四个角：

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## 外部工具

有几种不同的外部工具可用于创建碰撞形状：

* CodeAndWeb的[Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold)可用于创建带有精灵和匹配碰撞形状的游戏对象。
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor)可用于创建凸包形状。
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/)可用于创建凸包形状。

# 缩放碰撞形状
碰撞对象及其形状继承游戏对象的缩放比例。要禁用此行为，请取消选中*game.project*文件物理部分中的[Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms)复选框。请注意，仅支持均匀缩放，如果缩放不均匀，将使用最小的缩放值。

# 调整碰撞形状大小
可以在运行时使用`physics.set_shape()`调整碰撞对象的形状大小。示例：

```lua
-- 设置胶囊形状数据
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- 设置球形数据
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- 设置盒形数据
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
碰撞对象上必须已存在具有指定ID的正确类型的形状。
:::

# 旋转碰撞形状

## 在3D物理中旋转碰撞形状
在3D物理中，碰撞形状可以围绕所有轴旋转。


## 在2D物理中旋转碰撞形状
在2D物理中，碰撞形状只能围绕z轴旋转。围绕x或y轴旋转将产生不正确的结果，应避免这样做，即使旋转180度以基本上沿x或y轴翻转形状也不行。要翻转物理形状，建议使用[`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip)和[`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vlip:url-flip)。


# 调试
您可以[启用物理调试](/manuals/debugging/#debugging-problems-with-physics)以在运行时查看碰撞形状。
