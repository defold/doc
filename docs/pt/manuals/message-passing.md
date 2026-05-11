---
title: Passagem de mensagens no Defold
brief: Passagem de mensagens é o mecanismo usado pelo Defold para permitir que objetos fracamente acoplados se comuniquem. Este manual descreve esse mecanismo em profundidade.
---

# Passagem de mensagens

Passagem de mensagens é um mecanismo para objetos de jogo do Defold se comunicarem entre si. Este manual pressupõe que você tenha um entendimento básico do [mecanismo de endereçamento](/manuals/addressing) do Defold e dos [blocos básicos de construção](/manuals/building-blocks).

O Defold não usa orientação a objetos no sentido de você definir sua aplicação configurando hierarquias de classes com herança e funções de membro nos seus objetos (como Java, C++ ou C#). Em vez disso, o Defold estende Lua com um design orientado a objetos simples e poderoso, em que o estado do objeto é mantido internamente em componentes de script, acessível pela referência `self`. Além disso, objetos podem ser totalmente desacoplados por meio de passagem assíncrona de mensagens como forma de comunicação entre objetos.


## Exemplos de uso

Vamos primeiro observar alguns exemplos simples de uso. Suponha que você esteja criando um jogo composto por:

1. Uma coleção bootstrap principal contendo um objeto de jogo com um componente GUI (a GUI consiste em um minimapa e um contador de pontuação). Também há uma coleção com id "level".
2. A coleção chamada "level" contém dois objetos de jogo: um personagem herói controlado pelo jogador e um inimigo.

![Message passing structure](images/message_passing/message_passing_structure.png)

::: sidenote
O conteúdo deste exemplo vive em dois arquivos separados. Há um arquivo para a coleção bootstrap principal e outro para a coleção com o id "level". No entanto, nomes de arquivo _não importam_ no Defold. O que importa é a identidade que você atribui às instâncias.
:::

O jogo contém algumas mecânicas simples que exigem comunicação entre os objetos:

![Message passing](images/message_passing/message_passing.png)

① O herói soca o inimigo
: Como parte dessa mecânica, uma mensagem `"punch"` é enviada do componente de script "hero" para o componente de script "enemy". Como ambos os objetos vivem no mesmo lugar na hierarquia da coleção, o endereçamento relativo é preferível:

  ```lua
  -- Envia "punch" do script "hero" para o script "enemy"
  msg.post("enemy#controller", "punch")
  ```

  Há apenas um movimento de soco com força única no jogo, então a mensagem não precisa conter mais nenhuma informação além de seu nome, "punch".

  No componente de script do inimigo, você cria uma função para receber a mensagem:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  Neste caso, o código olha apenas para o nome da mensagem (enviada como uma string com hash no parâmetro `message_id`). O código não se importa com dados da mensagem nem com o remetente: *qualquer pessoa* enviando a mensagem "punch" causará dano ao pobre inimigo.

② Herói ganhando pontuação
: Sempre que o jogador derrota um inimigo, a pontuação do jogador aumenta. Uma mensagem `"update_score"` também é enviada do componente de script do objeto de jogo "hero" para o componente "gui" do objeto de jogo "interface".

  ```lua
  -- Inimigo derrotado. Aumenta o contador de pontuação em 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  Neste caso, não é possível escrever um endereço relativo, pois "interface" está na raiz da hierarquia de nomes e "hero" não. A mensagem é enviada ao componente GUI que tem um script anexado a ele, para que possa reagir à mensagem conforme necessário. Mensagens podem ser enviadas livremente entre scripts, scripts de GUI e scripts de renderização.

  A mensagem `"update_score"` é acoplada aos dados de pontuação. Os dados são passados como uma tabela Lua no parâmetro `message`:

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- define o contador de pontuação para a nova pontuação
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ Posição do inimigo no minimapa
: O jogador tem um minimapa na tela para ajudar a localizar e rastrear inimigos. Cada inimigo é responsável por sinalizar sua posição enviando uma mensagem `"update_minimap"` ao componente "gui" no objeto de jogo "interface":

  ```lua
  -- Envia a posição atual para atualizar o minimapa da interface
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  O código do script GUI precisa rastrear a posição de cada inimigo e, se o mesmo inimigo enviar uma nova posição, a antiga deve ser substituída. O remetente da mensagem (passado no parâmetro `sender`) pode ser usado como chave de uma tabela Lua com posições:

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- atualiza a posição no mapa
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- define o contador de pontuação para a nova pontuação
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- atualiza o minimapa com novas posições
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## Enviando mensagens

A mecânica de enviar uma mensagem é, como vimos acima, muito simples. Você chama a função `msg.post()`, que publica sua mensagem na fila de mensagens. Então, a cada frame, a engine percorre a fila e entrega cada mensagem ao endereço de destino. Para algumas mensagens de sistema (como `"enable"`, `"disable"`, `"set_parent"` etc.), o código da engine trata a mensagem. A engine também produz algumas mensagens de sistema (como `"collision_response"` em colisões de física) que são entregues aos seus objetos. Para mensagens de usuário enviadas a componentes de script, a engine simplesmente chama uma função Lua especial do Defold chamada `on_message()`.

Você pode enviar mensagens arbitrárias para qualquer objeto ou componente existente, e cabe ao código no lado do destinatário responder à mensagem. Se você enviar uma mensagem para um componente de script e o código do script ignorar a mensagem, tudo bem. A responsabilidade por lidar com mensagens está totalmente no lado que as recebe.

A engine verificará o endereço de destino da mensagem. Se você tentar enviar uma mensagem para um destinatário desconhecido, o Defold sinalizará um erro no console:

```lua
-- Tenta publicar em um objeto inexistente
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

A assinatura completa da chamada `msg.post()` é:

`msg.post(receiver, message_id, [message])`

receiver
: O id do componente ou objeto de jogo de destino. Observe que, se você direcionar para um objeto de jogo, a mensagem será transmitida para todos os componentes no objeto de jogo.

message_id
: Uma string ou string com hash com o nome da mensagem.

[message]
: Uma tabela Lua opcional com pares chave-valor de dados da mensagem. Quase qualquer tipo de dado pode ser incluído na tabela Lua de mensagem. Você pode passar números, strings, booleanos, URLs, hashes e tabelas aninhadas. Você não pode passar funções.

  ```lua
  -- Envia dados de tabela contendo uma tabela aninhada
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
Há um limite rígido para o tamanho da tabela do parâmetro `message`. Esse limite é de 2 kilobytes. Atualmente não há uma forma trivial de descobrir o tamanho exato de memória que uma tabela consome, mas você pode usar `collectgarbage("count")` antes e depois de inserir a tabela para monitorar o uso de memória.
:::

### Atalhos

O Defold fornece dois atalhos úteis que você pode usar para enviar mensagens sem especificar uma URL completa:

:[Shorthands](../shared/url-shorthands.md)


## Recebendo mensagens

Receber mensagens é uma questão de garantir que o componente de script de destino contenha uma função chamada `on_message()`. A função aceita quatro parâmetros:

`function on_message(self, message_id, message, sender)`

`self`
: Uma referência ao próprio componente de script.

`message_id`
: Contém o nome da mensagem. O nome tem _hash_.

`message`
: Contém os dados da mensagem. É uma tabela Lua. Se não houver dados, a tabela fica vazia.

`sender`
: Contém a URL completa do remetente.

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## Mensagens entre mundos de jogo

Se você usar um componente de proxy de coleção para carregar um novo mundo de jogo no runtime, vai querer passar mensagens entre os mundos de jogo. Suponha que você carregou uma coleção via proxy e que a propriedade *Name* da coleção esteja definida como "level":

![Collection name](images/message_passing/collection_name.png)

Assim que a coleção tiver sido carregada, inicializada e habilitada, você pode publicar mensagens para qualquer componente ou objeto no novo mundo especificando o nome do mundo de jogo no campo "socket" do endereço do destinatário:

```lua
-- Envia uma mensagem ao jogador no novo mundo de jogo
msg.post("level:/player#controller", "wake_up")
```
Uma descrição mais aprofundada sobre como proxies funcionam pode ser encontrada na documentação de [Proxies de Coleção](/manuals/collection-proxy).

## Cadeias de mensagens

Quando uma mensagem publicada é finalmente despachada, o `on_message()` dos destinatários é chamado. É bastante comum que o código de reação publique novas mensagens, que são adicionadas à fila de mensagens.

Quando a engine começa a despachar, ela percorre a fila de mensagens e chama a função `on_message()` de cada destinatário da mensagem, continuando até a fila ficar vazia. Se a passagem de despacho adicionar novas mensagens à fila, ela fará outra passagem. No entanto, há um limite rígido para quantas vezes a engine tenta esvaziar a fila, o que efetivamente coloca um limite em quão longas cadeias de mensagens você pode esperar que sejam totalmente despachadas dentro de um frame. Você pode testar facilmente quantas passagens de despacho a engine executa entre cada `update()` com o script a seguir:

```lua
function init(self)
    -- Estamos iniciando uma cadeia longa de mensagens durante o init do objeto
    -- e a mantemos em execução por várias etapas de update().
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

Executar este script imprimirá algo como:

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

Vemos que esta versão específica da engine Defold executa 10 passagens de despacho na fila de mensagens entre `init()` e a primeira chamada a `update()`. Em seguida, ela executa 75 passagens durante cada loop de atualização subsequente.
