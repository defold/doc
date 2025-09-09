---
title: 应用程序清单
brief: 本手册描述了如何使用应用程序清单来排除引擎中的功能。
---

# 应用程序清单

应用程序清单用于排除或控制要在引擎中包含哪些功能。排除引擎中未使用的功能是推荐的最佳实践，因为它会减小游戏的最终二进制文件大小。
此外，应用程序清单还包含一些用于控制 HTML5 平台代码编译的选项，如最低支持的浏览器版本/内存设置，这些也会影响结果二进制文件的大小。

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# 应用清单

在 `game.project` 中，将清单分配给 `Native Extensions` -> `App Manifest`。

## 物理

控制使用哪个物理引擎，或选择 None 来完全排除物理功能。

## 物理 2D

选择使用哪个版本的 Box2D。

## 骨骼 + 模型

控制骨骼和模型功能，或选择 None 来完全排除模型和骨骼功能。（参见[`模型`](https://defold.com/manuals/model/#model-component)文档）。

## 排除录制

从引擎中排除视频录制功能（参见[`start_record`](https://defold.com/ref/stable/sys/#start_record)消息文档）。

## 排除分析器

从引擎中排除分析器。分析器用于收集性能和使用计数器。在[分析手册](/manuals/profiling/)中学习如何使用分析器。

## 排除声音

从引擎中排除所有声音播放功能。

## 排除输入

从引擎中排除所有输入处理功能。

## 排除热更新

从引擎中排除[热更新功能](/manuals/live-update)。

## 排除图像

从引擎中排除`image`脚本模块[链接](https://defold.com/ref/stable/image/)。

## 排除类型

从引擎中排除`types`脚本模块[链接](https://defold.com/ref/stable/types/)。

## 排除 Basis Universal

从引擎中排除 Basis Universal[纹理压缩库](/manuals/texture-profiles)。

## 使用 Android 支持库

使用已弃用的 Android 支持库而不是 Android X。[更多信息](https://defold.com/manuals/android/#using-androidx)。

## 图形

选择使用哪个图形后端。

* OpenGL - 仅包含 OpenGL。
* Vulkan - 仅包含 Vulkan。
* OpenGL and Vulkan - 同时包含 OpenGL 和 Vulkan。Vulkan 将是默认选项，如果 Vulkan 不可用则回退到 OpenGL。

## 最低 Safari 版本（仅适用于 js-web 和 wasm-web）
YAML 字段名称：**`minSafariVersion`**
默认值：**90000**

支持的最低 Safari 版本。不能低于 90000。更多信息请查看 Emscripten 编译器选项[链接](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-safari-version)。

## 最低 Firefox 版本（仅适用于 js-web 和 wasm-web）
YAML 字段名称：**`minFirefoxVersion`**
默认值：**34**

支持的最低 Firefox 版本。不能低于 34。更多信息请查看 Emscripten 编译器选项[链接](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-firefox-version)。

## 最低 Chrome 版本（仅适用于 js-web 和 wasm-web）
YAML 字段名称：**`minChromeVersion`**
默认值：**32**

支持的最低 Chrome 版本。不能低于 32。更多信息请查看 Emscripten 编译器选项[链接](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#min-chrome-version)。

## 初始内存（仅适用于 js-web 和 wasm-web）
YAML 字段名称：**`initialMemory`**
默认值：**33554432**

为 Web 应用程序分配的内存大小。如果 ALLOW_MEMORY_GROWTH=0（js-web）- 这是 Web 应用程序可以使用的内存总量。更多信息请查看[链接](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#initial-memory)。单位为字节。注意该值必须是 WebAssembly 页面大小（64KiB）的倍数。
该选项与 *game.project* 中的 `html5.heap_size` [相关](https://defold.com/manuals/html5/#heap-size)。通过应用程序清单配置的选项在编译期间设置，并用作 `INITIAL_MEMORY` 选项的默认值。*game.project* 中的值会覆盖应用程序清单中的值，并在运行时使用。

## 栈大小（仅适用于 js-web 和 wasm-web）
YAML 字段名称：**`stackSize`**
默认值：**5242880**

应用程序的栈大小。更多信息请查看[链接](https://emscripten.org/docs/tools_reference/settings_reference.html?highlight=environment#stack-size)。单位为字节。
