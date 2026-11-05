---
title: Varlıkları içe aktarma ve düzenleme
brief: Bu kılavuz, varlıkların nasıl içe aktarılacağını ve düzenleneceğini açıklar.
---

# Varlıkları içe aktarma ve düzenleme {#importing-and-editing-assets}

Bir oyun projesi genellikle grafik, 3B model, ses dosyası, animasyon vb. üretmeye yönelik çeşitli özel programlarda hazırlanmış çok sayıda harici varlıktan (asset) oluşur. Defold, harici araçlarınızda çalışıp varlıklar tamamlandıkça bunları Defold'a içe aktardığınız bir iş akışı için tasarlanmıştır.


## Varlıkları içe aktarma {#importing-assets}

Defold, projenizde kullanılan tüm varlıkların proje hiyerarşisi içinde bir yerde bulunmasını gerektirir. Bu nedenle tüm varlıkları kullanmadan önce içe aktarmanız gerekir. Varlıkları içe aktarmak için dosyaları bilgisayarınızın dosya sisteminden sürükleyip Defold düzenleyicisinin *Assets bölmesinde* uygun bir yere bırakmanız yeterlidir.

![Dosyaları içe aktarma](images/graphics/import.png)

::: sidenote
Atlaslar ve karo kaynakları için PNG veya JPEG görüntüleri kullanın. PNG desteği RGB, RGBA ve indeksli renk (palet) görüntülerini kapsar. Model dokuları olarak kullanmak üzere [KTX2 kaynak dokuları](/manuals/importing-graphics/#ktx2-textures) da içe aktarılabilir.
:::


## Varlıkları kullanma {#using-assets}

Varlıklar Defold'a içe aktarıldıktan sonra Defold'un desteklediği çeşitli bileşen (component) türleri tarafından kullanılabilir:

* Görüntüler, 2B oyunlarda sık kullanılan birçok görsel bileşen türünü oluşturmak için kullanılabilir. [2B grafiklerin nasıl içe aktarılacağı ve kullanılacağı hakkında daha fazla bilgiyi burada bulabilirsiniz](/manuals/importing-graphics).
* Sesler, ses çalmak için [ses bileşeni (Sound)](/manuals/sound) tarafından kullanılabilir.
* Yazı tipleri, [etiket bileşeni (Label)](/manuals/label) ve GUI içindeki [metin düğümleri](/manuals/gui-text) tarafından kullanılır.
* glTF modelleri (*.gltf* ve *.glb*), animasyonlu 3B modelleri göstermek için [Model bileşeni](/manuals/model) tarafından kullanılabilir. Örgülerine, oluşturulan materyallerine ve gömülü görüntülerine göz atmak için bu dosyaları *Assets* panelinde genişletin. Gömülü görüntüler doğrudan kullanılabilir; dışarıdan başvurulan görüntüleri ve arabellekleri ayrı proje dosyaları olarak ekleyin. [Draco ve Meshopt ile sıkıştırılmış geometri](/manuals/importing-models/#compressed-geometry) de desteklenir ve içe aktarma/derleme sırasında çözülür. Model bileşeninde bir sahne veya örgü seçerken düzenleyici, materyal ve doku eşlemelerini doldurmayı önerebilir. Mevcut eşlemelerin yerine bunları uygulamak için <kbd>Auto Fill</kbd>, kendi eşlemelerinizi korumak için <kbd>Keep Current</kbd> seçeneğini seçin. [3B modelleri içe aktarma ve kullanma hakkında daha fazla bilgiyi burada bulabilirsiniz](/manuals/importing-models).


## Harici varlıkları düzenleme {#editing-external-assets}

Defold; görüntüler, ses dosyaları, modeller veya animasyonlar için düzenleme araçları sunmaz. Bu tür varlıkların Defold dışında, özel araçlarla oluşturulması ve Defold'a içe aktarılması gerekir. Defold, proje dosyalarınız arasındaki herhangi bir varlıkta yapılan değişiklikleri otomatik olarak algılar ve düzenleyici görünümünü buna göre günceller.


## Defold varlıklarını düzenleme {#editing-defold-assets}

Düzenleyici, tüm Defold varlıklarını birleştirmeye uygun metin tabanlı dosyalara kaydeder. Bu dosyaları basit betiklerle oluşturmak ve değiştirmek de kolaydır. Daha fazla bilgi için [bu forum konusuna](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) bakın. Ancak zaman zaman değiştiği için dosya biçimimizin ayrıntılarını yayımlamadığımızı unutmayın. Ayrıca varlık oluşturmak veya değiştirmek için betikler çalıştırmak üzere düzenleyicideki belirli yaşam döngüsü olaylarına [düzenleyici betikleri (Editor Scripts)](/manuals/editor-scripts/) aracılığıyla bağlanabilirsiniz.

Defold varlık dosyalarıyla bir metin düzenleyicisi veya harici araç üzerinden çalışırken daha dikkatli olmanız önerilir. Oluşturduğunuz hatalar, dosyanın Defold düzenleyicisinde açılmasını engelleyebilir.

[Tiled](/assets/tiled/) ve [Tilesetter](https://www.tilesetter.org/beta) gibi bazı harici araçlar, Defold varlıklarını otomatik olarak oluşturmak için kullanılabilir.
