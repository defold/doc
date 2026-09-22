---
title: Modelli 3D in Defold
brief: Questo manuale descrive come integrare modelli 3D, scheletri e animazioni nel tuo gioco.
---

# Componente modello {#model-component}

Defold è, alla base, un motore 3D. Anche quando lavori soltanto con contenuti 2D, tutto il rendering avviene in 3D, ma viene proiettato ortograficamente sullo schermo. Defold ti permette di utilizzare contenuti interamente 3D includendo asset 3D, o _modelli (Model)_, nelle tue collezioni. Puoi creare giochi esclusivamente in 3D con soli asset 3D, oppure combinare contenuti 3D e 2D come preferisci.

## Creazione di un componente modello {#creating-a-model-component}

I componenti modello si creano come qualsiasi altro componente di un oggetto di gioco. Puoi farlo in due modi:

- Crea un *file Model* <kbd>facendo clic con il pulsante destro</kbd> su una posizione nel browser *Assets* e selezionando <kbd>New... ▸ Model</kbd>.
- Crea il componente incorporato direttamente in un oggetto di gioco <kbd>facendo clic con il pulsante destro</kbd> su un oggetto di gioco nella vista *Outline* e selezionando <kbd>Add Component ▸ Model</kbd>.

![Modello in un oggetto di gioco](images/model/model_gltf.png)

Una volta creato il modello, devi specificare alcune proprietà:

### Proprietà del modello {#model-properties}

Oltre alle proprietà *Id*, *Position* e *Rotation*, sono disponibili le seguenti proprietà specifiche del componente:

*Scene*
: Il file glTF *.gltf* o *.glb* che contiene la geometria del modello. Se il file contiene forme di destinazione (morph target), queste vengono importate insieme alla scena. Prima di Defold 1.13.2, questa proprietà si chiamava *Mesh*.

*Mesh*
: Una mesh con nome facoltativa della *Scene* selezionata, disponibile da Defold 1.13.2. Lascia vuoto questo campo per renderizzare l'intera scena con le sue trasformazioni importate. Seleziona una mesh per renderizzarla una sola volta nelle sue coordinate locali, senza le trasformazioni dei nodi glTF. Sposta, ruota e scala il componente modello o il suo oggetto di gioco per posizionare la mesh selezionata.

*Create GO Bones*
: Seleziona questa opzione per creare un oggetto di gioco per ogni osso del modello. Puoi utilizzare questi oggetti di gioco per collegare altri oggetti di gioco, per esempio armi alle ossa delle mani e così via. 

*Skeleton*
: Questa proprietà deve fare riferimento al file glTF *.gltf* o *.glb* che contiene lo scheletro da utilizzare per l'animazione. Tieni presente che Defold richiede un unico osso radice nella gerarchia.

*Animations*
: Imposta questa proprietà sul file *Animation Set File* che contiene le animazioni da utilizzare sul modello.

*Default Animation*
: Questa è l'animazione, scelta dall'insieme di animazioni, che verrà riprodotta automaticamente sul modello.

Oltre alle proprietà precedenti, è presente anche un campo per assegnare un materiale a ciascuna mesh del modello:

*Material*
: Imposta questa proprietà su un materiale che hai creato e che sia adatto a un oggetto 3D con texture. Sono disponibili diversi materiali integrati che puoi utilizzare come punto di partenza:

  * Usa *model.material* per modelli statici senza istanziazione
  * Usa *model_instanced.material* per modelli statici con istanziazione
  * Usa *model_skinned.material* per modelli con deformazione scheletrica (animati) senza istanziazione
  * Usa *model_skinned_instanced.material* per modelli con deformazione scheletrica (animati) con istanziazione

In base al materiale, saranno presenti una o più proprietà per le texture:

*Texture*
: Questa proprietà deve puntare al file immagine della texture da applicare all'oggetto.


## Modifiche nell'editor {#editor-manipulation}

Una volta aggiunto il componente modello, puoi modificare e manipolare il componente e/o l'oggetto di gioco che lo contiene con i normali strumenti dello *Scene Editor*, per spostare, ruotare e ridimensionare il modello come preferisci.

## Modifiche a runtime {#runtime-manipulation}

Puoi manipolare i modelli durante l'esecuzione tramite diverse funzioni e proprietà (consulta la [documentazione API per le istruzioni d'uso](/ref/model/)).

![Wiggler nel gioco](images/model/runtime.png)

### Animazione a runtime {#runtime-animation}

Defold offre un potente supporto per il controllo delle animazioni durante l'esecuzione. Trovi maggiori informazioni nel [manuale delle animazioni dei modelli](/manuals/model-animation):

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

Il cursore di riproduzione dell'animazione può essere animato manualmente oppure tramite il sistema di animazione delle proprietà:

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

I modelli possono utilizzare anche animazioni glTF con forme di destinazione. I pesi delle forme di destinazione vengono animati con `model.play_anim()` come le altre animazioni dei modelli e possono essere letti o sovrascritti durante l'esecuzione tramite [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) e [`model.set_blend_weights()`](/ref/model#model.set_blend_weights). Per i dettagli, consulta la [sezione sulle forme di destinazione](/manuals/model-animation#morph-targets) nel manuale delle animazioni dei modelli.

### Modifica delle proprietà {#changing-properties}

Un modello dispone inoltre di diverse proprietà che puoi modificare utilizzando `go.get()` e `go.set()`:

`animation`
: L'animazione corrente del modello (`hash`) (SOLA LETTURA). Puoi cambiare l'animazione utilizzando `model.play_anim()` (vedi sopra).

`cursor`
: Il cursore normalizzato dell'animazione (`number`).

`material`
: Il materiale del modello (`hash`). Puoi modificarlo utilizzando una proprietà di risorsa materiale e `go.set()`. Consulta il [riferimento API per un esempio](/ref/model/#material).

`playback_rate`
: La velocità di riproduzione dell'animazione (`number`).

`textureN`
: Le texture del modello, dove N è compreso tra 0 e 15 (`hash`). Puoi leggere queste proprietà con `go.get()` e modificarle utilizzando una proprietà di risorsa texture e `go.set()`. Defold supporta al massimo 16 texture per chiamata di disegno, ma il numero utilizzabile da uno shader può essere inferiore con adattatori grafici che hanno un limite più basso di campionatori di texture.


## Materiale {#material}

I software 3D consentono generalmente di impostare proprietà sui vertici degli oggetti, come il colore e le texture. Queste informazioni vengono inserite nel file glTF *.gltf* o *.glb* che esporti dal software 3D. In base ai requisiti del tuo gioco, dovrai selezionare e/o creare materiali appropriati e _efficienti_ per i tuoi oggetti. Un materiale combina _programmi shader_ con un insieme di parametri per il rendering dell'oggetto.

Sono disponibili diversi materiali integrati che puoi utilizzare come punto di partenza:

  * Usa *model.material* per modelli statici senza istanziazione
  * Usa *model_instanced.material* per modelli statici con istanziazione
  * Usa *model_skinned.material* per modelli con deformazione scheletrica (animati) senza istanziazione
  * Usa *model_skinned_instanced.material* per modelli con deformazione scheletrica (animati) con istanziazione

I materiali integrati per i modelli usano lo spazio locale dei vertici. Per i modelli con deformazione scheletrica, lo spazio locale dei vertici consente al vertex shader di eseguire la deformazione sulla GPU tramite una texture delle matrici delle ossa; lo spazio locale dei vertici è necessario anche per l'istanziazione dei modelli. Un materiale personalizzato destinato a modelli con deformazione scheletrica sulla GPU o con istanziazione deve quindi utilizzare l'impostazione *Local* per lo spazio dei vertici.

La cache delle matrici delle ossa utilizza una texture `RGBA32F`. Se l'adattatore grafico attivo non supporta questo formato di texture, Defold non può creare un componente modello animato che utilizza un materiale nello spazio locale. Su OpenGL ES 2.0 e WebGL 1.0, il supporto dipende quindi dall'estensione dell'adattatore per le texture in virgola mobile. Per la compatibilità con un adattatore che ne è privo, utilizza un materiale personalizzato nello spazio del mondo, che esegue la deformazione scheletrica sulla CPU e non può utilizzare l'istanziazione dei modelli. Puoi regolare le dimensioni della cache nelle [impostazioni del progetto per i modelli](/manuals/project-settings/#model).

Se devi creare materiali personalizzati per i tuoi modelli, consulta la [documentazione sui materiali](/manuals/material). Il [manuale degli shader](/manuals/shader) contiene informazioni sul funzionamento dei programmi shader.


### Costanti del materiale {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: La tinta del modello (`vector4`). Il `vector4` rappresenta la tinta, con x, y, z e w corrispondenti alle componenti rosso, verde, blu e alfa.


## Rendering

Lo script di rendering predefinito è progettato specificamente per i giochi 2D e non funziona con i modelli 3D. Tuttavia, copiando lo script di rendering predefinito e aggiungendovi poche righe di codice, puoi abilitare il rendering dei tuoi modelli. Per esempio:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

Consulta la [documentazione sul rendering](/manuals/render) per i dettagli sul funzionamento degli script di rendering.
