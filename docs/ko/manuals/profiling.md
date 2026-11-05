---
title: Defold 프로파일링
brief: 이 매뉴얼은 Defold에서 제공하는 프로파일링 기능을 설명합니다.
---

# 프로파일링

Defold에는 엔진과 빌드 파이프라인에 통합된 프로파일링 도구가 포함되어 있습니다. 이 도구들은 성능, 메모리, 리소스 사용량 문제를 찾는 데 도움이 됩니다. 런타임 프로파일링 데이터는 여러 기능에서 사용할 수 있습니다.

* 기본 프로파일러와 게임 내 비주얼 프로파일러는 모든 플랫폼에서 사용할 수 있습니다.
* [Remotery 프로파일러](https://github.com/Celtoys/Remotery)와 대화형 웹 프레임 프로파일러는 데스크탑과 모바일 플랫폼에서 사용할 수 있습니다.
* Metal을 사용하는 macOS 디버그 빌드는 Xcode에서 검사할 [GPU 트레이스](#metal-gpu-trace-capture)를 저장할 수 있습니다.
* HTML5 빌드는 Defold scope를 브라우저의 Web Performance API에 게시할 수 있습니다.

[App Manifest](/manuals/app-manifest/#profiler)의 **Profiler** 설정은 프로파일러 코드를 빌드에 링크할지 제어합니다. 기본값은 **Debug Only**이며, **None**은 코드를 제외하고 **Always**는 디버그 빌드와 릴리스 빌드 모두에 포함합니다. *game.project*의 `profiler` 설정은 런타임 동작을 제어하지만 제외된 프로파일러 코드를 빌드에 다시 링크하지는 않습니다. 특히 **Track CPU**는 CPU 사용량 sampling을 제어하며 App Manifest 선택과는 별개입니다.

## 런타임 비주얼 프로파일러

프로파일러 지원을 포함한 빌드에는 실행 중인 어플리케이션 위에 라이브 정보를 오버레이로 표시하는 런타임 비주얼 프로파일러가 포함되어 있습니다:

```lua
function on_reload(self)
    -- 핫 리로드 시 비주얼 프로파일러를 토글합니다.
    profiler.enable_ui(true)
end
```

![비주얼 프로파일러](images/profiling/visual_profiler.png)

비주얼 프로파일러는 데이터를 표시하는 방식을 변경하는 데 사용할 수 있는 여러 함수를 제공합니다:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

프로파일러 함수에 대한 자세한 내용은 [profiler API 레퍼런스](/ref/profiler/)를 참조하세요.

## 웹 프로파일러
프로파일러 지원을 포함한 데스크탑 또는 모바일 빌드를 실행하는 동안 브라우저를 통해 대화형 프레임 및 리소스 프로파일러에 접근할 수 있습니다.

### Remotery 프레임 프로파일러
프레임 프로파일러를 사용하면 실행 중인 게임을 샘플링하고 개별 프레임을 자세히 분석할 수 있습니다. 프로파일러에 접근하려면:

1. 타겟 기기에서 게임을 시작합니다.
2. <kbd> Debug ▸ Open Web Profiler</kbd> 메뉴를 선택합니다.

프레임 프로파일러는 실행 중인 게임을 서로 다른 관점으로 보여주는 여러 섹션으로 나뉩니다. 오른쪽 위 모서리의 Pause 버튼을 눌러 프로파일러가 뷰를 업데이트하는 것을 일시적으로 멈출 수 있습니다.

![웹 프로파일러](images/profiling/webprofiler_page.png)

::: sidenote
여러 타겟을 동시에 사용할 때는 페이지 상단의 Connection Address 필드를 타겟이 시작될 때 콘솔에 표시된 Remotery 프로파일러 URL과 일치하도록 변경해 타겟 사이를 수동으로 전환할 수 있습니다:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline은 엔진에서 캡처한 데이터 프레임을 Thread마다 하나의 가로 타임라인으로 표시합니다. Main은 모든 게임 로직과 대부분의 엔진 코드가 실행되는 메인 thread입니다. Remotery는 프로파일러 자체를 위한 것이고, Sound는 사운드 믹싱과 재생 thread를 위한 것입니다. 확대하거나 축소할 수 있으며(마우스 휠 사용), 개별 프레임을 선택해 Frame Data 뷰에서 해당 프레임의 세부 정보를 볼 수 있습니다.

  ![Sample Timeline](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: Frame Data 뷰는 현재 선택한 프레임의 모든 데이터를 세부 항목으로 나누어 보여주는 테이블입니다. 각 엔진 범위(scope)에 몇 밀리초가 소요되었는지 볼 수 있습니다.

  ![프레임 데이터](images/profiling/webprofiler_frame_data.png)


Global Properties
: Global Properties 뷰는 카운터 테이블을 표시합니다. 예를 들어 드로우콜 수나 특정 타입의 컴포넌트 수를 추적하기 쉽게 해 줍니다.

  ![Global Properties](images/profiling/webprofiler_global_properties.png)

::: sidenote
LuaMem 값은 Lua 가비지 컬렉터가 보고한 Lua VM의 메모리 사용량을 킬로바이트 단위로 나타냅니다. Memory는 엔진이 사용한 메모리 양을 킬로바이트 단위로 나타냅니다.
:::

::: important
[Max Sample Count 설정](/manuals/project-settings/#max-sample-count)은 thread마다 프레임마다 기록되는 프로파일러 sample 수를 제한합니다. 프로파일러에서 제한을 초과했다고 보고하면 먼저 네이티브 익스텐션 프로파일링 코드에 짝이 맞지 않는 scope begin/end 쌍이 있는지 확인하세요. 실제 프레임에 설정된 제한보다 많은 scope가 포함된 경우에만 상한을 높이세요.
:::

### 리소스 프로파일러
리소스 프로파일러를 사용하면 실행 중인 게임을 검사하고 리소스 사용량을 자세히 분석할 수 있습니다. 프로파일러에 접근하려면:

1. 타겟 기기에서 게임의 디버그 빌드를 시작합니다.
2. 브라우저에서 [엔진 서비스 주소](/manuals/engine-service/#availability-and-port-discovery)인 `http://<address>:<port>/`를 엽니다. 실행 중인 엔진이 콘솔에 보고한 주소와 포트를 사용하세요.

리소스 프로파일러는 두 섹션으로 나뉩니다. 하나는 게임에 현재 인스턴스화된 컬렉션, 게임 오브젝트, 컴포넌트의 계층 뷰를 표시하고, 다른 하나는 현재 로드된 모든 리소스를 표시합니다.

![리소스 프로파일러](images/profiling/webprofiler_resources_page.png)

컬렉션 뷰
: 컬렉션 뷰는 게임에 현재 인스턴스화된 모든 게임 오브젝트와 컴포넌트의 계층 목록과, 이들이 어느 컬렉션에서 비롯되었는지를 표시합니다. 특정 시점에 게임에 어떤 것이 인스턴스화되어 있는지, 그리고 오브젝트가 어디에서 비롯되었는지 파고들어 이해해야 할 때 매우 유용한 도구입니다.

리소스 뷰
: 리소스 뷰는 현재 메모리에 로드된 모든 리소스와 각 리소스의 크기 및 참조 수를 표시합니다. 어플리케이션의 메모리 사용량을 최적화할 때 특정 시점에 무엇이 메모리에 로드되어 있는지 이해해야 하는 경우 유용합니다.

#### 리소스 로드 시간 {#resource-loading-times}

개별 리소스를 로드하는 데 걸리는 시간도 검사할 수 있습니다. 게임을 시작하기 전에 *game.project*의 [Resource → Profile](/manuals/project-settings/#profile)을 활성화하세요. 텍스트 뷰에서는 다음과 같이 설정합니다:

```ini
[resource]
profile = 1
```

이 설정은 기본적으로 비활성화되어 있습니다. 시작 시 로드를 측정하려면 활성화한 후 게임을 다시 시작하세요. 완료되거나 실패한 로드마다 리소스 경로, 총 시간, preload, read, create, post-create, queue, wait 단계의 시간을 담은 INFO 레벨 로그 항목을 기록합니다. 캐쉬 적중은 새 로드 기록을 만들지 않습니다.

리소스 프로파일러에서 **Capture**, **Show load times**를 차례로 클릭하면 시간 열이 나타납니다. **Capture**는 보관된 측정값의 표시를 갱신할 뿐, 프로파일링을 활성화하거나 이전 로드를 소급하여 측정하지 않습니다.

| 열 | 의미 |
| --- | --- |
| **Load (ms)** | 종속성, post-create 작업, 대기열 및 대기를 포함한 최초 로드의 총 경과 시간입니다. |
| **Preload (ms)** | preload 콜백에서 리소스를 준비하는 데 걸린 시간입니다. |
| **Read (ms)** | 리소스 데이터를 읽는 데 걸린 시간입니다. |
| **Create (ms)** | create 콜백에서 런타임 리소스를 생성하는 데 걸린 시간입니다. |

로드 시간을 표시하면 가장 느린 리소스부터 총 로드 시간 순으로 정렬합니다. 시간 열 제목을 클릭하면 해당 단계로 정렬하고, 다시 클릭하면 순서가 뒤집힙니다. **Load** 열의 막대는 현재 보이는 가장 느린 리소스 대비 각 총 시간을 표시합니다. 열을 다시 숨기려면 **Hide load times**를 클릭하세요.

로드 및 콜백 시간에는 중첩된 종속성 작업도 포함됩니다. 같은 작업이 여러 리소스의 측정값에 포함될 수 있으므로 시작 시간을 계산할 때 리소스별 총 시간을 합산하지 마세요. **Preload**, **Read**, **Create** 열만으로도 총 로드 시간을 모두 설명할 수는 없습니다. 추가 단계는 로그에서 확인할 수 있습니다.

긴 대시(`—`)는 완료된 측정값이 없다는 뜻입니다. 프로파일링이 비활성화되어 있거나 최초 로드가 아직 끝나지 않은 경우 등이 해당합니다. 측정된 0은 `0.000`으로 표시됩니다. 측정값은 최초 로드를 설명합니다. 캐쉬 적중과 핫 리로드는 값을 바꾸지 않으며 리소스를 언로드하면 보관된 측정값이 제거됩니다.

## Metal GPU 트레이스 캡처 {#metal-gpu-trace-capture}

[엔진 HTTP 서비스](/manuals/engine-service/#metal-gpu-trace-endpoint)는 macOS에서 Metal GPU 명령을 *.gputrace* 문서로 캡처할 수 있습니다. 완료된 트레이스를 Xcode에서 열어 캡처한 프레임을 검사하세요. 이 기능은 디버그 엔진에 내장되어 있습니다.

### 실행 및 지원 확인 {#launch-and-check-support}

네이티브 Metal 그래픽 백엔드를 포함한 macOS [Debug 번들](/manuals/bundling/#release-vs-debug)을 만듭니다. App Manifest를 사용한다면 Metal을 포함하는 **Graphics (macOS)** 옵션을 선택하세요. [그래픽 백엔드](/manuals/app-manifest/#graphics)를 참고하세요.

터미널에서 `METAL_CAPTURE_ENABLED=1`로 번들의 실행 파일을 실행하고 Metal 어댑터를 선택합니다. 다음 예제의 번들 경로와 실행 파일 이름을 바꾸세요:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

환경 변수는 엔진이 시작할 때 설정되어 있어야 합니다. HTTP 요청용 터미널에서만 설정해도 이미 실행 중인 엔진의 캡처는 활성화되지 않습니다.

다른 터미널에서 [로그에 표시된 엔진 서비스 포트](/manuals/engine-service/#availability-and-port-discovery)를 사용합니다. 다음 예제는 `curl`과 `jq`를 사용합니다:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

이 경로는 macOS에서만 등록됩니다. OpenAPI 문서의 항목이 `null`이면 이 엔진이 경로를 제공하지 않는다는 뜻입니다. 경로가 있어도 캡처 지원은 그래픽 어댑터와 실행 환경에 따라 달라집니다. Metal 캡처를 사용할 수 없으면 `GET /profiler/gputrace`는 `error.code: "gputrace_unsupported"`가 있는 HTTP 501을 반환합니다. 진행하기 전에 엔진이 Metal을 사용하고 `METAL_CAPTURE_ENABLED=1`로 실행되었는지 확인하세요. 지원되는 요청은 캡처 상태를 포함한 HTTP 200을 반환합니다.

### 프레임 캡처 및 검사 {#capture-and-inspect-frames}

`.gputrace`로 끝나는 쓰기 가능한 절대 출력 경로를 선택합니다. 상위 디렉토리는 존재해야 하고 그 경로에 기존 트레이스가 없어야 합니다. 경로는 엔진을 실행하는 컴퓨터의 경로입니다. 로컬 엔진에서 다음 예제는 새 임시 디렉토리를 만들고 한 프레임을 요청합니다:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames`는 선택 사항이며 기본값은 `1`, 허용 값은 `1`부터 `10000`까지의 정수입니다. 캡처는 다음 렌더링 프레임 전에 시작하고 요청한 수의 완전한 프레임을 제출한 후 멈춥니다. 기다리는 동안 게임이 계속 렌더링되도록 하세요. 대기 중이거나 활성인 캡처는 하나만 가능하며, 추가 시작 요청은 `error.code: "gputrace_active"`가 있는 HTTP 409를 반환합니다.

캡처가 예약되면 `POST`는 `ok: true`와 `data.state: "pending"`을 포함한 HTTP 200을 반환합니다. 캡처 완료는 이후 상태 요청으로 보고됩니다. `data.state`가 `complete`, `canceled`, `failed` 중 하나가 될 때까지 상태 요청을 반복하세요:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | 의미 |
| --- | --- |
| `idle` | 예약된 캡처가 없습니다. |
| `pending` | 렌더링 시작을 기다리고 있습니다. |
| `capturing` | 캡처가 진행 중입니다. `data.frames_captured`는 완료된 프레임 수를 보고합니다. |
| `complete` | 캡처가 끝났으며 트레이스를 열 수 있습니다. |
| `canceled` | 대기 중인 캡처가 시작 전에 취소되었습니다. |
| `failed` | 캡처를 시작하지 못했습니다. 네이티브 오류는 `data.error`를 확인하세요. |

`GET`은 현재 또는 최근 캡처를 설명합니다. `data.path`가 요청한 경로와 일치하는지 확인하세요. 실패한 캡처도 `ok: true`가 있는 HTTP 200을 반환하므로 `data.state`와 `data.error`로 결과를 판별합니다. 자동 클라이언트는 지연과 시간 제한을 두고 조회하세요.

상태가 `complete`가 되면 엔진의 Mac에서 Xcode로 트레이스를 엽니다:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

HTTP 엔드포인트는 상태를 반환하며, 트레이스는 엔진 호스트의 `data.path`에 저장됩니다. 원격 엔진은 로컬에서 열기 전에 해당 호스트에서 완료된 문서를 가져오세요.

### 캡처 취소 또는 중지 {#cancel-or-stop-a-capture}

대기 중인 캡처를 취소하거나 활성 캡처를 일찍 마치려면:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

대기 중인 캡처는 `canceled`로 바뀝니다. 활성 캡처는 `data.stop_requested`가 `true`로 바뀌고 현재 렌더링 프레임을 제출한 후 끝납니다. 종료 상태에 도달할 때까지 `GET`으로 계속 조회하세요. `DELETE`는 이미 디스크에 기록된 트레이스를 유지합니다. 대기 중이거나 활성인 캡처가 없으면 `error.code: "gputrace_inactive"`가 있는 HTTP 409를 반환합니다.

## HTML5 브라우저 performance timeline

HTML5는 브라우저 timeline에 Remotery 대신 Web Performance API를 사용합니다. Defold scope를 기록하려면 다음과 같이 합니다.

1. 선택한 App Manifest profiler 모드가 실행 중인 빌드 variant에 프로파일러 지원을 포함하는지 확인합니다.
2. *game.project*에서 **Performance Timeline Enabled**(`profiler.performance_timeline_enabled`)를 활성화합니다.
3. HTML5 빌드를 실행하고 브라우저 개발자 도구를 엽니다.
4. 브라우저의 **Performance** pane에서 세션을 기록하고 결과 timeline의 Defold scope를 확인합니다.

이 브라우저 timeline은 게임 내 비주얼 프로파일러와 대화형 Remotery 웹 프로파일러 모두와 별개입니다.


## 빌드 리포트 {#build-reports}
게임을 번들링할 때 빌드 리포트를 만들 수 있는 옵션이 있습니다. 이 옵션은 게임 번들에 포함되는 모든 에셋의 크기를 파악하는 데 매우 유용합니다. 게임을 번들링할 때 *Generate build report* 체크박스를 선택하기만 하면 됩니다.

![빌드 리포트](images/profiling/build_report.png)

빌더는 게임 번들과 함께 `report.html`이라는 파일을 생성합니다. 리포트를 살펴보려면 이 파일을 웹 브라우저에서 엽니다:

![빌드 리포트](images/profiling/build_report_html.png)

*Overview*는 리소스 타입을 기준으로 프로젝트 크기의 전체적인 시각적 분석을 제공합니다.

*Resources*는 크기, 압축률, 암호화 여부, 타입, 디렉토리 이름을 기준으로 정렬할 수 있는 자세한 리소스 목록을 보여줍니다. 표시되는 리소스 항목을 필터링하려면 "search" 필드를 사용합니다.

*Structure* 섹션은 프로젝트 파일 구조 안에서 리소스가 어떻게 구성되어 있는지를 기준으로 크기를 보여줍니다. 항목은 파일과 디렉토리 컨텐츠의 상대적 크기에 따라 초록색(가벼움)부터 파란색(무거움)까지 색상으로 구분됩니다.


## 외부 도구
내장 도구 외에도 무료로 사용할 수 있는 고품질 추적 및 프로파일링 도구가 다양하게 있습니다. 다음은 일부 예입니다:

ProFi (Lua)
: 내장 Lua 프로파일러는 제공하지 않지만, 사용하기 쉬운 외부 라이브러리가 있습니다. 스크립트에서 시간이 어디에 사용되는지 찾으려면 코드에 직접 시간 측정을 삽입하거나 [ProFi](https://github.com/jgrahamc/ProFi) 같은 Lua 프로파일링 라이브러리를 사용하세요.

  순수 Lua 프로파일러는 설치하는 각 훅마다 상당한 오버헤드를 추가한다는 점에 유의하세요. 이런 이유로 이러한 도구에서 얻는 타이밍 프로파일은 어느 정도 주의해서 보아야 합니다. 하지만 카운팅 프로파일은 충분히 정확합니다.

Instruments (macOS and iOS)
: Xcode의 일부인 성능 분석 및 시각화 도구입니다. 하나 이상의 앱이나 프로세스의 동작을 추적하고 검사할 수 있으며, 기기별 기능(Wi-Fi와 Bluetooth 등)을 살펴보는 등 더 많은 작업을 할 수 있습니다.

  ![instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Apple에서 다운로드할 수 있는 "Additional Tools for Xcode" 패키지의 일부입니다(Xcode 메뉴에서 <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> 선택).

  이 도구를 사용하면 실행 중인 Defold 어플리케이션을 검사하고 OpenGL을 어떻게 사용하는지 볼 수 있습니다. OpenGL 함수 호출을 추적하고, OpenGL 함수에 중단점을 설정하고, 어플리케이션 리소스(텍스쳐, 프로그램, 쉐이더 등)를 조사하고, 버퍼 컨텐츠를 살펴보고, OpenGL 상태의 다른 측면을 확인할 수 있습니다.

  ![opengl profiler](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  게임의 CPU, 메모리, 네트워크 활동에 대한 실시간 데이터를 캡처하는 프로파일링 도구 모음입니다. 코드 실행에 대한 샘플 기반 메서드 추적을 수행하고, 힙 덤프를 캡처하고, 메모리 할당을 확인하고, 네트워크로 전송된 파일의 세부 정보를 검사할 수 있습니다. 이 도구를 사용하려면 `AndroidManifest.xml`에 `android:debuggable="true"`를 설정해야 합니다.

  ![android profiler](images/profiling/android_profiler.png)

  참고: Android Studio 4.1부터는 [Android Studio를 시작하지 않고 프로파일링 도구를 실행](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers)할 수도 있습니다.

Graphics API Debugger (Android)
: https://github.com/google/gapid

  어플리케이션에서 그래픽 드라이버로 보내는 호출을 검사하고, 조정하고, 재생할 수 있는 도구 모음입니다. 이 도구를 사용하려면 `AndroidManifest.xml`에 `android:debuggable="true"`를 설정해야 합니다.

  ![graphics api debugger](images/profiling/gapid.png)
