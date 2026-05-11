---
title: Tutorial de endless runner
brief: Neste tutorial, você começa com um projeto vazio e cria um jogo runner completo com personagem animado, colisão física, pickups e pontuação.
---

# Tutorial Runner

Neste tutorial, começamos com um projeto vazio e criamos um jogo runner completo com um personagem animado, colisão física, pickups e pontuação.

Há muito a absorver ao aprender uma nova game engine, então criamos este tutorial para ajudar você a começar. É um tutorial bastante completo que mostra como a engine e o editor funcionam. Assumimos que você tem alguma familiaridade com programação.

Se precisar de uma introdução à programação em Lua, confira nosso [manual de Lua no Defold](/manuals/lua).

Se achar que este tutorial é um pouco demais para começar, confira nossa [página de tutoriais](//www.defold.com/tutorials), onde temos uma seleção de tutoriais com dificuldades variadas.

Se preferir assistir a tutoriais em vídeo, confira [a versão em vídeo no Youtube](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b).

Usamos assets de jogo de dois outros tutoriais, com pequenas modificações. O tutorial é dividido em várias etapas, com cada parte nos levando um passo importante em direção ao jogo final.

O resultado final será um jogo em que você controla um personagem herói que corre por um ambiente, coletando moedas e evitando obstáculos. O herói corre a uma velocidade fixa, e o jogador controla apenas o pulo do personagem pressionando um único botão (ou tocando a tela em um dispositivo móvel). O nível consiste em um fluxo infinito de plataformas para pular - e de moedas para coletar.

Se em algum momento você ficar preso neste tutorial ou ao criar seu jogo, não hesite em pedir ajuda no [Defold Forum](//forum.defold.com). No fórum, você pode discutir Defold, pedir ajuda à equipe do Defold, ver como outros desenvolvedores de jogos resolveram seus problemas e encontrar nova inspiração. Comece agora.

::: sidenote
Ao longo do tutorial, descrições detalhadas sobre conceitos e sobre como fazer certas etapas são marcadas como este parágrafo. Se você achar que essas seções entram em detalhes demais, pode pulá-las.
:::

Então vamos começar. Esperamos que você se divirta bastante ao seguir este tutorial e que ele ajude você a engrenar com o Defold.

> Baixe os assets deste tutorial [aqui](https://github.com/defold/sample-runner/tree/main/def-runner).

## ETAPA 1 - Instalação e configuração

O primeiro passo é [baixar os seguintes arquivos](https://github.com/defold/sample-runner/tree/main/def-runner).

Agora, se você ainda não baixou e instalou o editor Defold, é hora de fazer isso:

:[install](../shared/install.md)

Quando o editor estiver instalado e iniciado, é hora de criar um novo projeto e prepará-lo. Crie um [novo projeto](/manuals/project-setup/#creating-a-new-project) a partir do template "Empty Project".

::: sidenote
Este tutorial usa recursos de Spine, que foram movidos para sua própria extensão após o Defold 1.2.188. Se você estiver usando uma versão mais nova, adicione a [Spine Extension](https://github.com/defold/extension-spine) à seção de dependências de *game.project*.
:::

## O editor

Na primeira vez que você inicia o editor, ele começa em branco, sem nenhum projeto aberto. Então escolha <kbd>Open Project</kbd> no menu e selecione seu projeto recém-criado. Você também será solicitado a criar um "branch" para o projeto.

Agora, no *Assets pane*, você verá todos os arquivos que fazem parte do projeto. Se der um duplo clique no arquivo "main/main.collection", o arquivo será aberto na visualização do editor no centro:

![Editor overview](images/runner/1/editor2_overview.png)

O editor consiste nas seguintes áreas principais:

Assets pane
: Esta é uma visualização de todos os arquivos do seu projeto. Tipos de arquivo diferentes têm ícones diferentes. Dê um duplo clique em um arquivo para abri-lo em um editor designado para esse tipo de arquivo. A pasta especial somente leitura *builtins* é comum a todos os projetos e inclui itens úteis, como um script de renderização padrão, uma fonte, materiais para renderizar vários componentes e outras coisas.

Main Editor View
: Dependendo do tipo de arquivo que você está editando, esta visualização mostrará um editor para esse tipo. O mais usado é o editor Scene que você vê aqui. Cada arquivo aberto é mostrado em uma aba separada.

Changed Files
: Contém uma lista de todas as edições que você fez no seu branch desde a última sincronização. Então, se você vir algo neste painel, há alterações que ainda não estão no servidor. Você pode abrir um diff somente texto e reverter alterações por essa visualização.

Outline
: O conteúdo do arquivo atualmente editado em uma visualização hierárquica. Você pode adicionar, excluir, modificar e selecionar objetos e componentes por essa visualização.

Properties
: As propriedades definidas no objeto ou componente atualmente selecionado.

Console
: Ao executar o jogo, esta visualização captura saída (logs, erros, informações de debug etc.) vindo da engine do jogo, além de quaisquer mensagens de debug personalizadas de `print()` e `pprint()` nos seus scripts. Se o seu app ou jogo não iniciar, o console é o primeiro lugar a verificar. Atrás do console há um conjunto de abas exibindo informações de erro, além de um editor de curvas usado ao criar efeitos de partículas.

## Executando o jogo

O template de projeto "Empty" é, de fato, completamente vazio. Mesmo assim, selecione <kbd>Project ▸ Build</kbd> para compilar o projeto e iniciar o jogo.

![Build](images/runner/1/build_and_launch.png)

Uma tela preta talvez não seja muito empolgante, mas é uma aplicação de jogo Defold em execução, e podemos modificá-la facilmente para algo mais interessante. Então vamos fazer isso.

::: sidenote
O editor Defold trabalha com arquivos. Ao dar duplo clique em um arquivo no *Assets pane*, você o abre em um editor adequado. Depois, pode trabalhar com o conteúdo do arquivo.

Quando terminar de editar um arquivo, você precisa salvá-lo. Selecione <kbd>File ▸ Save</kbd> no menu principal. O editor dá uma dica adicionando um asterisco '\*' ao nome do arquivo na aba de qualquer arquivo que contenha alterações não salvas.

![File with unsaved changes](images/runner/1/file_changed.png)
:::

## Configurando o projeto

Antes de começar, vamos configurar várias opções do nosso projeto. Abra o asset *game.project* no `Assets Pane` e role até a seção Display. Defina `width` e `height` do projeto como `1280` e `720`, respectivamente.

Você também precisa adicionar a extensão Spine ao projeto para que possamos animar o personagem herói. Adicione uma versão da extensão Spine que seja compatível com a versão do editor Defold instalada. As versões disponíveis da Spine podem ser vistas aqui:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Clique com o botão direito no link para o arquivo zip da release que você quer usar:

![Right click and copy link to release](images/runner/extension-spine-releases.png)

Adicione o link da release à sua lista de [dependências de game.project](/manuals/libraries/#setting-up-library-dependencies). Depois que a extensão Spine for adicionada, você também precisa reiniciar o editor para ativar a integração com o editor incluída na extensão Spine.


## ETAPA 2 - Criando o chão

Vamos dar os primeiros passos e criar uma arena para nosso personagem, ou melhor, um trecho de chão com rolagem. Fazemos isso em algumas etapas.

1. Importe os assets de imagem para o projeto arrastando os arquivos "ground01.png" e "ground02.png" (da subpasta "level-images" no pacote de assets) para um local adequado no projeto, por exemplo a pasta "images" dentro da pasta "main".
2. Crie um novo arquivo *Atlas* para conter as texturas do chão (clique com o botão direito em uma pasta adequada, por exemplo a pasta *main*, no *Assets pane* e selecione <kbd>New ▸ Atlas File</kbd>). Nomeie o arquivo de atlas como *level.atlas*.

  ::: sidenote
  Um *Atlas* é um arquivo que combina um conjunto de imagens separadas em um único arquivo de imagem maior. O motivo para fazer isso é economizar espaço e também ganhar performance. Você pode ler mais sobre Atlases e outros recursos de gráficos 2D na [documentação de gráficos 2D](/manuals/2dgraphics).
  :::

3. Adicione as imagens do chão ao novo atlas clicando com o botão direito na raiz do atlas no *Outline* e selecionando <kbd>Add Images</kbd>. Selecione as imagens importadas e clique em *OK*. Cada imagem no atlas agora fica acessível como uma animação de um frame (imagem estática) para usar em sprites, efeitos de partículas e outros elementos visuais. Salve o arquivo.

  ![Create new atlas](images/runner/1/new_atlas.png)

  ![Add images to atlas](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Por que não funciona!?* Um problema comum de quem está começando com Defold é esquecer de salvar! Depois de adicionar imagens a um atlas, você precisa salvar o arquivo antes de conseguir acessar essa imagem.
  :::

4. Crie um arquivo de coleção *ground.collection* para o chão e adicione 7 objetos de jogo a ele (clique com o botão direito na raiz da coleção na visualização *Outline* e selecione <kbd>Add Game Object</kbd>). Nomeie os objetos "ground0", "ground1", "ground2" etc. alterando a propriedade *Id* na visualização *Properties*. Observe que o Defold atribui automaticamente um id único aos novos objetos de jogo.

5. Em cada objeto, adicione um componente de sprite (clique com o botão direito no objeto de jogo na visualização *Outline* e selecione <kbd>Add Component</kbd>, depois selecione *Sprite* e clique em *OK*), defina a propriedade *Image* do componente de sprite para o atlas que você acabou de criar e defina a animação padrão do sprite para uma das duas imagens de chão. Defina a posição X do _componente de sprite_ (não do objeto de jogo) como 190 e a posição Y como 40. Como a largura da imagem é 380 pixels e a deslocamos lateralmente pela metade disso, o pivô do objeto de jogo ficará na borda mais à esquerda da imagem do sprite.

  ![Create ground collection](images/runner/1/ground_collection.png)

6. Os gráficos que estamos usando são um pouco grandes demais, então escale cada objeto de jogo para 60% (escala 0.6 em X e Y, resultando em peças de chão com 228 pixels de largura).

  ![Scale ground](images/runner/1/scale_ground.png)

7. Posicione todos os _objetos de jogo_ em linha. Defina as posições X dos _objetos de jogo_ (não dos componentes de sprite) como 0, 228, 456, 684, 912, 1140 e 1368 (múltiplos da largura de 228 pixels).

  ::: sidenote
  Provavelmente é mais fácil criar um objeto de jogo completo já escalado com um componente de sprite e depois copiá-lo. Marque-o na visualização *Outline*, selecione <kbd>Edit ▸ Copy</kbd> e depois <kbd>Edit ▸ Paste</kbd>.

  Vale observar que, se você quiser tiles maiores ou menores, pode simplesmente alterar a escala. Porém, ao fazer isso, também precisará alterar as posições X de todos os objetos de jogo do chão para múltiplos da nova largura.
  :::

8. Salve o arquivo e então adicione *ground.collection* ao arquivo *main.collection*: primeiro dê um duplo clique no arquivo *main.collection*, depois clique com o botão direito no objeto raiz na visualização *Outline* e selecione <kbd>Add Collection From File</kbd>. No diálogo, selecione *ground.collection* e clique em *OK*. Certifique-se de colocar *ground.collection* na posição 0, 0, 0, ou ela ficará deslocada visualmente. Salve.

9. Inicie o jogo (<kbd>Project ▸ Build</kbd>) para ver se tudo está no lugar.

  ![Still ground](images/runner/1/still_ground.png)

Neste ponto, talvez você esteja confuso e se perguntando o que são todas essas coisas que criamos. Então vamos parar um momento e olhar para os blocos de construção mais básicos de qualquer projeto Defold:

Game objects
: São coisas que existem no jogo em execução. Cada objeto de jogo tem uma localização no espaço 3D, uma rotação e uma escala. Ele não precisa necessariamente estar visível. Um objeto de jogo contém qualquer número de _componentes_ que adicionam capacidades como gráficos (sprites, tilemaps, modelos, modelos Spine e efeitos de partículas), sons, física, fábricas (para spawn) e muito mais. _Componentes de script_ Lua também podem ser adicionados para dar comportamentos a um objeto de jogo. Cada objeto de jogo que existe nos seus jogos tem um *id* de que você precisa para se comunicar com ele por passagem de mensagens.

Collections
: Coleções não existem por si mesmas em um jogo em execução, mas são usadas para permitir nomeação estática de objetos de jogo e, ao mesmo tempo, permitir várias instâncias do mesmo objeto de jogo. Na prática, coleções são usadas como contêineres para objetos de jogo e outras coleções. Você pode usar coleções de forma parecida com protótipos (também conhecidos como "prefabs" ou "blueprints" em outras engines) de hierarquias complexas de objetos de jogo e coleções. Na inicialização, a engine carrega uma coleção principal e dá vida a tudo que você colocou dentro dela. Por padrão, esse é o arquivo *main.collection* na pasta *main* do seu projeto, mas você pode alterar isso nas configurações do projeto.

Por enquanto, essas descrições provavelmente bastam. Porém, um mergulho muito mais abrangente nesses conceitos pode ser encontrado no [manual de Blocos de Construção](/manuals/building-blocks). É uma boa ideia visitar esse manual em uma etapa posterior para entender melhor como as coisas funcionam no Defold.

## ETAPA 3 - Fazendo o chão se mover

Agora que temos todas as peças do chão no lugar, é bastante simples fazê-las se mover. A ideia é esta: mover as peças da direita para a esquerda e, quando uma peça alcançar a borda esquerda fora da tela, movê-la para a posição mais à direita. Para mover todos esses objetos de jogo, é necessário um script Lua, então vamos criar um:

1. Clique com o botão direito na pasta *main* no *Assets pane* e selecione <kbd>New ▸ Script File</kbd>. Nomeie o novo arquivo como *ground.script*.
2. Dê um duplo clique no novo arquivo para abrir o editor de script Lua.
3. Exclua o conteúdo padrão do arquivo, copie o código Lua abaixo para ele e salve o arquivo.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Velocidade em pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Armazene os ids dos objetos de jogo do chão em uma tabela Lua para que possamos iterar por eles.
2. A função `init()` é chamada quando o objeto de jogo ganha vida no jogo. Inicializamos uma variável de membro local do objeto que contém a velocidade do chão.
3. `update()` é chamada uma vez a cada frame, normalmente 60 vezes por segundo. `dt` contém o número de segundos desde a última chamada.
4. Itere por todos os objetos de jogo do chão.
5. Armazene a posição atual em uma variável local e, se o objeto atual estiver na borda mais à esquerda, mova-o para a borda mais à direita.
6. Diminua a posição X atual pela velocidade definida. Multiplique por `dt` para obter velocidade independente de framerate em pixels/s.
7. Atualize a posição do objeto com a nova velocidade.

::: sidenote
Defold é um núcleo de engine rápido que gerencia seus dados e objetos de jogo. Qualquer lógica ou comportamento de que você precise para seu jogo é criado na linguagem Lua. Lua é uma linguagem de programação rápida e leve, excelente para escrever lógica de jogo. Há ótimos recursos disponíveis para aprender a linguagem, como o livro [Programming in Lua](http://www.lua.org/pil/) e o [manual de referência Lua](http://www.lua.org/manual/5.3/) oficial.

O Defold adiciona um conjunto de APIs sobre Lua, além de um sistema de _passagem de mensagens_ que permite programar comunicações entre objetos de jogo. Veja o [manual de passagem de mensagens](/manuals/message-passing) para detalhes sobre como isso funciona.
:::

::: sidenote
Você pode alternar as seções Assets Pane, Console e Outline do editor usando as teclas <kbd>F6</kbd>, <kbd>F7</kbd> e <kbd>F8</kbd>, respectivamente
:::

Agora que temos um arquivo de script, devemos adicionar uma referência a ele em um componente de um objeto de jogo. Assim, o script será executado como parte do ciclo de vida do objeto de jogo. Fazemos isso criando um novo objeto de jogo em *ground.collection* e adicionando ao objeto um componente *Script* que se refere ao arquivo de script Lua que acabamos de criar:

1. Clique com o botão direito na raiz da coleção e selecione <kbd>Add Game Object</kbd>. Defina o *id* do objeto como "controller".
2. Clique com o botão direito no objeto "controller" e selecione <kbd>Add Component from file</kbd>, depois selecione o arquivo *ground.script*.

![Ground controller](images/runner/1/ground_controller.png)

Agora, quando você executar o jogo, o objeto de jogo "controller" executará o script em seu componente *Script*, fazendo o chão rolar suavemente pela tela.

## ETAPA 4 - Criando um personagem herói

O personagem herói será um objeto de jogo composto pelos seguintes componentes:

Um *Spine Model*
: Isso nos dá um pequeno personagem herói em estilo paper-doll cujas partes do corpo podem ser animadas de forma suave (e barata).

Um *Collision Object*
: Isso detectará colisões entre o personagem herói e coisas no nível sobre as quais ele pode correr, que são perigosas ou que podem ser coletadas.

Um *Script*
: Isso adquire entrada do usuário e reage a ela, faz o personagem herói pular, animar e lidar com colisões.

Comece importando as imagens das partes do corpo e depois adicione-as a um novo atlas que chamaremos de *hero.atlas*:

1. Crie uma nova pasta clicando com o botão direito no *Assets pane* e selecionando <kbd>New ▸ Folder</kbd>. Certifique-se de não selecionar uma pasta antes de clicar, ou a nova pasta será criada dentro da pasta marcada. Nomeie a pasta como "hero".
2. Crie um novo arquivo de atlas clicando com o botão direito na pasta *hero* e selecionando <kbd>New ▸ Atlas File</kbd>. Nomeie o arquivo como *hero.atlas*.
3. Crie uma nova subpasta *images* dentro da pasta *hero*. Clique com o botão direito na pasta *hero* e selecione <kbd>New ▸ Folder</kbd>.
4. Arraste as imagens de partes do corpo da pasta *hero-images* no pacote de assets para a pasta *images* que você acabou de criar no *Assets pane*.
5. Abra *hero.atlas*, clique com o botão direito no node raiz no *Outline* e selecione <kbd>Add Images</kbd>. Marque todas as imagens de partes do corpo e clique em *OK*.
6. Salve o arquivo de atlas.

![Hero atlas](images/runner/2/hero_atlas.png)

Também precisamos importar os dados de animação Spine e configurar uma *Spine Scene* para eles:

1. Arraste o arquivo *hero.spinejson* (incluído no pacote de assets) para a pasta *hero* no *Assets pane*.
2. Crie um arquivo *Spine Scene*. Clique com o botão direito na pasta *hero* e selecione <kbd>New ▸ Spine Scene File</kbd>. Nomeie o arquivo como *hero.spinescene*.
3. Dê um duplo clique no novo arquivo para abrir e editar a *Spine Scene*.
4. Defina a propriedade *spine_json* para o arquivo JSON importado *hero.spinejson*. Clique na propriedade e depois clique no botão seletor de arquivo *...* para abrir o navegador de recursos.
5. Defina a propriedade *atlas* para se referir ao arquivo *hero.atlas*.
6. Salve o arquivo.

![Hero spinescene](images/runner/2/hero_spinescene.png)

::: sidenote
O arquivo *hero.spinejson* foi exportado no formato Spine JSON. Você precisará do software de animação Spine para criar arquivos assim. Se quiser usar outro software de animação, pode exportar suas animações como sprite-sheets e usá-las como animações flip-book a partir de recursos *Tile Source* ou *Atlas*. Veja o manual sobre [Animação](/manuals/animation) para mais informações.
:::

### Construindo o objeto de jogo

Agora podemos começar a construir o gameobject do herói:

1. Crie um novo arquivo *hero.go* (clique com o botão direito na pasta *hero* e selecione <kbd>New ▸ Game Object File</kbd>).
2. Abra o arquivo de objeto de jogo.
3. Adicione um componente *Spine Model* a ele. (Clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Component</kbd>, depois selecione "Spine Model".)
4. Defina a propriedade *Spine Scene* do componente para o arquivo *hero.spinescene* que você acabou de criar e selecione "run_right" como a animação padrão (corrigiremos a animação adequadamente depois).
5. Salve o arquivo.

![Spinemodel properties](images/runner/2/spinemodel_properties.png)

Agora é hora de adicionar física para a colisão funcionar:

1. Adicione um componente *Collision Object* ao objeto de jogo do herói. (Clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Component</kbd>, depois selecione "Collision Object")
2. Clique com o botão direito no novo componente e selecione <kbd>Add Shape</kbd>. Adicione duas formas para cobrir o corpo do personagem. Uma esfera e uma caixa resolvem.
3. Clique nas formas e use o *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) para mover as formas para boas posições.
4. Marque o componente *Collision Object* e defina a propriedade *Type* como "Kinematic".

::: sidenote
Colisão "Kinematic" significa que queremos que colisões sejam registradas, mas a engine de física não resolverá colisões automaticamente nem simulará os objetos. A engine de física oferece suporte a vários tipos diferentes de objetos de colisão. Você pode ler mais sobre eles na [documentação de Física](/manuals/physics).
:::

É importante especificar com o que o objeto de colisão deve interagir:

1. Defina a propriedade *Group* para um novo grupo de colisão chamado "hero".
2. Defina a propriedade *Mask* para outro grupo, "geometry", com o qual este objeto de colisão deve registrar colisões. Observe que o grupo "geometry" ainda não existe, mas logo adicionaremos objetos de colisão pertencentes a ele.

Por fim, crie um novo arquivo *hero.script* e adicione-o ao objeto de jogo.

1. Clique com o botão direito na pasta *hero* no *Assets pane* e selecione <kbd>New ▸ Script File</kbd>. Nomeie o novo arquivo como *hero.script*.
2. Abra o novo arquivo, copie e cole o código a seguir no arquivo de script e salve. (O código é bem direto, exceto pelo solver que separa a forma de colisão do herói daquilo com que ela colide. Isso é feito pela função `handle_geometry_contact()`.)

![Hero game object](images/runner/2/hero_game_object.png)

::: sidenote
O motivo de tratarmos a colisão por conta própria é que, se em vez disso definíssemos o tipo do objeto de colisão do personagem como dynamic, a engine executaria uma simulação newtoniana dos corpos envolvidos. Para um jogo como este, tal simulação está longe do ideal; então, em vez de lutar contra a engine de física com várias forças, assumimos controle total.

Para fazer isso e tratar colisão corretamente, é necessário um pouco de matemática vetorial. Uma explicação completa sobre como resolver colisões cinemáticas é dada na [documentação de Física](/manuals/physics#resolving-kinematic-collisions).
:::

```lua
-- gravidade puxando o jogador para baixo em unidades de pixel/sˆ2
local gravity = -20

-- velocidade de decolagem ao pular em unidades de pixel/s
local jump_takeoff_speed = 900

function init(self)
    -- isto diz a engine para enviar entrada para on_input() neste script
    msg.post(".", "acquire_input_focus")

    -- salva a posicao inicial
    self.position = go.get_position()

    -- acompanha o vetor de movimento e se ha contato com o chao
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Devolve o foco de entrada quando o objeto e excluido
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Aplica gravidade se nao houver contato com o chao
        self.velocity = self.velocity + gravity
    end

    -- aplica velocidade ao personagem do jogador
    go.set_position(go.get_position() + self.velocity * dt)

    -- redefine estado volatil
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
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
    if message_id == hash("contact_point_response") then
        -- verifica se recebemos uma mensagem de ponto de contato. Uma mensagem para cada ponto de contato
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- permite pular apenas a partir do chao
    if self.ground_contact then
        -- define a velocidade de decolagem
        self.velocity.y = jump_takeoff_speed
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
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Adicione o script como um componente *Script* ao objeto do herói (clique com o botão direito na raiz de *hero.go* no *Outline* e selecione <kbd>Add Component from File</kbd>, depois selecione o arquivo *hero.script*).

Se quiser, agora você pode tentar adicionar temporariamente o personagem herói à coleção principal e executar o jogo para vê-lo cair através do mundo.

A última coisa de que precisamos para o herói ser funcional é entrada. O script acima já contém uma função `on_input()` que responde às ações "jump" e "touch" (para telas de toque). Vamos adicionar mapeamentos de entrada para essas ações.

1. Abra "input/game.input_bindings"
2. Adicione um key trigger para "KEY_SPACE" e nomeie a ação como "jump"
3. Adicione um touch trigger para "TOUCH_MULTI" e nomeie a ação como "touch". (Os nomes das ações são arbitrários, mas devem corresponder aos nomes no seu script. Observe que você não pode ter o mesmo nome de ação em vários triggers)
4. Salve o arquivo.

![Input bindings](images/runner/2/input_bindings.png)

## ETAPA 5 - Refatorando o nível

Agora que temos um personagem herói configurado com colisão e tudo mais, precisamos também adicionar colisão ao chão para que o personagem tenha algo com que colidir (ou sobre o que correr). Faremos isso em um segundo, mas primeiro devemos fazer uma pequena refatoração, colocar tudo do nível em uma coleção separada e limpar um pouco a estrutura de arquivos:

1. Crie um novo arquivo *level.collection* (clique com o botão direito em *main* no *Assets pane* e selecione <kbd>New ▸ Collection File</kbd>).
2. Abra o novo arquivo, clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Collection from File</kbd>, depois escolha *ground.collection*.
3. Em *level.collection*, clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Game Object File</kbd>, depois escolha *hero.go*.
4. Agora, crie uma nova pasta chamada *level* na raiz do projeto (clique com o botão direito no espaço em branco abaixo de *game.project* e selecione <kbd>New ▸ Folder</kbd>) e mova para ela os assets de nível que você criou até agora: os arquivos *level.collection*, *level.atlas*, a pasta "images" com as imagens do atlas do nível e os arquivos *ground.collection* e *ground.script*.
5. Abra *main.collection*, exclua *ground.collection* e, em vez disso, adicione *level.collection* (clique com o botão direito e <kbd>Add Collection from File</kbd>), que agora contém *ground.collection*. Certifique-se de posicionar a coleção em 0, 0, 0.

::: sidenote
Como você talvez já tenha notado, a hierarquia de arquivos vista no *Assets pane* é desacoplada da estrutura de conteúdo que você cria em suas coleções. Arquivos individuais são referenciados por arquivos de coleção e de objeto de jogo, mas sua localização é completamente arbitrária.

Se você quiser mover um arquivo para um novo local, o Defold ajuda atualizando automaticamente as referências ao arquivo (refatoração). Ao criar um software complexo, como um jogo, é extremamente útil poder alterar a estrutura do projeto conforme ele cresce e muda. O Defold incentiva isso e torna o processo suave, então não tenha medo de mover seus arquivos!
:::

Também devemos adicionar um objeto de jogo controller com um componente de script à coleção de nível:

1. Crie um novo arquivo de script. Clique com o botão direito na pasta *level* no *Assets pane* e selecione <kbd>New ▸ Script File</kbd>. Nomeie o arquivo como *controller.script*.
2. Abra o arquivo de script, copie o código a seguir para ele e salve:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Esta é uma propriedade de script. Definimos um valor padrão, mas qualquer instância posicionada do script pode sobrescrever esse valor diretamente na visualização de propriedades do editor.

3. Abra o arquivo *level.collection*.
4. Clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Game Object</kbd>.
5. Defina o *Id* como "controller".
6. Clique com o botão direito no objeto de jogo "controller" no *Outline*, selecione <kbd>Add Component from File</kbd> e selecione o arquivo *controller.script* na pasta *level*.
7. Salve o arquivo.

![Script property](images/runner/2/script_property.png)

::: sidenote
O objeto de jogo "controller" não existe em um arquivo, mas é criado no local dentro da coleção de nível. Isso significa que a instância do objeto de jogo é criada a partir dos dados no local. Isso é adequado para objetos de jogo de propósito único como este. Se você precisar de várias instâncias de algum objeto de jogo e quiser poder modificar o protótipo/template usado para criar cada instância, basta criar um arquivo de objeto de jogo e adicionar o objeto de jogo a partir do arquivo à coleção. Isso cria um objeto de jogo com uma referência ao arquivo como protótipo/template.

Agora, o propósito desse objeto de jogo "controller" é controlar tudo relacionado ao nível em execução. Em breve, esse script ficará encarregado de criar plataformas e moedas para o herói interagir, mas por enquanto ele apenas definirá a velocidade do nível.
:::

Na função `init()` do script controller do nível, ele envia uma mensagem ao componente de script do objeto controller do chão, endereçado por seu id:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

O id do objeto de jogo controller é definido como `"ground/controller"`, já que ele vive na coleção "ground". Depois adicionamos o id do componente `"controller"` após o caractere hash `"#"`, que separa o id do objeto do id do componente. Observe que o script do chão ainda não tem nenhum código para reagir à mensagem `set_speed`, então precisamos adicionar uma função `on_message()` a *ground.script* e adicionar lógica para isso.

1. Abra *ground.script*.
2. Adicione o seguinte código e salve o arquivo:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Todas as mensagens recebem hash internamente quando enviadas e devem ser comparadas com o valor com hash.
2. Os dados da mensagem são uma tabela Lua com os dados enviados com a mensagem.

![Add ground code](images/runner/insert_ground_code.png)

## ETAPA 6 - Física do chão e plataformas

Neste ponto, devemos adicionar colisão física ao chão:

1. Abra o arquivo *ground.collection*.
2. Adicione um novo componente *Collision Object* a um objeto de jogo adequado. Como o script do chão não responde a colisões (toda essa lógica está no script do herói), podemos colocá-lo em qualquer objeto de jogo _estacionário_ (os objetos de tile do chão não são estacionários, então evite-os). Um bom candidato é o objeto de jogo "controller", mas você pode criar um objeto separado para isso se preferir. Clique com o botão direito no objeto de jogo, selecione <kbd>Add Component</kbd> e selecione *Collision Object*.
3. Adicione uma box shape clicando com o botão direito no componente *Collision Object*, selecionando <kbd>Add Shape</kbd> e depois *Box*.
4. Use o *Move Tool* e o *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> e <kbd>Scene ▸ Scale Tool</kbd>) para fazer a caixa cobrir todos os tiles do chão.
5. Defina a propriedade *Type* do objeto de colisão como "Static", já que a física do chão não vai se mover.
6. Defina a propriedade *Group* do objeto de colisão como "geometry" e a *Mask* como "hero". Agora o objeto de colisão do herói e este registrarão colisões entre si.
7. Salve o arquivo.

![Ground collision](images/runner/2/ground_collision.png)

Agora você deve conseguir executar o jogo (<kbd>Project ▸ Build</kbd>). O personagem herói deve correr no chão, e deve ser possível pular com o botão <kbd>Space</kbd>. Se você executar o jogo em um dispositivo móvel, pode pular tocando na tela.

Para deixar a vida no mundo do jogo um pouco menos monótona, devemos adicionar plataformas para pular.

1. Arraste o arquivo de imagem *rock_planks.png* do pacote de assets para a subpasta *level/images*.
2. Abra *level.atlas* e adicione a nova imagem ao atlas (clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Images</kbd>).
3. Salve o arquivo.
4. Crie um novo arquivo *Game Object* chamado *platform.go* na pasta *level*. (Clique com o botão direito em *level* no *Assets pane* e selecione <kbd>New ▸ Game Object File</kbd>.)
5. Adicione um componente *Sprite* ao objeto de jogo (clique com o botão direito na raiz na visualização *Outline* e selecione <kbd>Add Component</kbd>, depois *Sprite*).
6. Defina a propriedade *Image* para se referir ao arquivo *level.atlas* e defina *Default Animation* como "rock_planks". Por conveniência, mantenha objetos de nível em uma subpasta "level/objects".
7. Adicione um componente *Collision Object* ao objeto de jogo da plataforma (clique com o botão direito na raiz na visualização *Outline* e selecione <kbd>Add Component</kbd>).
8. Certifique-se de definir o *Type* do componente como "Kinematic" e *Group* e *Mask* como "geometry" e "hero", respectivamente.
9. Adicione uma *Box Shape* ao componente *Collision Object*. (Clique com o botão direito no componente no *Outline* e selecione <kbd>Add Shape</kbd>, depois escolha *Box*).
10. Use o *Move Tool* e o *Scale Tool* (<kbd>Scene ▸ Move Tool</kbd> e <kbd>Scene ▸ Scale Tool</kbd>) para fazer a forma no componente *Collision Object* cobrir a plataforma.
11. Crie um arquivo *Script* *platform.script* (clique com o botão direito no *Assets pane* e selecione <kbd>New ▸ Script File</kbd>), coloque o código a seguir no arquivo e salve:

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Velocidade padrao em pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Apenas exclua a plataforma quando ela tiver saído pela borda direita da tela

12. Abra *platform.go* e adicione o novo script como componente (clique com o botão direito na raiz na visualização *Outline*, selecione <kbd>Add Component From File</kbd> e selecione *platform.script*).
13. Copie *platform.go* para um novo arquivo (clique com o botão direito no arquivo no *Assets pane* e selecione <kbd>Copy</kbd>, depois clique com o botão direito novamente e selecione <kbd>Paste</kbd>) e chame o novo arquivo de *platform_long.go*.
14. Abra *platform_long.go* e adicione um segundo componente *Sprite* (clique com o botão direito na raiz na visualização *Outline* e selecione <kbd>Add Component</kbd>). Como alternativa, você pode copiar o *Sprite* existente.
15. Use o *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) para posicionar os componentes *Sprite* lado a lado.
16. Use o *Move Tool* e o *Scale Tool* para fazer a forma no componente *Collision Object* cobrir ambas as plataformas.

![Platform](images/runner/2/platform_long.png)

::: sidenote
Observe que tanto *platform.go* quanto *platform_long.go* têm componentes *Script* que se referem ao mesmo arquivo de script. Isso é bom, pois quaisquer alterações que fizermos no arquivo de script afetarão o comportamento tanto das plataformas normais quanto das longas.
:::

## Gerando plataformas

A ideia do jogo é ser um endless runner simples. Isso significa que os objetos de jogo de plataforma não podem ser colocados em uma coleção no editor. Em vez disso, precisamos criá-los dinamicamente:

1. Abra *level.collection*.
2. Adicione dois componentes *Factory* ao objeto de jogo "controller" (clique com o botão direito nele, selecione <kbd>Add Component</kbd> e depois *Factory*)
3. Defina as propriedades *Id* dos componentes como "platform_factory" e "platform_long_factory".
4. Defina a propriedade *Prototype* de "platform_factory" para o arquivo */level/objects/platform.go*.
5. Defina a propriedade *Prototype* de "platform_long_factory" para o arquivo */level/objects/platform_long.go*.
6. Salve o arquivo.
7. Abra o arquivo *controller.script*, que gerencia o nível.
8. Modifique o script para que ele contenha o seguinte e então salve o arquivo:

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Talvez crie uma plataforma em altura aleatoria
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Valores predefinidos para a posição Y onde as plataformas serão criadas.
2. A função `update()` é chamada uma vez a cada frame e usamos isso para decidir se devemos criar uma plataforma normal ou longa em certos intervalos (para evitar sobreposições) e alturas. É fácil experimentar vários algoritmos de spawn para criar jogabilidades diferentes.

Agora execute o jogo (<kbd>Project ▸ Build</kbd>).

Uau, isso está começando a virar algo (quase) jogável...

![Running the game](images/runner/2/run_game.png)

## ETAPA 7 - Animação e morte

A primeira coisa que vamos fazer é dar vida ao personagem herói. Agora, o coitado está preso em um loop de corrida e não responde bem a pulos nem a qualquer outra coisa. O arquivo Spine que adicionamos a partir do pacote de assets na verdade contém um conjunto de animações exatamente para isso.

1. Abra o arquivo *hero.script* e adicione as seguintes funções _antes_ da função `update()` existente:

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- reproduz apenas animacoes que ainda nao estao em execucao
        if self.anim ~= anim then
            -- informa ao spine model para reproduzir a animacao
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- lembra qual animacao esta tocando
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- garante que a animacao correta esteja tocando
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. Encontre a função `update()` e adicione uma chamada a `update_animation`:

```lua
    ...
    -- aplica isso ao personagem do jogador
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Insert hero code](images/runner/insert_hero_code.png)

::: sidenote
Lua tem "escopo léxico" para variáveis locais e é sensível à ordem em que você coloca funções `local`. A função `update()` chama as funções locais `update_animation()` e `play_animation()`, o que significa que o runtime precisa ter visto as funções locais para conseguir chamá-las. É por isso que precisamos colocar as funções antes de `update()`. Se você inverter a ordem das funções, receberá um erro. Observe que isso se aplica apenas a variáveis `local`. Você pode ler mais sobre as regras de escopo de Lua e funções locais em http://www.lua.org/pil/6.2.html
:::

Isso é tudo que é necessário para adicionar animações de pulo e queda ao herói. Se você executar o jogo, perceberá que ele fica muito melhor de jogar. Talvez também perceba que, infelizmente, as plataformas podem empurrar o herói para fora da tela. Isso é um efeito colateral do tratamento de colisão, mas o remédio é fácil: adicionar perigo e tornar as bordas das plataformas perigosas!

1. Arraste *spikes.png* do pacote de assets para a pasta "level/images" no *Assets pane*.
2. Abra *level.atlas* e adicione a imagem (clique com o botão direito e selecione <kbd>Add Images</kbd>).
3. Abra *platform.go* e adicione alguns componentes *Sprite*. Defina *Image* como *level.atlas* e *Default Animation* como "spikes".
4. Use o *Move Tool* e o *Rotate Tool* para posicionar os espinhos ao longo das bordas da plataforma.
5. Para fazer os espinhos renderizarem atrás da plataforma, defina a posição *Z* dos sprites de espinho como -0.1.
6. Adicione um novo componente *Collision Object* às plataformas (clique com o botão direito na raiz no *Outline* e selecione <kbd>Add Component</kbd>). Defina a propriedade *Group* como "danger". Defina também *Mask* como "hero".
7. Adicione uma forma de caixa ao *Collision Object* (clique com o botão direito e selecione <kbd>Add Shape</kbd>) e use o *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) e o *Scale Tool* para posicionar a forma de modo que o personagem herói colida com o objeto "danger" ao atingir a plataforma pela lateral ou por baixo.
8. Salve o arquivo.

    ![Platform spikes](images/runner/3/danger_edges.png)

9. Abra *hero.go*, marque o *Collision Object* e adicione o nome "danger" à propriedade *Mask*. Depois salve o arquivo.

    ![Hero collision](images/runner/3/hero_collision.png)

10. Abra *hero.script* e altere a função `on_message()` para que tenhamos uma reação se o personagem herói colidir com uma borda "danger":

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- verifica se recebemos uma mensagem de ponto de contato
            if message.group == hash("danger") then
                -- Morre e reinicia
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Adicione rotação e movimento de queda ao herói quando ele morre. Isso pode ser muito melhorado!

11. Altere a função `init()` para enviar uma mensagem "reset" que inicializa o objeto, depois salve o arquivo:

    ```lua
    -- hero.script
    function init(self)
        -- isto nos permite lidar com entrada neste script
        msg.post(".", "acquire_input_focus")
        -- salva a posicao
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## ETAPA 8 - Redefinindo o nível

Se você testar o jogo agora, rapidamente ficará claro que o mecanismo de reset não funciona. O reset do herói está ok, mas você pode facilmente reiniciar em uma situação em que cairá imediatamente sobre a borda de uma plataforma e morrerá de novo. O que queremos é redefinir corretamente o nível inteiro quando houver morte. Como o nível é apenas uma série de plataformas criadas por spawn, só precisamos rastrear todas as plataformas criadas e então excluí-las no reset:

1. Abra o arquivo *controller.script* e edite o código para armazenar os ids de todas as plataformas criadas:

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Talvez crie uma plataforma em altura aleatoria
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, 0.6)
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Diz ao heroi para reiniciar.
            msg.post("hero#hero", "reset")
            -- Exclui todas as plataformas
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Usamos uma tabela para armazenar todas as plataformas criadas
    2. A mensagem "reset" exclui todas as plataformas armazenadas na tabela
    3. A mensagem "delete_spawn" exclui uma plataforma específica e a remove da tabela

2. Salve o arquivo.
3. Abra *platform.script* e modifique-o para que, em vez de apenas excluir uma plataforma que alcançou a borda mais à esquerda, ele envie uma mensagem ao controller do nível pedindo para remover a plataforma:

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Insert platform code](images/runner/insert_platform_code.png)

4. Salve o arquivo.
5. Abra *hero.script*. Agora, a última coisa que precisamos fazer é dizer ao nível para executar o reset. Movemos a mensagem que pede ao herói para reiniciar para o script controller do nível. Faz sentido centralizar o controle de reset assim, porque isso nos permite, por exemplo, introduzir uma sequência de morte temporizada mais longa com maior facilidade:

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Insert hero code](images/runner/insert_hero_code_2.png)

E agora o loop principal de reiniciar-morrer está no lugar!

Próximo passo - algo pelo que viver: moedas!

## ETAPA 9 - Moedas para coletar

A ideia é colocar moedas no nível para o jogador coletar. A primeira pergunta é como colocá-las no nível. Poderíamos, por exemplo, desenvolver um esquema de spawn que esteja de alguma forma em sintonia com o algoritmo de spawn de plataformas. Porém, no fim escolhemos uma abordagem muito mais fácil: fazer as próprias plataformas criarem moedas:

1. Arraste a imagem *coin.png* do pacote de assets para "level/images" no *Assets pane*.
2. Abra *level.atlas* e adicione a imagem (clique com o botão direito e selecione <kbd>Add Images</kbd>).
3. Crie um arquivo *Game Object* chamado *coin.go* na pasta *level* (clique com o botão direito em *level* no *Assets pane* e selecione <kbd>New ▸ Game Object File</kbd>).
4. Abra *coin.go* e adicione um componente *Sprite* (clique com o botão direito e selecione <kbd>Add Component</kbd> no *Outline*). Defina *Image* como *level.atlas* e *Default Animation* como "coin".
5. Adicione um *Collision Object* (clique com o botão direito no *Outline* e selecione <kbd>Add Component</kbd>)
e adicione uma forma *Sphere* que cubra a imagem (clique com o botão direito no componente e selecione <kbd>Add Shape</kbd>).
6. Use o *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) e o *Scale Tool* para fazer a esfera cobrir a imagem da moeda.
7. Defina o *Type* do objeto de colisão como "Kinematic", seu *Group* como "pickup" e sua *Mask* como "hero".
8. Abra *hero.go* e adicione "pickup" à propriedade *Mask* do componente *Collision Object*, depois salve o arquivo.
9. Crie um novo arquivo de script *coin.script* (clique com o botão direito em *level* no *Assets pane* e selecione <kbd>New ▸ Script File</kbd>). Substitua o código do template pelo seguinte:

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Adicione o arquivo de script como componente *Script* ao objeto da moeda (clique com o botão direito na raiz em *Outline* e selecione <kbd>Add Component from File</kbd>).

    ![Coin game object](images/runner/3/coin.png)

O plano é criar as moedas a partir dos objetos de plataforma, então coloque fábricas para as moedas em *platform.go* e *platform_long.go*.

1. Abra *platform.go* e adicione um componente *Factory* (clique com o botão direito no *Outline* e selecione <kbd>Add Component</kbd>).
2. Defina o *Id* da *Factory* como "coin_factory" e defina seu *Prototype* para o arquivo *coin.go*.
3. Agora abra *platform_long.go* e crie um componente *Factory* idêntico.
4. Salve os dois arquivos.

![Coin factory](images/runner/3/coin_factory.png)

Agora precisamos modificar *platform.script* para que ele crie e exclua as moedas:

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Velocidade padrao em pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Ao definir o pai da moeda criada como a plataforma, ela se moverá junto com a plataforma.
2. A animação faz as moedas dançarem para cima e para baixo em relação à plataforma que agora é o pai delas.

::: sidenote
Relações pai-filho são estritamente uma modificação do _scene graph_. Um filho será transformado (movido, escalado ou rotacionado) junto com seu pai. Se você precisar de relações adicionais de "posse" entre objetos de jogo, precisará rastrear isso especificamente no código.
:::

A última etapa deste tutorial é adicionar algumas linhas a *controller.script*:

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. O número de moedas a criar em uma plataforma normal.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- O dobro de moedas em plataformas longas
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Insert controller code](images/runner/insert_controller_code.png)

E agora temos um jogo simples, mas funcional! Se você chegou até aqui, talvez queira continuar por conta própria e adicionar o seguinte:

1. Contadores de pontuação e vidas
2. Efeitos de partículas para pickups e morte
3. Imagens de fundo bonitas

> Baixe a versão concluída do projeto [aqui](images/runner/sample-runner.zip)

Isso conclui este tutorial introdutório. Agora vá em frente e mergulhe no Defold. Temos muitos [manuais e tutoriais](//www.defold.com/learn) preparados para guiar você e, se ficar preso, será bem-vindo no [fórum](//forum.defold.com).

Boas criações com Defold!
