| System   | Graphics API               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal、OpenGL 3.3 或 Vulkan | 从 Defold 1.14.0 开始默认使用 Metal；通过 MoltenVK 使用 Vulkan |
| Windows  | OpenGL 3.3 或 Vulkan 1.1   |                          |
| Linux x86-64 | OpenGL 3.3 或 Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES 或 Vulkan 1.1   | 默认使用 EGL/GLES      |
| Android  | OpenGLES 3.0 或 Vulkan 1.1 | 回退到 OpenGLES 2.0      |
| iOS 设备 | OpenGLES 3.0、Metal 或 Vulkan | 默认使用 OpenGLES；通过 MoltenVK 使用 Vulkan |
| iOS 模拟器 | Metal                  | 从 Defold 1.14.0 开始始终使用 Metal |
| HTML5    | WebGL 2.0 或 WebGPU        | 回退到 WebGL 1.0         |
