---
title: Używanie zależności CocoaPods w kompilacjach na iOS i macOS
brief: Ta instrukcja wyjaśnia, jak używać CocoaPods do rozwiązywania zależności w kompilacjach na iOS i macOS.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) to menedżer zależności dla projektów Cocoa w Swift i Objective-C. CocoaPods jest zwykle używany do zarządzania zależnościami i integrowania ich w projektach Xcode. Defold nie używa Xcode podczas budowania na iOS i macOS, ale nadal używa CocoaPods do rozwiązywania zależności na serwerze buildów.


## Rozwiązywanie zależności

Rozszerzenia natywne mogą zawierać plik `Podfile` w folderach `manifests/ios` i `manifests/osx`, aby określić zależności rozszerzenia. Przykład:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Serwer buildów zbierze pliki `Podfile` ze wszystkich rozszerzeń i użyje ich do rozwiązania wszystkich zależności oraz dołączenia ich podczas budowania kodu natywnego.

Przykłady:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
