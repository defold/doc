---
title: Adattare la grafica a schermi di dimensioni diverse
brief: Questo manuale spiega come adattare il gioco e la grafica a schermi di dimensioni diverse.
---

# Introduzione {#introduction}

Ci sono diversi aspetti da considerare quando adatti il gioco e la grafica a schermi di dimensioni diverse:

* È un gioco rétro con grafica a bassa risoluzione e pixel perfettamente allineati oppure un gioco moderno con grafica di qualità HD?
* Come dovrebbe comportarsi il gioco quando viene eseguito a schermo intero su schermi di dimensioni diverse?
  * Su uno schermo ad alta risoluzione, il giocatore dovrebbe vedere una porzione maggiore del contenuto del gioco oppure la grafica dovrebbe regolare automaticamente lo zoom per mostrare sempre lo stesso contenuto?
* Come dovrebbe gestire il gioco i rapporti d'aspetto diversi da quello impostato in *game.project*?
  * Il giocatore dovrebbe vedere una porzione maggiore del contenuto del gioco? Oppure dovrebbero esserci delle bande nere? O magari degli elementi GUI ridimensionati?
* Di quali menu e componenti GUI a schermo hai bisogno e come dovrebbero adattarsi a schermi di dimensioni e orientamenti diversi?
  * I menu e gli altri componenti GUI dovrebbero cambiare layout quando cambia l'orientamento oppure dovrebbero mantenere lo stesso layout indipendentemente dall'orientamento?

Questo manuale affronta alcuni di questi aspetti e suggerisce le pratiche consigliate.


## Modificare il modo in cui viene visualizzato il contenuto {#how-to-change-how-your-content-is-rendered}

Lo script di rendering di Defold ti dà il pieno controllo dell'intera pipeline di rendering. Lo script di rendering decide sia l'ordine sia che cosa disegnare e come. Il comportamento predefinito dello script di rendering è disegnare sempre la stessa area di pixel, definita dalla larghezza e dall'altezza nel file *game.project*, anche se la finestra viene ridimensionata o la risoluzione effettiva dello schermo non corrisponde. Di conseguenza, il contenuto viene deformato se cambia il rapporto d'aspetto e ingrandito o rimpicciolito se cambiano le dimensioni della finestra. In alcuni giochi questo comportamento può essere accettabile, ma è più probabile che tu voglia mostrare una porzione maggiore o minore del contenuto del gioco se la risoluzione dello schermo o il rapporto d'aspetto sono diversi, o almeno assicurarti di ingrandire e rimpicciolire il contenuto senza modificarne il rapporto d'aspetto. Puoi modificare facilmente questo comportamento predefinito di deformazione; per sapere come farlo, consulta il [manuale del rendering](https://www.defold.com/manuals/render/#default-view-projection).


## Grafica rétro/a 8 bit {#retro8-bit-graphics}

Con grafica rétro/a 8 bit si indicano spesso i giochi che riproducono lo stile grafico delle vecchie console o dei vecchi computer, con la loro bassa risoluzione e la tavolozza di colori limitata. Per esempio, il Nintendo Entertainment System (NES) aveva una risoluzione dello schermo di 256x240, il Commodore 64 di 320x200 e il Gameboy di 160x144: tutte queste risoluzioni rappresentano soltanto una frazione delle dimensioni degli schermi moderni. Per rendere giocabili su un moderno schermo ad alta risoluzione i giochi che riproducono questo stile grafico e queste risoluzioni, occorre ingrandire la grafica di diverse volte. Un modo semplice per farlo consiste nel disegnare tutta la grafica alla bassa risoluzione e nello stile che desideri riprodurre, per poi ingrandirla durante il rendering. In Defold puoi ottenere facilmente questo risultato usando lo script di rendering e la [proiezione fissa](/manuals/render/#fixed-projection) impostata su un valore di zoom adatto.

Prendiamo questo insieme di tessere e il personaggio del giocatore ([fonte](https://ansimuz.itch.io/grotto-escape-game-art-pack)) e usiamoli per un gioco rétro a 8 bit con una risoluzione di 320x200:

![](images/screen_size/retro-player.png)

![](images/screen_size/retro-tiles.png)

Impostando 320x200 nel file *game.project* e avviando il gioco, il risultato sarebbe questo:

![](images/screen_size/retro-original_320x200.png)

La finestra è davvero minuscola su un moderno schermo ad alta risoluzione! Aumentando di quattro volte le dimensioni della finestra, fino a 1280x800, diventa più adatta a uno schermo moderno:

![](images/screen_size/retro-original_1280x800.png)

Ora che la finestra ha dimensioni più ragionevoli, dobbiamo intervenire anche sulla grafica. È così piccola che risulta molto difficile vedere che cosa sta succedendo nel gioco. Possiamo usare lo script di rendering per impostare una proiezione fissa con uno zoom:

```Lua
msg.post("@render:", "use_fixed_projection", { zoom = 4 })
```

::: sidenote
Puoi ottenere lo stesso risultato aggiungendo un [componente telecamera](/manuals/camera/) a un oggetto di gioco, selezionando *Orthographic Projection* e impostando *Orthographic Zoom* su 4.0:

![](images/screen_size/retro-camera_zoom.png)
:::

Questo produce il seguente risultato:

![](images/screen_size/retro-zoomed_1280x800.png)

Così va meglio. La finestra e la grafica hanno entrambe dimensioni adeguate, ma osservando più da vicino si nota un problema evidente:

![](images/screen_size/retro-zoomed_linear.png)

La grafica appare sfocata! Questo dipende dal modo in cui la grafica ingrandita viene campionata dalla texture durante il rendering da parte della GPU. L'impostazione predefinita nel file *game.project*, nella sezione *Graphics*, è *linear*:

![](images/screen_size/retro-settings_linear.png)

Impostandola su *nearest* otteniamo il risultato desiderato:

![](images/screen_size/retro-settings_nearest.png)

![](images/screen_size/retro-zoomed_nearest.png)

Ora abbiamo una grafica nitida, con *pixel perfettamente allineati*, per il nostro gioco rétro. Ci sono altri aspetti da considerare, come la disattivazione dei subpixel per gli sprite in *game.project*:

![](images/screen_size/retro-subpixels.png)

Quando l'opzione *Subpixels* è disattivata, gli sprite non vengono mai disegnati su mezzi pixel, ma si allineano sempre al pixel intero più vicino.

## Grafica ad alta risoluzione {#high-resolution-graphics}

Quando lavoriamo con grafica ad alta risoluzione, dobbiamo impostare il progetto e i contenuti in modo diverso rispetto alla grafica rétro/a 8 bit. Con la grafica bitmap, devi creare i contenuti in modo che abbiano un buon aspetto su uno schermo ad alta risoluzione quando vengono visualizzati in scala 1:1.

Come per la grafica rétro/a 8 bit, devi modificare lo script di rendering. In questo caso, la grafica deve ridimensionarsi in base alle dimensioni dello schermo mantenendo il rapporto d'aspetto originale:

```Lua
msg.post("@render:", "use_fixed_fit_projection")
```

In questo modo, la visualizzazione si ridimensiona per mostrare sempre la stessa quantità di contenuto specificata nel file *game.project*, eventualmente mostrando contenuto aggiuntivo sopra e sotto o ai lati, a seconda che il rapporto d'aspetto sia diverso o meno.

Devi impostare la larghezza e l'altezza nel file *game.project* su dimensioni che consentano di mostrare il contenuto del gioco senza ridimensionarlo.

### Impostazione per DPI elevati e schermi Retina {#high-dpi-setting-and-retina-screens}

Se desideri supportare anche gli schermi Retina ad alta risoluzione, puoi abilitare questa opzione nella sezione Display del file *game.project*:

![](images/screen_size/highdpi-enabled.png)

Questo crea un back buffer ad alta densità di pixel sugli schermi che lo supportano. Il gioco viene disegnato a una risoluzione doppia rispetto a quella definita nelle impostazioni Width e Height, che rimane comunque la risoluzione logica usata negli script e nelle proprietà. Ciò significa che tutte le misure restano invariate e che i contenuti disegnati in scala 1x mantengono lo stesso aspetto. Se però importi immagini ad alta risoluzione e le ridimensioni a 0.5x, verranno visualizzate sullo schermo con una densità di pixel elevata.


## Creare una GUI adattiva {#creating-an-adaptive-gui}

Il sistema per creare componenti GUI si basa su un insieme di elementi fondamentali, o [nodi](/manuals/gui/#node-types), e, anche se può sembrare troppo semplice, permette di creare qualsiasi cosa, dai pulsanti ai menu complessi e alle finestre popup. Le GUI che crei possono essere configurate per adattarsi automaticamente ai cambiamenti delle dimensioni e dell'orientamento dello schermo. Puoi, per esempio, mantenere i *nodi* ancorati alla parte superiore, inferiore o ai lati dello schermo; i nodi possono conservare le proprie dimensioni oppure estendersi. Puoi anche configurare le relazioni tra i *nodi*, le loro dimensioni e il loro aspetto in modo che cambino al variare delle dimensioni o dell'orientamento dello schermo.

### Proprietà dei *nodi* {#node-properties}

Ogni *nodo* di una GUI ha un punto di pivot, un ancoraggio orizzontale e verticale e una modalità di adattamento.

* Il punto di pivot definisce il punto centrale di un nodo.
* La modalità di ancoraggio controlla come viene modificata la posizione verticale e orizzontale del nodo quando i limiti della scena, o quelli del nodo genitore, vengono estesi per adattarsi alle dimensioni fisiche dello schermo.
* L'impostazione della modalità di adattamento controlla che cosa accade a un nodo quando i limiti della scena, o quelli del nodo genitore, vengono adattati alle dimensioni fisiche dello schermo.

Puoi approfondire queste proprietà [nel manuale della GUI](/manuals/gui/#node-properties).

### Layout {#layouts}

Defold supporta GUI che si adattano automaticamente ai cambiamenti di orientamento dello schermo sui dispositivi mobili. Con questa funzionalità puoi progettare una GUI capace di adattarsi all'orientamento e al rapporto d'aspetto di schermi di varie dimensioni. Puoi anche creare layout corrispondenti a modelli di dispositivo specifici. Per approfondire questo sistema, consulta il [manuale dei layout della GUI](/manuals/gui-layouts/)


## Provare schermi di dimensioni diverse {#testing-different-screen-sizes}

Il menu *Debug* contiene un'opzione per simulare la risoluzione di uno specifico modello di dispositivo oppure una risoluzione personalizzata. Mentre l'applicazione è in esecuzione, puoi selezionare <kbd>Debug->Simulate Resolution</kbd> e scegliere uno dei modelli di dispositivo dall'elenco. La finestra dell'applicazione in esecuzione verrà ridimensionata e potrai vedere come appare il gioco a una risoluzione diversa o con un rapporto d'aspetto diverso.

![](images/screen_size/simulate-resolution.png)
