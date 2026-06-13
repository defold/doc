---
title: Articulaciones de físicas en Defold
brief: Defold admite articulaciones para físicas 2D. Este manual explica cómo crear articulaciones y trabajar con ellas.
---

# Articulaciones

Defold admite articulaciones (joints) para físicas 2D. Una articulación conecta dos objetos de colisión mediante algún tipo de restricción. Los tipos de articulación compatibles son:

* **Fixed (physics.JOINT_TYPE_FIXED)** - Una articulación de cuerda que restringe la distancia máxima entre dos puntos. En Box2D se conoce como Rope joint.
* **Hinge (physics.JOINT_TYPE_HINGE)** - Una articulación de bisagra especifica un punto de anclaje en dos objetos de colisión y los mueve para que los dos objetos de colisión estén siempre en el mismo lugar, sin restringir la rotación relativa de los objetos de colisión. La articulación de bisagra puede activar un motor con torque máximo y velocidad definidos. En Box2D se conoce como [Revolute joint](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Weld (physics.JOINT_TYPE_WELD)** - Una articulación soldada intenta restringir todo el movimiento relativo entre dos objetos de colisión. La articulación soldada se puede suavizar como un resorte mediante una frecuencia y una relación de amortiguación. En Box2D se conoce como [Weld joint](https://box2d.org/documentation/group__weld__joint.html#details).
* **Spring (physics.JOINT_TYPE_SPRING)** - Una articulación de resorte mantiene dos objetos de colisión a una distancia constante entre sí. La articulación de resorte se puede suavizar como un resorte mediante una frecuencia y una relación de amortiguación. En Box2D se conoce como [Distance joint](https://box2d.org/documentation/group__distance__joint.html#details).
* **Slider (physics.JOINT_TYPE_SLIDER)** - Una articulación deslizante permite la traslación relativa de dos objetos de colisión a lo largo de un eje especificado e impide la rotación relativa. En Box2D se conoce como [Prismatic joint](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **Wheel (physics.JOINT_TYPE_WHEEL)** - Una articulación de rueda restringe un punto en `bodyB` a una línea en `bodyA`. La articulación de rueda también proporciona un resorte de suspensión. En Box2D se conoce como  [Wheel joint](https://box2d.org/documentation/group__wheel__joint.html#details).

## Crear articulaciones

Actualmente, las articulaciones solo se pueden crear programáticamente usando [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Está previsto agregar soporte en el editor para crear articulaciones, pero aún no se ha decidido una fecha de lanzamiento.
:::

```lua
-- conecta dos objetos de colisión con una restricción de articulación fija (cuerda)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Lo anterior creará una articulación fija con id `my_test_joint`, conectada entre los dos objetos de colisión `obj_a#collisionobject` y `obj_b#collisionobject`. La articulación está conectada 10 píxeles a la izquierda del centro del objeto de colisión `obj_a#collisionobject` y 20 píxeles por encima del centro del objeto de colisión `obj_b#collisionobject`. La longitud máxima de la articulación es de 20 píxeles.

## Destruir articulaciones

Una articulación se puede destruir usando [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destruye una articulación conectada previamente al primer objeto de colisión
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Leer y actualizar articulaciones

Las propiedades de una articulación se pueden leer usando [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) y definir usando [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- aumenta la velocidad del motor en 100 revoluciones por segundo
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Obtener la fuerza y el torque de reacción de una articulación

La fuerza y el torque de reacción aplicados a una articulación se pueden leer usando [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) y [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
