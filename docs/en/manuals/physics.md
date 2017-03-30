﻿---
title: Physics in Defold
brief: Defold includes physics engines for 2D and 3D. They allow you to simulate Newtonian physics interactions between different types of collision objects. This manual explains how this works.
---

# Physics

Defold includes a modified version of the [Box2D](http://www.box2d.org) physics engine for 2D physics simulations. It allows you to simulate Newtonian physics interactions between different types of _collision objects_. This manual explains how this works.

## Collision objects

A collision object is a component you use to extends a game object with physical behaviour. A collision object has different physical properties (like weight, restitution and friction) and its spatial extension is defined by one or more _shapes_ that you attach to the component. Defold supports the following types of collision object:

Static objects
: These do not react in themselves, but any other object that collides with static objects will react. These are very useful (and cheap performance-wise) for building level geometry (i.e. ground and walls) that does not move. You cannot move or otherwise change static objects.

Dynamic objects
: The physics engine solves all collisions for you and applies resulting forces. These are good for objects that should behave realistically, with the caveat that the only way you can manually control them is by applying forces to them.

Kinematic objects
: These types of objects will collide with other physics objects, but the job of resolving the collisions (or ignoring them) is yours. Kinematic objects are good when you need objects that collide and you want fine grained control over all reactions.

Triggers
: Triggers are objects that register simple collisions. These are good for game logic where you want some event to happen when some other object (i.e. the player character) reaches a specific spot.

## Editing collision objects

The editor allows you to easily attach a collision object to any game object:

![Physics collision object](images/physics/physics_collisionobject.png)

A collision object is constructed out of one or more physics shapes:

* Box shapes
* Sphere shapes
* Capsule shapes (does only work with 3D physics!)

You add these shapes and can use the ordinary editor transform tools to scale, rotate and position them. Each collision object has a number of properties:

![Physics properties](images/physics/physics_properties.png)

The *Collision Shape* property is used for tile map geometry that does not use ordinary primitive shapes. We’ll look at that below.

The *Type* property is used to set the type of collision object: `Dynamic`, `Kinematic`, `Static` or `Trigger`. If you set the object to `Dynamic` you _must_ set the *Mass* property to a non zero value. For dynamic or static objects you should also set the *Friction* and *Restitution* values.

::: important
If you set the type to `Dynamic` and forget to set the mass to non zero you will get a compilation error: `"ERROR:GAMESYS: Invalid mass 0.000000 for shape type 0"`
:::

## Friction

Friction makes it possible to make object slide realistically against each other. The friction value is usually set between `0` (no friction at all---a very slippery object) and `1` (strong friction---an abrasive object). However, any positive value is valid.

The friction strength is proportional to the normal force (this is called Coulomb friction). When the friction force is computed between two shapes (`A` and `B`), the friction values of both objects are combined by the geometric mean:

$$
F_{combined} = \sqrt{ F_A \times F_B }
$$

This means that if one of the objects has zero friction then the contact between them will have zero friction.

## Restitution

The restitution value sets the bounciness of the object. The value is usually between 0 (inelastic collision—the object does not bounce at all) and 1 (perfectly elastic collision—the object's velocity will be exactly reflected in the bounce)

Restitution values between two shapes (`A` and `B`) are combined using the following formula:

$$
R = \max{ \left( R_A, R_B \right) }
$$

::: sidenote
When a shape develops multiple contacts, restitution is simulated approximately because Box2D uses an iterative solver. Box2D also uses inelastic collisions when the collision velocity is small to prevent bounce-jitter
:::

## Linear and angular damping

Damping reduces the linear and angular velocities of the body. It is different from friction that only occurs with contact and can be used to give objects a floaty appearance, like they are moving through something thicker than air. Valid values for both linear and angular damping is between 0 and 1.

Box2D approximates damping for stability and performance. At small values, the damping effect is independent of the time step while at larger damping values, the damping effect varies with the time step. If you run your game with a fixed time step, this never becomes an issue.

## Locked rotation

Setting this property totally disables rotation on the collision object, no matter what forces are brought to it.

## Group and Mask

It is often desirable to be able to filter collision so that some types of objects collide with some other type, but not with a third kind. For instance, in a multiplayer shooter game you might want:

- Player characters that shoot bullet objects
- Bullet objects should collide with enemy objects
- Bullet objects should not collide with player characters
- Player characters should collide with enemy objects
- Player and enemies collide with the game world tiles

The physics engine allows you to group your physics objects and filter how they should collide. This is handled by named _collision groups_. For each collision object you create two properties control how the object collides with other objects:

Group
: The name of the collison group the object should belong to. You can have 16 different groups and you name them as you see fit for your application/game. For example "players", "bullets", "enemies" and "world".

Mask
: The other _groups_ this object should collide with. You can name one group or specify multiple groups in a comma separated list. If you leave the Mask field empty, the object will collide with nothing.


::: sidenote
Note that each collision involves two objects and it is important that both objects mutually specify each other's groups in their mask fields.
:::

![Collision groups and masks](images/physics/physics_group_mask.png)

To achieve the collision scheme outlined for the hypothetical shooter game above, the following setup would work:

Players
: *Group* = `players`, *Mask* =  `world, enemies`

Bullet
: *Group*: `bullets`, *Mask*: `enemies`

Enemies
: *Group*: `enemies`, *Mask*: `players, bullets`

World
: *Group*: `world`, *Mask*: `players, enemies`

## Tilesource collision shapes

The Defold editor has a tool that allows you to quickly generate physics shapes for a tilesource. In the tilesource editor, simply choose the image you wish to use as basis for collision. The editor will automatically generate a convex shape around each tile, taking into account pixels that are not 100% transparent:

![Physics tilesource](images/physics/physics_tilesource.png)

The editor draws the shapes in the color of the collision group you have assigned to the tile. You can have multiple collision groups per tilesource and the choice of group color is done automatically by the editor:

![Add collision group](images/physics/physics_add_collision_group.png)

To set a tile physics shape to a specific collision group, select the group and click the shape. To remove a tile shape from its collision group, select the "Tile source" root and click the tile.

To use the collision shapes from the Tile Source, create a collisionobject in the desired game object and select the Tile Source as its Collision Shape.

![Physics level example](images/physics/physics_level.png)

- Make sure the Tile Source you connected to the tile map has an image set for collisions. They should be rendered as lines on top of the texture in the Editor view.

- Make sure you have painted collision groups in the Tile Source for the tiles to support collision.

- Set the added Collision Object component's type to _Static_.

- Set the Group and Mask properties.

- Make sure that the Group and Mask properties of the Collision Objects you want colliding with the tiles.

## Collision messages

When two objects collide, the engine will broadcast messages to all components in both objects:

**`collision_response`**

This message is sent for all collision objects. It has the following fields set:

`other_id`
: the id of the instance the collision object collided with (`hash`)

`other_position`
: the world position of the instance the collision object collided with (`vector3`)

`group`
: the collision group of the other collision object (`hash`)

The collision_response message is only adequate to resolve collisions where you don't need any details on the actual intersection of the objects, for example if you want to detect if a bullet hits an enemy. There is only one of these messages sent for any colliding pair of objects each frame.

**`contact_point_response`**

This message is sent when one of the colliding objects is Dynamic or Kinematic. It has the following fields set:

`position`
: world position of the contact point (`vector3`).

`normal`
: normal in world space of the contact point, which points from the other object towards the current object (`vector3`).

`relative_velocity`
: the relative velocity of the collision object as observed from the other object (`vector3`).

`distance`
: the penetration distance between the objects -- non negative (`number`).

`applied_impulse`
: the impulse the contact resulted in (`number`).

`life_time`
: (*not currently used!*) life time of the contact (`number`).

`mass`
: the mass of the current collision object in kg (`number`).

`other_mass`
: the mass of the other collision object in kg (`number`).

`other_id`
: the id of the instance the collision object is in contact with (`hash`).

`other_position`
: the world position of the other collision object (`vector3`).

`group`
: the collision group of the other collision object (`hash`).

For a game or application where you need to separate objects perfectly, the `contact_point_response` message gives you all information you need. However, note that for any given collision pair, a number of `contact_point_response` message can be received each frame.

## Triggers

Triggers are light weight collision objects. In a trigger collision `collision_response` messages are sent. In addition, triggers also send a special `trigger_response` message when the collision begins and end. The message has the following fields:

`other_id`
: the id of the instance the collision object collided with (`hash`).

`enter`
: `true` if the interaction was an entry into the trigger, `false` if it was an exit. (`boolean`).


## Resolving Kinematic collisions

With Kinematic collision objects you have to resolve collisions yourself and move the objects apart from any penetration. A naive implementation of object separation looks like this:

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

This code will separate your Kinematic object from other physics object it penetrates, but the separation often overshoots and you will see jitter in many cases. To properly take a Kinematic object out of a collision we need to consider cases like the following:

![Physics collision](images/physics/physics_collision.png)

Here we will get two contact point messages, one for Object A and one for Object B. With the naive separation process above, the penetration vectors would just be added one after the other, resulting in the following separation:

![Physics separation naive](images/physics/physics_separate_naive.png)

Instead, we should iterate through the contact points and check if previous separations have already wholly or partially solved the separation we are about to make. In the collision example above we start by separation our character shape from Object A:

![Physics separation, step 1](images/physics/physics_separate_1.png)

We move our object along the normal of the Object A the distance of the penetration (the dotted red vector/arrow above). Now it is easy to see that the final movement we need to perform along the normal of Object B has already been partially covered by the first separation against Object A. We only need to separate along the filled green vector instead of the original one (dotted green).

It is straightforward to calculate the distance the previous movement out of Object B covered for us:

![Physics projection](images/physics/physics_projection.png)

The distance covered can be found if we project the penetration vector of Object A against the one of Object B. To find the final movement we need to perform we just subtract +l+ from our original penetration vector. For an arbitrary number of penetrations, we can accumulate the actual movements into a vector and project against each penetration vector in turn. The full implementation looks like this:

```lua
function on_message(self, message_id, message, sender)
    -- Handle collision
    if message_id == hash("contact_point_response") then
        -- Get the info needed to move out of collision. We might 
        -- get several contact points back and have to calculate
        -- how to move out of all accumulatively:
        if message.distance > 0 then
            -- First, project the penetration vector on 
            -- accumulated correction
            local proj = vmath.project(self.correction, message.normal * message.distance)
            if proj < 1 then
                -- Only care for projections that does not overshoot.
                local comp = (message.distance - message.distance * proj) * message.normal
                -- Apply compensation
                go.set_position(go.get_position() + comp)
                -- Accumulate the corrections done
                self.correction = self.correction + comp
            end
        end
    end
end
```

## Best practices

Triggers
: Trigger collision objects are sometimes too limited. Suppose you want a trigger that controls the intensity of a sound--the further the player moves into the trigger, the more intense the sound. This scenario requires a trigger that provides the penetration distance in the trigger. For this, a plain trigger collision object won’t do. Instead, you can set up a Kinematic object and never performing any separation of collisions but instead only registering them and use the collision data.

::: sidenote
Kinematic objects are more expensive than triggers, so use them wisely.
:::

Choosing between Dynamic or Kinematic objects
: If you are making a game with a player character (of some sort) that you maneuver through a level, it might seem like a good idea to create the player character as a Dynamic physics object and the world as a Static physics object. Player input is then handled by applying various forces on the player object.

  Going down that path is possible, but it is extremely hard to achieve great results. Your game controls will likely feel generic—like thousands of other games, since it is implemented the same way on the same physics engine. The problem boils down to the fact that the Box2D physics simulation is a realistic Newtonian simulation whereas a platformer is usually fundamentally different. You will therefore have to fight hard to make a Newtonian simulation behave in non-Newtonian fashion.

  One immediate problem is what should happen at edges. With a dynamic simulation running, the player physics object (here set up as a box) behaves like a realistic box and will tip over any edges.

  ![Dynamic physics](images/physics/physics_dynamic.png)

  This particular problem can be solved by setting the "Locked Rotation" property in the character's collision object. However, the example illustrates the core of the problem which is that the behavior of the character should be under the control of _you_, the designer/programmer and not being directly controlled by a physics simulation over which you have very limited control.

  So it is highly recommended that you implement your player character as a Kinematic physics object. Use the physics engine to detect collisions and deal with collisions and object separations as you need. Such an approach will initially require more work, but allows you to really design and fine-tune the player experience into something really good and unique.

(Some of the graphic assets used are made by Kenney: http://kenney.nl/assets)
