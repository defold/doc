---
title: Tutorial de platformer no Defold
brief: Neste artigo, você passa pela implementação de um platformer 2D básico baseado em tiles no Defold. As mecânicas que você aprende são mover para esquerda/direita, pular e cair.
---

# Platformer

Neste artigo, passamos pela implementação de um platformer 2D básico baseado em tiles no Defold. As mecânicas que aprenderemos são mover para esquerda/direita, pular e cair.

Há muitas formas diferentes de criar um platformer. Rodrigo Monteiro escreveu uma análise exaustiva sobre o assunto e mais [aqui](http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/).

Recomendamos muito a leitura se você está começando a criar platformers, pois ela contém muitas informações valiosas. Entraremos em um pouco mais de detalhe sobre alguns dos métodos descritos e sobre como implementá-los no Defold. Ainda assim, tudo deve ser fácil de portar para outras plataformas e linguagens (usamos Lua no Defold).

Assumimos que você conhece um pouco de matemática vetorial (álgebra linear). Se não conhece, é uma boa ideia estudar o assunto, já que ele é extremamente útil para desenvolvimento de jogos. David Rosen, da Wolfire, escreveu uma série muito boa sobre isso [aqui](http://blog.wolfire.com/2009/07/linear-algebra-for-game-developers-part-1/).

Se você já está usando o Defold, pode criar um novo projeto baseado no template-project _Platformer_ e experimentá-lo enquanto lê este artigo.

::: sidenote
Alguns leitores comentaram que nosso método sugerido não é possível com a implementação padrão do Box2D. Fizemos algumas modificações no Box2D para isso funcionar:

Colisões entre objetos cinemáticos e estáticos são ignoradas. Altere as verificações em `b2Body::ShouldCollide` e `b2ContactManager::Collide`.

Além disso, a distância de contato (chamada separation no Box2D) não é fornecida à função de callback.
Adicione um membro de distância a `b2ManifoldPoint` e certifique-se de que ele seja atualizado nas funções `b2Collide*`.
:::

## Detecção de colisão

A detecção de colisão é necessária para impedir que o jogador atravesse a geometria do nível.
Há várias formas de lidar com isso, dependendo do seu jogo e dos requisitos específicos dele.
Uma das formas mais fáceis, quando possível, é deixar uma engine de física cuidar disso.
No Defold, usamos a engine de física [Box2D](http://box2d.org/) para jogos 2D.
A implementação padrão do Box2D não tem todos os recursos necessários; veja o final deste artigo para saber como a modificamos.

Uma engine de física armazena os estados dos objetos físicos junto com suas formas para simular comportamento físico. Ela também reporta colisões durante a simulação, para que o jogo possa reagir conforme elas acontecem. Na maioria das engines de física há três tipos de objetos: objetos _static_, _dynamic_ e _kinematic_ (esses nomes podem ser diferentes em outras engines de física). Há outros tipos de objetos também, mas vamos ignorá-los por enquanto.

- Um objeto *static* nunca se move (por exemplo, geometria do nível).
- Um objeto *dynamic* é influenciado por forças e torques, que são transformados em velocidades durante a simulação.
- Um objeto *kinematic* é controlado pela lógica da aplicação, mas ainda afeta outros objetos dinâmicos.

Em um jogo como este, buscamos algo que se pareça com comportamento físico do mundo real, mas controles responsivos e mecânicas equilibradas são muito mais importantes. Um pulo que pareça bom não precisa ser fisicamente preciso nem agir sob gravidade real. [Esta](http://hypertextbook.com/facts/2007/mariogravity.shtml) análise mostra, porém, que a gravidade nos jogos Mario se aproxima cada vez mais de 9,8 m/s<sup>2</sup> a cada versão. :-)

É importante termos controle total sobre o que está acontecendo para podermos projetar e ajustar as mecânicas até alcançar a experiência pretendida. É por isso que escolhemos modelar o personagem do jogador como um objeto cinemático. Assim, podemos mover o personagem livremente, sem precisar lidar com forças físicas. Isso significa que teremos que resolver nós mesmos a separação entre o personagem e a geometria do nível (mais sobre isso depois), mas esse é um custo que estamos dispostos a aceitar. Representaremos o personagem do jogador por uma forma de caixa no mundo físico.

## Movimento

Agora que decidimos que o personagem do jogador será representado por um objeto cinemático, podemos movê-lo livremente definindo a posição. Vamos começar com o movimento para esquerda/direita.

O movimento será baseado em aceleração, para dar uma sensação de peso ao personagem. Como em um veículo comum, a aceleração define quão rápido o personagem do jogador consegue alcançar a velocidade máxima e mudar de direção. A aceleração atua durante o time-step do frame---geralmente fornecido em um parâmetro `dt` (delta-`t`)---e então é adicionada à velocidade. De forma semelhante, a velocidade atua durante o frame e a translação resultante é adicionada à posição. Em matemática, isso é chamado de [integração ao longo do tempo](http://en.wikipedia.org/wiki/Integral).

![Approximative velocity integration](images/platformer/integration.png)

As duas linhas verticais marcam o início e o fim do frame. A altura das linhas é a velocidade que o personagem do jogador tem nesses dois pontos no tempo. Vamos chamar essas velocidades de `v0` e `v1`. `v1` é dada pela aplicação da aceleração (a inclinação da curva) durante o time-step `dt`:

![Equation of velocity](images/platformer/equationofvelocity.png)

A área laranja é a translação que devemos aplicar ao personagem do jogador durante o frame atual. Geometricamente, podemos aproximar a área como:

![Equation of translation](images/platformer/equationoftranslation.png)

É assim que integramos a aceleração e a velocidade para mover o personagem no loop de atualização:

1. Determine a velocidade-alvo com base na entrada
2. Calcule a diferença entre nossa velocidade atual e a velocidade-alvo
3. Defina a aceleração para atuar na direção da diferença
4. Calcule a mudança de velocidade neste frame (`dv` é abreviação de delta-velocity), como acima:

    ```lua
    local dv = acceleration * dt
    ```

5. Verifique se `dv` excede a diferença de velocidade pretendida; se exceder, limite o valor
6. Salve a velocidade atual para uso posterior (`self.velocity`, que neste momento é a velocidade usada no frame anterior):

    ```lua
    local v0 = self.velocity
    ```

7. Calcule a nova velocidade adicionando a mudança de velocidade:

    ```lua
    self.velocity = self.velocity + dv
    ```

8. Calcule a translação em x neste frame integrando a velocidade, como acima:

    ```lua
    local dx = (v0 + self.velocity) * dt * 0.5
    ```

9. Aplique isso ao personagem do jogador

Se você não tiver certeza de como lidar com entrada no Defold, há um guia sobre isso [aqui](/manuals/input).

Neste ponto, conseguimos mover o personagem para a esquerda e para a direita, com uma sensação suave e com peso nos controles. Agora, vamos adicionar gravidade!

Gravidade também é uma aceleração, mas afeta o jogador ao longo do eixo y. Isso significa que ela será aplicada da mesma maneira que a aceleração de movimento descrita acima. Se simplesmente mudarmos os cálculos acima para vetores e garantirmos que incluímos a gravidade no componente y da aceleração no passo 3), tudo funcionará. Tem como não gostar de matemática vetorial? :-)

## Resposta de colisão

Agora nosso personagem do jogador pode se mover e cair, então é hora de olhar para as respostas de colisão.
Obviamente precisamos pousar e nos mover ao longo da geometria do nível. Usaremos os pontos de contato fornecidos pela engine de física para garantir que nunca fiquemos sobrepostos a nada.

Um ponto de contato carrega uma _normal_ do contato (apontando para fora do objeto com que colidimos, embora isso possa ser diferente em outras engines), além de uma _distância_, que mede quanto penetramos no outro objeto. Isso é tudo de que precisamos para separar o jogador da geometria do nível.
Como estamos usando uma caixa, podemos receber múltiplos pontos de contato durante um frame. Isso acontece, por exemplo, quando dois cantos da caixa intersectam o chão horizontal ou quando o jogador se move para dentro de um canto.

![Contact normals acting on the player character](images/platformer/collision.png)

Para evitar aplicar a mesma correção várias vezes, acumulamos as correções em um vetor para garantir que não vamos compensar demais. Isso nos faria acabar longe demais do objeto com que colidimos. Na imagem acima, você pode ver que temos atualmente dois pontos de contato, visualizados pelas duas setas (normais). A distância de penetração é a mesma para ambos os contatos; se a usássemos cegamente a cada vez, acabaríamos movendo o jogador duas vezes mais do que o necessário.

::: sidenote
É importante redefinir as correções acumuladas a cada frame para o vetor 0.
Coloque algo assim no final da função `update()`:
`self.corrections = vmath.vector3()`
:::

Assumindo que exista uma função de callback chamada para cada ponto de contato, veja como fazer a separação nessa função:

```lua
local proj = vmath.dot(self.correction, normal) -- <1>
local comp = (distance - proj) * normal -- <2>
self.correction = self.correction + comp -- <3>
go.set_position(go.get_position() + comp) -- <4>
```

1. Projete o vetor de correção sobre a normal do contato (o vetor de correção é o vetor 0 no primeiro ponto de contato)
2. Calcule a compensação que precisamos fazer para este ponto de contato
3. Adicione-a ao vetor de correção
4. Aplique a compensação ao personagem do jogador

Também precisamos cancelar a parte da velocidade do jogador que se move em direção ao ponto de contato:

```lua
proj = vmath.dot(self.velocity, message.normal) -- <1>
if proj < 0 then
    self.velocity = self.velocity - proj * message.normal -- <2>
end
```
1. Projete a velocidade sobre a normal
2. Se a projeção for negativa, significa que parte da velocidade aponta em direção ao ponto de contato; nesse caso, remova esse componente

## Pulo

Agora que podemos correr sobre a geometria do nível e cair, é hora de pular! Pulos em platformers podem ser feitos de muitas formas diferentes. Neste jogo, buscamos algo parecido com Super Mario Bros e Super Meat Boy. Ao pular, o personagem do jogador é impulsionado para cima por um impulso, que é basicamente uma velocidade fixa.

A gravidade puxará continuamente o personagem para baixo novamente, resultando em um arco de pulo agradável. Enquanto está no ar, o jogador ainda pode controlar o personagem. Se o jogador soltar o botão de pulo antes do pico do arco, a velocidade para cima é reduzida para interromper o pulo prematuramente.

1. Quando a entrada for pressionada, faça:

    ```lua
    -- jump_takeoff_speed e uma constante definida em outro lugar
    self.velocity.y = jump_takeoff_speed
    ```

    Isso só deve ser feito quando a entrada é _pressionada_, não a cada frame em que ela fica continuamente _segurada_.

2. Quando a entrada for liberada, faça:

    ```lua
    -- interrompe o pulo se ainda estivermos subindo
    if self.velocity.y > 0 then
        -- reduz a velocidade para cima
        self.velocity.y = self.velocity.y * 0.5
    end
    ```

ExciteMike fez alguns gráficos interessantes dos arcos de pulo em [Super Mario Bros 3](http://meyermike.com/wp/?p=175) e [Super Meat Boy](http://meyermike.com/wp/?p=160), que valem a pena conferir.

## Geometria do nível

A geometria do nível são as formas de colisão do ambiente com as quais o personagem do jogador (e possivelmente outras coisas) colide. No Defold, há duas formas de criar essa geometria.

Você pode criar formas de colisão separadas sobre os níveis que constrói. Esse método é muito flexível e permite posicionamento fino dos gráficos. Ele é especialmente útil se você quer inclinações suaves.
O jogo [Braid](http://braid-game.com/) usou esse método para construir níveis, e também é o método usado pelo nível de exemplo neste tutorial. Veja como fica no editor Defold:

![The Defold Editor with the level geometry and player placed into the world](images/platformer/editor.png)

Outra opção é construir níveis com tiles e deixar que o editor gere automaticamente as formas de física com base nos gráficos dos tiles. Isso significa que a geometria do nível será atualizada automaticamente quando você alterar os níveis, o que pode ser extremamente útil.

Os tiles colocados terão suas formas de física mescladas automaticamente em uma só se estiverem alinhados.
Isso elimina lacunas que podem fazer seu personagem parar ou bater ao deslizar por vários tiles horizontais. Isso é feito substituindo os polígonos dos tiles por edge shapes no Box2D em tempo de carregamento.

![Multiple tile-based polygons stitched into one](images/platformer/stitching.png)

Acima há um exemplo em que criamos cinco tiles vizinhos a partir de uma parte dos gráficos do platformer. Na imagem, você pode ver como os tiles colocados (acima) correspondem a uma única forma costurada em uma só (contorno cinza abaixo).

Confira nossos guias sobre [física](/manuals/physics) e [tiles](/manuals/2dgraphics) para mais informações.

## Palavras finais

Se você quiser mais informações sobre mecânicas de platformer, há uma quantidade impressionante de informações sobre a física em [Sonic](http://info.sonicretro.org/Sonic_Physics_Guide).

Se você testar nosso projeto template em um dispositivo iOS ou com mouse, o pulo pode parecer bem estranho.
É apenas nossa frágil tentativa de fazer platforming com entrada de um toque. :-)

Não falamos sobre como tratamos as animações neste jogo. Você pode ter uma ideia conferindo o *player.script* abaixo; procure a função `update_animations()`.

Esperamos que essas informações tenham sido úteis!
Faça um ótimo platformer para que todos possamos jogar! <3

## Código

Aqui está o conteúdo de *player.script*:

```lua
-- player.script

-- estes sao os ajustes das mecanicas; fique a vontade para altera-los para obter uma sensacao diferente
-- a aceleracao para mover para direita/esquerda
local move_acceleration = 3500
-- fator de aceleracao a usar quando estiver no ar
local air_acceleration_factor = 0.8
-- velocidade maxima para direita/esquerda
local max_speed = 450
-- gravidade puxando o jogador para baixo em unidades de pixel
local gravity = -1000
-- velocidade de decolagem ao pular em unidades de pixel
local jump_takeoff_speed = 550
-- intervalo em que um toque duplo deve ocorrer para ser considerado um pulo (usado apenas para controles mouse/touch)
local touch_jump_timeout = 0.2

-- prehashing de ids melhora a performance
local msg_contact_point_response = hash("contact_point_response")
local msg_animation_done = hash("animation_done")
local group_obstacle = hash("obstacle")
local input_left = hash("left")
local input_right = hash("right")
local input_jump = hash("jump")
local input_touch = hash("touch")
local anim_run = hash("run")
local anim_idle = hash("idle")
local anim_jump = hash("jump")
local anim_fall = hash("fall")

function init(self)
    -- isto nos permite lidar com entrada neste script
    msg.post(".", "acquire_input_focus")

    -- velocidade inicial do jogador
    self.velocity = vmath.vector3(0, 0, 0)
    -- variavel de suporte para acompanhar colisoes e separacao
    self.correction = vmath.vector3()
    -- se o jogador esta no chao ou nao
    self.ground_contact = false
    -- entrada de movimento no intervalo [-1,1]
    self.move_input = 0
    -- a animacao em execucao no momento
    self.anim = nil
    -- temporizador que controla a janela de pulo ao usar mouse/touch
    self.touch_jump_timer = 0
end

local function play_animation(self, anim)
    -- reproduz apenas animacoes que ainda nao estao em execucao
    if self.anim ~= anim then
        -- informa ao sprite para reproduzir a animacao
        sprite.play_flipbook("#sprite", anim)
        -- lembra qual animacao esta tocando
        self.anim = anim
    end
end

local function update_animations(self)
    -- garante que o personagem do jogador olhe para o lado certo
    sprite.set_hflip("#sprite", self.move_input < 0)
    -- garante que a animacao correta esteja tocando
    if self.ground_contact then
        if self.velocity.x == 0 then
            play_animation(self, anim_idle)
        else
            play_animation(self, anim_run)
        end
    else
        if self.velocity.y > 0 then
            play_animation(self, anim_jump)
        else
            play_animation(self, anim_fall)
        end
    end
end

function update(self, dt)
    -- determina a velocidade-alvo com base na entrada
    local target_speed = self.move_input * max_speed
    -- calcula a diferenca entre nossa velocidade atual e a velocidade-alvo
    local speed_diff = target_speed - self.velocity.x
    -- a aceleracao completa a integrar neste frame
    local acceleration = vmath.vector3(0, gravity, 0)
    if speed_diff ~= 0 then
        -- define a aceleracao para atuar na direcao da diferenca
        if speed_diff < 0 then
            acceleration.x = -move_acceleration
        else
            acceleration.x = move_acceleration
        end
        -- diminui a aceleracao quando no ar para dar uma sensacao mais lenta
        if not self.ground_contact then
            acceleration.x = air_acceleration_factor * acceleration.x
        end
    end
    -- calcula a mudanca de velocidade neste frame (dv e abreviacao de delta-velocity)
    local dv = acceleration * dt
    -- verifica se dv excede a diferenca de velocidade pretendida; nesse caso, limita
    if math.abs(dv.x) > math.abs(speed_diff) then
        dv.x = speed_diff
    end
    -- salva a velocidade atual para uso posterior
    -- (self.velocity, que neste momento e a velocidade usada no frame anterior)
    local v0 = self.velocity
    -- calcula a nova velocidade adicionando a mudanca de velocidade
    self.velocity = self.velocity + dv
    -- calcula a translacao neste frame integrando a velocidade
    local dp = (v0 + self.velocity) * dt * 0.5
    -- aplica isso ao personagem do jogador
    go.set_position(go.get_position() + dp)

    -- atualiza o temporizador de pulo
    if self.touch_jump_timer > 0 then
        self.touch_jump_timer = self.touch_jump_timer - dt
    end

    update_animations(self)

    -- redefine o estado volatil
    self.correction = vmath.vector3()
    self.move_input = 0
    self.ground_contact = false

end

local function handle_obstacle_contact(self, normal, distance)
    -- projeta o vetor de correcao sobre a normal do contato
    -- (o vetor de correcao e o vetor 0 no primeiro ponto de contato)
    local proj = vmath.dot(self.correction, normal)
    -- calcula a compensacao que precisamos fazer para este ponto de contato
    local comp = (distance - proj) * normal
    -- adiciona ao vetor de correcao
    self.correction = self.correction + comp
    -- aplica a compensacao ao personagem do jogador
    go.set_position(go.get_position() + comp)
    -- verifica se a normal aponta para cima o suficiente para considerar que o jogador esta no chao
    -- (0.7 e aproximadamente igual a 45 graus de desvio da direcao vertical pura)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- projeta a velocidade sobre a normal
    proj = vmath.dot(self.velocity, normal)
    -- se a projecao for negativa, significa que parte da velocidade aponta para o ponto de contato
    if proj < 0 then
        -- nesse caso, remove esse componente
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    -- verifica se recebemos uma mensagem de ponto de contato
    if message_id == msg_contact_point_response then
        -- verifica se o objeto e algo que consideramos um obstaculo
        if message.group == group_obstacle then
            handle_obstacle_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- permite pular apenas a partir do chao
    -- (estenda isto com um contador para fazer coisas como pulos duplos)
    if self.ground_contact then
        -- define a velocidade de decolagem
        self.velocity.y = jump_takeoff_speed
        -- reproduz animacao
        play_animation(self, anim_jump)
    end
end

local function abort_jump(self)
    -- interrompe o pulo se ainda estivermos subindo
    if self.velocity.y > 0 then
        -- reduz a velocidade para cima
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == input_left then
        self.move_input = -action.value
    elseif action_id == input_right then
        self.move_input = action.value
    elseif action_id == input_jump then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    elseif action_id == input_touch then
        -- move em direcao ao ponto de toque
        local diff = action.x - go.get_position().x
        -- fornece entrada apenas quando estiver longe (mais de 10 pixels)
        if math.abs(diff) > 10 then
            -- desacelera quando estiver a menos de 100 pixels de distancia
            self.move_input = diff / 100
            -- limita a entrada a [-1,1]
            self.move_input = math.min(1, math.max(-1, self.move_input))
        end
        if action.released then
            -- inicia a contagem da ultima liberacao para ver se estamos prestes a pular
            self.touch_jump_timer = touch_jump_timeout
        elseif action.pressed then
            -- pula com toque duplo
            if self.touch_jump_timer > 0 then
                jump(self)
            end
        end
    end
end
```
