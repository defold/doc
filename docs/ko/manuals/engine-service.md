---
title: 엔진 서비스와 런타임 HTTP API
brief: 이 매뉴얼에서는 실행 중인 Defold 디버그 엔진의 개발용 HTTP 서비스와 런타임 익스텐션 또는 외부 도구에서 이 서비스를 사용하는 방법을 설명합니다.
---

# 엔진 서비스와 런타임 HTTP API {#the-engine-service-and-runtime-http-apis}

Debug 모드로 프로젝트를 실행하면 게임이 포함된 특정 엔진 런타임 인스턴스를 위한 프로세스와 특수 엔진 서비스가 생성됩니다. 이 서비스는 개발 및 프로파일링 인프라, 런타임 로직과 메세지, 엔진 상태 및 익스텐션에 액세스하는 데 사용할 수 있습니다.

엔진 서비스는 실행 중인 디버그 또는 헤드리스 엔진(`dmengine` 또는 `dmengine_headless`)이 제공하는 개발용 HTTP 서비스입니다.

이 서비스는 Defold 에디터에 속하며 열린 프로젝트를 제어하는 [에디터 서버](/manuals/editor-http-api)와 별개입니다.

두 서비스는 서로 다른 포트를 사용합니다. 에디터 포트에 연결된 도구는 그 포트에서 런타임 익스텐션 경로를 호출할 수 없으며, 반대로 엔진 서비스에 연결된 도구는 에디터 동작을 호출할 수 없습니다.

엔진 서비스는 디버그, 개발 및 프로파일링 인프라의 일부입니다. 릴리스 엔진 인스턴스는 이 서비스를 생성하지 않습니다.

## 사용 가능 여부와 포트 찾기 {#availability-and-port-discovery}

에디터는 디버그 엔진을 시작할 때 동적으로 할당되는 서비스 포트를 요청합니다. 엔진은 선택된 포트를 *Console*에 표시하며, CLI에서 실행할 때는 로그에 기록합니다:

![Defold 디버그 빌드의 엔진 서비스 포트 정보](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

엔진은 실제 주소와 할당된 포트를 사용한 전체 OpenAPI 검색 URL도 기록합니다:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

에디터에서 게임을 실행하면 이 줄들이 에디터 콘솔에 나타납니다. 간단한 로컬 제어 프로그램은 이를 파싱할 수 있지만, 재사용할 통합 기능에서는 에디터나 래퍼가 엔진 인스턴스와 등록된 포트를 추적하도록 해야 합니다. 이렇게 하면 이전 포트를 새로 시작되거나 재사용된 프로세스와 혼동하지 않습니다.

엔진은 지원되는 플랫폼에서 서비스 검색을 통해 개발 타겟을 알리기도 합니다. 이 메커니즘은 주로 Defold 도구에서 사용하며 영구적으로 하드 코딩된 포트로 대체해서는 안 됩니다.

서버는 지정된 포트의 localhost(`127.0.0.1`)에서 액세스할 수 있습니다.

![엔진 서버 액세스](images/automation/engine-server.png)

## OpenAPI로 작업 검색하기 {#discovering-operations-through-openapi}

`GET /openapi.json`은 런타임 HTTP API를 설명하는 OpenAPI 3.0.3 문서를 반환합니다. 로그에 나온 엔진 서비스 포트를 사용하세요. 로컬 엔진에서는 아래의 `<port>`를 해당 포트로 바꿉니다:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

이 문서는 OpenAPI 메타데이터를 제공하는 네이티브 익스텐션을 포함하여 현재 등록된 핸들러의 경로, 메서드, 매개변수, 요청 본문, 응답을 설명합니다. 핸들러를 추가하거나 제거하면 `paths` 오브젝트가 바뀝니다. 프로파일러 및 익스텐션 경로는 실행 중인 엔진의 플랫폼, 설정, 등록된 익스텐션에 따라 달라지므로 사용하는 인스턴스에서 문서를 가져오세요.

OpenAPI 메타데이터 없이 등록된 핸들러도 호출할 수 있지만 문서에는 표시되지 않습니다. 문서에 있는 경로라도 해당 기능을 사용할 수 없다고 응답할 수 있습니다. 플랫폼에 의존하는 작업을 사용하기 전에 응답 설명과 기능 확인 엔드포인트를 검사하세요.

에디터는 에디터 포트에서 별도의 [OpenAPI 문서](/manuals/editor-http-api/#discovering-operations-through-openapi)를 제공합니다. 런타임 작업에는 엔진의 문서를 사용하세요.

## 내장 엔드포인트 {#built-in-endpoints}

현재 디버그 엔진은 소수의 핵심 경로를 등록합니다.

| 엔드포인트 | 용도 |
| --- | --- |
| `GET /openapi.json` | OpenAPI 메타데이터를 제공하는 현재 등록된 런타임 HTTP 작업 검색 |
| `GET /ping` | 엔진 서비스가 응답하는지 확인 |
| `GET /info` | 엔진 버전, 플랫폼, 빌드 식별자 및 로그 서비스 정보 읽기 |
| `GET /state` | Defold 도구에서 사용하는 개발 연결 상태 읽기 |
| `POST /post/<socket>/<message-type>` | Protobuf로 인코딩된 Defold 메세지를 이름이 지정된 엔진 소켓으로 게시 |

예를 들면 다음과 같습니다.

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

`/post` 경로는 핫 리로드, 재부팅, 크기 변경 및 프로세스 제어와 같은 개발 동작에서 사용됩니다. 본문은 경로에 이름이 지정된 유형의 바이너리 Protobuf 메세지이며 JSON 메세지 API가 아닙니다. 직렬화된 Protobuf 메세지는 1024바이트를 초과할 수 없으며, 초과하면 `400 Too large message`가 반환됩니다.

이러한 경로는 개발 인프라이며 엔진 구현에는 프로파일러 및 리소스 검사용 경로도 추가로 존재합니다.

## 녹화 엔드포인트 {#recording-endpoints}

데스크톱 디버그 엔진은 다음 경로로 네이티브 MP4 녹화도 제공합니다. 릴리스, 헤드리스, 모바일, 웹 빌드와 [App Manifest](/manuals/app-manifest/#exclude-record)의 **Exclude Record**가 활성화된 빌드에서는 이 경로를 포함하지 않습니다.

| 엔드포인트 | 용도 |
| --- | --- |
| `GET /recording/capabilities` | 영상/오디오 지원, 백엔드 요구 사항, 녹화 서비스의 `instance_id` 확인 |
| `GET /recording/status` | 현재 작업, 비동기 진행 상태, 완료된 파일 정보 읽기 |
| `POST /recording/start` | 녹화 요청 및 `operation_id` 수신 |
| `POST /recording/stop` | 지정한 작업의 중지 및 마무리 요청 |
| `GET /recording/files/{id}` | 완료된 MP4 다운로드 |
| `DELETE /recording/files/{id}` | 서비스가 보관하는 완료된 파일 삭제 |

`/openapi.json`에서 이 경로들을 찾은 다음 `/recording/capabilities`로 현재 플랫폼의 지원 여부를 확인하세요. 녹화 상태를 변경하는 요청에는 `X-Recording-Instance` 헤더가 필요하며, 중지 요청에는 수락된 `operation_id`도 필요합니다. 시작과 중지는 비동기 작업이므로 파일을 다운로드하기 전에 마무리가 끝날 때까지 기다려야 합니다. 전체 절차는 [녹화 매뉴얼](/manuals/recording/#recording-through-http)을 참고하세요.

HTTP 서비스는 Lua와 녹화기를 공유합니다. HTTP로 시작하면 지원되는 경우 기본적으로 어플리케이션 오디오가 활성화되고, Lua의 기본값은 영상만 녹화하는 것입니다. HTTP로 시작한 녹화에만 다운로드 가능한 `file` 정보가 있습니다. 다운로드 전에 `pending: false`, `finalized: true`, `file.state: "complete"`를 기다린 다음 [파일 크기와 SHA-256을 검증](/manuals/recording/#download-and-release-the-file)하세요. Lua와 HTTP 클라이언트를 함께 사용하려면 [녹화기 공유](/manuals/recording/#sharing-the-recorder-with-http-clients)를 참고하세요.

## Metal GPU 트레이스 엔드포인트 {#metal-gpu-trace-endpoint}

macOS의 디버그 엔진은 Metal GPU 트레이스 캡처용 `/profiler/gputrace`를 제공합니다. 이 경로는 macOS에서만 `/openapi.json`에 나타납니다. 캡처에는 네이티브 Metal 어댑터와 엔진 실행 환경의 `METAL_CAPTURE_ENABLED=1` 설정이 필요합니다. 캡처를 사용할 수 없으면 요청에 `error.code: "gputrace_unsupported"`를 포함한 HTTP 501을 반환합니다.

| 엔드포인트 | 용도 |
| --- | --- |
| `POST /profiler/gputrace` | 쓰기 가능한 절대 `.gputrace` 경로로 캡처를 예약합니다. `frames`의 기본값은 `1`이며 `1`–`10000`을 지정할 수 있습니다. |
| `GET /profiler/gputrace` | 현재 또는 최근 캡처의 상태, 경로, 프레임 수를 읽습니다. |
| `DELETE /profiler/gputrace` | 대기 중인 캡처를 취소하거나 현재 렌더링 프레임 이후 활성 캡처를 마칩니다. 디스크의 트레이스는 유지합니다. |

수락된 요청은 `ok: true`와 `data` 오브젝트를 포함한 HTTP 200을 반환합니다. 캡처는 비동기로 진행되므로 `data.state`가 `complete`, `canceled`, `failed` 중 하나가 될 때까지 `GET`으로 조회하세요. 네이티브 시작 실패는 `data.error`로 보고됩니다. 트레이스는 엔진 호스트에 기록됩니다. 실행 명령, 지원 여부 확인, 캡처 예제, Xcode에서 결과를 여는 방법은 [Metal GPU 트레이스 캡처 가이드](/manuals/profiling/#metal-gpu-trace-capture)를 참고하세요.

## 익스텐션에서 정의한 런타임 경로 {#extension-defined-runtime-routes}

디버그 빌드에서는 네이티브 익스텐션 SDK를 통해 엔진 웹 서버에 액세스할 수 있습니다. 익스텐션은 해당 서버에 경로 접두사를 등록하고 런타임 데이터에 종속된 동작을 노출할 수 있습니다.

익스텐션은 별도의 HTTP 서버를 열지 않고 기존 엔진 서비스를 공유할 수 있으므로 개발 도구에 유용합니다.

익스텐션에서 정의한 런타임 자동화 API는 다음과 같이 구성해야 합니다.

* 고유하고 버전이 지정된 경로 접두사를 사용합니다.
* 지원하는 기능을 노출합니다.
* 구조화된 오류를 반환합니다.
* 사용할 수 없는 플랫폼 또는 엔진 기능을 명시적으로 처리합니다.
* 동작을 개발 및 테스트 환경에만 한정합니다.
* 릴리스 빌드에서 생략되는지 문서화합니다.

### OpenAPI에 익스텐션 작업 공개하기 {#publishing-extension-operations-in-openapi}

네이티브 익스텐션의 어플리케이션 초기화 콜백에서 `dmEngine::GetWebServer(app_params)`로 서버를 가져오고, 반환 핸들이 null이 아닐 때만 핸들러를 등록합니다. 콜백 설정은 [익스텐션 라이프사이클](/manuals/extensions/#extension-lifecycle)을 참고하세요.

인자가 네 개인 `dmWebServer::AddHandler()` 오버로드는 OpenAPI 3.0.3 Paths Object를 JSON 문자열로 받습니다. 오브젝트의 최상위 키는 경로입니다. 각 경로는 등록된 접두사로 시작해야 하며 다른 핸들러가 이미 문서화한 경로이면 안 됩니다. 인라인 스키마 또는 결과 문서 내부의 경로 참조를 사용하세요.

예를 들어 이 헬퍼는 콜백과 상태 엔드포인트 설명을 등록합니다:

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

`GET /example/v1/status`를 구현하고 문서에 명시된 `text/plain` 응답을 반환하는 콜백을 전달합니다. 요청 경로와 메서드를 확인하고 응답을 만드는 책임은 여전히 콜백에 있습니다. 등록 결과를 확인하세요. 잘못되거나 충돌하는 메타데이터는 `dmWebServer::RESULT_ERROR_INVAL`을 반환합니다.

서버는 문자열을 복사하지 않고 JSON 포인터를 보관합니다. `dmWebServer::RemoveHandler()`로 핸들러를 제거하거나 서버가 파괴될 때까지 저장 공간을 변경하지 않고 유효하게 유지해야 합니다. 예제의 `static const char` 배열은 이 요구를 충족합니다. 핸들러를 제거하면 이후 `/openapi.json` 응답에서도 해당 경로가 제거됩니다.

인자가 세 개인 `dmWebServer::AddHandler(server, prefix, &params)` 오버로드도 계속 지원합니다. 네 번째 인자로 `0`을 전달하는 것과 같으며, 핸들러는 OpenAPI 메타데이터 없이 등록되어 검색에서 제외됩니다.

## Automation Bridge 익스텐션 {#automation-bridge-extension}

공식 Defold [Automation Bridge](https://github.com/defold/extension-automation-bridge)는 엔진 서비스를 기반으로 구축된 디버그 전용 네이티브 익스텐션입니다. 다음 경로 아래에 버전이 지정된 런타임 자동화 API를 등록합니다.

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

이 런타임 API는 씬과 노드 검사, 입력, 화면 정보, 스크린샷, 녹화, 라이프사이클 정보 및 선택적 어플리케이션 정의 동기화 같은 기능을 제공합니다. 몇 가지 동작은 다음과 같습니다.

| 동작 | 수행 작업 |
| --- | --- |
| `GET  /automation-bridge/v1/health` | 상태 보고서, API 기능 및 호환성 |
| `POST /automation-bridge/v1/input/click` | 런타임 입력 상호작용 |
| `GET  /automation-bridge/v1/screenshot` | 런타임 스크린샷 |

프로젝트에 설치된 버전에 맞는 익스텐션의 [네이티브 API 문서](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge)와 [Python 헬퍼 문서](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python)를 사용하세요.

Automation Bridge는 릴리스 빌드에서 HTTP API와 Lua 모듈을 모두 노출하지 않습니다.

### 에디터 클라이언트와 런타임 클라이언트 {#editor-and-runtime-clients}

Automation Bridge Python 헬퍼는 두 클라이언트 아키텍처를 보여 줍니다. `editor.open_project()` 함수는 에디터 프로젝트 클라이언트를 반환하고, `project.build_and_run()`은 별도의 엔진 클라이언트를 반환합니다.

| 클라이언트 | 용도 |
| --- | --- |
| Project | 에디터 HTTP API, 명령, 디버거, 콘솔, 환경 설정, 레퍼런스, 미리보기, 빌드 및 포트 찾기 |
| Game - 엔진 서비스 | 씬, 입력, 스크린샷, 런타임 상태 및 동기화 |

`project`와 `game`으로 구분하면 프로세스 경계가 명확해집니다. 에디터 동작은 에디터 서버에서 수행되며, 실행 중인 게임에 대한 관찰과 동작은 엔진 서비스에서 수행됩니다.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## 제한 사항과 보안 {#limitations-and-security}

엔진 서비스와 익스텐션에서 정의한 경로는 개발 도구이므로 그에 맞게 취급해야 합니다.

::: important
Defold 1.14.1 이상에서는 실행 중인 엔진의 `/openapi.json` 문서를 사용해 작업을 검색합니다. 이전 엔진은 이 엔드포인트를 제공하지 않습니다. OpenAPI 메타데이터 없이 등록된 핸들러는 익스텐션의 해당 버전 API 문서를 참고하세요.
:::

런타임 스크립트, 물리, 입력, 동적으로 생성된 오브젝트 및 플랫폼 렌더링에는 실행 중인 엔진이 필요하며 [자동화 런타임 테스트](/manuals/automated-testing)를 통해 검증해야 합니다.

* 라우터, 공개 인터페이스 또는 신뢰할 수 없는 터널을 통해 서비스를 게시하지 마세요.
* 엔진 서비스 경로에서 인증을 요구한다고 가정하지 마세요.
* 런타임 경로는 익스텐션 버전, 플랫폼, 그래픽 백엔드 및 엔진 기능에 따라 달라질 수 있습니다.
* 익스텐션에서 정의한 최신 API에는 버전 또는 기능 협상을 사용하세요.
