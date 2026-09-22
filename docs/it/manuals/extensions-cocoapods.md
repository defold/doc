---
title: Usare le dipendenze CocoaPods nelle build per iOS e macOS
brief: Questo manuale spiega come usare CocoaPods per risolvere le dipendenze nelle build per iOS e macOS.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) è un gestore di dipendenze per progetti Cocoa in Swift e Objective-C. CocoaPods viene generalmente usato per gestire e integrare le dipendenze nei progetti Xcode. Defold non usa Xcode per creare le build per iOS e macOS, ma usa comunque CocoaPods per risolvere le dipendenze sul server di build.


## Risoluzione delle dipendenze {#resolving-dependencies}

Le estensioni native possono includere un file `Podfile` nelle cartelle `manifests/ios` e `manifests/osx` per specificare le dipendenze dell'estensione. Esempio:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Il server di build raccoglie i file `Podfile` di tutte le estensioni e li usa per risolvere tutte le dipendenze e includerle durante la compilazione del codice nativo.

Esempi:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
