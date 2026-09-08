---
title: Tutorial di Magic Link
brief: In questo tutorial realizzerai un piccolo rompicapo completo, con una schermata iniziale, le meccaniche di gioco e una semplice progressione tra i livelli basata sull'aumento della difficoltà.
---

# Tutorial di Magic Link {#magic-link-tutorial}

Questo gioco è una variante del classico gioco di abbinamenti sulla scia di _Bejeweled_ e _Candy Crush_. Il giocatore trascina e collega blocchi dello stesso colore per rimuoverli, ma l'obiettivo del gioco non è eliminare lunghe serie di blocchi dello stesso colore, svuotare il tabellone o raccogliere punti, bensì collegare tra loro una serie di speciali "blocchi magici" sparsi sul tabellone.

Questo tutorial è una guida passo dopo passo in cui realizziamo il gioco partendo da un progetto già definito. Nella realtà, trovare un'impostazione che funzioni richiede molto tempo e impegno. Potresti partire da un'idea di base e poi trovare un modo per realizzarne un prototipo, così da capire meglio quali possibilità offre. Anche un gioco semplice come "Magic Link" richiede un lavoro di progettazione considerevole. Questo gioco ha attraversato alcune iterazioni e sperimentazioni prima di raggiungere la forma e le regole definitive, ancora ben lontane dalla perfezione. Per questo tutorial, però, salteremo quel processo e inizieremo a costruire il gioco sulla base del progetto definitivo.

## Primi passi {#getting-started}

Per iniziare, devi creare un nuovo progetto e importare il pacchetto di asset:

* Crea un [nuovo progetto](/manuals/project-setup/#creating-a-new-project) dal modello "Empty Project"
* Scarica il progetto completo di "Magic Link", [magic-link.zip](https://github.com/defold/defold-examples/releases/latest), come riferimento. Il progetto completo contiene tutti gli asset, nel caso tu voglia creare il progetto da zero.

## Regole del gioco {#game-rules}

![Schema delle regole del gioco](images/magic-link/linker_rules.png)

A ogni turno il tabellone viene riempito casualmente con blocchi colorati e una serie di blocchi magici. I blocchi colorati seguono queste regole:

* Scompaiono se il giocatore li collega, trascinando, ad altri blocchi dello stesso colore.
* Quando i blocchi scompaiono, lasciano spazi vuoti sotto quelli rimasti. I blocchi colorati cadono semplicemente in verticale negli spazi che si sono aperti sotto di loro.
* Il bordo inferiore dello schermo impedisce a tutti i blocchi di cadere oltre.

I blocchi magici si comportano diversamente, secondo queste regole:

* I blocchi magici si spostano _lateralmente_ se si apre uno spazio su uno dei due lati.
* Se invece si apre uno spazio sotto di loro, cadono come i normali blocchi colorati.

Il giocatore interagisce con il gioco secondo le seguenti regole:

* Il giocatore può trascinare e collegare blocchi colorati adiacenti in orizzontale, in verticale e in diagonale.
* I blocchi collegati scompaiono non appena il giocatore interrompe il tocco, sollevando il dito.
* I blocchi magici non reagiscono al trascinamento e non possono essere collegati manualmente.
* I blocchi magici, però, reagiscono quando sono adiacenti in orizzontale o in verticale: in queste circostanze si collegano automaticamente.
* Il livello è completato se il giocatore riesce a far collegare automaticamente tutti i blocchi magici sul tabellone.

Il livello di difficoltà determina il numero di blocchi magici inseriti nel tabellone.

## Panoramica {#overview}

Come per ogni progetto, dobbiamo pianificare a grandi linee come affrontare l'implementazione. Ci sono molti modi per strutturare e realizzare il gioco. Tecnicamente, se volessimo, potremmo implementarlo interamente nel sistema GUI. Tuttavia, realizzare il gioco con oggetti di gioco (game object) e sprite, usando le API GUI per l'interfaccia a schermo e gli elementi informativi sovrapposti, è di solito l'approccio più naturale: seguiremo quindi questa strada.

Poiché prevediamo che il numero di file rimarrà piuttosto basso, manterremo molto semplice la struttura delle cartelle del progetto:

![Struttura delle cartelle](images/magic-link/linker_folders.png)

*main*
: Questa cartella conterrà tutta la logica del gioco. Qui risiederanno tutti gli script, i file degli oggetti di gioco, i file di collezione, i file GUI e così via. Se preferisci suddividerla in più cartelle o usare sottocartelle, va benissimo.

*images*
: Tutti gli asset delle immagini saranno conservati in questa cartella.

*fonts*
: Qui saranno conservati i font usati per il rendering del testo.

*input*
: In questa cartella saranno conservati i binding di input.

## Configurazione del progetto {#setting-up-the-project}

Nel file *game.project* manterremo perlopiù le impostazioni predefinite, ma ci sono alcune scelte da fare. Prima di tutto, dobbiamo scegliere una risoluzione per il gioco. Cambiarla in seguito è piuttosto semplice e, per il gioco definitivo, dovremo lavorare un po' per ottenere un buon risultato visivo indipendentemente dalla risoluzione o dal rapporto d'aspetto del dispositivo di destinazione.

Abbiamo scelto una risoluzione di 640x960 pixel, quella nativa dell'iPhone 4. È anche una risoluzione che rientra in molti monitor, rendendo agevoli le prove di gioco sul computer. Se vuoi lavorare a una risoluzione diversa, dovrai soltanto adattare alcuni valori.

![Impostazioni del progetto](images/magic-link/linker_project_settings.png)

Dovremo anche aumentare il numero massimo di sprite visualizzati. Se vuoi, puoi passare alla sezione successiva e tornare qui quando la console ti segnala che hai raggiunto il limite degli sprite.

![Layout delle dimensioni del gioco](images/magic-link/linker_layout.png)

Possiamo calcolare il numero massimo di sprite necessari:

* Il tabellone conterrà 7x9 blocchi. Serviranno dei margini lungo i bordi e uno spazio in alto per alcuni elementi GUI. Questo significa che i blocchi misureranno circa 90x90 pixel. Se fossero più piccoli, sarebbe troppo difficile interagirvi sullo schermo di un telefono di piccole dimensioni.
* Ogni blocco è uno sprite. Useremo animazioni di un solo fotogramma per impostare il colore del blocco.
* Alcuni blocchi saranno magici e per ciascuno useremo 4 sprite per gli effetti speciali.
* La grafica dei collegamenti richiederà uno sprite per elemento. Nel caso peggiore saranno 61 sprite aggiuntivi, se il giocatore riuscisse in qualche modo a collegare l'intero tabellone, esclusi i 2 blocchi magici che non si possono collegare tramite trascinamento.

Supponiamo quindi di avere un massimo di 30 blocchi magici. Il tabellone è composto da 63 blocchi, cioè sprite. Tra questi, i 30 blocchi magici aggiungono 4 sprite ciascuno per gli effetti speciali: altri 120 sprite. Considerando la grafica dei collegamenti, che in questo caso arriva a un massimo di 33, dovremo disegnare almeno 120 + 33 = 153 sprite a ogni fotogramma. La potenza di due più vicina è 256.

Tuttavia, impostare il massimo a 256 non basta. Ogni volta che svuotiamo e reimpostiamo il tabellone, elimineremo tutti gli oggetti di gioco presenti e ne genereremo di nuovi. Il conteggio degli sprite dovrà tenere conto di tutti gli oggetti esistenti durante il fotogramma, compresi quelli eliminati, perché vengono rimossi alla fine del fotogramma. Impostare il numero massimo di sprite a 512 sarà quindi sufficiente.

![Numero massimo di sprite](images/magic-link/linker_sprite_max_count.png)

## Aggiunta degli asset grafici {#adding-the-graphics-assets}

Tutti gli asset necessari per il gioco sono stati preparati in anticipo. Li aggiungeremo come immagini da 512x512 pixel e lasceremo che il motore le ridimensioni alla dimensione desiderata.

::: sidenote
Abilitando *hidpi* nelle impostazioni del progetto, il backbuffer passa all'alta risoluzione. Disegnando immagini grandi in scala ridotta, queste appariranno molto nitide sugli schermi Retina.
:::

![Aggiunta delle immagini](images/magic-link/linker_add_images.png)

Oltre ai blocchi, sono inclusi un'immagine per il connettore e alcuni sprite per gli effetti. Abbiamo anche due immagini di sfondo: una da usare per il tabellone e una per il menu principale. Aggiungi tutte le immagini alla cartella *images*, poi crea un file atlas chiamato *sprites.atlas*. Apri il file atlas e aggiungi tutte le immagini.

![Aggiunta delle immagini all'atlas](images/magic-link/linker_add_to_atlas.png)

Ci sono anche alcune immagini GUI usate per creare elementi dell'interfaccia, come pulsanti e finestre a comparsa. Queste vanno aggiunte a un atlas separato chiamato *gui.atlas*.

## Generazione del tabellone {#generating-the-board}

Il primo passo è creare la logica del tabellone. Il tabellone risiederà in una propria collezione (collection), che conterrà tutto ciò che compare sullo schermo durante il gioco. Per ora servono soltanto il componente fabbrica (factory) "blockfactory" e lo script. In seguito aggiungeremo una fabbrica per i collegamenti, componenti GUI per il menu principale e, infine, la logica di caricamento per avviare il gioco dal menu principale e un modo per tornare al menu.

1. Crea *`board.collection`* nella cartella *`main`*. Assicurati di chiamarla "board", così potremo indirizzarla in seguito. Se aggiungi il componente sprite dello sfondo, imposta la sua posizione Z a -1, altrimenti non verrà disegnato dietro tutti i blocchi che genereremo in seguito.
2. Imposta temporaneamente *Main Collection*, sotto *Bootstrap*, in *game.project* a `/main/board.collection`, così potremo eseguire facilmente le prove.

![Collezione del tabellone](images/magic-link/linker_board_collection.png)

![Collezione del tabellone come collezione di bootstrap](images/magic-link/linker_bootstrap_board.png)

Il file script *board.script* conterrà tutta la logica del tabellone e dei suoi blocchi. Inizia creando la funzione che costruisce il tabellone e richiamala temporaneamente da `init()`. Aggiungiamo anche due funzioni che non useremo subito, ma che torneranno utili in seguito:

`filter()`
: Questa funzione ci permetterà di filtrare elenchi di elementi, cioè blocchi.

`build_blocklist()`
: Crea un elenco semplice, senza annidamenti, di tutti i blocchi sul tabellone, che potremo quindi filtrare.

Dopo aver costruito il tabellone, useremo due strutture di dati diverse contenenti tutti i blocchi, `self.blocks` e `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Poiché la grafica dei blocchi si sovrappone, dobbiamo disegnarli nell'ordine corretto. Per farlo, impostiamo la coordinata z di ogni blocco. Il valore rimarrà ben al di sopra di -1, dove si trova lo sprite dello sfondo.

La logica del tabellone genera oggetti di gioco "`block`" tramite il componente fabbrica "`blockfactory`". Perché questo funzioni, dobbiamo creare l'oggetto di gioco del blocco. Il blocco contiene uno script e uno sprite. Impostiamo l'animazione predefinita dello sprite su uno qualsiasi dei blocchi colorati di *`sprites.atlas`*, poi aggiungiamo codice a *`block.script`* per far assumere al blocco il colore corretto quando viene generato:

![Oggetto di gioco del blocco](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale_xy(0.18)     -- render scaled down without changing Z

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Imposta la proprietà *Prototype* del componente fabbrica "blockfactory" sul nuovo file di oggetto di gioco *block.go*.

![Fabbrica dei blocchi](images/magic-link/linker_blockfactory.png)

Ora dovresti poter eseguire il gioco e vedere il tabellone riempito con blocchi di colori casuali:

![Prima schermata](images/magic-link/linker_first_screenshot.png)

## Interazioni {#interactions}

Ora che abbiamo un tabellone, dobbiamo aggiungere l'interazione con l'utente. Per prima cosa, definiamo i binding di input in *game.input_binding*, nella cartella *input*. Assicurati che le impostazioni di *game.project* usino il tuo file dei binding di input.

![Binding di input](images/magic-link/linker_input_bindings.png)

Ci serve un solo binding e assegniamo `MOUSE_BUTTON_LEFT` all'azione chiamata "touch". Questo gioco non usa il multitocco e, per comodità, Defold converte i tocchi con un solo dito in clic del pulsante sinistro del mouse.

La gestione dell'input spetta al tabellone, quindi dobbiamo aggiungere il relativo codice in *board.script*:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- What block was touched or dragged over?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- outside board.
            return
        end

        if action.pressed then
            -- Player started touch
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- then drag
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false
    end
end
```

I messaggi `make_orange` e `make_green` sono temporanei e servono soltanto a verificare visivamente che il codice funzioni. Dobbiamo aggiungere codice a *block.script* per gestirli:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Ora i blocchi riceveranno prima un messaggio `make_orange`, poi messaggi `make_green` per tutto il tempo in cui mantieni il tocco o premi il pulsante del mouse. È quindi probabile che i blocchi diventino arancioni solo per un istante, se mai riuscirai a vederlo, prima di diventare verdi. Sappiamo però quale blocco sta toccando il giocatore! Se vuoi seguire più in dettaglio come viene gestito l'input, inserisci chiamate a `print()` o `pprint()` nel codice.

## Evidenziare i collegamenti {#mark-links}

Ora ci servono gli asset dell'indicatore che mostrerà quando il giocatore collega i blocchi. L'idea è semplicemente sovrapporre un elemento grafico a ogni blocco per indicare che è collegato.

Dobbiamo creare un oggetto di gioco "connector" che contenga lo sprite con l'immagine del connettore, oltre a un componente fabbrica "connector factory" nell'oggetto di gioco "board":

![Oggetto di gioco del connettore](images/magic-link/linker_connector.png)

![Fabbrica dei connettori](images/magic-link/linker_connector_factory.png)

Lo script di questo oggetto di gioco è essenziale: deve soltanto ridimensionare la grafica per adattarla al resto del gioco e impostare correttamente l'ordine Z.

```lua
-- connector.script
function init(self)
    go.set_scale_xy(0.18)           -- Scale in 2D without changing Z.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

La funzione `same_color_neighbors()` restituisce un elenco di blocchi adiacenti a un determinato blocco, nella posizione x, y, e dello stesso colore. Usa la funzione `filter()`, applicata all'elenco completo e non annidato dei blocchi in `self.blocks`.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Una funzione ausiliaria, `in_blocklist()`, verifica se un blocco è presente in un elenco di blocchi:

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Usiamo queste funzioni durante l'input di tocco e trascinamento in `on_input()` per costruire la catena dei blocchi toccati. Qui verificheremo anche se i blocchi sono magici e li ignoreremo, benché non ce ne siano ancora:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Infine, quando il tocco termina, rimuoviamo visivamente tutti i connettori dei collegamenti.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Connettori nel gioco](images/magic-link/linker_connector_screen.png)

## Rimozione dei blocchi collegati {#remove-linked-blocks}

Ora abbiamo la logica che permette di collegare blocchi dello stesso colore, ed eliminarli è semplice. Impostiamo la posizione sul tabellone a `hash("removing")` anziché semplicemente a `nil` perché, più avanti, quando implementeremo la logica dei blocchi magici, dovremo assicurarci che questi scorrano soltanto negli spazi dei blocchi appena rimossi. Se qui impostassimo la posizione sul tabellone a `nil`, non avremmo modo di distinguere i blocchi appena rimossi da quelli rimossi in precedenza.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Ci servirà anche una funzione per rimuovere effettivamente, impostandole a `nil`, le posizioni sul tabellone che sono state impostate a `hash("removing")`:

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Creiamo anche una funzione che fa scorrere verso il basso i blocchi rimasti quando quelli sottostanti vengono rimossi, cioè impostati a `nil`. Percorriamo il tabellone per colonne, da sinistra a destra, e ogni colonna dal basso verso l'alto. Se incontriamo una posizione vuota (`nil`), facciamo scorrere verso il basso tutti i blocchi che si trovano sopra di essa.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Scorrimento dei blocchi verso il basso](images/magic-link/linker_blocks_slide.png)

Ora possiamo semplicemente aggiungere le chiamate a queste funzioni in `on_input()`, quando il tocco termina e ci sono blocchi in `self.chain`.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Logica dei blocchi magici {#magic-block-logic}

È il momento di aggiungere i blocchi magici. Per prima cosa, permettiamo a un blocco di diventare magico. In questo modo potremo effettuare un passaggio separato sul tabellone già riempito e convertire in magici i blocchi desiderati. Per rendere i blocchi magici più vivaci, creiamo prima un effetto magico animato sotto forma di oggetto di gioco *`magic_fx.go`*, che potremo generare dal blocco magico.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Questo oggetto di gioco contiene due sprite. Uno è il colore "magic", uno sprite che usa l'immagine *`magic-sphere_layer2.png`*, e l'altro è un effetto "light", uno sprite che usa l'immagine *`magic-sphere_layer3.png`*. L'oggetto viene impostato per ruotare al momento della generazione, in base al valore della proprietà `direction`. Facciamo anche in modo che risponda a due messaggi, `lights_on` e `lights_off`, che controllano lo sprite dell'effetto luminoso.

Crea un nuovo script e aggiungilo come componente script a *`magic_fx.go`*:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Ora il blocco magico genererà due oggetti di gioco `magic_fx` quando riceve il messaggio `make_magic`. Ruoteranno in direzioni opposte, creando un piacevole gioco di colori all'interno dei blocchi. Aggiungiamo anche un ulteriore sprite a *`block.go`* con l'immagine *`magic-sphere_layer4.png`*. Questa immagine viene posta a una coordinata Z superiore a quella dell'effetto generato e disegna il guscio, o "copertura", della sfera magica.

![Sprite della copertura](images/magic-link/linker_cover.png)

Dobbiamo aggiungere un componente *Factory* all'oggetto di gioco del blocco e indicargli di usare il nostro oggetto di gioco *`magic_fx.go`* come *Prototype*. Lo script del blocco deve anche rispondere ai messaggi `lights_on` e `lights_off` e inoltrarli agli oggetti generati. Ricorda che gli oggetti generati devono essere eliminati quando viene eliminato il blocco: se ne occupa la funzione `final()` del blocco. Tutto questo avviene in *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale_xy(0.18) -- render scaled down without changing Z

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale.xy", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale.xy", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Ora possiamo creare blocchi magici e anche illuminarli, un effetto che useremo per indicare che un blocco magico si trova accanto a un altro blocco magico.

![Blocco magico senza e con illuminazione](images/magic-link/linker_magic_blocks.png)

Dobbiamo ora modificare il codice che riempie il tabellone con i blocchi, in modo da inserirvi anche alcuni blocchi magici:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

La meccanica principale dei blocchi magici è la capacità di scorrere lateralmente quando scompare un altro blocco accanto a loro. Implementiamo tutti i dettagli di questa meccanica nella funzione `slide_magic_blocks()` in *board.script*. L'algoritmo è semplice:

1. Per ogni riga del tabellone, crea un elenco `M` di blocchi magici.
2. Scorri tutti i blocchi magici nell'elenco `M`, ripetendo il processo finché l'elenco non smette di ridursi. A ogni iterazione:
    1. Se sotto il blocco magico c'è una posizione impostata a `hash("removing")`, rimuovilo semplicemente dall'elenco `M`.
    2. Se accanto al blocco magico c'è uno spazio vuoto contrassegnato con `hash("removing")`, fallo scorrere lì, imposta la vecchia posizione a `hash("removing")` e poi rimuovilo dall'elenco `M`.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Possiamo provare la meccanica aggiungendo una chiamata alla funzione in `on_input()`:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Ora è chiaro perché abbiamo usato l'etichetta intermedia `hash("removing")` sulle posizioni durante la rimozione. Senza di essa, i blocchi magici scorrerebbero avanti e indietro in qualsiasi posizione vuota ai lati. Potrebbe essere una meccanica interessante, ma non è quella prevista per questo piccolo gioco.

Ora ci serve una logica per rilevare se i blocchi magici sono collegati, cioè se si trovano a sinistra, a destra, sopra o sotto l'uno rispetto all'altro, e dobbiamo sapere se tutti i blocchi magici sul tabellone sono collegati. L'algoritmo usato è piuttosto semplice:

1. Crea un elenco `M` di tutti i blocchi magici sul tabellone.
2. Per ogni blocco nell'elenco `M`:
    1. Se il blocco non ha `region` impostato, assegnagli il numero di regione `R`, inizialmente `1`.
    2. Contrassegna tutti i vicini del blocco non ancora contrassegnati con lo stesso numero di regione `R` e ripeti l'operazione sui loro vicini, sui vicini dei loro vicini e così via.
    3. Aumenta il numero di regione `R` di `1`.

![Assegnazione delle regioni](images/magic-link/linker_regions.png)

Ecco l'implementazione dell'algoritmo:

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Creiamo anche funzioni che ci permettono di contare il numero di regioni tra i blocchi magici. Se il numero di regioni è 1, sappiamo che tutti i blocchi magici sono collegati. Aggiungiamo inoltre una funzione che spegne le luci di tutti i blocchi magici e una che accende gli effetti luminosi dei blocchi magici che hanno altri blocchi magici come vicini:

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Ora possiamo inserire queste parti della logica nel flusso complessivo. Innanzitutto, poiché il tabellone viene generato casualmente, esiste una piccola probabilità che inizi già in uno stato di vittoria. Se succede, scartiamo semplicemente il tabellone e lo ricreiamo:

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Il resto della logica va in `on_input()`. Non c'è ancora codice per gestire il messaggio `level_completed`, ma per ora va bene così:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Ora è possibile giocare e raggiungere lo stato di vittoria, anche se non succede ancora nulla quando colleghi tutti i blocchi magici.

![Prima vittoria](images/magic-link/linker_first_win.png)

## Cadute di blocchi {#drops}

L'idea della "caduta" è aggiungere una semplice meccanica di progressione. Premendo il pulsante *DROP*, il giocatore può eseguire un numero limitato di cadute, ciascuna delle quali fa semplicemente cadere sul tabellone alcuni nuovi pezzi casuali. Il giocatore inizia con una caduta disponibile e ne riceve una aggiuntiva ogni volta che completa un livello. Il codice di questa meccanica è racchiuso in due funzioni: una restituisce un elenco delle possibili posizioni di arrivo dei blocchi e l'altra esegue effettivamente la caduta, animazione compresa.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Possiamo provare le cadute eseguendo il codice seguente, per esempio in `on_reload()`, oppure associandolo a un'azione di input temporanea:

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Caduta di blocchi](images/magic-link/linker_drop.png)

## Il menu principale {#the-main-menu}

È il momento di mettere insieme il tutto. Per prima cosa, creiamo una schermata iniziale e separiamola dal tabellone. Il primo passo è creare *main_menu.gui* e configurarla con un pulsante *Start*, composto da un nodo di testo e un nodo box con texture, un nodo di testo per il titolo e alcuni blocchi decorativi, realizzati con nodi box con texture. Lo script *main_menu.gui_script* che colleghiamo alla GUI anima i blocchi decorativi in `init()`. Contiene anche una funzione `on_input()` che invia un messaggio `start_game` a uno script principale. Creeremo questo script tra poco.

![GUI del menu principale](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Poiché presto sarà lo script del menu principale ad avviare il gioco, rimuovi la chiamata temporanea di preparazione del tabellone da `init()` in *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3            -- Number of magic blocks on the board

    self.drops = 1                -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false        -- Drag touch input
end
```

Lo script principale conserverà lo stato generale del gioco e lo avvierà su richiesta. Vogliamo che *main.collection* contenga soltanto il minimo degli asset da mostrare all'avvio. Per farlo, inseriamo in *main.collection* un oggetto di gioco "main" che contiene la GUI del menu principale, un componente script e, soprattutto, un componente *Collection Proxy*.

Il proxy di collezione permette di caricare e scaricare dinamicamente collezioni nel gioco in esecuzione. Agisce per conto di uno specifico file di collezione: inviando messaggi al proxy, possiamo caricare, inizializzare, abilitare, disabilitare e scaricare la collezione dinamica. Per una descrizione completa del suo utilizzo, consulta la [documentazione sui proxy di collezione](/manuals/collection-proxy).

Nel nostro caso impostiamo la proprietà *Collection* del componente proxy di collezione a *board.collection*, che contiene il "livello".

![Collezione principale](images/magic-link/linker_main_collection.png)

Ora apri *game.project* e cambia *main_collection* della sezione di bootstrap in `/main/main.collectionc`.

![Collezione principale di bootstrap](images/magic-link/linker_bootstrap_main.png)

Ora avviare una partita significa inviare messaggi al proxy di collezione per caricare, inizializzare e abilitare il tabellone, poi disabilitare il menu principale per nasconderlo. Tornare al menu principale comporta l'operazione inversa, a condizione che il proxy abbia caricato la collezione.

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Il socket si chiama "main": assicurati di aver impostato questo nome in *main.collection*. Seleziona il nodo radice e verifica che la proprietà *Name* sia "main".
2. Analogamente, inviamo messaggi alla collezione caricata tramite il suo socket, il cui nome è definito dalla proprietà *Name* della collezione.

## La GUI durante il gioco {#the-in-game-gui}

Prima di aggiungere l'ultima parte della logica allo script del tabellone, dobbiamo aggiungere alcuni elementi GUI al tabellone. Per prima cosa, nella parte superiore, aggiungiamo un pulsante *RESTART* e un pulsante *DROP*.

![GUI del tabellone](images/magic-link/linker_board_gui.png)

Lo script della GUI del tabellone invia messaggi alla finestra di dialogo GUI di riavvio quando si fa clic sul relativo pulsante, e allo script del tabellone stesso quando si fa clic su *DROP*:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

La finestra di dialogo *RESTART* è semplice. La creiamo in *restart.gui* e le associamo un semplice script che non esegue alcuna azione se il giocatore fa clic su *NO*, invia un messaggio `restart_level` allo script del tabellone se fa clic su *YES* e un messaggio `to_main_menu` allo script principale se fa clic su *Quit to main menu*:

![GUI di riavvio](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Creiamo anche una semplice finestra di dialogo GUI per il completamento del livello in *level_complete.gui*, con un semplice script che invia un messaggio `next_level` allo script del tabellone quando il giocatore fa clic su *CONTINUE*:

![Finestra di dialogo di completamento del livello](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Una finestra di dialogo presenta il livello corrente, con uno script che si limita a mostrarla e nasconderla. Quando viene mostrata, il suo messaggio viene impostato su un testo che include il livello di difficoltà corrente:

![GUI di presentazione del livello](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Aggiungiamo anche una finestra di dialogo che compare se il giocatore prova a eseguire una caduta ma non c'è spazio sufficiente.

![GUI per lo spazio insufficiente per la caduta](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Infine, aggiungiamo questi componenti GUI a *board.collection* e il codice necessario a *board.script*:

![Collezione definitiva del tabellone](images/magic-link/linker_board_collection_final.png)

In `on_message()` ci serve il codice per tutti i messaggi inviati al tabellone e dal tabellone.

`start_level`
: Imposta il numero di blocchi magici in base al parametro di difficoltà, costruisce il tabellone e poi mostra la finestra di dialogo GUI "present_level" per 2 secondi prima di avviare il gioco, nascondendo la finestra e acquisendo il focus dell'input. Usiamo `go.animate()` come temporizzatore animando il valore di "timer", che non viene usato per altro.

`restart_level`
: È ciò che accade quando il giocatore preme il pulsante GUI *RESTART* e conferma. Svuota e ricostruisce il tabellone, poi reimposta il contatore delle cadute.

`level_completed`
: Viene inviato non appena il tabellone si trova in uno stato di vittoria. Disattiva l'input, anima i blocchi magici e mostra la finestra di dialogo GUI "level_complete". La finestra invierà un messaggio `next_level` quando il giocatore fa clic sul pulsante *CONTINUE* al suo interno.

`next_level`
: Quando riceve questo messaggio, svuota il tabellone, aumenta il contatore delle cadute e invia `start_level` impostando il livello di difficoltà successivo.

`drop`
: Verifica dove è possibile eseguire le cadute. Se non ci sono posizioni disponibili, mostra la finestra di dialogo GUI "no_drop_room"; altrimenti esegue la caduta, se il giocatore ne ha ancora a disposizione, diminuisce il contatore delle cadute e ne aggiorna la rappresentazione visiva.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale_xy(0.17, m.id)
            go.animate(m.id, "scale.xy", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

Ecco fatto! Il gioco e questo tutorial sono ora completi. Divertiti a giocare!

![Gioco completato](images/magic-link/linker_game_finished.png)

## Proseguire {#moving-on}

Questo piccolo gioco ha alcune caratteristiche interessanti: prova a sperimentare! Ecco un elenco di esercizi che puoi svolgere per prendere più confidenza con Defold:

* Rendi più chiara l'interazione. Chi gioca per la prima volta potrebbe avere difficoltà a capire come funziona il gioco e con quali elementi può interagire. Dedica un po' di tempo a rendere il gioco più comprensibile, senza inserire elementi di tutorial.
* Aggiungi i suoni. Al momento il gioco è completamente silenzioso: una buona colonna sonora e suoni per le interazioni lo migliorerebbero.
* Rileva automaticamente la fine della partita.
* Punteggio massimo. Aggiungi una funzionalità che conservi il punteggio massimo in modo persistente.
* Implementa nuovamente il gioco usando soltanto le API GUI.
* Attualmente il gioco prosegue aggiungendo un blocco magico a ogni passaggio di livello. Questo non può continuare all'infinito. Trova una soluzione soddisfacente al problema.
* Ottimizza il gioco e riduci il numero massimo di sprite riutilizzandoli anziché eliminarli e generarli di nuovo.
* Implementa un rendering del gioco indipendente dalla risoluzione, così che mantenga un buon aspetto su schermi con risoluzioni e rapporti d'aspetto diversi.
