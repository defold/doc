---
title: Defold karo kaynağı kılavuzu
brief: Bu kılavuz, karo kaynağının nasıl kullanılacağını ve oluşturulacağını açıklar.
---

# Karo kaynağı {#tile-source}

Bir *karo kaynağı (Tile Source)*, bir [karo haritası bileşeni (Tilemap component)](/manuals/tilemap) tarafından ızgara şeklinde bir alana karolar çizmek için kullanılabilir ya da bir [sprite bileşeninin](/manuals/sprite) veya [parçacık efekti bileşeninin (Particle Effect component)](/manuals/particlefx) grafik kaynağı olarak kullanılabilir. Karo kaynağındaki *çarpışma şekillerini (Collision Shapes)* de bir karo haritasında [çarpışma algılama ve fizik simülasyonu](/manuals/physics) için kullanabilirsiniz ([örnek](/examples/tilemap/collisions/)).

## Karo kaynağı oluşturma {#creating-a-tile-source}

Tüm karoları içeren bir görüntüye ihtiyacınız vardır. Her karo tam olarak aynı boyutlarda olmalı ve bir ızgaraya yerleştirilmelidir. Defold, karolar arasında _aralık_ ve her karonun çevresinde _kenar boşluğu_ kullanımını destekler.

![Karo görüntüsü](images/tilemap/small_map.png)

Kaynak görüntüyü oluşturduktan sonra bir karo kaynağı oluşturabilirsiniz:

- Görüntüyü *Assets* tarayıcısındaki bir proje konumuna sürükleyerek projenize içe aktarın.
- Yeni bir karo kaynağı dosyası oluşturun (*Assets* tarayıcısındaki bir konuma <kbd>sağ tıklayın</kbd>, ardından <kbd>New... ▸ Tile Source</kbd> seçeneğini seçin).
- Yeni dosyaya bir ad verin.
- Dosya artık karo kaynağı düzenleyicisinde açılır.
- *Image* özelliğinin yanındaki göz atma düğmesine tıklayın ve görüntünüzü seçin. Görüntünün artık düzenleyicide gösterilmesi gerekir.
- *Properties* panelindeki özellikleri kaynak görüntüyle eşleşecek şekilde ayarlayın. Her şey doğru olduğunda karolar tam olarak hizalanır.

![Karo kaynağı oluşturma](images/tilemap/tilesource.png)

Size
: Kaynak görüntünün boyutu.

Tile Width
: Her karonun genişliği.

Tile Height
: Her karonun yüksekliği.

Tile Margin
: Her karoyu çevreleyen piksel sayısı (yukarıdaki görüntüde turuncu).

Tile Spacing
: Karoların arasındaki piksel sayısı (yukarıdaki görüntüde mavi).

Inner Padding
: Oyun çalıştırıldığında kullanılan sonuç dokusunda karonun çevresine otomatik olarak kaç boş piksel ekleneceğini belirtir.

Extrude Border
: Oyun çalıştırıldığında kullanılan sonuç dokusunda kenar piksellerinin karonun çevresinde otomatik olarak kaç kez çoğaltılacağını belirtir.

Collision
: Karolar için otomatik olarak çarpışma şekilleri oluşturmakta kullanılacak görüntüyü belirtir.

## Karo kaynağında kare dizisi animasyonları {#tile-source-flip-book-animations}

Bir karo kaynağında animasyon tanımlamak için oynatılacak karoları animasyonun *Frames* özelliğiyle seçin. Karolar tekrarlar dahil herhangi bir sırada bulunabilir; bu nedenle kaynak görüntüyü yeniden düzenlemeniz gerekmez. Yeni oluşturulan tüm karo kaynaklarında "`anim`" adlı varsayılan bir animasyon bulunur. *Outline* görünümünde karo kaynağının kök öğesine <kbd>sağ tıklayıp</kbd> <kbd>Add ▸ Animation</kbd> seçeneğini seçerek yeni animasyonlar ekleyebilirsiniz.

Bir animasyon seçildiğinde animasyonun *Properties* paneli gösterilir.

Id
: Animasyonun kimliği. Karo kaynağı içinde benzersiz olmalıdır.

Frames
: Virgülle ayrılmış, animasyon sırasındaki karo numaraları. Numaralandırma sol üst köşede 1'den başlar ve satır satır sağa doğru ilerleyerek sağ alt köşeye kadar devam eder. Karo numaralarını tekrarlayabilir ve her iki yönde de uçları dahil aralıklar kullanabilirsiniz.

| Frames | Açılmış dizi |
| --- | --- |
| `1, 3, 6, 3` | `1, 3, 6, 3` |
| `1-4, 8` | `1, 2, 3, 4, 8` |
| `4-2` | `4, 3, 2` |

Düzenleyici, en az üç ardışık kareden oluşan dizileri aralık olarak gösterir. Örneğin `1, 2, 3`, `1-3` olurken `1, 2` iki karo numarası olarak kalır. Kare sırası ve tekrarlar korunur. Listede en az bir kare bulunmalı ve her karo numarası kaynak görüntüde var olmalıdır.

*Frames*, *Start Tile* ve *End Tile* yerine geçer. Düzenleyici, eski karo kaynağı dosyalarındaki geçerli aralıkları kare listelerine dönüştürür. Düzenleyici betiklerinde `start_tile` ve `end_tile` yerine `frames` tamsayı dizisini kullanın; [Karo kaynaklarını düzenleme](/manuals/editor-scripts/#editing-tilesources) bölümüne bakın.

Playback
: Animasyonun *Frames* listesi boyunca nasıl oynatılacağını belirtir:

  - `None` animasyonu hiç oynatmaz, ilk görüntü gösterilir.
  - `Once Forward` animasyonu ilk görüntüden son görüntüye kadar bir kez oynatır.
  - `Once Backward` animasyonu son görüntüden ilk görüntüye kadar bir kez oynatır.
  - `Once Ping Pong` animasyonu ilk görüntüden son görüntüye kadar ve ardından tekrar ikinci görüntüye dönerek bir kez oynatır.
  - `Loop Forward` animasyonu ilk görüntüden son görüntüye kadar sürekli tekrarlar.
  - `Loop Backward` animasyonu son görüntüden ilk görüntüye kadar sürekli tekrarlar.
  - `Loop Ping Pong` animasyonu ilk görüntüden son görüntüye kadar ve ardından tekrar ilk görüntüye dönerek sürekli tekrarlar.

Fps
: Animasyonun saniyedeki kare sayısı (FPS) olarak ifade edilen oynatma hızı.

Flip horizontal
: Animasyonu yatay olarak çevirir.

Flip vertical
: Animasyonu dikey olarak çevirir.

## Karo kaynağı çarpışma şekilleri {#tile-source-collision-shapes}

Defold, her karo için _dışbükey_ bir şekil oluşturmak üzere *Collision* özelliğinde belirtilen bir görüntüyü kullanır. Şekil, karonun renk bilgisi içeren, yani %100 saydam olmayan kısmının dış hatlarını izler.

Çarpışmalar için asıl grafikleri içeren görüntüyü kullanmak çoğu zaman mantıklıdır, ancak görsellerden farklı çarpışma şekilleri istiyorsanız ayrı bir görüntü belirtebilirsiniz. Bir çarpışma görüntüsü belirttiğinizde önizleme, oluşturulan çarpışma şekillerini gösteren dış hatları her karo üzerinde gösterecek şekilde güncellenir.

Karo kaynağının *Outline* görünümü, karo kaynağına eklediğiniz çarpışma gruplarını listeler. Yeni karo kaynağı dosyalarına "default" adlı bir çarpışma grubu eklenir. *Outline* görünümünde karo kaynağının kök öğesine <kbd>sağ tıklayıp</kbd> <kbd>Add ▸ Collision Group</kbd> seçeneğini seçerek yeni gruplar ekleyebilirsiniz.

Belirli bir gruba ait olması gereken karo şekillerini seçmek için *Outline* görünümünde grubu seçin, ardından gruba atamak istediğiniz her karoya tıklayın. Karonun ve şeklin dış hatları grubun rengiyle renklendirilir. Renk, düzenleyicide gruba otomatik olarak atanır.

![Çarpışma şekilleri](images/tilemap/collision.png)

Bir karoyu çarpışma grubundan çıkarmak için *Outline* görünümünde karo kaynağının kök öğesini seçin, ardından karoya tıklayın.
