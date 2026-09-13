---
title: Spiellogik in Skripten schreiben
brief: Dieses Handbuch beschreibt, wie du mit Skriptkomponenten Spiellogik hinzufügst.
---

# Skripte {#scripts}

Mit Skriptkomponenten (script components) kannst du Spiellogik in der [Programmiersprache Lua](/manuals/lua) erstellen.


## Skripttypen {#script-types}

In Defold gibt es drei Arten von Lua-Skripten, denen jeweils unterschiedliche Defold-Bibliotheken zur Verfügung stehen.

Spielobjekt-Skripte
: Dateierweiterung _.script_. Diese Skripte werden Spielobjekten (game objects) genau wie jede andere [Komponente (component)](/manuals/components) hinzugefügt. Defold führt den Lua-Code als Teil der Lebenszyklusfunktionen der Engine aus. Spielobjekt-Skripte werden üblicherweise verwendet, um Spielobjekte und die übergreifende Spiellogik zu steuern, etwa das Laden von Levels, Spielregeln und Ähnliches. Spielobjekt-Skripte haben Zugriff auf die [GO](/ref/go)-Funktionen und alle Defold-Bibliotheksfunktionen mit Ausnahme der [GUI](/ref/gui)- und [Render](/ref/render)-Funktionen.


GUI-Skripte
: Dateierweiterung _.gui_script_. Sie werden von GUI-Komponenten ausgeführt und enthalten üblicherweise die Logik, die zur Anzeige von GUI-Elementen wie Statusanzeigen, Menüs usw. erforderlich ist. Defold führt den Lua-Code als Teil der Lebenszyklusfunktionen der Engine aus. GUI-Skripte haben Zugriff auf die [GUI](/ref/gui)-Funktionen und alle Defold-Bibliotheksfunktionen mit Ausnahme der [GO](/ref/go)- und [Render](/ref/render)-Funktionen.


Render-Skripte
: Dateierweiterung _.render_script_. Sie werden von der Rendering-Pipeline ausgeführt und enthalten die Logik, die zum Rendern der gesamten Grafik einer Anwendung oder eines Spiels in jedem Frame erforderlich ist. Das Render-Skript nimmt im Lebenszyklus deines Spiels eine besondere Rolle ein. Einzelheiten findest du in der [Dokumentation zum Anwendungslebenszyklus](/manuals/application-lifecycle). Render-Skripte haben Zugriff auf die [Render](/ref/render)-Funktionen und alle Defold-Bibliotheksfunktionen mit Ausnahme der [GO](/ref/go)- und [GUI](/ref/gui)-Funktionen.


## Skriptausführung, Callbacks und self {#script-execution-callbacks-and-self}

Defold führt Lua-Skripte als Teil des Lebenszyklus der Engine aus und macht diesen Lebenszyklus über eine Reihe vordefinierter Callback-Funktionen zugänglich. Wenn du einem Spielobjekt eine Skriptkomponente hinzufügst, wird das Skript Teil des Lebenszyklus des Spielobjekts und seiner Komponente(n). Beim Laden wird das Skript im Lua-Kontext ausgewertet. Anschließend führt die Engine die folgenden Funktionen aus und übergibt als Parameter eine Referenz auf die aktuelle Instanz der Skriptkomponente. Du kannst diese `self`-Referenz verwenden, um den Zustand in der Komponenteninstanz zu speichern.

::: important
`self` ist ein `userdata`-Objekt, das sich wie eine Lua-Tabelle verhält. Du kannst es jedoch nicht mit `pairs()` oder `ipairs()` durchlaufen und auch nicht mit `pprint()` ausgeben.
:::

#### `init(self)`
Wird aufgerufen, wenn die Komponente initialisiert wird.

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Wird aufgerufen, wenn die Komponente gelöscht wird. Das ist zum Aufräumen nützlich, beispielsweise wenn du Spielobjekte dynamisch erzeugt hast, die zusammen mit der Komponente gelöscht werden sollen.

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)`
Aktualisierung unabhängig von der Bildrate. Der Parameter `dt` enthält die Zeitdifferenz seit der letzten Aktualisierung. Diese Funktion wird abhängig vom zeitlichen Ablauf eines Frames und der Frequenz der Aktualisierungen mit festem Zeitschritt `0-N` Mal aufgerufen. Sie wird nur aufgerufen, wenn `Physics`-->`Use Fixed Timestep` aktiviert ist und `Engine`-->`Fixed Update Frequency` in *game.project* größer als 0 ist. Das ist nützlich, wenn du Physikobjekte in regelmäßigen Abständen verändern möchtest, um eine stabile Physiksimulation zu erreichen.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Wird einmal pro Frame nach dem `fixed_update`-Callback aller Skripte aufgerufen (wenn Fixed Timestep aktiviert ist). Der Parameter `dt` enthält die Zeitdifferenz seit dem letzten Frame.

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)`
Wird einmal pro Frame nach dem `update`-Callback aller Skripte, aber unmittelbar vor dem Rendern aufgerufen. Der Parameter `dt` enthält die Zeitdifferenz seit dem letzten Frame.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Wenn Nachrichten über [`msg.post()`](/ref/msg#msg.post) an die Skriptkomponente gesendet werden, ruft die Engine diese Funktion der Empfängerkomponente auf. Erfahre [mehr über die Nachrichtenübermittlung](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Wenn diese Komponente den Eingabefokus erhalten hat (siehe [`acquire_input_focus`](/ref/go/#acquire_input_focus)), ruft die Engine diese Funktion auf, sobald eine Eingabe registriert wird. Erfahre [mehr über die Eingabeverarbeitung](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Diese Funktion wird aufgerufen, wenn das Skript über die Editorfunktion Hot Reload (<kbd>Edit ▸ Reload Resource</kbd>) neu geladen wird. Sie ist sehr nützlich für die Fehlersuche, zum Testen und für Feinabstimmungen. Erfahre [mehr über Hot Reload](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## Reaktive Logik {#reactive-logic}

Ein Spielobjekt mit einer Skriptkomponente implementiert eine bestimmte Logik. Oft hängt diese Logik von einem äußeren Faktor ab. Die künstliche Intelligenz (KI) eines Gegners könnte darauf reagieren, dass sich der Spieler in einem bestimmten Umkreis um den Gegner befindet; eine Tür könnte durch eine Interaktion des Spielers entriegelt und geöffnet werden usw.

Mit der Funktion `update()` kannst du komplexes Verhalten als Zustandsautomaten implementieren, der in jedem Frame ausgeführt wird---manchmal ist das der passende Ansatz. Jeder Aufruf von `update()` verursacht jedoch einen Aufwand. Wenn du die Funktion nicht wirklich benötigst, solltest du sie löschen und stattdessen versuchen, deine Logik _reaktiv_ aufzubauen. Es ist weniger aufwendig, passiv auf eine Nachricht zu warten, die eine Reaktion auslöst, als die Spielwelt aktiv nach Daten abzusuchen, auf die reagiert werden soll. Außerdem führt eine reaktive Lösung eines Entwurfsproblems oft auch zu klareren und stabileren Entwürfen und Implementierungen.

Sehen wir uns ein konkretes Beispiel an. Angenommen, du möchtest, dass eine Skriptkomponente 2 Sekunden nach ihrer Initialisierung eine Nachricht sendet. Sie soll dann auf eine bestimmte Antwortnachricht warten und 5 Sekunden nach Erhalt der Antwort eine weitere Nachricht senden. Der nicht reaktive Code dafür würde etwa so aussehen:

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

Selbst in diesem recht einfachen Fall erhalten wir eine ziemlich verworrene Logik. Mit Koroutinen in einem Modul (siehe unten) ließe sie sich übersichtlicher gestalten. Versuchen wir stattdessen jedoch, sie reaktiv umzusetzen und einen integrierten Zeitsteuerungsmechanismus zu verwenden.

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

Das ist übersichtlicher und leichter nachzuvollziehen. Wir beseitigen interne Zustandsvariablen, deren Verlauf in der Logik oft schwer nachzuvollziehen ist---und die zu schwer erkennbaren Fehlern führen können. Außerdem entfernen wir die Funktion `update()` vollständig. Dadurch muss die Engine unser Skript nicht mehr 60 Mal pro Sekunde aufrufen, selbst wenn es gerade nichts zu tun hat.


## Vorverarbeitung {#preprocessing}

Mit einem Lua-Präprozessor und speziellen Auszeichnungen kannst du Code abhängig von der Build-Variante bedingt einbinden. Beispiel:

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

Der Präprozessor ist als Build-Erweiterung verfügbar. Auf der [Seite der Erweiterung auf GitHub](https://github.com/defold/extension-lua-preprocessor) erfährst du mehr darüber, wie du ihn installierst und verwendest.


## Unterstützung durch den Editor {#editor-support}

Der Defold-Editor unterstützt das Bearbeiten von Lua-Skripten mit Syntaxhervorhebung und automatischer Vervollständigung. Um Defold-Funktionsnamen zu vervollständigen, drücke *Ctrl+Space*. Damit öffnest du eine Liste der Funktionen, die zu deiner bisherigen Eingabe passen.

![Automatische Vervollständigung](images/script/completion.png)
