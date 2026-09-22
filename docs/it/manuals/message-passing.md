---
title: Scambio di messaggi in Defold
brief: Lo scambio di messaggi è il meccanismo usato da Defold per consentire la comunicazione tra oggetti con poche dipendenze reciproche. Questo manuale descrive il meccanismo in dettaglio.
---

# Scambio di messaggi {#message-passing}

Lo scambio di messaggi è un meccanismo che consente agli oggetti di gioco (game object) di Defold di comunicare tra loro. Questo manuale presuppone una conoscenza di base del [meccanismo di indirizzamento](/manuals/addressing) e degli [elementi fondamentali](/manuals/building-blocks) di Defold.

Defold non adotta un approccio orientato agli oggetti in cui definisci l'applicazione creando gerarchie di classi con ereditarietà e funzioni membro negli oggetti (come in Java, C++ o C#). Defold estende invece Lua con un modello orientato agli oggetti semplice e potente, in cui lo stato degli oggetti viene mantenuto all'interno dei componenti script ed è accessibile tramite il riferimento `self`. Inoltre, gli oggetti possono essere completamente disaccoppiati usando lo scambio asincrono di messaggi come mezzo di comunicazione.


## Esempi di utilizzo {#usage-examples}

Vediamo innanzitutto alcuni semplici esempi di utilizzo. Supponi di creare un gioco composto da:

1. Una collezione (collection) principale di bootstrap contenente un oggetto di gioco con un componente GUI (la GUI è composta da una minimappa e un contatore del punteggio). È presente anche una collezione con ID "level".
2. La collezione denominata "level" contiene due oggetti di gioco: un eroe controllato dal giocatore e un nemico.

![Struttura dello scambio di messaggi](images/message_passing/message_passing_structure.png)

::: sidenote
Il contenuto di questo esempio si trova in due file separati. Un file contiene la collezione principale di bootstrap e l'altro la collezione con ID "level". Tuttavia, in Defold i nomi dei file _non contano_. Conta l'identità che assegni alle istanze.
:::

Il gioco contiene alcune semplici meccaniche che richiedono la comunicazione tra gli oggetti:

![Scambio di messaggi](images/message_passing/message_passing.png)

① L’eroe colpisce il nemico con un pugno
: Come parte di questa meccanica, il componente script di "hero" invia un messaggio `"punch"` al componente script di "enemy". Poiché entrambi gli oggetti si trovano nella stessa posizione nella gerarchia delle collezioni, è preferibile usare un indirizzo relativo:

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Nel gioco esiste un solo tipo di pugno, con una forza fissa, quindi il messaggio non deve contenere altre informazioni oltre al suo nome, "punch".

  Nel componente script del nemico, crea una funzione per ricevere il messaggio:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  In questo caso, il codice controlla soltanto il nome del messaggio (inviato come stringa sottoposta a hash nel parametro `message_id`). Il codice non tiene conto né dei dati del messaggio né del mittente---*chiunque* invii il messaggio "punch" infliggerà danni al povero nemico.

② L’eroe guadagna punti
: Ogni volta che il giocatore sconfigge un nemico, il suo punteggio aumenta. Inoltre, il componente script dell’oggetto di gioco "hero" invia un messaggio `"update_score"` al componente "gui" dell’oggetto di gioco "interface".

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  In questo caso non è possibile scrivere un indirizzo relativo, poiché "interface" si trova alla radice della gerarchia dei nomi, mentre "hero" no. Il messaggio viene inviato al componente GUI, a cui è associato uno script che può reagire al messaggio di conseguenza. I messaggi possono essere scambiati liberamente tra script, script GUI e script di rendering.

  Il messaggio `"update_score"` è accompagnato dai dati del punteggio. I dati vengono passati come tabella Lua nel parametro `message`:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Posizione del nemico sulla minimappa
: Il giocatore dispone di una minimappa sullo schermo per individuare i nemici e seguirne gli spostamenti. Ogni nemico è responsabile di segnalare la propria posizione inviando un messaggio `"update_minimap"` al componente "gui" dell’oggetto di gioco "interface":

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Il codice dello script GUI deve tenere traccia della posizione di ogni nemico e, se lo stesso nemico invia una nuova posizione, sostituire quella precedente. Il mittente del messaggio (passato nel parametro `sender`) può essere usato come chiave in una tabella Lua contenente le posizioni:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- update position on map
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- update the minimap with new positions
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Invio di messaggi {#sending-messages}

Il meccanismo di invio di un messaggio è, come abbiamo visto sopra, molto semplice. Chiami la funzione `msg.post()`, che inserisce il messaggio nella coda dei messaggi. Poi, a ogni frame, il motore scorre la coda e consegna ogni messaggio al relativo indirizzo di destinazione. Alcuni messaggi di sistema (come `"enable"`, `"disable"`, `"set_parent"` ecc.) vengono gestiti dal codice del motore. Il motore produce anche alcuni messaggi di sistema (come `"collision_response"` in caso di collisioni fisiche), che vengono consegnati ai tuoi oggetti. Per i messaggi definiti dall’utente inviati ai componenti script, il motore si limita a chiamare una funzione Lua speciale di Defold denominata `on_message()`.

Puoi inviare messaggi arbitrari a qualsiasi oggetto o componente esistente, e spetta al codice del destinatario rispondere al messaggio. Se invii un messaggio a un componente script e il codice dello script lo ignora, non c’è alcun problema. La responsabilità di gestire i messaggi ricade interamente sul destinatario.

Il motore controlla l’indirizzo di destinazione del messaggio. Se provi a inviare un messaggio a un destinatario sconosciuto, Defold segnala un errore nella console:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

La firma completa della chiamata a `msg.post()` è:

`msg.post(receiver, message_id, [message])`

receiver
: L’ID del componente o dell’oggetto di gioco destinatario. Se il destinatario è un oggetto di gioco, il messaggio viene inoltrato a tutti i suoi componenti.

message_id
: Una stringa o una stringa sottoposta a hash contenente il nome del messaggio.

[message]
: Una tabella Lua facoltativa contenente i dati del messaggio sotto forma di coppie chiave-valore. La tabella Lua del messaggio può contenere quasi qualsiasi tipo di dato. Puoi passare numeri, stringhe, valori booleani, URL, hash e tabelle annidate. Non puoi passare funzioni.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
La dimensione della tabella del parametro `message` ha un limite fisso di 2 kilobyte. Attualmente non esiste un modo semplice per determinare l’esatta quantità di memoria occupata da una tabella, ma puoi usare `collectgarbage("count")` prima e dopo l’inserimento della tabella per monitorare l’uso della memoria.
:::

### Forme abbreviate {#shorthands}

Defold offre due comode forme abbreviate per inviare messaggi senza specificare un URL completo:

:[Shorthands](../shared/url-shorthands.md)


## Ricezione di messaggi {#receiving-messages}

Per ricevere messaggi, assicurati che il componente script destinatario contenga una funzione denominata `on_message()`. La funzione accetta quattro parametri:

`function on_message(self, message_id, message, sender)`

`self`
: Un riferimento al componente script stesso.

`message_id`
: Contiene il nome del messaggio. Il nome è _sottoposto a hash_.

`message`
: Contiene i dati del messaggio sotto forma di tabella Lua. Se non ci sono dati, la tabella è vuota.

`sender`
: Contiene l’URL completo del mittente.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Scambio di messaggi tra mondi di gioco {#messaging-between-game-worlds}

Se usi un componente proxy di collezione (collection proxy) per caricare un nuovo mondo di gioco nel runtime, ti servirà scambiare messaggi tra i mondi di gioco. Supponi di aver caricato una collezione tramite un proxy e che la sua proprietà *Name* sia impostata su "level":

![Nome della collezione](images/message_passing/collection_name.png)

Non appena la collezione è stata caricata, inizializzata e abilitata, puoi inviare messaggi a qualsiasi componente o oggetto del nuovo mondo specificando il nome del mondo di gioco nel campo "socket" dell’indirizzo del destinatario:

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```
Una descrizione più approfondita del funzionamento dei proxy si trova nella documentazione dei [proxy di collezione](/manuals/collection-proxy).

## Catene di messaggi {#message-chains}

Quando un messaggio inviato viene infine consegnato, viene chiamata la funzione `on_message()` dei destinatari. Spesso il codice eseguito in risposta invia nuovi messaggi, che vengono aggiunti alla coda dei messaggi.

Quando il motore inizia a consegnare i messaggi, scorre la coda e chiama la funzione `on_message()` di ogni destinatario, proseguendo finché la coda non è vuota. Se durante un passaggio di consegna vengono aggiunti nuovi messaggi alla coda, il motore esegue un altro passaggio. Esiste però un limite fisso al numero di tentativi che il motore compie per svuotare la coda. Questo limita la lunghezza delle catene di messaggi che possono essere consegnate interamente in un singolo frame. Con lo script seguente puoi verificare facilmente quanti passaggi di consegna esegue il motore tra una chiamata a `update()` e la successiva:

```lua
function init(self)
    -- We’re starting a long message chain during object init
    -- and keeps it running through a number of update() steps.
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

L’esecuzione di questo script stampa un output simile al seguente:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Si vede che questa specifica versione del motore Defold esegue 10 passaggi di consegna sulla coda dei messaggi tra `init()` e la prima chiamata a `update()`. Esegue poi 75 passaggi durante ogni ciclo di aggiornamento successivo.
