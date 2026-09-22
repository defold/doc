---
title: Gamepad-Eingabe in Defold
brief: Dieses Handbuch erklärt, wie Gamepad-Eingaben funktionieren.
---

::: sidenote
Es wird empfohlen, dass du dich damit vertraut machst, wie Eingaben in Defold grundsätzlich funktionieren, wie du sie empfängst und in welcher Reihenfolge deine Skriptdateien sie erhalten. Mehr über das Eingabesystem erfährst du im [Handbuch zur Eingabeübersicht](/manuals/input).
:::

# Gamepads
Mit Gamepad-Eingabeauslösern kannst du Standardeingaben von Gamepads an Spielfunktionen binden. Bei Gamepad-Eingaben kannst du eine Eingabebindung (input binding) für folgende Bedienelemente anlegen:

- Linker und rechter Stick (Richtung und Klicks)
- Linkes und rechtes digitales Steuerkreuz. Das rechte Steuerkreuz entspricht normalerweise den Tasten „A“, „B“, „X“ und „Y“ des Xbox-Controllers sowie den Tasten „Quadrat“, „Kreis“, „Dreieck“ und „Kreuz“ des PlayStation-Controllers.
- Linker und rechter Trigger
- Linke und rechte Schultertaste
- Tasten Start, Back und Guide

![](images/input/gamepad_bindings.png)

::: important
Die folgenden Beispiele verwenden die Aktionen aus der obigen Abbildung. Wie bei allen Eingaben kannst du deine Eingabeaktionen beliebig benennen.
:::

## Digitale Tasten {#digital-buttons}
Digitale Tasten erzeugen die Ereignisse `pressed`, `released` und `repeated`. Das folgende Beispiel zeigt, wie du Eingaben einer digitalen Taste erkennst (Drücken oder Loslassen):

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## Analogsticks {#analog-sticks}
Analogsticks erzeugen fortlaufend Eingabeereignisse, wenn der Stick außerhalb der Totzone bewegt wird, die in der Gamepad-Einstellungsdatei definiert ist (siehe unten). Das folgende Beispiel zeigt, wie du Eingaben eines Analogsticks erkennst:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Analogsticks erzeugen auch die Ereignisse `pressed` und `released`, wenn sie in eine der vier Hauptrichtungen über einen bestimmten Schwellenwert hinaus bewegt werden. So lässt sich ein Analogstick einfach auch als digitale Richtungseingabe verwenden:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Mehrere Gamepads {#multiple-gamepads}
Defold unterstützt mehrere Gamepads über das Betriebssystem des Geräts. Aktionen setzen das Feld `gamepad` der Tabelle `action` auf die Nummer des Gamepads, von dem die Eingabe stammt:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Verbinden und Trennen {#connect-and-disconnect}
Gamepad-Eingabebindungen bieten auch zwei separate Bindungen namens `Connected` und `Disconnected`, mit denen du erkennst, wenn ein Gamepad verbunden (einschließlich der bereits beim Start verbundenen Geräte) oder getrennt wird.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## Gamepad-Rohdaten {#raw-gamepads}

Gamepad-Eingabebindungen bieten außerdem eine separate Bindung namens `Raw`, die ungefilterte Eingaben (ohne Anwendung der Totzone) der Tasten, Achsen und Rundblickschalter (Hats) jedes verbundenen Gamepads liefert.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Gamepad-Einstellungsdatei {#gamepads-settings-file}
Zum Einrichten der Gamepad-Eingabe wird für jeden Gamepad-Hardwaretyp eine separate Zuordnungsdatei verwendet. Die Zuordnungen für bestimmte Gamepad-Modelle werden in einer *gamepads*-Datei festgelegt. Defold enthält eine integrierte gamepads-Datei mit Einstellungen für gängige Gamepads:

![Gamepad-Einstellungen](images/input/gamepads.png)

Wenn du eine neue Gamepad-Einstellungsdatei erstellen musst, steht dir dafür ein einfaches Werkzeug zur Verfügung:

[Klicke hier, um gdc.zip herunterzuladen](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Es enthält ausführbare Dateien für Windows, Linux und macOS. Starte es über die Kommandozeile:

```sh
./gdc
```

Das Werkzeug fordert dich auf, verschiedene Tasten auf deinem verbundenen Controller zu drücken. Anschließend gibt es eine neue gamepads-Datei mit den korrekten Zuordnungen für deinen Controller aus. Speichere die neue Datei oder führe sie mit deiner vorhandenen gamepads-Datei zusammen. Aktualisiere dann die Einstellung in *game.project*:

![Gamepad-Einstellungen](images/input/gamepad_setting.png)

### Nicht identifizierte Gamepads {#unidentified-gamepads}

Wenn ein Gamepad verbunden wird und keine Zuordnung dafür vorhanden ist, erzeugt es nur die Aktionen `connected`, `disconnected` und `raw`. In diesem Fall musst du die Gamepad-Rohdaten manuell den Aktionen in deinem Spiel zuordnen.

Du kannst prüfen, ob eine Eingabeaktion für ein Gamepad von einem unbekannten Gamepad stammt, indem du den Wert `gamepad_unknown` aus `action` ausliest:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
``` 

## Gamepads in HTML5
Gamepads werden in HTML5-Builds unterstützt und erzeugen dieselben Eingabeereignisse wie auf anderen Plattformen. Die Gamepad-Unterstützung basiert auf der [Gamepad API](https://www.w3.org/TR/gamepad/), die von den meisten Browsern unterstützt wird ([siehe diese Kompatibilitätsübersicht](https://caniuse.com/?search=gamepad)). Wenn der Browser die Gamepad API nicht unterstützt, ignoriert Defold alle Gamepad-Eingabeauslöser in deinem Projekt ohne Meldung. Du kannst feststellen, ob der Browser die Gamepad API unterstützt, indem du prüfst, ob die Funktion `getGamepads` am Objekt `navigator` vorhanden ist:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Wenn dein Spiel innerhalb eines `iframe` läuft, musst du außerdem sicherstellen, dass dem `iframe` die Berechtigung `gamepad` hinzugefügt wurde:

```html
<iframe allow="gamepad"></iframe>
```

### Standard-Gamepad

Wenn der Browser ein verbundenes Gamepad als Standard-Gamepad erkennt, verwendet es die Zuordnung für `Standard Gamepad` in der [Gamepad-Einstellungsdatei](/manuals/input-gamepads/#gamepads-settings-file) (eine Zuordnung für `Standard Gamepad` ist in der Datei `default.gamepads` unter `/builtins` enthalten). Ein Standard-Gamepad ist als Gerät mit 16 Tasten und 2 Analogsticks definiert, dessen Tastenanordnung der eines PlayStation- oder Xbox-Controllers ähnelt (weitere Informationen findest du in der [W3C-Definition und Tastenanordnung](https://w3c.github.io/gamepad/#dfn-standard-gamepad)). Wenn das verbundene Gamepad nicht als Standard-Gamepad erkannt wird, sucht Defold in der Gamepad-Einstellungsdatei nach einer Zuordnung, die dem Gamepad-Hardwaretyp entspricht.

## Gamepads unter Windows {#gamepads-on-windows}
Unter Windows werden derzeit nur XBox-360-Controller unterstützt. Um deinen 360-Controller mit deinem Windows-Rechner zu verbinden, [stelle sicher, dass er korrekt eingerichtet ist](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepads unter Android {#gamepads-on-android}

Gamepads werden in Android-Builds unterstützt und erzeugen dieselben Eingabeereignisse wie auf anderen Plattformen. Die Gamepad-Unterstützung basiert auf dem [Android-Eingabesystem für Tasten- und Bewegungsereignisse](https://developer.android.com/training/game-controllers/controller-input). Die Android-Eingabeereignisse werden mithilfe derselben *gamepad*-Datei wie oben beschrieben in Defold-Gamepad-Ereignisse umgewandelt.

Wenn du unter Android zusätzliche Gamepad-Bindungen hinzufügst, kannst du die folgenden Zuordnungstabellen verwenden, um Android-Eingabeereignisse in Werte für die *gamepad*-Datei zu übersetzen:

| Tastenereignis zu Tastenindex | Index |
|-----------------------------|-------|
| `AKEYCODE_BUTTON_A`           | 0     |
| `AKEYCODE_BUTTON_B`           | 1     |
| `AKEYCODE_BUTTON_C`           | 2     |
| `AKEYCODE_BUTTON_X`           | 3     |
| `AKEYCODE_BUTTON_L1`          | 4     |
| `AKEYCODE_BUTTON_R1`          | 5     |
| `AKEYCODE_BUTTON_Y`           | 6     |
| `AKEYCODE_BUTTON_Z`           | 7     |
| `AKEYCODE_BUTTON_L2`          | 8     |
| `AKEYCODE_BUTTON_R2`          | 9     |
| `AKEYCODE_DPAD_CENTER`        | 10    |
| `AKEYCODE_DPAD_DOWN`          | 11    |
| `AKEYCODE_DPAD_LEFT`          | 12    |
| `AKEYCODE_DPAD_RIGHT`         | 13    |
| `AKEYCODE_DPAD_UP`            | 14    |
| `AKEYCODE_BUTTON_START`       | 15    |
| `AKEYCODE_BUTTON_SELECT`      | 16    |
| `AKEYCODE_BUTTON_THUMBL`      | 17    |
| `AKEYCODE_BUTTON_THUMBR`      | 18    |
| `AKEYCODE_BUTTON_MODE`        | 19    |
| `AKEYCODE_BUTTON_1`           | 20    |
| `AKEYCODE_BUTTON_2`           | 21    |
| `AKEYCODE_BUTTON_3`           | 22    |
| `AKEYCODE_BUTTON_4`           | 23    |
| `AKEYCODE_BUTTON_5`           | 24    |
| `AKEYCODE_BUTTON_6`           | 25    |
| `AKEYCODE_BUTTON_7`           | 26    |
| `AKEYCODE_BUTTON_8`           | 27    |
| `AKEYCODE_BUTTON_9`           | 28    |
| `AKEYCODE_BUTTON_10`          | 29    |
| `AKEYCODE_BUTTON_11`          | 30    |
| `AKEYCODE_BUTTON_12`          | 31    |
| `AKEYCODE_BUTTON_13`          | 32    |
| `AKEYCODE_BUTTON_14`          | 33    |
| `AKEYCODE_BUTTON_15`          | 34    |
| `AKEYCODE_BUTTON_16`          | 35    |

([Android-Definitionen für `KeyEvent`](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Bewegungsereignis zu Achsenindex | Index |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([Android-Definitionen für `MotionEvent`](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Verwende diese Zuordnungstabelle zusammen mit einer Gamepad-Test-App aus dem Google Play Store, um herauszufinden, welchem Tastenereignis jede Taste deines Gamepads zugeordnet ist.
