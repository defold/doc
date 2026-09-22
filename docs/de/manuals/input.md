---
title: Geräteeingabe in Defold
brief: Dieses Handbuch erklärt, wie Eingaben funktionieren, wie du Eingabeaktionen erfasst und interaktive Reaktionen in Skripten erstellst.
---

# Eingabe {#input}

Die Engine erfasst alle Benutzereingaben und leitet sie als Aktionen an Komponenten (components) vom Typ Skript oder GUI-Skript in Spielobjekten (game objects) weiter, die den Eingabefokus erhalten haben und die Funktion `on_input()` implementieren. Dieses Handbuch erklärt, wie du Eingabebindungen (input bindings) zum Erfassen von Eingaben einrichtest und Code erstellst, der darauf reagiert.

Das Eingabesystem verwendet einige einfache und leistungsfähige Konzepte, mit denen du Eingaben so verwalten kannst, wie es für dein Spiel sinnvoll ist.

![Eingabebindungen](images/input/overview.png)

Geräte
: Eingabegeräte, die Teil deines Computers oder Mobilgeräts oder daran angeschlossen sind, liefern unverarbeitete Eingaben auf Systemebene an die Defold-Laufzeitumgebung. Die folgenden Gerätetypen werden unterstützt:

  1. Tastatur (einzelne Tasten sowie Texteingabe)
  2. Maus (Position, Tastenklicks und Mausradaktionen)
  3. Berührungseingabe mit einer oder mehreren Berührungen (auf iOS- und Android-Geräten sowie in HTML5 auf Mobilgeräten)
  4. Gamepads (soweit sie vom Betriebssystem unterstützt und in der Datei [gamepads](/manuals/input-gamepads/#gamepads-settings-file) zugeordnet werden)

Eingabebindungen
: Bevor die Eingabe an ein Skript gesendet wird, werden die unverarbeiteten Eingaben des Geräts über die Tabelle der Eingabebindungen in sinnvolle *Aktionen* übersetzt.

Aktionen
: Aktionen werden anhand der (gehashten) Namen identifiziert, die du in der Datei für Eingabebindungen aufführst. Jede Aktion enthält außerdem relevante Daten zur Eingabe: ob eine Taste gedrückt oder losgelassen wird, die Koordinaten der Maus oder Berührung usw.

Eingabeempfänger
: Skriptkomponenten und GUI-Skripte können Eingabeaktionen empfangen, indem sie *den Eingabefokus anfordern*. Mehrere Empfänger können gleichzeitig aktiv sein.

Eingabestapel
: Die Liste der Eingabeempfänger, bei der der Empfänger, der den Fokus zuerst angefordert hat, ganz unten im Stapel steht und der letzte ganz oben.

Eingaben abfangen
: Ein Skript kann entscheiden, die empfangene Eingabe abzufangen, sodass Empfänger weiter unten im Stapel sie nicht erhalten.

## Eingabebindungen einrichten {#setting-up-input-bindings}

Die Eingabebindungen bilden eine projektweite Tabelle, mit der du festlegst, wie Geräteeingaben in benannte *Aktionen* übersetzt werden, bevor sie an deine Skriptkomponenten und GUI-Skripte weitergeleitet werden. Du kannst eine neue Datei für Eingabebindungen erstellen, indem du einen <kbd>Rechtsklick</kbd> auf einen Ort in der Ansicht *Assets* ausführst und <kbd>New... ▸ Input Binding</kbd> wählst. Damit die Engine die neue Datei verwendet, ändere den Eintrag *Game Binding* in *game.project*.

![Einstellung für Eingabebindungen](images/input/setting.png)

Bei allen neuen Projektvorlagen wird automatisch eine Standarddatei für Eingabebindungen erstellt, daher musst du normalerweise keine neue Bindungsdatei erstellen. Die Standarddatei heißt `game.input_binding` und befindet sich im Ordner `input` im Projektstammverzeichnis. <kbd>Doppelklicke</kbd> auf die Datei, um sie im Editor zu öffnen:

![Eingabebindungen festlegen](images/input/input_binding.png)

Um eine neue Bindung zu erstellen, klicke unten im Abschnitt des entsprechenden Auslösertyps auf die Schaltfläche <kbd>+</kbd>. Jeder Eintrag hat zwei Felder:

*Input*
: Die unverarbeitete Eingabe, auf die reagiert werden soll, ausgewählt aus einer scrollbaren Liste verfügbarer Eingaben.

*Action*
: Der Aktionsname, den Eingabeaktionen erhalten, wenn sie erstellt und an deine Skripte weitergeleitet werden. Derselbe Aktionsname kann mehreren Eingaben zugewiesen werden. Beispielsweise kannst du die Taste <kbd>Space</kbd> und die Gamepad-Taste `A` an die Aktion `jump` binden. Beachte, dass es einen bekannten Fehler gibt, durch den Berührungseingaben leider nicht dieselben Aktionsnamen wie andere Eingaben haben können.

## Auslösertypen {#trigger-types}

Du kannst fünf gerätespezifische Arten von Auslösern erstellen:

Key Triggers
: Eingabe einzelner Tastaturtasten. Jede Taste wird separat einer entsprechenden Aktion zugeordnet. Weitere Informationen findest du im [Handbuch zur Tasten- und Texteingabe](/manuals/input-key-and-text).

Text Triggers
: Textauslöser werden verwendet, um beliebige Texteingaben zu lesen. Weitere Informationen findest du im [Handbuch zur Tasten- und Texteingabe](/manuals/input-key-and-text)

Mouse Triggers
: Eingaben von Maustasten und Mausrädern. Weitere Informationen findest du im [Handbuch zur Maus- und Berührungseingabe](/manuals/input-mouse-and-touch).

Touch Triggers
: Auslöser für Berührungseingaben mit einer oder mehreren Berührungen sind auf iOS- und Android-Geräten in nativen Anwendungen und in HTML5-Bundles verfügbar. Weitere Informationen findest du im [Handbuch zur Maus- und Berührungseingabe](/manuals/input-mouse-and-touch).

Gamepad Triggers
: Gamepad-Auslöser ermöglichen es dir, Standard-Gamepad-Eingaben an Spielfunktionen zu binden. Weitere Informationen findest du im [Gamepad-Handbuch](/manuals/input-gamepads).

### Eingabe des Beschleunigungssensors {#accelerometer-input}

Zusätzlich zu den fünf oben aufgeführten Auslösertypen unterstützt Defold auch Eingaben des Beschleunigungssensors in nativen Android- und iOS-Anwendungen. Aktiviere das Kontrollkästchen *Use Accelerometer* im Abschnitt *Input* deiner Datei *game.project*.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- react to accelerometer data
    end
end
```

## Eingabefokus {#input-focus}

Um in einer Skriptkomponente oder einem GUI-Skript auf Eingabeaktionen zu reagieren, sollte die Nachricht `acquire_input_focus` an das Spielobjekt gesendet werden, das die Komponente enthält:

```lua
-- tell the current game object (".") to acquire input focus
msg.post(".", "acquire_input_focus")
```

Diese Nachricht weist die Engine an, eingabefähige Komponenten in den Spielobjekten zum *Eingabestapel* hinzuzufügen. Dazu gehören Skriptkomponenten, GUI-Komponenten und Sammlungs-Proxys (collection proxies). Die Komponenten der Spielobjekte werden oben auf den Eingabestapel gelegt; die zuletzt hinzugefügte Komponente steht ganz oben im Stapel. Beachte, dass alle Komponenten zum Stapel hinzugefügt werden, wenn das Spielobjekt mehr als eine eingabefähige Komponente enthält:

![Eingabestapel](images/input/input_stack.png)

Wenn ein Spielobjekt, das den Eingabefokus bereits angefordert hat, dies erneut tut, werden seine Komponenten an die oberste Stelle des Stapels verschoben.


## Weiterleitung von Eingaben und on_input() {#input-dispatch-and-on_input}

Eingabeaktionen werden entsprechend dem Eingabestapel von oben nach unten weitergeleitet.

![Weiterleitung von Aktionen](images/input/actions.png)

Bei jeder Komponente im Stapel, die eine Funktion `on_input()` enthält, wird diese Funktion einmal für jede Eingabeaktion während des Frames mit den folgenden Argumenten aufgerufen:

`self`
: Die aktuelle Skriptinstanz.

`action_id`
: Der gehashte Name der Aktion, wie in den Eingabebindungen festgelegt.

`action`
: Eine Tabelle mit den nützlichen Daten zur Aktion, etwa dem Eingabewert, ihrer Position (absolute Position und Positionsänderung), ob bei einer Tasteneingabe `pressed` gesetzt war usw. Einzelheiten zu den verfügbaren Aktionsfeldern findest du unter [on_input()](/ref/go#on_input).

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- move left
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- move right
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Eingabefokus und Sammlungs-Proxy-Komponenten {#input-focus-and-collection-proxy-components}

Jede Spielwelt, die dynamisch über einen Sammlungs-Proxy geladen wird, hat ihren eigenen Eingabestapel. Damit die Weiterleitung von Aktionen den Eingabestapel der geladenen Welt erreicht, muss sich die Proxy-Komponente im Eingabestapel der Hauptwelt befinden. Alle Komponenten im Stapel einer geladenen Welt werden verarbeitet, bevor die Weiterleitung im Hauptstapel nach unten fortgesetzt wird:

![Weiterleitung von Aktionen an Proxys](images/input/proxy.png)

::: important
Ein häufiger Fehler besteht darin, das Senden von `acquire_input_focus` an das Spielobjekt zu vergessen, das die Sammlungs-Proxy-Komponente enthält. Wenn du diesen Schritt überspringst, erreichen Eingaben keine der Komponenten im Eingabestapel der geladenen Welt.
:::


### Eingabefokus freigeben {#releasing-input}

Um nicht mehr auf Eingabeaktionen zu reagieren, sende eine Nachricht `release_input_focus` an das Spielobjekt. Diese Nachricht entfernt alle Komponenten des Spielobjekts aus dem Eingabestapel:

```lua
-- tell the current game object (".") to release input focus.
msg.post(".", "release_input_focus")
```


## Eingaben abfangen {#consuming-input}

Die Funktion `on_input()` einer Komponente kann aktiv steuern, ob Aktionen im Stapel weiter nach unten weitergegeben werden sollen:

- Wenn `on_input()` den Wert `false` zurückgibt oder keine Rückgabe erfolgt (dies entspricht der Rückgabe von `nil`, das in Lua als falsch gilt), werden Eingabeaktionen an die nächste Komponente im Eingabestapel weitergegeben.
- Wenn `on_input()` den Wert `true` zurückgibt, wird die Eingabe abgefangen. Keine Komponente weiter unten im Eingabestapel erhält die Eingabe. Beachte, dass dies für *alle* Eingabestapel gilt. Eine Komponente im Stapel einer über einen Proxy geladenen Welt kann Eingaben abfangen und dadurch verhindern, dass Komponenten im Hauptstapel Eingaben erhalten:

![Eingaben abfangen](images/input/consuming.png)

Es gibt viele gute Anwendungsfälle, in denen das Abfangen von Eingaben eine einfache und leistungsfähige Möglichkeit bietet, Eingaben zwischen verschiedenen Teilen eines Spiels umzuleiten. Das ist beispielsweise hilfreich, wenn du ein Pop-up-Menü benötigst, das vorübergehend als einziger Teil des Spiels auf Eingaben reagiert:

![Eingaben abfangen](images/input/game.png)

Das Pausenmenü ist anfangs ausgeblendet (deaktiviert) und wird aktiviert, wenn der Spieler das HUD-Element `PAUSE` berührt:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- Did the player press PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Tell the pause menu to take over.
            msg.post("pause_menu", "show")
        end
    end
end
```

![Pausenmenü](images/input/game_paused.png)

Die GUI des Pausenmenüs fordert den Eingabefokus an und fängt Eingaben ab, sodass nur noch die für das Pop-up-Menü relevanten Eingaben verarbeitet werden:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Show the pause menu.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Acquire input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- do things...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Hide the pause menu
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Release input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume all input. Anything below us on the input stack
  -- will never see input until we release input focus.
  return true
end
```
