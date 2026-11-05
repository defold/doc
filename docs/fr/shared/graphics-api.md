| Système   | API graphique               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 ou Vulkan | Metal est utilisé par défaut ; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 ou DirectX 12 | OpenGL est utilisé par défaut ; sélectionnez les backends dans le [manifeste d'application](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 ou Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES ou Vulkan 1.1   | EGL/GLES est utilisé par défaut |
| Android  | OpenGLES 3.0 ou Vulkan 1.1 | Repli facultatif sur OpenGLES 2.0 (voir ci-dessous) |
| Appareils iOS | OpenGLES 3.0, Metal ou Vulkan | OpenGLES est utilisé par défaut ; Vulkan via MoltenVK |
| Simulateur iOS | Metal                | Toujours Metal |
| HTML5    | WebGL 2.0 ou WebGPU        | Repli facultatif sur WebGL 1.0 (voir ci-dessous) |

Depuis Defold 1.14.1, les shaders OpenGLES 2.0 et WebGL 1.0 sont exclus par défaut. Pour prendre en charge ces API graphiques, désactivez [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) dans *game.project* (`shader.exclude_gles_sm100 = 0`).
