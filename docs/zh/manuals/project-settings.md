---
title: Defold 项目设置
brief: 本手册介绍了 Defold 中项目特定设置的工作方式。
---

# 项目设置

文件 *game.project* 包含所有项目级别的设置。它必须保存在项目的根文件夹中，并且必须命名为 *game.project*。引擎在启动和运行您的游戏时做的第一件事就是查找这个文件。

文件中的每个设置都属于一个类别。当您打开文件时，Defold 会将所有设置按类别分组展示。

![Project settings](images/project-settings/settings.jpg)


## 文件格式

*game.project* 中的设置通常在 Defold 内部修改，但该文件也可以在任何标准文本编辑器中编辑。该文件遵循 INI 文件格式标准，如下所示：

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

一个真实的例子是：

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

这意味着设置 *main_collection* 属于 *bootstrap* 类别。每当使用文件引用时（如上面的例子），路径需要附加一个 'c' 字符，这意味着您引用的是文件的编译版本。还要注意，包含 *game.project* 的文件夹将成为项目根目录，这就是为什么在设置路径中有一个初始 '/'。


## 运行时访问

可以在运行时使用 [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string)、[`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number) 和 [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) 从 *game.project* 中读取任何值。例子：

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
```

::: sidenote
键是类别和设置名称的组合，用点分隔，并用小写字母书写，任何空格字符用下划线替换。例子：“Project”类别中的“Title”字段变成 `project.title`，“Physics”类别中的“Gravity Y”字段变成 `physics.gravity_y`。
:::


## 部分和设置

下面是所有可用的设置，按类别排列。

### Project

#### Title
应用程序的标题。

#### Version
应用程序的版本。

#### Publisher
发布商名称。

#### Developer
开发商名称。

#### Write Log File
控制引擎何时写入日志文件。选项：

- “Never”：不写入日志文件。
- “Debug”：仅在 Debug 构建中写入日志文件。
- “Always”：在 Debug 和 Release 构建中都写入日志文件。

如果从编辑器运行多个实例，文件将被命名为 *instance_2_log.txt*，其中 `2` 是实例索引。如果运行单个实例或从打包运行，文件将被命名为 *log.txt*。日志文件的位置将是以下路径之一（按顺序尝试）：

1. 在 *project.log_dir* 中指定的路径（隐藏设置）
2. 系统日志路径：
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * 其他: 应用程序根目录
3. 应用程序支持路径
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` （例如 `C:\Users\<username>\AppData\Roaming`）
  * Android: `Context.getFilesDir()`
  * Linux: `HOME` 环境变量

#### Minimum Log Level
指定日志系统的最低日志级别。只有在此级别或以上的日志才会显示。

#### Compress Archive
在打包时启用存档压缩。请注意，这目前适用于除 Android 以外的所有平台，因为 apk 已经包含所有压缩数据。

#### Dependencies
项目 *库 URL* 的 URL 列表。有关更多信息，请参阅[库手册](/manuals/libraries/)。

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

加载自定义资源在[文件访问手册](/manuals/file-access/#how-to-access-files-bundled-with-the-application)中有更详细的介绍。

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

加载打包资源在[文件访问手册](/manuals/file-access/#how-to-access-files-bundled-with-the-application)中有更详细的介绍。

#### Bundle Exclude Resources
`bundle_exclude_resources`
一个逗号分隔的资源列表，这些资源不应包含在打包中。即，它们从 `bundle_resources` 步骤的集合结果中被删除。

---

### Bootstrap

#### Main Collection
用于启动应用程序的集合文件引用，默认为 `/logic/main.collection`。

#### Render
要使用的渲染设置文件，它定义了渲染管道，默认为 `/builtins/render/default.render`。

---

### Library

#### Include Dirs
应通过库共享从您的项目中共享的目录的空格分隔列表。有关更多信息，请参阅[库手册](/manuals/libraries/)。

---

### Script

#### Shared State
勾选以在所有脚本类型之间共享单个 Lua 状态。

---

### Engine

#### Run While Iconified
允许引擎在应用程序窗口最小化时继续运行（仅限桌面平台）。

#### Fixed Update Frequency
`fixed_update(self, dt)` 生命周期函数的更新频率。以赫兹为单位。

#### Max Time Step
如果单帧期间时间步长变得太大，它将被限制为此最大值。以秒为单位。

---

### Display

#### Width
应用程序窗口的宽度（以像素为单位）。

#### Height
应用程序窗口的高度（以像素为单位）。

#### High Dpi
在支持的显示器上创建高 dpi 后缓冲区。通常游戏将以比*宽度*和*高度*设置中设置的分辨率高一倍的分辨率渲染，这仍然是脚本和属性中使用的逻辑分辨率。

#### Samples
用于超级采样抗锯齿的样本数量。它设置 GLFW_FSAA_SAMPLES 窗口提示。值为 `0` 表示关闭抗锯齿。

#### Fullscreen
勾选应用程序是否应全屏启动。如果未勾选，应用程序将在窗口模式下运行。

#### Update Frequency
所需的帧率（以赫兹为单位）。设置为 0 表示可变帧率。大于 0 的值将导致固定帧率，在运行时上限为实际帧率（这意味着您不能在引擎帧中更新游戏循环两次）。使用 [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) 在运行时更改此值。此设置也适用于无头构建。

#### Swap interval
此整数值控制应用程序如何处理垂直同步。0 禁用垂直同步，默认值为 1。使用 OpenGL 适配器时，此值设置窗口应在[缓冲区交换之间更新](https://www.khronos.org/opengl/wiki/Swap_Interval)的帧数。对于 Vulkan，没有内置的交换间隔概念，该值控制是否应启用垂直同步。

#### Vsync
依赖硬件垂直同步进行帧时序。可以根据图形驱动程序和平台特性进行覆盖。对于已弃用的 'variable_dt' 行为，请取消勾选此设置并将帧上限设置为 0。

#### Display Profiles
指定要使用的显示配置文件，默认为 `/builtins/render/default.display_profilesc`。在[GUI 布局手册](/manuals/gui-layouts/#creating-display-profiles)中了解更多信息。

#### Dynamic Orientation
勾选应用程序是否应在设备旋转时动态切换纵向和横向。请注意，开发应用程序目前不遵守此设置。

#### Display Device Info
在启动时将 GPU 信息输出到控制台。

---

### Render

#### Clear Color Red
清除颜色红色通道，由渲染脚本和创建窗口时使用。

#### Clear Color Green
清除颜色绿色通道，由渲染脚本和创建窗口时使用。

#### Clear Color Blue
清除颜色蓝色通道，由渲染脚本和创建窗口时使用。

#### Clear Color Alpha
清除颜色 Alpha 通道，由渲染脚本和创建窗口时使用。

---

### Font

#### Runtime Generation
使用运行时字体生成。

---

### Physics

#### Max Collision Object Count
碰撞对象的最大数量。

#### Type
要使用的物理类型，`2D` 或 `3D`。

#### Gravity X
沿 x 轴的世界重力。以米每秒为单位。

#### Gravity Y
沿 y 轴的世界重力。以米每秒为单位。

#### Gravity Z
沿 z 轴的世界重力。以米每秒为单位。

#### Debug
勾选是否应可视化物理以进行调试。

#### Debug Alpha
可视化物理的 Alpha 分量值，`0`--`1`。

#### World Count
并发物理世界的最大数量，默认为 `4`。如果您通过集合代理同时加载超过 4 个世界，则需要增加此值。请注意，每个物理世界都会分配相当多的内存。

#### Scale
告诉物理引擎如何相对于游戏世界缩放物理世界以获得数值精度，`0.01`--`1.0`。如果值设置为 `0.02`，这意味着物理引擎将把 50 个单位视为 1 米（$1 / 0.02$）。

#### Allow Dynamic Transforms
勾选物理引擎是否应将游戏对象的变换应用于任何附加的碰撞对象组件。这可用于移动、缩放和旋转碰撞形状，即使是动态的。

#### Use Fixed Timestep
勾选物理引擎是否应使用固定和与帧率无关的更新。将此设置与 `fixed_update(self, dt)` 生命周期函数和 `engine.fixed_update_frequency` 项目设置结合使用，以定期与物理引擎交互。对于新项目，推荐的设置是 `true`。

#### Debug Scale
在物理中绘制单位对象的大小，如三元组和法线。

#### Max Collisions
将报告回脚本的碰撞数量。

#### Max Contacts
将报告回脚本的接触点数量。

#### Contact Impulse Limit
忽略值小于此设置的接触冲量。

#### Ray Cast Limit 2d
每帧 2d 射线投射请求的最大数量。

#### Ray Cast Limit 3d
每帧 3d 射线投射请求的最大数量。

#### Trigger Overlap Capacity
重叠物理触发器的最大数量。

#### Velocity Threshold
将导致弹性碰撞的最小速度。

#### Max Fixed Timesteps
使用固定时间步长时模拟中的最大步数（仅限 3D）。

---

### Graphics

#### Default Texture Min Filter
指定用于缩小过滤的过滤方式。

#### Default Texture Mag Filter
指定用于放大过滤的过滤方式。

#### Max Draw Calls
渲染调用的最大数量。

#### Max Characters:
文本渲染缓冲区中预分配的字符数，即每帧可以显示的字符数。

#### Max Font Batches
每帧可以显示的文本批次的最大数量。

#### Max Debug Vertices
调试顶点的最大数量。用于物理形状渲染等。

#### Texture Profiles
用于此项目的纹理配置文件，默认为 `/builtins/graphics/default.texture_profiles`。

#### Verify Graphics Calls
验证每次图形调用后的返回值并在日志中报告任何错误。

#### OpenGL Version Hint
OpenGL 上下文版本提示。如果选择了特定版本，这将用作所需的最低版本（不适用于 OpenGL ES）。

#### OpenGL Core Profile Hint
创建上下文时设置 'core' OpenGL 配置文件提示。核心配置文件删除了 OpenGL 的所有已弃用功能，例如立即模式渲染。不适用于 OpenGL ES。

---

### Shader

#### Exclude GLES 2.0
不为运行 OpenGLES 2.0 / WebGL 1.0 的设备编译着色器。

---

### Input

#### Repeat Delay
等待按住输入开始重复的秒数。

#### Repeat Interval
按住输入的每次重复之间等待的秒数。

#### Gamepads
游戏手柄配置文件的文件引用，它将游戏手柄信号映射到操作系统，默认为 `/builtins/input/default.gamepads`。

#### Game Binding
输入配置文件的文件引用，它将硬件输入映射到操作，默认为 `/input/game.input_binding`。

#### Use Accelerometer
勾选以使引擎每帧接收加速计输入事件。禁用加速计输入可能会带来一些性能好处。

---

### Resource

#### Http Cache
如果勾选，将为通过网络更快地加载资源到设备上运行的引擎启用 HTTP 缓存。

#### Uri
在哪里找到项目构建数据，采用 URI 格式。

#### Max Resources
可以同时加载的资源的最大数量。

---

### Network

#### Http Timeout
HTTP 超时（以秒为单位）。设置为 `0` 以禁用超时。

#### Http Thread Count
HTTP 服务的工作线程数。

#### Http Cache Enabled
勾选以启用网络请求的 HTTP 缓存（使用 `http.request()`）。HTTP 缓存将存储与请求关联的响应，并为后续请求重用存储的响应。HTTP 缓存支持 `ETag` 和 `Cache-Control: max-age` HTTP 响应头。

#### SSL Certificates
包含在 SSL 握手期间验证证书链时要使用的 SSL 根证书的文件。

---

### Collection

#### Max Instances
集合中游戏对象实例的最大数量，默认为 `1024`。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Max Input Stack Entries
输入堆栈中游戏对象的最大数量。

---

### Sound

#### Gain
全局增益（音量），`0`--`1`。

#### Use Linear Gain
如果启用，增益是线性的。如果禁用，使用指数曲线。

#### Max Sound Data
声音资源的最大数量，即运行时唯一声音文件的数量。

#### Max Sound Buffers
（当前未使用）并发声音缓冲区的最大数量。

#### Max Sound Sources
（当前未使用）并发播放声音的最大数量。

#### Max Sound Instances
并发声音实例的最大数量，即同时播放的实际声音。

#### Max Component Count
每个集合的声音组件的最大数量。

#### Sample Frame Count
每次音频更新使用的样本数。0 表示自动（48 kHz 为 1024，44.1 kHz 为 768）。

#### Use Thread
如果勾选，声音系统将使用线程进行声音播放，以减少主线程负载过重时的卡顿风险。

#### Stream Enabled
如果勾选，声音系统将使用流式传输来加载源文件。

#### Stream Cache Size
包含_所有_块的声音块缓存的最大大小。默认为 `2097152` 字节。
此数字应该大于加载的声音文件数乘以流块大小。
否则，您就有风险每帧都要逐出新块。

#### Stream Chunk Size
流音频的块大小（以字节为单位）。

#### Stream Preload Size
流音频的预加载大小（以字节为单位）。

---

### Sprite

#### Max Count
精灵组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Subpixels
允许精灵子像素定位。

---

### Tilemap

#### Max Count
瓦片地图组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Max Tile Count
瓦片的最大数量。

---

### Spine

#### Max Count
Spine 模型组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

---

### Mesh

#### Max Count
网格组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

---

### Model

#### Max Count
模型组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Split Meshes
将具有多个材质的网格拆分为多个网格。启用时，拥有多个材质的模型将被分解为每个材质一个网格。禁用时，整个模型将使用单个材质进行渲染。

#### Max Bone Matrix Texture Width
骨骼矩阵纹理的最大宽度。

#### Max Bone Matrix Texture Height
骨骼矩阵纹理的最大高度。

---

### GUI

#### Max Count
GUI 组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Max Particle Count
GUI 粒子效果的最大粒子数量。

#### Max Animation Count
GUI 动画的最大数量。

---

### Label

#### Max Count
标签组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Subpixels
允许标签子像素定位。

---

### Particle FX

#### Max Count
粒子 FX 组件的最大数量。[(参见组件最大数量优化的信息)](#component-max-count-optimizations)。

#### Max Particle Count
粒子的最大数量。

---

### Box2D

#### Velocity Iterations
Box2D 求解器速度迭代。

#### Position Iterations
Box2D 求解器位置迭代。

#### Sub Step Count
Box2D 步骤计数。

---

### Collection proxy

#### Max Count

集合代理的最大数量。[(有关组件最大数量优化的信息)](#component-max-count-optimizations)。

### Collection factory

#### Max Count

集合工厂的最大数量。[(有关组件最大数量优化的信息)](#component-max-count-optimizations)。

### Factory

#### Max Count

游戏对象工厂的最大数量。[(有关组件最大数量优化的信息)](#component-max-count-optimizations)。

### iOS

#### App Icon 57x57--180x180

用作给定宽度和高度尺寸 `W` × `H` 的应用图标的图像文件 (.png)。

#### Launch Screen

Storyboard 文件 (.storyboard)。了解如何在 [iOS 手册](/manuals/ios/#creating-a-storyboard) 中创建一个。

#### Icons Asset

包含应用图标的图标资源文件 (.car)。

#### Prerendered Icons

（iOS 6 及更早版本）如果您的图标是预渲染的，请勾选此项。如果未勾选，图标将自动添加光泽高亮。

#### Bundle Identifier

捆绑标识符让 iOS 识别您应用的任何更新。您的捆绑 ID 必须在 Apple 注册，并且对您的应用是唯一的。您不能对 iOS 和 macOS 应用使用相同的标识符。必须由两个或多个用点分隔的段组成。每个段必须以字母开头。每个段只能包含字母数字字母、下划线或连字符 (-) 字符（参见 [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)）。

#### Bundle Name

捆绑短名称（15 个字符）（参见 [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)）。

#### Bundle Version

捆绑版本，可以是数字或 x.y.z（参见 [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)）。

#### Info.plist

如果指定，在打包应用时使用此 *`info.plist`* 文件。

#### Privacy Manifest

应用的 Apple 隐私清单。该字段将默认为 `/builtins/manifests/ios/PrivacyInfo.xcprivacy`。

#### Custom Entitlements

如果指定，提供的配置文件（`.entitlements`、`.xcent`、`.plist`）中的权限将与打包应用时提供的配置文件中的权限合并。

#### Default Language

如果应用在 `Localizations` 列表中没有用户的首选语言时使用的语言（参见 [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)）。如果首选语言在那里可用，请使用两字母 ISO 639-1 标准或三字母 ISO 639-2。

#### Localizations

此字段包含逗号分隔的字符串，标识支持本地化的语言名称或 ISO 语言指示符（参见 [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)）。

### Android

#### App Icon 36x36--192x192

用作给定宽度和高度尺寸 `W` × `H` 的应用图标的图像文件 (.png)。

#### Push Icon Small--LargeXxxhdpi

用作 Android 上自定义推送通知图标的图像文件 (.png)。图标将自动用于本地或远程推送通知。如果未设置，默认将使用应用图标。

#### Push Field Title

指定应使用哪个有效负载 JSON 字段作为通知标题。将此设置留空会使推送默认使用应用名称作为标题。

#### Push Field Text

指定应使用哪个有效负载 JSON 字段作为通知文本。如果留空，将使用 `alert` 字段中的文本，就像在 iOS 上一样。

#### Version Code

指示应用版本的整数值。为每个后续更新增加该值。

#### Minimum SDK Version

应用运行所需的最低 API 级别（`android:minSdkVersion`）。

#### Target SDK Version

应用针对的 API 级别（`android:targetSdkVersion`）。

#### Package

包标识符。必须由两个或多个用点分隔的段组成。每个段必须以字母开头。每个段只能包含字母数字字母或下划线字符。

#### GCM Sender Id

Google Cloud Messaging 发送者 ID。将其设置为 Google 分配的字符串以启用推送通知。

#### FCM Application Id

Firebase Cloud Messaging 应用 ID。

#### Manifest

如果设置，在打包时使用指定的 Android 清单 XML 文件。

#### Iap Provider

指定要使用的商店。有效选项是 `Amazon` 和 `GooglePlay`。有关更多信息，请参考 [extension-iap](/extension-iap/)。

#### Input Method

指定在 Android 设备上获取键盘输入的方法。有效选项是 `KeyEvent`（旧方法）和 `HiddenInputField`（新方法）。

#### Immersive Mode

如果设置，隐藏导航和状态栏，并让您的应用捕获屏幕上的所有触摸事件。

#### Display Cutout

扩展到显示屏切口。

#### Debuggable

应用是否可以使用诸如 [GAPID](https://github.com/google/gapid) 或 [Android Studio](https://developer.android.com/studio/profile/android-profiler) 之类的工具进行调试。这将在 Android 清单中设置 `android:debuggable` 标志（[官方文档](https://developer.android.com/guide/topics/manifest/application-element#debug)）。

#### ProGuard config

自定义 ProGuard 文件，帮助从最终 APK 中删除冗余的 Java 类。

#### Extract Native Libraries

指定包安装程序是否将原生库从 APK 提取到文件系统。如果设置为 `false`，您的原生库将以未压缩的形式存储在 APK 中。虽然您的 APK 可能更大，但您的应用程序加载速度更快，因为库在运行时直接从 APK 加载。这将在 Android 清单中设置 `android:extractNativeLibs` 标志（[官方文档](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)）。

### macOS

#### App Icon

用作 macOS 应用图标的捆绑图标文件 (.icns)。

#### Info.plist

如果设置，在打包时使用指定的 info.plist 文件。

#### Privacy Manifest

应用的 Apple 隐私清单。该字段将默认为 `/builtins/manifests/osx/PrivacyInfo.xcprivacy`。

#### Bundle Identifier

捆绑标识符让 macOS 识别您应用的更新。您的捆绑 ID 必须在 Apple 注册，并且对您的应用是唯一的。您不能对 iOS 和 macOS 应用使用相同的标识符。必须由两个或多个用点分隔的段组成。每个段必须以字母开头。每个段只能包含字母数字字母、下划线或连字符 (-) 字符。

#### Default Language

如果应用在 `Localizations` 列表中没有用户的首选语言时使用的语言（参见 [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)）。如果首选语言在那里可用，请使用两字母 ISO 639-1 标准或三字母 ISO 639-2。

#### Localizations

此字段包含逗号分隔的字符串，标识支持本地化的语言名称或 ISO 语言指示符（参见 [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)）。

### Windows

#### App Icon

用作 Windows 应用图标的图像文件 (.ico)。有关如何创建 .ico 文件的更多信息，请参阅 [Windows 手册](/manuals/windows)。

### HTML5

有关这些选项的更多信息，请参阅 [HTML5 平台手册](/manuals/html5/)。

#### Heap Size

Emscripten 要使用的堆大小（以兆字节为单位）。

#### .html Shell

在打包时使用指定的模板 HTML 文件。默认为 `/builtins/manifests/web/engine_template.html`。

#### Custom .css

在打包时使用指定的主题 CSS 文件。默认为 `/builtins/manifests/web/light_theme.css`。

#### Splash Image

如果设置，在打包时使用指定的启动图像代替 Defold 徽标。

#### Archive Location Prefix

为 HTML5 打包时，游戏数据被拆分为一个或多个存档数据文件。当引擎启动游戏时，这些存档文件被读入内存。使用此设置指定数据的位置。

#### Archive Location Suffix

要附加到存档文件的后缀。例如，对于强制来自 CDN 的非缓存内容（例如 `?version2`）很有用。

#### Engine Arguments

将传递给引擎的参数列表。

#### Wasm Streaming

启用 wasm 文件的流式传输（更快且使用更少的内存，但需要 `application/wasm` MIME 类型）。

#### Show Fullscreen Button

在 `index.html` 文件中启用全屏按钮。

#### Show Made With Defold

在 `index.html` 文件中启用 Made With Defold 链接。

#### Show Console Banner

启用此选项将在引擎启动时在浏览器控制台中打印有关引擎和引擎版本的信息（使用 `console.log()`）。

#### Scale Mode

指定用于缩放游戏画布的方法。

#### Retry Count

引擎启动时下载文件的尝试次数（参见 `Retry Time`）。

#### Retry Time

下载失败时尝试下载文件之间等待的秒数（参见 `Retry Count`）。

#### Transparent Graphics Context

如果您希望图形上下文具有透明背景，请勾选此项。

### IAP

#### Auto Finish Transactions

勾选以自动完成 IAP 交易。如果未勾选，您需要在成功交易后显式调用 `iap.finish()`。

### Live update

#### Settings

在打包期间要使用的实时更新设置资源文件。

#### Mount On Start

启用应用启动时自动挂载先前挂载的资源。

### Native extension

#### _App Manifest_

如果设置，使用应用清单自定义引擎构建。这允许您从引擎中删除未使用的部分以减少最终二进制文件的大小。了解如何在 [应用清单手册](/manuals/app-manifest) 中排除未使用的功能。

### Profiler

#### Enabled

启用游戏内性能分析器。

#### Track Cpu

如果勾选，在构建的发布版本中启用 CPU 性能分析。通常，您只能在调试构建中访问性能分析信息。

#### Sleep Between Server Updates

服务器更新之间休眠的毫秒数。

#### Performance Timeline Enabled

启用浏览器内性能时间线（仅限 HTML5）。

## 在引擎启动时设置配置值

当引擎启动时，可以从命令行提供配置值，以覆盖 *game.project* 设置：

```bash
# 指定引导集合
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# 设置两个自定义配置值
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

自定义值可以像任何其他配置值一样，使用 [`sys.get_config_string()`](/ref/sys/#sys.get_config_string) 或 [`sys.get_config_number()`](/ref/sys/#sys.get_config_number) 读取：

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test2.my_value2")
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## 自定义项目设置

可以为主项目或为 [原生扩展](/manuals/extensions/) 定义自定义设置。主项目的自定义设置必须在项目根目录的 `game.properties` 文件中定义。对于原生扩展，它们应该在 `ext.manifest` 文件旁边的 `ext.properties` 文件中定义。

设置文件使用与 *game.project* 相同的 INI 格式，属性属性使用带后缀的点符号定义：

```
[my_category]
my_property.private = 1
...
```

始终应用的默认元文件可在[此处](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)获得

以下属性当前可用：

```
[my_extension]
// `type` - 用于值字符串解析
my_property.type = string // 以下值之一：bool, string, number, integer, string_array, resource

// `help` - 在编辑器中用作帮助提示（目前未使用）
my_property.help = string

// `default` - 如果用户未手动设置值，则用作默认值
my_property.default = string

// `private` - 打包过程中使用的私有值，但将从打包本身中删除
my_property.private = 1 // 布尔值 1 或 0

// `label` - 编辑器输入标签
my_property.label = My Awesome Property

// `minimum` 和/或 `maximum` - 数值属性的有效范围，在编辑器 UI 中验证
my_property.minimum = 0
my_property.maximum = 255

// `options` - 编辑器 UI 的下拉选择，逗号分隔的 value[:label] 对
my_property.options = android: Android, ios: iOS

// 仅 `resource` 类型：
my_property.filter = jpg,png // 资源选择器对话框的允许文件扩展名
my_property.preserve-extension = 1 // 使用原始资源扩展名而不是构建的扩展名

// 弃用
my_property.deprecated = 1 // 将属性标记为已弃用
my_property.severity-default = warning // 如果指定了已弃用的属性，但设置为默认值
my_property.severity-override = error  // 如果指定了已弃用的属性并设置为非默认值

```
此外，您可以在设置类别上设置以下属性：
```
[my_extension]
// `group` - game.project 类别组，例如 Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - 显示的类别标题
title = My Awesome Extension
// `help` - 显示的类别帮助
help = Settings for My Awesome Extension
```


目前，元属性仅在 `bob.jar` 打包应用程序时使用，但稍后将被编辑器解析并在 *game.project* 查看器中表示。
