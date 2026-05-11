---
title: Exemplo de código de conclusão de nível
brief: Neste projeto de exemplo, você aprende efeitos para mostrar a contagem de pontuação que poderia ocorrer quando um nível é concluído.
---
# Level complete - projeto de exemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/tSdTSvku1o8" frameborder="0" allowfullscreen></iframe>

Neste projeto de exemplo, que você pode [abrir pelo editor](/manuals/project-setup/) ou [baixar do GitHub](https://github.com/defold/sample-levelcomplete), demonstramos efeitos para mostrar a contagem de pontuação que poderia ocorrer quando um nível é concluído. Uma pontuação total é contada para cima e três estrelas aparecem quando diferentes níveis de pontuação são alcançados. O exemplo também usa a funcionalidade de reload para permitir iterações rápidas ao ajustar valores.

A cena é acionada por uma mensagem do jogo.
A mensagem contém a pontuação total obtida e em quais níveis de pontuação as três estrelas devem aparecer.
Quando isso acontece, o texto do título ("Level completed!") aparece gradualmente enquanto é reduzido até o tamanho regular (100%). Isso é feito em `on_message()` abaixo.

Depois que a animação do texto do título é concluída, a pontuação total começa a contar para cima. Cada vez que isso acontece, a pontuação atual é incrementada em um pequeno passo. Então verificamos se um dos níveis das estrelas foi cruzado; nesse caso, a animação de uma estrela começa (veja abaixo). Enquanto não alcançamos a pontuação-alvo, a pontuação total é animada com um efeito de quique.
Ela também cresce em direção a uma escala máxima conforme se aproxima da pontuação total. Da mesma forma, sua cor muda gradualmente de branco para verde. Isso é feito em `inc_score()`.

Cada vez que uma estrela aparece, ela surge gradualmente e encolhe até o tamanho regular. Isso é feito em `animate_star()`.

Quando a estrela termina de animar, estrelas menores são criadas em um círculo ao redor da estrela maior. Isso é feito em `spawn_small_stars()`.

Depois, elas são animadas para disparar aleatoriamente a partir da estrela. Tanto a velocidade quanto a escala são randomizadas enquanto elas se expandem para fora. Em seguida, elas desaparecem e finalmente são removidas. Isso é feito em `animate_small_star()` e `delete_small_star()`.

Quando a pontuação alcança a pontuação total, a marca de high-score aparece gradualmente e encolhe de volta para o lugar. Isso começa no final de `inc_score()` e é executado em `animate_imprint()`.

A função `setup()` garante que os nodes tenham os valores iniciais corretos. Ao chamar `setup()` a partir de `on_reload()`, garantimos que tudo seja configurado corretamente sempre que o script for recarregado pelo Defold Editor.

```lua
-- file: level_complete.gui_script

-- velocidade com que a pontuacao e incrementada por segundo
local score_inc_speed = 51100
-- quanto tempo entre cada atualizacao da pontuacao
local dt = 0.03
-- escala da pontuacao no inicio da contagem
local score_start_scale = 0.7
-- escala da pontuacao quando a pontuacao-alvo foi alcancada
local score_end_scale = 1.0
-- quanto a pontuacao "quica" a cada incremento
local score_bounce_factor = 1.1
-- quantas estrelas pequenas criar para cada estrela grande
local small_star_count = 16

local function setup(self)
    -- torna a cor do titulo transparente
    local c = gui.get_color(self.heading)
    c.w = 0
    gui.set_color(self.heading, c)
    -- torna a sombra do titulo transparente
    c = gui.get_shadow(self.heading)
    c.w = 0
    gui.set_shadow(self.heading, c)
    -- define o titulo inicialmente com o dobro da escala
    local s = 2
    gui.set_scale(self.heading, vmath.vector3(s, s, s))
    -- define a pontuacao inicial (0)
    gui.set_text(self.score, "0")
    -- define a cor da pontuacao como branco opaco
    gui.set_color(self.score, vmath.vector4(1, 1, 1, 1))
    -- define a escala para que a pontuacao possa crescer durante a contagem
    gui.set_scale(self.score, vmath.vector4(score_start_scale, score_start_scale, 1, 0))

    -- torna todas as estrelas grandes transparentes
    for i=1,#self.stars do
        gui.set_color(self.stars[i], vmath.vector4(1, 1, 1, 0))
    end
    -- torna a marca transparente
    gui.set_color(self.imprint, vmath.vector4(1, 1, 1, 0))
    -- a pontuacao sendo exibida atualmente
    self.current_score = 0
    -- a pontuacao-alvo durante a contagem
    self.target_score = 0
end

function init(self)
    -- recupera nodes para facilitar o acesso
    self.heading = gui.get_node("heading")
    self.stars = {gui.get_node("star_left"), gui.get_node("star_mid"), gui.get_node("star_right")}
    self.score = gui.get_node("score")
    self.imprint = gui.get_node("imprint")
    -- cor inicial da pontuacao
    self.score_start_color = vmath.vector4(1, 1, 1, 1)
    -- salva a cor da pontuacao e anima em direcao a ela durante a contagem posteriormente
    self.score_end_color = gui.get_color(self.score)
    setup(self)
end

-- remove uma estrela pequena, chamado quando a estrela terminou de animar
local function delete_small_star(self, small_star)
    gui.delete_node(small_star)
end

-- anima uma estrela pequena de acordo com a posicao inicial e o angulo dados
local function animate_small_star(self, pos, angle)
    -- direcao de deslocamento da estrela pequena
    local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0, 0)
    -- cria uma estrela pequena
    local small_star = gui.new_box_node(pos + dir * 20, vmath.vector3(64, 64, 0))
    -- define sua textura
    gui.set_texture(small_star, "small_star")
    -- define sua cor como branco total
    gui.set_color(small_star, vmath.vector4(1, 1, 1, 1))
    -- define escala inicial baixa
    local start_s = 0.3
    gui.set_scale(small_star, vmath.vector3(start_s, start_s, 1))
    -- variacao na escala de cada estrela pequena
    local end_s_var = 1
    -- escala final real desta estrela
    local end_s = 0.5 + math.random() * end_s_var
    gui.animate(small_star, gui.PROP_SCALE, vmath.vector4(end_s, end_s, 1, 0), gui.EASING_NONE, 0.5)
    -- variacao na distancia percorrida (essencialmente a velocidade da estrela)
    local dist_var = 300
    -- distancia real que a estrela percorrera
    local dist = 400 + math.random() * dist_var
    gui.animate(small_star, gui.PROP_POSITION, pos + dir * dist, gui.EASING_NONE, 0.5)
    gui.animate(small_star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_OUT, 0.3, 0.2, delete_small_star)
end

-- cria varias estrelas pequenas
local function spawn_small_stars(self, star)
    -- posicao da estrela grande ao redor da qual a estrela pequena sera criada
    local p = gui.get_position(star)
    for i = 1,small_star_count do
        -- calcula o angulo da estrela pequena especifica
        local angle = 2 * math.pi * i/small_star_count
        -- assim como a posicao
        local pos = vmath.vector3(p.x, p.y, 0)
        -- cria e anima a estrela pequena
        animate_small_star(self, pos, angle)
    end
end

-- inicia a animacao de aparecimento gradual de uma estrela grande
local function animate_star(self, star)
    -- duracao do aparecimento gradual
    local fade_in = 0.2
    -- torna-a transparente
    gui.set_color(star, vmath.vector4(1, 1, 1, 0))
    -- aparece gradualmente
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in)
    -- escala inicial
    local scale = 5
    gui.set_scale(star, vmath.vector3(scale, scale, 1))
    -- encolhe de volta para o lugar
    gui.animate(star, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, 0, spawn_small_stars)
end

-- inicia a animacao de aparecimento gradual da marca
local function animate_imprint(self)
    -- espera um pouco antes de a marca aparecer
    local delay = 0.8
    -- duracao do aparecimento gradual
    local fade_in = 0.2
    -- escala inicial
    local scale = 4
    gui.set_scale(self.imprint, vmath.vector4(scale, scale, 1, 0))
    -- encolhe de volta para o lugar
    gui.animate(self.imprint, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, fade_in, delay)
    -- tambem aparece gradualmente
    gui.animate(self.imprint, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_IN, fade_in, delay)
end

-- incrementa a pontuacao em um passo em direcao ao alvo
local function inc_score(self, node)
    -- quanto a pontuacao e incrementada neste passo
    local score_inc = score_inc_speed * dt
    -- nova pontuacao apos o incremento
    local new_score = self.current_score + score_inc
    for i = 1,#self.stars do
        -- inicia a animacao de uma estrela grande se cruzarmos o nivel de pontuacao para ela aparecer
        if self.current_score < self.star_levels[i] and new_score >= self.star_levels[i] then
            animate_star(self, self.stars[i])
        end
    end
    -- atualiza a pontuacao, mas limita ao alvo
    self.current_score = math.min(new_score, self.target_score)
    -- atualiza a pontuacao na tela
    gui.set_text(self.score, tostring(self.current_score))
    -- se ainda nao terminamos, continua animando e incrementando
    if self.current_score < self.target_score then
        -- quao perto estamos do alvo
        local f = self.current_score / self.target_score
        -- mistura a cor para obter um desaparecimento lento
        local c = vmath.lerp(f, self.score_start_color, self.score_end_color)
        gui.animate(self.score, gui.PROP_COLOR, c, gui.EASING_NONE, dt, 0, inc_score)
        -- nova escala para este passo
        local s = vmath.lerp(f, score_start_scale, score_end_scale)
        -- aumenta a escala pelo fator de quique
        local sp = s * score_bounce_factor
        -- anima da escala de quique de volta para a escala apropriada
        gui.set_scale(self.score, vmath.vector4(sp, sp, 1, 0))
        gui.animate(self.score, gui.PROP_SCALE, vmath.vector4(s, s, 1, 0), gui.EASING_NONE, dt)
    else
        -- terminamos, faz a marca aparecer gradualmente
        -- OBSERVACAO! em um caso real, isso deveria ser verificado contra o high score realmente armazenado
        animate_imprint(self)
    end
end

function on_message(self, message_id, message, sender)
    -- alguem nos informa que devemos exibir a cena de nivel concluido
    if message_id == hash("level_completed") then
        -- recupera a pontuacao obtida e em quais niveis de pontuacao as estrelas devem ser exibidas
        self.target_score = message.score
        self.star_levels = message.star_levels
        -- faz o titulo aparecer gradualmente ("level completed")
        local c = gui.get_color(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_COLOR, c, gui.EASING_IN, dt, 0.0, inc_score)
        c = gui.get_shadow(self.heading)
        c.w = 1
        gui.animate(self.heading, gui.PROP_SHADOW, c, gui.EASING_IN, dt, 0.0)
        -- encolhe para o lugar
        gui.animate(self.heading, gui.PROP_SCALE, vmath.vector4(1, 1, 1, 0), gui.EASING_IN, 0.2, 0.0)
    end
end

-- esta funcao e chamada quando o script e recarregado
-- ao configurar a cena e simular level complete, obtemos um fluxo de trabalho muito rapido para ajustes
function on_reload(self)
    -- garante que quaisquer alteracoes de configuracao sejam consideradas
    setup(self)
    -- simula que o nivel foi concluido
    msg.post("#gui", "level_completed", {score = 102000, star_levels = {40000, 70000, 100000}})
end
```
