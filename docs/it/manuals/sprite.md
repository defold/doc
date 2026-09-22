---
title: Visualizzare immagini 2D
brief: Questo manuale descrive come visualizzare immagini e animazioni 2D con il componente sprite.
---

# Sprite {#sprites}

Un componente sprite è una semplice immagine o un'animazione a fotogrammi (flipbook) visualizzata sullo schermo.

![sprite](images/graphics/sprite.png)

Il componente sprite può usare un [atlas](/manuals/atlas) o una [sorgente di tile (Tile Source)](/manuals/tilesource) per la propria grafica.

## Proprietà dello sprite {#sprite-properties}

Oltre alle proprietà *Id*, *Position* e *Rotation*, sono disponibili le seguenti proprietà specifiche del componente:

*Image*
: Se lo shader ha un solo campionatore, questo campo si chiama `Image`. Altrimenti, ogni slot prende il nome del campionatore di texture nel materiale.
Ogni slot specifica la risorsa atlas o sorgente di tile da usare per lo sprite con quel campionatore di texture.

*Default Animation*
: L'animazione da usare per lo sprite. Le informazioni sull'animazione vengono ricavate dal primo atlas o dalla prima sorgente di tile.

*Material*
: Il materiale da usare per il rendering dello sprite.

*Blend Mode*
: La modalità di fusione da usare per il rendering dello sprite.

*Size Mode*
: Se impostata su `Automatic`, l'editor determina le dimensioni dello sprite. Se impostata su `Manual`, puoi impostarle tu.

*Slice 9*
: Imposta questa proprietà per preservare le dimensioni in pixel della texture dello sprite lungo i bordi quando lo sprite viene ridimensionato.

:[Slice-9](../shared/slice-9-texturing.md)

### Modalità di fusione {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## Modifiche a runtime {#runtime-manipulation}

Puoi modificare gli sprite durante l'esecuzione tramite varie funzioni e proprietà (consulta la [documentazione API per l'utilizzo](/ref/sprite/)). Funzioni:

* `sprite.play_flipbook()` - Riproduce un'animazione su un componente sprite.
* `sprite.set_hflip()` e `sprite.set_vflip()` - Impostano il ribaltamento orizzontale e verticale dell'animazione di uno sprite.

Uno sprite ha anche diverse proprietà che puoi modificare con `go.get()` e `go.set()`:

`cursor`
: Il cursore normalizzato dell'animazione (`number`).

`image`
: L'immagine dello sprite (`hash`). Puoi cambiarla usando una proprietà di risorsa di tipo atlas o sorgente di tile e `go.set()`. Consulta il [riferimento API per un esempio](/ref/sprite/#image).

`material`
: Il materiale dello sprite (`hash`). Puoi cambiarlo usando una proprietà di risorsa di tipo materiale e `go.set()`. Consulta il [riferimento API per un esempio](/ref/sprite/#material).

`playback_rate`
: La velocità di riproduzione dell'animazione (`number`).

`scale`
: La scala non uniforme dello sprite (`vector3`).

`size`
: Le dimensioni dello sprite (`vector3`). Puoi modificarle solo se la proprietà `Size Mode` dello sprite è impostata su `Manual`.

## Costanti del materiale {#material-constants}

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: La tinta dello sprite (`vector4`). Il `vector4` rappresenta la tinta: `x`, `y`, `z` e `w` corrispondono rispettivamente ai componenti rosso, verde, blu e alfa.

## Attributi del materiale {#material-attributes}

Uno sprite può sovrascrivere gli attributi dei vertici del materiale attualmente assegnato, che il componente passa al vertex shader (consulta il [manuale sui materiali per maggiori dettagli](/manuals/material/#attributes)).

Gli attributi specificati nel materiale vengono visualizzati come normali proprietà nell'ispettore e possono essere impostati sui singoli componenti sprite. Se un attributo viene sovrascritto, viene visualizzato come una proprietà sovrascritta e salvato nel file dello sprite su disco:

![Attributi dello sprite](../images/graphics/sprite-attributes.png)

## Configurazione del progetto {#project-configuration}

Il file *game.project* contiene alcune [impostazioni del progetto](/manuals/project-settings#sprite) relative agli sprite.

## Sprite con più texture {#multi-textured-sprites}

Quando uno sprite usa più texture, ci sono alcuni aspetti da considerare.

### Animazioni {#animations}

I dati dell'animazione (fps, nomi dei fotogrammi) vengono attualmente ricavati dalla prima texture. La chiameremo "animazione guida".

Gli ID delle immagini dell'animazione guida vengono usati per cercare le immagini in un'altra texture.
È quindi importante assicurarsi che gli ID dei fotogrammi corrispondano tra le texture.

Per esempio, se `diffuse.atlas` contiene un'animazione `run` come questa:

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

Gli ID dei fotogrammi sarebbero quindi del tipo `run/hero_run_color_1`, che difficilmente si troverebbe, per esempio, in un `normal.atlas`:

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

Per rinominarli usiamo quindi `Rename patterns` nell'[atlas](/manuals/material/).
Imposta `_color=` e `_normal=` nei rispettivi atlas e otterrai nomi dei fotogrammi come questi in entrambi gli atlas:

```
run/hero_run_1
run/hero_run_2
...
```

### Coordinate UV {#uvs}

Le coordinate UV vengono ricavate dalla prima texture. Poiché esiste un solo insieme di vertici, non possiamo garantire
una buona corrispondenza se le texture secondarie hanno più coordinate UV o una forma diversa.

È importante tenerne conto: assicurati che le immagini abbiano forme sufficientemente simili, altrimenti potresti riscontrare artefatti di contaminazione dei bordi delle texture.

Le dimensioni delle immagini in ciascuna texture possono essere diverse.
