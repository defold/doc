---
title: Defold 视频录制
brief: 本手册介绍如何使用 Lua 或引擎 HTTP 服务将游戏窗口录制为 MP4。
---

# 视频录制 {#video-recording}

Defold 可以通过 [`recorder` Lua 模块](/ref/recorder/)或[引擎 HTTP 服务](/manuals/engine-service/#recording-endpoints)，将游戏窗口录制为 MP4 文件中的 H.264 视频。两个接口共用一个录制器，因此同一时间只能有一个录制处于启动、运行或完成写入状态。

## 可用范围 {#availability}

桌面**调试**引擎包含录制功能。发布、无头、移动和 Web 构建不包含此功能。在 [App Manifest](/manuals/app-manifest/#exclude-record) 中启用 **Exclude Record** 也会移除 Lua 模块和 HTTP 路由。

| 平台 | 视频要求 | 应用音频 |
| --- | --- | --- |
| macOS | macOS 15 或更高版本，使用 ScreenCaptureKit | 支持 |
| Windows | Windows 10 版本 1903 或更高版本，使用 Windows Graphics Capture 和 Media Foundation | Windows 构建 20348 或更高版本支持 |
| Linux | OpenGL、OpenGL ES 或 Vulkan，使用帧缓冲区捕获 | 不支持 |

视频和音频支持分别检查。HTTP 客户端可以检查 `/recording/capabilities`；Lua 调用者在请求的捕获不受支持时会收到错误。即使启动请求已被接受，操作系统权限和捕获设备故障也可能导致之后的异步错误。

录制器以物理像素表示的原生大小捕获游戏窗口内容。为了生成偶数视频尺寸，可能裁掉一行或一列。调整窗口大小或改变像素密度会停止录制并完成文件写入。捕获帧率为每秒 1–60 帧，默认为 30。

## 从 Lua 录制 {#recording-from-lua}

使用 [`recorder.start()`](/ref/recorder/#recorder.start)，传入可写输出路径和回调。父目录必须存在；[`sys.get_save_file()`](/ref/sys/#sys.get_save_file) 可提供适合的应用保存路径。现有输出文件可能被覆盖。Lua 录制归调用者所有，引擎退出后仍保留在磁盘上。

与 Lua 文件 I/O 一样，路径在 Windows 上使用 Windows ANSI 代码页，在其他平台使用 UTF-8。回调中的 `result.path` 保留传给 `recorder.start()` 的路径。

以下 `.script` 示例在捕获开始后录制五秒：

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

[`recorder.stop()`](/ref/recorder/#recorder.stop) 和 `recorder.start()` 在请求被接受时返回 `true`，拒绝时返回 `nil, error`。接受请求不代表捕获或文件写入已完成。无效选项会引发 Lua 错误。

回调在引擎更新期间运行：

| 事件 | 含义 |
| --- | --- |
| `recorder.EVENT_STARTED` | 捕获已开始，可以停止。 |
| `recorder.EVENT_STOPPED` | MP4 已完成写入，可以读取。调整窗口大小导致自动停止后也会触发。 |
| `recorder.EVENT_ERROR` | 捕获失败；请检查 `result.error`。启动失败时，可能在没有 `EVENT_STARTED` 的情况下触发此事件。 |

结果还包含 `path`、`width`、`height`、`fps` 和 `audio`。仅在收到 `EVENT_STOPPED` 后读取或上传输出。请保持发起录制的脚本存活以接收回调：删除脚本会丢弃回调，但不会停止捕获。引擎关闭时会完成捕获，但不会调用 Lua 回调。

**Lua 默认禁用音频**。在支持的平台上，设置 `audio = true` 可请求录制应用音频。请求不支持的音频会返回错误。

### 与 HTTP 客户端共用录制器 {#sharing-the-recorder-with-http-clients}

`recorder.stop()` 针对当前共享录制，包括通过 HTTP 启动的录制。当有操作等待处理或没有活动录制时，它返回错误。如果 HTTP 客户端停止 Lua 录制，原来的 Lua 回调仍会收到完成事件。通过 HTTP 启动不会创建 Lua 回调；请使用 HTTP 状态观察完成情况。

HTTP 状态可以描述 Lua 录制，但其 `file` 字段为 `null`：服务只为通过 HTTP 启动的录制准备下载。请在 `EVENT_STOPPED` 后从 `result.path` 读取 Lua 录制。

## 通过 HTTP 录制 {#recording-through-http}

录制路由使用游戏日志中打印的引擎服务端口。按照[引擎服务手册](/manuals/engine-service/#discovering-operations-through-openapi)所述，通过 `/openapi.json` 发现这些路由。无头或发布引擎不会提供它们。

以下命令使用 POSIX shell、`curl` 和 `jq`；下载校验步骤还使用 Python 3。请在同一个 shell 中运行，并将 `<port>` 替换为运行中引擎的端口。首先查询能力并保留服务标识：

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

只有 `supported` 为 `true` 时才继续；否则检查 `unsupported_reason` 和 `minimum_platform_version`。`audio` 字段报告音频支持。与 Lua 不同，**HTTP 录制在后端支持时默认启用音频**。下面的示例显式禁用音频。

### 启动并检查录制 {#start-and-inspect-the-recording}

启动时可以传入包含 `fps` 和/或 `audio` 的可选 JSON 对象。服务负责选择输出文件，不接受路径、宽度、高度或缩放比例。

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202 表示请求已被接受。重复执行以下状态命令，直到 `pending` 为 `false` 且 `active` 为 `true`。检查会拒绝其他操作的响应，并报告捕获或文件准备失败。如果自动停止已使录制完成，请在下载前继续执行[完成写入](#stop-and-wait-for-finalization)步骤。

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

让游戏运行所需的录制时长，然后请求停止。如果窗口大小改变且录制已完成，请跳过停止请求，继续执行下方的完成写入步骤。

### 停止并等待完成写入 {#stop-and-wait-for-finalization}

停止操作时，使用从启动响应中保留的 ID：

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 仅表示停止请求被接受。重复状态命令，直到 `pending` 为 `false`、`finalized` 为 `true`，且 `file.state` 为 `complete`。原生捕获完成后，服务还会准备文件大小和 SHA-256，因此只有 `state: "complete"` 和 `finalized: true` 并不意味着已可下载。如果 `state` 或 `file.state` 变为 `failed`，请停止等待；不要下载状态为 `pending` 或 `failed` 的文件。

自动客户端应以一定间隔轮询并设置超时，在每次响应中检查保留的操作 ID。等待捕获和完成写入期间，请让引擎继续更新。

### 下载并释放文件 {#download-and-release-the-file}

使用状态响应中已完成文件的相对 URL。以下检查还确保响应仍属于您的操作：

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

将完成后的状态凭据 `capture.json` 与 MP4 一起保留。`/recording/status` 描述当前操作，因此之后的录制会替换状态响应，即使此前的 HTTP 文件仍然可用。

在使用下载文件或删除服务副本前，请校验文件字节大小和 SHA-256：

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

不带 `Range` 请求头的 GET 会下载整个 MP4。如果客户端需要部分下载，服务也支持 `Range: bytes=0-1023` 等闭合字节范围。请使用同一份凭据校验拼接后的文件。

下载并校验文件后，可以释放服务保留的副本：

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP 录制文件会一直可用，直到被显式删除，或引擎关闭、重启。请在关闭引擎前下载它们。服务最多保留 128 个文件；删除已保存的完成文件，可为后续录制腾出空间。

### 一起保存操作标识 {#keeping-operation-identities-together}

每个 POST 和 DELETE 都要求 `X-Recording-Instance`。示例也会在状态和下载请求中发送它，以拒绝替换后的引擎返回的响应。请一起保存 `instance_id`、`operation_id` 和文件信息：服务标识在重新启动或引擎重启后会改变，新进程也可能复用操作编号。

缺少标识会返回 HTTP 400。过期标识、过期的停止操作或已删除文件会返回 HTTP 410。不要获取新的标识后，用它重试旧操作；应重新发现服务并开始新的录制。

### 处理 HTTP 失败 {#handling-http-failures}

被拒绝的请求返回包含 `error.code` 和 `error.message` 的 JSON。排查问题时，请为单独的 `curl` 请求添加 `-i` 并移除 `-f`，以查看 HTTP 状态和错误正文。

| HTTP 状态 | 检查事项 |
| --- | --- |
| 409 | 另一个录制正在活动或等待，当前录制尚不能停止，或文件仍在准备中。重试前读取状态。 |
| 500 | 录制启动、存储初始化或文件准备/读取失败。检查错误消息；捕获失败也会在状态中报告 `failure`。 |
| 501 | 不支持视频或请求的音频。检查能力；如果仅音频不可用，请使用 `audio: false`。 |
| 507 | 已达到服务保留文件数量上限。在开始另一个录制前，下载并删除已完成文件。 |
