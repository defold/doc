---
title: Defold의 충돌 이벤트
brief: "`physics.set_event_listener()`를 사용해 모든 충돌 및 상호작용 메세지를 지정한 단일 함수로 전달하면 충돌 이벤트 처리를 중앙화할 수 있습니다."
---

# Defold 물리 이벤트 처리

Defold는 `physics.set_event_listener()` 함수를 통해 중앙화된 물리 이벤트 처리를 제공합니다. 이 함수를 사용하면 모든 물리 상호작용 이벤트를 한곳에서 처리하는 커스텀 리스너를 설정할 수 있으므로, 코드를 간결하게 만들고 효율을 높일 수 있습니다.

## 물리 월드 리스너 설정

Defold에서는 각 컬렉션 프록시(Collection proxy)가 별도의 물리 월드를 만듭니다. 따라서 여러 컬렉션 프록시를 사용할 때는 각각에 연결된 별도의 물리 월드를 관리해야 합니다. 각 월드에서 물리 이벤트가 올바르게 처리되도록 하려면 각 컬렉션 프록시의 월드마다 물리 월드 리스너를 따로 설정해야 합니다.

이 설정은 프록시가 나타내는 컬렉션의 컨텍스트 안에서 물리 이벤트 리스너를 설정해야 한다는 뜻입니다. 이렇게 하면 리스너가 관련 물리 월드와 직접 연결되어 물리 이벤트를 정확하게 처리할 수 있습니다.

다음은 컬렉션 프록시 안에서 물리 월드 리스너를 설정하는 예입니다:

```lua
function init(self)
    -- 이 스크립트가 프록시에서 로드한 컬렉션 안의 게임 오브젝트에 연결되어 있다고 가정합니다
    -- 이 컬렉션 프록시의 물리 월드에 대한 물리 월드 리스너를 설정합니다
    physics.set_event_listener(physics_world_listener)
end
```

이 방법을 구현하면 컬렉션 프록시가 생성한 각 물리 월드에 전용 리스너가 있게 됩니다. 이는 여러 컬렉션 프록시를 사용하는 프로젝트에서 물리 이벤트를 효과적으로 처리하는 데 중요합니다.

::: important
리스너가 설정되면 이 리스너가 설정된 물리 월드에서는 [물리 메세지](/manuals/physics-messages)가 더 이상 전송되지 않습니다.
:::

## 이벤트 데이터 구조

각 물리 이벤트는 해당 이벤트와 관련된 특정 정보를 담은 `data` 테이블을 제공합니다.

1. **접촉점 이벤트 (`contact_point_event`):**
이 이벤트는 두 충돌 오브젝트 사이의 접촉점을 보고합니다. 충격력 계산이나 커스텀 충돌 응답처럼 세부적인 충돌 처리를 할 때 유용합니다.

   - `applied_impulse`: 접촉으로 발생한 임펄스입니다.
   - `distance`: 오브젝트 사이의 침투 거리입니다.
   - `a` 및 `b`: 충돌하는 엔티티를 나타내는 오브젝트이며, 각각 다음 항목을 포함합니다:
     - `position`: 접촉점의 월드 위치(vector3)입니다.
     - `instance_position`: 게임 오브젝트 인스턴스의 월드 위치(vector3)입니다.
     - `id`: 인스턴스 ID(hash)입니다.
     - `group`: 충돌 그룹(hash)입니다.
     - `relative_velocity`: 다른 오브젝트에 대한 상대 속도(vector3)입니다.
     - `mass`: 킬로그램 단위의 질량(number)입니다.
     - `normal`: 다른 오브젝트에서부터 향하는 접촉 노멀(vector3)입니다.

2. **충돌 이벤트 (`collision_event`):**
이 이벤트는 두 오브젝트 사이에 충돌이 발생했음을 나타냅니다. 접촉점 이벤트에 비해 더 일반화된 이벤트이며, 접촉점에 대한 자세한 정보 없이 충돌을 감지하는 데 적합합니다.

   - `a` 및 `b`: 충돌하는 엔티티를 나타내는 오브젝트이며, 각각 다음 항목을 포함합니다:
     - `position`: 월드 위치(vector3)입니다.
     - `id`: 인스턴스 ID(hash)입니다.
     - `group`: 충돌 그룹(hash)입니다.

3. **트리거 이벤트 (`trigger_event`):**
이 이벤트는 오브젝트가 트리거 오브젝트와 상호작용할 때 전송됩니다. 오브젝트가 들어오거나 나갈 때 어떤 일이 일어나게 하는 게임 내 영역을 만들 때 유용합니다.

   - `enter`: 상호작용이 진입(true)인지 이탈(false)인지를 나타냅니다.
   - `a` 및 `b`: 트리거 이벤트에 관여한 오브젝트이며, 각각 다음 항목을 포함합니다:
     - `id`: 인스턴스 ID(hash)입니다.
     - `group`: 충돌 그룹(hash)입니다.

4. **레이 캐스트 응답 (`ray_cast_response`):**
이 이벤트는 레이 캐스트에 대한 응답으로 전송되며, 레이가 맞힌 오브젝트에 대한 정보를 제공합니다.

   - `group`: 맞은 오브젝트의 충돌 그룹(hash)입니다.
   - `request_id`: 레이 캐스트 요청의 식별자(number)입니다.
   - `position`: 맞은 위치(vector3)입니다.
   - `fraction`: 레이 길이 중 맞은 지점이 발생한 비율(number)입니다.
   - `normal`: 맞은 위치의 노멀(vector3)입니다.
   - `id`: 맞은 오브젝트의 인스턴스 ID(hash)입니다.

5. **레이 캐스트 빗나감 (`ray_cast_missed`):**
이 이벤트는 레이 캐스트가 어떤 오브젝트도 맞히지 않았을 때 전송됩니다.

   - `request_id`: 빗나간 레이 캐스트 요청의 식별자(number)입니다.

## 사용 예

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- 세부 접촉점 데이터를 처리합니다
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- 일반 충돌 데이터를 처리합니다
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- 트리거 상호작용 데이터를 처리합니다
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- 레이 캐스트가 맞은 데이터를 처리합니다
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- 레이 캐스트가 빗나간 데이터를 처리합니다
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## 제한 사항

리스너는 이벤트가 발생하는 순간 동기적으로 호출됩니다. 이는 타임스텝 중간에 발생하므로 물리 월드가 잠겨 있다는 뜻입니다. 따라서 `physics.create_joint()`처럼 물리 월드 시뮬레이션에 영향을 줄 수 있는 함수는 사용할 수 없습니다.

다음은 이러한 제한을 피하는 작은 예입니다:
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- `physics.create_joint()`에 전달해야 하는 인자와 같은 방식으로 메세지를 채웁니다
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- 오브젝트 자신에게 메세지를 보냅니다
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- 함수 인자가 담긴 메세지를 언팩합니다
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
