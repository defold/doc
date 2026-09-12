---
title: Znaczniki tekstu formatowanego w silniku Defold
brief: Ta instrukcja wyjaśnia, jak stylizować komponenty Label i węzły tekstowe GUI za pomocą znaczników tekstu formatowanego oraz jak odczytywać odnośniki i obrazy ze skryptów Lua.
---

# Znaczniki tekstu formatowanego {#rich-text-markup}

Używaj znaczników w komponentach Label i węzłach tekstowych GUI, aby stosować zagnieżdżone style wizualne i efekty oraz odczytywać odnośniki i obrazy ze skryptów Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Możesz też zdefiniować w foncie nazwany styl obiektu wielokrotnego użytku i wybrać go w odnośniku:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Przegląd znaczników {#tag-reference}

| Znacznik | Przeznaczenie | Przykład |
| --- | --- | --- |
| [`color`](#color) | Ustawia kolor wypełnienia glifu. | <img src="/manuals/images/richtext/color_green.webp" alt="Zielony tekst" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Zmienia kształtowanie glifów i rozmiar układu. | <img src="/manuals/images/richtext/size_24.webp" alt="Tekst o rozmiarze 24 pikseli" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Stosuje statyczny lub animowany gradient kolorów. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Tekst z poziomym gradientem" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Podkreśla tekst. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Podkreślony tekst" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Przekreśla tekst. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Przekreślony tekst" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Ustawia szerokość i kolor obrysu glifu. | <img src="/manuals/images/richtext/outline.webp" alt="Tekst z obrysem" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Dodaje cień do tekstu. | <img src="/manuals/images/richtext/shadow.webp" alt="Tekst z cieniem" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Stosuje animowane przesunięcie losowe. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Drżący tekst" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Porusza tekstem w animowanej fali sinusoidalnej. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Falujący tekst" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Dodaje obiekt sprite w wierszu tekstu. | <img src="/manuals/images/richtext/sprite.webp" alt="Obraz osadzony w tekście" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Dodaje interaktywny obiekt odnośnika. | <img src="/manuals/images/richtext/link.webp" alt="Tekst odnośnika" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Składnia {#syntax}

W nazwach znaczników i atrybutów wielkość liter ma znaczenie. Znacznik z parą otwierającą i zamykającą dotyczy widocznego tekstu UTF-32 wewnątrz niego. Obiekty sprite używają znaczników samozamykających.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Atrybuty {#attributes}

Wartości atrybutów mogą być zapisane bez cudzysłowów, jeśli nie zawierają białych znaków, lub ujęte w pojedyncze albo podwójne cudzysłowy. `color` i `size` obsługują skrótowy zapis pierwszej wartości oraz postać z nazwą `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Zagnieżdżanie {#nesting}

Znaczniki trzeba zamykać w kolejności odwrotnej do ich otwierania. Wartości stylu wewnętrznego nadpisują tę samą właściwość stylu zewnętrznego. Różne właściwości łączą się ze sobą. Efekty fragmentów tekstu pozostają aktywne niezależnie, więc zagnieżdżone gradienty mnożą kolory, a zagnieżdżone efekty pozycji sumują przesunięcia.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Encje {#entities}

Dla zastrzeżonych znaków w widocznym tekście używaj `&amp;`, `&apos;`, `&gt;`, `&lt;` oraz `&quot;`. Encje numeryczne nie są obecnie obsługiwane.

## Znaczniki {#tags}

Znaczniki tekstu formatowanego stylizują otaczany fragment tekstu albo opisują obiekt, który można odczytać ze skryptu Lua. Znaczniki stylów używają odpowiadającego im znacznika zamykającego. Obiekt `sprite` jest samozamykający, natomiast `link` otacza tekst odnośnika.

### `color`

Ustawia kolor wypełnienia glifu. Kolory mają postać `#RRGGBB` lub `#RRGGBBAA`. Prefiks z symbolem hasza jest wymagany; `0xFF0000` i `FF0000` są nieprawidłowe. Wynik mnoży kolor bazowy etykiety lub mechanizmu renderującego.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `=color` lub `value=color` | Tak | Brak wartości domyślnej | Kolor wypełnienia w szesnastkowej postaci RGB lub RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Przykładowy tekst w nieprzezroczystym zielonym kolorze](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Przykładowy tekst w zielonym kolorze z połową krycia](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Zmienia kształtowanie glifów i rozmiar układu, a nie tylko skalę wierzchołków. Wartości względne zawsze odnoszą się do bazowego rozmiaru fontu układu. Nie łączą się kumulatywnie z otaczającym znacznikiem `size`.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `=size` lub `value=size` | Tak | Brak wartości domyślnej | Rozmiar bezwzględny, procent, wielokrotność rozmiaru bazowego lub przesunięcie ze znakiem względem rozmiaru bazowego, w jednej z poniższych postaci. |

| Postać | Przykład dla 32 px | Wynikowy rozmiar |
| --- | --- | --- |
| Sama liczba lub `px` | `24`, `24px` | 24 px |
| Procent rozmiaru bazowego | `120%` | 38.4 px |
| Wielokrotność rozmiaru bazowego | `2em` | 64 px |
| Przesunięcie ze znakiem względem rozmiaru bazowego | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Przykładowy tekst o rozmiarze 24 pikseli](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% z 32px*

![Przykładowy tekst o rozmiarze 120 procent z 32 pikseli](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em dla 32px*

![Przykładowy tekst o rozmiarze dwukrotnie większym niż bazowe 32 piksele](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Gradient przyjmuje dokładnie jeden kompletny zestaw atrybutów. Łączenie zestawów lub pominięcie jednego z atrybutów jest nieprawidłowe.

| Tryb | Wymagane atrybuty | Interpolacja |
| --- | --- | --- |
| Poziomy | `left`, `right` | Interpoluje między dwoma kolorami w poziomie. |
| Pionowy | `bottom`, `top` | Interpoluje między kolorem dolnym i górnym. |
| Czterech narożników | `tl`, `tr`, `bl`, `br` | Interpoluje między kolorami czterech wierzchołków. |

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `left`, `right` | Dla trybu poziomego | Brak | Kolory końców w poziomie, w postaci `#RRGGBB` lub `#RRGGBBAA`. Oba muszą być obecne. |
| `bottom`, `top` | Dla trybu pionowego | Brak | Kolory końców w pionie. Oba muszą być obecne. |
| `tl`, `tr`, `bl`, `br` | Dla trybu czterech narożników | Brak | Kolory lewego górnego, prawego górnego, lewego dolnego i prawego dolnego narożnika. Wszystkie cztery muszą być obecne. |
| `fit` | Nie | `span` | `glyph` próbkuje każdą pozycję ukształtowanego tekstu; `span` rozkłada gradient na całym tekście objętym znacznikiem. |
| `hz` | Nie | `0` | Liczba pełnych cykli przepływu na sekundę w zakresie `[0,)`; zero pozostawia gradient nieruchomy. |
| `direction` | Nie | `forward` | `forward` lub `reverse`. Steruje kierunkiem przepływu, gdy `hz` jest różne od zera. |

Gdy `fit` jest pominięte, `fit=span` rozkłada gradient na całym tekście objętym znacznikiem. `fit=glyph` próbkuje niezależnie każdą pozycję ukształtowanego tekstu. Opcjonalne `hz` określa liczbę pełnych cykli animacji przepływu na sekundę; domyślna wartość zero pozostawia gradient nieruchomy. Powtarzająca się, lustrzanie odbita rampa kolorów płynie bez przerwy i zawija się bez skoku koloru. Domyślnie używane jest `direction=forward`; użyj `direction=reverse`, aby odwrócić przepływ.

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

*Poziomy*

![Przykładowy tekst z poziomym gradientem od magenty do bieli](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Pionowy*

![Przykładowy tekst z pionowym niebieskim gradientem](images/richtext/gradient_vertical.webp)

</div>
</div>

**Cztery narożniki**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Przykładowy tekst z gradientem czterech narożników dopasowanym do każdego glifu](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Przykładowy tekst z gradientem czterech narożników dopasowanym do fragmentu tekstu](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animowany**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Animowany przepływający gradient dopasowany do każdego glifu](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Animowany przepływający gradient dopasowany do fragmentu tekstu](images/richtext/gradient_flow_span.webp)

</div>
</div>

Kolory gradientu mnożą bieżący kolor wypełnienia. Gradient wewnątrz `color=#808080` nie może więc utworzyć kanału jaśniejszego niż ten mnożnik bazowy.

### `ul`

Rysuje podkreślenie, korzystając z metryk podkreślenia fontu, jeśli są dostępne. Znacznik nie ma osobnego koloru: linia dziedziczy wynikowy kolor wypełnienia, w tym gradienty poziome, pionowe i czterech narożników.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `pattern` | Nie | `solid` | `solid` lub `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Ciągłe*

![Przykładowy tekst z ciągłym podkreśleniem](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Przerywane*

![Przykładowy tekst z przerywanym podkreśleniem](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Gradient*

![Przykładowy tekst z podkreśleniem gradientowym](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Rysuje linię przekreślającą otoczony tekst. Przyjmuje te same wartości `pattern` co `ul` i tak samo dziedziczy wynikowy kolor wypełnienia.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `pattern` | Nie | `solid` | `solid` lub `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Ciągłe*

![Przykładowy tekst z ciągłym przekreśleniem](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Przerywane*

![Przykładowy tekst z przerywanym przekreśleniem](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Ustawia szerokość obrysu, jego kolor lub oba parametry. Wymagany jest co najmniej jeden atrybut. Szerokość zero jawnie wyłącza obrys dla fragmentu tekstu.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `size` | Jeden z size/color | Dziedziczona; `0` dla domyślnego fontu | Szerokość w jednostkach układu, zakres `[0,)`. Przyrostki jednostek nie są akceptowane. |
| `color` | Jeden z size/color | Dziedziczony; `#000000` dla domyślnej etykiety | Jeden kolor obrysu w szesnastkowej postaci RGB (`#RRGGBB`) lub RGBA (`#RRGGBBAA`); składowa alfa steruje kryciem. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Zewnętrzny czarny obrys*

![Przykładowy tekst z zewnętrznym czarnym obrysem](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Dodaje twardy cień do otoczonego tekstu. Wymagany jest co najmniej jeden atrybut. Atrybuty pominięte przez zagnieżdżony znacznik zachowują wartości otaczającego cienia; atrybuty pominięte przez znacznik zewnętrzny zachowują bazowe wartości cienia fontu.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `color` | Nie | Dziedziczony; `#000000` dla domyślnej etykiety | Kolor cienia w postaci `#RRGGBB` lub `#RRGGBBAA`. |
| `x` | Nie | Dziedziczone; `0` dla domyślnego fontu | Poziome przesunięcie cienia w jednostkach układu. Wartości dodatnie przesuwają go w prawo. |
| `y` | Nie | Dziedziczone; `0` dla domyślnego fontu | Pionowe przesunięcie cienia w jednostkach układu. Wartości dodatnie przesuwają go w górę. |
| `blur` | Nie | Dziedziczone; `0` dla domyślnego fontu | Promień rozmycia w jednostkach układu, zakres `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Przykładowy tekst z przesuniętym cieniem](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Rozmycie cienia jest generowane i przechowywane w atlasie glifów. Fragment tekstu może żądać mniejszego rozmycia niż przygotowane w foncie; większe wartości są zachowywane w układzie, ale obecnie renderowanie używa największego rozmycia dostępnego w atlasie.
:::

### `shake`

Stosuje deterministyczne animowane przesunięcie losowe bez zmiany łamania wierszy ani granic układu. Efekt sam śledzi czas; skrypty nie muszą zmieniać tekstu etykiety w każdej klatce animacji.

| Atrybut | Wymagany | Domyślnie | Prawidłowe wartości | Znaczenie |
| --- | --- | --- | --- | --- |
| `hz` | Nie | 20 | `[0,)` | Liczba przejść do losowych pozycji docelowych na sekundę. Zero wstrzymuje efekt. |
| `amplitude` | Nie | 0.5 | `[0,)` | Maksymalne przesunięcie w jednostkach układu. |
| `fit` | Nie | `glyph` | `glyph` lub `span` | `glyph` próbkuje dla każdej jednostki ukształtowanych glifów przesunięcie zachowujące spójność klastrów. `span` przesuwa cały tekst objęty znacznikiem jako jedną sztywną całość. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Przykładowy tekst z animowanym drżeniem poszczególnych glifów](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Przykładowy tekst z animowanym drżeniem całego fragmentu](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Porusza znakami w górę i w dół w postaci animowanej fali sinusoidalnej, nie zmieniając łamania wierszy ani granic układu. Układ kumuluje czas animacji podczas aktualizacji.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `amplitude` | Nie | 1 | Maksymalne przesunięcie pionowe w jednostkach układu, zakres `[0,)`. |
| `hz` | Nie | 1 | Liczba pełnych cykli w czasie na sekundę, zakres `[0,)`. Zero wstrzymuje falę. |
| `wavelength` | Nie | 6 | Liczba pozycji widocznego tekstu UTF-32 na pełny cykl przestrzenny, zakres `[1,)`. Znaki kształtowane przez font wspólnie, takie jak znak bazowy i jego akcent łączący, poruszają się jako całość. |
| `fit` | Nie | `glyph` | `glyph` rozkłada falę przestrzenną wzdłuż tekstu. `span` nadaje całemu fragmentowi tekstu objętemu znacznikiem wspólne pionowe przesunięcie sinusoidalne. |
| `direction` | Nie | `forward` | `forward` zapewnia zwykły ruch. `reverse` odwraca kierunek przemieszczania się fali. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Przykładowy tekst z animowaną falą poszczególnych glifów](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Przykładowy tekst poruszający się jako jeden animowany fragment](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Dodaje samozamykający obiekt sprite w bieżącej pozycji widocznego tekstu. Jego atrybuty są zachowywane jako metadane dla `label.get_layout_objects()` i `gui.get_layout_objects()`.

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `id` | Nie | Generowany | Stały identyfikator, którego hasz trafia do pola `id` zwracanego obiektu układu. |
| `src` | Nie | Brak | Identyfikator zasobu sprite zdefiniowany przez aplikację, na przykład ścieżka obrazu lub atlasu w projekcie. |
| `animation` | Nie | Brak | Zdefiniowany przez aplikację identyfikator animacji w zasobie. |
| `width` | Nie | `1em` | Wynikowa szerokość obrazu. |
| `height` | Nie | `1em` | Wynikowa wysokość obrazu. |
| Dowolny inny atrybut | Nie | Nieobecny | Metadane zdefiniowane przez aplikację, zachowywane dla mechanizmu rozwiązywania obiektów i API obiektów układu. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Osadzony obraz po rozwiązaniu odwołania*

![Logo Defold wyrenderowane w wierszu tekstu](images/richtext/sprite.webp)

</div>
</div>

Wymiary przyjmują dodatnie wartości w jednostkach układu bez przyrostka albo z `px`, `em` lub `%`. Zarówno `em`, jak i `%` używają bazowego rozmiaru fontu układu tekstu.

Każdy pominięty wymiar domyślnie przyjmuje niezależnie wartość `1em`. Pominięcie obu tworzy obiekt `1em × 1em`; podanie samej szerokości nie wyznacza automatycznie wysokości na podstawie proporcji zasobu.

::: important
Znacznik sprite jest jedynie symbolem zastępczym pozwalającym programiście umieścić w tym miejscu dowolny obiekt!
:::

### `link`

Opisuje zakres widocznego tekstu jako obiekt odnośnika. Otoczony tekst jest układany normalnie i domyślnie otrzymuje nazwany styl `link`. Komponenty Label i GUI wybierają `link:hover` i `link:active` w odpowiedzi na wejście, bez ponownego kształtowania tekstu. Wiadomości powstające podczas obsługi wejścia odnośnika opisano w sekcji [wiadomości interakcji](#interaction-messages).

| Atrybut | Wymagany | Domyślnie | Znaczenie |
| --- | --- | --- | --- |
| `src` | Nie | Brak | Cel odnośnika zdefiniowany przez aplikację. Wartość jest zwracana jako ciąg znaków, bez automatycznej weryfikacji ani przechodzenia do celu. |
| `id` | Nie | Generowany | Stały identyfikator, którego hasz trafia do pola `id` zwracanego obiektu układu. |
| `style` | Nie | `link` | Nazwany styl domyślny tekstu odnośnika. |
| Dowolny inny atrybut | Nie | Nieobecny | Metadane zdefiniowane przez aplikację, takie jak identyfikator, akcja, podpowiedź lub wartość analityczna. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com wyrenderowane z domyślnym stylem odnośnika i podkreśleniem](images/richtext/link.webp)

</div>
</div>

Komponent śledzi stan wskaźnika dla każdego odnośnika. Stosuje `link:hover`, gdy wskaźnik znajduje się nad odnośnikiem, i `link:active`, gdy wskaźnik jest naciśnięty. Gdy żaden z tych stanów nie występuje, komponent przywraca styl wskazany przez atrybut `style` odnośnika albo `link`, jeśli atrybut jest nieobecny.

### Wiadomości interakcji {#interaction-messages}

Interakcja z odnośnikami korzysta ze zwykłego systemu wejścia Defold. Dodaj wiązanie Mouse Trigger dla `MOUSE_BUTTON_LEFT`, które włącza też obsługę pojedynczego dotyku, i przejmij fokus wejścia w skrypcie obiektu gry lub skrypcie GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Szczegóły konfiguracji znajdziesz w sekcjach [fokus wejścia](/manuals/input/#input-focus) oraz [wejście myszy i dotyku](/manuals/input-mouse-and-touch).

Gdy komponent etykiety lub GUI otrzymuje wejście wskaźnika, odnośniki generują poniższe wiadomości. Wiadomości etykiety trafiają do obiektu gry, do którego należy komponent; wiadomości GUI trafiają do skryptu GUI.

| Wiadomość | Kiedy jest wysyłana |
| --- | --- |
| `text_object_hovered` | Wskaźnik wchodzi w obszar odnośnika. |
| `text_object_unhovered` | Wskaźnik opuszcza obszar odnośnika. |
| `text_object_clicked` | Naciśnięcie zostaje zwolnione nad tym samym odnośnikiem. |

Każda wiadomość zawiera następujące pola:

| Pole | Typ | Opis |
| --- | --- | --- |
| `id` | `hash` | Atrybut `id` obiektu lub jego wygenerowany identyfikator obiektu układu. |
| `type` | `hash` | Typ obiektu układu, obecnie `hash("link")`. |
| `src` | `string` | Zdefiniowana przez aplikację wartość atrybutu `src` obiektu lub pusty ciąg, jeśli atrybut jest nieobecny. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Nazwane style {#named-styles}

Każda kolekcja fontów zawiera nazwane style obiektów wpływające wyłącznie na renderowanie. Odnośnik używa stylu wskazanego przez atrybut `style` albo `link`, jeśli atrybut jest nieobecny. Nie ma ogólnego znacznika fragmentu tekstu `<style>`.

Defold dostarcza następujące ustawienia domyślne:

| Styl | Mnożnik koloru wypełnienia | Dekoracja |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Ciągłe podkreślenie |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Brak |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Brak |

Zdefiniuj styl za pomocą ciągu tekstowego zawierającego znaczniki otwierające. Znaczniki są niejawnie zamykane w odwrotnej kolejności, dlatego znaczniki zamykające i widoczny tekst są niedozwolone.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Znaczniki są stosowane od lewej do prawej, jak gdyby były zagnieżdżone wokół tekstu obiektu. Styl obiektu wybrany przez wywołującego jest stosowany po stylu domyślnym. Gdy kilka znaczników ustawia tę samą właściwość renderowania, późniejsza wartość nadpisuje wcześniejsze. Efekty są dodawane w kolejności od lewej do prawej.

::: sidenote
Wywołanie `font.set_style()` zastępuje właściwości renderowania i efekty danego nazwanego stylu. Dekoracje zdefiniowane w zasobie pozostają niezmienione, dlatego ponowne zdefiniowanie `link` nie usuwa jego domyślnego podkreślenia. Nazwane style przyjmują znaczniki dotyczące tylko renderowania, takie jak `color`, `outline`, `shadow`, `gradient`, `wave` i `shake`. Znaczniki zmieniające układ, dekoracje i znaczniki obiektów są odrzucane.
:::

## API obiektów układu {#layout-object-api}

Użyj `label.get_layout_objects()` lub `gui.get_layout_objects()`, aby pobrać obiekty `sprite` i `link` z ułożonego tekstu.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Argument | Typ | Opis |
| --- | --- | --- |
| `url` | `string`, `hash` lub `url` | Komponent etykiety do odczytania, na przykład `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Argument | Typ | Opis |
| --- | --- | --- |
| `node` | `node` | Węzeł tekstowy GUI do odczytania, na przykład `gui.get_node("rich_text")`. |

Obie funkcje zwracają nowo utworzoną tablicę zawierającą bieżące obiekty układu w kolejności źródłowej. Zwracają pustą tablicę, jeśli tekst nie zawiera znaczników obiektów. Ponieważ obiekty i ich atrybuty są kopiowane do Lua przy każdym wywołaniu, zapisz wynik w pamięci podręcznej i pobierz go ponownie po zmianie tekstu lub innej właściwości wpływającej na jego układ.

### Pola zwracanego obiektu {#returned-object-fields}

| Pole | Typ | Opis |
| --- | --- | --- |
| `type` | `string` | `"sprite"` lub `"link"`. |
| `id` | `hash` | Identyfikator obiektu używany w wiadomościach interakcji. |
| `text_offset` | `number` | Pozycja w widocznym tekście liczona od zera, w punktach kodowych Unicode. Znaczniki są pomijane, a encje są liczone jako zdekodowane znaki. Dla obrazu jest to punkt wstawienia. |
| `text_length` | `number` | Długość otoczonego widocznego tekstu w punktach kodowych Unicode. Obraz ma długość jeden ze względu na wstawiony znak zastępujący obiekt o punkcie kodowym U+FFFC. |
| `width` | `number` | Wynikowa szerokość w jednostkach układu tekstu. Odnośniki mają obecnie szerokość zero. |
| `height` | `number` | Wynikowa wysokość w jednostkach układu tekstu. Odnośniki mają obecnie wysokość zero. |
| `x` | `number` | Pozioma pozycja lewego dolnego narożnika obiektu względem początku układu tekstu w lewym górnym rogu. |
| `y` | `number` | Pionowa pozycja lewego dolnego narożnika obiektu względem początku układu tekstu w lewym górnym rogu. |
| `attributes` | `table` | Wszystkie atrybuty znacznika jako pary klucz/wartość będące ciągami znaków. Wartości atrybutów zachowują postać źródłową, na przykład `"2em"`. Skrótowa wartość bez nazwy jest przechowywana pod kluczem `value`. |

::: sidenote
`text_offset` i `text_length` nie są przesunięciami bajtowymi UTF-8. Znak spoza ASCII, taki jak `å` lub `猫`, zajmuje jedną pozycję.
:::

### Przykład Lua {#lua-example}

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

## Przydatne połączenia {#useful-combinations}

### Kolorowy obrys z poziomym gradientem {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Gradient mnoży tylko kolor wypełnienia; obrys zachowuje własny kolor.

### Drżenie zdania z gradientem jednego słowa {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Zewnętrzny efekt pozycji dotyczy każdego glifu. Zagnieżdżony efekt koloru dotyczy tylko słowa „whole”.

### Nadpisywanie jednej właściwości z zachowaniem pozostałych {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Kolor wewnętrzny zmienia wypełnienie, zachowując odziedziczoną szerokość i kolor obrysu.
