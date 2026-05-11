---
title: Manual de clipping de GUI
brief: Este manual descreve como criar nodes GUI que mascaram outros nodes por meio de clipping com stencil.
---

# Clipping

Nodes GUI podem ser usados como nodes de *clipping*: máscaras que controlam como outros nodes são renderizados. Este manual explica como esse recurso funciona.

## Criando um node de clipping

Nodes Box, Text e Pie podem ser usados para clipping. Para criar um node de clipping, adicione um node à sua GUI e então defina suas propriedades conforme necessário:

Clipping Mode
: O modo usado para clipping.
  - `None` renderiza o node sem nenhum clipping.
  - `Stencil` faz o node escrever na máscara stencil atual.

Clipping Visible
: Marque para renderizar o conteúdo do node.

Clipping Inverted
: Marque para escrever a inversão da forma do node na máscara.

Em seguida, adicione como filhos ao node de clipping os nodes que você deseja recortar.

![Criar clipping](images/gui-clipping/create.png)

## Máscara stencil

O clipping funciona fazendo nodes escreverem em um *stencil buffer*. Esse buffer contém máscaras de clipping: informações que dizem à placa gráfica se um pixel deve ser renderizado ou não.

- Um node sem pai clipper, mas com o modo de clipping definido como `Stencil`, escreverá sua forma (ou sua forma inversa) em uma nova máscara de clipping armazenada no stencil buffer.
- Se um node de clipping tiver um pai clipper, ele recortará a máscara de clipping do pai. Um node filho de clipping nunca pode _estender_ a máscara de clipping atual, apenas recortá-la ainda mais.
- Nodes que não são clippers, mas são filhos de clippers, serão renderizados com a máscara de clipping criada pela hierarquia de pais.

![Hierarquia de clipping](images/gui-clipping/setup.png)

Aqui, três nodes estão configurados em uma hierarquia:

- As formas de hexágono e quadrado são ambas clippers de stencil.
- O hexágono cria uma nova máscara de clipping; o quadrado a recorta ainda mais.
- O node circular é um node pie comum, então será renderizado com a máscara de clipping criada pelos clippers pais.

Quatro combinações de clippers normais e invertidos são possíveis para essa hierarquia. A área verde marca a parte do círculo que é renderizada. O restante é mascarado:

![Máscaras stencil](images/gui-clipping/modes.png)

## Limitações de stencil

- O número total de clippers de stencil não pode exceder 256.
- A profundidade máxima de aninhamento de nodes filhos de _stencil_ é de 8 níveis. (Apenas nodes com clipping de stencil contam.)
- O número máximo de nodes stencil irmãos é 127. A cada nível para baixo em uma hierarquia de stencil, o limite máximo é reduzido pela metade.
- Nodes invertidos têm custo maior. Há um limite de 8 nodes de clipping invertidos, e cada um reduzirá pela metade a quantidade máxima de nodes de clipping não invertidos.
- Stencils renderizam uma máscara stencil a partir da _geometria_ do node (não da textura). É possível inverter a máscara definindo a propriedade *Inverted clipper*.


## Layers

Layers podem ser usadas para controlar a ordem de renderização (e batching) de nodes. Ao usar layers e nodes de clipping, a ordem usual de camadas é sobrescrita. A ordem das layers sempre tem precedência sobre a ordem de clipping; se atribuições de layer forem combinadas com nodes de clipping, o clipping pode acontecer fora de ordem se um node pai com clipping habilitado pertencer a uma layer mais alta que seus filhos. Os filhos sem layer atribuída ainda respeitarão a hierarquia e, em seguida, serão desenhados e recortados depois do pai.

::: sidenote
Um node de clipping e sua hierarquia serão desenhados primeiro se tiverem uma layer atribuída, e na ordem normal se nenhuma layer for atribuída.
:::

![Layers e clipping](images/gui-clipping/layers.png)

Neste exemplo, ambos os nodes clipper "`Donut BG`" e "`BG`" estão usando a mesma layer 1. A ordem de renderização entre eles seguirá a mesma ordem da hierarquia, em que "`Donut BG`" é renderizado antes de "`BG`". No entanto, o node filho "`Donut Shadow`" é atribuído à layer 2, que tem uma ordem de layer mais alta e, portanto, será renderizado depois de ambos os nodes de clipping. Neste caso, a ordem de renderização será:

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Aqui você pode ver que o objeto "`Donut Shadow`" será recortado por ambos os nodes de clipping devido às layers, mesmo sendo filho de apenas um deles.
