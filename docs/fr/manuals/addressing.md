---
title: L'adressage dans Defold
brief: Ce guide explique comment Defold résout le problème de l'adressage.
---

# Adressage

Le code qui contrôle un jeu en cours d'exécution doit être capable d'atteindre chaque objet et composant afin de déplacer, mettre à l'échelle, animer, supprimer et manipuler ce que le joueur voit et entend. C'est possible grâce au mécanisme d'adressage de Defold.

## Identifiants

Defold utilise des adresses (ou des URL, mais mettons cela de côté pour le moment) pour faire référence aux objets de jeu (*game objects*) et aux composants (*components*). Ces adresses sont constituées d'identifiants. Voici plusieurs exemples de la façon dont Defold utilise les adresses. Tout au long de ce guide, nous allons examiner leur fonctionnement plus en détail :

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Commençons par un exemple très simple. Vous avez un objet de jeu avec un seul sprite (un composant nommé `body`). Vous disposez également d'un script (un autre composant nommé `controller`) pour contrôler l'objet de jeu. La configuration dans l'éditeur ressemble à ceci :

![Objet bean dans l'éditeur](images/addressing/bean_editor.png)

Pour désactiver le sprite au démarrage du jeu afin de le faire apparaître plus tard, placez le code suivant dans `controller.script` :

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Ne vous préoccupez pas du caractère `#`, nous y reviendrons plus tard.

Tout fonctionne comme prévu. Lorsque le jeu démarre, le composant script *adresse* le composant sprite par son identifiant `body` et utilise cette adresse pour lui envoyer un *message* `disable` (désactiver). Ce message spécial du moteur masque l'image du sprite. Schématiquement, la configuration ressemble à ceci :

![Objet bean et ses composants](images/addressing/bean.png)

Les identifiants de la configuration sont choisis par le développeur et doivent être uniques dans leur contexte de nommage. Ici, nous avons choisi de donner à l'objet de jeu l'identifiant `bean` (haricot), de nommer son composant sprite `body` et son composant script de contrôle `controller`.

::: sidenote
Si vous ne choisissez pas de nom, l'éditeur le fera. Chaque fois que vous créez un objet de jeu ou un composant, une propriété *Id* unique est automatiquement définie.

- Les objets de jeu reçoivent automatiquement un identifiant appelé `go`, avec un suffixe numérique (`go2`, `go3`, etc.).
- Les composants reçoivent un identifiant correspondant à leur type (`sprite`, `sprite2`, etc.).

Vous pouvez conserver ces noms attribués automatiquement si vous le souhaitez, mais nous vous encourageons à les remplacer par des noms plus appropriés et descriptifs.
:::

Ajoutons un nouveau sprite et donnons un bouclier au haricot (`bean`) :

![Ajout du bouclier à bean dans l'éditeur](images/addressing/bean_shield_editor.png)

Ce nouveau composant doit être identifié de manière unique dans l'objet de jeu. Si vous lui donnez le nom `body` (corps), le script ne saura pas quel sprite doit recevoir le message `disable`. C'est pourquoi nous choisissons l'identifiant unique (et descriptif) `shield` (bouclier). Nous pouvons désormais activer et désactiver les sprites `body` et `shield` à volonté.

![Composants body et shield de bean](images/addressing/bean_shield.png)

::: sidenote
Si vous essayez d'utiliser un même identifiant plusieurs fois, l'éditeur signalera une erreur ; ce cas ne pose donc aucun problème en pratique :

![Erreur de collision d'identifiants](images/addressing/name_collision.png)
:::

Voyons ce qui se passe lorsque vous ajoutez d'autres objets de jeu. Supposons que vous associiez deux haricots dans une petite équipe. Vous nommez l'un des objets de jeu `bean` et l'autre `buddy`. Lorsque `bean` est inactif depuis un certain temps, il doit dire à `buddy` de commencer à danser. Nous allons envoyer un message personnalisé `dance` depuis le script `controller` de `bean` vers le script `controller` de `buddy` :

![Échange de messages entre bean et buddy](images/addressing/bean_buddy.png)

::: sidenote
Nous avons deux composants `controller` distincts, un dans chaque objet de jeu. Cela ne pose aucun problème, puisque chaque objet de jeu crée un nouveau contexte de nommage.
:::

Puisque le destinataire du message se trouve en dehors de l'objet de jeu `bean` (l'expéditeur), le code doit indiquer quel composant `controller` doit recevoir le message. Il doit spécifier à la fois l'identifiant de l'objet de jeu cible et celui du composant. L'adresse complète du composant devient `buddy#controller` et se compose de deux parties distinctes :

- d'abord, l'identifiant de l'objet de jeu cible (`buddy`) ;
- ensuite, le caractère séparant l'objet de jeu du composant (`#`) ;
- enfin, l'identifiant du composant cible (`controller`).

En revenant à l'exemple précédent contenant un seul objet de jeu, nous voyons qu'en omettant l'identifiant de l'objet de jeu dans l'adresse cible, le code peut adresser des composants de *l'objet de jeu actuel*.

Par exemple, `"#body"` désigne l'adresse du composant `body` dans l'objet de jeu actuel. Cette notation est très utile, car ce code fonctionnera dans *n'importe quel* objet de jeu comportant un composant `body`.

## Collections

Les collections permettent de créer des groupes ou des hiérarchies d'objets de jeu et de les réutiliser de manière contrôlée. Vous utilisez des fichiers de collection comme modèles (ou « prototypes », ou encore « prefabs ») dans l'éditeur lorsque vous ajoutez du contenu à votre jeu.

Supposons que vous souhaitiez créer un grand nombre d'équipes `bean`/`buddy`. Un bon moyen consiste à créer un modèle dans un nouveau *fichier de collection* nommé `team.collection`. Créez les objets de jeu de l'équipe dans la collection et enregistrez-la. Ensuite, placez une instance du contenu de `team.collection` dans la collection bootstrap principale et donnez à cette instance l'identifiant `team_1` :

![Collection team dans l'éditeur](images/addressing/team_editor.png)

Avec cette structure, l'objet de jeu `bean` peut toujours faire référence au composant `controller` de `buddy` par l'adresse `"buddy#controller"`.

![Structure de la collection team](images/addressing/collection_team.png)

Si vous ajoutez une deuxième instance de `team.collection` nommée `team_2`, le code exécuté dans les composants script de `team_2` fonctionnera tout aussi bien. L'instance de l'objet de jeu `bean` de la collection `team_2` peut toujours adresser le composant `controller` de `buddy` par l'adresse `"buddy#controller"`.

![Deux instances de la collection team](images/addressing/teams_editor.png)

## Adressage relatif

L'adresse `"buddy#controller"` fonctionne pour les objets de jeu des deux collections, car il s'agit d'une adresse *relative*. Chacune des collections `team_1` et `team_2` crée un nouveau contexte de nommage, ou espace de noms (*namespace*). Defold évite les collisions de noms en prenant en compte le contexte de nommage créé par une collection lors de l'adressage :

![Identifiants relatifs](images/addressing/relative_same.png)

- Dans le contexte de nommage `team_1`, les objets de jeu `bean` et `buddy` sont identifiés de manière unique.
- De même, dans `team_2`, `bean` et `buddy` sont également identifiés de manière unique.

L'adressage relatif fonctionne en ajoutant automatiquement le contexte de nommage actuel lors de la résolution d'une adresse cible. Ce mécanisme est très utile, car vous pouvez créer des groupes d'objets de jeu avec du code et les réutiliser efficacement tout au long du jeu.

### Raccourcis

Defold fournit deux raccourcis pratiques qui permettent d'envoyer un message sans spécifier l'URL complète :

:[Raccourcis](../shared/url-shorthands.md)

## Chemins des objets de jeu

Pour comprendre correctement le mécanisme de dénomination, regardons ce qui se passe lorsque vous créez et exécutez le projet :

1. L'éditeur lit la collection bootstrap (`main.collection`) et tout son contenu (objets de jeu et autres collections).
2. Pour chaque objet de jeu statique, le compilateur crée un identifiant. Celui-ci prend la forme d'un chemin (*path*) partant de la racine et descendant dans la hiérarchie de la collection jusqu'à l'objet. Un caractère `/` est ajouté à chaque niveau.

Dans l'exemple ci-dessus, le jeu s'exécute avec les quatre objets de jeu suivants :

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Les identifiants sont stockés sous forme de valeurs hachées. Le moteur conserve également l'état de hachage de chaque identifiant de collection, utilisé pour poursuivre le hachage d'une chaîne relative et produire un identifiant absolu.
:::

Au moment de l'exécution, le regroupement de collections n'existe pas. Il n'existe aucun moyen de savoir à quelle collection appartenait un objet de jeu spécifique avant la compilation. Il n'est pas non plus possible de manipuler tous les objets d'une collection à la fois. Pour effectuer de telles opérations, vous pouvez facilement assurer vous-même ce suivi dans le code. L'identifiant de chaque objet reste fixe pendant toute la durée de vie de celui-ci. Vous pouvez donc le stocker en toute sécurité et l'utiliser ultérieurement.

## L'adressage absolu

Il est possible d'utiliser les identifiants complets décrits ci-dessus pour l'adressage. En général, l'adressage relatif est conseillé, car il permet de réutiliser du contenu, mais il existe des cas où un adressage absolu devient nécessaire.

Par exemple, supposons que vous souhaitiez un gestionnaire d'IA qui suit l'état de chaque objet de jeu `bean`. Les haricots doivent rendre compte de leur état au gestionnaire, qui prend des décisions tactiques et leur donne des ordres en conséquence. Dans ce cas, il est logique de créer un seul objet de jeu gestionnaire nommé `manager`, doté d'un composant script, et de le placer avec les collections d'équipe dans la collection bootstrap.

![Objet de jeu manager](images/addressing/manager_editor.png)

Chaque `bean` doit envoyer des messages d'état au gestionnaire : `contact` s'il repère un ennemi ou `ouch!` s'il est touché et subit des dégâts. Pour que cela fonctionne, le script `controller` de `bean` utilise l'adressage absolu pour envoyer des messages au composant `controller` de `manager`.

Toute adresse commençant par `/` est résolue depuis la racine du monde de jeu. Celle-ci correspond à la racine de la *collection bootstrap* chargée au démarrage du jeu.

L'adresse absolue du script du gestionnaire est `"/manager#controller"`. Elle est résolue vers le bon composant, quel que soit l'endroit où elle est utilisée.

![Équipes et gestionnaire](images/addressing/teams_manager.png)

![Adressage absolu](images/addressing/absolute.png)

## Identifiants hachés

Le moteur stocke tous les identifiants sous forme de valeurs hachées. Toutes les fonctions qui prennent en argument un composant ou un objet de jeu acceptent une chaîne de caractères (*string*), un hachage ou un objet URL. Nous avons vu ci-dessus comment utiliser les chaînes pour l'adressage.

Lorsque vous obtenez l'identifiant d'un objet de jeu, le moteur renvoie toujours un identifiant de chemin absolu haché :

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Vous pouvez utiliser un tel identifiant à la place d'un identifiant sous forme de chaîne, ou en construire un vous-même. Notez cependant qu'un identifiant haché correspond au chemin d'accès de l'objet de jeu, c'est-à-dire à une adresse absolue :

::: sidenote
Les adresses relatives doivent être données sous forme de chaînes, car le moteur calcule un nouvel identifiant haché à partir de l'état de hachage du contexte de nommage actuel (la collection), auquel il ajoute la chaîne fournie.
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

## Les URL

Avant de terminer, examinons le format complet des adresses Defold : l'URL.

Une URL est un objet, généralement écrit sous la forme d'une chaîne spécialement formatée. Une URL générique se compose de trois parties :

`[socket:][path][#fragment]`

`socket`
: Identifie le monde de jeu (*game world*) de la cible. Cela est important lorsque vous travaillez avec des [proxys de collection](/manuals/collection-proxy) et sert alors à identifier la _collection chargée dynamiquement_.

`path`
: Cette partie de l'URL contient l'identifiant complet de l'objet de jeu cible.

`fragment`
: Identifie le composant cible dans l'objet de jeu spécifié.

Comme nous l'avons vu ci-dessus, vous pouvez omettre une partie, voire la plupart de ces informations dans la majorité des cas. Vous n'aurez presque jamais besoin de spécifier le `socket`, mais vous devrez souvent (quoique pas toujours) spécifier le chemin. Pour adresser des éléments dans un autre monde de jeu, vous devez spécifier la partie `socket` de l'URL. Par exemple, la chaîne URL complète du script `controller` dans l'objet de jeu `manager` ci-dessus est :

`"main:/manager#controller"`

et celle du composant `controller` de `buddy` dans `team_2` est :

`"main:/team_2/buddy#controller"`

Nous pouvons leur envoyer des messages :

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Construction d'objets URL

Les objets URL peuvent également être construits en code Lua :

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
