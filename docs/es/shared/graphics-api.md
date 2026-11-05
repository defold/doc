| Sistema | API gráfica                | Nota                      |
|---------|----------------------------|---------------------------|
| macOS    | Metal, OpenGL 3.3 o Vulkan | Metal es el predeterminado; Vulkan mediante MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 o DirectX 12 | OpenGL es el predeterminado; selecciona los backends en el [manifiesto de aplicación](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 o Vulkan 1.1 |                         |
| Linux ARM64  | OpenGL ES o Vulkan 1.1   | EGL/GLES es el predeterminado |
| Android  | OpenGLES 3.0 o Vulkan 1.1 | Cambio opcional a OpenGLES 2.0 (consulta más abajo) |
| Dispositivos iOS | OpenGLES 3.0, Metal o Vulkan | OpenGLES es el predeterminado; Vulkan mediante MoltenVK |
| Simulador de iOS | Metal                | Siempre Metal |
| HTML5    | WebGL 2.0 o WebGPU        | Cambio opcional a WebGL 1.0 (consulta más abajo) |

Desde Defold 1.14.1, los shaders OpenGLES 2.0 y WebGL 1.0 se excluyen de forma predeterminada. Para admitir estas API gráficas, desactiva [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) en *game.project* (`shader.exclude_gles_sm100 = 0`).
