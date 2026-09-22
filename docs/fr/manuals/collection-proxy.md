---
title: Manuel des proxys de collection
brief: Ce manuel explique comment créer dynamiquement de nouveaux mondes de jeu et passer de l'un à l'autre.
---

# Proxy de collection {#collection-proxy}

Le composant (component) proxy de collection (collection proxy) permet de charger et de décharger dynamiquement de nouveaux « mondes de jeu » (game world) à partir du contenu d'un fichier de collection. Les proxys de collection peuvent servir à passer d'un niveau de jeu ou d'un écran d'interface graphique à un autre, à charger et décharger des « scènes » narratives au fil d'un niveau, à charger et décharger des mini-jeux, et bien plus encore.

Defold organise tous les objets de jeu (game object) en collections. Une collection peut contenir des objets de jeu et d'autres collections (c'est-à-dire des sous-collections). Les proxys de collection vous permettent de répartir votre contenu dans des collections distinctes, puis de gérer dynamiquement leur chargement et leur déchargement à l'aide de scripts.

Les proxys de collection diffèrent des [composants collection factory](/manuals/collection-factory/). Une collection factory instancie le contenu d'une collection dans le monde de jeu actuel. Les proxys de collection créent un nouveau monde de jeu à l'exécution et répondent donc à d'autres besoins.

## Création d'un composant proxy de collection {#creating-a-collection-proxy-component}

1. Ajoutez un composant proxy de collection à un objet de jeu en effectuant un <kbd>clic droit</kbd> sur cet objet et en sélectionnant <kbd>Add Component ▸ Collection Proxy</kbd> dans le menu contextuel.

2. Définissez la propriété *Collection* pour référencer une collection que vous souhaitez charger dynamiquement dans l'environnement d'exécution ultérieurement. Il s'agit d'une dépendance statique au moment du build : la collection référencée et ses dépendances sont compilées. Elles sont incluses dans le bundle principal, sauf si la case *Exclude* est cochée. Lorsque *Exclude* est cochée, les ressources référencées uniquement par des proxys exclus peuvent être omises du bundle principal pour Live Update, et le proxy déchargé peut être redirigé vers une autre collection compilée à l'exécution, comme décrit ci-dessous.

![Ajout d'un composant proxy](images/collection-proxy/create_proxy.png)

(Vous pouvez exclure le contenu du build et le télécharger à l'aide de code en cochant la case *Exclude* et en utilisant la [fonctionnalité Live Update](/manuals/live-update/).)

## Démarrage {#bootstrap}

Au démarrage, le moteur Defold charge et instancie tous les objets de jeu d'une *collection bootstrap* dans l'environnement d'exécution. Il initialise et active ensuite les objets de jeu et leurs composants. La collection bootstrap que le moteur doit utiliser est définie dans les [paramètres du projet](/manuals/project-settings/#main-collection). Par convention, ce fichier de collection est généralement nommé `main.collection`.

![Démarrage](images/collection-proxy/bootstrap.png)

Pour accueillir les objets de jeu et leurs composants, le moteur alloue la mémoire nécessaire à l'ensemble du « monde de jeu » dans lequel le contenu de la collection bootstrap est instancié. Un monde physique distinct est également créé pour les objets de collision et la simulation physique.

Comme les composants script doivent pouvoir adresser tous les objets du jeu, même depuis l'extérieur du monde bootstrap, ce dernier reçoit un nom unique : la propriété *Name* que vous définissez dans le fichier de collection :

![Démarrage](images/collection-proxy/collection_id.png)

Si la collection chargée contient des composants proxy de collection, les collections qu'ils référencent ne sont *pas* chargées automatiquement. Vous devez contrôler le chargement de ces ressources à l'aide de scripts.

## Chargement d'une collection {#loading-a-collection}

Le chargement dynamique d'une collection par l'intermédiaire d'un proxy s'effectue en envoyant un message appelé `"load"` au composant proxy depuis un script :

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![Chargement](images/collection-proxy/proxy_load.png)

Le composant proxy demande au moteur d'allouer de l'espace pour un nouveau monde. Un monde physique distinct est également créé à l'exécution, et tous les objets de jeu de la collection « `mylevel.collection` » sont instanciés.

Le nouveau monde reçoit son nom de la propriété *Name* du fichier de collection, définie ici sur « `mylevel` ». Ce nom doit être unique. Si le nom défini dans la propriété *Name* du fichier de collection est déjà utilisé pour un monde chargé, le moteur signale une erreur de collision de noms :

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Lorsque le moteur a terminé de charger la collection, le composant proxy de collection renvoie un message nommé `"proxy_loaded"` au script qui a envoyé le message `"load"`. Le script peut alors initialiser et activer la collection en réponse à ce message :

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Ce message demande au composant proxy de collection de commencer à charger sa collection dans un nouveau monde. Le proxy renvoie un message appelé `"proxy_loaded"` lorsque le chargement est terminé.

`"async_load"`
: Ce message demande au composant proxy de collection de commencer à charger sa collection en arrière-plan dans un nouveau monde. Le proxy renvoie un message appelé `"proxy_loaded"` lorsque le chargement est terminé.

`"init"`
: Ce message indique au composant proxy de collection que tous les objets de jeu et composants instanciés doivent être initialisés. Toutes les fonctions `init()` des scripts sont appelées à cette étape.

`"enable"`
: Ce message indique au composant proxy de collection que tous les objets de jeu et composants doivent être activés. Par exemple, tous les composants sprite commencent à être dessinés lorsqu'ils sont activés.

## Modification de la collection d'un proxy exclu {#changing-an-excluded-proxys-collection}

[`collectionproxy.set_collection()`](/ref/collectionproxy/#collectionproxy.set_collection) permet de rediriger un proxy exclu et déchargé vers une collection compilée, ce qui est utile après le montage d'un paquet Live Update. La case *Exclude* du proxy doit être cochée et celui-ci ne doit être ni chargé ni en cours de chargement. Le chemin doit se terminer par `.collectionc`. La collection et toutes ses dépendances doivent être disponibles dans le système de ressources au moment du chargement du proxy.

Vérifiez la valeur de retour avant de charger le proxy. Initialisez et activez le nouveau monde uniquement après avoir reçu `proxy_loaded` :

```lua
local function load_mounted_level()
    local ok, result = collectionproxy.set_collection(
        "#level_proxy",
        "/level_pack/level_3.collectionc"
    )

    if ok then
        msg.post("#level_proxy", "load")
    else
        print("Unable to change proxy collection", result)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        msg.post(sender, "init")
        msg.post(sender, "enable")
    end
end
```

Appelez `collectionproxy.set_collection("#level_proxy", nil)` lorsque le proxy n'est ni chargé ni en cours de chargement pour rétablir la collection attribuée dans l'éditeur. Consultez le [manuel des scripts Live Update](/manuals/live-update-scripting/) pour le téléchargement et le montage de contenu, ainsi que la référence de l'API pour les codes d'échec `collectionproxy.RESULT_*`.

## Adressage dans le nouveau monde {#addressing-into-the-new-world}

La propriété *Name* définie dans le fichier de collection sert à adresser les objets de jeu et les composants du monde chargé. Par exemple, si vous créez un objet de chargement dans la collection bootstrap, vous pouvez avoir besoin de communiquer avec lui depuis n'importe quelle collection chargée :

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![Chargement](images/collection-proxy/message_passing.png)

Si vous devez communiquer avec un objet de jeu de la collection chargée depuis l'objet de chargement, vous pouvez envoyer un message en utilisant l'[URL complète de l'objet](/manuals/addressing/#urls) :

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
Il n'est pas possible d'accéder directement aux objets de jeu d'une collection chargée depuis l'extérieur de cette collection :

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Déchargement d'un monde {#unloading-a-world}

Pour décharger une collection chargée, envoyez les messages correspondant aux étapes inverses de son chargement :

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Ce message demande au composant proxy de collection de désactiver tous les objets de jeu et composants du monde. Les sprites cessent d'être affichés à cette étape.

`"final"`
: Ce message demande au composant proxy de collection de finaliser tous les objets de jeu et composants du monde. Toutes les fonctions `final()` des scripts sont appelées à cette étape.

`"unload"`
: Ce message demande au proxy de collection de supprimer complètement le monde de la mémoire.

Si vous n'avez pas besoin d'un contrôle aussi fin, vous pouvez envoyer directement le message `"unload"` sans d'abord désactiver et finaliser la collection. Le proxy désactive et finalise alors automatiquement la collection avant de la décharger.

Lorsque le proxy de collection a terminé de décharger la collection, il renvoie un message `"proxy_unloaded"` au script qui a envoyé le message `"unload"` :

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## Pas de temps {#time-step}

Vous pouvez appliquer un facteur d'échelle aux mises à jour d'un proxy de collection en modifiant le _pas de temps_. Ainsi, même si le jeu fonctionne à une cadence constante de 60 FPS, un proxy peut se mettre à jour à un rythme plus rapide ou plus lent, ce qui affecte notamment :

* La vitesse de simulation physique
* Le `dt` transmis à `update()`
* Les [animations de propriétés des objets de jeu et de l'interface graphique](https://defold.com/manuals/animation/#property-animation-1)
* Les [animations image par image](https://defold.com/manuals/animation/#flip-book-animation)
* Les [simulations d'effets de particules](https://defold.com/manuals/particlefx/)
* La vitesse des temporisateurs

Vous pouvez également définir le mode de mise à jour, qui vous permet de choisir si la mise à l'échelle doit s'effectuer de manière discrète (ce qui n'a de sens qu'avec un facteur d'échelle inférieur à 1.0) ou continue.

Vous contrôlez le facteur d'échelle et le mode de mise à l'échelle en envoyant au proxy un message `set_time_step` :

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Pour observer ce qui se passe lorsque nous modifions le pas de temps, nous pouvons créer un objet avec le code suivant dans un composant script, puis le placer dans la collection dont nous modifions le pas de temps :

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Avec un pas de temps de 0.2, nous obtenons le résultat suivant dans la console :

```txt
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` est toujours appelée 60 fois par seconde, mais la valeur de `dt` change. Nous voyons que seulement 1/5 (0.2) des appels à `update()` ont un `dt` de 1/60 (ce qui correspond à 60 FPS) ; pour les autres, il vaut zéro. Toutes les simulations physiques sont également mises à jour selon ce `dt` et n'avancent que sur une image sur cinq.

::: sidenote
Vous pouvez utiliser le pas de temps des collections pour mettre votre jeu en pause, par exemple pendant l'affichage d'une fenêtre contextuelle ou lorsque la fenêtre a perdu le focus. Utilisez `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` pour mettre le jeu en pause et `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` pour le reprendre.
:::

Consultez [`set_time_step`](/ref/collectionproxy#set_time_step) pour plus de détails.

## Précautions et problèmes courants {#caveats-and-common-issues}

Physique
: Les proxys de collection permettent de charger plusieurs collections de premier niveau, ou *mondes de jeu*, dans le moteur. Dans ce cas, il est important de savoir que chaque collection de premier niveau constitue un monde physique distinct. Les interactions physiques (collisions, déclencheurs, lancers de rayons) ne se produisent qu'entre les objets appartenant au même monde. Ainsi, même si les objets de collision de deux mondes se superposent visuellement, aucune interaction physique ne peut se produire entre eux.

Mémoire
: Chaque collection chargée crée un nouveau monde de jeu dont l'empreinte mémoire est relativement importante. Si vous chargez des dizaines de collections simultanément par l'intermédiaire de proxys, vous pourriez envisager de revoir votre conception. Pour créer de nombreuses instances de hiérarchies d'objets de jeu, les [composants collection factory](/manuals/collection-factory) conviennent mieux.

Entrée
: Si certains objets de votre collection chargée ont besoin d'actions d'entrée, vous devez vous assurer que l'objet de jeu contenant le proxy de collection acquiert les entrées. Lorsque l'objet de jeu reçoit des messages d'entrée, ceux-ci sont transmis à ses composants, c'est-à-dire aux proxys de collection. Les actions d'entrée sont envoyées à la collection chargée par l'intermédiaire du proxy.
