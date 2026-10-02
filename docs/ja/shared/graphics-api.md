| システム   | グラフィックス API               | 備考                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal、OpenGL 3.3 または Vulkan | Defold 1.14.0 以降の既定値は Metal。Vulkan は MoltenVK 経由 |
| Windows  | OpenGL 3.3 または Vulkan 1.1   |                          |
| Linux x86-64 | OpenGL 3.3 または Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES または Vulkan 1.1   | デフォルトは EGL/GLES |
| Android  | OpenGLES 3.0 または Vulkan 1.1 | OpenGLES 2.0 にフォールバック |
| iOS 実機 | OpenGLES 3.0、Metal または Vulkan | 既定値は OpenGLES。Vulkan は MoltenVK 経由 |
| iOS シミュレーター | Metal                | Defold 1.14.0 以降は常に Metal |
| HTML5    | WebGL 2.0 または WebGPU        | WebGL 1.0 にフォールバック    |
