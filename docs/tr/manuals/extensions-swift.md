---
title: iOS ve macOS için yerel kod eklentilerinde Swift kullanma
brief: Bu kılavuz, iOS ve macOS derlemelerinde bir yerel kod eklentisini Swift ile nasıl yazacağınızı açıklar.
---

# Yerel kod eklentilerinde Swift {#swift-in-native-extensions}

StoreKit 2 ve CryptoKit gibi birçok Apple API'sine yalnızca Swift kodundan erişilebilir. Bir yerel kod eklentisi (native extension), Objective-C++ dosyalarının yanında kendi Swift kaynak dosyalarını da içerebilir. Derleme sunucusu bu dosyaları eklentinin geri kalanıyla birlikte derler ve sonucu motora bağlar. Eklentinin kendi Swift kodunu derlemek, [Swift paketleri](/manuals/extensions-spm) veya [CocoaPods](/manuals/extensions-cocoapods) aracılığıyla hazır bağımlılıklar kullanmaktan ayrı bir işlemdir.

Swift kodu macOS için hem `arm64` hem de `x86_64` mimarisinde, iOS için de hem cihazlarda hem de simülatörde çalışacak şekilde derlenir. Diğer platformlar için yapılan derlemelerde Swift dosyaları yok sayılır.


## Swift kaynak dosyalarını ekleme {#adding-swift-sources}

`.swift` dosyalarını eklentinin `src` klasörüne, C++ ve Objective-C++ dosyalarının yanına yerleştirin.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Tüm Swift dosyalarını `src` klasöründe tutun. `commonsrc` veya `pluginsrc` klasöründe bir Swift dosyası bulunursa macOS veya iOS derlemesi başarısız olur.

Bir eklentinin tüm Swift dosyaları birlikte derlenerek tek bir Swift modülü oluşturur. Modül adı, `ext.manifest` dosyasındaki `name` değerinden türetilir. Harf, rakam veya alt çizgi dışındaki her karakter `_` ile değiştirilir. Örneğin `My-Extension`, `My_Extension` olur. Swift kodu Swift 5 dil modunda derlenir.

Modülün adı, kodun içe aktardığı modüllerin adlarından farklı olmalıdır. Örneğin `StoreKit` adlı bir eklenti `import StoreKit` kullanamaz, çünkü derleyici bu adı eklentinin kendi modülü olarak yorumlar.


## Objective-C++ kodundan Swift kodunu çağırma {#calling-swift-from-objective-c}

Eklentinin giriş noktası yine `DM_DECLARE_EXTENSION` ile kaydedilen bir C++ işlevidir. Bu nedenle eklentide en az bir `.cpp` veya `.mm` dosyası bulunmalıdır. Bu dosyadan Swift kodunu çağırmak için derleme sırasında oluşturulan `<Module>-Swift.h` başlığını kullanın.

Objective-C kodundan yalnızca `@objc` ile işaretlenen sınıflara, protokollere ve yöntemlere erişilebilir. Sınıfları `public` olarak işaretleyin ve `NSObject` sınıfından türetin.

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* Oluşturulan başlık `Foundation` modülünü içe aktarır. Diğer framework'lerdeki türler için bu başlıkta yalnızca ön bildirim bulunur. Bu türleri kullanan yöntemleri çağırmadan önce ilgili framework'ün (örneğin `UIKit`) başlığını `.mm` dosyasında içe aktarın.
* Objective-C kodunda `throws` işlevleri `NSError **` parametresi alan yöntemler, `async` işlevleri ise tamamlanma işleyicisi alan yöntemler olarak görünür.
* Genel tür ve işlevler (generics), ilişkili değer taşıyan numaralandırma türleri ve yapılar gibi Swift'e özgü özelliklere Objective-C kodundan erişilemez. Bunları `@objc` ile işaretlenmiş bir sınıf içinde sarmalayın.
* `.mm` dosyaları yalnızca iOS ve macOS için derlenir. Bu nedenle yalnızca `.mm` ve `.swift` dosyaları içeren bir eklenti diğer platformlarda `Extension has no source!` hatası verir. Eklentiyi diğer platformlar için de derlemek istiyorsanız `DM_DECLARE_EXTENSION` makrosunu bir `.cpp` dosyasına yerleştirin. `.mm` dosyasındaki kodu buradan bir `DM_PLATFORM_IOS` veya `DM_PLATFORM_OSX` derleme koşulu içinde çağırın.


## Swift kodundan Objective-C kodunu çağırma {#calling-objective-c-from-swift}

Swift kodunda Objective-C veya C bildirimlerini kullanmak için `src` klasörüne `<Module>-Bridging-Header.h` adlı bir köprü başlığı (bridging header) ekleyin. Örneğin `src/MyExtension-Bridging-Header.h` dosyası şu satırı içerebilir.

```cpp
#import "mynative.h"
```

Bu başlık varsa Swift modülüne otomatik olarak aktarılır. İçerdiği başlık dosyaları, eklentinin `include` klasöründe ve aşağıda açıklanan `additionalSwiftIncludePaths` ile belirtilen klasörlerde aranır.

`Foundation`, `UIKit` ve `StoreKit` gibi Apple framework'lerini Swift kodunda normal bir `import` deyimiyle içe aktarabilirsiniz. `ext.manifest` dosyasının `frameworks` ve `weakFrameworks` alanlarında listelenen framework'ler her zamanki gibi bağlanır. Swift kodunun içe aktardığı sistem framework'lerinin çoğu otomatik olarak bağlanır.


## Swift kodunda Swift paketlerini kullanma {#using-swift-packages-from-swift}

Eklenti, `SwiftPackages.json` dosyasında bildirdiği [Swift paketlerinin](/manuals/extensions-spm) ürünlerini kendi Swift kodunda kullanabilir. Modülü bir Swift dosyasında içe aktarın.

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

Bir paketin Objective-C başlıklarını, `.mm` dosyasında yaptığınız gibi köprü başlığında da içe aktarabilirsiniz.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Paketi, onu kullanan eklentinin `SwiftPackages.json` dosyasında bildirin. Derleme sunucusu önce paketleri, ardından eklentinin Swift kodunu derler. Paketin gerektirdiği işletim sistemi sürümü motorun desteklediği en düşük sürümden yeniyse bu sürümü `SwiftPackages.json` dosyasında `minVersion` olarak belirtin. Böylece eklentinin Swift kodu da bu sürüm için derlenir. CocoaPods bağımlılıklarının Swift kodundan kullanımı desteklenmez. Bu bağımlılıkları Objective-C++ dosyasında kullanın ve gerekenleri Swift koduna aktarın.


## Derleyici seçenekleri {#compiler-options}

Swift derleyicisinin seçeneklerini `ext.manifest` dosyasında, C++ derleyicisinin seçenekleriyle aynı `context` bölümünde ayarlayın.

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - C++ için ayarlanan tanımlar Swift'e koşullu derlemede kullanılacak adlar olarak aktarılır. Bu sayede `#if MY_DEFINE` Swift kodunda da çalışır. Swift yalnızca adları desteklediği için `MY_DEFINE=1` gibi bir tanımın değeri aktarılmaz.
* `swiftFlags` - Swift derleyicisinin ek bayrakları. Her bayrak ve her değer ayrı bir liste öğesidir. İzin listesinin dışındaki bayraklar derlemenin `Invalid flag - 'swiftFlags'` hatasıyla başarısız olmasına neden olur. Boşluk karakteri, ters eğik çizgi veya şablon sözdizimi içeren ya da bir yanıt dosyasını belirten bir değer ise `invalid 'swiftFlags' value` hatasına yol açar. Aşağıdaki bayraklara izin verilir.
  * `-enable-upcoming-feature <Feature>` - Dilin gelecek bir sürümünde sunulacak bir özelliği etkinleştirir. Örneğin `["-enable-upcoming-feature", "ExistentialAny"]` kullanabilirsiniz.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` ve `-Onone` - Optimizasyon düzeyini belirler. Varsayılan değer `-O` seçeneğidir.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Swift derleyicisinin başlık dosyalarını ve modülleri ararken eklentinin `include` klasörüne ek olarak bakacağı klasörler.
* `additionalFrameworkSearchPaths` - Eklentinin `lib/<platform>` klasörüne ek olarak framework'lerin aranacağı klasörler. Bunları Swift derleyicisi, eklentinin kaynak dosyalarını derleyen C++ ve Objective-C++ derleyicisi ve bağlayıcı kullanır.

Yollar eklenti klasörüne göre belirtilir. Yollar bu klasörün dışına çıkamaz ve yalnızca harf, rakam ve `._+-/` karakterlerini içerebilir. Derleme sunucusuna eklentinin yalnızca `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` ve `res/<platform>` klasörleri gönderilir. Bu nedenle yollar bu klasörlerden birinin içinde kalmalıdır. Eklentinin kök dizinindeki bir `vendor` klasörü gibi başka klasörlerde yer alan dosyalara derleme sırasında erişilemez.

`ios` platformunun Swift anahtarları hem cihazlar hem de simülatör için geçerlidir. Swift desteğinden önceki bir derleme sunucusu bu anahtarları `Manifest context variable unsupported` hatasıyla reddeder. Bu durumda Defold sürümü ve derleme sunucusu güncellenene kadar proje derlenemez.


## En düşük işletim sistemi sürümleri {#minimum-os-versions}

Swift çalışma zamanı ortamı, Defold'un desteklediği tüm iOS ve macOS sürümlerinin bir parçasıdır. Swift kodu, derlemenin hedeflediği en düşük iOS veya macOS sürümü için derlenir. Uygulama, işletim sistemindeki Swift çalışma zamanı ortamını kullanır. En düşük sürümden daha yeni bir sürümde sunulan API'leri çağırmadan önce `#available` ile sürümü kontrol edin.

Çalışma zamanı ortamının bazı bölümleri, işletim sisteminin ancak daha yeni sürümlerinde bulunur. Örneğin `MutableSpan` ve ilgili türler iOS 26 ve macOS 26 ile birlikte gelir. Hedeflenen en düşük sürüm daha eskiyse ve Swift kodunuz veya bir pakete ait dinamik framework bu tür bir özelliği kullanıyorsa uygulamanın o cihazlarda çalışması için ek bir kütüphane gerekebilir. Bunun için bir işlem yapmanız gerekmez. Derleme sunucusu, Xcode gibi, motorun ve motorla birlikte uygulamaya gömülen dinamik kütüphanelerin kullandığı kütüphaneleri bulup uygulamaya ekler. iOS'ta bu kütüphaneler uygulamanın `Frameworks` klasörüne yerleştirilir ve uygulama kodunun geri kalanıyla birlikte imzalanır.

Bir derlemenin hedeflediği en düşük işletim sistemi sürümü, motorun desteklediği en düşük sürümdür. Bunu Defold sürümü ve derleme sunucusu belirler. [Swift Package Manager kılavuzunda](/manuals/extensions-spm) açıklandığı gibi `SwiftPackages.json` dosyasındaki `minVersion` değeriyle paketler, Swift kodu ve motorun bağlama aşaması için bu alt sınırı yükseltebilirsiniz. Alt sınır düşürülemez.


## Sınırlamalar {#limitations}

* Swift kullanan eklentilerde de `DM_DECLARE_EXTENSION` içeren bir C++ veya Objective-C++ dosyası bulunmalıdır. Eklenti Swift kodundan kaydedilemez. Defold yazılım geliştirme kitinin (SDK, `dmsdk`) C++ API'sine Swift kodundan erişilemediği için bu API'yi Objective-C++ dosyasından çağırın. `dmsdk/dlib/hash.h` gibi C ile uyumlu `dmsdk` başlıklarını köprü başlığına dahil edebilirsiniz. Eklenti yalnızca `.swift` dosyaları içeriyorsa bağlayıcı, eklentinin adını taşıyan simgeyi bulamaz ve tanımsız simge hatası verir.
* CocoaPods bağımlılıklarının Swift kodundan kullanımı desteklenmez. Bu bağımlılıkları Objective-C++ dosyasında kullanın ve gerekenleri Swift koduna aktarın.
* Yalnızca Swift 5 dil modu desteklenir. C++ ile birlikte çalışabilirlik etkin değildir.
* Swift kaynak dosyaları Defold 1.14.2 sürümünden itibaren desteklenir. Daha eski bir SDK kullanan derleme sunucusunda derleme `Swift sources are not supported by this Defold SDK version` hatasıyla başarısız olur.
* `library` çıktısı oluşturulurken ([Bob](/manuals/bob) aracında `--build-artifacts library`) Swift kaynak dosyaları derlenmez. Bu nedenle `<Module>-Swift.h` başlığını içe aktaran bir Objective-C++ dosyası bu derlemede hata verir.


## Sorun giderme {#troubleshooting}

`no such module 'Name'`
: Modül, bir `SwiftPackages.json` dosyasında bildirilen bir paketin ürünü değildir. [Swift Package Manager kılavuzunda](/manuals/extensions-spm) açıklandığı gibi `products` listesinde modülü sağlayan bir ürün bulunduğunu kontrol edin.

`Swift sources are only supported in the 'src' folder`
: `.swift` dosyalarını eklentinin `src` klasörüne taşıyın.

`'MyExtension-Swift.h' file not found`
: Modül adı `ext.manifest` dosyasındaki `name` değerinden türetilir. `#import` satırındaki adı kontrol edin.

`unknown type name 'MyExtensionGreeter'`
: Oluşturulan başlıkta sınıfın bildirimi eksiktir. Sınıfın `public` ve `@objc` olarak işaretlendiğini, `NSObject` sınıfından türetildiğini ve `.mm` dosyasında `@objc(...)` ile belirtilen adın kullanıldığını kontrol edin.

`cannot find 'AppStore' in scope` ile birlikte `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: Eklenti, içe aktardığı bir modülle aynı adı taşıyor. `ext.manifest` dosyasında eklentinin adını değiştirin.

`Undefined symbols ... _MyExtension`
: Eklentide `DM_DECLARE_EXTENSION` eksik. Yukarıda açıklandığı gibi eklentiyi kaydeden bir `.mm` dosyası ekleyin.

`Invalid flag - 'swiftFlags'`
: Bayrak izin listesinde yok. Bayrağı kaldırın veya listedeki bayraklardan birini kullanın.

`invalid 'swiftFlags' value`
: Değer boşluk karakteri, ters eğik çizgi veya şablon sözdizimi içeriyor ya da bir yanıt dosyasını belirtiyor. Her bayrağı ve her değeri ayrı bir liste öğesine yerleştirin.
