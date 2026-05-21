---
title: Nodes GUI pie no Defold
brief: Este manual explica como usar nodes pie em cenas GUI do Defold.
---

# Nodes GUI pie

Nodes pie são usados para criar objetos circulares ou elipsoidais que variam de círculos simples a fatias e formatos quadrados de rosca.

## Criando um node pie

Clique com o botão direito na seção *Nodes* no *Outline* e selecione <kbd>Add ▸ Pie</kbd>. O novo node pie é selecionado e você pode modificar suas propriedades.

![Criar node pie](images/gui-pie/create.png)

As seguintes propriedades são exclusivas de nodes pie:

Inner Radius
: O raio interno do node, expresso ao longo do eixo X.

Outer Bounds
: A forma dos limites externos do node.

  - `Ellipse` estenderá o node até o raio externo.
  - `Rectangle` estenderá o node até a caixa delimitadora do node.

Perimeter Vertices
: O número de segmentos que será usado para construir a forma, expresso como o número de vértices necessários para circunscrever totalmente o perímetro de 360 graus do node.

Pie Fill Angle
: Quanto da fatia deve ser preenchido. Expresso como um ângulo no sentido anti-horário a partir da direita.

![Propriedades](images/gui-pie/properties.png)

Se você definir uma textura no node, a imagem da textura será aplicada plana, com os cantos da textura correspondendo aos cantos da caixa delimitadora do node.

## Modificar nodes pie em runtime

Nodes pie respondem a qualquer função genérica de manipulação de nodes para definir tamanho, pivô, cor e assim por diante. Existem algumas funções e propriedades exclusivas de nodes pie:

```lua
local pienode = gui.get_node("my_pie_node")

-- obtém os limites externos
local fill_angle = gui.get_fill_angle(pienode)

-- aumenta os vértices do perímetro
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- altera os limites externos
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- anima o raio interno
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
