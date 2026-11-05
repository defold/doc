| Sistema  | API gráfica                | Observação                |
|----------|----------------------------|---------------------------|
| macOS    | Metal, OpenGL 3.3 ou Vulkan | Metal é o padrão; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 ou DirectX 12 | OpenGL é o padrão; selecione os backends no [app manifest](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 ou Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES ou Vulkan 1.1   | EGL/GLES é o padrão    |
| Android  | OpenGLES 3.0 ou Vulkan 1.1 | Fallback opcional para OpenGLES 2.0 (veja abaixo) |
| Dispositivos iOS | OpenGLES 3.0, Metal ou Vulkan | OpenGLES é o padrão; Vulkan via MoltenVK |
| Simulador iOS | Metal                | Sempre Metal |
| HTML5    | WebGL 2.0 ou WebGPU        | Fallback opcional para WebGL 1.0 (veja abaixo) |

Desde o Defold 1.14.1, shaders OpenGLES 2.0 e WebGL 1.0 são excluídos por padrão. Para oferecer suporte a essas APIs gráficas, desabilite [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) em *game.project* (`shader.exclude_gles_sm100 = 0`).
