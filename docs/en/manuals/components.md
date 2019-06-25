---
title: Game object components
brief: This manual gives an overview of the components and how to use them.
---

#  Components

:[components](../shared/components.md)

## Component types

Defold supports the following component types:

* [Collection factory](/manuals/collection-factory) - Spawn collections
* [Collection proxy](/manuals/collection-proxy) - Load and unload collections
* [Collision object](/manuals/physics) - 2D and 3D physics
* [Camera](/manuals/camera) - Change the viewport and projection of the game world
* [Factory](/manuals/factory) - Spawn game objects
* [GUI](/manuals/gui) - Render a graphical user interface
* [Label](/manuals/label) - Render a piece of text
* [Model](/manuals/model) Show a 3D model (with optional animations)
* [Particle FX](/manuals/particlefx) -  Spawn particles
* [Script](/manuals/script) - Add game logic
* [Sound](/manuals/sound) - Play sound or music
* [Spine model](/manuals/spine-model) - Render a spine animation
* [Sprite](/manuals/sprite) - Show a 2D image (with optional flipbook animation)
* [Tilemap](/manuals/tilemap) - Show a grid of tiles

## Enabling and disabling components

The components of a game object are enabled when the game object is created. If you wish to disable a component this is done by sending a [**disable**](/ref/go/#disable) message to the component:

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

To enable a component again you can post an [**enable**](/ref/go/#enable) message to the component:

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```
