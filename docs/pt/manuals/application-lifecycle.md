---
title: Manual de ciclo de vida da aplicação Defold
brief: Este manual detalha o ciclo de vida de jogos e aplicações no Defold.
---

# Ciclo de vida da aplicação

O ciclo de vida de uma aplicação ou jogo no Defold é, em grande escala, simples. A engine passa por três estágios de execução: inicialização, loop de atualização (onde aplicativos e jogos passam a maior parte do tempo) e finalização.

::: sidenote
Este manual se refere às versões do Defold a partir da 1.12.0. Na versão 1.12.0 foram introduzidas mudanças no ciclo de vida e a nova função `late_update()`.
:::

![Lifecycle overview](images/application_lifecycle/application_lifecycle.png)

Em muitos casos, basta ter uma compreensão básica do funcionamento interno do Defold. Porém, você pode encontrar casos de borda em que a ordem exata em que o Defold executa suas tarefas se torna essencial. Este documento descreve como a engine executa uma aplicação do início ao fim.

A aplicação começa inicializando tudo o que é necessário para executar a engine. Ela carrega a coleção principal e chama [`init()`](/ref/go#init) em todos os componentes carregados que têm uma função Lua `init()` (componentes de script e componentes GUI com scripts de GUI). Isso permite que você faça uma inicialização personalizada.

Em seguida, a aplicação entra no loop de atualização, onde passará a maior parte do seu tempo de vida. A cada frame, os objetos de jogo e os componentes que eles contêm são atualizados. Todas as funções [`update()`](/ref/go#update) de scripts e scripts de GUI são chamadas. Durante o loop de atualização, mensagens são despachadas para seus destinatários, sons são reproduzidos e todos os gráficos são renderizados.

Em algum momento, o ciclo de vida da aplicação chega ao fim. Antes de encerrar, a engine sai do loop de atualização e entra em uma etapa de finalização. Ela prepara todos os objetos de jogo carregados para exclusão. As funções [`final()`](/ref/go#final) de todos os componentes dos objetos são chamadas, permitindo limpeza personalizada. Depois, os objetos são excluídos e a coleção principal é descarregada.

As etapas envolvidas na passagem ["despacho de mensagens"](#dispatching-messages) são mostradas em um diagrama separado no fim deste manual, para maior clareza, e são marcadas nos diagramas com um pequeno ícone de "envelope com uma seta" 📩.

## Inicialização

É aqui que seu jogo começa, no primeiro passo do jogo em execução. A inicialização pode ser separada em 3 fases:

![Initizalization](images/application_lifecycle/initialization.png)

### Pré-inicialização

Durante a fase `Preinitialization`, a engine executa várias etapas antes de carregar a coleção principal (bootstrap). O perfilador de memória, sockets, gráficos, HID (dispositivos de entrada), som, física e muito mais são configurados. A configuração da aplicação (*game.project*) também é carregada e configurada.

![Preinitialization](images/application_lifecycle/pre_init.png)

O primeiro ponto de entrada controlável pelo usuário, no fim da inicialização da engine, é a chamada à função `init()` do script de renderização atual.

A coleção principal é então carregada e inicializada.

### Inicialização da coleção

Durante a fase `Collection Init`, todos os objetos de jogo na coleção aplicam suas transformações: translação (mudança de posição), rotação e escala aos seus filhos. Em seguida, todas as funções `init()` de componentes existentes são chamadas.

![Collection Init](images/application_lifecycle/collection_init.png)

::: sidenote
A ordem em que as funções `init()` dos componentes de objetos de jogo são chamadas não é especificada. Você não deve assumir que a engine inicializa objetos pertencentes à mesma coleção em uma determinada ordem.
:::

### Post Update na inicialização

A engine então executa uma passagem completa de `Post Update`, a mesma que será executada depois de cada etapa de `Update Loop` mais adiante. Ela é executada no fim da inicialização porque seu código em `init()` pode postar novas mensagens, instruir fábricas a criar novos objetos, marcar objetos para exclusão e realizar outras ações.

![Post Update](images/application_lifecycle/post_init.png)

Essa passagem realiza a entrega de mensagens, a criação efetiva de objetos de jogo por fábricas e a exclusão de objetos. Observe que a passagem `Post Update` inclui uma sequência de "despacho de mensagens" que não apenas entrega mensagens enfileiradas, mas também processa mensagens enviadas a proxies de coleção. Quaisquer atualizações subsequentes de proxy (enable, disable, init, final, loading e marcação para unload) são realizadas durante essas etapas.

É totalmente possível carregar um [proxy de coleção](/manuals/collection-proxy) durante `init()`, garantir que todos os objetos contidos nele sejam inicializados e então descarregar a coleção pelo proxy, tudo isso antes que o primeiro `update()` de componente seja chamado, isto é, antes que a engine deixe a etapa de inicialização e entre no loop de atualização:

```lua
function init(self)
    print("init()")
    msg.post("#collectionproxy", "load")
end

function update(self, dt)
    -- A coleção do proxy é descarregada antes que este código seja alcançado.
    print("update()")
end

function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        print("proxy_loaded. Init, enable and then unload.")
        msg.post("#collectionproxy", "init")
        msg.post("#collectionproxy", "enable")
        msg.post("#collectionproxy", "unload")
        -- As funções init() e final() dos objetos da coleção do proxy
        -- são chamadas antes de chegarmos ao update() deste objeto
    end
end
```

## Loop de atualização

O loop de atualização executa uma sequência específica uma vez por frame. Essa sequência pode ser definida por 5 fases principais:

![Update Loop](images/application_lifecycle/update_loop.png)

1. Entrada (processamento e tratamento)
2. Atualização (incluindo atualizações Fixed, Regular, Late e de componentes da engine)
3. Atualização de renderização
4. Post Update (descarregamento de proxies de coleção, criação e exclusão de objetos de jogo)
5. Renderização do frame (os gráficos finais são renderizados)

### Fase de entrada

A entrada é lida dos dispositivos disponíveis, mapeada pelos [mapeamentos de entrada](/manuals/input) e então despachada. Qualquer objeto de jogo que tenha adquirido foco de entrada recebe entrada em todas as funções `on_input()` dos seus componentes. Um objeto de jogo com um componente de script e um componente GUI com script de GUI receberá entrada nas funções `on_input()` de ambos os componentes, desde que elas estejam definidas e que os componentes tenham adquirido foco de entrada.

![Input Phase](images/application_lifecycle/input_phase.png)

Qualquer objeto de jogo que tenha adquirido foco de entrada e contenha componentes de proxy de coleção despacha entrada para componentes dentro da coleção do proxy. Esse processo continua recursivamente por proxies de coleção habilitados dentro de proxies de coleção habilitados.

### Fase de atualização

A fase `Update` faz parte do loop de atualização. Ela começa uma vez para a coleção raiz e então é executada recursivamente para cada proxy de coleção habilitado.

Dentro de uma coleção, o Defold processa callbacks por tipo de componente: ele percorre todas as instâncias de um tipo de componente que implementa a etapa relevante, chama o callback Lua de cada instância, esvazia as mensagens e então passa para o próximo tipo de componente.

A ordem de alto nível das etapas de callback Lua de componentes de *script* é:

1. `fixed_update()` - chamada 0..N vezes por frame (se estiver usando passo de tempo fixo)
2. `update()` - chamada 1 vez por frame
3. `late_update()` - chamada 1 vez por frame

![Update Phase](images/application_lifecycle/update_phase.png)


Cada componente de objeto de jogo na coleção principal é percorrido. Se algum desses componentes tiver um script com uma função `fixed_update()`/`update()`/`late_update()`, ela será chamada. Se o componente for um proxy de coleção, cada componente na coleção do proxy é atualizado recursivamente com todas as etapas da fase `Update`.

::: sidenote
A ordem em que as funções `update()` dos componentes de objetos de jogo são chamadas não é especificada. Você não deve assumir que a engine atualiza objetos pertencentes à mesma coleção em uma determinada ordem. O mesmo vale para `fixed_update()` e `late_update()` (desde a 1.12.0).
:::

#### Física

Para componentes de objeto de colisão, mensagens de física (colisões, gatilhos, respostas de ray cast etc.) são despachadas pelo objeto de jogo que as engloba para todos os componentes que contêm um script com a função `on_message()`.

Se um [passo de tempo fixo](/manuals/physics/#physics-updates) for usado para simulação de física, também pode haver uma chamada à função `fixed_update()` em todos os componentes de script. Essa função é útil em jogos baseados em física quando você quer manipular objetos físicos em intervalos regulares para obter uma simulação física estável.

#### Transformações

Antes de **cada** atualização por tipo de componente, várias vezes durante o `Update Loop`, se necessário, as transformações são atualizadas, aplicando qualquer movimento, rotação e escala de objetos de jogo a cada componente de objeto de jogo e a qualquer componente de objeto de jogo filho.

Há uma atualização final adicional de transformações no fim do `Update Loop`, se necessário.

#### Fase de atualização da engine (sem atualizações fixas)

As tabelas abaixo descrevem as passagens de atualização no nível da *engine*. Elas omitem deliberadamente a ordem exata de prioridade interna dos componentes (que é um detalhe de implementação da engine), mas refletem as garantias de ordenação relevantes para scripting:

- `fixed_update()` roda antes de `update()`
- `late_update()` roda depois de `update()`
- mensagens postadas são esvaziadas entre atualizações por tipo de componente, e também entre as etapas de callback de script

Quando `Use Fixed Timestep` é `false` e/ou Fixed Update Frequency é `0`, no início da fase a engine prepara `dt` e então o fluxo segue como apresentado na tabela abaixo:

::: sidenote
Observe que, depois da atualização de **cada** tipo de componente, todas as mensagens são despachadas. Isso não está marcado na tabela abaixo para mantê-la limpa.
:::

| Etapa | Fase da engine | Callback Lua | Comentário |
|-|-|-|-|
| 1 | **Update** | `update()` | Chamada uma vez por frame para cada tipo de componente que implementa Update na ordem de prioridade interna. Além disso, animações de propriedades de objetos de jogo iniciadas com `go.animate()` são atualizadas aqui como um tipo de componente separado. Componentes de **física** são atualizados aqui. Para cada proxy de coleção habilitado, toda a fase `Update` é chamada recursivamente a partir da etapa 1. |
| 2 | **Late Update** | `late_update()` | Chamada uma vez por frame para cada tipo de componente que implementa Late Update na ordem de prioridade interna. |
| 3 | **Transforms** | | Uma atualização final adicional de transformações é executada no fim para cada componente, se necessário. |

#### Fase de atualização da engine com passo de tempo fixo

Quando `Use Fixed Timestep` é `true` e Fixed Update Frequency é diferente de zero, no início da fase a engine prepara `dt` (delta time), `fixed_dt` e `num_fixed_steps` (`0..N`), ou seja, quantas vezes a atualização fixa será chamada, determinado pelo tempo desde a última atualização para garantir uma quantidade fixa de atualizações.

::: sidenote
Observe que, depois da atualização de **cada** tipo de componente, todas as mensagens são despachadas. Isso não está marcado na tabela abaixo para mantê-la limpa.
:::

Então ela entra em loop:

| Etapa | Fase da engine | Callback Lua | Comentário |
|-|-|-|-|
| 1 | **Fixed Update** | `fixed_update()` | Chamada `0..N` vezes por frame, dependendo do tempo, para cada tipo de componente que implementa Fixed Update na ordem de prioridade interna. Inclui as etapas de Fixed Update dos componentes de *física*. |
| 2 | **Update** | `update()` | Chamada uma vez por frame para cada tipo de componente que implementa Update na ordem de prioridade interna. Além disso, animações de propriedades de objetos de jogo iniciadas com `go.animate()` são atualizadas aqui como um tipo de componente separado. Para cada proxy de coleção habilitado, a fase `Update` é chamada recursivamente a partir da etapa 1. |
| 3 | **Late Update** | `late_update()` | Chamada uma vez por frame para cada tipo de componente que implementa Late Update na ordem de prioridade interna. |
| 4 | **Transforms** | | Uma atualização final adicional de transformações é executada no fim para cada componente, se necessário. |

Se você precisar de mais detalhes sobre como o Defold funciona internamente durante a fase Update, vale a pena ler o próprio código [`gameobject.cpp`](https://github.com/defold/defold/blob/dev/engine/gameobject/src/gameobject/gameobject.cpp).

### Fase de atualização de renderização

O bloco de atualização de renderização primeiro despacha todas as mensagens enviadas ao socket `@render` (por exemplo, mensagens `set_view_projection` de componentes de câmera, mensagens `set_clear_color` etc.). Em seguida, o `update()` do script de renderização é chamado.

![Render Update Phase](images/application_lifecycle/render_update_phase.png)

### Fase de pós-atualização

Depois das atualizações, uma sequência de post update é executada. Ela descarrega da memória proxies de coleção marcados para descarregamento (isso acontece durante a sequência "despacho de mensagens"). Qualquer objeto de jogo marcado para exclusão chamará todas as funções `final()` dos seus componentes, se houver. O código nas funções `final()` frequentemente posta novas mensagens na fila, então a passagem "despacho de mensagens" é executada em seguida.

![Post Update Phase](images/application_lifecycle/post_update_phase.png)

Qualquer componente de fábrica que tenha recebido a instrução de criar um objeto de jogo fará isso em seguida. Por fim, objetos de jogo marcados para exclusão são de fato excluídos.

### Fase de renderização

A última etapa no loop de atualização envolve despachar mensagens de `@system` (mensagens `exit`, `reboot`, alternância do profiler, início e parada de captura de vídeo etc.).

![Render Phase](images/application_lifecycle/render_phase.png)

Depois, os gráficos são renderizados, assim como qualquer renderização do perfilador visual (veja a [documentação de depuração](/manuals/debugging)). Após a renderização dos gráficos, a captura de vídeo é feita.

#### Taxa de quadros e passo de tempo de coleções

O número de atualizações de frame por segundo (que equivale ao número de execuções do loop de atualização por segundo) pode ser definido nas configurações do projeto ou programaticamente enviando uma mensagem `set_update_frequency` ao socket `@system`. Além disso, é possível definir o _time step_ de proxies de coleção individualmente enviando uma mensagem `set_time_step` ao proxy. Alterar o time step de uma coleção não afeta a taxa de quadros. Isso afeta o passo de tempo de atualização da física, bem como a variável `dt` passada para `update().` Observe também que alterar o time step não altera o número de vezes que `update()` será chamado por frame: ele é sempre chamado exatamente uma vez.

(Consulte o [manual de proxy de coleção](/manuals/collection-proxy) e [`set_time_step`](/ref/collectionproxy#set-time-step) para detalhes)

#### Limitação de ritmo da engine

O Defold 1.12.0 introduziu uma API de limitação de ritmo da engine (`engine throttling`) que pode pular completamente atualizações da engine e renderização, ainda detectando entrada. Qualquer entrada desperta a engine novamente, e a engine pode voltar à limitação após um período de espera.

Consulte a API `sys.set_engine_throttle()` para detalhes e exemplos de uso.

## Finalização

Quando a aplicação é encerrada, primeiro ela termina a última sequência do loop de atualização, que descarregará quaisquer proxies de coleção: finalizando e excluindo todos os objetos de jogo em cada coleção de proxy.

Quando isso termina, a engine entra em uma sequência de finalização que trata a coleção principal e seus objetos:

![Finalization](images/application_lifecycle/finalization.png)

As funções `final()` de componentes são chamadas primeiro. Em seguida, ocorre um despacho de mensagens. Por fim, todos os objetos de jogo são excluídos e a coleção principal é descarregada.

A engine então prossegue com o desligamento interno dos subsistemas: a configuração do projeto é excluída, o perfilador de memória é desligado, e assim por diante.

A aplicação agora está completamente desligada.

## Despacho de mensagens {#dispatching-messages}

**Despacho de mensagens** é uma passagem especial executada depois da atualização de **cada** tipo de componente, por exemplo, atualização de sprites, atualização de scripts e qualquer outra ação que possa enviar mensagens. Durante sua execução, todas as mensagens postadas e reunidas em uma fila são despachadas. Elas são marcadas nos diagramas com pequenos ícones de "envelope com uma seta" 📩.

![Dispatch Messages](images/application_lifecycle/dispatch_messages.png)

Depois que todas as **mensagens de usuário** são despachadas chamando `on_message()` para cada componente, mensagens especiais do Defold são tratadas na seguinte ordem (também apresentada no diagrama), para cada proxy de coleção:

1. Mensagens `load` - carregam proxies de coleção marcados para carregamento e postam de volta a mensagem `proxy_loaded`.
2. Mensagens `unload` - descarregam proxies de coleção marcados para descarregamento e postam de volta a mensagem `proxy_unloaded`.
3. Mensagens `init` - acionam a fase `Collection Init` para todos os proxies de coleção que serão inicializados.
4. Mensagens `final` - acionam `final()` em todos os componentes do proxy marcado para finalização.
5. Mensagens `enable` - habilitam o proxy de coleção, então o `Update Loop` será executado para ele no próximo frame; isso aciona implicitamente `init()` para cada componente da coleção.
6. Mensagens `disable` - desabilitam o proxy de coleção, então o `Update Loop` **não** será executado para ele no próximo frame; isso interrompe completamente a execução do `Update Loop` para esse proxy.

Como o código `on_message()` de qualquer componente receptor pode postar mensagens adicionais, o despachador de mensagens continuará despachando mensagens postadas recursivamente até que a fila de mensagens esteja vazia. No entanto, há um limite para quantas passagens pela fila de mensagens o despachador realiza. Veja [cadeias de mensagens](/manuals/message-passing) para detalhes.
