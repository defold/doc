---
title: Optimizing a Defold game
brief: This manual describes how to optimize a Defold app for size and performance.
---

# Optimizing a Defold game
It is important to understand the technical constraints of the platform(s) where your game is supposed to run and to optimize your game for the platform(s) while developing your game. There are several aspects to consider:

* Application size
* Speed
* Memory usage
* Battery usage

## Optimize application size
Defold will create a dependency tree when building and bundling your application. The build system will start from the bootstrap collection specified in the *game.project* file and inspect every referenced collection, game object and component to build a list of the assets that are in use. It is only these assets that will get included in the final application bundle. Anything not directly referenced will get excluded. While it is good to know that unused assets will not be included you as a developer still needs to consider what goes into the final application and the size of the individual assets and the total size of the application bundle. Some target platforms and distribution channels have limitations on application size:

* Apple and Google has defined application size limits when downloading over mobile networks (as opposed to downloading over Wifi).
  * In the summer of 2019 these limits were 100 MB for Google Play and 150 MB for the Apple App Store.
* Facebook has a recommendation that a Facebook Instant Game should start in less than 5 seconds and preferably less than 3 seconds.
  * What this means for actual application size is not clearly defined but we are talking size in the range of up to 20 MB.
* Playable ads are usually limited to between 2 and 5 MB depending on the ad network.

:::sidenote
According to a 2017 study it was shown that "For every 6 MB increase to an APK’s size, we see a decrease in the install conversion rate of 1%." ([source](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

To get a better understanding of what makes up the size of your application you can [generate a build report](/manuals/bundling/#build-reports) when bundling. It is quite common that sounds and graphics is what takes up the bulk of the size of any game.

### Optimize sounds
Defold supports .ogg and .wav files where .ogg is typically used for music and .wav for sound effects. Sounds must be 16-bit with a sampling rate of 44100 so any optimizations must be done on the sounds before encoding them. You can edit the sounds in an external sound editor software to reduce the quality or convert from .wav to .ogg.

### Optimize graphics
You have several options when it comes to optimizing the graphics used by your game but the first thing to do is to check the size of the graphics that gets added to an atlas or used as a tilesource. You should never use a larger size on the graphics than is actually needed in your game. Importing large images and scaling them down to the appropriate size is a waste of texture memory and should be avoided. Start by adjusting the size of the images using external image editing software to the actual size needed in your game. For things such as background images it might also be ok to use a small image and scale it up to the desired size. Once you have the images down to the correct size and added to atlases or used in tilesources you also need to consider the size of the atlases themselves. The maximum atlas size that can be used varies between platforms and graphics hardware.

::: sidenote
[This forum posts](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) suggests several tips on how to resize multiple images using scripts or third party software.
:::

* Max texture size on HTML5: https://webglstats.com/webgl/parameter/MAX_TEXTURE_SIZE
* Max texture size on iOS:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Max texture size on Android varies greatly but in general all reasonably new devices support 4096x4096.

If an atlas is too large you need to either split it into several smaller atlases or scale the entire atlas using a texture profile. The texture profile system in Defold allows you to not only scale entire atlases but also to apply compression algorithms to reduce the size of the atlas on disk. You can [read more about texture profiles in the manual](/manuals/texture-profiles/).

::: sidenote
You can read more about how to optimize and manage textures in [this forum post](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### Exclude content for download on demand
Another way of reducing initial application size is to exclude parts of the game content from the application bundle and make this content downloadable on demand. Excluded content can be anything from entire levels to unlockable characters, skins, weapons or vehicles. Defold provides a system called Live Update for excluding content for download on demand. Learn more in the [Live Update manual](/manuals/live-update/).


## Optimize for application speed
Before trying to optimize a game with the goal to increase the speed at which the game runs you need to know where your bottlenecks are. What is actually taking up most of the time in a frame of your game? Is it the rendering? Is it your game logic? Is it the scene graph? To figure this out it is recommended to use the built-in profiling tools. Use the [on-screen or web profiler](/manuals/profiling/) to sample the performance of your game and then make a decision if and what to optimize. Once you have a better understanding of what takes time you can start addressing the problems.

### Reduce script execution time
Reducing script execution time is needed if the profiler shows high values for the `Script` scope. As a general rule of thumb you should of course try to run as little code as possible every frame. Running a lot of code in `update()` and `on_input()` every frame is likely to have an impact on your game's performance, especially on low end devices. Some guidelines are:

#### Use reactive code patterns
Don't poll for changes if you can get a callback. Don't manually animate something or perform a task that can be handed over to the engine (eg go.animate vs manually animating something).

#### Reduce garbage collection
If you create loads of short lived objects such as Lua tables every frame this will eventually trigger the garbage collector of Lua. When this happens it can manifest itself as small hitches/spikes in frame time. Re-use tables where you can and really try to avoid creating Lua tables inside loops and similar constructs if possible.

#### Pre-hash message and action ids
If you do a lot of message handling or have many input events to deal with it is recommended to pre-hash the strings. Consider this piece of code:

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

#### Prefer and cache URLs
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
        local pos = go.get_position(enemy_url)
        -- do something with pos
    end
```

### Reduce time it takes to render a frame
Reducing the time it takes to render a frame is needed if the profiler shows high values in the `Render` and `Render Script` scopes. There are several things to consider when trying to increase reduce the time it takes to render a frame:

* Reduce draw calls - Read more about reducing draw calls in [this forum post](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Reduce overdraw
* Reduce shader complexity - Read up on GLSL optimizations in [this Kronos article](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). You can also modify the default shaders used by Defold (found in `builtins/materials`) and reduce shader precision to gain some speed on low end devices. All shaders are using `highp` precision and a change to for instance `mediump` can in some cases improve performance slightly.

### Reduce scene graph complexity
Reducing the scene graph complexity is needed if the profiler shows high values in the `GameObject` scope and more specifically for the `UpdateTransform` sample. Some actions to take:

* Culling - Disable game objects (and their components) if they aren't currently visible. How this is determined depends very much on the type of game. For a 2D game it can be as easy as always disabling game objects that are outside of a rectangular area. You can use a physics trigger to detect this or by partitioning your objects into buckets. Once you know which objects to disable or enable you do this by sending a `disable` or `enable` message to each game object.


## Optimize memory usage
This section is not yet finished. Topics that will be covered:

* [Texture compression](/manuals/texture-profiles/)
* [Dynamic loading of collections](https://www.defold.com/manuals/collection-proxy/)
* [Dynamic loading of factories](https://www.defold.com/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Profiling](/manuals/profiling/)


## Optimize battery usage
This section is not yet finished. Topics that will be covered:

* Running code every frame
* Accelerometer on mobile
* [Profiling](/manuals/profiling/)
