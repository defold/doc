---
title: HTTP를 사용한 Defold 에디터 자동화
brief: 이 매뉴얼에서는 외부 도구에서 열린 Defold 에디터 프로젝트의 로컬 HTTP API를 찾고 사용하는 방법을 설명합니다.
---

# Defold 에디터 자동화 {#automating-the-defold-editor}

Defold 에디터는 자동화 동작을 위한 특수 서버를 엽니다. HTTP API는 열린 프로젝트를 제어합니다. 에디터 명령, 빌드, 프로젝트 리소스, 미리보기, 환경 설정, 콘솔 출력, 문서 검색 또는 에디터 스크립트 연동에 사용하세요. 실행 중인 게임을 검사하거나 제어하려면 [엔진 서비스 또는 런타임 자동화 API](/manuals/engine-service)를 사용하세요.

::: important
에디터 HTTP API는 실험적 기능이며 Defold 버전에 따라 변경될 수 있습니다. 실행 중인 에디터가 생성한 `/openapi.json` 문서는 사용 가능한 동작과 스키마의 기준 정보입니다.
:::

## 외부 도구에서 에디터 시작하기 {#starting-the-editor-from-an-external-tool}

외부 도구에는 에디터 실행 파일과 프로젝트 `game.project` 파일의 절대 경로가 필요합니다.

설치된 Defold 버전은 [에디터 매뉴얼](/manuals/editor/#editor-installation-metadata)에 설명된 대로 `installations.json`을 통해 찾을 수 있습니다. 이 파일의 `launcherPath` 필드에는 시작할 실행 파일이 들어 있습니다. 해당 프로젝트를 바로 열려면 `game.project` 경로를 첫 번째 위치 인자로 전달하세요.

선택적 `--port` 또는 `-p` 인자는 에디터 서버 포트를 선택합니다. 여러 프로젝트가 열려 있을 수 있다면 이 인자를 생략하여 Defold에서 사용 가능한 포트를 선택하도록 하는 편이 일반적으로 좋습니다.

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

에디터는 그래픽 데스크톱 어플리케이션입니다. 디스플레이에 액세스할 수 있는 대화형 사용자 세션에서 시작하세요. headless CI처럼 그래픽 세션을 사용할 수 없거나 컴파일 전용 자동화와 standalone 번들 생성이 필요한 경우 [Bob](/manuals/bob)을 사용하세요.

에디터를 시작한 후 프로젝트가 열리고 `.internal/editor.port`가 생성될 때까지 기다리세요. 그런 다음 유효한 문서를 반환할 때까지 `/openapi.json`을 폴링하세요. 프로세스를 생성했다고 해서 프로젝트가 준비된 것은 아닙니다.

## 에디터 서버 찾기 {#locating-the-editor-server}

에디터는 프로젝트가 열려 있는 동안 로컬 HTTP 서버를 시작합니다. 기본 브라우저에서 홈 페이지를 열려면 <kbd>Help ▸ Open Editor Server</kbd>를 선택하세요.

![로컬 에디터 서버 홈 페이지](images/automation/editor_server.png)

선택된 포트는 프로젝트 내부의 다음 파일에 기록됩니다.

```text
.internal/editor.port
```

이 매뉴얼의 이후 예제와 명령에서는 다음 셸 변수를 사용합니다.

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

포트 파일은 현재 에디터 세션에 속합니다. 에디터를 다시 시작한 후에는 이 파일을 다시 읽으세요.

::: important
에디터 서버는 신뢰할 수 있는 로컬 제어 인터페이스입니다. 공개 주소, 포트 포워딩 또는 신뢰할 수 없는 터널을 통해 노출하지 마세요.
:::

## OpenAPI를 통한 동작 찾기 {#discovering-operations-through-openapi}

외부 도구에 필요한 Defold 관련 부트스트랩 정보는 에디터 포트와 OpenAPI 문서뿐입니다.

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

반환된 OpenAPI 3.0.3 문서는 경로, 메서드, 파라미터, 명령 이름, 요청 포멧, 응답, 상태 코드 및 인증 요구 사항을 포함하여 실행 중인 에디터 버전이 지원하는 동작을 설명합니다.

문서화된 경로를 나열합니다.

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

사용 가능한 에디터 명령을 나열합니다.

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

버전을 인식하는 연동 기능에서는 필요한 각 동작을 확인하고 반환된 스키마에 따라 요청을 구성해야 합니다. 엔드포인트나 명령 이름의 완전한 복사본이라고 가정한 목록은 오래될 수 있으므로 유지하지 않는 것이 좋습니다.

에디터 스크립트에서 OpenAPI 동작 설명을 제공하면 프로젝트에서 정의한 경로도 `/openapi.json`에 나타납니다.

## 에디터 명령 실행하기 {#executing-editor-commands}

에디터 명령은 다음을 통해 호출합니다.

```text
POST /command/{command}
```

예를 들어 현재 `build` 명령은 프로젝트를 컴파일하고 실행합니다.

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

빌드에 성공하면 구조화된 결과를 반환합니다.

```json
{
  "success": true,
  "issues": []
}
```

빌드에 실패하면 다음과 같은 이슈와 함께 HTTP 상태 `422`를 반환합니다.

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

사용 가능한 필드는 오류에 따라 다릅니다. 리소스 경로와 소스 범위가 있으면 사용하되 메세지만 포함된 이슈도 처리하세요.

실행 중인 에디터에 나열되어 있을 때 일반적으로 유용한 명령은 다음과 같습니다.

`build`
: 프로젝트를 컴파일하고 실행합니다.

`clean-build`
: 빌드 캐쉬를 지운 다음 컴파일하고 실행합니다. 일반 빌드가 일관되지 않게 동작하거나 변경 사항을 놓치는 것으로 보일 때만 사용하세요.

`build-html5`
: HTML5용 프로젝트를 빌드하고 에디터 서버를 통해 출력에 액세스할 수 있게 합니다.

`fetch-libraries`
: 프로젝트 종속성을 다운로드하고 다시 로드합니다.

`hot-reload`
: 수정된 리소스를 실행 중인 게임에 다시 로드합니다.

`reload-extensions`
: 에디터 스크립트를 다시 로드합니다.

`debugger-start`, `debugger-stop` 및 디버거 단계 명령
: 디버그 세션과 실행 중인 프로젝트를 제어합니다.

정확한 이름과 사용 가능 여부는 에디터 버전과 현재 에디터 상태에 따라 달라집니다. `/openapi.json`에서 확인하세요.

프로젝트 리소스에서 동작하는 명령은 실행 전에 외부 파일 변경 사항을 동기화합니다.

### 명령 응답과 비동기 작업 {#command-responses-and-asynchronous-work}

명령 동작은 현재 OpenAPI 스키마에 응답 코드를 문서화합니다.

| 상태 | 의미 |
| --- | --- |
| `200` | 명령이 완료되고 결과를 반환함 |
| `202` | 명령이 수락되었고 비동기적으로 계속됨 |
| `403` | 현재 에디터 상태에서 명령이 활성화되지 않음 |
| `404` | 명령을 사용할 수 없음 |
| `422` | 빌드 또는 검증 실패 |
| `500` | 내부 에디터 오류 발생 |

HTTP `202` 응답은 요청한 결과가 존재한다는 증거가 아닙니다. 관련 출력, 리소스, 콘솔 마커 또는 제공되는 URL을 기다리고 타임아웃을 적용하세요.

### HTML5 빌드하기 {#building-html5}

현재 OpenAPI 문서에 `build-html5`가 나열되어 있으면 명령 동작을 통해 호출하세요.

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

명령은 비동기적으로 실행되며 일반적으로 HTTP `202`를 반환합니다. 빌드가 완료되면 에디터는 다음 주소에서 빌드를 제공합니다.

```text
http://127.0.0.1:<editor-port>/html5/
```

브라우저 테스트를 시작하기 전에 URL을 사용할 수 있을 때까지 기다리세요. 자세한 내용은 [HTML5 브라우저 테스트](/manuals/automated-testing/#browser-tests-for-html5)를 참고하세요.

## API 문서 검색하기 {#searching-api-documentation}

`/openapi.json`에 `/ref` 동작이 있으면 실행 중인 에디터 버전에 포함된 API 문서를 검색합니다. 해당 버전에 맞는 이름과 시그니쳐를 제공합니다.

예를 들어 함수를 검색하려면 다음을 사용합니다.

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

환경과 언어로 필터링합니다.

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

검색 파라미터는 다음과 같습니다.

`environment`
: `editor`, `runtime` 또는 쉼표로 구분한 값입니다.

`language`
: `Lua`, `C`, `C++` 또는 쉼표로 구분한 값입니다.

`q`
: 대소문자를 구분하지 않는 표현식입니다. 공백은 AND, `|`는 OR을 나타냅니다.

요약된 문서 리소스도 있습니다. [LLM 문서 인덱스](https://defold.com/llms.txt)는 공식 매뉴얼, API 네임스페이스 및 예제로 연결되며 [전체 LLM 문서](https://defold.com/llms-full.txt)는 오프라인 검색과 로컬 인덱싱을 지원하는 전체 문서를 나열합니다.

AI 에이전트는 토큰을 절약하고 특정 작업에 적합하게 준비된 깔끔한 컨텍스트를 만들기 위해 API나 메세지 하나만 필요할 때 전체 레퍼런스를 가져오지 말고 지정된 검색을 우선 사용해야 합니다.

## 콘솔 출력 읽기 {#reading-console-output}

에디터 콘솔을 JSON으로 읽습니다.

```sh
curl -sS "$BASE_URL/console" | jq
```

응답의 `lines`에는 콘솔 텍스트가, `regions`에는 오류, 평가 결과 및 리소스 레퍼런스를 포함한 의미론적 영역이 들어 있습니다.

콘솔 출력을 계속 확인하려면 다음을 사용합니다.

```sh
curl -N "$BASE_URL/console/stream"
```

스트림은 기존 콘솔 줄을 포함하며 이후 새 출력을 기다리면서 열린 상태로 유지됩니다. 완료 마커나 오류를 받거나, 프로세스 종료를 감지하거나, 타임아웃 또는 줄 제한에 도달하면 스트림을 닫으세요.

테스트 결과 프레이밍과 실패 분류에 대해서는 [자동화 테스트 및 검증](/manuals/automated-testing/#structured-test-results)을 참고하세요.

## 씬 미리보기 렌더링하기 {#rendering-scene-previews}

Defold 에디터(1.13.1 이상)는 `/preview/{path}` 명령을 통해 지원되는 씬 리소스의 "screenshot"을 PNG로 렌더링할 수 있습니다.

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

이 명령은 열린 Basic 3D 템플릿 프로젝트의 main 컬렉션을 기본 초기 뷰에서 렌더링합니다.

![에디터에서 렌더링한 main 컬렉션 미리보기](images/automation/main-preview.png)

렌더링을 사용하여 시각적 씬 에디터를 활용하는 리소스의 미리보기를 가져올 수 있습니다. 예를 들어 모델 컴포넌트를 같은 방식으로 렌더링하면 외형이나 쉐이더 정확성 등을 검증할 수 있습니다.

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![에디터에서 렌더링한 cube 모델 미리보기](images/automation/cube-preview.png)

`/preview/` 뒤의 경로에는 선행 슬래시가 포함되지 않습니다. 선택적 크기의 기본값은 프로젝트 디스플레이 크기이며 `1`에서 `4096` 사이여야 합니다.

| 상태 | 의미 |
| --- | --- |
| `200` | 미리보기가 렌더링됨 |
| `400` | 크기가 유효하지 않음 |
| `404` | 리소스를 찾을 수 없음 |
| `422` | 리소스가 로드되지 않았거나 씬 미리보기를 지원하지 않음 |

미리보기는 레벨 레이아웃, GUI 레이아웃, 쉐이더와 조명 설정, 시각적 회귀를 확인하거나 문서 썸네일을 만드는 등 프로젝트의 시각적 분석에 매우 유용할 수 있습니다.

::: important
에디터 미리보기는 실행 중인 게임의 스크린샷이 아닙니다. 동적으로 생성된 오브젝트, 런타임 후처리 또는 플랫폼별 렌더링을 검증하지 않습니다. 이러한 요소가 필요하면 [런타임 스크린샷](/manuals/automated-testing/#editor-previews-and-runtime-screenshots)을 사용하세요.
:::

## 에디터 Lua 실행하기 {#executing-editor-lua}

인증된 `POST /eval` 동작은 에디터 익스텐션 환경에서 Lua를 실행합니다. 세션별 bearer 토큰은 다음 위치에 저장됩니다.

```text
.internal/editor.token
```

토큰을 읽고 코드를 실행합니다.

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

출력된 내용과 반환값은 텍스트로 반환됩니다. 일반적인 응답은 다음과 같습니다.

| 상태 | 의미 |
| --- | --- |
| `200` | 코드가 실행됨 |
| `401` | bearer 토큰이 없거나 유효하지 않음 |
| `422` | Lua 코드를 파싱하거나 실행할 수 없음 |
| `503` | 에디터 익스텐션 환경이 준비되지 않음 |

클라이언트는 `503` 이후 다시 시도할 수 있지만 시도 횟수를 제한해야 합니다. `422`를 반환한 요청을 반복하기 전에 코드를 수정하세요.

평가된 코드는 [에디터 API](https://defold.com/ref/editor-lua/)와 에디터 스크립트 환경을 사용할 수 있습니다. 실행 중인 게임을 조작하는 `go.*` 같은 게임 런타임 API는 사용할 수 없습니다. 게임플레이에는 런타임 테스트, 디버거, 브라우저 테스트 또는 [런타임 자동화 API](/manuals/engine-service/#automation-bridge-extension)를 사용하세요.

### 리소스와 파일 수정하기 {#modifying-resources-and-files}

많은 Defold 소스 리소스는 텍스트 포멧을 사용하며 어떤 텍스트 편집 도구로도 편집할 수 있습니다. Defold 프로젝트의 구조화된 리소스를 수정할 때는 에디터 트랜잭션을 우선 사용하세요.

| 변경 | 권장 방법 |
| --- | --- |
| Lua, 쉐이더, JSON 또는 그 밖의 알려진 텍스트 포멧 | 직접 파일 수정 |
| 열린 에디터 탭의 저장하지 않은 텍스트 | `editor.get()` 및 `editor.transact()` |
| 컬렉션, 게임 오브젝트, GUI, 아틀라스 또는 그 밖의 구조화된 리소스 | 에디터 트랜잭션 |
| 반복적으로 생성되는 컨텐츠 | standalone 생성 도구 |
| 반복 가능한 프로젝트 동작 | 에디터 명령 또는 커스텀 HTTP 엔드포인트 |
| CI 전용 변환 | Bob 전에 실행되는 standalone 스크립트 |

리소스를 변경하기 전에 검사합니다.

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

트랜잭션을 수행하기 전에 `editor.can_get()`, `editor.can_set()` 및 기타 `editor.can_*()` 함수를 확인하세요.

에디터 Lua에서 `editor.execute()`를 사용하여 포멧터, 검증 도구 또는 생성 도구를 실행합니다.

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

명령이 프로젝트 리소스를 수정하지 않으면 불필요한 다시 로드를 방지하기 위해 `reload_resources = false`를 설정하세요.

::: important
`.internal/`의 파일이나 `build/`에서 생성된 컨텐츠를 수정하지 마세요.
:::

## 환경 설정 {#preferences}

에디터 환경 설정은 OpenAPI에 문서화된 경로(현재 `/prefs/{path}`)를 통해 읽고 쓸 수 있습니다.

예를 들어 구성된 코드 폰트 크기를 읽을 수 있습니다.

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

또는 다음과 같이 16으로 설정할 수 있습니다.

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

에디터는 환경 설정 스키마에 따라 값을 검증합니다. 경로나 값이 유효하지 않으면 HTTP `400`을 반환합니다.

환경 설정은 지속되는 사용자 또는 프로젝트 사용자 설정이며 `game.project`에 저장되는 프로젝트 구성이 아닙니다. 자동화에서 환경 설정을 일시적으로 변경해야 한다면 이전 값을 저장했다가 나중에 복원하세요.

## 프로젝트에서 정의한 경로 {#project-defined-routes}

에디터 스크립트는 [`get_http_server_routes()`](/manuals/editor-scripts/#http-server)를 사용하여 추가 경로를 정의할 수 있습니다. 선택적 OpenAPI 동작 테이블은 내장 동작과 동일한 `/openapi.json` 문서를 통해 경로를 노출합니다.

프로젝트에서 정의한 경로는 컨텐츠 생성, 검증, 보고서, 현지화 검사, 리소스 분석, 프로젝트별 테스트 또는 IDE나 외부 컨트롤러를 위한 더 작은 인터페이스를 제공할 수 있습니다.

좋은 경로는 명확한 이름을 가진 동작 하나를 수행하고, 입력을 검증하고, 구조화된 결과를 반환하고, 가능한 경우 멱등성을 갖추고, 비용이 많이 드는 작업을 제한해야 합니다.

프로젝트에서 정의한 경로는 `/eval` 토큰으로 자동 보호되지 않습니다. 경로에서 민감한 동작을 수행할 때는 프로젝트별 인증과 안전 검사를 추가하세요.

## 라이프사이클 훅 {#lifecycle-hooks}

훅은 빌드 전후, 번들 생성 전후 및 게임 프로세스 시작이나 종료 시 실행할 수 있는 함수입니다. 프로젝트 루트에는 `hooks.editor_script` 파일을 하나 포함할 수 있습니다. 루트 훅 파일만 이러한 이벤트를 수신하므로 프로젝트에서 이벤트 순서를 정의할 위치가 하나로 정해집니다.

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

`on_build_started()`에서 오류가 발생하면 에디터 빌드가 중지됩니다. 라이프사이클 훅은 에디터에서만 실행됩니다. 공유 검증과 생성 로직은 CI에서도 호출할 수 있는 standalone 스크립트에 넣으세요.

## 보안과 호환성 {#security-and-compatibility}

에디터 서버 전체를 신뢰할 수 있는 로컬 인터페이스로 취급하세요.

* 포트 액세스를 공개적으로 노출하지 마세요.
* `.internal/editor.token`을 보호하세요. 이 토큰은 현재 세션의 `/eval` 사용을 승인합니다.
* 외부에 제한 없는 `/eval` 액세스 권한을 부여하지 마세요.
* 토큰을 프롬프트, 보고서 또는 로그가 아닌 로컬 연동 계층에 보관하세요.
* 프로젝트에서 정의한 경로는 `/eval` 인증을 상속하지 않는다는 점에 유의하세요.
* 최신 `/openapi.json`을 사용하세요.
* 비동기 자동 명령과 에디터 시작에는 제한된 대기 시간을 사용하세요.

## 엔진 서버 {#engine-server}

에디터 서버는 에디터 프로세스에 속합니다. 실행 중인 게임은 다른 포트를 사용하고 역할도 다릅니다. 자세한 내용은 [엔진 서비스와 런타임 HTTP API 매뉴얼](/manuals/engine-service)을 참고하세요.
