---
title: Defold 应用程序生命周期手册
brief: 本手册详述了 Defold 游戏和应用程序的生命周期。
---

# 应用生命周期

Defold 应用程序或游戏的生命周期，从整体上看很简单。引擎会经历三个执行阶段：初始化、更新循环（应用和游戏大部分时间都处于这个阶段）以及最终化。

::: sidenote
本手册适用于 Defold 1.12.0 起的版本。1.12.0 引入了生命周期相关变更以及新的 `late_update()` 函数。
:::

![Lifecycle overview](images/application_lifecycle/application_lifecycle.png)

在许多情况下，只需要对 Defold 的内部工作方式有一个基础了解即可。不过，您可能会遇到一些边缘情况，此时 Defold 执行任务的精确顺序会变得非常重要。本文档描述引擎如何从开始到结束运行一个应用程序。

应用程序首先初始化运行引擎所需的一切。它加载主集合，并对所有已加载且具有 `init()` Lua 函数的组件（脚本组件以及带 GUI 脚本的 GUI 组件）调用 [`init()`](/ref/go#init)。这让您可以执行自定义初始化。

然后应用程序进入更新循环，应用程序的大部分生命周期都会在这里度过。每一帧，游戏对象及其包含的组件都会被更新。任何脚本和 GUI 脚本的 [`update()`](/ref/go#update) 函数都会被调用。在更新循环期间，消息会被分发给接收者，声音会播放，所有图形都会被渲染。

在某个时刻，应用程序生命周期会结束。在应用退出前，引擎会离开更新循环并进入最终化阶段。它会准备删除所有已加载的游戏对象。所有对象组件的 [`final()`](/ref/go#final) 函数都会被调用，以允许自定义清理。随后对象被删除，主集合被卸载。

为清晰起见，["分发消息"](#dispatching-messages)阶段中涉及的步骤会在本手册末尾以单独图表展示，并在图中用一个小的“带箭头信封”图标 📩 标记。

## 初始化

这是游戏开始运行的地方，也是运行中游戏的第一步。它可以分为 3 个阶段：

![Initizalization](images/application_lifecycle/initialization.png)

### 预初始化

在 `Preinitialization` 阶段，引擎会在加载主（bootstrap）集合之前执行许多步骤。内存分析器、套接字、图形、HID（输入设备）、声音、物理等都会被设置。应用程序配置（*game.project*）也会被加载和设置。

![Preinitialization](images/application_lifecycle/pre_init.png)

在引擎初始化结束时，第一个可由用户控制的入口点是调用当前渲染脚本的 `init()` 函数。

然后主集合会被加载并初始化。

### 集合初始化

在 `Collection Init` 阶段，集合中的所有游戏对象都会将它们的变换：平移（位置变化）、旋转和缩放应用到子对象。随后会调用所有存在的组件 `init()` 函数。

![Collection Init](images/application_lifecycle/collection_init.png)

::: sidenote
游戏对象组件 `init()` 函数的调用顺序未指定。您不应假设引擎会以某个特定顺序初始化同一集合中的对象。
:::

### 初始化中的后更新

随后，引擎会执行完整的 `Post Update` 阶段，这与稍后每次 `Update Loop` 步骤之后执行的阶段相同。它在初始化结束时执行，因为您的 `init()` 代码可能会发送新消息、指示工厂生成新对象、将对象标记为删除，或执行其他操作。

![Post Update](images/application_lifecycle/post_init.png)

此阶段会执行消息传递、实际的工厂游戏对象生成和对象删除。请注意，`Post Update` 阶段包含一个“分发消息”序列，它不仅会传递排队的消息，也会处理发送给集合代理的消息。后续的代理更新（enable、disable、init、final、loading 以及标记为卸载）都会在这些步骤中执行。

完全可以在 `init()` 中加载一个[集合代理](/manuals/collection-proxy)，确保其中所有对象都已初始化，然后通过代理卸载该集合；所有这些都发生在第一个组件 `update()` 被调用之前，也就是引擎离开初始化阶段并进入更新循环之前：

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- 在执行到这段代码之前，代理集合已经卸载。
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- 代理集合对象的 init() 和 final() 函数
        -- 会在执行到此对象的 update() 之前被调用
    end
end
```

## 更新循环

更新循环每帧按特定顺序运行一次。此顺序可以定义为 5 个主要阶段：

![Update Loop](images/application_lifecycle/update_loop.png)

1. 输入（处理和响应）
2. 更新（包括 Fixed、Regular、Late 以及引擎组件更新）
3. 渲染更新
4. 后更新（卸载集合代理，生成和删除游戏对象）
5. 帧渲染（渲染最终图形）

### 输入阶段

输入会从可用设备读取，根据[输入绑定](/manuals/input)映射，然后分发。任何已获取输入焦点的游戏对象都会将输入发送给其所有组件的 `on_input()` 函数。带脚本组件的游戏对象，以及带 GUI 脚本的 GUI 组件，都会在已定义并获取输入焦点的前提下接收各自组件的 `on_input()` 输入。

![Input Phase](images/application_lifecycle/input_phase.png)

任何已获取输入焦点且包含集合代理组件的游戏对象，都会将输入分发给代理集合中的组件。此过程会沿着已启用集合代理中的已启用集合代理递归进行。

### 更新阶段

`Update` 阶段是更新循环的一部分。它会先为根集合启动一次，然后对每个已启用的集合代理递归运行。

在一个集合内部，Defold 会按组件类型处理回调：它遍历实现了相关阶段的某一组件类型的所有实例，为每个实例调用 Lua 回调，刷新消息，然后继续处理下一个组件类型。

*script* 组件 Lua 回调阶段的高层顺序为：

1. `fixed_update()` - 每帧调用 0..N 次（使用固定时间步时）
2. `update()` - 每帧调用 1 次
3. `late_update()` - 每帧调用 1 次

![Update Phase](images/application_lifecycle/update_phase.png)


主集合中的每个游戏对象组件都会被遍历。如果这些组件中的任意组件带有包含 `fixed_update()`/`update()`/`late_update()` 函数的脚本，就会调用相应函数。如果组件是集合代理，代理集合中的每个组件都会递归地执行 `Update` 阶段中的所有步骤。

::: sidenote
游戏对象组件 `update()` 函数的调用顺序未指定。您不应假设引擎会以某个特定顺序更新同一集合中的对象。`fixed_update()` 和 `late_update()`（自 1.12.0 起）也是如此。
:::

#### 物理

对于碰撞对象组件，物理消息（碰撞、触发器、射线检测响应等）会在包含该组件的游戏对象内分发给所有带有 `on_message()` 函数脚本的组件。

如果物理模拟使用[固定时间步](/manuals/physics/#physics-updates)，所有脚本组件中也可能会调用 `fixed_update()` 函数。在基于物理的游戏中，当您希望以固定间隔操作物理对象以获得稳定的物理模拟时，此函数很有用。

#### 变换

在 `Update Loop` 期间，如果需要，在**每个**组件类型更新之前都会多次更新变换，将任何游戏对象移动、旋转和缩放应用到每个游戏对象组件以及任何子游戏对象组件。

在 `Update Loop` 末尾，如果需要，还会进行一次额外的最终变换更新。

#### 引擎更新阶段（无固定更新）

下面的表描述了*引擎层级*的更新阶段。它们有意省略了确切的内部组件优先级顺序（这是引擎实现细节），但反映了与脚本相关的顺序保证：

- `fixed_update()` 在 `update()` 之前运行
- `late_update()` 在 `update()` 之后运行
- 已发送消息会在组件类型更新之间刷新，也会在脚本回调阶段之间刷新

当 `Use Fixed Timestep` 为 `false` 和/或 Fixed Update Frequency 为 `0` 时，在阶段开始时会准备 `dt`，然后流程如下表所示：

:::sidenote
请注意，在**每个**组件类型更新之后，所有消息都会被分发；为保持表格清晰，下表中没有标出这一点。
:::

| Step | Engine Phase | Lua Callback | Comment |
|-|-|-|-|
| 1 | **Update** | `update()` | 对内部优先级顺序中实现 Update 的每个组件类型，每帧调用一次。此外，使用 `go.animate()` 启动的 GO 属性动画也会作为单独组件类型在此更新。**Physics** 组件在此更新。对于每个已启用的 Collection Proxy，整个 `Update` 阶段会从步骤 1 开始递归调用。 |
| 2 | **Late Update** | `late_update()` | 对内部优先级顺序中实现 Late Update 的每个组件类型，每帧调用一次。 |
| 3 | **Transforms** | | 如果需要，会在末尾为每个组件执行一次额外的最终变换更新。 |

#### 使用固定时间步的引擎更新阶段

当 `Use Fixed Timestep` 为 `true` 且 Fixed Update Frequency 非零时，阶段开始时会准备 `dt`（delta time）、`fixed_dt` 和 `num_fixed_steps`（`0..N`），即根据距离上次更新的时间决定固定更新要调用多少次，以确保固定数量的更新。

:::sidenote
请注意，在**每个**组件类型更新之后，所有消息都会被分发；为保持表格清晰，下表中没有标出这一点。
:::

随后它会循环：

| Step | Engine Phase | Lua Callback | Comment |
|-|-|-|-|
| 1 | **Fixed Update** | `fixed_update()` | 根据时间，对内部优先级顺序中实现 Fixed Update 的每个组件类型，每帧调用 `0..N` 次。它包括 *Physics* 组件的 Fixed Update 步骤。 |
| 2 | **Update** | `update()` | 对内部优先级顺序中实现 Update 的每个组件类型，每帧调用一次。此外，使用 `go.animate()` 启动的 GO 属性动画也会作为单独组件类型在此更新。对于每个已启用的 Collection Proxy，`Update` 阶段会从步骤 1 开始递归调用。 |
| 3 | **Late Update** | `late_update()` | 对内部优先级顺序中实现 Late Update 的每个组件类型，每帧调用一次。 |
| 4 | **Transforms** | | 如果需要，会在末尾为每个组件执行一次额外的最终变换更新。 |

如果您需要更深入了解 Defold 在 Update 阶段内部如何工作，值得直接阅读 [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp) 代码。

### 渲染更新阶段

渲染更新块首先分发所有发送到 `@render` socket 的消息（例如摄像机组件 `set_view_projection` 消息、`set_clear_color` 消息等）。随后调用渲染脚本的 `update()`。

![Render Update Phase](images/application_lifecycle/render_update_phase.png)

### 后更新阶段

更新完成后，会运行后更新序列。它会从内存中卸载标记为卸载的集合代理（这发生在“分发消息”序列期间）。任何标记为删除的游戏对象都会调用其所有组件的 `final()` 函数（如果存在）。`final()` 函数中的代码通常会向队列发送新消息，因此之后会运行“分发消息”阶段。

![Post Update Phase](images/application_lifecycle/post_update_phase.png)

任何被指示生成游戏对象的工厂组件会在接下来执行生成。最后，标记为删除的游戏对象会被实际删除。

### 渲染阶段

更新循环中的最后一步包括分发 `@system` 消息（`exit`、`reboot` 消息，切换 profiler，开始和停止视频捕获等）。

![Render Phase](images/application_lifecycle/render_phase.png)

随后图形会被渲染，visual profiler 的任何渲染也会执行（参见[调试文档](/manuals/debugging)）。图形渲染之后，会执行视频捕获。

#### 帧率和集合时间步

每秒帧更新数（等于每秒更新循环运行次数）可以在项目设置中设置，也可以通过向 `@system` socket 发送 `set_update_frequency` 消息以编程方式设置。此外，还可以通过向代理发送 `set_time_step` 消息，为集合代理单独设置_时间步_。更改集合的时间步不会影响帧率。它会影响物理更新时间步，以及传递给 `update().` 的 `dt` 变量。另请注意，更改时间步不会改变每帧调用 `update()` 的次数——它始终正好调用一次。

（详情请参阅[集合代理手册](/manuals/collection-proxy)和 [`set_time_step`](/ref/collectionproxy#set-time-step)）

#### 引擎节流

Defold 1.12.0 引入了引擎节流 API，可以完全跳过引擎更新和渲染，同时仍然检测输入。任何输入都会再次唤醒引擎，并且引擎可以在冷却后重新进入节流。

有关详细信息和用法示例，请参阅 `sys.set_engine_throttle()` API。

## 最终化

当应用程序退出时，它首先完成最后一次更新循环序列，这会卸载所有集合代理：最终化并删除每个代理集合中的所有游戏对象。

完成后，引擎进入处理主集合及其对象的最终化序列：

![Finalization](images/application_lifecycle/finalization.png)

首先调用组件 `final()` 函数。随后进行消息分发。最后，所有游戏对象都会被删除，主集合被卸载。

随后，引擎会在后台关闭各个子系统：项目配置被删除，内存分析器关闭，等等。

此时应用程序已完全关闭。

## 分发消息

**Dispatching Messages** 是在**每个**组件类型更新之后执行的特殊阶段，例如 sprites 更新、scripts 更新以及任何可能发送消息的其他操作。执行期间，所有收集在队列中的已发送消息都会被分发。它们在图中以小的“带箭头信封”图标 📩 标记。

![Dispatch Messages](images/application_lifecycle/dispatch_messages.png)

在所有**用户消息**通过为每个组件调用 `on_message()` 分发完毕后，Defold 特殊消息会按以下顺序处理（图中也以此顺序展示），并针对每个集合代理执行：

1. `load` 消息 - 加载标记为加载的集合代理，并回发 `proxy_loaded` 消息。
2. `unload` 消息 - 卸载标记为卸载的集合代理，并回发 `proxy_unloaded` 消息。
3. `init` 消息 - 为所有待初始化的集合代理触发 `Collection Init` 阶段。
4. `final` 消息 - 对标记为最终化的代理的所有组件触发 `final()`。
5. `enable` 消息 - 启用集合代理，使其在下一帧执行 `Update Loop`；这会隐式触发集合中每个组件的 `init()`。
6. `disable` 消息 - 禁用集合代理，使其在下一帧**不会**执行 `Update Loop`；它会完全停止运行该代理的 `Update Loop`。

由于任何接收组件的 `on_message()` 代码都可以发送额外消息，消息分发器会递归地继续分发已发送消息，直到消息队列为空。不过，消息分发器运行消息队列的次数是有限制的。详情请参阅[消息链](/manuals/message-passing)。
