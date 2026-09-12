---
title: Physikgelenke in Defold
brief: Defold unterstützt Gelenke für die 2D-Physik. Dieses Handbuch erklärt, wie du Gelenke erstellst und mit ihnen arbeitest.
---

# Gelenke {#joints}

Ein Gelenk (joint) verbindet zwei Kollisionsobjekte (collision objects) durch eine Zwangsbedingung (constraint). Defold unterstützt Gelenke sowohl in der 2D- als auch in der 3D-Physik über unterschiedliche APIs.

Dieses Handbuch beschreibt die 2D-Gelenke, die das Modul `physics` bereitstellt. Seit Defold 1.13.2 können 3D-Projekte über [`bullet3d.constraint`](/ref/beta/bullet3d.constraint/) Zwangsbedingungen erstellen und steuern, darunter Scharniere, Schieber und Federn. Verwende diese API mit starren Körpern (rigid bodies), die du über [`bullet3d.get_rigid_body()`](/ref/beta/bullet3d/#bullet3d.get_rigid_body) erhältst.

Die 2D-API `physics` unterstützt folgende Gelenktypen:

* **Festes Gelenk (Fixed, physics.JOINT_TYPE_FIXED)** - Ein Seilgelenk, das den maximalen Abstand zwischen zwei Punkten begrenzt. In Box2D wird es als Rope joint bezeichnet.
* **Scharniergelenk (Hinge, physics.JOINT_TYPE_HINGE)** - Ein Scharniergelenk legt einen Ankerpunkt an zwei Kollisionsobjekten fest und bewegt sie so, dass sich die beiden Kollisionsobjekte immer an derselben Stelle befinden. Die relative Drehung der Kollisionsobjekte ist dabei nicht eingeschränkt. Beim Scharniergelenk kann ein Motor mit einem festgelegten maximalen Motordrehmoment und einer festgelegten Drehzahl aktiviert werden. In Box2D wird es als [Drehgelenk (Revolute joint)](https://box2d.org/documentation/group__revolute__joint.html#details) bezeichnet.
* **Schweißgelenk (Weld, physics.JOINT_TYPE_WELD)** - Ein Schweißgelenk versucht, jede relative Bewegung zwischen zwei Kollisionsobjekten zu unterbinden. Das Schweißgelenk kann durch eine Frequenz und ein Dämpfungsverhältnis nachgiebig wie eine Feder eingestellt werden. In Box2D wird es als [Schweißgelenk (Weld joint)](https://box2d.org/documentation/group__weld__joint.html#details) bezeichnet.
* **Federgelenk (Spring, physics.JOINT_TYPE_SPRING)** - Ein Federgelenk hält zwei Kollisionsobjekte in einem konstanten Abstand zueinander. Das Federgelenk kann durch eine Frequenz und ein Dämpfungsverhältnis nachgiebig wie eine Feder eingestellt werden. In Box2D wird es als [Abstandsgelenk (Distance joint)](https://box2d.org/documentation/group__distance__joint.html#details) bezeichnet.
* **Schiebegelenk (Slider, physics.JOINT_TYPE_SLIDER)** - Ein Schiebegelenk ermöglicht die relative Verschiebung zweier Kollisionsobjekte entlang einer festgelegten Achse und verhindert ihre relative Drehung. In Box2D wird es als [prismatisches Gelenk (Prismatic joint)](https://box2d.org/documentation/group__prismatic__joint.html#details) bezeichnet.
* **Radgelenk (Wheel, physics.JOINT_TYPE_WHEEL)** - Ein Radgelenk beschränkt einen Punkt auf `bodyB` auf eine Linie auf `bodyA`. Das Radgelenk stellt außerdem eine Feder für die Aufhängung bereit. In Box2D wird es als  [Radgelenk (Wheel joint)](https://box2d.org/documentation/group__wheel__joint.html#details) bezeichnet.

## Gelenke erstellen {#creating-joints}

Die hier beschriebenen 2D-Gelenke werden per Code mit [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) erstellt:
::: sidenote
Die Unterstützung für das Erstellen von Gelenken im Editor ist geplant, ein Veröffentlichungsdatum steht jedoch noch nicht fest.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Das obige Beispiel erstellt ein festes Gelenk mit der ID `my_test_joint`, das die beiden Kollisionsobjekte `obj_a#collisionobject` und `obj_b#collisionobject` verbindet. Das Gelenk ist 10 Pixel rechts vom Mittelpunkt des Kollisionsobjekts `obj_a#collisionobject` und 20 Pixel oberhalb des Mittelpunkts des Kollisionsobjekts `obj_b#collisionobject` befestigt. Die maximale Länge des Gelenks beträgt 20 Pixel.

## Gelenke zerstören {#destroying-joints}

Du kannst ein Gelenk mit [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) zerstören:

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Gelenke auslesen und aktualisieren {#reading-from-and-updating-joints}

Du kannst die Eigenschaften eines Gelenks mit [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) auslesen und mit [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) setzen:

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

## Reaktionskraft und Drehmoment eines Gelenks auslesen {#get-joint-reaction-force-and-torque}

Du kannst die auf ein Gelenk wirkende Reaktionskraft und das Drehmoment mit [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) und [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id) auslesen.
