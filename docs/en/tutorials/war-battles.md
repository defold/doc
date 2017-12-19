---
title: War battles tutorial
brief: In this tutorial you will create the embryo of a small shooter game. This is a good starting point if you are new to Defold.
---

# War battles tutorial

This tutorial goes through the steps needed to create a small playable game embryo in Defold. You do not need to have any prior experience with Defold, but if you have done some programming in Lua, Javascript, Python or similar, that will help.

::: important
We are in the process of transitioning to Defold editor 2, which is currently in alpha. This guide is written for the new editor 2, but most details apply to editor 1 as well. You are very welcome to [try the new editor](https://www.defold.com/editor-two/).
:::

To get an idea about what you are about to build, you can try the result here:

<div id="game-container" class="game-container">
    <img id="game-preview" src="//storage.googleapis.com/defold-doc/assets/war-battles/preview.jpg"/>
    <canvas id="game-canvas" tabindex="1" width="720" height="720">
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
                    return ("//storage.googleapis.com/defold-doc/assets/war-battles" + path + "");
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

Before you begin, you need to create an empty project on the Defold Dashboard and then download a package with the assets needed to create this game.

1. Go to the [Defold Dashboard](//dashboard.defold.com)
2. Click *New Project*
3. Choose a name for the project and select "Start from a blank slate"

   ![create project](images/war-battles/create_project.png)

4. Start Defold.
5. Click to open project "From Dashboard".

   ![open from dashboard](images/war-battles/from_dashboard.png)

6. Select your newly created project and choose a suitable location on your hard drive for your local working copy.

   ![import](images/war-battles/import_project.png)

The editor now opens.

## Editor overview

Let's take a moment to familiarize ourselves with the various views in the editor.

![editor overview](images/war-battles/editor_overview.png)

1. The *Assets* view lists all the files that are part of your project. You click and scroll to navigate the list. All file oriented operations can be made in this view:

    * <kbd>Double click</kbd> a file to open it in an editor for that file type.
    * <kbd>Drag and drop</kbd> to move files and folders to new locations.
    * <kbd>Right click</kbd> to open a pop up menu from where you can create new files or folders, rename, delete, track file dependencies and more.

2. The *Editor* view in the center shows the currently open file in an editor for that file type. A toolbar is visible in the top right, including tools to move, rotate and scale currently selected items. In all visual editors you can alter the camera view:

    * <kbd>Scroll</kbd> to zoom in and out.
    * <kbd>Alt + left mouse button</kbd> to pan around.
    * <kbd>Ctrl + left mouse button</kbd> to rotate in 3D.
    * The menu <kbd>Scene ▸ Camera</kbd> includes tools to frame the view to the current selection and to realign the camera.

3. The *Outline* shows the content of the file currently being edited, but in a hierarchial tree structure. The outline reflects the editor view and allows you to perform many operations on your items:

    * <kbd>Click</kbd> to select an item. Hold <kbd>Shift</kbd> or <kbd>Option</kbd> to expand the selection.
    * <kbd>Drag and drop</kbd> to change the hierarchy.
    * <kbd>Right click</kbd> to open a pop up menu from where you can add items, delete selected items etc.

4. The *Properties* view shows properties associated with the currently selected item, like *Position*, *Rotation*, *Animation* etc, etc.

5. The *Console* shows any error output or purposeful printing that you do while your game is running. Alongside the console are tabs containing the *Curve editor* which is used when editing curves in the particle editor, the *Build errors* view that shows build errors, and the *Search results* view that displays search results.

6. The *Changed files* view lists any files that have been changed, added or deleted in your project. By synchronizing the project regularly you can bring your local copy in sync with what is stored in the project Git repository, that way you can collaborate within a team, and you won't lose your work if misfortune strikes. Some file oriented operations can be performed in this view:

    * <kbd>Double click</kbd> a file to open it in a suitable editor, just like in the assets view.
    * <kbd>Right click</kbd> a file to open a pop up menu from where you can open a diff view, revert all changes done to the file, find the file on the filesystem and more.

## Cleaning the project

The empty project template is not 100% empty so we should fix that:

1. Open the file "main/main.collection".
2. Mark the game object "logo" in either the outline or the editor.
3. Delete the game object.
4. Delete the file "main/images/logo.png" (you find it in the assets view).
5. Delete the file "main/logo.atlas" (you find it in the assets view).

Now the project is totally empty. You can verify this by selecting <kbd>Project ▸ Build</kbd> from the menu. This will launch the game and you should see nothing but a black window.

## Drawing the game map

Your game needs a setting, a map. The map that you are going to draw will be made out of tiles, small images that are put together like a mosaic into a larger image. In Defold, such an image is called a *Tile map*. In order to create a tile map, you need to import an image file that contain the various tiles. You then need to specify the size of the tiles, margins and padding on that image. This setup is done in a file of a type called *Tile source*.

1. Download the "War Battles" asset package. The file is a ZIP archive that you have to unpack on your hard drive.

   <a class="btn btn-primary btn-xs-block btn-icon" href="//storage.googleapis.com/defold-doc/assets/war-battles-assets.zip">Download asset package<span aria-hidden="true" class="icon icon-download"></span></a>

2. Drag the file "map.png", which contains all tiles, from the asset package to the folder "main" in the *Assets* view of your project.

3. <kbd>Right click</kbd> the folder *main* and select <kbd>New ▸ Tile source</kbd>. This will create a new tile source file. Name the file "map" (full name "map.tilesource").

   ![map](images/war-battles/map_tilesource.png)

4. The new tilesource file opens automatically in the editor. Set the *Image* property of the tile source to the image file "/main/map.png". The easiest way to do that is to click the resource selector by the *Image* property to bring up the resource selector. Then select the file "/main/map.png":

    ![tilesource](images/war-battles/tilesource.png)

    The tiles are 16⨉16 pixels in the source image with no margins or padding so there is no need to alter the default properties of the tile source.

5. <kbd>Right click</kbd> the folder *main* and select <kbd>New ▸ Tile map</kbd>. Name the file "map" (full name "map.tilemap"). The tile map is automatically opened in the editor view.

6. Set the *Tile source* property of the new tile map to "/main/map.tilesource".

7. Select "layer1" in the *Outline*.

8. Select <kbd>Scene ▸ Tile map ▸ Show palette</kbd>. This brings up the tile palette.

    ![palette](images/war-battles/palette.png)

9. Click on a grass tile. This selects the clicked tile as the current brush. Then paint the tile map layer as you see fit with the grass tile. Select other tiles from the tile palette to paint different graphics.

10. You can hold <kbd>Shift</kbd>, then <kbd>click and drag</kbd> to make a selection on the current layer. The selection then becomes your new brush. This is a useful way to paint with a brush consisting of multiple tiles.

    ![selection](images/war-battles/selection.png)

When you are happy with the map, it is time to add it to the game.

## Add the map to the game

Defold stores everything you build in *collections*. A collection is a container of game objects and other collections. In the file "game.project" you specify the collection that is loaded when the game starts up. This is initially set to the file "/main/main.collection".

1. Open the file "main.collection".

2. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add game object</kbd>.

    ![add game object](images/war-battles/add_game_object.png)

3. Change the *Id* property of the game object to "map". The id does not really matter for this game object but it is a good habit to set identifiers that are descriptive---it makes it easier to find your way around when you have many game objects.

4. <kbd>Right click</kbd> the new game object and select <kbd>Add Component File</kbd>.

    ![add component](images/war-battles/add_component.png)

5. In the resource selector, pick the file "/main/map.tilemap". This creates a new component in the game object based on the tilemap file. The tile map should now appear in the editor view.

    ![tilemap](images/war-battles/tilemap.png)

6. Run the game by selecting <kbd>Project ▸ Build</kbd> and check that everything looks good. If you feel that the window is a bit large you can open *game.project* in the project root and alter the display width and height:

    ![display](images/war-battles/display.png)

## The player animation

1. Drag the folder *units/infantry* from the asset package to the folder *main* in the *Assets* view. This copies a set of flip book animation frame images to your project. The images are divided into folders with one folder for each movement direction: up, down, up-diagonally, down-diagonally and side.

2. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Atlas</kbd>. Name the new atlas file "sprites" (full name "sprites.atlas"). An atlas is a collection of images (PNG or JPEG) that are baked into a larger texture. Defold uses atlases instead of single image files for performance and memory reasons. The new atlas should open in the editor.

3. <kbd>Right click</kbd> the root node of the atlas in the *Outline* and select <kbd>Add Animation Group</kbd>.

4. Select the new animation group and change its *Id* property to "player-down".

5. <kbd>Right click</kbd> the "player-down" animation group and select <kbd>Add Images...</kbd>. In the resource selector, pick the images */main/infantry/down/1.png* to */main/infantry/down/4.png*.

    ![add images](images/war-battles/add_images.png)

6. With the animation group marked, select <kbd>Scene ▸ Play</kbd> from the menu to preview the animation. It will play back at full 60 FPS which is way too fast. Set the playback speed (*Fps* property) to 8.

    ![play animation](images/war-battles/play_animation.png)

Now you have an atlas with a single flipbook animation for the player. This is enough for initial testing---you can add more animations later. Now, let's create the player game object.

## The player game object

1. Open *main.collection*.

2. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add Game Object</kbd>. Set the *Id* property of the new game object to "player".

3. Change the Z *Position* property of the game object named "player" to 1.0. Since the "map" game object is at the default Z position 0 the "player" game object must be at a higher value (between -1.0 and 1.0) for it to be on top of the level.

4. <kbd>Right click</kbd> the game object "player" and select <kbd>Add Component ▸ Sprite</kbd>. This creates a new sprite component in the "player" game object that can show graphics.

5. Make sure that the Z *Position* of the *Sprite* is 0 so it will be rendered at the same depth as the game object "player". Setting the Z to a different value will offset the sprite depth from 1.0

6. Set the *Image* property of the sprite to */main/sprites.atlas*.

7. Set the *Default Animation* property of the sprite to "player-down".

    ![player sprite](images/war-battles/player_sprite.png)

8. Run the game and check that the player character is animating.

The player game object now has visual representation in the game world. The next step is to add a script component to the player game object. This will allow you to create player behavior, such as movement. But that depends on user input, so first you need to set that up.

## Player input

1. Open the file "/input/game.input_binding". This file contains mappings from input sources (keyboard, touch screen, game pads etc) to input *actions*. Actions are just names that we want to associate with certain input.

2. Add *Key triggers* for the four arrow keys. Name the actions "up", "down", "left" and "right".

    ![input](images/war-battles/input_bindings.png)

## The player script

Unlike the sprite component, which you added directly into the "player" game object, a script component requires that you create a separate file. This script file is then used as basis for the script component.

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Script</kbd>. Name the new script file "player" (full name "player.script"). The script file, pre-filled with template functions, opens up in the editor.

    ![player script](images/war-battles/player_script.png)

2. Open *main.collection*, <kbd>Right click</kbd> the game object "player" and select <kbd>Add Component File</kbd>. Pick the new file "/main/player.script" as the file to use for the component.

You now have a script that runs in the "player" game object. It does not do anything yet though. Let's start by adding player movement.

## Player movement

The Lua code needed to create character movement in 8 directions is not long, but may require some time to understand completely. Copy the code below to *player.script*, run the game, then take your time to carefully read through the code notes below.

```lua
function init(self) -- <1>
    msg.post(".", "acquire_input_focus") -- <2>

    self.moving = false -- <3>    
    self.input = vmath.vector3() -- <4>
    self.dir = vmath.vector3(0, 1, 0) -- <5>
    self.speed = 50 -- <6>
end

function final(self) -- <7>
    msg.post(".", "release_input_focus") -- <8>
end

function update(self, dt) -- <9>
    if self.moving then
        local pos = go.get_position() -- <10>
        pos = pos + self.dir * self.speed * dt -- <11>
        go.set_position(pos) -- <12>
    end
    
    self.input.x = 0 -- <13>
    self.input.y = 0
    self.moving = false
end

function on_input(self, action_id, action) -- <14>
    if action_id == hash("up") then
        self.input.y = 1  -- <15>
    elseif action_id == hash("down") then
        self.input.y = -1
    elseif action_id == hash("left") then
        self.input.x = -1
    elseif action_id == hash("right") then
        self.input.x = 1
    end
        
    if vmath.length(self.input) > 0 then
        self.moving = true -- <16>
        self.dir = vmath.normalize(self.input) -- <17>
    end
end
```

1. The `init()` function is called when the script component is brought to life in the game engine. This function is useful for initial setup of the game object state.
2. This posts a message named "acquire_input_focus" to the current game object ("." is shorthand for the current game object). This is a system message that tells the engine to send input actions to this game object. The actions will arrive in this script component's `on_input()` function.
3. `self` is a reference to the current component instance. You can store state data that is local to the component instance in `self`. You use it like a Lua table by indexing the table field variables with the dot notation. The flag variable `moving` is used to track if the player is moving or not.
4. `input` is a vector3 that will point in any of the current 8 input directions. It will change as the player presses the arrow keys. The Z component of this vector is unused so it is kept at value 0.
5. `dir` is another vector3 that contains the direction the player faces. The direction vector is separate from the input vector because if there is no input and the player character does not move, it should still face a direction.
6. `speed` is the movement speed expressed in pixels per second.
7. The `final()` function is called when the script component is deleted from the game. This happens either when the container game object ("player") is deleted or when the game shuts down.
8. The script explicitly releases input focus, telling the engine that it wants no more input. Input focus is automatically released when the game object is deleted so this line is not necessary but is included here for clarity.
9. The `update()` function is called once each frame. The game is running at 60 frames per second so the function is called at an interval of 1/60 seconds. The argument variable `dt` contains the current frame interval---the time elapsed since the last call to the function.
10. If the `moving` flag is true, get the current game object position. The function `go.get_position()` takes an optional argument which is the id of the game object to get the position of. If no argument is given, the current game object's position is returned.
11. Add the current direction vector (scaled to speed and frame interval) to the position.
12. Set the position of the game object to the new position.
13. After the calculations have been made, set the input vector to 0 and unset the `moving` flag.
14. The `on_input()` function is called every frame for all mapped input that is active. The argument `action_id` contain the action as set up in the input bindings file. The argument `action` is a Lua table with details on the input.
15. For each input direction, set the X or the Y component of the `input` vector in `self`. If the user presses the <kbd>up arrow</kbd> and <kbd>left arrow</kbd> keys, the engine will call this function twice and the input vector will end up being set to `(-1, 1, 0)`.
16. If the user presses any of the arrow keys, the input vector length will be non zero. If so, set the `moving` flag so the player will be moved in `update()`. The reason the script does not move the player in the `on_input()` function is that it is simpler to collect all input each frame and then act upon it in `update()`.
17. The `dir` direction vector is set to the normalized value of the input. If the input vector is `(-1, 1, 0)`, for instance, the vector length is greater than 1. Normalizing the vector brings it to a length of exactly 1. Without normalization diagonal movement would be faster than horizontal and vertical. When the engine runs the `update()` function, any user input will have an effect on the `dir` vector which will cause the player to move.

With this piece of Lua code, your game now has a player character that can move around on the screen. Next, let's add the possibility to fire rockets.

Rockets should work like this: whenever the user presses a key, a rocket should fire. It should be possible to fire any number of rockets, not just one. Now, how do you achieve that? Consider *main.collection* for a second. It contains two game objects: the map and the player. Adding a new rocket game object to *main.collection* in the same way would not really get you the desired result---there would be only one rocket. So what to do?

What you need to is a *blueprint* for a rocket game object and then use some sort of "factory" that can create new game objects on the fly based on that blueprint. Let's start by creating the blueprint.

## The rocket game object

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Game Object</kbd>. Name this file "rocket" (full name "rocket.go").

    (Note that by creating this file, you do not create a new game object instance but a *blueprint* file for actual game object instances.)

2. Drag the folder *buildings/turret-rocket* from the asset package to the *main* folder in the *Assets* view.

3. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>Add Animation Group</kbd>). Name the animation "rocket".

4. Add the three rocket images to the animation group and set the *Fps* property to a value that makes the animation look good when you preview.

    ![rocket animation](images/war-battles/rocket_animation.png)

5. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Component ▸ Sprite</kbd>.

6. Set the *Image* property of the sprite to */main/sprites.atlas* and the *Default Animation* to "rocket".

Now you have a basic rocket game object blueprint, on file. The next step is to add functionality to spawn game objects based on this blueprint file. For that, you will use a *Factory* component. You also need to add a new input action for the firing mechanic.

## Spawning rockets

1. Open "main.collection" and <kbd>Right click</kbd> on the "player" game object. Select <kbd>Add Component ▸ Factory</kbd>.

2. Select the new factory component and set its *Id* property to "rocketfactory" and its *Prototype* to the file "/main/rocket.go" (the one you created above). Now the player game object is all set.

3. Open the file "/input/game.input_binding".

4. Add a *Key trigger* for the firing action. Call this action "fire".

    ![input](images/war-battles/input_bindings_fire.png)

5. Open *main/player.script* and add a flag to track if the player is firing to the `init()` function:

    ```lua
    function init(self)
        msg.post(".", "acquire_input_focus")
    
        self.moving = false
        self.firing = false -- <1>
        
        self.input = vmath.vector3()
        self.dir = vmath.vector3(0, 1, 0)
        self.speed = 50
    end
    ```
    1. Whenever the player is firing this value will be set to `true`.

6. In `update()`, add what should happen when the flag is set: the factory component should create a new game object instance:

    ```lua
    function update(self, dt)
        if self.moving then
            local pos = go.get_position()
            pos = pos + self.dir * self.speed * dt
            go.set_position(pos)
        end
        
        if self.firing then
            factory.create("#rocketfactory") -- <1>
        end
        
        self.input.x = 0
        self.input.y = 0
        
        self.moving = false
        self.firing = false -- <2>
    end
    ```
    1. If the `firing` flag is true, tell the factory component called "rocketfactory" that you just created to spawn a new game object. Note the character '#' that indicates that what follows is the id of a component.
    2. Set the firing flag to false. This flag will be set in `on_input()` each frame the player presses the fire key.

7. Scroll down to the `on_input()` function. Add a fourth `elseif` for the case where the function is called with the "fire" action and only the one frame when the key is pressed down:

    ```lua
        ...
        elseif action_id == hash("right") then
            self.input.x = 1
        elseif action_id == hash("fire") and action.pressed then
            self.firing = true
        end
        ...
    ```

If you run the game now you should be able to move around and drop rockets all over the map by hammering the fire key. This is a good start, now you only need to fix two things:

- When a rocket is spawned, it should be oriented in the player's direction. It should also move straight ahead.
- The rocket should explode after a short interval.

## Setting the direction of the rocket

1. Open *player.script* and scroll down to the `update()` function and update its code:

    ```lua
    function update(self, dt)
        if self.moving then
            local pos = go.get_position()
            pos = pos + self.dir * self.speed * dt
            go.set_position(pos)
        end
        
        if self.firing then
            local angle = math.atan2(self.dir.y, self.dir.x) -- <1>
            local rot = vmath.quat_rotation_z(angle) -- <2>
            local props = { dir = self.dir } -- <3>
            factory.create("#rocketfactory", nil, rot, props) -- <4>
        end
        ...
    ```
    1. Compute the angle (in radians) of the player.
    2. Create a quaternion for that angular rotation around Z.
    3. Create a table containing property values to pass to the rocket. The player's direction is the only data the rocket needs.
    4. Add explicit position (`nil`, the rocket will spawn at the player's position), rotation (the calculated quaternion) and spawn property values.

    Note that the rocket needs a movement direction in addition to the game object rotation (`rot`). It would be possible to make the rocket calculate its movement vector based on its rotation, but it is easier and more flexible to separate the two values. For instance, with a separate rotation it is possible to add rotation wobble to the rocket without it affecting the movement direction.

3.  <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Script</kbd>. Name the new script file "rocket" (full name "rocket.script"). Replace the template code in the file with the following:

    ```lua
    go.property("dir", vmath.vector3()) -- <1>
    
    function init(self)
        self.speed = 200 -- <2>
    end
    
    function update(self, dt)
        local pos = go.get_position() -- <3>
        pos = pos + self.dir * self.speed * dt -- <4>
        go.set_position(pos) -- <5>
    end
    ```
    1. Define a new script property named `dir` and initialize the property with a default empty vector (`vmath.vector3()`). The default value can be overrided by passing values to the `factory.create()` function. The current property value is accessed as `self.dir`. This is expected to be a unit vector (of length 1).
    2. A rocket speed value, expressed in pixels per second.
    3. Get the current rocket position.
    4. Calculate a new position based on the old position, the movement direction and the speed.
    5. Set the new position.

4. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Component File</kbd>. Select the file "rocket.script" as basis for the component.

5. Run the game and try the new mechanic. Notice that the rockets fly in the right direction but are oriented 180 degrees wrong. That's an easy fix.

    ![fire rockets](images/war-battles/fire_rockets.png)

6. Open *sprites.atlas*, select the "rocket" animation and click the *Flip horizontal* property.

    ![flip rocket](images/war-battles/flip_rocket.png)

7. Run the game again to verify that everything looks ok.

    ![fire rockets](images/war-battles/fire_rocket_2.png)

Now you only need to make the rockets explode a short while after they are fired.

## Explosions

1. Drag the folder *fx/explosion* from the asset package to the main folder in the Assets view.

2. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>Add Animation Group</kbd>). Call the animation "explosion".

3. Add the nine explosion images to the animation group and set the *Fps* property to a value that makes the animation look good when you preview. Also make sure that this animation has the *Playback* property set to `Once Forward`.

    ![explosion animation](images/war-battles/explosion_animation.png)

4. Open *rocket.script* and scroll down to the `init()` function and change it to:

    ```lua
    function init(self)
        self.speed = 200
        self.life = 1 -- <1>
    end
    ```
    1. This value will act as a timer to track the lifetime of the rocket.

5. Scroll down to the `update()` function and change it to:

    ```lua
    function update(self, dt)
        local pos = go.get_position()
        pos = pos + self.dir * self.speed * dt
        go.set_position(pos)
        
        self.life = self.life - dt -- <1>
        if self.life < 0 then -- <2>
            self.life = 1000 -- <3>
            go.set_rotation(vmath.quat()) -- <4>
            self.speed = 0 -- <5>
            msg.post("#sprite", "play_animation", { id = hash("explosion") }) -- <6>
        end
    end
    ```
    1. Decrease the life timer with delta time. It will decrease with 1.0 per second.
    2. When the life timer has reached zero.
    3. Set the life timer to a large value so this code won't run every subsequent update.
    4. Set the game object rotation to 0, otherwise the explosion graphics will be rotated.
    5. Set the movement speed to 0, otherwise the explosion graphics will move.
    6. Play the "explosion" animation on the game object's "sprite" component.

6. Below the `update()` function, add a new `on_message()` function:

    ```lua
    function on_message(self, message_id, message, sender) -- <1>
        if message_id == hash("animation_done") then -- <2>
            go.delete() -- <3>
        end 
    end
    ```
    1. The function `on_message()` gets called whenever a message is posted to this script component.
    2. Check if the message posted has the hashed name (or id) "animation_done". The engine runtime sends this message whenever a sprite animation initiated with "play_animation" from this script has completed.
    3. When the animation is done, delete the current game object.

Run the game.

![fire rockets](images/war-battles/fire_rocket_3.png)

This is definitely getting somewhere! But don't you think you need something to fire the rockets at?

## The tank game object

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Game Object</kbd>. Name this file "tank" (full name "tank.go"). Like the rocket game object, this is a file that can be used as a *blueprint* when creating actual tank game objects.

2. Drag the folder *units/tank* from the asset package to the *main* folder in the *Assets* view.

3. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>Add Animation Group</kbd>). Name the animation "tank-down".

4. Add the two downwards facing images (*/main/tank/down/1.png* and */main/tank/down/2.png*) to the animation and set it's *Fps* value to something that looks good.

    ![tank animation](images/war-battles/tank_animation.png)

5. Open *tank.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Component ▸ Sprite</kbd>.

6. Set the *Image* property of the sprite to */main/sprites.atlas* and the *Default animation* to "tank-down".

7. Open *main.collection*

8. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add Game Object File</kbd>. Select *tank.go* as blueprint for the new game object.

9. Create a few more tanks from the blueprint. Position them on the map with the *Move Tool*. Make sure to set the Z position to 1.0 so they are all rendered on top of the map.

    ![tanks](images/war-battles/tanks.png)

Run the game and check that the tanks look okay. You will notice that if you fire at the tanks, the rockets fly straight through them. The next step is to add collision between the tanks and the rockets.

## Adding collision objects

1. Open *tank.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Component ▸ Collision Object</kbd>.

2. Set the *Type* property to "Kinematic". This means that the physics engine will not simulate any gravity or collision on this object. Instead it will only detect and signal collisions and leave it to you to code the response.

3. Set the *Group* property to "tanks" and *Mask* to "rockets". This causes this game object to detect collisions against object in the group "rockets" that has the mask set to "tanks".

4. <kbd>Right click</kbd> the "collisionobject" component in the *Outline* and select <kbd>Add Shape ▸ Box</kbd>. Set the size of the box shape to match the tank graphics.

    ![tank collision](images/war-battles/tank_collision.png)

6. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add Component ▸ Collision Object</kbd>.

7. Set the *Type* property to "Kinematic".

8. Set the *Group* property to "rockets" and *Mask* to "tanks". This causes this game object to detect collisions against object in the group "tanks" that has the mask set to "rockets".

    Now the group and mask between rockets and tanks match each other so the physics engine will detect when they interact.

    ![rocket collision](images/war-battles/rocket_collision.png)

The physics engine sends messages to game objects that collide. The last piece of the puzzle is to add code that reacts to those messages.

## Reacting to collisions

1. Open *rocket.script* and scroll down to the `update()` function. There are a couple of things to do here:

    ```lua
    local function explode(self) -- <1>
        self.life = 1000
        go.set_rotation(vmath.quat())
        self.speed = 0
        msg.post("#sprite", "play_animation", { id = hash("explosion") })       
    end
    
    function update(self, dt)
        local pos = go.get_position()
        pos = pos + self.dir * self.speed * dt
        go.set_position(pos)
        
        self.life = self.life - dt
        if self.life < 0 then
            explode(self) -- <2>
        end
    end
    
    function on_message(self, message_id, message, sender)
        if message_id == hash("animation_done") then
            go.delete()
        elseif message_id == hash("collision_response") then -- <3>
            explode(self) -- <4>
            go.delete(message.other_id) -- <5>
        end
    end
    ```
    1. Since you want the rocket to explode either when the timer runs out (in `update()`) or when the rocket hits a tank (in `on_message()`) you should break out that piece of code to avoid duplication. In this case that is done with a local function. The function is declared `local`, meaning that it only exist within the scope of the rocket script. Lua's scoping rules says that local functions need to be declared before they are used. Therefore the function is placed above `update()`. Also make sure to pass `self` as a parameter to the function so you can access `self.life` etc.
    2. The code that used to live here has been moved to the `explode()` function.
    3. The engine sends a message called "collision_response" when the shapes collide, if the group and mask pairing is correct.
    4. Call the `explode()` function if there is a collision.
    5. Finally delete the tank. You get the id of the game object the rocket collided with through the `message.other_id` variable.

Run the game and destroy some tanks! The tanks aren't very interesting enemies, but they should nevertheless give you some score.

## Scoring GUI

1. Drag the the file "fonts/04font.ttf" from the asset pack folder to the "main" folder in the *Assets* view.

2. <kbd>Right click</kbd> the folder "main" in the *Assets* view and select <kbd>New ▸ Font</kbd>. Name this file "text" (full name "text.font").

3. Open *text.font* and set the *Font* property to the file "04font.ttf".

    ![text font](images/war-battles/text_font.png)

4. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Gui</kbd>. Name this file "ui" (full name "ui.gui"). It will contain the user interface where you will place the score counter.

5. Open "ui.gui". <kbd>Right click</kbd> *Fonts* in the *Outline* view and select <kbd>Add ▸ Fonts</kbd>. Select the "/main/text.font" file.

6. <kbd>Right click</kbd> *Nodes* in the *Outline* view and select <kbd>Add ▸ Text</kbd>.

7. Select the new text node in the outline and set its *Id* property to "score", its *Text* property to "SCORE: 0", its *Font* property to the font "text" and its *Pivot* property to "West".

8. Place the text node in the top left corner of the screen.

    ![ui gui](images/war-battles/ui.png)

9. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Gui Script</kbd>. Name this new file "ui" (full name "ui.gui_script").

10. Go back to "ui.gui" and select the root node in the *Outline*. Set the *Script* property to the file "/main/ui.gui_script" that you just created. Now if we add this Gui as a component to a game object the Gui will be displayed and the script will run.

11. Open *main.collection*.

12. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add Game Object</kbd>.

13. Set the *Id* property of the game object to "gui", then <kbd>Right click</kbd> it and select <kbd>Add Component File</kbd>. Select the file "/main/ui.gui". The new component will automatically get the *Id* "ui".

    ![main gui](images/war-battles/main_ui.png)

Now the score counter is displayed. You only need to add functionality in the Gui script so the score can be updated.

## Updating the score

1. Open *ui.gui_script*

2. Replace the template code with the following:

    ```lua
    function init(self)
        self.score = 0 -- <1>
    end
    
    function on_message(self, message_id, message, sender)
        if message_id == hash("add_score") then -- <2>
            self.score = self.score + message.score -- <3>
            local scorenode = gui.get_node("score") -- <4>
            gui.set_text(scorenode, "SCORE: " .. self.score) -- <5>
        end 
    end
    ```
    1. Store the current score in `self`. Start from 0.
    2. Reaction to a message named "add_score".
    3. Increase the current score value in `self` with the value passed in the message.
    4. Get hold of the text node named "score" that you created in the Gui.
    5. Update the text of the node to the string "SCORE: " and the current score value concatenated to the end of the string.

3. Open *rocket.script* and scroll down to the `on_message()` function where you need to add one new line of code:

    ```lua
    function on_message(self, message_id, message, sender)
        if message_id == hash("animation_done") then
            go.delete()
        elseif message_id == hash("collision_response") then
            explode(self)
            go.delete(message.other_id)
            msg.post("/gui#ui", "add_score", {score = 100}) -- <1>
        end
    end
    ```
    1. Post a message named "add_score" to the component "ui" in the game object named "gui" at the root of the main collection. Pass along a table where the field `score` has been set to 100.

4. Try the game!

![done](images/war-battles/done.png)

There you go! Well done!

## What next?

We hope you enjoyed this tutorial and that it was helpful. To get to know Defold better, we suggest that you to continue working with this little game. Here are a few suggested exercises:

1. Add directional animations for the player character. Tip, add a function called `update_animation(self)` to the `update()` function and change the animation depending on the value of the `self.dir` vector. It is also worth remembering that if you send a "play_animation" message each frame to a sprite, the animation will restart from the beginning, each frame---so you should only send "play_animation" when the animation should change.

2. Add an "idle" state to the player character so it only plays a walking animation when moving.

3. Make the tanks spawn dynamically. Look at how the rockets are spawned and do a similar setup for the tanks. You might want to create a new game object in the main collection with a script that controls the tank spawning.

4. Make the tanks patrol the map. One simple option is to have the tank pick a random point on the map and move towards that point. When it is within a short distance of the point, it picks a new point.

5. Make the tanks chase the player. One option is to add a new collision object to the tank with a spherical shape. If the player collides with the collision object, have the tank drive towards the player.

6. Make the tanks fire at the player.

7. Add sound effects.

If you are stuck, please head over to the [Defold Forum](//forum.defold.com) where you can talk to the Defold developers and many friendly users.