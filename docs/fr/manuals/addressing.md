---
Titre: L'adressage dans Defold
En résumé: Ce guide explique comment Defold résoud le problème d'adressage.
---

# Adressage

Le code qui contrôle un jeu en cours d'exécution doit être capable d'atteindre chaque objet et composant afin de déplacer, mettre à l'échelle, animer, supprimer et manipuler ce que le joueur voit et entend. C'est possible grâce au mécanisme d'adressage de Defold.

## Identifiants

Defold utilise des adresses (ou des URL, mais mettons cela de côté pour le moment) pour faire référence aux GameObjects (objets de jeu) et composants. Ces adresses sont constituées d'identifiants (id). Voici des exemples sur la façon dont Defold utilise les adresses. À travers ce guide, nous allons examiner leur fonctionnement plus en détail:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Commençons par un exemple très simple. Vous avez un GameObject avec un seul sprite (un composant du nom de "body"). Vous disposez également d'un script (un autre composant dont le nom est "controller") pour contrôler le GameObject. La configuration dans l'éditeur ressemble à ceci:

![image](https://github.com/unlitcolor/doc/assets/9135915/287609c7-32e4-43cc-bc79-3ea9ca065805)

Pour désactiver le sprite au démarrage du jeu et le faire apparaître plus tard, cela se fait facilement en plaçant le code suivant dans "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Ne vous préoccupez pas du caractère «#», nous y reviendrons plus tard.

Tout fonctionne comme prévu. Lorsque le jeu démarre, le composant script *adresse* le composant sprite via son identifiant "body" et utilise cette adresse pour lui envoyer un *message* contenant "disable" (désactiver). L'effet de ce message spécial est que le sprite cache son graphisme. Schématiquement, cela ressemble à ça:

![image](https://github.com/unlitcolor/doc/assets/9135915/c9851e7b-8365-4854-a49c-a225bfcbfdb9)

Les identifiants dans la configuration sont arbitraires. Ici, nous avons choisi de donner au GameObject l'id «bean» (haricot), son sprite a été nommé «body», et le script qui contrôle le personnage s'appelle «contrôleur».

> NOTE:
>Si vous ne mettez pas un nom à l'id, l'éditeur le fera. Chaque fois que vous créez un nouveau GameObject ou composant, une propriété *Id* unique est automatiquement définie.
>
>- Les GameObjects reçoivent automatiquement un identifiant appelé "go" avec un énumérateur ("go2", "go3" etc).
>- Les composants reçoivent un identifiant correspondant à leur type ("sprite", "sprite2" etc).
>
>Vous pouvez vous en tenir à ces noms attribués de manière automatique si vous le souhaitez, mais nous vous encourageons à les remplacer par des noms plus appropriés et descriptifs.
:::

Ajoutons un nouveau sprite et donnons un bouclier au haricot (bean):

![image](https://github.com/unlitcolor/doc/assets/9135915/79f3e091-0414-46eb-80d9-485da7e64842)

Ce nouveau composant doit être identifié de manière unique dans le GameObject. Si vous lui donnez le nom «body» (corps), le script ne comprendra pas quel sprite devra recevoir le message «disable». C'est pourquoi nous choisissons un id unique (et descriptif) "shield" (bouclier). Nous pouvons désormais activer et désactiver les sprites «body» et «shield» à volonté.

![image](https://github.com/unlitcolor/doc/assets/9135915/6a0c44dd-6aa1-45b3-a30c-14ec9ea1efd5)

> NOTE:
>Si vous utilisez un même identifiant plus d'une fois, l'éditeur signalera une erreur, donc vous n'aurez jamais de problème:

![image](https://github.com/unlitcolor/doc/assets/9135915/8c8d0e3e-c6fd-4818-9f98-649ffc921432)

Voyons ce qu'il se passe lorsque vous ajoutez plus de GameObjects. Supposons que vous associez deux «beans» dans une petite équipe. Vous nommez l'un des GameObjects "Bean" et l'autre "Buddy". Lorsque «bean» est inactif, après un certain temps, il doit dire à «buddy» de commencer à danser. On va envoyer un message personnalisé contenant le mot "dance" à partir du script "controller" dans "bean" vers le script "controller" dans "buddy" :

![image](https://github.com/unlitcolor/doc/assets/9135915/403f5c0f-faf8-433b-8371-1b921c0e4c64)

>NOTE:
>Nous avons deux composants «controller» distincts, un dans chaque GameObject, rien d'anormal puisque chaque GameObject crée un nouveau contexte de dénomination.

Puisque le destinataire du message se trouve en dehors du GameObject «bean» (l'expéditeur), le code doit indiquer quel «controller» doit recevoir le message. Il doit spécifier à la fois l’id du GameObject cible ainsi que celui du composant. L'adresse complète du composant devient « buddy#controller » et cette adresse se compose de deux parties distinctes.

- Première partie: L'identité du GameObject cible («buddy»),
- Le caractère séparateur GameObject/Composant ("#"),
- Deuxième partie: L'identité du composant cible ("controller").

En revenant à l'exemple précédent contenant un seul GameObject, nous voyons qu'en laissant de côté l'identifiant du GameObject de l'adresse cible, le code peut adresser des composants dans *le GameObject actuel*.

Par exemple, `"#body"` désigne l'adresse du composant "body" dans le GameObject actuel. Ceci est très utile car ce code fonctionnera dans *n'importe quel* GameObject, tant qu'un composant "body" est présent.

## Collections

Les Collections permettent de créer des groupes ou des hiérarchies de GameObjects et de les réutiliser de manière contrôlée. Vous utilisez des fichiers de collection comme modèles ("prototypes" ou "prefabs") dans l'éditeur lorsque vous peuplez votre jeu avec du contenu.

Supposons que vous souhaitiez créer un grand nombre d’équipes bean/buddy. Un bon moyen de le faire est de créer un modèle dans un nouveau fichier de collection *collection file* (nommez-le «team.collection»). Créez les GameObjects d'équipe dans la collection et enregistrez. Ensuite, placez une instance de team.collection dans la collection principale et donnez à l'instance un identifiant (nommez-la "team_1") :

![image](https://github.com/unlitcolor/doc/assets/9135915/fcb05a56-6a92-4ed0-812a-47952fb507b0)

Avec cette structure, le GameObject "bean" peut toujours faire référence au composant "controller" dans "buddy" par l'adresse `"buddy#controller"`.

![image](https://github.com/unlitcolor/doc/assets/9135915/74b76f07-c828-4f42-8545-5e0206707598)

Ajoutez une deuxième instance de "team.collection" (nommez-la "team_2"), le code exécuté dans les composants du script "team_2" fonctionnera tout aussi bien. L'instance du GameObject "bean" de la collection "team_2" peut toujours adresser le composant "controller" dans "buddy" par l'adresse `"buddy#controller"`.

![image](https://github.com/unlitcolor/doc/assets/9135915/73a455d2-9379-492c-ae0d-54a80351c82b)

## Adressage relatif

L'adresse `"buddy#controller"` fonctionne pour les GameObjects dans les deux collections car il s'agit d'une adresse *relative*. Chacune des collections "team_1" et "team_2" crée un nouveau contexte de dénomination, ou "namespace" (espace de nom). Defold évite les collisions de noms en prenant en compte le contexte de dénomination créé par une collection pour l'adressage:

![image](https://github.com/unlitcolor/doc/assets/9135915/80f64a03-6d8d-47df-b336-2e8084f76139)

- Dans le contexte de dénomination "team_1", les GameObjects "bean" et "buddy" sont identifiés de manière unique.
- De même, dans "team_2", "bean" et "buddy" sont également identifiés de manière unique.

L'adressage relatif fonctionne en ajoutant automatiquement le contexte de dénomination actuel lors de la résolution d'une adresse cible. Ce qui est très utile et puissant car vous pouvez créer des groupes de GameObjects avec du code et les réutiliser efficacement tout au long du jeu.

### Raccourcis

Defold fournit deux raccourcis pratiques que vous pouvez utiliser pour envoyer un message sans spécifier l'URL complète:

:[Raccourcis](../shared/url-shorthands.md)

## Les chemins des GameObjects

Pour comprendre correctement le mécanisme de dénomination, regardons ce qui se passe lorsque vous créez et exécutez le projet :

1. L'éditeur lit la collection en partant de la racine ("main.collection") et tout son contenu (GameObjects et autres collections).
2. Pour chaque GameObject statique, le compilateur crée un identifiant. Ceux-ci sont construits sous forme de «paths» (chemins) commençant par la racine et descendant dans la hiérarchie de la collection jusqu'au GameObject. Un caractère '/' est ajouté à chaque niveau.

Dans l'exemple ci-dessus, le jeu se déroule avec les 4 GameObjects suivants :

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

>NOTE:
>Les ids sont stockées sous forme de "valeurs hachées". L'exécution conserve l'état de hachage pour chaque id de collection utilisé pour continuer le hachage d'une chaîne de caractères relative en un id absolu.

Au moment de l'exécution, le regroupement de collections n'existe pas. Il n'existe aucun moyen de savoir à quelle collection appartenait un GameObject spécifique avant la compilation. Il n’est pas non plus possible de manipuler tous les objets d’une collection à la fois. Pour effectuer de telles opérations, vous pouvez facilement effectuer le suivi vous-même, dans le code. Chaque id reste fixe pendant toute la durée de vie du GameObject auquel il est associé. Vous pouvez stocker en toute sécurité l'id d'un GameObject et l'utiliser plus tard.

## L'adressage absolu

Il est possible d'utiliser les ids complets décrits ci-dessus lors de l'adressage. En général, l'adressage relatif est conseillé car il permet de réutiliser du contenu, mais il existe des cas où un adressage absolu devient nécessaire.

Par exemple, vous voulez un gestionnaire d'IA qui suit l'état de chaque GameObject bean. Vous voulez que les beans rendent compte de leur statut actif au gestionnaire, que ce dernier prenne des décisions tactiques et donne des ordres aux beans en fonction de leur statut. Dans ce cas, il est logique de créer un GameObject manager (gestionnaire) unique avec un composant script et de le placer avec les collections d'équipe dans la collection racine.

![image](https://github.com/unlitcolor/doc/assets/9135915/27faa1fb-6035-41cc-a440-49be11f17603)

Chaque bean doit envoyer des messages de statut au manager: «contact» un ennemi est repéré ou «ouch!» s'il est touché et subit des dégâts. Pour que cela fonctionne, le script controller du bean utilise l'adressage absolu pour envoyer des messages au composant «controller» dans «manager».

Toute adresse commençant par un «/» sera résolue à partir de la racine dans le jeu. Cela correspond à la *collection racine* chargée au démarrage du jeu.

L'adresse absolue du script du manager est `"/manager#controller"` et cette adresse absolue sera résolue en composant approprié, quel que soit l'endroit où il est utilisé.

![image](https://github.com/unlitcolor/doc/assets/9135915/cd3cefa8-52ef-4eef-9cec-d02b1723a8eb)

![image](https://github.com/unlitcolor/doc/assets/9135915/7f352f0b-44cd-4e82-9e2b-7adce736a222)

## Identifiants hachés

Le moteur stocke tous les identifiants sous forme de valeurs hachées. Toutes les fonctions qui prennent en argument un composant ou un GameObject acceptent une chaîne de caractères (string en anglais), un hachage ou un objet URL. Nous avons vu ci-dessus comment utiliser les strings pour l'adressage.

Lorsque vous obtenez l'id d'un GameObject, le moteur renverra toujours un identifiant de chemin absolu qui est haché :

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Vous pouvez utiliser un identifiant de ce genre à la place d'un id string ou en construire un vous-même. Notez cependant qu'un id haché correspond au chemin d'accès au GameObject, c'est à dire une adresse absolue :

>NOTE:
La raison pour laquelle les adresses relatives doivent être données sous forme de strings est que le moteur calculera un nouvel id de hachage en fonction de l'état de hachage du contexte de dénomination actuel (collection) avec le string ajoutée au hachage.

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

## Les URL

Avant de terminer, regardons le format complet des adresses Defold: l'URL.

Une URL est un GameObject, généralement écrit sous forme de strings spécialement formatées. Une URL générique se compose de trois parties :

`[socket:][path][#fragment]`

Socket (prise)
: Identifie le "game world" (monde de jeu) de la cible (ex: les niveaux, les menus, écrans de chargement...). Ceci est important lorsque vous travaillez avec des [Proxies de collection](/manuals/collection-proxy) et est ensuite utilisé pour identifier la _collection chargée dynamiquement_.

path
: Cette partie de l'URL contient l'id complet du GameObject cible.

fragment
: L'identité du composant cible dans le GameObject spécifié.

Comme nous l'avons vu ci-dessus, vous pouvez omettre une partie, voire la plupart de ces informations dans la majorité des cas. Vous n'aurez presque jamais besoin de spécifier le socket, mais vous devez souvent (mais pas toujours) spécifier le chemin. Dans les cas où vous devez aborder des choses dans un autre game world, vous devez spécifier la partie socket de l'URL. Par exemple, le string URL complet du script «controller» dans le GameObject «manager» ci-dessus est:

`"main:/manager#controller"`

et le controller buddy dans team_2 est :

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
