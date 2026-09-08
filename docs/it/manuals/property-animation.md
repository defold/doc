---
title: Manuale delle animazioni delle proprietà in Defold
brief: Questo manuale descrive come usare le animazioni delle proprietà in Defold.
---

# Animazione delle proprietà {#property-animation}

Tutte le proprietà numeriche (`numbers`, `vector3`, `vector4` e quaternioni) e le costanti degli shader possono essere animate con il sistema di animazione integrato, usando la funzione `go.animate()`. Il motore interpola automaticamente le proprietà in base alle modalità di riproduzione e alle funzioni di interpolazione (easing) specificate. Puoi anche specificare funzioni di interpolazione personalizzate.

  ![Animazione delle proprietà](images/animation/property_animation.png)
  ![Rimbalzo in ciclo](images/animation/bounce.gif)

## Animazione delle proprietà {#property-animation}

Per animare una proprietà di un oggetto di gioco (game object) o di un componente, usa la funzione `go.animate()`. Per le proprietà dei nodi GUI, la funzione corrispondente è `gui.animate()`.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Per interrompere tutte le animazioni di una determinata proprietà, chiama `go.cancel_animations()` oppure, per i nodi GUI, `gui.cancel_animations()`:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

Se annulli l'animazione di una proprietà composta, come `position`, vengono annullate anche tutte le animazioni delle sue singole componenti (`position.x`, `position.y` e `position.z`).

Il [manuale delle proprietà](/manuals/properties) elenca tutte le proprietà disponibili per oggetti di gioco, componenti e nodi GUI.

## Animazione delle proprietà dei nodi GUI {#gui-node-property-animation}

Puoi animare quasi tutte le proprietà dei nodi GUI. Per esempio, puoi rendere un nodo invisibile impostando la sua proprietà `color` su una trasparenza completa, per poi farlo apparire gradualmente animando il colore fino al bianco (cioè senza alcuna tinta).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Callback di completamento {#completion-callbacks}

Le funzioni di animazione delle proprietà `go.animate()` e `gui.animate()` supportano una funzione di callback Lua facoltativa come ultimo argomento. Questa funzione viene chiamata quando l'animazione giunge al termine. La funzione non viene mai chiamata per le animazioni cicliche, né quando un'animazione viene annullata manualmente tramite `go.cancel_animations()` o `gui.cancel_animations()`. Puoi usare la callback per attivare eventi al completamento dell'animazione o per concatenare più animazioni.

## Interpolazione {#easing}

L'interpolazione definisce come cambia nel tempo il valore animato. Le immagini qui sotto mostrano le funzioni applicate nel tempo per ottenere l'interpolazione.

I seguenti valori sono validi per l'interpolazione con `go.animate()`:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

I seguenti valori sono validi per l'interpolazione con `gui.animate()`:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Interpolazione lineare](images/properties/easing_linear.png)
![Curva con arretramento in ingresso](images/properties/easing_inback.png)
![Curva con arretramento in uscita](images/properties/easing_outback.png)
![Curva con arretramento in ingresso e in uscita](images/properties/easing_inoutback.png)
![Curva con arretramento in uscita e in ingresso](images/properties/easing_outinback.png)
![Rimbalzo in ingresso](images/properties/easing_inbounce.png)
![Rimbalzo in uscita](images/properties/easing_outbounce.png)
![Rimbalzo in ingresso e in uscita](images/properties/easing_inoutbounce.png)
![Rimbalzo in uscita e in ingresso](images/properties/easing_outinbounce.png)
![Curva elastica in ingresso](images/properties/easing_inelastic.png)
![Curva elastica in uscita](images/properties/easing_outelastic.png)
![Curva elastica in ingresso e in uscita](images/properties/easing_inoutelastic.png)
![Curva elastica in uscita e in ingresso](images/properties/easing_outinelastic.png)
![Curva sinusoidale in ingresso](images/properties/easing_insine.png)
![Curva sinusoidale in uscita](images/properties/easing_outsine.png)
![Curva sinusoidale in ingresso e in uscita](images/properties/easing_inoutsine.png)
![Curva sinusoidale in uscita e in ingresso](images/properties/easing_outinsine.png)
![Curva esponenziale in ingresso](images/properties/easing_inexpo.png)
![Curva esponenziale in uscita](images/properties/easing_outexpo.png)
![Curva esponenziale in ingresso e in uscita](images/properties/easing_inoutexpo.png)
![Curva esponenziale in uscita e in ingresso](images/properties/easing_outinexpo.png)
![Curva circolare in ingresso](images/properties/easing_incirc.png)
![Curva circolare in uscita](images/properties/easing_outcirc.png)
![Curva circolare in ingresso e in uscita](images/properties/easing_inoutcirc.png)
![Curva circolare in uscita e in ingresso](images/properties/easing_outincirc.png)
![Curva quadratica in ingresso](images/properties/easing_inquad.png)
![Curva quadratica in uscita](images/properties/easing_outquad.png)
![Curva quadratica in ingresso e in uscita](images/properties/easing_inoutquad.png)
![Curva quadratica in uscita e in ingresso](images/properties/easing_outinquad.png)
![Curva cubica in ingresso](images/properties/easing_incubic.png)
![Curva cubica in uscita](images/properties/easing_outcubic.png)
![Curva cubica in ingresso e in uscita](images/properties/easing_inoutcubic.png)
![Curva cubica in uscita e in ingresso](images/properties/easing_outincubic.png)
![Curva di quarto grado in ingresso](images/properties/easing_inquart.png)
![Curva di quarto grado in uscita](images/properties/easing_outquart.png)
![Curva di quarto grado in ingresso e in uscita](images/properties/easing_inoutquart.png)
![Curva di quarto grado in uscita e in ingresso](images/properties/easing_outinquart.png)
![Curva di quinto grado in ingresso](images/properties/easing_inquint.png)
![Curva di quinto grado in uscita](images/properties/easing_outquint.png)
![Curva di quinto grado in ingresso e in uscita](images/properties/easing_inoutquint.png)
![Curva di quinto grado in uscita e in ingresso](images/properties/easing_outinquint.png)

## Interpolazione personalizzata {#custom-easing}

Puoi creare curve di interpolazione personalizzate definendo un `vector` con un insieme di valori e passando poi il vettore al posto di una delle costanti di interpolazione predefinite elencate sopra. I valori del vettore descrivono una curva dal valore iniziale (`0`) al valore di destinazione (`1`). Il runtime campiona i valori del vettore e usa un'interpolazione lineare per calcolare i valori intermedi tra i punti definiti nel vettore.

Per esempio, il vettore:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

produce la seguente curva:

![Curva personalizzata](images/animation/custom_curve.png)

Nell'esempio seguente, la posizione y di un oggetto di gioco passa bruscamente dalla posizione corrente a 200 e viceversa, seguendo una curva a onda quadra:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Curva a onda quadra](images/animation/square_curve.png)
