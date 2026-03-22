---
title: Przykład kodu paralaksy
brief: W tym przykładzie nauczysz się używać efektu paralaksy do symulowania głębi w świecie gry.
---
# Paralaksa - projekt przykładowy

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


W tym przykładowym projekcie, który możesz [otworzyć z edytora](/manuals/project-setup/) albo [pobrać z repozytorium GitHub](https://github.com/defold/sample-parallax), pokazujemy, jak użyć efektu paralaksy do zasymulowania głębi w świecie gry.
Są dwie warstwy chmur, z których jedna sprawia wrażenie położonej dalej niż druga. Dla urozmaicenia dodano też animowany spodek.

Warstwy chmur są zbudowane z dwóch osobnych obiektów gry, z których każdy zawiera komponent *Tile Map* i *Script*.
Warstwy poruszają się z różnymi prędkościami, aby uzyskać efekt paralaksy. Robią to funkcje `update()` w plikach *background1.script* i *background2.script* poniżej.

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

Spodek jest osobnym obiektem gry, zawierającym komponent *Sprite* i *Script*.
Porusza się w lewo ze stałą prędkością. Ruch góra-dół uzyskuje się przez animowanie składowej `y` wokół stałej wartości za pomocą funkcji sinus w Lua (`math.sin()`). Odpowiada za to `update()` w pliku *spaceship.script*.


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
