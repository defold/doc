---
title: Importing and editing assets
brief: This manual covers how to import and edit assets.
---

# Importing and editing assets

A game project usually consists of a large number of external assets that are produced in various specialized programs for producing graphics, 3D models, sound files, animations and so forth. Defold is built for a workflow where you work in your external tools and then import the assets into Defold as they are finalized.


## Importing assets

Defold needs all the assets used in your project to be located somewhere in the project hierarchy. You therefore need to import all assets before you can use them. To import assets, simply drag the files from the file system on your computer and drop them in an appropriate place in the Defold editor *Assets pane*.

![Importing files](images/graphics/import.png){srcset="images/graphics/import@2x.png 2x"}

::: sidenote
Defold supports images in the PNG and JPEG image formats. Other image formats need to be converted before they can be used.
:::


## Using assets

When the assets are imported into Defold they can be used by the various component types supported by Defold:

* Images can be used to create many kinds of visual components frequently used in 2D games. Read more about [how to import and use 2D graphics here](/manuals/importing-graphics).
* Sounds can be used by the [Sound component](/manuals/sound) to play sounds.
* Spine animation data is used by the [Spine component](/manuals/spinemodel) to show and animate Spine models.
* Fonts are used by the [Label component](/manuals/label) and by [text nodes](/manuals/gui-text) in a GUI.
* Collada models can be used by the [Model component](/manuals/model) to show 3D models with animations. Read more about [how to import and use 3D models here](/manuals/importing-models).


## Editing external assets

Defold does not provide editing tools for images, sound files, models or animations. Such assets need to be created outside of Defold in specialized tools and imported into Defold. Defold automatically detects changes to any asset among your project files and updates the editor view accordingly.


## Editing Defold assets

The editor saves all Defold assets in text based files that are merge friendly. They are also easy to create and modify with simple scripts. See [this forum thread](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) for more information. Note though that we do not publish our file format details since they do change once in a while. You can also use [Editor Scripts](/manuals/editor-scripts/) to hook into certain life-cycle events in the Editor to run scripts to generate or modify assets.

Extra care should be taken when working with Defold asset files through a text editor or external tool. If you introduce errors those can prevent the file from opening in the Defold editor.

Some external tools [such as Tiled](/assets/tiled/) can be used to generate Defold Assets automatically.
