---
title: Entrées des manettes de jeu dans Defold
brief: Ce manuel explique le fonctionnement des entrées des manettes de jeu.
---

::: sidenote
Il est recommandé de vous familiariser avec le fonctionnement général des entrées dans Defold, la manière de les recevoir et l'ordre dans lequel elles sont reçues dans vos fichiers de script. Pour en savoir plus sur le système d'entrée, consultez le [manuel de présentation des entrées](/manuals/input).
:::

# Manettes de jeu {#gamepads}
Les déclencheurs de manette vous permettent d'associer les entrées standard d'une manette aux fonctions du jeu. Les entrées de manette proposent des liaisons pour :

- Sticks gauche et droit (direction et clics)
- Croix directionnelles gauche et droite. La croix de droite correspond généralement aux boutons « A », « B », « X » et « Y » de la manette Xbox et aux boutons « carré », « cercle », « triangle » et « croix » de la manette Playstation.
- Gâchettes gauche et droite
- Boutons de tranche gauche et droit
- Boutons Start, Back et Guide

![](images/input/gamepad_bindings.png)

::: important
Les exemples ci-dessous utilisent les actions présentées dans l'image ci-dessus. Comme pour toutes les entrées, vous êtes libre de nommer vos actions d'entrée comme vous le souhaitez.
:::

## Boutons numériques {#digital-buttons}
Les boutons numériques génèrent des événements `pressed`, `released` et `repeated`. Voici un exemple montrant comment détecter l'entrée d'un bouton numérique (enfoncé ou relâché) :

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## Sticks analogiques {#analog-sticks}
Les sticks analogiques génèrent des événements d'entrée continus lorsque le stick est déplacé en dehors de la zone morte définie dans le fichier de paramètres des manettes (voir ci-dessous). Voici un exemple montrant comment détecter l'entrée d'un stick analogique :

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

Les sticks analogiques génèrent également des événements `pressed` et `released` lorsqu'ils sont déplacés dans les directions cardinales au-delà d'une certaine valeur seuil. Cela permet aussi d'utiliser facilement un stick analogique comme entrée directionnelle numérique :

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## Plusieurs manettes {#multiple-gamepads}
Defold prend en charge plusieurs manettes par l'intermédiaire du système d'exploitation hôte. Les actions définissent le champ `gamepad` de la table `action` sur le numéro de la manette dont provient l'entrée :

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## Connexion et déconnexion {#connect-and-disconnect}
Les liaisons d'entrée des manettes proposent également deux liaisons distinctes nommées `Connected` et `Disconnected` pour détecter la connexion d'une manette (y compris celles connectées dès le démarrage) ou sa déconnexion.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## Entrées brutes des manettes {#raw-gamepads}

Les liaisons d'entrée des manettes proposent également une liaison distincte nommée `Raw` qui fournit les entrées non filtrées (sans application de zone morte) des boutons, des axes et des chapeaux directionnels de toute manette connectée.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Fichier de paramètres des manettes {#gamepads-settings-file}

Les correspondances de manette traduisent ses boutons, axes et chapeaux directionnels en commandes standard utilisées par vos liaisons d'entrée. Defold combine deux sources de correspondances configurées dans la section *Input* de *game.project* :

| Paramètre | Format des correspondances | Valeur par défaut |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | Base de données textuelle au format SDL, avec correspondance par GUID de la manette | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Anciennes entrées `.gamepads` par nom de périphérique et plateforme | `/builtins/input/default.gamepads` |

Les correspondances de la base SDL et les correspondances automatiques de la plateforme utilisent [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone). Les anciennes entrées `.gamepads` définissent leurs propres zones mortes. Sur Android, une manette absente de la base peut aussi recevoir une [correspondance automatique](#gamepads-on-android).

### Anciennes correspondances .gamepads {#legacy-gamepads-mappings}

Un fichier `.gamepads` peut contenir des correspondances pour plusieurs manettes. Les anciennes correspondances existantes restent prises en charge. Defold inclut celles des manettes courantes dans le fichier par défaut :

![Paramètres des manettes](images/input/gamepads.png)

Si vous devez créer une ancienne correspondance `.gamepads` sur une plateforme de bureau, l'outil suivant peut vous aider. Pour Android, consultez [Manettes sous Android](#gamepads-on-android).

[Cliquez pour télécharger gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Il comprend des exécutables pour Windows, Linux et macOS. Exécutez-le depuis la ligne de commande :

```sh
./gdc
```

L'outil vous demandera d'appuyer sur différents boutons de votre manette connectée. Il produira ensuite un nouveau fichier gamepads contenant les correspondances correctes pour votre manette. Enregistrez le nouveau fichier ou fusionnez-le avec votre fichier gamepads existant, puis mettez à jour le paramètre dans *game.project* :

![Paramètres des manettes](images/input/gamepad_setting.png)

### Manettes non identifiées {#unidentified-gamepads}

Lorsqu'aucune correspondance configurée ni aucune correspondance automatique de la plateforme n'est disponible, la manette ne génère que les actions liées à `Connected`, `Disconnected` et `Raw`. Vous pouvez ajouter une correspondance de manette ou traiter ses entrées brutes dans votre jeu.

Vous pouvez vérifier si une action d'entrée de manette provient ou non d'une manette inconnue en lisant la valeur `gamepad_unknown` de `action` :

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
``` 

## Manettes en HTML5 {#gamepads-in-html5}
Les manettes sont prises en charge dans les builds HTML5 et génèrent les mêmes événements d'entrée que sur les autres plateformes. Leur prise en charge repose sur l'[API Gamepad](https://www.w3.org/TR/gamepad/), disponible dans la plupart des navigateurs ([consultez ce tableau de compatibilité](https://caniuse.com/?search=gamepad)). Si le navigateur ne prend pas en charge l'API Gamepad, Defold ignore sans avertissement tous les déclencheurs de manette de votre projet. Vous pouvez vérifier si le navigateur prend en charge l'API Gamepad en vérifiant si la fonction `getGamepads` existe sur l'objet `navigator` :

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Si votre jeu s'exécute à l'intérieur d'un `iframe`, vous devez également vous assurer que cet `iframe` dispose de l'autorisation `gamepad` :

```html
<iframe allow="gamepad"></iframe>
```

### Manette standard {#standard-gamepad}

Si le navigateur identifie une manette connectée comme une manette standard, elle utilise les correspondances de `Standard Gamepad` dans le [fichier de paramètres des manettes](/manuals/input-gamepads/#gamepads-settings-file) (des correspondances pour `Standard Gamepad` sont incluses dans le fichier `default.gamepads` de `/builtins`). Une manette standard est définie comme ayant 16 boutons et deux sticks analogiques, avec une disposition des boutons semblable à celle d'une manette PlayStation ou Xbox (consultez la [définition du W3C et la disposition des boutons](https://w3c.github.io/gamepad/#dfn-standard-gamepad) pour en savoir plus). Si la manette connectée n'est pas identifiée comme une manette standard, Defold recherche dans le fichier de paramètres des manettes des correspondances adaptées au type de manette physique.

## Manettes sous Windows {#gamepads-on-windows}
Sous Windows, seules les manettes XBox 360 sont actuellement prises en charge. Pour connecter votre manette 360 à votre ordinateur Windows, [assurez-vous qu'elle est correctement configurée](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Manettes sous Android {#gamepads-on-android}

Les manettes sont prises en charge dans les builds Android et génèrent les mêmes actions d'entrée que sur les autres plateformes. Defold utilise les [correspondances de manettes](#gamepads-settings-file) configurées et peut attribuer automatiquement une correspondance à certaines manettes sans entrée correspondante.

Si une manette n'est pas identifiée ou si ses commandes sont incorrectes, testez-la sur l'appareil Android et ajoutez ou mettez à jour sa correspondance. Consultez [Manettes non identifiées](#unidentified-gamepads) et [Entrées brutes des manettes](#raw-gamepads) pour le dépannage.
