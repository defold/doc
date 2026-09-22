---
title: CocoaPods-Abhängigkeiten in iOS- und macOS-Builds verwenden
brief: Dieses Handbuch erklärt, wie du mit CocoaPods Abhängigkeiten in iOS- und macOS-Builds auflöst.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) ist ein Abhängigkeitsmanager für Cocoa-Projekte in Swift und Objective-C. CocoaPods wird üblicherweise verwendet, um Abhängigkeiten in Xcode-Projekten zu verwalten und einzubinden. Defold verwendet beim Erstellen von Builds für iOS und macOS kein Xcode, nutzt aber dennoch CocoaPods, um Abhängigkeiten auf dem Build-Server aufzulösen.


## Abhängigkeiten auflösen {#resolving-dependencies}

Native Erweiterungen (native extensions) können eine Datei namens `Podfile` in den Ordnern `manifests/ios` und `manifests/osx` enthalten, um die Abhängigkeiten der Erweiterung anzugeben. Beispiel:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Der Build-Server sammelt die `Podfile`-Dateien aller Erweiterungen und verwendet sie, um sämtliche Abhängigkeiten aufzulösen und beim Erstellen des nativen Codes einzubinden.

Beispiele:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
