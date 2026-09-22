---
title: Nodi Box della GUI in Defold
brief: Questo manuale spiega come usare i nodi Box della GUI.
---

# Nodi Box della GUI {#gui-box-nodes}

Un nodo Box è un rettangolo riempito con un colore, una texture o un'animazione.

## Aggiunta di nodi Box {#adding-box-nodes}

Aggiungi nuovi nodi Box con un <kbd>clic destro</kbd> nella vista *Outline* e selezionando <kbd>Add ▸ Box</kbd>, oppure premi <kbd>A</kbd> e seleziona <kbd>Box</kbd>.

Puoi usare immagini e animazioni degli atlas o delle sorgenti di tasselli (tile source) aggiunti alla GUI. Per aggiungere texture, fai <kbd>clic destro</kbd> sull'icona della cartella *Textures* nella vista *Outline* e seleziona <kbd>Add ▸ Textures...</kbd>. Quindi imposta la proprietà *Texture* del nodo Box:

![Texture](images/gui-box/create.png)

Il colore del nodo Box applica una tinta alla grafica. La tinta viene moltiplicata per i dati dell'immagine: se imposti il colore su bianco (il valore predefinito), non viene applicata alcuna tinta.

![Texture con tinta applicata](images/gui-box/tinted.png)

Il rendering dei nodi Box viene sempre eseguito, anche se non hanno una texture assegnata, se il loro alfa è impostato su `0` o se le loro dimensioni sono `0, 0, 0`. Assegna sempre una texture ai nodi Box, in modo che il sistema di rendering possa raggrupparli correttamente e ridurre il numero di chiamate di disegno.

## Riproduzione delle animazioni {#playing-animations}

I nodi Box possono riprodurre animazioni da atlas o sorgenti di tasselli. Consulta il [manuale delle animazioni flipbook](/manuals/flipbook-animation) per saperne di più.

:[Slice-9](../shared/slice-9-texturing.md)
