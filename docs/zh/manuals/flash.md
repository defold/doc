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

::: sidenote
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

::: sidenote
如果游戏对象的 z 轴位置不在 -1 到 1 的范围内就不会被渲染也就是不可见. Defold 新手经常会因为这个感到困惑, 所以如果发现该显示的东西不显示想想是不是这个原因.
:::

不同于 Flash 由编辑器决定显示索引 (然后可以使用 *Bring Forward* 和 *Send Backward* 之类的命令修改索引), Defold 可以在编辑器里直接设置游戏对象的 z 轴位置. 下图中, 你会看到 "logo3" 显示在最上层, 其 z 轴位置是 0.2. 其他两个的 z 轴位置是 0.0 和 0.1.

![z-order](images/flash/z_order.png)

注意游戏对象 z 轴位置是由其本身 z 轴位置, 连同其所有父级的 z 轴位置共同决定的. 比如, 假设上文图标位于 "logos" 集合中, 该集合又位于 "main" 集合中 (见下图). 如果 "logos" 集合 z 位置是 0.9, 那么这三个图标的 z 位置就会是 0.9, 1.0, 和 1.1. 所以, "logo3" 不会被渲染因为其 z 位置大于 1.

![z-order](images/flash/z_order_outline.png)

z 轴位置可由脚本更改. 如下代码设置了游戏对象的 z 轴位置:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Flash—hitTestObject 和 hitTestPoint 碰撞检测

Flash 中使用 `hitTestObject()` 方法进行基本碰撞检测. 举个例子, 有两个影片剪辑: "bullet" 和 "bullseye". 见下图. 在 Flash 编辑器选中对象时会显示一个蓝色边框, `hitTestObject()` 方法就是用这样的边框来进行碰撞检测的.

![hit test](images/flash/hittest.png)

如下使用 `hitTestObject()` 进行碰撞检测:

```as
bullet.hitTestObject(bullseye);
```

这样检测可能会不准确, 比如如下的情况:

![hit test bounding box](images/flash/hitboundingbox.png)

除了 `hitTestObject()` 还有 `hitTestPoint()` 方法. 此方法包含一个 `shapeFlag` 参数, 可以提供像素对目标有像素形状的碰撞检测. 如下使用 `hitTestPoint()` 进行碰撞检测:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

这样通过子弹 x 和 y 坐标 (子弹图片左上角) 对靶子形状进行碰撞检测. 因为 `hitTestPoint()` 是点对形状的碰撞检测, 哪个 (或哪些) 点需要检测是要考虑的关键.

## Defold—碰撞对象

Defold 内含物理引擎可以用于碰撞检测然后使用其上的脚本进行相应. 首先要在游戏对象上面添加碰撞对象组件. 如下图所示, 我们对 "bullet" 游戏对象添加了碰撞对象. 碰撞对象以红色半透明方块表示 (只在编辑器中可见):

![collision object](images/flash/collision_object.png)

Defold 包含一个 Box2D 物理引擎的修改版, 可以用来自动模拟真实的碰撞. 本教程使用运 Kinematic 碰撞对象, 因为它的碰撞检测和 Flash 的最接近. 关于动态碰撞详情请见 Defold [物理教程](/manuals/physics).

此碰撞对象包含如下属性:

![collision object properties](images/flash/collision_object_properties.png)

用一个矩形代表上例中的子弹. 圆形代表靶子进行碰撞检测. 设置类型为 Kinematic 意味着使用脚本进行碰撞处理, 物理引擎默认不是这样 (关于其他类型, 请见 [物理手册](/manuals/physics)). 属性 group 和 mask 分别决定了碰撞对象属于哪个组以及和哪个组相碰撞. 当前设置是 "bullet" 只能与 "target" 碰撞. 要是如下这样:

![collision group/mask](images/flash/collision_groupmask.png)

子弹之间就能相互碰撞了. 我们为靶子设置了如下的碰撞对象:

![collision object bullet](images/flash/collision_object_bullet.png)

注意 *Group* 属性设置为了 "target" 然后 *Mask* 设置为了 "bullet".

Flash 里, 需要脚本调用才会进行碰撞检测. Defold 里, 只要碰撞对象开启, 后台就会持续进行碰撞检测. 碰撞发生时, 消息会发送到游戏对象所有组件上 (更确切地说是脚本组件). 有 [碰撞处理和碰撞点处理消息](/manuals/physics/#碰撞消息), 其中包含了处理碰撞所需的各种信息.

Defold 的碰撞检测比 Flash 的要高级, 毫不费力就能检测复杂形状间的碰撞. 碰撞检测是自动的, 也就是说不需要手动遍历各个对象然后挨个进行碰撞检测. 但是没有 Flash 的 shapeFlag. 但是对于复杂图形可以使用简单图形组合达成. 更复杂的需求下, 还可以使用 [自定义图形](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash—事件监听

事件对象及其监听器用来检测各种事件 (比如说 鼠标点击, 按钮按下, 剪辑加载) 并在反馈里处理行为. 包括许许多多的事件.

## Defold—回调函数和消息

Defold 跟 Flash 比有几个地方差不多. 首先, 每个脚本组件都包含一组特定事件的回调函数. 具体有:

init
:   脚本组件初始化时调用. 相当于 Flash 的构造函数.

final
:   脚本组件析构时调用 (比如游戏对象被删除时).

update
:   在每一帧调用. 相当于 Flash 的 enterFrame.

on_message
:   当脚本组件收到消息时调用.

on_input
:   当用户输入 (比如鼠标或键盘) 发送到得到 [输入焦点](/ref/go/#acquire_input_focus) 的游戏对象上时调用, 得到输入焦点的游戏对象会接收并反馈所有输入.

on_reload
:   脚本组件重载时调用.

这些都是可选回调函数如果不需要可以删除. 关于如何接收输入, 详情请见 [输入教程](/manuals/input). 有一个关于集合代理易用错的地方 - 详情请见输入教程的 [这一章](/manuals/input/#输入调度和 on_input() 函数).

就像碰撞检测部分说的那样, 碰撞事件被发送到相关游戏对象上进行处理. 各个脚本组件的 on_message 回调函数会被调用.

## Flash—按钮剪辑

Flash 为按钮使用了一种特殊剪辑. 按钮监听到用户交互时使用特殊的事件处理方法 (比如 `click` 和 `buttonDown`) 来运行指定行为. 按钮 "Hit" 部分的图形决定了按钮的可点击区域.

![button](images/flash/button.png)

## Defold—GUI场景和脚本

Defold 没有内置按钮组件, 也不像 Flash 那样使用游戏对象的图形进行方便的点击检测. 使用 [GUI](/manuals/gui) 组件是一个通用方案, 部分因为 Defold GUI 组件的位置不受游戏中摄像机 (如果有使用). GUI API 还包含在 GUI 组件的范围内检测用户输入例如点击和触摸事件的功能.

## 调试

在 Flash 里, 用 `trace()` 命令帮助调试. 在 Defold 里相应的是 `print()`, 跟使用 `trace()` 方法一样:

```lua
print("Hello world!"")
```

可以调用一次 `print()` 函数输出多个变量:

```lua
print(score, health, ammo)
```

还有一个 `pprint()` 函数 (pretty print), 用于打印表. 此函数能输出表的内容, 包括嵌套表. 看下面的脚本:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

这里把表 (`factions`) 嵌入到表 (`world`) 里. 使用普通 `print()` 命令只会输出表的id, 不含内容:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

使用 `pprint()` 函数就能显示出更多内容:

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

如果游戏使用了碰撞检测, 可以发送如下消息开关物理调试:

```lua
msg.post("@system:", "toggle_physics_debug")
```

也可以在项目设置里打开物理调试. 打开物理调试前我们的项目看起来像这样:

![no debug](images/flash/no_debug.png)

打开物理调试显示出项目中的碰撞对象:

![with debug](images/flash/with_debug.png)

当碰撞发生时, 相关碰撞对象会高光显示. 而且, 碰撞向量也会被显示出来:

![collision](images/flash/collision.png)

最后, 关于检测 CPU 和内存使用情况详情请见 [性能分析教程](/ref/profiler/). 更高级的调试技术, 详情请见 Defold 手册的 [调试部分](/manuals/debugging).

## 更多参考

- [Defold examples](/examples)
- [Tutorials](/tutorials)
- [Manuals](/manuals)
- [Reference](/ref)
- [FAQ](/faq)

如果你有疑问, [Defold 论坛](//forum.defold.com) 是一个获取帮助的好地方.
