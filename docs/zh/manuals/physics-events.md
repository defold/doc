---
title: Defold 中的碰撞事件
brief: 可以通过使用 `physics.set_event_listener()` 将碰撞事件处理集中化，将所有碰撞和交互消息定向到单个指定函数。
---

# Defold 物理事件处理

以前，Defold 中的物理交互是通过向碰撞对象的所有组件广播消息来处理的。然而，从版本 1.6.4 开始，Defold 通过 `physics.set_event_listener()` 函数提供了一种更集中的方法。此函数允许您设置一个自定义监听器来在一个地方处理所有物理交互事件，从而简化代码并提高效率。

## 设置物理世界监听器

在 Defold 中，每个集合代理都会创建自己独立的物理世界。因此，当您使用多个集合代理时，管理与每个代理相关的不同物理世界至关重要。为了确保物理事件在每个世界中都能正确处理，您必须为每个集合代理的世界专门设置一个物理世界监听器。

这种设置意味着物理事件的监听器必须在代理所代表的集合的上下文中设置。通过这样做，您将监听器直接与相关的物理世界关联起来，使其能够准确地处理物理事件。

以下是在集合代理中设置物理世界监听器的示例：

```lua
function init(self)
    -- 假设此脚本附加到代理加载的集合中的游戏对象上
    -- 为此集合代理的物理世界设置物理世界监听器
    physics.set_event_listener(physics_world_listener)
end
```

通过实现此方法，您可以确保每个集合代理生成的物理世界都有其专用的监听器。对于使用多个集合代理的项目来说，这对于有效处理物理事件至关重要。

::: important
如果设置了监听器，[物理消息](/manuals/physics-messages)将不再发送给设置了此监听器的物理世界。
:::

## 事件数据结构

每个物理事件都提供一个包含与事件相关的特定信息的 `data` 表。

1. **接触点事件 (`contact_point_event`)：**
此事件报告两个碰撞对象之间的接触点。它对于详细的碰撞处理很有用，例如计算冲击力或自定义碰撞响应。

   - `applied_impulse`：接触产生的冲量。
   - `distance`：对象之间的穿透距离。
   - `a` 和 `b`：表示碰撞实体的对象，每个包含：
     - `position`：接触点的世界位置（vector3）。
     - `instance_position`：游戏对象实例的世界位置（vector3）。
     - `id`：实例 ID（hash）。
     - `group`：碰撞组（hash）。
     - `relative_velocity`：相对于另一个对象的速度（vector3）。
     - `mass`：质量，以千克为单位（number）。
     - `normal`：接触法线，指向另一个对象（vector3）。

2. **碰撞事件 (`collision_event`)：**
此事件表示两个对象之间发生了碰撞。与接触点事件相比，这是一个更通用的事件，非常适合检测碰撞，而无需有关接触点的详细信息。

   - `a` 和 `b`：表示碰撞实体的对象，每个包含：
     - `position`：世界位置（vector3）。
     - `id`：实例 ID（hash）。
     - `group`：碰撞组（hash）。

3. **触发器事件 (`trigger_event`)：** 
当对象与触发器对象交互时发送此事件。它对于在游戏中创建区域，当对象进入或退出时触发某些操作非常有用。

   - `enter`：指示交互是进入（true）还是退出（false）。
   - `a` 和 `b`：触发器事件中涉及的对象，每个包含：
     - `id`：实例 ID（hash）。
     - `group`：碰撞组（hash）。

4. **射线投射响应 (`ray_cast_response`)：**
此事件作为对射线投射的响应发送，提供有关射线击中的对象的信息。

   - `group`：被击中对象的碰撞组（hash）。
   - `request_id`：射线投射请求的标识符（number）。
   - `position`：击中位置（vector3）。
   - `fraction`：发生击中时射线长度的分数（number）。
   - `normal`：击中位置的法线（vector3）。
   - `id`：被击中对象的实例 ID（hash）。

5. **射线投射未命中 (`ray_cast_missed`)：**
当射线投射未击中任何对象时发送此事件。

   - `request_id`：未命中的射线投射请求的标识符（number）。

## 使用示例

```lua
local function physics_world_listener(self, events)
    for _,event in ipair(events) do
        if event.type == hash("contact_point_event") then
            -- 处理详细的接触点数据
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- 处理一般碰撞数据
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- 处理触发器交互数据
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- 处理射线投射命中数据
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- 处理射线投射未命中数据
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## 局限性

监听器在事件发生时同步调用。它发生在一个时间步长的中间，这意味着物理世界被锁定。这使得无法使用可能影响物理世界模拟的函数，例如 `physics.create_joint()`。

以下是一个如何避免这些限制的小示例：
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- 填充消息，方式与传递给 `physics.create_joint()` 的参数相同
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- 向对象本身发送消息
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- 解包带有函数参数的消息
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```