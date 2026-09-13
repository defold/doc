---
title: GUI şablonları kılavuzu
brief: Bu kılavuz, ortak şablonları veya 'prefab' yapılarını temel alan, yeniden kullanılabilir görsel GUI bileşenleri oluşturmak için kullanılan Defold GUI şablon sistemini açıklar.
---

# GUI şablon düğümleri

GUI şablon düğümleri (GUI template nodes), ortak şablonları veya "prefab" adı verilen hazır tanımları temel alan, yeniden kullanılabilir GUI bileşenleri (GUI components) oluşturmak için güçlü bir mekanizma sunar. Bu kılavuz, bu özelliği ve nasıl kullanılacağını açıklar.

GUI şablonu (GUI template), başka bir GUI sahnesinde (GUI scene) her düğümünün bir örneği (instance) oluşturulan bir GUI sahnesidir. Özgün şablon düğümlerindeki tüm özellik değerleri daha sonra geçersiz kılınabilir.

## Şablon oluşturma

GUI şablonu sıradan bir GUI sahnesidir, bu nedenle diğer GUI sahneleri gibi oluşturulur. *Assets* bölmesindeki bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Gui</kbd> seçeneğini seçin.

![Şablon oluşturma](images/gui-templates/create.png)

Şablonu oluşturun ve kaydedin. Örneğin düğümlerinin başlangıç noktasına göre yerleştirileceğini unutmayın; bu nedenle şablonu 0, 0, 0 konumunda oluşturmanız iyi olur.

## Şablondan örnekler oluşturma

Örneği temel alarak istediğiniz sayıda örnek oluşturabilirsiniz. Şablonu yerleştirmek istediğiniz GUI sahnesini oluşturun veya açın, ardından *Outline* görünümündeki *Nodes* bölümüne <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Template</kbd> seçeneğini seçin.

![Örnek oluşturma](images/gui-templates/create_instance.png)

*Template* özelliğini şablon GUI sahnesi dosyasına ayarlayın.

İstediğiniz sayıda şablon örneği ekleyebilir ve her örnekteki her düğümün özelliklerini geçersiz kılarak örnek düğümünün konumunu, rengini, boyutunu, dokusunu ve benzer özelliklerini değiştirebilirsiniz.

![Örnekler](images/gui-templates/instances.png)

Değiştirdiğiniz her özellik düzenleyicide maviyle işaretlenir. Değerini şablondaki değere döndürmek için özelliğin yanındaki sıfırlama düğmesine basın:

![Properties](images/gui-templates/properties.png)

Özellikleri geçersiz kılınmış tüm düğümler de *Outline* görünümünde mavi renkte gösterilir:

![Outline](images/gui-templates/outline.png)

Şablon örneği, *Outline* görünümünde daraltılabilir bir öğe olarak listelenir. Ancak bu görünümdeki öğenin *bir düğüm olmadığını* unutmamak önemlidir. Şablon örneği çalışma sırasında da var olmaz, ancak örneğin parçası olan tüm düğümler var olur.

Şablon örneğinin parçası olan düğümler, *Id* değerlerine bir önek ve eğik çizgi (`"/"`) eklenerek otomatik olarak adlandırılır. Önek, şablon örneğinde ayarlanan *Id* değeridir.

## Şablonları çalışma sırasında değiştirme

Şablon mekanizmasıyla eklenen düğümleri değiştiren veya sorgulayan betiklerin yalnızca örnek düğümlerinin adlandırılmasını dikkate alması ve şablon örneğinin *Id* değerini düğüm adı öneki olarak eklemesi gerekir:

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Do something...
end
```

Şablon örneğinin kendisine karşılık gelen bir düğüm yoktur. Bir örnek için kök düğüme ihtiyacınız varsa bunu şablona ekleyin.

Bir betik şablon GUI sahnesiyle ilişkilendirilmişse bu betik, örneğin düğüm ağacının parçası olmaz. Her GUI sahnesine yalnızca tek bir betik bağlayabilirsiniz; dolayısıyla betik mantığınızın, şablonlarınızın örneklerini oluşturduğunuz GUI sahnesinde bulunması gerekir.
