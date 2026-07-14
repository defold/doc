---
title: Scripts del editor
brief: Este manual explica cómo extender el editor usando Lua
---

# Scripts del editor {#editor-scripts}

Puedes crear elementos de menú personalizados y hooks de ciclo de vida del editor usando archivos Lua con una extensión especial: `.editor_script`. Con este sistema, puedes ajustar el editor para mejorar tu flujo de trabajo de desarrollo.

## Tiempo de ejecución de scripts del editor {#editor-script-runtime}

Los scripts del editor se ejecutan dentro del editor, en una VM Lua emulada por la VM Java. Todos los scripts comparten el mismo entorno único, lo que significa que pueden interactuar entre sí. Puedes cargar módulos Lua con `require`, igual que con los archivos `.script`, pero la versión de Lua que se ejecuta dentro del editor es diferente, así que asegúrate de que tu código compartido sea compatible. El editor usa Lua versión 5.2.x, más específicamente el runtime [luaj](https://github.com/luaj/luaj), que actualmente es la única solución viable para ejecutar Lua en la JVM. Además, hay algunas restricciones:
- no existe el paquete `debug`;
- no existe `os.execute`, aunque proporcionamos un `editor.execute()` similar;
- no existen `os.tmpname` ni `io.tmpfile`; actualmente los scripts del editor solo pueden acceder a archivos dentro del directorio del proyecto;
- actualmente no existe `os.rename`, aunque queremos agregarlo;
- no existen `os.exit` ni `os.setlocale`.
- no está permitido usar algunas funciones de larga duración en contextos donde el editor necesita una respuesta inmediata del script; consulta [Modos de ejecución](#execution-modes) para más detalles.

Todas las extensiones del editor definidas en scripts del editor se cargan cuando abres un proyecto. Cuando obtienes bibliotecas, las extensiones se recargan, ya que podría haber nuevos scripts del editor en las bibliotecas de las que dependes. Durante esta recarga no se incorporan cambios en tus propios scripts del editor, porque podrías estar modificándolos en ese momento. Para recargarlos también, ejecuta el comando **Project → Reload Editor Scripts**.

## Anatomía de `.editor_script` {#anatomy-of-editor_script}

Cada script del editor debe devolver un módulo, así:
```lua
local M = {}

function M.get_commands()
  -- TODO - definir comandos del editor
end

function M.get_language_servers()
  -- TODO - definir servidores de lenguaje
end

function M.get_prefs_schema()
  -- TODO - definir preferencias
end

return M
```
Luego el editor recopila todos los scripts del editor definidos en el proyecto y las bibliotecas, los carga en una sola VM Lua y los llama cuando es necesario (más sobre esto en las secciones [comandos](#commands) y [hooks de ciclo de vida](#lifecycle-hooks)).

## API del editor {#editor-api}

Puedes interactuar con el editor usando el paquete `editor`, que define esta API:
- `editor.platform` — un string, ya sea `"x86_64-win32"` para Windows, `"x86_64-macos"` para macOS o `"x86_64-linux"` para Linux.
- `editor.version` — un string, el nombre de versión de Defold, por ejemplo `"1.4.8"`
- `editor.engine_sha1` — un string, el SHA1 del motor Defold
- `editor.editor_sha1` — un string, el SHA1 del editor Defold
- `editor.get(node_id, property)` — obtiene un valor de algún nodo dentro del editor. Los nodos del editor son varias entidades, como archivos script o de colección, objetos de juego dentro de colecciones, archivos json cargados como recursos, etc. `node_id` es un userdata que el editor pasa al script del editor. Como alternativa, puedes pasar la ruta del recurso en lugar del id del nodo, por ejemplo `"/main/game.script"`. `property` es un string. Actualmente se soportan estas propiedades:
  - `"path"` — ruta de archivo desde la carpeta del proyecto para *recursos*, es decir, entidades que existen como archivos o directorios. Ejemplo de valor devuelto: `"/main/game.script"`
  - `"children"` — lista de rutas de recursos hijos para recursos de directorio
  - `"parent"` — nodo padre del editor para un nodo de Outline que tenga padre
  - `"text"` — contenido textual de un recurso editable como texto (como archivos script o json). Ejemplo de valor devuelto: `"function init(self)\nend"`. Ten en cuenta que esto no es lo mismo que leer el archivo con `io.open()`, porque puedes editar un archivo sin guardarlo, y esas ediciones solo están disponibles al acceder a la propiedad `"text"`.
  - para atlas: `images` (lista de nodos del editor para imágenes en el atlas) y `animations` (lista de nodos de animación)
  - para animaciones de atlas: `images` (igual que `images` en el atlas)
  - para tilemaps: `layers` (lista de nodos del editor para capas en el tilemap)
  - para capas de tilemap: `tiles` (una cuadrícula 2d ilimitada de tiles); consulta `tilemap.tiles.*` para más información
  - para particlefx: `emitters` (lista de nodos de emisor del editor) y `modifiers` (lista de nodos de modificador del editor)
  - para emisores particlefx: `modifiers` (lista de nodos de modificador del editor)
  - para objetos de colisión: `shapes` (lista de nodos del editor de formas de colisión)
  - para archivos GUI: listas de nodos como `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` y `layouts`
  - algunas propiedades que se muestran en la vista Properties cuando tienes algo seleccionado en la vista Outline. Se soportan estos tipos de propiedades de outline:
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Ten en cuenta que algunas de estas propiedades podrían ser de solo lectura, y algunas podrían no estar disponibles en distintos contextos, así que debes usar `editor.can_get` antes de leerlas y `editor.can_set` antes de hacer que el editor las defina. Pasa el cursor sobre el nombre de la propiedad en la vista Properties para ver un tooltip con información sobre cómo se nombra esta propiedad en los scripts del editor. Puedes definir propiedades de recurso como `nil` proporcionando el valor `""`.
- `editor.properties(node_id)` — devuelve una lista ordenada y dependiente del contexto con los nombres de las propiedades que pueden leerse de un nodo, por ejemplo `pprint(editor.properties("/game.project"))`. Usa las funciones `editor.can_*` para comprobar si una propiedad enumerada también puede modificarse, restablecerse, recibir elementos o reordenarse.
- `editor.can_get(node_id, property)` — comprueba si puedes obtener esta propiedad para que `editor.get()` no genere un error.
- `editor.can_set(node_id, property)` — comprueba si un paso de transacción `editor.tx.set()` con esta propiedad no generará un error.
- `editor.create_directory(resource_path)` — crea un directorio si no existe, junto con todos los directorios padre inexistentes.
- `editor.create_resources(resources)` — crea 1 o más recursos, ya sea desde plantillas o con contenido personalizado
- `editor.delete_directory(resource_path)` — elimina un directorio si existe, junto con todos los directorios y archivos hijos existentes.
- `editor.execute(cmd, [...args], [options])` — ejecuta un comando de shell y, opcionalmente, captura su salida.
- `editor.save()` — persiste en disco todos los cambios no guardados.
- `editor.transact(txs)` — modifica el estado en memoria del editor usando 1 o más pasos de transacción creados con funciones `editor.tx.*`.
- `editor.ui.*` — varias funciones relacionadas con la interfaz; consulta el [manual de UI](/manuals/editor-scripts-ui).
- `editor.prefs.*` — funciones para interactuar con las preferencias del editor; consulta [preferencias](#preferences).

Puedes encontrar la referencia completa de la API del editor [aquí](/ref/stable/editor/).

## Comandos {#commands}

Si un módulo de script del editor define `get_commands()`, se llama cuando se recargan las extensiones. Los comandos devueltos pueden aparecer en los menús de la barra de menús y en los menús contextuales de Assets, Outline, Scene y Code, según sus `locations`. Ejemplo:
```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
El editor espera que `get_commands()` devuelva un array de tablas, cada una describiendo un comando separado. La descripción de un comando consiste en:

- `label` (obligatorio) — texto de un elemento de menú que se mostrará al usuario
- `locations` (obligatorio) — un array que describe dónde debe estar disponible el comando. Los valores admitidos son `"Edit"`, `"View"`, `"Project"`, `"Debug"` y `"Help"` para los menús correspondientes de la barra de menús; `"Bundle"` para el submenú **Project → Bundle**; y `"Assets"`, `"Outline"`, `"Scene"` y `"Code"` para los menús contextuales correspondientes.
- `query` — una forma para que el comando pida al editor información relevante y defina sobre qué datos opera. Por cada clave en la tabla `query` habrá una clave correspondiente en la tabla `opts` que los callbacks `active` y `run` reciben como argumento. Claves soportadas:
  - `selection` significa que este comando es válido cuando hay algo seleccionado, y opera sobre esa selección.
    - `type` es un tipo de nodos seleccionados en el que el comando está interesado; actualmente se permiten estos tipos:
      - `"resource"` — en Assets y Outline, un recurso es el elemento seleccionado que tiene un archivo correspondiente. En la barra de menú (Edit o View), un recurso es el archivo abierto actualmente;
      - `"outline"` — algo que puede mostrarse en Outline. En Outline es un elemento seleccionado; en la barra de menú es el archivo abierto actualmente;
      - `"scene"` — algo que puede renderizarse en Scene.
    - `cardinality` define cuántos elementos seleccionados debe haber. Si es `"one"`, la selección pasada al callback del comando será un solo id de nodo. Si es `"many"`, la selección pasada al callback del comando será un array de uno o más ids de nodo.
  - `active_view` significa que este comando es válido cuando la vista activa del editor coincide con el tipo solicitado. La vista activa se pasa al callback del comando como `opts.active_view`.
    - `type` es el tipo de vista activa en el que el comando está interesado: `"code"`, `"scene"`, `"html"` o `"form"`.
    - La vista activa soporta las propiedades `"type"`, `"resource"` y `"dirty"`. Usa `editor.get(view, "resource")` para obtener el recurso mostrado en la vista, y `editor.get(view, "dirty")` para comprobar si tiene cambios sin guardar.
  - `argument` — argumento del comando. Actualmente, solo los comandos en la ubicación `"Bundle"` reciben un argumento, que es `true` cuando el comando de bundle se selecciona explícitamente y `false` al volver a crear el bundle.
- `id` - string identificador del comando, usado por ejemplo para persistir el último comando de bundle usado en `prefs`
- `active` - un callback que se ejecuta para comprobar que el comando está activo; se espera que devuelva un booleano. Si `locations` incluye `"Assets"`, `"Scene"` u `"Outline"`, `active` se llamará al mostrar el menú de contexto. Si `locations` incluye `"Edit"` o `"View"`, `active` se llamará en cada interacción del usuario, como escribir en el teclado o hacer click con el mouse, así que asegúrate de que `active` sea relativamente rápido.
- `run` - un callback que se ejecuta cuando el usuario selecciona el elemento de menú.

### Usar comandos para cambiar el estado en memoria del editor {#use-commands-to-change-the-in-memory-editor-state}

Dentro del callback `run`, puedes consultar y cambiar el estado en memoria del editor. La consulta se hace usando la función `editor.get()`, con la que puedes preguntar al editor por el estado actual de los archivos y la selección (si usas `query = {selection = ...}`). Puedes obtener la propiedad `"text"` de los recursos editables como texto y también algunas propiedades mostradas en la vista Properties; pasa el cursor sobre el nombre de la propiedad para ver un tooltip con información sobre cómo se nombra esa propiedad en scripts del editor. Cambiar el estado del editor se hace usando `editor.transact()`, donde agrupas 1 o más modificaciones en un único paso que se puede deshacer. Por ejemplo, si quieres poder restablecer la transformación de un objeto de juego, podrías escribir un comando así:
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position")
       and editor.can_set(node, "rotation")
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Usar comandos con la vista activa del editor {#use-commands-with-the-active-editor-view}

Los comandos en ubicaciones de menú como `"View"` pueden consultar la vista activa del editor. Esto es útil cuando un comando debe operar sobre el archivo o la escena que el usuario está viendo en ese momento:

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Editar atlas {#editing-atlases}

Además de leer y escribir propiedades de un atlas, puedes leer y modificar imágenes y animaciones del atlas. El atlas define las propiedades de lista de nodos `images` y `animations`, y las animaciones definen la propiedad de lista de nodos `images`: puedes usar los pasos de transacción `editor.tx.add`, `editor.tx.remove` y `editor.tx.clear` con estas propiedades.

Por ejemplo, para agregar una imagen a un atlas, ejecuta el siguiente código en el callback `run` del comando:
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Para encontrar el conjunto de todas las imágenes en un atlas, ejecuta el siguiente código:
```lua
local all_images = {} ---@type table<string, true>
-- primero, recopilar todas las imágenes "sueltas"
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- segundo, recopilar todas las imágenes usadas en animaciones
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
Para reemplazar todas las animaciones en un atlas:
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Editar tilesources {#editing-tilesources}

Además de las propiedades de outline, los tilesources definen las siguientes propiedades:
- `animations` - una lista de nodos de animación del tilesource
- `collision_groups` - una lista de nodos de grupo de colisión del tilesource
- `tile_collision_groups` - una tabla de asignaciones de grupo de colisión para tiles en el tilesource

Por ejemplo, así puedes configurar un tilesource:
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Editar tilemaps {#editing-tilemaps}

Los tilemaps definen la propiedad `layers`, una lista de nodos de capas de tilemap. Cada capa también define una propiedad `tiles` que contiene una cuadrícula 2d ilimitada de tiles en esa capa. Esto es diferente del motor: los tiles no tienen límites y se pueden agregar en cualquier lugar, incluidas coordenadas negativas. Para editar tiles, la API de scripts del editor define un módulo `tilemap.tiles` con las siguientes funciones:
- `tilemap.tiles.new()` para crear una estructura de datos nueva que contiene una cuadrícula 2d ilimitada de tiles (en el editor, a diferencia del motor, el tilemap es ilimitado y las coordenadas pueden ser negativas)
- `tilemap.tiles.get_tile(tiles, x, y)` para obtener un índice de tile en una coordenada específica
- `tilemap.tiles.get_info(tiles, x, y)` para obtener información completa del tile en una coordenada específica (la forma de los datos es la misma que en la función `tilemap.get_tile_info` del motor)
- `tilemap.tiles.iterator(tiles)` para crear un iterador sobre todos los tiles del tilemap
- `tilemap.tiles.clear(tiles)` para eliminar todos los tiles del tilemap
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` para definir un tile en una coordenada específica
- `tilemap.tiles.remove(tiles, x, y)` para eliminar un tile en una coordenada específica

Por ejemplo, así puedes imprimir el contenido de todo el tilemap:
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Aquí hay un ejemplo que muestra cómo agregar una capa con tiles a un tilemap:
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Editar particlefx {#editing-particlefx}

Puedes editar particlefx usando las propiedades `modifiers` y `emitters`. Por ejemplo, agregar un emisor circular con un modificador de aceleración se hace así:
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
Muchas propiedades particlefx son curvas o dispersiones de curva (es decir, curva + algún valor aleatorio). Las curvas se representan como una tabla con una lista no vacía de `points`, donde cada punto es una tabla con las siguientes propiedades:
- `x` - la coordenada x del punto, debe comenzar en 0 y terminar en 1
- `y` - el valor del punto
- `tx` (0 a 1) y `ty` (-1 a 1) - tangentes del punto. Por ejemplo, para un ángulo de 80 grados, `tx` debe ser `math.cos(math.rad(80))` y `ty` debe ser `math.sin(math.rad(80))`.
Las dispersiones de curva además tienen una propiedad numérica `spread`.

Por ejemplo, definir una curva alfa de vida de partícula para un emisor ya existente podría verse así:
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- empezar en 0, subir rápido
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- llegar a 1 al 20% de la vida
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- bajar lentamente a 0
    }})
})
```
Por supuesto, también es posible usar la clave `particle_key_alpha` en una tabla al crear un emisor. Además, puedes usar un solo número en su lugar para representar una curva "estática".

#### Editar objetos de colisión {#editing-collision-objects}

Además de las propiedades de outline predeterminadas, los objetos de colisión definen la propiedad de lista de nodos `shapes`. Agregar nuevas formas de colisión se hace así:
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- o "shape-type-sphere", "shape-type-capsule"
    })
})
```
La propiedad `type` de la forma es obligatoria durante la creación y no se puede cambiar después de agregar la forma. Hay 3 tipos de forma:
- `shape-type-box` - forma de caja con la propiedad `dimensions`
- `shape-type-sphere` - forma de esfera con la propiedad `diameter`
- `shape-type-capsule` - forma de cápsula con las propiedades `diameter` y `height`

#### Editar archivos GUI {#editing-gui-files}

Además de las propiedades de outline, los archivos GUI definen varias propiedades de listas de nodos:
- `layers` — lista de nodos de capa del editor (reordenable)
- `fonts` — lista de nodos de fuente del editor
- `materials` — lista de nodos de material del editor
- `textures` — lista de nodos de textura del editor
- `particlefxs` — lista de nodos Particle FX del editor
- `nodes` — lista de nodos GUI del editor
- `layouts` — lista de nodos de layout GUI del editor

Es posible editar capas GUI usando la propiedad `layers` del editor, por ejemplo:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Además, es posible reordenar capas:
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
De forma similar, las fuentes, materiales, texturas y particlefxs se editan usando las propiedades `fonts`, `materials`, `textures` y `particlefxs`:
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Estas propiedades no soportan reordenamiento.

Finalmente, puedes editar nodos GUI usando la propiedad de lista `nodes`, por ejemplo:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Los tipos de nodo integrados son:
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Si estás usando la extensión spine, también puedes usar el tipo de nodo `gui-node-type-spine`.

Si el archivo GUI define layouts, puedes obtener y definir los valores de layouts usando la sintaxis `layout:property`, por ejemplo:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- OBTENER:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- DEFINIR:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Las propiedades de layout que se definieron se pueden restablecer a sus valores predeterminados usando `editor.tx.reset`:
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Los árboles de nodos template se pueden leer, pero no editar; solo puedes definir propiedades de nodo del árbol de nodos template:
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (sobrescribe un valor del template)
```

#### Editar objetos de juego {#editing-game-objects}

Es posible editar componentes de un archivo de objeto de juego usando scripts del editor. Los componentes vienen en 2 variantes: referenciados e incrustados. Los componentes referenciados usan el tipo `component-reference` y actúan como referencias a otros recursos, permitiendo solo sobrescrituras de propiedades de objeto de juego definidas en scripts. Los componentes incrustados usan tipos como `sprite`, `label`, etc., y permiten editar todas las propiedades definidas en el tipo de componente, además de agregar subcomponentes como formas de objetos de colisión. Por ejemplo, puedes usar el siguiente código para configurar un objeto de juego:
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- definir una propiedad de objeto de juego definida en el script
    })
})
```

#### Editar colecciones {#editing-collections}
Es posible editar colecciones usando scripts del editor. Puedes agregar objetos de juego (incrustados o referenciados) y colecciones (referenciadas). Por ejemplo:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- objeto de juego incrustado
        type = "go",
        id = "root",
        children = {
            {
                -- objeto de juego referenciado
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- colección referenciada
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- los gos incrustados también pueden tener componentes
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- definir una propiedad de objeto de juego definida en el script
            }
        }
    })
})
```

Como en el editor, las colecciones referenciadas solo se pueden agregar a la raíz de la colección editada, y los objetos de juego solo se pueden agregar a objetos de juego incrustados o referenciados, pero no a colecciones referenciadas ni a objetos de juego dentro de esas colecciones referenciadas.

### Usar comandos de shell {#use-shell-commands}

Dentro del callback `run`, puedes escribir en archivos (usando el módulo `io`) y ejecutar comandos de shell (usando el comando `editor.execute()`). Al ejecutar comandos de shell, es posible capturar la salida de un comando de shell como un string y luego usarla en el código. Por ejemplo, si quieres crear un comando para formatear JSON que invoque el [`jq`](https://jqlang.github.io/jq/) instalado globalmente, puedes escribir el siguiente comando:
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- no recargar recursos porque jq no toca el disco
      out = "capture" -- devolver salida de texto en lugar de nada
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Como este comando invoca un programa de shell de una forma de solo lectura (y se lo notifica al editor usando `reload_resources = false`), obtienes el beneficio de hacer que esta acción se pueda deshacer.

::: sidenote
Si quieres distribuir tu script del editor como una biblioteca, quizá quieras incluir el programa binario para las plataformas del editor dentro de la dependencia. Consulta [Scripts del editor en bibliotecas](#editor-scripts-in-libraries) para más detalles sobre cómo hacerlo.
:::

## Hooks de ciclo de vida {#lifecycle-hooks}

Hay un archivo de script del editor tratado de forma especial: `hooks.editor_script`, ubicado en la raíz de tu proyecto, en el mismo directorio que *game.project*. Este y solo este script del editor recibirá eventos de ciclo de vida desde el editor. Ejemplo de ese archivo:
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Decidimos limitar los hooks de ciclo de vida a un solo archivo de script del editor porque el orden en el que ocurren los hooks de build es más importante que la facilidad para agregar otro paso de build. Los comandos son independientes entre sí, así que realmente no importa en qué orden se muestran en el menú; al final el usuario ejecuta un comando particular que seleccionó. Si fuera posible especificar hooks de build en diferentes scripts del editor, se crearía un problema: ¿en qué orden se ejecutan los hooks? Probablemente quieras crear checksums de contenido después de comprimirlo... Y tener un único archivo que establece el orden de los pasos de build llamando explícitamente a cada función de paso es una forma de resolver este problema.

Hooks de ciclo de vida existentes que `/hooks.editor_script` puede especificar:
- `on_build_started(opts)` — se ejecuta cuando el juego se construye para ejecutarse localmente o en algún objetivo remoto usando las opciones Project Build o Debug Start. Tus cambios aparecerán en el juego construido. Generar un error desde este hook abortará la build. `opts` es una tabla que contiene las siguientes claves:
  - `platform` — un string en formato `%arch%-%os%` que describe para qué plataforma se construye; actualmente siempre tiene el mismo valor que `editor.platform`.
- `on_build_finished(opts)` — se ejecuta cuando termina la build, sea exitosa o fallida. `opts` es una tabla con las siguientes claves:
  - `platform` — igual que en `on_build_started`
  - `success` — si la build fue exitosa, ya sea `true` o `false`
- `on_bundle_started(opts)` — se ejecuta cuando creas un bundle o una versión Build HTML5 de un juego. Igual que con `on_build_started`, los cambios disparados por este hook aparecerán en un bundle, y los errores abortarán un bundle. `opts` tendrá estas claves:
  - `output_directory` — una ruta de archivo que apunta a un directorio con la salida del bundle. **Project ▸ Build HTML5** usa su propio árbol de artefactos, por ejemplo `"/path/to/project/build/default_html5/__htmlLaunchDir"`, separado de la salida de Build normal ubicada en `build/default`.
  - `platform` — plataforma para la que se crea el bundle del juego. Consulta una lista de posibles valores de plataforma en el [manual de Bob](/manuals/bob).
  - `variant` — variante de bundle, ya sea `"debug"`, `"release"` o `"headless"`
- `on_bundle_finished(opts)` — se ejecuta cuando termina el bundle, sea exitoso o no. `opts` es una tabla con los mismos datos que `opts` en `on_bundle_started`, más la clave `success`, que indica si la build fue exitosa.
- `on_target_launched(opts)` — se ejecuta cuando el usuario lanzó un juego y este inició correctamente. `opts` contiene una clave `url` que apunta a un servicio del motor lanzado, por ejemplo, `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — se ejecuta cuando se cierra el juego lanzado; tiene los mismos opts que `on_target_launched`

Ten en cuenta que los hooks de ciclo de vida actualmente son una funcionalidad solo del editor, y Bob no los ejecuta al crear bundles desde la línea de comando.

## Servidores de lenguaje {#language-servers}

El editor admite un subconjunto del [Language Server Protocol](https://microsoft.github.io/language-server-protocol/): diagnósticos (lints), sugerencias de completado, información al pasar el cursor, símbolos del documento en el panel Structure, ir a la definición, buscar referencias y cambiar el nombre de símbolos. Pasa el cursor sobre un símbolo para ver información del servidor de lenguaje. Con el cursor sobre un símbolo, usa <kbd>F2</kbd> para cambiarle el nombre, <kbd>F12</kbd> para ir a su definición o <kbd>Shift+F12</kbd> para buscar referencias. Estas acciones también están disponibles en el menú <kbd>Edit</kbd>.

Para definir el servidor de lenguaje, necesitas editar la función `get_language_servers` de tu script del editor así:

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
El editor iniciará el servidor de lenguaje usando el `command` especificado, usando la entrada y salida estándar del proceso del servidor para la comunicación.

La tabla de definición de servidor de lenguaje puede especificar:
- `languages` (obligatorio) — una lista de lenguajes en los que el servidor está interesado, según se define [aquí](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (las extensiones de archivo también funcionan);
- `command` (obligatorio) - un array de comando y sus argumentos
- `watched_files` - un array de tablas con claves `pattern` (un glob) que activarán la notificación [watched files changed](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) del servidor.

## Servidor HTTP {#http-server}

Cada instancia en ejecución del editor tiene un servidor HTTP en ejecución. El servidor puede extenderse usando scripts del editor. Para extender el servidor HTTP del editor, necesitas agregar la función de script del editor `get_http_server_routes`; debe devolver las rutas adicionales:
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Después de recargar los scripts del editor, verás la siguiente salida en la consola: `My route: http://0.0.0.0:12345/my-extension`. Si abres este enlace en el navegador, verás tu mensaje `"Hello world!"`.

El argumento de entrada `request` es una tabla Lua simple con información sobre la solicitud. Contiene claves como `path` (segmento de ruta de URL que comienza con `/`), `method` de la solicitud (por ejemplo, `"GET"`), `headers` (una tabla con nombres de header en minúsculas) y, opcionalmente, `query` (el query string) y `body` (si la ruta define cómo interpretar el cuerpo). Por ejemplo, si quieres crear una ruta que acepte un cuerpo JSON, la defines con un parámetro convertidor `"json"`:
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Puedes probar este endpoint en la línea de comando usando `curl` y `jq`:
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
La ruta soporta patrones que pueden extraerse de la ruta de la solicitud y proporcionarse a la función manejadora como parte de la solicitud, por ejemplo:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Ahora, si abres por ejemplo `http://0.0.0.0:12345/my-extension/setting/project.title`, verás el título de tu juego tomado del archivo `/game.project`.

Además de un patrón de ruta de un solo segmento, también puedes hacer coincidir el resto de la ruta URL usando la sintaxis `{*name}`. Por ejemplo, aquí hay un endpoint de servidor de archivos simple que sirve archivos desde la raíz del proyecto:
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Ahora, al abrir por ejemplo `http://0.0.0.0:12345/my-extension/files/main/main.collection` en el navegador, se mostrará el contenido del archivo `main/main.collection`.

## Scripts del editor en bibliotecas {#editor-scripts-in-libraries}

Puedes publicar bibliotecas para que otras personas las usen que contengan comandos, y el editor las detectará automáticamente. Los hooks, en cambio, no pueden detectarse automáticamente, ya que tienen que definirse en un archivo que esté en la carpeta raíz de un proyecto, pero las bibliotecas solo exponen subcarpetas. Esto tiene la intención de dar más control sobre el proceso de build: aún puedes crear hooks de ciclo de vida como funciones simples en archivos `.lua`, para que los usuarios de tu biblioteca puedan requerirlos y usarlos en su `/hooks.editor_script`.

Ten en cuenta también que aunque las dependencias se muestran en la vista Assets, no existen como archivos (son entradas en un archivo zip). Es posible hacer que el editor extraiga algunos archivos de las dependencias a la carpeta `build/plugins/`. Para hacerlo, necesitas crear un archivo `ext.manifest` en la carpeta de tu biblioteca, y luego crear la carpeta `plugins/bin/${platform}` en la misma carpeta donde se encuentra el archivo `ext.manifest`. Los archivos de esa carpeta se extraerán automáticamente a la carpeta `/build/plugins/${extension-path}/plugins/bin/${platform}`, para que tus scripts del editor puedan referenciarlos.

## Preferencias {#preferences}

Los scripts del editor pueden definir y usar preferencias: piezas de datos persistentes y sin commit almacenadas en la computadora del usuario. Estas preferencias tienen tres características clave:
- tipadas: cada preferencia tiene una definición de esquema que incluye el tipo de dato y otros metadatos, como el valor predeterminado
- con alcance: las preferencias tienen alcance por proyecto o por usuario
- anidadas: cada clave de preferencia es un string separado por puntos, donde el primer segmento de ruta identifica un script del editor, y el resto

Todas las preferencias deben registrarse definiendo su esquema:
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Después de recargar ese script del editor, el editor registra este esquema. Luego el script del editor puede obtener y definir las preferencias, por ejemplo:
```lua
-- Obtener una preferencia específica
editor.prefs.get("my_json_formatter.indent.type")
-- Devuelve: "spaces"

-- Obtener un grupo de preferencias completo
editor.prefs.get("my_json_formatter")
-- Devuelve:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Definir múltiples preferencias anidadas a la vez
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Modos de ejecución {#execution-modes}

El tiempo de ejecución de scripts del editor usa 2 modos de ejecución que son mayormente transparentes para los scripts del editor: **immediate** y **long-running**.

El modo **immediate** se usa cuando el editor necesita recibir una respuesta del script lo más rápido posible. Por ejemplo, los callbacks `active` de los comandos de menú se ejecutan en modo immediate, porque estas comprobaciones se realizan en el hilo de interfaz del editor en respuesta a la interacción del usuario con el editor, y deben actualizar la interfaz dentro del mismo frame.

El modo **long-running** se usa cuando el editor no necesita una respuesta instantánea del script. Por ejemplo, los callbacks `run` de los comandos de menú se ejecutan en modo **long-running**, lo que permite que el script tome más tiempo para completar su trabajo.

Algunas de las funciones que pueden usar los scripts del editor pueden tardar mucho en ejecutarse. Por ejemplo, `editor.execute("git", "status", {reload_resources=false, out="capture"})` puede tardar hasta un segundo en proyectos suficientemente grandes. Para mantener la capacidad de respuesta y el rendimiento del editor, las funciones que podrían consumir mucho tiempo no están permitidas en contextos donde el editor necesita una respuesta inmediata. Intentar usar una función de este tipo en un contexto immediate producirá un error: `Cannot use long-running editor function in immediate context`. Para resolver este error, evita usar esas funciones en contextos immediate.

Las siguientes funciones se consideran long-running y no se pueden usar en modo immediate:
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` y `file:write()`: estas funciones modifican los archivos en disco, lo que hace que el editor sincronice su árbol de recursos en memoria con el estado del disco, algo que puede tardar segundos en proyectos grandes.
- `editor.execute()`: la ejecución de comandos de shell puede tardar una cantidad impredecible de tiempo.
- `editor.transact()`: las transacciones grandes en nodos ampliamente referenciados pueden tardar cientos de milisegundos, lo que es demasiado lento para la capacidad de respuesta de la interfaz.

Los siguientes contextos de ejecución de código usan el modo immediate:
- Callbacks `active` de comandos de menú: el editor necesita una respuesta del script dentro del mismo frame de la interfaz.
- Nivel superior de los scripts del editor: no esperamos que el acto de recargar scripts del editor tenga efectos secundarios.

## Acciones {#actions}

::: sidenote
Anteriormente, el editor interactuaba con la VM Lua de forma bloqueante, así que había un requisito estricto de que los scripts del editor no bloquearan, ya que algunas interacciones tienen que hacerse desde el hilo de interfaz del editor. Por esa razón, por ejemplo, no existían `editor.execute()` ni `editor.transact()`. En su lugar, la ejecución de scripts y el cambio del estado del editor se activaban devolviendo un array de "actions" desde hooks y callbacks `run` de comandos.

Ahora el editor interactúa con la VM Lua de forma no bloqueante, así que ya no hacen falta estas acciones: usar funciones como `editor.execute()` es más cómodo, conciso y potente. Las acciones ahora están **DEPRECATED**, aunque no tenemos planes de eliminarlas.
:::

Los scripts del editor pueden devolver un array de acciones desde la función `run` de un comando o desde las funciones hook de `/hooks.editor_script`. Luego el editor realizará estas acciones.

Una acción es una tabla que describe qué debe hacer el editor. Cada acción tiene una clave `action`. Las acciones vienen en 2 variantes: deshacibles y no deshacibles.

### Acciones deshacibles {#undoable-actions}

::: sidenote
Prefiere usar `editor.transact()`.
:::

Una acción deshacible se puede deshacer después de ejecutarse. Si un comando devuelve varias acciones deshacibles, se realizan juntas y se deshacen juntas. Debes usar acciones deshacibles si puedes. Su desventaja es que son más limitadas.

Acciones deshacibles existentes:
- `"set"` — define una propiedad de un nodo en el editor con algún valor. Ejemplo:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  La acción `"set"` requiere estas claves:
  - `node_id` — userdata de id de nodo. Como alternativa, puedes usar aquí la ruta de recurso en lugar del id de nodo que recibiste del editor, por ejemplo `"/main/game.script"`;
  - `property` — una propiedad de un nodo para definir, por ejemplo `"text"`;
  - `value` — nuevo valor para una propiedad. Para la propiedad `"text"` debe ser un string.

### Acciones no deshacibles {#non-undoable-actions}

::: sidenote
Prefiere usar `editor.execute()`.
:::

Una acción no deshacible borra el historial de deshacer, así que si quieres deshacer esa acción tendrás que usar otros medios, como el control de versiones.

Acciones no deshacibles existentes:
- `"shell"` — ejecuta un script de shell. Ejemplo:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- recortar "/" inicial
    }
  }
  ```
  La acción `"shell"` requiere la clave `command`, que es un array de comando y sus argumentos.

### Mezclar acciones y efectos secundarios {#mixing-actions-and-side-effects}

Puedes mezclar acciones deshacibles y no deshacibles. Las acciones se ejecutan secuencialmente, por lo que según el orden de las acciones terminarás perdiendo la capacidad de deshacer partes de ese comando.

En lugar de devolver acciones desde funciones que las esperan, puedes leer y escribir archivos directamente usando `io.open()`. Esto disparará una recarga de recursos que borrará el historial de deshacer.
