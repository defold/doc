---
title: Collision objects in Defold
brief: A collision object is a component you use to give a game object physical behaviour. A collision object has physical properties and a spatial shape.
---

# Collision objects

A collision object is a component you use to give a game object physical behaviour. A collision object has physical properties like weight, restitution and friction and its spatial extension is defined by one or more _shapes_ that you attach to the component. Defold supports the following types of collision objects:

Static objects
: Static objects never move but a dynamic object that collides with a static object will react by bouncing and/or sliding. Static objects are very useful for building level geometry (i.e. ground and walls) that does not move. They are also cheaper performance-wise than dynamic objects. You cannot move or otherwise change static objects.

Dynamic objects
: Dynamic objects are simulated by the physics engine. The engine solves all collisions and applies resulting forces. Dynamic objects are good for objects that should behave realistically. The most common way to affect them is indirectly, by [applying forces](/ref/physics/#apply_force) or changing the angular [damping](/ref/stable/physics/#angular_damping) and [velocity](/ref/stable/physics/#linear_velocity) and the linear [damping](/ref/stable/physics/#linear_damping) and [velocity](/ref/stable/physics/#angular_velocity). It is also possible to directly manipulate the position and orientation of a dynamic object when the [Allow Dynamic Transforms setting](/manuals/project-settings/#allow-dynamic-transforms) is enabled in *game.project*.

Kinematic objects
: Kinematic objects register collisions with other physics objects, but the physics engine do not perform any automatic simulation. The job of resolving collisions, or ignoring them, is left to you ([learn more](/manuals/physics-resolving-collisions)). Kinematic objects are very good for player or script controlled objects that require fine grained control of the physical reactions, like a player character.

Triggers
: Triggers are objects that register simple collisions. Triggers are light weight collision objects. They are similar to [ray casts](/manuals/physics-ray-casts) in that they read the physics world as opposed to interacting with it. They are good for objects that just need to register a hit (like a bullet) or as part of game logic where you want to trigger certain actions when an object reaches a specific point. Trigger are computationally cheaper than kinematic objects and should be used in favor of those if possible.


## Adding a collision object component

A collision object component has a set of *Properties* that sets its type and physics properties. It also contains one or more *Shapes* that define the whole shape of the physics object.

To add a collision object component to a game object:

1. In the *Outline* view, <kbd>right click</kbd> the game object and select <kbd>Add Component ▸ Collision Object</kbd> from the context menu. This creates a new component with no shapes.
2. <kbd>Right click</kbd> the new component and select <kbd>Add Shape ▸ Box / Capsule / Sphere</kbd>. This adds a new shape to the collision object component. You can add any number of shapes to the component. You can also use a tilemap or a convex hull to define the shape of the physics object.
3. Use the move, rotate and scale tools to edit the shapes.
4. Select the component in the *Outline* and edit the collision object's *Properties*.

![Physics collision object](images/physics/collision_object.png){srcset="images/physics/collision_object@2x.png 2x"}


## Adding a collision shape

A collision component can either use several primitive shapes or a single complex shape. Learn more about the various shapes and how to add them to a collision component in the [Collision Shapes manual](/manuals/physics-shapes).


## Collision object properties

Id
: The identity of the component.

Collision Shape
: This property is used for tile map geometry or convex shapes that does not use primitive shapes. See [Collision Shapes for more information](/manuals/physics-shapes).

Type
: The type of collision object: `Dynamic`, `Kinematic`, `Static` or `Trigger`. If you set the object to dynamic you _must_ set the *Mass* property to a non zero value. For dynamic or static objects you should also check that the *Friction* and *Restitution* values are good for your use-case.

Friction
: Friction makes it possible for objects to slide realistically against each other. The friction value is usually set between `0` (no friction at all---a very slippery object) and `1` (strong friction---an abrasive object). However, any positive value is valid.

  The friction strength is proportional to the normal force (this is called Coulomb friction). When the friction force is computed between two shapes (`A` and `B`), the friction values of both objects are combined by the geometric mean:

  $$
  F = sqrt( F_A * F_B )
  $$

  This means that if one of the objects has zero friction then the contact between them will have zero friction.

Restitution
: The restitution value sets the "bounciness" of the object. The value is usually between 0 (inelastic collision—the object does not bounce at all) and 1 (perfectly elastic collision---the object's velocity will be exactly reflected in the bounce)

  Restitution values between two shapes (`A` and `B`) are combined using the following formula:

  $$
  R = max( R_A, R_B )
  $$

  When a shape develops multiple contacts, restitution is simulated approximately because Box2D uses an iterative solver. Box2D also uses inelastic collisions when the collision velocity is small to prevent bounce-jitter

Linear damping
: Linear damping reduces the linear velocity of the body. It is different from friction, which only occurs during contact, and can be used to give objects a floaty appearance, like they are moving through something thicker than air. Valid values are between 0 and 1.

  Box2D approximates damping for stability and performance. At small values, the damping effect is independent of the time step while at larger damping values, the damping effect varies with the time step. If you run your game with a fixed time step, this never becomes an issue.

Angular damping
: Angular damping works like linear damping but reduces the angular velocity of the body. Valid values are between 0 and 1.

Locked rotation
: Setting this property totally disables rotation on the collision object, no matter what forces are brought to it.

Bullet
: Setting this property enables continuous collision detection (CCD) between the collision object and other dynamic collision objects. The Bullet property is ignored if the Type is not set to `Dynamic`.

Group
: The name of the collision group the object should belong to. You can have 16 different groups and you name them as you see fit for your game. For example "players", "bullets", "enemies" and "world". If the *Collision Shape* is set to a tile map, this field is not used but the groups names are taken from the tile source. [Learn more about collision groups](/manuals/physics-groups).

Mask
: The other _groups_ this object should collide with. You can name one group or specify multiple groups in a comma separated list. If you leave the Mask field empty, the object will not collide with anything. [Learn more about collision groups](/manuals/physics-groups).


## Runtime properties

A physics object has a number of different properties that can be read and changed using `go.get()` and `go.set()`:

`angular_damping`
: The angular damping value for the collision object component (`number`). [API reference](/ref/physics/#angular_damping).

`angular_velocity`
: The current angular velocity of the collision object component (`vector3`). [API reference](/ref/physics/#angular_velocity).

`linear_damping`
: The linear damping value for the collision object (`number`). [API reference](/ref/physics/#linear_damping).

`linear_velocity`
: The current linear velocity of the collision object component (`vector3`). [API reference](/ref/physics/#linear_velocity).

`mass`
: The defined physical mass of the collision object component. READ ONLY. (`number`). [API reference](/ref/physics/#mass).
