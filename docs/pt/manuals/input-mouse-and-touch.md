---
title: Entrada de mouse e toque no Defold
brief: Este manual explica como funciona a entrada de mouse e toque.
---

::: sidenote
Recomenda-se que você se familiarize com a forma geral como a entrada funciona no Defold, como receber entrada e em que ordem ela é recebida nos seus arquivos de script. Saiba mais sobre o sistema de entrada no [manual Visão geral de entrada](/manuals/input).
:::

# Mouse Triggers
Mouse triggers permitem mapear entrada de botões do mouse e rodas de rolagem para ações do jogo.

![](images/input/mouse_bindings.png)

::: sidenote
As entradas de botão do mouse `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_RIGHT` e `MOUSE_BUTTON_MIDDLE` são equivalentes a `MOUSE_BUTTON_1`, `MOUSE_BUTTON_2` e `MOUSE_BUTTON_3`.
:::

::: important
Os exemplos abaixo usam as ações mostradas na imagem acima. Como em toda entrada, você pode nomear suas ações de entrada da forma que quiser.
:::

## Botões do mouse
Botões do mouse geram eventos pressionados, soltos e repetidos. Exemplo mostrando como detectar entrada para o botão esquerdo do mouse (pressionado ou solto):

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- botão esquerdo do mouse pressionado
        elseif action.released then
            -- botão esquerdo do mouse solto
        end
    end
end
```

::: important
Ações de entrada `MOUSE_BUTTON_LEFT` (ou `MOUSE_BUTTON_1`) também são enviadas para entradas de toque único.
:::

## Roda do mouse
Entradas da roda do mouse detectam ações de rolagem. O campo `action.value` é `1` se a roda for rolada e `0` caso contrário. (Ações de rolagem são tratadas como se fossem pressionamentos de botão. Atualmente, o Defold não oferece suporte a entrada de rolagem fina em touchpads.)

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- a roda do mouse foi rolada para cima
        end
    end
end
```

## Movimento do mouse
O movimento do mouse é tratado separadamente. Eventos de movimento do mouse não são recebidos a menos que pelo menos um mouse trigger esteja configurado nos seus mapeamentos de entrada.

O movimento do mouse não é mapeado nos mapeamentos de entrada, mas `action_id` é definido como `nil` e a tabela `action` é preenchida com a localização e o delta de movimento da posição do mouse.

```lua
function on_input(self, action_id, action)
    if action.x and action.y then
        -- faz o objeto de jogo seguir o movimento do mouse/toque
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# Touch Triggers
Triggers do tipo toque único e multitoque estão disponíveis em dispositivos iOS e Android em aplicações nativas e em pacotes HTML5.

![](images/input/touch_bindings.png)

## Toque único
Triggers do tipo toque único não são configurados a partir da seção Touch Triggers dos mapeamentos de entrada. Em vez disso, **triggers de toque único são configurados automaticamente quando você tem entrada de botão do mouse configurada para `MOUSE_BUTTON_LEFT` ou `MOUSE_BUTTON_1`**.

## Multitoque
Triggers do tipo multitoque preenchem uma tabela chamada `touch` na tabela de ação. Os elementos da tabela são indexados por inteiros com números de `1` a `N`, onde `N` é o número de pontos de toque. Cada elemento da tabela contém campos com dados de entrada:

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Cria em cada ponto de toque
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
Multitoque não deve receber a mesma ação da entrada de botão do mouse para `MOUSE_BUTTON_LEFT` ou `MOUSE_BUTTON_1`. Atribuir a mesma ação efetivamente substituirá o toque único e impedirá que você receba qualquer evento de toque único.
:::

::: sidenote
O [asset Defold-Input](https://defold.com/assets/defoldinput/) pode ser usado para configurar facilmente controles virtuais na tela, como botões e sticks analógicos, com suporte a multitoque.
:::


## Detectando clique ou toque em objetos
Detectar quando o usuário clicou ou tocou em um componente visual é uma operação muito comum necessária em muitos jogos. Pode ser uma interação do usuário com um botão ou outro elemento de UI, ou a interação com um objeto de jogo, como uma unidade controlada pelo jogador em um jogo de estratégia, algum tesouro em uma fase de dungeon crawler ou um personagem que entrega missões em um RPG. A abordagem a ser usada varia dependendo do tipo de componente visual.

### Detectando interação com nodes GUI
Para elementos de UI, existe a função `gui.pick_node(node, x, y)`, que retorna true ou false dependendo se a coordenada especificada está dentro dos limites de um node GUI ou não. Consulte a [documentação da API](/ref/gui/#gui.pick_node:node-x-y), o [exemplo de pointer over](/examples/gui/pointer_over/) ou o [exemplo de botão](/examples/gui/button/) para saber mais.

### Detectando interação com objetos de jogo
Para objetos de jogo, detectar interação é mais complicado, pois coisas como translação da câmera e projeção do script de renderização afetarão os cálculos necessários. Há duas abordagens gerais para detectar interação com objetos de jogo:

  1. Rastrear a posição e o tamanho dos objetos de jogo com os quais o usuário pode interagir e verificar se a coordenada do mouse ou toque está dentro dos limites de algum dos objetos.
  2. Anexar objetos de colisão aos objetos de jogo com os quais o usuário pode interagir e um objeto de colisão que segue o mouse ou dedo, então verificar colisões entre eles.

::: sidenote
Uma solução pronta para uso que usa objetos de colisão para detectar entrada do usuário com suporte a arrastar e clicar pode ser encontrada no [asset Defold-Input](https://defold.com/assets/defoldinput/).
:::

Em ambos os casos, é necessário converter das coordenadas de espaço de tela do evento de mouse ou toque para as coordenadas de espaço de mundo dos objetos de jogo. Isso pode ser feito de algumas formas diferentes:

  * Manter manualmente o controle de qual visualização e projeção é usada pelo script de renderização e usar isso para converter de e para o espaço de mundo. Veja o [manual de câmera para um exemplo disso](/manuals/camera/#converting-mouse-to-world-coordinates).
  * Usar uma [solução de câmera de terceiros](/manuals/camera/#third-party-camera-solutions) e aproveitar as funções fornecidas de conversão de tela para mundo.
