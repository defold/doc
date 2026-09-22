---
title: 2B görüntüleri gösterme
brief: Bu kılavuz, sprite bileşeniyle 2B görüntülerin ve animasyonların nasıl gösterileceğini açıklar.
---

# Sprite bileşenleri

Sprite bileşeni (sprite component), ekranda gösterilen basit bir görüntü veya kare dizisi animasyonudur (flipbook animation).

![sprite bileşeni](images/graphics/sprite.png)

Sprite bileşeni, grafikleri için bir [atlas](/manuals/atlas) veya [karo kaynağı](/manuals/tilesource) (tile source) kullanabilir.

## Sprite özellikleri

*Id*, *Position* ve *Rotation* özelliklerine ek olarak bileşene özgü şu özellikler bulunur:

*Image*
: Gölgelendiricide (shader) tek bir örnekleyici (sampler) varsa bu alan `Image` olarak adlandırılır. Aksi halde her yuva, materyaldeki doku örnekleyicisinin adını alır.
Her yuva, o doku örnekleyicisinde sprite bileşeni için kullanılacak atlas veya karo kaynağını belirtir.

*Default Animation*
: Sprite bileşeninde kullanılacak animasyon. Animasyon bilgisi ilk atlastan veya karo kaynağından alınır.

*Material*
: Sprite bileşenini işlemek (rendering) için kullanılacak materyal.

*Blend Mode*
: Sprite bileşenini işlerken kullanılacak harmanlama modu (blend mode).

*Size Mode*
: `Automatic` olarak ayarlanırsa düzenleyici sprite bileşeninin boyutunu ayarlar. `Manual` olarak ayarlanırsa boyutu kendiniz belirleyebilirsiniz.

*Slice 9*
: Sprite bileşeni yeniden boyutlandırıldığında dokusunun kenarlarındaki piksel boyutunu korumak için ayarlayın.

:[Slice-9](../shared/slice-9-texturing.md)

### Harmanlama modları
:[blend-modes](../shared/blend-modes.md)

## Çalışma sırasında değiştirme

Sprite bileşenlerini çalışma sırasında çeşitli işlevler ve özellikler aracılığıyla değiştirebilirsiniz (kullanım için [API belgelerine](/ref/sprite/) bakın). İşlevler:

* `sprite.play_flipbook()` - Sprite bileşeninde bir animasyon oynatır.
* `sprite.set_hflip()` ve `sprite.set_vflip()` - Sprite animasyonunun yatay ve dikey çevirme durumunu ayarlar.

Sprite bileşeninin ayrıca `go.get()` ve `go.set()` kullanılarak değiştirilebilen çeşitli özellikleri vardır:

`cursor`
: Normalleştirilmiş animasyon imleci (`number`).

`image`
: Sprite görüntüsü (`hash`). Bunu, bir atlas veya karo kaynağına başvuran kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Bir örnek için [API başvurusuna](/ref/sprite/#image) bakın.

`material`
: Sprite materyali (`hash`). Bunu, bir materyal kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Bir örnek için [API başvurusuna](/ref/sprite/#material) bakın.

`playback_rate`
: Animasyonun oynatma hızı (`number`).

`scale`
: Sprite bileşeninin her eksende farklı olabilen ölçeği (`vector3`).

`size`
: Sprite bileşeninin boyutu (`vector3`). Yalnızca sprite bileşeninin `Size Mode` özelliği `Manual` olarak ayarlanmışsa değiştirilebilir.

## Materyal sabitleri

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: Sprite bileşeninin renk çarpanı (tint) (`vector4`). `vector4`, renk çarpanını temsil etmek için kullanılır; `x`, `y`, `z` ve `w` sırasıyla kırmızı, yeşil, mavi ve alfa çarpanlarına karşılık gelir.

## Materyal öznitelikleri

Sprite bileşeni, o anda atanmış materyalin köşe özniteliklerini (vertex attributes) geçersiz kılabilir; bu öznitelikler bileşenden köşe gölgelendiricisine iletilir (daha fazla bilgi için [Materyal kılavuzuna](/manuals/material/#attributes) bakın).

Materyalde belirtilen öznitelikler, özellik denetleyicisinde normal özellikler olarak görünür ve her sprite bileşeninde ayrı ayrı ayarlanabilir. Özniteliklerden herhangi biri geçersiz kılınırsa, geçersiz kılınmış bir özellik olarak görünür ve diskteki sprite dosyasında saklanır:

![sprite öznitelikleri](../images/graphics/sprite-attributes.png)

## Proje yapılandırması

*game.project* dosyasında sprite bileşenleriyle ilgili birkaç [proje ayarı](/manuals/project-settings#sprite) bulunur.

## Çok dokulu sprite bileşenleri {#multi-textured-sprites}

Bir sprite bileşeni birden fazla doku kullandığında dikkat edilmesi gereken bazı noktalar vardır.

### Animasyonlar

Animasyon verileri (fps, kare adları) şu anda ilk dokudan alınır. Buna "belirleyici animasyon" (driving animation) diyeceğiz.

Belirleyici animasyonun görüntü tanımlayıcıları, başka bir dokudaki görüntüleri bulmak için kullanılır.
Bu nedenle, kare tanımlayıcılarının dokular arasında eşleştiğinden emin olmak önemlidir.

Örneğin, `diffuse.atlas` dosyanızda şöyle bir `run` animasyonu varsa:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Kare tanımlayıcıları `run/hero_run_color_1` biçiminde olur; bu tanımlayıcının, örneğin şu `normal.atlas` dosyasında bulunması pek olası değildir:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Bu nedenle, bunları yeniden adlandırmak için [atlastaki](/manuals/material/) `Rename patterns` alanını kullanırız.
İlgili atlaslarda `_color=` ve `_normal=` değerlerini ayarladığınızda her iki atlasta da şu kare adlarını elde edersiniz:

```
run/hero_run_1
run/hero_run_2
...
```

### UV koordinatları

UV koordinatları ilk dokudan alınır. Yalnızca bir köşe kümesi bulunduğundan, ikincil dokularda daha fazla UV koordinatı veya farklı bir şekil varsa
zaten iyi bir eşleşme garanti edemeyiz.

Bu noktaya dikkat etmek önemlidir; görüntülerin yeterince benzer şekillere sahip olduğundan emin olun, aksi takdirde doku taşması (texture bleeding) yaşayabilirsiniz.

Her dokudaki görüntülerin boyutları farklı olabilir.
