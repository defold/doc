---
title: 使用 HTTP 自动操作 Defold 编辑器
brief: 本手册介绍外部工具如何发现和使用已打开 Defold 编辑器项目的本地 HTTP API。
---

# 自动操作 Defold 编辑器

Defold 编辑器会为自动化操作开放一个专用服务器。HTTP API 用于控制打开的项目。它可用于编辑器命令、构建、项目资源、预览、偏好设置、控制台输出、文档搜索或编辑器脚本集成。若要检查或控制运行中的游戏，请改用[引擎服务或运行时自动化 API](/manuals/engine-service)。

::: important
编辑器 HTTP API 尚处于实验阶段，可能会随 Defold 版本而变化。运行中的编辑器所生成的 `/openapi.json` 文档，是其可用操作和模式的权威来源。
:::

## 从外部工具启动编辑器

外部工具需要编辑器可执行文件，以及项目 `game.project` 文件的绝对路径。

可以按照[编辑器手册](/manuals/editor/#editor-installation-metadata)中的说明，通过 `installations.json` 找到已安装的 Defold 版本。其 `launcherPath` 字段包含要启动的可执行文件。将 `game.project` 路径作为第一个位置参数传入，即可直接打开该项目。

可选的 `--port` 或 `-p` 参数用于选择编辑器服务器端口。省略该参数会让 Defold 选择一个可用端口；当可能同时打开多个项目时，通常应采用这种方式。

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

编辑器是图形桌面应用程序。请在可以访问显示器的交互式用户会话中启动它。当图形会话不可用（例如在无头 CI 中），或只需执行编译自动化和创建独立包时，请使用 [Bob](/manuals/bob)。

启动编辑器后，请等待项目打开且 `.internal/editor.port` 出现。然后轮询 `/openapi.json`，直到它返回有效文档。不要因为进程已创建就认为项目已经就绪。

## 定位编辑器服务器

项目打开期间，编辑器会启动本地 HTTP 服务器。选择 <kbd>Help ▸ Open Editor Server</kbd>，可在默认浏览器中打开其主页：

![本地编辑器服务器主页](images/automation/editor_server.png)

所选端口会写入项目内的以下文件：

```text
.internal/editor.port
```

本手册后续示例和命令将使用以下 Shell 变量：

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

端口文件属于当前编辑器会话。重新启动编辑器后应再次读取该文件。

::: important
编辑器服务器是受信任的本地控制接口。不要通过公共地址、端口转发或不受信任的隧道将其公开。
:::

## 通过 OpenAPI 发现操作

外部工具唯一需要了解的 Defold 专用引导信息，是编辑器端口和 OpenAPI 文档：

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

返回的 OpenAPI 3.0.3 文档描述运行中编辑器版本所支持的操作，包括路径、方法、参数、命令名称、请求格式、响应、状态码和身份验证要求。

列出文档中的路径：

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

列出可用的编辑器命令：

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

了解版本的集成应验证所需的每项操作，并根据返回的模式配置请求。不建议维护一份据称包含全部端点或命令名称的副本，因为它可能会过时。

当项目定义的路由由编辑器脚本提供 OpenAPI 操作描述时，它们也会出现在 `/openapi.json` 中。

## 执行编辑器命令

编辑器命令通过以下路径调用：

```text
POST /command/{command}
```

例如，当前的 `build` 命令会编译并运行项目：

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

构建成功时会返回结构化结果：

```json
{
  "success": true,
  "issues": []
}
```

构建失败时会返回 HTTP 状态 `422`，并附带如下问题：

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

可用字段取决于错误类型。当资源路径和源代码范围存在时应使用它们，但也应能够处理仅包含消息的问题。

运行中的编辑器列出时，常用命令包括：

`build`
: 编译并运行项目。

`clean-build`
: 清除构建缓存，然后编译并运行。仅当常规构建表现不一致或似乎遗漏了更改时才使用此命令。

`build-html5`
: 为 HTML5 构建项目，并通过编辑器服务器提供输出。

`fetch-libraries`
: 下载并重新加载项目依赖项。

`hot-reload`
: 将修改后的资源重新加载到运行中的游戏。

`reload-extensions`
: 重新加载编辑器脚本。

`debugger-start`、`debugger-stop` 和调试器单步命令
: 控制调试会话和运行中的项目。

确切名称和可用性取决于编辑器版本和当前编辑器状态；请通过 `/openapi.json` 发现它们。

对项目资源执行操作的命令，会在执行前同步外部文件更改。

### 命令响应和异步工作

命令操作会在当前 OpenAPI 模式中说明响应码。

| 状态 | 含义 |
| --- | --- |
| `200` | 命令已完成并返回结果 |
| `202` | 命令已接受，并继续异步执行 |
| `403` | 命令在当前编辑器状态下未激活 |
| `404` | 命令不可用 |
| `422` | 构建或验证失败 |
| `500` | 发生编辑器内部错误 |

HTTP `202` 响应并不能证明请求的结果已经存在。应等待相关输出、资源、控制台标记或服务 URL，并实施超时。

### 构建 HTML5 {#building-html5}

如果当前 OpenAPI 文档列出了 `build-html5`，请通过命令操作调用它：

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

该命令异步运行，通常返回 HTTP `202`。构建完成后，编辑器会在以下位置提供该构建：

```text
http://127.0.0.1:<editor-port>/html5/
```

开始浏览器测试前，请等待该 URL 可用。更多详情请参阅 [HTML5 的浏览器测试](/manuals/automated-testing/#browser-tests-for-html5)。

## 搜索 API 文档

当 `/openapi.json` 中存在 `/ref` 操作时，它会搜索运行中编辑器版本所包含的 API 文档，并提供与该版本匹配的名称和签名。

例如，要搜索函数，请使用：

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

按环境和语言筛选：

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

搜索参数为：

`environment`
: `editor`、`runtime` 或以逗号分隔的值。

`language`
: `Lua`、`C`、`C++` 或以逗号分隔的值。

`q`
: 不区分大小写的表达式。空白表示 AND，而 `|` 表示 OR。

此外还有精简的文档资源：[LLM 文档索引](https://defold.com/llms.txt)链接到官方手册、API 命名空间和示例，[完整 LLM 文档](https://defold.com/llms-full.txt)则列出完整文档，以支持离线搜索和本地索引。

当只需要一个 API 或消息时，AI 智能体应优先执行针对性搜索，而不是检索完整参考资料，以节省 token，并为给定任务准备更完善、更干净的上下文。

## 读取控制台输出 {#reading-console-output}

以 JSON 格式读取编辑器控制台：

```sh
curl -sS "$BASE_URL/console" | jq
```

响应的 `lines` 中包含控制台文本，`regions` 中包含语义区域，包括错误、求值结果和资源引用。

要持续跟踪控制台输出，请使用：

```sh
curl -N "$BASE_URL/console/stream"
```

该流包含现有控制台行，随后保持打开以接收新输出。在收到完成标记或错误、检测到进程终止，或达到超时或行数限制后关闭该流。

有关测试结果分帧和失败分类，请参阅[自动化测试与验证](/manuals/automated-testing/#structured-test-results)。

## 渲染场景预览 {#rendering-scene-previews}

Defold 编辑器（自 1.13.1 起）可以通过命令 `/preview/{path}`，将受支持场景资源的“截图”渲染为 PNG：

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

这会在默认初始视图中渲染已打开 Basic 3D 模板项目的主集合：

![编辑器渲染的主集合预览](images/automation/main-preview.png)

可以使用渲染来获取利用可视化场景编辑器的资源预览。例如，可以用同样的方式渲染模型组件，从而验证其外观或着色器是否正确：

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![编辑器渲染的立方体模型预览](images/automation/cube-preview.png)

`/preview/` 后的路径不包含前导斜杠。可选尺寸默认使用项目显示大小，且必须介于 `1` 和 `4096` 之间。

| 状态 | 含义 |
| --- | --- |
| `200` | 预览已渲染 |
| `400` | 尺寸无效 |
| `404` | 未找到资源 |
| `422` | 资源未加载或不支持场景预览 |

预览对于项目的视觉分析非常有用，例如检查关卡布局、GUI 布局、着色器和光照设置、视觉回归，或创建文档缩略图。

::: important
编辑器预览不是运行中游戏的截图。它不会验证动态创建的对象、运行时后处理或特定于平台的渲染。当需要验证这些元素时，请使用[运行时截图](/manuals/automated-testing/#editor-previews-and-runtime-screenshots)。
:::

## 执行编辑器 Lua

经过身份验证的 `POST /eval` 操作会在编辑器扩展环境中执行 Lua。每个会话的 bearer token 存储在：

```text
.internal/editor.token
```

读取令牌并执行代码：

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

打印输出和返回值会以文本形式返回。典型响应为：

| 状态 | 含义 |
| --- | --- |
| `200` | 代码已执行 |
| `401` | bearer token 缺失或无效 |
| `422` | 无法解析或执行 Lua 代码 |
| `503` | 编辑器扩展环境尚未就绪 |

客户端可以在收到 `503` 后重试，但应限制尝试次数。对于返回 `422` 的请求，应先修正代码再重复请求。

被求值的代码可以使用[编辑器 API](https://defold.com/ref/editor-lua/) 和编辑器脚本环境。它无法使用 `go.*` 等游戏运行时 API 来操作运行中的游戏。对于游戏玩法，请使用运行时测试、调试器、浏览器测试或[运行时自动化 API](/manuals/engine-service/#automation-bridge-extension)。

### 修改资源和文件

许多 Defold 源资源使用文本格式，可以通过任何文本编辑工具进行编辑。修改 Defold 项目的结构化资源时，应优先使用编辑器事务。

| 更改 | 首选方法 |
| --- | --- |
| Lua、着色器、JSON 或其他已知文本格式 | 直接修改文件 |
| 已打开编辑器标签页中尚未保存的文本 | `editor.get()` 和 `editor.transact()` |
| 集合、游戏对象、GUI、图集或其他结构化资源 | 编辑器事务 |
| 重复生成的内容 | 独立生成器 |
| 可重复的项目操作 | 编辑器命令或自定义 HTTP 端点 |
| 仅用于 CI 的转换 | 在 Bob 之前运行的独立脚本 |

更改资源前先进行检查：

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

执行事务前，请检查 `editor.can_get()`、`editor.can_set()` 和其他 `editor.can_*()` 函数。

在编辑器 Lua 中使用 `editor.execute()` 运行格式化工具、验证器或生成器：

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

当命令不会修改项目资源时，请设置 `reload_resources = false`，以避免不必要的重新加载。

::: important
不要修改 `.internal/` 中的文件或 `build/` 中生成的内容。
:::

## 偏好设置

编辑器偏好设置可通过 OpenAPI 文档中说明的路径读取和写入，当前路径为 `/prefs/{path}`。

例如，可以读取配置的代码字体大小：

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

或将其设置为 16：

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

编辑器会根据偏好设置模式验证值。无效路径或值会返回 HTTP `400`。

偏好设置是持久保存的用户或项目用户设置，而不是存储在 `game.project` 中的项目配置。如果自动化需要临时更改偏好设置，请保存先前的值，并在完成后恢复。

## 项目定义的路由

编辑器脚本可以使用 [`get_http_server_routes()`](/manuals/editor-scripts/#http-server) 定义额外路由。可选的 OpenAPI 操作表会通过与内置操作相同的 `/openapi.json` 文档公开路由。

项目定义的路由可以提供内容生成、验证、报告、本地化检查、资源分析、项目专用测试，或为 IDE 和外部控制器提供更小的接口。

良好的路由应执行一项名称明确的操作、验证输入、返回结构化结果、尽可能保持幂等，并限制高成本工作。

项目定义的路由不会自动受到 `/eval` 令牌保护。当路由执行敏感操作时，请添加项目专用的身份验证和安全检查。

## 生命周期钩子 {#lifecycle-hooks}

钩子函数可以在构建前后、创建包前后以及游戏进程启动或终止时运行。项目根目录中可以包含一个 `hooks.editor_script` 文件。只有根目录的钩子文件会接收这些事件，让项目可以在一个位置定义事件顺序。

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

`on_build_started()` 引发的错误会停止编辑器构建。生命周期钩子仅在编辑器中运行；请将共享的验证和生成逻辑放在也可以从 CI 调用的独立脚本中。

## 安全性和兼容性

将整个编辑器服务器视为受信任的本地接口：

* 不要公开端口访问。
* 保护 `.internal/editor.token`；它授权当前会话使用 `/eval`。
* 不要向外部提供不受限制的 `/eval` 访问权限。
* 将令牌保留在本地集成层中，而不是放入提示、报告或日志。
* 请记住，项目定义的路由不会继承 `/eval` 身份验证。
* 使用最新的 `/openapi.json`。
* 对异步自动化命令和编辑器启动使用有界等待。

## 引擎服务器

编辑器服务器属于编辑器进程。运行中的游戏会使用不同的端口，并具有不同职责，详见[引擎服务和运行时 HTTP API 手册](/manuals/engine-service)。
