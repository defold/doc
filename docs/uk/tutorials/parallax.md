---
title: Приклад коду з паралаксом
brief: У цьому прикладі ви дізнаєтеся, як використовувати ефект паралаксу для імітації глибини в ігровому світі.
---
# Паралакс — приклад проєкту {#parallax-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


У цьому прикладі проєкту, який можна [відкрити з редактора](/manuals/project-setup/) або [завантажити з GitHub](https://github.com/defold/sample-parallax), ми показуємо, як використовувати ефект паралаксу для імітації глибини в ігровому світі.
Тут є два шари хмар, один із яких здається віддаленішим за інший. Для пожвавлення сцени також додано анімовану летючу тарілку.

Шари хмар створено як два окремі ігрові об’єкти (game object), кожен із яких містить карту плиток (*Tile Map*) і скрипт (*Script*).
Шари рухаються з різною швидкістю, створюючи ефект паралаксу. Це реалізовано у функції `update()` файлів *background1.script* і *background2.script*, наведених нижче.

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

Летюча тарілка — це окремий ігровий об’єкт, що містить спрайт (*Sprite*) і скрипт (*Script*).
Вона рухається ліворуч зі сталою швидкістю. Рух угору-вниз створюється анімацією її координати y навколо фіксованого значення за допомогою функції синуса Lua (`math.sin()`). Це реалізовано у функції `update()` файлу *spaceship.script*.


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
