---
title: 自动化测试与验证
brief: 本手册介绍如何在本地、运行中的游戏、浏览器和持续集成环境中设计、运行并报告确定性的 Defold 测试。
---

# 自动化测试与验证

自动化测试使用明确且机器可读的证据来验证 Defold 代码和内容。请使用本手册设计可供本地脚本、CI（持续集成）运行器和编码智能体共同使用的测试。本手册涵盖模块测试、运行集合、浏览器测试、运行时自动化、视觉检查、无头构建，并提供实用的良好实践。

## 验证层级

良好的自动化测试层级遵循测试金字塔框架，将测试分为三个主要层次：单元测试、集成测试和端到端（E2E）测试。在 Defold 中，可以将测试划分到启动时加载的特定集合中。通常最好从能够检测问题的最小、最快检查开始，再按需添加运行时或平台测试。

| 层级 | 合适的证据 |
| --- | --- |
| 静态验证 | 解析器、格式化工具、资源验证器或生成文件比较的结果 |
| 模块测试 | 对引擎依赖最少的可复用 Lua 逻辑所产生的断言结果 |
| 运行集合 | 消息、组件、输入、物理、生命周期和引擎行为 |
| 运行时自动化 | 实时场景状态、注入的输入、应用程序状态和运行时截图 |
| HTML5 浏览器测试 | 画布输入、浏览器集成、视口行为和 Web 输出 |
| 平台测试 | 实际目标平台上的行为和渲染结果 |
| 构建和打包 | Bob 退出状态、构建报告、存档和包产物 |

编译成功只证明项目能够构建，并不能证明游戏行为正确。截图无法证明复杂的过渡、动画、交互或游戏流程，但现代多模态解决方案可以用它检查某一帧的外观，以及着色器和视觉布局是否正确。不过，对于自动化测试，只要条件可以直接表达，就应优先使用确定性断言。

## 可复用且可测试的 Lua 代码

将可复用逻辑放在对引擎依赖最少的 Lua 模块中。这样，无需构建完整游戏世界即可测试纯数据转换、规则、状态机和计算。

将面向引擎的代码与它所调用的逻辑分离。脚本可以把消息和组件状态转换成对模块的调用，而测试则使用受控输入直接调用模块。

更多详情请参阅[编写代码手册](/manuals/writing-code)。

## 在运行集合中进行测试 {#tests-in-a-running-collection}

当行为依赖于游戏对象、组件、消息、输入、物理或其他引擎系统时，请使用专用的测试集合。

每项测试都应：

1. 建立已知状态；
2. 执行一个行为；
3. 断言并评估预期结果；
4. 清理创建的资源；
5. 输出结构化结果描述。

测试应优先使用彼此隔离的测试集合。项目可以通过 `game.project` 中的临时项目设置选择测试启动集合：

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

不要在项目的常规配置中保留临时测试启动集合。在 CI 中，应优先使用传递给 Bob 的专用设置文件。CI 不应更改代码仓库的状态，只应在需要时进行临时更改。

对于复杂游戏，可以创建带有预定义情境和简单白盒场景的小型“开发房间”集合。它们可以让机制易于复现，并简化测试开发，而无需在无关的游戏状态和区域中导航。

### 测试框架

项目可以实现一个小型运行器，或使用[社区测试库](https://defold.com/assets/?tag=testing)。

例如，[DefTest](https://defold.com/assets/deftest/) 是基于 Telescope 的单元测试库。它支持测试套件、建立和清理函数、断言、名称过滤、针对部分 Defold API 的模拟，以及可选的 LuaCov 覆盖率。测试可以从专用的启动集合运行，也可以在使用 Bob 创建的无头包中运行。

## 结构化测试结果 {#structured-test-results}

框架的控制台或日志摘要对开发者很有帮助，但无人值守的自动控制器仍需要明确的完成结果。如有必要，可在框架回调或摘要周围添加小型适配器，以便控制器轻松处理测试结果。

一种简单的结果描述格式，是在控制台的每个物理行上使用唯一前缀，后接一个 JSON 对象：

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

收集器应独立处理每一行，查找 `TEST` 前缀，解析其后的 JSON，并忽略无关的引擎输出。

请包含唯一的运行标识符，以防旧进程或并发进程的输出被误判为当前运行完成。每个套件都应输出一个含义明确的最终事件（如 `Pass`、`Failure`、`Crash`、`Timeout` 等）。

### 收集控制台输出

从编辑器运行游戏时，编辑器既会提供当前控制台历史记录，也会提供连续输出流。应在收到匹配的测试套件完成事件、进程终止、发生错误，或达到配置的超时和行数限制后关闭该流。

请在[编辑器 HTTP API 手册](/manuals/editor-http-api/#reading-console-output)中了解更多信息。

### 持久化日志

Defold 还可以通过启用 `Write Log File`（位于 `game.project` 中）来持久保存游戏日志。请参阅[游戏和系统日志](/manuals/debugging-game-and-system-logs/)。文件日志适用于打包后的应用程序，以及编辑器控制台不可用时对目标设备的测试。

项目可以使用内置的 `print()` 和 `pprint()` 函数，或使用资产门户中的其他[日志记录库](https://defold.com/assets/?tag=logging)。

## 通过运行时 API 测试运行中的游戏

运行时自动化 API 可以检查和控制实时调试引擎。当测试必须查找运行时对象、注入输入、等待可见状态或捕获渲染结果时，可以使用该 API。

更多详情请参阅[引擎服务手册](/manuals/engine-service/#automation-bridge-extension)。

以下示例使用 [Automation Bridge](https://github.com/defold/extension-automation-bridge) Python 辅助工具的结构。项目必须包含兼容版本的调试扩展，公开具有给定自动化 ID 的元素，并发布 `screen` 应用程序状态：

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

应用程序定义的状态和自动化 ID 使用 Automation Bridge 可选的仅调试 Lua API，项目必须启用并发布这些内容。固定的休眠时间容易受机器速度和帧时序影响；对明确定义的状态进行有界轮询会更加可靠。

Automation Bridge 是一个扩展，而不是核心引擎的一部分。请查阅其 [Python API 参考](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python)，了解所安装版本的选择器、等待、状态、事件、截图和诊断功能。

## HTML5 的浏览器测试 {#browser-tests-for-html5}

编辑器可以通过当前的 `build-html5` 命令创建并提供 HTML5 构建，具体请参阅[编辑器 HTTP API 手册](/manuals/editor-http-api/#building-html5)。Bob 也可以在不使用编辑器的情况下创建 HTML5 包。

Playwright、Puppeteer、Selenium、WebdriverIO 或 Cypress 等外部浏览器自动化工具可以：

* 等待 Defold 画布和应用程序就绪；
* 发送键盘、鼠标和模拟触摸输入；
* 调整视口大小；
* 收集浏览器控制台输出和 JavaScript 错误；
* 截取屏幕并比较产物。

指向画布的输入会通过项目的常规输入绑定和 `on_input()` 回调进行处理。测试时应同时检查游戏响应和浏览器专用的集成点。

最可靠的方法是在自定义 `index.html` 中公开一个明确的 JavaScript 测试桥接。在 Defold 端，HTML5 构建可以使用 `html5.run()` 执行 JavaScript，从而与此类浏览器端桥接进行通信。对于从 JavaScript 传回 Defold 的命令，请使用专用的 JavaScript 到引擎桥接。

浏览器测试应有明确的范围限制。在最终报告中区分页面加载失败、画布缺失、JavaScript 错误、测试超时和游戏断言失败。

## 用于视觉检查的编辑器预览和运行时截图 {#editor-previews-and-runtime-screenshots}

可以在打开的编辑器默认场景视图中为资源文件创建“截图”，也可以在运行时游戏中创建截图。

| 方法 | 用途 |
| --- | --- |
| [编辑器预览](/manuals/editor-http-api/#rendering-scene-previews) | 已加载资源的布局，例如关卡或 GUI、图集构成、瓦片地图检查、静态场景构成、编辑器渲染和着色器正确性，或制作文档缩略图 |
| [运行时截图](/manuals/engine-service) | 受控情境中运行构建的渲染状态 |

例如，可以使用图像比较进行回归测试。检查失败时，请保存差异图像和比较指标。

多模态模型可以在视觉检查中评估难以用其他方式表达的语义条件，例如文本被截断、控件重叠、选择状态不明确或内容超出安全区域。建议将这种评估视为具有明确标准的附加信号，而不是确定性逻辑检查或图像比较的替代品。

## 无头测试和 CI

使用 Bob 构建器 CLI 工具执行独立于编辑器的 CI。

您可以使用它解析依赖项、构建游戏、存档或独立包，并生成 JSON 报告：

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

使用专用设置构建无头测试包：

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

使用适合平台的进程控制器运行生成的可执行文件。捕获其退出状态和日志，实施超时，并要求输出结构化的测试套件完成事件。

[Bob 手册](/manuals/bob)介绍平台、设置文件、包、缓存、原生扩展和构建报告。

## 失败报告和产物

良好的测试结果应保留足够的证据来复现和诊断故障：

* 测试名称、运行标识符和断言详情；
* 经过时间和分类结果；
* 完整的控制台或进程日志；
* Defold 版本、目标平台和相关配置；
* Bob 构建报告和进程退出状态；
* 可用时的运行时状态或场景快照；
* 截图、基线差异、录制内容或浏览器跟踪；
* 所有生成产物的路径或链接。

开发者、本地脚本、CI 服务或 [AI 编码智能体](/manuals/ai-agents)应能够使用同一种格式。这样，即使将诊断或修复工作委派出去，验证本身仍然具有确定性。
