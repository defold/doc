---
title: 集合工厂手册
brief: 本手册解释了如何使用集合工厂组件来生成游戏对象的层级结构.
---

# 集合工厂

集合工厂组件用于将存储在集合文件中的游戏对象组和层级结构生成到运行中的游戏中。

集合提供了一种强大的机制来创建可重用的模板，或称为Defold中的"预制件"。有关集合的概述，请参阅[构建块文档](/manuals/building-blocks#collections)。集合可以放置在编辑器中，也可以动态插入到您的游戏中。

使用集合工厂组件，您可以将集合文件的内容生成到游戏世界中。这类似于对集合内的所有游戏对象执行工厂生成，然后在对象之间构建父子层级关系。一个典型的用例是生成由多个游戏对象组成的敌人（例如，敌人+武器）。

## 生成集合

假设我们想要一个角色游戏对象和一个单独的盾牌游戏对象作为角色的子对象。我们在一个集合文件中构建游戏对象层级结构，并将其保存为"bean.collection"。

::: sidenote
*集合代理*组件用于基于集合创建新的游戏世界，包括单独的物理世界。新世界通过新的套接字访问。当您向代理发送消息开始加载时，集合中包含的所有资产都通过代理加载。这使得它们对于例如在游戏中切换关卡非常有用。然而，新的游戏世界带来了相当多的开销，因此不要将它们用于少量内容的动态加载。有关更多信息，请参阅[集合代理文档](/manuals/collection-proxy)。
:::

![Collection to spawn](images/collection_factory/collection.png)

然后，我们将*集合工厂*添加到一个游戏对象中，该游戏对象将负责生成，并将"bean.collection"设置为组件的*原型*：

![Collection factory](images/collection_factory/factory.png)

现在，生成bean和shield只需要调用`collectionfactory.create()`函数：

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

该函数接受5个参数：

`url`
: 应该生成新游戏对象组的集合工厂组件的id。

`[position]`
: （可选）生成的游戏对象的世界位置。这应该是一个`vector3`。如果您不指定位置，对象将在集合工厂组件的位置生成。

`[rotation]`
: （可选）新游戏对象的世界旋转。这应该是一个`quat`。

`[properties]`
: （可选）一个带有`id`-`table`对的Lua表，用于初始化生成的游戏对象。有关如何构造此表的信息，请参见下文。

`[scale]`
: （可选）生成的游戏对象的缩放比例。缩放可以表示为一个`number`（大于0），它指定所有轴上的均匀缩放。您也可以提供一个`vector3`，其中每个组件指定相应轴上的缩放。

`collectionfactory.create()`将生成的游戏对象的标识作为表返回。表键将每个对象的集合本地id的哈希映射到每个对象的运行时id：

::: sidenote
"bean"和"shield"之间的父子关系*不会*在返回的表中反映出来。这种关系仅存在于运行时场景图中，即对象如何一起变换。重新设置对象的父级永远不会改变其id。
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. 添加了前缀`/collection[N]/`，其中`[N]`是一个计数器，以唯一标识每个实例：

## 属性

生成集合时，您可以通过构造一个表来将属性参数传递给每个游戏对象，其中键是对象id，值是包含要设置的脚本属性的表。

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

假设"bean.collection"中的"bean"游戏对象定义了"shield"属性。[脚本属性手册](/manuals/script-properties)包含有关脚本属性的信息。

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## 工厂资源的动态加载

通过选中集合工厂属性中的*动态加载*复选框，引擎会推迟与工厂关联的资源的加载。

![Load dynamically](images/collection_factory/load_dynamically.png)

取消选中该复选框时，引擎在加载集合工厂组件时加载原型资源，因此它们立即可用于生成。

选中该复选框时，您有两种使用选项：

同步加载
: 当您想要生成对象时调用[`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale])。这将同步加载资源，这可能会导致卡顿，然后生成新实例。

  ```lua
  function init(self)
      -- 集合工厂父级集合加载时
      -- 集合工厂资源不会被加载. 调用 create 函数
      -- 会把资源进行同步加载.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- 删掉游戏对象, 资源引用计数减少
      -- 本例中集合工厂资源也会被卸载
      -- 因为集合工厂组件不包含对资源的引用.
      go.delete(self.go_ids)

      -- 因为集合工厂组件不包含对资源的引用
      -- 所以对集合工厂调用 unload 没有意义
      collectionfactory.unload("#factory")
  end
  ```

异步加载
: 调用[`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function])以异步方式显式加载资源。当资源准备好生成时，会收到一个回调。

  ```lua
  function load_complete(self, url, result)
      -- 资源加载完成, 可以新建对象
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- 集合工厂父级集合加载时
      -- 集合工厂资源不被加载. 调用 load 函数进行资源异步加载.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- 删掉游戏对象, 资源引用计数减少
      -- 本例中集合工厂资源不会被卸载
      -- 因为集合工厂组件包含对资源的引用.
      go.delete(self.go_ids)

      -- 调用 unload 函数, 集合工厂对资源引用被释放,
      -- 这样资源才会被卸载.
      collectionfactory.unload("#factory")
  end
  ```


## 动态原型

可以通过选中集合工厂属性中的*动态原型*复选框来更改集合工厂可以创建的*原型*。

![Dynamic prototype](images/collection_factory/dynamic_prototype.png)

当*动态原型*选项被选中时，集合工厂组件可以使用`collectionfactory.set_prototype()`函数更改原型。示例：

```lua
collectionfactory.unload("#factory") -- 卸载之前的资源
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
当设置*动态原型*选项时，集合组件计数无法优化，拥有集合将使用*game.project*文件中的默认组件计数。
:::

