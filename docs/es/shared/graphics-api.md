| Sistema | API gráfica                | Nota                      |
|---------|----------------------------|---------------------------|
| macOS   | Metal, OpenGL 3.3 o Vulkan | Metal es el predeterminado desde Defold 1.14.0; Vulkan mediante MoltenVK |
| Windows | OpenGL 3.3 o Vulkan 1.1    |                           |
| Linux x86-64 | OpenGL 3.3 o Vulkan 1.1 |                         |
| Linux ARM64  | OpenGL ES o Vulkan 1.1   | EGL/GLES es el predeterminado |
| Android | OpenGLES 3.0 o Vulkan 1.1  | Fallback a OpenGLES 2.0   |
| Dispositivos iOS | OpenGLES 3.0, Metal o Vulkan | OpenGLES es el predeterminado; Vulkan mediante MoltenVK |
| Simulador de iOS | Metal             | Siempre Metal desde Defold 1.14.0 |
| HTML5   | WebGL 2.0 o WebGPU         | Fallback a WebGL 1.0      |
