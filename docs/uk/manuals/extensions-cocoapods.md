---
title: Використання залежностей CocoaPods у збірках для iOS і macOS
brief: У цьому посібнику пояснено, як використовувати CocoaPods для розв’язання залежностей у збірках для iOS і macOS.
---

# CocoaPods {#cocoapods}

[CocoaPods](https://cocoapods.org/) — це менеджер залежностей для проєктів Cocoa мовами Swift і Objective-C. CocoaPods зазвичай використовують для керування залежностями та їх інтеграції у проєкти Xcode. Defold не використовує Xcode під час збирання для iOS і macOS, але все ж використовує CocoaPods для розв’язання залежностей на сервері збирання.


## Розв’язання залежностей {#resolving-dependencies}

Нативні розширення можуть містити файл `Podfile` у папках `manifests/ios` і `manifests/osx`, щоб указати залежності розширення. Приклад:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Сервер збирання збере файли `Podfile` з усіх розширень і використає їх для розв’язання всіх залежностей та включення їх під час збирання нативного коду.

Приклади:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
