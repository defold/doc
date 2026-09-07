---
title: Impostazioni del progetto Defold
brief: Questo manuale descrive il funzionamento delle impostazioni specifiche del progetto in Defold.
---

# Impostazioni del progetto {#project-settings}

Il file *game.project* contiene tutte le impostazioni che si applicano all'intero progetto. Deve trovarsi nella cartella radice del progetto e deve chiamarsi *game.project*. La prima cosa che fa il motore quando si avvia e lancia il gioco è cercare questo file.

Ogni impostazione del file appartiene a una categoria. Quando apri il file, Defold mostra tutte le impostazioni raggruppate per categoria.

![Impostazioni del progetto](images/project-settings/settings.jpg)


## Formato del file {#file-format}

Le impostazioni in *game.project* si modificano solitamente da Defold, ma puoi anche modificare il file con qualsiasi editor di testo standard. Il file segue lo standard del formato INI e ha questo aspetto:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Un esempio concreto è:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

che indica che l'impostazione *main_collection* appartiene alla categoria *bootstrap*. Ogni volta che si usa un riferimento a un file, come nell'esempio precedente, occorre aggiungere il carattere 'c' alla fine del percorso, per indicare che si fa riferimento alla versione compilata del file. Inoltre, la cartella che contiene *game.project* è la radice del progetto: per questo il percorso dell'impostazione inizia con '/'.


## Accesso a runtime {#runtime-access}

Puoi leggere i valori di *game.project* durante l'esecuzione usando [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) e [`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean). Esempi:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
La chiave è formata dal nome della categoria e da quello dell'impostazione, separati da un punto e scritti in minuscolo, sostituendo gli eventuali spazi con trattini bassi. Esempi: il campo "Title" della categoria "Project" diventa `project.title` e il campo "Gravity Y" della categoria "Physics" diventa `physics.gravity_y`.
:::


## Sezioni e impostazioni {#sections-and-settings}

Di seguito sono elencate tutte le impostazioni disponibili, suddivise per categoria.

### Project

#### Title
Il titolo dell'applicazione.

#### Version
La versione dell'applicazione.

#### Publisher
Nome dell'editore del gioco.

#### Developer
Nome dello sviluppatore.

#### Write Log File
Controlla quando il motore scrive un file di log. Opzioni:

- "Never": non scrive un file di log.
- "Debug": scrive un file di log solo per le build di debug.
- "Always": scrive un file di log sia per le build di debug sia per quelle di release.

Se esegui più istanze dall'editor, il file si chiamerà *instance_2_log.txt*, dove `2` è l'indice dell'istanza. Se esegui una sola istanza o avvii l'applicazione da un bundle, il file si chiamerà *log.txt*. Il file di log si troverà in uno dei seguenti percorsi (provati nell'ordine indicato):

1. Il percorso specificato in *project.log_dir* (impostazione nascosta)
2. Il percorso dei log di sistema:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Altri: radice dell'applicazione
3. Il percorso di supporto dell'applicazione
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (ad esempio `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: variabile d'ambiente `HOME`

#### Minimum Log Level
Specifica il livello minimo per il sistema di log. Verranno mostrati solo i messaggi di log di questo livello o di un livello superiore.

#### Compress Archive
Abilita la compressione degli archivi durante la creazione dei bundle. Attualmente si applica a tutte le piattaforme tranne Android, dove l'apk contiene già tutti i dati compressi.

#### Dependencies
Un elenco degli URL *Library URL* del progetto. Per ulteriori informazioni, consulta il [manuale delle librerie](/manuals/libraries/).

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

Il caricamento delle risorse personalizzate è descritto più in dettaglio nel [manuale sull'accesso ai file](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

Il caricamento delle risorse del bundle è descritto più in dettaglio nel [manuale sull'accesso ai file](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Exclude Resources
`bundle_exclude_resources`
Un elenco separato da virgole delle risorse da escludere dal bundle. Queste vengono rimosse dall'insieme raccolto nella fase `bundle_resources`.

---

### Bootstrap

#### Main Collection
Riferimento al file della collezione da usare per avviare l'applicazione; il valore predefinito è `/logic/main.collection`.

#### Render
Il file di configurazione del rendering da usare, che definisce la pipeline di rendering; il valore predefinito è `/builtins/render/default.render`.

---

### Library

#### Include Dirs
Un elenco separato da spazi delle directory del progetto da condividere tramite la condivisione delle librerie. Per ulteriori informazioni, consulta il [manuale delle librerie](/manuals/libraries/).

---

### Script

#### Shared State
Seleziona questa opzione per condividere un unico stato Lua tra tutti i tipi di script.

---

### Engine

#### Run While Iconified
Consente al motore di continuare a funzionare quando la finestra dell'applicazione è ridotta a icona (solo sulle piattaforme desktop).

#### Fixed Update Frequency
La frequenza di aggiornamento della funzione del ciclo di vita `fixed_update(self, dt)`, espressa in hertz.

#### Max Time Step
Se il passo temporale diventa troppo grande durante un singolo frame, viene limitato a questo valore massimo, espresso in secondi.

---

### Display

#### Width
La larghezza in pixel della finestra dell'applicazione.

#### Height
L'altezza in pixel della finestra dell'applicazione.

#### High Dpi
Crea un back buffer ad alta densità di pixel sugli schermi che lo supportano. In genere il gioco viene renderizzato a una risoluzione doppia rispetto a quella definita dalle impostazioni *Width* e *Height*, che rimane la risoluzione logica usata negli script e nelle proprietà.

#### Samples
Il numero di campioni da usare per l'antialiasing tramite supercampionamento. Imposta il parametro della finestra `GLFW_FSAA_SAMPLES`. Un valore di `0` indica che l'antialiasing è disattivato.

#### Fullscreen
Seleziona questa opzione per avviare l'applicazione a schermo intero. Se non è selezionata, l'applicazione viene eseguita in una finestra.

#### Update Frequency
La frequenza dei frame desiderata, espressa in hertz. Imposta 0 per una frequenza variabile. Un valore maggiore di 0 produce una frequenza fissa, limitata durante l'esecuzione alla frequenza effettiva dei frame (quindi non puoi aggiornare il ciclo di gioco due volte nello stesso frame del motore). Usa [`sys.set_update_frequency(hz)`](https://defold.com/ref/stable/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) per modificare questo valore durante l'esecuzione. Questa impostazione funziona anche nelle build headless.

#### Swap interval
Questo valore intero controlla come l'applicazione gestisce la sincronizzazione verticale. 0 la disabilita e il valore predefinito è 1. Con un adattatore OpenGL, questo valore imposta il numero di frame per cui la finestra deve [aggiornarsi tra gli scambi dei buffer](https://www.khronos.org/opengl/wiki/Swap_Interval). Vulkan non prevede un intervallo di scambio: in questo caso il valore controlla se la sincronizzazione verticale deve essere abilitata.

#### Vsync
Impostazione per la compatibilità con le versioni precedenti. Questa impostazione è deprecata; usa **Swap Interval** per i nuovi progetti. Se è disabilitata, forza l'intervallo di scambio effettivo a `0`. Se è abilitata, **Swap Interval** determina il valore effettivo.

#### Display Profiles
Specifica il file dei profili di visualizzazione da usare; il valore predefinito è `/builtins/render/default.display_profilesc`. Per approfondire, consulta il [manuale dei layout GUI](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation
Seleziona questa opzione affinché l'applicazione passi dinamicamente dall'orientamento verticale a quello orizzontale quando ruoti il dispositivo. Attualmente l'applicazione di sviluppo non rispetta questa impostazione.

#### Display Device Info
Mostra nella console le informazioni sulla GPU all'avvio.

---

### Render

#### Clear Color Red
Il canale rosso del colore di cancellazione, usato dallo script di rendering e alla creazione della finestra.

#### Clear Color Green
Il canale verde del colore di cancellazione, usato dallo script di rendering e alla creazione della finestra.

#### Clear Color Blue
Il canale blu del colore di cancellazione, usato dallo script di rendering e alla creazione della finestra.

#### Clear Color Alpha
Il canale alfa del colore di cancellazione, usato dallo script di rendering e alla creazione della finestra.

---

### Font

#### Runtime Generation
Usa la generazione dei font a runtime.

---

### Physics

#### Max Collision Object Count
Il numero massimo di oggetti di collisione.

#### Type
Il tipo di fisica da usare, `2D` o `3D`.

#### Gravity X
La gravità del mondo lungo l'asse x, espressa in metri al secondo.

#### Gravity Y
La gravità del mondo lungo l'asse y, espressa in metri al secondo.

#### Gravity Z
La gravità del mondo lungo l'asse z, espressa in metri al secondo.

#### Debug
Seleziona questa opzione per visualizzare la fisica a scopo di debug.

#### Debug Alpha
Il valore della componente alfa per la visualizzazione della fisica, `0`--`1`.

#### World Count
Il numero massimo di mondi fisici simultanei, `4` per impostazione predefinita. Se carichi più di 4 mondi contemporaneamente tramite proxy di collezione, devi aumentare questo valore. Tieni presente che ogni mondo fisico alloca una quantità considerevole di memoria.

#### Scale
Indica al motore fisico come scalare i mondi fisici rispetto al mondo di gioco per garantire la precisione numerica, `0.01`--`1.0`. Se il valore è `0.02`, il motore fisico considera 50 unità equivalenti a 1 metro ($1 / 0.02$).

#### Allow Dynamic Transforms
Seleziona questa opzione affinché il motore fisico applichi la trasformazione di un oggetto di gioco ai componenti oggetto di collisione associati. Puoi usarla per spostare, scalare e ruotare le forme di collisione, anche quelle dinamiche.

#### Use Fixed Timestep
Seleziona questa opzione affinché il motore fisico usi aggiornamenti a intervalli fissi, indipendenti dalla frequenza dei frame. Usa questa impostazione insieme alla funzione del ciclo di vita `fixed_update(self, dt)` e all'impostazione del progetto `engine.fixed_update_frequency` per interagire con il motore fisico a intervalli regolari. Per i nuovi progetti, l'impostazione consigliata è `true`.

#### Debug Scale
La dimensione con cui disegnare gli oggetti unitari della fisica, come le terne di assi e le normali.

#### Max Collisions
Il numero di collisioni da segnalare agli script.

#### Max Contacts
Il numero di punti di contatto da segnalare agli script.

#### Contact Impulse Limit
Ignora gli impulsi di contatto con valori inferiori a questa impostazione.

#### Ray Cast Limit 2d
Il numero massimo di richieste di ray casting 2D per frame.

#### Ray Cast Limit 3d
Il numero massimo di richieste di ray casting 3D per frame.

#### Trigger Overlap Capacity
Il numero massimo di trigger fisici sovrapposti.

#### Velocity Threshold
La velocità minima che produce collisioni elastiche.

#### Max Fixed Timesteps
Il numero massimo di passi della simulazione quando si usa un passo temporale fisso (solo 3D).

---

### Graphics

#### Default Texture Min Filter
Specifica il filtro da usare per la riduzione delle texture.

#### Default Texture Mag Filter
Specifica il filtro da usare per l'ingrandimento delle texture.

#### Max Draw Calls
Il numero massimo di chiamate di rendering.

#### Max Characters:
Il numero di caratteri preallocati nel buffer di rendering del testo, cioè il numero di caratteri visualizzabili in ogni frame.

#### Max Font Batches
Il numero massimo di batch di testo visualizzabili in ogni frame.

#### Max Debug Vertices
Il numero massimo di vertici di debug. Vengono usati, tra le altre cose, per il rendering delle forme fisiche.

#### Texture Profiles
Il file dei profili delle texture da usare per questo progetto; il valore predefinito è `/builtins/graphics/default.texture_profiles`.

#### Verify Graphics Calls
Verifica il valore restituito da ogni chiamata grafica e segnala eventuali errori nel log.

#### OpenGL Version Hint
L'indicazione della versione del contesto OpenGL. Se selezioni una versione specifica, viene usata come versione minima richiesta (non si applica a OpenGL ES).

#### OpenGL Core Profile Hint
Imposta l'indicazione del profilo OpenGL 'core' alla creazione del contesto. Il profilo core rimuove tutte le funzionalità deprecate di OpenGL, come il rendering in modalità immediata. Non si applica a OpenGL ES.

#### Vulkan Version Major
`graphics.vulkan_version_major` indica la versione principale richiesta per il contesto/API Vulkan. Si applica solo quando è selezionato il backend grafico Vulkan. Il valore predefinito è `1`.

#### Vulkan Version Minor
`graphics.vulkan_version_minor` indica la versione secondaria richiesta per il contesto/API Vulkan. Si applica solo quando è selezionato il backend grafico Vulkan. Il valore predefinito è `0`.

---

### Shader

#### Exclude GLES 2.0
Non compilare gli shader per i dispositivi che usano OpenGLES 2.0 / WebGL 1.0.

#### GLSL ES Default Precision Float
`shader.glsl_es_default_precision_float` imposta il qualificatore di precisione globale predefinito per i valori a virgola mobile negli shader GLSL ES ottenuti tramite compilazione incrociata. I valori validi sono `mediump` e `highp`; il valore predefinito è `mediump`.

#### GLSL ES Default Precision Int
`shader.glsl_es_default_precision_int` imposta il qualificatore di precisione globale predefinito per i valori interi negli shader GLSL ES ottenuti tramite compilazione incrociata. I valori validi sono `mediump` e `highp`; il valore predefinito è `highp`.

---

### Input

#### Repeat Delay
I secondi di attesa prima che un input mantenuto premuto inizi a ripetersi.

#### Repeat Interval
I secondi di attesa tra le ripetizioni di un input mantenuto premuto.

#### Gamepads
Riferimento al file di configurazione dei gamepad, che associa i segnali dei gamepad al sistema operativo; il valore predefinito è `/builtins/input/default.gamepads`.

#### Game Binding
Riferimento al file di configurazione degli input, che associa gli input hardware alle azioni; il valore predefinito è `/input/game.input_binding`.

#### Use Accelerometer
Seleziona questa opzione affinché il motore riceva gli eventi di input dell'accelerometro a ogni frame. Disabilitare l'input dell'accelerometro può migliorare le prestazioni.

---

### Resource

#### Http Cache
Se selezionata, abilita una cache HTTP per caricare più velocemente le risorse dalla rete nel motore in esecuzione sul dispositivo.

#### Uri
La posizione dei dati della build del progetto, in formato URI.

#### Max Resources
Il numero massimo di risorse caricabili contemporaneamente.

---

### Network

#### Http Timeout
Il timeout HTTP in secondi. Imposta `0` per disabilitare il timeout.

#### Http Thread Count
Il numero di thread di lavoro per il servizio HTTP.

#### Http Cache Enabled
Seleziona questa opzione per abilitare la cache HTTP per le richieste di rete (tramite `http.request()`. La cache HTTP memorizza la risposta associata a una richiesta e la riutilizza per le richieste successive. La cache HTTP supporta le intestazioni di risposta HTTP `ETag` e `Cache-Control: max-age`.

#### SSL Certificates
Il file contenente i certificati radice SSL da usare per verificare la catena dei certificati durante gli handshake SSL.

---

### Collection

#### Max Instances
Il numero massimo di istanze di oggetti di gioco in una collezione, `1024` per impostazione predefinita. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Max Input Stack Entries
Il numero massimo di oggetti di gioco nello stack di input.

---

### Sound

#### Gain
Il guadagno globale (volume), `0`--`1`.

#### Use Linear Gain
Se abilitata, il guadagno è lineare. Se disabilitata, usa una curva esponenziale.

#### Max Sound Data
Il numero massimo di risorse audio, cioè il numero di file audio distinti durante l'esecuzione.

#### Max Sound Buffers
(Attualmente non usata) Il numero massimo di buffer audio simultanei.

#### Max Sound Sources
(Attualmente non usata) Il numero massimo di suoni riprodotti contemporaneamente.

#### Max Sound Instances
Il numero massimo di istanze sonore simultanee, cioè dei suoni effettivamente riprodotti contemporaneamente.

#### Max Component Count
Il numero massimo di componenti audio per collezione.

#### Sample Frame Count
Il numero di campioni usati per ogni aggiornamento audio. 0 indica una scelta automatica (1024 per 48 kHz, 768 per 44.1 kHz).

#### Use Thread
Se selezionata, il sistema audio usa i thread per riprodurre i suoni e ridurre il rischio di interruzioni quando il thread principale è sottoposto a un carico elevato.

#### Stream Enabled
Se selezionata, il sistema audio usa lo streaming per caricare i file sorgenti.

#### Stream Cache Size
La dimensione massima della cache dei blocchi audio, contenente _tutti_ i blocchi. Il valore predefinito è `2097152` byte.
Questo numero dovrebbe essere maggiore del prodotto tra il numero di file audio caricati e la dimensione dei blocchi dello streaming.
Altrimenti, rischi che i nuovi blocchi vengano rimossi dalla cache a ogni frame.

#### Stream Chunk Size
La dimensione in byte di ogni blocco trasmesso in streaming.

#### Stream Preload Size
Determina la dimensione in byte del blocco iniziale per i file audio letti dall'archivio.

---

### Sprite

#### Max Count
Il numero massimo di sprite per collezione. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Subpixels
Seleziona questa opzione per consentire agli sprite di apparire non allineati ai pixel.

---

### Tilemap

#### Max Count
Il numero massimo di mappe di tile per collezione. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Max Tile Count
Il numero massimo di tile visibili contemporaneamente per collezione.

---

### Spine

#### Max Count
Il numero massimo di componenti modello Spine. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

---

### Mesh

#### Max Count
Il numero massimo di componenti mesh per collezione. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

---

### Model

#### Max Count
Il numero massimo di componenti modello per collezione. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Split Meshes
Suddivide le mesh con più di 65536 vertici in nuove mesh.

#### Max Bone Matrix Texture Width
La larghezza massima della texture delle matrici delle ossa. Viene usata solo la dimensione necessaria per le animazioni, arrotondata per eccesso alla potenza di due più vicina.

#### Max Bone Matrix Texture Height
L'altezza massima della texture delle matrici delle ossa. Viene usata solo la dimensione necessaria per le animazioni, arrotondata per eccesso alla potenza di due più vicina.

---

### GUI

#### Max Count
Il numero massimo di componenti GUI. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Max Particle Count
Il numero massimo di particelle simultanee nella GUI.

#### Max Animation Count
Il numero massimo di animazioni attive nella GUI.

---

### Label

#### Max Count
Il numero massimo di etichette. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Subpixels
Seleziona questa opzione per consentire alle etichette di apparire non allineate ai pixel.

---

### Particle FX

#### Max Count
Il numero massimo di emettitori simultanei. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

#### Max Particle Count
Il numero massimo di particelle simultanee.

---

### Box2D

#### Velocity Iterations
Il numero di iterazioni sulla velocità per il risolutore fisico Box2D 2.2.

#### Position Iterations
Il numero di iterazioni sulla posizione per il risolutore fisico Box2D 2.2.

#### Sub Step Count
Il numero di sottopassi per il risolutore fisico Box2D 3.x.

---

### Collection proxy

#### Max Count
Il numero massimo di proxy di collezione. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count
Il numero massimo di factory di collezioni. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

---

### Factory

#### Max Count
Il numero massimo di factory di oggetti di gioco. [(Consulta le informazioni sull'ottimizzazione del numero massimo di componenti)](#component-max-count-optimizations).

---

### iOS

#### App Icon 57x57--180x180
Il file immagine (.png) da usare come icona dell'applicazione alle dimensioni di larghezza e altezza indicate, `W` &times; `H`.

#### Launch Screen
Il file storyboard (.storyboard). Per sapere come crearne uno, consulta il [manuale iOS](/manuals/ios/#creating-a-storyboard).

#### Icons Asset
Il file degli asset delle icone (.car) contenente le icone dell'applicazione.

#### Prerendered Icons
(iOS 6 e versioni precedenti) Seleziona questa opzione se le icone sono prerenderizzate. Se non è selezionata, alle icone viene aggiunto automaticamente un riflesso lucido.

#### Bundle Identifier
L'identificatore del bundle permette a iOS di riconoscere gli aggiornamenti dell'applicazione. L'ID del bundle deve essere registrato presso Apple e deve essere univoco per la tua applicazione. Non puoi usare lo stesso identificatore per applicazioni iOS e macOS. Deve essere composto da due o più segmenti separati da un punto. Ogni segmento deve iniziare con una lettera e contenere solo caratteri alfanumerici, trattini bassi o trattini (-) (consulta [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Bundle Name
Il nome breve del bundle (15 caratteri) (consulta [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version
La versione del bundle, espressa come numero o nel formato x.y.z. (consulta [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Info.plist
Se specificato, usa questo file *`Info.plist`* al posto del manifest di base iOS integrato durante la creazione del bundle dell'applicazione. Il manifest integrato contiene le voci della rete locale e di Bonjour necessarie al rilevamento delle destinazioni da parte dell'editor nelle build diverse da quelle di release. Se fornisci un manifest personalizzato e hai bisogno del rilevamento delle destinazioni, della profilazione, dell'hot reload o dello streaming dei log su un dispositivo, conserva queste voci come descritto nel [manuale iOS](/manuals/ios/#creating-an-ios-application-bundle).

#### Privacy Manifest
L'Apple Privacy Manifest dell'applicazione. Il valore predefinito del campo è `/builtins/manifests/ios/PrivacyInfo.xcprivacy`.

#### Custom Entitlements
Se specificato, le autorizzazioni del profilo di provisioning fornito (`.entitlements`, `.xcent`, `.plist`) vengono unite a quelle del profilo di provisioning fornito durante la creazione del bundle dell'applicazione.

#### Default Language
La lingua usata se l'applicazione non include la lingua preferita dall'utente nell'elenco `Localizations` (consulta [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Usa il codice a due lettere dello standard ISO 639-1 se la lingua preferita vi è presente, altrimenti quello a tre lettere dello standard ISO 639-2.

#### Localizations
Questo campo contiene stringhe separate da virgole che identificano il nome della lingua o il codice ISO delle localizzazioni supportate (consulta [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
Il file immagine (.png) da usare come icona dell'applicazione alle dimensioni di larghezza e altezza indicate, `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi
I file immagine (.png) da usare come icona personalizzata delle notifiche push su Android. Le icone vengono usate automaticamente sia per le notifiche push locali sia per quelle remote. Se non sono impostate, viene usata l'icona dell'applicazione.

#### Push Field Title
Specifica il campo JSON del payload da usare come titolo della notifica. Se lasci vuota questa impostazione, le notifiche push usano il nome dell'applicazione come titolo.

#### Push Field Text
Specifica il campo JSON del payload da usare come testo della notifica. Se lasci vuota questa impostazione, viene usato il testo del campo `alert`, come su iOS.

#### Version Code
Un valore intero che indica la versione dell'applicazione. Aumenta il valore a ogni aggiornamento successivo.

#### Minimum SDK Version
Il livello API minimo richiesto per eseguire l'applicazione (`android:minSdkVersion`).

#### Target SDK Version
Il livello API a cui è destinata l'applicazione (`android:targetSdkVersion`).

#### Package
L'identificatore del pacchetto. Deve essere composto da due o più segmenti separati da un punto. Ogni segmento deve iniziare con una lettera e contenere solo caratteri alfanumerici o trattini bassi.

#### GCM Sender Id
L'ID mittente di Google Cloud Messaging. Impostalo alla stringa assegnata da Google per abilitare le notifiche push.

#### FCM Application Id
L'ID applicazione di Firebase Cloud Messaging.

#### Manifest
Se impostato, usa il file XML del manifest Android specificato durante la creazione del bundle. Un manifest personalizzato sostituisce il manifest di base integrato di Defold. I frammenti di manifest delle estensioni native vengono comunque uniti al manifest personalizzato, ma le successive modifiche al manifest di base integrato non vengono ereditate automaticamente; quando aggiorni Defold, confronta quindi i manifest personalizzati con il manifest integrato corrente. Per i giochi, imposta `android:appCategory="game"` sull'elemento `<application>`. Per le applicazioni che non sono giochi, imposta `android:appCategory` solo se una delle [categorie di applicazioni](https://developer.android.com/guide/topics/manifest/application-element#appCategory) definite da Android descrive accuratamente l'applicazione.

#### Iap Provider
Specifica lo store da usare. Le opzioni valide sono `Amazon` e `GooglePlay`. Per ulteriori informazioni, consulta [extension-iap](/extension-iap/).

#### Input Method
Specifica il metodo da usare per ricevere l'input da tastiera sui dispositivi Android. Le opzioni valide sono `KeyEvent` (metodo precedente) e `HiddenInputField` (nuovo metodo).

#### Immersive Mode
Se impostata, nasconde le barre di navigazione e di stato e consente all'applicazione di acquisire tutti gli eventi di tocco sullo schermo.

#### Display Cutout
Estende la visualizzazione all'area del ritaglio dello schermo.

#### Debuggable
Indica se è possibile eseguire il debug dell'applicazione con strumenti come [GAPID](https://github.com/google/gapid) o [Android Studio](https://developer.android.com/studio/profile/android-profiler). Imposta il flag `android:debuggable` nel manifest Android ([documentazione ufficiale](https://developer.android.com/guide/topics/manifest/application-element#debug)).

#### ProGuard config
Un file ProGuard personalizzato che aiuta a rimuovere le classi Java ridondanti dall'APK finale.

#### Extract Native Libraries
Specifica se il programma di installazione dei pacchetti estrae le librerie native dall'APK al file system. Se impostata a `false`, le librerie native vengono memorizzate senza compressione nell'APK. Anche se l'APK può risultare più grande, l'applicazione si carica più velocemente perché le librerie vengono caricate direttamente dall'APK durante l'esecuzione. Imposta il flag `android:extractNativeLibs` nel manifest Android ([documentazione ufficiale](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
Il file dell'icona del bundle (.icns) da usare come icona dell'applicazione su macOS.

#### Info.plist
Se impostato, usa il file info.plist specificato durante la creazione del bundle.

#### Privacy Manifest
L'Apple Privacy Manifest dell'applicazione. Il valore predefinito del campo è `/builtins/manifests/osx/PrivacyInfo.xcprivacy`.

#### Bundle Identifier
L'identificatore del bundle permette a macOS di riconoscere gli aggiornamenti dell'applicazione. L'ID del bundle deve essere registrato presso Apple e deve essere univoco per la tua applicazione. Non puoi usare lo stesso identificatore per applicazioni iOS e macOS. Deve essere composto da due o più segmenti separati da un punto. Ogni segmento deve iniziare con una lettera e contenere solo caratteri alfanumerici, trattini bassi o trattini (-).

#### Default Language
La lingua usata se l'applicazione non include la lingua preferita dall'utente nell'elenco `Localizations` (consulta [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Usa il codice a due lettere dello standard ISO 639-1 se la lingua preferita vi è presente, altrimenti quello a tre lettere dello standard ISO 639-2.

#### Localizations
Questo campo contiene stringhe separate da virgole che identificano il nome della lingua o il codice ISO delle localizzazioni supportate (consulta [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows

#### App Icon
Il file immagine (.ico) da usare come icona dell'applicazione su Windows. Per sapere come creare un file .ico, consulta il [manuale Windows](/manuals/windows).

---

### HTML5

Consulta il [manuale della piattaforma HTML5](/manuals/html5/) per ulteriori informazioni su molte di queste opzioni.

#### Heap Size
La dimensione dell'heap in megabyte da usare per Emscripten.

#### .html Shell
Usa il file del modello HTML specificato durante la creazione del bundle. Il valore predefinito è `/builtins/manifests/web/engine_template.html`.

#### Custom .css
Usa il file CSS del tema specificato durante la creazione del bundle. Il valore predefinito è `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Se impostata, durante la creazione del bundle usa l'immagine di avvio specificata al posto del logo Defold.

#### Archive Location Prefix
Durante la creazione di un bundle HTML5, i dati del gioco vengono suddivisi in uno o più file di archivio. Quando il motore avvia il gioco, questi file di archivio vengono letti in memoria. Usa questa impostazione per specificare la posizione dei dati.

#### Archive Location Suffix
Il suffisso da aggiungere ai file di archivio. È utile, ad esempio, per forzare il caricamento di contenuti non presenti nella cache da una CDN (per esempio con `?version2`).

#### Engine Arguments
L'elenco degli argomenti da passare al motore.

#### Wasm Streaming
Abilita lo streaming del file wasm (più veloce e con un minore utilizzo di memoria, ma richiede il tipo MIME `application/wasm`).

#### Show Fullscreen Button
Abilita il pulsante Fullscreen nel file `index.html`.

#### Show Made With Defold
Abilita il link Made With Defold nel file `index.html`.

#### Show Console Banner
Se abilitata, questa opzione mostra informazioni sul motore e sulla sua versione nella console del browser (tramite `console.log()`) all'avvio del motore.

#### Scale Mode
Specifica il metodo da usare per scalare il canvas del gioco.

#### Retry Count
Il numero di tentativi di download di un file all'avvio del motore (consulta `Retry Time`).

#### Retry Time
Il numero di secondi di attesa tra i tentativi di download di un file quando il download fallisce (consulta `Retry Count`).

#### Transparent Graphics Context
Seleziona questa opzione se vuoi che il contesto grafico abbia uno sfondo trasparente.

---

### IAP

#### Auto Finish Transactions
Seleziona questa opzione per completare automaticamente le transazioni IAP. Se non è selezionata, devi chiamare esplicitamente `iap.finish()` dopo una transazione riuscita.

---

### Live update

#### Settings
Il file di risorsa delle impostazioni Liveupdate da usare durante la creazione del bundle.

---

### Native extension

#### _App Manifest_
Se impostato, usa il manifest dell'applicazione per personalizzare la build del motore. Puoi così rimuovere le parti inutilizzate del motore e ridurre le dimensioni del file binario finale. Scopri come escludere le funzionalità inutilizzate [nel manuale del manifest dell'applicazione](/manuals/app-manifest).

---

### Profiler

L'impostazione **Profiler** di App Manifest controlla se il codice del profilatore viene collegato nelle build di debug e di release. Le impostazioni seguenti controllano il comportamento a runtime del codice del profilatore presente nella build selezionata. Per i dettagli, consulta il [manuale della profilazione](/manuals/profiling/).

#### Enabled
Abilita il profilatore nel gioco.

#### Track Cpu
Il campionamento dell'utilizzo della CPU è abilitato per impostazione predefinita nelle build di debug. Abilita questa impostazione quando il campionamento della CPU serve anche in una build di release che include il supporto al profilatore tramite App Manifest.

#### Sleep Between Server Updates
Il numero di millisecondi di pausa tra gli aggiornamenti del server.

#### Performance Timeline Enabled
Abilita la sequenza temporale delle prestazioni nel browser (solo HTML5).

#### Max Sample Count
`profiler.max_sample_count` è il numero massimo di campioni del profilatore registrati per thread in ogni frame. Il valore predefinito è `4096` e il minimo è `128`. Aumentalo solo quando un profilo valido supera il limite; prima verifica che nel codice di profilazione delle estensioni native le chiamate di inizio e fine degli ambiti siano correttamente abbinate.

---

## Impostare i valori di configurazione all'avvio del motore {#setting-config-values-on-engine-startup}

All'avvio del motore puoi fornire dalla riga di comando valori di configurazione che sovrascrivono le impostazioni di *game.project*:

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

I valori personalizzati possono---come qualsiasi altro valore di configurazione---essere letti con la funzione corrispondente descritta in [Accesso a runtime](#runtime-access):

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Impostazioni personalizzate del progetto {#custom-project-settings}

Puoi definire impostazioni personalizzate per il progetto principale o per un'[estensione nativa](/manuals/extensions/). Le impostazioni personalizzate del progetto principale devono essere definite in un file `game.properties` nella radice del progetto. I file chiamati `ext.properties` vengono individuati in qualsiasi posizione del progetto e delle dipendenze di libreria recuperate; non richiedono un file `ext.manifest` adiacente. Tutti i metadati delle estensioni individuati vengono uniti, dopodiché viene applicato il file `game.properties` nella radice, che può sovrascriverli.

Il file delle impostazioni usa lo stesso formato INI di *game.project* e gli attributi delle proprietà vengono definiti con una notazione puntata e un suffisso:

```
[my_category]
my_property.private = 1
...
```

Il file dei metadati predefinito, che viene sempre applicato, è disponibile [qui](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)

Sono attualmente disponibili i seguenti attributi:

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
Puoi inoltre impostare i seguenti attributi per una categoria di impostazioni:
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Sia Bob sia l'editor analizzano questi file di metadati. L'editor li usa per creare i campi, le opzioni, i controlli di validazione e i suggerimenti corrispondenti nella vista di *game.project*.
