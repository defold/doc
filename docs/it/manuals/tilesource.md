---
title: Manuale delle sorgenti di tasselli di Defold
brief: Questo manuale descrive come utilizzare e creare una sorgente di tasselli.
---

# Sorgente di tasselli {#tile-source}

Una *sorgente di tasselli (tile source)* può essere utilizzata da un [componente mappa di tasselli (tile map)](/manuals/tilemap) per disegnare tasselli su una griglia, oppure come sorgente grafica per uno [sprite](/manuals/sprite) o un [componente effetto particellare](/manuals/particlefx). Puoi anche utilizzare le *forme di collisione* della sorgente di tasselli in una mappa di tasselli per il [rilevamento delle collisioni e la simulazione fisica](/manuals/physics) ([esempio](/examples/tilemap/collisions/)).

## Creare una sorgente di tasselli {#creating-a-tile-source}

Ti serve un'immagine che contenga tutti i tasselli. Ogni tassello deve avere esattamente le stesse dimensioni ed essere disposto in una griglia. Defold supporta una _spaziatura_ tra i tasselli e un _margine_ attorno a ogni tassello.

![Immagine dei tasselli](images/tilemap/small_map.png)

Una volta creata l'immagine sorgente, puoi creare una sorgente di tasselli:

- Importa l'immagine nel progetto trascinandola in una posizione del progetto nel pannello *Assets*.
- Crea un nuovo file sorgente di tasselli (<kbd>fai clic con il pulsante destro</kbd> su una posizione nel pannello *Assets*, quindi seleziona <kbd>New... ▸ Tile Source</kbd>).
- Assegna un nome al nuovo file.
- Il file si apre nell'editor delle sorgenti di tasselli.
- Fai clic sul pulsante di selezione accanto alla proprietà *Image* e seleziona la tua immagine. Ora dovresti vedere l'immagine nell'editor.
- Regola le impostazioni in *Properties* in modo che corrispondano all'immagine sorgente. Quando tutto è corretto, i tasselli saranno perfettamente allineati.

![Creazione di una sorgente di tasselli](images/tilemap/tilesource.png)

Size
: Le dimensioni dell'immagine sorgente.

Tile Width
: La larghezza di ogni tassello.

Tile Height
: L'altezza di ogni tassello.

Tile Margin
: Il numero di pixel che circondano ogni tassello (in arancione nell'immagine sopra).

Tile Spacing
: Il numero di pixel tra un tassello e l'altro (in blu nell'immagine sopra).

Inner Padding
: Specifica quanti pixel vuoti aggiungere automaticamente attorno al tassello nella texture risultante utilizzata durante l'esecuzione del gioco.

Extrude Border
: Specifica quante volte replicare automaticamente i pixel del bordo attorno al tassello nella texture risultante utilizzata durante l'esecuzione del gioco.

Collision
: Specifica l'immagine da utilizzare per generare automaticamente le forme di collisione dei tasselli.

## Animazioni a fotogrammi delle sorgenti di tasselli {#tile-source-flip-book-animations}

Per definire un'animazione in una sorgente di tasselli, i tasselli dei fotogrammi dell'animazione devono essere adiacenti, in una sequenza da sinistra a destra. La sequenza può proseguire da una riga a quella successiva. Tutte le sorgenti di tasselli appena create hanno un'animazione predefinita chiamata "`anim`". Puoi aggiungere nuove animazioni <kbd>facendo clic con il pulsante destro</kbd> sulla radice della sorgente di tasselli nella vista *Outline* e selezionando <kbd>Add ▸ Animation</kbd>.

Selezionando un'animazione, ne visualizzi le proprietà in *Properties*.

![Animazione della sorgente di tasselli](images/tilemap/animation.png)

Id
: L'identificatore dell'animazione. Deve essere univoco all'interno della sorgente di tasselli.

Start Tile
: Il primo tassello dell'animazione. La numerazione parte da 1 nell'angolo superiore sinistro e procede verso destra, riga per riga, fino all'angolo inferiore destro.

End Tile
: L'ultimo tassello dell'animazione.

Playback
: Specifica come riprodurre l'animazione:

  - `None` non riproduce l'animazione: viene visualizzata la prima immagine.
  - `Once Forward` riproduce l'animazione una volta dalla prima all'ultima immagine.
  - `Once Backward` riproduce l'animazione una volta dall'ultima alla prima immagine.
  - `Once Ping Pong` riproduce l'animazione una volta dalla prima all'ultima immagine e poi torna alla prima immagine.
  - `Loop Forward` riproduce l'animazione ripetutamente dalla prima all'ultima immagine.
  - `Loop Backward` riproduce l'animazione ripetutamente dall'ultima alla prima immagine.
  - `Loop Ping Pong` riproduce l'animazione ripetutamente dalla prima all'ultima immagine e poi torna alla prima immagine.

Fps
: La velocità di riproduzione dell'animazione, espressa in fotogrammi al secondo (FPS).

Flip horizontal
: Ribalta l'animazione in orizzontale.

Flip vertical
: Ribalta l'animazione in verticale.

## Forme di collisione delle sorgenti di tasselli {#tile-source-collision-shapes}

Defold utilizza un'immagine specificata nella proprietà *Collision* per generare una forma _convessa_ per ogni tassello. La forma delimita la parte del tassello che contiene informazioni di colore, cioè che non è trasparente al 100%.

Spesso è sensato utilizzare per le collisioni la stessa immagine che contiene la grafica vera e propria, ma puoi specificare un'immagine separata se desideri forme di collisione diverse dall'aspetto visivo. Quando specifichi un'immagine per le collisioni, l'anteprima viene aggiornata con un contorno su ogni tassello che indica le forme di collisione generate.

La vista *Outline* della sorgente di tasselli elenca i gruppi di collisione che hai aggiunto alla sorgente. Ai nuovi file sorgente di tasselli viene aggiunto un gruppo di collisione "default". Puoi aggiungere nuovi gruppi <kbd>facendo clic con il pulsante destro</kbd> sulla radice della sorgente di tasselli nella vista *Outline* e selezionando <kbd>Add ▸ Collision Group</kbd>.

Per selezionare le forme dei tasselli che devono appartenere a un determinato gruppo, seleziona il gruppo nella vista *Outline*, quindi fai clic su ogni tassello che desideri assegnare al gruppo. Il contorno del tassello e della forma assume il colore del gruppo. Il colore viene assegnato automaticamente al gruppo nell'editor.

![Forme di collisione](images/tilemap/collision.png)

Per rimuovere un tassello dal suo gruppo di collisione, seleziona l'elemento radice della sorgente di tasselli nella vista *Outline*, quindi fai clic sul tassello.
