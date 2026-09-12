---
title: Defold karo haritası kılavuzu
brief: Bu kılavuz Defold'un karo haritası desteğini ayrıntılarıyla açıklar.
---

# Karo haritası

*Karo haritası* (Tile Map), bir *karo kaynağındaki* (Tile Source) karoları geniş bir ızgara alanına yerleştirmenizi veya boyamanızı sağlayan bir bileşendir (component). Karo haritaları genellikle oyun bölümlerinin ortamlarını oluşturmak için kullanılır. Ayrıca, çarpışma algılama ve fizik simülasyonu için haritalarınızda karo kaynağının *çarpışma şekillerini* (Collision Shapes) kullanabilirsiniz ([örnek](/examples/tilemap/collisions/)).

Bir karo haritası oluşturmadan önce bir karo kaynağı oluşturmanız gerekir. Karo kaynağının nasıl oluşturulduğunu öğrenmek için [Karo kaynağı kılavuzuna](/manuals/tilesource) bakın.

## Karo haritası oluşturma

Yeni bir karo haritası oluşturmak için:

- *Assets* tarayıcısında bir konuma <kbd>sağ tıklayın</kbd>, ardından <kbd>New... ▸ Tile Map</kbd> seçeneğini seçin).
- Dosyaya bir ad verin.
- Yeni karo haritası otomatik olarak karo haritası düzenleyicisinde açılır.

  ![Yeni karo haritası](images/tilemap/tilemap.png)

- *Tile Source* özelliğini hazırladığınız bir karo kaynağı dosyasına ayarlayın.

Karo haritanıza karolar boyamak için:

1. *Outline* görünümünde üzerine boyama yapacağınız bir *Layer* katmanı seçin veya oluşturun.
2. Fırça olarak kullanılacak bir karo seçin (karo paletini göstermek için <kbd>Space</kbd> tuşuna basın) veya birden fazla karodan oluşan dikdörtgen bir fırça oluşturmak için palette tıklayıp sürükleyerek birkaç karo seçin.

   ![Palet](images/tilemap/palette.png)

3. Seçili fırçayla boyayın. Bir karoyu silmek için boş bir karo seçip fırça olarak kullanın veya silgiyi seçin (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Karoları boyama](images/tilemap/paint_tiles.png)

Karoları doğrudan bir katmandan alabilir ve seçimi fırça olarak kullanabilirsiniz. <kbd>Shift</kbd> tuşunu basılı tutup bir karoya tıklayarak onu geçerli fırça olarak seçin. <kbd>Shift</kbd> tuşunu basılı tutarken tıklayıp sürükleyerek daha büyük bir fırça olarak kullanılacak bir karo bloğu da seçebilirsiniz. Benzer şekilde, <kbd>Shift+Ctrl</kbd> tuşlarını basılı tutarak karoları kesebilir veya <kbd>Shift+Alt</kbd> tuşlarını basılı tutarak silebilirsiniz.

Fırçayı saat yönünde döndürmek için <kbd>Z</kbd> tuşunu kullanın. Fırçayı yatay çevirmek için <kbd>X</kbd>, dikey çevirmek için <kbd>Y</kbd> tuşunu kullanın.

![Karoları seçme](images/tilemap/pick_tiles.png)

## Oyununuza karo haritası ekleme

Oyununuza bir karo haritası eklemek için:

1. Karo haritası bileşenini barındıracak bir oyun nesnesi (game object) oluşturun. Oyun nesnesi bir dosyada bulunabilir veya doğrudan bir koleksiyonda (collection) oluşturulabilir.
2. Oyun nesnesinin köküne sağ tıklayın ve <kbd>Add Component File</kbd> seçeneğini seçin.
3. Karo haritası dosyasını seçin.

![Karo haritasını kullanma](images/tilemap/use_tilemap.png)

## Çalışma sırasında değiştirme

Karo haritalarını çalışma sırasında çeşitli işlevler ve özellikler aracılığıyla değiştirebilirsiniz (kullanım için [API belgelerine](/ref/tilemap/) bakın).

### Betikten karoları değiştirme

Oyununuz çalışırken bir karo haritasının içeriğini dinamik olarak okuyabilir ve yazabilirsiniz. Bunun için [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) ve [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) işlevlerini kullanın:

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Karo haritası özellikleri

*Id*, *Position*, *Rotation* ve *Scale* özelliklerinin yanı sıra bileşene özgü şu özellikler bulunur:

*Tile Source*
: Karo haritası için kullanılacak karo kaynağı.

*Material*
: Karo haritasının işlenmesinde (rendering), yani görüntüsünün oluşturulmasında kullanılacak materyal (material).

*Blend Mode*
: Karo haritası işlenirken kullanılacak harmanlama modu (blend mode).

### Harmanlama modları
:[blend-modes](../shared/blend-modes.md)

### Özellikleri değiştirme

Karo haritası, `go.get()` ve `go.set()` kullanılarak değiştirilebilen çeşitli özelliklere sahiptir:

`tile_source`
: Karo haritasının karo kaynağı (`hash`). Bunu bir karo kaynağına başvuran kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Örnek için [API başvurusuna](/ref/tilemap/#tile_source) bakın.

`material`
: Karo haritasının materyali (`hash`). Bunu bir materyale başvuran kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Örnek için [API başvurusuna](/ref/tilemap/#material) bakın.

### Materyal sabitleri

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: Karo haritasının renk çarpanı (tint) (`vector4`). Renk çarpanını temsil etmek için `vector4` kullanılır; x, y, z ve w sırasıyla kırmızı, yeşil, mavi ve alfa çarpanlarına karşılık gelir.

## Proje yapılandırması

*game.project* dosyasında karo haritalarıyla ilgili birkaç [proje ayarı](/manuals/project-settings#tilemap) bulunur.

## Harici araçlar

Doğrudan Defold karo haritalarına dışa aktarabilen harici harita/bölüm düzenleyicileri vardır:

### Tiled

[Tiled](https://www.mapeditor.org/), dik açılı, izometrik ve altıgen haritalar için tanınan ve yaygın olarak kullanılan bir harita düzenleyicisidir. Tiled çok çeşitli özellikleri destekler ve [doğrudan Defold'a dışa aktarabilir](https://doc.mapeditor.org/en/stable/manual/export-defold/). Karo haritası verilerinin ve ek üst verilerin nasıl dışa aktarılacağı hakkında daha fazla bilgi için [Defold kullanıcısı "goeshard" tarafından yazılan bu blog yazısını](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/) okuyun.


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold), basit temel karolardan otomatik olarak eksiksiz karo kümeleri oluşturmak için kullanılabilir ve doğrudan Defold'a dışa aktarabilen bir harita düzenleyicisine sahiptir.



