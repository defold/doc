---
title: Eigenschaften von Skriptkomponenten
brief: Dieses Handbuch erklärt, wie du Skriptkomponenten benutzerdefinierte Eigenschaften hinzufügst und im Editor sowie aus Skripten zur Laufzeit darauf zugreifst.
---

# Skripteigenschaften {#script-properties}

Skripteigenschaften (script properties) bieten eine einfache und leistungsfähige Möglichkeit, benutzerdefinierte Eigenschaften für eine bestimmte Instanz eines Spielobjekts (game object) zu definieren und zugänglich zu machen. Skripteigenschaften bestimmter Instanzen lassen sich direkt im Editor bearbeiten. Ihre Einstellungen können im Code verwendet werden, um das Verhalten eines Spielobjekts zu ändern. Skripteigenschaften sind in vielen Fällen sehr nützlich:

* Wenn du Werte für bestimmte Instanzen im Editor überschreiben und dadurch Skripte besser wiederverwenden möchtest.
* Wenn du ein Spielobjekt mit Anfangswerten dynamisch erzeugen möchtest.
* Wenn du die Werte einer Eigenschaft animieren möchtest.
* Wenn du von einem Skript aus auf Zustandsdaten in einem anderen zugreifen möchtest. (Beachte, dass es bei häufigen Zugriffen auf Eigenschaften zwischen Objekten besser sein kann, die Daten in einen gemeinsamen Speicher zu verschieben.)

Typische Anwendungsfälle sind das Festlegen der Lebenspunkte oder Geschwindigkeit einer bestimmten Gegner-KI, der Einfärbung eines einsammelbaren Objekts, des Atlas eines Sprites oder der Nachricht, die ein Schaltflächenobjekt beim Drücken senden soll---und/oder ihres Empfängers.

## Eine Skripteigenschaft definieren {#defining-a-script-property}

Skripteigenschaften werden einer Skriptkomponente (script component) hinzugefügt, indem du sie mit der speziellen Funktion `go.property()` definierst. Die Funktion muss auf der obersten Ebene verwendet werden---außerhalb von Lebenszyklusfunktionen wie `init()` und `update()`. Der für die Eigenschaft angegebene Standardwert bestimmt ihren Typ: `number`, `boolean`, `string`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` und `resource` (siehe unten).

::: important
Beachte, dass sich der ursprüngliche Zeichenfolgenwert eines Hash-Werts nur im Debug-Build ermitteln lässt, um die Fehlersuche zu erleichtern. Im Release-Build ist dieser Zeichenfolgenwert nicht vorhanden. Daher ist es dort nicht sinnvoll, mit `tostring()` die Zeichenfolge aus einem `hash`-Wert auszulesen.
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

Für jede aus diesem Skript erstellte Skriptkomponenteninstanz lassen sich dann die Eigenschaftswerte festlegen.

![Komponente mit Eigenschaften](images/script-properties/component.png)

 Wähle die Skriptkomponente in der Ansicht *Outline* im Editor aus. Die Eigenschaften erscheinen in der Ansicht *Properties*, wo du sie bearbeiten kannst:

![Properties](images/script-properties/properties.png)

Jede Eigenschaft, die mit einem neuen, für die Instanz spezifischen Wert überschrieben wird, ist blau markiert. Klicke auf die Schaltfläche zum Zurücksetzen neben dem Eigenschaftsnamen, um den Wert auf den im Skript festgelegten Standardwert zurückzusetzen.


::: important
Skripteigenschaften werden beim Erstellen des Projekts geparst. Wertausdrücke werden nicht ausgewertet. Das bedeutet, dass beispielsweise `go.property("hp", 3+6)` nicht funktioniert, `go.property("hp", 9)` dagegen schon.
:::

### Texteigenschaften {#text-properties}

Seit Defold 1.13.2 definiert eine Zeichenfolge als Standardwert eine Texteigenschaft. Texteigenschaften unterstützen UTF-8 und Zeilenumbruchzeichen und werden im Editor in einem mehrzeiligen Feld bearbeitet:

```lua
go.property("greeting", "Hello!\nWelcome, José!")

function init(self)
    go.set("#label", "text", self.greeting)
end
```

Wähle eine Skriptkomponente in einem Spielobjekt oder einer Sammlung (collection) aus, um ihre Texteigenschaften wie andere Skripteigenschaften zu überschreiben. Eingebettete NUL-Zeichen sind weder in Standardwerten noch in überschreibenden Werten erlaubt.

Andere Skripte können eine Texteigenschaft über die URL der Skriptkomponente lesen und schreiben. Füge beispielsweise das obige Skript und eine Beschriftungskomponente zu einem Spielobjekt namens `speaker` in der Sammlung hinzu und gib den Komponenten die Bezeichner `script` und `label`. Aktualisiere sie aus der Funktion `init()` eines anderen Skripts:

```lua
function init(self)
    local greeting = go.get("/speaker#script", "greeting")
    go.set("/speaker#script", "greeting", greeting .. "\nEnjoy the game!")
    go.set("/speaker#label", "text", go.get("/speaker#script", "greeting"))
end
```

Das Ändern der Skripteigenschaft aktualisiert die Beschriftung nicht automatisch; die letzte Zeile kopiert den neuen Wert ausdrücklich in die Eigenschaft `text` der Beschriftung.

## Auf Skripteigenschaften zugreifen {#accessing-script-properties}

Jede definierte Skripteigenschaft ist als gespeichertes Feld in `self`, der Referenz auf die Skriptinstanz, verfügbar:

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

Benutzerdefinierte Skripteigenschaften lassen sich auch mit `go.get()` lesen und mit `go.set()` schreiben. Numerische Eigenschaften, einschließlich Vektoren und Quaternionen, können mit `go.animate()` animiert werden. Texteigenschaften lassen sich lesen und schreiben, können aber nicht animiert werden:

```lua
-- another.script

-- increase "my_property" in "myobject#script" by 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animate "my_property" in "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Mit einer Fabrik erstellte Objekte {#factory-created-objects}

Wenn du das Spielobjekt mit einer Fabrik (factory) erstellst, kannst du die Skripteigenschaften zum Zeitpunkt der Erstellung festlegen:

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accessing factory-created script properties
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Wenn du über `collectionfactory.create()` eine Hierarchie von Spielobjekten dynamisch erzeugst, musst du den Objektbezeichnern Eigenschaftstabellen zuordnen. Diese Zuordnungen werden in einer Tabelle zusammengefasst und an die Funktion `create()` übergeben:

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Die über `factory.create()` und `collectionfactory.create()` angegebenen Eigenschaftswerte überschreiben sowohl die Werte in der Prototypdatei als auch die Standardwerte im Skript.

Wenn mehrere Skriptkomponenten eines Spielobjekts dieselbe Eigenschaft definieren, wird jede Komponente mit dem an `factory.create()` oder `collectionfactory.create()` übergebenen Wert initialisiert.


## Ressourceneigenschaften {#resource-properties}

Ressourceneigenschaften (resource properties) werden genauso definiert wie Skripteigenschaften für die grundlegenden Datentypen:

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Eine definierte Ressourceneigenschaft erscheint wie jede andere Skripteigenschaft in der Ansicht *Properties*, jedoch als Feld zur Auswahl einer Datei oder Ressource:

![Ressourceneigenschaften](images/script-properties/resource-properties.png)

Du greifst mit `go.get()` oder über die Skriptinstanzreferenz `self` auf Ressourceneigenschaften zu und verwendest sie mit `go.set()`:

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
