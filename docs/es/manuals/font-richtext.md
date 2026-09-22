---
title: Marcado de texto enriquecido en Defold
brief: Este manual explica cómo aplicar estilos a componentes Label y nodos de texto GUI mediante marcado de texto enriquecido, y cómo consultar enlaces y sprites desde Lua.
---

# Marcado de texto enriquecido {#rich-text-markup}

Usa marcado en los componentes Label y los nodos de texto GUI para aplicar estilos visuales y efectos anidados, y consultar enlaces y sprites desde Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

También puedes definir en la fuente un estilo de objeto reutilizable con nombre y seleccionarlo desde un enlace:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Referencia de etiquetas {#tag-reference}

| Etiqueta | Propósito | Ejemplo |
| --- | --- | --- |
| [`color`](#color) | Define el color de relleno del glifo. | <img src="/manuals/images/richtext/color_green.webp" alt="Texto verde" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Cambia la conformación de los glifos y el tamaño del layout. | <img src="/manuals/images/richtext/size_24.webp" alt="Texto de 24 pixeles" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Aplica un degradado de color estático o animado. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Texto con un degradado horizontal" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Subraya el texto. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Texto subrayado" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Tacha el texto. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Texto tachado" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Define el grosor y el color del contorno del glifo. | <img src="/manuals/images/richtext/outline.webp" alt="Texto con contorno" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Agrega una sombra al texto. | <img src="/manuals/images/richtext/shadow.webp" alt="Texto con sombra" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Aplica un desplazamiento aleatorio animado. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Texto que vibra" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Mueve el texto con una onda sinusoidal animada. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Texto que ondula" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Agrega un objeto sprite integrado en el texto. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite integrado en el texto" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Agrega un objeto de enlace interactivo. | <img src="/manuals/images/richtext/link.webp" alt="Texto con enlace" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Sintaxis {#syntax}

Los nombres de etiquetas y atributos distinguen entre mayúsculas y minúsculas. Una etiqueta con apertura y cierre se aplica al texto UTF-32 visible en su interior. Los objetos sprite usan etiquetas de cierre automático.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Atributos {#attributes}

Los atributos pueden escribirse sin comillas cuando no contienen espacios en blanco, o entre comillas simples o dobles. `color` y `size` admiten un primer valor abreviado además de la forma con el nombre `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Anidamiento {#nesting}

Las etiquetas deben cerrarse en orden inverso al de apertura. Los valores de un estilo interno sobrescriben la misma propiedad de un estilo externo. Las propiedades distintas se combinan. Los efectos de los fragmentos permanecen activos de forma independiente, por lo que los degradados anidados multiplican los colores y los efectos de posición anidados suman sus desplazamientos.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Entidades {#entities}

Usa `&amp;`, `&apos;`, `&gt;`, `&lt;` y `&quot;` para los caracteres reservados en el texto visible. Actualmente no se admiten entidades numéricas.

## Etiquetas {#tags}

Las etiquetas de texto enriquecido aplican estilos al fragmento de texto que encierran o describen un objeto que se puede consultar desde Lua. Las etiquetas de estilo usan una etiqueta de cierre correspondiente. El objeto `sprite` tiene cierre automático, mientras que `link` encierra el texto de su enlace.

### `color`

Define el color de relleno del glifo. Los colores usan `#RRGGBB` o `#RRGGBBAA`. El prefijo de almohadilla es obligatorio; `0xFF0000` y `FF0000` no son válidos. El resultado multiplica el color base del label o del renderizador.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `=color` o `value=color` | Sí | Sin valor predeterminado | Color de relleno en formato hexadecimal RGB o RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Texto de ejemplo renderizado en verde opaco](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Texto de ejemplo renderizado en verde con alfa a la mitad](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Cambia la conformación de los glifos y el tamaño del layout, no solo la escala de los vértices. Los valores relativos siempre usan el tamaño base de fuente del layout. No se acumulan con una etiqueta `size` que los encierre.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `=size` o `value=size` | Sí | Sin valor predeterminado | Tamaño absoluto, porcentaje, múltiplo del tamaño base o desplazamiento con signo respecto al tamaño base, mediante una de las formas siguientes. |

| Forma | Ejemplo con 32 px | Tamaño resuelto |
| --- | --- | --- |
| Número sin unidad o `px` | `24`, `24px` | 24 px |
| Porcentaje del tamaño base | `120%` | 38.4 px |
| Múltiplo del tamaño base | `2em` | 64 px |
| Desplazamiento con signo respecto al tamaño base | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Texto de ejemplo renderizado a 24 pixeles](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% de 32px*

![Texto de ejemplo renderizado al 120 por ciento de 32 pixeles](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em de 32px*

![Texto de ejemplo renderizado al doble del tamaño base de 32 pixeles](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Un degradado acepta exactamente un conjunto completo de atributos. Mezclar conjuntos u omitir un miembro no es válido.

| Modo | Atributos obligatorios | Interpolación |
| --- | --- | --- |
| Horizontal | `left`, `right` | Interpola entre los dos colores horizontales. |
| Vertical | `bottom`, `top` | Interpola entre los colores inferior y superior. |
| Cuatro esquinas | `tl`, `tr`, `bl`, `br` | Interpola entre los colores de cuatro vértices. |

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `left`, `right` | Para el modo horizontal | Ninguno | Colores de los extremos horizontales en formato `#RRGGBB` o `#RRGGBBAA`. Ambos deben estar presentes. |
| `bottom`, `top` | Para el modo vertical | Ninguno | Colores de los extremos verticales. Ambos deben estar presentes. |
| `tl`, `tr`, `bl`, `br` | Para el modo de cuatro esquinas | Ninguno | Colores superior izquierdo, superior derecho, inferior izquierdo e inferior derecho. Los cuatro deben estar presentes. |
| `fit` | No | `span` | `glyph` muestrea cada posición del texto conformado; `span` distribuye el degradado por todo el texto etiquetado. |
| `hz` | No | `0` | Ciclos completos de flujo por segundo en `[0,)`; cero mantiene el degradado estático. |
| `direction` | No | `forward` | `forward` o `reverse`. Controla la dirección del flujo cuando `hz` no es cero. |

Si se omite `fit`, `fit=span` distribuye el degradado por todo el texto etiquetado. `fit=glyph` muestrea cada posición del texto conformado de forma independiente. El atributo opcional `hz` especifica los ciclos completos de animación de flujo por segundo; su valor predeterminado de cero mantiene el degradado estático. La rampa de color repetida y reflejada fluye continuamente y vuelve a comenzar sin saltos de color. `direction=forward` es el valor predeterminado; usa `direction=reverse` para invertir el flujo.

```text
<gradient left=#FF00FF right=#FFFFFF>Horizontal Gradient</gradient>

<gradient hz=0.25 fit=glyph bottom=#182848 top=#4B6CB7>Animated vertical glyphs</gradient>

<gradient hz=0.25 direction=reverse left=#FF0000 right=#0000FF>Reverse flow</gradient>

<gradient hz=0.25 direction=reverse fit=span left=#FF0000 right=#0000FF>One animated span color</gradient>

<gradient fit=glyph tl=#FF0000 tr=#00FF00 bl=#0000FF br=#FFFFFF>
    Four corners
</gradient>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Horizontal*

![Texto de ejemplo con un degradado horizontal de magenta a blanco](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Vertical*

![Texto de ejemplo con un degradado azul vertical](images/richtext/gradient_vertical.webp)

</div>
</div>

**Cuatro esquinas**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de ejemplo con un degradado de cuatro esquinas ajustado a cada glifo](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de ejemplo con un degradado de cuatro esquinas ajustado al fragmento](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animado**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Degradado animado que fluye ajustado a cada glifo](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Degradado animado que fluye ajustado al fragmento](images/richtext/gradient_flow_span.webp)

</div>
</div>

Los colores del degradado multiplican el color de relleno actual. Por tanto, un degradado dentro de `color=#808080` no puede producir un canal más brillante que ese multiplicador base.

### `ul`

Dibuja un subrayado usando las métricas de subrayado de la fuente cuando están disponibles. La etiqueta no tiene un color independiente: la línea hereda el color de relleno efectivo, incluidos los degradados horizontales, verticales y de cuatro esquinas.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `pattern` | No | `solid` | `solid` o `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continuo*

![Texto de ejemplo con un subrayado continuo](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Discontinuo*

![Texto de ejemplo con un subrayado discontinuo](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Degradado*

![Texto de ejemplo con un subrayado degradado](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Dibuja una línea que tacha el texto encerrado. Acepta los mismos valores de `pattern` que `ul` y también hereda el color de relleno efectivo.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `pattern` | No | `solid` | `solid` o `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continuo*

![Texto de ejemplo con un tachado continuo](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Discontinuo*

![Texto de ejemplo con un tachado discontinuo](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Define el grosor del contorno, su color o ambos. Se requiere al menos un atributo. Un grosor de cero desactiva explícitamente el contorno del fragmento.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `size` | Uno de size/color | Heredado; `0` en una fuente predeterminada | Grosor en unidades de layout, intervalo `[0,)`. No se aceptan sufijos de unidad. |
| `color` | Uno de size/color | Heredado; `#000000` en un label predeterminado | Un solo color de contorno en formato hexadecimal RGB (`#RRGGBB`) o RGBA (`#RRGGBBAA`); el componente alfa controla la opacidad. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contorno negro exterior*

![Texto de ejemplo con un contorno negro exterior](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Agrega una sombra dura al texto encerrado. Se requiere al menos un atributo. Los atributos omitidos por una etiqueta anidada conservan el valor de la sombra que la encierra; los atributos omitidos por la etiqueta más externa conservan el valor de sombra base de la fuente.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `color` | No | Heredado; `#000000` en un label predeterminado | Color de la sombra en formato `#RRGGBB` o `#RRGGBBAA`. |
| `x` | No | Heredado; `0` en una fuente predeterminada | Desplazamiento horizontal de la sombra en unidades de layout. Los valores positivos la mueven a la derecha. |
| `y` | No | Heredado; `0` en una fuente predeterminada | Desplazamiento vertical de la sombra en unidades de layout. Los valores positivos la mueven hacia arriba. |
| `blur` | No | Heredado; `0` en una fuente predeterminada | Radio de desenfoque en unidades de layout, intervalo `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Texto de ejemplo con una sombra desplazada](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
El desenfoque de la sombra se genera y almacena en el atlas de glifos. Un fragmento puede solicitar un desenfoque menor que el precalculado en la fuente; los valores mayores se conservan en el layout, pero actualmente se renderizan usando el mayor desenfoque disponible en el atlas.
:::

### `shake`

Aplica un desplazamiento aleatorio animado y determinista sin cambiar los saltos de línea ni los límites del layout. El efecto controla el tiempo internamente; los scripts no necesitan modificar el texto del label en cada frame de animación.

| Atributo | Obligatorio | Predeterminado | Valores válidos | Significado |
| --- | --- | --- | --- | --- |
| `hz` | No | 20 | `[0,)` | Transiciones a destinos aleatorios por segundo. Cero pausa el efecto. |
| `amplitude` | No | 0.5 | `[0,)` | Desplazamiento máximo en unidades de layout. |
| `fit` | No | `glyph` | `glyph` o `span` | `glyph` muestrea un desplazamiento para cada unidad de glifo conformada respetando los grupos de caracteres. `span` mueve todo el fragmento de texto etiquetado como una unidad rígida. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de ejemplo con una vibración animada por glifo](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de ejemplo con una vibración animada de todo el fragmento](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Mueve los caracteres hacia arriba y hacia abajo con una onda sinusoidal animada sin cambiar los saltos de línea ni los límites del layout. El layout acumula el tiempo de animación al actualizarse.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `amplitude` | No | 1 | Desplazamiento vertical máximo en unidades de layout, intervalo `[0,)`. |
| `hz` | No | 1 | Ciclos temporales completos por segundo, intervalo `[0,)`. Cero pausa la onda. |
| `wavelength` | No | 6 | Posiciones de texto UTF-32 visible por ciclo espacial completo, intervalo `[1,)`. Los caracteres que la fuente conforma juntos, como un carácter base y su acento combinante, se mueven como una unidad. |
| `fit` | No | `glyph` | `glyph` aplica la onda espacial a lo largo del texto. `span` asigna a todo el fragmento etiquetado un desplazamiento sinusoidal vertical compartido. |
| `direction` | No | `forward` | `forward` avanza normalmente. `reverse` invierte la dirección de desplazamiento de la onda. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de ejemplo con una onda animada por glifo](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de ejemplo que se mueve como un solo fragmento animado](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Agrega un objeto sprite de cierre automático en la posición actual del texto visible. Sus atributos se conservan como metadatos para `label.get_layout_objects()` y `gui.get_layout_objects()`.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `id` | No | Generado | Identificador estable cuyo hash se guarda en el `id` del objeto de layout devuelto. |
| `src` | No | Ninguno | Identificador del recurso sprite definido por la aplicación, como una ruta de imagen o atlas del proyecto. |
| `animation` | No | Ninguno | Identificador de animación definido por la aplicación dentro del recurso. |
| `width` | No | `1em` | Ancho resuelto del sprite. |
| `height` | No | `1em` | Alto resuelto del sprite. |
| Cualquier otro atributo | No | Ausente | Metadatos definidos por la aplicación que se conservan para el resolvedor de objetos y las APIs de objetos de layout. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Sprite integrado en el texto, resuelto*

![Un logo de Defold renderizado integrado en el texto](images/richtext/sprite.webp)

</div>
</div>

Las dimensiones aceptan unidades de layout positivas sin sufijo, `px`, `em` o `%`. Tanto `em` como `%` usan el tamaño base de fuente del layout de texto.

Cada dimensión omitida toma de forma independiente el valor predeterminado `1em`. Omitir ambas produce un objeto de `1em × 1em`; especificar solo el ancho no calcula automáticamente el alto a partir de la relación de aspecto del recurso.

::: important
¡La etiqueta sprite es simplemente un marcador de posición para que el desarrollador coloque cualquier objeto en ese lugar!
:::

### `link`

Describe un rango de texto visible como un objeto de enlace. El texto encerrado se dispone normalmente y recibe de forma predeterminada el estilo con nombre `link`. Los componentes Label y GUI seleccionan `link:hover` y `link:active` en respuesta al input sin volver a conformar el texto. Consulta [mensajes de interacción](#interaction-messages) para conocer los mensajes generados por el input de enlaces.

| Atributo | Obligatorio | Predeterminado | Significado |
| --- | --- | --- | --- |
| `src` | No | Ninguno | Destino del enlace definido por la aplicación. El valor se devuelve como una cadena sin validación ni navegación automáticas. |
| `id` | No | Generado | Identificador estable cuyo hash se guarda en el `id` del objeto de layout devuelto. |
| `style` | No | `link` | Estilo predeterminado con nombre para el texto del enlace. |
| Cualquier otro atributo | No | Ausente | Metadatos definidos por la aplicación, como un identificador, una acción, un tooltip o un valor para analíticas. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com renderizado con el estilo de enlace predeterminado y un subrayado](images/richtext/link.webp)

</div>
</div>

El componente sigue el estado del puntero de cada enlace. Aplica `link:hover` mientras el puntero está sobre el enlace y `link:active` mientras permanece presionado. Cuando no se aplica ninguno de estos estados, el componente restaura el estilo indicado por el atributo `style` del enlace, o `link` si el atributo no está presente.

### Mensajes de interacción {#interaction-messages}

La interacción con enlaces usa el sistema de input normal de Defold. Agrega una vinculación Mouse Trigger para `MOUSE_BUTTON_LEFT`, que también activa el input de un solo toque, y adquiere el foco de input en el script del objeto de juego o en el script GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Consulta [foco de input](/manuals/input/#input-focus) e [input de mouse y táctil](/manuals/input-mouse-and-touch) para conocer los detalles de configuración.

Cuando un componente Label o GUI recibe input del puntero, los enlaces generan los siguientes mensajes. Los mensajes de Label se envían al objeto de juego al que pertenece; los mensajes de GUI se envían al script GUI.

| Mensaje | Cuándo se envía |
| --- | --- |
| `text_object_hovered` | El puntero entra en un enlace. |
| `text_object_unhovered` | El puntero sale de un enlace. |
| `text_object_clicked` | Se suelta una pulsación sobre el mismo enlace. |

Cada mensaje contiene estos campos:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | `hash` | El atributo `id` del objeto, o su id de objeto de layout generado. |
| `type` | `hash` | El tipo de objeto de layout, actualmente `hash("link")`. |
| `src` | `string` | El valor definido por la aplicación del atributo `src` del objeto, o una cadena vacía si no está presente. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Estilos con nombre {#named-styles}

Cada colección de fuentes contiene estilos de objeto con nombre que solo afectan al renderizado. Un enlace usa el estilo indicado por su atributo `style`, o `link` si el atributo no está presente. No existe una etiqueta general `<style>` para fragmentos.

Defold proporciona los siguientes valores predeterminados:

| Estilo | Multiplicador del color de relleno | Decoración |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Subrayado continuo |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Ninguna |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Ninguna |

Define un estilo con una cadena de texto que contenga etiquetas de apertura. Las etiquetas se cierran implícitamente en orden inverso, por lo que no se permiten etiquetas de cierre ni texto visible.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Las etiquetas se aplican de izquierda a derecha, como si estuvieran anidadas alrededor del texto del objeto. Un estilo de objeto seleccionado por quien llama se aplica después del estilo predeterminado. Cuando varias etiquetas definen la misma propiedad de renderizado, el valor aplicado después sobrescribe los anteriores. Los efectos se agregan en orden de izquierda a derecha.

::: sidenote
Llamar a `font.set_style()` reemplaza las propiedades de renderizado y los efectos de ese estilo con nombre. Las decoraciones definidas por el recurso no cambian, por lo que redefinir `link` no elimina su subrayado predeterminado. Los estilos con nombre aceptan etiquetas que solo afectan al renderizado, como `color`, `outline`, `shadow`, `gradient`, `wave` y `shake`. Se rechazan las etiquetas que cambian el layout, las de decoración y las de objetos.
:::

## API de objetos de layout {#layout-object-api}

Usa `label.get_layout_objects()` o `gui.get_layout_objects()` para obtener los objetos `sprite` y `link` del texto dispuesto.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Argumento | Tipo | Descripción |
| --- | --- | --- |
| `url` | `string`, `hash` o `url` | El componente Label que se va a consultar, por ejemplo `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Argumento | Tipo | Descripción |
| --- | --- | --- |
| `node` | `node` | El nodo de texto GUI que se va a consultar, por ejemplo `gui.get_node("rich_text")`. |

Ambas funciones devuelven un array nuevo que contiene los objetos de layout actuales en el orden del código fuente. Devuelven un array vacío cuando el texto no contiene etiquetas de objeto. Como los objetos y sus atributos se copian a Lua en cada llamada, guarda el resultado en caché y vuelve a consultarlo después de cambiar el texto u otra propiedad que cambie su layout.

### Campos del objeto devuelto {#returned-object-fields}

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `type` | `string` | `"sprite"` o `"link"`. |
| `id` | `hash` | Identificador de objeto usado en los mensajes de interacción. |
| `text_offset` | `number` | Posición con base cero en el texto visible, medida en puntos de código Unicode. Se excluye el marcado y las entidades cuentan como sus caracteres decodificados. Para un sprite, es su punto de inserción. |
| `text_length` | `number` | Longitud del texto visible encerrado, en puntos de código Unicode. Un sprite tiene longitud uno por su punto de código de sustitución de objeto U+FFFC insertado. |
| `width` | `number` | Ancho resuelto en unidades de layout de texto. Actualmente los enlaces tienen ancho cero. |
| `height` | `number` | Alto resuelto en unidades de layout de texto. Actualmente los enlaces tienen alto cero. |
| `x` | `number` | Posición horizontal de la esquina inferior izquierda del objeto respecto al origen superior izquierdo del layout de texto. |
| `y` | `number` | Posición vertical de la esquina inferior izquierda del objeto respecto al origen superior izquierdo del layout de texto. |
| `attributes` | `table` | Todos los atributos de la etiqueta como pares de clave/valor de tipo string. Los valores de los atributos conservan su representación de origen, como `"2em"`. Un valor abreviado sin nombre se almacena con la clave `value`. |

::: sidenote
`text_offset` y `text_length` no son desplazamientos en bytes UTF-8. Un carácter no ASCII como `å` o `猫` cuenta como una posición.
:::

### Ejemplo Lua {#lua-example}

```lua
local text = [[
Read the <link src=https://defold.com/manuals/ id=manual>manual</link>
or inspect <sprite src=images/info.png width=2em/> for more information.
]]

go.set("#label", "text", text)

local objects = label.get_layout_objects("#label")
for _, object in ipairs(objects) do
    if object.type == "link" then
        print("link", object.attributes.src)
        print("visible range", object.text_offset, object.text_length)
        print("position", object.x, object.y)
    elseif object.type == "sprite" then
        print("sprite", object.x, object.y, object.width, object.height)
        pprint(object.attributes)
    end
end

local gui_objects = gui.get_layout_objects(gui.get_node("rich_text"))
```

## Combinaciones útiles {#useful-combinations}

### Contorno de color con un degradado horizontal {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

El degradado multiplica solo el color de relleno; el contorno conserva su propio color.

### Hacer vibrar una frase y aplicar un degradado a una palabra {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

El efecto de posición externo se aplica a todos los glifos. El efecto de color anidado se aplica solo a “whole”.

### Sobrescribir una propiedad sin perder las demás {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

El color interno cambia el relleno mientras conserva el grosor y el color del contorno heredados.
