---
title: Debug su iOS/macOS
brief: Questo manuale descrive come eseguire il debug di una build con Xcode.
---

# Debug su iOS/macOS {#debugging-on-iosmacos}

Qui descriviamo come eseguire il debug di una build con [Xcode](https://developer.apple.com/xcode/), l'IDE consigliato da Apple per sviluppare per macOS e iOS.

## Xcode

* Crea il bundle dell'app con Bob, usando l'opzione `--with-symbols` ([maggiori informazioni](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Installa l'app con `Xcode`, `iTunes` o [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Procurati la cartella `.dSYM` (cioè i simboli di debug)

	* Se l'app non usa estensioni native, puoi scaricare il file `.dSYM` da [d.defold.com](http://d.defold.com)

	* Se usi un'estensione nativa, la cartella `.dSYM` viene generata quando crei una build con [bob.jar](https://www.defold.com/manuals/bob/). È sufficiente creare la build (senza archiviarla né creare un bundle):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Creare il progetto {#create-project}

Per eseguire correttamente il debug, occorre avere un progetto e mappare il codice sorgente.
Questo progetto serve soltanto per il debug, non per creare build.

* Crea un nuovo progetto Xcode e scegli il modello `Game`

	![Modello del progetto](images/extensions/debugging/ios/project_template.png)

* Scegli un nome (ad esempio `debug`) e le impostazioni predefinite

* Scegli una cartella in cui salvare il progetto

* Aggiungi il tuo codice all'app

	![Aggiunta di file](images/extensions/debugging/ios/add_files.png)

* Assicurati che "Copy items if needed" sia deselezionato.

	![Aggiunta del codice sorgente](images/extensions/debugging/ios/add_source.png)

* Questo è il risultato finale

	![Codice sorgente aggiunto](images/extensions/debugging/ios/added_source.png)


* Disabilita il passaggio `Build`

	![Modifica dello schema](images/extensions/debugging/ios/edit_scheme.png)

	![Disabilitazione della build](images/extensions/debugging/ios/disable_build.png)

* Imposta la versione di `Deployment target` in modo che sia superiore alla versione di iOS del tuo dispositivo

	![Versione di distribuzione](images/extensions/debugging/ios/deployment_version.png)

* Seleziona il dispositivo di destinazione

	![Selezione del dispositivo](images/extensions/debugging/ios/select_device.png)


### Avviare il debugger {#launch-the-debugger}

Hai diverse opzioni per eseguire il debug di un'app

1. Puoi scegliere `Debug` -> `Attach to process...` e selezionare l'app da lì

2. Oppure scegliere `Attach to process by PID or Process name`

	![Selezione del dispositivo](images/extensions/debugging/ios/attach_to_process_name.png)

3. Avvia l'app sul dispositivo

4. In `Edit Scheme` aggiungi la cartella <AppName>.app come eseguibile

### Simboli di debug {#debug-symbols}

**Per usare lldb, l'esecuzione deve essere in pausa**

* Aggiungi il percorso di `.dSYM` a lldb

```
(lldb) add-dsym <PathTo.dSYM>
```

	![Aggiunta di dSYM](images/extensions/debugging/ios/add_dsym.png)

* Verifica che `lldb` abbia letto correttamente i simboli

```
(lldb) image list <AppName>
```

### Mappatura dei percorsi {#path-mappings}

* Aggiungi il codice sorgente del motore (adatta i percorsi alle tue esigenze)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* Puoi ricavare dall'eseguibile la cartella del job. Il nome della cartella è `job1298751322870374150`, con un numero casuale diverso ogni volta.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Verifica le mappature del codice sorgente

```
(lldb) settings show target.source-map
```

Puoi verificare da quale file sorgente proviene un simbolo usando

```
(lldb) image lookup -va <SymbolName>
```

### Punti di interruzione {#breakpoints}

* Apri un file nella vista del progetto e imposta un punto di interruzione

	![Punto di interruzione](images/extensions/debugging/ios/breakpoint.png)

## Note {#notes}

### Verificare l'UUID del file binario {#check-uuid-of-binary}

Affinché il debugger accetti la cartella `.dSYM`, l'UUID deve corrispondere a quello dell'eseguibile di cui stai eseguendo il debug. Puoi verificare l'UUID in questo modo:

```sh
$ dwarfdump -u <PathToBinary>
```