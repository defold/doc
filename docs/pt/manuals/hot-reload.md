---
title: Hot reload
brief: Este manual explica o recurso de hot reload no Defold.
---

# Hot reload de recursos

O Defold permite fazer hot reload de recursos. Durante o desenvolvimento de um jogo, esse recurso ajuda a acelerar muito certas tarefas. Ele permite alterar código e conteúdo de um jogo enquanto ele está em execução. Casos de uso comuns incluem:

- Ajustar parâmetros de gameplay em scripts Lua.
- Editar e ajustar elementos gráficos (como efeitos de partículas ou elementos de GUI) e ver os resultados no contexto correto.
- Editar e ajustar código de shader e ver os resultados no contexto correto.
- Facilitar testes do jogo reiniciando fases, definindo estados e assim por diante, sem parar o jogo.

## Como fazer hot reload

Inicie o jogo a partir do editor (<kbd>Projeto ▸ Compilar</kbd>).

Para recarregar um recurso atualizado, basta selecionar o item de menu <kbd>Arquivo ▸ Recarregar</kbd> ou pressionar o atalho correspondente no teclado:

![Reloading resources](images/hot-reload/menu.png)

## Hot reload no dispositivo

O hot reload funciona tanto em dispositivos quanto no desktop. Para usá-lo em um dispositivo, execute uma build de depuração do seu jogo, ou o [aplicativo de desenvolvimento](/manuals/dev-app) no seu dispositivo móvel, e então escolha-o como alvo no editor:

![target device](images/hot-reload/target.png)

Agora, quando você compilar e executar, o editor envia todos os assets para o app em execução no dispositivo e inicia o jogo. A partir daí, qualquer arquivo que você recarregar por hot reload será atualizado no dispositivo.

Por exemplo, para adicionar alguns botões a uma GUI que está sendo exibida em um jogo em execução no seu telefone, basta abrir o arquivo GUI:

![reload gui](images/hot-reload/gui.png)

Adicione os novos botões, salve e faça hot reload do arquivo GUI. Agora você pode ver os novos botões na tela do telefone:

![reloaded gui](images/hot-reload/gui-reloaded.png)

Quando você faz hot reload de um arquivo, a engine imprime cada arquivo de recurso recarregado no console.

## Recarregando scripts

Qualquer arquivo de script Lua recarregado será executado novamente no ambiente Lua em execução.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

Alterar `my_value` para 11 e fazer hot reload do arquivo terá efeito imediato:

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

Observe que o hot reload não altera a execução das funções de ciclo de vida. Não há chamada para `init()` no hot reload, por exemplo. No entanto, se você redefinir as funções de ciclo de vida, as novas versões serão usadas.

## Recarregando módulos Lua

Desde que você adicione variáveis ao escopo global em um arquivo de módulo, recarregar o arquivo alterará essas variáveis globais:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- faça hot reload de "my_module.lua" e o novo valor será impresso
end
```

Um padrão comum de módulo Lua é construir uma tabela local, preenchê-la e então retorná-la:

```lua
--- my_module.lua
local M = {} -- um novo objeto tabela é criado aqui
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- imprimirá 10 mesmo que você altere e faça hot reload de "my_module.lua"
end
```

Alterar e recarregar "my_module.lua" _não_ mudará o comportamento de "user.script". Consulte o [manual de Módulos](/manuals/modules) para mais informações sobre o motivo e sobre como evitar essa armadilha.

## A função on_reload()

Todo componente de script pode definir uma função `on_reload()`. Se ela existir, será chamada sempre que o script for recarregado. Isso é útil para inspecionar ou alterar dados, enviar mensagens e assim por diante:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Recarregando código de shader

Ao recarregar vertex shaders e fragment shaders, o código GLSL é recompilado pelo driver gráfico e enviado para a GPU. Se o código do shader causar um crash, o que é fácil acontecer já que GLSL é escrito em um nível muito baixo, ele derrubará a engine.
