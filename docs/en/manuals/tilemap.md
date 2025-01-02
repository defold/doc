---
title: Defold tile map manual
brief: This manual details Defold's support for tile maps.
---

# Tile map

A *Tile Map* is a component that allows you to assemble, or paint, tiles from a *Tile Source* onto a large grid area. Tile maps are commonly used to build game level environments. You can also use the *Collision Shapes* from the tile source in your maps for collision detection and physics simulation ([example](/examples/tilemap/collisions/)).

Before you can create a tile map you need to create a Tile Source. Refer to the [Tile Source manual](/manuals/tilesource) to learn how to create a Tile Source.

## Creating a tile map

To create a new tile map:

- <kbd>Right click</kbd> a location in the *Assets* browser, then select <kbd>New... ▸ Tile Map</kbd>).
- Name the file.
- The new tile map automatically opens in the tile map editor.

  ![new tilemap](images/tilemap/tilemap.png){srcset="images/tilemap/tilemap@2x.png 2x"}

- Set the *Tile Source* property to a tile source file that you have prepared.

To paint tiles on your tile map:

1. Select or create a *Layer* to paint on in the *Outline* view.
2. Select a tile to use as a brush (press <kbd>Space</kbd> to show the tile palette) or select a few tiles by clicking and dragging in the palette to create a rectangle brush with multiple tiles.

   ![Palette](images/tilemap/palette.png){srcset="images/tilemap/palette@2x.png 2x"}

3. Paint with the selected brush. To erase a tile, either pick an empty tile and use it as brush, or select the eraser (<kbd>Edit ▸ Select Eraser</kbd>).

   ![Painting tiles](images/tilemap/paint_tiles.png){srcset="images/tilemap/paint_tiles@2x.png 2x"}

You can pick tiles directly from a layer and use the selection as a brush. Hold <kbd>Shift</kbd> and click a tile to pick it up as the current brush. While holding <kbd>Shift</kbd> you can also click and drag to select a block of tiles to use as a larger brush. Also, it is possible to cut tiles in a similar way by holding <kbd>Shift+Ctrl</kbd> or erase them by holding <kbd>Shift+Alt</kbd>.

For clockwise brush rotation, use <kbd>Z</kbd>. Use <kbd>X</kbd> for horizontal flipping and <kbd>Y</kbd> for vertical flipping of the brush.

![Picking tiles](images/tilemap/pick_tiles.png){srcset="images/tilemap/pick_tiles@2x.png 2x"}

## Adding a tile map to your game

To add a tile map to your game:

1. Create a game object to hold the tile map component. The game object can be in a file or created directly in a collection.
2. Right-click the root of the game object and select <kbd>Add Component File</kbd>.
3. Select the tile map file.

![Use tile map](images/tilemap/use_tilemap.png){srcset="images/tilemap/use_tilemap@2x.png 2x"}

## Runtime manipulation

You can manipulate tilemaps in runtime through a number of different functions and properties (refer to the [API docs for usage](/ref/tilemap/)).

### Changing tiles from script

You can read and write the content of a tile map dynamically while your game is running. To do so, use the [`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) and [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) functions:

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## Tilemap properties

Apart from the properties *Id*, *Position*, *Rotation* and *Scale* the following component specific properties exist:

*Tile Source*
: The tilesource resource to use for the tilemap.

*Material*
: The material to use for rendering the tilemap.

*Blend Mode*
: The blend mode to use when rendering the tilemap.

### Blend modes
:[blend-modes](../shared/blend-modes.md)

### Changing properties

A tilemap has a number of different properties that can be manipulated using `go.get()` and `go.set()`:

`tile_source`
: The tile map tile source (`hash`). You can change this using a tile source resource property and `go.set()`. Refer to the [API reference for an example](/ref/tilemap/#tile_source).

`material`
: The tile map material (`hash`). You can change this using a material resource property and `go.set()`. Refer to the [API reference for an example](/ref/tilemap/#material).

### Material constants

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: The color tint of the tile map (`vector4`). The vector4 is used to represent the tint with x, y, z, and w corresponding to the red, green, blue and alpha tint.

## Project configuration

The *game.project* file has a few [project settings](/manuals/project-settings#tilemap) related to tilemaps.

## External tools

There are external map/level editors that can export directly to Defold tilemaps:

### Tiled

[Tiled](https://www.mapeditor.org/) is a well-known and widely used map editor for orthogonal, isometric and hexagonal maps. Tiled has support for a wide array of features and can [export directly to Defold](https://doc.mapeditor.org/en/stable/manual/export-defold/). Learn more about how to export tilemap data and additional meta-data in [this blog post by Defold user "goeshard"](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) can be used to automatically create full tilesets from simple base tiles and it has a map editor which can export directly to Defold.




