---
title: Manual del componente Camera
brief: Este manual describe la funcionalidad del componente Camera de Defold.
---

# Cámaras

Una cámara en Defold es un componente que cambia el viewport y la proyección del mundo del juego. El componente Camera define una cámara básica en perspectiva u ortográfica que proporciona una matriz de vista y una matriz de proyección al script de render.

Una cámara en perspectiva se usa normalmente en juegos 3D, donde la vista de la cámara y el tamaño y la perspectiva de los objetos se basan en un frustum de vista, y en la distancia y el ángulo de visión desde la cámara hasta los objetos del juego.

Para juegos 2D, a menudo es deseable renderizar la escena con una proyección ortográfica. Esto significa que la vista de la cámara ya no está dictada por un frustum de vista, sino por una caja. La proyección ortográfica no es realista porque no altera el tamaño de los objetos según su distancia. Un objeto a 1000 unidades de distancia se renderizará con el mismo tamaño que un objeto justo frente a la cámara.

![proyecciones](images/camera/projections.png)


## Crear una cámara

Para crear una cámara, haz <kbd>click derecho</kbd> en un objeto de juego y selecciona <kbd>Add Component ▸ Camera</kbd>. Como alternativa, puedes crear un archivo de componente en la jerarquía de tu proyecto y agregar el archivo de componente al objeto de juego.

![crear componente Camera](images/camera/create.png)

El componente Camera tiene las siguientes propiedades que definen el *frustum* de la cámara:

![configuración de cámara](images/camera/settings.png)

Id
: El id del componente

Aspect Ratio
: (**Solo cámara en perspectiva**) - La relación entre el ancho y la altura del frustum. 1.0 significa que asumes una vista cuadrada. 1.33 es adecuado para una vista 4:3 como 1024x768. 1.78 es adecuado para una vista 16:9. Esta opción se ignora si *Auto Aspect Ratio* está activado.

Fov
: (**Solo cámara en perspectiva**) - El campo de visión *vertical* de la cámara, expresado en _radianes_. Cuanto más amplio sea el campo de visión, más verá la cámara.

Near Z
: El valor Z del plano de recorte cercano.

Far Z
: El valor Z del plano de recorte lejano.

Auto Aspect Ratio
: (**Solo cámara en perspectiva**) - Activa esto para permitir que la cámara calcule automáticamente la relación de aspecto.

Orthographic Projection
: Activa esto para cambiar la cámara a una proyección ortográfica (ver abajo).

Orthographic Zoom
: (**Solo cámara ortográfica**) - Un multiplicador de zoom controlado por el usuario (> 1 = acercar, < 1 = alejar). En el modo `Fixed` es el zoom efectivo. En los modos `Auto Fit` y `Auto Cover` se multiplica por el zoom calculado automáticamente, lo que permite aplicar un zoom adicional sin desactivar el ajuste automático.

Orthographic Mode
: (**Solo cámara ortográfica**) - Controla cómo la cámara ortográfica determina el zoom en relación con el tamaño de la ventana y tu resolución de diseño (los valores en `game.project` → `display.width/height`).
  - `Fixed` (usa zoom constante): Usa el valor actual de `Orthographic Zoom` tal como está.
  - `Auto Fit` (contain): Calcula automáticamente el zoom para que toda el área de diseño quepa dentro de la ventana y después lo multiplica por `Orthographic Zoom`. Puede mostrar contenido adicional a los lados o arriba/abajo.
  - `Auto Cover` (cover): Calcula automáticamente el zoom para que el área de diseño cubra toda la ventana y después lo multiplica por `Orthographic Zoom`. Puede recortar los lados o la parte superior/inferior.
  Disponible solo cuando `Orthographic Projection` está activado.


## Usar la cámara

Todas las cámaras se activan y actualizan automáticamente durante un frame, y el módulo Lua `camera` está disponible en todos los contextos de script. Desde Defold 1.8.1 ya no es necesario activar explícitamente una cámara enviando un mensaje `acquire_camera_focus` al componente Camera. Los mensajes antiguos para adquirir y liberar siguen disponibles, pero se recomienda usar en su lugar los mensajes `enable` y `disable`, igual que con cualquier otro componente que quieras activar o desactivar:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Para listar todas las cámaras disponibles actualmente, puedes usar `camera.get_cameras()`:

```lua
-- Nota: Las llamadas de render solo están disponibles en un render script.
--       La función camera.get_cameras() puede usarse en cualquier lugar,
--       pero render.set_camera solo puede usarse en un render script.

for k,v in pairs(camera.get_cameras()) do
    -- la tabla de cámaras contiene las URL de todas las cámaras
    render.set_camera(v)
    -- renderiza aquí; cualquier cosa renderizada aquí que use materiales con
    -- matrices de vista y proyección especificadas usará matrices de la cámara.
end
-- para desactivar una cámara, pasa nil (o ningún argumento) a render.set_camera.
-- después de esta llamada, todas las llamadas de render usarán las matrices de
-- vista y proyección especificadas en el contexto de render
-- (render.set_view y render.set_projection)
render.set_camera()
```

El módulo de scripting `camera` tiene varias funciones que pueden usarse para manipular la cámara. Estas son algunas de las funciones disponibles; para verlas todas, consulta el manual en la [documentación de la API](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- obtener relación de aspecto
camera.get_far_z(camera) -- obtener far z
camera.get_fov(camera) -- obtener campo de visión
camera.get_orthographic_mode(camera) -- obtener modo ortográfico (uno de camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- obtener el multiplicador de zoom controlado por el usuario
camera.get_orthographic_auto_zoom(camera) -- obtener el zoom calculado automáticamente
camera.set_aspect_ratio(camera, ratio) -- definir relación de aspecto
camera.set_far_z(camera, far_z) -- definir far z
camera.set_near_z(camera, near_z) -- definir near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- definir modo ortográfico
... And so forth
```

Una cámara se identifica mediante una URL, que es la ruta completa de escena del componente, incluida la colección, el objeto de juego al que pertenece y el id del componente. En este ejemplo, usarías la URL `/go#camera` para identificar el componente Camera desde la misma colección, y `main:/go#camera` al acceder a una cámara desde una colección diferente o desde el render script.

![crear componente Camera](images/camera/create.png)

```lua
-- Acceder a una cámara desde un script en la misma colección:
camera.get_fov("/go#camera")

-- Acceder a una cámara desde un script en una colección diferente:
camera.get_fov("main:/go#camera")

-- Acceder a una cámara desde el render script:
render.set_camera("main:/go#camera")
```

En cada frame, el componente Camera que actualmente tiene el foco de cámara enviará un mensaje `set_view_projection` al socket `@render`:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. El mensaje enviado desde el componente Camera incluye una matriz de vista y una matriz de proyección.

El componente Camera proporciona al render script una matriz de proyección en perspectiva u ortográfica, según la propiedad *Orthographic Projection* de la cámara. La matriz de proyección también tiene en cuenta los planos de recorte cercano y lejano definidos, el campo de visión y la configuración de relación de aspecto de la cámara.

La matriz de vista proporcionada por la cámara define la posición y la orientación de la cámara. Una cámara con *Orthographic Projection* centrará la vista en la posición del objeto de juego al que está adjunta, mientras que una cámara con *Perspective Projection* tendrá la esquina inferior izquierda de la vista posicionada en el objeto de juego al que está adjunta.


### Render script

Al usar el render script por defecto, Defold definirá automáticamente la última cámara activada que debe usarse para renderizar. Antes de este cambio, un script en alguna parte del proyecto tenía que enviar explícitamente el mensaje `use_camera_projection` al renderer para notificarle que debían usarse la vista y la proyección de los componentes Camera. Esto ya no es necesario, pero todavía es posible hacerlo por compatibilidad con versiones anteriores.

Como alternativa, puedes definir en un render script una cámara específica que debe usarse para renderizar. Esto puede ser útil en casos donde necesitas controlar con mayor precisión qué cámara debe usarse para renderizar, por ejemplo en un juego multijugador.

```lua
-- render.set_camera usará automáticamente las matrices de vista y proyección
-- para cualquier renderizado que ocurra hasta que se llame a render.set_camera().
render.set_camera("main:/my_go#camera")
```

Para comprobar si una cámara está activa o no, puedes usar la función `get_enabled` de la [Camera API](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera):

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- la cámara está activada; úsala para renderizar.
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Para usar la función `set_camera` junto con frustum culling, necesitas pasar esto como una opción a la función:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Desplazar la cámara

Desplazas/mueves la cámara por el mundo del juego moviendo el objeto de juego al que está adjunto el componente Camera. El componente Camera enviará automáticamente una matriz de vista actualizada basada en la posición actual de la cámara en los ejes x e y.

### Hacer zoom con la cámara

Puedes acercar y alejar cuando usas una cámara en perspectiva moviendo el objeto de juego al que está adjunta la cámara a lo largo del eje z. El componente Camera enviará automáticamente una matriz de vista actualizada basada en la posición z actual de la cámara.

Puedes acercar y alejar cuando usas una cámara ortográfica cambiando la propiedad *Orthographic Zoom* de la cámara, ya sea en el editor o durante la ejecución:

```lua
-- En el modo Fixed, este es el zoom efectivo.
go.set("#camera", "orthographic_zoom", 2)
```

En los modos `Auto Fit` y `Auto Cover`, *Orthographic Zoom* se aplica sobre el zoom calculado automáticamente; no se ignora. Por ejemplo, define *Orthographic Mode* como `Auto Fit` y *Orthographic Zoom* como `1.25` en el editor para ajustar el área de diseño a la ventana y después acercar un 25% adicional. La configuración equivalente durante la ejecución es:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` devuelve el zoom calculado a partir de las dimensiones actuales de la ventana y del proyecto en los modos `Auto Fit` y `Auto Cover`. En el modo `Fixed` devuelve `1.0`. El mismo valor está disponible mediante la propiedad de componente de solo lectura `orthographic_auto_zoom`:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Al usar una cámara ortográfica, también puedes cambiar cómo se determina el zoom mediante la opción `Orthographic Mode` o por script:

```lua
-- obtener el modo actual (uno de camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- cambiar a auto-fit (contain) para mantener siempre visible toda el área de diseño
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- cambiar a auto-cover para asegurar que el área de diseño cubra la ventana
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- cambiar al modo fixed para usar orthographic_zoom sin ajuste automático
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Zoom adaptativo

El concepto detrás del zoom adaptativo es ajustar el valor de zoom de la cámara cuando la resolución de la pantalla cambia respecto de la resolución inicial definida en *game.project*.

Dos enfoques comunes para el zoom adaptativo son:

1. Zoom máximo - Calcula un valor de zoom tal que el contenido cubierto por la resolución inicial en *game.project* llene y se expanda más allá de los límites de la pantalla, posiblemente ocultando parte del contenido a los lados o arriba y abajo.
2. Zoom mínimo - Calcula un valor de zoom tal que el contenido cubierto por la resolución inicial en *game.project* quede completamente contenido dentro de los límites de la pantalla, posiblemente mostrando contenido adicional a los lados o arriba y abajo.

Ejemplo:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- zoom máximo: asegura que las dimensiones de diseño iniciales llenen y se expandan más allá de los límites de la pantalla
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- zoom mínimo: asegura que las dimensiones de diseño iniciales se reduzcan y queden contenidas dentro de los límites de la pantalla
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale

            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Puedes ver un ejemplo completo de zoom adaptativo en [este proyecto de ejemplo](https://github.com/defold/sample-adaptive-zoom).

Nota: Con una cámara ortográfica ahora puedes lograr el comportamiento contain/cover sin código personalizado definiendo `Orthographic Mode` como `Auto Fit` (contain) o `Auto Cover` (cover). En estos modos, el zoom calculado a partir del tamaño de la ventana y la resolución de diseño se multiplica por `Orthographic Zoom`.


### Seguir un objeto de juego

Puedes hacer que la cámara siga un objeto de juego estableciendo el objeto de juego al que está adjunto el componente Camera como hijo del objeto de juego que debe seguir:

![seguir objeto de juego](images/camera/follow.png)

Una forma alternativa es actualizar en cada frame la posición del objeto de juego al que está adjunto el componente Camera a medida que se mueve el objeto de juego que debe seguir.

### Conversión entre coordenadas de pantalla y del mundo {#converting-mouse-to-world-coordinates}

Cuando una cámara se ha desplazado, ha hecho zoom o ha cambiado su proyección, las coordenadas de entrada ya no coinciden directamente con las coordenadas del mundo. Usa las funciones de conversión de la cámara con `action.screen_x` y `action.screen_y`. Si se omite la URL de cámara opcional, se usa la última cámara activada.

Para una cámara ortográfica, [`camera.screen_xy_to_world()`](/ref/camera/#camera.screen_xy_to_world:x-y-[camera]) devuelve el punto en el espacio del mundo situado en el plano cercano de la cámara para un píxel de pantalla:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local world_position = camera.screen_xy_to_world(
            action.screen_x, action.screen_y, "#camera")
        go.set_position(world_position, "/marker")
    end
end
```

Para una cámara en perspectiva, [`camera.screen_to_world()`](/ref/camera/#camera.screen_to_world:pos-[camera]) recibe un `vector3` cuyo componente Z es la profundidad de vista en unidades del mundo, medida desde el plano de la cámara:

```lua
local depth = 10
local world_position = camera.screen_to_world(
    vmath.vector3(action.screen_x, action.screen_y, depth), "#camera")
```

[`camera.world_to_screen()`](/ref/camera/#camera.world_to_screen:world_pos-[camera]) realiza la conversión inversa. Devuelve X e Y en píxeles de pantalla y usa en Z la misma convención de profundidad de vista, por lo que el resultado puede pasarse de nuevo a `camera.screen_to_world()`:

```lua
-- Update the cached world transform first if the object moved this frame.
go.update_world_transform("/marker")
local world_position = go.get_world_position("/marker")
local screen_position = camera.world_to_screen(world_position, "#camera")
```

Visita la [página de ejemplos](https://defold.com/examples/render/screen_to_world/) para ver la conversión de coordenadas en acción. También hay un [proyecto de ejemplo](https://github.com/defold/sample-screen-to-world-coordinates/) que muestra las mismas API.

::: sidenote
Las [soluciones de cámara de terceros mencionadas en este manual](/manuals/camera/#third-party-camera-solutions) proporcionan funciones para convertir hacia y desde coordenadas de pantalla.
:::

## Manipulación en runtime
Puedes manipular cámaras en runtime mediante varios mensajes y propiedades diferentes (consulta la [documentación de la API para el uso](/ref/camera/)).

Una cámara tiene varias propiedades diferentes que pueden manipularse con `go.get()` y `go.set()`:

`fov`
: El campo de visión de la cámara (`number`).

`near_z`
: El valor Z cercano de la cámara (`number`).

`far_z`
: El valor Z lejano de la cámara (`number`).

`orthographic_zoom`
: El multiplicador de zoom de la cámara ortográfica controlado por el usuario. En los modos `Auto Fit` y `Auto Cover` se multiplica por `orthographic_auto_zoom`. (`number`).

`orthographic_auto_zoom`
: El zoom ortográfico calculado para los modos `Auto Fit` y `Auto Cover`, o `1.0` en el modo `Fixed`. READ ONLY. (`number`).

`aspect_ratio`
: La relación entre el ancho y la altura del frustum. Se usa al calcular la proyección de una cámara en perspectiva. (`number`).

`view`
: La matriz de vista calculada de la cámara. READ ONLY. (`matrix4`).

`projection`
: La matriz de proyección calculada de la cámara. READ ONLY. (`matrix4`).


## Soluciones de cámara de terceros {#third-party-camera-solutions}

Hay soluciones de cámara creadas por la comunidad que implementan funcionalidades comunes como sacudida de pantalla, seguimiento de objetos de juego, conversión de coordenadas de pantalla a mundo y mucho más. Se pueden descargar desde el Defold asset portal:

- [Orthographic camera](https://defold.com/assets/orthographic/) (solo 2D) por Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D y 3D) por Klayton Kowalski.
