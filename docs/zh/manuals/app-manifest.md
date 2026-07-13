---
title: 应用程序清单
brief: 本手册描述了如何使用应用程序清单来排除引擎中的功能。
---

# 应用程序清单

应用程序清单控制将哪些功能和后端链接到引擎中。建议排除未使用的功能，因为这会减小游戏最终二进制文件的大小。应用程序清单还包含构建时选项，例如 HTML5 支持的最低浏览器版本和 WebAssembly 内存设置。

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# 应用清单

在 `game.project` 中，将清单分配给 `Native Extensions` -> `App Manifest`。

## 物理 2D {#physics-2d}

选择要包含的 Box2D 实现：

* **Box2D Version 3** - 包含 Box2D 3。这是一个需要主动选择的选项，可能会产生与旧实现不同的模拟结果，因此现有项目可能需要重新调整物理设置。
* **Box2D (Legacy Defold version)** - 包含旧版 Defold Box2D 实现。这是默认选项。
* **None** - 排除 2D 物理功能。

Box2D 求解器设置因版本而异。详情请参阅 [Box2D 项目设置](/manuals/project-settings/#box2d)。

## 物理 3D

包含 Bullet 3D 物理实现。默认包含此实现；禁用该设置可排除 3D 物理功能。

## 骨骼 + 模型

控制骨骼和模型功能，或选择 None 来完全排除模型和骨骼功能。（参见[`模型`](https://defold.com/manuals/model/#model-component)文档）。

## 排除录制

从引擎中排除视频录制功能（参见[`start_record`](https://defold.com/ref/stable/sys/#start_record)消息文档）。

## 分析器 {#profiler}

控制何时将分析器功能链接到引擎中：

* **Debug Only** - 仅在 Debug 构建中包含分析器。这是默认选项。
* **None** - 从所有构建变体中排除分析器功能。
* **Always** - 在 Debug 和 Release 构建中都包含分析器。

App Manifest 设置控制是否将分析器代码链接到构建中。*game.project* 中 `profiler` 下的设置控制分析器的运行时行为。请参阅[性能分析手册](/manuals/profiling/)了解如何使用相关功能。

## 声音 {#sound}

声音设置控制将哪些声音系统和解码器链接到引擎中。

### 排除声音

从引擎中排除所有声音播放功能。

### 排除声音解码器：WAV

排除对 WAV 声音资源的支持。

### 排除声音解码器：OGG

排除对 Ogg Vorbis 声音资源的支持。

### 包含声音解码器：Opus

包含对 Ogg Opus 声音资源的支持。默认排除 Opus 解码器，因此必须先启用此选项才能播放 `.opus` 资源。有关支持的格式，请参阅[声音手册](/manuals/sound/)。

## 排除输入

从引擎中排除所有输入处理功能。

## 排除热更新

从引擎中排除[热更新功能](/manuals/live-update)。

## 排除图像

从引擎中排除`image`脚本模块[链接](https://defold.com/ref/stable/image/)。

## 排除类型

从引擎中排除`types`脚本模块[链接](https://defold.com/ref/stable/types/)。

## 排除 Basis 转码器

从引擎中排除 Basis Universal[纹理压缩库](/manuals/texture-profiles)。

## 使用 Android 支持库

使用已弃用的 Android 支持库而不是 Android X。[更多信息](https://defold.com/manuals/android/#using-androidx)。

## 图形

选择每个平台要包含的图形后端。组合选项会同时包含两个后端，以便首选后端不可用时能够回退。

| 字段 | 平台 | 选项 | 默认值 |
|---|---|---|---|
| **Graphics** | Windows 和 Linux | OpenGL、Vulkan、OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL、Metal、Vulkan、OpenGL & Metal、OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL、Metal、Vulkan、OpenGL & Metal、OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan、OpenGL、Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL、WebGPU、WebGL & WebGPU | WebGL |

在 Linux ARM64 上，**OpenGL** 选项使用 OpenGL ES 后端。Android 的默认组合选项会在 Vulkan 可用时优先使用 Vulkan，否则回退到 OpenGL ES。

## 使用完整文本布局系统

启用后（`true`），在项目中使用 True Type 字体（`.ttf`）时，可以为 SDF 类型字体使用运行时生成。更多详细信息请阅读[字体手册](https://defold.com/manuals/font/#enabling-runtime-fonts)。

## 最低浏览器版本

YAML 字段 **`minSafariVersion`**、**`minFirefoxVersion`** 和 **`minChromeVersion`** 指定 Emscripten 针对的最低浏览器版本。非线程目标和线程目标当前的默认值及最低支持版本不同：

| 目标 | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

请在相应目标的上下文中指定覆盖值。线程目标还有额外的[托管要求](/manuals/html5/#creating-html5-bundle)。请参阅 Emscripten 设置参考中的 [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version)、[`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) 和 [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version)。

## 初始内存（HTML5）
YAML 字段名称：**`initialMemory`**
默认值：**33554432**

为 Web 应用程序分配的初始内存量，单位为字节。该值必须是 WebAssembly 页面大小（64 KiB）的倍数。请参阅 Emscripten 的 [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) 设置。

此选项提供编译时默认值。*game.project* 中的 [`html5.heap_size`](/manuals/html5/#heap-size) 值会在运行时覆盖它。

## 栈大小（HTML5）
YAML 字段名称：**`stackSize`**
默认值：**5242880**

应用程序的栈大小，单位为字节。请参阅 Emscripten 的 [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) 设置。
