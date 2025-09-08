---
title: Defold 中的消息传递
brief: 消息传递是 Defold 用于允许松耦合对象进行通信的机制。本手册深入描述了这一机制。
---

# 消息传递

消息传递是 Defold 游戏对象之间进行通信的机制。本手册假设您已对 Defold 的[寻址机制](/manuals/addressing)和[基本构建块](/manuals/building-blocks)有基本了解。

Defold 不采用面向对象的方式，即通过设置具有继承和成员函数的类层次结构来定义应用程序（如 Java、C++ 或 C#）。相反，Defold 通过一种简单而强大的面向对象设计扩展了 Lua，其中对象状态保存在脚本组件内部，可通过 `self` 引用访问。此外，对象还可以通过异步消息传递作为对象间的通信方式实现完全解耦合。

## 使用示例

让我们先看几个简单的使用示例。假设您正在构建一个由以下部分组成的游戏：

1. 一个主引导集合，包含一个带有 GUI 组件的游戏对象（GUI 由一个迷你地图和一个分数计数器组成）。还有一个 ID 为 "level" 的集合。
2. 名为 "level" 的集合包含两个游戏对象：一个英雄玩家角色和一个敌人。

![Message passing structure](images/message_passing/message_passing_structure.png)

::: sidenote
本示例的内容存在于两个单独的文件中。一个用于主引导集合，另一个用于 ID 为 "level" 的集合。然而，在 Defold 中，文件名_并不重要_。重要的是您为实例分配的身份标识。
:::

游戏包含一些需要对象间通信的简单机制：

![Message passing](images/message_passing/message_passing.png)

① 英雄攻击敌人
: 作为此机制的一部分，一个 `"punch"` 消息从 "hero" 脚本组件发送到 "enemy" 脚本组件。由于两个对象都位于集合层次结构中的同一位置，因此首选相对寻址：

  ```lua
  -- 从 "hero" 脚本向 "enemy" 脚本发送 "punch" 消息
  msg.post("enemy#controller", "punch")
  ```

  游戏中只有一种强度的攻击动作，因此消息除了其名称 "punch" 外不需要包含任何其他信息。

  在敌人的脚本组件中，您创建一个函数来接收消息：

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  在这种情况下，代码只查看消息的名称（作为哈希字符串在参数 `message_id` 中发送）。代码不关心消息数据或发送者---*任何人*发送 "punch" 消息都会对可怜的敌人造成伤害。

② 英雄获得分数
: 每当玩家击败敌人时，玩家分数会增加。一个 `"update_score"` 消息也从 "hero" 游戏对象的脚本组件发送到 "interface" 游戏对象的 "gui" 组件。

  ```lua
  -- 敌人被击败。分数计数器增加 100。
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  在这种情况下，不可能编写相对地址，因为 "interface" 位于命名层次结构的根部，而 "hero" 不是。消息被发送到附加了脚本的 GUI 组件，因此它可以相应地对消息做出反应。消息可以在脚本、GUI 脚本和渲染脚本之间自由发送。

  消息 `"update_score"` 与分数数据一起发送。数据作为 Lua 表在 `message` 参数中传递：

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- 将分数计数器设置为新分数
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ 迷你地图上的敌人位置
: 玩家在屏幕上有一个迷你地图，帮助定位和跟踪敌人。每个敌人负责通过向 "interface" 游戏对象中的 "gui" 组件发送 `"update_minimap"` 消息来发出其位置信号：

  ```lua
  -- 发送当前位置以更新界面迷你地图
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  GUI 脚本代码需要跟踪每个敌人的位置，如果同一个敌人发送新位置，则应替换旧位置。消息的发送者（在参数 `sender` 中传递）可以用作位置的 Lua 表的键：

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- 更新地图上的位置
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- 将分数计数器设置为新分数
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- 用新位置更新迷你地图
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## 发送消息

如上所述，发送消息的机制非常简单。您调用函数 `msg.post()` 将您的消息发布到消息队列。然后，每帧引擎会遍历队列并将每条消息传递到其目标地址。对于某些系统消息（如 `"enable"`、`"disable"`、`"set_parent"` 等），引擎代码会处理该消息。引擎还会产生一些系统消息（如物理碰撞时的 `"collision_response"`），这些消息会传递到您的对象。对于发送到脚本组件的用户消息，引擎只需调用一个名为 `on_message()` 的特殊 Defold Lua 函数。

您可以向任何现有对象或组件发送任意消息，由接收方代码负责响应该消息。如果您向脚本组件发送消息而脚本代码忽略该消息，那也没关系。处理消息的责任完全在接收方。

引擎会检查消息目标地址。如果您尝试向未知接收者发送消息，Defold 将在控制台中发出错误信号：

```lua
-- 尝试发布到不存在的对象
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

`msg.post()` 调用的完整签名是：

`msg.post(receiver, message_id, [message])`

receiver
: 目标组件或游戏对象的 ID。请注意，如果您以游戏对象为目标，消息将广播到游戏对象中的所有组件。

message_id
: 包含消息名称的字符串或哈希字符串。

[message]
: 包含消息数据键值对的可选 Lua 表。几乎任何类型的数据都可以包含在消息 Lua 表中。您可以传递数字、字符串、布尔值、URL、哈希和嵌套表。您不能传递函数。

  ```lua
  -- 发送包含嵌套表的表数据
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
`message` 参数表的大小有一个硬性限制。此限制设置为 2 千字节。目前没有简单的方法来确定表消耗的确切内存大小，但您可以在插入表之前和之后使用 `collectgarbage("count")` 来监控内存使用情况。
:::

### 简写形式

Defold 提供了两个方便的简写形式，您可以使用它们来发送消息而无需指定完整的 URL：

:[Shorthands](../shared/url-shorthands.md)


## 接收消息

接收消息是确保目标脚本组件包含名为 `on_message()` 的函数的问题。该函数接受四个参数：

`function on_message(self, message_id, message, sender)`

`self`
: 对脚本组件本身的引用。

`message_id`
: 包含消息的名称。该名称是_哈希_的。

`message`
: 包含消息数据。这是一个 Lua 表。如果没有数据，表为空。

`sender`
: 包含发送者的完整 URL。

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## 游戏世界之间的消息传递

如果您使用集合代理将新游戏世界加载到运行时中，您将需要在游戏世界之间传递消息。假设您已通过代理加载了一个集合，并且该集合的*名称*属性设置为 "level"：

![Collection name](images/message_passing/collection_name.png)

一旦集合被加载、初始化并启用，您就可以通过在接收者地址的 "socket" 字段中指定游戏世界名称，向新世界中的任何组件或对象发布消息：

```lua
-- 向新游戏世界中的玩家发送消息
msg.post("level:/player#controller", "wake_up")
```
关于代理如何工作的更深入描述可以在[集合代理](/manuals/collection-proxy)文档中找到。

## 消息链

当已发布的消息最终被分发时，接收者的 `on_message()` 会被调用。响应代码发布新消息是很常见的，这些新消息会被添加到消息队列中。

当引擎开始分发时，它将处理消息队列并调用每个消息接收者的 `on_message()` 函数，直到消息队列为空。如果分发过程向队列添加新消息，它将进行另一轮分发。然而，引擎尝试清空队列的次数有一个硬性限制，这有效地限制了您期望在一帧内完全分发的消息链的长度。您可以使用以下脚本轻松测试引擎在每个 `update()` 之间执行多少次分发传递：

```lua
function init(self)
    -- 我们在对象初始化期间启动一个长消息链
    -- 并通过多个 update() 步骤保持其运行。
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

运行此脚本将打印如下内容：

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

我们看到这个特定的 Defold 引擎版本在 `init()` 和第一次调用 `update()` 之间对消息队列执行 10 次分发传递。然后在每个后续更新循环中执行 75 次传递。

