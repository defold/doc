---
title: Defold 中的 Lua 模块
brief: Lua 模块允许您构建项目结构并创建可重用的库代码. 本手册介绍了如何在 Defold 中实现这一点.
---

# Lua 模块

Lua 模块允许您构建项目结构并创建可重用的库代码. 通常来说，在项目中避免重复是一个好主意. Defold 允许您使用 Lua 的模块功能将脚本文件包含到其他脚本文件中. 这使您能够将功能（和数据）封装在外部脚本文件中，以便在游戏对象和 GUI 脚本文件中重用.

## 引入 Lua 文件

存储在项目结构中某处以".lua"为文件扩展名的 Lua 代码可以被引入到脚本和 GUI 脚本文件中. 要创建新的 Lua 模块文件，请在 *Assets* 视图中右键单击您想要创建它的文件夹，然后选择 <kbd>New... ▸ Lua Module</kbd>. 给文件一个唯一的名称并按 <kbd>Ok</kbd>:

![new file](images/modules/new_name.png)

假设以下代码被添加到文件"main/anim.lua"中：

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

然后任何脚本都可以引入这个文件并使用该函数：

```lua
require "main.anim"

function update(self, dt)
    -- 更新位置，设置方向等
    ...

    -- 设置动画
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

函数 `require` 加载给定的模块. 它首先查看 `package.loaded` 表来确定模块是否已经加载. 如果已经加载，则 `require` 返回存储在 `package.loaded[module_name]` 中的值. 否则，它会通过加载器加载并评估文件.

提供给 `require` 的文件名字符串的语法有点特殊. Lua 将文件名字符串中的 '.' 字符替换为路径分隔符：在 macOS 和 Linux 上是 '/'，在 Windows 上是 '\'。

请注意，像我们上面那样使用全局作用域来存储状态和定义函数通常是一个坏主意. 您可能会遇到命名冲突，暴露模块的状态或在模块用户之间引入耦合.

## 模块

为了封装数据和函数，Lua 使用 _模块_。Lua 模块是一个常规的 Lua 表，用于包含函数和数据。该表被声明为局部变量，以避免污染全局作用域：

```lua
local M = {}

-- 私有
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

然后可以使用该模块。同样，最好将其分配给局部变量：

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## 模块热重载

考虑一个简单的模块：

```lua
-- module.lua
local M = {} -- 在局部作用域中创建一个新表
M.value = 4711
return M
```

以及该模块的使用者：

```lua
local m = require "module"
print(m.value) --> "4711" (即使 "module.lua" 被更改并热重载)
```

如果您热重载模块文件，代码会再次运行，但 `m.value` 没有任何变化。为什么会这样？

首先，在 "module.lua" 中创建的表是在局部作用域中创建的，并且该表的 _引用_ 被返回给用户。重新加载 "module.lua" 会再次评估模块代码，但这会在局部作用域中创建一个新表，而不是更新 `m` 所引用的表。

其次，Lua 缓存所需的文件。当文件第一次被需要时，它被放在 [`package.loaded`](/ref/package/#package.loaded) 表中，以便在后续需要时可以更快地读取。您可以通过将文件的条目设置为 nil 来强制文件从磁盘重新读取：`package.loaded["my_module"] = nil`。

要正确地热重载模块，您需要重新加载模块，重置缓存，然后重新加载所有使用该模块的文件。这远非最佳选择。

相反，您可以考虑在 _开发期间_ 使用的解决方法：将模块表放在全局作用域中，并让 `M` 引用全局表，而不是在每次文件评估时创建一个新表。重新加载模块会更改全局表的内容：

```lua
--- module.lua

-- 完成后替换为 local M = {}
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## 模块和状态

有状态的模块在模块的所有用户之间共享一个内部状态，可以与单例相比：

```lua
local M = {}

-- 模块的所有用户将共享此表
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

另一方面，无状态的模块不保留任何内部状态。相反，它提供了一种机制，将状态外部化到模块用户本地的单独表中。以下是实现此目的的几种不同方法：

使用状态表
: 也许最简单的方法是使用一个构造函数，它返回一个只包含状态的新表。状态作为每个操作状态表的函数的第一个参数显式传递给模块。

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  像这样使用模块：
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

使用元表
: 另一种方法是使用一个构造函数，每次调用时返回一个包含状态和模块公共函数的新表：

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- 使用冒号表示法时，self 被添加为第一个参数
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  像这样使用模块：

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- 使用冒号表示法时，"my_state" 被添加为第一个参数
  print(my_state:get_state()) --> 43
  ```

使用闭包
: 第三种方法是返回一个包含所有状态和函数的闭包。不需要像使用元表那样将实例作为参数传递（显式或使用冒号运算符隐式传递）。这种方法也比使用元表稍快，因为函数调用不需要通过 `__index` 元方法，但每个闭包都包含自己的方法副本，因此内存消耗更高。

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  像这样使用模块：

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
