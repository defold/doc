---
title: 2B grafikleri içe aktarma ve kullanma
brief: Bu kılavuz, 2B grafiklerin nasıl içe aktarılacağını ve kullanılacağını açıklar.
---

# 2B grafikleri içe aktarma {#importing-2d-graphics}

Defold, 2B oyunlarda sık kullanılan birçok görsel bileşen (component) türünü destekler. Defold ile durağan ve animasyonlu sprite bileşenleri, kullanıcı arayüzü (UI) bileşenleri, parçacık efektleri, karo haritaları ve bit eşlem yazı tipleri oluşturabilirsiniz. Bu görsel bileşenlerden herhangi birini oluşturabilmek için önce kullanmak istediğiniz grafikleri içeren görüntü dosyalarını içe aktarmanız gerekir. Görüntü dosyalarını içe aktarmak için dosyaları bilgisayarınızdaki dosya sisteminden sürükleyip Defold düzenleyicisindeki *Assets panelinde* uygun bir yere bırakmanız yeterlidir.

![Dosyaları içe aktarma](images/graphics/import.png)

::: sidenote
Atlaslar ve karo kaynakları için PNG veya JPEG görüntüleri kullanın. Model dokuları olarak kullanmak üzere KTX2 kaynak dokuları da içe aktarılabilir; aşağıya bakın.
:::


## KTX2 dokuları {#ktx2-textures}

Bağımsız bir *.ktx2* dosyasını *Assets* paneline sürükleyerek içe aktarın, ardından Model bileşeninin materyal doku alanına atayın. [glTF ve GLB modelleri](/manuals/importing-models/#ktx2-textures) de harici KTX2 dosyalarına başvurabilir veya gömülü KTX2 görüntüleri içerebilir. Atlas, karo kaynağı ve küp haritası yüzü girdileri mevcut görüntü biçimlerini kullanmaya devam eder.

Desteklenen KTX2 girdileri, ETC1S/BasisLZ, UASTC, BC7 veya 8 bit R/RG/RGB/RGBA UNORM ya da sRGB verisi kullanan 2B dokulardır. KTX2 dizileri, küp haritaları, hacimler ve HDR dokuları desteklenmez. KTX2, derleme sırasında Defold'un *.texturec* kaynaklarına dönüştürülür; çalışma zamanı KTX2 kapsayıcılarını okumaz.

Kaynak biçimini, boyutlarını, renk uzayını, alfa üst verilerini ve mip düzeylerini incelemek için bir KTX2 varlığını açın. *Outline*, hazırlanmış mip düzeylerini ayrı ayrı seçmenizi sağlar. Doku profili derlenmiş dokuyu yeniden boyutlandırsa veya mipmap kullanımını devre dışı bıraksa bile bunlar kaynak görüntülerini gösterir.

Kaynak biçimini korumakla başka biçimlere dönüştürmek arasında seçim yapmak için [doku profillerini](/manuals/texture-profiles/#ktx2-source-textures) kullanın. Hedef cihazlarınızın desteklediği çıktı biçimlerini seçin. **Keep KTX2 Format** seçeneğinin görüntü işleme sonrasında yeniden kodlama gerektirmesi dahil, zaten kayıplı olan bir kaynağı yeniden sıkıştırmak kaliteyi daha da düşürebilir.


## Defold varlıkları oluşturma {#creating-defold-assets}

Görüntüler Defold'a içe aktarıldıktan sonra Defold'a özgü varlıklar (asset) oluşturmak için kullanılabilir:

![atlas](images/icons/atlas.png){.icon} Atlas
: Atlas, daha büyük bir doku (texture) görüntüsünde otomatik olarak birleştirilen ayrı görüntü dosyalarının bir listesini içerir. Atlaslar durağan görüntüler ve birlikte bir kare dizisi animasyonu (flipbook animation) oluşturan görüntü kümeleri olan animasyon grupları (*Animation Groups*) içerebilir.

  ![atlas](images/graphics/atlas.png)

Atlas kaynağı hakkında daha fazla bilgi için [Atlas kılavuzuna](/manuals/atlas) bakın.

![karo kaynağı](images/icons/tilesource.png){.icon} Karo kaynağı
: Karo kaynağı (tile source), eşit aralıklı bir ızgara üzerinde sıralanmış daha küçük alt görüntülerden oluşacak şekilde önceden hazırlanmış bir görüntü dosyasına başvurur. Bu tür birleşik görüntüler için yaygın olarak kullanılan başka bir terim de _sprite sayfası_ (sprite sheet) ifadesidir. Karo kaynakları, animasyonun ilk ve son karosuyla tanımlanan kare dizisi animasyonları içerebilir. Karolara otomatik olarak çarpışma şekilleri eklemek için bir görüntü kullanmak da mümkündür.

  ![karo kaynağı](images/graphics/tilesource.png)

Karo kaynağı hakkında daha fazla bilgi için [Karo kaynağı kılavuzuna](/manuals/tilesource) bakın.

![bit eşlem yazı tipi](images/icons/font.png){.icon} Bit eşlem yazı tipi
: Bit eşlem yazı tipinin (bitmap font) glifleri (glyph), PNG biçimindeki bir yazı tipi sayfasında bulunur. Bu tür yazı tipleri, TrueType veya OpenType yazı tipi dosyalarından oluşturulan yazı tiplerine göre performans artışı sağlamaz; ancak doğrudan görüntü içinde istenilen grafikleri, renklendirmeleri ve gölgeleri içerebilir.

Bit eşlem yazı tipleri hakkında daha fazla bilgi için [Yazı tipleri kılavuzuna](/manuals/font/#bitmap-bmfonts) bakın.

  ![BMfont](images/font/bm_font.png)


## Defold varlıklarını kullanma {#using-defold-assets}

Görüntüleri Atlas ve Tile Source dosyalarına dönüştürdükten sonra bunları çeşitli görsel bileşen türleri oluşturmak için kullanabilirsiniz:

![sprite](images/icons/sprite.png){.icon}
: Sprite bileşeni, ekranda gösterilen durağan bir görüntü veya kare dizisi animasyonudur.

  ![sprite](images/graphics/sprite.png)

Sprite bileşenleri hakkında daha fazla bilgi için [Sprite kılavuzuna](/manuals/sprite) bakın.

![karo haritası](images/icons/tilemap.png){.icon} Karo haritası
: Karo haritası (tilemap) bileşeni, bir karo kaynağından gelen karoları (görüntü ve çarpışma şekilleri) bir araya getirerek bir harita oluşturur. Karo haritaları atlas kaynaklarını kullanamaz.

  ![karo haritası](images/graphics/tilemap.png)

Karo haritaları hakkında daha fazla bilgi için [Karo haritası kılavuzuna](/manuals/tilemap) bakın.

![parçacık efekti](images/icons/particlefx.png){.icon} Parçacık efekti
: Bir parçacık yayıcısından (emitter) oluşturulan parçacıklar, bir atlas veya karo kaynağındaki durağan bir görüntüden ya da kare dizisi animasyonundan oluşur.

  ![parçacıklar](images/graphics/particles.png)

Parçacık efektleri hakkında daha fazla bilgi için [Parçacık efekti kılavuzuna](/manuals/particlefx) bakın.

![GUI](images/icons/gui.png){.icon} GUI
: GUI kutu düğümleri ve daire dilimi düğümleri, atlaslardaki ve karo kaynaklarındaki durağan görüntüleri ve kare dizisi animasyonlarını kullanabilir.

  ![GUI](images/graphics/gui.png)

GUI hakkında daha fazla bilgi için [GUI kılavuzuna](/manuals/gui) bakın.
