---
title: Esempio di codice per la parallasse
brief: In questo esempio impari a usare un effetto di parallasse per simulare la profondità nel mondo di gioco.
---
# Parallasse - progetto di esempio {#parallax-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


In questo progetto di esempio, che puoi [aprire dall'editor](/manuals/project-setup/) o [scaricare da GitHub](https://github.com/defold/sample-parallax), mostriamo come usare un effetto di parallasse per simulare la profondità nel mondo di gioco.
Ci sono due livelli di nuvole, uno dei quali sembra più lontano dell'altro. C'è anche un disco volante animato per dare un tocco in più.

I livelli di nuvole sono realizzati come due oggetti di gioco (game object) distinti, ciascuno contenente un componente *Tile Map* e un componente *Script*.
I livelli si muovono a velocità diverse per creare l'effetto di parallasse. Questo avviene in `update()` di *background1.script* e *background2.script*, riportati di seguito.

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

Il disco volante è un oggetto di gioco distinto, contenente un componente *Sprite* e un componente *Script*.
Si muove verso sinistra a velocità costante. Il movimento su e giù si ottiene facendo oscillare la sua componente y attorno a un valore fisso mediante la funzione seno di Lua (`math.sin()`). Questo avviene in `update()` di *spaceship.script*.


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
