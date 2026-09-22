---
title: Manuel des factories de collection
brief: Ce manuel explique comment utiliser les composants factory de collection pour faire apparaître des hiérarchies d'objets de jeu.
---

# Factories de collection {#collection-factories}

Le composant (component) factory de collection sert à faire apparaître, dans un jeu en cours d'exécution, des groupes et des hiérarchies d'objets de jeu (game objects) enregistrés dans des fichiers de collection.

Les collections constituent un mécanisme puissant pour créer des modèles réutilisables, ou « prefabs », dans Defold. Pour une présentation des collections, consultez la [documentation sur les éléments constitutifs](/manuals/building-blocks#collections). Vous pouvez placer les collections dans l'éditeur ou les insérer dynamiquement dans votre jeu.

Avec un composant factory de collection, vous pouvez faire apparaître le contenu d'un fichier de collection dans un monde de jeu (game world). Cela revient à faire apparaître tous les objets de jeu de la collection à l'aide d'une factory, puis à construire la hiérarchie parent-enfant entre les objets. Un cas d'utilisation courant consiste à faire apparaître des ennemis composés de plusieurs objets de jeu (ennemi + arme, par exemple).

## Apparition d'une collection {#spawning-a-collection}

Supposons que nous voulions un objet de jeu représentant un personnage et un objet de jeu distinct représentant un bouclier, enfant du personnage. Nous construisons la hiérarchie des objets de jeu dans un fichier de collection et l'enregistrons sous le nom `bean.collection`.

::: sidenote
Le composant *proxy de collection* (collection proxy) sert à créer un nouveau monde de jeu, comprenant un monde physique distinct, à partir d'une collection. L'accès au nouveau monde se fait via un nouveau socket. Toutes les ressources contenues dans la collection sont chargées par le proxy lorsque vous lui envoyez un message pour démarrer le chargement. Les proxys sont donc très utiles, par exemple, pour changer de niveau dans un jeu. La création de nouveaux mondes de jeu entraîne toutefois un surcoût assez important : ne les utilisez donc pas pour charger dynamiquement de petits éléments. Pour en savoir plus, consultez la [documentation sur les proxys de collection](/manuals/collection-proxy).
:::

![Collection à faire apparaître](images/collection_factory/collection.png)

Nous ajoutons ensuite une *Collection factory* à un objet de jeu qui se chargera de l'apparition des objets, et définissons `bean.collection` comme *Prototype* du composant :

![Factory de collection](images/collection_factory/factory.png)

Pour faire apparaître un `bean` et son bouclier, il suffit maintenant d'appeler la fonction `collectionfactory.create()` :

```lua
local bean_ids = collectionfactory.create("#bean_factory")
```

La fonction accepte cinq paramètres :

`url`
: L'identifiant du composant factory de collection qui doit faire apparaître le nouvel ensemble d'objets de jeu.

`[position]`
: (facultatif) La position dans le monde des objets de jeu créés. Il doit s'agir d'un `vector3`. Si vous ne précisez pas de position, les objets apparaissent à la position du composant factory de collection.

`[rotation]`
: (facultatif) La rotation dans le monde des nouveaux objets de jeu. Il doit s'agir d'un `quat`.

`[properties]`
: (facultatif) Une table Lua contenant des paires `id`-`table` utilisées pour initialiser les objets de jeu créés. La construction de cette table est expliquée ci-dessous.

`[scale]`
: (facultatif) L'échelle des objets de jeu créés. Elle peut être exprimée par un `number` (supérieur à 0), qui définit une mise à l'échelle uniforme sur tous les axes. Vous pouvez également fournir un `vector3` dont chaque composante définit la mise à l'échelle sur l'axe correspondant.

`collectionfactory.create()` renvoie les identifiants des objets de jeu créés sous forme de table. Les clés de la table associent le hachage de l'identifiant local à la collection de chaque objet à son identifiant à l'exécution :

::: sidenote
La relation parent-enfant entre `bean` et `shield` n'apparaît *pas* dans la table renvoyée. Cette relation n'existe que dans le graphe de scène à l'exécution, c'est-à-dire dans la manière dont les objets sont transformés ensemble. Changer le parent d'un objet ne modifie jamais son identifiant.
:::

```lua
local bean_ids = collectionfactory.create("#bean_factory")
go.set_scale_xy(0.5, bean_ids[hash("/bean")])
pprint(bean_ids)
-- DEBUG:SCRIPT:
-- {
--   hash: [/shield] = hash: [/collection0/shield], -- <1>
--   hash: [/bean] = hash: [/collection0/bean],
-- }
```
1. Un préfixe `/collection[N]/`, où `[N]` est un compteur, est ajouté à l'identifiant pour identifier chaque instance de manière unique :

## Propriétés {#properties}

Lorsque vous faites apparaître une collection, vous pouvez transmettre des paramètres de propriété à chaque objet de jeu en construisant une table dont les clés sont les identifiants des objets et les valeurs sont des tables contenant les propriétés de script à définir.

```lua
local props = {}
props[hash("/bean")] = { shield = false }
local ids = collectionfactory.create("#bean_factory", nil, nil, props)
```

Supposons que l'objet de jeu `bean` de `bean.collection` définisse la propriété `shield`. Le [manuel des propriétés de script](/manuals/script-properties) contient des informations sur les propriétés de script.

```lua
-- bean/controller.script
go.property("shield", true)

function init(self)
    if not self.shield then
        go.delete("shield")
    end     
end
```

## Chargement dynamique des ressources de factory {#dynamic-loading-of-factory-resources}

Lorsque vous cochez la case *Load Dynamically* dans les propriétés de la factory de collection, le moteur reporte le chargement des ressources associées à la factory.

![Chargement dynamique](images/collection_factory/load_dynamically.png)

Lorsque la case est décochée, le moteur charge les ressources du prototype lors du chargement du composant factory de collection. Elles sont ainsi immédiatement prêtes à servir à la création d'objets.

Lorsque la case est cochée, vous disposez de deux modes d'utilisation :

Chargement synchrone
: Appelez [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create:url-[position]-[rotation]-[properties]-[scale]) lorsque vous voulez faire apparaître des objets. Cet appel charge les ressources de manière synchrone, ce qui peut provoquer une brève interruption, puis crée de nouvelles instances.

  ```lua
  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling create without
      -- having called load will create the resources synchronously.
      self.go_ids = collectionfactory.create("#collectionfactory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the collection
      -- factory component holds no reference.
      go.delete(self.go_ids)

      -- Calling unload will do nothing since factory holds
      -- no references
      collectionfactory.unload("#factory")
  end
  ```

Chargement asynchrone
: Appelez [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load:[url]-[complete_function]) pour charger explicitement les ressources de manière asynchrone. Lorsque les ressources sont prêtes à servir à la création d'objets, une fonction de rappel (callback) est appelée.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_ids = collectionfactory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the collection factory’s
      -- parent collection is loaded. Calling load will load the resources.
      collectionfactory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the collection factory
      -- component still holds a reference.
      go.delete(self.go_ids)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      collectionfactory.unload("#factory")
  end
  ```


## Prototype dynamique {#dynamic-prototype}

Il est possible de changer le *Prototype* qu'une factory de collection peut créer en cochant la case *Dynamic Prototype* dans les propriétés de la factory de collection.

![Prototype dynamique](images/collection_factory/dynamic_prototype.png)

Lorsque l'option *Dynamic Prototype* est cochée, le composant factory de collection peut changer de prototype à l'aide de la fonction `collectionfactory.set_prototype()`. Exemple :

```lua
collectionfactory.unload("#factory") -- unload the previous resources
collectionfactory.set_prototype("#factory", "/main/levels/level1.collectionc")
local ids = collectionfactory.create("#factory")
```

::: important
Lorsque l'option *Dynamic Prototype* est activée, le nombre de composants de la collection ne peut pas être optimisé et la collection qui contient la factory utilise les nombres de composants par défaut du fichier *game.project*.
:::
