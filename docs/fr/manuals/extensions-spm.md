---
title: Utilisation des dépendances Swift Package Manager dans les builds iOS et macOS
brief: Ce manuel explique comment utiliser Swift Package Manager pour résoudre les dépendances des builds iOS et macOS.
---

# Swift Package Manager {#swift-package-manager}

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) est le gestionnaire de dépendances intégré à Swift et Xcode. De nombreux SDK iOS et macOS sont distribués sous forme de paquets Swift, et certains ne sont plus publiés sous forme de CocoaPods. Defold n'utilise pas Xcode pour compiler le moteur, mais le serveur de build utilise Xcode pour télécharger et compiler les paquets Swift dont dépend une extension. Le résultat est ensuite lié au moteur de la même manière que les [dépendances CocoaPods](/manuals/extensions-cocoapods).

CocoaPods et les paquets Swift peuvent être utilisés dans le même projet, et même dans la même extension.


## Déclarer les dépendances {#declaring-dependencies}

Les extensions natives peuvent inclure un fichier `SwiftPackages.json` dans les dossiers `manifests/ios` et `manifests/osx` pour spécifier les paquets Swift dont elles dépendent. Exemple :

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

Ce fichier est en JSON standard. Vous n'écrivez pas vous-même de fichier `Package.swift` : le serveur de build en génère un à partir des fichiers `SwiftPackages.json` de toutes les extensions.

Le fichier contient les champs suivants :

* `platform` - Obligatoire. `"ios"` dans `manifests/ios/SwiftPackages.json` et `"osx"` dans `manifests/osx/SwiftPackages.json`.
* `minVersion` - Facultatif. Version minimale d'iOS ou macOS pour laquelle les paquets sont compilés, par exemple `"15.0"`. La valeur la plus élevée parmi toutes les extensions et la version minimale prise en charge par le moteur est utilisée, aussi bien pour compiler les paquets que pour effectuer l'édition de liens du moteur.
* `wrapperType` - Facultatif. `"static"` (par défaut) ou `"dynamic"`. Consultez [Liaison statique et dynamique](#static-and-dynamic-linking) ci-dessous.
* `packages` - Obligatoire. Liste de paquets. Chaque paquet comporte les champs suivants :
  * `url` - URL `https://` du dépôt git du paquet. Les URL contenant des identifiants, un port personnalisé ou une chaîne de requête, ainsi que les URL `ssh`, ne sont pas acceptées ; le dépôt doit donc être accessible publiquement.
  * `products` - Produits du paquet à lier au moteur. Il s'agit des produits de bibliothèque répertoriés dans la section `products` du fichier `Package.swift` du paquet. Un nom de produit n'est pas nécessairement identique au nom du paquet ou du module que vous importez.
  * Exactement une exigence de version :
    * `version` - Cette version exacte, par exemple `"12.16.0"`.
    * `from` - Cette version ou toute version ultérieure ayant la même version majeure. Par exemple, `"9.0.0"` est résolu vers la dernière version `9.x.x`.
    * `branch` - Le dernier commit d'une branche, par exemple `"main"`.
    * `revision` - Un commit précis, indiqué par son hachage complet de 40 caractères.

Le serveur de build rassemble les fichiers `SwiftPackages.json` de toutes les extensions pour résoudre l'ensemble des dépendances, y compris celles des paquets eux-mêmes, et les inclut lors de la compilation du code natif.


## Utiliser les paquets depuis le code d'une extension {#using-packages-from-extension-code}

Les en-têtes des produits sont accessibles au code source de l'extension. Utilisez-les depuis des fichiers source Objective-C++ (`.mm`). Cet exemple démarre le SDK [Sentry](https://github.com/getsentry/sentry-cocoa) au lancement de l'application :

`manifests/ios/SwiftPackages.json` :

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

`src/myextension.mm` :

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

* Les en-têtes Objective-C sont importés avec `#import <Module/Header.h>`, où `Module` est le nom du module qui les fournit.
* Les classes implémentées en Swift sont déclarées dans l'en-tête généré `<Module/Module-Swift.h>`. Celui-ci ne contient que les classes et méthodes que le module expose à Objective-C (marquées `@objc` en Swift). Importez `UIKit` (ou `AppKit` sur macOS) avant cet en-tête, car il utilise leurs types.


## Dépendances de plusieurs extensions {#dependencies-of-several-extensions}

Lorsque plusieurs extensions d'un projet utilisent des paquets Swift, tous leurs fichiers `SwiftPackages.json` pour la plateforme sont combinés en un seul graphe de paquets :

* Les paquets ayant la même URL sont fusionnés, et les produits demandés sont réunis.
* Un paquet partagé par plusieurs extensions doit avoir la même exigence de version dans chacune d'elles. Des exigences différentes, par exemple `"version": "12.16.0"` dans une extension et `"from": "12.0.0"` dans une autre, font échouer le build avec une erreur `Conflicting requirements for Swift package`.
* La valeur `minVersion` la plus élevée est utilisée.
* Toutes les extensions qui définissent `wrapperType` doivent choisir la même valeur.

Un projet peut également mélanger des extensions utilisant CocoaPods et des extensions utilisant des paquets Swift. Les deux sont résolus et liés au moteur. Un même SDK ne doit toutefois pas provenir des deux sources : si une extension obtient Firebase depuis un `Podfile` et une autre depuis un `SwiftPackages.json`, l'édition de liens du moteur échoue à cause de symboles en double. Les extensions partageant un SDK devraient utiliser le même gestionnaire de dépendances.


## Verrouiller les versions des paquets {#locking-package-versions}

Lorsque le build réussit, le serveur renvoie un fichier `Package.resolved` indiquant la version et le commit exacts de chaque paquet du graphe, y compris les dépendances des paquets. Ce fichier est placé dans le dossier de build du projet, par exemple `build/arm64-ios/Package.resolved`.

Copiez-le dans l'extension, à côté de `SwiftPackages.json` (par exemple `manifests/ios/Package.resolved`), pour verrouiller les versions des paquets. Le serveur de build utilise alors les versions verrouillées tant qu'elles respectent les exigences de `SwiftPackages.json`. Cela accélère aussi le build : sans fichier `Package.resolved`, le serveur découvre progressivement les dépendances des paquets, ce qui peut prendre beaucoup de temps pour ceux qui en ont de nombreuses.

Si plusieurs extensions incluent un fichier `Package.resolved` pour la même plateforme, un seul de ces fichiers est utilisé.


## Liaison statique et dynamique {#static-and-dynamic-linking}

Par défaut, tous les paquets Swift sont combinés en une seule bibliothèque statique liée à l'exécutable du moteur.

Certains SDK ne peuvent pas être combinés dans une bibliothèque statique, et l'édition de liens du moteur échoue alors à cause de symboles en double. Dans ce cas, définissez `"wrapperType": "dynamic"` dans `SwiftPackages.json`. Les paquets sont alors compilés en un framework dynamique intégré au bundle de l'application.


## Ressources et manifestes de confidentialité {#resources-and-privacy-manifests}

Les bundles de ressources et les manifestes de confidentialité (`PrivacyInfo.xcprivacy`) des paquets sont inclus dans le bundle de l'application de la même manière que pour les dépendances CocoaPods.


## Migrer depuis CocoaPods {#migrating-from-cocoapods}

De nombreux SDK sont publiés à la fois sous forme de pod et de paquet Swift. Pour migrer une extension d'un fichier `Podfile` vers un fichier `SwiftPackages.json` :

1. Recherchez le dépôt git du paquet Swift dans la documentation du SDK. Il s'agit souvent du même dépôt que celui du pod.
2. Recherchez les noms des produits dans le fichier `Package.swift` du paquet. Les noms des pods et des produits diffèrent souvent.
3. Remplacez le `Podfile` par un fichier `SwiftPackages.json`. La version `platform :ios` du `Podfile` devient `minVersion`.
4. Vérifiez que les lignes `#import` de l'extension correspondent toujours aux noms de modules des produits.

Par exemple, ce `Podfile` :

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

devient ce `SwiftPackages.json` :

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

Dans ce cas, les modules conservent leurs noms ; `#import <FBSDKCoreKit/FBSDKCoreKit.h>` fonctionne donc avec les deux.


## Limites {#limitations}

* Seuls les dépôts de paquets accessibles publiquement via `https://` sont pris en charge. Les registres de paquets Swift ne sont pas pris en charge.
* Les fichiers `Package.swift` et les plugins des paquets s'exécutent sans accès réseau sur le serveur de build. Le serveur télécharge lui-même les paquets et leurs frameworks binaires avant leur compilation.
* La compilation de paquets contenant des catalogues de ressources (`.xcassets`) pour iOS nécessite un serveur de build utilisant Xcode 27 ou une version ultérieure. Avec une version antérieure de Xcode, le build échoue avec une erreur indiquant les paquets concernés.
* Les fichiers `SwiftPackages.json` d'un projet peuvent déclarer au maximum 32 paquets et 64 produits par plateforme.


## Dépannage {#troubleshooting}

`'Module/Header.h' file not found` ou symboles non définis
: Vérifiez que les `products` de `SwiftPackages.json` sont des noms de produits de `Package.swift` et que l'en-tête appartient à l'un d'eux. Un serveur de build qui ne prend pas en charge Swift Package Manager ignore `SwiftPackages.json`, et la compilation ou l'édition de liens de l'extension échoue de la même manière.

`The Swift package graph did not resolve within the ... time budget`
: Les paquets ont trop de dépendances pour être découverts sans fichier de verrouillage. Ajoutez un fichier `Package.resolved` à côté de `SwiftPackages.json`, comme décrit dans [Verrouiller les versions des paquets](#locking-package-versions). Puisque le build n'a pas abouti, créez ce fichier localement, par exemple en ajoutant les mêmes paquets à un projet Xcode. Xcode stocke ce fichier dans `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Serveur de build local {#local-build-server}

Les paquets Swift sont compilés par le serveur de build macOS. Pour les utiliser avec un [serveur de build local](/manuals/extender-local-setup), celui-ci doit disposer d'une installation complète de Xcode (les Command Line Tools seuls ne suffisent pas), de [XcodeGen](https://github.com/yonaskolb/XcodeGen), et de la prise en charge de Swift Package Manager activée par le paramètre `extender.spm.enabled`. Consultez la [documentation du serveur de build sur GitHub](https://github.com/defold/extender) pour plus d'informations.
