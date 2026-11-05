---
title: Defold'da yazı tipleri kılavuzu
brief: Bu kılavuz, Defold'un yazı tiplerini nasıl kullandığını ve oyunlarınızda yazı tiplerini ekranda nasıl görüntüleyebileceğinizi açıklar.
---

# Yazı tipi dosyaları {#font-files}

Yazı tipleri (font), etiket bileşenlerinde (Label component) ve GUI metin düğümlerinde (GUI text node) metnin görüntüsünü oluşturmak için işleme (rendering) sırasında kullanılır. Defold çeşitli yazı tipi dosya biçimlerini destekler:

- TrueType
- OpenType
- BMFont

Hem eski hem de tam metin yerleşimi motorları, `.ttf` ve `.otf` kaynaklarından çalışma sırasında üretim de dahil olmak üzere TrueType dış hatlarını ve OpenType CFF1/CFF2 dış hatlarını destekler.

Metnin ayrı bölümlerini biçimlendirme, bağlantılar ve satır içi sprite bileşenleriyle çalışma hakkında bilgi için [Zengin metin işaretleme kılavuzuna](/manuals/font-richtext) bakın.

TrueType ve OpenType yazı tiplerinde *Mode* özelliği, gliflerin nasıl işleneceğini seçer:

- **Bitmap**, rasterleştirilmiş glif görüntülerini kullanır.
- **SDF** (işaretli uzaklık alanı), glif kenarlarına olan uzaklıkları bir dokuda saklayarak Bitmap'e göre daha esnek ölçekleme sağlar.
- **Vector**, glif yüzlerini eğri verilerinden işleyerek ölçeklendiklerinde keskin kalmalarını sağlar. Dış çizgi ve gölge efektleri yine bit eşlem verileri kullanır.

Yeni oluşturulan yazı tipi kaynakları **Vector** modunu ve **Dynamic** glif oluşturmayı kullanır. Mevcut yazı tipi kaynakları Bitmap veya SDF modlarını korur. BMFont kaynakları her zaman sağladıkları bit eşlemi kullanır.

Vector modu, `RGBA16F` ve `R32UI` dokuları için grafik desteği gerektirir ve OpenGL ES 2 ya da WebGL 1 üzerinde desteklenmez. Desteklenmeyen grafik bağdaştırıcılarını hedeflerken Bitmap veya SDF yazı tiplerini ve bunlarla eşleşen materyalleri kullanın; Vector'dan SDF'ye otomatik geri dönüş yoktur. Kurulum için [Vektör yazı tipleri](#vector-fonts) bölümüne bakın.

## Çevrimdışı veya çalışma zamanı yazı tipleri {#offline-or-runtime-fonts}

*Glyph Generation* özelliği, her yazı tipinin glif verilerinin ne zaman oluşturulacağını seçer:

- **Static**, seçilen glifleri derleme sırasında (çevrimdışı) oluşturur. *Characters* ve *All Chars*, hangi gliflerin dahil edileceğini kontrol eder. Kaynak `.ttf` veya `.otf` dosyası çalışma sırasında oluşturma için paketlenmez.
- **Dynamic**, kaynak `.ttf` veya `.otf` dosyasını paketler ve glifleri çalışma sırasında gerektikçe oluşturur. *Prewarm Text*, yazı tipi yüklenirken glifleri hazırlar. Diğer glifler daha sonra ihtiyaç duyuldukça oluşturulabilir.

SDF ve Vector yazı tipleri her iki seçeneği de destekler. Bitmap yazı tipleri ve BMFont kaynakları Static oluşturmayı kullanır. Her yazı tipi kaynağı bağımsız yapılandırılır; bu nedenle bir proje Static ve Dynamic yazı tiplerini birlikte kullanabilir.

Dinamik oluşturma, özellikle büyük karakter kümelerine sahip yazı tiplerinde paket boyutunu ve çalışma zamanı bellek kullanımını azaltabilir. Motorda tam metin yerleşim sistemini gerektirir; [Çalışma zamanı yazı tiplerini etkinleştirme](#enabling-runtime-fonts) bölümüne bakın.

## Metin yerleşimi desteği (ör. sağdan sola) {#text-layout-support-eg-right-to-left}

Çalışma zamanı yazı tipleri, sağdan sola gibi tam metin yerleşimlerini destekleme avantajına da sahiptir.
Şu anda [HarfBuzz](https://github.com/harfbuzz/harfbuzz), [SheenBidi](https://github.com/Tehreer/SheenBidi), [libunibreak](https://github.com/adah1972/libunibreak) ve [SkriBidi](https://github.com/memononen/Skribidi) kütüphanelerini kullanıyoruz.

[Çalışma zamanı yazı tiplerini etkinleştirme](/manuals/font#enabling-runtime-fonts) bölümüne bakın.

Düzenleyici, yazı tipi ve sahne metni önizlemeleri için motorun yazı tipi işleyicisini kullanır. Metin şekillendirme ve sağdan sola yerleşim, [çalışma zamanı yazı tiplerini](#enabling-runtime-fonts) ve App Manifest içindeki **Use full text layout system** seçeneğini gerektirir. Çevrimdışı yazı tiplerinde önizleme, yazı tipinin **Characters** ve **All Chars** ayarlarını dikkate alır.

## Yazı tipi koleksiyonu {#font-collection}

`.fontc` dosya biçimi, yazı tipi koleksiyonu (font collection) olarak da bilinir. Çevrimdışı modda bu koleksiyonla yalnızca bir yazı tipi ilişkilendirilir.
Çalışma zamanı yazı tiplerini kullanırken yazı tipi koleksiyonuyla birden fazla yazı tipi dosyasını (`.ttf` veya `.otf`) ilişkilendirebilirsiniz.

Bu, bellek kullanımını düşük tutarken farklı dillerdeki birden fazla metni işlemek için bir yazı tipi koleksiyonu kullanmanızı sağlar.
Örneğin, Japonca yazı tipini içeren bir koleksiyon yükleyebilir, ardından bu yazı tipini geçerli ana yazı tipiyle ilişkilendirebilir ve sonrasında Japonca yazı tipi koleksiyonunu bellekten kaldırabilirsiniz.

## Yazı tipi oluşturma {#creating-a-font}

Defold'da kullanmak üzere bir yazı tipi oluşturmak için menüden <kbd>File ▸ New...</kbd> seçeneğini, ardından <kbd>Font</kbd> seçeneğini seçerek yeni bir yazı tipi dosyası oluşturun. Ayrıca *Assets* tarayıcısında bir konuma <kbd>sağ tıklayıp</kbd> <kbd>New... ▸ Font</kbd> seçeneğini seçebilirsiniz.

![Yeni yazı tipinin adı](images/font/new_font_name.png)

Yeni yazı tipi dosyasına bir ad verin ve <kbd>Ok</kbd> düğmesine tıklayın. Yeni yazı tipi dosyası düzenleyicide açılır.

Kullanmak istediğiniz yazı tipini *Assets* tarayıcısına sürükleyin ve uygun bir konuma bırakın.

*Font* özelliğini yazı tipi dosyasına ayarlayın. `.ttf` veya `.otf` kaynağı için *Mode* ve *Glyph Generation* seçeneklerini seçin, ardından kalan özellikleri gerektiği gibi yapılandırın. Dynamic oluşturma için [çalışma zamanı yazı tipi kurulumunu](#enabling-runtime-fonts) da tamamlayın.

![Vector modu ve Dynamic glif oluşturma seçili yazı tipi özellikleri](images/font/font_properties.png)

Vector yazı tiplerinde görüntülenen metin boyutunu değiştirmek için Label bileşeninin veya GUI metin düğümünün *Font Size* özelliğini kullanın. *Outline/Shadow Bitmap Size*, efekt bit eşlemlerinin çözünürlüğünü görüntülenen metin boyutundan bağımsız olarak kontrol eder.

Bitmap ve SDF yazı tiplerinde oluşturulan glif boyutunu seçmek için yazı tipi kaynağında *Size* ayarını kullanın. BMFont boyutları kaynak `.fnt` dosyasından gelir. Bu yazı tiplerinin görüntülenen boyutunu değiştirmek için Label bileşenini veya GUI metin düğümünü ölçekleyin.

## Özellikler {#properties}

*Font*
: Yazı tipi verilerini üretmek için kullanılacak TTF, OTF veya *`.fnt`* dosyası.

*Material*
: Bu yazı tipini işlerken kullanılacak materyal (material). Yazı tipi moduyla eşleşmelidir; [Yazı tipi materyalleri](#font-materials) bölümüne bakın.

*Mode*
: `.ttf` veya `.otf` kaynağı için işleme tekniği: **Bitmap**, **SDF** veya **Vector**. Eski *Output Format* özelliğinin yerini alır. BMFont kaynaklarında bu özellik gösterilmez.

*Glyph Generation*
: **Static**, glif verilerini derleme sırasında oluşturur. **Dynamic**, çalışma sırasında oluşturur ve [tam metin yerleşim sistemini](#enabling-runtime-fonts) gerektirir. Bu özellik SDF ve Vector yazı tipleri için kullanılabilir. Bitmap modunda Static olarak sabittir; BMFont kaynaklarında gösterilmez.

*Render Mode*
: Oluşturulan Bitmap yazı tiplerinin katman düzeni. Bu özellik yalnızca `.ttf` ve `.otf` kaynaklarında Bitmap modunda gösterilir. SDF, Vector ve BMFont kaynakları için Defold katman düzenini otomatik seçer.

  - **Single Layer**, her karakter için tek bir dörtgen üretir.
  - **Multi Layer**, glif şekli, dış çizgi ve gölge için ayrı dörtgenler üretir. Katmanlar arkadan öne doğru işlenir; bu, dış çizgi glifler arasındaki uzaklıktan geniş olduğunda bir karakterin daha önce işlenmiş karakterleri kapatmasını önler. Ayrıca *Shadow X/Y* özelliklerindeki gölge kaydırmalarını etkinleştirir.

*Size*
: Bitmap veya SDF yazı tipi verileri oluşturulurken kullanılan, piksel cinsinden glif boyutu. BMFont kaynaklarında boyut `.fnt` dosyasından okunur ve burada düzenlenemez.

*Outline/Shadow Bitmap Size*
: Vector modunda *Size* yerine geçer. Hem Static hem de Dynamic oluşturmada etkin dış çizgi ve gölge efektlerinin bit eşlem çözünürlüğünü kontrol eder. Hiçbir efekt etkin değilse glif yüzleri eğri verileri kullandığı için devre dışıdır. Label veya GUI metin düğümünün *Font Size* değerini değiştirmek bu paylaşılan bit eşlem çözünürlüğünü değiştirmez.

*Antialias*
: Bitmap yazı tipi verileri oluşturulurken gliflere kenar yumuşatma uygulanıp uygulanmayacağı. Pikselleri bire bir koruyan işleme için devre dışı bırakın. Bu özellik yalnızca `.ttf` ve `.otf` kaynaklarında Bitmap modunda gösterilir.

*Alpha*
: Glifin saydamlığı. 0.0--1.0 aralığındadır; 0.0 saydam, 1.0 ise opak anlamına gelir.

*Outline Alpha*
: Üretilen dış çizginin saydamlığı. 0.0--1.0.

*Outline Width*
: Üretilen dış çizginin piksel cinsinden genişliği. Dış çizgi olmaması için 0 olarak ayarlayın.

*Shadow Alpha*
: Üretilen gölgenin saydamlığı. 0.0--1.0.

::: sidenote
Yerleşik Bitmap yazı tipi gölgelendiricisi, hem *Single Layer* hem de *Multi Layer* işleme modlarında gölgeleri destekler. *Single Layer* işleme kullanan ve gölgeye ihtiyaç duymayan oluşturulmuş Bitmap yazı tipleri için özel bir materyal `/builtins/fonts/font-singlelayer.fp` kullanabilir. SDF ve Vector yazı tipleri modlarıyla eşleşen gölgelendiriciler gerektirir; [Yazı tipi materyalleri](#font-materials) bölümüne bakın.
:::

*Shadow Blur*
: Oluşturulan gölgeye uygulanan bulanıklık miktarı. Keskin bir gölge için 0 olarak ayarlayın.

*Shadow X/Y*
: Oluşturulan gölgenin piksel cinsinden yatay ve dikey kaydırılması. Oluşturulmuş Bitmap yazı tiplerinde bu kaydırmaları uygulamak için *Multi Layer* işleme modunu kullanın. Defold, SDF ve Vector yazı tipleri için uygun katmanları otomatik seçer.

*Characters*
: Static oluşturma için derlenmiş yazı tipine dahil edilecek karakterler. Varsayılan olarak bu alan yazdırılabilir ASCII karakterlerini (32-126 karakter kodları) içerir. Çalışma sırasında hangi gliflerin kullanılabileceğini kontrol etmek için karakter ekleyin veya kaldırın.

*Prewarm Text*
: Dynamic oluşturmada *Characters* yerine geçer. Metin, yazı tipi yüklenirken glifleri oluşturmak ve önbelleği önceden hazırlamak için kullanılır. Daha sonra hangi karakterlerin oluşturulabileceğini sınırlamaz. Bir betikten [`font.prewarm_text()`](/ref/font/#font.prewarm_text) ile metni önceden hazırlayabilirsiniz.

::: sidenote
Yazdırılabilir ASCII karakterleri şunlardır:
space ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ \` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
:::

*All Chars*
: Static oluşturmada yazı tipini *Characters* ile sınırlamak yerine kaynakta bulunan tüm glifleri dahil eder. Dynamic yazı tiplerinde bu özellik gizlidir.

*Cache Width/Height*
: Bitmap ve SDF yazı tiplerinin ve Vector dış çizgi ve gölge efektlerinin kullandığı glif önbelleği (glyph cache) bit eşleminin boyutunu sınırlar. Motor metni işlerken glifi önbellek bit eşleminde arar. Glif burada yoksa işlenmeden önce önbelleğe eklenir. Önbellek bit eşlemi, motorun işlemesi istenen tüm glifleri barındıramayacak kadar küçükse bir hata bildirilir (`ERROR:RENDER: Out of available cache cells! Consider increasing cache_width or cache_height for the font.`).

  0 olarak ayarlanırsa önbellek boyutu otomatik olarak belirlenir ve en fazla 2048x4096 boyutuna kadar büyür.

## Yazı tipi materyalleri {#font-materials}

Yazı tipi moduyla eşleşen bir materyal kullanın. Yazı tipi kaynağının *Material* özelliği GUI metin düğümleri tarafından kullanılır. Label bileşenlerinin, yazı tipiyle eşleşmesi gereken ayrı bir *Material* özelliği vardır:

| Yazı tipi modu veya kaynağı | GUI metni için yazı tipi materyali | Label bileşeni materyali |
| --- | --- | --- |
| Bitmap | `/builtins/fonts/font.material` | `/builtins/fonts/label.material` |
| SDF | `/builtins/fonts/font-df.material` | `/builtins/fonts/label-df.material` |
| Vector | `/builtins/fonts/font-vector.material` | `/builtins/fonts/label-vector.material` |
| BMFont (`.fnt`) | `/builtins/fonts/font-fnt.material` | `/builtins/fonts/label-fnt.material` |

Yazı tipi düzenleyicisinde *Mode* değiştirmek, bu materyallerden biri zaten atanmışsa ilgili yerleşik Bitmap, SDF ve Vector materyalleri arasında geçiş yapar. Özel materyaller otomatik değiştirilmez. Yazı tipini kullanan Label bileşenlerinin *Material* özelliğini de kontrol edin.

## Vektör yazı tipleri {#vector-fonts}

Vektör yazı tipleri, glif yüzlerini eğrilerden işlediği için görüntülenen metin boyutu değiştiğinde keskin kalır. Gliflerini çalışma sırasında oluşturan bir yazı tipi kurmak için:

1. Örneğin `/fonts/ui.font` adlı bir `.font` kaynağı oluşturun ve *Font* özelliğinde TrueType veya OpenType kaynağı seçin. Normal metin için yerleşik `/builtins/fonts/vera_mo_bd.ttf` kullanılabilir.
2. *Mode* ayarını **Vector**, *Glyph Generation* ayarını **Dynamic**, *Material* ayarını `/builtins/fonts/font-vector.material` yapın. Yeni oluşturulan yazı tipi kaynaklarının varsayılanları bunlardır.
3. Projeye atanmış bir App Manifest içinde **Use full text layout system** seçeneğini etkinleştirin. Özel motoru yapılandırmak için [Çalışma zamanı yazı tiplerini etkinleştirme](#enabling-runtime-fonts) bölümünü izleyin.
4. *game.project* dosyasında [Shader ▸ Exclude GLES 2.0](/manuals/project-settings/#exclude-gles-20) seçeneğini etkinleştirin.
5. Yazı tipini bir [etikete](/manuals/label/) atayın veya GUI sahnesinin *Fonts* listesine ekleyip bir [metin düğümünde](/manuals/gui-text/) seçin. Etiket için bileşenin *Material* özelliğini de `/builtins/fonts/label-vector.material` olarak ayarlayın. Bileşenin veya düğümün *Font Size* değerini istenen görüntüleme boyutuna ayarlayın.

Vektör glif yüzleri eğri dokuları kullanır; ancak etkin dış çizgiler ve gölgeler yine SDF bit eşlem verileri oluşturur ve glif önbelleği doku belleği tüketir. *Outline/Shadow Bitmap Size*, bu bit eşlem çözünürlüğünü Label veya GUI metin düğümünün *Font Size* değerinden bağımsız olarak ayarlar. Bu efektlere ihtiyaç duyulmadığında bit eşlem verilerinin oluşturulmasını önlemek için *Outline Alpha* ve *Shadow Alpha* değerlerini `0` yapın.

### Renkli emoji {#color-emoji}

Vektör yazı tipleri, palet renkleri ile doğrusal ve dairesel renk geçişleri dahil COLRv1 renkli emoji işleyebilir. Bitmap ve SDF modları COLRv1 renklerini işlemez. Yukarıdaki Dynamic Vector kurulumunu kullanın, ardından yazı tipi koleksiyonuna yedek olarak bir COLRv1 emoji yazı tipi ekleyin. Normal metin özgün yazı tipini kullanmaya devam eder.

Örneğin COLRv1 [Noto Color Emoji yazı tipini](https://github.com/google/fonts/blob/main/ofl/notocoloremoji/NotoColorEmoji-Regular.ttf) projenize `/fonts/NotoColorEmoji-Regular.ttf` adıyla kopyalayın. COLRv1 sürümünü seçin: diğer emoji yazı tipleri, dosya adları `.ttf` ile bitse bile farklı bir renk biçimi kullanabilir.

*game.project* dosyasında **Project ▸ Custom Resources** alanına `/fonts/NotoColorEmoji-Regular.ttf` ekleyin. Başka özel kaynak yoksa ayar şöyledir:

```ini
[project]
custom_resources = /fonts/NotoColorEmoji-Regular.ttf
```

Lua içinde yazılmış bir yazı tipi yolu, yazı tipi dosyasının pakete eklenmesini sağlamaz. [Custom Resources](/manuals/project-settings/#custom-resources), bu kaynak yazı tipini kaynak sistemi üzerinden yükleyen [`font.add_font()`](/ref/font/#font.add_font) işlevine sunar. Paketten yüklerken kaynak yazı tipinin dize yolunu verin.

Yedek yazı tipini paylaşılan yazı tipi kaynağı başına bir kez ekleyin. Değişiklik bu yazı tipini kullanan her Label ve GUI metin düğümünü etkiler; aynı yedek yazı tipini iki kez eklemek hata verir. Aynı `.font` ile hem [Label örneğini](/manuals/label/#vector-fonts-and-color-emoji) hem de [GUI örneğini](/manuals/gui-text/#vector-fonts-and-color-emoji) kullanıyorsanız, iki örnekten biri metni önceden hazırlamadan veya göstermeden önce yedek yazı tipinin bir kez eklenmesini sağlayacak şekilde başlangıç işlemlerini düzenleyin. Örnekler, yedek yazı tipini ekledikten sonra metnin tamamını önceden hazırlar ve geri çağırım başarılı olduğunda gösterir.

## Uzaklık alanı yazı tipleri {#distance-field-fonts}

Uzaklık alanı yazı tipleri, dokuda bit eşlem verileri yerine glifin kenarına olan uzaklığı saklar. Motor yazı tipini işlerken uzaklık verilerini yorumlamak ve bunları kullanarak glifi çizmek için özel bir gölgelendirici gerekir. Uzaklık alanı yazı tipleri, bit eşlem yazı tiplerinden daha fazla kaynak tüketir ancak boyutlandırmada daha fazla esneklik sağlar.

![Uzaklık alanı yazı tipi](images/font/df_font.png)

*Mode* alanında **SDF**, *Glyph Generation* alanında **Static** veya **Dynamic** seçin. Yazı tipi için *`/builtins/fonts/font-df.material`*, Label bileşenleri için *`/builtins/fonts/label-df.material`* veya uzaklık alanı verilerini işleyen özel materyaller kullanın.

## Bit eşlem BMFont yazı tipleri {#bitmap-bmfonts}

Defold, üretilen bit eşlemlere ek olarak önceden hazırlanmış bit eşlem "BMFont" biçimindeki yazı tiplerini de destekler. Bu yazı tipleri, tüm glifleri içeren bir PNG yazı tipi sayfasından oluşur. Ayrıca bir *`.fnt`* dosyası, her glifin sayfanın neresinde bulunduğunu, boyutunu ve karakter çifti aralığı (kerning) bilgilerini içerir. (Defold'un, Phaser ve bazı diğer araçların kullandığı *`.fnt`* biçiminin XML sürümünü desteklemediğini unutmayın.)

Bu tür yazı tipleri, TrueType veya OpenType yazı tipi dosyalarından üretilen bit eşlem yazı tiplerine göre performans artışı sağlamaz; ancak doğrudan görüntü içinde istediğiniz grafikleri, renklendirmeleri ve gölgeleri barındırabilir.

Üretilen *`.fnt`* ve *`.png`* dosyalarını Defold projenize ekleyin. Bu dosyalar aynı klasörde bulunmalıdır. Yeni bir yazı tipi dosyası oluşturun ve *Font* özelliğini *`.fnt`* dosyasına ayarlayın. Defold, sağlanan bit eşlemi kullanır ve boyutunu `.fnt` dosyasından okur. BMFont kaynaklarında *Mode* ve *Glyph Generation* gösterilmez.

::: sidenote
BMFont oluşturmak için uygun dosyaları üretebilen bir araç kullanmanız gerekir. Çeşitli seçenekler bulunur:

* [Bitmap Font Generator](http://www.angelcode.com/products/bmfont/), AngelCode tarafından sağlanan, yalnızca Windows'ta çalışan bir araç.
* [Shoebox](http://renderhjs.net/shoebox/), Windows ve macOS için ücretsiz, Adobe Air tabanlı bir uygulama.
* [Hiero](https://libgdx.com/wiki/tools/hiero), açık kaynaklı, Java tabanlı bir araç.
* [Glyph Designer](https://71squared.com/glyphdesigner), 71 Squared tarafından geliştirilen ticari bir macOS aracı.
* [bmGlyph](https://www.bmglyph.com), Sovapps tarafından geliştirilen ticari bir macOS aracı.
:::

![BMfont](images/font/bm_font.png)

Yazı tipinin *Material* özelliğini *`/builtins/fonts/font-fnt.material`* olarak ayarlayın. Label bileşenleri için *`/builtins/fonts/label-fnt.material`* kullanın.

## Görüntü kusurları ve önerilen uygulamalar {#artifacts-and-best-practices}

Genel olarak bit eşlem yazı tipleri, yazı tipi ölçeklenmeden işlendiğinde en iyi sonucu verir. Ekrana işlenmeleri, uzaklık alanı yazı tiplerine göre daha hızlıdır.

Uzaklık alanı yazı tipleri büyütüldüğünde çok iyi sonuç verir. Bit eşlem yazı tipleri ise yalnızca piksellerden oluşan görüntüler olduğundan yazı tipi ölçeklenip büyütüldükçe pikseller de büyür ve bloklu görüntü kusurları oluşur. Aşağıdaki örnekte, 48 piksel boyutundaki bir yazı tipi 4 kat büyütülmüştür.

![Büyütülmüş yazı tipleri](images/font/scale_up.png)

Küçültme sırasında GPU, bit eşlem dokularını iyi bir sonuç verecek şekilde ve verimli olarak küçültebilir ve kenarlarını yumuşatabilir. Bit eşlem yazı tipi, rengini uzaklık alanı yazı tipinden daha iyi korur. Aşağıda, aynı örnek yazı tipinin 48 piksel boyutundan 1/5'ine küçültülmüş halinin yakınlaştırılmış görünümü bulunur:

![Küçültülmüş yazı tipleri](images/font/scale_down.png)

Uzaklık alanı yazı tiplerinin, gliflerin eğrilerini ifade edebilecek uzaklık bilgilerini barındıracak kadar büyük bir hedef boyutta işlenmesi gerekir. Aşağıdaki, yukarıdakiyle aynı yazı tipidir; ancak 18 piksel boyutundadır ve 10 kat büyütülmüştür. Bu boyutun, bu yazı tipinin şekillerini kodlamak için çok küçük olduğu açıktır:

![Uzaklık alanı görüntü kusurları](images/font/df_artifacts.png)

Gölge veya dış çizgi desteği istemiyorsanız bunlara ait alfa değerlerini sıfıra ayarlayın. Aksi takdirde gölge ve dış çizgi verileri yine üretilir ve gereksiz yere bellek tüketir. Vector modunda her iki efekti de devre dışı bırakmak, bit eşlem verilerinin oluşturulmasını önler; glif yüzleri eğri verilerini kullanmaya devam eder.

## Yazı tipi önbelleği {#font-cache}
Bitmap ve SDF yazı tipi kaynakları çalışma sırasında bir glif önbelleği dokusu ve yazı tipi verileri kullanır. Vektör yazı tipleri glif yüzlerini eğri verileri olarak saklar ve etkin dış çizgi ve gölge efektleri için bit eşlem önbelleği kullanır. Aşağıda açıklanan doku düzeni Bitmap ve SDF yazı tipleri için geçerlidir.

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

Çalışma sırasında oluşturma, yazı tipi kaynağı başına yapılandırılır:

1. `.font` kaynağını açın ve TrueType (`.ttf`) veya OpenType (`.otf`) kaynağı seçin.
2. *Mode* ayarını **SDF** veya **Vector**, *Glyph Generation* ayarını **Dynamic** yapın.
3. Eşleşen [yazı tipi ve Label materyallerini](#font-materials) seçin.
4. Bir [App Manifest](/manuals/app-manifest) ekleyin, bunu *game.project* dosyasında *Native Extensions ▸ App Manifest* alanına atayın ve **Use full text layout system** seçeneğini etkinleştirin. Bu, çalışma sırasında yazı tipi oluşturmayı ve tam metin yerleşimini destekleyen özel bir motor derler.
5. *Prewarm Text* alanını, yazı tipi yüklendikten kısa süre sonra gösterilecek metne ayarlayın. Daha sonra gerekecek metin için [`font.prewarm_text()`](/ref/font/#font.prewarm_text) kullanın ve göstermeden önce geri çağırımını bekleyin.

Yeni yazı tipi kaynakları zaten Vector modunu ve Dynamic oluşturmayı kullanır; ancak yine de yukarıdaki App Manifest yapılandırmasını gerektirir.

### Yazı tiplerini betikle yönetme {#font-scripting}

#### Glif önbelleğini önceden hazırlama {#prewarming-glyph-cache}

Dynamic yazı tipleri, yüklendiklerinde *Prewarm Text* için gereken glifleri oluşturur. Alan, yerleşimi yapılacak metin olarak yorumlandığından önbellek, metnin gerektirdiği glifler için hazırlanır. Dynamic yazı tiplerinde *All Chars* kullanılamaz.

Dynamic yazı tipi için `font.prewarm_text(font_collection, text, callback)` çağırabilirsiniz. Geri çağırım, tüm eksik gliflerin önbelleğe eklendiğini ve metni güvenle gösterebileceğinizi bildirir. Bu işlev Static yazı tipleriyle kullanılamaz.

### Yazı tipi koleksiyonuna yazı tipi ekleme ve koleksiyondan kaldırma {#addingremoving-fonts-to-a-font-collection}

Dynamic yazı tiplerinde, bir yazı tipi koleksiyonuna kaynak yazı tipi (`.ttf` veya `.otf`) eklemek veya koleksiyondan kaldırmak mümkündür.
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

### Glifleri önceden hazırlama {#prewarming-glyphs}

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
