---
title: Nachrichtenübermittlung in Defold
brief: Die Nachrichtenübermittlung ist der Mechanismus, mit dem Defold die Kommunikation zwischen lose gekoppelten Objekten ermöglicht. Dieses Handbuch beschreibt diesen Mechanismus ausführlich.
---

# Nachrichtenübermittlung {#message-passing}

Die Nachrichtenübermittlung (message passing) ist ein Mechanismus, über den Spielobjekte (game objects) in Defold miteinander kommunizieren. Dieses Handbuch setzt voraus, dass du ein grundlegendes Verständnis von Defolds [Adressierungsmechanismus](/manuals/addressing) und [grundlegenden Bausteinen](/manuals/building-blocks) hast.

Defold verwendet keine Objektorientierung in dem Sinne, dass du deine Anwendung durch Klassenhierarchien mit Vererbung und Memberfunktionen in deinen Objekten definierst (wie in Java, C++ oder C#). Stattdessen erweitert Defold Lua um einen einfachen und leistungsfähigen objektorientierten Entwurf, bei dem der Objektzustand intern in Skriptkomponenten (script components) gespeichert wird und über die Referenz `self` zugänglich ist. Außerdem lassen sich Objekte vollständig voneinander entkoppeln, indem sie über asynchrone Nachrichtenübermittlung miteinander kommunizieren.


## Anwendungsbeispiele {#usage-examples}

Sehen wir uns zunächst einige einfache Anwendungsbeispiele an. Angenommen, du entwickelst ein Spiel, das aus Folgendem besteht:

1. Einer Startsammlung (bootstrap collection) als Hauptsammlung, die ein Spielobjekt mit einer GUI-Komponente enthält (die GUI besteht aus einer Minikarte und einem Punktezähler). Außerdem gibt es eine Sammlung (collection) mit dem Bezeichner "level".
2. Die Sammlung namens "level" enthält zwei Spielobjekte: eine vom Spieler gesteuerte Heldenfigur und einen Gegner.

![Struktur der Nachrichtenübermittlung](images/message_passing/message_passing_structure.png)

::: sidenote
Der Inhalt dieses Beispiels befindet sich in zwei getrennten Dateien. Es gibt eine Datei für die Startsammlung und eine für die Sammlung mit dem Bezeichner "level". Dateinamen _spielen in Defold jedoch keine Rolle_. Entscheidend ist die Identität, die du den Instanzen zuweist.
:::

Das Spiel enthält einige einfache Mechaniken, die Kommunikation zwischen den Objekten erfordern:

![Nachrichtenübermittlung](images/message_passing/message_passing.png)

① Der Held schlägt den Gegner
: Als Teil dieser Mechanik wird eine Nachricht `"punch"` von der Skriptkomponente "hero" an die Skriptkomponente "enemy" gesendet. Da sich beide Objekte an derselben Stelle in der Sammlungshierarchie befinden, ist relative Adressierung vorzuziehen:

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  Im Spiel gibt es nur einen Schlag mit einer festen Stärke, daher muss die Nachricht außer ihrem Namen "punch" keine weiteren Informationen enthalten.

  In der Skriptkomponente des Gegners erstellst du eine Funktion, um die Nachricht zu empfangen:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  In diesem Fall prüft der Code nur den Namen der Nachricht (der als gehashte Zeichenfolge im Parameter `message_id` gesendet wird). Der Code berücksichtigt weder die Nachrichtendaten noch den Absender---*jeder*, der die Nachricht "punch" sendet, fügt dem armen Gegner Schaden zu.

② Der Held erhält Punkte
: Immer wenn der Spieler einen Gegner besiegt, erhöht sich sein Punktestand. Außerdem wird eine Nachricht `"update_score"` von der Skriptkomponente des Spielobjekts "hero" an die Komponente "gui" des Spielobjekts "interface" gesendet.

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  In diesem Fall lässt sich keine relative Adresse angeben, da sich "interface" an der Wurzel der Namenshierarchie befindet und "hero" nicht. Die Nachricht wird an die GUI-Komponente gesendet, der ein Skript zugewiesen ist, sodass sie entsprechend auf die Nachricht reagieren kann. Nachrichten können frei zwischen Skripten, GUI-Skripten und Render-Skripten gesendet werden.

  Die Nachricht `"update_score"` enthält Daten zum Punktestand. Diese Daten werden als Lua-Tabelle im Parameter `message` übergeben:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Die Position des Gegners auf der Minikarte
: Dem Spieler steht eine Minikarte auf dem Bildschirm zur Verfügung, um Gegner zu finden und zu verfolgen. Jeder Gegner ist dafür verantwortlich, seine Position zu melden, indem er eine Nachricht `"update_minimap"` an die Komponente "gui" im Spielobjekt "interface" sendet:

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  Der Code des GUI-Skripts muss die Position jedes Gegners verfolgen. Sendet derselbe Gegner eine neue Position, sollte sie die alte ersetzen. Der Absender der Nachricht (der im Parameter `sender` übergeben wird) kann als Schlüssel einer Lua-Tabelle mit Positionen verwendet werden:

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

## Nachrichten senden {#sending-messages}

Eine Nachricht zu senden ist, wie wir oben gesehen haben, sehr einfach. Du rufst die Funktion `msg.post()` auf, die deine Nachricht in die Nachrichtenwarteschlange einreiht. Die Engine durchläuft dann in jedem Frame die Warteschlange und stellt jede Nachricht an ihrer Zieladresse zu. Bei einigen Systemnachrichten (wie `"enable"`, `"disable"`, `"set_parent"` usw.) verarbeitet der Engine-Code die Nachricht. Die Engine erzeugt auch selbst einige Systemnachrichten (wie `"collision_response"` bei physikalischen Kollisionen), die deinen Objekten zugestellt werden. Bei benutzerdefinierten Nachrichten an Skriptkomponenten ruft die Engine lediglich eine spezielle Lua-Funktion von Defold namens `on_message()` auf.

Du kannst beliebige Nachrichten an jedes vorhandene Objekt oder jede vorhandene Komponente senden. Es liegt am Code auf der Empfängerseite, auf die Nachricht zu reagieren. Wenn du eine Nachricht an eine Skriptkomponente sendest und der Skriptcode sie ignoriert, ist das in Ordnung. Die Verantwortung für den Umgang mit Nachrichten liegt vollständig beim Empfänger.

Die Engine prüft die Zieladresse der Nachricht. Wenn du versuchst, eine Nachricht an einen unbekannten Empfänger zu senden, meldet Defold einen Fehler in der Konsole:

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

Die vollständige Signatur des Aufrufs `msg.post()` lautet:

`msg.post(receiver, message_id, [message])`

receiver
: Der Bezeichner der Zielkomponente oder des Zielspielobjekts. Beachte, dass die Nachricht an alle Komponenten im Spielobjekt gesendet wird, wenn du ein Spielobjekt als Ziel angibst.

message_id
: Eine Zeichenfolge oder gehashte Zeichenfolge mit dem Namen der Nachricht.

[message]
: Eine optionale Lua-Tabelle mit Schlüssel-Wert-Paaren für die Nachrichtendaten. Die Lua-Tabelle der Nachricht kann nahezu jeden Datentyp enthalten. Du kannst Zahlen, Zeichenfolgen, boolesche Werte, URLs, Hashwerte und verschachtelte Tabellen übergeben. Funktionen kannst du nicht übergeben.

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Für die Größe der Tabelle im Parameter `message` gibt es eine feste Obergrenze. Diese beträgt 2 Kilobyte. Derzeit gibt es keine einfache Möglichkeit, den genauen Speicherbedarf einer Tabelle zu bestimmen. Du kannst aber vor und nach dem Einfügen der Tabelle `collectgarbage("count")` verwenden, um den Speicherverbrauch zu beobachten.
:::

### Kurzformen {#shorthands}

Defold bietet zwei praktische Kurzformen, mit denen du Nachrichten senden kannst, ohne eine vollständige URL anzugeben:

:[Shorthands](../shared/url-shorthands.md)


## Nachrichten empfangen {#receiving-messages}

Um Nachrichten zu empfangen, musst du sicherstellen, dass die Zielskriptkomponente eine Funktion namens `on_message()` enthält. Die Funktion nimmt vier Parameter entgegen:

`function on_message(self, message_id, message, sender)`

`self`
: Eine Referenz auf die Skriptkomponente selbst.

`message_id`
: Enthält den Namen der Nachricht. Der Name ist _gehasht_.

`message`
: Enthält die Nachrichtendaten. Dies ist eine Lua-Tabelle. Wenn es keine Daten gibt, ist die Tabelle leer.

`sender`
: Enthält die vollständige URL des Absenders.

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

## Nachrichten zwischen Spielwelten {#messaging-between-game-worlds}

Wenn du eine Sammlungs-Proxy-Komponente (collection proxy component) verwendest, um eine neue Spielwelt in die Laufzeitumgebung zu laden, wirst du Nachrichten zwischen den Spielwelten übermitteln wollen. Angenommen, du hast eine Sammlung über einen Proxy geladen und ihre Eigenschaft *Name* ist auf "level" gesetzt:

![Name der Sammlung](images/message_passing/collection_name.png)

Sobald die Sammlung geladen, initialisiert und aktiviert wurde, kannst du Nachrichten an jede Komponente oder jedes Objekt in der neuen Welt senden, indem du den Namen der Spielwelt im Feld "socket" der Empfängeradresse angibst:

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```
Eine ausführlichere Beschreibung der Funktionsweise von Proxys findest du in der Dokumentation zu [Sammlungs-Proxys](/manuals/collection-proxy).

## Nachrichtenketten {#message-chains}

Wenn eine gesendete Nachricht schließlich zugestellt wird, wird `on_message()` beim Empfänger aufgerufen. Häufig sendet der Code als Reaktion neue Nachrichten, die der Nachrichtenwarteschlange hinzugefügt werden.

Wenn die Engine mit der Zustellung beginnt, arbeitet sie die Nachrichtenwarteschlange ab, ruft die Funktion `on_message()` jedes Nachrichtenempfängers auf und fährt fort, bis die Nachrichtenwarteschlange leer ist. Werden während dieses Durchlaufs neue Nachrichten zur Warteschlange hinzugefügt, führt sie einen weiteren Durchlauf aus. Es gibt jedoch eine feste Obergrenze dafür, wie oft die Engine versucht, die Warteschlange zu leeren. Dadurch ist die Länge der Nachrichtenketten begrenzt, deren vollständige Zustellung du innerhalb eines Frames erwarten kannst. Mit dem folgenden Skript kannst du leicht testen, wie viele Durchläufe der Nachrichtenverarbeitung die Engine zwischen den einzelnen Aufrufen von `update()` ausführt:

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

Wenn du dieses Skript ausführst, erhältst du eine Ausgabe wie die folgende:

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

Wir sehen, dass diese bestimmte Version der Defold-Engine zwischen `init()` und dem ersten Aufruf von `update()` die Nachrichtenwarteschlange in 10 Durchläufen abarbeitet. Anschließend führt sie bei jeder weiteren Aktualisierungsschleife 75 Durchläufe aus.
