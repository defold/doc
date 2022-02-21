---
title: Defold 术语
brief: 本教程列举了使用 Defold 工作中会遇到的各种专用词汇及其简短的解释.
---

# Defold 术语

该名词表简要介绍了您在 Defold 中遇到的各种术语.在大多数情况下,您会找到更多相关详细文档的链接.

## Animation set

![Animation set](images/icons/animationset.png){.left} 包含一组动画的 .dae 文件或其他用以读取动画的 .animationset 文件的动画集资源. 如果多个模型文件共享一组动画的话, 可以方便地把 .animationset 文件设置给其他模型. 详情请见 [3D 图像教程](/manuals/graphics/).

## Atlas

![Atlas](images/icons/atlas.png){.left} 图集是为了增加性能减少显存消耗而把许多单张图片合并而成的一张大图. 其中可以包括静态图和逐帧动画序列图. 图集可被 GUI, Sprite, Spine model 和 ParticleFX 组件所共享. 详情请见 [图集教程](/manuals/atlas).

## Builtins

![Builtins](images/icons/builtins.png){.left} 项目内置文件夹是一个包含必要默认资源的只读文件夹. 里面由默认着色器, 默认渲染脚本, 默认材质等等. 如果需要自定义这些默认资源, 只要把它们拷贝到你的项目目录中去, 然后自由修改即可.

## Camera

![Camera](images/icons/camera.png){.left} 摄像机组件决定了游戏世界哪些可见哪些不可见以及视口的投射类型. 一个常见用法是把摄像机放到主角游戏对象上, 或者放到一个跟随主角的包含一些平滑移动算法的游戏对象上. 详情请见 [摄像机教程](/manuals/camera).

## Collision object

![Collision object](images/icons/collision-object.png){.left} 碰撞对象组件为游戏对象增添了物理属性 (比如形状, 重量, 摩擦力和弹性). 这些属性决定了碰撞对象之间的碰撞效果. 常见碰撞对象有运动学, 动态和触发器三种类型. 运动学碰撞对象必须手动设置它的物理属性值, 动态碰撞对象由物理引擎基于牛顿物理定律计算它的物理属性. 触发器是一个形状, 能够检测其他物体进入或者离开. 详情请见 [物理教程](/manuals/physics).

## Component

组件赋予游戏对象以独特的功能和表现, 如图像, 动画, 逻辑和声音等等. 组件依附于游戏对象之上. Defold 中预置了许多组件. 详情请见 [游戏组成教程](/manuals/building-blocks).

## Collection

![Collection](images/icons/collection.png){.left} 集合是 Defold 的模板机制, 相当于其他引擎的 "prefabs" 即可重用游戏对象的树形结构. 集合可以包含游戏对象和其他集合. 集合结构作为文件资源储存, 既可以在编辑器里手动创建实例, 又可以在运行时动态创建实例. 详情请见 [游戏组成教程](/manuals/building-blocks).

## Collection factory

![Collection factory](images/icons/collection-factory.png){.left} 集合工厂是集合实例制造者, 可以在运行时动态创建集合实例. 详情请见 [集合工程教程](/manuals/collection-factory).

## Collection proxy

![Collection proxy](images/icons/collection-proxy.png){.left} 集合代理可以在游戏进行时加载并激活集合. 常常被用来切换游戏关卡. 详情请见 [集合代理教程](/manuals/collection-proxy).

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} Cubemap 是由 6 张纹理组成的一种特殊纹理, 可以完整覆盖在立方体上. 常常被用于天空盒, 也被用作各种反射纹理和光照纹理等.

## Debugging

调试是程序除错的方法. Defold 给用户提供了方便的内置调试器. 详情请见 [调试教程](/manuals/debugging).

## Display profiles

![Display profiles](images/icons/display-profiles.png){.left} 显示档案是一种文件资源用来确定在指定屏幕方向, 宽高比, 或设备型号匹配到显示设备时使用哪种用户界面布局方案. 它能帮助用户适配各种设备屏幕. 详情请见 [界面布局教程](/manuals/gui-layouts).

## Factory

![Factory](images/icons/factory.png){.left} 工厂是游戏对象实例制造者, 用来在运行时创建游戏对象实例. 例如, 发射子弹游戏对象, 就可以可以使用工厂 (其内部含有对象池功能). 详情请见 [工厂教程](/manuals/factory).

## Font

![Font file](images/icons/font.png){.left} 字体资源源自 TrueType 或 OpenType 字体文件. 可以设置渲染文字的大小和外观 (描边和阴影). GUI 和 Label 组件要用到字体资源. 详情请见 [字体教程](/manuals/font/).

## Fragment shader

![Fragment shader](images/icons/fragment-shader.png){.left} 一种运行于显卡上的用于处理多边形上每个像素 (片元) 的渲染程序. 由此程序决定每个像素的颜色. 最终像素颜色值通过计算和纹理查找 (一个或多个) 的方法得出. 详情请见 [着色器教程](/manuals/shader).

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} 手柄资源文件用来定义游戏手柄设备在指定平台上的输入对游戏的意义. 详情请见 [输入教程](/manuals/input).

## Game object

![Game object](images/icons/game-object.png){.left} 游戏对象在游戏过程中有各自的生命周期. 游戏对象是组件的容器, 比如可以包含声音和图像组件等. 游戏对象还是游戏逻辑脚本代码的载体. 游戏对象既可以使用编辑器创建并放置于集合志宏, 也可以使用工厂在运行时进行实例化. 详情请见 [游戏组成教程](/manuals/building-blocks).

## GUI

![GUI component](images/icons/gui.png){.left} GUI 组件用来组成用户界面: 包含文字, 图像等等. 这些组件组成树形结构, 可以被脚本和动画控制. GUI 组件常用于组成屏幕操作界面, 菜单系统和提示框等等. GUI 组件使用 GUI 脚本控制以实现交互行为. 详情请见 [GUI 教程](/manuals/gui).

## GUI script

![GUI script](images/icons/script.png){.left} GUI 脚本用于控制界面组件的行为. 它决定了界面元素如何移动, 用户如何与界面元素交互. 详情请见 [Defold 的 Lua 教程](/manuals/lua).

## Hot reload

Defold 允许在游戏运行时进行内容更新, 支持桌面和移动设备. 这项功能能为游戏开发者大大节省开发和调试时间. 详情请见 [热重载教程](/manuals/hot-reload).

## Input binding

![Input binding](images/icons/input-binding.png){.left} 输入绑定定义了输入设备 (鼠标, 键盘, 触摸屏和手柄等) 输入信息的含义. 它把硬件输入与游戏行为进行绑定, 比如 "跳跃" 和 "前进" _行为_. 这样监听输入的脚本就能根据这些行为控制与之相配的动作. 详情请见 [输入教程](/manuals/input).

## Label

![Label](images/icons/label.png){.left} 标签组件用来给游戏对象加上文字内容. 它使用指定字体在游戏空间中被渲染出来. 详情请见 [标签教程](/manuals/label).

## Library

![Game object](images/icons/builtins.png){.left} Defold 使用库机制进行资源共享. 资源共享可以是项目间的, 也可以是团队成员间的. 详情请见 [库教程](/manuals/libraries).

## Lua language

Lua 语言在 Defold 中用来创建游戏逻辑. Lua 是一种强大高效而又轻量级的脚本语言. 它支持多种设计模式和数据描述. 详情请见官网 https://www.lua.org/ 和 [Defold 脚本手册](/manuals/lua).

## Lua module

![Lua module](images/icons/lua-module.png){.left} Lua 模块可以用来构建项目编写可重用代码. 详情请见 [Lua 模块教程](/manuals/modules/)

## Material

![Material](images/icons/material.png){.left} 材质使用指定的着色器及其属性来实现特定的视觉效果. 详情请见 [材质教程](/manuals/material).

## Message

组件使用消息与系统或者与其他游戏对象进行信息交流. 有许多预定义的消息提供给组件使用以便实现某些功能. 比如隐藏图像或者推动物理物体. 游戏引擎通过消息传递事件, 比如物理物体碰撞事件. 要发送消息必须有接收者. 所以每个游戏对象每个组件的路径都是唯一的. Defold 给 Lua 增添了消息传递功能以及包含各种功能的库.

举个例子, 要隐藏一个 sprite 可以这么写:

```lua
msg.post("#weapon", "disable")
```

此处, `"#weapon"` 就是游戏对象 sprite 组件的路径. `"disable"` 是发给 sprite 组件的消息内容. 详情请见 [消息传递教程](/manuals/message-passing).

## Model

![Model](images/icons/model.png){.left} 3D 模型组件支持在游戏中使用 Collada 网格模型, 骨骼和动画. 详情请见 [模型教程](/manuals/model/).

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} 粒子特效用来实现游戏里的某些视觉效果. 包括雾, 烟, 火, 雨或者落叶等等. Defold 自带了一个功能强大的例子编辑器用来创建和实时调整粒子效果. 详情请见 [粒子教程](/manuals/particlefx).

## Profiling

性能对于游戏至关重要, 通过数据分析你可以发现游戏性能上的瓶颈以及内存泄漏等问题. 详情请见 [性能分析教程](/manuals/profiling).

## Render

![Render](images/icons/render.png){.left} 渲染文件包含把游戏渲染到屏幕所需的设置和参数. 渲染文件决定了使用哪个渲染脚本和哪个材质资源. 详情请见 [Render manual](/manuals/render/).

## Render script

![Render script](images/icons/script.png){.left} 渲染脚本是由 Lua 语言编写的用于渲染游戏内容的脚本. 自带的默认渲染脚本大多数情况下可用, 但是如果需求自定义效果就需要自己写渲染脚本了. 详情请见 [渲染教程](/manuals/render/) for more details on how the render pipeline works, and the [Lua in Defold manual](/manuals/lua).

## Script

![Script](images/icons/script.png){.left}  脚本是包含代码的组件, 它控制着游戏对象的行为. 使用脚本可以编写游戏逻辑, 对象交互 (人机交互或者游戏内游戏对象交互). 脚本用 Lua 语言写成. 使用 Defold, 必须要会写 Lua 脚本. 详情请见 [Defold 脚本教程](/manuals/lua).

## Sound

![Sound](images/icons/sound.png){.left} 声音组件用于播放声音. 目前 Defold 支持 WAV 和 Ogg Vorbis 格式的声音文件. 详情请见 [声音教程](/manuals/sound).

## Sprite

![Sprite](images/icons/sprite.png){.left} Sprite 可以使游戏对象显示出图像. 它使用瓷砖图源或者图集资源的数据显示图像. Sprite 也支持逐帧动画. 它常常被用于显示人物, 物品等.

## Texture profiles

![Texture profiles](images/icons/texture-profiles.png){.left} 纹理档案资源文件用于编译时自动处理和压缩图片数据 (Atlas, Tile sources, 3D Cubemaps 和 textures , GUI 等等). 详情请见 [Texture profiles manual](/manuals/texture-profiles).

## Tile map

![Tile map](images/icons/tilemap.png){.left} 瓷砖地图使用瓷砖图源数据建立一层或多层结构的平铺图像. 通常用来作为游戏场景: 背景, 墙, 建筑物和遮挡物等等. 可以指定混合模式显示多层关系. 比如叶子落在地上. 瓷砖也可以动态更换. 比如可以用来制作桥梁被炸毁的效果. 详情请见 [瓷砖地图教程](/manuals/tilemap).

## Tile source

![Tile source](images/icons/tilesource.png){.left} 瓷砖图源由许多相同大小码放整齐的小图组成. 可以使用瓷砖图源创建逐帧动画. 瓷砖图源可以通过图片数据自动生成碰撞形状. 做关卡时碰撞形状可以当作障碍或者与角色产生交互. 瓷砖地图 (以及 Sprite 和 ParticleFX) 之间可以共享图像资源. 注意能用图集别用瓷砖图源. 详情请见 [瓷砖地图教程](/manuals/tilemap).

## Vertex shader

![Vertex shader](images/icons/vertex-shader.png){.left} 顶点着色器用于计算多边形在屏幕上投射的位置. 对于各种可视组件, 比如 sprite, spine 模型 或者 3D 模型, 它们的形状由多边形顶点构成. 顶点着色程序负责处理顶点 (在全局游戏空间) 的位置并且负责计算出每个多边形顶点的在屏幕上的映射位置. 详情请见 [Shader manual](/manuals/shader).
