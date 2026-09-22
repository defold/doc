---
title: Entrées de la souris et entrées tactiles dans Defold
brief: Ce manuel explique le fonctionnement des entrées de la souris et des entrées tactiles.
---

::: sidenote
Il est recommandé de vous familiariser avec le fonctionnement général des entrées dans Defold, la façon de les recevoir et leur ordre de réception dans vos fichiers de script. Pour en savoir plus sur le système d'entrée, consultez le [manuel de présentation des entrées](/manuals/input).
:::

# Déclencheurs de la souris {#mouse-triggers}
Les déclencheurs de la souris vous permettent d'associer les entrées des boutons et des molettes de la souris à des actions du jeu.

![](images/input/mouse_bindings.png)

::: sidenote
Les entrées des boutons de la souris `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` et `MOUSE_BUTTON_MIDDLE` sont équivalentes à `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` et `MOUSE_BUTTON_3`.
:::

::: important
Les exemples ci-dessous utilisent les actions présentées dans l'image ci-dessus. Comme pour toutes les entrées, vous êtes libre de nommer vos actions d'entrée comme vous le souhaitez.
:::

## Boutons de la souris {#mouse-buttons}
Les boutons de la souris génèrent des événements `pressed`, `released` et `repeated`. Voici un exemple montrant comment détecter les entrées du bouton gauche de la souris (enfoncé ou relâché) :

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- left mouse button pressed
        elseif action.released then
            -- left mouse button released
        end
    end
end
```

::: important
Les actions d'entrée `MOUSE_BUTTON_LEFT` (ou `MOUSE_BUTTON_1`) sont également envoyées pour les entrées tactiles à un seul point de contact.
:::

## Molette de la souris {#mouse-wheel}
Les entrées de la molette de la souris détectent les actions de défilement. Le champ `action.value` vaut `1` si la molette est tournée et `0` sinon. (Les actions de défilement sont traitées comme des pressions sur des boutons. Defold ne prend actuellement pas en charge les entrées de défilement de haute précision des pavés tactiles.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- mouse wheel is scrolled up
        end
    end
end
```

## Déplacement de la souris {#mouse-movement}
Le déplacement de la souris est traité séparément. Les événements de déplacement de la souris ne sont reçus que si au moins un déclencheur de souris est configuré dans vos associations d'entrée.

Le déplacement de la souris n'est pas configuré dans les associations d'entrée, mais `action_id` est défini sur `nil` et la table `action` est remplie avec la position de la souris et la variation de cette position.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- let game object follow mouse/touch movement
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Déclencheurs tactiles {#touch-triggers}
Les déclencheurs à un seul point de contact et les déclencheurs multitactiles sont disponibles sur les appareils iOS et Android dans les applications natives et les bundles HTML5.

![](images/input/touch_bindings.png)

## Tactile à un seul point de contact {#single-touch}
Les déclencheurs à un seul point de contact ne sont pas configurés dans la section Touch Triggers des associations d'entrée. **Les déclencheurs à un seul point de contact sont configurés automatiquement lorsque vous avez configuré une entrée de bouton de souris pour `MOUSE_BUTTON_LEFT` ou `MOUSE_BUTTON_1`**.

## Multitactile {#multi-touch}
Les déclencheurs multitactiles remplissent une table appelée `touch` dans la table de l'action. Les éléments de cette table sont indexés par des nombres entiers de `1` à `N`, où `N` est le nombre de points de contact. Chaque élément de la table contient des champs avec les données d'entrée :

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Spawn at each touch point
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Le multitactile ne doit pas être associé à la même action que l'entrée de bouton de souris pour `MOUSE_BUTTON_LEFT` ou `MOUSE_BUTTON_1`. Associer la même action remplacera les entrées tactiles à un seul point de contact et vous empêchera de recevoir les événements correspondants.
:::

::: sidenote
La [ressource Defold-Input](https://defold.com/assets/defoldinput/) vous permet de configurer facilement des commandes virtuelles à l'écran, telles que des boutons et des sticks analogiques, avec une prise en charge du multitactile.
:::


## Détection des clics ou des appuis sur les objets {#detecting-click-or-tap-on-objects}
Détecter quand l'utilisateur a cliqué ou appuyé sur un composant (component) visuel est une opération très courante, nécessaire dans de nombreux jeux. Il peut s'agir d'une interaction avec un bouton ou un autre élément d'interface utilisateur, ou avec un objet de jeu (game object), tel qu'une unité contrôlée par le joueur dans un jeu de stratégie, un trésor dans un niveau de jeu d'exploration de donjons ou un donneur de quête dans un jeu de rôle. L'approche à utiliser varie selon le type de composant visuel.

### Détection des interactions avec les nœuds GUI {#detecting-interaction-with-gui-nodes}
Pour les éléments d'interface utilisateur, la fonction `gui.pick_node(node, x, y)` renvoie `true` ou `false` selon que les coordonnées spécifiées se trouvent ou non dans les limites d'un nœud GUI. Consultez la [documentation de l'API](/ref/gui/#gui.pick_node:node-x-y), l'[exemple de survol avec le pointeur](/examples/gui/pointer_over/) ou l'[exemple de bouton](/examples/gui/button/) pour en savoir plus.

### Détection des interactions avec les objets de jeu {#detecting-interaction-with-game-objects}
Pour les objets de jeu, il est plus compliqué de détecter les interactions, car des éléments tels que la translation de la caméra et la projection du script de rendu influent sur les calculs nécessaires. Il existe deux approches générales pour détecter les interactions avec les objets de jeu :

  1. Suivez la position et la taille des objets de jeu avec lesquels l'utilisateur peut interagir et vérifiez si les coordonnées de la souris ou du point de contact se trouvent dans les limites de l'un de ces objets.
  2. Attachez des objets de collision aux objets de jeu avec lesquels l'utilisateur peut interagir, ajoutez un objet de collision qui suit la souris ou le doigt et vérifiez les collisions entre eux.

::: sidenote
La [ressource Defold-Input](https://defold.com/assets/defoldinput/) propose une solution prête à l'emploi qui utilise des objets de collision pour détecter les entrées de l'utilisateur, avec une prise en charge du glissement et du clic.
:::

Dans les deux cas, il est nécessaire d'effectuer une conversion entre les coordonnées de l'événement de souris ou de contact dans l'espace écran et les coordonnées des objets de jeu dans l'espace monde. Vous pouvez procéder de différentes façons :

  * Suivez manuellement la vue et la projection utilisées par le script de rendu et servez-vous-en pour effectuer la conversion vers et depuis l'espace monde. Consultez le [manuel de la caméra pour un exemple](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Utilisez une [solution de caméra tierce](/manuals/camera/#third-party-camera-solutions) et ses fonctions de conversion de l'espace écran vers l'espace monde.
