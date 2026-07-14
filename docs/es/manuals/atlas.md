---
title: Manual de atlas
brief: Este manual explica cómo funcionan los recursos Atlas en Defold.
---

# Atlas

Aunque las imágenes individuales se usan a menudo como fuente para sprites, por motivos de rendimiento las imágenes deben combinarse en conjuntos de imágenes más grandes, llamados atlas. Combinar conjuntos de imágenes más pequeñas en atlas es especialmente importante en dispositivos móviles, donde la memoria y la potencia de procesamiento son más escasas que en computadoras de escritorio o consolas de videojuegos dedicadas.

En Defold, un recurso atlas es una lista de archivos de imagen separados, que se combinan automáticamente en una imagen más grande.

## Crear un atlas

Selecciona <kbd>New... ▸ Atlas</kbd> en el menú contextual del navegador *Assets*. Nombra el nuevo archivo de atlas. El editor abrirá el archivo en el editor de atlas. Las propiedades del atlas se muestran en el panel
*Properties* para que puedas editarlas (ver más abajo para más detalles).

Debes rellenar un atlas con imágenes o animaciones antes de poder usarlo como fuente gráfica para componentes de objeto, como componentes Sprite y ParticleFX.

Asegúrate de haber agregado tus imágenes al proyecto (arrastra y suelta archivos de imagen en la ubicación correcta en el navegador *Assets*).

Agregar imágenes individuales

: Arrastra y suelta imágenes desde el panel *Assets* a la vista del editor.

  Como alternativa, haz <kbd>click derecho</kbd> en la entrada raíz Atlas del panel *Outline*.

  Selecciona <kbd>Add Images</kbd> en el menú contextual emergente para agregar imágenes individuales.

  Se abre un diálogo desde el que puedes buscar y seleccionar las imágenes que quieres agregar al Atlas. Ten en cuenta que puedes filtrar los archivos de imagen y seleccionar varios archivos a la vez.

  ![Crear un atlas, agregar imágenes](images/atlas/add.png)

  Las imágenes agregadas se listan en *Outline* y el atlas completo puede verse en la vista central del editor. Puede que necesites presionar <kbd>F</kbd> (<kbd>View ▸ Frame Selection</kbd> en el menú) para encuadrar la selección.

  ![Imágenes agregadas](images/atlas/single_images.png)

Agregar animaciones flipbook
: Haz <kbd>click derecho</kbd> en la entrada raíz Atlas del panel *Outline*.

  Selecciona <kbd>Add Animation Group</kbd> en el menú contextual emergente para crear un grupo de animación flipbook.

  Se agrega al atlas un grupo de animación nuevo y vacío con un nombre predeterminado ("New Animation").

  Arrastra y suelta imágenes desde el panel *Assets* a la vista del editor para agregarlas al grupo seleccionado actualmente.

  Como alternativa, haz <kbd>click derecho</kbd> en el grupo nuevo y selecciona <kbd>Add Images</kbd> en el menú contextual.

  Se abre un diálogo desde el que puedes buscar y seleccionar las imágenes que quieres agregar al grupo de animación.

  ![Crear un atlas, agregar imágenes](images/atlas/add_animation.png)

  Presiona <kbd>Space</kbd> con el grupo de animación seleccionado para previsualizarlo, y <kbd>Ctrl/Cmd+T</kbd> para cerrar la previsualización. Ajusta las *Properties* de la animación según sea necesario (ver más abajo).

  ![Grupo de animación](images/atlas/animation_group.png)

Puedes reordenar las imágenes en la vista Outline seleccionándolas y presionando <kbd>Alt + Up/down</kbd>. También puedes crear duplicados fácilmente copiando y pegando imágenes en la vista Outline (desde el menú <kbd>Edit</kbd>, el menú contextual de click derecho o los atajos de teclado).

## Propiedades del atlas

Cada recurso atlas tiene un conjunto de propiedades. Estas se muestran en el panel *Properties* cuando seleccionas el elemento raíz en la vista *Outline*.

Size
: Muestra el tamaño total calculado del recurso de textura resultante. El ancho y el alto se ajustan a la potencia de dos más cercana. Ten en cuenta que, si activas la compresión de texturas, algunos formatos requieren texturas cuadradas. Las texturas no cuadradas se redimensionarán y se rellenarán con espacio vacío para hacer que la textura sea cuadrada. Consulta el [manual de perfiles de textura](/manuals/texture-profiles/) para más detalles.

Margin
: El número de pixeles que deben agregarse entre cada imagen.

Inner Padding
: El número de pixeles vacíos que deben agregarse como relleno alrededor de cada imagen.

Extrude Borders
: El número de pixeles de borde que deben agregarse repetidamente como relleno alrededor de cada imagen. Cuando el fragment shader muestrea pixeles en el borde de una imagen, los pixeles de una imagen vecina (en la misma textura de atlas) pueden sangrar sobre ella. Extruir el borde resuelve este problema.

Max Page Size
: El tamaño máximo de una página en un atlas de varias páginas. Esto puede usarse para dividir un atlas en varias páginas del mismo atlas para restringir el tamaño del atlas sin dejar de usar una sola draw call. Esta funcionalidad debe usarse en combinación con materiales habilitados para atlas de varias páginas, que se encuentran en `/builtins/materials/*_paged_atlas.material`.

![Atlas de varias páginas](images/atlas/multipage_atlas.png)

Rename Patterns
: Una lista separada por comas (´,´) de patrones de búsqueda y reemplazo, donde cada patrón tiene la forma `search=replace`.
El nombre original de cada imagen (el nombre base del archivo) se transformará usando estos patrones. (Por ejemplo, un patrón `hat=cat,_normal=` cambiará el nombre de una imagen llamada `hat_normal` a `cat`). Esto es útil al hacer coincidir animaciones entre atlas.

A continuación se muestran ejemplos de los distintos ajustes de propiedades con cuatro imágenes cuadradas de tamaño 64x64 agregadas a un atlas. Observa cómo el atlas salta a 256x256 en cuanto las imágenes no caben en 128x128, lo que produce mucho espacio de textura desperdiciado.

![Propiedades del atlas](images/atlas/atlas_properties.png)

## Propiedades de imagen

Cada imagen de un atlas tiene un conjunto de propiedades:

Id
: El id de la imagen (solo lectura).

Size
: El ancho y el alto de la imagen (solo lectura).

Pivot
: El punto de pivote de la imagen (en unidades). La esquina superior izquierda es (0,0) y la esquina inferior derecha es (1,1). El valor predeterminado es (0.5, 0.5). El pivote puede estar fuera del rango 0-1. El punto de pivote es donde se centrará la imagen cuando se use, por ejemplo, en un sprite. Puedes modificar el punto de pivote arrastrando el manipulador de pivote en la vista del editor. El manipulador solo será visible cuando haya una única imagen seleccionada. El ajuste a la rejilla puede activarse manteniendo presionado <kbd>Shift</kbd> mientras arrastras.

Sprite Trim Mode
: Cómo se renderiza el sprite. El valor predeterminado es renderizar el sprite como un rectángulo (Sprite Trim Mode configurado en Off). Si el sprite contiene muchos pixeles transparentes, puede ser más eficiente renderizarlo como una forma no rectangular usando entre 4 y 8 vértices. Ten en cuenta que el recorte de sprites no funciona junto con sprites slice-9.

Image
: Ruta a la imagen en sí.

![Propiedades de imagen](images/atlas/image_properties.png)

## Propiedades de animación

Además de la lista de imágenes que forman parte de un grupo de animación, hay un conjunto de propiedades disponible:

Id
: El nombre de la animación.

Fps
: La velocidad de reproducción de la animación, expresada en fotogramas por segundo (FPS).

Flip horizontal
: Invierte la animación horizontalmente.

Flip vertical
: Invierte la animación verticalmente.

Playback
: Especifica cómo debe reproducirse la animación:

  - `None` no reproduce nada; se muestra la primera imagen.
  - `Once Forward` reproduce la animación una vez desde la primera hasta la última imagen.
  - `Once Backward` reproduce la animación una vez desde la última hasta la primera imagen.
  - `Once Ping Pong` reproduce la animación una vez desde la primera hasta la última imagen y luego vuelve a la primera imagen.
  - `Loop Forward` reproduce la animación repetidamente desde la primera hasta la última imagen.
  - `Loop Backward` reproduce la animación repetidamente desde la última hasta la primera imagen.
  - `Loop Ping Pong` reproduce la animación repetidamente desde la primera hasta la última imagen y luego vuelve a la primera imagen.

## Creación de textura y atlas en runtime

Es posible crear una textura y un atlas en runtime.

### Crear un recurso Texture en runtime

Usa [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) para crear un nuevo recurso de textura:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Una vez creada la textura, puedes usar [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) para definir los pixeles de la textura:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
Es posible usar `resource.set_texture()` para actualizar también una subregión de la textura usando un ancho y alto de buffer menores que el tamaño completo de la textura, y cambiando los parámetros x e y de `resource.set_texture()`.
:::

La textura puede usarse directamente en un [componente de modelo](/manuals/model/) con `go.set()`:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Crear un Atlas en runtime

Si la textura debe usarse en un [componente sprite](/manuals/sprite/), primero debe usarse en un atlas. Usa [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) para crear un Atlas:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- asigna el atlas al componente 'sprite' del mismo objeto de juego
  go.set("#sprite", "image", my_atlas_id)

  -- reproduce la animación
  sprite.play_flipbook("#sprite", "my_animation")

```

Las entradas de `frames` son índices basados en 1 de la tabla `geometries`. Una lista puede reutilizar, reordenar u omitir geometrías, algo que no puede representarse mediante los campos de intervalo obsoletos `frame_start` y `frame_end`. `resource.get_atlas()` devuelve `frames`; usa la misma representación al pasar datos de atlas a `resource.set_atlas()` o `resource.create_atlas()`. El setter y el creador siguen aceptando los campos de intervalo por compatibilidad, pero el código nuevo debe usar `frames`.
