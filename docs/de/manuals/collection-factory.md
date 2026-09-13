---
title: Handbuch zu Sammlungsfabriken
brief: Dieses Handbuch erklärt, wie du mit Sammlungsfabrikkomponenten Hierarchien von Spielobjekten dynamisch erzeugst.
---

# Sammlungsfabriken {#collection-factories}

Die Sammlungsfabrik (collection factory) ist eine Komponente (component), mit der du Gruppen und Hierarchien von Spielobjekten (game objects), die in Sammlungsdateien gespeichert sind, in einem laufenden Spiel dynamisch erzeugst.

Sammlungen (collections) bieten einen leistungsfähigen Mechanismus, um wiederverwendbare Vorlagen oder „Prefabs“ in Defold zu erstellen. Eine Übersicht über Sammlungen findest du in der [Dokumentation zu den Bausteinen](/manuals/building-blocks#collections). Sammlungen können im Editor platziert oder dynamisch in dein Spiel eingefügt werden.

Mit einer Sammlungsfabrikkomponente kannst du die Inhalte einer Sammlungsdatei in einer Spielwelt dynamisch erzeugen. Das entspricht dem dynamischen Erzeugen aller Spielobjekte innerhalb der Sammlung durch eine Fabrik (factory) mit anschließendem Aufbau der Eltern-Kind-Hierarchie zwischen den Objekten. Ein typischer Anwendungsfall ist das dynamische Erzeugen von Gegnern, die aus mehreren Spielobjekten bestehen (zum Beispiel Gegner + Waffe).

## Eine Sammlung dynamisch erzeugen {#spawning-a-collection}

Angenommen, wir möchten ein Spielobjekt für eine Figur und ein separates Spielobjekt für einen Schild, das der Figur untergeordnet ist. Wir erstellen die Spielobjekthierarchie in einer Sammlungsdatei und speichern sie als `bean.collection`.

::: sidenote
Die Komponente *Sammlungs-Proxy (collection proxy)* wird verwendet, um auf Grundlage einer Sammlung eine neue Spielwelt einschließlich einer separaten Physikwelt zu erstellen. Auf die neue Welt wird über einen neuen Socket zugegriffen. Alle in der Sammlung enthaltenen Assets werden über den Proxy geladen, wenn du ihm eine Nachricht zum Starten des Ladevorgangs sendest. Dadurch sind Sammlungs-Proxys beispielsweise sehr nützlich, um in einem Spiel die Level zu wechseln. Neue Spielwelten bringen allerdings einen erheblichen Zusatzaufwand mit sich. Verwende sie daher nicht zum dynamischen Laden kleiner Inhalte. Weitere Informationen findest du in der [Dokumentation zu Sammlungs-Proxys](/manuals/collection-proxy).
:::

![Dynamisch zu erzeugende Sammlung](images/collection_factory/collection.png)

Anschließend fügen wir einem Spielobjekt, das für das dynamische Erzeugen zuständig sein wird, eine *Collection factory* hinzu und legen `bean.collection` als *Prototype* der Komponente fest:

![Sammlungsfabrik](images/collection_factory/factory.png)

Um `bean` und den Schild dynamisch zu erzeugen, müssen wir jetzt nur noch die Funktion `collectionfactory.create()` aufrufen:

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

Die Funktion nimmt 5 Parameter entgegen:

`url`
: Der Bezeichner (ID) der Sammlungsfabrikkomponente, die die neue Gruppe von Spielobjekten dynamisch erzeugen soll.

`[position]`
: (optional) Die Position der dynamisch erzeugten Spielobjekte im Weltkoordinatensystem. Dies sollte ein `vector3` sein. Wenn du keine Position angibst, werden die Objekte an der Position der Sammlungsfabrikkomponente erzeugt.

`[rotation]`
: (optional) Die Drehung der neuen Spielobjekte im Weltkoordinatensystem. Dies sollte ein `quat` sein.

`[properties]`
: (optional) Eine Lua-Tabelle mit `id`-`table`-Paaren, die zur Initialisierung der dynamisch erzeugten Spielobjekte verwendet werden. Wie du diese Tabelle aufbaust, erfährst du weiter unten.

`[scale]`
: (optional) Die Skalierung der dynamisch erzeugten Spielobjekte. Die Skalierung kann als `number` (größer als 0) angegeben werden, die eine gleichmäßige Skalierung entlang aller Achsen festlegt. Du kannst auch einen `vector3` angeben, bei dem jede Vektorkomponente die Skalierung entlang der entsprechenden Achse festlegt.

`collectionfactory.create()` gibt die Bezeichner der dynamisch erzeugten Spielobjekte als Tabelle zurück. Die Tabellenschlüssel ordnen den Hashwert der sammlungslokalen ID jedes Objekts dessen Laufzeit-ID zu:

::: sidenote
Die Eltern-Kind-Beziehung zwischen `bean` und `shield` wird in der zurückgegebenen Tabelle *nicht* abgebildet. Diese Beziehung besteht nur im Szenengraphen zur Laufzeit, also darin, wie Objekte gemeinsam transformiert werden. Die Zuordnung eines Objekts zu einem anderen übergeordneten Objekt ändert niemals seine ID.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. Der ID wird ein Präfix `/collection[N]/` hinzugefügt, wobei `[N]` ein Zähler ist, um jede Instanz eindeutig zu identifizieren:

## Eigenschaften {#properties}

Wenn du eine Sammlung dynamisch erzeugst, kannst du jedem Spielobjekt Eigenschaftsparameter übergeben. Erstelle dazu eine Tabelle, deren Schlüssel Objekt-IDs und deren Werte Tabellen mit den festzulegenden Skripteigenschaften sind.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Dabei gehen wir davon aus, dass das Spielobjekt `bean` in `bean.collection` die Eigenschaft `shield` definiert. [Das Handbuch zu Skripteigenschaften](/manuals/script-properties) enthält Informationen zu Skripteigenschaften.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Fabrikressourcen dynamisch laden {#dynamic-loading-of-factory-resources}

Wenn du das Kontrollkästchen *Load Dynamically* in den Eigenschaften der Sammlungsfabrik aktivierst, verschiebt die Engine das Laden der mit der Fabrik verknüpften Ressourcen auf einen späteren Zeitpunkt.

![Dynamisch laden](images/collection_factory/load_dynamically.png)

Wenn das Kontrollkästchen deaktiviert ist, lädt die Engine die Ressourcen des Prototyps beim Laden der Sammlungsfabrikkomponente, sodass sie sofort zum dynamischen Erzeugen bereitstehen.

Wenn das Kontrollkästchen aktiviert ist, hast du zwei Verwendungsmöglichkeiten:

Synchrones Laden
: Rufe [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) auf, wenn du Objekte dynamisch erzeugen möchtest. Dadurch werden die Ressourcen synchron geladen, was zu einem kurzen Ruckler führen kann. Anschließend werden neue Instanzen dynamisch erzeugt.

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

Asynchrones Laden
: Rufe [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) auf, um die Ressourcen ausdrücklich asynchron zu laden. Sobald die Ressourcen zum dynamischen Erzeugen bereitstehen, wird ein Callback aufgerufen.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## Dynamischer Prototyp {#dynamic-prototype}

Du kannst ändern, welchen *Prototype* eine Sammlungsfabrik erzeugen kann, indem du das Kontrollkästchen *Dynamic Prototype* in den Eigenschaften der Sammlungsfabrik aktivierst.

![Dynamischer Prototyp](images/collection_factory/dynamic_prototype.png)

Wenn die Option *Dynamic Prototype* aktiviert ist, kann die Sammlungsfabrikkomponente ihren Prototyp mit der Funktion `collectionfactory.set_prototype()` ändern. Beispiel:

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Wenn die Option *Dynamic Prototype* aktiviert ist, kann die Komponentenanzahl der Sammlung nicht optimiert werden. Die Sammlung, zu der die Komponente gehört, verwendet dann die Standardanzahlen für Komponenten aus der Datei *game.project*.
:::
