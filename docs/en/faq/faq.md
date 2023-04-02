---
title: Defold engine and editor FAQ
brief: Frequently asked questions about the Defold game engine, editor and platform.
---

# Frequently asked questions

## General questions

#### Q: Is Defold really free?

A: Yes, the Defold engine and editor with full functionality is completely free of charge. No hidden costs, fees or royalties. Just free.


#### Q: Why on earth would the Defold Foundation give Defold away?

A: One of the objectives of the [Defold Foundation](/foundation) is to make sure that the Defold software is available to developers world-wide and that the source code is available free of charge.


#### Q: How long will you support Defold?

A: We are deeply committed to Defold. The [Defold Foundation](/foundation) has been set up in such a way that it is guaranteed to exist as a responsible owner for Defold for many years to come. It is not going away.


#### Q: Can I trust Defold for professional development?

A: Absolutely. Defold is used by a growing number of professional game developers and game studios. Check out the [games showcase](/showcase) for examples of games created using Defold.


#### Q: What kind of user tracking are you doing?

A: We log anonymous usage data from our websites and the Defold editor in order to improve our services and product. There is no user tracking in the games you create (unless you add an analytics service yourself). Read more about this in our [Privacy Policy](/privacy-policy).


#### Q: Who made Defold?

A: Defold was created by Ragnar Svensson and Christian Murray. They started working on the engine, editor and servers in 2009. King and Defold started a partnership in 2013 and King acquired Defold in 2014. Read the full story [here](/about).


#### Q: Can I do 3D games in Defold?

A: Absolutely! The engine is a full blown 3D engine. However, the toolset is made for 2D so you will have to do a lot of heavy lifting yourself. Better 3D support is planned.


#### Q: What programming language do I work with in Defold?

A: Game logic in your Defold project is primarily written using the Lua language (specifically Lua 5.1/LuaJIT, refer to the [Lua manual](/manuals/lua) for details). Lua is a lightweight dynamic language that is fast and very powerful. You can also use native code (C/C++, Objective-C, Java and JavaScript depending on the platform) to extend the Defold engine with new functionality. When building custom materials, OpenGL ES SL shader language is used to write vertex and fragment
shaders.


## Platform questions

#### Q: What platforms does Defold run on?

A: The following platforms are supported for the editor/tools and the engine runtime:

  | System                     | Supported            |
  | -------------------------- | -------------------- |
  | macOS 11 Big Sur           | Editor               |
  | macOS 10.13 High Sierra    | Runtime              |
  | Windows Vista              | Editor and runtime   |
  | Ubuntu 18.04 (64 bit)(1)   | Editor               |
  | Linux (64 bit)(2)          | Runtime              |
  | iOS 11.0                   | Runtime              |
  | Android 4.4 (API level 19) | Runtime              |
  | HTML5                      | Runtime              |

  (1 The editor is built and tested for 64-bit Ubuntu 18.04. It should work on other distributions as well but we give no guarantees.)

  (2 The engine runtime should run on most 64-bit Linux distributions as long as graphics drivers are up to date, see below for more information on graphics APIs)


#### Q: What target platforms can I develop games for with Defold?

A: With one click you can publish to Nintendo Switch, iOS, Android and HTML5 as well as macOS, Windows and Linux. It’s truly one codebase with multiple supported platforms.


#### Q: What rendering API does Defold rely on?

A: As a developer you only have to worry about a single render API using a [fully scriptable rendering pipeline](/manuals/render/). The Defold render script API translates render operations into the following graphics APIs:

:[Graphics API](../shared/graphics-api.md)

#### Q: Is there a way to know what version I'm running?

A: Yes, select the "About" option in the Help menu. The popup clearly shows Defold beta version and, more importantly, the specific release SHA1. For runtime version lookup, use [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

The latest beta version available for download from http://d.defold.com/beta can be checked by opening http://d.defold.com/beta/info.json (the same file exists for stable versions as well: http://d.defold.com/stable/info.json)


#### Q: Is there a way to know what platform the game is running on at runtime?

A: Yes, check out [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info).


## Editor Questions
:[Editor FAQ](../shared/editor-faq.md)


## Linux Questions
:[Linux FAQ](../shared/linux-faq.md)


## Android Questions
:[Android FAQ](../shared/android-faq.md)


## HTML5 Questions
:[HTML5 FAQ](../shared/html5-faq.md)


## IOS Questions
:[iOS FAQ](../shared/ios-faq.md)


## Windows Questions
:[Windows FAQ](../shared/windows-faq.md)


## Console Questions
:[Consoles FAQ](../shared/consoles-faq.md)


## Publishing games

#### Q: I'm trying to publish my game to AppStore. How should I respond to IDFA?

A: When submitting, Apple has three checkboxes for their three valid use cases for the IDFA:

  1. Serve ads within the app
  2. Install attribution from ads
  3. User action attribution from ads

  If you check option 1, the app reviewer will look for ads to show up in the app. If your game does not show ads, the game might get rejected. Defold itself doesn't use AD id.


#### Q: How do I monetize my game?

A: Defold has support for in-app purchases and various advertising solutions. Check the [Monetization category in the Asset Portal](https://defold.com/tags/stars/monetization/) for an up to date list of available monetization options.


## Errors using Defold

#### Q: I can't start the game and there is no build error. What's wrong?

A: The build process can fail to rebuild files in rare cases where it have previously encountered build errors that you have fixed. Force a full rebuild by selecting *Project > Rebuild And Launch* from the menu.



## Game content

#### Q: Does Defold support prefabs?

A: Yes, it does. They are called [collections](/manuals/building-blocks/#collections). They allow you to create complex game object hierarchies and store those as a separate building blocks that you can instance in the editor or at runtime (through collection spawning). For GUI nodes there is support for GUI templates.


#### Q: I can't add a game object as a child to another game object, why?

A: Chances are that you try to add a child in the game object file and that is not possible. To understand why, you have to remember that parent-child hierarchies are strictly a _scene-graph_ transform hierarchy. A game object that has not been placed (or spawned) into a scene (collection) is not part of a scene-graph and can't therefore be part of a scene-graph hierarchy.


#### Q: Why can't I broadcast messages to all children of a game object?

A: Parent-child relations express nothing else than the scene-graph transform relations and should not be mistaken for object orientation aggregates. If you try to focus on your game data and how to best transform it as your game alter its state you will likely find less need to send messages with state data to many objects all the time. In the cases where you will need data hierarchies, these are easily constructed and handled in Lua.


#### Q: Why am I experiencing visual artifacts around the edges of my sprites?

A: That is a visual artifact called "edge bleeding" where the edge pixels of neighboring pixels in an atlas bleed into the image assigned to your sprite. The solution is to pad the edge of your atlas images with extra row(s) and column(s) of identical pixels. Luckily this can be done automatically by the atlas editor in Defold. Open your atlas and set the *Extrude Borders* value to 1.


#### Q: Can I tint my sprites or make them transparent, or do I have to write my own shader for it?

A: The built-in sprite shader that is used by default for all sprites has a constant "tint" defined:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: If I set the z coordinate of a sprite to 100 then it's not rendered. Why?

A: The Z-position of a game object controls rendering order. Low values are drawn before higher values. In the default render script game objects with a depth ranging between -1 and 1 are drawn, anything lower or higher will not be drawn. You can read more about the rendering script in the official [Render documentation](/manuals/render). On GUI nodes the Z value is ignored and does not affect rendering order at all. Instead nodes are rendered in the order they are listed and according to child hierarchies (and layering). Read more about gui rendering and draw call optimization using layers in the official [GUI documentation](/manuals/gui).


#### Q: Would changing the view projection Z-range to -100 to 100 impact performance?

A: No. The only effect is precision. The z-buffer is logarithmic and have very fine resolution of z values close to 0 and less resolution far away from 0. For instance, with a 24 bit buffer the values 10.0 and 10.000005 can be differentiated whereas 10000 and 10005 cannot.


#### Q: There is no consistency to how angles are represented, why?

A: Actually there is consistency. Angles are expressed as degrees everywhere in the editor and the game APIs. The math libs use radians. Currently the convention breaks for the `angular_velocity` physics property that is currently expressed as radians/s. That is expected to change.


#### Q: When creating a GUI box-node with only color (no texture), how will it be rendered?

A: It is just a vertex colored shape. Bear in mind that it will still cost fill-rate.


#### Q: If I change assets on the fly, will the engine automatically unload them?

A: All resources are ref-counted internally. As soon as the ref-count is zero the resource is released.


#### Q: Is it possible to play audio without the use of an audio component attached to a game object?

A: Everything is component-based. It's possible to create a headless game object with multiple sounds and play sounds by sending messages to the sound-controller object.


#### Q: Is it possible to change the audio file associated with an audio component at run time?

A: In general all resources are statically declared with the benefit that you get resource management for free. You can use [resource properties](/manuals/script-properties/#resource-properties) to change which resource that is assigned to a component.


#### Q: Is there a way to access the physics collision shape properties?

A: No, it is currently not possible.


#### Q: Is there any quick way to render the collision objects in my scene? (like Box2D's debugdraw)

A: Yes, set *physics.debug* flag in *game.project*. (Refer to the official [Project settings documentation](/manuals/project-settings/#debug))


#### Q: What are the performance costs of having many contacts/collisions?

A: Defold runs a modified version of Box2D in the background and the performance cost should be quite similar. You can always see how much time the engine spends on physics by bringing up the [profiler](/manuals/debugging). You should also consider what kind of collisions objects you use. Static objects are cheaper performance wise for instance. Refer to the official [Physics documentation](/manuals/physics) in Defold for more details.


#### Q: What's the performance impact of having many particle effect components?

A: It depends on if they are playing or not. A ParticleFx that isn't playing have zero performance cost. The performance implication of a playing ParticleFx must be evaluated using the profiler since its impact depends on how it is configured. As with most other things the memory is allocated up front for the number of ParticleFx defined as max_count in game.project.


#### Q: How do I receive input to a game object inside a collection loaded via a collection proxy?

A: Each proxy loaded collection has their own input stack. Input is routed from the main collection input stack via the proxy component to the objects in the collection. This means that it's not enough for the game object in the loaded collection to acquire input focus, the game object that _holds_ the proxy component need to acquire input focus as well. See the [Input documentation](/manuals/input) for details.


#### Q: Can I use string type script properties?

A: No. Defold supports properties of [hash](/ref/builtins#hash) types. These can be used to indicate types, state identifiers or keys of any kind. Hashes can also be used to store game object id's (paths) although [url](/ref/msg#msg.url) properties are often preferable since the editor automatically populate a drop-down with relevant URLs for you. See the [Script properties documentation](/manuals/script-properties) for details.


#### Q: How do I access the individual cells of a matrix (created using [vmath.matrix4()](/ref/vmath/#vmath.matrix4:m1) or similar)?

A: You access the cells using `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` etc


#### Q: I am getting `Not enough resources to clone the node` when using [gui.clone()](/ref/gui/#gui.clone:node) or [gui.clone_tree()](/ref/gui/#gui.clone_tree:node)

A: Increase the `Max Nodes` value of the gui component. You find this value in the Properties panel when selecting the root of the component in the Outline.


## The forum

#### Q: Can I post a thread where I advertise my work?

A: Of course! We have a special ["Work for hire" category](https://forum.defold.com/c/work-for-hire) for that. We will always encourage everything which benefits the community, and offering your services to the community---for remuneration or not---is a good example of that.


#### Q: I made a thread and added my work—can I add more?

A: In order to reduce bumping of "Work for hire" threads, you may not post more than once per 14 days in your own thread (unless it’s a direct reply to a comment in the thread, in which case you may reply). If you want to add additional work to your thread within the 14-day period, you must edit your existing posts with your added content.


#### Q: Can I use the Work for Hire category to post job offerings?

A: Sure, knock yourselves out! It can be used for offerings as well as requests, e.g. “Programmer looking for 2D pixel artist; I’m rich and I’ll pay you well”.
