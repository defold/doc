---
title: Defold glossary
brief: 本手册列出了在Defold工作中遇到的所有内容及其简要描述.
---

# Defold glossary

本词汇表简要介绍了您在Defold中遇到的所有内容.在大多数情况下,您会找到更多深入文档的链接.

## Animation set

![Animation set](images/icons/animationset.png){.left} 动画集资源包含一组.dae文件或其他.animationset文件，从中读取动画。将一个.animationset文件添加到另一个文件中很方便，如果您在多个模型之间共享部分动画集。有关详细信息，请参阅[模型动画手册](/manuals/model-animation/)。

## Atlas

![Atlas](images/icons/atlas.png){.left} 图集是一组单独的图像，出于性能和内存原因被编译成一张较大的图。它们可以包含静态图像或翻页动画图像序列。图集被各种组件使用，以共享图形资源。有关更多信息，请参阅[图集文档](/manuals/atlas)。

## Builtins

![Builtins](images/icons/builtins.png){.left} 内置项目文件夹是一个只读文件夹，包含有用的默认资源。在这里您可以找到默认渲染器、渲染脚本、材质等。如果您需要对这些资源进行自定义修改，只需将它们复制到您的项目中并按照您的需要进行编辑即可。

## Camera

![Camera](images/icons/camera.png){.left} 摄像机组件有助于决定游戏世界的哪些部分应该可见以及应该如何投影。一个常见的用例是将摄像机附加到玩家游戏对象，或者拥有一个带有摄像机的独立游戏对象，通过某种平滑算法跟随玩家移动。有关更多信息，请参阅[摄像机文档](/manuals/camera)。

## Collision object

![Collision object](images/icons/collision-object.png){.left} 碰撞对象是扩展游戏对象物理属性（如空间形状、重量、摩擦力和恢复力）的组件。这些属性决定了碰撞对象应该如何与其他碰撞对象碰撞。最常见的碰撞对象类型是运动学对象、动态对象和触发器。运动学对象提供您必须手动响应的详细碰撞信息，动态对象由物理引擎自动模拟以遵守牛顿物理学定律。触发器是检测其他形状是否已进入或退出触发器的简单形状。有关其工作原理的详细信息，请参阅[物理文档](/manuals/physics)。

## Component

组件用于赋予游戏对象特定的表达和/或功能，如图形、动画、编码行为和声音。它们没有自己的生命，必须包含在游戏对象内。Defold中有多种类型的组件可用。有关组件的描述，请参阅[构建块手册](/manuals/building-blocks)。

## Collection

![Collection](images/icons/collection.png){.left} 集合是Defold创建模板的机制，或在其他引擎中称为"prefabs"，其中游戏对象的层次结构可以被重用。集合是包含游戏对象和其他集合的树结构。集合始终存储在文件中，并通过在编辑器中手动放置或通过生成动态地引入游戏。有关集合的描述，请参阅[构建块手册](/manuals/building-blocks)。

## Collection factory

![Collection factory](images/icons/collection-factory.png){.left} 集合工厂组件用于将游戏对象层次结构动态生成到运行中的游戏中。有关详细信息，请参阅[集合工厂手册](/manuals/collection-factory)。

## Collection proxy

![Collection proxy](images/icons/collection-proxy.png){.left} 集合代理用于在应用程序或游戏运行时动态加载和启用集合。集合代理最常见的用例是在游戏进行时加载关卡。有关详细信息，请参阅[集合代理文档](/manuals/collection-proxy)。

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} 立方体贴图是一种特殊类型的纹理，由6种不同的纹理组成，这些纹理映射到立方体的侧面。这对于渲染天空盒和各种反射和光照贴图很有用。

## Debugging

在某个时刻，您的游戏会以意外的方式运行，您需要找出问题所在。学习如何调试是一门艺术，幸运的是，Defold附带了一个内置调试器来帮助您。有关更多信息，请参阅[调试手册](/manuals/debugging)。

## Display profiles

![Display profiles](images/icons/display-profiles.png){.left} 显示配置文件资源文件用于指定GUI布局依赖于方向、纵横比或设备型号。它有助于使您的UI适应任何类型的设备。在[布局手册](/manuals/gui-layouts)中阅读更多内容。

## Factory

![Factory](images/icons/factory.png){.left} 在某些情况下，您无法手动将所有需要的游戏对象放置在集合中，您必须动态地、即时地创建游戏对象。例如，玩家可能会发射子弹，每次按下扳机时都应该动态生成并发射子弹。要动态创建游戏对象（来自预分配的对象池），您可以使用工厂组件。有关详细信息，请参阅[工厂手册](/manuals/factory)。

## Font

![Font file](images/icons/font.png){.left} 字体资源是从TrueType或OpenType字体文件构建的。字体指定了渲染字体的大小以及渲染字体应具有的装饰类型（轮廓和阴影）。字体由GUI和标签组件使用。有关详细信息，请参阅[字体手册](/manuals/font/)。

## Fragment shader

![Fragment shader](images/icons/fragment-shader.png){.left} 这是一个在图形处理器上运行的程序，用于多边形绘制到屏幕时每个像素（片段）的处理。片段着色器的目的是决定每个结果片段的颜色。这是通过计算、纹理查找（一个或多个）或查找和计算的组合来完成的。有关更多信息，请参阅[着色器手册](/manuals/shader)。

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} 手柄资源文件定义了特定手柄设备输入如何映射到特定平台上的手柄输入触发器。有关详细信息，请参阅[输入手册](/manuals/input)。

## Game object

![Game object](images/icons/game-object.png){.left} 游戏对象是游戏世界中的基本构建块。它具有位置、旋转和缩放，并且可以包含提供图形、行为等的组件。游戏对象可以组织成层次结构，其中父游戏对象的变换会影响其子对象。有关游戏对象的描述，请参阅[构建块手册](/manuals/building-blocks)。

## GUI

![GUI](images/icons/gui.png){.left} GUI资源用于创建用户界面。GUI资源包含一个节点树，每个节点可以设置位置、旋转、缩放、大小、颜色、纹理、字体等属性。GUI资源由GUI组件使用。有关详细信息，请参阅[GUI手册](/manuals/gui)。

## GUI script

![GUI script](images/icons/script.png){.left} GUI脚本是一种Lua脚本，用于控制GUI节点的行为。GUI脚本可以控制节点的位置、旋转、缩放、颜色等属性，还可以处理用户输入事件。有关详细信息，请参阅[GUI手册](/manuals/gui)。

## Hot reload

![Hot reload](images/icons/hot-reload.png){.left} 热重载是一项功能，允许您在开发应用程序时更改资源并立即看到结果，而无需重新启动应用程序。这大大提高了开发速度。有关更多信息，请参阅[热重载手册](/manuals/hot-reload)。

## Input binding

![Input binding](images/icons/input-binding.png){.left} 输入绑定资源文件用于将输入设备上的各种输入（如键盘按键、鼠标按钮、游戏手柄按钮或触摸屏上的触摸）映射到一组触发器。例如，键盘上的空格键、游戏手柄上的A按钮和触摸屏上的触摸都可以映射到同一个"jump"触发器。游戏逻辑代码只需关心"jump"触发器，而不必关心具体的输入设备。有关详细信息，请参阅[输入手册](/manuals/input)。

## Label

![Label](images/icons/label.png){.left} 标签组件用于显示文本。标签组件使用字体资源，可以设置文本内容、颜色、大小、对齐方式等属性。有关详细信息，请参阅[GUI手册](/manuals/gui)。

## Library

![Library](images/icons/library.png){.left} 库是Defold编辑器的一部分，用于显示和管理项目中的所有资源文件。有关详细信息，请参阅[编辑器手册](/manuals/editor)。

## Lua language

![Lua](images/icons/lua.png){.left} Lua是一种轻量级、高效的脚本语言，Defold使用Lua作为游戏逻辑编程语言。有关详细信息，请参阅[Lua手册](/manuals/lua)。

## Lua module

![Lua module](images/icons/lua-module.png){.left} Lua模块是包含Lua代码的文件，可以被其他Lua文件引用。有关详细信息，请参阅[Lua手册](/manuals/lua)。

## Material

![Material](images/icons/material.png){.left} 材质资源定义了模型如何渲染。材质包含着色器程序和渲染状态。有关详细信息，请参阅[材质手册](/manuals/material)。

## Message

![Message](images/icons/message.png){.left} 消息是Defold中对象间通信的机制。游戏对象可以通过发送消息来与其他游戏对象或组件通信。有关详细信息，请参阅[消息手册](/manuals/message)。

## Model

![Model](images/icons/model.png){.left} 模型组件用于显示3D模型。模型组件使用模型资源和材质资源。有关详细信息，请参阅[模型手册](/manuals/model)。

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} 粒子特效组件用于显示粒子特效。粒子特效组件使用粒子特效资源。有关详细信息，请参阅[粒子特效手册](/manuals/particlefx)。

## Profiling

![Profiling](images/icons/profiling.png){.left} 性能分析是用于找出游戏性能瓶颈的工具。有关详细信息，请参阅[性能分析手册](/manuals/profiling)。

## Render

![Render](images/icons/render.png){.left} 渲染文件包含把游戏渲染到屏幕所需的设置和参数。渲染文件决定了使用哪个渲染脚本和哪个材质资源。有关详细信息，请参阅[渲染手册](/manuals/render/)。

## Render script

![Render script](images/icons/render-script.png){.left} 渲染脚本是一种Lua脚本，用于控制渲染过程。渲染脚本可以设置渲染目标、视口、清屏颜色等属性。有关详细信息，请参阅[渲染手册](/manuals/render)。

## Script

![Script](images/icons/script.png){.left} 脚本是一种Lua脚本，用于控制游戏对象的行为。脚本可以处理输入事件、发送消息、修改游戏对象属性等。有关详细信息，请参阅[脚本手册](/manuals/script)。

## Sound

![Sound](images/icons/sound.png){.left} 声音组件用于播放声音。目前 Defold 支持 WAV 和 Ogg Vorbis 格式的声音文件。有关详细信息，请参阅[声音手册](/manuals/sound)。

## Sprite

![Sprite](images/icons/sprite.png){.left} 精灵组件用于显示2D图像。精灵组件使用图集资源和材质资源。有关详细信息，请参阅[精灵手册](/manuals/sprite)。

## Texture profiles

![Texture profiles](images/icons/texture-profiles.png){.left} 纹理配置文件资源用于定义在不同平台和设备上如何优化纹理。有关详细信息，请参阅[纹理配置文件手册](/manuals/texture-profiles)。

## Tile map

![Tile map](images/icons/tile-map.png){.left} 瓦片地图组件用于显示2D瓦片地图。瓦片地图组件使用瓦片地图资源和瓦片图源资源。有关详细信息，请参阅[瓦片地图手册](/manuals/tile-map)。

## Tile source

![Tile source](images/icons/tilesource.png){.left} 瓦片图源资源用于定义瓦片地图中使用的瓦片。瓦片图源资源使用图像资源。有关详细信息，请参阅[瓦片图源手册](/manuals/tile-source)。

## Vertex shader

![Vertex shader](images/icons/vertex-shader.png){.left} 顶点着色器是一种运行于显卡上的用于处理多边形顶点的渲染程序。顶点着色器可以修改顶点的位置、颜色、纹理坐标等属性。有关详细信息，请参阅[着色器手册](/manuals/shader)。
