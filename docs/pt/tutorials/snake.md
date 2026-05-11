---
brief: Se você está começando no Defold, este guia ajudará você a começar com lógica de script junto com alguns blocos de construção do Defold para criar um clone de Snake do zero.
layout: tutorial
title: Criando um jogo Snake no Defold
difficulty: Beginner
---

# Snake

Este tutorial guia você pelo processo de criação de um dos jogos clássicos mais comuns que você pode tentar recriar. Há muitas variações desse jogo; esta apresenta uma cobra que come "comida" e só cresce quando come. Esta cobra também rasteja por um campo de jogo que contém obstáculos.

![thumbnail](images/snake/thumbnail.png)

### O que você aprenderá aqui?

Neste tutorial, você aprenderá a:
- criar um jogo do zero no Defold
- configurar e tratar entradas
- criar tilemaps e modificá-los em tempo de execução
- escrever scripts em Lua

### Uma observação para iniciantes

Este tutorial foi criado para iniciantes, mas se você é completamente novo no Defold e no desenvolvimento de jogos, recomendamos ler primeiro alguns manuais introdutórios, especialmente sobre os [Blocos de Construção do Defold](/manuals/building-blocks/) e o [Glossário](/manuals/glossary/). Se ainda não baixou o Defold, confira o [manual de Instalação](/manuals/install/). Também é recomendado conferir a [visão geral do Editor](manuals/editor/) para mergulhar rapidamente no próprio Editor, mas também fornecemos aqui capturas de tela para cada etapa.

## Criando o projeto

Inicie o Defold e:

1. Selecione *Create From* ▸ *Templates* no lado esquerdo.
2. Selecione *Empty Project*.
3. Digite um nome de projeto em *Title*.
4. Selecione uma *Location* para o projeto.
5. Clique em *Create New Project*.

![start](images/snake/1.png)

<input type="checkbox"/> Done!

## Configurações do projeto

Começaremos definindo a resolução do jogo.

1. Quando o Editor for aberto, procure pelo arquivo `game.project` no lado esquerdo, no painel *Assets*. Dê um duplo clique nele para abrir.
2. Vá para a seção *Display* do arquivo `game.project`.
3. Defina as dimensões do jogo (`Width` e `Height`) para 768⨉768 ou outro múltiplo de 16.

![display](images/snake/2.png)

O motivo para fazer isso é que o jogo será desenhado em uma grade onde cada segmento terá 16x16 pixels. Assim, a tela do jogo não cortará nenhum segmento parcial. Esse arquivo `game.project` contém todas as configurações importantes dos projetos; você pode ler sobre todas elas no [manual de Configurações do Projeto](/manuals/project-settings/).

<input type="checkbox"/> Done!

## Criando novas pastas no painel Assets

Muito pouco é necessário em termos de gráficos para um clone minimalista de Snake. Um segmento verde de 16⨉16 para a cobra, um bloco branco para os obstáculos e um bloco vermelho menor representando a comida.

Primeiro, crie um diretório para os assets no Defold Editor:

1. Dê <kbd>Right click</kbd> na pasta `main`
2. Selecione `New Folder`.
3. Um popup pedindo um nome aparecerá - digite `assets` e clique em `Create Folder`.

![new_folder](images/snake/3.png)

<input type="checkbox"/>`Done!`

## Adicionando gráficos ao jogo

Esta imagem abaixo é o único asset de que você precisa:

![snake_sprites](images/snake/snake.png)

1. Dê <kbd>Right click</kbd> na imagem acima e salve-a no seu disco local. Depois, arraste e solte (ou copie + cole) a imagem baixada no novo local da pasta do projeto que você acabou de criar.

![new_folder](images/snake/4.png)

Você também pode ler mais detalhes sobre [importar assets aqui](/manuals/importing-graphics/).

<input type="checkbox"/>`Done!`

## Adicionando Tile Source

O Defold fornece um componente [Tilemap](/manuals/tilemap/) integrado que você usará para criar o campo de jogo composto por *tiles* alinhados em uma grade. Um tilemap permite definir e ler tiles individuais, o que se encaixa perfeitamente neste jogo. Como tilemaps buscam seus gráficos em um [Tilesource](/manuals/tilesource/), você precisa criar um:

1. Dê <kbd>Right click</kbd> na pasta `assets`.
2. Selecione `New` ▸ `Tile Source` na seção "Resources".
3. Nomeie o novo arquivo como "snake" (o editor salvará o arquivo como `snake.tilesource`).

![new_tilesource](images/snake/5.png)

O tilesource será aberto em um Tilesource Editor dedicado para esse tipo de arquivo, e você precisará fornecer uma imagem para ele. No lado direito, você encontrará um painel `Properties`:

4. Defina a propriedade `Image` para o arquivo gráfico que você acabou de importar.
![tilesource](images/snake/6.png)

5. As propriedades `Width` e `Height` devem ser mantidas em 16 (valor padrão). Isso dividirá a imagem de 32⨉32 pixels em 4 tiles, numerados de 1–4.

![tilesource_properties](images/snake/7.png)

Observe que a propriedade *Extrude Borders* está definida como 2 pixels. Isso serve para evitar artefatos visuais ao redor dos tiles que têm gráficos até a borda.

Se você fizer qualquer alteração em um arquivo, um asterisco `*` aparece ao lado do nome dele na aba. Selecione `File` ▸ `Save All` ou use o atalho `<kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>⌘Cmd</kbd> + <kbd>S</kbd> no Mac) para salvar todos os arquivos.

<input type="checkbox"/> Done!

## Criando o tilemap do campo de jogo

Agora você tem um tilesource pronto para uso, então é hora de criar o componente tilemap do campo de jogo:

1. Dê <kbd>Right click</kbd> na pasta `main` e selecione <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> na seção "Components". Nomeie o novo arquivo como "grid" (o editor salvará o arquivo como "grid.tilemap").
![add_tilemap](images/snake/8.png)

2. Ele será aberto em um Tilemap Editor e destacará que precisa de uma **Tile Source**, então defina a propriedade *Tile Source* para o "snake.tilesource" criado anteriormente.
![set_tilesource](images/snake/9.png)

<input type="checkbox"/> Done!

## Desenhando tiles no tilemap

O Defold armazena apenas a área do tilemap que é realmente usada, então você precisa adicionar tiles suficientes para preencher os limites da tela.

1. Selecione a camada `layer1` no painel `Outline` do lado direito.
2. Escolha a opção de menu `Edit` ▸ `Select Tile...` ou o atalho <kbd>Space</kbd> para exibir a paleta de tiles, depois clique no tile que deseja usar ao pintar.
![tilemap](images/snake/10.png)

3. Pinte uma borda ao redor da tela e alguns obstáculos.
![tilemap_final](images/snake/11.png)

Você precisará de um tilemap de tamanho 48x48 tiles (porque nossa tela é 768 e temos tiles de 16px, então 768/16 = 48) para preencher a tela do jogo.

Salve o tilemap quando terminar.

<input type="checkbox"/> Done!

## Adicionando o tilemap ao jogo

Agora precisamos adicionar nosso tilemap ao jogo. Se você está familiarizado com os Blocos de Construção do Defold, componentes fazem parte de Objetos de Jogo e objetos de jogo podem ser definidos em Coleções.

1. Abra `main.collection` dando um duplo clique nele no painel `Assets`. No template Empty Project, por padrão, esta é a coleção bootstrap carregada ao iniciar a engine.

2. Dê <kbd>Right click</kbd> na raiz no `Outline` e selecione `Add Game Object`, o que cria um novo objeto de jogo na coleção que é carregada quando o jogo começa.
![add_game_object](images/snake/12.png)

3. Dê <kbd>Right click</kbd> no novo objeto de jogo e selecione `Add Component File`. Escolha o arquivo "grid.tilemap" que você acabou de criar.
![add_component](images/snake/13.png)

Agora temos um tilemap em nossa coleção de jogo. Ele deve ficar visível quando você executar o jogo pelo Editor.

1. Selecione `Project` ▸ `Build` ou o atalho <kbd>Ctrl</kbd> + <kbd>B</kbd> (<kbd>⌘Cmd</kbd> + <kbd>B</kbd> no Mac).

![run_game](images/snake/14.png)

<input type="checkbox"/> Done!

## Adicionando um script ao jogo

1. Dê <kbd>Right click</kbd> na pasta `main` no navegador `Assets` e selecione `New` ▸ `Script` na seção Scripts. Nomeie o novo arquivo de script como "snake" (ele será salvo como "snake.script"). Esse arquivo conterá toda a lógica do jogo.
![add_script](images/snake/15.png)

2. Volte para *main.collection* e dê <kbd>right click</kbd> no objeto de jogo que contém o tilemap. Selecione <kbd>Add&nbsp;Component&nbsp;File</kbd> e escolha o arquivo "snake.script".

![main _ollection](images/snake/16.png)

Agora você tem o componente tilemap e o script no lugar.

<input type="checkbox"/> Done!

## O script do jogo

O script que você vai escrever controlará todo o jogo. Adicionaremos recursos um por um.

### Algoritmo simples de movimento

A ideia de como isso funcionará é a seguinte:

1. O script mantém uma lista de posições de tiles que a cobra ocupa atualmente.
2. Se o jogador pressionar uma tecla direcional, armazene a direção em que a cobra deve se mover.
3. Em um intervalo regular, mova a cobra um passo na direção de movimento atual.

### Inicialização

Abra *snake.script* e localize a função `init()`. Essa função é chamada pela engine quando o script é inicializado no início do jogo. Altere o código para o seguinte:

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

Neste código, nós:

1. Armazenamos os segmentos da cobra como uma tabela Lua chamada `self.segments`, contendo uma lista de tabelas, cada uma com uma posição X e Y para um segmento.
2. Armazenamos a direção atual como uma tabela chamada `self.dir`, contendo uma direção X e Y.
3. Armazenamos a velocidade de movimento atual em `self.speed`, expressa em tiles por segundo.
4. Armazenamos um valor de temporizador em `self.time`, que será usado para acompanhar a velocidade de movimento.

O código de script acima está escrito na linguagem Lua. Há algumas coisas a observar sobre o código, mas se você ainda não entender nada do que vem abaixo, não se preocupe. Apenas acompanhe, experimente e dê tempo --- você acabará entendendo. Por enquanto, pode lembrar que em `init()` apenas inicializamos as variáveis que usaremos.

- O Defold reserva um conjunto de *funções* de callback integradas que são chamadas durante a vida de um componente de script. Elas *não* são métodos, mas funções comuns.
- O runtime passa uma referência para a instância atual do componente de script pelo parâmetro `self`. A referência `self` é usada para armazenar dados da instância.
- A referência `self` pode ser usada como uma tabela Lua na qual você pode armazenar dados. Basta usar a notação de ponto como faria com qualquer outra tabela: `self.data = "value"`. A referência é válida durante toda a vida do script, neste caso desde o início do jogo até você encerrá-lo.
- Literais de tabela Lua são escritos entre chaves `{}`.
- Entradas de tabela podem ser pares chave/valor (`{x = 10, y = 20}`), tabelas Lua aninhadas (`{ {a = 1}, {b = 2} }`) ou outros tipos de dados.

<input type="checkbox"/> Done!

### Update

A função `init()` é chamada exatamente uma vez, quando o componente de script é instanciado no jogo em execução. A função `update()`, porém, é chamada uma vez **a cada frame**, por padrão 60 vezes por segundo. Isso torna a função ideal para lógica de jogo em tempo real.

A ideia do update é esta: em algum intervalo definido, faça o seguinte:

1. Encontre onde está a cabeça da cobra e então crie uma nova cabeça na posição ao lado, deslocada pela direção de movimento atual. Então, se a cobra está se movendo por X=1 e Y=0 e a cabeça atual está na localização X=0 e Y=0, a nova cabeça deve ficar em X=1 e Y=0.
2. Salve a nova posição da cabeça na lista de segmentos que compõe a cobra.
3. Obtenha a posição da cauda a partir da tabela de segmentos.
4. Limpe o tile da cauda nessa posição.
5. Desenhe todos os segmentos da cobra (tiles) nas posições da tabela.

![algorithm](images/snake/17.png)

::: sidenote
Tenha em mente que a cabeça da cobra está no final da tabela, e a cauda está no começo.
:::

1. Encontre a função `update()` em *snake.script* e altere o código para o seguinte:

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

Neste código, nós:

1. Avançamos o temporizador com a diferença de tempo (em segundos) desde a última vez que `update()` foi invocada --- o chamado "delta time", ou `dt`.
2. Se o temporizador avançou o suficiente:
3. Obtemos a posição atual da cabeça. `#` é o operador usado para obter o comprimento de uma tabela quando ela é usada como array, que é o nosso caso --- todos os segmentos são valores de tabela sem chave especificada.
4. Criamos um novo segmento de cabeça com base na localização atual da cabeça e na direção de movimento (`self.dir`).
5. Adicionamos a nova cabeça ao final da tabela de segmentos.
6. Removemos a cauda do começo da tabela de segmentos.
7. Limpamos o tile na posição da cauda removida. Nosso tilemap `#grid` tem apenas 1 camada chamada `layer1`.
8. Percorremos os elementos da tabela de segmentos. Cada iteração terá `i` definido para a posição na tabela (começando em 1) e `s` definido para o segmento atual.
9. Definimos o tile na posição do segmento para o valor 2 (que é o tile com a cor verde da cobra).
10. Ao terminar, redefinimos o temporizador para zero.

Se executar o jogo agora, você deve ver a cobra de 4 segmentos rastejar da esquerda para a direita pelo campo de jogo.

![run the game](images/snake/snake_run_1.png)

<input type="checkbox"/> Done!

## Entrada do jogador

Antes de adicionar código para reagir à entrada do jogador, você precisa configurar as conexões de entrada.

### Mapeamentos de entrada

1. Encontre na pasta `input` o arquivo `game.input_binding` e dê <kbd>double click</kbd> para abri-lo.
2. Adicione um conjunto de mapeamentos *Key Trigger* para movimento para cima, para baixo, para a esquerda e para a direita. Na coluna *Input*, selecione teclas do teclado e, nas colunas *Action*, digite os nomes das ações.

![input](images/snake/18.png)

O arquivo de mapeamento de entrada mapeia a entrada real do usuário (teclas, movimentos do mouse etc.) para *nomes* de ação que são fornecidos aos scripts que solicitaram entrada.

<input type="checkbox"/> Done!

### Adquirindo foco de entrada

Com os mapeamentos no lugar, abra *snake.script* e adicione a linha a seguir no início da função `init()`:

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

A linha adicionada:
1. Envia uma mensagem ao objeto de jogo atual ("." é abreviação para o objeto de jogo atual) dizendo para ele começar a receber entrada da engine.

Depois encontre a função `on_input` e digite o seguinte código:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

Esses ramos `if...elseif...` fazem o seguinte:
1. Se a ação de entrada "up" for recebida, conforme configurado nos mapeamentos de entrada, e a tabela `action` tiver o campo `pressed` definido como `true` (o jogador pressionou a tecla), então:
2. Defina a direção de movimento.

Execute o jogo novamente e confira se consegue controlar a cobra.

<input type="checkbox"/> Done!

### Melhorando o tratamento de entrada

Agora, observe que, se você pressionar duas teclas simultaneamente, isso resultará em duas chamadas para `on_input()`, uma para cada tecla pressionada. Como o código acima está escrito, apenas a chamada que acontecer por último terá efeito na direção da cobra, já que chamadas subsequentes a `on_input()` sobrescreverão os valores em `self.dir`.

Observe também que, se a cobra se move para a esquerda e você pressiona a tecla <kbd>right</kbd>, ela virará para dentro de si mesma. A correção *aparentemente* óbvia para esse problema é adicionar uma condição extra às cláusulas `if` em `on_input()`:

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

Porém, se a cobra estiver se movendo para a esquerda e o jogador pressionar *rapidamente* primeiro <kbd>up</kbd> e depois <kbd>right</kbd> antes do próximo passo de movimento acontecer, apenas o pressionamento de <kbd>right</kbd> terá efeito e a cobra se moverá para dentro de si mesma. Com as condições adicionadas às cláusulas `if` mostradas acima, a entrada será ignorada. *Nada bom!*

Uma solução adequada para esse problema é armazenar a entrada em uma fila e retirar entradas dessa fila conforme a cobra se move:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

Desta vez, nós:
1. Adicionamos uma variável `self.dirqueue`, inicializada como uma tabela vazia.

Na função `update()`, adicione:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. Retire o primeiro item da fila de direções.
2. Se houver um item (`newdir` não é nulo), verifique se `newdir` aponta no sentido oposto a `self.dir`.
3. Defina a nova direção somente se ela não apontar para o lado oposto.

E modifique `on_input` para armazenar a entrada atual na fila:

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. Adicione a direção de entrada à fila de direções em vez de definir `self.dir` diretamente.

Inicie o jogo e confira se ele se comporta como esperado.

<input type="checkbox"/> Done!

## Comida e colisão com obstáculos

A cobra precisa de comida no mapa para poder ficar longa e rápida. Vamos adicionar isso!

### Gerando a comida

Acima da função `init()`, adicione uma nova função:

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

Nesta função, nós:
1. Declaramos uma nova função chamada `put_food()` que coloca um pedaço de comida no mapa.
2. Armazenamos uma posição X e Y aleatória em uma variável chamada `self.food`.
3. Definimos o tile na posição X e Y para o valor 3, que é o gráfico do tile da comida.

Depois chame-a no final da função `init()`:
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. Antes de começar a obter valores aleatórios com `math.random()`, defina a seed aleatória; caso contrário, a mesma série de valores aleatórios será gerada. Essa seed deve ser definida apenas uma vez.
2. Chame a função `put_food()` no início do jogo para que o jogador comece com um item de comida no mapa.

<input type="checkbox"/> Done!

### Comendo a comida

Agora, detectar se a cobra colidiu com algo é apenas uma questão de olhar o que há no tilemap para onde a cobra está indo e reagir.

Adicione uma variável que acompanha se a cobra está viva ou não:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. Uma flag indicando se a cobra está viva ou não.

Depois adicione lógica que testa colisão com parede/obstáculo e comida:

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. Avance a cobra somente se ela estiver viva.
2. Antes de desenhar no tilemap, leia o que há na posição onde a nova cabeça da cobra ficará.
3. Se o tile for um obstáculo ou outra parte da cobra, game over!
4. Se o tile for comida, aumente a velocidade e então coloque um novo item de comida.
5. Observe que a remoção da cauda só acontece se não houver colisão. Isso significa que, se o jogador comer comida, a cobra crescerá em um segmento, já que nenhuma cauda é removida nesse movimento.

Agora experimente o jogo e certifique-se de que ele funciona bem!

Isso conclui o tutorial, mas continue experimentando o jogo e trabalhando em alguns dos exercícios abaixo!

<input type="checkbox"/> Done!

## O script completo

Aqui está o código completo do script para referência:

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## Exercícios

É um bom exercício tentar implementar estas melhorias:

1. Adicione tratamento de entrada por tecla para reiniciar o jogo quando ele terminar.
2. Adicione pontuação e um contador de pontos, usando apenas um componente label (mais fácil) ou uma GUI completa.
3. A função put_food() não leva em conta a posição da cobra nem obstáculos. Corrija isso para que ela só gere comida em espaços livres.
4. Quando o jogo terminar, mostre uma mensagem “Game Over” e permita que o jogador tente novamente.
5. Crédito extra: adicione uma segunda cobra controlada por jogador.
