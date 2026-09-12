---
title: Defold'da zengin metin işaretlemesi
brief: Bu kılavuz, etiket bileşenlerini ve GUI metin düğümlerini zengin metin işaretlemesiyle nasıl biçimlendireceğinizi, bağlantıları ve sprite nesnelerini Lua'dan nasıl inceleyeceğinizi açıklar.
---

# Zengin metin işaretlemesi

İç içe görsel stiller ve efektler uygulamak, bağlantıları ve sprite nesnelerini Lua'dan incelemek için etiket bileşenlerinde (Label component) ve GUI metin düğümlerinde (GUI text node) işaretleme (markup) kullanın.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Alternatif olarak, yazı tipinde yeniden kullanılabilir, adlandırılmış bir nesne stili tanımlayın ve bu stili bir bağlantıdan seçin:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Etiket başvurusu

| Etiket | Amaç | Örnek |
| --- | --- | --- |
| [`color`](#color) | Glifin (glyph) dolgu rengini ayarlayın. | <img src="/manuals/images/richtext/color_green.webp" alt="Yeşil metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Glif şekillendirme ve yerleşim boyutunu değiştirin. | <img src="/manuals/images/richtext/size_24.webp" alt="24 piksel boyutunda metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Sabit veya animasyonlu bir renk geçişi uygulayın. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Yatay renk geçişli metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Metnin altını çizin. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Altı çizili metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Metnin üstünü çizin. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Üstü çizili metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Glif dış çizgisinin genişliğini ve rengini ayarlayın. | <img src="/manuals/images/richtext/outline.webp" alt="Dış çizgili metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Metne gölge ekleyin. | <img src="/manuals/images/richtext/shadow.webp" alt="Gölgeli metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Animasyonlu rastgele bir kaydırma uygulayın. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Titreyen metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Metni animasyonlu bir sinüs dalgasıyla hareket ettirin. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Dalgalanan metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Satır içi bir sprite nesnesi ekleyin. | <img src="/manuals/images/richtext/sprite.webp" alt="Satır içi sprite" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Etkileşimli bir bağlantı nesnesi ekleyin. | <img src="/manuals/images/richtext/link.webp" alt="Bağlantılı metin" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Sözdizimi

Etiketler ve öznitelik adları büyük/küçük harfe duyarlıdır. Açılış ve kapanış etiketinden oluşan bir çift, arasındaki görünür UTF-32 metnine uygulanır. Sprite nesneleri kendiliğinden kapanan etiketler kullanır.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Öznitelikler

Öznitelikler, boşluk karakteri içermediklerinde tırnaksız yazılabilir ya da tek veya çift tırnak içine alınabilir. `color` ve `size`, adlandırılmış `value` biçiminin yanı sıra kısaltılmış bir ilk değeri de destekler.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### İç içe yerleştirme

Etiketler son giren ilk çıkar sırasıyla kapatılmalıdır. İçteki stil değerleri, dıştaki stilin aynı özelliğini geçersiz kılar. Farklı özellikler birleşir. Metin aralığı (span) efektleri birbirinden bağımsız olarak etkin kalır; bu nedenle iç içe renk geçişleri renkleri çarpar, iç içe konum efektleri ise kaydırmalarını toplar.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Karakter başvuruları

Görünür metindeki ayrılmış karakterler için `&amp;`, `&apos;`, `&gt;`, `&lt;` ve `&quot;` kullanın. Sayısal karakter başvuruları şu anda desteklenmez.

## Etiketler

Zengin metin etiketleri, çevreledikleri bir metin aralığını biçimlendirir veya Lua'dan incelenebilen bir nesneyi tanımlar. Stil etiketleri eşleşen bir kapanış etiketi kullanır. `sprite` nesnesi kendiliğinden kapanırken `link`, bağlantı verilen metni çevreler.

### `color`

Glifin dolgu rengini ayarlar. Renkler `#RRGGBB` veya `#RRGGBBAA` biçimini kullanır. Kare işareti öneki zorunludur; `0xFF0000` ve `FF0000` geçersizdir. Sonuç, etiketin veya görüntüyü oluşturan işleyicinin (renderer) temel rengiyle çarpılır.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `=color` veya `value=color` | Evet | Varsayılan yok | Onaltılık RGB veya RGBA biçiminde dolgu rengi. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Opak yeşil renkte işlenmiş örnek metin](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Yarı alfa değerli yeşil renkte işlenmiş örnek metin](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Yalnızca köşe ölçeğini değil, glif şekillendirme ve yerleşim (layout) boyutunu da değiştirir. Göreli değerler her zaman yerleşimin temel yazı tipi boyutunu kullanır. Çevreleyen bir `size` etiketinin etkisiyle birleşmezler.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `=size` veya `value=size` | Evet | Varsayılan yok | Aşağıdaki biçimlerden biriyle belirtilen mutlak boyut, yüzde, temel boyutun katı veya temel boyuta göre işaretli fark. |

| Biçim | 32 px için örnek | Hesaplanan boyut |
| --- | --- | --- |
| Yalın sayı veya `px` | `24`, `24px` | 24 px |
| Temel boyutun yüzdesi | `120%` | 38,4 px |
| Temel boyutun katı | `2em` | 64 px |
| Temel boyuta göre işaretli fark | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![24 piksel boyutunda işlenmiş örnek metin](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px değerinin %120'si*

![32 pikselin yüzde 120'si boyutunda işlenmiş örnek metin](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*32px temel boyutuna göre 2em*

![32 piksellik temel boyutun iki katında işlenmiş örnek metin](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Bir renk geçişi (gradient), eksiksiz olarak belirtilmiş tek bir öznitelik kümesini kabul eder. Kümeleri karıştırmak veya bir üyeyi atlamak geçersizdir.

| Mod | Zorunlu öznitelikler | Ara değerleme |
| --- | --- | --- |
| Yatay | `left`, `right` | Yatay yöndeki iki renk arasında ara değerleme yapar. |
| Dikey | `bottom`, `top` | Alt ve üst renkler arasında ara değerleme yapar. |
| Dört köşe | `tl`, `tr`, `bl`, `br` | Dört köşe rengi arasında ara değerleme yapar. |

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `left`, `right` | Yatay mod için | Yok | `#RRGGBB` veya `#RRGGBBAA` biçiminde yatay uç nokta renkleri. İkisi de bulunmalıdır. |
| `bottom`, `top` | Dikey mod için | Yok | Dikey uç nokta renkleri. İkisi de bulunmalıdır. |
| `tl`, `tr`, `bl`, `br` | Dört köşe modu için | Yok | Sol üst, sağ üst, sol alt ve sağ alt renkleri. Dördü de bulunmalıdır. |
| `fit` | Hayır | `span` | `glyph`, şekillendirilmiş metindeki her konumu örnekler; `span`, renk geçişini etiketlenmiş metnin tamamına dağıtır. |
| `hz` | Hayır | `0` | `[0,)` aralığında, saniyedeki tam akış döngüsü sayısı; sıfır, renk geçişini sabit tutar. |
| `direction` | Hayır | `forward` | `forward` veya `reverse`. `hz` sıfırdan farklı olduğunda akış yönünü belirler. |

`fit` belirtilmediğinde `fit=span`, renk geçişini etiketlenmiş metnin tamamına dağıtır. `fit=glyph`, şekillendirilmiş metindeki her konumu bağımsız olarak örnekler. İsteğe bağlı `hz`, saniyedeki tam akış animasyonu döngülerinin sayısını belirtir; varsayılan sıfır değeri renk geçişini sabit tutar. Yansıtılarak yinelenen renk geçişi sürekli akar ve renk sıçraması olmadan başa döner. Varsayılan `direction=forward` değeridir; akışı tersine çevirmek için `direction=reverse` kullanın.

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

*Yatay*

![Macentadan beyaza yatay renk geçişli örnek metin](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Dikey*

![Dikey mavi renk geçişli örnek metin](images/richtext/gradient_vertical.webp)

</div>
</div>

**Dört köşe**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Her glife sığdırılmış dört köşeli renk geçişine sahip örnek metin](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Metin aralığına sığdırılmış dört köşeli renk geçişine sahip örnek metin](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animasyonlu**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Her glife sığdırılmış, animasyonlu akan renk geçişi](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Metin aralığına sığdırılmış, animasyonlu akan renk geçişi](images/richtext/gradient_flow_span.webp)

</div>
</div>

Renk geçişinin renkleri geçerli dolgu rengiyle çarpılır. Bu nedenle `color=#808080` içindeki bir renk geçişi, bu temel çarpandan daha parlak bir kanal değeri üretemez.

### `ul`

Varsa yazı tipinin alt çizgi ölçülerini kullanarak bir alt çizgi çizer. Etiketin bağımsız bir rengi yoktur: çizgi, yatay, dikey ve dört köşeli renk geçişleri dahil olmak üzere etkin dolgu rengini devralır.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `pattern` | Hayır | `solid` | `solid` veya `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Kesintisiz*

![Kesintisiz alt çizgili örnek metin](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Kesikli*

![Kesikli alt çizgili örnek metin](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Renk geçişi*

![Renk geçişli alt çizgisi olan örnek metin](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Çevrelenen metnin üstünü çizer. `pattern` için `ul` ile aynı değerleri kabul eder ve benzer şekilde etkin dolgu rengini devralır.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `pattern` | Hayır | `solid` | `solid` veya `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Kesintisiz*

![Üstü kesintisiz bir çizgiyle çizilmiş örnek metin](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Kesikli*

![Üstü kesikli bir çizgiyle çizilmiş örnek metin](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Dış çizgi genişliğini, dış çizgi rengini veya her ikisini ayarlar. En az bir öznitelik zorunludur. Sıfır genişlik, metin aralığı için dış çizgiyi açıkça devre dışı bırakır.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `size` | size/color özniteliklerinden biri | Devralınır; varsayılan bir yazı tipinde `0` | Yerleşim birimleri cinsinden genişlik; aralık `[0,)`. Birim son ekleri kabul edilmez. |
| `color` | size/color özniteliklerinden biri | Devralınır; varsayılan bir etikette `#000000` | Onaltılık RGB (`#RRGGBB`) veya RGBA (`#RRGGBBAA`) biçiminde tek bir dış çizgi rengi; alfa bileşeni opaklığı belirler. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Dışa doğru siyah dış çizgi*

![Dışa doğru siyah dış çizgili örnek metin](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Çevrelenen metne keskin kenarlı bir gölge ekler. En az bir öznitelik zorunludur. İç içe yerleştirilmiş bir etikette belirtilmeyen öznitelikler, çevreleyen gölgenin değerini korur; en dıştaki etikette belirtilmeyen öznitelikler ise yazı tipinin temel gölge değerini korur.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `color` | Hayır | Devralınır; varsayılan bir etikette `#000000` | `#RRGGBB` veya `#RRGGBBAA` biçiminde gölge rengi. |
| `x` | Hayır | Devralınır; varsayılan bir yazı tipinde `0` | Yerleşim birimleri cinsinden yatay gölge kaydırması. Pozitif değerler gölgeyi sağa taşır. |
| `y` | Hayır | Devralınır; varsayılan bir yazı tipinde `0` | Yerleşim birimleri cinsinden dikey gölge kaydırması. Pozitif değerler gölgeyi yukarı taşır. |
| `blur` | Hayır | Devralınır; varsayılan bir yazı tipinde `0` | Yerleşim birimleri cinsinden bulanıklık yarıçapı; aralık `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Kaydırılmış gölgesi olan örnek metin](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
Gölge bulanıklığı glif atlasında oluşturulur ve saklanır. Bir metin aralığı, yazı tipinde önceden hesaplanan bulanıklıktan daha küçük bir bulanıklık isteyebilir; daha büyük değerler yerleşimde korunur ancak şu anda atlastaki en büyük bulanıklık kullanılarak işlenir.
:::

### `shake`

Satır kaydırmayı veya yerleşim sınırlarını değiştirmeden, belirlenimci ve animasyonlu rastgele bir kaydırma uygular. Efekt zamanı kendi içinde takip eder; betiklerin her animasyon karesinde etiket metnini değiştirmesi gerekmez.

| Öznitelik | Zorunlu | Varsayılan | Geçerli değerler | Anlamı |
| --- | --- | --- | --- | --- |
| `hz` | Hayır | 20 | `[0,)` | Saniyedeki rastgele hedef geçişi sayısı. Sıfır, efekti duraklatır. |
| `amplitude` | Hayır | 0.5 | `[0,)` | Yerleşim birimleri cinsinden en büyük yer değiştirme. |
| `fit` | Hayır | `glyph` | `glyph` veya `span` | `glyph`, şekillendirilmiş her glif birimi için karakter kümelerinin bütünlüğünü koruyan bir kaydırma örnekler. `span`, etiketlenmiş metin aralığının tamamını tek bir katı birim olarak hareket ettirir. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Her glifi animasyonla titreyen örnek metin](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Metin aralığının tamamı animasyonla titreyen örnek metin](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Satır kaydırmayı veya yerleşim sınırlarını değiştirmeden, karakterleri animasyonlu bir sinüs dalgasıyla yukarı ve aşağı hareket ettirir. Yerleşim, güncellendiğinde animasyon süresini biriktirir.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `amplitude` | Hayır | 1 | Yerleşim birimleri cinsinden en büyük dikey yer değiştirme; aralık `[0,)`. |
| `hz` | Hayır | 1 | Saniyedeki tam zamansal döngü sayısı; aralık `[0,)`. Sıfır, dalgayı duraklatır. |
| `wavelength` | Hayır | 6 | Tam bir uzamsal döngüdeki görünür UTF-32 metin konumlarının sayısı; aralık `[1,)`. Bir temel karakter ve onunla birleşen aksan işareti gibi, yazı tipinin birlikte şekillendirdiği karakterler tek bir birim olarak hareket eder. |
| `fit` | Hayır | `glyph` | `glyph`, uzamsal dalgayı metin boyunca uygular. `span`, etiketlenmiş metin aralığının tamamına sinüs dalgasına göre tek bir ortak dikey kaydırma uygular. |
| `direction` | Hayır | `forward` | `forward`, normal yönde ilerler. `reverse`, dalganın ilerleme yönünü tersine çevirir. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Her glifi animasyonla dalgalanan örnek metin](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Tek bir metin aralığı olarak animasyonla hareket eden örnek metin](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Görünür metindeki geçerli konuma, kendiliğinden kapanan bir sprite nesnesi ekler. Öznitelikleri, `label.get_layout_objects()` ve `gui.get_layout_objects()` için üst veri olarak korunur.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `id` | Hayır | Oluşturulur | Döndürülen yerleşim nesnesinin `id` alanına karma değeri olarak kaydedilen, sabit kalan tanımlayıcı. |
| `src` | Hayır | Yok | Bir görüntünün veya atlasın proje yolu gibi, uygulama tanımlı sprite kaynağı tanımlayıcısı. |
| `animation` | Hayır | Yok | Kaynak içindeki uygulama tanımlı animasyon tanımlayıcısı. |
| `width` | Hayır | `1em` | Hesaplanan sprite genişliği. |
| `height` | Hayır | `1em` | Hesaplanan sprite yüksekliği. |
| Diğer herhangi bir öznitelik | Hayır | Bulunmaz | Nesne çözümleyicisi ve yerleşim nesnesi API'leri için korunan, uygulama tanımlı üst veriler. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Çözümlenmiş satır içi sprite nesnesi*

![Metinle aynı satırda işlenmiş bir Defold logosu](images/richtext/sprite.webp)

</div>
</div>

Boyutlar, pozitif yalın yerleşim birimlerini, `px`, `em` veya `%` kabul eder. Hem `em` hem de `%`, metin yerleşiminin temel yazı tipi boyutunu kullanır.

Belirtilmeyen her boyut, birbirinden bağımsız olarak varsayılan `1em` değerini alır. İkisinin de belirtilmemesi `1em × 1em` boyutunda bir nesne oluşturur; yalnızca genişliğin belirtilmesi, yüksekliği bir kaynağın en boy oranından otomatik olarak türetmez.

::: important
Sprite etiketi, geliştiricinin o konuma istediği nesneyi yerleştirebilmesi için yalnızca bir yer tutucudur!
:::

### `link`

Görünür metindeki bir aralığı bağlantı nesnesi olarak tanımlar. Çevrelenen metin normal şekilde yerleştirilir ve varsayılan olarak `link` adlı stili alır. Etiket ve GUI bileşenleri, metni yeniden şekillendirmeden girdiye yanıt olarak `link:hover` ve `link:active` stillerini seçer. Bağlantı girdisinin ürettiği iletiler için [Etkileşim iletileri](#interaction-messages) bölümüne bakın.

| Öznitelik | Zorunlu | Varsayılan | Anlamı |
| --- | --- | --- | --- |
| `src` | Hayır | Yok | Uygulama tanımlı bağlantı hedefi. Değer, otomatik doğrulama veya gezinme yapılmadan bir dize olarak döndürülür. |
| `id` | Hayır | Oluşturulur | Döndürülen yerleşim nesnesinin `id` alanına karma değeri olarak kaydedilen, sabit kalan tanımlayıcı. |
| `style` | Hayır | `link` | Bağlantı metni için adlandırılmış varsayılan stil. |
| Diğer herhangi bir öznitelik | Hayır | Bulunmaz | Tanımlayıcı, eylem, araç ipucu veya analitik değeri gibi uygulama tanımlı üst veriler. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![Varsayılan bağlantı stiliyle ve alt çizgiyle işlenmiş www.defold.com](images/richtext/link.webp)

</div>
</div>

Bileşen, her bağlantının işaretçi durumunu izler. İşaretçi bağlantının üzerindeyken `link:hover`, işaretçi basılıyken `link:active` stilini uygular. Bu durumlardan hiçbiri geçerli olmadığında bileşen, bağlantının `style` özniteliğinde adlandırılan stili veya öznitelik yoksa `link` stilini geri yükler.

### Etkileşim iletileri {#interaction-messages}

Bağlantı etkileşimi, Defold'un normal girdi sistemini kullanır. `MOUSE_BUTTON_LEFT` için bir Mouse Trigger eşlemesi ekleyin; bu, tek dokunuşlu girdiyi de etkinleştirir. Oyun nesnesinin (game object) betiğinde veya GUI betiğinde girdi odağını (input focus) alın:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Kurulum ayrıntıları için [Girdi odağı](/manuals/input/#input-focus) ve [Fare ve dokunma girdisi](/manuals/input-mouse-and-touch) bölümlerine bakın.

Bir etiket veya GUI bileşeni işaretçi girdisi aldığında bağlantılar aşağıdaki iletileri üretir. Etiket iletileri, etiketin sahibi olan oyun nesnesine; GUI iletileri ise GUI betiğine gönderilir.

| İleti | Gönderilme zamanı |
| --- | --- |
| `text_object_hovered` | İşaretçi bir bağlantının üzerine geldiğinde. |
| `text_object_unhovered` | İşaretçi bir bağlantının üzerinden ayrıldığında. |
| `text_object_clicked` | Basılı girdi aynı bağlantının üzerinde bırakıldığında. |

Her ileti şu alanları içerir:

| Alan | Tür | Açıklama |
| --- | --- | --- |
| `id` | `hash` | Nesnenin `id` özniteliği veya oluşturulan yerleşim nesnesi tanımlayıcısı. |
| `type` | `hash` | Yerleşim nesnesinin türü; şu anda `hash("link")`. |
| `src` | `string` | Nesnenin `src` özniteliğinin uygulama tanımlı değeri veya öznitelik yoksa boş dize. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Adlandırılmış stiller

Her yazı tipi koleksiyonu (font collection), yalnızca işlemeyi (rendering), yani görüntü oluşturmayı etkileyen adlandırılmış nesne stilleri içerir. Bir bağlantı, `style` özniteliğinde adlandırılan stili veya öznitelik yoksa `link` stilini kullanır. Genel amaçlı bir `<style>` metin aralığı etiketi yoktur.

Defold aşağıdaki varsayılanları sağlar:

| Stil | Dolgu rengi çarpanı | Süsleme |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Kesintisiz alt çizgi |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Yok |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Yok |

Açılış etiketlerini içeren bir metin dizesiyle stil tanımlayın. Etiketler ters sırayla örtük olarak kapatılır; bu nedenle kapanış etiketlerine ve görünür metne izin verilmez.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

Etiketler, nesne metninin çevresinde iç içe yerleştirilmiş gibi soldan sağa uygulanır. Çağıran kodun seçtiği nesne stili, varsayılan stilden sonra uygulanır. Birden çok etiket aynı işleme özelliğini ayarladığında, daha sonra uygulanan değer önceki değerleri geçersiz kılar. Efektler soldan sağa sırayla eklenir.

::: sidenote
`font.set_style()` çağrısı, belirtilen adlı stilin işleme özelliklerini ve efektlerini yenileriyle değiştirir. Kaynakta tanımlı süslemeler değişmez; dolayısıyla `link` stilini yeniden tanımlamak varsayılan alt çizgisini kaldırmaz. Adlandırılmış stiller `color`, `outline`, `shadow`, `gradient`, `wave` ve `shake` gibi yalnızca işlemeyi etkileyen etiketleri kabul eder. Yerleşimi değiştiren etiketler, süsleme etiketleri ve nesne etiketleri reddedilir.
:::

## Yerleşim nesnesi API'si

`label.get_layout_objects()` veya `gui.get_layout_objects()` kullanarak yerleştirilmiş metindeki `sprite` ve `link` nesnelerini alın.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Bağımsız değişken | Tür | Açıklama |
| --- | --- | --- |
| `url` | `string`, `hash` veya `url` | İncelenecek etiket bileşeni; örneğin `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Bağımsız değişken | Tür | Açıklama |
| --- | --- | --- |
| `node` | `node` | İncelenecek GUI metin düğümü; örneğin `gui.get_node("rich_text")`. |

Her iki işlev de geçerli yerleşim nesnelerini kaynak sırasıyla içeren, yeni oluşturulmuş bir dizi döndürür. Metin nesne etiketi içermediğinde boş bir dizi döndürürler. Nesneler ve öznitelikleri her çağrıda Lua'ya kopyalandığından, sonucu önbelleğe alın ve metni veya yerleşimini değiştiren başka bir özelliği değiştirdikten sonra yeniden sorgulayın.

### Döndürülen nesnenin alanları

| Alan | Tür | Açıklama |
| --- | --- | --- |
| `type` | `string` | `"sprite"` veya `"link"`. |
| `id` | `hash` | Etkileşim iletilerinde kullanılan nesne tanımlayıcısı. |
| `text_offset` | `number` | Görünür metindeki, Unicode kod noktalarıyla ölçülen sıfır tabanlı konum. İşaretleme dahil edilmez ve karakter başvuruları, çözümlendikleri karakterler olarak sayılır. Bir sprite için bu, ekleme noktasıdır. |
| `text_length` | `number` | Çevrelenen görünür metnin Unicode kod noktaları cinsinden uzunluğu. Bir sprite nesnesinin uzunluğu, nesneyi temsil etmek için eklenen U+FFFC kod noktası nedeniyle birdir. |
| `width` | `number` | Metin yerleşimi birimleri cinsinden hesaplanan genişlik. Bağlantıların genişliği şu anda sıfırdır. |
| `height` | `number` | Metin yerleşimi birimleri cinsinden hesaplanan yükseklik. Bağlantıların yüksekliği şu anda sıfırdır. |
| `x` | `number` | Nesnenin sol alt köşesinin, metin yerleşiminin sol üst başlangıç noktasına göre yatay konumu. |
| `y` | `number` | Nesnenin sol alt köşesinin, metin yerleşiminin sol üst başlangıç noktasına göre dikey konumu. |
| `attributes` | `table` | Dize türünde anahtar/değer çiftleri olarak tüm etiket öznitelikleri. Öznitelik değerleri, `"2em"` gibi kaynak gösterimlerini korur. Kısaltılmış biçimdeki adsız değer, `value` anahtarı altında saklanır. |

::: sidenote
`text_offset` ve `text_length`, UTF-8 bayt uzaklıkları değildir. `å` veya `猫` gibi ASCII dışı bir karakter, tek bir konum olarak sayılır.
:::

### Lua örneği

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

## Yararlı birleşimler

### Yatay renk geçişli, renkli dış çizgi

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

Renk geçişi yalnızca dolgu rengiyle çarpılır; dış çizgi kendi rengini korur.

### Bir cümleyi titretme, bir sözcüğe renk geçişi uygulama

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

Dıştaki konum efekti her glife uygulanır. İç içe yerleştirilmiş renk efekti yalnızca "whole" sözcüğüne uygulanır.

### Diğerlerini kaybetmeden tek bir özelliği geçersiz kılma

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

İçteki renk, devralınan dış çizgi genişliğini ve rengini korurken dolgu rengini değiştirir.
