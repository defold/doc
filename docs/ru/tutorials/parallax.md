---
title: Пример кода Parallax
brief: В этом примере вы узнаете, как использовать эффект параллакса для имитации глубины в игровом мире.
---
# Parallax — пример проекта

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


В этом примере проекта, который можно [открыть из редактора](/manuals/project-setup/) или [скачать с GitHub](https://github.com/defold/sample-parallax), мы показываем, как использовать эффект параллакса для имитации глубины в игровом мире.
Здесь есть два слоя облаков, и один из них выглядит более удалённым, чем другой. Для живости также добавлена анимированная летающая тарелка.

Слои облаков построены как два отдельных игровых объекта, каждый со своими *Tile Map* и *Script*.
Слои движутся с разной скоростью, что и создаёт эффект параллакса. Это делается в `update()` файлов *background1.script* и *background2.script*, приведённых ниже.

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

Летающая тарелка сделана как отдельный игровой объект со *Sprite* и *Script*.
Она движется влево с постоянной скоростью. Движение вверх-вниз получается за счёт анимации компоненты y вокруг фиксированного значения с помощью функции Lua sine (`math.sin()`). Это реализовано в `update()` файла *spaceship.script*.


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
