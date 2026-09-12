---
title: Strahlabfragen in Defold
brief: Strahlabfragen werden verwendet, um die Physikwelt entlang eines geraden Strahls auszulesen. Dieses Handbuch erklärt, wie das funktioniert.
---

## Strahlabfragen {#ray-casts}

Mit Strahlabfragen (raycast) liest du die Physikwelt (physics world) entlang eines geraden Strahls aus. Um einen Strahl in die Physikwelt zu senden, gibst du eine Start- und eine Endposition sowie [eine Menge von Kollisionsgruppen (collision groups)](/manuals/physics-groups) an, gegen die geprüft werden soll.

Trifft der Strahl ein Physikobjekt, erhältst du Informationen über das getroffene Objekt. Strahlen können dynamische, kinematische und statische Kollisionsobjekte (collision objects) schneiden. Sie interagieren nicht mit Triggern.

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
Strahlabfragen ignorieren Kollisionsobjekte, die den Startpunkt des Strahls enthalten. Dies ist eine Einschränkung von Box2D.
:::
