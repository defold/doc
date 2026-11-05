---
title: Uygulama bildirimi
brief: Bu kılavuz, uygulama bildiriminin özellikleri motordan çıkarmak için nasıl kullanılabileceğini açıklar.
---

# Uygulama bildirimi {#app-manifest}

Uygulama bildirimi (application manifest), hangi özelliklerin ve arka uçların (backend) motora bağlanacağını belirler. Kullanılmayan özelliklerin çıkarılması önerilir; bu, oyununuzun son ikili dosyasının boyutunu küçültür. Uygulama bildirimi ayrıca desteklenen en düşük HTML5 tarayıcı sürümleri ve WebAssembly bellek ayarları gibi derleme zamanı seçeneklerini de içerir.

![](images/app_manifest/create-app-manifest.png)

# Bildirimi uygulama {#applying-the-manifest}

`game.project` dosyasında bildirimi `Native Extensions` -> `App Manifest` alanına atayın.

## Physics 2D

Dahil edilecek Box2D uygulamasını seçin:

* **Box2D Version 3** - Box2D 3'ü dahil edin. Bunun için bu seçeneği açıkça seçmeniz gerekir. Eski uygulamadan farklı simülasyon sonuçları üretebileceğinden, mevcut projelerin fizik ayarlarını yeniden düzenlemesi gerekebilir.
* **Box2D (Legacy Defold version)** - Eski Defold Box2D uygulamasını dahil edin. Varsayılan budur.
* **None** - 2B fiziği çıkarın.

Box2D çözücü ayarları sürüme özgüdür. Ayrıntılar için [Box2D proje ayarlarına](/manuals/project-settings/#box2d) bakın.

## Physics 3D

Bullet 3B fizik uygulamasını dahil edin. Varsayılan olarak dahildir; 3B fiziği çıkarmak için bu ayarı devre dışı bırakın.

## Rig + Model

İskelet düzeneği (rig) ve model işlevlerini belirleyin veya model ve iskelet düzeneğini tamamen çıkarmak için None seçeneğini seçin. ([`Model`](https://defold.com/manuals/model/#model-component) belgelerine bakın).


## Exclude Record

Yerel MP4 kaydını, [`recorder` Lua modülünü](/ref/recorder/) ve kayıt HTTP hizmetini masaüstü hata ayıklama derlemelerinden çıkarın. Kayıt, yayıma yönelik derlemelerde, görüntüsüz (headless) derlemelerde, mobil ve web derlemelerinde zaten bulunmaz. İş akışı için [kayıt kılavuzuna](/manuals/recording) bakın.


## Profiler

Profil çıkarıcı (profiler) işlevlerinin motora ne zaman bağlanacağını belirleyin:

* **Debug Only** - Profil çıkarıcıyı yalnızca hata ayıklama derlemelerine dahil edin. Varsayılan budur.
* **None** - Profil çıkarıcı işlevlerini tüm derleme çeşitlerinden çıkarın.
* **Always** - Profil çıkarıcıyı hem hata ayıklama derlemelerine hem de yayıma yönelik derlemelere dahil edin.

Uygulama bildirimi ayarı, profil çıkarıcı kodunun derlemeye bağlanıp bağlanmayacağını belirler. *game.project* dosyasındaki `profiler` altındaki ayarlar, profil çıkarıcının çalışma sırasındaki davranışını belirler. Mevcut olanakların nasıl kullanılacağını [Profil çıkarma kılavuzunda](/manuals/profiling/) öğrenin.


## Sound

Ses ayarları, hangi ses sisteminin ve kod çözücülerin motora bağlanacağını belirler.

### Exclude Sound

Tüm ses oynatma özelliklerini motordan çıkarın.

### Exclude Sound Decoder: WAV

WAV ses kaynakları desteğini çıkarın.

### Exclude Sound Decoder: OGG

Ogg Vorbis ses kaynakları desteğini çıkarın.

### Include Sound Decoder: Opus

Ogg Opus ses kaynakları desteğini dahil edin. Opus kod çözücü varsayılan olarak dahil değildir; bu nedenle `.opus` kaynaklarının oynatılabilmesi için bu seçeneğin etkinleştirilmesi gerekir. Desteklenen biçimler için [Ses kılavuzuna](/manuals/sound/) bakın.


## Exclude Input

Tüm girdi işleme özelliklerini motordan çıkarın.


## Exclude GUI

GUI kaynaklarını, bileşenlerini (component) ve Lua desteğini motordan kaldırın. Bunu yalnızca proje GUI sahneleri veya GUI betikleri kullanmıyorsa etkinleştirin. Etiket (label) bileşenleri kullanılabilir durumda kalır. Bu seçenek varsayılan olarak devre dışıdır.


## Exclude Particle FX

Parçacık efekti (particle effect) kaynaklarını, bileşenlerini ve `particlefx` Lua modülünü kaldırın. Bu işlem GUI sahnelerindeki parçacık düğümlerinin desteğini de kaldırır; parçacık düğümü içermeyen GUI sahneleri desteklenmeye devam eder. Bu seçeneği etkinleştirmeden önce parçacık efektlerine yapılan başvuruları ve bunların API çağrılarını kaldırın. Varsayılan olarak devre dışıdır.


## Exclude Tilemaps

Karo haritası (tilemap) kaynaklarını, bileşenlerini ve `tilemap` Lua modülünü kaldırın. Bunu yalnızca proje karo haritası bileşenlerini veya bunların API'lerini kullanmıyorsa etkinleştirin. Diğer bileşenlerin kullandığı karo kaynakları kullanılabilir durumda kalır. Bu seçenek varsayılan olarak devre dışıdır.


## Exclude Live Update

[Live Update işlevlerini](/manuals/live-update) motordan çıkarın.


## Exclude Image

`image` betik modülünü ([belgeler](https://defold.com/ref/image/)) motordan çıkarın.


## Exclude Types

`types` betik modülünü ([belgeler](https://defold.com/ref/types/)) motordan çıkarın.


## Exclude Basis Transcoder

Basis Universal [doku sıkıştırma kütüphanesini](/manuals/texture-profiles) motordan çıkarın.


## Use Android Support Lib

Android X yerine kullanımı artık önerilmeyen Android Support Library'yi kullanın. [Daha fazla bilgi](https://defold.com/manuals/android/#using-androidx).


## Graphics

Her platform için dahil edilecek grafik arka uçlarını seçin. Birleşik bir seçenek birden çok arka uç içerir; böylece motor, tercih ettiği arka uç kullanılamadığında diğerine dönebilir. Daha fazla arka uç eklemek motor boyutunu artırır.

Windows ve Linux ayrı alanlar kullanır. **DX12** seçeneği, Windows'ta DirectX 12'yi seçer.

| Alan | Platformlar | Seçenekler | Varsayılan |
|---|---|---|---|
| **Graphics (Linux)** | Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (Windows)** | Windows | OpenGL, Vulkan, DX12, OpenGL & Vulkan, OpenGL & DX12, Vulkan & DX12, OpenGL & Vulkan & DX12 | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Metal |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Linux ARM64 üzerinde **OpenGL** seçeneği, OpenGL ES arka ucunu kullanır. Android'in varsayılan birleşik seçeneği, kullanılabiliyorsa Vulkan'ı tercih eder; kullanılamıyorsa OpenGL ES'ye geçer.

macOS varsayılan olarak yerel Metal arka ucunu kullanır. macOS ve iOS'ta **Vulkan** seçeneği, MoltenVK aracılığıyla Vulkan'ı kullanır. iOS simülatörü (`arm64_sim-ios`), cihazlar için belirlenen **Graphics (iOS)** seçeneğinden bağımsız olarak her zaman Metal kullanır.

## Use full text layout system

Etkinleştirildiğinde (`true`), sağdan sola yazılan diller dahil olmak üzere metinleri şekillendirmek için tam metin yerleşim sistemi dahil edilir. TrueType (`.ttf`) veya OpenType (`.otf`) yazı tiplerini çalışma sırasında oluşturmak için bu seçeneği etkinleştirin ve bunu gerektiren her yazı tipi kaynağında *Glyph Generation* ayarını **Dynamic** olarak belirleyin. Dinamik oluşturma hem **SDF** hem de **Vector** modlarını destekler. [Yazı tipi kılavuzunda](/manuals/font/#enabling-runtime-fonts) daha fazla bilgi edinin.


## Use Rich Text

Etiketler ve GUI metni için zengin metin ayrıştırmasını ve stil efektlerini dahil edin. Bu seçenek varsayılan olarak etkindir. Proje yalnızca düz metne ihtiyaç duyduğunda motor boyutunu küçültmek için bu seçeneği devre dışı bırakın. Etiketler ve GUI metni desteklenmeye devam eder, ancak işaretleme, biçimlendirme veya efekt uygulamak yerine düz metin olarak görüntülenir.


## En düşük tarayıcı sürümleri {#minimum-browser-versions}

**`minSafariVersion`**, **`minFirefoxVersion`** ve **`minChromeVersion`** YAML alanları, Emscripten'in hedeflediği en düşük tarayıcı sürümlerini belirtir. Geçerli varsayılan değerler ve desteklenen en düşük sürümler, iş parçacığı kullanmayan ve kullanan hedefler arasında farklılık gösterir:

| Hedef | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Varsayılanların yerine kullanılacak değerleri ilgili hedefin bağlamında belirtin. İş parçacığı kullanan hedefin ayrıca ek [barındırma gereksinimleri](/manuals/html5/#creating-html5-bundle) vardır. Emscripten ayar başvurusundaki [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) ve [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version) ayarlarına bakın.

## Başlangıç belleği (HTML5) {#initial-memory-html5}
YAML alan adı: **`initialMemory`**
Varsayılan değer: **33554432**

Web uygulaması için başlangıçta ayrılan bellek miktarı, bayt cinsindendir. Değer, WebAssembly sayfa boyutunun (64 KiB) katı olmalıdır. Emscripten'in [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) ayarına bakın.

Bu seçenek, kod derleme zamanındaki varsayılan değeri sağlar. *game.project* dosyasındaki [`html5.heap_size`](/manuals/html5/#heap-size) değeri, çalışma sırasında bunun yerine geçer.

## Yığın boyutu (HTML5) {#stack-size-html5}
YAML alan adı: **`stackSize`**
Varsayılan değer: **5242880**

Uygulama yığınının bayt cinsinden boyutu. Emscripten'in [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) ayarına bakın.
