---
title: Defold'da ışın sorguları
brief: Işın sorguları, fizik dünyasını doğrusal bir ışın boyunca sorgulamak için kullanılır. Bu kılavuz bunun nasıl çalıştığını açıklar.
---

## Işın sorguları

Işın sorguları (ray cast), fizik dünyasını (physics world) doğrusal bir ışın boyunca sorgulamak için kullanılır. Fizik dünyasında bir ışın sorgusu yapmak için başlangıç ve bitiş konumlarının yanı sıra sınamanın yapılacağı [bir çarpışma grubu (collision group) kümesi](/manuals/physics-groups) belirtin.

Işın bir fizik nesnesine isabet ederse isabet ettiği nesne hakkında bilgi alırsınız. Işınlar dinamik, kinematik ve statik nesnelerle kesişir. Tetikleyicilerle (trigger) etkileşime girmezler.

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
Işın sorguları, ışının başlangıç noktasını içeren çarpışma nesnelerini (collision object) yok sayar. Bu, Box2D'nin bir kısıtlamasıdır.
:::
