---
title: Articulations physiques dans Defold
brief: Defold prend en charge les articulations pour la physique en 2D. Ce manuel explique comment créer et utiliser des articulations.
---

# Articulations {#joints}

Defold prend en charge les articulations (joints) pour la physique en 2D. Une articulation relie deux objets de collision au moyen d'une contrainte. Les types d'articulations pris en charge sont les suivants :

* **Fixe (physics.JOINT_TYPE_FIXED)** - Une articulation de type corde qui limite la distance maximale entre deux points. Dans Box2D, elle est appelée articulation de type corde (Rope joint).
* **Pivot (physics.JOINT_TYPE_HINGE)** - Une articulation pivot définit un point d'ancrage sur deux objets de collision et les déplace de manière que les deux objets de collision restent toujours au même endroit, sans restreindre leur rotation relative. L'articulation pivot peut activer un moteur avec un couple maximal et une vitesse définis. Dans Box2D, elle est appelée [articulation pivot (Revolute joint)](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Soudure (physics.JOINT_TYPE_WELD)** - Une articulation de type soudure tente de contraindre tous les mouvements relatifs entre deux objets de collision. L'articulation de type soudure peut être rendue souple comme un ressort en définissant une fréquence et un taux d'amortissement. Dans Box2D, elle est appelée [articulation de type soudure (Weld joint)](https://box2d.org/documentation/group__weld__joint.html#details).
* **Ressort (physics.JOINT_TYPE_SPRING)** - Une articulation de type ressort maintient une distance constante entre deux objets de collision. L'articulation de type ressort peut être rendue souple comme un ressort en définissant une fréquence et un taux d'amortissement. Dans Box2D, elle est appelée [articulation de distance (Distance joint)](https://box2d.org/documentation/group__distance__joint.html#details).
* **Glissière (physics.JOINT_TYPE_SLIDER)** - Une articulation glissière permet la translation relative de deux objets de collision le long d'un axe spécifié et empêche leur rotation relative. Dans Box2D, elle est appelée [articulation prismatique (Prismatic joint)](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **Roue (physics.JOINT_TYPE_WHEEL)** - Une articulation de type roue contraint un point de `bodyB` à se déplacer sur une ligne de `bodyA`. L'articulation de type roue fournit également un ressort de suspension. Dans Box2D, elle est appelée [articulation de type roue (Wheel joint)](https://box2d.org/documentation/group__wheel__joint.html#details).

## Création d'articulations {#creating-joints}

Pour le moment, les articulations ne peuvent être créées que par programmation à l'aide de [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) :
::: sidenote
La prise en charge de la création d'articulations dans l'éditeur est prévue, mais aucune date de sortie n'a été fixée.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Le code ci-dessus crée une articulation fixe portant l'identifiant `my_test_joint` entre les deux objets de collision `obj_a#collisionobject` et `obj_b#collisionobject`. L'articulation est reliée à un point situé 10 pixels à droite du centre de l'objet de collision `obj_a#collisionobject` et à un point situé 20 pixels au-dessus du centre de l'objet de collision `obj_b#collisionobject`. La longueur maximale de l'articulation est de 20 pixels.

## Destruction d'articulations {#destroying-joints}

Vous pouvez détruire une articulation à l'aide de [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) :

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Lecture et mise à jour des articulations {#reading-from-and-updating-joints}

Vous pouvez lire les propriétés d'une articulation à l'aide de [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) et les définir à l'aide de [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) :

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- increase motor speed by 100 revolutions per second
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Récupération de la force et du couple de réaction d'une articulation {#get-joint-reaction-force-and-torque}

Vous pouvez lire la force et le couple de réaction appliqués à une articulation à l'aide de [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) et de [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
