---
title: Defold의 영상 녹화
brief: 이 매뉴얼은 Lua 또는 엔진 HTTP 서비스로 게임 창을 MP4로 녹화하는 방법을 설명합니다.
---

# 영상 녹화 {#video-recording}

Defold는 [`recorder` Lua 모듈](/ref/recorder/) 또는 [엔진 HTTP 서비스](/manuals/engine-service/#recording-endpoints)를 통해 게임 창을 MP4 파일의 H.264 영상으로 녹화할 수 있습니다. 두 인터페이스는 하나의 녹화기를 공유하므로 한 번에 하나의 녹화만 시작, 실행, 마무리할 수 있습니다.

## 사용 가능 환경 {#availability}

녹화는 데스크톱 **디버그** 엔진에 포함됩니다. 릴리스, 헤드리스, 모바일, 웹 빌드에는 포함되지 않습니다. [App Manifest](/manuals/app-manifest/#exclude-record)에서 **Exclude Record**를 활성화해도 Lua 모듈과 HTTP 경로가 제거됩니다.

| 플랫폼 | 영상 요구 사항 | 어플리케이션 오디오 |
| --- | --- | --- |
| macOS | macOS 15 이상, ScreenCaptureKit 사용 | 지원 |
| Windows | Windows 10 버전 1903 이상, Windows Graphics Capture 및 Media Foundation 사용 | Windows 빌드 20348 이상에서 지원 |
| Linux | OpenGL, OpenGL ES 또는 Vulkan, 프레임버퍼 캡처 사용 | 미지원 |

영상과 오디오 지원은 별도로 검사합니다. HTTP 클라이언트는 `/recording/capabilities`로 확인할 수 있으며, Lua 호출은 요청한 캡처가 지원되지 않으면 오류를 받습니다. 시작 요청이 수락된 후에도 운영체제 권한이나 캡처 기기 실패로 비동기 오류가 발생할 수 있습니다.

녹화기는 게임 창의 컨텐츠를 물리 픽셀 기준 원래 크기로 캡처합니다. 영상 크기를 짝수로 맞추기 위해 한 행이나 열을 잘라낼 수 있습니다. 창 크기나 픽셀 밀도를 바꾸면 녹화를 중지하고 마무리합니다. 캡처 속도는 초당 1–60프레임이며 기본값은 30입니다.

## Lua에서 녹화하기 {#recording-from-lua}

쓰기 가능한 출력 경로와 콜백으로 [`recorder.start()`](/ref/recorder/#recorder.start)를 사용합니다. 상위 디렉토리는 존재해야 합니다. [`sys.get_save_file()`](/ref/sys/#sys.get_save_file)은 적절한 어플리케이션 저장 경로를 제공합니다. 기존 출력 파일을 덮어쓸 수 있습니다. Lua 녹화 파일은 호출자 소유이며 엔진 종료 후에도 디스크에 남습니다.

경로는 Lua 파일 I/O와 마찬가지로 Windows에서는 Windows ANSI 코드 페이지를, 다른 플랫폼에서는 UTF-8을 사용합니다. 콜백의 `result.path`는 `recorder.start()`에 전달한 경로를 그대로 유지합니다.

다음 `.script` 예제는 캡처 시작 후 5초 동안 녹화합니다:

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

`recorder.start()`와 [`recorder.stop()`](/ref/recorder/#recorder.stop)은 수락되면 `true`, 거절되면 `nil, error`를 반환합니다. 수락되었다고 캡처나 파일 마무리가 끝난 것은 아닙니다. 잘못된 옵션은 Lua 오류를 발생시킵니다.

콜백은 엔진 업데이트 중에 실행됩니다:

| 이벤트 | 의미 |
| --- | --- |
| `recorder.EVENT_STARTED` | 캡처가 활성화되었습니다. 이제 중지할 수 있습니다. |
| `recorder.EVENT_STOPPED` | MP4 마무리가 끝났으며 읽을 준비가 되었습니다. 크기 변경으로 자동 중지된 후에도 발생합니다. |
| `recorder.EVENT_ERROR` | 캡처가 실패했습니다. `result.error`를 확인하세요. 시작 실패 시 `EVENT_STARTED` 없이 이 이벤트가 발생할 수 있습니다. |

결과에는 `path`, `width`, `height`, `fps`, `audio`도 들어 있습니다. 출력 파일은 `EVENT_STOPPED` 이후에만 읽거나 업로드하세요. 콜백을 받으려면 시작한 스크립트를 유지해야 합니다. 스크립트를 삭제하면 캡처는 계속되지만 콜백은 버려집니다. 엔진 종료는 Lua 콜백을 호출하지 않고 캡처를 마무리합니다.

오디오는 **Lua에서 기본적으로 비활성화**되어 있습니다. 지원 플랫폼에서 어플리케이션 오디오를 요청하려면 `audio = true`를 설정하세요. 지원하지 않는 오디오를 요청하면 오류를 반환합니다.

### HTTP 클라이언트와 녹화기 공유하기 {#sharing-the-recorder-with-http-clients}

`recorder.stop()`은 HTTP로 시작한 녹화를 포함하여 현재 공유 녹화를 대상으로 합니다. 작업이 대기 중이거나 활성 녹화가 없으면 오류를 반환합니다. HTTP 클라이언트가 Lua 녹화를 중지해도 원래 Lua 콜백은 완료 이벤트를 받습니다. HTTP로 시작해도 Lua 콜백이 생성되지는 않으므로 완료 여부는 HTTP 상태로 확인하세요.

HTTP 상태는 Lua 녹화도 설명할 수 있지만 `file` 필드는 `null`입니다. 서비스는 HTTP로 시작한 녹화에 대해서만 다운로드를 준비합니다. Lua 녹화는 `EVENT_STOPPED` 후 `result.path`에서 읽으세요.

## HTTP로 녹화하기 {#recording-through-http}

녹화 경로는 게임 로그에 출력된 엔진 서비스 포트를 사용합니다. [엔진 서비스 매뉴얼](/manuals/engine-service/#discovering-operations-through-openapi)에 설명된 대로 `/openapi.json`에서 찾으세요. 헤드리스 또는 릴리스 엔진은 이 경로를 제공하지 않습니다.

다음 명령은 POSIX 셸, `curl`, `jq`를 사용하며 다운로드 검증 단계에는 Python 3도 필요합니다. 같은 셸에서 실행하고 `<port>`를 실행 중인 엔진의 포트로 바꾸세요. 먼저 지원 기능을 조회하고 서비스 식별자를 보관합니다:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

`supported`가 `true`일 때만 진행하세요. 그렇지 않으면 `unsupported_reason`과 `minimum_platform_version`을 확인합니다. `audio` 필드는 오디오 지원을 보고합니다. Lua와 달리 **HTTP 녹화는 백엔드가 지원하면 기본적으로 오디오를 활성화합니다**. 아래 예제는 오디오를 명시적으로 비활성화합니다.

### 녹화 시작 및 검사 {#start-and-inspect-the-recording}

선택적으로 `fps` 및/또는 `audio`를 포함한 JSON 오브젝트로 시작합니다. 출력 파일은 서비스가 선택하며 경로, 너비, 높이, 스케일은 받지 않습니다.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202는 요청을 수락했다는 뜻입니다. `pending`이 `false`, `active`가 `true`가 될 때까지 다음 상태 명령을 다시 실행하세요. 검사는 다른 작업의 응답을 거부하고 캡처나 파일 준비 실패를 보고합니다. 자동 중지로 녹화 마무리가 이미 끝났다면 다운로드 전에 [마무리 단계](#stop-and-wait-for-finalization)를 계속 진행하세요.

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

원하는 녹화 시간 동안 게임을 실행한 다음 중지를 요청합니다. 창 크기가 바뀌어 녹화가 이미 끝났다면 중지 요청을 건너뛰고 아래의 마무리 단계로 진행합니다.

### 중지 및 마무리 대기 {#stop-and-wait-for-finalization}

시작 응답에서 보관한 ID의 작업을 중지합니다:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202는 중지 요청이 수락되었다는 뜻일 뿐입니다. `pending`이 `false`, `finalized`가 `true`, `file.state`가 `complete`가 될 때까지 상태 명령을 반복하세요. 서비스는 네이티브 캡처가 끝난 후 파일 크기와 SHA-256을 준비하므로 `state: "complete"`와 `finalized: true`만으로는 다운로드 준비가 끝났다고 볼 수 없습니다. `state`나 `file.state`가 `failed`가 되면 기다리기를 중단하세요. 상태가 `pending` 또는 `failed`인 파일은 다운로드하지 마세요.

자동 클라이언트는 지연과 시간 제한을 두고 조회하며 모든 응답에서 보관한 작업 ID를 확인해야 합니다. 캡처와 마무리를 기다리는 동안 엔진이 계속 업데이트되도록 하세요.

### 파일 다운로드 및 해제 {#download-and-release-the-file}

상태 응답에 있는 완료된 파일의 상대 URL을 사용합니다. 아래 검사는 응답이 여전히 자신의 작업에 속하는지도 확인합니다:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

완료된 상태 정보를 MP4와 함께 `capture.json`에 보관하세요. `/recording/status`는 현재 작업을 설명하므로, 이전 HTTP 파일이 계속 남아 있더라도 이후 녹화가 상태 응답을 대체합니다.

다운로드한 파일을 사용하거나 서비스의 복사본을 삭제하기 전에 바이트 크기와 SHA-256을 검증합니다:

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

`Range` 헤더 없는 GET은 전체 MP4를 다운로드합니다. 부분 다운로드가 필요한 클라이언트를 위해 `Range: bytes=0-1023` 같은 양끝이 지정된 바이트 범위도 지원합니다. 조합한 파일도 같은 상태 정보와 대조하여 검증하세요.

파일을 다운로드하고 검증한 후에는 서비스가 보관하는 복사본을 해제할 수 있습니다:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP 녹화 파일은 명시적으로 삭제하거나 엔진이 종료 또는 재부팅될 때까지 사용할 수 있습니다. 엔진을 닫기 전에 다운로드하세요. 서비스는 최대 128개 파일을 보관합니다. 추가 녹화를 위한 공간을 확보하려면 저장을 마친 완료 파일을 삭제하세요.

### 작업 식별자 함께 보관하기 {#keeping-operation-identities-together}

모든 POST와 DELETE에는 `X-Recording-Instance`가 필요합니다. 예제는 교체된 엔진의 응답을 거부하기 위해 상태 및 다운로드 요청에도 이 헤더를 보냅니다. `instance_id`, `operation_id`, 파일 정보를 함께 보관하세요. 다시 시작하거나 재부팅하면 서비스 식별자가 바뀌며 새 프로세스가 작업 번호를 재사용할 수 있습니다.

식별자가 없으면 HTTP 400을 반환합니다. 오래된 식별자, 오래된 중지 작업, 삭제된 파일은 HTTP 410을 반환합니다. 새 식별자를 가져와 이전 작업의 재시도에 재사용하지 마세요. 새 서비스를 찾아 새 녹화를 시작하세요.

### HTTP 실패 처리 {#handling-http-failures}

거절된 요청은 `error.code`와 `error.message`가 있는 JSON을 반환합니다. 문제를 해결하려면 개별 `curl` 요청에 `-i`를 추가하고 `-f`를 빼서 HTTP 상태와 오류 본문을 확인하세요.

| HTTP 상태 | 확인 사항 |
| --- | --- |
| 409 | 다른 녹화가 활성 또는 대기 중이거나, 현재 녹화를 아직 중지할 수 없거나, 파일을 준비 중입니다. 재시도 전에 상태를 읽으세요. |
| 500 | 녹화 시작, 저장 공간 초기화, 파일 준비/읽기에 실패했습니다. 오류 메세지를 확인하세요. 캡처 실패는 상태의 `failure`로도 보고됩니다. |
| 501 | 영상 또는 요청한 오디오를 지원하지 않습니다. 지원 기능을 확인하고, 오디오만 사용할 수 없다면 `audio: false`를 사용하세요. |
| 507 | 서비스의 보관 파일 한도에 도달했습니다. 새 녹화를 시작하기 전에 완료 파일을 다운로드하고 삭제하세요. |
