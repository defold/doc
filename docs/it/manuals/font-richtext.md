---
title: Markup del testo formattato in Defold
brief: Questo manuale spiega come applicare stili ai componenti Label e ai nodi di testo GUI con il markup del testo formattato e come esaminare link e sprite da Lua.
---

# Markup del testo formattato {#rich-text-markup}

Usa il markup nei componenti Label e nei nodi di testo GUI per applicare stili visivi ed effetti annidati ed esaminare link e sprite da Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

In alternativa, definisci sul font uno stile di oggetto riutilizzabile con nome e selezionalo da un link:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Riferimento dei tag {#tag-reference}

| Tag | Scopo | Esempio |
| --- | --- | --- |
| [`color`](#color) | Imposta il colore di riempimento dei glifi. | <img src="/manuals/images/richtext/color_green.webp" alt="Testo verde" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Modifica la dimensione dei glifi nella composizione e nel layout. | <img src="/manuals/images/richtext/size_24.webp" alt="Testo a 24 pixel" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Applica un gradiente di colore statico o animato. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Testo con gradiente orizzontale" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Sottolinea il testo. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Testo sottolineato" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Barra il testo. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Testo barrato" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Imposta spessore e colore del contorno dei glifi. | <img src="/manuals/images/richtext/outline.webp" alt="Testo con contorno" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Aggiunge un'ombra al testo. | <img src="/manuals/images/richtext/shadow.webp" alt="Testo con ombra" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Applica uno spostamento casuale animato. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Testo che trema" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Muove il testo lungo un'onda sinusoidale animata. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Testo che ondeggia" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Aggiunge un oggetto sprite in linea. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite in linea" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Aggiunge un oggetto link interattivo. | <img src="/manuals/images/richtext/link.webp" alt="Testo con link" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Sintassi {#syntax}

I nomi dei tag e degli attributi distinguono tra maiuscole e minuscole. Un tag con apertura e chiusura si applica al testo UTF-32 visibile che contiene. Gli oggetti sprite usano tag a chiusura automatica.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Attributi {#attributes}

Gli attributi possono essere scritti senza virgolette se non contengono spazi oppure racchiusi tra virgolette singole o doppie. `color` e `size` supportano sia un primo valore abbreviato sia la forma con nome `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Annidamento {#nesting}

I tag devono essere chiusi nell'ordine inverso rispetto a quello di apertura. I valori degli stili interni sovrascrivono la stessa proprietà di uno stile esterno. Le proprietà diverse si combinano. Gli effetti delle porzioni di testo rimangono attivi in modo indipendente: i gradienti annidati moltiplicano i colori e gli effetti di posizione annidati sommano i propri spostamenti.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Entità {#entities}

Usa `&amp;`, `&apos;`, `&gt;`, `&lt;` e `&quot;` per i caratteri riservati nel testo visibile. Le entità numeriche non sono attualmente supportate.

## Tag {#tags}

I tag del testo formattato applicano uno stile a una porzione di testo racchiusa al loro interno oppure descrivono un oggetto che puoi esaminare da Lua. I tag di stile usano un tag di chiusura corrispondente. L'oggetto `sprite` è a chiusura automatica, mentre `link` racchiude il testo del collegamento.

### `color`

Imposta il colore di riempimento dei glifi. I colori usano `#RRGGBB` o `#RRGGBBAA`. Il prefisso cancelletto è obbligatorio; `0xFF0000` e `FF0000` non sono validi. Il risultato moltiplica il colore di base dell'etichetta o del renderer.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `=color` o `value=color` | Sì | Nessun valore predefinito | Colore di riempimento in formato esadecimale RGB o RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Testo di esempio renderizzato in verde opaco](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Testo di esempio renderizzato in verde con alfa dimezzato](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Modifica la dimensione dei glifi nella composizione e nel layout, non soltanto la scala dei vertici. I valori relativi usano sempre la dimensione di base del font del layout. Non si moltiplicano con un tag `size` esterno.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `=size` o `value=size` | Sì | Nessun valore predefinito | Dimensione assoluta, percentuale, multiplo della dimensione di base oppure scostamento con segno dalla dimensione di base, usando una delle forme seguenti. |

| Forma | Esempio con 32 px | Dimensione risultante |
| --- | --- | --- |
| Numero senza unità o `px` | `24`, `24px` | 24 px |
| Percentuale della dimensione di base | `120%` | 38.4 px |
| Multiplo della dimensione di base | `2em` | 64 px |
| Scostamento con segno dalla dimensione di base | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Testo di esempio renderizzato a 24 pixel](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% di 32px*

![Testo di esempio renderizzato al 120 percento di 32 pixel](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em di 32px*

![Testo di esempio renderizzato al doppio della dimensione di base di 32 pixel](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Un gradiente accetta esattamente un insieme completo di attributi. Combinare insiemi diversi oppure omettere un membro non è valido.

| Modalità | Attributi obbligatori | Interpolazione |
| --- | --- | --- |
| Orizzontale | `left`, `right` | Interpola tra i due colori orizzontali. |
| Verticale | `bottom`, `top` | Interpola tra i colori inferiore e superiore. |
| Quattro angoli | `tl`, `tr`, `bl`, `br` | Interpola tra i colori dei quattro vertici. |

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `left`, `right` | Per la modalità orizzontale | Nessuno | Colori degli estremi orizzontali in formato `#RRGGBB` o `#RRGGBBAA`. Devono essere entrambi presenti. |
| `bottom`, `top` | Per la modalità verticale | Nessuno | Colori degli estremi verticali. Devono essere entrambi presenti. |
| `tl`, `tr`, `bl`, `br` | Per la modalità a quattro angoli | Nessuno | Colori in alto a sinistra, in alto a destra, in basso a sinistra e in basso a destra. Devono essere tutti e quattro presenti. |
| `fit` | No | `span` | `glyph` campiona ogni posizione del testo composto; `span` distribuisce il gradiente sull'intero testo racchiuso nel tag. |
| `hz` | No | `0` | Cicli completi di scorrimento al secondo nell'intervallo `[0,)`; zero mantiene statico il gradiente. |
| `direction` | No | `forward` | `forward` o `reverse`. Controlla la direzione dello scorrimento quando `hz` è diverso da zero. |

Quando `fit` è omesso, `fit=span` distribuisce il gradiente sull'intero testo racchiuso nel tag. `fit=glyph` campiona ogni posizione del testo composto in modo indipendente. L'attributo facoltativo `hz` specifica il numero di cicli completi di animazione dello scorrimento al secondo; il suo valore predefinito di zero mantiene statico il gradiente. La rampa di colori speculare e ripetuta scorre in modo continuo e ricomincia senza salti di colore. `direction=forward` è il valore predefinito; usa `direction=reverse` per invertire lo scorrimento.

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

*Orizzontale*

![Testo di esempio con un gradiente orizzontale dal magenta al bianco](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Verticale*

![Testo di esempio con un gradiente blu verticale](images/richtext/gradient_vertical.webp)

</div>
</div>

**Quattro angoli**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Testo di esempio con un gradiente a quattro angoli adattato a ogni glifo](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Testo di esempio con un gradiente a quattro angoli adattato alla porzione di testo](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animato**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Gradiente animato a scorrimento adattato a ogni glifo](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Gradiente animato a scorrimento adattato alla porzione di testo](images/richtext/gradient_flow_span.webp)

</div>
</div>

I colori del gradiente moltiplicano il colore di riempimento corrente. Un gradiente all'interno di `color=#808080` non può quindi produrre un canale più luminoso di quel moltiplicatore di base.

### `ul`

Disegna una sottolineatura usando le metriche di sottolineatura del font, quando disponibili. Il tag non ha un colore indipendente: la linea eredita il colore di riempimento effettivo, inclusi i gradienti orizzontali, verticali e a quattro angoli.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `pattern` | No | `solid` | `solid` o `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continua*

![Testo di esempio con sottolineatura continua](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tratteggiata*

![Testo di esempio con sottolineatura tratteggiata](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Gradiente*

![Testo di esempio con sottolineatura a gradiente](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Disegna una linea che barra il testo racchiuso nel tag. Accetta gli stessi valori di `pattern` di `ul` e ne eredita allo stesso modo il colore di riempimento effettivo.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `pattern` | No | `solid` | `solid` o `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Continua*

![Testo di esempio barrato con linea continua](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tratteggiata*

![Testo di esempio barrato con linea tratteggiata](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Imposta lo spessore del contorno, il suo colore o entrambi. È richiesto almeno un attributo. Uno spessore pari a zero disabilita esplicitamente il contorno per la porzione di testo.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `size` | Uno tra size/color | Ereditato; `0` in un font predefinito | Spessore in unità di layout, intervallo `[0,)`. Non sono accettati suffissi di unità. |
| `color` | Uno tra size/color | Ereditato; `#000000` in un'etichetta predefinita | Unico colore del contorno in formato esadecimale RGB (`#RRGGBB`) o RGBA (`#RRGGBBAA`); la componente alfa controlla l'opacità. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contorno nero esterno*

![Testo di esempio con un contorno nero esterno](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Aggiunge un'ombra dai bordi netti al testo racchiuso nel tag. È richiesto almeno un attributo. Gli attributi omessi da un tag annidato conservano il valore dell'ombra esterna; quelli omessi dal tag più esterno conservano il valore di base dell'ombra del font.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `color` | No | Ereditato; `#000000` in un'etichetta predefinita | Colore dell'ombra in formato `#RRGGBB` o `#RRGGBBAA`. |
| `x` | No | Ereditato; `0` in un font predefinito | Spostamento orizzontale dell'ombra in unità di layout. I valori positivi la spostano a destra. |
| `y` | No | Ereditato; `0` in un font predefinito | Spostamento verticale dell'ombra in unità di layout. I valori positivi la spostano verso l'alto. |
| `blur` | No | Ereditato; `0` in un font predefinito | Raggio di sfocatura in unità di layout, intervallo `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Testo di esempio con un'ombra spostata](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
La sfocatura dell'ombra viene generata e memorizzata nell'atlas dei glifi. Una porzione di testo può richiedere una sfocatura inferiore a quella precalcolata del font; i valori maggiori vengono conservati nel layout, ma attualmente sono renderizzati usando la massima sfocatura disponibile nell'atlas.
:::

### `shake`

Applica uno spostamento casuale animato deterministico senza modificare gli a capo o i limiti del layout. L'effetto tiene traccia del tempo internamente; gli script non devono modificare il testo dell'etichetta a ogni fotogramma dell'animazione.

| Attributo | Obbligatorio | Valore predefinito | Valori validi | Significato |
| --- | --- | --- | --- | --- |
| `hz` | No | 20 | `[0,)` | Transizioni verso posizioni casuali al secondo. Zero mette in pausa l'effetto. |
| `amplitude` | No | 0.5 | `[0,)` | Spostamento massimo in unità di layout. |
| `fit` | No | `glyph` | `glyph` o `span` | `glyph` campiona uno spostamento per ogni unità di glifo composta, senza separare i gruppi di caratteri. `span` muove l'intera porzione di testo racchiusa nel tag come un'unica unità rigida. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Testo di esempio con un tremolio animato per ogni glifo](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Testo di esempio con un tremolio animato dell'intera porzione di testo](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Muove i caratteri verso l'alto e il basso lungo un'onda sinusoidale animata senza modificare gli a capo o i limiti del layout. Il layout accumula il tempo di animazione quando viene aggiornato.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `amplitude` | No | 1 | Spostamento verticale massimo in unità di layout, intervallo `[0,)`. |
| `hz` | No | 1 | Cicli temporali completi al secondo, intervallo `[0,)`. Zero mette in pausa l'onda. |
| `wavelength` | No | 6 | Posizioni del testo UTF-32 visibile per ogni ciclo spaziale completo, intervallo `[1,)`. I caratteri che il font compone insieme, come un carattere di base e il suo accento combinante, si muovono come un'unica unità. |
| `fit` | No | `glyph` | `glyph` applica l'onda spaziale lungo il testo. `span` assegna all'intera porzione di testo racchiusa nel tag un unico spostamento sinusoidale verticale condiviso. |
| `direction` | No | `forward` | `forward` avanza normalmente. `reverse` inverte la direzione di propagazione dell'onda. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Testo di esempio con un'onda animata per ogni glifo](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Testo di esempio che si muove come un'unica porzione animata](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Aggiunge un oggetto sprite a chiusura automatica nella posizione corrente del testo visibile. I suoi attributi vengono conservati come metadati per `label.get_layout_objects()` e `gui.get_layout_objects()`.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `id` | No | Generato | Identificatore stabile trasformato in hash nel campo `id` dell'oggetto di layout restituito. |
| `src` | No | Nessuno | Identificatore della risorsa sprite definito dall'applicazione, come il percorso di un'immagine o di un atlas nel progetto. |
| `animation` | No | Nessuno | Identificatore di animazione all'interno della risorsa definito dall'applicazione. |
| `width` | No | `1em` | Larghezza risultante dello sprite. |
| `height` | No | `1em` | Altezza risultante dello sprite. |
| Qualsiasi altro attributo | No | Assente | Metadati definiti dall'applicazione e conservati per il risolutore degli oggetti e le API degli oggetti di layout. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Sprite in linea risolto*

![Un logo Defold renderizzato in linea con il testo](images/richtext/sprite.webp)

</div>
</div>

Le dimensioni accettano valori positivi in unità di layout senza suffisso, `px`, `em` o `%`. Sia `em` sia `%` usano la dimensione di base del font del layout del testo.

Ogni dimensione mancante assume indipendentemente il valore predefinito `1em`. Omettendole entrambe si ottiene un oggetto `1em × 1em`; specificare soltanto la larghezza non ricava automaticamente l'altezza dalle proporzioni della risorsa.

::: important
Il tag sprite è soltanto un segnaposto che permette allo sviluppatore di inserire un oggetto qualsiasi in quella posizione!
:::

### `link`

Descrive un intervallo di testo visibile come oggetto link. Il testo racchiuso viene disposto normalmente e riceve per impostazione predefinita lo stile con nome `link`. I componenti Label e GUI selezionano `link:hover` e `link:active` in risposta all'input senza ricomporre il testo. Consulta [Messaggi di interazione](#interaction-messages) per i messaggi prodotti dall'input sui link.

| Attributo | Obbligatorio | Valore predefinito | Significato |
| --- | --- | --- | --- |
| `src` | No | Nessuno | Destinazione del link definita dall'applicazione. Il valore viene restituito come stringa senza convalida o navigazione automatica. |
| `id` | No | Generato | Identificatore stabile trasformato in hash nel campo `id` dell'oggetto di layout restituito. |
| `style` | No | `link` | Stile predefinito con nome per il testo del link. |
| Qualsiasi altro attributo | No | Assente | Metadati definiti dall'applicazione, come un identificatore, un'azione, un suggerimento o un valore per l'analisi dell'utilizzo. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com renderizzato con lo stile predefinito dei link e una sottolineatura](images/richtext/link.webp)

</div>
</div>

Il componente tiene traccia dello stato del puntatore per ogni link. Applica `link:hover` mentre il puntatore è sopra il link e `link:active` mentre il pulsante del puntatore è premuto. Quando nessuno dei due stati è attivo, il componente ripristina lo stile indicato dall'attributo `style` del link, oppure `link` se l'attributo è assente.

### Messaggi di interazione {#interaction-messages}

L'interazione con i link usa il normale sistema di input di Defold. Aggiungi un binding Mouse Trigger per `MOUSE_BUTTON_LEFT`, che abilita anche l'input a tocco singolo, e acquisisci il focus dell'input nello script dell'oggetto di gioco o nello script GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Consulta [Focus dell'input](/manuals/input/#input-focus) e [Input da mouse e tocco](/manuals/input-mouse-and-touch) per i dettagli della configurazione.

Quando un componente etichetta o GUI riceve input dal puntatore, i link producono i messaggi seguenti. I messaggi delle etichette vengono inviati all'oggetto di gioco a cui appartengono; i messaggi GUI vengono inviati allo script GUI.

| Messaggio | Quando viene inviato |
| --- | --- |
| `text_object_hovered` | Il puntatore entra in un link. |
| `text_object_unhovered` | Il puntatore esce da un link. |
| `text_object_clicked` | Il pulsante viene rilasciato sopra lo stesso link su cui è stato premuto. |

Ogni messaggio contiene questi campi:

| Campo | Tipo | Descrizione |
| --- | --- | --- |
| `id` | `hash` | L'attributo `id` dell'oggetto oppure il suo ID generato di oggetto di layout. |
| `type` | `hash` | Il tipo dell'oggetto di layout, attualmente `hash("link")`. |
| `src` | `string` | Il valore definito dall'applicazione per l'attributo `src` dell'oggetto, oppure una stringa vuota se assente. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Stili con nome {#named-styles}

Ogni collezione di font contiene stili di oggetto con nome che influiscono soltanto sul rendering. Un link usa lo stile indicato dal suo attributo `style`, oppure `link` se l'attributo è assente. Non esiste un tag generico `<style>` per le porzioni di testo.

Defold fornisce i seguenti valori predefiniti:

| Stile | Moltiplicatore del colore di riempimento | Decorazione |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Sottolineatura continua |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Nessuna |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Nessuna |

Definisci uno stile con una stringa di testo contenente tag di apertura. I tag vengono chiusi implicitamente nell'ordine inverso, quindi non sono consentiti tag di chiusura né testo visibile.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

I tag vengono applicati da sinistra a destra, come se fossero annidati attorno al testo dell'oggetto. Uno stile di oggetto selezionato dal chiamante viene applicato dopo lo stile predefinito. Quando più tag impostano la stessa proprietà di rendering, il valore applicato per ultimo sovrascrive quelli precedenti. Gli effetti vengono aggiunti nell'ordine da sinistra a destra.

::: sidenote
Chiamare `font.set_style()` sostituisce le proprietà di rendering e gli effetti di quello stile con nome. Le decorazioni definite dalla risorsa rimangono invariate, quindi ridefinire `link` non rimuove la sua sottolineatura predefinita. Gli stili con nome accettano tag che influiscono soltanto sul rendering, come `color`, `outline`, `shadow`, `gradient`, `wave` e `shake`. I tag che modificano il layout, quelli di decorazione e quelli di oggetto vengono rifiutati.
:::

## API degli oggetti di layout {#layout-object-api}

Usa `label.get_layout_objects()` o `gui.get_layout_objects()` per recuperare gli oggetti `sprite` e `link` dal testo già disposto nel layout.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Argomento | Tipo | Descrizione |
| --- | --- | --- |
| `url` | `string`, `hash` o `url` | Il componente etichetta da esaminare, per esempio `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Argomento | Tipo | Descrizione |
| --- | --- | --- |
| `node` | `node` | Il nodo di testo GUI da esaminare, per esempio `gui.get_node("rich_text")`. |

Entrambe le funzioni restituiscono un array appena creato che contiene gli oggetti di layout correnti nell'ordine del sorgente. Restituiscono un array vuoto quando il testo non contiene tag di oggetto. Poiché gli oggetti e i loro attributi vengono copiati in Lua a ogni chiamata, conserva il risultato in cache e ripeti la richiesta dopo aver modificato il testo o un'altra proprietà che ne cambia il layout.

### Campi degli oggetti restituiti {#returned-object-fields}

| Campo | Tipo | Descrizione |
| --- | --- | --- |
| `type` | `string` | `"sprite"` o `"link"`. |
| `id` | `hash` | Identificatore dell'oggetto usato nei messaggi di interazione. |
| `text_offset` | `number` | Posizione nel testo visibile, con indice a partire da zero, misurata in punti di codice Unicode. Il markup è escluso e le entità contano come i caratteri decodificati. Per uno sprite, è il suo punto di inserimento. |
| `text_length` | `number` | Lunghezza del testo visibile racchiuso nel tag in punti di codice Unicode. Uno sprite ha lunghezza uno per il punto di codice U+FFFC di sostituzione dell'oggetto che viene inserito. |
| `width` | `number` | Larghezza risultante in unità di layout del testo. Attualmente i link hanno larghezza zero. |
| `height` | `number` | Altezza risultante in unità di layout del testo. Attualmente i link hanno altezza zero. |
| `x` | `number` | Posizione orizzontale dell'angolo inferiore sinistro dell'oggetto rispetto all'origine superiore sinistra del layout del testo. |
| `y` | `number` | Posizione verticale dell'angolo inferiore sinistro dell'oggetto rispetto all'origine superiore sinistra del layout del testo. |
| `attributes` | `table` | Tutti gli attributi dei tag come coppie chiave/valore di tipo stringa. I valori degli attributi conservano la rappresentazione sorgente, come `"2em"`. Un valore abbreviato senza nome viene memorizzato sotto la chiave `value`. |

::: sidenote
`text_offset` e `text_length` non sono offset in byte UTF-8. Un carattere non ASCII come `å` o `猫` conta come una posizione.
:::

### Esempio Lua {#lua-example}

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

## Combinazioni utili {#useful-combinations}

### Contorno colorato con un gradiente orizzontale {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Il gradiente moltiplica soltanto il colore di riempimento; il contorno mantiene il proprio colore.

### Far tremare una frase e applicare un gradiente a una parola {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

L'effetto di posizione esterno si applica a ogni glifo. L'effetto di colore annidato si applica soltanto a “whole”.

### Sovrascrivere una proprietà senza perdere le altre {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Il colore interno cambia il riempimento mantenendo lo spessore e il colore del contorno ereditati.
