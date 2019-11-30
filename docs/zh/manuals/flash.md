---
title: Flash 开发者 Defold 过渡教程
brief: 本教程针对 Flash 游戏开发者对比介绍了 Defold 相对应的概念和方法.
---

# Flash 开发者 Defold 过渡

本教程针对 Flash 游戏开发者对比介绍了 Defold 相对应的概念和方法.

## 介绍

Flash 上手快门槛低. 新用户开发方便入门, 短时间内就可以开发出简单的游戏. Defold 针对游戏开发提供了类似的易用工具集, 此外还对高端开发者提供了更自由的发挥空间 (比如自己编写渲染脚本).

Flash 用 ActionScript (最新 3.0 版) 写脚本, Defold 用 Lua 写脚本. 本教程不涉及 Lua 和 Actionscript 3.0 编程. [Defold Lua 教程](/manuals/lua) 介绍了 Defold 中的 lua 脚本, [Programming in Lua](https://www.lua.org/pil/) (第一版) 有在线免费版可供学习.

Jesse Warden 写了一篇 [Actionscript 与 Lua 简要对比](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html) 的文章, 可以先看看这个. 注意 Defold 和 Flash 架构上的不同比起脚本语言的区别更多. Actionscript 和 Flash 是标准的面向对象的架构. Defold 却没有类也没有集成的概念. 它有着叫做 *游戏对象* 的概念, 用来表达视听, 行为和数据. 脚本通过调用 Defold API *函数* 进行逻辑编写. 而且, Defold 推荐使用 *消息* 机制进行对象间的互相通信. 消息机制比函数调用更高级别. 这些概念需要一段时间掌握, 本教程不做讲解.

本教程, 主要是寻找 Flash 开发中的关键技术, 然后在 Defold 中找到对应的解决方案. 我们将探讨相似处和区别以及一些注意事项, 让你快速从 Flash 过渡到 Defold.

## 影片剪辑和游戏对象

影片剪辑是 Flash 游戏开发的基础组成部分. 每个影片剪辑包含自己的时间轴. Defold 中类似的概念是游戏对象.

![game object and movieclip](images/flash/go_movieclip.png)

不同的是, Defold 游戏对象没有时间轴. 却能包含很多组件. 组件有 sprite, sound, 脚本---等等 (关于组件详情请见 [构成教程](/manuals/building-blocks)). 下图这个游戏对象包含一个 sprite 和一个脚本. 脚本用来控制游戏对象生命周期中的行为:

![script component](images/flash/script_component.png)

影片剪辑可以包含其他影片剪辑, 游戏对象不是 *包含* 其他游戏对象. 但是能够与其他游戏对象建立 *父子* 层级关系, 父子关系的游戏对象可以一起移动, 旋转和缩放.

## Flash 手动创建影片剪辑

Flash 里, 可以从库中往时间轴上拖放影片剪辑以创建实例. 下图中, 舞台上的每个图标都是logo影片剪辑的实例:

![manual movie clips](images/flash/manual_movie_clips.png)

## Defold 手动创建游戏对象

上文说了, Defold 没有时间轴概念. 但是, 集合可以用来管理游戏对象. 集合是容纳游戏对象和其他集合的容器 (或称 prefabs). 最简单的情况, 一个游戏有一个集合. 通常, Defold 游戏包含许多集合, 或者手动指定启动 “main” 集合或者通过 [集合代理](/manuals/collection-proxy) 动态载入集合. 但是 Flash 的 "levels" 或者 "screens" 没有这个能力.

下面的例子里, "main" 集合 (看右边, *Outline* 窗口里) 包含3个 "logo" 游戏对象 (看左边, *Assets* 浏览器窗口里):

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

::: 注意
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

## Flash—物体

Flash 里经常使用时间轴 (下图上半部分) 和舞台 (时间轴下方):

![timeline and stage](images/flash/stage.png)

就像上文提到的影片剪辑容器, 舞台是Flash游戏的顶级容器. 舞台默认有一个子集, 叫 *MainTimeline*. 项目中每个影片剪辑都有子集的时间轴, 可以作为容纳其他组件的容器 (包括可以嵌套影片剪辑).

## Defold—集合

Defold 的集合类似于舞台. 引擎启动时集合文件的内容组成了游戏世界. 默认启动集合叫 "main.collection" 但是可以在 *game.project* 项目配置文件里随意更改:

![game.project](images/flash/game_project.png)

集合作为容器管理着游戏对象和其他集合. 通过 [集合工厂](/manuals/collection-factory/#创建集合) 可以在运行时动态创建集合内容, 就像游戏对象工厂创建游戏对象一样. 集合可以包含多组敌人, 或者一堆钱币, 之类的. 下图中, 我们手动拖放了两组 "logos" 集合到 "main" 集合中.

![collection](images/flash/collection.png)

有时, 你需要载入完整的游戏世界. [集合代理](/manuals/collection-proxy/) 组件能让你基于集合文件内容创建一个新的游戏世界. 这在诸如需要加载关卡, 迷你游戏, 或者过场动画之类的功能时很有用.

## Flash—时间轴

Flash 时间轴主要用来制作动画, 可以是逐帧动画也可以是形状/运动补间动画. 项目设置定义了全局 FPS (帧每秒) 决定了每帧显示多长时间. 老鸟用户可以随时修改游戏 FPS, 或者为影片剪辑独立设置 FPS.

形状补间可以在矢量图的两个状态间进行插值. 这主要针对简单的图形和应用, 比如下例中把方块补间成三角:

![timeline](images/flash/timeline.png)

运动补间可以应用于对象属性, 包括大小, 位置和旋转. 下例中这些属性都进行了补间.

![motion tween](images/flash/tween.png)

## Defold—属性动画

Defold 不使用矢量图而是使用位图, 所以没有形状补间. 但是运动补间可以使用 [属性动画](/ref/go/#go.animate) 来实现. 通过脚本, 调用 `go.animate()` 函数即可. go.animate() 函数基于各种缓动函数 (可以自定义) , 对属性 (比如颜色, 缩放, 旋转或者位置) 进行从初始值到设定结束值的补间. Defold 引擎内置了许多要 Flash 用户自定义才能实现的 [缓动函数](/manuals/animation/#easing).

Flash 在时间轴上用关键帧做动画, Defold 动画功能之一是用导入的序列图做逐帧动画. 动画基于图集管理. 下例中图集有一个叫做 "run" 的动画. 此动画由一组图片组成:

![flipbook](images/flash/flipbook.png)

## Flash—深度索引

在 Flash 里, 显示列表决定显示次序. 每个容器 (比如舞台) 都有一个显示列表. 对象使用 `addChild()` 方法会自动被加入到显示列表顶端, 从 0 开始索引层层递增. 下图中, 有三个 "logo" 影片剪辑的对象:

![depth index](images/flash/depth_index.png)

图标上标注了其所在显示列表索引位置. 除去 x/y 位置设置, 如下代码会把图标加入到显示列表中:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

显示列表索引位置决定了它们的显示层次. 如果交互两个图标的索引, 比如:

```as
swapChildren(logo2,logo3);
```

结果如下 (索引已更新):

![depth index](images/flash/depth_index_2.png)

## Defold— z 轴位置

Defold 里游戏对象的位置向量包含三部分: x, y, 和 z. 其中 z 轴位置决定了其深度. 在默认 [渲染脚本](/manuals/render) 中, z 轴位置范围是 -1 到 1.

::: 注意
如果游戏对象的 z 轴位置不在 -1 到 1 的范围内就不会被渲染也就是不可见. Defold 新手经常会因为这个感到困惑, 所以如果发现该显示的东西不显示想想是不是这个原因.
:::

不同于 Flash 由编辑器决定显示索引 (然后可以使用 *Bring Forward* 和 *Send Backward* 之类的命令修改索引), Defold 可以在编辑器里直接设置游戏对象的 z 轴位置. 下图中, 你会看到 "logo3" 显示在最上层, 其 z 轴位置是 0.2. 其他两个的 z 轴位置是 0.0 和 0.1.

![z-order](images/flash/z_order.png)

Note that the z position of a game object nested in one or more collections is decided by its own z position, together with that of all its parents. For instance, imagine the logo game objects above were placed in a "logos" collection which in turn was placed in "main" (see screenshot below). If the "logos" collection had a z position of 0.9, the z positions of the game objects contained within would be 0.9, 1.0, and 1.1. Therefore, "logo3" would not be rendered as its z position is greater than 1.

![z-order](images/flash/z_order_outline.png)

The z position of a game object can of course be changed using script. Assume the below is located in the script component of a game object:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Flash—hitTestObject and hitTestPoint collision detection

Basic collision detection in Flash is achieved by using the `hitTestObject()` method. In this example, we have two movie clips: "bullet" and "bullseye". These are illustrated in the screenshot below. The blue boundary box is visible when selecting the symbols in the Flash editor, and it is these boundary boxes that drive the result of the `hitTestObject()` method.

![hit test](images/flash/hittest.png)

Collision detection using `hitTestObject()` is done as follows:

```as
bullet.hitTestObject(bullseye);
```

Using the boundary boxes in this case would not be appropriate, as a hit would be registered in the scenario below:

![hit test bounding box](images/flash/hitboundingbox.png)

An alternative to `hitTestObject()` is the `hitTestPoint()` method. This method contains a `shapeFlag` parameter, which allows hit tests to be conducted against the actual pixels of an object as opposed to the bounding box. Collision detection using `hitTestPoint()` could be done as below:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

This line would check the x and y position of the bullet (top left in this scenario) against the shape of the target. Since `hitTestPoint()` checks a point against a shape, which point (or points!) to check is a key consideration.

## Defold—collision objects

Defold includes a physics engine that can detect collisions and let a script react to it. Collision detection in Defold starts with assigning collision object components to game objects. In the screenshot below, we have added a collision object to the "bullet" game object. The collision object is indicated as the red transparent box (which is visible in the editor only):

![collision object](images/flash/collision_object.png)

Defold includes a modified version of the Box2D physics engine, which can simulate realistic collisions automatically. This guide assumes use of the kinematic collision objects, as these most closely resemble collision detection in Flash. Read more about the dynamic collision objects in the Defold [physics manual](/manuals/physics).

The collision object includes the following properties:

![collision object properties](images/flash/collision_object_properties.png)

A box shape has been used as this was most appropriate for the bullet graphic. The other shape used for 2D collisions, sphere, will be used for the target. Setting the type to Kinematic means resolving collisions is done by your script as opposed to the built-in physics engine (for more information on the other types, please refer to the [physics manual](/manuals/physics)). The group and mask properties determine what collision group the object belongs to and what collision group it should be checked against, respectively. The current setup means a "bullet" can only collide with a "target". Imagine the setup was changed to the below:

![collision group/mask](images/flash/collision_groupmask.png)

Now, bullets can collide with targets and other bullets. For reference, we have set up a collision object for the target that looks as follows:

![collision object bullet](images/flash/collision_object_bullet.png)

Note how the *Group* property is set to "target" and *Mask* is set to "bullet".

In Flash, collision detection occurs only when explicitly called by the script. In Defold, collision detection occurs continuously in the background as long as a collision object remains enabled. When a collision occurs, messages are sent to all components of a game object (most relevantly, the script components). These are the [collision_response and contact_point_response](/manuals/physics/#collision-messages) messages, which contain all the information required to resolve the collision as desired.

The advantage of Defold collision detection is that it is more advanced than that of Flash, with the ability to detect collisions between relatively complex shapes with very little setup effort. Collision detection is automatic, meaning looping through the various objects in the different collision groups and explicitly performing hit tests is not required. The main drawback is that there is no equivalent to the Flash shapeFlag. However, for most uses combinations of the basic box and sphere shapes suffice. For more complex scenarios, custom shapes [are possible](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash—event handling

Event objects and their associated listeners are used to detect various events (e.g. mouse clicks, button presses, clips being loaded) and trigger actions in response. There are a variety of events to work with.

## Defold—call-back functions and messaging

The Defold equivalent of the Flash event handling system consists of a few aspects. Firstly, each script component comes with a set of callback-functions that detect specific events. These are:

init
:   Called when the script component is initialised. Equivalent to the constructor function in Flash.

final
:   Called when the script component is destroyed (e.g. a spawned game object is removed).

update
:   Called every frame. Equivalent to enterFrame in Flash.

on_message
:   Called when the script component receives a message.

on_input
:   Called when user input (e.g. mouse or keyboard) is sent to a game object with [input focus](/ref/go/#acquire_input_focus), which means that the object receives all input and can react to it.

on_reload
:   Called when the script component is reloaded.

The callback functions listed above are all optional and can be removed if not used. For details on how to set up input, please refer to the [input manual](/manuals/input). A common pitfall occurs when working with collection proxies - please refer to [this section](/manuals/input/#input-dispatch-and-on_input) of the input manual for more information.

As discussed in the collision detection section, collision events are dealt with through the sending of messages to the game objects involved. Their respective script components receive the message in their on_message callback functions.

## Flash—button symbols

Flash uses a dedicated symbol type for buttons. Buttons use specific event handler methods (e.g. `click` and `buttonDown`) to execute actions when user interaction is detected. The graphical shape of a button in the "Hit" section of the button symbol determines the hit area of the button.

![button](images/flash/button.png)

## Defold—GUI scenes and scripts

Defold does not include a native button component, nor can clicks be easily detected against the shape of a given game object in the way buttons are handled in Flash. The use of a [GUI](/manuals/gui) component is the most common solution, partially because the positions of the Defold GUI components are not affected by the in-game camera (if used). The GUI API also contains functions for detecting if user input like clicks and touch events are within the bounds of a GUI element.

## Debugging

In Flash, the `trace()` command is your friend when debugging. The Defold equivalent is `print()`, and is used in the same way as `trace()`:

```lua
print("Hello world!"")
```

You can print multiple variables using one `print()` function:

```lua
print(score, health, ammo)
```

There is also a `pprint()` function (pretty print), which is useful when dealing with tables. This function prints the content of tables, including nested tables. Consider the script below:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

This contains a table (`factions`) nested in a table (`world`). Using the regular `print()` command would output the unique id of the table, but not the actual contents:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Using the `pprint()` function as illustrated above gives more meaningful results:

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

If your game uses collision detection, you can toggle physics debugging by posting the message below:

```lua
msg.post("@system:", "toggle_physics_debug")
```

Physics debug can also be enabled in the project settings. Before toggling physics debug our project would look like this:

![no debug](images/flash/no_debug.png)

Toggling physics debug displays the collision objects added to our game objects:

![with debug](images/flash/with_debug.png)

When collisions occur, the relevant collision objects light up. In addition, the collision vector is displayed:

![collision](images/flash/collision.png)

Finally, see the [profiler documentation](/ref/profiler/) for information on how to monitor CPU and memory usage. For more information on advanced debugging techniques, see the [debugging section](/manuals/debugging) in the Defold manual.

## Where to go from here

- [Defold examples](/examples)
- [Tutorials](/tutorials)
- [Manuals](/manuals)
- [Reference](/ref)
- [FAQ](/faq)

If you have questions or get stuck, the [Defold forums](//forum.defold.com) are a great place to reach out for help.
