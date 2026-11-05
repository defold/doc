---
title: Defold'da etiket metin bileşenleri
brief: Bu kılavuz, oyun dünyasındaki oyun nesnelerinde metin kullanmak için etiket bileşenlerinin nasıl kullanılacağını açıklar.
---

# Etiket {#label}

Bir *etiket* (Label) bileşeni (component), bir metin parçasını oyun uzayında ekranda görüntüler. Varsayılan olarak tüm sprite ve karo grafikleriyle birlikte sıralanır ve çizilir. Bileşenin, metnin nasıl işleneceğini (rendering) belirleyen bir dizi özelliği vardır. Defold'un GUI sistemi metni destekler ancak GUI öğelerini oyun dünyasına yerleştirmek zor olabilir. Etiketler bunu kolaylaştırır.

## Etiket oluşturma {#creating-a-label}

Bir etiket bileşeni oluşturmak için oyun nesnesine (game object) <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Label</kbd> seçeneğini seçin.

![Etiket ekleme](images/label/add_label.png)

(Aynı şablondan birden fazla etiket örneği oluşturmak isterseniz alternatif olarak yeni bir etiket bileşeni dosyası oluşturabilirsiniz: *Assets* tarayıcısındaki bir klasöre <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Label</kbd> seçeneğini seçin, ardından dosyayı istediğiniz oyun nesnelerine bileşen olarak ekleyin)

![Yeni etiket](images/label/label.png)

*Font* özelliğini kullanmak istediğiniz yazı tipine ayarlayın ve *Material* özelliğini yazı tipi türüyle eşleşen bir materyale ayarladığınızdan emin olun:

![Yazı tipi ve materyal](images/label/font_material.png)

## Vektör yazı tipleri ve renkli emoji {#vector-fonts-and-color-emoji}

Bir Vector yazı tipi kullanmak için [Vektör yazı tipi kurulumunu](/manuals/font/#vector-fonts) izleyin, `.font` kaynağını etiketin *Font* özelliğine atayın ve etiketin *Material* özelliğini `/builtins/fonts/label-vector.material` olarak ayarlayın. Görüntülenen boyutu kontrol etmek için *Font Size* özelliğini kullanın.

Renkli emoji için [COLRv1 yedek yazı tipi ve paketleme kurulumunu](/manuals/font/#color-emoji) da tamamlayın. Aşağıdaki örnek, `label` kimliğine sahip bir etiket ve aynı oyun nesnesinde bir betik olduğunu varsayar. Selamlamayı yalnızca glifleri hazır olduktan sonra görüntülemek için etiketin *Text* alanını boş bırakın:

```lua
function init(self)
    local text = "Hello 😀 🍎 🚀"
    local font_resource = go.get("#label", "font")
    -- Add the fallback once for this shared font resource.
    font.add_font(font_resource, "/fonts/NotoColorEmoji-Regular.ttf")
    font.prewarm_text(font_resource, text, function(self, request_id, result, err)
        if result then
            go.set("#label", "text", text)
        else
            print("Could not prepare label text:", err)
        end
    end)
end
```

Normal harfler özgün yazı tipini, emoji ise eklenen renkli yazı tipini kullanır. Diğer etiketler veya GUI metin düğümleri bu yazı tipi kaynağını paylaşıyorsa yedek yazı tipini tek bir yerde başlatıp yeniden kullanın.

## Etiket özellikleri {#label-properties}

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
: Bu etiketi işlemek için kullanılacak materyal. Yazı tipinin modu veya kaynağıyla (Bitmap, SDF, Vector veya BMFont) eşleşen bir materyal seçin. Eşleşen yerleşik Label materyalleri için [Yazı tipi materyalleri](/manuals/font/#font-materials) bölümüne bakın.

### Harmanlama modları {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Dayanak noktası ve hizalama {#pivot-and-alignment}

*Pivot* özelliğini ayarlayarak metnin hizalama modunu değiştirebilirsiniz.

*Ortalanmış*
: Dayanak noktası `Center`, `North` veya `South` olarak ayarlanırsa metin ortalanır.

*Sola hizalı*
: Dayanak noktası `West` modlarından herhangi birine ayarlanırsa metin sola hizalanır.

*Sağa hizalı*
: Dayanak noktası `East` modlarından herhangi birine ayarlanırsa metin sağa hizalanır.

![Metin hizalama](images/label/align.png)

## Çalışma sırasında değiştirme {#runtime-manipulation}

Etiket metnini ve çeşitli diğer özellikleri alıp ayarlayarak çalışma sırasında etiketleri değiştirebilirsiniz.

`text`
: Etiketin metin içeriği (`string`). `go.get()` ve `go.set()` aracılığıyla kullanılabilir.

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
`label.set_text()` ve `label.get_text()` işlevlerinin kullanımı artık önerilmez; bunların yerine `text` özelliği önerilir. Eski işlevler uyumluluk için kullanılabilir durumdadır. Eski ayarlama işlevi bir iletiyi kuyruğa eklerken `go.set()` metni hemen günceller.
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

## Proje yapılandırması {#project-configuration}

*game.project* dosyasında etiketlerle ilgili birkaç [proje ayarı](/manuals/project-settings#label) bulunur.
