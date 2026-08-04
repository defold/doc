---
title: 자동화 테스트 및 검증
brief: 이 매뉴얼에서는 로컬, 실행 중인 게임, 브라우저 및 지속적 통합 환경에서 결정론적 Defold 테스트를 설계하고 실행하고 보고하는 방법을 설명합니다.
---

# 자동화 테스트 및 검증 {#automated-testing-and-verification}

자동화 테스트는 명시적이고 머신이 읽을 수 있는 증거를 사용하여 Defold 코드와 컨텐츠를 검증합니다. 이 매뉴얼을 활용하여 로컬 스크립트, CI(Continuous Integration) 러너 및 코딩 에이전트에서 모두 작동하는 테스트를 설계하세요. 모듈 테스트, 실행 중인 컬렉션, 브라우저 테스트, 런타임 자동화, 시각적 검사, headless 빌드를 다루고 유용한 모범 사례를 제공합니다.

## 검증 수준 {#verification-levels}

좋은 자동화 테스트 수준은 테스트를 단위 테스트, 통합 테스트, 엔드투엔드(E2E) 테스트의 세 가지 주요 계층으로 나누는 테스트 피라미드 프레임워크를 따릅니다. Defold에서는 부트스트랩 시 로드할 수 있는 특정 컬렉션으로 테스트를 분리할 수 있습니다. 일반적으로 문제를 감지할 수 있는 가장 좁고 빠른 검사부터 시작한 다음 필요할 때 런타임 또는 플랫폼 테스트를 추가하는 것이 좋습니다.

| 수준 | 적합한 증거 |
| --- | --- |
| 정적 검증 | 파서, 포멧터, 리소스 검증 도구 또는 생성된 파일 비교 |
| 모듈 테스트 | 엔진 종속성이 최소화된 재사용 가능한 Lua 로직의 assertion 결과 |
| 실행 중인 컬렉션 | 메세지, 컴포넌트, 입력, 물리, 라이프사이클 및 엔진 동작 |
| 런타임 자동화 | 실시간 씬 상태, 주입된 입력, 어플리케이션 상태 및 런타임 스크린샷 |
| HTML5 브라우저 테스트 | Canvas 입력, 브라우저 연동, 뷰포트 동작 및 웹 출력 |
| 플랫폼 테스트 | 실제 타겟 플랫폼의 동작과 렌더링 |
| 빌드 및 번들 | Bob 종료 상태, 빌드 보고서, 아카이브 및 번들 아티팩트 |

컴파일에 성공했다는 것은 프로젝트가 빌드된다는 의미이지만 게임플레이 동작이 올바르다는 의미는 아닙니다. 스크린샷은 복잡한 전환, 애니메이션, 상호작용 또는 게임플레이 흐름을 증명하지 못하지만, 최신 멀티모달 솔루션에서 한 프레임의 모습과 쉐이더 및 시각적 레이아웃이 올바른지 검사하는 데 사용할 수 있습니다. 하지만 자동화 테스트에서는 조건을 직접 표현할 수 있을 때마다 결정론적 assertion을 우선하세요.

## 재사용 및 테스트 가능한 Lua 코드 {#reusable-and-testable-lua-code}

재사용 가능한 로직은 엔진 종속성을 최소화한 Lua 모듈에 보관하세요. 그러면 순수 데이터 변환, 규칙, 상태 머신 및 계산을 완전한 게임 월드를 구성하지 않고도 실행할 수 있습니다.

엔진과 상호작용하는 코드를 이 코드가 호출하는 로직과 분리하세요. 스크립트는 메세지와 컴포넌트 상태를 모듈 호출로 변환할 수 있고, 테스트는 제어된 입력으로 모듈을 직접 호출할 수 있습니다.

자세한 내용은 [코드 작성 매뉴얼](/manuals/writing-code)을 참고하세요.

## 실행 중인 컬렉션의 테스트 {#tests-in-a-running-collection}

동작이 게임 오브젝트, 컴포넌트, 메세지, 입력, 물리 또는 기타 엔진 시스템에 종속된다면 전용 테스트 컬렉션을 사용하세요.

각 테스트에서는 다음을 수행해야 합니다.

1. 알려진 상태를 설정합니다.
2. 하나의 동작을 실행합니다.
3. 예상 결과를 assertion하고 평가합니다.
4. 생성된 리소스를 정리합니다.
5. 구조화된 결과 설명을 출력합니다.

테스트에는 격리된 테스트 컬렉션을 우선 사용하세요. 프로젝트는 `game.project`의 임시 프로젝트 설정을 통해 테스트 부트스트랩 컬렉션을 선택할 수 있습니다.

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

프로젝트의 일반 설정에 임시 테스트 부트스트랩을 남겨 두지 마세요. CI에서는 Bob에 전달하는 전용 설정 파일을 우선 사용하세요. CI는 저장소의 상태를 변경할 수 없으며 필요할 때 임시 변경만 해야 합니다.

복잡한 게임에서는 미리 정의된 시나리오와 간단한 블록아웃으로 작은 "development room" 컬렉션을 만들 수 있습니다. 이러한 컬렉션을 사용하면 게임에서 관련 없는 상태와 섹션을 거치지 않고도 메커니즘을 재현하고 테스트 개발을 더 쉽게 할 수 있습니다.

### 테스트 프레임워크 {#test-frameworks}

프로젝트에서 간단한 러너를 구현하거나 [커뮤니티 테스트 라이브러리](https://defold.com/assets/?tag=testing)를 사용할 수 있습니다.

예를 들어 [DefTest](https://defold.com/assets/deftest/)는 Telescope를 기반으로 하는 단위 테스트 라이브러리입니다. 테스트 스위트, 설정 및 정리 함수, assertion, 이름 필터링, 일부 Defold API용 mock 및 선택적 LuaCov 커버리지를 지원합니다. Bob으로 생성된 headless 번들을 포함하여 전용 부트스트랩 컬렉션에서 테스트를 실행할 수 있습니다.

## 구조화된 테스트 결과 {#structured-test-results}

프레임워크의 콘솔/로그 요약은 개발자에게 유용할 수 있지만 무인 자동 컨트롤러에는 여전히 명시적인 완료 결과가 필요합니다. 컨트롤러에서 테스트 결과를 쉽게 처리할 수 있도록 필요한 경우 프레임워크 콜백이나 요약 주위에 작은 어댑터를 추가하세요.

간단한 결과 설명에서는 고유한 접두사 뒤에 각 실제 콘솔 줄마다 하나의 JSON 오브젝트를 사용할 수 있습니다.

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

수집기는 각 줄을 독립적으로 처리하고, `TEST` 접두사를 찾고, 그 뒤의 JSON을 파싱하고, 관련 없는 엔진 출력을 무시해야 합니다.

이전 프로세스나 동시에 실행되는 프로세스의 출력이 현재 실행을 완료시키지 못하도록 고유한 실행 식별자를 포함하세요. 모든 테스트 스위트는 명확한 최종 이벤트(예: `Pass`, `Failure`, `Crash`, `Timeout` 등)를 하나씩 출력해야 합니다.

### 콘솔 출력 수집 {#collecting-console-output}

게임을 에디터에서 실행하면 현재 콘솔 기록과 연속 스트림을 모두 제공합니다. 일치하는 테스트 스위트 완료 이벤트, 프로세스 종료, 오류를 받거나 구성된 타임아웃 또는 줄 제한에 도달하면 스트림을 닫으세요.

자세한 내용은 [에디터 HTTP API 매뉴얼](/manuals/editor-http-api/#reading-console-output)을 참고하세요.

### 저장되는 로그 {#persisted-logs}

Defold는 `Write Log File`을 `game.project`에서 활성화하여 게임 로그를 저장할 수도 있습니다. [게임 및 시스템 로그](/manuals/debugging-game-and-system-logs/)를 참고하세요. 파일 로깅은 패키지된 어플리케이션과 에디터 콘솔을 사용할 수 없는 타겟 기기를 테스트할 때 유용합니다.

프로젝트에서 내장 `print()` 및 `pprint()` 함수나 Asset Portal의 다른 [로깅 라이브러리](https://defold.com/assets/?tag=logging)를 사용할 수 있습니다.

## 런타임 API를 통한 실행 중인 게임 테스트 {#testing-a-running-game-through-a-runtime-api}

런타임 자동화 API는 실시간 디버그 엔진을 검사하고 제어할 수 있습니다. 테스트에서 런타임 오브젝트를 찾고, 입력을 주입하고, 표시 상태를 기다리거나 렌더링된 결과를 캡처해야 할 때 사용할 수 있습니다.

자세한 내용은 [엔진 서비스 매뉴얼](/manuals/engine-service/#automation-bridge-extension)을 참고하세요.

다음 예제에서는 [Automation Bridge](https://github.com/defold/extension-automation-bridge) Python 헬퍼 구조를 사용합니다. 프로젝트에는 호환되는 버전의 디버그 익스텐션이 포함되어 있어야 하며, 지정된 automation id를 가진 요소를 노출하고 `screen` 어플리케이션 상태를 게시해야 합니다.

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

어플리케이션에서 정의한 상태와 automation id는 Automation Bridge의 선택적 디버그 전용 Lua API를 사용하며 프로젝트에서 이를 활성화하고 게시해야 합니다. 고정된 대기 시간은 머신 속도와 프레임 타이밍에 영향을 받기 쉽습니다. 정의된 상태를 제한된 시간 동안 폴링하는 방식이 더 안정적입니다.

Automation Bridge는 익스텐션이며 핵심 엔진의 일부가 아닙니다. 설치된 버전의 선택자, 대기, 상태, 이벤트, 스크린샷 및 진단에 대해서는 [Python API 레퍼런스](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python)를 참고하세요.

## HTML5 브라우저 테스트 {#browser-tests-for-html5}

에디터는 [에디터 HTTP API 매뉴얼](/manuals/editor-http-api/#building-html5)에 설명된 현재 `build-html5` 명령을 통해 HTML5 빌드를 생성하고 제공할 수 있습니다. Bob을 사용해 에디터 없이 HTML5 번들을 만들 수도 있습니다.

Playwright, Puppeteer, Selenium, WebdriverIO 또는 Cypress와 같은 외부 브라우저 자동화 도구는 다음 작업을 수행할 수 있습니다.

* Defold canvas와 어플리케이션 준비 상태 기다리기
* 키보드, 마우스 및 에뮬레이션된 터치 입력 보내기
* 뷰포트 크기 변경하기
* 브라우저 콘솔 출력과 JavaScript 오류 수집하기
* 스크린샷을 찍고 아티팩트 비교하기

canvas에 전달된 입력은 프로젝트의 일반 입력 바인딩과 `on_input()` 콜백을 통해 처리됩니다. 게임 응답과 브라우저별 연동 지점을 모두 테스트하세요.

가장 안정적인 접근 방식은 커스텀 `index.html`에서 명시적인 JavaScript 테스트 브리지를 노출하는 것입니다. Defold 측에서 HTML5 빌드는 `html5.run()`을 사용하여 JavaScript를 실행할 수 있으므로 이러한 브라우저 측 브리지와 통신할 수 있습니다. JavaScript에서 Defold로 전달되는 명령에는 전용 JavaScript-to-engine 브리지를 사용하세요.

브라우저 테스트는 제한된 시간 안에 끝나도록 구성하세요. 최종 보고서에서 페이지 로드 실패, 누락된 canvas, JavaScript 오류, 테스트 타임아웃 및 실패한 게임 assertion을 구분하세요.

## 시각적 검사를 위한 에디터 미리보기 및 런타임 스크린샷 {#editor-previews-and-runtime-screenshots}

열린 에디터의 기본 씬 뷰에 있는 리소스 파일이나 런타임 게임의 스크린샷을 생성할 수 있습니다.

| 방법 | 용도 |
| --- | --- |
| [에디터 미리보기](/manuals/editor-http-api/#rendering-scene-previews) | 로드된 리소스 레이아웃(예: 레벨 또는 GUI), 아틀라스 구성, 타일 맵 검사, 정적 씬 구성, 에디터 렌더링 및 쉐이더 정확성 또는 문서 썸네일 생성 |
| [런타임 스크린샷](/manuals/engine-service) | 제어된 시나리오에서 실행 중인 빌드가 렌더링한 상태 |

회귀 테스트 등에 이미지 비교를 사용할 수 있습니다. 검사에 실패하면 차이 이미지와 비교 메트릭을 저장하세요.

멀티모달 모델은 잘린 텍스트, 겹치는 컨트롤, 불명확한 선택 상태 또는 안전 영역 밖의 컨텐츠처럼 다른 방식으로 표현하기 어려운 시각 검사의 의미론적 조건을 평가할 수 있습니다. 이 평가를 명시적 기준과 함께 추가 신호로 취급하는 것이 좋지만, 결정론적 로직 검사나 이미지 비교를 대체해서는 안 됩니다.

## Headless 테스트와 CI {#headless-tests-and-ci}

에디터와 독립적인 CI에는 Bob builder CLI 도구를 사용하세요.

Bob을 사용하여 종속성을 확인하고 게임, 아카이브 또는 standalone 번들을 빌드하고 JSON 보고서를 생성할 수 있습니다.

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

전용 설정으로 headless 테스트 번들을 빌드합니다.

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

플랫폼에 적합한 프로세스 컨트롤러로 생성된 실행 파일을 실행하세요. 종료 상태와 로그를 캡처하고, 타임아웃을 적용하고, 구조화된 테스트 스위트 완료 이벤트를 요구하세요.

[Bob 매뉴얼](/manuals/bob)은 플랫폼, 설정 파일, 번들, 캐쉬, 네이티브 익스텐션 및 빌드 보고서를 설명합니다.

## 실패 보고서와 아티팩트 {#failure-reports-and-artifacts}

좋은 테스트 결과에는 실패를 재현하고 진단하기에 충분한 증거가 남아 있어야 합니다.

* 테스트 이름, 실행 식별자 및 assertion 세부 정보
* 경과 시간과 분류된 결과
* 전체 콘솔 또는 프로세스 로그
* Defold 버전, 타겟 플랫폼 및 관련 구성
* Bob 빌드 보고서와 프로세스 종료 상태
* 사용 가능한 경우 런타임 상태 또는 씬 스냅샷
* 스크린샷, baseline 차이, 녹화 또는 브라우저 trace
* 생성된 모든 아티팩트의 경로 또는 링크

개발자, 로컬 스크립트, CI 서비스 또는 [AI 코딩 에이전트](/manuals/ai-agents)에서 동일한 포멧을 사용할 수 있어야 합니다. 이렇게 하면 진단이나 복구를 위임하더라도 검증이 결정론적으로 유지됩니다.
