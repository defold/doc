---
title: Manual de tile map de Defold
brief: Este manual detalla el soporte de Defold para tile maps.
---

# Tile map

Un *Tile Map* es un componente que te permite componer, o pintar, tiles desde un *Tile Source* sobre una amplia área en cuadrícula. Los tile maps se usan comúnmente para construir entornos de niveles de juego. También puedes usar las *Collision Shapes* del tile source en tus mapas para detección de colisiones y simulación de física ([ejemplo](/examples/tilemap/collisions/)).

Antes de poder crear un tile map, necesitas crear un Tile Source. Consulta el [manual de Tile Source](/manuals/tilesource) para aprender cómo crear un Tile Source.

## Crear un tile map

Para crear un tile map nuevo:

- Haz <kbd>click derecho</kbd> en una ubicación del navegador *Assets* y selecciona <kbd>New... ▸ Tile Map</kbd>.
- Asigna un nombre al archivo.
- El tile map nuevo se abre automáticamente en el editor de tile maps.

  ![tilemap nuevo](images/tilemap/tilemap.png)

- Define la propiedad *Tile Source* con un archivo tile source que hayas preparado.

Para pintar tiles en tu tile map:

1. Selecciona o crea una *Layer* en la que pintar en la vista *Outline*.
2. Selecciona un tile para usarlo como pincel (presiona <kbd>Space</kbd> para mostrar la paleta de tiles) o selecciona algunos tiles haciendo click y arrastrando en la paleta para crear un pincel rectangular con varios tiles.

   ![Paleta](images/tilemap/palette.png)

3. Pinta con el pincel seleccionado. Para borrar un tile, elige un tile vacío y úsalo como pincel, o selecciona el borrador (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Pintar tiles](images/tilemap/paint_tiles.png)

Puedes tomar tiles directamente desde una capa y usar la selección como pincel. Mantén presionado <kbd>Shift</kbd> y haz click en un tile para tomarlo como el pincel actual. Mientras mantienes presionado <kbd>Shift</kbd>, también puedes hacer click y arrastrar para seleccionar un bloque de tiles que se usará como un pincel más grande. Además, es posible cortar tiles de forma similar manteniendo presionado <kbd>Shift+Ctrl</kbd> o borrarlos manteniendo presionado <kbd>Shift+Alt</kbd>.

Para rotar el pincel en sentido horario, usa <kbd>Z</kbd>. Usa <kbd>X</kbd> para voltear el pincel horizontalmente y <kbd>Y</kbd> para voltearlo verticalmente.

![Tomar tiles](images/tilemap/pick_tiles.png)

## Agregar un tile map a tu juego

Para agregar un tile map a tu juego:

1. Crea un objeto de juego para contener el componente tile map. El objeto de juego puede estar en un archivo o crearse directamente en una colección.
2. Haz <kbd>click derecho</kbd> en la raíz del objeto de juego y selecciona <kbd>Add Component File</kbd>.
3. Selecciona el archivo de tile map.

![Usar tile map](images/tilemap/use_tilemap.png)

## Manipulación en runtime

Puedes manipular tilemaps en runtime mediante varias funciones y propiedades diferentes (consulta la [documentación de la API para ver su uso](/ref/tilemap/)).

### Cambiar tiles desde un script

Puedes leer y escribir dinámicamente el contenido de un tile map mientras tu juego se ejecuta. Para hacerlo, usa las funciones [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) y [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile):

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Reemplaza el tile de césped (2) por un tile de agujero peligroso (número 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Propiedades de tilemap

Además de las propiedades *Id*, *Position*, *Rotation* y *Scale*, existen las siguientes propiedades específicas del componente:

*Tile Source*
: El recurso tile source que se usará para el tilemap.

*Material*
: El material que se usará para renderizar el tilemap.

*Blend Mode*
: El modo de mezcla que se usará al renderizar el tilemap.

### Modos de mezcla
:[blend-modes](../shared/blend-modes.md)

### Cambiar propiedades

Un tilemap tiene varias propiedades diferentes que se pueden manipular con `go.get()` y `go.set()`:

`tile_source`
: El tile source del tile map (`hash`). Puedes cambiarlo usando una propiedad de recurso tile source y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/tilemap/#tile_source).

`material`
: El material del tile map (`hash`). Puedes cambiarlo usando una propiedad de recurso material y `go.set()`. Consulta la [referencia de la API para ver un ejemplo](/ref/tilemap/#material).

### Constantes de material

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: El tinte de color del tile map (`vector4`). El `vector4` se usa para representar el tinte con x, y, z y w correspondientes al tinte rojo, verde, azul y alfa.

## Configuración del proyecto

El archivo *game.project* tiene algunas [configuraciones del proyecto](/manuals/project-settings#tilemap) relacionadas con tilemaps.

## Herramientas externas

Hay editores externos de mapas/niveles que pueden exportar directamente a tilemaps de Defold:

### Tiled

[Tiled](https://www.mapeditor.org/) es un editor de mapas conocido y ampliamente usado para mapas ortogonales, isométricos y hexagonales. Tiled tiene soporte para una amplia variedad de funcionalidades y puede [exportar directamente a Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/). Aprende más sobre cómo exportar datos de tilemap y metadatos adicionales en [esta publicación de blog del usuario de Defold "goeshard"](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) se puede usar para crear automáticamente tilesets completos a partir de tiles base simples y tiene un editor de mapas que puede exportar directamente a Defold.
