---
title: Yerel kod eklentileri - eklenti bildirimleri
brief: Bu kılavuz, eklenti bildirimini ve bunun uygulama ve motor bildirimleriyle ilişkisini açıklar.
---

# Eklenti, uygulama ve motor bildirim dosyaları

Eklenti bildirimi (extension manifest), tek bir eklentinin derleme sürecinde kullanılan bayrakları (flags) ve tanımları (defines) içeren bir yapılandırma dosyasıdır. Bu yapılandırma, uygulama düzeyindeki bir yapılandırmayla ve Defold motorunun kendisi için temel düzeyde bir yapılandırmayla birleştirilir.

## Uygulama bildirimi

Uygulama bildirimi (application manifest, dosya uzantısı `.appmanifest`), oyununuzun derleme sunucularında nasıl derleneceğini belirleyen uygulama düzeyinde bir yapılandırmadır. Uygulama bildirimi, motorun kullanmadığınız bölümlerini kaldırmanızı sağlar. Bir fizik motoruna ihtiyacınız yoksa yürütülebilir dosyanın boyutunu küçültmek için fizik motorunu dosyadan kaldırabilirsiniz. Kullanılmayan özelliklerin nasıl dışlanacağını [uygulama bildirimi kılavuzundan](/manuals/app-manifest) öğrenin.

## Motor bildirimi

Motorun ve Defold yazılım geliştirme kitinin (SDK) her sürümü, Defold motoruna ait bir derleme bildirimi (`build.yml`) içerir. Bildirim, hangi SDK sürümlerinin kullanılacağını, hangi derleyicilerin, bağlayıcıların (linkers) ve diğer araçların çalıştırılacağını ve bu araçlara hangi varsayılan derleme ve bağlama bayraklarının aktarılacağını belirler. Bildirimi [GitHub üzerinde](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml) share/extender/build_input.yml dosyasında bulabilirsiniz.

## Eklenti bildirimi

Eklenti bildirimi (`ext.manifest`) ise bir eklentiye özel yapılandırma dosyasıdır. Eklenti bildirimi, eklentinin kaynak kodunun nasıl derlenip bağlanacağını ve hangi ek kütüphanelerin dahil edileceğini belirler. 

Üç farklı bildirim dosyasının tümü aynı sözdizimini kullanır. Böylece birleştirilebilir ve eklentilerin ve oyunun nasıl derleneceğini tamamen belirleyebilirler.

Derlenen her eklenti için bildirimler aşağıdaki gibi birleştirilir:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Bu, kullanıcının motorun ve her bir eklentinin varsayılan davranışını geçersiz kılmasını sağlar. Son bağlama aşamasında ise uygulama bildirimini Defold bildirimiyle birleştiririz:

	manifest = merge(game.appmanifest, build.yml)


### ext.manifest dosyası

Bildirim dosyası, eklentinin adının yanı sıra platforma özgü kod derleme bayrakları, bağlama bayrakları, kütüphaneler ve framework'ler içerebilir. *ext.manifest* dosyasında bir "platforms" bölümü yoksa veya listede bir platform eksikse, dağıtım paketi oluşturduğunuz platform için derleme yine yapılır, ancak hiçbir ek bayrak ayarlanmaz.

Aşağıda bir örnek verilmiştir:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    arm64_sim-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### İzin verilen anahtarlar

Platforma özgü kod derleme bayrakları için izin verilen anahtarlar şunlardır:

* `frameworks` - Derleme sırasında dahil edilecek Apple framework'leri (iOS ve macOS)
* `weakFrameworks` - Derleme sırasında isteğe bağlı olarak dahil edilecek Apple framework'leri (iOS ve macOS)
* `flags` - Derleyiciye aktarılacak bayraklar
* `linkFlags` - Bağlayıcıya aktarılacak bayraklar
* `libs` - Bağlama sırasında dahil edilecek ek kütüphaneler
* `defines` - Derleme sırasında ayarlanacak tanımlar
* `aaptExtraPackages` - Oluşturulacak ek paket adı (Android)
* `aaptExcludePackages` - Dışlanacak paketleri belirten düzenli ifade (regexp) veya paketlerin tam adları (Android)
* `aaptExcludeResourceDirs` - Dışlanacak kaynak dizinlerini belirten düzenli ifade veya dizinlerin tam adları (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Bu bayraklar, platform bağlamında daha önce tanımlanmış öğeleri kaldırmak için kullanılır.

Tüm anahtar sözcüklere bir izin listesi filtresi uygularız. Bunun amacı, geçersiz yol işlemlerini ve derleme için yüklenen dosyaların bulunduğu klasörün dışındaki dosyalara erişimi önlemektir.
