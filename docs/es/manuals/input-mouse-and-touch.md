---
title: Input de mouse y touch en Defold
brief: Este manual explica cómo funciona el input de mouse y touch.
---

::: sidenote
Se recomienda que te familiarices con la forma general en que funciona el input en Defold, cómo recibir input y en qué orden se recibe en tus archivos script. Aprende más sobre el sistema de input en el [manual de visión general del input](/manuals/input).
:::

# Triggers de mouse
Los triggers de mouse permiten vincular input de los botones del mouse y de las ruedas de desplazamiento a acciones del juego.

![](images/input/mouse_bindings.png)

::: sidenote
Los inputs de botones del mouse `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` y `MOUSE_BUTTON_MIDDLE` son equivalentes a `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` y `MOUSE_BUTTON_3`.
:::

::: important
Los ejemplos siguientes usan las acciones mostradas en la imagen anterior. Como con todo input, puedes nombrar tus acciones de input como quieras.
:::

## Botones del mouse
Los botones del mouse generan eventos `pressed`, `released` y `repeated`. Ejemplo que muestra cómo detectar input para el botón izquierdo del mouse (ya sea presionado o soltado):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- botón izquierdo del mouse presionado
        elseif action.released then
            -- botón izquierdo del mouse soltado
        end
    end
end
```

::: important
Las acciones de input `MOUSE_BUTTON_LEFT` (o `MOUSE_BUTTON_1`) también se envían para input de tipo Single-touch.
:::

## Rueda del mouse
El input de la rueda del mouse detecta acciones de desplazamiento. El campo `action.value` es `1` si la rueda se desplaza y `0` en caso contrario. (Las acciones de desplazamiento se tratan como si fueran pulsaciones de botón. Actualmente Defold no admite input de desplazamiento granular en paneles táctiles.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- la rueda del mouse se desplazó hacia arriba
        end
    end
end
```

## Movimiento del mouse
El movimiento del mouse se maneja por separado. Los eventos de movimiento del mouse no se reciben a menos que se configure al menos un trigger de mouse en tus input bindings.

El movimiento del mouse no se vincula en los input bindings, sino que `action_id` se establece en `nil` y la tabla `action` se rellena con la ubicación y el delta de movimiento de la posición del mouse.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- hacer que el objeto de juego siga el movimiento del mouse/touch
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Triggers de touch
Los triggers de tipo Single-touch y Multi-touch están disponibles en dispositivos iOS y Android en aplicaciones nativas y en bundles HTML5.

![](images/input/touch_bindings.png)

## Single-touch
Los triggers de tipo Single-touch no se configuran desde la sección Touch Triggers de los input bindings. En su lugar, **los triggers Single-touch se configuran automáticamente cuando tienes input de botón del mouse configurado para `MOUSE_BUTTON_LEFT` o `MOUSE_BUTTON_1`**.

## Multi-touch
Los triggers de tipo Multi-touch rellenan una tabla en la tabla de acción llamada `touch`. Los elementos de la tabla tienen índices enteros con números `1`--`N`, donde `N` es el número de puntos táctiles. Cada elemento de la tabla contiene campos con datos de input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Crear una instancia en cada punto táctil
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
A Multi-touch no debe asignársele la misma acción que al input de botón del mouse para `MOUSE_BUTTON_LEFT` o `MOUSE_BUTTON_1`. Asignar la misma acción sobrescribirá en la práctica Single-touch e impedirá que recibas eventos Single-touch.
:::

::: sidenote
El [asset Defold-Input](https://defold.com/assets/defoldinput/) puede usarse para configurar fácilmente controles virtuales en pantalla, como botones y sticks analógicos, con soporte para multi touch.
:::


## Detectar clicks o toques en objetos
Detectar cuándo el usuario ha hecho click o ha tocado un componente visual es una operación muy común que se necesita en muchos juegos. Puede ser la interacción del usuario con un botón u otro elemento de interfaz, o la interacción con un objeto de juego, como una unidad controlada por el jugador en un juego de estrategia, un tesoro en un nivel de un dungeon crawler o un personaje que entrega misiones en un RPG. El enfoque a usar varía según el tipo de componente visual.

### Detectar interacción con nodos GUI
Para los elementos de interfaz existe la función `gui.pick_node(node, x, y)`, que devolverá `true` o `false` según si la coordenada especificada está dentro de los límites de un nodo GUI. Consulta la [documentación de la API](/ref/gui/#gui.pick_node:node-x-y), el [ejemplo de pointer over](/examples/gui/pointer_over/) o el [ejemplo de botón](/examples/gui/button/) para aprender más.

### Detectar interacción con objetos de juego
Para los objetos de juego es más complicado detectar la interacción, ya que elementos como la traslación de la cámara y la proyección del script de render afectan los cálculos requeridos. Hay dos enfoques generales para detectar interacción con objetos de juego:

  1. Rastrear la posición y el tamaño de los objetos de juego con los que el usuario puede interactuar y comprobar si la coordenada del mouse o touch está dentro de los límites de alguno de los objetos.
  2. Adjuntar objetos de colisión a los objetos de juego con los que el usuario puede interactuar, y un objeto de colisión que siga al mouse o al dedo, y comprobar las colisiones entre ellos.

::: sidenote
Una solución lista para usar que utiliza objetos de colisión para detectar input del usuario con soporte para arrastrar y hacer click se puede encontrar en el [asset Defold-Input](https://defold.com/assets/defoldinput/).
:::

En ambos casos es necesario convertir entre las coordenadas de espacio de pantalla del evento de mouse o touch y las coordenadas de espacio del mundo de los objetos de juego. Esto se puede hacer de un par de formas distintas:

  * Mantén manualmente un registro de qué vista y proyección usa el script de render y usa esto para convertir hacia y desde el espacio del mundo. Consulta el [manual de cámara para ver un ejemplo de esto](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Usa una [solución de cámara de terceros](/manuals/camera/#third-party-camera-solutions) y aprovecha las funciones proporcionadas de conversión de pantalla a mundo.
