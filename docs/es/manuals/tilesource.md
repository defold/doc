---
title: Manual de tile source de Defold
brief: Describe cómo usar y crear un tile source.
---

# Tile source {#tile-source}

Un *Tile Source* puede ser usado por un [componente Tilemap](/manuals/tilemap) para pintar tiles sobre un área de cuadrícula, o puede usarse como fuente gráfica para un [Sprite](/manuals/sprite) o un [componente Particle Effect](/manuals/particlefx). También puedes usar las *Collision Shapes* del tile source en un Tilemap para [detección de colisiones y simulación física](/manuals/physics) ([ejemplo](/examples/tilemap/collisions/)).

## Crear un tile source {#creating-a-tile-source}

Necesitas una imagen que contenga todos los tiles. Cada tile debe tener exactamente las mismas dimensiones y estar colocado en una cuadrícula. Defold admite _espaciado_ entre los tiles y un _margen_ alrededor de cada tile.

![imagen de tiles](images/tilemap/small_map.png)

Una vez creada la imagen fuente, puedes crear un Tile Source:

- Importa la imagen a tu proyecto arrastrándola a una ubicación del proyecto en el navegador *Assets*.
- Crea un nuevo archivo tile source (<kbd>click derecho</kbd> en una ubicación del navegador *Assets* y luego selecciona <kbd>New... ▸ Tile Source</kbd>).
- Nombra el archivo nuevo.
- El archivo se abre ahora en el editor de tile source.
- Haz click en el botón de búsqueda junto a la propiedad *Image* y selecciona tu imagen. Ahora deberías ver la imagen mostrada en el editor.
- Ajusta las *Properties* para que coincidan con la imagen fuente. Cuando todo sea correcto, los tiles se alinearán perfectamente.

![Crear un Tile Source](images/tilemap/tilesource.png)

Size
: El tamaño de la imagen fuente.

Tile Width
: El ancho de cada tile.

Tile Height
: El alto de cada tile.

Tile Margin
: El número de pixeles que rodean cada tile (naranja en la imagen anterior).

Tile Spacing
: El número de pixeles entre cada tile (azul en la imagen anterior).

Inner Padding
: Especifica cuántos pixeles vacíos deben agregarse automáticamente alrededor del tile en la textura resultante usada cuando se ejecuta el juego.

Extrude Border
: Especifica cuántas veces deben replicarse automáticamente los pixeles de borde alrededor del tile en la textura resultante usada cuando se ejecuta el juego.

Collision
: Especifica la imagen que se usará para generar automáticamente formas de colisión para los tiles.

## Animaciones flipbook de tile source {#tile-source-flip-book-animations}

Para definir una animación en un tile source, selecciona los tiles que se reproducirán mediante su propiedad *Frames*. Los tiles pueden aparecer en cualquier orden, incluidas repeticiones, sin necesidad de reorganizar la imagen fuente. Todos los tile sources nuevos tienen una animación predeterminada llamada "`anim`". Puedes agregar animaciones haciendo <kbd>click derecho</kbd> en la raíz del tile source en *Outline* y seleccionando <kbd>Add ▸ Animation</kbd>.

Al seleccionar una animación se muestran las *Properties* de la animación.

Id
: El identificador de la animación. Debe ser único para el tile source.

Frames
: Los números de tile en orden de animación, separados por comas. La numeración comienza en 1 en la esquina superior izquierda y avanza hacia la derecha, fila a fila, hasta la esquina inferior derecha. Puedes repetir números y usar rangos inclusivos en ambas direcciones.

| Frames | Secuencia expandida |
| --- | --- |
| `1, 3, 6, 3` | `1, 3, 6, 3` |
| `1-4, 8` | `1, 2, 3, 4, 8` |
| `4-2` | `4, 3, 2` |

El editor muestra las secuencias consecutivas de al menos tres frames como rangos. Por ejemplo, `1, 2, 3` se convierte en `1-3`, mientras que `1, 2` permanece como dos números de tile. Se conservan el orden de los frames y las repeticiones. La lista debe contener al menos un frame, y cada número de tile debe existir en la imagen fuente.

*Frames* sustituye a *Start Tile* y *End Tile*. El editor convierte los rangos válidos de archivos tile source antiguos en listas de frames. En scripts del editor, usa el array de enteros `frames` en lugar de `start_tile` y `end_tile`; consulta [Editar tile sources](/manuals/editor-scripts/#editing-tilesources).

Playback
: Especifica cómo debe reproducirse la animación a través de la lista *Frames*:

  - `None` no reproduce nada; se muestra la primera imagen.
  - `Once Forward` reproduce la animación una vez desde la primera hasta la última imagen.
  - `Once Backward` reproduce la animación una vez desde la última hasta la primera imagen.
  - `Once Ping Pong` reproduce la animación una vez desde la primera hasta la última imagen y después vuelve hasta la segunda imagen.
  - `Loop Forward` reproduce la animación repetidamente desde la primera hasta la última imagen.
  - `Loop Backward` reproduce la animación repetidamente desde la última hasta la primera imagen.
  - `Loop Ping Pong` reproduce la animación repetidamente desde la primera hasta la última imagen y luego vuelve a la primera imagen.

Fps
: La velocidad de reproducción de la animación, expresada en fotogramas por segundo (FPS).

Flip horizontal
: Invierte la animación horizontalmente.

Flip vertical
: Invierte la animación verticalmente.

## Formas de colisión de tile source {#tile-source-collision-shapes}

Defold usa una imagen especificada en la propiedad *Collision* para generar una forma _convexa_ para cada tile. La forma contorneará la parte del tile que contiene información de color, es decir, que no es 100% transparente.

A menudo tiene sentido usar la misma imagen para la colisión que la que contiene los gráficos reales, pero puedes especificar una imagen separada si quieres formas de colisión que difieran de los gráficos visibles. Cuando especificas una imagen de colisión, la previsualización se actualiza con un contorno en cada tile que indica las formas de colisión generadas.

La vista *Outline* del tile source lista los grupos de colisión que has agregado al tile source. Los archivos tile source nuevos tendrán agregado un grupo de colisión "default". Puedes agregar grupos nuevos haciendo <kbd>click derecho</kbd> en la raíz del tile source en *Outline* y seleccionando <kbd>Add ▸ Collision Group</kbd>.

Para seleccionar las formas de tile que deben pertenecer a un grupo determinado, selecciona el grupo en *Outline* y luego haz click en cada tile que quieras asignar al grupo. El contorno del tile y de la forma se colorea con el color del grupo. El editor asigna automáticamente el color al grupo.

![Formas de colisión](images/tilemap/collision.png)

Para eliminar un tile de su grupo de colisión, selecciona el elemento raíz del tile source en *Outline* y luego haz click en el tile.
