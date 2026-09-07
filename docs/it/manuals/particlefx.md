---
title: Effetti particellari in Defold
brief: Questo manuale spiega come funziona il componente Particle FX e come modificarlo per creare effetti particellari visivi.
---

# Effetti particellari {#particle-fx}

Gli effetti particellari vengono usati per arricchire l'aspetto visivo dei giochi. Puoi usarli per creare esplosioni, schizzi di sangue, scie, fenomeni atmosferici o qualsiasi altro effetto.

![Editor degli effetti particellari](images/particlefx/editor.png)

Gli effetti particellari sono costituiti da una serie di emettitori e da modificatori facoltativi:

Emettitore
: Un emettitore è una forma posizionata nello spazio che emette particelle distribuite uniformemente al suo interno. L'emettitore contiene proprietà che controllano la generazione delle particelle, oltre all'immagine o all'animazione, alla durata di vita, al colore, alla forma e alla velocità delle singole particelle.

Modificatore
: Un modificatore agisce sulla velocità delle particelle generate per farle accelerare o rallentare in una determinata direzione, muoversi radialmente o ruotare attorno a un punto. I modificatori possono agire sulle particelle di un singolo emettitore o su un emettitore specifico.

## Creare un effetto {#creating-an-effect}

Seleziona <kbd>New... ▸ Particle FX</kbd> dal menu contestuale nel pannello *Assets*. Assegna un nome al nuovo file dell'effetto particellare. L'editor aprirà il file nell'[editor di scena](/manuals/editor/#the-scene-editor).

Il pannello *Outline* mostra l'emettitore predefinito. Seleziona l'emettitore per visualizzarne le proprietà nel pannello *Properties* sottostante.

![Particelle predefinite](images/particlefx/default.png)

Per aggiungere un nuovo emettitore all'effetto, <kbd>fai clic con il pulsante destro</kbd> sulla radice in *Outline* e seleziona <kbd>Add Emitter ▸ [type]</kbd> dal menu contestuale. Puoi cambiare il tipo di emettitore nelle sue proprietà.

Per aggiungere un nuovo modificatore, <kbd>fai clic con il pulsante destro</kbd> sulla posizione in cui inserirlo in *Outline* (la radice dell'effetto o un emettitore specifico) e seleziona <kbd>Add Modifier</kbd>, quindi seleziona il tipo di modificatore.

![Aggiungere un modificatore](images/particlefx/add_modifier.png)

![Selezionare il modificatore da aggiungere](images/particlefx/add_modifier_select.png)

Un modificatore collocato nella radice dell'effetto (che non sia figlio di un emettitore) agisce su tutte le particelle dell'effetto.

Un modificatore aggiunto come figlio di un emettitore agisce solo su quell'emettitore.

## Visualizzare l'anteprima di un effetto {#previewing-an-effect}

* Seleziona <kbd>View ▸ Play</kbd> dal menu per visualizzare l'anteprima dell'effetto. Potresti dover ridurre lo zoom della camera per vedere correttamente l'effetto.
* Seleziona di nuovo <kbd>View ▸ Play</kbd> per mettere in pausa l'effetto.
* Seleziona <kbd>View ▸ Stop</kbd> per arrestare l'effetto. Avviandolo di nuovo, ripartirà dal suo stato iniziale.

Quando modifichi un emettitore o un modificatore, il risultato è immediatamente visibile nell'editor, anche con l'effetto in pausa:

![Modificare le particelle](images/particlefx/rotate.gif)

## Proprietà dell'emettitore {#emitter-properties}

Id
: Identificatore dell'emettitore (usato per impostare le costanti di rendering di emettitori specifici).

Position/Rotation
: Trasformazione dell'emettitore rispetto al componente ParticleFX.

Play Mode
: Controlla la riproduzione dell'emettitore:
  - `Once` arresta l'emettitore al termine della sua durata.
  - `Loop` riavvia l'emettitore al termine della sua durata.

Size Mode
: Controlla le dimensioni delle animazioni flipbook:
  - `Auto` mantiene per ciascun fotogramma dell'animazione flipbook le dimensioni dell'immagine sorgente.
  - `Manual` imposta le dimensioni delle particelle in base alla proprietà delle dimensioni.

Emission Space
: Lo spazio geometrico in cui si troveranno le particelle generate:
  - `World` muove le particelle indipendentemente dall'emettitore.
  - `Emitter` muove le particelle rispetto all'emettitore.

Duration
: Il numero di secondi durante i quali l'emettitore deve emettere particelle.

Start Delay
: Il numero di secondi che l'emettitore deve attendere prima di emettere particelle.

Start Offset
: Il numero di secondi dall'inizio della simulazione delle particelle da cui deve partire l'emettitore; in altre parole, la durata della simulazione preliminare dell'effetto.

Image
: Il file immagine (sorgente di tile o atlas) da usare per applicare le texture alle particelle e animarle.

Animation
: L'animazione del file *Image* da usare per le particelle.

Material
: Il materiale da usare per l'ombreggiatura delle particelle.

Blend Mode
: Le modalità di fusione disponibili sono `Alpha`, `Add` e `Multiply`.

Max Particle Count
: Il numero di particelle provenienti da questo emettitore che possono esistere contemporaneamente.

Emitter Type
: La forma dell'emettitore
  - `Circle` emette particelle da una posizione casuale all'interno di un cerchio. Le particelle sono dirette dal centro verso l'esterno. Il diametro del cerchio è definito da *Emitter Size X*.

  - `2D Cone` emette particelle da una posizione casuale all'interno di un cono piatto (un triangolo). Le particelle sono dirette verso l'esterno attraverso la parte superiore del cono. *Emitter Size X* definisce la larghezza della parte superiore e *Y* definisce l'altezza.

  - `Box` emette particelle da una posizione casuale all'interno di un parallelepipedo. Le particelle sono dirette verso l'alto lungo l'asse Y locale del parallelepipedo. *Emitter Size X*, *Y* e *Z* definiscono rispettivamente larghezza, altezza e profondità. Per un rettangolo 2D, mantieni a zero la dimensione Z.

  - `Sphere` emette particelle da una posizione casuale all'interno di una sfera. Le particelle sono dirette dal centro verso l'esterno. Il diametro della sfera è definito da *Emitter Size X*.

  - `Cone` emette particelle da una posizione casuale all'interno di un cono 3D. Le particelle sono dirette verso l'esterno attraverso il disco superiore del cono. *Emitter Size X* definisce il diametro del disco superiore e *Y* definisce l'altezza del cono.

  ![Tipi di emettitore](images/particlefx/emitter_types.png)

Particle Orientation
: L'orientamento delle particelle emesse:
  - `Default` imposta l'orientamento unitario
  - `Initial Direction` mantiene l'orientamento iniziale delle particelle emesse.
  - `Movement Direction` adatta l'orientamento delle particelle alla loro velocità.

Inherit Velocity
: Un fattore di scala che stabilisce quanta velocità dell'emettitore debbano ereditare le particelle. Questo valore è disponibile solo quando *Space* è impostato su `World`. La velocità dell'emettitore viene stimata a ogni fotogramma.

Stretch With Velocity
: Seleziona questa opzione per scalare l'eventuale allungamento delle particelle nella direzione del movimento.

### Modalità di fusione {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## Proprietà dell'emettitore animabili tramite curve {#keyable-emitter-properties}

Queste proprietà hanno due campi: un valore e un intervallo di variazione. La variazione viene applicata casualmente a ogni particella generata. Per esempio, se il valore è 50 e la variazione è 3, ogni particella generata riceverà un valore compreso tra 47 e 53 (50 +/- 3).

![Proprietà](images/particlefx/property.png)

Attivando il pulsante della chiave, il valore della proprietà viene controllato da una curva lungo la durata dell'emettitore. Per ripristinare una proprietà controllata da una curva, disattiva il pulsante della chiave.

![Proprietà controllata da una curva](images/particlefx/key.png)

Il *Curve Editor* (disponibile tra le schede della vista inferiore) permette di modificare la curva. Le proprietà controllate da curve non possono essere modificate nella vista *Properties*, ma solo nel *Curve Editor*. <kbd>Fai clic e trascina</kbd> i punti e le tangenti per modificare la forma della curva. <kbd>Fai doppio clic</kbd> sulla curva per aggiungere punti di controllo. Per rimuovere un punto di controllo, <kbd>fai doppio clic</kbd> su di esso.

![Editor delle curve degli effetti particellari](images/particlefx/curve_editor.png)

Per regolare automaticamente lo zoom del Curve Editor in modo da mostrare tutte le curve, premi <kbd>F</kbd>.

Le seguenti proprietà possono essere controllate da curve lungo la durata di riproduzione dell'emettitore:

Spawn Rate
: Il numero di particelle da emettere al secondo.

Emitter Size X/Y/Z
: Le dimensioni della forma dell'emettitore; vedi *Emitter Type* sopra.

Particle Life Time
: La durata di vita di ogni particella generata, in secondi.

Initial Speed
: La velocità iniziale di ogni particella generata.

Initial Size
: Le dimensioni iniziali di ogni particella generata. Se imposti *Size Mode* su `Automatic` e usi un'animazione flipbook come sorgente delle immagini, questa proprietà viene ignorata.

Initial Red/Green/Blue/Alpha
: I valori iniziali delle componenti di colore della tinta delle particelle.

Initial Rotation
: I valori iniziali di rotazione (in gradi) delle particelle.

Initial Stretch X/Y
: I valori iniziali di allungamento (in unità) delle particelle.

Initial Angular Velocity
: La velocità angolare iniziale (in gradi/secondo) di ogni particella generata.

Le seguenti proprietà possono essere controllate da curve lungo la durata di vita delle particelle:

Life Scale
: Il valore di scala nel corso della vita di ogni particella.

Life Red/Green/Blue/Alpha
: Il valore della tinta delle componenti di colore nel corso della vita di ogni particella.

Life Rotation
: Il valore di rotazione (in gradi) nel corso della vita di ogni particella.

Life Stretch X/Y
: Il valore di allungamento (in unità) nel corso della vita di ogni particella.

Life Angular Velocity
: La velocità angolare (in gradi/secondo) nel corso della vita di ogni particella.

## Modificatori {#modifiers}

Sono disponibili quattro tipi di modificatori che agiscono sulla velocità delle particelle:

`Acceleration`
: Accelerazione in una direzione generica.

`Drag`
: Riduce l'accelerazione delle particelle in proporzione alla loro velocità.

`Radial`
: Attrae le particelle verso una posizione oppure le respinge da essa.

`Vortex`
: Fa muovere le particelle in direzione circolare o a spirale attorno alla propria posizione.

  ![Modificatori](images/particlefx/modifiers.png)

## Proprietà dei modificatori {#modifier-properties}

Position/Rotation
: La trasformazione del modificatore rispetto al suo genitore.

Magnitude
: L'intensità dell'effetto che il modificatore esercita sulle particelle.

Max Distance
: La distanza massima entro la quale le particelle sono influenzate da questo modificatore. Usata solo per Radial e Vortex.

## Controllare un effetto particellare {#controlling-a-particle-effect}

Per avviare e arrestare un effetto particellare da uno script:

```lua
-- start the effect component "particles" in the current game object
particlefx.play("#particles")

-- stop the effect component "particles" in the current game object
particlefx.stop("#particles")
```

Per avviare e arrestare un effetto particellare da uno script GUI, consulta il [manuale degli effetti particellari nella GUI](/manuals/gui-particlefx#controlling-the-effect) per maggiori informazioni.

::: sidenote
Un effetto particellare continuerà a emettere particelle anche se viene eliminato l'oggetto di gioco a cui apparteneva il componente dell'effetto particellare.
:::
Consulta la [documentazione di riferimento degli effetti particellari](/ref/particlefx) per maggiori informazioni.

## Costanti del materiale {#material-constants}

Il materiale predefinito degli effetti particellari dispone delle seguenti costanti, che possono essere modificate con `particlefx.set_constant()` e ripristinate con `particlefx.reset_constant()` (consulta il [manuale dei materiali per maggiori dettagli](/manuals/material/#vertex-and-fragment-constants)):

`tint`
: La tinta di colore dell'effetto particellare (`vector4`). Il vector4 rappresenta la tinta, con x, y, z e w corrispondenti alle componenti rosso, verde, blu e alpha. Consulta il [riferimento API per un esempio](/ref/particlefx/#particlefx.set_constant:url-constant-value).


## Configurazione del progetto {#project-configuration}

Il file *game.project* contiene alcune [impostazioni del progetto](/manuals/project-settings#particle-fx) relative alle particelle.
