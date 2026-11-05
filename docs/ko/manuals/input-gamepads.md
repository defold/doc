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

게임패드 매핑은 컨트롤러의 버튼, 축, 햇을 입력 바인딩에서 사용하는 표준 컨트롤로 변환합니다. Defold는 *game.project*의 *Input* 섹션에 설정된 두 매핑 소스를 결합합니다:

| 설정 | 매핑 포멧 | 기본값 |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | 컨트롤러 GUID로 일치시키는 SDL 포멧 텍스트 데이터베이스 | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | 기기 이름과 플랫폼에 대한 레거시 `.gamepads` 항목 | `/builtins/input/default.gamepads` |

SDL 데이터베이스 매핑과 자동 플랫폼 매핑은 [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone)을 사용합니다. 레거시 `.gamepads` 항목은 자체 데드존을 정의합니다. Android에서는 데이터베이스 항목이 없는 컨트롤러에도 [자동 매핑](#gamepads-on-android)이 적용될 수 있습니다.

### 레거시 .gamepads 매핑 {#legacy-gamepads-mappings}

하나의 `.gamepads` 파일에 여러 컨트롤러의 매핑을 넣을 수 있습니다. 기존 레거시 매핑도 계속 지원합니다. Defold는 기본 파일에 일반적인 컨트롤러의 매핑을 포함합니다:

![게임패드 설정](images/input/gamepads.png)

데스크톱 플랫폼에서 레거시 `.gamepads` 매핑을 만들어야 한다면 다음 도구가 도움이 됩니다. Android는 [Android 게임패드](#gamepads-on-android)를 참고하세요.

[gdc.zip 다운로드 클릭](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

이 파일에는 Windows, Linux, macOS용 바이너리가 포함되어 있습니다. 커맨드 라인에서 실행합니다:

```sh
./gdc
```

이 도구는 연결된 컨트롤러에서 여러 버튼을 누르라고 요청합니다. 그러면 컨트롤러에 맞는 올바른 매핑이 들어 있는 새 gamepads 파일을 출력합니다. 새 파일을 저장하거나 기존 gamepads 파일과 병합한 뒤, *game.project*의 설정을 업데이트합니다:

![게임패드 설정](images/input/gamepad_setting.png)

### 식별되지 않은 게임패드 {#unidentified-gamepads}

설정된 매핑도 자동 플랫폼 매핑도 사용할 수 없으면 게임패드는 `Connected`, `Disconnected`, `Raw`에 바인딩된 동작만 생성합니다. 컨트롤러 매핑을 추가하거나 게임에서 원시 입력을 처리할 수 있습니다.

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

연결된 게임패드가 브라우저에서 표준 게임패드로 식별되면, [gamepads 설정 파일](/manuals/input-gamepads/#gamepads-settings-file)의 `Standard Gamepad` 매핑을 사용합니다(`Standard Gamepad` 매핑은 `/builtins`의 `default.gamepads` 파일에 포함되어 있습니다). 표준 게임패드는 PlayStation 또는 Xbox 컨트롤러와 비슷한 버튼 레이아웃을 가진 16개 버튼과 2개 아날로그 스틱으로 정의됩니다(자세한 내용은 [W3C 정의와 버튼 레이아웃](https://w3c.github.io/gamepad/#dfn-standard-gamepad)을 참고하세요). 연결된 게임패드가 표준 게임패드로 식별되지 않으면 Defold는 게임패드 설정 파일에서 하드웨어 게임패드 타입과 일치하는 매핑을 찾습니다.

## Windows의 게임패드 {#gamepads-on-windows}
Windows에서는 현재 XBox 360 컨트롤러만 지원됩니다. 360 컨트롤러를 Windows 머신에 연결하려면 [올바르게 설정되어 있는지 확인하세요](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Android의 게임패드 {#gamepads-on-android}

Android 빌드는 게임패드를 지원하며 다른 플랫폼과 같은 입력 동작을 생성합니다. Defold는 설정된 [게임패드 매핑](#gamepads-settings-file)을 사용하고, 일치하는 항목이 없는 일부 컨트롤러는 자동으로 매핑할 수 있습니다.

컨트롤러를 식별할 수 없거나 컨트롤이 잘못 동작하면 Android 기기에서 테스트하고 매핑을 추가하거나 갱신하세요. 문제 해결은 [식별되지 않은 게임패드](#unidentified-gamepads)와 [원시 게임패드](#raw-gamepads)를 참고하세요.
