---
title: Exemplo de código de parallax
brief: Neste exemplo, você aprende a usar um efeito de parallax para simular profundidade no mundo do jogo.
---
# Parallax - projeto de exemplo

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdNA7kanRQE" frameborder="0" allowfullscreen></iframe>


Neste projeto de exemplo, que você pode [abrir pelo editor](/manuals/project-setup/) ou [baixar do GitHub](https://github.com/defold/sample-parallax), demonstramos como usar um efeito de parallax para simular profundidade no mundo do jogo.
Há duas camadas de nuvens, em que uma delas parece estar mais ao fundo do que a outra. Também há um disco voador animado para dar um toque extra.

As camadas de nuvens são construídas como dois objetos de jogo separados, cada um contendo um *Tile Map* e um *Script*.
As camadas se movem em velocidades diferentes para criar o efeito de parallax. Isso é feito em `update()` de *background1.script* e *background2.script* abaixo.

```lua
-- file: background1.script

function init(self)
    msg.post("@render:", "clear_color", { color = vmath.vector4(0.52, 0.80, 1, 0) } )
end

-- o plano de fundo e um tilemap em um gameobject
-- movemos o gameobject para criar o efeito de parallax

function update(self, dt)
    -- aumenta a posicao x em 1 unidade por frame para o efeito de parallax
    local p = go.get_position()
    p.x = p.x + 1
    go.set_position(p)
end
```

```lua
-- file: background2.script

-- o plano de fundo e um tilemap em um gameobject
-- movemos o gameobject para criar o efeito de parallax

function update(self, dt)
    -- aumenta a posicao x em 0.5 unidade por frame para o efeito de parallax
    local p = go.get_position()
    p.x = p.x + 0.5
    go.set_position(p)
end
```

O disco voador é um objeto de jogo separado, contendo um *Sprite* e um *Script*.
Ele se move para a esquerda em uma velocidade constante. O movimento para cima e para baixo é obtido animando seu componente y ao redor de um valor fixo usando a função seno de Lua (`math.sin()`). Isso é feito em `update()` de *spaceship.script*.


```lua
-- file: spaceship.script

function init(self)
    -- guarda a posicao y inicial para que possamos
    -- mover a nave sem alterar o script
    self.start_y = go.get_position().y
    -- define o contador como zero. usado para o movimento com seno abaixo
    self.counter = 0
end

function update(self, dt)
    -- diminui a posicao x em 2 unidades por frame
    local p = go.get_position()
    p.x = p.x - 2

    -- move a posicao y ao redor do y inicial
    p.y = self.start_y + 8 * math.sin(self.counter * 0.08)

    -- atualiza a posicao
    go.set_position(p)

    -- remove a nave quando ela sair da tela
    if p.x < - 32 then
        go.delete()
    end

    -- incrementa o contador
    self.counter = self.counter + 1
end
```
