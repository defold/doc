---
title: Defold'da yazı tipleri kılavuzu
brief: Bu kılavuz, Defold'un yazı tiplerini nasıl kullandığını ve oyunlarınızda yazı tiplerini ekranda nasıl görüntüleyebileceğinizi açıklar.
---

# Yazı tipi dosyaları

Yazı tipleri (font), etiket bileşenlerinde (Label component) ve GUI metin düğümlerinde (GUI text node) metnin görüntüsünü oluşturmak için işleme (rendering) sırasında kullanılır. Defold çeşitli yazı tipi dosya biçimlerini destekler:

- TrueType
- OpenType
- BMFont

Defold 1.13.2'den itibaren hem eski hem de tam metin yerleşimi motorları, `.ttf` ve `.otf` kaynaklarından çalışma sırasında üretim de dahil olmak üzere TrueType dış hatlarını ve OpenType CFF1/CFF2 dış hatlarını destekler.

Metnin ayrı bölümlerini biçimlendirme, bağlantılar ve satır içi sprite bileşenleriyle çalışma hakkında bilgi için [Zengin metin işaretleme kılavuzuna](/manuals/font-richtext) bakın.

Projenize eklenen yazı tipleri, Defold'un işleyebileceği bir doku (texture) biçimine otomatik olarak dönüştürülür. Her birinin kendine özgü avantajları ve dezavantajları olan iki yazı tipi işleme tekniği bulunur:

- Bit eşlem (Bitmap)
- Uzaklık alanı (Distance field)

## Çevrimdışı veya çalışma zamanı yazı tipleri

Varsayılan olarak, rasterleştirilmiş glif (glyph) görüntülerine dönüştürme işlemi proje derlenirken (çevrimdışı) gerçekleşir. Bunun dezavantajı, her yazı tipinin olası tüm gliflerinin derleme aşamasında rasterleştirilmesi gerekmesidir. Bu işlem, bellek tüketen ve dağıtım paketinin boyutunu da artıran çok büyük dokular üretebilir.

"Çalışma zamanı yazı tipleri" (runtime fonts) kullanıldığında, `.ttf` ve `.otf` yazı tipleri olduğu gibi paketlenir ve rasterleştirme çalışma sırasında ihtiyaç duyuldukça gerçekleşir. Bu, hem çalışma zamanındaki bellek kullanımını hem de dağıtım paketinin boyutunu en aza indirir.

## Metin yerleşimi desteği (ör. sağdan sola) {#text-layout-support-eg-right-to-left}

Çalışma zamanı yazı tipleri, sağdan sola gibi tam metin yerleşimlerini destekleme avantajına da sahiptir.
Şu anda [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) ve [SkriBidi](https://github.com/memononen/Skribidi) kütüphanelerini kullanıyoruz.

[Çalışma zamanı yazı tiplerini etkinleştirme](/manuals/font#enabling-runtime-fonts) bölümüne bakın.

Düzenleyici, yazı tipi ve sahne metni önizlemeleri için motorun yazı tipi işleyicisini kullanır. Metin şekillendirme ve sağdan sola yerleşim, [çalışma zamanı yazı tiplerini](#enabling-runtime-fonts) ve App Manifest içindeki **Use full text layout system** seçeneğini gerektirir. Çevrimdışı yazı tiplerinde önizleme, yazı tipinin **Characters** ve **All Chars** ayarlarını dikkate alır.

## Yazı tipi koleksiyonu

`.fontc` dosya biçimi, yazı tipi koleksiyonu (font collection) olarak da bilinir. Çevrimdışı modda bu koleksiyonla yalnızca bir yazı tipi ilişkilendirilir.
Çalışma zamanı yazı tiplerini kullanırken yazı tipi koleksiyonuyla birden fazla yazı tipi dosyasını (`.ttf` veya `.otf`) ilişkilendirebilirsiniz.

Bu, bellek kullanımını düşük tutarken farklı dillerdeki birden fazla metni işlemek için bir yazı tipi koleksiyonu kullanmanızı sağlar.
Örneğin, Japonca yazı tipini içeren bir koleksiyon yükleyebilir, ardından bu yazı tipini geçerli ana yazı tipiyle ilişkilendirebilir ve sonrasında Japonca yazı tipi koleksiyonunu bellekten kaldırabilirsiniz.

## Yazı tipi oluşturma

Defold'da kullanmak üzere bir yazı tipi oluşturmak için menüden <kbd>File ▸ New...</kbd> seçeneğini, ardından <kbd>Font</kbd> seçeneğini seçerek yeni bir yazı tipi dosyası oluşturun. Ayrıca *Assets* tarayıcısında bir konuma <kbd>sağ tıklayıp</kbd> <kbd>New... ▸ Font</kbd> seçeneğini seçebilirsiniz.

![Yeni yazı tipinin adı](images/font/new_font_name.png)

Yeni yazı tipi dosyasına bir ad verin ve <kbd>Ok</kbd> düğmesine tıklayın. Yeni yazı tipi dosyası düzenleyicide açılır.

![Yeni yazı tipi](images/font/new_font.png)

Kullanmak istediğiniz yazı tipini *Assets* tarayıcısına sürükleyin ve uygun bir konuma bırakın.

*Font* özelliğini yazı tipi dosyasına ayarlayın ve yazı tipi özelliklerini gerektiği gibi düzenleyin.

## Özellikler {#properties}

*Font*
: Yazı tipi verilerini üretmek için kullanılacak TTF, OTF veya *`.fnt`* dosyası.

*Material*
: Bu yazı tipini işlerken kullanılacak materyal (material). Uzaklık alanı yazı tipleri ve BMFont yazı tipleri için bu özelliği değiştirdiğinizden emin olun (ayrıntılar için aşağıya bakın).

*Output Format*
: Üretilen yazı tipi verilerinin türü.

  - `TYPE_BITMAP`, içe aktarılan OTF veya TTF dosyasını, metin düğümlerini işlemek için bit eşlem verilerinin kullanıldığı bir yazı tipi sayfası dokusuna dönüştürür. Renk kanalları; glifin ana şeklini, dış çizgisini ve düşen gölgesini kodlamak için kullanılır. *`.fnt`* dosyalarında kaynak dokunun bit eşlemi olduğu gibi kullanılır.
  - `TYPE_DISTANCE_FIELD` İçe aktarılan yazı tipi, piksel verilerinin ekran pikselleri yerine yazı tipinin kenarına olan uzaklıkları temsil ettiği bir yazı tipi sayfası dokusuna dönüştürülür. Ayrıntılar için aşağıya bakın.

*Render Mode*
: Glifleri işlemek için kullanılacak işleme modu.

  - `MODE_SINGLE_LAYER`, her karakter için tek bir dörtgen üretir.
  - `MODE_MULTI_LAYER`, sırasıyla glifin şekli, dış çizgisi ve gölgeleri için ayrı dörtgenler üretir. Katmanlar arkadan öne doğru işlenir. Böylece dış çizgi, glifler arasındaki mesafeden daha geniş olduğunda bir karakterin önceden işlenmiş karakterleri kapatması önlenir. Bu işleme modu, yazı tipi kaynağındaki Shadow X/Y özelliklerinde belirtildiği gibi düşen gölgenin doğru şekilde kaydırılmasını da sağlar.

*Size*
: Gliflerin piksel cinsinden hedef boyutu.

*Antialias*
: Yazı tipi hedef bit eşleme dönüştürülürken kenar yumuşatma uygulanıp uygulanmayacağı. Yazı tipinin pikselleri bire bir korunarak işlenmesini istiyorsanız 0 olarak ayarlayın.

*Alpha*
: Glifin saydamlığı. 0.0--1.0 aralığındadır; 0.0 saydam, 1.0 ise opak anlamına gelir.

*Outline Alpha*
: Üretilen dış çizginin saydamlığı. 0.0--1.0.

*Outline Width*
: Üretilen dış çizginin piksel cinsinden genişliği. Dış çizgi olmaması için 0 olarak ayarlayın.

*Shadow Alpha*
: Üretilen gölgenin saydamlığı. 0.0--1.0.

::: sidenote
Gölge desteği, yerleşik yazı tipi materyali gölgelendiricileri (shader) tarafından sağlanır ve hem tek hem de çok katmanlı işleme modunu destekler. Katmanlı yazı tipi işlemeye veya gölge desteğine ihtiyacınız yoksa *`builtins/font-singlelayer.fp`* gibi daha basit bir gölgelendirici kullanmanız önerilir.
:::

*Shadow Blur*
: Bit eşlem yazı tiplerinde bu ayar, her yazı tipi glifine küçük bir bulanıklaştırma çekirdeğinin kaç kez uygulanacağını belirtir. Uzaklık alanı yazı tiplerinde ise bu ayar, bulanıklığın piksel cinsinden gerçek genişliğine eşittir.

*Shadow X/Y*
: Üretilen gölgenin piksel cinsinden yatay ve dikey kaydırılması. Bu ayar, glif gölgesini yalnızca Render Mode değeri `MODE_MULTI_LAYER` olarak ayarlandığında etkiler.

*Characters*
: Yazı tipine dahil edilecek karakterler. Varsayılan olarak bu alan, yazdırılabilir ASCII karakterlerini (32-126 karakter kodları) içerir. Yazı tipine daha fazla veya daha az karakter dahil etmek için bu alana karakter ekleyebilir veya alandan karakter kaldırabilirsiniz.

Çalışma zamanı yazı tiplerinde bu metin, önbelleği uygun gliflerle önceden hazırlamak için kullanılır. Bu işlem yükleme sırasında gerçekleşir. `font.prewarm_text()` işlevine bakın.

::: sidenote
Yazdırılabilir ASCII karakterleri şunlardır:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Bu özelliği işaretlerseniz kaynak dosyada bulunan tüm glifler çıktıya dahil edilir.

*Cache Width/Height*
: Glif önbelleği (glyph cache) bit eşleminin boyutunu sınırlar. Motor metni işlerken glifi önbellek bit eşleminde arar. Glif burada yoksa işlenmeden önce önbelleğe eklenir. Önbellek bit eşlemi, motorun işlemesi istenen tüm glifleri barındıramayacak kadar küçükse bir hata bildirilir (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  0 olarak ayarlanırsa önbellek boyutu otomatik olarak belirlenir ve en fazla 2048x4096 boyutuna kadar büyür.

## Uzaklık alanı yazı tipleri

Uzaklık alanı yazı tipleri, dokuda bit eşlem verileri yerine glifin kenarına olan uzaklığı saklar. Motor yazı tipini işlerken uzaklık verilerini yorumlamak ve bunları kullanarak glifi çizmek için özel bir gölgelendirici gerekir. Uzaklık alanı yazı tipleri, bit eşlem yazı tiplerinden daha fazla kaynak tüketir ancak boyutlandırmada daha fazla esneklik sağlar.

![Uzaklık alanı yazı tipi](images/font/df_font.png)

Yazı tipini oluştururken *Material* özelliğini *`builtins/fonts/font-df.material`* (veya uzaklık alanı verilerini işleyebilen başka bir materyal) olarak değiştirdiğinizden emin olun; aksi takdirde yazı tipi ekranda işlenirken doğru gölgelendirici kullanılmaz.

## Bit eşlem BMFont yazı tipleri {#bitmap-bmfonts}

Defold, üretilen bit eşlemlere ek olarak önceden hazırlanmış bit eşlem "BMFont" biçimindeki yazı tiplerini de destekler. Bu yazı tipleri, tüm glifleri içeren bir PNG yazı tipi sayfasından oluşur. Ayrıca bir *`.fnt`* dosyası, her glifin sayfanın neresinde bulunduğunu, boyutunu ve karakter çifti aralığı (kerning) bilgilerini içerir. (Defold'un, Phaser ve bazı diğer araçların kullandığı *`.fnt`* biçiminin XML sürümünü desteklemediğini unutmayın.)

Bu tür yazı tipleri, TrueType veya OpenType yazı tipi dosyalarından üretilen bit eşlem yazı tiplerine göre performans artışı sağlamaz; ancak doğrudan görüntü içinde istediğiniz grafikleri, renklendirmeleri ve gölgeleri barındırabilir.

Üretilen *`.fnt`* ve *`.png`* dosyalarını Defold projenize ekleyin. Bu dosyalar aynı klasörde bulunmalıdır. Yeni bir yazı tipi dosyası oluşturun ve *font* özelliğini *`.fnt`* dosyasına ayarlayın. *output_format* değerinin `TYPE_BITMAP` olarak ayarlandığından emin olun. Defold bir bit eşlem üretmez; PNG'de sağlanan bit eşlemi kullanır.

::: sidenote
BMFont oluşturmak için uygun dosyaları üretebilen bir araç kullanmanız gerekir. Çeşitli seçenekler bulunur:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), AngelCode tarafından sağlanan, yalnızca Windows'ta çalışan bir araç.
* [Shoebox](http://renderhjs.net/shoebox/), Windows ve macOS için ücretsiz, Adobe Air tabanlı bir uygulama.
* [Hiero](https://libgdx.com/wiki/tools/hiero), açık kaynaklı, Java tabanlı bir araç.
* [Glyph Designer](https://71squared.com/glyphdesigner), 71 Squared tarafından geliştirilen ticari bir macOS aracı.
* [bmGlyph](https://www.bmglyph.com), Sovapps tarafından geliştirilen ticari bir macOS aracı.
:::

![BMfont](images/font/bm_font.png)

Yazı tipinin doğru işlenmesi için yazı tipini oluştururken materyal özelliğini *`builtins/fonts/font-fnt.material`* olarak ayarlamayı unutmayın.

## Görüntü kusurları ve önerilen uygulamalar

Genel olarak bit eşlem yazı tipleri, yazı tipi ölçeklenmeden işlendiğinde en iyi sonucu verir. Ekrana işlenmeleri, uzaklık alanı yazı tiplerine göre daha hızlıdır.

Uzaklık alanı yazı tipleri büyütüldüğünde çok iyi sonuç verir. Bit eşlem yazı tipleri ise yalnızca piksellerden oluşan görüntüler olduğundan yazı tipi ölçeklenip büyütüldükçe pikseller de büyür ve bloklu görüntü kusurları oluşur. Aşağıdaki örnekte, 48 piksel boyutundaki bir yazı tipi 4 kat büyütülmüştür.

![Büyütülmüş yazı tipleri](images/font/scale_up.png)

Küçültme sırasında GPU, bit eşlem dokularını iyi bir sonuç verecek şekilde ve verimli olarak küçültebilir ve kenarlarını yumuşatabilir. Bit eşlem yazı tipi, rengini uzaklık alanı yazı tipinden daha iyi korur. Aşağıda, aynı örnek yazı tipinin 48 piksel boyutundan 1/5'ine küçültülmüş halinin yakınlaştırılmış görünümü bulunur:

![Küçültülmüş yazı tipleri](images/font/scale_down.png)

Uzaklık alanı yazı tiplerinin, gliflerin eğrilerini ifade edebilecek uzaklık bilgilerini barındıracak kadar büyük bir hedef boyutta işlenmesi gerekir. Aşağıdaki, yukarıdakiyle aynı yazı tipidir; ancak 18 piksel boyutundadır ve 10 kat büyütülmüştür. Bu boyutun, bu yazı tipinin şekillerini kodlamak için çok küçük olduğu açıktır:

![Uzaklık alanı görüntü kusurları](images/font/df_artifacts.png)

Gölge veya dış çizgi desteği istemiyorsanız bunlara ait alfa değerlerini sıfıra ayarlayın. Aksi takdirde gölge ve dış çizgi verileri yine üretilir ve gereksiz yere bellek tüketir.

## Yazı tipi önbelleği
Defold'daki bir yazı tipi kaynağı, çalışma sırasında iki şey oluşturur: bir doku ve yazı tipi verileri.

* Yazı tipi verileri, her biri temel karakter çifti aralığı bilgileri ve ilgili glifin bit eşlem verilerini içeren glif kayıtlarının listesinden oluşur.
* Doku, motor içinde "glif önbelleği dokusu" olarak adlandırılır ve belirli bir yazı tipindeki metni işlerken kullanılır.

Çalışma sırasında metin işlenirken motor, hangi gliflerin doku önbelleğinde bulunduğunu kontrol etmek için önce işlenecek glifler üzerinde dolaşır. Glif doku önbelleğinde bulunmayan her glif, yazı tipi verilerinde saklanan bit eşlem verilerinden dokuya aktarım yapılmasını tetikler.

Her glif, önbelleğe yazı tipinin taban çizgisine göre yerleştirilir. Bu, bir gölgelendiricide glifin karşılık gelen önbellek hücresi içindeki yerel doku koordinatlarının hesaplanmasını sağlar. Böylece renk geçişleri veya doku kaplamaları gibi belirli metin efektlerini dinamik olarak elde edebilirsiniz. Motor, önbellekle ilgili ölçüleri gölgelendiriciye `texture_size_recip` adlı özel bir gölgelendirici sabiti aracılığıyla sunar. Bu sabitin vektör bileşenleri aşağıdaki bilgileri içerir:

* `texture_size_recip.x`, önbellek genişliğinin çarpmaya göre tersidir
* `texture_size_recip.y`, önbellek yüksekliğinin çarpmaya göre tersidir
* `texture_size_recip.z`, önbellek hücresi genişliğinin önbellek genişliğine oranıdır
* `texture_size_recip.w`, önbellek hücresi yüksekliğinin önbellek yüksekliğine oranıdır

Örneğin, bir gölgelendirici parçasında renk geçişi oluşturmak için şunu yazmanız yeterlidir:

`float horizontal_gradient = fract(var_texcoord0.y / texture_size_recip.w);`

Gölgelendirici uniform parametreleri hakkında daha fazla bilgi için [Gölgelendirici kılavuzuna](/manuals/shader) bakın.

## Çalışma zamanı yazı tiplerini etkinleştirme {#enabling-runtime-fonts}

TrueType (`.ttf`) veya OpenType (`.otf`) yazı tipleri kullanıldığında, SDF türündeki yazı tipleri için çalışma sırasında üretim kullanılabilir. `.otf` kaynaklarından çalışma sırasında üretim, Defold 1.13.2'den itibaren desteklenir.
Bu yaklaşım, bir Defold oyununun indirme boyutunu ve çalışma zamanındaki bellek tüketimini önemli ölçüde azaltabilir.
Küçük dezavantajı, her glifin üretiminin eşzamansız olmasıdır.

* Özelliği etkinleştirmek için game.project dosyasında `font.runtime_generation` ayarını yapın.

* Bir [App Manifest](/manuals/app-manifest) ekleyin ve `Use full text layout system` seçeneğini etkinleştirin.
Bu işlem, söz konusu özelliğin etkin olduğu özel bir motor derler.

::: sidenote
Bu özellik şu anda deneyseldir, ancak gelecekte varsayılan iş akışı olarak kullanılması amaçlanmaktadır.
:::

::: important
`font.runtime_generation` ayarı, projedeki tüm `.ttf` ve `.otf` yazı tiplerini etkiler.
:::


### Yazı tiplerini betikle yönetme

#### Glif önbelleğini önceden hazırlama

Çalışma zamanı yazı tiplerinin kullanımını kolaylaştırmak için glif önbelleğinin önceden hazırlanması desteklenir.
Bu, yazı tipinin *Characters* alanında listelenen gliflerin üretileceği anlamına gelir.

::: sidenote
`All Chars` seçiliyse önceden hazırlama yapılmaz; çünkü bu, tüm glifleri aynı anda üretmek zorunda kalmama amacına aykırıdır.
:::

`Characters` alanı `.fontc` dosyasında ayarlanmışsa glif önbelleğinde hangi gliflerin güncellenmesi gerektiğini belirlemek için bu alan metin olarak kullanılır.

`font.prewarm_text(font_collection, text, callback)` çağrısıyla glif önbelleğini elle güncellemek de mümkündür. Bu işlev, eksik gliflerin tümü glif önbelleğine eklendiğinde ve metni ekranda güvenle gösterebileceğinizde size haber vermek için bir geri çağırım (callback) sağlar.

### Yazı tipi koleksiyonuna yazı tipi ekleme ve koleksiyondan kaldırma

Çalışma zamanı yazı tiplerinde, bir yazı tipi koleksiyonuna yazı tipi (`.ttf`) eklemek veya koleksiyondan kaldırmak mümkündür.
Bu, büyük bir yazı tipi farklı karakter kümeleri (ör. CJK) için birden fazla dosyaya bölündüğünde kullanışlıdır.

::: important
Bir yazı tipi koleksiyonuna yazı tipi eklemek, tüm glifleri otomatik olarak yüklemez veya işlemez.
:::

```lua
function init(self)
    -- Get the target font collection.
    self.font_collection = go.get("#label", "font")

    -- Get the first font assigned to the selected language collection.
    local language_collection = go.get("localization_japanese#label", "font")
    local font_info = font.get_info(language_collection)
    self.language_ttf_hash = font_info.fonts[1].path_hash

    -- Associate it with the target collection and increase its reference count.
    font.add_font(self.font_collection, self.language_ttf_hash)
end
```

```lua
function final(self)
    -- Remove the association and release the font reference.
    font.remove_font(self.font_collection, self.language_ttf_hash)
end
```

### Glifleri önceden hazırlama

Çalışma zamanı yazı tipiyle bir metni düzgün gösterebilmek için gliflerin çözümlenmesi gerekir. `font.prewarm_text()` işlevi bunu sizin için yapar.
Bu işlem eşzamansızdır. İşlem tamamlanıp geri çağırım alındığında, söz konusu glifleri içeren herhangi bir iletiyi güvenle gösterebilirsiniz.

::: important
Glif önbelleği dolarsa önbellekteki en eski glif çıkarılır.
:::

```lua
font.prewarm_text(self.font_collection, info.text, function (self, request_id, result, err)
    if result then
      print("PREWARMING OK!")
      go.set(self.label, "text", info.text)
    else
      print("Error prewarming text:", err)
    end
  end)
```
