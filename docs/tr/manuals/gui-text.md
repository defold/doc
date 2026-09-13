---
title: Defold GUI metin düğümleri
brief: Bu kılavuz, GUI sahnelerine nasıl metin ekleneceğini açıklar.
---

# GUI metin düğümleri

Defold, GUI sahnesinde metin işleme (rendering) için özel bir GUI düğümü (GUI node) türünü destekler. Projeye eklenen herhangi bir yazı tipi kaynağı, metin düğümlerini (text node) işlemek için kullanılabilir.

Düzenleyici önizlemesi, motorun yazı tipi işleyicisini kullanarak metin şekillendirmeyi ve sağdan sola yerleşimi destekler. Gerekli yazı tipi ve App Manifest ayarları için [metin yerleşimi desteğine](/manuals/font/#text-layout-support-eg-right-to-left) bakın.

## Metin düğümleri ekleme

GUI metin düğümlerinde kullanmak istediğiniz yazı tiplerinin GUI bileşenine (GUI component) eklenmesi gerekir. Bunun için *Fonts* klasörüne sağ tıklayın, üstteki <kbd>GUI</kbd> menüsünü kullanın veya ilgili klavye kısayoluna basın.

![Yazı tipleri](images/gui-text/fonts.png)

Metin düğümlerinin bir dizi özel özelliği vardır:

*Font*
: Oluşturduğunuz her metin düğümünün *Font* özelliği ayarlanmalıdır.

*Text*
: Bu özellik, görüntülenen metni içerir.

*Line Break*
: Metin hizalaması, dayanak noktası (pivot) ayarını izler ve bu özelliğin ayarlanması, metnin birden çok satıra yayılmasını sağlar. Düğümün genişliği, metnin nerede alt satıra kaydırılacağını belirler.

## Hizalama

Düğümün dayanak noktasını ayarlayarak metnin hizalama modunu değiştirebilirsiniz.

*Ortalanmış*
: Dayanak noktası `Center`, `North` veya `South` olarak ayarlanırsa metin ortalanır.

*Sola hizalı*
: Dayanak noktası `West` modlarından herhangi birine ayarlanırsa metin sola hizalanır.

*Sağa hizalı*
: Dayanak noktası `East` modlarından herhangi birine ayarlanırsa metin sağa hizalanır.

![Metin hizalaması](images/gui-text/align.png)

## Çalışma sırasında metin düğümlerini değiştirme

Metin düğümleri, boyut, dayanak noktası, renk ve benzerlerini ayarlayan tüm genel düğüm düzenleme işlevleriyle değiştirilebilir. Yalnızca metin düğümlerine özgü birkaç işlev de vardır:

* Bir metin düğümünün yazı tipini değiştirmek için [`gui.set_font()`](/ref/gui/#gui.set_font) işlevini kullanın.
* Bir metin düğümünün satır kaydırma davranışını değiştirmek için [`gui.set_line_break()`](/ref/gui/#gui.set_line_break) işlevini kullanın.
* Bir metin düğümünün içeriğini değiştirmek için [`gui.set_text()`](/ref/gui/#gui.set_text) işlevini kullanın.

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("set_score") then
        local s = gui.get_node("score")
        gui.set_text(s, message.score)
    end
end
```
