---
title: Tutorial Magic Link
brief: Neste tutorial, você vai criar um pequeno jogo de quebra-cabeça completo, com tela inicial, mecânicas de jogo e progressão simples de níveis na forma de dificuldade crescente.
---

# Tutorial Magic Link

Este jogo é uma variação dos clássicos jogos de combinação no estilo de _Bejeweled_ e _Candy Crush_. O jogador arrasta e conecta blocos da mesma cor para removê-los, mas o objetivo do jogo não é remover longas sequências de blocos da mesma cor, limpar o tabuleiro ou acumular pontos, e sim fazer com que um conjunto de "blocos mágicos" especiais espalhados pelo tabuleiro se conecte.

Este tutorial foi escrito como um guia passo a passo em que criamos o jogo a partir de um design completo. Na prática, leva bastante tempo e esforço para encontrar um design que funcione. Você pode começar com uma ideia central e então encontrar uma forma de prototipá-la para entender melhor o que essa ideia pode trazer. Até mesmo um jogo simples como "Magic Link" exige bastante trabalho de design. Este jogo passou por algumas iterações e experimentos até chegar à sua forma final (ainda longe de ser perfeita) e ao seu conjunto de regras. Mas, neste tutorial, vamos pular esse processo e começar a construir a partir do design final.

## Primeiros passos

Você precisa começar criando um novo projeto e importando o pacote de assets:

* Crie um [novo projeto](/manuals/project-setup/#creating-a-new-project) a partir do modelo "Empty Project"
* Baixe o projeto "Magic Link" completo [magic-link.zip](https://github.com/defold/defold-examples/releases/latest) como referência. O projeto completo contém todos os assets, caso você queira criar o projeto do zero.

## Regras do jogo

![Esquema das regras do jogo](images/magic-link/linker_rules.png)

O tabuleiro é preenchido aleatoriamente com blocos coloridos e um conjunto de blocos mágicos a cada rodada. Os blocos coloridos seguem estas regras:

* Eles desaparecem se o jogador os conectar (arrastando) com blocos da mesma cor.
* Quando os blocos desaparecem, deixam buracos abaixo. Os blocos coloridos simplesmente caem verticalmente nos buracos que se abriram abaixo.
* A parte inferior da tela impede que todos os blocos continuem caindo.

Os blocos mágicos se comportam de forma diferente, de acordo com estas regras:

* Blocos mágicos se movem _para os lados_ se aparecer uma abertura em qualquer um dos lados.
* Se aparecer um buraco abaixo, eles caem como blocos coloridos comuns.

O jogador interage com o jogo de acordo com as seguintes regras:

* O jogador pode arrastar e conectar blocos coloridos adjacentes horizontalmente, verticalmente e diagonalmente.
* Os blocos conectados desaparecem assim que o jogador solta a entrada de toque (levanta o dedo).
* Blocos mágicos não reagem ao arrasto e não podem ser conectados manualmente.
* No entanto, blocos mágicos reagem quando são conectados horizontal ou verticalmente. Ou seja, eles se conectam automaticamente nessas circunstâncias.
* O nível é concluído se o jogador conseguir conectar automaticamente todos os blocos mágicos no tabuleiro.

O nível de dificuldade controla o número de blocos mágicos colocados no tabuleiro.

## Visão geral

Como em todos os projetos, precisamos traçar um plano geral de como abordar a implementação. Há muitas formas de estruturar e construir este jogo. Tecnicamente, poderíamos implementar o jogo inteiro no sistema de GUI se quiséssemos. No entanto, criar o jogo com objetos de jogo e sprites e usar as APIs de GUI para elementos de GUI na tela e HUD costuma ser a forma natural de construir um jogo, então vamos seguir esse caminho.

Como esperamos que o número de arquivos permaneça relativamente baixo, vamos manter a estrutura de pastas do projeto bem simples:

![Estrutura de pastas](images/magic-link/linker_folders.png)

*main*
: Esta pasta conterá toda a lógica do jogo. Todos os scripts, arquivos de objeto de jogo, arquivos de coleção, arquivos de GUI e assim por diante ficarão nesta pasta. Se você quiser dividir esta pasta em várias ou manter subpastas, tudo bem.

*images*
: Todos os assets de imagem ficarão nesta pasta.

*fonts*
: As fontes usadas para renderização de texto ficam aqui.

*input*
: Os mapeamentos de entrada ficam nesta pasta.

## Configurando o projeto

O arquivo *game.project* será mantido em grande parte com as configurações padrão, mas há algumas configurações a decidir. Antes de tudo, precisamos escolher uma resolução para o jogo. É bem fácil alterar a resolução mais tarde e, em um jogo final, precisaríamos fazer algum trabalho para que o jogo fique bom independentemente da resolução ou da proporção de tela do dispositivo-alvo.

Escolhemos definir a resolução como 640x960 pixels, que é a resolução nativa do iPhone 4. Ela também cabe em muitos monitores, então testar o jogo no computador fica tranquilo. Se quiser trabalhar com uma resolução diferente, você só terá que ajustar alguns valores de outra forma.

![Configurações do projeto](images/magic-link/linker_project_settings.png)

Também precisamos aumentar o número máximo de sprites renderizados. Se quiser, você pode pular para a próxima seção e voltar aqui quando for avisado no console de que atingiu o limite de sprites.

![Layout de escala do jogo](images/magic-link/linker_layout.png)

Podemos calcular o número máximo de sprites necessário:

* O tabuleiro do jogo terá 7x9 blocos. O tabuleiro precisará de algumas margens nas bordas e também de espaço no topo para alguns elementos de GUI. Isso significa que os blocos terão cerca de 90x90 pixels. Qualquer tamanho menor que isso deixaria os blocos pequenos demais para interagir em uma tela pequena de telefone.
* Cada bloco é um sprite. Vamos usar animações de um único frame para definir a cor do bloco.
* Alguns blocos serão blocos mágicos, e vamos usar 4 sprites para efeitos especiais em cada um deles.
* Os gráficos de conexão precisarão de um sprite por elemento. No pior caso, isso acrescenta mais 61 sprites, se o jogador de alguma forma conectar todo o tabuleiro (menos 2 blocos mágicos que não podem ser conectados por arrasto).

Então, suponha que tenhamos no máximo 30 blocos mágicos. O tabuleiro tem 63 blocos (sprites). Desses, os 30 blocos mágicos adicionam 4 sprites para efeitos especiais. Isso acrescenta 120 sprites. Portanto, com os gráficos de conexão (que neste caso chegam a no máximo 33), precisaremos desenhar pelo menos 120 + 33 = 153 sprites a cada frame. A potência de dois mais próxima é 256.

No entanto, definir o máximo como 256 não é suficiente. Sempre que limpamos e reiniciamos o tabuleiro, vamos excluir todos os objetos de jogo atuais e criar novos. A contagem de sprites precisa acomodar todos os objetos que permanecem vivos durante o frame. Isso inclui objetos excluídos, porque eles são removidos no fim do frame. Portanto, definir o número máximo de sprites como 512 será suficiente.

![Contagem máxima de sprites](images/magic-link/linker_sprite_max_count.png)

## Adicionando os assets gráficos

Todos os assets necessários para o jogo foram preparados com antecedência. Vamos adicioná-los como imagens de 512x512 pixels e deixar a engine reduzi-las para o tamanho-alvo.

::: sidenote
Ativar *hidpi* nas configurações do projeto significa que o back buffer passa a ter alta resolução. Ao desenhar imagens grandes reduzidas na tela, elas aparecerão muito nítidas em telas Retina.
:::

![Adicionar imagens](images/magic-link/linker_add_images.png)

Além dos blocos, há uma imagem de "connector" e sprites de efeito. Também temos duas imagens de fundo: uma será usada como plano de fundo do tabuleiro do jogo e a outra será usada no menu principal. Adicione todas as imagens à pasta *images* e então crie um arquivo de atlas *sprites.atlas*. Abra o arquivo de atlas e adicione todas as imagens.

![Adicionar imagens ao Atlas](images/magic-link/linker_add_to_atlas.png)

Há um conjunto de imagens de GUI usadas para criar elementos de GUI, como botões e popups. Elas são adicionadas a um atlas separado chamado *gui.atlas*.

## Gerando o tabuleiro

O primeiro passo é construir a lógica do tabuleiro. O tabuleiro ficará em sua própria coleção, que conterá tudo que aparece na tela durante o gameplay. Por enquanto, o necessário é apenas o componente de fábrica "blockfactory" e o script. Mais tarde, adicionaremos uma fábrica para conexões, componentes de GUI do menu principal e, por fim, a mecânica de carregamento para iniciar o gameplay a partir do menu principal e uma forma de voltar ao menu.

1. Crie *`board.collection`* na pasta *`main`*. Certifique-se de nomeá-la como "board" para podermos endereçá-la mais tarde. Se você adicionar o componente de sprite de fundo, defina sua posição Z como -1, ou ele não será desenhado atrás de todos os blocos que criaremos depois.
2. Defina temporariamente *Main Collection* (em *Bootstrap*) no *game.project* como `/main/board.collection` para facilitar os testes.

![Coleção do tabuleiro](images/magic-link/linker_board_collection.png)

![Bootstrap da coleção do tabuleiro](images/magic-link/linker_bootstrap_board.png)

O arquivo de script *board.script* conterá toda a lógica do próprio tabuleiro e dos blocos no tabuleiro. Comece criando a função que constrói o tabuleiro e invoque-a (temporariamente) a partir de `init()`. Também vamos adicionar duas funções que não usaremos agora, mas que serão úteis mais tarde:

`filter()`
: Esta função permitirá filtrar listas de itens (blocos).

`build_blocklist()`
: Cria uma lista de todos os blocos do tabuleiro organizada como uma lista plana, o que permite filtrá-la.

Depois que o tabuleiro for construído, usaremos dois conjuntos de dados diferentes contendo todos os blocos, `self.blocks` e `self.board`:

```lua
-- board.script
go.property("timer", 0)     -- Usado para cronometrar eventos
local blocksize = 80        -- Distância entre os centros dos blocos
local edge = 40             -- Borda esquerda e direita.
local bottom_edge = 50      -- Borda inferior.
local boardwidth = 7        -- Número de colunas
local boardheight = 9       -- Número de linhas
local centeroff = vmath.vector3(8, -8, 0) -- Deslocamento central do gfx do conector, pois há sombra abaixo na img do bloco
local dropamount = 3        -- O número de blocos soltos em um "drop"
local colors = { hash("orange"), hash("pink"), hash("blue"), hash("yellow"), hash("green") }

--
-- filter(function, table)
-- ex.: filter(is_even, {1,2,3,4}) -> {2,4}
--
local function filter(func, tbl)
    local new = {}
    for i, v in pairs(tbl) do
        if func(v) then
            new[i] = v
        end
    end
    return new
end

--
-- Cria uma lista de blocos em 1 dimensão para facilitar a filtragem
--
local function build_blocklist(self)
    self.blocks = {}
    for x, l in pairs(self.board) do
        for y, b in pairs(self.board[x]) do
            table.insert(self.blocks, { id = b.id, color = b.color, x = b.x, y = b.y })
        end
    end
end

--
-- INIT
--
function init(self)
    self.board = {}             -- Contém a estrutura do tabuleiro
    self.blocks = {}            -- Lista de todos os blocos. Usada para facilitar a filtragem na seleção.
    self.chain = {}             -- Cadeia de seleção atual
    self.connectors = {}        -- Elementos conectores para marcar a cadeia de seleção
    self.num_magic = 3          -- Número de blocos mágicos no tabuleiro
    self.drops = 1              -- Número de drops disponíveis
    self.magic_blocks = {}      -- Blocos mágicos que estão alinhados
    self.dragging = false       -- Entrada de toque por arrasto
    msg.post(".", "acquire_input_focus")
    msg.post("#", "start_level")
end

local function build_board(self)
    math.randomseed(os.time())
    local pos = vmath.vector3()
    local c
    local x = 0
    local y = 0
    for x = 0,boardwidth-1 do
        pos.x = edge + blocksize / 2 + blocksize * x
        self.board[x] = {}
        for y = 0,boardheight-1 do
            pos.y = bottom_edge + blocksize / 2 + blocksize * y
            -- Calcula z
            pos.z = x * -0.1 + y * 0.01 -- <1>
            c = colors[math.random(#colors)]    -- Escolhe uma cor aleatória
            local id = factory.create("#blockfactory", pos, null, { color = c })
            self.board[x][y] = { id = id, color = c,  x = x, y = y }
        end
    end

    -- Cria uma lista 1d que podemos filtrar facilmente.
    build_blocklist(self)
end

function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        build_board(self)
    end
end
```
1. Observe que, como os gráficos dos blocos se sobrepõem, precisamos desenhá-los na ordem correta. Isso é feito definindo a coordenada z de cada bloco. O valor ficará bem acima de -1, onde temos o sprite de fundo.

A lógica do tabuleiro cria objetos de jogo "`block`" por meio do componente de fábrica "`blockfactory`". Precisamos construir o objeto de jogo do bloco para que isso funcione. O bloco tem um script e um sprite. Definimos a animação padrão do sprite como qualquer um dos blocos coloridos em *`sprites.atlas`* e então adicionamos código a *`block.script`* para fazer o bloco assumir a cor correta quando for criado:

![Objeto de jogo de bloco](images/magic-link/linker_block.png)

```lua
-- block.script
go.property("color", hash("none"))

function init(self)
    go.set_scale(0.18)        -- renderiza reduzido

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end
```

Defina o *Prototype* do componente de fábrica "blockfactory" para o novo arquivo de objeto de jogo *block.go*.

![Fábrica de blocos](images/magic-link/linker_blockfactory.png)

Agora você deve conseguir executar o jogo e ver o tabuleiro preenchido com blocos de cores aleatórias:

![Primeira captura de tela](images/magic-link/linker_first_screenshot.png)

## Interações

Agora que temos um tabuleiro, devemos adicionar interação do usuário. Primeiro, definimos os mapeamentos de entrada em *game.input_binding* na pasta *input*. Certifique-se de que as configurações de *game.project* usem seu arquivo de mapeamento de entrada.

![Mapeamentos de entrada](images/magic-link/linker_input_bindings.png)

Precisamos de apenas um mapeamento e vamos atribuir `MOUSE_BUTTON_LEFT` ao nome de ação "touch". Este jogo não usa multitoque e, por conveniência, o Defold traduz a entrada de toque de um dedo em cliques do botão esquerdo do mouse.

A responsabilidade de lidar com a entrada fica com o tabuleiro, então precisamos adicionar código para isso em *board.script*:

```lua
-- board.script
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.value == 1 then
        -- Qual bloco foi tocado ou recebeu o arrasto?
        local x = math.floor((action.x - edge) / blocksize)
        local y = math.floor((action.y - bottom_edge) / blocksize)

        if x < 0 or x >= boardwidth or y < 0 or y >= boardheight or self.board[x][y] == nil then
            -- fora do tabuleiro.
            return
        end

        if action.pressed then
            -- O jogador iniciou o toque
            msg.post(self.board[x][y].id, "make_orange")

            self.dragging = true
        elseif self.dragging then
            -- então arrasta
            msg.post(self.board[x][y].id, "make_green")
        end
    elseif action_id == hash("touch") and action.released then
        -- O jogador soltou o toque.
        self.dragging = false
    end
end
```

As mensagens `make_orange` e `make_green` são apenas temporárias para obter retorno visual de que o código funciona. Precisamos adicionar código a *block.script* para tratar essas mensagens:

```lua
-- block.script
function on_message(self, message_id, message, sender)
    if message_id == hash("make_orange") then
        sprite.play_flipbook("#sprite", hash("orange"))
    elseif message_id == hash("make_green") then
        sprite.play_flipbook("#sprite", hash("green"))
    end
end
```

Agora os blocos receberão primeiro uma mensagem `make_orange` e depois mensagens `make_green` enquanto você tocar (ou pressionar o mouse), então é provável que os blocos apenas pisquem em laranja (se isso for perceptível) antes de ficarem verdes. Mas agora sabemos qual bloco o jogador toca! Se quiser rastrear como a entrada é tratada com mais detalhes, insira chamadas `print()` ou `pprint()` no código.

## Marcar conexões

Agora precisamos de assets para o marcador que será usado para indicar quando os blocos são conectados pelo jogador. A ideia é simplesmente sobrepor um gráfico em cada bloco para mostrar que ele está conectado.

Precisamos criar um objeto de jogo "connector", que contém a imagem de sprite do conector, além de um componente de fábrica "connector factory" no objeto de jogo "board":

![Objeto de jogo connector](images/magic-link/linker_connector.png)

![Fábrica de conectores](images/magic-link/linker_connector_factory.png)

O script deste objeto de jogo é mínimo: ele só precisa escalar os gráficos para que combinem com o resto do jogo e definir corretamente a ordem Z.

```lua
-- connector.script
function init(self)
    go.set_scale(0.18)              -- Define a escala deste objeto de jogo.
    go.set(".", "position.z", 1)    -- Coloca no topo.
end
```

A função `same_color_neighbors()` retorna uma lista de blocos adjacentes a um bloco específico (na posição x, y) e da mesma cor. Esta função usa a função `filter()` aplicada à lista plana completa de blocos em `self.blocks`.

```lua
-- board.script
--
-- Retorna uma lista de blocos vizinhos da mesma cor que o
-- bloco em x, y
--
local function same_color_neighbors(self, x, y)
    local f = function (v)
        return (v.id ~= self.board[x][y].id) and
               (v.x == x or v.x == x - 1 or v.x == x + 1) and
               (v.y == y or v.y == y - 1 or v.y == y + 1) and
               (v.color == self.board[x][y].color)
    end
    return filter(f, self.blocks)
end
```

Uma função auxiliar `in_blocklist()` verifica se um bloco existe em uma lista de blocos:

```lua
-- board.script
--
-- O bloco existe na lista de blocos?
--
local function in_blocklist(blocks, block)
    for i, b in pairs(blocks) do
        if b.id == block then
            return true
        end
    end
    return false
end
```

Usamos essas funções durante a entrada de toque e arrasto em `on_input()` para construir as conexões de blocos tocadas. Aqui, também testaremos e ignoraremos blocos mágicos, mesmo que ainda não exista nenhum:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    -- Se estiver tentando manipular blocos mágicos, ignore.
    if self.board[x][y].color == hash("magic") then
        return
    end

    if action.pressed then
        -- Lista de vizinhos da mesma cor que o bloco tocado
        self.neighbors = same_color_neighbors(self, x, y)
        self.chain = {}
        table.insert(self.chain, self.board[x][y])

        -- Marca o bloco.
        p = go.get_position(self.board[x][y].id)
        local id = factory.create("#connectorfactory", p + centeroff)
        table.insert(self.connectors, id)

        self.dragging = true
    elseif self.dragging then
        -- então arrasta
        if in_blocklist(self.neighbors, self.board[x][y].id) and not in_blocklist(self.chain, self.board[x][y].id) then
            -- arrastando sobre um vizinho da mesma cor
            table.insert(self.chain, self.board[x][y])
            self.neighbors = same_color_neighbors(self, x, y)

            -- Marca o bloco.
            p = go.get_position(self.board[x][y].id)
            local id = factory.create("#connectorfactory", p + centeroff)
            table.insert(self.connectors, id)
        end
    end
```

E, por fim, ao soltar o toque, removemos visualmente todos os conectores de conexão.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- O jogador soltou o toque.
        self.dragging = false

        -- Esvazia a cadeia de gráficos conectores.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
end
```

![Conectores no jogo](images/magic-link/linker_connector_screen.png)

## Remover blocos conectados

Agora temos a lógica pronta para permitir a conexão de blocos da mesma cor, e simplesmente remover os blocos conectados é fácil. O motivo de definirmos a posição no tabuleiro como `hash("removing")` em vez de apenas `nil` é que, mais tarde, quando fizermos a lógica dos blocos mágicos, precisaremos garantir que eles deslizem apenas para blocos recém-removidos. Se definíssemos a posição no tabuleiro como `nil` aqui, não teríamos como distinguir entre blocos recém-removidos e blocos que já haviam sido removidos antes.

```lua
-- board.script
-- Remove a cadeia de blocos atualmente selecionada
--
local function remove_chain(self)
    -- Exclui todos os blocos encadeados
    for i, c in ipairs(self.chain) do
        self.board[c.x][c.y] = hash("removing")
        go.delete(c.id)
    end
    self.chain = {}
end
```

Também precisaremos de uma função para remover de fato (definir como `nil`) as posições do tabuleiro que foram definidas como `hash("removing")`:

```lua
-- board.script
--
-- Define blocos removidos como nil
--
local function nilremoved(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] == hash("removing") then
                self.board[x][y] = nil
            end
        end
    end
end
```

Também criamos uma função que desliza os blocos restantes para baixo conforme os blocos abaixo deles são removidos (definidos como `nil`). Iteramos pelo tabuleiro coluna por coluna, da esquerda para a direita, e percorremos cada coluna de baixo para cima. Se encontrarmos uma posição vazia (`nil`), deslizamos todos os blocos acima dessa posição para baixo.

```lua
-- board.script
--
-- Aplica a lógica de deslocamento para baixo a todos os blocos.
--
local function slide_board(self)
    -- Desliza todos os blocos restantes para baixo, para espaços vazios.
    -- Ir coluna por coluna facilita isso.
    local dy = 0
    local pos = vmath.vector3()
    for x = 0,boardwidth - 1 do
        dy = 0
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil then
                if dy > 0 then
                    -- Move para baixo dy passos
                    self.board[x][y - dy] = self.board[x][y]
                    self.board[x][y] = nil
                    -- Calcula nova posição
                    self.board[x][y - dy].y = self.board[x][y - dy].y - dy
                    go.animate(self.board[x][y-dy].id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * (y - dy), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula novo z
                    go.set(self.board[x][y-dy].id, "position.z", x * -0.1 + (y-dy) * 0.01)
                end
            else
                dy = dy + 1
            end
        end
    end
    -- blocklist precisa ser atualizada
    build_blocklist(self)
end
```

![Deslizar blocos para baixo](images/magic-link/linker_blocks_slide.png)

Agora podemos simplesmente adicionar chamadas a essas funções em `on_input()` quando o toque for solto e houver blocos em `self.chain`.

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- O jogador soltou o toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Há uma cadeia de blocos. Remove-a do tabuleiro e desliza os blocos restantes para baixo.
            remove_chain(self)
            nilremoved(self)
            slide_board(self)
        end

        -- Esvazia a cadeia de gráficos conectores.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

## Lógica dos blocos mágicos

Agora é hora de adicionar os blocos mágicos ao conjunto. Primeiro, vamos adicionar a capacidade de um bloco se tornar um bloco mágico. Assim, podemos fazer uma passagem separada no tabuleiro preenchido e converter os blocos desejados em blocos mágicos. Para deixar os blocos mágicos mais interessantes, vamos primeiro criar um efeito mágico animado na forma de um objeto de jogo *`magic_fx.go`*, que poderemos criar a partir do bloco mágico.

![Magic_fx.go](images/magic-link/linker_magic_fx.png)

Este objeto de jogo contém dois sprites. Um é a cor "magic" (um sprite usando a imagem *`magic-sphere_layer2.png`*) e o outro é um efeito de "light" (um sprite usando a imagem *`magic-sphere_layer3.png`*). O objeto é configurado para girar quando é criado, dependendo do valor da propriedade `direction`. Também fazemos o objeto escutar duas mensagens: `lights_on` e `lights_off`, que controlam o sprite de efeito de luz.

Crie um novo script e adicione-o como componente de script a *`magic_fx.go`*:

```lua
-- magic_fx.script
go.property("direction", hash("left"))

function init(self)
    msg.post("#", "lights_off")
    if self.direction == hash("left") then
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, 360,  go.EASING_LINEAR, 3 + math.random())
    else
        go.set(".", "euler.z", 0)
        go.animate(".", "euler.z", go.PLAYBACK_LOOP_FORWARD, -360,  go.EASING_LINEAR, 2 + math.random())
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("lights_on") then
        msg.post("#light", "enable")
    elseif message_id == hash("lights_off") then
        msg.post("#light", "disable")
    end
end
```

Agora, o bloco mágico criará dois objetos de jogo `magic_fx` ao receber a mensagem `make_magic`. Cada um girará na direção oposta, criando uma bela dança de cores dentro dos blocos. Também adicionamos outro sprite a *`block.go`* com a imagem *`magic-sphere_layer4.png`*. Essa imagem fica em um Z mais alto que o efeito criado e desenha a casca ou "cover" da esfera mágica.

![Sprite de cover](images/magic-link/linker_cover.png)

Observe que precisamos adicionar um componente *Factory* ao objeto de jogo do bloco e dizer a ele para usar nosso objeto de jogo *`magic_fx.go`* como *Prototype*. O script do bloco também precisa escutar as mensagens `lights_on` e `lights_off` e propagá-las para os objetos criados. Note que os objetos criados precisam ser excluídos quando o bloco for excluído. Isso é tratado na função `final()` do bloco. Tudo isso acontece em *`block.script`*.

```lua
-- block.script
function init(self)
    go.set_scale(0.18) -- renderiza reduzido

    self.fx1 = nil
    self.fx2 = nil

    msg.post("#cover", "disable")

    if self.color ~= nil then
        sprite.play_flipbook("#sprite", self.color)
    else
        msg.post("#sprite", "disable")
    end
end

function final(self)
    if self.fx1 ~= nil then
        go.delete(self.fx1)
    end

    if self.fx2 ~= nil then
        go.delete(self.fx2)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("make_magic") then
        self.color = hash("magic")
        msg.post("#cover", "enable")
        msg.post("#sprite", "enable")
        sprite.play_flipbook("#sprite", hash("magic-sphere_layer1"))

        self.fx1 = factory.create("#fxfactory", p, nil, { direction = hash("left") })
        self.fx2 = factory.create("#fxfactory", p, nil, { direction = hash("right") })

        go.set_parent(self.fx1, go.get_id())
        go.set_parent(self.fx2, go.get_id())

        go.set(self.fx1, "position.z", 0.01)
        go.set(self.fx1, "scale", 1)
        go.set(self.fx2, "position.z", 0.02)
        go.set(self.fx2, "scale", 1)
    elseif message_id == hash("lights_on") or message_id == hash("lights_off") then
        msg.post(self.fx1, message_id)
        msg.post(self.fx2, message_id)
    end
end
```

Agora conseguimos transformar blocos em blocos mágicos e também acendê-los, um efeito que usaremos para indicar que um bloco mágico está ao lado de outro bloco mágico.

![Bloco mágico sem e com luz](images/magic-link/linker_magic_blocks.png)

O código que preenche o tabuleiro com blocos agora precisa ser alterado para que tenhamos alguns blocos mágicos nele:

```lua
-- board.script
local function build_board(self)

    ...

    -- Distribui blocos mágicos.
    local rand_x = 0
    local rand_y
    for y = 0, boardheight - 1, boardheight / self.num_magic do
        local set = false
        while not set do
            rand_y = math.random(math.floor(y), math.min(boardheight - 1, math.floor(y + boardheight / self.num_magic)))
            rand_x = math.random(0, boardwidth - 1)
            if self.board[rand_x][rand_y].color ~= hash("magic") then
                msg.post(self.board[rand_x][rand_y].id, "make_magic")
                self.board[rand_x][rand_y].color = hash("magic")
                set = true
            end
        end
    end

    -- Cria uma lista 1d que podemos filtrar facilmente.
    build_blocklist(self)
end
```

A mecânica principal dos blocos mágicos é a capacidade de deslizar para os lados quando outro bloco desaparece ao lado deles. Refletimos todos os detalhes dessa mecânica na função `slide_magic_blocks()` em *board.script*. O algoritmo é simples:

1. Para cada linha do tabuleiro, crie uma lista `M` de blocos mágicos.
2. Itere por cada bloco mágico na lista `M` até que ela pare de diminuir. A cada iteração:
    1. Se o bloco mágico tiver uma posição de bloco `hash("removing")` abaixo dele, apenas remova-o da lista `M`.
    2. Se o bloco mágico tiver um buraco ao lado marcado com `hash("removing")`, deslize-o para lá, defina sua posição antiga como `hash("removing")` e então remova-o da lista `M`.

```lua
-- board.script
-- Aplica a lógica de deslocamento aos blocos mágicos. Desliza apenas para posições
-- marcadas para remoção com hash("removing")
--
local function slide_magic_blocks(self)
    -- Desliza todos os blocos mágicos para o lado que deve deslizar primeiro.
    -- Isso funciona melhor linha por linha!
    local row_m
    for y = 0,boardheight - 1 do
        row_m = {}
        -- Cria lista de blocos mágicos nesta linha.
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil and self.board[x][y] ~= hash("removing") and self.board[x][y].color == hash("magic") then
                table.insert(row_m, self.board[x][y])
            end
        end

        local mc = #row_m + 1
        -- Percorre a lista, desliza e remove se possível. Repete até que a lista não diminua.
        while #row_m < mc do
            mc = #row_m
            for i, m in pairs(row_m) do
                local x = m.x
                if y > 0 and self.board[x][y-1] == hash("removing") then
                    -- Buraco abaixo, não faz nada.
                    row_m[i] = nil
                elseif x > 0 and self.board[x-1][y] == hash("removing") then
                    -- Buraco à esquerda! Desliza o bloco mágico para lá
                    self.board[x-1][y] = self.board[x][y]
                    self.board[x-1][y].x = x - 1
                    go.animate(self.board[x][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x - 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula novo z
                    go.set(self.board[x][y].id, "position.z", (x - 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Será definido como nil depois
                    row_m[i] = nil
                elseif x < boardwidth - 1 and self.board[x + 1][y] == hash("removing") then
                    -- Buraco à direita. Desliza o bloco mágico para lá
                    self.board[x+1][y] = self.board[x][y]
                    self.board[x+1][y].x = x + 1
                    go.animate(self.board[x+1][y].id, "position.x", go.PLAYBACK_ONCE_FORWARD, edge + blocksize / 2 + blocksize * (x + 1), go.EASING_OUTBOUNCE, 0.3)
                    -- Calcula novo z
                    go.set(self.board[x+1][y].id, "position.z", (x + 1) * -0.1 + y * 0.01)
                    self.board[x][y] = hash("removing") -- Será definido como nil depois
                    row_m[i] = nil
                end
            end
        end
    end
end
```

Podemos testar a mecânica adicionando uma chamada para a função em `on_input()`:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- O jogador soltou o toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Há uma cadeia de blocos. Remove-a do tabuleiro
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Desliza os blocos restantes para baixo.
            slide_board(self)
        end
        self.chain = {}
        -- Esvaziar a cadeia limpa os gráficos conectores.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Agora fica claro por que usamos a "tag" intermediária `hash("removing")` nas posições ao removê-las. Sem ela, os blocos mágicos deslizariam para frente e para trás para qualquer posição vazia ao lado. Talvez fosse uma mecânica interessante, mas não é a que queremos para este pequeno jogo.

Agora precisamos de lógica para detectar se blocos mágicos estão conectados (à esquerda, à direita, acima ou abaixo uns dos outros) e precisamos saber se todos os blocos mágicos no tabuleiro estão conectados. O algoritmo usado é bem direto:

1. Crie uma lista `M` de todos os blocos mágicos no tabuleiro.
2. Para cada bloco na lista `M`:
    1. Se o bloco não tiver `region` definido, atribua a ele o número de região `R` (inicialmente `1`).
    2. Marque todos os vizinhos não marcados do bloco com o mesmo número de região `R` e siga iterando para os vizinhos deles, os vizinhos dos vizinhos, e assim por diante.
    3. Aumente o número de região `R` em `1`.

![Marcar regiões](images/magic-link/linker_regions.png)

Esta é a implementação do algoritmo:

```lua
-- board.script
--
-- Cria lista de todos os blocos mágicos atuais.
--
local function magic_blocks(self)
    local magic = {}
    for x = 0,boardwidth - 1 do
        for y = 0,boardheight - 1 do
            if self.board[x][y] ~= nil and self.board[x][y].color == hash("magic") then
                table.insert(magic, self.board[x][y])
            end
        end
    end
    return magic
end

--
-- Filtra blocos mágicos adjacentes
--
local function adjacent_magic_blocks(blocks, block)
    return filter(function (e)
        return (block.x == e.x and math.abs(block.y - e.y) == 1) or
            (block.y == e.y and math.abs(block.x - e.x) == 1)
    end, blocks)
end

--
-- Espalha a região para os vizinhos
--
local function mark_neighbors(blocks, block, region)
    local neighbors = adjacent_magic_blocks(blocks, block)
    for i, m in pairs(neighbors) do
        if m.region == nil then
            m.region = region
            mark_neighbors(blocks, m, region)
        end
    end
end

--
-- Marca todas as regiões dos blocos mágicos
--
local function mark_magic_regions(self)
    local m_blocks = magic_blocks(self)
    -- 1. Limpa todas as marcas de região e conta vizinhos
    for i, m in pairs(m_blocks) do
        m.region = nil
        local n = 0
        for _ in pairs(adjacent_magic_blocks(m_blocks, m)) do n = n + 1 end
        m.neighbors = n
    end

    -- 2. Atribui regiões e as espalha
    local region = 1
    for i, m in pairs(m_blocks) do
        if m.region == nil then
            m.region = region
            mark_neighbors(m_blocks, m, region)
            region = region + 1
        end
    end
    return m_blocks
end
```

Também criamos funções que nos permitem contar o número de regiões entre os blocos mágicos. Se o número de regiões for 1, sabemos que todos os blocos mágicos estão conectados. Além disso, adicionamos uma função que apaga as luzes em todos os blocos mágicos e outra que acende os efeitos de luz nos blocos mágicos que têm blocos mágicos vizinhos:

```lua
-- board.script
--
-- Conta o número de regiões conectadas entre os blocos mágicos.
--
local function count_magic_regions(blocks)
    local maxr = 0
    for i, m in pairs(blocks) do
        if m.region > maxr then
            maxr = m.region
        end
    end
    return maxr
end

--
-- Apaga as luzes de todos os blocos mágicos listados
--
local function shutdown_lined_up_magic(self)
    for i, m in ipairs(self.lined_up_magic) do
        msg.post(m.id, "lights_off")
    end
end

--
-- Define destaque para todos os blocos mágicos
--
local function highlight_magic(blocks)
    for i, m in pairs(blocks) do
        if m.neighbors > 0 then
            msg.post(m.id, "lights_on")
        else
            msg.post(m.id, "lights_off")
        end
    end
end
```

Agora podemos inserir esses trechos de lógica no fluxo geral. Primeiro, como a geração do tabuleiro é aleatória, há uma pequena chance de ele começar em estado de vitória. Se isso acontecer, descartamos o tabuleiro e o criamos novamente:

```lua
-- board.script
--
-- Limpa o tabuleiro
--
local function clear_board(self)
    for y = 0,boardheight - 1 do
        for x = 0,boardwidth - 1 do
            if self.board[x][y] ~= nil then
                go.delete(self.board[x][y].id)
                self.board[x][y] = nil
            end
        end
    end
end

local function build_board(self)

    ...

    -- Cria uma lista 1d que podemos filtrar facilmente.
    build_blocklist(self)

    local magic_blocks = mark_magic_regions(self)
    if count_magic_regions(magic_blocks) == 1 then
        -- "Vitória" desde o início. Cria novo tabuleiro.
        clear_board(self)
        build_board(self)
    end
    highlight_magic(magic_blocks)
end
```

O restante da lógica cabe em `on_input()`. Ainda não há código para lidar com a mensagem `level_completed`, mas por enquanto não há problema:

```lua
-- board.script
function on_input(self, action_id, action)

    ...

    elseif action_id == hash("touch") and action.released then
        -- O jogador soltou o toque.
        self.dragging = false

        if #self.chain > 1 then
            -- Há uma cadeia de blocos. Remove-a do tabuleiro e preenche o tabuleiro novamente.
            remove_chain(self)
            slide_magic_blocks(self)
            nilremoved(self)
            -- Desliza os blocos restantes para baixo.
            slide_board(self)

            local magic_blocks = mark_magic_regions(self)
            -- Destaca blocos mágicos adjacentes.
            if count_magic_regions(magic_blocks) == 1 then
                -- Vitória!
                msg.post("#", "level_completed")
            end
            highlight_magic(magic_blocks)
        end
        self.chain = {}
        -- Esvaziar a cadeia limpa os gráficos conectores.
        for i, c in ipairs(self.connectors) do
            go.delete(c)
        end
        self.connectors = {}
    end
```

Agora é possível jogar e chegar ao estado de vitória, embora ainda nada aconteça quando você conecta todos os blocos mágicos.

![Primeira vitória](images/magic-link/linker_first_win.png)

## Drops

A ideia do "drop" é adicionar uma mecânica simples de progressão. O jogador pode executar um número limitado de "drops", que simplesmente soltam algumas novas peças aleatórias no tabuleiro, pressionando o botão *DROP*. O jogador começa com um drop e, cada vez que um nível é concluído, recebe um drop adicional. O código da mecânica de drop cabe em duas funções: uma que retorna uma lista de possíveis posições onde os drops podem cair, e outra que executa o drop de fato, com animação e tudo.

```lua
-- board.script
--
-- Encontra posições para um drop.
--
local function dropspots(self)
    local spots = {}
    for x = 0, boardwidth - 1 do
        for y = 0, boardheight - 1 do
            if self.board[x][y] == nil then
                table.insert(spots, { x = x, y = y })
                break
            end
        end
    end
    -- Se houver mais que dropamount, remove aleatoriamente um slot até chegar a dropamount
    for c = 1, #spots - dropamount do
        table.remove(spots, math.random(#spots))
    end
    return spots
end

--
-- Executa o drop
--
local function drop(self, spots)
    for i, s in pairs(spots) do
        local pos = vmath.vector3()
        pos.x = edge + blocksize / 2 + blocksize * s.x
        pos.y = 1000
        c = colors[math.random(#colors)]    -- Escolhe uma cor aleatória
        local id = factory.create("#blockfactory", pos, null, { color = c })
        go.animate(id, "position.y", go.PLAYBACK_ONCE_FORWARD, bottom_edge + blocksize / 2 + blocksize * s.y, go.EASING_OUTBOUNCE, 0.5)
        -- Calcula novo z
        go.set(id, "position.z", s.x * -0.1 + s.y * 0.01)

        self.board[s.x][s.y] = { id = id, color = c,  x = s.x, y = s.y }
    end

    -- Recria blocklist
    build_blocklist(self)
end
```

Podemos testar os drops executando o seguinte, por exemplo, em `on_reload()`, ou vinculando isso a uma ação de entrada temporária:

```lua
s = dropspots(self)
if #s > 0 then
    -- Executa o drop
    drop(self, s)
end
```

![Drop](images/magic-link/linker_drop.png)

## O menu principal

Agora é hora de juntar tudo. Antes de tudo, vamos criar uma tela inicial e separá-la do tabuleiro. O passo 1 é criar uma *main_menu.gui* e configurá-la com um botão *Start* (um node de texto e um node box texturizado), um node de texto de título e alguns blocos decorativos (nodes box texturizados). O script *main_menu.gui_script* que anexamos à GUI anima os blocos decorativos em `init()`. Ele também contém um `on_input()` que envia uma mensagem `start_game` para um script principal. Criaremos esse script em instantes.

![GUI do menu principal](images/magic-link/linker_main_menu.png)

```lua
-- main_menu.gui_script
function init(self)
    msg.post(".", "acquire_input_focus")

    local bs = { "brick1", "brick2", "brick3", "brick4", "brick5", "brick6" }
    for i, b in ipairs(bs) do
        local n = gui.get_node(b)
        local rt = (math.random() * 3) + 1
        local a = math.random(-45, 45)
        gui.set_color(n, vmath.vector4(1, 1, 1, 0))

        gui.animate(n, "position.y", -100 - math.random(0, 50), gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "color.w", 1, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
        gui.animate(n, "rotation.z", a, gui.EASING_INSINE, 1 + rt, 0, nil, gui.PLAYBACK_LOOP_FORWARD)
    end

    gui.animate(gui.get_node("start"), "color.x", 1, gui.EASING_INOUTSINE, 1, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local start = gui.get_node("start")

        if gui.pick_node(start, action.x, action.y) then
            msg.post("/main#script", "start_game")
        end
    end
end
```

Como em breve o trabalho de iniciar o jogo será feito pelo script do menu principal, remova a chamada temporária de configuração do tabuleiro em `init()` em *board.script*:

```lua
-- board.script
--
-- INIT
--
function init(self)
    self.board = {}                -- Contém a estrutura do tabuleiro
    self.blocks = {}            -- Lista de todos os blocos. Usada para facilitar a filtragem na seleção.

    self.chain = {}                -- Cadeia de seleção atual
    self.connectors = {}        -- Elementos conectores para marcar a cadeia de seleção
    self.num_magic = 3            -- Número de blocos mágicos no tabuleiro

    self.drops = 1                -- Número de drops disponíveis

    self.magic_blocks = {}        -- Blocos mágicos que estão alinhados

    self.dragging = false        -- Entrada de toque por arrasto
end
```

O script principal manterá o estado geral do jogo e iniciará o jogo quando solicitado. O que queremos fazer aqui é fazer com que *main.collection* contenha apenas a quantidade mínima de assets necessários para mostrar a tela inicial. Fazemos isso deixando *main.collection* conter um objeto de jogo "main" que mantém a GUI do menu principal, um componente de script e, mais importante, um componente *Collection Proxy*.

O proxy de coleção (collection proxy) nos permite carregar e descarregar coleções dinamicamente no jogo em execução. Ele age em nome de um arquivo de coleção especificado, e carregamos, inicializamos, habilitamos, desabilitamos e descarregamos a coleção dinâmica enviando mensagens ao proxy. Para uma descrição completa de como usá-los, consulte a [documentação de Collection Proxy](/manuals/collection-proxy).

No nosso caso, definimos a propriedade *Collection* do componente de proxy de coleção como *board.collection*, que contém o "level".

![coleção main](images/magic-link/linker_main_collection.png)

Agora devemos abrir *game.project* e alterar o *main_collection* de bootstrap para `/main/main.collectionc`.

![coleção main de bootstrap](images/magic-link/linker_bootstrap_main.png)

Agora, iniciar um jogo significa enviar mensagens ao nosso proxy de coleção para carregar, inicializar e habilitar o tabuleiro, e então desabilitar o menu principal (para que ele não apareça). Voltar ao menu principal faz o inverso (desde que o proxy tenha carregado a coleção).

```lua
-- main.script
function init(self)
    msg.post("#", "to_main_menu")
    self.state = "MAIN_MENU"
end

function on_message(self, message_id, message, sender)
    if message_id == hash("to_main_menu") then
        if self.state ~= "MAIN_MENU" then
            msg.post("#boardproxy", "unload")
        end
        msg.post("main:/main#menu", "enable") -- <1>
        self.state = "MAIN_MENU"
    elseif message_id == hash("start_game") then
        msg.post("#boardproxy", "load")
        msg.post("#menu", "disable")
    elseif message_id == hash("proxy_loaded") then
        -- A coleção do tabuleiro foi carregada...
        msg.post(sender, "init")
        msg.post("board:/board#script", "start_level", { difficulty = 1 }) -- <2>
        msg.post(sender, "enable")
        self.state = "GAME_RUNNING"
    end
end
```
1. Observe que chamamos o socket de "main", que é um nome que precisamos garantir que esteja definido em *main.collection*. Selecione o node raiz e verifique se a propriedade *Name* é "main".
2. De forma semelhante, enviamos mensagens para a coleção carregada por meio do socket dela, nomeado pela propriedade *Name* na coleção.

## A GUI dentro do jogo

Antes de adicionarmos a peça final da lógica ao script do tabuleiro, devemos adicionar um conjunto de elementos de GUI ao tabuleiro. Primeiro, no topo do tabuleiro, adicionamos um botão *RESTART* e um botão *DROP*.

![gui do tabuleiro](images/magic-link/linker_board_gui.png)

O script da GUI do tabuleiro envia mensagens para o elemento de diálogo da GUI de reinício ao clicar e de volta para o próprio script do tabuleiro ao clicar em *DROP*:

```lua
-- board.gui_script
function init(self)
    msg.post("#", "show")
    msg.post("/restart#gui", "hide")
    msg.post("/level_complete#gui", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
    elseif message_id == hash("set_drop_counter") then
        local n = gui.get_node("drop_counter")
        gui.set_text(n, message.drops .. " x")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local restart = gui.get_node("restart")
        local drop = gui.get_node("drop")

        if gui.pick_node(restart, action.x, action.y) then
            -- Mostra a caixa de diálogo de reinício.
            msg.post("/restart#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(drop, action.x, action.y) then
            msg.post("/board#script", "drop")
        end
    end
end
```

O diálogo *RESTART* é simples. Nós o criamos como *restart.gui* e anexamos um script simples que não faz nada se o jogador clicar em *NO*, envia uma mensagem `restart_level` ao script do tabuleiro se o jogador clicar em *YES* e uma mensagem `to_main_menu` ao script principal se o jogador clicar em *Quit to main menu*:

![GUI de reinício](images/magic-link/linker_restart_gui.png)

```lua
-- restart.gui_script
function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local yes = gui.get_node("yes")
        local no = gui.get_node("no")
        local quit = gui.get_node("quit")

        if gui.pick_node(no, action.x, action.y) then
            msg.post("#", "hide")
            msg.post("/board#gui", "show")
        elseif gui.pick_node(yes, action.x, action.y) then
            msg.post("board:/board#script", "restart_level")
            msg.post("/board#gui", "show")
            msg.post("#", "hide")
        elseif gui.pick_node(quit, action.x, action.y) then
            msg.post("main:/main#script", "to_main_menu")
            msg.post("#", "hide")
        end
    end
    -- Consome toda a entrada até desaparecer.
    return true
end
```

Também construímos um diálogo simples de conclusão de nível em *level_complete.gui*, com um script simples que envia uma mensagem `next_level` ao script do tabuleiro quando o jogador clica em *CONTINUE*:

![diálogo de conclusão de nível](images/magic-link/linker_level_complete_gui.png)

```lua
-- level_complete.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
        msg.post(".", "release_input_focus")
    elseif message_id == hash("show") then
        msg.post("#", "enable")
        msg.post(".", "acquire_input_focus")
    end
end

function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        local continue = gui.get_node("continue")

        if gui.pick_node(continue, action.x, action.y) then
            msg.post("board#script", "next_level")
            msg.post("#", "hide")
        end
    end
    -- Consome toda a entrada até desaparecer.
    return true
end
```

Um diálogo usado para apresentar o nível atual, com um script que apenas oculta e mostra o diálogo. Ao mostrar, a mensagem do diálogo é definida para uma mensagem que inclui o nível de dificuldade atual:

![GUI de apresentação do nível](images/magic-link/linker_present_level_gui.png)

```lua
-- present_level.gui_script
function init(self)
    msg.post("#", "hide")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        local n = gui.get_node("message")
        gui.set_text(n, "Level " .. message.level)
        msg.post("#", "enable")
    end
end
```

Também adicionamos um diálogo que aparece se o jogador tenta fazer um drop, mas não há espaço para isso.

![GUI sem espaço para drop](images/magic-link/linker_no_drop_room_gui.png)

```lua
-- no_drop_room.gui_script
function init(self)
    msg.post("#", "hide")
    self.t = 0
end

function update(self, dt)
    if self.t < 0 then
        msg.post("#", "hide")
    else
        self.t = self.t - dt
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("hide") then
        msg.post("#", "disable")
    elseif message_id == hash("show") then
        self.t = 1
        msg.post("#", "enable")
    end
end
```

Por fim, adicionamos esses componentes de GUI a *board.collection* e adicionamos o código necessário a *board.script*:

![Coleção final do tabuleiro](images/magic-link/linker_board_collection_final.png)

Precisamos de código para todas as mensagens enviadas para o tabuleiro e a partir dele em `on_message()`.

`start_level`
: Define o número de blocos mágicos de acordo com o parâmetro de dificuldade, constrói o tabuleiro e então mostra o diálogo da GUI "present_level" por 2 segundos antes de iniciar o jogo (removendo o diálogo e adquirindo foco de entrada). Observe que usamos `go.animate()` como temporizador ao animar o valor de "timer", que não é usado para mais nada.

`restart_level`
: Isso é o que acontece quando o jogador pressiona e confirma o botão de GUI *RESTART*. Limpa e recria o tabuleiro e redefine o contador de drops.

`level_completed`
: Enviada assim que o tabuleiro está em um estado de vitória. Desliga a entrada, anima os blocos mágicos e mostra o diálogo da GUI "level_complete". O diálogo enviará de volta uma mensagem `next_level` quando o jogador clicar no botão *CONTINUE* no diálogo.

`next_level`
: Quando esta mensagem é recebida, limpa o tabuleiro, aumenta o contador de drops e envia `start_level` com o próximo nível de dificuldade definido.

`drop`
: Verifica onde os drops podem ser feitos. Se não houver posições possíveis, mostra o diálogo da GUI "no_drop_room"; caso contrário, executa o drop (se o jogador ainda tiver drops), diminui o contador de drops e atualiza a representação visual do contador.

```lua
-- board.script
function on_message(self, message_id, message, sender)
    if message_id == hash("start_level") then
        self.num_magic = message.difficulty + 1
        build_board(self)

        msg.post("#gui", "set_drop_counter", { drops = self.drops } )

        msg.post("present_level#gui", "show", { level = message.difficulty } )
        -- Espera um pouco...
        go.animate("#", "timer", go.PLAYBACK_ONCE_FORWARD, 1, go.EASING_LINEAR, 2, 0, function ()
            msg.post("present_level#gui", "hide")
            msg.post(".", "acquire_input_focus")
        end)
    elseif message_id == hash("restart_level") then
        clear_board(self)
        build_board(self)
        self.drops = 1
        msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        msg.post(".", "acquire_input_focus")
    elseif message_id == hash("level_completed") then
        -- desliga a entrada
        msg.post(".", "release_input_focus")

        -- Anima a magia!
        for i, m in ipairs(magic_blocks(self)) do
            go.set_scale(0.17, m.id)
            go.animate(m.id, "scale", go.PLAYBACK_LOOP_PINGPONG, 0.19, go.EASING_INSINE, 0.5, 0)
        end

        -- Mostra a tela de conclusão
        msg.post("level_complete#gui", "show")
    elseif message_id == hash("next_level") then
        clear_board(self)
        self.drops = self.drops + 1
        -- O nível de dificuldade é o número de blocos mágicos - 1
        msg.post("#", "start_level", { difficulty = self.num_magic })
    elseif message_id == hash("drop") then
        s = dropspots(self)
        if #s == 0 then
            -- Não é possível executar o drop
            msg.post("no_drop_room#gui", "show")
        elseif self.drops > 0 then
            -- Executa o drop
            drop(self, s)
            self.drops = self.drops - 1
            msg.post("#gui", "set_drop_counter", { drops = self.drops } )
        end
    end
end
```

Pronto! O jogo, e este tutorial, agora estão concluídos. Aproveite para jogar!

![Jogo concluído](images/magic-link/linker_game_finished.png)

## Próximos passos

Este pequeno jogo tem algumas propriedades interessantes, e recomendamos que você experimente com ele. Aqui está uma lista de exercícios que você pode fazer para se familiarizar mais com o Defold:

* Esclareça a interação. Um novo jogador pode ter dificuldade para entender como o jogo funciona e com o que pode interagir. Dedique algum tempo para deixar o jogo mais claro, sem inserir elementos de tutorial.
* Adicione sons. O jogo atualmente é totalmente silencioso e se beneficiaria de uma boa trilha sonora e sons de interação.
* Detecte game over automaticamente.
* High score. Adicione uma funcionalidade de high score persistente.
* Reimplemente o jogo usando apenas as APIs de GUI.
* Atualmente, o jogo continua adicionando um bloco mágico a cada aumento de nível. Isso não é sustentável para sempre. Encontre uma solução satisfatória para esse problema.
* Otimize o jogo e reduza a contagem máxima de sprites reutilizando sprites em vez de excluí-los e recriá-los.
* Implemente renderização independente de resolução para que o jogo fique igualmente bom em telas com resoluções e proporções de tela diferentes.
