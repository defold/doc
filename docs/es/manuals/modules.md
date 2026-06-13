---
title: Módulos Lua en Defold
brief: Los módulos Lua te permiten estructurar tu proyecto y crear código de biblioteca reutilizable. Este manual explica cómo hacerlo en Defold.
---

# Módulos Lua

Los módulos Lua te permiten estructurar tu proyecto y crear código de biblioteca reutilizable. En general, es una buena idea evitar la duplicación en tus proyectos. Defold te permite usar la funcionalidad de módulos de Lua para incluir archivos script en otros archivos script. Esto te permite encapsular funcionalidad (y datos) en un archivo script externo para reutilizarlo en archivos script de objetos de juego y GUI.

## Cargar archivos Lua con `require`

El código Lua guardado en archivos con extensión ".lua" en cualquier lugar de la estructura de tu proyecto de juego se puede cargar con `require` desde archivos script y archivos de script GUI. Para crear un nuevo archivo de módulo Lua, haz click derecho en la carpeta donde quieres crearlo en la vista *Assets* y selecciona <kbd>New... ▸ Lua Module</kbd>. Dale al archivo un nombre único y presiona <kbd>Ok</kbd>:

![archivo nuevo](images/modules/new_name.png)

Supongamos que se agrega el siguiente código al archivo "`main/anim.lua`":

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

Entonces cualquier script puede cargar este archivo con `require` y usar la función:

```lua
require "main.anim"

function update(self, dt)
    -- actualiza la posición, define la dirección, etc.
    ...

    -- define la animación
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

La función `require` carga el módulo dado. Empieza buscando en la tabla `package.loaded` para determinar si el módulo ya está cargado. Si lo está, `require` devuelve el valor guardado en `package.loaded[module_name]`. De lo contrario, carga y evalúa el archivo mediante un cargador.

La sintaxis del string de nombre de archivo proporcionado a `require` es un poco especial. Lua reemplaza los caracteres `.` en el string de nombre de archivo por separadores de ruta: `/` en macOS y Linux, y `\\` en Windows.

Ten en cuenta que normalmente es mala idea usar el ámbito global para guardar estado y definir funciones como hicimos arriba. Te arriesgas a tener colisiones de nombres, exponer el estado del módulo o introducir acoplamiento entre los usuarios del módulo.

## Módulos

Para encapsular datos y funciones, Lua usa _módulos_. Un módulo Lua es una tabla Lua normal que se usa para contener funciones y datos. La tabla se declara local para no contaminar el ámbito global:

```lua
local M = {}

-- privado
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

Luego se puede usar el módulo. De nuevo, es preferible asignarlo a una variable local:

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## Recarga en caliente de módulos

Considera un módulo simple:

```lua
-- module.lua
local M = {} -- crea una tabla nueva en el ámbito local
M.value = 4711
return M
```

Y un usuario del módulo:

```lua
local m = require "module"
print(m.value) --> "4711" (incluso si "module.lua" se cambia y se recarga en caliente)
```

Si recargas en caliente el archivo de módulo, el código se ejecuta de nuevo, pero no ocurre nada con `m.value`. ¿Por qué ocurre esto?

Primero, la tabla creada en "module.lua" se crea en el ámbito local y se devuelve al usuario una _referencia_ a esa tabla. Recargar "module.lua" evalúa de nuevo el código del módulo, pero eso crea una tabla nueva en el ámbito local en lugar de actualizar la tabla a la que hace referencia `m`.

En segundo lugar, Lua almacena en caché los archivos cargados con `require`. La primera vez que se requiere un archivo, se coloca en la tabla [`package.loaded`](/ref/package/#package.loaded) para que se pueda leer más rápido en llamadas posteriores a `require`. Puedes forzar que un archivo se vuelva a leer desde el disco estableciendo la entrada del archivo en `nil`: `package.loaded["my_module"] = nil`.

Para recargar correctamente un módulo en caliente, necesitas recargar el módulo, restablecer la caché y luego recargar todos los archivos que usan el módulo. Esto está lejos de ser óptimo.

En su lugar, podrías considerar una solución alternativa para usar _durante el desarrollo_: coloca la tabla del módulo en el ámbito global y haz que `M` se refiera a la tabla global en lugar de crear una tabla nueva cada vez que se evalúe el archivo. Recargar el módulo cambiará entonces el contenido de la tabla global:

```lua
--- module.lua

-- Reemplaza por local M = {} al terminar
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## Módulos y estado

Los módulos con estado mantienen un estado interno que se comparte entre todos los usuarios del módulo y se puede comparar con singletons:

```lua
local M = {}

-- todos los usuarios del módulo compartirán esta tabla
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

Un módulo sin estado, por otro lado, no mantiene ningún estado interno. En su lugar, proporciona un mecanismo para externalizar el estado en una tabla separada que es local para el usuario del módulo. Estas son algunas formas distintas de implementar esto:

Usar una tabla de estado
: Tal vez el enfoque más sencillo sea usar una función constructora que devuelva una tabla nueva que contenga solo estado. El estado se pasa explícitamente al módulo como primer parámetro de cada función que manipula la tabla de estado.

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

  Usa el módulo así:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

Usar metatablas
: Otro enfoque es usar una función constructora que devuelva una tabla nueva con estado y las funciones públicas del módulo cada vez que se la llama:

  ```lua
  local M = {}

  function M:alter_state(v)
      -- self se agrega como primer argumento al usar la notación :
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

  Usa el módulo así:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" se agrega como primer argumento al usar la notación :
  print(my_state:get_state()) --> 43
  ```

Usar closures
: Una tercera forma es devolver un closure que contenga todo el estado y las funciones. No es necesario pasar la instancia como argumento (ni explícitamente ni de forma implícita usando el operador de dos puntos) como al usar metatablas. Este método también es algo más rápido que usar metatablas, ya que las llamadas a funciones no necesitan pasar por los metamétodos `__index`, pero cada closure contiene su propia copia de los métodos, por lo que el consumo de memoria es mayor.

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

  Usa el módulo así:

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state())
  ```
