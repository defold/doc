---
title: Defold 定位
brief: 本教程解释了 Defold 如何实现地址定位功能.
---

# 定位

为了让代码能够控制每个对象和组件的移动, 缩放, 播放动画或者添加删除各种视听元素, Defold 提供了地址定位机制.

## 标志

Defold 使用地址 (称为 URL, 暂且不表) 来引用游戏对象和组件. 地址里包含各种标志. 下面列举了 Defold 使用地址的例子. 本教程将详述地址的用法:

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
1. 不知道 '#' 是什么意思没关系, 一会儿就谈到.

就像设计的那样, 游戏一开始脚本组件 *定位* 到了sprite组件 "body" 对其地址发出了一个  "disable" 的 *消息* . 这个消息的结果就是把sprite隐藏了. 也就是说, 整个流程是这样的:

![bean](images/addressing/bean.png)

id可以随意设置. 当前我们对游戏对象设置了一个id "bean", sprite组件叫做 "body", 控制这个对象的脚本组件叫做 "controller".

::: 注意
如果你不手动命名, 编辑器会自动设置一个命名. 每当新建一个游戏对象或组件, 系统会将唯一 *Id* 赋值给它.

- 游戏对象就是go后面跟一个数字 ("go2", "go3" 以此类推).
- 组件就是组件名后面跟一个数字 ("sprite", "sprite2" 以此类推).

自动命名虽然能用, 但是我们鼓励你自己将命名设计的更好, 更有意义.
:::

现在, 再增加一个sprite来给豆子先生添加一个盾牌:

![bean](images/addressing/bean_shield_editor.png)

每个游戏对象的组件id必须唯一. 再叫 "body" 的话脚本就不知道该给谁发送 "disable" 信息了. 所以我们选择了 (更具意义的) id "shield". 这样不管是 "body" 还是 "shield" 我们都能自由控制了.

![bean](images/addressing/bean_shield.png)

::: 注意
如果你非要设置成一样的id, 系统会提示错误阻止你这样做:

![bean](images/addressing/name_collision.png)
:::

现在再多加一些游戏对象进来试试. 假设你要让两个 "豆子先生" 组个队. 一个叫 "bean" 另一个叫 "buddy". 然后, 当 "bean" 等待一段时间后, 它就让 "buddy" 开始跳舞. 也就是从 "bean" 的脚本组件 "controller" 发送一个自定义消息 "dance" 到 "buddy" 的 "controller" :

![bean](images/addressing/bean_buddy.png)

::: 注意
这两个脚本组件都叫 "controller", 但是由于唯一性是对每个游戏对象来说的, 所以这样做是可以的.
:::

这次的消息是发给本游戏对象 ("bean") 之外的地方, 代码需要知道哪个 "controller" 来接收这个消息. 既需要对象id也需要组件id. 完整的地址是 `"buddy#controller"` 它包含两个方面内容.

- 首先需要指定目标对象的id ("buddy"),
- 然后是对象/组件分隔符 ("#"),
- 组后是组件的id ("controller").

回过头来看上个例子我们没有指定对象的id, 系统默认对象就是脚本所在的 *当前游戏对象*.

比如, `"#body"` 就是在当前游戏对象里找 "body" 组件. 这就很方便因为脚本可以在 *任何* 游戏对象上运行, 只要它有 "body" 组件.

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

简化符
: Defold 支持如下相对地址简化符:

  `.`
  : 代表本游戏对象.

  `#`
  : 代表本组件.

  举例:

  ```lua
   -- Let this game object acquire input focus
   msg.post(".", "acquire_input_focus")
  ```

  ```lua
   -- Post "reset" to the current script
   msg.post("#", "reset")
  ```

## 游戏对象路径

为了正确理解命名机制, 我们来看看游戏编译运行时发生了什么:

1. 编辑器读取引导启动集合 ("main.collection") 与其所有内容 (游戏对象和其他集合).
2. 对于每个静态的游戏对象, 编译器分配唯一id. 游戏对象 "路径" 从引导启动集合根节点起, 到嵌套关系里找到这个对象为止. 每个 '/' 符号代表嵌套的每一层.

如上示例, 游戏里就有四个游戏对象路径:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: 注意
游戏里的各种id存储为哈希值. 包括集合里的相对路径也哈希成绝对路径.
:::

运行时, 不存在集合的概念. 编译前, 对象是不属于集合的. 也无法对集合本身施加操作. 有必要的话, 需要用代码维护集合里的对象. 每个对象id都是静态的, 并且在它们的生命周期中都保持不变. 所以保存一个对象的id后总可以使用此id引用它.

## 绝对地址

定位的时候完全可以使用绝对地址. 多数情况下相对地址有助于代码重用, 但是有些情况下还得使用绝对地址定位.

比如, 你需要一个 AI 管理器管理每个豆子先生. 豆子先生要向管理器报告自身的激活状态, 管理器根据它们的状态决定它们的排序. 这就需要创建一个带脚本的管理器对象然后把它放在引导启动集合的根目录下.

![manager object](images/addressing/manager_editor.png)

Each bean is then responsible for sending status messages to the manager: "contact" if it spots an enemy or "ouch!" if it is hit and takes damage. For this to work, the bean controller scrips use absolute addressing to send messages to the component "controller" in "manager".

Any address that starts with a '/' will be resolved from the root of the game world. This corresponds to the root of the *bootstrap collection* that is loaded on game start.

The absolute address of the manager script is `"/manager#controller"` and this absolute address will resolve to the right component no matter where it is used.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Hashed identifiers

The engine stores all identifiers as hashed values. All functions that take as argument a component or a game object accepts a string, hash or an URL object. We have seen how to use strings for addressing above.

When you get the identifier of a game object, the engine will always return an absolute path identifier that is hashed:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

You can use such an identifier in place of a string id, or construct one yourself. Note though that a hashed id corresponds to the path to the object, i.e. an absolute address:

::: sidenote
The reason relative addresses must be given as strings is because the engine will compute a new hash id based on the hash state of the current naming context (collection) with the given string added to the hash.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URLs

To complete the picture, let's look at the full format of Defold addresses: the URL.

An URL is an object, usually written as specially formatted strings. A generic URL consists of three parts:

`[socket:][path][#fragment]`

socket
: Identifies the game world of the target. This is important when working with [Collection Proxies](/manuals/collection-proxy) and is then used to identify the _dynamically loaded collection_.

path
: This part of the URL contains the full id of the target game object.

fragment
: The identity of the target component within the specified game object.

As we have seen above, you can leave out some, or most of this information in the majority of cases. You almost never need to specify the socket, and you often, but not always, have to specify the path. In those cases when you do need to address things in another game world then you need to specify the socket part of the URL. For instance, the full URL string for the "controller" script in the "manager" game object above is:

`"main:/manager#controller"`

and the buddy controller in team_2 is:

`"main:/team_2/buddy#controller"`

We can send messages to them:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Constructing URL objects

URL objects can also be constructed programmatically in Lua code:

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
