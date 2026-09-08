---
title: Manuale degli atlas
brief: Questo manuale spiega come funzionano le risorse atlas in Defold.
---

# Atlas

Sebbene spesso si usino immagini singole come sorgente per gli sprite, per ragioni di prestazioni è necessario combinarle in insiemi più grandi, chiamati atlas. Combinare insiemi di immagini più piccole in atlas è particolarmente importante sui dispositivi mobili, dove memoria e potenza di elaborazione sono più limitate rispetto ai computer desktop o alle console di gioco dedicate.

In Defold, una risorsa atlas è un elenco di file di immagini separati, che vengono combinati automaticamente in un'immagine più grande.

## Creazione di un atlas {#creating-an-atlas}

Seleziona <kbd>New... ▸ Atlas</kbd> dal menu contestuale nel browser *Assets*. Assegna un nome al nuovo file atlas. L'editor aprirà il file nell'editor degli atlas. Le proprietà dell'atlas vengono mostrate nel
pannello *Properties*, dove puoi modificarle (vedi sotto per i dettagli).

Devi aggiungere immagini o animazioni a un atlas prima di poterlo usare come sorgente grafica per i componenti degli oggetti, come gli sprite e i componenti ParticleFX.

Assicurati di aver aggiunto le immagini al progetto (trascina e rilascia i file delle immagini nella posizione corretta nel browser *Assets*)

Aggiunta di immagini singole

: Trascina e rilascia le immagini dal pannello *Asset* nella vista dell'editor.
  
  In alternativa, <kbd>fai clic con il pulsante destro</kbd> sulla voce radice Atlas nel pannello *Outline*.

  Seleziona <kbd>Add Images</kbd> dal menu contestuale che compare per aggiungere immagini singole.

  Si apre una finestra di dialogo in cui puoi trovare e selezionare le immagini da aggiungere all'atlas. Puoi filtrare i file delle immagini e selezionare più file contemporaneamente.

  ![Creazione di un atlas, aggiunta di immagini](images/atlas/add.png)

  Le immagini aggiunte sono elencate in *Outline* e l'intero atlas è visibile nella vista centrale dell'editor. Potrebbe essere necessario premere <kbd>F</kbd> (<kbd>View ▸ Frame Selection</kbd> dal menu) per inquadrare la selezione.

  ![Immagini aggiunte](images/atlas/single_images.png)

Aggiunta di animazioni flipbook
: <kbd>Fai clic con il pulsante destro</kbd> sulla voce radice Atlas nel pannello *Outline*.

  Seleziona <kbd>Add Animation Group</kbd> dal menu contestuale che compare per creare un gruppo di animazione flipbook.

  All'atlas viene aggiunto un nuovo gruppo di animazione vuoto con un nome predefinito (`New Animation`).

  Trascina e rilascia le immagini dal pannello *Asset* nella vista dell'editor per aggiungerle al gruppo attualmente selezionato.
  
  In alternativa, <kbd>fai clic con il pulsante destro</kbd> sul nuovo gruppo e seleziona <kbd>Add Images</kbd> dal menu contestuale.

  Si apre una finestra di dialogo in cui puoi trovare e selezionare le immagini da aggiungere al gruppo di animazione.

  ![Creazione di un atlas, aggiunta di immagini](images/atlas/add_animation.png)

  Premi <kbd>Space</kbd> con il gruppo di animazione selezionato per visualizzarne l'anteprima e <kbd>Ctrl/Cmd+T</kbd> per chiudere l'anteprima. Regola le proprietà dell'animazione in *Properties* secondo necessità (vedi sotto).

  ![Gruppo di animazione](images/atlas/animation_group.png)

Puoi riordinare le immagini in Outline selezionandole e premendo <kbd>Alt + Up/down</kbd>. Puoi anche creare facilmente duplicati copiando e incollando le immagini in Outline (dal menu <kbd>Edit</kbd>, dal menu contestuale accessibile con il pulsante destro o tramite le scorciatoie da tastiera).

## Proprietà dell'atlas {#atlas-properties}

Ogni risorsa atlas ha un insieme di proprietà. Queste vengono mostrate nel pannello *Properties* quando selezioni l'elemento radice nella vista *Outline*.

Size
: Mostra le dimensioni totali calcolate della risorsa texture risultante. La larghezza e l'altezza vengono impostate alla potenza di due più vicina. Tieni presente che, se attivi la compressione delle texture, alcuni formati richiedono texture quadrate. Le texture non quadrate vengono quindi ridimensionate e riempite con spazio vuoto per renderle quadrate. Consulta il [manuale dei profili delle texture](/manuals/texture-profiles/) per i dettagli.

Margin
: Il numero di pixel da aggiungere tra un'immagine e l'altra.

Inner Padding
: Il numero di pixel vuoti da aggiungere attorno a ogni immagine.

Extrude Borders
: Il numero di pixel del bordo da ripetere attorno a ogni immagine. Quando il fragment shader campiona i pixel sul bordo di un'immagine, i pixel di un'immagine vicina (sulla stessa texture dell'atlas) possono contaminare il risultato. L'estrusione del bordo risolve questo problema.

Max Page Size
: Le dimensioni massime di una pagina in un atlas a più pagine. Questa proprietà permette di suddividere un atlas in più pagine dello stesso atlas per limitarne le dimensioni, continuando a usare una sola chiamata di disegno. Questa funzionalità deve essere usata insieme ai materiali che supportano gli atlas a più pagine, disponibili in `/builtins/materials/*_paged_atlas.material`.

![Atlas a più pagine](images/atlas/multipage_atlas.png)

Rename Patterns
: Un elenco di schemi di ricerca e sostituzione separati da virgole (´,´), in cui ogni schema ha la forma `search=replace`.
Il nome originale di ogni immagine (il nome del file senza estensione) viene trasformato usando questi schemi. (Ad esempio, lo schema `hat=cat,_normal=` rinomina un'immagine chiamata `hat_normal` in `cat`). Questo è utile per far corrispondere le animazioni tra atlas.

Ecco alcuni esempi delle diverse impostazioni delle proprietà con quattro immagini quadrate di dimensioni 64x64 aggiunte a un atlas. Nota come l'atlas passi a 256x256 non appena le immagini non rientrano più in 128x128, causando un notevole spreco di spazio nella texture.

![Proprietà dell'atlas](images/atlas/atlas_properties.png)

## Proprietà delle immagini {#image-properties}

Ogni immagine in un atlas ha un insieme di proprietà:

Id
: L'ID dell'immagine (sola lettura).

Size
: La larghezza e l'altezza dell'immagine (sola lettura).

Pivot
: Il punto di riferimento dell'immagine (in unità). L'angolo superiore sinistro è (0,0) e quello inferiore destro è (1,1). Il valore predefinito è (0.5, 0.5). Il punto di riferimento può trovarsi al di fuori dell'intervallo 0-1. È il punto rispetto al quale l'immagine viene centrata quando viene usata, ad esempio, in uno sprite. Puoi modificarlo trascinando la relativa maniglia nella vista dell'editor. La maniglia è visibile solo quando è selezionata una singola immagine. Puoi attivare l'aggancio tenendo premuto <kbd>Shift</kbd> durante il trascinamento.

Sprite Trim Mode
: Il modo in cui viene disegnato lo sprite. Per impostazione predefinita, lo sprite viene disegnato come un rettangolo (Sprite Trim Mode impostato su Off). Se lo sprite contiene molti pixel trasparenti, può essere più efficiente disegnarlo come una forma non rettangolare usando da 4 a 8 vertici. Tieni presente che il ritaglio degli sprite non funziona con gli sprite slice-9.

Image
: Il percorso dell'immagine.

![Proprietà delle immagini](images/atlas/image_properties.png)

## Proprietà delle animazioni {#animation-properties}

Oltre all'elenco delle immagini che fanno parte di un gruppo di animazione, è disponibile un insieme di proprietà:

Id
: Il nome dell'animazione.

Fps
: La velocità di riproduzione dell'animazione, espressa in fotogrammi al secondo (FPS).

Flip horizontal
: Capovolge l'animazione in orizzontale.

Flip vertical
: Capovolge l'animazione in verticale.

Playback
: Specifica come deve essere riprodotta l'animazione:

  - `None` non riproduce l'animazione e mostra la prima immagine.
  - `Once Forward` riproduce l'animazione una volta dalla prima all'ultima immagine.
  - `Once Backward` riproduce l'animazione una volta dall'ultima alla prima immagine.
  - `Once Ping Pong` riproduce l'animazione una volta dalla prima all'ultima immagine e poi torna alla prima immagine.
  - `Loop Forward` riproduce l'animazione ripetutamente dalla prima all'ultima immagine.
  - `Loop Backward` riproduce l'animazione ripetutamente dall'ultima alla prima immagine.
  - `Loop Ping Pong` riproduce l'animazione ripetutamente dalla prima all'ultima immagine e poi torna alla prima immagine.

## Creazione di texture e atlas a runtime {#runtime-texture-and-atlas-creation}

È possibile creare una texture e un atlas durante l'esecuzione.

### Creazione di una risorsa texture a runtime {#creating-a-texture-resource-at-runtime}

Usa [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) per creare una nuova risorsa texture:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Una volta creata la texture, puoi usare [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) per impostarne i pixel:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
Puoi usare `resource.set_texture()` anche per aggiornare una porzione della texture, usando un buffer con larghezza e altezza inferiori alle dimensioni totali della texture e modificando i parametri x e y di `resource.set_texture()`.
:::

La texture può essere usata direttamente su un [componente modello](/manuals/model/) tramite `go.set()`:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Creazione di un atlas a runtime {#creating-an-atlas-at-runtime}

Per usare la texture su un [componente sprite](/manuals/sprite/), devi prima usarla in un atlas. Usa [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) per creare un atlas:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

Le voci di `frames` sono indici con base 1 nella tabella `geometries`. Un elenco può riutilizzare, riordinare o saltare le geometrie, operazioni che non possono essere rappresentate dai campi di intervallo deprecati `frame_start` e `frame_end`. `resource.get_atlas()` restituisce `frames`; usa la stessa rappresentazione quando passi i dati dell'atlas a `resource.set_atlas()` o `resource.create_atlas()`. Le funzioni di impostazione e creazione accettano ancora i campi di intervallo per compatibilità, ma il nuovo codice dovrebbe usare `frames`.
