| System   | Graphics API               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 or Vulkan | Metal is the default; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 or DirectX 12 | DX12 is the default from 1.14.2; select additional backends in the [app manifest](/manuals/app-manifest/#graphics) for fallback |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 | From 1.14.2, Vulkan is preferred with OpenGL fallback |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | From 1.14.2, Vulkan is preferred with OpenGL ES fallback |
| Android  | OpenGLES 3.0 or Vulkan 1.1 | Optional fallback to OpenGLES 2.0 (see below) |
| iOS devices | OpenGLES 3.0, Metal or Vulkan | OpenGLES is the default; Vulkan via MoltenVK |
| iOS simulator | Metal                | Always Metal |
| HTML5    | WebGL 2.0 or WebGPU        | Optional fallback to WebGL 1.0 (see below) |

In Defold 1.14.1, Windows and Linux x86-64 default to OpenGL, and Linux ARM64 defaults to OpenGL ES. See the [application manifest graphics settings](/manuals/app-manifest/#graphics) for backend selection and fallback behavior.

Since Defold 1.14.1, OpenGLES 2.0 and WebGL 1.0 shaders are excluded by default. To support these graphics APIs, disable [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project* (`shader.exclude_gles_sm100 = 0`).
