---
title: Exemplo de código de HUD
brief: Neste projeto de exemplo, você aprende efeitos para contagem de pontuação.
---
# HUD - projeto de exemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/NoPHHG2kbOk" frameborder="0" allowfullscreen></iframe>

Neste projeto de exemplo, que você pode [abrir pelo editor](/manuals/project-setup/) ou [baixar do GitHub](https://github.com/defold/sample-hud), demonstramos efeitos para contagem de pontuação. As pontuações aparecem aleatoriamente pela tela, simulando um jogo em que o jogador obtém pontos em posições diferentes.

As pontuações flutuam por um tempo depois de aparecerem. Para conseguir isso, definimos as pontuações como transparentes e depois fazemos a cor aparecer gradualmente. Também as animamos para cima. Isso é feito em `on_message()` abaixo.

Depois, elas se movem para a pontuação total no topo da tela, onde são somadas.
Elas também desaparecem levemente enquanto se movem para cima. Isso é feito em `float_done()`.

Quando chegam à pontuação no topo, seus valores são adicionados a uma pontuação-alvo, em direção à qual a pontuação total faz a contagem. Isso é feito em `swoosh_done()`.

Quando o script é atualizado, ele verifica se a pontuação-alvo aumentou e se a pontuação total precisa ser contada para cima. Quando isso é verdadeiro, a pontuação total é incrementada em um passo menor.
A escala da pontuação total é então animada para criar um efeito de quique. Isso é feito em `update()`.

Cada vez que o total é incrementado, criamos uma quantidade de estrelas menores e as animamos para fora da pontuação total. As estrelas são criadas, animadas e removidas em `spawn_stars()`, `fade_out_star()` e `delete_star()`.

```lua
-- file: hud.gui_script
-- velocidade com que a pontuacao aumenta por segundo
local score_inc_speed = 1000

function init(self)
    -- a pontuacao-alvo e a pontuacao atual no jogo
    self.target_score = 0
    -- a pontuacao atual sendo contada ate a pontuacao-alvo
    self.current_score = 0
    -- a pontuacao como exibida no hud
    self.displayed_score = 0
    -- mantem uma referencia ao node que exibe a pontuacao para uso posterior abaixo
    self.score_node = gui.get_node("score")
end

local function delete_star(self, star)
    -- a estrela terminou a animacao, remova-a
    gui.delete_node(star)
end

local function fade_out_star(self, star)
    -- faz a estrela desaparecer antes da remocao
    gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0), gui.EASING_INOUT, 0.2, 0.0, delete_star)
end

local function spawn_stars(self, amount)
    -- posicao do node de pontuacao, usada para posicionar as estrelas
    local p = gui.get_position(self.score_node)
    -- distancia da posicao onde a estrela e criada
    local start_distance = 0
    -- distancia onde a estrela para
    local end_distance = 240
    -- distancia angular entre cada estrela no circulo de estrelas
    local angle_step = 2 * math.pi / amount
    -- randomiza o angulo inicial
    local angle = angle_step * math.random()
    for i=1,amount do
        -- incrementa o angulo pelo passo para obter uma distribuicao uniforme de estrelas
        angle = angle + angle_step
        -- direcao do movimento da estrela
        local dir = vmath.vector3(math.cos(angle), math.sin(angle), 0)
        -- posicoes inicial/final da estrela
        local start_p = p + dir * start_distance
        local end_p = p + dir * end_distance
        -- cria o node da estrela
        local star = gui.new_box_node(vmath.vector3(start_p.x, start_p.y, 0), vmath.vector3(30, 30, 0))
        -- define sua textura
        gui.set_texture(star, "star")
        -- define como transparente
        gui.set_color(star, vmath.vector4(1, 1, 1, 0))
        -- aparece gradualmente
        gui.animate(star, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.2, 0.0, fade_out_star)
        -- anima a posicao
        gui.animate(star, gui.PROP_POSITION, end_p, gui.EASING_NONE, 0.55)
    end
end

function update(self, dt)
    -- verifica se a pontuacao precisa ser atualizada
    if self.current_score < self.target_score then
        -- incrementa a pontuacao para este passo de tempo ate alcancar a pontuacao-alvo
        self.current_score = self.current_score + score_inc_speed * dt
        -- limita a pontuacao para que ela nao passe da pontuacao-alvo
        self.current_score = math.min(self.current_score, self.target_score)
        -- arredonda a pontuacao para baixo para exibi-la sem decimais
        local floored_score = math.floor(self.current_score)
        -- verifica se a pontuacao exibida deve ser atualizada
        if self.displayed_score ~= floored_score then
            -- atualiza a pontuacao exibida
            self.displayed_score = floored_score
            -- atualiza o texto do node de pontuacao
            gui.set_text(self.score_node, string.format("%d p", self.displayed_score))
            -- define a escala do node de pontuacao um pouco maior que o normal
            local s = 1.3
            gui.set_scale(self.score_node, vmath.vector3(s, s, s))
            -- entao anima a escala de volta para o valor original
            s = 1.0
            gui.animate(self.score_node, gui.PROP_SCALE, vmath.vector3(s, s, s), gui.EASING_OUT, 0.2)
            -- cria estrelas
            spawn_stars(self, 4)
        end
    end
end

-- esta funcao armazena a pontuacao adicionada para que a pontuacao exibida possa ser contada na funcao update
local function swoosh_done(self, node)
    -- recupera a pontuacao do node
    local amount = tonumber(gui.get_text(node))
    -- aumenta a pontuacao-alvo; veja a funcao update para saber como a pontuacao e atualizada para corresponder a ela
    self.target_score = self.target_score + amount
    -- remove a pontuacao temporaria
    gui.delete_node(node)
end

-- esta funcao anima o node depois que ele flutuou, fazendo-o partir rapidamente em direcao a pontuacao total exibida
local function float_done(self, node)
    local duration = 0.2
    -- parte rapidamente em direcao a pontuacao exibida
    gui.animate(node, gui.PROP_POSITION, gui.get_position(self.score_node), gui.EASING_IN, duration, 0.0, swoosh_done)
    -- tambem desaparece parcialmente durante esse movimento
    gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 0.6), gui.EASING_IN, duration)
end

function on_message(self, message_id, message, sender)
    -- registra a pontuacao adicionada; esta mensagem poderia ser enviada por qualquer um que queira incrementar a pontuacao
    if message_id == hash("add_score") then
        -- cria um novo node de pontuacao temporario
        local node = gui.new_text_node(message.position, tostring(message.amount))
        -- usa a fonte pequena para ele
        gui.set_font(node, "small_score")
        -- inicialmente transparente
        gui.set_color(node, vmath.vector4(1, 1, 1, 0))
        gui.set_outline(node, vmath.vector4(0, 0, 0, 0))
        -- aparece gradualmente
        gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_OUT, 0.3)
        gui.animate(node, gui.PROP_OUTLINE, vmath.vector4(0, 0, 0, 1), gui.EASING_OUT, 0.3)
        -- flutua
        local offset = vmath.vector3(0, 20, 0)
        gui.animate(node, gui.PROP_POSITION, gui.get_position(node) + offset, gui.EASING_NONE, 0.5, 0.0, float_done)
    end
end
```

No main.script, recebemos entrada de toque/mouse e então enviamos uma mensagem ao script de GUI para criar novas pontuações usando a posição do toque.

```lua
-- Ao clicar/tocar, obtem a posicao do toque e a envia por mensagem ao script de GUI hud, junto com a quantidade de pontos.

function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    local pos = vmath.vector3(action.x, action.y, 0) -- usa input action.x e action.y como posicoes x e y do toque
    if action_id == hash("touch") then
        if action.pressed then
            msg.post("main:/hud#hud", "add_score" , { position = pos, amount = 1500})
        end
    end
end
```
