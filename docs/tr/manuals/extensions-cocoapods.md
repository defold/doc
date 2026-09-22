---
title: iOS ve macOS derlemelerinde CocoaPods bağımlılıklarını kullanma
brief: Bu kılavuz, iOS ve macOS derlemelerinde bağımlılıkları çözümlemek için CocoaPods'un nasıl kullanılacağını açıklar.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/), Swift ve Objective-C ile geliştirilen Cocoa projeleri için bir bağımlılık yöneticisidir. CocoaPods genellikle Xcode projelerindeki bağımlılıkları yönetmek ve projeye dahil etmek için kullanılır. Defold, iOS ve macOS için derleme yaparken Xcode kullanmaz, ancak derleme sunucusundaki bağımlılıkları çözümlemek için yine de CocoaPods kullanır.


## Bağımlılıkları çözümleme

Yerel kod eklentileri (native extension), eklenti bağımlılıklarını belirtmek için `manifests/ios` ve `manifests/osx` klasörlerinde bir `Podfile` dosyası içerebilir. Örnek:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Derleme sunucusu, tüm eklentilerdeki `Podfile` dosyalarını toplar ve bu dosyaları kullanarak tüm bağımlılıkları çözümler ve yerel kodu derlerken bunları dahil eder.

Örnekler:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)