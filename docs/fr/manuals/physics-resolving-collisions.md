---
title: Résolution des collisions cinématiques dans Defold
brief: Ce manuel explique comment résoudre les collisions physiques cinématiques.
---

# Résolution des collisions cinématiques {#resolving-kinematic-collisions}

L'utilisation d'objets de collision cinématiques vous oblige à résoudre vous-même les collisions et à déplacer les objets en réaction. Voici une implémentation naïve qui sépare deux objets en collision :

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

Ce code sépare votre objet cinématique des autres objets physiques qu'il pénètre, mais la séparation est souvent excessive et vous observerez des tremblements dans de nombreux cas. Pour mieux comprendre le problème, considérons le cas suivant, où un personnage contrôlé par le joueur est entré en collision avec deux objets, *A* et *B* :

![Collision physique](images/physics/collision_multi.png)

Le moteur physique envoie plusieurs messages `"contact_point_response"`, un pour l'objet *A* et un pour l'objet *B*, lors de l'image où la collision se produit. Si vous déplacez le personnage en réponse à chaque pénétration, comme dans le code naïf ci-dessus, la séparation obtenue est la suivante :

- Déplacement du personnage hors de l'objet *A* selon sa distance de pénétration (la flèche noire)
- Déplacement du personnage hors de l'objet *B* selon sa distance de pénétration (la flèche noire)

L'ordre de ces déplacements est arbitraire, mais le résultat est identique dans les deux cas : une séparation totale qui correspond à la *somme des vecteurs de pénétration individuels* :

![Séparation physique naïve](images/physics/separation_naive.png)

Pour séparer correctement le personnage des objets *A* et *B*, vous devez traiter la distance de pénétration de chaque point de contact et vérifier si des séparations précédentes ont déjà résolu la séparation, en tout ou en partie.

Supposons que le premier message de point de contact provienne de l'objet *A* et que vous déplaciez le personnage vers l'extérieur selon le vecteur de pénétration de *A* :

![Première étape de la séparation physique](images/physics/separation_step1.png)

Le personnage est alors déjà partiellement séparé de *B*. La compensation finale nécessaire pour le séparer complètement de l'objet *B* est indiquée par la flèche noire ci-dessus. La longueur du vecteur de compensation peut être calculée en projetant le vecteur de pénétration de *A* sur le vecteur de pénétration de *B* :

![Projection](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

Le vecteur de compensation s'obtient en réduisant la longueur de *B* de *l*. Pour effectuer ce calcul pour un nombre quelconque de pénétrations, vous pouvez accumuler la correction nécessaire dans un vecteur, en partant d'un vecteur de correction de longueur nulle et en procédant ainsi pour chaque point de contact :

1. Projetez la correction actuelle sur le vecteur de pénétration du contact.
2. Calculez la compensation restante à partir du vecteur de pénétration (selon la formule ci-dessus).
3. Déplacez l'objet selon le vecteur de compensation.
4. Ajoutez la compensation à la correction accumulée.

Voici une implémentation complète :

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
