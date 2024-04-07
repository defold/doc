---
title: Defold 的碰撞事件
brief: 集中使用 `physics.set_listener()` 进行碰撞监听, 传导碰撞和交互信息到一个指定函数里.
---

# Defold 物理事件处理

以前, Defold 中的物理交互通过广播消息到所有碰撞对象组件来进行处理. 但是, 从版本 1.6.4 开始, Defold 提供了一个更集中的方法 `physics.set_listener()` 函数. 这个函数让你设置一个自定义监听器来处理所有物理交互, 从而简化代码并提高效率.

## 设置物理世界监听器

Defold 中, 各个集合代理创建各自的物理世界. 所以操作多个集合代理的时候, 保持各个物理世界的独立性很重要. 为确保物理事件在各个物理世界中正确处理, 必须对每个集合代理的世界分别设置监听器.

这钟机制意味着物理事件的侦听器必须在代理集合的上下文中设置. 这样就可以将侦听器直接与相关的物理世界关联起来, 使其能够准确地处理物理事件.

以下是在集合代理里设置物理世界监听器的例子:

```lua
	function init(self)
    -- 假设此脚本附加到了代理加载集合中的游戏对象里
    -- 为此集合代理的物理世界设置物理世界侦听器
    physics.set_listener(physics_world_listener)
end
```

通过实现此方法, 就可以确保集合代理生成的每个物理世界都有其专用的侦听器. 这对于使用多个集合代理的项目里能有效处理物理事件很重要.

::: important
如果设置了监听器, [物理消息](/manuals/physics-messages) 就不会再发送给有监听器的物理世界了.
:::

## 事件数据结构

每个物理事件提供 `data` 表, 包含了与事件相关的特定信息.

1. **碰撞点 (`contact_point_event`):**
这是物体发生碰撞发出的碰撞点事件. 该事件常用作碰撞详情的处理, 比如计算冲量或自定义碰撞响应.

   - `applied_impulse`: 碰撞产生的冲量.
   - `distance`: 碰撞对象间的穿透距离.
   - `a` 和 `b`: 碰撞涉及的物体, 它们包含:
     - `position`: 世界位置 (vector3).
     - `id`: 物体 ID (hash).
     - `group`: 碰撞组 (hash).
     - `relative_velocity`: 相对于另一物体的速度 (vector3).
     - `mass`: 千克质量 (number).
     - `normal`: 碰撞法线, 从另一物体发出 (vector3).

2. **碰撞事件 (`collision_event`):**
这是物体发生碰撞时发出的事件. 与碰撞点事件相比, 这是一个更普遍的事件, 非常适合检测碰撞, 而无需有关碰撞点的详细信息.

   - `a` 和 `b`: 碰撞事件中涉及的物体, 它们包含:
     - `position`: 世界位置 (vector3).
     - `id`: 物体 ID (hash).
     - `group`: 碰撞组 (hash).

3. **触发器事件 (`trigger_event`):** 
这是物体碰撞触发器时发出的事件. 它在游戏中创建对象进入或退出某区域时很有用.

   - `enter`: 碰撞交互进入 (true) 退出 (false).
   - `a` 和 `b`: 触发器事件中涉及的物体, 它们包含:
     - `id`: 物体 ID (hash).
     - `group`: 碰撞组 (hash).

4. **射线响应 (`ray_cast_response`):**
这是射线的响应事件, 提供了射线碰撞物体的相关信息.

   - `group`: 碰撞物体的碰撞组 (hash).
   - `request_id`: 射线 id (number).
   - `position`: 碰撞位置 (vector3).
   - `fraction`: 发生碰撞时光线长度的百分数 (number).
   - `normal`: 碰撞点的法线 (vector3).
   - `id`: 碰撞物体的 id (hash).

5. **射线失败 (`ray_cast_missed`):**
当射线没有碰撞到任何物体时发送该事件.

   - `request_id`: 碰撞失败的射线 id (number).

## 实例

```lua
local function physics_world_listener(self, event, data)
    if event == hash("contact_point_event") then
        -- 处理碰撞点数据
        pprint(data)
    elseif event == hash("collision_event") then
        -- 处理一般碰撞数据
        pprint(data)
    elseif event == hash("trigger_event") then
        -- 处理触发器碰撞数据
        pprint(data)
    elseif event == hash("ray_cast_response") then
        -- 处理射线碰撞数据
        pprint(data)
    elseif event == hash("ray_cast_missed") then
        -- 处理射线失败数据
        pprint(data)
    end
end

function init(self)
    physics.set_listener(physics_world_listener)
end
```

## 局限性

监听器在事件发生时同步调用. 发生在 timestep 之中, 这意味着物理世界是锁定的. 这就不能使用改变物理世界的函数, 比如  `physics.create_joint()`.

这里有个能绕过这个限制的例子:
```lua
local function physics_world_listener(self, event, data)
    if event == hash("contact_point_event") then
        local position_a = event.a.normal * SIZE
        local position_b =  event.b.normal * SIZE
        local url_a = msg.url(nil, event.a.id, "collisionobject")
        local url_b = msg.url(nil, event.b.id, "collisionobject")
        -- 填充将被发送到 `physics.create_joint()` 的消息
        local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
        -- 发送消息到本对象
        msg.post(".", "create_joint", message)
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- 从函数参数解包消息
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_listener(physics_world_listener)
end
```