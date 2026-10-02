| Sistema  | API gráfica                | Observação                |
|----------|----------------------------|---------------------------|
| macOS    | Metal, OpenGL 3.3 ou Vulkan | Metal é o padrão desde o Defold 1.14.0; Vulkan via MoltenVK |
| Windows  | OpenGL 3.3 ou Vulkan 1.1   |                           |
| Linux x86-64 | OpenGL 3.3 ou Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES ou Vulkan 1.1   | EGL/GLES é o padrão    |
| Android  | OpenGLES 3.0 ou Vulkan 1.1 | Fallback para OpenGLES 2.0 |
| Dispositivos iOS | OpenGLES 3.0, Metal ou Vulkan | OpenGLES é o padrão; Vulkan via MoltenVK |
| Simulador iOS | Metal                | Sempre Metal a partir do Defold 1.14.0 |
| HTML5    | WebGL 2.0 ou WebGPU        | Fallback para WebGL 1.0   |
