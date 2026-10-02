| Système   | API graphique               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 ou Vulkan | Metal est utilisé par défaut depuis Defold 1.14.0 ; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3 ou Vulkan 1.1   |                          |
| Linux x86-64 | OpenGL 3.3 ou Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES ou Vulkan 1.1   | EGL/GLES est utilisé par défaut |
| Android  | OpenGLES 3.0 ou Vulkan 1.1 | Repli sur OpenGLES 2.0 |
| Appareils iOS | OpenGLES 3.0, Metal ou Vulkan | OpenGLES est utilisé par défaut ; Vulkan via MoltenVK |
| Simulateur iOS | Metal                | Toujours Metal depuis Defold 1.14.0 |
| HTML5    | WebGL 2.0 ou WebGPU        | Repli sur WebGL 1.0    |
