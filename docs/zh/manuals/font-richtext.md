---
title: Defold 中的富文本标记
brief: 本手册介绍如何使用富文本标记为 Label 组件和 GUI 文本节点设置样式，以及如何通过 Lua 检查链接和精灵。
---

# 富文本标记 {#rich-text-markup}

在 Label 组件和 GUI 文本节点中使用标记，可以应用嵌套的视觉样式和效果，并通过 Lua 检查链接和精灵。

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

也可以在字体上定义可复用的命名对象样式，并通过链接选择该样式：

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## 标记参考 {#tag-reference}

| 标记 | 用途 | 示例 |
| --- | --- | --- |
| [`color`](#color) | 设置字形填充颜色。 | <img src="/manuals/images/richtext/color_green.webp" alt="绿色文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | 更改字形塑形和布局大小。 | <img src="/manuals/images/richtext/size_24.webp" alt="24 像素文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | 应用静态或动态颜色渐变。 | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="带水平渐变的文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | 为文本添加下划线。 | <img src="/manuals/images/richtext/underline_solid.webp" alt="带下划线的文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | 为文本添加删除线。 | <img src="/manuals/images/richtext/strike_solid.webp" alt="带删除线的文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | 设置字形轮廓宽度和颜色。 | <img src="/manuals/images/richtext/outline.webp" alt="带轮廓的文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | 为文本添加阴影。 | <img src="/manuals/images/richtext/shadow.webp" alt="带阴影的文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | 应用动态随机偏移。 | <img src="/manuals/images/richtext/shake_glyph.webp" alt="抖动文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | 使文本按正弦波运动。 | <img src="/manuals/images/richtext/wave_glyph.webp" alt="波动文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | 添加内嵌精灵对象。 | <img src="/manuals/images/richtext/sprite.webp" alt="内嵌精灵" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | 添加交互式链接对象。 | <img src="/manuals/images/richtext/link.webp" alt="链接文本" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## 语法 {#syntax}

标记和属性名称区分大小写。成对标记应用于其内部的可见 UTF-32 文本。精灵对象使用自闭合标记。

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### 属性 {#attributes}

属性不包含空白字符时可以不加引号，也可以使用单引号或双引号。`color` 和 `size` 既支持首个值的简写形式，也支持带名称的 `value` 形式。

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### 嵌套 {#nesting}

标记必须按后进先出的顺序闭合。内部样式值会覆盖外部样式的同一属性。不同属性会组合生效。文本片段的效果各自保持启用，因此嵌套渐变会将颜色相乘，嵌套位置效果会将偏移相加。

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### 实体 {#entities}

在可见文本中，使用 `&amp;`、`&apos;`、`&gt;`、`&lt;` 和 `&quot;` 表示保留字符。目前不支持数字实体。

## 标记 {#tags}

富文本标记可以为包围的文本片段设置样式，也可以描述可通过 Lua 检查的对象。样式标记使用匹配的闭合标记。`sprite` 对象使用自闭合标记，而 `link` 包围其链接文本。

### `color`

设置字形填充颜色。颜色使用 `#RRGGBB` 或 `#RRGGBBAA`。必须包含井号前缀；`0xFF0000` 和 `FF0000` 无效。结果会与标签或渲染器的基础颜色相乘。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `=color` 或 `value=color` | 是 | 无默认值 | 十六进制 RGB 或 RGBA 形式的填充颜色。 |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![渲染为不透明绿色的示例文本](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![渲染为半透明绿色的示例文本](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

更改字形塑形和布局大小，而不只是缩放顶点。相对值始终使用布局的基础字号，不会与外层 `size` 标记累乘。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `=size` 或 `value=size` | 是 | 无默认值 | 使用下列形式之一指定绝对大小、百分比、基础大小的倍数，或相对于基础大小的带符号偏移。 |

| 形式 | 基础字号为 32 px 时的示例 | 解析后的大小 |
| --- | --- | --- |
| 纯数字或 `px` | `24`、`24px` | 24 px |
| 基础大小的百分比 | `120%` | 38.4 px |
| 基础大小的倍数 | `2em` | 64 px |
| 相对于基础大小的带符号偏移 | `+4`、`-4` | 36 px、28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![以 24 像素渲染的示例文本](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px 的 120%*

![以 32 像素的 120% 渲染的示例文本](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*基础字号为 32px 时的 2em*

![以 32 像素基础大小的两倍渲染的示例文本](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

渐变只接受一组完整的属性集。混合不同属性集或省略其中的成员均无效。

| 模式 | 必需属性 | 插值 |
| --- | --- | --- |
| 水平 | `left`、`right` | 在水平方向的两个颜色之间插值。 |
| 垂直 | `bottom`、`top` | 在底部和顶部颜色之间插值。 |
| 四角 | `tl`、`tr`、`bl`、`br` | 在四个顶点颜色之间插值。 |

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `left`、`right` | 水平模式下必需 | 无 | `#RRGGBB` 或 `#RRGGBBAA` 形式的水平端点颜色。两者必须同时存在。 |
| `bottom`、`top` | 垂直模式下必需 | 无 | 垂直端点颜色。两者必须同时存在。 |
| `tl`、`tr`、`bl`、`br` | 四角模式下必需 | 无 | 左上、右上、左下和右下的颜色。四个属性必须全部存在。 |
| `fit` | 否 | `span` | `glyph` 对塑形后的每个文本位置采样；`span` 将渐变分布到标记包围的整段文本中。 |
| `hz` | 否 | `0` | 每秒完整流动周期数，范围为 `[0,)`；零表示静态渐变。 |
| `direction` | 否 | `forward` | `forward` 或 `reverse`。当 `hz` 不为零时控制流动方向。 |

省略 `fit` 时，`fit=span` 将渐变分布到标记包围的整段文本中。`fit=glyph` 对塑形后的每个文本位置独立采样。可选的 `hz` 指定每秒完整流动动画的周期数；默认值为零，保持渐变静止。重复的镜像色带会连续流动，并在循环时保持颜色平滑衔接。默认为 `direction=forward`；使用 `direction=reverse` 可反转流动方向。

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

*水平*

![具有从品红到白色的水平渐变的示例文本](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*垂直*

![具有蓝色垂直渐变的示例文本](images/richtext/gradient_vertical.webp)

</div>
</div>

**四角**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![四角渐变适配到每个字形的示例文本](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![四角渐变适配到整段文本的示例文本](images/richtext/gradient_four_text.webp)

</div>
</div>

**动画**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![适配到每个字形的动态流动渐变](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![适配到整段文本的动态流动渐变](images/richtext/gradient_flow_span.webp)

</div>
</div>

渐变颜色会与当前填充颜色相乘。因此，位于 `color=#808080` 内的渐变无法生成比该基础乘数更亮的颜色通道。

### `ul`

在字体提供下划线度量时，使用这些度量绘制下划线。此标记没有独立的颜色：线条会继承实际生效的填充颜色，包括水平、垂直和四角渐变。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `pattern` | 否 | `solid` | `solid` 或 `dashed`。 |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*实线*

![带实线下划线的示例文本](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*虚线*

![带虚线下划线的示例文本](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*渐变*

![带渐变下划线的示例文本](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

在包围的文本上绘制删除线。此标记接受与 `ul` 相同的 `pattern` 值，同样会继承实际生效的填充颜色。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `pattern` | 否 | `solid` | `solid` 或 `dashed`。 |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*实线*

![带实线删除线的示例文本](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*虚线*

![带虚线删除线的示例文本](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

设置轮廓宽度、轮廓颜色，或同时设置两者。至少需要一个属性。将宽度设为零会明确禁用该文本片段的轮廓。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `size` | size/color 中至少一个 | 继承；默认字体为 `0` | 以布局单位表示的宽度，范围为 `[0,)`。不接受单位后缀。 |
| `color` | size/color 中至少一个 | 继承；默认标签为 `#000000` | 十六进制 RGB（`#RRGGBB`）或 RGBA（`#RRGGBBAA`）形式的单一轮廓颜色；alpha 分量控制不透明度。 |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*黑色外轮廓*

![带黑色外轮廓的示例文本](images/richtext/outline.webp)

</div>
</div>

### `shadow`

为包围的文本添加硬阴影。至少需要一个属性。嵌套标记省略的属性保留外层阴影的值；最外层标记省略的属性保留字体的基础阴影值。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `color` | 否 | 继承；默认标签为 `#000000` | `#RRGGBB` 或 `#RRGGBBAA` 形式的阴影颜色。 |
| `x` | 否 | 继承；默认字体为 `0` | 以布局单位表示的水平阴影偏移。正值向右移动。 |
| `y` | 否 | 继承；默认字体为 `0` | 以布局单位表示的垂直阴影偏移。正值向上移动。 |
| `blur` | 否 | 继承；默认字体为 `0` | 以布局单位表示的模糊半径，范围为 `[0,)`。 |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![带偏移阴影的示例文本](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
阴影模糊会生成并存储在字形图集中。文本片段可以请求小于字体烘焙模糊值的模糊；更大的值会保留在布局中，但目前渲染时会使用图集中可用的最大模糊值。
:::

### `shake`

应用确定性的动态随机偏移，不改变换行或布局边界。该效果在内部计时；脚本不需要在每个动画帧修改标签文本。

| 属性 | 必需 | 默认值 | 有效值 | 含义 |
| --- | --- | --- | --- | --- |
| `hz` | 否 | 20 | `[0,)` | 每秒向新随机目标过渡的次数。零表示暂停效果。 |
| `amplitude` | 否 | 0.5 | `[0,)` | 以布局单位表示的最大位移。 |
| `fit` | 否 | `glyph` | `glyph` 或 `span` | `glyph` 为每个塑形后的字形单元采样偏移，并保持字形簇完整。`span` 将标记包围的整段文本作为一个刚性单元移动。 |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![逐字形动态抖动的示例文本](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![整段动态抖动的示例文本](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

使字符沿动态正弦波上下移动，不改变换行或布局边界。布局在更新时累积动画时间。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `amplitude` | 否 | 1 | 以布局单位表示的最大垂直位移，范围为 `[0,)`。 |
| `hz` | 否 | 1 | 每秒完整时间周期数，范围为 `[0,)`。零表示暂停波动。 |
| `wavelength` | 否 | 6 | 每个完整空间周期包含的可见 UTF-32 文本位置数，范围为 `[1,)`。字体将其组合塑形的字符（例如基础字符及其组合重音符号）会作为一个单元移动。 |
| `fit` | 否 | `glyph` | `glyph` 将空间波形应用于整段文本。`span` 为标记包围的整段文本提供一个共用的垂直正弦偏移。 |
| `direction` | 否 | `forward` | `forward` 正常推进。`reverse` 反转波的传播方向。 |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![逐字形动态波动的示例文本](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![整段一同运动的示例文本](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

在可见文本的当前位置添加一个自闭合的精灵对象。其属性会作为元数据保留，供 `label.get_layout_objects()` 和 `gui.get_layout_objects()` 使用。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `id` | 否 | 自动生成 | 稳定标识符，其哈希值作为返回的布局对象的 `id`。 |
| `src` | 否 | 无 | 应用程序定义的精灵资源标识符，例如图像或图集的项目路径。 |
| `animation` | 否 | 无 | 应用程序定义的资源内动画标识符。 |
| `width` | 否 | `1em` | 解析后的精灵宽度。 |
| `height` | 否 | `1em` | 解析后的精灵高度。 |
| 其他任意属性 | 否 | 不存在 | 应用程序定义的元数据，会保留供对象解析器和布局对象 API 使用。 |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*解析后的内嵌精灵*

![与文本同行渲染的 Defold 标志](images/richtext/sprite.webp)

</div>
</div>

尺寸接受正值，可使用无单位的布局单位、`px`、`em` 或 `%`。`em` 和 `%` 均基于文本布局的基础字号。

每个缺省的尺寸分别默认为 `1em`。同时省略宽度和高度会生成 `1em × 1em` 的对象；仅指定宽度不会根据资源的宽高比自动推算高度。

::: important
sprite 标记只是一个占位符，开发者可以在该位置放置任何对象！
:::

### `link`

将一段可见文本描述为链接对象。包围的文本按常规方式布局，默认应用名为 `link` 的样式。Label 和 GUI 组件会根据输入选择 `link:hover` 和 `link:active`，而无需重新塑形文本。有关链接输入产生的消息，请参阅[交互消息](#interaction-messages)。

| 属性 | 必需 | 默认值 | 含义 |
| --- | --- | --- | --- |
| `src` | 否 | 无 | 应用程序定义的链接目标。该值以字符串形式返回，不会自动验证或跳转。 |
| `id` | 否 | 自动生成 | 稳定标识符，其哈希值作为返回的布局对象的 `id`。 |
| `style` | 否 | `link` | 链接文本使用的命名默认样式。 |
| 其他任意属性 | 否 | 不存在 | 应用程序定义的元数据，例如标识符、操作、工具提示或分析数据值。 |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![使用默认链接样式和下划线渲染的 www.defold.com](images/richtext/link.webp)

</div>
</div>

组件跟踪每个链接的指针状态。指针悬停在链接上时应用 `link:hover`，指针按下时应用 `link:active`。两种状态均不适用时，组件会恢复链接的 `style` 属性指定的样式；没有该属性时则恢复为 `link`。

### 交互消息 {#interaction-messages}

链接交互使用 Defold 的常规输入系统。为 `MOUSE_BUTTON_LEFT` 添加 Mouse Trigger 绑定，这也会启用单点触摸输入，然后在游戏对象的脚本或 GUI 脚本中获取输入焦点：

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

有关设置的详细信息，请参阅[输入焦点](/manuals/input/#input-focus)和[鼠标与触摸输入](/manuals/input-mouse-and-touch)。

当标签或 GUI 组件收到指针输入时，链接会产生以下消息。标签消息发送给所属的游戏对象；GUI 消息发送给 GUI 脚本。

| 消息 | 发送时机 |
| --- | --- |
| `text_object_hovered` | 指针进入链接。 |
| `text_object_unhovered` | 指针离开链接。 |
| `text_object_clicked` | 在同一链接上按下后释放。 |

每条消息包含以下字段：

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `id` | `hash` | 对象的 `id` 属性，或其自动生成的布局对象 ID。 |
| `type` | `hash` | 布局对象类型，目前为 `hash("link")`。 |
| `src` | `string` | 应用程序定义的对象 `src` 属性值；不存在时为空字符串。 |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## 命名样式 {#named-styles}

每个字体集合都包含仅影响渲染的命名对象样式。链接使用其 `style` 属性指定的样式；没有该属性时使用 `link`。不存在通用的 `<style>` 文本片段标记。

Defold 提供以下默认样式：

| 样式 | 填充颜色乘数 | 装饰 |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | 实线下划线 |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | 无 |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | 无 |

使用包含起始标记的文本字符串定义样式。标记会隐式地按相反顺序闭合，因此不允许包含闭合标记和可见文本。

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

标记从左到右应用，就像嵌套在对象文本周围一样。调用者选定的对象样式在默认样式之后应用。多个标记设置同一渲染属性时，后应用的值覆盖先前的值。效果按从左到右的顺序追加。

::: sidenote
调用 `font.set_style()` 会替换该命名样式的渲染属性和效果。资源定义的装饰保持不变，因此重新定义 `link` 不会移除其默认下划线。命名样式接受 `color`、`outline`、`shadow`、`gradient`、`wave` 和 `shake` 等仅影响渲染的标记。改变布局的标记、装饰标记和对象标记均不被接受。
:::

## 布局对象 API {#layout-object-api}

使用 `label.get_layout_objects()` 或 `gui.get_layout_objects()`，可以从已布局的文本中获取 `sprite` 和 `link` 对象。

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| `url` | `string`、`hash` 或 `url` | 要检查的标签组件，例如 `"#label"`。 |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| `node` | `node` | 要检查的 GUI 文本节点，例如 `gui.get_node("rich_text")`。 |

这两个函数都返回新创建的数组，按源文本顺序包含当前布局对象。文本中没有对象标记时，会返回空数组。由于每次调用都会将对象及其属性复制到 Lua 中，建议缓存结果，并在更改文本或其他会改变布局的属性后再次查询。

### 返回的对象字段 {#returned-object-fields}

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `type` | `string` | `"sprite"` 或 `"link"`。 |
| `id` | `hash` | 交互消息使用的对象标识符。 |
| `text_offset` | `number` | 在可见文本中从零开始的位置，以 Unicode 码点计量。不包含标记，实体按解码后的字符计数。对于精灵，这是其插入位置。 |
| `text_length` | `number` | 包围的可见文本长度，以 Unicode 码点计量。精灵会插入 U+FFFC 对象替换码点，因此长度为一。 |
| `width` | `number` | 解析后的宽度，以文本布局单位表示。目前链接的宽度为零。 |
| `height` | `number` | 解析后的高度，以文本布局单位表示。目前链接的高度为零。 |
| `x` | `number` | 对象左下角相对于文本布局左上角原点的水平位置。 |
| `y` | `number` | 对象左下角相对于文本布局左上角原点的垂直位置。 |
| `attributes` | `table` | 所有标记属性，以字符串键值对表示。属性值保留其源表示形式，例如 `"2em"`。简写的无名值存储在键 `value` 下。 |

::: sidenote
`text_offset` 和 `text_length` 不是 UTF-8 字节偏移。`å` 或 `猫` 等非 ASCII 字符计为一个位置。
:::

### Lua 示例 {#lua-example}

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

## 实用组合 {#useful-combinations}

### 彩色轮廓与水平渐变 {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

渐变只与填充颜色相乘；轮廓保留自己的颜色。

### 让整句抖动，并为一个单词添加渐变 {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

外层的位置效果应用于每个字形。嵌套的颜色效果仅应用于“whole”。

### 覆盖一个属性并保留其他属性 {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

内部颜色改变填充颜色，同时保留继承的轮廓宽度和颜色。
