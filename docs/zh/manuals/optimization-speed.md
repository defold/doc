---
title: 优化 Defold 游戏的运行时性能
brief: 本手册描述了如何优化 Defold 游戏以稳定的帧率运行。
---

# 优化运行时速度
在尝试优化游戏以使其以稳定的高帧率运行之前，您需要了解瓶颈在哪里。在游戏的一帧中，实际上是什么占用了大部分时间？是渲染吗？是您的游戏逻辑吗？是场景图吗？为了弄清楚这一点，建议使用内置的性能分析工具。使用[屏幕或网页分析器](/manuals/profiling/)来采样游戏的性能，然后决定是否以及优化什么。一旦您更好地了解什么占用了时间，就可以开始解决这些问题。

## 减少脚本执行时间
如果分析器显示`Script`作用域的值很高，则需要减少脚本执行时间。作为一般经验法则，您当然应该尝试每帧运行尽可能少的代码。每帧在`update()`和`on_input()`中运行大量代码可能会影响游戏的性能，尤其是在低端设备上。一些指导原则是：

### 使用反应式代码模式
如果您可以获得回调，就不要轮询更改。不要手动动画或执行可以交给引擎的任务（例如，`go.animate()`与手动动画相比）。

### 减少垃圾回收
如果您每帧创建大量短生命周期的对象，如Lua表，最终会触发Lua的垃圾收集器。当这种情况发生时，它可能表现为帧时间中的小卡顿/峰值。尽可能重用表，并尽量避免在循环和类似构造中创建Lua表。

### 预哈希消息和动作ID
如果您进行大量消息处理或需要处理许多输入事件，建议预哈希字符串。考虑这段代码：

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

在上述场景中，每次收到消息时都会重新创建哈希字符串。这可以通过创建一次哈希字符串并在处理消息时使用哈希版本来改进：

```lua
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

### 优先使用并缓存URL
消息传递或以其他方式寻址游戏对象或组件可以通过提供字符串或哈希作为ID或作为URL来完成。如果使用字符串或哈希，它将在内部转换为URL。因此，建议缓存经常使用的URL，以获得系统最佳性能。考虑以下情况：

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- 对pos做一些操作
```

在所有三种情况下，都会检索ID为`enemy`的游戏对象的位置。在第一种和第二种情况下，ID（字符串或哈希）将在使用前转换为URL。这告诉我们，最好缓存URL并使用缓存版本以获得最佳性能：

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- 对pos做一些操作
    end
```

## 减少渲染一帧所需时间
如果分析器在`Render`和`Render Script`作用域中显示高值，则需要减少渲染一帧所需时间。在尝试减少渲染一帧所需时间时，有几点需要考虑：

* 减少绘制调用 - 在[这篇论坛帖子](https://forum.defold.com/t/draw-calls-and-defold/4674)中阅读更多关于减少绘制调用的内容
* 减少过度绘制
* 减少着色器复杂度 - 阅读[这篇Khronos文章](https://www.khronos.org/opengl/wiki/GLSL_Optimizations)中的GLSL优化。您还可以修改Defold使用的默认着色器（在`builtins/materials`中找到），并降低着色器精度以在低端设备上获得一些速度。所有着色器都使用`highp`精度，在某些情况下，更改为例如`mediump`可以略微提高性能。

## 减少场景图复杂度
如果分析器在`GameObject`作用域中显示高值，特别是对于`UpdateTransform`采样，则需要减少场景图复杂度。可以采取的一些措施：

* 剔除 - 如果游戏对象（及其组件）当前不可见，则禁用它们。如何确定这一点很大程度上取决于游戏类型。对于2D游戏，可以像禁用矩形区域外的所有游戏对象一样简单。您可以使用物理触发器来检测这一点，或者将您的对象分区到桶中。一旦知道要禁用或启用哪些对象，就可以通过向每个游戏对象发送`disable`或`enable`消息来执行此操作。

## 视锥体剔除
渲染脚本可以自动忽略在定义的边界框（视锥体）之外的游戏对象组件的渲染。在[渲染管线手册](/manuals/render/#frustum-culling)中了解有关视锥体剔除的更多信息。

# 特定平台优化

## Android设备性能框架
Android动态性能框架是一组API，允许游戏更直接地与Android设备的电源和热系统交互。可以监控Android系统上的动态行为，并在不会使设备过热的可持续水平上优化游戏性能。使用[Android动态性能框架扩展](https://defold.com/extension-adpf/)来监控和优化您的Defold游戏在Android设备上的性能。