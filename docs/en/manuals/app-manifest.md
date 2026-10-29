---
title: App manifest
brief: This manual describes how the app manifest can be used to exclude features from the engine.
---

# App manifest

The application manifest controls which features and backends are linked into the engine. Excluding unused features is recommended because it decreases the final binary size of your game. The application manifest also contains build-time options such as the minimum supported HTML5 browser versions and WebAssembly memory settings.

![](images/app_manifest/create-app-manifest.png)

# Applying the manifest

In `game.project`, assign the manifest to `Native Extensions` -> `App Manifest`.

## Physics 2D

Select which Box2D implementation to include:

* **Box2D Version 3** - Include Box2D 3. This is opt-in and may produce different simulation results than the legacy implementation, so existing projects may need to retune their physics settings.
* **Box2D (Legacy Defold version)** - Include the legacy Defold Box2D implementation. This is the default.
* **None** - Exclude 2D physics.

The Box2D solver settings are version-specific. See the [Box2D project settings](/manuals/project-settings/#box2d) for details.

## Physics 3D

Include the Bullet 3D physics implementation. It is included by default; disable this setting to exclude 3D physics.

## Rig + Model

Control rig and model functionality, or select None to exclude model and rig completely. (See [`Model`](https://defold.com/manuals/model/#model-component) documentation).


## Exclude Record

Exclude native MP4 recording, the [`recorder` Lua module](/ref/recorder/) and the recording HTTP service from desktop debug builds. Recording is already omitted from release, headless, mobile and web builds. See the [recording manual](/manuals/recording) for the workflow.


## Profiler

Control when profiler functionality is linked into the engine:

* **Debug Only** - Include the profiler in debug builds only. This is the default.
* **None** - Exclude profiler functionality from all build variants.
* **Always** - Include the profiler in both debug and release builds.

The app-manifest setting controls whether the profiler code is linked into a build. The settings under `profiler` in *game.project* control profiler behavior at runtime. Learn how to use the available facilities in the [Profiling manual](/manuals/profiling/).


## Sound

The sound controls determine which sound system and decoders are linked into the engine.

### Exclude Sound

Exclude all sound playing capabilities from the engine.

### Exclude Sound Decoder: WAV

Exclude support for WAV sound resources.

### Exclude Sound Decoder: OGG

Exclude support for Ogg Vorbis sound resources.

### Include Sound Decoder: Opus

Include support for Ogg Opus sound resources. The Opus decoder is excluded by default, so this option must be enabled before `.opus` resources can be played. See the [Sound manual](/manuals/sound/) for supported formats.


## Exclude Input

Exclude all input handling from the engine.


## Exclude GUI

Remove GUI resources, components and Lua support from the engine. Enable this only if the project does not use GUI scenes or GUI scripts. Label components remain available. This option is disabled by default.


## Exclude Particle FX

Remove particle effect resources, components and the `particlefx` Lua module. This also removes support for particle nodes in GUI scenes; GUI scenes without particle nodes remain supported. Remove references to particle effects and calls to their APIs before enabling this option. It is disabled by default.


## Exclude Tilemaps

Remove tilemap resources, components and the `tilemap` Lua module. Enable this only if the project does not use tilemap components or their APIs. Tile sources used by other components remain available. This option is disabled by default.


## Exclude Live Update

Exclude the [Live Update functionality](/manuals/live-update) from the engine.


## Exclude Image

Exclude `image` script module [link](https://defold.com/ref/image/) from the engine.


## Exclude Types

Exclude `types` script module [link](https://defold.com/ref/types/) from the engine.


## Exclude Basis Transcoder

Exclude the Basis Universal [texture compression library](/manuals/texture-profiles) from the engine.


## Use Android Support Lib

Use the deprecated Android Support Library instead of Android X. [More info](https://defold.com/manuals/android/#using-androidx).


## Graphics

Select which graphics backends to include for each platform. A combined choice includes multiple backends so the engine can fall back when its preferred backend is unavailable. Including more backends increases engine size.

Windows and Linux use separate fields. The **DX12** option selects DirectX 12 on Windows.

| Field | Platforms | Choices | Default |
|---|---|---|---|
| **Graphics (Linux)** | Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (Windows)** | Windows | OpenGL, Vulkan, DX12, OpenGL & Vulkan, OpenGL & DX12, Vulkan & DX12, OpenGL & Vulkan & DX12 | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Metal |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

On Linux ARM64, the **OpenGL** choice uses the OpenGL ES backend. The Android combined default prefers Vulkan when available and falls back to OpenGL ES.

Since Defold 1.14.0, macOS uses the native Metal backend by default. The **Vulkan** choice on macOS and iOS uses Vulkan through MoltenVK. The iOS simulator (`arm64_sim-ios`) always uses Metal, regardless of the **Graphics (iOS)** choice for devices.

## Use full text layout system

If enabled (`true`), this includes the full text layout system for shaping text, including right-to-left languages. Enable this option to use runtime generation for TrueType (`.ttf`) or OpenType (`.otf`) fonts, and set *Glyph Generation* to **Dynamic** in each font resource that needs it. Dynamic generation supports both **SDF** and **Vector** modes. The former `font.runtime_generation` setting in *game.project* is deprecated and has no effect. Read more in the [Font Manual](/manuals/font/#enabling-runtime-fonts).


## Use Rich Text

Include rich text parsing and style effects for labels and GUI text. This option is enabled by default. Disable it to reduce engine size when the project only needs plain text. Labels and GUI text remain supported, but markup renders as plain text instead of applying formatting or effects.


## Minimum browser versions

The YAML fields **`minSafariVersion`**, **`minFirefoxVersion`**, and **`minChromeVersion`** specify the minimum browser versions targeted by Emscripten. The current defaults and minimum supported versions differ between the non-threaded and threaded targets:

| Target | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Specify overrides in the context for the relevant target. The threaded target also has additional [hosting requirements](/manuals/html5/#creating-html5-bundle). See the Emscripten settings reference for [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version), and [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version).

## Initial memory (HTML5)
YAML field name: **`initialMemory`**
Default value: **33554432**

The initial amount of memory allocated for the web application, in bytes. The value must be a multiple of the WebAssembly page size (64 KiB). See Emscripten's [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) setting.

This option supplies the compile-time default. The [`html5.heap_size`](/manuals/html5/#heap-size) value in *game.project* overrides it at runtime.

## Stack size (HTML5)
YAML field name: **`stackSize`**
Default value: **5242880**

The application stack size, in bytes. See Emscripten's [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) setting.
