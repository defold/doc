---
title: Collection proxy manual
brief: This manual explains how to dynamically create new game worlds and switch between them.
---

# Collection proxy

The collection proxy component is used to load and unload new game "worlds" dynamically based on the content of a collection file. They can be used to implement switching between game levels, GUI screens, loading and unloading of narrative "scenes" throughout a level, loading/unloading of mini-games and more.

Defold organizes all game objects in collections. A collection can contain game objects and other collections (i.e. sub-collections). Collection proxies allow you to split your content into separate collections and then dynamically manage the loading and unloading of these collections through scripting.

Collection proxies differ from [collection factory components](/manuals/collection-factory/). A collection factory instanciates the contents of a collection into the current game world. Collection proxies create a new game world in runtime and are thus have different use-cases.

## Creating a collection proxy component

1. Add a collection proxy component to a game object by <kbd>right clicking</kbd> a game object and selecting <kbd>Add Component ▸ Collection Proxy</kbd> from the context menu.

2. Set the *Collection* property to reference a collection that you wish to dynamically load into the runtime at a later point. The reference is static and makes sure that all the content of the referenced collection end up in the final game.

![add proxy component](images/collection-proxy/create_proxy.png){srcset="images/collection-proxy/create_proxy@2x.png 2x"}

(You can exclude the content in the build and download it with code instead by checking the *Exclude* box and using the [Live update feature](/manuals/live-update/).)

## Bootstrap

When the Defold engine starts it loads and instanciates all game objects from a *bootstrap collection* into the runtime. It then initializes and enables the game objects and their components. Which bootstrap collection the engine should use is set in the [project settings](/manuals/project-settings/#main-collection). By convention this collection file is usually named "main.collection".

![bootstrap](images/collection-proxy/bootstrap.png){srcset="images/collection-proxy/bootstrap@2x.png 2x"}

To fit the game objects and their components the engine allocates the memory needed for the whole "game world" into which the contents of the bootstrap collection are instanciated. A separate physics world is also created for any collision objects and physics simulation.

Since script components need to be able to address all objects in the game, even from outside the bootstrap world, it is given a unique name: the *Name* property that you set in the collection file:

![bootstrap](images/collection-proxy/collection_id.png){srcset="images/collection-proxy/collection_id@2x.png 2x"}

If the collection that is loaded contains collection proxy components, the collections that those refer to are *not* loaded automatically. You need to control the loading of these resources through scripts.

## Loading a collection

Dynamically loading a collection via proxy is done by sending a message called `"load"` to the proxy component from a script:

```lua
-- Tell the proxy "myproxy" to start loading.
msg.post("#myproxy", "load")
```

![load](images/collection-proxy/proxy_load.png){srcset="images/collection-proxy/proxy_load@2x.png 2x"}

The proxy component will instruct the engine to allocate space for a new world. A separate runtime physics world is also created and all the game objects in the collection "mylevel.collection" are instantiated.

The new world gets its name from the *Name* property in the collection file, in this example it is set to "mylevel". The name has to be unique. If the *Name* set in the collection file is already used for a loaded world, the engine will signal a name collision error:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

When the engine has finished loading the collection, the collection proxy component will send a message named `"proxy_loaded"` back to the script that sent the `"load"` message. The script can then initialize and enable the collection as a reaction to the message:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- New world is loaded. Init and enable it.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: This message tells the collection proxy component to start loading its collection into a new world. The proxy will send back a message called `"proxy_loaded"` when it's done.

`"async_load"`
: This message tells the collection proxy component to start background loading its collection into a new world. The proxy will send back a message called `"proxy_loaded"` when it's done.

`"init"`
: This message tells the collection proxy component that all the game objects and components that has been instantiated should be initialized. All script `init()` functions are called at this stage.

`"enable"`
: This message tells the collection proxy component that all the game objects and components should be enabled. All sprite components begin to draw when enabled, for instance.

## Addressing into the new world

The *Name* set in the collection file properties is used to address game objects and components in the loaded world. If you, for instance, create a loader object in the bootstrap collection you may need to communicate with it from any loaded collection:

```lua
-- tell the loader to load the next level:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![load](images/collection-proxy/message_passing.png){srcset="images/collection-proxy/message_passing@2x.png 2x"}

## Unloading a world

To unload a loaded collection, you send messages corresponding to the converse steps of the loading:

```lua
-- unload the level
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: This message tells the collection proxy component to disable all the game object and components in the world. Sprites stop being rendered at this stage.

`"final"`
: This message tells the collection proxy component to finalize all the game object and components in the world. All scripts' `final()` functions are called at this stage.

`"unload"`
: This message tells the collection proxy to remove the world completely from memory.

If you don’t need the finer grained control, you can send the `"unload"` message directly without first disabling and finalizing the collection. The proxy will then automatically disable and finalize the collection before it’s unloaded.

When the collection proxy has finished unloading the collection it will send a `"proxy_unloaded"` message back to the script that sent the `"unload"` message:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, the world is unloaded...
        ...
    end
end
```


## Time step

Collection proxy updates can be scaled by altering the _time step_. This means that even though the game ticks at a steady 60 FPS, a proxy can update at a higher or lower pace, affecting physics and the `dt` variable passed to `update()`. You can also set the update mode, which allows you to control if the scaling should be performed discretely (which only makes sense with a scale factor below 1.0) or continuously.

You control the scale factor and the scaling mode by sending the proxy a `set_time_step` message:

```lua
-- update loaded world at one-fifth-speed.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

To see what's happening when changing the time step, we can create an object with the following code in a script component and put it in the collection we're altering the timestep of:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

With a time step of 0.2, we get the following result in the console:

```txt
INFO:DLIB: SSDP started (ssdp://192.168.0.102:54967, http://0.0.0.0:62162)
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` is still called 60 times a second, but the value of `dt` changes. We see that only 1/5 (0.2) of the calls to `update()` will have a `dt` of 1/60 (corresponding to 60 FPS)---the rest is zero. All physics simulations will also be updated according to that dt and advance only in one fifth of the frames.

See [`set_time_step`](/ref/collectionproxy#set_time_step) for more details.

## Caveats and common issues

Physics
: Through collection proxies it is possible to load more than one top level collection, or *game world* into the engine. When doing so it is important to know that each top level collection is a separate physical world. Physics interactions (collisions, triggers, ray-casts) only happen between objects belonging to the same world. So even if the collision objects from two worlds visually sits right on top of each other, there cannot be any physics interaction between them.

Memory
: Each loaded collection creates a new game world which comes with a relatively large memory footprint. If you load dozens of collections simultaneously through proxies, you might want to reconsider your design. To spawn many instances of game object hierarchies, [collection factories](/manuals/collection-factory) are more suitable.

Input
: If you have objects in your loaded collection that require input actions, you need to make sure that the game object that contains the collection proxy acquires input. When the game object receives input messages these are propagated to the components of that object, i.e. the collection proxies. The input actions are sent via the proxy into the loaded collection.
