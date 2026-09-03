---
title: 엔진 서비스와 런타임 HTTP API
brief: 이 매뉴얼에서는 실행 중인 Defold 디버그 엔진의 개발용 HTTP 서비스와 런타임 익스텐션 또는 외부 도구에서 이 서비스를 사용하는 방법을 설명합니다.
---

# 엔진 서비스와 런타임 HTTP API {#the-engine-service-and-runtime-http-apis}

Debug 모드로 프로젝트를 실행하면 게임이 포함된 특정 엔진 런타임 인스턴스를 위한 프로세스와 특수 엔진 서비스가 생성됩니다. 이 서비스는 개발 및 프로파일링 인프라, 런타임 로직과 메세지, 엔진 상태 및 익스텐션에 액세스하는 데 사용할 수 있습니다.

엔진 서비스는 실행 중인 디버그 엔진(`dmengine`)이 소유하는 개발용 HTTP 서비스입니다.

이 서비스는 Defold 에디터에 속하며 열린 프로젝트를 제어하는 [에디터 서버](/manuals/editor-http-api)와 별개입니다.

두 서비스는 서로 다른 포트를 사용합니다. 에디터 포트에 연결된 도구는 그 포트에서 런타임 익스텐션 경로를 호출할 수 없으며, 반대로 엔진 서비스에 연결된 도구는 에디터 동작을 호출할 수 없습니다.

엔진 서비스는 디버그, 개발 및 프로파일링 인프라의 일부입니다. 릴리스 엔진 인스턴스는 이 서비스를 생성하지 않습니다.

## 사용 가능 여부와 포트 찾기 {#availability-and-port-discovery}

에디터가 디버그 엔진을 시작할 때 동적으로 할당된 서비스 포트를 요청합니다. 엔진은 선택된 포트를 `Console`에 보고합니다(CLI에서 실행한 경우에는 로그에도 보고합니다).

![Defold 디버그 빌드의 엔진 서비스 포트 정보](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

게임을 에디터에서 실행하면 이 줄이 에디터 콘솔에 나타납니다. 간단한 로컬 컨트롤러에서는 이 줄을 파싱할 수 있지만, 재사용 가능한 연동 기능에서는 에디터나 에디터 래퍼가 엔진 인스턴스와 등록된 포트를 추적하도록 해야 합니다. 이렇게 하면 이전 포트를 새로 시작했거나 재사용된 프로세스의 포트로 혼동하는 문제를 방지할 수 있습니다.

엔진은 지원되는 플랫폼에서 서비스 검색을 통해 개발 타겟을 알리기도 합니다. 이 메커니즘은 주로 Defold 도구에서 사용하며 영구적으로 하드 코딩된 포트로 대체해서는 안 됩니다.

서버는 지정된 포트의 localhost(`127.0.0.1`)에서 액세스할 수 있습니다.

![엔진 서버 액세스](images/automation/engine-server.png)

## 내장 엔드포인트 {#built-in-endpoints}

현재 디버그 엔진은 소수의 핵심 경로를 등록합니다.

| 엔드포인트 | 용도 |
| --- | --- |
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
현재 엔진 서비스는 OpenAPI 문서를 게시하지 않습니다. 연동 기능에서는 문서화된 동작이나 익스텐션의 버전이 지정된 API만 사용해야 합니다.
:::

런타임 스크립트, 물리, 입력, 동적으로 생성된 오브젝트 및 플랫폼 렌더링에는 실행 중인 엔진이 필요하며 [자동화 런타임 테스트](/manuals/automated-testing)를 통해 검증해야 합니다.

* 라우터, 공개 인터페이스 또는 신뢰할 수 없는 터널을 통해 서비스를 게시하지 마세요.
* 엔진 서비스 경로에서 인증을 요구한다고 가정하지 마세요.
* 런타임 경로는 익스텐션 버전, 플랫폼, 그래픽 백엔드 및 엔진 기능에 따라 달라질 수 있습니다.
* 익스텐션에서 정의한 최신 API에는 버전 또는 기능 협상을 사용하세요.
