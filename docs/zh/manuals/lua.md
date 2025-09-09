---
title: Defold 中的 Lua 编程
brief: 本手册简要介绍了 Lua 编程基础以及在 Defold 中使用 Lua 的注意事项.
---

# Defold 中的 Lua

Defold 引擎嵌入了 Lua 语言用以编写脚本. Lua 是一种轻量级动态语言, 不但功能强大, 而且速度快, 易于嵌入. 它被广泛运用于游戏脚本编程. Lua 程序使用简单的过程式语法编写. 该语言是动态类型的, 由字节码解释器运行. 它具有自动内存管理和增量垃圾收集功能.

本手册简要介绍了 Lua 编程的基本知识以及在 Defold 中使用 Lua 的注意事项. 如果你有 Python, Perl, Ruby, Javascript 或类似动态语言的经验, 将会很快上手. 如果你是编程新手, 可能需要先阅读一本针对初学者的 Lua 书籍. 有很多这样的书可供选择.

## Lua 版本

Defold 使用 [LuaJIT](https://luajit.org/)，这是一个高度优化的 Lua 版本，适用于游戏和其他性能关键软件。它与 Lua 5.1 完全向上兼容，并支持所有标准 Lua 库函数和完整的 Lua/C API 函数集。

LuaJIT 还添加了几个[语言扩展](https://luajit.org/extensions.html)和一些 Lua 5.2 和 5.3 的功能。

我们努力使 Defold 在所有平台上保持一致，但目前我们在平台之间的 Lua 语言版本上有一些微小差异：
* iOS 不允许 JIT 编译。
* Nintendo Switch 不允许 JIT 编译。
* HTML5 使用 Lua 5.1.4 而不是 LuaJIT。

::: important
为了保证您的游戏在所有支持的平台上都能正常工作，我们强烈建议您只使用 Lua 5.1 的语言功能。
:::


### 标准库和扩展
Defold 包含所有 [Lua 5.1 标准库](http://www.lua.org/manual/5.1/manual.html#5) 以及一个 socket 和位操作库：

  - base (`assert()`, `error()`, `print()`, `ipairs()`, `require()` 等)
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket (来自 [LuaSocket](https://github.com/diegonehab/luasocket))
  - bitop (来自 [BitOp](http://bitop.luajit.org/api.html))

所有库都在 [参考 API 文档](/ref/go) 中有文档说明。

## Lua 书籍和资源

### 在线资源
* [Programming in Lua (第一版)](http://www.lua.org/pil/contents.html) 后续版本有印刷版。
* [Lua 5.1 参考手册](http://www.lua.org/manual/5.1/)
* [15 分钟学习 Lua](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua - 教程部分](https://github.com/LewisJEllis/awesome-lua#tutorials)

### 书籍
* [Programming in Lua](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua 是关于该语言的官方书籍，为任何想要使用 Lua 的程序员提供了坚实的基础。作者是该语言的首席架构师 Roberto Ierusalimschy。
* [Lua programming gems](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - 这本文集记录了一些关于如何用 Lua 编写好程序的现有智慧和经验。
* [Lua 5.1 参考手册](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - 也可以在线获取（见上文）
* [Beginning Lua Programming](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### 视频
* [一个视频学会 Lua](https://www.youtube.com/watch?v=iMacxZQMPXs)

## 语法

程序具有简单易读的语法。语句每行写一个，不需要标记语句的结束。您可以选择使用分号 `;` 来分隔语句。代码块由关键字界定，以 `end` 关键字结束。注释可以是块注释，也可以是行注释：

```lua
--[[
这里是块注释
可以占用好几行.
--]]

a = 10
b = 20 ; c = 30 -- 一行定义俩变量

if my_variable == 3 then
    call_some_function(true) -- 这是一个行注释
else
    call_another_function(false)
end
```

## 变量和数据类型

Lua 是动态类型语言，意味着变量没有类型，但值有类型。与静态类型语言不同，您可以根据需要为任何变量分配任何值。

Lua 中有八种基本类型：

`nil`
: 此类型只有一个值 `nil`。它通常表示没有有用的值，例如未赋值的变量。

  ```lua
  print(my_var) -- 输出 'nil' 因为 'my_var' 还没赋值
  ```

boolean
: 具有 `true` 或 `false` 值。为 `false` 或 `nil` 的条件被视为假。任何其他值使其为真。

  ```lua
  flag = true
  if flag then
      print("flag is true")
  else
      print("flag is false")
  end

  if my_var then
      print("my_var is not nil nor false!")
  end

  if not my_var then
      print("my_var is either nil or false!")
  end
  ```

number
: 数字在内部表示为 64 位 _整数_ 或 64 位 _浮点数_。Lua 根据需要自动在这些表示之间转换，因此您通常不必担心它。

  ```lua
  print(10) --> 输出 '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- 整数
  b = 7/3 -- 浮点数
  print(a - b) --> '2.6666666666667'
  ```

string
: 字符串是不可变的字节序列，可以包含任何 8 位值，包括嵌入的零 (`\0`)。Lua 对字符串内容不做任何假设，因此您可以在其中存储任何您喜欢的数据。字符串字面量用单引号或双引号编写。Lua 在运行时在数字和字符串之间转换。字符串可以用 `..` 运算符连接。

  字符串可以包含以下 C 风格的转义序列：

  | 序列 | 字符 |
  | -------- | --------- |
  | `\a`     | 响铃       |
  | `\b`     | 退格 |
  | `\f`     | 换页  |
  | `\n`     | 换行    |
  | `\r`     | 回车 |
  | `\t`     | 水平制表符 |
  | `\v`     | 垂直制表符   |
  | `\\`     | 反斜杠      |
  | `\"`     | 双引号   |
  | `\'`     | 单引号   |
  | `\[`     | 左方括号    |
  | `\]`     | 右方括号   |
  | `\ddd`   | 由其数值表示的字符，其中 `ddd` 是最多三个 _十进制_ 数字的序列 |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- 报错, 不能转换为 "hello"
  print(my_string .. 1) --> "hello1"

  print("one\nstring") --> one
                       --> string

  print("\097bc") --> "abc"

  multi_line_string = [[
  Here is a chunk of text that runs over several lines. This is all
  put into the string and is sometimes very handy.
  ]]
  ```

function
: 函数是 Lua 中的第一类值，意味着您可以将它们作为参数传递给函数，并将它们作为值返回。分配给函数的变量包含对该函数的引用。您可以将变量分配给匿名函数，但为了方便起见，Lua 提供了语法糖 (`function name(param1, param2) ... end`)。

  ```lua
  -- 赋值 'my_plus' 为函数
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- 函数 'my_mult' 标准声明
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- 把函数 'func' 用作参数
  function operate(func, p, q)
      return func(p, q) -- Calls the provided function with parameters 'p' and 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- 创建 adder 函数并返回该函数
  function create_adder(n)
      return function(a)
          return a + n
      end
  end

  adder = create_adder(2)
  print(adder(3)) --> 5
  print(adder(10)) --> 12
  ```

table
: 表是 Lua 中唯一的数据结构类型。它们是关联数组 _对象_，用于表示列表、数组、序列、符号表、集合、记录、图形、树等。表总是匿名的，分配给表的变量不包含表本身，而是对它的引用。当将表初始化为序列时，第一个索引是 `1`，而不是 `0`。

  ```lua
  -- 初始化表中序列
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- 初始化表作为记录使用
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- 使用构造符号 {} 创建一个表
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- same as t["x"] = 1

  -- 迭代表中键值对
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- u 和 t 都保存了对表的引用
  u[1] = "changed"

  for key, value in pairs(t) do --再次迭代t!
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

userdata
: 提供用户数据以允许任意 C 数据存储在 Lua 变量中。Defold 使用 Lua userdata 对象来存储哈希值 (hash)、URL 对象 (url)、数学对象 (vector3, vector4, matrix4, quaternion)、游戏对象、GUI 节点 (node)、渲染谓词 (predicate)、渲染目标 (render_target) 和渲染常量缓冲区 (constant_buffer)

thread
: 线程表示独立的执行线程，用于实现协程。详见下文。

## 运算符

算术运算符
: 数学运算符 `+`, `-`, `*`, `/`，一元 `-`（取反）和指数 `^`。

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua 在运行时提供数字和字符串之间的自动转换。应用于字符串的任何数字运算都会尝试将字符串转换为数字：

  ```lua
  print("10" + 1) --> 11
  ```

关系/比较运算符
: `<`（小于），`>`（大于），`<=`（小于或等于），`>=`（大于或等于），`==`（等于），`~=`（不等于）。这些运算符总是返回 `true` 或 `false`。不同类型的值被认为是不同的。如果类型相同，则根据它们的值进行比较。Lua 通过引用比较表、用户数据和函数。只有当两个这样的值引用同一个对象时，才认为它们是相等的。

  ```lua
  a = 5
  b = 6

  if a <= b then
      print("a is less than or equal to b")
  end

  print("A" < "a") --> true
  print("aa" < "ab") --> true
  print(10 == "10") --> false
  print(tostring(10) == "10") --> true
  ```

逻辑运算符
: `and`，`or` 和 `not`。如果第一个参数是 `false`，`and` 返回第一个参数，否则返回第二个参数。如果第一个参数不是 `false`，`or` 返回第一个参数，否则返回第二个参数。

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

连接
: 字符串可以用 `..` 运算符连接。连接时数字会转换为字符串。

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

长度
: 一元长度运算符 `#`。字符串的长度是其字节数。表的长度是其序列长度，即从 `1` 开始编号且值不为 `nil` 的索引数量。注意：如果序列中有 `nil` 值的"空洞"，长度可以是 `nil` 值之前的任何索引。

  ```lua
  s = "donkey"
  print(#s) --> 6

  t = { "a", "b", "c", "d" }
  print(#t) --> 4

  u = { a = 1, b = 2, c = 3 }
  print(#u) --> 0

  v = { "a", "b", nil }
  print(#v) --> 2
  ```

## 流程控制

Lua 提供了一组常规的流程控制结构。

if---then---else
: 测试条件，如果条件为真则执行 `then` 部分，否则执行（可选的）`else` 部分。您可以使用 `elseif` 来代替嵌套的 `if` 语句。这取代了 Lua 中没有的 switch 语句。

  ```lua
  a = 5
  b = 4

  if a < b then
      print("a is smaller than b")
  end

  if a == '1' then
      print("a is 1")
  elseif a == '2' then
      print("a is 2")
  elseif a == '3' then
      print("a is 3")
  else
      print("I have no idea what a is...")
  end
  ```

while
: 测试条件并只要条件为真就执行代码块。

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- 输出每一天
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: 重复执行代码块直到条件为真。条件在主体之后测试，因此它至少会执行一次。

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- 输出每一天
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: Lua 有两种类型的 `for` 循环：数值型和通用型。数值型 `for` 接受 2 或 3 个数值，而通用型 `for` 迭代由 _迭代器_ 函数返回的所有值。

  ```lua
  -- 输出数字 1 到 10
  for i = 1, 10 do
      print(i)
  end

  -- 输出数字 1 到 10 而且每次步进 2 个值
  for i = 1, 10, 2 do
      print(i)
  end

  -- 输出数字 10 到 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- 迭代序列输出内容
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break 和 return
: 使用 `break` 语句从 `for`、`while` 或 `repeat` 循环的内部块中跳出。使用 `return` 从函数返回值或结束函数的执行并返回到调用者。`break` 或 `return` 只能作为块的最后一个语句出现。

  ```lua
  a = 1
  while true do
      a = a + 1
      if a >= 100 then
          break
      end
  end

  function my_add(a, b)
      return a + b
  end

  print(my_add(10, 12)) --> 22
  ```

## 局部变量、全局变量和词法作用域

您声明的所有变量默认都是全局的，意味着它们在 Lua 运行时上下文的所有部分都可用。您可以明确地将变量声明为 `local`，这意味着该变量将仅存在于当前作用域内。

每个 Lua 源文件定义一个单独的作用域。在文件最顶层声明的局部变量意味着该变量对于 Lua 脚本文件是局部的。每个函数创建另一个嵌套作用域，每个控制结构块创建额外的作用域。您可以使用 `do` 和 `end` 关键字明确创建作用域。Lua 是词法作用域的，意味着作用域可以完全访问来自封闭作用域的 _局部_ 变量。请注意，局部变量必须在使用前声明。

```lua
function my_func(a, b)
    -- 'a' 和 'b' 是函数本地变量并在函数范围内有效

    do
        local x = 1
    end

    print(x) --> nil. 'x' 在 do-end 范围之外无效
    print(foo) --> nil. 'foo' 的定义在 'my_func' 之后
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' 经过定义就变成文件范围本地有效了.
```

请注意，如果您在脚本文件中将函数声明为 `local`（这通常是个好主意），您需要注意代码的排序。如果您有相互调用的函数，可以使用前向声明。

```lua
local func2 -- 提前声明 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- or func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

如果您在另一个函数中编写一个函数，它也可以完全访问来自封闭函数的局部变量。这是一个非常强大的结构。

```lua
function create_counter(x)
    -- 'x' is a local variable in 'create_counter'
    return function()
        x = x + 1
        return x
    end
end

count1 = create_counter(10)
count2 = create_counter(20)
print(count1()) --> 11
print(count2()) --> 21
print(count1()) --> 12
```

## 变量遮蔽

在块中声明的局部变量将遮蔽周围块中具有相同名称的变量。

```lua
my_global = "global"
print(my_global) -->"global"

local v = "local"
print(v) --> "local"

local function test(v)
    print(v)
end

function init(self)
    v = "apple"
    print(v) --> "apple"
    test("banana") --> "banana"
end
```

## 协程

函数从头到尾执行，没有办法在中途停止它们。协程允许您这样做，这在某些情况下可能非常方便。假设我们想要创建一个非常特定的逐帧动画，我们将游戏对象从 y 位置 `0` 移动到从第 1 帧到第 5 帧的非常特定的 y 位置。我们可以用 `update()` 函数（见下文）中的计数器和位置列表来解决这个问题。然而，使用协程，我们得到一个非常干净的实现，易于扩展和使用。所有状态都包含在协程本身中。

当协程让出时，它将控制权返回给调用者，但会记住其执行点，以便以后可以继续执行。

```lua
-- 这就是协程
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- 返回最后一个值
end

function init(self)
    self.co = coroutine.create(sequence) -- 创建协程. 'self.co' 是线程对象
    go.set_position(vmath.vector3(100, 0, 0)) -- 设置初始位置
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- 继续运行协程.
    if status then
        -- 如果协程还没运行完, 则使用协程返回的位置值
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Defold 中的 Lua 上下文

您声明的所有变量默认都是全局的，意味着它们在 Lua 运行时上下文的所有部分都可用。Defold 在 *game.project* 中有一个 *shared_state* 设置来控制此上下文。如果设置了该选项，所有脚本、GUI 脚本和渲染脚本都在同一个 Lua 上下文中评估，全局变量在任何地方都可见。如果未设置该选项，引擎会在单独的上下文中执行脚本、GUI 脚本和渲染脚本。

![上下文](images/lua/lua_contexts.png)

Defold 允许您在几个单独的游戏对象组件中使用相同的脚本文件。任何本地声明的变量都在使用相同脚本文件的组件之间共享。

```lua
-- 'my_global_value' 可以被所有脚本, gui 脚本, 渲染脚本以及模块 (Lua 文件) 访问
my_global_value = "global scope"

-- 此变量可以被所有使用本脚本文件的组件访问
local script_value = "script scope"

function init(self, dt)
    -- 这个变量只在本组件中可以访问
    self.foo = "self scope"

    -- 这个变量只在init函数里而且必须在声明之后才可以访问
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- 在 init() 之外此变量不可访问
end
```



## 性能考虑

在以流畅的 60 FPS 运行的高性能游戏中，小的性能错误可能会对体验产生很大影响。有一些简单的通用事项需要考虑，还有一些可能看起来不太有问题的事项。

从简单的事情开始。编写不包含不必要循环的直截了当的代码通常是一个好主意。有时您确实需要遍历事物列表，但如果事物列表足够大，请小心。这个示例在一台相当不错的笔记本电脑上运行时间略超过 1 毫秒，如果每帧只有 16 毫秒（在 60 FPS 下），并且引擎、渲染脚本、物理模拟等消耗了其中的一部分，这可能会产生很大的影响。

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

使用 `socket.gettime()` 返回的值（自系统纪元以来的秒数）来基准测试可疑代码。

## 内存和垃圾回收

Lua 的垃圾回收默认在后台自动运行，并回收 Lua 运行时分配的内存。收集大量垃圾可能是一项耗时的任务，因此最好减少需要垃圾回收的对象数量：

* 局部变量本身是免费的，不会产生垃圾。（即 `local v = 42`）
* 每个 _新的唯一_ 字符串都会创建一个新对象。编写 `local s = "some_string"` 将创建一个新对象并将 `s` 分配给它。局部变量 `s` 本身不会产生垃圾，但字符串对象会。多次使用相同的字符串不会增加额外的内存成本。
* 每次执行表构造函数（`{ ... }`）时都会创建一个新表。
* 执行 _函数语句_ 会创建一个闭包对象。（即执行语句 `function () ... end`，而不是调用已定义的函数）
* 可变参数函数（`function(v, ...) end`）在每次 _调用_ 函数时都会为省略号创建一个表（在 Lua 5.2 版本之前，或者如果不使用 LuaJIT）。
* `dofile()` 和 `dostring()`
* 用户数据对象

在许多情况下，您可以避免创建新对象，而是重用已有的对象。例如，以下在每个 `update()` 结尾处很常见：

```lua
-- 重置速度
self.velocity = vmath.vector3()
```

很容易忘记每次调用 `vmath.vector3()` 都会创建一个新对象。让我们找出一个 `vector3` 使用多少内存：

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 总共分配了 70 字节
```

在两次调用 `collectgarbage()` 之间增加了 70 字节，但这包括的不仅仅是 `vector3` 对象的分配。每次打印 `collectgarbage()` 的结果都会构建一个字符串，这本身就会增加 22 字节的垃圾：

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 分配了 22 字节
```

所以一个 `vector3` 的重量是 70-22=48 字节。这并不多，但如果您在 60 FPS 的游戏中每帧创建 _一个_，突然间每秒就会产生 2.8 kB 的垃圾。如果有 360 个脚本组件，每个每帧创建一个 `vector3`，我们每秒将看到 1 MB 的垃圾生成。数字可以非常迅速地累加。当 Lua 运行时收集垃圾时，它可能会消耗掉许多宝贵的毫秒——尤其是在移动平台上。

避免分配的一种方法是创建一个 `vector3`，然后继续使用同一个对象。例如，要重置 `vector3`，我们可以使用以下构造：

```lua
-- 而不是执行 self.velocity = vmath.vector3() 创建一个新对象
-- 我们将现有的速度矢量对象的分量清零
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

默认的垃圾收集方案可能对某些时间关键的应用程序不是最优的。如果您在游戏或应用程序中看到卡顿，您可能希望通过 [`collectgarbage()`](/ref/base/#collectgarbage) Lua 函数调整 Lua 收集垃圾的方式。例如，您可以使用较低的 `step` 值每帧运行收集器一小段时间。要了解您的游戏或应用程序消耗了多少内存，您可以使用以下代码打印当前的垃圾字节数：

```lua
print(collectgarbage("count") * 1024)
```

## 最佳实践

一个常见的实现设计考虑是如何为共享行为构建代码结构。有几种可能的方法。

模块中的行为
: 将行为封装在模块中允许您在不同的游戏对象脚本组件（和 GUI 脚本）之间轻松共享代码。在编写模块函数时，通常最好编写严格的函数式代码。在某些情况下，存储状态或副作用是必要的（或导致更清晰的设计）。如果必须在模块中存储内部状态，请注意组件共享 Lua 上下文。有关详细信息，请参阅[模块文档](/manuals/modules)。

  ![Module](images/lua/lua_module.png)

  此外，即使可以让模块代码直接修改游戏对象的内部（通过将 `self` 传递给模块函数），我们也强烈不鼓励您这样做，因为您会创建非常紧密的耦合。

带有封装行为的辅助游戏对象
: 就像您可以将脚本代码包含在 Lua 模块中一样，您也可以将其包含在带有脚本组件的游戏对象中。不同之处在于，如果将其包含在游戏对象中，您只能严格通过消息传递与其通信。

  ![Helper](images/lua/lua_helper.png)

在集合内将游戏对象与辅助行为对象分组
: 在此设计中，您可以创建一个自动作用于另一个目标游戏对象的行为游戏对象，要么通过预定义的名称（用户必须重命名目标游戏对象以匹配），要么通过指向目标游戏对象的 `go.property()` URL。

  ![Collection](images/lua/lua_collection.png)

  这种设置的好处是您可以将行为游戏对象拖放到包含目标对象的集合中。不需要额外的代码。

  在需要管理大量游戏对象的情况下，这种设计不是可取的，因为行为对象会为每个实例重复，每个对象都会消耗内存。
