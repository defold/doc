---
title: Crear un juego de 15 puzzle en Defold
brief: Si eres nuevo en Defold, esta guía te ayudará a experimentar con algunos de los bloques de construcción de Defold y ejecutar lógica de script.
---

# El clásico 15 puzzle

Este conocido puzzle se volvió popular en América durante la década de 1870. El objetivo del puzzle es organizar las fichas del tablero deslizándolas horizontal y verticalmente. El puzzle empieza desde una posición en la que las fichas han sido mezcladas.

La versión más común del puzzle muestra los números 1--15 en las fichas. Sin embargo, puedes hacer el puzzle un poco más desafiante haciendo que las fichas formen parte de una imagen. Antes de empezar, intenta resolver el puzzle. Haz click en una ficha adyacente al cuadrado vacío para deslizar la ficha a la posición vacía.

## Crear el proyecto

1. Inicia Defold.
2. Selecciona *New Project* a la izquierda.
3. Selecciona la pestaña *From Template*.
4. Selecciona *Empty Project*
5. Selecciona una ubicación para el proyecto en tu disco local.
6. Haz click en *Create New Project*.

Abre el archivo de configuración *game.project* y define las dimensiones del juego en 512⨉512. Estas dimensiones coincidirán con la imagen que vas a usar.

![display settings](images/15-puzzle/display_settings.png)

El siguiente paso es descargar una imagen adecuada para el puzzle. Elige cualquier imagen cuadrada, pero asegúrate de escalarla a 512 por 512 pixels. Si no quieres salir a buscar una imagen, aquí hay una:

![Mona Lisa](images/15-puzzle/monalisa.png)

Descarga la imagen y luego arrástrala a la carpeta *main* de tu proyecto.

## Representar la cuadrícula

Defold contiene un componente *Tilemap* integrado que es perfecto para visualizar el tablero del puzzle. Los tilemaps te permiten definir y leer tiles individuales, que es todo lo que necesitas para este proyecto.

Pero antes de crear el tilemap, necesitas un *Tilesource* del que el tilemap tomará sus imágenes de tile.

Haz <kbd>Right click</kbd> en la carpeta *main* y selecciona <kbd>New ▸ Tile Source</kbd>. Nombra el nuevo archivo `monalisa.tilesource`.

Define las propiedades *Width* y *Height* del tile en 128. Esto dividirá la imagen de 512⨉512 pixels en 16 tiles. Los tiles se numerarán 1--16 cuando los pongas en el tilemap.

![Tile source](images/15-puzzle/tilesource.png)

Luego, haz <kbd>Right click</kbd> en la carpeta *main* y selecciona <kbd>New ▸ Tile Map</kbd>. Nombra el nuevo archivo "grid.tilemap".

Defold necesita que inicialices la cuadrícula. Para hacerlo, selecciona la capa "layer1" y pinta la cuadrícula 4⨉4 de tiles justo arriba a la derecha del origen. Realmente no importa a qué tiles los configures. En un momento escribirás código que definirá automáticamente el contenido de estos tiles.

![Tile map](images/15-puzzle/tilemap.png)

## Unir las piezas

Abre *main.collection*. Haz <kbd>Right click</kbd> en el nodo raíz en *Outline* y selecciona <kbd>Add Game Object</kbd>. Define la propiedad *Id* del nuevo objeto de juego como "game".

Haz <kbd>Right click</kbd> en el objeto de juego y selecciona <kbd>Add Component File</kbd>. Selecciona el archivo *grid.tilemap*. Define la propiedad *Id* como "tilemap".

Haz <kbd>Right click</kbd> en el objeto de juego y selecciona <kbd>Add Component ▸ Label</kbd>. Define la propiedad *Id* de la label como "done" y su propiedad *Text* como "Well done". Mueve la label al centro del tilemap.

Define la posición Z de la label en 1 para asegurarte de que se dibuje encima de la cuadrícula.

![Main collection](images/15-puzzle/main_collection.png)

Luego, crea un archivo de script Lua para la lógica del puzzle: haz <kbd>right click</kbd> en la carpeta *main* y selecciona <kbd>New ▸ Script</kbd>. Nombra el nuevo archivo "game.script".

Luego haz <kbd>Right click</kbd> en el objeto de juego llamado "game" en *main.collection* y selecciona <kbd>Add Component File</kbd>. Selecciona el archivo *game.script*.

Ejecuta el juego. Deberías ver la cuadrícula como la dibujaste y la label con el mensaje "Well done" encima.

## La lógica del puzzle

Ahora tienes todas las piezas en su lugar, así que el resto del tutorial se dedicará a unir la lógica del puzzle.

El script llevará su propia representación de las fichas del tablero, separada del tilemap. Esto se debe a que es posible hacerla más fácil de operar. En lugar de almacenar los tiles en un arreglo bidimensional, los tiles se almacenan como una lista unidimensional en una tabla Lua. La lista contiene el número de tile en secuencia, empezando desde la esquina superior izquierda de la cuadrícula hasta la esquina inferior derecha:

```lua
-- El tablero completado se ve así:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

El código que toma una lista de tiles como esa y la dibuja en nuestro tilemap es bastante simple, pero necesita convertir la posición en la lista a una posición x e y:

```lua
-- Dibuja una lista de tabla de tiles sobre un tilemap 4x4
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. En los tilemaps, el tile con valor x 1 y valor y 1 está abajo a la izquierda. Por lo tanto, la posición y debe invertirse.

Puedes comprobar que la función funciona como se espera creando una función `init()` de prueba:

```lua
function init(self)
    -- Un tablero invertido, para probar
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Con los tiles en una lista de tabla Lua, mezclar el orden es superfácil. El código simplemente recorre cada elemento de la lista e intercambia cada tile con otro tile elegido aleatoriamente:

```lua
-- Intercambia dos elementos en una lista de tabla
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Aleatoriza el orden de los elementos en una lista de tabla
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Antes de continuar, hay algo sobre el 15 puzzle que realmente necesitas considerar: si aleatorizas el orden de los tiles como estás haciendo arriba, hay un 50% de probabilidad de que el puzzle sea *imposible* de resolver.

Esto es una mala noticia, ya que definitivamente no quieres presentar al jugador un puzzle que no se puede resolver.

Por suerte, es posible averiguar si una configuración se puede resolver o no. Así:

## Solubilidad

Para averiguar si una posición en un puzzle 4⨉4 se puede resolver, se necesitan dos piezas de información:

1. El número de "inversiones" en la configuración. Una inversión ocurre cuando una ficha precede a otra ficha con un número menor. Por ejemplo, dada la lista `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}`, tiene 3 inversiones:

    - el número 12 tiene 11 y 10 después de él, dando 2 inversiones.
    - el número 11 tiene 10 después de él, dando 1 inversión más.

    (Ten en cuenta que el estado resuelto del puzzle tiene cero inversiones)

2. La fila donde está el cuadrado vacío (representado por `0` en la lista).

Estos dos números se pueden calcular con las siguientes funciones:

```lua
-- Cuenta el número de inversiones en una lista de tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Ten en cuenta que el cuadrado vacío no cuenta.

```lua
-- Encuentra la posición x e y de un tile dado
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Posición Y desde abajo.

Ahora, dados estos dos números, es posible decir si un estado del puzzle se puede resolver o no. Un estado de tablero 4⨉4 es *solvable* si:

- Si el cuadrado vacío está en una fila *impar* (1 o 3 contando desde abajo) y el número de inversiones es *par*.
- Si el cuadrado vacío está en una fila *par* (2 o 4 contando desde abajo) y el número de inversiones es *impar*.

## ¿Cómo funciona esto?

Cada movimiento legal mueve una pieza intercambiando su lugar con el cuadrado vacío, horizontal o verticalmente.

Mover una pieza horizontalmente no cambia el número de inversiones, ni tampoco cambia el número de fila donde encuentras el cuadrado vacío.

Mover una pieza verticalmente, sin embargo, cambia la paridad del número de inversiones (de impar a par, o de par a impar). También cambia la paridad de la fila del cuadrado vacío.

Por ejemplo:

![sliding a piece](images/15-puzzle/slide.png)

Este movimiento cambia el orden de los tiles de:

`{ ... 0, 11, 2, 13, 6 ... }`

a

`{ ... 6, 11, 2, 13, 0 ... }`

El nuevo estado agrega 3 inversiones así:

- El número 6 agrega 1 inversión (el número 2 está ahora después de 6)
- El número 11 pierde 1 inversión (el número 6 está ahora antes de 11)
- El número 13 pierde 1 inversión (el número 6 está ahora antes de 13)

Las formas posibles en que el número de inversiones puede cambiar por un deslizamiento vertical son ±1 o ±3.

Las formas posibles en que la fila del cuadrado vacío puede cambiar por un deslizamiento vertical son ±1.

En el estado final del puzzle, el cuadrado vacío está en la esquina inferior derecha (la fila *impar* 1) y el número de inversiones es el valor *par* 0. Cada movimiento legal deja estos dos valores intactos (movimiento horizontal) o cambia su polaridad (movimiento vertical). Ningún movimiento legal puede hacer que la polaridad de las inversiones y la fila del cuadrado vacío sea *impar*, *impar* o *par*, *par*.

Por lo tanto, cualquier estado del puzzle donde los dos números sean ambos impares o ambos pares es imposible de resolver.

Este es el código que comprueba la solubilidad:

```lua
-- ¿La lista de tabla dada de tiles 4x4 se puede resolver?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Entrada del usuario

Lo único que falta por hacer ahora es hacer que el puzzle sea interactivo.

Crea una función `init()` que haga toda la configuración en runtime usando las funciones creadas arriba:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Dile al motor que este objeto de juego debe recibir input.
2. Inicializa el generador aleatorio.
3. Crea un estado aleatorio inicial para el tablero.
4. Si el estado no se puede resolver, mezcla otra vez.
5. Dibuja el tablero.
6. Define una bandera de completado para seguir el estado de victoria.
7. Deshabilita la label del mensaje de completado.

Abre */input/game.input_bindings* y agrega un nuevo *Mouse Trigger*. Define el nombre de la acción como "press":

![input](images/15-puzzle/input.png)

Vuelve al script y crea una función `on_input()`.

```lua
-- Trata la entrada del usuario
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Si hay una pulsación del botón del mouse y el juego sigue en ejecución, haz lo siguiente.
2. Calcula el cuadrado x e y en el que el usuario hizo click.
3. Encuentra la ubicación actual del cuadrado vacío (0).
4. Si el cuadrado clickeado está justo encima, debajo, a la izquierda o a la derecha del cuadrado vacío, haz lo siguiente:
5. Intercambia los tiles del cuadrado clickeado y el vacío.
6. Vuelve a dibujar el tablero actualizado.
7. Si el número de inversiones en el tablero es 0, lo que significa que todo está en el orden correcto, y el cuadrado vacío está en la columna más a la derecha (debe estar en la última fila para que las inversiones sean 0), entonces el puzzle está resuelto, así que haz lo siguiente:
8. Define la bandera de completado.
9. Habilita/muestra el mensaje de completado.

¡Y eso es todo! Terminaste, ¡el juego de puzzle está completo!

## El script completo

Este es el código completo del script como referencia:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Ejercicios adicionales

1. Haz un puzzle 5⨉5, luego uno 6⨉5. Asegúrate de que las comprobaciones de solubilidad funcionen de forma general.
2. Agrega animaciones de deslizamiento. Los tiles no se pueden mover por separado del tilemap, así que tendrás que encontrar una manera de resolver eso. ¿Quizá un tilemap separado que solo contenga la pieza que se desliza?
