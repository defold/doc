---
title: L'adressage dans Defold
brief: Ce manuel explique comment Defold résout le problème de l'adressage.
---

# Adressage {#addressing}

Le code qui contrôle un jeu en cours d'exécution doit pouvoir atteindre chaque objet de jeu (game object) et chaque composant (component) afin de déplacer, mettre à l'échelle, animer, supprimer et manipuler ce que le joueur voit et entend. Le mécanisme d'adressage de Defold le permet.

## Identifiants {#identifiers}

Defold utilise des adresses (ou des URL, mais mettons cela de côté pour le moment) pour faire référence aux objets de jeu et aux composants. Ces adresses sont constituées d'identifiants. Voici plusieurs exemples de la façon dont Defold utilise les adresses. Tout au long de ce manuel, nous allons examiner leur fonctionnement en détail :

```lua
local id = factory.create("#enemy_factory")
go.set("my_gameobject#my_label", "text", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Commençons par un exemple très simple. Supposons que vous ayez un objet de jeu doté d'un seul composant sprite. Vous disposez également d'un composant script pour contrôler l'objet de jeu. La configuration dans l'éditeur ressemblerait à ceci :

![Objet bean dans l'éditeur](images/addressing/bean_editor.png)

Vous souhaitez maintenant désactiver le sprite au démarrage du jeu afin de le faire apparaître plus tard. Il suffit pour cela de placer le code suivant dans "controller.script" :

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Ne vous inquiétez pas si le caractère '#' vous intrigue. Nous y reviendrons bientôt.

Cela fonctionnera comme prévu. Lorsque le jeu démarre, le composant script *s'adresse* au composant sprite au moyen de son identifiant "body" et utilise cette adresse pour lui envoyer un *message* "disable". Ce message spécial du moteur amène le composant sprite à masquer l'image du sprite. Schématiquement, la configuration ressemble à ceci :

![Objet bean](images/addressing/bean.png)

Les identifiants de la configuration sont définis par le développeur et doivent être uniques dans leur contexte de nommage. Ici, nous avons choisi de donner à l'objet de jeu l'identifiant "bean", de nommer son composant sprite "body" et le composant script qui contrôle le personnage "controller". Les identifiants utilisés dans les adresses URL sous forme de chaînes ne devraient pas contenir `:` ou `#`, car la syntaxe des URL réserve `:` au séparateur de socket et `#` au séparateur entre l'objet de jeu et le composant. L'analyseur d'URL ne rejette pas les autres signes de ponctuation.

::: sidenote
Si vous ne choisissez pas de nom, l'éditeur le fera. Chaque fois que vous créez un objet de jeu ou un composant dans l'éditeur, une propriété *Id* unique est automatiquement définie.

- Les objets de jeu reçoivent automatiquement un identifiant nommé "go", assorti d'un numéro ("go2", "go3", etc.).
- Les composants reçoivent un identifiant correspondant à leur type ("sprite", "sprite2", etc.).

Vous pouvez conserver ces noms attribués automatiquement si vous le souhaitez, mais nous vous encourageons à remplacer les identifiants par des noms pertinents et descriptifs.
:::

Ajoutons maintenant un autre composant sprite et donnons un bouclier au haricot :

![Objet bean](images/addressing/bean_shield_editor.png)

Le nouveau composant doit être identifié de manière unique dans l'objet de jeu. Si vous lui donniez le nom "body", le code du script ne permettrait pas de déterminer à quel sprite envoyer le message "disable". Nous choisissons donc l'identifiant unique (et descriptif) "shield". Nous pouvons désormais activer et désactiver les sprites "body" et "shield" à volonté.

![Objet bean](images/addressing/bean_shield.png)

::: sidenote
Si vous essayez d'utiliser un identifiant plusieurs fois, l'éditeur signalera une erreur ; cela ne pose donc jamais de problème en pratique :

![Objet bean](images/addressing/name_collision.png)
:::

Voyons maintenant ce qui se passe si vous ajoutez d'autres objets de jeu. Supposons que vous souhaitiez associer deux « haricots » dans une petite équipe. Vous décidez de nommer l'un des objets de jeu "bean" et l'autre "buddy". De plus, lorsque "bean" est inactif depuis un certain temps, il doit dire à "buddy" de commencer à danser. Pour cela, vous envoyez un message personnalisé nommé "dance" depuis le composant script "controller" de "bean" vers le script "controller" de "buddy" :

![Objet bean](images/addressing/bean_buddy.png)

::: sidenote
Deux composants distincts sont nommés "controller", un dans chaque objet de jeu, mais cela est parfaitement autorisé puisque chaque objet de jeu crée un nouveau contexte de nommage.
:::

Puisque le destinataire du message se trouve en dehors de l'objet de jeu qui envoie le message ("bean"), le code doit indiquer quel "controller" doit le recevoir. Il doit spécifier à la fois l'identifiant de l'objet de jeu cible et celui du composant. L'adresse complète du composant devient `"buddy#controller"` et se compose de deux parties distinctes.

- D'abord vient l'identifiant de l'objet de jeu cible ("buddy"),
- puis le caractère séparant l'objet de jeu du composant ("#"),
- et enfin l'identifiant du composant cible ("controller").

En revenant à l'exemple précédent contenant un seul objet de jeu, nous voyons qu'en omettant la partie de l'adresse cible qui contient l'identifiant de l'objet de jeu, le code peut adresser des composants de *l'objet de jeu actuel*.

Par exemple, `"#body"` désigne l'adresse du composant "body" dans l'objet de jeu actuel. Cette notation est très utile, car ce code fonctionnera dans *n'importe quel* objet de jeu, à condition qu'un composant "body" y soit présent.

## Collections {#collections}

Les collections permettent de créer des groupes ou des hiérarchies d'objets de jeu et de les réutiliser de manière contrôlée. Vous utilisez des fichiers de collection comme modèles (ou « prototypes » ou « prefabs ») dans l'éditeur lorsque vous ajoutez du contenu à votre jeu.

Supposons que vous souhaitiez créer un grand nombre d'équipes bean/buddy. Un bon moyen consiste à créer un modèle dans un nouveau *fichier de collection* (nommez-le "team.collection"). Créez les objets de jeu de l'équipe dans ce fichier de collection et enregistrez-le. Ensuite, placez une instance du contenu de ce fichier de collection dans votre collection bootstrap principale et donnez un identifiant à cette instance (nommez-la "team_1") :

![Objet bean](images/addressing/team_editor.png)

Avec cette structure, l'objet de jeu "bean" peut toujours faire référence au composant "controller" de "buddy" par l'adresse `"buddy#controller"`.

![Objet bean](images/addressing/collection_team.png)

Et si vous ajoutez une deuxième instance de "team.collection" (nommez-la "team_2"), le code exécuté dans les composants script de "team_2" fonctionnera tout aussi bien. L'instance de l'objet de jeu "bean" de la collection "team_2" peut toujours adresser le composant "controller" de "buddy" par l'adresse `"buddy#controller"`.

![Objet bean](images/addressing/teams_editor.png)

## Adressage relatif {#relative-addressing}

L'adresse `"buddy#controller"` fonctionne pour les objets de jeu des deux collections, car il s'agit d'une adresse *relative*. Chacune des collections "team_1" et "team_2" crée un nouveau contexte de nommage, ou espace de noms (namespace), si vous préférez. Defold évite les collisions de noms en tenant compte, pour l'adressage, du contexte de nommage créé par une collection :

![Identifiant relatif](images/addressing/relative_same.png)

- Dans le contexte de nommage "team_1", les objets de jeu "bean" et "buddy" sont identifiés de manière unique.
- De même, dans le contexte de nommage "team_2", les objets de jeu "bean" et "buddy" sont également identifiés de manière unique.

L'adressage relatif fonctionne en préfixant automatiquement l'adresse cible par le contexte de nommage actuel lors de sa résolution. Ce mécanisme est lui aussi extrêmement utile et puissant, car vous pouvez créer des groupes d'objets de jeu avec du code et les réutiliser efficacement dans tout le jeu.

### Raccourcis {#shorthands}

Defold fournit deux raccourcis pratiques qui permettent d'envoyer des messages sans spécifier une URL complète :

:[Shorthands](../shared/url-shorthands.md)

## Chemins des objets de jeu {#game-object-paths}

Pour bien comprendre le mécanisme de nommage, voyons ce qui se passe lorsque vous compilez et exécutez le projet :

1. L'éditeur lit la collection bootstrap ("main.collection") et tout son contenu (objets de jeu et autres collections).
2. Pour chaque objet de jeu statique, le compilateur crée un identifiant. Ces identifiants sont construits sous forme de « chemins » qui partent de la racine bootstrap et descendent dans la hiérarchie des collections jusqu'à l'objet. Un caractère '/' est ajouté à chaque niveau.

Dans l'exemple ci-dessus, le jeu s'exécute avec les quatre objets de jeu suivants :

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Les identifiants sont stockés sous forme de valeurs hachées. Le moteur d'exécution conserve également l'état de hachage de chaque identifiant de collection, utilisé pour poursuivre le hachage d'une chaîne relative et produire un identifiant absolu.
:::

À l'exécution, le regroupement en collections n'existe pas. Il n'existe aucun moyen de savoir à quelle collection appartenait un objet de jeu donné avant la compilation. Il n'est pas non plus possible de manipuler tous les objets d'une collection à la fois. Si vous avez besoin d'effectuer de telles opérations, vous pouvez facilement assurer vous-même ce suivi dans le code. L'identifiant de chaque objet est statique : il est garanti qu'il reste fixe pendant toute la durée de vie de l'objet. Vous pouvez donc conserver l'identifiant d'un objet en toute sécurité et l'utiliser ultérieurement.

## Adressage absolu {#absolute-addressing}

Il est possible d'utiliser les identifiants complets décrits ci-dessus pour l'adressage. Dans la plupart des cas, l'adressage relatif est préférable, car il permet de réutiliser le contenu, mais il existe des cas où l'adressage absolu devient nécessaire.

Par exemple, supposons que vous souhaitiez un gestionnaire d'IA qui suit l'état de chaque objet haricot. Vous souhaitez que les haricots rendent compte de leur état d'activité au gestionnaire, qui prend des décisions tactiques et leur donne des ordres en fonction de leur état. Dans ce cas, il serait tout à fait logique de créer un seul objet de jeu gestionnaire doté d'un composant script et de le placer aux côtés des collections d'équipe dans la collection bootstrap.

![Objet gestionnaire](images/addressing/manager_editor.png)

Chaque haricot est alors chargé d'envoyer des messages d'état au gestionnaire : "contact" s'il repère un ennemi ou "ouch!" s'il est touché et subit des dégâts. Pour que cela fonctionne, le script de contrôle du haricot utilise l'adressage absolu pour envoyer des messages au composant "controller" de "manager".

Toute adresse commençant par '/' est résolue depuis la racine du monde de jeu (game world). Celle-ci correspond à la racine de la *collection bootstrap* chargée au démarrage du jeu.

L'adresse absolue du script du gestionnaire est `"/manager#controller"` et cette adresse absolue sera résolue vers le bon composant, quel que soit l'endroit où elle est utilisée.

![Équipes et gestionnaire](images/addressing/teams_manager.png)

![Adressage absolu](images/addressing/absolute.png)

## Identifiants hachés {#hashed-identifiers}

Le moteur stocke tous les identifiants sous forme de valeurs hachées. Toutes les fonctions qui prennent en argument un composant ou un objet de jeu acceptent une chaîne de caractères, un hachage ou un objet URL. Nous avons vu ci-dessus comment utiliser les chaînes de caractères pour l'adressage.

Lorsque vous obtenez l'identifiant d'un objet de jeu, le moteur renvoie toujours un identifiant de chemin absolu haché :

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Vous pouvez utiliser un tel identifiant à la place d'un identifiant sous forme de chaîne, ou en construire un vous-même. Notez cependant qu'un identifiant haché correspond au chemin de l'objet, c'est-à-dire à une adresse absolue :

::: sidenote
Les adresses relatives doivent être fournies sous forme de chaînes de caractères, car le moteur calcule un nouvel identifiant haché à partir de l'état de hachage du contexte de nommage actuel (la collection), en ajoutant la chaîne fournie au hachage.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URL {#urls}

Pour compléter cette présentation, examinons le format complet des adresses Defold : l'URL.

Une URL est un objet, généralement écrit sous la forme d'une chaîne spécialement formatée. Une URL générique se compose de trois parties :

`[socket:][path][#fragment]`

socket
: Identifie le monde de jeu de la cible. Cela est important lorsque vous travaillez avec des [proxys de collection (collection proxies)](/manuals/collection-proxy) et sert alors à identifier la _collection chargée dynamiquement_.

path
: Cette partie de l'URL contient l'identifiant complet de l'objet de jeu cible.

fragment
: L'identifiant du composant cible dans l'objet de jeu spécifié.

Comme nous l'avons vu ci-dessus, vous pouvez omettre une partie, voire la plupart de ces informations dans la majorité des cas. Vous n'avez presque jamais besoin de spécifier le champ socket, et vous devez souvent, mais pas toujours, spécifier le champ path. Lorsque vous devez adresser des éléments dans un autre monde de jeu, vous devez spécifier la partie socket de l'URL. Par exemple, la chaîne URL complète du script "controller" dans l'objet de jeu "manager" ci-dessus est :

`"main:/manager#controller"`

et celle du script de contrôle de buddy dans team_2 est :

`"main:/team_2/buddy#controller"`

Nous pouvons leur envoyer des messages :

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Construction d'objets URL {#constructing-url-objects}

Les objets URL peuvent également être construits par programmation dans du code Lua :

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
