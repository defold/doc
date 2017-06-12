---
title: Defold project settings
brief: This manual describes how project specific settings work in Defold.
---

# Project settings

The file *game.project* contains all project wide settings. It must stay in the root folder of the project and must be named *game.project*. The first thing the engine does when starting up and launching your game is look for this file.

Every setting in the file belongs to a category. The format of the file is simple text and can be edited by any standard text editor. The format looks like this:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

A real example is:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

which means that the setting *main_collection* belongs to the *bootstrap* category.
Whenever a file reference is used, like the example above, the path needs to be appended with a 'c' character, which means you're referencing the compiled version of the file.
Also note that the folder containing *game.project* will be the project root, which is why there is an initial '/' in the setting path.

Below are all the available settings, arranged by section. Some settings are not yet exposed in the settings editor (these are marked "hidden setting" below), but can be set manually by right clicking "game.project" and selecting <kbd>Open With ▸ Text Editor</kbd>.

## Setting config values on engine startup

When the engine starts, it is possible to provide config values from the command line that override the *game.project* settings:

```bash
# Specify a bootstap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set the custom value "test.my_value"
$ dmengine --config=test.my_value=4711
```

Custom values can---just like any other config value---be read with [`sys.get_config()`](/ref/sys/#sys.get_config).

## Project

title
: The title of the application.

version
: The version of the application.

write_log
: When checked, the engine will write a log file *log.txt* in the project root. When running on iOS, the log file can be accessed through iTunes and the *Apps* tab and the *File Sharing* section. On Android, the file is stored in the app's external storage. When running the *dmengine* development app, you can view the log with:

```bash
$ adb shell cat /mnt/sdcard/Android/data/com.defold.dmengine/files/log.txt
```

compress_archive
: Enables compression of archives when bundling. Note that this currently applies to all platforms except Android where the apk already contains all data compressed.

dependencies
: A comma-separated list of URLs to the project *Library URL*s (can be found in the [Defold dashboard](//dashboard.defold.com)) that this project uses. Note that you need to be a member of the dependent projects.

custom_resources (hidden setting)
: A comma separated list of resources that will be included in the project. If directories are specified, all files and directories in that directory are recursively included.

bundle_resources (hidden setting)
: A directory containing resource files and folders that should be copied as-is into the resulting package when bundling. The directory is specified with an absolute path from the project root, for example `/res`. The resource directory must contain subfolders named by `platform`, or `architecure-platform`. Supported platforms are `ios`, `android`, `osx` and `web`. Supported arc-platform pairs are `armv7-ios`, `arm64-ios`, `armv7-android`, `x86_64-osx` and `js-web`. A subfolder named `common` is also allowed, containing resource files common for all platforms.

bundle_exclude_resources (hidden setting)
: A comma separated list of resources that should not be included in the bundle.

## Bootstrap

main_collection
: File reference of the collection to use for starting the application, `/logic/main.collectionc` by default.

render
: Which render file to use, which defines the render pipeline, `/builtins/render/default.renderc` by default.

## Library

include_dirs
: A space separated list of directories that should be shared from your project via library sharing.

## Script

shared_state
: Check to share a single Lua state between all script types, checked by default.

## Tracking

app_id
: A unique tracking ID for this project. The project tracking ID an be found on the project dashboard.

## Display

width
: The width in pixels of the application window, `960` by default.

height
: The height in pixels of the application window, `640` by default.

high_dpi
: Creates a high dpi back buffer on displays that support it. I.e. the game will render in higher resolution.

samples
: How many samples to use for super sampling anti-aliasing, `0` by default, which means it is turned off.

fullscreen
: Check if the application should start full screen. If unchecked, the application runs windowed.

update_frequency
: Frame update frequency, `60` by default. Valid values are `60`, `30`, `20`, `15`, `12`, `10`, `6`, `5`, `4`, `3`, `2` or `1`.

variable_dt
: Check if time step should be measured against actual time or be fixed (set to *update_frequency*).

display_profiles
: Specifies which display profiles file to use, `/builtins/render/default.display_profilesc` by default.

dynamic_orientation
: Check if the app should dynamically switch between portrait and landscape on device rotation. Note that the development app does not currently respect this setting.

## Physics

type
: Which type of physics to use, `2D` (default) or `3D`.

gravity_y
: World gravity along y-axis, `-10` by default (natural gravity)

debug
: Check if physics should be visualized for debugging.

debug_alpha
: Alpha component value for visualized physics, `0`--`1`. The value is `0.9` by default.

world_count
: Max number of concurrent physics worlds, `4` by default (careful, they waste memory).

gravity_x
: World gravity along x-axis, `0` by default.

gravity_z
: World gravity along z-axis, `0` by default.

scale
: How to scale the physics worlds in relation to the game world for numerical precision, `0.01`--`1`. The value is `0.02` by default, meaning that the physics engine will see 160 units as 3.2 meters.

debug_scale
: How big to draw unit objects in physics, like triads and normals, `30` by default.

max_collisions
: How many collisions that will be reported back to the scripts, `64` by default.

max_contacts
: How many contact points that will be reported back to the scripts, `128` by default.

contact_impulse_limit
: Ignore contact impulses with values less than this setting, `0` by default.

## Graphics

default_texture_min_filter
: Specifies which filtering to use for min filtering, `linear` (default) or `nearest`.

default_texture_mag_filter
: Specifies which filtering to use for mag filtering, `linear` (default) or `nearest`.

max_debug_vertices
: The maximum number of debug vertices. Used for physics shape rendering among other things, `10000` by default.

texture_profiles
: The texture profiles file to use for this project, `/builtins/graphics/default.texture_profiles` by default.

## Input

repeat_delay
: Seconds to wait before a held down input should start repeating itself, `0.5` by default.

repeat_interval
: Seconds to wait between each repetition of a held down input, `0.2` by default.

gamepads
: File reference of the gamepads config file, which maps gamepad signals to OS, `/builtins/input/default.gamepadsc` by default.

game_binding
: File reference of the input config file, which maps hardware inputs to actions, `/input/game.input_bindingc` by default.

## Resource

http_cache
: Check if the HTTP cache should be enabled for faster loads over network.

uri
: Where to find the project build data, in URI format.

max_resources
: The max number of resources that can be loaded at the same time, `1024` by default.

## Network

http_timeout
: The HTTP timeout in seconds. Set to `0` to disable timeout, which is the default.

## Collection

max_instances
: Max number of game object instances in a collection, `1024` by default.

## Sound

gain
: Global gain (volume), `0`--`1`, The value is `1` by default.

max_sound_data
: Max number of different sounds, `128` by default.

max_sound_buffers
: Max number of concurrent sound buffers, `32` by default.

max_sound_sources
: Max number of concurrently playing sounds, `16` by default.

max_sound_instances
: Max number of concurrent sound instances, `256` by default.

## Sprite

max_count
: Max number of sprites, `128` by default.

subpixels
: Check to allow sprites to appear unaligned with respect to pixels, checked by default.

## Spine

max_count
: Max number of spine models, `128` by default.

## GUI

max_count
: Max number of GUI components, `64` by default.

## Label

max_count
: Max number of labels, `64` by default.

sub_pixels
: Check to allow lables to appear unaligned with respect to pixels, checked by default.

## Particle FX

max_emitter_count
: The max number of concurrent emitters, `64` by default.

max_particle_count
: The max number of concurrent particles, `1024` by default.

## Collection proxy

max_count
: Max number of collection proxies, `8` by default.

## Collection factory

max_count
: Max number of collection factories, `128` by default.

## Factory

max_count
: Max number of game object factories, `128` by default.

## iOS

app_icon_WxH
: Image file to use as application icon at given width and height dimensions `W` &times; `H`.

launch_image_WxH
: Image file to use as application launch image for resolution width and height dimensions `W` &times; `H`. Note that iOS selects the display resolution based on the launch image.

pre_rendered_icons
: (iOS 6 and earlier) Check if your icons are pre-rendered. If this is unchecked the icons will get a glossy highlight added automatically.

bundle_identifier
: The bundle identifier lets iOS recognize any updates to your app. Your bundle ID must be registered with Apple and be unique to your app. You cannot use the same identifier for both iOS and OS X apps.

infoplist
: If specified, use this info.plist file when bundling your app.

## Android

app_icon_WxH
: Image file to use as application icon at given width and height dimensions `W` &times; `H`.

version_code
: An integer value indicating the version of the app. Increase the value for each subsequent update.

push_icon_SIZE
: Image files to be used as custom push notification icon on Android. The icons will automatically be used for both local or remote push notifications. If not set the application icon will be used by default.

push_field_title
: Specifies which payload JSON field should be used as notification title. Leaving this setting empty makes the pushes default to the application name as title.

push_field_text
: Specifies which payload JSON field should be used as notification text. If left empty, the text in the field `alert` is used, just as on iOS.

package
: Package identifier.

gcm_sender_id
: Google Cloud Messaging Sender Id. Set this to the string assigned by Google to enable push notifications.

manifest
: If set, use the specified Android manifest XML file when bundling.

iap_provider
: Specifies which store to use. Valid options are `Amazon` and `GooglePlay`, `GooglePlay` by default.

input_method
: Specifies which method to use to get keyboard input on Android devices. Valid options are `KeyEvent` (old method) and `HiddenInputField` (new). `KeyEvent` by default.

## OS X

app_icon
: Image file to use as application icon on OS X.

infoplist
: If set, use the specified info.plist file when bundling.

bundle_identifier
: The bundle identifier lets OS X recognize updates to your app. Your bundle ID must be registered with Apple and be unique to your app. You cannot use the same identifier for both iOS and OS X apps.

## Windows

app_icon
: Image file to use as application icon on Windows.

## HTML5

set_custom_heap_size
: If set, Emscripten allocates *custom_heap_size* number of bytes for the application heap.

custom_heap_size
: Sets the custom heap size for Emscripten to use if *set_custom_heap_size* is set. If not set, 256MB is allocated for the application heap.

include_dev_tool
: Includes a visual dev-tool in the application that allows tracking of memory usage.

htmlfile
: If set, use the specified template HTML file when bundling.

cssfile
: If set, use the specified CSS file when bundling.

splash_image
: If set, use the specified splash image on startup when bundling.

archive_location_prefix
: When bundling for HTML5 game data is split up into one or more archive data files. When the engine starts the game, these archive files are read into memory. Use this setting to specify the location of the data, `archive` by default.

archive_location_suffix
: Suffix to be appended to the archive files. Useful to, for instance, force non-cached content from a CDN (`?version2` for example).

## Facebook

appid (hidden setting)
: The application id as issued by Facebook.

## IAP

auto_finish_transactions
: Check to automatically finish IAP transactions. If unchecked, you need to explicitly call `iap.finish()` after a successful transaction, checked by default.



