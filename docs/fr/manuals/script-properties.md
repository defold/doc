---
title: Propriétés des composants script
brief: Ce manuel explique comment ajouter des propriétés personnalisées aux composants script et y accéder depuis l'éditeur et les scripts en cours d'exécution.
---

# Propriétés de script {#script-properties}

Les propriétés de script offrent un moyen simple et puissant de définir et d'exposer des propriétés personnalisées pour une instance particulière d'objet de jeu (game object). Vous pouvez modifier les propriétés de script d'instances particulières directement dans l'éditeur et utiliser leurs valeurs dans le code pour modifier le comportement d'un objet de jeu. Les propriétés de script sont très utiles dans de nombreux cas :

* Lorsque vous souhaitez remplacer des valeurs pour des instances particulières dans l'éditeur et ainsi améliorer la réutilisabilité du script.
* Lorsque vous souhaitez créer un objet de jeu avec des valeurs initiales.
* Lorsque vous souhaitez animer les valeurs d'une propriété.
* Lorsque vous souhaitez accéder aux données d'état d'un script depuis un autre. (Notez que si vous accédez fréquemment aux propriétés entre objets, il peut être préférable de déplacer les données vers un stockage partagé.)

Les cas d'utilisation courants consistent à définir les points de vie ou la vitesse de l'IA d'un ennemi donné, la teinte d'un objet à ramasser, l'atlas d'un sprite ou le message qu'un objet bouton doit envoyer lorsqu'il est actionné---et/ou la destination de ce message.

## Définir une propriété de script {#defining-a-script-property}

Les propriétés de script sont ajoutées à un composant script (script component) en les définissant avec la fonction spéciale `go.property()`. Cette fonction doit être utilisée au niveau supérieur du script---en dehors des fonctions du cycle de vie telles que `init()` et `update()`. La valeur par défaut fournie pour la propriété détermine son type : `number`, `boolean`, `hash`, `msg.url`, `vmath.vector3`, `vmath.vector4`, `vmath.quaternion` et `resource` (voir ci-dessous).

::: important
Notez que retrouver la chaîne d'origine à partir d'une valeur de hachage n'est possible que dans un build Debug, afin de faciliter le débogage. Dans un build Release, cette chaîne n'existe pas ; utiliser `tostring()` sur une valeur `hash` pour en extraire la chaîne n'a donc aucun sens.
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

Il est alors possible de définir les valeurs des propriétés pour toute instance de composant script créée à partir de ce script.

![Composant avec des propriétés](images/script-properties/component.png)

 Sélectionnez le composant script dans la vue *Outline* de l'éditeur : les propriétés apparaissent dans la vue *Properties*, où vous pouvez les modifier :

![Propriétés](images/script-properties/properties.png)

Toute propriété dont la valeur est remplacée par une nouvelle valeur propre à l'instance est affichée en bleu. Cliquez sur le bouton de réinitialisation à côté du nom de la propriété pour rétablir la valeur par défaut (définie dans le script).


::: important
Les propriétés de script sont analysées lors du build du projet. Les expressions utilisées comme valeurs ne sont pas évaluées. Cela signifie qu'une expression telle que `go.property("hp", 3+6)` ne fonctionnera pas, tandis que `go.property("hp", 9)` fonctionnera.
:::

## Accéder aux propriétés de script {#accessing-script-properties}

Toute propriété de script définie est disponible sous la forme d'un membre stocké dans `self`, la référence à l'instance du script :

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

Les propriétés de script définies par l'utilisateur sont également accessibles au moyen des fonctions `get`, `set` et `animate`, de la même manière que toute autre propriété :

```lua
-- another.script

-- increase "my_property" in "myobject#script" by 1
local val = go.get("myobject#my_script", "my_property")
go.set("myobject#my_script", "my_property", val + 1)

-- animate "my_property" in "myobject#my_script"
go.animate("myobject#my_script", "my_property", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 2.0)
```

## Objets créés par une factory {#factory-created-objects}

Si vous utilisez une factory pour créer l'objet de jeu, vous pouvez définir les propriétés de script au moment de sa création :

```lua
local props = { health = 50, target = msg.url("player") }
local id = factory.create("#can_factory", nil, nil, props)

-- Accessing factory-created script properties
local url = msg.url(nil, id, "can")
local can_health = go.get(url, "health")
```

Lorsque vous créez une hiérarchie d'objets de jeu au moyen de `collectionfactory.create()`, vous devez associer les identifiants des objets à des tables de propriétés. Ces associations sont regroupées dans une table transmise à la fonction `create()` :

```lua
local props = {}
props[hash("/can1")] = { health = 150 }
props[hash("/can2")] = { health = 250, target = msg.url("player") }
props[hash("/can3")] = { health = 200 }

local ids = collectionfactory.create("#cangang_factory", nil, nil, props)
```

Les valeurs de propriétés fournies via `factory.create()` et `collectionfactory.create()` remplacent toute valeur définie dans le fichier prototype ainsi que les valeurs par défaut du script.

Si plusieurs composants script attachés à un objet de jeu définissent la même propriété, chaque composant sera initialisé avec la valeur fournie à `factory.create()` ou à `collectionfactory.create()`.


## Propriétés de ressources {#resource-properties}

Les propriétés de ressources se définissent de la même manière que les propriétés de script pour les types de données de base :

```lua
go.property("my_atlas", resource.atlas("/atlas.atlas"))
go.property("my_font", resource.font("/font.font"))
go.property("my_material", resource.material("/material.material"))
go.property("my_texture", resource.texture("/texture.png"))
go.property("my_tile_source", resource.tile_source("/tilesource.tilesource"))
```

Lorsqu'une propriété de ressource est définie, elle apparaît dans la vue *Properties* comme toute autre propriété de script, mais sous la forme d'un champ de sélection de fichier ou de ressource :

![Propriétés de ressources](images/script-properties/resource-properties.png)

Vous accédez aux propriétés de ressources avec `go.get()` ou via `self`, la référence à l'instance du script, et vous les utilisez avec `go.set()` :

```lua
function init(self)
  go.set("#sprite", "image", self.my_atlas)
  go.set("#label", "font", self.my_font)
  go.set("#sprite", "material", self.my_material)
  go.set("#model", "texture0", self.my_texture)
  go.set("#tilemap", "tile_source", self.my_tile_source)
end
```
