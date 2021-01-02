---
title: Physics in Defold
brief: Defold includes physics engines for 2D and 3D. They allow you to simulate Newtonian physics interactions between different types of collision objects.
---

# Physics

Defold includes a modified version of the [Box2D](http://www.box2d.org) physics engine (version 2.1) for 2D physics simulations and the Bullet physics engine (version 2.77) for 3D physics. It allows you to simulate Newtonian physics interactions between different types of _collision objects_. This manual explains how this works.

The main concepts of the physics engines used in Defold are:

* Collision objects - A collision object is a component you use to give a game object physical behaviour. A collision object has physical properties like weight, friction and shape. [Learn how to create a collision object](/manuals/physics-objects).
* Collision shapes - A collision object can either use several primitive shapes or a single complex shape to define its spatial extension. [Learn how to add shapes to a collision object](/manuals/physics-shapes).
* Collision groups - All collision objects must belong to a predefined group and each collision object can specify a list of other groups it can collide with. [Learn how to use collision groups](/manuals/physics-groups).
* Collision messages - When two collision objects collide the physics engine send messages to the game objects the components belong to. [Learn more about collision messages](/manuals/physics-messages)

In addition to the collision objects themselves you can also define collision object constraints, more commonly known as joints, to connect two collision objects and limit or in other ways apply force and influence how they behave in the physics simulation. [Learn more about joins](/manuals/physics-joints).

You can also probe and read the physics world along a linear ray know as ray casts. [Learn more about ray casts](/manuals/physics-ray-casts).


## Units used by the physics engine simulation

The physics engine simulates Newtonian physics and it is designed to work well with meters, kilograms and seconds (MKS) units. Furthermore, the physics engine is tuned to work well with moving objects of a size in the 0.1 to 10 meters range (static objects can be larger) and by default the engine treats 1 unit (pixel) as 1 meter. This conversion between pixels and meters is convenient on a simulation level, but from a game creation perspective it isn't very useful. With default settings a collision shape with a size of 200 pixels would be treated as having a size of 200 meters which is well outside of the recommended range, at least for a moving object. In general it is required that the physics simulation is scaled for it to work well with the typical size of objects in a game. The scale of the physics simulation can be changed in `game.project` via the [physics scale setting](/manuals/project-settings/#physics). Setting this value to for instance 0.02 would mean that 200 pixels would be treated as a 4 meters. Do note that the gravity (also changed in `game.project`) has to be increased to accommodate for the change in scale.


## Caveats and common issues

Collection proxies
: Through collection proxies it is possible to load more than one top level collection, or *game world* into the engine. When doing so it is important to know that each top level collection is a separate physical world. Physics interactions ([collisions, triggers](/manuals/physics-messages) and [ray-casts](/manuals/physics-ray-casts)) only happen between objects belonging to the same world. So even if the collision objects from two worlds visually sits right on top of each other, there cannot be any physics interaction between them.

Collisions not detected
: If you have problems with collisions not being handled or detected properly then make sure to read up on [physics debugging in the Debugging manual](/manuals/debugging/#debugging-problems-with-physics).
