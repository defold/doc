---
title: 使用脚本编写游戏逻辑
brief: 本教程介绍了如何使用脚本组件加入游戏逻辑
---

# 脚本

脚本组件使用 [Lua 编程语言](/manuals/lua) 编程. 脚本像其他 [组件](/manuals/components) 一样附加到游戏对象上, Defold 会在引擎声明循环周期中运行这些 Lua 代码.


## 脚本类型

Defold 里有三种脚本, 每种脚本对应各自的 Defold 函数库.

Logic scripts
: 扩展名 _.script_. 在游戏对象的脚本组件里运行. 逻辑脚本通常用于控制游戏对象, 加载关卡, 制定游戏规则之类的. 逻辑脚本可以使用除了 [GUI](/ref/gui) 和 [Render](/ref/render) 函数库以外的所有代码库.


GUI scripts
: 扩展名 _.gui_script_. 在 GUI 组件里使用, 通常用来显示比如对话框, 菜单之类的 GUI 组件. GUI 脚本对应使用 [GUI](/ref/gui) 函数库.


Render scripts
: 扩展名 _.render_script_. 通过渲染流程运行, 包含渲染每帧所有图像的逻辑. 渲染脚本对应使用 [Render](/ref/render) 函数库.


## 脚本运行, 回调和 self

Defold 把 Lua 脚本作为引擎生命周期的一部分来执行并且向脚本暴露了一些生命周期函数. 当你把脚本组件附加到游戏对象上时这个脚本就变成了游戏对象及其组件的生命周期的一部分. 脚本加载后先进行上下文评估, 然后引擎开始执行以下函数同时传递一个当前组件实例的引用作参数. 这个参数就是 `self` , 可以用来保存组件实例上的各种状态.

::: 注意
`self` 是一个 userdata 对象, 可以用作 Lua 表但是不能使用 `pairs()` 或者 `ipairs()`迭代, 而且也不能使用 `pprint()` 输出其内容.
:::

`init(self)`
: 组件初始化时调用.

  ```lua
  function init(self)
      -- 这些变量会在组件生命周期中一直存在
      self.my_var = "something"
      self.age = 0
  end
  ```

`final(self)`
: 组件被删除时调用. 用以进行析构操作, 比如说把早先创建的对象一并删除掉.

  ```lua
  function final(self)
      if self.my_var == "something" then
          -- 做一些清理工作
      end
  end
  ```

`update(self, dt)`
: 每帧调用一次. `dt` 是从上一帧到这一帧的时差.

  ```lua
  function update(self, dt)
      self.age = self.age + dt -- 把每帧时差加到 age 上
  end
  ```

`fixed_update(self, dt)`
: 不基于 update 的固定帧率更新. `dt` 是从上一帧到这一帧的时差. 主要用于对物理对象进行一个稳定的交互模拟的情形. 需要在 *game.project* 文件里设置 `physics.use_fixed_timestep`.

  ```lua
  function fixed_update(self, dt)
      msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
  end
  ```

`on_message(self, message_id, message, sender)`
: 当使用 [`msg.post()`](/ref/msg#msg.post) 把消息发送到脚本组件上时, 接收方组件的脚本中此函数被调用.

    ```lua
    function on_message(self, message_id, message, sender)
        if message_id == hash("increase_score") then
            self.total_score = self.total_score + message.score
        end
    end
    ```
    
`on_input(self, action_id, action)`
: 如果组件掌握输入焦点 (见 [`acquire_input_focus`](/ref/go/#acquire_input_focus)) 那么当输入触发时此函数被引擎调用.


    ```lua
    function on_input(self, action_id, action)
        if action_id == hash("touch") and action.pressed then
            print("Touch", action.x, action.y)
        end
    end
    ```
    
`on_reload(self)`
: 当使用编辑器的热重载功能 (<kbd>Edit ▸ Reload Resource</kbd>) 重载脚本时此函数被调用. 这对于调试, 测试和微调看效果等需求非常方便. 详情请见 [热重载教程](/manuals/hot-reload).

  ```lua
  function on_reload(self)
      print(self.age) -- 输出对象的 age
  end
  ```


## 链式逻辑

带脚本的游戏对象可以实现一些逻辑. 通常, 逻辑是否触发取决于一些条件. 玩家走到敌人一定距离之内才会触发敌人AI; 关闭的们只有在玩家交互之后才能打开等等等等.

在 `update()` 函数中可以实现复杂的行为定义比如每帧运行的状态机---有时这是不错的用法. 但是每帧调用一个 `update()` 一点点计时有点浪费. 可以的话最好自己实现一个不依靠update _链式逻辑_. 它不是被动等待时间累计而是主动设置触发时间目标. 此外, 链式逻辑的设计往往需要尽量简洁稳定易于实现.

来看一个具体实例. 假设你希望一个脚本初始化2秒后发出一个消息. 然后等待消息被收到, 之后过5秒再发一个消息. 非链式逻辑代码看起里像这样:

```lua
function init(self)
    -- 计时器.
    self.counter = 0
    -- 状态.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- 2 秒后发送消息
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- 状态改变后 5 秒再发送一个消息
        msg.post("another_object", "another_message")
        --再次改变状态以避免再次进入这里的代码.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- 第一个消息收到, 改变状态
        self.state = "second"
        -- 清空计时器
        self.counter = 0
    end
end
```

本来逻辑挺简单, 代码却麻烦的一塌糊涂. 其实使用携程 (见下文) 就能大大简化代码复杂度, 这回先用内置计时器功能改写一下.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- 等 2 秒后调用 send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- 等 5 秒后调用 send_second()
		timer.delay(5, false, send_second)
	end
end
```

这样就简单易懂多了. 不需要导出调整状态变量 --- 不小心就出错. 我们还完全离开了 `update()` 功能. 这样就不必让引擎每秒白白调用 60 次函数, 尽管里面没代码.


## 编辑器支持

Defold 编辑器支持 Lua 脚本编辑, 还提供语法高亮和自动补全功能. 要让 Defold 补全函数名, 按 *Ctrl+Space* 会弹出相关函名数列表.

![Auto completion](images/script/completion.png){srcset="images/script/completion@2x.png 2x"}
