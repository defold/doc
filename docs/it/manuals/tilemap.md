---
title: Manuale delle mappe di tasselli di Defold
brief: Questo manuale descrive in dettaglio il supporto di Defold per le mappe di tasselli.
---

# Mappa di tasselli {#tile-map}

Una *mappa di tasselli (tile map)* è un componente che permette di disporre, o dipingere, i tasselli di una *sorgente di tasselli (tile source)* su un'ampia area a griglia. Le mappe di tasselli vengono comunemente usate per costruire gli ambienti dei livelli di gioco. Nelle mappe puoi anche usare le *forme di collisione (Collision Shapes)* della sorgente di tasselli per il rilevamento delle collisioni e la simulazione fisica ([esempio](/examples/tilemap/collisions/)).

Prima di creare una mappa di tasselli devi creare una sorgente di tasselli. Consulta il [manuale delle sorgenti di tasselli](/manuals/tilesource) per sapere come crearne una.

## Creare una mappa di tasselli {#creating-a-tile-map}

Per creare una nuova mappa di tasselli:

- <kbd>Fai clic con il tasto destro</kbd> su una posizione nel browser *Assets*, quindi seleziona <kbd>New... ▸ Tile Map</kbd>).
- Assegna un nome al file.
- La nuova mappa di tasselli si apre automaticamente nell'editor delle mappe di tasselli.

  ![Nuova mappa di tasselli](images/tilemap/tilemap.png)

- Imposta la proprietà *Tile Source* su un file di sorgente di tasselli che hai preparato.

Per dipingere tasselli sulla mappa:

1. Seleziona o crea un *Layer* su cui dipingere nella vista *Outline*.
2. Seleziona un tassello da usare come pennello (premi <kbd>Space</kbd> per mostrare la tavolozza dei tasselli), oppure seleziona più tasselli facendo clic e trascinando nella tavolozza per creare un pennello rettangolare composto da più tasselli.

   ![Tavolozza](images/tilemap/palette.png)

3. Dipingi con il pennello selezionato. Per cancellare un tassello, scegli un tassello vuoto e usalo come pennello, oppure seleziona la gomma (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Dipingere tasselli](images/tilemap/paint_tiles.png)

Puoi prelevare tasselli direttamente da un livello e usare la selezione come pennello. Tieni premuto <kbd>Shift</kbd> e fai clic su un tassello per impostarlo come pennello corrente. Tenendo premuto <kbd>Shift</kbd> puoi anche fare clic e trascinare per selezionare un blocco di tasselli da usare come pennello più grande. Allo stesso modo, puoi tagliare i tasselli tenendo premuto <kbd>Shift+Ctrl</kbd> o cancellarli tenendo premuto <kbd>Shift+Alt</kbd>.

Per ruotare il pennello in senso orario, usa <kbd>Z</kbd>. Usa <kbd>X</kbd> per ribaltare il pennello in orizzontale e <kbd>Y</kbd> per ribaltarlo in verticale.

![Prelevare tasselli](images/tilemap/pick_tiles.png)

## Aggiungere una mappa di tasselli al gioco {#adding-a-tile-map-to-your-game}

Per aggiungere una mappa di tasselli al gioco:

1. Crea un oggetto di gioco che contenga il componente mappa di tasselli. L'oggetto di gioco può trovarsi in un file o essere creato direttamente in una collezione.
2. Fai clic con il tasto destro sulla radice dell'oggetto di gioco e seleziona <kbd>Add Component File</kbd>.
3. Seleziona il file della mappa di tasselli.

![Usare una mappa di tasselli](images/tilemap/use_tilemap.png)

## Modifiche durante l'esecuzione {#runtime-manipulation}

Puoi modificare le mappe di tasselli durante l'esecuzione tramite varie funzioni e proprietà (consulta la [documentazione API per le istruzioni d'uso](/ref/tilemap/)).

### Modificare i tasselli da uno script {#changing-tiles-from-script}

Puoi leggere e scrivere dinamicamente il contenuto di una mappa di tasselli mentre il gioco è in esecuzione. Per farlo, usa le funzioni [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) e [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile):

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Proprietà della mappa di tasselli {#tilemap-properties}

Oltre alle proprietà *Id*, *Position*, *Rotation* e *Scale*, sono disponibili le seguenti proprietà specifiche del componente:

*Tile Source*
: La risorsa sorgente di tasselli da usare per la mappa di tasselli.

*Material*
: Il materiale da usare per il rendering della mappa di tasselli.

*Blend Mode*
: La modalità di fusione da usare per il rendering della mappa di tasselli.

### Modalità di fusione {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Modificare le proprietà {#changing-properties}

Una mappa di tasselli ha varie proprietà che possono essere modificate usando `go.get()` e `go.set()`:

`tile_source`
: La sorgente di tasselli della mappa (`hash`). Puoi cambiarla usando una proprietà di risorsa di tipo sorgente di tasselli e `go.set()`. Consulta la [documentazione di riferimento dell'API per un esempio](/ref/tilemap/#tile_source).

`material`
: Il materiale della mappa di tasselli (`hash`). Puoi cambiarlo usando una proprietà di risorsa di tipo materiale e `go.set()`. Consulta la [documentazione di riferimento dell'API per un esempio](/ref/tilemap/#material).

### Costanti del materiale {#material-constants}

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: La tinta della mappa di tasselli (`vector4`). Il tipo `vector4` viene usato per rappresentare la tinta, con x, y, z e w che corrispondono rispettivamente alle componenti rosso, verde, blu e alfa della tinta.

## Configurazione del progetto {#project-configuration}

Il file *game.project* contiene alcune [impostazioni del progetto](/manuals/project-settings#tilemap) relative alle mappe di tasselli.

## Strumenti esterni {#external-tools}

Esistono editor esterni di mappe e livelli che possono esportare direttamente nel formato delle mappe di tasselli di Defold:

### Tiled

[Tiled](https://www.mapeditor.org/) è un editor di mappe noto e molto diffuso, adatto a mappe ortogonali, isometriche ed esagonali. Tiled supporta numerose funzionalità e può [esportare direttamente per Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/). Per saperne di più su come esportare i dati delle mappe di tasselli e metadati aggiuntivi, consulta [questo articolo del blog dell'utente Defold "goeshard"](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) permette di creare automaticamente insiemi completi di tasselli a partire da semplici tasselli di base e dispone di un editor di mappe che può esportare direttamente per Defold.



