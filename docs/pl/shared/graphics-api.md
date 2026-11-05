| System operacyjny | API graficzne | Uwagi |
|---|---|---|
| macOS | Metal, OpenGL 3.3 lub Vulkan | Domyślnie Metal; Vulkan przez MoltenVK |
| Windows | OpenGL 3.3, Vulkan 1.1 lub DirectX 12 | Domyślnie OpenGL; backendy wybiera się w [manifeście aplikacji](/manuals/app-manifest/#graphics) |
| Linux x86-64 | OpenGL 3.3 lub Vulkan 1.1 | |
| Linux ARM64 | OpenGL ES lub Vulkan 1.1 | Domyślnie EGL/GLES |
| Android | OpenGLES 3.0 lub Vulkan 1.1 | Opcjonalne przełączanie na OpenGLES 2.0 (patrz niżej) |
| Urządzenia iOS | OpenGLES 3.0, Metal lub Vulkan | Domyślnie OpenGLES; Vulkan przez MoltenVK |
| Symulator iOS | Metal | Zawsze Metal |
| HTML5 | WebGL 2.0 lub WebGPU | Opcjonalne przełączanie na WebGL 1.0 (patrz niżej) |

Od wersji Defold 1.14.1 shadery OpenGLES 2.0 i WebGL 1.0 są domyślnie wykluczone. Aby obsługiwać te API graficzne, wyłącz [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) w *game.project* (`shader.exclude_gles_sm100 = 0`).
