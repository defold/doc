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
Defold admite múltiples gamepads a través del sistema operativo host; las acciones establecen el campo `gamepad` de la tabla `action` con el número del gamepad del que se originó el input:

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

Las asignaciones de gamepad convierten los botones, ejes y crucetas de un mando en los controles estándar usados por tus input bindings. Defold combina dos fuentes de asignaciones configuradas en la sección *Input* de *game.project*:

| Ajuste | Formato de asignación | Valor predeterminado |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | Base de datos de texto en formato SDL, con correspondencia mediante el GUID del mando | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Entradas `.gamepads` heredadas para nombres de dispositivos y plataformas | `/builtins/input/default.gamepads` |

Las asignaciones de la base de datos SDL y las asignaciones automáticas de la plataforma usan [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone). Las entradas `.gamepads` heredadas definen sus propias zonas muertas. En Android, un mando sin entrada en la base de datos también puede recibir una [asignación automática](#gamepads-on-android).

### Asignaciones .gamepads heredadas {#legacy-gamepads-mappings}

Un archivo `.gamepads` puede contener asignaciones para varios mandos. Las asignaciones heredadas existentes siguen admitiéndose. Defold incluye asignaciones para mandos comunes en el archivo predeterminado:

![Configuración de gamepads](images/input/gamepads.png)

Si necesitas crear una asignación `.gamepads` heredada en una plataforma de escritorio, la siguiente herramienta puede ayudarte. Para Android, consulta [Gamepads en Android](#gamepads-on-android).

[Haz click para descargar gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Incluye binarios para Windows, Linux y macOS. Ejecútala desde la línea de comando:

```sh
./gdc
```

La herramienta te pedirá que presiones distintos botones en tu mando conectado. Luego generará un nuevo archivo gamepads con los mapeos correctos para tu mando. Guarda el archivo nuevo, o combínalo con tu archivo gamepads existente, y luego actualiza la configuración en *game.project*:

![Configuración de gamepads](images/input/gamepad_setting.png)

### Gamepads no identificados {#unidentified-gamepads}

Cuando no hay una asignación configurada ni una asignación automática de la plataforma, el gamepad solo genera las acciones vinculadas a `Connected`, `Disconnected` y `Raw`. Puedes agregar una asignación para el mando o procesar su input sin interpretar en tu juego.

Es posible comprobar si una acción de input para un gamepad proviene de un gamepad desconocido o no leyendo el valor `gamepad_unknown` de `action`:

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

Si el navegador identifica un gamepad conectado como gamepad estándar, usará el mapeo para `Standard Gamepad` en el [archivo de configuración de gamepads](/manuals/input-gamepads/#gamepads-settings-file) (el archivo `default.gamepads` en `/builtins` incluye un mapeo de `Standard Gamepad`). Un gamepad estándar se define como un dispositivo con 16 botones y 2 sticks analógicos, con una disposición de botones similar a un mando PlayStation o Xbox (consulta la [definición y disposición de botones de W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad) para más información). Si el gamepad conectado no se identifica como un gamepad estándar, Defold buscará en el archivo de configuración de gamepads un mapeo que coincida con el tipo de hardware del gamepad.

## Gamepads en Windows {#gamepads-on-windows}
En Windows, actualmente solo se admiten mandos Xbox 360. Para conectar tu mando 360 a tu computadora Windows, [asegúrate de que esté configurado correctamente](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepads en Android {#gamepads-on-android}

Los gamepads se admiten en builds de Android y generan las mismas acciones de input que en otras plataformas. Defold usa las [asignaciones de gamepad](#gamepads-settings-file) configuradas y puede asignar automáticamente algunos mandos que no tienen una entrada correspondiente.

Si no se identifica un mando o sus controles son incorrectos, pruébalo en el dispositivo Android y agrega o actualiza su asignación. Consulta [Gamepads no identificados](#unidentified-gamepads) y [Gamepads sin interpretar](#raw-gamepads) para resolver problemas.
