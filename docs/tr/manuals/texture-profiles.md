---
title: Defold'da doku profilleri
brief:  Defold, otomatik doku işlemeyi ve görüntü verilerinin sıkıştırılmasını destekler. Bu kılavuz, kullanılabilen işlevleri açıklar.
---

# Doku profilleri

Defold, otomatik doku (texture) işlemeyi ve görüntü verilerinin sıkıştırılmasını destekler (*atlaslarda (Atlas)*, *karo kaynaklarında (Tile sources)*, *küp haritalarında (Cubemaps)* ve modeller, GUI vb. için kullanılan bağımsız dokularda).

İki sıkıştırma türü vardır: yazılımla görüntü sıkıştırma ve donanımla doku sıkıştırma.

1. Yazılımla sıkıştırma (PNG ve JPEG gibi), görüntü kaynaklarının depolama boyutunu azaltır. Bu da son dağıtım paketinin boyutunu küçültür. Ancak görüntü dosyalarının belleğe okunurken açılması gerekir; bu nedenle bir görüntü diskte küçük olsa bile bellekte çok yer kaplayabilir.

2. Donanımla doku sıkıştırma da görüntü kaynaklarının depolama boyutunu azaltır. Ancak yazılımla sıkıştırmadan farklı olarak, dokuların bellekte kapladığı alanı da azaltır. Bunun nedeni, grafik donanımının sıkıştırılmış dokuları önce açmak zorunda kalmadan doğrudan işleyebilmesidir.

Dokuların işlenmesi, belirli bir doku profili (texture profile) üzerinden yapılandırılır. Bu dosyada, belirli bir platform için dağıtım paketleri oluşturulurken hangi sıkıştırılmış biçimlerin ve türün kullanılması gerektiğini belirten _profiller_ oluşturursunuz. Ardından _profiller_, eşleşen dosya _yol desenleriyle_ ilişkilendirilir; böylece projenizdeki hangi dosyaların sıkıştırılacağını ve bunun tam olarak nasıl yapılacağını ayrıntılı olarak kontrol edebilirsiniz.

Kullanılabilen tüm donanımla doku sıkıştırma yöntemleri kayıplı olduğundan, doku verilerinizde görüntü kusurları oluşur. Bu kusurlar, kaynak malzemenizin görünümüne ve kullanılan sıkıştırma yöntemine büyük ölçüde bağlıdır. En iyi sonuçları elde etmek için kaynak malzemenizi test etmeniz ve denemeler yapmanız önerilir. Burada Google'dan yardım alabilirsiniz.

Dağıtım paketi arşivlerindeki son doku verilerine (sıkıştırılmış veya ham) hangi yazılımla görüntü sıkıştırma yönteminin uygulanacağını seçebilirsiniz. Defold, [Basis Universal](https://github.com/BinomialLLC/basis_universal) ve [ASTC](https://www.khronos.org/opengl/wiki/ASTC_Texture_Compression) sıkıştırma biçimlerini destekler.

::: sidenote
Sıkıştırma, yoğun kaynak kullanan ve zaman alan bir işlemdir. Sıkıştırılacak doku görüntülerinin sayısına, seçilen doku biçimlerine ve yazılımla sıkıştırma türüne bağlı olarak _çok_ uzun proje derleme sürelerine yol açabilir.
:::

### Basis Universal

Basis Universal (kısaca BasisU), görüntüyü bir ara biçime sıkıştırır. Bu biçim, çalışma sırasında geçerli cihazın GPU'suna uygun bir donanım biçimine dönüştürülür. Basis Universal biçimi, yüksek kaliteli ancak kayıplı bir biçimdir.
Oyun arşivinde saklanan dosyaların boyutunu daha da küçültmek için tüm görüntüler ayrıca LZ4 kullanılarak sıkıştırılır.

### ASTC

ASTC, ARM tarafından geliştirilmiş ve Khronos Group tarafından standartlaştırılmış esnek ve verimli bir doku sıkıştırma biçimidir. Çok çeşitli blok boyutları ve bit hızları sunarak geliştiricilerin görüntü kalitesiyle bellek kullanımını etkili biçimde dengelemesini sağlar. ASTC, 4×4 ile 12×12 teksel (texel) arasında değişen çeşitli blok boyutlarını destekler; bunlar teksel başına 8 bitten 0,89 bite kadar değişen bit hızlarına karşılık gelir. Bu esneklik, doku kalitesiyle depolama gereksinimleri arasındaki dengenin ayrıntılı olarak kontrol edilmesini sağlar.

ASTC, 4×4 ile 12×12 teksel arasında değişen çeşitli blok boyutlarını destekler; bunlar teksel başına 8 bitten 0,89 bite kadar değişen bit hızlarına karşılık gelir. Bu esneklik, doku kalitesiyle depolama gereksinimleri arasındaki dengenin ayrıntılı olarak kontrol edilmesini sağlar. Aşağıdaki tabloda desteklenen blok boyutları ve bunlara karşılık gelen bit hızları gösterilmektedir:

| Blok boyutu (genişlik x yükseklik) | Piksel başına bit |
| --------------------------- | -------------- |
| 4x4                         | 8.00           |
| 5x4                         | 6.40           |
| 5x5                         | 5.12           |
| 6x5                         | 4.27           |
| 6x6                         | 3.56           |
| 8x5                         | 3.20           |
| 8x6                         | 2.67           |
| 10x5                        | 2.56           |
| 10x6                        | 2.13           |
| 8x8                         | 2.00           |
| 10x8                        | 1.60           |
| 10x10                       | 1.28           |
| 12x10                       | 1.07           |
| 12x12                       | 0.89           |


#### Desteklenen cihazlar

ASTC çok iyi sonuçlar verse de tüm grafik kartları tarafından desteklenmez. Üreticiye göre desteklenen cihazların kısa bir listesi şöyledir:

| GPU üreticisi         | Destek                                                               |
| ------------------ | --------------------------------------------------------------------- |
| ARM (Mali)         | OpenGL ES 3.2 veya Vulkan desteği olan tüm ARM Mali GPU'ları ASTC'yi destekler.  |
| Qualcomm (Adreno)  | OpenGL ES 3.2 veya Vulkan desteği olan Adreno GPU'ları ASTC'yi destekler.          |
| Apple              | A8 çipinden itibaren Apple GPU'ları ASTC'yi destekler.                            |
| NVIDIA             | ASTC desteği çoğunlukla mobil GPU'lar içindir (ör. Tegra tabanlı çipler).     |
| AMD (Radeon)       | Vulkan desteği olan AMD GPU'ları genellikle ASTC'yi yazılım aracılığıyla destekler.     |
| Intel (tümleşik) | Modern Intel GPU'larında ASTC yazılım aracılığıyla desteklenir.                  |

## Doku profilleri

Her proje, dokuları sıkıştırırken kullanılan yapılandırmayı içeren belirli bir *.texture_profiles* dosyası içerir. Varsayılan olarak bu dosya *builtins/graphics/default.texture_profiles* dosyasıdır ve her doku kaynağını, donanımla doku sıkıştırma kullanmadan RGBA ve varsayılan ZLib dosya sıkıştırmasını kullanan bir profille eşleştiren yapılandırmaya sahiptir.

Doku sıkıştırma eklemek için:

- Yeni bir doku profilleri dosyası oluşturmak için <kbd>File ▸ New...</kbd> seçeneğini seçin ve *Texture Profiles* öğesini seçin. (Alternatif olarak *default.texture_profiles* dosyasını *builtins* dışındaki bir konuma kopyalayın)
- Yeni dosya için bir ad ve konum seçin.
- *game.project* dosyasındaki *texture_profiles* girdisini yeni dosyayı gösterecek şekilde değiştirin.
- *.texture_profiles* dosyasını açın ve gereksinimlerinize göre yapılandırın.

![Yeni profil dosyası](images/texture_profiles/texture_profiles_new_file.png)

![Doku profilini ayarlama](images/texture_profiles/texture_profiles_game_project.png)

Doku profillerinin kullanımını düzenleyici tercihlerinden açıp kapatabilirsiniz. <kbd>File ▸ Preferences...</kbd> seçeneğini seçin. *General* sekmesinde *Enable texture profiles* adlı bir onay kutusu bulunur.

![Doku profili tercihleri](images/texture_profiles/texture_profiles_preferences.png)

## Path Settings

Doku profilleri dosyasının *Path Settings* bölümü, yol desenlerinin bir listesini ve yolla eşleşen kaynaklar işlenirken hangi *profile* değerinin kullanılacağını içerir. Yollar, "Ant Glob" desenleri olarak ifade edilir (ayrıntılar için [belgelere](http://ant.apache.org/manual/dirtasks.html#patterns) bakın). Desenler şu joker karakterlerle ifade edilebilir:

`*`
: Sıfır veya daha fazla karakterle eşleşir. Örneğin `sprite*.png`, *`sprite.png`*, *`sprite1.png`* ve *`sprite_with_a_long_name.png`* dosyalarıyla eşleşir.

`?`
: Tam olarak bir karakterle eşleşir. Örneğin: `sprite?.png`, *sprite1.png* ve *`spriteA.png`* dosyalarıyla eşleşir ancak *`sprite.png`* veya *`sprite_with_a_long_name.png`* ile eşleşmez.

`**`
: Tam bir dizin ağacıyla veya---bir dizinin adı olarak kullanıldığında---sıfır veya daha fazla dizinle eşleşir. Örneğin: `/gui/**`, */gui* dizinindeki ve tüm alt dizinlerindeki bütün dosyalarla eşleşir.

![Yollar](images/texture_profiles/texture_profiles_paths.png)

Bu örnekte iki yol deseni ve bunlara karşılık gelen profiller bulunur.

`/gui/**/*.atlas`
: *`/gui`* dizinindeki veya alt dizinlerinden herhangi birindeki tüm *.atlas* dosyaları "gui_atlas" profiline göre işlenir.

`/**/*.atlas`
: Projenin herhangi bir yerindeki tüm *.atlas* dosyaları "atlas" profiline göre işlenir.

Daha genel yolun en sona yerleştirildiğine dikkat edin. Eşleştirme algoritması yukarıdan aşağıya çalışır. Kaynak yoluyla eşleşen ilk girdi kullanılır. Listenin daha aşağısındaki eşleşen bir yol ifadesi hiçbir zaman ilk eşleşmeyi geçersiz kılmaz. Yollar ters sırada yerleştirilmiş olsaydı, *`/gui`* dizinindekiler dahil her atlas "atlas" profiliyle işlenirdi.

Profil dosyasındaki hiçbir yolla _eşleşmeyen_ doku kaynakları derlenir ve 2'nin en yakın kuvvetine ölçeklenir; bunun dışında değiştirilmeden bırakılır.

## Profiller

Doku profilleri dosyasının *profiles* bölümü, adlandırılmış profillerin bir listesini içerir. Her profil bir veya daha fazla *platforms* öğesi içerir ve her platform bir özellik listesiyle tanımlanır.

![Profiller](images/texture_profiles/texture_profiles_profiles.png)

*Platforms*
: Eşleşen bir platform belirtir. `OS_ID_GENERIC` tüm platformlarla, `OS_ID_WINDOWS` Windows hedefli dağıtım paketleriyle, `OS_ID_IOS` iOS dağıtım paketleriyle eşleşir; diğerleri de aynı şekilde çalışır. `OS_ID_GENERIC` belirtilirse tüm platformlar için dahil edileceğine dikkat edin.

::: important
İki [yol ayarı](#path-settings) aynı dosyayla eşleşirse ve yol farklı platformlara sahip farklı profiller kullanıyorsa **her iki** profil de kullanılır ve **iki** doku oluşturulur.
:::

*Formats*
: Oluşturulacak bir veya daha fazla doku biçimi. Birden fazla biçim belirtilirse her biçim için dokular oluşturulur ve dağıtım paketine dahil edilir. Motor, çalıştığı platformun desteklediği bir biçimdeki dokuları seçer.

*Mipmaps*
: İşaretliyse platform için mipmap yapıları oluşturulur. Varsayılan olarak işaretli değildir.

*Premultiply alpha*
: İşaretliyse doku verileri alfa değeriyle önceden çarpılır. Varsayılan olarak işaretlidir.

*Max Texture Size*
: Sıfırdan farklı bir değere ayarlanırsa dokuların piksel boyutu belirtilen sayıyla sınırlandırılır. Genişliği veya yüksekliği belirtilen değerden büyük olan tüm dokular küçültülür.

Bir profile eklenen her *Formats* öğesi şu özelliklere sahiptir:

*Format*
: Doku kodlanırken kullanılacak biçim. Kullanılabilen tüm doku biçimleri için aşağıya bakın.

*Compressor*
: Doku kodlanırken kullanılacak sıkıştırıcı.

*Compressor Preset*
: Ortaya çıkan sıkıştırılmış görüntüyü kodlamak için kullanılacak sıkıştırma hazır ayarını seçer. Her sıkıştırıcı hazır ayarı sıkıştırıcıya özgüdür ve ayarları sıkıştırıcının kendisine bağlıdır. Bu ayarları basitleştirmek için mevcut sıkıştırma hazır ayarları dört düzeyde sunulur:

| Hazır ayar    | Not                                          |
| --------- | --------------------------------------------- |
| `LOW`     | En hızlı sıkıştırma. Düşük görüntü kalitesi        |
| `MEDIUM`  | Varsayılan sıkıştırma. En iyi görüntü kalitesi       |
| `HIGH`    | En yavaş sıkıştırma. Daha küçük dosya boyutu        |
| `HIGHEST` | Yavaş sıkıştırma. En küçük dosya boyutu          |

`uncompressed` sıkıştırıcısının yalnızca `uncompressed` adlı bir hazır ayarı vardır; bu, dokulara sıkıştırma uygulanmayacağı anlamına gelir.
Kullanılabilen sıkıştırıcıların listesi için [Sıkıştırıcılar](#compressors) bölümüne bakın.

## Doku biçimleri

Grafik donanımı dokuları, farklı kanal sayıları ve bit derinlikleriyle sıkıştırılmamış veya *kayıplı* sıkıştırılmış verilere dönüştürülebilir. Donanımla sıkıştırmanın sabit olması, görüntünün içeriğinden bağımsız olarak ortaya çıkan görüntünün sabit bir boyutta olacağı anlamına gelir. Bu nedenle sıkıştırma sırasındaki kalite kaybı, özgün dokunun içeriğine bağlıdır.

Basis Universal sıkıştırmasının başka bir biçime dönüştürülmesi cihazın GPU yeteneklerine bağlı olduğundan, Basis Universal sıkıştırmasıyla kullanılması önerilen biçimler şu genel biçimlerdir:
`TEXTURE_FORMAT_RGB`, `TEXTURE_FORMAT_RGBA`, `TEXTURE_FORMAT_RGB_16BPP`, `TEXTURE_FORMAT_RGBA_16BPP`, `TEXTURE_FORMAT_LUMINANCE` ve `TEXTURE_FORMAT_LUMINANCE_ALPHA`.

Basis Universal biçim dönüştürücüsü, `ASTC4x4`, `BCx`, `ETC2`, `ETC1` ve `PVRTC1` gibi birçok çıktı biçimini destekler.

Aşağıdaki kayıplı sıkıştırma biçimleri şu anda desteklenmektedir:

| Biçim                            | Sıkıştırma | Ayrıntılar  |
| --------------------------------- | ----------- | -------------------------------- |
| `TEXTURE_FORMAT_RGB`              | yok        | 3 kanallı renk. Alfa atılır |
| `TEXTURE_FORMAT_RGBA`             | yok        | 3 kanallı renk ve tam alfa.    |
| `TEXTURE_FORMAT_RGB_16BPP`        | yok        | 3 kanallı renk. 5+6+5 bit. |
| `TEXTURE_FORMAT_RGBA_16BPP`       | yok        | 3 kanallı renk ve tam alfa. 4+4+4+4 bit. |
| `TEXTURE_FORMAT_LUMINANCE`        | yok        | 1 kanallı gri tonlama, alfa yok. RGB kanalları çarpılarak tek kanala dönüştürülür. Alfa atılır. |
| `TEXTURE_FORMAT_LUMINANCE_ALPHA`  | yok        | 1 kanallı gri tonlama ve tam alfa. RGB kanalları çarpılarak tek kanala dönüştürülür. |

ASTC için kanal sayısı her zaman 4'tür (RGB + alfa) ve blok sıkıştırmasının boyutunu biçimin kendisi belirler.
Bu biçimlerin yalnızca bir ASTC sıkıştırıcısıyla uyumlu olduğunu unutmayın; diğer tüm birleşimler derleme hatasına yol açar.

`TEXTURE_FORMAT_RGBA_ASTC_4X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X4`
`TEXTURE_FORMAT_RGBA_ASTC_5X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X5`
`TEXTURE_FORMAT_RGBA_ASTC_6X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X5`
`TEXTURE_FORMAT_RGBA_ASTC_8X6`
`TEXTURE_FORMAT_RGBA_ASTC_8X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X5`
`TEXTURE_FORMAT_RGBA_ASTC_10X6`
`TEXTURE_FORMAT_RGBA_ASTC_10X8`
`TEXTURE_FORMAT_RGBA_ASTC_10X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X10`
`TEXTURE_FORMAT_RGBA_ASTC_12X12`


## Sıkıştırıcılar {#compressors}

Aşağıdaki doku sıkıştırıcıları varsayılan olarak desteklenir. Doku dosyası belleğe yüklendiğinde verilerin sıkıştırması açılır.

| Ad                              | Biçimler                   | Not                                                                                          |
| --------------------------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| `Uncompressed`                    | Tüm biçimler               | Sıkıştırma uygulanmaz. Varsayılan.                                                      |
| `BasisU`                          | Tüm RGB/RGBA biçimleri      | Basis Universal yüksek kaliteli, kayıplı sıkıştırma. Daha düşük kalite düzeyi, daha küçük boyut sağlar. |
| `ASTC`                            | Tüm ASTC biçimleri          | ASTC kayıplı sıkıştırma. Daha düşük kalite düzeyi, daha küçük boyut sağlar.                          |

::: sidenote
Defold, doku sıkıştırma hattında kurulabilir sıkıştırıcıları destekler. Bu, WEBP veya tamamen özel bir yöntem gibi bir doku sıkıştırma algoritmasının bir eklenti içinde uygulanmasını mümkün kılar.
:::

## Örnek görüntü

Çıktının daha iyi anlaşılması için aşağıda bir örnek verilmiştir.
Görüntü kalitesinin, sıkıştırma süresinin ve sıkıştırılmış boyutun her zaman girdi görüntüsüne bağlı olduğunu ve değişebileceğini unutmayın.

Temel görüntü (1024x512):
![Yeni profil dosyası](images/texture_profiles/kodim03_pow2.png)

### Sıkıştırma süreleri

| Hazır ayar    | Sıkıştırma süresi | Göreli süre |
| --------- | ---------------- | ------------- |
| `LOW`     | 0m0.143s         | 0.5x            |
| `MEDIUM`  | 0m0.294s         | 1.0x            |
| `HIGH`    | 0m1.764s         | 6.0x            |
| `HIGHEST` | 0m1.109s         | 3.8x            |

### Sinyal kaybı

Karşılaştırma, `basisu` aracı kullanılarak (PSNR ölçülerek) yapılır.
100 dB, sinyal kaybı olmadığı anlamına gelir (yani özgün görüntüyle aynıdır).

| Hazır ayar    | Sinyal                                           |
| --------- | ------------------------------------------------ |
| `LOW`     | Max:  34 Mean: 0.470 RMS: 1.088 PSNR: 47.399 dB |
| `MEDIUM`  | Max:  35 Mean: 0.439 RMS: 1.061 PSNR: 47.620 dB |
| `HIGH`    | Max:  37 Mean: 0.898 RMS: 1.606 PSNR: 44.018 dB |
| `HIGHEST` | Max:  51 Mean: 1.298 RMS: 2.478 PSNR: 40.249 dB |

### Sıkıştırılmış dosya boyutları

Özgün dosya boyutu 1572882 bayttır.

| Hazır ayar    | Dosya boyutları | Oran   |
| --------- | ---------- | ------- |
| `LOW`     | 357225     | 22.71 %  |
| `MEDIUM`  | 365548     | 23.24 %  |
| `HIGH`    | 277186     | 17.62 %  |
| `HIGHEST` | 254380     | 16.17 %  |


### Görüntü kalitesi

Ortaya çıkan görüntüler aşağıdadır (`basisu` aracı kullanılarak ASTC kodlamasından elde edilmiştir).

`LOW`
![düşük sıkıştırma hazır ayarı](images/texture_profiles/kodim03_pow2.fast.png)

`MEDIUM`
![orta sıkıştırma hazır ayarı](images/texture_profiles/kodim03_pow2.normal.png)

`HIGH`
![yüksek sıkıştırma hazır ayarı](images/texture_profiles/kodim03_pow2.high.png)

`HIGHEST`
![en iyi sıkıştırma hazır ayarı](images/texture_profiles/kodim03_pow2.best.png)
