---
title: Ejemplo de código Level complete
brief: En este proyecto de ejemplo, aprenderás efectos para mostrar el conteo de puntuación que podría ocurrir cuando se completa un nivel.
---
# Level complete - proyecto de ejemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

En este proyecto de ejemplo, que puedes [abrir desde el editor](/manuals/project-setup/) o [descargar desde GitHub](https://github.com/defold/sample-levelcomplete), demostramos efectos para mostrar el conteo de puntuación que podría ocurrir cuando se completa un nivel. Una puntuación total se cuenta hacia arriba y aparecen tres estrellas cuando se alcanzan distintos niveles. El ejemplo también usa la funcionalidad de recarga para una iteración rápida al ajustar valores.

La escena se activa mediante un mensaje del juego.
El mensaje contiene la puntuación total obtenida y en qué niveles deben aparecer las tres estrellas.
Cuando esto ocurre, el texto de encabezado ("Level completed!") aparece gradualmente mientras se reduce a su tamaño regular (100%). Esto se hace en `on_message()` más abajo.

Después de completar la animación del texto de encabezado, la puntuación total empieza a contar hacia arriba. Cada vez que esto ocurre, la puntuación actual se incrementa en un paso pequeño. Luego comprobamos si se ha cruzado uno de los niveles de estrella, en cuyo caso empieza la animación de una estrella (ver más abajo). Mientras no hayamos alcanzado la puntuación objetivo, la puntuación total se anima con un efecto de rebote.
También crecerá hacia un máximo de escala cuanto más cerca esté de la puntuación total. De la misma manera, su color cambia gradualmente de blanco a verde. Esto se hace en `inc_score()`.

Cada vez que aparece una estrella, se desvanece hacia dentro y se encoge hasta su tamaño regular. Esto se hace en `animate_star()`.

Cuando la estrella ha terminado de animarse, las estrellas más pequeñas se generan en un círculo alrededor de la estrella grande. Esto se hace en `spawn_small_stars()`.

Luego se animan para salir disparadas aleatoriamente desde la estrella. Se aleatorizan tanto en velocidad como en escala mientras se expanden hacia afuera. Luego se desvanecen y finalmente se eliminan. Esto se hace en `animate_small_star()` y `delete_small_star()`.

Cuando la puntuación ha alcanzado la puntuación total, la marca de high-score aparece gradualmente y se encoge de vuelta a su lugar. Esto empieza al final de `inc_score()` y se realiza en `animate_imprint()`.

La función `setup()` se asegura de que los nodos tengan los valores iniciales correctos. Al llamar a `setup()` desde `on_reload()`, nos aseguramos de que todo se configure correctamente cada vez que el script se recarga desde el Defold Editor.

```lua
-- file: level_complete.gui_script

-- qué tan rápido se incrementa la puntuación por segundo
local score_inc_speed = 51100
-- cuánto tiempo hay entre cada actualización de la puntuación
local dt = 0.03
-- escala de la puntuación al inicio del conteo
local score_start_scale = 0.7
-- escala de la puntuación cuando se ha alcanzado la puntuación objetivo
local score_end_scale = 1.0
-- cuánto "rebota" la puntuación en cada incremento
local score_bounce_factor = 1.1
-- cuántas estrellas pequeñas generar por cada estrella grande
local small_star_count = 16

local function setup(self)
    -- hace transparente el color del encabezado
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- hace transparente la sombra del encabezado
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- define inicialmente el encabezado al doble de escala
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- define la puntuación inicial (0)
    gui.set_text(self.score, "0")
    -- define el color de la puntuación como blanco opaco
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- define la escala para que la puntuación pueda crecer mientras se cuenta
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- hace transparentes todas las estrellas grandes
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- hace transparente la marca
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- la puntuación que se muestra actualmente
    self.current_score = 0
    -- la puntuación objetivo durante el conteo
    self.target_score = 0
end

function init(self)
    -- recupera nodos para acceder a ellos con más facilidad
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- color inicial de la puntuación
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- guarda el color de la puntuación y anima hacia él durante el conteo más adelante
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- elimina una estrella pequeña, llamada cuando la estrella ha terminado de animarse
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- anima una estrella pequeña según la posición inicial y el ángulo dados
local function animate_small_star(self, pos, angle)
    -- dirección de desplazamiento de la estrella pequeña
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- crea una estrella pequeña
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- define su textura
    gui.set_texture(small_star, "small_star")
    -- define su color como blanco completo
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- define una escala inicial baja
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- variación en la escala de cada estrella pequeña
    local end_s_var = 1
    -- escala final real de esta estrella
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- variación en la distancia recorrida (básicamente la velocidad de la estrella)
    local dist_var = 300
    -- distancia real que recorrerá la estrella
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- genera una cantidad de estrellas pequeñas
local function spawn_small_stars(self, star)
    -- posición de la estrella grande alrededor de la cual aparecerá la estrella pequeña
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- calcula el ángulo de la estrella pequeña particular
        local angle = 2 * math.pi * i/small_star_count
        -- además de la posición
        local pos = vmath.vector3(p.x, p.y, 0)
        -- genera y anima la estrella pequeña
        animate_small_star(self, pos, angle)
    end
end

-- inicia la animación de una estrella grande apareciendo gradualmente
local function animate_star(self, star)
    -- duración de aparición gradual
    local fade_in = 0.2
    -- la hace transparente
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- aparece gradualmente
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- escala inicial
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- se encoge de vuelta a su lugar
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- inicia la animación de la marca apareciendo gradualmente
local function animate_imprint(self)
    -- espera un poco antes de que aparezca la marca
    local delay = 0.8
    -- duración de aparición gradual
    local fade_in = 0.2
    -- escala inicial
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- se encoge de vuelta a su lugar
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- también aparece gradualmente
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- incrementa la puntuación un paso hacia el objetivo
local function inc_score(self, node)
    -- cuánto se incrementa la puntuación en este paso
    local score_inc = score_inc_speed * dt
    -- nueva puntuación después del incremento
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- empieza a animar una estrella grande si cruzamos el nivel de puntuación para que aparezca
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- actualiza la puntuación, pero la limita al objetivo
    self.current_score = math.min(new_score, self.target_score)
    -- actualiza la puntuación en pantalla
    gui.set_text(self.score, tostring(self.current_score))
    -- si todavía no terminamos, sigue animando e incrementando
    if self.current_score < self.target_score then
        -- qué tan cerca estamos del objetivo
        local f = self.current_score / self.target_score
        -- mezcla el color para obtener un desvanecimiento lento
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- nueva escala para este paso
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- aumenta la escala por el factor de rebote
        local sp = s * score_bounce_factor
        -- anima desde la escala rebotada de vuelta a la escala apropiada
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- terminamos, aparece gradualmente la marca
        -- NOTE! en un caso real, esto debería comprobarse contra el high score almacenado real
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- alguien nos dice que debemos mostrar la escena de nivel completado
    if message_id == hash("level_completed") then
        -- recupera la puntuación obtenida y los niveles de puntuación en los que se deben mostrar las estrellas
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- aparece gradualmente el encabezado ("level completed")
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- se encoge a su lugar
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- esta función se llama cuando el script se recarga
-- al configurar la escena y simular nivel completado, obtenemos un flujo de trabajo realmente rápido para ajustar valores
function on_reload(self)
    -- asegúrate de que se tengan en cuenta los cambios de configuración
    setup(self)
    -- simula que el nivel se ha completado
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```
