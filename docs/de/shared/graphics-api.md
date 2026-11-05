| System   | Grafik-API                 | Hinweis                  |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 oder Vulkan | Metal ist Standard; Vulkan über MoltenVK |
| Windows  | OpenGL 3.3, Vulkan 1.1 oder DirectX 12 | OpenGL ist Standard; Backends im [Anwendungsmanifest](/manuals/app-manifest/#graphics) auswählen |
| Linux x86-64 | OpenGL 3.3 oder Vulkan 1.1 |                      |
| Linux ARM64  | OpenGL ES oder Vulkan 1.1 | EGL/GLES ist der Standard |
| Android  | OpenGLES 3.0 oder Vulkan 1.1 | Optionaler Rückfall auf OpenGLES 2.0 (siehe unten) |
| iOS-Geräte | OpenGLES 3.0, Metal oder Vulkan | OpenGLES ist der Standard; Vulkan über MoltenVK |
| iOS-Simulator | Metal                | Immer Metal |
| HTML5    | WebGL 2.0 oder WebGPU        | Optionaler Rückfall auf WebGL 1.0 (siehe unten) |

Seit Defold 1.14.1 sind OpenGLES-2.0- und WebGL-1.0-Shader standardmäßig ausgeschlossen. Deaktiviere zur Unterstützung dieser Grafik-APIs [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) in *game.project* (`shader.exclude_gles_sm100 = 0`).
