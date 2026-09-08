---
title: L'editor di scena di Defold
brief: L'editor di scena permette di modificare collezioni, oggetti di gioco, GUI, effetti particellari e altri asset visivi. Questo manuale spiega la selezione, gli strumenti e come navigare nella vista della scena in 2D e 3D, comprese la modalità telecamera libera e le impostazioni della telecamera.
---

# L'editor di scena di Defold {#the-defold-scene-editor}

L'**editor di scena (Scene Editor)** è l'editor visivo utilizzato per creare e modificare scene come collezioni, oggetti di gioco e altri asset visivi.

Per impostazione predefinita, molte scene visive si aprono con una vista **ortografica 2D**. Per lavorare in 3D puoi passare a un layout orientato al 3D, attivare un piano della griglia 3D e utilizzare una telecamera **prospettica**.

## Aprire l'editor di scena {#opening-the-scene-editor}

Apri l'editor di scena facendo doppio clic su una risorsa visiva nel pannello *Assets*, ad esempio:

- **Struttura della scena** — collezioni (`.collection`), oggetti di gioco (`.go`)
- **Asset 2D** — atlas (`.atlas`), mappe di tile (`.tilemap`), sprite (`.sprite`), sorgenti di tile (`.tilesource`)
- **Asset 3D** — modelli (`.model`, `.glb`, `.gltf`)
- **UI** — scene GUI (`.gui`)
- **Effetti** — effetti particellari (`.particlefx`)
- E altri ancora

## Navigazione nella vista della scena (controlli della telecamera) {#scene-view-navigation-camera-controls}

La telecamera dell'editor di scena può essere controllata con il mouse e la tastiera. I controlli disponibili dipendono dall'uso della navigazione standard della telecamera o della **modalità telecamera libera (Free Camera Mode)**.

### Navigazione standard (tutti gli editor visivi) {#standard-navigation-all-visual-editors}

Questi controlli sono disponibili negli editor visivi:

- **Traslazione**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Zoom**
  - <kbd>Mouse Wheel</kbd>, oppure
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Rotazione/orbita (3D) attorno alla selezione**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Puoi anche utilizzare **Frame Selection** (<kbd>F</kbd>) per inquadrare la selezione corrente con la telecamera.

## Orientamento della scena in 2D e 3D {#2d-and-3d-scene-orientation}

La vista della scena può essere utilizzata sia per lavorare in 2D sia in 3D:

- In **2D**, in genere lavori con una vista ortografica e una griglia orientata al 2D.
- In **3D**, in genere:
  - Riallinei la vista a un orientamento 3D,
  - Utilizzi una telecamera **prospettica**,
  - Scegli un piano della griglia adatto (spesso **Y** per il “terreno”).

Puoi accedere a queste funzioni tramite la barra degli strumenti e il menu **View**.

![Editor di scena in 3D](images/editor/3d_scene.png)

## Panoramica della barra degli strumenti {#toolbar-overview}

In alto a destra nella vista della scena è presente una barra con gli strumenti e le opzioni di visualizzazione più comuni (da sinistra a destra):

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) — alterna tra l'orientamento 2D e 3D (scorciatoia <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Barra degli strumenti](images/editor/toolbar.png)

## Selezionare e manipolare gli oggetti {#manipulating-objects}

### Selezionare gli oggetti {#selecting-objects}

<kbd>Fai clic con il pulsante sinistro del mouse</kbd> sugli oggetti nella finestra principale per selezionarli. Il rettangolo (o parallelepipedo) che circonda l'oggetto nella vista dell'editor viene evidenziato in ciano per indicare quale elemento è selezionato. L'oggetto selezionato viene evidenziato anche nella vista `Outline`, come nell'immagine sopra.

  Puoi selezionare gli oggetti anche nei seguenti modi:

- <kbd>Fai clic con il pulsante sinistro del mouse</kbd> e <kbd>trascina</kbd> per selezionare tutti gli oggetti all'interno dell'area di selezione.
- <kbd>Fai clic con il pulsante sinistro del mouse</kbd> sugli oggetti nella vista `Outline`: tenendo premuto <kbd>⇧ Shift</kbd> puoi estendere la selezione, mentre tenendo premuto <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> puoi selezionare o deselezionare l'oggetto su cui fai clic.

#### Strumento di spostamento {#move-tool}

![Strumento di spostamento](images/editor/icon_move.png){.left}

Per spostare gli oggetti, usa lo strumento *Move Tool*. Puoi trovarlo nella barra degli strumenti in alto a destra nell'editor di scena oppure attivarlo premendo il tasto <kbd>W</kbd>.

![Spostamento di un oggetto](images/editor/move.png){.inline}![Spostamento di un oggetto in 3D](images/editor/move_3d.png){.inline}

Il gizmo cambia e mostra una serie di manipolatori, quadrati e frecce (il manipolatore selezionato diventa arancione), che puoi <kbd>trascinare</kbd> per spostare l'oggetto:

- una maniglia quadrata centrale ciano per spostare l'oggetto solo nello spazio dello schermo,
- 3 frecce rosse, verdi e blu lungo ciascun asse per spostare l'oggetto solo lungo l'asse X, Y o Z corrispondente.
- 3 maniglie quadrate rosse, verdi e blu (con contorno e riempimento trasparente) per spostare l'oggetto solo sul piano corrispondente, ad esempio il piano X-Y (blu) e i piani X-Z (verde) e Y-Z (rosso), visibili ruotando la telecamera in 3D.

#### Strumento di rotazione {#rotate-tool}

![Strumento di rotazione](images/editor/icon_rotate.png){.left}

Per ruotare gli oggetti, usa lo strumento *Rotate Tool* selezionandolo nella barra degli strumenti oppure premendo il tasto <kbd>E</kbd>.

![Rotazione di un oggetto](images/editor/rotate.png){.inline}![Rotazione di un oggetto in 3D](images/editor/rotate_3d.png){.inline}

Questo strumento è composto da quattro manipolatori circolari (il manipolatore selezionato diventa arancione) che puoi <kbd>trascinare</kbd> per ruotare l'oggetto:

- un manipolatore ciano (il cerchio esterno, più grande) che ruota l'oggetto nello spazio dello schermo
- 3 manipolatori circolari più piccoli, rossi, verdi e blu, che consentono di ruotare separatamente attorno a ciascuno degli assi X, Y e Z. Nella vista ortografica 2D, due di essi sono perpendicolari agli assi X e Y, quindi i cerchi appaiono come due linee che attraversano l'oggetto.

#### Strumento di ridimensionamento {#scale-tool}

![Strumento di ridimensionamento](images/editor/icon_scale.png){.left}

Per ridimensionare gli oggetti, usa lo strumento *Scale Tool* selezionandolo nella barra degli strumenti oppure premendo il tasto <kbd>R</kbd>.

![Ridimensionamento di un oggetto](images/editor/scale.png){.inline}![Ridimensionamento di un oggetto in 3D](images/editor/scale_3d.png){.inline}

Questo strumento è composto da una serie di manipolatori quadrati e cubici (il manipolatore selezionato diventa arancione) che puoi <kbd>trascinare</kbd> per ridimensionare l'oggetto:

- un cubo ciano al centro ridimensiona l'oggetto uniformemente su tutti gli assi (compreso Z).
- 3 manipolatori cubici rossi, blu e verdi ridimensionano l'oggetto separatamente lungo ciascuno degli assi X, Y e Z.
- 3 manipolatori quadrati rossi, verdi e blu (con contorno e riempimento trasparente) ridimensionano l'oggetto separatamente sui piani X-Y, X-Z o Y-Z.

### Filtri di visibilità {#visibility-filters}

Fai clic sull'**icona a forma di occhio della visibilità** (`👁`) nella barra degli strumenti per attivare o disattivare la visualizzazione dei vari tipi di componenti, dei riquadri di delimitazione e delle linee guida (`Component Guides` oppure la scorciatoia <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) o <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac)).

![Filtri di visibilità](images/editor/visibilityfilters.png)

## Impostazioni della griglia {#grid-settings}

Puoi personalizzare la griglia in base al tuo flusso di lavoro (particolarmente utile in 3D). Fai clic sul pulsante **Grid Settings** (`▦`) per aprire il popup delle impostazioni della griglia.

![Impostazioni della griglia](images/editor/grid_popup.png)

Le impostazioni comprendono:

- **Grid size (X/Y/Z)**
  Imposta la distanza tra le linee della griglia lungo ciascun asse. Utilizza valori più piccoli per posizionare con precisione gli oggetti piccoli, oppure valori più grandi per una visione d'insieme più ampia.
- **Active plane (X/Y/Z)**
  Seleziona il piano su cui viene disegnata la griglia. Quando lavori in 2D, in genere è **Z** (il piano X-Y predefinito). In 3D, si usa spesso **Y** per rappresentare un terreno o un pavimento.
- **Grid color**
  Imposta il colore delle linee della griglia. Utile per ottenere contrasto con i diversi sfondi della scena.
- **Grid opacity**
  Controlla la trasparenza delle linee della griglia. Valori più bassi rendono la griglia meno invadente, mantenendola comunque come riferimento.
- Un pulsante **Reset to Defaults**
  Ripristina tutte le impostazioni della griglia ai valori originali.

## Tipo di telecamera: prospettica e ortografica {#camera-type-perspective-vs-orthographic}

L'editor di scena supporta entrambi i tipi:

- Telecamera **ortografica** (comune quando si lavora in 2D)
- Telecamera **prospettica** (comune quando si lavora in 3D)

Utilizza il pulsante della telecamera nella barra degli strumenti per passare da un tipo all'altro. Nelle scene 3D, la navigazione prospettica risulta in genere più naturale.

## Modalità telecamera libera {#free-camera-mode}

Per navigare rapidamente in 3D, l'editor di scena offre la **modalità telecamera libera**, una telecamera in prima persona, in “stile FPS”.

### Attivare la modalità telecamera libera {#activating-free-camera-mode}

- Tieni premuto <kbd>Right Mouse Button</kbd> — la modalità telecamera libera rimane attiva finché tieni premuto il pulsante
- <kbd>Shift</kbd> + <kbd>`</kbd> (accento grave) — attiva la modalità telecamera libera, mantenendola attiva anche dopo il rilascio

::: sidenote
In alcuni layout di tastiera (ad esempio quello svedese), il tasto dell'accento grave è un tasto morto e potrebbe non attivare la scorciatoia come previsto. Puoi
riassegnare questa scorciatoia in `File ▸ Preferences ▸ Keys` e inserire una combinazione per `Scene -> Free Camera -> Activate`
:::

Quando la modalità telecamera libera è attiva, la vista della scena viene evidenziata da una linea lungo i bordi.

### Uscire dalla modalità telecamera libera {#exiting-free-camera-mode}

- Rilascia <kbd>Right Mouse Button</kbd> (se l'hai attivata tenendolo premuto), oppure
- Premi <kbd>Left Mouse Button</kbd>, <kbd>Right Mouse Button</kbd> (premi e rilascia) oppure <kbd>Esc</kbd> se la modalità telecamera libera è stata attivata in modo persistente.

### Guardarsi intorno (visuale con il mouse) {#looking-around-mouse-look}

Quando la modalità telecamera libera è attiva, questi controlli gestiscono il movimento della telecamera (anziché gli strumenti dell'editor):

- Muovi il mouse per controllare l'**imbardata** (sinistra/destra) e il **beccheggio** (alto/basso)
- Il beccheggio è limitato per evitare che la telecamera si capovolga

Puoi anche invertire l'asse Y (vedi **Impostazioni della telecamera libera** di seguito).

### Spostarsi {#moving}

Quando la modalità telecamera libera è attiva:

- <kbd>W</kbd> — avanti
- <kbd>S</kbd> — indietro
- <kbd>A</kbd> — a sinistra
- <kbd>D</kbd> — a destra
- <kbd>E</kbd> — in alto
- <kbd>Q</kbd> — in basso

::: sidenote
Tutti i tasti di movimento possono essere riassegnati in `File ▸ Preferences ▸ Keys`. Cerca poi `Scene -> Free Camera`
:::

Modificatori di velocità:

- Tieni premuto <kbd>Shift</kbd> — muoviti più velocemente
- Tieni premuto <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> — muoviti più lentamente e con maggiore precisione

### Modalità camminata (facoltativa) {#walking-mode-optional}

La modalità telecamera libera supporta la **modalità camminata (Walking Mode)**.

Quando è attiva:
- Il movimento verso l'alto e il basso è vincolato per riprodurre meglio una camminata in prima persona su un piano del terreno.
- È utile quando esplori un livello e vuoi mantenere un movimento coerente “a terra”.

## Popup delle impostazioni della telecamera {#camera-settings-popup}

Il pulsante della telecamera prospettica nella barra degli strumenti dispone di un popup con le preferenze relative alla telecamera.

![Impostazioni della telecamera prospettica](images/editor/camera_popup.png)

Il popup contiene:

- **Move Speed**
  Regola la velocità di movimento della telecamera libera.

- **Look Sensitivity**
  Regola la velocità con cui la telecamera ruota in risposta al movimento del mouse.

- **Invert Y**
  Inverte il movimento verticale della visuale con il mouse.

- **Walking Mode**
  Vincola il movimento per una navigazione simile a una camminata sul terreno.

- **Reset to Defaults**
  Ripristina le impostazioni predefinite della telecamera.
