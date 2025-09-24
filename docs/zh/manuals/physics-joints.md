---
title: Defold 中的物理关节
brief: Defold 支持 2D 物理关节。本手册解释了如何创建和使用关节。
---

# 关节

Defold 支持 2D 物理关节。关节使用某种约束连接两个碰撞对象。支持的关节类型有：

* **Fixed (physics.JOINT_TYPE_FIXED)** - 一个限制两点之间最大距离的绳索关节。在 Box2D 中被称为绳索关节。
* **Hinge (physics.JOINT_TYPE_HINGE)** - 铰链关节在两个碰撞对象上指定一个锚点，并移动它们使两个碰撞对象始终在同一位置，碰撞对象的相对旋转不受限制。铰链关节可以启用具有定义的最大引擎扭矩和速度的马达。在 Box2D 中被称为[旋转关节](https://box2d.org/documentation/group__revolute__joint.html#details)。
* **Weld (physics.JOINT_TYPE_WELD)** - 焊接关节试图约束两个碰撞对象之间的所有相对运动。焊接关节可以通过频率和阻尼比使其像弹簧一样柔软。在 Box2D 中被称为[焊接关节](https://box2d.org/documentation/group__weld__joint.html#details)。
* **Spring (physics.JOINT_TYPE_SPRING)** - 弹簧关节使两个碰撞对象保持彼此之间的恒定距离。弹簧关节可以通过频率和阻尼比使其像弹簧一样柔软。在 Box2D 中被称为[距离关节](https://box2d.org/documentation/group__distance__joint.html#details)。
* **Slider (physics.JOINT_TYPE_SLIDER)** - 滑动关节允许两个碰撞对象沿指定轴相对平移，并防止相对旋转。在 Box2D 中被称为[棱柱关节](https://box2d.org/documentation/group__prismatic__joint.html#details)。
* **Wheel (physics.JOINT_TYPE_WHEEL)** - 轮子关节将 `bodyB` 上的一个点限制到 `bodyA` 上的一条线上。轮子关节还提供悬架弹簧。在 Box2D 中被称为[轮子关节](https://box2d.org/documentation/group__wheel__joint.html#details)。

## 创建关节

目前只能通过编程方式使用 [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) 创建关节：
::: sidenote
编辑器支持创建关节的功能已在计划中，但尚未确定发布日期。
:::

```lua
-- 用固定关节约束（绳索）连接两个碰撞对象
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

上述代码将创建一个 ID 为 `my_test_joint` 的固定关节，连接在两个碰撞对象 `obj_a#collisionobject` 和 `obj_b#collisionobject` 之间。关节连接在碰撞对象 `obj_a#collisionobject` 中心左侧 10 像素和碰撞对象 `obj_b#collisionobject` 中心上方 20 像素的位置。关节的最大长度为 20 像素。

## 销毁关节

可以使用 [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) 销毁关节：

```lua
-- 销毁先前连接到第一个碰撞对象的关节
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## 读取和更新关节

可以使用 [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) 读取关节属性，并使用 [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) 设置关节属性：

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- 将马达速度提高每秒 100 转
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## 获取关节反作用力和扭矩

可以使用 [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) 和 [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id) 读取施加到关节的反作用力和扭矩。
