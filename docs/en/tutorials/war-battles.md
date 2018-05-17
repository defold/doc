---
title: War battles tutorial
brief: In this tutorial you will create the embryo of a small shooter game. This is a good starting point if you are new to Defold.
github: https://github.com/defold/tutorial-war-battles
---

# War battles tutorial

In this tutorial you will learn how to create a small playable game featuring movement and firing mechanics.

The tutorial is integrated with the Defold editor and easily accessible:

1. Start Defold.
2. Select *New Project* on the left.
3. Select the *From Tutorial* tab.
4. Select the "War battles tutorial"
5. Select a location for the project on your local drive and click *Create New Project*.

![new project](images/new-war-battles.png){srcset="images/new-war-battles@2x.png 2x"}

The editor automatically opens the "README" file from the project root, containing the full tutorial text.

![icon](images/icon-tutorial.svg){style="display:inline;margin:0 0.5rem 0 0;vertical-align: middle;"}
[You can also read the full tutorial text on Github](https://github.com/defold/tutorial-war-battles)

To get an idea about what you are about to build, you can try the game here. Move with the <kbd>arrow buttons</kbd> and fire with <kbd>space</kbd>.

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

If you get stuck, head over to the [Defold Forum](//forum.defold.com) where you will get help from the Defold team and many friendly users.

Happy Defolding!
