---
title: Optimizing runtime performance of a Defold game
brief: This manual describes how to optimize a Defold game to run at a stable high frame rate.
---

# Optimizing runtime speed
Before trying to optimize a game with the goal to make it run at a stable high frame rate you need to know where your bottlenecks are. What is actually taking up most of the time in a frame of your game? Is it the rendering? Is it your game logic? Is it the scene graph? To figure this out it is recommended to use the built-in profiling tools. Use the [on-screen or web profiler](/manuals/profiling/) to sample the performance of your game and then make a decision if and what to optimize. Once you have a better understanding of what takes time you can start addressing the problems.

## Reduce script execution time
Reducing script execution time is needed if the profiler shows high values for the `Script` scope. As a general rule of thumb you should of course try to run as little code as possible every frame. Running a lot of code in `update()` and `on_input()` every frame is likely to have an impact on your game's performance, especially on low end devices. Some guidelines are:

### Use reactive code patterns
Don't poll for changes if you can get a callback. Don't manually animate something or perform a task that can be handed over to the engine (e.g. `go.animate)()` vs manually animating something).

### Reduce garbage collection
If you create loads of short lived objects such as Lua tables every frame this will eventually trigger the garbage collector of Lua. When this happens it can manifest itself as small hitches/spikes in frame time. Re-use tables where you can and really try to avoid creating Lua tables inside loops and similar constructs if possible.

### Pre-hash message and action ids
If you do a lot of message handling or have many input events to deal with it is recommended to prehash the strings. Consider this piece of code:

```
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

In the above scenario the hashed string would be recreated every time a message is received. This can be improved by creating the hashed strings once and use the hashed versions when handling messages:

```
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Prefer and cache URLs
Message passing or in other ways addressing a game object or component can be done both by providing an id as a string or hash or as a URL. If a string or hash is used it will internally be translated into a URL. It is therefore recommended to cache URLs that are used often, to get the best possible performance out of the system. Consider the following:

```
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- do something with pos
```

In all three cases the position of a game object with id `enemy` would be retrieved. In the first and second case the id (string or hash) would be converted into a URL before being used. This tells us that it's better to cache URLs and use the cached version for the best possible performance:

```
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- do something with pos
    end
```

## Reduce time it takes to render a frame
Reducing the time it takes to render a frame is needed if the profiler shows high values in the `Render` and `Render Script` scopes. There are several things to consider when trying to increase reduce the time it takes to render a frame:

* Reduce draw calls - Read more about reducing draw calls in [this forum post](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Reduce overdraw
* Reduce shader complexity - Read up on GLSL optimizations in [this Khronos article](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). You can also modify the default shaders used by Defold (found in `builtins/materials`) and reduce shader precision to gain some speed on low end devices. All shaders are using `highp` precision and a change to for instance `mediump` can in some cases improve performance slightly.

## Reduce scene graph complexity
Reducing the scene graph complexity is needed if the profiler shows high values in the `GameObject` scope and more specifically for the `UpdateTransform` sample. Some actions to take:

* Culling - Disable game objects (and their components) if they aren't currently visible. How this is determined depends very much on the type of game. For a 2D game it can be as easy as always disabling game objects that are outside of a rectangular area. You can use a physics trigger to detect this or by partitioning your objects into buckets. Once you know which objects to disable or enable you do this by sending a `disable` or `enable` message to each game object.

## Frustum culling
The render script can automatically ignore rendering of game object component that are outside of a defined bounding box (frustum). Learn more about Frustum Culling in the [Render Pipeline manual](/manuals/render/#frustum-culling).