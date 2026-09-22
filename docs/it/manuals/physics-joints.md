---
title: Giunti fisici in Defold
brief: Defold supporta i giunti per la fisica 2D. Questo manuale spiega come creare e utilizzare i giunti.
---

# Giunti {#joints}

Un giunto (joint) collega due oggetti di collisione applicando un vincolo. Defold supporta giunti sia nella fisica 2D sia in quella 3D, attraverso API diverse.

Questo manuale descrive i giunti 2D esposti dal modulo `physics`. Da Defold 1.13.2, i progetti 3D possono creare e controllare vincoli tramite [`bullet3d.constraint`](/ref/beta/bullet3d.constraint/), tra cui cerniere, cursori e molle. Usa questa API con i corpi rigidi ottenuti tramite [`bullet3d.get_rigid_body()`](/ref/beta/bullet3d/#bullet3d.get_rigid_body).

I tipi di giunto supportati dall'API 2D `physics` sono:

* **Fisso (physics.JOINT_TYPE_FIXED)** - Un giunto a fune che limita la distanza massima tra due punti. In Box2D è chiamato Rope joint.
* **A cerniera (physics.JOINT_TYPE_HINGE)** - Un giunto a cerniera definisce un punto di ancoraggio su due oggetti di collisione e li sposta in modo che i due oggetti di collisione si trovino sempre nella stessa posizione, senza limitarne la rotazione relativa. Il giunto a cerniera può attivare un motore con coppia massima e velocità definite. In Box2D è chiamato [giunto rotoidale (Revolute joint)](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Saldato (physics.JOINT_TYPE_WELD)** - Un giunto saldato cerca di vincolare tutti i movimenti relativi tra due oggetti di collisione. Puoi rendere il giunto saldato elastico come una molla, definendo una frequenza e un rapporto di smorzamento. In Box2D è chiamato [giunto saldato (Weld joint)](https://box2d.org/documentation/group__weld__joint.html#details).
* **A molla (physics.JOINT_TYPE_SPRING)** - Un giunto a molla mantiene due oggetti di collisione a una distanza costante l'uno dall'altro. Puoi rendere il giunto a molla elastico, definendo una frequenza e un rapporto di smorzamento. In Box2D è chiamato [giunto di distanza (Distance joint)](https://box2d.org/documentation/group__distance__joint.html#details).
* **A scorrimento (physics.JOINT_TYPE_SLIDER)** - Un giunto a scorrimento consente la traslazione relativa di due oggetti di collisione lungo un asse specificato e ne impedisce la rotazione relativa. In Box2D è chiamato [giunto prismatico (Prismatic joint)](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **A ruota (physics.JOINT_TYPE_WHEEL)** - Un giunto a ruota vincola un punto su `bodyB` a una retta su `bodyA`. Il giunto a ruota fornisce anche una molla di sospensione. In Box2D è chiamato [giunto a ruota (Wheel joint)](https://box2d.org/documentation/group__wheel__joint.html#details).

## Creazione dei giunti {#creating-joints}

I giunti 2D descritti qui vengono creati tramite codice usando [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
È previsto il supporto alla creazione dei giunti nell'editor, ma non è ancora stata stabilita una data di rilascio.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Il codice precedente crea un giunto fisso con ID `my_test_joint` che collega i due oggetti di collisione `obj_a#collisionobject` e `obj_b#collisionobject`. Il giunto è collegato 10 pixel a destra del centro dell'oggetto di collisione `obj_a#collisionobject` e 20 pixel sopra il centro dell'oggetto di collisione `obj_b#collisionobject`. La lunghezza massima del giunto è di 20 pixel.

## Distruzione dei giunti {#destroying-joints}

Puoi distruggere un giunto utilizzando [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Lettura e aggiornamento dei giunti {#reading-from-and-updating-joints}

Puoi leggere le proprietà di un giunto utilizzando [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) e impostarle utilizzando [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

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

## Lettura della forza e della coppia di reazione del giunto {#get-joint-reaction-force-and-torque}

Puoi leggere la forza e la coppia di reazione applicate a un giunto utilizzando [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) e [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
