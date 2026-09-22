---
title: Utilisation des dépendances CocoaPods dans les builds iOS et macOS
brief: Ce manuel explique comment utiliser CocoaPods pour résoudre les dépendances dans les builds iOS et macOS.
---

# CocoaPods {#cocoapods}

[CocoaPods](https://cocoapods.org/) est un gestionnaire de dépendances pour les projets Cocoa écrits en Swift et en Objective-C. CocoaPods sert généralement à gérer et à intégrer les dépendances dans les projets Xcode. Defold n'utilise pas Xcode pour créer des builds pour iOS et macOS, mais utilise néanmoins CocoaPods pour résoudre les dépendances sur le serveur de build.


## Résolution des dépendances {#resolving-dependencies}

Les extensions natives peuvent inclure un fichier `Podfile` dans les dossiers `manifests/ios` et `manifests/osx` pour spécifier les dépendances de l'extension. Exemple :

```
platform :ios '11.0'

pod 'FirebaseCore', '10.22.0'
pod 'FirebaseInstallations', '10.22.0'
```

Le serveur de build rassemblera les fichiers `Podfile` de toutes les extensions et les utilisera pour résoudre toutes les dépendances et les inclure lors de la compilation du code natif.

Exemples :

* [Firebase](https://github.com/defold/extension-firebase/blob/master/firebase/manifests/ios/Podfile)
* [Facebook](https://github.com/defold/extension-facebook/blob/master/facebook/manifests/ios/Podfile)