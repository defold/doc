---
title: Swift in nativen Erweiterungen für iOS und macOS verwenden
brief: Dieses Handbuch erklärt, wie du den Code einer nativen Erweiterung für iOS- und macOS-Builds in Swift schreibst.
---

# Swift in nativen Erweiterungen {#swift-in-native-extensions}

Viele Apple-APIs wie StoreKit 2 oder CryptoKit lassen sich nur aus Swift aufrufen. Eine native Erweiterung (native extension) kann neben ihren Objective-C++-Dateien eigene Swift-Quelldateien enthalten. Der Build-Server kompiliert sie zusammen mit dem übrigen Code der Erweiterung und linkt das Ergebnis in die Engine. Unabhängig davon kannst du über [Swift-Pakete](/manuals/extensions-spm) und [CocoaPods](/manuals/extensions-cocoapods) fertige Abhängigkeiten einbinden.

Swift-Code wird für macOS (`arm64` und `x86_64`) und für iOS (Geräte und Simulator) kompiliert. Bei Builds für andere Plattformen werden die Swift-Dateien ignoriert.


## Swift-Quelldateien hinzufügen {#adding-swift-sources}

Lege die `.swift`-Dateien zusammen mit den C++- und Objective-C++-Dateien im Ordner `src` der Erweiterung ab.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Lege alle Swift-Dateien in `src` ab. Findet der Build-Server eine Swift-Datei in `commonsrc` oder `pluginsrc`, schlägt der Build für macOS oder iOS fehl.

Alle Swift-Dateien einer Erweiterung werden gemeinsam zu einem einzigen Swift-Modul kompiliert. Der Modulname ergibt sich aus dem Wert von `name` in `ext.manifest`. Jedes Zeichen außer Buchstaben, Ziffern und Unterstrichen wird dabei durch `_` ersetzt (aus `My-Extension` wird `My_Extension`). Der Compiler arbeitet im Sprachmodus Swift 5.

Der Modulname muss sich von den Namen aller Module unterscheiden, die der Code importiert. In einer Erweiterung namens `StoreKit` funktioniert `import StoreKit` daher nicht. Der Compiler versteht den Import als Verweis auf das Modul selbst.


## Swift aus Objective-C++ aufrufen {#calling-swift-from-objective-c}

Der Einstiegspunkt einer Erweiterung ist weiterhin eine C++-Funktion, die du mit `DM_DECLARE_EXTENSION` registrierst. Daher benötigt die Erweiterung mindestens eine `.cpp`- oder `.mm`-Datei. Aus dieser Datei rufst du den Swift-Code über den generierten Header `<Module>-Swift.h` auf.

In Objective-C sind nur Klassen, Protokolle und Methoden sichtbar, die mit `@objc` gekennzeichnet sind. Deklariere die Klassen als `public` und leite sie von `NSObject` ab.

`src/Greeter.swift`:

```swift
import Foundation

@objc(MyExtensionGreeter)
public class Greeter: NSObject {
    @objc public func message() -> String {
        return "Hello from Swift"
    }
}
```

`src/myextension.mm`:

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

* Der generierte Header importiert `Foundation`. Für Typen aus anderen Frameworks enthält er lediglich Vorwärtsdeklarationen. Importiere den Header des jeweiligen Frameworks (beispielsweise `UIKit`) in der `.mm`-Datei, bevor du Methoden aufrufst, die diese Typen verwenden.
* Funktionen mit `throws` stehen als Methoden mit einem Parameter vom Typ `NSError **` zur Verfügung. Funktionen mit `async` stehen als Methoden mit einem Completion-Handler zur Verfügung.
* Swift-spezifische Sprachmerkmale wie Generics, Enums mit assoziierten Werten und Structs sind in Objective-C nicht sichtbar. Kapsle sie in einer mit `@objc` gekennzeichneten Klasse.
* `.mm`-Dateien werden nur für iOS und macOS kompiliert. Besteht die Erweiterung ausschließlich aus `.mm`- und `.swift`-Dateien, schlägt der Build für andere Plattformen mit der Meldung `Extension has no source!` fehl. Um die Erweiterung auch für andere Plattformen zu erstellen, platziere `DM_DECLARE_EXTENSION` in einer `.cpp`-Datei. Rufe darin den Code aus der `.mm`-Datei innerhalb eines Präprozessorblocks auf, der auf `DM_PLATFORM_IOS` oder `DM_PLATFORM_OSX` prüft.


## Objective-C aus Swift aufrufen {#calling-objective-c-from-swift}

Um Objective-C- oder C-Deklarationen in Swift zu verwenden, füge dem Ordner `src` einen Bridging-Header namens `<Module>-Bridging-Header.h` hinzu. In diesem Beispiel heißt die Datei `src/MyExtension-Bridging-Header.h` und enthält den folgenden Import.

```cpp
#import "mynative.h"
```

Ist der Bridging-Header vorhanden, wird er automatisch in das Swift-Modul importiert. Nach Headern, die er einbindet, sucht der Compiler im Ordner `include` der Erweiterung und in den unter `additionalSwiftIncludePaths` aufgeführten Ordnern (siehe unten).

Apple-Frameworks wie `Foundation`, `UIKit` oder `StoreKit` importierst du in Swift mit einem gewöhnlichen `import`. Die in `ext.manifest` unter `frameworks` und `weakFrameworks` aufgeführten Frameworks werden wie gewohnt gelinkt. Die meisten Systemframeworks werden automatisch gelinkt, wenn der Swift-Code sie importiert.


## Swift-Pakete im Swift-Code verwenden {#using-swift-packages-from-swift}

Die Produkte der [Swift-Pakete](/manuals/extensions-spm), die eine Erweiterung in `SwiftPackages.json` deklariert, stehen ihrem Swift-Code zur Verfügung. Importiere das Modul in einer Swift-Datei.

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

Die Objective-C-Header eines Pakets kannst du im Bridging-Header genauso importieren wie in einer `.mm`-Datei.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Deklariere das Paket in der Datei `SwiftPackages.json` der Erweiterung, die es verwendet. Der Build-Server erstellt zuerst die Pakete und kompiliert anschließend den Swift-Code der Erweiterung. Benötigt ein Paket eine neuere Betriebssystemversion als die von der Engine unterstützte Mindestversion, gib die benötigte Version als `minVersion` in `SwiftPackages.json` an. Der Swift-Code der Erweiterung wird dann ebenfalls für diese Version kompiliert. Swift-Code kann CocoaPods-Abhängigkeiten nicht direkt verwenden. Verwende sie in der Objective-C++-Datei und übergib dem Swift-Code, was er benötigt.


## Compileroptionen {#compiler-options}

Die Optionen für den Swift-Compiler legst du in der Datei `ext.manifest` im selben `context` fest wie die Optionen für den C++-Compiler.

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

* `defines` - Die für C++ gesetzten Präprozessor-Definitionen werden als Namen für die bedingte Kompilierung an Swift übergeben. Dadurch funktioniert `#if MY_DEFINE` auch in Swift. Bei Definitionen wie `MY_DEFINE=1` entfällt der Wert, da Swift nur Namen unterstützt.
* `swiftFlags` - Zusätzliche Optionen für den Swift-Compiler. Gib jede Option und jeden Wert als eigenen Listeneintrag an. Optionen, die nicht auf der Positivliste stehen, führen zum Build-Fehler `Invalid flag - 'swiftFlags'`. Enthält ein Wert Leerraumzeichen, einen umgekehrten Schrägstrich oder Vorlagensyntax oder verweist er auf eine Antwortdatei, schlägt der Build mit der Meldung `invalid 'swiftFlags' value` fehl. Folgende Optionen sind zulässig.
  * `-enable-upcoming-feature <Feature>` - Aktiviert ein für eine künftige Sprachversion vorgesehenes Merkmal, beispielsweise mit `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` und `-Onone` - Legen die Optimierungsstufe fest. Der Standardwert ist `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Ordner, in denen der Swift-Compiler zusätzlich zum Ordner `include` der Erweiterung nach Headern und Modulen sucht.
* `additionalFrameworkSearchPaths` - Ordner, in denen zusätzlich zum Ordner `lib/<platform>` der Erweiterung nach Frameworks gesucht wird. Diese Suchpfade verwenden sowohl der Swift-Compiler als auch der C++- und Objective-C++-Compiler beim Kompilieren der Quelldateien der Erweiterung. Der Linker verwendet sie ebenfalls.

Die Pfade sind relativ zum Erweiterungsordner, müssen innerhalb dieses Ordners bleiben und dürfen nur Buchstaben, Ziffern und die Zeichen `._+-/` enthalten. An den Build-Server werden nur die Ordner `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` und `res/<platform>` der Erweiterung übertragen. Die Pfade müssen daher auf einen dieser Ordner oder einen seiner Unterordner verweisen. Dateien in anderen Ordnern, etwa in einem Ordner `vendor` auf der obersten Ebene der Erweiterung, stehen beim Build nicht zur Verfügung.

Die Swift-Schlüssel der Plattform `ios` gelten für Geräte und Simulator gleichermaßen. Ein älterer Build-Server ohne Swift-Unterstützung lehnt sie mit der Meldung `Manifest context variable unsupported` ab. Damit du wieder einen Build des Projekts erstellen kannst, musst du sowohl die Defold-Version als auch den Build-Server aktualisieren.


## Mindestversionen der Betriebssysteme {#minimum-os-versions}

Die Swift-Laufzeitumgebung ist Bestandteil aller von Defold unterstützten iOS- und macOS-Versionen. Der Swift-Code wird für die iOS- oder macOS-Mindestversion des Builds kompiliert. Die Anwendung verwendet die Swift-Laufzeitumgebung des Betriebssystems. Wenn du eine API aufrufen möchtest, die erst nach dieser Mindestversion eingeführt wurde, prüfe ihre Verfügbarkeit zuvor mit `#available`.

Einige Teile der Laufzeitumgebung gehören erst ab einer neueren Version zum Betriebssystem. Beispielsweise sind `MutableSpan` und verwandte Typen ab iOS 26 und macOS 26 enthalten. Liegt die Mindestversion darunter und nutzt dein Swift-Code oder ein dynamisches Framework aus einem Paket eine solche Funktion, braucht die Anwendung für Geräte mit älterem Betriebssystem möglicherweise eine zusätzliche Bibliothek. Das erledigt der Build-Server automatisch. Wie Xcode ermittelt er, welche Bibliotheken die Engine und die mit ihr eingebetteten dynamischen Bibliotheken benötigen, und fügt sie der Anwendung hinzu. Unter iOS legt er sie im Ordner `Frameworks` der Anwendung ab und signiert sie zusammen mit dem übrigen Code.

Für einen Build gilt die von der Engine unterstützte Mindestversion. Sie hängt von der Defold-Version und dem Build-Server ab. Mit `minVersion` in einer Datei `SwiftPackages.json` kannst du diese Mindestversion für die Pakete, den Swift-Code und das Linken der Engine anheben, wie im [Handbuch zu Swift Package Manager](/manuals/extensions-spm) beschrieben. Sie lässt sich nicht herabsetzen.


## Einschränkungen {#limitations}

* Die Erweiterung benötigt weiterhin eine C++- oder Objective-C++-Datei mit `DM_DECLARE_EXTENSION`. Aus Swift lässt sich die Erweiterung nicht registrieren. Die C++-API des Defold-SDK (`dmsdk`) ist aus Swift ebenfalls nicht zugänglich. Rufe sie daher aus der Objective-C++-Datei auf. C-kompatible Header aus `dmsdk`, etwa `dmsdk/dlib/hash.h`, kannst du in den Bridging-Header einbinden. Enthält die Erweiterung nur `.swift`-Dateien, schlägt das Linken fehl. Die Fehlermeldung nennt ein undefiniertes Symbol mit dem Namen der Erweiterung.
* Swift-Code kann CocoaPods-Abhängigkeiten nicht direkt verwenden. Verwende sie in der Objective-C++-Datei und übergib dem Swift-Code, was er benötigt.
* Nur der Sprachmodus Swift 5 wird unterstützt. Die Interoperabilität mit C++ ist nicht aktiviert.
* Defold unterstützt Swift-Quelldateien ab Version 1.14.2. Auf einem Build-Server mit einem älteren SDK schlägt der Build mit der Meldung `Swift sources are not supported by this Defold SDK version` fehl.
* Beim Erstellen des Artefakts `library` (`--build-artifacts library` in [Bob](/manuals/bob)) werden Swift-Quelldateien nicht kompiliert. Eine Objective-C++-Datei, die `<Module>-Swift.h` importiert, lässt sich bei diesem Build daher nicht kompilieren.


## Fehlerbehebung {#troubleshooting}

`no such module 'Name'`
: Das Modul gehört zu keinem Produkt eines Pakets, das in einer Datei `SwiftPackages.json` deklariert ist. Prüfe, ob unter `products` ein Produkt aufgeführt ist, das das Modul bereitstellt, wie im [Handbuch zu Swift Package Manager](/manuals/extensions-spm) beschrieben.

`Swift sources are only supported in the 'src' folder`
: Verschiebe die `.swift`-Dateien in den Ordner `src` der Erweiterung.

`'MyExtension-Swift.h' file not found`
: Der Modulname wird aus dem Wert von `name` in `ext.manifest` gebildet. Prüfe den Namen in der `#import`-Zeile.

`unknown type name 'MyExtensionGreeter'`
: Die Klasse fehlt im generierten Header. Prüfe, ob die Klasse mit `public` und `@objc` gekennzeichnet ist und von `NSObject` abgeleitet ist. Prüfe außerdem, ob die `.mm`-Datei den in `@objc(...)` angegebenen Namen verwendet.

`cannot find 'AppStore' in scope` zusammen mit `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: Die Erweiterung hat denselben Namen wie ein Modul, das sie importiert. Benenne die Erweiterung in `ext.manifest` um.

`Undefined symbols ... _MyExtension`
: In der Erweiterung fehlt `DM_DECLARE_EXTENSION`. Füge eine `.mm`-Datei hinzu, die die Erweiterung wie oben beschrieben registriert.

`Invalid flag - 'swiftFlags'`
: Die Option steht nicht auf der Positivliste. Entferne sie oder verwende eine der aufgeführten Optionen.

`invalid 'swiftFlags' value`
: Der Wert enthält Leerraumzeichen, einen umgekehrten Schrägstrich oder Vorlagensyntax oder verweist auf eine Antwortdatei. Gib jede Option und jeden Wert als eigenen Listeneintrag an.
