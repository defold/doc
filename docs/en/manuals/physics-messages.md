---
title: Collision messages in Defold
brief: When two objects collide, the engine will broadcast messages to all components in both objects.
---

# Collision messages

When two objects collide, the engine will broadcast messages to all components in both objects:

## Collision response

The `"collision_response"` message is sent for all collision objects. It has the following fields set:

`other_id`
: the id of the instance the collision object collided with (`hash`)

`other_position`
: the world position of the instance the collision object collided with (`vector3`)

`other_group`
: the collision group of the other collision object (`hash`)

`own_group`
: the collision group of the collision object (`hash`)

The collision_response message is only adequate to resolve collisions where you don't need any details on the actual intersection of the objects, for example if you want to detect if a bullet hits an enemy. There is only one of these messages sent for any colliding pair of objects each frame.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Contact point response

The `"contact_point_response"` message is sent when one of the colliding objects is dynamic or kinematic. It has the following fields set:

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

`other_group`
: the collision group of the other collision object (`hash`).

`own_group`
: the collision group of the collision object (`hash`).

For a game or application where you need to separate objects perfectly, the `"contact_point_response"` message gives you all information you need. However, note that for any given collision pair, several `"contact_point_response"` messages can be received each frame, depending on the nature of the collision. See [Resolving collisions for more information](/manuals/physics-resolving-collisions).

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

## Trigger response

The `"trigger_response"`  message is sent when a colliding object is of type "trigger".


In a trigger collision `"collision_response"` messages are sent. In addition, triggers also send a special `"trigger_response"` message when the collision begins and ends. The message has the following fields:

`other_id`
: the id of the instance the collision object collided with (`hash`).

`enter`
: `true` if the interaction was an entry into the trigger, `false` if it was an exit. (`boolean`).

`other_group`
: the collision group of the other collision object (`hash`).

`own_group`
: the collision group of the collision object (`hash`).

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
