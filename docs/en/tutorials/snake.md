---
title: Building a snake game in Defold
brief: If you are new to Defold, this guide will help you to get started with script logic together with a few of the building blocks in Defold.
---

# Snake

This tutorial walks you through the process of creating a snake game. This is onen of the most common classic games you can attempt to recreate. There are a lot of variations on this game, this one features a snake that eats "fruit", that only grows when it eats. The snake also crawls on a playfield that contains obstacles.

Before beginning, take a minute and try the game:

<div id="game-container" class="game-container">
  <img id="game-preview" src="//storage.googleapis.com/defold-doc/assets/snake/preview.jpg"/>
  <canvas id="game-canvas" tabindex="1" width="512" height="512">
  </canvas>
  <button id="game-button">
    START GAME <span class="icon"></span>
  </button>
  <script src="//storage.googleapis.com/defold-doc/assets/dmloader.js"></script>
  <script src="//storage.googleapis.com/defold-doc/assets/dmengine_1_2_107.js" async></script>
  <script>
      /* Load app on click in container. */
      document.getElementById("game-button").onclick = function (e) {
          var extra_params = {
              archive_location_filter: function( path ) {
                  return ("//storage.googleapis.com/defold-doc/assets/snake" + path + "");
              },
              load_done: function() {},
              game_start: function() {
                  var e = document.getElementById("game-preview");
                  e.parentElement.removeChild(e);
              }
          }
          Module.runApp("game-canvas", extra_params);
          document.getElementById("game-button").style.display = 'none';
          document.getElementById("game-button").onclick = null;
      };
  </script>
</div>

## Setting up the project

Create a new project and do a quick clean up. If you already know how to do that, great. If you don’t, head over to the [war battles](/tutorials/war-battles) tutorial and read the sections “Setting up the project” through “Cleaning the project”. There is also an overview of the editor there that will help you find your way around if you are totally new to Defold.

With the project cleaned up, open the *game.project* settings file and set the dimensions of the game to 768⨉768 or some other multiple of 16. The reason why you want to do this is because the game will be drawn on a grid where each segment is going to be 16x16 pixels, and this way the game screen won't cut off any segments at the edges.

## Adding graphics to the game

Very little is needed in terms of graphics. One 16x16 segment for the snake, one for obstacles and one for the "fruit". Here is an image containing the graphics. Download it and drag it to a location in the project folder.

![snake sprites](images/snake/snake.png)

Defold provides a built in *Tilemap* component that you will use to create the playfield. A tilemap allow you to set and read individual tiles, which suits this game perfectly. A tilemap will fetch its graphics from a *Tilesource* so you need to create one:

<kbd>Right click</kbd> the *main* folder and select <kbd>New ▸ Tile Source</kbd>. Name the new file "snake.tilesource".

The *Width* and *Height* properties should be kept at 16. This will split the 32⨉32 pixel image into 4 tiles, numbered 1–4.

![tilesource](images/snake/tilesource.png)

Note that the *Extrude Borders* property is set to 1 pixel. This is to prevent visual artifacts around the tiles that have graphics all the way out to the edge.

## Creating the play field tilemap

Now you have a tilesource ready for use so it's time to create the playfield tilemap component:

<kbd>Right click</kbd> the *main* folder and select <kbd>New ▸ Tile Map</kbd>. Name the new file "grid.tilemap".

Defold only stores the area of the tilemap that is actually used so you need to add enough tiles to fill the boundaries of the screen. Select the "layer1" layer and paint a border around the edge of the screen and some obstacles. Choose the menu option <kbd>Scene ▸ Tile Map ▸ Show Palette</kbd> to display the tile palette, then click the tile you want to use when painting.

![tilemap](images/snake/tilemap.png)

Save the tilemap when you are done.

## Adding the tilemap and a script to the game

Now open *main.collection*. <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Game Object</kbd> which creates a new game object in the main collection that is loaded when the game starts.

![add game object](images/snake/add_game_object.png)

Then <kbd>Right click</kbd> then new game object and select <kbd>Add Component File</kbd>. Choose the file "grid.tilemap" that you just created.

![add component](images/snake/add_component_file.png)

<kbd>Right click</kbd> the folder *main* in the *Assets* browser and select <kbd>New ▸ Script</kbd>. Name the new script file "snake.script". This file will hold all the logic for the game.

Go back to *main.collection* and <kbd>right click</kbd> then game object holding the tilemap. Select <kbd>Add Component File</kbd> and choose the file "snake.script".

Now you have the tilemap component and the script in place. If you run the game you should see the playfield as you drew it on the tilemap.

![main collection](images/snake/main_collection_no_gui.png)

## Coding the game

The script you are going to create will drive all of the game. The idea is to basically do this:

1. Keep a list of tile positions the snake currently occupies.
2. If the player presses a directional key, store the direction the snake should be moving.
3. At a regular interval, move the snake one step in the current movement direction, then redraw the snake at the new position.

Open *snake.script* and locate the `init()` function. This function is called by the engine when the script is initialized on game start. Change the code to the following.

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24} } -- <2>
    self.dir = {x = 1, y = 0} -- <3>
    self.speed = 7.0 -- <4>

    self.t = 0 -- <5>
end
```
1. Send a message to the current game object ("." is shorthand for the current game object) telling it to start receiving input from the engine.
2. Store the segments of the snake as a Lua table containing a list of tables, each holding a X and Y position.
3. Store the current direction as a table holding an X and Y direction.
4. Store the current movement speed.