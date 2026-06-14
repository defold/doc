---
title: Defold 프로파일링
brief: 이 매뉴얼은 Defold에서 제공하는 프로파일링 기능을 설명합니다.
---

# 프로파일링

Defold에는 엔진과 빌드 파이프라인에 통합된 프로파일링 도구 세트가 포함되어 있습니다. 이 도구들은 성능과 메모리 사용량 문제를 찾는 데 도움이 되도록 설계되었습니다. 내장 프로파일러는 디버그 빌드에서만 사용할 수 있습니다. Defold에서 사용하는 프레임 프로파일러는 [Celtoys의 Remotery 프로파일러](https://github.com/Celtoys/Remotery)입니다.

## 런타임 비주얼 프로파일러

디버그 빌드에는 실행 중인 어플리케이션 위에 라이브 정보를 오버레이로 렌더링해 표시하는 런타임 비주얼 프로파일러가 포함되어 있습니다:

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

프로파일러 함수에 대한 자세한 내용은 [profiler API 레퍼런스](/ref/stable/profiler/)를 참조하세요.

## 웹 프로파일러
게임의 디버그 빌드를 실행하는 동안, 브라우저를 통해 대화형 웹 기반 프로파일러에 접근할 수 있습니다.

### 프레임 프로파일러
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

### 리소스 프로파일러
리소스 프로파일러를 사용하면 실행 중인 게임을 검사하고 리소스 사용량을 자세히 분석할 수 있습니다. 프로파일러에 접근하려면:

1. 타겟 기기에서 게임을 시작합니다.
2. 브라우저를 열고 http://localhost:8002 로 이동합니다.

리소스 프로파일러는 두 섹션으로 나뉩니다. 하나는 게임에 현재 인스턴스화된 컬렉션, 게임 오브젝트, 컴포넌트의 계층 뷰를 표시하고, 다른 하나는 현재 로드된 모든 리소스를 표시합니다.

![리소스 프로파일러](images/profiling/webprofiler_resources_page.png)

컬렉션 뷰
: 컬렉션 뷰는 게임에 현재 인스턴스화된 모든 게임 오브젝트와 컴포넌트의 계층 목록과, 이들이 어느 컬렉션에서 비롯되었는지를 표시합니다. 특정 시점에 게임에 어떤 것이 인스턴스화되어 있는지, 그리고 오브젝트가 어디에서 비롯되었는지 파고들어 이해해야 할 때 매우 유용한 도구입니다.

리소스 뷰
: 리소스 뷰는 현재 메모리에 로드된 모든 리소스와 각 리소스의 크기 및 참조 수를 표시합니다. 어플리케이션의 메모리 사용량을 최적화할 때 특정 시점에 무엇이 메모리에 로드되어 있는지 이해해야 하는 경우 유용합니다.


## 빌드 리포트
게임을 번들링할 때 빌드 리포트를 만들 수 있는 옵션이 있습니다. 이 옵션은 게임 번들에 포함되는 모든 에셋의 크기를 파악하는 데 매우 유용합니다. 게임을 번들링할 때 *Generate build report* 체크박스를 선택하기만 하면 됩니다.

![빌드 리포트](images/profiling/build_report.png)

빌더는 게임 번들과 함께 "report.html"이라는 파일을 생성합니다. 리포트를 살펴보려면 이 파일을 웹 브라우저에서 엽니다:

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

  게임의 CPU, 메모리, 네트워크 활동에 대한 실시간 데이터를 캡처하는 프로파일링 도구 모음입니다. 코드 실행에 대한 샘플 기반 메서드 추적을 수행하고, 힙 덤프를 캡처하고, 메모리 할당을 확인하고, 네트워크로 전송된 파일의 세부 정보를 검사할 수 있습니다. 이 도구를 사용하려면 "AndroidManifest.xml"에 `android:debuggable="true"`를 설정해야 합니다.

  ![android profiler](images/profiling/android_profiler.png)

  참고: Android Studio 4.1부터는 [Android Studio를 시작하지 않고 프로파일링 도구를 실행](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers)할 수도 있습니다.

Graphics API Debugger (Android)
: https://github.com/google/gapid

  어플리케이션에서 그래픽 드라이버로 보내는 호출을 검사하고, 조정하고, 재생할 수 있는 도구 모음입니다. 이 도구를 사용하려면 "AndroidManifest.xml"에 `android:debuggable="true"`를 설정해야 합니다.

  ![graphics api debugger](images/profiling/gapid.png)
