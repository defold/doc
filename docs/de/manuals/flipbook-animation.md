---
title: Handbuch zu Flipbook-Animationen in Defold
brief: Dieses Handbuch beschreibt, wie du Flipbook-Animationen in Defold verwendest.
---

# Flipbook-Animation {#flip-book-animation}

Eine Flipbook-Animation (flipbook animation) besteht aus einer Reihe von Einzelbildern, die nacheinander angezeigt werden. Die Technik ähnelt stark der traditionellen Folienanimation (siehe http://en.wikipedia.org/wiki/Traditional_animation). Sie bietet unbegrenzte Möglichkeiten, da jedes Einzelbild unabhängig bearbeitet werden kann. Da jedoch jedes Einzelbild als eigenes Bild gespeichert wird, kann der Speicherbedarf hoch sein. Wie flüssig die Animation wirkt, hängt auch von der Anzahl der pro Sekunde angezeigten Bilder ab. Eine höhere Anzahl von Bildern bedeutet allerdings meist auch mehr Arbeit. In Defold werden Flipbook-Animationen entweder als einzelne Bilder gespeichert, die einem [Atlas](/manuals/atlas) hinzugefügt werden, oder als [Kachelquelle](/manuals/tilesource) (tile source), in der alle Einzelbilder in einer horizontalen Folge angeordnet sind.

  ![Animationsbogen](images/animation/animsheet.png){.inline}
  ![Laufanimation in Schleife](images/animation/runloop.gif){.inline}

## Flipbook-Animationen abspielen {#playing-flip-book-animations}

Sprites und GUI-Box-Knoten (GUI box nodes) können Flipbook-Animationen abspielen, und du kannst ihre Wiedergabe zur Laufzeit umfassend steuern.

Sprites
: Um eine Animation zur Laufzeit abzuspielen, verwendest du die Funktion [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Ein Beispiel findest du weiter unten.

GUI-Box-Knoten
: Um eine Animation zur Laufzeit abzuspielen, verwendest du die Funktion [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Ein Beispiel findest du weiter unten.

::: sidenote
Der Wiedergabemodus `Once Ping Pong` spielt die Animation bis zum letzten Einzelbild ab, kehrt dann die Reihenfolge um und spielt sie rückwärts bis zum **zweiten** Einzelbild der Animation ab, nicht bis zum ersten. Dadurch lassen sich Animationen leichter aneinanderreihen.
:::

### Sprite-Beispiel {#sprite-example}

Angenommen, dein Spiel hat eine Ausweichfunktion namens "dodge", mit der die Spielfigur durch Drücken einer bestimmten Taste ausweichen kann. Du hast vier Animationen erstellt, um die Funktion durch visuelle Rückmeldungen zu unterstützen:

"idle"
: Eine wiederholt abgespielte Animation der Spielfigur im Ruhezustand.

"dodge_idle"
: Eine wiederholt abgespielte Animation der Spielfigur im Ruhezustand in der Ausweichhaltung.

"start_dodge"
: Eine einmal abgespielte Übergangsanimation, die die Spielfigur vom Stehen in die Ausweichhaltung versetzt.

"stop_dodge"
: Eine einmal abgespielte Übergangsanimation, die die Spielfigur aus der Ausweichhaltung zurück ins Stehen versetzt.

Das folgende Skript stellt die Logik bereit:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### Beispiel für einen GUI-Box-Knoten {#gui-box-node-example}

Wenn du eine Animation oder ein Bild für einen Knoten auswählst, weist du ihm tatsächlich die Bildquelle (Atlas oder Kachelquelle) und die Standardanimation in einem Schritt zu. Die Bildquelle ist im Knoten statisch festgelegt, aber die aktuell abzuspielende Animation kann zur Laufzeit geändert werden. Standbilder werden als Animationen mit einem Einzelbild behandelt. Ein Bild zur Laufzeit zu ändern, entspricht daher dem Abspielen einer anderen Flipbook-Animation für den Knoten:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Callbacks bei Abschluss {#completion-callbacks}

Die Funktionen `sprite.play_flipbook()` und `gui.play_flipbook()` unterstützen eine optionale Lua-Callback-Funktion als letztes Argument. Diese Funktion wird aufgerufen, wenn die Animation bis zum Ende abgespielt wurde. Bei wiederholt abgespielten Animationen wird die Funktion nie aufgerufen. Mit dem Callback kannst du nach Abschluss einer Animation Ereignisse auslösen oder mehrere Animationen aneinanderreihen. Beispiele:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
