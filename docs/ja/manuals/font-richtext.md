---
title: Defold のリッチテキストマークアップ
brief: リッチテキストマークアップを使って Label コンポーネントと GUI テキストノードのスタイルを設定し、Lua からリンクやスプライトを調べる方法を説明します。
---

# リッチテキストマークアップ {#rich-text-markup}

Label コンポーネント（component）と GUI テキストノードでマークアップを使うと、入れ子の視覚スタイルやエフェクトを適用し、Lua からリンクやスプライトを調べられます。

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

または、フォントに再利用できる名前付きオブジェクトスタイルを定義して、リンクから選択できます。

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## タグリファレンス {#tag-reference}

| タグ | 用途 | 例 |
| --- | --- | --- |
| [`color`](#color) | グリフの塗りの色を設定します。 | <img src="/manuals/images/richtext/color_green.webp" alt="緑のテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | グリフの字形形成とレイアウトのサイズを変更します。 | <img src="/manuals/images/richtext/size_24.webp" alt="24 ピクセルのテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | 静的またはアニメーションするカラーグラデーションを適用します。 | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="水平方向のグラデーションを持つテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | テキストに下線を引きます。 | <img src="/manuals/images/richtext/underline_solid.webp" alt="下線付きのテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | テキストに取り消し線を引きます。 | <img src="/manuals/images/richtext/strike_solid.webp" alt="取り消し線付きのテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | グリフの輪郭の幅と色を設定します。 | <img src="/manuals/images/richtext/outline.webp" alt="輪郭付きのテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | テキストに影を追加します。 | <img src="/manuals/images/richtext/shadow.webp" alt="影付きのテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | アニメーションするランダムなオフセットを適用します。 | <img src="/manuals/images/richtext/shake_glyph.webp" alt="震えるテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | 正弦波のアニメーションでテキストを動かします。 | <img src="/manuals/images/richtext/wave_glyph.webp" alt="波打つテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | インラインのスプライトオブジェクトを追加します。 | <img src="/manuals/images/richtext/sprite.webp" alt="インラインのスプライト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | 操作に反応するリンクオブジェクトを追加します。 | <img src="/manuals/images/richtext/link.webp" alt="リンクされたテキスト" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## 構文 {#syntax}

タグ名と属性名では大文字と小文字が区別されます。対になったタグは、その内側の表示される UTF-32 テキストに適用されます。スプライトオブジェクトには自己終了タグを使います。

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### 属性 {#attributes}

属性値に空白が含まれていなければ引用符を省略できます。単一引用符または二重引用符で囲むこともできます。`color` と `size` では、名前付きの `value` 形式に加えて、最初の値を省略形で指定できます。

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### 入れ子 {#nesting}

タグは、後から開いたものから順に閉じる必要があります。内側のスタイルの値は、外側のスタイルの同じプロパティを上書きします。異なるプロパティは組み合わされます。スパンのエフェクトはそれぞれ独立して有効なため、入れ子のグラデーションは色を乗算し、入れ子の位置エフェクトはオフセットを加算します。

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### 実体参照 {#entities}

表示するテキスト内の予約文字には `&amp;`、`&apos;`、`&gt;`、`&lt;`、`&quot;` を使います。数値文字参照は現在サポートされていません。

## タグ {#tags}

リッチテキストのタグは、囲んだテキストの範囲（スパン）にスタイルを適用するか、Lua から調べられるオブジェクトを記述します。スタイルタグには対応する終了タグを使います。`sprite` オブジェクトは自己終了形式で、`link` はリンクするテキストを囲みます。

### `color`

グリフの塗りの色を設定します。色には `#RRGGBB` または `#RRGGBBAA` を使います。先頭のハッシュ記号は必須で、`0xFF0000` と `FF0000` は無効です。結果はラベルまたはレンダラーの基本色に乗算されます。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `=color` または `value=color` | はい | 既定値なし | RGB または RGBA の16進数形式で指定する塗りの色。 |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![不透明な緑で描画したサンプルテキスト](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![アルファ値が半分の緑で描画したサンプルテキスト](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

頂点のスケールだけでなく、グリフの字形形成とレイアウトのサイズを変更します。相対値には常にレイアウトの基本フォントサイズを使います。外側の `size` タグと累積して計算されることはありません。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `=size` または `value=size` | はい | 既定値なし | 以下の形式のいずれかで指定する絶対サイズ、百分率、基本サイズの倍数、または基本サイズからの符号付きオフセット。 |

| 形式 | 32 px の場合の例 | 解決後のサイズ |
| --- | --- | --- |
| 数値のみ、または `px` | `24`, `24px` | 24 px |
| 基本サイズに対する百分率 | `120%` | 38.4 px |
| 基本サイズの倍数 | `2em` | 64 px |
| 基本サイズからの符号付きオフセット | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![24 ピクセルで描画したサンプルテキスト](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px の 120%*

![32 ピクセルの 120% で描画したサンプルテキスト](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px を基準とする 2em*

![基本サイズ 32 ピクセルの2倍で描画したサンプルテキスト](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

グラデーションには、完全な属性セットをちょうど1つ指定します。複数のセットを混在させたり、セット内の属性を省略したりすると無効です。

| モード | 必須の属性 | 補間 |
| --- | --- | --- |
| 水平方向 | `left`, `right` | 水平方向の2色の間を補間します。 |
| 垂直方向 | `bottom`, `top` | 下端と上端の色の間を補間します。 |
| 四隅 | `tl`, `tr`, `bl`, `br` | 4つの頂点色の間を補間します。 |

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `left`, `right` | 水平方向モードで必須 | なし | `#RRGGBB` または `#RRGGBBAA` 形式の水平方向の端点の色。両方が必須です。 |
| `bottom`, `top` | 垂直方向モードで必須 | なし | 垂直方向の端点の色。両方が必須です。 |
| `tl`, `tr`, `bl`, `br` | 四隅モードで必須 | なし | 左上、右上、左下、右下の色。4つすべてが必須です。 |
| `fit` | いいえ | `span` | `glyph` は字形形成後のテキストの各位置でサンプリングします。`span` はタグで囲まれたテキスト全体にグラデーションを分布させます。 |
| `hz` | いいえ | `0` | 1秒当たりの流れるアニメーションの完全な周期数。範囲は `[0,)` です。ゼロにするとグラデーションは静止します。 |
| `direction` | いいえ | `forward` | `forward` または `reverse`。`hz` がゼロでない場合の流れる方向を制御します。 |

`fit` を省略すると、`fit=span` によりタグで囲まれたテキスト全体にグラデーションが分布します。`fit=glyph` は字形形成後のテキストの各位置を独立してサンプリングします。省略可能な `hz` は、流れるアニメーションの1秒当たりの完全な周期数を指定します。既定値のゼロではグラデーションは静止します。鏡像として繰り返す色の変化が連続して流れ、色の飛びなしに折り返します。既定値は `direction=forward` です。流れを逆にするには `direction=reverse` を使います。

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

*水平方向*

![マゼンタから白への水平方向のグラデーションを適用したサンプルテキスト](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*垂直方向*

![青の垂直方向のグラデーションを適用したサンプルテキスト](images/richtext/gradient_vertical.webp)

</div>
</div>

**四隅**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![各グリフに合わせて四隅のグラデーションを適用したサンプルテキスト](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![スパンに合わせて四隅のグラデーションを適用したサンプルテキスト](images/richtext/gradient_four_text.webp)

</div>
</div>

**アニメーション**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![各グリフに合わせて流れるグラデーションのアニメーション](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![スパンに合わせて流れるグラデーションのアニメーション](images/richtext/gradient_flow_span.webp)

</div>
</div>

グラデーションの色は現在の塗りの色に乗算されます。そのため、`color=#808080` の内側にあるグラデーションは、この基本乗算値より明るい色成分を生成できません。

### `ul`

フォントの下線メトリクスが利用できる場合は、それを使って下線を描画します。このタグ自体に独立した色はありません。線は、水平方向、垂直方向、四隅のグラデーションを含め、適用後の塗りの色を継承します。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `pattern` | いいえ | `solid` | `solid` または `dashed`。 |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*実線*

![実線の下線付きのサンプルテキスト](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*破線*

![破線の下線付きのサンプルテキスト](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*グラデーション*

![グラデーションの下線付きのサンプルテキスト](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

囲まれたテキストに取り消し線を描画します。`ul` と同じ `pattern` 値を受け取り、同様に適用後の塗りの色を継承します。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `pattern` | いいえ | `solid` | `solid` または `dashed`。 |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*実線*

![実線の取り消し線付きのサンプルテキスト](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*破線*

![破線の取り消し線付きのサンプルテキスト](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

輪郭の幅、色、またはその両方を設定します。少なくとも1つの属性が必須です。幅をゼロにすると、そのスパンの輪郭が明示的に無効になります。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `size` | size/color のいずれか | 継承。既定のフォントでは `0` | レイアウト単位での幅。範囲は `[0,)` です。単位の接尾辞は使えません。 |
| `color` | size/color のいずれか | 継承。既定のラベルでは `#000000` | 16進数の RGB (`#RRGGBB`) または RGBA (`#RRGGBBAA`) 形式で指定する単色の輪郭色。アルファ成分が不透明度を制御します。 |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*外側の黒い輪郭*

![外側に黒い輪郭を付けたサンプルテキスト](images/richtext/outline.webp)

</div>
</div>

### `shadow`

囲まれたテキストに硬い影を追加します。少なくとも1つの属性が必須です。入れ子のタグで省略した属性は外側の影の値を保持し、一番外側のタグで省略した属性はフォントの基本の影の値を保持します。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `color` | いいえ | 継承。既定のラベルでは `#000000` | `#RRGGBB` または `#RRGGBBAA` 形式の影の色。 |
| `x` | いいえ | 継承。既定のフォントでは `0` | レイアウト単位での影の水平オフセット。正の値は右に移動します。 |
| `y` | いいえ | 継承。既定のフォントでは `0` | レイアウト単位での影の垂直オフセット。正の値は上に移動します。 |
| `blur` | いいえ | 継承。既定のフォントでは `0` | レイアウト単位でのぼかし半径。範囲は `[0,)` です。 |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![位置をずらした影付きのサンプルテキスト](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
影のぼかしは生成後、グリフアトラスに保存されます。スパンはフォントに焼き込まれたぼかしより小さいぼかしを要求できます。それより大きい値はレイアウトには保持されますが、現在はアトラス内で利用できる最大のぼかしで描画されます。
:::

### `shake`

改行位置やレイアウトの境界を変えずに、決定論的にアニメーションするランダムなオフセットを適用します。エフェクトが内部で時間を管理するため、スクリプトでアニメーションの各フレームごとにラベルのテキストを変更する必要はありません。

| 属性 | 必須 | 既定値 | 有効な値 | 意味 |
| --- | --- | --- | --- | --- |
| `hz` | いいえ | 20 | `[0,)` | 1秒当たりのランダムな目標への遷移回数。ゼロにするとエフェクトが一時停止します。 |
| `amplitude` | いいえ | 0.5 | `[0,)` | レイアウト単位での最大変位。 |
| `fit` | いいえ | `glyph` | `glyph` または `span` | `glyph` は、字形形成後の各グリフ単位について、文字のクラスターを分断しないオフセットをサンプリングします。`span` はタグで囲まれたテキストスパン全体を1つの剛体として動かします。 |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![グリフごとに震えるアニメーションを適用したサンプルテキスト](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![スパン全体が震えるアニメーションを適用したサンプルテキスト](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

改行位置やレイアウトの境界を変えずに、正弦波のアニメーションで文字を上下に動かします。レイアウトは更新時にアニメーション時間を累積します。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `amplitude` | いいえ | 1 | レイアウト単位での垂直方向の最大変位。範囲は `[0,)` です。 |
| `hz` | いいえ | 1 | 時間に対する1秒当たりの完全な周期数。範囲は `[0,)` です。ゼロにすると波が一時停止します。 |
| `wavelength` | いいえ | 6 | 空間内の1つの完全な周期に含まれる、表示される UTF-32 テキストの位置数。範囲は `[1,)` です。基底文字と結合アクセントなど、フォントがまとめて字形形成する文字は一体となって動きます。 |
| `fit` | いいえ | `glyph` | `glyph` はテキスト全体に空間的な波を適用します。`span` はタグで囲まれたテキストスパン全体に、共通の垂直方向の正弦オフセットを与えます。 |
| `direction` | いいえ | `forward` | `forward` は通常どおり進みます。`reverse` は波の進行方向を反転します。 |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![グリフごとに波打つアニメーションを適用したサンプルテキスト](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![1つのスパンとして動くアニメーションを適用したサンプルテキスト](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

表示されるテキストの現在位置に、自己終了形式のスプライトオブジェクトを追加します。その属性は `label.get_layout_objects()` と `gui.get_layout_objects()` のメタデータとして保持されます。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `id` | いいえ | 生成されます | 返されるレイアウトオブジェクトの `id` にハッシュ化される、安定した識別子。 |
| `src` | いいえ | なし | 画像やアトラスのプロジェクトパスなど、アプリケーションが定義するスプライトリソースの識別子。 |
| `animation` | いいえ | なし | リソース内の、アプリケーションが定義するアニメーション識別子。 |
| `width` | いいえ | `1em` | 解決後のスプライトの幅。 |
| `height` | いいえ | `1em` | 解決後のスプライトの高さ。 |
| その他の属性 | いいえ | 存在しません | オブジェクトリゾルバーとレイアウトオブジェクト API のために保持される、アプリケーションが定義するメタデータ。 |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*解決されたインラインのスプライト*

![テキスト内にインラインで描画した Defold ロゴ](images/richtext/sprite.webp)

</div>
</div>

寸法には、正の数値のみのレイアウト単位、`px`、`em`、`%` を指定できます。`em` と `%` はどちらもテキストレイアウトの基本フォントサイズを使います。

省略した寸法はそれぞれ独立して `1em` になります。両方を省略すると `1em × 1em` のオブジェクトになります。幅だけを指定しても、リソースのアスペクト比から高さが自動的に計算されることはありません。

::: important
sprite タグは、開発者がその場所に任意のオブジェクトを配置するためのプレースホルダーです。
:::

### `link`

表示されるテキストの範囲をリンクオブジェクトとして記述します。囲まれたテキストは通常どおりレイアウトされ、既定では名前付きの `link` スタイルが適用されます。Label コンポーネントと GUI コンポーネントは、テキストの字形形成をやり直さずに、入力に応じて `link:hover` と `link:active` を選択します。リンクへの入力が生成するメッセージについては、[操作メッセージ](#interaction-messages)を参照してください。

| 属性 | 必須 | 既定値 | 意味 |
| --- | --- | --- | --- |
| `src` | いいえ | なし | アプリケーションが定義するリンク先。自動検証や移動は行わず、値を文字列として返します。 |
| `id` | いいえ | 生成されます | 返されるレイアウトオブジェクトの `id` にハッシュ化される、安定した識別子。 |
| `style` | いいえ | `link` | リンクテキストの名前付きの既定スタイル。 |
| その他の属性 | いいえ | 存在しません | 識別子、アクション、ツールチップ、分析用の値など、アプリケーションが定義するメタデータ。 |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![既定のリンクスタイルと下線で描画した www.defold.com](images/richtext/link.webp)

</div>
</div>

コンポーネントは各リンクのポインター状態を追跡します。ポインターがリンク上にある間は `link:hover` を、ポインターを押している間は `link:active` を適用します。どちらの状態にも該当しなくなると、リンクの `style` 属性で指定された名前のスタイルに戻します。属性がなければ `link` に戻します。

### 操作メッセージ {#interaction-messages}

リンクの操作には Defold の通常の入力システムを使います。`MOUSE_BUTTON_LEFT` の Mouse Trigger バインディングを追加します。これによりシングルタッチ入力も有効になります。続いて、ゲームオブジェクト（game object）のスクリプトまたは GUI スクリプトで入力フォーカスを取得します。

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

設定の詳細は、[入力フォーカス](/manuals/input/#input-focus)と[マウスとタッチ入力](/manuals/input-mouse-and-touch)を参照してください。

ラベルまたは GUI コンポーネントがポインター入力を受け取ると、リンクは以下のメッセージを生成します。ラベルのメッセージはそのラベルを所有するゲームオブジェクトに送信され、GUI のメッセージは GUI スクリプトに送信されます。

| メッセージ | 送信されるタイミング |
| --- | --- |
| `text_object_hovered` | ポインターがリンクに入ったとき。 |
| `text_object_unhovered` | ポインターがリンクから離れたとき。 |
| `text_object_clicked` | 押した後、同じリンク上で離したとき。 |

各メッセージには以下のフィールドが含まれます。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `id` | `hash` | オブジェクトの `id` 属性、または生成されたレイアウトオブジェクト ID。 |
| `type` | `hash` | レイアウトオブジェクトの種類。現在は `hash("link")` です。 |
| `src` | `string` | アプリケーションが定義するオブジェクトの `src` 属性の値。属性がなければ空文字列です。 |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## 名前付きスタイル {#named-styles}

各フォントコレクションには、描画だけに作用する名前付きオブジェクトスタイルが含まれます。リンクは `style` 属性で指定した名前のスタイルを使い、属性がなければ `link` を使います。汎用の `<style>` スパンタグはありません。

Defold には以下の既定値があります。

| スタイル | 塗りの色の乗算値 | 装飾 |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | 実線の下線 |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | なし |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | なし |

開始タグを含むテキスト文字列でスタイルを定義します。タグは逆順に暗黙的に閉じられるため、終了タグや表示されるテキストを含めることはできません。

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

タグは、オブジェクトのテキストを入れ子で囲むように、左から右へ適用されます。呼び出し元が選択したオブジェクトスタイルは既定のスタイルの後に適用されます。複数のタグが同じ描画プロパティを設定する場合、後から適用した値が前の値を上書きします。エフェクトは左から右の順序で追加されます。

::: sidenote
`font.set_style()` を呼び出すと、その名前付きスタイルの描画プロパティとエフェクトが置き換えられます。リソースで定義された装飾は変わらないため、`link` を再定義しても既定の下線は削除されません。名前付きスタイルでは、`color`、`outline`、`shadow`、`gradient`、`wave`、`shake` など、描画だけに作用するタグを使えます。レイアウトを変更するタグ、装飾タグ、オブジェクトタグは拒否されます。
:::

## レイアウトオブジェクト API {#layout-object-api}

`label.get_layout_objects()` または `gui.get_layout_objects()` を使うと、レイアウト済みのテキストから `sprite` オブジェクトと `link` オブジェクトを取得できます。

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| 引数 | 型 | 説明 |
| --- | --- | --- |
| `url` | `string`、`hash`、または `url` | 調べるラベルコンポーネント。例: `"#label"`。 |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| 引数 | 型 | 説明 |
| --- | --- | --- |
| `node` | `node` | 調べる GUI テキストノード。例: `gui.get_node("rich_text")`。 |

どちらの関数も、現在のレイアウトオブジェクトをソース内の順序で格納した新しい配列を返します。テキストにオブジェクトタグが含まれていなければ、空の配列を返します。呼び出すたびにオブジェクトとその属性が Lua にコピーされるため、結果をキャッシュし、テキストやレイアウトに影響する別のプロパティを変更した後で再取得してください。

### 返されるオブジェクトのフィールド {#returned-object-fields}

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `type` | `string` | `"sprite"` または `"link"`。 |
| `id` | `hash` | 操作メッセージで使われるオブジェクト識別子。 |
| `text_offset` | `number` | 表示されるテキスト内の、Unicode コードポイント単位で測ったゼロ始まりの位置。マークアップは除外され、実体参照はデコード後の文字として数えます。スプライトでは、その挿入位置です。 |
| `text_length` | `number` | 囲まれた表示テキストの Unicode コードポイント数。スプライトでは、挿入される U+FFFC オブジェクト置換コードポイントにより長さが1になります。 |
| `width` | `number` | テキストレイアウト単位での解決後の幅。リンクの幅は現在ゼロです。 |
| `height` | `number` | テキストレイアウト単位での解決後の高さ。リンクの高さは現在ゼロです。 |
| `x` | `number` | テキストレイアウトの左上の原点を基準とする、オブジェクトの左下隅の水平位置。 |
| `y` | `number` | テキストレイアウトの左上の原点を基準とする、オブジェクトの左下隅の垂直位置。 |
| `attributes` | `table` | 文字列のキーと値のペアとして格納したすべてのタグ属性。属性値は `"2em"` などソースの表現を保持します。名前のない省略形の値は `value` キーに格納されます。 |

::: sidenote
`text_offset` と `text_length` は UTF-8 のバイトオフセットではありません。`å` や `猫` などの非 ASCII 文字は1つの位置として数えます。
:::

### Lua の例 {#lua-example}

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

## 便利な組み合わせ {#useful-combinations}

### 色付きの輪郭と水平方向のグラデーション {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

グラデーションは塗りの色だけに乗算されます。輪郭は自身の色を保持します。

### 文を震わせ、1つの単語にグラデーションを付ける {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

外側の位置エフェクトはすべてのグリフに適用されます。入れ子の色エフェクトは「whole」だけに適用されます。

### 他のプロパティを保持したまま1つのプロパティを上書きする {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

内側の色は、継承した輪郭の幅と色を保持しながら、塗りを変更します。
