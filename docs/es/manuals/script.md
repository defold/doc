---
title: Escribir lógica de juego en scripts
brief: Este manual describe cómo agregar lógica de juego usando componentes script.
---

# Scripts

Los componentes script te permiten crear lógica de juego usando el [lenguaje de programación Lua](/manuals/lua).


## Tipos de script

Hay tres tipos de script Lua en Defold, cada uno con distintas bibliotecas de Defold disponibles.

Scripts de objeto de juego
: Extensión _.script_. Estos scripts se agregan a objetos de juego exactamente como cualquier otro [componente](/manuals/components), y Defold ejecutará el código Lua como parte de las funciones del ciclo de vida del motor. Los scripts de objeto de juego se suelen usar para controlar objetos de juego y la lógica que une el juego con la carga de niveles, las reglas del juego y demás. Los scripts de objeto de juego tienen acceso a las funciones [GO](/ref/go) y a todas las funciones de la biblioteca de Defold excepto las funciones [GUI](/ref/gui) y [Render](/ref/render).


Scripts GUI
: Extensión _.gui_script_. Ejecutados por componentes GUI, suelen contener la lógica necesaria para mostrar elementos GUI como HUD, menús, etc. Defold ejecutará el código Lua como parte de las funciones del ciclo de vida del motor. Los scripts GUI tienen acceso a las funciones [GUI](/ref/gui) y a todas las funciones de la biblioteca de Defold excepto las funciones [GO](/ref/go) y [Render](/ref/render).


Scripts de render
: Extensión _.render_script_. Ejecutados por el pipeline de renderizado, contienen la lógica necesaria para renderizar todos los gráficos de la app o el juego en cada frame. El script de render tiene un lugar especial en el ciclo de vida de tu juego. Puedes encontrar detalles en la [documentación del ciclo de vida de la aplicación](/manuals/application-lifecycle). Los scripts de render tienen acceso a las funciones [Render](/ref/render) y a todas las funciones de la biblioteca de Defold excepto las funciones [GO](/ref/go) y [GUI](/ref/gui).


## Ejecución de scripts, callbacks y self

Defold ejecuta scripts Lua como parte del ciclo de vida del motor y expone el ciclo de vida a través de un conjunto de funciones callback predefinidas. Cuando agregas un componente script a un objeto de juego, el script pasa a formar parte del ciclo de vida del objeto de juego y de sus componentes. El script se evalúa en el contexto Lua cuando se carga; luego el motor ejecuta las siguientes funciones y pasa como parámetro una referencia a la instancia actual del componente script. Puedes usar esta referencia `self` para almacenar estado en la instancia del componente.

::: important
`self` es un objeto `userdata` que actúa como una tabla Lua, pero no puedes iterar sobre él con `pairs()` o `ipairs()` ni puedes imprimirlo usando `pprint()`.
:::

#### `init(self)`
Se llama cuando se inicializa el componente.

```lua
function init(self)
  -- Estas variables están disponibles durante toda la vida de la instancia del componente
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
Se llama cuando se elimina el componente. Esto es útil para hacer limpieza, por ejemplo si has generado objetos de juego que deben eliminarse cuando se elimina el componente.

```lua
function final(self)
  if self.my_var == "something" then
      -- hacer algo de limpieza
  end
end
```

#### `fixed_update(self, dt)`
Actualización independiente de la tasa de frames. El parámetro `dt` contiene el tiempo delta desde la última actualización. Esta función se llama de `0-N` veces según la temporización de frames y la frecuencia de actualización fija. Solo se llama cuando `Physics`-->`Use Fixed Timestep` está activado y `Engine`-->`Fixed Update Frequency` es mayor que 0 en *game.project*. Es útil cuando quieres manipular objetos de física a intervalos regulares para lograr una simulación física estable.

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
Se llama una vez por frame después del callback `fixed_update` de todos los scripts (si Fixed Timestep está activado). El parámetro `dt` contiene el tiempo delta desde el último frame.

```lua
function update(self, dt)
  self.age = self.age + dt -- aumentar la edad con el intervalo de tiempo
end
```

#### `late_update(self, dt)`
Se llama una vez por frame después del callback `update` de todos los scripts, pero justo antes del render. El parámetro `dt` contiene el tiempo delta desde el último frame.

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
Cuando se envían mensajes al componente script mediante [`msg.post()`](/ref/msg#msg.post), el motor llama a esta función del componente receptor. Aprende [más sobre el paso de mensajes](/manuals/message-passing).

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
Si este componente ha adquirido el foco de input (consulta [`acquire_input_focus`](/ref/go/#acquire_input_focus)), el motor llama a esta función cuando se registra input. Aprende [más sobre el manejo de input](/manuals/input).

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
Esta función se llama cuando el script se recarga mediante la función de hot reload del editor (<kbd>Edit ▸ Reload Resource</kbd>). Es muy útil para depurar, probar y ajustar. Aprende [más sobre hot-reload](/manuals/hot-reload).

```lua
function on_reload(self)
  print(self.age) -- imprimir la edad de este objeto de juego
end
```


## Lógica reactiva

Un objeto de juego con un componente script implementa algo de lógica. A menudo, esa lógica depende de algún factor externo. La IA de un enemigo podría reaccionar cuando el jugador está dentro de cierto radio de la IA; una puerta podría desbloquearse y abrirse como resultado de la interacción del jugador, etc.

La función `update()` te permite implementar comportamientos complejos definidos como una máquina de estados que se ejecuta en cada frame; a veces ese es el enfoque adecuado. Pero cada llamada a `update()` tiene un costo asociado. A menos que realmente necesites la función, deberías eliminarla e intentar construir la lógica de forma _reactiva_. Es más barato esperar pasivamente a que algún mensaje active una respuesta que sondear activamente el mundo del juego en busca de datos a los que responder. Además, resolver un problema de diseño de forma reactiva también suele llevar a un diseño y una implementación más limpios y estables.

Veamos un ejemplo concreto. Supón que quieres que un componente script envíe un mensaje 2 segundos después de que se haya iniciado. Luego debe esperar un mensaje de respuesta determinado y, tras recibir la respuesta, debe enviar otro mensaje 5 segundos más tarde. El código no reactivo para eso se vería más o menos así:

```lua
function init(self)
    -- Contador para llevar la cuenta del tiempo.
    self.counter = 0
    -- Lo necesitamos para llevar la cuenta de nuestro estado.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- enviar mensaje después de 2 segundos
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- enviar mensaje 5 segundos después de recibir "response"
        msg.post("another_object", "another_message")
        -- Establecer el estado en nil para no volver a llegar a este bloque de estado.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- Estado "first" completado. Entrar al siguiente
        self.state = "second"
        -- reiniciar el contador a cero
        self.counter = 0
    end
end
```

Incluso en este caso bastante simple, obtenemos una lógica bastante enredada. Es posible mejorar su aspecto con la ayuda de coroutines en un módulo (ver abajo), pero en su lugar intentemos hacerla reactiva y usar un mecanismo de temporización integrado.

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Esperar 2 s y luego llamar a send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Esperar 5 s y luego llamar a send_second()
		timer.delay(5, false, send_second)
	end
end
```

Esto es más limpio y fácil de seguir. Nos deshacemos de variables de estado internas que a menudo son difíciles de seguir a través de la lógica y que pueden provocar errores sutiles. También eliminamos por completo la función `update()`. Eso libera al motor de llamar a nuestro script 60 veces por segundo, aunque solo esté inactivo.


## Preprocesamiento

Es posible usar un preprocesador Lua y marcado especial para incluir código condicionalmente según la variante de build. Ejemplo:

```lua
-- Usa una de las siguientes palabras clave: RELEASE, DEBUG o HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE
local lives_num = 3
--#ENDIF
```

El preprocesador está disponible como una extensión de build. Aprende más sobre cómo instalarlo y usarlo en la [página de la extensión en GitHub](https://github.com/defold/extension-lua-preprocessor).


## Soporte del editor

El editor Defold admite la edición de scripts Lua con coloreado de sintaxis y autocompletado. Para completar nombres de funciones de Defold, presiona *Ctrl+Space* para abrir una lista de las funciones que coinciden con lo que estás escribiendo.

![Autocompletado](images/script/completion.png)
