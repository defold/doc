---
title: Uso delle dipendenze Swift Package Manager nelle build iOS e macOS
brief: Questo manuale spiega come usare Swift Package Manager per risolvere le dipendenze nelle build iOS e macOS.
---

# Swift Package Manager

[Swift Package Manager](https://www.swift.org/documentation/package-manager/) è il gestore delle dipendenze integrato in Swift e Xcode. Molti SDK iOS e macOS vengono distribuiti come pacchetti Swift e alcuni non vengono più pubblicati come CocoaPods. Defold non usa Xcode per creare una build del motore, ma il server di build usa Xcode per scaricare e compilare i pacchetti Swift da cui dipende un'estensione. Il risultato viene poi collegato al motore come avviene per le [dipendenze CocoaPods](/manuals/extensions-cocoapods).

CocoaPods e pacchetti Swift possono essere usati nello stesso progetto e persino nella stessa estensione.


## Dichiarazione delle dipendenze {#declaring-dependencies}

Le estensioni native possono includere un file `SwiftPackages.json` nelle cartelle `manifests/ios` e `manifests/osx` per specificare i pacchetti Swift da cui dipendono. Esempio:

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

Il file è in semplice formato JSON. Non devi scrivere un file `Package.swift`: il server di build ne genera uno a partire dai file `SwiftPackages.json` di tutte le estensioni.

Il file contiene i seguenti campi:

* `platform` - Obbligatorio. `"ios"` in `manifests/ios/SwiftPackages.json` e `"osx"` in `manifests/osx/SwiftPackages.json`.
* `minVersion` - Facoltativo. La versione minima di iOS o macOS per cui vengono compilati i pacchetti, per esempio `"15.0"`. Viene usato il valore più alto tra quelli di tutte le estensioni e la versione minima supportata dal motore, sia per compilare i pacchetti sia per collegare il motore.
* `wrapperType` - Facoltativo. `"static"` (predefinito) o `"dynamic"`. Consulta [Collegamento statico e dinamico](#static-and-dynamic-linking) di seguito.
* `packages` - Obbligatorio. Un elenco di pacchetti. Ogni pacchetto contiene i seguenti campi:
  * `url` - L'URL `https://` del repository git del pacchetto. Non sono accettati URL con credenziali, una porta personalizzata o una stringa di query, né URL `ssh`: il repository deve quindi essere accessibile pubblicamente.
  * `products` - I prodotti del pacchetto da collegare al motore. Sono i prodotti di libreria elencati nella sezione `products` del file `Package.swift` del pacchetto. Il nome di un prodotto non coincide necessariamente con il nome del pacchetto o del modulo importato.
  * Esattamente un requisito di versione:
    * `version` - Questa versione esatta, per esempio `"12.16.0"`.
    * `from` - Questa versione o una versione successiva con lo stesso numero di versione principale. Per esempio `"9.0.0"` risolve alla release `9.x.x` più recente.
    * `branch` - Il commit più recente di un branch, per esempio `"main"`.
    * `revision` - Un commit specifico, indicato dall'hash completo di 40 caratteri.

Il server di build raccoglie i file `SwiftPackages.json` di tutte le estensioni e li usa per risolvere tutte le dipendenze, comprese quelle dei pacchetti stessi, includendole nella compilazione del codice nativo.


## Uso dei pacchetti dal codice dell'estensione {#using-packages-from-extension-code}

Gli header dei prodotti sono disponibili al codice sorgente dell'estensione. Usali da file sorgente Objective-C++ (`.mm`). Questo esempio avvia l'SDK [Sentry](https://github.com/getsentry/sentry-cocoa) all'avvio dell'applicazione:

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

* Gli header Objective-C vengono importati come `#import <Module/Header.h>`, dove `Module` è il nome del modulo che li fornisce.
* Le classi implementate in Swift sono dichiarate nell'header generato `<Module/Module-Swift.h>`. Questo contiene soltanto le classi e i metodi che il modulo espone a Objective-C (contrassegnati con `@objc` in Swift). Importa `UIKit` (o `AppKit` su macOS) prima di esso, perché l'header generato ne usa i tipi.


## Dipendenze di più estensioni {#dependencies-of-several-extensions}

Quando più estensioni di un progetto usano pacchetti Swift, tutti i relativi file `SwiftPackages.json` per la piattaforma vengono combinati in un unico grafo di pacchetti:

* I pacchetti con lo stesso URL vengono uniti e i prodotti richiesti vengono combinati.
* Un pacchetto condiviso da più estensioni deve avere lo stesso requisito di versione in tutte. Requisiti diversi, per esempio `"version": "12.16.0"` in un'estensione e `"from": "12.0.0"` in un'altra, fanno fallire la build con un errore `Conflicting requirements for Swift package`.
* Viene usato il valore `minVersion` più alto.
* Tutte le estensioni che impostano `wrapperType` devono impostarlo allo stesso valore.

Un progetto può anche combinare estensioni che usano CocoaPods ed estensioni che usano pacchetti Swift. Entrambi vengono risolti e collegati al motore. Tuttavia lo stesso SDK non deve provenire da entrambi: se un'estensione ottiene Firebase da un `Podfile` e un'altra da un `SwiftPackages.json`, il collegamento del motore fallisce con errori di simboli duplicati. Le estensioni che condividono un SDK dovrebbero usare lo stesso gestore delle dipendenze.


## Blocco delle versioni dei pacchetti {#locking-package-versions}

Quando la build riesce, il server di build restituisce un file `Package.resolved` che elenca la versione e il commit esatti di ogni pacchetto nel grafo, comprese le dipendenze dei pacchetti. Il file viene collocato nella cartella di build del progetto, per esempio `build/arm64-ios/Package.resolved`.

Copia questo file nell'estensione, accanto a `SwiftPackages.json` (per esempio `manifests/ios/Package.resolved`), per bloccare le versioni dei pacchetti. Il server di build usa quindi le versioni bloccate finché soddisfano i requisiti in `SwiftPackages.json`. Ciò velocizza anche la build: senza un file `Package.resolved`, il server scopre le dipendenze dei pacchetti passo per passo, operazione che può richiedere molto tempo per pacchetti con molte dipendenze.

Se più estensioni includono un file `Package.resolved` per la stessa piattaforma, ne viene usato soltanto uno.


## Collegamento statico e dinamico {#static-and-dynamic-linking}

Per impostazione predefinita tutti i pacchetti Swift vengono combinati in una libreria statica, collegata poi all'eseguibile del motore.

Alcuni SDK non possono essere combinati in una libreria statica e il collegamento del motore fallisce con errori di simboli duplicati. In questo caso imposta `"wrapperType": "dynamic"` in `SwiftPackages.json`. I pacchetti vengono quindi compilati in un framework dinamico, incorporato nel bundle dell'applicazione.


## Risorse e manifest della privacy {#resources-and-privacy-manifests}

I bundle di risorse e i manifest della privacy (`PrivacyInfo.xcprivacy`) dei pacchetti vengono inclusi nel bundle dell'applicazione come avviene per le dipendenze CocoaPods.


## Migrazione da CocoaPods {#migrating-from-cocoapods}

Molti SDK vengono pubblicati sia come pod sia come pacchetti Swift. Per migrare un'estensione da un `Podfile` a un file `SwiftPackages.json`:

1. Trova il repository git del pacchetto Swift nella documentazione dell'SDK. Spesso coincide con il repository del pod.
2. Trova i nomi dei prodotti nel file `Package.swift` del pacchetto. I nomi dei pod e quelli dei prodotti sono spesso diversi.
3. Sostituisci il `Podfile` con un file `SwiftPackages.json`. La versione `platform :ios` del `Podfile` diventa `minVersion`.
4. Assicurati che le righe `#import` dell'estensione corrispondano ancora ai nomi dei moduli dei prodotti.

Per esempio, questo `Podfile`:

```
platform :ios, '12.0'
pod 'FBSDKCoreKit', '17.0.0'
pod 'FBSDKLoginKit', '17.0.0'
pod 'FBSDKShareKit', '17.0.0'
pod 'FBSDKGamingServicesKit', '17.0.0'
```

diventa questo `SwiftPackages.json`:

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

In questo caso i moduli mantengono i propri nomi, quindi `#import <FBSDKCoreKit/FBSDKCoreKit.h>` funziona con entrambi.


## Limitazioni {#limitations}

* Sono supportati soltanto repository di pacchetti accessibili pubblicamente tramite `https://`. I registri di pacchetti Swift non sono supportati.
* I file `Package.swift` e i plugin dei pacchetti vengono eseguiti sul server di build senza accesso alla rete. Il server scarica autonomamente i pacchetti e i relativi framework binari prima di compilarli.
* La compilazione di pacchetti contenenti cataloghi di asset (`.xcassets`) per iOS richiede un server di build che usi Xcode 27 o versioni successive. Con una versione precedente di Xcode, la build fallisce con un errore che indica questi pacchetti.
* I file `SwiftPackages.json` di un progetto possono dichiarare al massimo 32 pacchetti e 64 prodotti per piattaforma.


## Risoluzione dei problemi {#troubleshooting}

`'Module/Header.h' file not found` o simboli non definiti
: Controlla che i `products` in `SwiftPackages.json` siano nomi di prodotti presenti in `Package.swift` e che l'header appartenga a uno di essi. Un server di build che non supporta Swift Package Manager ignora `SwiftPackages.json` e la compilazione o il collegamento dell'estensione fallisce nello stesso modo.

`The Swift package graph did not resolve within the ... time budget`
: I pacchetti hanno troppe dipendenze per essere individuate senza un file di blocco. Aggiungi un file `Package.resolved` accanto a `SwiftPackages.json`, come descritto in [Blocco delle versioni dei pacchetti](#locking-package-versions). Poiché la build non è stata completata, crea il file localmente, per esempio aggiungendo gli stessi pacchetti a un progetto Xcode. Xcode memorizza il file in `<project>.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`.


## Server di build locale {#local-build-server}

I pacchetti Swift vengono compilati dal server di build macOS. Per usare pacchetti Swift con un [server di build locale](/manuals/extender-local-setup), sono necessari un'installazione completa di Xcode (i soli Command Line Tools non bastano), [XcodeGen](https://github.com/yonaskolb/XcodeGen) e il supporto a Swift Package Manager abilitato tramite l'impostazione `extender.spm.enabled`. Per ulteriori informazioni, consulta la [documentazione del server di build su GitHub](https://github.com/defold/extender).
