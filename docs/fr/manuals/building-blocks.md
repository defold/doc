---
title: Les éléments constitutifs de Defold
brief: Ce manuel explique en détail le fonctionnement des objets de jeu, des composants et des collections.
---

#  Éléments constitutifs {#building-blocks}

La conception de Defold repose sur quelques concepts qu'il est essentiel de bien comprendre. Ce manuel présente les éléments constitutifs de Defold. Après l'avoir lu, poursuivez avec le [manuel sur l'adressage](/manuals/addressing) et le [manuel sur l'échange de messages](/manuals/message-passing). Un ensemble de [tutoriels](/tutorials/getting-started) est également accessible depuis l'éditeur pour vous aider à démarrer rapidement.

![Éléments constitutifs](images/building_blocks/building_blocks.png)

Vous utilisez trois types d'éléments de base pour construire un jeu Defold :

Collection
: Une collection est un fichier qui sert à structurer votre jeu. Dans les collections, vous construisez des hiérarchies d'objets de jeu et d'autres collections. Elles servent généralement à structurer les niveaux du jeu, les groupes d'ennemis ou les personnages composés de plusieurs objets de jeu.

Objet de jeu (game object)
: Un objet de jeu est un conteneur doté d'un identifiant, d'une position, d'une rotation et d'une échelle. Il sert à contenir des composants. Les objets de jeu servent généralement à créer les personnages jouables, les projectiles, le système de règles du jeu ou un chargeur de niveaux.

Composant (component)
: Les composants sont des entités placées dans des objets de jeu pour leur donner une représentation visuelle, sonore et/ou logique dans le jeu. Ils servent généralement à créer les sprites des personnages, les fichiers de script, à ajouter des effets sonores ou des effets de particules.

## Collections {#collections}

Les collections sont des structures arborescentes qui contiennent des objets de jeu et d'autres collections. Une collection est toujours stockée dans un fichier.

Lorsque le moteur Defold démarre, il charge une seule _collection bootstrap_, définie dans le fichier de paramètres *game.project*. La collection bootstrap est souvent nommée "main.collection", mais vous êtes libre de choisir le nom que vous voulez.

Une collection peut contenir des objets de jeu et d'autres collections (par référence au fichier de la sous-collection), imbriqués à n'importe quelle profondeur. Voici un exemple de fichier nommé "main.collection". Il contient un objet de jeu (avec l'identifiant "can") et une sous-collection (avec l'identifiant "bean"). Cette sous-collection contient à son tour deux objets de jeu : "bean" et "shield".

![Collection](images/building_blocks/collection.png)

Notez que la sous-collection dont l'identifiant est "bean" est stockée dans son propre fichier, nommé "/main/bean.collection", et que "main.collection" ne contient qu'une référence à ce fichier :

![Collection bean](images/building_blocks/bean_collection.png)

Vous ne pouvez pas adresser les collections elles-mêmes, car aucun objet ne correspond aux collections "main" et "bean" à l'exécution. Vous devez toutefois parfois utiliser l'identité d'une collection dans le _chemin_ vers un objet de jeu (consultez le [manuel sur l'adressage](/manuals/addressing) pour plus de détails) :

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Une collection est toujours ajoutée à une autre collection sous la forme d'une référence à un fichier de collection :

<kbd>Faites un clic droit</kbd> sur la collection dans la vue *Outline* et sélectionnez <kbd>Add Collection File</kbd>.

## Objets de jeu {#game-objects}

Les objets de jeu sont des objets simples qui ont chacun leur propre durée de vie pendant l'exécution de votre jeu. Ils possèdent une position, une rotation et une échelle qui peuvent chacune être modifiées et animées à l'exécution.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Les objets de jeu peuvent être utilisés vides (comme repères de position, par exemple), mais ils sont généralement dotés de divers composants, tels que des sprites, des sons, des scripts, des modèles, des factories et d'autres encore. Les objets de jeu sont soit créés dans l'éditeur et placés dans des fichiers de collection, soit générés dynamiquement à l'exécution au moyen de composants _factory_.

Les objets de jeu sont soit ajoutés directement dans une collection, soit ajoutés à une collection sous la forme d'une référence à un fichier d'objet de jeu :

<kbd>Faites un clic droit</kbd> sur la collection dans la vue *Outline* et sélectionnez <kbd>Add Game Object</kbd> (ajout direct) ou <kbd>Add Game Object File</kbd> (ajout par référence à un fichier).


## Composants {#components}

:[components](../shared/components.md)

Consultez la [présentation des composants](/manuals/components/) pour obtenir la liste de tous les types de composants disponibles.

## Objets ajoutés directement ou par référence {#objects-added-in-place-or-by-reference}

Lorsque vous créez un _fichier_ de collection, d'objet de jeu ou de composant, vous créez ce que nous appelons un prototype (également appelé « prefab » ou « blueprint » dans d'autres moteurs). Cela ajoute seulement un fichier à l'arborescence du projet ; rien n'est ajouté à votre jeu en cours d'exécution. Pour ajouter une instance de collection, d'objet de jeu ou de composant fondée sur un fichier prototype, vous en ajoutez une instance dans l'un de vos fichiers de collection.

Vous pouvez voir sur quel fichier repose une instance d'objet dans la vue Outline. Le fichier "main.collection" contient trois instances fondées sur des fichiers :

1. La sous-collection "bean".
2. Le composant script "bean" de l'objet de jeu "bean" dans la sous-collection "bean".
3. Le composant script "can" de l'objet de jeu "can".

![Instance](images/building_blocks/instance.png)

L'intérêt de créer des fichiers prototypes devient évident lorsque vous avez plusieurs instances d'un objet de jeu ou d'une collection et souhaitez toutes les modifier :

![Instances d'objet de jeu](images/building_blocks/go_instance.png)

Lorsque vous modifiez le fichier prototype, toute instance qui utilise ce fichier est immédiatement mise à jour.

![Modification du prototype d'objet de jeu](images/building_blocks/go_change_blueprint.png)

Ici, l'image du sprite du fichier prototype est modifiée, et toutes les instances qui utilisent ce fichier sont immédiatement mises à jour :

![Instances d'objet de jeu mises à jour](images/building_blocks/go_instance2.png)

## Relations parent-enfant entre objets de jeu {#childing-game-objects}

Dans un fichier de collection, vous pouvez construire des hiérarchies d'objets de jeu dans lesquelles un ou plusieurs objets de jeu sont les enfants d'un même objet de jeu parent. Il suffit de <kbd>faire glisser</kbd> un objet de jeu et de le <kbd>déposer</kbd> sur un autre pour que l'objet déplacé devienne un enfant de l'objet cible :

![Relations parent-enfant entre objets de jeu](images/building_blocks/childing.png)

Les hiérarchies parent-enfant entre objets constituent une relation dynamique qui détermine la manière dont les objets réagissent aux transformations. Toute transformation (déplacement, rotation ou mise à l'échelle) appliquée à un objet est à son tour appliquée aux enfants de cet objet, aussi bien dans l'éditeur qu'à l'exécution :

![Transformation d'un enfant](images/building_blocks/child_transform.png)

Inversement, les translations d'un enfant s'effectuent dans l'espace local du parent. Dans l'éditeur, vous pouvez choisir de modifier un objet de jeu enfant dans l'espace local ou dans l'espace du monde en sélectionnant <kbd>Edit ▸ World Space</kbd> (par défaut) ou <kbd>Edit ▸ Local Space</kbd>.

Il est également possible de changer le parent d'un objet à l'exécution en envoyant un message `set_parent` à cet objet.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Une erreur courante consiste à croire que la place d'un objet de jeu dans la hiérarchie des collections change lorsqu'il intègre une hiérarchie parent-enfant. Il s'agit pourtant de deux choses très différentes. Les hiérarchies parent-enfant modifient dynamiquement le graphe de scène, ce qui permet de rattacher visuellement les objets les uns aux autres. La seule chose qui détermine l'adresse d'un objet de jeu est sa place dans la hiérarchie des collections. L'adresse reste fixe pendant toute la durée de vie de l'objet.
:::
