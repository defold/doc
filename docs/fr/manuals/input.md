---
title: Entrées des périphériques dans Defold
brief: Ce manuel explique le fonctionnement des entrées, comment capturer les actions d'entrée et créer des réactions interactives dans les scripts.
---

# Entrées {#input}

Toutes les entrées utilisateur sont capturées par le moteur et transmises sous forme d'actions aux composants (component) script et script d'interface graphique des objets de jeu (game object) qui ont acquis le focus d'entrée et qui implémentent la fonction `on_input()`. Ce manuel explique comment configurer les liaisons pour capturer les entrées et comment écrire du code qui y réagit.

Le système d'entrée utilise un ensemble de concepts simples et puissants qui vous permettent de gérer les entrées selon les besoins de votre jeu.

![Liaisons d'entrée](images/input/overview.png)

Périphériques
: Les périphériques d'entrée intégrés à votre ordinateur ou appareil mobile, ou qui y sont connectés, fournissent des entrées brutes au niveau du système à l'environnement d'exécution Defold. Les types de périphériques suivants sont pris en charge :

  1. Clavier (touches individuelles et saisie de texte)
  2. Souris (position, clics sur les boutons et actions de la molette)
  3. Entrées tactiles simples et multitactiles (sur les appareils iOS et Android et en HTML5 sur mobile)
  4. Manettes (selon la prise en charge par le système d'exploitation et les correspondances définies dans le fichier [gamepads](/manuals/input-gamepads/#gamepads-settings-file))

Liaisons d'entrée
: Avant qu'une entrée ne soit envoyée à un script, l'entrée brute du périphérique est convertie en *actions* significatives au moyen de la table des liaisons d'entrée.

Actions
: Les actions sont identifiées par les noms (hachés) que vous indiquez dans le fichier de liaisons d'entrée. Chaque action contient également les données pertinentes sur l'entrée : si un bouton est enfoncé ou relâché, les coordonnées de la souris et du contact tactile, etc.

Écouteurs d'entrées
: Tout composant script ou script d'interface graphique peut recevoir des actions d'entrée en *acquérant le focus d'entrée*. Plusieurs écouteurs peuvent être actifs en même temps.

Pile d'entrée
: La liste des écouteurs d'entrées, avec le premier à avoir acquis le focus en bas de la pile et le dernier en haut.

Consommation des entrées
: Un script peut choisir de consommer l'entrée qu'il a reçue, empêchant ainsi les écouteurs situés plus bas dans la pile de la recevoir.

## Configuration des liaisons d'entrée {#setting-up-input-bindings}

Les liaisons d'entrée constituent une table commune à l'ensemble du projet qui vous permet de spécifier comment les entrées des périphériques doivent être converties en *actions* nommées avant d'être transmises à vos composants script et scripts d'interface graphique. Vous pouvez créer un nouveau fichier de liaisons d'entrée : <kbd>faites un clic droit</kbd> sur un emplacement dans la vue *Assets* et sélectionnez <kbd>New... ▸ Input Binding</kbd>. Pour que le moteur utilise le nouveau fichier, modifiez l'entrée *Game Binding* dans *game.project*.

![Paramètre des liaisons d'entrée](images/input/setting.png)

Un fichier de liaisons d'entrée par défaut est automatiquement créé avec tous les modèles de nouveaux projets ; il n'est donc généralement pas nécessaire d'en créer un autre. Le fichier par défaut s'appelle `game.input_binding` et se trouve dans le dossier `input` à la racine du projet. <kbd>Double-cliquez</kbd> sur le fichier pour l'ouvrir dans l'éditeur :

![Configuration des liaisons d'entrée](images/input/input_binding.png)

Pour créer une nouvelle liaison, cliquez sur le bouton <kbd>+</kbd> en bas de la section correspondant au type de déclencheur. Chaque entrée comporte deux champs :

*Input*
: L'entrée brute à écouter, sélectionnée dans une liste déroulante des entrées disponibles.

*Action*
: Le nom d'action attribué aux actions d'entrée lorsqu'elles sont créées et transmises à vos scripts. Le même nom d'action peut être attribué à plusieurs entrées. Par exemple, vous pouvez lier la touche <kbd>Space</kbd> et le bouton `A` de la manette à l'action `jump`. Notez qu'un bug connu empêche malheureusement les entrées tactiles d'utiliser les mêmes noms d'action que les autres entrées.

## Types de déclencheurs {#trigger-types}

Vous pouvez créer cinq types de déclencheurs propres aux périphériques :

Key Triggers
: Entrées provenant de touches individuelles du clavier. Chaque touche est associée séparément à une action correspondante. Pour en savoir plus, consultez le [manuel sur les entrées clavier et la saisie de texte](/manuals/input-key-and-text).

Text Triggers
: Les déclencheurs de texte servent à lire du texte saisi librement. Pour en savoir plus, consultez le [manuel sur les entrées clavier et la saisie de texte](/manuals/input-key-and-text)

Mouse Triggers
: Entrées provenant des boutons et des molettes de la souris. Pour en savoir plus, consultez le [manuel sur les entrées souris et tactiles](/manuals/input-mouse-and-touch).

Touch Triggers
: Les déclencheurs tactiles simples et multitactiles sont disponibles sur les appareils iOS et Android dans les applications natives et les bundles HTML5. Pour en savoir plus, consultez le [manuel sur les entrées souris et tactiles](/manuals/input-mouse-and-touch).

Gamepad Triggers
: Les déclencheurs de manette vous permettent de lier les entrées standard des manettes aux fonctions du jeu. Pour en savoir plus, consultez le [manuel sur les manettes](/manuals/input-gamepads).

### Entrées de l'accéléromètre {#accelerometer-input}

En plus des cinq types de déclencheurs répertoriés ci-dessus, Defold prend également en charge les entrées de l'accéléromètre dans les applications natives Android et iOS. Cochez la case *Use Accelerometer* dans la section *Input* de votre fichier *game.project*.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- react to accelerometer data
    end
end
```

## Focus d'entrée {#input-focus}

Pour écouter les actions d'entrée dans un composant script ou un script d'interface graphique, le message `acquire_input_focus` doit être envoyé à l'objet de jeu qui contient le composant :

```lua
-- tell the current game object (".") to acquire input focus
msg.post(".", "acquire_input_focus")
```

Ce message demande au moteur d'ajouter à la *pile d'entrée* les composants capables de recevoir des entrées présents dans les objets de jeu (composants script, composants d'interface graphique et proxys de collection (collection proxy)). Les composants de l'objet de jeu sont placés en haut de la pile d'entrée ; le composant ajouté en dernier se trouvera au sommet de la pile. Notez que si l'objet de jeu contient plusieurs composants capables de recevoir des entrées, ils seront tous ajoutés à la pile :

![Pile d'entrée](images/input/input_stack.png)

Si un objet de jeu qui a déjà acquis le focus d'entrée l'acquiert à nouveau, son ou ses composants seront déplacés en haut de la pile.


## Distribution des entrées et on_input() {#input-dispatch-and-on_input}

Les actions d'entrée sont transmises selon l'ordre de la pile d'entrée, du haut vers le bas.

![Distribution des actions](images/input/actions.png)

Pour tout composant de la pile qui contient une fonction `on_input()`, cette fonction sera appelée une fois pour chaque action d'entrée au cours de l'image, avec les arguments suivants :

`self`
: L'instance actuelle du script.

`action_id`
: Le nom haché de l'action, tel qu'il est configuré dans les liaisons d'entrée.

`action`
: Une table contenant les données utiles sur l'action, comme la valeur de l'entrée, son emplacement (positions absolues et variations de position), si le bouton a été enfoncé (`pressed`), etc. Consultez [on_input()](/ref/go#on_input) pour plus de détails sur les champs d'action disponibles.

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- move left
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- move right
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Focus d'entrée et composants proxy de collection {#input-focus-and-collection-proxy-components}

Chaque monde de jeu (game world) chargé dynamiquement par un proxy de collection possède sa propre pile d'entrée. Pour que les actions soient transmises à la pile d'entrée du monde chargé, le composant proxy doit figurer dans la pile d'entrée du monde principal. Tous les composants de la pile d'un monde chargé sont traités avant que la distribution se poursuive vers le bas de la pile principale :

![Distribution des actions aux proxys](images/input/proxy.png)

::: important
Oublier d'envoyer `acquire_input_focus` à l'objet de jeu qui contient le composant proxy de collection est une erreur courante. Omettre cette étape empêche les entrées d'atteindre tous les composants de la pile d'entrée du monde chargé.
:::


### Libération du focus d'entrée {#releasing-input}

Pour cesser d'écouter les actions d'entrée, envoyez un message `release_input_focus` à l'objet de jeu. Ce message retirera tous les composants de cet objet de jeu de la pile d'entrée :

```lua
-- tell the current game object (".") to release input focus.
msg.post(".", "release_input_focus")
```


## Consommation des entrées {#consuming-input}

La fonction `on_input()` d'un composant peut contrôler activement si les actions doivent être transmises plus bas dans la pile ou non :

- Si `on_input()` renvoie `false`, ou si aucune valeur de retour n'est indiquée (ce qui implique un retour de `nil`, une valeur fausse en Lua), les actions d'entrée seront transmises au composant suivant dans la pile d'entrée.
- Si `on_input()` renvoie `true`, l'entrée est consommée. Aucun composant situé plus bas dans la pile d'entrée ne la recevra. Notez que cela s'applique à *toutes* les piles d'entrée. Un composant de la pile d'un monde chargé par proxy peut consommer une entrée et empêcher les composants de la pile principale de la recevoir :

![Consommation des entrées](images/input/consuming.png)

Dans de nombreux cas, la consommation des entrées offre un moyen simple et puissant de transférer les entrées entre différentes parties d'un jeu. Par exemple, si vous avez besoin d'un menu en surimpression qui soit temporairement la seule partie du jeu à écouter les entrées :

![Consommation des entrées](images/input/game.png)

Le menu de pause est initialement masqué (désactivé) et il est activé lorsque le joueur touche l'élément `PAUSE` de l'affichage tête haute (HUD) :

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- Did the player press PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Tell the pause menu to take over.
            msg.post("pause_menu", "show")
        end
    end
end
```

![Menu de pause](images/input/game_paused.png)

L'interface graphique du menu de pause acquiert le focus d'entrée et consomme les entrées, empêchant toute entrée autre que celles qui concernent le menu en surimpression :

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Show the pause menu.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Acquire input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- do things...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Hide the pause menu
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Release input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume all input. Anything below us on the input stack
  -- will never see input until we release input focus.
  return true
end
```
