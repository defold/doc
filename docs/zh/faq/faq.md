---
title: Defold 引擎与编辑器常见问题和解答
brief: 有关 Defold 游戏引擎和编辑器及平台的常见问题和解答.
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


#### 问: Defold 能做 3D 游戏吗?

答: 可以! 游戏引擎纯 3D. 然而, 工具都是针对 2D 游戏设计的, 所以 3D 游戏工具你得自己开发. 提升 3D 支持的计划进行中.


#### 问: Defold 游戏开发用什么语言?

答: Defold 项目游戏逻辑基本使用 Lua 语言 (特指 Lua 5.1/LuaJIT, 详情请见 [Lua 教程](/manuals/lua)). Lua 是一种强大快速的动态语言. 同时也支持使用原生 (C/C++, Objective-C, Java 和 JavaScript等) 语言来扩展 Defold 引擎功能. 自定义材质, 使用 OpenGL ES SL 语言编写的顶点和片元着色程序.


## 平台相关

#### 问: Defold 可以运行在哪些平台上?

答: 下表列出了编辑器工具与游戏引擎运行环境的支持情况:

  | 系统                        | 支持                  |
  | -------------------------- | -------------------- |
  | macOS 10.12 Sierra         | 编辑器                |
  | macOS 10.7 Lion            | 游戏引擎               |
  | Windows Vista              | 编辑器与游戏引擎        |
  | Ubuntu 18.04 (64 bit)(1)   | 编辑器                |
  | Linux (64 bit)(2)          | 游戏引擎              |
  | iOS 9.0                    | 游戏引擎              |
  | Android 4.4 (API level 19) | 游戏引擎              |
  | HTML5                      | 游戏引擎              |

  (1 编辑器在 64-bit Ubuntu 18.04 平台上通过编译和测试. 其他版本应该同样可以运行但是未经过测试.)

  (2 游戏引擎在大多数 64-bit Linux 版本上只要更新显卡驱动支持 OpenGL ES 2.0 的基本都能运行.)


#### 问: Defold 能输出哪些平台的游戏?

答: 可以一键发布 任天堂 Switch, iOS, Android 和 HTML5 游戏, 外加 macOS, Windows 和 Linux 游戏. 真正的一套代码平台通用.


#### 问: Defold 基于何种渲染引擎?

A: Defold 在 HTML5 中使用 WebGL, iOS 和 macOS 中使用 Metal, 其他平臺中使用 Vulkan 或者 OpenGL ES 2.0. 作爲開發者只需要關心可編程渲染管綫所支持的一種渲染 API 即可.


#### 问: 如何获取 Defold 版本信息?

答: 点击菜单栏 "About" 项. 弹出窗口详细列出了 Defold 版本号, 和文件哈希 SHA1. 对于游戏引擎版本, 调用 [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info) 获取.

最新测试版位于 http://d.defold.com/beta 可以查看 http://d.defold.com/beta/info.json (正式版同样也有: http://d.defold.com/stable/info.json) 文件获取最新版本信息.


#### 问: 运行时如何获取系统信息?

答: 调用 [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info) 获取.


## 編輯器相關
:[Editor FAQ](../shared/editor-faq.md)


## Linux 相關
:[Linux FAQ](../shared/linux-faq.md)


## Android 相關
:[Android FAQ](../shared/android-faq.md)


## HTML5 相關
:[HTML5 FAQ](../shared/html5-faq.md)


## IOS 相關
:[iOS FAQ](../shared/ios-faq.md)


## Windows 相關
:[Windows FAQ](../shared/windows-faq.md)


## Consoles 相關
:[Consoles FAQ](../shared/consoles-faq.md)

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


#### 问: 游戏无法启动也没有报错. 怎么办?

答: 如果二次编译不通过很肯能由你最后做的改动导致. 从菜单栏选择 *Project > Rebuild And Launch* 试试.


## 游戏内容相关

#### 问: Defold 里有 prefab 吗?

答: 有. Defold 里叫 [集合](/manuals/building-blocks/#collections). 它能帮助建立储存游戏内容为树形结构以便在编辑器或者游戏运行时创建实例. 对于 GUI 节点类似结构称为 GUI 模板.


#### 问: 为什么我不能在游戏对象下建立子游戏对象?

答: 有一种可能是因为父级游戏对象是一个文件引用. 对于父子结构的游戏对象来说它们的位移关系通过 _场景结构_ 表达. 没有被加入到场景里的游戏对象无法于其他对象建立父子关系.


#### 问: 为什么我不能在所有子游戏对象间广播消息?

答: 父子关系除了场景结构中表现相对位移以外别无其他特别之处. 如果需要跟踪子对象状态无需时刻向所有子对象发送消息. 这种情况下你需要使用 Lua 编写数据结构.


#### 问: 精灵对象周围出现黑白边?

答: 这被称作 "边缘出血" 现象, 渲染精灵对象的时候把纹理旁边的一些像素也加入进来了. 解决办法是用纹理边缘的像素再扩充一圈. 好在 Defold 编辑器有工具能自动做这件事. 尝试打开图集并且设置 *Extrude Borders* 的值为 1.


#### 问: 精灵变色, 透明效果如何制作?

A: 精灵默认着色程序包含 "tint" 属性:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  sprite.set_constant("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### 问: 为什么游戏对象的z值设为100就看不见了?

答: z值表示深度方向的遮挡关系. z值小的位于z值大的游戏对象前面. 默认渲染程序的z值范围是 -1 到 1, 此范围之外的不被渲染. 关于渲染脚本详情请见 [渲染教程](/manuals/render). 对于 GUI 节点来说z值毫无作用. 节点的遮挡顺序取决于树形结构 (以及层次设置). 关于用户界面节点的渲染详情请见 [GUI 教程](/manuals/gui).


#### 问: 要是把视口深度范围设为 -100 到 100 会影响性能吗?

答: 不影响性能但是影响精度. z缓存是一种对数结构靠近 0 差别明显, 远离 0 差别不明显. 比如说, 用 24 位缓存 10.0 对比 10.000005 区别明显但是 10000 对比 10005 区别不明显.


#### 问: 角度的单位为什么不一致?

答: 实际上一致. 编辑器和游戏API使用角度制. 数学计算库使用弧度制. 目前对于物理 `angular_velocity` 是个例外使用了弧度制. 以后可能会矫正.


#### 问: 只有颜色没有纹理的GUI节点如何渲染?

答: 作为顶点着色形状渲染, 注意其性能消耗.


#### 问: 如何释放资源所占用的内存?

答: 引擎对所有资源都有引用计数. 一旦引用为0则资源自动被释放.


#### 问: 不用游戏对象能播放声音吗?

答: 游戏引擎设计模式基于组件. 可以建立一个不可见游戏对象把声音组件放入然后需要播放时给它发消息即可.


#### 问: 运行时声音组件播放的声音文件能更改吗?

答: 一般资源都是静态声明随意管理的. 可以使用 [资源属性](/manuals/script-properties/#resource-properties) 来修改与组件关联的资源.


#### 问: 存取物理碰撞形状属性的方法?

答: 目前尚未支持.


#### 问: 有办法快速渲染物理碰撞对象吗? (就像 Box2D 的 debugdraw 那样)

答: 有, 要在 *game.project* 里设置 *physics.debug* 项. (参见 [项目设置教程](/manuals/project-settings/#debug))


#### 问: 许多物理碰撞的主要性能消耗在哪里?

答: Defold 包含的是 Box2D 略微修改版本, 所以性能应该和原版差不多. 可以使用 [调试器](/manuals/debugging) 跟踪物理碰撞数量. 确保用对碰撞对象. 比如静态碰撞对象性能高些. 详情请见 Defold 的 [物理教程](/manuals/physics).


#### 问: 如果有许多粒子效果, 对性能影响大不大?

答: 这取决于粒子效果是否正在播放. 没有播放的粒子效果不消耗性能. 播放中的粒子效果性能消耗取决于其配置情况, 可以用调试器来观察. 粒子效果的内存消耗基本上取决于项目设置的 max_count 数.


#### 问: 如何得到集合代理加载的集合里的游戏对象的输入信息?

答: 每个集合都有自己的输入栈. 输入从主集合通过代理组件传递到被载入集合里的游戏对象. 换句话说仅游戏对象获得输入焦点是不够的, 那个代理组件 _所在的_ 游戏对象同样需要获得输入焦点. 详情请见 [输入教程](/manuals/input).


#### 问: 脚本属性有字符串类型的吗?

答: 没有. Defold 只有 [哈希](/ref/builtins#hash) 类型的脚本属性. 用来表示枚举, 表示状态, 表示各种类型都没问题. 而且游戏对象的 id (路径) 也是用其 [url](/ref/msg#msg.url) 属性的哈希来保存, 遇到这样的属性时编辑器会自动建立相关路径弹框供你选择. 详情请见 [脚本属性教程](/manuals/script-properties).


#### 问: 如何存取矩阵 (使用 [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) 之类的函数生成的) 内部数据?

答: 使用 `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` 之类的属性可以访问内部数据.


#### 问: 使用 [gui.clone()](/ref/gui/#gui.clone:node) 或 [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) 时报 `Not enough resources to clone the node` 的错误信息?

答: 增加gui组件的 `Max Nodes` 值. 在大纲视图gui根节点的属性面板上就能看到.


## 论坛相关

#### 问: 我能在论坛上打广告吗?

答: 可以! 论坛有一个 ["Work for hire" 类目](https://forum.defold.com/c/work-for-hire). 能充实社区论坛的所有信息都欢迎, 这里可以发布求职广告.


#### 问: 可以无限打广告?

答: 为避免 "Work for hire" 类目论坛被爆, 至少14天内不许再加广告 (除非有人回复找你, 此时你可以立即回复这个人). 14天内, 只能通过更新帖子的方式加入新内容.


#### 问: 我能发布招聘广告吗?

答: 可以, 自己找! 招聘也行求职也行, 比如 “程序员找美工; 高价求不差钱”.
