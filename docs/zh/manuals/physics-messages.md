---
title: Defold 中的碰撞消息
brief: 当两个碰撞对象接触, 引擎会向这两个对象上的所有组件广播碰撞消息.
---

# 碰撞消息

当两个碰撞对象接触, 引擎会向这两个对象上的所有组件广播碰撞消息:

## 碰撞响应

所有碰撞物体都会收到 `"collision_response"` 消息. 消息包含如下内容:

`other_id`
: 另一个碰撞物的id (`hash`过的)

`other_position`
: 另一个碰撞物的世界坐标 (`vector3`类型)

`other_group`
: 另一个碰撞物所在的碰撞组 (`hash`过的)

`own_group`
: 碰撞物体的碰撞组 (`hash`过的)

如果不需要很详细的信息, 碰撞响应消息就足够了, 比如检测子弹是否碰撞了敌人. 每帧每对碰撞物只有一个能收到此消息.

```Lua
function on_message(self, message_id, message, sender)
    -- 辨识消息
    if message_id == hash("collision_response") then
        -- 做出响应
        print("I collided with", message.other_id)
    end
end
```

## 碰撞点响应

如果碰撞一方是 dynamic 或 kinematic 对象, 那么它会收到 `"contact_point_response"` 消息. 消息包含如下内容:

`position`
: 接触点世界坐标 (`vector3`类型).

`normal`
: 接触点世界坐标系法向量, 方向是从另一物体指向当前物体 (`vector3`类型).

`relative_velocity`
: 两个接触物体之间的相对速度, 方向是从另一物体指向当前物体 (`vector3`类型).

`distance`
: 两个接触物体之间穿透距离 -- 非负数 (`number`类型).

`applied_impulse`
: 两个接触物体间的冲量大小 (`number`类型).

`life_time`
: (*目前未使用*) 接触时长 (`number`类型).

`mass`
: 当前物体质量, 单位千克 (`number`类型).

`other_mass`
: 另一个物体质量, 单位千克 (`number`类型).

`other_id`
: 另一个物体的id (`hash`过的).

`other_position`
: 另一个物体的世界坐标 (`vector3`类型).

`group`
: 另一个物体所处的碰撞组 (`hash`过的).

`own_group`
: 碰撞物体的碰撞组 (`hash`过的).

要让相碰撞的物体好好分离, 用 `"contact_point_response"` 消息里的数据就够了. 注意每帧每对碰撞物可能不止收到一个 `"contact_point_response"` 消息, 这取决于接触的情况, 详见 [碰撞处理教程](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## 触发器响应

作为 "trigger" 类型的碰撞对象会收到 `"trigger_response"` 消息.
触发器与碰撞对象接触时会收到 `"collision_response"` 消息. 而且, 接触开始和结束时都会收到 `"trigger_response"` 消息. 消息包含如下信息:

`other_id`
: 另一个物体的id (`hash`过的).

`enter`
: 如果另一个物体进入触发器为 `true`, 离开为 `false`. (`boolean`类型).

`other_group`
: 另一个物体所处的碰撞组 (`hash`过的).

`own_group`
: 碰撞物体的碰撞组 (`hash`过的).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
