---
title: Defold 的设备输入操作
brief: 本教程介绍了输入系统如何工作, 如何捕获输入行为和相关脚本代码.
---

# 输入

输入由引擎捕获并转化为输入行为传送到获取了输入焦点并且实现了 `on_input()` 函数的游戏对象脚本组件中去. 本教程介绍了捕获输入绑定行为的方法以及如何用代码对输入做出响应.

输入系统包含一些概念, 用以让开发者直观地处理游戏逻辑.

![Input bindings](images/input/overview.png)

Devices
: 不管是插上的, 连上的, 有线无线的, 操作系统级别的底层能够进行输入的设备. Defold 支持以下设备:

  1. 键盘 (包括按键输入和文本输入)
  2. 鼠标 (位置, 按键, 滚轮输入)
  3. 单点/多点触摸屏 (iOS, Android 设备和 HTML5 手机端)
  4. 游戏手柄 (操作系统负责将其输入发送给游戏然后映射给脚本. 详见 [游戏手柄配置文件](#gamepads-settings-file))

Input bindings
: 发送给脚本之前设备原始输入信号要通过映射表转化为有意义的 *动作* 指令.

Actions
: 动作是列在输入绑定文件里的 (哈希过的) 名字. 每种动作还包括其相关数据: 比如按钮是被按下还是抬起, 鼠标或触摸屏幕坐标等等.

Input listeners
: 脚本可以得到 *获取了输入焦点的* 组件的输入消息. 一个输入信息可以同时激活多个输入监听器.

Input stack
: 首个获取输入焦点的组件位于最下端, 最后一个获取输入焦点的组件位于最上端的输入监听器堆栈.

Consuming input
: 脚本消耗了输入信息, 不再让输入栈的深层监听器得到这个信息.

## 输入绑定设置

输入绑定是整个项目通用的, 记录如何把设备输入映射为带名字的 *动作* 以方便脚本使用的列表. 新建输入绑定文件, 在 *Assets* 视图中 <kbd>右键点击</kbd> 选择 <kbd>New... ▸ Input Binding</kbd>. 然后修改 *game.project* 里 *Game Binding* 项对输入绑定文件的引用.

![Input binding setting](images/input/setting.png)

每个新建项目都会自动生成默认输入绑定文件. 默认叫做 "game.input_binding", 位于项目根目录下 "input" 文件夹内. <kbd>双击</kbd> 即可在编辑器中打开此文件:

![Input set bindings](images/input/input_binding.png)

点击相关触发类型底部的 <kbd>+</kbd> 按钮, 即可新建一个绑定项. 每一项有两个部分:

*Input*
: 需要监听的底层输入信号, 从滚动列表里选择.

*Action*
: 输入对应的用于发送给脚本的动作名. 一个动作可以对应多个输入. 例如, 可以设置按下 <kbd>空格</kbd> 键和游戏手柄 "A" 按钮都是 `jump` 动作. 可是触屏输入的动作名必须是唯一值.

## 触发器类型

触发器有五种类型:

Key Triggers
: 键盘单键输入. 每个键分别映射为指定的动作. 一一对应. 详情请见 [键盘按键输入教程](/manuals/input-key-and-text).

Text Triggers
: 文本触发器用来读取输入的文字. 详情请见 [键盘按键输入教程](/manuals/input-key-and-text).

Mouse Triggers
: 来自鼠标按键和滚轮的输入. 详情请见 [鼠标和触摸输入教程](/manuals/input-mouse-and-touch).

Touch Triggers
: iOS 和 Android 设备上运行的原生应用与HTML5应用都支持单点和多点触摸输入. 详情请见 [鼠标和触摸输入教程](/manuals/input-mouse-and-touch).

Gamepad Triggers
: 这种触发器可以绑定标准手柄输入到游戏功能的映射. 详情请见 [游戏手柄输入教程](/manuals/input-gamepads).

### 加速度计输入

除了上述五种输入触发器, Defold 还支持 Android 和 iOS 原生系统加速度计输入. 需要勾选 *game.project* 配置文件中输入部分里的 Use Accelerometer.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- 读取加速度计数据
    end
end
```

## 输入焦点

脚本要想获得输入消息, 就要把 `acquire_input_focus` 消息发给其所在的游戏对象:

```lua
-- 告诉当前游戏对象 (".") 要接收输入消息了
msg.post(".", "acquire_input_focus")
```

此消息让引擎把可接收输入的游戏对象组件 (脚本, GUI 和集合代理) 压入 *输入栈*. 这些组件位于栈顶; 最后入栈的组件位于栈顶. 注意如果一个游戏对象包含多个输入组件, 所有组件都会入栈:

![Input stack](images/input/input_stack.png)

如果已获得输入焦点的游戏对象再次请求输入焦点, 那么其组件会被移至输入栈顶端.


## 输入调度和 on_input() 函数

输入事件在输入栈上, 从上到下传递.

![Action dispatch](images/input/actions.png)

每个入栈组件都有 `on_input()` 函数, 一帧中每个输入都调用一次该函数, 连同如下参数:

`self`
: 当前脚本实例引用.

`action_id`
: 动作名哈希串, 与输入映射配置的名称一致.

`action`
: 有关动作的表, 包含比如输入值, 位置和移动距离, 按键是不是 `按下` 状态等等. 详情请见 [on_input() 函数](/ref/go#on_input).

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- 左移
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- 右移
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### 输入焦点与集合代理组件

由集合代理动态载入的游戏世界都有自己的输入栈. 为了让被载入的游戏世界获得输入信息, 集合代理组件必须位于主游戏世界的输入栈里. 被加载的游戏世界优先于主游戏世界获得输入信息:

![Action dispatch to proxies](images/input/proxy.png)

::: sidenote
开发者经常会忘记发送 `acquire_input_focus` 来使集合代理所在的游戏对象获得输入焦点. 不这么做的话此集合代理加载的所有游戏世界都无法获得输入消息.
:::


### 释放输入焦点

要取消动作监听, 发送 `release_input_focus` 消息给游戏对象即可. 这样该游戏对象的所有组件都会从输入栈中移除:

```lua
-- 告诉当前游戏对象 (".") 释放输入焦点.
msg.post(".", "release_input_focus")
```


## 输入传播

每个 `on_input()` 函数都能决定当前动作是否要阻止其继续传播下去:

- 如果 `on_input()` 返回 `false`, 或者未返回值 (此时默认返回 `nil` 也被看作是false) 输入动作会继续传播.
- 如果 `on_input()` 返回 `true` 输入就此销毁. 再无组件可以接收到这个消息. 作用于 *全部* 输入栈. 也就是说集合代理加载的组件销毁输入那么主栈的组件就收不到这个输入消息了:

![consuming input](images/input/consuming.png)

输入消耗可以使游戏变得灵活, 控制性更强. 例如, 如果需要弹出菜单暂时只有部分界面可以接受点击:

![consuming input](images/input/game.png)

菜单开始是隐藏的 (disabled) 玩家点击 "PAUSE" 组件, 菜单被激活:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- 玩家点击了 PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- 弹出暂停菜单.
            msg.post("pause_menu", "show")
        end
    end
end
```

![pause menu](images/input/game_paused.png)

此时弹出的暂停菜单获得输入焦点并且消耗输入, 以防止点击穿透:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- 显示暂停菜单.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- 获得输入焦点.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- 这里做其他游戏逻辑...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- 隐藏暂停菜单
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- 释放输入焦点.
        msg.post(".", "release_input_focus")
    end
  end

  -- 消耗掉输入. 输入栈里其他组件
  -- 不会得到输入, 直到脚本释放输入焦点.
  return true
end
```
