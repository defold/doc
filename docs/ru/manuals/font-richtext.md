---
title: Форматированная текстовая разметка в Defold
brief: В этом руководстве объясняется, как оформлять компоненты Label и GUI-ноды Text с помощью форматированной текстовой разметки и получать сведения о ссылках и спрайтах из Lua.
---

# Форматированная текстовая разметка {#rich-text-markup}

Используйте разметку в компонентах Label и GUI-нодах Text, чтобы применять вложенные визуальные стили и эффекты и получать сведения о ссылках и спрайтах из Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Также можно определить для шрифта переиспользуемый именованный стиль объекта и выбрать его в ссылке:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Справочник тегов {#tag-reference}

| Тег | Назначение | Пример |
| --- | --- | --- |
| [`color`](#color) | Задаёт цвет заполнения глифа. | <img src="/manuals/images/richtext/color_green.webp" alt="Зелёный текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Изменяет размер формирования и размещения глифов. | <img src="/manuals/images/richtext/size_24.webp" alt="Текст размером 24 пикселя" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Применяет статический или анимированный цветовой градиент. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Текст с горизонтальным градиентом" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Подчёркивает текст. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Подчёркнутый текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Перечёркивает текст. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Перечёркнутый текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Задаёт ширину и цвет обводки глифа. | <img src="/manuals/images/richtext/outline.webp" alt="Текст с обводкой" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Добавляет тень к тексту. | <img src="/manuals/images/richtext/shadow.webp" alt="Текст с тенью" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Применяет анимированное случайное смещение. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Трясущийся текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Перемещает текст по анимированной синусоиде. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Волнообразно движущийся текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Добавляет встроенный объект-спрайт. | <img src="/manuals/images/richtext/sprite.webp" alt="Встроенный спрайт" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Добавляет интерактивный объект-ссылку. | <img src="/manuals/images/richtext/link.webp" alt="Текст ссылки" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Синтаксис {#syntax}

Имена тегов и атрибутов чувствительны к регистру. Парный тег применяется к видимому тексту UTF-32 внутри него. Для объектов-спрайтов используются самозакрывающиеся теги.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Атрибуты {#attributes}

Значения атрибутов можно записывать без кавычек, если они не содержат пробельных символов, либо заключать в одинарные или двойные кавычки. `color` и `size` поддерживают сокращённую запись первого значения и именованную форму `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Вложенность {#nesting}

Теги должны закрываться в порядке, обратном открытию. Значения внутреннего стиля переопределяют те же свойства внешнего стиля. Разные свойства сочетаются. Эффекты фрагментов остаются активными независимо друг от друга, поэтому вложенные градиенты перемножают цвета, а вложенные эффекты положения складывают свои смещения.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Символьные ссылки {#entities}

Для зарезервированных символов в видимом тексте используйте `&amp;`, `&apos;`, `&gt;`, `&lt;` и `&quot;`. Числовые символьные ссылки пока не поддерживаются.

## Теги {#tags}

Теги форматированного текста либо оформляют заключённый в них фрагмент текста, либо описывают объект, о котором можно получить сведения из Lua. Теги стилей используют соответствующий закрывающий тег. Объект `sprite` самозакрывающийся, а `link` заключает в себе текст ссылки.

### `color` {#color}

Задаёт цвет заполнения глифа. Цвета записываются в формате `#RRGGBB` или `#RRGGBBAA`. Префикс решётки обязателен; значения `0xFF0000` и `FF0000` недопустимы. Результат умножается на базовый цвет метки или рендерера.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `=color` или `value=color` | Да | Нет значения по умолчанию | Цвет заполнения в шестнадцатеричном формате RGB или RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Пример текста непрозрачного зелёного цвета](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Пример зелёного текста с половинной непрозрачностью](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size` {#size}

Изменяет размер формирования и размещения глифов, а не только масштаб вершин. Относительные значения всегда используют базовый размер шрифта раскладки. Они не накапливаются с учётом внешнего тега `size`.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `=size` или `value=size` | Да | Нет значения по умолчанию | Абсолютный размер, процент, множитель базового размера или смещение от базового размера со знаком в одной из перечисленных ниже форм. |

| Форма | Пример при 32 px | Вычисленный размер |
| --- | --- | --- |
| Число без суффикса или `px` | `24`, `24px` | 24 px |
| Процент базового размера | `120%` | 38.4 px |
| Множитель базового размера | `2em` | 64 px |
| Смещение от базового размера со знаком | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Пример текста размером 24 пикселя](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% от 32px*

![Пример текста размером 120 процентов от 32 пикселей](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em при 32px*

![Пример текста вдвое больше базового размера 32 пикселя](images/richtext/size_2em.webp)

</div>
</div>

### `gradient` {#gradient}

Градиент принимает ровно один полный набор атрибутов. Смешивать наборы или пропускать отдельные атрибуты набора нельзя.

| Режим | Обязательные атрибуты | Интерполяция |
| --- | --- | --- |
| Горизонтальный | `left`, `right` | Интерполяция между двумя цветами по горизонтали. |
| Вертикальный | `bottom`, `top` | Интерполяция между нижним и верхним цветами. |
| Четыре угла | `tl`, `tr`, `bl`, `br` | Интерполяция между цветами четырёх вершин. |

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `left`, `right` | Для горизонтального режима | Нет | Цвета горизонтальных концов в формате `#RRGGBB` или `#RRGGBBAA`. Требуются оба. |
| `bottom`, `top` | Для вертикального режима | Нет | Цвета вертикальных концов. Требуются оба. |
| `tl`, `tr`, `bl`, `br` | Для режима четырёх углов | Нет | Цвета верхнего левого, верхнего правого, нижнего левого и нижнего правого углов. Требуются все четыре. |
| `fit` | Нет | `span` | `glyph` выполняет выборку для каждой позиции сформированного текста; `span` распределяет градиент по всему тексту внутри тега. |
| `hz` | Нет | `0` | Число полных циклов перетекания в секунду в диапазоне `[0,)`; ноль оставляет градиент неподвижным. |
| `direction` | Нет | `forward` | `forward` или `reverse`. Управляет направлением перетекания при ненулевом `hz`. |

Если `fit` не задан, `fit=span` распределяет градиент по всему тексту внутри тега. `fit=glyph` выполняет выборку для каждой позиции сформированного текста независимо. Необязательный `hz` задаёт число полных циклов анимации перетекания в секунду; его значение по умолчанию, ноль, оставляет градиент неподвижным. Повторяющаяся зеркальная цветовая шкала непрерывно перемещается и зацикливается без скачка цвета. По умолчанию используется `direction=forward`; задайте `direction=reverse`, чтобы изменить направление перетекания на обратное.

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

*Горизонтальный*

![Пример текста с горизонтальным градиентом от пурпурного к белому](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Вертикальный*

![Пример текста с вертикальным синим градиентом](images/richtext/gradient_vertical.webp)

</div>
</div>

**Четыре угла**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Пример текста с градиентом по четырём углам каждого глифа](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Пример текста с градиентом по четырём углам всего фрагмента](images/richtext/gradient_four_text.webp)

</div>
</div>

**Анимированный**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Анимированный перетекающий градиент для каждого глифа](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Анимированный перетекающий градиент для всего фрагмента](images/richtext/gradient_flow_span.webp)

</div>
</div>

Цвета градиента умножаются на текущий цвет заполнения. Поэтому градиент внутри `color=#808080` не может дать значение канала ярче этого базового множителя.

### `ul` {#ul}

Рисует подчёркивание, используя метрики подчёркивания шрифта, если они доступны. У тега нет собственного цвета: линия наследует итоговый цвет заполнения, включая горизонтальные, вертикальные градиенты и градиенты по четырём углам.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `pattern` | Нет | `solid` | `solid` или `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Сплошное*

![Пример текста со сплошным подчёркиванием](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Штриховое*

![Пример текста со штриховым подчёркиванием](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Градиент*

![Пример текста с градиентным подчёркиванием](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike` {#strike}

Рисует линию через заключённый в тег текст. Принимает те же значения `pattern`, что и `ul`, и также наследует итоговый цвет заполнения.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `pattern` | Нет | `solid` | `solid` или `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Сплошное*

![Пример текста, перечёркнутого сплошной линией](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Штриховое*

![Пример текста, перечёркнутого штриховой линией](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline` {#outline}

Задаёт ширину обводки, её цвет или оба параметра. Требуется хотя бы один атрибут. Нулевая ширина явно отключает обводку для фрагмента.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `size` | Один из size/color | Наследуется; `0` у шрифта по умолчанию | Ширина в единицах раскладки, диапазон `[0,)`. Суффиксы единиц не допускаются. |
| `color` | Один из size/color | Наследуется; `#000000` у метки по умолчанию | Единый цвет обводки в шестнадцатеричном формате RGB (`#RRGGBB`) или RGBA (`#RRGGBBAA`); альфа-компонент управляет непрозрачностью. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Внешняя чёрная обводка*

![Пример текста с внешней чёрной обводкой](images/richtext/outline.webp)

</div>
</div>

### `shadow` {#shadow}

Добавляет чёткую тень к заключённому в тег тексту. Требуется хотя бы один атрибут. Атрибуты, пропущенные во вложенном теге, сохраняют значения внешней тени; атрибуты, пропущенные в самом внешнем теге, сохраняют базовые значения тени шрифта.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `color` | Нет | Наследуется; `#000000` у метки по умолчанию | Цвет тени в формате `#RRGGBB` или `#RRGGBBAA`. |
| `x` | Нет | Наследуется; `0` у шрифта по умолчанию | Горизонтальное смещение тени в единицах раскладки. Положительные значения смещают её вправо. |
| `y` | Нет | Наследуется; `0` у шрифта по умолчанию | Вертикальное смещение тени в единицах раскладки. Положительные значения смещают её вверх. |
| `blur` | Нет | Наследуется; `0` у шрифта по умолчанию | Радиус размытия в единицах раскладки, диапазон `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Пример текста со смещённой тенью](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Размытие тени генерируется и хранится в атласе глифов. Фрагмент может запросить меньшее размытие, чем запечённое в шрифте; большие значения сохраняются в раскладке, но сейчас отрисовываются с максимальным размытием, доступным в атласе.
:::

### `shake` {#shake}

Применяет детерминированное анимированное случайное смещение, не меняя переносы строк или границы раскладки. Эффект самостоятельно отслеживает время; скриптам не нужно изменять текст метки для каждого кадра анимации.

| Атрибут | Обязательный | По умолчанию | Допустимые значения | Значение |
| --- | --- | --- | --- | --- |
| `hz` | Нет | 20 | `[0,)` | Число переходов к случайным целевым положениям в секунду. Ноль приостанавливает эффект. |
| `amplitude` | Нет | 0.5 | `[0,)` | Максимальное смещение в единицах раскладки. |
| `fit` | Нет | `glyph` | `glyph` или `span` | `glyph` выбирает смещение для каждой сформированной единицы глифов, сохраняя целостность кластеров. `span` перемещает весь текст внутри тега как единое целое. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Пример текста с анимированной тряской каждого глифа](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Пример текста с анимированной тряской всего фрагмента](images/richtext/shake_span.webp)

</div>
</div>

### `wave` {#wave}

Перемещает символы вверх и вниз по анимированной синусоиде, не меняя переносы строк или границы раскладки. При обновлении раскладка накапливает время анимации.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `amplitude` | Нет | 1 | Максимальное вертикальное смещение в единицах раскладки, диапазон `[0,)`. |
| `hz` | Нет | 1 | Число полных временных циклов в секунду, диапазон `[0,)`. Ноль приостанавливает волну. |
| `wavelength` | Нет | 6 | Число позиций видимого текста UTF-32 на полный пространственный цикл, диапазон `[1,)`. Символы, которые шрифт формирует вместе, например базовый символ и его комбинируемый знак ударения, движутся как единое целое. |
| `fit` | Нет | `glyph` | `glyph` применяет пространственную волну вдоль текста. `span` задаёт всему тексту внутри тега одно общее вертикальное синусоидальное смещение. |
| `direction` | Нет | `forward` | `forward` задаёт обычное движение. `reverse` меняет направление движения волны на обратное. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Пример текста с анимированной волной для каждого глифа](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Пример текста, движущегося как один анимированный фрагмент](images/richtext/wave_span.webp)

</div>
</div>

### `sprite` {#sprite}

Добавляет самозакрывающийся объект-спрайт в текущей позиции видимого текста. Его атрибуты сохраняются как метаданные для `label.get_layout_objects()` и `gui.get_layout_objects()`.

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `id` | Нет | Генерируется | Стабильный идентификатор, хеш которого возвращается в поле `id` объекта раскладки. |
| `src` | Нет | Нет | Заданный приложением идентификатор ресурса спрайта, например путь к изображению или атласу в проекте. |
| `animation` | Нет | Нет | Заданный приложением идентификатор анимации внутри ресурса. |
| `width` | Нет | `1em` | Вычисленная ширина спрайта. |
| `height` | Нет | `1em` | Вычисленная высота спрайта. |
| Любой другой атрибут | Нет | Отсутствует | Заданные приложением метаданные, сохраняемые для обработчика объектов и API объектов раскладки. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Встроенный спрайт после обработки*

![Логотип Defold, отрисованный в строке с текстом](images/richtext/sprite.webp)

</div>
</div>

Размеры принимают положительные значения в единицах раскладки без суффикса, `px`, `em` или `%`. И `em`, и `%` используют базовый размер шрифта текстовой раскладки.

Каждый из неуказанных размеров независимо получает значение `1em`. Если не задать оба, получится объект `1em × 1em`; при указании только ширины высота не вычисляется автоматически по соотношению сторон ресурса.

::: important
Тег sprite — лишь заполнитель, на место которого разработчик может поместить любой объект!
:::

### `link` {#link}

Описывает диапазон видимого текста как объект-ссылку. Заключённый в тег текст размещается обычным образом и по умолчанию получает именованный стиль `link`. Компоненты Label и GUI выбирают `link:hover` и `link:active` в ответ на ввод без повторного формирования текста. Сообщения, возникающие при взаимодействии со ссылкой, описаны в разделе [Сообщения взаимодействия](#interaction-messages).

| Атрибут | Обязательный | По умолчанию | Значение |
| --- | --- | --- | --- |
| `src` | Нет | Нет | Заданная приложением цель ссылки. Значение возвращается как строка без автоматической проверки или перехода. |
| `id` | Нет | Генерируется | Стабильный идентификатор, хеш которого возвращается в поле `id` объекта раскладки. |
| `style` | Нет | `link` | Именованный стиль по умолчанию для текста ссылки. |
| Любой другой атрибут | Нет | Отсутствует | Заданные приложением метаданные, например идентификатор, действие, подсказка или значение для аналитики. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com со стандартным стилем ссылки и подчёркиванием](images/richtext/link.webp)

</div>
</div>

Компонент отслеживает состояние указателя для каждой ссылки. Он применяет `link:hover`, пока указатель находится над ссылкой, и `link:active`, пока указатель нажат. Если ни одно из этих состояний не активно, компонент восстанавливает стиль, заданный атрибутом `style` ссылки, либо `link`, если атрибут отсутствует.

### Сообщения взаимодействия {#interaction-messages}

Взаимодействие со ссылками использует обычную систему ввода Defold. Добавьте привязку Mouse Trigger для `MOUSE_BUTTON_LEFT`, которая также включает одиночный сенсорный ввод, и получите фокус ввода в скрипте игрового объекта или GUI-скрипте:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Подробнее о настройке см. в разделах [Фокус ввода](/manuals/input/#input-focus) и [Ввод с помощью мыши и касаний](/manuals/input-mouse-and-touch).

Когда компонент Label или GUI получает ввод указателя, ссылки создают следующие сообщения. Сообщения Label отправляются игровому объекту, которому принадлежит компонент; сообщения GUI отправляются в GUI-скрипт.

| Сообщение | Когда отправляется |
| --- | --- |
| `text_object_hovered` | Указатель входит в область ссылки. |
| `text_object_unhovered` | Указатель покидает область ссылки. |
| `text_object_clicked` | Нажатие отпускается над той же ссылкой. |

Каждое сообщение содержит следующие поля:

| Поле | Тип | Описание |
| --- | --- | --- |
| `id` | `hash` | Атрибут `id` объекта или его сгенерированный идентификатор объекта раскладки. |
| `type` | `hash` | Тип объекта раскладки, в настоящее время `hash("link")`. |
| `src` | `string` | Заданное приложением значение атрибута `src` объекта или пустая строка, если он отсутствует. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Именованные стили {#named-styles}

Каждая коллекция шрифтов содержит именованные стили объектов, влияющие только на отрисовку. Ссылка использует стиль, заданный её атрибутом `style`, либо `link`, если атрибут отсутствует. Универсального тега `<style>` для фрагментов текста нет.

Defold предоставляет следующие значения по умолчанию:

| Стиль | Множитель цвета заполнения | Оформление |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Сплошное подчёркивание |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Нет |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Нет |

Определите стиль строкой текста, содержащей открывающие теги. Теги неявно закрываются в обратном порядке, поэтому закрывающие теги и видимый текст не допускаются.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Теги применяются слева направо, как если бы они были вложены вокруг текста объекта. Выбранный вызывающим кодом стиль объекта применяется после стиля по умолчанию. Если несколько тегов задают одно и то же свойство отрисовки, последнее применённое значение переопределяет предыдущие. Эффекты добавляются в порядке слева направо.

::: sidenote
Вызов `font.set_style()` заменяет свойства отрисовки и эффекты этого именованного стиля. Заданное в ресурсе оформление остаётся неизменным, поэтому переопределение `link` не удаляет его стандартное подчёркивание. Именованные стили принимают теги, влияющие только на отрисовку, такие как `color`, `outline`, `shadow`, `gradient`, `wave` и `shake`. Теги, изменяющие раскладку, теги оформления и теги объектов отклоняются.
:::

## API объектов раскладки {#layout-object-api}

Используйте `label.get_layout_objects()` или `gui.get_layout_objects()`, чтобы получить объекты `sprite` и `link` из размещённого текста.

### `label.get_layout_objects()` {#labelget_layout_objects}

```lua
objects = label.get_layout_objects(url)
```

| Аргумент | Тип | Описание |
| --- | --- | --- |
| `url` | `string`, `hash` или `url` | Компонент Label, о котором нужно получить сведения, например `"#label"`. |

### `gui.get_layout_objects()` {#guiget_layout_objects}

```lua
objects = gui.get_layout_objects(node)
```

| Аргумент | Тип | Описание |
| --- | --- | --- |
| `node` | `node` | GUI-нода Text, о которой нужно получить сведения, например `gui.get_node("rich_text")`. |

Обе функции возвращают новый массив с текущими объектами раскладки в порядке их появления в исходном тексте. Если в тексте нет тегов объектов, возвращается пустой массив. Поскольку при каждом вызове объекты и их атрибуты копируются в Lua, кэшируйте результат и повторяйте запрос после изменения текста или другого свойства, влияющего на раскладку.

### Поля возвращаемых объектов {#returned-object-fields}

| Поле | Тип | Описание |
| --- | --- | --- |
| `type` | `string` | `"sprite"` или `"link"`. |
| `id` | `hash` | Идентификатор объекта, используемый в сообщениях взаимодействия. |
| `text_offset` | `number` | Позиция в видимом тексте с отсчётом от нуля, измеряемая в кодовых точках Unicode. Разметка не учитывается, а символьные ссылки считаются как декодированные символы. Для спрайта это точка его вставки. |
| `text_length` | `number` | Длина заключённого в тег видимого текста в кодовых точках Unicode. Длина спрайта равна единице из-за вставленной кодовой точки U+FFFC, обозначающей заменяющий объект символ. |
| `width` | `number` | Вычисленная ширина в единицах текстовой раскладки. У ссылок ширина в настоящее время равна нулю. |
| `height` | `number` | Вычисленная высота в единицах текстовой раскладки. У ссылок высота в настоящее время равна нулю. |
| `x` | `number` | Горизонтальная позиция нижнего левого угла объекта относительно начала координат раскладки в её верхнем левом углу. |
| `y` | `number` | Вертикальная позиция нижнего левого угла объекта относительно начала координат раскладки в её верхнем левом углу. |
| `attributes` | `table` | Все атрибуты тега в виде строковых пар ключ/значение. Значения атрибутов сохраняют исходное представление, например `"2em"`. Сокращённое неименованное значение хранится под ключом `value`. |

::: sidenote
`text_offset` и `text_length` — не смещения в байтах UTF-8. Символ вне ASCII, например `å` или `猫`, занимает одну позицию.
:::

### Пример Lua {#lua-example}

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

## Полезные сочетания {#useful-combinations}

### Цветная обводка с горизонтальным градиентом {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Градиент умножает только цвет заполнения; обводка сохраняет собственный цвет.

### Тряска предложения и градиент для одного слова {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Внешний эффект положения применяется к каждому глифу. Вложенный цветовой эффект применяется только к слову «whole».

### Переопределение одного свойства с сохранением остальных {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Внутренний цвет меняет заполнение, сохраняя унаследованные ширину и цвет обводки.
