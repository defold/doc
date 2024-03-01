---
title: Collision events in Defold
brief: Collision event handling can be centralized by using `physics.set_listener()` to direct all collision and interaction messages to a single specified function.
---

# Defold Physics Event Handling

Previously, physics interactions in Defold were handled by broadcasting messages to all components of colliding objects. However, starting with version 1.6.4, Defold offers a more centralized approach through the `physics.set_listener()` function. This function allows you to set a custom listener to handle all physics interaction events in one place, thereby streamlining your code and improving efficiency.

## Setting the Physics World Listener

To start using this new functionality, you need to use the `physics.set_listener` function. This function takes a callback as its argument, which will be called with information about all physics interactions in the world. The general syntax is as follows:

```lua
physics.set_listener(function(self, event, data)
    -- Event handling logic goes here
end)

```

::: important
If a listener is set, [physics messages](/manuals/physics-messages) will no longer be sent.
:::

## Event Data Structure

Each physics event provides a `data` table containing specific information relevant to the event.

1. **Contact Point Event (`contact_point_event`):**
This event reports a contact point between two collision objects. It is useful for detailed collision handling, such as calculating impact forces or custom collision responses.

   - `applied_impulse`: The impulse resulting from the contact.
   - `distance`: The penetration distance between the objects.
   - `a` and `b`: Objects representing the colliding entities, each containing:
     - `position`: World position (vector3).
     - `id`: Instance ID (hash).
     - `group`: Collision group (hash).
     - `relative_velocity`: Velocity relative to the other object (vector3).
     - `mass`: Mass in kilograms (number).
     - `normal`: Contact normal, pointing from the other object (vector3).

2. **Collision Event (`collision_event`):**
This event indicates that a collision has occurred between two objects. It is a more generalized event compared to the contact point event, ideal for detecting collisions without needing detailed information about the contact points.

   - `a` and `b`: Objects representing the colliding entities, each containing:
     - `position`: World position (vector3).
     - `id`: Instance ID (hash).
     - `group`: Collision group (hash).

3. **Trigger Event (`trigger_event`):** 
This event is sent when an object interacts with a trigger object. It's useful for creating areas in your game that cause something to happen when an object enters or exits.

   - `enter`: Indicates if the interaction was an entry (true) or an exit (false).
   - `a` and `b`: Objects involved in the trigger event, each containing:
     - `id`: Instance ID (hash).
     - `group`: Collision group (hash).

4. **Ray Cast Response (`ray_cast_response`):**
This event is sent in response to a raycast, providing information about the object hit by the ray.

   - `group`: Collision group of the hit object (hash).
   - `request_id`: Identifier of the raycast request (number).
   - `position`: Hit position (vector3).
   - `fraction`: The fraction of the ray's length at which the hit occurred (number).
   - `normal`: Normal at the hit position (vector3).
   - `id`: Instance ID of the hit object (hash).

5. **Ray Cast Missed (`ray_cast_missed`):**
This event is sent when a raycast does not hit any object.

   - `request_id`: Identifier of the raycast request that missed (number).

## Example Usage

```lua
local function physics_world_listener(self, event, data)
    if event == hash("contact_point_event") then
        -- Handle detailed contact point data
        pprint(data)
    elseif event == hash("collision_event") then
        -- Handle general collision data
        pprint(data)
    elseif event == hash("trigger_event") then
        -- Handle trigger interaction data
        pprint(data)
    elseif event == hash("ray_cast_response") then
        -- Handle raycast hit data
        pprint(data)
    elseif event == hash("ray_cast_missed") then
        -- Handle raycast miss data
        pprint(data)
    end
end

function init(self)
    physics.set_listener(physics_world_listener)
end
```

## Limitations

The listener calls synchronously at the moment it occurs. It happens in the middle of a timestep, which means that the physics world is locked. This makes it impossible to use functions that may affect physics world simulations, e.g., `physics.create_joint()`.

Here is a small example of how to avoid these limitations:
```lua
local function physics_world_listener(self, event, data)
    if event == hash("contact_point_event") then
        local position_a = event.a.normal * SIZE
        local position_b =  event.b.normal * SIZE
        local url_a = msg.url(nil, event.a.id, "collisionobject")
        local url_b = msg.url(nil, event.b.id, "collisionobject")
        -- fill the message in the same way arguments should be passed to `physics.create_joint()`
        local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
        -- send message to the object itself
        msg.post(".", "create_joint", message)
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_listener(physics_world_listener)
end
```
