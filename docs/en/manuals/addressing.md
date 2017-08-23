---
title: Addressing in Defold
brief: This manual explains how Defold has solved the problem of addressing.
---

# Addressing

Every game object and component that exist in runtime must be possible to address. This manual describes how Defold solves the addressing problem.

## Identifiers

When you create a new game object or component in the editor, a unique *Id* property is automatically set. Game objects automatically get an id called "go" with an enumerator ("go2", "go3" etc) and components get an id corresponding to the component type ("sprite", "sprite2" etc). All these identifiers can be modified and you are encouraged to pick good, descriptive names for your game objects and components.

![identifiers](images/addressing/identifiers.png)

Here we have created a collection file containing two separate game objects. We have given the game objects the identifiers "soldier" and "shield". Each game object also contains a single sprite component. The sprites are both named "sprite". There is also a script component in the "shield" game object that we have named "controller".

Let's look a bit closer at the "shield" game object:

![shield flip](images/addressing/shield_script.png)

First, let's see how we can move the whole game object 10 pixels to the left:

```lua
local pos = go.get_position()
pos.x = pos.x + 10
go.set_position(pos)
```

Notice that there are no address identifiers in this code at all. This is because Defold knows that the script is running in a component inside the "shield" game object. It is therefore possible to *imply* the addresses. Let's explicitly put the addresses so we can see what
s really going on:

```lua
local pos = go.get_position("shield")
pos.x = position.x + 10
go.set_position(pos, "shield")
```

By omitting the identifier string, the current game object is implied.

Now suppose we want to write code in the script that disables the shield sprite only. The script and the sprite lives in the same game object so the game object id can be implied:

```lua
msg.post("#sprite", "disable")
```

Notice the initial character '#' before the component id. The hash sign is used to separate the game object id from the component id. Since we don't have a game object id before the hash sign, it starts the address string.

If the script wants to disable the sprite in the "soldier" game object, it is no longer possible to leave out the game object id:

```lua
msg.post("soldier#sprite", "disable")
```

Without the "soldier" part in the address, the runtime cannot separate the component "sprite" in the "shield" game object from the component "sprite" in the "soldier" game object. Defold combines the identity of the game object with that of the component and that explains why we can have two components named "sprite" without violating the requirement for identity uniqueness.

![sprite identifiers](images/addressing/sprites.png)

## Collections and game object ids


Every object in Defold is uniquely addressed through a URL (Uniform Resource Locator). The address is set at compile time and stays fixed throughout the object’s lifetime. This means that if you save the address to an object it will stay valid for as long as the object exists; you never have to worry about updating object references that you store.