| Система  | Графический API            | Примечание               |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 или Vulkan | Metal по умолчанию с Defold 1.14.0; Vulkan через MoltenVK |
| Windows  | OpenGL 3.3 или Vulkan 1.1  |                          |
| Linux x86-64 | OpenGL 3.3 или Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES или Vulkan 1.1   | По умолчанию EGL/GLES  |
| Android  | OpenGLES 3.0 или Vulkan 1.1 | Fallback на OpenGLES 2.0 |
| Устройства iOS | OpenGLES 3.0, Metal или Vulkan | OpenGLES по умолчанию; Vulkan через MoltenVK |
| Симулятор iOS | Metal                | Всегда Metal с Defold 1.14.0 |
| HTML5    | WebGL 2.0 или WebGPU       | Fallback на WebGL 1.0    |
