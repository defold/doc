---
title: Script GUI in Defold
brief: Questo manuale spiega come usare gli script GUI.
---

# Script GUI {#gui-scripts}

Per controllare la logica della GUI e animare i nodi, usa gli script Lua. Gli script GUI funzionano come i normali script degli oggetti di gioco (game object), ma vengono salvati con un tipo di file diverso e hanno accesso a un insieme diverso di funzioni: quelle del modulo `gui`.

## Aggiungere uno script a una GUI {#adding-a-script-to-a-gui}

Per aggiungere uno script a una GUI, crea prima un file di script GUI: <kbd>fai clic con il pulsante destro</kbd> su una posizione nel pannello *Assets* e seleziona <kbd>New ▸ Gui Script</kbd> dal menu contestuale.

L'editor apre automaticamente il nuovo file dello script. Il file si basa su un modello e contiene funzioni del ciclo di vita vuote, proprio come gli script degli oggetti di gioco:

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

Per associare lo script a un componente GUI, apri il file del prototipo del componente GUI (noto anche come "prefab" o "blueprint" in altri motori) e seleziona il nodo radice nella vista *Outline* per visualizzare le *Properties* della GUI. Imposta la proprietà *Script* sul file dello script

![Script](images/gui-script/set_script.png)

Se il componente GUI è stato aggiunto a un oggetto di gioco in un punto qualsiasi del gioco, lo script verrà ora eseguito.

## Lo spazio dei nomi "gui" {#the-gui-namespace}

Gli script GUI hanno accesso allo spazio dei nomi `gui` e a [tutte le funzioni `gui`](/ref/gui). Lo spazio dei nomi `go` non è disponibile, quindi devi separare la logica degli oggetti di gioco in componenti script e far comunicare gli script GUI con quelli degli oggetti di gioco. Qualsiasi tentativo di usare le funzioni `go` causerà un errore:

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

## Scambio di messaggi {#message-passing}

Qualsiasi componente GUI a cui è associato uno script può comunicare con altri oggetti nell'ambiente di esecuzione del gioco tramite lo scambio di messaggi, comportandosi come qualsiasi altro componente script.

Puoi indirizzare i messaggi al componente GUI come faresti con qualsiasi altro componente script:

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![Scambio di messaggi](images/gui-script/message_passing.png)

## Indirizzamento dei nodi {#addressing-nodes}

I nodi GUI possono essere manipolati da uno script GUI associato al componente. Ogni nodo deve avere un *Id* univoco, impostato nell'editor:

![Scambio di messaggi](images/gui-script/node_id.png)

L'*Id* permette a uno script di ottenere un riferimento al nodo e manipolarlo con le [funzioni dello spazio dei nomi `gui`](/ref/gui):

```lua
-- extend the health bar by 10 units
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Nodi creati dinamicamente {#dynamically-created-nodes}

Per creare un nuovo nodo tramite uno script durante l'esecuzione hai due possibilità. La prima consiste nel creare nodi da zero chiamando le funzioni `gui.new_[type]_node()`. Queste restituiscono un riferimento al nuovo nodo che puoi usare per manipolarlo:

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

![Nodo dinamico](images/gui-script/dynamic_nodes.png)

L'alternativa per creare nuovi nodi consiste nel clonare un nodo esistente con la funzione `gui.clone()` oppure un albero di nodi con la funzione `gui.clone_tree()`:

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

## ID dei nodi dinamici {#dynamic-node-ids}

Ai nodi creati dinamicamente non viene assegnato un ID. È una scelta progettuale. I riferimenti restituiti da `gui.new_[type]_node()`, `gui.clone()` e `gui.clone_tree()` sono tutto ciò che serve per accedere ai nodi, quindi devi conservarli.

```lua
-- Add a text node
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contains the reference to the node.
-- The node has no id, and that is fine. There's no reason why we want
-- to do gui.get_node() when we already have the reference.
```
