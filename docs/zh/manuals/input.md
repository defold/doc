---
title: Defold 的设备输入操作
brief: 本教程介绍了输入系统如何工作, 如何捕获输入行为和相关脚本代码.
---

# 输入

输入由引擎捕获并转化为输入行为传送到获取了输入焦点并且实现了 `on_input()` 函数的游戏对象脚本组件中去. 本教程介绍了捕获输入绑定行为的方法以及如何用代码对输入做出响应.

输入系统包含一些概念, 用以让开发者直观地处理游戏逻辑.

![Input bindings](images/input/overview.png){srcset="images/input/overview@2x.png 2x"}

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

输入绑定是整个项目通用的, 记录如何把设备输入映射为带名字的 *动作* 以方便脚本使用的列表. 新建输入绑定文件, 在 *Assets* 视图中 <kbd>右键点击</kbd> 选择 <kbd>New... ▸ Input Binding</kbd>. 然后修改 "game.project" 里 *Game Binding* 项对输入绑定文件的引用.

![Input binding setting](images/input/setting.png){srcset="images/input/setting@2x.png 2x"}

每个新建项目都会自动生成默认输入绑定文件. 默认叫做 "game.input_binding", 位于项目根目录下 "input" 文件夹内. <kbd>双击</kbd> 即可在编辑器中打开此文件:

![Input set bindings](images/input/input_binding.png){srcset="images/input/input_binding@2x.png 2x"}

点击相关触发类型底部的 <kbd>+</kbd> 按钮, 即可新建一个绑定项. 每一项有两个部分:

*Input*
: 需要监听的底层输入信号, 从滚动列表里选择.

*Action*
: 输入对应的用于发送给脚本的动作名. 一个动作可以对应多个输入. 例如, 可以设置按下 <kbd>空格</kbd> 键和游戏手柄 "A" 按钮都是 `jump` 动作. 可是触屏输入的动作名必须是唯一值.

## 触发器类型

触发器有五种类型:

Key Triggers
: 键盘单键输入. 每个键分别映射为动作. 一个键一个功能, 比如箭头键或者 WASD 键对应上左下右. 如果需要获得输入字符, 要使用 text triggers (见下文).

Mouse Triggers
: 鼠标按键或者滚轮输入. 鼠标移动输入事件不在这里设定. 但是如果没设定鼠标触发器, 也不会捕获鼠标移动事件.

  - 鼠标按键输入 `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` 和 `MOUSE_BUTTON_MIDDLE` 等同于 `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` 和 `MOUSE_BUTTON_3`.

  - **单点触摸也会触发 `MOUSE_BUTTON_LEFT` (或 `MOUSE_BUTTON_1`) 事件**.

  - 鼠标滚轮转动输入. 如果 `action.value` 为 `1` 代表转动, 为 `0` 代表不转动. (滚轮转动被当作按钮按下处理. Defold 目前不支持触摸板上的滚轮输入.)

  - 鼠标移动不在此做设定, 但是鼠标移动时会自动发出事件, 其中 `action_id` 为 `nil` 并且 `action` 表保存了鼠标位置与移动距离.

Gamepad Triggers
: 游戏手柄触发器绑定标准手柄输入到游戏功能的映射. Defold 通过操作系统支持多种游戏手柄, 事件里 `gamepad` 项对应手柄输入来源:

  ```lua
  if action_id == hash("gamepad_start") then
    if action.gamepad == 0 then
      -- gamepad 0 申请加入游戏
    end
  end
  ```

  游戏手柄可以绑定:

  - 左右摇杆 (方向和按下)
  - 手柄按钮. 通常右手柄 Xbox 为 "A", "B", "X" 和 "Y", Playstation 为 "方块", "圆圈", "三角" 和 "十叉".
  - 方向按钮.
  - 左右肩按钮.
  - 开始, 后退, 暂停按钮

  在 Windows 上, 只支持 XBox 360 兼容手柄. 安装方法请见 http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows

  每种手柄分别对应一份映射文件. 详情请见下文.
  
  游戏手柄还有 `Connected` 和 `Disconnected` 两种事件用以通知手柄连接和断开.

Touch Triggers
: iOS 和 Android 设备支持单点触摸. 单点触摸不用在触摸映射部分进行设置. 而在 **鼠标映射设置 `MOUSE_BUTTON_LEFT` 或 `MOUSE_BUTTON_1`** 之后自动触发.

: iOS 和 Android 设备支持 APP 和 HTML5 应用的多点触摸. 触发时 `touch` 表即是记录触摸点的数组. 其中数组键 `1`--`N` 的 `N` 是触摸点的排号. 对应的值为触摸点数据:

  ```lua
  -- 捕获到接触事件时触发
  for i, touchdata in ipairs(action.touch) do
    local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
    factory.create("#factory", pos)
  end
  ```

::: 注意
多点触摸动作名不能与 `MOUSE_BUTTON_LEFT` 或 `MOUSE_BUTTON_1` 的动作名重名. 否则的话将导致事件覆盖, 就监听不到单点触摸事件了.
:::

::: 注意
公共资源 [Defold 输入手柄](https://defold.com/assets/defoldinput/) 可以用来在多点触摸屏上模拟手柄输入.
:::

Text Triggers
: 文本触发器用来读取输入的文字. 分为以下两种:

  - `text` 捕获一般字符输入. 事件 `text` 项保存了输入的字符. 动作由按下按钮时触发, 不存在 `release` 和 `repeated` 事件.

    ```lua
    if action_id == hash("text") then
      -- 收集输入字符填充 "user" 节点...
      local node = gui.get_node("user")
      local name = gui.get_text(node)
      name = name .. action.text
      gui.set_text(node, name)
    end
    ```

  - `marked-text` 一般用于亚洲键盘可把多个按键事件合为一个输入事件. 比如说, iOS 里的 "Japanese-Kana" 键盘, 用户输入多个键时键盘上方就会显示出可供输入的文字或字符串.

  ![Input marked text](images/input/marked_text.png){srcset="images/input/marked_text@2x.png 2x"}

  - 每个键被按下时触发事件, 动作 `text` 为目前已经输入了的字符串 (星号标记文本).
  - 用户选择了要提交的文字时, 一个 `text` 类型动作被触发 (证明当前触发器配置正确). 而这个动作的 `text` 项保存了用户最终提交的文字.

## 输入焦点

脚本要想获得输入消息, 就要把 `acquire_input_focus` 消息发给其所在的游戏对象:

```lua
-- 告诉当前游戏对象 (".") 要接收输入消息了
msg.post(".", "acquire_input_focus")
```

此消息让引擎把可接收输入的游戏对象组件 (脚本, GUI 和集合代理) 压入 *输入栈*. 这些组件位于栈顶; 最后入栈的组件位于栈顶. 注意如果一个游戏对象包含多个输入组件, 所有组件都会入栈:

![Input stack](images/input/input_stack.png){srcset="images/input/input_stack@2x.png 2x"}

由集合代理加载的每个游戏世界都有自己的输入栈. 被加载的游戏世界获得输入, 前提是主游戏世界输入栈里包含了这个游戏世界的集合代理.

已获得输入焦点的游戏对象再次请求焦点的话, 它上面的所有组件都会被推到输入栈顶.

要取消动作监听, 发送 `release_input_focus` 消息给游戏对象即可. 这样该游戏对象的所有组件都会从输入栈中移除:

```lua
-- 告诉当前游戏对象 (".") 释放输入焦点.
msg.post(".", "release_input_focus")
```

## 输入调度和 on_input() 函数

输入事件在输入栈上, 从上到下传递.

![Action dispatch](images/input/actions.png){srcset="images/input/actions@2x.png 2x"}

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

集合代理必须位于主世界输入栈中才能把输入传递到其代理的游戏世界中去. 代理入栈的组件优先与主世界组件获得输入事件触发动作:

![Action dispatch to proxies](images/input/proxy.png){srcset="images/input/proxy@2x.png 2x"}

使用集合代理组件时经常会忘记让其游戏对象 `acquire_input_focus`. 没有这一步其加载的游戏世界将得不到任何输入信息.

## Consuming input

每个 `on_input()` 函数都能决定当前动作是否要阻止其继续传播下去:

- 如果 `on_input()` 返回 `false`, 或者未返回值 (此时默认返回 `nil` 也被看作是false) 输入动作会继续传播.
- 如果 `on_input()` 返回 `true` 输入就此销毁. 再无组件可以接收到这个消息. 作用于 *全部* 输入栈. 也就是说集合代理加载的组件销毁输入那么主栈的组件就收不到这个输入消息了:

![consuming input](images/input/consuming.png){srcset="images/input/consuming@2x.png 2x"}

输入消耗可以使游戏变得灵活, 控制性更强. 例如, 如果需要弹出菜单暂时只有部分界面可以接受点击:

![consuming input](images/input/game.png){srcset="images/input/game@2x.png 2x"}

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

![pause menu](images/input/game_paused.png){srcset="images/input/game_paused@2x.png 2x"}

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


## 拾取检测

游戏里经常可见拾取操作. 可能是玩家点击界面按钮或者战略游戏里玩家选取一个作战单位, RPG 游戏点取宝箱等等. 不同组件有不同解决方法.

### 界面点击检测

界面有一个 `gui.pick_node(node, x, y)` 函数来判断点击输入是否处在某个节点范围之内. 详见 [API 文档](/ref/gui/#gui.pick_node:node-x-y), [指针悬停示例](https://www.defold.com/examples/pointer_over/) 或者 [按钮示例](https://www.defold.com/examples/button/).

### 游戏对象点击检测
游戏对象检测有点复杂, 因为摄像机移动和渲染脚本映射都会影响位置计算. 方法主要分为两种:

  1. 追踪游戏对象的位置和大小然后检测点选位置是否包含在内.
  2. 给游戏对象加入碰撞组件再在点选位置生成一个碰撞对象检查二者碰撞情况.

::: 注意
公共资源 [Defold 输入库](https://github.com/britzl/defold-input) 是一个开箱即用的输入检测库.
:::

无论哪种方案都必须将鼠标手点选的屏幕坐标转换成游戏对象的世界坐标. 实现思路如下:

  * 手动跟踪渲染脚本使用的视口和投射用以进行坐标转换. 详见 [摄像机教程的这个示例](/manuals/camera/#鼠标位置转换为世界坐标).
  * 使用 [第三方摄像机解决方案](/manuals/camera/#第三方摄像机解决方案) 里面的屏幕到世界坐标转换函数.


## 游戏手柄配置文件

游戏手柄配置保存在 *gamepads* 文件里. Defold 自带一个通用手柄配置文件:

![Gamepad settings](images/input/gamepads.png){srcset="images/input/gamepads@2x.png 2x"}

如需自定义手柄配置, 这里有个工具可供使用:

[gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

其中包含可运行于 Windows, Linux 和 macOS 上的可执行文件. 从命令行打开:

```sh
./gdc
```

工具提示你按下手柄某个按键. 然后输出配置文件. 保存这个文件, 并在 "game.project" 里引用它:

![Gamepad settings](images/input/gamepad_setting.png){srcset="images/input/gamepad_setting@2x.png 2x"}
