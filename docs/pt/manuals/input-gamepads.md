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
Botões digitais geram eventos `pressed` (pressionado), `released` (solto) e `repeated` (repetido). Exemplo mostrando como detectar entrada para um botão digital (pressionado ou solto):

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

Sticks analógicos também geram eventos `pressed` (pressionado) e `released` (solto) quando movidos nas direções cardeais acima de um certo valor limite. Isso facilita usar também um stick analógico como entrada direcional digital:

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- o stick esquerdo foi movido até a posição extrema inferior
    end
end
```

## Vários gamepads
O Defold oferece suporte a vários gamepads por meio do sistema operacional host; ações definem o campo `gamepad` da tabela `action` para o número do gamepad de onde a entrada se originou:

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

<a id="raw-gamepads"></a>

## Gamepads brutos

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

## Arquivo de configurações de gamepads {#gamepads-settings-file}

Mapeamentos de gamepad traduzem os botões, eixos e direcionais de um controle para os controles padrão usados pelos mapeamentos de entrada. O Defold combina duas fontes de mapeamento configuradas na seção *Input* de *game.project*:

| Configuração | Formato de mapeamento | Padrão |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | Banco de dados de texto no formato SDL, associado pelo GUID do controle | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | Entradas `.gamepads` legadas para nomes de dispositivos e plataformas | `/builtins/input/default.gamepads` |

Mapeamentos do banco de dados SDL e mapeamentos automáticos da plataforma usam [Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone). Entradas `.gamepads` legadas definem suas próprias zonas mortas. No Android, um controle sem entrada no banco de dados também pode receber um [mapeamento automático](#gamepads-on-android).

### Mapeamentos .gamepads legados {#legacy-gamepads-mappings}

Um arquivo `.gamepads` pode conter mapeamentos para vários controles. Mapeamentos legados existentes continuam sendo aceitos. O Defold inclui mapeamentos para controles comuns no arquivo padrão:

![Gamepad settings](images/input/gamepads.png)

Se precisar criar um mapeamento `.gamepads` legado em uma plataforma desktop, a ferramenta abaixo pode ajudar. Para Android, consulte [Gamepads no Android](#gamepads-on-android).

[Clique para baixar gdc.zip](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032).

Ela inclui binários para Windows, Linux e macOS. Execute-a pela linha de comando:

```sh
./gdc
```

A ferramenta pedirá que você pressione diferentes botões no controle conectado. Ela então produzirá um novo arquivo gamepads com os mapeamentos corretos para o seu controle. Salve o novo arquivo, ou mescle-o ao seu arquivo gamepads existente, e depois atualize a configuração em *game.project*:

![Gamepad settings](images/input/gamepad_setting.png)

<a id="unidentified-gamepads"></a>

### Gamepads não identificados

Quando não há um mapeamento configurado nem um mapeamento automático da plataforma, o gamepad gera apenas as ações vinculadas a `Connected`, `Disconnected` e `Raw`. Você pode adicionar um mapeamento do controle ou processar sua entrada bruta no jogo.

É possível verificar se uma ação de entrada de um gamepad vem de um gamepad desconhecido ou não lendo o valor `gamepad_unknown` de `action`:

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

## Gamepads em HTML5 {#gamepads-in-html5}
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

Se um gamepad conectado for identificado pelo navegador como um gamepad padrão, ele usará o mapeamento de `Standard Gamepad` no [arquivo de configurações de gamepads](/manuals/input-gamepads/#gamepads-settings-file) (um mapeamento de `Standard Gamepad` está incluído no arquivo `default.gamepads` em `/builtins`). Um gamepad padrão é definido como tendo 16 botões e 2 sticks analógicos com um layout de botões semelhante ao de um controle PlayStation ou Xbox (veja a [definição e o layout de botões do W3C](https://w3c.github.io/gamepad/#dfn-standard-gamepad) para mais informações). Se o gamepad conectado não for identificado como um gamepad padrão, o Defold procurará um mapeamento que corresponda ao tipo de hardware do gamepad no arquivo de configurações de gamepad.

## Gamepads no Windows
No Windows, atualmente apenas controles Xbox 360 têm suporte. Para conectar seu controle 360 à sua máquina Windows, [certifique-se de que ele esteja configurado corretamente](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows).

<a id="gamepads-on-android"></a>

## Gamepads no Android

Gamepads são aceitos em builds Android e geram as mesmas ações de entrada que em outras plataformas. O Defold usa os [mapeamentos de gamepad](#gamepads-settings-file) configurados e pode mapear automaticamente alguns controles sem uma entrada correspondente.

Se um controle não for identificado ou seus comandos estiverem incorretos, teste-o no dispositivo Android e adicione ou atualize seu mapeamento. Consulte [Gamepads não identificados](#unidentified-gamepads) e [Gamepads brutos](#raw-gamepads) para solucionar problemas.
