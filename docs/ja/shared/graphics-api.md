| システム   | グラフィックス API               | 備考                     |
|----------|----------------------------|--------------------------|
| macOS    | Metal、OpenGL 3.3、Vulkan | デフォルトは Metal。Vulkan は MoltenVK 経由 |
| Windows  | OpenGL 3.3、Vulkan 1.1、DirectX 12 | デフォルトは OpenGL。[App Manifest](/manuals/app-manifest/#graphics) でバックエンドを選択 |
| Linux x86-64 | OpenGL 3.3 または Vulkan 1.1 |                        |
| Linux ARM64  | OpenGL ES または Vulkan 1.1   | デフォルトは EGL/GLES |
| Android  | OpenGLES 3.0、Vulkan 1.1 | 任意で OpenGLES 2.0 へのフォールバック（下記参照） |
| iOS 実機 | OpenGLES 3.0、Metal または Vulkan | 既定値は OpenGLES。Vulkan は MoltenVK 経由 |
| iOS シミュレーター | Metal                | 常に Metal |
| HTML5    | WebGL 2.0、WebGPU        | 任意で WebGL 1.0 へのフォールバック（下記参照） |

Defold 1.14.1 以降では、OpenGLES 2.0 と WebGL 1.0 用のシェーダーはデフォルトで除外されます。これらの API に対応するには、*game.project* の [Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) を無効にします（`shader.exclude_gles_sm100 = 0`）。
