---
title: Bir Defold oyununun boyutunu optimize etme
brief: Bu kılavuz, bir Defold oyununun boyutunun nasıl optimize edileceğini açıklar.
---

# Oyun boyutunu optimize etme

Oyununuzun boyutu, web ve mobil gibi platformlarda başarıyı belirleyen kritik bir etken olabilir. Disk alanının ucuz ve genellikle bol olduğu masaüstü ve konsollarda ise daha az önem taşır.

### iOS ve Android
Apple ve Google, uygulamaların Wifi yerine mobil ağlar üzerinden indirilmesi için boyut sınırları belirlemiştir. Android'de bu sınır, [Android App Bundle](https://developer.android.com/guide/app-bundle#size_restrictions) biçiminde yayımlanan uygulamalar için 200 MB'tır. iOS'te uygulama 200 MB'tan büyükse kullanıcılara bir uyarı gösterilir, ancak kullanıcılar yine de indirmeye devam edebilir.

::: sidenote
2017 yılında yapılan bir araştırmada şu sonuç elde edilmiştir: "Bir APK'nın boyutundaki her 6 MB'lık artışta, kurulum dönüşüm oranında %1'lik bir düşüş görüyoruz." ([kaynak](https://medium.com/googleplaydev/shrinking-apks-growing-installs-5d3fcba23ce2))
:::

### HTML5
Poki ve diğer birçok web oyunu platformu, ilk indirme boyutunun 5 MB'tan büyük olmamasını önerir.

Facebook, bir Facebook Instant Game oyununun 5 saniyeden kısa sürede, tercihen 3 saniyeden kısa sürede başlamasını önerir. Bunun uygulama boyutu açısından tam olarak ne anlama geldiği açıkça tanımlanmamıştır, ancak burada 20 MB'a kadar olan boyutlardan söz ediyoruz.

Oynanabilir reklamlar, reklam ağına bağlı olarak genellikle 2 ile 5 MB arasında bir boyutla sınırlıdır.

## Boyut optimizasyonu stratejileri
Uygulama boyutunu iki şekilde optimize edebilirsiniz: motorun boyutunu ve/veya oyun varlıklarının (assets) boyutunu küçülterek.

Uygulamanızın boyutunu hangi öğelerin oluşturduğunu daha iyi anlamak için paketleme sırasında [bir derleme raporu oluşturabilirsiniz](/manuals/bundling/#build-reports). Oyun boyutunun büyük bölümünü seslerin ve grafiklerin oluşturması oldukça yaygındır.

::: important
Defold, uygulamanızı derlerken ve paketlerken bir bağımlılık ağacı oluşturur. Derleme sistemi, *game.project* dosyasında belirtilen başlangıç koleksiyonundan (bootstrap collection) başlayarak başvurulan her koleksiyonu (collection), oyun nesnesini (game object) ve bileşeni (component) inceler ve kullanılan varlıkların bir listesini oluşturur. Son uygulama dağıtım paketine yalnızca bu varlıklar dahil edilir. Doğrudan başvurulmayan her şey dışarıda bırakılır. Kullanılmayan varlıkların dahil edilmeyeceğini bilmek yararlı olsa da geliştirici olarak son uygulamaya nelerin dahil edildiğini, tek tek varlıkların boyutlarını ve uygulama dağıtım paketinin toplam boyutunu yine de göz önünde bulundurmanız gerekir. 
:::

## Motor boyutunu optimize etme
Motor boyutunu küçültmenin hızlı bir yolu, motorda kullanmadığınız işlevleri kaldırmaktır. Bu işlem, ihtiyaç duymadığınız motor bileşenlerini kaldırmanıza olanak tanıyan [uygulama bildirimi dosyasında](https://defold.com/manuals/app-manifest/) yapılır. Örnekler:

* Fizik - Oyununuz Box2D veya Bullet3D fiziğini kullanmıyorsa fizik motorlarını kaldırmanız kuvvetle önerilir
* GUI, parçacık efektleri ve karo haritaları - Bu bileşenler, [App Manifest bileşen anahtarlarıyla](/manuals/app-manifest/#exclude-gui) ayrı ayrı dışarıda bırakılabilir. Dışarıda bıraktığınız her özelliğe ait bileşen başvurularını ve API çağrılarını kaldırın. Parçacık efektlerini dışarıda bırakmak, GUI sahnelerindeki parçacık düğümlerinin desteğini de kaldırır.
* Zengin metin - Etiketlerin ve GUI metinlerinin yalnızca düz metne ihtiyacı varsa [Use Rich Text](/manuals/app-manifest/#use-rich-text) ayarını devre dışı bırakın. Bu işlem, normal metin işlemeyi (rendering) korurken zengin metin ayrıştırmasını ve stil efektlerini kaldırır.
* LiveUpdate - Oyununuz LiveUpdate kullanmıyorsa bu özellik kaldırılabilir
* Görüntü yükleme - Oyununuz `image.load()` kullanarak görüntüleri elle yüklemiyor ve kodlarını çözmüyorsa
* BasisU - Oyununuz az sayıda doku (texture) içeriyorsa BasisU olmadan (uygulama bildirimi üzerinden kaldırılarak) ve doku sıkıştırması kullanılmadan alınan derlemenin boyutunu, BasisU ve sıkıştırılmış dokular kullanılan bir derlemeyle karşılaştırın. Az sayıda doku içeren oyunlarda ikili dosyanın boyutunu küçültmek ve doku sıkıştırmasını atlamak daha yararlı olabilir. Ayrıca dönüştürücüyü kullanmamak, oyununuzu çalıştırmak için gereken bellek miktarını azaltabilir.

## Varlık boyutunu optimize etme
Varlık boyutu optimizasyonunda en büyük kazanımlar genellikle seslerin ve dokuların boyutunu küçülterek elde edilir.

### Sesleri optimize etme
Defold şu biçimleri destekler:
* .wav
* .ogg
* .opus

Defold, 8 bit ve 16 bit PCM Wave dosyalarını destekler. Ogg Vorbis ve Ogg Opus, bir PCM bit derinliği gereksinimi yerine kendi sıkıştırılmış biçimlerini kullanır. Opus kod çözücüsü varsayılan olarak dahil edilmez; `.opus` kaynaklarını (resources) kullanmadan önce [App Manifest](/manuals/app-manifest/#sound) içinde **Include Sound Decoder: Opus** ayarını etkinleştirin.
Ses kod çözücülerimiz, geçerli ses cihazının ihtiyaçlarına göre seslerin örnekleme hızlarını artırır veya azaltır.

Ses efektleri gibi kısa sesler genellikle daha yüksek oranda sıkıştırılırken müzik dosyaları daha az sıkıştırılır.
Defold herhangi bir sıkıştırma yapmaz; bu nedenle geliştiricinin her ses biçimi için sıkıştırmayı ayrıca yapması gerekir.

Sesleri harici bir ses düzenleme yazılımında (veya örneğin [ffmpeg](https://ffmpeg.org) kullanarak komut satırında) düzenleyip kalitelerini düşürebilir veya biçimler arasında dönüştürebilirsiniz. İçeriğin boyutunu daha da küçültmek için sesleri stereodan monoya dönüştürmeyi de değerlendirin.

### Dokuları optimize etme
Oyununuzda kullanılan dokuları optimize etmek için çeşitli seçenekleriniz vardır, ancak önce bir atlasa eklenen veya karo kaynağı (tile source) olarak kullanılan görüntülerin boyutunu kontrol etmelisiniz. Görüntüleri hiçbir zaman oyununuzda gerçekten gerekenden daha büyük boyutta kullanmayın. Büyük görüntüleri içe aktarıp uygun boyuta küçültmek, doku belleğini boşa harcar ve bundan kaçınılması önerilir. Öncelikle harici bir görüntü düzenleme yazılımı kullanarak görüntülerin boyutunu oyununuzda gereken gerçek boyuta ayarlayın. Arka plan görüntüleri gibi öğelerde küçük bir görüntü kullanıp istenen boyuta büyütmek de uygun olabilir. Görüntüleri doğru boyuta küçültüp atlaslara ekledikten veya karo kaynaklarında kullanmaya başladıktan sonra atlasların kendi boyutlarını da göz önünde bulundurmanız gerekir. Kullanılabilecek en büyük atlas boyutu, platforma ve grafik donanımına göre değişir.

::: sidenote
[Bu forum gönderisi](https://forum.defold.com/t/texture-management-in-defold/8921/17?u=britzl), betikler veya üçüncü taraf yazılımlar kullanarak birden fazla görüntüyü yeniden boyutlandırmaya yönelik çeşitli ipuçları sunar.
:::

* HTML5'te [Web3D Survey projesine](https://web3dsurvey.com/webgl/parameters/MAX_TEXTURE_SIZE) bildirilen en büyük doku boyutu
* iOS'te en büyük doku boyutu:
  * iPad: 2048x2048
  * iPhone 4: 2048x2048
  * iPad 2, 3, Mini, Air, Pro: 4096x4096
  * iPhone 4s, 5, 6+, 6s: 4096x4096
* Android'de en büyük doku boyutu büyük ölçüde değişir, ancak genel olarak nispeten yeni tüm cihazlar en az 4096x4096 boyutunu destekler.

Bir atlas çok büyükse onu birkaç küçük atlasa bölmeniz, çok sayfalı atlaslar kullanmanız veya bir doku profili (texture profile) kullanarak atlasın tamamını ölçeklemeniz gerekir. Defold'un doku profili sistemi, atlasların tamamını ölçeklemenin yanı sıra atlasın diskteki boyutunu küçültmek için sıkıştırma algoritmaları uygulamanıza da olanak tanır. [Kılavuzda doku profilleri hakkında daha fazla bilgi edinebilirsiniz](/manuals/texture-profiles/). Ne kullanacağınızı bilmiyorsanız daha sonra yapacağınız özelleştirmeler için başlangıç noktası olarak şu ayarları deneyin:

* mipmaps: false
* premultiply_alpha: true
* format: TEXTURE_FORMAT_RGBA
* compression_level: NORMAL
* compression_type: COMPRESSION_TYPE_BASIS_UASTC

::: sidenote
Dokuları optimize etme ve yönetme hakkında daha fazla bilgiyi [bu forum gönderisinde](https://forum.defold.com/t/texture-management-in-defold/8921) bulabilirsiniz.
:::

### Yazı tiplerini optimize etme
Kullanacağınız simgeleri belirleyip All Chars onay kutusunu kullanmak yerine bunları [Characters](/manuals/font/#properties) alanında belirtirseniz yazı tiplerinizin boyutu daha küçük olur.

### Gerektiğinde indirmek üzere içeriği dışarıda bırakma
Uygulamanın başlangıç boyutunu küçültmenin bir başka yolu, oyun içeriğinin bazı bölümlerini uygulama dağıtım paketinin dışında bırakıp gerektiğinde indirmektir. Defold, gerektiğinde indirmek üzere içeriği dışarıda bırakmak için Live Update adlı bir sistem sunar.

Dışarıda bırakılan içerik, bölümlerin tamamından kilidi açılabilen karakterlere, görünümlere, silahlara veya araçlara kadar her şey olabilir. Oyununuz çok fazla içerik barındırıyorsa yükleme sürecini, başlangıç koleksiyonu ve ilk bölümün koleksiyonu yalnızca o bölüm için gereken asgari kaynakları içerecek şekilde düzenleyin. Bunu, "Exclude" onay kutusu etkinleştirilmiş koleksiyon vekilleri (collection proxy) veya fabrikalar (factory) kullanarak yapabilirsiniz. Kaynakları oyuncunun ilerlemesine göre ayırın. Bu yaklaşım, kaynakların verimli yüklenmesini sağlar ve başlangıçtaki bellek kullanımını düşük tutar. Daha fazla bilgi için [Live Update kılavuzuna](/manuals/live-update/) bakın.

## Android'e özgü boyut optimizasyonları
Android derlemeleri hem 32 bit hem de 64 bit CPU mimarilerini desteklemelidir. [Android için dağıtım paketi oluştururken](/manuals/android) hangi CPU mimarilerinin dahil edileceğini belirtebilirsiniz:

![Android dağıtım paketini imzalama](images/android/sign_bundle.png)

Varsayılan olarak bir dağıtım paketi `armv7-android` ve `arm64-android` mimarilerini içerir. Üçüncü bir mimari olan `x86_64-android` de kullanılabilir, ancak fiziksel cihazlardan çok Android emülatörleri, ChromeOS ve Windows Subsystem for Android için yararlı olduğundan varsayılan olarak dahil edilmez. Özellikle bu ortamlardan birini hedeflemeniz gerekmiyorsa dağıtım paketinin boyutunu düşük tutmak için bu seçeneği işaretlemeyin.

Google Play, bir oyunun her sürümü için [birden fazla APK'yı](https://developer.android.com/google/play/publishing/multiple-apks) destekler. Bu sayede her CPU mimarisi için bir tane olmak üzere iki APK oluşturup ikisini de Google Play'e yükleyerek uygulama boyutunu küçültebilirsiniz.

[APK genişletme dosyalarını](https://developer.android.com/google/play/expansion-files) ve [Live Update içeriğini](/manuals/live-update), [Asset Portal'daki APKX uzantısı](https://defold.com/assets/apkx/) sayesinde birlikte de kullanabilirsiniz.
