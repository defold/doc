---
title: El pipeline de renderizado en Defold
brief: Este manual explica cómo funciona el pipeline de renderizado de Defold y cómo puedes programarlo.
---

# Render

Cada objeto que el motor muestra en pantalla: sprites, modelos, tiles, partículas o nodos GUI, se dibuja mediante un renderizador. En el centro del renderizador hay un script de render que controla el pipeline de renderizado. Por defecto, cada objeto 2D se dibuja con el bitmap correcto, con el blending especificado y en la profundidad Z correcta, por lo que puede que nunca tengas que pensar en el renderizado más allá del orden y el blending simple. Para la mayoría de juegos 2D, el pipeline por defecto funciona bien, pero tu juego podría tener requisitos especiales. Si ese es el caso, Defold te permite escribir un pipeline de renderizado a medida.

### Pipeline de renderizado - ¿Qué, cuándo y dónde?

El pipeline de renderizado controla qué renderizar, cuándo renderizarlo y también dónde renderizarlo. Qué renderizar se controla con los [predicados de render](#render-predicates). Cuándo renderizar un predicado se controla en el [script de render](#the-render-script) y dónde renderizar un predicado se controla mediante la [proyección de vista](#default-view-projection). El pipeline de renderizado también puede descartar los gráficos, dibujados por un predicado de render, que quedan fuera de una caja delimitadora o frustum definido. Este proceso se llama frustum culling.


## El render por defecto

El archivo render contiene una referencia al script de render actual, además de materiales personalizados que deben estar disponibles en el script de render (para usar con [`render.enable_material()`](/ref/render/#render.enable_material)).

En el centro del pipeline de renderizado está el _script de render_. Este es un script Lua con las funciones `init()`, `update()` y `on_message()`, y se usa principalmente para interactuar con la API gráfica subyacente. El script de render tiene un lugar especial en el ciclo de vida de tu juego. Puedes encontrar más detalles en la [documentación del ciclo de vida de la aplicación](/manuals/application-lifecycle).

En la carpeta "Builtins" de tus proyectos puedes encontrar el recurso render por defecto ("default.render") y el script de render por defecto ("default.render_script").

![Render integrado](images/render/builtin.png)

Para configurar un renderizador personalizado:

1. Copia los archivos "default.render" y "default.render_script" a una ubicación dentro de la jerarquía de tu proyecto. Por supuesto, puedes crear un script de render desde cero, pero es buena idea empezar con una copia del script por defecto, especialmente si eres nuevo en Defold o en la programación gráfica.

2. Edita tu copia del archivo "default.render" y cambia la propiedad *Script* para que haga referencia a tu copia del script de render.

3. Cambia la propiedad *Render* (bajo *bootstrap*) en el archivo de configuración *game.project* para que haga referencia a tu copia del archivo "default.render".


## Predicados de render {#render-predicates}

Para poder controlar el orden de dibujo de los objetos, creas _predicados_ de render. Un predicado declara qué debe dibujarse a partir de una selección de _tags_ de material.

Cada objeto que se dibuja en la pantalla tiene un material asociado que controla cómo debe dibujarse en la pantalla. En el material, especificas uno o más _tags_ que deben asociarse con el material.

En tu script de render, puedes crear entonces un *predicado de render* y especificar qué tags deben pertenecer a ese predicado. Cuando le indicas al motor que dibuje el predicado, se dibuja cada objeto con un material que contenga todos los tags especificados para el predicado.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- un predicado que coincide con todos los sprites con el tag "tree"
local trees = render.predicate({"tree"})
-- dibujará Sprite 1, 2 y 3
render.draw(trees)

-- un predicado que coincide con todos los sprites con el tag "outlined"
local outlined = render.predicate({"outlined"})
-- dibujará Sprite 1, 2 y 4
render.draw(outlined)

-- un predicado que coincide con todos los sprites con los tags "outlined" Y "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- dibujará Sprite 1 y 2
render.draw(outlined_trees)
```


Puedes encontrar una descripción detallada de cómo funcionan los materiales en la [documentación de Material](/manuals/material).


## Proyección de vista por defecto {#default-view-projection}

El script de render por defecto está configurado para usar una proyección ortográfica adecuada para juegos 2D. Proporciona tres proyecciones ortográficas diferentes: `Stretch` (por defecto), `Fixed Fit` y `Fixed`. Como alternativa a las proyecciones ortográficas del script de render por defecto, también tienes la opción de usar la matriz de proyección proporcionada por un componente Camera.

### Proyección Stretch

La proyección stretch siempre dibujará un área de tu juego igual a las dimensiones definidas en *game.project*, incluso cuando la ventana cambie de tamaño. Si cambia la relación de aspecto, el contenido del juego se estirará vertical u horizontalmente:

![Proyección Stretch](images/render/stretch_projection.png)

*Proyección Stretch con el tamaño original de la ventana*

![Proyección Stretch al cambiar el tamaño](images/render/stretch_projection_resized.png)

*Proyección Stretch con la ventana estirada horizontalmente*

La proyección stretch es la proyección por defecto, pero si la has cambiado y necesitas volver a ella, lo haces enviando un mensaje al script de render:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Proyección Fixed Fit

Al igual que la proyección stretch, la proyección fixed fit siempre mostrará un área del juego igual a las dimensiones definidas en *game.project*, pero si la ventana cambia de tamaño y cambia la relación de aspecto, el contenido del juego mantendrá la relación de aspecto original y se mostrará contenido adicional del juego vertical u horizontalmente:

![Proyección Fixed Fit](images/render/fixed_fit_projection.png)

*Proyección Fixed Fit con el tamaño original de la ventana*

![Proyección Fixed Fit al cambiar el tamaño](images/render/fixed_fit_projection_resized.png)

*Proyección Fixed Fit con la ventana estirada horizontalmente*

![Proyección Fixed Fit al reducir el tamaño](images/render/fixed_fit_projection_resized_smaller.png)

*Proyección Fixed Fit con la ventana reducida al 50% del tamaño original*

Activas la proyección fixed fit enviando un mensaje al script de render:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Proyección Fixed {#fixed-projection}

La proyección fixed mantendrá la relación de aspecto original y renderizará el contenido de tu juego con un nivel de zoom fijo. Esto significa que si el nivel de zoom está definido en algo distinto de 100%, mostrará más o menos que el área del juego definida por las dimensiones en *game.project*:

![Proyección Fixed](images/render/fixed_projection_zoom_2_0.png)

*Proyección Fixed con el zoom definido en 2*

![Proyección Fixed](images/render/fixed_projection_zoom_0_5.png)

*Proyección Fixed con el zoom definido en 0.5*

![Proyección Fixed](images/render/fixed_projection_zoom_2_0_resized.png)

*Proyección Fixed con el zoom definido en 2 y la ventana reducida al 50% del tamaño original*

Activas la proyección fixed enviando un mensaje al script de render:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Proyección Camera

Cuando usas el script de render por defecto y hay [componentes Camera](/manuals/camera) activados disponibles en el proyecto, estos tendrán prioridad sobre cualquier otra vista/proyección definida en el script de render. Para leer más sobre cómo trabajar con componentes Camera en scripts de render, consulta la [documentación de Camera](/manuals/camera).

Las cámaras ortográficas admiten un `Orthographic Mode` que controla cómo la cámara se adapta a la ventana:
- `Fixed` usa el valor `Orthographic Zoom` de la cámara.
- `Auto Fit` (contain) mantiene visible toda el área de diseño.
- `Auto Cover` (cover) llena la ventana y puede recortar.

Puedes cambiar de modo en el editor o en tiempo de ejecución mediante la Camera API:

```lua
-- Usar comportamiento auto-fit con una cámara ortográfica
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Consultar el modo actual
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Frustum culling

La API de render de Defold permite a los desarrolladores realizar algo llamado frustum culling. Cuando el frustum culling está activado, se ignora cualquier gráfico que quede fuera de una caja delimitadora o frustum definido. En un mundo de juego grande donde solo una parte es visible a la vez, el frustum culling puede reducir drásticamente la cantidad de datos que deben enviarse a la GPU para el renderizado, lo que aumenta el rendimiento y ahorra batería (en dispositivos móviles). Es común usar la vista y la proyección de la cámara para crear la caja delimitadora. El script de render por defecto usa la vista y la proyección (de la cámara) para calcular un frustum.

Activa el frustum culling para una llamada de dibujo pasando una matriz de vista-proyección en la opción `frustum` de `render.draw()`:

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

Al renderizar con un componente Camera, `render.set_camera()` puede usar automáticamente la matriz de vista-proyección de la cámara para las llamadas de dibujo posteriores:

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

Los emisores de Particle FX se descartan según sus límites cuando se usa cualquiera de estos métodos.

El frustum culling se implementa en el motor por tipo de componente. Estado actual:

| Componente  | Soportado |
|-------------|-----------|
| Sprite      | Sí        |
| Model       | Sí        |
| Mesh        | Sí (1)    |
| Label       | Sí        |
| Spine       | Sí        |
| Particle fx | Sí        |
| Tilemap     | Sí        |
| Rive        | No        |

1 = La caja delimitadora de Mesh debe definirla el desarrollador. [Más información](/manuals/mesh/#frustum-culling).


::: sidenote
A partir de Defold 1.13.0, las primitivas de los componentes usan un orden antihorario de los vértices, con la normal de la primitiva apuntando hacia la cámara. Los sprites, los nodos GUI, los tilemaps (tilegrids) y los Particle FX usan el mismo orden que los demás tipos de componentes, por lo que se puede usar la misma configuración de descarte de caras para todos los componentes.

Esto puede afectar a los proyectos que configuran el descarte de caras para componentes distintos de los modelos. Si un componente se descarta de forma inesperada, asegúrate de seleccionar las caras posteriores con `render.set_cull_face(graphics.FACE_TYPE_BACK)`, o elimina la llamada a `render.set_cull_face()` para usar el modo predeterminado `graphics.FACE_TYPE_BACK`.
:::

## Sistemas de coordenadas

Cuando los componentes se renderizan, normalmente se habla de en qué sistema de coordenadas se renderizan. En la mayoría de juegos tienes algunos componentes dibujados en espacio del mundo y otros en espacio de pantalla.

Los componentes GUI y sus nodos suelen dibujarse en el sistema de coordenadas de espacio de pantalla, con la esquina inferior izquierda de la pantalla en la coordenada (0,0) y la esquina superior derecha en (ancho de pantalla, alto de pantalla). El sistema de coordenadas de espacio de pantalla nunca se desplaza ni se traslada de ninguna otra forma mediante una cámara. Esto hace que los nodos GUI siempre se dibujen en pantalla, independientemente de cómo se renderice el mundo.

Los sprites, tilemaps y otros componentes usados por objetos de juego que existen en tu mundo de juego suelen dibujarse en el sistema de coordenadas de espacio del mundo. Si no haces modificaciones en tu script de render y no usas ningún componente Camera para cambiar la proyección de vista, este sistema de coordenadas es igual que el sistema de coordenadas de espacio de pantalla, pero en cuanto agregas una cámara y la mueves o cambias la proyección de vista, los dos sistemas de coordenadas se separan. Cuando la cámara se mueve, la esquina inferior izquierda de la pantalla se desplazará desde (0, 0) para que se rendericen otras partes del mundo. Si la proyección cambia, las coordenadas se trasladarán (es decir, se desplazarán desde 0, 0) y también se modificarán mediante un factor de escala.


## El script de render {#the-render-script}

A continuación se muestra el código de un script de render personalizado que es una versión ligeramente modificada del integrado.

init()
: La función `init()` se usa para configurar los predicados, la vista y el color de limpieza. Estas variables se usarán durante el renderizado real.

```lua
function init(self)
    -- Definir los predicados de render. Cada predicado se dibuja por separado y
    -- eso nos permite cambiar el estado de OpenGL entre dibujos.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Crear y llenar tablas de datos que se usarán en update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: La función `update()` se llama una vez por frame. Su función es realizar el dibujo real llamando a las API subyacentes de OpenGL ES (OpenGL Embedded Systems API). Para entender correctamente qué ocurre en la función `update()`, necesitas entender cómo funciona OpenGL. Hay muchos recursos excelentes sobre OpenGL ES disponibles. El sitio oficial es un buen punto de partida. Lo encontrarás en https://www.khronos.org/opengles/

  Este ejemplo contiene la configuración necesaria para dibujar modelos 3D. La función `init()` definió un predicado `self.predicates.model`. En otro lugar se creó un material con el tag "model". También hay algunos componentes de modelo que usan el material:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- limpiar buffers de pantalla
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- renderizar modelos
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- renderizar mundo (sprites, tilemaps, partículas, etc.)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- renderizar GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Hasta aquí, este es un script de render simple y directo. Dibuja de la misma manera en cada frame. Sin embargo, a veces es deseable poder introducir estado en el script de render y realizar operaciones diferentes según ese estado. También puede ser deseable comunicarse con el script de render desde otras partes del código del juego.

on_message()
: Un script de render puede definir una función `on_message()` y recibir mensajes desde otras partes de tu juego o app. Un caso común donde un componente externo envía información al script de render es la _cámara_. Un componente Camera que ha adquirido el foco de cámara enviará automáticamente su vista y proyección al script de render en cada frame. Este mensaje se llama `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Alguien nos envió un nuevo color de limpieza para usar.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- El componente Camera que tiene el foco de cámara enviará mensajes
        -- set_view_projection al socket @render. Podemos usar la información
        -- de la cámara para definir la vista (y posiblemente la proyección)
        -- del renderizado.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

Sin embargo, cualquier script o script GUI puede enviar mensajes al script de render mediante el socket especial `@render`:

```lua
-- Cambiar el color de limpieza.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Recursos de render
Para pasar ciertos recursos del motor al script de render, puedes agregarlos a la tabla `Render Resources` del archivo `.render` asignado al proyecto:

![Recursos de render](images/render/render_resources.png)

Usar estos recursos en un script de render:

```lua
-- "my_material" se usará ahora para todas las draw calls asociadas con el predicado
render.enable_material("my_material")
-- todo lo dibujado por el predicado terminará en "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- vincular la textura resultante del render target a lo que se esté renderizando mediante el predicado
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
Actualmente Defold solo admite `Materials` y `Render Targets` como recursos de render referenciados, pero con el tiempo este sistema admitirá más tipos de recursos.
:::

## Handles de textura

Las texturas en Defold se representan internamente como un handle, que en esencia equivale a un número que debe identificar de forma única un objeto de textura en cualquier parte del motor. Esto significa que puedes conectar el mundo de los objetos de juego con el mundo del renderizado pasando estos handles entre el sistema de render y un script de objeto de juego. Por ejemplo, un script puede crear una textura dinámica en un script adjunto a un objeto de juego y enviarla al renderizador para usarla como textura global en un comando de dibujo.

En un archivo `.script`:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- nota: my_texture_resource es un hash de la ruta del recurso, que no puede usarse como handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contiene información sobre la textura, como ancho, alto, etc.
-- también contiene el handle, que es lo que buscamos
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

En un archivo `.render_script`:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- vincular la textura personalizada al estado de dibujo
    render.enable_texture(0, self.my_texture)
    -- dibujar...
end
```

::: sidenote
Actualmente no hay forma de cambiar a qué textura debe apuntar un recurso; solo puedes usar handles sin procesar como este en el script de render.
:::

## APIs gráficas soportadas
La API de script de render de Defold traduce las operaciones de render a las siguientes API gráficas:

:[Graphics API](../shared/graphics-api.md)


## Mensajes de sistema

`"set_view_projection"`
: Este mensaje se envía desde componentes Camera que han adquirido el foco de cámara.

`"window_resized"`
: El motor enviará este mensaje cuando cambie el tamaño de la ventana. Puedes escuchar este mensaje para modificar el renderizado cuando cambie el tamaño de la ventana objetivo. En escritorio esto significa que la ventana real del juego cambió de tamaño, y en dispositivos móviles este mensaje se envía cada vez que ocurre un cambio de orientación.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- La ventana cambió de tamaño. message.width y message.height contienen las nuevas dimensiones.
    ...
  end
end
```

`"draw_line"`
: Dibuja una línea de debug. Se usa para visualizar `ray_casts`, vectores y más. Las líneas se dibujan con la llamada `render.draw_debug3d()`.

```lua
-- dibujar una línea blanca
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )
```

`"draw_text"`
: Dibuja texto de debug. Se usa para imprimir información de debug. El texto se dibuja con la fuente integrada `always_on_top.font`. La fuente del sistema tiene un material con el tag `debug_text` y se renderiza con otro texto en el script de render por defecto.

```lua
-- dibujar un mensaje de texto
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })
```

El profiler visual accesible mediante el mensaje `"toggle_profile"` enviado al socket `@system` no forma parte del renderizador programable. Se dibuja separado de tu script de render.


## Draw calls y batching {#draw-calls-and-batching}

Una draw call es el término usado para describir el proceso de configurar la GPU para dibujar un objeto en la pantalla usando una textura y un material con ajustes adicionales opcionales. Este proceso suele consumir muchos recursos y se recomienda que el número de draw calls sea lo más bajo posible. Puedes medir el número de draw calls y el tiempo que lleva renderizarlas usando el [profiler integrado](/manuals/profiling/).

Defold intentará agrupar operaciones de renderizado en lotes para reducir el número de draw calls según un conjunto de reglas definidas abajo. Las reglas difieren entre componentes GUI y todos los demás tipos de componentes.


### Reglas de batching para componentes no GUI

El renderizado se hace según el orden z, de menor a mayor. El motor empezará ordenando la lista de cosas que debe dibujar e iterará desde valores z bajos hasta altos. Cada objeto de la lista se agrupará en la misma draw call que el objeto anterior si se cumplen las siguientes condiciones:

* Pertenece al mismo proxy de colección
* Es del mismo tipo de componente (sprite, particle fx, tilemap, etc.)
* Usa la misma textura (atlas o tile source)
* Tiene el mismo material
* Tiene las mismas constantes de shader (como tint)

Esto significa que si dos componentes sprite en el mismo proxy de colección tienen valores z adyacentes o iguales (y por tanto quedan uno junto al otro en la lista ordenada), usan la misma textura, material y constantes, se agruparán en la misma draw call.


### Reglas de batching para componentes GUI

El renderizado de los nodos de un componente GUI se hace de arriba hacia abajo en la lista de nodos. Cada nodo de la lista se agrupará en la misma draw call que el nodo anterior si se cumplen las siguientes condiciones:

* Es del mismo tipo (box, text, pie, etc.)
* Usa la misma textura (atlas o tile source)
* Tiene el mismo blend mode.
* Tiene la misma fuente (solo para nodos de texto)
* Tiene la misma configuración de stencil

::: sidenote
El renderizado de nodos se hace por componente. Esto significa que los nodos de componentes GUI diferentes no se agruparán en lotes.
:::

La capacidad de organizar nodos en jerarquías facilita agrupar nodos en unidades manejables. Pero las jerarquías pueden romper efectivamente el renderizado en lotes si mezclas distintos tipos de nodo. Es posible agrupar nodos GUI en lotes de manera más efectiva y a la vez mantener jerarquías de nodos usando capas GUI. Puedes leer más sobre las capas GUI y cómo afectan las draw calls en el [manual de GUI](/manuals/gui#layers-and-draw-calls).
