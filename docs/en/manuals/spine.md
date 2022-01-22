---
title: Spine bone animation in Defold
brief: This manual explains how to bring Spine animations from _Spine_ or _Dragon Bone_ into Defold.
---

# Spine animation

_Spine_ is a third party animation tool by Esoteric Software. Spine animation provides 2D _skeletal animation_ support (see http://en.wikipedia.org/wiki/Skeletal_animation). This is a fundamentally different technique from [flipbook animations](/manuals/flipbook-animation) that is closer to cutout animation. In cutout animation separate pieces of the animated object (e.g body parts, eyes, mouth etc) are moved individually between each frame. Spine animation let you build an invisible, virtual skeleton consisting of a hierarchy of interconnected _bones_. This skeleton, or _rig_, is then animated and individual images are attached to the bones. Defold supports animations created or exported in the [Spine JSON format](http://esotericsoftware.com/spine-json-format). Skeletal animation is very smooth since the engine can interpolate the location of each bone for each frame. It is particularly useful to animate characters and animals, but works very well for other types of objects, like ropes, vehicles or foliage.

  ![Spine animation](images/animation/spine_animation.png){.inline}
  ![Run loop](images/animation/frog_runloop.gif){.inline}

Defold implements runtime evaluation and animation expressed in the [Spine JSON format](http://esotericsoftware.com/spine-json-format).

Defold supports most of Spine's animation features, including inverse kinematics (IK).

::: important
Currently, Defold does not support animation keys that flip bones over the X or Y axis. Defold supports mesh animation but only with bones, meaning that you can't animate single vertices. If you need to animate single vertices you can do that through a bone being 100% bound to that vertex only and animate the bone.
:::

::: important
The Spine runtime implementation in Defold supports all Spine 2.x features. The runtime provides only limited additional support for Spine 3.x features. Make sure to use only Spine 2.x features to ensure compatibility with the Defold runtime!
:::

## Concepts

*Spine JSON data file*
: This data file contains the skeleton, all the image slot names, skins and the actual animation data. No images are embedded in this file though. Create this file from your animation software of choice.

*Spine scene*
: The Defold resource tying together the Spine JSON data file and the Defold image atlas file that is used to fill bone slots with graphics.

*Spine model*
: The _SpineModel_ component is put in a game object to bring the graphics and animation to the screen. The component contains the skeleton game object hierarchy, which animation to play, what skin to use and it also specifies the material used for rendering the model. See [SpineModel documentation](/manuals/spinemodel) for details.

*Spine Node*
: If using Spine animation in a GUI scene, use Spine GUI nodes instead of Spine model components. See the [GUI spine documentation](/manuals/gui-spine) for details.

## Animation tools

The Spine JSON data format that Defold supports can be created by Esoteric Software's _Spine_ software. In addition, _Dragon Bones_ has the ability to export Spine JSON data files.

_Spine_ is available from http://esotericsoftware.com

![Spine](images/spine/spine.png)

_Dragon Bones_ is available from http://dragonbones.com

![Dragon Bones](images/spine/dragonbones.png)

::: important
_Dragon Bones_ should typically be able to export to Spine JSON data files without any problems. If your _Dragon Bones_ exported data file isn't rendered properly in Defold we recommend that you use the official [Spine Skeleton Viewer](http://esotericsoftware.com/spine-skeleton-viewer) to first verify that the data can be correctly parsed. If there is a problem with the exported data the Spine Skeleton Viewer can pinpoint problems in the JSON data file, for instance missing or incorrect fields.
:::


## Importing a Spine character and animations

When you have a model and animations that you have created in Spine, the process of importing them into Defold is straightforward:

- Add a project dependency for https://github.com/defold/extension-spine
- Export a Spine JSON version of the animation data.
- Put the exported JSON file somewhere in your project hierarchy.
- Put all images associated with the model somewhere in your project hierarchy.
- Create an _Atlas_ file and add all the images to it. (See [2D graphics documentation](/manuals/2dgraphics) for details on how to create an atlas and below for some caveats)

![Export JSON from Spine](images/spine/spine_json_export.png)

If you work in _Dragon Bones_, simply select *Spine* as your output data type. Also select *Images* as image type. This will export a *.json* file and all necessary images into a folder. Then add those to Defold as described above.

![Export JSON from Dragon Bones](images/spine/dragonbones_json_export.png)

When you have the animation data and image files imported and set up in Defold, you need to create a _Spine scene_ resource file:

- Create a new _Spine scene_ resource file (Select <kbd>New ▸ Spine Scene File</kbd> from the main menu)
- The new file opens in the spine scene editor.
- Set the *Properties*.

![Setup the Spine Scene](images/spine/spinescene.png){srcset="images/spine/spinescene@2x.png 2x"}

Spine Json
: The Spine JSON file to use as source for bone and animation data.

Atlas
: The atlas containing images named corresponding to the Spine data file.

## Creating SpineModel components

When you have all data imported and your _Spine scene_ resource file ready, you can create SpineModel components. See [SpineModel documentation](/manuals/spinemodel) for details.

## Creating Spine GUI nodes

You can also use Spine animations in GUI scenes. See the [GUI spine documentation](/manuals/gui-spine) for details.

## Playing animations

To run animations on your model, simply call the [`spine.play_anim()`](/ref/spine#spine.play_anim) function:

```lua
function init(self)
    -- Play the "walk" animation on component "spinemodel" and blend against previous
    -- animation for the first 0.1 seconds
    local anim_props = { blend_duration = 0.1 }
    spine.play_anim("#spinemodel", "run", go.PLAYBACK_LOOP_FORWARD, anim_props)
end
```

![Spine model in game](images/animation/spine_ingame.png){srcset="images/animation/spine_ingame@2x.png 2x"}

If an animation is played with any of the `go.PLAYBACK_ONCE_*` modes and you have provided a callback function to `spine.play_anim()` the callback is run on animation complete. See below for information on callbacks.

### Cursor animation

In addition to using the `spine.play_anim()` to advance a spine animation, *Spine Model* components expose a "cursor" property that can be manipulated with `go.animate()` (more about [property animations](/manuals/property-animation)):

```lua
-- Set the animation on the spine model but don't run it.
spine.play_anim("#spinemodel", "run_right", go.PLAYBACK_NONE)

-- Set the cursor to position 0
go.set("#spinemodel", "cursor", 0)

-- Tween the cursor slowly between 0 and 1 pingpong with in-out quad easing.
go.animate("#spinemodel", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 6)
```

::: important
When tweening or setting the cursor, timeline events may not fire as expected.
:::

### The bone hierarchy

The individual bones in the Spine skeleton are represented internally as game objects. In the *Outline* view of the Spine model component, the full hierarchy is visible. You can see each bone's name and its place in the skeleton hierarchy.

![Spine model hierarchy](images/animation/spine_bones.png){srcset="images/animation/spine_bones@2x.png 2x"}

With the bone name at hand, you are able to retrieve the instance id of the bone in runtime. The function [`spine.get_go()`](/ref/spine#spine.get_go) returns the id of the specified bone and you can, for instance, child other game objects under the animated game object:

```lua
-- Attach pistol game object to the hand of the heroine
local hand = spine.get_go("heroine#spinemodel", "front_hand")
msg.post("pistol", "set_parent", { parent_id = hand })
```

### Timeline events

Spine animations can trigger timed events by sending messages at precise moments. They are very useful for events that should take place in sync with your animation, like playing footstep sounds, spawning particle effects, attaching or detaching objects to the bone hierarchy or anything else you would like to happen.

Events are added in the Spine software and are visualized on the playback timeline:

![Spine events](images/animation/spine_events.png)

Each event is referenced with a name identifier ("bump" in the example above) and each event instance on the timeline can contain additional information:

Integer
: A numerical value expressed as an integer.

Float
: A floating point numerical value.

String
: A string value.

When the animation plays and events are encountered, `spine_event` messages are sent back to the script component that called `spine.play()`. The message data contains the custom numbers and strings embedded in the event, as well as a few additional fields that are sometimes useful:

`t`
: The number of seconds passed since the first frame of the animation.

`animation_id`
: The animation name, hashed.

`string`
: The provided string value, hashed.

`float`
: The provided floating point numerical value.

`integer`
: The provided integer numerical value.

`event_id`
: The event identifier, hashed.

`blend_weight`
: How much of the animation is blended in at this point. 0 means that nothing of the current animation is part of the blend yet, 1 means that the blend consists of the current animation to 100%.

```lua
-- Spine animation contains events that are used to play sounds in sync with the animation.
-- These arrive here as messages.
function on_message(self, message_id, message, sender)
  if message_id == hash("spine_event") and message.event_id == hash("play_sound") then
    -- Play animation sound. The custom event data contains the sound component and the gain.
    local url = msg.url("sounds")
    url.fragment = message.string
    sound.play(url, { gain = message.float })
  end
end
```

## Completion callbacks

The spine animation function `spine.play_anim()` support an optional Lua callback function as the last argument. This function will be called when the animation has played to the end. The function is never called for looping animations, nor when an animation is manually canceled via `spine.cancel()`. The callback can be used to trigger events on animation completion or to chain multiple animations together.

```lua
local function anim_done(self)
    -- the animation is done, do something useful...
end

function init(self)
    -- Play the "walk" animation on component "spinemodel" and blend against previous
    -- animation for the first 0.1 seconds, then call callback.
    local anim_props = { blend_duration = 0.1 }
    spine.play_anim("#spinemodel", "run", go.PLAYBACK_LOOP_FORWARD, anim_props, anim_done)
end
```

## Playback Modes

Animations can be played either once or in a loop. How the animation plays is determined by the playback mode:

* go.PLAYBACK_NONE
* go.PLAYBACK_ONCE_FORWARD
* go.PLAYBACK_ONCE_BACKWARD
* go.PLAYBACK_ONCE_PINGPONG
* go.PLAYBACK_LOOP_FORWARD
* go.PLAYBACK_LOOP_BACKWARD
* go.PLAYBACK_LOOP_PINGPONG

The pingpong modes run the animation first forward, then backward.

## Atlas caveats

The animation data references the images used for the bones by name with the file suffix stripped off. You add images to your Spine project in the Spine software and they are listed in the hierarchy under *Images*:

![Spine images hierarchy](images/spine/spine_images.png)

This example shows files laid out in a flat structure. It is, however, possible to organize the files in subfolders and the file references will reflect that. For instance, a file *head_parts/eyes.png* on disk will be referenced as *head_parts/eyes* when you use it in a slot. This is also the name used in the exported JSON file so when creating the Defold image atlas, all names must match an atlas animation.

If you select <kbd>Add Images</kbd> Defold will automatically create animation groups with the same name as the added files, but with the file suffix stripped off. So, after having added the file *eyes.png* its animation group can be referenced by the name "eyes". This works with file names only, not paths.

So what do you do if your animation references "head_parts/eyes"? The easiest way to accomplish a match is to add an animation group (right click the root node in the Atlas *Outline* view and select *Add Animation Group*). You can then name that group "head_parts/eyes" (it's just a name, not a path and `/` characters are legal) and then add the file "eyes.png" to the group.

![Atlas path names](images/spine/atlas_names.png){srcset="images/spine/atlas_names@2x.png 2x"}

Moving on to animate your Spine model, please read the [Animation documentation](/manuals/animation).
