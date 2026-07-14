---
title: Endereçamento no Defold
brief: Este manual explica como o Defold resolve o problema de endereçamento.
---

# Endereçamento

O código que controla um jogo em execução precisa conseguir alcançar todos os objetos e componentes para mover, escalar, animar, excluir e manipular o que o jogador vê e ouve. O mecanismo de endereçamento do Defold torna isso possível.

## Identificadores

O Defold usa endereços (ou URLs, mas vamos ignorar isso por enquanto) para se referir a objetos de jogo e componentes. Esses endereços consistem em identificadores. A seguir estão alguns exemplos de como o Defold usa endereços. Ao longo deste manual, vamos examinar em detalhes como eles funcionam:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Vamos começar com um exemplo bem simples. Suponha que você tenha um objeto de jogo com um único componente de sprite. Você também tem um componente de script para controlar o objeto de jogo. A configuração no editor ficaria mais ou menos assim:

![bean in editor](images/addressing/bean_editor.png)

Agora você quer desabilitar o sprite quando o jogo começa, para poder fazê-lo aparecer depois. Isso é fácil: basta colocar o código abaixo em "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Não se preocupe se o caractere '#' parecer confuso. Já vamos chegar nele.

Isso funcionará como esperado. Quando o jogo começa, o componente de script *endereça* o componente de sprite pelo identificador "body" e usa esse endereço para enviar a ele uma *mensagem* "disable". O efeito dessa mensagem especial da engine é fazer o componente de sprite ocultar os gráficos do sprite. De forma esquemática, a configuração fica assim:

![bean](images/addressing/bean.png)

Os identificadores na configuração são definidos pelo desenvolvedor e precisam ser únicos dentro do contexto de nomenclatura em que são usados. Aqui escolhemos dar ao objeto de jogo o identificador "bean"; seu componente de sprite foi chamado de "body"; e o componente de script que controla o personagem foi chamado de "controller". Identificadores usados em endereços URL representados por strings não devem conter `:` nem `#`, pois a sintaxe de URL reserva `:` como separador de socket e `#` como separador entre objeto de jogo e componente. Fora isso, o analisador de URLs não rejeita sinais de pontuação.

::: sidenote
Se você não escolher um nome, o editor escolherá um. Sempre que você cria um novo objeto de jogo ou componente no editor, uma propriedade *Id* única é definida automaticamente.

- Objetos de jogo recebem automaticamente um id chamado "go" com um enumerador ("go2", "go3" etc).
- Componentes recebem um id correspondente ao tipo de componente ("sprite", "sprite2" etc).

Você pode manter esses nomes atribuídos automaticamente se quiser, mas recomendamos trocar os identificadores por nomes bons e descritivos.
:::

Agora vamos adicionar outro componente de sprite e dar um escudo ao bean:

![bean](images/addressing/bean_shield_editor.png)

O novo componente precisa ser identificado de forma única dentro do objeto de jogo. Se você desse a ele o nome "body", o código do script ficaria ambíguo quanto a qual sprite deveria receber a mensagem "disable". Por isso escolhemos o identificador único (e descritivo) "shield". Agora podemos habilitar e desabilitar os sprites "body" e "shield" separadamente.

![bean](images/addressing/bean_shield.png)

::: sidenote
Se você tentar usar o mesmo identificador mais de uma vez, o editor sinalizará um erro, então isso nunca se torna um problema na prática:

![bean](images/addressing/name_collision.png)
:::

Agora vamos ver o que acontece quando você adiciona mais objetos de jogo. Suponha que você queira formar uma pequena equipe com dois "beans". Você decide chamar um dos objetos de jogo "bean" e o outro "buddy". Além disso, quando "bean" ficar ocioso por um tempo, ele deve avisar "buddy" para começar a dançar. Isso é feito enviando uma mensagem personalizada chamada "dance" do componente de script "controller" em "bean" para o script "controller" em "buddy":

![bean](images/addressing/bean_buddy.png)

::: sidenote
Há dois componentes separados chamados "controller", um em cada objeto de jogo, mas isso é perfeitamente válido, já que cada objeto de jogo cria um novo contexto de nomeação.
:::

Como o destinatário da mensagem está fora do objeto de jogo que envia a mensagem ("bean"), o código precisa especificar qual "controller" deve receber a mensagem. Ele precisa especificar tanto o id do objeto de jogo de destino quanto o id do componente. O endereço completo do componente se torna `"buddy#controller"` e consiste em duas partes separadas.

- Primeiro vem a identidade do objeto de jogo de destino ("buddy"),
- depois o caractere separador entre objeto de jogo e componente ("#"),
- e por fim a identidade do componente de destino ("controller").

Voltando ao exemplo anterior, com um único objeto de jogo, vemos que ao omitir a parte do identificador do objeto de jogo no endereço de destino, o código pode endereçar componentes no *objeto de jogo atual*.

Por exemplo, `"#body"` representa o endereço do componente "body" no objeto de jogo atual. Isso é muito útil porque esse código funcionará em *qualquer* objeto de jogo, desde que exista um componente "body" nele.

## Coleções

Coleções possibilitam criar grupos, ou hierarquias, de objetos de jogo e reutilizá-los de forma controlada. Você usa arquivos de coleção como modelos (ou "protótipos" ou "prefabs") no editor ao preencher seu jogo com conteúdo.

Suponha que você queira criar um grande número de equipes bean/buddy. Uma boa forma de fazer isso é criar um modelo em um novo *arquivo de coleção* (chame-o de "team.collection"). Monte os objetos de jogo da equipe no arquivo de coleção e salve-o. Depois, coloque uma instância do conteúdo desse arquivo de coleção na sua coleção bootstrap principal e dê um identificador à instância (chame-a de "team_1"):

![bean](images/addressing/team_editor.png)

Com essa estrutura, o objeto de jogo "bean" ainda pode se referir ao componente "controller" em "buddy" pelo endereço `"buddy#controller"`.

![bean](images/addressing/collection_team.png)

E se você adicionar uma segunda instância de "team.collection" (chame-a de "team_2"), o código em execução dentro dos componentes de script de "team_2" funcionará da mesma forma. A instância do objeto de jogo "bean" da coleção "team_2" ainda pode endereçar o componente "controller" em "buddy" pelo endereço `"buddy#controller"`.

![bean](images/addressing/teams_editor.png)

## Endereçamento relativo

O endereço `"buddy#controller"` funciona para os objetos de jogo nas duas coleções porque é um endereço *relativo*. Cada uma das coleções "team_1" e "team_2" cria um novo contexto de nomeação, ou "namespace", se preferir. O Defold evita colisões de nomes levando em conta o contexto de nomeação que uma coleção cria para o endereçamento:

![relative id](images/addressing/relative_same.png)

- Dentro do contexto de nomeação "team_1", os objetos de jogo "bean" e "buddy" são identificados de forma única.
- Da mesma forma, dentro do contexto de nomeação "team_2", os objetos de jogo "bean" e "buddy" também são identificados de forma única.

O endereçamento relativo funciona acrescentando automaticamente o contexto de nomeação atual ao resolver um endereço de destino. Isso também é extremamente útil e poderoso, porque permite criar grupos de objetos de jogo com código e reutilizá-los de forma eficiente por todo o jogo.

### Atalhos

O Defold fornece dois atalhos práticos que você pode usar para enviar mensagens sem especificar uma URL completa:

:[Shorthands](../shared/url-shorthands.md)

## Caminhos de objetos de jogo

Para entender corretamente o mecanismo de nomeação, vamos ver o que acontece quando você compila e executa o projeto:

1. O editor lê a coleção bootstrap ("main.collection") e todo o seu conteúdo (objetos de jogo e outras coleções).
2. Para cada objeto de jogo estático, o compilador cria um identificador. Eles são construídos como "paths", começando na raiz bootstrap e descendo pela hierarquia de coleções até o objeto. Um caractere '/' é adicionado em cada nível.

No exemplo acima, o jogo será executado com os seguintes 4 objetos de jogo:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
As identidades são armazenadas como valores com hash. O runtime também armazena o estado de hash de cada identidade de coleção, usado para continuar o hash de uma string relativa até chegar a um id absoluto.
:::

Em tempo de execução, o agrupamento por coleção não existe. Não há como descobrir a qual coleção um objeto de jogo específico pertencia antes da compilação. Também não é possível manipular todos os objetos de uma coleção de uma só vez. Se você precisar realizar esse tipo de operação, pode controlar isso facilmente em código. O identificador de cada objeto é estático e tem garantia de permanecer fixo durante todo o tempo de vida do objeto. Isso significa que você pode armazenar com segurança a identidade de um objeto e usá-la mais tarde.

## Endereçamento absoluto

É possível usar os identificadores completos descritos acima ao endereçar. Na maioria dos casos, o endereçamento relativo é preferível, já que permite reutilizar conteúdo, mas há casos em que o endereçamento absoluto se torna necessário.

Por exemplo, suponha que você queira um gerenciador de IA que acompanhe o estado de cada objeto bean. Você quer que os beans informem seu estado ativo ao gerenciador, e que o gerenciador tome decisões táticas e dê ordens aos beans com base nesse estado. Nesse caso, faz todo sentido criar um único objeto de jogo gerenciador com um componente de script e colocá-lo ao lado das coleções de equipes na coleção bootstrap.

![manager object](images/addressing/manager_editor.png)

Cada bean então fica responsável por enviar mensagens de estado ao gerenciador: "contact" se avistar um inimigo ou "ouch!" se for atingido e sofrer dano. Para isso funcionar, o script controlador do bean usa endereçamento absoluto para enviar mensagens ao componente "controller" em "manager".

Qualquer endereço que começa com '/' será resolvido a partir da raiz do mundo do jogo. Isso corresponde à raiz da *coleção bootstrap* carregada no início do jogo.

O endereço absoluto do script do gerenciador é `"/manager#controller"`, e esse endereço absoluto será resolvido para o componente correto independentemente de onde for usado.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Identificadores com hash

A engine armazena todos os identificadores como valores com hash. Todas as funções que recebem como argumento um componente ou um objeto de jogo aceitam também uma string, um hash ou um objeto URL. Acima, vimos como usar strings para endereçamento.

Quando você obtém o identificador de um objeto de jogo, a engine sempre retorna um identificador de caminho absoluto com hash:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Você pode usar esse tipo de identificador no lugar de um id em string, ou construir um por conta própria. Observe, porém, que um id com hash corresponde ao caminho do objeto, isto é, a um endereço absoluto:

::: sidenote
Endereços relativos precisam ser fornecidos como strings porque a engine calcula um novo id com hash com base no estado de hash do contexto de nomeação atual (coleção), adicionando a string fornecida ao hash.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- Isto não funcionará! Endereços relativos devem ser fornecidos como strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URLs

Para completar a visão geral, vamos ver o formato completo dos endereços no Defold: a URL.

Uma URL é um objeto, geralmente escrito como uma string com formatação especial. Uma URL genérica consiste em três partes:

`[socket:][path][#fragment]`

socket
: Identifica o mundo de jogo do alvo. Isso é importante ao trabalhar com [proxies de coleção](/manuals/collection-proxy), quando é usado para identificar a _coleção carregada dinamicamente_.

path
: Esta parte da URL contém o id completo do objeto de jogo de destino.

fragment
: A identidade do componente de destino dentro do objeto de jogo especificado.

Como vimos acima, você pode omitir parte, ou a maior parte, dessas informações na maioria dos casos. Quase nunca é necessário especificar o socket, e muitas vezes, mas nem sempre, é necessário especificar o path. Nos casos em que você precisa endereçar coisas em outro mundo de jogo, precisa especificar a parte de socket da URL. Por exemplo, a string de URL completa para o script "controller" no objeto de jogo "manager" acima é:

`"main:/manager#controller"`

e o controller do buddy em team_2 é:

`"main:/team_2/buddy#controller"`

Podemos enviar mensagens para eles:

```lua
-- Envia "hello" para o script do gerenciador e para o bean buddy da equipe
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Construindo objetos URL

Objetos URL também podem ser construídos programaticamente em código Lua:

```lua
-- Constrói um objeto URL a partir de uma string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (valor numérico interno)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Constrói uma URL a partir de parâmetros:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Constrói a partir de um objeto URL vazio:
local my_url = msg.url()
my_url.socket = "main" -- especifique por nome válido
my_url.path = hash("/manager") -- especifique como string ou hash
my_url.fragment = "controller" -- especifique como string ou hash

-- Envia para o alvo especificado pela URL
msg.post(my_url, "hello_manager!")
```
