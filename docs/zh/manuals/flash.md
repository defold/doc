---
title: Defold for Flash users
brief: 本指南为 Flash 游戏开发者介绍了 Defold 作为替代方案。它涵盖了 Flash 游戏开发中使用的一些关键概念，并解释了 Defold 中相应的工具和方法。
---

# Defold for Flash users

本指南为 Flash 游戏开发者介绍了 Defold 作为替代方案。它涵盖了 Flash 游戏开发中使用的一些关键概念，并解释了 Defold 中相应的工具和方法。

## Introduction

Flash 的一些主要优势是易用性和低入门门槛。新用户可以快速学习该程序，并能在有限的时间投入内创建基本游戏。Defold 通过提供一套专门用于游戏设计的工具提供了类似的优势，同时使高级开发者能够为更复杂的需求创建高级解决方案（例如允许开发者编辑默认渲染脚本）。

Flash 游戏使用 ActionScript 编程（3.0 是最新版本），而 Defold 脚本使用 Lua 编写。本指南不会详细比较 Lua 和 Actionscript 3.0。[Defold 手册](/manuals/lua) 提供了 Defold 中 Lua 编程的良好介绍，并引用了非常有用的 [Programming in Lua](https://www.lua.org/pil/)（第一版），该书可在线免费获取。

Jesse Warden 的一篇文章提供了 [Actionscript 和 Lua 的基本比较](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html)，这可以作为一个很好的起点。但请注意，Defold 和 Flash 在构建方式上的差异比语言层面可见的差异更深。Actionscript 和 Flash 在经典意义上是面向对象的，具有类和继承。Defold 没有类，也没有继承。它包含 *游戏对象* 的概念，可以包含视听表示、行为和数据。对游戏对象的操作是通过 Defold API 中可用的 *函数* 完成的。此外，Defold 鼓励使用 *消息* 在对象之间进行通信。消息是比方法调用更高级的构造，并不打算用作方法调用。这些差异很重要，需要一段时间才能适应，但本指南不会详细讨论。

相反，本指南探讨了 Flash 游戏开发的一些关键概念，并概述了 Defold 中最接近的等价物。讨论了相似性和差异，以及常见的陷阱，使你能够从 Flash 过渡到 Defold 时快速上手。

## 影片剪辑和游戏对象

影片剪辑是 Flash 游戏开发的基础组成部分。每个影片剪辑包含自己的时间轴。Defold 中类似的概念是游戏对象。

![game object and movieclip](images/flash/go_movieclip.png)

不同的是，Defold 游戏对象没有时间轴。却能包含很多组件。组件有 sprite、sound、脚本等等（关于组件详情请见 [构成教程](/manuals/building-blocks)）。下图这个游戏对象包含一个 sprite 和一个脚本。脚本用来控制游戏对象生命周期中的行为：

![script component](images/flash/script_component.png)

影片剪辑可以包含其他影片剪辑，游戏对象不是 *包含* 其他游戏对象。但是能够与其他游戏对象建立 *父子* 层级关系，父子关系的游戏对象可以一起移动、旋转和缩放。

## Flash 手动创建影片剪辑

在 Flash 中，影片剪辑可以在 IDE 中手动创建，也可以运行时动态创建。手动创建的影片剪辑需要给实例名，才能在代码里引用。

![manual movie clips](images/flash/manual_movie_clips.png)

## Defold—manually creating game objects

Defold 中，游戏对象可以在编辑器里手动创建，也可以运行时动态创建。手动创建的游戏对象需要给唯一 id，才能在代码里引用。

集合可以用来管理游戏对象。集合是容纳游戏对象和其他集合的容器（或称 prefabs）。最简单的情况，一个游戏有一个集合。通常，Defold 游戏包含许多集合，或者手动指定启动 “main” 集合或者通过 [集合代理](/manuals/collection-proxy) 动态载入集合。但是 Flash 的 "levels" 或者 "screens" 没有这个能力。

下面的例子里，"main" 集合（看右边，*Outline* 窗口里）包含3个 "logo" 游戏对象（看左边，*Assets* 浏览器窗口里）：

![manual game objects](images/flash/manual_game_objects.png)

## Flash—手动引用影片剪辑

Flash 需要定义影片剪辑实例名再手动引用:

![flash instance name](images/flash/flash_instance_name.png)

## Defold—游戏对象id

Defold 通过地址引用所有对象. 多数情况下使用快捷地址或者短小的名字就好. 例如:

- `"."` 定位当前游戏对象.
- `"#"` 定位当前脚本组件.
- `"logo"` 定位 id 叫 "logo" 的游戏对象.
- `"#script"` 定位当前游戏对象里 id 叫 "script" 的脚本组件.
- `"logo#script"` 定位游戏对象 "logo" 下的 "script" 脚本.

手动拖放对象的地址由 *Id* 属性 (上图右下角) 决定. 每个集合里一个对象的id是唯一的. 编辑器可以自动生成默认id但是所有对象的id都可以随意更改.

![game object id](images/flash/game_object_id.png)

::: important
对象的id可以使用脚本: `print(go.get_id())` 查看. 它会在控制台打印出当前游戏对象的id.
:::

地址定位和消息传递是 Defold 游戏开发的核心概念. [定位教程](/manuals/addressing) 和 [消息传递教程](/manuals/message-passing) 里有更详细的介绍.

## Flash—动态创建影片剪辑

Flash 里动态创建影片剪辑, 需要预先设置好 ActionScript Linkage:

![actionscript linkage](images/flash/actionscript_linkage.png)

它创建了一个类 (本例是 Logo 图标), 这个类可以用于创建对象. 如下代码使用Logo类在舞台上创建了logo对象:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold—使用工厂创建游戏对象

Defold 使用 *工厂* 动态创建游戏对象. 工厂是创建游戏对象拷贝的组件. 本例中, 以 "logo" 游戏对象为原型创建了一个工厂组件:

![logo factory](images/flash/logo_factory.png)

注意工厂组件, 需要像其他组件一样, 需要添加到游戏对象里才能用. 本例中, 我们创建了叫做 "factories" 的游戏对象, 来容纳工厂组件:

![factory component](images/flash/factory_component.png)

如下代码使用工厂创建了游戏对象实例:

```lua
local logo_id = factory.create("factories#logo_factory")
```

URL 是 `factory.create()` 函数的必要参数. 此外, 还有可选参数用以设置位置, 旋转, 缩放, 和其他属性. 工厂组件详情请见 [工厂教程](/manuals/factory). 注意调用 `factory.create()` 可返回被创建游戏对象的id. 可以把这个id放入表中留待以后引用 (Lua 的表相当于其他语言的数组).

## Flash—stage

In Flash, we are familiar with the Timeline (top section of the screenshot below) and the Stage (visible below the Timeline):

![timeline and stage](images/flash/stage.png)

As discussed in the movie clips section above, the Stage is essentially the top level container of a Flash game and is created each time a project is exported. The Stage will by default have one child, the *`MainTimeline`*. Each movie clip generated in the project will have its own timeline, and can serve as a container for other symbols (including movie clips).

## Defold—collections

Defold 的集合类似于舞台. 引擎启动时集合文件的内容组成了游戏世界. 默认启动集合叫 "main.collection" 但是可以在 *game.project* 项目配置文件里随意更改:

![game.project](images/flash/game_project.png)

集合作为容器管理着游戏对象和其他集合. 通过 [集合工厂](/manuals/collection-factory/#创建集合) 可以在运行时动态创建集合内容, 就像游戏对象工厂创建游戏对象一样. 集合可以包含多组敌人, 或者一堆钱币, 之类的. 下图中, 我们手动拖放了两组 "logos" 集合到 "main" 集合中.

![collection](images/flash/collection.png)

有时, 你需要载入完整的游戏世界. [集合代理](/manuals/collection-proxy/) 组件能让你基于集合文件内容创建一个新的游戏世界. 这在诸如需要加载关卡, 迷你游戏, 或者过场动画之类的功能时很有用.

## Flash—时间轴和属性动画

Flash 使用时间轴创建动画。可以在时间轴上添加关键帧并设置对象的属性，如位置、大小、透明度等。Flash 会自动在关键帧之间创建补间动画。

Flash 的时间轴以帧为单位，默认帧率是 24 FPS（帧每秒）。可以通过修改帧率来改变动画速度。

形状补间可以在矢量图的两个状态间进行插值。这主要针对简单的图形和应用，比如下例中把方块补间成三角：

![timeline](images/flash/timeline.png)

运动补间可以应用于对象属性，包括大小、位置和旋转。下例中这些属性都进行了补间。

![motion tween](images/flash/tween.png)

## Defold—属性动画

Defold 不使用矢量图而是使用位图，所以没有形状补间。但是运动补间可以使用 [属性动画](/ref/go/#go.animate) 来实现。通过脚本，调用 `go.animate()` 函数即可。go.animate() 函数基于各种缓动函数（可以自定义），对属性（比如颜色、缩放、旋转或者位置）进行从初始值到设定结束值的补间。Defold 引擎内置了许多要 Flash 用户自定义才能实现的 [缓动函数](/manuals/animation/#easing)。

Flash 在时间轴上用关键帧做动画，Defold 动画功能之一是用导入的序列图做逐帧动画。动画基于图集管理。下例中图集有一个叫做 "run" 的动画，此动画由一组图片组成：

![flipbook](images/flash/flipbook.png)

## Flash—depth index

在 Flash 里，深度索引（显示列表索引）决定影片剪辑的显示顺序。每个容器（如舞台）都维护一个显示列表，索引值越大，对象越靠前显示。对象通过 `addChild()` 方法加入显示列表，索引从 0 开始递增。下图展示了三个 "logo" 影片剪辑的深度索引：

![depth index](images/flash/depth_index.png)

示例代码将三个图标按顺序加入显示列表：

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1); // 索引 0
addChild(logo2); // 索引 1
addChild(logo3); // 索引 2
```

通过 swapChildren() 可交换对象的深度索引，例如：

```as
swapChildren(logo2, logo3); // 交换索引 1 和 2
```

交换后效果如下：

![depth index](images/flash/depth_index_2.png)

## Defold—z position

Defold 使用 z 轴位置控制游戏对象的显示顺序。每个游戏对象的位置向量包含 x、y、z 三个分量，其中 z 值越大，对象越靠前显示。在默认 [渲染脚本](/manuals/render) 中，z 轴有效范围为 -1 到 1。

::: important
若游戏对象的 z 值超出 [-1, 1] 范围将不会被渲染（不可见）。这是新手常见困惑点，若对象未显示请优先检查 z 值。
:::

与 Flash 的深度索引不同，Flash 编辑器只隐含深度索引（并允许使用*Bring Forward*和*Send Backward*等命令修改），而 Defold 可直接在编辑器中设置 z 值。下图示例中，"logo3" 因 z=0.2 显示在最上层，其余两个对象 z 值分别为 0.0 和 0.1：

![z-order](images/flash/z_order.png)

层级叠加规则：对象的最终 z 值 = 自身 z 值 + 所有父级 z 值之和。例如，若 "logos" 集合（包含三个图标）的 z=0.9，则三个图标的最终 z 值为 0.9、1.0、1.1，此时 "logo3" 因 z=1.1 > 1 而不可见：

![z-order](images/flash/z_order_outline.png)

脚本动态修改：
```lua
local pos = go.get_position()
pos.z = 0.5  -- 设置 z 轴位置
go.set_position(pos)
```

## Flash `hitTestObject` and `hitTestPoint` collision detection

Basic collision detection in Flash is achieved by using the `hitTestObject()` method. In this example, we have two movie clips: "bullet" and "bullseye". These are illustrated in the screenshot below. The blue boundary box is visible when selecting the symbols in the Flash editor, and it is these boundary boxes that drive the result of the `hitTestObject()` method.

![hit test](images/flash/hittest.png)

Using `hitTestObject()` for collision detection:

```as
bullet.hitTestObject(bullseye);
```

In this case, the use of boundary boxes is inappropriate, as the following scenario would register a collision:

![hit test bounding box](images/flash/hitboundingbox.png)

In addition to `hitTestObject()`, there is also the `hitTestPoint()` method. This method includes a `shapeFlag` parameter that provides pixel-perfect collision detection against the actual shape of the target. Using `hitTestPoint()` for collision detection:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

This performs collision detection between the bullet's x and y coordinates (the top-left corner of the bullet image) and the bullseye shape. Since `hitTestPoint()` checks for collisions between a point and a shape, determining which point (or points!) to check is a crucial consideration.

## Defold—collision objects

Defold 内含物理引擎可以用于碰撞检测然后使用其上的脚本进行响应。首先要在游戏对象上面添加碰撞对象组件。如下图所示，我们对 "bullet" 游戏对象添加了碰撞对象。碰撞对象以红色半透明方块表示（只在编辑器中可见）：

![collision object](images/flash/collision_object.png)

Defold 包含一个 Box2D 物理引擎的修改版，可以用来自动模拟真实的碰撞。本教程使用 Kinematic 碰撞对象，因为它的碰撞检测和 Flash 的最接近。关于动态碰撞详情请见 Defold [物理教程](/manuals/physics)。

此碰撞对象包含如下属性：

![collision object properties](images/flash/collision_object_properties.png)

用一个矩形代表上例中的子弹。圆形代表靶子进行碰撞检测。设置类型为 Kinematic 意味着使用脚本进行碰撞处理，物理引擎默认不是这样（关于其他类型，请见 [物理手册](/manuals/physics)）。属性 group 和 mask 分别决定了碰撞对象属于哪个组以及和哪个组相碰撞。当前设置是 "bullet" 只能与 "target" 碰撞。要是如下这样：

![collision group/mask](images/flash/collision_groupmask.png)

子弹之间就能相互碰撞了。我们为靶子设置了如下的碰撞对象：

![collision object bullet](images/flash/collision_object_bullet.png)

注意 *Group* 属性设置为了 "target" 然后 *Mask* 设置为了 "bullet"。

Flash 里，需要脚本调用才会进行碰撞检测。Defold 里，只要碰撞对象开启，后台就会持续进行碰撞检测。碰撞发生时，消息会发送到游戏对象所有组件上（更确切地说是脚本组件）。有 [碰撞处理和碰撞点处理消息](/manuals/physics/#碰撞消息)，其中包含了处理碰撞所需的各种信息。

Defold 的碰撞检测比 Flash 的要高级，毫不费力就能检测复杂形状间的碰撞。碰撞检测是自动的，也就是说不需要手动遍历各个对象然后挨个进行碰撞检测。但是没有 Flash 的 `shapeFlag`。但是对于复杂图形可以使用简单图形组合达成。更复杂的需求下，还可以使用 [自定义图形](https://forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985)。

## Flash—event handling

In Flash, event handling is done through event listeners. You can use the addEventListener() method to add event listeners.

## Defold—call-back functions and messaging

Defold 中与 Flash 事件处理系统等效的几个方面。首先，每个脚本组件都带有一组检测特定事件的回调函数。这些函数包括：

init
:   脚本组件初始化时调用。相当于 Flash 中的构造函数。

final
:   脚本组件被销毁时调用（例如，生成的游戏对象被移除）。

update
:   每帧调用。相当于 Flash 中的 `enterFrame`。

on_message
:   脚本组件接收到消息时调用。

on_input
:   当用户输入（例如鼠标或键盘）发送到具有[输入焦点](/ref/go/#acquire_input_focus)的游戏对象时调用，这意味着该对象接收所有输入并可以对其做出反应。

on_reload
:   脚本组件重新加载时调用。

上面列出的回调函数都是可选的，如果不使用可以删除。有关如何设置输入的详细信息，请参阅[输入手册](/manuals/input)。使用集合代理时会出现一个常见问题 - 请参阅输入手册的[此部分](/manuals/input/#input-dispatch-and-on_input)获取更多信息。

如碰撞检测部分所述，碰撞事件通过向涉及的游戏对象发送消息来处理。它们各自的脚本组件在其 on_message 回调函数中接收消息。

## Flash—button symbols

Flash uses a dedicated symbol type for buttons. Buttons use specific event handling methods (such as `click` and `buttonDown`) to perform actions when user interaction is detected. The graphic shape in the "Hit" part of a button symbol determines the clickable area of the button.

![button](images/flash/button.png)

## Defold—GUI scenes and scripts

Defold does not include a native button component, nor can it detect clicks on a given game object's shape as easily as you can in Flash. Using [GUI](/manuals/gui) components is the most common solution, partly because Defold GUI components are positioned independently of any in-game camera (if one is used). The GUI API also includes functions to detect if user input (such as click and touch events) falls within the bounds of a GUI element.

## Debugging

In Flash, you use the `trace()` command to help with debugging. The equivalent in Defold is `print()`, which works the same way as `trace()`:

```lua
print("Hello world!")
```

You can print multiple variables with a single `print()` call:

```lua
print(score, health, ammo)
```

There's also a `pprint()` function (pretty print) for printing tables. This function outputs the contents of a table, including nested tables. Consider the following script:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Here we embed a table (`factions`) into another table (`world`). Using the regular `print()` command would only output the table's id, not its contents:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Using the `pprint()` function shows much more useful information:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

If your game uses collision detection, you can toggle physics debugging with the following message:

```lua
msg.post("@system:", "toggle_physics_debug")
```

You can also enable physics debugging in the project settings. Before enabling physics debugging, our project looks like this:

![no debug](images/flash/no_debug.png)

With physics debugging enabled, the collision objects in the project are shown:

![with debug](images/flash/with_debug.png)

当碰撞发生时，相关碰撞对象会高光显示。而且，碰撞向量也会被显示出来：

![collision](images/flash/collision.png)

最后，关于检测 CPU 和内存使用情况详情请见 [性能分析教程](/ref/profiler/)。更高级的调试技术，详情请见 Defold 手册的 [调试部分](/manuals/debugging)。

## Where to go from here

- [Defold 示例](/examples)
- [教程](/tutorials)
- [手册](/manuals)
- [参考](/ref/go)
- [常见问题](/faq/faq)

如果你有问题或遇到困难，[Defold 论坛](https://forum.defold.com) 是寻求帮助的好地方。
