---
title: Codebeispiel für Parallaxe
brief: In diesem Beispiel lernst du, wie du mit einem Parallaxeneffekt Tiefe in der Spielwelt simulierst.
---
# Parallaxe - Beispielprojekt {#parallax-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


In diesem Beispielprojekt, das du [im Editor öffnen](/manuals/project-setup/) oder [von GitHub herunterladen](https://github.com/defold/sample-parallax) kannst, zeigen wir, wie du mit einem Parallaxeneffekt Tiefe in der Spielwelt simulierst.
Es gibt zwei Wolkenebenen, von denen eine weiter hinten zu liegen scheint als die andere. Außerdem gibt es eine animierte fliegende Untertasse, die die Szene belebt.

Die Wolkenebenen sind als zwei separate Spielobjekte (game objects) aufgebaut, die jeweils eine *Kachelkarte* (tile map) und ein *Skript* enthalten.
Die Ebenen werden mit unterschiedlichen Geschwindigkeiten bewegt, um den Parallaxeneffekt zu erzeugen. Dies geschieht in `update()` in *background1.script* und *background2.script*, wie unten gezeigt.

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

Die fliegende Untertasse ist ein separates Spielobjekt, das ein *Sprite* und ein *Skript* enthält.
Sie wird mit konstanter Geschwindigkeit nach links bewegt. Die Auf-und-ab-Bewegung entsteht, indem ihre y-Komponente mithilfe der Lua-Sinusfunktion (`math.sin()`) um einen festen Wert herum animiert wird. Dies geschieht in `update()` in *spaceship.script*.


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
