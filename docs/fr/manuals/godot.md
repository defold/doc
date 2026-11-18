---
title: Defold pour les utilisateurs de Godot
brief: Ce guide présente Defold aux utilisateurs de Godot. Il met en parallèle les concepts des deux moteurs et montre comment utiliser les outils et les API correspondants.
---

# Defold pour les utilisateurs de Godot {#defold-for-godot-users}

Si vous connaissez Godot, vous avez déjà une bonne partie des connaissances nécessaires pour créer un jeu avec Defold. Ce guide montre comment vous appuyer sur cette expérience pour démarrer rapidement et explique les différences à connaître pour éviter les pièges courants. Nous avons utilisé Godot 4.7 pour rédiger cet article.

## Introduction {#introduction}

Defold est un moteur de jeu gratuit et multiplateforme pour les jeux 2D et 3D. Son éditeur fonctionne sous Windows, Linux et macOS. Le code source du moteur et de l’éditeur est disponible dans son intégralité sur [GitHub](https://github.com/defold/defold/). Vous pouvez le compiler vous-même ou télécharger la version adaptée à votre système.

À première vue, Defold ressemble beaucoup à Godot. Les deux moteurs permettent d’assembler un jeu à partir d’éléments réutilisables et de définir leur comportement par des scripts. Godot propose de nombreux nœuds spécialisés. Defold s’appuie sur un ensemble plus restreint de composants (components) à usage plus général, que vous pilotez avec des scripts et des modules Lua pour mettre en œuvre les mécaniques de jeu. Un personnage jouable peut par exemple être un objet de jeu (game object) qui réunit un sprite ou un modèle, un objet de collision et un script.

Defold privilégie un moteur d’exécution léger et une utilisation efficace des ressources, deux atouts particulièrement importants pour les jeux web et mobiles. Certaines limites du moteur sont fixées à l’avance pour permettre la préallocation de mémoire.

Defold propose moins d’éléments de jeu et d’interface prêts à l’emploi que Godot, mais vous pouvez combiner ou étendre ses composants pour obtenir les mêmes résultats. L’équipe veille à garder le cœur du moteur aussi léger que possible. Vous pouvez encore en réduire la taille en excluant les fonctionnalités inutilisées, ou l’enrichir avec des extensions natives et des modules Lua. Le [Defold Asset Portal](https://defold.com/assets/) regroupe des centaines de modules, de bibliothèques et d’extensions pour créer, par exemple, des interfaces complexes ou des pipelines de rendu avancés, ou encore simplifier certaines tâches de développement.

La [présentation des fonctionnalités de Defold](https://defold.com/product/) donne plus de détails.

## Installation {#installation}

1. Téléchargez la version de Defold adaptée à votre système depuis la [page de téléchargement](https://defold.com/download/).
2. Décompressez l’archive et lancez l’éditeur.

Vous pouvez créer et exécuter votre premier projet sans installer de gestionnaire de projets distinct ni de modèles d’exportation. Consultez le [manuel d’installation](/manuals/install/) pour connaître la procédure propre à votre plateforme.

Vous pouvez mettre Defold à jour directement depuis l’éditeur. Lorsque vous mettez un projet existant à jour, consultez les notes de version et testez le jeu sur ses plateformes cibles.

## Écran d’accueil {#welcome-screen}

L’écran d’accueil de Defold permet d’ouvrir un projet récent ou d’en créer un. Il joue un rôle comparable à celui du gestionnaire de projets de Godot.

![Gestionnaire de projets de Godot et écran d’accueil de Defold](images/godot/godot_1.png)

Pour créer un projet dans Defold, choisissez parmi les catégories suivantes :

- **Templates** pour démarrer avec un projet vide ou adapté à une plateforme précise.
- **Tutorials** pour découvrir Defold à travers des projets guidés.
- **Samples** pour explorer des exemples et des kits de démarrage que vous pouvez exécuter.

![Création d’un projet dans Godot et catégories de projets dans Defold](images/godot/godot_2.png)

La catégorie Samples comprend des projets de démarrage et des exemples semblables à ceux du Godot Asset Store.

![Exemples et projets de démarrage proposés dans Godot et Defold](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Présentation de l’éditeur Defold {#defold-editor-overview}

Vous reconnaîtrez les principaux panneaux, même si leurs noms et leurs emplacements diffèrent. Pour faciliter la comparaison, nous avons réorganisé les panneaux de Godot afin de les rapprocher de la disposition par défaut de Defold.

![Vue d’ensemble de l’éditeur Godot](images/godot/godot_4.png)
![Vue d’ensemble de l’éditeur Defold](images/godot/godot_5.png)

| Godot | Defold | Rôle dans l’éditeur Defold |
|---|---|---|
| Panneau FileSystem | Assets | Permet de gérer les fichiers et les dossiers du projet. Son arborescence correspond exactement à celle du projet sur le disque. |
| Vue 2D/3D et éditeurs de ressources | Main editor | S’adapte au fichier ouvert (collection, GUI, atlas, script, etc.). Peut être scindé en deux panneaux. |
| Panneau Scene | Outline | Affiche la structure de la ressource ouverte. Chaque ressource a sa propre arborescence et il n’existe pas d’arbre de scène global à l’exécution. |
| Inspector | Properties | Affiche les propriétés de l’objet, du composant ou de la ressource sélectionnés. |
| Output et Debugger | Tools | Regroupe notamment Console, Build Errors, Search Results et le débogueur. |
| Intégration du contrôle de version | Changed Files | Affiche les modifications lorsque le projet utilise Git. |

Dans l’éditeur 3D de Defold, une barre d’outils apparaît dans le coin supérieur droit. Vous trouverez sa description dans le [manuel de l’éditeur de scène](/manuals/scene-editing/#toolbar-overview).

### Orientation de la scène en 2D et en 3D {#2d-and-3d-scene-orientation}

:[Orientation de la scène en 2D et en 3D](../shared/2d-and-3d-scene-orientation.md)

### Panneaux {#panes}

Les panneaux de Defold restent dans la fenêtre de l’éditeur. Vous pouvez les redimensionner en faisant glisser leurs bords, ou les afficher et les masquer avec `F6`, `F7` et `F8` ou depuis le menu `View`.

![Affichage des panneaux dans l’éditeur](images/editor/editor_panes.png)

### Coordonnées {#coordinates}

Dans une collection Defold en 2D, si vous utilisez le script de rendu par défaut et qu’aucun composant caméra n’est présent, le point `(0, 0)` se trouve en bas à gauche de la fenêtre de jeu. L’axe Y positif pointe vers le **haut** et l’axe X positif vers la droite.

Dans le repère habituel de l’écran 2D de Godot, l’axe Y positif pointe vers le **bas**. Tenez compte de cette différence lorsque vous réutilisez des positions ou du code de déplacement.

![Les axes Y des repères 2D de Defold et de Godot pointent dans des directions opposées](images/godot/godot_6.png)

En 3D, l’axe Y positif de Godot pointe vers le haut, comme dans Defold. Defold utilise le même repère 3D pour les jeux 2D et 3D. En 2D, on travaille généralement dans le plan XY avec une projection orthographique. Vous pouvez configurer la caméra autrement si nécessaire.

![Orientation des axes dans les repères 3D de Defold et de Godot](images/godot/godot_7.png)

Pour plus de détails, consultez le [manuel de présentation de l’éditeur Defold](/manuals/editor/).

---

## Concepts fondamentaux {#key-concepts}

Dans Godot, vous assemblez des nœuds pour créer des **scènes**. Dans Defold, vous travaillez avec des composants, des objets de jeu et des collections d’objets de jeu.

Dans Godot, pour créer un personnage jouable, vous pouvez partir d’un `Node2D` avec un enfant `Sprite2D`, attacher un script au nœud racine, puis placer le personnage dans votre première scène (`Scene`).
Dans Defold, vous pouvez créer le personnage sous la forme d’un objet de jeu contenant les composants `Sprite` et `Script`, puis le placer dans une collection.

![Comparaison des nœuds d’un personnage dans Godot avec les objets de jeu et les composants dans Defold](images/godot/key_concepts.png)

Le [manuel des éléments constitutifs](/manuals/building-blocks/) présente ces concepts en détail.

### Objets de jeu {#game-objects}

Dans Defold, un **objet de jeu** est un *conteneur* de composants. Il possède :

- une **identité** ;
- une **transformation** (position, rotation, échelle).

Un objet de jeu peut jouer un rôle semblable à celui d’un `Node2D` ou d’un `Node3D` de Godot. Defold utilise un seul type d’objet de jeu : tous les objets ont une transformation 3D, y compris dans un jeu 2D.

Un objet de jeu peut avoir pour parent un autre objet de jeu, dont il hérite alors la transformation. Vous pouvez définir ces relations dans une collection ou les modifier à l’exécution. Changer le parent d’un objet ne modifie pas son adresse.

Dans une collection, vous pouvez définir un objet de jeu directement dans le fichier `.collection` en tant qu’objet **intégré**, ou ajouter une référence à un prototype `.go` réutilisable. Modifier la définition d’un objet intégré affecte la collection qui le contient. Les objets définis indépendamment conservent leur propre définition. Modifier un prototype `.go` met à jour les instances qui y font référence, sous réserve des valeurs redéfinies pour chaque instance. Plusieurs objets, même intégrés, peuvent partager une ressource de composant. Modifier cette ressource peut donc affecter tous les objets qui l’utilisent. Si vous réutilisez une collection, les modifications de ses objets intégrés se répercutent partout où cette collection est référencée.

### Composants {#components}

Les composants sont des éléments spécialisés qui donnent aux objets de jeu leur apparence, leurs propriétés physiques, leurs sons ou encore leur comportement.

Ajoutez à un objet de jeu un composant `Sprite` pour afficher une image, un composant `Sound` pour jouer un son ou un composant `Script` pour exécuter du code Lua.

Chaque composant appartient à un objet de jeu et ne peut avoir de composants enfants. Pour construire une hiérarchie, définissez des relations parent-enfant entre les objets de jeu d’une collection.

Dans Defold, vous ne pouvez pas changer le comportement d’un composant en lui attachant un script comme dans Godot. Vous pouvez le régler dans le panneau Properties. Vous pouvez aussi créer des composants personnalisés à l’aide d’extensions natives, comme avec les GDExtensions. Citons les composants officiels [Rive](https://github.com/defold/extension-rive) et [Spine](https://github.com/defold/extension-spine), ainsi que [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) et [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation), développés par la communauté.

Dans Defold, un script est lui-même un composant que vous pouvez ajouter à n’importe quel objet de jeu. Un même objet peut accueillir plusieurs composants, y compris plusieurs scripts.

Les composants ne sont pas imbriqués et sont indépendants des scripts personnalisés. Cette conception orientée données permet à Defold de les stocker efficacement en mémoire.

| Nœud Godot | Composant Defold | Remarques |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Affiche des textures 2D et des animations flipbook à partir d’un atlas (une texture regroupant plusieurs images) ou d’une source de tuiles. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` et leurs équivalents 3D | [Objet de collision](/manuals/physics-objects/) | Gère la physique et les déclencheurs. Les formes de collision sont définies directement dans le composant. Elles n’ont pas de nœuds enfants distincts. Vous pouvez choisir un objet statique, dynamique, cinématique ou déclencheur. |
| Script `.gd` attaché à un nœud | Script | Contient le code Lua qui définit la logique, traite les entrées et contrôle d’autres composants et objets de jeu. |
| `TileMapLayer` | [Tilemap](/manuals/tilemap/) | Affiche une carte sur une grille à partir d’une source de tuiles et des couches de la tilemap. |
| `Label` | [Nœud de texte GUI](/manuals/gui-text/) | Utilisez un nœud de texte GUI pour les textes d’interface et un [composant Label](/manuals/label/) pour le texte affiché dans le monde de jeu. |
| `AudioStreamPlayer` | [Sound](/manuals/sound/) | Joue des sons. Vous pouvez régler Speed, Pan et Gain. |
| `Camera2D` / `Camera3D` | [Caméra](/manuals/camera/) | Prend en charge les projections orthographique et en perspective. |
| Hiérarchie de `Control` / `CanvasLayer` | [GUI](/manuals/gui/) | Un composant GUI contient sa propre hiérarchie de nœuds (Box, Text, Pie, etc.). Un script `.gui_script` dédié contrôle l’interface. |
| `MeshInstance3D` | [Model](/manuals/model/) ou [Mesh](/manuals/mesh/) | Model affiche du contenu 3D importé. Mesh permet de créer une géométrie personnalisée à partir d’un tampon. |
| `CPUParticles2D` / `GPUParticles2D` et leurs équivalents 3D | [ParticleFX](/manuals/particlefx/) | Émet des particules 2D ou 3D configurées dans l’éditeur de particules de Defold. |
| `PackedScene.instantiate()` | Factory / Collection Factory | Des composants distincts définissent les objets de jeu ou les collections que vous pouvez créer à l’exécution. |

### Collections et mondes {#collections-and-worlds}

Une **collection** décrit des objets de jeu, leurs composants et leurs relations parent-enfant. Vous pouvez imbriquer une collection dans une autre pour réutiliser un groupe d’objets, comme avec une scène imbriquée dans Godot. Defold ne propose pas l’équivalent général des scènes héritées de Godot. Vous pouvez réutiliser des prototypes et des collections, puis personnaliser les instances à l’aide de propriétés ou de scripts.

Un fichier de collection décrit ce que Defold doit créer à l’exécution : les objets de jeu, leurs composants et leur hiérarchie. La collection elle-même ne correspond à aucun nœud racine et n’existe pas sous la forme d’un objet sur lequel vous pourriez appeler des méthodes.

Au démarrage, Defold lit le fichier `game.project`. Le paramètre **Bootstrap ▸ Main Collection** y désigne la première collection à charger. Defold crée ainsi le monde de jeu (game world) initial. Les objets placés dans des collections imbriquées font partie de ce même monde.

Un composant **factory de collection** (Collection Factory) instancie un groupe d’objets de jeu et leurs composants dans le monde **existant** auquel appartient la factory.

Un **proxy de collection** (Collection Proxy) charge une collection distincte et crée un **nouveau monde** avec son propre espace de noms (namespace) pour les adresses et sa propre simulation physique. Cette distinction importe, par exemple, pour faire apparaître un ennemi qui devra interagir avec la géométrie du niveau actuel ou pour charger un tout autre niveau, éventuellement de manière asynchrone. Ces deux opérations sont détaillées plus loin.

Godot utilise `PackedScene` pour instancier des objets comme pour changer de scène. Changer de scène avec le `SceneTree` revient, dans Defold, à charger un monde distinct avec un proxy de collection.

Le tableau suivant récapitule les correspondances :

| Godot | Defold | Remarques |
|---|---|---|
| `Node3D` avec des nœuds enfants | Objet de jeu avec des composants | Les composants apportent des fonctionnalités et un comportement. Les objets de jeu fournissent la transformation et l’identité. |
| Transformation d’un `Node2D` / `Node3D` | Transformation de l’objet de jeu | Présente sur tous les objets de jeu. |
| Scène / `PackedScene` | Prototype d’objet de jeu (`.go`) ou collection (`.collection`) | Un prototype décrit un objet. Une collection décrit un groupe d’objets et leur hiérarchie. |
| `PackedScene.instantiate()` | Factory ou factory de collection | Crée un objet ou un groupe d’objets de jeu dans le monde actuel et renvoie leurs identifiants. |
| Changement de scène avec `SceneTree` + `PackedScene.instantiate()` | Proxy de collection | Charge un nouveau monde distinct et y crée les objets de jeu. |

---

## Écriture du code {#code-writing}

L’éditeur Defold intègre un éditeur de code pour tous les fichiers texte et les scripts. Il propose entre autres la complétion automatique, le formatage et une vue Structure qui répertorie les données et les fonctions du fichier. Consultez la section [Utiliser l’éditeur de code intégré](/manuals/writing-code/#using-the-built-in-code-editor).

Vous pouvez aussi ouvrir tous les fichiers texte et les scripts Defold dans un éditeur externe. Defold propose plusieurs fonctionnalités pour faciliter son utilisation depuis un outil tel que VS Code. Consultez la section [Utiliser un éditeur de code externe](/manuals/writing-code/#using-an-external-code-editor).

### Lua et les scripts {#lua-and-scripts}

Dans Defold, les scripts qui définissent la logique du jeu utilisent Lua. Ce langage peut vous rappeler GDScript, avec quelques différences importantes. Defold prend aussi en charge Teal, un dialecte de Lua à typage statique. Comme les GDExtensions, les extensions natives de Defold permettent d’utiliser d’autres langages : C, C++, C#, Objective-C, Java ou JavaScript, selon la plateforme cible. Nous y reviendrons plus loin.

Dans Defold, vous travaillerez principalement avec les fichiers Lua suivants :

| Fichier | Rôle |
|---|---|
| `.script` | Définit la logique et le comportement du jeu et contrôle les autres objets de jeu et composants avec des API telles que `go`, `factory`, `sprite`, `tilemap` ou `physics`. |
| `.gui_script` | Définit le comportement d’une interface graphique avec l’API `gui`. |
| `.render_script` | Gère le rendu avec l’API `render`. |
| `.lua` | Contient un module Lua réutilisable que vous chargez avec `require()`, par exemple une bibliothèque de code ou des fonctions utilitaires. |

Une table Lua peut contenir des données, des fonctions, ou les deux. Pour organiser votre code, vous n’avez pas besoin de reproduire la hiérarchie de classes de GDScript. Placez la logique réutilisable dans des modules et appelez-la depuis le script qui gère le comportement concerné.

Defold utilise une version de Lua compatible avec Lua 5.1. Les particularités du langage et les différences entre plateformes sont décrites dans [Lua dans Defold](/manuals/lua/).

### Cycle de vie de l’application {#application-lifecycle}

Un jeu Defold commence par une phase d’initialisation et se termine par une phase de finalisation. Entre les deux, à chaque image, une boucle met à jour les transformations et les composants, exécute le code et traite les messages.

![Cycle de vie d’une application Defold](images/application_lifecycle/application_lifecycle.png)

Comme Godot et d’autres moteurs, Defold appelle certaines fonctions de vos scripts Lua à des étapes précises du cycle de vie de l’application. Leurs noms diffèrent, mais leurs rôles vous seront familiers.

| Godot | Defold | Rôle |
|---|---|---|
| `_ready()` | `init(self)` | Initialise les données de l’instance et acquiert le focus d’entrée si nécessaire. |
| `_process(delta)` | `update(self, dt)` | Effectue une mise à jour à chaque image. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | Effectue une mise à jour à pas de temps fixe lorsque cette option est activée. |
| `_input(event)` | `on_input(self, action_id, action)` | Traite les entrées transmises aux écouteurs de l’objet. |
| Fonction de rappel d’un signal | `on_message(self, message_id, message, sender)` | Reçoit les messages envoyés par les scripts ou les composants du moteur. |
| `_exit_tree()` | `final(self)` | Libère les ressources lors de la finalisation de l’instance du script. |

Dans Godot, la fonction `_ready()` de chaque enfant s’exécute avant celle de son parent. Dans Defold, l’ordre d’initialisation et de mise à jour des objets et de leurs composants n’est pas garanti. Utilisez des messages pour coordonner les objets sans supposer que le `init()` d’un objet s’exécutera en premier.

Pour utiliser `fixed_update()`, donnez à **Engine ▸ Fixed Update Frequency** une valeur positive telle que 60 dans `game.project` et activez **Physics ▸ Use Fixed Timestep**.

Defold fournit aussi `late_update(self, dt)` pour les opérations à effectuer après les mises à jour ordinaires et avant le rendu, comme l’ajustement d’une caméra. Une dernière mise à jour des transformations peut encore avoir lieu ensuite si nécessaire.

Désactiver un composant et le supprimer sont deux opérations distinctes.

Le [manuel du cycle de vie de l’application](/manuals/application-lifecycle/) décrit le déroulement complet et les fonctions de rappel disponibles pour chaque type de script.

### Données d’instance et données locales {#instance-data-vs-local-data}

Chaque instance d’un composant script reçoit dans les fonctions de rappel son propre `self`, dans lequel vous pouvez conserver son état, par exemple `self.health` ou `self.target`. Même deux composants script rattachés au même objet de jeu ont des `self` distincts. `self` est une donnée utilisateur (userdata) dont les champs sont accessibles comme ceux d’une table Lua. Ce type ne prend toutefois pas en charge certaines opérations sur les tables, comme `pairs(self)`. Les variables d’instance (`var`) jouent un rôle semblable dans Godot.

Godot traite chaque fichier `.gd` comme une définition de classe. Attachez un fichier `.gd` à dix ennemis : Godot crée dix instances distinctes de la classe, chacune avec sa propre copie des variables déclarées au niveau du fichier avec var.

Au chargement de la ressource de script, Defold exécute le fichier `.script` comme un bloc de code Lua. Chaque instance du composant script reçoit ensuite son propre `self` dans les fonctions de rappel du cycle de vie telles que `init(self)` et `update(self, dt)`.

En revanche, une variable locale déclarée au niveau du fichier `.script` est partagée par **toutes les instances** de ce script. Ces variables locales correspondent aux variables statiques de Godot (`static var`).

![Données propres à une instance et variable locale partagée dans Defold](images/lua/self_local.png)

Dans cet exemple, faire passer le champ `self.has_shield` d’une instance à `true` n’affecte pas les autres. En revanche, modifier la variable locale `color` peut avoir un effet sur toutes les instances utilisant ce fichier, puisqu’elles la partagent.

### Propriétés {#properties}

Pour déclarer une **propriété** d’instance modifiable, utilisez `go.property()`. Vous pouvez ensuite y accéder via `self`. Comme `@export` dans Godot, cette déclaration expose la valeur dans l’éditeur. Dans Defold, elle apparaît dans le panneau `Properties`.

![Propriétés d’un script dans l’éditeur Defold](images/script-properties/properties.png)

Dans Godot, voici un exemple en **GDScript** attaché à un `Node3D` :

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

Dans Defold, voici son équivalent en **Lua**, sous la forme d’un composant script :

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Le code Lua accède à la propriété via `self.speed`. Vous pouvez aussi fournir sa valeur à la création de l’objet. Les transformations de Defold utilisent des `vector3`, même en 2D : vous devez donc fournir une coordonnée Z.

Consultez les [propriétés de script](/manuals/script-properties/) pour connaître les types pris en charge et le [manuel des scripts](/manuals/script/) pour d’autres exemples.

---

## Messages et adressage {#messages-and-addressing}

Dans Godot, les signaux permettent à un objet de notifier les écouteurs connectés lorsqu’un événement se produit. Dans Defold, les scripts communiquent le plus souvent en envoyant un message à l’adresse d’un objet ou d’un composant.

Vous pouvez envoyer un message depuis n’importe quel script avec `msg.post()`. Un script reçoit et traite les messages dans sa fonction de rappel `on_message()`.

![Échange de messages dans Defold](images/message_passing/messages_overview.png)

Un personnage peut, par exemple, signaler un changement de score à l’interface de jeu (HUD).

Dans Godot, le nœud `Player` (`Node2D`) utilise le script `player.gd`. Son frère `GUI` (`CanvasLayer`) utilise `gui.gd` et contient un nœud Label nommé `ScoreText`.

![Configuration des nœuds pour l’envoi d’un signal dans Godot](images/godot/godot_signals.png)

Dans Defold, l’objet de jeu `player` possède le script `player.script`. L’objet de jeu `hud` possède un composant `gui` qui contient un nœud de texte `score` et utilise `hud.gui_script`.

![Objets et composants utilisés pour l’échange de messages dans Defold](images/godot/defold_messages.png)

### Envoyer des messages {#sending-messages}

Dans Godot, les nœuds Player et GUI ont le même parent. Player connecte son signal `score_changed` à une méthode du script de GUI, qui met ensuite à jour le nœud Label.

**GDScript**, dans `player.gd` :

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

Dans Godot, `Player` définit un signal appelé `score_changed`. Dans `_ready()`, il connecte ce signal à la méthode `set_score()` du script de GUI. Chaque appel à `collect()` augmente le score et émet le signal avec la nouvelle valeur.

Dans Defold, associez la touche **Space** à l’action `collect` dans vos liaisons d’entrée. L’objet `player` initialise son score dans `init()` et demande le focus d’entrée pour recevoir les événements d’entrée. À chaque appel, `collect(self)` incrémente le score et envoie un message `score_changed` à `/hud#gui`. La table du message contient le nouveau score.

**Lua**, dans `player.script` :

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

Dans Defold, le joueur envoie le message à l’adresse du destinataire. Il n’a pas besoin de connecter au préalable un signal à l’interface comme dans Godot. En combinant ce mécanisme avec l’adressage relatif de Defold, vous pouvez écrire des fonctions et des scripts réutilisables.

### Recevoir et traiter les messages {#receiving-and-handling-messages}

L’interface reçoit ensuite la valeur et met à jour le texte du score.

**GDScript**, dans `gui.gd`, attaché à `GUI` (`CanvasLayer`) :

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

Le script de GUI reçoit la valeur émise via `set_score()`, puis met à jour son nœud Label enfant, `ScoreText`. Le joueur n’accède pas directement à ce nœud et ne le modifie pas lui-même.

Le script GUI de Defold récupère d’abord le nœud de texte du score avec `gui.get_node()`. Lorsque le composant GUI reçoit un message, `on_message()` vérifie son identifiant. S’il s’agit de `score_changed`, le script lit `message.value` et met à jour le texte avec `gui.set_text()`.

**Lua**, dans `hud.gui_script`, associé au composant GUI :

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

Le message Defold est adressé au **composant** GUI. C’est le script GUI qui le reçoit et qui décide comment l’utiliser et quel nœud de texte mettre à jour. L’expéditeur n’a pas à connaître le nœud qui affiche le score.

Sur les deux captures d’écran, le texte initial est `Score: 0`. Lorsque le score change, les scripts de cet exemple remplacent tout le texte par la valeur numérique.

`msg.post()` place le message dans une file d’attente pour le distribuer ultérieurement. Il n’appelle pas immédiatement le destinataire et ne renvoie aucun résultat de son script. Les messages sont souvent distribués au cours de la même image. Toutefois, le nombre de passes de distribution est limité et une longue chaîne de messages peut se poursuivre au-delà de l’image en cours. Pour répondre, le destinataire peut envoyer un autre message à l’adresse de l’expéditeur transmise à `on_message()`. Consultez la section [Chaînes de messages](/manuals/message-passing/#message-chains).

La communication avec plusieurs écouteurs diffère également. Dans Godot, vous pouvez connecter un signal à plusieurs méthodes. Émettre ce signal avertit alors tous les écouteurs connectés. Un message Defold, lui, est envoyé à une adresse précise. Pour notifier plusieurs destinataires, envoyez un message à chacun ou mettez en place un système d’abonnement dans votre jeu.

### Trouver un objet grâce à l’adressage de Defold {#finding-an-object-addressing-in-defold}

Defold ne possède pas d’équivalent général de `get_node()` qui renverrait un objet Lua représentant une autre instance de script. Vous utilisez un identifiant ou une **URL** avec une fonction de l’API du moteur comme `go.get_position()`, `go.set()` ou `msg.post()`.

Une URL Defold comporte trois parties :

```lua
socket:/path#component
```

- **Socket** : identifie un monde, par exemple celui de la collection principale chargée au démarrage, ou un monde chargé par un proxy de collection.
- **Chemin** : identifie un objet de jeu dans ce monde.
- **Composant** : identifie un composant de cet objet.

Vous pouvez utiliser une URL complète ou omettre certaines parties pour former une adresse relative. Un script peut par exemple utiliser uniquement la partie composant pour s’adresser à un composant du même objet de jeu. Voici quelques adresses courantes :

| Adresse | Signification |
|---|---|
| `"#sprite"` | Le composant sprite de l’objet de jeu actuel. |
| `"/player#controller"` | Le composant controller de l’objet player dans le monde actuel. |
| `"level:/player#controller"` | Le composant controller dans le monde chargé nommé level. |
| `"."` | Raccourci désignant l’objet de jeu actuel (`Game Object`). Le message est distribué à ses composants. |
| `"#"` | Raccourci désignant le composant `Script` actuel. |

Les collections imbriquées peuvent ajouter des préfixes aux chemins des objets. Les relations parent-enfant utilisées pour les transformations ne modifient pas l’adresse d’un objet.

Lorsque vous créez des objets à l’exécution, conservez dans votre code les identifiants renvoyés par `factory.create()` ou `collectionfactory.create()`.

Les groupes Godot utilisés pour rechercher des objets dans la logique du jeu ou appeler `call_group()` n’ont pas d’équivalent intégré dans Defold. Pour ces usages, vous devez tenir votre propre registre d’objets ou organiser vous-même l’acheminement des messages.

Dans Defold, les groupes physiques des objets de collision servent à filtrer les collisions : le masque définit les groupes avec lesquels un objet peut entrer en collision. Ces groupes sont indépendants de la messagerie.

Lisez dès vos premiers pas les manuels de l’[adressage](/manuals/addressing/) et de l’[échange de messages](/manuals/message-passing/). Ils répondent à de nombreuses questions qui se posent lors d’un premier projet.

---

## Autoloads et état partagé {#autoloads-and-shared-state}

Les modules Lua permettent aussi d’appeler directement des fonctions Lua au lieu de passer par la messagerie de Defold.

Si vous stockez des données partagées dans un **Autoload** de Godot, un module Lua peut jouer ce rôle dans Defold. Enregistrez-le par exemple sous `modules/game_state.lua` et chargez-le avec `require "modules.game_state"`.

**GDScript**, avec `game_state.gd` enregistré comme Autoload sous le nom `GameState` :

```gdscript
extends Node
var score: int = 0
```

Équivalent en **Lua**, dans `modules/game_state.lua` :

```lua
local M = { score = 0 }
return M
```

Un autre script peut alors utiliser les données partagées :

**GDScript** :

```gdscript
func add_point():
    GameState.score += 1
```

**Lua** :

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

La fonction `require()` met le module en cache. Les scripts qui le chargent partagent donc la table qu’il renvoie. Les scripts d’objets de jeu, de GUI et de rendu partagent le même état Lua. Décharger un proxy de collection ne réinitialise pas les données du module. Vous pouvez les réinitialiser explicitement au début d’une nouvelle partie.

Un module Lua de Defold n’est pas un objet de jeu : il ne reçoit aucune fonction de rappel du cycle de vie, de la messagerie ou des entrées. Si votre Autoload exécute du code à chaque image, joue des sons ou gère les transitions entre niveaux, placez cette logique dans le script d’un objet de la collection. Vous pouvez aussi définir une fonction dans le module et l’appeler explicitement depuis les fonctions de rappel du script.

Module Lua `my_module` :

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Script Lua :
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Pour les données propres à chaque instance, le module peut renvoyer une fonction qui crée une nouvelle table. Vous pouvez ensuite stocker cette table dans `self`. Le [manuel des modules](/manuals/modules/) fournit plus de détails et explique les précautions à prendre lors du rechargement à chaud.

---

## Créer des objets et charger des niveaux {#spawning-objects-and-loading-levels}

### Factories {#factories}

Pour créer un objet de jeu à l’exécution dans Defold, ajoutez un composant **Factory** et renseignez sa propriété **Prototype** avec le fichier `.go` voulu.

Pour instancier les objets d’une collection, ajoutez un composant **Collection Factory** et indiquez le fichier `.collection` à utiliser. La factory crée le groupe d’objets en conservant leurs relations parent-enfant.

Dans l’exemple Godot ci-dessous, un nœud `Node2D` placé à l’origine de la scène utilise un script pour créer des projectiles :

**GDScript** :

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

Dans Defold, l’objet de jeu contient un composant factory dont l’identifiant est `bullet_factory`. La fonction `factory.create()` lui demande de créer l’objet de jeu désigné par sa propriété `Prototype`.

![Configuration d’une factory de projectiles dans Defold](images/godot/defold_factory.png)

Sur la capture d’écran, la factory est appelée dans `init()`. La fonction ci-dessous montre comment préciser la position de départ et renvoyer l’identifiant de l’objet créé.

**Lua** :

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

La fonction Defold renvoie l’**identifiant** de l’objet créé. Vous pouvez le passer aux fonctions de l’API `go`. Vous pouvez aussi construire l’URL d’un composant avec `msg.url(nil, id, "controller")` si l’objet créé possède un composant script nommé `controller`. L’identifiant lui-même ne fournit aucune méthode.

Une factory de collection renvoie une table qui associe à chaque identifiant d’objet du prototype celui de l’objet créé. Conservez-la pour pouvoir supprimer ces objets par la suite.

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

À la différence de `queue_free()` dans Godot, `go.delete(id)` ne supprime pas les enfants par défaut. Utilisez `go.delete(id, true)` pour supprimer un objet et tous ses descendants actuels. Si vous passez la table renvoyée par la factory à `go.delete(ids)`, seuls les objets énumérés seront supprimés. Les objets que vous leur avez rattachés après leur création seront conservés. Une suppression récursive à partir d’une racine connue, en revanche, supprime aussi tout autre objet placé depuis sous cette racine. Consultez la référence de [`go.delete()`](/ref/go/#go.delete).

Defold réserve de la mémoire à l’avance pour les objets de jeu et les composants. Si la création échoue parce qu’une limite est atteinte, vérifiez **Collection ▸ Max Instances** et les limites des composants concernés dans `game.project`. Augmenter toutes les limites augmente aussi la consommation de mémoire.

Les manuels des [factories](/manuals/factory/) et des [factories de collection](/manuals/collection-factory/) détaillent les propriétés, les transformations et le chargement dynamique.

### Proxies de collection {#collection-proxies}

Pour charger une collection dans Defold, par exemple pour un niveau, ajoutez un composant **Collection Proxy** à un objet persistant et associez sa propriété **Collection** au fichier `.collection` voulu.

![Configuration d’un proxy de collection dans Defold](images/godot/defold_proxy.png)

Envoyez `"load"` ou `"async_load"` avec `msg.post()`. Le proxy répond par un message `"proxy_loaded"` à la fin du chargement. Vous pouvez alors envoyer `"init"` et `"enable"` pour initialiser et démarrer le monde chargé. Utilisez à cet effet l’adresse fournie à on_message dans le paramètre `sender`.

Vous contrôlez ainsi quels mondes sont chargés et actifs. Contrairement à un changement de scène dans Godot, cette opération ne remplace pas automatiquement la scène actuelle. Pour décharger une autre collection et retirer son monde, envoyez le message `"unload"` à son proxy. Celui-ci désactive et finalise automatiquement le monde avant de le décharger, puis répond par `"proxy_unloaded"`. Vous pouvez également envoyer `"disable"` et `"final"` séparément pour contrôler le moment de ces étapes.

Les objets de collision qui appartiennent à deux mondes chargés par des proxies distincts n’entrent pas en collision, même si ces deux mondes sont chargés et visibles à l’écran en même temps. Leurs objets de jeu et leurs composants peuvent toutefois échanger des messages par des URL qui incluent le socket de destination.

Consultez le [manuel des proxies de collection](/manuals/collection-proxy/) avant de mettre en place vos transitions. Il explique le chargement et le déchargement, la transmission des entrées et le réglage de la fréquence de mise à jour d’un monde chargé.

## Ressources et fichiers du projet {#project-resources-and-assets}

Un projet Defold est un dossier contenant `game.project`, des scripts et des ressources. Le panneau **Assets** reflète son arborescence. La plupart des ressources Defold sont définies dans des fichiers texte, ce qui permet de consulter leurs modifications dans un outil de gestion de versions.

Lorsque vous compilez le jeu ou créez un bundle, Defold convertit les ressources sources aux formats utilisés à l’exécution. Les ressources référencées par la collection principale, les factories et les proxies de collection forment un arbre de dépendances. Un fichier placé dans le dossier du projet sans être référencé n’est pas inclus dans le bundle.

Il n’existe pas d’équivalent général des classes `Resource` personnalisées et des fichiers `.tres` de Godot. Utilisez les types de ressources de Defold pour le contenu destiné au moteur et des tables Lua ou des fichiers de données pour les données propres à votre jeu. L’[API `resource`](/ref/resource/) permet de créer ou de modifier les ressources prises en charge à l’exécution.

Les ressources d’une factory ordinaire sont chargées en même temps qu’elle. Pour différer leur chargement, activez **Load Dynamically**, puis utilisez `factory.load()` ou `collectionfactory.load()` pour les préparer de manière asynchrone. Le contenu d’un proxy de collection se charge à votre demande.

Charger un contenu plus tard depuis un bundle et le télécharger ultérieurement sont deux opérations distinctes. [Live Update](/manuals/live-update/) permet à Defold d’exclure du contenu du bundle initial pour le distribuer séparément.

Pour plus de détails, consultez le [manuel de gestion des ressources](/manuals/resource/).

---

## Entrées {#input}

L’`InputMap` de Godot correspond au fichier `.input_binding` de Defold. Vous pouvez associer un événement d’entrée (clavier, manette, souris, toucher ou saisie de texte) à une action nommée. Sélectionnez le fichier de liaisons dans **Input ▸ Game Binding** de `game.project`.

![Liaisons d’entrée dans Defold](images/input/defold_input.png)

Dans Defold, l’objet de jeu destinataire doit **acquérir le focus d’entrée**. Il rejoint alors la pile des entrées et ses composants script et GUI peuvent recevoir les appels à `on_input()`.

Sur la capture d’écran, la barre d’espace est associée à `collect`. L’exemple indépendant ci-dessous utilise une action nommée `fire`, que vous devez également ajouter à vos liaisons d’entrée.

**GDScript** :

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua** :

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

Selon le type d’entrée, la table `action` contient des champs tels que `pressed`, `released` et `value`.

L’action parcourt la pile en commençant par le dernier écouteur ayant acquis le focus. Renvoyez `true` depuis `on_input()` pour consommer une action, par exemple lorsqu’un menu traite un clic.

Dans un monde chargé par un proxy, l’objet qui porte le proxy et les écouteurs du monde chargé doivent chacun acquérir le focus d’entrée. Si un script qui fonctionnait cesse de recevoir les entrées après un changement de niveau, vérifiez ces deux étapes.

Consultez le [manuel des entrées](/manuals/input/), celui de la [souris et des entrées tactiles](/manuals/input-mouse-and-touch/) et celui des [manettes](/manuals/input-gamepads/) pour plus de détails.

---

## Physique et collisions {#physics-and-collisions}

Un **objet de collision** de Defold correspond aux corps physiques de Godot. Ce composant regroupe les paramètres physiques **et** les formes de collision. Dans `game.project`, vous choisissez entre la physique 2D et 3D. Le manifeste d’application permet aussi de sélectionner la version du moteur physique ou de désactiver entièrement la physique.

Defold propose quatre types d’objets de collision :

| Godot | Type Defold | Rôle |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Reste immobile. Les objets dynamiques réagissent à son contact. |
| `RigidBody2D` / `3D` | `Dynamic` | Le moteur physique simule le mouvement et résout les collisions. |
| `CharacterBody2D` / `3D` | `Kinematic` | Le moteur physique transmet les données de collision. Votre code doit traiter les collisions et les résoudre. |
| `Area2D` | `Trigger` | Signale uniquement les entrées et les sorties, sans réponse physique. |

Un objet cinématique de Defold se comporte différemment d’un `CharacterBody2D` qui utilise `move_and_slide()`. Defold détecte les contacts et vous transmet leurs données dans le message de collision. Votre script gère le mouvement et la réaction à la collision. Consultez le [manuel de résolution des collisions](/manuals/physics-resolving-collisions/) pour programmer le contrôle d’un personnage.

Les groupes et les masques utilisent des noms, là où Godot numérote les couches de collision. Pour qu’une collision soit enregistrée, **chaque objet doit inclure le groupe de l’autre dans son masque**.

![Groupes et masques de collision dans Defold](images/physics/collision_groups.png)

Sur cette capture d’écran, l’objet de jeu `danger` appartient au groupe `player` et l’objet `player` au groupe `danger`. Les noms des groupes peuvent différer des identifiants des objets. Ici, les masques permettent bien aux deux groupes d’interagir.

Par défaut, les objets de collision envoient des messages aux scripts attachés à leur objet de jeu. Traitez `"collision_response"`, `"contact_point_response"` et `"trigger_response"` dans `on_message()`. Les messages des déclencheurs contiennent un champ `enter` qui distingue une entrée d’une sortie. Tant que deux objets restent en contact, des messages de collision ou de contact peuvent se répéter. La réception d’un message ne signifie donc pas forcément qu’il y a eu un nouvel impact.

Vous pouvez aussi traiter les événements physiques à l’aide d’un [écouteur d’événements de collision](/manuals/physics-events/). Choisissez le mécanisme adapté à votre jeu : installer un écouteur remplace la distribution par défaut des messages physiques. Les scripts ne reçoivent alors plus ces messages.

Defold propose des formes de collision primitives et complexes. Vous les trouverez dans le [manuel des formes de collision](/manuals/physics-shapes).

![Forme de collision définie par un maillage](images/physics/mesh.png)

Pour en savoir plus sur la physique et ses API, consultez la [présentation de la physique](/manuals/physics/), les [objets de collision](/manuals/physics-objects/), les [messages de collision](/manuals/physics-messages/) et les [lancers de rayons](/manuals/physics-ray-casts/).

---

## Interface graphique (GUI) {#gui}

Dans Defold, l’interface se construit dans un **composant GUI** créé à partir d’un fichier `.gui`. Vous y agencez des nœuds tels que des boîtes, du texte ou des secteurs circulaires. Un script `.gui_script` dédié contrôle le composant, comme un script attaché à un `CanvasLayer` dans Godot.

Ces nœuds appartiennent à l’interface et sont indépendants de la hiérarchie des transformations de l’objet de jeu. Par défaut, l’interface est dessinée par-dessus le jeu. Elle reste en place lorsque la caméra du jeu ou l’objet qui porte le composant GUI se déplace.

Associez un `.gui_script` au composant pour contrôler les nœuds avec `gui.get_node()`, `gui.set_text()` et les autres fonctions de `gui`. L’API `gui` est réservée aux scripts GUI, et l’API `go` aux scripts d’objets de jeu. Utilisez des messages pour communiquer entre les deux, comme dans l’exemple du score.

Les modèles d’interface permettent de réutiliser la hiérarchie de nœuds d’une autre GUI, un peu comme on réutilise un nœud dans Godot.

Defold fournit des nœuds simples à assembler pour construire une interface. Godot propose pour sa part des widgets prêts à l’emploi, comme Button ou les conteneurs de mise en page. Pour créer un bouton dans Defold, vous pouvez combiner une boîte et du texte, gérer les entrées dans le script GUI et vérifier avec `gui.pick_node()` si le pointeur se trouve sur le nœud.

Les interfaces de Defold disposent aussi de **couches** (Layers), comparables aux couches de `CanvasLayer` dans Godot. Les couches de Defold portent des noms et leur ordre dans la liste Layers détermine l’ordre de dessin.

Les ancres, les pivots, les modes d’ajustement et les [mises en page d’interface graphique](/manuals/gui-layouts/) permettent d’adapter l’interface aux différents écrans. Ils répondent à certains des mêmes besoins que les conteneurs de mise en page de Godot, mais leur fonctionnement diffère.

Pour une interface plus complexe ou de plus grande taille, vous pouvez programmer vos propres outils de mise en page et widgets ou utiliser une bibliothèque de la communauté telle que [Druid](https://defold.com/assets/druid/).

Consultez les manuels de l’[interface graphique](/manuals/gui/) et des [scripts GUI](/manuals/gui-script/) pour plus de détails.

## Animation {#animation}

Plusieurs outils de Defold couvrent les usages du composant `AnimationPlayer` de Godot :

- L’**animation flipbook** lit une séquence d’images sur un sprite ou un nœud GUI de type boîte.
- L’**animation de modèle** joue des animations squelettiques importées sur des modèles 3D.
- L’**animation de propriété** interpole des valeurs avec `go.animate()` ou `gui.animate()`.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** et **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** sont d’autres formats d’animation disponibles sous forme d’extensions.

### Des tweens aux animations de propriétés de Defold {#tweens-defold-property-animations}

Un tween simple de Godot se traduit facilement par une animation de propriété dans Defold. Ces deux exemples déplacent un objet jusqu’à `X = 200` en une demi-seconde.

**GDScript**, sur un `Node2D` :

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

**Lua**, dans le script d’un objet de jeu :

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Pour enchaîner des changements de propriétés, jouer des sons ou déclencher des événements de jeu, coordonnez les différentes étapes en Lua. Defold ne dispose pas encore d’un éditeur de pistes d’animation dédié. Le Curve Editor du panneau Tools sert à modifier les courbes qui décrivent l’évolution des propriétés ParticleFX pendant la durée de vie d’une particule.

Consultez la [présentation des animations](/manuals/animation/), les [animations de propriétés](/manuals/property-animation/), les [animations flipbook](/manuals/flipbook-animation/) et les [animations de modèles](/manuals/model-animation/). La présentation renvoie également aux extensions Spine et Rive.

## Tilemaps {#tilemaps}

Un composant `Tilemap` de Defold utilise une **source de tuiles** qui contient une grille de tuiles. Vous pouvez peindre ces tuiles sur des couches dans l’éditeur de tilemaps intégré, puis les modifier à l’exécution avec l’API `tilemap`.

Les tilemaps intégrées de Defold utilisent une grille rectangulaire. Les jeux de terrains et les règles de placement automatique des tuiles de Godot ne se transposent pas encore directement dans Defold. Vous pouvez programmer le comportement souhaité ou utiliser un éditeur de cartes qui exporte vers Defold, comme [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) ou [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold).

Consultez le [manuel des tilemaps](/manuals/tilemap/).

---

## Pipeline de rendu {#rendering-pipeline}

Le pipeline de rendu de Defold est entièrement programmable avec un fichier `.render` personnalisé, un `.render_script` et des shaders. Le pipeline fourni par défaut convient à la plupart des jeux.

Le script de rendu par défaut prend en charge les contenus 2D et 3D courants. Un `.render_script` personnalisé contrôle les passes de dessin, les cibles de rendu et les autres opérations de rendu. Il peut sélectionner des groupes de composants à l’aide de prédicats fondés sur les étiquettes des matériaux. Defold prend en charge le rendu physiquement réaliste (PBR) dès l’installation. La communauté propose également de nombreux pipelines et shaders personnalisés.


Defold utilise des shaders GLSL, avec des fichiers distincts pour les programmes de sommets et de fragments. Godot utilise son propre langage de shaders inspiré de GLSL et lui ajoute des éléments propres au moteur. Vous devrez donc parfois adapter les shaders issus de Godot ou d’autres sources comme Shadertoy. Le [manuel des shaders](/manuals/shader/) précise les contraintes à respecter dans Defold.

Les **matériaux** de Defold associent les programmes de sommets et de fragments (shaders), les textures ainsi que les constantes et les attributs des shaders. Vous pouvez prendre pour point de départ les matériaux par défaut du dossier `builtins`.

Consultez les manuels du [rendu](/manuals/render/), des [matériaux](/manuals/material/) et des [shaders](/manuals/shader/) pour modifier le comportement par défaut.

### Ordre de dessin et couches {#draw-order-and-layers}

L’entier `z_index` de Godot n’a pas d’équivalent direct dans les propriétés de Defold. Defold est un moteur 3D : il utilise une coordonnée Z dans l’espace. Selon la configuration du rendu, déplacer un objet sur l’axe Z ne revient pas forcément à le déplacer en profondeur, ni à changer son ordre de dessin comme avec un indice de tri 2D.

Dans la configuration orthographique **par défaut**, Defold affiche uniquement les objets dont la position Z est comprise entre −1 et 1. Vous pouvez par exemple utiliser 0,1 et 0,2 pour placer les objets sur des plans distincts. Un message au script de rendu permet de modifier cette plage. Dans cette configuration simple, la position Z de l’objet de jeu ou du composant sprite détermine l’ordre de profondeur : un objet dont le Z est élevé se dessine par-dessus celui dont le Z est plus faible. Le résultat rappelle `z_index` dans Godot. Une caméra en perspective ou une modification du `.render_script` peut changer ce comportement.

Les nœuds GUI ignorent la coordonnée Z du monde. Par défaut, les composants GUI sont dessinés dans une passe distincte après les sprites du monde. Changer la position Z d’un nœud GUI ne change donc pas son ordre de dessin. Cet ordre suit la hiérarchie de l’interface de haut en bas dans le panneau Outline. Les couches GUI (`Layers`) prennent le pas sur l’ordre des nœuds pour regrouper les appels de dessin, un peu comme les couches de `CanvasLayer`.

### Caméras et coordonnées {#cameras-and-coordinates}

Ajoutez un composant `Camera` à un objet de jeu et déplacez cet objet pour déplacer la caméra. Configurez une projection orthographique pour une vue 2D classique ou une projection en perspective pour une vue 3D.

Le script de rendu par défaut utilise automatiquement la dernière caméra activée. Sans caméra, le rendu adopte une vue orthographique 2D. Si le projet contient une seule caméra activée, le moteur utilise celle-ci. Vous pouvez commencer ainsi et personnaliser le rendu quand votre jeu l’exige.

La caméra détermine comment les coordonnées du monde sont projetées à l’écran. Lorsque vous traitez les entrées du pointeur dans le monde de jeu, utilisez les fonctions de conversion de l’[API caméra](/ref/camera/) pour passer des coordonnées du pointeur à celles du monde. Par défaut, la détection du nœud GUI sous le pointeur utilise toujours les coordonnées de l’interface.

Le [manuel de la caméra](/manuals/camera/) détaille la projection, le zoom et la conversion des coordonnées.

---

## Exporter un jeu {#exporting-a-game}

Dans Defold, l’exportation consiste à **créer un bundle**. Choisissez **Project ▸ Bundle**, sélectionnez la plateforme cible et configurez les options du bundle. L’éditeur fournit tous les outils de build. Vous n’avez donc pas à installer séparément de modèles d’exportation comme dans Godot.

Le fichier `game.project` contient les paramètres du projet et des plateformes, notamment la collection principale, les liaisons d’entrée et les dimensions de l’affichage. Les exigences de signature de la plateforme et les règles des boutiques peuvent toujours s’appliquer. Si votre projet utilise des extensions natives, le service de build dans le cloud nécessite une connexion réseau pour compiler votre moteur personnalisé. Vous pouvez aussi configurer ce service vous-même pour travailler en local.

La taille finale du bundle dépend des ressources, des extensions et des paramètres de build. Générez un rapport de build (`Build Report`) pour savoir ce que contient votre jeu.

Consultez les manuels sur la [création de bundles](/manuals/bundling/), les [paramètres du projet](/manuals/project-settings/) et [HTML5](/manuals/html5/). Testez rapidement un premier bundle sur votre plateforme cible, surtout si le jeu utilise des shaders, des extensions natives ou des services de cette plateforme.

## Bibliothèques et extensions {#libraries-and-extensions}

Vous pouvez ajouter au projet des **dépendances de bibliothèques** contenant des scripts et des ressources partagés. Ajoutez l’URL de leurs archives dans `game.project`, puis récupérez les bibliothèques. Le portail de ressources de Defold, l’[Asset Portal](https://defold.com/assets/), est un bon point de départ pour les trouver. Comme dans Godot, l’extension d’éditeur **Asset Store** permet de rechercher et de télécharger des ressources directement dans l’éditeur Defold.

Les **scripts et interfaces de l’éditeur** permettent d’ajouter des commandes, d’automatiser des tâches et de créer des interfaces personnalisées. Vous pouvez, par exemple, accélérer l’édition des niveaux, la création de ressources ou le placement automatique des tuiles. Ces scripts couvrent certains usages d’`EditorPlugin` et de `@tool` dans Godot, tout en utilisant l’API `editor` et le cycle de vie propres à Defold.

Les **extensions natives** permettent d’étendre le moteur au-delà de Lua. Elles peuvent exposer du code natif aux scripts, ajouter des composants ou intégrer des services propres à une plateforme. Leur rôle est comparable à celui de GDExtension, avec une API et un processus de build différents.

Consultez les manuels des [bibliothèques](/manuals/libraries/), des [scripts de l’éditeur](/manuals/editor-scripts/) et des [extensions natives](/manuals/extensions/).

## Rechargement à chaud {#hot-reload}

Defold permet de recharger à chaud les ressources d’un jeu en cours d’exécution. Compilez et lancez le jeu, modifiez une ressource prise en charge, enregistrez-la et choisissez **File ▸ Hot Reload** pour appliquer les changements. Le rechargement à chaud fonctionne aussi lorsque vous ciblez un build de débogage sur un appareil.

Recharger un script ne rappelle pas `init()`. Les données d’instance sont conservées : une nouvelle valeur d’initialisation n’apparaîtra donc pas automatiquement dans `self`. Utilisez `on_reload(self)` pour ajuster l’état existant, ou recompilez le jeu pour repartir de son état initial. Si un module Lua renvoie une nouvelle table au rechargement, les autres scripts conservent leurs références à l’ancienne. Le [manuel des modules](/manuals/modules/) fournit plus de détails.

Consultez le [manuel du rechargement à chaud](/manuals/hot-reload/).

## Points d’arrêt et débogage {#breakpoints-and-debugging}

Le débogueur intégré à l’éditeur propose des points d’arrêt, l’exécution pas à pas et l’inspection des données. Utilisez Console pour les messages du jeu en cours d’exécution et Build Errors pour les problèmes de build. Le profileur permet d’analyser la durée des images, la mémoire et le rendu. Les rapports de build indiquent la place qu’occupe chaque ressource dans le bundle.

Consultez les manuels du [débogage de la logique du jeu](/manuals/debugging-game-logic/) et du [profilage](/manuals/profiling/).

## Automatisation des flux de travail {#automated-workflows}

Defold propose plusieurs interfaces pour automatiser le développement et travailler avec des agents IA. Les scripts de l’éditeur automatisent les tâches répétitives. L’API HTTP de l’éditeur, documentée avec OpenAPI, permet aux outils externes et aux agents IA d’inspecter des projets, d’exécuter des commandes et de lancer des builds. Le service HTTP du moteur et l’extension Automation Bridge permettent d’inspecter un jeu en cours d’exécution, de simuler des entrées et de prendre des captures d’écran. Grâce à ces outils, des agents de programmation comme Codex, Claude Code et Cursor peuvent enchaîner les modifications du projet, les builds, les tests et les corrections.

Consultez les manuels de l’[automatisation](/manuals/automation/), de l’[API HTTP de l’éditeur](/manuals/editor-http-api/), du [service du moteur](/manuals/engine-service/) et des [tests automatisés](/manuals/automated-testing/).

---

## Pièges courants {#common-pitfalls}

### Utiliser une collection comme nœud racine {#treating-a-collection-as-a-root-node}

Une collection Defold décrit des objets de jeu et leurs relations, mais elle ne devient pas un objet racine à l’exécution. Pour coordonner les objets d’un niveau, ajoutez un objet de jeu avec son propre script. Consultez [Collections et mondes](#collections-and-worlds).

### Supprimer une hiérarchie {#deleting-a-hierarchy}

Dans Godot, `queue_free()` supprime aussi les descendants du nœud. Dans Defold, `go.delete(id)` laisse les objets enfants en place, sauf si vous demandez explicitement une suppression récursive. La section [Factories](#factories) montre comment supprimer une hiérarchie et comment nettoyer les objets créés par une factory de collection.

### Compter sur l’héritage de scènes {#expecting-scene-inheritance}

Defold ne propose pas le même système de scènes héritées que Godot. Vous ne pouvez donc pas redéfinir librement la structure d’une scène dérivée de la même façon. Réutilisez des prototypes et des collections, puis personnalisez les instances au moyen de propriétés ou de scripts. Consultez [Collections et mondes](#collections-and-worlds).

### Appeler un autre script à partir d’une référence à un objet {#calling-another-script-through-an-object-reference}

L’identifiant d’un objet de jeu Defold ne donne pas un accès général aux fonctions d’une autre instance de script. Utilisez des messages pour communiquer entre composants ou rassemblez les fonctions partagées dans un module Lua. Consultez [Messages et adressage](#messages-and-addressing) et [Autoloads et état partagé](#autoloads-and-shared-state).

### Stocker l’état d’une instance dans une variable locale au niveau du fichier {#keeping-instance-state-in-a-top-level-local}

Une variable locale déclarée au niveau du fichier de script est partagée par les instances qui utilisent ce fichier. La modifier pour une instance peut donc affecter toutes les autres. Stockez les données propres à chaque instance dans `self`, comme indiqué dans [Données d’instance et données locales](#instance-data-vs-local-data).

### Supposer que les entrées sont activées automatiquement {#assuming-input-is-enabled-automatically}

Un objet de jeu Defold doit acquérir le focus d’entrée pour que ses composants reçoivent les entrées. Dans un monde chargé par un proxy, l’objet qui porte le proxy doit lui aussi acquérir le focus. La section [Entrées](#input) détaille les liaisons, le focus et le fonctionnement de la pile des entrées.

### Attendre d’un objet cinématique qu’il glisse automatiquement {#expecting-automatic-sliding-from-a-kinematic-collider}

Defold détecte les contacts des objets de collision cinématiques, mais ne reproduit pas automatiquement le comportement de `move_and_slide()` de Godot. Votre script doit gérer le déplacement et la réponse aux collisions. Consultez [Physique et collisions](#physics-and-collisions).

### Configurer un seul masque de collision {#configuring-only-one-collision-mask}

Si un seul des deux objets est configuré pour interagir avec l’autre, la collision ne sera pas enregistrée. Chaque objet doit inclure le groupe de l’autre dans son masque. Consultez [Physique et collisions](#physics-and-collisions).

### Reprendre les coordonnées 2D telles quelles {#copying-2d-coordinates-unchanged}

L’axe Y de Godot et celui d’une configuration 2D classique de Defold ont des sens opposés. Du code de déplacement repris tel quel risque donc de déplacer les objets dans la mauvaise direction. En présence d’une caméra, les positions à l’écran et dans le monde diffèrent également. Consultez [Coordonnées](#coordinates) et [Caméras et coordonnées](#cameras-and-coordinates).

### Trier les nœuds GUI selon leur coordonnée Z dans le monde {#using-world-z-to-sort-gui-nodes}

Dans Defold, changer la position Z d’un nœud GUI n’a pas d’effet sur son ordre de dessin. Utilisez l’ordre des nœuds dans la hiérarchie de l’interface et les couches GUI, comme indiqué dans [Ordre de dessin et couches](#draw-order-and-layers).

### Attendre du rechargement à chaud qu’il redémarre l’objet {#expecting-hot-reload-to-restart-the-object}

Recharger un script à chaud ne relance pas `init()`. Les instances peuvent donc conserver leur état antérieur. La section [Rechargement à chaud](#hot-reload) explique comment gérer cet état et le rechargement des modules.

### Supposer que décharger un niveau efface l’état partagé {#expecting-a-level-unload-to-clear-shared-state}

Dans Godot comme dans Defold, un changement de niveau peut préserver l’état partagé : celui d’un Autoload ou celui d’un module Lua mis en cache. Réinitialisez explicitement les données partagées si nécessaire. À la différence d’un nœud Autoload, un module Lua ne reçoit pas automatiquement de fonctions de rappel. Consultez [Autoloads et état partagé](#autoloads-and-shared-state).

## Pour aller plus loin {#where-to-go-from-here}

Le [Defold Learn Hub](https://defold.com/learn/) rassemble les manuels, exemples, tutoriels, vidéos et cours qui vous aideront à faire vos premiers pas et à approfondir votre connaissance de Defold. Nous vous conseillons notamment les ressources suivantes :

- [Éléments constitutifs](/manuals/building-blocks/)
- [Adressage](/manuals/addressing/)
- [Échange de messages](/manuals/message-passing/)
- [Exemples Defold](/examples/)
- [Tutoriels](/tutorials/)
- [Référence de l’API](/ref/go/)

Si vous avez besoin d’aide, posez votre question sur le [forum Defold](https://forum.defold.com/) ou sur [Discord](https://defold.com/discord/). Joignez un petit projet et décrivez le comportement de Godot que vous souhaitez reproduire : les autres utilisateurs pourront ainsi vous aider plus facilement.
