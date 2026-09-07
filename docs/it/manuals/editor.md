---
title: Panoramica dell'editor
brief: Questo manuale presenta l'aspetto e il funzionamento dell'editor Defold e spiega come orientarsi al suo interno.
---

# Panoramica dell'editor {#editor-overview}

L'editor consente di esplorare e gestire in modo efficiente tutti i file e le cartelle del progetto di gioco. Quando apri un file per modificarlo, viene mostrato l'editor adatto al suo tipo, con tutte le informazioni pertinenti suddivise in viste separate.

## Avvio dell'editor {#starting-the-editor}

Quando avvii l'editor Defold, viene mostrata una schermata per selezionare e creare progetti. Fai clic per scegliere che cosa vuoi fare:

MY PROJECTS
: Qui trovi i progetti aperti di recente, per potervi accedere rapidamente. È la vista predefinita della schermata iniziale.

  Se non hai ancora aperto alcun progetto (o li hai rimossi tutti), vengono mostrati due pulsanti: puoi fare clic su `Open From Disk…` per cercare e aprire un progetto tramite il gestore di file del sistema, oppure sul pulsante `Create New Project` per passare alla scheda `TEMPLATES`.

  ![I miei progetti](images/editor/start_no_projects.png)


  Se hai già aperto dei progetti, viene mostrato il relativo elenco, come nell'immagine seguente:

  ![I miei progetti](images/editor/start_my_projects.png)

TEMPLATES
: Contiene progetti di base vuoti o quasi vuoti, pensati per avviare rapidamente un nuovo progetto Defold per determinate piattaforme o con determinate estensioni.


TUTORIALS
: Contiene progetti con tutorial guidati da cui imparare, con cui giocare e da modificare, se preferisci seguire un tutorial.


SAMPLES
: Contiene progetti preparati per illustrare casi d'uso specifici.

  ![Nuovo progetto](images/editor/start_templates.png)

Quando crei un nuovo progetto, questo viene salvato sul disco locale e anche tutte le modifiche vengono salvate localmente.

Puoi approfondire le diverse opzioni nel [manuale sulla configurazione del progetto](https://www.defold.com/manuals/project-setup/).

## Lingua dell'editor {#editor-language}

Nell'angolo in basso a sinistra della schermata iniziale trovi un selettore della lingua: scegli tra le localizzazioni attualmente disponibili. Questa opzione è disponibile anche nell'editor in `File ▸ Preferences ▸ General ▸ Editor Language`.

![Lingue](images/editor/languages.png)

## I pannelli dell'editor {#the-editor-views}

L'editor Defold è suddiviso in una serie di pannelli, o viste, che mostrano informazioni specifiche.

![Editor 2](images/editor/editor_overview.png)

### 1. Pannello Assets {#1-assets-pane}
Elenca tutti i file e le cartelle che fanno parte del progetto in una struttura ad albero, corrispondente a quella presente sul disco. Fai clic e scorri per esplorare l'elenco. In questa vista puoi eseguire tutte le operazioni sui file:

   - <kbd>Fai clic con il pulsante sinistro del mouse</kbd> per selezionare un file o una cartella; tenendo premuto <kbd>⇧ Shift</kbd> puoi estendere la selezione, mentre tenendo premuto <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puoi selezionare o deselezionare l'elemento su cui fai clic.
   - <kbd>Fai doppio clic</kbd> su un file per aprirlo nell'editor specifico per quel tipo di file.
   - <kbd>Trascina e rilascia</kbd> per aggiungere al progetto file da altre posizioni sul disco oppure per spostare file e cartelle in nuove posizioni all'interno del progetto.
   - <kbd>Fai clic con il pulsante destro del mouse</kbd> per aprire un _menu contestuale_ da cui puoi creare nuovi file o cartelle, rinominarli, eliminarli, esaminare le dipendenze dei file e altro ancora.

I file e le cartelle eliminati tramite il pannello *Assets* vengono spostati nel cestino del sistema, se la piattaforma lo supporta. Se lo spostamento nel cestino non è supportato o non riesce, l'editor li elimina definitivamente.

### 2. Pannello Scene Editor {#the-scene-editor}

Facendo doppio clic su un file di collezione, oggetto di gioco o componente visivo, si apre lo *Scene Editor*, l'editor visivo per creare e modificare le scene. I file di script e le altre risorse non visive si aprono invece nei rispettivi editor dedicati.

![Editor della scena](images/editor/2d_scene.png)

Alcune delle funzionalità principali dell'editor della scena:

- [Navigazione nelle scene 2D e 3D](/manuals/scene-editing/#2d-and-3d-scene-orientation) con modalità della camera ortografica e prospettica
- [Strumenti di trasformazione](/manuals/scene-editing/#manipulating-objects) per spostare, ruotare e ridimensionare gli oggetti
- [Modalità camera libera](/manuals/scene-editing/#free-camera-mode) per la navigazione 3D in prima persona
- [Impostazioni della griglia](/manuals/scene-editing/#grid-settings) con dimensioni, piano e aspetto configurabili
- [Filtri di visibilità](/manuals/scene-editing/#visibility-filters) per mostrare o nascondere tipi di componenti e guide

Per saperne di più, consulta il [manuale dell'editor della scena](/manuals/scene-editing/).

### 3. Pannello Outline {#3-outline-pane}

Questa vista mostra il contenuto del file che stai modificando in una struttura gerarchica ad albero. La vista Outline rispecchia la vista dell'editor e consente di eseguire operazioni sugli elementi:

   - <kbd>Fai clic con il pulsante sinistro del mouse</kbd> per selezionare un elemento; tenendo premuto <kbd>⇧ Shift</kbd> puoi estendere la selezione, mentre tenendo premuto <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puoi selezionare o deselezionare l'elemento su cui fai clic.
   - <kbd>Trascina e rilascia</kbd> per spostare gli elementi. Rilascia un oggetto di gioco su un altro oggetto di gioco in una collezione per creare una relazione genitore-figlio.
   - <kbd>Fai clic con il pulsante destro del mouse</kbd> per aprire un _menu contestuale_ da cui puoi aggiungere elementi, eliminare quelli selezionati e così via.

Puoi mostrare o nascondere gli oggetti di gioco e i componenti visivi facendo clic sulla piccola icona a forma di occhio `👁` a destra di un elemento nell'elenco.

![Struttura degli elementi](images/editor/outline.png)

### 4. Pannello Properties {#4-properties-pane}

Questa vista mostra le proprietà associate all'elemento selezionato, come Id, URL, Position, Rotation, Scale e altre proprietà specifiche del componente, oltre alle proprietà personalizzate degli script.

Puoi anche <kbd>trascinare</kbd> la freccia verticale `↕` e muovere il mouse per cambiare il valore della proprietà numerica corrispondente.

![Proprietà](images/editor/properties.png)

### 5. Pannello Tools {#5-tools-pane}

Questa vista contiene diverse schede.

Scheda *Console* : mostra gli errori, gli avvisi e le informazioni emessi dal motore, oltre all'output che produci esplicitamente mentre il gioco è in esecuzione,

*Build Errors* : mostra gli errori del processo di build,

*Search Results* : mostra i risultati della ricerca (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd> + <kbd>F</kbd>) nell'intero progetto, se fai clic su `Keep Results`

*Curve Editor* : viene usato per modificare le curve nell'[editor delle particelle](/manuals/particlefx/).

Il pannello Tools viene usato anche per interagire con il debugger integrato. Per saperne di più, consulta il [manuale sul debug](/manuals/debugging/).

### 6. Pannello Changed Files {#6-changed-files-pane}

Se il progetto usa Git, questa vista elenca i file modificati, aggiunti, rinominati o eliminati localmente rispetto al commit corrente (`HEAD`). Usa un client Git esterno o la riga di comando per sincronizzarti con un repository remoto. Puoi saperne di più nel [manuale sul controllo di versione](/manuals/version-control/). In questa vista puoi eseguire alcune operazioni sui file:

   - <kbd>Fai clic con il pulsante sinistro del mouse</kbd> - per selezionare un file; tenendo premuto <kbd>⇧ Shift</kbd> puoi estendere la selezione, mentre tenendo premuto <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puoi selezionare o deselezionare l'elemento su cui fai clic. Se è selezionato un solo file modificato, puoi fare clic su `Diff` per visualizzarne le differenze. Puoi fare clic su `Revert` per annullare le modifiche in tutti i file selezionati.
   - <kbd>Fai doppio clic con il pulsante sinistro del mouse</kbd> su un file per aprirne una vista. L'editor apre il file nell'editor adatto, come nella vista Assets.
   - <kbd>Fai clic con il pulsante destro del mouse</kbd> su un file per aprire un menu da cui puoi visualizzare le differenze, annullare tutte le modifiche apportate al file, individuare il file nel file system e altro ancora.

### Barra dei menu {#menu-bar}

Nella parte superiore della vista dell'editor, oppure nella barra di sistema su Mac, trovi la barra dei menu con 6 menu: `File`, `Edit`, `View`, `Project`, `Debug`, `Help`. Le loro funzioni sono spiegate nei manuali.

### Barra di stato {#status-bar}

Nella barra inferiore dell'editor trovi una piccola area in cui viene mostrato lo stato, ad esempio:
- quando è disponibile un nuovo aggiornamento, compare il pulsante `Update Available`: consulta la sezione Aggiornamento dell'editor più avanti in questo manuale.
- durante la creazione di una build o di un bundle, viene mostrato l'avanzamento dell'operazione.

## Dimensioni e visibilità dei pannelli {#panes-size-and-visibility}

Puoi regolare le dimensioni dei pannelli nell'editor <kbd>trascinando</kbd> i bordi delle sezioni che separano i 6 pannelli descritti sopra.

Puoi mostrare o nascondere i pannelli dell'editor usando le opzioni del menu `View` o le relative scorciatoie:
- `Toggle Assets Pane` (<kbd>F6</kbd>) per mostrare o nascondere i pannelli Assets e Changed Files
- `Toggle Changed Files` per mostrare o nascondere soltanto il pannello Changed Files
- `Toggle Tools Pane` (<kbd>F7</kbd>) per mostrare o nascondere il pannello Tools
- `Toggle Properties Pane` (<kbd>F8</kbd>) per mostrare o nascondere i pannelli Outline e Properties

![Visibilità dei pannelli](images/editor/editor_panes.png)

Nel menu `View` puoi anche attivare, disattivare o modificare altre impostazioni di visualizzazione, come Grid, Guides o Camera, inquadrare la selezione (`Frame Selection` o tasto <kbd>F</kbd>) e passare dalla vista predefinita 2D a quella 3D e viceversa (`Realign Camera` o tasto <kbd>.</kbd>). Molte di queste opzioni sono accessibili anche dalla barra degli strumenti o tramite scorciatoie.

## Schede {#tabs}

Se hai più file aperti, nella parte superiore della vista dell'editor viene mostrata una scheda per ciascun file. Puoi riordinare le schede all'interno di un pannello: <kbd>trascinale e rilasciale</kbd> per scambiarne la posizione nella barra delle schede. Puoi anche:

- <kbd>Fare clic con il pulsante destro del mouse</kbd> su una scheda per aprire un _menu contestuale_,
- Fare clic su `Close` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>W</kbd>) per chiudere una singola scheda,
- Fare clic su `Close Others` per chiudere tutte le schede tranne quella selezionata,
- Fare clic su `Close All` (<kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>Shift</kbd>+<kbd>W</kbd>) per chiudere tutte le schede del pannello attivo,
- Selezionare `➝| Open As` - per usare un editor diverso da quello predefinito o lo strumento esterno associato impostato in `File ▸ Preferences ▸ Code ▸ Custom Editor`. Per saperne di più, consulta il [manuale delle preferenze](/manuals/editor-preferences).

![Schede](images/editor/tabs_custom.png)

## Modifica in viste affiancate {#side-by-side-editing}

Puoi aprire 2 viste dell'editor una accanto all'altra.

- <kbd>Fai clic con il pulsante destro del mouse</kbd> sulla scheda dell'editor che vuoi spostare e seleziona `Move to Other Tab Pane`.

![2 pannelli](images/editor/2-panes.png)

Puoi anche usare il menu della scheda e scegliere `Swap with Other Tab Pane` per spostare una scheda da un pannello all'altro, oppure `Join Tab Panes` per riunire i pannelli in uno solo.

## Creazione di nuovi file di progetto {#creating-new-project-files}

Per creare nuovi file di risorse, seleziona `File ▸ New…` e scegli il tipo di file dal menu, oppure usa il menu contestuale:

<kbd>Fai clic con il pulsante destro del mouse</kbd> sulla posizione di destinazione nella vista `Assets`, quindi seleziona `New… ▸ [file type]`:

![Creazione di un file](images/editor/create_file.png)

Digita un nome appropriato per il nuovo file in *Name* ed eventualmente cambia *Location*. Il nome completo del file, compresa l'estensione che ne indica il tipo, viene mostrato sotto *Preview* nella finestra di dialogo:

![Nome del nuovo file](images/editor/create_file_name.png)

## Modelli {#templates}

Puoi specificare modelli personalizzati per ogni progetto. Per farlo, crea una nuova cartella chiamata `templates` nella directory radice del progetto e aggiungi nuovi file chiamati `default.*` con le estensioni desiderate, ad esempio `/templates/default.gui` o `/templates/default.script`. Inoltre, se in questi file viene usato il token `{{NAME}}`, questo verrà sostituito con il nome del file specificato nella finestra di creazione del file.

Se è disponibile un modello per un determinato tipo di file, ogni nuovo file di quel tipo viene inizializzato con il contenuto del file corrispondente in `templates`.


![Modelli](images/editor/templates.png)

## Importazione di file nel progetto {#importing-files-to-your-project}

Per aggiungere file di asset (immagini, suoni, modelli e così via) al progetto, trascinali e rilasciali nella posizione corretta della vista *Assets*. Vengono create delle _copie_ dei file nella posizione selezionata all'interno della struttura dei file del progetto. Per saperne di più, consulta il [manuale sull'importazione degli asset](/manuals/importing-assets/).

![Importazione di file](images/editor/import.png)

## Aggiornamento dell'editor {#updating-the-editor}

L'editor verifica automaticamente la disponibilità di aggiornamenti quando è connesso a Internet. Quando viene rilevato un aggiornamento, viene mostrato il link blu `Update Available` nell'angolo in basso a sinistra della schermata di selezione del progetto o nell'angolo in basso a destra della finestra dell'editor.

![Aggiornamento dalla selezione del progetto](images/editor/update_start.png)
![Aggiornamento dall'editor](images/editor/update_available.png)

Fai clic sul link `Update Available` per scaricare e installare l'aggiornamento. Si apre una finestra di conferma con le informazioni: fai clic su `Download Update` per procedere.

![Finestra di aggiornamento dell'editor](images/editor/update.png)

L'avanzamento del download viene mostrato nella barra di stato inferiore:

![Avanzamento del download](images/editor/download_status.png)

Una volta scaricato l'aggiornamento, il link blu diventa `Restart to Update`. Fai clic per riavviare e aprire l'editor aggiornato.

![Riavvio per aggiornare](images/editor/restart_to_update.png)

## Preferenze {#preferences}

Puoi modificare le impostazioni dell'editor nella finestra `Preferences`. Per aprirla, fai clic su `File ▸ Preferences…` oppure usa la scorciatoia <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> + <kbd>,</kbd>

Per maggiori dettagli, consulta il [manuale delle preferenze](/manuals/editor-preferences)

![Preferenze](images/editor/preferences.png)

## Log dell'editor {#editor-logs}
Se riscontri un problema con l'editor e devi segnalarlo (`Help  ▸ Report Issue`), è utile fornire i file di log dell'editor. Per aprire la cartella dei log nel gestore di file del sistema, fai clic su `Help ▸ Show Logs`.

Per saperne di più, consulta il [manuale su come ottenere aiuto](/manuals/getting-help/#getting-help).

![Visualizzazione dei log](images/editor/show_logs.png)

I file di log dell'editor si trovano qui:

  * Windows: `C:\Users\ **Your Username** \AppData\Local\Defold`
  * macOS: `/Users/ **Your Username** /Library/Application Support/` oppure `~/Library/Application Support/Defold`
  * Linux: `$XDG_STATE_HOME/Defold` oppure `~/.local/state/Defold`

Puoi accedere ai log anche mentre l'editor è in esecuzione, se lo avvii da un terminale o dal prompt dei comandi. Per avviare l'editor, usa il comando:

```shell
# Linux:
$ ./path/to/Defold/Defold

# macOS:
$ > ./path/to/Defold.app/Contents/MacOS/Defold
```

## Server dell'editor {#editor-server}

Quando l'editor apre un progetto, avvia un server web su una porta casuale. Il server può essere usato per interagire con l'editor da altre applicazioni. La porta viene scritta nel file `.internal/editor.port`.

Il server fornisce una specifica OpenAPI all'indirizzo `http://localhost:$(cat .internal/editor.port)/openapi.json`. È un punto di partenza minimo utile per i flussi di lavoro basati su agenti.

Inoltre, l'eseguibile dell'editor dispone dell'opzione a riga di comando `--port` (o `-p`), che consente di specificare la porta all'avvio, ad esempio::
```shell
# Windows
.\path\to\Defold\Defold.exe --port 8181

# Linux:
./path/to/Defold/Defold --port 8181

# macOS:
./path/to/Defold/Defold.app/Contents/MacOS/Defold --port 8181
```

## Metadati di installazione dell'editor {#editor-installation-metadata}

All'avvio, l'editor scrive le informazioni sul programma di avvio e sui percorsi di installazione in una posizione prestabilita. Le integrazioni con IDE di terze parti e altri strumenti possono usare queste informazioni per individuare gli editor Defold installati:

| Sistema operativo | Posizione |
|---------|----------|
| macOS   | `~/Library/Application Support/Defold/installations.json` |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/Defold/installations.json` |
| Windows | `%LOCALAPPDATA%\Defold\installations.json` |

Il file contiene un array JSON con un oggetto per ogni installazione nota:

```json
[
  {
    "launcherPath": "/Applications/Defold.app/Contents/MacOS/Defold",
    "installPath": "/Applications/Defold.app",
    "lastLaunchedAt": "2026-07-06T12:34:56.789Z"
  }
]
```

## Personalizzazione dell'aspetto dell'editor {#editor-styling}

Puoi modificare l'aspetto dell'editor usando stili personalizzati. Per saperne di più, consulta il [manuale sulla personalizzazione dell'aspetto dell'editor](/manuals/editor-styling).

## FAQ
:[Editor FAQ](../shared/editor-faq.md)
