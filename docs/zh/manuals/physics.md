---
title: Defold 中的物理系统
brief: Defold 包含的物理引擎可以基于牛顿物理定律模拟物体运动碰撞时的物理效果. 本教程介绍了物理引擎的使用方法.
---

# 物理

Defold 包含一个修改版的 [Box2D](http://www.box2d.org) 物理引擎 (版本 2.1) 用于模拟2D物理效果和一个 Bullet physics 引擎 (版本 2.77) 用来模拟3D物理效果. 物理引擎可以基于牛顿物理定律模拟各种 _碰撞物体_ 运动碰撞时的物理效果. 本教程介绍了物理引擎的使用方法.

## 碰撞对象

碰撞对象是能给与游戏对象物理行为的组件. 碰撞对象包含许多物理属性比如重量, 弹性, 阻力等等. 组件上定义的一个或多个 _形状_ 决定了它在物理空间中的样子. Defold 支持以下的碰撞对象:

Static objects
: 静态对象不会移动但是能和移动物体进行碰撞. 静态对象很适合制作游戏固定场景元素 (比如地板和墙). 它们比动态对象性能消耗少. 静态对象不能被移动和修改.

Dynamic objects
: 动态对象由物理引擎负责计算位移. 处理碰撞然后给予力. 动态对象看起来很有真实感但是你 *不能* 直接控制它的位置与方向. 要想对其施加影响, 只能向它施加力的作用.

Kinematic objects
: 动画对象可以和其他对象产生碰撞, 但是物理引擎并不处理它们. 忽略碰撞, 或者交给你来处理. 动画对象很适合用作由脚本控制的又能对物理做出反应的物体, 比如游戏角色.

Triggers
: 触发器是记录碰撞的物体. 很适合用作碰撞检测 (比如子弹碰撞) 或者接触后触发时间的场景. 触发器比动画对象节省性能所以可以多用一些.

## 加入 collision object 组件

碰撞对象组件包含一系列 *属性* 用以设定其类型和物理特性. 还包含一个或多个 *形状* 用以定义这个物体的物理形态.

在游戏对象上添加碰撞对象组件:

1. In the *Outline* view, <kbd>right click</kbd> the game object and select <kbd>Add Component ▸ Collision Object</kbd> from the context menu. This creates a new component with no shapes.
2. <kbd>Right click</kbd> the new component and select <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. This adds a new shape to the collision object component. You can add any number of shapes to the component. You can also use a tilemap or a convex hull to define the shape of the physics object.
3. Use the move, rotate and scale tools to edit the shapes.
4. Select the component in the *Outline* and edit the collision object's *Properties*.

![Physics collision object](images/physics/collision_object.png){srcset="images/physics/collision_object@2x.png 2x"}

Id
: 组件名.

Collision Shape
: 这个是针对瓷砖地图的几何形状设置. 详见下文.

Type
: 碰撞对象的类型有: `Dynamic`, `Kinematic`, `Static` 和 `Trigger`. 如果设为动态就 _必须_ 设置其 *Mass* 属性为非0的值. 动态静态碰撞对象都需要为其设置适当的 *Friction* 和 *Restitution* 值.

Friction
: 摩擦可以做出一个物体在另一个物体上滑动的效果. 一般摩擦系数取值范围从 `0` (无摩擦---超级光滑) 到 `1` (强摩擦---超级粗糙) 之间. 但其实任何正数值都有效.

  摩擦力于法方向上的力成正比 (称为库伦摩擦). 计算两个物体 (`A` 和 `B`) 间的摩擦力时, 摩擦系数取两个物体的几何平均值:

  $$
  F_{combined} = \sqrt{ F_A \times F_B }
  $$

  也就是说只要有一个物体是0摩擦的, 两个物体之间就不会有摩擦力.

Restitution
: 弹性是物体的 "反弹性能". 一般取值范围从 0 (非弹性碰撞—一点也不反弹) 到 1 (完全弹性碰撞---物体速度在碰撞后完全反向)

  两个物体 (`A` 和 `B`) 之间的弹性计算基于以下公式:

  $$
  R = \max{ \left( R_A, R_B \right) }
  $$

  当一个形状发生多处碰撞时, 弹性模拟并不精确因为 Box2D 使用的是迭代解算器. Box2D 在碰撞相对速度很小时也使用非弹性碰撞代替, 以防止反弹抖动.


Linear damping
: 线性阻尼会减小刚体的线性速度. 不像摩擦只在物体接触时产生, 线性阻尼始终应用与线性移动的物体上, 给人一种物体飘进比空气密度大的环境中的感觉. 取值范围 0 到 1.

  Box2D 并不精确计算阻尼. 值很小时阻尼与时间无关, 值很大时阻尼随时间变化. 如果时间步固定, 这不会造成问题.

Angular damping
: 角阻尼与线性阻尼类似, 不同的是它减小的是刚体角速度. 取值范围 0 到 1.

Locked rotation
: 关闭碰撞对象的旋转, 无论力如何施加都不会旋转.

Group
: 此碰撞对象所归属的碰撞组. 可以自由定义16个组. 比如 "players", "bullets", "enemies" 或 "world". 如果瓷砖地图上设置了 *Collision Shape*, 则使用的是瓷砖图源里的组名而不是该属性定义的组名.

Mask
: 可以与此对象进行碰撞的 _组_. 如果指定多个, 组名以逗号分割. 如果值为空, 则此对象不与任何物体进行碰撞.

### Collision shapes

碰撞对象的形状可以由多个简单形状组成也可以由一个复杂形状代替. 简单形状有 *box*, *sphere* 和 *capsule*. 复杂形状可以由瓷砖地图生成或者使用凸多边形.

### Box shape
方形设定由位置, 旋转和尺寸 (宽度, 高度和深度) 组成:

![Box shape](images/physics/box.png)

### Sphere shape
圆形设定由位置, 旋转和直径组成:

![Sphere shape](images/physics/sphere.png)

### Capsule shape
胶囊形设定由位置, 旋转, 直径和高度组成:

![Sphere shape](images/physics/capsule.png)

### 瓷砖地图碰撞形状
Defold 包含一个功能就是从瓷砖地图中自动生成物理碰撞形状. [瓷砖地图教程](/manuals/tilemap/) 介绍了新建瓷砖图源的碰撞组与把瓷砖分配给碰撞组的 ([例子](/examples/tilemap/collisions/)).

在瓷砖地图上添加碰撞:

1. Add the tilemap to a game object by <kbd>right-clicking</kbd> the game object and selecting <kbd>Add Component File</kbd>. Select the tile map file.
2. Add a collision object component to the game object by <kbd>right-clicking</kbd> the game object and selecting <kbd>Add Component ▸ Collision Object</kbd>.
3. Instead of adding shapes to the component, set the *Collision Shape* property to the *tilemap* file.
4. Set up the collision object component *Properties* as usual.

![Tilesource collision](images/physics/collision_tilemap.png){srcset="images/physics/collision_tilemap@2x.png 2x"}

::: important
Note that the *Group* property is **not** used here since the collision groups are defined in the tile map's tile source.
:::

### Convex hull shape
Defold includes a feature allowing you to create a convex hull shape from three or more points. You can use an external tool such as the [Defold Polygon Editor](/assets/defoldpolygoneditor/) or the [Physics Body Editor](/assets/physicsbodyeditor/) to create a convex hull shape.

1. Create convex hull shape file (file extension `.convexshape`) using an external editor.
2. Instead of adding shapes to the collision object component, set the *Collision Shape* property to the *convex shape* file.

::: sidenote
The shape will not be drawn in the editor. You can [enable Physics debugging](/manuals/debugging/#debugging-problems-with-physics) at runtime to see the shape.
:::


### Scaling collision shapes

It is possible to let the collision object and its shapes inherit the scale of the game object. Check the [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) checkbox in the Physics section of *game.project* to enable this. Note that only uniform scaling is supported and that the smallest scale value will be used if the scale isn't uniform.


### Rotating collision shapes

### Rotating collision shapes in 3D physics
Collision shapes in 3D physics can be rotated around all axis.


### Rotating collision shapes in 2D physics
Collision shapes in 2D physics can only be rotated around the z-axis. Rotation around the x or y axis will yield incorrect results and should be avoided, even when rotating 180 degrees to essentially flip the shape along the x or y axis. To flip a physics shape it is recommended to use [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) and [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip).


### Units used by the physics engine simulation

The physics engine simulates Newtonian physics and it is designed to work well with meters, kilograms and seconds (MKS) units. Furthermore, the physics engine is tuned to work well with moving objects of a size in the 0.1 to 10 meters range (static objects can be larger) and by default the engine treats 1 unit (pixel) as 1 meter. This conversion between pixels and meters is convenient on a simulation level, but from a game creation perspective it isn't very useful. With default settings a collision shape with a size of 200 pixels would be treated as having a size of 200 meters which is well outside of the recommended range, at least for a moving object. In general it is required that the physics simulation is scaled for it to work well with the typical size of objects in a game. The scale of the physics simulation can be changed in `game.project` via the [physics scale setting](/manuals/project-settings/#physics). Setting this value to for instance 0.02 would mean that 200 pixels would be treated as a 4 meters. Do note that the gravity (also changed in `game.project`) has to be increased to accommodate for the change in scale.

## Group and mask

The physics engine allows you to group your physics objects and filter how they should collide. This is handled by named _collision groups_. For each collision object you create two properties control how the object collides with other objects, *Group* and *Mask*.

For a collision between two objects to register both objects must mutually specify each other's groups in their *Mask* field.

![Physics collision group](images/physics/collision_group.png){srcset="images/physics/collision_group@2x.png 2x"}

The *Mask* field can contain multiple group names, allowing for complex interaction scenarios.


## Collision messages

When two objects collide, the engine will broadcast messages to all components in both objects:

**`"collision_response"`**

This message is sent for all collision objects. It has the following fields set:

`other_id`
: the id of the instance the collision object collided with (`hash`)

`other_position`
: the world position of the instance the collision object collided with (`vector3`)

`other_group`
: the collision group of the other collision object (`hash`)

The collision_response message is only adequate to resolve collisions where you don't need any details on the actual intersection of the objects, for example if you want to detect if a bullet hits an enemy. There is only one of these messages sent for any colliding pair of objects each frame.

**`"contact_point_response"`**

This message is sent when one of the colliding objects is dynamic or kinematic. It has the following fields set:

`position`
: world position of the contact point (`vector3`).

`normal`
: normal in world space of the contact point, which points from the other object towards the current object (`vector3`).

`relative_velocity`
: the relative velocity of the collision object as observed from the other object (`vector3`).

`distance`
: the penetration distance between the objects -- non negative (`number`).

`applied_impulse`
: the impulse the contact resulted in (`number`).

`life_time`
: (*not currently used!*) life time of the contact (`number`).

`mass`
: the mass of the current collision object in kg (`number`).

`other_mass`
: the mass of the other collision object in kg (`number`).

`other_id`
: the id of the instance the collision object is in contact with (`hash`).

`other_position`
: the world position of the other collision object (`vector3`).

`group`
: the collision group of the other collision object (`hash`).

For a game or application where you need to separate objects perfectly, the `"contact_point_response"` message gives you all information you need. However, note that for any given collision pair, several `"contact_point_response"` messages can be received each frame, depending on the nature of the collision. See below for more information.

## Trigger messages

Triggers are light weight collision objects. Thay are similar to ray casts in that they read the physics world as opposed to interacting with it.

In a trigger collision `"collision_response"` messages are sent. In addition, triggers also send a special `"trigger_response"` message when the collision begins and ends. The message has the following fields:

`other_id`
: the id of the instance the collision object collided with (`hash`).

`enter`
: `true` if the interaction was an entry into the trigger, `false` if it was an exit. (`boolean`).

## Resolving kinematic collisions

Using kinematic collision objects require you to resolve collisions yourself and move the objects as a reaction. A naive implementation of separating two colliding objects looks like this:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

This code will separate your kinematic object from other physics object it penetrates, but the separation often overshoots and you will see jitter in many cases. To understand the problem better, consider the following case where a player character has collided with two objects, *A* and *B*:

![Physics collision](images/physics/collision_multi.png){srcset="images/physics/collision_multi@2x.png 2x"}

The physics engine will send multiple `"contact_point_response"` message, one for object *A* and one for object *B* the frame the collision occurs. If you move the character in response to each penetration, as in the naive code above, the resulting separation would be:

- Move the character out of object *A* according to its penetration distance (the black arrow)
- Move the character out of object *B* according to its penetration distance (the black arrow)

The order of these is arbitrary but the result is the same either way: a total separation that is the *sum of the individual penetration vectors*:

![Physics separation naive](images/physics/separation_naive.png){srcset="images/physics/separation_naive@2x.png 2x"}

To properly separate the character from objects *A* and *B*, you need to handle each contact point's penetration distance and check if any previous separations have already, wholly or partially, solved the separation.

Suppose that the first contact point message comes from object *A* and that you move the character out by *A*'s penetration vector:

![Physics separation step 1](images/physics/separation_step1.png){srcset="images/physics/separation_step1@2x.png 2x"}

Then the character has already been partially separated from *B*. The final compensation necessary to perform full separation from object *B* is indicated by the black arrow above. The length of the compensation vector can be calculated by projecting the penetration vector of *A* onto the penetration vector of *B*:

![Projection](images/physics/projection.png){srcset="images/physics/projection@2x.png 2x"}

$$l = vmath.project(A, B) \times vmath.length(B)$$

The compensation vector can be found by reducing the length of *B* by *l*. To calculate this for an arbitrary number of penetrations, you can accumulate the necessary correction in a vector by, for each contact point, and starting with a zero length correction vector:

1. Project the current correction against the contact's penetration vector.
2. Calculate what compensation is left from the penetration vector (as per the formula above).
3. Move the object by the compensation vector.
4. Add the compensation to the accumulated correction.

A complete implementation looks like this:

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```

## Ray casts

Ray casts are used to read the physics world along a linear ray. To cast a ray into the physics world, you provide a start and end position as well as a set of collision groups to test against.

If the ray hits a physics object you will get information about the object it hit. Rays intersect with dynamic, kinematic and static objects. They do not interact with triggers.

```lua
function update(self, dt)
  -- request ray cast
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
      -- act on the hit (see 'ray_cast_response' message for all values)
      print(result.id)
  end
end
```

::: sidenote
Ray casts will ignore collision objects that contain the starting point of the ray. This is a limitation in Box2D.
:::

## Joints

Defold supports joints for 2D physics. A joint connects two collision objects using some kind of constraint. The supported joint types are:

* Fixed (physics.JOINT_TYPE_FIXED) - A rope joint that restricts the maximum distance between two points. In Box2D referred to as a Rope joint.
* Hinge (physics.JOINT_TYPE_HINGE) - A hinge joint specifies an anchor point on two collision objects and moves them so that the two collision objects are always in the same place, and the relative rotation of the collision objects is not restricted. The hinge joint can enable a motor with a defined maximum engine torque and speed. In Box2D referred to as a Revolute joint.
* Spring (physics.JOINT_TYPE_SPRING) - A spring joint keeps two collision objects at a constant distance from each other. The spring joint can be made soft like a spring with a frequency and damping ratio. In Box2D referred to as a Distance joint.
* Slider (physics.JOINT_TYPE_SLIDER) - A slider joint allows for relative translation of two collision objects along a specified axis and prevents relative rotation. In Box2D referred to as a Prismatic joint.

### Creating joints

Joints can currently only be created programmatically using [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Editor support for creating joints is planned but no release date has been decided.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

The above will create a fixed joint with id `my_test_joint` connected between the two collision object `obj_a#collisionobject` and `obj_b#collisionobject`. The joint is connected 10 pixels to the left of the center of collision object `obj_a#collisionobject` and 20 pixels above the center of collision object `obj_b#collisionobject`. The maximum length of the joint is 20 pixels.

### Destroying joints

A joint can be destroyed using [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

### Reading from and Updating joints

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

### Get joint reaction force and torque

The reaction force and torque applied to a joint can be read using [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) and [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).


## Caveats and common issues

Collection proxies
: Through collection proxies it is possible to load more than one top level collection, or *game world* into the engine. When doing so it is important to know that each top level collection is a separate physical world. Physics interactions (collisions, triggers, ray-casts) only happen between objects belonging to the same world. So even if the collision objects from two worlds visually sits right on top of each other, there cannot be any physics interaction between them.

Collisions not detected
: If you have problems with collisions not being handled or detected properly then make sure to read up on [physics debugging in the Debugging manual](/manuals/debugging/#debugging-problems-with-physics).
