| Система   | Графический API               | Примечание                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 или Vulkan | По умолчанию Metal; Vulkan через MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 или DirectX 12 | По умолчанию OpenGL; бэкенды выбираются в [манифесте приложения](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 или Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES или Vulkan 1.1   | По умолчанию EGL/GLES |
| Android  | OpenGLES 3.0 или Vulkan 1.1 | Необязательный переход на OpenGLES 2.0 (см. ниже) |
| Устройства iOS | OpenGLES 3.0, Metal или Vulkan | По умолчанию OpenGLES; Vulkan через MoltenVK |
| Симулятор iOS | Metal                | Всегда Metal |
| HTML5    | WebGL 2.0 или WebGPU        | Необязательный переход на WebGL 1.0 (см. ниже) |

Начиная с Defold 1.14.1, шейдеры OpenGLES 2.0 и WebGL 1.0 по умолчанию исключены. Для поддержки этих графических API отключите [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) в *game.project* (`shader.exclude_gles_sm100 = 0`).
