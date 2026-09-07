---
title: Debug su Android
brief: Questo manuale descrive come eseguire il debug di una build con Android Studio.
---

# Debug su Android {#debugging-on-android}

Qui descriviamo come eseguire il debug di una build con [Android Studio](https://developer.android.com/studio/), l'IDE ufficiale per Android, il sistema operativo di Google.


## Android Studio

* Prepara il bundle impostando l'opzione `android.debuggable` in *game.project*

	![android.debuggable](images/extensions/debugging/android/game_project_debuggable.png)

* Crea il bundle dell'app in modalità debug in una cartella a tua scelta.

	![Creazione del bundle Android](images/extensions/debugging/android/bundle_android.png)

* Avvia [Android Studio](https://developer.android.com/studio/)

* Scegli `Profile or debug APK`

	![Debug dell'APK](images/extensions/debugging/android/android_profile_or_debug.png)

* Scegli il bundle APK che hai appena creato

	![Selezione dell'APK](images/extensions/debugging/android/android_select_apk.png)

* Seleziona il file `.so` principale e assicurati che contenga i simboli di debug

	![Selezione del file .so](images/extensions/debugging/android/android_missing_symbols.png)

* Se non li contiene, carica un file `.so` da cui non siano stati rimossi i simboli di debug. (La dimensione è di circa 20 MB)

* Le mappature dei percorsi consentono di associare i singoli percorsi usati per compilare l'eseguibile nel cloud a una cartella effettiva sul tuo disco locale.

* Seleziona il file .so, quindi aggiungi una mappatura verso il tuo disco locale

	![Mappatura dei percorsi 1](images/extensions/debugging/android/path_mappings_android.png)

	![Mappatura dei percorsi 2](images/extensions/debugging/android/path_mappings_android2.png)

* Se hai accesso al codice sorgente del motore, aggiungi una mappatura dei percorsi anche per quello.

* Assicurati di passare alla versione di cui stai eseguendo il debug

	defold$ git checkout 1.2.148

* Premi `Apply changes`

* Ora dovresti vedere il codice sorgente mappato nel tuo progetto

	![Codice sorgente](images/extensions/debugging/android/source_mappings_android.png)

* Aggiungi un punto di interruzione

	![Punto di interruzione](images/extensions/debugging/android/breakpoint_android.png)

* Premi `Run` -> `Debug "Appname"` ed esegui il codice nel quale vuoi interrompere l'esecuzione

	![Punto di interruzione](images/extensions/debugging/android/callstack_variables_android.png)

* Ora puoi procedere passo per passo nello stack di chiamate e ispezionare le variabili


## Note {#notes}

### Cartella del job di un'estensione nativa {#native-extension-job-folder}

Attualmente, questo flusso di lavoro è un po' scomodo per lo sviluppo. Il nome della cartella del job
è casuale per ogni build, rendendo la mappatura dei percorsi non valida a ogni nuova build.

Tuttavia, funziona bene per una sessione di debug.

Le mappature dei percorsi vengono memorizzate nel file di progetto `.iml` del progetto Android Studio.

È possibile ricavare la cartella del job dall'eseguibile

```sh
$ arm-linux-androideabi-readelf --string-dump=.debug_str build/armv7-android/libdmengine.so | grep /job
```

La cartella del job ha un nome come `job1298751322870374150`, con un numero casuale ogni volta.

