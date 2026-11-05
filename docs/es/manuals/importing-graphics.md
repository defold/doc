---
title: Importación y uso de gráficos 2D
brief: Este manual explica cómo importar y usar gráficos 2D.
---

# Importación de gráficos 2D {#importing-2d-graphics}

Defold admite muchos tipos de componentes visuales que se usan frecuentemente en juegos 2D. Puedes usar Defold para crear sprites estáticos y animados, componentes de interfaz, efectos de partículas, tile maps y fuentes bitmap. Antes de poder crear cualquiera de estos componentes visuales, debes importar archivos de imagen con los gráficos que quieras usar. Para importar archivos de imagen, simplemente arrastra los archivos desde el sistema de archivos de tu computadora y suéltalos en una ubicación adecuada del panel *Assets* del editor Defold.

![Importando archivos](images/graphics/import.png)

::: sidenote
Usa imágenes PNG o JPEG para atlas y tile sources. También puedes importar texturas fuente KTX2 para usarlas como texturas de modelos; consulta más abajo.
:::

## Texturas KTX2 {#ktx2-textures}

Importa un archivo *.ktx2* independiente arrastrándolo al panel *Assets* y asígnalo a un campo de textura de material de un componente Model. Los [modelos glTF y GLB](/manuals/importing-models/#ktx2-textures) también pueden referenciar archivos KTX2 externos o contener imágenes KTX2 integradas. Las entradas de atlas, tile sources y caras de cubemap siguen usando sus formatos de imagen existentes.

Las entradas KTX2 admitidas son texturas 2D que usan ETC1S/BasisLZ, UASTC, BC7 o datos R/RG/RGB/RGBA de 8 bits UNORM o sRGB. No se admiten arrays KTX2, cubemaps, volúmenes ni texturas HDR. KTX2 se procesa durante la build para generar recursos *.texturec* de Defold; el runtime no lee contenedores KTX2.

Abre un asset KTX2 para inspeccionar su formato de origen, dimensiones, espacio de color, metadatos alpha y niveles mip. *Outline* permite seleccionar cada nivel mip del archivo fuente. Estos muestran las imágenes originales aunque un perfil de textura redimensione la textura compilada o desactive sus mipmaps.

Usa [perfiles de textura](/manuals/texture-profiles/#ktx2-source-textures) para elegir entre conservar el formato de origen y convertirlo a otros formatos. Elige formatos de salida compatibles con tus dispositivos objetivo. Recomprimir una fuente que ya tiene pérdidas puede reducir más la calidad, incluso cuando **Keep KTX2 Format** necesita volver a codificarla después de procesar la imagen.


## Crear assets de Defold {#creating-defold-assets}

Cuando las imágenes se importan en Defold, pueden usarse para crear assets específicos de Defold:

![atlas](images/icons/atlas.png){.icon} Atlas
: Un atlas contiene una lista de archivos de imagen separados, que se combinan automáticamente en una imagen de textura más grande. Los atlas pueden contener imágenes estáticas y *Animation Groups*, conjuntos de imágenes que juntas forman una animación flipbook.

  ![atlas](images/graphics/atlas.png)

Aprende más sobre el recurso atlas en el [manual de Atlas](/manuals/atlas).

![tile source](images/icons/tilesource.png){.icon} Tile Source
: Un tile source hace referencia a un archivo de imagen que ya está compuesto por subimágenes más pequeñas ordenadas en una rejilla uniforme. Otro término usado comúnmente para este tipo de imagen compuesta es _sprite sheet_. Los tile sources pueden contener animaciones flipbook, definidas por el primer y el último tile de la animación. También es posible usar una imagen para adjuntar automáticamente formas de colisión a los tiles.

  ![tile source](images/graphics/tilesource.png)

Aprende más sobre el recurso tile source en el [manual de Tile source](/manuals/tilesource).

![bitmap font](images/icons/font.png){.icon} Bitmap Font
: Una fuente bitmap tiene sus glifos en una hoja de fuente PNG. Estos tipos de fuentes no ofrecen ninguna mejora de rendimiento frente a fuentes generadas desde archivos de fuente TrueType u OpenType, pero pueden incluir gráficos arbitrarios, coloración y sombras directamente en la imagen.

Aprende más sobre las fuentes bitmap en el [manual de Fuentes](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png)


## Usar assets de Defold {#using-defold-assets}

Cuando hayas convertido las imágenes en archivos Atlas y Tile Source, puedes usarlos para crear varios tipos distintos de componentes visuales:

![sprite](images/icons/sprite.png){.icon}
: Un sprite es una imagen estática o una animación flipbook que se muestra en pantalla.

  ![sprite](images/graphics/sprite.png)

Aprende más sobre sprites en el [manual de Sprite](/manuals/sprite).

![tile map](images/icons/tilemap.png){.icon} Tile map
: Un componente tilemap compone un mapa a partir de tiles (imágenes y formas de colisión) que provienen de un tile source. Los tile maps no pueden usar atlas como fuente.

  ![tilemap](images/graphics/tilemap.png)

Aprende más sobre tilemaps en el [manual de Tilemap](/manuals/tilemap).

![particle effect](images/icons/particlefx.png){.icon} Particle fx
: Las partículas que se generan desde un emisor de partículas están compuestas por una imagen estática o una animación flipbook de un atlas o un tile source.

  ![particles](images/graphics/particles.png)

Aprende más sobre efectos de partículas en el [manual de Particle fx](/manuals/particlefx).

![gui](images/icons/gui.png){.icon} GUI
: Los nodos caja GUI y los nodos Pie pueden usar imágenes estáticas y animaciones flipbook de atlas y tile sources.

  ![gui](images/graphics/gui.png)

Aprende más sobre GUIs en el [manual de GUI](/manuals/gui).
