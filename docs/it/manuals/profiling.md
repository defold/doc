---
title: Profilazione in Defold
brief: Questo manuale spiega gli strumenti di profilazione disponibili in Defold.
---

# Profilazione {#profiling}

Defold include strumenti di profilazione integrati nel motore e nella pipeline di build. Aiutano a individuare problemi di prestazioni, memoria e utilizzo delle risorse. I dati di profilazione raccolti durante l'esecuzione possono essere utilizzati da diversi strumenti:

* Il profilatore di base e il profilatore visivo integrato nel gioco sono disponibili su tutte le piattaforme.
* Il [profilatore Remotery](https://github.com/Celtoys/Remotery) e il profilatore web interattivo dei fotogrammi sono disponibili su piattaforme desktop e mobili.
* Le build di debug macOS che usano Metal possono salvare [tracce GPU](#metal-gpu-trace-capture) da ispezionare in Xcode.
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

Consulta il [riferimento API del profilatore](/ref/profiler/) per ulteriori informazioni sulle funzioni del profilatore.

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

1. Avvia una build di debug del gioco sul dispositivo di destinazione.
2. Apri l'[indirizzo del servizio del motore](/manuals/engine-service/#availability-and-port-discovery) in un browser: `http://<address>:<port>/`. Usa l'indirizzo e la porta riportati nella console dal motore in esecuzione.

Il profilatore delle risorse è suddiviso in 2 sezioni: una mostra una vista gerarchica delle collezioni, degli oggetti di gioco e dei componenti attualmente istanziati nel gioco, mentre l'altra mostra tutte le risorse attualmente caricate.

![Profilatore delle risorse](images/profiling/webprofiler_resources_page.png)

Vista delle collezioni
: La vista delle collezioni mostra un elenco gerarchico di tutti gli oggetti di gioco e i componenti attualmente istanziati nel gioco e delle collezioni da cui provengono. È uno strumento molto utile quando devi esaminare e capire quali istanze sono presenti nel gioco in un dato momento e da dove provengono gli oggetti.

Vista delle risorse
: La vista delle risorse mostra tutte le risorse attualmente caricate in memoria, le loro dimensioni e il numero di riferimenti a ciascuna risorsa. È utile per ottimizzare l'utilizzo della memoria dell'applicazione quando devi capire che cosa è caricato in memoria in un dato momento.

#### Tempi di caricamento delle risorse {#resource-loading-times}

Puoi anche ispezionare quanto impiegano a caricarsi le singole risorse. Abilita [Resource → Profile](/manuals/project-settings/#profile) in *game.project* prima di avviare il gioco. Nella vista testuale, l'impostazione è:

```ini
[resource]
profile = 1
```

L'impostazione è disabilitata per impostazione predefinita. Riavvia il gioco dopo averla abilitata per misurare i caricamenti iniziali. Ogni caricamento completato o fallito scrive una voce di log di livello INFO con il percorso della risorsa, il tempo totale e i tempi delle fasi di precaricamento, lettura, creazione, post-creazione, accodamento e attesa. Gli accessi soddisfatti dalla cache non producono nuove registrazioni di caricamento.

Nel profiler delle risorse, fai clic su **Capture**, quindi su **Show load times** per mostrare le colonne dei tempi. **Capture** aggiorna la vista delle misurazioni conservate; non abilita la profilazione né misura retroattivamente i caricamenti precedenti.

| Colonna | Significato |
| --- | --- |
| **Load (ms)** | Tempo totale trascorso per il caricamento iniziale, comprese dipendenze, operazioni di post-creazione, accodamento e attesa. |
| **Preload (ms)** | Tempo impiegato per preparare la risorsa nel callback di precaricamento. |
| **Read (ms)** | Tempo impiegato per leggere i dati della risorsa. |
| **Create (ms)** | Tempo impiegato per creare la risorsa a runtime nel callback di creazione. |

Mostrare i tempi di caricamento ordina la tabella per tempo totale, con le risorse più lente per prime. Fai clic sull'intestazione di una colonna dei tempi per ordinare in base a quella fase; fai di nuovo clic per invertire l'ordine. Le barre nella colonna **Load** mostrano ogni totale in rapporto alla risorsa visibile più lenta. Fai clic su **Hide load times** per nascondere nuovamente le colonne.

I tempi di caricamento e dei callback includono tutte le operazioni sulle dipendenze annidate. Non sommare i totali tra risorse per calcolare il tempo di avvio, perché lo stesso lavoro può comparire nelle misurazioni di più risorse. Le colonne **Preload**, **Read** e **Create** non coprono inoltre l'intero tempo totale di caricamento; le fasi aggiuntive sono riportate nel log.

Un trattino lungo (`—`) indica che non è disponibile una misurazione completata, per esempio perché la profilazione era disabilitata o il caricamento iniziale non è terminato. Uno zero misurato viene mostrato come `0.000`. Le misurazioni descrivono il caricamento iniziale: gli accessi alla cache e gli hot reload le lasciano invariate, mentre scaricare una risorsa rimuove la sua misurazione conservata.

## Acquisizione delle tracce GPU Metal {#metal-gpu-trace-capture}

Il [servizio HTTP del motore](/manuals/engine-service/#metal-gpu-trace-endpoint) può acquisire i comandi GPU Metal in un documento *.gputrace* su macOS. Apri la traccia completata in Xcode per ispezionare i frame acquisiti. Questa funzionalità è integrata nel motore di debug.

### Avvio e verifica del supporto {#launch-and-check-support}

Crea un [bundle di debug](/manuals/bundling/#release-vs-debug) macOS con il backend grafico Metal nativo incluso. Se usi un App Manifest, seleziona un'opzione **Graphics (macOS)** che includa Metal; consulta [backend grafici](/manuals/app-manifest/#graphics).

Avvia l'eseguibile del bundle da un terminale con `METAL_CAPTURE_ENABLED=1` e seleziona l'adattatore Metal. Sostituisci il percorso del bundle e il nome dell'eseguibile in questo esempio:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

La variabile d'ambiente deve essere impostata quando il motore si avvia. Impostarla soltanto nel terminale usato per le richieste HTTP non abilita l'acquisizione in un motore già in esecuzione.

In un secondo terminale, usa la [porta del servizio del motore stampata nel log](/manuals/engine-service/#availability-and-port-discovery). Gli esempi seguenti usano `curl` e `jq`:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

La route viene registrata soltanto su macOS. Una voce `null` nel documento OpenAPI indica che questo motore non la espone. Anche quando la route è presente, il supporto per l'acquisizione dipende dall'adattatore grafico e dall'ambiente di avvio. `GET /profiler/gputrace` restituisce HTTP 501 con `error.code: "gputrace_unsupported"` quando l'acquisizione Metal non è disponibile. Prima di procedere, controlla che il motore usi Metal e sia stato avviato con `METAL_CAPTURE_ENABLED=1`. Una richiesta supportata restituisce HTTP 200 con lo stato dell'acquisizione.

### Acquisizione e ispezione dei frame {#capture-and-inspect-frames}

Scegli un percorso di uscita assoluto e scrivibile che termini in `.gputrace`, con una directory genitore esistente e senza una traccia già presente in quel percorso. Il percorso si trova sul computer che esegue il motore. Per un motore locale, questo esempio crea una nuova directory temporanea e richiede un frame:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` è facoltativo, ha come valore predefinito `1` e accetta interi da `1` a `10000`. L'acquisizione inizia prima del frame renderizzato successivo e termina dopo l'invio del numero richiesto di frame completi. Mantieni attivo il rendering del gioco durante l'attesa. Può esserci una sola acquisizione in attesa o attiva; un'altra richiesta di avvio restituisce HTTP 409 con `error.code: "gputrace_active"`.

`POST` restituisce HTTP 200 con `ok: true` e `data.state: "pending"` quando l'acquisizione viene pianificata. Il completamento viene riportato dalle successive richieste di stato. Ripeti la richiesta di stato finché `data.state` non diventa `complete`, `canceled` o `failed`:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Significato |
| --- | --- |
| `idle` | Nessuna acquisizione è stata pianificata. |
| `pending` | L'acquisizione attende l'inizio del rendering. |
| `capturing` | L'acquisizione è attiva; `data.frames_captured` riporta i frame completati. |
| `complete` | L'acquisizione è terminata e la traccia può essere aperta. |
| `canceled` | Un'acquisizione in attesa è stata annullata prima di iniziare. |
| `failed` | L'acquisizione non è riuscita ad avviarsi; esamina `data.error` per l'errore nativo. |

`GET` descrive l'acquisizione corrente o più recente. Controlla che `data.path` corrisponda al percorso richiesto. Un'acquisizione fallita restituisce comunque HTTP 200 con `ok: true`; esamina `data.state` e `data.error` per determinarne il risultato. Per un client automatico, interroga il servizio con un intervallo e un timeout.

Quando lo stato è `complete`, apri la traccia in Xcode sul Mac del motore:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

L'endpoint HTTP restituisce lo stato; la traccia viene salvata in `data.path` sull'host del motore. Per un motore remoto, recupera il documento completato da quell'host prima di aprirlo localmente.

### Annullamento o arresto di un'acquisizione {#cancel-or-stop-a-capture}

Per annullare un'acquisizione in attesa o terminare anticipatamente un'acquisizione attiva:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Un'acquisizione in attesa passa a `canceled`. Per un'acquisizione attiva, `data.stop_requested` diventa `true` e l'acquisizione termina dopo l'invio del frame attualmente renderizzato. Continua a interrogare `GET` fino a uno stato finale. `DELETE` lascia su disco ogni traccia già scritta. Se non ci sono acquisizioni in attesa o attive, restituisce HTTP 409 con `error.code: "gputrace_inactive"`.

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
