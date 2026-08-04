---
title: Pruebas automatizadas y verificación
brief: Este manual explica cómo diseñar, ejecutar y documentar pruebas deterministas de Defold de forma local, en un juego en ejecución, en navegadores y en integración continua.
---

# Pruebas automatizadas y verificación

Las pruebas automatizadas verifican el código y el contenido de Defold mediante evidencias explícitas y legibles por máquinas. Utiliza este manual para diseñar pruebas que funcionen por igual con scripts locales, ejecutores de CI (integración continua) y agentes de programación. Abarca pruebas de módulos, colecciones en ejecución, pruebas de navegador, automatización de runtime, comprobaciones visuales y builds headless, además de proporcionar buenas prácticas útiles.

## Niveles de verificación

Los niveles adecuados de pruebas automatizadas siguen el modelo de la pirámide de pruebas, que divide las pruebas en tres capas principales: pruebas unitarias, pruebas de integración y pruebas de extremo a extremo (E2E). En Defold puedes separar las pruebas en colecciones específicas que se pueden cargar en el bootstrap. Por lo general, conviene comenzar con la comprobación más específica y rápida que pueda detectar el problema y, después, añadir pruebas de runtime o de plataforma cuando sea necesario.

| Nivel | Evidencia adecuada |
| --- | --- |
| Validación estática | Parser, formateador, validador de recursos o comparación de archivos generados |
| Prueba de módulo | Resultados de aserciones para lógica Lua reutilizable con dependencias mínimas del motor |
| Colección en ejecución | Mensajes, componentes, input, físicas, ciclo de vida y comportamiento del motor |
| Automatización de runtime | Estado activo de la escena, input inyectado, estado de la aplicación y capturas de pantalla del runtime |
| Prueba de navegador HTML5 | Input del canvas, integración con el navegador, comportamiento del viewport y salida web |
| Prueba de plataforma | Comportamiento y renderizado de la plataforma objetivo real |
| Build y bundle | Estado de salida de Bob, informe de build, archivo y artefactos del bundle |

Una compilación correcta demuestra que el proyecto compila, pero no que el comportamiento del juego sea correcto. Una captura de pantalla no demuestra transiciones, animaciones, interacciones o flujos de juego complejos, pero las soluciones multimodales modernas pueden utilizarla para inspeccionar el aspecto de un fotograma y comprobar si los shaders y el layout visual son correctos. No obstante, para las pruebas automatizadas debes preferir aserciones deterministas siempre que la condición pueda expresarse directamente.

## Código Lua reutilizable y fácil de probar

Mantén la lógica reutilizable en módulos Lua con dependencias mínimas del motor. De este modo, las transformaciones de datos puras, reglas, máquinas de estados y cálculos se pueden probar sin construir un mundo de juego completo.

Separa el código que interactúa con el motor de la lógica que invoca. Un script puede convertir mensajes y el estado de componentes en llamadas a un módulo, mientras que las pruebas llaman al módulo directamente con entradas controladas.

Consulta el [manual sobre cómo escribir código](/manuals/writing-code) para obtener más detalles.

## Pruebas en una colección en ejecución {#tests-in-a-running-collection}

Utiliza una colección de pruebas específica cuando el comportamiento dependa de objetos de juego, componentes, mensajes, input, físicas u otros sistemas del motor.

Cada prueba debe:

1. establecer un estado conocido;
2. ejecutar un comportamiento;
3. comprobar y evaluar el resultado esperado;
4. limpiar los recursos creados;
5. emitir una descripción estructurada del resultado.

Prefiere colecciones de pruebas aisladas. Un proyecto puede seleccionar una colección bootstrap de pruebas mediante una configuración temporal del proyecto en `game.project`:

```ini
[bootstrap]
main_collection = /test/test.collectionc
```

No dejes un bootstrap temporal de pruebas en la configuración normal del proyecto. En CI, es preferible pasar a Bob un archivo de configuración específico. CI no puede cambiar el estado del repositorio; solo debe realizar cambios temporales cuando sea necesario.

Para juegos complejos, puedes crear pequeñas colecciones de "salas de desarrollo" con escenarios predefinidos y blockouts sencillos. Estas colecciones hacen que las mecánicas sean reproducibles y facilitan las pruebas durante el desarrollo sin tener que recorrer estados y secciones del juego que no estén relacionados.

### Frameworks de pruebas

Los proyectos pueden implementar un pequeño ejecutor o utilizar una [biblioteca de pruebas de la comunidad](https://defold.com/assets/?tag=testing).

Por ejemplo, [DefTest](https://defold.com/assets/deftest/) es una biblioteca de pruebas unitarias basada en Telescope. Permite utilizar suites, funciones de configuración y limpieza, aserciones, filtros por nombre, mocks de determinadas API de Defold y cobertura opcional mediante LuaCov. Las pruebas pueden ejecutarse desde una colección bootstrap específica, incluso en un bundle headless creado con Bob.

## Resultados de pruebas estructurados {#structured-test-results}

El resumen de la consola o del log de un framework puede resultar útil a los desarrolladores, pero un controlador automático desatendido necesita además un resultado de finalización explícito. Si es necesario, añade un pequeño adaptador alrededor del callback o resumen del framework para que el controlador procese con facilidad los resultados de las pruebas.

Una descripción sencilla de los resultados puede utilizar un prefijo único seguido de un objeto JSON en cada línea física de la consola:

```text
TEST {"run":"8f13","event":"suite_start","tests":2}
TEST {"run":"8f13","event":"case","name":"player_moves","status":"pass","duration_ms":3}
TEST {"run":"8f13","event":"case","name":"player_stops","status":"pass","duration_ms":2}
TEST {"run":"8f13","event":"suite_end","status":"pass","passed":2,"failed":0}
```

Un recopilador debe procesar cada línea de manera independiente, encontrar el prefijo `TEST`, analizar el JSON que lo sigue e ignorar la salida del motor que no esté relacionada.

Incluye un identificador de ejecución único para que la salida de un proceso antiguo o simultáneo no pueda completar la ejecución actual. Cada suite debe emitir un único evento final inequívoco (como `Pass`, `Failure`, `Crash`, `Timeout`, etc.).

### Recopilar la salida de la consola

Cuando un juego se ejecuta desde el editor, este proporciona tanto el historial actual de la consola como un stream continuo. Cierra el stream después de recibir el evento de finalización de la suite correspondiente, la terminación del proceso o un error, o cuando se alcance un tiempo de espera o límite de líneas configurado.

Consulta más información en el [manual de la API HTTP del editor](/manuals/editor-http-api/#reading-console-output).

### Logs guardados

Defold también puede guardar el log del juego si se activa `Write Log File` en `game.project`. Consulta [Logs del juego y del sistema](/manuals/debugging-game-and-system-logs/). Escribir el log en un archivo resulta útil para aplicaciones empaquetadas y para probar dispositivos objetivo en los que la consola del editor no está disponible.

El proyecto puede utilizar las funciones integradas `print()` y `pprint()`, o, por ejemplo, cualquier otra [biblioteca de logging](https://defold.com/assets/?tag=logging) de nuestro Asset Portal.

## Probar un juego en ejecución mediante una API de runtime

Una API de automatización de runtime puede inspeccionar y controlar un motor de depuración activo. Se puede utilizar cuando las pruebas deben encontrar objetos de runtime, inyectar input, esperar a un estado visible o capturar el resultado renderizado.

Consulta el [manual del servicio del motor](/manuals/engine-service/#automation-bridge-extension) para obtener más detalles.

El siguiente ejemplo utiliza la estructura del helper de Python de [Automation Bridge](https://github.com/defold/extension-automation-bridge). El proyecto debe incluir una versión compatible de la extensión de depuración, exponer un elemento con el id de automatización indicado y publicar el estado de aplicación `screen`:

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()

try:
    play = game.element(automation_id="play_button")
    game.click(play)
    game.wait_for_state("screen", "gameplay", timeout=5.0)
    screenshot = game.screenshot()
    print(screenshot.path)
finally:
    game.close_engine()
```

Los estados definidos por la aplicación y los ids de automatización utilizan la API Lua opcional y exclusiva para depuración de Automation Bridge, que el proyecto debe activar y publicar. Una espera de duración fija es vulnerable a la velocidad de la máquina y a los tiempos de los fotogramas; realizar consultas limitadas hasta alcanzar un estado definido es más fiable.

Automation Bridge es una extensión, no forma parte del núcleo del motor. Consulta su [referencia de la API de Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) para conocer los selectores, esperas, estados, eventos, capturas de pantalla y diagnósticos de la versión instalada.

## Pruebas de navegador para HTML5 {#browser-tests-for-html5}

El editor puede crear y servir una build HTML5 mediante su comando `build-html5` actual, como se describe en el [manual de la API HTTP del editor](/manuals/editor-http-api/#building-html5). Bob también puede crear un bundle HTML5 sin el editor.

Las herramientas externas de automatización de navegadores como Playwright, Puppeteer, Selenium, WebdriverIO o Cypress pueden:

* esperar a que el canvas de Defold y la aplicación estén listos;
* enviar input de teclado, ratón y pulsaciones táctiles emuladas;
* cambiar el tamaño del viewport;
* recopilar la salida de la consola del navegador y los errores de JavaScript;
* realizar capturas de pantalla y comparar artefactos.

El input dirigido al canvas se procesa mediante los bindings de input y callbacks `on_input()` habituales del proyecto. Prueba tanto la respuesta del juego como los puntos de integración específicos del navegador.

El método más fiable consiste en exponer un bridge de pruebas de JavaScript explícito en el archivo `index.html` personalizado. En Defold, las builds HTML5 pueden ejecutar JavaScript mediante `html5.run()`, lo que permite comunicarse con dicho bridge del lado del navegador. Para los comandos que viajan desde JavaScript de vuelta a Defold, utiliza un bridge específico entre JavaScript y el motor.

Mantén las pruebas de navegador limitadas. Distingue en el informe final entre un error al cargar la página, la ausencia del canvas, un error de JavaScript, un tiempo de espera de la prueba y una aserción fallida del juego.

## Vistas previas del editor y capturas de pantalla del runtime para la inspección visual {#editor-previews-and-runtime-screenshots}

Es posible crear una captura de pantalla de los archivos de recursos en la vista de escena predeterminada del editor abierto o de un juego en runtime.

| Método | Propósito |
| --- | --- |
| [Vista previa del editor](/manuals/editor-http-api/#rendering-scene-previews) | Layout de un recurso cargado, por ejemplo, un nivel o una GUI; composición de un atlas, inspección de un tilemap, composición estática de una escena, corrección del renderizado y los shaders del editor o creación de miniaturas para la documentación |
| [Captura de pantalla del runtime](/manuals/engine-service) | Estado renderizado de una build en ejecución en un escenario controlado |

Puedes utilizar la comparación de imágenes, por ejemplo, para pruebas de regresión. Cuando una comprobación falle, guarda la imagen de diferencias y las métricas de comparación.

Un modelo multimodal puede evaluar durante la inspección visual condiciones semánticas difíciles de expresar de otra forma, como texto recortado, controles superpuestos, estados de selección poco claros o contenido fuera de un área segura. Se recomienda tratar esa evaluación como una señal adicional con criterios explícitos, pero no como sustituto de comprobaciones lógicas deterministas ni de la comparación de imágenes.

## Pruebas headless y CI

Utiliza Bob, la herramienta de build mediante CLI, para procesos de CI independientes del editor.

Puedes utilizarla para resolver dependencias, crear una build del juego, un archivo o un bundle independiente y generar un informe JSON:

```sh
mkdir -p build/reports

java -jar bob.jar \
  --root . \
  --archive \
  --build-report-json build/reports/build-report.json \
  resolve build
```

Crea un bundle de pruebas headless con una configuración específica:

```sh
java -jar bob.jar \
  --root . \
  --settings test/test.settings \
  --platform x86_64-linux \
  --variant headless \
  --archive \
  --bundle-output build/test-bundle \
  resolve build bundle
```

Ejecuta el archivo resultante con un controlador de procesos adecuado para la plataforma. Captura su estado de salida y sus logs, establece un tiempo de espera y exige el evento estructurado de finalización de la suite.

El [manual de Bob](/manuals/bob) describe las plataformas, los archivos de configuración, los bundles, las cachés, las extensiones nativas y los informes de build.

## Informes de fallos y artefactos

Los resultados adecuados de las pruebas deben conservar evidencias suficientes para reproducir y diagnosticar un fallo:

* el nombre de la prueba, el identificador de ejecución y los detalles de la aserción;
* el tiempo transcurrido y el resultado clasificado;
* el log completo de la consola o del proceso;
* la versión de Defold, la plataforma objetivo y la configuración relevante;
* el informe de build de Bob y el estado de salida del proceso;
* el estado de runtime o snapshot de la escena cuando esté disponible;
* capturas de pantalla, diferencias respecto a la referencia, grabaciones o trazas del navegador;
* rutas o enlaces a todos los artefactos generados.

El mismo formato debe poder utilizarlo un desarrollador, un script local, un servicio de CI o un [agente de programación con IA](/manuals/ai-agents). Esto mantiene determinista la verificación incluso cuando se delega el diagnóstico o la reparación.
