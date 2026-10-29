| System   | Graphics API               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 or Vulkan | Metal is the default since Defold 1.14.0; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 or DirectX 12 | OpenGL is the default; select backends in the [app manifest](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | EGL/GLES is the default |
| Android  | OpenGLES 3.0 or Vulkan 1.1 | Optional fallback to OpenGLES 2.0 (see below) |
| iOS devices | OpenGLES 3.0, Metal or Vulkan | OpenGLES is the default; Vulkan via MoltenVK |
| iOS simulator | Metal                | Always Metal since Defold 1.14.0 |
| HTML5    | WebGL 2.0 or WebGPU        | Optional fallback to WebGL 1.0 (see below) |

Since Defold 1.14.1, OpenGLES 2.0 and WebGL 1.0 shaders are excluded by default. To support these graphics APIs, disable [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project* (`shader.exclude_gles_sm100 = 0`).
