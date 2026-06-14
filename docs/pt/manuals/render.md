---
title: O pipeline de renderização no Defold
brief: Este manual explica como o pipeline de renderização do Defold funciona e como você pode programá-lo.
---

# Renderização

Todo objeto exibido na tela pela engine - sprites, modelos, tiles, partículas ou nós de GUI - é desenhado por um renderizador. No centro do renderizador está um script de renderização que controla o pipeline de renderização. Por padrão, todo objeto 2D é desenhado com o bitmap correto, com a mesclagem especificada e na profundidade Z correta. Assim, talvez você nunca precise pensar em renderização além da ordem e de mesclagens simples. Para a maioria dos jogos 2D, o pipeline padrão funciona bem, mas seu jogo pode ter requisitos especiais. Se esse for o caso, o Defold permite escrever um pipeline de renderização sob medida.

### Pipeline de renderização - o quê, quando e onde?

O pipeline de renderização controla o que renderizar, quando renderizar e também onde renderizar. O que renderizar é controlado por [predicados de renderização](#render-predicates). Quando renderizar um predicado é controlado no [script de renderização](#the-render-script), e onde renderizar um predicado é controlado pela [projeção de visualização](#default-view-projection). O pipeline de renderização também pode descartar gráficos desenhados por um predicado de renderização que estejam fora de uma caixa delimitadora ou frustum definido. Esse processo é chamado de frustum culling.


## A renderização padrão

O arquivo de renderização contém uma referência ao script de renderização atual, além de materiais personalizados que devem ficar disponíveis no script de renderização (use com [`render.enable_material()`](/ref/render/#render.enable_material))

No centro do pipeline de renderização está o _script de renderização_. Esse é um script Lua com as funções `init()`, `update()` e `on_message()`, usado principalmente para interagir com a API gráfica subjacente. O script de renderização tem um lugar especial no ciclo de vida do seu jogo. Detalhes podem ser encontrados na [documentação do ciclo de vida da aplicação](/manuals/application-lifecycle).

Na pasta "Builtins" dos seus projetos, você encontra o recurso de renderização padrão ("default.render") e o script de renderização padrão ("default.render_script").

![Builtin render](images/render/builtin.png)

Para configurar um renderizador personalizado:

1. Copie os arquivos "default.render" e "default.render_script" para um local na hierarquia do seu projeto. É claro que você pode criar um script de renderização do zero, mas é uma boa ideia começar com uma cópia do script padrão, especialmente se você ainda está começando no Defold e/ou em programação gráfica.

2. Edite sua cópia do arquivo "default.render" e altere a propriedade *Script* para apontar para sua cópia do script de renderização.

3. Altere a propriedade *Render* (em *bootstrap*) no arquivo de configurações *game.project* para apontar para sua cópia do arquivo "default.render".


## Predicados de renderização {#render-predicates}

Para controlar a ordem de desenho dos objetos, você cria _predicados_ de renderização. Um predicado declara o que deve ser desenhado com base em uma seleção de _tags_ de material.

Cada objeto desenhado na tela tem um material associado que controla como o objeto deve ser desenhado na tela. No material, você especifica uma ou mais _tags_ que devem ser associadas ao material.

No seu script de renderização, você pode então criar um *render predicate* e especificar quais tags devem pertencer a esse predicado. Quando você manda a engine desenhar o predicado, cada objeto com um material contendo todas as tags especificadas para o predicado será desenhado.

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- um predicado que corresponde a todos os sprites com a tag "tree"
local trees = render.predicate({"tree"})
-- desenhará Sprite 1, 2 e 3
render.draw(trees)

-- um predicado que corresponde a todos os sprites com a tag "outlined"
local outlined = render.predicate({"outlined"})
-- desenhará Sprite 1, 2 e 4
render.draw(outlined)

-- um predicado que corresponde a todos os sprites com as tags "outlined" E "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- desenhará Sprite 1 e 2
render.draw(outlined_trees)
```


Uma descrição detalhada de como os materiais funcionam pode ser encontrada na [documentação de Material](/manuals/material).


## Projeção de visualização padrão {#default-view-projection}

O script de renderização padrão é configurado para usar uma projeção ortográfica adequada para jogos 2D. Ele fornece três projeções ortográficas diferentes: `Stretch` (padrão), `Fixed Fit` e `Fixed`. Como alternativa às projeções ortográficas no script de renderização padrão, você também tem a opção de usar a matriz de projeção fornecida por um componente de câmera.

### Projeção Stretch

A projeção stretch sempre desenha uma área do seu jogo igual às dimensões definidas em *game.project*, mesmo quando a janela é redimensionada. Se a proporção de tela mudar, o conteúdo do jogo será esticado vertical ou horizontalmente:

![Stretch projection](images/render/stretch_projection.png)

*Projeção Stretch com o tamanho original da janela*

![Stretch projection when resized](images/render/stretch_projection_resized.png)

*Projeção Stretch com a janela esticada horizontalmente*

A projeção stretch é a projeção padrão, mas se você mudou para outra e precisa voltar, faça isso enviando uma mensagem ao script de renderização:

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### Projeção Fixed Fit

Assim como a projeção stretch, a projeção fixed fit sempre mostra uma área do jogo igual às dimensões definidas em *game.project*, mas se a janela for redimensionada e a proporção de tela mudar, o conteúdo do jogo manterá a proporção original e conteúdo adicional será mostrado vertical ou horizontalmente:

![Fixed fit projection](images/render/fixed_fit_projection.png)

*Projeção Fixed Fit com o tamanho original da janela*

![Fixed fit projection when resized](images/render/fixed_fit_projection_resized.png)

*Projeção Fixed Fit com a janela esticada horizontalmente*

![Fixed fit projection when smaller](images/render/fixed_fit_projection_resized_smaller.png)

*Projeção Fixed Fit com a janela reduzida a 50% do tamanho original*

Você ativa a projeção fixed fit enviando uma mensagem ao script de renderização:

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### Projeção Fixed {#fixed-projection}

A projeção fixed manterá a proporção de tela original e renderizará o conteúdo do jogo com um nível fixo de zoom. Isso significa que, se o nível de zoom for definido para algo diferente de 100%, ela mostrará mais ou menos que a área do jogo definida pelas dimensões em *game.project*:

![Fixed projection](images/render/fixed_projection_zoom_2_0.png)

*Projeção Fixed com zoom definido como 2*

![Fixed projection](images/render/fixed_projection_zoom_0_5.png)

*Projeção Fixed com zoom definido como 0.5*

![Fixed projection](images/render/fixed_projection_zoom_2_0_resized.png)

*Projeção Fixed com zoom definido como 2 e janela reduzida a 50% do tamanho original*

Você ativa a projeção fixed enviando uma mensagem ao script de renderização:

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### Projeção de câmera

Ao usar o script de renderização padrão, se houver [componentes Camera](/manuals/camera) ativados disponíveis no projeto, eles terão precedência sobre qualquer outra visualização/projeção definida no script de renderização. Para ler mais sobre como trabalhar com componentes de câmera em scripts de renderização, consulte a [documentação de Camera](/manuals/camera).

Câmeras ortográficas suportam um `Orthographic Mode` que controla como a câmera se adapta à janela:
- `Fixed` usa o valor `Orthographic Zoom` da câmera.
- `Auto Fit` (contain) mantém toda a área de design visível.
- `Auto Cover` (cover) preenche a janela e pode cortar.

Você pode alternar modos no Editor ou em tempo de execução pela Camera API:

```lua
-- Usa comportamento auto-fit com uma câmera ortográfica
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Consulta o modo atual
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## Frustum culling

A API de renderização do Defold permite que desenvolvedores façam algo chamado frustum culling. Quando frustum culling está ativado, qualquer gráfico fora de uma caixa delimitadora ou frustum definido será ignorado. Em um mundo de jogo grande, onde apenas uma parte fica visível por vez, frustum culling pode reduzir drasticamente a quantidade de dados que precisa ser enviada à GPU para renderização, aumentando o desempenho e economizando bateria (em dispositivos móveis). É comum usar a visualização e a projeção da câmera para criar a caixa delimitadora. O script de renderização padrão usa a visualização e a projeção (da câmera) para calcular um frustum.

Frustum culling é implementado na engine por tipo de componente. Status atual:

| Component   | Supported |
|-------------|-----------|
| Sprite      | YES       |
| Model       | YES       |
| Mesh        | YES (1)   |
| Label       | YES       |
| Spine       | YES       |
| Particle fx | NO        |
| Tilemap     | YES       |
| Rive        | NO        |

1 = A caixa delimitadora de Mesh precisa ser definida pelo desenvolvedor. [Saiba mais](/manuals/mesh/#frustum-culling).


## Sistemas de coordenadas

Quando componentes são renderizados, normalmente falamos em qual sistema de coordenadas eles são renderizados. Na maioria dos jogos, alguns componentes são desenhados em espaço de mundo e outros em espaço de tela.

Componentes GUI e seus nós geralmente são desenhados no sistema de coordenadas de espaço de tela, com o canto inferior esquerdo da tela na coordenada (0,0) e o canto superior direito em (largura da tela, altura da tela). O sistema de coordenadas de espaço de tela nunca é deslocado nem traduzido de outra forma por uma câmera. Isso mantém os nós de GUI sempre desenhados na tela, independentemente de como o mundo é renderizado.

Sprites, tilemaps e outros componentes usados por objetos de jogo que existem no mundo do seu jogo geralmente são desenhados no sistema de coordenadas de espaço de mundo. Se você não fizer modificações no script de renderização e não usar nenhum componente de câmera para alterar a projeção de visualização, esse sistema de coordenadas será o mesmo que o sistema de coordenadas de espaço de tela. Mas assim que você adicionar uma câmera e movê-la ou alterar a projeção de visualização, os dois sistemas de coordenadas passarão a divergir. Quando a câmera se move, o canto inferior esquerdo da tela será deslocado de (0, 0) para que outras partes do mundo sejam renderizadas. Se a projeção mudar, as coordenadas serão traduzidas (ou seja, deslocadas de 0, 0) e modificadas por um fator de escala.


## O script de renderização {#the-render-script}

Abaixo está o código de um script de renderização personalizado, que é uma versão levemente modificada do script integrado.

init()
: A função `init()` é usada para configurar os predicados, a visualização e a cor de limpeza. Essas variáveis serão usadas durante a renderização propriamente dita.

```lua
function init(self)
    -- Define os predicados de renderização. Cada predicado é desenhado separadamente e
    -- isso permite alterar o estado do OpenGL entre os desenhos.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Cria e preenche tabelas de dados que serão usadas em update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: A função `update()` é chamada uma vez a cada frame. Sua função é realizar o desenho propriamente dito chamando as APIs OpenGL ES subjacentes (OpenGL Embedded Systems API). Para entender corretamente o que acontece na função `update()`, você precisa entender como o OpenGL funciona. Há muitos ótimos recursos sobre OpenGL ES disponíveis. O site oficial é um bom ponto de partida. Você o encontra em https://www.khronos.org/opengles/

  Este exemplo contém a configuração necessária para desenhar modelos 3D. A função `init()` definiu um predicado `self.predicates.model`. Em outro lugar, um material com a tag "model" foi criado. Também há alguns componentes de modelo que usam esse material:

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- limpa os buffers da tela
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- renderiza modelos
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- renderiza o mundo (sprites, tilemaps, partículas etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- renderiza GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

Até aqui, este é um script de renderização simples e direto. Ele desenha da mesma maneira em cada frame. Porém, às vezes é desejável introduzir estado no script de renderização e realizar operações diferentes dependendo desse estado. Também pode ser desejável comunicar-se com o script de renderização a partir de outras partes do código do jogo.

on_message()
: Um script de renderização pode definir uma função `on_message()` e receber mensagens de outras partes do seu jogo ou app. Um caso comum em que um componente externo envia informações ao script de renderização é a _câmera_. Um componente de câmera que adquiriu foco de câmera enviará automaticamente sua visualização e projeção ao script de renderização a cada frame. Essa mensagem se chama `"set_view_projection"`:

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Alguém nos enviou uma nova cor de limpeza a ser usada.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- O componente de câmera que tem foco de câmera enviará mensagens
        -- set_view_projection para o socket @render. Podemos usar as informações
        -- da câmera para definir a visualização (e possivelmente a projeção) da renderização.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

No entanto, qualquer script ou script de GUI pode enviar mensagens ao script de renderização pelo socket especial `@render`:

```lua
-- Altera a cor de limpeza.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## Recursos de renderização
Para passar certos recursos da engine para o script de renderização, você pode adicioná-los à tabela `Render Resources` no arquivo `.render` atribuído ao projeto:

![Render resources](images/render/render_resources.png)

Usando esses recursos em um script de renderização:

```lua
-- "my_material" agora será usado para todas as chamadas de desenho associadas ao predicado
render.enable_material("my_material")
-- tudo que for desenhado pelo predicado acabará em "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- vincula a textura de resultado do render target ao que estiver sendo renderizado pelo predicado
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
No momento, o Defold suporta apenas `Materials` e `Render Targets` como recursos de renderização referenciados, mas com o tempo mais tipos de recurso serão suportados por esse sistema.
:::

## Handles de textura

Texturas no Defold são representadas internamente como um handle, que essencialmente equivale a um número que deve identificar de forma única um objeto de textura em qualquer lugar da engine. Isso significa que você pode conectar o mundo de game objects ao mundo de renderização passando esses handles entre o sistema de renderização e um script de game object. Por exemplo, um script pode criar uma textura dinâmica em um script anexado a um game object e enviá-la ao renderizador para ser usada como textura global em um comando de desenho.

Em um arquivo `.script`:

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- observação: my_texture_resource é um hash para o caminho do recurso, que não pode ser usado como handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contém informações sobre a textura, como largura, altura e assim por diante
-- ele também contém o handle, que é o que queremos
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

Em um arquivo `.render_script`:

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- vincula a textura personalizada ao estado de desenho
    render.enable_texture(0, self.my_texture)
    -- desenha..
end
```

::: sidenote
Atualmente não há como alterar para qual textura um recurso deve apontar; você só pode usar handles brutos como este no script de renderização.
:::

## APIs gráficas suportadas
A API de script de renderização do Defold traduz operações de renderização para as seguintes APIs gráficas:

:[Graphics API](../shared/graphics-api.md)


## Mensagens do sistema

`"set_view_projection"`
: Esta mensagem é enviada por componentes de câmera que adquiriram foco de câmera.

`"window_resized"`
: A engine enviará esta mensagem quando houver mudanças no tamanho da janela. Você pode ouvir esta mensagem para alterar a renderização quando o tamanho da janela alvo mudar. No desktop, isso significa que a janela real do jogo foi redimensionada; em dispositivos móveis, esta mensagem é enviada sempre que ocorre uma mudança de orientação.

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- A janela foi redimensionada. message.width e message.height contêm as novas dimensões.
    ...
  end
end
```

`"draw_line"`
: Desenha uma linha de debug. Use para visualizar `ray_casts`, vetores e mais. As linhas são desenhadas com a chamada `render.draw_debug3d()`.

```lua
-- desenha uma linha branca
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: Desenha texto de debug. Use para imprimir informações de debug. O texto é desenhado com a fonte integrada `always_on_top.font`. A fonte do sistema tem um material com a tag `debug_text` e é renderizada com outros textos no script de renderização padrão.

```lua
-- desenha uma mensagem de texto
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

O profiler visual acessível pela mensagem `"toggle_profile"` enviada ao socket `@system` não faz parte do renderizador programável. Ele é desenhado separadamente do seu script de renderização.


## Draw calls e batching {#draw-calls-and-batching}

Uma draw call é o termo usado para descrever o processo de configurar a GPU para desenhar um objeto na tela usando uma textura e um material com configurações adicionais opcionais. Esse processo geralmente consome muitos recursos, e recomenda-se que o número de draw calls seja o menor possível. Você pode medir o número de draw calls e o tempo que elas levam para renderizar usando o [profiler integrado](/manuals/profiling/).

O Defold tentará agrupar operações de renderização para reduzir o número de draw calls de acordo com um conjunto de regras definidas abaixo. As regras diferem entre componentes GUI e todos os outros tipos de componente.


### Regras de batch para componentes não GUI

A renderização é feita com base na ordem z, de baixo para alto. A engine começará ordenando a lista de coisas a desenhar e iterará dos valores z mais baixos para os mais altos. Cada objeto na lista será agrupado na mesma draw call que o objeto anterior se as seguintes condições forem atendidas:

* Pertence ao mesmo proxy de coleção
* É do mesmo tipo de componente (sprite, particle fx, tilemap etc)
* Usa a mesma textura (atlas ou tile source)
* Tem o mesmo material
* Tem as mesmas constantes de shader (como tint)

Isso significa que, se dois componentes sprite no mesmo proxy de coleção tiverem valores z adjacentes ou iguais (e, portanto, ficarem próximos na lista ordenada), usarem a mesma textura, material e constantes, eles serão agrupados na mesma draw call.


### Regras de batch para componentes GUI

A renderização dos nós em um componente GUI é feita de cima para baixo na lista de nós. Cada nó da lista será agrupado na mesma draw call que o nó anterior se as seguintes condições forem atendidas:

* É do mesmo tipo (box, text, pie etc)
* Usa a mesma textura (atlas ou tile source)
* Tem o mesmo modo de mesclagem.
* Tem a mesma fonte (somente para nós de texto)
* Tem as mesmas configurações de stencil

::: sidenote
A renderização de nós é feita por componente. Isso significa que nós de componentes GUI diferentes não serão agrupados em batch.
:::

A capacidade de organizar nós em hierarquias facilita agrupá-los em unidades gerenciáveis. Mas hierarquias podem efetivamente quebrar a renderização em batch se você misturar tipos de nós diferentes. É possível agrupar nós GUI em batch de forma mais eficiente mantendo hierarquias de nós usando camadas de GUI. Você pode ler mais sobre camadas de GUI e como elas afetam draw calls no [manual de GUI](/manuals/gui#layers-and-draw-calls).
