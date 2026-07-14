---
title: Propriedades no Defold
brief: Este manual explica que tipos de propriedades existem no Defold, e como elas são usadas e animadas.
---

# Propriedades

O Defold expõe propriedades para objetos de jogo, componentes e nodes de GUI que podem ser lidas, definidas e animadas. Existem os seguintes tipos de propriedades:

* Transformações de objeto de jogo definidas pelo sistema (posição, rotação e escala) e propriedades específicas de componentes (por exemplo, o tamanho em pixels de um sprite ou a massa de um objeto de colisão)
* Propriedades de componentes de script definidas pelo usuário em scripts Lua (veja a [documentação de propriedades de script](/manuals/script-properties) para detalhes)
* Propriedades de nodes de GUI
* Constantes de shader definidas em shaders e arquivos de material (veja a [documentação de Material](/manuals/material) para detalhes)

Propriedades numéricas exibem uma alça de arrasto quando você passa o mouse sobre o campo de entrada. Você pode aumentar/diminuir o valor arrastando a alça para a direita/esquerda ou para cima/baixo, respectivamente.

Dependendo de onde uma propriedade é encontrada, você a acessa por meio de uma função genérica ou de uma função específica da propriedade. Muitas propriedades podem ser animadas automaticamente. Animar propriedades pelo sistema integrado é altamente recomendado em vez de manipular as propriedades você mesmo (dentro de uma função `update()`), tanto por motivos de desempenho quanto de conveniência.

Propriedades compostas dos tipos `vector3`, `vector4` ou `quaternion` também expõem seus subcomponentes (`x`, `y`, `z` e `w`). Você pode endereçar os componentes individualmente adicionando um ponto (`.`) e o nome do componente ao nome da propriedade. Por exemplo, para definir o componente x da posição de um objeto de jogo:

```lua
-- Define a posição x de "game_object" para 10.
go.set("game_object", "position.x", 10)
```

As funções `go.get()`, `go.set()` e `go.animate()` recebem uma referência como primeiro parâmetro e um identificador de propriedade como segundo. A referência identifica o objeto de jogo ou componente e pode ser uma string, um hash ou uma URL. URLs são explicadas em detalhe no [manual de endereçamento](/manuals/addressing). O identificador de propriedade é uma string ou hash que nomeia a propriedade:

```lua
-- Define a escala x do componente sprite
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

Para nodes de GUI, o node é fornecido como primeiro parâmetro de uma função específica da propriedade ou das funções genéricas `gui.get()` e `gui.set()`:

```lua
-- Obtém a cor do botão
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## Propriedades de objetos de jogo e componentes

Todos os objetos de jogo, e alguns tipos de componente, têm propriedades que podem ser lidas e manipuladas em tempo de execução. Leia esses valores com [`go.get()`](/ref/go#go.get) e escreva-os com [`go.set()`](/ref/go#go.set). Dependendo do tipo de valor da propriedade, você pode animar os valores com [`go.animate()`](/ref/go#go.animate). Um pequeno conjunto de propriedades é somente leitura.

`get`{.mark}
: Pode ser lida com [`go.get()`](/ref/go#go.get).

`get+set`{.mark}
: Pode ser lida com [`go.get()`](/ref/go#go.get) e escrita com [`go.set()`](/ref/go#go.set). Valores numéricos podem ser animados com [`go.animate()`](/ref/go#go.animate).

*PROPRIEDADES DE OBJETO DE JOGO*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | A posição local do objeto de jogo. | `vector3`      | `get+set`{.mark} |
| *rotation* | Rotação local do objeto de jogo, expressa como um `quaternion`.  | `quaternion` | `get+set`{.mark} |
| *euler*    | Rotação local do objeto de jogo, em ângulos de Euler. | `vector3` | `get+set`{.mark} |
| *scale*    | Escala local não uniforme do objeto de jogo, expressa como um vetor onde cada componente contém um multiplicador ao longo de cada eixo. Para dobrar o tamanho em X e Y sem alterar Z, use `vmath.vector3(2.0, 2.0, 1.0)`. | `vector3` | `get+set`{.mark} |
| *scale.xy*    | Escala local não uniforme do objeto de jogo nos eixos X e Y. Use esta propriedade ou `go.set_scale_xy()` quando não desejar alterar a escala em Z. | `vector3` | `get+set`{.mark} |

::: sidenote
Também existem funções específicas para trabalhar com a transformação do objeto de jogo; elas são `go.get_position()`, `go.set_position()`, `go.get_rotation()`, `go.set_rotation()`,  `go.get_scale()`, `go.set_scale()` e `go.set_scale_xy()`.
:::

*PROPRIEDADES DE COMPONENTE SPRITE*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | O tamanho não escalado do sprite: seu tamanho conforme obtido do atlas de origem. | `vector3` | `get`{.mark} |
| *image* | O hash do caminho da textura do sprite. | `hash` | `get`{.mark}|
| *scale* | Escala não uniforme do sprite. | `vector3` | `get+set`{.mark}|
| *scale.xy* | Escala não uniforme do sprite ao longo dos eixos X e Y. | `vector3` | `get+set`{.mark}|
| *material* | O material usado pelo sprite. | `hash` | `get+set`{.mark}|
| *cursor* | Posição (entre 0--1) do cursor de reprodução. | `number` | `get+set`{.mark}|
| *playback_rate* | A taxa de quadros da animação flipbook. | `number` | `get+set`{.mark}|

*PROPRIEDADES DE COMPONENTE DE OBJETO DE COLISÃO*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | A massa do objeto de colisão. | `number` | `get`{.mark} |
| *linear_velocity* | A velocidade linear atual do objeto de colisão. | `vector3` | `get`{.mark} |
| *angular_velocity* | A velocidade angular atual do objeto de colisão. | `vector3` | `get`{.mark} |
| *linear_damping* | Amortecimento linear do objeto de colisão. | `vector3` | `get+set`{.mark} |
| *angular_damping* | Amortecimento angular do objeto de colisão. | `vector3` | `get+set`{.mark} |

*PROPRIEDADES DE COMPONENTE MODEL (3D)*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | A animação atual.                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | Os hashes dos caminhos das texturas do modelo. | `hash` | `get+set`{.mark}|
| *cursor*  | Posição (entre 0--1) do cursor de reprodução. | `number`   | `get+set`{.mark} |
| *playback_rate* | A taxa de reprodução da animação. Um multiplicador da taxa de reprodução da animação. | `number` | `get+set`{.mark} |
| *material* | O material usado pelo modelo. | `hash` | `get+set`{.mark}|

*PROPRIEDADES DE COMPONENTE LABEL*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | A escala do rótulo. | `vector3` | `get+set`{.mark} |
| *scale.xy* | A escala do rótulo ao longo dos eixos X e Y. | `vector3` | `get+set`{.mark}|
| *color*     | A cor do rótulo. | `vector4` | `get+set`{.mark} |
| *outline* | A cor de contorno do rótulo. | `vector4` | `get+set`{.mark} |
| *shadow* | A cor da sombra do rótulo. | `vector4` | `get+set`{.mark} |
| *size* | O tamanho do rótulo. O tamanho limitará o texto se a quebra de linha estiver habilitada. | `vector3` | `get+set`{.mark} |
| *material* | O material usado pelo rótulo. | `hash` | `get+set`{.mark}|
| *font* | A fonte usada pelo rótulo. | `hash` | `get+set`{.mark}|


## Propriedades de nodes de GUI

Nodes de GUI têm funções getter e setter específicas para cada propriedade, como `gui.get_position()` e `gui.set_position()`. Como alternativa, as propriedades integradas listadas abaixo podem ser lidas e escritas com `gui.get(node, property)` e `gui.set(node, property, value)`. Outros valores de node ainda podem exigir suas funções dedicadas. Constantes de material em nodes de GUI também usam as funções genéricas. Para endereçar um componente de uma propriedade vetorial, acrescente seu nome, por exemplo `gui.set(node, "color.x", 1)`.

As funções genéricas e as funções específicas da propriedade nem sempre usam tipos de valor idênticos. `gui.get()` retorna um `vector4` para as propriedades completas `position`, `scale`, `size` e `euler`, enquanto as funções específicas correspondentes retornam um `vector3`. `gui.set()` aceita um `vector3` ou `vector4` para essas propriedades. A propriedade genérica `rotation` usa um quaternion; use `euler` ao definir a rotação em graus.

* `position` (ou `gui.PROP_POSITION`)
* `rotation` (ou `gui.PROP_ROTATION`)
* `euler` (ou `gui.PROP_EULER`)
* `scale` (ou `gui.PROP_SCALE`)
* `color` (ou `gui.PROP_COLOR`)
* `outline` (ou `gui.PROP_OUTLINE`)
* `shadow` (ou `gui.PROP_SHADOW`)
* `size` (ou `gui.PROP_SIZE`)
* `fill_angle` (ou `gui.PROP_FILL_ANGLE`)
* `inner_radius` (ou `gui.PROP_INNER_RADIUS`)
* `leading` (ou `gui.PROP_LEADING`)
* `tracking` (ou `gui.PROP_TRACKING`)
* `slice9` (ou `gui.PROP_SLICE9`)

Observe que todos os valores de cor são codificados em um `vector4`, onde os componentes correspondem aos valores RGBA:

`x`
: O componente de cor vermelho

`y`
: O componente de cor verde

`z`
: O componente de cor azul

`w`
: O componente alfa

*PROPRIEDADES DE NODE DE GUI*

| propriedade   | descrição                            | tipo            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | A cor da face do node.            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | A cor do contorno do node.         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | A posição do node. | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | A rotação do node. O getter retorna um quaternion; o setter aceita um quaternion ou ângulos de Euler como vetor. | `quaternion`, `vector3` ou `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | A rotação do node expressa como ângulos de Euler em graus. | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | A escala do node expressa como um multiplicador ao longo de cada eixo. | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | A cor da sombra do node. | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | O tamanho não escalado do node. | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | O ângulo de preenchimento de um node pie expresso em graus no sentido anti-horário. | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | O raio interno de um node pie. | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | A escala de espaçamento entre linhas de um node de texto. | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | A escala de espaçamento entre letras de um node de texto. | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | As distâncias das bordas de um node slice9. | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
