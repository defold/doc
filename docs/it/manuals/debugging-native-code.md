---
title: Debug del codice nativo in Defold
brief: Questo manuale spiega come eseguire il debug del codice nativo in Defold.
---

# Debug del codice nativo {#debugging-native-code}

Defold è sottoposto a numerosi test e, in condizioni normali, dovrebbe andare in crash molto raramente. È tuttavia impossibile garantire che non si verifichino mai crash, soprattutto se il tuo gioco utilizza estensioni native. Se riscontri crash o codice nativo che non si comporta come previsto, puoi procedere in diversi modi:

* Usa un debugger per eseguire il codice passo passo
* Esegui il debug tramite messaggi di stampa
* Analizza un log di crash
* Risolvi i simboli di uno stack di chiamate


## Usare un debugger {#use-a-debugger}

Il metodo più comune consiste nell'eseguire il codice tramite un `debugger`. Questo consente di eseguire il codice passo passo, impostare punti di interruzione (`breakpoints`) e interrompe l'esecuzione in caso di crash.

Sono disponibili diversi debugger per ogni piattaforma.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Ogni strumento consente di eseguire il debug su determinate piattaforme:

* Visual studio - Windows + piattaforme che supportano gdbserver (ad esempio Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + piattaforme che supportano gdbserver
* Xcode -  macOS, iOS ([ulteriori informazioni](/manuals/debugging-native-code-ios))
* Android Studio - Android ([ulteriori informazioni](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (tramite lldb)


## Eseguire il debug tramite messaggi di stampa {#use-print-debugging}

Il modo più semplice per eseguire il debug del codice nativo è usare [messaggi di stampa](http://en.wikipedia.org/wiki/Debugging#Techniques). Usa le funzioni del [namespace `dmLog`](/ref/stable/dmLog/) per osservare le variabili o indicare il flusso di esecuzione. Tutte le funzioni di log stampano nella vista *Console* dell'editor e nel [log del gioco](/manuals/debugging-game-and-system-logs).


## Analizzare un log di crash {#analyze-a-crash-log}

Il motore Defold salva un file `_crash` se si verifica un crash irreversibile. Il file contiene informazioni sul sistema e sul crash. L'[output del log del gioco](/manuals/debugging-game-and-system-logs) indica dove si trova il file di crash (la posizione varia a seconda del sistema operativo, del dispositivo e dell'applicazione).

Puoi usare il [modulo crash](https://www.defold.com/ref/crash/) per leggere questo file nella sessione successiva. Si consiglia di leggere il file, raccogliere le informazioni, stamparle nella console e inviarle a un [servizio di analisi](/tags/stars/analytics/) che supporti la raccolta dei log di crash.

::: important
Su Windows viene generato anche un file `_crash.dmp`. Questo file è utile per il debug di un crash.
:::

### Recuperare il log di crash da un dispositivo {#getting-the-crash-log-from-a-device}

Se si verifica un crash su un dispositivo mobile, puoi scaricare il file di crash sul tuo computer e analizzarlo localmente.

#### Android

Se l'app [consente il debug](/manuals/project-settings/#android), puoi recuperare il log di crash usando lo [strumento Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) e il comando `adb shell`:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

In iTunes puoi visualizzare/scaricare il container di un'app.

Nella finestra `Xcode -> Devices` puoi anche selezionare i log di crash


## Risolvere i simboli di uno stack di chiamate {#symbolicate-a-callstack}

Se ottieni uno stack di chiamate da un file `_crash` o da un [file di log](/manuals/debugging-game-and-system-logs), puoi risolverne i simboli. Questo significa convertire ogni indirizzo nello stack di chiamate in un nome di file e un numero di riga, facilitando così l'individuazione della causa del problema.

È importante associare allo stack di chiamate il motore corretto, altrimenti rischi di indagare sul codice sbagliato! Usa l'opzione [`--with-symbols`](https://www.defold.com/manuals/bob/) quando crei un bundle con [Bob](https://www.defold.com/manuals/bob/) oppure seleziona la casella "Generate debug symbols" nella finestra di creazione del bundle dell'editor:

* iOS - la cartella `dmengine.dSYM.zip` in `build/arm64-ios` contiene i simboli di debug per le build iOS.
* macOS - la cartella `dmengine.dSYM.zip` in `build/x86_64-macos` contiene i simboli di debug per le build macOS.
* Android - la cartella di output del bundle `projecttitle.apk.symbols/lib/` contiene i simboli di debug per le architetture di destinazione.
* Linux - l'eseguibile contiene i simboli di debug.
* Windows - il file `dmengine.pdb` in `build/x86_64-win32` contiene i simboli di debug per le build Windows.
* HTML5 - la directory `<project_name>_symbols` accanto al bundle HTML5 contiene `<project_name>_wasm.js.symbols` e, quando è selezionata l'architettura `wasm_pthread-web`, `<project_name>_pthread_wasm.js.symbols`.

::: important
È fondamentale conservare i simboli di debug per ogni release pubblica del tuo gioco e sapere a quale release appartengono. Senza i simboli di debug non potrai analizzare alcun crash del codice nativo! Dovresti inoltre conservare una versione `unstripped` del motore, cioè con i simboli ancora presenti. Questo permette di risolvere al meglio i simboli dello stack di chiamate.
:::


### Caricare i simboli su Google Play {#uploading-symbols-to-google-play}
Puoi [caricare i simboli di debug su Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) affinché i crash registrati in Google Play mostrino gli stack di chiamate con i simboli risolti. Comprimi in un archivio ZIP il contenuto della cartella di output del bundle `projecttitle.apk.symbols/lib/`. La cartella include una o più sottocartelle con nomi di architetture come `arm64-v8a`, `armeabi-v7a` e `x86_64`.


### Risolvere i simboli di uno stack di chiamate Android {#symbolicate-an-android-callstack}

1. Recupera il motore dalla cartella della build

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Estrai l'archivio in una cartella:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Trova l'indirizzo nello stack di chiamate

	Ad esempio, nello stack di chiamate con i simboli ancora da risolvere potrebbe apparire così

	`#00 pc 00257224 libmy_game_name.so`

	Dove *`00257224`* è l'indirizzo

4. Risolvi l'indirizzo

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Nota: se ottieni una traccia dello stack dai [log di Android](/manuals/debugging-game-and-system-logs), potresti riuscire a risolverne i simboli usando [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Risolvere i simboli di uno stack di chiamate iOS {#symbolicate-an-ios-callstack}

1. Se utilizzi estensioni native, il server può fornirti i simboli (.dSYM) (passa `--with-symbols` a bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Se non utilizzi estensioni native, scarica i simboli del motore standard:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Risolvi i simboli usando l'indirizzo di caricamento

	Per qualche motivo, inserire soltanto l'indirizzo dello stack di chiamate non funziona (cioè con indirizzo di caricamento 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Non funziona nemmeno specificare direttamente l'indirizzo di caricamento

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Sommare l'indirizzo di caricamento all'indirizzo funziona:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
