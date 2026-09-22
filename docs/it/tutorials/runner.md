---
title: Tutorial di un runner senza fine
brief: In questo tutorial parti da un progetto vuoto e crei un gioco runner completo con un personaggio animato, collisioni fisiche, oggetti da raccogliere e punteggio.
---

# Tutorial di un runner {#runner-tutorial}

In questo tutorial partiamo da un progetto vuoto e creiamo un gioco runner completo con un personaggio animato, collisioni fisiche, oggetti da raccogliere e punteggio.

Quando impari a usare un nuovo motore di gioco ci sono molte cose da assimilare, quindi abbiamo creato questo tutorial per aiutarti a cominciare. È un tutorial piuttosto completo che illustra il funzionamento del motore e dell'editor. Presupponiamo che tu abbia una certa familiarità con la programmazione.

Se ti serve un'introduzione alla programmazione in Lua, consulta il nostro [manuale di Lua in Defold](/manuals/lua).

Se questo tutorial ti sembra un po' troppo impegnativo per iniziare, visita la nostra [pagina dei tutorial](//www.defold.com/tutorials), dove trovi una selezione di tutorial di vari livelli di difficoltà.

Se preferisci guardare dei video tutorial, consulta [la versione video su YouTube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b).

Utilizziamo asset di gioco provenienti da altri due tutorial, con alcune piccole modifiche. Il tutorial è suddiviso in diversi passaggi, ognuno dei quali ci avvicina in modo significativo al gioco finale.

Il risultato finale sarà un gioco in cui controlli un eroe che corre attraverso un ambiente, raccogliendo monete ed evitando ostacoli. L'eroe corre a velocità costante e il giocatore ne controlla soltanto i salti premendo un unico pulsante (o toccando lo schermo su un dispositivo mobile). Il livello consiste in un flusso infinito di piattaforme su cui saltare e di monete da raccogliere.

Se in qualsiasi momento ti blocchi durante questo tutorial o mentre crei il tuo gioco, non esitare a chiederci aiuto sul [forum di Defold](//forum.defold.com). Nel forum puoi discutere di Defold, chiedere aiuto al team di Defold, vedere come altri sviluppatori di giochi hanno risolto i loro problemi e trovare nuove idee. Inizia subito.

::: sidenote
Nel corso del tutorial, le descrizioni dettagliate dei concetti e delle procedure sono contrassegnate come questo paragrafo. Se ritieni che queste sezioni siano troppo approfondite, puoi saltarle.
:::

Cominciamo, quindi. Ci auguriamo che questo tutorial ti diverta e ti aiuti a muovere i primi passi con Defold.

> Scarica gli asset per questo tutorial [qui](https://github.com/defold/sample-runner/tree/main/def-runner).

## PASSAGGIO 1 - Installazione e configurazione {#step-1-installation-and-setup}

Il primo passaggio consiste nello [scaricare i seguenti file](https://github.com/defold/sample-runner/tree/main/def-runner).

Se non hai ancora scaricato e installato l'editor Defold, è il momento di farlo:

:[install](../shared/install.md)

Una volta installato e avviato l'editor, è il momento di creare un nuovo progetto e prepararlo. Crea un [nuovo progetto](/manuals/project-setup/#creating-a-new-project) dal modello "Empty Project".

::: sidenote
Questo tutorial utilizza le funzionalità Spine dell'[estensione Spine](https://github.com/defold/extension-spine). Aggiungi l'estensione alla sezione delle dipendenze di *game.project*.
:::

## L'editor {#the-editor}

Al primo avvio, l'editor è vuoto e non ha alcun progetto aperto: scegli quindi <kbd>Open Project</kbd> dal menu e seleziona il progetto appena creato. Ti verrà anche chiesto di creare un "ramo" per il progetto.

Nel *pannello Assets* vedrai tutti i file che fanno parte del progetto. Facendo doppio clic sul file "main/main.collection", questo si aprirà nella vista dell'editor al centro:

![Panoramica dell'editor](images/runner/1/editor2_overview.png)

L'editor è composto dalle seguenti aree principali:

Pannello Assets
: Questa vista mostra tutti i file del progetto. I diversi tipi di file hanno icone diverse. Fai doppio clic su un file per aprirlo nell'editor dedicato a quel tipo di file. La cartella speciale di sola lettura *builtins* è comune a tutti i progetti e comprende elementi utili come uno script di rendering predefinito, un font, materiali per il rendering di vari componenti e altro ancora.

Vista principale dell'editor
: A seconda del tipo di file che stai modificando, questa vista mostra l'editor corrispondente. Quello più usato è l'editor di scene che vedi qui. Ogni file aperto viene mostrato in una scheda separata.

Changed Files
: Contiene i file aggiunti, modificati, rinominati o eliminati localmente rispetto al commit Git corrente. Puoi visualizzare le differenze di un file di testo modificato o rinominato alla volta; qui puoi anche annullare le modifiche locali selezionate. Utilizza un client Git esterno o la riga di comando per sincronizzarti con un repository remoto.

Outline
: Il contenuto del file che stai modificando, mostrato in una vista gerarchica. Attraverso questa vista puoi aggiungere, eliminare, modificare e selezionare oggetti e componenti.

Properties
: Le proprietà impostate sull'oggetto o sul componente attualmente selezionato.

Console
: Durante l'esecuzione del gioco, questa vista raccoglie l'output (log, errori, informazioni di debug e così via) proveniente dal motore di gioco, oltre agli eventuali messaggi di debug personalizzati `print()` e `pprint()` dei tuoi script. Se l'applicazione o il gioco non si avvia, la console è la prima cosa da controllare. Dietro la console si trovano una serie di schede che mostrano informazioni sugli errori e un editor di curve utilizzato per creare effetti particellari.

## Eseguire il gioco {#running-the-game}

Il modello di progetto "Empty" è effettivamente del tutto vuoto. Seleziona comunque <kbd>Project ▸ Build</kbd> per creare la build del progetto e avviare il gioco.

![Creazione della build](images/runner/1/build_and_launch.png)

Uno schermo nero forse non è molto entusiasmante, ma è un'applicazione di gioco Defold in esecuzione e possiamo facilmente trasformarla in qualcosa di più interessante. Facciamolo.

::: sidenote
L'editor Defold lavora sui file. Facendo doppio clic su un file nel *pannello Assets*, lo apri nell'editor adatto. Puoi quindi lavorare sul contenuto del file.

Quando hai finito di modificare un file, devi salvarlo. Seleziona <kbd>File ▸ Save</kbd> nel menu principale. L'editor ti ricorda le modifiche non salvate aggiungendo un asterisco '\*' al nome del file nella relativa scheda.

![File con modifiche non salvate](images/runner/1/file_changed.png)
:::

## Configurare il progetto {#setting-up-the-project}

Prima di iniziare, configuriamo alcune impostazioni del progetto. Apri l'asset *game.project* da `Assets Pane` e scorri fino alla sezione Display. Imposta `width` e `height` del progetto rispettivamente su `1280` e `720`.

Devi anche aggiungere l'estensione Spine al progetto, così potremo animare l'eroe. Aggiungi una versione dell'estensione Spine compatibile con la versione dell'editor Defold che hai installato. Le versioni disponibili di Spine sono elencate qui:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Fai clic con il pulsante destro sul link al file zip della release che vuoi utilizzare:

![Clic con il pulsante destro e copia del link alla release](images/runner/extension-spine-releases.png)

Aggiungi il link alla release all'elenco delle [dipendenze di game.project](/manuals/libraries/#setting-up-library-dependencies). Dopo aver aggiunto l'estensione Spine, devi anche riavviare l'editor per attivare l'integrazione con l'editor inclusa nell'estensione.


## PASSAGGIO 2 - Creare il terreno {#step-2-creating-the-ground}

Compiamo i primi piccoli passi e creiamo uno spazio per il nostro personaggio, o meglio un tratto di terreno a scorrimento. Lo faremo in pochi passaggi.

1. Importa gli asset grafici nel progetto trascinando i file immagine "ground01.png" e "ground02.png" (dalla sottocartella "level-images" del pacchetto di asset) in una posizione adatta del progetto, per esempio nella cartella "images" all'interno della cartella "main".
2. Crea un nuovo file *Atlas* che contenga le texture del terreno (fai clic con il pulsante destro su una cartella adatta, per esempio *main*, nel *pannello Assets* e seleziona <kbd>New ▸ Atlas File</kbd>). Assegna al file atlas il nome *level.atlas*.

  ::: sidenote
  Un *atlas* è un file che combina un insieme di immagini separate in un unico file immagine più grande. Questo permette di risparmiare spazio e migliorare le prestazioni. Puoi approfondire gli atlas e le altre funzionalità grafiche 2D nella [documentazione della grafica 2D](/manuals/2dgraphics).
  :::

3. Aggiungi le immagini del terreno al nuovo atlas facendo clic con il pulsante destro sulla radice dell'atlas in *Outline* e selezionando <kbd>Add Images</kbd>. Seleziona le immagini importate e fai clic su *OK*. Ogni immagine nell'atlas è ora accessibile come animazione di un singolo fotogramma (immagine fissa), da utilizzare in sprite, effetti particellari e altri elementi visivi. Salva il file.

  ![Creare un nuovo atlas](images/runner/1/new_atlas.png)

  ![Aggiungere immagini all'atlas](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Perché non funziona!?* Un problema comune per chi inizia a usare Defold è dimenticarsi di salvare! Dopo aver aggiunto immagini a un atlas, devi salvare il file prima di poter accedere alle immagini.
  :::

4. Crea un file di collezione *ground.collection* per il terreno e aggiungi 7 oggetti di gioco (fai clic con il pulsante destro sulla radice della collezione nella vista *Outline* e seleziona <kbd>Add Game Object</kbd>). Assegna agli oggetti i nomi "ground0", "ground1", "ground2" e così via modificando la proprietà *Id* nella vista *Properties*. Tieni presente che Defold assegna automaticamente un ID univoco ai nuovi oggetti di gioco.

5. Aggiungi un componente sprite a ciascun oggetto (fai clic con il pulsante destro sull'oggetto di gioco nella vista *Outline* e seleziona <kbd>Add Component</kbd>, poi seleziona *Sprite* e fai clic su *OK*), imposta la proprietà *Image* del componente sprite sull'atlas appena creato e imposta l'animazione predefinita dello sprite su una delle due immagini del terreno. Imposta la posizione X del _componente sprite_ (non dell'oggetto di gioco) su 190 e la posizione Y su 40. Poiché l'immagine è larga 380 pixel e la spostiamo lateralmente della metà di tale valore, il punto di pivot dell'oggetto di gioco si troverà sul bordo sinistro dell'immagine dello sprite.

  ![Creare la collezione del terreno](images/runner/1/ground_collection.png)

6. La grafica che utilizziamo è un po' troppo grande, quindi ridimensiona ogni oggetto di gioco al 60% (scala di 0.6 su X e Y, ottenendo tratti di terreno larghi 228 pixel).

  ![Ridimensionare il terreno](images/runner/1/scale_ground.png)

7. Disponi tutti gli _oggetti di gioco_ in fila. Imposta le posizioni X degli _oggetti di gioco_ (non dei componenti sprite) su 0, 228, 456, 684, 912, 1140 e 1368 (multipli della larghezza di 228 pixel).

  ::: sidenote
  Probabilmente è più semplice creare un oggetto di gioco completo, già ridimensionato e dotato di un componente sprite, e poi copiarlo. Selezionalo nella vista *Outline*, quindi seleziona <kbd>Edit ▸ Copy</kbd> e poi <kbd>Edit ▸ Paste</kbd>.

  Se vuoi tasselli più grandi o più piccoli, puoi semplicemente cambiare la scala. In questo caso, però, dovrai anche modificare le posizioni X di tutti gli oggetti di gioco del terreno affinché siano multipli della nuova larghezza.
  :::

8. Salva il file, poi aggiungi *ground.collection* al file *main.collection*: fai prima doppio clic sul file *main.collection*, poi fai clic con il pulsante destro sull'oggetto radice nella vista *Outline* e seleziona <kbd>Add Collection From File</kbd>. Nella finestra di dialogo, seleziona *ground.collection* e fai clic su *OK*. Assicurati di collocare *ground.collection* nella posizione 0, 0, 0, altrimenti apparirà spostata. Salva il file.

9. Avvia il gioco (<kbd>Project ▸ Build</kbd>) per verificare che tutto sia al suo posto.

  ![Terreno fermo](images/runner/1/still_ground.png)

A questo punto potresti avere un po' di confusione e chiederti che cosa siano davvero tutte le cose che abbiamo creato. Fermiamoci quindi un momento a esaminare gli elementi fondamentali di ogni progetto Defold:

Oggetti di gioco
: Sono entità che esistono nel gioco in esecuzione. Ogni oggetto di gioco ha una posizione nello spazio 3D, una rotazione e una scala. Non deve necessariamente essere visibile. Un oggetto di gioco contiene un numero qualsiasi di _componenti_ che aggiungono funzionalità come grafica (sprite, mappe di tasselli, modelli, modelli Spine ed effetti particellari), suoni, fisica, fabbriche (factory, per generare oggetti) e altro ancora. Puoi anche aggiungere _componenti script_ Lua per assegnare comportamenti a un oggetto di gioco. Ogni oggetto di gioco presente nei tuoi giochi ha un *id*, necessario per comunicare con esso attraverso lo scambio di messaggi.

Collezioni
: Le collezioni non esistono autonomamente in un gioco in esecuzione, ma permettono di assegnare nomi statici agli oggetti di gioco e, allo stesso tempo, di avere più istanze dello stesso oggetto di gioco. In pratica, le collezioni sono contenitori di oggetti di gioco e di altre collezioni. Puoi utilizzarle come prototipi (chiamati anche "prefab" o "blueprint" in altri motori) di gerarchie complesse di oggetti di gioco e collezioni. All'avvio, il motore carica una collezione principale e dà vita a tutto ciò che vi hai inserito. Per impostazione predefinita si tratta del file *main.collection* nella cartella *main* del progetto, ma puoi cambiarlo nelle impostazioni del progetto.

Per il momento queste descrizioni dovrebbero bastare. Puoi però trovare una spiegazione molto più approfondita nel [manuale degli elementi fondamentali](/manuals/building-blocks). Ti consigliamo di consultarlo in seguito per comprendere meglio come funziona Defold.

## PASSAGGIO 3 - Muovere il terreno {#step-3-making-the-ground-move}

Ora che tutti i tratti di terreno sono al loro posto, farli muovere è piuttosto semplice. L'idea è questa: spostare i tratti da destra a sinistra e, quando un tratto raggiunge l'estremità sinistra fuori dallo schermo, spostarlo nella posizione più a destra. Per muovere tutti questi oggetti di gioco serve uno script Lua, quindi creiamone uno:

1. Fai clic con il pulsante destro sulla cartella *main* nel *pannello Assets* e seleziona <kbd>New ▸ Script File</kbd>. Assegna al nuovo file il nome *ground.script*.
2. Fai doppio clic sul nuovo file per aprire l'editor di script Lua.
3. Elimina il contenuto predefinito del file e copia al suo interno il codice Lua seguente, poi salva il file.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Speed in pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Memorizza gli ID degli oggetti di gioco del terreno in una tabella Lua, così da poterli scorrere.
2. La funzione `init()` viene chiamata quando l'oggetto di gioco prende vita nel gioco. Inizializziamo una variabile membro locale all'oggetto che contiene la velocità del terreno.
3. `update()` viene chiamata una volta per fotogramma, in genere 60 volte al secondo. `dt` contiene il numero di secondi trascorsi dall'ultima chiamata.
4. Scorri tutti gli oggetti di gioco del terreno.
5. Memorizza la posizione corrente in una variabile locale, poi, se l'oggetto corrente si trova all'estremità sinistra, spostalo all'estremità destra.
6. Riduci la posizione X corrente in base alla velocità impostata. Moltiplica per `dt` per ottenere una velocità in pixel/s indipendente dalla frequenza dei fotogrammi.
7. Aggiorna la posizione dell'oggetto con la nuova velocità.

::: sidenote
Il nucleo del motore Defold gestisce rapidamente i dati e gli oggetti di gioco. Tutta la logica e tutti i comportamenti necessari per il tuo gioco vengono creati in Lua. Lua è un linguaggio di programmazione veloce e leggero, ottimo per scrivere la logica di gioco. Esistono eccellenti risorse per impararlo, come il libro [Programming in Lua](http://www.lua.org/pil/) e il [manuale di riferimento ufficiale di Lua](http://www.lua.org/manual/5.3/).

Defold aggiunge a Lua una serie di API e un sistema di _scambio di messaggi_ che permette di programmare la comunicazione tra gli oggetti di gioco. Consulta il [manuale dello scambio di messaggi](/manuals/message-passing) per i dettagli sul suo funzionamento.
:::

::: sidenote
Puoi mostrare o nascondere le sezioni Assets Pane, Console e Outline dell'editor usando rispettivamente i tasti <kbd>F6</kbd>, <kbd>F7</kbd> e <kbd>F8</kbd>.
:::

Ora che abbiamo un file di script, dobbiamo aggiungere un riferimento a esso in un componente di un oggetto di gioco. In questo modo lo script verrà eseguito come parte del ciclo di vita dell'oggetto di gioco. Creiamo quindi un nuovo oggetto di gioco in *ground.collection* e aggiungiamogli un componente *Script* che faccia riferimento al file di script Lua appena creato:

1. Fai clic con il pulsante destro sulla radice della collezione e seleziona <kbd>Add Game Object</kbd>. Imposta l'*id* dell'oggetto su "controller".
2. Fai clic con il pulsante destro sull'oggetto "controller" e seleziona <kbd>Add Component from file</kbd>, poi seleziona il file *ground.script*.

![Controller del terreno](images/runner/1/ground_controller.png)

Ora, quando esegui il gioco, l'oggetto di gioco "controller" eseguirà lo script nel suo componente *Script*, facendo scorrere il terreno in modo fluido sullo schermo.

## PASSAGGIO 4 - Creare un eroe {#step-4-creating-a-hero-character}

L'eroe sarà un oggetto di gioco composto dai seguenti componenti:

Un *Spine Model*
: Questo ci fornisce un piccolo eroe simile a una marionetta di carta, le cui parti del corpo possono essere animate in modo fluido e con un costo ridotto.

Un *Collision Object*
: Rileverà le collisioni tra l'eroe e gli elementi del livello su cui può correre, che sono pericolosi o che può raccogliere.

Uno *Script*
: Acquisisce l'input dell'utente e vi reagisce, gestisce i salti e le animazioni dell'eroe e si occupa delle collisioni.

Inizia importando le immagini delle parti del corpo, poi aggiungile a un nuovo atlas che chiameremo *hero.atlas*:

1. Crea una nuova cartella facendo clic con il pulsante destro nel *pannello Assets* e selezionando <kbd>New ▸ Folder</kbd>. Assicurati di non selezionare una cartella prima di fare clic, altrimenti la nuova cartella verrà creata al suo interno. Assegna alla cartella il nome "hero".
2. Crea un nuovo file atlas facendo clic con il pulsante destro sulla cartella *hero* e selezionando <kbd>New ▸ Atlas File</kbd>. Assegna al file il nome *hero.atlas*.
3. Crea una nuova sottocartella *images* nella cartella *hero*. Fai clic con il pulsante destro sulla cartella *hero* e seleziona <kbd>New ▸ Folder</kbd>.
4. Trascina le immagini delle parti del corpo dalla cartella *hero-images* del pacchetto di asset alla cartella *images* appena creata nel *pannello Assets*.
5. Apri *hero.atlas*, fai clic con il pulsante destro sul nodo radice in *Outline* e seleziona <kbd>Add Images</kbd>. Seleziona tutte le immagini delle parti del corpo e fai clic su *OK*.
6. Salva il file atlas.

![Atlas dell'eroe](images/runner/2/hero_atlas.png)

Dobbiamo anche importare i dati delle animazioni Spine e configurare una *Spine Scene* per utilizzarli:

1. Trascina il file *hero.spinejson* (incluso nel pacchetto di asset) nella cartella *hero* del *pannello Assets*.
2. Crea un file *Spine Scene*. Fai clic con il pulsante destro sulla cartella *hero* e seleziona <kbd>New ▸ Spine Scene File</kbd>. Assegna al file il nome *hero.spinescene*.
3. Fai doppio clic sul nuovo file per aprire e modificare la *Spine Scene*.
4. Imposta la proprietà *spine_json* sul file JSON importato *hero.spinejson*. Fai clic sulla proprietà, poi sul pulsante di selezione del file *...* per aprire il browser delle risorse.
5. Imposta la proprietà *atlas* in modo che faccia riferimento al file *hero.atlas*.
6. Salva il file.

![Scena Spine dell'eroe](images/runner/2/hero_spinescene.png)

::: sidenote
Il file *hero.spinejson* è stato esportato in formato Spine JSON. Per creare file di questo tipo ti serve il software di animazione Spine. Se vuoi usare un altro software di animazione, puoi esportare le animazioni come fogli di sprite e utilizzarle come animazioni flipbook da risorse *Tile Source* o *Atlas*. Consulta il manuale delle [animazioni](/manuals/animation) per maggiori informazioni.
:::

### Costruire l'oggetto di gioco {#building-the-game-object}

Ora possiamo iniziare a costruire l'oggetto di gioco dell'eroe:

1. Crea un nuovo file *hero.go* (fai clic con il pulsante destro sulla cartella *hero* e seleziona <kbd>New ▸ Game Object File</kbd>).
2. Apri il file dell'oggetto di gioco.
3. Aggiungi un componente *Spine Model*. (Fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Component</kbd>, poi seleziona "Spine Model".)
4. Imposta la proprietà *Spine Scene* del componente sul file *hero.spinescene* appena creato e seleziona "run_right" come animazione predefinita (sistemeremo correttamente le animazioni più avanti).
5. Salva il file.

![Proprietà del modello Spine](images/runner/2/spinemodel_properties.png)

Ora è il momento di aggiungere la fisica affinché le collisioni funzionino:

1. Aggiungi un componente *Collision Object* all'oggetto di gioco dell'eroe. (Fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Component</kbd>, poi seleziona "Collision Object".)
2. Fai clic con il pulsante destro sul nuovo componente e seleziona <kbd>Add Shape</kbd>. Aggiungi due forme che coprano il corpo del personaggio. Andranno bene una sfera e un parallelepipedo.
3. Fai clic sulle forme e usa *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) per collocarle nelle posizioni appropriate.
4. Seleziona il componente *Collision Object* e imposta la proprietà *Type* su "Kinematic".

::: sidenote
Le collisioni di tipo "Kinematic" vengono rilevate, ma il motore fisico non le risolve automaticamente e non simula gli oggetti. Il motore fisico supporta diversi tipi di oggetti di collisione. Puoi approfondirli nella [documentazione della fisica](/manuals/physics).
:::

È importante specificare con cosa deve interagire l'oggetto di collisione:

1. Imposta la proprietà *Group* su un nuovo gruppo di collisione chiamato "hero".
2. Imposta la proprietà *Mask* su un altro gruppo, "geometry", con cui questo oggetto di collisione deve rilevare collisioni. Il gruppo "geometry" non esiste ancora, ma presto aggiungeremo oggetti di collisione che vi appartengono.

Infine, crea un nuovo file *hero.script* e aggiungilo all'oggetto di gioco.

1. Fai clic con il pulsante destro sulla cartella *hero* nel *pannello Assets* e seleziona <kbd>New ▸ Script File</kbd>. Assegna al nuovo file il nome *hero.script*.
2. Apri il nuovo file, copia e incolla al suo interno il codice seguente e poi salvalo. (Il codice è piuttosto semplice, a parte il risolutore che separa la forma di collisione dell'eroe dagli oggetti con cui collide. Se ne occupa la funzione `handle_geometry_contact()`.)

![Oggetto di gioco dell'eroe](images/runner/2/hero_game_object.png)

::: sidenote
Gestiamo le collisioni autonomamente perché, se impostassimo l'oggetto di collisione del personaggio come dinamico, il motore eseguirebbe una simulazione newtoniana dei corpi coinvolti. Per un gioco come questo, una simulazione del genere è tutt'altro che ottimale: invece di contrastare il motore fisico applicando varie forze, assumiamo quindi il pieno controllo.

Per farlo e gestire correttamente le collisioni serve un po' di matematica vettoriale. Trovi una spiegazione approfondita su come risolvere le collisioni cinematiche nella [documentazione della fisica](/manuals/physics-resolving-collisions/).
:::

```lua
-- gravity pulling the player down in pixel units/sˆ2
local gravity = -20

-- take-off speed when jumping in pixel units/s
local jump_takeoff_speed = 900

function init(self)
    -- this tells the engine to send input to on_input() in this script
    msg.post(".", "acquire_input_focus")

    -- save the starting position
    self.position = go.get_position()

    -- keep track of movement vector and if there is ground contact
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Return input focus when the object is deleted
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Apply gravity if there's no ground contact
        self.velocity = self.velocity + gravity
    end

    -- apply velocity to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- check if we received a contact point message. One message for each contact point
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Aggiungi lo script come componente *Script* all'oggetto dell'eroe (fai clic con il pulsante destro sulla radice di *hero.go* in *Outline* e seleziona <kbd>Add Component from File</kbd>, poi seleziona il file *hero.script*).

Se vuoi, ora puoi provare ad aggiungere temporaneamente l'eroe alla collezione principale ed eseguire il gioco per vederlo cadere attraverso il mondo.

L'ultima cosa che serve per rendere operativo l'eroe è l'input. Lo script qui sopra contiene già una funzione `on_input()` che risponde alle azioni "jump" e "touch" (per gli schermi tattili). Aggiungiamo i binding di input per queste azioni.

1. Apri "input/game.input_bindings".
2. Aggiungi un trigger da tastiera per "KEY_SPACE" e assegna all'azione il nome "jump".
3. Aggiungi un trigger tattile per "TOUCH_MULTI" e assegna all'azione il nome "touch". (I nomi delle azioni sono arbitrari, ma devono corrispondere ai nomi nello script. Non puoi usare lo stesso nome di azione per più trigger.)
4. Salva il file.

![Binding di input](images/runner/2/input_bindings.png)

## PASSAGGIO 5 - Riorganizzare il livello {#step-5-refactoring-the-level}

Ora che abbiamo un eroe completo di collisioni e di tutto il necessario, dobbiamo aggiungere le collisioni anche al terreno, in modo che l'eroe abbia qualcosa con cui collidere (o su cui correre). Lo faremo tra un momento, ma prima riorganizziamo un po' il progetto: mettiamo tutti gli elementi del livello in una collezione separata e riordiniamo la struttura dei file:

1. Crea un nuovo file *level.collection* (fai clic con il pulsante destro su *main* nel *pannello Assets* e seleziona <kbd>New ▸ Collection File</kbd>).
2. Apri il nuovo file, fai clic con il pulsante destro sulla radice in *Outline*, seleziona <kbd>Add Collection from File</kbd> e scegli *ground.collection*.
3. In *level.collection*, fai clic con il pulsante destro sulla radice in *Outline*, seleziona <kbd>Add Game Object File</kbd> e scegli *hero.go*.
4. Ora crea una nuova cartella chiamata *level* nella radice del progetto (fai clic con il pulsante destro nello spazio bianco sotto *game.project* e seleziona <kbd>New ▸ Folder</kbd>), poi sposta al suo interno gli asset del livello creati finora: i file *level.collection* e *level.atlas*, la cartella "images" con le immagini per l'atlas del livello e i file *ground.collection* e *ground.script*.
5. Apri *main.collection*, elimina *ground.collection* e aggiungi al suo posto *level.collection* (fai clic con il pulsante destro e seleziona <kbd>Add Collection from File</kbd>), che ora contiene *ground.collection*. Assicurati di collocare la collezione nella posizione 0, 0, 0.

::: sidenote
Come forse avrai già notato, la gerarchia dei file visibile nel *pannello Assets* è indipendente dalla struttura dei contenuti che costruisci nelle collezioni. I file di collezione e di oggetto di gioco contengono riferimenti ai singoli file, ma questi possono trovarsi dove preferisci.

Se vuoi spostare un file, Defold ti aiuta aggiornando automaticamente i riferimenti al file (refactoring). Quando realizzi un software complesso come un gioco, è estremamente utile poter cambiare la struttura del progetto man mano che cresce e si evolve. Defold lo incoraggia e rende il processo semplice, quindi non temere di spostare i file!
:::

Dobbiamo anche aggiungere alla collezione del livello un oggetto di gioco controller con un componente script:

1. Crea un nuovo file di script. Fai clic con il pulsante destro sulla cartella *level* nel *pannello Assets* e seleziona <kbd>New ▸ Script File</kbd>. Assegna al file il nome *controller.script*.
2. Apri il file di script, copia al suo interno il codice seguente e salva il file:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Questa è una proprietà dello script. Le assegniamo un valore predefinito, ma ogni istanza dello script inserita può sovrascriverlo direttamente nella vista delle proprietà dell'editor.

3. Apri il file *level.collection*.
4. Fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Game Object</kbd>.
5. Imposta *Id* su "controller".
6. Fai clic con il pulsante destro sull'oggetto di gioco "controller" in *Outline*, seleziona <kbd>Add Component from File</kbd> e scegli il file *controller.script* nella cartella *level*.
7. Salva il file.

![Proprietà dello script](images/runner/2/script_property.png)

::: sidenote
L'oggetto di gioco "controller" non esiste in un file, ma viene creato direttamente nella collezione del livello. Questo significa che l'istanza dell'oggetto di gioco viene creata a partire dai dati incorporati nella collezione. È una soluzione adatta agli oggetti di gioco con un unico scopo, come questo. Se ti servono più istanze di un oggetto di gioco e vuoi poter modificare il prototipo o modello usato per creare ciascuna istanza, crea un file di oggetto di gioco e aggiungi l'oggetto alla collezione dal file. In questo modo crei un oggetto di gioco che fa riferimento al file come prototipo o modello.

Lo scopo di questo oggetto di gioco "controller" è controllare tutto ciò che riguarda il livello in esecuzione. Presto questo script si occuperà di generare piattaforme e monete con cui l'eroe potrà interagire, ma per ora imposterà soltanto la velocità del livello.
:::

Nella funzione `init()` dello script controller del livello viene inviato un messaggio al componente script dell'oggetto controller del terreno, indirizzato tramite il suo ID:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

L'ID dell'oggetto di gioco controller è impostato su `"ground/controller"` perché si trova nella collezione "ground". Aggiungiamo poi l'ID del componente, `"controller"`, dopo il carattere cancelletto `"#"` che separa l'ID dell'oggetto da quello del componente. Lo script del terreno non contiene ancora codice per reagire al messaggio `set_speed`, quindi dobbiamo aggiungere una funzione `on_message()` a *ground.script* e la logica necessaria.

1. Apri *ground.script*.
2. Aggiungi il codice seguente e salva il file:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Tutti i messaggi vengono internamente sottoposti a hash quando sono inviati e devono essere confrontati con il valore hash.
2. I dati del messaggio sono una tabella Lua contenente i dati inviati insieme al messaggio.

![Aggiungere il codice del terreno](images/runner/insert_ground_code.png)

## PASSAGGIO 6 - Fisica del terreno e piattaforme {#step-6-ground-physics-and-platforms}

A questo punto dobbiamo aggiungere le collisioni fisiche al terreno:

1. Apri il file *ground.collection*.
2. Aggiungi un nuovo componente *Collision Object* a un oggetto di gioco adatto. Poiché lo script del terreno non risponde alle collisioni (tutta quella logica si trova nello script dell'eroe), possiamo inserirlo in qualsiasi oggetto di gioco _fermo_ (gli oggetti dei tasselli del terreno si muovono, quindi evitali). L'oggetto di gioco "controller" è una buona scelta, ma se preferisci puoi creare un oggetto separato. Fai clic con il pulsante destro sull'oggetto di gioco, seleziona <kbd>Add Component</kbd> e poi *Collision Object*.
3. Aggiungi una forma a parallelepipedo facendo clic con il pulsante destro sul componente *Collision Object* e selezionando <kbd>Add Shape</kbd>, poi *Box*.
4. Usa *Move Tool* e *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> e <kbd>Scene ▸ Scale Tool</kbd>) per fare in modo che il parallelepipedo copra tutti i tasselli del terreno.
5. Imposta la proprietà *Type* dell'oggetto di collisione su "Static", poiché la rappresentazione fisica del terreno non si muoverà.
6. Imposta la proprietà *Group* dell'oggetto di collisione su "geometry" e *Mask* su "hero". Ora l'oggetto di collisione dell'eroe e questo oggetto rileveranno le collisioni tra loro.
7. Salva il file.

![Collisione del terreno](images/runner/2/ground_collision.png)

Ora dovresti poter provare a eseguire il gioco (<kbd>Project ▸ Build</kbd>). L'eroe dovrebbe correre sul terreno e dovrebbe essere possibile saltare con il tasto <kbd>Space</kbd>. Se esegui il gioco su un dispositivo mobile, puoi saltare toccando lo schermo.

Per rendere la vita nel nostro mondo di gioco un po' meno monotona, aggiungiamo delle piattaforme su cui saltare.

1. Trascina il file immagine *rock_planks.png* dal pacchetto di asset alla sottocartella *level/images*.
2. Apri *level.atlas* e aggiungi la nuova immagine all'atlas (fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Images</kbd>).
3. Salva il file.
4. Crea un nuovo file *Game Object* chiamato *platform.go* nella cartella *level*. (Fai clic con il pulsante destro su *level* nel *pannello Assets*, poi seleziona <kbd>New ▸ Game Object File</kbd>.)
5. Aggiungi un componente *Sprite* all'oggetto di gioco (fai clic con il pulsante destro sulla radice nella vista *Outline* e seleziona <kbd>Add Component</kbd>, poi *Sprite*).
6. Imposta la proprietà *Image* in modo che faccia riferimento al file *level.atlas* e imposta *Default Animation* su "rock_planks". Per comodità, conserva gli oggetti del livello in una sottocartella "level/objects".
7. Aggiungi un componente *Collision Object* all'oggetto di gioco della piattaforma (fai clic con il pulsante destro sulla radice nella vista *Outline* e seleziona <kbd>Add Component</kbd>).
8. Assicurati di impostare *Type* del componente su "Kinematic", *Group* su "geometry" e *Mask* su "hero".
9. Aggiungi una *Box Shape* al componente *Collision Object*. (Fai clic con il pulsante destro sul componente in *Outline* e seleziona <kbd>Add Shape</kbd>, poi scegli *Box*.)
10. Usa *Move Tool* e *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> e <kbd>Scene ▸ Scale Tool</kbd>) affinché la forma del componente *Collision Object* copra la piattaforma.
11. Crea un file *Script* chiamato *platform.script* (fai clic con il pulsante destro nel *pannello Assets*, poi seleziona <kbd>New ▸ Script File</kbd>), inserisci il codice seguente nel file e salvalo:

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Default speed in pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Elimina semplicemente la piattaforma quando si è spostata oltre il bordo destro dello schermo.

12. Apri *platform.go* e aggiungi il nuovo script come componente (fai clic con il pulsante destro sulla radice nella vista *Outline*, seleziona <kbd>Add Component From File</kbd> e scegli *platform.script*).
13. Copia *platform.go* in un nuovo file (fai clic con il pulsante destro sul file nel *pannello Assets* e seleziona <kbd>Copy</kbd>, poi fai di nuovo clic con il pulsante destro e seleziona <kbd>Paste</kbd>) e chiama il nuovo file *platform_long.go*.
14. Apri *platform_long.go* e aggiungi un secondo componente *Sprite* (fai clic con il pulsante destro sulla radice nella vista *Outline* e seleziona <kbd>Add Component</kbd>). In alternativa, puoi copiare lo *Sprite* esistente.
15. Usa *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) per disporre i componenti *Sprite* uno accanto all'altro.
16. Usa *Move Tool* e *Scale Tool* affinché la forma del componente *Collision Object* copra entrambe le piattaforme.

![Piattaforma](images/runner/2/platform_long.png)

::: sidenote
Sia *platform.go* sia *platform_long.go* hanno componenti *Script* che fanno riferimento allo stesso file di script. È utile, perché qualsiasi modifica al file di script influenzerà il comportamento sia delle piattaforme normali sia di quelle lunghe.
:::

## Generare le piattaforme {#spawning-platforms}

L'idea è creare un semplice runner senza fine. Questo significa che non possiamo collocare gli oggetti di gioco delle piattaforme in una collezione nell'editor. Dobbiamo invece generarli dinamicamente:

1. Apri *level.collection*.
2. Aggiungi due componenti *Factory* all'oggetto di gioco "controller" (fai clic con il pulsante destro sull'oggetto e seleziona <kbd>Add Component</kbd>, poi *Factory*).
3. Imposta le proprietà *Id* dei componenti su "platform_factory" e "platform_long_factory".
4. Imposta la proprietà *Prototype* di "platform_factory" sul file */level/objects/platform.go*.
5. Imposta la proprietà *Prototype* di "platform_long_factory" sul file */level/objects/platform_long.go*.
6. Salva il file.
7. Apri il file *controller.script*, che gestisce il livello.
8. Modifica lo script in modo che contenga quanto segue, poi salva il file:

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Maybe spawn a platform at random height
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Valori predefiniti per la posizione Y a cui generare le piattaforme.
2. La funzione `update()` viene chiamata una volta per fotogramma e la usiamo per decidere se generare una piattaforma normale o lunga a determinati intervalli (per evitare sovrapposizioni) e altezze. È facile sperimentare diversi algoritmi di generazione per creare gameplay differenti.

Ora esegui il gioco (<kbd>Project ▸ Build</kbd>).

Wow, sta cominciando a diventare qualcosa di (quasi) giocabile...

![Eseguire il gioco](images/runner/2/run_game.png)

## PASSAGGIO 7 - Animazioni e morte {#step-7-animation-and-death}

La prima cosa da fare è dare vita all'eroe. In questo momento il poveretto è bloccato in un ciclo di corsa e non reagisce bene ai salti o ad altro. Il file Spine che abbiamo aggiunto dal pacchetto di asset contiene proprio una serie di animazioni adatte a questo scopo.

1. Apri il file *hero.script* e aggiungi le funzioni seguenti _prima_ della funzione `update()` esistente:

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- only play animations which are not already playing
        if self.anim ~= anim then
            -- tell the spine model to play the animation
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- remember which animation is playing
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- make sure the right animation is playing
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Trova la funzione `update()` e aggiungi una chiamata a `update_animation`:

```lua
    ...
    -- apply it to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Inserire il codice dell'eroe](images/runner/insert_hero_code.png)

::: sidenote
Lua usa un "ambito lessicale" per le variabili locali e tiene conto dell'ordine in cui inserisci le funzioni `local`. La funzione `update()` chiama le funzioni locali `update_animation()` e `play_animation()`: questo significa che il runtime deve aver già incontrato le funzioni locali per poterle chiamare. Per questo dobbiamo inserirle prima di `update()`. Se inverti l'ordine delle funzioni, otterrai un errore. Questo vale soltanto per le variabili `local`. Puoi approfondire le regole di ambito e le funzioni locali di Lua su http://www.lua.org/pil/6.2.html
:::

Questo è tutto ciò che serve per aggiungere le animazioni di salto e caduta all'eroe. Se esegui il gioco, noterai che giocare è molto più piacevole. Potresti anche accorgerti che, purtroppo, le piattaforme possono spingere l'eroe fuori dallo schermo. È un effetto collaterale della gestione delle collisioni, ma il rimedio è semplice: aggiungiamo un po' di violenza e rendiamo pericolosi i bordi delle piattaforme!

1. Trascina *spikes.png* dal pacchetto di asset alla cartella "level/images" nel *pannello Assets*.
2. Apri *level.atlas* e aggiungi l'immagine (fai clic con il pulsante destro e seleziona <kbd>Add Images</kbd>).
3. Apri *platform.go* e aggiungi alcuni componenti *Sprite*. Imposta *Image* su *level.atlas* e *Default Animation* su "spikes".
4. Usa *Move Tool* e *Rotate Tool* per collocare gli spuntoni lungo i bordi della piattaforma.
5. Per disegnare gli spuntoni dietro la piattaforma, imposta la posizione *Z* dei loro sprite su -0.1.
6. Aggiungi un nuovo componente *Collision Object* alle piattaforme (fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Component</kbd>). Imposta la proprietà *Group* su "danger" e *Mask* su "hero".
7. Aggiungi una forma a parallelepipedo al *Collision Object* (fai clic con il pulsante destro e seleziona <kbd>Add Shape</kbd>) e usa *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) e *Scale Tool* per collocare la forma in modo che l'eroe entri in collisione con l'oggetto "danger" quando colpisce la piattaforma di lato o da sotto.
8. Salva il file.

    ![Spuntoni della piattaforma](images/runner/3/danger_edges.png)

9. Apri *hero.go*, seleziona il *Collision Object* e aggiungi il nome "danger" alla proprietà *Mask*. Poi salva il file.

    ![Collisione dell'eroe](images/runner/3/hero_collision.png)

10. Apri *hero.script* e modifica la funzione `on_message()` in modo da ottenere una reazione quando l'eroe collide con un bordo "danger":

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Aggiungi una rotazione e un movimento di caduta all'eroe quando muore. Questo effetto può essere migliorato molto!

11. Modifica la funzione `init()` affinché invii un messaggio "reset" per inizializzare l'oggetto, poi salva il file:

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## PASSAGGIO 8 - Ripristinare il livello {#step-8-resetting-the-level}

Se provi il gioco ora, ti accorgerai subito che il meccanismo di ripristino non funziona. L'eroe viene ripristinato correttamente, ma può facilmente ritrovarsi in una situazione in cui cade immediatamente sul bordo di una piattaforma e muore di nuovo. Vogliamo invece ripristinare correttamente l'intero livello alla morte dell'eroe. Poiché il livello è soltanto una serie di piattaforme generate, basta tenere traccia di tutte le piattaforme generate ed eliminarle al ripristino:

1. Apri il file *controller.script* e modifica il codice in modo che memorizzi gli ID di tutte le piattaforme generate:

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Usiamo una tabella per memorizzare tutte le piattaforme generate.
    2. Il messaggio "reset" elimina tutte le piattaforme memorizzate nella tabella.
    3. Il messaggio "delete_spawn" elimina una piattaforma specifica e la rimuove dalla tabella.

2. Salva il file.
3. Apri *platform.script* e modificalo in modo che, invece di eliminare semplicemente una piattaforma che ha raggiunto l'estremità sinistra, invii un messaggio al controller del livello chiedendo di rimuoverla:

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Inserire il codice della piattaforma](images/runner/insert_platform_code.png)

4. Salva il file.
5. Apri *hero.script*. L'ultima cosa da fare ora è chiedere al livello di eseguire il ripristino. Abbiamo spostato il messaggio che chiede all'eroe di ripristinarsi nello script controller del livello. Centralizzare in questo modo il controllo del ripristino ha senso perché ci permette, per esempio, di introdurre più facilmente una sequenza di morte temporizzata più lunga:

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Inserire il codice dell'eroe](images/runner/insert_hero_code_2.png)

Ora il ciclo principale di ripartenza e morte è pronto!

Passiamo a qualcosa per cui valga la pena vivere: le monete!

## PASSAGGIO 9 - Monete da raccogliere {#step-9-coins-to-collect}

L'idea è inserire nel livello delle monete che il giocatore possa raccogliere. La prima domanda è come inserirle. Potremmo, per esempio, sviluppare uno schema di generazione coordinato in qualche modo con l'algoritmo di generazione delle piattaforme. Alla fine, però, abbiamo scelto un approccio molto più semplice: lasciare che siano le piattaforme stesse a generare le monete:

1. Trascina l'immagine *coin.png* dal pacchetto di asset a "level/images" nel *pannello Assets*.
2. Apri *level.atlas* e aggiungi l'immagine (fai clic con il pulsante destro e seleziona <kbd>Add Images</kbd>).
3. Crea un file *Game Object* chiamato *coin.go* nella cartella *level* (fai clic con il pulsante destro su *level* nel *pannello Assets* e seleziona <kbd>New ▸ Game Object File</kbd>).
4. Apri *coin.go* e aggiungi un componente *Sprite* (fai clic con il pulsante destro in *Outline* e seleziona <kbd>Add Component</kbd>). Imposta *Image* su *level.atlas* e *Default Animation* su "coin".
5. Aggiungi un *Collision Object* (fai clic con il pulsante destro in *Outline* e seleziona <kbd>Add Component</kbd>)
e aggiungi una forma *Sphere* che copra l'immagine (fai clic con il pulsante destro sul componente e seleziona <kbd>Add Shape</kbd>).
6. Usa *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) e *Scale Tool* affinché la sfera copra l'immagine della moneta.
7. Imposta *Type* dell'oggetto di collisione su "Kinematic", *Group* su "pickup" e *Mask* su "hero".
8. Apri *hero.go* e aggiungi "pickup" alla proprietà *Mask* del componente *Collision Object*, poi salva il file.
9. Crea un nuovo file di script *coin.script* (fai clic con il pulsante destro su *level* nel *pannello Assets* e seleziona <kbd>New ▸ Script File</kbd>). Sostituisci il codice del modello con quanto segue:

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Aggiungi il file di script come componente *Script* all'oggetto della moneta (fai clic con il pulsante destro sulla radice in *Outline* e seleziona <kbd>Add Component from File</kbd>).

    ![Oggetto di gioco della moneta](images/runner/3/coin.png)

Vogliamo generare le monete dagli oggetti delle piattaforme, quindi aggiungi le fabbriche per le monete a *platform.go* e *platform_long.go*.

1. Apri *platform.go* e aggiungi un componente *Factory* (fai clic con il pulsante destro in *Outline* e seleziona <kbd>Add Component</kbd>).
2. Imposta *Id* della *Factory* su "coin_factory" e *Prototype* sul file *coin.go*.
3. Ora apri *platform_long.go* e crea un componente *Factory* identico.
4. Salva i due file.

![Fabbrica delle monete](images/runner/3/coin_factory.png)

Ora dobbiamo modificare *platform.script* affinché generi ed elimini le monete:

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Default speed in pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Impostando la piattaforma come genitore della moneta generata, la moneta si muoverà insieme alla piattaforma.
2. L'animazione fa oscillare le monete su e giù rispetto alla piattaforma, che ora è il loro genitore.

::: sidenote
Le relazioni genitore-figlio modificano esclusivamente il _grafo della scena_. Un figlio viene trasformato (spostato, ridimensionato o ruotato) insieme al suo genitore. Se ti servono ulteriori relazioni di "appartenenza" tra gli oggetti di gioco, devi tenerne traccia esplicitamente nel codice.
:::

L'ultimo passaggio di questo tutorial consiste nell'aggiungere un paio di righe a *controller.script*:

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. Il numero di monete da generare su una piattaforma normale.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Twice the number of coins on long platforms
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Inserire il codice del controller](images/runner/insert_controller_code.png)

Ora abbiamo un gioco semplice ma funzionante! Se sei arrivato fin qui, potresti voler continuare per conto tuo e aggiungere quanto segue:

1. Contatori del punteggio e delle vite
2. Effetti particellari per la raccolta degli oggetti e la morte
3. Belle immagini di sfondo

> Scarica la versione completa del progetto [qui](images/runner/sample-runner.zip).

Questo conclude il tutorial introduttivo. Ora continua a esplorare Defold. Abbiamo preparato molti [manuali e tutorial](//www.defold.com/learn) per guidarti e, se ti blocchi, sei il benvenuto sul [forum](//forum.defold.com).

Buon divertimento con Defold!
