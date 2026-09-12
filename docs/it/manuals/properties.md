---
title: Proprietà in Defold
brief: Questo manuale illustra i tipi di proprietà disponibili in Defold e spiega come usare e animare le proprietà.
---

# Proprietà {#properties}

Defold espone proprietà per oggetti di gioco (game object), componenti e nodi GUI che puoi leggere, impostare e animare. Esistono i seguenti tipi di proprietà:

* Trasformazioni degli oggetti di gioco definite dal sistema (posizione, rotazione e scala) e proprietà specifiche dei componenti (per esempio le dimensioni in pixel di uno sprite o la massa di un oggetto di collisione)
* Proprietà dei componenti script definite dall'utente negli script Lua (consulta la [documentazione sulle proprietà degli script](/manuals/script-properties) per i dettagli)
* Proprietà dei nodi GUI
* Costanti degli shader definite negli shader e nei file dei materiali (consulta la [documentazione sui materiali](/manuals/material) per i dettagli)

Le proprietà numeriche mostrano una maniglia di trascinamento quando passi il puntatore sul loro campo di immissione. Puoi aumentare o diminuire il valore trascinando la maniglia rispettivamente verso destra o sinistra, oppure verso l'alto o il basso.

A seconda di dove si trova una proprietà, puoi accedervi tramite una funzione generica o una funzione specifica per quella proprietà. Molte proprietà possono essere animate automaticamente. È fortemente consigliato animare le proprietà tramite il sistema integrato anziché modificarle direttamente (all'interno di una funzione `update()`), sia per le prestazioni sia per la praticità.

Le proprietà composte di tipo `vector3`, `vector4` o `quaternion` espongono anche le proprie componenti (`x`, `y`, `z` e `w`). Puoi accedere alle componenti singolarmente aggiungendo al nome della proprietà un punto (`.`) e il nome della componente. Per esempio, per impostare la componente x della posizione di un oggetto di gioco:

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

Le funzioni `go.get()`, `go.set()` e `go.animate()` accettano un riferimento come primo parametro e un identificatore di proprietà come secondo. Il riferimento identifica l'oggetto di gioco o il componente e può essere una stringa, un hash o un URL. Gli URL sono spiegati in dettaglio nel [manuale sull'indirizzamento](/manuals/addressing). L'identificatore della proprietà è una stringa o un hash che ne specifica il nome:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

Per i nodi GUI, il nodo viene passato come primo parametro a una funzione specifica per la proprietà oppure alle funzioni generiche `gui.get()` e `gui.set()`:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Proprietà degli oggetti di gioco e dei componenti {#game-object-and-component-properties}

Tutti gli oggetti di gioco e alcuni tipi di componenti hanno proprietà che puoi leggere e modificare durante l'esecuzione. Leggi questi valori con [`go.get()`](/ref/go#go.get) e scrivili con [`go.set()`](/ref/go#go.set). A seconda del tipo di valore della proprietà, puoi animarne i valori con [`go.animate()`](/ref/go#go.animate). Un piccolo gruppo di proprietà è di sola lettura.

`get`{.mark}
: Puoi leggerla con [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Puoi leggerla con [`go.get()`](/ref/go#go.get) e scriverla con [`go.set()`](/ref/go#go.set). Puoi animare i valori numerici con [`go.animate()`](/ref/go#go.animate).

*PROPRIETÀ DEGLI OGGETTI DI GIOCO*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | La posizione locale dell'oggetto di gioco. | `vector3`      | `get+set`{.mark} |
| *rotation* | La rotazione locale dell'oggetto di gioco, espressa come `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | La rotazione locale dell'oggetto di gioco, espressa in angoli di Eulero. | `vector3` | `get+set`{.mark} |
| *scale*    | La scala locale non uniforme dell'oggetto di gioco, espressa come un vettore in cui ogni componente contiene un moltiplicatore lungo il rispettivo asse. Per raddoppiare le dimensioni lungo X e Y senza modificare Z, usa `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | La scala locale non uniforme dell'oggetto di gioco lungo gli assi X e Y. Usa questa proprietà o `go.set_scale_xy()` quando non vuoi modificare la scala lungo Z. | `vector3` | `get+set`{.mark} |

::: sidenote
Esistono anche funzioni specifiche per lavorare con la trasformazione dell'oggetto di gioco: `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` e `go.set_scale_xy()`.
:::

*PROPRIETÀ DEL COMPONENTE SPRITE*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | Le dimensioni dello sprite prima dell'applicazione della scala, così come sono definite nell'atlas di origine. | `vector3` | `get`{.mark} |
| *image* | L'hash del percorso della texture dello sprite. | `hash` | `get`{.mark}|
| *scale* | La scala non uniforme dello sprite. | `vector3` | `get+set`{.mark}|
| *scale.xy* | La scala non uniforme dello sprite lungo gli assi X e Y. | `vector3` | `get+set`{.mark}|
| *material* | Il materiale usato dallo sprite. | `hash` | `get+set`{.mark}|
| *cursor* | La posizione (tra 0--1) del cursore di riproduzione. | `number` | `get+set`{.mark}|
| *playback_rate* | La frequenza dei fotogrammi dell'animazione flipbook. | `number` | `get+set`{.mark}|

*PROPRIETÀ DEL COMPONENTE OGGETTO DI COLLISIONE*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | La massa dell'oggetto di collisione. | `number` | `get`{.mark} |
| *linear_velocity* | La velocità lineare attuale dell'oggetto di collisione. | `vector3` | `get`{.mark} |
| *angular_velocity* | La velocità angolare attuale dell'oggetto di collisione. | `vector3` | `get`{.mark} |
| *linear_damping* | Lo smorzamento lineare dell'oggetto di collisione. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Lo smorzamento angolare dell'oggetto di collisione. | `vector3` | `get+set`{.mark} |

*PROPRIETÀ DEL COMPONENTE MODELLO (3D)*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | L'animazione attuale.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Gli hash dei percorsi delle texture del modello. | `hash` | `get+set`{.mark}|
| *cursor*  | La posizione (tra 0--1) del cursore di riproduzione. | `number`   | `get+set`{.mark} |
| *playback_rate* | La velocità di riproduzione dell'animazione. Un moltiplicatore della velocità di riproduzione dell'animazione. | `number` | `get+set`{.mark} |
| *material* | Il materiale usato dal modello. | `hash` | `get+set`{.mark}|

*PROPRIETÀ DEL COMPONENTE ETICHETTA (LABEL)*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *text* | Il contenuto testuale dell'etichetta. Disponibile da Defold 1.13.2. | `string` | `get+set`{.mark} |
| *scale* | La scala dell'etichetta. | `vector3` | `get+set`{.mark} |
| *scale.xy* | La scala dell'etichetta lungo gli assi X e Y. | `vector3` | `get+set`{.mark}|
| *color*     | Il colore dell'etichetta. | `vector4` | `get+set`{.mark} |
| *outline* | Il colore del contorno dell'etichetta. | `vector4` | `get+set`{.mark} |
| *shadow* | Il colore dell'ombra dell'etichetta. | `vector4` | `get+set`{.mark} |
| *size* | Le dimensioni dell'etichetta. Le dimensioni limitano il testo se il ritorno a capo è abilitato. | `vector3` | `get+set`{.mark} |
| *material* | Il materiale usato dall'etichetta. | `hash` | `get+set`{.mark}|
| *font* | Il font usato dall'etichetta. | `hash` | `get+set`{.mark}|


## Proprietà dei nodi GUI {#gui-node-properties}

I nodi GUI hanno funzioni di lettura e scrittura specifiche per ciascuna proprietà, come `gui.get_position()` e `gui.set_position()`. In alternativa, puoi leggere e scrivere le proprietà integrate elencate di seguito con `gui.get(node, property)` e `gui.set(node, property, value)`. Altri valori dei nodi possono comunque richiedere le rispettive funzioni dedicate. Anche le costanti dei materiali sui nodi GUI usano le funzioni generiche. Per accedere a una componente di una proprietà vettoriale, aggiungine il nome, per esempio `gui.set(node, "color.x", 1)`.

Le funzioni generiche e quelle specifiche per le proprietà non usano sempre gli stessi tipi di valore. `gui.get()` restituisce un `vector4` per le proprietà complete `position`, `scale`, `size` ed `euler`, mentre le funzioni specifiche corrispondenti restituiscono un `vector3`. `gui.set()` accetta sia un `vector3` sia un `vector4` per queste proprietà. La proprietà generica `rotation` usa un quaternione; usa `euler` per impostare la rotazione in gradi.

* `position` (o `gui.PROP_POSITION`)
* `rotation` (o `gui.PROP_ROTATION`)
* `euler` (o `gui.PROP_EULER`)
* `scale` (o `gui.PROP_SCALE`)
* `color` (o `gui.PROP_COLOR`)
* `outline` (o `gui.PROP_OUTLINE`)
* `shadow` (o `gui.PROP_SHADOW`)
* `size` (o `gui.PROP_SIZE`)
* `fill_angle` (o `gui.PROP_FILL_ANGLE`)
* `inner_radius` (o `gui.PROP_INNER_RADIUS`)
* `leading` (o `gui.PROP_LEADING`)
* `tracking` (o `gui.PROP_TRACKING`)
* `slice9` (o `gui.PROP_SLICE9`)

Tutti i valori dei colori sono codificati in un `vector4` le cui componenti corrispondono ai valori RGBA:

`x`
: La componente rossa del colore

`y`
: La componente verde del colore

`z`
: La componente blu del colore

`w`
: La componente alfa

*PROPRIETÀ DEI NODI GUI*

| proprietà   | descrizione                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | Il colore della superficie del nodo.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | Il colore del contorno del nodo.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | La posizione del nodo. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | La rotazione del nodo. La funzione di lettura restituisce un quaternione; quella di scrittura accetta un quaternione o angoli di Eulero sotto forma di vettore. | `quaternion`, `vector3` o `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | La rotazione del nodo espressa come angoli di Eulero in gradi. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | La scala del nodo espressa come un moltiplicatore lungo ciascun asse. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | Il colore dell'ombra del nodo. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | Le dimensioni del nodo prima dell'applicazione della scala. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | L'angolo di riempimento di un nodo a torta (pie), espresso in gradi in senso antiorario. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | Il raggio interno di un nodo a torta. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | Il fattore di scala dell'interlinea di un nodo di testo. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | Il fattore di scala della spaziatura tra le lettere di un nodo di testo. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | Le distanze dei bordi di un nodo slice9. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
