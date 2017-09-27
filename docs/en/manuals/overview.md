---
title: Editor overview
brief: This manual gives an overview on how the editor look and works, and how to navigate in it.
---

# Editor overview

The editor allows you to browse and manipulate all files in your game project in an efficient manner. Editing files brings up a suitable editor and shows all relevant information about the file in separate views.

:[overview](../shared/overview.md)

## The scene editor

Defold contains a number of editors, but the Scene Editor is the one used the most. All Game Objects and Collections, as well as some component types, are created and edited in this editor.

![Select object](images/scene_editing/scene_editing_select.png)

## Selecting objects

Click on objects in the main window to select them. The rectangle surrounding the object in the editor view will highlight green to indicate what item is selected.

You can also select objects by:

- <kbd>Click and drag</kbd> to select all objects inside the selection region.
- <kbd>Click</kbd> objects in the Outline view.

Hold <kbd>Shift</kbd> or <kbd>⌘</kbd> (Mac) or <kbd>Ctrl</kbd> while clicking to expand the selection.

## The Move tool

To move objects, use the *Move Tool*. It is accessible through the menu <kbd>Scene ▸ Move Tool</kbd> or by pressing the <kbd>W</kbd> key.

![Scene menu](images/scene_editing/scene_editing_scene.png)

The selected object now shows three manipulation points that are used to move the object. Click and drag in the green square to move the object freely:

![Move object](images/scene_editing/scene_editing_move.png)

You can also move the object along just one selected axis by clicking and dragging along the corresponding arrow. Clicking and dragging on the red arrow allows movement on the *X* axis only whereas clicking and dragging on the green arrow allows movement on the *Y* axis only.

Move against the grid
: Hold <kbd>Shift</kbd> when using the move tool to snap the center of the game object to the grid. The default grid size is set to 100. If you wish to alter the size of the grid, you can specify a custom grid size in the preferences. Select <kbd>Defold Editor ▸ Preferences...</kbd>

    ![Grid size](images/scene_editing/scene_editing_grid.png)

## Rotate Tool

The *Rotate Tool* is accessible through the menu <kbd>Scene ▸ Rotate Tool</kbd> or by pressing the <kbd>E</kbd> key.

![Rotate object](images/scene_editing/scene_editing_rotate.png)

This tool consists of three handles that you can manipulate. If you are working on 2D objects, you would probably only want to use the handle that rotates around the *Z* axis, which is the blue circle around the object. Click and drag on the circle to rotate the object.

If you want to rotate around the *X* or *Y* axis, click and drag on the green and red circles. Since the view is peripendicular to those axis, the circles only appear as two lines crossing the object: a green horizontal one and a red vertical.

## Scale Tool

The *Scale Tool* is accessed through the menu <kbd>Scene ▸ Scale Tool</kbd> or by pressing the <kbd>R</kbd> key.

![Scale object](images/scene_editing/scene_editing_scale.png)

Click the red or green handle and drag to scale the object. Game objects can be scaled freely along the *X* and *Y* axis, causing the object to stretch or compress visually.

::: sidenote
Currently, sprites can not be scaled in the editor. They do, however, support *runtime* free-form scaling. See the [2D Graphics documentation](/manuals/2dgraphics/) for details.
:::

## Selecting what is showing in the Scene Editor

It is often convenient to be able to disable the visual rendering of certain types of information in the Scene Editor, especially when you are working on a complicated collection with lots of objects containing physics, triggers and layers upon layers of graphical assets. The Scene Editor allows you to enable and disable the rendering of different types of information in the editor. Select the <kbd>Scene ▸ Show</kbd> submenu and then chose what you want to see in the editor.

![Showing information](images/scene_editing/scene_editing_show.png)

The choices you make are stored in the editor and apply to all Scene Editor instances. Your choices are rememberered between sessions too so if you close the Defold editor down and start it up the next day, your Show settings will be intact.

