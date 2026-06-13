---
title: Scripts GUI en Defold
brief: Este manual explica los scripts GUI.
---

# Scripts GUI

Para controlar la lógica de tu GUI y animar nodos, usas scripts Lua. Los scripts GUI funcionan igual que los scripts normales de objetos de juego, pero se guardan como un tipo de archivo distinto y tienen acceso a un conjunto diferente de funciones: las funciones del módulo `gui`.

## Agregar un script a una GUI

Para agregar un script a una GUI, primero crea un archivo de script GUI haciendo <kbd>click derecho</kbd> en una ubicación del navegador *Assets* y seleccionando <kbd>New ▸ Gui Script</kbd> en el menú contextual.

El editor abre automáticamente el nuevo archivo de script. Está basado en una plantilla e incluye funciones de ciclo de vida vacías, igual que los scripts de objeto de juego:

```lua
function init(self)
   -- Agrega aquí el código de inicialización
   -- Elimina esta función si no la necesitas
end

function final(self)
   -- Agrega aquí el código de finalización
   -- Elimina esta función si no la necesitas
end

function update(self, dt)
   -- Agrega aquí el código de actualización
   -- Elimina esta función si no la necesitas
end

function on_message(self, message_id, message, sender)
   -- Agrega aquí el código de gestión de mensajes
   -- Elimina esta función si no la necesitas
end

function on_input(self, action_id, action)
   -- Agrega aquí el código de gestión de input
   -- Elimina esta función si no la necesitas
end

function on_reload(self)
   -- Agrega aquí el código de gestión de input
   -- Elimina esta función si no la necesitas
end
```

Para adjuntar el script a un componente GUI, abre el archivo de prototipo del componente GUI (también conocido como "prefabs" o "blueprints" en otros motores) y selecciona la raíz en *Outline* para mostrar las *Properties* de la GUI. Define la propiedad *Script* con el archivo de script.

![Script](images/gui-script/set_script.png)

Si el componente GUI se agregó a un objeto de juego en alguna parte de tu juego, el script se ejecutará ahora.

## El namespace "gui"

Los scripts GUI tienen acceso al namespace `gui` y a [todas las funciones del módulo `gui`](/ref/gui). El namespace `go` no está disponible, así que tendrás que separar la lógica de objetos de juego en componentes script y comunicarte entre los scripts GUI y los scripts de objetos de juego. Cualquier intento de usar las funciones `go` causará un error:

```lua
function init(self)
   local id = go.get_id()
end
```

```txt
ERROR:SCRIPT: /main/my_gui.gui_script:2: You can only access go.* functions and values from a script instance (.script file)
stack traceback:
   [C]: in function 'get_id'
   /main/my_gui.gui_script:2: in function </main/my_gui.gui_script:1>
```

## Paso de mensajes

Todo componente GUI con un script adjunto puede comunicarse con otros objetos en el entorno de runtime de tu juego mediante paso de mensajes; se comportará como cualquier otro componente script.

Direccionas el componente GUI como lo harías con cualquier otro componente script:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![paso de mensajes](images/gui-script/message_passing.png)

## Direccionamiento de nodos

Los nodos GUI se pueden manipular mediante un script GUI adjunto al componente. Cada nodo debe tener un *Id* único configurado en el editor:

![paso de mensajes](images/gui-script/node_id.png)

El *Id* permite que un script obtenga una referencia al nodo y lo manipule con las [funciones del namespace `gui`](/ref/gui):

```lua
-- Amplía la barra de salud 10 unidades
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Nodos creados dinámicamente

Para crear un nodo nuevo mediante script en runtime tienes dos opciones. La primera opción es crear nodos desde cero llamando a las funciones `gui.new_[type]_node()`. Estas devuelven una referencia al nodo nuevo que puedes usar para manipularlo:

```lua
-- Crea un nuevo nodo caja
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- Crea un nuevo nodo de texto
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![nodo dinámico](images/gui-script/dynamic_nodes.png)

La forma alternativa de crear nodos nuevos es clonar un nodo existente con la función `gui.clone()` o un árbol de nodos con la función `gui.clone_tree()`:

```lua
-- Clona el nodo healthbar
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- Clona el árbol de nodos del botón
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- Obtiene la nueva raíz del árbol
local new_root = new_button_nodes["my_button"]

-- Mueve la raíz (y sus hijos) 300 a la derecha
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## Ids de nodos dinámicos

Los nodos creados dinámicamente no tienen un id asignado. Esto es intencional. Las referencias que devuelven `gui.new_[type]_node()`, `gui.clone()` y `gui.clone_tree()` son lo único necesario para poder acceder a los nodos, y debes llevar el seguimiento de esa referencia.

```lua
-- Agrega un nodo de texto
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contiene la referencia al nodo.
-- El nodo no tiene id, y está bien. No hay razón para hacer
-- gui.get_node() cuando ya tenemos la referencia.
```
