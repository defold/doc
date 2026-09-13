---
title: Uygulama bildirimi
brief: Bu kılavuz, uygulama bildiriminin özellikleri motordan çıkarmak için nasıl kullanılabileceğini açıklar.
---

# Uygulama bildirimi

Uygulama bildirimi (application manifest), hangi özelliklerin ve arka uçların (backend) motora bağlanacağını belirler. Kullanılmayan özelliklerin çıkarılması önerilir; bu, oyununuzun son ikili dosyasının boyutunu küçültür. Uygulama bildirimi ayrıca desteklenen en düşük HTML5 tarayıcı sürümleri ve WebAssembly bellek ayarları gibi derleme zamanı seçeneklerini de içerir.

![](images/app_manifest/create-app-manifest.png)

![](images/app_manifest/app-manifest.png)

# Bildirimi uygulama

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

Video kaydetme özelliğini motordan çıkarın ([`start_record`](https://defold.com/ref/stable/sys/#start_record) iletisinin belgelerine bakın).


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

`image` betik modülünü ([belgeler](https://defold.com/ref/stable/image/)) motordan çıkarın.


## Exclude Types

`types` betik modülünü ([belgeler](https://defold.com/ref/stable/types/)) motordan çıkarın.


## Exclude Basis Transcoder

Basis Universal [doku sıkıştırma kütüphanesini](/manuals/texture-profiles) motordan çıkarın.


## Use Android Support Lib

Android X yerine kullanımı artık önerilmeyen Android Support Library'yi kullanın. [Daha fazla bilgi](https://defold.com/manuals/android/#using-androidx).


## Graphics

Her platform için hangi grafik arka uçlarının dahil edileceğini seçin. Birleşik seçim her iki arka ucu da dahil eder; böylece tercih edilen arka uç kullanılamadığında diğerine geçilebilir.

| Alan | Platformlar | Seçenekler | Varsayılan |
|---|---|---|---|
| **Graphics** | Windows ve Linux | OpenGL, Vulkan, OpenGL & Vulkan | OpenGL |
| **Graphics (macOS)** | macOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | Vulkan |
| **Graphics (iOS)** | iOS | OpenGL, Metal, Vulkan, OpenGL & Metal, OpenGL & Vulkan | OpenGL |
| **Graphics (Android)** | Android | OpenGL+Vulkan, OpenGL, Vulkan | OpenGL+Vulkan |
| **Graphics (HTML5)** | HTML5 | WebGL, WebGPU, WebGL & WebGPU | WebGL |

Linux ARM64 üzerinde **OpenGL** seçeneği, OpenGL ES arka ucunu kullanır. Android'in varsayılan birleşik seçeneği, kullanılabiliyorsa Vulkan'ı tercih eder; kullanılamıyorsa OpenGL ES'ye geçer.

## Use full text layout system

Etkinleştirildiğinde (`true`), sağdan sola yazılan diller dahil olmak üzere metinleri şekillendirmek için tam metin yerleşim sistemi dahil edilir. Bu seçeneği *game.project* dosyasındaki `font.runtime_generation` ile birlikte etkinleştirin; böylece TrueType (`.ttf`) veya OpenType (`.otf`) kaynaklarından çalışma sırasında SDF yazı tipleri oluşturabilirsiniz. `.otf` kaynaklarından çalışma sırasında oluşturma, Defold 1.13.2'den beri desteklenir. [Yazı tipi kılavuzunda](/manuals/font/#enabling-runtime-fonts) daha fazla bilgi edinin.


## Use Rich Text

Etiketler ve GUI metni için zengin metin ayrıştırmasını ve stil efektlerini dahil edin. Bu seçenek varsayılan olarak etkindir. Proje yalnızca düz metne ihtiyaç duyduğunda motor boyutunu küçültmek için bu seçeneği devre dışı bırakın. Etiketler ve GUI metni desteklenmeye devam eder, ancak işaretleme, biçimlendirme veya efekt uygulamak yerine düz metin olarak görüntülenir.


## En düşük tarayıcı sürümleri

**`minSafariVersion`**, **`minFirefoxVersion`** ve **`minChromeVersion`** YAML alanları, Emscripten'in hedeflediği en düşük tarayıcı sürümlerini belirtir. Geçerli varsayılan değerler ve desteklenen en düşük sürümler, iş parçacığı kullanmayan ve kullanan hedefler arasında farklılık gösterir:

| Hedef | Safari | Firefox | Chrome |
|---|---:|---:|---:|
| `wasm-web` | `101000` | `40` | `45` |
| `wasm_pthread-web` | `150000` | `79` | `75` |

Varsayılanların yerine kullanılacak değerleri ilgili hedefin bağlamında belirtin. İş parçacığı kullanan hedefin ayrıca ek [barındırma gereksinimleri](/manuals/html5/#creating-html5-bundle) vardır. Emscripten ayar başvurusundaki [`MIN_SAFARI_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-safari-version), [`MIN_FIREFOX_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-firefox-version) ve [`MIN_CHROME_VERSION`](https://emscripten.org/docs/tools_reference/settings_reference.html#min-chrome-version) ayarlarına bakın.

## Başlangıç belleği (HTML5)
YAML alan adı: **`initialMemory`**
Varsayılan değer: **33554432**

Web uygulaması için başlangıçta ayrılan bellek miktarı, bayt cinsindendir. Değer, WebAssembly sayfa boyutunun (64 KiB) katı olmalıdır. Emscripten'in [`INITIAL_MEMORY`](https://emscripten.org/docs/tools_reference/settings_reference.html#initial-memory) ayarına bakın.

Bu seçenek, kod derleme zamanındaki varsayılan değeri sağlar. *game.project* dosyasındaki [`html5.heap_size`](/manuals/html5/#heap-size) değeri, çalışma sırasında bunun yerine geçer.

## Yığın boyutu (HTML5)
YAML alan adı: **`stackSize`**
Varsayılan değer: **5242880**

Uygulama yığınının bayt cinsinden boyutu. Emscripten'in [`STACK_SIZE`](https://emscripten.org/docs/tools_reference/settings_reference.html#stack-size) ayarına bakın.
