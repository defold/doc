---
title: Defold의 키 및 텍스트 입력
brief: 이 매뉴얼은 키 및 텍스트 입력이 작동하는 방식을 설명합니다.
---

::: sidenote
Defold에서 입력이 작동하는 일반적인 방식, 입력을 수신하는 방법, 스크립트 파일에서 입력이 어떤 순서로 수신되는지 먼저 익혀 두는 것을 권장합니다. 입력 시스템에 대한 자세한 내용은 [입력 개요 매뉴얼](/manuals/input)을 참고하세요.
:::

# 키 트리거
키 트리거는 단일 키 키보드 입력을 게임 동작에 바인딩할 수 있게 해줍니다. 각 키는 대응하는 동작에 개별적으로 매핑됩니다. 키 트리거는 화살표 키나 WASD 키로 캐릭터를 이동하는 것처럼 특정 버튼을 특정 함수에 연결할 때 사용합니다. 임의의 키보드 입력을 읽어야 한다면 텍스트 트리거(아래 참고)를 사용하세요.

![](images/input/key_bindings.png)

```lua
function on_input(self, action_id, action)
    if action_id == hash("left") then
        if action.pressed then
            -- 왼쪽으로 이동 시작
        elseif action.released then
            -- 왼쪽으로 이동 중지
        end
    end
end
```

# 텍스트 트리거
텍스트 트리거는 임의의 텍스트 입력을 읽을 때 사용합니다. 텍스트 트리거에는 `text`와 `marked-text` 두 가지 타입이 있습니다.

![](images/input/text_bindings.png)

## 텍스트
`text`는 일반 텍스트 입력을 캡쳐합니다. 입력한 문자가 포함된 문자열로 action 테이블의 `text` 필드를 설정합니다. 동작은 버튼을 누르는 순간에만 발생하며, `release`나 `repeated` 동작은 전송되지 않습니다.

```lua
function on_input(self, action_id, action)
    if action_id == hash("text") then
        -- 입력한 문자를 "user" 노드의 텍스트에 이어 붙입니다...
        local node = gui.get_node("user")
        local name = gui.get_text(node)
        name = name .. action.text
        gui.set_text(node, name)
    end
end
```

## 조합 중인 텍스트
`marked-text`는 여러 번의 키 입력이 하나의 입력으로 매핑될 수 있는 아시아권 키보드에서 주로 사용합니다. 예를 들어 iOS "Japanese-Kana" 키보드에서는 사용자가 조합을 입력할 수 있고, 키보드 상단에 입력 가능한 기호나 기호 시퀀스가 표시됩니다.

![조합 중인 텍스트 입력](images/input/marked_text.png)

- 각 키 입력은 별도의 동작을 생성하고, 동작의 `text` 필드를 현재 입력 중인 기호 시퀀스(조합 중인 텍스트)로 설정합니다.
- 사용자가 기호 또는 기호 조합을 선택하면, 입력 바인딩 목록에 해당 항목이 설정되어 있는 경우 별도의 `text` 타입 트리거 동작이 전송됩니다. 이 별도 동작은 동작의 `text` 필드를 최종 기호 시퀀스로 설정합니다.
