---
title: Defold 中的碰撞对象
brief: 碰撞对象是用于给游戏对象赋予物理行为的组件。碰撞对象具有物理属性和空间形状。
---

# 碰撞对象

碰撞对象是用于给游戏对象赋予物理行为的组件。碰撞对象具有物理属性，如重量、弹性和摩擦力，其空间范围由您附加到组件的一个或多个 _形状_ 定义。Defold 支持以下类型的碰撞对象：

Static objects
: 静态对象永远不会移动，但与静态对象碰撞的动态对象会通过反弹和/或滑动做出反应。静态对象对于构建不会移动的关卡几何体（即地面和墙壁）非常有用。它们在性能方面也比动态对象更便宜。您不能移动或以其他方式更改静态对象。

Dynamic objects
: 动态对象由物理引擎模拟。引擎解决所有碰撞并应用产生的力。动态对象适用于应该表现得真实的对象。影响它们的最常见方式是间接的，通过[施加力](/ref/physics/#apply_force)或改变角[阻尼](/ref/stable/physics/#angular_damping)和[速度](/ref/stable/physics/#linear_velocity)以及线性[阻尼](/ref/stable/physics/#linear_damping)和[速度](/ref/stable/physics/#angular_velocity)。当在 *game.project* 中启用[允许动态变换设置](/manuals/project-settings/#allow-dynamic-transforms)时，也可以直接操纵动态对象的位置和方向。

Kinematic objects
: 运动学对象会注册与其他物理对象的碰撞，但物理引擎不执行任何自动模拟。解决碰撞或忽略它们的工作留给您来完成（[了解更多](/manuals/physics-resolving-collisions)）。运动学对象非常适合需要精细控制物理反应的玩家或脚本控制的对象，如玩家角色。

Triggers
: 触发器是注册简单碰撞的对象。触发器是轻量级的碰撞对象。它们类似于[射线投射](/manuals/physics-ray-casts)，因为它们读取物理世界而不是与之交互。它们非常适合只需要记录命中（如子弹）的对象，或者作为游戏逻辑的一部分，当对象到达特定点时触发某些动作。触发器在计算上比运动学对象更便宜，如果可能，应该优先使用它们。


## 添加碰撞对象组件

碰撞对象组件有一组 *属性*，用于设置其类型和物理属性。它还包含一个或多个定义物理对象整体形状的 *形状*。

要向游戏对象添加碰撞对象组件：

1. 在 *大纲* 视图中，<kbd>右键点击</kbd>游戏对象并从上下文菜单中选择 <kbd>Add Component ▸ Collision Object</kbd>。这将创建一个没有形状的新组件。
2. <kbd>右键点击</kbd>新组件并选择 <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>。这会向碰撞对象组件添加一个新形状。您可以为组件添加任意数量的形状。您也可以使用瓦片地图或凸包来定义物理对象的形状。
3. 使用移动、旋转和缩放工具编辑形状。
4. 在 *大纲* 中选择组件并编辑碰撞对象的 *属性*。

![Physics collision object](images/physics/collision_object.png)


## 添加碰撞形状

碰撞组件可以使用多个基本形状或单个复杂形状。在[碰撞形状手册](/manuals/physics-shapes)中了解有关各种形状以及如何将它们添加到碰撞组件的更多信息。


## 碰撞对象属性

Id
: 组件的标识符。

Collision Shape
: 此属性用于瓦片地图几何体或不使用基本形状的凸形状。有关更多信息，请参见[碰撞形状](/manuals/physics-shapes)。

Type
: 碰撞对象的类型：`Dynamic`、`Kinematic`、`Static` 或 `Trigger`。如果将对象设置为动态，您 _必须_ 将 *Mass* 属性设置为非零值。对于动态或静态对象，您还应该检查 *Friction* 和 *Restitution* 值是否适合您的用例。

Friction
: 摩擦使对象能够彼此真实地滑动。摩擦值通常设置在 `0`（完全没有摩擦——非常光滑的对象）和 `1`（强摩擦——磨蚀性对象）之间。但是，任何正值都是有效的。

  摩擦强度与法向力成正比（这被称为库仑摩擦）。当计算两个形状（`A` 和 `B`）之间的摩擦力时，两个对象的摩擦值通过几何平均值组合：

```math
F = sqrt( F_A * F_B )
```

  这意味着如果其中一个对象的摩擦为零，那么它们之间的接触将具有零摩擦。

Restitution
: 恢复值设置对象的"弹性"。值通常在 0（非弹性碰撞——对象根本不反弹）和 1（完全弹性碰撞——对象的速度将在反弹中完全反射）之间

  两个形状（`A` 和 `B`）之间的恢复值使用以下公式组合：

```math
R = max( R_A, R_B )
```

  当一个形状产生多个接触时，恢复是近似模拟的，因为 Box2D 使用迭代求解器。当碰撞速度很小时，Box2D 也使用非弹性碰撞以防止反弹抖动

Linear damping
: 线性阻尼减少物体的线性速度。它与摩擦不同，摩擦只在接触期间发生，可以用来给物体一种漂浮的外观，就像它们在比空气更稠密的东西中移动一样。有效值在 0 和 1 之间。

  Box2D 为了稳定性和性能而近似阻尼。在小值时，阻尼效应与时间步长无关，而在较大的阻尼值时，阻尼效应随时间步长而变化。如果您以固定时间步长运行游戏，这永远不会成为问题。

Angular damping
: 角阻尼像线性阻尼一样工作，但减少物体的角速度。有效值在 0 和 1 之间。

Locked rotation
: 设置此属性完全禁用碰撞对象的旋转，无论施加什么力。

Bullet
: 设置此属性启用碰撞对象与其他动态碰撞对象之间的连续碰撞检测（CCD）。如果类型未设置为 `Dynamic`，则忽略 Bullet 属性。

Group
: 对象应属于的碰撞组的名称。您可以有 16 个不同的组，并根据您的游戏需要为它们命名。例如"players"、"bullets"、"enemies"和"world"。如果 *Collision Shape* 设置为瓦片地图，则不使用此字段，但组名取自瓦片源。[了解有关碰撞组的更多信息](/manuals/physics-groups)。

Mask
: 此对象应该与之碰撞的其他 _组_。您可以命名一个组或在逗号分隔的列表中指定多个组。如果将 Mask 字段留空，对象将不会与任何东西碰撞。[了解有关碰撞组的更多信息](/manuals/physics-groups)。

Generate Collision Events
: 如果启用，将允许此对象发送碰撞事件

Generate Contact Events
: 如果启用，将允许此对象发送接触事件

Generate Trigger Events
: 如果启用，将允许此对象发送触发器事件


## 运行时属性

物理对象有许多不同的属性，可以使用 `go.get()` 和 `go.set()` 读取和更改：

`angular_damping`
: 碰撞对象组件的角阻尼值（`number`）。[API 参考](/ref/physics/#angular_damping)。

`angular_velocity`
: 碰撞对象组件的当前角速度（`vector3`）。[API 参考](/ref/physics/#angular_velocity)。

`linear_damping`
: 碰撞对象的线性阻尼值（`number`）。[API 参考](/ref/physics/#linear_damping)。

`linear_velocity`
: 碰撞对象组件的当前线性速度（`vector3`）。[API 参考](/ref/physics/#linear_velocity)。

`mass`
: 碰撞对象组件的已定义物理质量。只读。（`number`）。[API 参考](/ref/physics/#mass)。
