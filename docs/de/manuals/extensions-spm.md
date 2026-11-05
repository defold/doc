---
title: Abhängigkeiten mit Swift Package Manager in iOS- und macOS-Builds verwenden
brief: Dieses Handbuch erklärt, wie du Abhängigkeiten in iOS- und macOS-Builds mit Swift Package Manager auflöst.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) ist die in Swift und Xcode integrierte Abhängigkeitsverwaltung. Viele iOS- und macOS-SDKs werden als Swift-Pakete bereitgestellt, manche nicht mehr als CocoaPods. Defold verwendet Xcode nicht zum Erstellen der Engine, der Build-Server nutzt es jedoch zum Herunterladen und Erstellen der Swift-Pakete, von denen eine Erweiterung abhängt. Das Ergebnis wird anschließend wie [CocoaPods-Abhängigkeiten](/manuals/extensions-cocoapods) in die Engine eingebunden.

CocoaPods und Swift-Pakete können im selben Projekt und sogar in derselben Erweiterung verwendet werden.


## Abhängigkeiten deklarieren {#declaring-dependencies}

Native Erweiterungen können eine Datei `SwiftPackages.json` in den Ordnern `manifests/ios` und `manifests/osx` enthalten, um die Swift-Pakete anzugeben, von denen sie abhängen. Beispiel:

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

Die Datei besteht aus einfachem JSON. Du schreibst keine eigene Datei `Package.swift`; der Build-Server erzeugt sie aus den Dateien `SwiftPackages.json` aller Erweiterungen.

Die Datei enthält folgende Felder:

* `platform` - Erforderlich. `"ios"` in `manifests/ios/SwiftPackages.json` und `"osx"` in `manifests/osx/SwiftPackages.json`.
* `minVersion` - Optional. Die minimale iOS- oder macOS-Version, für die die Pakete erstellt werden, beispielsweise `"15.0"`. Verwendet wird der höchste Wert aller Erweiterungen und der von der Engine unterstützten Mindestversion, sowohl beim Erstellen der Pakete als auch beim Linken der Engine.
* `wrapperType` - Optional. `"static"` (Standard) oder `"dynamic"`. Siehe unten [Statisches und dynamisches Linken](#static-and-dynamic-linking).
* `packages` - Erforderlich. Eine Liste von Paketen. Jedes Paket hat folgende Felder:
  * `url` - Die `https://`-URL des Git-Repositorys des Pakets. URLs mit Zugangsdaten, einem benutzerdefinierten Port oder einer Abfragezeichenfolge sowie `ssh`-URLs werden nicht akzeptiert; das Repository muss daher öffentlich zugänglich sein.
  * `products` - Die Produkte des Pakets, die mit der Engine gelinkt werden sollen. Dies sind die Bibliotheksprodukte im Abschnitt `products` der Datei `Package.swift` des Pakets. Ein Produktname muss nicht dem Namen des Pakets oder des importierten Moduls entsprechen.
  * Genau eine Versionsanforderung:
    * `version` - Genau diese Version, beispielsweise `"12.16.0"`.
    * `from` - Diese Version oder eine spätere Version mit derselben Hauptversion. Beispielsweise wird `"9.0.0"` zur neuesten Veröffentlichung von `9.x.x` aufgelöst.
    * `branch` - Der neueste Commit eines Branches, beispielsweise `"main"`.
    * `revision` - Ein bestimmter Commit, angegeben als vollständiger Commit-Hash mit 40 Zeichen.

Der Build-Server sammelt die Dateien `SwiftPackages.json` aller Erweiterungen, löst damit sämtliche Abhängigkeiten einschließlich der Abhängigkeiten der Pakete selbst auf und bezieht sie beim Erstellen des nativen Codes ein.


## Pakete aus Erweiterungscode verwenden {#using-packages-from-extension-code}

Die Header der Produkte stehen dem Quellcode der Erweiterung zur Verfügung. Verwende sie aus Objective-C++-Quelldateien (`.mm`). Dieses Beispiel startet das [Sentry-SDK](https://github.com/getsentry/sentry-cocoa) beim Start der Anwendung:

`manifests/ios/SwiftPackages.json`:

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

`src/myextension.mm`:

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

* Objective-C-Header werden als `#import <Module/Header.h>` importiert, wobei `Module` der Name des Moduls ist, das sie bereitstellt.
* In Swift implementierte Klassen werden im erzeugten Header `<Module/Module-Swift.h>` deklariert. Er enthält nur die Klassen und Methoden, die das Modul für Objective-C verfügbar macht (in Swift mit `@objc` markiert). Importiere davor `UIKit` (unter macOS `AppKit`), da der erzeugte Header deren Typen verwendet.


## Abhängigkeiten mehrerer Erweiterungen {#dependencies-of-several-extensions}

Wenn mehrere Erweiterungen eines Projekts Swift-Pakete verwenden, werden alle ihre Dateien `SwiftPackages.json` für die Plattform zu einem gemeinsamen Paketgraphen zusammengeführt:

* Pakete mit derselben URL werden zusammengeführt, und die angeforderten Produkte werden kombiniert.
* Ein Paket, das mehrere Erweiterungen gemeinsam verwenden, muss in allen dieselbe Versionsanforderung haben. Unterschiedliche Anforderungen, etwa `"version": "12.16.0"` in einer Erweiterung und `"from": "12.0.0"` in einer anderen, lassen den Build mit dem Fehler `Conflicting requirements for Swift package` scheitern.
* Der höchste Wert für `minVersion` wird verwendet.
* Alle Erweiterungen, die `wrapperType` setzen, müssen denselben Wert verwenden.

Ein Projekt kann auch Erweiterungen mit CocoaPods und Erweiterungen mit Swift-Paketen kombinieren. Beide werden aufgelöst und mit der Engine gelinkt. Dasselbe SDK darf jedoch nicht aus beiden Quellen stammen: Bezieht eine Erweiterung Firebase aus einer `Podfile` und eine andere aus einer `SwiftPackages.json`, schlägt das Linken der Engine wegen doppelter Symbole fehl. Erweiterungen, die ein SDK gemeinsam verwenden, sollten dieselbe Abhängigkeitsverwaltung nutzen.


## Paketversionen festschreiben {#locking-package-versions}

Bei erfolgreichem Build liefert der Build-Server eine Datei `Package.resolved`, die die genaue Version und den Commit jedes Pakets im Graphen einschließlich der Paketabhängigkeiten auflistet. Sie wird im Build-Ordner des Projekts abgelegt, beispielsweise unter `build/arm64-ios/Package.resolved`.

Kopiere diese Datei in die Erweiterung neben `SwiftPackages.json` (beispielsweise `manifests/ios/Package.resolved`), um die Paketversionen festzuschreiben. Der Build-Server verwendet dann die festgeschriebenen Versionen, solange sie den Anforderungen in `SwiftPackages.json` entsprechen. Dies beschleunigt auch den Build: Ohne `Package.resolved` ermittelt der Build-Server die Paketabhängigkeiten schrittweise, was bei Paketen mit vielen Abhängigkeiten lange dauern kann.

Wenn mehrere Erweiterungen eine Datei `Package.resolved` für dieselbe Plattform enthalten, wird nur eine davon verwendet.


## Statisches und dynamisches Linken {#static-and-dynamic-linking}

Standardmäßig werden alle Swift-Pakete zu einer statischen Bibliothek zusammengefasst, die in die ausführbare Engine-Datei gelinkt wird.

Manche SDKs können nicht zu einer statischen Bibliothek zusammengefasst werden; das Linken der Engine schlägt dann wegen doppelter Symbole fehl. Setze in diesem Fall `"wrapperType": "dynamic"` in `SwiftPackages.json`. Die Pakete werden dann als dynamisches Framework erstellt und in das Anwendungs-Bundle eingebettet.


## Ressourcen und Datenschutzmanifeste {#resources-and-privacy-manifests}

Ressourcen-Bundles und Datenschutzmanifeste (`PrivacyInfo.xcprivacy`) der Pakete werden wie bei CocoaPods-Abhängigkeiten in das Anwendungs-Bundle aufgenommen.


## Von CocoaPods migrieren {#migrating-from-cocoapods}

Viele SDKs werden sowohl als Pod als auch als Swift-Paket veröffentlicht. So stellst du eine Erweiterung von einer `Podfile` auf eine Datei `SwiftPackages.json` um:

1. Suche das Git-Repository des Swift-Pakets in der SDK-Dokumentation. Häufig ist es dasselbe Repository wie beim Pod.
2. Suche die Produktnamen in der Datei `Package.swift` des Pakets. Pod-Namen und Produktnamen unterscheiden sich häufig.
3. Ersetze die `Podfile` durch eine Datei `SwiftPackages.json`. Die Version aus `platform :ios` in der `Podfile` wird zu `minVersion`.
4. Stelle sicher, dass die `#import`-Zeilen der Erweiterung weiterhin zu den Modulnamen der Produkte passen.

Beispielsweise wird diese `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

zu dieser `SwiftPackages.json`:

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

In diesem Fall behalten die Module ihre Namen, sodass `#import <FBSDKCoreKit/FBSDKCoreKit.h>` mit beiden Varianten funktioniert.


## Einschränkungen {#limitations}

* Es werden nur Paket-Repositorys unterstützt, die öffentlich über `https://` zugänglich sind. Swift-Paketregistries werden nicht unterstützt.
* Die Dateien `Package.swift` und die Plugins der Pakete laufen auf dem Build-Server ohne Netzwerkzugriff. Der Build-Server lädt die Pakete und ihre binären Frameworks selbst herunter, bevor die Pakete erstellt werden.
* Das Erstellen von Paketen mit Asset-Katalogen (`.xcassets`) für iOS benötigt einen Build-Server mit Xcode 27 oder neuer. Bei einer älteren Xcode-Version schlägt der Build mit einem Fehler fehl, der die betreffenden Pakete nennt.
* Die Dateien `SwiftPackages.json` eines Projekts dürfen pro Plattform höchstens 32 Pakete und 64 Produkte deklarieren.


## Fehlerbehebung {#troubleshooting}

`'Module/Header.h' file not found` oder nicht definierte Symbole
: Prüfe, ob die `products` in `SwiftPackages.json` Produktnamen aus `Package.swift` sind und ob der Header zu einem dieser Produkte gehört. Ein Build-Server ohne Unterstützung für Swift Package Manager ignoriert `SwiftPackages.json`; die Erweiterung scheitert dann auf dieselbe Weise beim Kompilieren oder Linken.

`The Swift package graph did not resolve within the ... time budget`
: Die Pakete haben zu viele Abhängigkeiten, um sie ohne Lock-Datei zu ermitteln. Ergänze eine Datei `Package.resolved` neben `SwiftPackages.json`, wie unter [Paketversionen festschreiben](#locking-package-versions) beschrieben. Da der Build nicht abgeschlossen wurde, erstelle die Datei lokal, beispielsweise indem du dieselben Pakete einem Xcode-Projekt hinzufügst. Xcode speichert sie unter `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Lokaler Build-Server {#local-build-server}

Swift-Pakete werden vom macOS-Build-Server erstellt. Für ihre Verwendung mit einem [lokalen Build-Server](/manuals/extender-local-setup) benötigt dieser eine vollständige Xcode-Installation (die Command Line Tools allein reichen nicht), [XcodeGen](https://github.com/yonaskolb/XcodeGen) und über die Einstellung `extender.spm.enabled` aktivierte Unterstützung für Swift Package Manager. Weitere Informationen findest du in der [Build-Server-Dokumentation auf GitHub](https://github.com/defold/extender).
