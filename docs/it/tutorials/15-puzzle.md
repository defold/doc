---
title: Creare il gioco del 15 in Defold
brief: Se hai appena iniziato a usare Defold, questa guida ti aiuterà a sperimentare alcuni dei suoi elementi fondamentali e a eseguire la logica degli script.
---

# Il classico gioco del 15 {#the-classic-15-puzzle}

Questo noto rompicapo divenne popolare in America negli anni 1870. Lo scopo del gioco è riordinare le tessere sulla griglia facendole scorrere in orizzontale e in verticale. La partita inizia da una configurazione in cui le tessere sono state mescolate.

La versione più comune del gioco riporta sulle tessere i numeri da 1 a 15. Puoi però renderlo un po' più impegnativo usando tessere che compongono un'immagine. Prima di iniziare, prova a risolvere il rompicapo. Fai clic su una tessera adiacente alla casella vuota per farla scorrere nella posizione libera.

## Creazione del progetto {#creating-the-project}

1. Avvia Defold.
2. Seleziona *New Project* sulla sinistra.
3. Seleziona la scheda *From Template*.
4. Seleziona *Empty Project*
5. Scegli una posizione per il progetto sul disco locale.
6. Fai clic su *Create New Project*.

Apri il file delle impostazioni *game.project* e imposta le dimensioni del gioco a 512⨉512. Queste dimensioni corrisponderanno a quelle dell'immagine che utilizzerai.

![Impostazioni dello schermo](images/15-puzzle/display_settings.png)

Il passo successivo è scaricare un'immagine adatta al rompicapo. Scegli un'immagine quadrata e assicurati di ridimensionarla a 512 per 512 pixel. Se non vuoi cercarne una, eccone una pronta:

![Mona Lisa](images/15-puzzle/monalisa.png)

Scarica l'immagine, poi trascinala nella cartella *main* del progetto.

## Rappresentazione della griglia {#representing-the-grid}

Defold include un componente *Tilemap*, ideale per visualizzare la griglia del rompicapo. Le mappe di tessere consentono di impostare e leggere le singole tessere: è tutto ciò che serve per questo progetto.

Prima di creare la mappa di tessere, però, ti serve una *Tilesource* da cui la mappa ricaverà le immagini delle tessere.

<kbd>Fai clic con il pulsante destro</kbd> sulla cartella *main* e seleziona <kbd>New ▸ Tile Source</kbd>. Assegna al nuovo file il nome `monalisa.tilesource`.

Imposta le proprietà *Width* e *Height* delle tessere a 128. In questo modo l'immagine da 512⨉512 pixel verrà suddivisa in 16 tessere. Quando le inserirai nella mappa, le tessere saranno numerate da 1 a 16.

![Sorgente delle tessere](images/15-puzzle/tilesource.png)

Poi <kbd>fai clic con il pulsante destro</kbd> sulla cartella *main* e seleziona <kbd>New ▸ Tile Map</kbd>. Assegna al nuovo file il nome "grid.tilemap".

Defold richiede che la griglia venga inizializzata. Per farlo, seleziona il livello "layer1" e dipingi la griglia di tessere 4⨉4 subito in alto a destra rispetto all'origine. Non importa quali tessere scegli. Tra poco scriverai il codice che imposterà automaticamente il contenuto di queste tessere.

![Mappa di tessere](images/15-puzzle/tilemap.png)

## Mettere insieme i pezzi {#putting-the-pieces-together}

Apri *main.collection*. <kbd>Fai clic con il pulsante destro</kbd> sul nodo radice nella vista *Outline* e seleziona <kbd>Add Game Object</kbd>. Imposta la proprietà *Id* del nuovo oggetto di gioco (game object) a "game".

<kbd>Fai clic con il pulsante destro</kbd> sull'oggetto di gioco e seleziona <kbd>Add Component File</kbd>. Seleziona il file *grid.tilemap*. Imposta la proprietà *Id* a "tilemap".

<kbd>Fai clic con il pulsante destro</kbd> sull'oggetto di gioco e seleziona <kbd>Add Component ▸ Label</kbd>. Imposta la proprietà *Id* dell'etichetta a "done" e la proprietà *Text* a "Well done". Sposta l'etichetta al centro della mappa di tessere.

Imposta la posizione Z dell'etichetta a 1 per assicurarti che venga disegnata sopra la griglia.

![Collezione principale](images/15-puzzle/main_collection.png)

Ora crea un file di script Lua per la logica del rompicapo: <kbd>fai clic con il pulsante destro</kbd> sulla cartella *main* e seleziona <kbd>New ▸ Script</kbd>. Assegna al nuovo file il nome "game.script".

Poi <kbd>fai clic con il pulsante destro</kbd> sull'oggetto di gioco chiamato "game" in *main.collection* e seleziona <kbd>Add Component File</kbd>. Seleziona il file *game.script*.

Esegui il gioco. Dovresti vedere la griglia così come l'hai disegnata e, sopra di essa, l'etichetta con il messaggio "Well done".

## La logica del rompicapo {#the-puzzle-logic}

Ora tutti gli elementi sono al loro posto, quindi il resto del tutorial sarà dedicato a realizzare la logica del rompicapo.

Lo script manterrà una propria rappresentazione delle tessere della griglia, separata dalla mappa di tessere. Questo permette di semplificare le operazioni da eseguire su di esse. Anziché memorizzare le tessere in un array bidimensionale, le conserveremo come elenco monodimensionale in una tabella Lua. L'elenco contiene i numeri delle tessere in sequenza, dall'angolo superiore sinistro della griglia fino all'angolo inferiore destro:

```lua
-- The completed board looks like this:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

Il codice che prende un elenco di tessere di questo tipo e lo disegna sulla nostra mappa di tessere è piuttosto semplice, ma deve convertire la posizione nell'elenco in una posizione x e y:

```lua
-- Draw a table list of tiles onto a 4x4 tilemap
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. Nelle mappe di tessere, la tessera con valore x pari a 1 e valore y pari a 1 si trova in basso a sinistra. Occorre quindi invertire la posizione y.

Puoi verificare che la funzione si comporti come previsto creando una funzione `init()` di prova:

```lua
function init(self)
    -- An inverted board, for test
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Con le tessere in un elenco all'interno di una tabella Lua, mescolarne l'ordine è molto semplice. Il codice scorre tutti gli elementi dell'elenco e scambia ogni tessera con un'altra scelta a caso:

```lua
-- Swap two items in a table list
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomize the order of a the elements in a table list
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Prima di proseguire, c'è un aspetto del gioco del 15 che devi tenere presente: se disponi le tessere in ordine casuale come hai fatto sopra, c'è il 50% di probabilità che il rompicapo sia *impossibile* da risolvere.

Questo è un problema, perché di certo non vuoi proporre al giocatore un rompicapo senza soluzione.

Fortunatamente è possibile stabilire se una configurazione sia risolvibile o meno. Ecco come:

## Risolvibilità {#solvability}

Per stabilire se una configurazione di un rompicapo 4⨉4 sia risolvibile, servono due informazioni:

1. Il numero di "inversioni" nella configurazione. Si ha un'inversione quando una tessera precede un'altra tessera con un numero inferiore. Per esempio, l'elenco `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` presenta 3 inversioni:

    - il numero 12 è seguito da 11 e 10, dando luogo a 2 inversioni.
    - il numero 11 è seguito da 10, dando luogo a un'altra inversione.

    (Osserva che la configurazione del rompicapo risolto ha zero inversioni)

2. La riga in cui si trova la casella vuota (indicata con `0` nell'elenco).

Questi due numeri si possono calcolare con le seguenti funzioni:

```lua
-- Count the number of inversions in a list of tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Osserva che la casella vuota non viene conteggiata.

```lua
-- Find the x and y position of a given tile
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Posizione Y a partire dal basso.

Con questi due numeri è possibile stabilire se una configurazione del rompicapo sia risolvibile o meno. Una configurazione della griglia 4⨉4 è *risolvibile* se:

- La casella vuota si trova su una riga *dispari* (1 o 3 contando dal basso) e il numero di inversioni è *pari*.
- La casella vuota si trova su una riga *pari* (2 o 4 contando dal basso) e il numero di inversioni è *dispari*.

## Perché funziona? {#how-does-this-work}

Ogni mossa consentita sposta una tessera scambiandone la posizione con la casella vuota, in orizzontale o in verticale.

Spostare una tessera in orizzontale non cambia né il numero di inversioni né il numero della riga in cui si trova la casella vuota.

Spostare una tessera in verticale, invece, cambia la parità del numero di inversioni (da dispari a pari o da pari a dispari). Cambia anche la parità della riga della casella vuota.

Per esempio:

![Scorrimento di una tessera](images/15-puzzle/slide.png)

Questa mossa cambia l'ordine delle tessere da:

`{ ... 0, 11, 2, 13, 6 ... }`

a

`{ ... 6, 11, 2, 13, 0 ... }`

Il numero totale di inversioni diminuisce di 1, come segue:

- Il numero 6 aggiunge 1 inversione (il numero 2 si trova ora dopo il 6)
- Il numero 11 perde 1 inversione (il numero 6 si trova ora prima dell'11)
- Il numero 13 perde 1 inversione (il numero 6 si trova ora prima del 13)

Uno scorrimento verticale può cambiare il numero di inversioni di ±1 o ±3.

Uno scorrimento verticale può cambiare il numero della riga della casella vuota di ±1.

Nella configurazione finale del rompicapo, la casella vuota si trova nell'angolo inferiore destro (la riga 1, *dispari*) e il numero di inversioni è 0, un valore *pari*. Ogni mossa consentita lascia intatti questi due valori (spostamento orizzontale) oppure ne inverte la parità (spostamento verticale). Nessuna mossa consentita può mai rendere le parità del numero di inversioni e della riga della casella vuota rispettivamente *dispari*, *dispari* oppure *pari*, *pari*.

Qualsiasi configurazione del rompicapo in cui i due numeri sono entrambi dispari o entrambi pari è quindi impossibile da risolvere.

Ecco il codice che verifica la risolvibilità:

```lua
-- Is the given table list of 4x4 tiles solvable?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Input dell'utente {#user-input}

Ora rimane soltanto da rendere interattivo il rompicapo.

Crea una funzione `init()` che esegua tutta l'inizializzazione a runtime usando le funzioni create sopra:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Comunica al motore che questo oggetto di gioco deve ricevere input.
2. Imposta il seme del generatore di numeri casuali.
3. Crea una configurazione casuale iniziale della griglia.
4. Se la configurazione non è risolvibile, mescola di nuovo.
5. Disegna la griglia.
6. Imposta un indicatore di completamento per tenere traccia della vittoria.
7. Disabilita l'etichetta con il messaggio di completamento.

Apri */input/game.input_bindings* e aggiungi un nuovo *Mouse Trigger*. Imposta il nome dell'azione a "press":

![Input](images/15-puzzle/input.png)

Torna allo script e crea una funzione `on_input()`.

```lua
-- Deal with user input
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Se viene premuto un pulsante del mouse e la partita è ancora in corso, esegui le operazioni seguenti.
2. Calcola le coordinate x e y della casella su cui l'utente ha fatto clic.
3. Trova la posizione attuale della casella vuota (0).
4. Se la casella su cui è stato fatto clic si trova immediatamente sopra, sotto, a sinistra o a destra di quella vuota, esegui le operazioni seguenti:
5. Scambia le tessere nella casella su cui è stato fatto clic e in quella vuota.
6. Ridisegna la griglia aggiornata.
7. Se il numero di inversioni sulla griglia è 0, cioè tutto è nell'ordine corretto, e la casella vuota si trova nella colonna più a destra (deve trovarsi nell'ultima riga perché le inversioni siano 0), allora il rompicapo è risolto: esegui le operazioni seguenti:
8. Imposta l'indicatore di completamento.
9. Abilita/mostra il messaggio di completamento.

E questo è tutto! Hai finito: il gioco del 15 è completo!

## Lo script completo {#the-complete-script}

Ecco il codice completo dello script come riferimento:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Altri esercizi {#further-exercises}

1. Crea un rompicapo 5⨉5, poi uno 6⨉5. Assicurati che i controlli di risolvibilità funzionino in generale.
2. Aggiungi animazioni di scorrimento. Le tessere non possono essere spostate separatamente dalla mappa, quindi dovrai trovare una soluzione. Potresti usare una mappa di tessere separata che contenga soltanto la tessera che scorre?
