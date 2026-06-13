---
title: Input de dispositivos en Defold
brief: Este manual explica cómo funciona el input, cómo capturar acciones de input y crear reacciones interactivas en scripts.
---

# Input

Todo el input del usuario es capturado por el motor y se despacha como acciones a componentes script y scripts GUI en objetos de juego que han adquirido el foco de input y que implementan la función `on_input()`. Este manual explica cómo configurar bindings para capturar input y cómo crear código que responda a él.

El sistema de input usa un conjunto de conceptos simples y potentes que te permiten gestionar el input como mejor se adapte a tu juego.

![Bindings de input](images/input/overview.png)

Dispositivos
: Los dispositivos de input que forman parte de tu computadora o dispositivo móvil, o que están conectados a ellos, proporcionan input raw de nivel de sistema al runtime de Defold. Se admiten los siguientes tipos de dispositivos:

  1. Teclado (teclas individuales e input de texto)
  2. Mouse (posición, clicks de botones y acciones de rueda del mouse)
  3. Single-touch y multi-touch (en dispositivos iOS y Android, y HTML5 en móviles)
  4. Gamepads (según el soporte del sistema operativo y el mapeo en el archivo [gamepads](#gamepads-settings-file))

Bindings de input
: Antes de que el input se envíe a un script, el input raw del dispositivo se traduce en *acciones* significativas mediante la tabla de bindings de input.

Acciones
: Las acciones se identifican por los nombres (convertidos en hash) que enumeras en el archivo de bindings de input. Cada acción también contiene datos relevantes sobre el input: si un botón se presionó o se soltó, las coordenadas del mouse y del toque, etc.

Listeners de input
: Cualquier componente script o script GUI puede recibir acciones de input al *adquirir el foco de input*. Varios listeners pueden estar activos al mismo tiempo.

Pila de input
: La lista de listeners de input, con el primer elemento que adquirió el foco en la parte inferior de la pila y el último en la parte superior.

Consumir input
: Un script puede elegir consumir el input que recibió, lo que impide que los listeners más abajo en la pila lo reciban.

## Configurar bindings de input

Los bindings de input son una tabla global del proyecto que te permite especificar cómo debe traducirse el input de dispositivos a *acciones* con nombre antes de que se despachen a tus componentes script y scripts GUI. Puedes crear un nuevo archivo de binding de input haciendo <kbd>click derecho</kbd> en una ubicación de la vista *Assets* y seleccionando <kbd>New... ▸ Input Binding</kbd>. Para hacer que el motor use el archivo nuevo, cambia la entrada *Game Binding* en *game.project*.

![Configuración de binding de input](images/input/setting.png)

Un archivo de binding de input predeterminado se crea automáticamente con todas las plantillas de proyecto nuevas, así que normalmente no necesitas crear un archivo de binding nuevo. El archivo predeterminado se llama "game.input_binding" y se encuentra en la carpeta "input" en la raíz del proyecto. Haz <kbd>doble click</kbd> en el archivo para abrirlo en el editor:

![Conjunto de bindings de input](images/input/input_binding.png)

Para crear un binding nuevo, haz click en el botón <kbd>+</kbd> en la parte inferior de la sección del tipo de trigger correspondiente. Cada entrada tiene dos campos:

*Input*
: El input raw que se escuchará, seleccionado desde una lista desplazable de inputs disponibles.

*Action*
: El nombre de acción dado a las acciones de input cuando se crean y despachan a tus scripts. El mismo nombre de acción se puede asignar a múltiples inputs. Por ejemplo, puedes vincular la tecla <kbd>Space</kbd> y el botón "A" del gamepad a la acción `jump`. Ten en cuenta que existe un bug conocido por el cual los inputs táctiles, lamentablemente, no pueden tener los mismos nombres de acción que otros inputs.

## Tipos de triggers

Hay cinco tipos de triggers específicos de dispositivo que puedes crear:

Triggers de teclas
: Input de teclado de una sola tecla. Cada tecla se mapea por separado a una acción correspondiente. Aprende más en el [manual de input de teclas y texto](/manuals/input-key-and-text).

Triggers de texto
: Los triggers de texto se usan para leer input de texto arbitrario. Aprende más en el [manual de input de teclas y texto](/manuals/input-key-and-text)

Triggers de mouse
: Input de botones del mouse y ruedas de desplazamiento. Aprende más en el [manual de input de mouse y touch](/manuals/input-mouse-and-touch).

Triggers de touch
: Los triggers de tipo Single-touch y Multi-touch están disponibles en dispositivos iOS y Android en aplicaciones nativas y en bundles HTML5. Aprende más en el [manual de mouse y touch](/manuals/input-mouse-and-touch).

Triggers de gamepad
: Los triggers de gamepad te permiten vincular input de gamepad estándar a funciones del juego. Aprende más en el [manual de gamepads](/manuals/input-gamepads).

### Input de acelerómetro

Además de los cinco tipos de triggers distintos enumerados arriba, Defold también admite input de acelerómetro en aplicaciones nativas de Android y iOS. Marca la casilla *Use Accelerometer* en la sección *Input* de tu archivo *game.project*.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- reaccionar a los datos del acelerómetro
    end
end
```

## Foco de input

Para escuchar acciones de input en un componente script o script GUI, se debe enviar el mensaje `acquire_input_focus` al objeto de juego que contiene el componente:

```lua
-- indica al objeto de juego actual (".") que adquiera el foco de input
msg.post(".", "acquire_input_focus")
```

Este mensaje indica al motor que agregue a la *pila de input* los componentes capaces de recibir input (componentes script, componentes GUI y proxies de colección) de los objetos de juego. Los componentes del objeto de juego se colocan en la parte superior de la pila de input; el componente que se agregue al final quedará en la parte superior de la pila. Ten en cuenta que si el objeto de juego contiene más de un componente capaz de recibir input, todos los componentes se agregarán a la pila:

![Pila de input](images/input/input_stack.png)

Si un objeto de juego que ya ha adquirido el foco de input lo vuelve a adquirir, sus componentes se moverán a la parte superior de la pila.


## Despacho de input y on_input()

Las acciones de input se despachan según la pila de input, de arriba hacia abajo.

![Despacho de acciones](images/input/actions.png)

A todo componente que esté en la pila y contenga una función `on_input()` se le llamará esa función, una vez por cada acción de input durante el frame, con los siguientes argumentos:

`self`
: La instancia de script actual.

`action_id`
: El nombre convertido en hash de la acción, según está configurado en los bindings de input.

`action`
: Una tabla que contiene los datos útiles sobre la acción, como el valor del input, su ubicación (posiciones absoluta y delta), si el input de botón fue `pressed`, etc. Consulta [on_input()](/ref/go#on_input) para ver detalles sobre los campos de acción disponibles.

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- mover a la izquierda
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- mover a la derecha
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Foco de input y componentes proxy de colección

Cada mundo de juego cargado dinámicamente mediante un proxy de colección tiene su propia pila de input. Para que el despacho de acciones alcance la pila de input del mundo cargado, el componente proxy debe estar en la pila de input del mundo principal. Todos los componentes en la pila de un mundo cargado se manejan antes de que el despacho continúe hacia abajo por la pila principal:

![Despacho de acciones a proxies](images/input/proxy.png)

::: important
Es un error común olvidar enviar `acquire_input_focus` al objeto de juego que contiene el componente proxy de colección. Omitir este paso impide que el input llegue a cualquiera de los componentes en la pila de input del mundo cargado.
:::


### Liberar foco de input

Para dejar de escuchar acciones de input, envía un mensaje `release_input_focus` al objeto de juego. Este mensaje eliminará de la pila de input todos los componentes del objeto de juego:

```lua
-- indica al objeto de juego actual (".") que libere el foco de input.
msg.post(".", "release_input_focus")
```


## Consumir input

La función `on_input()` de un componente puede controlar activamente si las acciones deben pasarse más abajo en la pila o no:

- Si `on_input()` devuelve `false`, o se omite el `return` (esto implica un retorno `nil`, que es un valor falso en Lua), las acciones de input se pasarán al siguiente componente de la pila de input.
- Si `on_input()` devuelve `true`, el input se consume. Ningún componente más abajo en la pila de input recibirá el input. Ten en cuenta que esto se aplica a *todas* las pilas de input. Un componente en la pila de un mundo cargado por proxy puede consumir input, lo que impide que los componentes en la pila principal reciban input:

![consumir input](images/input/consuming.png)

Hay muchos buenos casos de uso en los que consumir input proporciona una forma simple y potente de mover el input entre distintas partes de un juego. Por ejemplo, si necesitas un menú popup que temporalmente sea la única parte del juego que escucha input:

![consumir input](images/input/game.png)

El menú de pausa está inicialmente oculto (deshabilitado) y se habilita cuando el jugador toca el elemento HUD "PAUSE":

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- ¿El jugador presionó PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Indica al menú de pausa que tome el control.
            msg.post("pause_menu", "show")
        end
    end
end
```

![menú de pausa](images/input/game_paused.png)

El menú GUI de pausa adquiere el foco de input y consume input, lo que impide cualquier input que no sea relevante para el menú popup:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Muestra el menú de pausa.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Adquiere foco de input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- hacer cosas...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Oculta el menú de pausa
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Libera foco de input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume todo el input. Cualquier cosa por debajo de nosotros en la pila de input
  -- no verá input hasta que liberemos el foco de input.
  return true
end
```
