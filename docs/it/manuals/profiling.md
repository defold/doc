---
title: Profilazione in Defold
brief: Questo manuale spiega gli strumenti di profilazione disponibili in Defold.
---

# Profilazione {#profiling}

Defold include strumenti di profilazione integrati nel motore e nella pipeline di build. Aiutano a individuare problemi di prestazioni, memoria e utilizzo delle risorse. I dati di profilazione raccolti durante l'esecuzione possono essere utilizzati da diversi strumenti:

* Il profilatore di base e il profilatore visivo integrato nel gioco sono disponibili su tutte le piattaforme.
* Il [profilatore Remotery](https://github.com/Celtoys/Remotery) e il profilatore web interattivo dei fotogrammi sono disponibili su piattaforme desktop e mobili.
* Le build HTML5 possono pubblicare gli ambiti di profilazione di Defold tramite la Web Performance API del browser.

L'impostazione **Profiler** nell'[App Manifest](/manuals/app-manifest/#profiler) controlla se il codice del profilatore viene collegato alla build. **Debug Only** è l'opzione predefinita, **None** lo esclude e **Always** lo include sia nelle build di debug sia in quelle di release. Le impostazioni `profiler` in *game.project* controllano il comportamento durante l'esecuzione, ma non reintegrano nella build il codice del profilatore escluso. In particolare, **Track CPU** controlla il campionamento dell'utilizzo della CPU ed è indipendente dalla scelta effettuata nell'App Manifest.

## Il profilatore visivo a runtime {#the-runtime-visual-profiler}

Le build che includono il supporto alla profilazione dispongono di un profilatore visivo a runtime che mostra informazioni in tempo reale sovrapposte all'applicazione in esecuzione:

```lua
function on_reload(self)
    -- Toggle the visual profiler on hot reload.
    profiler.enable_ui(true)
end
```

![Profilatore visivo](images/profiling/visual_profiler.png)

Il profilatore visivo offre diverse funzioni che permettono di modificare il modo in cui presenta i dati:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Consulta il [riferimento API del profilatore](/ref/stable/profiler/) per ulteriori informazioni sulle funzioni del profilatore.

## Il profilatore web {#the-web-profiler}
Durante l'esecuzione di una build desktop o mobile che include il supporto alla profilazione, puoi accedere tramite un browser ai profilatori interattivi dei fotogrammi e delle risorse.

### Profilatore dei fotogrammi Remotery {#remotery-frame-profiler}
Il profilatore dei fotogrammi consente di campionare il gioco durante l'esecuzione e analizzare in dettaglio i singoli fotogrammi. Per accedere al profilatore:

1. Avvia il gioco sul dispositivo di destinazione.
2. Seleziona la voce di menu <kbd> Debug ▸ Open Web Profiler</kbd>.

Il profilatore dei fotogrammi è suddiviso in diverse sezioni, che offrono viste differenti del gioco in esecuzione. Premi il pulsante Pause nell'angolo in alto a destra per interrompere temporaneamente l'aggiornamento delle viste.

![Profilatore web](images/profiling/webprofiler_page.png)

::: sidenote
Quando usi più destinazioni contemporaneamente, puoi passare manualmente dall'una all'altra modificando il campo Connection Address nella parte superiore della pagina, in modo che corrisponda all'URL del profilatore Remotery mostrato nella console all'avvio della destinazione:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: La vista Sample Timeline mostra i dati dei fotogrammi acquisiti nel motore, con una sequenza temporale orizzontale per ogni thread. Main è il thread principale, che esegue tutta la logica del gioco e la maggior parte del codice del motore. Remotery è il thread del profilatore stesso e Sound è quello dedicato al missaggio e alla riproduzione audio. Puoi ingrandire e ridurre la visualizzazione (con la rotella del mouse) e selezionare singoli fotogrammi per esaminarne i dettagli nella vista Frame Data.

  ![Sequenza temporale dei campioni](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: La vista Frame Data è una tabella che mostra in dettaglio tutti i dati del fotogramma attualmente selezionato. Puoi vedere quanti millisecondi vengono impiegati in ciascun ambito del motore.

  ![Dati del fotogramma](images/profiling/webprofiler_frame_data.png)


Global Properties
: La vista Global Properties mostra una tabella di contatori. Permettono, ad esempio, di monitorare facilmente il numero di chiamate di disegno o il numero di componenti di un determinato tipo.

  ![Proprietà globali](images/profiling/webprofiler_global_properties.png)

::: sidenote
Il valore LuaMem è la quantità di memoria in kilobyte utilizzata dalla macchina virtuale Lua, come riportata dal garbage collector di Lua. Memory è la quantità di memoria in kilobyte utilizzata dal motore.
:::

::: important
L'[impostazione Max Sample Count](/manuals/project-settings/#max-sample-count) limita il numero di campioni del profilatore registrati per thread e per fotogramma. Se il profilatore segnala il superamento del limite, controlla prima che nel codice di profilazione delle estensioni native ogni inizio di ambito abbia una fine corrispondente. Aumenta il limite solo quando un fotogramma valido contiene più ambiti di quanti ne consenta il limite configurato.
:::

### Profilatore delle risorse {#resource-profiler}
Il profilatore delle risorse consente di ispezionare il gioco durante l'esecuzione e analizzare in dettaglio l'utilizzo delle risorse. Per accedere al profilatore:

1. Avvia il gioco sul dispositivo di destinazione.
2. Apri un browser e vai all'indirizzo http://localhost:8002

Il profilatore delle risorse è suddiviso in 2 sezioni: una mostra una vista gerarchica delle collezioni, degli oggetti di gioco e dei componenti attualmente istanziati nel gioco, mentre l'altra mostra tutte le risorse attualmente caricate.

![Profilatore delle risorse](images/profiling/webprofiler_resources_page.png)

Vista delle collezioni
: La vista delle collezioni mostra un elenco gerarchico di tutti gli oggetti di gioco e i componenti attualmente istanziati nel gioco e delle collezioni da cui provengono. È uno strumento molto utile quando devi esaminare e capire quali istanze sono presenti nel gioco in un dato momento e da dove provengono gli oggetti.

Vista delle risorse
: La vista delle risorse mostra tutte le risorse attualmente caricate in memoria, le loro dimensioni e il numero di riferimenti a ciascuna risorsa. È utile per ottimizzare l'utilizzo della memoria dell'applicazione quando devi capire che cosa è caricato in memoria in un dato momento.

## Sequenza temporale delle prestazioni nel browser per HTML5 {#html5-browser-performance-timeline}

HTML5 utilizza la Web Performance API al posto di Remotery per la sequenza temporale del browser. Per registrare gli ambiti di Defold:

1. Assicurati che la modalità di profilazione selezionata nell'App Manifest includa il supporto alla profilazione nella variante di build che stai eseguendo.
2. Abilita **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) in *game.project*.
3. Avvia la build HTML5 e apri gli strumenti per sviluppatori del browser.
4. Registra una sessione nel pannello **Performance** del browser ed esamina gli ambiti di Defold nella sequenza temporale risultante.

Questa sequenza temporale del browser è separata sia dal profilatore visivo integrato nel gioco sia dal profilatore web interattivo Remotery.


## Report di build {#build-reports}
Quando crei il bundle del gioco, puoi scegliere di generare un report di build. È molto utile per comprendere le dimensioni di tutti gli asset inclusi nel bundle del gioco. Basta selezionare la casella *Generate build report* durante la creazione del bundle.

![Report di build](images/profiling/build_report.png)

Lo strumento di build produce un file chiamato `report.html` accanto al bundle del gioco. Apri il file in un browser web per consultare il report:

![Report di build](images/profiling/build_report_html.png)

La sezione *Overview* offre una panoramica visiva delle dimensioni del progetto, suddivise per tipo di risorsa.

La sezione *Resources* mostra un elenco dettagliato delle risorse, che puoi ordinare per dimensioni, rapporto di compressione, crittografia, tipo e nome della directory. Usa il campo "search" per filtrare le risorse visualizzate.

La sezione *Structure* mostra le dimensioni in base all'organizzazione delle risorse nella struttura dei file del progetto. Le voci sono contrassegnate da colori che vanno dal verde (leggero) al blu (pesante), in base alle dimensioni relative dei file e del contenuto delle directory.


## Strumenti esterni {#external-tools}
Oltre agli strumenti integrati, sono disponibili numerosi strumenti gratuiti di alta qualità per il tracciamento e la profilazione. Eccone una selezione:

ProFi (Lua)
: Non forniamo un profilatore Lua integrato, ma esistono librerie esterne abbastanza semplici da usare. Per individuare dove i tuoi script impiegano più tempo, inserisci misurazioni dei tempi direttamente nel codice oppure usa una libreria di profilazione Lua come [ProFi](https://github.com/jgrahamc/ProFi).

  Tieni presente che i profilatori scritti interamente in Lua aggiungono un notevole carico a ogni hook che installano. Per questo motivo, valuta con cautela i profili temporali ottenuti con strumenti di questo tipo. I profili basati sui conteggi sono invece sufficientemente accurati.

Instruments (macOS e iOS)
: È uno strumento di analisi e visualizzazione delle prestazioni incluso in Xcode. Consente di tracciare e ispezionare il comportamento di una o più app o processi, esaminare funzionalità specifiche del dispositivo (come Wi-Fi e Bluetooth) e molto altro.

  ![Instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Fa parte del pacchetto "Additional Tools for Xcode", che puoi scaricare da Apple (seleziona <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> nel menu di Xcode).

  Questo strumento consente di ispezionare un'applicazione Defold in esecuzione e vedere come utilizza OpenGL. Permette di tracciare le chiamate alle funzioni OpenGL, impostare punti di interruzione sulle funzioni OpenGL, esaminare le risorse dell'applicazione (texture, programmi, shader ecc.), visualizzare il contenuto dei buffer e controllare altri aspetti dello stato di OpenGL.

  ![Profilatore OpenGL](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Un insieme di strumenti di profilazione che acquisisce in tempo reale dati sull'utilizzo della CPU e della memoria e sull'attività di rete del gioco. Puoi tracciare i metodi eseguiti dal codice mediante campionamento, acquisire dump dell'heap, visualizzare le allocazioni di memoria e ispezionare i dettagli dei file trasmessi in rete. Per usare lo strumento devi impostare `android:debuggable="true"` in `AndroidManifest.xml`.

  ![Android Profiler](images/profiling/android_profiler.png)

  Nota: da Android Studio 4.1 è possibile anche [eseguire gli strumenti di profilazione senza avviare Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  È un insieme di strumenti che consente di ispezionare, modificare e rieseguire le chiamate di un'applicazione a un driver grafico. Per usare lo strumento devi impostare `android:debuggable="true"` in `AndroidManifest.xml`.

  ![Graphics API Debugger](images/profiling/gapid.png)
