---
title: Rich-Text-Markup in Defold
brief: Dieses Handbuch erklärt, wie du Beschriftungskomponenten und GUI-Textknoten mit Rich-Text-Markup gestaltest und Links und Sprites in Lua untersuchst.
---

# Rich-Text-Markup

Verwende Markup in Beschriftungskomponenten (Label components) und GUI-Textknoten (GUI text nodes), um verschachtelte visuelle Stile und Effekte anzuwenden und Links und Sprites in Lua zu untersuchen.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Alternativ kannst du einen wiederverwendbaren benannten Objektstil für die Schriftressource definieren und ihn in einem Link auswählen:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Tag-Referenz {#tag-reference}

| Tag | Zweck | Beispiel |
| --- | --- | --- |
| [`color`](#color) | Legt die Füllfarbe der Glyphen fest. | <img src="/manuals/images/richtext/color_green.webp" alt="Grüner Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Ändert die Glyphenformung und die Layoutgröße. | <img src="/manuals/images/richtext/size_24.webp" alt="Text mit einer Größe von 24 Pixeln" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Wendet einen statischen oder animierten Farbverlauf an. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Text mit einem horizontalen Farbverlauf" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Unterstreicht Text. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Unterstrichener Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Streicht Text durch. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Durchgestrichener Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Legt die Breite und Farbe der Glyphenkontur fest. | <img src="/manuals/images/richtext/outline.webp" alt="Text mit Kontur" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Fügt Text einen Schatten hinzu. | <img src="/manuals/images/richtext/shadow.webp" alt="Text mit einem Schatten" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Wendet einen animierten zufälligen Versatz an. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Zitternder Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Bewegt Text in einer animierten Sinuswelle. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Wellenförmig bewegter Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Fügt ein Sprite-Objekt in den Textfluss ein. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite im Textfluss" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Fügt ein interaktives Link-Objekt hinzu. | <img src="/manuals/images/richtext/link.webp" alt="Verlinkter Text" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Syntax

Bei Tags und Attributnamen wird zwischen Groß- und Kleinschreibung unterschieden. Ein Tag-Paar wirkt auf den darin enthaltenen sichtbaren UTF-32-Text. Sprite-Objekte verwenden selbstschließende Tags.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Attribute {#attributes}

Attributwerte dürfen ohne Anführungszeichen stehen, wenn sie keine Leerraumzeichen enthalten, oder in einfachen oder doppelten Anführungszeichen eingeschlossen sein. `color` und `size` unterstützen sowohl einen ersten Wert in Kurzschreibweise als auch die benannte Form `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Verschachtelung {#nesting}

Tags müssen in umgekehrter Reihenfolge ihres Öffnens geschlossen werden. Innere Stilwerte überschreiben dieselbe Eigenschaft eines äußeren Stils. Unterschiedliche Eigenschaften werden kombiniert. Effekte auf Textbereiche bleiben unabhängig voneinander aktiv. Verschachtelte Farbverläufe multiplizieren daher ihre Farben, und verschachtelte Positionseffekte addieren ihre Versätze.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Entitäten {#entities}

Verwende `&amp;`, `&apos;`, `&gt;`, `&lt;` und `&quot;` für reservierte Zeichen im sichtbaren Text. Numerische Entitäten werden derzeit nicht unterstützt.

## Tags

Rich-Text-Tags gestalten entweder einen eingeschlossenen Textbereich oder beschreiben ein Objekt, das in Lua untersucht werden kann. Stil-Tags verwenden ein passendes schließendes Tag. Das Objekt `sprite` ist selbstschließend, während `link` den verlinkten Text einschließt.

### `color`

Legt die Füllfarbe der Glyphen fest. Farben verwenden `#RRGGBB` oder `#RRGGBBAA`. Das vorangestellte Rautezeichen ist erforderlich; `0xFF0000` und `FF0000` sind ungültig. Das Ergebnis multipliziert die Grundfarbe der Beschriftung oder des Renderers.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `=color` oder `value=color` | Ja | Kein Standardwert | Füllfarbe in hexadezimaler RGB- oder RGBA-Form. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Beispieltext in deckendem Grün](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Beispieltext in Grün mit halbem Alphawert](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Ändert die Glyphenformung und die Layoutgröße, nicht nur die Vertex-Skalierung. Relative Werte beziehen sich immer auf die Basisschriftgröße des Layouts. Sie werden nicht mit einem umschließenden `size`-Tag verrechnet.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `=size` oder `value=size` | Ja | Kein Standardwert | Absolute Größe, Prozentsatz, Vielfaches der Basisgröße oder vorzeichenbehafteter Versatz gegenüber der Basisgröße in einer der folgenden Formen. |

| Form | Beispiel bei 32 px | Berechnete Größe |
| --- | --- | --- |
| Zahl ohne Einheit oder `px` | `24`, `24px` | 24 px |
| Prozentsatz der Basisgröße | `120%` | 38,4 px |
| Vielfaches der Basisgröße | `2em` | 64 px |
| Vorzeichenbehafteter Versatz gegenüber der Basisgröße | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Beispieltext mit einer Größe von 24 Pixeln](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% von 32px*

![Beispieltext mit 120 Prozent von 32 Pixeln](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em bei 32px*

![Beispieltext mit dem Doppelten der Basisgröße von 32 Pixeln](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Ein Farbverlauf akzeptiert genau einen vollständigen Attributsatz. Das Mischen von Sätzen oder das Auslassen eines zugehörigen Attributs ist ungültig.

| Modus | Erforderliche Attribute | Interpolation |
| --- | --- | --- |
| Horizontal | `left`, `right` | Interpoliert zwischen den beiden horizontalen Farben. |
| Vertikal | `bottom`, `top` | Interpoliert zwischen der unteren und der oberen Farbe. |
| Vier Ecken | `tl`, `tr`, `bl`, `br` | Interpoliert zwischen vier Vertex-Farben. |

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `left`, `right` | Für den horizontalen Modus | Keiner | Farben der horizontalen Endpunkte in der Form `#RRGGBB` oder `#RRGGBBAA`. Beide müssen vorhanden sein. |
| `bottom`, `top` | Für den vertikalen Modus | Keiner | Farben der vertikalen Endpunkte. Beide müssen vorhanden sein. |
| `tl`, `tr`, `bl`, `br` | Für den Modus mit vier Ecken | Keiner | Farben oben links, oben rechts, unten links und unten rechts. Alle vier müssen vorhanden sein. |
| `fit` | Nein | `span` | `glyph` tastet jede geformte Textposition ab; `span` verteilt den Farbverlauf über den gesamten vom Tag eingeschlossenen Text. |
| `hz` | Nein | `0` | Vollständige Durchlaufzyklen pro Sekunde im Bereich `[0,)`; null hält den Farbverlauf statisch. |
| `direction` | Nein | `forward` | `forward` oder `reverse`. Steuert die Flussrichtung, wenn `hz` ungleich null ist. |

Wenn `fit` weggelassen wird, verteilt `fit=span` den Farbverlauf über den gesamten vom Tag eingeschlossenen Text. `fit=glyph` tastet jede geformte Textposition unabhängig ab. Das optionale Attribut `hz` gibt die Anzahl vollständiger Durchlaufzyklen der Animation pro Sekunde an; sein Standardwert null hält den Farbverlauf statisch. Die sich wiederholende, gespiegelte Farbskala fließt kontinuierlich und beginnt ohne Farbsprung wieder von vorn. `direction=forward` ist der Standardwert; verwende `direction=reverse`, um die Flussrichtung umzukehren.

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

![Beispieltext mit einem horizontalen Farbverlauf von Magenta zu Weiß](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Vertikal*

![Beispieltext mit einem vertikalen blauen Farbverlauf](images/richtext/gradient_vertical.webp)

</div>
</div>

**Vier Ecken**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Beispieltext mit einem an jede Glyphe angepassten Farbverlauf zwischen vier Ecken](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Beispieltext mit einem an den Textbereich angepassten Farbverlauf zwischen vier Ecken](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animiert**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Animierter fließender Farbverlauf, an jede Glyphe angepasst](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Animierter fließender Farbverlauf, an den Textbereich angepasst](images/richtext/gradient_flow_span.webp)

</div>
</div>

Die Farben des Farbverlaufs multiplizieren die aktuelle Füllfarbe. Ein Farbverlauf innerhalb von `color=#808080` kann daher keinen Farbkanal erzeugen, der heller als dieser Basismultiplikator ist.

### `ul`

Zeichnet eine Unterstreichung anhand der Unterstreichungsmetriken der Schriftart, sofern diese verfügbar sind. Das Tag hat keine eigene Farbe: Die Linie erbt die wirksame Füllfarbe, einschließlich horizontaler und vertikaler Farbverläufe sowie Farbverläufe zwischen vier Ecken.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `pattern` | Nein | `solid` | `solid` oder `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Durchgezogen*

![Beispieltext mit einer durchgezogenen Unterstreichung](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Gestrichelt*

![Beispieltext mit einer gestrichelten Unterstreichung](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Farbverlauf*

![Beispieltext mit einer Unterstreichung mit Farbverlauf](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Zeichnet eine Linie durch den eingeschlossenen Text. Akzeptiert dieselben Werte für `pattern` wie `ul` und erbt ebenfalls die wirksame Füllfarbe.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `pattern` | Nein | `solid` | `solid` oder `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Durchgezogen*

![Beispieltext mit einer durchgezogenen Durchstreichung](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Gestrichelt*

![Beispieltext mit einer gestrichelten Durchstreichung](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Legt die Konturbreite, die Konturfarbe oder beides fest. Mindestens ein Attribut ist erforderlich. Eine Breite von null deaktiviert die Kontur für den Textbereich ausdrücklich.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `size` | Eines von size/color | Geerbt; `0` bei einer Standardschriftart | Breite in Layout-Einheiten, Bereich `[0,)`. Einheitensuffixe werden nicht akzeptiert. |
| `color` | Eines von size/color | Geerbt; `#000000` bei einer Standardbeschriftung | Eine einzelne Konturfarbe in hexadezimaler RGB- (`#RRGGBB`) oder RGBA-Form (`#RRGGBBAA`); die Alpha-Komponente steuert die Deckkraft. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Äußere schwarze Kontur*

![Beispieltext mit einer äußeren schwarzen Kontur](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Fügt dem eingeschlossenen Text einen harten Schatten hinzu. Mindestens ein Attribut ist erforderlich. Attribute, die ein verschachteltes Tag auslässt, behalten den Schattenwert des umschließenden Tags bei; Attribute, die das äußerste Tag auslässt, behalten den Basisschattenwert der Schriftart bei.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `color` | Nein | Geerbt; `#000000` bei einer Standardbeschriftung | Schattenfarbe in der Form `#RRGGBB` oder `#RRGGBBAA`. |
| `x` | Nein | Geerbt; `0` bei einer Standardschriftart | Horizontaler Schattenversatz in Layout-Einheiten. Positive Werte verschieben ihn nach rechts. |
| `y` | Nein | Geerbt; `0` bei einer Standardschriftart | Vertikaler Schattenversatz in Layout-Einheiten. Positive Werte verschieben ihn nach oben. |
| `blur` | Nein | Geerbt; `0` bei einer Standardschriftart | Weichzeichnungsradius in Layout-Einheiten, Bereich `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Beispieltext mit einem versetzten Schatten](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Die Schattenweichzeichnung wird erzeugt und im Glyphenatlas gespeichert. Ein Textbereich kann eine geringere Weichzeichnung als die in der Schriftart vorberechnete Weichzeichnung anfordern; größere Werte bleiben im Layout erhalten, werden derzeit aber mit der größten im Atlas verfügbaren Weichzeichnung gerendert.
:::

### `shake`

Wendet einen deterministischen animierten zufälligen Versatz an, ohne den Zeilenumbruch oder die Layoutgrenzen zu ändern. Der Effekt verwaltet seine Zeit intern; Skripte müssen den Beschriftungstext nicht für jeden Animationsframe ändern.

| Attribut | Erforderlich | Standardwert | Gültige Werte | Bedeutung |
| --- | --- | --- | --- | --- |
| `hz` | Nein | 20 | `[0,)` | Übergänge zu zufälligen Zielen pro Sekunde. Null pausiert den Effekt. |
| `amplitude` | Nein | 0.5 | `[0,)` | Maximale Verschiebung in Layout-Einheiten. |
| `fit` | Nein | `glyph` | `glyph` oder `span` | `glyph` tastet für jede geformte Glypheneinheit einen Versatz ab, der zusammengehörige Zeichencluster erhält. `span` bewegt den gesamten vom Tag eingeschlossenen Textbereich als eine starre Einheit. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Beispieltext mit einem animierten Zittern jeder Glyphe](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Beispieltext mit einem animierten Zittern des gesamten Textbereichs](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Bewegt Zeichen in einer animierten Sinuswelle auf und ab, ohne den Zeilenumbruch oder die Layoutgrenzen zu ändern. Das Layout summiert bei jeder Aktualisierung die Animationszeit.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `amplitude` | Nein | 1 | Maximale vertikale Verschiebung in Layout-Einheiten, Bereich `[0,)`. |
| `hz` | Nein | 1 | Vollständige zeitliche Zyklen pro Sekunde, Bereich `[0,)`. Null pausiert die Welle. |
| `wavelength` | Nein | 6 | Sichtbare UTF-32-Textpositionen pro vollständigem räumlichem Zyklus, Bereich `[1,)`. Zeichen, die die Schriftart gemeinsam formt, etwa ein Basiszeichen und sein kombinierender Akzent, bewegen sich als Einheit. |
| `fit` | Nein | `glyph` | `glyph` wendet die räumliche Welle über den Text hinweg an. `span` gibt dem gesamten vom Tag eingeschlossenen Textbereich einen gemeinsamen vertikalen Sinusversatz. |
| `direction` | Nein | `forward` | `forward` bewegt die Welle normal vorwärts. `reverse` kehrt die Bewegungsrichtung der Welle um. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Beispieltext mit einer animierten Wellenbewegung jeder Glyphe](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Beispieltext, der sich als ein animierter Textbereich bewegt](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Fügt an der aktuellen Position im sichtbaren Text ein selbstschließendes Sprite-Objekt ein. Seine Attribute bleiben als Metadaten für `label.get_layout_objects()` und `gui.get_layout_objects()` erhalten.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `id` | Nein | Generiert | Stabiler Bezeichner, dessen Hash als `id` des zurückgegebenen Layout-Objekts verwendet wird. |
| `src` | Nein | Keiner | Von der Anwendung definierter Bezeichner einer Sprite-Ressource, etwa ein Projektpfad zu einem Bild oder Atlas. |
| `animation` | Nein | Keiner | Von der Anwendung definierter Animationsbezeichner innerhalb der Ressource. |
| `width` | Nein | `1em` | Berechnete Sprite-Breite. |
| `height` | Nein | `1em` | Berechnete Sprite-Höhe. |
| Beliebiges anderes Attribut | Nein | Nicht vorhanden | Von der Anwendung definierte Metadaten, die für die Objektauflösung und die Layout-Objekt-APIs erhalten bleiben. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Aufgelöstes Sprite im Textfluss*

![Ein im Textfluss gerendertes Defold-Logo](images/richtext/sprite.webp)

</div>
</div>

Abmessungen akzeptieren positive Layout-Einheiten ohne Suffix sowie `px`, `em` oder `%`. Sowohl `em` als auch `%` beziehen sich auf die Basisschriftgröße des Textlayouts.

Jede fehlende Abmessung erhält unabhängig den Standardwert `1em`. Werden beide weggelassen, entsteht ein Objekt mit `1em × 1em`; wird nur die Breite angegeben, wird die Höhe nicht automatisch aus dem Seitenverhältnis einer Ressource abgeleitet.

::: important
Das Sprite-Tag ist lediglich ein Platzhalter, an dessen Stelle du ein beliebiges Objekt einfügen kannst!
:::

### `link`

Beschreibt einen Bereich des sichtbaren Textes als Link-Objekt. Der eingeschlossene Text erhält das normale Layout und standardmäßig den benannten Stil `link`. Beschriftungs- und GUI-Komponenten wählen als Reaktion auf Eingaben `link:hover` und `link:active` aus, ohne den Text erneut zu formen. Unter [Interaktionsnachrichten](#interaction-messages) findest du die Nachrichten, die durch Eingaben auf Links erzeugt werden.

| Attribut | Erforderlich | Standardwert | Bedeutung |
| --- | --- | --- | --- |
| `src` | Nein | Keiner | Von der Anwendung definiertes Linkziel. Der Wert wird als Zeichenfolge ohne automatische Validierung oder Navigation zurückgegeben. |
| `id` | Nein | Generiert | Stabiler Bezeichner, dessen Hash als `id` des zurückgegebenen Layout-Objekts verwendet wird. |
| `style` | Nein | `link` | Benannter Standardstil für den Linktext. |
| Beliebiges anderes Attribut | Nein | Nicht vorhanden | Von der Anwendung definierte Metadaten, etwa ein Bezeichner, eine Aktion, ein Tooltip oder ein Analysewert. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com mit dem Standard-Linkstil und einer Unterstreichung gerendert](images/richtext/link.webp)

</div>
</div>

Die Komponente verfolgt den Zeigerzustand jedes Links. Sie wendet `link:hover` an, solange sich der Zeiger über dem Link befindet, und `link:active`, solange die Zeigereingabe gedrückt gehalten wird. Wenn keiner der beiden Zustände zutrifft, stellt die Komponente den im Attribut `style` des Links benannten Stil wieder her oder `link`, wenn das Attribut fehlt.

### Interaktionsnachrichten {#interaction-messages}

Die Interaktion mit Links verwendet Defolds normales Eingabesystem. Füge unter Mouse Trigger eine Eingabebindung (input binding) für `MOUSE_BUTTON_LEFT` hinzu, die auch Single-Touch-Eingaben aktiviert, und fordere den Eingabefokus im Skript des Spielobjekts (game object) oder im GUI-Skript an:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Einzelheiten zur Einrichtung findest du unter [Eingabefokus](/manuals/input/#input-focus) und [Maus- und Touch-Eingaben](/manuals/input-mouse-and-touch).

Wenn eine Beschriftungs- oder GUI-Komponente Zeigereingaben empfängt, erzeugen Links die folgenden Nachrichten. Beschriftungsnachrichten werden an das zugehörige Spielobjekt gesendet; GUI-Nachrichten werden an das GUI-Skript gesendet.

| Nachricht | Sendezeitpunkt |
| --- | --- |
| `text_object_hovered` | Der Zeiger tritt in einen Link ein. |
| `text_object_unhovered` | Der Zeiger verlässt einen Link. |
| `text_object_clicked` | Nach dem Drücken über einem Link wird über demselben Link losgelassen. |

Jede Nachricht enthält diese Felder:

| Feld | Typ | Beschreibung |
| --- | --- | --- |
| `id` | `hash` | Das Attribut `id` des Objekts oder seine generierte Layout-Objekt-ID. |
| `type` | `hash` | Der Typ des Layout-Objekts, derzeit `hash("link")`. |
| `src` | `string` | Der von der Anwendung definierte Wert des Attributs `src` des Objekts oder eine leere Zeichenfolge, wenn es fehlt. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Benannte Stile {#named-styles}

Jede Schriftsammlung (font collection) enthält benannte Objektstile, die ausschließlich das Rendering beeinflussen. Ein Link verwendet den im Attribut `style` benannten Stil oder `link`, wenn das Attribut fehlt. Es gibt kein allgemeines `<style>`-Tag für Textbereiche.

Defold stellt die folgenden Standardwerte bereit:

| Stil | Multiplikator der Füllfarbe | Textauszeichnung |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Durchgezogene Unterstreichung |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Keine |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Keine |

Definiere einen Stil mit einer Zeichenfolge, die öffnende Tags enthält. Die Tags werden implizit in umgekehrter Reihenfolge geschlossen; schließende Tags und sichtbarer Text sind daher nicht erlaubt.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Tags werden von links nach rechts angewendet, als wären sie um den Objekttext verschachtelt. Ein vom Aufrufer ausgewählter Objektstil wird nach dem Standardstil angewendet. Wenn mehrere Tags dieselbe Rendering-Eigenschaft setzen, überschreibt der später angewendete Wert die früheren Werte. Effekte werden in der Reihenfolge von links nach rechts angehängt.

::: sidenote
Ein Aufruf von `font.set_style()` ersetzt die Rendering-Eigenschaften und Effekte dieses benannten Stils. In der Ressource definierte Textauszeichnungen bleiben unverändert. Eine Neudefinition von `link` entfernt daher seine standardmäßige Unterstreichung nicht. Benannte Stile akzeptieren Tags, die ausschließlich das Rendering beeinflussen, etwa `color`, `outline`, `shadow`, `gradient`, `wave` und `shake`. Tags, die das Layout ändern, sowie Textauszeichnungs- und Objekt-Tags werden abgelehnt.
:::

## API für Layout-Objekte {#layout-object-api}

Verwende `label.get_layout_objects()` oder `gui.get_layout_objects()`, um die Objekte `sprite` und `link` aus Text mit berechnetem Layout abzurufen.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Argument | Typ | Beschreibung |
| --- | --- | --- |
| `url` | `string`, `hash` oder `url` | Die zu untersuchende Beschriftungskomponente, zum Beispiel `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Argument | Typ | Beschreibung |
| --- | --- | --- |
| `node` | `node` | Der zu untersuchende GUI-Textknoten, zum Beispiel `gui.get_node("rich_text")`. |

Beide Funktionen geben ein neu erstelltes Array mit den aktuellen Layout-Objekten in der Reihenfolge ihres Auftretens im Quelltext zurück. Sie geben ein leeres Array zurück, wenn der Text keine Objekt-Tags enthält. Da die Objekte und ihre Attribute bei jedem Aufruf nach Lua kopiert werden, speichere das Ergebnis zwischen und frage es erneut ab, nachdem du den Text oder eine andere Eigenschaft geändert hast, die sein Layout verändert.

### Zurückgegebene Objektfelder {#returned-object-fields}

| Feld | Typ | Beschreibung |
| --- | --- | --- |
| `type` | `string` | `"sprite"` oder `"link"`. |
| `id` | `hash` | Objektbezeichner, der in Interaktionsnachrichten verwendet wird. |
| `text_offset` | `number` | Bei null beginnende Position im sichtbaren Text, gemessen in Unicode-Codepunkten. Markup wird nicht mitgezählt, und Entitäten zählen als ihre dekodierten Zeichen. Bei einem Sprite ist dies seine Einfügeposition. |
| `text_length` | `number` | Länge des eingeschlossenen sichtbaren Textes in Unicode-Codepunkten. Ein Sprite hat die Länge eins für seinen eingefügten Codepunkt U+FFFC, das Objektersetzungszeichen. |
| `width` | `number` | Berechnete Breite in Textlayout-Einheiten. Links haben derzeit die Breite null. |
| `height` | `number` | Berechnete Höhe in Textlayout-Einheiten. Links haben derzeit die Höhe null. |
| `x` | `number` | Horizontale Position der unteren linken Ecke des Objekts relativ zum Ursprung oben links im Textlayout. |
| `y` | `number` | Vertikale Position der unteren linken Ecke des Objekts relativ zum Ursprung oben links im Textlayout. |
| `attributes` | `table` | Alle Tag-Attribute als Schlüssel-Wert-Paare aus Zeichenfolgen. Attributwerte behalten ihre Darstellung aus dem Quelltext bei, etwa `"2em"`. Ein unbenannter Wert in Kurzschreibweise wird unter dem Schlüssel `value` gespeichert. |

::: sidenote
`text_offset` und `text_length` sind keine UTF-8-Byte-Offsets. Ein Nicht-ASCII-Zeichen wie `å` oder `猫` zählt als eine Position.
:::

### Lua-Beispiel {#lua-example}

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

## Nützliche Kombinationen {#useful-combinations}

### Farbige Kontur mit horizontalem Farbverlauf {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Der Farbverlauf multipliziert nur die Füllfarbe; die Kontur behält ihre eigene Farbe.

### Einen Satz zittern lassen und ein Wort mit einem Farbverlauf versehen {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Der äußere Positionseffekt wirkt auf jede Glyphe. Der verschachtelte Farbeffekt wirkt nur auf „whole“.

### Eine Eigenschaft überschreiben, ohne die anderen zu verlieren {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Die innere Farbe ändert die Füllung und behält dabei die geerbte Konturbreite und -farbe bei.
