---
title: Physics joints in Defold
brief: Defold supports joints for 2D physics. This manual explains how to create and work with joints.
---

# Joints

Defold supports joints for 2D physics. A joint connects two collision objects using some kind of constraint. The supported joint types are:

* **Fixed (physics.JOINT_TYPE_FIXED)** - A rope joint that restricts the maximum distance between two points. In Box2D referred to as a Rope joint.
* **Hinge (physics.JOINT_TYPE_HINGE)** - A hinge joint specifies an anchor point on two collision objects and moves them so that the two collision objects are always in the same place, and the relative rotation of the collision objects is not restricted. The hinge joint can enable a motor with a defined maximum engine torque and speed. In Box2D referred to as a Revolute joint.
* **Spring (physics.JOINT_TYPE_SPRING)** - A spring joint keeps two collision objects at a constant distance from each other. The spring joint can be made soft like a spring with a frequency and damping ratio. In Box2D referred to as a Distance joint.
* **Slider (physics.JOINT_TYPE_SLIDER)** - A slider joint allows for relative translation of two collision objects along a specified axis and prevents relative rotation. In Box2D referred to as a Prismatic joint.

## Creating joints

Joints can currently only be created programmatically using [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Editor support for creating joints is planned but no release date has been decided.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

The above will create a fixed joint with id `my_test_joint` connected between the two collision object `obj_a#collisionobject` and `obj_b#collisionobject`. The joint is connected 10 pixels to the left of the center of collision object `obj_a#collisionobject` and 20 pixels above the center of collision object `obj_b#collisionobject`. The maximum length of the joint is 20 pixels.

## Destroying joints

A joint can be destroyed using [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Reading from and updating joints

The properties of a joint can be read using [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) and set using [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- increase motor speed by 100 revolutions per second
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Get joint reaction force and torque

The reaction force and torque applied to a joint can be read using [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) and [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
