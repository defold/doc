---
title: Usar dependencias de CocoaPods en builds de iOS y macOS
brief: Este manual explica cómo usar CocoaPods para resolver dependencias en builds de iOS y macOS.
---

# CocoaPods

[CocoaPods](https://cocoapods.org/) es un gestor de dependencias para proyectos Cocoa de Swift y Objective-C. CocoaPods se usa normalmente para gestionar e integrar dependencias en proyectos Xcode. Defold no usa Xcode al crear builds para iOS y macOS, pero aun así usa CocoaPods para resolver dependencias en el servidor de build.


## Resolución de dependencias

Las extensiones nativas pueden incluir un archivo `Podfile` en las carpetas `manifests/ios` y `manifests/osx` para especificar las dependencias de la extensión. Ejemplo:

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

El servidor de build recopilará los archivos `Podfile` de todas las extensiones y los usará para resolver todas las dependencias e incluirlas al compilar el código nativo.

Ejemplos:

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)
