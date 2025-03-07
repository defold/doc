---
title: Defold 中的 Lua 模块
brief: Lua 模块使你的项目更具结构化还可以创建可重用库代码. 本教程介绍了其在 Defold 中的用法.
---

# Lua 模块

Lua 模块使你的项目更具结构化还可以创建可重用库代码. 这是降低项目复杂度的好办法. Defold 可以使用 Lua 模块功能把脚本引入到其他脚本中去. 它可以封装函数 (和数据) 到专门的文件以便由游戏对象和 GUI 脚本重用.

## 引入 Lua 文件

Lua 代码保存在游戏项目中的 ".lua" 文件里, 可以由脚本和gui脚本引入. 创建Lua模块, 在 *Assets* 视图右键点击, 选择 <kbd>New... ▸ Lua Module</kbd>. 输入文件名点击 <kbd>Ok</kbd>:

![new file](images/modules/new_name.png)

假设 "main/anim.lua" 有如下代码:

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

这样其他脚本就能引入这个文件使用其中的函数:

```lua
require "main.anim"

function update(self, dt)
    -- 更新位置, 设置方向之类的
    ...

    -- 设置方向动画
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        msg.post("#sprite", "play_animation", { id = anim })
        self.current_anim = anim
    end
end
```

关键字 `require` 引入了模块. 先从 `package.loaded` 表中查找模块是否已被加载. 找到后, `require` 返回 `package.loaded[module_name]` 的值. 否则, 使用加载其加载并处理模块文件.

`require` 接文件名的语法有点特别. Lua 把文件名中的 '.' 替换为路径分隔符: 在 macOS 和 Linux 上是 '/' , 在 Windows 上是 '\\' .

注意尽量不要像上例那样在全局范围保存数据和定义函数. 这样可能会造成命名冲突, 暴露模块数据或者增加模块调用者间的耦合.

## 模块

Lua 使用 _模块_ 封装数据和函数. Lua 模块是用来保存函数和数据的普通表. 这个表被定义在本地而不是全局范围:

```lua
local M = {}

-- 私有
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

这样就定义好了模块. 使用时也是, 最好把模块定义为本地变量:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## 模块热重载

假设有如下模块:

```lua
-- module.lua
local M = {} -- 本地表
M.value = 4711
return M
```

然后使用这个模块: 

```lua
local m = require "module"
print(m.value) --> "4711" (如果 "module.lua" 更改了此值并且完成热重载这个值仍然不变)
```

如果 "module.lua" 更改了此值并且完成热重载 `m.value` 仍然不变. 为什么呢?

首先, "module.lua" 表建立在本地环境下作为 _引用_ 返回. 重载 "module.lua" 模块时解析了代码但是新建了另一个本地表 `m` 却没有更新对它的引用.

其次, Lua 加载了模块. 文件第一次被加载时, 会被放入 [`package.loaded`](/ref/package/#package.loaded) 表中便于后续快速访问. 如果把模块设置为 nil 可以强制它重新加载: `package.loaded["my_module"] = nil`.

要想正确热重载模块, 需要先加载模块, 重置缓存然后更新每个引用模块的文件. 这不利于优化.

一定需要的话可以考虑在 _开发时_ 使用一个解决方法: 把模块表放入全局空间然后返回 `M` 的引用. 重载时会更新全局表:

```lua
--- module.lua

-- 测试完了还是替换成 local M = {}
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## 模块和缓存

带缓存模块的数据表在所有调用者之间共享:

```lua
local M = {}

-- 所有调用者共享此表
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

无缓存模块内部不存储缓存数据. 但是它可以把实例缓存作为本地表暴露给调用者. 有若干种方式实现这样的功能:

使用数据表
: 构造函数返回包含一个值的缓存表. 每个缓存相关函数都需要把实例作为第一个参数传入.

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
  
  调用如下:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

使用元数据表
: 构造函数返回缓存表以及所有缓存相关函数:

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- 使用 : 声明函数会自动添加第一个参数self
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

  调用如下:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- 使用 : 调用函数会自动添加第一个参数"my_state"
  print(my_state:get_state()) --> 43
  ```

使用闭包
:  构造函数返回缓存表及所有相关函数. 无需传入实例作为第一个参数 (无需显式传入也无需用冒号隐式传入). 这种方法运行较快因为不必从元数据 `__index` 查找函数, 但是每个闭包都包含全套功能所以占用内存稍多.

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

  调用如下:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
