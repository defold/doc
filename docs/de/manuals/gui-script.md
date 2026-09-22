---
title: GUI-Skripte in Defold
brief: Dieses Handbuch erklärt die Skriptprogrammierung für GUIs.
---

# GUI-Skripte {#gui-scripts}

Mit Lua-Skripten steuerst du die Logik deiner GUI und animierst Knoten (nodes). GUI-Skripte (GUI scripts) funktionieren wie normale Skripte für Spielobjekte (game objects), werden aber als anderer Dateityp gespeichert und haben Zugriff auf einen anderen Satz von Funktionen: die Funktionen des Moduls `gui`.

## Einer GUI ein Skript hinzufügen {#adding-a-script-to-a-gui}

Um einer GUI ein Skript hinzuzufügen, erstelle zunächst eine GUI-Skriptdatei, indem du im *Assets*-Browser an der gewünschten Stelle einen <kbd>Rechtsklick</kbd> ausführst und im eingeblendeten Kontextmenü <kbd>New ▸ Gui Script</kbd> auswählst.

Der Editor öffnet die neue Skriptdatei automatisch. Sie basiert auf einer Vorlage und enthält wie Spielobjekt-Skripte leere Lebenszyklusfunktionen:

```lua
function init(self)
   -- Add initialization code here
   -- Remove this function if not needed
end

function final(self)
   -- Add finalization code here
   -- Remove this function if not needed
end

function update(self, dt)
   -- Add update code here
   -- Remove this function if not needed
end

function on_message(self, message_id, message, sender)
   -- Add message-handling code here
   -- Remove this function if not needed
end

function on_input(self, action_id, action)
   -- Add input-handling code here
   -- Remove this function if not needed
end

function on_reload(self)
   -- Add input-handling code here
   -- Remove this function if not needed
end
```

Um das Skript einer GUI-Komponente (GUI component) zuzuweisen, öffne die Prototypdatei der GUI-Komponente (in anderen Engines auch als „Prefabs“ oder „Blueprints“ bezeichnet) und wähle den obersten Eintrag in *Outline* aus, um den Bereich *Properties* der GUI anzuzeigen. Setze die Eigenschaft *Script* auf die Skriptdatei.

![Skript](images/gui-script/set_script.png)

Wenn die GUI-Komponente einem Spielobjekt irgendwo in deinem Spiel hinzugefügt wurde, wird das Skript jetzt ausgeführt.

## Der Namensraum „gui“ {#the-gui-namespace}

GUI-Skripte haben Zugriff auf den Namensraum `gui` und [alle `gui`-Funktionen](/ref/gui). Der Namensraum `go` ist nicht verfügbar. Du musst die Logik der Spielobjekte daher in Skriptkomponenten auslagern und die GUI-Skripte und Spielobjekt-Skripte miteinander kommunizieren lassen. Jeder Versuch, die `go`-Funktionen zu verwenden, führt zu einem Fehler:

```lua
function init(self)
   local id = go.get_id()
end
```

```txt
ERROR:SCRIPT: /main/my_gui.gui_script:2: You can only access go.* functions and values from a script instance (.script file)
stack traceback:
   [C]: in function 'get_id'
   /main/my_gui.gui_script:2: in function </main/my_gui.gui_script:1>
```

## Nachrichtenübermittlung {#message-passing}

Jede GUI-Komponente mit einem zugewiesenen Skript kann durch Nachrichtenübermittlung mit anderen Objekten in der Laufzeitumgebung deines Spiels kommunizieren. Sie verhält sich dabei wie jede andere Skriptkomponente.

Du adressierst die GUI-Komponente wie jede andere Skriptkomponente:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![Nachrichtenübermittlung](images/gui-script/message_passing.png)

## Knoten adressieren {#addressing-nodes}

GUI-Knoten lassen sich durch ein GUI-Skript verändern, das der Komponente zugewiesen ist. Jeder Knoten muss eine eindeutige *Id* haben, die im Editor festgelegt wird:

![Nachrichtenübermittlung](images/gui-script/node_id.png)

Über die *Id* kann ein Skript eine Referenz auf den Knoten erhalten und ihn mit den [Funktionen des Namensraums `gui`](/ref/gui) verändern:

```lua
-- extend the health bar by 10 units
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Dynamisch erstellte Knoten {#dynamically-created-nodes}

Um zur Laufzeit mit einem Skript einen neuen Knoten zu erstellen, hast du zwei Möglichkeiten. Die erste Möglichkeit ist, Knoten durch Aufrufe der Funktionen `gui.new_[type]_node()` neu zu erstellen. Diese geben eine Referenz auf den neuen Knoten zurück, mit der du ihn verändern kannst:

```lua
-- Create a new box node
local new_position = vmath.vector3(400, 300, 0)
local new_size = vmath.vector3(450, 400, 0)
local new_boxnode = gui.new_box_node(new_position, new_size)
gui.set_color(new_boxnode, vmath.vector4(0.2, 0.26, 0.32, 1))

-- Create a new text node
local new_textnode = gui.new_text_node(new_position, "Hello!")
gui.set_font(new_textnode, "sourcesans")
gui.set_color(new_textnode, vmath.vector4(0.69, 0.6, 0.8, 1.0))
```

![Dynamischer Knoten](images/gui-script/dynamic_nodes.png)

Alternativ kannst du neue Knoten erstellen, indem du einen vorhandenen Knoten mit der Funktion `gui.clone()` oder einen Knotenbaum mit der Funktion `gui.clone_tree()` klonst:

```lua
-- clone the healthbar
local healthbar_node = gui.get_node("healthbar")
local healthbar_node_2 = gui.clone(healthbar_node)

-- clone button node-tree
local button = gui.get_node("my_button")
local new_button_nodes = gui.clone_tree(button)

-- get the new tree root
local new_root = new_button_nodes["my_button"]

-- move the root (and children) 300 to the right
local root_position = gui.get_position(new_root)
root_position.x = root_position.x + 300
gui.set_position(new_root, root_position)
```

## Bezeichner dynamischer Knoten {#dynamic-node-ids}

Dynamisch erstellten Knoten wird kein Bezeichner zugewiesen. Das ist beabsichtigt. Die von `gui.new_[type]_node()`, `gui.clone()` und `gui.clone_tree()` zurückgegebenen Referenzen sind alles, was du für den Zugriff auf die Knoten brauchst. Du solltest diese Referenzen daher aufbewahren.

```lua
-- Add a text node
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contains the reference to the node.
-- The node has no id, and that is fine. There's no reason why we want
-- to do gui.get_node() when we already have the reference.
```
