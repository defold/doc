---
title: Defold 中的 GUI 脚本 
brief: 本教程介绍了 GUI 脚本.
---

# GUI 脚本

为了控制 GUI 逻辑和动画节点要使用 Lua 脚本. GUI 脚本和游戏对象脚本一样, 但是扩展名不一样而且使用的函数集不一样: 使用 `gui` 模块函数.

## 在 GUI 上添加脚本

要在 GUI 上添加脚本, 首先在 *Assets* 浏览器里<kbd>右键点击</kbd> 再在弹出菜单选择 <kbd>New ▸ Gui Script</kbd> 来创建 GUI 脚本.

编辑器会自动打开脚本文件. 它基于一个模板, 各种空白生命周期函数齐全, 跟游戏对象脚本一样:

```lua
function init(self)
   -- Add initialization code here
   -- Remove this function if not needed
end

function final(self)
   -- Add finalization code here
   -- Remove this function if not needed
end

function update(self, dt)
   -- Add update code here
   -- Remove this function if not needed
end

function on_message(self, message_id, message, sender)
   -- Add message-handling code here
   -- Remove this function if not needed
end

function on_input(self, action_id, action)
   -- Add input-handling code here
   -- Remove this function if not needed
end

function on_reload(self)
   -- Add input-handling code here
   -- Remove this function if not needed
end
```

要把脚本添加到 GUI 组件, 打开 GUI 蓝图文件, 在 *Outline* 里选择根节点显示出 GUI *Properties*. 把 *Script* 属性设置为脚本文件即可.

![Script](images/gui-script/set_script.png){srcset="images/gui-script/set_script@2x.png 2x"}

如果这个 GUI 组件被添加到游戏中的游戏对象里, 它上面的脚本就可以运行了.

## "gui" 命名空间

GUI 脚本访问 `gui` 命名空间及其 [所有gui函数](/ref/gui). `go` 命名空间不可用, 所以要注意区分游戏对象的脚本组件以及二者间的消息传递. 尝试使用 `go` 函数会报错:

```lua
function init(self)
   local id = go.get_id()
end
```

```txt
ERROR:SCRIPT: /main/my_gui.gui_script:2: You can only access go.* functions and values from a script instance (.script file)
stack traceback:
   [C]: in function 'get_id'
   /main/my_gui.gui_script:2: in function </main/my_gui.gui_script:1>
```

## 消息传递

游戏运行时 GUI 脚本可与其他对象互相传递消息, 同其他脚本组件相同.

定位 GUI 组件也与其他脚本组件中定位方法相同:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![message passing](images/gui-script/message_passing.png){srcset="images/gui-script/message_passing@2x.png 2x"}

## 定位节点

GUI 中的节点可由脚本控制. 在编辑器中每个节点都有唯一 *Id*:

![message passing](images/gui-script/node_id.png){srcset="images/gui-script/node_id@2x.png 2x"}

*Id* 使得脚本引用节点并对其使用 [gui 命名空间函数](/ref/gui) 进行控制:

```lua
-- 扩展 10 单位血条
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## 动态创建节点

在运行时使用脚本创建新节点有两种方法. 一种是通过调用 `gui.new_[type]_node()` 函数. 该函数返回新节点引用以便对其进行控制:

```lua
-- 新建节点
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- 新建文本节点
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![dynamic node](images/gui-script/dynamic_nodes.png){srcset="images/gui-script/dynamic_nodes@2x.png 2x"}

第二种方法是通过调用 `gui.clone()` 函数克隆一个已存在的节点或者通过调用 `gui.clone_tree()` 函数克隆一个已存在的节点树:

```lua
-- 克隆血条
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- 克隆按钮节点树
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- 获得节点树根节点
local new_root = new_button_nodes["my_button"]

-- 向右移动根节点 (及其子节点) 300 像素
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## 动态节点id

动态创建的节点没有id. 设计上就是这样. 引用由 `gui.new_[type]_node()`, `gui.clone()` 和 `gui.clone_tree()` 函数返回, 这是访问动态节点的唯一途径, 记得保留好这个引用.

```lua
-- 添加文本节点
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" 保存新节点的引用.
-- 新节点没有 id, 但是没关系. 得到节点的引用
-- 就没有必要使用 gui.get_node() 函数了.
```
