---
title: Side scroller tutorial
brief: This tutorial is intended to give a taste of what making games in Defold is about. It goes through creating a new project, based on a simple side-scroller. You will then learn how to tweak the game to make it more fun. Finally you will add a new game object. The tutorial should only take about 10 minutes.
---

# Side scroller

The game is extremely simple. The player controls a space ship and is supposed to collect stars that appear on the screen. The ship is controlled with the up and down arrow keys on the keyboard.

(You can try the game right here in the browser. Use the arrow keys to control the ship.)

<div id="game-container" class="game-container">
  <img id="game-preview" src="//storage.googleapis.com/defold-doc/assets/side-scroller/preview.jpg"/>
  <canvas id="game-canvas" tabindex="1" width="1280" height="720">
  </canvas>
  <button id="game-button">
    START GAME <span class="icon"></span>
  </button>
  <script src="//storage.googleapis.com/defold-doc/assets/dmloader.js"></script>
  <script src="//storage.googleapis.com/defold-doc/assets/dmengine_1_2_106.js" async></script>
  <script>
      /* Load app on click in container. */
      document.getElementById("game-button").onclick = function (e) {
          var extra_params = {
              archive_location_filter: function( path ) {
                  return ("//storage.googleapis.com/defold-doc/assets/side-scroller" + path + "");
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

## Setup

1. Start by going to the [Defold Dashboard](//dashboard.defold.com), log in and click *New Project*.
2. Select the *Side Scroller* tutorial as the template project.

   ![New project](images/side-scroller/new_project.png)

3. Click <kbd>Save</kbd>.

Now your new project exist on our cloud servers and you can start work on it in the editor:

1. Start Defold.
2. In the project selector, click "Open Project" <kbd>From Dashboard</kbd>. The first time you do this you will need to log in with your account.
3. Select your new project.
4. Select a location on your hard drive where your working copy will be stored.
5. Click <kbd>Import</kbd>.

  ![Import](images/side-scroller/import.jpg)

6. The editor now opens your new project:

  ![Editor](images/side-scroller/editor.jpg)

7. Try running the game by selecting the menu item <kbd>Project ▸ Build</kbd>. You can steer the space ship with the arrow keys and pick up stars.

  ![Run the game](images/side-scroller/run_game.jpg)

## Tweaking the game

The game is currently not much fun, but you can improve it with some simple tweaks. You will do the update tweaks to the game live so make sure that you keep the game running somewhere on your desktop.

First, let's adjust the speed of the space ship:

1. In the editor, open the file "spaceship.script" with the menu item <kbd>File ▸ Open Asset...</kbd>. (Type "space" to searching among all the available assets and select the file "spaceship.script".)

   ![Open asset](images/side-scroller/open_asset.png)

3. Click <kbd>Open</kbd>. The file now opens in the Lua code editor.

   ![Code editor](images/side-scroller/code_editor.jpg)

4. At the top of the file, change:

   ```lua
   local max_speed = 60
   ```

   to:

   ```lua
   local max_speed = 150
   ```

   This will increase the movement speed of the space ship.

3. Reload the script file into the running game with <kbd>File ▸ Hot Reload</kbd>.

Try moving the space ship with the arrow-keys on your keyboard. Notice how the it moves faster now.

Currently, the player only gets 1 point for each star collected. More score is more fun so let's fix that.

1. Open the file "star.script". Either use <kbd>File ▸ Open Asset...</kbd> or find the file in the *Assets* browser in the leftmost editor pane and double click it. The file is in the "star" folder.
2. At the top of the file, change:

    ```lua
    local score = 1
    ```

    to:

    ```lua
    local score = 1000
    ```

3. Reload the script file into the running game with <kbd>File ▸ Hot Reload</kbd>.
4. Collect some stars and notice how the score has dramatically increased.

## Adding bonus stars

![Bonus stars](images/side-scroller/bonus_star.jpg)

The game would be a bit more interesting if bonus stars would appear now and then. In order to make that happen, you need to create a new *game object* file, which will work as a blueprint for the new type of star.

1. Add a new game object file. <kbd>Right-click</kbd> the "stars" folder in the *Assets* view and select <kbd>New... ▸ Game Object</kbd>. Name the new file "bonus_star". (The editor will automaticaly append a file ending so the full name will be "bonus_star.go".)

   ![New game object](images/side-scroller/new_game_object.png)

2. The editor automatically opens the new file so you can edit it.

3. Add a *Sprite* component to the game object. <kbd>Right-click</kbd> the root of the *Outline* view and select <kbd>Add Component ▸ Sprite</kbd>. This allows you to attach graphics to the bonus star.

   ![Add component](images/side-scroller/add_component.png)

In the *Outline* view, you will see a new item called "sprite". When it is clicked, its properties are displayed in the *Properties* view below. The sprite currently has no graphics attached so you need to do that:

1. Set the *Image* property to "stars.atlas" by using the browse-button <kbd>...</kbd>. The atlas contains the graphics for the bonus star.

2. Set *Default Animation* to "bonus_star" and hit *ENTER*. "bonus_star" is an animation defined in the atlas.

   ![Sprite properties](images/side-scroller/sprite_properties.jpg)

3. A green star should appear in the editor. Hit the <kbd>F</kbd> key or select <kbd>View ▸ Frame Selection</kbd> if the view of the star is not very good.

4. Add a *Collision Object* component to the game object. <kbd>Right click</kbd> the root "Game Object" item in the *Outline* view and select <kbd>Add Component ▸ Collision Object</kbd>. This lets the bonus stars collide with other game objects, like the player space ship which is necessary for it to be able to gather bonus stars as well as ordinary stars.

5. Click on the "collisionobject" item in the *Outline* view to show its properties.

6. In the *Properties* view, set its *Type* to "Kinematic". This means that the collision object will follow the game object it belongs to.

7. <kbd>Right click</kbd> "collisionobject" in the *Outline* view and select <kbd>Add Shape ▸ Sphere</kbd>. Any shape(s) you add to the collision object defines its boundary as far as collisions are concerned.

8. Select the *Scale Tool* in the toolbar and use the scale handle to resize the sphere in the scene view until it reasonably covers the star. You can also edit the *Diameter* property directly in the *Properties* view.

   ![Sphere size](images/side-scroller/sphere_size.jpg)

7. <kbd>Right click</kbd> the root "Game Object" item in the *Outline* view again and select <kbd>Add Component File</kbd>, then select the script "bonus_star.script". This script moves the bonus stars and make sure the player gets the right amount of points for catching them.

Now the bonus star game object file contains the blueprint for a game object containing graphics (the sprite), collision shapes (the collision object) and logic that moves the star and reacts to collisions (the script).

![Bonus star game object](images/side-scroller/bonus_star_done.jpg)

## Creating a bonus star factory

*Factory Components* are responsible for making sure game objects of various kind appear in the game. For your new bonus stars, you need to create a factory:

1. Open the file "factory.go" with <kbd>File ▸ Open Assets...</kbd>. This game object file contains a script and a factory.

2. Add a secondary factory component to it. <kbd>Right click</kbd> the root "Game Object" item in the *Outline* view and select <kbd>Add Component ▸ Factory</kbd>.

3. Set the new factory component's *Id* property to "bonus_factory".

4. Set its *Prototype* property to "bonus_star.go" with the browse-button (<kbd>...</kbd>).

   ![Factory component](images/side-scroller/factory.jpg)

## Modify the factory script

The last step is to make sure the factory game object starts creating the bonus stars by modifying its script.

1. Open *factory.script* with <kbd>File ▸ Open Assets...</kbd>

2. Near the bottom of the file, change:

    ```lua
    -- component = "#bonus_factory"
    ```

    to:

    ```lua
    component = "#bonus_factory"
    ```

    This causes the bonus stars to appear roughly 20% of the time.

3. Restart the game by closing the window (or <kbd>Esc</kbd>) to exit, then <kbd>Project ▸ Build</kbd> in the editor.

   The new bonus stars will start to appear!

![Run final game](images/side-scroller/run_final.jpg)

**You Win!**

Now go ahead and create more games in Defold!
