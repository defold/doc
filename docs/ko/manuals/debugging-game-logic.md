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

디버거를 실행하려면 <kbd>Debug ▸ Start/Attach</kbd>를 선택합니다. 그러면 디버거가 연결된 상태로 게임이 시작되거나, 이미 실행 중인 게임에 디버거가 연결됩니다.

![개요](images/debugging/overview.png)

디버거가 연결되면 콘솔의 디버거 제어 버튼이나 <kbd>Debug</kbd> 메뉴를 통해 게임 실행을 제어할 수 있습니다:

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  게임 실행을 즉시 중단합니다. 게임은 현재 지점에서 중단됩니다. 이제 게임 상태를 검사하거나, 게임을 단계별로 진행하거나, 다음 브레이크포인트까지 계속 실행할 수 있습니다. 현재 실행 지점은 코드 에디터에 표시됩니다.

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
Lua 코드 한 줄이 하나의 표현식에 대응되는 것은 아닙니다. 디버거에서 단계 실행은 한 번에 하나의 표현식씩 앞으로 이동하므로, 현재는 다음 줄로 진행하려면 step 버튼을 두 번 이상 눌러야 할 수 있습니다.
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
: 디버거가 연결되어 있고 게임이 브레이크포인트에서 중지된 상태에서는 현재 컨텍스트를 가진 Lua 런타임을 사용할 수 있습니다. 콘솔 하단에 Lua 표현식을 입력하고 <kbd>Enter</kbd>를 눌러 평가합니다:

  ![콘솔](images/debugging/console.png)

  현재 평가기를 통해서는 변수를 수정할 수 없습니다.

디버거 분리하기
: <kbd>Debug ▸ Detach Debugger</kbd>를 선택해 게임에서 디버거를 분리합니다. 게임은 즉시 계속 실행됩니다.

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

## 물리 문제 디버깅

물리에 문제가 있거나 충돌이 예상대로 동작하지 않는다면 물리 디버깅을 활성화하는 것을 권장합니다. *game.project* 파일의 *Physics* 섹션에서 *Debug* 체크박스를 선택합니다:

![물리 디버그 설정](images/debugging/physics_debug_setting.png)

이 체크박스가 활성화되면 Defold는 모든 충돌 모형과 충돌 접점을 그립니다:

![물리 디버그 시각화](images/debugging/physics_debug_visualisation.png)
