---
title: Oyun nesnesi bileşenleri
brief: Bu kılavuz, bileşenlere ve bunların nasıl kullanılacağına genel bir bakış sunar.
---

#  Bileşenler

:[components](../shared/components.md)

## Bileşen türleri

Defold aşağıdaki bileşen (component) türlerini destekler:

* [Koleksiyon fabrikası (collection factory)](/manuals/collection-factory) - Koleksiyonları (collection) çalışma sırasında oluşturma
* [Koleksiyon vekili (collection proxy)](/manuals/collection-proxy) - Koleksiyonları yükleme ve bellekten kaldırma
* [Çarpışma nesnesi](/manuals/physics) - 2B ve 3B fizik
* [Kamera](/manuals/camera) - Oyun dünyasının görüntü alanını ve izdüşümünü değiştirme
* [Fabrika (factory)](/manuals/factory) - Oyun nesnelerini (game object) çalışma sırasında oluşturma
* [GUI](/manuals/gui) - Grafik kullanıcı arayüzü işleme (rendering)
* [Etiket](/manuals/label) - Bir metin parçasını işleme
* [Işık](/manuals/light) - Gölgelendiriciler için ışık verisi ekleme
* [Örgü](/manuals/mesh) 3B örgü gösterme (çalışma sırasında oluşturma ve değiştirme desteğiyle)
* [Model](/manuals/model) 3B model gösterme (isteğe bağlı animasyonlarla)
* [Parçacık efekti](/manuals/particlefx) -  Parçacıkları çalışma sırasında oluşturma
* [Betik](/manuals/script) - Oyun mantığı ekleme
* [Ses](/manuals/sound) - Ses veya müzik çalma
* [Sprite bileşeni](/manuals/sprite) - 2B görüntü gösterme (isteğe bağlı kare dizisi animasyonuyla)
* [Karo haritası](/manuals/tilemap) - Karolardan oluşan bir ızgara gösterme

Eklentiler aracılığıyla başka bileşenler eklenebilir:

* [Rive modeli](/extension-rive) - Rive animasyonu işleme
* [Spine modeli](/extension-spine) - Spine animasyonu işleme


## Bileşenleri etkinleştirme ve devre dışı bırakma

Bir oyun nesnesinin bileşenleri, oyun nesnesi oluşturulduğunda etkinleştirilir. Bir bileşeni devre dışı bırakmak istiyorsanız bunu bileşene bir [`disable`](/ref/go/#disable) iletisi göndererek yapabilirsiniz:

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

Bir bileşeni yeniden etkinleştirmek için bileşene bir [`enable`](/ref/go/#enable) iletisi gönderebilirsiniz:

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## Bileşen özellikleri

Defold bileşen türlerinin her biri farklı özelliklere sahiptir. Düzenleyicideki [Properties paneli](/manuals/editor/#the-editor-views), [Outline panelinde](/manuals/editor/#the-editor-views) o anda seçili olan bileşenin özelliklerini gösterir. Kullanılabilir bileşen özellikleri hakkında daha fazla bilgi edinmek için ilgili bileşen türlerinin kılavuzlarına bakın.

## Bileşen konumu, dönmesi ve ölçeği

Görsel bileşenlerin genellikle konum ve dönme özellikleri, çoğu zaman da ölçek özelliği vardır. Bu özellikler düzenleyiciden değiştirilebilir ve hemen hemen hiçbir durumda çalışma sırasında değiştirilemez (tek istisna, çalışma sırasında değiştirilebilen sprite ve etiket bileşenlerinin ölçeğidir).

Bir bileşenin konumunu, dönmesini veya ölçeğini çalışma sırasında değiştirmeniz gerekiyorsa bunun yerine bileşenin ait olduğu oyun nesnesinin konumunu, dönmesini veya ölçeğini değiştirin. Bunun bir yan etkisi olarak oyun nesnesindeki tüm bileşenler etkilenir. Bir oyun nesnesine bağlı birçok bileşenden yalnızca birini değiştirmek istiyorsanız söz konusu bileşeni ayrı bir oyun nesnesine taşımanız ve bu nesneyi, bileşenin başlangıçta ait olduğu oyun nesnesine alt nesne olarak eklemeniz önerilir.

## Bileşen çizim sırası

Görsel bileşenlerin çizim sırası iki şeye bağlıdır:

### İşleme betiği yüklemleri
Her bileşene bir [materyal (material)](/manuals/material/) atanır ve her materyalin bir veya daha fazla etiketi vardır. İşleme betiği (render script) ise her biri bir veya daha fazla materyal etiketiyle eşleşen bir dizi işleme yüklemi (render predicate) tanımlar. İşleme betiğinin *update()* işlevinde [yüklemler tek tek çizilir](/manuals/render/#render-predicates) ve her yüklemde tanımlanan etiketlerle eşleşen bileşenler çizilir. Varsayılan işleme betiği önce sprite bileşenlerini ve karo haritalarını bir geçişte, ardından parçacık efektlerini başka bir geçişte çizer; her iki geçiş de dünya uzayında gerçekleşir. İşleme betiği daha sonra GUI bileşenlerini ekran uzayında ayrı bir geçişte çizmeye devam eder.

### Bileşen z değeri
Tüm oyun nesneleri ve bileşenler, konumları `vector3` nesneleriyle ifade edilen 3B uzayda yer alır. Oyununuzun grafik içeriğini 2B olarak görüntülediğinizde X ve Y değerleri bir nesnenin "genişlik" ve "yükseklik" eksenlerindeki konumunu, Z konumu ise "derinlik" eksenindeki konumunu belirler. Z konumu, üst üste gelen nesnelerin görünürlüğünü kontrol etmenizi sağlar: Z değeri 1 olan bir sprite bileşeni, Z konumu 0 olan bir sprite bileşeninin önünde görünür. Defold varsayılan olarak -1 ile 1 arasındaki Z değerlerine izin veren bir koordinat sistemi kullanır:

![model](images/graphics/z-order.png)

Bir [işleme yüklemiyle](/manuals/render/#render-predicates) eşleşen bileşenler birlikte çizilir ve çizilme sıraları bileşenin son z değerine bağlıdır. Bir bileşenin son z değeri, bileşenin kendisinin, ait olduğu oyun nesnesinin ve varsa tüm üst oyun nesnelerinin z değerlerinin toplamıdır.

::: sidenote
Birden fazla GUI bileşeninin çizilme sırası, GUI bileşenlerinin z değeriyle **belirlenmez**. GUI bileşenlerinin çizim sırası [gui.set_render_order()](/ref/gui/#gui.set_render_order:order) işleviyle kontrol edilir.
:::

Örnek: A ve B adlı iki oyun nesnesi. B, A'nın alt nesnesidir. B'nin bir sprite bileşeni vardır.

| Öğe      | Z değeri |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

Yukarıdaki hiyerarşide, B üzerindeki sprite bileşeninin son z değeri 2 + 1 + 0.5 = 3.5 olur.

::: important
İki bileşenin z değeri tam olarak aynıysa sıralama tanımsızdır; bileşenler sırayla birbirinin önüne geçerek titreyebilir veya bir platformda bir sırayla, başka bir platformda farklı bir sırayla işlenebilir.

İşleme betiği, z değerleri için bir yakın düzlem ve bir uzak düzlem tanımlar. Z değeri bu aralığın dışında kalan bileşenler işlenmez. Varsayılan aralık -1 ile 1 arasındadır, ancak [kolayca değiştirilebilir](/manuals/render/#default-view-projection). Yakın ve uzak sınırları -1 ve 1 olduğunda Z değerlerinin sayısal hassasiyeti çok yüksektir. 3B varlıklarla çalışırken varsayılan izdüşümün yakın ve uzak sınırlarını özel bir işleme betiğinde değiştirmeniz gerekebilir. Daha fazla bilgi için [İşleme kılavuzuna](/manuals/render/) bakın.
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
