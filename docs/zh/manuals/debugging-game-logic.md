---
title: Defold 中的调试
brief: 本教程介绍了 Defold 中自带的调试功能.
---

# 调试游戏逻辑

Defold 内置集成式 Lua 调试器及检视工具. 加上内置的 [分析工具](/manuals/profiling) 构成强大工具集帮你快速找到逻辑错误和性能问题.

## 打印输出与可视调试

Defold 最基础的调试功能是 [控制台打印输出](http://en.wikipedia.org/wiki/Debugging#Techniques). 使用 `print()` 或 [`pprint()`](/ref/builtins#pprint) 来检查变量值或者逻辑流程. 如果有个游戏对象不正常, 只需要将包含调试代码的脚本组件拖上去就行了. 打印输出函数会把信息发送到编辑器的 *控制台* 与 [游戏日志](/manuals/debugging-game-and-system-logs) 中.

更进一步来说, 引擎有绘制调试信息的功能, 可以显示文字和画线. 用此功能需要向 `@render` 接口发送消息:

```lua
-- 把变量 "my_val" 画在屏幕上
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- 画出带颜色的文字
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- 在主角和敌人之间画一条线
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

调试绘制与普通的渲染处于同一个渲染管线之上.

* `"draw_line"` 实际是是使用渲染脚本的 `render.draw_debug3d()` 函数进行绘制的.
* `"draw_text"` 使用的是 `/builtins/fonts/debug/always_on_top.font` 字体和 `/builtins/fonts/debug/always_on_top_font.material` 材质.
* `"draw_debug_text"` 与 `"draw_text"` 类似, 只是可以自定义文字颜色.

注意一般调试信息都需要实时更新所以把它们放在 `update()` 函数中是个好主意.

## Running the debugger

一种办法是通过 <kbd>Debug ▸ Run with Debugger</kbd> 运行游戏并且自动接入调试器, 另一种是通过 <kbd>Debug ▸ Attach Debugger</kbd> 把调试器接入正在运行中的游戏上.

![overview](images/debugging/overview.png){srcset="images/debugging/overview@2x.png 2x"}

调试器接入后, 就可以使用控制台上的调试控制按钮, 或者使用 <kbd>Debug</kbd> 菜单了:

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  立即断下游戏. 游戏于此点暂停. 此时可以观察游戏状态, 逐步运行, 或者运行到下一个断点. 断点会在代码编辑器上标识出来:

  ![script](images/debugging/script.png){srcset="images/debugging/script@2x.png 2x"}

Continue
: ![play](images/debugging/play.svg){width=60px .left}
  继续运行游戏. 直到按下暂停键或者遇到断点. 如果遇到断点停下, 运行点会在代码编辑器的断点标识之上标识出来:

  ![break](images/debugging/break.png){srcset="images/debugging/break@2x.png 2x"}

Stop
: ![stop](images/debugging/stop.svg){width=60px .left}
  停止调试. 立即停止调试, 断开调试器, 关闭游戏.

Step Over
: ![step over](images/debugging/step_over.svg){width=60px .left}
  步越. 步进时如果运行到某个 Lua 函数, 步越 _不会进入这个函数_ 而是执行它然后停在函数下一行上. 图中, 如果用户按下 "step over", 调试器会执行代码直至调用 `nextspawn()` 函数下面的 `end` 位置处:

  ![step](images/debugging/step.png){srcset="images/debugging/step@2x.png 2x"}

::: sidenote
一行Lua代码不一定就是一句Lua表达式. 调试器按表达式步进, 也就是说有可能出现一行多个表达式的情况就要多按几下步进才会运行到下一行.
:::

Step Into
: ![step in](images/debugging/step_in.svg){width=60px .left}
  步入. 步进时如果运行到某个 Lua 函数, 步入 _会进入这个函数_. 一个函数调用会在调用堆栈上增加一项. 可以在堆栈列表上点选来查看各函数入口及其所有变量信息. 图中, 用户步入了 `nextspawn()` 函数:

  ![step into](images/debugging/step_into.png){srcset="images/debugging/step_into@2x.png 2x"}

Step Out
: ![step out](images/debugging/step_out.svg){width=60px .left}
  步出. 运行游戏直到函数出口. 如果步入了一个函数, 按 "step out" 按钮能运行代码到函数返回位置.

设置/清除断点
: 可以在代码中随意设置断点. 接入调试器的游戏运行时, 会在断点处暂停, 等待你的下一步交互.

  ![add breakpoint](images/debugging/add_breakpoint.png){srcset="images/debugging/add_breakpoint@2x.png 2x"}

  设置/清除断点, 可以在代码编辑器里行号右边右键点击. 还可以从菜单中选择 <kbd>Edit ▸ Toggle Breakpoint</kbd>.

设置条件断点
: 可以设置需要计算条件为真才触发的断点. 条件可以读取随着代码执行当前行的本地变量.

  ![edit breakpoint](images/debugging/edit_breakpoint.png){srcset="images/debugging/edit_breakpoint@2x.png 2x"}

  要编辑断电条件, 右键点击代码编辑器行号的右边的列, 或者从菜单栏点选 <kbd>Edit ▸ Edit Breakpoint</kbd>.

执行Lua表达式
: 调试器停在断点上时, 可以直接使用包含有当前上下文的 Lua 运行时. 在控制台底部输入表达式后按 <kbd>回车键</kbd> 来运行:

  ![console](images/debugging/console.png){srcset="images/debugging/console@2x.png 2x"}

  目前不支持用表达式来修改变量.

断开调试器
: 通过选择 <kbd>Debug ▸ Detach Debugger</kbd> 可以把调试器从游戏上断开. 游戏会继续运行.

## Lua 调试库

Lua 包含一个有用的调试库, 帮你查看 Lua 环境的底层. 详情请见: http://www.lua.org/pil/contents.html#23.

## 调试步骤

如果发现错误或者bug, 建议进行如下调试:

1. 检查控制台看看输出什么报错没有.

2. 在适当地方加入 `print` 语句证明这段代码运行到了没有.

3. 看看编辑器各种设置是否配置正确. 代码加到游戏对象上了吗? 输入得到焦点了吗? 输入消息监听对了吗? 材质上有着色程序吗? 等等.

4. 如果某些代码取决于变量的值 (比如if语句), 使用 `print` 或者调试器看看那些变量值对不对.

有的 bug 藏得很深, 调试起来很费时, 需要一丝一丝地捋, 逐步缩小可能出错的范围最终消灭错误源头. 这种情况下建议使用 "二分法":

1. 线确定哪一半代码一定包含着错误.
2. 继续二分二分, 缩小范围.
3. 最终找到并消灭错误.

祝你调试愉快!

## 物理引擎调试

如果使用物理系统过程中发现错误请开启物理调试. 在 *game.project* 文件的 *Physics* 部分, 勾选 *Debug* 项:

![physics debug setting](images/debugging/physics_debug_setting.png)

这样 Defold 就会把所有物理形状和碰撞接触点绘制到屏幕上:

![physics debug visualisation](images/debugging/physics_debug_visualisation.png)
