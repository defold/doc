---
title: macOS platformu için Defold geliştirme
brief: Bu kılavuz, macOS üzerinde Defold uygulamalarının nasıl derlenip çalıştırılacağını açıklar
---

# macOS için geliştirme

macOS platformu için Defold uygulamaları geliştirmek, dikkate alınması gereken çok az nokta içeren basit bir süreçtir.

## Proje ayarları

macOS'a özgü uygulama yapılandırması, *game.project* ayar dosyasının [macOS bölümünden](/manuals/project-settings/#macos) yapılır.

## Uygulama simgesi

Bir macOS oyununda kullanılan uygulama simgesi .`icns` biçiminde olmalıdır. Bir `.iconset` içinde toplanan `.png` dosyalarından kolayca bir `.icns` dosyası oluşturabilirsiniz. [`.icns` dosyası oluşturmaya yönelik resmî yönergeleri](https://developer.apple.com/library/archive/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html) izleyin. Gerekli adımların kısa özeti şöyledir:

* Simgeler için bir klasör oluşturun, örneğin `game.iconset`
* Simge dosyalarını oluşturduğunuz klasöre kopyalayın:

    * `icon_16x16.png`
    * `icon_16x16@2x.png`
    * `icon_32x32.png`
    * `icon_32x32@2x.png`
    * `icon_128x128.png`
    * `icon_128x128@2x.png`
    * `icon_256x256.png`
    * `icon_256x256@2x.png`
    * `icon_512x512.png`
    * `icon_512x512@2x.png`

* `iconutil` komut satırı aracını kullanarak `.iconset` klasörünü bir `.icns` dosyasına dönüştürün:

```
iconutil -c icns -o game.icns game.iconset
```

## Uygulamanızı yayımlama
Uygulamanızı Mac App Store'da, Steam veya itch.io gibi üçüncü taraf bir mağaza ya da portalda veya kendi web siteniz üzerinden yayımlayabilirsiniz. Uygulamanızı yayımlamadan önce gönderime hazırlamanız gerekir. Uygulamayı nasıl dağıtmayı planladığınızdan bağımsız olarak aşağıdaki adımlar gereklidir:

1. Çalıştırma izinlerini ekleyerek herkesin oyununuzu çalıştırabilmesini sağlayın (varsayılan olarak yalnızca dosya sahibinin çalıştırma izni vardır):

```
$ chmod +x Game.app/Contents/MacOS/Game
```

2. Oyununuzun gerektirdiği izinleri belirten bir yetki (entitlement) dosyası oluşturun. Çoğu oyun için aşağıdaki izinler yeterlidir:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
  </dict>
</plist>
```

  * `com.apple.security.cs.allow-jit` - Uygulamanın MAP_JIT bayrağını kullanarak yazılabilir ve yürütülebilir bellek oluşturmasına izin verilip verilmediğini belirtir
  * `com.apple.security.cs.allow-unsigned-executable-memory` - Uygulamanın MAP_JIT bayrağının kullanımından kaynaklanan kısıtlamalar olmadan yazılabilir ve yürütülebilir bellek oluşturmasına izin verilip verilmediğini belirtir
  * `com.apple.security.cs.allow-dyld-environment-variables` - Uygulamanın, uygulama sürecine kod eklemek için kullanabileceğiniz dinamik bağlayıcı ortam değişkenlerinden etkilenmesine izin verilip verilmediğini belirtir

Bazı uygulamalar ek yetkilere de ihtiyaç duyabilir. Steamworks eklentisi şu ek yetkiyi gerektirir:

```
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

  * `com.apple.security.cs.disable-library-validation` - Uygulamanın kod imzalama gerektirmeden herhangi bir eklenti veya yazılım çatısı yüklemesine izin verilip verilmediğini belirtir.

Bir uygulamaya verilebilecek tüm yetkiler, resmî [Apple geliştirici belgelerinde](https://developer.apple.com/documentation/bundleresources/entitlements) listelenmiştir.

3. Oyununuzu `codesign` kullanarak imzalayın:

```
$ codesign --force --sign "Developer ID Application: Company Name" --options runtime --deep --timestamp --entitlements entitlement.plist Game.app
```

## Mac App Store dışında yayımlama
Apple, Mac App Store dışında dağıtılan tüm yazılımların macOS Catalina'da varsayılan olarak çalışabilmesi için Apple tarafından onaylanmasını (notarization) zorunlu tutar. Xcode dışında, betiklerle yürütülen bir derleme ortamına onay sürecini nasıl ekleyeceğinizi öğrenmek için [resmî belgelere](https://developer.apple.com/documentation/xcode/notarizing_macos_software_before_distribution/customizing_the_notarization_workflow) bakın. Gerekli adımların kısa özeti şöyledir:

1. İzinleri eklemek ve uygulamayı imzalamak için yukarıdaki adımları izleyin.

2. Oyununuzu ZIP arşivine sıkıştırın ve `altool` kullanarak onay için yükleyin.

```
$ xcrun altool --notarize-app
               --primary-bundle-id "com.acme.foobar"
               --username "AC_USERNAME"
               --password "@keychain:AC_PASSWORD"
               --asc-provider <ProviderShortname>
               --file Game.zip

altool[16765:378423] No errors uploading 'Game.zip'.
RequestUUID = 2EFE2717-52EF-43A5-96DC-0797E4CA1041
```

3. `altool --notarize-app` çağrısının döndürdüğü istek UUID değerini kullanarak gönderiminizin durumunu kontrol edin:

```
$ xcrun altool --notarization-info 2EFE2717-52EF-43A5-96DC-0797E4CA1041
               -u "AC_USERNAME"
```

4. Durum `success` olana kadar bekleyin ve onay biletini oyuna iliştirin:

```
$ xcrun stapler staple "Game.app"
```

5. Oyununuz artık dağıtıma hazırdır.

## Mac App Store'da yayımlama
Mac App Store'da yayımlama süreci [Apple geliştirici belgelerinde](https://developer.apple.com/macos/submit/) ayrıntılı olarak açıklanmıştır. Göndermeden önce yukarıda açıklandığı gibi izinleri eklediğinizden ve uygulamayı `codesign` ile imzaladığınızdan emin olun.

Not: Mac App Store'da yayımlarken oyunun Apple'ın onay (notarization) sürecinden geçmesi gerekmez.

:[Apple Privacy Manifest](../shared/apple-privacy-manifest.md)
