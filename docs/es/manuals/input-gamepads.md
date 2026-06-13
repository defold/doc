---
title: Input de gamepad en Defold
brief: Este manual explica cómo funciona el input de gamepad.
---

::: sidenote
Se recomienda que te familiarices con la forma general en que funciona el input en Defold, cómo recibir input y en qué orden se recibe en tus archivos script. Aprende más sobre el sistema de input en el [manual de visión general del input](/manuals/input).
:::

# Gamepads {#gamepads}
Los triggers de gamepad permiten vincular input de gamepad estándar a funciones del juego. El input de gamepad ofrece bindings para:

- Sticks izquierdo y derecho (dirección y clicks)
- Pads digitales izquierdo y derecho. El pad derecho normalmente se traduce a los botones "A", "B", "X" e "Y" del mando Xbox, y a los botones "cuadrado", "círculo", "triángulo" y "cruz" del mando PlayStation.
- Gatillos izquierdo y derecho
- Botones superiores izquierdo y derecho
- Botones Start, Back y Guide

![](images/input/gamepad_bindings.png)

::: important
Los ejemplos siguientes usan las acciones mostradas en la imagen anterior. Como con todo input, puedes nombrar tus acciones de input como quieras.
:::

## Botones digitales {#digital-buttons}
Los botones digitales generan eventos `pressed`, `released` y `repeated`. Ejemplo que muestra cómo detectar input para un botón digital (presionado o soltado):

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- empezar a moverse hacia la izquierda
        elseif action.released then
            -- dejar de moverse hacia la izquierda
        end
    end
end
```

## Sticks analógicos {#analog-sticks}
Los sticks analógicos generan eventos de input continuos cuando el stick se mueve fuera de la zona muerta definida en el archivo de configuración de gamepads (ver abajo). Ejemplo que muestra cómo detectar input para un stick analógico:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- el stick izquierdo se movió hacia abajo
        print(action.value) -- un valor entre 0.0 y -1.0
    end
end
```

Los sticks analógicos también generan eventos `pressed` y `released` cuando se mueven en las direcciones cardinales por encima de cierto valor umbral. Esto facilita usar también un stick analógico como input direccional digital:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- el stick izquierdo se movió hasta su posición inferior extrema
    end
end
```

## Múltiples gamepads {#multiple-gamepads}
Defold admite múltiples gamepads a través del sistema operativo host; las acciones establecen el campo `gamepad` de la tabla de acción con el número del gamepad del que se originó el input:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- el gamepad 0 quiere unirse al juego
        end
    end
end
```

## Conexión y desconexión {#connect-and-disconnect}
Los bindings de input de gamepad también proporcionan dos bindings separados llamados `Connected` y `Disconnected` para detectar cuándo un gamepad se conecta (incluso los conectados desde el inicio) o se desconecta.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- el gamepad 0 se conectó
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- el gamepad 0 se desconectó
        end
    end
end
```

## Gamepads raw {#raw-gamepads}

Los bindings de input de gamepad también proporcionan un binding separado llamado `Raw` para dar el input de botones, ejes y hats sin filtrar (sin aplicar la zona muerta) de cualquier gamepad conectado.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Archivo de configuración de gamepads {#gamepads-settings-file}
La configuración del input de gamepad usa un archivo de mapeo separado para cada tipo de hardware de gamepad. Los mapeos de gamepads para hardware específico se definen en un archivo *gamepads*. Defold incluye un archivo gamepads integrado con configuraciones para gamepads comunes:

![Configuración de gamepads](images/input/gamepads.png)

Si necesitas crear un nuevo archivo de configuración de gamepads, tenemos una herramienta simple para ayudarte:

[Haz click para descargar gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Incluye binarios para Windows, Linux y macOS. Ejecútala desde la línea de comando:

```sh
./gdc
```

La herramienta te pedirá que presiones distintos botones en tu mando conectado. Luego generará un nuevo archivo gamepads con los mapeos correctos para tu mando. Guarda el archivo nuevo, o combínalo con tu archivo gamepads existente, y luego actualiza la configuración en *game.project*:

![Configuración de gamepads](images/input/gamepad_setting.png)

### Gamepads no identificados {#unidentified-gamepads}

Cuando se conecta un gamepad y no existe ningún mapeo para él, el gamepad solo generará acciones "connected", "disconnected" y "raw". En este caso necesitas mapear manualmente los datos raw del gamepad a acciones en tu juego.

Es posible comprobar si una acción de input para un gamepad proviene de un gamepad desconocido o no leyendo el valor `gamepad_unknown` de la acción:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
```

## Gamepads en HTML5 {#gamepads-in-html5}
Los gamepads son compatibles con builds HTML5 y generan los mismos eventos de input que en otras plataformas. El soporte de gamepads se basa en la [Gamepad API](https://www.w3.org/TR/gamepad/), que es compatible con la mayoría de los navegadores ([consulta esta tabla de soporte](https://caniuse.com/?search=gamepad)). Si el navegador no admite la Gamepad API, Defold ignorará silenciosamente cualquier trigger de Gamepad en tu proyecto. Puedes comprobar si el navegador admite la Gamepad API revisando si la función `getGamepads` existe en el objeto `navigator`:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Si tu juego se ejecuta dentro de un `iframe`, también debes asegurarte de que el `iframe` tenga añadido el permiso `gamepad`:

```html
<iframe allow="gamepad"></iframe>
```

### Gamepad estándar {#standard-gamepad}

Si el navegador identifica un gamepad conectado como gamepad estándar, usará el mapeo para "Standard Gamepad" en el [archivo de configuración de gamepads](/manuals/input-gamepads/#gamepads-settings-file) (el archivo `default.gamepads` en `/builtins` incluye un mapeo de Standard Gamepad). Un gamepad estándar se define como un dispositivo con 16 botones y 2 sticks analógicos, con una disposición de botones similar a un mando PlayStation o Xbox (consulta la [definición y disposición de botones de W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad) para más información). Si el gamepad conectado no se identifica como un gamepad estándar, Defold buscará en el archivo de configuración de gamepads un mapeo que coincida con el tipo de hardware del gamepad.

## Gamepads en Windows {#gamepads-on-windows}
En Windows, actualmente solo se admiten mandos Xbox 360. Para conectar tu mando 360 a tu computadora Windows, [asegúrate de que esté configurado correctamente](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepads en Android {#gamepads-on-android}

Los gamepads son compatibles con builds Android y generan los mismos eventos de input que en otras plataformas. El soporte de gamepads se basa en el [sistema de input de Android para eventos de tecla y movimiento](https://developer.android.com/training/game-controllers/controller-input). Los eventos de input de Android se traducirán a eventos de gamepad de Defold usando el mismo archivo *gamepad* descrito arriba.

Al agregar bindings de gamepad adicionales en Android, puedes usar las siguientes tablas de consulta para traducir los eventos de input de Android a valores del archivo *gamepad*:

| Evento de tecla a índice de botón | Índice |
|-----------------------------------|--------|
| `AKEYCODE_BUTTON_A`               | 0      |
| `AKEYCODE_BUTTON_B`               | 1      |
| `AKEYCODE_BUTTON_C`               | 2      |
| `AKEYCODE_BUTTON_X`               | 3      |
| `AKEYCODE_BUTTON_L1`              | 4      |
| `AKEYCODE_BUTTON_R1`              | 5      |
| `AKEYCODE_BUTTON_Y`               | 6      |
| `AKEYCODE_BUTTON_Z`               | 7      |
| `AKEYCODE_BUTTON_L2`              | 8      |
| `AKEYCODE_BUTTON_R2`              | 9      |
| `AKEYCODE_DPAD_CENTER`            | 10     |
| `AKEYCODE_DPAD_DOWN`              | 11     |
| `AKEYCODE_DPAD_LEFT`              | 12     |
| `AKEYCODE_DPAD_RIGHT`             | 13     |
| `AKEYCODE_DPAD_UP`                | 14     |
| `AKEYCODE_BUTTON_START`           | 15     |
| `AKEYCODE_BUTTON_SELECT`          | 16     |
| `AKEYCODE_BUTTON_THUMBL`          | 17     |
| `AKEYCODE_BUTTON_THUMBR`          | 18     |
| `AKEYCODE_BUTTON_MODE`            | 19     |
| `AKEYCODE_BUTTON_1`               | 20     |
| `AKEYCODE_BUTTON_2`               | 21     |
| `AKEYCODE_BUTTON_3`               | 22     |
| `AKEYCODE_BUTTON_4`               | 23     |
| `AKEYCODE_BUTTON_5`               | 24     |
| `AKEYCODE_BUTTON_6`               | 25     |
| `AKEYCODE_BUTTON_7`               | 26     |
| `AKEYCODE_BUTTON_8`               | 27     |
| `AKEYCODE_BUTTON_9`               | 28     |
| `AKEYCODE_BUTTON_10`              | 29     |
| `AKEYCODE_BUTTON_11`              | 30     |
| `AKEYCODE_BUTTON_12`              | 31     |
| `AKEYCODE_BUTTON_13`              | 32     |
| `AKEYCODE_BUTTON_14`              | 33     |
| `AKEYCODE_BUTTON_15`              | 34     |
| `AKEYCODE_BUTTON_16`              | 35     |

([definiciones de Android `KeyEvent`](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Evento de movimiento a índice de eje | Índice |
|--------------------------------------|--------|
| `AMOTION_EVENT_AXIS_X`               | 0      |
| `AMOTION_EVENT_AXIS_Y`               | 1      |
| `AMOTION_EVENT_AXIS_Z`               | 2      |
| `AMOTION_EVENT_AXIS_RZ`              | 3      |
| `AMOTION_EVENT_AXIS_LTRIGGER`        | 4      |
| `AMOTION_EVENT_AXIS_RTRIGGER`        | 5      |
| `AMOTION_EVENT_AXIS_HAT_X`           | 6      |
| `AMOTION_EVENT_AXIS_HAT_Y`           | 7      |

([definiciones de Android `MotionEvent`](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Usa esta tabla de consulta junto con una app de prueba de gamepad de Google Play Store para averiguar a qué evento de tecla está mapeado cada botón de tu gamepad.
