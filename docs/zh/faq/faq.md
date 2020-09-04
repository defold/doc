---
title: Defold 引擎与编辑器常见问题和解答
brief:有关 Defold 游戏引擎和编辑器及平台的常见问题和解答.
---

# 常见问题

## 一般常见

#### 问: Defold 真的免费吗?

答: 对, Defold 引擎与编辑器和所有功能完全免费. 没有暗扣费, 手续费和使用权费用. 完全免费.


#### 问: Defold 基金会为什么开发并免费提供 Defold?

答: [Defold 基金会](/foundation) 的一大目标就是让 Defold 软件能够被世界上所有开发者免费使用并且源码也是公开免费的.


#### 问: Defold 能持续维护多久?

答: 我们承诺维护 Defold. [Defold 基金会](/foundation) 的成立就是为了保证 Defold 能够被持续维护. 我们不会放弃.


#### 问: 专业开发的话 Defold 值得信赖吗?

答: 必须值得信赖. Defold 已被越来越多的职业开发者和工作室所采用. 可以参考位于 [游戏展示页](/showcase) 上的用 Defold 开发的各种样例.


#### 问: 你们做了什么样的用户跟踪?

答: 我们的网站和 Defold 编辑器会使用匿名回报一些数据用以提升我们的服务和产品质量. 你编译出版的游戏里不带任何用户跟踪 (除非你自己加入分析服务功能). 详情请见我们的 [隐私政策](/privacy-policy).


#### 问: 谁制作了 Defold?

答: Defold 由 Ragnar Svensson 和 Christian Murray 开发. 他们从2009年就开始了游戏引擎, 编辑器和配套服务的开发. King 和 Defold 在2013年建立了合作关系然后并于2014年获得 Defold. 详情请见 [这里](/about).


## 平台相关

#### 问: Defold 可以运行在哪些平台上?

答: 下表列出了编辑器工具与游戏引擎运行环境的支持情况:

  | 系统                        | 支持                  |
  | -------------------------- | -------------------- |
  | macOS 10.7 Lion            | 编辑器与游戏引擎        |
  | Windows Vista              | 编辑器与游戏引擎        |
  | Ubuntu 18.04 (64 bit)(1)   | 编辑器                |
  | Linux (64 bit)(2)          | 游戏引擎              |
  | iOS 8.0                    | 游戏引擎              |
  | Android 4.1 (API level 16) | 游戏引擎              |
  | HTML5                      | 游戏引擎              |

  (1 编辑器在 64-bit Ubuntu 18.04 平台上通过编译和测试. 其他版本应该同样可以运行但是未经过测试.)

  (2 游戏引擎在大多数 64-bit Linux 版本上只要更新显卡驱动支持 OpenGL ES 2.0 的基本都能运行.)


#### 问: 运行编辑器需要什么硬件系统?

答: 编辑器最多占用 75% 的空闲系统内存. 一般 4 GB 内存的电脑就可以运行 Defold 小项目了. 中大型项目建议配备 6 GB 或更多内存.


#### 问: Defold 能输出哪些平台的游戏?

答: 可以一键发布 任天堂 Switch, iOS, Android 和 HTML5 游戏, 外加 macOS/OS X, Windows 和 Linux 游戏. 真正的一套代码平台通用.


#### 问: Defold 基于何种渲染引擎?

A: Defold 使用 OpenGL ES 2.0 进行图像渲染, 全平台有效. （如果平台渲染引擎更新, Defold引擎也会随之更新）


#### 问: Defold 能做 3D 游戏吗?

答: 可以! 游戏引擎纯 3D. 然而, 工具都是针对 2D 游戏设计的, 所以 3D 游戏工具你得自己开发. 提升 3D 支持的计划进行中.


#### 问: Defold 游戏开发用什么语言?

答: Defold 项目游戏逻辑基本使用 Lua 语言 (特指 Lua 5.1/LuaJIT, 详情请见 [Lua 教程](/manuals/lua)). Lua 是一种强大快速的动态语言. 同时也支持使用原生 (C/C++, Objective-C, Java 和 JavaScript等) 语言来扩展 Defold 引擎功能. 自定义材质, 使用 OpenGL ES SL 语言编写的顶点和片元着色程序.


#### 问: 如何获取 Defold 版本信息?

答: 点击菜单栏 "About" 项. 弹出窗口详细列出了 Defold 版本号, 和文件哈希 SHA1. 对于游戏引擎版本, 调用 [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info) 获取.

最新测试版位于 http://d.defold.com/beta 可以查看 http://d.defold.com/beta/info.json (正式版同样也有: http://d.defold.com/stable/info.json) 文件获取最新版本信息.


#### 问: 运行时如何获取系统信息?

答: 调用 [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info) 获取.


#### 问: Defold 测试版会自动更新吗?

答: Defold 测试版编辑器会在启动时检查并自动更新, 正式版也是.


## 发布相关

#### 问: 我想把游戏发布到 AppStore. 如何设置 IDFA?

答: 提交游戏时, Apple 为广告商提供了3种 IDFA 用例:

  1. 应用内展示广告
  2. 用广告提升安装量
  3. 用广告提升点击量

  如果选择第一个, 编辑会在你的游戏里找广告. 如果没找到, 游戏很可能会被拒. Defold 本身不使用广告商id.


#### 问: 怎么用游戏获利?

答: Defold 支持游戏内付费和多种广告服务. 最新相关信息详见 [资源中心的盈利类目](https://defold.com/tags/stars/monetization/).


## Defold 报错

#### 问: 编辑器不启动, 项目不加载?

答: 检查 Defold 安装路径里是否有空格. 比如, 把编辑器放在mac系统 *Applications* 中的 *Defold-macosx* 文件夹里, 就能运行.  改成 *Defold macosx* 就无法运行. 在 Windows 上, 像 *C:\\Program Files\\* 这样的路径都不行. 这归因于系统架构的一个bug.


#### 问: 游戏无法启动也没有报错. 怎么办?

答: 如果二次编译不通过很肯能由你最后做的改动导致. 从菜单栏选择 *Project > Rebuild And Launch* 试试.


#### 问: 启动 Defold 时报了 Java 相关的错?

答: `javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target`

这个错是由于编辑器尝试建立 https 连接而服务器证书无法验证导致.

详情请见 [这里](https://github.com/defold/editor2-issues/blob/master/faq/pkixpathbuilding.md).


## Linux
:[Linux 问答](../shared/linux-faq.md)


## Android
:[Android 问答](../shared/android-faq.md)


## HTML5
:[HTML5 问答](../shared/html5-faq.md)


## Windows
:[Windows 问答](../shared/windows-faq.md)

## Nintendo Switch
:[Nintendo Switch 问答](../shared/nintendo-switch-faq.md)


## 游戏内容相关

#### 问: Defold 里有 prefab 吗?

A: 有. Defold 里叫 [集合](/manuals/building-blocks/#collections). They allow you to create complex game object hierarchies and store those as a separate building blocks that you can instance in the editor or at runtime (through collection spawning). For GUI nodes there is support for GUI templates.


#### Q: I can't add a game object as a child to another game object, why?

A: Chances are that you try to add a child in the game object file and that is not possible. To understand why, you have to remember that parent-child hierarchies are strictly a _scene-graph_ transform hierarchy. A game object that has not been placed (or spawned) into a scene (collection) is not part of a scene-graph and can't therefore be part of a scene-graph hierarchy.


#### Q: Why can't I broadcast messages to all children of a game object?

A: Parent-child relations express nothing else than the scene-graph transform relations and should not be mistaken for object orientation aggregates. If you try to focus on your game data and how to best transform it as your game alter its state you will likely find less need to send messages with state data to many objects all the time. In the cases where you will need data hierarchies, these are easily constructed and handled in Lua.


#### Q: Why am I experiencing visual artifacts around the edges of my sprites?

A: That is a visual artifact called "edge bleeding" where the edge pixels of neighboring pixels in an atlas bleed into the image assigned to your sprite. The solution is to pad the edge of your atlas images with extra row(s) and column(s) of identical pixels. Luckily this can be done automatically by the atlas editor in Defold. Open your atlas and set the *Extrude Borders* value to 1.


#### Q: Can I tint my sprites or make them transparent, or do I have to write my own shader for it?

A: The built-in sprite shader that is used by default for all sprites has a constant "tint" defined:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  sprite.set_constant("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: If I set the z coordinate of a sprite to 100 then it's not rendered. Why?

A: The Z-position of a game object controls rendering order. Low values are drawn before higher values. In the default render script game objects with a depth ranging between -1 and 1 are drawn, anything lower or higher will not be drawn. You can read more about the rendering script in the official [Render documentation](/manuals/render). On GUI nodes the Z value is ignored and does not affect rendering order at all. Instead nodes are rendered in the order they are listed and according to child hierarchies (and layering). Read more about gui rendering and draw call optimization using layers in the official [GUI documentation](/manuals/gui).


#### Q: Would changing the view projection Z-range to -100 to 100 impact performance?

A: No. The only effect is precision. The z-buffer is logarithmic and have very fine resolution of z values close to 0 and less resolution far away from 0. For instance, with a 24 bit buffer the values 10.0 and 10.000005 can be differentiated whereas 10000 and 10005 cannot.


#### Q: There is no consistency to how angles are represented, why?

A: Actually there is consistency. Angles are expressed as degrees everywhere in the editor and the game APIs. The math libs use radians. Currently the convention breaks for the `angular_velocity` physics property that is currently expressed as radians/s. That is expected to change.


#### Q: When creating a GUI box-node with only color (no texture), how will it be rendered?

A: It is just a vertex colored shape. Bear in mind that it will still cost fill-rate.


#### Q: If I change assets on the fly, will the engine automatically unload them?

A: All resources are ref-counted internally. As soon as the ref-count is zero the resource is released.


#### Q: Is it possible to play audio without the use of an audio component attached to a game object?

A: Everything is component-based. It's possible to create a headless game object with multiple sounds and play sounds by sending messages to the sound-controller object.


#### Q: Is it possible to change the audio file associated with an audio component at run time?

A: In general all resources are statically declared with the benefit that you get resource management for free. You can use [resource properties](/manuals/script-properties/#resource-properties) to change which resource that is assigned to a component.


#### Q: Is there a way to access the physics collision shape properties?

A: No, it is currently not possible.


#### Q: Is there any quick way to render the collision objects in my scene? (like Box2D's debugdraw)

A: Yes, set *physics.debug* flag in *game.project*. (Refer to the official [Project settings documentation](/manuals/project-settings/#debug))


#### Q: What are the performance costs of having many contacts/collisions?

A: Defold runs a modified version of Box2D in the background and the performance cost should be quite similar. You can always see how much time the engine spends on physics by bringing up the [profiler](/manuals/debugging). You should also consider what kind of collisions objects you use. Static objects are cheaper performance wise for instance. Refer to the official [Physics documentation](/manuals/physics) in Defold for more details.


#### Q: What's the performance impact of having many particle effect components?

A: It depends on if they are playing or not. A ParticleFx that isn't playing have zero performance cost. The performance implication of a playing ParticleFx must be evaluated using the profiler since its impact depends on how it is configured. As with most other things the memory is allocated up front for the number of ParticleFx defined as max_count in game.project.


#### Q: How do I receive input to a game object inside a collection loaded via a collection proxy?

A: Each proxy loaded collection has their own input stack. Input is routed from the main collection input stack via the proxy component to the objects in the collection. This means that it's not enough for the game object in the loaded collection to acquire input focus, the game object that _holds_ the proxy component need to acquire input focus as well. See the [Input documentation](/manuals/input) for details.


#### Q: Can I use string type script properties?

A: No. Defold supports properties of [hash](/ref/builtins#hash) types. These can be used to indicate types, state identifiers or keys of any kind. Hashes can also be used to store game object id's (paths) although [url](/ref/msg#msg.url) properties are often preferable since the editor automatically populate a drop-down with relevant URLs for you. See the [Script properties documentation](/manuals/script-properties) for details.


#### Q: How do I access the individual cells of a matrix (created using [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) or similar)?

A: You access the cells using `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` etc


#### Q: I am getting `Not enough resources to clone the node` when using [gui.clone()](/ref/gui/#gui.clone:node) or [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

A: Increase the `Max Nodes` value of the gui component. You find this value in the Properties panel when selecting the root of the component in the Outline.


## The forum

#### Q: Can I post a thread where I advertise my work?

A: Of course! We have a special ["Work for hire" category](https://forum.defold.com/c/work-for-hire) for that. We will always encourage everything which benefits the community, and offering your services to the community---for remuneration or not---is a good example of that.


#### Q: I made a thread and added my work—can I add more?

A: In order to reduce bumping of "Work for hire" threads, you may not post more than once per 14 days in your own thread (unless it’s a direct reply to a comment in the thread, in which case you may reply). If you want to add additional work to your thread within the 14-day period, you must edit your existing posts with your added content.


#### Q: Can I use the Work for Hire category to post job offerings?

A: Sure, knock yourselves out! It can be used for offerings as well as requests, e.g. “Programmer looking for 2D pixel artist; I’m rich and I’ll pay you well”.
