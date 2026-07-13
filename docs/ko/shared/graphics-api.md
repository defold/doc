| 시스템   | 그래픽 API                 | 참고                       |
|----------|----------------------------|----------------------------|
| macOS    | OpenGL 3.3 or Metal        | MoltenVK를 통한 Vulkan     |
| Windows  | OpenGL 3.3 or Vulkan 1.1   |                            |
| Linux x86-64 | OpenGL 3.3 or Vulkan 1.1 |                          |
| Linux ARM64  | OpenGL ES or Vulkan 1.1   | 기본값은 EGL/GLES입니다  |
| Android  | OpenGLES 3.0 or Vulkan 1.1 | OpenGLES 2.0으로 폴백      |
| iOS      | OpenGLES 3.0 or Metal      | MoltenVK를 통한 Vulkan     |
| HTML5    | WebGL 2.0 or WebGPU        | WebGL 1.0으로 폴백         |
