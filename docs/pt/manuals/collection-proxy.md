---
title: Manual de proxy de coleção
brief: Este manual explica como criar dinamicamente novos mundos de jogo e alternar entre eles.
---

# Proxy de coleção

O componente de proxy de coleção é usado para carregar e descarregar dinamicamente novos "mundos" de jogo com base no conteúdo de um arquivo de coleção. Eles podem ser usados para implementar alternância entre fases do jogo, telas de GUI, carregamento e descarregamento de "cenas" narrativas ao longo de uma fase, carregamento/descarregamento de minijogos e mais.

O Defold organiza todos os objetos de jogo em coleções. Uma coleção pode conter objetos de jogo e outras coleções (isto é, subcoleções). Proxies de coleção permitem dividir seu conteúdo em coleções separadas e então gerenciar dinamicamente o carregamento e descarregamento dessas coleções por script.

Proxies de coleção diferem de [componentes de fábrica de coleção](/manuals/collection-factory/). Uma fábrica de coleção instancia o conteúdo de uma coleção no mundo de jogo atual. Proxies de coleção criam um novo mundo de jogo em runtime e, portanto, têm casos de uso diferentes.

## Criando um componente de proxy de coleção

1. Adicione um componente de proxy de coleção a um objeto de jogo usando <kbd>right-click</kbd> em um objeto de jogo e selecionando <kbd>Add Component ▸ Collection Proxy</kbd> no menu de contexto.

2. Defina a propriedade *Collection* para referenciar uma coleção que você deseja carregar dinamicamente no runtime em um momento posterior. A referência é estática e garante que todo o conteúdo da coleção referenciada acabe no jogo final.

![adicionar componente proxy](images/collection-proxy/create_proxy.png)

(Você pode excluir o conteúdo do build e baixá-lo com código em vez disso marcando a caixa *Exclude* e usando o [recurso Live Update](/manuals/live-update/).)

## Bootstrap

Quando a engine Defold inicia, ela carrega e instancia todos os objetos de jogo de uma *coleção bootstrap* no runtime. Em seguida, inicializa e ativa os objetos de jogo e seus componentes. Qual coleção bootstrap a engine deve usar é definido nas [configurações do projeto](/manuals/project-settings/#main-collection). Por convenção, esse arquivo de coleção normalmente se chama "main.collection".

![bootstrap](images/collection-proxy/bootstrap.png)

Para acomodar os objetos de jogo e seus componentes, a engine aloca a memória necessária para todo o "mundo de jogo" no qual o conteúdo da coleção bootstrap é instanciado. Um mundo de física separado também é criado para quaisquer objetos de colisão e simulação de física.

Como componentes de script precisam poder endereçar todos os objetos do jogo, mesmo de fora do mundo bootstrap, ele recebe um nome único: a propriedade *Name* que você define no arquivo de coleção:

![bootstrap](images/collection-proxy/collection_id.png)

Se a coleção carregada contiver componentes de proxy de coleção, as coleções às quais eles se referem *não* são carregadas automaticamente. Você precisa controlar o carregamento desses recursos por scripts.

## Carregando uma coleção

O carregamento dinâmico de uma coleção por proxy é feito enviando uma mensagem chamada `"load"` ao componente proxy a partir de um script:

```lua
-- Diz ao proxy "myproxy" para iniciar o carregamento.
msg.post("#myproxy", "load")
```

![carregar](images/collection-proxy/proxy_load.png)

O componente proxy instruirá a engine a alocar espaço para um novo mundo. Um mundo de física de runtime separado também é criado, e todos os objetos de jogo na coleção "`mylevel.collection`" são instanciados.

O novo mundo recebe seu nome da propriedade *Name* no arquivo de coleção; neste exemplo, ela está definida como "`mylevel`". O nome precisa ser único. Se o *Name* definido no arquivo de coleção já estiver em uso por um mundo carregado, a engine sinalizará um erro de colisão de nomes:

```txt
ERROR:GAMEOBJECT: The collection 'default' could not be created since there is already a socket with the same name.
WARNING:RESOURCE: Unable to create resource: build/default/mylevel.collectionc
ERROR:GAMESYS: The collection /mylevel.collectionc could not be loaded.
```

Quando a engine terminar de carregar a coleção, o componente de proxy de coleção enviará uma mensagem chamada `"proxy_loaded"` de volta ao script que enviou a mensagem `"load"`. O script pode então inicializar e ativar a coleção em reação à mensagem:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_loaded") then
        -- Novo mundo carregado. Inicialize e ative-o.
        msg.post(sender, "init")
        msg.post(sender, "enable")
        ...
    end
end
```

`"load"`
: Esta mensagem informa ao componente de proxy de coleção que ele deve começar a carregar sua coleção em um novo mundo. O proxy enviará de volta uma mensagem chamada `"proxy_loaded"` quando terminar.

`"async_load"`
: Esta mensagem informa ao componente de proxy de coleção que ele deve começar a carregar sua coleção em segundo plano em um novo mundo. O proxy enviará de volta uma mensagem chamada `"proxy_loaded"` quando terminar.

`"init"`
: Esta mensagem informa ao componente de proxy de coleção que todos os objetos de jogo e componentes que foram instanciados devem ser inicializados. Todas as funções `init()` de script são chamadas nesta etapa.

`"enable"`
: Esta mensagem informa ao componente de proxy de coleção que todos os objetos de jogo e componentes devem ser ativados. Todos os componentes sprite começam a desenhar quando ativados, por exemplo.

## Endereçando o novo mundo

O *Name* definido nas propriedades do arquivo de coleção é usado para endereçar objetos de jogo e componentes no mundo carregado. Se, por exemplo, você criar um objeto loader na coleção bootstrap, talvez precise se comunicar com ele a partir de qualquer coleção carregada:

```lua
-- diz ao loader para carregar a próxima fase:
msg.post("main:/loader#script", "load_level", { level_id = 2 })
```

![carregar](images/collection-proxy/message_passing.png)

E, se você precisar se comunicar com um objeto de jogo na coleção carregada a partir do loader, pode enviar uma mensagem usando a [URL completa para o objeto](/manuals/addressing/#urls):

```lua
msg.post("mylevel:/myobject", "hello")
```

::: important
Não é possível acessar diretamente objetos de jogo em uma coleção carregada a partir de fora da coleção:

```lua
local position = go.get_position("mylevel:/myobject")
-- loader.script:42: function called can only access instances within the same collection.
```
:::


## Descarregando um mundo

Para descarregar uma coleção carregada, envie mensagens correspondentes às etapas inversas do carregamento:

```lua
-- descarrega a fase
msg.post("#myproxy", "disable")
msg.post("#myproxy", "final")
msg.post("#myproxy", "unload")
```

`"disable"`
: Esta mensagem informa ao componente de proxy de coleção que ele deve desativar todos os objetos de jogo e componentes no mundo. Sprites param de ser renderizados nesta etapa.

`"final"`
: Esta mensagem informa ao componente de proxy de coleção que ele deve finalizar todos os objetos de jogo e componentes no mundo. Todas as funções `final()` dos scripts são chamadas nesta etapa.

`"unload"`
: Esta mensagem informa ao proxy de coleção que ele deve remover o mundo completamente da memória.

Se você não precisa desse controle mais granular, pode enviar a mensagem `"unload"` diretamente, sem antes desativar e finalizar a coleção. O proxy então desativará e finalizará automaticamente a coleção antes de descarregá-la.

Quando o proxy de coleção terminar de descarregar a coleção, ele enviará uma mensagem `"proxy_unloaded"` de volta ao script que enviou a mensagem `"unload"`:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("proxy_unloaded") then
        -- Ok, o mundo foi descarregado...
        ...
    end
end
```


## Passo de tempo

Atualizações de proxy de coleção podem ser escaladas alterando o _passo de tempo_. Isso significa que, embora o jogo atualize em um ritmo constante de 60 FPS, um proxy pode atualizar em um ritmo maior ou menor, afetando coisas como:

* Velocidade da simulação de física
* O `dt` passado para `update()`
* [Animações de propriedades de objetos de jogo e gui](https://defold.com/manuals/animation/#property-animation-1)
* [Animações flipbook](https://defold.com/manuals/animation/#flip-book-animation)
* [Simulações de Particle FX](https://defold.com/manuals/particlefx/)
* Velocidade de timer

Você também pode definir o modo de atualização, que permite controlar se a escala deve ser realizada discretamente (o que só faz sentido com um fator de escala abaixo de 1.0) ou continuamente.

Você controla o fator de escala e o modo de escala enviando ao proxy uma mensagem `set_time_step`:

```lua
-- atualiza o mundo carregado a um quinto da velocidade.
msg.post("#myproxy", "set_time_step", {factor = 0.2, mode = 1}
```

Para ver o que acontece ao mudar o passo de tempo, podemos criar um objeto com o seguinte código em um componente de script e colocá-lo na coleção cujo timestep estamos alterando:

```lua
function update(self, dt)
    print("update() with timestep (dt) " .. dt)
end
```

Com um passo de tempo de 0.2, obtemos o seguinte resultado no console:

```txt
INFO:DLIB: SSDP started (ssdp://192.168.0.102:54967, http://0.0.0.0:62162)
INFO:ENGINE: Defold Engine 1.2.37 (6b3ae27)
INFO:ENGINE: Loading data from: build/default
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0
DEBUG:SCRIPT: update() with timestep (dt) 0.016666667535901
```

`update()` ainda é chamado 60 vezes por segundo, mas o valor de `dt` muda. Vemos que apenas 1/5 (0.2) das chamadas a `update()` terão um `dt` de 1/60 (correspondente a 60 FPS)---o restante é zero. Todas as simulações de física também serão atualizadas de acordo com esse `dt` e avançarão apenas em um quinto dos frames.

::: sidenote
Você pode usar a funcionalidade de passo de tempo da coleção para pausar seu jogo, por exemplo enquanto mostra um popup ou quando a janela perdeu o foco. Use `msg.post("#myproxy", "set_time_step", {factor = 0, mode = 0})` para pausar e `msg.post("#myproxy", "set_time_step", {factor = 1, mode = 1})` para retomar.
:::

Veja [`set_time_step`](/ref/collectionproxy#set_time_step) para mais detalhes.

## Ressalvas e problemas comuns

Physics
: Por meio de proxies de coleção, é possível carregar mais de uma coleção de nível superior, ou *mundo de jogo*, na engine. Ao fazer isso, é importante saber que cada coleção de nível superior é um mundo físico separado. Interações de física (colisões, gatilhos, ray-casts) só acontecem entre objetos pertencentes ao mesmo mundo. Portanto, mesmo que objetos de colisão de dois mundos estejam visualmente bem em cima uns dos outros, não pode haver interação de física entre eles.

Memory
: Cada coleção carregada cria um novo mundo de jogo, que vem com uma pegada de memória relativamente grande. Se você carregar dezenas de coleções simultaneamente por proxies, talvez seja melhor reconsiderar seu design. Para criar muitas instâncias de hierarquias de objetos de jogo, [fábricas de coleção](/manuals/collection-factory) são mais adequadas.

Input
: Se você tem objetos em sua coleção carregada que exigem ações de entrada, precisa garantir que o objeto de jogo que contém o proxy de coleção adquira entrada. Quando o objeto de jogo recebe mensagens de entrada, elas são propagadas aos componentes desse objeto, isto é, aos proxies de coleção. As ações de entrada são enviadas pelo proxy para dentro da coleção carregada.
