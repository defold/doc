---
title: Depuração no Defold
brief: Este manual explica os recursos de depuração presentes no Defold.
---

# Depurando lógica de jogo

O Defold contém um depurador Lua integrado com recurso de inspeção. Junto com as [ferramentas de profiling](/manuals/profiling) integradas, ele é uma ferramenta poderosa que pode ajudar a encontrar a causa de bugs na lógica do seu jogo ou a analisar problemas de desempenho.

## Depuração com print e visual

A forma mais simples de depurar seu jogo no Defold é usar [print debugging](http://en.wikipedia.org/wiki/Debugging#Techniques). Use instruções `print()` ou [`pprint()`](/ref/builtins#pprint) para observar variáveis ou indicar o fluxo de execução. Se um objeto de jogo sem script se comportar de forma estranha, você pode simplesmente anexar um script a ele com o único propósito de depuração. Usar qualquer uma das funções de impressão imprimirá na visualização *Console* do editor e no [log do jogo](/manuals/debugging-game-and-system-logs).

Além de imprimir, a engine também pode desenhar texto de depuração e linhas retas na tela. Isso é feito enviando mensagens ao socket `@render`:

```lua
-- Desenha o valor de "my_val" com texto de depuração na tela
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Desenha texto colorido na tela
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Desenha uma linha de depuração entre player e enemy na tela
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

As mensagens visuais de depuração adicionam dados ao pipeline de renderização e são desenhadas como parte do pipeline de renderização regular.

* `"draw_line"` adiciona dados que são renderizados com a função `render.draw_debug3d()` no script de renderização.
* `"draw_text"` é renderizado com `/builtins/fonts/debug/always_on_top.font`, que usa o material `/builtins/fonts/debug/always_on_top_font.material`.
* `"draw_debug_text"` é igual a `"draw_text"`, mas é renderizado em uma cor personalizada.

Observe que provavelmente você vai querer atualizar esses dados a cada frame, então enviar as mensagens na função `update()` é uma boa ideia.

## Executando o depurador

O depurador Lua está disponível em builds nativos de depuração e headless. Use uma engine da mesma versão do Defold que o editor. Builds de release e Web não permitem conectar o depurador.

Para executar o depurador, selecione <kbd>Debug ▸ Start/Attach</kbd>. Isso inicia o jogo com o depurador conectado ou o conecta a um jogo já em execução. Ao iniciar um jogo para depuração, o editor instala os pontos de interrupção habilitados antes de executar os scripts de inicialização, permitindo definir um ponto de interrupção em `init()` antes de iniciar.

Para conectar a um dispositivo, selecione-o em <kbd>Project ▸ Targets</kbd> e escolha <kbd>Debug ▸ Start/Attach</kbd>. A conexão pausa a execução na próxima linha Lua. O editor configura a conexão do depurador automaticamente para alvos locais e remotos compatíveis. Consulte [Alvos remotos](#remote-targets) para conhecer os requisitos de conexão ou veja como [conectar um depurador externo](#native-dap-connections).

![visão geral](images/debugging/overview.png)

Assim que o depurador é anexado, você tem controle da execução do jogo pelos botões de controle do depurador no console ou pelo menu <kbd>Debug</kbd>:

Break
: ![pausar](images/debugging/pause.svg){width=60px .left}
  Pausa a execução Lua na próxima linha do código-fonte. Você pode então inspecionar o estado do jogo, avançar passo a passo ou continuar a execução até o próximo ponto de interrupção. O ponto atual de execução é marcado no editor de código:

  ![script](images/debugging/script.png)

Continue
: ![reproduzir](images/debugging/play.svg){width=60px .left}
  Continua a execução do jogo. O código do jogo continuará executando até você pressionar pause ou até a execução atingir um breakpoint que você definiu. Se a execução parar em um breakpoint definido, o ponto de execução será marcado no editor de código sobre o marcador de breakpoint:

  ![break](images/debugging/break.png)

Stop
: ![parar](images/debugging/stop.svg){width=60px .left}
  Para o depurador. Pressionar este botão interrompe imediatamente o depurador, o desanexa do jogo e encerra o jogo em execução.

Step Over
: ![step over](images/debugging/step_over.svg){width=60px .left}
  Avança a execução do programa em um passo. Se a execução envolver a chamada de outra função Lua, a execução _não entrará na função_, mas continuará e parará na próxima linha abaixo da chamada da função. Neste exemplo, se o usuário pressionar "step over", o depurador executará o código e parará na instrução `end` abaixo da linha com a chamada à função `nextspawn()`:

  ![step](images/debugging/step.png)

::: sidenote
O avanço passo a passo segue as linhas do código-fonte Lua. Um passo pode voltar à mesma linha, por exemplo quando um loop se repete, portanto nem sempre avança para a próxima linha do arquivo.
:::

Step Into
: ![step in](images/debugging/step_in.svg){width=60px .left}
  Avança a execução do programa em um passo. Se a execução envolver a chamada de outra função Lua, a execução _entrará na função_. Chamar a função adiciona uma entrada à call stack. Você pode clicar em cada entrada na lista da call stack para ver o ponto de entrada e o conteúdo de todas as variáveis naquela closure. Aqui, o usuário entrou na função `nextspawn()`:

  ![step into](images/debugging/step_into.png)

Step Out
: ![step out](images/debugging/step_out.svg){width=60px .left}
  Continua a execução até retornar da função atual. Se você entrou na execução de uma função, pressionar o botão "step out" continuará a execução até a função retornar.

Definindo e limpando breakpoints
: Você pode definir um número arbitrário de breakpoints no seu código Lua. Quando o jogo roda com o depurador anexado, ele interromperá a execução no próximo breakpoint encontrado e aguardará mais interação sua.

  ![adicionar breakpoint](images/debugging/add_breakpoint.png)

  Para definir ou limpar um breakpoint, clique na coluna logo à direita dos números de linha no editor de código. Você também pode selecionar <kbd>Edit ▸ Toggle Breakpoint</kbd> no menu.

Desativando e ativando breakpoints
: Breakpoints podem ser temporariamente desativados sem serem removidos. Quando desativados, são ignorados durante a execução, mas podem ser reativados a qualquer momento. Clique com o botão direito no gutter do editor de código e alterne a checkbox `Enabled`. Breakpoints desativados aparecem vazados para indicar que estão inativos.

  ![desativar breakpoint](images/debugging/disable_breakpoint.png)

Definindo breakpoints condicionais
: Você pode configurar seu breakpoint para conter uma condição que precisa ser avaliada como true para que o breakpoint seja disparado. A condição pode acessar variáveis locais disponíveis na linha durante a execução do código.

  ![editar breakpoint](images/debugging/edit_breakpoint.png)

  Para editar a condição do breakpoint, clique com o botão direito na coluna logo à direita dos números de linha no editor de código ou selecione <kbd>Edit ▸ Edit Breakpoint</kbd> no menu.

Avaliando expressões Lua
: Com o jogo pausado, selecione um frame em *Call Stack*, digite uma expressão ou instrução Lua na parte inferior do console e pressione <kbd>Enter</kbd>. A avaliação usa as variáveis locais, upvalues e globais do frame selecionado. Resultados que são tabelas incluem seu conteúdo aninhado.

  ![console](images/debugging/console.png)

  Você também pode alterar valores por meio de atribuições, por exemplo `self.score = 100` em um frame no qual `self` esteja disponível. O código avaliado tem os mesmos efeitos sobre o estado do jogo que o código executado pelo próprio jogo.

Inspecionando variáveis
: Selecione um frame em *Call Stack* para inspecionar suas variáveis locais e upvalues na visualização *Variables*. Expanda `_G` para inspecionar variáveis globais, e expanda tabelas ou `self` para inspecionar seus campos. O editor preserva os caminhos expandidos, a seleção e a posição de rolagem ao avançar passo a passo, trocar de frame ou atualizar após uma avaliação, enquanto busca os valores atuais.

Desanexando o depurador
: Selecione <kbd>Debug ▸ Detach Debugger</kbd> para desconectar o depurador do jogo. O jogo continuará a execução imediatamente. Use <kbd>Debug ▸ Start/Attach</kbd> para conectar novamente sem reiniciar o jogo.

## Conexões DAP nativas {#native-dap-connections}

A engine oferece um servidor nativo do Debug Adapter Protocol (DAP) sobre TCP. Para usar um cliente DAP externo, inicie a escuta em uma engine nativa de depuração ou headless do Defold e conecte o cliente ao endereço e à porta da engine. O editor configura a escuta automaticamente quando você usa <kbd>Debug ▸ Start/Attach</kbd>.

O editor atual não pode se conectar a engines antigas que oferecem suporte apenas a MobDebug. A chamada `require "builtins.scripts.mobdebug"` não é necessária nem está disponível nas versões atuais.

### Iniciando a escuta {#starting-the-listener}

Primeiro, faça o build do projeto. No diretório do projeto que contém `build/default/game.projectc`, execute a engine nativa de depuração com estas [substituições de configuração na inicialização](/manuals/project-settings/#setting-config-values-on-engine-startup):

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

Conecte seu cliente DAP a `127.0.0.1:8172`. A engine aguarda o cliente configurar os pontos de interrupção antes de executar os scripts de inicialização.

| Configuração | Padrão | Finalidade |
| --- | --- | --- |
| `debugger.enabled` | `0` | Defina como `1` para iniciar a escuta durante a inicialização da engine. |
| `debugger.address` | `127.0.0.1` | Endereço IPv4 de escuta. O padrão aceita conexões do mesmo computador. |
| `debugger.port` | `8172` | Porta TCP de escuta. Use `0` para selecionar uma porta disponível. |
| `debugger.wait` | `0` | Defina como `1` para aguardar a configuração do cliente de depuração antes de executar os scripts de inicialização. |

Você também pode adicionar esses valores à [seção Debugger de game.project](/manuals/project-settings/#debugger). O editor configura a escuta automaticamente para <kbd>Debug ▸ Start/Attach</kbd>, portanto a configuração manual só é necessária quando você inicia a escuta por conta própria.

O log da engine informa o endereço e a porta selecionados. Com `debugger.wait=0`, o jogo inicia imediatamente e você pode conectar depois. Com `debugger.wait=1`, ele aguarda o cliente concluir a configuração da sessão, incluindo os pontos de interrupção. Em inicializações locais de depuração, o editor seleciona automaticamente uma porta disponível.

Desconectar um cliente retoma a execução e mantém a escuta disponível para outra conexão. Uma desconexão durante a espera pela configuração de inicialização também libera a engine. Se a escuta não puder iniciar, a engine registra o erro e continua a inicialização; você pode tentar novamente a partir do Lua com `debugger.start(0)` para selecionar uma porta disponível.

### Habilitando a escuta durante a execução {#enabling-the-listener-while-running}

Para habilitar a escuta a partir de um script sem reiniciar o jogo:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` retorna imediatamente a porta de escuta. Não aguarda um cliente nem pausa o jogo. Argumentos omitidos usam `debugger.port` e `debugger.address`; passar `0` seleciona uma porta disponível. Chamadas repetidas retornam a porta da escuta existente e não alteram seu endereço nem sua porta. O módulo `debugger` é fornecido pelas engines nativas de depuração e headless.

A porta deve ser um número inteiro entre `0` e `65535`. Passe `nil` como primeiro argumento para substituir apenas o endereço. Argumentos inválidos ou uma falha ao vincular a escuta geram um erro Lua.

### Alvos remotos {#remote-targets}

Para uma conexão direta a partir de outro computador, vincule a escuta à interface IPv4 do dispositivo ou a `0.0.0.0` (todas as interfaces IPv4). Por exemplo, use `debugger.start(8172, "0.0.0.0")` ou adicione `--config=debugger.address=0.0.0.0` ao comando de inicialização acima. Conecte o cliente ao endereço IP real do dispositivo e permita acesso TCP à porta de escuta. `0.0.0.0` é um endereço de vinculação, não o endereço que deve ser informado no cliente.

O editor Defold solicita essa vinculação remota automaticamente e usa a porta `8172 + project.instance_index` para alvos remotos. Ele não consegue descobrir uma porta remota selecionada dinamicamente. Se você já iniciou a escuta remota em localhost ou em outra porta, reinicie a engine antes de conectar pelo editor.

O depurador pode avaliar código Lua e não possui autenticação. Habilite o acesso remoto apenas em uma rede de desenvolvimento confiável.

### Clientes externos {#external-clients}

Use um cliente que permita conectar diretamente a um servidor DAP sobre TCP. Configure seu mapeamento de código-fonte para a pasta que contém `game.project` (o argumento de conexão DAP `localRoot`). Inicie a escuta da engine primeiro e depois conecte o cliente.

#### VS Code {#vs-code}

Instale a [extensão Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`), abra a pasta que contém `game.project` no VS Code e adicione esta configuração a `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

Se o VS Code abrir um arquivo `.script`, `.gui_script` ou `.render_script` como texto simples, selecione **Lua** no indicador de linguagem da barra de status antes de definir pontos de interrupção.

Defina um ponto de interrupção, por exemplo na função `init()` de um script. Inicie a engine usando o [comando de inicialização acima](#starting-the-listener) e selecione **Attach to Defold Lua** na visualização **Run and Debug** do VS Code. Com `debugger.wait=1`, a engine executa os scripts de inicialização após o cliente instalar os pontos de interrupção. Defina `stopOnEntry` como `true` se também quiser pausar na próxima linha Lua após a conexão.

A [configuração `debugServer`](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug) do VS Code conecta diretamente à escuta TCP local da engine. O campo `address` é exigido pela configuração de conexão da extensão Lua Debug. Se alterar a porta de escuta, atualize ambos os campos. `localRoot` deve apontar para a pasta do projeto para que o cliente possa mapear os nomes dos arquivos-fonte Lua da engine aos seus arquivos.

Para uma engine remota, encaminhe sua porta DAP para localhost e coloque a porta encaminhada em ambos os campos, ou use um cliente DAP que conecte diretamente ao host remoto.

## Aba Breakpoints

  ![aba de breakpoints](images/debugging/breakpoints_tab.png)

  Ao trabalhar com vários breakpoints em scripts diferentes, a aba Breakpoints oferece uma visualização centralizada para gerenciar todos os seus breakpoints em um só lugar.

##### Controles de breakpoint individual

  Para trabalhar com breakpoints individuais:
  - Clique no ícone vermelho de lixeira para remover um breakpoint
  - Dê um duplo clique na linha (fora da área da condição) para navegar até aquela linha na Code View
  - Dê um duplo clique na célula da condição ou clique no ícone de caneta para editar breakpoints condicionais
  - Clique no botão X de limpar ao passar o mouse sobre uma célula de condição para limpar a condição

##### Operações em lote

  Selecione vários breakpoints usando Ctrl/Cmd+clique ou Shift+clique e então clique com o botão direito para realizar ações em massa. Você pode editar condições em vários breakpoints simultaneamente, alternar o estado ativo deles ou removê-los por completo.

  Os botões da barra de ferramentas permitem ativar, desativar ou alternar todos os breakpoints de uma vez, útil quando você quer executar seu jogo sem parar, mas não quer perder as posições deles. Você também pode remover todos quando terminar sua sessão de depuração.

## Biblioteca debug de Lua

Lua vem com uma biblioteca debug que é útil em algumas situações, principalmente se você precisa inspecionar detalhes internos do seu ambiente Lua. Você encontra mais informações sobre ela no [capítulo sobre a Debug Library no manual de Lua](http://www.lua.org/pil/contents.html#23).

## Checklist de depuração

Se você encontrar um erro ou se o seu jogo não se comportar como esperado, aqui está um checklist de depuração:

1. Verifique a saída do console e confirme que não há erros de runtime.

2. Adicione instruções `print` ao seu código para verificar se o código realmente está rodando.

3. Se ele não estiver rodando, verifique se você fez no editor a configuração correta necessária para o código executar. O script foi adicionado ao objeto de jogo certo? Seu script adquiriu foco de entrada? Os input-triggers estão corretos? O código de shader foi adicionado ao material? Etc.

4. Se seu código depende dos valores de variáveis (em um if-statement, por exemplo), use `print` nesses valores onde são usados ou verificados, ou inspecione-os com o depurador.

Às vezes encontrar um bug pode ser um processo difícil e demorado, exigindo que você percorra seu código pouco a pouco, verificando tudo, estreitando o código defeituoso e eliminando fontes de erro. Isso é melhor feito por um método chamado "dividir e conquistar":

1. Descubra qual metade (ou menos) do código deve conter o bug.
2. Mais uma vez, descubra qual metade dessa metade deve conter o bug.
3. Continue estreitando o código que deve causar o bug até encontrá-lo.

Boa caça!

## Depurando problemas com física {#debugging-problems-with-physics}

Se você tem problemas com física e colisões não estão funcionando como esperado, recomenda-se habilitar a depuração de física. Marque a checkbox *Debug* na seção *Physics* do arquivo *game.project*:

![configuração de depuração de física](images/debugging/physics_debug_setting.png)

Quando esta checkbox está habilitada, o Defold desenha todas as formas de colisão e pontos de contato das colisões:

![visualização de depuração de física](images/debugging/physics_debug_visualisation.png)
