---
title: Defold 中的物理关节
brief: Defold 支持 2D 物理关节约束. 本教程介绍了其用法.
---

# 關節約束

Defold 支持物理关节. 一个关键基于某种限制连接两个物体. 支持的关节类型如下:

* **Fixed (physics.JOINT_TYPE_FIXED)** - 限制两物体最大距离的固定关节. 在 Box2D 被称为绳子关节.
* **Hinge (physics.JOINT_TYPE_HINGE)** - 把两个物体通过一个锚点钉在一起的钉子关节. 两物体相对位置固定而相对旋转没有限制. 这种关节可以开启马达给一个最大扭力与速度. 在 Box2D 被称为旋转关节.
* **Weld (physics.JOINT_TYPE_WELD)** - 用於完全保持對象之間的位置關係的關節. 通過調整頻率和阻尼率軟化的焊接關節可以產生類似彈簧的效果. 在 Box2D 被称为焊接关节.
* **Spring (physics.JOINT_TYPE_SPRING)** - 限制两个物体之间距离范围的弹簧关节. 弹簧关节通过设定其频率和阻尼比可以让物体像是被软弹簧连接. 在 Box2D 被称为距离关节.
* **Slider (physics.JOINT_TYPE_SLIDER)** - 限制两物体只能在某个指定轴上相对移动而不允许相对转动的滑动关节. 在 Box2D 被称为活塞关节.

## 建立关节

目前只能使用 [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) 函数手动建立关节:

::: 注意
编辑器可视环境下创建关节的功能在开发计划中但发布时间未知.
:::

```lua
-- 将两个碰撞物体用固定关节连接 (绳子)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

上述代码创建了一个固定关节, 其id为 `my_test_joint`, 连接了两个物体 `obj_a#collisionobject` 与 `obj_b#collisionobject`. 关节位于 `obj_a#collisionobject` 偏左10像素, `obj_b#collisionobject` 偏上20像素的位置上. 设定的最大距离是20像素.

## 删除关节

可以使用 [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) 函数删除关节:

```lua
-- 删除上面提到的第一个物体上的关节
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## 关节属性及修改

可以使用 [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) 读取关节属性, 使用 [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) 修改关节属性:

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- 马达速度提升每秒100转
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## 关节反作用力和扭矩

可以使用 [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) 读取关节反作用力, 使用 [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id) 读取关节扭力.
