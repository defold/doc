---
brief: Si eres nuevo en Defold, esta guía te ayudará a empezar con lógica de script junto con algunos de los bloques de construcción de Defold para crear un clon de Snake desde cero.
layout: tutorial
title: Crear un juego de snake en Defold
difficulty: Beginner
---

# Snake

Este tutorial te guía por el proceso de crear uno de los juegos clásicos más comunes que puedes intentar recrear. Hay muchas variaciones de este juego; esta presenta una serpiente que come "comida" y que solo crece cuando come. Esta serpiente también se arrastra por un campo de juego que contiene obstáculos.

![thumbnail](images/snake/thumbnail.png)

### Lo que aprenderás

En este tutorial aprenderás a:
- Crear un juego desde cero en Defold
- Configurar y manejar inputs
- Crear tile maps y modificarlos durante runtime
- Escribir scripts en Lua

### Una nota para principiantes

Este tutorial está diseñado para principiantes, pero si eres completamente nuevo en Defold y el desarrollo de juegos, recomendamos leer primero algunos de los manuales introductorios, especialmente sobre los [bloques de construcción de Defold](/manuals/building-blocks/) y el [glosario](/manuals/glossary/). Si todavía no has descargado Defold, revisa el [manual de instalación](/manuals/install/). También se recomienda revisar la [visión general del editor](/manuals/editor/) para entrar rápidamente en el editor, pero aquí también proporcionamos capturas de pantalla para cada paso.

## Crear el proyecto

Inicia Defold y:

1. Selecciona *Create From* ▸ *Templates* en el lado izquierdo.
2. Selecciona *Empty Project*.
3. Escribe un nombre de proyecto en el campo *Title*.
4. Selecciona una *Location* para el proyecto.
5. Haz click en *Create New Project*.

![start](images/snake/1.png)

<input type="checkbox"/> ¡Hecho!

## Configuración del proyecto

Empezaremos definiendo la resolución del juego.

1. Cuando el editor esté abierto, busca el archivo `game.project` en el lado izquierdo, en el panel *Assets*. Haz doble click en él para abrirlo.
2. Ve a la sección *Display* del archivo `game.project`.
3. Define las dimensiones del juego (`Width` y `Height`) en 768⨉768 o algún otro múltiplo de 16.

![display](images/snake/2.png)

La razón por la que quieres hacer esto es que el juego se dibujará sobre una cuadrícula donde cada segmento será de 16x16 pixels, y de esta manera la pantalla del juego no cortará segmentos parciales. El archivo `game.project` contiene todas las configuraciones importantes del proyecto; puedes leer sobre todas ellas en el [manual de configuración del proyecto](/manuals/project-settings/).

<input type="checkbox"/> ¡Hecho!

## Crear nuevas carpetas en el panel Assets

Se necesita muy poco en términos de gráficos para un clon minimalista de Snake. Un segmento verde de 16⨉16 para la serpiente, un bloque blanco para los obstáculos y un bloque rojo más pequeño que representa la comida.

Primero, crea un directorio para los assets en el editor Defold:

1. Haz <kbd>Right click</kbd> en la carpeta `main`
2. Selecciona `New Folder`.
3. Aparecerá un popup pidiendo un nombre: escribe `assets` y haz click en `Create Folder`.

![new_folder](images/snake/3.png)

<input type="checkbox"/> ¡Hecho!

## Agregar gráficos al juego

La imagen de abajo es el único asset que necesitas:

![snake_sprites](images/snake/snake.png)

1. Haz <kbd>Right click</kbd> en la imagen de arriba y guárdala en tu disco local. Luego, arrastra y suelta (o copia + pega) la imagen descargada en la nueva ubicación de la carpeta del proyecto que acabas de crear.

![new_folder](images/snake/4.png)

También puedes leer más detalles sobre [importar assets aquí](/manuals/importing-graphics/).

<input type="checkbox"/> ¡Hecho!

## Agregar un Tile Source

Defold proporciona un componente [Tile Map](/manuals/tilemap/) integrado que usarás para crear el campo de juego formado por *tiles* alineados en una cuadrícula. Un tile map te permite definir y leer tiles individuales, lo que se ajusta perfectamente a este juego. Como los tile maps obtienen sus gráficos de un [Tile Source](/manuals/tilesource/), necesitas crear uno:

1. Haz <kbd>Right click</kbd> en la carpeta `assets`.
2. Selecciona `New` ▸ `Tile Source` en la sección "Resources".
3. Nombra el nuevo archivo "snake" (el editor guardará el archivo como `snake.tilesource`).

![new_tilesource](images/snake/5.png)

El tile source se abrirá en un Tile Source Editor dedicado para este tipo de archivo, y se te pedirá que proporciones una imagen para que funcione. En el lado derecho puedes encontrar un panel `Properties`:

4. Define la propiedad `Image` con el archivo de gráficos que acabas de importar.
![tilesource](images/snake/6.png)

5. Las propiedades `Width` y `Height` deben mantenerse en 16 (valor predeterminado). Esto dividirá la imagen de 32⨉32 pixels en 4 tiles, numerados 1–4.

![tilesource_properties](images/snake/7.png)

Ten en cuenta que la propiedad *Extrude Borders* está definida en 2 pixels. Esto es para evitar artefactos visuales alrededor de los tiles que tienen gráficos hasta el borde.

Si haces algún cambio en un archivo, aparece una marca de asterisco `*` junto a su nombre en su pestaña. Selecciona `File` ▸ `Save All` o usa el atajo <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> en Mac) para guardar todos los archivos.

<input type="checkbox"/> ¡Hecho!

## Crear el tile map del campo de juego

Ahora tienes un tile source listo para usar, así que es momento de crear el componente tile map del campo de juego:

1. Haz <kbd>Right click</kbd> en la carpeta `main` y selecciona <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> en la sección "Components". Nombra el nuevo archivo "grid" (el editor guardará el archivo como "grid.tilemap").
![add_tilemap](images/snake/8.png)

2. Se abrirá en un Tile Map Editor, y resaltará que necesita un **Tile Source**, así que define la propiedad *Tile Source* al "snake.tilesource" creado previamente.
![set_tilesource](images/snake/9.png)

<input type="checkbox"/> ¡Hecho!

## Dibujar tiles en el tile map

Defold solo almacena el área del tile map que realmente se usa, así que necesitas agregar suficientes tiles para llenar los límites de la pantalla.

1. Selecciona la capa `layer1` en el panel `Outline` del lado derecho.
2. Elige la opción de menú `Edit` ▸ `Select Tile...` o el atajo <kbd>Space</kbd> para mostrar la paleta de tiles, luego haz click en el tile que quieras usar al pintar.
![tilemap](images/snake/10.png)

3. Pinta un borde alrededor del borde de la pantalla y algunos obstáculos.
![tilemap_final](images/snake/11.png)

Necesitarás un tile map de tamaño 48x48 tiles (porque nuestro display es 768 y tenemos tiles de 16px, así que 768/16 = 48) para llenar la pantalla del juego.

Guarda el tile map cuando termines.

<input type="checkbox"/> ¡Hecho!

## Agregar el tile map al juego

Ahora necesitamos agregar nuestro tile map al juego. Si estás familiarizado con los bloques de construcción de Defold, los componentes son parte de los objetos de juego y los objetos de juego se pueden definir en las colecciones.

1. Abre `main.collection` haciendo doble click en él en el panel `Assets`. En la plantilla Empty Project, esta es por defecto la colección bootstrap que se carga al iniciar el motor.

2. Haz <kbd>Right click</kbd> en la raíz en `Outline` y selecciona `Add Game Object`, lo que crea un nuevo objeto de juego en la colección que se carga cuando empieza el juego.
![add_game_object](images/snake/12.png)

3. Haz <kbd>Right click</kbd> en el nuevo objeto de juego y selecciona `Add Component File`. Elige el archivo "grid.tilemap" que acabas de crear.
![add_component](images/snake/13.png)

Ahora tenemos un tile map en nuestra colección de juego. Debería ser visible cuando ejecutas el juego desde el editor.

1. Selecciona `Project` ▸ `Build` o el atajo <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> en Mac).

![run_game](images/snake/14.png)

<input type="checkbox"/> ¡Hecho!

## Agregar un script al juego

1. Haz <kbd>Right click</kbd> en la carpeta `main` en el navegador `Assets` y selecciona `New` ▸ `Script` en la sección Scripts. Nombra el nuevo archivo script "snake" (se guardará como "snake.script"). Este archivo contendrá toda la lógica del juego.
![add_script](images/snake/15.png)

2. Vuelve a *main.collection* y haz <kbd>right click</kbd> en el objeto de juego que contiene el tile map. Selecciona <kbd>Add&nbsp;Component&nbsp;File</kbd> y elige el archivo "snake.script".

![main _ollection](images/snake/16.png)

Ahora tienes el componente tile map y el script en su lugar.

<input type="checkbox"/> ¡Hecho!

## El script del juego

El script que vas a escribir controlará todo el juego. Iremos agregando funcionalidades una por una.

### Algoritmo de movimiento simple

La idea de cómo funcionará es la siguiente:

1. El script mantiene una lista de posiciones de tile que la serpiente ocupa actualmente.
2. Si el jugador presiona una tecla direccional, almacena la dirección en la que debería moverse la serpiente.
3. En un intervalo regular, mueve la serpiente un paso en la dirección de movimiento actual.

### Inicialización

Abre *snake.script* y localiza la función `init()`. Esta función es llamada por el motor cuando el script se inicializa al iniciar el juego. Cambia el código a lo siguiente:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

En este código:

1. Almacenamos los segmentos de la serpiente como una tabla Lua llamada `self.segments` que contiene una lista de tablas, cada una con una posición X e Y para un segmento.
2. Almacenamos la dirección actual como una tabla llamada `self.dir` con una dirección X e Y.
3. Almacenamos la velocidad de movimiento actual en `self.speed`, expresada como tiles por segundo.
4. Almacenamos un valor de temporizador en `self.time` que se usará para seguir la velocidad de movimiento.

El código de script anterior está escrito en el lenguaje Lua. Hay algunas cosas que tener en cuenta sobre el código, pero si todavía no entiendes algo de lo siguiente, no te preocupes. Solo acompaña, experimenta y dale tiempo --- eventualmente lo entenderás. Por ahora, puedes recordar que en `init()` solo inicializamos las variables que usaremos.

- Defold reserva un conjunto de *funciones* callback integradas que se llaman durante la vida de un componente script. Estas *no* son métodos sino funciones simples.
- El runtime pasa una referencia a la instancia actual del componente script mediante el parámetro `self`. La referencia `self` se usa para almacenar datos de instancia.
- La referencia `self` se puede usar como una tabla Lua en la que puedes almacenar datos. Solo usa la notación de punto como harías con cualquier otra tabla: `self.data = "value"`. La referencia es válida durante toda la vida del script, en este caso desde el inicio del juego hasta que lo cierras.
- Los literales de tabla Lua se escriben rodeados por llaves `{}`.
- Las entradas de tabla pueden ser pares clave/valor (`{x = 10, y = 20}`), tablas Lua anidadas (`{ {a = 1}, {b = 2} }`) u otros tipos de datos.

<input type="checkbox"/> ¡Hecho!

### Update

La función `init()` se llama exactamente una vez, cuando el componente script se instancia en el juego en ejecución. La función `update()`, sin embargo, se llama una vez **cada frame**. Eso hace que la función sea ideal para lógica de juego en tiempo real.

La idea para update es esta: en algún intervalo definido, haz lo siguiente:

1. Encuentra dónde está la cabeza de la serpiente, luego crea una nueva cabeza en la posición junto a ella desplazada por la dirección de movimiento actual. Entonces, si la serpiente se mueve con X=1 e Y=0 y la cabeza actual está en la ubicación X=0 e Y=0, la nueva cabeza debería estar en X=1 e Y=0.
2. Guarda la nueva posición de cabeza en la lista de segmentos que constituye la serpiente.
3. Obtén la posición de la cola desde la tabla de segmentos.
4. Borra el tile de la cola en esta posición.
5. Dibuja todos los segmentos de la serpiente (tiles) en las posiciones de la tabla.

![algorithm](images/snake/17.png)

:::sidenote
Ten en cuenta que nuestra cabeza de la serpiente está al final de la tabla, y la cola al principio.
:::

1. Encuentra la función `update()` en *snake.script* y cambia el código a lo siguiente:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

En este código:

1. Avanzamos el temporizador con la diferencia de tiempo (en segundos) desde la última vez que se invocó `update()` --- el llamado "delta time", o `dt`.
2. Si el temporizador ha avanzado lo suficiente:
3. Obtén la posición actual de la cabeza. `#` es el operador usado para obtener la longitud de una tabla cuando se usa como arreglo, que es nuestro caso --- todos los segmentos son valores de tabla sin clave especificada.
4. Crea un nuevo segmento de cabeza según la ubicación actual de la cabeza y la dirección de movimiento (`self.dir`).
5. Agrega la nueva cabeza a la tabla de segmentos (al final).
6. Elimina la cola desde el inicio de la tabla de segmentos.
7. Borra el tile en la posición de la cola eliminada. Nuestro tile map `#grid` tiene solo 1 capa llamada `layer1`.
8. Recorre los elementos de la tabla de segmentos. Cada iteración tendrá `i` definido a la posición en la tabla (empezando desde 1) y `s` definido al segmento actual.
9. Define el tile en la posición del segmento al valor 2 (que es el tile con el color verde de la serpiente).
10. Al terminar, reinicia el temporizador a cero.

Si ejecutas el juego ahora, deberías ver la serpiente de 4 segmentos de largo arrastrarse de izquierda a derecha sobre el campo de juego.

![run the game](images/snake/snake_run_1.png)

<input type="checkbox"/> ¡Hecho!

## Input del jugador

Antes de agregar código para reaccionar al input del jugador, necesitas configurar las conexiones de input.

### Input bindings

1. Encuentra en la carpeta `input` el archivo `game.input_binding` y haz <kbd>double click</kbd> para abrirlo.
2. Agrega un conjunto de bindings *Key Trigger* para movimiento arriba, abajo, izquierda y derecha. En la columna *Input* selecciona teclas del teclado y en las columnas *Action* escribe nombres de acción.

![input](images/snake/18.png)

El archivo de input binding mapea la entrada real del usuario (teclas, movimientos del mouse, etc.) a *nombres* de acción que se entregan a los scripts que han solicitado input.

<input type="checkbox"/> ¡Hecho!

### Adquirir foco de input

Con los bindings en su lugar, abre *snake.script* y agrega la siguiente línea al principio de la función `init()`:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

La línea agregada:
1. Envía un mensaje al objeto de juego actual ("." es una abreviatura para el objeto de juego actual) indicándole que empiece a recibir input del motor.

Luego encuentra la función `on_input` y escribe el siguiente código:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Estas ramas `if...elseif...` hacen lo siguiente:
1. Si se recibe la acción de input "up", como se configuró en los input bindings, y la tabla `action` tiene el campo `pressed` definido en `true` (el jugador presionó la tecla), entonces:
2. Define la dirección de movimiento.

Ejecuta el juego de nuevo y comprueba que puedes dirigir la serpiente.

<input type="checkbox"/> ¡Hecho!

### Mejorar el manejo de input

Ahora, observa que si presionas dos teclas simultáneamente, eso resultará en dos llamadas a `on_input()`, una por cada pulsación. Tal como está escrito el código anterior, solo la llamada que ocurra al final tendrá efecto en la dirección de la serpiente, ya que las llamadas posteriores a `on_input()` sobrescribirán los valores en `self.dir`.

Ten en cuenta también que si la serpiente se mueve a la izquierda y presionas la tecla <kbd>right</kbd>, la serpiente se dirigirá hacia sí misma. La solución *aparentemente* obvia a este problema es agregar una condición adicional a las cláusulas `if` en `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Sin embargo, si la serpiente se mueve a la izquierda y el jugador presiona *rápidamente* primero <kbd>up</kbd>, luego <kbd>right</kbd> antes de que ocurra el siguiente paso de movimiento, solo la pulsación de <kbd>right</kbd> tendrá efecto y la serpiente se moverá hacia sí misma. Con las condiciones agregadas a las cláusulas `if` mostradas arriba, el input se ignorará. *¡No está bien!*

Una solución adecuada a este problema es almacenar el input en una cola y extraer entradas de esa cola a medida que la serpiente se mueve:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Esta vez:
1. Agregamos una variable `self.dirqueue` que se inicializa como una tabla vacía.

En la función `update()` agrega:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Extrae el primer elemento de la cola de direcciones.
2. Si hay un elemento (`newdir` no es null), comprueba si `newdir` apunta en sentido opuesto a `self.dir`.
3. Define una nueva dirección solo si no apunta en sentido opuesto.

Y modifica `on_input` para almacenar el input actual en la cola en su lugar:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Agrega la dirección de input a la cola de direcciones en lugar de definir `self.dir` directamente.

Inicia el juego y comprueba que se juega como se espera.

<input type="checkbox"/> ¡Hecho!

## Comida y colisión con obstáculos

La serpiente necesita comida en el mapa para poder crecer larga y rápida. ¡Agreguemos eso!

### Generar la comida

Encima de la función `init()` agrega una nueva función:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

En esta función:
1. Declaramos una nueva función llamada `put_food()` que coloca una pieza de comida en el mapa.
2. Almacenamos una posición X e Y aleatoria en una variable llamada `self.food`.
3. Definimos el tile en la posición X e Y al valor 3, que es el gráfico de tile para la comida.

Luego llámala al final de la función `init()`:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Antes de empezar a extraer valores aleatorios con `math.random()`, define la semilla aleatoria; de lo contrario se generará la misma serie de valores aleatorios. Esta semilla solo debe definirse una vez.
2. Llama a la función `put_food()` al iniciar el juego para que el jugador empiece con una comida en el mapa.

<input type="checkbox"/> ¡Hecho!

### Comer la comida

Ahora, detectar si la serpiente ha colisionado con algo es solo cuestión de mirar qué hay en el tile map hacia donde se dirige la serpiente y reaccionar.

Agrega una variable que mantenga registro de si la serpiente está viva o no:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Una bandera que indica si la serpiente está viva o no.

Luego agrega lógica que pruebe colisión con muro/obstáculo y comida:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Avanza la serpiente solo si está viva.
2. Antes de dibujar en el tile map, lee qué hay en la posición donde estará la nueva cabeza de la serpiente.
3. Si el tile es un obstáculo u otra parte de la serpiente, ¡game over!
4. Si el tile es comida, aumenta la velocidad y luego coloca una nueva comida.
5. Ten en cuenta que la eliminación de la cola solo ocurre si no hay colisión. Esto significa que si el jugador come comida, la serpiente crecerá un segmento, ya que no se elimina ninguna cola en ese movimiento.

Ahora prueba el juego y asegúrate de que se juega bien.

Esto concluye el tutorial, pero sigue experimentando con el juego y trabaja en algunos de los ejercicios de abajo.

<input type="checkbox"/> ¡Hecho!

## El script completo

Este es el código completo del script como referencia:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Ejercicios

Es un buen ejercicio intentar implementar estas mejoras:

1. Agrega manejo de input de tecla para reiniciar el juego cuando termine.
2. Agrega puntuación y un contador de puntuación, ya sea usando solo un componente label (más fácil) o una gui completa.
3. La función put_food() no tiene en cuenta la posición de la serpiente ni ningún obstáculo. Arréglala para que solo aparezca en espacios libres.
4. Cuando termine el juego, muestra un mensaje “Game Over” y permite que el jugador lo intente otra vez.
5. Extra: agrega una segunda serpiente controlada por jugador.
