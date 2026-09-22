---
title: Defold'da özellikler
brief: Bu kılavuz, Defold'da hangi özellik türlerinin bulunduğunu, bunların nasıl kullanıldığını ve bunlara nasıl animasyon uygulandığını açıklar.
---

# Özellikler

Defold, oyun nesneleri (game object), bileşenler (component) ve GUI düğümleri (GUI node) için okunabilen, ayarlanabilen ve animasyon uygulanabilen özellikler (property) sunar. Aşağıdaki özellik türleri bulunur:

* Sistem tarafından tanımlanan oyun nesnesi dönüşümleri (konum, dönme ve ölçek) ve bileşene özgü özellikler (örneğin bir sprite bileşeninin piksel boyutu veya bir çarpışma nesnesinin (collision object) kütlesi)
* Lua betiklerinde tanımlanan, kullanıcı tanımlı betik bileşeni (script component) özellikleri (ayrıntılar için [Betik özellikleri belgelerine](/manuals/script-properties) bakın)
* GUI düğümü özellikleri
* Gölgelendiricilerde (shader) ve materyal (material) dosyalarında tanımlanan gölgelendirici sabitleri (ayrıntılar için [Materyal belgelerine](/manuals/material) bakın)

Sayısal özelliklerin giriş alanının üzerine geldiğinizde bir sürükleme tutamacı görünür. Tutamacı sağa/sola veya yukarı/aşağı sürükleyerek değeri sırasıyla artırabilir/azaltabilirsiniz.

Bir özelliğe, bulunduğu yere bağlı olarak genel amaçlı bir işlev veya özelliğe özgü bir işlev aracılığıyla erişirsiniz. Özelliklerin birçoğuna otomatik olarak animasyon uygulanabilir. Hem performans hem de kullanım kolaylığı açısından, özellikleri kendiniz değiştirmek (bir `update()` işlevinin içinde) yerine yerleşik sistem aracılığıyla animasyon uygulamanız özellikle önerilir.

`vector3`, `vector4` veya kuaterniyon (`quaternion`) türündeki bileşik özellikler, alt bileşenlerini (`x`, `y`, `z` ve `w`) de erişime açar. Adın sonuna bir nokta (`.`) ve bileşenin adını ekleyerek bileşenleri ayrı ayrı adresleyebilirsiniz. Örneğin, bir oyun nesnesinin konumunun x bileşenini ayarlamak için:

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

`go.get()`, `go.set()` ve `go.animate()` işlevleri ilk parametre olarak bir başvuru, ikinci parametre olarak bir özellik tanımlayıcısı alır. Başvuru, oyun nesnesini veya bileşeni tanımlar ve bir dize, karma (hash) değeri veya URL olabilir. URL'ler [adresleme kılavuzunda](/manuals/addressing) ayrıntılı olarak açıklanır. Özellik tanımlayıcısı, özelliği adlandıran bir dize veya karma değeridir:

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

GUI düğümleri için düğüm, özelliğe özgü bir işleve veya genel amaçlı `gui.get()` ve `gui.set()` işlevlerine ilk parametre olarak verilir:

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Oyun nesnesi ve bileşen özellikleri

Tüm oyun nesneleri ve bazı bileşen türleri, çalışma sırasında okunabilen ve değiştirilebilen özelliklere sahiptir. Bu değerleri [`go.get()`](/ref/go#go.get) ile okuyun ve [`go.set()`](/ref/go#go.set) ile yazın. Özellik değerinin türüne bağlı olarak, değerlere [`go.animate()`](/ref/go#go.animate) ile animasyon uygulayabilirsiniz. Özelliklerin küçük bir bölümü salt okunurdur.

`get`{.mark}
: [`go.get()`](/ref/go#go.get) ile okunabilir.

`get+set`{.mark}
: [`go.get()`](/ref/go#go.get) ile okunabilir ve [`go.set()`](/ref/go#go.set) ile yazılabilir. Sayısal değerlere [`go.animate()`](/ref/go#go.animate) ile animasyon uygulanabilir.

*Oyun nesnesi özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | Oyun nesnesinin yerel konumu. | `vector3`      | `get+set`{.mark} |
| *rotation* | Oyun nesnesinin `quaternion` olarak ifade edilen yerel dönmesi.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Oyun nesnesinin Euler açılarıyla ifade edilen yerel dönmesi. | `vector3` | `get+set`{.mark} |
| *scale*    | Oyun nesnesinin yerel, eşit olmayan ölçeği; her bileşeni ilgili eksen boyunca bir çarpan içeren bir vektör olarak ifade edilir. Z'yi değiştirmeden X ve Y boyutlarını iki katına çıkarmak için `vmath.vector3(2.0, 2.0, 1.0)` kullanın. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | Oyun nesnesinin X ve Y eksenleri boyunca yerel, eşit olmayan ölçeği. Z ekseninde ölçekleme amaçlanmadığında bu özelliği veya `go.set_scale_xy()` işlevini kullanın. | `vector3` | `get+set`{.mark} |

::: sidenote
Oyun nesnesi dönüşümüyle çalışmak için özel işlevler de bulunur: `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` ve `go.set_scale_xy()`.
:::

*Sprite bileşeni özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | Sprite bileşeninin ölçeklenmemiş boyutu---kaynak atlastan alınan boyutu. | `vector3` | `get`{.mark} |
| *image* | Sprite bileşeninin doku yolunun karma değeri. | `hash` | `get`{.mark}|
| *scale* | Sprite bileşeninin eşit olmayan ölçeği. | `vector3` | `get+set`{.mark}|
| *scale.xy* | Sprite bileşeninin X ve Y eksenleri boyunca eşit olmayan ölçeği. | `vector3` | `get+set`{.mark}|
| *material* | Sprite bileşeninin kullandığı materyal. | `hash` | `get+set`{.mark}|
| *cursor* | Oynatma imlecinin konumu (0--1 arasında). | `number` | `get+set`{.mark}|
| *playback_rate* | Kare dizisi animasyonunun (flipbook animation) kare hızı. | `number` | `get+set`{.mark}|

*Çarpışma nesnesi bileşeni özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | Çarpışma nesnesinin kütlesi. | `number` | `get`{.mark} |
| *linear_velocity* | Çarpışma nesnesinin geçerli doğrusal hızı. | `vector3` | `get`{.mark} |
| *angular_velocity* | Çarpışma nesnesinin geçerli açısal hızı. | `vector3` | `get`{.mark} |
| *linear_damping* | Çarpışma nesnesinin doğrusal sönümlemesi. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Çarpışma nesnesinin açısal sönümlemesi. | `vector3` | `get+set`{.mark} |

*Model (3B) bileşeni özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | Geçerli animasyon.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Modelin doku yollarının karma değerleri. | `hash` | `get+set`{.mark}|
| *cursor*  | Oynatma imlecinin konumu (0--1 arasında). | `number`   | `get+set`{.mark} |
| *playback_rate* | Animasyonun oynatma hızı. Animasyonun oynatma hızı için bir çarpandır. | `number` | `get+set`{.mark} |
| *material* | Modelin kullandığı materyal. | `hash` | `get+set`{.mark}|

*Etiket bileşeni özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *text* | Etiketin (label) metin içeriği. Defold 1.13.2 sürümünden itibaren kullanılabilir. | `string` | `get+set`{.mark} |
| *scale* | Etiketin ölçeği. | `vector3` | `get+set`{.mark} |
| *scale.xy* | Etiketin X ve Y eksenleri boyunca ölçeği. | `vector3` | `get+set`{.mark}|
| *color*     | Etiketin rengi. | `vector4` | `get+set`{.mark} |
| *outline* | Etiketin dış çizgi rengi. | `vector4` | `get+set`{.mark} |
| *shadow* | Etiketin gölge rengi. | `vector4` | `get+set`{.mark} |
| *size* | Etiketin boyutu. Satır kaydırma etkinse boyut, metni sınırlar. | `vector3` | `get+set`{.mark} |
| *material* | Etiketin kullandığı materyal. | `hash` | `get+set`{.mark}|
| *font* | Etiketin kullandığı yazı tipi. | `hash` | `get+set`{.mark}|


## GUI düğümü özellikleri

GUI düğümlerinin `gui.get_position()` ve `gui.set_position()` gibi, özellik değerlerini okumaya ve ayarlamaya özgü işlevleri vardır. Aşağıda listelenen yerleşik özellikler, alternatif olarak `gui.get(node, property)` ve `gui.set(node, property, value)` ile de okunup yazılabilir. Diğer düğüm değerleri yine de kendilerine özgü işlevleri gerektirebilir. GUI düğümlerindeki materyal sabitleri de genel amaçlı işlevleri kullanır. Bir vektör özelliğinin tek bir bileşenini adreslemek için sonuna bileşen adını ekleyin; örneğin `gui.set(node, "color.x", 1)`.

Genel amaçlı ve özelliğe özgü işlevler her zaman aynı değer türlerini kullanmaz. `gui.get()` işleviyle `position`, `scale`, `size` ve `euler` özellikleri bütün olarak okunduğunda bir `vector4` döndürülür; karşılık gelen özelliğe özgü işlevler ise bir `vector3` döndürür. `gui.set()` bu özellikler için hem `vector3` hem de `vector4` kabul eder. Genel amaçlı `rotation` özelliği bir kuaterniyon kullanır; dönmeyi derece cinsinden ayarlarken `euler` kullanın.

* `position` (veya `gui.PROP_POSITION`)
* `rotation` (veya `gui.PROP_ROTATION`)
* `euler` (veya `gui.PROP_EULER`)
* `scale` (veya `gui.PROP_SCALE`)
* `color` (veya `gui.PROP_COLOR`)
* `outline` (veya `gui.PROP_OUTLINE`)
* `shadow` (veya `gui.PROP_SHADOW`)
* `size` (veya `gui.PROP_SIZE`)
* `fill_angle` (veya `gui.PROP_FILL_ANGLE`)
* `inner_radius` (veya `gui.PROP_INNER_RADIUS`)
* `leading` (veya `gui.PROP_LEADING`)
* `tracking` (veya `gui.PROP_TRACKING`)
* `slice9` (veya `gui.PROP_SLICE9`)

Tüm renk değerlerinin, bileşenleri RGBA değerlerine karşılık gelen bir `vector4` içinde kodlandığını unutmayın:

`x`
: Kırmızı renk bileşeni

`y`
: Yeşil renk bileşeni

`z`
: Mavi renk bileşeni

`w`
: Alfa bileşeni

*GUI düğümü özellikleri*

| özellik   | açıklama                            | tür            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | Düğümün yüzey rengi.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | Düğümün dış çizgi rengi.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | Düğümün konumu. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | Düğümün dönmesi. Okuma işlevi bir kuaterniyon döndürür; ayarlama işlevi bir kuaterniyon veya vektör biçiminde Euler açıları kabul eder. | `quaternion`, `vector3` veya `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | Düğümün derece cinsinden Euler açılarıyla ifade edilen dönmesi. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | Düğümün her eksen boyunca bir çarpan olarak ifade edilen ölçeği. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | Düğümün gölge rengi. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | Düğümün ölçeklenmemiş boyutu. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | Daire dilimi düğümünün (pie node) saat yönünün tersine, derece cinsinden ifade edilen dolgu açısı. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | Daire dilimi düğümünün iç yarıçapı. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | Metin düğümünün satır aralığı ölçeği. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | Metin düğümünün harf aralığı ölçeği. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | Bir slice9 düğümünün kenar mesafeleri. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
