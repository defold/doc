---
title: War battles tutorial
brief: In this tutorial you will create a small shooter game. This is a good starting point if you are new to Defold.
---

# War battles tutorial

This tutorial goes through all the steps needed to create a small playable game in Defold. You do not need to have any prior experience with Defold, but if you have done some programming in Lua, Javascript, Python or similar, that will help.

To get an idea about what you will build, you can try the result here:

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

You need to create an empty project in Defold and download the asset package.

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

    * <kbd>Double click</kbd> a file to open it in a suitable editor.
    * <kbd>Drag and drop</kbd> to move files and folders to new locations.
    * <kbd>Right click</kbd> to open a pop up menu from where you can create new files or folders, rename, delete see dependencies and more.

2. The *Editor* view in the center shows the currently open file in a suitable editor. Defold includes editors for all its file types. A toolbar is visible in the top right. There you find tools to move, rotate and scale the currently selected item. For all visual editors you can also alter the camera view:

    * <kbd>Scroll</kbd> to zoom in and out.
    * <kbd>Alt + left mouse button</kbd> to pan around.
    * <kbd>Ctrl + left mouse button</kbd> to rotate in 3D.
    * The menu <kbd>Scene ▸ Camera</kbd> includes tools to frame and realign the camera.

3. The *Outline* shows the content of the currently open file in a hierarchial tree structure. The outline reflects the editor view and allows you to perform many operations on your items:

    * <kbd>Click</kbd> to select an item. Hold <kbd>Shift</kbd> or <kbd>Option</kbd> to expand the selection.
    * <kbd>Drag and drop</kbd> to change the hierarchy.
    * <kbd>Right click</kbd> to open a pop up menu from where you can add items, delete selected items etc.

4. The *Properties* view shows properties associated with the currently selected item, like *Position*, *Rotation*, *Animation* etc etc.

5. The *Console* shows any output that is printed when you run the game. Alongside the console is the *Curve editor* which is used when editing curves in the particle editor, the *Build errors* view that shows build errors and the *Search results* view that displays search results.

6. The *Changed files* view lists any files that has been changed, added or deleted in your project. By synchronizing the project regularly you can upload all file changes to the project Git repository, that way you won't lose your work if unfortune strikes. Some file oriented operations can be performed in this view:

    * <kbd>Double click</kbd> a file to open it in a suitable editor, just like in the assets view.
    * <kbd>Right click</kbd> to open a pop up menu from where you can open a diff view or revert all changes done to the file.

## Cleaning the project

The empty project template is not 100% empty so we should fix that:

1. Open the file *main/main.collection*.
2. Mark the game object "logo" in either the outline or the editor.
3. Delete the game object.
4. Delete the file *main/images/logo.png* (you find it in the assets view).
5. Delete the file *main/logo.atlas* (you find it in the assets view).

Now the project is totally empty. You can verify this by selecting <kbd>Project ▸ Build</kbd> from the menu. This will launch the game and you should see nothing but a black window.

## Drawing a map

The map that you are going to draw will be made out of tiles, small images that are put together like a mosaic into a larger image. In Defold, such an image is called a *Tile map*. In order to create a tile map, you need to import an image with the various tiles, and also set up the sizes, margins etc of that image. This setup is done in a file called a *Tile source*.

1. Download the "War Battles" asset package. The file is a ZIP archive that you have to unpack on your hard drive.

   <a class="btn btn-primary btn-xs-block btn-icon" href="//storage.googleapis.com/defold-doc/assets/war-battles-assets.zip">Download asset package<span aria-hidden="true" class="icon icon-download"></span></a>

2. Drag the file *map.png*, which contains all tiles, to the folder *main* in the *Assets* view of your project.
3. <kbd>Right click</kbd> the folder *main* and select <kbd>New ▸ Tile source</kbd>. This will create a new tile source file. Name the file *map.tilesource*.

   ![map](images/war-battles/map_tilesource.png)

4. The new tilesource opens in the editor. Set the *Image* property of the tile source to "/main/map.png". Easiest is to click the resource selector by the *Image* property to bring up the resource selector. Then select the file */main/map.png*:

    ![tilesource](images/war-battles/tilesource.png)

    The tiles are 16⨉16 pixels in the source image so there is no need to alter the properties of the tile source.

5. <kbd>Right click</kbd> the folder *main* and select <kbd>New ▸ Tile map</kbd>. Name the file *map.tilemap*.

6. Set the *Tile source* property of the new tile map to "/main/map.tilesource".

7. Select "layer1" in the *Outline*.

8. Select <kbd>Scene ▸ Tile map ▸ Show palette</kbd>. This brings up the tile palette.

    ![palette](images/war-battles/palette.png)

9. Click on a grass tile to select the tile as brush. Now paint the tile map layer as you see fit. You can hold <kbd>Shift</kbd> and click to make a selection on the layer. The selection then becomes your new brush. This is useful to copy rectangular areas.

    ![selection](images/war-battles/selection.png)

When you are happy with the map, it is time to add it to the game.

## Add the map to the game

1. Open *main.collection*. A collection is a container of game objects and other collections. You use collections to organize your game objects. In *game.project* you specify the collection that is loaded when the game starts up. This is initially set to "/main/main.collection".

2. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add game object</kbd>.

    ![add game object](images/war-battles/add_game_object.png)

3. Change the *Id* property of the game object to "map". The id does not really matter for this game object but it is a good habit to set identifiers that are descriptive---it makes it easier to find your way around when you have many game objects.

4. <kbd>Right click</kbd> the new game object and select <kbd>Add component file</kbd>.

    ![add component](images/war-battles/add_component.png)

5. In the resource selector, pick "/main/map.tilemap". This adds a new tilemap component to the game object. The tile map should now appear in the editor view.

    ![tilemap](images/war-battles/tilemap.png)

6. Run the game by selecting <kbd>Project ▸ Build</kbd> and check that everything looks good. If you feel that the window is a bit large you can open *game.project* in the project root and alter the display width and height:

    ![display](images/war-battles/display.png)

## The player animation

1. Drag the folder *infantry* (it's in the folder *units*) from the asset package to the folder *main* in the *Assets* view. This copies a set of flip book animation frame images to your project. The images are divided into one folder for each movement direction: up, down, up-diagonally, down-diagonally and side.

2. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Atlas</kbd>. An atlas is a collection of images (PNG or JPEG) that are baked into a larger texture. Atlases are used instead of single image files for performance and memory reasons. The new atlas should open in the editor.

3. <kbd>Right click</kbd> the root node of the atlas in the *Outline* and select <kbd>New ▸ Animation group</kbd>.

4. Select the new animation group and change its *Id* property to "player-down".

5. <kbd>Right click</kbd> the "player-down" animation group and select <kbd>Add images...</kbd>. In the resource selector, pick the images */main/infantry/down/1.png* to */main/infantry/down/4.png*.

    ![add images](images/war-battles/add_images.png)

6. With the animation group marked, select <kbd>Scene ▸ Play</kbd> from the menu to preview the animation. It will play back at full 60 FPS which is way too fast. Set the playback speed (*Fps* property) to 8.

    ![play animation](images/war-battles/play_animation.png)

Now you have an atlas with a single flipbook animation for the player. You will add more animations later, but first, let's create the player game object.

## The player game object

1. Open *main.collection*.

2. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add game object</kbd>. Set the *Id* property of the new game object to "player".

3. Change the Z *Position* property of the game object to 1.0. Since the "map" game object is at the default Z position 0 the "player" game object needs to be at a higher value so it's drawn on top.

4. <kbd>Right click</kbd> the game object "player" and select <kbd>Add component ▸ Sprite</kbd>. This creates a new sprite component in the "player" game object that can show graphics.

5. Set the *Image* property of the sprite to "/main/sprites.atlas".

6. Set the *Animation* property of the sprite to "player-down".

    ![player sprite](images/war-battles/player_sprite.png)

7. Run the game and check that the player character is animating.

The player game object now has a sprite component that gives it visual representation in the game world. The next step is to add a script component that gives the player game object behavior. The player game object's behavior, however, is depending on user input, so that needs to be set up first.

## Player input

1. Open the file */input/game.input_binding*. This file contains mappings from input sources (keyboard, touch screen, game pads etc) to input *actions*. Actions are just names that we want certain input being associated with.

2. Add *Key triggers* for the four arrow keys.

    ![input](images/war-battles/input_bindings.png)

## The player script

Unlike the sprite component, which you added inline into the "player" game object, a script component requires that you create a separate file.

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Script</kbd>. Name the new script file "player.script". The script file should open in the editor. It is pre-filled with functions from a template.

    ![player script](images/war-battles/player_script.png)

2. Open *main.collection*, <kbd>Right click</kbd> the game object "player" and select <kbd>Add component file</kbd>. Pick the new file */main/player.script* for the component.

You now have a script that runs in the "player" game object. It does not do anything though so let's start by adding player movement.

## Player movement

The Lua code needed to create character movement in 8 directions is not long, but may require some time to understand completely. Take your time and read through the extensive code notes as you copy the below script code into *player.script*.

```lua
function init(self) -- <1>
    msg.post("#", "acquire_input_focus") -- <2>

    self.moving = false -- <3>    
    self.input = vmath.vector3() -- <4>
    self.dir = vmath.vector3(0, 1, 0) -- <5>
    self.speed = 50 -- <6>
end

function final(self) -- <7>
    msg.post("#", "release_input_focus") -- <8>
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

1. The `init()` function is called when the script component is brought to life in the game engine.
2. This posts a message named "acquire_input_focus" to the current component ("#" is shorthand for the current component). This is a system message that tells the engine to send input actions to this script component.
3. `self` is a reference to the current component instance. You can keep state data that is local to the component instance by storing it in self. The flag `moving` is used to track if the player is moving or not.
4. `input` is a vector3 that will point in any of the current 8 input directions. It changes as the player presses the arrow keys. The Z component of this vector is unused.
5. `dir` is a vector3 that indicates the direction the player faces. The direction vector is separate from the input vector because if there is no input, the player character should still face in a direction, even if not moving.
6. `speed` is the movement speed expressed in pixels per second.
7. The `final()` function is called when the script component is deleted from the game. This happens either when the container game object ("player") is deleted or when the game shuts down.
8. The script explicitly releases input focus, telling the engine that it wants no more input. Input focus is automatically released when the game object is deleted so this line is not necessary but is included for clarity.
9. The `update()` function is called once each frame. The game is running at 60 frames per second so the function is called at an interval of 1/60 seconds. The argument variable `dt` contains the current interval.
10. If the `moving` flag is true, get the current game object position. The function `go.get_position()` takes an optional argument which is the id of the game object to get the position of. If no argument is given, the current game object position is returned.
11. Add the current direction vector (scaled to speed and frame interval) to the position.
12. Set the position of the game object to the new position.
13. After the calculations have been made, set the input vector to 0 and unset the `moving` flag.
14. The `on_input()` function is called every frame for all mapped input. The argument variable `action_id` contain the action as set up in the input bindings file. The argument variable `action` is a Lua table with details on the input.
15. For each input direction, set the X or the Y component of the `input` vector in `self`. If the user presses the <kbd>up arrow</kbd> and <kbd>left arrow</kbd> keys, the engine will call this function twice and the input vector will be set to `(-1, 1, 0)`.
16. If the user presses any of the arrow keys, the input vector length will be non zero. If so, set the `moving` flag so the player will be moved in `update()`.
17. The `dir` direction vector is set to the normalized value of the input. If the input vector is `(-1, 1, 0)`, for instance, the vector length is greater than 1. Normalizing the vector brings it to a length of exactly 1. Without normalization diagonal movement would be faster than horizontal and vertical. When the engine runs the `update()` function, any user input will have an effect on the `dir` vector which will cause the player to move.

With this piece of Lua code, your game now has a player character that can move around on the screen. The character, however, only plays one single animation in an endless loop. This will be fixed soon, but first we should add the possibility to fire rockets.

## The rocket game object

Consider the main collection for a second. Now it contains two game objects: the map and the player, and that's fine since there is only one map and one player. But rockets will be a different story. They should work like this: whenever the user presses a key, a rocket should fire. For this to work you need a way of creating a new game object for each key press.

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Game object</kbd>. Name this file *rocket.go*. Note that by creating this file, you do not create a game object but a file can be used as a *blueprint* when creating an actual game object.

2. Drag the folder *buildings/turret-rocket* from the asset package to the *main* folder in the *Assets* view.

3. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>New ▸ Animation group</kbd>). Name the animation "rocket".

4. Add the three rocket images to the animation group and set the *Fps* property to a value that makes the animation look good when you preview.

    ![rocket animation](images/war-battles/rocket_animation.png)

5. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add component ▸ Sprite</kbd>.

6. Set the *Image* property of the sprite to "/main/sprites.atlas" and the *Default animation* to "rocket".

Now you have a basic rocket game object blueprint. The next step is to add functionality to spawn game objects based on this blueprint file. For that, you will use a *Factory* component. You also need to add a new input action for the firing mechanic.

## Spawning rockets

1. Open *main.collection* and <kbd>Right click</kbd> on the "player" game object. Select <kbd>Add component ▸ Factory</kbd>.

2. Select the new factory component and set its *Id* property to "rocketfactory" and its *Prototype* to the file "/main/rocket.go" that you created above. Now the player game object is all set.

3. Open the file */input/game.input_binding*.

4. Add a *Key trigger* for the firing action.

    ![input](images/war-battles/input_bindings_fire.png)

5. Open *main/player.script* and add a flag to track if the player is firing in the `init()` function:

    ```lua
    function init(self)
        msg.post("#", "acquire_input_focus")
    
        self.moving = false
        self.firing = false -- <1>
        
        self.input = vmath.vector3()
        self.dir = vmath.vector3(0, 1, 0)
        self.speed = 50
    end
    ```
    1. Whenever the player is firing this value will be set to `true`.

6. Add what should happen when the flag is set in `update()`. The factory should create a new game object instance:

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
    1. If the `firing` flag is true, tell the factory component called "rocketfactory" that you just created to spawn a new game object.
    2. Set the flag to false. This flag will be set in `on_input()` each frame the player presses the fire key.

7. Scroll down to the `on_input()` function. Add a fourth `elseif` for the case where the function is called with the "fire" action:

    ```lua
        ...
        elseif action_id == hash("right") then
            self.input.x = 1
        elseif action_id == hash("fire") and action.pressed then
            self.firing = true
        end
        ...
    ```

If you run the game now you should be able to move around and drop rockets all over the map by hammering the fire key. This is a good start, now you only need to fix three things:

1. When the rocket is spawned, it should be oriented in the player's direction and it should move straight ahead.
2. The rocket should explode after a second or so.

Let's do these things one by one:

## Setting the direction of the rocket

1. Open *main/player.script* and scroll down to the `on_input()` function.

    ```lua
        ...
        elseif action_id == hash("right") then
            self.input.x = 1
        elseif action_id == hash("fire") and action.pressed then
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
    3. Add explicit position (`nil`, the rocket will spawn at the player's position), rotation (the calculated quaternion) and spawn property values.

    Note that the rocket needs a movement direction in addition to the game object rotation (`rot`). It would be possible to make the rocket calculate its movement vector based on its rotation, but it is easier and more flexible to separate the two values. For instance, with a separate rotation it is possible to add rotation wobble to the rocket without it affecting the movement direction.

3.  <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Script</kbd>. Name the new script file "rocket.script". Replace the code of the file with the following:

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
    1. Define a new script property named `dir` and initialize the property with a default empty vector (`vmath.vector3()`). The default value can be overrided by passing values to the `factory.create()` function. The current property value is accessed as `self.dir`.
    2. A rocket speed value, expressed in pixels per second.
    3. Get the current rocket position.
    4. Calculate a new position based on the old position, the movement direction (unit vector) and the speed.
    5. Set the new position.

4. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add component ▸ Script</kbd>. Select "rocket.script" for the component.

5. Run the game and try the new mechanic. Notice that the rockets fly in the right direction but are oriented 180 degrees wrong.

    ![fire rockets](images/war-battles/fire_rockets.png)

6. Open *sprites.atlas*, select the "rocket" animation and click the *Flip horizontal* property.

    ![flip rocket](images/war-battles/flip_rocket.png)

7. Run the game again to verify that everything looks ok.

    ![fire rockets](images/war-battles/fire_rocket_2.png)

Now you only need to make the rockets explode.

## Explosions

1. Drag the folder *fx/explosion* from the asset package to the main folder in the Assets view.

2. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>New ▸ Animation group</kbd>). Call the animation "explosion".

3. Add the nine explosion images to the animation group and set the *Fps* property to a value that makes the animation look good when you preview. Also make sure that this animation has the *Playback* property set to `Once Forward`.

    ![explosion animation](images/war-battles/explosion_animation.png)

4. Open *main/rocket.script* and scroll down to the `init()` function and change it to:

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
    2. If the message posted has the hashed name (or id) "animation_done", then. The engine runtime sends back this message when a sprite animation initiated with "play_animation" has finished playing.
    3. When the animation is done, delete the current game object.

Run the game. Now it starts feeling like the embryo for a nice little game, don't you think?

![fire rockets](images/war-battles/fire_rocket_3.png)

But now you need something to fire the rockets at. Enter tanks!

## The tank game object

1. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Game object</kbd>. Name this file *tank.go*. Like the rocket game object, this is a file that can be used as a *blueprint* when creating the actual tank game objects.

2. Drag the folder *units/tank* from the asset package to the *main* folder in the *Assets* view.

3. Open *sprites.atlas* and create a new animation group (right click the root node and select <kbd>New ▸ Animation group</kbd>). Name the animation "tank-down".

4. Add the two downwards facing images (*/main/tank/down/1.png* and */main/tank/down/2.png*) to the animation and set it's *Fps* value to something that looks good.

    ![tank animation](images/war-battles/tank_animation.png)

5. Open *tank.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add component ▸ Sprite</kbd>.

6. Set the *Image* property of the sprite to "/main/sprites.atlas" and the *Default animation* to "tank-down".

7. Open *main.collection*

8. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add Game Object File</kbd>. Select *tank.go* as blueprint for the new game object.

9. Create a few more tanks and position them on the map with the *Move Tool*. Make sure to set the Z position to 1.0 so they are rendered on top of the map.

    ![tanks](images/war-battles/tanks.png)

Run the game and check that the tanks look okay. You will notice that the rockets fly straight through the tanks so the next step is to add collision between the tanks and the rockets. To do this you need to add a new component to the tank and the rocket game object:

## Adding collision objects

1. Open *tank.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add component ▸ Collision Object</kbd>.

2. Set the *Type* property to "Kinematic". This means that the physics engine will not simulate any gravity or collision on this object. Instead it will detect collisions and leave it to you to code the response.

3. Set the *Group* property to "tanks" and *Mask* to "rockets". This causes this game object to detect collisions against object in the group "rockets" that has the mask set to "tanks".

4. <kbd>Right click</kbd> the "collisionobject" component in the *Outline* and select <kbd>Add Shape ▸ Box</kbd>. Set the size of the box shape to match the tank graphics.

    ![tank collision](images/war-battles/tank_collision.png)

6. Open *rocket.go* and <kbd>Right click</kbd> the root in the *Outline* and select <kbd>Add component ▸ Collision Object</kbd>.

7. Set the *Type* property to "Kinematic".

8. Set the *Group* property to "rockets" and *Mask* to "tanks". This causes this game object to detect collisions against object in the group "tanks" that has the mask set to "rockets". Since that is what you set the group and mask to in *tank.go* the rockets and tanks will interact physically.

    ![rocket collision](images/war-battles/rocket_collision.png)

Now the engine will detect when these game objects intersect and send messages to them when that happens. The last piece of the puzzle is an addition to the rocket's script.

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
    1. Since you want the rocket to explode either when the timer runs out (in `update()`) or when the rocket hits a tank (in `on_message()`) you should break out that piece of code to avoid duplication. There are a few options, the easiest is probably to just create a local function. The function is declared `local` meaning it only exist for the rocket script. Therefore it must be placed before it is used, above `update()`, this is how Lua's scoping rules work. Also note that you should pass `self` as a parameter to the function to be able to access `self.life` etc.
    2. The code that used to live here has been moved to the `explode()` function.
    3. The engine sends a message called "collision_response" when the shapes collide, if the group and mask pairing is correct.
    4. Call the `explode()` function if there is a collision.
    5. Finally delete the tank. You get the id of the game object the rocket collided with in the `message.other_id` variable.

And now you can run the game and try to destroy some tanks. The tanks aren't very interesting enemies, but they should nevertheless give you some score.

## Scoring GUI

1. Drag the the file *fonts/04B_03.TTF* from the asset pack folder to the *main* folder in the *Assets* view.

2. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Font</kbd>. Name this file *text.font*.

    ![text font](images/war-battles/text_font.png)

3. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Gui</kbd>. Name this file *ui.gui*. It will contain the user interface where you will place the score counter.

4. Open *ui.gui*. <kbd>Right click</kbd> *Fonts* in the *Outline* view and select <kbd>Add ▸ Fonts</kbd>. Select the */main/text.font* file.

5. <kbd>Right click</kbd> *Nodes* in the *Outline* view and select <kbd>Add ▸ Text</kbd>.

6. Select the new text node in the outline and set its *Id* property to "score", its *Text* property to "SCORE: 0", its *Font* property to the font "text" and its *Pivot* property to "West".

7. Place the text node in the top left corner of the screen.

    ![ui gui](images/war-battles/ui.png)

8. <kbd>Right click</kbd> the folder *main* in the *Assets* view and select <kbd>New ▸ Gui Script</kbd>. Name this file *ui.gui_script*.

9. Go back to *ui.gui* and select the root node in the *Outline*. Set the *Script* property to the file */main/ui.gui_script* that you just created. Now if we add this Gui as a component to a game object the script will run for the component.

10. Open *main.collection*.

11. <kbd>Right click</kbd> the root node of the collection in the *Outline* and select <kbd>Add game object</kbd>.

11. Set the id of the game object to "gui", then <kbd>Right click</kbd> it and select <kbd>Add Component File</kbd>. Select the file */main/ui.gui*.

    ![main gui](images/war-battles/main_gui.png)

Now there is a score counter on screen. You only need to add functionality in the Gui script so the score can be updated.

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

3. Open *rocket.script* and scroll down to the `on_message()` function where you need to add a line of code:

    ```lua
    function on_message(self, message_id, message, sender)
        if message_id == hash("animation_done") then
            go.delete()
        elseif message_id == hash("collision_response") then
            explode(self)
            go.delete(message.other_id)
            msg.post("/gui#gui", "add_score", {score = 100}) -- <1>
        end
    end
    ```
    1. Post a message named "add_score" to the component "gui" in the game object named "gui" at the root of the main collection. Pass along a table where the entry `score` has been set to 100.

4. Try the game!

![done](images/war-battles/done.png)

Well done! We hope you enjoyed this tutorial and that it was helpful.

## What next?

To get to know Defold better, we suggest that you to continue working with this little game. Here are a few good exercises:

1. Add directional animations for the player character. Tip, add a function called `update_animation(self)` to the `update()` function and change the animation depending on the value of the `self.dir` vector. It is also worth remembering that if you send a "play_animation" message each frame to a sprite, the animation will restart from the beginning, each frame---so you should only send "play_animation" when the animation should change.

2. Add an "idle" state to the player character so it only plays a walking animation when moving.

3. Make the tanks spawn dynamically. Look at how the rockets are spawned and do a similar setup for the tanks. You might want to create a new game object in the main collection with a script that controls the tank spawning.

4. Make the tanks patrol the map. One simple option is to have the tank pick a random point on the map and move towards that point. When it is within a short distance of the point, it picks a new point.

5. Make the tanks chase the player. One option is to add a new collision object to the tank with a spherical shape. If the player collides with the collision object, have the tank drive towards the player.

6. Make the tanks fire at the player.

7. Add sound effects.

If you are stuck, please head over to the [Defold Forum](//forum.defold.com) where you can talk to the Defold developers and many friendly users.