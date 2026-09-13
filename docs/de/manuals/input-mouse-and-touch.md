---
title: Maus- und Berührungseingaben in Defold
brief: Dieses Handbuch erklärt, wie Maus- und Berührungseingaben funktionieren.
---

::: sidenote
Du solltest dich damit vertraut machen, wie Eingaben in Defold grundsätzlich funktionieren, wie du Eingaben empfängst und in welcher Reihenfolge deine Skriptdateien sie empfangen. Mehr über das Eingabesystem erfährst du im [Handbuch zur Eingabeübersicht](/manuals/input).
:::

# Mausauslöser {#mouse-triggers}
Mit Mausauslösern kannst du Eingaben von Maustasten und Mausrädern an Spielaktionen binden.

![](images/input/mouse_bindings.png)

::: sidenote
Die Maustasteneingaben `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` und `MOUSE_BUTTON_MIDDLE` entsprechen `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` und `MOUSE_BUTTON_3`.
:::

::: important
Die folgenden Beispiele verwenden die Aktionen aus der Abbildung oben. Wie bei allen Eingaben kannst du deine Eingabeaktionen beliebig benennen.
:::

## Maustasten {#mouse-buttons}
Maustasten erzeugen die Ereignisse `pressed`, `released` und `repeated`. Dieses Beispiel zeigt, wie du Eingaben der linken Maustaste erkennst (Drücken oder Loslassen):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- left mouse button pressed
        elseif action.released then
            -- left mouse button released
        end
    end
end
```

::: important
Eingabeaktionen für `MOUSE_BUTTON_LEFT` (oder `MOUSE_BUTTON_1`) werden auch bei einzelnen Berührungseingaben gesendet.
:::

## Mausrad {#mouse-wheel}
Mausradeingaben erkennen Scrollaktionen. Das Feld `action.value` ist `1`, wenn das Rad gedreht wird, und andernfalls `0`. (Scrollaktionen werden wie Tastendrücke behandelt. Defold unterstützt derzeit keine fein abgestuften Scrolleingaben auf Touchpads.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- mouse wheel is scrolled up
        end
    end
end
```

## Mausbewegung {#mouse-movement}
Mausbewegungen werden gesondert behandelt. Ereignisse für Mausbewegungen werden nur empfangen, wenn in deinen Eingabebindungen (input bindings) mindestens ein Mausauslöser eingerichtet ist.

Mausbewegungen werden nicht in den Eingabebindungen zugeordnet. Stattdessen wird `action_id` auf `nil` gesetzt und die Tabelle `action` mit der Position und der Positionsänderung der Maus gefüllt.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- let game object follow mouse/touch movement
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Auslöser für Berührungseingaben {#touch-triggers}
Auslöser für einzelne Berührungseingaben und Mehrfacheingaben per Berührung sind auf iOS- und Android-Geräten in nativen Anwendungen und in HTML5-Bundles verfügbar.

![](images/input/touch_bindings.png)

## Einzelne Berührungseingabe {#single-touch}
Auslöser für einzelne Berührungseingaben werden nicht im Abschnitt Touch Triggers der Eingabebindungen eingerichtet. Stattdessen **werden Auslöser für einzelne Berührungseingaben automatisch eingerichtet, wenn du Maustasteneingaben für `MOUSE_BUTTON_LEFT` oder `MOUSE_BUTTON_1` eingerichtet hast**.

## Mehrfacheingabe per Berührung {#multi-touch}
Auslöser für Mehrfacheingaben per Berührung füllen eine Tabelle namens `touch` innerhalb der Aktionstabelle. Die Elemente dieser Tabelle sind mit den ganzen Zahlen `1`--`N` indiziert, wobei `N` die Anzahl der Berührungspunkte ist. Jedes Element der Tabelle enthält Felder mit Eingabedaten:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Spawn at each touch point
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Mehrfacheingaben per Berührung darf nicht dieselbe Aktion zugewiesen werden wie Maustasteneingaben für `MOUSE_BUTTON_LEFT` oder `MOUSE_BUTTON_1`. Wenn du dieselbe Aktion zuweist, werden einzelne Berührungseingaben überschrieben, und du kannst keine Ereignisse für einzelne Berührungseingaben mehr empfangen.
:::

::: sidenote
Mit dem [Asset Defold-Input](https://defold.com/assets/defoldinput/) kannst du leicht virtuelle Bildschirmsteuerelemente wie Schaltflächen und Analogsticks mit Unterstützung für Mehrfacheingaben per Berührung einrichten.
:::


## Klicks oder Antippen auf Objekten erkennen {#detecting-click-or-tap-on-objects}
Zu erkennen, wann jemand eine visuelle Komponente (component) angeklickt oder angetippt hat, ist ein sehr häufiger Vorgang, der in vielen Spielen benötigt wird. Dabei kann es sich um die Interaktion mit einer Schaltfläche oder einem anderen UI-Element handeln oder um die Interaktion mit einem Spielobjekt (game object), etwa einer vom Spieler gesteuerten Einheit in einem Strategiespiel, einem Schatz in einem Level eines Dungeon-Crawlers oder einem Auftraggeber in einem RPG. Welche Vorgehensweise du verwendest, hängt von der Art der visuellen Komponente ab.

### Interaktionen mit GUI-Knoten erkennen {#detecting-interaction-with-gui-nodes}
Für UI-Elemente gibt es die Funktion `gui.pick_node(node, x, y)`. Sie gibt `true` oder `false` zurück, je nachdem, ob die angegebene Koordinate innerhalb der Grenzen eines GUI-Knotens (GUI node) liegt. Weitere Informationen findest du in der [API-Dokumentation](/ref/gui/#gui.pick_node:node-x-y), im [Beispiel für das Bewegen des Mauszeigers über einen Knoten](/examples/gui/pointer_over/) oder im [Schaltflächenbeispiel](/examples/gui/button/).

### Interaktionen mit Spielobjekten erkennen {#detecting-interaction-with-game-objects}
Bei Spielobjekten ist es komplizierter, Interaktionen zu erkennen, da beispielsweise die Verschiebung der Kamera und die Projektion des Render-Skripts die erforderlichen Berechnungen beeinflussen. Es gibt zwei grundsätzliche Vorgehensweisen, um Interaktionen mit Spielobjekten zu erkennen:

  1. Verfolge die Position und Größe der Spielobjekte, mit denen interagiert werden kann, und prüfe, ob die Maus- oder Berührungskoordinate innerhalb der Grenzen eines dieser Objekte liegt.
  2. Füge den Spielobjekten, mit denen interagiert werden kann, Kollisionsobjekte (collision objects) hinzu. Füge außerdem ein Kollisionsobjekt hinzu, das der Maus oder dem Finger folgt, und prüfe auf Kollisionen zwischen ihnen.

::: sidenote
Eine einsatzbereite Lösung, die mit Kollisionsobjekten Eingaben erkennt und dabei Ziehen und Klicken unterstützt, findest du im [Asset Defold-Input](https://defold.com/assets/defoldinput/).
:::

In beiden Fällen musst du zwischen den Koordinaten des Maus- oder Berührungsereignisses im Bildschirmkoordinatensystem und den Koordinaten der Spielobjekte im Weltkoordinatensystem umrechnen. Das ist auf verschiedene Arten möglich:

  * Verfolge manuell, welche Ansicht und Projektion das Render-Skript verwendet, und nutze diese Informationen, um in das Weltkoordinatensystem und daraus zurück umzurechnen. Ein Beispiel dafür findest du im [Kamerahandbuch](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Verwende eine [Kameralösung eines Drittanbieters](/manuals/camera/#third-party-camera-solutions) und nutze die bereitgestellten Funktionen zur Umrechnung vom Bildschirm- in das Weltkoordinatensystem.
