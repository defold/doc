---
title: Messages de collision dans Defold
brief: Lorsque deux objets entrent en collision, le moteur appelle la fonction de rappel d'événement ou diffuse des messages.
---

# Messages de collision {#collision-messages}

Lorsque deux objets entrent en collision, le moteur envoie un événement à la fonction de rappel (callback) d'événement ou diffuse des messages aux deux objets.

## Filtrage des événements {#event-filtering}

Vous pouvez contrôler les types d'événements générés à l'aide des options de chaque objet :

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

Elles valent toutes `true` par défaut.
Lorsque deux objets de collision interagissent, nous vérifions si nous devons envoyer un message à l'utilisateur en fonction de ces cases à cocher.

Par exemple, avec les cases à cocher "Generate Contact Events" :

Avec `physics.set_event_listener()` :

| Composant A | Composant B | Envoi d'un message |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | Oui          |
| ❌          | ✅︎          | Oui          |
| ✅︎          | ❌          | Oui          |
| ❌          | ❌          | Non          |

Avec le gestionnaire de messages par défaut :

| Composant A | Composant B | Envoi de message(s)   |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | Oui (A,B) + (B,A) |
| ❌          | ✅︎          | Oui (B,A)         |
| ✅︎          | ❌          | Oui (A,B)         |
| ❌          | ❌          | Non               |

## Réponse à une collision {#collision-response}

Le message `"collision_response"` est envoyé lorsque l'un des objets en collision est de type "dynamic", "kinematic" ou "static". Les champs suivants sont renseignés :

`other_id`
: l'identifiant de l'instance avec laquelle l'objet de collision est entré en collision (`hash`)

`other_position`
: la position dans le monde de l'instance avec laquelle l'objet de collision est entré en collision (`vector3`)

`other_group`
: le groupe de collision de l'autre objet de collision (`hash`)

`own_group`
: le groupe de collision de l'objet de collision (`hash`)

Le message `collision_response` ne convient que pour résoudre les collisions qui ne nécessitent aucun détail sur l'intersection réelle des objets, par exemple pour détecter si une balle touche un ennemi. Un seul de ces messages est envoyé par image pour chaque paire d'objets en collision.

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## Réponse à un point de contact {#contact-point-response}

Le message `"contact_point_response"` est envoyé lorsque l'un des objets en collision est de type "dynamic" ou "kinematic" et que l'autre est de type "dynamic", "kinematic" ou "static". Les champs suivants sont renseignés :

`position`
: la position du point de contact dans le monde (`vector3`).

`normal`
: la normale du point de contact dans l'espace du monde, orientée de l'autre objet vers l'objet actuel (`vector3`).

`relative_velocity`
: la vitesse relative de l'objet de collision observée depuis l'autre objet (`vector3`).

`distance`
: la distance de pénétration entre les objets -- positive ou nulle (`number`).

`applied_impulse`
: l'impulsion résultant du contact (`number`).

`life_time`
: (*actuellement inutilisé !*) la durée de vie du contact (`number`).

`mass`
: la masse de l'objet de collision actuel en kg (`number`).

`other_mass`
: la masse de l'autre objet de collision en kg (`number`).

`other_id`
: l'identifiant de l'instance avec laquelle l'objet de collision est en contact (`hash`).

`other_position`
: la position de l'autre objet de collision dans le monde (`vector3`).

`other_group`
: le groupe de collision de l'autre objet de collision (`hash`).

`own_group`
: le groupe de collision de l'objet de collision (`hash`).

Pour un jeu ou une application où vous devez séparer parfaitement les objets, le message `"contact_point_response"` vous fournit toutes les informations nécessaires. Cependant, pour une paire d'objets en collision donnée, plusieurs messages `"contact_point_response"` peuvent être reçus à chaque image, selon la nature de la collision. Consultez le [manuel sur la résolution des collisions pour en savoir plus](/manuals/physics-resolving-collisions).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## Réponse de déclencheur {#trigger-response}

Le message `"trigger_response"` est envoyé lorsque l'un des objets en collision est de type "trigger". Il est envoyé une première fois lorsque la collision est détectée, puis une seconde fois lorsque les objets ne sont plus en collision. Il comporte les champs suivants :

`other_id`
: l'identifiant de l'instance avec laquelle l'objet de collision est entré en collision (`hash`).

`enter`
: `true` si l'interaction correspond à une entrée dans le déclencheur, `false` s'il s'agit d'une sortie. (`boolean`).

`other_group`
: le groupe de collision de l'autre objet de collision (`hash`).

`own_group`
: le groupe de collision de l'objet de collision (`hash`).

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
