---
title: Manual de fuentes en Defold
brief: Este manual describe cómo Defold maneja las fuentes y cómo llevar texto a la pantalla en tus juegos.
---

# Archivos de fuente {#font-files}

Las fuentes se usan para renderizar texto en componentes Label y nodos de texto GUI. Defold admite varios formatos de archivo de fuente:

- TrueType
- OpenType
- BMFont

Las fuentes agregadas a tu proyecto se convierten automáticamente a un formato de textura que Defold puede renderizar. Hay dos técnicas de renderizado de fuentes disponibles, cada una con sus propias ventajas y desventajas específicas:

- Bitmap
- Distance field

## Fuentes offline o en runtime {#offline-or-runtime-fonts}

De forma predeterminada, la conversión a imágenes de glifos rasterizadas ocurre durante la build (offline). Esto tiene la desventaja de que cada fuente debe rasterizar todos los glifos posibles en la etapa de build, lo que puede producir texturas muy grandes que consumen memoria y también aumentan el tamaño del bundle.

Al usar "fuentes en runtime", las fuentes `.ttf` se incluirán en el bundle tal cual, y la rasterización ocurrirá bajo demanda en runtime. Esto minimiza tanto el uso de memoria en runtime como el tamaño del bundle.

## Compatibilidad con layout de texto (p. ej., derecha a izquierda) {#text-layout-support-eg-right-to-left}

Las fuentes en runtime también tienen la ventaja de admitir layout de texto completo, por ejemplo de derecha a izquierda.
Actualmente usamos las bibliotecas [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) y [SkriBidi](https://github.com/memononen/Skribidi).

Consulta [Habilitar fuentes en runtime](/manuals/font#enabling-runtime-fonts)

## Colección de fuentes {#font-collection}

El formato de archivo `.fontc` también se conoce como colección de fuentes. En modo offline, solo una fuente está asociada a ella.
Al usar fuentes en runtime, puedes asociar más de un archivo de fuente (`.ttf`) con la colección de fuentes.

Esto permite usar una colección de fuentes al renderizar varios textos en distintos idiomas, manteniendo baja la huella de memoria.
Por ejemplo, cargar una colección con la fuente japonesa, asociar esa fuente con la fuente principal actual y luego descargar la colección de fuente japonesa.

## Crear una fuente {#creating-a-font}

Para crear una fuente que se pueda usar en Defold, crea un nuevo archivo Font seleccionando <kbd>File ▸ New...</kbd> desde el menú y luego selecciona <kbd>Font</kbd>. También puedes hacer <kbd>click derecho</kbd> en una ubicación del navegador *Assets* y seleccionar <kbd>New... ▸ Font</kbd>.

![New font name](images/font/new_font_name.png)

Dale un nombre al nuevo archivo de fuente y haz click en <kbd>Ok</kbd>. El nuevo archivo de fuente se abre ahora en el editor.

![New font](images/font/new_font.png)

Arrastra la fuente que quieres usar al navegador *Assets* y suéltala en una ubicación adecuada.

Define la propiedad *Font* con el archivo de fuente y ajusta las propiedades de la fuente según sea necesario.

## Propiedades {#properties}

*Font*
: El archivo TTF, OTF o *`.fnt`* que se usará para generar los datos de la fuente.

*Material*
: El material que se usará al renderizar esta fuente. Asegúrate de cambiarlo para fuentes distance field y BMFonts (consulta más abajo para más detalles).

*Output Format*
: El tipo de datos de fuente que se genera.

  - `TYPE_BITMAP` convierte el archivo OTF o TTF importado en una textura de hoja de fuente donde los datos bitmap se usan para renderizar nodos de texto. Los canales de color se usan para codificar la forma de la cara, el contorno y la sombra proyectada. Para archivos *`.fnt`*, el bitmap de textura fuente se usa tal cual.
  - `TYPE_DISTANCE_FIELD` La fuente importada se convierte en una textura de hoja de fuente donde los datos de pixel no representan pixeles de pantalla, sino distancias al borde de la fuente. Consulta más abajo para más detalles.

*Render Mode*
: El modo de render que se usará para renderizar glifos.

  - `MODE_SINGLE_LAYER` produce un solo quad para cada carácter.
  - `MODE_MULTI_LAYER` produce quads separados para la forma del glifo, el contorno y las sombras, respectivamente. Las capas se renderizan en orden de atrás hacia delante, lo que evita que un carácter oculte caracteres renderizados anteriormente si el contorno es más ancho que la distancia entre glifos. Este modo de render también permite desplazar correctamente la sombra proyectada, según lo especificado por las propiedades Shadow X/Y en el recurso de fuente.

*Size*
: El tamaño objetivo de los glifos en pixeles.

*Antialias*
: Indica si la fuente debe tener antialias cuando se graba en el bitmap objetivo. Define este valor en 0 si quieres un renderizado de fuente pixel perfect.

*Alpha*
: La transparencia del glifo. 0.0--1.0, donde 0.0 significa transparente y 1.0 opaco.

*Outline Alpha*
: La transparencia del contorno generado. 0.0--1.0.

*Outline Width*
: El ancho del contorno generado en pixeles. Define este valor en 0 para no usar contorno.

*Shadow Alpha*
: La transparencia de la sombra generada. 0.0--1.0.

::: sidenote
El soporte de sombras está habilitado por los shaders de material de fuente integrados y maneja tanto el modo de render de una capa como el de varias capas. Si no necesitas renderizado de fuentes por capas ni soporte de sombras, es mejor usar un shader más simple como *`builtins/font-singlelayer.fp`*.
:::

*Shadow Blur*
: Para fuentes bitmap, esta opción indica cuántas veces se aplicará un pequeño kernel de desenfoque a cada glifo de la fuente. Para fuentes distance field, esta opción equivale al ancho real del desenfoque en pixeles.

*Shadow X/Y*
: El desplazamiento horizontal y vertical, en pixeles, de la sombra generada. Esta opción solo afectará la sombra del glifo cuando Render Mode esté configurado en `MODE_MULTI_LAYER`.

*Characters*
: Qué caracteres se incluirán en la fuente. De forma predeterminada, este campo incluye los caracteres ASCII imprimibles (códigos de carácter 32-126). Puedes agregar o eliminar caracteres de este campo para incluir más o menos caracteres en la fuente.

Para fuentes en runtime, este texto actúa como un precalentamiento de caché con los glifos correctos. Esto ocurre durante el tiempo de carga. Consulta `font.prewarm_text()`.

::: sidenote
Los caracteres ASCII imprimibles son:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Si marcas esta propiedad, todos los glifos disponibles en el archivo fuente se incluirán en la salida.

*Cache Width/Height*
: Restringe el tamaño del bitmap de caché de glifos. Cuando el motor renderiza texto, busca el glifo en el bitmap de caché. Si no existe allí, se agregará a la caché antes de renderizar. Si el bitmap de caché es demasiado pequeño para contener todos los glifos que se pide renderizar al motor, se señalará un error (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Si se define en 0, el tamaño de caché se configura automáticamente y crecerá hasta un máximo de 2048x4096.

## Fuentes de campo de distancia {#distance-field-fonts}

Las fuentes de campo de distancia almacenan en la textura la distancia al borde del glifo, en lugar de datos bitmap. Cuando el motor renderiza la fuente, se necesita un shader especial para interpretar los datos de distancia y usarlos para dibujar el glifo. Las fuentes de campo de distancia usan más recursos que las fuentes bitmap, pero permiten mayor flexibilidad de tamaño.

![Distance field font](images/font/df_font.png)

Asegúrate de cambiar la propiedad *Material* de la fuente a *`builtins/fonts/font-df.material`* (o cualquier otro material que pueda manejar los datos de campo de distancia) cuando crees la fuente, o la fuente no usará el shader correcto cuando se renderice en pantalla.

## Bitmap BMFonts {#bitmap-bmfonts}

Además de bitmaps generados, Defold admite fuentes en formato bitmap "BMFont" pregeneradas. Estas fuentes consisten en una hoja de fuente PNG con todos los glifos. Además, un archivo *`.fnt`* contiene información sobre dónde se encuentra cada glifo en la hoja, así como información de tamaño y kerning. (Ten en cuenta que Defold no admite la versión XML del formato *`.fnt`* que usan Phaser y algunas otras herramientas)

Estos tipos de fuentes no ofrecen ninguna mejora de rendimiento respecto de las fuentes bitmap generadas desde archivos de fuente TrueType u OpenType, pero pueden incluir gráficos arbitrarios, colores y sombras directamente en la imagen.

Agrega los archivos *`.fnt`* y *`.png`* generados a tu proyecto Defold. Estos archivos deben estar en la misma carpeta. Crea un nuevo archivo de fuente y define la propiedad *font* con el archivo *`.fnt`*. Asegúrate de que *output_format* esté definido en `TYPE_BITMAP`. Defold no generará un bitmap, sino que usará el proporcionado en el PNG.

::: sidenote
Para crear un BMFont, debes usar una herramienta que pueda generar los archivos adecuados. Existen varias opciones:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), una herramienta solo para Windows proporcionada por AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), una app gratuita basada en Adobe Air para Windows y macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), una herramienta open source basada en Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), una herramienta comercial para macOS de 71 Squared.
* [bmGlyph](https://www.bmglyph.com), una herramienta comercial para macOS de Sovapps.
:::

![BMfont](images/font/bm_font.png)

Para que la fuente se renderice correctamente, no olvides definir la propiedad Material en *`builtins/fonts/font-fnt.material`* cuando crees la fuente.

## Artefactos y buenas prácticas {#artifacts-and-best-practices}

En general, las fuentes bitmap son mejores cuando la fuente se renderiza sin escalado. Son más rápidas de renderizar en pantalla que las fuentes de campo de distancia.

Las fuentes de campo de distancia responden muy bien al escalado hacia arriba. Las fuentes bitmap, en cambio, al ser solo imágenes pixeladas, aumentarán de tamaño haciendo que los pixeles crezcan a medida que se escala la fuente, lo que produce artefactos en bloques. El siguiente es un ejemplo con tamaño de fuente de 48 pixeles, escalado 4 veces hacia arriba.

![Fonts scaled up](images/font/scale_up.png)

Al escalar hacia abajo, las texturas bitmap pueden reducirse de forma correcta y eficiente, con antialias, mediante la GPU. Una fuente bitmap conserva mejor su color que una fuente de campo de distancia. Aquí hay un zoom de la misma fuente de ejemplo con tamaño de 48 pixeles, escalada hacia abajo a 1/5 de su tamaño:

![Fonts scaled down](images/font/scale_down.png)

Las fuentes de campo de distancia deben renderizarse a un tamaño objetivo lo bastante grande como para contener información de distancia que pueda expresar las curvas de los glifos de la fuente. Esta es la misma fuente que arriba, pero con tamaño de 18 pixeles y escalada 10 veces hacia arriba. Queda claro que es demasiado pequeña para codificar las formas de esta tipografía:

![Distance field artifacts](images/font/df_artifacts.png)

Si no quieres soporte de sombra o contorno, define sus valores alpha respectivos en cero. De lo contrario, se seguirán generando datos de sombra y contorno, ocupando memoria innecesaria.

## Caché de fuentes {#font-cache}
En runtime, un recurso de fuente en Defold dará como resultado dos cosas: una textura y los datos de la fuente.

* Los datos de la fuente consisten en una lista de entradas de glifos, cada una con información básica de kerning y los datos bitmap de ese glifo.
* La textura se llama internamente "glyph cache texture" y se usará al renderizar texto para una fuente específica.

En runtime, al renderizar texto, el motor primero recorrerá los glifos que se deben renderizar para comprobar qué glifos están disponibles en la caché de textura. Cada glifo que falte en la caché de textura de glifos activará una carga de textura desde los datos bitmap almacenados en los datos de la fuente.

Cada glifo se coloca internamente en la caché según la línea base de la fuente, lo que permite calcular coordenadas de textura locales del glifo dentro de su celda de caché correspondiente en un shader. Esto significa que puedes lograr ciertos efectos de texto, como gradientes o superposiciones de textura, de forma dinámica. El motor expone métricas de la caché al shader mediante una constante especial de shader llamada `texture_size_recip`, que contiene la siguiente información en los componentes del vector:

* `texture_size_recip.x` es el inverso del ancho de la caché
* `texture_size_recip.y` es el inverso de la altura de la caché
* `texture_size_recip.z` es la relación entre el ancho de la celda de caché y el ancho de la caché
* `texture_size_recip.w` es la relación entre la altura de la celda de caché y la altura de la caché

Por ejemplo, para generar un gradiente en un fragment shader, simplemente escribe:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Para más información sobre uniforms de shader, consulta el [manual de shaders](/manuals/shader).

## Habilitar fuentes en runtime {#enabling-runtime-fonts}

Es posible usar la generación en runtime para fuentes de tipo SDF al usar fuentes TrueType (`.ttf`).
Este enfoque puede reducir mucho el tamaño de descarga y el consumo de memoria en runtime de un juego Defold.
La pequeña desventaja es la naturaleza asíncrona de generar cada glifo.

* Habilita la funcionalidad definiendo `font.runtime_generation` en `game.project`.

* Agrega un [App Manifest](/manuals/app-manifest) y habilita la opción `Use full text layout system`.
Esto crea un motor personalizado que tiene esta funcionalidad habilitada.

::: sidenote
Esta funcionalidad es actualmente experimental, pero con la intención de usarse como flujo de trabajo predeterminado en el futuro.
:::

::: important
La configuración `font.runtime_generation` afecta a todas las fuentes `.ttf` del proyecto.
:::


### Scripting de fuentes {#font-scripting}

#### Precalentar la caché de glifos {#prewarming-glyph-cache}

Para facilitar el uso de las fuentes en runtime, estas admiten el precalentamiento de la caché de glifos.
Esto significa que la fuente generará los glifos listados en la propiedad *Characters*.

::: sidenote
Si `All Chars` está seleccionado, no habrá precalentamiento, ya que eso anula el propósito de no tener que generar todos los glifos al mismo tiempo.
:::

Si el campo `Characters` del archivo `.fontc` está definido, se usa como texto para determinar qué glifos deben actualizarse en la caché de glifos.

También es posible actualizar manualmente la caché de glifos llamando a `font.prewarm_text(font_collection, text, callback)`. Proporciona un callback para avisarte cuando todos los glifos faltantes se han agregado a la caché de glifos y es seguro presentar el texto en pantalla.

### Agregar/eliminar fuentes de una colección de fuentes {#addingremoving-fonts-to-a-font-collection}

Para fuentes en runtime, es posible agregar o eliminar fuentes (`.ttf`) de una colección de fuentes.
Esto es útil cuando una fuente grande se ha dividido en varios archivos para distintos conjuntos de caracteres (p. ej., CJK)

::: important
Agregar una fuente a una colección de fuentes no carga ni renderiza automáticamente todos los glifos.
:::

```lua
-- obtiene la fuente principal
local font_collection = go.get("#label", "font")
font.add_font(font_collection, self.language_ttf_hash)

-- obtiene la fuente del idioma seleccionado
local font_collection_language = go.get("localization_japanese#label", "font")
local font_info = font.get_info(font_collection_language)
self.language_ttf_hash = font_info.fonts[1].path_hash -- obtiene la primera fuente (la especificada en el editor)
font.add_font(self.font_collection, self.language_ttf_hash) -- aumenta el contador de referencia de la fuente
```

```lua
-- elimina la referencia de la fuente
font.add_font(self.font_collection, self.language_ttf_hash)
```

### Precalentar glifos {#prewarming-glyphs}

Para mostrar correctamente un texto con una fuente en runtime, los glifos deben resolverse. `font.prewarm_text()` hace esto por ti.
Es una operación asíncrona y, una vez que termina y recibes el callback, es seguro continuar y mostrar cualquier mensaje que contenga los glifos.

::: important
Si la caché de glifos se llena, se expulsará el glifo más antiguo de la caché.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      label.set_text(self.label, info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
