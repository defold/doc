| Sistema   | API grafica               | Note                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 o Vulkan | Metal è il valore predefinito; Vulkan tramite MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 o DirectX 12 | OpenGL è il valore predefinito; seleziona i backend nell'[app manifest](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 o Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES o Vulkan 1.1   | EGL/GLES è l'opzione predefinita |
| Android  | OpenGLES 3.0 o Vulkan 1.1 | Ripiego facoltativo su OpenGLES 2.0 (vedi sotto) |
| Dispositivi iOS | OpenGLES 3.0, Metal o Vulkan | OpenGLES è l'opzione predefinita; Vulkan tramite MoltenVK |
| Simulatore iOS | Metal                | Sempre Metal |
| HTML5    | WebGL 2.0 o WebGPU        | Ripiego facoltativo su WebGL 1.0 (vedi sotto) |

Da Defold 1.14.1, gli shader OpenGLES 2.0 e WebGL 1.0 sono esclusi per impostazione predefinita. Per supportare queste API grafiche, disabilita [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project* (`shader.exclude_gles_sm100 = 0`).
