---
title: Marcação de texto formatado no Defold
brief: Este manual explica como aplicar estilos a componentes Label e nós de texto de GUI com marcação de texto formatado e como inspecionar links e sprites com Lua.
---

# Marcação de texto formatado {#rich-text-markup}

Use marcação em componentes Label e nós de texto de GUI para aplicar estilos visuais e efeitos aninhados e inspecionar links e sprites com Lua.

```lua
go.set("#label", "text", "Score: <color=#69D2E7>1200</color>")
```

Como alternativa, defina na fonte um estilo de objeto nomeado e reutilizável e selecione-o em um link:

```lua
local fontpath = "/fonts/ui.fontc"
font.set_style(fontpath, "menu_link", "<color=#69D2E7>")
go.set("#label", "text", "Open <link style=menu_link src=inventory>inventory</link>")
```

## Referência de tags {#tag-reference}

| Tag | Finalidade | Exemplo |
| --- | --- | --- |
| [`color`](#color) | Define a cor de preenchimento do glifo. | <img src="/manuals/images/richtext/color_green.webp" alt="Texto verde" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`size`](#size) | Altera a modelagem dos glifos e o tamanho do layout. | <img src="/manuals/images/richtext/size_24.webp" alt="Texto a 24 pixels" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`gradient`](#gradient) | Aplica um gradiente de cores estático ou animado. | <img src="/manuals/images/richtext/gradient_horizontal.webp" alt="Texto com gradiente horizontal" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`ul`](#ul) | Sublinha o texto. | <img src="/manuals/images/richtext/underline_solid.webp" alt="Texto sublinhado" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`strike`](#strike) | Risca o texto. | <img src="/manuals/images/richtext/strike_solid.webp" alt="Texto tachado" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`outline`](#outline) | Define a largura e a cor do contorno do glifo. | <img src="/manuals/images/richtext/outline.webp" alt="Texto com contorno" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shadow`](#shadow) | Adiciona uma sombra ao texto. | <img src="/manuals/images/richtext/shadow.webp" alt="Texto com sombra" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`shake`](#shake) | Aplica um deslocamento aleatório animado. | <img src="/manuals/images/richtext/shake_glyph.webp" alt="Texto tremendo" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`wave`](#wave) | Move o texto em uma onda senoidal animada. | <img src="/manuals/images/richtext/wave_glyph.webp" alt="Texto ondulando" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`sprite`](#sprite) | Adiciona um objeto sprite no meio do texto. | <img src="/manuals/images/richtext/sprite.webp" alt="Sprite inserido no texto" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |
| [`link`](#link) | Adiciona um objeto de link interativo. | <img src="/manuals/images/richtext/link.webp" alt="Texto com link" style="height:1.75em;width:auto;max-width:none;display:inline-block;margin:0;vertical-align:middle;"> |

## Sintaxe {#syntax}

Os nomes de tags e atributos diferenciam maiúsculas de minúsculas. Uma tag com abertura e fechamento se aplica ao texto UTF-32 visível dentro dela. Objetos sprite usam tags que se fecham sozinhas.

```text
<color=#69D2E7>colored text</color>
<ul pattern=dashed>underlined text</ul>
<outline size=2 color=#000000>outlined text</outline>
<shadow x=2 y=-2 color=#00000080>shadowed text</shadow>
<sprite src=images/icon.png width=2em/>
```

### Atributos {#attributes}

Atributos podem ser escritos sem aspas quando não contêm espaços em branco, ou entre aspas simples ou duplas. `color` e `size` aceitam um primeiro valor abreviado, além da forma nomeada `value`.

```text
<color=#FF8800>Orange</color>
<color value="#FF8800">Orange</color>
<size='120%'>Larger</size>
```

### Aninhamento {#nesting}

As tags devem ser fechadas na ordem inversa à de abertura. Os valores de um estilo interno sobrescrevem a mesma propriedade de um estilo externo. Propriedades diferentes se combinam. Os efeitos de cada trecho permanecem ativos de forma independente; portanto, gradientes aninhados multiplicam as cores e efeitos de posição aninhados somam seus deslocamentos.

```text
<color=#FFCC00>
    Gold <outline size=2 color=#000000>with a black outline</outline>
</color>
```

### Entidades {#entities}

Use `&amp;`, `&apos;`, `&gt;`, `&lt;` e `&quot;` para caracteres reservados no texto visível. Entidades numéricas ainda não são aceitas.

## Tags

Tags de texto formatado aplicam estilos a um trecho de texto delimitado ou descrevem um objeto que pode ser inspecionado com Lua. Tags de estilo usam uma tag de fechamento correspondente. O objeto `sprite` se fecha sozinho, enquanto `link` delimita o texto do link.

### `color`

Define a cor de preenchimento do glifo. As cores usam `#RRGGBB` ou `#RRGGBBAA`. O prefixo de cerquilha é obrigatório; `0xFF0000` e `FF0000` são inválidos. O resultado multiplica a cor base do label ou do renderizador.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `=color` ou `value=color` | Sim | Sem padrão | Cor de preenchimento no formato hexadecimal RGB ou RGBA. |

```text
<color=#00FF00>Opaque green</color>
<color=#00FF0080>Half-alpha green</color>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF00*

![Texto de exemplo renderizado em verde opaco](images/richtext/color_green.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*#00FF0080*

![Texto de exemplo renderizado em verde com metade do alfa](images/richtext/color_green_alpha.webp)

</div>
</div>

### `size`

Altera a modelagem dos glifos e o tamanho do layout, não apenas a escala dos vértices. Valores relativos sempre usam o tamanho base da fonte do layout. Eles não se acumulam com uma tag `size` externa.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `=size` ou `value=size` | Sim | Sem padrão | Tamanho absoluto, porcentagem, múltiplo do tamanho base ou deslocamento com sinal em relação ao tamanho base, usando uma das formas abaixo. |

| Forma | Exemplo a 32 px | Tamanho resolvido |
| --- | --- | --- |
| Número sem unidade ou `px` | `24`, `24px` | 24 px |
| Porcentagem do tamanho base | `120%` | 38.4 px |
| Múltiplo do tamanho base | `2em` | 64 px |
| Deslocamento com sinal em relação ao tamanho base | `+4`, `-4` | 36 px, 28 px |

```text
<size=24px>Exactly 24 pixels</size>
<size=120%>120% of the layout base size</size>
<size=2em>Twice the layout base size</size>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*24px*

![Texto de exemplo renderizado a 24 pixels](images/richtext/size_24.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*120% de 32px*

![Texto de exemplo renderizado a 120 por cento de 32 pixels](images/richtext/size_120.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*2em de 32px*

![Texto de exemplo renderizado ao dobro do tamanho base de 32 pixels](images/richtext/size_2em.webp)

</div>
</div>

### `gradient`

Um gradiente aceita exatamente um conjunto completo de atributos. Misturar conjuntos ou omitir um membro é inválido.

| Modo | Atributos obrigatórios | Interpolação |
| --- | --- | --- |
| Horizontal | `left`, `right` | Interpola entre as duas cores horizontais. |
| Vertical | `bottom`, `top` | Interpola entre as cores inferior e superior. |
| Quatro cantos | `tl`, `tr`, `bl`, `br` | Interpola entre as cores dos quatro vértices. |

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `left`, `right` | No modo horizontal | Nenhum | Cores das extremidades horizontais no formato `#RRGGBB` ou `#RRGGBBAA`. Ambas devem estar presentes. |
| `bottom`, `top` | No modo vertical | Nenhum | Cores das extremidades verticais. Ambas devem estar presentes. |
| `tl`, `tr`, `bl`, `br` | No modo de quatro cantos | Nenhum | Cores dos cantos superior esquerdo, superior direito, inferior esquerdo e inferior direito. As quatro devem estar presentes. |
| `fit` | Não | `span` | `glyph` amostra cada posição de texto modelado; `span` distribui o gradiente por todo o texto delimitado pela tag. |
| `hz` | Não | `0` | Ciclos completos de fluxo por segundo em `[0,)`; zero mantém o gradiente estático. |
| `direction` | Não | `forward` | `forward` ou `reverse`. Controla a direção do fluxo quando `hz` é diferente de zero. |

Quando `fit` é omitido, `fit=span` distribui o gradiente por todo o texto delimitado pela tag. `fit=glyph` amostra cada posição de texto modelado de forma independente. O atributo opcional `hz` especifica os ciclos completos de animação de fluxo por segundo; seu padrão zero mantém o gradiente estático. A rampa de cores espelhada e repetida flui continuamente e reinicia sem saltos de cor. `direction=forward` é o padrão; use `direction=reverse` para inverter o fluxo.

```text
<gradient left=#FF00FF right=#FFFFFF>Horizontal Gradient</gradient>

<gradient hz=0.25 fit=glyph bottom=#182848 top=#4B6CB7>Animated vertical glyphs</gradient>

<gradient hz=0.25 direction=reverse left=#FF0000 right=#0000FF>Reverse flow</gradient>

<gradient hz=0.25 direction=reverse fit=span left=#FF0000 right=#0000FF>One animated span color</gradient>

<gradient fit=glyph tl=#FF0000 tr=#00FF00 bl=#0000FF br=#FFFFFF>
    Four corners
</gradient>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Horizontal*

![Texto de exemplo com um gradiente horizontal de magenta a branco](images/richtext/gradient_horizontal.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Vertical*

![Texto de exemplo com um gradiente azul vertical](images/richtext/gradient_vertical.webp)

</div>
</div>

**Quatro cantos**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de exemplo com um gradiente de quatro cantos ajustado a cada glifo](images/richtext/gradient_four_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de exemplo com um gradiente de quatro cantos ajustado ao trecho](images/richtext/gradient_four_text.webp)

</div>
</div>

**Animado**

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Gradiente de fluxo animado ajustado a cada glifo](images/richtext/gradient_flow_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Gradiente de fluxo animado ajustado ao trecho](images/richtext/gradient_flow_span.webp)

</div>
</div>

As cores do gradiente multiplicam a cor de preenchimento atual. Portanto, um gradiente dentro de `color=#808080` não pode produzir um canal mais brilhante que esse multiplicador base.

### `ul`

Desenha um sublinhado usando as métricas de sublinhado da fonte quando disponíveis. A tag não tem uma cor independente: a linha herda a cor de preenchimento efetiva, incluindo gradientes horizontais, verticais e de quatro cantos.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `pattern` | Não | `solid` | `solid` ou `dashed`. |

```text
<ul>Solid underline</ul>
<ul pattern=dashed>Dashed underline</ul>
<ul><gradient left=#FF00FF right=#FFFFFF>Gradient line</gradient></ul>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contínuo*

![Texto de exemplo com sublinhado contínuo](images/richtext/underline_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tracejado*

![Texto de exemplo com sublinhado tracejado](images/richtext/underline_dashed.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Gradiente*

![Texto de exemplo com sublinhado em gradiente](images/richtext/underline_gradient.webp)

</div>
</div>

### `strike`

Desenha uma linha sobre o texto delimitado. Aceita os mesmos valores de `pattern` que `ul` e também herda a cor de preenchimento efetiva.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `pattern` | Não | `solid` | `solid` ou `dashed`. |

```text
<strike>No longer available</strike>
<strike pattern=dashed>Dashed strikethrough</strike>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contínuo*

![Texto de exemplo com tachado contínuo](images/richtext/strike_solid.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Tracejado*

![Texto de exemplo com tachado tracejado](images/richtext/strike_dashed.webp)

</div>
</div>

### `outline`

Define a largura do contorno, sua cor ou ambas. Pelo menos um atributo é obrigatório. Uma largura zero desativa explicitamente o contorno do trecho.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `size` | Um entre size/color | Herdado; `0` em uma fonte padrão | Largura em unidades de layout, intervalo `[0,)`. Sufixos de unidade não são aceitos. |
| `color` | Um entre size/color | Herdado; `#000000` em um label padrão | Uma única cor de contorno no formato hexadecimal RGB (`#RRGGBB`) ou RGBA (`#RRGGBBAA`); o componente alfa controla a opacidade. |

```text
<outline size=3 color=#000000>Black outline</outline>
<outline color=#FF0000>Keep inherited width, change color</outline>
<outline size=0>Disable inherited outline</outline>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Contorno preto externo*

![Texto de exemplo com contorno preto externo](images/richtext/outline.webp)

</div>
</div>

### `shadow`

Adiciona uma sombra de bordas nítidas ao texto delimitado. Pelo menos um atributo é obrigatório. Atributos omitidos por uma tag aninhada mantêm o valor da sombra externa; atributos omitidos pela tag mais externa mantêm o valor base da sombra da fonte.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `color` | Não | Herdado; `#000000` em um label padrão | Cor da sombra no formato `#RRGGBB` ou `#RRGGBBAA`. |
| `x` | Não | Herdado; `0` em uma fonte padrão | Deslocamento horizontal da sombra em unidades de layout. Valores positivos a movem para a direita. |
| `y` | Não | Herdado; `0` em uma fonte padrão | Deslocamento vertical da sombra em unidades de layout. Valores positivos a movem para cima. |
| `blur` | Não | Herdado; `0` em uma fonte padrão | Raio de desfoque em unidades de layout, intervalo `[0,)`. |

```text
<shadow x=6 y=-6 blur=4 color=#000000A0>Shadow</shadow>
<shadow x=-2>Override only the horizontal offset</shadow>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*x=6, y=-6, blur=4*

![Texto de exemplo com uma sombra deslocada](images/richtext/shadow.webp)

</div>
</div>

::: sidenote
O desfoque da sombra é gerado e armazenado no atlas de glifos. Um trecho pode solicitar um desfoque menor que o pré-calculado na fonte; valores maiores são preservados no layout, mas atualmente são renderizados usando o maior desfoque disponível no atlas.
:::

### `shake`

Aplica um deslocamento aleatório animado e determinístico sem alterar a quebra de linhas nem os limites do layout. O efeito controla o tempo internamente; os scripts não precisam modificar o texto do label a cada frame da animação.

| Atributo | Obrigatório | Padrão | Valores válidos | Significado |
| --- | --- | --- | --- | --- |
| `hz` | Não | 20 | `[0,)` | Transições para alvos aleatórios por segundo. Zero pausa o efeito. |
| `amplitude` | Não | 0.5 | `[0,)` | Deslocamento máximo em unidades de layout. |
| `fit` | Não | `glyph` | `glyph` ou `span` | `glyph` amostra um deslocamento que preserva os agrupamentos para cada unidade de glifo modelado. `span` move todo o trecho delimitado pela tag como uma unidade rígida. |

```text
<shake>Default shake</shake>
<shake hz=12 amplitude=0.8 fit=glyph>Glyph shake</shake>
<shake hz=12 amplitude=0.8 fit=span>Rigid span shake</shake>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de exemplo com tremor animado por glifo](images/richtext/shake_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de exemplo com tremor animado do trecho inteiro](images/richtext/shake_span.webp)

</div>
</div>

### `wave`

Move os caracteres para cima e para baixo em uma onda senoidal animada sem alterar a quebra de linhas nem os limites do layout. O layout acumula o tempo de animação quando é atualizado.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `amplitude` | Não | 1 | Deslocamento vertical máximo em unidades de layout, intervalo `[0,)`. |
| `hz` | Não | 1 | Ciclos temporais completos por segundo, intervalo `[0,)`. Zero pausa a onda. |
| `wavelength` | Não | 6 | Posições de texto UTF-32 visível por ciclo espacial completo, intervalo `[1,)`. Caracteres que a fonte modela juntos, como um caractere base e seu acento combinante, movem-se como uma unidade. |
| `fit` | Não | `glyph` | `glyph` aplica a onda espacial ao longo do texto. `span` atribui a todo o trecho delimitado pela tag um único deslocamento senoidal vertical compartilhado. |
| `direction` | Não | `forward` | `forward` avança normalmente. `reverse` inverte a direção de propagação da onda. |

```text
<wave>Animated character wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph>Travelling wave</wave>
<wave amplitude=4 hz=3 wavelength=8 fit=glyph direction=reverse>Reverse travelling wave</wave>
<wave amplitude=4 hz=1 fit=span>Whole span moves together</wave>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=glyph`*

![Texto de exemplo com onda animada por glifo](images/richtext/wave_glyph.webp)

</div>
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`fit=span`*

![Texto de exemplo movendo-se como um único trecho animado](images/richtext/wave_span.webp)

</div>
</div>

### `sprite`

Adiciona um objeto sprite com fechamento próprio na posição atual do texto visível. Seus atributos são preservados como metadados para `label.get_layout_objects()` e `gui.get_layout_objects()`.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `id` | Não | Gerado | Identificador estável convertido em hash no campo `id` do objeto de layout retornado. |
| `src` | Não | Nenhum | Identificador de recurso de sprite definido pela aplicação, como um caminho de imagem ou atlas do projeto. |
| `animation` | Não | Nenhum | Identificador de animação definido pela aplicação dentro do recurso. |
| `width` | Não | `1em` | Largura resolvida do sprite. |
| `height` | Não | `1em` | Altura resolvida do sprite. |
| Qualquer outro atributo | Não | Ausente | Metadados definidos pela aplicação, preservados para o resolvedor de objetos e as APIs de objetos de layout. |

```text
A <sprite src=engine/engine/content/builtins/assets/images/logo/logo_256.png/> logo
<sprite src=images/banner.png width=4em height=2em/>
<sprite src=images/icons.atlas animation=coin width=2em/>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*Sprite resolvido inserido no texto*

![Um logotipo do Defold renderizado junto ao texto](images/richtext/sprite.webp)

</div>
</div>

As dimensões aceitam valores positivos em unidades de layout sem sufixo, `px`, `em` ou `%`. Tanto `em` quanto `%` usam o tamanho base da fonte do layout de texto.

Cada dimensão ausente assume `1em` de forma independente. Omitir ambas produz um objeto de `1em × 1em`; especificar somente a largura não calcula a altura automaticamente a partir da proporção do recurso.

::: important
A tag sprite é apenas um espaço reservado para o desenvolvedor inserir qualquer objeto naquele lugar!
:::

### `link`

Descreve um intervalo de texto visível como um objeto de link. O texto delimitado é disposto normalmente e recebe o estilo nomeado `link` por padrão. Componentes Label e GUI selecionam `link:hover` e `link:active` em resposta à entrada, sem remodelar o texto. Consulte [mensagens de interação](#interaction-messages) para saber quais mensagens são produzidas pela entrada nos links.

| Atributo | Obrigatório | Padrão | Significado |
| --- | --- | --- | --- |
| `src` | Não | Nenhum | Destino do link definido pela aplicação. O valor é retornado como string sem validação ou navegação automática. |
| `id` | Não | Gerado | Identificador estável convertido em hash no campo `id` do objeto de layout retornado. |
| `style` | Não | `link` | Estilo padrão nomeado para o texto do link. |
| Qualquer outro atributo | Não | Ausente | Metadados definidos pela aplicação, como identificador, ação, dica de ferramenta ou valor de análise. |

```text
<ul><link id=website src=https://www.defold.com>www.defold.com</link></ul>
<link id=inventory style=menu_link action=open_inventory item=sword>Iron sword</link>
```

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;margin:1rem 0 2rem;" markdown="1">
<div style="flex:1 1 280px;max-width:426px;" markdown="1">

*`style=link`*

![www.defold.com renderizado com o estilo padrão de link e um sublinhado](images/richtext/link.webp)

</div>
</div>

O componente acompanha o estado do ponteiro em cada link. Aplica `link:hover` enquanto o ponteiro está sobre o link e `link:active` enquanto o botão está pressionado. Quando nenhum dos estados se aplica, o componente restaura o estilo nomeado pelo atributo `style` do link, ou `link` quando o atributo está ausente.

### Mensagens de interação {#interaction-messages}

A interação com links usa o sistema normal de entrada do Defold. Adicione uma associação Mouse Trigger para `MOUSE_BUTTON_LEFT`, que também ativa a entrada por toque único, e adquira o foco de entrada no script do objeto de jogo ou no script de GUI:

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end
```

Consulte [foco de entrada](/manuals/input/#input-focus) e [entrada de mouse e toque](/manuals/input-mouse-and-touch) para saber como configurar.

Quando um componente Label ou GUI recebe entrada do ponteiro, os links produzem as mensagens a seguir. As mensagens de Label são enviadas ao objeto de jogo que o contém; as mensagens de GUI são enviadas ao script de GUI.

| Mensagem | Quando é enviada |
| --- | --- |
| `text_object_hovered` | O ponteiro entra em um link. |
| `text_object_unhovered` | O ponteiro sai de um link. |
| `text_object_clicked` | O botão é solto sobre o mesmo link em que foi pressionado. |

Cada mensagem contém estes campos:

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `id` | `hash` | O atributo `id` do objeto ou seu id de objeto de layout gerado. |
| `type` | `hash` | O tipo do objeto de layout, atualmente `hash("link")`. |
| `src` | `string` | O valor do atributo `src` do objeto definido pela aplicação, ou uma string vazia quando ausente. |

```lua
function on_message(self, message_id, message)
    if message_id == hash("text_object_clicked") then
        assert(message.type == hash("link"))
        print(message.id, message.src)
    end
end
```

## Estilos nomeados {#named-styles}

Cada coleção de fontes contém estilos de objeto nomeados que afetam apenas a renderização. Um link usa o estilo nomeado pelo atributo `style`, ou `link` quando o atributo está ausente. Não existe uma tag geral `<style>` para trechos de texto.

O Defold fornece os seguintes padrões:

| Estilo | Multiplicador da cor de preenchimento | Decoração |
| --- | --- | --- |
| `link` | `(0.10, 0.45, 0.90, 1.0)` | Sublinhado contínuo |
| `link:hover` | `(0.30, 0.65, 1.00, 1.0)` | Nenhuma |
| `link:active` | `(0.05, 0.30, 0.70, 1.0)` | Nenhuma |

Defina um estilo com uma string de texto contendo tags de abertura. As tags são fechadas implicitamente na ordem inversa; portanto, tags de fechamento e texto visível não são permitidos.

```lua
font.set_style("/fonts/ui.fontc", "link",
    "<color=#2673ff><outline color=#000000 size=1>")

font.set_style("/fonts/ui.fontc", "link:hover",
    "<color=#66b3ff><shake amplitude=0.2 hz=20>")
```

As tags são aplicadas da esquerda para a direita, como se estivessem aninhadas ao redor do texto do objeto. Um estilo de objeto selecionado pelo código chamador é aplicado após o estilo padrão. Quando várias tags definem a mesma propriedade de renderização, o valor aplicado depois sobrescreve os anteriores. Os efeitos são acrescentados na ordem da esquerda para a direita.

::: sidenote
Chamar `font.set_style()` substitui as propriedades de renderização e os efeitos desse estilo nomeado. As decorações definidas pelo recurso permanecem iguais; portanto, redefinir `link` não remove seu sublinhado padrão. Estilos nomeados aceitam tags que afetam apenas a renderização, como `color`, `outline`, `shadow`, `gradient`, `wave` e `shake`. Tags que alteram o layout, de decoração e de objetos são rejeitadas.
:::

## API de objetos de layout {#layout-object-api}

Use `label.get_layout_objects()` ou `gui.get_layout_objects()` para obter os objetos `sprite` e `link` do texto já disposto.

### `label.get_layout_objects()`

```lua
objects = label.get_layout_objects(url)
```

| Argumento | Tipo | Descrição |
| --- | --- | --- |
| `url` | `string`, `hash` ou `url` | O componente Label a inspecionar, por exemplo `"#label"`. |

### `gui.get_layout_objects()`

```lua
objects = gui.get_layout_objects(node)
```

| Argumento | Tipo | Descrição |
| --- | --- | --- |
| `node` | `node` | O nó de texto de GUI a inspecionar, por exemplo `gui.get_node("rich_text")`. |

Ambas as funções retornam um array recém-criado contendo os objetos atuais do layout na ordem do texto-fonte. Retornam um array vazio quando o texto não contém tags de objeto. Como os objetos e seus atributos são copiados para Lua a cada chamada, mantenha o resultado em cache e consulte novamente após alterar o texto ou outra propriedade que mude seu layout.

### Campos do objeto retornado {#returned-object-fields}

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `type` | `string` | `"sprite"` ou `"link"`. |
| `id` | `hash` | Identificador de objeto usado nas mensagens de interação. |
| `text_offset` | `number` | Posição a partir de zero no texto visível, medida em pontos de código Unicode. A marcação é excluída e as entidades contam como seus caracteres decodificados. Para um sprite, esta é sua posição de inserção. |
| `text_length` | `number` | Comprimento do texto visível delimitado em pontos de código Unicode. Um sprite tem comprimento um por causa do ponto de código de substituição de objeto U+FFFC inserido. |
| `width` | `number` | Largura resolvida em unidades de layout de texto. Links atualmente têm largura zero. |
| `height` | `number` | Altura resolvida em unidades de layout de texto. Links atualmente têm altura zero. |
| `x` | `number` | Posição horizontal do canto inferior esquerdo do objeto em relação à origem superior esquerda do layout de texto. |
| `y` | `number` | Posição vertical do canto inferior esquerdo do objeto em relação à origem superior esquerda do layout de texto. |
| `attributes` | `table` | Todos os atributos da tag como pares de chave/valor de strings. Os valores dos atributos mantêm sua representação original, como `"2em"`. Um valor abreviado sem nome é armazenado sob a chave `value`. |

::: sidenote
`text_offset` e `text_length` não são deslocamentos em bytes UTF-8. Um caractere não ASCII, como `å` ou `猫`, conta como uma posição.
:::

### Exemplo em Lua {#lua-example}

```lua
local text = [[
Read the <link src=https://defold.com/manuals/ id=manual>manual</link>
or inspect <sprite src=images/info.png width=2em/> for more information.
]]

go.set("#label", "text", text)

local objects = label.get_layout_objects("#label")
for _, object in ipairs(objects) do
    if object.type == "link" then
        print("link", object.attributes.src)
        print("visible range", object.text_offset, object.text_length)
        print("position", object.x, object.y)
    elseif object.type == "sprite" then
        print("sprite", object.x, object.y, object.width, object.height)
        pprint(object.attributes)
    end
end

local gui_objects = gui.get_layout_objects(gui.get_node("rich_text"))
```

## Combinações úteis {#useful-combinations}

### Contorno colorido com gradiente horizontal {#colored-outline-with-a-horizontal-gradient}

```text
<outline size=2 color=#101820>
    <gradient left=#FEE715 right=#FF6F61>Gradient title</gradient>
</outline>
```

O gradiente multiplica apenas a cor de preenchimento; o contorno mantém sua própria cor.

### Tremer uma frase e aplicar gradiente a uma palavra {#shake-a-sentence-gradient-one-word}

```text
<shake hz=20 amplitude=0.5>
    This <gradient left=#FF00FF right=#FFFFFF>whole</gradient> text shakes!
</shake>
```

O efeito de posição externo se aplica a cada glifo. O efeito de cor aninhado se aplica somente a “whole”.

### Sobrescrever uma propriedade sem perder as outras {#override-one-property-without-losing-the-others}

```text
<color=#FFFFFF><outline size=2 color=#000000>
    Normal <color=#FF4040>warning</color> normal
</outline></color>
```

A cor interna altera o preenchimento, preservando a largura e a cor do contorno herdadas.
