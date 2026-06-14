---
title: Defold의 레이 캐스트
brief: 레이 캐스트는 선형 광선을 따라 물리 월드를 읽는 데 사용됩니다. 이 매뉴얼은 그 동작 방식을 설명합니다.
---

## 레이 캐스트

레이 캐스트는 선형 광선을 따라 물리 월드를 읽는 데 사용됩니다. 물리 월드에 광선을 캐스트하려면 시작 위치와 끝 위치, 그리고 테스트할 [충돌 그룹 집합](/manuals/physics-groups)을 제공합니다.

광선이 물리 오브젝트에 닿으면 닿은 오브젝트에 대한 정보를 얻습니다. 광선은 다이나믹, 키네마틱, 정적 오브젝트와 교차합니다. 트리거와는 상호작용하지 않습니다.

```lua
function update(self, dt)
  -- 레이 캐스트 요청
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
      -- 히트 처리(모든 값은 'ray_cast_response' 메세지 참고)
      print(result.id)
  end
end
```

::: sidenote
레이 캐스트는 광선의 시작점을 포함하는 충돌 오브젝트를 무시합니다. 이는 Box2D의 제한사항입니다.
:::
