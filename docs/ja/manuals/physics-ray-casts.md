---
title: Defold のレイキャスト
brief: レイキャストは、直線状のレイに沿って物理ワールドを調べるために使います。このマニュアルでは、その仕組みを説明します。
---

## レイキャスト {#ray-casts}

レイキャスト（ray cast）は、直線状のレイに沿って物理ワールド（physics world）を調べるために使います。物理ワールド内でレイキャストを行うには、始点と終点の位置に加え、判定対象の[コリジョングループ（collision group）の集合](/manuals/physics-groups)を指定します。

レイが物理オブジェクトにヒットすると、そのオブジェクトについての情報が得られます。レイは動的オブジェクト（dynamic object）、キネマティックオブジェクト（kinematic object）、静的オブジェクト（static object）と交差します。トリガー（trigger）とは相互作用しません。

```lua
function update(self, dt)
  -- request ray cast
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
      -- act on the hit (see 'ray_cast_response' message for all values)
      print(result.id)
  end
end
```

::: sidenote
レイキャストは、レイの始点を内部に含むコリジョンオブジェクト（collision object）を無視します。これは Box2D の制限です。
:::
