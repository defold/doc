---
title: Defold 中的寻址
brief: 本手册解释了 Defold 如何解决寻址问题.
---

# 寻址

控制运行游戏的代码必须能够访问每个对象和组件，以便移动、缩放、制作动画、删除和操作玩家看到和听到的内容。Defold的寻址机制使这成为可能。

## 标识符

Defold使用地址（或URL，但我们暂时忽略这一点）来引用游戏对象和组件。这些地址由标识符组成。以下是Defold如何使用地址的所有示例。在本手册中，我们将详细研究它们的工作原理：

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

先看一个简单的例子. 比如你有一个含有Sprite的游戏对象. 然后附加一个脚本来控制这个对象. 在编辑器里的设置就差不多这样:

![bean in editor](images/addressing/bean_editor.png)

你想开始先关闭这个sprite, 留待以后显示. 我们来简单创建一个脚本 "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
<1> 如果你对'#'字符感到困惑，不用担心，我们很快会讲到它。

这将按预期工作。当游戏启动时，脚本组件通过其标识符"body"*寻址*到精灵组件，并使用该地址向其发送一条带有"disable"的*消息*。这个特殊引擎消息的效果是精灵组件隐藏精灵图形。从示意图上看，设置如下：

![bean](images/addressing/bean.png)

设置中的标识符是任意的。在这里，我们选择给游戏对象命名为"bean"，其精灵组件命名为"body"，而控制角色的脚本组件命名为"controller"。

::: sidenote
如果你不选择名称，编辑器会为你选择。每当你在编辑器中创建新的游戏对象或组件时，会自动设置一个唯一的*Id*属性。

- 游戏对象自动获得一个名为"go"的id，后面跟着枚举器（"go2"、"go3"等）。
- 组件获得一个对应于组件类型的id（"sprite"、"sprite2"等）。

自动命名虽然能用，但是我们鼓励你自己将命名设计的更好，更有意义。
:::

现在, 再增加一个sprite来给豆子先生添加一个盾牌:

![bean](images/addressing/bean_shield_editor.png)

每个游戏对象的组件id必须唯一. 再叫 "body" 的话脚本就不知道该给谁发送 "disable" 信息了. 所以我们选择了 (更具意义的) id "shield". 这样不管是 "body" 还是 "shield" 我们都能自由控制了.

![bean](images/addressing/bean_shield.png)

::: sidenote
如果你非要设置成一样的id, 系统会提示错误阻止你这样做:

![bean](images/addressing/name_collision.png)
:::

现在再多加一些游戏对象进来试试. 假设你要让两个 "豆子先生" 组个队. 一个叫 "bean" 另一个叫 "buddy". 然后, 当 "bean" 等待一段时间后, 它就让 "buddy" 开始跳舞. 也就是从 "bean" 的脚本组件 "controller" 发送一个自定义消息 "dance" 到 "buddy" 的 "controller" :

![bean](images/addressing/bean_buddy.png)

::: sidenote
这两个脚本组件都叫 "controller", 但是由于唯一性是对每个游戏对象来说的, 所以这样做是可以的.
:::

这次的消息是发给本游戏对象 ("bean") 之外的地方, 代码需要知道哪个 "controller" 来接收这个消息. 既需要对象id也需要组件id. 完整的地址是 `"buddy#controller"` 它包含两个方面内容.

- 首先需要指定目标对象的id ("buddy"),
- 然后是对象/组件分隔符 ("#"),
- 最后是组件的id ("controller").

回过头来看上个例子我们没有指定对象的id, 系统默认对象就是脚本所在的 *当前游戏对象*.

在上述示例中，脚本组件使用相对地址"#body"来寻址精灵组件。该地址是相对的，因为它是从脚本组件所在位置开始解析的。地址中的"#"字符表示"当前游戏对象中的组件"。因此，整个地址"#body"应解释为"当前游戏对象中标识符为'body'的组件"。

## 集合

集合可以用来创建一组游戏对象, 或者嵌套游戏对象然后在需要的时候使用它们. 当你在编辑器里做实例化操作时集合文件就可作为模板 (有的叫 "prototypes" 有的叫 "prefabs").

比如你想建立许多 bean/buddy 二人组. 最好把它们做成 *集合文件* (命名为 "team.collection"). 编译并保存好. 然后在引导启动集合里就可以实例化并命名 (比如 "team_1"):

![bean](images/addressing/team_editor.png)

这种结构下, "bean" 游戏对象依旧可以使用地址 `"buddy#controller"` 来引用"buddy"的"controller"组件.

![bean](images/addressing/collection_team.png)

如果你再实例化一个 "team.collection" (命名 "team_2"), 那么 "team_2" 的脚本也能顺利运行. "team_2"中的"bean" 对象同样使用地址 `"buddy#controller"` 来引用"buddy"的"controller"组件.

![bean](images/addressing/teams_editor.png)

## 相对地址

地址 `"buddy#controller"` 在两组实例下都能运行因为它是一个 *相对* 地址. 集合 "team_1" 和 "team_2" 都有自己的上下文, 或者叫做 "命名空间". Defold 认为集合内这样的相对地址与命名是合理的:

![relative id](images/addressing/relative_same.png)

- "team_1"的命名空间里 "bean" 和 "buddy" 都是唯一id.
- 同样在"team_2"的命名空间里 "bean" 和 "buddy" 也都是唯一id.

实际上相对地址在后台已经把上下文考虑在内. 这同样很方便因为你可以用同样的代码创建很多个集合的实例.

### 简化符

Defold 提供两种简化写法用来简化消息传递时需要输入的完整地址:

:[Shorthands](../shared/url-shorthands.md)

## 游戏对象路径

为了正确理解命名机制, 我们来看看游戏编译运行时发生了什么:

1. 编辑器读取引导启动集合 ("main.collection") 与其所有内容 (游戏对象和其他集合).
2. 对于每个静态的游戏对象, 编译器分配唯一id. 游戏对象 "路径" 从引导启动集合根节点起, 到嵌套关系里找到这个对象为止. 每个 '/' 符号代表嵌套的每一层.

如上示例, 游戏里就有四个游戏对象路径:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
游戏里的各种id存储为哈希值. 包括集合里的相对路径也哈希成绝对路径.
:::

运行时, 不存在集合的概念. 编译前, 对象是不属于集合的. 也无法对集合本身施加操作. 有必要的话, 需要用代码维护集合里的对象. 每个对象id都是静态的, 并且在它们的生命周期中都保持不变. 所以保存一个对象的id后总可以使用此id引用它.

## 绝对地址

定位的时候完全可以使用上述完整的标记. 多数情况下相对地址有助于代码重用, 但是有些情况下还得使用绝对地址定位.

比如, 你需要一个 AI 管理器管理每个豆子先生. 豆子先生要向管理器报告自身的激活状态, 管理器根据它们的状态决定它们的排序. 这就需要创建一个带脚本的管理器对象然后把它放在引导启动集合的根目录下.

![manager object](images/addressing/manager_editor.png)

然后每个豆子先生负责向管理器发送状态消息: "contact" 表明碰到了敌人, 或者 "ouch!" 表明受到了袭击. 为了这项工作, 豆子控制器脚本使用相对地址向 "manager" 里的 "controller" 组件发送消息.

绝对地址是从游戏世界的根（即"集合"）开始解析的。绝对地址以"/"字符开头，表示"从根开始"。

控制器脚本的绝对地址是`"/manager#controller"` 而且不管组件用在哪里该绝对地址总能定位到该组件.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## 哈希ID

Defold引擎将每个标识符转换为64位哈希值，用于内部寻址。这比使用字符串更节省内存和CPU。然而，有时你需要手动计算哈希值，例如在将游戏状态保存到文件时。所有以组件或游戏对象为参数的方法可以接受字符串, 哈希或者 URL 对象. 我们已经在上面看到如何使用字符串进行定位了.

当你获取游戏对象的 id , 引擎总是返回一个绝对路径 id 的哈希值:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

你可以用该标记代替字符串 id, 或者自己写一个. 注意虽然哈希化 id 对应了对象的路径, 比如绝对地址:

::: sidenote
相对地址必须作为字符串使用因为引擎会基于当前命名上下文(集合)的哈希状态, 把字符串添加到哈希后面, 计算出新的哈希id.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- 这样无法工作! 相对地址必须使用字符串.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL格式

Defold中的URL遵循以下格式：

```
[socket:][path][#fragment]
```

其中：
- `socket` - 用于网络通信（可选）
- `path` - 游戏对象和集合的路径
- `fragment` - 组件的标识符（以"#"开头）

URL是一个对象，通常用特定格式的字符串表示。一般一个URL包含三个部分：

socket
: 代表目标的游戏世界. 使用 [集合代理](/manuals/collection-proxy) 时, 它用来表示 _动态加载的集合_.

path
: 该部分包含目标游戏对象的完整 id.

fragment
: 标志了指定游戏对象内的目标组件.

上面已经看到, 你可以省略一些, 或者大多数情况下省略许多部分. 几乎可以不用到 socket, 经常, 不是所有情况下, 需要指定路径. 需要定位其他游戏世界里的东西的情况下需要指定 URL 的 socket 部分. 例如,  上述 "manager" 游戏对象里的 "controller" 脚本的完整 URL 字符串为:

`"main:/manager#controller"`

然后 team_2 里的 buddy 控制器为:

`"main:/team_2/buddy#controller"`

我们可以向它们发送消息:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## 构建 URL 对象

URL 对象也可以使用 Lua 代码构建:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")

```

### URL示例

| URL | 描述 |
|-----|------|
| `"#"` | 当前游戏对象 |
| `"#body"` | 当前游戏对象中标识符为"body"的组件 |
| `"/level1/main/bean#body"` | "level1"集合中"main"集合里"bean"游戏对象的"body"组件 |
| `"main:/bean#body"` | 在"main"socket中，"bean"游戏对象的"body"组件 |

### URL对象

你可以使用`msg.url()`函数创建URL对象：

```lua
local my_url = msg.url("#body")
```

这将返回一个URL对象，可以用于寻址或存储。URL对象也可以从字符串、哈希值或其他URL对象构造：

```lua
local my_url1 = msg.url("#body") -- 从字符串构造
local my_url2 = msg.url(my_url1) -- 从另一个URL对象构造
local my_url3 = msg.url(nil, "/level1/main/bean", hash("body")) -- 从路径和哈希值构造
```

### 发送消息

你可以使用`msg.post()`函数向URL发送消息：

```lua
msg.post("#body", "disable")
```

这将向当前游戏对象中标识符为"body"的组件发送一条"disable"消息。你也可以使用URL对象：

```lua
local my_url = msg.url("#body")
msg.post(my_url, "disable")
```

### URL字符串

你可以使用`tostring()`函数将URL对象转换为字符串：

```lua
local my_url = msg.url("#body")
print(tostring(my_url)) -- 输出: "#body"
```

### URL哈希

你可以使用`msg.url()`函数将URL对象转换为哈希值：

```lua
local my_url = msg.url("#body")
print(my_url) -- 输出: 哈希值
```

### URL比较

你可以使用`==`运算符比较两个URL对象：

```lua
local my_url1 = msg.url("#body")
local my_url2 = msg.url("#body")
if my_url1 == my_url2 then
    print("URLs are equal")
end
```
