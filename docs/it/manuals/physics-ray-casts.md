---
title: Proiezione di raggi in Defold
brief: La proiezione di raggi permette di esaminare il mondo fisico lungo un raggio rettilineo. Questo manuale ne spiega il funzionamento.
---

## Proiezione di raggi {#ray-casts}

La proiezione di raggi (ray cast) permette di esaminare il mondo fisico lungo un raggio rettilineo. Per proiettare un raggio nel mondo fisico, specifica una posizione iniziale e una finale, oltre a [un insieme di gruppi di collisione](/manuals/physics-groups) con cui verificare le intersezioni.

Se il raggio colpisce un oggetto fisico, ricevi informazioni sull'oggetto colpito. I raggi intersecano oggetti dinamici, cinematici e statici. Non interagiscono con i trigger.

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
La proiezione di raggi ignora gli oggetti di collisione che contengono il punto iniziale del raggio. Si tratta di una limitazione di Box2D.
:::
