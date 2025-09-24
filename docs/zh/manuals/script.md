---
title: 使用脚本编写游戏逻辑
brief: 本手册描述了如何使用脚本组件添加游戏逻辑。
---

# 脚本

脚本组件允许您使用 [Lua 编程语言](/manuals/lua) 创建游戏逻辑。


## 脚本类型

Defold 中有三种类型的 Lua 脚本，每种脚本都有不同的 Defold 库可用。

游戏对象脚本
: 扩展名 _.script_。这些脚本像任何其他[组件](/manuals/components)一样添加到游戏对象上，Defold 会将 Lua 代码作为引擎生命周期函数的一部分执行。游戏对象脚本通常用于控制游戏对象以及将游戏与关卡加载、游戏规则等绑定的逻辑。游戏对象脚本可以访问 [GO](/ref/go) 函数和所有 Defold 库函数，除了 [GUI](/ref/gui) 和 [Render](/ref/render) 函数。


GUI 脚本
: 扩展名 _.gui_script_。由 GUI 组件运行，通常包含显示 GUI 元素（如平视显示器、菜单等）所需的逻辑。Defold 会将 Lua 代码作为引擎生命周期函数的一部分执行。GUI 脚本可以访问 [GUI](/ref/gui) 函数和所有 Defold 库函数，除了 [GO](/ref/go) 和 [Render](/ref/render) 函数。


渲染脚本
: 扩展名 _.render_script_。由渲染管线运行，包含每帧渲染所有应用/游戏图形所需的逻辑。渲染脚本在游戏生命周期中具有特殊位置。详细信息可在[应用程序生命周期文档](/manuals/application-lifecycle)中找到。渲染脚本可以访问 [Render](/ref/render) 函数和所有 Defold 库函数，除了 [GO](/ref/go) 和 [GUI](/ref/gui) 函数。


## 脚本执行、回调和 self

Defold 将 Lua 脚本作为引擎生命周期的一部分执行，并通过一组预定义的回调函数暴露生命周期。当您将脚本组件添加到游戏对象时，该脚本成为游戏对象及其组件生命周期的一部分。脚本在加载时在 Lua 上下文中评估，然后引擎执行以下函数，并将对当前脚本组件实例的引用作为参数传递。您可以使用这个 `self` 引用在组件实例中存储状态。

::: important
`self` 是一个 userdata 对象，其行为类似于 Lua 表，但您不能使用 `pairs()` 或 `ipairs()` 对其进行迭代，也不能使用 `pprint()` 打印它。
:::

#### `init(self)`
组件初始化时调用。

```lua
function init(self)
  -- 这些变量在组件实例的整个生命周期中都可用
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
组件被删除时调用。这对于清理目的很有用，例如，如果您生成了应该在组件被删除时删除的游戏对象。

```lua
function final(self)
  if self.my_var == "something" then
      -- 进行一些清理
  end
end
```

#### `update(self, dt)`
每帧调用一次。`dt` 包含自上一帧以来的增量时间。

```lua
function update(self, dt)
  self.age = self.age + dt -- 使用时间步长增加年龄
end
```

#### `fixed_update(self, dt)`
与帧率无关的更新。`dt` 包含自上次更新以来的增量时间。当启用 `engine.fixed_update_frequency`（!= 0）时调用此函数。当在 *game.project* 中启用 `physics.use_fixed_timestep` 时，如果您希望以固定间隔操作物理对象以实现稳定的物理模拟，这很有用。

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### on_message(self, message_id, message, sender)
当通过 [`msg.post()`](/ref/msg#msg.post) 将消息发送到脚本组件时，引擎会调用接收器组件的此函数。了解更多关于[消息传递](/manuals/message-passing)的信息。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
如果此组件已获取输入焦点（请参阅 [`acquire_input_focus`](/ref/go/#acquire_input_focus)），则在注册输入时引擎会调用此函数。了解更多关于[输入处理](/manuals/input)的信息。

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
当通过热重载编辑器功能（<kbd>Edit ▸ Reload Resource</kbd>）重载脚本时调用此函数。这对于调试、测试和调整目的非常有用。了解更多关于[热重载](/manuals/hot-reload)的信息。

```lua
function on_reload(self)
  print(self.age) -- 打印此游戏对象的年龄
end
```


## 反应式逻辑

带有脚本组件的游戏对象实现了一些逻辑。通常，该逻辑依赖于某些外部因素。敌人 AI 可能会对玩家位于 AI 一定半径内做出反应；门可能因玩家交互而解锁和打开，等等。

`update()` 函数允许您实现定义为每帧运行的状态机的复杂行为——有时这是足够的方法。但是每次调用 `update()` 都有关联的成本。除非您确实需要该函数，否则应该删除它，而是尝试以_反应式_方式构建您的逻辑。被动等待某些消息触发响应比主动探测游戏世界以获取要响应的数据更便宜。此外，以反应式方式解决设计问题通常也会导致更清洁、更稳定的设计和实现。

让我们看一个具体的例子。假设您希望脚本组件在初始化后 2 秒发送一条消息。然后它应该等待某个响应消息，并在收到响应后 5 秒再发送另一条消息。非反应式代码看起来像这样：

```lua
function init(self)
    -- 用于跟踪时间的计数器
    self.counter = 0
    -- 我们需要这个来跟踪我们的状态
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- 2秒后发送消息
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- 收到"response"后5秒发送消息
        msg.post("another_object", "another_message")
        -- 将状态设为nil，这样我们就不会再次到达这个状态块
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- "first"状态完成。进入下一个
        self.state = "second"
        -- 将计数器归零
        self.counter = 0
    end
end
```

即使在这个相当简单的情况下，我们的逻辑也变得相当复杂。借助模块中的协程（见下文）可以使这看起来更好，但让我们尝试使其成为反应式的并使用内置的计时机制。

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- 等待2秒然后调用send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- 等待5秒然后调用send_second()
		timer.delay(5, false, send_second)
	end
end
```

这更清洁，更容易理解。我们摆脱了在逻辑中通常难以跟踪的内部状态变量——这可能导致微妙的错误。我们还完全摆脱了 `update()` 函数。这使引擎免于每秒调用我们的脚本 60 次，即使它只是在空闲状态。


## 预处理

可以使用 Lua 预处理器和特殊标记根据构建变体有条件地包含代码。示例：

```lua
-- 使用以下关键字之一：RELEASE、DEBUG 或 HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

预处理器作为构建扩展可用。在 [GitHub 上的扩展页面](https://github.com/defold/extension-lua-preprocessor) 了解更多关于如何安装和使用它的信息。


## 编辑器支持

Defold 编辑器支持带有语法着色和自动补全功能的 Lua 脚本编辑。要填写 Defold 函数名，请按 *Ctrl+Space* 弹出与您正在键入的内容匹配的函数列表。

![Auto completion](images/script/completion.png)
