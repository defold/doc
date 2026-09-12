---
title: Bir uygulamayı paketleme
brief: Bu kılavuz, bir uygulama dağıtım paketinin nasıl oluşturulacağını açıklar.
---

# Bir uygulamayı paketleme

Uygulamanızı geliştirirken oyunu hedef platformlarda mümkün olduğunca sık test etmeyi alışkanlık haline getirmeniz önerilir. Böylece performans sorunlarını, çözmenin çok daha kolay olduğu geliştirme sürecinin erken aşamalarında tespit edebilirsiniz. Gölgelendiriciler (shader) gibi konulardaki farklılıkları bulmak için de tüm hedef platformlarda test yapmanız önerilir. Mobil cihazlar için geliştirme yaparken, tam bir paketleme (bundling) ve uygulamayı kaldırıp yeniden kurma döngüsü yerine [mobil geliştirme uygulamasını](/manuals/dev-app/) kullanarak içeriği uygulamaya gönderebilirsiniz.

Defold'un desteklediği tüm platformlar için, harici araçlara gerek duymadan doğrudan Defold düzenleyicisinden bir uygulama dağıtım paketi (application bundle) oluşturabilirsiniz. Komut satırı araçlarımızı kullanarak komut satırından da paketleme yapabilirsiniz. Projeniz bir veya daha fazla [yerel kod eklentisi (native extension)](/manuals/extensions) içeriyorsa uygulamayı paketlemek için ağ bağlantısı gerekir.

## Düzenleyiciden paketleme

Project menüsündeki Bundle seçeneğiyle bir uygulama dağıtım paketi oluşturabilirsiniz:

![](images/bundling/bundle_menu.png)

Menü seçeneklerinden herhangi birini seçtiğinizde, ilgili platforma ait Bundle iletişim kutusu açılır.

### Derleme raporları {#build-reports}

Oyununuzu paketlerken bir derleme raporu (build report) oluşturma seçeneği bulunur. Bu, oyununuzun dağıtım paketindeki tüm varlıkların (asset) boyutlarını anlamak için çok yararlıdır. Oyunu paketlerken *Generate build report* onay kutusunu işaretlemeniz yeterlidir.

![derleme raporu](images/profiling/build_report.png)

Derleme raporları hakkında daha fazla bilgi edinmek için [Profil çıkarma kılavuzuna](/manuals/profiling/#build-reports) bakın.

### Android

Android uygulama dağıtım paketi (.apk dosyası) oluşturma işlemi [Android kılavuzunda](/manuals/android/#creating-an-android-application-bundle) açıklanır.

### iOS

iOS uygulama dağıtım paketi (.ipa dosyası) oluşturma işlemi [iOS kılavuzunda](/manuals/ios/#creating-an-ios-application-bundle) açıklanır.

### macOS

macOS uygulama dağıtım paketi (.app dosyası) oluşturma işlemi [macOS kılavuzunda](/manuals/macos) açıklanır.

### Linux

Linux uygulama dağıtım paketi oluşturmak, özel bir kurulum veya *game.project* [proje ayarları dosyasında](/manuals/project-settings/) platforma özgü isteğe bağlı bir yapılandırma gerektirmez.

### Windows

Windows uygulama dağıtım paketi (.exe dosyası) oluşturma işlemi [Windows kılavuzunda](/manuals/windows) açıklanır.

### HTML5

HTML5 uygulama dağıtım paketi oluşturma işlemi ve isteğe bağlı kurulum [HTML5 kılavuzunda](/manuals/html5/#creating-html5-bundle) açıklanır.

#### Facebook Instant Games

Bir HTML5 uygulama dağıtım paketinin, özellikle Facebook Instant Games için hazırlanmış özel bir sürümünü oluşturabilirsiniz. Bu işlem [Facebook Instant Games kılavuzunda](/manuals/instant-games/) açıklanır.

## Komut satırından paketleme

Düzenleyici, uygulamayı paketlemek için [Bob](/manuals/bob/) adlı komut satırı aracımızı kullanır.

Uygulamanızın günlük geliştirme sürecinde derleme ve paketleme işlemlerini büyük olasılıkla Defold düzenleyicisinden yaparsınız. Başka durumlarda uygulama dağıtım paketlerini otomatik oluşturmak isteyebilirsiniz. Örneğin yeni bir sürüm yayımlarken tüm hedefler için toplu derleme yaparken veya oyunun en son sürümünün gece derlemelerini oluştururken bunu isteyebilirsiniz; bu işlemler bir sürekli tümleştirme (CI) ortamında da yapılabilir. Bir uygulamanın derlenmesi ve paketlenmesi, [Bob komut satırı aracı](/manuals/bob/) kullanılarak olağan düzenleyici iş akışının dışında gerçekleştirilebilir.

## Dağıtım paketinin yapısı

Dağıtım paketinin mantıksal yapısı şöyledir:

![](images/bundling/bundle_schematic_01.png)

Dağıtım paketi bir klasöre yazılır. Platforma bağlı olarak bu klasör, zip biçiminde arşivlenerek bir `.apk` veya `.ipa` dosyasına da dönüştürülebilir.
Klasörün içeriği platforma bağlıdır.

Paketleme sürecimiz, yürütülebilir dosyaların yanı sıra platform için gerekli varlıkları da toplar (örneğin Android için .xml kaynak dosyaları).

[bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources) ayarını kullanarak, dağıtım paketine olduğu gibi yerleştirilmesi gereken varlıkları yapılandırabilirsiniz.
Bunu her platform için ayrı ayrı kontrol edebilirsiniz.

Oyun varlıkları `game.arcd` dosyasında bulunur ve LZ4 sıkıştırması kullanılarak ayrı ayrı sıkıştırılır.
[custom_resources](https://defold.com/manuals/project-settings/#custom-resources) ayarını kullanarak, `game.arcd` dosyasına (sıkıştırılarak) yerleştirilmesi gereken varlıkları yapılandırabilirsiniz.
Bu varlıklara [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource) işlevi aracılığıyla erişilebilir.

## Yayıma yönelik paketler ve hata ayıklama paketleri

Bir uygulama dağıtım paketi oluştururken hata ayıklama paketi (debug) veya yayıma yönelik paket (release) oluşturmayı seçebilirsiniz. Bu iki paket arasındaki farklar küçüktür, ancak bunları akılda tutmak önemlidir:

* Yayıma yönelik derlemeler varsayılan olarak [profil çıkarıcıyı (profiler)](/manuals/profiling) içermez. Hem hata ayıklama derlemelerine hem de yayıma yönelik derlemelere profil çıkarıcı desteği eklemek için [uygulama bildiriminde (App Manifest)](/manuals/app-manifest/#profiler) **Profiler** ayarını **Always** olarak ayarlayın.
* Yayıma yönelik derlemeler [ekran kaydediciyi](/ref/stable/sys/#start_record) içermez
* Yayıma yönelik derlemeler, `print()` çağrılarının veya herhangi bir yerel kod eklentisinin çıktısını göstermez
* Yayıma yönelik derlemelerde `is_debug` değeri, `sys.get_engine_info()` içinde `false` olarak ayarlanır
* Yayıma yönelik derlemeler, `hash` değerleri için `tostring()` çağrıldığında ters arama yapmaz. Pratikte bu, `tostring()` işlevinin `url` veya `hash` türündeki bir değer için özgün dize yerine sayısal gösterimi döndürmesi anlamına gelir (`'hash: [/camera_001]'` yerine `'hash: [11844936738040519888 (unknown)]'`)
* Yayıma yönelik derlemeler, [çalışma sırasında yeniden yükleme (hot reload)](/manuals/hot-reload) ve benzer işlevler için düzenleyiciden hedef olarak seçilmeyi desteklemez


