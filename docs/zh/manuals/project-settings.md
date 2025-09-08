# Defold 项目设置

本手册描述了 Defold 中项目特定设置的工作方式。

Defold 项目设置保存在项目根目录下的 `game.project` 文件中。这些设置控制引擎的各个方面，从显示和渲染到物理和输入。

## 运行时访问

您可以在运行时通过 [`sys.get_config()`](/ref/sys/#sys.get_config) 函数访问设置值：

```lua
local width = tonumber(sys.get_config("display.width"))
```

## 设置类别

### Bootstrap

#### Main Collection

指定游戏启动时要加载的主集合。这通常是您的游戏世界或菜单的集合。

#### Render

指定游戏启动时要加载的渲染脚本。这通常是您的游戏渲染脚本，但如果您有多个渲染脚本，则可以指定一个不同的脚本用于启动。

#### Collection Proxies

指定游戏启动时要加载的集合代理列表。这通常用于加载游戏资源，如图像、声音等。

### Display

#### Width

游戏画布的宽度（以像素为单位）。

#### Height

游戏画布的高度（以像素为单位）。

#### High Dpi

如果设置，将启用高 DPI 支持。这意味着在高 DPI 设备上，游戏将以更高的分辨率渲染，从而提供更清晰的图像。

#### Samples

多重采样抗锯齿的样本数。值越高，图像质量越好，但性能开销也越大。

#### Fullscreen

如果设置，游戏将以全屏模式启动。

#### Project Orientation

指定项目的方向。有效值为 `Default`、`Landscape`、`Landscape Flipped`、`Portrait` 和 `Portrait Flipped`。

#### Dynamic Orientation

如果设置，将启用动态方向支持。这意味着游戏将根据设备方向自动旋转。

#### Clear Color Red, Green, Blue

指定清除颜色的红色、绿色和蓝色分量。值范围为 0.0 到 1.0。

#### Clear Color Alpha

指定清除颜色的 alpha 分量。值范围为 0.0 到 1.0。

### Engine

#### Version

指定要使用的引擎版本。这可以是特定版本号，也可以是 `stable`、`beta` 或 `alpha`。

#### Fixed Delta

如果设置，将使用固定的时间步长。这意味着游戏将以固定的帧率运行，而不管实际帧率如何。

#### Fixed Update Frequency

指定固定更新的频率（以 Hz 为单位）。这仅在使用固定时间步长时使用。

#### Max Frame Pacing

指定最大帧间隔（以毫秒为单位）。这用于限制帧率，从而减少电池消耗。

#### Vsync

如果设置，将启用垂直同步。这意味着游戏将与显示器的刷新率同步，从而减少撕裂。

#### Collection Proxies

指定要加载的集合代理列表。这通常用于加载游戏资源，如图像、声音等。

### Input

#### Repeat Delay

指定重复按键的延迟（以毫秒为单位）。这用于控制按键重复的频率。

#### Repeat Interval

指定重复按键的间隔（以毫秒为单位）。这用于控制按键重复的频率。

#### Gamepads

如果设置，将启用游戏手柄支持。

#### Gamepad Deadzone

指定游戏手柄的死区。这用于控制游戏手柄的灵敏度。

#### Touch Deadzone

指定触摸的死区。这用于控制触摸的灵敏度。

#### Mouse Deadzone

指定鼠标的死区。这用于控制鼠标的灵敏度。

### Library

#### Include Dirs

指定要包含的目录列表。这用于指定包含头文件的目录。

#### Library Dirs

指定要链接的库目录列表。这用于指定包含库文件的目录。

#### Libraries

指定要链接的库列表。这用于指定要链接的库文件。

### Logging

#### Level

指定日志级别。有效值为 `DEBUG`、`INFO`、`WARNING`、`ERROR` 和 `FATAL`。

#### Minimum Log Level

指定最小日志级别。有效值为 `DEBUG`、`INFO`、`WARNING`、`ERROR` 和 `FATAL`。

#### To Console

如果设置，将启用控制台日志记录。

#### To File

如果设置，将启用文件日志记录。

### Network

#### Http Timeout

指定 HTTP 请求的超时时间（以秒为单位）。

### Physics

#### Type

指定物理引擎的类型。有效值为 `2D`、`3D` 和 `2D_3D`。

#### Gravity X, Y, Z

指定重力的 X、Y 和 Z 分量。

#### World Scale

指定物理世界的比例。这用于控制物理世界的缩放。

#### Debug

如果设置，将启用物理调试模式。这意味着物理对象将显示为线框。

#### Debug Alpha

指定物理调试模式的 alpha 值。值范围为 0.0 到 1.0。

#### Velocity Iterations

Box2D 2.2 物理求解器的速度迭代次数。

#### Position Iterations

Box2D 2.2 物理求解器的位置迭代次数。

#### Sub Step Count

Box2D 3.x 物理求解器的子步数。

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
