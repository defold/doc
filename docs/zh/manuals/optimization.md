---
title: Defold 游戏优化
brief: 本教程介绍了如何优化 Defold 应用的包体和性能.
---

# Defold 游戏优化
开发时就要考虑游戏在目标平台上的运行和优化. 需要考虑以下几个方面:

* 应用大小
* 运行速度
* 内存占用
* 耗电情况

## 应用大小优化
Defold 编译和打包时建立了一个依赖树. 编译系统从 *game.project* 文件指定的启动集合开始检查每个被引用的集合, 游戏对象及组件需要的资源. 这些被依赖的资源才会最终被导入包内. 没被引用的被排除在包外. 即使这样开发者还应该考虑包内资源空间占用情况. 有些平台与发布渠道限制了应用包体大小:

* Apple 和 Google 规定了设备使用移动网络 (而不是 Wifi) 下载应用的大小限制.
  * 2019 年夏 Google Play 限制 100 MB, Apple App Store 限制 150 MB.
* Facebook 建议 Facebook Instant Game 要在 5 秒内最好是 3 秒内启动.
  * 这虽然没有直接规定大小, 我们讨论认为大小应该限制在 20 MB 以内.
* Playable ads 基于广告商网络一般限制在 2 到 5 MB.

为了更好的分析包体空间占用可以在编译时 [生成编译报告](/manuals/bundling/#build-reports). 通常声音和图片占游戏空间最大部分.

### 声音优化
Defold 支持 .ogg 和 .wav 文件其中 .ogg 一般用于音乐 .wav 一般用于音效. Sounds 必须是 16-bit 采样率 44100 所以编码前就要对其做好优化. 可以使用第三方软件降低音质或者把 .wav 转换成 .ogg.

### 图片优化
对游戏的图片优化有几种办法, 首先要做的就是检查图集和瓷砖图源内容图片的大小. 导入的图片尺寸不要超过游戏所需大小. 导入大图片再缩小使用是现存资源的浪费. 可以使用第三方图片编辑器先把图片修改成所需大小. 对于背景图之类的有时可以导入小图片再放大使用. 小图改好了还要考虑图集和瓷砖图源本身的大小. 不同平台和显示硬件的纹理尺寸限制可能不一样.

::: 注意
[这个帖子](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl) 在使用脚本与第三方软件修改图片大小的方面给出了许多建议.
:::

* HTML5 游戏最大纹理: https://webglstats.com/webgl/parameter/MAX_TEXTURE_SIZE
* iOS 游戏最大纹理:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Android 各不相同但是新设备基本都支持 4096x4096.

如果图集太大就需要切分成小图集或者使用 texture profile 缩小整个图集. Defold 的 texture profile 系统不但可以缩小图集还可以通过应用压缩算法减小图集占用空间. 详见 [纹理档教程](/manuals/texture-profiles/).

::: 注意
优化和管理纹理可以参考 [这个帖子](https://forum.defold.com/t/texture-management-in-defold/8921).
:::

### 排除内容按需下载
Another way of reducing initial application size is to exclude parts of the game content from the application bundle and make this content downloadable on demand. Excluded content can be anything from entire levels to unlockable characters, skins, weapons or vehicles. Defold provides a system called Live Update for excluding content for download on demand. Learn more in the [Live Update manual](/manuals/live-update/).


## Optimize for application speed
Before trying to optimize a game with the goal to increase the speed at which the game runs you need to know where your bottlenecks are. What is actually taking up most of the time in a frame of your game? Is it the rendering? Is it your game logic? Is it the scene graph? To figure this out it is recommended to use the built in profiling tools. Use the [on-screen or web profiler](/manuals/profiling/) to sample the performance of your game and then make a decision if and what to optimize. Once you have a better understanding of what takes time you can start addressing the problems.

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
