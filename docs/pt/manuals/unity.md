---
title: Defold para usuários de Unity
brief: Este guia ajuda você a migrar rapidamente para o Defold se já tem experiência com Unity. Ele cobre alguns dos principais conceitos usados no Unity e explica as ferramentas e métodos correspondentes no Defold.
---

# Defold para usuários de Unity

Se você já tem experiência com Unity, este guia ajuda você a se tornar produtivo no Defold rapidamente. Ele foca no essencial e aponta para os manuais oficiais do Defold sempre que detalhes mais profundos forem necessários.

## Introdução

O Defold é uma engine de jogos 3D totalmente gratuita e verdadeiramente multiplataforma, com um Editor para Windows, Linux e macOS. O código-fonte completo está disponível no [Github](https://github.com/defold/defold/).

O Defold é focado em desempenho, mesmo em dispositivos de baixo custo. Ele usa um modelo de componentes pequeno, em que muitas interações de gameplay são tratadas por código e passagem de mensagens.

O Defold é muito menor que o Unity. O tamanho da engine com um projeto vazio fica entre 1-3 MB em todas as plataformas. Você pode remover partes adicionais da engine e mover parte do conteúdo do jogo para [Live Update](/manuals/live-update), baixando-o separadamente depois. Uma comparação de tamanho e outros motivos para escolher o Defold são descritos na [página Why Defold](https://defold.com/why/).

Para personalizar o Defold conforme suas necessidades, você pode escrever por conta própria ou usar algo existente:

1. Pipeline de renderização totalmente programável (script de renderização + materiais/shaders), com alguns backends para escolher (OpenGL, Vulkan etc.).
2. Código e componentes como Native Extensions (C++/C#).
3. Editor Scripts e widgets de UI para personalizar o Editor.
3. Builds alteradas da engine e do editor, já que o código-fonte completo e um pipeline de build estão disponíveis.

Também recomendamos assistir ao vídeo da Game From Scratch sobre [Defold para desenvolvedores Unity](https://www.youtube.com/watch?v=-3CzCbd4QZ0).

---

## Instalação

1. Baixe o Defold para o seu sistema operacional.
2. Descompacte e execute.

É isso. Sem hub, sem SDK adicional, sem instalação de toolchains ou bundles de plataforma. É por isso que dizemos que o Defold não exige configuração inicial.

Se precisar de mais detalhes, leia este curto [manual de instalação](/manuals/install/).

### Versões

O Defold é atualizado com frequência e não tem uma trilha "LTS". Recomendamos sempre usar a versão mais recente. Novas versões são lançadas regularmente - normalmente todo mês, com cerca de duas semanas de beta público. Você pode atualizar o Defold diretamente pelo Editor.

---

## Tela de boas-vindas

O Defold recebe você com uma tela de boas-vindas semelhante ao Unity Hub, onde é possível abrir projetos recentes:

![Welcome screen comparison](images/unity/unity_defold_start.png)

Ou iniciar um novo a partir de:
- `Templates` - projetos vazios básicos para uma configuração mais rápida para uma plataforma ou gênero específico,
- `Tutorials` - tours guiados de aprendizado que ajudam você a dar os primeiros passos,
- `Samples` - casos de uso e exemplos oficiais ou contribuídos pela comunidade,

![Welcome Templates comparison](images/unity/unity_defold_templates.png)

Quando você criar seu primeiro projeto e/ou abri-lo, ele será aberto no Defold Editor.

## Hello World

Esta é uma forma rápida de fazer algo no Defold: siga os passos e depois volte para ler o restante do manual.

1. Selecione um projeto vazio em `Templates`, dê um nome em `Title`, escolha um local e crie-o clicando em `Create New Project`. Ele será aberto no Defold Editor.
![Hello World Step 1](images/unity/helloworld_1.png)
2. No lado esquerdo, no painel `Assets`, abra a pasta `main` e dê duplo clique em `main.collection` para abri-la.
3. No lado direito, no painel `Outline`, clique com o botão direito em `Collection` e selecione `Add Game Object`.
![Hello World Step 2](images/unity/helloworld_2.png)
4. Clique com o botão direito no objeto de jogo `go` criado, selecione `Add Component` e depois `Label`.
![Hello World Step 3](images/unity/helloworld_3.png)
5. Abaixo, no lado esquerdo, no painel `Properties`, digite algo na propriedade `Text`.
6. Na visualização principal e central da cena, arraste, mova e solte o label para uma posição em torno de `(480,320,0)`, ou altere isso em `Properties`: `Position`.
![Hello World Step 4](images/unity/helloworld_4.png)
7. Depois de alterar a posição do label, salve o projeto clicando em `File` -> `Save All` ou usando o atalho <kbd>Ctrl</kbd>+<kbd>S</kbd> (<kbd>Cmd</kbd>+<kbd>S</kbd> no Mac).
8. Compile seu projeto clicando em `Project` -> `Build` ou usando o atalho <kbd>Ctrl</kbd>+<kbd>B</kbd> (<kbd>Cmd</kbd>+<kbd>B</kbd> no Mac).
![Hello World Step 5](images/unity/helloworld_5.png)

Você acabou de compilar seu primeiro projeto no Defold e deve ver seu texto na janela. Os conceitos de objeto de jogo e componente devem ser familiares para você. As coleções, outline, propriedades e o motivo de termos movido um pouco o label na direção superior direita são explicados abaixo.

---

## Visão geral do Defold Editor

Apresentaremos o Defold Editor aqui pela perspectiva do que um usuário de Unity talvez queira saber primeiro, mas recomendamos também conferir o [manual completo de visão geral do editor](/manuals/editor) depois.

### Comparação dos editores

A primeira diferença que você notará entre Unity e Defold é o layout padrão do Editor. Estamos mostrando um Unity Editor com um layout levemente modificado para corresponder ao layout padrão do Defold. Eles estão lado a lado para facilitar a comparação visual dos painéis principais, já que assim você deve reconhecer mais facilmente as abas do Unity.

![Editor Comparison](images/unity/defold_unity_editor.png)

Por padrão, o Defold Editor abre em uma pré-visualização 2D ortográfica. Se você vai trabalhar em um projeto 3D, ou apenas quer uma experiência mais próxima do Unity, recomendamos mudar de 2D para 3D desmarcando o alternador `2D` na barra de ferramentas e alterando a projeção da câmera para perspectiva marcando o alternador `Perspective`:

![Defold Toolbar](images/unity/defold_2d.png)

Você também pode ajustar as `Grid Settings` na barra de ferramentas para usar o plano `Y`, como no Unity:

![Defold 3D settings](images/unity/defold_3d.png)

### Visão geral dos painéis do Defold

O Defold Editor é dividido em 6 painéis principais.

![Editor 2](images/editor/editor_overview.png)

Abaixo está uma comparação da nomenclatura do Defold e das diferenças funcionais:

| Defold | Unity | Diferenças |
|---|---|---|
| 1. Assets | Project (Assets Browser) | No Defold, o painel Assets fica encaixado à esquerda. O Defold não cria arquivos `meta`. |
| 2. Main Editor | Scene View | O Defold Editor é sensível ao contexto (editores diferentes para tipos de arquivo diferentes), enquanto o Unity usa janelas especializadas separadas (por exemplo, Animator, Shader Graph). O Defold também tem um editor de código integrado. |
| 3. Outline | Hierarchy | O Defold reflete apenas o arquivo aberto no momento ou o elemento selecionado (objeto de jogo ou componente), não uma hierarquia global. |
| 4. Properties | Inspector | O Defold mostra apenas as propriedades da **seleção atual** no Outline, não de todos os componentes no objeto de jogo. |
| 5. Tools | Console | O Defold fornece ferramentas em abas como Console, Curve Editor, Build Errors, Search Results, Breakpoints e Debugger. |
| 6. Changed Files | Unity Version Control (Plastic) | No Defold, depois que o Git é integrado ao seu projeto, os arquivos alterados aparecem aqui. Você ainda pode usar Git externamente. |

Outras nomenclaturas úteis relacionadas ao Editor:

| Defold | Unity | Diferenças |
|---|---|---|
| Game Build | Game Preview | Mostra o jogo em execução compilado com a engine. O Defold pode executar várias instâncias do jogo a partir do Editor, semelhante ao Multiplayer Play Mode do Unity 6+. No Defold, o jogo sempre roda em uma janela separada, não encaixada. O Defold também pode executar o jogo em um dispositivo externo (por exemplo, um celular), semelhante ao Unity Remote. |
| Tabs | Tabs | O Defold permite edição lado a lado em dois painéis dentro da visualização Main Editor. Abas e painéis ficam encaixados dentro de uma única janela do Editor; a visibilidade dos painéis pode ser alternada (<kbd>F6</kbd>, <kbd>F7</kbd>, <kbd>F8</kbd>) e os tamanhos dos painéis podem ser ajustados. |
| Toolbar | Toolbar / Scene View Options | Apenas em versões mais novas do Unity, as ferramentas de transformação foram movidas para a Scene view, de forma semelhante ao Defold. |
| Console | Console | O Console do Defold não é destacável. Erros de build no Defold aparecem em uma aba separada `Build Errors`. |
| Build Errors | Compilation Errors in Console | Scripts Lua são interpretados, então não há erros de compilação. Porém, seu projeto é construído, e alguns erros podem aparecer durante a build. O Defold também usa um Lua Language Server para análise estática de scripts. |
| Search Results | Search / Project Search | Filtragem por tipos e rótulos não existe no Defold. |
| Curve Editor | Unity Curve Editor | O Curve Editor do Defold permite editar curvas apenas para propriedades de efeitos de partículas. |
| [Debugger](/manuals/debugging/) | Visual Studio Debugger | O depurador vem totalmente integrado ao Defold por padrão. Há uma aba adicional para rastrear, ativar e desativar breakpoints. |

---

## Conceitos principais

Se você generalizar o suficiente, os conceitos principais por trás da maioria das engines de jogos são muito parecidos. Eles existem para ajudar desenvolvedores a criar jogos com mais facilidade, como montar blocos, enquanto lidam por conta própria com tarefas complexas e relacionadas a plataforma.

### Blocos de construção

O Defold trabalha com apenas alguns blocos básicos de construção:

![Building blocks](images/unity/blocks.png)

Para mais detalhes, consulte o manual completo sobre [blocos de construção do Defold](/manuals/building-blocks/).

### Game Objects
O Defold usa **"Game Objects"**, semelhante ao Unity. Em ambas as engines, objetos de jogo são contêineres de dados com um ID, e todos têm transformações: posição, rotação e escala. Mas no Defold, a transformação é integrada em vez de ser um componente separado.

Você pode criar relações pai-filho entre objetos de jogo. No Defold, isso só pode ser feito no Editor dentro de uma "Collection" (explicada abaixo) ou dinamicamente por script. Objetos de jogo não podem conter outros objetos de jogo como objetos aninhados da mesma forma que podem no Unity.

### Components
Em ambas as engines, Game Objects podem ser estendidos com **"Components"**. O Defold fornece um conjunto mínimo de componentes essenciais. Há menos distinção entre 2D e 3D do que no Unity (por exemplo, colliders), então há menos componentes no geral, e alguns do Unity podem fazer falta.

#### Componentes de comportamento

No Unity, "component" geralmente significa um `MonoBehaviour` anexado a um `GameObject`. Você pode criar o seu herdando de `MonoBehaviour` ou usar componentes integrados, como Light, alguns itens de física e assim por diante.

No Defold, Component se refere exclusivamente ao equivalente aos componentes integrados do Unity; o Defold não trata um script como um monobehaviour e não exige nenhuma "marcação" explícita para anexá-lo a um game object, além de criar callbacks/eventos de escuta.

Comportamento personalizado de gameplay geralmente não é adicionado como muitos componentes de script separados no mesmo objeto de jogo. Em vez disso, ele costuma ser implementado em módulos Lua e usado por um `.script` hospedeiro, ou tratado por um script de sistema maior que controla muitos objetos. A seção Escrita de código abaixo cobre isso com mais detalhes.

Leia mais sobre [Componentes do Defold aqui](/manuals/components/).

A tabela abaixo apresenta componentes semelhantes do Unity para consulta rápida, com links para cada manual de componente do Defold:

| Defold | Unity | Diferenças |
|---|---|---|
| [Sprite](/manuals/sprite/) | Sprite Renderer | No Defold, você só pode alterar o tint (propriedade de cor) via código. |
| [Tilemap](/manuals/tilemap/) | Tilemap / Grid | O Defold tem um Tilemap Editor integrado que suporta grades quadradas (mas há uma extensão para, por exemplo, [Hexagon](https://github.com/selimanac/defold-hexagon/)) e não tem regras integradas de autotiling. Ferramentas como [Tiled](https://defold.com/assets/tiled/), [TileSetter](https://defold.com/assets/tilesetter/) ou [Sprite Fusion](https://defold.com/assets/spritefusion/) têm opções de exportação para Defold. |
| [Label](/manuals/label/) | Text / TextMeshPro | O Defold tem uma [extensão RichText](https://defold.com/assets/richtext/) para formatação rica (semelhante ao TextMeshPro). |
| [Sound](/manuals/sound/) | AudioSource | O Defold tem apenas uma fonte de som global (não espacial). Há uma [extensão FMOD](https://github.com/defold/extension-fmod) oficial para Defold. |
| [Factory](/manuals/factory/) | Prefab Instantiate() | No Defold, uma Factory é um componente com um protótipo específico (prefab). |
| [Collection Factory](/manuals/collection-factory/) | - (Sem equivalente direto de componente) | Um componente Collection Factory no Defold pode instanciar vários Game Objects com relações pai-filho de uma vez. |
| [Collision Object](/manuals/physics-objects) | Rigidbody + Collider | No Defold, objetos físicos e formas de colisão são combinados em um único componente. |
| [Collision Shapes](/manuals/physics-shapes/)  | BoxCollider / SphereCollider / CapsuleCollider | No Defold, formas (box, sphere, capsule) são configuradas dentro do componente Collision Object. Ambos suportam formas de colisão vindas de tilemaps e dados de casco convexo. |
| [Camera](/manuals/camera/) | Camera | No Unity, a câmera tem mais configurações integradas de renderização e pós-processamento, enquanto o Defold delega esse controle personalizado ao usuário via script de renderização. |
| [GUI](/manuals/gui/) | UI Toolkit / Unity UI / uGUI Canvas | A GUI do Defold é um componente poderoso para criar UIs completas e templates. O Unity não tem um componente único equivalente, mas sim vários frameworks de UI. O Defold também tem uma extensão para [Extension](https://github.com/britzl/extension-imgui). |
| [GUI Script](/manuals/gui-script/) | Unity UI / uGUI scripts | A GUI do Defold pode ser controlada por scripts de GUI usando a API dedicada `gui`. |
| [Model](/manuals/model/) | MeshRenderer + Material | No Defold, um componente Model reúne um arquivo de modelo 3D, texturas e um material com shaders. |
| [Mesh](/manuals/mesh/) | MeshRenderer / MeshFilter / Procedural Mesh | No Defold, Mesh é um componente para gerenciar um conjunto de vértices via código. É semelhante a um Model do Defold, mas ainda mais baixo nível. |
| [ParticleFX](/manuals/particlefx/) | Particle System | O editor de partículas do Defold suporta efeitos de partículas 2D/3D com muitas propriedades, e permite animá-las ao longo do tempo usando curvas no Curve Editor. Ele não tem Trails ou Collisions. |
| [Script](/manuals/script/) | Script | Mais detalhes sobre diferenças de programação são explicados abaixo. |

#### Extensões e componentes personalizados

O Defold também tem componentes oficiais [Spine](/extension-spine/) e [Rive](/extension-rive/) disponíveis por extensões.

Você também pode criar seus próprios [Components personalizados](https://github.com/defold/extension-simpledata) usando Native Extensions, como este [Object Interpolation Component](https://github.com/indiesoftby/defold-object-interpolation) criado pela comunidade.

Alguns componentes do Unity não têm equivalente pronto no Defold, por exemplo: Audio Listener, Light, Terrain, LineRenderer, TrailRenderer, Cloth ou Animator. Porém, toda essa funcionalidade pode ser implementada em scripts, e já existem soluções disponíveis - por exemplo, diferentes pipelines de iluminação, o componente Mesh para gerar malhas arbitrárias (incluindo terreno), ou [Hyper Trails](https://defold.com/assets/hypertrails/) para efeitos de trilha personalizáveis. O Defold também pode adicionar novos componentes integrados no futuro, como luzes.

### Resources

Alguns Components exigem **"Resources"**, semelhante ao Unity; por exemplo, sprites e modelos precisam de texturas. Alguns deles são comparados na tabela abaixo:

| Defold | Unity | Diferenças |
|---|---|---|
| [Atlas](/manuals/atlas/) | Sprite Atlas / Texture2D | O Defold também tem uma [extensão para Texture Packer](https://defold.com/extension-texturepacker/). |
| [Tile source](/manuals/tilesource/) | Tile Palette + Asset | No Defold, um tile source pode ser usado como textura para tilemaps, mas também para sprites ou partículas. |
| [Font](/manuals/font/) | Font | Usada pelo componente Label do Defold ou por nós de texto em GUI, semelhante a Text/TextMeshPro no Unity. |
| [Material](/manuals/material/) | Material | No Defold, shaders são chamados de vertex program e fragment program. |

### Collection vs Scene

No Defold, Game Objects e Components podem ser colocados em arquivos separados, como prefabs do Unity, ou definidos em um arquivo combinado de **"Collection"**.

Uma Collection no Defold é essencialmente um arquivo de texto com uma descrição estática de cena. Ela **não** é um objeto em tempo de execução. Ela apenas define quais Game Objects devem ser instanciados no jogo e como as relações pai-filho entre esses objetos devem ser estabelecidas.

#### Game Worlds

Cenas do Unity compartilham por padrão o mesmo estado global do jogo e a mesma simulação física, efetivamente o mesmo *world* (*game world*). No Defold, você tem duas opções:
1. Instanciar objetos de jogo a partir de um único arquivo de objeto de jogo por uma `Factory`, ou de um arquivo de coleção por uma `Collection Factory`, para um *world* já instanciado, como prefabs.
2. Criar um *world* de jogo separado em tempo de execução, com seus próprios objetos de jogo, mundo físico, operações da engine e namespace de endereçamento, por meio de uma coleção carregada no bootstrap ou por um componente `Collection Proxy`.

Fábricas e componentes Proxy também são explicados abaixo.
Leia mais sobre Collections no [manual Building Blocks](/manuals/building-blocks/#collections).

---

## Recursos e assets do projeto

Unity e Defold armazenam conteúdo de jogo no diretório do projeto, mas diferem em como assets são rastreados e preparados.

### Assets

O Unity mantém assets em `Assets/` e gera arquivos `.meta`. O Defold não tem arquivos meta. O projeto no Defold é apenas sua estrutura de pastas, exatamente como no disco, e o painel `Assets` sempre a espelha.

### Formatos de recurso

O Unity importa e converte assets para outros formatos nos bastidores. No Defold, você trabalha diretamente com recursos-fonte (`.png`, `.gltf`, `.wav`, `.ogg` etc.) e os atribui a `Components`.

O Unity pode usar uma única imagem como Sprite. No Defold, imagens podem ser usadas diretamente para Models/Meshes, mas Sprites/GUI/Tilemaps/Particles exigem um atlas (texturas empacotadas) ou um tilesource (tiles em grade).

A maioria dos recursos do Defold é armazenada como texto, o que é amigável para controle de versão.

### Library Cache

O Unity gera uma pasta `Library/` para assets importados. O Defold não tem esse diretório; assets são processados durante builds, com saídas em cache na pasta de build (e caches de build locais/remotos opcionais).

---

## Escrita de código

Um equivalente do Defold aos scripts `MonoBehaviour` é um componente Script, mas há algumas diferenças importantes.

### Lua

Scripts do Defold são escritos em [Lua](https://www.lua.org/), uma linguagem dinâmica e multiparadigma.

Há alguns tipos de scripts Lua: `*.script`, `*.gui_script`, `*.render_script`, `*.editor_script` e módulos `*.lua`.

### Teal

O Defold suporta o uso de transpilers que emitem código Lua, como [Teal](https://teal-language.org/) - um dialeto de Lua com tipagem estática -, mas essa funcionalidade é mais limitada e exige configuração adicional. Detalhes estão disponíveis no [repositório da extensão Teal](https://github.com/defold/extension-teal).

### Native Extensions em C++/C#

No Defold, Native Extensions podem ser escritas em várias outras linguagens: C, C++, C#, Objective-C, Java ou JS, dependendo da plataforma-alvo. Se você se sente muito confortável com C#, tecnicamente é possível estruturar a maior parte da lógica do jogo em uma extensão C# e apenas chamá-la a partir de um pequeno script Lua de bootstrap, embora isso exija conhecimento avançado de API e não seja recomendado para iniciantes.

Leia mais sobre extensões no [manual Defold Native Extensions](/manuals/extensions/).


### De MonoBehaviours para módulos Lua

O Unity tem um modelo aberto de scripts. Como `MonoBehaviour` é a principal forma de adicionar comportamento no editor, muitos projetos Unity começam com um script no estilo controlador para cada GameObject importante: `PlayerController`, `EnemyController`, `BulletController`, `GameManager`, `EnemyManager` e assim por diante.

O Defold é mais específico sobre sua arquitetura padrão. Um objeto de jogo pode ter um `.script`, mas raramente você precisa criar um script para cada Game Object, porque um único script no Defold pode controlar centenas ou milhares de outros objetos e seus componentes, mesmo que eles não tenham scripts próprios, graças ao poderoso endereçamento e passagem de mensagens do Defold. Criar scripts para corresponder a cada Game Object raramente é necessário e pode levar a uma complexidade contraproducente.

Para comportamento de gameplay reutilizável, desenvolvedores Unity frequentemente avançam para composição: scripts `MonoBehaviour` menores, como `Health.cs`, `Attack.cs` ou `EnemyFinder.cs`, anexados ao mesmo GameObject. No Defold, você geralmente mantém um `.script` anexado como host ou coordenador e coloca a lógica reutilizável em módulos Lua comuns.

No Unity, essa composição poderia ficar assim:

```text
Player
├── PlayerMovement.cs
├── PlayerAttack.cs
├── EnemyFinder.cs
└── Health.cs
```

No Defold, as mesmas responsabilidades costumam ser divididas entre um script anexado e módulos reutilizáveis:

```text
player.go
├── sprite
├── collisionobject
└── player.script

modules/
├── player_movement.lua
├── player_attack.lua
├── enemy_finder.lua
└── health.lua
```

O `.script` anexado se torna o host ou coordenador. Os módulos Lua contêm lógica reutilizável, semelhante a como pequenos scripts `MonoBehaviour` geralmente contêm uma responsabilidade no Unity.

```lua
local movement = require "modules.player_movement"
local attack = require "modules.player_attack"
local finder = require "modules.enemy_finder"
local health = require "modules.health"

function init(self)
    self.movement = movement.new(self)
    self.attack = attack.new(self)
    self.finder = finder.new(self)
    self.health = health.new(self)
end

function update(self, dt)
    self.movement:update(dt)
    self.attack:update(dt)
    self.finder:update(dt)
end

function on_message(self, message_id, message, sender)
    self.health:on_message(message_id, message, sender)
    self.attack:on_message(message_id, message, sender)
end
```

A diferença importante não é que o Defold impeça uma arquitetura modular; é onde a composição acontece e como o código de gameplay se comunica:

| Unity | Defold |
|---|---|
| Anexar vários scripts `MonoBehaviour` no Inspector | Anexar um `.script` e compor módulos Lua no código |
| Usar `GetComponent<T>()` ou campos serializados para conectar comportamentos | Armazenar instâncias de módulos em `self` e usar endereços/mensagens entre objetos |
| Cada componente pode ter seus próprios métodos de ciclo de vida | O script host encaminha `init()`, `update()`, `on_message()`, `final()` etc. |
| Muitos estilos arquiteturais são possíveis | Composição explícita em código e orientada a mensagens é a prática comum |

Isso pode parecer estranho no começo, especialmente se você está acostumado a configurar comportamento adicionando componentes no Inspector. No Defold, muitas coisas que você talvez configurasse visualmente no Unity podem ser criadas, conectadas, ativadas, desativadas ou atualizadas por código. O sistema de mensagens do Defold ajuda a desacoplar a lógica: o remetente posta dados para um endereço, e o receptor decide o que fazer com eles.

Essa abordagem, embora recomendada, não é imposta, e você ainda pode escrever seus scripts como quiser, inclusive anexando vários scripts por objeto de jogo ou se aproximando de um estilo de programação orientado a objetos. Também existem bibliotecas para ajudar nisso ([defold-oop](https://github.com/xiyoo0812/defold-oop) ou [lua-class](https://github.com/d954mas/lua-class)).

Para muitos objetos do mesmo tipo, como projéteis, inimigos, partículas, tiles ou elementos interativos simples, muitas vezes é melhor controlá-los a partir de um script de sistema ou gerenciador em vez de dar a cada objeto um script separado. Use scripts por objeto quando um objeto tiver seu próprio estado e comportamento significativos. Use módulos quando quiser lógica reutilizável. Use scripts de sistema quando um script puder controlar muitos objetos de forma eficiente.

Um exemplo mostrando como usar propriedades de script do Defold, factories, endereçamento e mensagens para controlar várias unidades pode ser encontrado [aqui](https://defold.com/examples/factory/spawn_manager/).

Bons manuais sobre escrita de código:
- [Manual de Script](/manuals/script/)
- [Escrevendo código](/manuals/writing-code/)
- [Depuração](/manuals/debugging/)


### Editor de código integrado

O Defold Editor inclui um editor de código integrado com autocompletar, destaque de sintaxe, consulta rápida de documentação, linting e um depurador integrado.

![Defold Code Editor](/images/editor/code-editor.png)

### VS Code e outros editores

Você ainda pode usar seu próprio editor externo se preferir. Todos os componentes do Defold e arquivos relacionados são baseados em texto, então você pode editá-los com qualquer editor de texto, mas deve seguir a formatação e a estrutura de elementos corretas, já que eles são baseados em Protobuf.

Se você está acostumado com VS Code e quer usá-lo para escrever o código do seu jogo, recomendamos instalar [Defold Kit](https://marketplace.visualstudio.com/items?itemName=astronachos.defold) ou [Defold Buddy](https://marketplace.visualstudio.com/items?itemName=mikatuo.vscode-defold-ide) pelo Visual Studio Marketplace.

Você também pode configurar as preferências do Defold Editor para abrir arquivos de texto por padrão no VS Code (ou qualquer outro editor externo). Veja [Editor Preferences](/manuals/editor-preferences/) para detalhes.

### Shaders - GLSL

O Defold usa GLSL (OpenGL Shading Language) para shaders - `Vertex Programs` e `Fragment Programs`, semelhante ao Unity. Embora o Defold não ofereça um Shader Graph como o Unity (o que pode ser uma desvantagem), você ainda pode criar shaders equivalentes escrevendo código.

Leia mais sobre shaders no [manual de Shaders](/manuals/shader).

#### Materials

O Defold usa o conceito de `Material`, que conecta shaders `.fp` e `.vp`, samplers (texturas) e outras coisas como Vertex Attributes ou Constants.

Leia mais sobre materiais no [manual de Materials](/manuals/material).

---

## Sistema de mensagens

No Defold, objetos não mantêm referências diretas uns aos outros. Não existe `GetComponent`, não há chamadas de método entre scripts de objetos diferentes e não há acesso global à cena como no Unity.

Em vez disso, scripts se comunicam por passagem de mensagens: você envia mensagens a outros scripts em vez de chamar métodos ou acessar componentes diretamente. O que esses objetos fazem com as mensagens depende deles.

Isso pode parecer estranho no começo, mas promove baixo acoplamento e reduz interdependências rígidas.


### Enviando uma mensagem

No Unity, a comunicação geralmente se parece com isto:

```c#
var enemy = GameObject.Find("Enemy");
enemy.GetComponent<EnemyAI>().TakeDamage(10);
```

Assim, objetos podem referenciar diretamente uns aos outros e chamar métodos em outros scripts. Tudo existe em um único espaço de cena compartilhado.

No Defold, você envia uma mensagem de um script para outro script (ou outro componente):

```lua
msg.post("#my_component", "my_message", { my_name = "Defold" })
```

E pode tratar essas mensagens no script:

```lua
function on_message(self, message_id, messsage)
    if message_id == hash("my_message") then
        print("Hello ", message.my_name)
    end
end
```

Ignore `#` e `hash` por enquanto; falaremos disso depois. O restante deve ser direto. Você pode enviar uma mensagem para qualquer componente (até para o mesmo script) de qualquer objeto de jogo instanciado.

#### Componentes que não são scripts

Às vezes você envia mensagens para componentes como `Sprite` ou `Collision`, por exemplo, para ativá-los ou desativá-los. Às vezes `Components` enviam mensagens para seu script, por exemplo quando uma colisão ocorre, para que você possa tratá-la. Internamente, o Defold usa o mesmo sistema de mensagens para eventos da engine e comunicação de gameplay.

O sistema de mensagens é um pouco semelhante ao SendMessage do Unity ou a sistemas de eventos, embora o endereçamento e as convenções sejam diferentes.

Você pode ler mais detalhes no [Manual de Passagem de Mensagens](/manuals/message-passing/).

### Endereçamento

Objetos e componentes no Defold são identificados por endereços, conhecidos como URLs.

Cada objeto e componente instanciado tem seu próprio endereço único, e você não precisa percorrer um grafo de cena para encontrá-los. Isso torna o endereçamento explícito e direto.

Uma URL simples no Defold pode ser assim:
```lua
"/player"
```

Isso é *conceitualmente* semelhante a:
```c#
GameObject.Find("player")
```

Agora é hora de explicar por que `"/"` ou `"#"` foram usados nos endereços.

Uma URL Defold (semelhante a [URL](https://en.wikipedia.org/wiki/URL)) consiste em três partes:

```yaml
socket: /path #fragment
```

ou, descrito com a nomenclatura do Defold:

```yaml
collection: /gameobject #component 
```
Os espaços nas descrições acima foram adicionados apenas para separar visualmente essas 3 partes.

Em termos simples:
1. `collection:` identifica o contexto de coleção, com `:` no fim.
2. `/path` identifica o Game Object, com `/` antes do ID.
3. `#fragment` identifica o componente específico nesse objeto (como script, sprite ou componente de colisão), com `#` antes do ID.

#### Endereço estático

Esses identificadores são determinados na criação de cada item e nunca mudam, mesmo que você altere relações pai-filho. Você pode defini-los na propriedade `Id` dos arquivos, ou obtê-los em tempo de execução por chamadas a `factory.create` ou `collectionfactory.create`, ao instanciar.

#### Endereçamento relativo

Você nem sempre precisa usar uma URL completa.

Se enviar mensagens dentro da mesma coleção (o mesmo *world*), pode omitir a parte do socket:

```yaml
/gameobject #component
```
Se estiver enviando para um componente dentro do mesmo objeto de jogo, também pode omitir a parte do objeto de jogo:

```yaml
#component
```

Dois atalhos úteis são:
- `#` para enviar a este componente *Script*
- `.` para enviar a todos os componentes neste *Game Object*

Endereçamento relativo e atalhos permitem escrever URLs reutilizáveis em diferentes contextos e objetos de jogo sem especificar caminhos completos.

### Mensagens para GUI e render

Como o Defold separa o mundo da GUI do mundo dos Game Objects, você também pode enviar mensagens de `.scripts` de objetos de jogo para `.gui_scripts`.

Você também pode enviar mensagens para namespaces especiais do sistema usando um identificador que começa com `@`. Por exemplo, o sistema de renderização pode ser endereçado via `@render`: e você pode usar isso para controlar certos recursos integrados de renderização, como alterar a projeção no script de renderização padrão:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

Mais detalhes podem ser encontrados no [manual de Endereçamento](/manuals/addressing/).

---

## Prefabs e instâncias

O Unity pode instanciar qualquer coisa na Scene de forma estática ou dinâmica, e o Defold pode fazer o mesmo. No Unity, você pega um Prefab e chama `Instantiate(prefab)`. No Defold, há 3 componentes para instanciar conteúdo:

- `Factory` - instancia um **único Game Object** a partir de um determinado protótipo: um arquivo `*.go` (prefab).
- `Collection Factory` - instancia um **conjunto de Game Objects** com relações pai-filho a partir de um determinado protótipo: um arquivo `*.collection`.
- `Collection Proxy` - **carrega** e instancia um novo *world* a partir de um arquivo `*.collection`.

### Factory

Depois de definir um componente `Factory` com sua propriedade `Prototype` apontando para o arquivo de Game Object apropriado, instanciar é tão simples quanto chamar no código:

```lua
factory.create("#my_factory")
```

Isso usa o endereço do componente, neste caso um caminho relativo usando o identificador `"#my_factory"`.

Ele retorna o identificador da instância recém-criada, então se você precisar usá-la depois vale armazená-la em uma variável:

```lua
local new_instance_id = factory.create("#my_factory")
```

Lembre-se de que, no Defold, você não precisa criar pools de objetos manualmente - a própria engine faz pooling internamente para você.

Confira mais detalhes no [manual de Factory](/manuals/factory/).

### Collection Factory

A diferença entre os componentes `Factory` e `Collection Factory` é que Collection Factory pode instanciar **vários** objetos de jogo de uma só vez e definir, na criação, as relações pai-filho conforme definidas no arquivo `*.collection`.

Essa distinção não existe no Unity; ele não tem um conceito dedicado que corresponda à Collection Factory do Defold. A analogia mais próxima é apenas um Prefab aninhado que contém uma hierarquia de objetos.

Ela retorna uma **tabela** com os ids de todas as instâncias criadas:

```lua
local spawned_instances = collectionfactory.create("#my_collectionfactory")
```

Confira mais detalhes no [manual de Collection Factory](/manuals/collection-factory/).

#### Propriedades personalizadas de instâncias

Ao chamar `factory.create()` ou `collectionfactory.create()`, você também pode especificar parâmetros opcionais como posição, rotação, escala e propriedades de script, para controlar exatamente como e onde a instância aparece e como ela se comporta, por exemplo:

```lua
local scale_2d = vmath.vector3(0.5, 0.5, 1.0)
factory.create("#my_factory", my_position, my_rotation, my_properties, scale_2d)
```

A ordem dos argumentos opcionais é properties seguida de scale. Use um `vector3` com Z definido explicitamente como `1.0` ao alterar somente a escala dos eixos X e Y de um objeto 2D; uma escala numérica é aplicada uniformemente aos três eixos.

#### Carregamento dinâmico

Tanto em componentes `Factory` quanto `Collection Factory`, você pode marcar um Prototype para carregamento dinâmico de recursos, de modo que seus assets pesados só sejam carregados para a memória quando necessário e descarregados quando não forem mais usados.

Confira mais detalhes no [manual de Gerenciamento de Recursos](/manuals/resource/).

### Collection Proxy

O `Collection Proxy` referencia um arquivo `*.collection` específico, mas em vez de injetar os objetos no *world atual* (como factories), ele **carrega e instancia um novo mundo de jogo**. Isso é um pouco semelhante a carregar uma cena inteira no Unity, mas com separação mais rígida.

No Unity, você poderia carregar uma cena aditiva assim:

```c#
SceneManager.LoadSceneAsync("Level2", LoadSceneMode.Additive);
```

No Defold, você carrega a nova coleção simplesmente enviando uma mensagem ao componente `Collection Proxy`:

```lua
msg.post("#myproxy", "load")
```

1. Quando você envia ao proxy uma mensagem `"load"` (ou `"async_load"` para carregamento assíncrono), a engine aloca um novo world, instancia tudo nessa coleção ali e o mantém isolado.
2. Depois de carregado, o proxy envia de volta uma mensagem `"proxy_loaded"` indicando que o world está pronto.
3. Então você normalmente envia mensagens `"init"` e `"enable"` para que os objetos nesse novo world comecem seu ciclo de vida normal.

Para se comunicar entre os worlds carregados, você precisa usar mensagens explícitas com URLs que incluam o nome do world (`collection:`, a primeira parte da URL).

Esse isolamento pode ser uma grande vantagem ao implementar transições de nível, minigames ou grandes sistemas modulares, porque evita interações não intencionais e também permite controle separado sobre o tempo de atualização, se necessário (por exemplo, para pausa ou câmera lenta).

Se você já usou várias cenas no Unity e precisou que elas se comportassem de forma independente, pense em um `Collection Proxy` como uma forma de trazer esse conceito diretamente para o Defold.

Confira mais detalhes no [manual de Collection Proxy](/manuals/collection-proxy/).

---

## Ciclo de vida da aplicação

Você conhece um conjunto de eventos de ciclo de vida do Unity: `Awake`, `Start`, `Update`, `FixedUpdate`, `LateUpdate`, `OnDestroy` ou `OnApplicationQuit`.

O Defold também tem um ciclo de vida da aplicação bem definido, mas os conceitos e a terminologia diferem. O Defold expõe estágios do ciclo de vida por meio de um conjunto de callbacks Lua predefinidos, chamados pela engine durante a inicialização, a cada frame e na finalização.

Aqui está uma comparação:

| Defold | Unity | Comentário |
|-|-|-|
| `init()` | `Awake()` / `Start()` / `OnEnable()`| O Defold tem um único ponto de entrada e callback de inicialização - init(). Ele é chamado em cada componente quando ele é criado. |
| `on_input` | Input Methods | O Defold recebe entradas quando o [foco de entrada é definido para o script](/manuals/input/#input-focus). Processado primeiro no loop de atualização. |
| `fixed_update()` | `FixedUpdate()` | Chamado em passo de tempo fixo. Para ativá-lo no Defold, você precisa definir `Use Fixed Timestep` - [detalhes](https://defold.com/manuals/project-settings/#use-fixed-timestep). Desde 1.12.0, ele roda antes de `update()`. |
| `update()` | `Update()` | Chamado uma vez por frame com delta time. |
| `late_update()` | `LateUpdate()` | Chamado depois de `update()`, logo antes da renderização do frame. Disponível desde 1.12.0. |
| `on_message` | Message Receiver | Callback central do Defold para receber mensagens. Processado quando há qualquer mensagem em uma fila. |
| `final` | `OnDisable` / `OnDestroy` / `OnApplicationQuit` | O Defold chama callbacks `final()` para cada componente quando seu objeto de jogo é destruído em tempo de execução (usando `go.delete()`), quando o world/coleção é descarregado e durante o encerramento da aplicação para todos os objetos restantes. |

::: sidenote
Lembre-se de que o Defold não garante nenhuma ordem de execução entre componentes quando vários são inicializados/atualizados/removidos de uma vez. Um design desacoplado é recomendado.
:::

### Inicialização

Pense no `init()` do Defold como a combinação de elementos de `Awake()`, `Start()` e `OnEnable()` do Unity em um único ponto de entrada, onde a engine já configurou tudo e você pode preparar com segurança o estado do seu componente.

### Quando as mensagens são tratadas?

Como você já pode postar mensagens em `init()`, as mensagens são despachadas primeiro logo após a inicialização.

Depois, as mensagens são tratadas após cada loop interno de processamento, sempre que há algo em uma fila. Assim, `on_message()` pode ser chamado, por exemplo, até várias vezes em um loop de atualização.

### Loop de atualização

A cada frame, o Defold passa por uma sequência de operações - tratar entrada, despachar mensagens, disparar atualizações de scripts e GUI, aplicar física, transformações e, no fim, renderizar gráficos.

### Finalização

No Defold, limpeza está sempre ligada à exclusão ou ao descarregamento do world, e seu único hook de saída por componente é `final()`.

Uma diferença sutil em relação ao modelo do Unity é que não há distinção entre um componente ser desativado e a aplicação inteira ser encerrada.

### Renderização

O script de renderização (`*.render_script`) faz parte do pipeline de renderização, que também participa do ciclo de vida com seus próprios callbacks `init()`, `update()` e `on_message()`, mas eles operam na thread de renderização e são separados da lógica de scripts de objetos de jogo e GUI.

Para mais detalhes, leia o [Manual do Ciclo de Vida da Aplicação](/manuals/application-lifecycle/).

---

## GUI

A GUI do Defold é um framework inteiro e dedicado para interfaces de usuário - menus, sobreposições, diálogos e outros elementos, semelhante ao UI Toolkit ou uGUI com Canvas.

GUI é um Component e é separada de Game Objects e Collections. Em vez de Game Objects, você trabalha com nós de GUI organizados em uma hierarquia, controlados por um script de GUI.

### Nós de GUI

Ao abrir um arquivo de componente `*.gui` no Defold, você vê um canvas onde posiciona `"GUI nodes"`. Eles são os blocos de construção da GUI. Você pode adicionar nós de GUI do tipo:

- Box (forma retangular com uma textura)
- Text (com qualquer fonte)
- Pie (elemento radial de preenchimento tipo fatia com uma textura)
- ParticleFX
- Template (outro arquivo `.gui` inteiro aninhado, como um prefab de GUI)
- e nó Spine, ao usar a extensão Spine.

### GUI Script

O componente GUI tem uma propriedade especial para scripts de GUI: você atribui um arquivo `*.gui_script` por componente, e isso permite modificar o comportamento do componente. Ele é muito semelhante a scripts comuns, exceto que não usa o namespace `go.*` (que é para scripts de objeto de jogo). Em vez disso, usa uma API especial no namespace `gui.*`, que só funciona dentro de scripts de GUI (`*.gui_script`). Você pode pensar nisso como uma Scene separada. Unity UI (uGUI) com Canvas.

### Renderização de GUI

Elementos de GUI são renderizados independentemente da câmera do jogo, normalmente em screen-space, mas esse comportamento pode ser alterado em pipelines de renderização personalizados.

Para mais detalhes, leia o [Manual de GUI](/manuals/gui/).

## Onde estão as Sorting Layers?

Esta é uma dúvida muito comum na migração a partir do Unity.

Componentes GUI têm `Layers`, e isso funciona quase da mesma forma que "Sorting Layers" no Unity. Mas para outros componentes, como `Sprites`, `Tilemaps`, `Models` etc., não há um equivalente direto.

Em vez disso, você normalmente combina:
- Ordenação fina pelo eixo Z ao usar uma câmera padrão ou profundidade ao usar um componente Camera.
- Ordenação mais ampla pelo script de renderização usando predicados de renderização - para selecionar o que desenhar por tags de material.

Mas você não deve imitar Sorting Layers do Unity com muitas tags, porque no Defold tags são um mecanismo no nível da renderização. Usá-las em excesso pode quebrar batching e aumentar o custo de draw.

---

## Para onde ir agora?

- [Exemplos do Defold](/examples)
- [Tutoriais](/tutorials)
- [Manuais](/manuals)
- [Referências de API](/ref/go)
- [FAQ](/faq/faq)

Se você tiver dúvidas ou ficar travado, o [Fórum Defold](//forum.defold.com) ou o [Discord](https://defold.com/discord/) são ótimos lugares para pedir ajuda.
