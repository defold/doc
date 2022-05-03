---
title: Defold 项目配置
brief: 本教程介绍了如何在 Defold 中进行项目配置工作.
---

# 项目配置

*game.project* 文件涵盖了项目需要的所有设置. 它必须位于项目根目录而且必须命名为 *game.project*. 游戏引擎打开游戏的头一件事就是读取这个文件.

各种设置划分成各个类目. 打开该文件时 Defold 会把设置分门别类显示出来.

![Project settings](images/project-settings/settings.jpg)

下面是根据不同模块排序的各种设置. 其中有一些不在编辑器中显示 (标注为 "隐藏设置"), 但是可以右键点击 "game.project" 然后选择 <kbd>Open With ▸ Text Editor</kbd> 来进行手动编辑.

## 各类设置

### Project

#### Title
项目标题.

#### Version
版本.

#### Write Log
选中时, 游戏引擎会在项目根目录记录 *log.txt* 日志. 运行于 iOS 时, 日志文件可以通过 iTunes 和 *Apps* 页的 *File Sharing* 部分访问. 在 Android 上, 日志文件保存在应用的外存中. 在运行 *dmengine* 开发应用时, 可以通过以下命令查看日志:

```bash
$ adb shell cat /mnt/sdcard/Android/data/com.defold.dmengine/files/log.txt
```

#### Compress Archive
打包时启用压缩. 注意此设置除了 Android 都有效, 因为apk已经是压缩档了.

#### Dependencies
项目的 *Library URL* 列表. 详情请见 [Libraries 教程](/manuals/libraries/).

#### Custom Resources
`custom_resources`
项目中包含的以逗号分隔的资源列表. 如指定的是目录, 则目录下所有文件及其子目录都会包含进去. 这些资源可以通过 [`sys.load_resource()`](/ref/sys/#sys.load_resource) 载入.

#### Bundle Resources
`bundle_resources`
需要根据平台单独打包的以逗号分隔的资源目录列表. 目录必须是以项目根目录开始的绝对路径, 比如像 `/res`. 资源目录里要包含 `platform`, 或者 `architecure-platform` 的子目录.

支持的 platform 有 `ios`, `android`, `osx`, `win32`, `linux`, `web`, `switch`.

支持包含名为 `common` 的文件夹, 可以在其中加入各平台公用的资源文件.

不同平台访问 bundle 资源的方法不一样. 使用 Lua 的 `io` 模块是可行的. 但是要特别注意写对各平台的文件路径.
(举例: 在安卓平台上要这么写 "file:///android_asset/")

#### Bundle Exclude Resources
`bundle_exclude_resources`
项目中排除的以逗号分隔的资源列表.
也就是说, 这些资源会被从 `bundle_resources` 设置的基础上被剔除.

---

### Bootstrap

#### Main Collection
打开应用启动的起始集合, 默认 `/logic/main.collection`.

#### Render
指定使用哪个渲染文件, 它决定了渲染流程, 默认 `/builtins/render/default.render`.

---

### Library

#### Include Dirs
使用库共享机制从项目中共享出去的以逗号分隔的目录列表.

---

### Script

#### Shared State
打开则共享脚本的Lua状态, 默认关闭.

---

### Engine

#### Run While Iconified
当游戏应用程序窗口最小化时允许其在后台继续运行 (仅桌面平台有效), 默认值是 `false`.

### Display

#### Width
应用窗口像素为单位宽度, 默认 `960`.

#### Height
应用窗口像素为单位高度, 默认 `640`.

#### High Dpi
开启高dpi后台缓存来支持超高清. 技术上就是以 *Width* 和 *Height* 设置的双倍进行渲染, 但是脚本和属性使用的逻辑分辨率不变.

#### Samples
超采样抗锯齿所使用的采样数量. 窗口提示是 GLFW_FSAA_SAMPLES. 默认是 `0`, 相当于关闭抗锯齿.

#### Fullscreen
设置应用启动是否使用全屏. 如果关闭, 应用会以窗口形式启动.

#### Frame Cap
如果 `Vsync` 开启, 则为锁帧频率匹配最接近的交换间隔. 否则的话依据锁帧设置计时器, 0 代表不锁帧. 此设置相当于 `display.update_frequency`. ([见下文](#vsync-frame-cap-and-swap-interval)).

#### Vsync
垂直同步, 根据硬件的帧率进行刷新. 可以被驱动程序或者操作系统平台设置覆盖. ([见下文](#vsync-frame-cap-and-swap-interval)).

#### Display Profiles
指定使用哪个显示样式文件, 默认 `/builtins/render/default.display_profilesc`.  详情请见 [GUI 排版教程](/manuals/gui-layouts/#新建显示档案).

#### Dynamic Orientation
开启的话会在设备转动时动态切换横竖显示方向. 注意开发用app（指dmengine）不参考此设置.

---

### Render

#### Clear Color Red
清除红色通道, 建立游戏窗口和渲染脚本中使用.

#### Clear Color Green
清除绿色通道, 建立游戏窗口和渲染脚本中使用.

#### Clear Color Blue
清除蓝色通道, 建立游戏窗口和渲染脚本中使用.

#### Clear Color Alpha
清除alpha通道, 建立游戏窗口和渲染脚本中使用.

---

### Physics

#### Type
使用何种物理引擎, `2D` (默认) 还是 `3D`.

#### Gravity Y
延Y轴的重力加速度, 默认是 `-10` (自然重力加速度)

#### Debug
设置物理是否显示debug线.

#### Debug Alpha
debug线的不透明度, `0`--`1`. 默认是 `0.9`.

#### World Count
可以同时存在的物理世界最大数目, 默认是`4`. 如果需要使用 collection proxies 载入更多物理世界可以提高此设置. 请注意每个物理世界都要占用相应的内存.

#### Gravity X
延X轴的重力加速度, 默认是 `0`.

#### Gravity Z
延Z轴的重力加速度, 默认是 `0`.

#### Scale
设定物理世界与游戏世界的数值映射比例, `0.01`--`1.0`. 如果设置为 `0.02`, 相当于物理引擎视50个游戏单位为1米 ($1 / 0.02$). 默认值是 `1.0`.

#### Allow Dynamic Transforms
設置物理碰撞對象的变化是否繼承于其父級游戲對象, 所谓变化包括父级的移动, 缩放和缩放, 即使当前物体是动态物理物体也可继承父级的变化. 默認為 `true`.

#### Debug Scale
设置物理标识画多大, 比如原向量和法线,  默认是 `30`.

#### Max Collisions
设置向脚本报告多少个碰撞, 默认是 `64`.

#### Max Contacts
设置向脚本报告多少碰撞点, 默认是 `128`.

#### Contact Impulse Limit
设置小于多大的碰撞冲量会被忽略, 默认是 `0.0`.

#### Ray Cast Limit 2d
每帧中2d射线最大请求数量. 默认是 `64`.

#### Ray Cast Limit 3d
每帧中3d射线最大请求数量. 默认是 `128`.

#### Trigger Overlap Capacity
物理 trigger 的最大重叠数量. 默认是 `16`.

---

### Graphics

#### Default Texture Min Filter
设置缩小过滤方式, `linear` (默认) 或者 `nearest`.

#### Default Texture Mag Filter
设置放大过滤方式, `linear` (默认) 或者 `nearest`.

#### Max Draw Calls
渲染请求最大数目, 默认是 `1024`.

#### Max Characters:
在渲染缓冲区预加载字符数目, 也就是每帧最多显示多少字符, 默认是 `8192`.

#### Max Debug Vertices
debug顶点最大数目. 用于物理形状渲染与其他一些功能, 默认是 `10000`.

#### Texture Profiles
项目使用的纹理档配置文件, 默认是 `/builtins/graphics/default.texture_profiles`.

### Shader

#### Output SPIR-V
为 Metal 和 Vulkan 编译输出 SPIR-V 着色器.

---

### Input

#### Repeat Delay
按下输入保持时等待多少秒后开始算作重复输入, 默认是 `0.5`.

#### Repeat Interval
按下并保持时重复输入的时间间隔, 默认是 `0.2`.

#### Gamepads
手柄设置文件的引用, 用于映射手柄到 OS 的输入信号, 默认是 `/builtins/input/default.gamepads`.

#### Game Binding
输入设置文件的引用, 用于映射硬件输入到游戏行为, 默认是 `/input/game.input_binding`.

#### Use Accelerometer
开启后游戏引擎会在每帧接收加速度计数据. 关闭会获得少许性能提升, 默认开启.

---

### Resource

#### Http Cache
开启后, 会开启HTTP缓存用于设备上的游戏引擎从缓存中快速导入网络数据, 默认关闭.

#### Uri
项目编译数据地址, URI 格式.

#### Max Resources
一次可以加载资源的最大数目, 默认是 `1024`.

---

### Network

#### Http Timeout
HTTP超时秒数. 设置为 `0` 则关闭超时, 默认关闭.

---

### Collection

#### Max Instances
一个集合里容纳游戏对象实例的最大数目, 默认是`1024`.

#### Max Input Stack Entries
输入栈内最大游戏对象数目, 默认是`16`.

---

### Sound

#### Gain
全局增益 (音量), `0`--`1`, 默认值是 `1`.

#### Max Sound Data
声音资源的最大数目, 也就是运行时声音文件使用数目, 默认是 `128`.

#### Max Sound Buffers
(目前未使用) 同一时间声音缓冲最大数目, 默认是 `32`.

#### Max Sound Sources
(目前未使用) 同一时间声音音源最大数目, 默认是 `16`.

#### Max Sound Instances
同一时间声音实例最大数目, 也就是实际同时播放声音最大数目. 默认是 `256`.

#### Use Thread
勾選的話, 系統將使用綫程進行聲音播放以減少因爲主綫程過載造成的卡頓. 默認勾選.

---

### Sprite

#### Max Count
每个集合最大sprite数目, 默认是 `128`. [(参见最大组件数优化)](#component_max_count_optimzations).

#### Subpixels
开启后允许sprite不与像素对齐, 默认开启.

---

### Tilemap

#### Max Count
每个集合的瓷砖地图最大数目, 默认是 `16`. [(参见最大组件数优化)](#component_max_count_optimzations).

#### Max Tile Count
每个集合可同时显示的瓷砖最大数目, 默认是 `2048`.

---

### Spine

#### Max Count
spine 模型最大数目, 默认是 `128`.

---

### Mesh

#### Max Count
每个集合最大容纳3D模型面数, 默认是 `128`. [(参见最大组件数优化)](#component_max_count_optimzations).

---

### Model

#### Max Count
每个集合最大容纳3D模型组件个数, 默认是 `128`. [(参见最大组件数优化)](#component_max_count_optimzations).

---

### GUI

#### Max Count
GUI 组件最大数目, 默认是 `64`. [(参见最大组件数优化)](#component_max_count_optimzations).

#### Max Particlefx Count
同一时间粒子发射器最大数目, 默认是 `64`.

#### Max Particle Count
同一时间粒子最大数目, 默认是 `1024`.

---

### Label

#### Max Count
label 最大数目, 默认是 `64`. [(参见最大组件数优化)](#component_max_count_optimzations).

#### Subpixels
开启后允许 lables 不与像素对齐, 默认开启.

---

### Particle FX

#### Max Count
同一时间粒子发射器最大数目, 默认是 `64`. [(参见最大组件数优化)](#component_max_count_optimzations).

#### Max Particle Count
同一时间粒子最大数目, 默认是 `1024`.

---

### Collection proxy

#### Max Count
集合代理最大数目, 默认是 `8`. [(参见最大组件数优化)](#component_max_count_optimzations).

---

### Collection factory

#### Max Count
集合工厂最大数目, 默认是 `128`. [(参见最大组件数优化)](#component_max_count_optimzations).

---

### Factory

#### Max Count
游戏对象工厂最大数目, 默认是 `128`. [(参见最大组件数优化)](#component_max_count_optimzations).

---

### iOS

#### App Icon 57x57--180x180
用于应用图标的图片 (.png) 文件, 宽高分辨率表示为 `W` &times; `H`.

#### Launch Screen
Storyboard 文件 (.storyboard). 其创建方法详情请见 [iOS 教程](/manuals/ios/#创建 storyboard).

#### Launch Image 320x480--2436x1125
用于应用启动图的图片 (.png) 文件, 宽高分辨率表示为 `W` &times; `H`. iOS 基于启动图选择分辨率.

#### Pre Rendered Icons
(iOS 6 及更早) 设置图标是否预渲染. 如果关闭则图标自动添加平滑高光效果.

#### Bundle Identifier
打包id使得 iOS 认识你的应用的版本更新. 你的打包 ID 必须在 Apple 注册且确保应用唯一性. iOS 与 macOS 应用不可以使用同一id.

#### Info.plist
如果设置了, 则打包应用时使用此 info.plist 文件.

#### Custom Entitlements
如果设置了, 则打包应用会把这里的配置与档案文件 (.entitlements, .xcent, .plist) 里面设置的权限相混合.

#### Override Entitlements
如果设置了, 则会覆盖档案文件 (.entitlements, .xcent, .plist) 里面设置的权限. 必须与上面的 Custom Entitlements 配置项一起使用.

#### Default Language
如果用户没有指定 `Localizations` 列表里的语言, 则使用此处设置的语言 (见 [CFBundleDevelopmentRegion](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Localizations
以逗号分割的语言名称缩写或者是 ISO 语言代号 (见 [CFBundleLocalizations](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
用于应用图标的图片 (.png) 文件, 宽高分辨率表示为 `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi
用于Android上客户推送通知图标的图片 (.png) 文件. 图标会自动应用于本地与远程推送通知. 如果未设置默认使用应用图标.

#### Push Field Title
指定用于通知标题的酬载 JSON 域. 保留空白则默认推送应用名作为标题.

#### Push Field Text
指定用于通知文本的酬载 JSON 域. 保留空白则默认推送 `alert` 域的文本, iOS 同样如此.

#### Version Code
表示应用版本号的整数值. 随着后续更新增大此值.

#### Package
包id.

#### Gcm Sender Id
Google Cloud Messaging Sender Id. 此值由 Google 签发, 设置后才能开启推送通知.

#### Manifest
如果设置了, 则编译时使用指定 Android manifest XML 文件.

#### Iap Provider
指定使用哪个应用商店. 合法值是 `Amazon` 和 `GooglePlay`, 默认是 `GooglePlay`.

#### Input Method
指定获取 Android 设备键盘输入的方式. 合法值是 `KeyEvent` (老方法) 和 `HiddenInputField` (新方法). 默认是 `KeyEvent`.

#### Immersive Mode
如果开启, 则隐藏导航条和状态条并且让你的应用获取屏幕上所有触碰信息.

#### Debuggable
指定应用是否可以使用诸如 [GAPID](https://github.com/google/gapid) 或者 [Android Studio](https://developer.android.com/studio/profile/android-profiler) 之类的工具来调试. 这将开启 Android manifest 的 `android:debuggable` 选项.

---

### macOS

#### App Icon
用于macOS应用图标的图片 (.png) 文件.

#### Info.plist
如果设置了, 则编译时使用指定的 info.plist 文件.

#### Bundle Identifier
打包id使得 macOS 认识你的应用的版本更新. 你的打包 ID 必须在 Apple 注册且确保应用唯一性. iOS 与 macOS 应用不可以使用同一id.

---

### Windows

#### App Icon
用于Windows应用图标的图片 (.ico) 文件. 对于如何创建图标文件详情请见 [Windows 教程](/manuals/windows).

#### Iap Provider
指定使用哪个应用商店. 合法值是 `None` 和 `Gameroom`, 默认是 `None`.

---

### HTML5

#### Heap Size
指定Emscripten所使用的堆大小 (兆字节) . 默认值是 256MB.

#### .html Shell
指定编译时使用的 HTML 文件. 默认是 `/builtins/manifests/web/engine_template.html`.

#### Custom .css
指定编译时使用的 CSS 文件. 默认是 `/builtins/manifests/web/light_theme.css`.

#### Splash Image
如果设置了, 则在打包时使用指定的溅射屏幕图片代替Defold Logo.

#### Archive Location Prefix
指定打包 HTML5 时游戏数据是否拆分为多个数据包文件. 游戏启动时, 这些数据文件会被读入内存. 使用此设置指定数据包的位置, 默认值是 `archive`.

#### Archive Location Suffix
指定数据包文件的后缀. 比如说适用于, 来自 CDN 的强制非缓存文件 (比如后缀 `?version2`).

#### Engine Arguments
传到游戏引擎里的参数列表.

#### Show Fullscreen Button
在 `index.html` 文件中开启全屏按钮. 默认是 `true`.

#### Show Made With Defold
 在 `index.html` 文件中开启 Defold 链接. 默认是 `true`.

#### Scale Mode
指定游戏 canvas 所使用的缩放方式. 默认是 `Downscale Fit`.

---

### IAP

#### Auto Finish Transactions
开启后自动完成 IAP 交易. 如果关闭, 在交易成功后你需要手动调用 `iap.finish()` , 默认开启.

---

### Live update

#### Private Key
如果设置了, 则在编译热更新内容时使用指定的私匙. 如果不设置, 则自动生成一个私匙.

#### Public Key
如果设置了, 则在编译热更新内容时使用指定的公匙. 如果不设置, 则自动生成一个私匙.

---

### Native extension

#### _App Manifest_
如果设置了, 则在自定义引擎编译时使用指定的 manifest. 此设置可以让你移除引擎不必要的部分来减小包体. 注意此设置尚在测试中. 使用方法详情请见 [这个帖子](https://forum.defold.com/t/native-extensions/4946/142).

---

### Profiler

#### Track Cpu
如果开启, 则在编译版本中开启 CPU profiling. 通常, 你只能在 debug 版本中进行调试.

---

## File format

设置文件的格式时简单的文本 (INI 格式) 并且可以使用标准文本编辑器编辑. 其格式看起来像这样:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

实例比如像:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

意味着设置 *main_collection* 隶属于 *bootstrap* 栏目.
当引用了一个文件, 比如上面的例子, 路径尾需要加一个 'c' 字符, 表明引用的时编译后的文件.
注意包含 *game.project* 的文件夹将作为项目根目录, 这就是路径开头使用 '/' 的原因.


## 在引擎启动时设定配置值

引擎启动时, 可以从命令行输入设置来覆盖 *game.project* 里的设定:

```bash
# Specify a bootstap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=1234
```

自定义值可以---像其他设置一样---使用 [`sys.get_config()`](/ref/sys/#sys.get_config) 读取:

```lua
local my_value = tonumber(sys.get_config("test.my_value"))
```

## 最大组件数优化
配置文件 `game.project` 包含针对各种资源同时存在的最大数目的配置项, 容器大都是每个载入的集合 (也叫做游戏世界). Defold 引擎使用这些最大值来预分配内存以避免游戏运行时内存动态分配及内存碎片化.

用于表示组件和其他资源的 Defold 数据结构优化为尽可能少用内存, 但当配置这些最大值时仍要留意是否保证了满足游戏运行的需求.

另一方面 Defold 编译处理会分析游戏内容, 如果明确分析出必要的内存需求则会覆盖最大值设置:

* 如果集合不含工厂组件则仅分配各个组件必须的内存忽略最大值设置.
* 如果集合包含工厂组件则分析工厂可实例化的游戏对象组件的必要内存并为其实例化分配足够内存.


## 垂直同步, 帧数锁定 和 刷新间隔
首先要注意的是桌面平台上垂直同步可以被显卡设置控制. 比如如果在显卡控制面板里强制开启了垂直同步那么从 Defold 的角度是没法读写这个设置的. 大多数移动设备也都默认开启了垂直同步.

如果在 `game.project` 中开启 `Vsync` 的话, 引擎依照硬件垂直同步根据检测到的任何显示设备刷新率决定固定 `dt` 值. 这是默认的情况. 如果开启 `Vsync` 并且设置 `Frame cap` > 0, 则帧率设置兼顾显示器刷新率与锁帧频率. 如果 `Vsync` 关闭并且设置 `Frame cap` 为 0, `dt` 就不是固定的了而是使用实际的时间间隔. 如果 `Vsync` 关闭并且设置 `Frame cap` > 0, 时间步进取帧数锁定设置的值. 不同平台和硬件设备下无法保证刷新间隔时间一致.

交换间隔是指在垂直空白期 (v-blank) 同步中交换前后缓冲的间隔, 是屏幕图片从前缓冲更新数据的硬件事件. 取值为1就是每个v-blank做一次交换缓冲, 取值为2就是每两个（每隔一个）v-blank做一次交换缓冲, 以此类推. 取值为0则做交换缓冲时不等待v-blank时间\*. 调用 [```set_vsync_swap_interval```](/ref/sys/#sys.set_vsync_swap_interval:swap_interval) 方法可以设置 `swap_interval` 的值.


### 注意事项
目前, Defold 在初始化时查询屏幕刷新率并且把它作为固定 `dt` 的依据. 如果你需要支持可变刷新率 (比如 GSync 或者 FreeSync) 或者其他刷新率不是很有参考性的情况下, 关闭 `Vsync`来使引擎测量每帧实际 `dt` 而不是固定dt.


### Defold 中的垂直同步与帧数锁定

<table>
  <tr>
    <th></th>
    <th><b>Frame cap 为 0 (默认)</b></th>
    <th><b>Frame cap 大于 0</b></th>
  </tr>
  <tr>
    <td><b>Vsync 开启 (默认)</b></td>
    <td>依据硬件垂直同步. 取<code>1/(屏幕刷新率)</code> 作为固定 <code>dt</code> .</td>
    <td>固定 <code>dt</code> 为 <code>(交换间隔)/(显示器刷新率)</code> 其中交换间隔取值基于锁帧频率.</td>
  </tr>
  <tr>
    <td><b>Vsync 关闭</b></td>
    <td>依据记录的每帧实际消耗系统时间计算 <code>dt</code>. 驱动程序有权强制开启垂直同步.</td>
    <td>固定 <code>dt</code> 为 <code>1 / (锁定帧数)</code>. 计时与等待取值基于锁帧频率.</td>
  </tr>
</table>
