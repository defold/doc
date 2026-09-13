---
title: Defold proje ayarları
brief: Bu kılavuz, Defold'da projeye özgü ayarların nasıl çalıştığını açıklar.
---

# Proje ayarları

*game.project* dosyası, proje genelindeki tüm ayarları içerir. Bu dosya projenin kök klasöründe kalmalı ve adı *game.project* olmalıdır. Motor, başlatılıp oyununuzu çalıştırırken ilk olarak bu dosyayı arar.

Dosyadaki her ayar bir kategoriye aittir. Dosyayı açtığınızda Defold, tüm ayarları kategorilere göre gruplandırarak gösterir.

![Proje ayarları](images/project-settings/settings.jpg)


## Dosya biçimi

*game.project* içindeki ayarlar genellikle Defold içinden değiştirilir; ancak dosya, herhangi bir standart metin düzenleyicisinde de düzenlenebilir. Dosya, INI dosya biçimi standardına uyar ve şu şekilde görünür:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Gerçek bir örnek:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

Bu, *main_collection* ayarının *bootstrap* kategorisine ait olduğu anlamına gelir. Yukarıdaki örnekte olduğu gibi bir dosya başvurusu kullanıldığında yolun sonuna 'c' karakteri eklenmelidir; bu, dosyanın derlenmiş sürümüne başvurduğunuz anlamına gelir. Ayrıca *game.project* dosyasını içeren klasörün proje kökü olacağını unutmayın; ayar yolunun başında '/' bulunmasının nedeni budur.


## Çalışma sırasında erişim {#runtime-access}

Çalışma sırasında *game.project* içindeki değerleri [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) ve [`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean) işlevleriyle okuyabilirsiniz. Örnekler:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
Anahtar, kategori adıyla ayar adının bir noktayla ayrılarak birleştirilmesinden oluşur; tüm harfler küçük yazılır ve boşluk karakterleri alt çizgilerle değiştirilir. Örnekler: "Project" kategorisindeki "Title" alanı `project.title`, "Physics" kategorisindeki "Gravity Y" alanı ise `physics.gravity_y` olur.
:::


## Bölümler ve ayarlar

Kullanılabilir tüm ayarlar aşağıda kategorilere göre sıralanmıştır.

### Project

#### Title
Uygulamanın başlığı.

#### Version
Uygulamanın sürümü.

#### Publisher
Yayımcının adı.

#### Developer
Geliştiricinin adı.

#### Write Log File
Motorun ne zaman günlük dosyası yazacağını belirler. Seçenekler:

- "Never": Günlük dosyası yazılmaz.
- "Debug": Yalnızca Debug derlemeleri için günlük dosyası yazılır.
- "Always": Hem Debug hem de Release derlemeleri için günlük dosyası yazılır.

Düzenleyiciden birden fazla örnek (instance) çalıştırılıyorsa dosyanın adı *instance_2_log.txt* olur; buradaki `2`, örnek indeksidir. Tek bir örnek çalıştırılıyorsa veya uygulama dağıtım paketinden (bundle) çalıştırılıyorsa dosyanın adı *log.txt* olur. Günlük dosyasının konumu aşağıdaki yollardan biri olacaktır (sırayla denenir):

1. *project.log_dir* içinde belirtilen yol (gizli ayar)
2. Sistem günlük yolu:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Diğerleri: Uygulama kökü
3. Uygulama destek yolu
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (ör. `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: `HOME` ortam değişkeni

#### Minimum Log Level
Günlüğe kaydetme sistemi için en düşük günlük düzeyini belirtin. Yalnızca bu düzeydeki veya daha üst düzeylerdeki günlük kayıtları gösterilir.

#### Compress Archive
Paketleme sırasında arşivlerin sıkıştırılmasını etkinleştirir. Bunun şu anda, apk dosyasının tüm verileri zaten sıkıştırılmış olarak içerdiği Android dışındaki tüm platformlar için geçerli olduğunu unutmayın.

#### Dependencies
Projenin *Library URL* adreslerinin listesi. Daha fazla bilgi için [Kütüphaneler kılavuzuna](/manuals/libraries/) bakın.

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

Özel kaynakların (custom resource) yüklenmesi, [Dosya erişimi kılavuzunda](/manuals/file-access/#how-to-access-files-bundled-with-the-application) daha ayrıntılı açıklanır.

Eklentilerin `custom_resources.default` üzerinden `ext.properties` dosyasında sağladığı yollar, bu ayarla birleştirilir. Bir örnek için [eklentilerin özel kaynaklarına](/manuals/extensions/#custom-resources) bakın.

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

Dağıtım paketine eklenen kaynakların yüklenmesi, [Dosya erişimi kılavuzunda](/manuals/file-access/#how-to-access-files-bundled-with-the-application) daha ayrıntılı açıklanır.

#### Bundle Exclude Resources
`bundle_exclude_resources`
Dağıtım paketine dahil edilmemesi gereken kaynakların virgülle ayrılmış listesi. Başka bir deyişle bu kaynaklar, `bundle_resources` adımında toplanan kaynaklardan çıkarılır.

---

### Bootstrap

#### Main Collection
Uygulamayı başlatmak için kullanılacak koleksiyonun (collection) dosya başvurusu; varsayılan olarak `/logic/main.collection`.

#### Render
Görüntü oluşturma hattını tanımlayan işleme (rendering) yapılandırma dosyası; varsayılan olarak `/builtins/render/default.render`.

---

### Library

#### Include Dirs
Projenizden kütüphane paylaşımı yoluyla paylaşılacak dizinlerin boşlukla ayrılmış listesi. Daha fazla bilgi için [Kütüphaneler kılavuzuna](/manuals/libraries/) bakın.

---

### Script

#### Shared State
Tüm betik türleri arasında tek bir Lua durumu paylaşmak için işaretleyin.

---

### Engine

#### Run While Iconified
Uygulama penceresi simge durumuna küçültüldüğünde motorun çalışmaya devam etmesine izin verir (yalnızca masaüstü platformları).

#### Fixed Update Frequency
`fixed_update(self, dt)` yaşam döngüsü işlevinin Hertz cinsinden güncelleme sıklığı.

#### Max Time Step
Tek bir kare sırasında zaman adımı çok büyürse bu en yüksek değerle sınırlandırılır. Saniye cinsindendir.

---

### Display

#### Width
Uygulama penceresinin piksel cinsinden genişliği.

#### Height
Uygulama penceresinin piksel cinsinden yüksekliği.

#### High Dpi
Destekleyen ekranlarda yüksek DPI değerine sahip bir arka arabellek oluşturur. Oyun genellikle *Width* ve *Height* ayarlarında belirtilenin iki katı çözünürlükte işlenir; bu ayarlardaki değerler, betiklerde ve özelliklerde kullanılan mantıksal çözünürlük olarak kalır.

#### Samples
Süper örneklemeli kenar yumuşatma için kullanılacak örnek sayısı. `GLFW_FSAA_SAMPLES` pencere ipucunu ayarlar. `0` değeri, kenar yumuşatmanın kapalı olduğu anlamına gelir.

Bu ayar pencereyi denetler. Ekran dışı [çok örneklemeli işleme hedeflerinin](/manuals/render/#multisampled-render-targets) kendi örnek sayıları vardır.

#### Fullscreen
Uygulamanın tam ekran başlaması için işaretleyin. İşaretli değilse uygulama pencerede çalışır.

#### Update Frequency
Hertz cinsinden istenen kare hızı. Değişken kare hızı için 0 olarak ayarlayın. 0'dan büyük bir değer, çalışma sırasında gerçek kare hızına göre sınırlanan sabit bir kare hızı sağlar (yani oyun döngüsünü bir motor karesinde iki kez güncelleyemezsiniz). Bu değeri çalışma sırasında değiştirmek için [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) işlevini kullanın. Bu ayar, grafik arayüzü olmadan çalışan derlemelerde de geçerlidir.

#### Swap interval
Bu tam sayı değeri, uygulamanın dikey eşitlemeyi (vsync) nasıl kullanacağını belirler. 0, dikey eşitlemeyi devre dışı bırakır; varsayılan değer 1'dir. OpenGL bağdaştırıcısı kullanılırken bu değer, pencerenin [arabellek takasları arasında güncelleneceği](https://www.khronos.org/opengl/wiki/Swap_Interval) kare sayısını belirler. Vulkan'da yerleşik bir takas aralığı kavramı olmadığından bu değer, dikey eşitlemenin etkinleştirilip etkinleştirilmeyeceğini belirler.

#### Vsync
Eski sürümlerle uyumluluk ayarı. Bu ayarın kullanımı artık önerilmez; yeni projelerde **Swap Interval** kullanın. Devre dışı bırakılırsa geçerli takas aralığını `0` yapar. Etkinleştirilirse geçerli değeri **Swap Interval** belirler.

#### Display Profiles
Kullanılacak ekran profilleri dosyasını belirtir; varsayılan olarak `/builtins/render/default.display_profilesc`. Daha fazla bilgi için [GUI yerleşimleri kılavuzuna](/manuals/gui-layouts/#creating-display-profiles) bakın.

#### Dynamic Orientation
Cihaz döndürüldüğünde uygulamanın dikey ve yatay yönelimler arasında dinamik olarak geçiş yapması için işaretleyin. Geliştirme uygulamasının şu anda bu ayarı dikkate almadığını unutmayın.

#### Display Device Info
Başlangıçta GPU bilgilerini konsola yazdırır.

---

### Render

#### Clear Color Red
İşleme betiğinde (render script) ve pencere oluşturulurken kullanılan temizleme renginin kırmızı kanalı.

#### Clear Color Green
İşleme betiğinde ve pencere oluşturulurken kullanılan temizleme renginin yeşil kanalı.

#### Clear Color Blue
İşleme betiğinde ve pencere oluşturulurken kullanılan temizleme renginin mavi kanalı.

#### Clear Color Alpha
İşleme betiğinde ve pencere oluşturulurken kullanılan temizleme renginin alfa kanalı.

---

### Font

#### Runtime Generation
Çalışma sırasında yazı tipi oluşturmayı kullanır.

---

### Physics

#### Max Collision Object Count
En fazla çarpışma nesnesi (collision object) sayısı.

#### Type
Kullanılacak fizik türü: `2D` veya `3D`.

#### Gravity X
Dünyanın x eksenindeki yer çekimi. Saniyede metre cinsindendir.

#### Gravity Y
Dünyanın y eksenindeki yer çekimi. Saniyede metre cinsindendir.

#### Gravity Z
Dünyanın z eksenindeki yer çekimi. Saniyede metre cinsindendir.

#### Debug
Fiziğin hata ayıklama amacıyla görselleştirilmesi için işaretleyin.

#### Debug Alpha
Görselleştirilen fiziğin alfa bileşeni değeri, `0`--`1`.

#### World Count
Aynı anda var olabilecek en fazla fizik dünyası sayısı; varsayılan olarak `4`. Koleksiyon vekilleri (collection proxy) aracılığıyla aynı anda 4'ten fazla dünya yüklüyorsanız bu değeri artırmanız gerekir. Her fizik dünyasının kayda değer miktarda bellek ayırdığını unutmayın.

#### Scale
Fizik motoruna, sayısal hassasiyet için fizik dünyalarını oyun dünyasına göre nasıl ölçekleyeceğini bildirir; `0.01`--`1.0`. Değer `0.02` olarak ayarlanırsa fizik motoru 50 birimi 1 metre olarak kabul eder ($1 / 0.02$).

#### Allow Dynamic Transforms
Fizik motorunun bir oyun nesnesinin (game object) dönüşümünü, nesneye bağlı tüm çarpışma nesnesi bileşenlerine (component) uygulaması için işaretleyin. Bu, dinamik olanlar dahil çarpışma şekillerini taşımak, ölçeklemek ve döndürmek için kullanılabilir.

#### Use Fixed Timestep
Fizik motorunun sabit ve kare hızından bağımsız güncellemeler kullanması için işaretleyin. Fizik motoruyla düzenli aralıklarla etkileşime girmek için bu ayarı, `fixed_update(self, dt)` yaşam döngüsü işlevi ve `engine.fixed_update_frequency` proje ayarıyla birlikte kullanın. Yeni projeler için önerilen ayar `true` değeridir.

#### Debug Scale
Fizikte eksen üçlüleri ve normaller gibi birim nesnelerin ne büyüklükte çizileceği.

#### Max Collisions
Betiklere bildirilecek çarpışma sayısı.

#### Max Contacts
Betiklere bildirilecek temas noktası sayısı.

#### Contact Impulse Limit
Değeri bu ayardan küçük olan temas itmelerini yok sayar.

#### Ray Cast Limit 2d
Kare başına en fazla 2B ışın sorgusu isteği sayısı.

#### Ray Cast Limit 3d
Kare başına en fazla 3B ışın sorgusu isteği sayısı.

#### Trigger Overlap Capacity
Üst üste gelen en fazla fizik tetikleyicisi sayısı.

#### Velocity Threshold
Esnek çarpışmayla sonuçlanacak en düşük hız.

#### Max Fixed Timesteps
Sabit zaman adımı kullanılırken simülasyondaki en fazla adım sayısı (yalnızca 3B).

---

### Graphics

#### Default Texture Min Filter
Küçültme filtrelemesinde kullanılacak filtreleme türünü belirtir.

#### Default Texture Mag Filter
Büyütme filtrelemesinde kullanılacak filtreleme türünü belirtir.

#### Max Draw Calls
En fazla işleme çağrısı sayısı.

#### Max Characters:
Metin işleme arabelleğinde önceden yer ayrılan karakter sayısı; başka bir deyişle her karede görüntülenebilecek karakter sayısı.

#### Max Font Batches
Her karede görüntülenebilecek en fazla metin çizim grubu sayısı.

#### Max Debug Vertices
En fazla hata ayıklama köşesi sayısı. Diğer kullanımların yanı sıra fizik şekillerinin işlenmesinde kullanılır.

#### Texture Profiles
Bu proje için kullanılacak doku profilleri dosyası; varsayılan olarak `/builtins/graphics/default.texture_profiles`.

#### Verify Graphics Calls
Her grafik çağrısından sonra dönüş değerini doğrular ve hataları günlüğe kaydeder.

#### WebGL Version Hint
`graphics.webgl_version_hint`, HTML5 için istenecek WebGL bağlamı sürümünü seçer. Geçerli değerler `1` (WebGL 1) ve `2` (WebGL 2, varsayılan) değerleridir. WebGL 2'yi destekleyen bir tarayıcıda bile WebGL 1'i hedeflemek veya test etmek için `1` olarak ayarlayın. Gerekli gölgelendiricilerin dahil edilmesi için WebGL 1'i hedeflerken [Exclude GLES 2.0](#exclude-gles-20) ayarını devre dışı bırakılmış olarak tutun.

#### OpenGL Version Hint
OpenGL bağlamı sürüm ipucu. Belirli bir sürüm seçilirse gereken en düşük sürüm olarak kullanılır (OpenGL ES için geçerli değildir).

#### OpenGL Core Profile Hint
Bağlam oluşturulurken 'core' OpenGL profil ipucunu ayarlar. Çekirdek profil, anında modda işleme gibi kullanımı artık önerilmeyen tüm özellikleri OpenGL'den kaldırır. OpenGL ES için geçerli değildir.

#### Vulkan Version Major
`graphics.vulkan_version_major`, Vulkan bağlamının/API'sinin ana sürüm ipucudur. Yalnızca Vulkan grafik arka ucu seçildiğinde geçerlidir. Varsayılan değer `1`'dir.

#### Vulkan Version Minor
`graphics.vulkan_version_minor`, Vulkan bağlamının/API'sinin alt sürüm ipucudur. Yalnızca Vulkan grafik arka ucu seçildiğinde geçerlidir. Varsayılan değer `0`'dır.

---

### Shader

#### Exclude GLES 2.0
OpenGLES 2.0 / WebGL 1.0 çalıştıran cihazlar için gölgelendiricileri derlemez.

#### GLSL ES Default Precision Float
`shader.glsl_es_default_precision_float`, çapraz derlenen GLSL ES gölgelendiricilerinde kayan noktalı değerler için varsayılan genel hassasiyet niteleyicisini ayarlar. Geçerli değerler `mediump` ve `highp`; varsayılan değer `mediump`.

#### GLSL ES Default Precision Int
`shader.glsl_es_default_precision_int`, çapraz derlenen GLSL ES gölgelendiricilerinde tam sayı değerleri için varsayılan genel hassasiyet niteleyicisini ayarlar. Geçerli değerler `mediump` ve `highp`; varsayılan değer `highp`.

---

### Input

#### Repeat Delay
Basılı tutulan bir girdinin yinelenmeye başlaması için beklenecek saniye sayısı.

#### Repeat Interval
Basılı tutulan bir girdinin her yinelenmesi arasında beklenecek saniye sayısı.

#### Gamepads
Oyun kumandası sinyallerini işletim sistemiyle eşleyen oyun kumandaları yapılandırma dosyasının başvurusu; varsayılan olarak `/builtins/input/default.gamepads`.

#### Game Binding
Donanım girdilerini eylemlere eşleyen girdi yapılandırma dosyasının başvurusu; varsayılan olarak `/input/game.input_binding`.

#### Use Accelerometer
Motorun her karede ivmeölçer girdi olaylarını alması için işaretleyin. İvmeölçer girdisini devre dışı bırakmak bir miktar performans artışı sağlayabilir.

---

### Resource

#### Http Cache
İşaretlenirse kaynakların ağ üzerinden cihazda çalışan motora daha hızlı yüklenmesi için bir HTTP önbelleği etkinleştirilir.

#### Uri
Projenin derleme verilerinin nerede bulunacağı; URI biçimindedir.

#### Max Resources
Aynı anda yüklenebilecek en fazla kaynak sayısı.

---

### Network

#### Http Timeout
Saniye cinsinden HTTP zaman aşımı. Zaman aşımını devre dışı bırakmak için `0` olarak ayarlayın.

#### Http Thread Count
HTTP hizmeti için çalışan iş parçacığı sayısı.

#### Http Cache Enabled
Ağ istekleri (`http.request()` kullanılarak yapılan) için HTTP önbelleğini etkinleştirmek üzere işaretleyin. HTTP önbelleği, bir istekle ilişkili yanıtı saklar ve saklanan yanıtı sonraki isteklerde yeniden kullanır. HTTP önbelleği, `ETag` ve `Cache-Control: max-age` HTTP yanıt üstbilgilerini destekler.

#### SSL Certificates
SSL el sıkışmaları sırasında sertifika zincirini doğrulamak için kullanılacak SSL kök sertifikalarını içeren dosya.

---

### Collection

#### Max Instances
Bir koleksiyondaki en fazla oyun nesnesi örneği sayısı; varsayılan olarak `1024`. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Max Input Stack Entries
Girdi yığınındaki en fazla oyun nesnesi sayısı.

---

### Sound

#### Gain
Genel kazanç (ses düzeyi), `0`--`1`.

#### Use Linear Gain
Etkinleştirilirse kazanç doğrusaldır. Devre dışı bırakılırsa üstel bir eğri kullanılır.

#### Max Sound Data
En fazla ses kaynağı sayısı; başka bir deyişle çalışma sırasındaki benzersiz ses dosyalarının sayısı.

#### Max Sound Buffers
(Şu anda kullanılmıyor) Aynı anda var olabilecek en fazla ses arabelleği sayısı.

#### Max Sound Sources
(Şu anda kullanılmıyor) Aynı anda çalınabilecek en fazla ses sayısı.

#### Max Sound Instances
Aynı anda var olabilecek en fazla ses örneği sayısı; başka bir deyişle aynı anda gerçekten çalınan sesler.

#### Max Component Count
Koleksiyon başına en fazla ses bileşeni sayısı.

#### Sample Frame Count
Her ses güncellemesinde kullanılan örnek sayısı. 0, otomatik anlamına gelir (48 kHz için 1024, 44,1 kHz için 768).

#### Use Thread
İşaretlenirse ses sistemi, ana iş parçacığı yoğun yük altındayken takılma riskini azaltmak için ses oynatmada iş parçacıkları kullanır.

#### Stream Enabled
İşaretlenirse ses sistemi, kaynak dosyaları yüklemek için akış yöntemini kullanır.

#### Stream Cache Size
_Tüm_ parçaları içeren ses parçası önbelleğinin en büyük boyutu. Varsayılan olarak `2097152` bayt.
Bu sayının, yüklü ses dosyası sayısıyla akış parçası boyutunun çarpımından büyük olması önerilir.
Aksi takdirde yeni parçaların her karede önbellekten çıkarılması riski doğar.

#### Stream Chunk Size
Akışla aktarılan her parçanın bayt cinsinden boyutu.

#### Stream Preload Size
Arşivden okunan ses dosyaları için ilk parçanın bayt cinsinden boyutunu belirler.

---

### Sprite

#### Max Count
Koleksiyon başına en fazla sprite bileşeni sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Subpixels
Sprite bileşenlerinin piksellere hizalanmadan görüntülenmesine izin vermek için işaretleyin.

---

### Tilemap

#### Max Count
Koleksiyon başına en fazla karo haritası (tile map) sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Max Tile Count
Koleksiyon başına aynı anda görünür olabilecek en fazla karo sayısı.

---

### Spine

#### Max Count
En fazla Spine model bileşeni sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

---

### Mesh

#### Max Count
Koleksiyon başına en fazla örgü (mesh) bileşeni sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

---

### Model

#### Max Count
Koleksiyon başına en fazla model bileşeni sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Split Meshes
65536'dan fazla köşesi olan örgüleri yeni örgülere böler.

#### Max Bone Matrix Texture Width
Kemik matrisi dokusunun en büyük genişliği. Yalnızca animasyonlar için gereken boyut kullanılır ve yukarı doğru ikinin en yakın kuvvetine yuvarlanır.

#### Max Bone Matrix Texture Height
Kemik matrisi dokusunun en büyük yüksekliği. Yalnızca animasyonlar için gereken boyut kullanılır ve yukarı doğru ikinin en yakın kuvvetine yuvarlanır.

---

### GUI

#### Max Count
En fazla GUI bileşeni sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Max Particle Count
GUI'de aynı anda var olabilecek en fazla parçacık sayısı.

#### Max Animation Count
GUI'deki en fazla etkin animasyon sayısı.

---

### Label

#### Max Count
En fazla etiket (label) sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Subpixels
Etiketlerin piksellere hizalanmadan görüntülenmesine izin vermek için işaretleyin.

---

### Particle FX

#### Max Count
Aynı anda var olabilecek en fazla yayıcı (emitter) sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

#### Max Particle Count
Aynı anda var olabilecek en fazla parçacık sayısı.

---

### Box2D

#### Velocity Iterations
Box2D 2.2 fizik çözücüsü için hız yinelemesi sayısı.

#### Position Iterations
Box2D 2.2 fizik çözücüsü için konum yinelemesi sayısı.

#### Sub Step Count
Box2D 3.x fizik çözücüsü için alt adım sayısı.

---

### Collection proxy

#### Max Count
En fazla koleksiyon vekili sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count
En fazla koleksiyon fabrikası (collection factory) sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

---

### Factory

#### Max Count
En fazla oyun nesnesi fabrikası (factory) sayısı. [(Bileşen sayısı üst sınırı optimizasyonlarıyla ilgili bilgilere bakın)](#component-max-count-optimizations).

---

### iOS

#### App Icon 57x57--180x180
Belirtilen `W` &times; `H` genişlik ve yükseklik boyutlarında uygulama simgesi olarak kullanılacak görüntü dosyası (.png).

#### Launch Screen
Storyboard dosyası (.storyboard). Böyle bir dosyanın nasıl oluşturulacağını [iOS kılavuzundan](/manuals/ios/#creating-a-storyboard) öğrenebilirsiniz.

#### Icons Asset
Uygulama simgelerini içeren simge varlığı dosyası (.car).

#### Prerendered Icons
(iOS 6 ve öncesi) Simgeleriniz önceden işlenmişse işaretleyin. İşaretli değilse simgelere otomatik olarak parlak bir vurgu eklenir.

#### Bundle Identifier
Paket tanımlayıcısı, iOS'un uygulamanızın güncellemelerini tanımasını sağlar. Paket kimliğiniz Apple'a kaydedilmeli ve uygulamanıza özgü olmalıdır. iOS ve macOS uygulamaları için aynı tanımlayıcıyı kullanamazsınız. Noktayla ayrılmış iki veya daha fazla bölümden oluşmalıdır. Her bölüm bir harfle başlamalıdır. Her bölüm yalnızca harflerden, rakamlardan, alt çizgi veya kısa çizgi (-) karakterinden oluşmalıdır (bkz. [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Bundle Name
Paketin kısa adı (15 karakter) (bkz. [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version
Paketin sürümü; bir sayı veya x.y.z biçiminde (bkz. [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Info.plist
Belirtilirse uygulamanız paketlenirken yerleşik iOS temel bildirimi yerine bu *`Info.plist`* dosyası kullanılır. Yerleşik bildirim, yayıma yönelik olmayan derlemelerde düzenleyicinin hedef keşfi için gereken yerel ağ ve Bonjour girdilerini içerir. Özel bir bildirim sağlıyorsanız ve bir cihazda hedef keşfine, profil çıkarmaya, çalışma sırasında yeniden yüklemeye (hot reload) veya günlük akışına ihtiyaç duyuyorsanız bu girdileri [iOS kılavuzunda](/manuals/ios/#creating-an-ios-application-bundle) açıklandığı şekilde koruyun.

#### Privacy Manifest
Uygulamanın Apple Privacy Manifest dosyası. Alanın varsayılan değeri `/builtins/manifests/ios/PrivacyInfo.xcprivacy` olacaktır.

#### Custom Entitlements
Belirtilirse sağlanan sağlama profilindeki (provisioning profile; `.entitlements`, `.xcent`, `.plist`) yetkiler, uygulama paketlenirken sağlanan sağlama profilindeki yetkilerle birleştirilir.

#### Default Language
Uygulamanın `Localizations` listesinde kullanıcının tercih ettiği dil bulunmuyorsa kullanılacak dil (bkz. [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Tercih edilen dil iki harfli ISO 639-1 standardında bulunuyorsa bu standardı, bulunmuyorsa üç harfli ISO 639-2 standardını kullanın.

#### Localizations
Bu alan, desteklenen yerelleştirmelerin dil adını veya ISO dil kodunu belirten, virgülle ayrılmış dizeleri içerir (bkz. [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
Belirtilen `W` &times; `H` genişlik ve yükseklik boyutlarında uygulama simgesi olarak kullanılacak görüntü dosyası (.png).

#### Push Icon Small--LargeXxxhdpi
Android'de özel anlık bildirim simgesi olarak kullanılacak görüntü dosyaları (.png). Simgeler hem yerel hem de uzak anlık bildirimlerde otomatik olarak kullanılır. Ayarlanmazsa varsayılan olarak uygulama simgesi kullanılır.

#### Push Field Title
Bildirim başlığı olarak JSON yükündeki hangi alanın kullanılacağını belirtir. Bu ayar boş bırakılırsa anlık bildirimlerin başlığı varsayılan olarak uygulama adı olur.

#### Push Field Text
Bildirim metni olarak JSON yükündeki hangi alanın kullanılacağını belirtir. Boş bırakılırsa iOS'ta olduğu gibi `alert` alanındaki metin kullanılır.

#### Version Code
Uygulamanın sürümünü belirten bir tam sayı değeri. Sonraki her güncellemede bu değeri artırın.

#### Minimum SDK Version
Uygulamanın çalışması için gereken en düşük API düzeyi (`android:minSdkVersion`).

#### Target SDK Version
Uygulamanın hedeflediği API düzeyi (`android:targetSdkVersion`).

#### Package
Paket tanımlayıcısı. Noktayla ayrılmış iki veya daha fazla bölümden oluşmalıdır. Her bölüm bir harfle başlamalıdır. Her bölüm yalnızca harflerden, rakamlardan veya alt çizgi karakterinden oluşmalıdır.

#### GCM Sender Id
Google Cloud Messaging gönderen tanımlayıcısı. Anlık bildirimleri etkinleştirmek için bunu Google'ın atadığı dizeye ayarlayın.

#### FCM Application Id
Firebase Cloud Messaging uygulama tanımlayıcısı.

#### Manifest
Ayarlanırsa paketleme sırasında belirtilen Android bildirim XML dosyası kullanılır. Özel bir bildirim, Defold'un yerleşik temel bildiriminin yerini alır. Yerel kod eklentilerinin (native extension) bildirim parçaları yine bu dosyayla birleştirilir; ancak yerleşik temel bildirimde daha sonra yapılan değişiklikler otomatik olarak aktarılmaz. Bu nedenle sürüm yükseltirken özel bildirimleri geçerli yerleşik bildirimle karşılaştırın. Oyunlar için `android:appCategory="game"` ayarını `<application>` öğesinde yapın. Oyun olmayan uygulamalarda `android:appCategory` ayarını yalnızca Android'in tanımlı [uygulama kategorilerinden](https://developer.android.com/guide/topics/manifest/application-element#appCategory) biri uygulamayı doğru şekilde tanımlıyorsa yapın.

#### Iap Provider
Kullanılacak mağazayı belirtir. `Amazon` ve `GooglePlay` seçenekleri geçerlidir. Daha fazla bilgi için [extension-iap](/extension-iap/) sayfasına bakın.

#### Input Method
Android cihazlarda klavye girdisi almak için kullanılacak yöntemi belirtir. Geçerli seçenekler `KeyEvent` (eski yöntem) ve `HiddenInputField` (yeni).

#### Immersive Mode
Ayarlanırsa gezinme ve durum çubuklarını gizler ve uygulamanızın ekrandaki tüm dokunma olaylarını yakalamasını sağlar.

#### Display Cutout
Ekran çentiğine kadar genişletir.

#### Debuggable
[GAPID](https://github.com/google/gapid) veya [Android Studio](https://developer.android.com/studio/profile/android-profiler) gibi araçlarla uygulamada hata ayıklanıp ayıklanamayacağını belirler. Android bildirimindeki `android:debuggable` bayrağını ayarlar ([resmî belgeler](https://developer.android.com/guide/topics/manifest/application-element#debug)).

#### R8 Keep Rules
`android.r8_keep_rules`, Android derlemelerinde Java kodunun R8 ile küçültülmesini, optimize edilmesini ve karartılmasını etkinleştirmek için bir `.keep` dosyası seçer. D8'i küçültme yapmadan kullanmak için ayarı boş bırakın.

Defold'un varsayılan kurallarını doğrudan kullanmak için `/builtins/manifests/android/dmengine.keep` dosyasını seçin. Eklentiler kendi [koruma kurallarını](/manuals/extensions/#r8-keep-rules-for-android) sağlar; bu kurallar bu dosyayla birleştirilir.

Yerleşik dosyayı yalnızca projeye özgü kurallar eklemeniz gerekiyorsa projenize kopyalayın. Kopyadaki yerleşik kuralları koruyun: özel bir dosya seçmek, projenin tüm kural kümesini değiştirir.

R8'i etkinleştirmek ve karartma eşlemesini yayıma yönelik bir dağıtım paketiyle birlikte saklamak için [Android kılavuzuna](/manuals/android/#shrinking-java-code-with-r8) bakın.

#### Extract Native Libraries
Paket yükleyicisinin yerel kod kütüphanelerini APK dosyasından dosya sistemine çıkarıp çıkarmayacağını belirtir. `false` olarak ayarlanırsa yerel kod kütüphaneleriniz APK içinde sıkıştırılmadan saklanır. APK dosyanız daha büyük olsa da kütüphaneler çalışma sırasında doğrudan APK dosyasından yüklendiği için uygulamanız daha hızlı yüklenir. Android bildirimindeki `android:extractNativeLibs` bayrağını ayarlar ([resmî belgeler](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
macOS'ta uygulama simgesi olarak kullanılacak paket simgesi dosyası (.icns).

#### Info.plist
Ayarlanırsa paketleme sırasında belirtilen info.plist dosyası kullanılır.

#### Privacy Manifest
Uygulamanın Apple Privacy Manifest dosyası. Alanın varsayılan değeri `/builtins/manifests/osx/PrivacyInfo.xcprivacy` olacaktır.

#### Bundle Identifier
Paket tanımlayıcısı, macOS'un uygulamanızın güncellemelerini tanımasını sağlar. Paket kimliğiniz Apple'a kaydedilmeli ve uygulamanıza özgü olmalıdır. iOS ve macOS uygulamaları için aynı tanımlayıcıyı kullanamazsınız. Noktayla ayrılmış iki veya daha fazla bölümden oluşmalıdır. Her bölüm bir harfle başlamalıdır. Her bölüm yalnızca harflerden, rakamlardan, alt çizgi veya kısa çizgi (-) karakterinden oluşmalıdır.

#### Default Language
Uygulamanın `Localizations` listesinde kullanıcının tercih ettiği dil bulunmuyorsa kullanılacak dil (bkz. [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Tercih edilen dil iki harfli ISO 639-1 standardında bulunuyorsa bu standardı, bulunmuyorsa üç harfli ISO 639-2 standardını kullanın.

#### Localizations
Bu alan, desteklenen yerelleştirmelerin dil adını veya ISO dil kodunu belirten, virgülle ayrılmış dizeleri içerir (bkz. [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows

#### App Icon
Windows'ta uygulama simgesi olarak kullanılacak görüntü dosyası (.ico). .ico dosyası oluşturma hakkında daha fazla bilgi için [Windows kılavuzuna](/manuals/windows) bakın.

---

### HTML5

Bu seçeneklerin çoğu hakkında daha fazla bilgi için [HTML5 platformu kılavuzuna](/manuals/html5/) bakın.

#### Heap Size
Emscripten'in kullanacağı öbeğin megabayt cinsinden boyutu.

#### .html Shell
Paketleme sırasında belirtilen HTML şablon dosyasını kullanır. Varsayılan olarak `/builtins/manifests/web/engine_template.html`.

#### Custom .css
Paketleme sırasında belirtilen CSS tema dosyasını kullanır. Varsayılan olarak `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Ayarlanırsa oluşturulan dağıtım paketinde, başlangıçta Defold logosu yerine belirtilen açılış görüntüsü kullanılır.

#### Archive Location Prefix
HTML5 için paketleme yapılırken oyun verileri bir veya daha fazla arşiv veri dosyasına bölünür. Motor oyunu başlattığında bu arşiv dosyaları belleğe okunur. Verilerin konumunu belirtmek için bu ayarı kullanın.

#### Archive Location Suffix
Arşiv dosyalarının sonuna eklenecek son ek. Örneğin bir CDN'den önbelleğe alınmamış içeriğin alınmasını zorlamak için yararlıdır (örneğin `?version2`).

#### Engine Arguments
Motora geçirilecek bağımsız değişkenlerin listesi.

#### Wasm Streaming
wasm dosyasının akışla aktarılmasını etkinleştirir (daha hızlıdır ve daha az bellek kullanır, ancak `application/wasm` MIME türünü gerektirir).

#### Show Fullscreen Button
`index.html` dosyasında Fullscreen Button düğmesini etkinleştirir.

#### Show Made With Defold
`index.html` dosyasında Made With Defold bağlantısını etkinleştirir.

#### Show Console Banner
Bu seçenek etkinleştirildiğinde, motor başladığında motor ve sürümü hakkında bilgiler tarayıcı konsoluna yazdırılır (`console.log()` kullanılarak).

#### Scale Mode
Oyun tuvalini ölçeklemek için kullanılacak yöntemi belirtir.

#### Retry Count
Başlangıç sırasında başarısız bir indirmeden sonraki yeniden deneme sayısı; ağ hatalarını, başarısız HTTP durumlarını ve motorun JavaScript veya WebAssembly dosyasındaki boyut uyuşmazlıklarını kapsar. İlk istek ayrı sayılır. Arşiv dosyası doğrulamasının kendi yeniden deneme sınırı vardır; [indirme doğrulamasına](/manuals/html5/#download-verification) ve `Retry Time` ayarına bakın.

#### Retry Time
İndirme başarısız olduğunda dosyayı indirme girişimleri arasında beklenecek saniye sayısı (bkz. `Retry Count`).

#### Verify Downloaded File Size
`html5.verify_downloaded_file_size`, indirilen motor ve arşiv dosyalarını beklenen boyutlarıyla karşılaştırır. Varsayılan olarak etkindir (`true`). Yalnızca bir sunucu, ara sunucu veya CDN dosyaları bilerek yeniden yazıp boyutlarını değiştiriyorsa `false` olarak ayarlayın. Doğrulama başarısız olursa başlatma başarısızlıkla sonuçlanmadan önce indirme yeniden denenir. Motor indirmeleriyle arşiv dosyası doğrulamasının yeniden deneme sınırları farklıdır; [indirme doğrulamasına](/manuals/html5/#download-verification) bakın.

#### Transparent Graphics Context
Grafik bağlamının saydam bir arka plana sahip olması için işaretleyin.

---

### IAP

#### Auto Finish Transactions
IAP işlemlerini otomatik olarak tamamlamak için işaretleyin. İşaretli değilse başarılı bir işlemden sonra `iap.finish()` işlevini açıkça çağırmanız gerekir.

---

### Live update

#### Settings
Paketleme sırasında kullanılacak Live Update ayarları kaynak dosyası.

---

### Native extension

#### _App Manifest_
Ayarlanırsa motor derlemesini özelleştirmek için uygulama bildirimi (app manifest) kullanılır. Bu, son ikili dosyanın boyutunu azaltmak için motorun kullanılmayan bölümlerini kaldırmanızı sağlar. Kullanılmayan özellikleri nasıl hariç tutacağınızı [uygulama bildirimi kılavuzundan](/manuals/app-manifest) öğrenebilirsiniz.

---

### Profiler

App Manifest içindeki **Profiler** ayarı, profil çıkarıcı kodunun hata ayıklama derlemelerine ve yayıma yönelik derlemelere bağlanıp bağlanmayacağını belirler. Aşağıdaki ayarlar, seçilen derlemede bulunan profil çıkarıcı kodunun çalışma sırasındaki davranışını denetler. Ayrıntılar için [Profil çıkarma kılavuzuna](/manuals/profiling/) bakın.

#### Enabled
Oyun içi profil çıkarıcıyı etkinleştirir.

#### Track Cpu
CPU kullanımı örneklemesi, hata ayıklama derlemelerinde varsayılan olarak etkindir. App Manifest aracılığıyla profil çıkarıcı desteği içeren, yayıma yönelik bir derlemede de CPU örneklemesi gerekiyorsa bu ayarı etkinleştirin.

#### Sleep Between Server Updates
Sunucu güncellemeleri arasında beklenecek milisaniye sayısı.

#### Performance Timeline Enabled
Tarayıcı içi performans zaman çizelgesini etkinleştirir (yalnızca HTML5).

#### Max Sample Count
`profiler.max_sample_count`, her karede iş parçacığı başına kaydedilen en fazla profil çıkarıcı örneği sayısıdır. Varsayılan değer `4096`, en düşük değer ise `128`'dir. Bunu yalnızca geçerli bir profil sınırı aşıyorsa artırın; önce yerel kod eklentilerinin profil çıkarma kodunda eşleşmeyen kapsam başlatma/bitirme çağrılarını kontrol edin.

---

## Motor başlangıcında yapılandırma değerlerini ayarlama

Motor başlarken komut satırından *game.project* ayarlarını geçersiz kılan yapılandırma değerleri sağlanabilir:

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

Özel değerler---tıpkı diğer yapılandırma değerleri gibi---[Çalışma sırasında erişim](#runtime-access) bölümünde açıklanan uygun işlevle okunabilir:

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Özel proje ayarları

Ana proje veya bir [yerel kod eklentisi](/manuals/extensions/) için özel ayarlar tanımlanabilir. Ana projenin özel ayarları, proje kökündeki bir `game.properties` dosyasında tanımlanmalıdır. `ext.properties` adlı dosyalar, projenin ve alınan kütüphane bağımlılıklarının herhangi bir yerinde bulunabilir; aynı dizinde bir `ext.manifest` bulunmasını gerektirmezler. Bulunan tüm eklenti üst verileri birleştirilir, ardından kökteki `game.properties` dosyası uygulanır ve bu üst verileri geçersiz kılabilir.

Ayarlar dosyası, *game.project* ile aynı INI biçimini kullanır ve özellik öznitelikleri, son ek içeren noktalı bir gösterimle tanımlanır:

```
[my_category]
my_property.private = 1
...
```

Her zaman uygulanan varsayılan üst veri dosyası [burada](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties) bulunur

Şu anda aşağıdaki öznitelikler kullanılabilir:

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
Ayrıca bir ayar kategorisinde aşağıdaki öznitelikleri ayarlayabilirsiniz:
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Hem Bob hem de düzenleyici bu üst veri dosyalarını ayrıştırır. Düzenleyici, *game.project* görüntüleyicisinde ilgili alanları, seçenekleri, doğrulamayı ve yardım araç ipuçlarını oluşturmak için bunları kullanır.
