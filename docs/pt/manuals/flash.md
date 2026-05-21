---
title: Defold para usuários de Flash
brief: Este guia apresenta o Defold como uma alternativa para desenvolvedores de jogos em Flash. Ele cobre alguns dos principais conceitos usados no desenvolvimento de jogos em Flash e explica as ferramentas e métodos correspondentes no Defold.
---

# Defold para usuários de Flash

Este guia apresenta o Defold como uma alternativa para desenvolvedores de jogos em Flash. Ele cobre alguns dos principais conceitos usados no desenvolvimento de jogos em Flash e explica as ferramentas e métodos correspondentes no Defold.

## Introdução

Algumas das principais vantagens do Flash eram a acessibilidade e as baixas barreiras de entrada. Novos usuários podiam aprender o programa rapidamente e criar jogos básicos com pouco investimento de tempo. O Defold oferece uma vantagem semelhante ao fornecer um conjunto de ferramentas dedicado ao design de jogos, ao mesmo tempo em que permite que desenvolvedores avançados criem soluções avançadas para requisitos mais sofisticados (por exemplo, permitindo que desenvolvedores editem o script de renderização padrão).

Jogos em Flash são programados em ActionScript (sendo a versão 3.0 a mais recente), enquanto scripts no Defold são feitos em Lua. Este guia não fará uma comparação detalhada entre Lua e Actionscript 3.0. O [manual do Defold](/manuals/lua) fornece uma boa introdução à programação em Lua no Defold e referencia o extremamente útil [Programming in Lua](https://www.lua.org/pil/) (primeira edição), disponível gratuitamente online.

Um artigo de Jesse Warden oferece uma [comparação básica entre Actionscript e Lua](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html), que pode servir como um bom ponto de partida. Observe, porém, que há diferenças mais profundas na forma como Defold e Flash são construídos do que aquilo que é visível no nível da linguagem. Actionscript e Flash são orientados a objetos no sentido clássico, com classes e herança. O Defold não tem classes nem herança. Ele inclui o conceito de *objeto de jogo*, que pode conter representação audiovisual, comportamento e dados. Operações em objetos de jogo são feitas com *funções* disponíveis nas APIs do Defold. Além disso, o Defold incentiva o uso de *mensagens* para comunicação entre objetos. Mensagens são uma construção de nível mais alto que chamadas de método e não devem ser usadas como tal. Essas diferenças são importantes e levam algum tempo para se acostumar, mas não serão cobertas em detalhe neste guia.

Em vez disso, este guia explora alguns dos principais conceitos do desenvolvimento de jogos em Flash e mostra quais são os equivalentes mais próximos no Defold. Semelhanças e diferenças são discutidas, junto com armadilhas comuns, para ajudar você a começar bem a transição do Flash para o Defold.

## Movie clips e objetos de jogo

Movie clips são um componente essencial do desenvolvimento de jogos em Flash. Eles são símbolos, cada um contendo uma timeline única. O conceito equivalente mais próximo no Defold é um objeto de jogo.

![objeto de jogo e movieclip](images/flash/go_movieclip.png)

Ao contrário dos movie clips do Flash, objetos de jogo do Defold não têm timelines. Em vez disso, um objeto de jogo consiste em múltiplos componentes. Componentes incluem sprites, sons e scripts, entre muitos outros (para mais detalhes sobre os componentes disponíveis, veja a [documentação de blocos de construção](/manuals/building-blocks) e artigos relacionados). O objeto de jogo na captura de tela abaixo consiste em um sprite e um script. O componente de script é usado para controlar o comportamento e a aparência dos objetos de jogo ao longo do ciclo de vida do objeto:

![componente de script](images/flash/script_component.png)

Embora movie clips possam conter outros movie clips, objetos de jogo não podem *conter* objetos de jogo. No entanto, objetos de jogo podem ser tornados *filhos* de outros objetos de jogo, criando hierarquias que podem ser movidas, escaladas ou rotacionadas em conjunto.

## Flash - criando movie clips manualmente

No Flash, instâncias de movie clips podem ser adicionadas manualmente à cena ao arrastá-las da biblioteca para a timeline. Isso é ilustrado na captura de tela abaixo, em que cada logo do Flash é uma instância do movieclip "logo":

![movie clips manuais](images/flash/manual_movie_clips.png)

## Defold - criando objetos de jogo manualmente

Como mencionado anteriormente, o Defold não tem o conceito de timeline. Em vez disso, objetos de jogo são organizados em coleções. Coleções são contêineres (ou prefabs) que contêm objetos de jogo e outras coleções. No nível mais básico, um jogo pode consistir em apenas uma coleção. Com mais frequência, jogos Defold usam múltiplas coleções, adicionadas manualmente à coleção bootstrap “main” ou carregadas dinamicamente por meio de [proxies de coleção](/manuals/collection-proxy). Esse conceito de carregar "níveis" ou "telas" não tem um equivalente direto no Flash.

No exemplo abaixo, a coleção "main" contém três instâncias (listadas à direita, na janela *Outline*) do objeto de jogo "logo" (visto à esquerda, na janela do navegador *Assets*):

![objetos de jogo manuais](images/flash/manual_game_objects.png)

## Flash - referenciando movie clips criados manualmente

Referenciar movie clips criados manualmente no Flash exige o uso de um nome de instância definido manualmente:

![nome de instância no Flash](images/flash/flash_instance_name.png)

## Defold - id de objeto de jogo

No Defold, todos os objetos de jogo e componentes são referenciados por meio de um endereço. Na maioria dos casos, basta um nome simples ou um atalho. Por exemplo:

- `"."` endereça o objeto de jogo atual.
- `"#"` endereça o componente atual (o script).
- `"logo"` endereça o objeto de jogo com o id "logo".
- `"#script"` endereça o componente com id "script" no objeto de jogo atual.
- `"logo#script"` endereça o componente com id "script" no objeto de jogo com id "logo".

O endereço de objetos de jogo colocados manualmente é determinado pela propriedade *Id* atribuída (veja a parte inferior direita da captura de tela). O id precisa ser único no arquivo de coleção atual em que você está trabalhando. O editor define automaticamente um id para você, mas você pode alterá-lo para cada instância de objeto de jogo que criar.

![id de objeto de jogo](images/flash/game_object_id.png)

::: sidenote
Você pode encontrar o id de um objeto de jogo executando o seguinte código no componente de script dele: `print(go.get_id())`. Isso imprimirá o id do objeto de jogo atual no console.
:::

O modelo de endereçamento e a passagem de mensagens são conceitos fundamentais no desenvolvimento de jogos com Defold. O [manual de endereçamento](/manuals/addressing) e o [manual de passagem de mensagens](/manuals/message-passing) explicam esses conceitos em detalhes.

## Flash - criando movie clips dinamicamente

Para criar movie clips dinamicamente no Flash, primeiro é necessário configurar o ActionScript Linkage:

![actionscript linkage](images/flash/actionscript_linkage.png)

Isso cria uma classe (Logo, neste caso), que então permite instanciar novas instâncias dessa classe. Adicionar uma instância da classe Logo ao Stage poderia ser feito assim:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold - criando objetos de jogo usando fábricas

No Defold, a geração dinâmica de objetos de jogo é feita com o uso de *fábricas*. Fábricas são componentes usados para criar cópias de um objeto de jogo específico. Neste exemplo, uma fábrica foi criada com o objeto de jogo "logo" como protótipo:

![fábrica de logo](images/flash/logo_factory.png)

É importante observar que fábricas, como todos os componentes, precisam ser adicionadas a um objeto de jogo antes de poderem ser usadas. Neste exemplo, criamos um objeto de jogo chamado "factories" para conter nosso componente de fábrica:

![componente de fábrica](images/flash/factory_component.png)

A função a chamar para gerar uma instância do objeto de jogo logo é:

```lua
local logo_id = factory.create("factories#logo_factory")
```

A URL é um parâmetro obrigatório de `factory.create()`. Além disso, você pode adicionar parâmetros opcionais para definir posição, rotação, propriedades e escala. Para mais informações sobre o componente de fábrica, consulte o [manual de fábrica](/manuals/factory). Vale observar que chamar `factory.create()` retorna o id do objeto de jogo criado. Esse id pode ser armazenado para referência posterior em uma tabela (que é o equivalente Lua de um array).

## Flash - stage

No Flash, estamos familiarizados com a Timeline (seção superior da captura de tela abaixo) e o Stage (visível abaixo da Timeline):

![timeline e stage](images/flash/stage.png)

Como discutido na seção sobre movie clips acima, o Stage é essencialmente o contêiner de nível superior de um jogo em Flash e é criado sempre que um projeto é exportado. Por padrão, o Stage terá um filho, o *`MainTimeline`*. Cada movie clip gerado no projeto terá sua própria timeline e pode servir como contêiner para outros símbolos (incluindo movie clips).

## Defold - coleções

O equivalente do Defold ao Stage do Flash é uma coleção. Quando a engine inicia, ela cria um novo mundo de jogo com base no conteúdo de um arquivo de coleção. Por padrão, esse arquivo se chama "main.collection", mas você pode alterar qual coleção é carregada na inicialização acessando o arquivo de configurações *game.project*, que fica na raiz de todo projeto Defold:

![game.project](images/flash/game_project.png)

Coleções são contêineres usados no editor para organizar objetos de jogo e outras coleções. O conteúdo de uma coleção também pode ser criado via script no runtime usando uma [fábrica de coleção](/manuals/collection-factory/#spawning-a-collection), que funciona da mesma forma que uma fábrica comum de objetos de jogo. Isso é útil para criar grupos de inimigos ou um padrão de itens coletáveis, por exemplo. Na captura de tela abaixo, posicionamos manualmente duas instâncias da coleção "logos" na coleção "main".

![coleção](images/flash/collection.png)

Em alguns casos, você quer carregar um mundo de jogo completamente novo. O componente [proxy de coleção](/manuals/collection-proxy/) permite criar um novo mundo de jogo com base no conteúdo de um arquivo de coleção. Isso seria útil em cenários como carregar novos níveis de jogo, minigames ou cutscenes.

## Flash - timeline

A timeline do Flash é usada principalmente para animação, com várias técnicas frame a frame ou tweens de forma/movimento. A configuração geral de FPS (frames por segundo) do projeto define por quanto tempo um frame é exibido. Usuários avançados podem modificar o FPS geral do jogo, ou até mesmo o de movie clips individuais.

Shape tweens permitem a interpolação de gráficos vetoriais entre dois estados. Isso é útil principalmente para formas e aplicações simples, como demonstra o exemplo abaixo de um shape tween transformando um quadrado em um triângulo:

![timeline](images/flash/timeline.png)

Motion tweens permitem animar várias propriedades de um objeto, incluindo tamanho, posição e rotação. No exemplo abaixo, todas as propriedades listadas foram modificadas.

![motion tween](images/flash/tween.png)

## Defold - animação de propriedades

O Defold trabalha com imagens em pixels em vez de gráficos vetoriais, portanto não tem um equivalente para shape tweening. No entanto, motion tweening tem um equivalente poderoso em [animação de propriedades](/ref/go/#go.animate). Isso é feito via script, usando a função `go.animate()`. A função go.animate() interpola uma propriedade (como cor, escala, rotação ou posição) do valor inicial para o valor final desejado, usando uma das muitas funções de easing disponíveis (incluindo funções personalizadas). Onde o Flash exigia que o usuário implementasse funções de easing mais avançadas, o Defold inclui [muitas funções de easing](/manuals/animation/#easing) integradas à engine.

Enquanto o Flash usa keyframes de gráficos em uma timeline para animação, um dos principais métodos de animação gráfica no Defold é a animação flip-book de sequências de imagens importadas. As animações são organizadas em um componente de objeto de jogo conhecido como atlas. Neste caso, temos um atlas para um personagem de jogo com uma sequência de animação chamada "run". Ela consiste em uma série de arquivos png:

![flipbook](images/flash/flipbook.png)

## Flash - índice de profundidade

No Flash, a display list determina o que é mostrado e em que ordem. A ordenação de objetos em um contêiner (como o Stage) é tratada por um índice. Objetos adicionados a um contêiner usando o método `addChild()` ocuparão automaticamente a posição superior do índice, começando em 0 e incrementando a cada objeto adicional. Na captura de tela abaixo, geramos três instâncias do movie clip "logo":

![índice de profundidade](images/flash/depth_index.png)

As posições na display list são indicadas pelos números ao lado de cada instância de logo. Ignorando qualquer código para lidar com a posição x/y dos movie clips, o exemplo acima poderia ter sido gerado assim:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

Se um objeto é exibido acima ou abaixo de outro é determinado por suas posições relativas no índice da display list. Isso é bem ilustrado ao trocar as posições de índice de dois objetos, por exemplo:

```as
swapChildren(logo2,logo3);
```

O resultado ficaria como abaixo (com a posição de índice atualizada):

![índice de profundidade](images/flash/depth_index_2.png)

## Defold - posição z

As posições de objetos de jogo no Defold são representadas por vetores compostos por três variáveis: x, y e z. A posição z determina a profundidade de um objeto de jogo. No [script de renderização](/manuals/render) padrão, as posições z disponíveis vão de -1 a 1.

::: sidenote
Objetos de jogo com posição z fora do intervalo de -1 a 1 não serão renderizados e, portanto, não ficarão visíveis. Essa é uma armadilha comum para desenvolvedores novos no Defold e vale a pena lembrar disso se um objeto de jogo não estiver visível quando você espera que esteja.
:::

Ao contrário do Flash, em que o editor apenas sugere a indexação de profundidade (e permite modificá-la usando comandos como *Bring Forward* e *Send Backward*), o Defold permite definir diretamente a posição z dos objetos no editor. Na captura de tela abaixo, você pode ver que "logo3" é exibido por cima e tem posição z 0.2. Os outros objetos de jogo têm posições z 0.0 e 0.1.

![ordem z](images/flash/z_order.png)

Observe que a posição z de um objeto de jogo aninhado em uma ou mais coleções é decidida por sua própria posição z junto com a de todos os seus pais. Por exemplo, imagine que os objetos de jogo logo acima foram colocados em uma coleção "logos", que por sua vez foi colocada em "main" (veja a captura de tela abaixo). Se a coleção "logos" tivesse posição z 0.9, as posições z dos objetos de jogo contidos nela seriam 0.9, 1.0 e 1.1. Portanto, "logo3" não seria renderizado, pois sua posição z é maior que 1.

![ordem z](images/flash/z_order_outline.png)

A posição z de um objeto de jogo pode, é claro, ser alterada usando script. Suponha que o código abaixo esteja no componente de script de um objeto de jogo:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Detecção de colisão com `hitTestObject` e `hitTestPoint` no Flash

A detecção básica de colisão no Flash é feita usando o método `hitTestObject()`. Neste exemplo, temos dois movie clips: "bullet" e "bullseye". Eles são ilustrados na captura de tela abaixo. A caixa de limite azul fica visível ao selecionar os símbolos no editor Flash, e são essas caixas de limite que determinam o resultado do método `hitTestObject()`.

![hit test](images/flash/hittest.png)

A detecção de colisão usando `hitTestObject()` é feita assim:

```as
bullet.hitTestObject(bullseye);
```

Usar as caixas de limite neste caso não seria adequado, pois um acerto seria registrado no cenário abaixo:

![caixa de limite de hit test](images/flash/hitboundingbox.png)

Uma alternativa a `hitTestObject()` é o método `hitTestPoint()`. Esse método contém um parâmetro `shapeFlag`, que permite realizar testes de colisão contra os pixels reais de um objeto, em vez da caixa de limite. A detecção de colisão usando `hitTestPoint()` poderia ser feita assim:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Essa linha verificaria a posição x e y do projétil (canto superior esquerdo neste cenário) contra a forma do alvo. Como `hitTestPoint()` verifica um ponto contra uma forma, qual ponto (ou quais pontos!) verificar é uma consideração importante.

## Defold - objetos de colisão

O Defold inclui uma engine de física que consegue detectar colisões e permitir que um script reaja a elas. A detecção de colisão no Defold começa ao atribuir componentes de objeto de colisão a objetos de jogo. Na captura de tela abaixo, adicionamos um objeto de colisão ao objeto de jogo "bullet". O objeto de colisão é indicado como a caixa vermelha transparente (visível apenas no editor):

![objeto de colisão](images/flash/collision_object.png)

O Defold inclui uma versão modificada da engine de física Box2D, que consegue simular colisões realistas automaticamente. Este guia assume o uso de objetos de colisão cinemáticos, pois são os que mais se aproximam da detecção de colisão no Flash. Leia mais sobre objetos de colisão dinâmicos no [manual de física](/manuals/physics) do Defold.

O objeto de colisão inclui as seguintes propriedades:

![propriedades do objeto de colisão](images/flash/collision_object_properties.png)

Uma forma de caixa foi usada porque era a mais adequada para o gráfico do projétil. A outra forma usada para colisões 2D, esfera, será usada para o alvo. Definir o tipo como Kinematic significa que a resolução de colisões é feita pelo seu script, em vez da engine de física integrada (para mais informações sobre os outros tipos, consulte o [manual de física](/manuals/physics)). As propriedades group e mask determinam a qual grupo de colisão o objeto pertence e contra qual grupo de colisão ele deve ser verificado, respectivamente. A configuração atual significa que um "bullet" só pode colidir com um "target". Imagine que a configuração fosse alterada para a abaixo:

![grupo/máscara de colisão](images/flash/collision_groupmask.png)

Agora, projéteis podem colidir com alvos e outros projéteis. Para referência, configuramos um objeto de colisão para o alvo assim:

![objeto de colisão do projétil](images/flash/collision_object_bullet.png)

Observe como a propriedade *Group* está definida como "target" e *Mask* como "bullet".

No Flash, a detecção de colisão ocorre apenas quando é chamada explicitamente pelo script. No Defold, a detecção de colisão ocorre continuamente em segundo plano enquanto um objeto de colisão permanece habilitado. Quando uma colisão ocorre, mensagens são enviadas a todos os componentes de um objeto de jogo (mais relevantemente, aos componentes de script). Essas são as mensagens [collision_response and contact_point_response](/manuals/physics-messages), que contêm todas as informações necessárias para resolver a colisão como desejado.

A vantagem da detecção de colisão do Defold é que ela é mais avançada que a do Flash, com a capacidade de detectar colisões entre formas relativamente complexas com muito pouco esforço de configuração. A detecção de colisão é automática, o que significa que não é necessário percorrer os vários objetos nos diferentes grupos de colisão e executar hit tests explicitamente. A principal desvantagem é que não há equivalente ao `shapeFlag` do Flash. No entanto, para a maioria dos usos, combinações das formas básicas de caixa e esfera são suficientes. Para cenários mais complexos, formas personalizadas [são possíveis](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash - tratamento de eventos

Objetos de evento e seus listeners associados são usados para detectar vários eventos (por exemplo, cliques do mouse, pressionamentos de botão, clips sendo carregados) e disparar ações em resposta. Há uma variedade de eventos com os quais trabalhar.

## Defold - funções callback e mensagens

O equivalente do Defold ao sistema de tratamento de eventos do Flash consiste em alguns aspectos. Primeiro, cada componente de script vem com um conjunto de funções callback que detectam eventos específicos. Elas são:

init
:   Chamada quando o componente de script é inicializado. Equivalente à função construtora no Flash.

final
:   Chamada quando o componente de script é destruído (por exemplo, um objeto de jogo criado dinamicamente é removido).

update
:   Chamada a cada frame. Equivalente a `enterFrame` no Flash.

on_message
:   Chamada quando o componente de script recebe uma mensagem.

on_input
:   Chamada quando entrada do usuário (por exemplo, mouse ou teclado) é enviada a um objeto de jogo com [foco de entrada](/ref/go/#acquire_input_focus), o que significa que o objeto recebe toda a entrada e pode reagir a ela.

on_reload
:   Chamada quando o componente de script é recarregado.

As funções callback listadas acima são todas opcionais e podem ser removidas se não forem usadas. Para detalhes sobre como configurar entrada, consulte o [manual de entrada](/manuals/input). Uma armadilha comum ocorre ao trabalhar com proxies de coleção; consulte [esta seção](/manuals/input/#input-dispatch-and-on_input) do manual de entrada para mais informações.

Como discutido na seção de detecção de colisão, eventos de colisão são tratados por meio do envio de mensagens aos objetos de jogo envolvidos. Seus respectivos componentes de script recebem a mensagem em suas funções callback on_message.

## Flash - símbolos de botão

O Flash usa um tipo de símbolo dedicado para botões. Botões usam métodos específicos de tratamento de eventos (por exemplo, `click` e `buttonDown`) para executar ações quando interação do usuário é detectada. A forma gráfica de um botão na seção "Hit" do símbolo de botão determina a área de acerto do botão.

![botão](images/flash/button.png)

## Defold - cenas GUI e scripts

O Defold não inclui um componente nativo de botão, nem cliques podem ser detectados facilmente contra a forma de um determinado objeto de jogo da maneira como botões são tratados no Flash. O uso de um componente [GUI](/manuals/gui) é a solução mais comum, em parte porque as posições dos componentes GUI do Defold não são afetadas pela câmera do jogo (se usada). A API GUI também contém funções para detectar se a entrada do usuário, como cliques e eventos de toque, está dentro dos limites de um elemento GUI.

## Depuração

No Flash, o comando `trace()` é seu amigo ao depurar. O equivalente no Defold é `print()`, e é usado da mesma forma que `trace()`:

```lua
print("Hello world!"")
```

Você pode imprimir múltiplas variáveis usando uma função `print()`:

```lua
print(score, health, ammo)
```

Há também uma função `pprint()` (pretty print), que é útil ao lidar com tabelas. Essa função imprime o conteúdo de tabelas, incluindo tabelas aninhadas. Considere o script abaixo:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Ele contém uma tabela (`factions`) aninhada em uma tabela (`world`). Usar o comando `print()` comum produziria o id único da tabela, mas não seu conteúdo real:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Usar a função `pprint()` como ilustrado acima dá resultados mais significativos:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Se seu jogo usa detecção de colisão, você pode alternar a depuração de física enviando a mensagem abaixo:

```lua
msg.post("@system:", "toggle_physics_debug")
```

A depuração de física também pode ser habilitada nas configurações do projeto. Antes de alternar a depuração de física, nosso projeto ficaria assim:

![sem debug](images/flash/no_debug.png)

Alternar a depuração de física exibe os objetos de colisão adicionados aos nossos objetos de jogo:

![com debug](images/flash/with_debug.png)

Quando colisões ocorrem, os objetos de colisão relevantes se iluminam. Além disso, o vetor de colisão é exibido:

![colisão](images/flash/collision.png)

Por fim, consulte a [documentação do profiler](/ref/profiler/) para informações sobre como monitorar o uso de CPU e memória. Para mais informações sobre técnicas avançadas de depuração, consulte a [seção de depuração](/manuals/debugging) no manual do Defold.

## Para onde ir a partir daqui

- [Exemplos do Defold](/examples)
- [Tutoriais](/tutorials)
- [Manuais](/manuals)
- [Referência](/ref/go)
- [FAQ](/faq/faq)

Se você tiver dúvidas ou ficar preso, os [fóruns do Defold](//forum.defold.com) são um ótimo lugar para pedir ajuda.
