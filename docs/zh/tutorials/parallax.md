---
title: Parallax code sample
brief: In this sample, you learn how to use a parallax effect to simulate depth in the game world.
---
# Parallax

<iframe width="560" height="315" src="https://www.youtube.com/embed/rv7GrtmUrPU" frameborder="0" allowfullscreen></iframe>

In this sample, we demonstrate how to use a parallax effect to simulate depth in the game world.
There are two layers of clouds, where one of the layers has the appearance of being further back than the other. There is also an animated saucer for flavor.

The cloud layers are built as two separate game objects, containing a *Tile Map* and *Script* each.
The layers are moved at different speeds, to give the parallax effect. This is done in `update()` of *background1.script* and *background2.script* below.

```lua
-- file: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- the background is a tilemap in a gameobject
-- we move the gameobject for the parallax effect

function update(self, dt)
    -- decrease x-position by 1 units per frame for parallax effect
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- file: background2.script

-- the background is a tilemap in a gameobject
-- we move the gameobject for the parallax effect

function update(self, dt)
    -- decrease x-position by 0.5 units per frame for parallax effect
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

The saucer is a separate game object, containing a *Sprite* and a *Script*.
It is moved to the left at a constant speed. The up-down-motion is obtained by animating its y-component around a fixed value using the Lua sine function (`math.sin()`). This is done in `update()` of *spaceship.script*.


```lua
-- file: spaceship.script

function init(self)
    -- remeber initial y position such that we
    -- can move the spaceship without changing the script
    self.start_y = go.get_position().y
    -- set counter to zero. use for sin-movement below
    self.counter = 0
end

function update(self, dt)
    -- decrease x-position by 2 units per frame
    local p = go.get_position()
    p.x = p.x - 2

    -- move the y position around initial y
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- update position
    go.set_position(p)

    -- remove shaceship when outside of screen
    if p.x < - 32 then
        go.delete()
    end

    -- increase the counter
    self.counter = self.counter + 1
end
```
