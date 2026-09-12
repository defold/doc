---
title: Paralaks kod örneği
brief: Bu örnekte, oyun dünyasında derinlik hissi yaratmak için paralaks efektini nasıl kullanacağınızı öğreneceksiniz.
---
# Paralaks - örnek proje

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


[Düzenleyiciden açabileceğiniz](/manuals/project-setup/) veya [GitHub'dan indirebileceğiniz](https://github.com/defold/sample-parallax) bu örnek projede, oyun dünyasında derinlik hissi yaratmak için paralaks (parallax) efektinin nasıl kullanılacağını gösteriyoruz.
Bulutlardan oluşan iki katman vardır; katmanlardan biri diğerinden daha gerideymiş gibi görünür. Sahneye renk katmak için animasyonlu bir uçan daire de bulunur.

Bulut katmanları, her biri bir *Tile Map* (karo haritası) ve bir *Script* (betik) bileşeni (component) içeren iki ayrı oyun nesnesi (game object) olarak oluşturulmuştur.
Paralaks efekti oluşturmak için katmanlar farklı hızlarda hareket ettirilir. Aşağıdaki kodda bu işlem `update()` işlevi içinde, *background1.script* ve *background2.script* dosyalarında yapılır.

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

Uçan daire, bir *Sprite* bileşeni ve bir *Script* bileşeni içeren ayrı bir oyun nesnesidir.
Sabit hızla sola hareket ettirilir. Yukarı aşağı hareketi, Lua sinüs işlevi (`math.sin()`) kullanılarak y bileşeninin sabit bir değer etrafında animasyonla değiştirilmesiyle elde edilir. Bu işlem `update()` işlevi içinde, *spaceship.script* dosyasında yapılır.


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
