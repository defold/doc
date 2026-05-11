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

Para executar o depurador, selecione <kbd>Debug ▸ Start/Attach</kbd>, o que inicia o jogo com o depurador anexado ou anexa o depurador a um jogo que já está em execução.

![visão geral](images/debugging/overview.png)

Assim que o depurador é anexado, você tem controle da execução do jogo pelos botões de controle do depurador no console ou pelo menu <kbd>Debug</kbd>:

Break
: ![pausar](images/debugging/pause.svg){width=60px .left}
  Interrompe imediatamente a execução do jogo. O jogo será interrompido no ponto atual. Agora você pode inspecionar o estado do jogo, avançar passo a passo ou continuar a execução até o próximo breakpoint. O ponto atual de execução é marcado no editor de código:

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
Uma linha de código Lua não corresponde a uma única expressão. Avançar no depurador move uma expressão por vez, o que significa que, atualmente, talvez você precise pressionar o botão de passo mais de uma vez para avançar para a próxima linha.
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
: Breakpoints podem ser temporariamente desativados sem serem removidos. Quando desativados, são ignorados durante a execução, mas podem ser reativados a qualquer momento. Clique com o botão direito no gutter do editor de código e alterne a checkbox Enabled. Breakpoints desativados aparecem vazados para indicar que estão inativos.

  ![desativar breakpoint](images/debugging/disable_breakpoint.png)

Definindo breakpoints condicionais
: Você pode configurar seu breakpoint para conter uma condição que precisa ser avaliada como true para que o breakpoint seja disparado. A condição pode acessar variáveis locais disponíveis na linha durante a execução do código.

  ![editar breakpoint](images/debugging/edit_breakpoint.png)

  Para editar a condição do breakpoint, clique com o botão direito na coluna logo à direita dos números de linha no editor de código ou selecione <kbd>Edit ▸ Edit Breakpoint</kbd> no menu.

Avaliando expressões Lua
: Com o depurador anexado e o jogo parado em um breakpoint, um runtime Lua fica disponível com o contexto atual. Digite expressões Lua na parte inferior do console e pressione <kbd>Enter</kbd> para avaliá-las:

  ![console](images/debugging/console.png)

  Atualmente não é possível modificar variáveis pelo avaliador.

Desanexando o depurador
: Selecione <kbd>Debug ▸ Detach Debugger</kbd> para desanexar o depurador do jogo. Ele continuará executando imediatamente.

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

## Depurando problemas com física

Se você tem problemas com física e colisões não estão funcionando como esperado, recomenda-se habilitar a depuração de física. Marque a checkbox *Debug* na seção *Physics* do arquivo *game.project*:

![configuração de depuração de física](images/debugging/physics_debug_setting.png)

Quando esta checkbox está habilitada, o Defold desenha todas as formas de colisão e pontos de contato das colisões:

![visualização de depuração de física](images/debugging/physics_debug_visualisation.png)
