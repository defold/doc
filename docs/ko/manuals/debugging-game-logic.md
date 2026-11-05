---
title: Defold에서 디버깅
brief: 이 매뉴얼은 Defold에서 제공하는 디버깅 기능을 설명합니다.
---

# 게임 로직 디버깅

Defold에는 검사 기능을 갖춘 통합 Lua 디버거가 포함되어 있습니다. 내장 [프로파일링 도구](/manuals/profiling)와 함께 사용하면 게임 로직의 버그 원인을 찾거나 성능 문제를 분석하는 데 도움이 되는 강력한 도구입니다.

## 출력과 시각적 디버깅

Defold에서 게임을 디버깅하는 가장 간단한 방법은 [print 디버깅](http://en.wikipedia.org/wiki/Debugging#Techniques)을 사용하는 것입니다. `print()` 또는 [`pprint()`](/ref/builtins#pprint) 문을 사용해 변수를 확인하거나 실행 흐름을 표시합니다. 스크립트가 없는 게임 오브젝트가 이상하게 동작한다면, 디버깅 목적으로만 스크립트를 붙여도 됩니다. 출력 함수 중 하나를 사용하면 에디터의 *Console* 뷰와 [게임 로그](/manuals/debugging-game-and-system-logs)에 출력됩니다.

출력 외에도 엔진은 화면에 디버그 텍스트와 직선을 그릴 수 있습니다. 이는 `@render` 소켓으로 메세지를 보내 수행합니다:

```lua
-- 화면에 디버그 텍스트로 "my_val" 값 그리기
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- 화면에 색상이 지정된 텍스트 그리기
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- 화면에 플레이어와 적 사이의 디버그 라인 그리기
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

시각적 디버그 메세지는 렌더링 파이프라인에 데이터를 추가하며 일반 렌더 파이프라인의 일부로 그려집니다.

* `"draw_line"`은 렌더 스크립트의 `render.draw_debug3d()` 함수로 렌더링되는 데이터를 추가합니다.
* `"draw_text"`는 `/builtins/fonts/debug/always_on_top_font.material` 메터리얼을 사용하는 `/builtins/fonts/debug/always_on_top.font`로 렌더링됩니다.
* `"draw_debug_text"`는 `"draw_text"`와 같지만, 커스텀 색상으로 렌더링됩니다.

이 데이터는 매 프레임 업데이트하려 할 가능성이 높으므로 `update()` 함수에서 메세지를 보내는 것이 좋습니다.

## 디버거 실행하기

Lua 디버거는 네이티브 디버그 및 헤드리스 빌드에서 사용할 수 있습니다. 에디터와 같은 Defold 버전의 엔진을 사용하세요. 릴리스와 웹 빌드는 디버거 연결을 지원하지 않습니다.

디버거를 실행하려면 <kbd>Debug ▸ Start/Attach</kbd>를 선택합니다. 디버거가 연결된 상태로 게임을 시작하거나 이미 실행 중인 게임에 연결합니다. 디버깅을 위해 게임을 시작할 때 에디터는 시작 스크립트를 실행하기 전에 활성화된 중단점을 설정하므로, 실행 전에 `init()`에 중단점을 설정할 수 있습니다.

기기에 연결하려면 <kbd>Project ▸ Targets</kbd>에서 기기를 선택한 다음 <kbd>Debug ▸ Start/Attach</kbd>를 선택합니다. 연결되면 다음 Lua 줄에서 일시 정지합니다. 에디터는 지원되는 로컬 및 원격 타겟에 대한 디버거 연결을 자동으로 설정합니다. 연결 요구 사항은 [원격 타겟](#remote-targets)을 참고하거나 [외부 디버거 연결 방법](#native-dap-connections)을 확인하세요.

![개요](images/debugging/overview.png)

디버거가 연결되면 콘솔의 디버거 제어 버튼이나 <kbd>Debug</kbd> 메뉴를 통해 게임 실행을 제어할 수 있습니다:

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  다음 소스 줄에서 Lua 실행을 일시 정지합니다. 게임 상태를 검사하고 한 단계씩 진행하거나 다음 중단점까지 실행을 계속할 수 있습니다. 현재 실행 위치는 코드 에디터에 표시됩니다:

  ![스크립트](images/debugging/script.png)

Continue
: ![play](images/debugging/play.svg){width=60px .left}
  게임 실행을 계속합니다. 일시 정지를 누르거나 설정한 브레이크포인트에 실행이 도달할 때까지 게임 코드가 계속 실행됩니다. 설정한 브레이크포인트에서 실행이 중단되면 실행 지점이 브레이크포인트 마커 위에 코드 에디터에 표시됩니다.

  ![브레이크](images/debugging/break.png)

Stop
: ![stop](images/debugging/stop.svg){width=60px .left}
  디버거를 중지합니다. 이 버튼을 누르면 디버거가 즉시 중지되고, 게임에서 분리되며, 실행 중인 게임이 종료됩니다.

Step Over
: ![step over](images/debugging/step_over.svg){width=60px .left}
  프로그램 실행을 한 단계 진행합니다. 실행 과정에 다른 Lua 함수 실행이 포함되어 있으면, 실행은 _함수 안으로 들어가지 않고_ 계속 진행한 뒤 함수 호출 아래의 다음 줄에서 중지됩니다. 이 예제에서 사용자가 "step over"를 누르면 디버거는 코드를 실행하고 `nextspawn()` 함수 호출이 있는 줄 아래의 `end` 문에서 중지됩니다.

  ![단계](images/debugging/step.png)

::: sidenote
단계 실행은 Lua 소스 줄을 따릅니다. 루프가 반복될 때처럼 같은 줄에 다시 도달할 수도 있으므로 항상 파일의 다음 줄로 이동하는 것은 아닙니다.
:::

Step Into
: ![step in](images/debugging/step_in.svg){width=60px .left}
  프로그램 실행을 한 단계 진행합니다. 실행 과정에 다른 Lua 함수 실행이 포함되어 있으면, 실행은 _함수 안으로 들어갑니다_. 함수를 호출하면 호출 스택(call stack)에 항목이 추가됩니다. 호출 스택 목록의 각 항목을 클릭하면 진입점과 해당 클로저의 모든 변수 내용을 볼 수 있습니다. 여기서는 사용자가 `nextspawn()` 함수 안으로 들어갔습니다.

  ![함수 안으로 들어가기](images/debugging/step_into.png)

Step Out
: ![step out](images/debugging/step_out.svg){width=60px .left}
  현재 함수에서 반환될 때까지 실행을 계속합니다. 함수 안으로 단계 실행한 상태에서 "step out" 버튼을 누르면 함수가 반환될 때까지 실행이 계속됩니다.

브레이크포인트 설정 및 해제
: Lua 코드에 원하는 수만큼 브레이크포인트를 설정할 수 있습니다. 디버거가 연결된 상태로 게임을 실행하면 다음 브레이크포인트를 만났을 때 실행이 중지되고 추가 상호작용을 기다립니다.

  ![브레이크포인트 추가](images/debugging/add_breakpoint.png)

  브레이크포인트를 설정하거나 해제하려면 코드 에디터에서 줄 번호 바로 오른쪽 열을 클릭합니다. 메뉴에서 <kbd>Edit ▸ Toggle Breakpoint</kbd>를 선택할 수도 있습니다.

브레이크포인트 비활성화 및 활성화
: 브레이크포인트는 제거하지 않고 일시적으로 비활성화할 수 있습니다. 비활성화된 브레이크포인트는 실행 중에 무시되지만 언제든지 다시 활성화할 수 있습니다. 코드 에디터 gutter에서 브레이크포인트를 마우스 오른쪽 버튼으로 클릭한 다음 `Enabled` 체크박스를 토글합니다. 비활성화된 브레이크포인트는 비활성 상태임을 나타내기 위해 속이 빈 모양으로 표시됩니다.

  ![브레이크포인트 비활성화](images/debugging/disable_breakpoint.png)

조건부 브레이크포인트 설정
: 브레이크포인트가 트리거되려면 true로 평가되어야 하는 조건을 포함하도록 설정할 수 있습니다. 조건은 코드 실행 중 해당 줄에서 사용할 수 있는 로컬 변수에 액세스할 수 있습니다.

  ![브레이크포인트 편집](images/debugging/edit_breakpoint.png)

  브레이크포인트 조건을 편집하려면 코드 에디터에서 줄 번호 바로 오른쪽 열을 마우스 오른쪽 버튼으로 클릭하거나, 메뉴에서 <kbd>Edit ▸ Edit Breakpoint</kbd>를 선택합니다.

Lua 표현식 평가
: 게임이 일시 정지된 상태에서 *Call Stack*의 프레임을 선택하고 콘솔 하단에 Lua 표현식이나 문장을 입력한 다음 <kbd>Enter</kbd>를 누릅니다. 평가에는 선택한 프레임의 지역 변수, 업밸류, 전역 변수가 사용됩니다. 테이블 결과에는 중첩된 내용도 포함됩니다.

  ![콘솔](images/debugging/console.png)

  대입으로 값을 변경할 수도 있습니다. 예를 들어 `self`를 사용할 수 있는 프레임에서는 `self.score = 100`을 실행할 수 있습니다. 평가한 코드는 게임에서 실행한 코드와 마찬가지로 게임 상태에 영향을 줍니다.

변수 검사
: *Call Stack*에서 프레임을 선택하면 *Variables* 창에서 지역 변수와 업밸류를 검사할 수 있습니다. `_G`를 펼쳐 전역 변수를 확인하고, 테이블이나 `self`를 펼쳐 필드를 확인합니다. 에디터는 단계 실행, 프레임 전환, 평가 후 갱신 시 최신 값을 가져오면서 펼쳐진 경로, 선택 항목, 스크롤 위치를 유지합니다.

디버거 분리하기
: <kbd>Debug ▸ Detach Debugger</kbd>를 선택하면 게임에서 디버거의 연결을 해제합니다. 게임은 즉시 계속 실행됩니다. 게임을 다시 시작하지 않고 연결하려면 <kbd>Debug ▸ Start/Attach</kbd>를 사용하세요.

## 네이티브 DAP 연결 {#native-dap-connections}

엔진은 TCP를 통해 네이티브 Debug Adapter Protocol(DAP) 서버를 제공합니다. 외부 DAP 클라이언트를 사용하려면 네이티브 Defold 디버그 또는 헤드리스 엔진에서 리스너를 시작한 다음, 엔진의 주소와 포트로 클라이언트를 연결합니다. <kbd>Debug ▸ Start/Attach</kbd>를 사용하면 에디터가 리스너 설정을 자동으로 처리합니다.

현재 에디터는 MobDebug만 지원하는 이전 엔진에 연결할 수 없습니다. 현재 버전에는 `require "builtins.scripts.mobdebug"` 호출이 필요하지 않으며 사용할 수도 없습니다.

### 리스너 시작하기 {#starting-the-listener}

먼저 프로젝트를 빌드하세요. `build/default/game.projectc`가 있는 프로젝트 디렉토리에서 다음 [시작 설정 재정의](/manuals/project-settings/#setting-config-values-on-engine-startup)를 사용해 네이티브 디버그 엔진을 실행합니다:

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

DAP 클라이언트를 `127.0.0.1:8172`에 연결합니다. 엔진은 시작 스크립트를 실행하기 전에 클라이언트가 중단점을 설정할 때까지 기다립니다.

| 설정 | 기본값 | 용도 |
| --- | --- | --- |
| `debugger.enabled` | `0` | 엔진 시작 시 리스너를 시작하려면 `1`로 설정합니다. |
| `debugger.address` | `127.0.0.1` | 연결을 수신할 IPv4 주소입니다. 기본값은 같은 컴퓨터에서 오는 연결을 허용합니다. |
| `debugger.port` | `8172` | TCP 수신 포트입니다. 사용 가능한 포트를 선택하려면 `0`을 사용합니다. |
| `debugger.wait` | `0` | 시작 스크립트를 실행하기 전에 디버거 클라이언트의 설정을 기다리려면 `1`로 설정합니다. |

이 값들을 [game.project의 Debugger 섹션](/manuals/project-settings/#debugger)에 추가할 수도 있습니다. <kbd>Debug ▸ Start/Attach</kbd>에서는 에디터가 리스너를 자동으로 설정하므로 직접 리스너를 시작할 때만 수동 설정이 필요합니다.

엔진 로그에 선택된 주소와 포트가 표시됩니다. `debugger.wait=0`이면 게임이 즉시 시작되며 나중에 연결할 수 있습니다. `debugger.wait=1`이면 클라이언트가 중단점을 포함한 세션 설정을 마칠 때까지 기다립니다. 로컬 디버그 실행에서는 에디터가 사용 가능한 포트를 자동으로 선택합니다.

클라이언트 연결이 끊어지면 실행을 재개하고 리스너는 다음 연결을 받을 수 있는 상태로 유지됩니다. 시작 설정을 기다리는 중에 연결이 끊겨도 엔진은 실행을 재개합니다. 리스너를 시작할 수 없으면 엔진은 오류를 기록하고 시작을 계속합니다. Lua에서 `debugger.start(0)`을 호출해 사용 가능한 포트로 다시 시도할 수 있습니다.

### 실행 중 리스너 활성화하기 {#enabling-the-listener-while-running}

게임을 다시 시작하지 않고 스크립트에서 리스너를 활성화하려면:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])`는 수신 포트를 즉시 반환합니다. 클라이언트를 기다리거나 게임을 일시 정지하지 않습니다. 생략한 인자는 `debugger.port`와 `debugger.address`를 사용하며, `0`을 전달하면 사용 가능한 포트를 선택합니다. 반복 호출하면 기존 리스너의 포트를 반환하며 주소나 포트를 변경하지 않습니다. `debugger` 모듈은 네이티브 디버그 및 헤드리스 엔진에서 제공합니다.

포트는 `0`부터 `65535`까지의 정수여야 합니다. 주소만 재정의하려면 첫 번째 인자로 `nil`을 전달하세요. 잘못된 인자나 리스너 바인딩 실패는 Lua 오류를 발생시킵니다.

### 원격 타겟 {#remote-targets}

다른 컴퓨터에서 직접 연결하려면 리스너를 기기의 IPv4 인터페이스 또는 `0.0.0.0`(모든 IPv4 인터페이스)에 바인딩합니다. 예를 들어 `debugger.start(8172, "0.0.0.0")`을 사용하거나 위 시작 명령에 `--config=debugger.address=0.0.0.0`을 추가합니다. 클라이언트를 기기의 실제 IP 주소에 연결하고 수신 포트에 대한 TCP 액세스를 허용하세요. `0.0.0.0`은 바인딩 주소이며 클라이언트에 입력할 주소가 아닙니다.

Defold 에디터는 원격 바인딩을 자동으로 요청하고 원격 타겟에는 `8172 + project.instance_index` 포트를 사용합니다. 동적으로 선택된 원격 포트는 찾을 수 없습니다. 원격 리스너를 localhost나 다른 포트에서 이미 시작했다면 에디터에서 연결하기 전에 엔진을 다시 시작하세요.

디버거는 Lua를 평가할 수 있으며 인증 기능이 없습니다. 신뢰할 수 있는 개발 네트워크에서만 원격 액세스를 활성화하세요.

### 외부 클라이언트 {#external-clients}

TCP를 통해 DAP 서버에 직접 연결할 수 있는 클라이언트를 사용합니다. 소스 매핑을 `game.project`가 있는 폴더로 설정합니다(DAP의 `localRoot` 연결 인자). 먼저 엔진 리스너를 시작한 다음 클라이언트를 연결하세요.

#### VS Code {#vs-code}

[Lua Debug 익스텐션](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug)(`actboy168.lua-debug`)을 설치하고 VS Code에서 `game.project`가 있는 폴더를 연 다음, `.vscode/launch.json`에 다음 설정을 추가합니다:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

VS Code가 `.script`, `.gui_script`, `.render_script` 파일을 일반 텍스트로 열면 중단점을 설정하기 전에 상태 표시줄의 언어 표시에서 **Lua**를 선택하세요.

스크립트의 `init()` 함수 같은 곳에 중단점을 설정합니다. [위의 시작 명령](#starting-the-listener)으로 엔진을 시작한 다음 VS Code의 **Run and Debug** 창에서 **Attach to Defold Lua**를 선택합니다. `debugger.wait=1`이면 클라이언트가 중단점을 설정한 후에 엔진이 시작 스크립트를 실행합니다. 연결 후 다음 Lua 줄에서도 일시 정지하려면 `stopOnEntry`를 `true`로 설정하세요.

VS Code의 [`debugServer` 설정](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug)은 엔진의 로컬 TCP 리스너에 직접 연결합니다. `address` 필드는 Lua Debug 익스텐션의 연결 설정에 필요합니다. 리스너 포트를 변경하면 두 필드를 모두 갱신하세요. 클라이언트가 엔진의 Lua 소스 이름을 파일에 매핑할 수 있도록 `localRoot`는 프로젝트 폴더를 가리켜야 합니다.

원격 엔진의 경우 DAP 포트를 localhost로 포워딩하고 두 필드에 포워딩된 포트를 입력하거나, 원격 호스트에 직접 연결하는 DAP 클라이언트를 사용하세요.

## Breakpoints 탭

  ![Breakpoints 탭](images/debugging/breakpoints_tab.png)

  여러 스크립트에 걸쳐 여러 브레이크포인트를 작업할 때, Breakpoints 탭은 모든 브레이크포인트를 한곳에서 관리할 수 있는 통합된 뷰를 제공합니다.

##### 개별 브레이크포인트 컨트롤

  개별 브레이크포인트를 다룰 때:
  - 빨간 휴지통 아이콘을 클릭해 브레이크포인트를 제거합니다.
  - 행을 더블 클릭해(조건 영역 바깥) Code View의 해당 줄로 이동합니다.
  - 조건 셀을 더블 클릭하거나 펜 아이콘을 클릭해 조건부 브레이크포인트를 편집합니다.
  - 조건 셀 위에 마우스를 올렸을 때 나타나는 X clear 버튼을 클릭해 조건을 지웁니다.

##### 일괄 작업

  Ctrl/Cmd+click 또는 Shift+click을 사용해 여러 브레이크포인트를 선택한 다음 마우스 오른쪽 버튼을 클릭해 일괄 작업을 수행합니다. 여러 브레이크포인트의 조건을 동시에 편집하거나, 활성 상태를 토글하거나, 완전히 제거할 수 있습니다.

  툴바 버튼을 사용하면 모든 브레이크포인트를 한 번에 활성화, 비활성화 또는 토글할 수 있습니다. 게임을 멈추지 않고 실행하고 싶지만 브레이크포인트 위치는 잃고 싶지 않을 때 유용합니다. 디버깅 세션이 끝나면 모두 제거할 수도 있습니다.

## Lua debug 라이브러리

Lua에는 특정 상황에서 유용한 debug 라이브러리가 포함되어 있으며, 특히 Lua 환경의 내부를 검사해야 할 때 유용합니다. 자세한 내용은 [Lua 매뉴얼의 Debug Library 장](http://www.lua.org/pil/contents.html#23)에서 확인할 수 있습니다.

## 디버깅 체크리스트

에러가 발생하거나 게임이 예상대로 동작하지 않는다면 다음 디버깅 체크리스트를 확인하세요:

1. 콘솔 출력을 확인하고 런타임 에러가 없는지 검증합니다.

2. 코드에 `print` 문을 추가해 코드가 실제로 실행되는지 검증합니다.

3. 코드가 실행되지 않는다면, 코드 실행에 필요한 적절한 설정을 에디터에서 완료했는지 확인합니다. 스크립트가 올바른 게임 오브젝트에 추가되어 있나요? 스크립트가 입력 포커스를 획득했나요? input-triggers가 올바른가요? 쉐이더 코드가 메터리얼에 추가되었나요? 등입니다.

4. 코드가 변수 값에 의존한다면(예: if 문), 해당 값이 사용되거나 검사되는 위치에서 `print`로 출력하거나 디버거로 검사합니다.

버그를 찾는 일은 때로 어렵고 시간이 많이 걸릴 수 있습니다. 코드 조각을 하나씩 훑으며 모든 것을 확인하고, 문제가 있는 코드를 좁혀 가며 에러 원인을 제거해야 할 수 있습니다. 이 작업에는 "분할 정복(divide and conquer)"이라는 방법이 가장 좋습니다:

1. 버그를 포함할 수밖에 없는 코드의 절반(또는 그보다 더 작은 범위)을 파악합니다.
2. 다시 그 절반 중 버그를 포함할 수밖에 없는 절반을 파악합니다.
3. 버그를 찾을 때까지 버그를 일으킬 수밖에 없는 코드 범위를 계속 좁혀 갑니다.

성공적인 버그 찾기를 바랍니다!

## 물리 문제 디버깅 {#debugging-problems-with-physics}

물리에 문제가 있거나 충돌이 예상대로 동작하지 않는다면 물리 디버깅을 활성화하는 것을 권장합니다. *game.project* 파일의 *Physics* 섹션에서 *Debug* 체크박스를 선택합니다:

![물리 디버그 설정](images/debugging/physics_debug_setting.png)

이 체크박스가 활성화되면 Defold는 모든 충돌 모형과 충돌 접점을 그립니다:

![물리 디버그 시각화](images/debugging/physics_debug_visualisation.png)
