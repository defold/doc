---
title: Layouts de GUI en Defold
brief: Defold soporta GUIs que se adaptan automáticamente a cambios de orientación de pantalla en dispositivos móviles. Este documento explica cómo funciona esta funcionalidad.
---

# Layouts

Defold soporta GUIs que se adaptan automáticamente a cambios de orientación de pantalla en dispositivos móviles. Al usar esta funcionalidad puedes diseñar GUIs que se adapten a la orientación y la relación de aspecto de un rango de tamaños de pantalla. También es posible crear layouts que coincidan con modelos de dispositivo concretos.

## Crear perfiles de pantalla {#creating-display-profiles}

Por defecto, la configuración de *game.project* especifica que se usa un archivo integrado de configuración de perfiles de pantalla ("builtins/render/default.display_profiles"). Los perfiles predeterminados son "Landscape" (1280 píxeles de ancho y 720 píxeles de alto) y "Portrait" (720 píxeles de ancho y 1280 píxeles de alto). No se establece ningún modelo de dispositivo en los perfiles, por lo que coincidirán con cualquier dispositivo.

Para crear un nuevo archivo de configuración de perfiles, copia el de la carpeta "builtins" o haz <kbd>click derecho</kbd> en una ubicación adecuada en la vista *Assets* y selecciona <kbd>New... ▸ Display Profiles</kbd>. Dale un nombre adecuado al nuevo archivo y haz click en <kbd>Ok</kbd>.

El editor ahora abre el nuevo archivo para editarlo. Añade nuevos perfiles haciendo click en el <kbd>+</kbd> de la lista *Profiles*. Para cada perfil, añade un conjunto de calificadores (*qualifiers*) para el perfil:

Width
: El ancho en píxeles del calificador.

Height
: El alto en píxeles del calificador.

Device Models
: Una lista separada por comas de modelos de dispositivo. El modelo de dispositivo coincide con el inicio del nombre del modelo de dispositivo; por ejemplo, `iPhone10` coincidirá con los modelos "iPhone10,\*". Los nombres de modelo con comas deben ir entre comillas, es decir, `"iPhone10,3", "iPhone10,6"` coincide con los modelos iPhone X (consulta la [wiki de iPhone](https://www.theiphonewiki.com/wiki/Models)). Ten en cuenta que las únicas plataformas que informan un modelo de dispositivo al llamar a `sys.get_sys_info()` son Android e iOS. Otras plataformas devuelven una cadena vacía y, por lo tanto, nunca elegirán un perfil de pantalla que tenga un calificador de modelo de dispositivo.

![Nuevos perfiles de pantalla](images/gui-layouts/new_profiles.png)

También necesitas especificar que el motor debe usar tus nuevos perfiles. Abre *game.project* y selecciona el archivo de perfiles de pantalla en la configuración *Display Profiles* bajo *display*:

![Configuración](images/gui-layouts/settings.png)

Si quieres que el motor cambie automáticamente entre layouts verticales y horizontales cuando el dispositivo rote, marca la casilla *Dynamic Orientation*. El motor seleccionará dinámicamente un layout coincidente y también cambiará la selección si el dispositivo cambia de orientación.

### Selección automática de layout (Auto Layout Selection, Display Profiles)

El recurso Display Profiles tiene una opción "Auto Layout Selection" (ON por defecto). Cuando está en ON, el motor selecciona automáticamente el layout de GUI con mejor coincidencia tanto cuando se crea la escena como cuando cambia el tamaño de la ventana/pantalla. Cuando está en OFF, el motor no cambiará layouts automáticamente; usa `gui.set_layout()` desde tu script GUI para cambiar layouts manualmente. Esta configuración se guarda en el archivo Display Profiles y afecta a todas las escenas GUI.

## Layouts de GUI

El conjunto actual de perfiles de pantalla puede usarse para crear variantes de layout de tu configuración de nodos GUI. Para añadir un nuevo layout a una escena GUI, haz click derecho en el icono *Layouts* de la vista *Outline* y selecciona <kbd>Add ▸ Layout ▸ ...</kbd>:

![Añadir layout a la escena](images/gui-layouts/add_layout.png)

Al editar una escena GUI, todos los nodos se editan en un layout concreto. El layout seleccionado actualmente se indica en el desplegable de layouts de la escena GUI en la barra de herramientas. Si no se elige ningún layout, los nodos se editan en el layout *Default*.

![Barra de herramientas de layouts](images/gui-layouts/toolbar.png)

![edición en vertical](images/gui-layouts/portrait.png)

Cada cambio que hagas en una propiedad de un nodo con un layout seleccionado _sobrescribe_ la propiedad con respecto al layout *Default*. Las propiedades sobrescritas se marcan en azul. Los nodos con propiedades sobrescritas también se marcan en azul. Puedes hacer click en el botón de restablecer junto a cualquier propiedad sobrescrita para restablecerla a su valor original.

![edición en horizontal](images/gui-layouts/landscape.png)

Un layout no puede eliminar ni crear nodos nuevos, solo sobrescribir propiedades. Si necesitas quitar un nodo de un layout, puedes mover el nodo fuera de la pantalla o eliminarlo con lógica de script. También debes prestar atención al layout seleccionado actualmente. Si añades un layout a tu proyecto, el nuevo layout se configurará de acuerdo con el layout seleccionado actualmente. Además, copiar y pegar nodos tiene en cuenta el layout seleccionado actualmente, tanto al copiar *como* al pegar.

## Selección dinámica de perfiles

Cuando Auto Layout Selection está activado, el motor selecciona automáticamente el layout con mejor coincidencia. La coincidencia dinámica de layout puntúa cada calificador de perfil de pantalla de acuerdo con las siguientes reglas:

1. Si no hay un modelo de dispositivo establecido, o si el modelo de dispositivo coincide, se calcula una puntuación (S) para el calificador.

2. La puntuación (S) se calcula con el área de la pantalla (A), el área del calificador (A_Q), la relación de aspecto de la pantalla (R) y la relación de aspecto del calificador (R_Q):

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. Se selecciona el perfil con el calificador de menor puntuación, si la orientación (horizontal o vertical) del calificador coincide con la pantalla.

4. Si no se encuentra ningún perfil con un calificador de la misma orientación, se selecciona el perfil con el calificador de mejor puntuación de la otra orientación.

5. Si no se puede seleccionar ningún perfil, se usa el perfil de respaldo *Default*.

Dado que el layout *Default* se usa como respaldo en runtime si no hay un layout con mejor coincidencia, esto significa que si añades un layout "Landscape", será la mejor coincidencia para *todas* las orientaciones hasta que también añadas un layout "Portrait".

## Mensajes de cambio de layout

Cuando cambia el layout, se envía un mensaje `layout_changed` al script del componente GUI. Esto ocurre cuando el motor cambia el layout automáticamente (Auto Layout Selection ON) o cuando tu script llama a `gui.set_layout()` y el layout cambia realmente. El mensaje contiene el identificador hash del layout para que el script pueda ejecutar lógica en función de qué layout está seleccionado:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- cambiando el layout a orientación horizontal
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- cambiando el layout a orientación vertical
  end
end
```

Además, el script de render actual recibe un mensaje cada vez que cambia la ventana (vista del juego), y esto incluye los cambios de orientación.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- Se redimensionó la ventana. message.width y message.height contienen las
    -- nuevas dimensiones de la ventana.
  end
end
```

Cuando se cambia la orientación, el administrador de layouts de GUI escalará y reposicionará automáticamente los nodos GUI según tu layout y las propiedades de los nodos. Sin embargo, el contenido dentro del juego se renderiza en una pasada separada (por defecto) con una proyección stretch-fit en la ventana actual. Para cambiar este comportamiento, proporciona tu propio script de render modificado o usa una [biblioteca](/assets/) de cámara.

## Selección manual de layout (Lua)

Cuando Auto Layout Selection está en OFF para los Display Profiles en uso, el motor no cambiará layouts automáticamente. Usa estas funciones desde un script GUI para gestionar layouts manualmente:

### gui.set_layout(layout)

- Acepta un string o hash (id de layout).
- Devuelve un booleano: `true` si el layout existe en la escena y se aplicó; `false` en caso contrario.
- Si el layout existe en Display Profiles, actualiza la resolución de la escena al ancho/alto del perfil.
- Emite `layout_changed` cuando el layout cambia realmente.

Ejemplo:

```lua
function init(self)
    -- Aplica manualmente el layout "Portrait"
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- Devuelve una tabla que mapea cada hash de id de layout a `vmath.vector3(width, height, 0)`.
- Para el layout predeterminado, devuelve la resolución actual de la escena.

Ejemplo:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Nota: Si existe un layout de GUI en la escena pero no está presente en Display Profiles, `gui.set_layout()` aún aplica las sobrescrituras de nodos por layout, pero no cambia la resolución de la escena.
