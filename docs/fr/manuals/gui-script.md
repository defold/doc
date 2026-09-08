---
title: Scripts d'interface graphique dans Defold
brief: Ce manuel explique la programmation des interfaces graphiques par script.
---

# Scripts d'interface graphique {#gui-scripts}

Pour contrôler la logique de votre interface graphique et animer les nœuds, vous utilisez des scripts Lua. Les scripts d'interface graphique fonctionnent comme les scripts habituels d'objet de jeu (game object), mais sont enregistrés dans un autre type de fichier et ont accès à un autre ensemble de fonctions : celles du module `gui`.

## Ajouter un script à une interface graphique {#adding-a-script-to-a-gui}

Pour ajouter un script à une interface graphique, créez d'abord un fichier de script d'interface graphique en <kbd>cliquant avec le bouton droit</kbd> sur un emplacement dans le navigateur *Assets*, puis en sélectionnant <kbd>New ▸ Gui Script</kbd> dans le menu contextuel.

L'éditeur ouvre automatiquement le nouveau fichier de script. Il repose sur un modèle et contient des fonctions de cycle de vie vides, comme les scripts d'objet de jeu :

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

Pour attacher le script à un composant (component) d'interface graphique, ouvrez le fichier prototype du composant d'interface graphique (également désigné par les termes « prefabs » ou « blueprints » dans d'autres moteurs) et sélectionnez la racine dans *Outline* pour afficher les *Properties* de l'interface graphique. Affectez le fichier de script à la propriété *Script*.

![Script](images/gui-script/set_script.png)

Si le composant d'interface graphique a été ajouté à un objet de jeu quelque part dans votre jeu, le script s'exécutera désormais.

## L'espace de noms « gui » {#the-gui-namespace}

Les scripts d'interface graphique ont accès à l'espace de noms (namespace) `gui` et à [toutes les fonctions `gui`](/ref/gui). L'espace de noms `go` n'est pas disponible ; vous devez donc placer la logique des objets de jeu dans des composants script distincts et faire communiquer les scripts d'interface graphique et les scripts d'objet de jeu. Toute tentative d'utilisation des fonctions `go` provoquera une erreur :

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

## Échange de messages {#message-passing}

Tout composant d'interface graphique auquel un script est attaché peut communiquer avec d'autres objets dans l'environnement d'exécution de votre jeu par échange de messages. Il se comporte comme n'importe quel autre composant script.

Vous vous adressez au composant d'interface graphique comme à n'importe quel autre composant script :

```lua
local stats = { score = 4711, stars = 3, health = 6 }
msg.post("hud#gui", "set_stats", stats)
```

![échange de messages](images/gui-script/message_passing.png)

## Adressage des nœuds {#addressing-nodes}

Les nœuds d'interface graphique peuvent être manipulés par un script d'interface graphique attaché au composant. Chaque nœud doit avoir un *Id* unique, défini dans l'éditeur :

![échange de messages](images/gui-script/node_id.png)

L'*Id* permet à un script d'obtenir une référence au nœud et de le manipuler avec les [fonctions de l'espace de noms `gui`](/ref/gui) :

```lua
-- extend the health bar by 10 units
local healthbar_node = gui.get_node("healthbar")
local size = gui.get_size(healthbar_node)
size.x = size.x + 10
gui.set_size(healthbar_node, size)
```

## Nœuds créés dynamiquement {#dynamically-created-nodes}

Pour créer un nouveau nœud par script à l'exécution, vous avez deux possibilités. La première consiste à créer des nœuds à partir de zéro en appelant les fonctions `gui.new_[type]_node()`. Elles renvoient une référence au nouveau nœud, que vous pouvez utiliser pour le manipuler :

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

![nœud dynamique](images/gui-script/dynamic_nodes.png)

L'autre méthode pour créer de nouveaux nœuds consiste à cloner un nœud existant avec la fonction `gui.clone()` ou une arborescence de nœuds avec la fonction `gui.clone_tree()` :

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

## Identifiants des nœuds dynamiques {#dynamic-node-ids}

Aucun identifiant n'est attribué aux nœuds créés dynamiquement. C'est un choix de conception. Les références renvoyées par `gui.new_[type]_node()`, `gui.clone()` et `gui.clone_tree()` suffisent pour accéder aux nœuds, et vous devriez conserver ces références.

```lua
-- Add a text node
local new_textnode = gui.new_text_node(vmath.vector3(100, 100, 0), "Hello!")
-- "new_textnode" contains the reference to the node.
-- The node has no id, and that is fine. There's no reason why we want
-- to do gui.get_node() when we already have the reference.
```
