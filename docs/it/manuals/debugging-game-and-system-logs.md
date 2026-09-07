---
title: Debug - log di gioco e di sistema
brief: Questo manuale spiega come leggere i log di gioco e di sistema.
---

# Log di gioco e di sistema {#game-and-system-log}

Il log di gioco mostra tutto l'output del motore, delle estensioni native e della logica del tuo gioco. Puoi usare i comandi [print()](/ref/stable/base/#print:...) e [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) negli script e nei moduli Lua per mostrare informazioni nel log di gioco. Puoi usare le funzioni del [namespace `dmLog`](/ref/stable/dmLog/) per scrivere nel log di gioco dalle estensioni native. Puoi leggere il log di gioco dall'editor, da una finestra del terminale, con strumenti specifici della piattaforma o da un file di log.

I log di sistema sono generati dal sistema operativo e possono fornire ulteriori informazioni utili per individuare un problema. Possono contenere tracce dello stack in caso di crash e avvisi di memoria insufficiente.

::: important
La registrazione dei log nella console o sullo schermo mostra informazioni solo nelle build di debug. Nelle build di release il log della console è vuoto, ma puoi abilitare la registrazione su file anche nelle build di release selezionando "Always" per l'impostazione del progetto "Write Log File". Vedi i dettagli di seguito.
:::

## Leggere il log di gioco dall'editor {#reading-the-game-log-from-the-editor}

Quando esegui il gioco localmente dall'editor o tramite una connessione all'[app di sviluppo per dispositivi mobili](/manuals/dev-app), tutto l'output viene mostrato nel pannello della console dell'editor:

![Editor 2](images/editor/editor2_overview.png)

## Leggere il log di gioco dal terminale {#reading-the-game-log-from-the-terminal}

Quando esegui un gioco Defold dal terminale, il log viene mostrato nella finestra del terminale stesso. Su Windows e Linux, digita il nome dell'eseguibile nel terminale per avviare il gioco. Su macOS devi avviare il motore dall'interno del file .app:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Leggere i log di gioco e di sistema con strumenti specifici della piattaforma {#reading-game-and-system-logs-using-platform-specific-tools}

### HTML5

Puoi leggere i log con gli strumenti per sviluppatori forniti dalla maggior parte dei browser.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - <kbd>Menu ▸ More Tools ▸ Developer Tools</kbd>
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - <kbd>Tools ▸ Web Developer ▸ Web Console</kbd>
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - <kbd>Develop ▸ Show JavaScript Console</kbd>

### Android

Puoi usare lo strumento Android Debug Bridge (ADB) per visualizzare i log di gioco e di sistema.

:[Android ADB](../shared/android-adb.md)

Dopo averlo installato e configurato, collega il dispositivo tramite USB, apri un terminale ed esegui:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

Il dispositivo invierà quindi tutto l'output al terminale corrente, insieme ai messaggi stampati dal gioco.

Se vuoi vedere solo l'output delle applicazioni Defold, usa questo comando:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

Hai diverse possibilità per leggere i log di gioco e di sistema su iOS:

1. Puoi usare lo [strumento Console](https://support.apple.com/guide/console/welcome/mac) per leggere i log di gioco e di sistema.
2. Puoi usare il debugger LLDB per collegarti a un gioco in esecuzione sul dispositivo. Per eseguire il debug di un gioco, questo deve essere firmato con un “Apple Developer Provisioning Profile” che includa il dispositivo su cui vuoi eseguire il debug. Crea il bundle del gioco dall'editor e fornisci il profilo di provisioning nella finestra di dialogo del bundle (la creazione di bundle per iOS è disponibile solo su macOS).

Per avviare il gioco e collegare il debugger ti servirà uno strumento chiamato [ios-deploy](https://github.com/phonegap/ios-deploy). Installa il gioco ed eseguine il debug con il seguente comando in un terminale:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

Il comando installerà l'app sul dispositivo, la avvierà e vi collegherà automaticamente un debugger LLDB. Se non hai mai usato LLDB, leggi [Primi passi con LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Leggere il log di gioco dal file di log {#reading-the-game-log-from-the-log-file}

Usa l'impostazione del progetto "Write Log File" in *game.project* per controllare la registrazione dei log su file:

- "Never": non scrivere un file di log.
- "Debug": scrivere un file di log solo per le build di debug.
- "Always": scrivere un file di log sia per le build di debug sia per quelle di release.

Quando la registrazione su file è abilitata, tutto l'output del gioco viene scritto su disco in un file chiamato "`log.txt`". Ecco come estrarre il file se esegui il gioco su un dispositivo:

iOS
: Collega il dispositivo a un computer con macOS e Xcode installati.

  Apri Xcode e vai a <kbd>Window ▸ Devices and Simulators</kbd>.

  Seleziona il dispositivo nell'elenco, quindi seleziona l'app interessata nell'elenco *Installed Apps*.

  Fai clic sull'icona a forma di ingranaggio sotto l'elenco e seleziona <kbd>Download Container...</kbd>.

  ![Scaricare il container](images/debugging/download_container.png)

  Una volta estratto, il container verrà mostrato nel *Finder*. Fai clic con il pulsante destro sul container e seleziona <kbd>Show Package Content</kbd>. Individua il file "`log.txt`", che dovrebbe trovarsi in "`AppData/Documents/`".

Android(
: La possibilità di estrarre il file "`log.txt`" dipende dalla versione del sistema operativo e dal produttore. Ecco una [guida passo passo](https://stackoverflow.com/a/48077004/129360) breve e semplice.
