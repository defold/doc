---
title: Defold 中的碰撞消息
brief: 当两个对象碰撞时，引擎将调用事件回调或广播消息。
---

# 碰撞消息

当两个对象碰撞时，引擎将向事件回调发送事件或向两个对象广播消息。

## 事件过滤

可以使用每个对象的标志来控制生成的事件类型：

* "生成碰撞事件"
* "生成接触事件"
* "生成触发器事件"

这些默认情况下都为 `true`。
当两个碰撞对象交互时，我们会根据这些复选框检查是否应该向用户发送消息。

例如，给定"生成接触事件"复选框：

当使用 `physics.set_event_listener()` 时：

| 组件 A | 组件 B | 发送消息 |
|---------|---------|----------|
| ✅︎      | ✅︎      | 是       |
| ❌      | ✅︎      | 是       |
| ✅︎      | ❌      | 是       |
| ❌      | ❌      | 否       |

当使用默认消息处理程序时：

| 组件 A | 组件 B | 发送消息        |
|---------|---------|-----------------|
| ✅︎      | ✅︎      | 是 (A,B) + (B,A) |
| ❌      | ✅︎      | 是 (B,A)        |
| ✅︎      | ❌      | 是 (A,B)        |
| ❌      | ❌      | 否              |

## 碰撞响应

当碰撞对象之一是"动态"、"运动学"或"静态"类型时，将发送 `"collision_response"` 消息。它设置了以下字段：

`other_id`
: 碰撞对象碰撞到的实例的ID（`hash`）

`other_position`
: 碰撞对象碰撞到的实例的世界位置（`vector3`）

`other_group`
: 另一个碰撞对象的碰撞组（`hash`）

`own_group`
: 碰撞对象的碰撞组（`hash`）

碰撞响应消息仅适用于您不需要对象实际相交细节的碰撞情况，例如，如果您想检测子弹是否击中敌人。对于任何碰撞对象对，每帧只发送一条这样的消息。

```Lua
function on_message(self, message_id, message, sender)
    -- 检查消息
    if message_id == hash("collision_response") then
        -- 采取行动
        print("I collided with", message.other_id)
    end
end
```

## 接触点响应

当碰撞对象之一是"动态"或"运动学"类型，而另一个是"动态"、"运动学"或"静态"类型时，将发送 `"contact_point_response"` 消息。它设置了以下字段：

`position`
: 接触点的世界位置（`vector3`）。

`normal`
: 接触点在世界空间中的法线，从另一个对象指向当前对象（`vector3`）。

`relative_velocity`
: 从另一个对象观察到的碰撞对象的相对速度（`vector3`）。

`distance`
: 对象之间的穿透距离——非负数（`number`）。

`applied_impulse`
: 接触产生的冲量（`number`）。

`life_time`
: （*目前未使用！*）接触的生命周期（`number`）。

`mass`
: 当前碰撞对象的质量，以千克为单位（`number`）。

`other_mass`
: 另一个碰撞对象的质量，以千克为单位（`number`）。

`other_id`
: 碰撞对象接触到的实例的ID（`hash`）。

`other_position`
: 另一个碰撞对象的世界位置（`vector3`）。

`other_group`
: 另一个碰撞对象的碰撞组（`hash`）。

`own_group`
: 碰撞对象的碰撞组（`hash`）。

对于需要完美分离对象的游戏或应用程序，`"contact_point_response"` 消息为您提供了您需要的所有信息。但是，请注意，对于任何给定的碰撞对，每帧可能会收到多个 `"contact_point_response"` 消息，这取决于碰撞的性质。有关更多信息，请参阅[解决碰撞](/manuals/physics-resolving-collisions)。

```Lua
function on_message(self, message_id, message, sender)
    -- 检查消息
    if message_id == hash("contact_point_response") then
        -- 采取行动
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## 触发器响应

当碰撞对象之一是"触发器"类型时，将发送 `"trigger_response"` 消息。当首次检测到碰撞时将发送一次消息，然后当对象不再碰撞时再发送一次。它具有以下字段：

`other_id`
: 碰撞对象碰撞到的实例的ID（`hash`）。

`enter`
: 如果交互是进入触发器则为 `true`，如果是退出则为 `false`。（`boolean`）。

`other_group`
: 另一个碰撞对象的碰撞组（`hash`）。

`own_group`
: 碰撞对象的碰撞组（`hash`）。

```Lua
function on_message(self, message_id, message, sender)
    -- 检查消息
    if message_id == hash("trigger_response") then
        if message.enter then
            -- 为进入采取行动
            print("I am now inside", message.other_id)
        else
            -- 为退出采取行动
            print("I am now outside", message.other_id)
        end
    end
end
```
