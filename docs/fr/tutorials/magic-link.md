---
title: Tutoriel Magic Link
brief: Dans ce tutoriel, vous allez créer un petit jeu de réflexion complet avec un écran de démarrage, les mécaniques du jeu et une progression simple des niveaux sous la forme d'une difficulté croissante.
---

# Tutoriel Magic Link {#magic-link-tutorial}

Ce jeu est une variante du jeu d'association classique dans la lignée de _Bejeweled_ et de _Candy Crush_. Le joueur relie par glissement des blocs de même couleur pour les supprimer, mais le but du jeu n'est pas de supprimer de longues séries de blocs de même couleur, de vider le plateau ou de récolter des points : il s'agit de réunir un ensemble de « blocs magiques » spéciaux dispersés sur le plateau pour qu'ils se connectent.

Ce tutoriel est un guide pas à pas dans lequel nous construisons le jeu à partir d'une conception complète. En réalité, trouver une conception qui fonctionne demande beaucoup de temps et d'efforts. Vous pouvez partir d'une idée centrale, puis chercher un moyen d'en faire un prototype pour mieux comprendre ce qu'elle peut apporter. Même un jeu simple comme « Magic Link » demande un travail de conception assez conséquent. Ce jeu a connu quelques itérations et expérimentations avant d'aboutir à sa forme et à ses règles définitives (encore loin d'être parfaites). Mais, pour ce tutoriel, nous allons passer cette étape et commencer à construire le jeu à partir de sa conception finale.

## Premiers pas {#getting-started}

Vous devez commencer par créer un nouveau projet et importer le paquet de ressources :

* Créez un [nouveau projet](/manuals/project-setup/#creating-a-new-project) à partir du modèle "Empty Project"
* Téléchargez le projet « Magic Link » complet [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) comme référence. Le projet complet contient toutes les ressources si vous souhaitez créer le projet à partir de zéro.

## Règles du jeu {#game-rules}

![Schéma des règles du jeu](images/magic-link/linker_rules.png)

À chaque manche, le plateau est rempli aléatoirement de blocs colorés et d'un ensemble de blocs magiques. Les blocs colorés suivent ces règles :

* Ils disparaissent si le joueur les relie par glissement à des blocs de même couleur.
* Lorsque des blocs disparaissent, ils laissent des trous en dessous. Les blocs colorés tombent simplement à la verticale dans les trous qui se sont ouverts sous eux.
* Le bas de l'écran empêche tous les blocs de tomber plus bas.

Les blocs magiques se comportent différemment, selon ces règles :

* Les blocs magiques se déplacent _latéralement_ si une ouverture apparaît d'un côté ou de l'autre.
* Si un trou apparaît en dessous, ils tombent à la place comme les blocs colorés ordinaires.

Le joueur interagit avec le jeu selon les règles suivantes :

* Le joueur peut relier par glissement les blocs colorés adjacents horizontalement, verticalement et en diagonale.
* Les blocs reliés disparaissent dès que le joueur relâche le contact tactile (lève le doigt).
* Les blocs magiques ne réagissent pas au glissement et ne peuvent pas être reliés manuellement.
* Les blocs magiques réagissent en revanche lorsqu'ils se touchent horizontalement ou verticalement. Autrement dit, ils se relient automatiquement dans ces circonstances.
* Le niveau est terminé si le joueur parvient à relier automatiquement tous les blocs magiques du plateau.

Le niveau de difficulté détermine le nombre de blocs magiques placés sur le plateau.

## Vue d'ensemble {#overview}

Comme pour tout projet, nous devons définir les grandes lignes de notre approche de l'implémentation. Il existe de nombreuses façons de structurer et de construire ce jeu. Techniquement, nous pourrions, si nous le souhaitions, implémenter l'ensemble du jeu dans le système d'interface graphique. Cependant, construire le jeu avec des objets de jeu (game object) et des sprites, et utiliser les API GUI pour les éléments d'interface graphique et d'affichage tête haute à l'écran, est le plus souvent la manière naturelle de créer un jeu ; c'est donc la voie que nous allons suivre.

Comme nous prévoyons un nombre de fichiers assez limité, nous allons conserver une structure de dossiers très simple pour le projet :

![Structure des dossiers](images/magic-link/linker_folders.png)

*main*
: Ce dossier contiendra toute la logique du jeu. Tous les scripts, fichiers d'objets de jeu, fichiers de collection, fichiers d'interface graphique, etc., seront placés dans ce dossier. Vous pouvez tout à fait le diviser en plusieurs dossiers ou y créer des sous-dossiers si vous le souhaitez.

*images*
: Toutes les ressources d'image seront placées dans ce dossier.

*fonts*
: Les polices utilisées pour le rendu du texte sont conservées ici.

*input*
: Les associations d'entrées sont conservées dans ce dossier.

## Configuration du projet {#setting-up-the-project}

Le fichier *game.project* conserve principalement les paramètres par défaut, mais certains choix restent à faire. Tout d'abord, nous devons choisir une résolution pour le jeu. Il est assez facile de changer la résolution par la suite et, pour un jeu finalisé, nous devrons faire en sorte qu'il ait un bel aspect, quelle que soit la résolution ou le rapport d'aspect de l'appareil cible.

Nous avons choisi une résolution de 640x960 pixels, qui est la résolution native de l'iPhone 4. C'est aussi une résolution qui tient sur de nombreux moniteurs, ce qui facilite les tests du jeu sur ordinateur. Si vous souhaitez travailler avec une autre résolution, vous n'aurez que quelques valeurs à ajuster différemment.

![Paramètres du projet](images/magic-link/linker_project_settings.png)

Nous allons aussi devoir augmenter le nombre maximal de sprites rendus. Si vous le souhaitez, vous pouvez passer à la section suivante et revenir ici lorsque la console vous indique que vous avez atteint la limite de sprites.

![Disposition du jeu à l'échelle](images/magic-link/linker_layout.png)

Nous pouvons calculer le nombre maximal de sprites nécessaires :

* Le plateau de jeu contiendra 7x9 blocs. Il faudra prévoir des marges sur les bords ainsi que de l'espace en haut pour certains éléments d'interface graphique. Les blocs mesureront donc environ 90x90 pixels. Plus petits, ils seraient trop minuscules pour permettre une interaction sur le petit écran d'un téléphone.
* Chaque bloc est un sprite. Nous allons utiliser des animations d'une seule image pour définir la couleur du bloc.
* Certains blocs seront magiques et nous utiliserons quatre sprites pour les effets spéciaux de chacun d'eux.
* Les éléments graphiques des liaisons nécessiteront un sprite par élément. Dans le pire des cas, cela représente 61 sprites supplémentaires, si le joueur parvient à relier l'ensemble du plateau (à l'exception de deux blocs magiques qui ne peuvent pas être reliés par glissement).

Supposons donc que nous ayons un maximum de 30 blocs magiques. Le plateau compte 63 blocs (sprites). Parmi eux, les 30 blocs magiques ajoutent chacun quatre sprites pour les effets spéciaux. Cela représente 120 sprites supplémentaires. Avec les éléments graphiques des liaisons (33 au maximum dans ce cas), nous devrons donc dessiner au moins 120 + 33 = 153 sprites à chaque image. La puissance de deux la plus proche est 256.

Cependant, fixer le maximum à 256 ne suffit pas. Chaque fois que nous vidons et réinitialisons le plateau, nous allons supprimer tous les objets de jeu actuels et en créer de nouveaux. Le nombre de sprites doit tenir compte de tous les objets qui existent au cours de l'image. Cela inclut les objets supprimés, car ils sont retirés à la fin de l'image. Fixer le nombre maximal de sprites à 512 suffira donc.

![Nombre maximal de sprites](images/magic-link/linker_sprite_max_count.png)

## Ajout des ressources graphiques {#adding-the-graphics-assets}

Toutes les ressources nécessaires au jeu ont été préparées à l'avance. Nous les ajoutons sous forme d'images de 512x512 pixels et laissons le moteur les réduire à la taille cible.

::: sidenote
L'activation de *hidpi* dans les paramètres du projet fait passer le tampon arrière en haute résolution. De grandes images affichées à une échelle réduite paraîtront très nettes sur les écrans Retina.
:::

![Ajout des images](images/magic-link/linker_add_images.png)

En plus des blocs, une image de « connecteur » et des sprites d'effets sont fournis. Nous avons également deux images d'arrière-plan : l'une servira de fond au plateau de jeu et l'autre au menu principal. Ajoutez toutes les images au dossier *images*, puis créez un fichier d'atlas *sprites.atlas*. Ouvrez le fichier d'atlas et ajoutez-y toutes les images.

![Ajout des images à l'atlas](images/magic-link/linker_add_to_atlas.png)

Un ensemble d'images d'interface graphique permet de créer des éléments tels que des boutons et des fenêtres contextuelles. Elles sont ajoutées à un atlas distinct nommé *gui.atlas*.

## Génération du plateau {#generating-the-board}

La première étape consiste à créer la logique du plateau. Le plateau disposera de sa propre collection, qui contiendra tout ce qui est affiché à l'écran pendant la partie. Pour le moment, seuls le composant (component) factory "blockfactory" et le script sont nécessaires. Plus tard, nous ajouterons une factory pour les liaisons, des composants d'interface graphique pour le menu principal et, enfin, des mécanismes de chargement pour démarrer une partie depuis le menu principal et un moyen de revenir au menu.

1. Créez *`board.collection`* dans le dossier *`main`*. Veillez à la nommer "board" pour que nous puissions l'adresser plus tard. Si vous ajoutez le composant sprite de l'arrière-plan, veillez à fixer sa position Z à -1, sinon il ne sera pas dessiné derrière tous les blocs que nous créerons plus tard.
2. Définissez temporairement *Main Collection* (sous *Bootstrap*) dans *game.project* sur `/main/board.collection` pour faciliter les tests.

![Collection du plateau](images/magic-link/linker_board_collection.png)

![Collection du plateau au démarrage](images/magic-link/linker_bootstrap_board.png)

Le fichier de script *board.script* contiendra toute la logique du plateau lui-même et des blocs qu'il contient. Commencez par créer la fonction de construction du plateau et appelez-la (temporairement) depuis `init()`. Nous ajoutons également deux fonctions que nous n'utiliserons pas tout de suite, mais qui nous seront utiles plus tard :

`filter()`
: Cette fonction nous permettra de filtrer des listes d'éléments (blocs).

`build_blocklist()`
: Crée une liste à plat de tous les blocs du plateau, ce qui nous permet de la filtrer.

Après la construction du plateau, nous utiliserons deux ensembles de données différents contenant tous les blocs, `self.blocks` et `self.board` :

```lua
-- board.script
go.property("timer", 0)     -- Use to time events
local blocksize = 80        -- Distance between block centers
local edge = 40             -- Left and right edge.
local bottom_edge = 50      -- Bottom edge.
local boardwidth = 7        -- Number of columns
local boardheight = 9       -- Number of rows
local centeroff = vmath.vector3(8, -8, 0) -- Center offset for connector gfx since there's shadow below in the block img
local dropamount = 3        -- The number of blocks dropped on a "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- e.g: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Build a list of blocks in 1 dimension for easy filtering
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.
    self.chain = {}             -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3          -- Number of magic blocks on the board
    self.drops = 1              -- Number of drops you have available
    self.magic_blocks = {}      -- Magic blocks that are lined up
    self.dragging = false       -- Drag touch input
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calc z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Pick a random color
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Notez que les images des blocs se chevauchent : nous devons donc les dessiner dans le bon ordre. Pour cela, nous définissons la coordonnée z de chaque bloc. La valeur restera bien au-dessus de -1, où se trouve le sprite d'arrière-plan.

La logique du plateau crée des objets de jeu "`block`" au moyen du composant factory "`blockfactory`". Pour que cela fonctionne, nous devons créer l'objet de jeu du bloc. Le bloc possède un script et un sprite. Nous définissons l'animation par défaut du sprite sur l'un des blocs colorés de *`sprites.atlas`*, puis ajoutons du code à *`block.script`* pour que le bloc prenne la bonne couleur à sa création :

![Objet de jeu du bloc](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale_xy(0.18)     -- render scaled down without changing Z

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Définissez la propriété *Prototype* du composant factory "blockfactory" sur le nouveau fichier d'objet de jeu *block.go*.

![Factory des blocs](images/magic-link/linker_blockfactory.png)

Vous devriez maintenant pouvoir lancer le jeu et voir le plateau rempli de blocs aux couleurs aléatoires :

![Première capture d'écran](images/magic-link/linker_first_screenshot.png)

## Interactions {#interactions}

Maintenant que nous avons un plateau, nous devons ajouter les interactions utilisateur. Définissons d'abord les associations d'entrées dans *game.input_binding*, dans le dossier *input*. Assurez-vous que les paramètres de *game.project* utilisent votre fichier d'associations d'entrées.

![Associations d'entrées](images/magic-link/linker_input_bindings.png)

Nous n'avons besoin que d'une association et nous affectons `MOUSE_BUTTON_LEFT` au nom d'action "touch". Ce jeu n'utilise pas le multitouch et, pour simplifier les choses, Defold convertit les entrées tactiles à un doigt en clics gauches de la souris.

Le traitement des entrées revient au plateau ; nous devons donc ajouter le code correspondant dans *board.script* :

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- What block was touched or dragged over?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- outside board.
            return
        end

        if action.pressed then
            -- Player started touch
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- then drag
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false
    end
end
```

Les messages `make_orange` et `make_green` sont seulement temporaires : ils fournissent un retour visuel qui confirme que le code fonctionne. Nous devons ajouter du code à *block.script* pour traiter ces messages :

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Les blocs recevront maintenant d'abord un message `make_orange`, puis des messages `make_green` tant que vous maintenez le contact tactile (ou le bouton de la souris enfoncé). Il est donc probable que les blocs ne fassent que clignoter en orange (voire pas du tout) avant de devenir verts. Mais nous savons bien quel bloc le joueur touche ! Si vous souhaitez suivre plus précisément le traitement des entrées, insérez des appels à `print()` ou à `pprint()` dans le code.

## Marquage des liaisons {#mark-links}

Nous avons maintenant besoin de ressources pour le marqueur qui indiquera que des blocs sont reliés par le joueur. L'idée consiste simplement à superposer un élément graphique à chaque bloc pour montrer qu'il est relié.

Nous devons créer un objet de jeu "connector" contenant l'image du sprite de connecteur, ainsi qu'un composant factory "connector factory" dans l'objet de jeu "board" :

![Objet de jeu du connecteur](images/magic-link/linker_connector.png)

![Factory des connecteurs](images/magic-link/linker_connector_factory.png)

Le script de cet objet de jeu est minimal : il doit seulement redimensionner l'image pour l'accorder au reste du jeu et définir correctement l'ordre Z.

```lua
-- connector.script
function init(self)
    go.set_scale_xy(0.18)           -- Scale in 2D without changing Z.
    go.set(".", "position.z", 1)    -- Put on top.
end
```

La fonction `same_color_neighbors()` renvoie une liste de blocs adjacents à un bloc donné (à la position x, y) et de même couleur. Elle utilise la fonction `filter()`, appliquée à la liste à plat complète des blocs dans `self.blocks`.

```lua
-- board.script
--
-- Returns a list of neighbor blocks of the same color as the
-- block on x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Une fonction utilitaire `in_blocklist()` vérifie si un bloc existe dans une liste de blocs :

```lua
-- board.script
--
-- Does the block exist in the list of blocks?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Nous utilisons ces fonctions lors des entrées tactiles et des glissements dans `on_input()` pour construire les chaînes de blocs touchés. Nous détectons et ignorons ici les blocs magiques, même s'il n'y en a pas encore :

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- If trying to manipulate magic blocks, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- List of neighbors of the same color as touched block
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Mark block.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- then drag
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- dragging over a same-colored neighbor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Mark block.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

Enfin, lorsque le contact tactile est relâché, supprimez visuellement tous les connecteurs des liaisons.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Connecteurs dans le jeu](images/magic-link/linker_connector_screen.png)

## Suppression des blocs reliés {#remove-linked-blocks}

La logique permettant de relier des blocs de même couleur est maintenant en place, et il est facile de supprimer les blocs reliés. Si nous définissons leur emplacement sur le plateau sur `hash("removing")` au lieu de simplement `nil`, c'est parce que, plus tard, lorsque nous implémenterons la logique des blocs magiques, nous devrons nous assurer qu'ils glissent uniquement vers les emplacements des blocs qui viennent d'être supprimés. Si nous définissons ici l'emplacement sur le plateau sur `nil`, nous ne pouvons pas distinguer les blocs qui viennent d'être supprimés de ceux qui l'ont été auparavant.

```lua
-- board.script
-- Remove the currently selected block-chain
--
local function remove_chain(self)
    -- Delete all chained blocks
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Nous aurons aussi besoin d'une fonction pour supprimer réellement (définir sur `nil`) les emplacements du plateau qui ont été définis sur `hash("removing")` :

```lua
-- board.script
--
-- Set removed blocks to nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Nous créons également une fonction qui fait descendre les blocs restants lorsque les blocs situés sous eux sont supprimés (définis sur `nil`). Nous parcourons le plateau colonne par colonne, de gauche à droite, et chaque colonne de bas en haut. Si nous rencontrons un emplacement vide (`nil`), nous faisons descendre tous les blocs situés au-dessus.

```lua
-- board.script
--
-- Apply shift-down logic to all blocks.
--
local function slide_board(self)
    -- Slide all remaining blocks down into blank spots.
    -- Going column by column makes this easy.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move down dy steps
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calc new position
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist needs updating
    build_blocklist(self)
end
```

![Descente des blocs](images/magic-link/linker_blocks_slide.png)

Nous pouvons maintenant simplement ajouter des appels à ces fonctions dans `on_input()` lorsque le contact tactile a été relâché et que `self.chain` contient des blocs.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and slide the remaining blocks down.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Empty chain of connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Logique des blocs magiques {#magic-block-logic}

Il est temps d'ajouter les blocs magiques. Tout d'abord, ajoutons la possibilité de transformer un bloc en bloc magique. Nous pourrons ainsi faire un passage distinct sur le plateau rempli et convertir les blocs de notre choix en blocs magiques. Pour donner un peu plus d'éclat aux blocs magiques, créons d'abord un effet magique animé sous la forme d'un objet de jeu *`magic_fx.go`*, que nous pourrons créer depuis le bloc magique.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Cet objet de jeu contient deux sprites. L'un représente la couleur "magic" (un sprite utilisant l'image *`magic-sphere_layer2.png`*) et l'autre est un effet "light" (un sprite utilisant l'image *`magic-sphere_layer3.png`*). L'objet est configuré pour tourner dès sa création, selon la valeur de la propriété `direction`. Nous faisons aussi en sorte que l'objet écoute deux messages : `lights_on` et `lights_off`, qui contrôlent le sprite de l'effet lumineux.

Créez un nouveau script et ajoutez-le comme composant script à *`magic_fx.go`* :

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Le bloc magique créera maintenant deux objets de jeu `magic_fx` à la réception du message `make_magic`. Chacun tournera dans une direction opposée, créant une jolie danse de couleurs à l'intérieur des blocs. Nous ajoutons également un sprite supplémentaire à *`block.go`* avec l'image *`magic-sphere_layer4.png`*. Cette image est placée à une coordonnée Z supérieure à celle de l'effet créé et dessine la coque, ou « enveloppe », de la sphère magique.

![Sprite de l'enveloppe](images/magic-link/linker_cover.png)

Notez que nous devons ajouter un composant *Factory* à l'objet de jeu du bloc et lui indiquer d'utiliser notre objet de jeu *`magic_fx.go`* comme *Prototype*. Le script du bloc doit également écouter les messages `lights_on` et `lights_off` et les transmettre aux objets créés. Notez que ces objets doivent être supprimés lorsque le bloc est supprimé. La fonction `final()` du bloc s'en charge. Tout cela se passe dans *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale_xy(0.18) -- render scaled down without changing Z

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale.xy", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale.xy", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Nous pouvons maintenant créer des blocs magiques et les illuminer, un effet que nous utiliserons pour indiquer qu'un bloc magique se trouve à côté d'un autre.

![Bloc magique sans et avec éclairage](images/magic-link/linker_magic_blocks.png)

Le code qui remplit le plateau de blocs doit maintenant être modifié pour y placer quelques blocs magiques :

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribute magic blocks.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Build 1d list that we can easily filter.
    build_blocklist(self)
end
```

La principale mécanique des blocs magiques est leur capacité à glisser latéralement lorsqu'un autre bloc disparaît à côté d'eux. Nous implémentons tous les détails de cette mécanique dans la fonction `slide_magic_blocks()` de *board.script*. L'algorithme est simple :

1. Pour chaque ligne du plateau, créez une liste `M` de blocs magiques.
2. Parcourez chaque bloc magique de la liste `M` jusqu'à ce que la liste ne diminue plus. À chaque itération :
    1. Si l'emplacement du bloc situé sous le bloc magique vaut `hash("removing")`, retirez simplement le bloc magique de la liste `M`.
    2. Si le bloc magique a un trou sur le côté marqué `hash("removing")`, faites-le glisser dans ce trou, définissez son ancien emplacement sur `hash("removing")`, puis retirez-le de la liste `M`.

```lua
-- board.script
-- Apply the shifting logic to magic blocks. Only slide to positions
-- marked for removal with hash("removing")
--
local function slide_magic_blocks(self)
    -- Slide all magic blocks to the side that should slide first.
    -- This works best going row by row!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Build list of magic blocks on this row.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Go through list, slide and remove if possible. Reiterate until the list does not shrink.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Hole below, do nothing.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Hole to the left! Slide magic block there
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Hole to the right. Slide magic block there
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calc new z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Will be nilled later
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Nous pouvons essayer cette mécanique en ajoutant un appel à la fonction dans `on_input()` :

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Nous voyons maintenant clairement pourquoi nous avons utilisé le marqueur intermédiaire `hash("removing")` sur les emplacements lors de leur suppression. Sans lui, les blocs magiques glisseraient d'un côté à l'autre dans n'importe quel emplacement vide adjacent. Une mécanique peut-être intéressante, mais qui ne correspond pas à celle prévue pour ce petit jeu.

Il nous faut maintenant une logique pour détecter si des blocs magiques sont connectés (situés à gauche, à droite, au-dessus ou au-dessous les uns des autres), et pour savoir si tous les blocs magiques du plateau sont connectés. L'algorithme utilisé est assez simple :

1. Créez une liste `M` de tous les blocs magiques du plateau.
2. Pour chaque bloc de la liste `M` :
    1. Si aucune `region` n'est définie pour le bloc, attribuez-lui le numéro de région `R` (initialement `1`).
    2. Marquez tous les voisins non marqués du bloc avec le même numéro de région `R`, puis poursuivez avec leurs voisins, les voisins de leurs voisins, et ainsi de suite.
    3. Augmentez le numéro de région `R` de `1`.

![Marquage des régions](images/magic-link/linker_regions.png)

Voici l'implémentation de l'algorithme :

```lua
-- board.script
--
-- Build list of all current magic blocks.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filter out adjacent magic blocks
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Spread region to neighbors
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Mark all magic block regions
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Clear all region marks and count neighbors
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Assign regions and spread them
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Nous créons aussi des fonctions permettant de compter le nombre de régions parmi les blocs magiques. S'il n'y a qu'une région, nous savons que tous les blocs magiques sont connectés. De plus, nous ajoutons une fonction qui éteint les lumières de tous les blocs magiques, et une autre qui active les effets lumineux des blocs magiques ayant des blocs magiques voisins :

```lua
-- board.script
--
-- Count the number of connected regions among the magic blocks.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Shut off lights on all listed magic blocks
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Set highlight for all magic blocks
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Nous pouvons maintenant intégrer ces éléments de logique au déroulement général. Tout d'abord, comme la génération du plateau est aléatoire, il existe une faible probabilité qu'il soit gagnant dès le départ. Si cela arrive, nous supprimons simplement le plateau et le reconstruisons :

```lua
-- board.script
--
-- Clear the board
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Build 1d list that we can easily filter.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Win" from start. Make new board.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

Le reste de la logique prend place dans `on_input()`. Il n'y a toujours pas de code pour traiter le message `level_completed`, mais cela convient pour le moment :

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- Player released touch.
        self.dragging = false

        if #self.chain > 1 then
            -- There is a chain of blocks. Remove it from board and refill board.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Slide remaining blocks down.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Highlight adjacent magic blocks.
            if count_magic_regions(magic_blocks) == 1 then
                -- Win!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Empty chain clears connector graphics.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Il est maintenant possible de jouer et d'atteindre la condition de victoire, même s'il ne se passe encore rien lorsque vous reliez tous les blocs magiques.

![Première victoire](images/magic-link/linker_first_win.png)

## Lâchers de blocs {#drops}

L'idée du « lâcher » est d'ajouter une mécanique de progression simple. Le joueur peut effectuer un nombre limité de lâchers en appuyant sur le bouton *DROP* : chaque lâcher fait simplement tomber quelques nouvelles pièces aléatoires sur le plateau. Le joueur commence avec un lâcher et en reçoit un supplémentaire chaque fois qu'il termine un niveau. Le code de cette mécanique tient dans deux fonctions : l'une renvoie la liste des emplacements où les blocs lâchés peuvent atterrir, et l'autre effectue le lâcher proprement dit, avec l'animation et tout le reste.

```lua
-- board.script
--
-- Find spots for a drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- If more than dropamount, randomly remove a slot until dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Perform the drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Pick a random color
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calc new z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Rebuild blocklist
    build_blocklist(self)
end
```

Nous pouvons tester les lâchers en exécutant le code suivant, par exemple dans `on_reload()`, ou en l'associant à une action d'entrée temporaire :

```lua
s = dropspots(self)
if #s > 0 then
    -- Do the drop
    drop(self, s)
end
```

![Lâcher de blocs](images/magic-link/linker_drop.png)

## Le menu principal {#the-main-menu}

Il est temps de tout assembler. Commençons par créer un écran de démarrage et le séparer du plateau. La première étape consiste à créer *main_menu.gui* et à y placer un bouton *Start* (un nœud de texte et un nœud de boîte texturé), un nœud de texte pour le titre et quelques blocs décoratifs (des nœuds de boîte texturés). Le script *main_menu.gui_script* que nous attachons à l'interface graphique anime les blocs décoratifs dans `init()`. Il contient aussi une fonction `on_input()` qui envoie un message `start_game` à un script principal. Nous allons créer ce script dans un instant.

![Interface graphique du menu principal](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Puisque le script du menu principal se chargera bientôt de démarrer le jeu, supprimez l'appel temporaire de création du plateau dans `init()`, dans *board.script* :

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contains the board structure
    self.blocks = {}            -- List of all blocks. Used for easy filtering on selection.

    self.chain = {}                -- Current selection chain
    self.connectors = {}        -- Connector elements to mark the selection chain
    self.num_magic = 3            -- Number of magic blocks on the board

    self.drops = 1                -- Number of drops you have available

    self.magic_blocks = {}        -- Magic blocks that are lined up

    self.dragging = false        -- Drag touch input
end
```

Le script principal conservera l'état général du jeu et démarrera la partie sur demande. Ici, nous voulons que *main.collection* contienne uniquement le minimum de ressources nécessaires à l'affichage au démarrage. Pour cela, *main.collection* contiendra un objet de jeu "main" regroupant l'interface graphique du menu principal, un composant script et, surtout, un composant *Collection Proxy*.

Le proxy de collection (collection proxy) nous permet de charger et de décharger dynamiquement des collections dans le jeu en cours d'exécution. Il agit au nom d'un fichier de collection donné : nous chargeons, initialisons, activons, désactivons et déchargeons la collection dynamique en envoyant des messages au proxy. Pour une description complète de leur utilisation, consultez la [documentation des proxys de collection](/manuals/collection-proxy).

Dans notre cas, nous définissons la propriété *Collection* du composant proxy de collection sur *board.collection*, qui contient le « niveau ».

![Collection principale](images/magic-link/linker_main_collection.png)

Nous devons maintenant ouvrir *game.project* et définir la collection bootstrap *main_collection* sur `/main/main.collectionc`.

![Collection principale au démarrage](images/magic-link/linker_bootstrap_main.png)

Démarrer une partie consiste maintenant à envoyer des messages à notre proxy de collection pour charger, initialiser et activer le plateau, puis à désactiver le menu principal (pour le masquer). Le retour au menu principal effectue l'opération inverse (à condition que le proxy ait chargé la collection).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- Board collection has loaded...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Notez que nous appelons le socket "main" : nous devons nous assurer que ce nom est défini dans *main.collection*. Sélectionnez le nœud racine et vérifiez que la propriété *Name* vaut "main".
2. De même, nous envoyons des messages à la collection chargée par l'intermédiaire de son socket, dont le nom est défini par la propriété *Name* de la collection.

## L'interface graphique en jeu {#the-in-game-gui}

Avant d'ajouter la dernière partie de la logique au script du plateau, nous devons ajouter au plateau un ensemble d'éléments d'interface graphique. Nous plaçons d'abord un bouton *RESTART* et un bouton *DROP* au-dessus du plateau.

![Interface graphique du plateau](images/magic-link/linker_board_gui.png)

Le script de l'interface graphique du plateau envoie des messages à la boîte de dialogue de redémarrage lors d'un clic, et au script du plateau lui-même lorsque l'on clique sur *DROP* :

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Show the restart dialog box.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

La boîte de dialogue *RESTART* est simple. Nous la créons dans *restart.gui* et lui attachons un script simple qui ne fait rien si le joueur clique sur *NO*, envoie un message `restart_level` au script du plateau s'il clique sur *YES*, et un message `to_main_menu` au script principal s'il clique sur *Quit to main menu* :

![Interface graphique de redémarrage](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Nous créons aussi une boîte de dialogue simple de fin de niveau dans *level_complete.gui*, avec un script simple qui envoie un message `next_level` au script du plateau lorsque le joueur clique sur *CONTINUE* :

![Boîte de dialogue de fin de niveau](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consume all input until we're gone.
    return true
end
```

Une boîte de dialogue sert à présenter le niveau actuel, avec un script qui se limite à la masquer et à l'afficher. Lors de l'affichage, son message est défini de manière à inclure le niveau de difficulté actuel :

![Interface graphique de présentation du niveau](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Nous ajoutons également une boîte de dialogue qui s'affiche si le joueur tente d'effectuer un lâcher alors qu'il n'y a pas de place.

![Interface graphique indiquant le manque de place pour un lâcher](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Enfin, nous ajoutons ces composants d'interface graphique à *board.collection* et le code nécessaire à *board.script* :

![Collection finale du plateau](images/magic-link/linker_board_collection_final.png)

Nous devons écrire le code de traitement de tous les messages envoyés depuis et vers le plateau dans `on_message()`.

`start_level`
: Définit le nombre de blocs magiques selon le paramètre de difficulté, construit le plateau, puis affiche la boîte de dialogue "present_level" pendant deux secondes avant de démarrer la partie (en retirant la boîte de dialogue et en acquérant le focus d'entrée). Notez que nous utilisons `go.animate()` comme temporisateur en animant la valeur de "timer", qui n'est utilisée à aucune autre fin.

`restart_level`
: C'est ce qui se produit lorsque le joueur appuie sur le bouton *RESTART* de l'interface graphique et confirme son choix. Vide et reconstruit le plateau, et réinitialise le compteur de lâchers.

`level_completed`
: Envoyé dès que le plateau est dans un état gagnant. Désactive les entrées, anime les blocs magiques et affiche la boîte de dialogue "level_complete". Celle-ci renverra un message `next_level` lorsque le joueur cliquera sur son bouton *CONTINUE*.

`next_level`
: À la réception de ce message, vide le plateau, augmente le compteur de lâchers et envoie `start_level` avec le niveau de difficulté suivant.

`drop`
: Vérifie où des lâchers sont possibles. S'il n'y a aucun emplacement disponible, affiche la boîte de dialogue "no_drop_room". Sinon, effectue le lâcher (s'il en reste au joueur), diminue le compteur de lâchers et met à jour son affichage.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Wait some...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- turn off input
        msg.post(".", "release_input_focus")

        -- Animate the magic!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale_xy(0.17, m.id)
            go.animate(m.id, "scale.xy", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Show completion screen
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- Difficulty level is number of magic blocks - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Can't perform drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Do the drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

Et voilà ! Le jeu et ce tutoriel sont maintenant terminés ! Amusez-vous bien avec ce jeu !

![Jeu terminé](images/magic-link/linker_game_finished.png)

## Pour aller plus loin {#moving-on}

Ce petit jeu présente des propriétés intéressantes et nous vous encourageons à expérimenter avec lui. Voici une liste d'exercices que vous pouvez réaliser pour vous familiariser davantage avec Defold :

* Clarifiez les interactions. Un nouveau joueur peut avoir du mal à comprendre le fonctionnement du jeu et les éléments avec lesquels il peut interagir. Prenez le temps de rendre le jeu plus clair, sans ajouter d'éléments de tutoriel.
* Ajoutez des sons. Le jeu est actuellement totalement silencieux et gagnerait à disposer d'une bande sonore agréable et de sons d'interaction.
* Détectez automatiquement la fin de partie.
* Meilleur score. Ajoutez une fonctionnalité de meilleur score persistante.
* Réimplémentez le jeu en utilisant uniquement les API GUI.
* Actuellement, le jeu continue en ajoutant un bloc magique à chaque passage au niveau suivant. Cela ne peut pas durer indéfiniment. Trouvez une solution satisfaisante à ce problème.
* Optimisez le jeu et réduisez le nombre maximal de sprites en les réutilisant au lieu de les supprimer et de les recréer.
* Implémentez un rendu du jeu indépendant de la résolution afin qu'il soit aussi beau sur des écrans de résolutions et de rapports d'aspect différents.
