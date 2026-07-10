---
title: Manual do componente de câmera
brief: Este manual descreve a funcionalidade do componente de câmera do Defold.
---

# Câmeras

Uma câmera no Defold é um componente que altera o viewport e a projeção do mundo do jogo. O componente de câmera define uma câmera perspectiva ou ortográfica básica que fornece uma matriz de visualização e uma matriz de projeção ao script de renderização.

Uma câmera perspectiva normalmente é usada em jogos 3D, em que a visão da câmera e o tamanho e a perspectiva dos objetos são baseados em um frustum de visualização e na distância e no ângulo de visão da câmera até os objetos no jogo.

Para jogos 2D, costuma ser desejável renderizar a cena com uma projeção ortográfica. Isso significa que a visão da câmera não é mais determinada por um frustum de visualização, mas por uma caixa. A projeção ortográfica não é realista, pois não altera o tamanho dos objetos com base em sua distância. Um objeto a 1000 unidades de distância será renderizado com o mesmo tamanho que um objeto bem na frente da câmera.

![projeções](images/camera/projections.png)


## Criando uma câmera

Para criar uma câmera, use <kbd>right click</kbd> em um objeto de jogo e selecione <kbd>Add Component ▸ Camera</kbd>. Como alternativa, você pode criar um arquivo de componente na hierarquia do seu projeto e adicionar o arquivo de componente ao objeto de jogo.

![criar componente de câmera](images/camera/create.png)

O componente de câmera tem as seguintes propriedades, que definem o *frustum* da câmera:

![configurações da câmera](images/camera/settings.png)

Id
: O id do componente.

Aspect Ratio
: (**Somente câmera perspectiva**) - A razão entre a largura e a altura do frustum. 1.0 significa que você assume uma visualização quadrada. 1.33 é bom para uma visualização 4:3, como 1024x768. 1.78 é bom para uma visualização 16:9. Esta configuração é ignorada se *Auto Aspect Ratio* estiver definido.

Fov
: (**Somente câmera perspectiva**) - O campo de visão *vertical* da câmera, expresso em _radianos_. Quanto maior o campo de visão, mais a câmera verá.

Near Z
: O valor Z do plano de recorte próximo.

Far Z
: O valor Z do plano de recorte distante.

Auto Aspect Ratio
: (**Somente câmera perspectiva**) - Defina isto para permitir que a câmera calcule automaticamente a proporção de tela.

Orthographic Projection
: Defina isto para mudar a câmera para uma projeção ortográfica (veja abaixo).

Orthographic Zoom
: (**Somente câmera ortográfica**) - Um multiplicador de zoom controlado pelo usuário (> 1 = aproximar, < 1 = afastar). No modo `Fixed`, ele é o zoom efetivo. Nos modos `Auto Fit` e `Auto Cover`, ele é multiplicado pelo zoom calculado automaticamente, permitindo aplicar zoom adicional sem desativar o ajuste automático.

Orthographic Mode
: (**Somente câmera ortográfica**) - Controla como a câmera ortográfica determina o zoom em relação ao tamanho da janela e à resolução de design (os valores em `game.project` → `display.width/height`).
  - `Fixed` (usa zoom constante): Usa o valor atual de `Orthographic Zoom` como está.
  - `Auto Fit` (contain): Calcula automaticamente o zoom para que toda a área de design caiba dentro da janela e depois o multiplica por `Orthographic Zoom`. Pode mostrar conteúdo extra nas laterais ou acima/abaixo.
  - `Auto Cover` (cover): Calcula automaticamente o zoom para que a área de design cubra a janela inteira e depois o multiplica por `Orthographic Zoom`. Pode recortar nas laterais ou acima/abaixo.
  Disponível somente quando `Orthographic Projection` está ativado.


## Usando a câmera

Todas as câmeras são ativadas e atualizadas automaticamente durante um frame, e o módulo Lua `camera` fica disponível em todos os contextos de script. Desde o Defold 1.8.1, não é mais necessário ativar explicitamente uma câmera enviando uma mensagem `acquire_camera_focus` ao componente de câmera. As mensagens antigas de adquirir e liberar continuam disponíveis, mas recomenda-se usar as mensagens `enable` e `disable`, como em qualquer outro componente que você queira ativar ou desativar:

```lua
msg.post("#camera", "disable")
msg.post("#camera", "enable")
```

Para listar todas as câmeras disponíveis no momento, você pode usar `camera.get_cameras()`:

```lua
-- Observação: as chamadas render só estão disponíveis em um script de renderização.
--             A função camera.get_cameras() pode ser usada em qualquer lugar,
--             mas render.set_camera só pode ser usada em um script de renderização.

for k,v in pairs(camera.get_cameras()) do
    -- a tabela de câmeras contém as URLs de todas as câmeras
    render.set_camera(v)
    -- faça a renderização aqui; tudo que for renderizado aqui e usar materiais com
    -- matrizes de visualização e projeção especificadas usará matrizes da câmera.
end
-- para desativar uma câmera, passe nil (ou nenhum argumento) para render.set_camera.
-- depois desta chamada, todas as chamadas render usarão as matrizes de visualização
-- e projeção especificadas no contexto de renderização
-- (render.set_view e render.set_projection)
render.set_camera()
```

O módulo de script `camera` tem várias funções que podem ser usadas para manipular a câmera. Estes são apenas alguns exemplos; para ver todas as funções disponíveis, consulte o manual na [documentação da API](/ref/camera/)).

```lua
camera.get_aspect_ratio(camera) -- obtém a proporção de tela
camera.get_far_z(camera) -- obtém far z
camera.get_fov(camera) -- obtém o campo de visão
camera.get_orthographic_mode(camera) -- obtém o modo ortográfico (um de camera.ORTHO_MODE_*)
camera.get_orthographic_zoom(camera) -- obtém o multiplicador de zoom controlado pelo usuário
camera.get_orthographic_auto_zoom(camera) -- obtém o zoom calculado automaticamente
camera.set_aspect_ratio(camera, ratio) -- define a proporção de tela
camera.set_far_z(camera, far_z) -- define far z
camera.set_near_z(camera, near_z) -- define near z
camera.set_orthographic_mode(camera, camera.ORTHO_MODE_AUTO_FIT) -- define o modo ortográfico
... e assim por diante
```

Uma câmera é identificada por uma URL, que é o caminho completo do componente na cena, incluindo a coleção, o objeto de jogo ao qual ela pertence e o id do componente. Neste exemplo, você usaria a URL `/go#camera` para identificar o componente de câmera dentro da mesma coleção, e `main:/go#camera` ao acessar uma câmera de uma coleção diferente ou do script de renderização.

![criar componente de câmera](images/camera/create.png)

```lua
-- Acessando uma câmera a partir de um script na mesma coleção:
camera.get_fov("/go#camera")

-- Acessando uma câmera a partir de um script em uma coleção diferente:
camera.get_fov("main:/go#camera")

-- Acessando uma câmera a partir do script de renderização:
render.set_camera("main:/go#camera")
```

A cada frame, o componente de câmera que está com foco de câmera enviará uma mensagem `set_view_projection` para o socket `@render`:

```lua
-- builtins/render/default.render_script
--
function on_message(self, message_id, message)
    if message_id == hash("set_view_projection") then
        self.view = message.view                    -- [1]
        self.projection = message.projection
    end
end
```
1. A mensagem enviada pelo componente de câmera inclui uma matriz de visualização e uma matriz de projeção.

O componente de câmera fornece ao script de renderização uma matriz de projeção perspectiva ou ortográfica, dependendo da propriedade *Orthographic Projection* da câmera. A matriz de projeção também leva em conta os planos de recorte próximo e distante definidos, o campo de visão e as configurações de proporção de tela da câmera.

A matriz de visualização fornecida pela câmera define a posição e a orientação da câmera. Uma câmera com *Orthographic Projection* centralizará a visualização na posição do objeto de jogo ao qual ela está anexada, enquanto uma câmera com *Perspective Projection* terá o canto inferior esquerdo da visualização posicionado no objeto de jogo ao qual ela está anexada.


### Script de renderização

Ao usar o script de renderização padrão, o Defold definirá automaticamente a última câmera ativada que deve ser usada para renderização. Antes dessa mudança, algum script no projeto precisava enviar explicitamente a mensagem `use_camera_projection` ao renderer para notificá-lo de que a visualização e a projeção dos componentes de câmera deveriam ser usadas. Isso não é mais necessário, mas ainda é possível fazer isso por compatibilidade com versões anteriores.

Como alternativa, você pode definir em um script de renderização uma câmera específica que deve ser usada para renderizar. Isso pode ser útil em casos em que você precisa controlar com mais precisão qual câmera deve ser usada para renderização, por exemplo em um jogo multiplayer.

```lua
-- render.set_camera usará automaticamente as matrizes de visualização e projeção
-- para qualquer renderização que acontecer até render.set_camera() ser chamada.
render.set_camera("main:/my_go#camera")
```

Para verificar se uma câmera está ativa ou não, você pode usar a função `get_enabled` da [API Camera](https://defold.com/ref/alpha/camera/#camera.get_enabled:camera):

```lua
if camera.get_enabled("main:/my_go#camera") then
    -- a câmera está ativada, use-a para renderizar!
    render.set_camera("main:/my_go#camera")
end
```

::: sidenote
Para usar a função `set_camera` junto com frustum culling, você precisa passar isto como uma opção para a função:
`render.set_camera("main:/my_go#camera", {use_frustum = true})`
:::

### Movendo a câmera

Você desloca/move a câmera pelo mundo do jogo movendo o objeto de jogo ao qual o componente de câmera está anexado. O componente de câmera enviará automaticamente uma matriz de visualização atualizada com base na posição atual da câmera nos eixos x e y.

### Aplicando zoom à câmera

Você pode aproximar e afastar ao usar uma câmera perspectiva movendo o objeto de jogo ao qual a câmera está anexada ao longo do eixo z. O componente de câmera enviará automaticamente uma matriz de visualização atualizada com base na posição z atual da câmera.

Você pode aproximar e afastar ao usar uma câmera ortográfica alterando a propriedade *Orthographic Zoom* da câmera, no editor ou em tempo de execução:

```lua
-- No modo Fixed, este é o zoom efetivo.
go.set("#camera", "orthographic_zoom", 2)
```

Nos modos `Auto Fit` e `Auto Cover`, *Orthographic Zoom* é aplicado sobre o zoom calculado automaticamente; ele não é ignorado. Por exemplo, defina *Orthographic Mode* como `Auto Fit` e *Orthographic Zoom* como `1.25` no editor para ajustar a área de design à janela e depois aplicar 25% de zoom adicional. A configuração equivalente em tempo de execução é:

```lua
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)
go.set("#camera", "orthographic_zoom", 1.25)

local auto_zoom = camera.get_orthographic_auto_zoom("#camera")
local zoom_multiplier = camera.get_orthographic_zoom("#camera")
local effective_zoom = auto_zoom * zoom_multiplier
```

`camera.get_orthographic_auto_zoom()` retorna o zoom calculado a partir das dimensões atuais da janela e do projeto nos modos `Auto Fit` e `Auto Cover`. No modo `Fixed`, retorna `1.0`. O mesmo valor está disponível por meio da propriedade de componente somente leitura `orthographic_auto_zoom`:

```lua
local auto_zoom = go.get("#camera", "orthographic_auto_zoom")
```

Ao usar uma câmera ortográfica, você também pode trocar como o zoom é determinado usando a configuração `Orthographic Mode` ou por script:

```lua
-- obtém o modo atual (um de camera.ORTHO_MODE_FIXED, _AUTO_FIT, _AUTO_COVER)
local mode = camera.get_orthographic_mode("#camera")

-- muda para auto-fit (contain) para manter sempre toda a área de design visível
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_FIT)

-- muda para auto-cover para garantir que a área de design cubra a janela
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_AUTO_COVER)

-- muda para o modo fixed para usar orthographic_zoom sem ajuste automático
camera.set_orthographic_mode("#camera", camera.ORTHO_MODE_FIXED)
```

### Zoom adaptativo

O conceito por trás do zoom adaptativo é ajustar o valor de zoom da câmera quando a resolução do display muda em relação à resolução inicial definida em *game.project*.

Duas abordagens comuns para zoom adaptativo são:

1. Max zoom - Calcular um valor de zoom de forma que o conteúdo coberto pela resolução inicial em *game.project* preencha e se expanda além dos limites da tela, possivelmente ocultando parte do conteúdo nas laterais ou acima e abaixo.
2. Min zoom - Calcular um valor de zoom de forma que o conteúdo coberto pela resolução inicial em *game.project* fique completamente contido dentro dos limites da tela, possivelmente mostrando conteúdo adicional nas laterais ou acima e abaixo.

Exemplo:

```lua
local DISPLAY_WIDTH = sys.get_config_int("display.width")
local DISPLAY_HEIGHT = sys.get_config_int("display.height")

function init(self)
    local initial_zoom = go.get("#camera", "orthographic_zoom")
    local display_scale = window.get_display_scale()
    window.set_listener(function(self, event, data)
        if event == window.WINDOW_EVENT_RESIZED then
            local window_width = data.width
            local window_height = data.height
            local design_width = DISPLAY_WIDTH / initial_zoom
            local design_height = DISPLAY_HEIGHT / initial_zoom

            -- max zoom: garante que as dimensões iniciais de design preencham
            -- e se expandam além dos limites da tela
            local zoom = math.max(window_width / design_width, window_height / design_height) / display_scale

            -- min zoom: garante que as dimensões iniciais de design encolham
            -- e fiquem contidas dentro dos limites da tela
            --local zoom = math.min(window_width / design_width, window_height / design_height) / display_scale
            
            go.set("#camera", "orthographic_zoom", zoom)
        end
    end)
end
```

Um exemplo completo de zoom adaptativo pode ser visto [neste projeto de exemplo](https://github.com/defold/sample-adaptive-zoom).

Observação: com uma câmera ortográfica, agora você pode obter comportamento contain/cover sem código personalizado definindo `Orthographic Mode` como `Auto Fit` (contain) ou `Auto Cover` (cover). Nesses modos, o zoom calculado com base no tamanho da janela e na resolução de design é multiplicado por `Orthographic Zoom`.


### Seguindo um objeto de jogo

Você pode fazer a câmera seguir um objeto de jogo definindo o objeto de jogo ao qual o componente de câmera está anexado como filho do objeto de jogo a ser seguido:

![seguir objeto de jogo](images/camera/follow.png)

Uma forma alternativa é atualizar a posição do objeto de jogo ao qual o componente de câmera está anexado a cada frame, conforme o objeto de jogo a ser seguido se move.

### Convertendo mouse para coordenadas do mundo {#converting-mouse-to-world-coordinates}

Quando a câmera foi deslocada, recebeu zoom ou teve sua projeção alterada em relação à projeção ortográfica Stretch padrão, as coordenadas do mouse fornecidas na função de ciclo de vida `on_input()` não corresponderão mais às coordenadas do mundo dos seus objetos de jogo. Você precisa levar em conta manualmente a mudança na visualização ou projeção. O código para converter de coordenadas de mouse/tela para coordenadas do mundo é este:

```Lua
--- Converte coordenadas de tela em coordenadas do mundo levando em conta
-- a visualização e a projeção de uma câmera específica
-- @param camera URL da câmera a usar para conversão
-- @param screen_x Coordenada x da tela a converter
-- @param screen_y Coordenada y da tela a converter
-- @param z coordenada z opcional para passar pela conversão; o padrão é 0
-- @return world_x A coordenada x do mundo resultante da coordenada de tela
-- @return world_y A coordenada y do mundo resultante da coordenada de tela
-- @return world_z A coordenada z do mundo resultante da coordenada de tela
function M.screen_to_world(camera, screen_x, screen_y, z)
    local projection = go.get(camera, "projection")
    local view = go.get(camera, "view")
    local w, h = window.get_size()

    -- https://defold.com/manuals/camera/#converting-mouse-to-world-coordinates
    local inv = vmath.inv(projection * view)
    local x = (2 * screen_x / w) - 1
    local y = (2 * screen_y / h) - 1
    local x1 = x * inv.m00 + y * inv.m01 + z * inv.m02 + inv.m03
    local y1 = x * inv.m10 + y * inv.m11 + z * inv.m12 + inv.m13
    return x1, y1, z or 0
end
```

Lembre-se de que os valores `action.screen_x` e `action.screen_y` de `on_input()` devem ser usados como argumentos para esta função. Visite a [página de exemplos](https://defold.com/examples/render/screen_to_world/) para ver a conversão de coordenadas de tela para mundo em ação. Também há um [projeto de exemplo](https://github.com/defold/sample-screen-to-world-coordinates/) mostrando como fazer conversão de coordenadas de tela para mundo.

::: sidenote
As [soluções de câmera de terceiros mencionadas neste manual](/manuals/camera/#third-party-camera-solutions) fornecem funções para converter para e a partir de coordenadas de tela.
:::

## Manipulação em runtime
Você pode manipular câmeras em runtime por meio de várias mensagens e propriedades diferentes (consulte a [documentação da API para uso](/ref/camera/)).

Uma câmera tem várias propriedades diferentes que podem ser manipuladas usando `go.get()` e `go.set()`:

`fov`
: O campo de visão da câmera (`number`).

`near_z`
: O valor Z próximo da câmera (`number`).

`far_z`
: O valor Z distante da câmera (`number`).

`orthographic_zoom`
: O multiplicador de zoom da câmera ortográfica controlado pelo usuário. Nos modos `Auto Fit` e `Auto Cover`, ele é multiplicado por `orthographic_auto_zoom`. (`number`).

`orthographic_auto_zoom`
: O zoom ortográfico calculado nos modos `Auto Fit` e `Auto Cover`, ou `1.0` no modo `Fixed`. SOMENTE LEITURA. (`number`).

`aspect_ratio`
: A razão entre a largura e a altura do frustum. Usada ao calcular a projeção de uma câmera perspectiva. (`number`).

`view`
: A matriz de visualização calculada da câmera. SOMENTE LEITURA. (`matrix4`).

`projection`
: A matriz de projeção calculada da câmera. SOMENTE LEITURA. (`matrix4`).


## Soluções de câmera de terceiros {#third-party-camera-solutions}

Há soluções de câmera feitas pela comunidade que implementam recursos comuns, como tremor de tela, seguir objetos de jogo, conversão de coordenadas de tela para mundo e muito mais. Elas podem ser baixadas no Portal de Assets do Defold:

- [Orthographic camera](https://defold.com/assets/orthographic/) (somente 2D), por Björn Ritzl.
- [Defold Rendy](https://defold.com/assets/defold-rendy/) (2D e 3D), por Klayton Kowalski.
