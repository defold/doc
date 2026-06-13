---
title: Tutorial Magic Link
brief: En este tutorial construirás un pequeño juego de puzzle completo con una pantalla de inicio, las mecánicas del juego y una progresión de niveles simple en forma de dificultad creciente.
---

# Tutorial Magic Link

Este juego es una variación del clásico juego de combinar al estilo de _Bejeweled_ y _Candy Crush_. El jugador arrastra y enlaza bloques del mismo color para eliminarlos, pero el objetivo del juego no es eliminar largas series de bloques del mismo color, limpiar el tablero o acumular puntos, sino lograr que un conjunto de "magic blocks" especiales repartidos por el tablero se conecten.

Este tutorial está escrito como una guía paso a paso en la que construimos el juego sobre un diseño completo. En realidad, encontrar un diseño que funcione toma mucho tiempo y esfuerzo. Podrías empezar con una idea central y luego buscar una forma de prototiparla para comprender mejor qué puede aportar esa idea. Incluso un juego simple como "Magic Link" requiere bastante trabajo de diseño. Este juego pasó por un par de iteraciones y algo de experimentación hasta llegar a su forma final (y todavía lejos de ser perfecta) y su conjunto de reglas. Pero para este tutorial, vamos a saltarnos ese proceso y empezar a construir sobre el diseño final.

## Primeros pasos

Necesitas empezar creando un nuevo proyecto e importando el paquete de assets:

* Crea un [proyecto nuevo](/manuals/project-setup/#creating-a-new-project) desde la plantilla "Empty Project"
* Descarga el proyecto completo "Magic Link" [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) como referencia. El proyecto completo contiene todos los assets por si quieres crear el proyecto desde cero.

## Reglas del juego

![Game rules schematic](images/magic-link/linker_rules.png)

El tablero se llena aleatoriamente con bloques de colores y un conjunto de magic blocks en cada ronda. Los bloques de colores siguen estas reglas:

* Desaparecen si el jugador los conecta (arrastrando) con bloques del mismo color.
* Cuando los bloques desaparecen, dejan huecos debajo. Los bloques de colores simplemente caen verticalmente en los huecos que se han abierto debajo.
* La parte inferior de la pantalla impide que todos los bloques sigan cayendo.

Los magic blocks se comportan de otra manera, según estas reglas:

* Los magic blocks se mueven _hacia los lados_ si aparece una abertura a cualquiera de los lados.
* Si aparece un hueco debajo, en cambio caen como los bloques de colores normales.

El jugador interactúa con el juego según las siguientes reglas:

* El jugador puede arrastrar y enlazar bloques de colores que son adyacentes horizontal, vertical y diagonalmente.
* Los bloques enlazados desaparecen tan pronto como el jugador suelta el touch input (levanta el dedo).
* Los magic blocks no reaccionan al arrastre y no pueden enlazarse manualmente.
* Los magic blocks, sin embargo, reaccionan al estar conectados horizontal o verticalmente. Es decir, se auto-enlazan bajo estas circunstancias.
* El nivel se completa si el jugador logra auto-enlazar todos los magic blocks del tablero.

El nivel de dificultad gobierna el número de magic blocks que se colocan en el tablero.

## Visión general

Como con todos los proyectos, necesitamos idear un plan general sobre cómo abordar la implementación. Hay muchas maneras en que el juego podría estructurarse y construirse. Técnicamente podríamos implementar todo el juego en el sistema GUI si quisiéramos. Sin embargo, construir el juego con objetos de juego y sprites, y usar las API de GUI para la GUI en pantalla y los elementos de heads-up display, suele ser la forma natural de construir un juego, así que tomaremos ese camino.

Como esperamos que el número de archivos se mantenga bastante bajo, mantendremos la estructura de carpetas del proyecto muy simple:

![Folder structure](images/magic-link/linker_folders.png)

*main*
: Esta carpeta contendrá toda la lógica del juego. Todos los scripts, archivos de objetos de juego, archivos de colección, archivos GUI, etc. residirán en esta carpeta. Si quieres dividir esta carpeta en varias o mantener subcarpetas, está perfectamente bien.

*images*
: Todos los assets de imagen vivirán en esta carpeta.

*fonts*
: Las fuentes usadas para renderizar texto se guardan aquí.

*input*
: Los input bindings se guardan en esta carpeta.

## Configurar el proyecto

El archivo *game.project* se mantiene principalmente con la configuración predeterminada, pero hay algunos ajustes por decidir. En primer lugar, necesitamos seleccionar una resolución para el juego. Es bastante fácil cambiar la resolución en una etapa posterior, y para un juego final necesitaremos hacer algo de trabajo para que el juego se vea bien independientemente de la resolución o relación de aspecto del dispositivo objetivo.

Elegimos definir la resolución en 640x960 pixels, que es la resolución nativa del iPhone 4. También es una resolución que cabe en muchos monitores, así que el playtesting en la computadora se vuelve fluido. Si quieres trabajar en una resolución diferente, solo tendrás que ajustar algunos valores de otra manera.

![Project settings](images/magic-link/linker_project_settings.png)

También vamos a necesitar aumentar el número máximo de sprites renderizados. Si quieres, puedes saltar a la siguiente sección y volver aquí cuando se te notifique en la consola que alcanzaste el límite de sprites.

![Game scale layout](images/magic-link/linker_layout.png)

Podemos calcular un número máximo de sprites necesarios:

* El tablero de juego contendrá bloques 7x9. El tablero necesitará algunos márgenes alrededor de los bordes y espacio arriba para algunos elementos GUI. Esto significa que los bloques tendrán alrededor de 90x90 pixels de tamaño. Más pequeños que eso serían demasiado diminutos para interactuar con ellos en la pantalla de un teléfono pequeño.
* Cada bloque es un sprite. Vamos a usar animaciones de un frame para definir el color del bloque.
* Algunos de los bloques serán magic blocks y vamos a usar 4 sprites para efectos especiales en cada uno de ellos.
* Los gráficos de enlace necesitarán un sprite por elemento. En el peor caso, eso son 61 sprites adicionales, si de algún modo el jugador enlaza todo el tablero (menos 2 magic blocks que no se pueden enlazar arrastrando).

Entonces, supongamos que tenemos un máximo de 30 magic blocks. El tablero tiene 63 bloques (sprites). De estos, los 30 magic blocks agregan 4 sprites para efectos especiales. Eso son 120 sprites adicionales. Así que, con los gráficos de enlace (que son máximo 33 en este caso), necesitaremos dibujar al menos 120 + 33 = 153 sprites por frame. La potencia de dos más cercana es 256.

Sin embargo, definir el máximo en 256 no es suficiente. Cada vez que limpiemos y reiniciemos el tablero vamos a eliminar todos los objetos de juego actuales y generar nuevos. El contador de sprites tendrá que cubrir todos los objetos que están vivos durante el frame. Eso incluye cualquier objeto eliminado, porque se eliminan al final del frame. Por lo tanto, definir el número máximo de sprites en 512 será suficiente.

![Max sprite count](images/magic-link/linker_sprite_max_count.png)

## Agregar los assets gráficos

Todos los assets necesarios para el juego se prepararon de antemano. Los agregaremos como imágenes de 512x512 pixels y dejaremos que el motor las escale al tamaño objetivo.

::: sidenote
Habilitar *hidpi* en la configuración del proyecto significa que el backbuffer se vuelve de alta resolución. Al dibujar imágenes grandes escaladas hacia abajo, se verán muy nítidas en pantallas retina.
:::

![Add images](images/magic-link/linker_add_images.png)

Además de los bloques, se incluye una imagen "connector" más sprites de efectos. También tenemos dos imágenes de fondo. Una se usará como fondo del tablero de juego y otra se usará para el menú principal. Agrega todas las imágenes a la carpeta *images*, luego crea un archivo de atlas *sprites.atlas*. Abre el archivo de atlas y agrega todas las imágenes.

![Add images to Atlas](images/magic-link/linker_add_to_atlas.png)

Hay un conjunto de imágenes GUI que se usan para crear elementos GUI, como botones y popups. Estas se agregan a un atlas separado llamado *gui.atlas*.

## Generar el tablero

El primer paso es construir la lógica del tablero. El tablero residirá en su propia colección, que contendrá todo lo que aparece en pantalla durante el gameplay. Por ahora, lo único necesario es el componente factory "blockfactory" y el script. Más adelante agregaremos una factory para conexiones, componentes GUI del menú principal y finalmente mecánicas de carga para iniciar el gameplay desde el menú principal y una forma de salir al menú.

1. Crea *`board.collection`* en la carpeta *`main`*. Asegúrate de nombrarla "board" para que podamos direccionarla más adelante. Si agregas el componente sprite de fondo, asegúrate de definir su posición Z en -1, o no se dibujará detrás de todos los bloques que generaremos luego.
2. Define temporalmente *Main Collection* (bajo *Bootstrap*) en *game.project* como `/main/board.collection` para poder probar fácilmente.

![Board collection](images/magic-link/linker_board_collection.png)

![Board collection bootstrap](images/magic-link/linker_bootstrap_board.png)

El archivo script *board.script* contendrá toda la lógica del tablero en sí y de los bloques del tablero. Empieza creando la función que construye el tablero e invócala (temporalmente) desde `init()`. También agregaremos dos funciones que no usaremos ahora pero que serán útiles más adelante:

`filter()`
: Esta función nos permitirá filtrar listas de elementos (bloques).

`build_blocklist()`
: Crea una lista de todos los bloques del tablero dispuesta como una lista plana, lo que nos permite filtrarla.

Después de construir el tablero, usaremos dos conjuntos de datos diferentes que contienen todos los bloques, `self.blocks` y `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Se usa para temporizar eventos
local blocksize = 80        -- Distancia entre centros de bloques
local edge = 40             -- Borde izquierdo y derecho.
local bottom_edge = 50      -- Borde inferior.
local boardwidth = 7        -- Número de columnas
local boardheight = 9       -- Número de filas
local centeroff = vmath.vector3(8, -8, 0) -- Offset central para el gfx del connector porque hay sombra debajo en la img del bloque
local dropamount = 3        -- El número de bloques que caen en un "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Construye una lista de bloques en 1 dimensión para facilitar el filtrado
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contiene la estructura del tablero
    self.blocks = {}            -- Lista de todos los bloques. Usada para facilitar el filtrado en la selección.
    self.chain = {}             -- Cadena de selección actual
    self.connectors = {}        -- Elementos connector para marcar la cadena de selección
    self.num_magic = 3          -- Número de magic blocks en el tablero
    self.drops = 1              -- Número de drops disponibles
    self.magic_blocks = {}      -- Magic blocks que están alineados
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calcula z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Elige un color aleatorio
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Construye lista 1d que podemos filtrar fácilmente.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Ten en cuenta que como los gráficos de bloque se solapan, necesitamos dibujarlos en el orden correcto. Esto se hace definiendo la coordenada z para cada bloque. El valor permanecerá muy por encima de -1, donde tenemos el sprite de fondo.

La lógica del tablero genera objetos de juego "`block`" mediante el componente factory "`blockfactory`". Necesitamos construir el objeto de juego block para que esto funcione. El bloque tiene un script y un sprite. Definimos la animación predeterminada del sprite como cualquiera de los bloques de color en *`sprites.atlas`*, luego agregamos código a *`block.script`* para hacer que el bloque adopte el color correcto cuando se genera:

![Block game object](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale(0.18)        -- renderizado escalado hacia abajo

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Define la propiedad *Prototype* del componente factory "blockfactory" al nuevo archivo gameobject *block.go*.

![Block factory](images/magic-link/linker_blockfactory.png)

Ahora deberías poder ejecutar el juego y ver el tablero lleno de bloques de colores aleatorios:

![First screenshot](images/magic-link/linker_first_screenshot.png)

## Interacciones

Ahora que tenemos un tablero, debemos agregar interacción de usuario. Primero definimos los input bindings en *game.input_binding* en la carpeta *input*. Asegúrate de que la configuración de *game.project* use tu archivo de input bindings.

![Input bindings](images/magic-link/linker_input_bindings.png)

Solo necesitamos un binding y asignamos `MOUSE_BUTTON_LEFT` al nombre de acción "touch". Este juego no usa multi touch y, por comodidad, Defold traduce la entrada de un dedo en clicks de mouse izquierdo.

El trabajo de tratar con el input recae en el tablero, así que necesitamos agregar código para eso en *board.script*:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- ¿Qué bloque fue tocado o atravesado al arrastrar?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- fuera del tablero.
            return
        end

        if action.pressed then
            -- El jugador empezó el toque
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- luego arrastra
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- El jugador soltó el toque.
        self.dragging = false
    end
end
```

Los mensajes `make_orange` y `make_green` son solo temporales para obtener feedback visual de que el código funciona. Necesitamos agregar código a *block.script* para manejar estos mensajes:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Ahora los bloques se rociarán primero con un mensaje `make_orange`, luego con mensajes `make_green` mientras mantengas el toque (o la pulsación del mouse), así que lo más probable es que los bloques solo parpadeen en naranja (si es que eso) antes de volverse verdes. ¡Pero sí sabemos qué bloque toca el jugador! Si quieres rastrear cómo se maneja el input con más detalle, inserta llamadas `print()` o `pprint()` en el código.

## Marcar enlaces

Ahora necesitamos assets para el marcador que se usará para indicar cuándo los bloques están enlazados por el jugador. La idea es simplemente superponer un gráfico en cada bloque para mostrar que está enlazado.

Necesitamos crear un objeto de juego "connector", que contenga la imagen sprite connector y también un componente factory "connector factory" en el objeto de juego "board":

![Connector game object](images/magic-link/linker_connector.png)

![Connector factory](images/magic-link/linker_connector_factory.png)

El script de este objeto de juego es mínimo; solo necesita escalar los gráficos para que coincidan con el resto del juego y definir correctamente el orden Z.

```lua
-- connector.script
function init(self)
    go.set_scale(0.18)              -- Define la escala de este objeto de juego.
    go.set(".", "position.z", 1)    -- Colócalo encima.
end
```

La función `same_color_neighbors()` devuelve una lista de bloques que son adyacentes a un bloque particular (en la posición x, y) y del mismo color. Esta función usa la función `filter()` que se aplica a la lista plana completa de bloques en `self.blocks`.

```lua
-- board.script
--
-- Devuelve una lista de bloques vecinos del mismo color que el
-- bloque en x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Una función auxiliar `in_blocklist()` comprueba si un bloque existe en una lista de bloques:

```lua
-- board.script
--
-- ¿Existe el bloque en la lista de bloques?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Usamos estas funciones durante el input de toque y arrastre en `on_input()` para construir los enlaces tocados de bloques. Aquí probaremos e ignoraremos magic blocks aunque todavía no haya ninguno:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- Si intenta manipular magic blocks, ignorar.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- Lista de vecinos del mismo color que el bloque tocado
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Marca bloque.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- luego arrastra
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- arrastrando sobre un vecino del mismo color
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Marca bloque.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Y finalmente, al soltar el toque, elimina visualmente todos los link connectors.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- El jugador soltó el toque.
        self.dragging = false

        -- Vacía la cadena de gráficos connector.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Connectors in game](images/magic-link/linker_connector_screen.png)

## Eliminar bloques enlazados

Ahora tenemos la lógica en su lugar para permitir enlazar bloques de los mismos colores, y simplemente eliminar los bloques enlazados es fácil. La razón por la que definimos la posición en el tablero como `hash("removing")` en lugar de simplemente `nil` es porque más adelante, cuando hagamos la lógica de magic blocks, necesitamos asegurarnos de que los magic blocks se deslicen solo hacia bloques recién eliminados. Si definimos la posición en el tablero como `nil` aquí, no tenemos forma de distinguir entre bloques recién eliminados y bloques que fueron eliminados previamente.

```lua
-- board.script
-- Elimina la cadena de bloques actualmente seleccionada
--
local function remove_chain(self)
    -- Elimina todos los bloques encadenados
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

También necesitaremos una función para eliminar realmente (definir como `nil`) las posiciones en el tablero que se han definido como `hash("removing")`:

```lua
-- board.script
--
-- Define bloques eliminados como nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

También creamos una función que desliza los bloques restantes hacia abajo a medida que los bloques debajo de ellos se eliminan (se definen como `nil`). Iteramos sobre el tablero columna por columna de izquierda a derecha y recorremos cada columna de abajo hacia arriba. Si encontramos una posición vacía (`nil`), deslizamos hacia abajo todos los bloques encima de esa posición.

```lua
-- board.script
--
-- Aplica lógica de desplazamiento hacia abajo a todos los bloques.
--
local function slide_board(self)
    -- Desliza todos los bloques restantes hacia abajo a los espacios vacíos.
    -- Ir columna por columna hace esto fácil.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Mover hacia abajo dy pasos
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calcula nueva posición
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula nueva z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist necesita actualizarse
    build_blocklist(self)
end
```

![Slide blocks down](images/magic-link/linker_blocks_slide.png)

Ahora simplemente podemos agregar llamadas a estas funciones en `on_input()` cuando se haya soltado el toque y haya bloques en `self.chain`.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- El jugador soltó el toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Hay una cadena de bloques. Elimínala del tablero y desliza hacia abajo los bloques restantes.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Vacía la cadena de gráficos connector.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Lógica de magic blocks

Ahora es momento de agregar los magic blocks a la mezcla. Primero, agreguemos la capacidad de que un bloque se convierta en magic block. De esa manera podemos hacer un paso separado sobre el tablero lleno y convertir los bloques que queremos en magic. Para darle algo de sabor a los magic blocks, primero creemos un efecto magic animado en forma de un objeto de juego *`magic_fx.go`* que podamos generar desde el magic block.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Este objeto de juego contiene dos sprites. Uno es el color "magic" (un sprite que usa la imagen *`magic-sphere_layer2.png`*) y el otro es un efecto "light" (un sprite que usa la imagen *`magic-sphere_layer3.png`*). El objeto está configurado para rotar cuando se genera, según el valor de la propiedad `direction`. También hacemos que el objeto escuche dos mensajes: `lights_on` y `lights_off`, que controlan el sprite del efecto de luz.

Crea un nuevo script y agrégalo como componente script a *`magic_fx.go`*:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Ahora, el magic block generará dos objetos de juego `magic_fx` al recibir el mensaje `make_magic`. Cada uno rotará en dirección opuesta, creando una bonita danza de color dentro de los bloques. También agregamos un sprite adicional a *`block.go`* con la imagen *`magic-sphere_layer4.png`*. Esta imagen se coloca en una Z más alta que el efecto generado y dibuja la cáscara o "cover" de la esfera mágica.

![Cover sprite](images/magic-link/linker_cover.png)

Ten en cuenta que debemos agregar un componente *Factory* al objeto de juego block y decirle que use nuestro objeto de juego *`magic_fx.go`* como *Prototype*. El script block también necesita escuchar los mensajes `lights_on` y `lights_off` y propagarlos hacia abajo a los objetos generados. Ten en cuenta que los objetos generados deben eliminarse cuando se elimina el bloque. Esto se encarga en la función `final()` del bloque. Todo esto ocurre en *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale(0.18) -- renderizado escalado hacia abajo

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Ahora podemos crear magic blocks y también encenderlos, un efecto que usaremos para indicar que un magic block está junto a otro magic block.

![Magic block without and with light](images/magic-link/linker_magic_blocks.png)

El código que llena el tablero con bloques ahora necesita modificarse para que tengamos algunos magic blocks allí:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribuye magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Construye lista 1d que podemos filtrar fácilmente.
    build_blocklist(self)
end
```

La mecánica principal de los magic blocks es su capacidad de deslizarse hacia los lados cuando otro bloque desaparece junto a ellos. Reflejamos todos los detalles de esa mecánica en la función `slide_magic_blocks()` en *board.script*. El algoritmo es simple:

1. Para cada fila del tablero, crea una lista `M` de magic blocks.
2. Itera por cada magic block en la lista `M` hasta que no se reduzca. En cada iteración:
    1. Si el magic block tiene una ubicación de bloque `hash("removing")` debajo, simplemente elimínalo de la lista `M`.
    2. Si el magic block tiene un hueco al costado marcado `hash("removing")`, deslízalo ahí, define su posición anterior como `hash("removing")` y luego elimínalo de la lista `M`.

```lua
-- board.script
-- Aplica la lógica de desplazamiento a magic blocks. Solo se desliza a posiciones
-- marcadas para eliminación con hash("removing")
--
local function slide_magic_blocks(self)
    -- Desliza todos los magic blocks hacia el lado que debe deslizar primero.
    -- ¡Esto funciona mejor yendo fila por fila!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Construye lista de magic blocks en esta fila.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Recorre la lista, desliza y elimina si es posible. Reitera hasta que la lista no se reduzca.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hueco debajo, no hacer nada.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- ¡Hueco a la izquierda! Desliza magic block ahí
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula nueva z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Se convertirá en nil luego
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hueco a la derecha. Desliza magic block ahí
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula nueva z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Se convertirá en nil luego
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Podemos probar la mecánica agregando una llamada a la función en `on_input()`:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- El jugador soltó el toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Hay una cadena de bloques. Elimínala del tablero
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Desliza hacia abajo los bloques restantes.
            slide_board(self)
        end
        self.chain = {}
        -- Cadena vacía limpia los gráficos connector.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Ahora vemos claramente por qué usamos la "etiqueta" intermedia `hash("removing")` en posiciones al eliminarlas. Sin ella, los magic blocks se deslizarían de un lado a otro hacia cualquier posición vacía al costado. Quizá una mecánica interesante, pero no la pensada para este pequeño juego.

Ahora necesitamos lógica para detectar si los magic blocks están conectados (sentados a la izquierda, derecha, arriba o abajo unos de otros), y necesitamos saber si todos los magic blocks del tablero están conectados. El algoritmo usado es bastante directo:

1. Crea una lista `M` de todos los magic blocks del tablero.
2. Para cada bloque de la lista `M`:
    1. Si el bloque no tiene `region` definida, asígnale el número de región `R` (inicialmente `1`).
    2. Marca todos los vecinos no marcados del bloque con el mismo número de región `R` e itera hacia sus vecinos, los vecinos de sus vecinos, etc.
    3. Aumenta el número de región `R` en `1`.

![Mark regions](images/magic-link/linker_regions.png)

Esta es la implementación del algoritmo:

```lua
-- board.script
--
-- Construye lista de todos los magic blocks actuales.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filtra magic blocks adyacentes
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Propaga región a vecinos
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Marca todas las regiones de magic blocks
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Limpia todas las marcas de región y cuenta vecinos
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Asigna regiones y las propaga
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

También creamos funciones que nos permiten contar el número de regiones entre los magic blocks. Si el número de regiones es 1, sabemos que todos los magic blocks están conectados. Además, agregamos una función que apaga las luces en todos los magic blocks y otra que enciende los efectos de luz en los magic blocks que tienen magic blocks vecinos:

```lua
-- board.script
--
-- Cuenta el número de regiones conectadas entre los magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Apaga luces en todos los magic blocks listados
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Define highlight para todos los magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Ahora podemos insertar estas partes de lógica en el flujo general. Primero, como la generación del tablero es aleatoria, hay una pequeña probabilidad de que empiece en estado ganador. Si eso ocurre, simplemente descartamos el tablero y lo construimos otra vez:

```lua
-- board.script
--
-- Limpia el tablero
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Construye lista 1d que podemos filtrar fácilmente.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Victoria" desde el inicio. Crear tablero nuevo.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

El resto de la lógica encaja en `on_input()`. Todavía no hay código para tratar con el mensaje `level_completed`, pero eso está bien por ahora:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- El jugador soltó el toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Hay una cadena de bloques. Elimínala del tablero y rellena el tablero.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Desliza hacia abajo los bloques restantes.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Resalta magic blocks adyacentes.
            if count_magic_regions(magic_blocks) == 1 then
                -- ¡Victoria!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Cadena vacía limpia los gráficos connector.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Ahora es posible jugar y alcanzar el estado ganador, aunque todavía no pasa nada cuando enlazas todos los magic blocks.

![First win](images/magic-link/linker_first_win.png)

## Drops

La idea del "drop" es agregar una mecánica de progresión simple. El jugador puede realizar un número limitado de "drop", que simplemente deja caer un par de piezas aleatorias nuevas sobre el tablero, presionando el botón *DROP*. El jugador empieza con un drop y cada vez que se limpia un nivel se concede un drop adicional. El código para la mecánica de drop encaja en dos funciones. Una devuelve una lista de posibles lugares donde pueden terminar los drops, y otra realiza el drop real con animación y todo.

```lua
-- board.script
--
-- Encuentra lugares para un drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- Si hay más que dropamount, elimina aleatoriamente un slot hasta dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Realiza el drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Elige un color aleatorio
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calcula nueva z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Reconstruye blocklist
    build_blocklist(self)
end
```

Podemos probar drops ejecutando lo siguiente, por ejemplo en `on_reload()`, o vinculándolo a una acción de input temporal:

```lua
s = dropspots(self)
if #s > 0 then
    -- Realiza el drop
    drop(self, s)
end
```

![Drop](images/magic-link/linker_drop.png)

## El menú principal

Ahora es momento de unirlo todo. Primero, creemos una pantalla inicial y separémosla del tablero. El paso 1 es crear un *main_menu.gui* y configurarlo con un botón *Start* (un nodo de texto y un nodo caja texturizado), un nodo de texto de título y algunos bloques decorativos (nodos caja texturizados). El script *main_menu.gui_script* que adjuntamos a la GUI anima los bloques decorativos en `init()`. También contiene un `on_input()` que envía un mensaje `start_game` a un script principal. Crearemos ese script en un minuto.

![Main menu GUI](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Como el trabajo de iniciar el juego pronto lo hará el script del menú principal, elimina la llamada temporal de configuración del tablero en `init()` en *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contiene la estructura del tablero
    self.blocks = {}            -- Lista de todos los bloques. Usada para facilitar el filtrado en la selección.

    self.chain = {}                -- Cadena de selección actual
    self.connectors = {}        -- Elementos connector para marcar la cadena de selección
    self.num_magic = 3            -- Número de magic blocks en el tablero

    self.drops = 1                -- Número de drops disponibles

    self.magic_blocks = {}        -- Magic blocks que están alineados

    self.dragging = false        -- Drag touch input
end
```

El script principal mantendrá el estado general del juego e iniciará el juego cuando se le solicite. Lo que queremos hacer aquí es hacer que *main.collection* contenga solo la cantidad mínima de assets que necesitamos mostrar al iniciar. Lo hacemos dejando que *main.collection* contenga un objeto de juego "main" que sostiene la GUI del menú principal, un componente script y, lo más importante, un componente *Collection Proxy*.

El proxy de colección nos permite cargar y descargar dinámicamente colecciones en el juego en ejecución. Actúa en nombre de un archivo de colección especificado y cargamos, inicializamos, habilitamos, deshabilitamos y descargamos la colección dinámica enviando mensajes al proxy. Para una descripción completa de cómo usarlos, consulta la [documentación de Collection Proxy](/manuals/collection-proxy).

En nuestro caso definimos la propiedad *Collection* del componente collection proxy como *board.collection*, que contiene el "level".

![main collection](images/magic-link/linker_main_collection.png)

Ahora debemos abrir *game.project* y cambiar el bootstrap *main_collection* a `/main/main.collectionc`.

![bootstrap main collection](images/magic-link/linker_bootstrap_main.png)

Ahora, iniciar un juego significa enviar mensajes a nuestro collection proxy para cargar, inicializar y habilitar el tablero, y luego deshabilitar el menú principal (para que no se muestre). Volver al menú principal hace lo contrario (dado que el proxy ha cargado la colección).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Ten en cuenta que llamamos al socket "main", que es un nombre que debemos asegurarnos de haber definido en *main.collection*. Selecciona el nodo raíz y comprueba que la propiedad *Name* sea "main".
2. De forma similar, enviamos mensajes a la colección cargada mediante su socket, nombrado a través de la propiedad *Name* en la colección.

## La GUI dentro del juego

Antes de agregar la pieza final de lógica al script del tablero, debemos agregar un conjunto de elementos GUI al tablero. Primero, en la parte superior del tablero, agregamos un botón *RESTART* y un botón *DROP*.

![board gui](images/magic-link/linker_board_gui.png)

El script de la GUI del tablero envía mensajes al elemento de diálogo GUI de reinicio al hacer click y de vuelta al propio script del tablero al hacer click en *DROP*:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Muestra el cuadro de diálogo de reinicio.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

El diálogo *RESTART* es simple. Lo construimos como *restart.gui* y adjuntamos un script simple que no hace nada si el jugador hace click en *NO*, envía un mensaje `restart_level` al script del tablero si el jugador hace click en *YES* y un mensaje `to_main_menu` al script principal si el jugador hace click en *Quit to main menu*:

![restart GUI](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume todo el input hasta que desaparezcamos.
    return true
end
```

También construimos un diálogo GUI simple para completar nivel en *level_complete.gui* con un script simple que envía un mensaje `next_level` al script del tablero cuando el jugador hace click en *CONTINUE*:

![level complete dialog](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume todo el input hasta que desaparezcamos.
    return true
end
```

Un diálogo que se usa para presentar el nivel actual, con un script que solo incluye ocultar y mostrar el diálogo. Al mostrar, el mensaje del diálogo se define como un mensaje que incluye el nivel de dificultad actual:

![present level GUI](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

También agregamos un diálogo que se muestra si el jugador intenta hacer un drop pero no hay espacio para él.

![no drop room GUI](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Finalmente, agregamos estos componentes GUI a *board.collection* y agregamos el código necesario a *board.script*:

![Final board collection](images/magic-link/linker_board_collection_final.png)

Necesitamos código para todos los mensajes que se envían hacia y desde el tablero en `on_message()`.

`start_level`
: Define el número de magic blocks según el parámetro de dificultad, construye el tablero y luego muestra el diálogo GUI "present_level" durante 2 segundos antes de iniciar el juego (eliminando el diálogo y adquiriendo foco de input). Ten en cuenta que usamos `go.animate()` como temporizador animando el valor de "timer", que no se usa para nada más.

`restart_level`
: Esto es lo que ocurre cuando el jugador presiona y confirma el botón GUI *RESTART*. Limpia y reconstruye el tablero y reinicia el contador de drops.

`level_completed`
: Se envía tan pronto como el tablero está en estado ganador. Apaga el input, anima los magic blocks y muestra el diálogo GUI "level_complete". El diálogo enviará de vuelta un mensaje `next_level` cuando el jugador haga click en el botón *CONTINUE* del diálogo.

`next_level`
: Cuando se recibe este mensaje, limpia el tablero, aumenta el contador de drops y envía `start_level` con el siguiente nivel de dificultad definido.

`drop`
: Comprueba dónde se pueden hacer drops. Si no hay lugares posibles, muestra el diálogo GUI "no_drop_room"; de lo contrario realiza el drop (si al jugador le quedan drops), disminuye el contador de drops y actualiza la representación visual del contador.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Espera un poco...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- apaga input
        msg.post(".", "release_input_focus")

        -- ¡Anima la magia!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale(0.17, m.id)
            go.animate(m.id, "scale", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Muestra pantalla de completado
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- El nivel de dificultad es número de magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- No se puede realizar drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Realiza el drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

¡Ahí lo tienes! ¡El juego, y este tutorial, ahora están completos! ¡Disfruta jugando este juego!

![Game finished](images/magic-link/linker_game_finished.png)

## Seguir adelante

Este pequeño juego tiene algunas propiedades interesantes y te animamos a experimentar con él. Aquí hay una lista de ejercicios que puedes hacer para familiarizarte más con Defold:

* Clarifica la interacción. Un jugador nuevo puede tener dificultades para entender cómo funciona el juego y con qué puede interactuar. Dedica algo de tiempo a hacer el juego más claro, sin insertar elementos de tutorial.
* Agrega sonidos. El juego está actualmente totalmente silencioso y se beneficiaría de una buena banda sonora y sonidos de interacción.
* Detecta automáticamente game over.
* High score. Agrega una funcionalidad de high score persistente.
* Reimplementa el juego usando solo las API de GUI.
* Actualmente, el juego continúa agregando un magic block por cada aumento de nivel. Eso no es sostenible para siempre. Encuentra una solución satisfactoria para este problema.
* Optimiza el juego y reduce el contador máximo de sprites reutilizando sprites en lugar de eliminarlos y volver a generarlos.
* Implementa renderizado del juego independiente de la resolución para que se vea igual de bien en pantallas con diferentes resoluciones y relaciones de aspecto.
