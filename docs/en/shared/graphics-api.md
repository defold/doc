| System   | Graphics API               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 or Vulkan | Metal is the default since Defold 1.14.0; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3 or Vulkan 1.1   |                          |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | EGL/GLES is the default |
| Android  | OpenGLES 3.0 or Vulkan 1.1 | Fallback to OpenGLES 2.0 |
| iOS devices | OpenGLES 3.0, Metal or Vulkan | OpenGLES is the default; Vulkan via MoltenVK |
| iOS simulator | Metal                | Always Metal since Defold 1.14.0 |
| HTML5    | WebGL 2.0 or WebGPU        | Fallback to WebGL 1.0    |
