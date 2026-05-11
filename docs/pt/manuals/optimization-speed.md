---
title: Otimizando o desempenho em tempo de execução de um jogo Defold
brief: Este manual descreve como otimizar um jogo Defold para rodar com uma taxa de quadros alta e estável.
---

# Otimizando a velocidade em tempo de execução
Antes de tentar otimizar um jogo com o objetivo de fazê-lo rodar com uma taxa de quadros alta e estável, você precisa saber onde estão os gargalos. O que realmente consome a maior parte do tempo em um frame do seu jogo? É a renderização? É a lógica do jogo? É o grafo de cena? Para descobrir isso, recomenda-se usar as ferramentas de profiling integradas. Use o [perfilador na tela ou web](/manuals/profiling/) para amostrar o desempenho do seu jogo e então decidir se deve otimizar e o que otimizar. Depois de entender melhor o que consome tempo, você pode começar a tratar os problemas.

## Reduzir o tempo de execução de scripts
Reduzir o tempo de execução de scripts é necessário se o perfilador mostrar valores altos para o escopo `Script`. Como regra geral, é claro que você deve tentar executar o mínimo de código possível a cada frame. Executar muito código em `update()` e `on_input()` a cada frame provavelmente impactará o desempenho do seu jogo, especialmente em dispositivos de baixo desempenho. Algumas diretrizes:

### Use padrões de código reativos
Não faça polling por mudanças se você puder receber um callback. Não anime algo manualmente nem execute uma tarefa que possa ser entregue à engine (por exemplo, `go.animate()` em vez de animar algo manualmente).

### Reduzir garbage collection
Se você cria muitos objetos de vida curta, como tabelas Lua, a cada frame, isso acabará acionando o coletor de lixo do Lua. Quando isso acontece, pode se manifestar como pequenas travadas/picos no tempo de frame. Reutilize tabelas sempre que possível e tente realmente evitar criar tabelas Lua dentro de loops e construções semelhantes.

### Pré-calcular hashes de ids de mensagens e ações
Se você lida com muitas mensagens ou tem muitos eventos de entrada para tratar, é recomendado pré-calcular os hashes das strings. Considere este trecho de código:

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("message1") then
        msg.post(sender, hash("message3"))
    elseif message_id == hash("message2") then
        msg.post(sender, hash("message4"))
    end
end
```

No cenário acima, a string com hash seria recriada toda vez que uma mensagem fosse recebida. Isso pode ser melhorado criando as strings com hash uma vez e usando as versões com hash ao tratar mensagens:

```lua
local MESSAGE1 = hash("message1")
local MESSAGE2 = hash("message2")
local MESSAGE3 = hash("message3")
local MESSAGE4 = hash("message4")

function on_message(self, message_id, message, sender)
    if message_id == MESSAGE1 then
        msg.post(sender, MESSAGE3)
    elseif message_id == MESSAGE2 then
        msg.post(sender, MESSAGE4)
    end
end
```

### Prefira e faça cache de URLs
A passagem de mensagens, ou outras formas de endereçar um objeto de jogo ou componente, pode ser feita fornecendo um id como string ou hash, ou como uma URL. Se uma string ou hash for usado, internamente ele será traduzido para uma URL. Portanto, é recomendado fazer cache das URLs usadas com frequência para obter o melhor desempenho possível do sistema. Considere o seguinte:

```lua
    local pos = go.get_position("enemy")
    local pos = go.get_position(hash("enemy"))
    local pos = go.get_position(msg.url("enemy"))
    -- faz algo com pos
```

Em todos os três casos, a posição de um objeto de jogo com id `enemy` seria obtida. No primeiro e no segundo caso, o id (string ou hash) seria convertido em uma URL antes de ser usado. Isso nos diz que é melhor fazer cache de URLs e usar a versão em cache para obter o melhor desempenho possível:

```lua
    function init(self)
        self.enemy_url = msg.url("enemy")
    end

    function update(self, dt)
        local pos = go.get_position(self.enemy_url)
        -- faz algo com pos
    end
```

## Reduzir o tempo necessário para renderizar um frame
Reduzir o tempo necessário para renderizar um frame é necessário se o perfilador mostrar valores altos nos escopos `Render` e `Render Script`. Há várias coisas a considerar ao tentar reduzir o tempo necessário para renderizar um frame:

* Reduzir draw calls - Leia mais sobre como reduzir draw calls [neste post do fórum](https://forum.defold.com/t/draw-calls-and-defold/4674)
* Reduzir overdraw
* Reduzir a complexidade dos shaders - Leia sobre otimizações GLSL [neste artigo da Khronos](https://www.khronos.org/opengl/wiki/GLSL_Optimizations). Você também pode modificar os shaders padrão usados pelo Defold (encontrados em `builtins/materials`) e reduzir a precisão dos shaders para ganhar alguma velocidade em dispositivos de baixo desempenho. Todos os shaders usam precisão `highp`, e uma mudança para, por exemplo, `mediump` pode em alguns casos melhorar ligeiramente o desempenho.

## Reduzir a complexidade do grafo de cena
Reduzir a complexidade do grafo de cena é necessário se o perfilador mostrar valores altos no escopo `GameObject` e, mais especificamente, na amostra `UpdateTransform`. Algumas ações a tomar:

* Culling - Desabilite objetos de jogo (e seus componentes) se eles não estiverem visíveis no momento. Como isso é determinado depende muito do tipo de jogo. Para um jogo 2D, pode ser tão simples quanto sempre desabilitar objetos de jogo que estejam fora de uma área retangular. Você pode usar um gatilho de física para detectar isso ou particionar seus objetos em buckets. Depois de saber quais objetos desabilitar ou habilitar, faça isso enviando uma mensagem `disable` ou `enable` para cada objeto de jogo.

## Frustum culling
O script de renderização pode ignorar automaticamente a renderização de componentes de objetos de jogo que estejam fora de uma caixa delimitadora definida (frustum). Saiba mais sobre Frustum Culling no [manual do Pipeline de Renderização](/manuals/render/#frustum-culling).

# Otimizações específicas de plataforma

## Android Device Performance Framework
Android Dynamic Performance Framework é um conjunto de APIs que permite que jogos interajam mais diretamente com os sistemas de energia e temperatura dos dispositivos Android. É possível monitorar o comportamento dinâmico em sistemas Android e otimizar o desempenho do jogo em um nível sustentável que não superaqueça os dispositivos. Use a [extensão Android Dynamic Performance Framework](https://defold.com/extension-adpf/) para monitorar e otimizar o desempenho do seu jogo Defold em dispositivos Android.
