| Система | Графічний API | Примітка |
|----------|----------------------------|--------------------------|
| macOS | Metal, OpenGL 3.3 або Vulkan | Metal використовується за замовчуванням; Vulkan через MoltenVK |
| Windows | OpenGL 3.3, Vulkan 1.1 або DirectX 12 | OpenGL використовується за замовчуванням; виберіть бекенди в [маніфесті застосунку](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 або Vulkan 1.1 | |
| Linux ARM64 | OpenGL ES або Vulkan 1.1 | Типово використовується EGL/GLES |
| Android | OpenGLES 3.0 або Vulkan 1.1 | Необов’язковий резервний варіант — OpenGLES 2.0 (див. нижче) |
| Пристрої iOS | OpenGLES 3.0, Metal або Vulkan | Типово використовується OpenGLES; Vulkan через MoltenVK |
| Симулятор iOS | Metal | Завжди Metal |
| HTML5 | WebGL 2.0 або WebGPU | Необов’язковий резервний варіант — WebGL 1.0 (див. нижче) |

Починаючи з Defold 1.14.1, шейдери OpenGLES 2.0 і WebGL 1.0 за замовчуванням виключено. Щоб підтримувати ці графічні API, вимкніть [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) у *game.project* (`shader.exclude_gles_sm100 = 0`).
