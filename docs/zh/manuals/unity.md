---
title: 面向 Unity 用户的 Defold
brief: 如果你已有 Unity 经验，本指南可以帮助你快速切换到 Defold。它介绍 Unity 中常见的一些关键概念，并说明 Defold 中对应的工具和方法。
---

# 面向 Unity 用户的 Defold

如果你已有 Unity 经验，本指南可以帮助你快速上手 Defold。它聚焦于必要概念，并在需要更深入细节时指向官方 Defold 手册。

## 简介

Defold 是一个完全免费的、真正跨平台的 3D 游戏引擎，并提供适用于 Windows、Linux 和 macOS 的编辑器。完整源代码可在 [Github](https://github.com/defold/defold/) 获取。

Defold 注重性能，即使在低端设备上也如此。它使用小型组件模型，许多游戏交互通过代码和消息传递处理。

Defold 比 Unity 小得多。空项目的引擎体积在所有平台上约为 1-3 MB。你可以裁剪掉引擎的额外部分，并把部分游戏内容放入 [Live Update](/manuals/live-update)，以后再单独下载。体积对比以及选择 Defold 的其他原因，可参阅 [Why Defold 页面](https://defold.com/why/)。

要根据自己的需要定制 Defold，你可以编写自己的实现，或使用已有方案：

1. 完全可脚本化的渲染管线（渲染脚本 + 材质/着色器），并可选择少量后端（OpenGL、Vulkan 等）。
2. 通过 Native Extensions（C++/C#）添加代码和组件。
3. 使用 Editor Scripts 和 UI 小部件定制编辑器。
3. 修改引擎和编辑器构建，因为完整源代码和构建管线都是可用的。

我们也建议观看 Game From Scratch 的视频：[Defold for Unity developers](https://www.youtube.com/watch?v=-3CzCbd4QZ0)。

---

## 安装

1. 下载适用于你操作系统的 Defold。
2. 解压并启动。

就是这样。不需要 Hub，不需要额外安装 SDK、工具链或平台包。这就是为什么我们说 Defold 是零配置。

如需更多细节，请阅读这篇简短的[安装手册](/manuals/install/)。

### 版本

Defold 更新频繁，没有 “LTS” 分支。我们建议始终使用最新版本。新版本会定期发布，通常每月一次，并包含大约两周的公开 beta。你可以直接在编辑器中更新 Defold。

---

## 欢迎界面

Defold 会显示一个类似 Unity Hub 的欢迎界面，你可以从这里打开最近的项目：

![Welcome screen comparison](images/unity/unity_defold_start.png)

也可以从以下入口新建项目：

- `Templates` - 面向特定平台或类型的基础空项目，用于快速开始。
- `Tutorials` - 帮助你完成第一步的引导式学习流程。
- `Samples` - 官方或社区贡献的用例和示例。

![Welcome Templates comparison](images/unity/unity_defold_templates.png)

创建第一个项目和/或打开项目后，它会在 Defold Editor 中打开。

## Hello World

这是在 Defold 中快速做出东西的方式。按步骤操作，然后再回来阅读手册其余部分。

1. 从 `Templates` 中选择空项目，在 `Title` 中命名，选择位置，然后点击 `Create New Project` 创建。项目会在 Defold Editor 中打开。
![Hello World Step 1](images/unity/helloworld_1.png)
2. 在左侧 `Assets` 面板中打开 `main` 文件夹，双击 `main.collection` 将其打开。
3. 在右侧 `Outline` 面板中右键点击 `Collection`，选择 `Add Game Object`。
![Hello World Step 2](images/unity/helloworld_2.png)
4. 右键点击创建出的 `go` 游戏对象，选择 `Add Component`，然后选择 `Label`。
![Hello World Step 3](images/unity/helloworld_3.png)
5. 在左下方的 `Properties` 面板中，在 `Text` 属性里输入一些文字。
6. 在中央主场景视图中拖动标签，将它放到大约 `(480,320,0)` 的位置，或在 `Properties` 的 `Position` 中修改。
![Hello World Step 4](images/unity/helloworld_4.png)
7. 修改标签位置后，点击 `File` -> `Save All` 保存项目，或使用快捷键 <kbd>Ctrl</kbd>+<kbd>S</kbd>（Mac 上为 <kbd>Cmd</kbd>+<kbd>S</kbd>）。
8. 点击 `Project` -> `Build` 构建项目，或使用快捷键 <kbd>Ctrl</kbd>+<kbd>B</kbd>（Mac 上为 <kbd>Cmd</kbd>+<kbd>B</kbd>）。
![Hello World Step 5](images/unity/helloworld_5.png)

你刚刚构建了自己的第一个 Defold 项目，并应该能在窗口中看到文字。游戏对象和组件的概念对你应该很熟悉。下面会解释集合、轮廓、属性，以及为什么需要把标签稍微往右上方移动。

---

## Defold Editor 概览

这里会从 Unity 用户最先想了解的角度介绍 Defold Editor，不过我们也建议之后阅读完整的[编辑器概览手册](/manuals/editor-overview)。

### 编辑器对比

Unity 和 Defold 的第一个明显差异是默认编辑器布局。下面展示的 Unity Editor 布局经过轻微调整，以便与 Defold 的默认布局对应。两者并排放置，方便直观比较主要面板，也更容易识别 Unity 中熟悉的标签页。

![Editor Comparison](images/unity/defold_unity_editor.png)

默认情况下，Defold Editor 会以 2D 正交预览打开。如果你要开发 3D 项目，或只是希望体验更接近 Unity，建议在工具栏中取消勾选 `2D`，并勾选 `Perspective` 将相机投影切换为透视投影：

![Defold Toolbar](images/unity/defold_2d.png)

你也可以在工具栏中调整 `Grid Settings`，让网格使用与 Unity 类似的 `Y` 平面：

![Defold 3D settings](images/unity/defold_3d.png)

### Defold 面板概览

Defold Editor 分为 6 个主要面板。

![Editor 2](images/editor/editor_overview.png)

下面比较 Defold 的命名和功能差异：

| Defold | Unity | 差异 |
|---|---|---|
| 1. Assets | Project (Assets Browser) | 在 Defold 中，Assets 面板停靠在左侧。Defold 不会创建任何 `meta` 文件。 |
| 2. Main Editor | Scene View | Defold Editor 是上下文相关的，不同文件类型有不同编辑器；Unity 则使用独立的专用窗口（如 Animator、Shader Graph）。Defold 也内置了代码编辑器。 |
| 3. Outline | Hierarchy | Defold 只显示当前打开的文件或所选元素（游戏对象或组件），不是全局层级。 |
| 4. Properties | Inspector | Defold 只显示 **Outline 中当前选择项** 的属性，不会一次显示游戏对象上的所有组件。 |
| 5. Tools | Console | Defold 提供 Console、Curve Editor、Build Errors、Search Results、Breakpoints 和 Debugger 等标签页工具。 |
| 6. Changed Files | Unity Version Control (Plastic) | 在 Defold 中，一旦 Git 集成到项目中，修改过的文件会显示在这里。你仍然可以在外部使用 Git。 |

其他与编辑器相关的常用命名：

| Defold | Unity | 差异 |
|---|---|---|
| Game Build | Game Preview | 显示由引擎构建并运行的游戏。Defold 可以从编辑器运行多个游戏实例，类似 Unity 6+ Multiplayer Play Mode。Defold 的游戏始终在单独窗口中运行，而不是停靠在编辑器内。Defold 也可以在外部设备上运行游戏（例如手机），类似 Unity Remote。 |
| Tabs | Tabs | Defold 允许在 Main Editor 中并排编辑两个面板。标签页和面板停靠在同一个编辑器窗口内；面板可见性可切换（<kbd>F6</kbd>、<kbd>F7</kbd>、<kbd>F8</kbd>），面板大小也可调整。 |
| Toolbar | Toolbar / Scene View Options | 只有较新的 Unity 版本才把变换工具移入 Scene 视图，这一点与 Defold 类似。 |
| Console | Console | Defold Console 不能分离。Defold 中的构建错误会出现在单独的 `Build Errors` 标签页。 |
| Build Errors | Compilation Errors in Console | Lua 脚本是解释执行的，因此没有编译错误。不过项目构建过程中仍可能出现错误。Defold 也使用 Lua Language Server 对脚本进行静态分析。 |
| Search Results | Search / Project Search | Defold 中没有按类型和标签过滤的功能。 |
| Curve Editor | Unity Curve Editor | Defold Curve Editor 只允许编辑粒子效果属性的曲线。 |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | Debugger 开箱即用并完全集成在 Defold 中。还有一个额外标签页用于跟踪、启用和禁用断点。 |

---

## 关键概念

从足够抽象的角度看，大多数游戏引擎背后的关键概念都很相似。它们的目标都是帮助开发者更轻松地构建游戏，就像搭积木一样，同时自行处理复杂和平台相关的任务。

### 构建块

Defold 只使用少量基础构建块：

![Building blocks](images/unity/blocks.png)

更多细节请参阅完整的 [Defold 构建块手册](/manuals/building-blocks/)。

### 游戏对象

Defold 使用类似 Unity 的 **"Game Objects"**。在两个引擎中，游戏对象都是带 ID 的数据容器，并且都拥有变换：位置、旋转和缩放。不过在 Defold 中，变换是内置的，而不是一个单独组件。

你可以在游戏对象之间创建父子关系。在 Defold 中，这只能在编辑器内的 "Collection"（下文会解释）中完成，或在脚本中动态完成。游戏对象不能像 Unity 那样把其他游戏对象作为嵌套对象直接包含在内部。

### 组件

在两个引擎中，Game Objects 都可以通过 **"Components"** 扩展。Defold 提供一组精简的核心组件。它对 2D 和 3D 的区分比 Unity 少（例如碰撞体），因此整体组件更少，你可能会缺少一些 Unity 中熟悉的组件。

#### 行为组件

在 Unity 中，"component" 通常指附加到 `GameObject` 的 `MonoBehaviour`。你可以继承 `MonoBehaviour` 创建自己的组件，也可以使用 Unity 内置组件，例如 Light、一些物理组件等。

在 Defold 中，Component 专指 Unity 内置组件的大致对应物。Defold 不会把脚本当作 MonoBehaviour，也不需要通过显式“标记”来把脚本附加到游戏对象上；你只需要创建事件监听函数/回调。

自定义游戏行为通常不会作为多个单独的脚本组件添加到同一个游戏对象上。更常见的做法是把它实现为 Lua 模块，由一个宿主 `.script` 使用，或由一个更大的系统脚本控制许多对象。下面的代码编写部分会更详细说明。

更多内容请阅读 [Defold Components 手册](/manuals/components/)。

下表列出类似的 Unity 组件，便于快速查找，并附有各 Defold 组件手册链接：

| Defold | Unity | 差异 |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | 在 Defold 中，只能通过代码修改 tint（颜色属性）。 |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | Defold 内置 Tilemap Editor，支持方形网格（也有例如 [Hexagon](https://github.com/selimanac/defold-hexagon/) 的扩展），但没有内置自动铺瓦规则。[Tiled](https://defold.com/assets/tiled/)、[TileSetter](https://defold.com/assets/tilesetter/) 或 [Sprite Fusion](https://defold.com/assets/spritefusion/) 等工具可导出到 Defold。 |
| [Label](/manuals/label/) | Text / TextMeshPro | Defold 有用于富文本格式的 [RichText 扩展](https://defold.com/assets/richtext/)（类似 TextMeshPro）。 |
| [Sound](/manuals/sound/) | AudioSource | Defold 只有全局声音源（非空间音频）。Defold 有官方 [FMOD 扩展](https://github.com/defold/extension-fmod)。 |
| [Factory](/manuals/factory/) | Prefab Instantiate() | 在 Defold 中，Factory 是带有特定原型（prefab）的组件。 |
| [Collection Factory](/manuals/collection-factory/) | -（无直接组件对应物） | Defold 中的 Collection Factory 组件可以一次生成多个带父子关系的 Game Objects。 |
| [Collision Object](/manuals/physics-object) | Rigidbody + Collider | 在 Defold 中，物理对象和碰撞形状组合在一个组件中。 |
| [Collision Shapes](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | 在 Defold 中，形状（box、sphere、capsule）配置在 Collision Object 组件内。两者都支持来自 tilemap 和凸包数据的碰撞形状。 |
| [Camera](/manuals/camera/) | Camera | Unity 的相机有更多内置渲染和后处理设置，而 Defold 通过渲染脚本把控制权交给用户。 |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | Defold GUI 是用于构建完整 UI 和模板的强大组件。Unity 没有一个等价的单一 UI 组件，而是有多个 UI 框架。Defold 也有 [ImGui 扩展](https://github.com/britzl/extension-imgui)。 |
| [GUI Script](/manuals/gui-script/) | Unity UI / uGUI scripts | Defold GUI 可通过 GUI scripts 使用专用 `gui` API 控制。 |
| [Model](/manuals/model/) | MeshRenderer + Material | 在 Defold 中，Model 组件包含 3D 模型文件、纹理，以及带着色器的材质。 |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | 在 Defold 中，Mesh 是一个用于通过代码管理顶点集的组件。它类似 Defold Model，但更底层。 |
| [ParticleFX](/manuals/particlefx/) | Particle System | Defold 的粒子编辑器支持带有许多属性的 2D/3D 粒子效果，并可在 Curve Editor 中用曲线随时间动画化。它没有 Trails 或 Collisions。 |
| [Script](/manuals/script/) | Script | 编程差异会在下文详细解释。 |

#### 扩展和自定义组件

Defold 还通过扩展提供官方 [Spine](/manuals/extension-spine/) 和 [Rive](/manuals/extension-rive/) 组件。

你也可以使用 Native Extensions 创建自己的[自定义组件](https://github.com/defold/extension-simpledata)，例如这个社区创建的 [Object Interpolation Component](https://github.com/indiesoftby/defold-object-interpolation)。

有些 Unity 组件在 Defold 中没有开箱即用的等价物，例如 Audio Listener、Light、Terrain、LineRenderer、TrailRenderer、Cloth 或 Animator。不过这些功能都可以用脚本实现，而且已有可用方案，例如不同的光照管线、用于生成任意网格（包括地形）的 Mesh 组件，或用于可定制拖尾效果的 [Hyper Trails](https://defold.com/assets/hypertrails/)。Defold 未来也可能添加新的内置组件，例如灯光。

### 资源

有些 Components 需要 **"Resources"**，这与 Unity 类似，例如 sprites 和 models 需要 textures。下面比较其中几个：

| Defold | Unity | 差异 |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | Defold 也有 [Texture Packer 扩展](https://defold.com/extension-texturepacker/)。 |
| [Tile source](/manuals/tilesource/) | Tile Palette + Asset | 在 Defold 中，tile source 可作为 tilemap 的纹理，也可用于 sprites 或 particles。 |
| [Font](/manuals/font/) | Font | 由 Defold Label 组件或 GUI 中的文本节点使用，类似 Unity 中的 Text/TextMeshPro。 |
| [Material](/manuals/material/) | Material | 在 Defold 中，着色器被称为 vertex program 和 fragment program。 |

### Collection 与 Scene

在 Defold 中，Game Objects 和 Components 可以像 Unity prefabs 一样放在独立文件中，也可以定义在一个组合用的 **"Collection"** 文件里。

Defold 中的 Collection 本质上是带有静态场景描述的文本文件。它**不是**运行时对象。它只定义游戏中应实例化哪些 Game Objects，以及这些对象之间应如何建立父子关系。

#### 游戏世界

Unity scenes 默认共享同一个全局游戏状态和同一个物理模拟，实际上就是同一个 *world*。在 Defold 中，你有两个选择：

1. 通过 `Factory` 从单个游戏对象文件实例化对象，或通过 `Collection Factory` 从集合文件实例化对象，把它们放入一个已经实例化的指定 *world* 中，类似 prefabs。
2. 在运行时创建一个独立的游戏 *world*，它拥有自己的游戏对象、物理世界、引擎操作和寻址命名空间。这个 world 可由启动时加载的集合或 `Collection Proxy` 组件创建。

Factories 和 Proxy 组件也会在后文解释。
更多集合信息请阅读 [Building Blocks 手册](/manuals/building-blocks/#collections)。

---

## 项目资源和资产

Unity 和 Defold 都把游戏内容存储在项目目录中，但它们跟踪和准备资产的方式不同。

### 资产

Unity 把资产放在 `Assets/` 中，并生成 `.meta` 文件。Defold 没有 meta 文件。Defold 项目就是你的文件夹结构，与磁盘上的结构完全一致，`Assets` 面板始终映射该结构。

### 资源格式

Unity 会在后台导入资产，并把它们转换为其他格式。在 Defold 中，你直接使用源资源（`.png`、`.gltf`、`.wav`、`.ogg` 等），并把它们分配给 `Components`。

Unity 可以把单张图片用作 Sprite。在 Defold 中，图片可直接用于 Models/Meshes，但 Sprites/GUI/Tilemaps/Particles 需要 atlas（打包纹理）或 tilesource（基于网格的瓦片）。

大多数 Defold 资源以文本形式存储，对版本控制友好。

### Library 缓存

Unity 会为导入资产生成 `Library/` 文件夹。Defold 没有这样的目录；资产会在构建期间处理，缓存输出位于构建文件夹下，也可使用可选的本地/远程构建缓存。

---

## 代码编写

Defold 中与 `MonoBehaviour` 脚本最接近的是 Script 组件，但有一些值得了解的差异。

### Lua

Defold 脚本使用动态类型、多范式的 [Lua](https://www.lua.org/) 语言编写。

Lua 脚本有几种类型：`*.script`、`*.gui_script`、`*.render_script`、`*.editor_script` 和 `*.lua` 模块。

### Teal

Defold 支持使用输出 Lua 代码的转译器，例如 [Teal](https://teal-language.org/) 这种静态类型 Lua 方言，但此功能更受限，并需要额外配置。详情见 [Teal Extension Repository](https://github.com/defold/extension-teal)。

### C++/C# Native Extensions

Defold Native Extensions 可以使用多种其他语言编写：C、C++、C#、Objective-C、Java 或 JS，具体取决于目标平台。如果你非常熟悉 C#，理论上可以把大部分游戏逻辑组织到 C# 扩展里，再从一个小 Lua 启动脚本调用它，不过这需要较高级的 API 知识，不建议初学者这样做。

更多扩展内容请阅读 [Defold Native Extensions 手册](/manuals/extensions/)。

### 从 MonoBehaviours 到 Lua 模块

Unity 的脚本模型很开放。由于 `MonoBehaviour` 是在编辑器中添加行为的主要方式，许多 Unity 项目会从每个重要 GameObject 一个控制器式脚本开始：`PlayerController`、`EnemyController`、`BulletController`、`GameManager`、`EnemyManager` 等。

Defold 对默认架构更明确。一个游戏对象可以有 `.script`，但你很少需要为每个 Game Object 创建脚本，因为借助 Defold 强大的寻址和消息传递，一个 Defold 脚本可以控制成百上千个其他对象及其组件，而这些对象甚至不需要自己的脚本。按每个 Game Object 创建脚本通常没有必要，还可能带来反效果的复杂度。

对于可复用的游戏行为，Unity 开发者常会转向组合：把 `Health.cs`、`Attack.cs` 或 `EnemyFinder.cs` 这类较小的 `MonoBehaviour` 脚本附加到同一个 GameObject。在 Defold 中，你通常保留一个附加的 `.script` 作为宿主或协调者，并把可复用逻辑放入普通 Lua 模块。

在 Unity 中，这种组合可能如下所示：

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

在 Defold 中，相同职责通常拆分到一个附加脚本和多个可复用模块中：

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

附加的 `.script` 成为宿主或协调者。Lua 模块包含可复用逻辑，类似 Unity 中的小型 `MonoBehaviour` 脚本通常只负责一个职责。

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

重要差异不是 Defold 阻止模块化架构，而是组合发生的位置，以及游戏代码如何通信：

| Unity | Defold |
|---|---|
| 在 Inspector 中附加多个 `MonoBehaviour` 脚本 | 附加一个 `.script`，并在代码中组合 Lua 模块 |
| 使用 `GetComponent<T>()` 或序列化字段连接行为 | 把模块实例存储在 `self` 上，并在对象之间使用地址/消息 |
| 每个组件都可以有自己的生命周期方法 | 宿主脚本分发 `init()`、`update()`、`on_message()`、`final()` 等 |
| 可以使用许多架构风格 | 面向消息、显式代码组合是常见做法 |

如果你习惯在 Inspector 中通过添加组件配置行为，一开始这可能会感觉不太一样。在 Defold 中，许多你在 Unity 里可视化配置的东西，可以改为通过代码创建、连接、启用、禁用或更新。Defold 的消息系统有助于解耦逻辑：发送者把数据发送到一个地址，接收者决定如何处理。

这种方式虽被推荐，但不是强制的。你仍然可以按自己喜欢的方式写脚本，包括为每个游戏对象附加多个脚本，或更接近面向对象风格，也有库可帮助你这样做（[defold-oop](https://github.com/xiyoo0812/defold-oop) 或 [lua-class](https://github.com/d954mas/lua-class)）。

对于许多同类型对象，例如子弹、敌人、粒子、瓦片或简单交互元素，通常最好由系统或管理器脚本控制它们，而不是给每个对象单独添加脚本。当对象确实拥有自己的重要状态和行为时，再使用对象级脚本。需要可复用逻辑时使用模块。当一个脚本能高效控制许多对象时使用系统脚本。

一个展示如何利用 Defold 脚本属性、工厂、寻址和消息传递来控制多个单位的示例可在[这里](https://defold.com/examples/factory/spawn_manager/)找到。

推荐的代码编写手册：

- [Script 手册](/manuals/script/)
- [Writing code](/manuals/writing-code/)
- [Debugging](/manuals/debugging/)

### 内置代码编辑器

Defold Editor 包含内置代码编辑器，支持代码补全、语法高亮、快速文档查找、linting 和内置调试器。

![Defold Code Editor](/images/editor/code-editor.png)

### VS Code 和其他编辑器

如果你愿意，仍然可以使用自己的外部编辑器。所有 Defold 组件和相关文件都是基于文本的，所以可用任何文本编辑器编辑，但必须遵循正确的格式和元素结构，因为它们基于 Protobuf。

如果你习惯 VS Code，并想用它编写游戏代码，建议从 Visual Studio Marketplace 安装 [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) 或 [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide)。

你也可以配置 Defold Editor 偏好设置，让文本文件默认在 VS Code（或其他外部编辑器）中打开。详情见 [Editor Preferences](/manuals/editor-preferences/)。

### Shaders - GLSL

Defold 使用 GLSL（OpenGL Shading Language）编写着色器，即 `Vertex Programs` 和 `Fragment Programs`，这与 Unity 类似。虽然 Defold 没有 Unity 那样的 Shader Graph（这可能是缺点），但你仍然可以通过编写代码创建等价着色器。

更多着色器内容请阅读 [Shaders 手册](/manuals/shader)。

#### 材质

Defold 使用 `Material` 概念连接 `.fp` 和 `.vp` 着色器、采样器（纹理），以及 Vertex Attributes 或 Constants 等其他内容。

更多材质内容请阅读 [Materials 手册](/manuals/material)。

---

## 消息系统

在 Defold 中，对象之间不会保存直接引用。没有 `GetComponent`，脚本之间不会跨对象直接调用方法，也没有像 Unity 那样的全局场景访问。

相反，脚本通过消息传递通信：你向其他脚本发送消息，而不是直接调用方法或访问组件。那些对象如何处理消息，由它们自己决定。

一开始这可能不熟悉，但它鼓励低耦合并减少紧密依赖。

### 发送消息

在 Unity 中，通信通常看起来像这样：

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

因此对象可以直接引用彼此，并调用其他脚本上的方法。所有对象都存在于同一个共享场景空间中。

在 Defold 中，你从一个脚本向另一个脚本（或其他组件）发送消息：

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

并可在脚本中处理这些消息：

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

暂时不用关心 `#` 和 `hash`，后面会解释。其余部分应该很直接。你可以向任何已实例化游戏对象上的任何组件发送消息，甚至可以发送给同一个脚本。

#### 脚本以外的组件

有时你会向 `Sprite` 或 `Collision` 等组件发送消息，例如启用或禁用它们。有时 `Components` 会向你的脚本发送消息，例如发生碰撞时，你可以处理该消息。Defold 内部也使用同一套消息系统处理引擎事件和游戏通信。

消息系统在某种程度上类似 Unity 的 SendMessage 或事件系统，但寻址方式和约定不同。

更多细节请阅读 [Message Passing 手册](/manuals/message-passing/)。

### 寻址

Defold 中的对象和组件通过地址标识，这些地址称为 URL。

每个已实例化对象和组件都有自己的唯一地址，你不需要遍历场景图来查找它们。这让寻址变得显式而直接。

Defold 中的简单 URL 可能如下所示：

```lua
"/player"
```

它在*概念上*类似于：

```c#
GameObject.Find("player")
```

现在可以解释为什么地址中会使用 `"/"` 或 `"#"`。

Defold URL（类似 [URL](https://en.wikipedia.org/wiki/URL)）由三部分组成：

```yaml
socket: /path #fragment
```

或者用 Defold 命名来描述：

```yaml
collection: /gameobject #component
```

上面的描述中添加空格只是为了直观分隔这 3 部分。

简单来说：

1. `collection:` 标识集合上下文，并以 `:` 结尾。
2. `/path` 标识 Game Object，并在 ID 前使用 `/`。
3. `#fragment` 标识该对象上的具体组件（例如 script、sprite 或 collision component），并在 ID 前使用 `#`。

#### 静态地址

这些标识符在各自创建时确定，之后永不改变，即使你修改父子关系也是如此。你可以在文件的 `Id` 属性中设置它们，或者在运行时通过 `factory.create` 或 `collectionfactory.create` 实例化时获取。

#### 相对寻址

你不总是需要使用完整 URL。

如果在同一 collection（同一个 *world*）内发送消息，可以省略 socket 部分：

```yaml
/gameobject #component
```

如果要发送到同一个游戏对象内的组件，也可以省略游戏对象部分：

```yaml
#component
```

两个有用的简写：

- `#` 表示发送到当前 *Script* 组件。
- `.` 表示发送到当前 *Game Object* 中的所有组件。

相对寻址和简写允许你编写可在不同上下文和游戏对象中复用的 URL，而无需指定完整路径。

### 发送消息到 GUI 和 render

由于 Defold 将 GUI world 与 Game Object world 分离，你也可以从游戏对象 `.scripts` 向 `.gui_scripts` 发送消息。

你还可以使用以 `@` 开头的标识符向特殊系统命名空间发送消息。例如，渲染系统可通过 `@render`: 寻址，你可以用它控制某些内置渲染功能，例如在默认渲染脚本中修改投影：

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

更多细节请阅读 [Addressing 手册](/manuals/addressing/)。

---

## Prefabs 和实例

Unity 可以静态或动态实例化 Scene 中的任何内容，Defold 也可以做到。在 Unity 中，你取一个 Prefab 并调用 `Instantiate(prefab)`。在 Defold 中，有 3 个用于实例化内容的组件：

- `Factory` - 从给定原型实例化**单个 Game Object**：一个 `*.go` 文件（prefab）。
- `Collection Factory` - 从给定原型实例化一组带父子关系的 **Game Objects**：一个 `*.collection` 文件。
- `Collection Proxy` - **加载**并实例化来自 `*.collection` 文件的新 *world*。

### Factory

定义好 `Factory` 组件，并将其 `Prototype` 属性设置为合适的 Game Object 文件后，在代码中生成对象非常简单：

```lua
factory.create("#my_factory")
```

这里使用组件地址，在此例中是带有 `"#my_factory"` 标识符的相对路径。

它会返回新创建实例的标识符。如果之后需要使用它，值得把它存入变量：

```lua
local new_instance_id = factory.create("#my_factory")
```

请记住，在 Defold 中你不需要手动池化对象，引擎本身会在内部为你处理池化。

更多细节请阅读 [Factory 手册](/manuals/factory/)。

### Collection Factory

`Factory` 与 `Collection Factory` 组件的区别在于，Collection Factory 可以一次生成**多个**游戏对象，并在创建时按 `*.collection` 文件中定义的方式建立父子关系。

Unity 中没有这种区分，也没有专门对应 Defold Collection Factory 的概念。最接近的类比是包含对象层级的嵌套 Prefab。

它会返回一个包含所有已生成实例 id 的**表**：

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

更多细节请阅读 [Collection Factory 手册](/manuals/collection-factory/)。

#### 实例的自定义属性

调用 `factory.create()` 或 `collectionfactory.create()` 时，也可以指定可选参数，例如位置、旋转、缩放和脚本属性，从而精确控制实例出现的位置和方式，以及它的行为，例如：

```lua
factory.create("#my_factory", my_position, my_rotation, my_scale, my_properties)
```

#### 动态加载

在 `Factory` 和 `Collection Factory` 组件中，你可以把 Prototype 标记为动态资源加载，使其较重的资源只在需要时加载到内存，并在不再使用时卸载。

更多细节请阅读 [Resource Management 手册](/manuals/resource/)。

### Collection Proxy

`Collection Proxy` 引用一个具体的 `*.collection` 文件，但它不是像 factories 那样把对象注入到*当前 world*，而是**加载并实例化一个新的游戏 world**。这有点类似 Unity 中加载整个 scene，但隔离更严格。

在 Unity 中，你可能这样加载 additive scene：

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

在 Defold 中，你只需向 `Collection Proxy` 组件发送消息即可加载新集合：

```lua
msg.post("#myproxy", "load")
```

1. 当你向 proxy 发送 `"load"`（或用于异步加载的 `"async_load"`）消息时，引擎会分配一个新 world，将该 collection 中的一切实例化到其中，并保持隔离。
2. 加载完成后，proxy 会返回 `"proxy_loaded"` 消息，表示 world 已准备好。
3. 然后通常发送 `"init"` 和 `"enable"` 消息，让新 world 中的对象开始正常生命周期。

要在已加载的 worlds 之间通信，必须使用包含 world 名称（URL 的第一部分 `collection:`）的 URL 进行显式消息传递。

在实现关卡切换、小游戏或大型模块化系统时，这种隔离会非常有优势，因为它能防止非预期交互，并且在需要时允许分别控制更新时间（例如暂停或慢动作）。

如果你曾在 Unity 中使用多个 scenes，并希望它们彼此独立运行，可以把 `Collection Proxy` 理解为把这个概念直接带入 Defold 的方式。

更多细节请阅读 [Collection Proxy 手册](/manuals/collection-proxy/)。

---

## 应用生命周期

你已经熟悉 Unity 的一组生命周期事件：`Awake`、`Start`、`Update`、`FixedUpdate`、`LateUpdate`、`OnDestroy` 或 `OnApplicationQuit`。

Defold 也有定义明确的应用生命周期，但概念和术语不同。Defold 通过一组预定义 Lua 回调暴露生命周期阶段，这些回调会在初始化、每帧处理和最终化期间由引擎调用。

下面是对比：

| Defold | Unity | 说明 |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| Defold 只有一个初始化入口点和回调：init()。组件创建时都会调用它。 |
| `on_input` | Input Methods | 当[脚本设置了输入焦点](/manuals/input/#input-focus)时，Defold 会接收输入。它在更新循环中最先处理。 |
| `fixed_update()` | `FixedUpdate()` | 以固定时间步调用。要在 Defold 中启用它，必须设置 `Use Fixed Timestep`，详见[项目设置](https://defold.com/manuals/project-settings/#use-fixed-timestep)。从 1.12.0 开始，它在 `update()` 前运行。 |
| `update()` | `Update()` | 每帧调用一次，并带有 delta time。 |
| `late_update()` | `LateUpdate()` | 在 `update()` 后、帧渲染前调用。从 1.12.0 开始可用。 |
| `on_message` | Message Receiver | Defold 接收消息的核心回调。当队列中有消息时处理。 |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | 当游戏对象在运行时被销毁（使用 `go.delete()`）、world/collection 被卸载，或应用终止时，Defold 会为相关组件调用 `final()` 回调。 |

::: sidenote
请记住，当多个组件同时初始化、更新或移除时，Defold 不保证它们之间的执行顺序。建议使用解耦设计。
:::

### 初始化

可以把 Defold 的 `init()` 理解为 Unity 中 `Awake()`、`Start()` 和 `OnEnable()` 的组合：这是一个单一入口点，引擎已经设置好一切，你可以安全地准备组件状态。

### 消息何时处理？

因为你已经可以在 `init()` 中发送消息，所以消息会在初始化刚结束后首先分发。

之后，消息会在每个内部处理循环后，只要队列中有内容就被处理。因此 `on_message()` 可能会在一次 update 循环中被调用多次。

### 更新循环

每一帧，Defold 都会运行一系列操作：处理输入、分发消息、触发脚本和 GUI 更新、应用物理和变换，最后渲染图形。

### 最终化

在 Defold 中，清理始终与删除或卸载 world 绑定，而你唯一的组件级退出钩子是 `final()`。

与 Unity 模型相比，一个细微区别是：Defold 不区分组件被禁用和整个应用退出。

### 渲染

渲染脚本（`*.render_script`）是渲染管线的一部分，也通过自己的 `init()`、`update()` 和 `on_message()` 回调参与生命周期，但它们运行在渲染线程上，并与游戏对象和 GUI 脚本逻辑分离。

更多细节请阅读 [Application Lifecycle 手册](/manuals/application-lifecycle/)。

---

## GUI

Defold 的 GUI 是一个完整且独立的用户界面框架，用于菜单、覆盖层、对话框和其他元素，类似 UI Toolkit 或带 Canvas 的 uGUI。

GUI 是一个 Component，并且与 Game Objects 和 Collections 分离。你不使用 Game Objects，而是使用按层级排列的 GUI nodes，并由 GUI script 驱动。

### GUI Nodes

打开 Defold 中的 `*.gui` 组件文件时，你会看到一个可放置 `"GUI nodes"` 的画布。它们是 GUI 的构建块。你可以添加以下类型的 GUI nodes：

- Box（带纹理的矩形形状）
- Text（可使用任意字体）
- Pie（带纹理的径向填充扇形元素）
- ParticleFX
- Template（另一个完整的嵌套 `.gui` 文件，类似 GUI prefab）
- 使用 Spine 扩展时的 Spine node

### GUI Script

GUI component 有一个用于 GUI scripts 的特殊属性：每个 component 分配一个 `*.gui_script` 文件，用于修改组件行为。因此它与普通 scripts 很相似，只是它不使用 `go.*` 命名空间（该命名空间用于 game object scripts）。它改用只在 GUI scripts（`*.gui_script`）中工作的特殊 `gui.*` 命名空间 API。你可以把它理解为一个独立的 Scene，类似带 Canvas 的 Unity UI (uGUI)。

### GUI 渲染

GUI 元素独立于游戏相机渲染，通常在屏幕空间中渲染，但在自定义渲染管线中可以改变此行为。

更多细节请阅读 [GUI 手册](/manuals/gui/)。

## Sorting Layers 在哪里？

这是从 Unity 迁移时非常常见的困惑。

GUI components 有 `Layers`，这几乎与 Unity 中的 "Sorting Layers" 相同，但对 `Sprites`、`Tilemaps`、`Models` 等其他组件来说，没有直接等价物。

通常你会组合使用：

- 使用默认相机时通过 Z 轴进行细粒度排序，或使用 Camera 组件时通过深度排序。
- 通过渲染脚本中的 render predicates 进行粗粒度排序，按材质标签选择绘制内容。

但不应使用大量 tags 来模仿 Unity Sorting Layers，因为在 Defold 中，tags 是渲染层面的机制。过度使用会破坏 batching 并增加绘制开销。

---

## 接下来去哪里？

- [Defold 示例](/examples)
- [教程](/tutorials)
- [手册](/manuals)
- [API 参考](/ref/go)
- [FAQ](/faq/faq)

如果你有问题或遇到困难，[Defold Forum](//forum.defold.com) 或 [Discord](https://defold.com/discord/) 都是寻求帮助的好地方。
