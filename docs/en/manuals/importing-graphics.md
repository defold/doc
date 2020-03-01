---
title: Importing and using 2D graphics
brief: This manual covers how to import and use 2D graphics.
---

# Importing 2D graphics

Defold supports many kinds of visual components frequently used in 2D games. Use can use Defold to create static and animated sprites, UI components, particle effects, tile maps, bitmap fonts and Spine animations. Before you can create any of these visual components you need to import image files with the graphics that you wish to use. To import image files you simply drag the files from the file system on your computer and drop them in an appropriate place in the Defold editor *Assets pane*.

![Importing files](images/graphics/import.png){srcset="images/graphics/import@2x.png 2x"}

::: sidenote
Defold supports images in the PNG and JPEG image formats. Other image formats need to be converted before they can be used.
:::


## Creating Defold assets

When the images are imported into Defold they can be used to create Defold specific assets:

![atlas](images/icons/atlas.png){.icon} Atlas
: An atlas contains a list of separate images files, which are automatically combined into a larger texture image. Atlases can contain still images and *Animation Groups*, sets of images that together form a flipbook animation.

  ![atlas](images/graphics/atlas.png){srcset="images/graphics/atlas@2x.png 2x"}

Learn more about the atlas resource in the [Atlas manual](/manuals/atlas).

![tile source](images/icons/tilesource.png){.icon} Tile Source
: A tile source references an image file that is already made out to consist of smaller sub-images ordered on a uniform grid. Another term commonly used for this type of compound image is _sprite sheet_. Tile sources can contain flipbook animations, defined by the first and last tile for the animation. It is also possible to use an image to automatically attach collision shapes to tiles.

  ![tile source](images/graphics/tilesource.png){srcset="images/graphics/tilesource@2x.png 2x"}

Learn more about the tile source resource in the [Tile source manual](/manuals/tilesource).

![bitmap font](images/icons/font.png){.icon} Bitmap Font
: A bitmap font has its glyphs in a PNG font sheet. These types of fonts provide no performance improvement from fonts generated from TrueType or OpenType font files, but can include arbitrary graphics, coloring and shadows right in the image.

Learn more about bitmap fonts in the [Fonts manual](/manuals/font/#bitmap-bmfonts).

  ![BMfont](images/font/bm_font.png){srcset="images/font/bm_font@2x.png 2x"}


## Using Defold assets

When you have converted the images into Atlas and Tile Source files you can use these to create several different kinds of visual components:

![sprite](images/icons/sprite.png){.icon}
: A sprite is either a static image or flipbook animation that is displayed on screen.

  ![sprite](images/graphics/sprite.png){srcset="images/graphics/sprite@2x.png 2x"}

Learn more about sprites in the [Sprite manual](/manuals/sprite).

![tile map](images/icons/tilemap.png){.icon} Tile map
: A tilemap component pieces together a map from tiles (image and collision shapes) that come from a tile source. Tile maps cannot use atlas sources.

  ![tilemap](images/graphics/tilemap.png){srcset="images/graphics/tilemap@2x.png 2x"}

Learn more about tilemaps in the [Tilemap manual](/manuals/tilemap).

![particle effect](images/icons/particlefx.png){.icon} Particle fx
: Particles that are spawned from a particle emitter consist of a still image or a flipbook animation from an atlas or tile source.

  ![particles](images/graphics/particles.png){srcset="images/graphics/particles@2x.png 2x"}

Learn more about particle effects in the [Particle fx manual](/manuals/particlefx).

![gui](images/icons/gui.png){.icon} GUI
: GUI box nodes and pie nodes can use still images and flipbook animations from atlases and tile sources.

  ![gui](images/graphics/gui.png){srcset="images/graphics/gui@2x.png 2x"}

Learn more about GUIs in the [GUI manual](/manuals/gui).

![spine](images/icons/spine-model.png){.icon} Spine model
: Spine models gets their data from Spine scene resources. Those contain two pieces of data:

  1. A Spine Json file that describes the bone animations.
  2. An atlas that contain the images that are attached to the bones. Spine models cannot use data from tile maps.

  ![spine](images/graphics/spine.png){srcset="images/graphics/spine@2x.png 2x"}

Learn more about Spine models in the [Spine model manual](/manuals/spinemodel).
