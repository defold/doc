---
title: Creazione del bundle di un'applicazione
brief: Questo manuale spiega come creare il bundle di un'applicazione.
---

# Creazione del bundle di un'applicazione {#bundling-an-application}

Durante lo sviluppo dell'applicazione, prendi l'abitudine di testare il gioco sulle piattaforme di destinazione il più spesso possibile. Questo ti permette di individuare i problemi di prestazioni nelle prime fasi dello sviluppo, quando è molto più facile risolverli. È inoltre consigliabile testare il gioco su tutte le piattaforme di destinazione per rilevare differenze di comportamento, ad esempio negli shader. Quando sviluppi per dispositivi mobili, puoi usare l'[app di sviluppo per dispositivi mobili](/manuals/dev-app/) per inviare contenuti all'app, evitando di dover creare ogni volta un bundle completo e disinstallare e reinstallare l'app.

Puoi creare il bundle di un'applicazione per tutte le piattaforme supportate da Defold direttamente dall'editor Defold, senza bisogno di strumenti esterni. Puoi anche creare il bundle dalla riga di comando usando i nostri strumenti a riga di comando. La creazione del bundle di un'applicazione richiede una connessione di rete se il progetto contiene una o più [estensioni native](/manuals/extensions).

## Creazione del bundle dall'editor {#bundling-from-within-the-editor}

Per creare il bundle di un'applicazione, usa l'opzione Bundle nel menu Project:

![](images/bundling/bundle_menu.png)

Selezionando una qualsiasi delle opzioni del menu, si apre la finestra di dialogo Bundle per la piattaforma corrispondente.

### Report di build {#build-reports}

Quando crei il bundle del gioco, puoi scegliere di generare un report di build. È molto utile per conoscere le dimensioni di tutti gli asset inclusi nel bundle del gioco. Basta selezionare la casella *Generate build report* durante la creazione del bundle.

![report di build](images/profiling/build_report.png)

Per saperne di più sui report di build, consulta il [manuale sulla profilazione](/manuals/profiling/#build-reports).

### Android

La creazione del bundle di un'applicazione Android (file .apk) è descritta nel [manuale Android](/manuals/android/#creating-an-android-application-bundle).

### iOS

La creazione del bundle di un'applicazione iOS (file .ipa) è descritta nel [manuale iOS](/manuals/ios/#creating-an-ios-application-bundle).

### macOS

La creazione del bundle di un'applicazione macOS (file .app) è descritta nel [manuale macOS](/manuals/macos).

### Linux

La creazione del bundle di un'applicazione Linux non richiede una preparazione specifica né configurazioni opzionali della piattaforma in *game.project*, il [file delle impostazioni del progetto](/manuals/project-settings/).

### Windows

La creazione del bundle di un'applicazione Windows (file .exe) è descritta nel [manuale Windows](/manuals/windows).

### HTML5

La creazione del bundle di un'applicazione HTML5 e le configurazioni opzionali sono descritte nel [manuale HTML5](/manuals/html5/#creating-html5-bundle).

#### Facebook Instant Games

Puoi creare una versione speciale del bundle di un'applicazione HTML5 destinata a Facebook Instant Games. Questo processo è descritto nel [manuale Facebook Instant Games](/manuals/instant-games/).

## Creazione del bundle dalla riga di comando {#bundling-from-the-command-line}

L'editor usa il nostro strumento a riga di comando [Bob](/manuals/bob/) per creare il bundle dell'applicazione.

Durante lo sviluppo quotidiano dell'applicazione, probabilmente crei build e bundle dall'editor Defold. In altre circostanze, potresti voler generare automaticamente i bundle dell'applicazione, ad esempio creando build in serie per tutte le piattaforme di destinazione quando pubblichi una nuova versione, oppure creando build notturne dell'ultima versione del gioco, magari in un ambiente di integrazione continua (CI). Puoi creare build e bundle di un'applicazione al di fuori del normale flusso di lavoro dell'editor usando lo [strumento a riga di comando Bob](/manuals/bob/).

## Struttura del bundle {#the-bundle-layout}

La struttura logica di un bundle è la seguente:

![](images/bundling/bundle_schematic_01.png)

Un bundle viene generato in una cartella. A seconda della piattaforma, questa cartella può anche essere compressa in un archivio ZIP con estensione `.apk` o `.ipa`.
Il contenuto della cartella dipende dalla piattaforma.

Oltre ai file eseguibili, il nostro processo di creazione del bundle raccoglie anche gli asset necessari per la piattaforma (ad esempio, i file di risorse .xml per Android).

Con l'impostazione [bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources), puoi specificare gli asset da inserire nel bundle senza modifiche.
Puoi configurare questa impostazione per ciascuna piattaforma.

Gli asset del gioco si trovano nel file `game.arcd` e sono compressi singolarmente con l'algoritmo LZ4.
Con l'impostazione [custom_resources](https://defold.com/manuals/project-settings/#custom-resources), puoi specificare gli asset da inserire, compressi, in `game.arcd`.
Puoi accedere a questi asset tramite la funzione [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource).

## Build di release e di debug {#release-vs-debug}

Quando crei il bundle di un'applicazione, puoi scegliere tra un bundle di debug e uno di release. Le differenze tra i due bundle sono piccole, ma è importante tenerle presenti:

* Le build di release non includono il [profilatore](/manuals/profiling) per impostazione predefinita. Imposta **Profiler** su **Always** nel [manifest dell'applicazione](/manuals/app-manifest/#profiler) per includere il supporto al profilatore sia nelle build di debug sia in quelle di release.
* Le build di release non includono il [registratore dello schermo](/ref/stable/sys/#start_record)
* Le build di release non mostrano l'output delle chiamate a `print()` né quello delle estensioni native
* Le build di release hanno il valore `is_debug` in `sys.get_engine_info()` impostato su `false`
* Le build di release non risalgono alle stringhe originali dei valori `hash` quando viene chiamata `tostring()`. In pratica, una chiamata a `tostring()` per un valore di tipo `url` o `hash` restituisce la sua rappresentazione numerica anziché la stringa originale (`'hash: [/camera_001]'` rispetto a `'hash: [11844936738040519888 (unknown)]'`)
* Le build di release non possono essere selezionate come destinazione dall'editor per l'[hot reload](/manuals/hot-reload) e funzionalità simili


