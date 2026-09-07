---
title: Scripts de l'éditeur
brief: Ce manuel explique comment étendre l'éditeur à l'aide de Lua
---

# Scripts de l'éditeur {#editor-scripts}

Vous pouvez créer des éléments de menu personnalisés et des hooks de cycle de vie de l'éditeur à l'aide de fichiers Lua portant une extension spéciale : `.editor_script`. Ce système vous permet d'adapter l'éditeur pour améliorer votre flux de travail de développement.

## Environnement d'exécution des scripts de l'éditeur {#editor-script-runtime}

Les scripts de l'éditeur s'exécutent dans l'éditeur, au sein d'une machine virtuelle Lua émulée par une machine virtuelle Java. Tous les scripts partagent un seul et même environnement, ce qui leur permet d'interagir entre eux. Vous pouvez charger des modules Lua avec `require`, comme dans les fichiers `.script`, mais la version de Lua qui s'exécute dans l'éditeur est différente : assurez-vous donc que votre code partagé est compatible. L'éditeur utilise Lua version 5.2.x, plus précisément l'environnement d'exécution [luaj](https://github.com/luaj/luaj), qui est actuellement la seule solution viable pour exécuter Lua sur la JVM. Il existe également certaines restrictions :
- le paquet `debug` n'est pas disponible ;
- `os.execute` n'est pas disponible, mais nous proposons une fonction similaire, `editor.execute()` ;
- `os.tmpname` et `io.tmpfile` ne sont pas disponibles — les scripts de l'éditeur ne peuvent actuellement accéder qu'aux fichiers situés dans le répertoire du projet ;
- `os.rename` n'est pas disponible pour le moment, bien que nous souhaitions l'ajouter ;
- `os.exit` et `os.setlocale` ne sont pas disponibles.
- certaines fonctions à exécution longue ne sont pas autorisées dans les contextes où l'éditeur a besoin d'une réponse immédiate du script ; consultez les [modes d'exécution](#execution-modes) pour plus de détails.

Toutes les extensions de l'éditeur définies dans les scripts de l'éditeur sont chargées à l'ouverture d'un projet. Lorsque vous récupérez des bibliothèques, les extensions sont rechargées, car les bibliothèques dont vous dépendez peuvent contenir de nouveaux scripts de l'éditeur. Ce rechargement ne prend pas en compte les modifications de vos propres scripts de l'éditeur, car vous pourriez être en train de les modifier. Pour les recharger également, exécutez la commande **Project → Reload Editor Scripts**.

## Anatomie d'un fichier `.editor_script` {#anatomy-of-editor_script}

Chaque script de l'éditeur devrait renvoyer un module, comme ceci :
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

function M.get_prefs_schema()
  -- TODO - define preferences
end

return M
```
L'éditeur rassemble ensuite tous les scripts de l'éditeur définis dans le projet et les bibliothèques, les charge dans une seule machine virtuelle Lua et les appelle selon les besoins (voir les sections [commandes](#commands) et [hooks de cycle de vie](#lifecycle-hooks) pour plus de détails).

## API de l'éditeur {#editor-api}

Vous pouvez interagir avec l'éditeur à l'aide du paquet `editor`, qui définit l'API suivante :
- `editor.platform` — une chaîne de caractères, soit `"x86_64-win32"` pour Windows, `"x86_64-macos"` pour macOS ou `"x86_64-linux"` pour Linux.
- `editor.version` — une chaîne de caractères indiquant le nom de la version de Defold, par exemple `"1.4.8"`
- `editor.engine_sha1` — une chaîne de caractères contenant le SHA1 du moteur Defold
- `editor.editor_sha1` — une chaîne de caractères contenant le SHA1 de l'éditeur Defold
- `editor.get(node_id, property)` — récupère la valeur d'une propriété d'un nœud dans l'éditeur. Les nœuds de l'éditeur représentent diverses entités, comme des fichiers de script ou de collection, des objets de jeu (game objects) dans des collections, des fichiers JSON chargés comme ressources, etc. `node_id` est une valeur userdata transmise au script de l'éditeur par l'éditeur. Vous pouvez également transmettre un chemin de ressource à la place de l'identifiant du nœud, par exemple `"/main/game.script"`. `property` est une chaîne de caractères. Les propriétés suivantes sont actuellement prises en charge :
  - `"path"` — chemin du fichier à partir du dossier du projet pour les *ressources* — les entités qui existent sous forme de fichiers ou de répertoires. Exemple de valeur renvoyée : `"/main/game.script"`
  - `"children"` — liste des chemins des ressources enfants pour les ressources de type répertoire
  - `"parent"` — nœud parent dans l'éditeur pour un nœud de la vue Outline qui possède un parent
  - `"text"` — contenu textuel d'une ressource modifiable sous forme de texte (comme les fichiers de script ou JSON). Exemple de valeur renvoyée : `"function init(self)\nend"`. Notez que cela diffère de la lecture du fichier avec `io.open()`, car vous pouvez modifier un fichier sans l'enregistrer, et ces modifications ne sont accessibles que via la propriété `"text"`.
  - pour les atlas : `images` (liste des nœuds de l'éditeur correspondant aux images de l'atlas) et `animations` (liste des nœuds d'animation)
  - pour les animations d'atlas : `images` (comme `images` dans l'atlas)
  - pour les tilemaps : `layers` (liste des nœuds de l'éditeur correspondant aux couches de la tilemap)
  - pour les couches de tilemap : `tiles` (une grille de tuiles 2D sans limites), voir `tilemap.tiles.*` pour plus d'informations
  - pour les effets de particules : `emitters` (liste des nœuds d'émetteur de l'éditeur) et `modifiers` (liste des nœuds de modificateur de l'éditeur)
  - pour les émetteurs d'effets de particules : `modifiers` (liste des nœuds de modificateur de l'éditeur)
  - pour les objets de collision : `shapes` (liste des nœuds de forme de collision de l'éditeur)
  - pour les fichiers GUI : des listes de nœuds telles que `layers`, `fonts`, `materials`, `textures`, `particlefxs`, `nodes` et `layouts`
  - certaines propriétés affichées dans la vue Properties lorsque vous avez sélectionné un élément dans la vue Outline. Les types de propriétés de la vue Outline suivants sont pris en charge :
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    Notez que certaines de ces propriétés peuvent être en lecture seule et que d'autres peuvent être indisponibles selon le contexte ; utilisez donc `editor.can_get` avant de les lire et `editor.can_set` avant de demander à l'éditeur de les définir. Survolez le nom d'une propriété dans la vue Properties pour afficher une infobulle indiquant son nom dans les scripts de l'éditeur. Vous pouvez définir les propriétés de ressource sur `nil` en fournissant la valeur `""`.
- `editor.properties(node_id)` — renvoie une liste triée des noms de propriétés lisibles sur un nœud, adaptée au contexte, par exemple `pprint(editor.properties("/game.project"))`. Utilisez les fonctions `editor.can_*` pour vérifier si une propriété de la liste peut également être modifiée ou réinitialisée, si des éléments peuvent y être ajoutés ou si leur ordre peut être modifié.
- `editor.can_get(node_id, property)` — vérifie si vous pouvez lire cette propriété afin que `editor.get()` ne lève pas d'erreur.
- `editor.can_set(node_id, property)` — vérifie qu'une étape de transaction `editor.tx.set()` portant sur cette propriété ne lèvera pas d'erreur.
- `editor.create_directory(resource_path)` — crée un répertoire s'il n'existe pas, ainsi que tous les répertoires parents manquants.
- `editor.create_resources(resources)` — crée une ou plusieurs ressources, à partir de modèles ou avec un contenu personnalisé
- `editor.delete_directory(resource_path)` — supprime un répertoire s'il existe, ainsi que tous les répertoires et fichiers enfants existants.
- `editor.execute(cmd, [...args], [options])` — exécute une commande shell, en capturant éventuellement sa sortie.
- `editor.save()` — enregistre sur disque toutes les modifications non enregistrées.
- `editor.transact(txs)` — modifie l'état de l'éditeur en mémoire à l'aide d'une ou plusieurs étapes de transaction créées avec les fonctions `editor.tx.*`.
- `editor.ui.*` — diverses fonctions liées à l'interface utilisateur, voir le [manuel de l'interface utilisateur](/manuals/editor-scripts-ui).
- `editor.prefs.*` — fonctions permettant d'interagir avec les préférences de l'éditeur, voir les [préférences](#preferences).

Vous trouverez la référence complète de l'API de l'éditeur [ici](/ref/stable/editor/).

## Commandes {#commands}

Si un module de script de l'éditeur définit `get_commands()`, cette fonction est appelée lors du rechargement des extensions. Les commandes renvoyées peuvent apparaître dans les menus de la barre de menus et dans les menus contextuels Assets, Outline, Scene et Code, selon leurs `locations`. Exemple :

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
L'éditeur attend de `get_commands()` un tableau de tables, chacune décrivant une commande distincte. La description d'une commande comprend :

- `label` (obligatoire) — le texte de l'élément de menu affiché à l'utilisateur
- `locations` (obligatoire) — un tableau décrivant où cette commande doit être disponible. Les valeurs prises en charge sont `"Edit"`, `"View"`, `"Project"`, `"Debug"` et `"Help"` pour les menus correspondants de la barre de menus ; `"Bundle"` pour le sous-menu **Project → Bundle** ; et `"Assets"`, `"Outline"`, `"Scene"` et `"Code"` pour les menus contextuels correspondants.
- `query` — permet à la commande de demander à l'éditeur les informations pertinentes et de définir les données sur lesquelles elle agit. Chaque clé de la table `query` possède une clé correspondante dans la table `opts` que les callbacks `active` et `run` reçoivent en argument. Clés prises en charge :
  - `selection` indique que cette commande est valide lorsqu'un élément est sélectionné et qu'elle agit sur cette sélection.
    - `type` est le type des nœuds sélectionnés qui intéressent la commande ; les types suivants sont actuellement autorisés :
      - `"resource"` — dans Assets et Outline, la ressource est l'élément sélectionné qui possède un fichier correspondant. Dans la barre de menus (Edit ou View), la ressource est le fichier actuellement ouvert ;
      - `"outline"` — un élément qui peut être affiché dans la vue Outline. Dans Outline, il s'agit de l'élément sélectionné ; dans la barre de menus, du fichier actuellement ouvert ;
      - `"scene"` — un élément qui peut être rendu dans la vue Scene.
    - `cardinality` définit le nombre d'éléments qui doivent être sélectionnés. Avec `"one"`, la sélection transmise au callback de la commande est un identifiant de nœud unique. Avec `"many"`, la sélection transmise au callback de la commande est un tableau contenant un ou plusieurs identifiants de nœud.
  - `active_view` indique que cette commande est valide lorsque la vue active de l'éditeur correspond au type demandé. La vue active est transmise au callback de la commande sous la forme `opts.active_view`.
    - `type` est le type de vue active qui intéresse la commande, soit `"code"`, `"scene"`, `"html"` ou `"form"`.
    - La vue active prend en charge les propriétés `"type"`, `"resource"` et `"dirty"`. Utilisez `editor.get(view, "resource")` pour récupérer la ressource affichée dans la vue et `editor.get(view, "dirty")` pour vérifier si elle contient des modifications non enregistrées.
  - `argument` — argument de la commande. Actuellement, seules les commandes à l'emplacement `"Bundle"` reçoivent un argument, qui vaut `true` lorsque la commande de création de bundle est sélectionnée explicitement et `false` lors d'une nouvelle création du bundle.
- `id` - chaîne de caractères identifiant la commande, utilisée par exemple pour conserver dans `prefs` la dernière commande de création de bundle utilisée
- `active` - un callback exécuté pour vérifier que la commande est active et qui doit renvoyer un booléen. Si `locations` contient `"Assets"`, `"Scene"` ou `"Outline"`, `active` est appelé lors de l'affichage du menu contextuel. Si les emplacements incluent `"Edit"` ou `"View"`, active est appelé à chaque interaction de l'utilisateur, comme une saisie au clavier ou un clic de souris ; veillez donc à ce que `active` soit relativement rapide.
- `run` - un callback exécuté lorsque l'utilisateur sélectionne l'élément de menu.

### Utiliser les commandes pour modifier l'état de l'éditeur en mémoire {#use-commands-to-change-the-in-memory-editor-state}

Dans le gestionnaire `run`, vous pouvez interroger et modifier l'état de l'éditeur en mémoire. Pour l'interroger, utilisez la fonction `editor.get()`, qui vous permet de demander à l'éditeur l'état actuel des fichiers et de la sélection (si vous utilisez `query = {selection = ...}`). Vous pouvez récupérer la propriété `"text"` des ressources modifiables sous forme de texte, ainsi que certaines propriétés affichées dans la vue Properties — survolez le nom d'une propriété pour afficher une infobulle indiquant son nom dans les scripts de l'éditeur. Pour modifier l'état de l'éditeur, utilisez `editor.transact()`, qui regroupe une ou plusieurs modifications en une seule étape annulable. Par exemple, pour pouvoir réinitialiser la transformation d'un objet de jeu, vous pourriez écrire une commande comme celle-ci :
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### Utiliser les commandes avec la vue active de l'éditeur {#use-commands-with-the-active-editor-view}

Les commandes situées dans des menus tels que `"View"` peuvent interroger la vue actuellement active de l'éditeur. Cela est utile lorsqu'une commande doit agir sur le fichier ou la scène que l'utilisateur consulte actuellement :

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### Modifier les atlas {#editing-atlases}

Outre la lecture et l'écriture des propriétés d'un atlas, vous pouvez lire et modifier ses images et ses animations. Un atlas définit les propriétés de liste de nœuds `images` et `animations`, et les animations définissent la propriété de liste de nœuds `images` : vous pouvez utiliser les étapes de transaction `editor.tx.add`, `editor.tx.remove` et `editor.tx.clear` avec ces propriétés.

Par exemple, pour ajouter une image à un atlas, exécutez le code suivant dans le gestionnaire `run` de la commande :
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
Pour obtenir l'ensemble de toutes les images d'un atlas, exécutez le code suivant :
```lua
local all_images = {} ---@type table<string, true>
-- first, collect all "bare" images
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- second, collect all images used in animations
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
Pour remplacer toutes les animations d'un atlas :
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### Modifier les sources de tuiles {#editing-tilesources}

En plus des propriétés de la vue Outline, les sources de tuiles (tilesources) définissent les propriétés suivantes :
- `animations` - une liste des nœuds d'animation de la source de tuiles
- `collision_groups` - une liste des nœuds de groupe de collision de la source de tuiles
- `tile_collision_groups` - une table associant les tuiles de la source de tuiles à leurs groupes de collision

Par exemple, voici comment configurer une source de tuiles :
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### Modifier les tilemaps {#editing-tilemaps}

Les tilemaps définissent la propriété `layers`, une liste de nœuds correspondant aux couches de la tilemap. Chaque couche définit également une propriété `tiles` contenant une grille de tuiles 2D sans limites pour cette couche. Cela diffère du moteur : les tuiles n'ont pas de limites et peuvent être ajoutées n'importe où, y compris à des coordonnées négatives. Pour modifier les tuiles, l'API des scripts de l'éditeur définit un module `tilemap.tiles` avec les fonctions suivantes :
- `tilemap.tiles.new()` pour créer une nouvelle structure de données contenant une grille de tuiles 2D sans limites (dans l'éditeur, contrairement au moteur, la tilemap n'a pas de limites et les coordonnées peuvent être négatives)
- `tilemap.tiles.get_tile(tiles, x, y)` pour obtenir l'indice d'une tuile à des coordonnées précises
- `tilemap.tiles.get_info(tiles, x, y)` pour obtenir toutes les informations sur une tuile à des coordonnées précises (la structure des données est la même que dans la fonction `tilemap.get_tile_info` du moteur)
- `tilemap.tiles.iterator(tiles)` pour créer un itérateur sur toutes les tuiles de la tilemap
- `tilemap.tiles.clear(tiles)` pour supprimer toutes les tuiles de la tilemap
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` pour définir une tuile à des coordonnées précises
- `tilemap.tiles.remove(tiles, x, y)` pour supprimer une tuile à des coordonnées précises

Par exemple, voici comment afficher le contenu de la tilemap entière :
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

Voici un exemple montrant comment ajouter une couche contenant des tuiles à une tilemap :
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### Modifier les effets de particules {#editing-particlefx}

Vous pouvez modifier les effets de particules à l'aide des propriétés `modifiers` et `emitters`. Par exemple, voici comment ajouter un émetteur circulaire avec un modificateur d'accélération :
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
De nombreuses propriétés des effets de particules sont des courbes ou des courbes avec dispersion (c'est-à-dire une courbe + une valeur de variation aléatoire). Une courbe est représentée par une table contenant une liste non vide de `points`, où chaque point est une table possédant les propriétés suivantes :
- `x` - la coordonnée x du point, qui doit commencer à 0 et se terminer à 1
- `y` - la valeur du point
- `tx` (de 0 à 1) et `ty` (de -1 à 1) - les tangentes du point. Par exemple, pour un angle de 80 degrés, `tx` doit valoir `math.cos(math.rad(80))` et `ty` doit valoir `math.sin(math.rad(80))`.
Les courbes avec dispersion possèdent en plus une propriété numérique `spread`.

Par exemple, la définition d'une courbe d'alpha sur la durée de vie des particules pour un émetteur existant pourrait ressembler à ceci :
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- start at 0, go up quickly
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- reach 1 at 20% of a lifetime
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- slowly go down to 0
    }})
})
```
Bien entendu, il est également possible d'utiliser la clé `particle_key_alpha` dans une table lors de la création d'un émetteur. Vous pouvez aussi utiliser un nombre seul pour représenter une courbe « statique ».

#### Modifier les objets de collision {#editing-collision-objects}

En plus des propriétés par défaut de la vue Outline, les objets de collision définissent la propriété de liste de nœuds `shapes`. Voici comment ajouter de nouvelles formes de collision :
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
La propriété `type` d'une forme est obligatoire lors de sa création et ne peut plus être modifiée une fois la forme ajoutée. Il existe trois types de formes :
- `shape-type-box` - une forme de boîte possédant une propriété `dimensions`
- `shape-type-sphere` - une forme de sphère possédant une propriété `diameter`
- `shape-type-capsule` - une forme de capsule possédant les propriétés `diameter` et `height`

#### Modifier les fichiers GUI {#editing-gui-files}

En plus des propriétés de la vue Outline, les fichiers GUI définissent plusieurs propriétés de liste de nœuds :

- `layers` — liste des nœuds de couche de l'éditeur (réordonnable)
- `fonts` — liste des nœuds de police de l'éditeur
- `materials` — liste des nœuds de matériau de l'éditeur
- `textures` — liste des nœuds de texture de l'éditeur
- `particlefxs` — liste des nœuds Particle FX de l'éditeur
- `nodes` — liste des nœuds de l'éditeur correspondant aux nœuds d'interface graphique
- `layouts` — liste des nœuds de l'éditeur correspondant aux dispositions de l'interface graphique

Vous pouvez modifier les couches de l'interface graphique à l'aide de la propriété `layers` de l'éditeur, par exemple :
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
Vous pouvez également réordonner les couches :
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
De la même manière, les polices, matériaux, textures et effets de particules se modifient à l'aide des propriétés `fonts`, `materials`, `textures` et `particlefxs` :
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
Ces propriétés ne prennent pas en charge la réorganisation.

Enfin, vous pouvez modifier les nœuds de l'interface graphique à l'aide de la propriété de liste `nodes`, par exemple :
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
Les types de nœuds intégrés sont :
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Si vous utilisez l'extension spine, vous pouvez également utiliser le type de nœud `gui-node-type-spine`.

Si le fichier GUI définit des dispositions, vous pouvez lire et définir leurs valeurs à l'aide de la syntaxe `layout:property`, par exemple :
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

Les propriétés de disposition qui ont été définies peuvent être réinitialisées à leurs valeurs par défaut à l'aide de `editor.tx.reset` :
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
Les arborescences de nœuds de modèle peuvent être lues, mais pas modifiées — vous pouvez uniquement définir les propriétés des nœuds de l'arborescence du modèle :
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### Modifier les objets de jeu {#editing-game-objects}

Vous pouvez modifier les composants (components) d'un fichier d'objet de jeu à l'aide des scripts de l'éditeur. Il existe deux sortes de composants : référencés et intégrés. Les composants référencés utilisent le type `component-reference` et servent de références à d'autres ressources, en autorisant uniquement la surcharge des propriétés go définies dans les scripts. Les composants intégrés utilisent des types tels que `sprite`, `label`, etc., et permettent de modifier toutes les propriétés définies dans le type de composant, ainsi que d'ajouter des sous-composants comme les formes des objets de collision. Par exemple, vous pouvez utiliser le code suivant pour configurer un objet de jeu :
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- set a go property defined in the script
    })
})
```

#### Modifier les collections {#editing-collections}
Vous pouvez modifier les collections à l'aide des scripts de l'éditeur. Vous pouvez ajouter des objets de jeu (intégrés ou référencés) et des collections (référencées). Par exemple :
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embbedded game object
        type = "go",
        id = "root",
        children = {
            {
                -- referenced game object
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referenced collection
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- embedded gos can also have components
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- set a go property defined in the script
            }
        }
    })
})
```

Comme dans l'éditeur, les collections référencées ne peuvent être ajoutées qu'à la racine de la collection modifiée, et les objets de jeu ne peuvent être ajoutés qu'à des objets de jeu intégrés ou référencés, mais pas à des collections référencées ni à des objets de jeu appartenant à ces collections référencées.

### Utiliser les commandes shell {#use-shell-commands}

Dans le gestionnaire `run`, vous pouvez écrire dans des fichiers (à l'aide du module `io`) et exécuter des commandes shell (à l'aide de la commande `editor.execute()`). Lors de l'exécution d'une commande shell, vous pouvez capturer sa sortie sous forme de chaîne de caractères, puis l'utiliser dans le code. Par exemple, pour créer une commande de formatage JSON qui fait appel à [`jq`](https://jqlang.github.io/jq/) installé globalement, vous pouvez écrire la commande suivante :
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
Comme cette commande appelle le programme shell en lecture seule (et en informe l'éditeur à l'aide de `reload_resources = false`), vous bénéficiez de la possibilité d'annuler cette action.

::: sidenote
Si vous souhaitez distribuer votre script de l'éditeur sous forme de bibliothèque, vous pouvez inclure dans la dépendance le programme binaire pour les plateformes de l'éditeur. Consultez la section [Scripts de l'éditeur dans les bibliothèques](#editor-scripts-in-libraries) pour plus de détails sur la marche à suivre.
:::

## Hooks de cycle de vie {#lifecycle-hooks}

Un fichier de script de l'éditeur bénéficie d'un traitement particulier : `hooks.editor_script`, situé à la racine de votre projet, dans le même répertoire que *game.project*. Ce script de l'éditeur, et lui seul, reçoit les événements de cycle de vie de l'éditeur. Exemple d'un tel fichier :
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
Nous avons décidé de limiter les hooks de cycle de vie à un seul fichier de script de l'éditeur, car l'ordre d'exécution des hooks de build est plus important que la facilité d'ajout d'une nouvelle étape de build. Les commandes sont indépendantes les unes des autres ; leur ordre d'affichage dans le menu importe donc peu, puisque l'utilisateur exécute finalement la commande particulière qu'il a sélectionnée. S'il était possible de définir des hooks de build dans différents scripts de l'éditeur, cela poserait un problème : dans quel ordre les hooks s'exécuteraient-ils ? Vous souhaitez probablement créer les sommes de contrôle du contenu après sa compression... Un fichier unique qui établit l'ordre des étapes de build en appelant explicitement la fonction de chaque étape permet de résoudre ce problème.

Hooks de cycle de vie existants que `/hooks.editor_script` peut définir :
- `on_build_started(opts)` — exécuté lors de la création d'un build du jeu destiné à être exécuté localement ou sur une cible distante, à l'aide des options Project Build ou Debug Start. Vos modifications apparaîtront dans le jeu compilé. Lever une erreur depuis ce hook interrompt le build. `opts` est une table contenant les clés suivantes :
  - `platform` — une chaîne de caractères au format `%arch%-%os%` décrivant la plateforme pour laquelle le build est créé, actuellement toujours identique à la valeur de `editor.platform`.
- `on_build_finished(opts)` — exécuté lorsque le build est terminé, qu'il ait réussi ou échoué. `opts` est une table contenant les clés suivantes :
  - `platform` — identique à celle de `on_build_started`
  - `success` — indique si le build a réussi, soit `true` ou `false`
- `on_bundle_started(opts)` — exécuté lorsque vous créez un bundle ou générez une version HTML5 du jeu. Comme avec `on_build_started`, les modifications déclenchées par ce hook apparaîtront dans le bundle et les erreurs interrompront sa création. `opts` contient les clés suivantes :
  - `output_directory` — un chemin de fichier pointant vers le répertoire de sortie du bundle. **Project ▸ Build HTML5** utilise sa propre arborescence d'artefacts, par exemple `"/path/to/project/build/default_html5/__htmlLaunchDir"`, distincte de la sortie normale de Build sous `build/default`.
  - `platform` — la plateforme pour laquelle le bundle du jeu est créé. Consultez la liste des valeurs de plateforme possibles dans le [manuel de Bob](/manuals/bob).
  - `variant` — la variante du bundle, soit `"debug"`, `"release"` ou `"headless"`
- `on_bundle_finished(opts)` — exécuté lorsque la création du bundle est terminée, qu'elle ait réussi ou non. `opts` est une table contenant les mêmes données que `opts` dans `on_bundle_started`, plus une clé `success` indiquant si le build a réussi.
- `on_target_launched(opts)` — exécuté lorsque l'utilisateur a lancé un jeu et que celui-ci a démarré avec succès. `opts` contient une clé `url` pointant vers un service du moteur lancé, par exemple `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — exécuté lorsque le jeu lancé est fermé, avec les mêmes opts que `on_target_launched`

Notez que les hooks de cycle de vie sont actuellement une fonctionnalité propre à l'éditeur et qu'ils ne sont pas exécutés par Bob lors de la création de bundles en ligne de commande.

## Serveurs de langage {#language-servers}

L'éditeur prend en charge un sous-ensemble du [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) : diagnostics (analyse statique), complétion, informations au survol, symboles du document dans le volet Structure, accès à la définition, recherche de références et renommage de symboles. Survolez un symbole pour afficher les informations du serveur de langage. Lorsque le curseur se trouve sur un symbole, utilisez <kbd>F2</kbd> pour le renommer, <kbd>F12</kbd> pour accéder à sa définition ou <kbd>Shift+F12</kbd> pour rechercher ses références. Ces actions sont également accessibles depuis le menu <kbd>Edit</kbd>.

Pour définir le serveur de langage, vous devez modifier la fonction `get_language_servers` de votre script de l'éditeur comme ceci :

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
L'éditeur démarre le serveur de langage à l'aide de la commande spécifiée dans `command`, en utilisant l'entrée et la sortie standard du processus serveur pour communiquer.

La table de définition du serveur de langage peut préciser :
- `languages` (obligatoire) — une liste des langages qui intéressent le serveur, tels que définis [ici](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers) (les extensions de fichier fonctionnent également) ;
- `command` (obligatoire) - un tableau contenant la commande et ses arguments
- `watched_files` - un tableau de tables comportant des clés `pattern` (un motif glob), qui déclencheront la notification de [modification des fichiers surveillés](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) du serveur.

## Serveur HTTP {#http-server}

Chaque instance de l'éditeur en cours d'exécution possède un serveur HTTP actif. Ce serveur peut être étendu à l'aide des scripts de l'éditeur. Pour étendre le serveur HTTP de l'éditeur, vous devez ajouter la fonction de script de l'éditeur `get_http_server_routes` — elle doit renvoyer les routes supplémentaires :
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
Après le rechargement des scripts de l'éditeur, la sortie suivante apparaît dans la console : `My route: http://0.0.0.0:12345/my-extension`. Si vous ouvrez ce lien dans le navigateur, vous verrez votre message `"Hello world!"`.

L'argument d'entrée `request` est une simple table Lua contenant des informations sur la requête. Elle contient des clés telles que `path` (le segment de chemin de l'URL qui commence par `/`), `method` (la méthode de la requête, par exemple `"GET"`), `headers` (une table dont les noms d'en-tête sont en minuscules) et, éventuellement, `query` (la chaîne de requête) et `body` (si la route définit comment interpréter le corps). Par exemple, pour créer une route qui accepte un corps JSON, définissez-la avec un paramètre de conversion `"json"` :
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
Vous pouvez tester ce point de terminaison en ligne de commande à l'aide de `curl` et `jq` :
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
Le chemin de la route prend en charge des motifs qui peuvent être extraits du chemin de la requête et transmis à la fonction de traitement dans la requête, par exemple :
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
Désormais, si vous ouvrez par exemple `http://0.0.0.0:12345/my-extension/setting/project.title`, vous verrez le titre de votre jeu extrait du fichier `/game.project`.

En plus d'un motif de chemin à segment unique, vous pouvez également capturer le reste du chemin de l'URL à l'aide de la syntaxe `{*name}`. Par exemple, voici un point de terminaison simple de serveur de fichiers qui sert les fichiers depuis la racine du projet :
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
Désormais, ouvrir par exemple `http://0.0.0.0:12345/my-extension/files/main/main.collection` dans le navigateur affichera le contenu du fichier `main/main.collection`.

## Scripts de l'éditeur dans les bibliothèques {#editor-scripts-in-libraries}

Vous pouvez publier des bibliothèques contenant des commandes pour que d'autres personnes les utilisent ; l'éditeur les détectera automatiquement. En revanche, les hooks ne peuvent pas être détectés automatiquement, car ils doivent être définis dans un fichier situé dans le dossier racine d'un projet, alors que les bibliothèques n'exposent que des sous-dossiers. Cela vise à vous donner davantage de contrôle sur le processus de build : vous pouvez toujours créer des hooks de cycle de vie sous forme de simples fonctions dans des fichiers `.lua`, afin que les utilisateurs de votre bibliothèque puissent les charger et les utiliser dans leur `/hooks.editor_script`.

Notez également que, bien que les dépendances soient affichées dans la vue Assets, elles n'existent pas sous forme de fichiers (ce sont des entrées d'une archive zip). Vous pouvez demander à l'éditeur d'extraire certains fichiers des dépendances dans le dossier `build/plugins/`. Pour cela, créez un fichier `ext.manifest` dans le dossier de votre bibliothèque, puis un dossier `plugins/bin/${platform}` dans le dossier où se trouve le fichier `ext.manifest`. Les fichiers de ce dossier seront automatiquement extraits dans le dossier `/build/plugins/${extension-path}/plugins/bin/${platform}`, afin que vos scripts de l'éditeur puissent y faire référence.

## Préférences {#preferences}

Les scripts de l'éditeur peuvent définir et utiliser des préférences — des données persistantes, non enregistrées dans le système de gestion de versions, stockées sur l'ordinateur de l'utilisateur. Ces préférences possèdent trois caractéristiques principales :
- typées : chaque préférence possède une définition de schéma qui inclut le type de données et d'autres métadonnées, comme la valeur par défaut
- à portée définie : les préférences s'appliquent soit à un projet, soit à un utilisateur
- imbriquées : chaque clé de préférence est une chaîne de caractères dont les segments sont séparés par des points, où le premier segment de chemin identifie un script de l'éditeur, et le reste

Toutes les préférences doivent être enregistrées en définissant leur schéma :
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
Après le rechargement d'un tel script de l'éditeur, l'éditeur enregistre ce schéma. Le script de l'éditeur peut alors lire et définir les préférences, par exemple :
```lua
-- Get a specific preference
editor.prefs.get("my_json_formatter.indent.type")
-- Returns: "spaces"

-- Get an entire preference group
editor.prefs.get("my_json_formatter")
-- Returns:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Set multiple nested preferences at once
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## Modes d'exécution {#execution-modes}

L'environnement d'exécution des scripts de l'éditeur utilise deux modes d'exécution, généralement transparents pour les scripts de l'éditeur : **immédiat** et **à exécution longue**.

Le mode **immédiat** est utilisé lorsque l'éditeur doit recevoir une réponse du script aussi vite que possible. Par exemple, les callbacks `active` des commandes de menu sont exécutés en mode immédiat, car ces vérifications s'effectuent sur le thread de l'interface utilisateur de l'éditeur en réponse aux interactions de l'utilisateur et doivent mettre à jour l'interface pendant le même cycle d'affichage.

Le mode **à exécution longue** est utilisé lorsque l'éditeur n'a pas besoin d'une réponse instantanée du script. Par exemple, les callbacks `run` des commandes de menu sont exécutés dans un mode **à exécution longue**, ce qui permet au script de prendre plus de temps pour terminer son travail.

Certaines fonctions utilisables par les scripts de l'éditeur peuvent prendre beaucoup de temps à s'exécuter. Par exemple, `editor.execute("git", "status", {reload_resources=false, out="capture"})` peut prendre jusqu'à une seconde sur des projets suffisamment volumineux. Pour préserver la réactivité et les performances de l'éditeur, les fonctions susceptibles de prendre du temps ne sont pas autorisées dans les contextes où l'éditeur a besoin d'une réponse immédiate. Tenter d'utiliser une telle fonction dans un contexte immédiat entraîne l'erreur suivante : `Cannot use long-running editor function in immediate context`. Pour résoudre cette erreur, évitez d'utiliser ces fonctions dans les contextes immédiats.

Les fonctions suivantes sont considérées comme des fonctions à exécution longue et ne peuvent pas être utilisées en mode immédiat :
- `editor.create_directory()`, `editor.create_resources()`, `editor.delete_directory()`, `editor.save()`, `os.remove()` et `file:write()` : ces fonctions modifient les fichiers sur disque, ce qui amène l'éditeur à synchroniser son arborescence de ressources en mémoire avec l'état du disque, une opération qui peut prendre plusieurs secondes dans les projets volumineux.
- `editor.execute()` : l'exécution de commandes shell peut prendre une durée imprévisible.
- `editor.transact()` : les transactions volumineuses sur des nœuds largement référencés peuvent prendre des centaines de millisecondes, ce qui est trop lent pour préserver la réactivité de l'interface utilisateur.

Les contextes d'exécution de code suivants utilisent le mode immédiat :
- Les callbacks `active` des commandes de menu : l'éditeur a besoin d'une réponse du script pendant le même cycle d'affichage de l'interface utilisateur.
- Le niveau supérieur des scripts de l'éditeur : nous ne nous attendons pas à ce que le rechargement des scripts de l'éditeur produise des effets de bord.

## Actions {#actions}

::: sidenote
Auparavant, l'éditeur interagissait avec la machine virtuelle Lua de manière bloquante ; il était donc impératif que les scripts de l'éditeur ne bloquent pas, car certaines interactions doivent s'effectuer depuis le thread de l'interface utilisateur de l'éditeur. C'est pourquoi, par exemple, `editor.execute()` et `editor.transact()` n'existaient pas. L'exécution des scripts et la modification de l'état de l'éditeur étaient déclenchées par le renvoi d'un tableau d'« actions » depuis les hooks et les gestionnaires `run` des commandes.

L'éditeur interagit désormais avec la machine virtuelle Lua de manière non bloquante, et ces actions ne sont donc plus nécessaires : l'utilisation de fonctions comme `editor.execute()` est plus pratique, concise et puissante. Les actions sont désormais **DÉCONSEILLÉES**, mais nous ne prévoyons pas de les supprimer.
:::

Les scripts de l'éditeur peuvent renvoyer un tableau d'actions depuis la fonction `run` d'une commande ou depuis les fonctions de hook de `/hooks.editor_script`. Ces actions sont ensuite exécutées par l'éditeur.

Une action est une table décrivant ce que l'éditeur doit faire. Chaque action possède une clé `action`. Il existe deux sortes d'actions : annulables et non annulables.

### Actions annulables {#undoable-actions}

::: sidenote
Préférez utiliser `editor.transact()`.
:::

Une action annulable peut être annulée après son exécution. Si une commande renvoie plusieurs actions annulables, elles sont exécutées ensemble et annulées ensemble. Vous devriez utiliser des actions annulables lorsque c'est possible. Leur inconvénient est qu'elles sont plus limitées.

Actions annulables existantes :
- `"set"` — définit une propriété d'un nœud de l'éditeur à une valeur donnée. Exemple :
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  L'action `"set"` nécessite les clés suivantes :
  - `node_id` — une valeur userdata identifiant le nœud. Vous pouvez aussi utiliser ici un chemin de ressource à la place de l'identifiant de nœud reçu de l'éditeur, par exemple `"/main/game.script"` ;
  - `property` — une propriété du nœud à définir, par exemple `"text"` ;
  - `value` — la nouvelle valeur de la propriété. Pour la propriété `"text"`, il doit s'agir d'une chaîne de caractères.

### Actions non annulables {#non-undoable-actions}

::: sidenote
Préférez utiliser `editor.execute()`.
:::

Une action non annulable efface l'historique d'annulation. Pour annuler une telle action, vous devrez donc utiliser d'autres moyens, comme la gestion de versions.

Actions non annulables existantes :
- `"shell"` — exécute un script shell. Exemple :
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  L'action `"shell"` nécessite la clé `command`, qui est un tableau contenant la commande et ses arguments.

### Combiner actions et effets de bord {#mixing-actions-and-side-effects}

Vous pouvez combiner des actions annulables et non annulables. Les actions sont exécutées séquentiellement ; selon leur ordre, vous finirez donc par perdre la possibilité d'annuler certaines parties de la commande.

Au lieu de renvoyer des actions depuis les fonctions qui les attendent, vous pouvez simplement lire et écrire directement dans les fichiers à l'aide de `io.open()`. Cela déclenche un rechargement des ressources qui efface l'historique d'annulation.
