---
title: Recarga en caliente
brief: Este manual explica la funcionalidad de recarga en caliente de Defold.
---

# Recarga de recursos en caliente

Defold te permite recargar recursos en caliente. Al desarrollar un juego, esta funcionalidad ayuda a acelerar enormemente ciertas tareas. Te permite cambiar el código y el contenido de un juego mientras se está ejecutando. Algunos casos de uso comunes son:

- Ajustar parámetros de gameplay en scripts Lua.
- Editar y ajustar elementos gráficos (como efectos de partículas o elementos GUI) y ver los resultados en el contexto adecuado.
- Editar y ajustar código shader y ver los resultados en el contexto adecuado.
- Facilitar las pruebas del juego reiniciando niveles, definiendo estados y demás, sin detener el juego.

## Cómo recargar en caliente

Inicia tu juego desde el editor (<kbd>Project ▸ Build</kbd>).

Para recargar un recurso actualizado, simplemente selecciona el elemento de menú <kbd>File ▸ Hot Reload</kbd> o presiona el atajo correspondiente en el teclado:

![Recarga de recursos](images/hot-reload/menu.png)

## Recarga en caliente en dispositivo

La recarga en caliente funciona tanto en dispositivos como en computadoras de escritorio. Para usarla en un dispositivo, ejecuta una build de depuración de tu juego, o la [app de desarrollo](/manuals/dev-app) en tu dispositivo móvil, y luego selecciona el dispositivo como objetivo de build desde el editor:

![dispositivo objetivo](images/hot-reload/target.png)

Ahora, cuando crees la build y la ejecutes, el editor sube todos los assets a la app en ejecución en el dispositivo e inicia el juego. A partir de ese momento, cualquier archivo que recargues en caliente se actualizará en el dispositivo.

Por ejemplo, para agregar un par de botones a una GUI que se está mostrando en un juego en ejecución en tu teléfono, simplemente abre el archivo GUI:

![recargar gui](images/hot-reload/gui.png)

Agrega los botones nuevos, guarda y recarga en caliente el archivo GUI. Ahora puedes ver los botones nuevos en la pantalla del teléfono:

![gui recargada](images/hot-reload/gui-reloaded.png)

Cuando recargas un archivo en caliente, el motor imprimirá en la consola cada archivo de recurso recargado.

## Recarga de scripts

Cualquier archivo script Lua que se recargue se ejecutará de nuevo en el entorno Lua en ejecución.

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

Cambiar `my_value` a 11 y recargar el archivo en caliente tendrá efecto inmediato:

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

Ten en cuenta que la recarga en caliente no altera la ejecución de las funciones de ciclo de vida. Por ejemplo, no se llama a `init()` durante la recarga en caliente. Sin embargo, si redefiniste las funciones de ciclo de vida, se usarán las versiones nuevas.

## Recarga de módulos Lua

Siempre que agregues variables al ámbito global en un archivo de módulo, recargar el archivo modificará esos valores globales:

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- recarga en caliente "my_module.lua" y se imprimirá el valor nuevo
end
```

Un patrón común de módulo Lua es construir una tabla local, poblarla y luego devolverla:

```lua
--- my_module.lua
local M = {} -- aquí se crea un objeto tabla nuevo
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- imprimirá 10 incluso si cambias y recargas en caliente "my_module.lua"
end
```

Cambiar y recargar "my_module.lua" _no_ cambiará el comportamiento de "user.script". Consulta [el manual de Módulos](/manuals/modules) para obtener más información sobre por qué sucede esto y cómo evitar este problema.

## La función on_reload()

Cada componente script puede definir una función `on_reload()`. Si existe, se llamará cada vez que se recargue el script. Esto es útil para inspeccionar o cambiar datos, enviar mensajes y demás:

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## Recarga de código shader

Al recargar vertex shaders y fragment shaders, el driver gráfico recompila el código GLSL y lo sube a la GPU. Si el código shader provoca un crash, algo fácil de hacer porque GLSL está escrito a un nivel muy bajo, también hará caer al motor.
