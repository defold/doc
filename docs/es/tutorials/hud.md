---
title: Ejemplo de código HUD
brief: En este proyecto de ejemplo, aprenderás efectos para contar la puntuación.
---
# HUD - proyecto de ejemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

En este proyecto de ejemplo, que puedes [abrir desde el editor](/manuals/project-setup/) o [descargar desde GitHub](https://github.com/defold/sample-hud), demostramos efectos para contar la puntuación. Las puntuaciones aparecen aleatoriamente por la pantalla, simulando un juego en el que el jugador obtiene puntos en distintas posiciones.

Las puntuaciones flotan durante un rato después de aparecer. Para lograr esto, hacemos que las puntuaciones sean transparentes y luego hacemos aparecer gradualmente su color. También las animamos hacia arriba. Esto se hace en `on_message()` más abajo.

Luego se mueven hacia la puntuación total en la parte superior de la pantalla, donde se suman.
También se desvanecen ligeramente mientras se mueven hacia arriba. Esto se hace en `float_done()`.

Cuando han alcanzado la puntuación superior, sus cantidades se agregan a una puntuación objetivo hacia la que va contando la puntuación total. Esto se hace en `swoosh_done()`.

Cuando se actualiza el script, comprueba si la puntuación objetivo ha aumentado y si la puntuación total necesita contarse hacia arriba. Cuando esto es cierto, la puntuación total se incrementa en un paso más pequeño.
Luego se anima la escala de la puntuación total para dar un efecto de rebote. Esto se hace en `update()`.

Cada vez que se incrementa el total, generamos una cantidad de estrellas más pequeñas y las animamos hacia afuera desde la puntuación total. Las estrellas se generan, animan y eliminan en `spawn_stars()`, `fade_out_star()` y `delete_star()`.

```lua
-- file: hud.gui_script
-- qué tan rápido aumenta la puntuación por segundo
local score_inc_speed = 1000

function init(self)
    -- la puntuación objetivo es la puntuación actual en el juego
    self.target_score = 0
    -- la puntuación actual que se cuenta hacia la puntuación objetivo
    self.current_score = 0
    -- la puntuación tal como se muestra en el hud
    self.displayed_score = 0
    -- conserva una referencia al nodo que muestra la puntuación para usarlo más abajo
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- la estrella terminó su animación, elimínala
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- desvanece la estrella antes de eliminarla
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- posición del nodo de puntuación, usada para colocar las estrellas
    local p = gui.get_position(self.score_node)
    -- distancia desde la posición donde aparece la estrella
    local start_distance = 0
    -- distancia donde se detiene la estrella
    local end_distance = 240
    -- distancia angular entre cada estrella en el círculo de estrellas
    local angle_step = 2 * math.pi / amount
    -- aleatoriza el ángulo inicial
    local angle = angle_step * math.random()
    for i=1,amount do
        -- incrementa el ángulo por el paso para obtener una distribución uniforme de estrellas
        angle = angle + angle_step
        -- dirección del movimiento de la estrella
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- posiciones inicial/final de la estrella
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- crea el nodo de la estrella
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- define su textura
        gui.set_texture(star, "star")
        -- define transparente
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- aparece gradualmente
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- anima la posición
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- comprueba si la puntuación necesita actualizarse
    if self.current_score < self.target_score then
        -- incrementa la puntuación para este timestep para crecer hacia la puntuación objetivo
        self.current_score = self.current_score + score_inc_speed * dt
        -- limita la puntuación para que no pase de la puntuación objetivo
        self.current_score = math.min(self.current_score, self.target_score)
        -- redondea hacia abajo la puntuación para mostrarla sin decimales
        local floored_score = math.floor(self.current_score)
        -- comprueba si la puntuación mostrada debe actualizarse
        if self.displayed_score ~= floored_score then
            -- actualiza la puntuación mostrada
            self.displayed_score = floored_score
            -- actualiza el texto del nodo de puntuación
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- define la escala del nodo de puntuación para que sea un poco mayor de lo normal
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- luego anima la escala de vuelta al valor original
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- genera estrellas
            spawn_stars(self, 4)
        end
    end
end

-- esta función almacena la puntuación agregada para que la puntuación mostrada pueda contarse en la función update
local function swoosh_done(self, node)
    -- recupera la puntuación del nodo
    local amount = tonumber(gui.get_text(node))
    -- aumenta la puntuación objetivo, consulta la función update para ver cómo la puntuación se actualiza para coincidir con la puntuación objetivo
    self.target_score = self.target_score + amount
    -- elimina la puntuación temporal
    gui.delete_node(node)
end

-- esta función anima el nodo desde haber flotado primero hasta salir con un swoosh hacia la puntuación total mostrada
local function float_done(self, node)
    local duration = 0.2
    -- sale con un swoosh hacia la puntuación mostrada
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- también se desvanece parcialmente durante el swoosh
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- registra la puntuación agregada, este mensaje podría enviarlo cualquiera que quiera incrementar la puntuación
    if message_id == hash("add_score") then
        -- crea un nuevo nodo de puntuación temporal
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- usa la fuente pequeña para él
        gui.set_font(node, "small_score")
        -- inicialmente transparente
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- aparece gradualmente
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- flota
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

En main.script recibimos entrada táctil o del mouse y luego enviamos un mensaje al script de GUI que crea nuevas puntuaciones usando la posición del toque.

```lua
-- Al hacer click/tocar, obtiene la posición del toque y la envía mediante un mensaje al script GUI del HUD, junto con la cantidad de puntos anotados.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- usa input action.x y action.y como posiciones x e y del toque
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```
