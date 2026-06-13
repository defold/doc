---
title: Ejemplo de código Parallax
brief: En este ejemplo, aprenderás a usar un efecto de parallax para simular profundidad en el mundo del juego.
---
# Parallax - proyecto de ejemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


En este proyecto de ejemplo, que puedes [abrir desde el editor](/manuals/project-setup/) o [descargar desde GitHub](https://github.com/defold/sample-parallax), demostramos cómo usar un efecto de parallax para simular profundidad en el mundo del juego.
Hay dos capas de nubes, donde una de las capas tiene la apariencia de estar más atrás que la otra. También hay un platillo animado para darle sabor.

Las capas de nubes se construyen como dos objetos de juego separados, cada uno con un *Tile Map* y un *Script*.
Las capas se mueven a distintas velocidades para dar el efecto de parallax. Esto se hace en `update()` de *background1.script* y *background2.script* más abajo.

```lua
-- file: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- el fondo es un tilemap en un gameobject
-- movemos el gameobject para el efecto de parallax

function update(self, dt)
    -- disminuye la posición x en 1 unidad por frame para el efecto de parallax
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- file: background2.script

-- el fondo es un tilemap en un gameobject
-- movemos el gameobject para el efecto de parallax

function update(self, dt)
    -- disminuye la posición x en 0.5 unidades por frame para el efecto de parallax
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

El platillo es un objeto de juego separado, que contiene un *Sprite* y un *Script*.
Se mueve hacia la izquierda a velocidad constante. El movimiento arriba-abajo se obtiene animando su componente y alrededor de un valor fijo usando la función seno de Lua (`math.sin()`). Esto se hace en `update()` de *spaceship.script*.


```lua
-- file: spaceship.script

function init(self)
    -- recuerda la posición y inicial para que podamos
    -- mover la nave espacial sin cambiar el script
    self.start_y = go.get_position().y
    -- define el contador en cero. se usa para el movimiento sin más abajo
    self.counter = 0
end

function update(self, dt)
    -- disminuye la posición x en 2 unidades por frame
    local p = go.get_position()
    p.x = p.x - 2

    -- mueve la posición y alrededor de la y inicial
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- actualiza la posición
    go.set_position(p)

    -- elimina la nave espacial cuando está fuera de la pantalla
    if p.x < - 32 then
        go.delete()
    end

    -- incrementa el contador
    self.counter = self.counter + 1
end
```
