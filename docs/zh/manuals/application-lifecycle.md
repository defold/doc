---
title: Defold 应用生命周期手册
brief: 本手册详述了 Defold 游戏和应用程序的生命周期。
---

# 应用生命周期

Defold 应用程序或游戏的生命周期总体上很简单。引擎会经历三个执行阶段：初始化、更新循环（应用程序和游戏大部分时间都在这里度过）和最终化。

![Lifecycle overview](images/application_lifecycle/application_lifecycle_overview.png)

在许多情况下，只需要对 Defold 的内部工作原理有一个基本的了解就足够了。然而，你可能会遇到一些边缘情况，此时 Defold 执行任务的精确顺序变得至关重要。本文档描述了引擎如何从头到尾运行应用程序。

应用程序首先初始化运行引擎所需的一切。它加载主集合并调用所有具有 `init()` Lua 函数的已加载组件（脚本组件和带有 GUI 脚本的 GUI 组件）的 [`init()`](/ref/go#init) 函数。这允许你进行自定义初始化。

然后应用程序进入更新循环，应用程序将在此度过其生命周期的大部分时间。每一帧，游戏对象及其包含的组件都会被更新。任何脚本和 GUI 脚本的 [`update()`](/ref/go#update) 函数都会被调用。在更新循环期间，消息被分发给它们的接收者，声音被播放，所有图形都被渲染。

在某个时刻，应用程序的生命周期将结束。在应用程序退出之前，引擎会退出更新循环并进入最终化阶段。它准备删除所有已加载的游戏对象。所有对象组件的 [`final()`](/ref/go#final) 函数都会被调用，这允许进行自定义清理。然后对象被删除，主集合被卸载。

## 初始化

下图包含了初始化步骤的更详细分解。"dispatch messages"传递中涉及的步骤（在"spawn dynamic objects"之前）为了清晰起见已单独放在右侧的块中。

![Lifecycle overview](images/application_lifecycle/application_lifecycle_init.png)

实际上，在主集合加载之前，引擎在初始化过程中会采取更多步骤。内存分析器、套接字、图形、HID（输入设备）、声音、物理等等都被设置。应用程序配置（*game.project*）也被加载和设置。

在引擎初始化结束时，第一个用户可控制的入口点是对当前渲染脚本的 `init()` 函数的调用。

然后加载并初始化主集合。集合中的所有游戏对象将其变换（平移（位置变化）、旋转和缩放）应用到它们的子对象。然后调用所有存在的组件 `init()` 函数。

::: sidenote
游戏对象组件 `init()` 函数的调用顺序是未指定的。你不应该假设引擎以特定顺序初始化属于同一集合的对象。
:::

由于你的 `init()` 代码可以发布新消息，告诉工厂生成新对象，标记对象以供删除以及执行各种操作，引擎接下来会执行完整的"post-update"传递。此传递执行消息传递、实际的工厂游戏对象生成和对象删除。请注意，post-update 传递包含一个"dispatch messages"序列，它不仅发送任何排队的消息，还处理发送到集合代理的消息。代理的任何后续更新（启用和禁用、加载和标记为卸载）都在这些步骤中执行。

研究上图可以发现，在 `init()` 期间加载[集合代理](/manuals/collection-proxy)，确保其包含的所有对象都被初始化，然后通过代理卸载集合是完全可能的——所有这些都在第一个组件 `update()` 被调用之前，即在引擎离开初始化阶段并进入更新循环之前：

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- 在到达此代码之前，代理集合已被卸载。
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- 代理集合对象的 init() 和 final() 函数
        -- 在我们到达此对象的 update() 之前被调用
    end
end
```

## 更新循环

更新循环每帧运行一次长序列。下图中的更新序列为了清晰起见分为逻辑序列块。"Dispatch messages"出于同样的原因也被单独分解出来：

![Update loop](images/application_lifecycle/application_lifecycle_update.png)

## 输入

从可用设备读取输入，根据[输入绑定](/manuals/input)进行映射，然后分发。任何获得输入焦点的游戏对象都会将输入发送到其所有组件的 `on_input()` 函数。具有脚本组件和带有 GUI 脚本的 GUI 组件的游戏对象将获得输入到两个组件的 `on_input()` 函数——前提是它们已被定义并且已获得输入焦点。

任何获得输入焦点并包含集合代理组件的游戏对象会将输入分发到代理集合内的组件。这个过程在启用的集合代理内的启用的集合代理中递归进行下去。

## 更新

遍历主集合中的每个游戏对象组件。如果这些组件中的任何一个具有脚本 `update()` 函数，那么该函数将被调用。如果组件是集合代理，则代理集合中的每个组件都会递归地更新，执行上图"update"序列中的所有步骤。

::: sidenote
如果[物理模拟使用固定时间步](/manuals/physics/#physics-updates)，则所有脚本组件中也可能会有对 `fixed_update()` 函数的调用。在基于物理的游戏中，当你希望以固定间隔操作物理对象以实现稳定的物理模拟时，此函数很有用。
:::

::: sidenote
游戏对象组件 `update()` 函数的调用顺序是未指定的。你不应该假设引擎以特定顺序更新属于同一集合的对象。
:::

在下一步中，所有已发布的消息都被分发。由于任何接收者组件的 `on_message()` 代码可以发布额外的消息，消息分发器将继续分发已发布的消息，直到消息队列为空。然而，消息分发器通过消息队列运行的次数是有限制的。有关详细信息，请参阅[消息链](/manuals/message-passing#message-chains)。

对于碰撞对象组件，物理消息（碰撞、触发器、ray_cast 响应等）被分发到包含具有 `on_message()` 函数的脚本的所有组件的整个游戏对象。

然后进行变换，应用任何游戏对象移动、旋转和缩放到每个游戏对象组件以及任何子游戏对象组件。

## 渲染更新

渲染更新块向 `@render` 套接字分发消息（摄像机组件 `set_view_projection` 消息、`set_clear_color` 消息等）。然后调用渲染脚本 `update()`。

## 后更新

更新之后，运行后更新序列。它从内存中卸载标记为卸载的集合代理（这发生在"dispatch messages"序列期间）。任何标记为删除的游戏对象将调用其所有组件的 `final()` 函数（如果有的话）。`final()` 函数中的代码通常会向队列发布新消息，因此之后会运行"dispatch messages"传递。

任何被告知生成游戏对象的工厂组件将在此执行此操作。最后，标记为删除的游戏对象实际上被删除。

更新循环中的最后一步涉及分发 `@system` 消息（`exit`、`reboot` 消息，切换分析器，启动和停止视频捕获等）。然后渲染图形。在图形渲染期间，进行视频捕获，以及视觉分析器的任何渲染（参见[调试文档](/manuals/debugging)）。

## 帧率和集合时间步

每秒帧更新数（等于每秒更新循环运行次数）可以在项目设置中设置，或者通过向 `@system` 套接字发送 `set_update_frequency` 消息以编程方式设置。此外，可以通过向代理发送 `set_time_step` 消息来为集合代理单独设置_时间步_。更改集合的时间步不会影响帧率。它确实会影响物理更新时间步以及传递给 `update()` 的 `dt` 变量。还要注意，更改时间步不会改变每帧调用 `update()` 的次数——它总是恰好一次。

（有关详细信息，请参阅[集合代理手册](/manuals/collection-proxy)和[`set_time_step`](/ref/collectionproxy#set-time-step)）

## 最终化

当应用程序退出时，首先它完成最后的更新循环序列，这将卸载任何集合代理：最终化并删除每个代理集合中的所有游戏对象。

当完成后，引擎进入处理主集合及其对象的最终化序列：

![Finalization](images/application_lifecycle/application_lifecycle_final.png)

首先调用组件 `final()` 函数。随后进行消息分发。最后，所有游戏对象都被删除，主集合被卸载。

引擎随后在幕后进行子系统的关闭：项目配置被删除，内存分析器被关闭等等。

现在应用程序已完全关闭。

