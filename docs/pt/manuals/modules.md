---
title: Módulos Lua no Defold
brief: Módulos Lua permitem estruturar seu projeto e criar código de biblioteca reutilizável. Este manual explica como fazer isso no Defold.
---

# Módulos Lua

Módulos Lua permitem estruturar seu projeto e criar código de biblioteca reutilizável. Em geral, é uma boa ideia evitar duplicação nos seus projetos. O Defold permite usar a funcionalidade de módulos do Lua para incluir arquivos de script em outros arquivos de script. Isso permite encapsular funcionalidades (e dados) em um arquivo de script externo para reutilização em objetos de jogo e arquivos de script de GUI.

## Requisitando arquivos Lua

Código Lua armazenado em arquivos com extensão ".lua" em algum lugar da estrutura do seu projeto pode ser requisitado em arquivos de script e scripts de GUI. Para criar um novo arquivo de módulo Lua, clique com o botão direito na pasta onde deseja criá-lo no painel *Assets* e selecione <kbd>New... ▸ Lua Module</kbd>. Dê um nome único ao arquivo e pressione <kbd>Ok</kbd>:

![new file](images/modules/new_name.png)

Suponha que o código a seguir seja adicionado ao arquivo "`main/anim.lua`":

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

Então qualquer script pode requisitar esse arquivo e usar a função:

```lua
require "main.anim"

function update(self, dt)
    -- atualiza a posição, define a direção etc.
    ...

    -- define a animação
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

A função `require` carrega o módulo informado. Ela começa procurando na tabela `package.loaded` para determinar se o módulo já foi carregado. Se tiver sido, `require` retorna o valor armazenado em `package.loaded[module_name]`. Caso contrário, ela carrega e avalia o arquivo por meio de um carregador.

A sintaxe da string de nome de arquivo fornecida a `require` é um pouco especial. Lua substitui caracteres '.' na string do nome de arquivo por separadores de caminho: '/' no macOS e Linux e '\\' no Windows.

Observe que normalmente é uma má ideia usar o escopo global para armazenar estado e definir funções como fizemos acima. Você corre o risco de colisões de nomes, de expor o estado do módulo ou de introduzir acoplamento entre os usuários do módulo.

## Módulos

Para encapsular dados e funções, Lua usa _módulos_. Um módulo Lua é uma tabela Lua comum usada para conter funções e dados. A tabela é declarada como local para não poluir o escopo global:

```lua
local M = {}

-- privado
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

O módulo então pode ser usado. Novamente, é preferível atribuí-lo a uma variável local:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Hot reload de módulos

Considere um módulo simples:

```lua
-- module.lua
local M = {} -- cria uma nova tabela no escopo local
M.value = 4711
return M
```

E um usuário do módulo:

```lua
local m = require "module"
print(m.value) --> "4711" (mesmo se "module.lua" for alterado e recarregado com hot reload)
```

Se você fizer hot reload do arquivo do módulo, o código é executado novamente, mas nada acontece com `m.value`. Por quê?

Primeiro, a tabela criada em "module.lua" é criada no escopo local e uma _referência_ a essa tabela é retornada ao usuário. Recarregar "module.lua" avalia o código do módulo novamente, mas isso cria uma nova tabela no escopo local em vez de atualizar a tabela à qual `m` se refere.

Segundo, Lua coloca arquivos requisitados em cache. Na primeira vez que um arquivo é requisitado, ele é colocado na tabela [`package.loaded`](/ref/package/#package.loaded) para que possa ser lido mais rapidamente em chamadas `require` posteriores. Você pode forçar um arquivo a ser relido do disco definindo a entrada do arquivo como nil: `package.loaded["my_module"] = nil`.

Para fazer hot reload corretamente de um módulo, você precisa recarregar o módulo, redefinir o cache e então recarregar todos os arquivos que usam o módulo. Isso está longe do ideal.

Em vez disso, você pode considerar uma alternativa para usar _durante o desenvolvimento_: colocar a tabela do módulo no escopo global e fazer `M` referenciar a tabela global em vez de criar uma nova tabela cada vez que o arquivo é avaliado. Recarregar o módulo então altera o conteúdo da tabela global:

```lua
--- module.lua

-- Troque por local M = {} quando terminar
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Módulos e estado

Módulos com estado mantêm um estado interno compartilhado entre todos os usuários do módulo e podem ser comparados a singletons:

```lua
local M = {}

-- todos os usuários do módulo compartilharão esta tabela
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Um módulo sem estado, por outro lado, não mantém nenhum estado interno. Em vez disso, ele fornece um mecanismo para externalizar o estado em uma tabela separada, local ao usuário do módulo. Aqui estão algumas formas diferentes de implementar isso:

Usando uma tabela de estado
: Talvez a abordagem mais simples seja usar uma função construtora que retorna uma nova tabela contendo apenas estado. O estado é passado explicitamente para o módulo como o primeiro parâmetro de toda função que manipula a tabela de estado.

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  Use o módulo assim:
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Usando metatables
: Outra abordagem é usar uma função construtora que retorna uma nova tabela com estado e as funções públicas do módulo sempre que é chamada:

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self é adicionado como primeiro argumento ao usar a notação :
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  Use o módulo assim:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" é adicionado como primeiro argumento ao usar a notação :
  print(my_state:get_state()) --> 43
  ```

Usando closures
: Uma terceira forma é retornar uma closure contendo todo o estado e as funções. Não é necessário passar a instância como argumento (nem explicitamente nem implicitamente usando o operador de dois-pontos), como acontece com metatables. Esse método também é um pouco mais rápido do que usar metatables, pois as chamadas de função não precisam passar pelos metamétodos `__index`; porém, cada closure contém sua própria cópia dos métodos, então o consumo de memória é maior.

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  Use o módulo assim:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
