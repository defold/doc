---
title: Defold의 충돌 메세지
brief: 두 오브젝트가 충돌하면 엔진은 이벤트 콜백을 호출하거나 메세지를 브로드캐스트합니다.
---

# 충돌 메세지

두 오브젝트가 충돌하면 엔진은 이벤트 콜백에 이벤트를 보내거나 두 오브젝트 모두에 메세지를 브로드캐스트합니다.

## 이벤트 필터링

생성되는 이벤트의 타입은 각 오브젝트의 플래그로 제어할 수 있습니다:

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

기본적으로 이 값들은 모두 `true`입니다.
두 충돌 오브젝트가 상호작용할 때, 해당 체크박스 상태에 따라 사용자에게 메세지를 보내야 하는지 확인합니다.

예를 들어 "Generate Contact Events" 체크박스가 다음과 같을 때:

`physics.set_event_listener()`를 사용하는 경우:

| 컴포넌트 A | 컴포넌트 B | 메세지 전송 |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | 예          |
| ❌          | ✅︎          | 예          |
| ✅︎          | ❌          | 예          |
| ❌          | ❌          | 아니요       |

기본 메세지 핸들러를 사용하는 경우:

| 컴포넌트 A | 컴포넌트 B | 메세지 전송       |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | 예 (A,B) + (B,A) |
| ❌          | ✅︎          | 예 (B,A)         |
| ✅︎          | ❌          | 예 (A,B)         |
| ❌          | ❌          | 아니요            |

## 충돌 응답

충돌하는 오브젝트 중 하나가 "dynamic", "kinematic" 또는 "static" 타입이면 `"collision_response"` 메세지가 전송됩니다. 이 메세지에는 다음 필드가 설정됩니다:

`other_id`
: 충돌 오브젝트가 충돌한 인스턴스의 id입니다(`hash`).

`other_position`
: 충돌 오브젝트가 충돌한 인스턴스의 월드 위치입니다(`vector3`).

`other_group`
: 다른 충돌 오브젝트의 충돌 그룹입니다(`hash`).

`own_group`
: 충돌 오브젝트의 충돌 그룹입니다(`hash`).

`collision_response` 메세지는 오브젝트의 실제 교차에 대한 세부 정보가 필요 없는 충돌을 해결하는 경우에만 적합합니다. 예를 들어 총알이 적에게 맞았는지 감지하려는 경우입니다. 충돌하는 오브젝트 쌍마다 프레임당 이 메세지는 하나만 전송됩니다.

```Lua
function on_message(self, message_id, message, sender)
    -- 메세지 확인
    if message_id == hash("collision_response") then
        -- 동작 수행
        print("I collided with", message.other_id)
    end
end
```

## 접촉점 응답

충돌하는 오브젝트 중 하나가 "dynamic" 또는 "kinematic" 타입이고, 다른 하나가 "dynamic", "kinematic" 또는 "static" 타입이면 `"contact_point_response"` 메세지가 전송됩니다. 이 메세지에는 다음 필드가 설정됩니다:

`position`
: 접촉점의 월드 위치입니다(`vector3`).

`normal`
: 접촉점의 월드 공간 법선으로, 다른 오브젝트에서 현재 오브젝트 방향을 가리킵니다(`vector3`).

`relative_velocity`
: 다른 오브젝트에서 관찰한 충돌 오브젝트의 상대 속도입니다(`vector3`).

`distance`
: 오브젝트 사이의 관통 거리입니다. 음수가 아닙니다(`number`).

`applied_impulse`
: 접촉으로 인해 발생한 충격량입니다(`number`).

`life_time`
: (*현재 사용되지 않음!*) 접촉의 수명입니다(`number`).

`mass`
: 현재 충돌 오브젝트의 질량(kg)입니다(`number`).

`other_mass`
: 다른 충돌 오브젝트의 질량(kg)입니다(`number`).

`other_id`
: 충돌 오브젝트가 접촉한 인스턴스의 id입니다(`hash`).

`other_position`
: 다른 충돌 오브젝트의 월드 위치입니다(`vector3`).

`other_group`
: 다른 충돌 오브젝트의 충돌 그룹입니다(`hash`).

`own_group`
: 충돌 오브젝트의 충돌 그룹입니다(`hash`).

오브젝트를 정확히 분리해야 하는 게임이나 어플리케이션에서는 `"contact_point_response"` 메세지가 필요한 모든 정보를 제공합니다. 그러나 주어진 충돌 쌍마다 충돌의 특성에 따라 매 프레임 여러 개의 `"contact_point_response"` 메세지를 받을 수 있다는 점에 유의하세요. 자세한 내용은 [충돌 해결](/manuals/physics-resolving-collisions)을 참고하세요.

```Lua
function on_message(self, message_id, message, sender)
    -- 메세지 확인
    if message_id == hash("contact_point_response") then
        -- 동작 수행
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## 트리거 응답

충돌하는 오브젝트 중 하나가 "trigger" 타입이면 `"trigger_response"`  메세지가 전송됩니다. 메세지는 충돌이 처음 감지될 때 한 번, 그리고 오브젝트가 더 이상 충돌하지 않을 때 한 번 더 전송됩니다. 이 메세지에는 다음 필드가 있습니다:

`other_id`
: 충돌 오브젝트가 충돌한 인스턴스의 id입니다(`hash`).

`enter`
: 상호작용이 트리거에 진입한 경우 `true`, 빠져나간 경우 `false`입니다(`boolean`).

`other_group`
: 다른 충돌 오브젝트의 충돌 그룹입니다(`hash`).

`own_group`
: 충돌 오브젝트의 충돌 그룹입니다(`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- 메세지 확인
    if message_id == hash("trigger_response") then
        if message.enter then
            -- 진입 동작 수행
            print("I am now inside", message.other_id)
        else
            -- 이탈 동작 수행
            print("I am now outside", message.other_id)
        end
    end
end
```
