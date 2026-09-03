---
title: 引擎服务和运行时 HTTP API
brief: 本手册介绍运行中的 Defold 调试引擎所提供的开发 HTTP 服务，以及运行时扩展或外部工具如何使用该服务。
---

# 引擎服务和运行时 HTTP API

在调试模式下运行项目时，会为包含游戏的特定引擎运行时实例创建一个进程，并提供一项特殊的引擎服务。该服务可用于开发和分析基础设施、运行时逻辑和消息、引擎状态及扩展。

引擎服务是由运行中的调试引擎（`dmengine`）所拥有的开发 HTTP 服务。

它与属于 Defold 编辑器、用于控制打开项目的[编辑器服务器](/manuals/editor-http-api)相互独立。

这两项服务使用不同的端口。连接到编辑器端口的工具无法在那里调用运行时扩展路由；反之，连接到引擎服务的工具也无法调用编辑器操作。

引擎服务是调试、开发和分析基础设施的一部分。发布版引擎实例不会创建该服务。

## 可用性和端口发现

编辑器启动调试引擎时，会请求一个动态分配的服务端口。引擎会在 `Console`（以及从 CLI 运行时的日志）中报告所选端口：

![Defold 调试构建中的引擎服务端口信息](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

从编辑器启动游戏时，该行会出现在编辑器控制台中。简单的本地控制器可以解析这一行，但可复用的集成应让编辑器或其封装程序跟踪引擎实例和已注册端口，从而避免将旧端口与新启动或复用的进程混淆。

引擎还会在支持的平台上通过服务发现公布开发目标。该机制主要由 Defold 工具使用，不应改用永久硬编码的端口来代替。

服务器可通过给定端口在 localhost（`127.0.0.1`）上访问：

![访问引擎服务器](images/automation/engine-server.png)

## 内置端点

当前的调试引擎会注册一小组核心路由。

| 端点 | 用途 |
| --- | --- |
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

## 扩展定义的运行时路由

在调试构建中，原生扩展 SDK 可以提供对引擎 Web 服务器的访问。扩展可以在该服务器上注册路由前缀，并公开依赖运行时数据的操作。

这对开发工具很有帮助，因为扩展可以共享现有引擎服务，而不必再打开一个 HTTP 服务器。

扩展定义的运行时自动化 API 应：

* 使用独立且带版本号的路由前缀；
* 公开所支持的功能；
* 返回结构化错误；
* 明确处理不可用的平台或引擎功能；
* 将操作限制在开发和测试范围内；
* 说明发布构建中是否会省略该 API。

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

### 编辑器客户端和运行时客户端

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

## 限制和安全性

引擎服务和扩展定义的路由都是开发工具，应当以此为前提进行处理。

::: important
引擎服务目前不会发布 OpenAPI 文档。集成应仅使用文档中明确说明的行为，或扩展提供的带版本号 API。
:::

运行时脚本、物理、输入、动态创建的对象和特定于平台的渲染都需要运行中的引擎，并应通过[自动化运行时测试](/manuals/automated-testing)进行验证。

* 不要通过路由器、公共接口或不受信任的隧道发布该服务。
* 不要假定引擎服务路由需要身份验证。
* 运行时路由可能因扩展版本、平台、图形后端和引擎功能而异。
* 对扩展定义的最新 API 使用版本或功能协商。
