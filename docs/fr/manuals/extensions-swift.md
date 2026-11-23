---
title: Utiliser Swift dans les extensions natives pour iOS et macOS
brief: Ce manuel explique comment écrire le code d'une extension native en Swift pour les builds iOS et macOS.
---

# Swift dans les extensions natives {#swift-in-native-extensions}

De nombreuses API Apple, comme StoreKit 2 ou CryptoKit, ne sont accessibles qu'en Swift. Une extension native peut contenir ses propres fichiers source Swift aux côtés de ses fichiers Objective-C++. Le serveur de build les compile avec le reste de l'extension et lie le résultat au moteur. Les [paquets Swift](/manuals/extensions-spm) et [CocoaPods](/manuals/extensions-cocoapods) permettent quant à eux d'intégrer des dépendances prêtes à l'emploi.

Le serveur compile le code Swift pour macOS (`arm64` et `x86_64`) et pour iOS (appareils et simulateur). Il ignore les fichiers Swift lors des builds destinés aux autres plateformes.


## Ajouter des fichiers source Swift {#adding-swift-sources}

Placez les fichiers `.swift` dans le dossier `src` de l'extension, aux côtés des fichiers C++ et Objective-C++.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Conservez tous les fichiers Swift dans `src`. Le build macOS ou iOS échoue si le serveur trouve un fichier Swift dans `commonsrc` ou `pluginsrc`.

Le compilateur regroupe tous les fichiers Swift d'une extension en un seul module Swift. Le nom du module provient du champ `name` de `ext.manifest`. Tout caractère autre qu'une lettre, un chiffre ou un trait de soulignement est remplacé par `_` (par exemple, `My-Extension` devient `My_Extension`). Le compilateur utilise le mode de langage Swift 5.

Le nom du module doit être différent de celui des modules que le code importe. Une extension nommée `StoreKit` ne peut pas utiliser `import StoreKit`, car le compilateur considère que le module s'importe lui-même.


## Appeler du code Swift depuis Objective-C++ {#calling-swift-from-objective-c}

Le point d'entrée d'une extension reste une fonction C++ enregistrée avec `DM_DECLARE_EXTENSION`. L'extension doit donc contenir au moins un fichier `.cpp` ou `.mm`. C'est depuis ce fichier que vous appelez le code Swift grâce à l'en-tête généré `<Module>-Swift.h`.

Objective-C n'a accès qu'aux classes, aux protocoles et aux méthodes portant l'attribut `@objc`. Déclarez les classes `public` et faites-les hériter de `NSObject`, comme dans cet exemple.

`src/Greeter.swift` :

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm` :

```cpp
#include <dmsdk/sdk.h>
#import <Foundation/Foundation.h>
#import "MyExtension-Swift.h"

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    MyExtensionGreeter* greeter = [[MyExtensionGreeter alloc] init];
    dmLogInfo("%s", [[greeter message] UTF8String]);
    return dmExtension::RESULT_OK;
}

DM_DECLARE_EXTENSION(MyExtension, "MyExtension", AppInitializeMyExtension, 0, 0, 0, 0, 0)
```

* L'en-tête généré importe `Foundation`. Pour les types provenant d'autres frameworks, il ne contient que des déclarations anticipées. Importez l'en-tête du framework concerné (par exemple `UIKit`) dans le fichier `.mm` avant d'appeler des méthodes qui utilisent ces types.
* Les fonctions `throws` sont accessibles sous forme de méthodes qui prennent un paramètre `NSError **`, et les fonctions `async` sous forme de méthodes qui prennent un gestionnaire de fin d'exécution.
* Objective-C n'a pas accès aux fonctionnalités propres à Swift, comme les types génériques, les énumérations avec valeurs associées et les structures. Encapsulez-les dans une classe `@objc`.
* Les fichiers `.mm` ne sont compilés que pour iOS et macOS. Si une extension ne contient que des fichiers `.mm` et `.swift`, le build pour toute autre plateforme échoue avec l'erreur `Extension has no source!`. Pour que l'extension soit également compilée pour les autres plateformes, placez `DM_DECLARE_EXTENSION` dans un fichier `.cpp`. Dans ce fichier, placez l'appel au code du fichier `.mm` dans un bloc de compilation conditionnelle qui vérifie `DM_PLATFORM_IOS` ou `DM_PLATFORM_OSX`.


## Appeler du code Objective-C depuis Swift {#calling-objective-c-from-swift}

Pour utiliser des déclarations Objective-C ou C depuis Swift, ajoutez au dossier `src` un en-tête de liaison (bridging header) nommé `<Module>-Bridging-Header.h`, par exemple `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Si cet en-tête existe, le compilateur l'importe automatiquement dans le module Swift. Il recherche les en-têtes qui y sont inclus dans le dossier `include` de l'extension et dans les dossiers indiqués dans `additionalSwiftIncludePaths` (voir ci-dessous).

Depuis Swift, importez les frameworks Apple, comme `Foundation`, `UIKit` ou `StoreKit`, avec l'instruction `import` habituelle. Les frameworks répertoriés dans les champs `frameworks` et `weakFrameworks` du fichier `ext.manifest` sont liés comme d'habitude. La plupart des frameworks système sont liés automatiquement dès que le code Swift les importe.


## Utiliser des paquets Swift depuis le code Swift {#using-swift-packages-from-swift}

Le code Swift d'une extension a accès aux produits des [paquets Swift](/manuals/extensions-spm) que l'extension déclare dans `SwiftPackages.json`. Importez le module dans un fichier Swift.

```swift
import Foundation
import Sentry

@objc(MyExtensionCrashReporter)
public class CrashReporter: NSObject {
    @objc public func start(dsn: String) {
        SentrySDK.start { options in
            options.dsn = dsn
        }
    }
}
```

Vous pouvez importer les en-têtes Objective-C d'un paquet dans l'en-tête de liaison, comme vous le feriez dans un fichier `.mm`.

`src/MyExtension-Bridging-Header.h` :

```cpp
#import <Sentry/Sentry.h>
```

Déclarez le paquet dans le fichier `SwiftPackages.json` de l'extension qui l'utilise. Le serveur de build compile d'abord les paquets, puis le code Swift de l'extension. Si un paquet exige une version du système plus récente que la version minimale prise en charge par le moteur, indiquez cette version dans le champ `minVersion` de `SwiftPackages.json`. Le serveur compilera aussi le code Swift de l'extension pour cette version. L'utilisation des dépendances CocoaPods depuis le code Swift n'est pas prise en charge. Utilisez-les depuis le fichier Objective-C++ et transmettez au code Swift les éléments dont il a besoin.


## Options du compilateur {#compiler-options}

Définissez les options du compilateur Swift dans le fichier `ext.manifest`, dans le même bloc `context` que les options du compilateur C++.

```yaml
name: MyExtension

platforms:
    ios:
        context:
            defines: ["MY_DEFINE"]
            swiftFlags: ["-strict-concurrency=complete"]
            additionalSwiftIncludePaths: ["include/vendor/headers"]
            additionalFrameworkSearchPaths: ["lib/ios/vendor/frameworks"]
    osx:
        context:
            defines: ["MY_DEFINE"]
```

* `defines` - Les noms des macros définies pour C++ sont transmis à Swift pour la compilation conditionnelle. Vous pouvez donc utiliser `#if MY_DEFINE` en Swift. Si une macro a une valeur, comme dans `MY_DEFINE=1`, cette valeur est ignorée car Swift ne prend en charge que les noms.
* `swiftFlags` - Options supplémentaires du compilateur Swift. Placez chaque option et chaque valeur dans un élément distinct de la liste. Le serveur filtre les options à l'aide d'une liste d'autorisation. Toute autre option fait échouer le build avec l'erreur `Invalid flag - 'swiftFlags'`. Si une valeur contient un caractère d'espacement, une barre oblique inverse ou une expression de gabarit, ou si elle désigne un fichier de réponse, le build échoue avec l'erreur `invalid 'swiftFlags' value`. Les options autorisées figurent ci-dessous.
  * `-enable-upcoming-feature <Feature>` - Active une fonctionnalité prévue dans une prochaine version du langage, par exemple `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` et `-Onone` - Niveau d'optimisation. La valeur par défaut est `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Dossiers dans lesquels le compilateur Swift recherche des en-têtes et des modules, en plus du dossier `include` de l'extension.
* `additionalFrameworkSearchPaths` - Dossiers dans lesquels les outils de build recherchent des frameworks, en plus du dossier `lib/<platform>` de l'extension. Ces dossiers servent au compilateur Swift, au compilateur C++ et Objective-C++ pour les fichiers source de l'extension, ainsi qu'à l'éditeur de liens.

Les chemins sont relatifs au dossier de l'extension, doivent rester à l'intérieur de ce dossier et ne peuvent contenir que des lettres, des chiffres et les caractères `._+-/`. Seuls les dossiers `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` et `res/<platform>` de l'extension sont envoyés au serveur de build. Les chemins doivent donc désigner des emplacements dans l'un de ces dossiers. Les fichiers placés ailleurs, par exemple dans un dossier `vendor` à la racine de l'extension, ne sont pas disponibles pendant le build.

Les clés Swift de la plateforme `ios` s'appliquent aux appareils comme au simulateur. Un serveur de build antérieur à la prise en charge de Swift rejette ces clés avec l'erreur `Manifest context variable unsupported`. Le build du projet échoue alors jusqu'à ce que vous mettiez à jour la version de Defold et le serveur de build.


## Versions minimales du système d'exploitation {#minimum-os-versions}

Toutes les versions d'iOS et de macOS prises en charge par Defold intègrent l'environnement d'exécution Swift. Le code Swift est compilé pour la version minimale d'iOS ou de macOS ciblée par le build. L'application utilise ensuite l'environnement d'exécution Swift du système. Avant d'appeler une API introduite après cette version minimale, vérifiez sa disponibilité avec `#available`.

Certaines parties de l'environnement d'exécution n'ont été intégrées au système que dans des versions plus récentes. Par exemple, `MutableSpan` et les types associés sont intégrés à partir d'iOS 26 et de macOS 26. Si la version minimale est antérieure et que votre code Swift ou un framework dynamique d'un paquet utilise une telle fonctionnalité, l'application peut avoir besoin d'une bibliothèque supplémentaire pour fonctionner sur les appareils équipés d'une version antérieure du système. Comme Xcode, le serveur de build repère les bibliothèques dont dépendent le moteur et les bibliothèques dynamiques embarquées avec lui, puis les ajoute automatiquement à l'application. Sur iOS, ces bibliothèques sont placées dans le dossier `Frameworks` de l'application et signées en même temps que le reste du code.

La version minimale ciblée par le build est celle que le moteur prend en charge. Elle dépend de la version de Defold et du serveur de build. Le champ `minVersion` d'un fichier `SwiftPackages.json` permet de relever cette version pour les paquets, le code Swift et l'édition de liens du moteur, comme l'explique le [manuel de Swift Package Manager](/manuals/extensions-spm). Il est impossible de l'abaisser.


## Limites {#limitations}

* Une extension doit toujours contenir un fichier C++ ou Objective-C++ avec `DM_DECLARE_EXTENSION`. Le code Swift ne peut pas enregistrer l'extension. L'API C++ du SDK Defold (`dmsdk`) n'est pas accessible depuis Swift. Appelez-la depuis le fichier Objective-C++. Vous pouvez inclure les en-têtes de `dmsdk` compatibles avec C, comme `dmsdk/dlib/hash.h`, dans l'en-tête de liaison. Si l'extension ne contient que des fichiers `.swift`, l'édition de liens échoue et signale un symbole non défini portant le nom de l'extension.
* L'utilisation des dépendances CocoaPods depuis le code Swift n'est pas prise en charge. Utilisez-les depuis le fichier Objective-C++ et transmettez au code Swift les éléments dont il a besoin.
* Seul le mode de langage Swift 5 est pris en charge. L'interopérabilité avec C++ n'est pas activée.
* Les fichiers source Swift sont pris en charge à partir de Defold 1.14.2. Si le serveur de build utilise un SDK plus ancien, le build échoue avec l'erreur `Swift sources are not supported by this Defold SDK version`.
* Lors de la génération de l'artefact `library` (avec `--build-artifacts library` dans [Bob](/manuals/bob)), les fichiers source Swift ne sont pas compilés. La compilation de tout fichier Objective-C++ qui importe `<Module>-Swift.h` échoue donc dans ce cas.


## Dépannage {#troubleshooting}

`no such module 'Name'`
: Le module ne fait partie des produits d'aucun paquet déclaré dans un fichier `SwiftPackages.json`. Vérifiez que la liste `products` contient un produit qui fournit ce module, comme l'explique le [manuel de Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Déplacez les fichiers `.swift` dans le dossier `src` de l'extension.

`'MyExtension-Swift.h' file not found`
: Le nom du module provient du champ `name` de `ext.manifest`. Vérifiez le nom dans la directive `#import`.

`unknown type name 'MyExtensionGreeter'`
: La classe est absente de l'en-tête généré. Vérifiez qu'elle est déclarée `public`, qu'elle porte l'attribut `@objc`, qu'elle hérite de `NSObject` et que le fichier `.mm` utilise le nom indiqué dans `@objc(...)`.

`cannot find 'AppStore' in scope` accompagné de `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: L'extension porte le même nom qu'un module qu'elle importe. Renommez l'extension dans `ext.manifest`.

`Undefined symbols ... _MyExtension`
: L'extension ne contient pas de déclaration `DM_DECLARE_EXTENSION`. Ajoutez un fichier `.mm` qui enregistre l'extension comme indiqué plus haut.

`Invalid flag - 'swiftFlags'`
: Cette option ne figure pas dans la liste des options autorisées. Supprimez-la ou utilisez l'une des options de la liste.

`invalid 'swiftFlags' value`
: La valeur contient un caractère d'espacement, une barre oblique inverse ou une expression de gabarit, ou bien elle désigne un fichier de réponse. Placez chaque option et chaque valeur dans un élément distinct de la liste.
