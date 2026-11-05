---
title: Depuración en Defold
brief: Este manual explica las funcionalidades de depuración presentes en Defold.
---

# Depuración de la lógica del juego {#debugging-game-logic}

Defold contiene un depurador Lua integrado con una herramienta de inspección. Junto con las [herramientas de profiling](/manuals/profiling) integradas, es una herramienta potente que puede ayudar a encontrar la causa de errores en la lógica de tu juego o a analizar problemas de rendimiento.

## Depuración visual y con impresión {#print-and-visual-debugging}

La forma más sencilla de depurar tu juego en Defold es usar [depuración con impresión](http://en.wikipedia.org/wiki/Debugging#Techniques). Usa sentencias `print()` o [`pprint()`](/ref/builtins#pprint) para observar variables o indicar el flujo de ejecución. Si un objeto de juego sin script se comporta de forma extraña, puedes simplemente adjuntarle un script con el único propósito de depurar. Usar cualquiera de las funciones de impresión imprimirá en la vista *Console* del editor y en el [log del juego](/manuals/debugging-game-and-system-logs).

Además de imprimir, el motor también puede dibujar texto de depuración y líneas rectas en la pantalla. Esto se hace enviando mensajes al socket `@render`:

```lua
-- Dibuja el valor de "my_val" con texto de depuración en la pantalla
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Dibuja texto con color en la pantalla
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Dibuja una línea de depuración entre player y enemy en la pantalla
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

Los mensajes visuales de depuración agregan datos al pipeline de renderizado y se dibujan como parte del pipeline de renderizado normal.

* `"draw_line"` agrega datos que se renderizan con la función `render.draw_debug3d()` en el script de renderizado.
* `"draw_text"` se renderiza con `/builtins/fonts/debug/always_on_top.font`, que usa el material `/builtins/fonts/debug/always_on_top_font.material`.
* `"draw_debug_text"` es igual que `"draw_text"`, pero se renderiza con un color personalizado.

Ten en cuenta que probablemente querrás actualizar estos datos en cada frame, así que enviar los mensajes en la función `update()` es una buena idea.

## Ejecutar el depurador {#running-the-debugger}

El depurador Lua está disponible en builds nativas de depuración y headless. Usa un motor de la misma versión de Defold que el editor. Las builds release y web no permiten adjuntar el depurador.

Para ejecutar el depurador, selecciona <kbd>Debug ▸ Start/Attach</kbd>. Esto inicia el juego con el depurador adjunto o lo adjunta a un juego que ya está en ejecución. Al iniciar un juego para depurarlo, el editor instala los breakpoints activados antes de ejecutar los scripts de inicio, de modo que puedes definir un breakpoint en `init()` antes del lanzamiento.

Para adjuntarlo a un dispositivo, selecciónalo en <kbd>Project ▸ Targets</kbd> y elige <kbd>Debug ▸ Start/Attach</kbd>. La conexión pausa la ejecución en la siguiente línea Lua. El editor configura automáticamente la conexión del depurador para los destinos locales y remotos compatibles. Consulta [Destinos remotos](#remote-targets) para conocer los requisitos de conexión o aprende a [conectar un depurador externo](#native-dap-connections).

![overview](images/debugging/overview.png)

En cuanto el depurador está adjunto, tienes control de la ejecución del juego mediante los botones de control del depurador en la consola, o mediante el menú <kbd>Debug</kbd>:

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  Pausa la ejecución de Lua en la siguiente línea de código fuente. Ahora puedes inspeccionar el estado del juego, avanzar paso a paso o continuar hasta el siguiente breakpoint. El punto actual de ejecución se marca en el editor de código:

  ![script](images/debugging/script.png)

Continue
: ![play](images/debugging/play.svg){width=60px .left}
  Continúa ejecutando el juego. El código del juego seguirá ejecutándose hasta que presiones pausa o la ejecución llegue a un breakpoint que hayas definido. Si la ejecución se interrumpe en un breakpoint definido, el punto de ejecución se marca en el editor de código encima del marcador del breakpoint:

  ![break](images/debugging/break.png)

Stop
: ![stop](images/debugging/stop.svg){width=60px .left}
  Detiene el depurador. Al presionar este botón, el depurador se detendrá inmediatamente, se separará del juego y terminará el juego en ejecución.

Step Over
: ![step over](images/debugging/step_over.svg){width=60px .left}
  Avanza la ejecución del programa un paso. Si la ejecución implica ejecutar otra función Lua, la ejecución _no entrará en la función_, sino que continuará ejecutándose y se detendrá en la siguiente línea debajo de la llamada a la función. En este ejemplo, si el usuario presiona "Step Over", el depurador ejecutará el código y se detendrá en la sentencia `end` debajo de la línea con la llamada a la función `nextspawn()`:

  ![step](images/debugging/step.png)

::: sidenote
El avance paso a paso sigue las líneas del código fuente Lua. Un paso puede volver a la misma línea, por ejemplo al repetirse un bucle, por lo que no siempre avanza a la siguiente línea del archivo.
:::

Step Into
: ![step in](images/debugging/step_in.svg){width=60px .left}
  Avanza la ejecución del programa un paso. Si la ejecución implica ejecutar otra función Lua, la ejecución _entrará en la función_. Llamar a la función agrega una entrada al call stack. Puedes hacer click en cada entrada de la lista del call stack para ver el punto de entrada y el contenido de todas las variables en ese closure. Aquí, el usuario ha entrado en la función `nextspawn()`:

  ![step into](images/debugging/step_into.png)

Step Out
: ![step out](images/debugging/step_out.svg){width=60px .left}
  Continúa la ejecución hasta que retorne de la función actual. Si has avanzado la ejecución dentro de una función, presionar el botón "Step Out" continuará la ejecución hasta que la función retorne.

Definir y borrar breakpoints
: Puedes definir un número arbitrario de breakpoints en tu código Lua. Cuando el juego se ejecuta con el depurador adjunto, detendrá la ejecución en el siguiente breakpoint que encuentre y esperará a que interactúes de nuevo.

  ![add breakpoint](images/debugging/add_breakpoint.png)

  Para definir o borrar un breakpoint, haz click en la columna justo a la derecha de los números de línea en el editor de código. También puedes seleccionar <kbd>Edit ▸ Toggle Breakpoint</kbd> desde el menú.

Desactivar y activar breakpoints
: Los breakpoints pueden desactivarse temporalmente sin eliminarlos. Cuando están desactivados, se ignoran durante la ejecución, pero pueden volver a activarse en cualquier momento. Haz click derecho sobre él en el margen del editor de código y luego activa o desactiva la casilla `Enabled`. Los breakpoints desactivados aparecen huecos para indicar que están inactivos.

  ![disable breakpoint](images/debugging/disable_breakpoint.png)

Definir breakpoints condicionales
: Puedes configurar tu breakpoint para que contenga una condición que debe evaluarse como true para que el breakpoint se active. La condición puede acceder a las variables locales disponibles en la línea durante la ejecución del código.

  ![edit breakpoint](images/debugging/edit_breakpoint.png)

  Para editar la condición del breakpoint, haz click derecho en la columna justo a la derecha de los números de línea en el editor de código, o selecciona <kbd>Edit ▸ Edit Breakpoint</kbd> desde el menú.

Evaluar expresiones Lua
: Con el juego pausado, selecciona una entrada de *Call Stack*, escribe una expresión o sentencia Lua en la parte inferior de la consola y presiona <kbd>Enter</kbd>. La evaluación usa las variables locales, los upvalues y las variables globales de la entrada seleccionada. Los resultados que son tablas incluyen su contenido anidado.

  ![console](images/debugging/console.png)

  También puedes cambiar valores mediante asignaciones, por ejemplo `self.score = 100` en una entrada donde `self` esté disponible. El código evaluado tiene los mismos efectos sobre el estado del juego que el código ejecutado por el propio juego.

Inspeccionar variables
: Selecciona una entrada de *Call Stack* para inspeccionar sus variables locales y upvalues en la vista *Variables*. Expande `_G` para inspeccionar las variables globales, y las tablas o `self` para inspeccionar sus campos. El editor conserva las rutas expandidas, la selección y la posición de desplazamiento al avanzar, cambiar de entrada o actualizar tras una evaluación, mientras obtiene los valores actuales.

Separar el depurador
: Selecciona <kbd>Debug ▸ Detach Debugger</kbd> para separar el depurador del juego. Este continuará ejecutándose inmediatamente. Usa <kbd>Debug ▸ Start/Attach</kbd> para adjuntarlo de nuevo sin reiniciar el juego.

## Conexiones DAP nativas {#native-dap-connections}

El motor proporciona un servidor nativo de Debug Adapter Protocol (DAP) a través de TCP. Para usar un cliente DAP externo, inicia el listener en un motor nativo de Defold de depuración o headless y conecta el cliente a la dirección y el puerto del motor. El editor configura automáticamente el listener cuando usas <kbd>Debug ▸ Start/Attach</kbd>.

El editor actual no puede conectarse a motores antiguos que solo admiten MobDebug. En las versiones actuales no se necesita ni está disponible la llamada `require "builtins.scripts.mobdebug"`.

### Iniciar el listener {#starting-the-listener}

Primero crea una build de tu proyecto. Desde el directorio del proyecto que contiene `build/default/game.projectc`, ejecuta el motor nativo de depuración con estos [valores de configuración al iniciar](/manuals/project-settings/#setting-config-values-on-engine-startup):

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

Conecta tu cliente DAP a `127.0.0.1:8172`. El motor espera a que el cliente configure los breakpoints antes de ejecutar los scripts de inicio.

| Ajuste | Valor predeterminado | Propósito |
| --- | --- | --- |
| `debugger.enabled` | `0` | Establécelo en `1` para iniciar el listener al arrancar el motor. |
| `debugger.address` | `127.0.0.1` | Dirección IPv4 en la que se escuchan conexiones. El valor predeterminado acepta conexiones desde la misma computadora. |
| `debugger.port` | `8172` | Puerto TCP de escucha. Usa `0` para seleccionar un puerto disponible. |
| `debugger.wait` | `0` | Establécelo en `1` para esperar a que el cliente del depurador configure la sesión antes de ejecutar los scripts de inicio. |

También puedes agregar estos valores a la [sección Debugger de game.project](/manuals/project-settings/#debugger). El editor configura automáticamente el listener para <kbd>Debug ▸ Start/Attach</kbd>, por lo que solo necesitas configurarlo manualmente cuando lo inicias por tu cuenta.

El log del motor indica la dirección y el puerto seleccionados. Con `debugger.wait=0`, el juego se inicia inmediatamente y puedes adjuntar el depurador después. Con `debugger.wait=1`, espera hasta que el cliente termine de configurar la sesión, incluidos los breakpoints. En los lanzamientos locales de depuración, el editor selecciona automáticamente un puerto disponible.

Al desconectar un cliente se reanuda la ejecución y el listener queda disponible para otra conexión. Desconectar mientras se espera la configuración de inicio también libera al motor. Si el listener no puede iniciarse, el motor registra el error y continúa arrancando; puedes reintentarlo desde Lua con `debugger.start(0)` para seleccionar un puerto disponible.

### Activar el listener durante la ejecución {#enabling-the-listener-while-running}

Para activar el listener desde un script sin reiniciar el juego:

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` devuelve inmediatamente el puerto de escucha. No espera a un cliente ni pausa el juego. Los argumentos omitidos usan `debugger.port` y `debugger.address`; pasar `0` selecciona un puerto disponible. Las llamadas sucesivas devuelven el puerto del listener existente y no cambian su dirección ni su puerto. Los motores nativos de depuración y headless proporcionan el módulo `debugger`.

El puerto debe ser un entero entre `0` y `65535`. Pasa `nil` como primer argumento para cambiar solo la dirección. Los argumentos no válidos o un fallo al vincular el listener generan un error Lua.

### Destinos remotos {#remote-targets}

Para conectar directamente desde otra computadora, vincula el listener a la interfaz IPv4 del dispositivo o a `0.0.0.0` (todas las interfaces IPv4). Por ejemplo, usa `debugger.start(8172, "0.0.0.0")` o agrega `--config=debugger.address=0.0.0.0` al comando de inicio anterior. Conecta el cliente a la dirección IP real del dispositivo y permite el acceso TCP al puerto de escucha. `0.0.0.0` es una dirección de vinculación, no la dirección que debes introducir en el cliente.

El editor Defold solicita esta vinculación remota automáticamente y usa el puerto `8172 + project.instance_index` para destinos remotos. No puede descubrir un puerto remoto seleccionado dinámicamente. Si ya iniciaste el listener remoto en localhost o en otro puerto, reinicia el motor antes de adjuntarlo desde el editor.

El depurador puede evaluar Lua y no tiene autenticación. Activa el acceso remoto únicamente en una red de desarrollo de confianza.

### Clientes externos {#external-clients}

Usa un cliente que permita adjuntarse directamente a un servidor DAP por TCP. Configura su correspondencia de archivos fuente con la carpeta que contiene `game.project` (el argumento DAP `localRoot` de attach). Inicia primero el listener del motor y después adjunta el cliente.

#### VS Code

Instala la [extensión Lua Debug](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug) (`actboy168.lua-debug`), abre en VS Code la carpeta que contiene `game.project` y agrega esta configuración a `.vscode/launch.json`:

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

Si VS Code abre un archivo `.script`, `.gui_script` o `.render_script` como texto sin formato, selecciona **Lua** en el indicador de lenguaje de la barra de estado antes de definir breakpoints.

Define un breakpoint, por ejemplo en la función `init()` de un script. Inicia el motor con el [comando de inicio anterior](#starting-the-listener) y selecciona **Attach to Defold Lua** en la vista **Run and Debug** de VS Code. Con `debugger.wait=1`, el motor ejecuta los scripts de inicio después de que el cliente instale los breakpoints. Establece `stopOnEntry` en `true` si también quieres pausar en la siguiente línea Lua después de adjuntarlo.

El [ajuste `debugServer` de VS Code](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug) conecta directamente con el listener TCP local del motor. El campo `address` es obligatorio en la configuración de attach de la extensión Lua Debug. Si cambias el puerto de escucha, actualiza ambos campos. `localRoot` debe apuntar a la carpeta del proyecto para que el cliente pueda asociar los nombres de código fuente Lua del motor con tus archivos.

Para un motor remoto, reenvía su puerto DAP a localhost y coloca el puerto reenviado en ambos campos, o usa un cliente DAP que se conecte directamente al host remoto.

## Pestaña Breakpoints {#breakpoints-tab}

  ![breakpoints tab](images/debugging/breakpoints_tab.png)

  Cuando trabajas con múltiples breakpoints en distintos scripts, la pestaña Breakpoints proporciona una vista centralizada para gestionar todos tus breakpoints en un solo lugar.

##### Controles de breakpoints individuales {#individual-breakpoint-controls}

  Para trabajar con breakpoints individuales:
  - Haz click en el icono rojo de papelera para eliminar un breakpoint
  - Haz doble click en la fila (fuera del área de condición) para navegar a esa línea en Code View
  - Haz doble click en la celda de condición o haz click en el icono de lápiz para editar breakpoints condicionales
  - Haz click en el botón X de borrado al pasar el cursor sobre una celda de condición para borrar la condición

##### Operaciones en lote {#batch-operations}

  Selecciona múltiples breakpoints usando Ctrl/Cmd+click o Shift+click, y luego haz click derecho para realizar acciones en bloque. Puedes editar condiciones en varios breakpoints simultáneamente, alternar su estado activo o eliminarlos por completo.

  Los botones de la barra de herramientas te permiten activar, desactivar o alternar todos los breakpoints a la vez, lo que es útil cuando quieres ejecutar tu juego sin detenerte, pero no quieres perder sus posiciones. También puedes eliminarlos todos cuando termines tu sesión de depuración.

## Biblioteca debug de Lua {#lua-debug-library}

Lua viene con una biblioteca debug que resulta útil en algunas situaciones, especialmente si necesitas inspeccionar los detalles internos de tu entorno Lua. Puedes encontrar más información sobre ella en [el capítulo sobre la Debug Library en el manual de Lua](http://www.lua.org/pil/contents.html#23).

## Checklist de depuración {#debugging-checklist}

Si encuentras un error o si tu juego no se comporta como esperabas, aquí tienes un checklist de depuración:

1. Revisa la salida de la consola y verifica que no haya errores de runtime.

2. Agrega sentencias `print` a tu código para verificar que el código realmente se está ejecutando.

3. Si no se está ejecutando, comprueba que hayas hecho la configuración adecuada en el editor requerida para que el código se ejecute. ¿El script está agregado al objeto de juego correcto? ¿Tu script ha adquirido foco de input? ¿Los input-triggers son correctos? ¿El código del shader está agregado al material? Etc.

4. Si tu código depende de los valores de variables (en una sentencia `if`, por ejemplo), usa `print` con esos valores donde se usan o se comprueban, o inspecciónalos con el depurador.

A veces encontrar un bug puede ser un proceso difícil y lento, que requiere recorrer tu código poco a poco, revisar todo, acotar el código defectuoso y eliminar fuentes de error. Esto se hace mejor con un método llamado "divide y vencerás":

1. Determina qué mitad (o menos) del código debe contener el bug.
2. De nuevo, determina qué mitad, de esa mitad, debe contener el bug.
3. Continúa acotando el código que debe causar el bug hasta que lo encuentres.

¡Buena caza!

## Depuración de problemas con físicas {#debugging-problems-with-physics}

Si tienes problemas con físicas y las colisiones no funcionan como se esperaba, se recomienda activar la depuración de físicas. Marca la casilla *Debug* en la sección *Physics* del archivo *game.project*:

![physics debug setting](images/debugging/physics_debug_setting.png)

Cuando esta casilla está marcada, Defold dibujará todas las formas de colisión y los puntos de contacto de las colisiones:

![physics debug visualization](images/debugging/physics_debug_visualisation.png)
