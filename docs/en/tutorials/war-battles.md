---
title: War battles tutorial
brief: In this tutorial you will create the embryo of a small shooter game. This is a good starting point if you are new to Defold.
---

# War battles tutorial

This tutorial goes through the steps needed to create a small playable game embryo in Defold. You do not need to have any prior experience with Defold, but if you have done some programming in Lua, Javascript, Python or similar, that will help. To get an idea about what you are about to build, you can try the result here:

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

## New project

The tutorial is integrated with the editor so it is really easy to get going:

1. Start Defold.
2. Select *New Project* on the left.
3. Select the *From Tutorial* tab.
4. Select the "War battles tutorial"
5. Select a location for the project on your local drive and click *Create New Project*.

![create project](images/war-battles/create_project.png)

The editor now automatically opens the "README" file from the project root, containing the full tutorial text.

- If you are new to Defold, check out the [editor introduction](/manuals/editor).
- If you get stuck, please head over to the [Defold Forum](//forum.defold.com) where you can talk to the Defold developers and many friendly users.
- The tutorial is also available on Github: https://github.com/defold/tutorial-war-battles

Happy Defolding!