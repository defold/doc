| Sistem   | Grafik API'si              | Not                      |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 veya Vulkan | Varsayılan Metal'dir; MoltenVK aracılığıyla Vulkan |
| Windows  | OpenGL 3.3, Vulkan 1.1 veya DirectX 12 | Varsayılan OpenGL'dir; arka uçları [uygulama bildiriminde](/manuals/app-manifest/#graphics) seçin |
| Linux x86-64 | OpenGL 3.3 veya Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES veya Vulkan 1.1   | Varsayılan EGL/GLES'tir |
| Android  | OpenGLES 3.0 veya Vulkan 1.1 | İsteğe bağlı olarak OpenGLES 2.0'a geri dönüş (aşağıya bakın) |
| iOS cihazları | OpenGLES 3.0, Metal veya Vulkan | Varsayılan OpenGLES'tir; MoltenVK aracılığıyla Vulkan |
| iOS simülatörü | Metal                | Her zaman Metal |
| HTML5    | WebGL 2.0 veya WebGPU        | İsteğe bağlı olarak WebGL 1.0'a geri dönüş (aşağıya bakın) |

Defold 1.14.1'den itibaren OpenGLES 2.0 ve WebGL 1.0 gölgelendiricileri varsayılan olarak dışarıda bırakılır. Bu grafik API'lerini desteklemek için *game.project* dosyasında [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) ayarını devre dışı bırakın (`shader.exclude_gles_sm100 = 0`).
