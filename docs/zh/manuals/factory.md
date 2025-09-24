---
title: Factory 组件手册
brief: 本手册解释了如何使用工厂组件在运行时动态生成游戏对象.
---

# Factory 组件

Factory 组件用于在游戏运行时从对象池中动态生成游戏对象。

当您将 Factory 组件添加到游戏对象时，您可以在 *Prototype* 属性中指定工厂应使用哪个游戏对象文件作为原型（在其他引擎中也称为"预制件"或"蓝图"）来创建所有新的游戏对象。

![Factory component](images/factory/factory_collection.png)

![Factory component](images/factory/factory_component.png)

要创建游戏对象, 调用 `factory.create()`:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Spawned game object](images/factory/factory_spawned.png)

`factory.create()` 接受5个参数：

`url`
: 应生成新游戏对象的工厂组件的 ID。

`[position]`
: （可选）新游戏对象的世界位置。这应该是一个 `vector3`。如果您不指定位置，游戏对象将在工厂组件的位置生成。

`[rotation]`
: （可选）新游戏对象的世界旋转。这应该是一个 `quat`。

`[properties]`
: （可选）一个 Lua 表，包含任何用于初始化游戏对象的脚本属性值。有关脚本属性的信息，请参阅[脚本属性手册](/manuals/script-properties)。

`[scale]`
: （可选）生成的游戏对象的缩放比例。缩放可以表示为一个 `number`（大于0），指定所有轴上的均匀缩放。您也可以提供一个 `vector3`，其中每个组件指定沿相应轴的缩放。

例如：

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- 以无旋转但双倍缩放生成。
-- 将星星的分数设置为10。
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. 设置星星游戏对象的"score"属性。

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. "score"脚本属性定义为默认值。
2. 将"score"脚本属性引用为存储在"self"中的值。

![Spawned game object with property and scaling](images/factory/factory_spawned2.png)

::: important
Defold 目前不支持碰撞形状的非均匀缩放。如果您提供非均匀缩放值，例如 `vmath.vector3(1.0, 2.0, 1.0)`，精灵将正确缩放，但碰撞形状不会。
:::


## Factory 创建对象的寻址

Defold 的寻址机制使得可以访问运行中游戏中的每个对象和组件。[寻址手册](/manuals/addressing/)详细介绍了系统的工作原理。可以对生成的游戏对象及其组件使用相同的寻址机制。通常，使用生成对象的 ID 就足够了，例如在发送消息时：

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: important
向游戏对象本身而不是特定组件传递消息实际上会将消息发送到所有组件。这通常不是问题，但如果对象有很多组件，最好记住这一点。
:::

但是，如果您需要访问生成的游戏对象上的特定组件，例如禁用碰撞对象或更改精灵图像，该怎么办？解决方案是从游戏对象 ID 和组件 ID 构造一个 URL。

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```

## 跟踪生成的对象和父对象

当您调用 `factory.create()` 时，您会获得新游戏对象的 ID，允许您存储该 ID 以供将来参考。一个常见的用法是生成对象并将其 ID 添加到表中，以便以后可以一次性删除它们，例如在重置关卡布局时：

```lua
-- spawner.script
self.spawned_coins = {}

...

-- 生成一个硬币并将其存储在"coins"表中。
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

然后稍后：

```lua
-- spawner.script
-- 删除所有生成的硬币。
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- 或者替代方案
go.delete(self.spawned_coins)
```

另一种常见情况是，您希望生成的对象知道生成它的游戏对象。一个例子是某种只能一次生成一个的自主对象。然后，生成的对象需要在其被删除或停用时通知生成器，以便可以生成另一个：

```lua
-- spawner.script
-- 生成一个无人机并将其父级设置为此脚本组件的 URL
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

生成对象的逻辑：

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- 我死了。
    msg.post(self.parent, "drone_dead")
end
```

## Factory 资源的动态加载

通过勾选工厂属性中的 *Load Dynamically* 复选框，引擎会推迟与工厂关联的资源的加载。

![Load dynamically](images/factory/load_dynamically.png)

如果不勾选该复选框，引擎会在加载工厂组件时加载原型资源，使它们立即可用于生成。

勾选该复选框后，您有两种使用选项：

同步加载
: 当您想要生成对象时调用 [`factory.create()`](/ref/factory/#factory.create)。这将同步加载资源，可能会导致卡顿，然后生成新实例。

  ```lua
  function init(self)
      -- 当工厂的父级集合加载时，
-- 没有工厂资源被加载。在没有调用 load 的情况下调用 create
-- 将同步创建资源。
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- 删除游戏对象。将减少资源引用计数。
-- 在这种情况下，资源被删除，因为工厂组件
-- 不持有引用。
      go.delete(self.go_id)

      -- 调用 unload 不会执行任何操作，因为工厂不持有引用
      factory.unload("#factory")
  end
  ```

异步加载
: 调用 [`factory.load()`](/ref/factory/#factory.load) 显式异步加载资源。当资源准备好生成时，会收到一个回调。

  ```lua
  function load_complete(self, url, result)
      -- 加载完成，资源已准备好生成
      self.go_id = factory.create(url)
  end

  function init(self)
      -- 当工厂的父级集合加载时，
-- 没有工厂资源被加载。调用 load 将加载资源。
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- 删除游戏对象。将减少资源引用计数。
-- 在这种情况下，资源不会被删除，因为工厂组件
-- 仍然持有引用。
      go.delete(self.go_id)

      -- 调用 unload 将减少工厂组件持有的资源引用计数，
-- 导致资源被销毁。
      factory.unload("#factory")
  end
  ```

## 动态原型

通过勾选工厂属性中的 *Dynamic Prototype* 复选框，可以更改工厂可以创建的 *Prototype*。

![Dynamic prototype](images/factory/dynamic_prototype.png)

当 *Dynamic Prototype* 选项被勾选时，工厂组件可以使用 `factory.set_prototype()` 函数更改原型。示例：

```lua
factory.unload("#factory") -- 卸载之前的资源
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
当设置 *Dynamic Prototype* 选项时，无法优化集合组件计数，拥有集合将使用 *game.project* 文件中的默认组件计数。
:::


## 实例限制

项目设置 *Collection related settings* 中的 *max_instances* 限制了世界中可以存在的游戏对象实例总数（启动时加载的 main.collection 或通过集合代理加载的任何世界）。世界中存在的所有游戏对象都计入此限制，无论它们是通过编辑器手动放置的还是通过脚本在运行时生成的。

![Max instances](images/factory/factory_max_instances.png)

如果您将 *max_instances* 设置为 1024 并在主集合中有 24 个手动放置的游戏对象，您可以额外生成 1000 个游戏对象。一旦删除一个游戏对象，您就可以自由生成另一个实例。

## 游戏对象池

将生成的游戏对象保存在池中并重用它们似乎是个好主意。然而，引擎已经在底层进行了对象池化，因此额外的开销只会减慢速度。删除游戏对象并生成新对象既更快又更干净。
