---
title: Manuale del componente fabbrica
brief: Questo manuale spiega come usare i componenti fabbrica per generare dinamicamente oggetti di gioco durante l'esecuzione.
---

# Componenti fabbrica {#factory-components}

I componenti fabbrica (factory) permettono di generare dinamicamente oggetti di gioco da un pool di oggetti in un gioco in esecuzione.

Quando aggiungi un componente fabbrica a un oggetto di gioco, specifichi nella proprietà *Prototype* quale file di oggetto di gioco la fabbrica deve usare come prototipo (chiamato anche "prefab" o "blueprint" in altri motori) per tutti i nuovi oggetti di gioco che crea.

![Componente fabbrica](images/factory/factory_collection.png)

![Componente fabbrica](images/factory/factory_component.png)

Per avviare la creazione di un oggetto di gioco, chiama `factory.create()`:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Oggetto di gioco generato](images/factory/factory_spawned.png)

`factory.create()` accetta 5 parametri:

`url`
: L'ID del componente fabbrica che deve generare un nuovo oggetto di gioco.

`[position]`
: (facoltativo) La posizione del nuovo oggetto di gioco nello spazio globale. Deve essere un `vector3`. Se non specifichi una posizione, l'oggetto di gioco viene generato nella posizione dell'oggetto di gioco che chiama `factory.create()`.

`[rotation]`
: (facoltativo) La rotazione del nuovo oggetto di gioco nello spazio globale. Deve essere un `quat`.

`[properties]`
: (facoltativo) Una tabella Lua con gli eventuali valori delle proprietà dello script con cui inizializzare l'oggetto di gioco. Consulta il [manuale delle proprietà degli script](/manuals/script-properties) per informazioni sulle proprietà degli script.

`[scale]`
: (facoltativo) La scala dell'oggetto di gioco generato. La scala può essere espressa come un `number` (maggiore di 0) che specifica un ridimensionamento uniforme lungo tutti gli assi. Puoi anche fornire un `vector3` in cui ciascuna componente specifica il ridimensionamento lungo l'asse corrispondente.

Per esempio:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Spawn with no rotation but double scale.
-- Set the score of the star to 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Imposta la proprietà "score" dell'oggetto di gioco della stella.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. La proprietà dello script "score" viene definita con un valore predefinito.
2. Accedi alla proprietà dello script "score" come valore memorizzato in "self".

![Oggetto di gioco generato con proprietà e ridimensionamento](images/factory/factory_spawned2.png)

::: sidenote
Defold attualmente non supporta il ridimensionamento non uniforme delle forme di collisione. Se fornisci un valore di scala non uniforme, per esempio `vmath.vector3(1.0, 2.0, 1.0)`, lo sprite verrà ridimensionato correttamente, ma le forme di collisione no.
:::


## Indirizzamento degli oggetti creati da una fabbrica {#addressing-of-factory-created-objects}

Il meccanismo di indirizzamento di Defold permette di accedere a ogni oggetto e componente in un gioco in esecuzione. Il [manuale dell'indirizzamento](/manuals/addressing/) spiega in dettaglio il funzionamento del sistema. Puoi usare lo stesso meccanismo di indirizzamento per gli oggetti di gioco generati e i loro componenti. Spesso basta usare l'ID dell'oggetto generato, per esempio quando invii un messaggio:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
Inviare un messaggio all'oggetto di gioco stesso invece che a un componente specifico comporta l'invio del messaggio a tutti i componenti. In genere questo non è un problema, ma tienilo presente se l'oggetto ha molti componenti.
:::

Come puoi accedere a un componente specifico di un oggetto di gioco generato, per esempio per disattivare un oggetto di collisione o cambiare l'immagine di uno sprite? La soluzione è costruire un URL a partire dall'ID dell'oggetto di gioco e dall'ID del componente.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Tenere traccia degli oggetti generati e dei loro genitori {#tracking-spawned-and-parent-objects}

Quando chiami `factory.create()`, ottieni l'ID del nuovo oggetto di gioco e puoi memorizzarlo per farvi riferimento in seguito. Un uso comune consiste nel generare oggetti e aggiungere i loro ID a una tabella per poterli eliminare tutti in un secondo momento, per esempio quando ripristini la disposizione degli oggetti di un livello:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Spawn a coin and store it in the "coins" table.
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

E poi, in un secondo momento:

```lua
-- spawner.script
-- Delete all spawned coins.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- or alternatively
go.delete(self.spawned_coins)
```

Spesso serve anche che l'oggetto generato conosca l'oggetto di gioco che lo ha generato. Un esempio è un tipo di oggetto autonomo di cui può esistere una sola istanza generata alla volta. L'oggetto generato deve quindi avvisare il generatore quando viene eliminato o disattivato, in modo che se ne possa generare un altro:

```lua
-- spawner.script
-- Spawn a drone and set its parent to the url of this script component
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

E la logica dell'oggetto generato:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- I'm dead.
    msg.post(self.parent, "drone_dead")
end
```

## Caricamento dinamico delle risorse della fabbrica {#dynamic-loading-of-factory-resources}

Selezionando la casella *Load Dynamically* nelle proprietà della fabbrica, il motore rimanda il caricamento delle risorse associate alla fabbrica.

![Caricamento dinamico](images/factory/load_dynamically.png)

Con la casella deselezionata, il motore carica le risorse del prototipo quando viene caricato il componente fabbrica, rendendole subito disponibili per generare oggetti.

Con la casella selezionata, hai due possibilità:

Caricamento sincrono
: Chiama [`factory.create()`](/ref/factory/#factory.create) quando vuoi generare oggetti. Le risorse verranno caricate in modo sincrono, il che potrebbe causare un breve rallentamento, e poi verranno generate nuove istanze.

  ```lua
  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling create without having called
      -- load will create the resources synchronously.
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the factory component
      -- holds no reference.
      go.delete(self.go_id)

      -- Calling unload will do nothing since factory holds no references
      factory.unload("#factory")
  end
  ```

Caricamento asincrono
: Chiama [`factory.load()`](/ref/factory/#factory.load) per caricare esplicitamente le risorse in modo asincrono. Quando le risorse sono pronte per generare oggetti, viene invocata una callback.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_id = factory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling load will load the resources.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the factory component
      -- still holds a reference.
      go.delete(self.go_id)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      factory.unload("#factory")
  end
  ```

## Prototipo dinamico {#dynamic-prototype}

Puoi cambiare il *Prototype* che una fabbrica può creare selezionando la casella *Dynamic Prototype* nelle proprietà della fabbrica.

![Prototipo dinamico](images/factory/dynamic_prototype.png)

Quando l'opzione *Dynamic Prototype* è selezionata, il componente fabbrica può cambiare prototipo usando la funzione `factory.set_prototype()`. Esempio:

```lua
factory.unload("#factory") -- unload the previous resources
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Quando l'opzione *Dynamic Prototype* è attiva, il numero di componenti della collezione non può essere ottimizzato e la collezione che contiene la fabbrica userà i conteggi predefiniti dei componenti del file *game.project*.
:::


## Limiti delle istanze {#instance-limits}

L'impostazione di progetto *Max Instances* nella sezione *Collection* è il limite massimo al numero di oggetti di gioco in ciascuna collezione (mondo). Durante la build, Defold può allocare una capacità inferiore quando può stabilire che ciò è sicuro. Tutti gli oggetti di gioco che esistono contemporaneamente in un mondo concorrono al raggiungimento della capacità, sia che siano stati inseriti nell'editor sia che siano stati generati durante l'esecuzione.

![Numero massimo di istanze](images/factory/factory_max_instances.png)

L'allocazione effettiva dipende dall'analisi svolta durante la build:

* Quando la build può determinare un numero fisso di oggetti di gioco (in genere quando la collezione non contiene fabbriche né fabbriche di collezioni (collection factory)), la capacità corrisponde al numero determinato in fase di compilazione, con un limite massimo di *Max Instances*.
* Una collezione che contiene una fabbrica o una fabbrica di collezioni usa *Max Instances* come capacità per gli oggetti di gioco. Per un prototipo referenziato staticamente, la build identifica i tipi di componenti che la fabbrica può generare. Questi tipi usano i rispettivi conteggi massimi impostati nel progetto, mentre i tipi di componenti non interessati possono ancora usare conteggi esatti.
* Attivare *Dynamic Prototype* disabilita l'analisi del numero di componenti per la collezione che contiene la fabbrica, che quindi usa *Max Instances* e i conteggi massimi configurati per ciascun tipo di componente.

Imposta *Max Instances* in base al maggior numero di oggetti di gioco che possono esistere contemporaneamente in un mondo dinamico. Consulta [Ottimizzazioni del numero massimo di componenti](/manuals/project-settings/#component-max-count-optimizations) per sapere come vengono calcolati gli altri limiti dei componenti.

## Riutilizzo degli oggetti di gioco tramite pool {#pooling-of-game-objects}

Può sembrare una buona idea conservare gli oggetti di gioco generati in un pool e riutilizzarli. Tuttavia, il motore gestisce già internamente un pool di oggetti, quindi il lavoro aggiuntivo causerebbe solo rallentamenti. Eliminare gli oggetti di gioco e generarne di nuovi è più veloce e più semplice.
