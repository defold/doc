---
title: Defold的构建块
brief: 本手册深入探讨游戏对象、组件和集合的工作原理细节。
---

#  构建块

Defold设计的核心是几个非常重要的概念，掌握这些概念至关重要。本手册解释了Defold的构建块由什么组成。阅读本手册后，请继续阅读[定位手册](/manuals/addressing)和[消息传递手册](/manuals/message-passing)。编辑器中还提供了一套[教程](/tutorials/getting-started)，可以帮助您快速上手。

![Building blocks](images/building_blocks/building_blocks.png)

您可以使用三种基本类型的构建块来构建Defold游戏：

Collection
: 集合是用于构建游戏结构的文件。在集合中，您可以构建游戏对象和其他集合的层次结构。它们通常用于构建游戏关卡、敌人群体或由多个游戏对象组成的角色。

Game object
: 游戏对象是具有ID、位置、旋转和缩放的容器。它用于容纳组件。它们通常用于创建玩家角色、子弹、游戏规则系统或关卡加载器。

Component
: 组件是放置在游戏对象中的实体，为游戏对象提供视觉、听觉和/或逻辑表示。它们通常用于创建角色精灵、脚本文件、添加音效或添加粒子效果。

## 集合

集合是包含游戏对象和其他集合的树形结构。集合总是存储在文件中。

当Defold引擎启动时，它会加载一个在*game.project*设置文件中指定的_引导集合_。引导集合通常命名为"main.collection"，但您可以自由使用任何您喜欢的名称。

集合可以包含游戏对象和其他集合（通过引用子集合文件），可以任意深度嵌套。下面是一个名为"main.collection"的文件示例。它包含一个游戏对象（ID为"can"）和一个子集合（ID为"bean"）。子集合又包含两个游戏对象："bean"和"shield"。

![Collection](images/building_blocks/collection.png)

请注意，ID为"bean"的子集合存储在自己的文件中，名为"/main/bean.collection"，仅在"main.collection"中被引用：

![Bean collection](images/building_blocks/bean_collection.png)

您无法对集合本身进行寻址，因为没有与"main"和"bean"集合对应的运行时对象。但是，您有时需要使用集合的标识作为游戏对象_路径_的一部分（详细信息请参阅[定位手册](/manuals/addressing)）：

```lua
-- file: can.script
-- 获取"bean"集合中"bean"游戏对象的位置
local pos = go.get_position("bean/bean")
```

集合总是作为对集合文件的引用添加到另一个集合中：

在*Outline*视图中<kbd>右键单击</kbd>集合并选择<kbd>Add Collection File</kbd>。

## 游戏对象

游戏对象是在游戏执行期间各自具有独立生命周期的简单对象。游戏对象具有位置、旋转和缩放，每个属性都可以在运行时进行操作和动画处理。

```lua
-- 为"can"游戏对象的X位置设置动画
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

游戏对象可以空着使用（例如作为位置标记），但通常配备各种组件，如精灵、声音、脚本、模型、工厂等。游戏对象要么在编辑器中创建，放置在集合文件中，要么在运行时通过_factory_组件动态生成。

游戏对象可以直接添加到集合中，或者作为对游戏对象文件的引用添加到集合中：

在*Outline*视图中<kbd>右键单击</kbd>集合并选择<kbd>Add Game Object</kbd>（就地添加）或<kbd>Add Game Object File</kbd>（作为文件引用添加）。


## 组件

:[components](../shared/components.md)

可用组件列表详见 [组件概述](/manuals/components/).

## 就地添加或通过引用添加的对象

当您创建集合、游戏对象或组件_文件_时，您创建的是我们所说的原型（在其他引擎中也称为"预制件"或"蓝图"）。这只是在项目文件结构中添加了一个文件，并没有在运行的游戏中添加任何内容。要添加基于原型文件的集合、游戏对象或组件的实例，您需要在其中一个集合文件中添加它的实例。

您可以在大纲视图中看到对象实例基于哪个文件。"main.collection"文件包含三个基于文件的实例：

1. "bean"子集合。
2. "bean"子集合中"bean"游戏对象中的"bean"脚本组件。
3. "can"游戏对象中的"can"脚本组件。

![Instance](images/building_blocks/instance.png)

当您有多个游戏对象或集合的实例并希望更改所有实例时，创建原型文件的好处就变得明显：

![GO instances](images/building_blocks/go_instance.png)

通过更改原型文件，任何使用该文件的实例都将立即更新。

![GO changing prototype](images/building_blocks/go_change_blueprint.png)

这里原型文件的精灵图像被更改，所有使用该文件的实例立即更新：

![GO instances updated](images/building_blocks/go_instance2.png)

## 创建游戏对象的父子关系

在集合文件中，您可以构建游戏对象的层次结构，使一个或多个游戏对象成为单个父游戏对象的子对象。只需简单地<kbd>拖动</kbd>一个游戏对象并将其<kbd>放置</kbd>到另一个游戏对象上，被拖动的游戏对象就成为目标游戏对象的子对象：

![Childing game objects](images/building_blocks/childing.png)

对象父子层次结构是一种动态关系，影响对象如何响应变换。在编辑器和运行时，应用于对象的任何变换（移动、旋转或缩放）都会依次应用于对象的子对象：

![Child transform](images/building_blocks/child_transform.png)

相反，子对象的平移是在父对象的局部空间中完成的。在编辑器中，您可以通过选择<kbd>Edit ▸ World Space</kbd>（默认）或<kbd>Edit ▸ Local Space</kbd>来选择在局部空间或世界空间中编辑子游戏对象。

也可以在运行时通过向对象发送`set_parent`消息来更改对象的父级。

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
一个常见的误解是，当游戏对象成为父子层次结构的一部分时，它在集合层次结构中的位置会发生变化。然而，这是两个非常不同的概念。父子层次结构动态地改变场景图，允许对象在视觉上相互附加。决定游戏对象地址的唯一因素是它在集合层次结构中的位置。地址在对象的整个生命周期中是静态的。
:::
