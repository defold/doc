---
title: Lancers de rayons dans Defold
brief: Les lancers de rayons permettent d'interroger le monde physique le long d'un rayon rectiligne. Ce manuel explique leur fonctionnement.
---

## Lancers de rayons {#ray-casts}

Les lancers de rayons (ray casts) permettent d'interroger le monde physique le long d'un rayon rectiligne. Pour lancer un rayon dans le monde physique, vous fournissez une position de départ et une position d'arrivée, ainsi qu'[un ensemble de groupes de collision](/manuals/physics-groups) à tester.

Si le rayon touche un objet physique, vous obtenez des informations sur l'objet touché. Les rayons peuvent rencontrer des objets dynamiques, cinématiques et statiques. Ils n'interagissent pas avec les déclencheurs.

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
Les lancers de rayons ignorent les objets de collision qui contiennent le point de départ du rayon. Il s'agit d'une limitation de Box2D.
:::
