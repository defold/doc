---
title: Criando um jogo de 15-puzzle no Defold
brief: Se você está começando no Defold, este guia ajudará você a experimentar alguns dos blocos de construção do Defold e executar lógica em scripts.
---

# O clássico 15-puzzle

Este quebra-cabeça famoso se tornou popular nos Estados Unidos durante a década de 1870. O objetivo é organizar as peças no tabuleiro deslizando-as na horizontal e na vertical. O quebra-cabeça começa em uma posição em que as peças foram embaralhadas.

A versão mais comum do quebra-cabeça mostra os números 1--15 nas peças. Porém, você pode deixá-lo um pouco mais desafiador fazendo com que as peças sejam partes de uma imagem. Antes de começar, tente resolver o quebra-cabeça. Clique em uma peça adjacente ao quadrado vazio para deslizar a peça para a posição vazia.

## Criando o projeto

1. Inicie o Defold.
2. Selecione *New Project* à esquerda.
3. Selecione a aba *From Template*.
4. Selecione *Empty Project*
5. Selecione uma localização para o projeto no seu disco local.
6. Clique em *Create New Project*.

Abra o arquivo de configurações *game.project* e defina as dimensões do jogo para 512⨉512. Essas dimensões corresponderão à imagem que você vai usar.

![display settings](images/15-puzzle/display_settings.png)

O próximo passo é baixar uma imagem adequada para o quebra-cabeça. Escolha qualquer imagem quadrada, mas certifique-se de redimensioná-la para 512 por 512 pixels. Se não quiser sair procurando uma imagem, aqui está uma:

![Mona Lisa](images/15-puzzle/monalisa.png)

Baixe a imagem e depois arraste-a para a pasta *main* do seu projeto.

## Representando a grade

O Defold contém um componente *Tilemap* integrado que é perfeito para visualizar o tabuleiro do quebra-cabeça. Tilemaps permitem definir e ler tiles individuais, que é tudo de que você precisa neste projeto.

Mas, antes de criar o tilemap, você precisa de um *Tilesource* de onde o tilemap puxará as imagens dos tiles.

Dê <kbd>Right click</kbd> na pasta *main* e selecione <kbd>New ▸ Tile Source</kbd>. Nomeie o novo arquivo como `monalisa.tilesource`.

Defina as propriedades *Width* e *Height* do tile como 128. Isso dividirá a imagem de 512⨉512 pixels em 16 tiles. Os tiles serão numerados de 1--16 quando você os colocar no tilemap.

![Tile source](images/15-puzzle/tilesource.png)

Em seguida, dê <kbd>Right click</kbd> na pasta *main* e selecione <kbd>New ▸ Tile Map</kbd>. Nomeie o novo arquivo "grid.tilemap".

O Defold precisa que você inicialize a grade. Para fazer isso, selecione a camada "layer1" e pinte a grade 4⨉4 de tiles logo acima e à direita da origem. Não importa muito quais valores você definir para os tiles. Em instantes, você escreverá código que definirá o conteúdo desses tiles automaticamente.

![Tile map](images/15-puzzle/tilemap.png)

## Juntando as peças

Abra *main.collection*. Dê <kbd>Right click</kbd> no node raiz no *Outline* e selecione <kbd>Add Game Object</kbd>. Defina a propriedade *Id* do novo objeto de jogo como "game".

Dê <kbd>Right click</kbd> no objeto de jogo e selecione <kbd>Add Component File</kbd>. Selecione o arquivo *grid.tilemap*. Defina a propriedade *Id* como "tilemap".

Dê <kbd>Right click</kbd> no objeto de jogo e selecione <kbd>Add Component ▸ Label</kbd>. Defina a propriedade *Id* do label como "done" e sua propriedade *Text* como "Well done". Mova o label para o centro do tilemap.

Defina a posição Z do label como 1 para garantir que ele seja desenhado por cima da grade.

![Main collection](images/15-puzzle/main_collection.png)

Em seguida, crie um arquivo de script Lua para a lógica do quebra-cabeça: dê <kbd>right click</kbd> na pasta *main* e selecione <kbd>New ▸ Script</kbd>. Nomeie o novo arquivo como "game.script".

Depois, dê <kbd>Right click</kbd> no objeto de jogo chamado "game" em *main.collection* e selecione <kbd>Add Component File</kbd>. Selecione o arquivo *game.script*.

Execute o jogo. Você deve ver a grade como a desenhou e o label com a mensagem "Well done" por cima.

## A lógica do quebra-cabeça

Agora todas as peças estão no lugar, então o restante do tutorial será dedicado a montar a lógica do quebra-cabeça.

O script manterá sua própria representação das peças do tabuleiro, separada do tilemap. Isso porque é possível facilitar a operação sobre esses dados. Em vez de armazenar os tiles em um array bidimensional, eles são armazenados como uma lista unidimensional em uma tabela Lua. A lista contém o número do tile em sequência, começando pelo canto superior esquerdo da grade até o canto inferior direito:

```lua
-- O tabuleiro completo fica assim:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

O código que recebe uma lista de tiles como essa e a desenha no nosso tilemap é bem simples, mas precisa converter a posição na lista em uma posição x e y:

```lua
-- Desenha uma lista de tiles em uma tabela sobre um tilemap 4x4
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. Em tilemaps, o tile com valor x 1 e valor y 1 fica no canto inferior esquerdo. Portanto, a posição y precisa ser invertida.

Você pode verificar se a função funciona como esperado criando uma função `init()` de teste:

```lua
function init(self)
    -- Um tabuleiro invertido, para teste
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

Com os tiles em uma lista de tabela Lua, embaralhar a ordem é muito fácil. O código simplesmente percorre cada elemento da lista e troca cada tile por outro tile escolhido aleatoriamente:

```lua
-- Troca dois itens em uma lista de tabela
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomiza a ordem dos elementos em uma lista de tabela
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

Antes de seguir, há algo sobre o 15-puzzle que você realmente precisa considerar: se você randomizar a ordem dos tiles como está fazendo acima, há 50% de chance de que o quebra-cabeça seja *impossível* de resolver.

Isso é um problema, já que você definitivamente não quer apresentar ao jogador um quebra-cabeça que não pode ser resolvido.

Felizmente, é possível descobrir se uma configuração é solucionável ou não. Veja como:

## Solucionabilidade

Para descobrir se uma posição em um quebra-cabeça 4⨉4 é solucionável, duas informações são necessárias:

1. O número de "inversões" na configuração. Uma inversão ocorre quando um tile vem antes de outro tile com número menor. Por exemplo, dada a lista `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}`, ela tem 3 inversões:

    - o número 12 tem 11 e 10 depois dele, gerando 2 inversões.
    - o número 11 tem 10 depois dele, gerando mais 1 inversão.

    (Observe que o estado resolvido do quebra-cabeça tem zero inversões)

2. A linha em que o quadrado vazio está (representado por `0` na lista).

Esses dois números podem ser calculados com as seguintes funções:

```lua
-- Conta o numero de inversoes em uma lista de tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. Observe que o quadrado vazio não conta.

```lua
-- Encontra a posicao x e y de um tile especifico
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. Posição Y a partir de baixo.

Agora, com esses dois números, é possível dizer se um estado do quebra-cabeça é solucionável ou não. Um estado de tabuleiro 4⨉4 é *solucionável* se:

- Se o quadrado vazio estiver em uma linha *ímpar* (1 ou 3 contando de baixo) e o número de inversões for *par*.
- Se o quadrado vazio estiver em uma linha *par* (2 ou 4 contando de baixo) e o número de inversões for *ímpar*.

## Como isso funciona?

Cada movimento legal move uma peça trocando seu lugar com o quadrado vazio, na horizontal ou na vertical.

Mover uma peça na horizontal não altera o número de inversões nem altera o número da linha em que você encontra o quadrado vazio.

Mover uma peça na vertical, porém, muda a paridade do número de inversões (de ímpar para par, ou de par para ímpar). Isso também muda a paridade da linha do quadrado vazio.

Por exemplo:

![sliding a piece](images/15-puzzle/slide.png)

Esse movimento altera a ordem dos tiles de:

`{ ... 0, 11, 2, 13, 6 ... }`

para

`{ ... 6, 11, 2, 13, 0 ... }`

O novo estado adiciona 3 inversões da seguinte forma:

- O número 6 adiciona 1 inversão (o número 2 agora está depois do 6)
- O número 11 perde 1 inversão (o número 6 agora está antes do 11)
- O número 13 perde 1 inversão (o número 6 agora está antes do 13)

As formas possíveis de o número de inversões mudar com um deslizamento vertical são ±1 ou ±3.

As formas possíveis de a linha do quadrado vazio mudar com um deslizamento vertical são ±1.

No estado final do quebra-cabeça, o quadrado vazio está no canto inferior direito (a linha *ímpar* 1) e o número de inversões é o valor *par* 0. Cada movimento legal mantém esses dois valores intactos (movimento horizontal) ou troca sua polaridade (movimento vertical). Nenhum movimento legal jamais pode tornar a polaridade das inversões e da linha do quadrado vazio *ímpar*, *ímpar* ou *par*, *par*.

Portanto, qualquer estado do quebra-cabeça em que os dois números sejam ambos ímpares ou ambos pares é impossível de resolver.

Aqui está o código que verifica a solucionabilidade:

```lua
-- A lista de tabela dada com tiles 4x4 e solucionavel?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## Entrada do usuário

A única coisa que resta fazer agora é tornar o quebra-cabeça interativo.

Crie uma função `init()` que faça toda a configuração em tempo de execução usando as funções criadas acima:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. Informe à engine que este objeto de jogo deve receber entrada.
2. Inicialize o randomizador.
3. Crie um estado inicial aleatório para o tabuleiro.
4. Se o estado não for solucionável, embaralhe novamente.
5. Desenhe o tabuleiro.
6. Defina uma flag de conclusão para rastrear o estado de vitória.
7. Desative o label da mensagem de conclusão.

Abra */input/game.input_bindings* e adicione um novo *Mouse Trigger*. Defina o nome da ação como "press":

![input](images/15-puzzle/input.png)

Volte para o script e crie uma função `on_input()`.

```lua
-- Lida com a entrada do usuario
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. Se houver um clique do botão do mouse e o jogo ainda estiver em execução, faça o seguinte.
2. Calcule os quadrados x e y em que o usuário clicou.
3. Encontre a localização atual do quadrado vazio (0).
4. Se o quadrado clicado estiver logo acima, abaixo, à esquerda ou à direita do quadrado vazio, faça o seguinte:
5. Troque os tiles do quadrado clicado e do quadrado vazio.
6. Redesenhe o tabuleiro atualizado.
7. Se o número de inversões no tabuleiro for 0, significando que tudo está na ordem correta, e o quadrado vazio estiver na coluna mais à direita (ele precisa estar na última linha para que as inversões sejam 0), então o quebra-cabeça está resolvido; portanto, faça o seguinte:
8. Defina a flag de conclusão.
9. Ative/mostre a mensagem de conclusão.

E é isso! Você terminou, o jogo de quebra-cabeça está completo!

## O script completo

Aqui está o código completo do script para referência:

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## Exercícios adicionais

1. Faça um quebra-cabeça 5⨉5 e depois um 6⨉5. Certifique-se de que as verificações de solucionabilidade funcionem de forma geral.
2. Adicione animações de deslizamento. Os tiles não podem ser movidos separadamente do tilemap, então você precisará encontrar uma forma de resolver isso. Talvez um tilemap separado que contenha apenas a peça que está deslizando?
