---
title: iOS ve macOS derlemelerinde Swift Package Manager bağımlılıklarını kullanma
brief: Bu kılavuz, iOS ve macOS derlemelerinde bağımlılıkları çözümlemek için Swift Package Manager kullanımını açıklar.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/), Swift ve Xcode'un yerleşik bağımlılık yöneticisidir. Birçok iOS ve macOS SDK'sı Swift paketi olarak dağıtılır; bazıları artık CocoaPods olarak yayımlanmaz. Defold motoru derlerken Xcode kullanmaz, ancak derleme sunucusu bir eklentinin bağımlı olduğu Swift paketlerini indirmek ve derlemek için Xcode kullanır. Sonuç, [CocoaPods bağımlılıklarıyla](/manuals/extensions-cocoapods) aynı şekilde motora bağlanır.

CocoaPods ve Swift paketleri aynı projede, hatta aynı eklentide kullanılabilir.


## Bağımlılıkları bildirme {#declaring-dependencies}

Yerel kod eklentileri (native extension), bağımlı oldukları Swift paketlerini belirtmek için `manifests/ios` ve `manifests/osx` klasörlerinde bir `SwiftPackages.json` dosyası içerebilir. Örnek:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/firebase/firebase-ios-sdk.git",
      "version": "12.16.0",
      "products": ["FirebaseCore", "FirebaseInstallations"]
    }
  ]
}
```

Dosya düz JSON biçimindedir. `Package.swift` dosyasını kendiniz yazmazsınız; derleme sunucusu bunu tüm eklentilerin `SwiftPackages.json` dosyalarından oluşturur.

Dosya şu alanları içerir:

* `platform` - Zorunlu. `manifests/ios/SwiftPackages.json` içinde `"ios"`, `manifests/osx/SwiftPackages.json` içinde `"osx"`.
* `minVersion` - İsteğe bağlı. Paketlerin hedeflediği en düşük iOS veya macOS sürümü; örneğin `"15.0"`. Hem paketler derlenirken hem de motor bağlanırken tüm eklentilerin değerleri ve motorun desteklediği en düşük sürüm arasından en yüksek değer kullanılır.
* `wrapperType` - İsteğe bağlı. `"static"` (varsayılan) veya `"dynamic"`. Aşağıdaki [Statik ve dinamik bağlama](#static-and-dynamic-linking) bölümüne bakın.
* `packages` - Zorunlu. Paket listesi. Her paket şu alanları içerir:
  * `url` - Paketin Git deposunun `https://` URL adresi. Kimlik bilgileri, özel bağlantı noktası veya sorgu dizesi içeren URL adresleri ve `ssh` URL adresleri kabul edilmez; bu nedenle depo herkese açık olmalıdır.
  * `products` - Paketin motora bağlanacak ürünleri. Bunlar, paketin `Package.swift` dosyasının `products` bölümünde listelenen kütüphane ürünleridir. Ürün adı, paketin adıyla veya içe aktardığınız modülün adıyla aynı olmak zorunda değildir.
  * Tam olarak bir sürüm gereksinimi:
    * `version` - Tam olarak bu sürüm; örneğin `"12.16.0"`.
    * `from` - Bu sürüm veya aynı ana sürüme sahip daha yeni bir sürüm. Örneğin `"9.0.0"`, en yeni `9.x.x` sürümüne çözümlenir.
    * `branch` - Bir daldaki en son Git kaydı (commit); örneğin `"main"`.
    * `revision` - Tam 40 karakterlik Git kaydı karma değeriyle belirtilen belirli bir kayıt.

Derleme sunucusu, tüm eklentilerin `SwiftPackages.json` dosyalarını toplar; paketlerin kendi bağımlılıkları dahil tüm bağımlılıkları bunlarla çözümler ve yerel kodu derlerken dahil eder.


## Paketleri eklenti kodundan kullanma {#using-packages-from-extension-code}

Ürünlerin başlık dosyaları eklentinin kaynak kodunda kullanılabilir. Bunları Objective-C++ (`.mm`) kaynak dosyalarından kullanın. Bu örnek, uygulama başladığında [Sentry](https://github.com/getsentry/sentry-cocoa) SDK'sını başlatır:

`manifests/ios/SwiftPackages.json`:

```json
{
  "platform": "ios",
  "minVersion": "15.0",
  "packages": [
    {
      "url": "https://github.com/getsentry/sentry-cocoa.git",
      "from": "9.0.0",
      "products": ["Sentry"]
    }
  ]
}
```

`src/myextension.mm`:

```cpp
#include <dmsdk/sdk.h>

#if defined(DM_PLATFORM_IOS)
#import <UIKit/UIKit.h>
#import <Sentry/Sentry.h>
#import <Sentry/Sentry-Swift.h>
#endif

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
#if defined(DM_PLATFORM_IOS)
    [SentrySDK startWithConfigureOptions:^(SentryOptions* options) {
        options.dsn = @"https://examplePublicKey@o0.ingest.sentry.io/0";
    }];
#endif
    return dmExtension::RESULT_OK;
}
```

* Objective-C başlıkları `#import <Module/Header.h>` biçiminde içe aktarılır; burada `Module`, bunları sağlayan modülün adıdır.
* Swift ile uygulanan sınıflar, oluşturulan `<Module/Module-Swift.h>` başlığında bildirilir. Bu başlık yalnızca modülün Objective-C'ye sunduğu (Swift'te `@objc` olarak işaretlenmiş) sınıf ve yöntemleri içerir. Oluşturulan başlık bunların türlerini kullandığı için önce `UIKit` (veya macOS'ta `AppKit`) içe aktarın.


## Birden çok eklentinin bağımlılıkları {#dependencies-of-several-extensions}

Bir projedeki birden çok eklenti Swift paketleri kullandığında platforma ait tüm `SwiftPackages.json` dosyaları tek bir paket grafiğinde birleştirilir:

* Aynı URL adresine sahip paketler birleştirilir ve istenen ürünler bir araya getirilir.
* Birden çok eklentinin paylaştığı bir paketin sürüm gereksinimi hepsinde aynı olmalıdır. Örneğin bir eklentide `"version": "12.16.0"`, diğerinde `"from": "12.0.0"` gibi farklı gereksinimler, derlemenin `Conflicting requirements for Swift package` hatasıyla başarısız olmasına yol açar.
* En yüksek `minVersion` kullanılır.
* `wrapperType` ayarlayan tüm eklentiler aynı değeri ayarlamalıdır.

Bir projede CocoaPods kullanan eklentilerle Swift paketleri kullanan eklentiler birlikte de bulunabilir. Her ikisi de çözümlenir ve motora bağlanır. Ancak aynı SDK iki kaynaktan birden gelmemelidir: bir eklenti Firebase'i `Podfile` dosyasından, diğeri `SwiftPackages.json` dosyasından alırsa motor yinelenen simge hatalarıyla bağlanamaz. Bir SDK'yı paylaşan eklentilerin aynı bağımlılık yöneticisini kullanması önerilir.


## Paket sürümlerini sabitleme {#locking-package-versions}

Derleme başarılı olduğunda derleme sunucusu, paketlerin bağımlılıkları dahil grafikteki her paketin tam sürümünü ve Git kaydını listeleyen bir `Package.resolved` dosyası döndürür. Dosya, projenin derleme klasörüne; örneğin `build/arm64-ios/Package.resolved` konumuna yerleştirilir.

Paket sürümlerini sabitlemek için bu dosyayı eklentiye, `SwiftPackages.json` dosyasının yanına kopyalayın (örneğin `manifests/ios/Package.resolved`). Derleme sunucusu, `SwiftPackages.json` gereksinimleriyle eşleştikleri sürece sabitlenmiş sürümleri kullanır. Bu, derlemeyi de hızlandırır: `Package.resolved` olmadan derleme sunucusu paket bağımlılıklarını adım adım keşfeder; bu, çok bağımlılığı olan paketlerde uzun sürebilir.

Birden çok eklenti aynı platform için `Package.resolved` içeriyorsa bunlardan yalnızca biri kullanılır.


## Statik ve dinamik bağlama {#static-and-dynamic-linking}

Varsayılan olarak tüm Swift paketleri, motorun yürütülebilir dosyasına bağlanan tek bir statik kütüphanede birleştirilir.

Bazı SDK'lar statik kütüphanede birleştirilemez ve bu durumda motor yinelenen simge hatalarıyla bağlanamaz. Böyle bir durumda `SwiftPackages.json` içinde `"wrapperType": "dynamic"` ayarlayın. Paketler, uygulama dağıtım paketine gömülen dinamik bir framework olarak derlenir.


## Kaynaklar ve gizlilik bildirimleri {#resources-and-privacy-manifests}

Paketlerin kaynak paketleri ve gizlilik bildirimleri (`PrivacyInfo.xcprivacy`), CocoaPods bağımlılıklarında olduğu gibi uygulama dağıtım paketine dahil edilir.


## CocoaPods'tan geçiş {#migrating-from-cocoapods}

Birçok SDK hem pod hem de Swift paketi olarak yayımlanır. Bir eklentiyi `Podfile` dosyasından `SwiftPackages.json` dosyasına taşımak için:

1. SDK belgelerinde Swift paketinin Git deposunu bulun. Bu genellikle pod ile aynı depodur.
2. Paketin `Package.swift` dosyasında ürün adlarını bulun. Pod adları ve ürün adları genellikle farklıdır.
3. `Podfile` yerine bir `SwiftPackages.json` dosyası koyun. `Podfile` içindeki `platform :ios` sürümü `minVersion` olur.
4. Eklentinin `#import` satırlarının ürünlerin modül adlarıyla hâlâ eşleştiğinden emin olun.

Örneğin şu `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

şu `SwiftPackages.json` dosyasına dönüşür:

```json
{
  "platform": "ios",
  "minVersion": "12.0",
  "packages": [
    {
      "url": "https://github.com/facebook/facebook-ios-sdk.git",
      "version": "17.0.0",
      "products": ["FacebookCore", "FacebookLogin", "FacebookShare", "FacebookGamingServices"]
    }
  ]
}
```

Bu durumda modül adları aynı kalır; dolayısıyla `#import <FBSDKCoreKit/FBSDKCoreKit.h>` her ikisiyle de çalışır.


## Sınırlamalar {#limitations}

* Yalnızca `https://` üzerinden herkese açık olan paket depoları desteklenir. Swift paket kayıt hizmetleri desteklenmez.
* Paketlerin `Package.swift` dosyaları ve eklentileri, derleme sunucusunda ağ erişimi olmadan çalışır. Derleme sunucusu, paketler derlenmeden önce paketleri ve ikili framework'lerini kendisi indirir.
* iOS için varlık katalogları (`.xcassets`) içeren paketleri derlemek, Xcode 27 veya sonrasını kullanan bir derleme sunucusu gerektirir. Xcode'un önceki bir sürümünde derleme, bu paketlerin adlarını belirten bir hatayla başarısız olur.
* Bir projenin `SwiftPackages.json` dosyaları, platform başına en fazla 32 paket ve 64 ürün bildirebilir.


## Sorun giderme {#troubleshooting}

`'Module/Header.h' file not found` veya tanımsız simgeler
: `SwiftPackages.json` içindeki `products` değerlerinin `Package.swift` dosyasındaki ürün adları olduğunu ve başlığın bunlardan birine ait olduğunu kontrol edin. Swift Package Manager desteklemeyen bir derleme sunucusu `SwiftPackages.json` dosyasını yok sayar; bu durumda eklenti aynı şekilde derlenemez veya bağlanamaz.

`The Swift package graph did not resolve within the ... time budget`
: Paketler, kilit dosyası olmadan keşfedilemeyecek kadar çok bağımlılığa sahiptir. [Paket sürümlerini sabitleme](#locking-package-versions) bölümünde açıklandığı gibi `SwiftPackages.json` yanına bir `Package.resolved` dosyası ekleyin. Derleme tamamlanmadığı için dosyayı yerel olarak, örneğin aynı paketleri bir Xcode projesine ekleyerek oluşturun. Xcode dosyayı `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved` konumunda saklar.


## Yerel derleme sunucusu {#local-build-server}

Swift paketleri macOS derleme sunucusunda derlenir. [Yerel derleme sunucusuyla](/manuals/extender-local-setup) Swift paketleri kullanmak için sunucuda tam bir Xcode kurulumu (yalnızca Command Line Tools yeterli değildir), [XcodeGen](https://github.com/yonaskolb/XcodeGen) ve `extender.spm.enabled` ayarıyla etkinleştirilmiş Swift Package Manager desteği gerekir. Daha fazla bilgi için [GitHub'daki derleme sunucusu belgelerine](https://github.com/defold/extender) başvurun.
