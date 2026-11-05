---
title: Manual de animações flip-book no Defold
brief: Este manual descreve como usar animações flip-book no Defold.
---

# Animação flip-book

Uma animação flipbook consiste em uma série de imagens estáticas exibidas em sequência. A técnica é muito semelhante à animação tradicional em células (consulte http://en.wikipedia.org/wiki/Traditional_animation). Ela oferece possibilidades ilimitadas, pois cada frame pode ser manipulado individualmente. No entanto, armazenar muitas imagens distintas pode exigir bastante memória de textura. A suavidade da animação também depende do número de imagens exibidas por segundo, mas aumentar esse número geralmente também aumenta o trabalho necessário. As animações flipbook do Defold são armazenadas como imagens individuais adicionadas a um [Atlas](/manuals/atlas) ou como tiles em uma [fonte de tiles](/manuals/tilesource). Animações de fontes de tiles usam uma lista *Frames* para selecionar tiles da grade de imagens em qualquer ordem, incluindo repetições.

  ![Folha de animação](images/animation/animsheet.png){.inline}
  ![Loop de corrida](images/animation/runloop.gif){.inline}

## Reproduzindo animações flip-book

Sprites e nodes GUI do tipo box podem reproduzir animações flip-book, e você tem bastante controle sobre elas em tempo de execução.

Sprites
: Para executar uma animação em tempo de execução, use a função [`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]). Veja um exemplo abaixo.

Nodes GUI do tipo box
: Para executar uma animação em tempo de execução, use a função [`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]). Veja um exemplo abaixo.

::: sidenote
O modo de reprodução `Once Ping Pong` reproduz a animação até o último frame e então inverte a ordem e reproduz de volta até o **segundo** frame da animação, não até o primeiro. Isso é feito para facilitar o encadeamento de animações.
:::

### Exemplo de sprite

Suponha que seu jogo tenha um recurso de "dodge" que permite ao jogador pressionar um botão específico para esquivar. Você criou quatro animações para dar feedback visual ao recurso:

"idle"
: Uma animação em loop do personagem do jogador parado.

"dodge_idle"
: Uma animação em loop do personagem do jogador parado enquanto está em posição de esquiva.

"start_dodge"
: Uma animação de transição executada uma vez, levando o personagem do jogador da posição em pé para a esquiva.

"stop_dodge"
: Uma animação de transição executada uma vez, levando o personagem do jogador da esquiva de volta para a posição em pé.

O script a seguir fornece a lógica:

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" é nossa ação de entrada
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- lembra que estamos esquivando
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- não estamos mais esquivando
            self.dodge = false
        end
    end
end
```

### Exemplo de node GUI do tipo box

Ao selecionar uma animação ou imagem para um node, você na verdade atribui a fonte da imagem (atlas ou tile source) e a animação padrão de uma vez. A fonte da imagem é definida estaticamente no node, mas a animação atual a reproduzir pode ser alterada em tempo de execução. Imagens estáticas são tratadas como animações de um frame, então alterar uma imagem em tempo de execução equivale a reproduzir uma animação flip-book diferente no node:

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- Isso exige que o node tenha uma animação padrão no mesmo atlas ou tile source que
    -- a nova animação/imagem que estamos reproduzindo.
    gui.play_flipbook(character_node, "jump_left")
end
```


## Callbacks de conclusão

As funções `sprite.play_flipbook()` e `gui.play_flipbook()` aceitam uma função callback Lua opcional como último argumento. Essa função será chamada quando a animação terminar de reproduzir. A função nunca é chamada para animações em loop. O callback pode ser usado para disparar eventos ao concluir a animação ou para encadear várias animações. Exemplos:

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
