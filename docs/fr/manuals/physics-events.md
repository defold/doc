---
title: Événements de collision dans Defold
brief: La gestion des événements de collision peut être centralisée à l'aide de `physics.set_event_listener()` pour diriger tous les messages de collision et d'interaction vers une seule fonction spécifiée.
---

# Gestion des événements physiques dans Defold {#defold-physics-event-handling}

Defold propose une gestion centralisée des événements physiques au moyen de la fonction `physics.set_event_listener()`. Cette fonction vous permet de définir un écouteur personnalisé pour gérer tous les événements d'interaction physique au même endroit, ce qui simplifie votre code et améliore son efficacité.

## Définition de l'écouteur du monde physique {#setting-the-physics-world-listener}

Dans Defold, chaque proxy de collection (collection proxy) crée son propre monde physique distinct. Par conséquent, lorsque vous travaillez avec plusieurs proxys de collection, il est essentiel de gérer les différents mondes physiques associés à chacun. Pour que les événements physiques soient traités correctement dans chaque monde, vous devez définir un écouteur de monde physique propre au monde de chaque proxy de collection.

Cela signifie que l'écouteur d'événements physiques doit être défini depuis le contexte de la collection que le proxy représente. Vous associez ainsi l'écouteur directement au monde physique concerné, ce qui lui permet de traiter correctement les événements physiques.

Voici un exemple montrant comment définir un écouteur de monde physique au sein d'un proxy de collection :

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

En appliquant cette méthode, vous vous assurez que chaque monde physique généré par un proxy de collection dispose de son propre écouteur. C'est indispensable pour gérer efficacement les événements physiques dans les projets qui utilisent plusieurs proxys de collection.

::: important
Si un écouteur est défini, les [messages physiques](/manuals/physics-messages) ne seront plus envoyés pour le monde physique dans lequel cet écouteur est défini.
:::

## Structure des données d'événement {#event-data-structure}

L'écouteur est appelé avec `self` et une table `events`. La table `events` est un tableau contenant tous les événements physiques collectés pour la fonction de rappel. Chaque entrée est une table d'événement comportant un champ `type` qui contient le nom haché de l'événement, ainsi que des champs supplémentaires propres à ce type d'événement.

Les tables d'événement contiennent les données suivantes :

1. **Événement de point de contact (`contact_point_event`) :**
Cet événement signale un point de contact entre deux objets de collision. Il est utile pour une gestion détaillée des collisions, par exemple pour calculer les forces d'impact ou définir des réponses personnalisées aux collisions.

   - `applied_impulse` : Impulsion résultant du contact.
   - `distance` : Distance de pénétration entre les objets.
   - `a` et `b` : Objets représentant les entités en collision, chacun contenant :
     - `position` : Position du point de contact dans le monde (vector3).
     - `instance_position` : Position de l'instance d'objet de jeu (game object) dans le monde (vector3).
     - `id` : Identifiant de l'instance (hash).
     - `group` : Groupe de collision (hash).
     - `relative_velocity` : Vitesse par rapport à l'autre objet (vector3).
     - `mass` : Masse en kilogrammes (number).
     - `normal` : Normale du contact, orientée depuis l'autre objet (vector3).

2. **Événement de collision (`collision_event`) :**
Cet événement indique qu'une collision s'est produite entre deux objets. Il est plus général que l'événement de point de contact et convient parfaitement à la détection des collisions lorsqu'aucune information détaillée sur les points de contact n'est nécessaire.

   - `a` et `b` : Objets représentant les entités en collision, chacun contenant :
     - `position` : Position dans le monde (vector3).
     - `id` : Identifiant de l'instance (hash).
     - `group` : Groupe de collision (hash).

3. **Événement de déclenchement (`trigger_event`) :** 
Cet événement est envoyé lorsqu'un objet interagit avec un objet déclencheur. Il est utile pour créer dans votre jeu des zones qui provoquent une action lorsqu'un objet y entre ou en sort.

   - `enter` : Indique si l'interaction correspond à une entrée (true) ou à une sortie (false).
   - `a` et `b` : Objets impliqués dans l'événement de déclenchement, chacun contenant :
     - `id` : Identifiant de l'instance (hash).
     - `group` : Groupe de collision (hash).

4. **Réponse au lancer de rayon (`ray_cast_response`) :**
Cet événement est envoyé en réponse à un lancer de rayon et fournit des informations sur l'objet touché par le rayon.

   - `group` : Groupe de collision de l'objet touché (hash).
   - `request_id` : Identifiant de la requête de lancer de rayon (number).
   - `position` : Position de l'impact (vector3).
   - `fraction` : Fraction de la longueur du rayon à laquelle l'impact s'est produit (number).
   - `normal` : Normale à la position de l'impact (vector3).
   - `id` : Identifiant de l'instance de l'objet touché (hash).

5. **Lancer de rayon sans impact (`ray_cast_missed`) :**
Cet événement est envoyé lorsqu'un lancer de rayon ne touche aucun objet.

   - `request_id` : Identifiant de la requête de lancer de rayon qui n'a touché aucun objet (number).

## Exemple d'utilisation {#example-usage}

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## Limitations {#limitations}

L'écouteur est appelé de manière synchrone au moment où l'événement se produit. Cet appel a lieu au milieu d'un pas de temps, ce qui signifie que le monde physique est verrouillé. Il est donc impossible d'utiliser des fonctions qui peuvent modifier les simulations du monde physique, par exemple `physics.create_joint()`.

Voici un petit exemple montrant comment contourner ces limitations :
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
