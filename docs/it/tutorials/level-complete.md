---
title: Esempio di codice per il completamento di un livello
brief: In questo progetto di esempio impari a creare effetti per mostrare il conteggio del punteggio al completamento di un livello.
---
# Livello completato - progetto di esempio {#level-complete-sample-project}

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

In questo progetto di esempio, che puoi [aprire dall'editor](/manuals/project-setup/) o [scaricare da GitHub](https://github.com/defold/sample-levelcomplete), mostriamo alcuni effetti per visualizzare il conteggio del punteggio al completamento di un livello. Il punteggio aumenta fino al totale e compaiono tre stelle al raggiungimento di soglie diverse. L'esempio usa anche la funzionalità di ricaricamento per verificare rapidamente il risultato quando si modificano i valori.

La scena viene attivata da un messaggio proveniente dal gioco.
Il messaggio contiene il punteggio totale ottenuto e le soglie alle quali devono apparire le tre stelle.
Quando arriva il messaggio, il testo del titolo ("Level completed!") appare gradualmente, mentre si riduce fino alle dimensioni normali (100%). Questo avviene in `on_message()`, riportata di seguito.

Al termine dell'animazione del titolo, inizia il conteggio del punteggio totale. A ogni aggiornamento, il punteggio corrente aumenta di una piccola quantità. Poi verifichiamo se è stata superata una delle soglie per le stelle; in tal caso, avviamo l'animazione di una stella (vedi sotto). Finché non viene raggiunto il punteggio finale, il punteggio totale viene animato con un effetto di rimbalzo.
Inoltre, man mano che si avvicina al punteggio totale, la sua scala aumenta fino a un valore massimo. Allo stesso modo, il suo colore passa gradualmente dal bianco al verde. Questo avviene in `inc_score()`.

Ogni volta che appare una stella, questa diventa gradualmente visibile e si riduce fino alle dimensioni normali. Questo avviene in `animate_star()`.

Al termine dell'animazione della stella, vengono generate stelle più piccole disposte in cerchio intorno alla stella più grande. Questo avviene in `spawn_small_stars()`.

Le stelle più piccole vengono poi animate in modo da schizzare verso l'esterno dalla stella. Mentre si allontanano, sia la velocità sia la scala variano casualmente. Poi scompaiono gradualmente e infine vengono eliminate. Questo avviene in `animate_small_star()` e `delete_small_star()`.

Quando il conteggio raggiunge il punteggio totale, il timbro del record appare gradualmente e si riduce fino alle dimensioni previste. Questa animazione viene avviata alla fine di `inc_score()` ed eseguita in `animate_imprint()`.

La funzione `setup()` assicura che i nodi abbiano i valori iniziali corretti. Chiamando `setup()` da `on_reload()`, ci assicuriamo che tutto sia configurato correttamente ogni volta che lo script viene ricaricato dall'editor Defold.

```lua
-- file: level_complete.gui_script

-- how fast the score is incremented per second
local score_inc_speed = 51100
-- how long time between each update of the score
local dt = 0.03
-- scale of the score at the start of counting
local score_start_scale = 0.7
-- scale of the score when the target score has been reached
local score_end_scale = 1.0
-- how much the score "bounces" at each increment
local score_bounce_factor = 1.1
-- how many small stars to spawn for each big star
local small_star_count = 16

local function setup(self)
    -- make heading color transparent
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- make heading shadow transparent
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- set heading to twice the scale initially
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- set initial score (0)
    gui.set_text(self.score, "0")
    -- set score color to opaque white
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- set scale so the score can grow while counting
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- make all big stars transparent
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- make the imprint transparent
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- the score currently being displayed
    self.current_score = 0
    -- the target score when counting
    self.target_score = 0
end

function init(self)
    -- retrieve nodes for easier access
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- start color of the score
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- save score color and animate towards it during counting later
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- delete a small star, called when the star has finished animating
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- animate a small star according to the given initial position and angle
local function animate_small_star(self, pos, angle)
    -- direction of travel for the small star
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- create a small star
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- set its texture
    gui.set_texture(small_star, "small_star")
    -- set its color to full white
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- set start scale low
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- variation in scale of each small star
    local end_s_var = 1
    -- actual end scale of this star
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- variation in distance traveled (essentially speed of the star)
    local dist_var = 300
    -- actual distance the star will travel
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- spawn a number of small stars
local function spawn_small_stars(self, star)
    -- position of the big star the small star will spawn around
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- calculate the angle of the particular small star
        local angle = 2 * math.pi * i/small_star_count
        -- as well as position
        local pos = vmath.vector3(p.x, p.y, 0)
        -- spawn and animate the small star
        animate_small_star(self, pos, angle)
    end
end

-- start the animation of a big star fading in
local function animate_star(self, star)
    -- fade in duration
    local fade_in = 0.2
    -- make it transparent
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- fade in
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- initial scale
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- shrink back into place
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- start the animation of the imprint fading in
local function animate_imprint(self)
    -- wait a bit before the imprint appears
    local delay = 0.8
    -- fade in duration
    local fade_in = 0.2
    -- initial scale
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- shrink back into place
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- also fade in
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- increment the score one step towards the target
local function inc_score(self, node)
    -- how much the score is incremented this step
    local score_inc = score_inc_speed * dt
    -- new score after increment
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- start animating a big star if we cross the level in score for it to appear
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- update score, but clamp at target
    self.current_score = math.min(new_score, self.target_score)
    -- update the score on screen
    gui.set_text(self.score, tostring(self.current_score))
    -- if we are not yet done, keep animating and incrementing
    if self.current_score < self.target_score then
        -- how close we are to the target
        local f = self.current_score / self.target_score
        -- blend the color to get a slow fade
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- new scale for this step
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- increase the scale by the bounce factor
        local sp = s * score_bounce_factor
        -- animate from bounced scale back to the appropriate scale
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- we are done, fade in the imprint
        -- NOTE! this should in a real case be checked against the actual stored high score
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- someone tells us that we should display the level completed scene
    if message_id == hash("level_completed") then
        -- retrieve the obtained score and at which score levels the stars should be displayed
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- fade in heading ("level completed")
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- shrink it into place
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- this function is called when the script is reloaded
-- by setting up the scene and simulating level complete, we get a really fast workflow for tweaking
function on_reload(self)
    -- make sure any setup changes are taken into account
    setup(self)
    -- simulate that the level has been completed
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```
