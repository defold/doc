---
title: 热重载
brief: 本教程介绍了 Defold 中的热重载特性.
---

# 热重载资源

Defold 允许资源的热重载. 开发游戏时此功能可以大大节省时间. 它可以让你在游戏运行时修改代码和内容. 经常用于:

- 使用 Lua 脚本调整游戏.
- 编辑调整可视元素 (比如粒子特效或 GUI 元素) 即时观察效果.
- 编辑调整 shader 代码即时观察效果.
- 测试时重启关卡, 设定状态之类---而不用关闭游戏.

## 如何热重载

从编辑器启动游戏 (<kbd>Project ▸ Build</kbd>).

选择菜单项 <kbd>File ▸ Hot Reload</kbd> 或者通过键盘快捷键实现热重载:

![Reloading resources](images/hot-reload/menu.png){srcset="images/hot-reload/menu@2x.png 2x"}

## 设备上的热重载

除了桌面设备, 热重载也可以其他设备上使用. 要在设备上使用热重载, 在移动设备上运行游戏的调试（debug）版本, 或者运行 [开发应用](/manuals/dev-app) , 然后在编辑器中选择目标设备:

![target device](images/hot-reload/target.png){srcset="images/hot-reload/target@2x.png 2x"}

当编译运行时, 编辑器会把所有资源上传到设备上运行着的游戏里. 也就是说, 热重载的所有文件都会在设备上进行更新.

比如, 想在手机上运行着的游戏 GUI 上添加几个按钮, 仅需要打开 GUI 文件:

![reload gui](images/hot-reload/gui.png){srcset="images/hot-reload/gui@2x.png 2x"}

加入按钮, 保存并热重载 GUI 文件. 然后在手机上就能看见新建的按钮了:

![reloaded gui](images/hot-reload/gui-reloaded.png){srcset="images/hot-reload/gui-reloaded@2x.png 2x"}

当你将某个文件进行热重载, 游戏引擎会在控制台列出每个被热重载了的资源文件.

## 重载脚本

任何被重载的 Lua 脚本文件都会在 Lua 运行环境里重新执行.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

修改 `my_value` 为 11 然后进行热重载就可以看到改动立刻生效了:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

注意热重载不影响生命周期函数的执行. 比如热更新不会自动调用 `init()` 函数. 当然在这些函数上所做的修改, 还是会被更新的.

## 重载 Lua 模块

只要在模块文件中加入了全局变量, 重载此模块文件后变量也会随之更新:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Lua 模块的一个常用方法是构造一个局部数据表, 输出并返回它:

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

更改并重载 "my_module.lua" 并 _不会_ 更新 "user.script" 的输出值. 关于这种情况的成因以及如何避免, 详见 [模块教程](/manuals/modules).

## on_reload() 函数

所有脚本组件都能定义 `on_reload()` 函数. 如果此函数存在, 则在重载时会自动被调用. 对于检查和修改数据, 发送消息之类的很有用:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## 重载shader数据

当重载顶点与片元着色器时, GLSL 代码会被显卡驱动程序重新编译并上传至 GPU. 因为 GLSL 很底层的所以很有可能出现着色器代码崩溃的情况, 这种情况下游戏引擎也会崩溃.
