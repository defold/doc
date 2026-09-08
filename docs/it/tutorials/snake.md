---
brief: Se non conosci ancora Defold, questa guida ti aiuterà a muovere i primi passi con la logica degli script e con alcuni degli elementi fondamentali di Defold, per creare da zero un clone di Snake.
layout: tutorial
title: Creare un gioco Snake in Defold
difficulty: Beginner
---

# Snake

Questo tutorial ti accompagna nella creazione di uno dei giochi classici più comuni che puoi provare a ricreare. Esistono molte varianti di questo gioco; in questa, un serpente mangia del "cibo" e cresce soltanto quando mangia. Il serpente si muove inoltre su un campo di gioco che contiene ostacoli.

![anteprima](images/snake/thumbnail.png)

### Che cosa imparerai {#what-youll-learn}

In questo tutorial imparerai a:
- Creare un gioco da zero in Defold
- Configurare e gestire gli input
- Creare mappe di tile e modificarle durante l'esecuzione
- Scrivere script in Lua

### Una nota per chi inizia {#a-note-for-beginners}

Questo tutorial è pensato per i principianti, ma se non hai mai usato Defold e non hai esperienza nello sviluppo di giochi, ti consigliamo di leggere prima alcuni manuali introduttivi, in particolare quelli sugli [elementi fondamentali di Defold](/manuals/building-blocks/) e il [glossario](/manuals/glossary/). Se non hai ancora scaricato Defold, consulta il [manuale di installazione](/manuals/install/). Ti consigliamo anche di consultare la [panoramica dell'editor](/manuals/editor/) per familiarizzare rapidamente con l'editor stesso; qui, comunque, trovi schermate per ogni passaggio.

## Creare il progetto {#creating-the-project}

Avvia Defold e:

1. Seleziona *Create From* ▸ *Templates* sul lato sinistro.
2. Seleziona *Empty Project*.
3. Digita un nome per il progetto nel campo *Title*.
4. Seleziona una posizione per il progetto in *Location*.
5. Fai clic su *Create New Project*.

![avvio](images/snake/1.png)

<input type="checkbox"/> Fatto!

## Impostazioni del progetto {#project-settings}

Iniziamo definendo la risoluzione del gioco.

1. Una volta aperto l'editor, cerca il file `game.project` sul lato sinistro, nel pannello *Assets*. Fai doppio clic sul file per aprirlo.
2. Vai alla sezione *Display* del file `game.project`.
3. Imposta le dimensioni del gioco (`Width` e `Height`) a 768⨉768 o a un altro multiplo di 16.

![schermo](images/snake/2.png)

Questo passaggio serve perché il gioco verrà disegnato su una griglia in cui ogni segmento misura 16x16 pixel: in questo modo, i bordi dello schermo di gioco non taglieranno alcun segmento. Il file `game.project` contiene tutte le impostazioni importanti del progetto; puoi scoprirle nel [manuale delle impostazioni del progetto](/manuals/project-settings/).

<input type="checkbox"/> Fatto!

## Creare nuove cartelle nel pannello Assets {#creating-new-folders-in-the-assets-pane}

Per un clone minimalista di Snake servono pochissimi elementi grafici: un segmento verde di 16⨉16 pixel per il serpente, un blocco bianco per gli ostacoli e un blocco rosso più piccolo che rappresenta il cibo.

Per prima cosa, crea una directory per gli asset nell'editor Defold:

1. <kbd>Fai clic con il tasto destro</kbd> sulla cartella `main`
2. Seleziona `New Folder`.
3. Apparirà una finestra che chiede un nome: digita `assets` e fai clic su `Create Folder`.

![nuova cartella](images/snake/3.png)

<input type="checkbox"/> Fatto!

## Aggiungere la grafica al gioco {#adding-graphics-to-the-game}

L'immagine qui sotto è l'unico asset di cui hai bisogno:

![sprite del serpente](images/snake/snake.png)

1. <kbd>Fai clic con il tasto destro</kbd> sull'immagine qui sopra e salvala sul disco locale. Poi trascina (o copia e incolla) l'immagine scaricata nella nuova posizione che hai appena creato nella cartella del progetto.

![nuova cartella](images/snake/4.png)

Puoi anche trovare maggiori dettagli sull'[importazione degli asset qui](/manuals/importing-graphics/).

<input type="checkbox"/> Fatto!

## Aggiungere una sorgente di tile {#adding-a-tile-source}

Defold offre un componente [mappa di tile (Tile Map)](/manuals/tilemap/) integrato, che userai per creare il campo di gioco composto da *tile* allineati su una griglia. Una mappa di tile consente di impostare e leggere singoli tile, ed è quindi perfetta per questo gioco. Poiché le mappe di tile ricavano la propria grafica da una [sorgente di tile (Tile Source)](/manuals/tilesource/), devi crearne una:

1. <kbd>Fai clic con il tasto destro</kbd> sulla cartella `assets`.
2. Seleziona `New` ▸ `Tile Source` nella sezione "Resources".
3. Assegna al nuovo file il nome "snake" (l'editor lo salverà come `snake.tilesource`).

![nuova sorgente di tile](images/snake/5.png)

La sorgente di tile si aprirà nell'editor dedicato a questo tipo di file e ti verrà chiesto di assegnarle un'immagine affinché possa funzionare. Sul lato destro trovi il pannello `Properties`:

4. Imposta la proprietà `Image` sul file grafico che hai appena importato.
![sorgente di tile](images/snake/6.png)

5. Le proprietà `Width` e `Height` devono rimanere impostate a 16 (valore predefinito). In questo modo l'immagine di 32⨉32 pixel verrà suddivisa in 4 tile, numerati da 1 a 4.

![proprietà della sorgente di tile](images/snake/7.png)

Nota che la proprietà *Extrude Borders* è impostata a 2 pixel. Questo serve a evitare artefatti visivi attorno ai tile la cui grafica si estende fino al bordo.

Se modifichi un file, nella sua scheda appare un asterisco `*` accanto al nome. Seleziona `File` ▸ `Save All` oppure usa la scorciatoia <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> su Mac) per salvare tutti i file.

<input type="checkbox"/> Fatto!

## Creare la mappa di tile del campo di gioco {#creating-the-playfield-tile-map}

Ora hai una sorgente di tile pronta all'uso: è il momento di creare il componente mappa di tile del campo di gioco:

1. <kbd>Fai clic con il tasto destro</kbd> sulla cartella `main` e seleziona <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> nella sezione "Components". Assegna al nuovo file il nome "grid" (l'editor lo salverà come "grid.tilemap").
![aggiungere una mappa di tile](images/snake/8.png)

2. Il file si aprirà nell'editor delle mappe di tile, che segnalerà la necessità di una **Tile Source**: imposta quindi la proprietà *Tile Source* su "snake.tilesource", creata in precedenza.
![impostare la sorgente di tile](images/snake/9.png)

<input type="checkbox"/> Fatto!

## Disegnare i tile nella mappa {#drawing-tiles-in-the-tile-map}

Defold memorizza soltanto l'area della mappa di tile effettivamente utilizzata, quindi devi aggiungere abbastanza tile da riempire lo schermo fino ai bordi.

1. Seleziona il livello `layer1` nel pannello `Outline` sul lato destro.
2. Scegli l'opzione di menu `Edit` ▸ `Select Tile...` oppure la scorciatoia <kbd>Space</kbd> per mostrare la tavolozza dei tile, poi fai clic sul tile che vuoi usare per disegnare.
![mappa di tile](images/snake/10.png)

3. Disegna una cornice lungo il bordo dello schermo e alcuni ostacoli.
![mappa di tile completata](images/snake/11.png)

Per riempire lo schermo del gioco, ti servirà una mappa di 48x48 tile (perché lo schermo misura 768 pixel e i tile sono di 16 pixel, quindi 768/16 = 48).

Salva la mappa di tile quando hai finito.

<input type="checkbox"/> Fatto!

## Aggiungere la mappa di tile al gioco {#adding-the-tile-map-to-the-game}

Ora dobbiamo aggiungere la mappa di tile al gioco. Se conosci gli elementi fondamentali di Defold, sai che i componenti fanno parte degli oggetti di gioco (game object) e che gli oggetti di gioco possono essere definiti nelle collezioni (collection).

1. Apri `main.collection` facendo doppio clic sul file nel pannello `Assets`. Nel modello Empty Project, questa è per impostazione predefinita la collezione di bootstrap caricata all'avvio del motore.

2. <kbd>Fai clic con il tasto destro</kbd> sulla radice in `Outline` e seleziona `Add Game Object`: questo crea un nuovo oggetto di gioco nella collezione caricata all'avvio del gioco.
![aggiungere un oggetto di gioco](images/snake/12.png)

3. <kbd>Fai clic con il tasto destro</kbd> sul nuovo oggetto di gioco e seleziona `Add Component File`. Scegli il file "grid.tilemap" che hai appena creato.
![aggiungere un componente](images/snake/13.png)

Ora abbiamo una mappa di tile nella collezione del gioco. Dovrebbe essere visibile quando avvii il gioco dall'editor.

1. Seleziona `Project` ▸ `Build` oppure usa la scorciatoia <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> su Mac).

![avviare il gioco](images/snake/14.png)

<input type="checkbox"/> Fatto!

## Aggiungere uno script al gioco {#adding-a-script-to-the-game}

1. <kbd>Fai clic con il tasto destro</kbd> sulla cartella `main` nel pannello `Assets` e seleziona `New` ▸ `Script` nella sezione Scripts. Assegna al nuovo file script il nome "snake" (verrà salvato come "snake.script"). Questo file conterrà tutta la logica del gioco.
![aggiungere uno script](images/snake/15.png)

2. Torna a *main.collection* e <kbd>fai clic con il tasto destro</kbd> sull'oggetto di gioco che contiene la mappa di tile. Seleziona <kbd>Add&nbsp;Component&nbsp;File</kbd> e scegli il file "snake.script".

![collezione principale](images/snake/16.png)

Ora il componente mappa di tile e lo script sono al loro posto.

<input type="checkbox"/> Fatto!

## Lo script del gioco {#the-game-script}

Lo script che scriverai gestirà l'intero gioco. Aggiungeremo le funzionalità una alla volta.

### Un semplice algoritmo di movimento {#simple-movement-algorithm}

L'idea di funzionamento è la seguente:

1. Lo script mantiene un elenco delle posizioni dei tile attualmente occupati dal serpente.
2. Se il giocatore preme un tasto direzionale, memorizza la direzione in cui il serpente deve muoversi.
3. A intervalli regolari, sposta il serpente di un passo nella direzione di movimento corrente.

### Inizializzazione {#initialization}

Apri *snake.script* e individua la funzione `init()`. Il motore chiama questa funzione quando lo script viene inizializzato all'avvio del gioco. Sostituisci il codice con il seguente:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

In questo codice:

1. Memorizziamo i segmenti del serpente in una tabella Lua chiamata `self.segments`, che contiene un elenco di tabelle, ciascuna con una posizione X e Y per un segmento.
2. Memorizziamo la direzione corrente in una tabella chiamata `self.dir`, che contiene una direzione X e Y.
3. Memorizziamo la velocità di movimento corrente in `self.speed`, espressa in tile al secondo.
4. Memorizziamo in `self.time` il valore di un timer che verrà usato per gestire la velocità di movimento.

Il codice dello script qui sopra è scritto in Lua. Ci sono alcuni aspetti da osservare, ma se non capisci ancora qualcuno dei punti seguenti, non preoccuparti. Continua a seguire il tutorial, sperimenta e prenditi il tempo necessario: con la pratica li capirai. Per ora, ricorda soltanto che in `init()` abbiamo inizializzato le variabili che useremo.

- Defold riserva una serie di *funzioni* di callback integrate che vengono chiamate durante il ciclo di vita di un componente script. *Non* sono metodi, ma semplici funzioni.
- Il runtime passa un riferimento all'istanza corrente del componente script attraverso il parametro `self`. Il riferimento `self` viene usato per memorizzare i dati dell'istanza.
- Il riferimento `self` può essere usato come una tabella Lua in cui memorizzare dati. Basta usare la notazione con il punto come per qualsiasi altra tabella: `self.data = "value"`. Il riferimento è valido per l'intero ciclo di vita dello script, in questo caso dall'avvio del gioco fino alla sua chiusura.
- I letterali delle tabelle Lua si scrivono tra parentesi graffe `{}`.
- Gli elementi di una tabella possono essere coppie chiave/valore (`{x = 10, y = 20}`), tabelle Lua annidate (`{ {a = 1}, {b = 2} }`) o altri tipi di dati.

<input type="checkbox"/> Fatto!

### Aggiornamento {#update}

La funzione `init()` viene chiamata esattamente una volta, quando il componente script viene istanziato nel gioco in esecuzione. La funzione `update()`, invece, viene chiamata una volta **a ogni fotogramma**. Questo la rende ideale per la logica di gioco in tempo reale.

L'idea per l'aggiornamento è questa: a intervalli prestabiliti, esegui le seguenti operazioni:

1. Trova la posizione della testa del serpente, poi crea una nuova testa nella posizione adiacente, spostata nella direzione di movimento corrente. Quindi, se il serpente si muove di X=1 e Y=0 e la testa attuale si trova in X=0 e Y=0, la nuova testa dovrà trovarsi in X=1 e Y=0.
2. Salva la posizione della nuova testa nell'elenco dei segmenti che costituiscono il serpente.
3. Recupera la posizione della coda dalla tabella dei segmenti.
4. Cancella il tile della coda in questa posizione.
5. Disegna tutti i segmenti del serpente (tile) nelle posizioni indicate dalla tabella.

![algoritmo](images/snake/17.png)

:::sidenote
Ricorda che la testa del nostro serpente si trova alla fine della tabella, mentre la coda si trova all'inizio.
:::

1. Individua la funzione `update()` in *snake.script* e sostituisci il codice con il seguente:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

In questo codice:

1. Incrementiamo il timer della differenza di tempo (in secondi) trascorsa dall'ultima chiamata a `update()`, il cosiddetto "delta time", o `dt`.
2. Se il timer è avanzato abbastanza:
3. Recuperiamo la posizione della testa corrente. `#` è l'operatore usato per ottenere la lunghezza di una tabella, purché sia usata come array, proprio come in questo caso: tutti i segmenti sono valori della tabella senza una chiave specificata.
4. Creiamo un nuovo segmento di testa in base alla posizione della testa corrente e alla direzione di movimento (`self.dir`).
5. Aggiungiamo la nuova testa alla fine della tabella dei segmenti.
6. Rimuoviamo la coda dall'inizio della tabella dei segmenti.
7. Cancelliamo il tile nella posizione della coda rimossa. La nostra mappa di tile `#grid` ha un solo livello, chiamato `layer1`.
8. Scorriamo gli elementi della tabella dei segmenti. A ogni iterazione, `i` contiene la posizione nella tabella (a partire da 1) e `s` contiene il segmento corrente.
9. Impostiamo il tile nella posizione del segmento al valore 2 (che corrisponde al tile con il colore verde del serpente).
10. Al termine, azzeriamo il timer.

Se avvii il gioco ora, dovresti vedere il serpente, lungo 4 segmenti, spostarsi da sinistra a destra sul campo di gioco.

![avviare il gioco](images/snake/snake_run_1.png)

<input type="checkbox"/> Fatto!

## Input del giocatore {#player-input}

Prima di aggiungere il codice che reagisce all'input del giocatore, devi configurare le associazioni di input.

### Binding di input {#input-bindings}

1. Nella cartella `input`, trova il file `game.input_binding` e <kbd>fai doppio clic</kbd> per aprirlo.
2. Aggiungi una serie di binding *Key Trigger* per il movimento verso l'alto, il basso, sinistra e destra. Nella colonna *Input* seleziona i tasti della tastiera e nelle colonne *Action* digita i nomi delle azioni.

![associazioni di input](images/snake/18.png)

Il file dei binding di input associa gli input effettivi dell'utente (tasti, movimenti del mouse e così via) ai *nomi* delle azioni che vengono passati agli script che hanno richiesto di ricevere input.

<input type="checkbox"/> Fatto!

### Acquisire il focus dell'input {#acquiring-input-focus}

Una volta configurati i binding, apri *snake.script* e aggiungi la seguente riga all'inizio della funzione `init()`:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

La riga aggiunta:
1. Invia un messaggio all'oggetto di gioco corrente ("." è un'abbreviazione per indicare l'oggetto di gioco corrente), chiedendogli di iniziare a ricevere input dal motore.

Poi individua la funzione `on_input` e digita il seguente codice:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Questi rami `if...elseif...` eseguono le seguenti operazioni:
1. Se viene ricevuta l'azione di input "up", come configurato nei binding di input, e nella tabella `action` il campo `pressed` è impostato a `true` (il giocatore ha premuto il tasto), allora:
2. Impostano la direzione di movimento.

Avvia di nuovo il gioco e verifica di riuscire a guidare il serpente.

<input type="checkbox"/> Fatto!

### Migliorare la gestione dell'input {#improving-input-handling}

Ora nota che, se premi due tasti contemporaneamente, vengono effettuate due chiamate a `on_input()`, una per ogni pressione. Con il codice scritto sopra, soltanto l'ultima chiamata ha effetto sulla direzione del serpente, poiché le chiamate successive a `on_input()` sovrascrivono i valori in `self.dir`.

Nota anche che, se il serpente si muove verso sinistra e premi il tasto <kbd>right</kbd>, il serpente andrà contro sé stesso. La soluzione *apparentemente* ovvia a questo problema è aggiungere un'ulteriore condizione alle clausole `if` in `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Tuttavia, se il serpente si muove verso sinistra e il giocatore preme *rapidamente* prima <kbd>up</kbd>, poi <kbd>right</kbd>, prima che avvenga il passo di movimento successivo, soltanto la pressione di <kbd>right</kbd> avrà effetto e il serpente andrà contro sé stesso. Con le condizioni aggiunte alle clausole `if` mostrate sopra, l'input verrà ignorato. *Non va bene!*

Una soluzione corretta a questo problema consiste nel memorizzare gli input in una coda e nell'estrarli man mano che il serpente si muove:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Questa volta:
1. Abbiamo aggiunto una variabile `self.dirqueue`, inizializzata come tabella vuota.

Nella funzione `update()` aggiungi:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Estrai il primo elemento dalla coda delle direzioni.
2. Se c'è un elemento (`newdir` non è nullo), controlla se `newdir` punta nella direzione opposta a `self.dir`.
3. Imposta la nuova direzione soltanto se non è opposta a quella corrente.

Modifica inoltre `on_input` affinché memorizzi l'input corrente nella coda:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Aggiungi la direzione dell'input alla coda delle direzioni, invece di impostare direttamente `self.dir`.

Avvia il gioco e verifica che funzioni come previsto.

<input type="checkbox"/> Fatto!

## Cibo e collisioni con gli ostacoli {#food-and-collision-with-obstacles}

Il serpente ha bisogno di cibo sulla mappa per diventare più lungo e più veloce. Aggiungiamolo!

### Generare il cibo {#spawning-the-food}

Sopra la funzione `init()`, aggiungi una nuova funzione:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

In questa funzione:
1. Dichiariamo una nuova funzione chiamata `put_food()` che posiziona un pezzo di cibo sulla mappa.
2. Memorizziamo una posizione X e Y casuale in una variabile chiamata `self.food`.
3. Impostiamo il tile nella posizione X e Y al valore 3, che corrisponde alla grafica del cibo.

Poi chiamala alla fine della funzione `init()`:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Prima di iniziare a ottenere valori casuali con `math.random()`, imposta il seme del generatore casuale; altrimenti verrà generata sempre la stessa sequenza di valori. Questo seme va impostato una sola volta.
2. Chiama la funzione `put_food()` all'avvio del gioco, in modo che il giocatore inizi con un pezzo di cibo sulla mappa.

<input type="checkbox"/> Fatto!

### Mangiare il cibo {#eating-the-food}

Ora, per rilevare se il serpente ha urtato qualcosa, basta controllare che cosa si trova sulla mappa di tile nella direzione in cui si sta muovendo e reagire di conseguenza.

Aggiungi una variabile che tenga traccia del fatto che il serpente sia vivo o meno:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Un flag che indica se il serpente è vivo o meno.

Poi aggiungi la logica che verifica le collisioni con pareti, ostacoli e cibo:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Fai avanzare il serpente soltanto se è vivo.
2. Prima di disegnare sulla mappa di tile, leggi che cosa si trova nella posizione che occuperà la nuova testa del serpente.
3. Se il tile è un ostacolo o un'altra parte del serpente, la partita è finita!
4. Se il tile è cibo, aumenta la velocità, poi posiziona un nuovo pezzo di cibo.
5. Nota che la coda viene rimossa soltanto se non c'è una collisione. Questo significa che, se il giocatore mangia il cibo, il serpente cresce di un segmento, perché in quel movimento la coda non viene rimossa.

Ora prova il gioco e assicurati che funzioni bene!

Il tutorial termina qui, ma continua a sperimentare con il gioco e prova a svolgere alcuni degli esercizi qui sotto!

<input type="checkbox"/> Fatto!

## Lo script completo {#the-complete-script}

Ecco il codice completo dello script come riferimento:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Esercizi {#exercises}

Per esercitarti, prova a implementare questi miglioramenti:

1. Aggiungi la gestione di un tasto per riavviare il gioco quando la partita è finita.
2. Aggiungi l'assegnazione dei punti e un contatore del punteggio, usando un semplice componente etichetta (più facile) oppure un'intera GUI.
3. La funzione put_food() non tiene conto della posizione del serpente o degli ostacoli. Correggila in modo che generi il cibo soltanto nelle posizioni libere.
4. Quando la partita è finita, mostra un messaggio “Game Over” e consenti al giocatore di riprovare.
5. Per una sfida in più: aggiungi un secondo serpente controllato da un giocatore.
