---
title: Estensioni native - manifest delle estensioni
brief: Questo manuale descrive il manifest di un'estensione e le sue relazioni con il manifest dell'applicazione e quello del motore.
---

# File manifest dell'estensione, dell'applicazione e del motore {#extension-application-and-engine-manifest-files}

Il manifest di un'estensione è un file di configurazione con opzioni e definizioni del preprocessore usate per creare la build di una singola estensione. Questa configurazione viene combinata con una configurazione a livello di applicazione e una configurazione di base per il motore Defold stesso.

## Manifest dell'applicazione {#app-manifest}

Il manifest dell'applicazione (estensione del file `.appmanifest`) è una configurazione a livello di applicazione che stabilisce come creare la build del gioco sui server di build. Il manifest dell'applicazione permette di rimuovere le parti del motore che non usi. Se non ti serve un motore fisico, puoi rimuoverlo dall'eseguibile per ridurne le dimensioni. Scopri come escludere le funzionalità inutilizzate [nel manuale sul manifest dell'applicazione](/manuals/app-manifest).

## Manifest del motore {#engine-manifest}

Il motore Defold ha un manifest di build (`build.yml`) incluso in ogni release del motore e dell'SDK Defold. Il manifest stabilisce quali versioni degli SDK usare, quali compilatori, linker e altri strumenti eseguire e quali opzioni predefinite di build e collegamento passare a questi strumenti. Puoi trovare il manifest in share/extender/build_input.yml [su GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Manifest dell'estensione {#extension-manifest}

Il manifest dell'estensione (`ext.manifest`) è invece un file di configurazione specifico per un'estensione. Il manifest dell'estensione stabilisce come compilare e collegare il codice sorgente dell'estensione e quali librerie aggiuntive includere. 

I tre diversi file manifest condividono la stessa sintassi, così da poter essere combinati e controllare completamente il processo di build delle estensioni e del gioco.

Per ogni estensione di cui viene creata la build, i manifest vengono combinati come segue:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Questo permette di modificare il comportamento predefinito del motore e di ogni estensione. Per la fase finale di collegamento, il manifest dell'applicazione viene combinato con quello di Defold:

	manifest = merge(game.appmanifest, build.yml)


### Il file ext.manifest {#the-extmanifest-file}

Oltre al nome dell'estensione, il file manifest può contenere opzioni di compilazione e di collegamento, librerie e framework specifici per ciascuna piattaforma. Se il file *ext.manifest* non contiene una sezione "platforms", oppure una piattaforma non è presente nell'elenco, la build per la piattaforma per cui crei il bundle viene comunque eseguita, ma senza impostare opzioni aggiuntive.

Ecco un esempio:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    arm64_sim-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Chiavi ammesse {#allowed-keys}

Le chiavi ammesse per le opzioni di compilazione specifiche di una piattaforma sono:

* `frameworks` - Framework Apple da includere nella build (iOS e macOS)
* `weakFrameworks` - Framework Apple da includere facoltativamente nella build (iOS e macOS)
* `flags` - Opzioni da passare al compilatore
* `linkFlags` - Opzioni da passare al linker
* `libs` - Librerie aggiuntive da includere durante il collegamento
* `defines` - Definizioni del preprocessore da impostare durante la build
* `aaptExtraPackages` - Nome del pacchetto aggiuntivo da generare (Android)
* `aaptExcludePackages` - Espressioni regolari (o nomi esatti) dei pacchetti da escludere (Android)
* `aaptExcludeResourceDirs` - Espressioni regolari (o nomi esatti) delle directory di risorse da escludere (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Queste opzioni servono a rimuovere elementi definiti in precedenza nel contesto della piattaforma.

A tutte le parole chiave viene applicato un filtro basato su un elenco di valori consentiti. Questo evita la gestione di percorsi non consentiti e l’accesso a file esterni alla cartella dei contenuti caricati per la build.
