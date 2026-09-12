---
title: Handbuch zu Fabrikkomponenten
brief: Dieses Handbuch erklärt, wie du Fabrikkomponenten verwendest, um Spielobjekte zur Laufzeit dynamisch zu erzeugen.
---

# Fabrikkomponenten {#factory-components}

Eine Fabrik (factory) ist eine Komponente (component), die Spielobjekte (game objects) aus einem Objektpool dynamisch in einem laufenden Spiel erzeugt.

Wenn du einem Spielobjekt eine Fabrikkomponente hinzufügst, legst du in der Eigenschaft *Prototype* fest, welche Spielobjektdatei die Fabrik als Prototyp (in anderen Engines auch als „Prefabs“ oder „Blueprints“ bekannt) für alle neuen Spielobjekte verwenden soll, die sie erzeugt.

![Fabrikkomponente](images/factory/factory_collection.png)

![Fabrikkomponente](images/factory/factory_component.png)

Rufe `factory.create()` auf, um die Erzeugung eines Spielobjekts auszulösen:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Dynamisch erzeugtes Spielobjekt](images/factory/factory_spawned.png)

`factory.create()` nimmt 5 Parameter entgegen:

`url`
: Der Bezeichner (ID) der Fabrikkomponente, die ein neues Spielobjekt erzeugen soll.

`[position]`
: (optional) Die Position des neuen Spielobjekts im Weltkoordinatensystem. Sie sollte als `vector3` angegeben werden. Wenn du keine Position angibst, wird das Spielobjekt an der Position des Spielobjekts erzeugt, das `factory.create()` aufruft.

`[rotation]`
: (optional) Die Drehung des neuen Spielobjekts im Weltkoordinatensystem. Sie sollte als `quat` angegeben werden.

`[properties]`
: (optional) Eine Lua-Tabelle mit beliebigen Werten für Skripteigenschaften, mit denen das Spielobjekt initialisiert werden soll. Informationen zu Skripteigenschaften findest du im [Handbuch zu Skripteigenschaften](/manuals/script-properties).

`[scale]`
: (optional) Die Skalierung des erzeugten Spielobjekts. Die Skalierung kann als Wert vom Typ `number` (größer als 0) angegeben werden, der eine gleichmäßige Skalierung entlang aller Achsen festlegt. Du kannst auch einen `vector3` angeben, bei dem jede Komponente die Skalierung entlang der entsprechenden Achse festlegt.

Zum Beispiel:

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Spawn with no rotation but double scale.
-- Set the score of the star to 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Legt die Eigenschaft „score“ des Stern-Spielobjekts fest.

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
1. Die Skripteigenschaft „score“ wird mit einem Standardwert definiert.
2. Greife auf die Skripteigenschaft „score“ als einen in „self“ gespeicherten Wert zu.

![Dynamisch erzeugtes Spielobjekt mit Eigenschaft und Skalierung](images/factory/factory_spawned2.png)

::: sidenote
Defold unterstützt derzeit keine ungleichmäßige Skalierung von Kollisionsformen. Wenn du einen ungleichmäßigen Skalierungswert angibst, zum Beispiel `vmath.vector3(1.0, 2.0, 1.0)`, wird das Sprite korrekt skaliert, die Kollisionsformen jedoch nicht.
:::


## Adressierung von Objekten, die eine Fabrik erzeugt hat {#addressing-of-factory-created-objects}

Mit dem Adressierungsmechanismus von Defold kannst du auf jedes Objekt und jede Komponente in einem laufenden Spiel zugreifen. Das [Handbuch zur Adressierung](/manuals/addressing/) erklärt ausführlich, wie das System funktioniert. Du kannst denselben Adressierungsmechanismus auch für dynamisch erzeugte Spielobjekte und deren Komponenten verwenden. Oft genügt die ID des erzeugten Objekts, zum Beispiel beim Senden einer Nachricht:

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
Wenn du eine Nachricht an das Spielobjekt selbst statt an eine bestimmte Komponente sendest, wird sie tatsächlich an alle Komponenten gesendet. Das ist normalerweise kein Problem, aber du solltest es im Hinterkopf behalten, wenn das Objekt viele Komponenten hat.
:::

Was aber, wenn du auf eine bestimmte Komponente eines erzeugten Spielobjekts zugreifen musst, zum Beispiel um ein Kollisionsobjekt zu deaktivieren oder das Bild eines Sprites zu ändern? Die Lösung besteht darin, eine URL aus der ID des Spielobjekts und der ID der Komponente zusammenzusetzen.

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


## Erzeugte und übergeordnete Objekte nachverfolgen {#tracking-spawned-and-parent-objects}

Wenn du `factory.create()` aufrufst, erhältst du die ID des neuen Spielobjekts zurück und kannst sie für spätere Zugriffe speichern. Häufig erzeugst du Objekte und fügst ihre IDs einer Tabelle hinzu, damit du sie später alle löschen kannst, zum Beispiel beim Zurücksetzen einer Level-Anordnung:

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Spawn a coin and store it in the "coins" table.
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

Und später:

```lua
-- spawner.script
-- Delete all spawned coins.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- or alternatively
go.delete(self.spawned_coins)
```

Häufig soll das erzeugte Objekt auch das Spielobjekt kennen, das es erzeugt hat. Ein Beispiel wäre ein autonomes Objekt, von dem jeweils nur eines erzeugt werden kann. Das erzeugte Objekt muss dann seinen Erzeuger benachrichtigen, wenn es gelöscht oder deaktiviert wird, damit ein weiteres erzeugt werden kann:

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

Und die Logik des erzeugten Objekts:

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- I'm dead.
    msg.post(self.parent, "drone_dead")
end
```

## Dynamisches Laden von Fabrikressourcen {#dynamic-loading-of-factory-resources}

Wenn du das Kontrollkästchen *Load Dynamically* in den Eigenschaften der Fabrik aktivierst, verschiebt die Engine das Laden der mit der Fabrik verknüpften Ressourcen auf einen späteren Zeitpunkt.

![Dynamisch laden](images/factory/load_dynamically.png)

Wenn das Kontrollkästchen deaktiviert ist, lädt die Engine die Prototypressourcen beim Laden der Fabrikkomponente, sodass sie sofort zum Erzeugen von Objekten bereitstehen.

Wenn das Kontrollkästchen aktiviert ist, hast du zwei Möglichkeiten:

Synchrones Laden
: Rufe [`factory.create()`](/ref/factory/#factory.create) auf, wenn du Objekte erzeugen möchtest. Dadurch werden die Ressourcen synchron geladen, was zu einem kurzen Ruckler führen kann. Anschließend werden neue Instanzen erzeugt.

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

Asynchrones Laden
: Rufe [`factory.load()`](/ref/factory/#factory.load) auf, um die Ressourcen ausdrücklich asynchron zu laden. Sobald die Ressourcen zum Erzeugen von Objekten bereitstehen, wird ein Callback aufgerufen.

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

## Dynamischer Prototyp {#dynamic-prototype}

Du kannst ändern, welchen *Prototype* eine Fabrik erzeugen kann, indem du das Kontrollkästchen *Dynamic Prototype* in den Eigenschaften der Fabrik aktivierst.

![Dynamischer Prototyp](images/factory/dynamic_prototype.png)

Wenn die Option *Dynamic Prototype* aktiviert ist, kann die Fabrikkomponente den Prototyp mit der Funktion `factory.set_prototype()` ändern. Beispiel:

```lua
factory.unload("#factory") -- unload the previous resources
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Wenn die Option *Dynamic Prototype* aktiviert ist, kann die Anzahl der Komponenten in der Sammlung (collection) nicht optimiert werden. Die Sammlung, zu der die Fabrik gehört, verwendet dann die Standardanzahlen für Komponenten aus der Datei *game.project*.
:::


## Instanzgrenzen {#instance-limits}

Die Projekteinstellung *Max Instances* unter *Collection* ist die Obergrenze für die Anzahl der Spielobjekte in jeder Sammlung (Welt). Beim Build kann Defold eine kleinere Kapazität zuweisen, wenn sich feststellen lässt, dass dies sicher ist. Alle gleichzeitig existierenden Spielobjekte in einer Welt zählen zu dieser Kapazität, unabhängig davon, ob sie im Editor platziert oder zur Laufzeit erzeugt wurden.

![Maximale Anzahl der Instanzen](images/factory/factory_max_instances.png)

Die tatsächliche Zuweisung hängt von der Analyse beim Build ab:

* Wenn beim Build eine feste Anzahl von Spielobjekten ermittelt werden kann (in der Regel, wenn die Sammlung weder eine Fabrik noch eine Sammlungsfabrik (collection factory) enthält), entspricht die Kapazität der kompilierten Anzahl, begrenzt durch *Max Instances*.
* Eine Sammlung, die eine Fabrik oder Sammlungsfabrik enthält, verwendet *Max Instances* als Kapazität für Spielobjekte. Bei einem statisch referenzierten Prototyp ermittelt der Build, welche Komponententypen die Fabrik erzeugen kann. Diese Typen verwenden ihre jeweiligen im Projekt festgelegten Höchstanzahlen, während nicht betroffene Komponententypen weiterhin genaue Anzahlen verwenden können.
* Wenn du *Dynamic Prototype* aktivierst, wird die Analyse der Komponentenanzahl für die Sammlung, zu der die Fabrik gehört, deaktiviert. Sie verwendet deshalb *Max Instances* und die konfigurierten Höchstanzahlen für die einzelnen Komponententypen.

Richte *Max Instances* nach der größten Anzahl von Spielobjekten aus, die in einer dynamischen Welt gleichzeitig existieren können. Unter [Optimierung der maximalen Komponentenanzahl](/manuals/project-settings/#component-max-count-optimizations) erfährst du, wie die übrigen Komponentengrenzen berechnet werden.

## Spielobjekte in Pools verwalten {#pooling-of-game-objects}

Es mag sinnvoll erscheinen, erzeugte Spielobjekte in einem Pool zu speichern und wiederzuverwenden. Die Engine verwendet jedoch intern bereits Objektpooling, sodass zusätzlicher Verwaltungsaufwand die Abläufe nur verlangsamt. Spielobjekte zu löschen und neue zu erzeugen ist sowohl schneller als auch sauberer.
