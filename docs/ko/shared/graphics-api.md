| 시스템   | 그래픽 API                 | 참고                       |
|----------|----------------------------|----------------------------|
| macOS    | Metal, OpenGL 3.3 or Vulkan | Defold 1.14.0부터 기본값은 Metal; MoltenVK를 통한 Vulkan |
| Windows  | OpenGL 3.3 or Vulkan 1.1   |                            |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 |                          |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | 기본값은 EGL/GLES입니다  |
| Android  | OpenGLES 3.0 or Vulkan 1.1 | OpenGLES 2.0으로 폴백      |
| iOS 기기 | OpenGLES 3.0, Metal or Vulkan | 기본값은 OpenGLES; MoltenVK를 통한 Vulkan |
| iOS 시뮬레이터 | Metal                | Defold 1.14.0부터 항상 Metal |
| HTML5    | WebGL 2.0 or WebGPU        | WebGL 1.0으로 폴백         |
