---
title: Cenas GUI no Defold
brief: Este manual percorre o editor GUI do Defold, os vários tipos de nodes GUI e scripting de GUI.
---

# GUI

O Defold fornece um editor GUI personalizado e recursos poderosos de scripting, feitos sob medida para a construção e implementação de interfaces de usuário.

Uma interface gráfica de usuário no Defold é um componente que você constrói, anexa a um objeto de jogo e coloca em uma coleção. Esse componente tem as seguintes propriedades:

* Ele tem recursos de layout simples, mas poderosos, que permitem renderizar sua interface de usuário independentemente da resolução e da proporção de tela.
* Ele pode ter comportamento lógico anexado por meio de um *script de GUI*.
* Ele é (por padrão) renderizado sobre outros conteúdos, independentemente da visão da câmera; portanto, mesmo que você tenha uma câmera em movimento, seus elementos de GUI permanecerão fixos na tela. O comportamento de renderização pode ser alterado.

Componentes GUI são renderizados independentemente da visualização do jogo. Por isso, eles não são colocados em um local específico no editor de coleção, nem têm uma representação visual no editor de coleção. No entanto, componentes GUI precisam residir em um objeto de jogo que tenha uma localização em uma coleção. Alterar essa localização não tem efeito sobre a GUI.

## Criando um componente GUI

Componentes GUI são criados a partir de um arquivo de protótipo de cena GUI (também conhecido como "prefab" ou "blueprint" em outras engines). Para criar um novo componente GUI, clique com o botão direito em um local no navegador *Assets* e selecione <kbd>New ▸ Gui</kbd>. Digite um nome para o novo arquivo GUI e pressione <kbd>Ok</kbd>.

![Novo arquivo GUI](images/gui/new_gui_file.png)

O Defold agora abre automaticamente o arquivo no editor de cenas GUI.

![Nova GUI](images/gui/new_gui.png)

O *Outline* lista todo o conteúdo da GUI: sua lista de nodes e quaisquer dependências (veja abaixo).

A área central de edição mostra a GUI. A barra de ferramentas no canto superior direito da área de edição contém as ferramentas *Move*, *Rotate* e *Scale*, além de um seletor de [layout](/manuals/gui-layouts).

![barra de ferramentas](images/gui/toolbar.png)

Um retângulo branco mostra os limites do layout selecionado atualmente, ou da largura e altura de exibição padrão conforme definido nas configurações do projeto.

## Propriedades da Gui

Selecionar o node raiz "Gui" no *Outline* mostra as *Properties* do componente GUI:

*Script*
: O script de GUI vinculado a este componente GUI.

*Material*
: O material usado ao renderizar esta GUI. Observe que também é possível adicionar vários materiais a uma Gui pelo painel *Outline* e atribuí-los a nodes individuais.

*Adjust Reference*
: Controla como o *Adjust Mode* de cada node deve ser calculado:

  - `Per Node` ajusta cada node em relação ao tamanho ajustado do node pai, ou à tela redimensionada.
  - `Disable` desativa o modo de ajuste de node. Isso força todos os nodes a manterem seu tamanho definido.

*Current Nodes*
: O número de nodes atualmente usados nesta GUI.

*Max Nodes*
: O número máximo de nodes para esta GUI.

*Max Dynamic Textures*
: O número máximo de texturas dinâmicas rastreadas por este componente GUI, `128` por padrão. Isso inclui texturas criadas com [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) e texturas externas atribuídas à GUI com `go.set(..., "textures", ...)` ou `gui.set(msg.url(), "textures", ...)`. Projetos que substituem muitas texturas externas talvez precisem aumentar esse limite.


## Manipulação em runtime

Você pode manipular propriedades de GUI em runtime a partir de um componente de script usando `go.get()` e `go.set()`:

Fontes
: Obtém ou define uma fonte usada em uma GUI.

![get_set_font](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- obtém o arquivo de fonte atualmente atribuído à fonte com id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- define a fonte com id 'default' para o arquivo de fonte atribuído à propriedade de recurso 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- obtém o novo arquivo de fonte atribuído à fonte com id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materiais
: Obtém ou define um material usado em uma GUI.

![get_set_material](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- obtém o arquivo de material atualmente atribuído ao material com id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- define o id de material 'effect' para o arquivo de material atribuído à propriedade de recurso 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- obtém o novo arquivo de material atribuído ao material com id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Texturas
: Obtém ou define uma textura (atlas) usada em uma GUI.

![get_set_texture](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- obtém o arquivo de textura atualmente atribuído à textura com id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- define a textura com id 'theme' para o arquivo de textura atribuído à propriedade de recurso 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- obtém o novo arquivo de textura atribuído à textura com id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Dependências

A árvore de recursos em um jogo Defold é estática, então quaisquer dependências necessárias para seus nodes GUI precisam ser adicionadas ao componente. O *Outline* agrupa todas as dependências por tipo sob "pastas":

![dependências](images/gui/dependencies.png)

Para adicionar uma nova dependência, arraste-a e solte-a do painel *Asset* para a visualização do editor.

Como alternativa, clique com o botão direito na raiz "Gui" no *Outline* e selecione <kbd>Add ▸ [type]</kbd> no menu de contexto popup.

Você também pode clicar com o botão direito no ícone da pasta do tipo que deseja adicionar e selecionar <kbd>Add ▸ [type]</kbd>.

## Tipos de node {#node-types}

Um componente GUI é construído a partir de um conjunto de nodes. Nodes são elementos simples. Eles podem ser transladados (movidos, escalados e rotacionados) e organizados em hierarquias pai-filho, seja no editor ou em runtime por scripting. Existem os seguintes tipos de node:

Box node
: ![box node](images/icons/gui-box-node.png){.left}
  Node retangular com uma única cor, textura ou animação flip-book. Consulte a [documentação de Box node](/manuals/gui-box) para detalhes.

<div style="clear: both;"></div>

Text node
: ![text node](images/icons/gui-text-node.png){.left}
  Exibe texto. Consulte a [documentação de Text node](/manuals/gui-text) para detalhes.

<div style="clear: both;"></div>

Pie node
: ![pie node](images/icons/gui-pie-node.png){.left}
  Um node circular ou elipsoidal que pode ser parcialmente preenchido ou invertido. Consulte a [documentação de Pie node](/manuals/gui-pie) para detalhes.

<div style="clear: both;"></div>

Template node
: ![template node](images/icons/gui.png){.left}
  Templates são usados para criar instâncias baseadas em outros arquivos de cena GUI. Consulte a [documentação de Template node](/manuals/gui-template) para detalhes.

<div style="clear: both;"></div>

ParticleFX node
: ![particlefx node](images/icons/particlefx.png){.left}
  Reproduz um efeito de partículas. Consulte a [documentação de ParticleFX node](/manuals/gui-particlefx) para detalhes.

<div style="clear: both;"></div>

Adicione nodes clicando com o botão direito na pasta *Nodes* e selecionando <kbd>Add ▸</kbd> e então <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> ou <kbd>ParticleFx</kbd>.

![Adicionar nodes](images/gui/add_node.png)

Você também pode pressionar <kbd>A</kbd> e selecionar o tipo que deseja adicionar à GUI.

## Propriedades dos nodes {#node-properties}

Cada node tem um conjunto extenso de propriedades que controlam sua aparência:

Id
: A identidade do node. Esse nome precisa ser único dentro da cena GUI.

Position, Rotation and Scale
: Controlam a localização, orientação e alongamento do node. Você pode usar as ferramentas *Move*, *Rotate* e *Scale* para alterar esses valores. Os valores podem ser animados por script ([saiba mais](/manuals/property-animation)).

Size (box, text and pie nodes)
: O tamanho do node é automático por padrão, mas ao definir *Size Mode* como `Manual`, você pode alterar o valor. O tamanho define os limites do node e é usado ao fazer picking de entrada. Esse valor pode ser animado por script ([saiba mais](/manuals/property-animation)).

Size Mode (box and pie nodes)
: Se definido como `Automatic`, o editor definirá um tamanho para o node. Se definido como `Manual`, você pode definir o tamanho por conta própria.

Enabled
: Se desmarcado, o node não é renderizado, não é animado e não pode ser escolhido usando `gui.pick_node()`. Use `gui.set_enabled()` e `gui.is_enabled()` para alterar e verificar essa propriedade programaticamente.

Visible
: Se desmarcado, o node não é renderizado, mas ainda pode ser animado e escolhido usando `gui.pick_node()`. Use `gui.set_visible()` e `gui.get_visible()` para alterar e verificar essa propriedade programaticamente.

Text (text nodes)
: O texto a exibir no node.

Line Break (text nodes)
: Defina para que o texto quebre de acordo com a largura do node.

Font (text nodes)
: A fonte a usar ao renderizar o texto.

Texture (box and pie nodes)
: A textura a desenhar no node. Esta é uma referência a uma imagem ou animação em um atlas ou tile source.

Material (box, pie nodes, text and particlefx nodes)
: O material a usar ao desenhar o node. Pode ser um material adicionado à seção Materials do *Outline* ou deixado em branco para usar o material padrão atribuído ao componente GUI.

Slice 9 (box nodes)
: Defina para preservar o tamanho em pixels da textura do node ao redor das bordas quando o node for redimensionado. Consulte a [documentação de Box node](/manuals/gui-box) para detalhes.

Inner Radius (pie nodes)
: O raio interno do node, expresso ao longo do eixo X. Consulte a [documentação de Pie node](/manuals/gui-pie) para detalhes.

Outer Bounds (pie nodes)
: Controla o comportamento dos limites externos. Consulte a [documentação de Pie node](/manuals/gui-pie) para detalhes.

Perimeter Vertices (pie nodes)
: O número de segmentos que será usado para construir a forma. Consulte a [documentação de Pie node](/manuals/gui-pie) para detalhes.

Pie Fill Angle (pie nodes)
: Quanto da fatia deve ser preenchido. Consulte a [documentação de Pie node](/manuals/gui-pie) para detalhes.

Template (template nodes)
: O arquivo de cena GUI a usar como template para o node. Consulte a [documentação de Template node](/manuals/gui-template) para detalhes.

ParticleFX (particlefx nodes)
: O efeito de partículas a usar neste node. Consulte a [documentação de ParticleFX node](/manuals/gui-particlefx) para detalhes.

Color
: A cor do node. Se o node tiver textura, a cor tinge a textura. A cor pode ser animada por script ([saiba mais](/manuals/property-animation)).

Alpha
: A translucidez do node. O valor alpha pode ser animado por script ([saiba mais](/manuals/property-animation)).

Inherit Alpha
: Marcar esta caixa faz um node herdar o valor alpha do node pai. O valor alpha do node é então multiplicado pelo valor alpha do pai.

Leading (text nodes)
: Um número de escala para o espaçamento entre linhas. Um valor de `0` significa sem espaçamento entre linhas. `1` (o padrão) é espaçamento normal entre linhas.

Tracking (text nodes)
: Um número de escala para o espaçamento entre letras. O padrão é 0.

Layer
: Atribuir uma layer ao node sobrescreve a ordem normal de desenho e, em vez disso, segue a ordem das layers. Veja abaixo os detalhes.

Blend mode
: Controla como os gráficos do node são mesclados com os gráficos de fundo:
  - `Alpha` mescla por alpha os valores de pixel do node com o fundo. Isso corresponde ao modo de mesclagem "Normal" em softwares gráficos.
  - `Add` adiciona os valores de pixel do node ao fundo. Isso corresponde a "Linear dodge" em alguns softwares gráficos.
  - `Multiply` multiplica os valores de pixel do node com o fundo.
  - `Screen` multiplica inversamente os valores de pixel do node com o fundo. Isso corresponde ao modo de mesclagem "Screen" em softwares gráficos.

Pivot
: Define o ponto de pivô do node. Isso pode ser visto como o "ponto central" do node. Qualquer rotação, escala ou mudança de tamanho acontecerá ao redor desse ponto.

  Os valores possíveis são `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` ou `South East`.

  ![ponto de pivô](images/gui/pivot.png)

  Se você alterar o pivô de um node, o node será movido para que o novo pivô fique na posição do node. Nodes de texto são alinhados de modo que `Center` define texto centralizado, `West` define texto alinhado à esquerda e `East` define texto alinhado à direita.

X Anchor, Y Anchor
: Ancoragem controla como a posição vertical e horizontal do node é alterada quando os limites da cena, ou os limites do node pai, são esticados para caber no tamanho físico da tela.

  ![Âncora sem ajuste](images/gui/anchoring_unadjusted.png)

  Os seguintes modos de ancoragem estão disponíveis:

  - `None` (tanto para *X Anchor* quanto para *Y Anchor*) mantém a posição do node a partir do centro do node pai ou da cena, relativa ao seu tamanho *ajustado*.
  - `Left` ou `Right` (*X Anchor*) escala a posição horizontal do node para que ele mantenha a posição a partir das bordas esquerda e direita do node pai ou da cena na mesma porcentagem.
  - `Top` ou `Bottom` (*Y Anchor*) escala a posição vertical do node para que ele mantenha a posição a partir das bordas superior e inferior do node pai ou da cena na mesma porcentagem.

  ![Ancoragem](images/gui/anchoring.png)

Adjust Mode
: Define o modo de ajuste do node. A configuração de modo de ajuste controla o que acontece com um node quando os limites da cena, ou os limites do node pai, são ajustados para caber no tamanho físico da tela.

  Um node criado em uma cena cuja resolução lógica é uma resolução típica de paisagem:

  ![Sem ajuste](images/gui/unadjusted.png)

  Ajustar a cena a uma tela em retrato faz com que a cena seja esticada. A caixa delimitadora de cada node é esticada de forma semelhante. Porém, ao definir o modo de ajuste, a proporção do conteúdo do node pode ser preservada. Os seguintes modos estão disponíveis:

  - `Fit` escala o conteúdo do node para que seja igual à largura ou altura da caixa delimitadora esticada, o que for menor. Em outras palavras, o conteúdo caberá dentro da caixa delimitadora esticada do node.
  - `Zoom` escala o conteúdo do node para que seja igual à largura ou altura da caixa delimitadora esticada, o que for maior. Em outras palavras, o conteúdo cobrirá totalmente a caixa delimitadora esticada do node.
  - `Stretch` estica o conteúdo do node para preencher a caixa delimitadora esticada do node.

  ![Modos de ajuste](images/gui/adjusted.png)

  Se a propriedade de cena GUI *Adjust Reference* estiver definida como `Disabled`, essa configuração será ignorada.

Clipping Mode (box and pie nodes)
: Define o modo de clipping no node:

  - `None` renderiza o node normalmente.
  - `Stencil` faz os limites do node definirem uma máscara stencil usada para recortar os nodes filhos do node.

  Consulte o [manual de clipping de GUI](/manuals/gui-clipping) para detalhes.

Clipping Visible (box and pie nodes)
: Defina para renderizar o conteúdo do node na área de stencil. Consulte o [manual de clipping de GUI](/manuals/gui-clipping) para detalhes.

Clipping Inverted (box and pie nodes)
: Inverte a máscara stencil. Consulte o [manual de clipping de GUI](/manuals/gui-clipping) para detalhes.


## Pivot, Anchors e Adjust Mode

A combinação das propriedades Pivot, Anchors e Adjust Mode permite um design de GUIs muito flexível, mas pode ser um pouco difícil entender como tudo funciona sem observar um exemplo concreto. Vamos usar como exemplo este mockup de GUI criado para uma tela 640x1136:

![](images/gui/adjustmode_example_original.png)

A UI foi criada com X e Y Anchors definidos como None, e o Adjust Mode de cada node foi deixado no valor padrão Fit. O ponto Pivot do painel superior é North, o pivô do painel inferior é South e o ponto Pivot das barras no painel superior está definido como West. O restante dos nodes tem pontos de pivô definidos como Center. Se redimensionarmos a janela para deixá-la mais larga, isto acontece:

![](images/gui/adjustmode_example_resized.png)

Agora, e se quisermos que as barras superior e inferior tenham sempre a mesma largura da tela? Podemos alterar o Adjust Mode dos painéis de fundo cinza no topo e na parte inferior para Stretch:

![](images/gui/adjustmode_example_resized_stretch.png)

Isso é melhor. Os painéis de fundo cinza agora sempre serão esticados até a largura da janela, mas as barras no painel superior, assim como as duas caixas na parte inferior, não estão posicionadas corretamente. Se quisermos manter as barras do topo posicionadas à esquerda, precisamos alterar o X Anchor de None para Left:

![](images/gui/adjustmode_example_top_anchor_left.png)

Isso é exatamente o que queremos para o painel superior. As barras no painel superior já tinham seus pontos Pivot definidos como West, o que significa que elas se posicionarão corretamente com a borda esquerda/oeste das barras (Pivot) ancorada à borda esquerda do painel pai (X Anchor).

Agora, se definirmos o X Anchor como Left para a caixa da esquerda e o X Anchor como Right para a caixa da direita, obtemos o seguinte resultado:

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Esse não é exatamente o resultado esperado. As duas caixas deveriam permanecer tão próximas das bordas esquerda e direita quanto as duas barras no painel superior. O motivo é que o ponto Pivot está errado:

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Ambas as caixas têm o ponto Pivot definido como Center. Isso significa que, quando a tela fica mais larga, o ponto central (o ponto de pivô) das caixas permanece à mesma distância relativa das bordas. No caso da caixa esquerda, era 17% da borda esquerda com a janela original de 640x1136:

![](images/gui/adjustmode_example_original_ratio.png)

Quando a tela é redimensionada, o ponto central da caixa esquerda permanece à mesma distância de 17% da borda esquerda:

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Se alterarmos o ponto Pivot de Center para West na caixa da esquerda e para East na caixa da direita, e reposicionarmos as caixas, obtemos o resultado desejado mesmo quando a tela é redimensionada:

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Ordem de desenho

Todos os nodes são renderizados na ordem em que estão listados sob a pasta "Nodes". O node no topo da lista é desenhado primeiro e, portanto, aparecerá atrás de todos os outros nodes. O último node da lista é desenhado por último, o que significa que aparecerá na frente de todos os outros nodes. Alterar o valor Z de um node não controla sua ordem de desenho; no entanto, se você definir o valor Z fora do intervalo de renderização do seu script de renderização, o node não será mais renderizado na tela. Você pode sobrescrever a ordenação por índice dos nodes com layers (veja abaixo).

![Ordem de desenho](images/gui/draw_order.png)

Selecione um node e pressione <kbd>Alt + Up/Down</kbd> para mover um node para cima ou para baixo e alterar sua ordem de índice.

A ordem de desenho pode ser alterada por script:

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Hierarquias pai-filho

Um node se torna filho de outro node ao ser arrastado para cima do node que você deseja que seja o pai. Um node com pai herda a transformação (posição, rotação e escala) aplicada ao pai e relativa ao pivô do pai.

![Pai filho](images/gui/parent_child.png)

Pais são desenhados antes de seus filhos. Use layers para alterar a ordem de desenho de nodes pai e filho e para otimizar a renderização de nodes (veja abaixo).


## Layers e draw calls {#layers-and-draw-calls}

Layers oferecem controle detalhado sobre como os nodes são desenhados e podem ser usadas para reduzir o número de draw calls que a engine precisa criar para desenhar uma cena GUI. Quando a engine está prestes a desenhar os nodes de uma cena GUI, ela agrupa os nodes em lotes de draw calls com base nas seguintes condições:

- Os nodes devem usar o mesmo tipo.
- Os nodes devem usar o mesmo atlas ou tile source.
- Os nodes devem ser renderizados com o mesmo blend mode.
- Eles devem usar a mesma fonte.

Se um node diferir do anterior em qualquer um desses pontos, ele quebrará o lote e criará outra draw call. Nodes de clipping sempre quebram o lote, e cada escopo de stencil também quebra o lote.

A capacidade de organizar nodes em hierarquias facilita agrupar nodes em unidades gerenciáveis. Mas hierarquias podem quebrar efetivamente a renderização em lote se você misturar diferentes tipos de node:

![Quebra de lote na hierarquia](images/gui/break_batch.png)

Quando o pipeline de renderização percorre a lista de nodes, ele é forçado a configurar um lote separado para cada node, porque os tipos são diferentes. No total, esses três botões exigirão seis draw calls.

Ao atribuir layers aos nodes, eles podem ser ordenados de forma diferente, permitindo que o pipeline de renderização agrupe os nodes em menos draw calls. Comece adicionando à cena as layers de que você precisa. Clique com o botão direito no ícone da pasta "Layers" no *Outline* e selecione <kbd>Add ▸ Layer</kbd>. Marque a nova layer e atribua a ela uma propriedade *Name* na visualização *Properties*.

![Layers](images/gui/layers.png)

Então defina a propriedade *Layer* de cada node para a layer correspondente. A ordem de desenho das layers tem precedência sobre a ordem indexada normal dos nodes, então definir os nodes box de gráficos dos botões como "graphics" e os nodes de texto dos botões como "text" resultará na seguinte ordem de desenho:

* Primeiro, todos os nodes da layer "graphics", a partir do topo:

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Depois, todos os nodes da layer "text", a partir do topo:

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Os nodes agora podem ser agrupados em duas draw calls, em vez de seis. Um grande ganho de desempenho!

Observe que um node filho sem layer definida herdará implicitamente a configuração de layer do node pai. Não definir uma layer em um node implicitamente o adiciona à layer "null", que é desenhada antes de qualquer outra layer.
