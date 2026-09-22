---
title: Manuel du composant factory
brief: Ce manuel explique comment utiliser les composants factory pour créer dynamiquement des objets de jeu à l'exécution.
---

# Composants factory {#factory-components}

Les composants factory (factory component) servent à créer dynamiquement des objets de jeu (game object) à partir d'une réserve d'objets dans un jeu en cours d'exécution.

Lorsque vous ajoutez un composant factory à un objet de jeu, vous indiquez dans la propriété *Prototype* le fichier d'objet de jeu que la factory doit utiliser comme prototype (également appelé « prefabs » ou « blueprints » dans d'autres moteurs) pour tous les nouveaux objets de jeu qu'elle crée.

![Composant factory](images/factory/factory_collection.png)

![Composant factory](images/factory/factory_component.png)

Pour déclencher la création d'un objet de jeu, appelez `factory.create()` :

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
factory.create(component, p)
```

![Objet de jeu créé](images/factory/factory_spawned.png)

`factory.create()` prend cinq paramètres :

`url`
: L'identifiant du composant factory qui doit créer un nouvel objet de jeu.

`[position]`
: (facultatif) La position du nouvel objet de jeu dans le monde. Il doit s'agir d'un `vector3`. Si vous n'indiquez pas de position, l'objet de jeu est créé à la position de l'objet de jeu qui appelle `factory.create()`.

`[rotation]`
: (facultatif) La rotation du nouvel objet de jeu dans le monde. Il doit s'agir d'un `quat`.

`[properties]`
: (facultatif) Une table Lua contenant les valeurs des propriétés de script avec lesquelles initialiser l'objet de jeu. Consultez le [manuel des propriétés de script](/manuals/script-properties) pour en savoir plus sur ces propriétés.

`[scale]`
: (facultatif) L'échelle de l'objet de jeu créé. Elle peut être exprimée sous la forme d'un `number` (supérieur à 0) qui définit une mise à l'échelle uniforme sur tous les axes. Vous pouvez également fournir un `vector3` dont chaque composante définit la mise à l'échelle sur l'axe correspondant.

Par exemple :

```lua
-- factory.script
local p = go.get_position()
p.y = vmath.lerp(math.random(), min_y, max_y)
local component = "#star_factory"
-- Spawn with no rotation but double scale.
-- Set the score of the star to 10.
factory.create(component, p, nil, { score = 10 }, 2.0) -- <1>
```
1. Définit la propriété « score » de l'objet de jeu étoile.

```lua
-- star.script
go.property("score", 1) -- <1>

local speed = -240

function update(self, dt)
    local p = go.get_position()
    p.x = p.x + speed * dt
    if p.x < -32 then
        go.delete()
    end
    go.set_position(p)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("collision_response") then
        msg.post("main#gui", "add_score", {amount = self.score}) -- <2>
        go.delete()
    end
end
```
1. La propriété de script « score » est définie avec une valeur par défaut.
2. Accédez à la propriété de script « score » comme à une valeur stockée dans « self ».

![Objet de jeu créé avec une propriété et une mise à l'échelle](images/factory/factory_spawned2.png)

::: sidenote
Defold ne prend actuellement pas en charge la mise à l'échelle non uniforme des formes de collision. Si vous fournissez une valeur d'échelle non uniforme, par exemple `vmath.vector3(1.0, 2.0, 1.0)`, le sprite sera mis à l'échelle correctement, mais pas les formes de collision.
:::


## Adressage des objets créés par une factory {#addressing-of-factory-created-objects}

Le mécanisme d'adressage de Defold permet d'accéder à chaque objet et composant dans un jeu en cours d'exécution. Le [manuel sur l'adressage](/manuals/addressing/) explique en détail le fonctionnement de ce système. Vous pouvez utiliser le même mécanisme d'adressage pour les objets de jeu créés dynamiquement et leurs composants. Il suffit souvent d'utiliser l'identifiant de l'objet créé, par exemple pour envoyer un message :

```lua
local function create_hunter(target_id)
    local id = factory.create("#hunterfactory")
    msg.post(id, "hunt", { target = target_id })
    return id
end
```

::: sidenote
Envoyer un message à l'objet de jeu lui-même plutôt qu'à un composant particulier transmet en fait le message à tous les composants. Cela ne pose généralement pas de problème, mais gardez-le à l'esprit si l'objet possède de nombreux composants.
:::

Mais comment accéder à un composant particulier d'un objet de jeu créé dynamiquement, par exemple pour désactiver un objet de collision ou changer l'image d'un sprite ? La solution consiste à construire une URL à partir de l'identifiant de l'objet de jeu et de celui du composant.

```lua
local function create_guard(unarmed)
    local id = factory.create("#guardfactory")
    if unarmed then
        local weapon_sprite_url = msg.url(nil, id, "weapon")
        msg.post(weapon_sprite_url, "disable")

        local body_sprite_url = msg.url(nil, id, "body")
        sprite.play_flipbook(body_sprite_url, hash("red_guard"))
    end
end
```


## Suivi des objets créés et des objets parents {#tracking-spawned-and-parent-objects}

Lorsque vous appelez `factory.create()`, vous obtenez l'identifiant du nouvel objet de jeu, que vous pouvez conserver pour l'utiliser ultérieurement. Un usage courant consiste à créer des objets et à ajouter leurs identifiants à une table afin de pouvoir tous les supprimer plus tard, par exemple lors de la réinitialisation de l'agencement d'un niveau :

```lua
-- spawner.script
self.spawned_coins = {}

...

-- Spawn a coin and store it in the "coins" table.
local id = factory.create("#coinfactory", coin_position)
table.insert(self.spawned_coins, id)
```

Puis, plus tard :

```lua
-- spawner.script
-- Delete all spawned coins.
for _, coin_id in ipairs(self.spawned_coins) do
    go.delete(coin_id)
end

-- or alternatively
go.delete(self.spawned_coins)
```

Il est également courant de vouloir que l'objet créé connaisse l'objet de jeu qui l'a créé. C'est le cas, par exemple, d'un type d'objet autonome dont une seule instance peut être créée à la fois. L'objet créé doit alors informer son créateur lorsqu'il est supprimé ou désactivé, afin qu'un autre puisse être créé :

```lua
-- spawner.script
-- Spawn a drone and set its parent to the url of this script component
self.spawned_drone = factory.create("#dronefactory", drone_position, nil, { parent = msg.url() })

...

function on_message(self, message_id, message, sender)
    if message_id == hash("drone_dead") then
        self.spawned_drone = nil
    end
end
```

Et la logique de l'objet créé :

```lua
-- drone.script
go.property("parent", msg.url())

...

function final(self)
    -- I'm dead.
    msg.post(self.parent, "drone_dead")
end
```

## Chargement dynamique des ressources d'une factory {#dynamic-loading-of-factory-resources}

Si vous cochez la case *Load Dynamically* dans les propriétés de la factory, le moteur reporte le chargement des ressources qui lui sont associées.

![Chargement dynamique](images/factory/load_dynamically.png)

Lorsque la case est décochée, le moteur charge les ressources du prototype au moment du chargement du composant factory, afin qu'elles soient immédiatement prêtes pour la création d'objets.

Lorsque la case est cochée, vous avez deux possibilités :

Chargement synchrone
: Appelez [`factory.create()`](/ref/factory/#factory.create) lorsque vous souhaitez créer des objets. Les ressources seront chargées de manière synchrone, ce qui peut provoquer une brève interruption, puis de nouvelles instances seront créées.

  ```lua
  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling create without having called
      -- load will create the resources synchronously.
      self.go_id = factory.create("#factory")
  end

  function final(self)  
      -- Delete game objects. Will decref resources.
      -- In this case resources are deleted since the factory component
      -- holds no reference.
      go.delete(self.go_id)

      -- Calling unload will do nothing since factory holds no references
      factory.unload("#factory")
  end
  ```

Chargement asynchrone
: Appelez [`factory.load()`](/ref/factory/#factory.load) pour charger explicitement les ressources de manière asynchrone. Lorsqu'elles sont prêtes pour la création d'objets, une fonction de rappel (callback) est appelée.

  ```lua
  function load_complete(self, url, result)
      -- Loading is complete, resources are ready to spawn
      self.go_id = factory.create(url)
  end

  function init(self)
      -- No factory resources are loaded when the factory’s parent
      -- collection is loaded. Calling load will load the resources.
      factory.load("#factory", load_complete)
  end

  function final(self)
      -- Delete game object. Will decref resources.
      -- In this case resources aren’t deleted since the factory component
      -- still holds a reference.
      go.delete(self.go_id)

      -- Calling unload will decref resources held by the factory component,
      -- resulting in resources being destroyed.
      factory.unload("#factory")
  end
  ```

## Prototype dynamique {#dynamic-prototype}

Vous pouvez changer le *Prototype* qu'une factory peut créer en cochant la case *Dynamic Prototype* dans les propriétés de la factory.

![Prototype dynamique](images/factory/dynamic_prototype.png)

Lorsque l'option *Dynamic Prototype* est cochée, le composant factory peut changer de prototype à l'aide de la fonction `factory.set_prototype()`. Exemple :

```lua
factory.unload("#factory") -- unload the previous resources
factory.set_prototype("#factory", "/main/levels/enemyA.goc")
local enemy_id = factory.create("#factory")
```

::: important
Lorsque l'option *Dynamic Prototype* est activée, le nombre de composants de la collection ne peut pas être optimisé, et la collection qui contient la factory utilisera les nombres de composants par défaut du fichier *game.project*.
:::


## Limites d'instances {#instance-limits}

Le paramètre de projet *Max Instances*, dans la section *Collection*, définit la limite supérieure du nombre d'objets de jeu dans chaque collection (monde). Lors du build, Defold peut allouer une capacité plus faible s'il peut déterminer que cela ne présente aucun risque. Tous les objets de jeu présents simultanément dans un monde sont comptabilisés dans cette capacité, qu'ils aient été placés dans l'éditeur ou créés à l'exécution.

![Nombre maximal d'instances](images/factory/factory_max_instances.png)

L'allocation effective dépend de l'analyse effectuée lors du build :

* Lorsque le build peut déterminer un nombre fixe d'objets de jeu (généralement lorsque la collection ne contient ni factory ni factory de collection), la capacité correspond au nombre compilé, plafonné par *Max Instances*.
* Une collection contenant une factory ou une factory de collection utilise *Max Instances* comme capacité d'objets de jeu. Pour un prototype référencé statiquement, le build identifie les types de composants que la factory peut créer. Ces types utilisent leurs nombres maximaux respectifs définis dans le projet, tandis que les types de composants non concernés peuvent toujours utiliser des nombres exacts.
* Activer *Dynamic Prototype* désactive l'analyse du nombre de composants pour la collection qui contient la factory. Celle-ci utilise donc *Max Instances* et les nombres maximaux configurés pour chaque type de composant.

Définissez *Max Instances* en fonction du plus grand nombre d'objets de jeu susceptibles d'être présents simultanément dans un monde dynamique. Consultez la section [Optimisations des nombres maximaux de composants](/manuals/project-settings/#component-max-count-optimizations) pour savoir comment les autres limites de composants sont calculées.

## Mise en réserve des objets de jeu {#pooling-of-game-objects}

Il peut sembler judicieux de conserver les objets de jeu créés dans une réserve pour les réutiliser. Cependant, le moteur gère déjà une réserve d'objets en interne, et toute surcharge supplémentaire ne fera que ralentir les opérations. Il est à la fois plus rapide et plus propre de supprimer les objets de jeu et d'en créer de nouveaux.
