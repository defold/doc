---
title: Defold 3D graphics manual
brief: This manual outlines the 3D support in Defold.
---

# 3D graphics

Defold is at its core a 3D engine. Even when you work with 2D material only all rendering is done in 3D, but orthographically projected onto the screen.

Defold allows you to utilize full 3D content by including 3D assets, or _Models_ into your collections. You can build games in strictly 3D with only 3D assets, or you can mix 3D and 2D content as you wish.

## Defold resources

*Model*
: The model component contains the object mesh, its skeleton and animations. Like all visual components it also has a material tied to it.

*Animation Set*
: The animation set file contains a list of *.dae* files from where to read animations. You can also add other *.animationset* files to an animation set, which is handy if you share partial sets of animations between several models.


The [Model documentation](/manuals/model) explains how to import 3D assets and create models.

The [Animation documentation](/manuals/animation) explains how to animate 3D models.

## Collada support

Defold's 3D support requires you to save or export model, skeleton and animation data in the _Collada_ format. This is a widely adopted format that most 3D modelling software supports. So you should be able to create assets in in _Maya_, _3D Max_, _Blender_, _Sketchup_ or any other popular software and then bring the results into Defold.

::: important
Defold currently supports only baked animations. Animations need to have matrices for each animated bone each keyframe, and not position, rotation and scale as separate keys.

Animations are also linearly interpolated. If you do more advanced curve interpolation the animations needs to be prebaked from the exporter.

Animation clips in Collada are not supported. To use multiple animations per model, export them into separate *.dae* files and gather the files into an *.animationset* file in Defold.
:::

## Materials, shaders and textures

3D software commonly allows you to set properties on your object vertices, like coloring and texturing. This information goes into the Collada *.dae* file that you export from your 3D software. Depending on the requirements of your game you will have to select and/or create appropriate and _performant_ materials for your objects. A material combines _shader programs_ with a set of parameters for rendering of the object.

You will also need to design and implement a game camera that works with your intended gameplay.

Your Defold project has some built-in materials that are used to render sprites, tiles, particles and GUI nodes. For 3D models, there is no suitable built-in material so we have to create one. For the example book model there is a "textured.material" resource ready-made.

Read the [Material documentation](/manuals/material) for information on how materials work and how you can create materials that work with textured 3D models.

The [Shader manual](/manuals/shader) contains information on how shader programs work.

## Rendering

The last thing to do to get the model into the game is to alter the *Render Script* for the project. The default render script is tailor made for 2D games and does not work with 3D models. But by copying the default render script and adding a handful of lines of Lua code we can make sure that our book is rendered as expected. For the example the render script is already set up.

Read the [Rendering documentation](/manuals/rendering) for details on how render scripts work.


