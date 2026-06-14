---
title: Defold의 게임패드 입력
brief: 이 매뉴얼은 게임패드 입력이 작동하는 방식을 설명합니다.
---

::: sidenote
Defold에서 입력이 작동하는 일반적인 방식, 입력을 수신하는 방법, 그리고 스크립트 파일에서 입력을 어떤 순서로 받는지 먼저 익히는 것이 좋습니다. 입력 시스템에 대한 자세한 내용은 [입력 개요 매뉴얼](/manuals/input)을 참고하세요.
:::

# 게임패드 {#gamepads}
게임패드 트리거를 사용하면 표준 게임패드 입력을 게임 함수에 바인딩할 수 있습니다. 게임패드 입력은 다음에 대한 바인딩을 제공합니다:

- 왼쪽 및 오른쪽 스틱(방향과 클릭)
- 왼쪽 및 오른쪽 디지털 패드. 오른쪽 패드는 일반적으로 Xbox 컨트롤러의 "A", "B", "X", "Y" 버튼과 Playstation 컨트롤러의 "square", "circle", "triangle", "cross" 버튼에 해당합니다.
- 왼쪽 및 오른쪽 트리거
- 왼쪽 및 오른쪽 숄더 버튼
- Start, Back 및 Guide 버튼

![](images/input/gamepad_bindings.png)

::: important
아래 예제는 위 이미지에 표시된 동작을 사용합니다. 모든 입력과 마찬가지로 입력 동작의 이름은 원하는 대로 자유롭게 지정할 수 있습니다.
:::

## 디지털 버튼 {#digital-buttons}
디지털 버튼은 `pressed`, `released`, `repeated` 이벤트를 생성합니다. 디지털 버튼의 입력(눌림 또는 해제)을 감지하는 예제입니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- 왼쪽으로 이동 시작
        elseif action.released then
            -- 왼쪽 이동 중지
        end
    end
end
```

## 아날로그 스틱 {#analog-sticks}
아날로그 스틱은 게임패드 설정 파일에 정의된 데드존 밖으로 스틱이 움직일 때 연속 입력 이벤트를 생성합니다(아래 참고). 아날로그 스틱의 입력을 감지하는 예제입니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- 왼쪽 스틱이 아래로 움직였습니다
        print(action.value) -- 0.0과 -1.0 사이의 값
    end
end
```

아날로그 스틱은 특정 임계값을 넘어서 상하좌우 방향으로 움직일 때 `pressed` 및 `released` 이벤트도 생성합니다. 따라서 아날로그 스틱을 디지털 방향 입력으로도 쉽게 사용할 수 있습니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- 왼쪽 스틱이 최대 아래쪽 위치로 움직였습니다
    end
end
```

## 여러 게임패드 {#multiple-gamepads}
Defold는 호스트 운영체제를 통해 여러 게임패드를 지원하며, 동작은 `action` 테이블의 `gamepad` 필드를 입력이 발생한 게임패드 번호로 설정합니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- 게임패드 0이 게임에 참가하려고 합니다
        end
    end
end
```

## 연결과 연결 해제 {#connect-and-disconnect}
게임패드 입력 바인딩은 게임패드가 연결되었는지(시작 시점부터 연결된 경우 포함) 또는 연결 해제되었는지를 감지하기 위해 `Connected`와 `Disconnected`라는 별도의 바인딩 두 개도 제공합니다.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- 게임패드 0이 연결되었습니다
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- 게임패드 0이 연결 해제되었습니다
        end
    end
end
```

## Raw 게임패드 {#raw-gamepads}

게임패드 입력 바인딩은 연결된 모든 게임패드의 필터링되지 않은(데드존이 적용되지 않은) 버튼, 축(axis), 햇(hat) 입력을 제공하기 위해 `Raw`라는 별도 바인딩도 제공합니다.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Gamepads 설정 파일 {#gamepads-settings-file}
게임패드 입력 설정은 하드웨어 게임패드 타입마다 별도의 매핑 파일을 사용합니다. 특정 하드웨어 게임패드의 게임패드 매핑은 *gamepads* 파일에서 설정합니다. Defold는 일반적인 게임패드 설정이 포함된 내장 gamepads 파일을 제공합니다:

![게임패드 설정](images/input/gamepads.png)

새 게임패드 설정 파일을 만들어야 한다면, 이를 도와주는 간단한 도구가 있습니다:

[gdc.zip 다운로드 클릭](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

이 파일에는 Windows, Linux, macOS용 바이너리가 포함되어 있습니다. 커맨드 라인에서 실행합니다:

```sh
./gdc
```

이 도구는 연결된 컨트롤러에서 여러 버튼을 누르라고 요청합니다. 그러면 컨트롤러에 맞는 올바른 매핑이 들어 있는 새 gamepads 파일을 출력합니다. 새 파일을 저장하거나 기존 gamepads 파일과 병합한 뒤, *game.project*의 설정을 업데이트합니다:

![게임패드 설정](images/input/gamepad_setting.png)

### 식별되지 않은 게임패드 {#unidentified-gamepads}

게임패드가 연결되었지만 해당 게임패드에 대한 매핑이 없으면, 게임패드는 "connected", "disconnected", "raw" 동작만 생성합니다. 이 경우 게임에서 원시 게임패드 데이터를 동작에 직접 매핑해야 합니다.

게임패드의 입력 동작이 알 수 없는 게임패드에서 온 것인지 여부는 `action`의 `gamepad_unknown` 값을 읽어 확인할 수 있습니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
```

## HTML5의 게임패드 {#gamepads-in-html5}
게임패드는 HTML5 빌드에서 지원되며 다른 플랫폼과 동일한 입력 이벤트를 생성합니다. 게임패드 지원은 대부분의 브라우저에서 지원되는 [Gamepad API](https://www.w3.org/TR/gamepad/)를 기반으로 합니다([지원 현황 표 참고](https://caniuse.com/?search=gamepad)). 브라우저가 Gamepad API를 지원하지 않으면 Defold는 프로젝트의 모든 Gamepad 트리거를 조용히 무시합니다. 브라우저가 Gamepad API를 지원하는지는 `navigator` 오브젝트에 `getGamepads` 함수가 있는지 확인하여 검사할 수 있습니다:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

게임이 `iframe` 안에서 실행 중이라면 `iframe`에 `gamepad` 권한도 추가되어 있는지 확인해야 합니다:

```html
<iframe allow="gamepad"></iframe>
```

### 표준 게임패드 {#standard-gamepad}

연결된 게임패드가 브라우저에서 표준 게임패드로 식별되면, [gamepads 설정 파일](/manuals/input-gamepads/#gamepads-settings-file)의 "Standard Gamepad" 매핑을 사용합니다(`Standard Gamepad` 매핑은 `/builtins`의 `default.gamepads` 파일에 포함되어 있습니다). 표준 게임패드는 PlayStation 또는 Xbox 컨트롤러와 비슷한 버튼 레이아웃을 가진 16개 버튼과 2개 아날로그 스틱으로 정의됩니다(자세한 내용은 [W3C 정의와 버튼 레이아웃](https://w3c.github.io/gamepad/#dfn-standard-gamepad)을 참고하세요). 연결된 게임패드가 표준 게임패드로 식별되지 않으면 Defold는 게임패드 설정 파일에서 하드웨어 게임패드 타입과 일치하는 매핑을 찾습니다.

## Windows의 게임패드 {#gamepads-on-windows}
Windows에서는 현재 XBox 360 컨트롤러만 지원됩니다. 360 컨트롤러를 Windows 머신에 연결하려면 [올바르게 설정되어 있는지 확인하세요](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Android의 게임패드 {#gamepads-on-android}

게임패드는 Android 빌드에서 지원되며 다른 플랫폼과 동일한 입력 이벤트를 생성합니다. 게임패드 지원은 [키 및 모션 이벤트용 Android 입력 시스템](https://developer.android.com/training/game-controllers/controller-input)을 기반으로 합니다. Android 입력 이벤트는 위에서 설명한 것과 같은 *gamepad* 파일을 사용하여 Defold 게임패드 이벤트로 변환됩니다.

Android에서 게임패드 바인딩을 추가할 때는 다음 조회 테이블을 사용하여 Android 입력 이벤트를 *gamepad* 파일 값으로 변환할 수 있습니다:

| Key event에서 버튼 인덱스로 | 인덱스 |
|-----------------------------|-------|
| `AKEYCODE_BUTTON_A`           | 0     |
| `AKEYCODE_BUTTON_B`           | 1     |
| `AKEYCODE_BUTTON_C`           | 2     |
| `AKEYCODE_BUTTON_X`           | 3     |
| `AKEYCODE_BUTTON_L1`          | 4     |
| `AKEYCODE_BUTTON_R1`          | 5     |
| `AKEYCODE_BUTTON_Y`           | 6     |
| `AKEYCODE_BUTTON_Z`           | 7     |
| `AKEYCODE_BUTTON_L2`          | 8     |
| `AKEYCODE_BUTTON_R2`          | 9     |
| `AKEYCODE_DPAD_CENTER`        | 10    |
| `AKEYCODE_DPAD_DOWN`          | 11    |
| `AKEYCODE_DPAD_LEFT`          | 12    |
| `AKEYCODE_DPAD_RIGHT`         | 13    |
| `AKEYCODE_DPAD_UP`            | 14    |
| `AKEYCODE_BUTTON_START`       | 15    |
| `AKEYCODE_BUTTON_SELECT`      | 16    |
| `AKEYCODE_BUTTON_THUMBL`      | 17    |
| `AKEYCODE_BUTTON_THUMBR`      | 18    |
| `AKEYCODE_BUTTON_MODE`        | 19    |
| `AKEYCODE_BUTTON_1`           | 20    |
| `AKEYCODE_BUTTON_2`           | 21    |
| `AKEYCODE_BUTTON_3`           | 22    |
| `AKEYCODE_BUTTON_4`           | 23    |
| `AKEYCODE_BUTTON_5`           | 24    |
| `AKEYCODE_BUTTON_6`           | 25    |
| `AKEYCODE_BUTTON_7`           | 26    |
| `AKEYCODE_BUTTON_8`           | 27    |
| `AKEYCODE_BUTTON_9`           | 28    |
| `AKEYCODE_BUTTON_10`          | 29    |
| `AKEYCODE_BUTTON_11`          | 30    |
| `AKEYCODE_BUTTON_12`          | 31    |
| `AKEYCODE_BUTTON_13`          | 32    |
| `AKEYCODE_BUTTON_14`          | 33    |
| `AKEYCODE_BUTTON_15`          | 34    |
| `AKEYCODE_BUTTON_16`          | 35    |

([Android `KeyEvent` 정의](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Motion event에서 축 인덱스로 | 인덱스 |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([Android `MotionEvent` 정의](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

이 조회 테이블을 Google Play Store의 게임패드 테스트 앱과 함께 사용하면 게임패드의 각 버튼이 어떤 key event에 매핑되는지 파악할 수 있습니다.
