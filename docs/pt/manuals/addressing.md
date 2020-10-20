---
title: Endereçamento no Defold
brief: Esse manual explica como o Defold resolve problemas de endereçamento.
---

# Endereçamento

Um código que controla um jogo rodando tem que ser capaz de alcançar todo objeto e componente para que seja possivel a movimentaçao, a alteração na escala de tamnho, a animação e alterações no que o player vê e escuta. O mecanismo de Endereçamento do Defold torna isso possível.

## Identificadores

O Defold utiliza o Endereçamento (ou URLs, mas vamos ignorar por ora) para se referir a objetos no jogo e componentes. Esses endereçamentos consistem em identificadores. Os seguintes exemplos são sobre como o Defold usa o endereçamento. Dentro desse documento iremos examinar em detalhes como ele funciona:

```lua
local id = factory.create("#enemy_factory")
label.set_text("my_gameobject#my_label", "Hello World!")

local pos = go.get_position("my_gameobject")
go.set_position(pos, "/level/stuff/other_gameobject")

msg.post("#", "hello_there")
local id = go.get_id(".")
```

Vamos começar com um exemplo bem simples. Suponha que você tem um game object com um único sprite component. Você também tem um script component para controlar o game object. O setup no editor ficaria parecido com o exibido abaixo :

![bean in editor](images/addressing/bean_editor.png)

Agora você preccisa desabilitar o sprite quando o jogo iniciar para que ele possa aparecer tardiamente. Essa é uma tarefa facil, basta apenas colocar o seguinte código no "controller.script":

```lua
function init(self)
    msg.post("#body", "disable") -- <1>
end
```
1. Não se preocupe se não está entendendo o uso do '#'. Nos veremos ele mais adiante no documento.

Isso vai funcionar como esperado. Quando o jogo começar o script component *addresses*(Endereça) o sprite component pelo sseu identificador "body" e o utiliza esse Endereço para enviar uma *message*(Mensagem) com o "disable". O efeito dessa mensagem especial da engine é que o sprite component esconde o sprite graphics Schematically, o setup fica assim:

![bean](images/addressing/bean.png)

Os identificadores no setup são arbitrários. Aqui nos escolhemos dar ao game object o nome de "bean", o seu componente de sprite foi nominado "body", e o script component que controla o personagem foi nomeado "controller".

::: sidenote
Se voce não escolher um nome o editor escolherá automaticamente. Sempre que você criar um object ou component ele terá um *Id* próprio que sera automaticamente gerado.

- Game objects automaticamente ganham um id chamado "go" com um enumerador ("go2", "go3" etc).
- Components ganham um id de acordo como tipo de component ("sprite", "sprite2" etc).

Você pode deixar o editor designar os nomes automaticamente, entretanto nos encorajamos você a utilizar nomes descritivos.
:::

Agora vamos adicionar outro sprite component e dar ao bean um shield:

![bean](images/addressing/bean_shield_editor.png)

O novo component tem de ser identificado de forma única. se você fosse nomealo "body" o código do script seria ambiguo, assim também recebendo a mensagem de "disable" do sprite. Nesse caso selecionamos um identificador único e descritivo: "shield". Agora podemos desabilitar o "body" e "shield" sprites separadamente.

![bean](images/addressing/bean_shield.png)

::: sidenote
Se voce tentar utilizar o mesmo identificador mais de uma vez o editor indicará erro, portanto isso não será um problema:

![bean](images/addressing/name_collision.png)
:::

Agora vamos ver o que acontece se você adicionar mais de um game object. Suponha que você queira unir dois "beans" em um pequeno time. Você decide chamar um de  "bean" e o outro de  "buddy". Futuramente, quando o "bean" estiver em idle por um tempo , o programa deve fazer com que o "buddy" comece a dançar. Isso é feito enviando uma mensagem personalizada chamada  "dance" do "controller" script component em "bean" para o "controller" script no "buddy":

![bean](images/addressing/bean_buddy.png)

::: sidenote
Existem dois components chamados "controller", um em cada game object, mas isso não causa problemas uma vez que cada game object cria um new naming context.
:::

Desde que o endereçamento da mensagem está fora do game object enviando a mensagem ("bean"), o código precisa especificar qual "controller" deve receber a mensagem. Ele precisa especificar ambos, o target game id e o component id. O endereçamento completo fica `"buddy#controller"` e ele consistem em duas partes.

-  Primeiro viem o identificador do target game object ("buddy"),
-  A seguir pelo game object/component separator character ("#"),
-  E por fim você escreve o identity do target component("controller").

Voltando ao último exemplo com um único game object nos vemos que deixando o object identifier sendo parte do target address, o código pode endereçar components no *current game object*.

Por exemplo, `"#body"` demonstra o endereço do component "body" no atual game object. Isso é muito útil porque o código ira funcionar em *any*(qualquer) game object, enquanto existir um component "body" presente.

## Collections

As coleções possibilitam a criação de grupos, ou hierarquias, de game objects ou reutiliza-los controladamente. Você utiliza arquivos de coleção como templates (ou "prototypes" ou "prefabs") no editor quando voce popula o seu game.

Suponha que voce deseje criar um número maior de times de  bean/buddy. A melhor maneira de fazer isso é criando um template em um novo *collection file* (coloque o nome de  "team.collection"). Crie o game objects no arquivo de collection e o salve. Depois disso coloque uma instancia desse collection file's contents no seu main bootstrap collection e dê a instancia um identificador (chame-o de "team_1"):

![bean](images/addressing/team_editor.png)

Com essa estrutura o "bean" ainda pode se referir ao "controller" component no "buddy" pelo endereço `"buddy#controller"`.

![bean](images/addressing/collection_team.png)

E se você adicionar um segunda instancia de "team.collection" (chame-o de "team_2"), o código rodando dentro do "team_2" script components vai funcionar como esperado. O "bean" game object instance da collection "team_2" ainda pode endereçar o "controller" component no "buddy" pelo endereço `"buddy#controller"`.

![bean](images/addressing/teams_editor.png)

## Relative addressing

O endereçamento `"buddy#controller"` funciona para game objects nas duas collections porque é um endereço *relative*(relativo). Cada uma das coleções "team_1" e "team_2" cria um novo contexto de nomeamento, ou "namespace" se voce preferir. Defold evita colisãp de nomes :levando em conta o naming context de uma collection para o endereçamento:

![relative id](images/addressing/relative_same.png)

- Com o contexto de nomeamento "team_1", o game objects "bean" e o "buddy" sçao identificaod unicamente.
- Similarmente, com o name context do  "team_2", os game objects "bean" e "buddy" também são unicamente identificados.

O endereçamento relativo funciona de forma que automaticamente prevê o atual naming context quando esta resolvendo o target adress. Isso novamente vem a ser funcional e importante, sendo que você pode criar grupos de game objects com código e reutiliza-los de forma eficiente.

### Shorthands

Defold proporciona two handy shorthands que te possibilita enviar messagens sem especificar uma URL completa:

:[Shorthands](../shared/url-shorthands.md)

## Game object paths

Para entendermos o naming mechanism vamos ver o que acontece quando você cria e roda um projeto:

1. O edito lê o bootstrap collection ("main.collection") e adiciona todo seu conteudo (game objects  e outras collections).
2. Para cada objeto estático, o compilador cria um identificador. Esses são criados como "paths" começando na bootstrap root, até a hierarquia da collection até o object. um '/' character é adicionado em cada level.

Para o exemplo acima, o jogo ira rodar com os 4 game objects seguintes:

- /team_1/bean
- /team_1/buddy
- /team_2/bean
- /team_2/buddy

::: sidenote
Os identificadores são guardados como um valor de tamanho fixo. O runtime também guarda o hash state para cada collection identificada, que por sua vez é utilizada para continuar o processo de relative hashing de uma string para um id absoluto.
:::

No runtime, o agrupamento da collection não existe. Não se pode identificar de qual collection um game object especifico pertencia antes da compilação. Também não é possivel manipular todos os objects de uma collections de uma vez. Se você precisar realizar essas operações você pode tentar achar no código. Cada id de object é estático, e é garantido ele se manter fixo durante a existência do object. Isso signigica que você pode de maneira segura guardar o identificador de um object e utiliza-lo tardiamente.

## Absolute addressing

É possivel utilizar os full identifiers descritos acima ao endereçar. Na maioria dos casos o relative adressing é preferido por permitir a reutilização do conteudo, mas existem casos em que o absolutely adressing é necessário.

Por exemplo, supondo que voce queira um AI mananger que siga o estado de cada bean object. Você quer que os beans reportem a sua atividade ao mananger, e o manager toma as decisões táticas e e da ordens aos beans baseado em seus status atuais. Faria total sentido em criar um single manager game object com um  script component e coloca-lo junto a team collections no bootstrap collection.

![manager object](images/addressing/manager_editor.png)

Cada bean é responsavel por enviar o seu status ao mananger: "contact" se encontrar um inimigo ou "ouch!" se for atingido. Para esse trabalho, o bean controller scrips utiliza absolute addressing para enviar mensagens ao component "controller" no "manager".

Qualquer endereçamento que começar com  '/' sera "resolvido" a partir da root of the game world(raiz do jogo). Isso corresponde a raiz do *bootstrap collection* que é carregada com o início do jogo.

O absolute address do the manager script é `"/manager#controller"` e esse  absolute address vai até o componet correto idenpendentemente de onde foi utilizado.

![teams and manager](images/addressing/teams_manager.png)

![absolute addressing](images/addressing/absolute.png)

## Hashed identifiers

A engine guarda all identificadores como hashed values. Todas as funções que aceitam como argumento componets or game objects aceitam também uma string, hash ou URL object. Nos vimos como usar strings para endereçamento acima.

Quando você pega o identificador de um game object, a engine vai sempre retornar um absolute path identifier que é hashed:

```lua
local my_id = go.get_id()
print(my_id) --> hash: [/path/to/the/object]

local spawned_id = factory.create("#some_factory")
print(spawned_id) --> hash: [/instance42]
```

Você pode usar um identificador no lugar de uma string id, ou construir um por conta propria. Uma hashed id corresponde ao path(caminho) ao object, i.e. um absolute address:

::: sidenote
A rasão para  os relative adresses terem de ser dados como strings é porque a engine vai computar um novo hash id baseado no hash state do atual naming context (collection) com a string adicionada ao hash.
:::

```lua
local spawned_id = factory.create("#some_factory")
local pos = vmath.vector3(100, 100, 0)
go.set_position(pos, spawned_id)

local other_id = hash("/path/to/the/object")
go.set_position(pos, other_id)

-- This will not work! Relative addresses must be given as strings.
local relative_id = hash("my_object")
go.set_position(pos, relative_id)
```

## URLs

Para completar a figura, vamo olhar para o formato completo do endereçamento do Defold: the URL.

Uma URL é um object, geralmente escritos como specially formatted strings, ou strings com formatação especial. Uma URL  genérica consistem em tres partes:

`[socket:][path][#fragment]`

socket
: Identifica o mundo do jogo do target. Isso é importante quando trabalhando com o [Collection Proxies](/manuals/collection-proxy) e então é utilizado para identificar o  _dynamically loaded collection_.

path
: Essa parte da URL contem o full id do target game object.

fragment
:  A identidade do target component com o specified game object.

Assim como vimos acima, você pode deixar de fora parte, ou grande maioria das informações na maioria dos casos. Você quase nunca precisa especificar o socket, e você frequentemente, mas nem sempre, precisa especificar o path. Nesses casos em que você precisa endereçar coisas em um outro mundo do game, você necessitará especificar a parte do socket na URL. Na instancia, a URL string completa para o "controller" script no "manager" game object acima é:

`"main:/manager#controller"`

e o buddy controller in team_2 é:

`"main:/team_2/buddy#controller"`

Nos podemos enviar mensagens para eles:

```lua
-- Send "hello" to the manager script and team buddy bean
msg.post("main:/manager#controller", "hello_manager")
msg.post("main:/team_2/buddy#controller", "hello_buddy")
```

## Constructing URL objects

URL objects também podem ser construidos em forma de programação em código Lua:

```lua
-- Construct URL object from a string:
local my_url = msg.url("main:/manager#controller")
print(my_url) --> url: [main:/manager#controller]
print(my_url.socket) --> 786443 (internal numeric value)
print(my_url.path) --> hash: [/manager]
print(my_url.fragment) --> hash: [controller]

-- Construct URL from parameters:
local my_url = msg.url("main", "/manager", "controller")
print(my_url) --> url: [main:/manager#controller]

-- Build from empty URL object:
local my_url = msg.url()
my_url.socket = "main" -- specify by valid name
my_url.path = hash("/manager") -- specify as string or hash
my_url.fragment = "controller" -- specify as string or hash

-- Post to target specified by URL
msg.post(my_url, "hello_manager!")
```
