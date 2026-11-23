---
title: Uso di Swift nelle estensioni native per iOS e macOS
brief: Questo manuale spiega come scrivere in Swift il codice di un'estensione nativa per le build iOS e macOS.
---

# Swift nelle estensioni native {#swift-in-native-extensions}

Molte API di Apple, come StoreKit 2 e CryptoKit, sono accessibili solo da Swift. Un'estensione nativa può includere i propri file sorgente Swift accanto ai file Objective-C++. Il server di build li compila insieme al resto dell'estensione e collega il risultato al motore. I [pacchetti Swift](/manuals/extensions-spm) e [CocoaPods](/manuals/extensions-cocoapods) servono invece a integrare dipendenze già pronte.

Il codice Swift viene compilato per macOS (`arm64` e `x86_64`) e per iOS (dispositivi e simulatore). Nelle build per le altre piattaforme i file Swift vengono ignorati.


## Aggiunta dei sorgenti Swift {#adding-swift-sources}

Inserisci i file `.swift` nella cartella `src` dell'estensione, accanto ai file C++ e Objective-C++, come nell'esempio seguente.

```
myextension/
├── ext.manifest
└── src/
    ├── myextension.mm
    └── Greeter.swift
```

Tieni tutti i file Swift in `src`. La build per macOS o iOS fallisce se trova un file Swift in `commonsrc` o in `pluginsrc`.

Tutti i file Swift di un'estensione vengono compilati insieme in un unico modulo Swift. Il nome del modulo deriva dal campo `name` di `ext.manifest`. Ogni carattere diverso da una lettera, una cifra o un trattino basso viene sostituito con `_` (per esempio, `My-Extension` diventa `My_Extension`). Il compilatore usa la modalità Swift 5 del linguaggio.

Il modulo deve avere un nome diverso da quelli dei moduli importati dal codice. In un'estensione chiamata `StoreKit` non puoi usare `import StoreKit`, perché il compilatore interpreta l'istruzione come un tentativo di importare il modulo stesso.


## Chiamare Swift da Objective-C++ {#calling-swift-from-objective-c}

Il punto di ingresso di un'estensione è sempre una funzione C++ registrata con `DM_DECLARE_EXTENSION`. L'estensione deve quindi contenere almeno un file `.cpp` o `.mm`. Da questo file puoi chiamare il codice Swift tramite l'header generato `<Module>-Swift.h`.

Da Objective-C sono visibili solo le classi, i protocolli e i metodi contrassegnati con `@objc`. Dichiara le classi `public` e falle derivare da `NSObject`, come in questo esempio.

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

* L'header generato importa `Foundation`. Per i tipi degli altri framework contiene solo dichiarazioni anticipate. Prima di chiamare metodi che usano quei tipi, importa nel file `.mm` l'header del framework corrispondente (per esempio `UIKit`).
* Le funzioni `throws` sono esposte come metodi con un parametro `NSError **`, mentre le funzioni `async` sono esposte come metodi con una callback di completamento.
* Le funzionalità specifiche di Swift, come i tipi generici, le enumerazioni con valori associati e le strutture, non sono visibili da Objective-C. Per usarle, racchiudile in una classe `@objc`.
* I file `.mm` vengono compilati solo per iOS e macOS. Se l'estensione contiene soltanto file `.mm` e `.swift`, la build per le altre piattaforme fallisce con l'errore `Extension has no source!`. Per creare la build anche per queste piattaforme, sposta `DM_DECLARE_EXTENSION` in un file `.cpp`. Da lì richiama il codice del file `.mm` all'interno di un blocco di compilazione condizionale che verifichi `DM_PLATFORM_IOS` o `DM_PLATFORM_OSX`.


## Chiamare Objective-C da Swift {#calling-objective-c-from-swift}

Per usare da Swift le dichiarazioni Objective-C o C, aggiungi alla cartella `src` un header di collegamento (bridging header) chiamato `<Module>-Bridging-Header.h`. Un esempio è `src/MyExtension-Bridging-Header.h`.

```cpp
#import "mynative.h"
```

Se presente, l'header di collegamento viene importato automaticamente nel modulo Swift. Per trovare gli header che esso include, il compilatore cerca nella cartella `include` dell'estensione e nelle cartelle elencate in `additionalSwiftIncludePaths` (vedi più avanti).

In Swift puoi importare i framework Apple, come `Foundation`, `UIKit` o `StoreKit`, con una normale istruzione `import`. I framework elencati in `frameworks` e `weakFrameworks` nel file `ext.manifest` vengono collegati come di consueto. La maggior parte dei framework di sistema viene collegata automaticamente quando il codice Swift li importa.


## Usare i pacchetti Swift dal codice Swift {#using-swift-packages-from-swift}

Il codice Swift di un'estensione può usare i prodotti dei [pacchetti Swift](/manuals/extensions-spm) che l'estensione dichiara in `SwiftPackages.json`. Importa il modulo in un file Swift, come nell'esempio seguente.

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

Nell'header di collegamento puoi importare gli header Objective-C di un pacchetto nello stesso modo in cui li importeresti da un file `.mm`.

`src/MyExtension-Bridging-Header.h`:

```cpp
#import <Sentry/Sentry.h>
```

Dichiara il pacchetto nel file `SwiftPackages.json` dell'estensione che lo usa. Il server di build compila prima i pacchetti e poi il codice Swift dell'estensione. Se un pacchetto richiede una versione del sistema operativo superiore alla minima supportata dal motore, specifica la versione richiesta in `minVersion` nel file `SwiftPackages.json`. Anche il codice Swift dell'estensione verrà compilato per quella versione. L'uso delle dipendenze CocoaPods dal codice Swift non è supportato. Usale dal file Objective-C++ e passa al codice Swift ciò che gli serve.


## Opzioni del compilatore {#compiler-options}

Imposta le opzioni del compilatore Swift nel file `ext.manifest`, nello stesso `context` delle opzioni del compilatore C++.

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

* `defines` - Le definizioni del preprocessore impostate per C++ vengono passate a Swift come nomi per la compilazione condizionale. Puoi quindi usare `#if MY_DEFINE` anche in Swift. Il valore assegnato a una definizione, come in `MY_DEFINE=1`, viene scartato perché Swift accetta solo i nomi.
* `swiftFlags` - Opzioni aggiuntive per il compilatore Swift. Inserisci ogni opzione e ogni valore in un elemento distinto dell'elenco. Se un'opzione non rientra fra quelle ammesse, la build fallisce con l'errore `Invalid flag - 'swiftFlags'`. Se un valore contiene caratteri di spaziatura, una barra rovesciata o la sintassi di un template, oppure indica un file di risposta, la build fallisce con l'errore `invalid 'swiftFlags' value`. Sono ammesse le opzioni seguenti.
  * `-enable-upcoming-feature <Feature>` - Abilita una funzionalità prevista per una versione futura del linguaggio, per esempio `["-enable-upcoming-feature", "ExistentialAny"]`.
  * `-strict-concurrency=minimal|targeted|complete`
  * `-enforce-exclusivity=checked|unchecked`
  * `-O`, `-Osize` e `-Onone` - Impostano il livello di ottimizzazione. Il valore predefinito è `-O`.
  * `-suppress-warnings`
* `additionalSwiftIncludePaths` - Cartelle in cui il compilatore Swift cerca header e moduli, oltre alla cartella `include` dell'estensione.
* `additionalFrameworkSearchPaths` - Cartelle in cui cercare i framework, oltre alla cartella `lib/<platform>` dell'estensione. Le usano il compilatore Swift, il compilatore C++ e Objective-C++ quando compila i sorgenti dell'estensione, e il linker.

I percorsi sono relativi alla cartella dell'estensione, devono rimanere al suo interno e possono contenere solo lettere, cifre e i caratteri `._+-/`. Il server di build riceve soltanto le cartelle `include`, `src`, `commonsrc`, `pluginsrc`, `lib/<platform>`, `manifests/<platform>` e `res/<platform>` dell'estensione. I percorsi devono quindi puntare all'interno di una di queste cartelle. I file che si trovano altrove, per esempio in una cartella `vendor` alla radice dell'estensione, non sono disponibili durante la build.

Le chiavi Swift della piattaforma `ios` si applicano sia ai dispositivi sia al simulatore. Un server di build precedente all'introduzione del supporto per Swift rifiuta queste chiavi con l'errore `Manifest context variable unsupported`. Per poter creare nuovamente la build del progetto, aggiorna sia Defold sia il server di build.


## Versioni minime del sistema operativo {#minimum-os-versions}

Il runtime Swift è incluso in tutte le versioni di iOS e macOS supportate da Defold. Il codice Swift viene compilato per la versione minima di iOS o macOS prevista dalla build e l'applicazione usa il runtime Swift del sistema operativo. Prima di chiamare API introdotte dopo la versione minima, verificane la disponibilità con `#available`.

Alcuni componenti del runtime sono inclusi nel sistema operativo solo a partire da una versione successiva. Per esempio, `MutableSpan` e i tipi correlati sono inclusi a partire da iOS 26 e macOS 26. Se la versione minima è precedente e il codice Swift o un framework dinamico di un pacchetto usa una di queste funzionalità, l'applicazione potrebbe richiedere una libreria aggiuntiva per funzionare sui dispositivi con una versione precedente del sistema. Il server di build se ne occupa automaticamente. Come Xcode, individua le librerie usate dal motore e dalle librerie dinamiche distribuite insieme a esso e le aggiunge all'applicazione. Su iOS le colloca nella cartella `Frameworks` dell'applicazione e le firma insieme al resto del codice.

La versione minima del sistema operativo per una build è quella supportata dal motore e dipende dalla versione di Defold e dal server di build. Con `minVersion` in un file `SwiftPackages.json` puoi alzarla per la compilazione dei pacchetti e del codice Swift e per il collegamento del motore, come descritto nel [manuale di Swift Package Manager](/manuals/extensions-spm). Non puoi abbassarla.


## Limitazioni {#limitations}

* Un'estensione deve comunque contenere un file C++ o Objective-C++ con `DM_DECLARE_EXTENSION`. Il codice Swift non può registrare l'estensione. Inoltre, l'API C++ dell'SDK Defold (`dmsdk`) non è accessibile da Swift, quindi chiamala dal file Objective-C++. Nell'header di collegamento puoi includere gli header di `dmsdk` compatibili con C, come `dmsdk/dlib/hash.h`. Se la build contiene solo file `.swift`, il collegamento fallisce con un errore di simbolo non definito che riporta il nome dell'estensione.
* L'uso delle dipendenze CocoaPods dal codice Swift non è supportato. Usale dal file Objective-C++ e passa al codice Swift ciò che gli serve.
* È supportata solo la modalità Swift 5 del linguaggio. L'interoperabilità con C++ non è abilitata.
* I sorgenti Swift sono supportati a partire da Defold 1.14.2. Se il server di build usa un SDK precedente, la build fallisce con l'errore `Swift sources are not supported by this Defold SDK version`.
* Durante la creazione dell'artefatto `library` (`--build-artifacts library` in [Bob](/manuals/bob)) i sorgenti Swift non vengono compilati. Di conseguenza, in questa build la compilazione di un file Objective-C++ che importa `<Module>-Swift.h` fallisce.


## Risoluzione dei problemi {#troubleshooting}

`no such module 'Name'`
: Il modulo non è un prodotto di un pacchetto dichiarato in un file `SwiftPackages.json`. Verifica che `products` includa un prodotto che fornisce il modulo, come descritto nel [manuale di Swift Package Manager](/manuals/extensions-spm).

`Swift sources are only supported in the 'src' folder`
: Sposta i file `.swift` nella cartella `src` dell'estensione.

`'MyExtension-Swift.h' file not found`
: Il nome del modulo deriva dal campo `name` in `ext.manifest`. Controlla il nome nella riga `#import`.

`unknown type name 'MyExtensionGreeter'`
: La classe non compare nell'header generato. Verifica che sia contrassegnata con `public` e `@objc`, che derivi da `NSObject` e che il file `.mm` usi il nome indicato in `@objc(...)`.

`cannot find 'AppStore' in scope` insieme a `file 'A.swift' is part of module 'StoreKit'; ignoring import`
: L'estensione ha lo stesso nome di un modulo che importa. Rinomina l'estensione in `ext.manifest`.

`Undefined symbols ... _MyExtension`
: Nell'estensione manca `DM_DECLARE_EXTENSION`. Aggiungi un file `.mm` che registri l'estensione come descritto sopra.

`Invalid flag - 'swiftFlags'`
: L'opzione non è nell'elenco di quelle ammesse. Rimuovila o usa una delle opzioni elencate.

`invalid 'swiftFlags' value`
: Il valore contiene caratteri di spaziatura, una barra rovesciata o la sintassi di un template, oppure indica un file di risposta. Inserisci ogni opzione e ogni valore in un elemento distinto dell'elenco.
