---
title: Розмітка форматованого тексту в Defold
brief: Цей посібник пояснює, як оформлювати компоненти Label і текстові вузли GUI за допомогою розмітки форматованого тексту та як інспектувати посилання й спрайти з Lua.
---

# Розмітка форматованого тексту {#rich-text-markup}

Використовуйте розмітку в компонентах Label і текстових вузлах GUI, щоб застосовувати вкладені візуальні стилі й ефекти та інспектувати посилання й спрайти з Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Також можна визначити для шрифту іменований стиль об’єкта для повторного використання й вибрати його в посиланні:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Довідник тегів {#tag-reference}

| Тег | Призначення | Приклад |
| --- | --- | --- |
| [`color`](#color) | Задати колір заливки гліфа. | <img src="/manuals/images/richtext/color_green.webp" alt="Зелений текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Змінити формування гліфів і розмір компонування. | <img src="/manuals/images/richtext/size_24.webp" alt="Текст розміром 24 пікселі" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Застосувати статичний або анімований колірний градієнт. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Текст із горизонтальним градієнтом" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Підкреслити текст. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Підкреслений текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Закреслити текст. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Закреслений текст" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Задати товщину й колір обведення гліфа. | <img src="/manuals/images/richtext/outline.webp" alt="Текст з обведенням" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Додати тінь до тексту. | <img src="/manuals/images/richtext/shadow.webp" alt="Текст із тінню" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Застосувати анімоване випадкове зміщення. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Текст, що тремтить" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Рухати текст анімованою синусоїдальною хвилею. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Текст, що рухається хвилею" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Додати вбудований об’єкт спрайта. | <img src="/manuals/images/richtext/sprite.webp" alt="Вбудований спрайт" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Додати інтерактивний об’єкт посилання. | <img src="/manuals/images/richtext/link.webp" alt="Текст посилання" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Синтаксис {#syntax}

Назви тегів і атрибутів чутливі до регістру. Парний тег застосовується до видимого тексту UTF-32 усередині нього. Об’єкти спрайтів використовують самозакривні теги.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Атрибути {#attributes}

Атрибути можна записувати без лапок, якщо вони не містять пробільних символів, або в одинарних чи подвійних лапках. `color` і `size` підтримують скорочений запис першого значення, а також іменовану форму `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Вкладеність {#nesting}

Теги мають закриватися у зворотному порядку до відкриття: останній відкритий закривається першим. Значення внутрішнього стилю перевизначають ту саму властивість зовнішнього стилю. Різні властивості поєднуються. Ефекти фрагментів залишаються активними незалежно, тому вкладені градієнти перемножують кольори, а вкладені ефекти позиції додають свої зміщення.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Символьні посилання {#entities}

Для зарезервованих символів у видимому тексті використовуйте `&amp;`, `&apos;`, `&gt;`, `&lt;` і `&quot;`. Числові символьні посилання наразі не підтримуються.

## Теги {#tags}

Теги форматованого тексту або оформлюють охоплений фрагмент тексту, або описують об’єкт, який можна інспектувати з Lua. Теги стилів мають відповідний закривний тег. Об’єкт `sprite` є самозакривним, а `link` охоплює текст посилання.

### `color`

Задає колір заливки гліфа. Для кольорів використовуються `#RRGGBB` або `#RRGGBBAA`. Префікс решітки обов’язковий; `0xFF0000` і `FF0000` недопустимі. Результат множиться на базовий колір напису або засобу рендерингу.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `=color` або `value=color` | Так | Немає | Колір заливки в шістнадцятковій формі RGB або RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Текст прикладу, відображений непрозорим зеленим](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Текст прикладу, відображений напівпрозорим зеленим](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Змінює формування гліфів і розмір компонування, а не лише масштаб вершин. Відносні значення завжди використовують базовий розмір шрифту компонування. Вони не накопичуються з охоплювальним тегом `size`.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `=size` або `value=size` | Так | Немає | Абсолютний розмір, відсоток, кратне значення базового розміру або зміщення зі знаком від базового розміру в одній із наведених нижче форм. |

| Форма | Приклад для 32 px | Обчислений розмір |
| --- | --- | --- |
| Число без суфікса або `px` | `24`, `24px` | 24 px |
| Відсоток від базового розміру | `120%` | 38.4 px |
| Кратне значення базового розміру | `2em` | 64 px |
| Зміщення зі знаком від базового розміру | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Текст прикладу, відображений розміром 24 пікселі](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% від 32px*

![Текст прикладу, відображений розміром 120 відсотків від 32 пікселів](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em від 32px*

![Текст прикладу, відображений удвічі більшим за базовий розмір 32 пікселі](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Градієнт приймає рівно один повний набір атрибутів. Не можна змішувати набори або пропускати окремий атрибут набору.

| Режим | Обов’язкові атрибути | Інтерполяція |
| --- | --- | --- |
| Горизонтальний | `left`, `right` | Інтерполює між двома кольорами по горизонталі. |
| Вертикальний | `bottom`, `top` | Інтерполює між нижнім і верхнім кольорами. |
| За чотирма кутами | `tl`, `tr`, `bl`, `br` | Інтерполює між кольорами чотирьох вершин. |

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `left`, `right` | Для горизонтального режиму | Немає | Кольори горизонтальних кінцевих точок у формі `#RRGGBB` або `#RRGGBBAA`. Обидва обов’язкові. |
| `bottom`, `top` | Для вертикального режиму | Немає | Кольори вертикальних кінцевих точок. Обидва обов’язкові. |
| `tl`, `tr`, `bl`, `br` | Для режиму за чотирма кутами | Немає | Кольори верхнього лівого, верхнього правого, нижнього лівого й нижнього правого кутів. Усі чотири обов’язкові. |
| `fit` | Ні | `span` | `glyph` вибирає колір для кожної позиції сформованого тексту; `span` розподіляє градієнт по всьому тексту, охопленому тегом. |
| `hz` | Ні | `0` | Кількість повних циклів перетікання за секунду в діапазоні `[0,)`; нуль залишає градієнт статичним. |
| `direction` | Ні | `forward` | `forward` або `reverse`. Керує напрямком перетікання, коли `hz` не дорівнює нулю. |

Якщо `fit` не вказано, `fit=span` розподіляє градієнт по всьому тексту, охопленому тегом. `fit=glyph` незалежно вибирає колір для кожної позиції сформованого тексту. Необов’язковий `hz` задає кількість повних циклів анімації перетікання за секунду; його стандартне нульове значення залишає градієнт статичним. Повторювана дзеркальна шкала кольорів плавно перетікає й починається знову без стрибка кольору. За замовчуванням використовується `direction=forward`; задайте `direction=reverse`, щоб змінити напрямок перетікання.

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

*Горизонтальний*

![Текст прикладу з горизонтальним градієнтом від пурпурового до білого](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Вертикальний*

![Текст прикладу з вертикальним синім градієнтом](images/richtext/gradient_vertical.webp)

</div>
</div>

**За чотирма кутами**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Текст прикладу з градієнтом за чотирма кутами, застосованим до кожного гліфа](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Текст прикладу з градієнтом за чотирма кутами, застосованим до фрагмента](images/richtext/gradient_four_text.webp)

</div>
</div>

**Анімований**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Анімований градієнт із перетіканням, застосований до кожного гліфа](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Анімований градієнт із перетіканням, застосований до фрагмента](images/richtext/gradient_flow_span.webp)

</div>
</div>

Кольори градієнта множаться на поточний колір заливки. Тому градієнт усередині `color=#808080` не може створити канал, яскравіший за цей базовий множник.

### `ul`

Малює підкреслення, використовуючи метрики підкреслення шрифту, якщо вони доступні. Тег не має окремого кольору: лінія успадковує фактичний колір заливки, зокрема горизонтальні й вертикальні градієнти та градієнти за чотирма кутами.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `pattern` | Ні | `solid` | `solid` або `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Суцільний*

![Текст прикладу із суцільним підкресленням](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Штриховий*

![Текст прикладу зі штриховим підкресленням](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Градієнтний*

![Текст прикладу з градієнтним підкресленням](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Малює лінію крізь охоплений текст. Приймає ті самі значення `pattern`, що й `ul`, і так само успадковує фактичний колір заливки.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `pattern` | Ні | `solid` | `solid` або `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Суцільний*

![Текст прикладу із суцільним закресленням](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Штриховий*

![Текст прикладу зі штриховим закресленням](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Задає товщину обведення, його колір або обидва параметри. Потрібен щонайменше один атрибут. Нульова товщина явно вимикає обведення для фрагмента.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `size` | Один із size/color | Успадковується; `0` у стандартного шрифту | Товщина в одиницях компонування, діапазон `[0,)`. Суфікси одиниць не допускаються. |
| `color` | Один із size/color | Успадковується; `#000000` у стандартного напису | Один колір обведення в шістнадцятковій формі RGB (`#RRGGBB`) або RGBA (`#RRGGBBAA`); альфа-компонент керує непрозорістю. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Зовнішнє чорне обведення*

![Текст прикладу із зовнішнім чорним обведенням](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Додає чітку тінь до охопленого тексту. Потрібен щонайменше один атрибут. Атрибути, пропущені у вкладеному тегу, зберігають значення зовнішньої тіні; атрибути, пропущені в зовнішньому тегу найвищого рівня, зберігають базове значення тіні шрифту.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `color` | Ні | Успадковується; `#000000` у стандартного напису | Колір тіні у формі `#RRGGBB` або `#RRGGBBAA`. |
| `x` | Ні | Успадковується; `0` у стандартного шрифту | Горизонтальне зміщення тіні в одиницях компонування. Додатні значення зміщують її праворуч. |
| `y` | Ні | Успадковується; `0` у стандартного шрифту | Вертикальне зміщення тіні в одиницях компонування. Додатні значення зміщують її вгору. |
| `blur` | Ні | Успадковується; `0` у стандартного шрифту | Радіус розмиття в одиницях компонування, діапазон `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Текст прикладу зі зміщеною тінню](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Розмиття тіні генерується й зберігається в атласі гліфів. Фрагмент може запитати менше розмиття, ніж заздалегідь згенероване розмиття шрифту; більші значення зберігаються в компонуванні, але наразі рендеряться з найбільшим розмиттям, доступним в атласі.
:::

### `shake`

Застосовує детерміноване анімоване випадкове зміщення без зміни перенесення рядків або меж компонування. Ефект самостійно відстежує час; скриптам не потрібно змінювати текст напису для кожного кадру анімації.

| Атрибут | Обов’язковий | За замовчуванням | Допустимі значення | Значення |
| --- | --- | --- | --- | --- |
| `hz` | Ні | 20 | `[0,)` | Кількість переходів до випадкових цільових позицій за секунду. Нуль призупиняє ефект. |
| `amplitude` | Ні | 0.5 | `[0,)` | Максимальне зміщення в одиницях компонування. |
| `fit` | Ні | `glyph` | `glyph` або `span` | `glyph` вибирає зміщення для кожної сформованої одиниці гліфів, зберігаючи цілісність кластерів. `span` переміщує весь фрагмент тексту, охоплений тегом, як єдине жорстке ціле. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Текст прикладу з анімованим тремтінням окремих гліфів](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Текст прикладу з анімованим тремтінням усього фрагмента](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Рухає символи вгору й униз анімованою синусоїдальною хвилею без зміни перенесення рядків або меж компонування. Компонування накопичує час анімації під час оновлення.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `amplitude` | Ні | 1 | Максимальне вертикальне зміщення в одиницях компонування, діапазон `[0,)`. |
| `hz` | Ні | 1 | Кількість повних часових циклів за секунду, діапазон `[0,)`. Нуль призупиняє хвилю. |
| `wavelength` | Ні | 6 | Кількість позицій видимого тексту UTF-32 на повний просторовий цикл, діапазон `[1,)`. Символи, які шрифт формує разом, як-от базовий символ і його комбінований діакритичний знак, рухаються як одне ціле. |
| `fit` | Ні | `glyph` | `glyph` застосовує просторову хвилю вздовж тексту. `span` задає всьому фрагменту тексту, охопленому тегом, спільне вертикальне синусоїдальне зміщення. |
| `direction` | Ні | `forward` | `forward` рухає хвилю у звичайному напрямку. `reverse` змінює напрямок її руху на протилежний. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Текст прикладу з анімованим хвильовим рухом окремих гліфів](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Текст прикладу, що рухається як один анімований фрагмент](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Додає самозакривний об’єкт спрайта в поточній позиції видимого тексту. Його атрибути зберігаються як метадані для `label.get_layout_objects()` і `gui.get_layout_objects()`.

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `id` | Ні | Генерується | Стабільний ідентифікатор, хеш якого записується до `id` поверненого об’єкта компонування. |
| `src` | Ні | Немає | Визначений застосунком ідентифікатор ресурсу спрайта, як-от шлях зображення або атласу в проєкті. |
| `animation` | Ні | Немає | Визначений застосунком ідентифікатор анімації в ресурсі. |
| `width` | Ні | `1em` | Обчислена ширина спрайта. |
| `height` | Ні | `1em` | Обчислена висота спрайта. |
| Будь-який інший атрибут | Ні | Відсутній | Визначені застосунком метадані, що зберігаються для обробника об’єктів і API об’єктів компонування. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Відображений вбудований спрайт*

![Логотип Defold, відображений у рядку тексту](images/richtext/sprite.webp)

</div>
</div>

Розміри приймають додатні значення в одиницях компонування без суфікса, `px`, `em` або `%`. Як `em`, так і `%` використовують базовий розмір шрифту компонування тексту.

Кожен пропущений розмір незалежно приймає стандартне значення `1em`. Якщо пропустити обидва, утвориться об’єкт `1em × 1em`; якщо вказати лише ширину, висота не обчислюватиметься автоматично зі співвідношення сторін ресурсу.

::: important
Тег sprite — це лише заповнювач, на місці якого розробник може розмістити будь-який об’єкт!
:::

### `link`

Описує діапазон видимого тексту як об’єкт посилання. Охоплений текст компонується звичайним чином і за замовчуванням отримує іменований стиль `link`. Компоненти Label і GUI вибирають `link:hover` та `link:active` у відповідь на введення без повторного формування тексту. Про повідомлення, які виникають під час взаємодії з посиланням, читайте в розділі [Повідомлення взаємодії](#interaction-messages).

| Атрибут | Обов’язковий | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `src` | Ні | Немає | Визначена застосунком ціль посилання. Значення повертається як рядок без автоматичної перевірки або переходу. |
| `id` | Ні | Генерується | Стабільний ідентифікатор, хеш якого записується до `id` поверненого об’єкта компонування. |
| `style` | Ні | `link` | Іменований стандартний стиль тексту посилання. |
| Будь-який інший атрибут | Ні | Відсутній | Визначені застосунком метадані, як-от ідентифікатор, дія, підказка або значення для аналітики. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com зі стандартним стилем посилання й підкресленням](images/richtext/link.webp)

</div>
</div>

Компонент відстежує стан вказівника для кожного посилання. Він застосовує `link:hover`, поки вказівник перебуває над посиланням, і `link:active`, поки натискання утримується. Коли жоден із цих станів не діє, компонент відновлює стиль, указаний атрибутом `style` посилання, або `link`, якщо атрибут відсутній.

### Повідомлення взаємодії {#interaction-messages}

Взаємодія з посиланнями використовує звичайну систему введення Defold. Додайте прив’язку Mouse Trigger для `MOUSE_BUTTON_LEFT`, яка також вмикає введення одним дотиком, і отримайте фокус введення у скрипті ігрового об’єкта або скрипті GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Докладні відомості про налаштування наведено в розділах [Фокус введення](/manuals/input/#input-focus) і [Введення мишею й дотиком](/manuals/input-mouse-and-touch).

Коли компонент напису або GUI отримує введення від вказівника, посилання породжують наведені нижче повідомлення. Повідомлення написів надсилаються ігровому об’єкту, якому вони належать; повідомлення GUI — скрипту GUI.

| Повідомлення | Коли надсилається |
| --- | --- |
| `text_object_hovered` | Вказівник входить у ділянку посилання. |
| `text_object_unhovered` | Вказівник виходить із ділянки посилання. |
| `text_object_clicked` | Натискання відпущено над тим самим посиланням. |

Кожне повідомлення містить такі поля:

| Поле | Тип | Опис |
| --- | --- | --- |
| `id` | `hash` | Атрибут `id` об’єкта або його згенерований ідентифікатор об’єкта компонування. |
| `type` | `hash` | Тип об’єкта компонування, наразі `hash("link")`. |
| `src` | `string` | Визначене застосунком значення атрибута `src` об’єкта або порожній рядок, якщо атрибут відсутній. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Іменовані стилі {#named-styles}

Кожна колекція шрифтів містить іменовані стилі об’єктів, які впливають лише на рендеринг. Посилання використовує стиль, указаний його атрибутом `style`, або `link`, якщо атрибут відсутній. Загального тегу `<style>` для фрагментів немає.

Defold надає такі стандартні значення:

| Стиль | Множник кольору заливки | Декорування |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Суцільне підкреслення |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Немає |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Немає |

Визначте стиль текстовим рядком, що містить відкривні теги. Теги неявно закриваються у зворотному порядку, тому закривні теги й видимий текст не допускаються.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Теги застосовуються зліва направо, ніби вони вкладені навколо тексту об’єкта. Стиль об’єкта, вибраний у виклику, застосовується після стандартного стилю. Якщо кілька тегів задають ту саму властивість рендерингу, пізніше застосоване значення перевизначає попередні. Ефекти додаються в порядку зліва направо.

::: sidenote
Виклик `font.set_style()` замінює властивості рендерингу й ефекти цього іменованого стилю. Декорування, визначене ресурсом, залишається незмінним, тому перевизначення `link` не вилучає його стандартного підкреслення. Іменовані стилі приймають теги, які впливають лише на рендеринг, як-от `color`, `outline`, `shadow`, `gradient`, `wave` і `shake`. Теги зміни компонування, декорування та об’єктів відхиляються.
:::

## API об’єктів компонування {#layout-object-api}

Використовуйте `label.get_layout_objects()` або `gui.get_layout_objects()`, щоб отримати об’єкти `sprite` і `link` зі скомпонованого тексту.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Аргумент | Тип | Опис |
| --- | --- | --- |
| `url` | `string`, `hash` або `url` | Компонент напису для інспектування, наприклад `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Аргумент | Тип | Опис |
| --- | --- | --- |
| `node` | `node` | Текстовий вузол GUI для інспектування, наприклад `gui.get_node("rich_text")`. |

Обидві функції повертають новостворений масив із поточними об’єктами компонування в порядку їх появи у вихідному тексті. Якщо текст не містить тегів об’єктів, вони повертають порожній масив. Оскільки об’єкти та їхні атрибути копіюються до Lua під час кожного виклику, кешуйте результат і запитуйте його знову після зміни тексту або іншої властивості, яка змінює його компонування.

### Поля поверненого об’єкта {#returned-object-fields}

| Поле | Тип | Опис |
| --- | --- | --- |
| `type` | `string` | `"sprite"` або `"link"`. |
| `id` | `hash` | Ідентифікатор об’єкта, який використовується в повідомленнях взаємодії. |
| `text_offset` | `number` | Позиція у видимому тексті з відліком від нуля, виміряна в кодових точках Unicode. Розмітка не враховується, а символьні посилання рахуються як декодовані символи. Для спрайта це точка його вставлення. |
| `text_length` | `number` | Довжина охопленого видимого тексту в кодових точках Unicode. Спрайт має довжину один завдяки вставленій кодовій точці заміни об’єкта U+FFFC. |
| `width` | `number` | Обчислена ширина в одиницях компонування тексту. Наразі ширина посилань дорівнює нулю. |
| `height` | `number` | Обчислена висота в одиницях компонування тексту. Наразі висота посилань дорівнює нулю. |
| `x` | `number` | Горизонтальна позиція нижнього лівого кута об’єкта відносно початку координат у верхньому лівому куті компонування тексту. |
| `y` | `number` | Вертикальна позиція нижнього лівого кута об’єкта відносно початку координат у верхньому лівому куті компонування тексту. |
| `attributes` | `table` | Усі атрибути тегу як пари рядкових ключів і значень. Значення атрибутів зберігають свій вихідний запис, наприклад `"2em"`. Скорочене неіменоване значення зберігається під ключем `value`. |

::: sidenote
`text_offset` і `text_length` не є байтовими зміщеннями UTF-8. Символ поза ASCII, як-от `å` або `猫`, рахується як одна позиція.
:::

### Приклад Lua {#lua-example}

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

## Корисні поєднання {#useful-combinations}

### Кольорове обведення з горизонтальним градієнтом {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Градієнт множить лише колір заливки; обведення зберігає власний колір.

### Тремтіння речення й градієнт одного слова {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Зовнішній ефект позиції застосовується до кожного гліфа. Вкладений колірний ефект застосовується лише до «whole».

### Перевизначення однієї властивості зі збереженням інших {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

Внутрішній колір змінює заливку, зберігаючи успадковані товщину й колір обведення.
