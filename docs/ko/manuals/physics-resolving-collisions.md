---
title: Defold에서 Kinematic 충돌 해결하기
brief: 이 매뉴얼은 Kinematic 물리 충돌을 해결하는 방법을 설명합니다.
---

# Kinematic 충돌 해결하기

Kinematic 충돌 오브젝트를 사용하면 충돌을 직접 해결하고 그 반응으로 오브젝트를 이동해야 합니다. 충돌 중인 두 오브젝트를 분리하는 단순한 구현은 다음과 같습니다:

```lua
function on_message(self, message_id, message, sender)
  -- 충돌 처리
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

이 코드는 Kinematic 오브젝트가 침투한 다른 물리 오브젝트로부터 Kinematic 오브젝트를 분리하지만, 분리가 필요 이상으로 커지는 경우가 많아 여러 상황에서 떨림이 보일 수 있습니다. 문제를 더 잘 이해하기 위해 플레이어 캐릭터가 두 오브젝트 *A*와 *B*에 충돌한 다음 상황을 생각해 보겠습니다:

![물리 충돌](images/physics/collision_multi.png)

물리 엔진은 충돌이 발생한 프레임에 여러 `"contact_point_response"` 메세지를 보냅니다. 하나는 오브젝트 *A*에 대한 것이고, 하나는 오브젝트 *B*에 대한 것입니다. 위의 단순한 코드처럼 각 침투에 반응해 캐릭터를 이동하면 결과 분리는 다음과 같습니다:

- 오브젝트 *A*의 침투 거리(검은색 화살표)에 따라 캐릭터를 오브젝트 *A* 밖으로 이동합니다.
- 오브젝트 *B*의 침투 거리(검은색 화살표)에 따라 캐릭터를 오브젝트 *B* 밖으로 이동합니다.

이 순서는 임의적이지만 어느 쪽이든 결과는 같습니다. 전체 분리는 *각 침투 벡터의 합*이 됩니다:

![단순한 물리 분리](images/physics/separation_naive.png)

오브젝트 *A*와 *B*로부터 캐릭터를 올바르게 분리하려면 각 접촉점의 침투 거리를 처리하고, 이전 분리가 이미 전체 또는 일부 분리를 해결했는지 확인해야 합니다.

첫 번째 접촉점 메세지가 오브젝트 *A*에서 오고, *A*의 침투 벡터만큼 캐릭터를 밖으로 이동한다고 가정해 보겠습니다:

![물리 분리 1단계](images/physics/separation_step1.png)

그러면 캐릭터는 이미 *B*로부터 부분적으로 분리된 상태입니다. 오브젝트 *B*로부터 완전히 분리하기 위해 최종적으로 필요한 보정은 위의 검은색 화살표로 표시되어 있습니다. 보정 벡터의 길이는 *A*의 침투 벡터를 *B*의 침투 벡터에 투영해서 계산할 수 있습니다:

![투영](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

보정 벡터는 *B*의 길이에서 *l*을 줄여 구할 수 있습니다. 임의 개수의 침투에 대해 이를 계산하려면, 길이가 0인 보정 벡터에서 시작해 각 접촉점마다 필요한 보정을 벡터에 누적하면 됩니다:

1. 현재 보정을 접촉점의 침투 벡터에 투영합니다.
2. 침투 벡터에서 남은 보정이 얼마인지 계산합니다(위 공식 기준).
3. 보정 벡터만큼 오브젝트를 이동합니다.
4. 누적된 보정에 이 보정을 더합니다.

전체 구현은 다음과 같습니다:

```lua
function init(self)
  -- 보정 벡터
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- 보정 초기화
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- 충돌 처리
  if message_id == hash("contact_point_response") then
    -- 충돌에서 벗어나기 위해 필요한 정보를 가져옵니다. 여러
    -- 접촉점이 반환될 수 있으므로 이 프레임의 보정 벡터를
    -- 누적해 접촉점 전체에서 어떻게 벗어날지 계산해야 합니다:
    if message.distance > 0 then
      -- 먼저 누적된 보정을 침투 벡터에 투영합니다
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- 초과하지 않는 투영만 고려합니다.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- 보정 적용
        go.set_position(go.get_position() + comp)
        -- 완료된 보정 누적
        self.correction = self.correction + comp
      end
    end
  end
end
```
