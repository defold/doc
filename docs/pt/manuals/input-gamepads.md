---
title: Entrada de gamepad no Defold
brief: Este manual explica como funciona a entrada de gamepad.
---

::: sidenote
Recomenda-se que você se familiarize com a forma geral como a entrada funciona no Defold, como receber entrada e em que ordem ela é recebida nos seus arquivos de script. Saiba mais sobre o sistema de entrada no [manual Visão geral de entrada](/manuals/input).
:::

# Gamepads
Gamepad triggers permitem mapear entrada padrão de gamepad para funções do jogo. A entrada de gamepad oferece mapeamentos para:

- Sticks esquerdo e direito (direção e cliques)
- Pads digitais esquerdo e direito. O pad direito geralmente corresponde aos botões "A", "B", "X" e "Y" no controle Xbox e aos botões "square", "circle", "triangle" e "cross" no controle Playstation.
- Gatilhos esquerdo e direito
- Botões superiores esquerdo e direito
- Botões Start, Back e Guide

![](images/input/gamepad_bindings.png)

::: important
Os exemplos abaixo usam as ações mostradas na imagem acima. Como em toda entrada, você pode nomear suas ações de entrada da forma que quiser.
:::

## Botões digitais
Botões digitais geram eventos pressionados, soltos e repetidos. Exemplo mostrando como detectar entrada para um botão digital (pressionado ou solto):

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- começar a mover para a esquerda
        elseif action.released then
            -- parar de mover para a esquerda
        end
    end
end
```

## Sticks analógicos
Sticks analógicos geram eventos de entrada contínuos quando o stick é movido para fora da zona morta definida no arquivo de configurações de gamepad (veja abaixo). Exemplo mostrando como detectar entrada para um stick analógico:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- o stick esquerdo foi movido para baixo
        print(action.value) -- um valor entre 0.0 e -1.0
    end
end
```

Sticks analógicos também geram eventos pressionados e soltos quando movidos nas direções cardeais acima de um certo valor limite. Isso facilita usar também um stick analógico como entrada direcional digital:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- o stick esquerdo foi movido até a posição extrema inferior
    end
end
```

## Vários gamepads
O Defold oferece suporte a vários gamepads por meio do sistema operacional host; ações definem o campo `gamepad` da tabela de ação para o número do gamepad de onde a entrada se originou:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 quer entrar no jogo
        end
    end
end
```

## Conexão e desconexão
Mapeamentos de entrada de gamepad também fornecem dois mapeamentos separados chamados `Connected` e `Disconnected` para detectar quando um gamepad é conectado (mesmo os conectados desde o início) ou desconectado.

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 foi conectado
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 foi desconectado
        end
    end
end
```

## Gamepads brutos
(Desde o Defold 1.2.183)

Mapeamentos de entrada de gamepad também fornecem um mapeamento separado chamado `Raw` para disponibilizar a entrada não filtrada (sem deadzone aplicada) de botões, eixos e hats de qualquer gamepad conectado.

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## Arquivo de configurações de gamepads
A configuração de entrada de gamepad usa um arquivo de mapeamento separado para cada tipo de gamepad de hardware. Mapeamentos de gamepad para hardwares específicos são definidos em um arquivo *gamepads*. O Defold vem com um arquivo gamepads integrado com configurações para gamepads comuns:

![Gamepad settings](images/input/gamepads.png)

Se você precisar criar um novo arquivo de configurações de gamepad, temos uma ferramenta simples para ajudar:

[Clique para baixar gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Ela inclui binários para Windows, Linux e macOS. Execute-a pela linha de comando:

```sh
./gdc
```

A ferramenta pedirá que você pressione diferentes botões no controle conectado. Ela então produzirá um novo arquivo gamepads com os mapeamentos corretos para o seu controle. Salve o novo arquivo, ou mescle-o ao seu arquivo gamepads existente, e depois atualize a configuração em *game.project*:

![Gamepad settings](images/input/gamepad_setting.png)

### Gamepads não identificados
(Desde o Defold 1.2.186)

Quando um gamepad é conectado e não existe mapeamento para ele, o gamepad gerará apenas ações "connected", "disconnected" e "raw". Nesse caso, você precisa mapear manualmente os dados brutos do gamepad para ações no seu jogo.

(Desde o Defold 1.4.8)

É possível verificar se uma ação de entrada de um gamepad vem de um gamepad desconhecido ou não lendo o valor `gamepad_unknown` da ação:

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
``` 

## Gamepads em HTML5
Gamepads têm suporte em builds HTML5 e geram os mesmos eventos de entrada que em outras plataformas. O suporte a gamepads é baseado na [Gamepad API](https://www.w3.org/TR/gamepad/), que é compatível com a maioria dos navegadores ([consulte esta tabela de suporte](https://caniuse.com/?search=gamepad)). Se o navegador não oferecer suporte à Gamepad API, o Defold ignorará silenciosamente quaisquer Gamepad triggers no seu projeto. Você pode verificar se o navegador oferece suporte à Gamepad API conferindo se a função `getGamepads` existe no objeto `navigator`:

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

Se o seu jogo estiver sendo executado dentro de um `iframe`, você também deve garantir que o `iframe` tenha a permissão `gamepad` adicionada:

```html
<iframe allow="gamepad"></iframe>
```

### Gamepad padrão
(Desde o Defold 1.4.1)

Se um gamepad conectado for identificado pelo navegador como um gamepad padrão, ele usará o mapeamento de "Standard Gamepad" no [arquivo de configurações de gamepads](/manuals/input-gamepads/#gamepads-settings-file) (um mapeamento de Standard Gamepad está incluído no arquivo `default.gamepads` em `/builtins`). Um gamepad padrão é definido como tendo 16 botões e 2 sticks analógicos com um layout de botões semelhante ao de um controle PlayStation ou Xbox (veja a [definição e o layout de botões do W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad) para mais informações). Se o gamepad conectado não for identificado como um gamepad padrão, o Defold procurará um mapeamento que corresponda ao tipo de hardware do gamepad no arquivo de configurações de gamepad.

## Gamepads no Windows
No Windows, atualmente apenas controles Xbox 360 têm suporte. Para conectar seu controle 360 à sua máquina Windows, [certifique-se de que ele esteja configurado corretamente](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

## Gamepads no Android
(Desde o Defold 1.2.183)

Gamepads têm suporte em builds Android e geram os mesmos eventos de entrada que em outras plataformas. O suporte a gamepads é baseado no [sistema de entrada do Android para eventos de tecla e movimento](https://developer.android.com/training/game-controllers/controller-input). Os eventos de entrada do Android serão traduzidos para eventos de gamepad do Defold usando o mesmo arquivo *gamepad* descrito acima.

Ao adicionar mapeamentos de gamepad adicionais no Android, você pode usar as seguintes tabelas de consulta para traduzir dos eventos de entrada do Android para valores do arquivo *gamepad*:

| Evento de tecla para índice de botão | Índice | Versão |
|-----------------------------|-------|---------|
| `AKEYCODE_BUTTON_A`           | 0     | 1.2.183 |
| `AKEYCODE_BUTTON_B`           | 1     | 1.2.183 |
| `AKEYCODE_BUTTON_C`           | 2     | 1.2.183 |
| `AKEYCODE_BUTTON_X`           | 3     | 1.2.183 |
| `AKEYCODE_BUTTON_L1`          | 4     | 1.2.183 |
| `AKEYCODE_BUTTON_R1`          | 5     | 1.2.183 |
| `AKEYCODE_BUTTON_Y`           | 6     | 1.2.183 |
| `AKEYCODE_BUTTON_Z`           | 7     | 1.2.183 |
| `AKEYCODE_BUTTON_L2`          | 8     | 1.2.183 |
| `AKEYCODE_BUTTON_R2`          | 9     | 1.2.183 |
| `AKEYCODE_DPAD_CENTER`        | 10    | 1.2.183 |
| `AKEYCODE_DPAD_DOWN`          | 11    | 1.2.183 |
| `AKEYCODE_DPAD_LEFT`          | 12    | 1.2.183 |
| `AKEYCODE_DPAD_RIGHT`         | 13    | 1.2.183 |
| `AKEYCODE_DPAD_UP`            | 14    | 1.2.183 |
| `AKEYCODE_BUTTON_START`       | 15    | 1.2.183 |
| `AKEYCODE_BUTTON_SELECT`      | 16    | 1.2.183 |
| `AKEYCODE_BUTTON_THUMBL`      | 17    | 1.2.183 |
| `AKEYCODE_BUTTON_THUMBR`      | 18    | 1.2.183 |
| `AKEYCODE_BUTTON_MODE`        | 19    | 1.2.183 |
| `AKEYCODE_BUTTON_1`           | 20    | 1.2.186 |
| `AKEYCODE_BUTTON_2`           | 21    | 1.2.186 |
| `AKEYCODE_BUTTON_3`           | 22    | 1.2.186 |
| `AKEYCODE_BUTTON_4`           | 23    | 1.2.186 |
| `AKEYCODE_BUTTON_5`           | 24    | 1.2.186 |
| `AKEYCODE_BUTTON_6`           | 25    | 1.2.186 |
| `AKEYCODE_BUTTON_7`           | 26    | 1.2.186 |
| `AKEYCODE_BUTTON_8`           | 27    | 1.2.186 |
| `AKEYCODE_BUTTON_9`           | 28    | 1.2.186 |
| `AKEYCODE_BUTTON_10`          | 29    | 1.2.186 |
| `AKEYCODE_BUTTON_11`          | 30    | 1.2.186 |
| `AKEYCODE_BUTTON_12`          | 31    | 1.2.186 |
| `AKEYCODE_BUTTON_13`          | 32    | 1.2.186 |
| `AKEYCODE_BUTTON_14`          | 33    | 1.2.186 |
| `AKEYCODE_BUTTON_15`          | 34    | 1.2.186 |
| `AKEYCODE_BUTTON_16`          | 35    | 1.2.186 |

([definições de `KeyEvent` do Android](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719))

| Evento de movimento para índice de eixo | Índice |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

([definições de `MotionEvent` do Android](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d))

Use esta tabela de consulta em combinação com um app de teste de gamepad da Google Play Store para descobrir para qual evento de tecla cada botão do seu gamepad está mapeado.
