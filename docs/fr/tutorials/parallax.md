---
title: Exemple de code de parallaxe
brief: Dans cet exemple, vous apprenez à utiliser un effet de parallaxe pour simuler la profondeur dans le monde de jeu.
---
# Parallaxe - projet exemple {#parallax-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


Dans ce projet exemple, que vous pouvez [ouvrir depuis l'éditeur](/manuals/project-setup/) ou [télécharger depuis GitHub](https://github.com/defold/sample-parallax), nous montrons comment utiliser un effet de parallaxe pour simuler la profondeur dans le monde de jeu (game world).
Il y a deux couches de nuages, dont l'une semble plus éloignée que l'autre. Une soucoupe animée vient également agrémenter la scène.

Les couches de nuages sont constituées de deux objets de jeu (game objects) distincts, contenant chacun un composant (component) *Tile Map* et un composant *Script*.
Les couches se déplacent à des vitesses différentes pour produire l'effet de parallaxe. Ce déplacement est effectué dans `update()` de *background1.script* et *background2.script* ci-dessous.

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

La soucoupe est un objet de jeu distinct, contenant un composant *Sprite* et un composant *Script*.
Elle se déplace vers la gauche à une vitesse constante. Le mouvement de haut en bas est obtenu en animant sa coordonnée y autour d'une valeur fixe à l'aide de la fonction sinus de Lua (`math.sin()`). Cette animation est effectuée dans `update()` de *spaceship.script*.


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
