---
title: Defold para usuários de Godot
brief: Este guia apresenta o Defold a quem já usa o Godot. Ele compara conceitos familiares e mostra como usar as ferramentas e APIs correspondentes no Defold.
---

# Defold para usuários de Godot {#defold-for-godot-users}

Se você tem experiência com o Godot, já conhece boa parte do que precisa para criar um jogo no Defold. Este guia mostra como aproveitar essa experiência para começar a desenvolver rapidamente e explica as diferenças entre as duas engines que costumam causar confusão. Os exemplos usam o Godot 4.7.

## Introdução {#introduction}

O Defold é uma engine gratuita e multiplataforma para jogos 2D e 3D, com editor para Windows, Linux e macOS. O código-fonte completo da engine e do editor está disponível no [GitHub](https://github.com/defold/defold/). Você pode compilá-lo ou baixar uma versão pronta para o seu sistema operacional.

À primeira vista, o Defold se parece muito com o Godot. Nas duas engines, você monta o jogo a partir de peças reutilizáveis e define o comportamento delas com scripts. O Godot oferece muitos nós especializados. O Defold tem menos tipos de componentes, de uso mais geral, e usa scripts e módulos Lua para implementar a lógica do jogo. Por exemplo, o personagem do jogador pode ser um objeto de jogo (game object) com os seguintes componentes: um sprite ou modelo, um objeto de colisão e um script.

O Defold prioriza uma engine de execução compacta e o uso eficiente dos recursos, o que é especialmente útil em jogos para a web e dispositivos móveis. Alguns limites da engine são definidos de antemão para que a memória possa ser alocada com antecedência.

O Defold oferece menos elementos prontos para a lógica do jogo e a interface do que o Godot. Para obter os mesmos resultados, você pode combinar ou estender os componentes do Defold. O núcleo da engine foi projetado para ser leve. Você pode reduzir ainda mais seu tamanho removendo funcionalidades desnecessárias ou ampliá-lo com extensões nativas e módulos Lua. O [Portal de Assets do Defold](https://defold.com/assets/) reúne centenas de módulos, bibliotecas e extensões que ajudam, por exemplo, a criar interfaces complexas, construir pipelines de renderização mais avançados ou simplificar tarefas de desenvolvimento.

Para conhecer outras funcionalidades do Defold, consulte a [página do produto](https://defold.com/product/).

## Instalação {#installation}

1. Baixe a versão do Defold para o seu sistema operacional na [página de download](https://defold.com/download/).
2. Descompacte o arquivo e inicie o editor.

Você pode criar e executar seu primeiro projeto sem instalar um gerenciador separado ou modelos de exportação. Consulte o [manual de instalação](/manuals/install/) para ver as instruções da sua plataforma.

Você pode atualizar o Defold pelo próprio editor. Ao atualizar um projeto existente, confira as notas da versão e teste o jogo nas plataformas-alvo.

## Tela de boas-vindas {#welcome-screen}

Ao abrir o Defold, você verá uma tela de boas-vindas onde pode abrir projetos recentes ou criar um projeto. Ela tem uma função semelhante à do gerenciador de projetos do Godot.

![Gerenciador de projetos do Godot e tela de boas-vindas do Defold](images/godot/godot_1.png)

Para criar um projeto no Defold, escolha uma destas abas:

- Em **Modelos (Templates)**, comece com um projeto vazio, básico ou específico de uma plataforma.
- Em **Tutoriais (Tutorials)**, siga um projeto introdutório passo a passo.
- Em **Exemplos (Samples)**, execute e explore exemplos e kits iniciais.

![Gerenciador de projetos do Godot e tela de boas-vindas do Defold](images/godot/godot_2.png)

Na aba Exemplos, você encontra projetos iniciais e exemplos semelhantes aos da loja de assets do Godot:

![Gerenciador de projetos do Godot e tela de boas-vindas do Defold](images/godot/godot_3.png)

:[Hello World](../shared/hello-world.md)

---

## Visão geral do editor Defold {#defold-editor-overview}

Você reconhecerá os principais painéis, embora os nomes e as posições sejam diferentes. Para facilitar a comparação, reorganizamos os painéis do editor do Godot para aproximá-los da disposição padrão do Defold:

![Visão geral do editor do Godot](images/godot/godot_4.png)
![Visão geral do editor Defold](images/godot/godot_5.png)

| Godot | Defold | Função no editor Defold |
|---|---|---|
| Painel FileSystem | Conteúdo (Assets) | Permite gerenciar as pastas e os arquivos do projeto. A organização é a mesma do diretório do projeto no disco. |
| Vista 2D/3D e editores de recursos | Editor principal (Main editor) | Muda conforme o arquivo aberto: coleção, GUI, atlas, script etc. Pode ser dividido em dois painéis. |
| Painel Scene | Estrutura (Outline) | Mostra a estrutura do recurso atual. A árvore global da cena em execução não aparece aqui. |
| Inspector | Propriedades (Properties) | Mostra as propriedades do objeto, componente ou recurso selecionado. |
| Output e Debugger | Ferramentas (Tools) | Reúne o console, os erros de compilação, os resultados da busca e o depurador. |
| Integração com controle de versão | Arquivos Modificados (Changed Files) | Mostra as alterações quando o projeto usa Git. |

No editor 3D do Defold, você também verá uma barra de ferramentas no canto superior direito. Conheça seus controles no [manual de edição de cenas](/manuals/scene-editing/#toolbar-overview).

### Orientação de cena 2D e 3D {#2d-and-3d-scene-orientation}

:[Orientação de cena 2D e 3D](../shared/2d-and-3d-scene-orientation.md)

### Painéis {#panes}

Os painéis do Defold ficam na janela do editor. Para redimensioná-los, arraste as bordas. Você pode exibir ou ocultar os painéis com as teclas `F6`, `F7` e `F8` ou pelo menu Visualizar (`View`):

![Como exibir ou ocultar os painéis](images/editor/editor_panes.png)

### Coordenadas {#coordinates}

Em uma configuração 2D com o script de renderização padrão e sem componente de câmera na coleção, as coordenadas `(0, 0)` ficam no canto inferior esquerdo da janela do jogo. Y aumenta para **cima** e X aumenta para a direita.

Nas coordenadas de tela 2D que o Godot normalmente usa, Y aumenta para **baixo**. Lembre-se dessa diferença ao transferir posições ou código de movimento.

![Diferença entre as coordenadas 2D do Defold e do Godot](images/godot/godot_6.png)

No sistema de coordenadas 3D do Godot, assim como no Defold, Y aumenta para cima. O Defold usa um único sistema de coordenadas 3D para jogos 2D e 3D. Em uma configuração 2D típica, você trabalha no plano XY com projeção ortográfica. Você pode configurar a câmera de outra forma se precisar.

![Semelhança entre as coordenadas 3D do Defold e do Godot](images/godot/godot_7.png)

Saiba mais sobre o editor Defold no [manual de visão geral do editor](/manuals/editor/).

---

## Conceitos principais {#key-concepts}

No Godot, você monta **cenas** a partir de nós. No Defold, trabalha com componentes, objetos de jogo e coleções de objetos de jogo.

Por exemplo, no Godot você pode criar o personagem do jogador com um `Node2D`, adicionar um `Sprite2D` como filho e anexar um script ao nó raiz. Em seguida, você coloca o personagem na sua primeira cena (`Scene`).
No Defold, você pode criar o mesmo personagem com um objeto de jogo que contém os componentes `Sprite` e `Script`. Depois, você o coloca em uma coleção.

![Nós do Godot em comparação com objetos de jogo e componentes do Defold](images/godot/key_concepts.png)

O [manual de blocos de construção](/manuals/building-blocks/) explica esses conceitos em detalhes.

### Objetos de jogo {#game-objects}

No Defold, um **objeto de jogo** é um *contêiner* de componentes. Cada objeto tem:

- **identidade**
- **transformação** (posição, rotação e escala)

Um objeto de jogo pode desempenhar um papel semelhante ao de um `Node2D` ou `Node3D` no Godot. O Defold usa o mesmo tipo de objeto nos dois casos: todos os objetos de jogo têm uma transformação 3D, inclusive em jogos 2D.

Um objeto de jogo pode ser filho de outro e herdar sua transformação. Você pode organizar essas relações em uma coleção ou alterá-las em tempo de execução. Mudar o pai de um objeto não altera seu endereço.

Você pode definir um objeto **embutido** diretamente no arquivo `.collection` ou adicionar à coleção uma referência a um protótipo `.go` reutilizável. Editar a definição de um objeto embutido altera essa coleção, sem afetar os objetos definidos independentemente. Editar um protótipo `.go` atualiza as instâncias que o referenciam, respeitando os valores que foram sobrescritos em cada instância. Vários objetos, inclusive os embutidos, podem compartilhar recursos de componentes por referência. Alterar um desses recursos pode afetar todos os objetos que o utilizam. Se você reutilizar a coleção, as alterações nos objetos embutidos aparecerão em todos os lugares que a referenciam.

### Componentes {#components}

Componentes são blocos de construção especializados. Eles podem dar aos objetos de jogo uma aparência, propriedades físicas, som ou comportamento, por exemplo.

Adicione um componente `Sprite` ao objeto de jogo para exibir uma imagem, um `Sound` para reproduzir áudio ou um `Script` para executar código Lua.

Os componentes pertencem aos objetos de jogo e não podem ter componentes filhos. Para criar uma hierarquia, organize os próprios objetos em relações de pai e filho dentro de uma coleção.

Diferentemente do Godot, você não pode anexar um script diretamente a um componente para mudar seu comportamento. Você pode ajustá-lo no painel Propriedades ou criar componentes personalizados com extensões nativas, de forma semelhante às GDExtensions. Alguns exemplos são os componentes oficiais [Rive](https://github.com/defold/extension-rive) e [Spine](https://github.com/defold/extension-spine) e os componentes da comunidade [Sprite Loop](https://github.com/Balkan-Ram-Games/spriteloop-defold) e [Object Interpolation](https://github.com/indiesoftby/defold-object-interpolation).

No Defold, o próprio script é um componente que você pode adicionar a qualquer objeto de jogo. Um mesmo objeto pode ter vários componentes, inclusive vários scripts.

Como os componentes não têm hierarquia entre si e são independentes dos scripts personalizados, a engine consegue organizá-los de forma eficiente na memória. Essa é uma característica do projeto orientado a dados do Defold.

| Nó do Godot | Componente do Defold | Observações |
|---|---|---|
| `Sprite2D` / `AnimatedSprite2D` | [Sprite](/manuals/sprite/) | Renderiza texturas 2D e animações de flipbook a partir de um atlas (uma textura com várias imagens) ou de uma fonte de tiles. |
| `Area2D` / `RigidBody2D` / `StaticBody2D` e seus equivalentes em 3D | [Objeto de colisão](/manuals/physics-objects/) | Cuida da física e dos gatilhos. As formas de colisão são definidas no próprio componente, sem criar nós filhos separados. Os tipos disponíveis são estático, dinâmico, cinemático e gatilho. |
| Script `.gd` anexado a um nó | Script | Contém o código Lua que implementa a lógica, trata entradas e controla outros componentes e objetos de jogo. |
| `TileMapLayer` | [Tilemap](/manuals/tilemap/) | Renderiza um mapa em grade com uma fonte de tiles e camadas de mapa. |
| `Label` | [Nó de texto da GUI](/manuals/gui-text/) | Use um nó de texto para o texto da interface. Para texto no mundo do jogo, use um [componente Label](/manuals/label/). |
| `AudioStreamPlayer` | [Sound](/manuals/sound/) | Reproduz áudio. Você pode ajustar a velocidade (Speed), o panorama (Pan) e o ganho (Gain). |
| `Camera2D` / `Camera3D` | [Câmera](/manuals/camera/) | Oferece projeção ortográfica e em perspectiva. |
| Hierarquia de `Control` / `CanvasLayer` | [GUI](/manuals/gui/) | Um componente de GUI contém sua própria hierarquia de nós (Box, Text e Pie, por exemplo). Um script `.gui_script` dedicado controla a interface. |
| `MeshInstance3D` | [Modelo](/manuals/model/) ou [Malha](/manuals/mesh/) | Model exibe conteúdo 3D importado. Mesh permite usar geometria personalizada a partir de um buffer. |
| `CPUParticles2D` / `GPUParticles2D` e seus equivalentes em 3D | [ParticleFX](/manuals/particlefx/) | Emite partículas 2D ou 3D configuradas no editor de partículas do Defold. |
| `PackedScene.instantiate()` | Factory / Collection Factory | O Defold usa componentes distintos para definir quais objetos de jogo ou coleções podem ser criados em tempo de execução. |

### Coleções e mundos {#collections-and-worlds}

Uma **coleção** (collection) descreve os objetos de jogo, seus componentes e as relações de pai e filho. Você pode incluir uma coleção em outra para reutilizar um grupo de objetos, de forma semelhante a uma cena aninhada no Godot. O Defold não oferece um mecanismo de herança de cenas de uso geral como o do Godot. Para reutilizar conteúdo, use protótipos e coleções e personalize as instâncias com propriedades ou scripts.

O arquivo de coleção não se torna uma entidade em tempo de execução. Não há um objeto de coleção no qual chamar métodos, nem um nó raiz que represente a própria coleção. O arquivo contém as definições que o Defold usa para criar os objetos de jogo, seus componentes e a hierarquia entre eles durante a execução.

Ao iniciar o jogo, o Defold lê o arquivo `game.project`. A opção **Inicialização ▸ Coleção Principal (Bootstrap ▸ Main Collection)** define a primeira coleção a carregar, que dá origem ao mundo inicial do jogo. Os objetos das coleções aninhadas fazem parte desse mesmo mundo.

Uma **fábrica de coleção** (Collection Factory) instancia um grupo de objetos de jogo e seus componentes no mundo **existente** em que a fábrica se encontra.

Um **proxy de coleção** (Collection Proxy) carrega uma coleção separada e cria um **novo mundo**, com seu próprio espaço de endereços e sua própria simulação de física. Essa diferença importa, por exemplo, ao criar um inimigo que precisa interagir com a geometria de uma fase existente ou ao carregar uma fase inteira, possivelmente de forma assíncrona. Você verá essas operações adiante.

O Godot usa `PackedScene` tanto para criar instâncias quanto para trocar de cena. A troca de cena com `SceneTree` tem efeito semelhante ao carregamento de um mundo separado com um proxy de coleção.

A tabela resume essas relações:

| Godot | Defold | Observações |
|---|---|---|
| `Node3D` com nós filhos | Objeto de jogo com componentes | Os componentes fornecem funcionalidades e comportamento. O objeto de jogo fornece a transformação e a identidade. |
| Transformação de `Node2D` / `Node3D` | Transformação do objeto de jogo | Faz parte de todo objeto de jogo. |
| Cena / `PackedScene` | Protótipo de objeto de jogo (`.go`) ou coleção (`.collection`) | Um protótipo descreve um objeto. Uma coleção descreve um grupo de objetos e sua hierarquia. |
| `PackedScene.instantiate()` | Fábrica ou fábrica de coleção | Cria um objeto de jogo ou um grupo de objetos no mundo atual e retorna seus identificadores. |
| Troca de cena com `SceneTree` + `PackedScene.instantiate()` | Proxy de coleção | Carrega e cria um mundo separado e instancia os objetos de jogo dentro dele. |

---

## Escrevendo código {#code-writing}

O editor Defold inclui um editor de código para scripts e outros arquivos de texto. Ele oferece preenchimento automático, formatação e uma vista da estrutura do código, com seus dados e funções, entre outros recursos. Consulte a seção [Usando o editor de código integrado](/manuals/writing-code/#using-the-built-in-code-editor).

Se preferir, você pode abrir todos os scripts e arquivos de texto do Defold em um editor externo. O Defold também oferece recursos de integração com ferramentas como o VS Code. Consulte a seção [Usando um editor de código externo](/manuals/writing-code/#using-an-external-code-editor).

### Lua e scripts {#lua-and-scripts}

Os scripts de jogo do Defold são escritos em Lua. A linguagem lembra GDScript em alguns aspectos, mas há diferenças importantes. O Defold também oferece suporte a Teal, um dialeto de Lua com tipagem estática. Assim como o Godot tem GDExtensions, o Defold pode usar extensões nativas escritas em C, C++, C#, Objective-C, Java ou JavaScript, dependendo da plataforma-alvo. Voltaremos a elas mais adiante.

Os principais tipos de arquivo Lua usados no Defold são:

| Arquivo | Finalidade |
|---|---|
| `.script` | Implementa a lógica e o comportamento do jogo. Usa APIs como `go`, `factory`, `sprite`, `tilemap` ou `physics` para controlar outros objetos de jogo e componentes. |
| `.gui_script` | Define o comportamento da interface com a API `gui`. |
| `.render_script` | Controla a renderização com a API `render`. |
| `.lua` | Contém módulos Lua reutilizáveis, como bibliotecas de código ou funções utilitárias, carregados com `require()`. |

As tabelas Lua podem conter dados, funções ou ambos. Para organizar o código, você não precisa reproduzir a hierarquia de classes do GDScript. Coloque a lógica reutilizável em módulos e chame-a no script responsável pelo comportamento em questão.

Os scripts do Defold são compatíveis com Lua 5.1. Para entender as diferenças da linguagem e as particularidades de cada plataforma, leia [Lua no Defold](/manuals/lua/).

### Ciclo de vida da aplicação {#application-lifecycle}

Normalmente, um jogo no Defold começa com a inicialização e termina com a finalização. Entre essas fases, a cada quadro, o ciclo de atualização recalcula transformações, atualiza componentes, executa código e processa mensagens.

![Ciclo de vida da aplicação no Defold](images/application_lifecycle/application_lifecycle.png)

Assim como o Godot e outras engines, o Defold chama funções de script em diferentes momentos do ciclo de vida da aplicação. Os callbacks Lua têm nomes diferentes, mas suas funções são familiares:

| Godot | Defold | Observações |
|---|---|---|
| `_ready()` | `init(self)` | Inicializa os dados da instância e, se necessário, adquire o foco de entrada. |
| `_process(delta)` | `update(self, dt)` | Atualiza a cada quadro. |
| `_physics_process(delta)` | `fixed_update(self, dt)` | Atualiza em intervalos fixos quando essa opção está habilitada. |
| `_input(event)` | `on_input(self, action_id, action)` | Trata a entrada entregue aos componentes do objeto que a recebem. |
| Callback de sinal | `on_message(self, message_id, message, sender)` | Recebe mensagens de scripts ou componentes da engine. |
| `_exit_tree()` | `final(self)` | Libera recursos quando a instância do script é finalizada. |

O Godot chama `_ready()` nos nós filhos antes de chamá-lo no pai. O Defold não garante a ordem de inicialização ou atualização entre objetos de jogo e componentes. Coordene os objetos com mensagens para que nenhum deles dependa de outro executar `init()` primeiro.

Para usar `fixed_update()`, abra `game.project`, defina **Motor ▸ Frequência de Atualização Fixa (Engine ▸ Fixed Update Frequency)** como um valor positivo, por exemplo 60, e habilite **Física ▸ Usar Timestep Fixo (Physics ▸ Use Fixed Timestep)**.

O Defold também oferece `late_update(self, dt)` para tarefas que devem ocorrer depois das atualizações normais e antes da renderização, como ajustar a câmera. Se necessário, a engine ainda pode atualizar as transformações uma última vez depois desse callback.

Desativar um componente é diferente de excluí-lo.

Veja a sequência completa e os callbacks disponíveis para cada tipo de script no [manual de ciclo de vida da aplicação](/manuals/application-lifecycle/).

### Dados da instância e dados locais {#instance-data-vs-local-data}

Nos callbacks, cada instância de um componente de script recebe seu próprio `self` para guardar dados como `self.health` ou `self.target`. Mesmo dois componentes de script no mesmo objeto de jogo têm valores de `self` distintos. O parâmetro `self` é um userdata cujos campos você acessa como os de uma tabela. Ele não é uma tabela Lua, por isso operações como `pairs(self)` não funcionam. No Godot, as variáveis de instância (`var`) têm uma função semelhante.

O Godot trata cada arquivo `.gd` como a definição de uma classe. Quando você anexa um arquivo `.gd` a dez inimigos, o Godot cria dez instâncias da classe, cada uma com sua própria cópia das variáveis declaradas com var no nível do arquivo.

No Defold, o conteúdo de um arquivo `.script` é executado como um bloco de código Lua quando o recurso de script é carregado. Cada instância do componente de script recebe seu próprio `self` nos callbacks do ciclo de vida, como `init(self)` e `update(self, dt)`.

Já uma variável local declarada no nível do arquivo `.script` é compartilhada por **todas as instâncias** desse script. No Godot, o equivalente a essas variáveis locais do Defold são as variáveis estáticas (`static var`).

![Diferença entre os dados da instância e os dados locais no Defold](images/lua/self_local.png)

No exemplo acima, definir `self.has_shield` como `true` em uma instância não afeta as outras. Já a variável local `color` é compartilhada por todas as instâncias que usam esse arquivo de script. Uma alteração nela pode afetar todas essas instâncias.

### Propriedades {#properties}

Use `go.property()` para declarar uma **propriedade** editável por instância. O script acessa a propriedade por meio de `self`. Assim como `@export` no Godot, isso expõe o valor no editor. No Defold, as propriedades ficam no painel Propriedades (`Properties`):

![Propriedades no editor Defold](images/script-properties/properties.png)

Veja um exemplo para comparação em **GDScript** no Godot, com o script anexado a um `Node3D`:

```gdscript
extends Node3D

@export var speed: float = 100.0

func _process(delta):
    position.x += speed * delta
```

No Defold, o mesmo exemplo em **Lua**, em um componente de script:

```lua
go.property("speed", 100)

function update(self, dt)
    local position = go.get_position()
    position.x = position.x + self.speed * dt
    go.set_position(position)
end
```

Você pode acessar a propriedade Lua em `self.speed` e também definir seu valor ao criar o objeto. No Defold, as transformações usam `vector3` até mesmo em 2D, então você também precisa informar a coordenada Z.

Consulte [Propriedades de script](/manuals/script-properties/) para saber quais tipos de propriedade você pode usar e [Scripts](/manuals/script/) para ver mais exemplos.

---

## Mensagens e endereçamento {#messages-and-addressing}

No Godot, um objeto emite um sinal para avisar quem se conectou a esse evento. No Defold, os scripts costumam se comunicar enviando mensagens ao endereço de um objeto ou componente.

Você pode enviar uma mensagem com `msg.post()` a partir de qualquer script e receber e tratar mensagens no callback `on_message()` do script destinatário.

![Passagem de mensagens no Defold](images/message_passing/messages_overview.png)

Por exemplo, o personagem do jogador pode avisar à interface (HUD) que a pontuação mudou.

No Godot, o nó `Player` (`Node2D`) usa `player.gd`. Seu irmão `GUI` (`CanvasLayer`) usa `gui.gd` e contém um Label chamado `ScoreText`:

![Organização dos nós para o exemplo de sinais no Godot](images/godot/godot_signals.png)

No Defold, o objeto de jogo `player` tem o script `player.script`. O objeto de jogo `hud` tem um componente `gui` que contém um nó de texto chamado `score` e usa o script `hud.gui_script`:

![Organização dos objetos para o exemplo de mensagens no Defold](images/godot/defold_messages.png)

### Envio de mensagens {#sending-messages}

No Godot, Player e GUI são nós irmãos. Player conecta seu sinal `score_changed` a um método do script da GUI, que atualiza o Label.

**GDScript**, em `player.gd`:

```gdscript
extends Node2D

signal score_changed(value: int)
var score: int = 0

func _ready() -> void:
    score_changed.connect(get_node("../GUI").set_score)

func collect() -> void:
    score += 1
    score_changed.emit(score)

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        if event.keycode == KEY_SPACE:
            collect()
```

No Godot, `Player` define o sinal `score_changed`. Durante `_ready()`, ele conecta o sinal ao método `set_score()` do script da GUI. Cada chamada a `collect()` incrementa a pontuação e emite o sinal com o novo valor.

No Defold, associe a **barra de espaço** à ação `collect` no mapeamento de entrada. O objeto `player` inicializa sua pontuação em `init()` e solicita o foco de entrada para receber eventos. Quando `collect(self)` é chamada, a função incrementa a pontuação e envia uma mensagem `score_changed` para `/hud#gui` com o novo valor na tabela da mensagem.

**Lua**, em `player.script`:

```lua
function init(self)
    self.score = 0
    msg.post(".", "acquire_input_focus")
end

local function collect(self)
    self.score = self.score + 1
    msg.post("/hud#gui", "score_changed", { value = self.score })
end

function on_input(self, action_id, action)
    if action_id == hash("collect") and action.pressed then
        collect(self)
    end
end
```

No Defold, o jogador pode enviar a mensagem diretamente ao endereço do destinatário, sem precisar conectar antecipadamente um sinal à GUI como no Godot. Se você usar endereços relativos, poderá reutilizar as funções e os scripts em outros objetos.

### Recebimento e tratamento de mensagens {#receiving-and-handling-messages}

Ao receber o valor, a GUI atualiza o texto da pontuação.

**GDScript**, em `gui.gd`, anexado a `GUI` (`CanvasLayer`):

```gdscript
extends CanvasLayer

func set_score(value: int) -> void:
    $ScoreText.text = str(value)
```

O script da GUI recebe o valor emitido por meio de `set_score()` e atualiza seu nó filho `ScoreText`. O personagem do jogador não acessa nem altera esse Label diretamente.

No Defold, primeiro o script da GUI obtém o nó de texto da pontuação com `gui.get_node()`. Quando o componente de GUI recebe uma mensagem, `on_message()` verifica o identificador dela. Se for `score_changed`, o script lê `message.value` e atualiza o texto com `gui.set_text()`.

**Lua**, em `hud.gui_script`, atribuído ao componente de GUI:

```lua
function init(self)
    self.score_node = gui.get_node("score")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("score_changed") then
        gui.set_text(self.score_node, tostring(message.value))
    end
end
```

Observe que a mensagem do Defold tem como destinatário o **componente** de GUI. É o script desse componente que decide o que fazer com a mensagem e qual nó de texto atualizar.

As duas imagens mostram o texto inicial `Score: 0`. Quando a pontuação muda, os scripts do exemplo substituem todo o texto pelo valor numérico.

A chamada a `msg.post()` coloca a mensagem na fila para entrega posterior. Ela não chama o destinatário imediatamente nem retorna um resultado do script que recebe a mensagem. A entrega costuma ocorrer no mesmo quadro, mas o número de passagens de processamento é limitado e uma cadeia longa pode se estender aos quadros seguintes. Para responder, o destinatário pode enviar outra mensagem à URL do remetente recebida em `on_message()`. Consulte [Cadeias de mensagens](/manuals/message-passing/#message-chains).

Há outra diferença quando vários destinatários precisam receber uma notificação. No Godot, um mesmo sinal pode ser conectado a vários métodos. Ao emitir o sinal, todos os métodos conectados são notificados. No Defold, cada mensagem tem um endereço de destino. Para avisar vários destinatários, você pode enviar uma mensagem a cada um ou implementar um sistema de inscrições no jogo.

### Como encontrar um objeto pelo endereço no Defold {#finding-an-object-addressing-in-defold}

Não há um equivalente genérico a `get_node()` que retorne um objeto Lua representando outra instância de script. Para interagir com ela, use um identificador ou uma **URL** com funções da engine como `go.get_position()`, `go.set()` ou `msg.post()`.

Uma URL do Defold tem três partes:

```lua
socket:/path#component
```

- **Socket** identifica o mundo, por exemplo o da coleção principal carregada na inicialização ou um mundo carregado por um proxy de coleção.
- **Caminho (path)** identifica um objeto de jogo nesse mundo.
- **Componente (component)** identifica um componente nesse objeto.

Você pode usar uma URL completa ou omitir partes para formar um endereço relativo. Por exemplo, um script pode usar apenas a parte do componente para endereçar outro componente do mesmo objeto de jogo. Estas são algumas formas comuns:

| Endereço | Significado |
|---|---|
| `"#sprite"` | O componente sprite do objeto de jogo atual. |
| `"/player#controller"` | O componente controller do objeto player no mundo atual. |
| `"level:/player#controller"` | O componente controller do objeto player no mundo carregado chamado level. |
| `"."` | Abreviação para o objeto de jogo atual (`Game Object`). Seus componentes recebem a mensagem. |
| `"#"` | Abreviação para o componente de script atual (`Script`). |

Coleções aninhadas podem acrescentar prefixos aos caminhos dos objetos. As relações de pai e filho que determinam as transformações não alteram o endereço do objeto.

Ao criar objetos dinamicamente, guarde no código os identificadores retornados por `factory.create()` ou `collectionfactory.create()`.

O Defold não tem um equivalente integrado aos grupos que o Godot usa para consultar objetos ou chamar `call_group()`. Para obter esse comportamento, mantenha seu próprio registro de objetos ou implemente o encaminhamento de mensagens.

No Defold, os grupos de física dos objetos de colisão servem para filtrar colisões. A máscara define com quais outros grupos cada objeto pode colidir. Esses grupos não participam da passagem de mensagens.

Vale a pena ler os manuais de [Endereçamento](/manuals/addressing/) e [Passagem de mensagens](/manuals/message-passing/) logo no início. Eles respondem a muitas dúvidas que surgem no primeiro projeto.

---

## Autoloads e estado compartilhado {#autoloads-and-shared-state}

Você também pode chamar funções Lua diretamente por meio de módulos, como alternativa à comunicação pelo sistema de mensagens do Defold.

Se você usa um **Autoload** no Godot para guardar dados compartilhados, pode usar um módulo Lua para o mesmo fim no Defold. Salve o módulo, por exemplo, em `modules/game_state.lua` e carregue-o com `require "modules.game_state"`.

**GDScript**, com `game_state.gd` registrado como um Autoload chamado `GameState`:

```gdscript
extends Node
var score: int = 0
```

O equivalente em **Lua**, em `modules/game_state.lua`:

```lua
local M = { score = 0 }
return M
```

Outro script pode então acessar os dados compartilhados:

**GDScript**:

```gdscript
func add_point():
    GameState.score += 1
```

**Lua**:

```lua
local game_state = require "modules.game_state"

local function add_point()
    game_state.score = game_state.score + 1
end
```

A função `require()` mantém o módulo em cache, de modo que todos os scripts que o carregam compartilham a tabela retornada. Os scripts de objetos de jogo, de GUI e de renderização compartilham o estado Lua. Descarregar um proxy de coleção não reinicializa os dados do módulo. Você pode reinicializá-los explicitamente ao começar uma nova partida.

Um módulo Lua do Defold não é um objeto de jogo e não recebe callbacks do ciclo de vida, de mensagens ou de entrada. Se você usa um Autoload para executar código a cada quadro, reproduzir sons ou gerenciar transições de fase, coloque essa lógica no script de um objeto da coleção. Você também pode definir uma função no módulo e chamá-la explicitamente no callback correspondente do script.

Módulo Lua `my_module`:

```lua
local M = {}

function M.init(self)
    print("My init")
end

return M
```

Script Lua:
```lua
local my_module = require "my_module"

function init(self)
    my_module.init(self)
end
```

Para manter dados por instância, o módulo pode retornar uma função que cria uma tabela nova a cada chamada. Você pode guardar essa tabela em `self`. O [manual de módulos](/manuals/modules/) explica esse padrão e os cuidados ao usar hot reload.

---

## Criação de objetos e carregamento de fases {#spawning-objects-and-loading-levels}

### Fábricas {#factories}

Para criar um objeto de jogo em tempo de execução, adicione um componente **Fábrica (Factory)** e defina sua propriedade **Protótipo (Prototype)** como o arquivo `.go` desejado.

Para coleções, adicione uma **fábrica de coleção** que use o arquivo `.collection` desejado. Ela criará um grupo de objetos preservando as relações de pai e filho.

No exemplo do Godot abaixo, o nó que cria os projéteis é um `Node2D` na origem da cena. Seu script instancia os projéteis:

**GDScript**:

```gdscript
extends Node2D

const BULLET = preload("res://bullet.tscn")

func spawn_bullet():
    var bullet = BULLET.instantiate()
    bullet.position = Vector2(200, 100)
    add_child(bullet)
    return bullet
```

No Defold, o objeto de jogo do exemplo tem um componente de fábrica com o identificador `bullet_factory`. Com `factory.create()`, criamos uma instância do objeto que a fábrica referencia na propriedade Protótipo (`Prototype`):

![Configuração da fábrica no Defold](images/godot/defold_factory.png)

Na imagem, a fábrica é chamada em `init()`. A função a seguir mostra como informar a posição inicial do projétil e retornar seu identificador:

**Lua**:

```lua
local function spawn_bullet()
    local position = vmath.vector3(200, 100, 0)
    local id = factory.create("#bullet_factory", position)
    return id
end
```

A função do Defold retorna o **identificador** do objeto. Esse valor não tem métodos próprios. Passe-o às funções da API `go` ou monte uma URL de componente com `msg.url(nil, id, "controller")`, caso o objeto criado tenha um componente de script chamado `controller`.

Uma fábrica de coleção retorna uma tabela que associa o identificador de cada objeto no protótipo ao identificador da instância criada. Guarde a tabela para poder excluir os objetos depois:

```lua
local ids = collectionfactory.create("#collection_factory")
-- Later, when the spawned objects are no longer needed:
go.delete(ids)
```

Ao contrário de `queue_free()` no Godot, `go.delete(id)` no Defold não exclui os descendentes por padrão. Use `go.delete(id, true)` para excluir um objeto e todos os seus descendentes atuais. Se você passar a tabela da fábrica a `go.delete(ids)`, a função excluirá apenas os objetos listados e preservará outros objetos que tenham se tornado filhos deles posteriormente. Já a exclusão recursiva a partir de uma raiz conhecida atinge todos os objetos que estiverem abaixo dela naquele momento. Consulte [`go.delete()`](/ref/go/#go.delete).

O Defold reserva antecipadamente espaço para objetos de jogo e componentes. Se a criação de um objeto falhar por ter atingido um limite, verifique **Coleção ▸ Máximo de instâncias (Collection ▸ Max Instances)** e os limites dos componentes correspondentes em `game.project`. Aumentar todos os limites também aumenta o consumo de memória.

Consulte os manuais de [Fábrica](/manuals/factory/) e [Fábrica de coleção](/manuals/collection-factory/) para saber mais sobre propriedades, transformações e carregamento dinâmico.

### Proxies de coleção {#collection-proxies}

Para carregar uma coleção no Defold, por exemplo ao entrar em uma fase, adicione um componente **Proxy de Coleção (Collection Proxy)** a um objeto persistente. Defina a propriedade **Coleção (Collection)** como o arquivo `.collection` desejado.

![Configuração do proxy de coleção no Defold](images/godot/defold_proxy.png)

Envie `"load"` ou `"async_load"` com `msg.post()`. Quando terminar de carregar, o proxy responderá com `"proxy_loaded"`. Em seguida, você pode enviar `"init"` e `"enable"` usando o endereço recebido por on_message no parâmetro `sender` para inicializar e ativar o mundo carregado.

Assim você controla quais mundos estão carregados e em execução. Carregar uma coleção não substitui automaticamente a cena atual como uma troca de cena no Godot. Para remover um mundo, envie `"unload"` ao proxy correspondente. Ele desativará e finalizará o mundo antes de descarregá-lo e responderá com `"proxy_unloaded"`. Para controlar essas etapas individualmente, você também pode enviar `"disable"` e `"final"` separadamente.

Objetos de colisão em mundos carregados por proxies diferentes não colidem entre si, mesmo quando os dois mundos estão carregados e visíveis ao mesmo tempo. Objetos de jogo e componentes desses mundos, porém, podem trocar mensagens usando URLs que incluam o socket de destino.

Leia o [manual de proxy de coleção](/manuals/collection-proxy/) antes de implementar transições de fase. Ele explica o carregamento e o descarregamento, o encaminhamento de entrada e o controle da frequência de atualização de um mundo carregado.

## Recursos e assets do projeto {#project-resources-and-assets}

Um projeto do Defold é uma pasta que contém `game.project`, scripts e recursos. O painel **Conteúdo (Assets)** reproduz a estrutura dessa pasta. A maioria das definições de recursos do Defold fica em arquivos de texto, o que permite examinar as alterações em um sistema de controle de versão.

Ao compilar ou empacotar o jogo, o Defold converte os recursos de origem em formatos usados em tempo de execução. Os recursos referenciados a partir da coleção principal, das fábricas e dos proxies de coleção formam uma árvore de dependências. Um arquivo colocado na pasta do projeto sem ser referenciado não entra no pacote.

Não há um único equivalente de uso geral no Defold para as classes `Resource` personalizadas e os arquivos `.tres` do Godot. Use os tipos de recurso do Defold para conteúdo da engine e tabelas Lua ou arquivos de dados para conteúdo específico do jogo. A [API `resource`](/ref/resource/) permite criar ou alterar os tipos de recurso compatíveis em tempo de execução.

Por padrão, os recursos de uma fábrica são carregados junto com ela. Para adiar o carregamento, habilite **Carregar Dinamicamente (Load Dynamically)** e use `factory.load()` ou `collectionfactory.load()` para prepará-los de forma assíncrona. Já o conteúdo de um proxy de coleção só é carregado quando você o solicita.

Carregar depois um recurso que já está no pacote é diferente de baixá-lo posteriormente. Com o [Live Update](/manuals/live-update/), você pode excluir conteúdo do pacote inicial e disponibilizá-lo separadamente.

Saiba mais no [manual de gerenciamento de recursos](/manuals/resource/).

---

## Entrada {#input}

O `InputMap` do Godot corresponde ao arquivo `.input_binding` do Defold. Nele, você associa um evento de teclado, gamepad, mouse, toque ou texto a um nome de ação. Em `game.project`, selecione o arquivo de mapeamento na opção **Entrada ▸ Ligação do Jogo (Input ▸ Game Binding)**.

![Mapeamento de entrada](images/input/defold_input.png)

Para receber entrada, o objeto de jogo precisa **adquirir o foco de entrada**. Isso o coloca na pilha de entrada. Seus componentes de script e de GUI passam então a receber chamadas a `on_input()`.

Na imagem, a barra de espaço está associada a `collect`. O exemplo a seguir é independente e usa a ação `fire`, que você também precisa adicionar ao mapeamento de entrada:

**GDScript**:

```gdscript
extends Node

func _input(event):
    if event.is_action_pressed("fire"):
        print("Fire")
```

**Lua**:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("fire") and action.pressed then
        print("Fire")
    end
end
```

Dependendo da entrada, a tabela `action` contém campos como `pressed`, `released` e `value`.

A entrada percorre a pilha a partir do objeto que adquiriu o foco mais recentemente. Retorne `true` em `on_input()` para consumir a ação, por exemplo quando um menu já tratou um clique.

Para um mundo carregado por proxy, tanto o objeto que contém o proxy quanto os objetos que recebem entrada nesse mundo precisam adquirir o foco. Esquecer uma dessas etapas é uma causa comum de um script deixar de receber entrada depois de uma troca de fase.

Saiba mais nos manuais de [Entrada](/manuals/input/), [Mouse e toque](/manuals/input-mouse-and-touch/) e [Gamepads](/manuals/input-gamepads/).

---

## Física e colisões {#physics-and-collisions}

O **objeto de colisão** (Collision Object) do Defold corresponde aos corpos físicos do Godot. Ele reúne as configurações de física **e** as formas de colisão em um único componente. Em `game.project`, você pode escolher entre física 2D e 3D. No manifesto do aplicativo (App Manifest), também é possível escolher a versão da engine de física ou desativar a física por completo.

O Defold oferece quatro tipos de objeto de colisão:

| Godot | Tipo no Defold | Observações |
|---|---|---|
| `StaticBody2D` / `3D` | `Static` | Permanece imóvel. Objetos dinâmicos reagem ao contato com ele. |
| `RigidBody2D` / `3D` | `Dynamic` | A engine de física simula o movimento e resolve as colisões. |
| `CharacterBody2D` / `3D` | `Kinematic` | A engine de física fornece os dados das colisões. Seu código precisa reagir a elas e resolvê-las. |
| `Area2D` | `Trigger` | Informa apenas os eventos de entrada e saída, sem resposta física. |

Um objeto cinemático no Defold se comporta de maneira diferente de um `CharacterBody2D` que usa `move_and_slide()`. O Defold detecta os contatos e fornece os dados na mensagem de resposta à colisão. O movimento e a resposta ficam a cargo do seu script. Para implementar o controle de um personagem, consulte o [manual de resolução de colisões](/manuals/physics-resolving-collisions/).

Os grupos e as máscaras usam nomes em vez de camadas de colisão numeradas. Para que uma colisão seja registrada, **cada objeto precisa incluir na sua máscara o grupo do outro**.

![Grupos e máscaras de colisão no Defold](images/physics/collision_groups.png)

Na imagem, o objeto de jogo `danger` pertence ao grupo `player`, enquanto o objeto `player` pertence ao grupo `danger`. O nome do grupo não precisa coincidir com o identificador do objeto. As máscaras permitem que esses dois grupos interajam.

Por padrão, os objetos de colisão enviam mensagens aos scripts do objeto de jogo a que pertencem. Trate as mensagens `"collision_response"`, `"contact_point_response"` ou `"trigger_response"` em `on_message()`. A mensagem de gatilho inclui um campo `enter` que distingue entrada e saída. Mensagens de colisão e contato podem se repetir enquanto os objetos permanecem em contato. Uma nova mensagem, portanto, não significa necessariamente um novo impacto.

Você também pode tratar os eventos de física por meio de um [listener de eventos de colisão](/manuals/physics-events/). Escolha qual abordagem usar: registrar o listener substitui o envio padrão de mensagens de física, que deixarão de ser enviadas aos scripts.

Você pode usar tanto formas de colisão primitivas quanto formas complexas. Veja o [manual de formas de colisão](/manuals/physics-shapes).

![Forma de colisão de malha](images/physics/mesh.png)

Para saber mais sobre o sistema e suas APIs, consulte [Visão geral da física](/manuals/physics/), [Objetos de colisão](/manuals/physics-objects/), [Mensagens de colisão](/manuals/physics-messages/) e [Ray casts](/manuals/physics-ray-casts/).

---

## GUI

No Defold, você cria a interface em um **componente de GUI** a partir de um arquivo `.gui`. Dentro dele, você organiza nós como caixas, textos e setores circulares. Um script `.gui_script` próprio controla o componente, de forma semelhante a um script anexado a um `CanvasLayer` no Godot.

Esses nós pertencem à GUI e ficam fora da hierarquia de transformações dos objetos de jogo. Por padrão, a GUI é desenhada sobre o jogo e não acompanha o movimento da câmera nem do objeto que contém o componente de GUI.

Atribua um `.gui_script` ao componente para controlar os nós com `gui.get_node()`, `gui.set_text()` e outras funções de `gui`. A API `gui` só está disponível nos scripts de GUI, enquanto a API `go` é exclusiva dos scripts de objetos de jogo. Para que os dois tipos de script se comuniquem, use mensagens, como no exemplo da pontuação.

Com os templates, você pode reutilizar a hierarquia de nós de outra GUI, de modo semelhante à reutilização de um nó no Godot.

O Defold fornece nós simples para montar a interface. Elementos como Button ou os Containers de layout do Godot não vêm prontos. Para criar um botão, por exemplo, combine uma caixa com um texto, trate a entrada no script de GUI e use `gui.pick_node()` para verificar se o ponteiro está sobre o botão.

A GUI do Defold também permite usar **camadas (Layers)**, semelhantes às camadas de `CanvasLayer` no Godot. No Defold, cada camada recebe um nome em vez de um número. A posição na lista Layers determina a ordem de desenho.

Âncoras, pivôs, modos de ajuste e [layouts de GUI](/manuals/gui-layouts/) ajudam a adaptar a interface a telas diferentes. Esses mecanismos têm funções semelhantes às dos Containers de layout do Godot, mas não funcionam exatamente da mesma maneira.

Para interfaces maiores ou mais complexas, você pode escrever seu próprio código de layout e widgets ou usar uma biblioteca da comunidade, como [Druid](https://defold.com/assets/druid/).

Para saber mais, consulte os manuais de [GUI](/manuals/gui/) e [Scripts de GUI](/manuals/gui-script/).

## Animação {#animation}

O Defold oferece várias ferramentas de animação que, em conjunto, cobrem diferentes usos de `AnimationPlayer`:

- **Animação de flipbook** reproduz sequências de imagens em sprites e nós de caixa da GUI.
- **Animação de modelo** reproduz animações de esqueleto importadas em modelos 3D.
- **Animação de propriedade** interpola valores com `go.animate()` ou `gui.animate()`.
- **[Spine](https://github.com/defold/extension-spine)**, **[Rive](https://github.com/defold/extension-rive)** e **[SpriteLoop](https://github.com/Balkan-Ram-Games/spriteloop-defold)** são outros formatos de animação disponíveis por meio de extensões.

### Tweens e animações de propriedades no Defold {#tweens-defold-property-animations}

Você pode reproduzir um Tween simples do Godot com uma animação de propriedade no Defold. Os dois exemplos movem um objeto até `X = 200` em meio segundo:

**GDScript**, em um `Node2D`:

```gdscript
func move_to_target():
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 200.0, 0.5)
```

**Lua**, em um script de objeto de jogo:

```lua
local function move_to_target()
    go.animate(".", "position.x", go.PLAYBACK_ONCE_FORWARD,
        200, go.EASING_OUTQUAD, 0.5)
end
```

Para criar sequências que alterem várias propriedades, reproduzam sons ou disparem eventos no jogo, coordene as etapas em Lua. O Defold ainda não tem um editor de linha do tempo específico para animações. O Editor de Curvas, no painel Ferramentas, edita as curvas das propriedades de ParticleFX ao longo da vida de uma partícula.

Consulte [Animação](/manuals/animation/), [Animação de propriedade](/manuals/property-animation/), [Animação de flipbook](/manuals/flipbook-animation/) e [Animação de modelo](/manuals/model-animation/). A visão geral também traz links para as extensões Spine e Rive.

## Mapas de tiles {#tilemaps}

O componente `Tilemap` do Defold usa uma **fonte de tiles** (tile source) que contém uma grade de tiles. Você pode pintar tiles em camadas no editor de mapas integrado e alterá-los em tempo de execução com a API `tilemap`.

O mapa de tiles integrado do Defold usa uma grade retangular. Os conjuntos de terrenos e as regras de colocação automática de tiles do Godot ainda não podem ser transferidos diretamente. Você pode reproduzir o comportamento necessário em código ou usar um editor de mapas externo que exporte para o Defold, como o [Tiled](https://doc.mapeditor.org/en/stable/manual/export-defold/?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website) ou o [TileSetter](https://www.tilesetter.org/docs/exporting?utm_source=defold&utm_medium=referral&utm_campaign=defold&utm_content=defold-website#defold).

Consulte o [manual de mapas de tiles](/manuals/tilemap/).

---

## Pipeline de renderização {#rendering-pipeline}

O Defold permite programar todo o pipeline de renderização com um arquivo `.render` personalizado, um `.render_script` e shaders. Você também pode usar o pipeline padrão da engine, que atende à maioria dos jogos.

O script de renderização padrão do Defold lida com conteúdo 2D e 3D comum. Um `.render_script` personalizado controla as passagens de desenho, os alvos de renderização e outras operações. Por meio de predicados de renderização, o script usa as tags dos materiais para selecionar grupos de componentes. O Defold oferece renderização baseada em física (PBR) de fábrica. A comunidade também disponibiliza diversos pipelines e shaders personalizados.


O Defold usa shaders GLSL e mantém os programas de vértices e fragmentos em arquivos separados. O Godot tem sua própria linguagem de shaders, semelhante a GLSL, com recursos específicos da engine. Por isso, shaders do Godot ou de outras fontes, como o Shadertoy, podem precisar de ajustes. Consulte os requisitos do Defold no [manual de shaders](/manuals/shader/).

No Defold, os **materiais** associam os programas de vértices e de fragmentos (shaders) às texturas, constantes e atributos dos shaders. Você pode usar como ponto de partida os materiais padrão que ficam na pasta `builtins`.

Quando precisar alterar o comportamento padrão, consulte [Renderização](/manuals/render/), [Materiais](/manuals/material/) e [Shaders](/manuals/shader/).

### Ordem de desenho e camadas {#draw-order-and-layers}

O inteiro `z_index` do Godot não corresponde diretamente a uma propriedade do Defold. No Defold, o efeito de deslocar um objeto ao longo de Z depende da configuração da renderização: esse eixo nem sempre corresponde à profundidade na tela. Como o Defold é uma engine 3D, ele usa a coordenada Z do objeto no espaço em vez de um índice inteiro exclusivo para ordenar objetos em 2D.

Na configuração ortográfica **padrão**, o Defold só renderiza objetos com posição Z entre -1,0 e 1,0. Você pode usar valores fracionários, como 0,1 e 0,2, para separar camadas, ou mudar o intervalo enviando uma mensagem ao script de renderização. Nessa configuração simples, a posição Z do objeto de jogo ou do componente Sprite determina a ordem de desenho: valores maiores aparecem sobre valores menores, o que lembra `z_index` no Godot. Esse comportamento pode mudar com uma câmera em perspectiva ou um `.render_script` personalizado.

Os nós de GUI ignoram o Z do mundo. Por padrão, a engine desenha os componentes de GUI em uma passagem separada, depois dos sprites do mundo. Alterar a posição Z de um nó de GUI não muda sua ordem de desenho. A ordem depende da posição dos nós na hierarquia da GUI, de cima para baixo no painel Estrutura, e das camadas (`Layers`). As camadas têm prioridade sobre a ordem dos nós para permitir o agrupamento das chamadas de desenho. Nesse sentido, lembram as camadas de `CanvasLayer`.

### Câmeras e coordenadas {#cameras-and-coordinates}

Adicione um componente `Camera` a um objeto de jogo. Para mover a câmera, mova esse objeto. Use a projeção ortográfica para uma vista 2D típica ou a projeção em perspectiva para 3D.

Com o script de renderização padrão, a última câmera habilitada é usada automaticamente. Sem nenhuma câmera, a engine exibe uma vista 2D ortográfica. Se houver uma única câmera habilitada, ela será usada. Você pode começar com essa configuração e personalizar a renderização conforme as necessidades do jogo.

A câmera muda a relação entre as coordenadas do mundo e as da tela. Para tratar a entrada do ponteiro no mundo, converta as coordenadas com as funções da [API de câmera](/ref/camera/). As coordenadas do ponteiro não são, em geral, posições no mundo. Por padrão, o teste de seleção dos nós de GUI continua a usar as coordenadas da GUI.

Consulte o [manual de câmera](/manuals/camera/) para saber mais sobre projeção, zoom e conversão de coordenadas.

---

## Exportação de um jogo {#exporting-a-game}

No Defold, exportar o jogo é **empacotá-lo** (bundling). Selecione **Projeto ▸ Empacotar (Project ▸ Bundle)**, escolha a plataforma-alvo e configure as opções do pacote. O editor fornece as ferramentas de build. Você não precisa instalar modelos de exportação separadamente como no Godot.

O arquivo `game.project` reúne as configurações do projeto e das plataformas, incluindo a coleção principal, o mapeamento de entrada e o tamanho da tela. Observe os requisitos de assinatura e de publicação na loja da plataforma. Projetos com extensões nativas precisam de conexão com a rede para compilar uma engine personalizada pelo serviço de build na nuvem. Como alternativa, você pode configurar o serviço para executar localmente.

O tamanho final do pacote depende dos assets, das extensões e das configurações de build. Gere um relatório de compilação (`Build Report`) para ver o que está incluído.

Leia [Empacotamento](/manuals/bundling/), [Configurações do projeto](/manuals/project-settings/) e [HTML5](/manuals/html5/). Teste um pacote na plataforma-alvo desde o início, especialmente se o jogo usar shaders, extensões nativas ou serviços da plataforma.

## Bibliotecas e extensões {#libraries-and-extensions}

Você pode adicionar ao projeto **dependências de biblioteca** com scripts e recursos compartilhados. Adicione as URLs dos arquivos das bibliotecas em `game.project` e use o comando Buscar Bibliotecas. O [Portal de Assets](https://defold.com/assets/) do Defold é um bom lugar para encontrá-las. A extensão de editor **Asset Store** permite pesquisar e baixar assets diretamente no editor, como no Godot.

Para personalizar o editor, use os **scripts e a interface do editor**. Com eles você pode adicionar comandos, automatizar tarefas e criar interfaces próprias, por exemplo para editar fases mais depressa, criar recursos ou automatizar a colocação de tiles. Eles desempenham algumas das funções de `EditorPlugin` e `@tool` do Godot, mas seguem o ciclo de vida do Defold e usam a API `editor` da engine.

Se você precisar de funcionalidades da engine além do que Lua oferece, as **extensões nativas** podem expor código nativo aos scripts ou acrescentar componentes e integrações com plataformas. Seu papel é semelhante ao de GDExtension, com outra API e outro processo de build.

Consulte [Bibliotecas](/manuals/libraries/), [Scripts do editor](/manuals/editor-scripts/) e [Extensões nativas](/manuals/extensions/).

## Hot reload

Com o hot reload do Defold, você pode atualizar um jogo durante a execução. Compile e execute o jogo, edite um recurso compatível, salve-o e escolha **Arquivo ▸ Recarregar (File ▸ Hot Reload)** para aplicar a alteração. O hot reload também funciona quando o alvo do editor é uma versão de depuração em execução em um dispositivo.

Recarregar um script não chama `init()` novamente. Os dados das instâncias são preservados, portanto um novo valor de inicialização não aparece automaticamente em `self`. Use `on_reload(self)` para ajustar o estado existente ou faça outra build se precisar recomeçar do zero. Se você recarregar um módulo Lua que retorna uma tabela nova, os outros scripts que guardaram referências à tabela antiga continuarão usando a antiga. Consulte o [manual de módulos](/manuals/modules/).

Leia o [manual de hot reload](/manuals/hot-reload/).

## Pontos de interrupção e depuração {#breakpoints-and-debugging}

Com o depurador integrado do editor, você pode definir pontos de interrupção, avançar passo a passo e inspecionar os valores do programa. Consulte o Console para ver a saída do jogo e a aba Erros de Compilação para encontrar problemas de build. O perfilador ajuda a analisar o tempo de cada quadro, o uso de memória e a renderização. Os relatórios de compilação mostram quais recursos contribuem para o tamanho do pacote.

Consulte [Depuração da lógica do jogo](/manuals/debugging-game-logic/) e [Análise de desempenho](/manuals/profiling/).

## Fluxos de trabalho automatizados {#automated-workflows}

O Defold oferece várias interfaces para automatizar tarefas e desenvolver com assistência de IA. Scripts do editor podem automatizar tarefas repetitivas. A API HTTP do editor, documentada com OpenAPI, permite que ferramentas externas e agentes de IA inspecionem projetos, executem comandos e iniciem builds. Com o serviço HTTP da engine e a extensão Automation Bridge, é possível inspecionar o jogo em execução, simular entradas e capturar a tela. Juntas, essas ferramentas permitem que agentes de programação como Codex, Claude Code e Cursor modifiquem projetos, compilem jogos, testem o comportamento e corrijam problemas em ciclos sucessivos.

Para saber mais, consulte [Automação](/manuals/automation/), [API HTTP do editor](/manuals/editor-http-api/), [Serviço da engine](/manuals/engine-service/) e [Testes automatizados](/manuals/automated-testing/).

---

## Erros comuns {#common-pitfalls}

### Tratar uma coleção como nó raiz {#treating-a-collection-as-a-root-node}

Uma coleção do Defold descreve os objetos de jogo e as relações entre eles, mas não se torna um objeto raiz durante a execução. Para coordenar os objetos de uma fase, adicione um objeto de jogo com um script próprio. Consulte [Coleções e mundos](#collections-and-worlds).

### Excluir uma hierarquia {#deleting-a-hierarchy}

No Godot, `queue_free()` exclui também os descendentes do nó. No Defold, `go.delete(id)` preserva os objetos filhos, a menos que você solicite a exclusão recursiva. Consulte [Fábricas](#factories) para ver um exemplo e saber como excluir os objetos criados por uma fábrica de coleção.

### Contar com herança de cenas {#expecting-scene-inheritance}

O Defold não oferece o mesmo mecanismo de herança de cenas do Godot. Isso significa que você não pode modificar livremente a estrutura de uma cena derivada como faria lá. Você pode reutilizar protótipos e coleções e personalizar as instâncias com propriedades ou scripts. Consulte [Coleções e mundos](#collections-and-worlds).

### Chamar outro script por uma referência ao objeto {#calling-another-script-through-an-object-reference}

O identificador de um objeto de jogo não dá acesso direto a funções em outra instância de script. Para que os componentes se comuniquem, use mensagens. Para compartilhar funções, coloque-as em um módulo Lua. Consulte [Mensagens e endereçamento](#messages-and-addressing) e [Autoloads e estado compartilhado](#autoloads-and-shared-state).

### Guardar o estado da instância em uma variável local no nível do arquivo {#keeping-instance-state-in-a-top-level-local}

Todas as instâncias que usam o mesmo arquivo de script compartilham as variáveis locais declaradas no nível do arquivo. Assim, mudar o valor para uma instância pode afetar as demais. Guarde o estado de cada instância em `self`, como explicado em [Dados da instância e dados locais](#instance-data-vs-local-data).

### Presumir que a entrada já está habilitada {#assuming-input-is-enabled-automatically}

Um objeto de jogo precisa adquirir o foco de entrada para que seus componentes recebam eventos de entrada. Se o mundo foi carregado por um proxy, o objeto que contém o proxy também precisa do foco. Consulte [Entrada](#input) para entender os mapeamentos, o foco e a pilha de entrada.

### Esperar que um objeto cinemático deslize automaticamente {#expecting-automatic-sliding-from-a-kinematic-collider}

O Defold detecta os contatos de objetos de colisão cinemáticos, mas não reproduz automaticamente o comportamento de `move_and_slide()` do Godot. O script precisa implementar o movimento e a resposta à colisão. Consulte [Física e colisões](#physics-and-collisions).

### Configurar apenas uma máscara de colisão {#configuring-only-one-collision-mask}

Se só um dos objetos estiver configurado para interagir com o outro, a colisão não será registrada. Cada objeto precisa incluir na sua máscara o grupo do outro. Consulte [Física e colisões](#physics-and-collisions).

### Copiar as coordenadas 2D sem ajustes {#copying-2d-coordinates-unchanged}

O eixo Y do Godot cresce no sentido oposto ao de uma configuração 2D típica do Defold. Por isso, copiar o código de movimento pode fazer o objeto andar na direção errada. Com uma câmera, as posições na tela e no mundo também podem diferir. Consulte [Coordenadas](#coordinates) e [Câmeras e coordenadas](#cameras-and-coordinates).

### Usar o Z do mundo para ordenar nós de GUI {#using-world-z-to-sort-gui-nodes}

Mudar a posição Z de um nó de GUI não altera sua ordem de desenho no Defold. Use a ordem dos nós e as camadas da GUI, como explicado em [Ordem de desenho e camadas](#draw-order-and-layers).

### Esperar que o hot reload reinicie o objeto {#expecting-hot-reload-to-restart-the-object}

Recarregar um script com hot reload não executa `init()` de novo. As instâncias existentes podem, portanto, conservar os valores antigos. Consulte [Hot reload](#hot-reload) para saber como tratar o estado de instâncias e o recarregamento de módulos.

### Esperar que descarregar uma fase apague o estado compartilhado {#expecting-a-level-unload-to-clear-shared-state}

Tanto o estado de um Autoload do Godot quanto os dados em cache de um módulo Lua podem persistir entre fases. Reinicialize os dados compartilhados explicitamente quando necessário. Ao contrário de um nó Autoload, um módulo Lua não recebe callbacks automaticamente. Consulte [Autoloads e estado compartilhado](#autoloads-and-shared-state).

## Para onde ir agora? {#where-to-go-from-here}

O [Defold Learn Hub](https://defold.com/learn/) reúne manuais, exemplos, tutoriais, vídeos, cursos e outros materiais para começar a desenvolver e conhecer melhor o Defold. Estes são bons pontos de partida:

- [Blocos de construção](/manuals/building-blocks/)
- [Endereçamento](/manuals/addressing/)
- [Passagem de mensagens](/manuals/message-passing/)
- [Exemplos do Defold](/examples/)
- [Tutoriais](/tutorials/)
- [Referência da API](/ref/go/)

Se precisar de ajuda, pergunte no [Fórum do Defold](https://forum.defold.com/) ou no [Discord](https://defold.com/discord/). Compartilhar um projeto pequeno e descrever o comportamento do Godot que você quer reproduzir facilita a ajuda de outras pessoas.
