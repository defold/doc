---
title: GUI kırpma kılavuzu
brief: Bu kılavuz, şablonla kırpma yoluyla diğer düğümleri maskeleyen GUI düğümlerinin nasıl oluşturulacağını açıklar.
---

# Kırpma

GUI düğümleri (GUI nodes), *kırpma* (clipping) düğümleri olarak kullanılabilir; bunlar, diğer düğümlerin işleme (rendering) sırasında nasıl görüntülendiğini denetleyen maskelerdir. Bu kılavuz, bu özelliğin nasıl çalıştığını açıklar.

## Kırpma düğümü oluşturma

Kutu (Box), metin (Text) ve daire dilimi (Pie) düğümleri kırpma için kullanılabilir. Bir kırpma düğümü oluşturmak için GUI sahnenize bir düğüm ekleyin, ardından özelliklerini buna göre ayarlayın:

Clipping Mode
: Kırpma için kullanılan mod.
  - `None`, düğümü herhangi bir kırpma yapmadan işler.
  - `Stencil`, düğümün geçerli şablon maskesine yazmasını sağlar.

Clipping Visible
: Düğümün içeriğini işlemek için işaretleyin.

Clipping Inverted
: Düğümün şeklinin tersini maskeye yazmak için işaretleyin.

Ardından kırpılmasını istediğiniz düğümleri kırpma düğümüne alt düğüm olarak ekleyin.

![Kırpma oluşturma](images/gui-clipping/create.png)

## Şablon maskesi

Kırpma, düğümlerin bir *şablon arabelleğine* (stencil buffer) yazmasıyla çalışır. Bu arabellek, grafik kartına bir pikselin işlenip işlenmemesi gerektiğini bildiren bilgiler olan kırpma maskelerini içerir.

- Kırpıcı bir üst düğümü olmayan ancak kırpma modu `Stencil` olarak ayarlanmış bir düğüm, şeklini (veya şeklinin tersini) şablon arabelleğinde saklanan yeni bir kırpma maskesine yazar.
- Bir kırpma düğümünün kırpıcı bir üst düğümü varsa bunun yerine üst düğümün kırpma maskesini kırpar. Kırpma yapan bir alt düğüm, geçerli kırpma maskesini hiçbir zaman _genişletemez_; yalnızca daha fazla kırpabilir.
- Kırpıcılara alt düğüm olarak bağlı olan ve kendileri kırpma yapmayan düğümler, üst düğüm hiyerarşisinin oluşturduğu kırpma maskesiyle işlenir.

![Kırpma hiyerarşisi](images/gui-clipping/setup.png)

Burada üç düğüm bir hiyerarşi içinde düzenlenmiştir:

- Altıgen ve kare şekillerin ikisi de şablonla kırpma yapar.
- Altıgen yeni bir kırpma maskesi oluşturur, kare ise bu maskeyi daha fazla kırpar.
- Daire düğümü sıradan bir daire dilimi düğümüdür; bu nedenle kırpma yapan üst düğümlerinin oluşturduğu kırpma maskesiyle işlenir.

Bu hiyerarşi için normal ve ters çevrilmiş kırpıcıların dört birleşimi mümkündür. Yeşil alan, dairenin işlenen bölümünü gösterir. Geri kalanı maskelenir:

![Şablon maskeleri](images/gui-clipping/modes.png)

## Şablon sınırlamaları

- Şablonla kırpma yapan düğümlerin toplam sayısı 256'yı aşamaz.
- _Şablon_ kullanan alt düğümlerin en fazla iç içe geçme derinliği 8 düzeydir. (Yalnızca şablonla kırpma yapan düğümler sayılır.)
- Aynı üst düğüme bağlı şablon düğümlerinin sayısı en fazla 127 olabilir. Şablon hiyerarşisinde aşağıya doğru her düzeyde bu üst sınır yarıya iner.
- Ters çevrilmiş düğümlerin maliyeti daha yüksektir. En fazla 8 ters çevrilmiş kırpma düğümüne izin verilir ve bunların her biri, ters çevrilmemiş kırpma düğümleri için izin verilen en yüksek sayıyı yarıya indirir.
- Şablonlar, şablon maskesini düğümün _geometrisini_ (dokusunu değil) işleyerek oluşturur. *Inverted clipper* özelliği ayarlanarak maske ters çevrilebilir.


## Katmanlar

Katmanlar (layers), düğümlerin işleme sırasını (ve toplu çizimini) denetlemek için kullanılabilir. Katmanlar ve kırpma düğümleri birlikte kullanıldığında olağan katman sırası geçersiz kılınır. Katman sırası her zaman kırpma sırasından önceliklidir---katman atamaları kırpma düğümleriyle birlikte kullanılırsa, kırpması etkin bir üst düğüm alt düğümlerinden daha yüksek bir katmana ait olduğunda kırpma sırası bozulabilir. Katman atanmamış alt düğümler yine hiyerarşiye uyar ve dolayısıyla üst düğümden sonra çizilip kırpılır.

::: sidenote
Bir kırpma düğümü ve hiyerarşisi, düğüme bir katman atanmışsa önce, katman atanmamışsa normal sırada çizilir.
:::

![Katmanlar ve kırpma](images/gui-clipping/layers.png)

Bu örnekte, "`Donut BG`" ve "`BG`" kırpma düğümlerinin ikisi de aynı katmanı, katman 1'i kullanır. Aralarındaki işleme sırası hiyerarşideki sırayla aynı olur; "`Donut BG`", "`BG`" düğümünden önce işlenir. Ancak "`Donut Shadow`" alt düğümü, katman sırası daha yüksek olan katman 2'ye atanmıştır ve bu nedenle her iki kırpma düğümünden sonra işlenir. Bu durumda işleme sırası şöyle olur:

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Burada "`Donut Shadow`" nesnesinin, yalnızca birinin alt düğümü olmasına rağmen, katmanlama nedeniyle her iki kırpma düğümü tarafından kırpılacağını görebilirsiniz.
