| 시스템   | 그래픽 API                 | 참고                       |
|----------|----------------------------|--------------------------|
| macOS    | Metal, OpenGL 3.3 또는 Vulkan | 기본값은 Metal, Vulkan은 MoltenVK 사용 |
| Windows  | OpenGL 3.3, Vulkan 1.1 또는 DirectX 12 | 기본값은 OpenGL, [앱 메니페스트](/manuals/app-manifest/#graphics)에서 백엔드 선택 |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 |                          |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | 기본값은 EGL/GLES입니다  |
| Android  | OpenGLES 3.0 또는 Vulkan 1.1 | 선택적으로 OpenGLES 2.0으로 대체 가능(아래 참고) |
| iOS 기기 | OpenGLES 3.0, Metal or Vulkan | 기본값은 OpenGLES; MoltenVK를 통한 Vulkan |
| iOS 시뮬레이터 | Metal                | 항상 Metal |
| HTML5    | WebGL 2.0 또는 WebGPU        | 선택적으로 WebGL 1.0으로 대체 가능(아래 참고) |

Defold 1.14.1 버전부터 OpenGLES 2.0과 WebGL 1.0 쉐이더는 기본적으로 제외됩니다. 이 그래픽 API를 지원하려면 *game.project*에서 [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20)을 비활성화하세요(`shader.exclude_gles_sm100 = 0`).
