---
title: Defold pour les utilisateurs de Flash
brief: Ce guide présente Defold comme une alternative pour les développeurs de jeux Flash. Il aborde certains des concepts clés du développement de jeux Flash et explique les outils et méthodes correspondants dans Defold.
---

# Defold pour les utilisateurs de Flash {#defold-for-flash-users}

Ce guide présente Defold comme une alternative pour les développeurs de jeux Flash. Il aborde certains des concepts clés du développement de jeux Flash et explique les outils et méthodes correspondants dans Defold.

## Introduction {#introduction}

L'accessibilité et la facilité de prise en main figuraient parmi les principaux atouts de Flash. Les nouveaux utilisateurs pouvaient apprendre rapidement à utiliser le programme et créer des jeux simples en y consacrant peu de temps. Defold offre un avantage similaire en proposant un ensemble d'outils dédiés à la conception de jeux, tout en permettant aux développeurs expérimentés de créer des solutions avancées pour des besoins plus complexes (par exemple, en leur permettant de modifier le script de rendu par défaut).

Les jeux Flash sont programmés en ActionScript (dont la version la plus récente est la 3.0), tandis que les scripts Defold sont écrits en Lua. Ce guide ne compare pas en détail Lua et ActionScript 3.0. Le [manuel Defold](/manuals/lua) propose une bonne introduction à la programmation en Lua dans Defold et renvoie au très utile ouvrage [Programming in Lua](https://www.lua.org/pil/) (première édition), disponible gratuitement en ligne.

Un article de Jesse Warden propose une [comparaison élémentaire d'ActionScript et de Lua](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html), qui peut constituer un bon point de départ. Notez toutefois que les différences de conception entre Defold et Flash sont plus profondes que ce qui est visible au niveau du langage. ActionScript et Flash sont orientés objet au sens classique, avec des classes et de l'héritage. Defold n'a ni classes ni héritage. Il inclut le concept d'*objet de jeu* (game object), qui peut contenir une représentation audiovisuelle, un comportement et des données. Les opérations sur les objets de jeu s'effectuent à l'aide de *fonctions* disponibles dans les API Defold. De plus, Defold encourage l'utilisation de *messages* pour communiquer entre les objets. Les messages sont une construction de plus haut niveau que les appels de méthodes et ne sont pas destinés à être utilisés comme tels. Ces différences sont importantes et demandent un certain temps d'adaptation, mais elles ne seront pas abordées en détail dans ce guide.

Ce guide explore plutôt certains des concepts clés du développement de jeux dans Flash et présente leurs équivalents les plus proches dans Defold. Il aborde les similitudes et les différences, ainsi que les pièges courants, pour vous aider à démarrer rapidement votre transition de Flash vers Defold.

## Clips d'animation et objets de jeu {#movie-clips-and-game-objects}

Les clips d'animation (movie clips) sont un élément essentiel du développement de jeux Flash. Ce sont des symboles, chacun contenant un scénario qui lui est propre. Le concept équivalent le plus proche dans Defold est l'objet de jeu.

![objet de jeu et clip d'animation](images/flash/go_movieclip.png)

Contrairement aux clips d'animation Flash, les objets de jeu Defold n'ont pas de scénario. Un objet de jeu est composé de plusieurs composants (components). Les composants comprennent notamment les sprites, les sons et les scripts---parmi bien d'autres (pour en savoir plus sur les composants disponibles, consultez la [documentation sur les éléments de base](/manuals/building-blocks) et les articles associés). L'objet de jeu de la capture d'écran ci-dessous est constitué d'un sprite et d'un script. Le composant script sert à contrôler le comportement et l'apparence des objets de jeu tout au long de leur cycle de vie :

![composant script](images/flash/script_component.png)

Alors que les clips d'animation peuvent contenir d'autres clips d'animation, les objets de jeu ne peuvent pas *contenir* d'objets de jeu. Toutefois, les objets de jeu peuvent être *rattachés comme enfants* à d'autres objets de jeu, ce qui crée des hiérarchies que vous pouvez déplacer, mettre à l'échelle ou faire pivoter ensemble.

## Flash — création manuelle de clips d'animation {#flashmanually-creating-movie-clips}

Dans Flash, vous pouvez ajouter manuellement des instances de clips d'animation à votre scène en les faisant glisser depuis la bibliothèque vers le scénario. C'est ce qu'illustre la capture d'écran ci-dessous, où chaque logo Flash est une instance du clip d'animation `logo` :

![clips d'animation créés manuellement](images/flash/manual_movie_clips.png)

## Defold — création manuelle d'objets de jeu {#defoldmanually-creating-game-objects}

Comme indiqué précédemment, Defold n'a pas de concept de scénario. Les objets de jeu sont organisés en collections. Les collections sont des conteneurs (ou prefabs) qui regroupent des objets de jeu et d'autres collections. Dans le cas le plus simple, un jeu peut se composer d'une seule collection. Le plus souvent, les jeux Defold utilisent plusieurs collections, soit ajoutées manuellement à la collection bootstrap `main`, soit chargées dynamiquement par des [proxys de collection](/manuals/collection-proxy) (collection proxies). Ce concept de chargement de « niveaux » ou d'« écrans » n'a pas d'équivalent direct dans Flash.

Dans l'exemple ci-dessous, la collection `main` contient trois instances (répertoriées à droite, dans la fenêtre *Outline*) de l'objet de jeu `logo` (visible à gauche, dans la fenêtre du navigateur *Assets*) :

![objets de jeu créés manuellement](images/flash/manual_game_objects.png)

## Flash — référencement des clips d'animation créés manuellement {#flashreferencing-manually-created-movie-clips}

Pour faire référence à des clips d'animation créés manuellement dans Flash, vous devez utiliser un nom d'instance défini manuellement :

![nom d'instance Flash](images/flash/flash_instance_name.png)

## Defold — identifiant d'objet de jeu {#defoldgame-object-id}

Dans Defold, tous les objets de jeu et composants sont référencés par une adresse. Dans la plupart des cas, un simple nom ou une forme abrégée suffit. Par exemple :

- `"."` désigne l'objet de jeu actuel.
- `"#"` désigne le composant actuel (le script).
- `"logo"` désigne l'objet de jeu dont l'identifiant est `logo`.
- `"#script"` désigne le composant dont l'identifiant est `script` dans l'objet de jeu actuel.
- `"logo#script"` désigne le composant dont l'identifiant est `script` dans l'objet de jeu dont l'identifiant est `logo`.

L'adresse des objets de jeu placés manuellement est déterminée par la propriété *Id* qui leur est attribuée (voir en bas à droite de la capture d'écran). L'identifiant doit être unique dans le fichier de collection sur lequel vous travaillez. L'éditeur définit automatiquement un identifiant pour vous, mais vous pouvez le modifier pour chaque instance d'objet de jeu que vous créez.

![identifiant d'objet de jeu](images/flash/game_object_id.png)

::: sidenote
Vous pouvez obtenir l'identifiant d'un objet de jeu en exécutant le code suivant dans son composant script : `print(go.get_id())`. L'identifiant de l'objet de jeu actuel sera affiché dans la console.
:::

Le modèle d'adressage et l'échange de messages sont des concepts clés du développement de jeux Defold. Le [manuel sur l'adressage](/manuals/addressing) et le [manuel sur l'échange de messages](/manuals/message-passing) les expliquent en détail.

## Flash — création dynamique de clips d'animation {#flashdynamically-creating-movie-clips}

Pour créer dynamiquement des clips d'animation dans Flash, vous devez d'abord configurer ActionScript Linkage :

![liaison ActionScript](images/flash/actionscript_linkage.png)

Cela crée une classe (`Logo` dans ce cas), ce qui permet ensuite de créer de nouvelles instances de cette classe. Vous pouvez ajouter une instance de la classe `Logo` à la scène comme suit :

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold — création d'objets de jeu à l'aide de factories {#defoldcreating-game-objects-using-factories}

Dans Defold, la création dynamique d'objets de jeu s'effectue à l'aide de *factories*. Les factories sont des composants qui servent à créer des copies d'un objet de jeu donné. Dans cet exemple, une factory a été créée avec l'objet de jeu `logo` comme prototype :

![factory de logo](images/flash/logo_factory.png)

Notez que les factories, comme tous les composants, doivent être ajoutées à un objet de jeu avant de pouvoir être utilisées. Dans cet exemple, nous avons créé un objet de jeu nommé `factories` pour contenir notre composant factory :

![composant factory](images/flash/factory_component.png)

La fonction à appeler pour créer une instance de l'objet de jeu `logo` est la suivante :

```lua
local logo_id = factory.create("factories#logo_factory")
```

L'URL est un paramètre obligatoire de `factory.create()`. Vous pouvez également ajouter des paramètres facultatifs pour définir la position, la rotation, les propriétés et l'échelle. Pour plus d'informations sur le composant factory, consultez le [manuel sur les factories](/manuals/factory). Notez que l'appel à `factory.create()` renvoie l'identifiant de l'objet de jeu créé. Vous pouvez stocker cet identifiant dans une table (l'équivalent Lua d'un tableau) pour y faire référence ultérieurement.

## Flash — scène {#flashstage}

Dans Flash, vous connaissez Timeline (la partie supérieure de la capture d'écran ci-dessous) et Stage (visible sous Timeline) :

![scénario et scène](images/flash/stage.png)

Comme indiqué plus haut dans la section sur les clips d'animation, la scène est essentiellement le conteneur de plus haut niveau d'un jeu Flash et est créée chaque fois qu'un projet est exporté. Par défaut, la scène contient un enfant, *`MainTimeline`*. Chaque clip d'animation créé dans le projet possède son propre scénario et peut servir de conteneur à d'autres symboles (y compris des clips d'animation).

## Defold — collections {#defoldcollections}

L'équivalent de la scène Flash dans Defold est une collection. Au démarrage, le moteur crée un nouveau monde de jeu (game world) à partir du contenu d'un fichier de collection. Par défaut, ce fichier s'appelle `main.collection`, mais vous pouvez changer la collection chargée au démarrage en accédant au fichier de paramètres *game.project* situé à la racine de chaque projet Defold :

![game.project](images/flash/game_project.png)

Les collections sont des conteneurs utilisés dans l'éditeur pour organiser les objets de jeu et les autres collections. Le contenu d'une collection peut également être créé par script en cours d'exécution à l'aide d'une [factory de collection](/manuals/collection-factory/#spawning-a-collection), qui fonctionne de la même manière qu'une factory d'objets de jeu classique. Cela sert, par exemple, à créer des groupes d'ennemis ou un ensemble de pièces à collecter disposées selon un motif. Dans la capture d'écran ci-dessous, nous avons placé manuellement deux instances de la collection `logos` dans la collection `main`.

![collection](images/flash/collection.png)

Dans certains cas, vous souhaitez charger un monde de jeu entièrement nouveau. Le composant [proxy de collection](/manuals/collection-proxy/) vous permet de créer un nouveau monde de jeu à partir du contenu d'un fichier de collection. Cela peut servir à charger de nouveaux niveaux de jeu, des mini-jeux ou des cinématiques.

## Flash — scénario {#flashtimeline}

Le scénario Flash sert principalement à l'animation, à l'aide de diverses techniques image par image ou d'interpolations de forme ou de mouvement. Le paramètre FPS (images par seconde) global du projet définit la durée d'affichage d'une image. Les utilisateurs expérimentés peuvent modifier la fréquence d'images globale du jeu, voire celle de clips d'animation individuels.

Les interpolations de forme permettent d'interpoler des graphismes vectoriels entre deux états. Elles sont surtout utiles pour des formes et des applications simples, comme le montre l'exemple ci-dessous, où un carré est transformé en triangle par interpolation de forme :

![scénario](images/flash/timeline.png)

Les interpolations de mouvement permettent d'animer diverses propriétés d'un objet, notamment sa taille, sa position et sa rotation. Dans l'exemple ci-dessous, toutes les propriétés répertoriées ont été modifiées.

![interpolation de mouvement](images/flash/tween.png)

## Defold — animation de propriétés {#defoldproperty-animation}

Defold utilise des images matricielles plutôt que des graphismes vectoriels et n'a donc pas d'équivalent à l'interpolation de forme. En revanche, l'interpolation de mouvement possède un équivalent puissant : l'[animation de propriétés](/ref/go/#go.animate). Celle-ci s'effectue par script, à l'aide de la fonction `go.animate()`. La fonction `go.animate()` interpole une propriété (telle que la couleur, l'échelle, la rotation ou la position) de sa valeur initiale à la valeur finale souhaitée, en utilisant l'une des nombreuses fonctions d'accélération disponibles (y compris des fonctions personnalisées). Là où Flash exigeait que l'utilisateur implémente les fonctions d'accélération plus avancées, Defold intègre [de nombreuses fonctions d'accélération](/manuals/property-animation/#easing) au moteur.

Alors que Flash utilise des images clés de graphismes dans un scénario pour l'animation, l'une des principales méthodes d'animation graphique de Defold consiste à animer des séquences d'images importées, à la manière d'un folioscope. Les animations sont organisées dans un composant d'objet de jeu appelé atlas. Dans cet exemple, nous avons un atlas pour un personnage de jeu avec une séquence d'animation nommée `run`. Celle-ci se compose d'une série de fichiers png :

![animation image par image](images/flash/flipbook.png)

## Flash — indice de profondeur {#flashdepth-index}

Dans Flash, la liste d'affichage détermine ce qui est affiché et dans quel ordre. L'ordre des objets dans un conteneur (comme la scène) est géré par un indice. Les objets ajoutés à un conteneur à l'aide de la méthode `addChild()` occupent automatiquement la position la plus haute de l'indice, qui commence à 0 et augmente avec chaque objet ajouté. Dans la capture d'écran ci-dessous, nous avons créé trois instances du clip d'animation `logo` :

![indice de profondeur](images/flash/depth_index.png)

Les positions dans la liste d'affichage sont indiquées par les nombres à côté de chaque instance de `logo`. En omettant le code qui gère la position x/y des clips d'animation, le résultat ci-dessus aurait pu être créé comme suit :

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

L'affichage d'un objet au-dessus ou en dessous d'un autre est déterminé par leurs positions relatives dans l'indice de la liste d'affichage. Vous pouvez bien l'illustrer en permutant les positions de deux objets dans cet indice, par exemple :

```as
swapChildren(logo2,logo3);
```

Le résultat ressemblerait à celui ci-dessous (avec la position dans l'indice mise à jour) :

![indice de profondeur](images/flash/depth_index_2.png)

## Defold — position z {#defoldz-position}

Les positions des objets de jeu dans Defold sont représentées par des vecteurs composés de trois variables : x, y et z. La position z détermine la profondeur d'un objet de jeu. Dans le [script de rendu](/manuals/render) par défaut, les positions z disponibles vont de -1 à 1.

::: sidenote
Les objets de jeu dont la position z se situe en dehors de l'intervalle de -1 à 1 ne sont pas rendus et ne sont donc pas visibles. C'est un piège courant pour les développeurs qui découvrent Defold : gardez-le à l'esprit lorsqu'un objet de jeu n'est pas visible alors que vous vous attendez à le voir.
:::

Contrairement à Flash, où l'éditeur ne gère les indices de profondeur qu'implicitement (et permet de les modifier avec des commandes comme *Bring Forward* et *Send Backward*), Defold vous permet de définir la position z des objets directement dans l'éditeur. Dans la capture d'écran ci-dessous, vous pouvez voir que `logo3` est affiché au-dessus des autres et possède une position z de 0.2. Les autres objets de jeu ont des positions z de 0.0 et 0.1.

![ordre selon l'axe z](images/flash/z_order.png)

Notez que la position z d'un objet de jeu imbriqué dans une ou plusieurs collections dépend de sa propre position z et de celle de tous ses parents. Par exemple, imaginez que les objets de jeu `logo` ci-dessus soient placés dans une collection `logos`, elle-même placée dans `main` (voir la capture d'écran ci-dessous). Si la collection `logos` avait une position z de 0.9, les positions z des objets de jeu qu'elle contient seraient de 0.9, 1.0 et 1.1. Par conséquent, `logo3` ne serait pas rendu, car sa position z est supérieure à 1.

![ordre selon l'axe z](images/flash/z_order_outline.png)

Vous pouvez bien sûr modifier la position z d'un objet de jeu par script. Supposons que le code ci-dessous se trouve dans le composant script d'un objet de jeu :

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Détection des collisions dans Flash avec `hitTestObject` et `hitTestPoint` {#flash-hittestobject-and-hittestpoint-collision-detection}

La détection de collisions de base dans Flash s'effectue à l'aide de la méthode `hitTestObject()`. Dans cet exemple, nous avons deux clips d'animation : `bullet` et `bullseye`. Ils sont illustrés dans la capture d'écran ci-dessous. Le rectangle englobant bleu apparaît lorsque vous sélectionnez les symboles dans l'éditeur Flash, et ce sont ces rectangles englobants qui déterminent le résultat de la méthode `hitTestObject()`.

![test de collision](images/flash/hittest.png)

La détection de collisions avec `hitTestObject()` s'effectue comme suit :

```as
bullet.hitTestObject(bullseye);
```

L'utilisation des rectangles englobants ne conviendrait pas dans ce cas, car une collision serait détectée dans la situation ci-dessous :

![test de collision avec le rectangle englobant](images/flash/hitboundingbox.png)

Une alternative à `hitTestObject()` est la méthode `hitTestPoint()`. Cette méthode possède un paramètre `shapeFlag`, qui permet d'effectuer les tests de collision sur les pixels réels d'un objet plutôt que sur son rectangle englobant. La détection de collisions avec `hitTestPoint()` pourrait s'effectuer comme suit :

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Cette ligne testerait la position x et y du projectile (en haut à gauche dans ce cas) par rapport à la forme de la cible. Puisque `hitTestPoint()` teste un point par rapport à une forme, le choix du point (ou des points !) à tester est essentiel.

## Defold — objets de collision {#defoldcollision-objects}

Defold inclut un moteur physique qui peut détecter les collisions et permettre à un script d'y réagir. Pour détecter les collisions dans Defold, commencez par attribuer des composants d'objet de collision aux objets de jeu. Dans la capture d'écran ci-dessous, nous avons ajouté un objet de collision à l'objet de jeu `bullet`. L'objet de collision est représenté par le rectangle rouge transparent (visible uniquement dans l'éditeur) :

![objet de collision](images/flash/collision_object.png)

Defold inclut une version modifiée du moteur physique Box2D, qui peut simuler automatiquement des collisions réalistes. Ce guide suppose l'utilisation d'objets de collision cinématiques, car ce sont ceux qui ressemblent le plus à la détection de collisions dans Flash. Pour en savoir plus sur les objets de collision dynamiques, consultez le [manuel sur la physique](/manuals/physics) de Defold.

L'objet de collision possède les propriétés suivantes :

![propriétés de l'objet de collision](images/flash/collision_object_properties.png)

Une forme de boîte a été utilisée, car elle convient le mieux au graphisme du projectile. L'autre forme utilisée pour les collisions 2D, la sphère, servira pour la cible. Définir le type sur Kinematic signifie que votre script résout les collisions, au lieu du moteur physique intégré (pour plus d'informations sur les autres types, consultez le [manuel sur la physique](/manuals/physics)). Les propriétés *Group* et *Mask* déterminent respectivement le groupe de collision auquel appartient l'objet et celui avec lequel les collisions doivent être testées. La configuration actuelle signifie qu'un `bullet` ne peut entrer en collision qu'avec un `target`. Imaginez que la configuration soit modifiée comme suit :

![groupe et masque de collision](images/flash/collision_groupmask.png)

Les projectiles peuvent maintenant entrer en collision avec des cibles et avec d'autres projectiles. À titre de référence, nous avons configuré pour la cible un objet de collision qui se présente comme suit :

![objet de collision du projectile](images/flash/collision_object_bullet.png)

Notez que la propriété *Group* est définie sur `target` et *Mask* sur `bullet`.

Dans Flash, la détection de collisions n'a lieu que lorsque le script l'appelle explicitement. Dans Defold, elle s'effectue en continu en arrière-plan tant qu'un objet de collision reste activé. Lorsqu'une collision se produit, des messages sont envoyés à tous les composants d'un objet de jeu (notamment aux composants script). Il s'agit des messages [`collision_response` et `contact_point_response`](/manuals/physics-messages), qui contiennent toutes les informations nécessaires pour résoudre la collision de la manière souhaitée.

La détection de collisions de Defold a l'avantage d'être plus avancée que celle de Flash : elle peut détecter des collisions entre des formes relativement complexes avec très peu de configuration. Elle est automatique, ce qui vous évite de parcourir les différents objets des groupes de collision et d'effectuer explicitement des tests de collision. Son principal inconvénient est l'absence d'équivalent au paramètre `shapeFlag` de Flash. Cependant, dans la plupart des cas, des combinaisons des formes de base boîte et sphère suffisent. Pour les cas plus complexes, des formes personnalisées [sont possibles](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash — gestion des événements {#flashevent-handling}

Les objets événement et les écouteurs associés servent à détecter différents événements (par exemple, des clics de souris, des pressions sur des boutons ou le chargement de clips) et à déclencher des actions en réponse. Vous disposez de divers événements.

## Defold — fonctions de rappel et échange de messages {#defoldcall-back-functions-and-messaging}

L'équivalent Defold du système de gestion des événements de Flash comprend plusieurs éléments. Tout d'abord, chaque composant script dispose d'un ensemble de fonctions de rappel (callbacks) qui détectent des événements précis. Ce sont les suivantes :

init
:   Appelée lorsque le composant script est initialisé. Équivalente à la fonction constructeur dans Flash.

final
:   Appelée lorsque le composant script est détruit (par exemple, lorsqu'un objet de jeu créé dynamiquement est supprimé).

update
:   Appelée à chaque image. Équivalente à `enterFrame` dans Flash.

on_message
:   Appelée lorsque le composant script reçoit un message.

on_input
:   Appelée lorsqu'une entrée utilisateur (par exemple, de la souris ou du clavier) est envoyée à un objet de jeu qui possède le [focus d'entrée](/ref/go/#acquire_input_focus), ce qui signifie que l'objet reçoit toutes les entrées et peut y réagir.

on_reload
:   Appelée lorsque le composant script est rechargé.

Les fonctions de rappel répertoriées ci-dessus sont toutes facultatives et peuvent être supprimées si elles ne sont pas utilisées. Pour savoir comment configurer les entrées, consultez le [manuel sur les entrées](/manuals/input). Un piège courant se présente lorsque vous utilisez des proxys de collection : consultez [cette section](/manuals/input/#input-dispatch-and-on_input) du manuel sur les entrées pour plus d'informations.

Comme expliqué dans la section sur la détection des collisions, les événements de collision sont traités par l'envoi de messages aux objets de jeu concernés. Leurs composants script respectifs reçoivent le message dans leur fonction de rappel `on_message`.

## Flash — symboles de bouton {#flashbutton-symbols}

Flash utilise un type de symbole dédié aux boutons. Les boutons utilisent des méthodes de gestion des événements spécifiques (par exemple, `click` et `buttonDown`) pour exécuter des actions lorsqu'une interaction utilisateur est détectée. La forme graphique d'un bouton dans la section « Hit » du symbole de bouton détermine la zone cliquable du bouton.

![bouton](images/flash/button.png)

## Defold — scènes et scripts d'interface graphique {#defoldgui-scenes-and-scripts}

Defold n'inclut pas de composant bouton natif, et il n'est pas non plus facile de détecter des clics sur la forme d'un objet de jeu comme le permettent les boutons dans Flash. L'utilisation d'un composant [GUI](/manuals/gui) est la solution la plus courante, notamment parce que les positions des composants GUI de Defold ne sont pas affectées par la caméra du jeu (si vous en utilisez une). L'API GUI contient également des fonctions permettant de détecter si des entrées utilisateur, comme les clics et les événements tactiles, se trouvent dans les limites d'un élément d'interface graphique.

## Débogage {#debugging}

Dans Flash, la commande `trace()` est votre alliée pour le débogage. Son équivalent dans Defold est `print()`, qui s'utilise de la même manière que `trace()` :

```lua
print("Hello world!"")
```

Vous pouvez afficher plusieurs variables avec une seule fonction `print()` :

```lua
print(score, health, ammo)
```

Il existe également une fonction `pprint()` (affichage formaté), utile lorsque vous travaillez avec des tables. Cette fonction affiche le contenu des tables, y compris les tables imbriquées. Considérez le script ci-dessous :

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Il contient une table (`factions`) imbriquée dans une table (`world`). La commande `print()` classique afficherait l'identifiant unique de la table, mais pas son contenu :

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

L'utilisation de la fonction `pprint()` comme illustré ci-dessus donne des résultats plus utiles :

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Si votre jeu utilise la détection de collisions, vous pouvez activer ou désactiver le débogage physique en envoyant le message ci-dessous :

```lua
msg.post("@system:", "toggle_physics_debug")
```

Vous pouvez également activer le débogage physique dans les paramètres du projet. Avant son activation, notre projet se présente comme suit :

![sans débogage](images/flash/no_debug.png)

L'activation du débogage physique affiche les objets de collision ajoutés à nos objets de jeu :

![avec débogage](images/flash/with_debug.png)

Lorsqu'une collision se produit, les objets de collision concernés s'illuminent. Le vecteur de collision est également affiché :

![collision](images/flash/collision.png)

Enfin, consultez la [documentation du profileur](/ref/profiler/) pour savoir comment surveiller l'utilisation du processeur et de la mémoire. Pour plus d'informations sur les techniques de débogage avancées, consultez la [section sur le débogage](/manuals/debugging) du manuel Defold.

## Pour aller plus loin {#where-to-go-from-here}

- [Exemples Defold](/examples)
- [Tutoriels](/tutorials)
- [Manuels](/manuals)
- [Référence](/ref/go)
- [FAQ](/faq/faq)

Si vous avez des questions ou rencontrez des difficultés, les [forums Defold](//forum.defold.com) sont un excellent endroit pour demander de l'aide.
