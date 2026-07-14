---
title: Propiedades en Defold
brief: Este manual explica qué tipos de propiedades existen en Defold y cómo se usan y se animan.
---

# Propiedades

Defold expone propiedades para objetos de juego (Game objects), componentes (Components) y nodos GUI que se pueden leer, definir y animar. Existen los siguientes tipos de propiedades:

* Transformaciones de objetos de juego definidas por el sistema (posición, rotación y escala) y propiedades específicas de componentes (por ejemplo, el tamaño en píxeles de un sprite o la masa de un objeto de colisión)
* Propiedades de componentes de script definidas por el usuario en scripts Lua (consulta la [documentación de propiedades de script](/manuals/script-properties) para más detalles)
* Propiedades de nodos GUI
* Constantes de shader definidas en shaders y archivos de material (consulta la [documentación de material](/manuals/material) para más detalles)

Las propiedades numéricas muestran un control de arrastre cuando pasas el cursor sobre su campo de entrada. Puedes aumentar o disminuir su valor arrastrando el control hacia la derecha/izquierda o arriba/abajo, respectivamente.

Según dónde se encuentre una propiedad, accedes a ella mediante una función genérica o una función específica de la propiedad. Muchas de las propiedades se pueden animar automáticamente. Se recomienda encarecidamente animar propiedades mediante el sistema integrado en vez de manipularlas directamente (dentro de una función `update()`), tanto por rendimiento como por comodidad.

Las propiedades compuestas de tipo `vector3`, `vector4` o `quaternion` también exponen sus subcomponentes (`x`, `y`, `z` y `w`). Puedes hacer referencia a los componentes individualmente añadiendo al nombre un punto (`.`) y el nombre del componente. Por ejemplo, para definir el componente x de la posición de un objeto de juego:

```lua
-- Define la posición x de "game_object" en 10.
go.set("game_object", "position.x", 10)
```

Las funciones `go.get()`, `go.set()` y `go.animate()` toman una referencia como primer parámetro y un identificador de propiedad como segundo. La referencia identifica el objeto de juego o componente, y puede ser un string, un hash o una URL. Las URL se explican en detalle en el [manual de direccionamiento](/manuals/addressing). El identificador de propiedad es un string o hash que nombra la propiedad:

```lua
-- Define la escala x del componente sprite
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

En los nodos GUI, el nodo se proporciona como primer parámetro a una función específica de la propiedad o a las funciones genéricas `gui.get()` y `gui.set()`:

```lua
-- Obtiene el color del botón
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Propiedades de objetos de juego y componentes

Todos los objetos de juego, y algunos tipos de componente, tienen propiedades que se pueden leer y manipular en tiempo de ejecución. Obtén estos valores con [`go.get()`](/ref/go#go.get) y defínelos con [`go.set()`](/ref/go#go.set). Según el tipo del valor de la propiedad, puedes animar los valores con [`go.animate()`](/ref/go#go.animate). Un pequeño conjunto de propiedades es de solo lectura.

`get`{.mark}
: Se puede leer con [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Se puede leer con [`go.get()`](/ref/go#go.get) y escribir con [`go.set()`](/ref/go#go.set). Los valores numéricos se pueden animar con [`go.animate()`](/ref/go#go.animate).

*PROPIEDADES DE OBJETOS DE JUEGO*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | La posición local del objeto de juego. | `vector3`      | `get+set`{.mark} |
| *rotation* | Rotación local del objeto de juego, expresada como un `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Rotación local del objeto de juego, ángulos de Euler. | `vector3` | `get+set`{.mark} |
| *scale*    | Escala local no uniforme del objeto de juego, expresada como un vector donde cada componente contiene un multiplicador a lo largo de cada eje. Para duplicar el tamaño en X e Y sin cambiar Z, usa `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy* | Escala local no uniforme del objeto de juego a lo largo de los ejes X e Y. Usa esta propiedad o `go.set_scale_xy()` cuando no se pretenda escalar Z. | `vector3` | `get+set`{.mark} |

::: sidenote
También existen funciones específicas para trabajar con la transformación del objeto de juego; son `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`, `go.get_scale()`, `go.set_scale()` y `go.set_scale_xy()`.
:::

*PROPIEDADES DEL COMPONENTE SPRITE*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | El tamaño no escalado del sprite, su tamaño tal como se toma del atlas de origen. | `vector3` | `get`{.mark} |
| *image* | El hash de la ruta de textura del sprite. | `hash` | `get`{.mark}|
| *scale* | Escala no uniforme del sprite. | `vector3` | `get+set`{.mark}|
| *scale.xy* | Escala no uniforme del sprite a lo largo de los ejes X e Y. | `vector3` | `get+set`{.mark}|
| *material* | El material que usa el sprite. | `hash` | `get+set`{.mark}|
| *cursor* | Posición (entre 0--1) del cursor de reproducción. | `number` | `get+set`{.mark}|
| *playback_rate* | La velocidad de reproducción de la animación flipbook, expresada en fotogramas por segundo (FPS). | `number` | `get+set`{.mark}|

*PROPIEDADES DEL COMPONENTE COLLISION OBJECT*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | La masa del objeto de colisión. | `number` | `get`{.mark} |
| *linear_velocity* | La velocidad lineal actual del objeto de colisión. | `vector3` | `get`{.mark} |
| *angular_velocity* | La velocidad angular actual del objeto de colisión. | `vector3` | `get`{.mark} |
| *linear_damping* | Amortiguación lineal del objeto de colisión. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Amortiguación angular del objeto de colisión. | `vector3` | `get+set`{.mark} |

*PROPIEDADES DEL COMPONENTE MODEL (3D)*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | La animación actual.                  | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Los hashes de las rutas de textura del modelo. | `hash` | `get+set`{.mark}|
| *cursor*  | Posición (entre 0--1) del cursor de reproducción. | `number`   | `get+set`{.mark} |
| *playback_rate* | La tasa de reproducción de la animación. Un multiplicador de la tasa de reproducción de la animación. | `number` | `get+set`{.mark} |
| *material* | El material que usa el modelo. | `hash` | `get+set`{.mark}|

*PROPIEDADES DEL COMPONENTE LABEL*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | La escala del label. | `vector3` | `get+set`{.mark} |
| *scale.xy* | La escala del label a lo largo de los ejes X e Y. | `vector3` | `get+set`{.mark}|
| *color*     | El color del label. | `vector4` | `get+set`{.mark} |
| *outline* | El color del contorno del label. | `vector4` | `get+set`{.mark} |
| *shadow* | El color de la sombra del label. | `vector4` | `get+set`{.mark} |
| *size* | El tamaño del label. El tamaño restringirá el texto si el salto de línea está activado. | `vector3` | `get+set`{.mark} |
| *material* | El material que usa el label. | `hash` | `get+set`{.mark}|
| *font* | La fuente que usa el label. | `hash` | `get+set`{.mark}|


## Propiedades de nodos GUI

Los nodos GUI tienen funciones getter y setter específicas de cada propiedad, como `gui.get_position()` y `gui.set_position()`. Como alternativa, las propiedades integradas que se indican a continuación pueden leerse y escribirse con `gui.get(node, property)` y `gui.set(node, property, value)`. Otros valores de nodo pueden seguir requiriendo sus funciones específicas. Las constantes de material de los nodos GUI también usan las funciones genéricas. Para direccionar un componente de una propiedad vectorial, agrega su nombre; por ejemplo, `gui.set(node, "color.x", 1)`.

Las funciones genéricas y las específicas de cada propiedad no siempre usan tipos de valor idénticos. `gui.get()` devuelve un `vector4` para las propiedades completas `position`, `scale`, `size` y `euler`, mientras que las funciones específicas correspondientes devuelven un `vector3`. `gui.set()` acepta un `vector3` o un `vector4` para esas propiedades. La propiedad genérica `rotation` usa un quaternion; usa `euler` al definir la rotación en grados.

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

Ten en cuenta que todos los valores de color están codificados en un `vector4`, donde los componentes corresponden a los valores RGBA:

`x`
: El componente de color rojo

`y`
: El componente de color verde

`z`
: El componente de color azul

`w`
: El componente alfa

*PROPIEDADES DE NODOS GUI*

| propiedad  | descripción                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | El color frontal del nodo.             | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | El color del contorno del nodo.        | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | La posición del nodo. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | La rotación del nodo. El getter devuelve un quaternion; el setter acepta un quaternion o ángulos de Euler como vector. | `quaternion`, `vector3` o `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | La rotación del nodo expresada como ángulos de Euler en grados. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | La escala del nodo expresada como un multiplicador a lo largo de cada eje. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | El color de la sombra del nodo. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | El tamaño sin escalar del nodo. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | El ángulo de relleno de un nodo Pie expresado en grados en sentido antihorario. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | El radio interior de un nodo Pie. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | La escala del espaciado entre líneas de un nodo de texto. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | La escala del espaciado entre letras de un nodo de texto. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | Las distancias de borde de un nodo slice9. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
