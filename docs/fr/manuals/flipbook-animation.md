---
title: Manuel des animations image par image dans Defold
brief: Ce manuel décrit comment utiliser les animations image par image dans Defold.
---

# Animation image par image {#flip-book-animation}

Une animation image par image (flipbook) se compose d'une série d'images fixes affichées successivement. Cette technique est très proche de l'animation traditionnelle sur celluloïd (voir http://en.wikipedia.org/wiki/Traditional_animation). Elle offre des possibilités illimitées puisque chaque image peut être modifiée individuellement. Cependant, comme chaque image est stockée séparément, l'empreinte mémoire peut être importante. La fluidité de l'animation dépend également du nombre d'images affichées par seconde, mais augmenter ce nombre augmente généralement aussi la quantité de travail nécessaire. Dans Defold, les animations image par image sont stockées soit sous forme d'images individuelles ajoutées à un [atlas](/manuals/atlas), soit dans une [source de tuiles](/manuals/tilesource) où toutes les images sont disposées en une séquence horizontale.

  ![Planche d'animation](images/animation/animsheet.png){.inline}
  ![Course en boucle](images/animation/runloop.gif){.inline}

## Lecture des animations image par image {#playing-flip-book-animations}

Les sprites et les nœuds de boîte de l'interface graphique peuvent lire des animations image par image, que vous pouvez contrôler avec précision en cours d'exécution.

Sprites
: Pour lire une animation en cours d'exécution, utilisez la fonction [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Vous trouverez un exemple ci-dessous.

Nœuds de boîte de l'interface graphique
: Pour lire une animation en cours d'exécution, utilisez la fonction [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Vous trouverez un exemple ci-dessous.

::: sidenote
Le mode de lecture `Once Ping Pong` lit l'animation jusqu'à la dernière image, puis inverse l'ordre et la lit en sens inverse jusqu'à la **deuxième** image de l'animation, sans revenir à la première. Ce comportement facilite l'enchaînement des animations.
:::

### Exemple avec un sprite {#sprite-example}

Supposons que votre jeu possède une fonction "dodge" qui permet au joueur d'appuyer sur un bouton spécifique pour esquiver. Vous avez créé quatre animations pour accompagner cette fonction d'un retour visuel :

"idle"
: Une animation en boucle du personnage du joueur au repos.

"dodge_idle"
: Une animation en boucle du personnage du joueur au repos dans la posture d'esquive.

"start_dodge"
: Une animation de transition lue une seule fois, qui fait passer le personnage du joueur de la position debout à la posture d'esquive.

"stop_dodge"
: Une animation de transition lue une seule fois, qui fait repasser le personnage du joueur de la posture d'esquive à la position debout.

Le script suivant fournit la logique :

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### Exemple avec un nœud de boîte de l'interface graphique {#gui-box-node-example}

Lorsque vous sélectionnez une animation ou une image pour un nœud, vous lui attribuez en fait simultanément la source d'images (atlas ou source de tuiles) et l'animation par défaut. La source d'images est définie de manière statique dans le nœud, mais l'animation à lire peut être modifiée en cours d'exécution. Les images fixes sont traitées comme des animations à une seule image : changer d'image en cours d'exécution revient donc à lire une autre animation image par image pour le nœud :

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Fonctions de rappel de fin d'animation {#completion-callbacks}

Les fonctions `sprite.play_flipbook()` et `gui.play_flipbook()` acceptent une fonction de rappel Lua facultative comme dernier argument. Cette fonction est appelée lorsque l'animation est arrivée à son terme. Elle n'est jamais appelée pour les animations en boucle. La fonction de rappel peut servir à déclencher des événements à la fin d'une animation ou à enchaîner plusieurs animations. Exemples :

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
