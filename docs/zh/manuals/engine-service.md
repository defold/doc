---
title: 引擎服务和运行时 HTTP API
brief: 本手册介绍运行中的 Defold 调试引擎所提供的开发 HTTP 服务，以及运行时扩展或外部工具如何使用该服务。
---

# 引擎服务和运行时 HTTP API {#the-engine-service-and-runtime-http-apis}

在调试模式下运行项目时，会为包含游戏的特定引擎运行时实例创建一个进程，并提供一项特殊的引擎服务。该服务可用于开发和分析基础设施、运行时逻辑和消息、引擎状态及扩展。

引擎服务是由正在运行的调试或无头引擎（`dmengine` 或 `dmengine_headless`）提供的开发用 HTTP 服务。

它与属于 Defold 编辑器、用于控制打开项目的[编辑器服务器](/manuals/editor-http-api)相互独立。

这两项服务使用不同的端口。连接到编辑器端口的工具无法在那里调用运行时扩展路由；反之，连接到引擎服务的工具也无法调用编辑器操作。

引擎服务是调试、开发和分析基础设施的一部分。发布版引擎实例不会创建该服务。

## 可用性和端口发现 {#availability-and-port-discovery}

编辑器启动调试引擎时，会请求动态分配的服务端口。引擎会在 *Console* 中报告所选端口；从 CLI 运行时，也会在日志中报告：

![Defold 调试构建中的引擎服务端口信息](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

引擎还会记录包含其实际地址和所分配端口的完整 OpenAPI 发现 URL：

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

从编辑器启动游戏时，这些行会出现在编辑器控制台中。简单的本地控制程序可以解析这些内容，但可复用的集成应让编辑器或其包装程序跟踪引擎实例和已注册端口，避免将旧端口与新启动或复用的进程混淆。

引擎还会在支持的平台上通过服务发现公布开发目标。该机制主要由 Defold 工具使用，不应改用永久硬编码的端口来代替。

服务器可通过给定端口在 localhost（`127.0.0.1`）上访问：

![访问引擎服务器](images/automation/engine-server.png)

## 通过 OpenAPI 发现操作 {#discovering-operations-through-openapi}

`GET /openapi.json` 返回描述运行时 HTTP API 的 OpenAPI 3.0.3 文档。请使用日志中的引擎服务端口。对于本地引擎，将下方的 `<port>` 替换为该端口：

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

该文档描述当前已注册处理器提供的路径、方法、参数、请求体和响应，也包含提供 OpenAPI 元数据的原生扩展。添加或移除处理器时，其 `paths` 对象会随之变化。分析器和扩展路由取决于运行中的引擎平台、配置和已注册扩展，因此请从正在使用的实例获取文档。

没有注册 OpenAPI 元数据的处理器仍可调用，但不会出现在文档中。文档中列出的路由也可能报告某项能力不可用；使用依赖平台的操作前，请检查其响应说明和相关能力端点。

编辑器在编辑器端口上有自己的 [OpenAPI 文档](/manuals/editor-http-api/#discovering-operations-through-openapi)。运行时操作应使用引擎的文档。

## 内置端点 {#built-in-endpoints}

当前的调试引擎会注册一小组核心路由。

| 端点 | 用途 |
| --- | --- |
| `GET /openapi.json` | 发现当前已注册且提供 OpenAPI 元数据的运行时 HTTP 操作 |
| `GET /ping` | 检查引擎服务是否响应 |
| `GET /info` | 读取引擎版本、平台、构建标识符和日志服务信息 |
| `GET /state` | 读取 Defold 工具使用的开发连接状态 |
| `POST /post/<socket>/<message-type>` | 向指定的引擎套接字发送经 Protobuf 编码的 Defold 消息 |

例如：

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

`/post` 路由供热重载、重新启动、调整大小和进程控制等开发操作使用。其请求体是路由中所指定类型的二进制 Protobuf 消息；它不是 JSON 消息 API。Protobuf 消息序列化后不得超过 1024 字节，否则将返回 `400 Too large message`。

这些路由属于开发基础设施，引擎实现中还存在其他分析器和资源检查路由。

## 录制端点 {#recording-endpoints}

桌面调试引擎还通过以下路由提供原生 MP4 录制。发布、无头、移动和 Web 构建，以及在 [App Manifest](/manuals/app-manifest/#exclude-record) 中启用 **Exclude Record** 的构建均不包含这些路由。

| 端点 | 用途 |
| --- | --- |
| `GET /recording/capabilities` | 发现视频/音频支持、后端要求和录制服务的 `instance_id` |
| `GET /recording/status` | 读取当前操作、异步进度和已完成文件的信息 |
| `POST /recording/start` | 请求开始录制并接收其 `operation_id` |
| `POST /recording/stop` | 请求停止指定操作并完成文件写入 |
| `GET /recording/files/{id}` | 下载已完成写入的 MP4 |
| `DELETE /recording/files/{id}` | 删除服务保留的已完成文件 |

先通过 `/openapi.json` 发现这些路由，再检查 `/recording/capabilities` 了解当前平台的支持情况。修改录制状态的请求必须携带 `X-Recording-Instance` 请求头，停止时还必须提供已接受的 `operation_id`。启动和停止均为异步操作；请等文件完成写入后再下载。完整流程请参阅[录制手册](/manuals/recording/#recording-through-http)。

HTTP 服务与 Lua 共用录制器。在支持音频的平台上，HTTP 启动默认启用应用音频；Lua 启动默认仅录制视频。只有通过 HTTP 启动的录制才提供可下载的 `file` 凭据。下载前，请等待 `pending: false`、`finalized: true` 和 `file.state: "complete"`，然后[校验文件大小和 SHA-256](/manuals/recording/#download-and-release-the-file)。同时使用 Lua 和 HTTP 客户端时，请参阅[共用录制器](/manuals/recording/#sharing-the-recorder-with-http-clients)。

## Metal GPU 跟踪端点 {#metal-gpu-trace-endpoint}

在 macOS 上，调试引擎提供 `/profiler/gputrace` 来捕获 Metal GPU 跟踪。此路由仅在 macOS 的 `/openapi.json` 中出现。捕获要求使用原生 Metal 适配器，并在引擎的启动环境中设置 `METAL_CAPTURE_ENABLED=1`。如果无法捕获，请求会返回 HTTP 501，并包含 `error.code: "gputrace_unsupported"`。

| 端点 | 用途 |
| --- | --- |
| `POST /profiler/gputrace` | 安排捕获到可写的绝对 `.gputrace` 路径；`frames` 默认为 `1`，可取 `1`–`10000`。 |
| `GET /profiler/gputrace` | 读取当前或最近一次捕获的状态、路径和帧数。 |
| `DELETE /profiler/gputrace` | 取消等待中的捕获，或在当前渲染帧之后结束活动捕获；保留磁盘上的跟踪文件。 |

已接受的请求返回 HTTP 200，包含 `ok: true` 和 `data` 对象。捕获异步进行：轮询 `GET`，直到 `data.state` 为 `complete`、`canceled` 或 `failed`。原生启动失败会在 `data.error` 中报告。跟踪文件写入引擎所在主机。有关启动命令、支持检测、捕获示例以及在 Xcode 中打开结果，请参阅 [Metal GPU 跟踪捕获指南](/manuals/profiling/#metal-gpu-trace-capture)。

## 扩展定义的运行时路由 {#extension-defined-runtime-routes}

在调试构建中，原生扩展 SDK 可以提供对引擎 Web 服务器的访问。扩展可以在该服务器上注册路由前缀，并公开依赖运行时数据的操作。

这对开发工具很有帮助，因为扩展可以共享现有引擎服务，而不必再打开一个 HTTP 服务器。

扩展定义的运行时自动化 API 应：

* 使用独立且带版本号的路由前缀；
* 公开所支持的功能；
* 返回结构化错误；
* 明确处理不可用的平台或引擎功能；
* 将操作限制在开发和测试范围内；
* 说明发布构建中是否会省略该 API。

### 在 OpenAPI 中发布扩展操作 {#publishing-extension-operations-in-openapi}

在原生扩展的应用初始化回调中，使用 `dmEngine::GetWebServer(app_params)` 获取服务器，且仅在返回的句柄非空时注册处理器。回调设置请参阅[扩展生命周期](/manuals/extensions/#extension-lifecycle)。

四参数的 `dmWebServer::AddHandler()` 重载接受以 JSON 字符串表示的 OpenAPI 3.0.3 Paths Object。该对象的顶层键为路由路径。每条路径必须以注册的前缀开头，且不能已由其他处理器记录。请使用内联 schema，或引用最终文档中的路径。

例如，以下辅助函数注册一个回调及其状态端点说明：

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

传入实现 `GET /example/v1/status` 并返回文档规定的 `text/plain` 响应的回调。检查请求路径和方法、生成响应仍由回调负责。请检查注册结果：元数据无效或冲突时会返回 `dmWebServer::RESULT_ERROR_INVAL`。

服务器保留 JSON 指针，不复制字符串。在通过 `dmWebServer::RemoveHandler()` 移除处理器或销毁服务器前，必须保持其存储内容不变且有效。示例中的 `static const char` 数组满足此要求。移除处理器也会从后续 `/openapi.json` 响应中移除其路径。

仍然支持三参数的 `dmWebServer::AddHandler(server, prefix, &params)` 重载。它等同于将第四个参数设为 `0`：注册不含 OpenAPI 元数据的处理器，不将其包含在发现结果中。

## Automation Bridge 扩展 {#automation-bridge-extension}

Defold 官方的 [Automation Bridge](https://github.com/defold/extension-automation-bridge) 是一个基于引擎服务构建、仅用于调试的原生扩展。它会在以下路径下注册带版本号的运行时自动化 API：

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

其运行时 API 提供场景和节点检查、输入、屏幕信息、截图、录制、生命周期信息，以及可选的应用程序自定义同步等功能。其中一些操作包括：

| 操作 | 行为 |
| --- | --- |
| `GET  /automation-bridge/v1/health` | 健康状况报告、API 功能和兼容性 |
| `POST /automation-bridge/v1/input/click` | 执行运行时输入交互 |
| `GET  /automation-bridge/v1/screenshot` | 获取运行时截图 |

请使用扩展的[原生 API 文档](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge)和 [Python 辅助工具文档](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python)，并以项目中安装的版本为准。

Automation Bridge 不会在发布构建中公开其 HTTP API 或 Lua 模块。

### 编辑器客户端和运行时客户端 {#editor-and-runtime-clients}

Automation Bridge Python 辅助工具展示了双客户端架构。函数 `editor.open_project()` 返回编辑器项目客户端，而 `project.build_and_run()` 返回独立的引擎客户端。

| 客户端 | 用途 |
| --- | --- |
| Project | 编辑器 HTTP API、命令、调试器、控制台、偏好设置、参考资料、预览、构建和端口发现 |
| Game - engine service | 场景、输入、截图、运行时状态和同步 |

`project` 和 `game` 之间的划分明确体现了进程边界。编辑器操作仍在编辑器服务器上执行，而对实时游戏进行的观察和操作仍在引擎服务上执行。

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## 限制和安全性 {#limitations-and-security}

引擎服务和扩展定义的路由都是开发工具，应当以此为前提进行处理。

::: important
在 Defold 1.14.1 及更高版本中，请使用运行中引擎的 `/openapi.json` 文档进行发现。较早的引擎不提供此端点。对于没有注册 OpenAPI 元数据的处理器，请查阅扩展对应版本的 API 文档。
:::

运行时脚本、物理、输入、动态创建的对象和特定于平台的渲染都需要运行中的引擎，并应通过[自动化运行时测试](/manuals/automated-testing)进行验证。

* 不要通过路由器、公共接口或不受信任的隧道发布该服务。
* 不要假定引擎服务路由需要身份验证。
* 运行时路由可能因扩展版本、平台、图形后端和引擎功能而异。
* 对扩展定义的最新 API 使用版本或功能协商。
