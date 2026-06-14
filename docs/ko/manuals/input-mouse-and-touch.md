---
title: Defold의 마우스 및 터치 입력
brief: 이 매뉴얼은 마우스 및 터치 입력이 작동하는 방식을 설명합니다.
---

::: sidenote
Defold에서 입력이 작동하는 일반적인 방식, 입력을 받는 방법, 스크립트 파일에서 입력을 받는 순서를 먼저 익히는 것이 좋습니다. 입력 시스템에 대한 자세한 내용은 [입력 개요 매뉴얼](/manuals/input)을 참고하세요.
:::

# 마우스 트리거
마우스 트리거를 사용하면 마우스 버튼과 스크롤 휠의 입력을 게임 동작에 바인딩할 수 있습니다.

![](images/input/mouse_bindings.png)

::: sidenote
마우스 버튼 입력 `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT`, `MOUSE_BUTTON_MIDDLE`은 `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2`, `MOUSE_BUTTON_3`과 동일합니다.
:::

::: important
아래 예제는 위 이미지에 표시된 동작을 사용합니다. 모든 입력과 마찬가지로 입력 동작의 이름은 원하는 방식으로 자유롭게 지정할 수 있습니다.
:::

## 마우스 버튼
마우스 버튼은 `pressed`, `released`, `repeated` 이벤트를 생성합니다. 다음은 마우스 왼쪽 버튼의 입력(눌림 또는 해제)을 감지하는 예입니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- 마우스 왼쪽 버튼이 눌림
        elseif action.released then
            -- 마우스 왼쪽 버튼이 해제됨
        end
    end
end
```

::: important
`MOUSE_BUTTON_LEFT`(또는 `MOUSE_BUTTON_1`) 입력 동작은 단일 터치 입력에도 전송됩니다.
:::

## 마우스 휠
마우스 휠 입력은 스크롤 동작을 감지합니다. 휠을 스크롤하면 `action.value` 필드가 `1`이고, 그렇지 않으면 `0`입니다. (스크롤 동작은 버튼 누름처럼 처리됩니다. Defold는 현재 터치패드의 세밀한 스크롤 입력을 지원하지 않습니다.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- 마우스 휠을 위로 스크롤함
        end
    end
end
```

## 마우스 움직임
마우스 움직임은 별도로 처리됩니다. 입력 바인딩에 마우스 트리거가 하나 이상 설정되어 있지 않으면 마우스 움직임 이벤트를 받을 수 없습니다.

마우스 움직임은 입력 바인딩에 바인딩되지 않지만 `action_id`는 `nil`로 설정되고 `action` 테이블에는 마우스 위치의 좌표와 델타 이동값이 채워집니다.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- 게임 오브젝트가 마우스/터치 움직임을 따라가게 함
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# 터치 트리거
Single-touch 및 Multi-touch 타입 트리거는 네이티브 어플리케이션의 iOS 및 Android 장치와 HTML5 번들에서 사용할 수 있습니다.

![](images/input/touch_bindings.png)

## Single-touch
Single-touch 타입 트리거는 입력 바인딩의 Touch Triggers 섹션에서 설정하지 않습니다. 대신 **`MOUSE_BUTTON_LEFT` 또는 `MOUSE_BUTTON_1`의 마우스 버튼 입력을 설정하면 single-touch 트리거가 자동으로 설정됩니다**.

## Multi-touch
Multi-touch 타입 트리거는 action 테이블 안의 `touch`라는 테이블을 채웁니다. 이 테이블의 요소는 `1`--`N` 숫자로 정수 인덱싱되며, 여기서 `N`은 터치 지점의 수입니다. 테이블의 각 요소에는 입력 데이터 필드가 포함됩니다:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- 각 터치 지점에 스폰
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Multi-touch에는 `MOUSE_BUTTON_LEFT` 또는 `MOUSE_BUTTON_1`의 마우스 버튼 입력과 같은 동작을 할당하면 안 됩니다. 같은 동작을 할당하면 사실상 single-touch를 덮어써서 어떤 single-touch 이벤트도 받을 수 없게 됩니다.
:::

::: sidenote
[Defold-Input asset](https://defold.com/assets/defoldinput/)을 사용하면 multi touch를 지원하는 버튼이나 아날로그 스틱 같은 가상 화면 컨트롤을 쉽게 설정할 수 있습니다.
:::


## 오브젝트의 클릭 또는 탭 감지
사용자가 비주얼 컴포넌트를 클릭하거나 탭했는지 감지하는 것은 많은 게임에서 필요한 매우 일반적인 작업입니다. 버튼이나 다른 UI 요소와의 사용자 상호작용일 수도 있고, 전략 게임에서 플레이어가 조종하는 유닛, 던전 크롤러 레벨의 보물, RPG의 퀘스트 제공자 같은 게임 오브젝트와의 상호작용일 수도 있습니다. 사용할 접근 방식은 비주얼 컴포넌트의 타입에 따라 달라집니다.

### GUI 노드와의 상호작용 감지
UI 요소에는 지정한 좌표가 GUI 노드의 범위 안에 있는지에 따라 `true` 또는 `false`를 반환하는 `gui.pick_node(node, x, y)` 함수가 있습니다. 자세한 내용은 [API docs](/ref/gui/#gui.pick_node:node-x-y), [pointer over example](/examples/gui/pointer_over/) 또는 [button example](/examples/gui/button/)을 참고하세요.

### 게임 오브젝트와의 상호작용 감지
게임 오브젝트의 경우 카메라 변환이나 렌더 스크립트 투영 같은 요소가 필요한 계산에 영향을 주기 때문에 상호작용 감지가 더 복잡합니다. 게임 오브젝트와의 상호작용을 감지하는 일반적인 접근 방식은 두 가지입니다:

  1. 사용자가 상호작용할 수 있는 게임 오브젝트의 위치와 크기를 추적하고, 마우스 또는 터치 좌표가 오브젝트 중 하나의 범위 안에 있는지 확인합니다.
  2. 사용자가 상호작용할 수 있는 게임 오브젝트에 충돌 오브젝트를 붙이고, 마우스나 손가락을 따라가는 충돌 오브젝트 하나를 추가한 뒤 이들 사이의 충돌을 확인합니다.

::: sidenote
드래그와 클릭 지원을 포함해 충돌 오브젝트로 사용자 입력을 감지하는 바로 사용할 수 있는 솔루션은 [Defold-Input asset](https://defold.com/assets/defoldinput/)에서 찾을 수 있습니다.
:::

두 경우 모두 마우스 또는 터치 이벤트의 화면 공간 좌표와 게임 오브젝트의 월드 공간 좌표 사이를 변환해야 합니다. 이 작업은 몇 가지 다른 방법으로 수행할 수 있습니다:

  * 렌더 스크립트가 사용하는 뷰와 투영을 직접 추적하고, 이를 사용해 월드 공간으로 또는 월드 공간에서 변환합니다. 예시는 [카메라 매뉴얼](/manuals/camera/#converting-mouse-to-world-coordinates)을 참고하세요.
  * [타사 카메라 솔루션](/manuals/camera/#third-party-camera-solutions)을 사용하고 제공되는 화면-월드 변환 함수를 활용합니다.
