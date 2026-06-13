---
title: Manual de animações de propriedade no Defold
brief: Este manual descreve como usar animações de propriedade no Defold.
---

# Animação de propriedade

Todas as propriedades numéricas (`números`, `vector3`, `vector4` e quaternions) e constantes de shader podem ser animadas com o sistema de animação integrado, usando a função `go.animate()`. A engine fará automaticamente o "tween" das propriedades de acordo com os modos de reprodução e funções de easing fornecidos. Você também pode especificar funções de easing personalizadas.

  ![Property animation](images/animation/property_animation.png)
  ![Bounce loop](images/animation/bounce.gif)

## Animação de propriedade

Para animar uma propriedade de objeto de jogo ou componente, use a função `go.animate()`. Para propriedades de nodes de GUI, a função correspondente é `gui.animate()`.

```lua
-- Define o componente y da propriedade position para 200
go.set(".", "position.y", 200)
-- Então o anima
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Para parar todas as animações de uma determinada propriedade, chame `go.cancel_animations()`, ou, para nodes de GUI, `gui.cancel_animations()`:

```lua
-- Para a animação de rotação euler z no objeto de jogo atual
go.cancel_animations(".", "euler.z")
```

Se você cancelar a animação de uma propriedade composta, como `position`, quaisquer animações dos subcomponentes (`position.x`, `position.y` e `position.z`) também serão canceladas.

O [manual de Propriedades](/manuals/properties) contém todas as propriedades disponíveis em objetos de jogo, componentes e nodes de GUI.

## Animação de propriedades de nodes de GUI

Quase todas as propriedades de nodes de GUI podem ser animadas. Você pode, por exemplo, tornar um node invisível definindo sua propriedade `color` como totalmente transparente e então fazê-lo aparecer animando a cor para branco (isto é, sem cor de tint).

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Anima a cor para branco
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Anima o componente vermelho da cor de contorno
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- E move para a posição x 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Callbacks de conclusão

As funções de animação de propriedade `go.animate()` e `gui.animate()` aceitam uma função de callback Lua opcional como último argumento. Essa função será chamada quando a animação for reproduzida até o fim. A função nunca é chamada para animações em loop, nem quando uma animação é cancelada manualmente via `go.cancel_animations()` ou `gui.cancel_animations()`. O callback pode ser usado para disparar eventos na conclusão da animação ou para encadear várias animações.

## Easing

Easing define como o valor animado muda ao longo do tempo. As imagens abaixo descrevem as funções aplicadas ao longo do tempo para criar o easing.

Os seguintes valores de easing são válidos para `go.animate()`:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

Os seguintes valores de easing são válidos para `gui.animate()`:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Linear interpolation](images/properties/easing_linear.png)
![In back](images/properties/easing_inback.png)
![Out back](images/properties/easing_outback.png)
![In-out back](images/properties/easing_inoutback.png)
![Out-in back](images/properties/easing_outinback.png)
![In bounce](images/properties/easing_inbounce.png)
![Out bounce](images/properties/easing_outbounce.png)
![In-out bounce](images/properties/easing_inoutbounce.png)
![Out-in bounce](images/properties/easing_outinbounce.png)
![In elastic](images/properties/easing_inelastic.png)
![Out elastic](images/properties/easing_outelastic.png)
![In-out elastic](images/properties/easing_inoutelastic.png)
![Out-in elastic](images/properties/easing_outinelastic.png)
![In sine](images/properties/easing_insine.png)
![Out sine](images/properties/easing_outsine.png)
![In-out sine](images/properties/easing_inoutsine.png)
![Out-in sine](images/properties/easing_outinsine.png)
![In exponential](images/properties/easing_inexpo.png)
![Out exponential](images/properties/easing_outexpo.png)
![In-out exponential](images/properties/easing_inoutexpo.png)
![Out-in exponential](images/properties/easing_outinexpo.png)
![In circlic](images/properties/easing_incirc.png)
![Out circlic](images/properties/easing_outcirc.png)
![In-out circlic](images/properties/easing_inoutcirc.png)
![Out-in circlic](images/properties/easing_outincirc.png)
![In quadratic](images/properties/easing_inquad.png)
![Out quadratic](images/properties/easing_outquad.png)
![In-out quadratic](images/properties/easing_inoutquad.png)
![Out-in quadratic](images/properties/easing_outinquad.png)
![In cubic](images/properties/easing_incubic.png)
![Out cubic](images/properties/easing_outcubic.png)
![In-out cubic](images/properties/easing_inoutcubic.png)
![Out-in cubic](images/properties/easing_outincubic.png)
![In quartic](images/properties/easing_inquart.png)
![Out quartic](images/properties/easing_outquart.png)
![In-out quartic](images/properties/easing_inoutquart.png)
![Out-in quartic](images/properties/easing_outinquart.png)
![In quintic](images/properties/easing_inquint.png)
![Out quintic](images/properties/easing_outquint.png)
![In-out quintic](images/properties/easing_inoutquint.png)
![Out-in quintic](images/properties/easing_outinquint.png)

## Easing personalizado

Você pode criar curvas de easing personalizadas definindo um `vector` com um conjunto de valores e então fornecendo o vector em vez de uma das constantes de easing predefinidas acima. Os valores do vector expressam uma curva do valor inicial (`0`) ao valor-alvo (`1`). O runtime amostra valores do vector e interpola linearmente ao calcular valores entre os pontos expressos no vector.

Por exemplo, o vector:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

produz a seguinte curva:

![Custom curve](images/animation/custom_curve.png)

O exemplo a seguir faz a posição y de um objeto de jogo saltar entre a posição atual e 200 de acordo com uma curva quadrada:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Square curve](images/animation/square_curve.png)
