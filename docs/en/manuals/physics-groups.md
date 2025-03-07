---
title: Collision groups in Defold
brief: The physics engine allows you to group your physics objects and filter how they should collide.
---

# Group and mask

The physics engine allows you to group your physics objects and filter how they should collide. This is handled by named _collision groups_. For each collision object you create two properties control how the object collides with other objects, *Group* and *Mask*.

For a collision between two objects to register both objects must mutually specify each other's groups in their *Mask* field.

![Physics collision group](images/physics/collision_group.png)

The *Mask* field can contain multiple group names, allowing for complex interaction scenarios.

## Detecting collisions
When two collision objects with matching groups and masks collide the physics engine will generate [collision messages](/manuals/physics-messages) that can be used in games to react to collisions.
