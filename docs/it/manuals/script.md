---
title: Scrivere la logica di gioco negli script
brief: Questo manuale descrive come aggiungere la logica di gioco usando i componenti script.
---

# Script {#scripts}

I componenti script consentono di creare la logica di gioco usando il [linguaggio di programmazione Lua](/manuals/lua).


## Tipi di script {#script-types}

In Defold esistono tre tipi di script Lua, ciascuno con accesso a un diverso insieme di librerie Defold.

Script degli oggetti di gioco
: Estensione _.script_. Questi script vengono aggiunti agli oggetti di gioco esattamente come qualsiasi altro [componente](/manuals/components) e Defold ne esegue il codice Lua nelle funzioni del ciclo di vita del motore. Gli script degli oggetti di gioco vengono solitamente usati per controllare gli oggetti di gioco e la logica che coordina il gioco, dal caricamento dei livelli alle regole di gioco e così via. Gli script degli oggetti di gioco hanno accesso alle funzioni [GO](/ref/go) e a tutte le funzioni delle librerie Defold, tranne quelle di [GUI](/ref/gui) e [Render](/ref/render).


Script GUI
: Estensione _.gui_script_. Vengono eseguiti dai componenti GUI e di solito contengono la logica necessaria per visualizzare elementi della GUI come pannelli informativi in sovrimpressione (HUD), menu e così via. Defold esegue il codice Lua nelle funzioni del ciclo di vita del motore. Gli script GUI hanno accesso alle funzioni [GUI](/ref/gui) e a tutte le funzioni delle librerie Defold, tranne quelle di [GO](/ref/go) e [Render](/ref/render).


Script di rendering
: Estensione _.render_script_. Vengono eseguiti dalla pipeline di rendering e contengono la logica necessaria per disegnare tutta la grafica dell’applicazione o del gioco a ogni fotogramma. Lo script di rendering occupa una posizione particolare nel ciclo di vita del gioco. Puoi trovare i dettagli nella [documentazione sul ciclo di vita dell’applicazione](/manuals/application-lifecycle). Gli script di rendering hanno accesso alle funzioni [Render](/ref/render) e a tutte le funzioni delle librerie Defold, tranne quelle di [GO](/ref/go) e [GUI](/ref/gui).


## Esecuzione degli script, callback e self {#script-execution-callbacks-and-self}

Defold esegue gli script Lua durante il ciclo di vita del motore e rende accessibili le sue fasi attraverso un insieme di funzioni di callback predefinite. Quando aggiungi un componente script a un oggetto di gioco, lo script entra a far parte del ciclo di vita dell’oggetto e dei suoi componenti. Lo script viene valutato nel contesto Lua al momento del caricamento, poi il motore esegue le seguenti funzioni passando come parametro un riferimento all’istanza corrente del componente script. Puoi usare questo riferimento `self` per memorizzare lo stato nell’istanza del componente.

::: important
`self` è un oggetto `userdata` che si comporta come una tabella Lua, ma non puoi iterarne gli elementi con `pairs()` o `ipairs()` né stamparlo usando `pprint()`.
:::

#### `init(self)`
Viene chiamata quando il componente viene inizializzato.

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Viene chiamata quando il componente viene eliminato. È utile per le operazioni di pulizia, per esempio se hai generato oggetti di gioco che devono essere eliminati insieme al componente.

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)`
Aggiornamento indipendente dalla frequenza dei fotogrammi. Il parametro `dt` contiene il tempo trascorso dall’ultimo aggiornamento. Questa funzione viene chiamata `0-N` volte in base alla durata del fotogramma e alla frequenza di aggiornamento fissa. Viene chiamata solo quando `Physics`-->`Use Fixed Timestep` è abilitato e `Engine`-->`Fixed Update Frequency` è maggiore di 0 in *game.project*. È utile quando vuoi manipolare oggetti fisici a intervalli regolari per ottenere una simulazione fisica stabile.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Viene chiamata una volta per fotogramma dopo la callback `fixed_update` di tutti gli script (se Fixed Timestep è abilitato). Il parametro `dt` contiene il tempo trascorso dall’ultimo fotogramma.

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)`
Viene chiamata una volta per fotogramma dopo la callback `update` di tutti gli script, ma subito prima del rendering. Il parametro `dt` contiene il tempo trascorso dall’ultimo fotogramma.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Quando vengono inviati messaggi al componente script tramite [`msg.post()`](/ref/msg#msg.post), il motore chiama questa funzione del componente ricevente. Scopri [di più sullo scambio di messaggi](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Se questo componente ha acquisito il focus dell’input (vedi [`acquire_input_focus`](/ref/go/#acquire_input_focus)), il motore chiama questa funzione quando viene rilevato un input. Scopri [di più sulla gestione dell’input](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Questa funzione viene chiamata quando lo script viene ricaricato tramite la funzione di hot reload dell’editor (<kbd>Edit ▸ Reload Resource</kbd>). È molto utile per il debug, i test e la messa a punto. Scopri [di più sull’hot reload](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## Logica reattiva {#reactive-logic}

Un oggetto di gioco con un componente script implementa una logica. Spesso questa logica dipende da un fattore esterno. L’IA di un nemico potrebbe reagire alla presenza del giocatore entro un certo raggio dal nemico; una porta potrebbe sbloccarsi e aprirsi in seguito a un’interazione del giocatore, e così via.

La funzione `update()` consente di implementare comportamenti complessi definiti come una macchina a stati eseguita a ogni fotogramma: a volte è l’approccio adatto. Tuttavia, ogni chiamata a `update()` ha un costo. A meno che la funzione non ti serva davvero, dovresti eliminarla e provare a costruire la logica _in modo reattivo_. Attendere passivamente un messaggio che attivi una risposta richiede meno risorse che interrogare attivamente il mondo di gioco alla ricerca di dati a cui reagire. Inoltre, affrontare un problema di progettazione in modo reattivo porta spesso a un progetto e a un’implementazione più chiari e stabili.

Vediamo un esempio concreto. Supponiamo che tu voglia far inviare a un componente script un messaggio 2 secondi dopo la sua inizializzazione. Il componente deve poi attendere un determinato messaggio di risposta e, una volta ricevuto, inviare un altro messaggio dopo 5 secondi. Il codice non reattivo per ottenere questo comportamento sarebbe simile al seguente:

```lua
function init(self)
    -- Counter to keep track of time.
    self.counter = 0
    -- We need this to keep track of our state.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- send message after 2 seconds
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- send message 5 seconds after we received "response"
        msg.post("another_object", "another_message")
        -- Nil the state so we don’t reach this state block again.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- “first” state done. enter next
        self.state = "second"
        -- zero the counter
        self.counter = 0
    end
end
```

Anche in questo caso piuttosto semplice, la logica risulta alquanto intricata. È possibile migliorarla usando le coroutine in un modulo (vedi sotto), ma proviamo invece a renderla reattiva usando un meccanismo di temporizzazione integrato.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Wait 2s then call send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Wait 5s then call send_second()
		timer.delay(5, false, send_second)
	end
end
```

Questo codice è più chiaro e facile da seguire. Eliminiamo le variabili di stato interne, di cui spesso è difficile seguire l’evoluzione nella logica e che possono causare errori difficili da individuare. Eliminiamo anche del tutto la funzione `update()`. In questo modo il motore non deve chiamare il nostro script 60 volte al secondo, anche quando è semplicemente in attesa.


## Preelaborazione {#preprocessing}

Puoi usare un preprocessore Lua e una sintassi speciale per includere codice in modo condizionale in base alla variante della build. Esempio:

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

Il preprocessore è disponibile come estensione di build. Per saperne di più su come installarlo e usarlo, consulta la [pagina dell’estensione su GitHub](https://github.com/defold/extension-lua-preprocessor).


## Supporto dell’editor {#editor-support}

L’editor Defold supporta la modifica degli script Lua con evidenziazione della sintassi e completamento automatico. Per completare i nomi delle funzioni Defold, premi *Ctrl+Space* per visualizzare un elenco delle funzioni che corrispondono a ciò che stai digitando.

![Completamento automatico](images/script/completion.png)
