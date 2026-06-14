---
title: Escrevendo lógica de jogo em scripts
brief: Este manual descreve como adicionar lógica de jogo usando componentes de script.
---

# Scripts

Componentes de script permitem criar lógica de jogo usando a [linguagem de programação Lua](/manuals/lua).


## Tipos de script

Há três tipos de script Lua no Defold, cada um com diferentes bibliotecas do Defold disponíveis.

Scripts de objeto de jogo
: Extensão _.script_. Esses scripts são adicionados a objetos de jogo exatamente como qualquer outro [componente](/manuals/components), e o Defold executará o código Lua como parte das funções de ciclo de vida da engine. Scripts de objeto de jogo geralmente são usados para controlar objetos de jogo e a lógica que conecta o jogo, como carregamento de fases, regras do jogo e assim por diante. Scripts de objeto de jogo têm acesso às funções [GO](/ref/go) e a todas as funções de biblioteca do Defold, exceto às funções [GUI](/ref/gui) e [Render](/ref/render).


Scripts de GUI
: Extensão _.gui_script_. Executados por componentes GUI e geralmente contendo a lógica necessária para exibir elementos de GUI, como HUDs, menus etc. O Defold executará o código Lua como parte das funções de ciclo de vida da engine. Scripts de GUI têm acesso às funções [GUI](/ref/gui) e a todas as funções de biblioteca do Defold, exceto às funções [GO](/ref/go) e [Render](/ref/render).


Scripts de renderização
: Extensão _.render_script_. Executados pelo pipeline de renderização e contendo a lógica necessária para renderizar todos os gráficos da aplicação/jogo a cada frame. O script de renderização tem um lugar especial no ciclo de vida do seu jogo. Detalhes podem ser encontrados na [documentação do ciclo de vida da aplicação](/manuals/application-lifecycle). Scripts de renderização têm acesso às funções [Render](/ref/render) e a todas as funções de biblioteca do Defold, exceto às funções [GO](/ref/go) e [GUI](/ref/gui).


## Execução de scripts, callbacks e self

O Defold executa scripts Lua como parte do ciclo de vida da engine e expõe esse ciclo por meio de um conjunto de funções de callback predefinidas. Quando você adiciona um componente de script a um objeto de jogo, o script passa a fazer parte do ciclo de vida do objeto e de seus componentes. O script é avaliado no contexto Lua quando é carregado; depois, a engine executa as funções a seguir e passa como parâmetro uma referência para a instância atual do componente de script. Você pode usar essa referência `self` para armazenar estado na instância do componente.

::: important
`self` é um objeto `userdata` que se comporta como uma tabela Lua, mas você não pode iterar sobre ele com `pairs()` ou `ipairs()` e não pode imprimi-lo usando `pprint()`.
:::

#### `init(self)`
Chamado quando o componente é inicializado.

```lua
function init(self)
  -- Estas variáveis ficam disponíveis durante toda a vida da instância do componente
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Chamado quando o componente é excluído. Isso é útil para limpeza, por exemplo, se você criou objetos de jogo que devem ser excluídos quando o componente for excluído.

```lua
function final(self)
  if self.my_var == "something" then
      -- faça alguma limpeza
  end
end
```

#### `fixed_update(self, dt)`
Atualização independente da taxa de quadros. O parâmetro `dt` contém o delta de tempo desde a última atualização. Essa função é chamada de `0-N` vezes, dependendo do tempo do frame e da frequência de atualização fixa. Ela é chamada apenas quando `Physics`-->`Use Fixed Timestep` está ativado e `Engine`-->`Fixed Update Frequency` é maior que 0 em *game.project*. Útil quando você quer manipular objetos físicos em intervalos regulares para obter uma simulação física estável.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Chamado uma vez a cada frame após o callback `fixed_update` de todos os scripts (se Fixed Timestep estiver ativado). O parâmetro `dt` contém o delta de tempo desde o último frame.

```lua
function update(self, dt)
  self.age = self.age + dt -- aumenta a idade com o passo de tempo
end
```

#### `late_update(self, dt)`
Chamado uma vez a cada frame após o callback `update` de todos os scripts, mas pouco antes da renderização. O parâmetro `dt` contém o delta de tempo desde o último frame.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Quando mensagens são enviadas ao componente de script por meio de [`msg.post()`](/ref/msg#msg.post), a engine chama essa função no componente receptor. Saiba [mais sobre passagem de mensagens](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Se este componente tiver adquirido foco de entrada (veja [`acquire_input_focus`](/ref/go/#acquire_input_focus)), a engine chama essa função quando uma entrada é registrada. Saiba [mais sobre tratamento de entrada](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Essa função é chamada quando o script é recarregado pela função de hot reload do editor (<kbd>Edit ▸ Reload Resource</kbd>). Ela é muito útil para depuração, testes e ajustes. Saiba [mais sobre hot-reload](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- imprime a idade deste objeto de jogo
end
```


## Lógica reativa

Um objeto de jogo com um componente de script implementa alguma lógica. Muitas vezes, essa lógica depende de algum fator externo. Uma IA inimiga pode reagir ao jogador estar dentro de certo raio; uma porta pode destrancar e abrir como resultado da interação do jogador, etc.

A função `update()` permite implementar comportamentos complexos definidos como uma máquina de estados executada a cada frame - às vezes essa é a abordagem adequada. Mas há um custo associado a cada chamada de `update()`. A menos que você realmente precise da função, deve removê-la e tentar construir sua lógica de forma _reativa_. É mais barato esperar passivamente por uma mensagem que dispare uma resposta do que sondar ativamente o mundo do jogo em busca de dados aos quais responder. Além disso, resolver um problema de design de forma reativa também costuma levar a um design e uma implementação mais limpos e estáveis.

Vejamos um exemplo concreto. Suponha que você queira que um componente de script envie uma mensagem 2 segundos após ser iniciado. Ele então deve esperar por uma determinada mensagem de resposta e, depois de recebê-la, enviar outra mensagem 5 segundos depois. O código não reativo para isso ficaria mais ou menos assim:

```lua
function init(self)
    -- Contador para acompanhar o tempo.
    self.counter = 0
    -- Precisamos disso para acompanhar nosso estado.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- envia mensagem após 2 segundos
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- envia mensagem 5 segundos depois de recebermos "response"
        msg.post("another_object", "another_message")
        -- Define o estado como nil para não entrar novamente neste bloco.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- estado "first" concluído. entra no próximo
        self.state = "second"
        -- zera o contador
        self.counter = 0
    end
end
```

Mesmo nesse caso bastante simples, acabamos com uma lógica relativamente embolada. É possível melhorar isso com a ajuda de corrotinas em um módulo (veja abaixo), mas vamos tentar tornar isso reativo e usar um mecanismo de temporização integrado.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Aguarda 2s e então chama send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Aguarda 5s e então chama send_second()
		timer.delay(5, false, send_second)
	end
end
```

Isso é mais limpo e mais fácil de acompanhar. Eliminamos variáveis internas de estado que muitas vezes são difíceis de seguir pela lógica - e que podem levar a bugs sutis. Também removemos completamente a função `update()`. Isso evita que a engine chame nosso script 60 vezes por segundo, mesmo quando ele está apenas ocioso.


## Pré-processamento

É possível usar um pré-processador Lua e marcação especial para incluir código condicionalmente com base na variante da build. Exemplo:

```lua
-- Use uma das seguintes palavras-chave: RELEASE, DEBUG ou HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

O pré-processador está disponível como uma extensão de build. Saiba mais sobre como instalar e usá-lo na [página da extensão no GitHub](https://github.com/defold/extension-lua-preprocessor).


## Suporte do editor

O editor Defold suporta edição de scripts Lua com coloração de sintaxe e autocompletar. Para completar nomes de funções do Defold, pressione *Ctrl+Space* para abrir uma lista de funções correspondentes ao que você está digitando.

![Auto completion](images/script/completion.png)
