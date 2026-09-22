---
title: Defold'da etiket metin bileşenleri
brief: Bu kılavuz, oyun dünyasındaki oyun nesnelerinde metin kullanmak için etiket bileşenlerinin nasıl kullanılacağını açıklar.
---

# Etiket

Bir *etiket* (Label) bileşeni (component), bir metin parçasını oyun uzayında ekranda görüntüler. Varsayılan olarak tüm sprite ve karo grafikleriyle birlikte sıralanır ve çizilir. Bileşenin, metnin nasıl işleneceğini (rendering) belirleyen bir dizi özelliği vardır. Defold'un GUI sistemi metni destekler ancak GUI öğelerini oyun dünyasına yerleştirmek zor olabilir. Etiketler bunu kolaylaştırır.

## Etiket oluşturma

Bir etiket bileşeni oluşturmak için oyun nesnesine (game object) <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Label</kbd> seçeneğini seçin.

![Etiket ekleme](images/label/add_label.png)

(Aynı şablondan birden fazla etiket örneği oluşturmak isterseniz alternatif olarak yeni bir etiket bileşeni dosyası oluşturabilirsiniz: *Assets* tarayıcısındaki bir klasöre <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Label</kbd> seçeneğini seçin, ardından dosyayı istediğiniz oyun nesnelerine bileşen olarak ekleyin)

![Yeni etiket](images/label/label.png)

*Font* özelliğini kullanmak istediğiniz yazı tipine ayarlayın ve *Material* özelliğini yazı tipi türüyle eşleşen bir materyale ayarladığınızdan emin olun:

![Yazı tipi ve materyal](images/label/font_material.png)

## Etiket özellikleri

*Id*, *Position*, *Rotation* ve *Scale* özelliklerinin yanı sıra bileşene özgü aşağıdaki özellikler de bulunur:

*Text*
: Etiketin metin içeriği.

*Size*
: Metnin sınırlayıcı kutusunun boyutu. *Line Break* etkinleştirilmişse genişlik, metnin hangi noktada alt satıra kaydırılacağını belirtir.

*Color*
: Metnin rengi.

*Outline*
: Dış çizginin rengi.

*Shadow*
: Gölgenin rengi.

::: sidenote
Varsayılan materyalde performans nedeniyle gölge işlemenin devre dışı bırakıldığını unutmayın.
:::

*Leading*
: Satır aralığı için bir ölçekleme katsayısı. 0 değeri satır aralığını kaldırır. Varsayılan değer 1'dir.

*Tracking*
: Harf aralığı için bir ölçekleme katsayısı. Varsayılan değer 0'dır.

*Pivot*
: Metnin dayanak noktası (pivot). Metin hizalamasını değiştirmek için bunu kullanın (aşağıya bakın).

*Blend Mode*
: Etiketi işlerken kullanılacak harmanlama modu (blend mode).

*Line Break*
: Metin hizalaması dayanak noktası ayarını izler ve bu özelliği etkinleştirmek metnin birden fazla satıra yayılmasını sağlar. Bileşenin genişliği, metnin nerede alt satıra kaydırılacağını belirler. Metnin alt satıra kaydırılabilmesi için içinde bir boşluk bulunması gerektiğini unutmayın.

*Font*
: Bu etiket için kullanılacak yazı tipi kaynağı.

*Material*
: Bu etiketi işlemek için kullanılacak materyal. Kullandığınız yazı tipi türü (bit eşlem, uzaklık alanı veya BMFont) için oluşturulmuş bir materyal seçtiğinizden emin olun.

### Harmanlama modları
:[blend-modes](../shared/blend-modes.md)

### Dayanak noktası ve hizalama

*Pivot* özelliğini ayarlayarak metnin hizalama modunu değiştirebilirsiniz.

*Ortalanmış*
: Dayanak noktası `Center`, `North` veya `South` olarak ayarlanırsa metin ortalanır.

*Sola hizalı*
: Dayanak noktası `West` modlarından herhangi birine ayarlanırsa metin sola hizalanır.

*Sağa hizalı*
: Dayanak noktası `East` modlarından herhangi birine ayarlanırsa metin sağa hizalanır.

![Metin hizalama](images/label/align.png)

## Çalışma sırasında değiştirme

Etiket metnini ve çeşitli diğer özellikleri alıp ayarlayarak çalışma sırasında etiketleri değiştirebilirsiniz.

`text`
: Etiketin metin içeriği (`string`). Defold 1.13.2 sürümünden itibaren `go.get()` ve `go.set()` aracılığıyla kullanılabilir.

`color`
: Etiket rengi (`vector4`)

`outline`
: Etiketin dış çizgi rengi (`vector4`)

`shadow`
: Etiketin gölge rengi (`vector4`)

`scale`
: Etiketin ölçeği; tüm eksenlerde eşit ölçekleme için bir `number` veya her eksende ayrı ölçekleme için bir `vector3`.

`size`
: Etiketin boyutu (`vector3`)

```lua
function init(self)
    -- Set the text of the "my_label" component in the same game object
    -- as this script.
    go.set("#my_label", "text", "New text")
    local text = go.get("#my_label", "text")
    print(text) -- New text
end
```

::: sidenote
Defold 1.13.2 sürümünden itibaren `label.set_text()` ve `label.get_text()` işlevlerinin kullanımı artık önerilmez; bunların yerine `text` özelliği önerilir. Eski işlevler uyumluluk için kullanılabilir durumdadır. Eski ayarlama işlevi bir iletiyi kuyruğa eklerken `go.set()` metni hemen günceller.
:::

```lua
function init(self)
    -- Set the color of the "my_label" component in the same game object
    -- as this script. Color is a RGBA value stored in a vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...and remove the outline, by setting its alpha to 0...
    go.set("#my_label", "outline.w", 0)

    -- ...and scale it x2 along x axis.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Proje yapılandırması

*game.project* dosyasında etiketlerle ilgili birkaç [proje ayarı](/manuals/project-settings#label) bulunur.
