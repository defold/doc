---
title: Entrada de dispositivos no Defold
brief: Este manual explica como a entrada funciona, como capturar ações de entrada e criar reações interativas em scripts.
---

# Entrada

Toda entrada do usuário é capturada pela engine e despachada como ações para componentes de script e scripts de GUI em objetos de jogo que adquiriram foco de entrada e implementam a função `on_input()`. Este manual explica como configurar mapeamentos para capturar entrada e como criar código que responde a ela.

O sistema de entrada usa um conjunto de conceitos simples e poderosos, permitindo que você gerencie a entrada da forma mais adequada para o seu jogo.

![Input bindings](images/input/overview.png)

Dispositivos
: Dispositivos de entrada que fazem parte do seu computador ou dispositivo móvel, ou que estão conectados a ele, fornecem entrada bruta em nível de sistema para o runtime do Defold. Os seguintes tipos de dispositivo têm suporte:

  1. Teclado (tecla única e entrada de texto)
  2. Mouse (posição, cliques de botão e ações da roda do mouse)
  3. Toque único e multitoque (em dispositivos iOS e Android e HTML5 em mobile)
  4. Gamepads (conforme suportados pelo sistema operacional e mapeados no arquivo [gamepads](#gamepads-settings-file))

Mapeamentos de entrada
: Antes que a entrada seja enviada para um script, a entrada bruta do dispositivo é traduzida em *ações* significativas por meio da tabela de mapeamentos de entrada.

Ações
: Ações são identificadas pelos nomes (com hash) que você lista no arquivo de mapeamentos de entrada. Cada ação também contém dados relevantes sobre a entrada: se um botão foi pressionado ou solto, as coordenadas do mouse e do toque etc.

Listeners de entrada
: Qualquer componente de script ou script de GUI pode receber ações de entrada ao *adquirir foco de entrada*. Vários listeners podem estar ativos ao mesmo tempo.

Pilha de entrada
: A lista de listeners de entrada, com o primeiro adquirente de foco na parte inferior da pilha e o último adquirente no topo.

Consumindo entrada
: Um script pode optar por consumir a entrada recebida, impedindo que listeners mais abaixo na pilha a recebam.

## Configurando mapeamentos de entrada

Os mapeamentos de entrada são uma tabela de todo o projeto que permite especificar como a entrada de dispositivos deve ser traduzida em *ações* nomeadas antes de ser despachada para seus componentes de script e scripts de GUI. Você pode criar um novo arquivo de mapeamento de entrada: <kbd>clique com o botão direito</kbd> em um local na visualização *Conteúdo* e selecione <kbd>Novo... ▸ Mapeamento de Entrada</kbd>. Para fazer a engine usar o novo arquivo, altere a entrada *Game Binding* em *game.project*.

![Input binding setting](images/input/setting.png)

Um arquivo de mapeamento de entrada padrão é criado automaticamente com todos os novos modelos de projeto, então normalmente não há necessidade de criar um novo arquivo de mapeamento. O arquivo padrão se chama "game.input_binding" e pode ser encontrado na pasta "input" na raiz do projeto. Dê <kbd>clique duplo</kbd> no arquivo para abri-lo no editor:

![Input set bindings](images/input/input_binding.png)

Para criar um novo mapeamento, clique no botão <kbd>+</kbd> na parte inferior da seção do tipo de trigger relevante. Cada entrada tem dois campos:

*Input*
: A entrada bruta a escutar, selecionada em uma lista rolável de entradas disponíveis.

*Action*
: O nome de ação dado às ações de entrada quando elas são criadas e despachadas para seus scripts. O mesmo nome de ação pode ser atribuído a várias entradas. Por exemplo, você pode mapear a tecla <kbd>Space</kbd> e o botão "A" do gamepad para a ação `jump`. Observe que há um bug conhecido em que entradas de toque infelizmente não podem ter os mesmos nomes de ação que outras entradas.

## Tipos de trigger

Há cinco tipos de trigger específicos de dispositivo que você pode criar:

Key Triggers
: Entrada de teclado de tecla única. Cada tecla é mapeada separadamente para uma ação correspondente. Saiba mais no [manual de entrada de teclas e texto](/manuals/input-key-and-text).

Text Triggers
: Text triggers são usados para ler entrada de texto arbitrária. Saiba mais no [manual de entrada de teclas e texto](/manuals/input-key-and-text)

Mouse Triggers
: Entrada de botões do mouse e rodas de rolagem. Saiba mais no [manual de entrada de mouse e toque](/manuals/input-mouse-and-touch).

Touch Triggers
: Triggers do tipo toque único e multitoque estão disponíveis em dispositivos iOS e Android em aplicações nativas e em pacotes HTML5. Saiba mais no [manual de mouse e toque](/manuals/input-mouse-and-touch).

Gamepad Triggers
: Gamepad triggers permitem mapear entrada padrão de gamepad para funções do jogo. Saiba mais no [manual de gamepads](/manuals/input-gamepads).

### Entrada de acelerômetro

Além dos cinco tipos de trigger listados acima, o Defold também oferece suporte a entrada de acelerômetro em aplicações nativas Android e iOS. Marque a caixa Use Accelerometer na seção Input do arquivo *game.project*.

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- reagir aos dados do acelerômetro
    end
end
```

## Foco de entrada

Para escutar ações de entrada em um componente de script ou script de GUI, a mensagem `acquire_input_focus` deve ser enviada ao objeto de jogo que contém o componente:

```lua
-- diz ao objeto de jogo atual (".") para adquirir foco de entrada
msg.post(".", "acquire_input_focus")
```

Essa mensagem instrui a engine a adicionar componentes capazes de entrada (componentes de script, componentes GUI e proxies de coleção) nos objetos de jogo à *pilha de entrada*. Os componentes do objeto de jogo são colocados no topo da pilha de entrada; o componente adicionado por último ficará no topo da pilha. Observe que, se o objeto de jogo contiver mais de um componente capaz de entrada, todos os componentes serão adicionados à pilha:

![Input stack](images/input/input_stack.png)

Se um objeto de jogo que já adquiriu foco de entrada fizer isso novamente, seu(s) componente(s) serão movidos para o topo da pilha.


## Despacho de entrada e on_input()

Ações de entrada são despachadas de acordo com a pilha de entrada, do topo para a base.

![Action dispatch](images/input/actions.png)

Qualquer componente que esteja na pilha e contenha uma função `on_input()` terá essa função chamada, uma vez para cada ação de entrada durante o frame, com os seguintes argumentos:

`self`
: A instância de script atual.

`action_id`
: O nome com hash da ação, conforme configurado nos mapeamentos de entrada.

`action`
: Uma tabela contendo os dados úteis sobre a ação, como o valor da entrada, sua localização (posições absoluta e delta), se a entrada de botão foi `pressed` etc. Veja [on_input()](/ref/go#on_input) para detalhes sobre os campos de ação disponíveis.

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- mover para a esquerda
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- mover para a direita
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### Foco de entrada e componentes de proxy de coleção

Cada mundo de jogo carregado dinamicamente por meio de um proxy de coleção tem sua própria pilha de entrada. Para que o despacho de ações alcance a pilha de entrada do mundo carregado, o componente de proxy precisa estar na pilha de entrada do mundo principal. Todos os componentes na pilha de um mundo carregado são tratados antes que o despacho continue descendo pela pilha principal:

![Action dispatch to proxies](images/input/proxy.png)

::: important
É um erro comum esquecer de enviar `acquire_input_focus` ao objeto de jogo que contém o componente de proxy de coleção. Pular esta etapa impede que a entrada chegue a qualquer um dos componentes na pilha de entrada do mundo carregado.
:::


### Liberando entrada

Para parar de escutar ações de entrada, envie uma mensagem `release_input_focus` ao objeto de jogo. Essa mensagem removerá qualquer componente do objeto de jogo da pilha de entrada:

```lua
-- diz ao objeto de jogo atual (".") para liberar o foco de entrada.
msg.post(".", "release_input_focus")
```


## Consumindo entrada

O `on_input()` de um componente pode controlar ativamente se as ações devem ou não ser passadas adiante para baixo na pilha:

- Se `on_input()` retorna `false`, ou se o retorno é omitido (isso implica um retorno `nil`, que é um valor falso em Lua), as ações de entrada serão passadas ao próximo componente na pilha de entrada.
- Se `on_input()` retorna `true`, a entrada é consumida. Nenhum componente mais abaixo na pilha de entrada receberá a entrada. Observe que isso se aplica a *todas* as pilhas de entrada. Um componente na pilha de um mundo carregado por proxy pode consumir entrada, impedindo que componentes na pilha principal recebam entrada:

![consuming input](images/input/consuming.png)

Há muitos bons casos de uso em que consumir entrada fornece uma forma simples e poderosa de alternar a entrada entre diferentes partes de um jogo. Por exemplo, se você precisar de um menu popup que temporariamente seja a única parte do jogo que escuta entrada:

![consuming input](images/input/game.png)

O menu de pausa inicialmente está oculto (desativado) e, quando o jogador toca no item HUD "PAUSE", ele é ativado:

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- O jogador pressionou PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Diga ao menu de pausa para assumir.
            msg.post("pause_menu", "show")
        end
    end
end
```

![pause menu](images/input/game_paused.png)

A GUI do menu de pausa adquire foco de entrada e consome a entrada, impedindo qualquer entrada além da relevante para o menu popup:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Mostra o menu de pausa.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Adquire entrada.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- faça coisas...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Oculta o menu de pausa
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Libera entrada.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consome toda a entrada. Qualquer coisa abaixo de nós na pilha de entrada
  -- não verá a entrada até liberarmos o foco de entrada.
  return true
end
```
