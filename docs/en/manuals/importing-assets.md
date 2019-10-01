---
title: Importing and editing assets
brief: This manual covers how to import and edit assets in Defold using external editors.
---

# Importing and editing assets

A game project usually consists of a large number of external assets that are produced in various specialized programs for producing graphics, 3D models, sound files, animations and so forth. Defold is built for a workflow where you work in your external tools and then import the assets into Defold as they are finalized. When the assets are imported into Defold they can be used by the various component types to create flipbook animations, tilemaps, particle effects and many other things:

* Images can be used to create texture [atlases](/manuals/atlas) and tile sources which in turn can be used by visual components such as [sprites](/manuals/sprite), [tilemaps](/manuals/tilemap) and [particle effects](/manuals/particlefx). Read more about this in the [Graphics manual](/manuals/graphics/#importing-image-files).
* Sounds can be used by the [Sound component](/manuals/sound) to play sounds.
* Spine animation data is used by the [Spine component](/manuals/spinemodel) to show and animate Spine models.
* Fonts are used by the [Label component](/manuals/label) and by [text nodes](/manuals/gui-text) in a GUI.
* Collada models can be used by the [Model component](/manuals/model) to show 3D models with animations.


## External editors and tools

Defold does not provide editing tools for creating images, sound files, models or animations. Such assets need to be created outside of Defold in specialized tools and imported into Defold. Defold automatically detects changes to any asset in the project hierarchy and updates the editor view accordingly.

There is currently no way to hook custom build steps into the in-editor builder, but we provide a stand-alone build pipeline (see [Bob the builder](/manuals/bob)) that can be incorporated in any pipeline.

The editor saves all Defold assets in text based files that are merge friendly. They are also easy to create and modify with simple scripts. See [this forum thread](https://forum.defold.com/t/deftree-a-python-module-for-editing-defold-files/15210) for more information. Note though that we do not publish our file format details since they do change once in a while.

Extra care should be taken when working with Defold asset files through a text editor or external tool. If you introduce errors those can prevent the file from opening in the Defold editor.
