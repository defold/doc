---
title: Depuración en Defold
brief: Este manual explica las funcionalidades de depuración presentes en Defold.
---

# Depuración de la lógica del juego

Defold contiene un depurador Lua integrado con una herramienta de inspección. Junto con las [herramientas de profiling](/manuals/profiling) integradas, es una herramienta potente que puede ayudar a encontrar la causa de errores en la lógica de tu juego o a analizar problemas de rendimiento.

## Depuración visual y con impresión

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

## Ejecutar el depurador

Para ejecutar el depurador, selecciona <kbd>Debug ▸ Start/Attach</kbd>, que inicia el juego con el depurador adjunto o adjunta el depurador a un juego que ya está en ejecución.

![overview](images/debugging/overview.png)

En cuanto el depurador está adjunto, tienes control de la ejecución del juego mediante los botones de control del depurador en la consola, o mediante el menú <kbd>Debug</kbd>:

Break
: ![pause](images/debugging/pause.svg){width=60px .left}
  Interrumpe la ejecución del juego inmediatamente. El juego se detendrá en su punto actual. Ahora puedes inspeccionar el estado del juego, avanzar paso a paso o continuar ejecutándolo hasta el siguiente breakpoint. El punto actual de ejecución se marca en el editor de código:

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
Una línea de código Lua no corresponde a una sola expresión. Avanzar paso a paso en el depurador avanza una expresión a la vez, lo que significa que actualmente puede que tengas que presionar el botón de paso más de una vez para avanzar a la siguiente línea.
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
: Con el depurador adjunto y el juego detenido en un breakpoint, hay un runtime Lua disponible con el contexto actual. Escribe expresiones Lua en la parte inferior de la consola y presiona <kbd>Enter</kbd> para evaluarlas:

  ![console](images/debugging/console.png)

  Actualmente no es posible modificar variables mediante el evaluador.

Separar el depurador
: Selecciona <kbd>Debug ▸ Detach Debugger</kbd> para separar el depurador del juego. El juego continuará ejecutándose inmediatamente.

## Pestaña Breakpoints

  ![breakpoints tab](images/debugging/breakpoints_tab.png)

  Cuando trabajas con múltiples breakpoints en distintos scripts, la pestaña Breakpoints proporciona una vista centralizada para gestionar todos tus breakpoints en un solo lugar.

##### Controles de breakpoints individuales

  Para trabajar con breakpoints individuales:
  - Haz click en el icono rojo de papelera para eliminar un breakpoint
  - Haz doble click en la fila (fuera del área de condición) para navegar a esa línea en Code View
  - Haz doble click en la celda de condición o haz click en el icono de lápiz para editar breakpoints condicionales
  - Haz click en el botón X de borrado al pasar el cursor sobre una celda de condición para borrar la condición

##### Operaciones en lote

  Selecciona múltiples breakpoints usando Ctrl/Cmd+click o Shift+click, y luego haz click derecho para realizar acciones en bloque. Puedes editar condiciones en varios breakpoints simultáneamente, alternar su estado activo o eliminarlos por completo.

  Los botones de la barra de herramientas te permiten activar, desactivar o alternar todos los breakpoints a la vez, lo que es útil cuando quieres ejecutar tu juego sin detenerte, pero no quieres perder sus posiciones. También puedes eliminarlos todos cuando termines tu sesión de depuración.

## Biblioteca debug de Lua

Lua viene con una biblioteca debug que resulta útil en algunas situaciones, especialmente si necesitas inspeccionar los detalles internos de tu entorno Lua. Puedes encontrar más información sobre ella en [el capítulo sobre la Debug Library en el manual de Lua](http://www.lua.org/pil/contents.html#23).

## Checklist de depuración

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
