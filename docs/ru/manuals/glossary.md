---
title: Defold glossary
brief: This manual lists everything that you encounter working in Defold with a brief description.
---

# Defold glossary

This glossary gives a brief description to all the things you encounter in Defold. In most cases, you will find a link to more in-depth documentation.

## Animation set

![Animation set](images/icons/animationset.png){.left} An animation set resource contains a list of .dae files or other .animationset files from where to read animations. Adding one .animationset files to another is handy if you share partial sets of animations between several models. See the [3D graphics manual](/manuals/graphics/) for details.

## Atlas

![Atlas](images/icons/atlas.png){.left} An atlas is a set of separate images that are compiled into a larger sheet for performance and memory reasons. They can contain still images or flip-book animated series of images. Atlases are used by GUI, Sprite, Spine model and ParticleFX components to share graphics resources. See the [Atlas documentation](/manuals/atlas) for more information.

## Builtins

![Builtins](images/icons/builtins.png){.left} The builtins project folder is a read-only folder containing useful default resources. Here you find the default renderer, render script, materials and more. If you need custom modifications on any of these resources, simply copy them into your project and edit as you see fit.

## Camera

![Camera](images/icons/camera.png){.left} The camera component helps to decide what part of the game world should be visible and how it should be projected. A common use case is to attach a camera to the player game object, or to have a separate game object with a camera that follows the player around with some smoothing algorithm. See the [Camera documentation](/manuals/camera) for more information.

## Collision object

![Collision object](images/icons/collision-object.png){.left} Collision objects are components that extend game objects with physical properties (like spatial shape, weight, friction and restitution). These properties govern how the collision object should collide with other collision objects. The most common types of collision objects are kinematic objects, dynamic objects and triggers. A kinematic object gives detailed collision information that you have to manually respond to, a dynamic object is automatically simulated by the physics engine to obey Newtonian laws of physics. Triggers are simple shapes that detect if other shapes have entered or exited the trigger. See the [Physics documentation](/manuals/physics) for details on how this works.

## Component

Components are used to give specific expression and/or functionality to game objects, like graphics, animation, coded behavior and sound. They don’t live a life of their own but have to be contained inside game objects. There are many kinds of components available in Defold. See [the Building blocks manual](/manuals/building-blocks) for a description of components.

## Collection

![Collection](images/icons/collection.png){.left} Collections are Defold’s mechanism for creating templates, or what in other engines are called "prefabs" in where hierarchies of game objects can be reused. Collections are tree structures that hold game objects and other collections. A collection is always stored on file and brought into the game either statically by placing it manually in the editor, or dynamically by spawning. See [the Building blocks manual](/manuals/building-blocks) for a description of collections.

## Collection factory

![Collection factory](images/icons/collection-factory.png){.left} A Collection factory component is used to spawn hierarchies of game objects dynamically into a running game. See the [Collection factory manual](/manuals/collection-factory) manual for details.

## Collection proxy

![Collection](images/icons/collection.png){.left} A Collection proxy is used to load and enable collections on the fly while an app or game is running. The most common use case for Collection proxies is to load levels as they are to be played. See the [Collection proxy documentation](/manuals/collection-proxy) for details.

## Cubemap

![Cubemap](images/icons/cubemap.png){.left} A cubemap is a special type of texture that consists of 6 different textures that are mapped on the sides of a cube. This is useful for rendering skyboxes and different kinds of reflection and illumination maps.

## Debugging

At some point your game will behave in an unexpected way and you need to figure out what is wrong. Learning how to debug is an art and fortunately Defold ships with a built-in debugger to help you out. See the [Debugging manual](/manuals/debugging) for more information.

## Display profiles

![Display profiles](images/icons/display-profiles.png){.left} The display profiles resource file is used for specifying GUI layouts depends on the orientation, aspect ratio or device model. It helps to adapt your UI for any kind of devices. Read more in the [Layouts manual](/manuals/gui-layouts).

## Factory

![Factory](images/icons/factory.png){.left} In some situations you cannot manually place all needed game objects in a collection, you have to create the game objects dynamically, on the fly. For instance, a player might fire bullets and each shot should be dynamically spawned and sent off whenever the player presses the trigger. To create game objects dynamically (from a pre-allocated pool of objects), you use a factory component. See the [Factory manual](/manuals/factory) for details.

## Font

![Font file](images/icons/font.png){.left} A Font resource is built from a TrueType or OpenType font file. The Font specifies which size to render the font in and what type of decoration (outline and shadow) the rendered font should have. Fonts are used by GUI and Label components. See the [Font manual](/manuals/font/) for details.

## Fragment shader

![Fragment shader](images/icons/fragment-shader.png){.left} This is a program that is run on the graphics processor for each pixel (fragment) in a polygon when it is drawn to the screen. The purpose of the fragment shader is to decide the color of each resulting fragment. This is done by calculation, texture lookups (one or several) or a combination of lookups and computations. See the [Shader manual](/manuals/shader) for more information.

## Gamepads

![Gamepads](images/icons/gamepad.png){.left} A gamepads resource file defines how specific gamepad device input is mapped to gamepad input triggers on a certain platform. See the [Input manual](/manuals/input) for details.

## Game object

![Game object](images/icons/game-object.png){.left} Game objects are simple objects that have a separate lifespan during the execution of your game. Game objects are containers and are usually equipped with visual or audible components, like a sound or a sprite. They can also be equipped with behavior through script components. You create game objects and place them in collections in the editor, or spawn them dynamically at run-time with factories. See [the Building blocks manual](/manuals/building-blocks) for a description of game objects.

## GUI

![GUI component](images/icons/gui.png){.left} A GUI component contains elements used to construct user interfaces: text and colored and/or textured blocks. Elements can be organized into hierarchical structures, scripted and animated. GUI components are typically used to create heads-up displays, menu systems and on-screen notifications. GUI components are controlled with GUI scripts that define the behavior of the GUI and control the user interaction with it. Read more in the [GUI documentation](/manuals/gui).

## GUI script

![GUI script](images/icons/script.png){.left} GUI scripts are used to control the behaviour of GUI components. They control GUI animations and how the user interacts with the GUI. See the [Lua in Defold manual](/manuals/lua) for details on how Lua scripts are used in Defold.

## Hot reload

The Defold editor allows you to update content in an already running game, on desktop and device. This feature is extremely powerful and can improve the development workflow a lot. See the [Hot reload manual](/manuals/hot-reload) for more information.

## Input binding

![Input binding](images/icons/input-binding.png){.left} Input binding files define how the game should interpret hardware input (mouse, keyboard, touchscreen and gamepad). The file binds hardware input to high level input _actions_ like "jump" and "move_forward". In script components that listen to input you are able to script the actions the game or app should take given certain input. See the [Input documentation](/manuals/input) for details.

## Label

![Label](images/icons/label.png){.left} The label component allows you to attach text content to any game object. It renders a piece of text with a particular font, on screen, in game space. See the [Label manual](/manuals/label) for more information.

## Library

![Game object](images/icons/builtins.png){.left} Defold allows you to share data between projects through a powerful library mechanism. You can use it to set up shared libraries that are accessible from all your projects, either for yourself or across the whole team. Read more about the library mechanism in the [Libraries documentation](/manuals/libraries).

## Lua language

The Lua programming language is used in Defold to create game logic. Lua is a powerful, efficient, very small scripting language. It supports procedural programming, object-oriented programming, functional programming, data-driven programming, and data description. You can read more about the language on the official Lua homepage at https://www.lua.org/ and in the [Lua in Defold manual](/manuals/lua).

## Lua module

![Lua module](images/icons/lua-module.png){.left} Lua modules allow you to structure your project and create reusable library code. Read more about it in the [Lua modules manual](/manuals/modules/)

## Material

![Material](images/icons/material.png){.left} Materials define how different objects should be rendered by specifying shaders and their properties. See the [Material manual](/manuals/material) for more information.

## Message

Components communicate with each other and other systems through message passing. Components also respond to a set of predefined messages that alter them or trigger specific actions. You send messages to hide graphics or nudge physics objects. The engine also uses messages to notify components of events, for instance when physics shapes collide. The message passing mechanism needs a recipient for each sent message. Therefore, everything in the game is uniquely addressed. To allow communication between objects, Defold extends Lua with message passing. Defold also provides a library of useful functions.

For instance, the Lua-code required to hide a sprite component on a game object looks like this:

```lua
msg.post("#weapon", "disable")
```

Here, `"#weapon"` is the address of the current object's sprite component. `"disable"` is a message that sprite components respond to. See the [Message passing documentation](/manuals/message-passing) for an in depth explanation of how message passing works.

## Model

![Model](images/icons/model.png){.left} With the 3D model component can import Collada mesh, skeleton and animation assets into your game. See the [Model manual](/manuals/model/) for more information.

## ParticleFX

![ParticleFX](images/icons/particlefx.png){.left} Particles are very useful for creating nice visual effects, particularly in games. you can use them to create fog, smoke, fire, rain or falling leaves. Defold contains a powerful particle effects editor that allows you to build and tweak effects while you run them real time in your game. The [ParticleFX documentation](/manuals/particlefx) gives you the details on how that works.

## Profiling

Good performance is key in games and it is vital that you are able to do performance and memory profiling to measure your game and identify performance bottlenecks and memory problems that needs to be fixed. See the [Profiling manual](/manuals/profiling) for more information on the profiling tools available for Defold.

## Render

![Render](images/icons/render.png){.left} Render files contain settings used when rendering the game to the screen. Render files define which Render script to use for rendering and which materials to use. See the [Render manual](/manuals/render/) for more details.

## Render script

![Render script](images/icons/script.png){.left} A Render script is a Lua script that controls how the game or app should be rendered to the screen. There is a default Render script that covers most common cases, but you can write your own if you need custom lighting models and other effects. See the [Render manual](/manuals/render/) for more details on how the render pipeline works, and the [Lua in Defold manual](/manuals/lua) for details on how Lua scripts are used in Defold.

## Script

![Script](images/icons/script.png){.left}  A script is a component that contains a program that defines game object behaviors. With scripts you can specify the rules of your game, how objects should respond to various interactions (with the player as well as other objects). All scripts are written in the Lua programming language. To be able to work with Defold, you or someone on your team needs to learn how to program in Lua. See the [Lua in Defold manual](/manuals/lua) for an overview on Lua and details on how Lua scripts are used in Defold.

## Sound

![Sound](images/icons/sound.png){.left} The sound component is responsible for playing a specific sound. Currently, Defold supports sound files in the WAV and Ogg Vorbis formats. See the [Sound manual](/manuals/sound) for more information.

## Spine model

![Spine model](images/icons/spine-model.png){.left} The Spine model component is used to bring Spine skeletal animations to life in Defold. Read more about how to use it in the [Spine model manual](/manuals/spinemodel).

## Spine scene

![Spine scene](images/icons/spine-scene.png){.left} The Spine scene resource ties together the Spine JSON data file and the Defold image atlas file that is used to fill bone slots with graphics. The [Spine animation manual](/manuals/spine) contains more information.

## Sprite

![Sprite](images/icons/sprite.png){.left} A sprite is a component that extends game objects with graphics. It displays an image either from a Tile source or from an Atlas. Sprites have built-in support for flip-book and bone animation. Sprites are usually used for characters and items.

## Texture profiles

![Texture profiles](images/icons/texture-profiles.png){.left} The texture profiles resource file is used in the bundling process to automatically process and compress image data (in Atlas, Tile sources, Cubemaps and stand-alone textures used for models, GUI etc). Read more in the [Texture profiles manual](/manuals/texture-profiles).

## Tile map

![Tile map](images/icons/tilemap.png){.left} Tile map components display images from a tile source in one or more overlaid grids. They are most commonly used to build game environments: ground, walls, buildings and obstacles. A tile map can display several layers aligned on top of each other with a specified blend mode. This is useful to, for example, put foliage on top of grass background tiles. It is also possible to dynamically change the displayed image in a tile. That allows you to, for instance, destroy a bridge and make it impassable by simply replacing the tiles with ones depicting the broken down bridge and containing the corresponding physics shape. See the [Tile map documentation](/manuals/tilemap) for more information.

## Tile source

![Tile source](images/icons/tilesource.png){.left} A tile source describes a texture that is composed of multiple smaller images, each with the same size. You can define flip-book animations from a sequence of images in a tile source. Tile sources can also automatically calculate collision shapes from image data. This is very useful for creating tiled levels that object can collide and interact with. Tile sources are used by Tile map components (and Sprite and ParticleFX) to share graphics resources. Note that Atlases are often a better fit than tile sources. See the [Tile map documentation](/manuals/tilemap) for more information.

## Vertex shader

![Vertex shader](images/icons/vertex-shader.png){.left} The vertex shader computes the screen geometry of a component's primitive polygon shapes. For any type of visual component, be it a sprite, spine model or model, the shape is represented by a set of polygon vertex positions. The vertex shader program processes each vertex (in world space) and computes the resulting coordinate that each vertex of a primitive should have. See the [Shader manual](/manuals/shader) for more information.
