---
title: Automatización en Defold
brief: Este manual presenta las interfaces de automatización de Defold y explica cómo elegir entre flujos de trabajo del editor, de runtime, de línea de comandos, de pruebas y dirigidos por agentes.
---

# Automatización en Defold

Este manual ofrece una descripción general y enlaces a los manuales específicos de cada tema.

Defold permite automatizar tareas en varios niveles. Elegir una interfaz adecuada para la tarea es uno de los aspectos más importantes de una automatización eficaz. La siguiente tabla puede ayudarte a elegir la interfaz más sencilla para una acción determinada:

| Capa | Propósito |
| --- | --- |
| [Scripts del editor](/manuals/editor-scripts) | Comandos personalizados y flujos de trabajo o integraciones del editor que agilizan las pruebas y el desarrollo, por ejemplo, la creación de niveles y assets |
| [Scripts de interfaz del editor](/manuals/editor-scripts-ui/) | Herramientas visuales, popups, configuradores o interfaces de usuario personalizados mediante scripts del editor |
| [API HTTP del editor](/manuals/editor-http-api) | Controlar el proyecto abierto en el editor Defold mediante operaciones OpenAPI, recursos del proyecto, builds, comandos del editor, vistas previas, preferencias, salida de la consola o scripts del editor para operaciones personalizadas, herramientas externas, integraciones con IDE y controladores de pruebas |
| [CLI de Bob](/manuals/bob) | Crear una build del proyecto, archivos de datos o bundles independientes desde la línea de comandos, informes y CI |
| [Hooks del ciclo de vida](/manuals/editor-http-api#lifecycle-hooks) | Validación o generación antes y después de las builds o la creación de bundles en el editor |
| [Servicio HTTP del motor](/manuals/engine-service) | Inspección del motor de videojuegos Defold (`dmengine`) en ejecución, servicios de desarrollo, profiling, mensajes de runtime o API de automatización de runtime definidas por extensiones; consultas de herramientas externas y envío de comandos a una build de depuración en ejecución |
| [Automation Bridge](https://github.com/defold/extension-automation-bridge) | Extensión oficial de Defold que proporciona endpoints adicionales de automatización del runtime del motor |
| [Pruebas automatizadas](/manuals/automated-testing) | Probar la lógica del juego, mensajes, componentes, input, físicas y el comportamiento del motor; inspeccionar escenas y obtener información visual, por ejemplo, mediante una [vista previa del editor](/manuals/editor-http-api/#rendering-scene-previews), input inyectado, el estado activo de la aplicación y [colecciones de pruebas en ejecución](/manuals/automated-testing/#tests-in-a-running-collection) |
| Scripts de shell o ejecutores de tareas | Generación, formato, validación y tareas repetibles; operaciones habituales con archivos |
| Herramientas externas de automatización específicas de la plataforma y del navegador web | Herramientas de pruebas de escritorio, pruebas de interacción con HTML5, capturas de pantalla e integraciones web |
| Agentes de programación con IA y modelos multimodales | Tareas para las que resulta difícil o imposible implementar un método determinista, análisis semántico de escenas, layouts de GUI o capturas de pantalla del runtime |

La distinción más importante es la que existe entre el editor Defold y un juego en ejecución. Son procesos independientes con servidores HTTP distintos.

## Automatización determinista o agentes de IA

Prefiere una solución determinista cuando la secuencia de operaciones ya se conozca, por ejemplo, en un validador de niveles, un formateador, una tarea de build o una prueba de regresión. Normalmente, estas soluciones deben tener entradas, salidas, tiempos de espera y códigos de salida estables. Esto resulta apropiado para hooks y pruebas automatizados que puedan ejecutarse de forma fiable en CI. También es preferible una solución determinista para la creación procedimental de recursos de tus proyectos; por ejemplo, una herramienta que convierta objetos glTF en modelos con un material determinado, rellene un nivel con árboles, etc. Estos procedimientos pueden crearse fácilmente para cada proyecto con scripts del editor y de interfaz. Consulta más información en [el manual](/manuals/editor-scripts-ui).

Un agente puede ser útil cuando una tarea requiere investigación o análisis multimodal (por ejemplo, visual): localizar los recursos relevantes, seleccionar una implementación, modificar varios archivos, interpretar errores e iterar hasta cumplir unos criterios de aceptación definidos. Aun así, el agente debe llamar a interfaces deterministas y consumir las mismas evidencias que un script local o un ejecutor de CI. Consulta el manual sobre [cómo usar agentes de programación con IA en Defold](/manuals/ai-agents).

## El ciclo de automatización {#the-automation-loop}

Un proceso de automatización fiable forma un ciclo cerrado:

1. Inspeccionar: leer los archivos del proyecto, la descripción actual de la interfaz y la documentación relevante.
2. Cambiar: usar transacciones del editor, scripts del editor o herramientas de archivos y shell.
3. Verificar: crear la build, ejecutar pruebas específicas y recopilar logs, informes, estados o imágenes.
4. Evaluar: comparar las evidencias con los criterios de aceptación y, después, finalizar o volver a intentarlo.

![El ciclo de automatización de inspeccionar, cambiar, verificar y evaluar](images/automation/automation_loop.png)

La verificación debe aportar evidencias del entorno real. Entre las evidencias adecuadas se incluyen:

* el resultado de una build correcta;
* una suite de pruebas completada explícitamente;
* el estado esperado del juego en ejecución;
* un bundle o informe de build generado;
* una comparación de imágenes determinista;
* una captura de pantalla que cumpla los criterios visuales definidos.

Define el resultado esperado antes de realizar cambios. Define también un tiempo de espera y un número máximo de intentos de reparación. Un proceso desatendido no debe continuar indefinidamente si no puede satisfacer los criterios de aceptación.

## Próximos pasos

Encontrarás más detalles sobre temas específicos relacionados con los flujos de trabajo de automatización en los siguientes manuales:

* [Automatizar tareas del editor Defold con la API HTTP](/manuals/editor-http-api)
* [El servicio del motor y la API HTTP de runtime](/manuals/engine-service)
* [Pruebas automatizadas y verificación](/manuals/automated-testing)
* [Usar agentes de programación con IA en Defold](/manuals/ai-agents)
