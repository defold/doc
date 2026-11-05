---
title: Manual de fuentes en Defold
brief: Este manual describe cómo Defold maneja las fuentes y cómo llevar texto a la pantalla en tus juegos.
---

# Archivos de fuente {#font-files}

Las fuentes se usan para renderizar texto en componentes Label y nodos de texto GUI. Defold admite varios formatos de archivo de fuente:

- TrueType
- OpenType
- BMFont

Tanto el motor de layout de texto heredado como el completo admiten contornos TrueType y OpenType CFF1/CFF2, incluida la generación en runtime a partir de recursos `.ttf` y `.otf`.

Para saber cómo aplicar estilos a fragmentos de texto y trabajar con enlaces y sprites integrados en el texto, consulta el [manual de marcado de texto enriquecido](/manuals/font-richtext).

Para fuentes TrueType y OpenType, la propiedad *Mode* selecciona cómo se renderizan los glifos:

- **Bitmap** usa imágenes de glifos rasterizadas.
- **SDF** (campo de distancia con signo) almacena las distancias a los bordes de los glifos en una textura, lo que permite un escalado más flexible que Bitmap.
- **Vector** renderiza las caras de los glifos a partir de datos de curvas y mantiene su nitidez al escalarlos. Los efectos de contorno y sombra siguen usando datos bitmap.

Los recursos de fuente nuevos usan el modo **Vector** y la generación de glifos **Dynamic**. Los recursos existentes conservan su modo Bitmap o SDF. Las fuentes BMFont siempre usan el bitmap que proporcionan.

El modo Vector requiere compatibilidad gráfica con texturas `RGBA16F` y `R32UI`, y no se admite en OpenGL ES 2 ni WebGL 1. Usa fuentes Bitmap o SDF con los materiales correspondientes si tus adaptadores gráficos objetivo no son compatibles; no hay un cambio automático de Vector a SDF. Consulta [Fuentes vectoriales](#vector-fonts) para configurarlas.

## Fuentes offline o en runtime {#offline-or-runtime-fonts}

La propiedad *Glyph Generation* selecciona cuándo se generan los datos de los glifos de cada fuente:

- **Static** genera los glifos seleccionados durante la build (offline). *Characters* y *All Chars* controlan cuáles se incluyen. El archivo fuente `.ttf` o `.otf` no se incluye en el bundle para generación en runtime.
- **Dynamic** incluye el archivo fuente `.ttf` o `.otf` en el bundle y genera glifos bajo demanda en runtime. *Prewarm Text* prepara los glifos cuando se carga la fuente. Los demás pueden generarse posteriormente según se necesiten.

Las fuentes SDF y Vector admiten ambas opciones. Las fuentes Bitmap y BMFont usan generación Static. Cada recurso de fuente se configura por separado, de modo que un proyecto puede combinar fuentes Static y Dynamic.

La generación dinámica puede reducir el tamaño del bundle y el uso de memoria en runtime, especialmente para fuentes con grandes conjuntos de caracteres. Requiere el sistema completo de layout de texto en el motor; consulta [Habilitar fuentes en runtime](#enabling-runtime-fonts).

## Compatibilidad con layout de texto (p. ej., derecha a izquierda) {#text-layout-support-eg-right-to-left}

Las fuentes en runtime también tienen la ventaja de admitir layout de texto completo, por ejemplo de derecha a izquierda.
Actualmente usamos las bibliotecas [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) y [SkriBidi](https://github.com/memononen/Skribidi).

Consulta [Habilitar fuentes en runtime](/manuals/font#enabling-runtime-fonts)

El editor usa el renderizador de fuentes del motor para las vistas previas de fuentes y texto de las escenas. La conformación del texto y el layout de derecha a izquierda requieren [fuentes en runtime](#enabling-runtime-fonts) y la opción **Use full text layout system** en App Manifest. Para fuentes offline, la vista previa respeta los ajustes **Characters** y **All Chars** de la fuente.

## Colección de fuentes {#font-collection}

El formato de archivo `.fontc` también se conoce como colección de fuentes. En modo offline, solo una fuente está asociada a ella.
Al usar fuentes en runtime, puedes asociar más de un archivo de fuente (`.ttf` o `.otf`) con la colección de fuentes.

Esto permite usar una colección de fuentes al renderizar varios textos en distintos idiomas, manteniendo baja la huella de memoria.
Por ejemplo, cargar una colección con la fuente japonesa, asociar esa fuente con la fuente principal actual y luego descargar la colección de fuente japonesa.

## Crear una fuente {#creating-a-font}

Para crear una fuente que se pueda usar en Defold, crea un nuevo archivo Font seleccionando <kbd>File ▸ New...</kbd> desde el menú y luego selecciona <kbd>Font</kbd>. También puedes hacer <kbd>click derecho</kbd> en una ubicación del navegador *Assets* y seleccionar <kbd>New... ▸ Font</kbd>.

![New font name](images/font/new_font_name.png)

Dale un nombre al nuevo archivo de fuente y haz click en <kbd>Ok</kbd>. El nuevo archivo de fuente se abre ahora en el editor.

Arrastra la fuente que quieres usar al navegador *Assets* y suéltala en una ubicación adecuada.

Establece la propiedad *Font* con el archivo de fuente. Para una fuente `.ttf` o `.otf`, selecciona *Mode* y *Glyph Generation* y configura las demás propiedades según sea necesario. Para la generación Dynamic, completa también la [configuración de fuentes en runtime](#enabling-runtime-fonts).

![Font properties with Vector mode and Dynamic glyph generation](images/font/font_properties.png)

Para las fuentes Vector, usa *Font Size* en un componente Label o nodo de texto GUI para cambiar el tamaño del texto mostrado. *Outline/Shadow Bitmap Size* controla la resolución de los bitmaps de los efectos independientemente del tamaño del texto mostrado.

Para las fuentes Bitmap y SDF, establece *Size* en el recurso de fuente para elegir el tamaño de los glifos generados. El tamaño de una BMFont procede del archivo fuente `.fnt`. Para cambiar el tamaño mostrado de estas fuentes, escala el componente Label o nodo de texto GUI.

## Propiedades {#properties}

*Font*
: El archivo TTF, OTF o *`.fnt`* que se usará para generar los datos de la fuente.

*Material*
: El material que se usará para renderizar esta fuente. Debe corresponder a su modo; consulta [Materiales de fuentes](#font-materials).

*Mode*
: La técnica de renderizado para una fuente `.ttf` o `.otf`: **Bitmap**, **SDF** o **Vector**. Sustituye a la antigua propiedad *Output Format*. No se muestra para fuentes BMFont.

*Glyph Generation*
: **Static** genera los datos de los glifos durante la build. **Dynamic** los genera en runtime y requiere el [sistema completo de layout de texto](#enabling-runtime-fonts). Esta propiedad está disponible para fuentes SDF y Vector. En modo Bitmap está fijada en Static y no se muestra para fuentes BMFont.

*Render Mode*
: La disposición de capas para fuentes Bitmap generadas. Esta propiedad solo se muestra en modo Bitmap para fuentes `.ttf` y `.otf`. Para fuentes SDF, Vector y BMFont, Defold selecciona la disposición automáticamente.

  - **Single Layer** produce un solo quad para cada carácter.
  - **Multi Layer** produce quads separados para la forma del glifo, el contorno y la sombra. Las capas se renderizan de atrás hacia delante, lo que evita que un carácter oculte caracteres renderizados antes si el contorno es más ancho que la distancia entre glifos. Esto también permite aplicar los desplazamientos de sombra de las propiedades *Shadow X/Y*.

*Size*
: El tamaño de los glifos en píxeles usado al generar los datos de fuentes Bitmap o SDF. Para fuentes BMFont, se lee del archivo `.fnt` y no puede editarse aquí.

*Outline/Shadow Bitmap Size*
: En modo Vector, sustituye a *Size*. Controla la resolución de los bitmaps de los efectos de contorno y sombra activados, tanto con generación Static como Dynamic. Se desactiva cuando ninguno de esos efectos está activado, ya que las caras de los glifos usan datos de curvas. Cambiar el *Font Size* de un Label o nodo de texto GUI no modifica esta resolución compartida de los bitmaps.

*Antialias*
: Indica si se suavizan los glifos al generar datos de fuente Bitmap. Desactívala para un renderizado pixel perfect. Esta propiedad solo se muestra en modo Bitmap para fuentes `.ttf` y `.otf`.

*Alpha*
: La transparencia del glifo. 0.0--1.0, donde 0.0 significa transparente y 1.0 opaco.

*Outline Alpha*
: La transparencia del contorno generado. 0.0--1.0.

*Outline Width*
: El ancho del contorno generado en pixeles. Define este valor en 0 para no usar contorno.

*Shadow Alpha*
: La transparencia de la sombra generada. 0.0--1.0.

::: sidenote
El shader de fuentes Bitmap integrado admite sombras tanto en el modo de renderizado *Single Layer* como en *Multi Layer*. Para fuentes Bitmap generadas que usan *Single Layer* y no necesitan sombras, un material personalizado puede usar `/builtins/fonts/font-singlelayer.fp`. Las fuentes SDF y Vector requieren shaders que correspondan a su modo; consulta [Materiales de fuentes](#font-materials).
:::

*Shadow Blur*
: La cantidad de desenfoque aplicada a la sombra generada. Establécela en 0 para una sombra nítida.

*Shadow X/Y*
: El desplazamiento horizontal y vertical en píxeles de la sombra generada. Para fuentes Bitmap generadas, usa el modo de renderizado *Multi Layer* para aplicar estos desplazamientos. Defold selecciona automáticamente las capas adecuadas para fuentes SDF y Vector.

*Characters*
: Para la generación Static, los caracteres que se incluirán en la fuente compilada. De forma predeterminada, este campo contiene los caracteres ASCII imprimibles (códigos 32-126). Agrega o elimina caracteres para controlar qué glifos estarán disponibles en runtime.

*Prewarm Text*
: Para la generación Dynamic, sustituye a *Characters*. El texto se usa para generar glifos y preparar la caché cuando se carga la fuente. No limita qué caracteres pueden generarse más adelante. También puedes preparar texto desde un script con [`font.prewarm_text()`](/ref/font/#font.prewarm_text).

::: sidenote
Los caracteres ASCII imprimibles son:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Para la generación Static, incluye todos los glifos disponibles en la fuente en lugar de limitarla a *Characters*. Esta propiedad se oculta para fuentes Dynamic.

*Cache Width/Height*
: Limita el tamaño del bitmap de caché de glifos que usan las fuentes Bitmap y SDF, y los efectos de contorno y sombra de Vector. Cuando el motor renderiza texto, busca el glifo en el bitmap de caché. Si no está allí, lo agrega antes de renderizarlo. Si el bitmap es demasiado pequeño para contener todos los glifos que se pide renderizar al motor, se indica un error (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  Si se define en 0, el tamaño de caché se configura automáticamente y crecerá hasta un máximo de 2048x4096.

## Materiales de fuentes {#font-materials}

Usa un material que corresponda al modo de la fuente. Los nodos de texto GUI usan el *Material* del recurso de fuente. Los componentes Label tienen una propiedad *Material* independiente que también debe corresponder a la fuente:

| Modo o tipo de fuente | Material de fuente para texto GUI | Material del componente Label |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Cambiar *Mode* en el editor de fuentes alterna entre los materiales integrados correspondientes de Bitmap, SDF y Vector cuando la fuente ya tiene asignado uno de ellos. Los materiales personalizados no se sustituyen automáticamente. Comprueba también la propiedad *Material* de los componentes Label que usan la fuente.

## Fuentes vectoriales {#vector-fonts}

Las fuentes vectoriales renderizan las caras de los glifos a partir de curvas, por lo que conservan su nitidez al cambiar el tamaño del texto mostrado. Para configurar una fuente que genere sus glifos en runtime:

1. Crea un recurso `.font`, por ejemplo `/fonts/ui.font`, y selecciona una fuente TrueType u OpenType en su propiedad *Font*. Puedes usar `/builtins/fonts/vera_mo_bd.ttf` para texto normal.
2. Establece *Mode* en **Vector**, *Glyph Generation* en **Dynamic** y *Material* en `/builtins/fonts/font-vector.material`. Estos son los valores predeterminados de los recursos de fuente nuevos.
3. Activa **Use full text layout system** en un App Manifest asignado al proyecto. Sigue [Habilitar fuentes en runtime](#enabling-runtime-fonts) para configurar el motor personalizado.
4. Activa [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) en *game.project*.
5. Asigna la fuente a un [Label](/manuals/label/) o agrégala a *Fonts* de una escena GUI y selecciónala en un [nodo de texto](/manuals/gui-text/). Para un Label, establece también el *Material* del componente en `/builtins/fonts/label-vector.material`. Ajusta *Font Size* del componente o nodo al tamaño de visualización deseado.

Las caras de los glifos Vector usan texturas de curvas, pero los contornos y las sombras activados siguen generando datos bitmap SDF y consumiendo memoria de textura de la caché de glifos. *Outline/Shadow Bitmap Size* establece esa resolución de bitmap independientemente del *Font Size* del Label o nodo de texto GUI. Establece *Outline Alpha* y *Shadow Alpha* en `0` cuando no necesites esos efectos para evitar generar sus datos bitmap.

### Emoji a color {#color-emoji}

Las fuentes Vector pueden renderizar emoji a color COLRv1, incluidos colores de paleta y degradados lineales y radiales. Los modos Bitmap y SDF no renderizan colores COLRv1. Usa la configuración Dynamic Vector anterior y agrega una fuente de emoji COLRv1 como alternativa a la colección de fuentes. El texto normal sigue usando la fuente original.

Por ejemplo, copia la [fuente Noto Color Emoji](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) en formato COLRv1 a tu proyecto como `/fonts/NotoColorEmoji-Regular.ttf`. Elige la versión COLRv1: otras fuentes de emoji pueden usar un formato de color distinto aunque su nombre de archivo termine en `.ttf`.

Agrega `/fonts/NotoColorEmoji-Regular.ttf` a **Project ▸ Custom Resources** en *game.project*. Si no hay otros recursos personalizados, el ajuste es:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Escribir una ruta de fuente en Lua no hace que el archivo se incluya en el bundle. [Custom Resources](/manuals/project-settings/#custom-resources) pone esta fuente a disposición de [`font.add_font()`](/ref/font/#font.add_font), que la carga mediante el sistema de recursos. Pasa la ruta de la fuente como cadena al cargarla desde el bundle.

Agrega la fuente alternativa una sola vez por recurso de fuente compartido. El cambio afecta a todos los Label y nodos de texto GUI que usan esa fuente, y agregar la misma alternativa dos veces genera un error. Si usas tanto el [ejemplo de Label](/manuals/label/#vector-fonts-and-color-emoji) como el [ejemplo de GUI](/manuals/gui-text/#vector-fonts-and-color-emoji) con el mismo `.font`, coordina la inicialización para agregar la alternativa una sola vez antes de que cualquiera de los ejemplos prepare o muestre texto. Los ejemplos preparan el texto completo después de agregar la alternativa y lo muestran cuando el callback termina correctamente.

## Fuentes de campo de distancia {#distance-field-fonts}

Las fuentes de campo de distancia almacenan en la textura la distancia al borde del glifo, en lugar de datos bitmap. Cuando el motor renderiza la fuente, se necesita un shader especial para interpretar los datos de distancia y usarlos para dibujar el glifo. Las fuentes de campo de distancia usan más recursos que las fuentes bitmap, pero permiten mayor flexibilidad de tamaño.

![Distance field font](images/font/df_font.png)

Selecciona **SDF** en *Mode* y elige **Static** o **Dynamic** en *Glyph Generation*. Usa *`/builtins/fonts/font-df.material`* para la fuente y *`/builtins/fonts/label-df.material`* para los componentes Label, o materiales personalizados que manejen datos de campos de distancia.

## Bitmap BMFonts {#bitmap-bmfonts}

Además de bitmaps generados, Defold admite fuentes en formato bitmap "BMFont" pregeneradas. Estas fuentes consisten en una hoja de fuente PNG con todos los glifos. Además, un archivo *`.fnt`* contiene información sobre dónde se encuentra cada glifo en la hoja, así como información de tamaño y kerning. (Ten en cuenta que Defold no admite la versión XML del formato *`.fnt`* que usan Phaser y algunas otras herramientas)

Estos tipos de fuentes no ofrecen ninguna mejora de rendimiento respecto de las fuentes bitmap generadas desde archivos de fuente TrueType u OpenType, pero pueden incluir gráficos arbitrarios, colores y sombras directamente en la imagen.

Agrega los archivos *`.fnt`* y *`.png`* generados a tu proyecto Defold. Deben estar en la misma carpeta. Crea un archivo de fuente nuevo y establece su propiedad *Font* con el archivo *`.fnt`*. Defold usa el bitmap proporcionado y lee su tamaño del archivo `.fnt`. *Mode* y *Glyph Generation* no se muestran para fuentes BMFont.

::: sidenote
Para crear un BMFont, debes usar una herramienta que pueda generar los archivos adecuados. Existen varias opciones:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), una herramienta solo para Windows proporcionada por AngelCode.
* [Shoebox](http://renderhjs.net/shoebox/), una app gratuita basada en Adobe Air para Windows y macOS.
* [Hiero](https://libgdx.com/wiki/tools/hiero), una herramienta open source basada en Java.
* [Glyph Designer](https://71squared.com/glyphdesigner), una herramienta comercial para macOS de 71 Squared.
* [bmGlyph](https://www.bmglyph.com), una herramienta comercial para macOS de Sovapps.
:::

![BMfont](images/font/bm_font.png)

Establece el *Material* de la fuente en *`/builtins/fonts/font-fnt.material`*. Para los componentes Label, usa *`/builtins/fonts/label-fnt.material`*.

## Artefactos y buenas prácticas {#artifacts-and-best-practices}

En general, las fuentes bitmap son mejores cuando la fuente se renderiza sin escalado. Son más rápidas de renderizar en pantalla que las fuentes de campo de distancia.

Las fuentes de campo de distancia responden muy bien al escalado hacia arriba. Las fuentes bitmap, en cambio, al ser solo imágenes pixeladas, aumentarán de tamaño haciendo que los pixeles crezcan a medida que se escala la fuente, lo que produce artefactos en bloques. El siguiente es un ejemplo con tamaño de fuente de 48 pixeles, escalado 4 veces hacia arriba.

![Fonts scaled up](images/font/scale_up.png)

Al escalar hacia abajo, las texturas bitmap pueden reducirse de forma correcta y eficiente, con antialias, mediante la GPU. Una fuente bitmap conserva mejor su color que una fuente de campo de distancia. Aquí hay un zoom de la misma fuente de ejemplo con tamaño de 48 pixeles, escalada hacia abajo a 1/5 de su tamaño:

![Fonts scaled down](images/font/scale_down.png)

Las fuentes de campo de distancia deben renderizarse a un tamaño objetivo lo bastante grande como para contener información de distancia que pueda expresar las curvas de los glifos de la fuente. Esta es la misma fuente que arriba, pero con tamaño de 18 pixeles y escalada 10 veces hacia arriba. Queda claro que es demasiado pequeña para codificar las formas de esta tipografía:

![Distance field artifacts](images/font/df_artifacts.png)

Si no quieres sombras o contornos, establece sus valores alpha en cero. De lo contrario, sus datos seguirán generándose y ocuparán memoria innecesariamente. En modo Vector, desactivar ambos efectos evita generar sus datos bitmap; las caras de los glifos siguen usando datos de curvas.

## Caché de fuentes {#font-cache}
Los recursos de fuentes Bitmap y SDF usan una textura de caché de glifos y datos de fuente en runtime. Las fuentes Vector almacenan las caras de sus glifos como datos de curvas y usan una caché bitmap para los efectos de contorno y sombra activados. La disposición de texturas descrita a continuación se aplica a las fuentes Bitmap y SDF.

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

La generación en runtime se configura por recurso de fuente:

1. Abre el recurso `.font` y selecciona una fuente TrueType (`.ttf`) u OpenType (`.otf`).
2. Establece *Mode* en **SDF** o **Vector** y *Glyph Generation* en **Dynamic**.
3. Elige los [materiales de fuente y Label](#font-materials) correspondientes.
4. Agrega un [App Manifest](/manuals/app-manifest), asígnalo a *Native Extensions ▸ App Manifest* en *game.project* y activa **Use full text layout system**. Esto crea un motor personalizado compatible con la generación de fuentes en runtime y el layout completo de texto.
5. Establece *Prewarm Text* con el texto que se mostrará poco después de cargar la fuente. Para texto que se necesite más adelante, usa [`font.prewarm_text()`](/ref/font/#font.prewarm_text) y espera a su callback antes de mostrarlo.

Los recursos de fuente nuevos ya usan el modo Vector y la generación Dynamic, pero siguen requiriendo la configuración de App Manifest anterior.

### Scripting de fuentes {#font-scripting}

#### Precalentar la caché de glifos {#prewarming-glyph-cache}

Las fuentes Dynamic generan los glifos necesarios para *Prewarm Text* al cargarse. El campo se interpreta como texto al que aplicar layout, por lo que la caché se prepara para los glifos que ese texto necesita. *All Chars* no está disponible para fuentes Dynamic.

También puedes llamar a `font.prewarm_text(font_collection, text, callback)` para una fuente Dynamic. El callback indica cuándo se han agregado a la caché todos los glifos que faltaban y es seguro mostrar el texto. Esta función no puede usarse con fuentes Static.

### Agregar/eliminar fuentes de una colección de fuentes {#addingremoving-fonts-to-a-font-collection}

Para las fuentes Dynamic, se pueden agregar o eliminar fuentes de origen (`.ttf` u `.otf`) de una colección de fuentes.
Esto es útil cuando una fuente grande se ha dividido en varios archivos para distintos conjuntos de caracteres (p. ej., CJK)

::: important
Agregar una fuente a una colección de fuentes no carga ni renderiza automáticamente todos los glifos.
:::

```lua
function init(self)
    -- Obtén la colección de fuentes de destino.
    self.font_collection = go.get("#label", "font")

    -- Obtén la primera fuente asignada a la colección del idioma seleccionado.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Asóciala con la colección de destino e incrementa su contador de referencias.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Elimina la asociación y libera la referencia a la fuente.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
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
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
