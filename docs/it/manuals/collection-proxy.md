---
title: Manuale dei proxy di collezione
brief: Questo manuale spiega come creare dinamicamente nuovi mondi di gioco e passare da uno all'altro.
---

# Proxy di collezione {#collection-proxy}

Il componente proxy di collezione (collection proxy) permette di caricare e scaricare dinamicamente nuovi "mondi" di gioco a partire dal contenuto di un file di collezione. Puoi usarlo per passare da un livello di gioco all'altro o da una schermata GUI all'altra, caricare e scaricare "scene" narrative nel corso di un livello, caricare e scaricare minigiochi e altro ancora.

Defold organizza tutti gli oggetti di gioco in collezioni. Una collezione può contenere oggetti di gioco e altre collezioni (cioè sottocollezioni). I proxy di collezione ti permettono di suddividere i contenuti in collezioni separate e di gestirne dinamicamente il caricamento e lo scaricamento tramite script.

I proxy di collezione si distinguono dai [componenti fabbrica di collezioni (collection factory)](/manuals/collection-factory/). Una fabbrica di collezioni istanzia il contenuto di una collezione nel mondo di gioco corrente. I proxy di collezione creano un nuovo mondo di gioco durante l'esecuzione e hanno quindi casi d'uso diversi.

## Creare un componente proxy di collezione {#creating-a-collection-proxy-component}

1. Aggiungi un componente proxy di collezione a un oggetto di gioco facendo <kbd>clic con il pulsante destro</kbd> sull'oggetto e selezionando <kbd>Add Component ▸ Collection Proxy</kbd> dal menu contestuale.

2. Imposta la proprietà *Collection* in modo che faccia riferimento a una collezione da caricare dinamicamente nel runtime in un secondo momento. Si tratta di una dipendenza statica definita in fase di build: la collezione a cui si fa riferimento e le sue dipendenze vengono compilate. Se *Exclude* non è selezionato, vengono incluse nel bundle principale. Quando *Exclude* è selezionato, le risorse a cui si fa riferimento soltanto tramite proxy esclusi possono essere omesse dal bundle principale per Live Update, e il proxy non caricato può essere reindirizzato a un'altra collezione compilata durante l'esecuzione, come descritto di seguito.

![aggiunta di un componente proxy](images/collection-proxy/create_proxy.png)

(Puoi escludere il contenuto dalla build e scaricarlo tramite codice selezionando la casella *Exclude* e usando la [funzionalità Live Update](/manuals/live-update/).)

## Bootstrap

All'avvio, il motore Defold carica e istanzia nel runtime tutti gli oggetti di gioco di una *collezione di bootstrap*. Poi inizializza e abilita gli oggetti di gioco e i loro componenti. La collezione di bootstrap da utilizzare viene specificata nelle [impostazioni del progetto](/manuals/project-settings/#main-collection). Per convenzione, questo file di collezione è solitamente denominato `main.collection`.

![bootstrap](images/collection-proxy/bootstrap.png)

Per ospitare gli oggetti di gioco e i loro componenti, il motore alloca la memoria necessaria per l'intero "mondo di gioco" in cui viene istanziato il contenuto della collezione di bootstrap. Viene inoltre creato un mondo fisico separato per gli oggetti di collisione e la simulazione fisica.

Poiché i componenti script devono poter indirizzare tutti gli oggetti del gioco, anche dall'esterno del mondo di bootstrap, a questo mondo viene assegnato un nome univoco: la proprietà *Name* impostata nel file di collezione:

![bootstrap](images/collection-proxy/collection_id.png)

Se la collezione caricata contiene componenti proxy di collezione, le collezioni a cui questi fanno riferimento *non* vengono caricate automaticamente. Devi controllare il caricamento di queste risorse tramite script.

## Caricare una collezione {#loading-a-collection}

Per caricare dinamicamente una collezione tramite un proxy, invia da uno script un messaggio chiamato `"load"` al componente proxy:

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![caricamento](images/collection-proxy/proxy_load.png)

Il componente proxy indica al motore di allocare lo spazio per un nuovo mondo. Viene inoltre creato un mondo fisico separato a runtime e vengono istanziati tutti gli oggetti di gioco della collezione "`mylevel.collection`".

Il nome del nuovo mondo deriva dalla proprietà *Name* nel file di collezione, che in questo esempio è impostata su "`mylevel`". Il nome deve essere univoco. Se il valore di *Name* impostato nel file di collezione è già utilizzato da un mondo caricato, il motore segnala un errore di conflitto tra nomi:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Quando il motore ha terminato di caricare la collezione, il componente proxy di collezione invia un messaggio chiamato `"proxy_loaded"` allo script che ha inviato il messaggio `"load"`. Lo script può quindi inizializzare e abilitare la collezione in risposta al messaggio:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Questo messaggio indica al componente proxy di collezione di iniziare a caricare la propria collezione in un nuovo mondo. Al termine, il proxy risponde con un messaggio chiamato `"proxy_loaded"`.

`"async_load"`
: Questo messaggio indica al componente proxy di collezione di iniziare a caricare in background la propria collezione in un nuovo mondo. Al termine, il proxy risponde con un messaggio chiamato `"proxy_loaded"`.

`"init"`
: Questo messaggio indica al componente proxy di collezione di inizializzare tutti gli oggetti di gioco e i componenti istanziati. In questa fase vengono chiamate tutte le funzioni `init()` degli script.

`"enable"`
: Questo messaggio indica al componente proxy di collezione di abilitare tutti gli oggetti di gioco e i componenti. Per esempio, tutti i componenti sprite iniziano a essere disegnati quando vengono abilitati.

## Cambiare la collezione di un proxy escluso {#changing-an-excluded-proxys-collection}

[`collectionproxy.set_collection()`](/ref/collectionproxy/#collectionproxy.set_collection) può reindirizzare un proxy escluso e non caricato a una collezione compilata: questa funzione è utile dopo aver montato un pacchetto Live Update. Il proxy deve avere *Exclude* selezionato e non deve essere caricato né in fase di caricamento. Il percorso deve terminare con `.collectionc`. La collezione e tutte le sue dipendenze devono essere disponibili nel sistema delle risorse quando il proxy viene caricato.

Controlla il valore restituito prima di caricare il proxy. Inizializza e abilita il nuovo mondo solo dopo aver ricevuto `proxy_loaded`:

```lua
local function load_mounted_level()
    local ok, result = collectionproxy.set_collection(
        "#level_proxy",
        "/level_pack/level_3.collectionc"
    )

    if ok then
        msg.post("#level_proxy", "load")
    else
        print("Unable to change proxy collection", result)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

Chiama `collectionproxy.set_collection("#level_proxy", nil)` quando il proxy non è caricato né in fase di caricamento per ripristinare la collezione assegnata nell'editor. Consulta il [manuale degli script di Live Update](/manuals/live-update-scripting/) per scaricare e montare i contenuti e il riferimento API per i codici di errore `collectionproxy.RESULT_*`.

## Indirizzare oggetti nel nuovo mondo {#addressing-into-the-new-world}

Il valore di *Name* impostato nelle proprietà del file di collezione viene utilizzato per indirizzare gli oggetti di gioco e i componenti nel mondo caricato. Per esempio, se crei un oggetto di caricamento nella collezione di bootstrap, potresti dover comunicare con esso da qualsiasi collezione caricata:

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![caricamento](images/collection-proxy/message_passing.png)

Se invece devi comunicare dall'oggetto di caricamento con un oggetto di gioco nella collezione caricata, puoi inviare un messaggio usando l'[URL completo dell'oggetto](/manuals/addressing/#urls):

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
Non è possibile accedere direttamente agli oggetti di gioco di una collezione caricata dall'esterno della collezione:

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Scaricare un mondo {#unloading-a-world}

Per scaricare una collezione caricata, invia i messaggi corrispondenti alle operazioni inverse del caricamento:

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Questo messaggio indica al componente proxy di collezione di disabilitare tutti gli oggetti di gioco e i componenti nel mondo. In questa fase gli sprite smettono di essere renderizzati.

`"final"`
: Questo messaggio indica al componente proxy di collezione di finalizzare tutti gli oggetti di gioco e i componenti nel mondo. In questa fase vengono chiamate le funzioni `final()` di tutti gli script.

`"unload"`
: Questo messaggio indica al proxy di collezione di rimuovere completamente il mondo dalla memoria.

Se non hai bisogno di un controllo così dettagliato, puoi inviare direttamente il messaggio `"unload"` senza prima disabilitare e finalizzare la collezione. Il proxy disabilita e finalizza automaticamente la collezione prima di scaricarla.

Quando il proxy di collezione ha terminato di scaricare la collezione, invia un messaggio `"proxy_unloaded"` allo script che ha inviato il messaggio `"unload"`:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## Passo temporale {#time-step}

Puoi modificare la velocità degli aggiornamenti di un proxy di collezione cambiando il _passo temporale_. Questo significa che, anche se il gioco avanza a 60 FPS costanti, un proxy può aggiornarsi a una velocità maggiore o minore, influenzando aspetti quali:

* Velocità della simulazione fisica
* Il valore di `dt` passato a `update()`
* [Animazioni delle proprietà degli oggetti di gioco e della GUI](https://defold.com/manuals/animation/#property-animation-1)
* [Animazioni flipbook](https://defold.com/manuals/animation/#flip-book-animation)
* [Simulazioni degli effetti particellari](https://defold.com/manuals/particlefx/)
* Velocità dei timer

Puoi anche impostare la modalità di aggiornamento, che permette di controllare se la variazione di velocità deve essere applicata in modo discreto (sensato soltanto con un fattore di scala inferiore a 1.0) o continuo.

Per controllare il fattore di scala e la modalità di applicazione, invia al proxy un messaggio `set_time_step`:

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Per vedere cosa succede quando cambia il passo temporale, puoi creare un oggetto con il seguente codice in un componente script e inserirlo nella collezione di cui stai modificando il passo temporale:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Con un passo temporale di 0.2, ottieni il seguente risultato nella console:

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` viene ancora chiamata 60 volte al secondo, ma il valore di `dt` cambia. Solo 1/5 (0.2) delle chiamate a `update()` ha un valore di `dt` pari a 1/60 (corrispondente a 60 FPS)---nelle altre è zero. Anche tutte le simulazioni fisiche vengono aggiornate in base a questo `dt` e avanzano soltanto in un quinto dei fotogrammi.

::: sidenote
Puoi usare il passo temporale della collezione per mettere in pausa il gioco, per esempio mentre mostri una finestra popup o quando la finestra ha perso il focus. Usa `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` per mettere in pausa e `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` per riprendere.
:::

Consulta [`set_time_step`](/ref/collectionproxy#set_time_step) per maggiori dettagli.

## Limitazioni e problemi comuni {#caveats-and-common-issues}

Fisica
: Tramite i proxy di collezione è possibile caricare nel motore più di una collezione di primo livello, o *mondo di gioco*. In questo caso, è importante sapere che ogni collezione di primo livello è un mondo fisico separato. Le interazioni fisiche (collisioni, trigger, ray cast) avvengono soltanto tra oggetti appartenenti allo stesso mondo. Quindi, anche se gli oggetti di collisione di due mondi appaiono perfettamente sovrapposti, non può esserci alcuna interazione fisica tra loro.

Memoria
: Ogni collezione caricata crea un nuovo mondo di gioco, che occupa una quantità di memoria relativamente elevata. Se carichi decine di collezioni contemporaneamente tramite proxy, potrebbe essere opportuno ripensare la struttura del gioco. Per generare molte istanze di gerarchie di oggetti di gioco, sono più adatte le [fabbriche di collezioni](/manuals/collection-factory).

Input
: Se nella collezione caricata ci sono oggetti che richiedono azioni di input, devi assicurarti che l'oggetto di gioco contenente il proxy di collezione acquisisca l'input. Quando l'oggetto di gioco riceve messaggi di input, questi vengono propagati ai suoi componenti, cioè ai proxy di collezione. Le azioni di input vengono inviate alla collezione caricata tramite il proxy.
