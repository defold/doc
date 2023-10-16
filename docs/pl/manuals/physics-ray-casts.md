---
title: Promienie Ray casts w Defoldzie
brief: Ta instrukcja wyjaśnia działanie promieni Ray casts w Defoldzie.
---

## Promienie Ray casts

Promienie (ang. "ray casts") silnika fizycznego sprawdzają i odczytują świat wzdłuż liniowego promienia i raportują o wykrytych obiektach kolizji na ich przecięciu. Aby wysłać promień do świata fizycznego, podajesz pozycję początkową i końcową oraz zestaw [grup kolizyjnych](/manuals/physics-groups), z którymi chcesz przetestować dany promień.

Jeśli promień trafi w obiekt fizyczny, otrzymasz informacje o obiekcie, który został trafiony. Promienie przecinają obiekty kolizji dynamiczne, kinematyczne i statyczne. Nie oddziałują one z wyzwalaczami (ang. trigger).

```lua
function update(self, dt)
  -- wysłanie promienia
  local my_start = vmath.vector3(0, 0, 0)
  local my_end = vmath.vector3(100, 1000, 1000)
  local my_groups = { hash("my_group1"), hash("my_group2") }

  local result = physics.raycast(my_start, my_end, my_groups)
  if result then
       -- działanie w przypadku trafienia (zobacz wiadomość 'ray_cast_response' w celu uzyskania wszystkich wartości)
      print(result.id)
  end
end
```

::: sidenote
Promienie będą ignorować obiekty kolizji, które zawierają punkt początkowy promienia. Jest to ograniczenie w Box2D.
:::
