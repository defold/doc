---
title: Proprietà dei componenti script
brief: Questo manuale spiega come aggiungere proprietà personalizzate ai componenti script e accedervi dall'editor e dagli script durante l'esecuzione.
---

# Proprietà degli script {#script-properties}

Le proprietà degli script offrono un modo semplice e potente per definire ed esporre proprietà personalizzate per una specifica istanza di un oggetto di gioco (game object). Puoi modificarle per singole istanze direttamente nell'editor e usarne i valori nel codice per cambiare il comportamento di un oggetto di gioco. Le proprietà degli script sono molto utili in numerosi casi:

* Quando vuoi sovrascrivere i valori per singole istanze nell'editor, aumentando così la riutilizzabilità degli script.
* Quando vuoi generare un oggetto di gioco con valori iniziali.
* Quando vuoi animare i valori di una proprietà.
* Quando vuoi accedere ai dati di stato di uno script da un altro. (Tieni presente che, se accedi spesso alle proprietà tra oggetti diversi, potrebbe essere meglio spostare i dati in uno spazio di archiviazione condiviso.)

Tra i casi d'uso comuni ci sono l'impostazione della vita o della velocità di uno specifico nemico controllato dall'IA, della tinta di un oggetto da raccogliere, dell'atlas di uno sprite oppure del messaggio che un oggetto pulsante deve inviare quando viene premuto---e/o della sua destinazione.

## Definire una proprietà di uno script {#defining-a-script-property}

Per aggiungere proprietà a un componente script, definiscile con la funzione speciale `go.property()`. La funzione deve essere usata al livello principale dello script---al di fuori delle funzioni del ciclo di vita come `init()` e `update()`. Il valore predefinito fornito per la proprietà ne determina il tipo: `number`, `boolean`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` e `resource` (vedi sotto).

::: important
Tieni presente che è possibile risalire alla stringa di un valore hash solo nelle build di debug, per facilitare il debug. Nelle build di release, la stringa corrispondente non è disponibile, quindi usare `tostring()` su un valore `hash` per estrarne la stringa non ha senso.
:::


```lua
-- can.script
-- Define script properties for health and an attack target
go.property("health", 100)
go.property("target", msg.url())

function init(self)
  -- store initial position of target.
  -- self.target is a url referencing another object.
  self.target_pos = go.get_position(self.target)
  ...
end

function on_message(self, message_id, message, sender)
  if message_id == hash("take_damage") then
    -- decrease the health property
    self.health = self.health - message.damage
    if self.health <= 0 then
      go.delete()
    end
  end
end
```

Puoi quindi impostare i valori delle proprietà di qualsiasi istanza di componente script creata da questo script.

![Componente con proprietà](images/script-properties/component.png)

 Seleziona il componente script nella vista *Outline* dell'editor: le proprietà compaiono nella vista *Properties*, dove puoi modificarle:

![Proprietà](images/script-properties/properties.png)

Ogni proprietà sovrascritta con un nuovo valore specifico dell'istanza viene evidenziata in blu. Fai clic sul pulsante di ripristino accanto al nome della proprietà per tornare al valore predefinito (impostato nello script).


::: important
Le proprietà degli script vengono analizzate durante la build del progetto. Le espressioni che definiscono i valori non vengono valutate. Questo significa che un'istruzione come `go.property("hp", 3+6)` non funziona, mentre `go.property("hp", 9)` sì.
:::

## Accedere alle proprietà degli script {#accessing-script-properties}

Ogni proprietà definita nello script è disponibile come membro di `self`, il riferimento all'istanza dello script:

```lua
-- my_script.script
go.property("my_property", 1)

function update(self, dt)
  -- Read and write the property
  if self.my_property == 1 then
      self.my_property = 3
  end
end
```

Puoi accedere alle proprietà degli script definite dall'utente anche tramite le funzioni `get`, `set` e `animate`, come per qualsiasi altra proprietà:

```lua
-- another.script

-- increase "my_property" in "myobject#script" by 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animate "my_property" in "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Oggetti creati da una fabbrica {#factory-created-objects}

Se usi una fabbrica (factory) per creare l'oggetto di gioco, puoi impostare le proprietà degli script al momento della creazione:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accessing factory-created script properties
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Quando generi una gerarchia di oggetti di gioco tramite `collectionfactory.create()`, devi associare gli ID degli oggetti alle tabelle delle proprietà. Queste associazioni vengono raccolte in una tabella e passate alla funzione `create()`:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

I valori delle proprietà forniti tramite `factory.create()` e `collectionfactory.create()` sovrascrivono sia i valori impostati nel file del prototipo sia quelli predefiniti nello script.

Se più componenti script associati a un oggetto di gioco definiscono la stessa proprietà, ogni componente viene inizializzato con il valore fornito a `factory.create()` o `collectionfactory.create()`.


## Proprietà di tipo risorsa {#resource-properties}

Le proprietà di tipo risorsa si definiscono come le proprietà degli script per i tipi di dati di base:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Quando definisci una proprietà di tipo risorsa, questa compare nella vista *Properties* come qualsiasi altra proprietà dello script, ma sotto forma di campo per la selezione di un file o di una risorsa:

![Proprietà di tipo risorsa](images/script-properties/resource-properties.png)

Puoi accedere alle proprietà di tipo risorsa con `go.get()` o tramite il riferimento all'istanza dello script `self`, e usarle con `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
