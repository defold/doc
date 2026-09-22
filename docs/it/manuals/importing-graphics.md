---
title: Importazione e utilizzo della grafica 2D
brief: Questo manuale spiega come importare e utilizzare la grafica 2D.
---

# Importazione della grafica 2D {#importing-2d-graphics}

Defold supporta molti tipi di componenti visivi comunemente usati nei giochi 2D. Puoi usare Defold per creare sprite statici e animati, componenti dell'interfaccia utente, effetti particellari, mappe di tasselli (tile map) e font bitmap. Prima di poter creare questi componenti visivi, devi importare i file immagine contenenti la grafica che vuoi utilizzare. Per importare i file immagine, basta trascinarli dal file system del computer e rilasciarli nella posizione appropriata nel *pannello Assets* dell'editor Defold.

![Importazione dei file](images/graphics/import.png)

::: sidenote
Defold supporta immagini nei formati PNG e JPEG. Le immagini in altri formati devono essere convertite prima di poter essere utilizzate.
:::


## Creazione di asset Defold {#creating-defold-assets}

Una volta importate in Defold, le immagini possono essere usate per creare asset specifici di Defold:

![atlas](images/icons/atlas.png){.icon} Atlas
: Un atlas contiene un elenco di file immagine separati, che vengono combinati automaticamente in una texture più grande. Gli atlas possono contenere immagini statiche e *Animation Groups*, insiemi di immagini che insieme formano un'animazione flipbook.

  ![atlas](images/graphics/atlas.png)

Per saperne di più sulla risorsa atlas, consulta il [manuale degli atlas](/manuals/atlas).

![sorgente di tasselli](images/icons/tilesource.png){.icon} Tile Source
: Una sorgente di tasselli (tile source) fa riferimento a un file immagine già composto da immagini più piccole disposte su una griglia uniforme. Un altro termine comunemente usato per questo tipo di immagine composta è _foglio di sprite (sprite sheet)_. Le sorgenti di tasselli possono contenere animazioni flipbook, definite dal primo e dall'ultimo tassello dell'animazione. È anche possibile usare un'immagine per associare automaticamente forme di collisione ai tasselli.

  ![sorgente di tasselli](images/graphics/tilesource.png)

Per saperne di più sulla risorsa sorgente di tasselli, consulta il [manuale delle sorgenti di tasselli](/manuals/tilesource).

![font bitmap](images/icons/font.png){.icon} Bitmap Font
: Un font bitmap contiene i suoi glifi in un foglio di caratteri PNG. Questi tipi di font non offrono miglioramenti delle prestazioni rispetto ai font generati da file TrueType o OpenType, ma possono includere elementi grafici di qualsiasi tipo, colori e ombre direttamente nell'immagine.

Per saperne di più sui font bitmap, consulta il [manuale dei font](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png)


## Utilizzo degli asset Defold {#using-defold-assets}

Dopo aver convertito le immagini in file Atlas e Tile Source, puoi usarli per creare diversi tipi di componenti visivi:

![sprite](images/icons/sprite.png){.icon}
: Uno sprite è un'immagine statica o un'animazione flipbook visualizzata sullo schermo.

  ![sprite](images/graphics/sprite.png)

Per saperne di più sugli sprite, consulta il [manuale degli sprite](/manuals/sprite).

![mappa di tasselli](images/icons/tilemap.png){.icon} Tile map
: Un componente mappa di tasselli assembla una mappa usando tasselli (immagini e forme di collisione) provenienti da una sorgente di tasselli. Le mappe di tasselli non possono usare atlas come sorgenti.

  ![mappa di tasselli](images/graphics/tilemap.png)

Per saperne di più sulle mappe di tasselli, consulta il [manuale delle mappe di tasselli](/manuals/tilemap).

![effetto particellare](images/icons/particlefx.png){.icon} Particle fx
: Le particelle generate da un emettitore di particelle sono costituite da un'immagine statica o da un'animazione flipbook proveniente da un atlas o da una sorgente di tasselli.

  ![particelle](images/graphics/particles.png)

Per saperne di più sugli effetti particellari, consulta il [manuale degli effetti particellari](/manuals/particlefx).

![GUI](images/icons/gui.png){.icon} GUI
: I nodi rettangolari (box) e a settore circolare (pie) della GUI possono usare immagini statiche e animazioni flipbook provenienti da atlas e sorgenti di tasselli.

  ![GUI](images/graphics/gui.png)

Per saperne di più sulle GUI, consulta il [manuale della GUI](/manuals/gui).
