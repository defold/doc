| System   | Graphics API               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal、OpenGL 3.3 或 Vulkan | 默认使用 Metal；Vulkan 通过 MoltenVK 提供 |
| Windows  | OpenGL 3.3、Vulkan 1.1 或 DirectX 12 | 默认使用 OpenGL；在[应用清单](/manuals/app-manifest/#graphics)中选择后端 |
| Linux x86-64 | OpenGL 3.3 或 Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES 或 Vulkan 1.1   | 默认使用 EGL/GLES      |
| Android  | OpenGLES 3.0 或 Vulkan 1.1 | 可选回退到 OpenGLES 2.0（见下文） |
| iOS 设备 | OpenGLES 3.0、Metal 或 Vulkan | 默认使用 OpenGLES；通过 MoltenVK 使用 Vulkan |
| iOS 模拟器 | Metal                | 始终使用 Metal |
| HTML5    | WebGL 2.0 或 WebGPU        | 可选回退到 WebGL 1.0（见下文） |

从 Defold 1.14.1 起，默认排除 OpenGLES 2.0 和 WebGL 1.0 着色器。要支持这些图形 API，请在 *game.project* 中禁用 [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20)（`shader.exclude_gles_sm100 = 0`）。
