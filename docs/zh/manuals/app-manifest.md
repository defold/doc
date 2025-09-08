---
title: 应用清单
brief: 本手册介绍了如何使用应用清单来排除引擎中的功能。
---

# 应用清单

应用清单用于排除或控制要在引擎中包含哪些功能。排除引擎中未使用的功能是推荐的最佳实践，因为它会减小游戏的最终二进制文件大小。
此外，应用清单还包含一些用于控制 HTML5 平台代码编译的选项，如最低支持的浏览器版本/内存设置，这些也会影响结果二进制文件的大小。

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# 应用清单

在 `game.project` 中，将清单分配给 `Native Extensions` -> `App Manifest`。

## Physics

控制使用哪个物理引擎，或选择 None 来完全排除物理功能。

## Physics 2d

选择使用哪个版本的 Box2D。

## Rig + Model

控制骨骼和模型功能，或选择 None 来完全排除模型和骨骼功能。（参见[`模型`](https://defold.com/manuals/model/#model-component)文档）。

## Exclude Record

从引擎中排除视频录制功能（参见[`start_record`](https://defold.com/ref/stable/sys/#start_record)消息文档）。

## Exclude Profiler

从引擎中排除分析器。分析器用于收集性能和使用计数器。在[分析手册](/manuals/profiling/)中学习如何使用分析器。

## Exclude Sound

从引擎中排除所有声音播放功能。

## Exclude Input

从引擎中排除所有输入处理功能。

## Exclude Live Update

从引擎中排除[热更新功能](/manuals/live-update)。

## Exclude Image

从引擎中排除`image`脚本模块[链接](https://defold.com/ref/stable/image/)。

## Exclude Types

从引擎中排除`types`脚本模块[链接](https://defold.com/ref/stable/types/)。

## Exclude Basis Universal

从引擎中排除 Basis Universal[纹理压缩库](/manuals/texture-profiles)。

## Use Android Support Lib

使用已弃用的 Android 支持库而不是 Android X。[更多信息](https://defold.com/manuals/android/#using-androidx)。

## Graphics

选择使用哪个图形后端。

* OpenGL - 仅包含 OpenGL。
* Vulkan - 仅包含 Vulkan。
* OpenGL and Vulkan - 同时包含 OpenGL 和 Vulkan。Vulkan 将是默认选项，如果 Vulkan 不可用则回退到 OpenGL。

## HTML5 平台设置

### 浏览器版本

设置 HTML5 构建要支持的最低浏览器版本。这会影响最终二进制文件的大小，因为引擎会包含所有必要的 polyfill 来支持指定的浏览器版本。

* 默认值 - 包含所有 polyfill，支持所有浏览器。
* ES2015 - 包含支持 ES2015（或更高版本）浏览器所需的 polyfill。
* ES2017 - 包含支持 ES2017（或更高版本）浏览器所需的 polyfill。
* ES2019 - 包含支持 ES2019（或更高版本）浏览器所需的 polyfill。
* ES2021 - 包含支持 ES2021（或更高版本）浏览器所需的 polyfill。

### 内存设置

控制 HTML5 构建的内存设置。这会影响最终二进制文件的大小，因为引擎会包含所有必要的 polyfill 来支持指定的内存设置。

* 默认值 - 包含所有 polyfill，支持所有内存设置。
* 128MB - 包含支持 128MB 内存设置所需的 polyfill。
* 256MB - 包含支持 256MB 内存设置所需的 polyfill。
* 512MB - 包含支持 512MB 内存设置所需的 polyfill。
* 1GB - 包含支持 1GB 内存设置所需的 polyfill。
