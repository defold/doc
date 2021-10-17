---
title: Manual de ciclo de vida da aplicação Defold.
brief: Esse manual detalha o ciclo de vida dos games e aplicações do Defold.
---

# Ciclo de vida da aplicação

O ciclo de vida de uma aplicação ou jogo no Defold esta em uma escala simples. A engine movimenta entre três estágios de execução: inicialização, update (onde apps e jogos passam maior parte do tempo) e finalização.

![Visão geral do Ciclo de vida](images/application_lifecycle/application_lifecycle_overview.png)

Em varios casos somente um conhecimento rudimentar do funcionamento do Defold é necessário. De qualquer forma, você pode se deparar com casos em que a ordem que o Defold leva se torna vital. Esse documento descreve como a engine roda uma aplicação do início ao fim

A aplicação começa incializando tudo que é necessário para rodar a engine. Ela carrega a coleção principal e chama [`init()`](/ref/go#init) em todos os componentes carregados que têm uma função Lua `init()` (componentes de scripts e GUI com scripts de GUI). Isso permite que você customize a inicialização.

A aplicação então insere um loop de update em que a aplicação ira gastar maior parte de seu tempo de vida. Cada frame, objeto do jogo e os componentes neles contidas são atualizados. Qualquer script e script de GUI tem suas funções [`update()`](/ref/go#update) chamadas. Durante um loop de update mensagens são disparadas para seus recipientes, sons são tocados e todos os gráficos são renderizados 

Em algum ponto, o ciclo de vida da aplicação chegará a um fim. Antes da aplicação sair, a engine sai do update loop e entra na fase de finalização. Isso prepara todos objetos do jogo carregados para serem deletados. Todos componentes de objetos tem a função [`final()`](/ref/go#final) que são chamados, permitindo uma limpeza personalizada. Então os objetos são deletados e a coleção principal e descarregada. 

## Inicialização

O diagrama contem uma simplificação mais detalhada dos passos de incialização. Os passos envolvendo as "mensagens de despache" (logo antes de "spawn dynamic objects") foram colocados em um bloco separado à direita para dar maior clareza.

![Visão geral do Ciclo de vida](images/application_lifecycle/application_lifecycle_init.png)

A engine atualmente requer muito mais passos durante a inicialização, antes da coleção principal ser carregada. O perfilador de memôria, os sockets,os gráficos, os HID (dispositivos de entrada), os sons, a física e muito mais são settados. A configuração da aplicação ("game.project") também é carregada e settada.

O primeiro ponto de entrada controlavel pelo usuário, no fim da inicialização da engine, é a chamada para a função do script de renderização `init()`. 

A coleção principal é então carregada e inicializada. Todos os objetos do jogo na coleção aplicam suas transformações (tradução (mudança de posição), rotação e escala) ao seus filhos. Todas funções de componentes `init()` que existem então são chamados.

::: sidenote
A ordem em que a função do objeto componente `init()` é chamada não é específica. Você não deve assumir que a engine incializa objetos pertencentes a mesma coleção em uma certa ordem.
:::

Desde que o código do seu `init()` possa postar novas mensagens, dizer as fábricas para spawnarem novos objetos, marcar objetos para serem deletados e fazer todo tipo de coisas, a engine performa um full "post-update" em seguida. Esse pass carrega uma mensagem, que contem o objeto factory spawnando e deletando objetos. Perceba que o post-update inclui uma sequencia de "mensagens despachadas" que não somente envia mensagens que estão na fila mas também lida com mensagens enviadas para coletores proxies. Qualquer updates subsequentes nos proxies (habilitados ou desabilitados, carregando e marcado para descarregamento) são realizados durante esses pasos.

Estudando o diagrama acima revela que é possível carregar uma [coleção proxy](/manuals/collection-proxy) durante o `init()`, isso assegura que objetos contidos serão inicializados, e então descarregam a coleção pelo proxy---isso tudo antes do primeiro componente `update()` ser chamado, i.e. antes da engine deixar a fase de incialização e entrar no loop de update:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- The proxy collection is unloaded before this code is reached.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- The proxy collection objects’ init() and final() functions
        -- are called before we reach this object’s update()
    end
end
```

## O loop de update

O loop de update roda durante uma longa sequencia em cada frama. A sequência no diagrama abaixo é dividida entre sequências logicas de blocos para clareza. "Mensagens de despache" também são separados pela mesma razão:

![loop de Update](images/application_lifecycle/application_lifecycle_update.png)

## Input

Input é lido de dispositivos disponíveis, mapeados contra [binds de input](/manuals/input) e então despachados. Qualquer objeto que adquirir foco de imput pega inputs enviados para todos as funções de componentes `on_input()`. Um objeto com um componente de script e um GUI componente com um script GUI vai pegar um input para ambas funções de componentes `on_input()` ---dado que eles são definidos e tenham foco de input.

Qualquer objecto que tenha adquirido foco de input e contenha coleções proxy com componentes dispachaveis com input para componentes dentro da coleção da proxy. Esse processo continua recursivamente abaixo em coleções proxyes dentro de coleções proxies ativas.

## Update

Cada componente game object na coleção principal é atravessado. Se qualquer um desses componentes tiver um função de script `update()`, então isso será chamado. Se o componente é uma coleçaõ proxy, cada componente na coleção proxy é recursivamente atualizado com todos os passos na sequência "update" no diagrama acima. 

::: sidenote
A ordem em cada função de componende de game object `update()` não é específica. Você não deve assumir que a engine atualiza os objetos pertencentes a mesma coleção em uma certa ordem. 
:::

No próximo passo, todas as mensagens são despachadas. Desde que qualquer componenente receptor `on_message()` pode postar mensagens adicionais o dispachante de mensagens irá continuar a dispachar mensagens postadas, ate que a fila esteja vazia. Entretanto tem-se um limite a quantas rodadas na fila de mensagens podem ser rodadas pelo dispacher. Veja [Passagem de mensagem](/manuals/message-passing) e a sessão "Tópicos avançados" para maiores detalhes.

Para componentes de objeto de colisão, mensagens de physics (colisões, gatilhos, respostas ray_cast e etc) são dispachados pelo encompassing game object para todos os componentes que contêm funções de script com uma `on_message()`.

Transformações são entao finalizadas, aplicando qualquer movimento de game object, rotação e escalamento a cada componente de game object e qualquer filho componente de game object.

## Atualização de Render

O bloco de atualização render despacha mensagens ao socket `@render` (mensagens de componente de camera `set_view_projection`, `set_clear_color`, etc). O script de render `update()` é então chamado.   

## Atualização de Post

Depois das atualizações, uma atualização post é rodada. Ela descarrega da memoria coleções proxy que estão marcas para unloading (isso acontede durante a sequência de "mensagens de despache"). Qualquer game object que é marcado para deleção vai chamar todas suas funções de compontens `final()`, se tiver alguma. O código em funções `final()` geralmente postam novas mensagens na fila para que um dispacher seja rodado posteriormente. 

Qualquer componente de fabrica que foi invocado para spawnar um game object vai fazer isso depois, Finalmente game objects que estão marcados para deleção serão deletados. 

O último passo no loop de updates envolve as mensagens do dispatching `@system` (mensagens de `exit`, `reboot`, habilitando o profiler, inciando e parando capturas de vídeo, etc). Então gráficos são renderizados. Durante a renderização dos gráficos, a captura do vídeo é feita, como qualquer rendering do visual profiler (Veja em [Documentação de debugação](/manuals/debugging).)

## Frame rate e time step das coleções

O número de frases atualizadas por segundo (que iguala o número runs de loops de update por segundo) podem ser settadas nas configurações do projeto, ou programavelmente enviando uma mensagem de `set_update_frequency` ao socket do `@system`. Em adição, é possível settar o _time step_ para cada coleção de proxies individualmente enviando a mensagem `set_time_step` para o proxy. Mudando o time step da coleção não afeta a frama rate. Afeta o time step do update da física  assim como as variaveis `dt` passadas para o `update().` Também perceba que alterando o time step nao altera o número maximo de `update().` chamados por frame---é sempre um.

(Veja [Manual de coleção de proxy](/manuals/collection-proxy) e [`set_time_step`](/ref/collectionproxy#set-time-step) para detalhes)

## Finalização

Quando a aplicação sai, primeiro finaliza a última sequência de loop de update, que vai descarregar qualquer coleção proxy: finalizando e deletando todos game objects em cada coleção proxy.

Quando isso é feito a engine entra em uma sequencia de finalização que lidá a coleção principal e seus objetos:

![Finalização](images/application_lifecycle/application_lifecycle_final.png)

A função de componente `final()` são chamadas primeiramente. Subsequentemente despachando mensagens. Finalmente, todos game objects são deletados e a coleção principal é descarregada. 

A engine segue com o desligamento por tras das cenas, desligando os subsystemas: configurações de projeto é deletada, o memory profiler e desligado, e assim por diante. 

A aplicação agora está totalmente desligada.
