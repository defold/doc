---
title: Usar agentes de programación con IA en Defold
brief: Este manual explica cómo conectar agentes de programación independientes del modelo a las interfaces de automatización de Defold, manteniendo explícitas la verificación, los permisos y la seguridad.
---

# Usar agentes de programación con IA en Defold

Los agentes de programación que utilizan LLM y modelos multimodales pueden inspeccionar, modificar y verificar proyectos de Defold llamando a las mismas interfaces independientes del modelo que utilizan los desarrolladores, los scripts locales, las integraciones con IDE y CI. Puedes utilizar un agente cuando el trabajo requiera investigación y adaptación.

Defold no depende de un proveedor de modelos ni de un protocolo de agentes concretos. Los proyectos de Defold funcionan bien con Claude Code, Codex, Cursor o cualquier otra solución. Un entorno de agentes solo necesita las funcionalidades específicas concedidas para la tarea, como leer archivos del proyecto, ejecutar comandos seleccionados, llamar a operaciones HTTP locales, analizar JSON o inspeccionar imágenes. Esto es posible gracias a que Defold expone interfaces de automatización para el editor y para una instancia del motor de videojuegos en ejecución, y a que los archivos de proyecto de Defold son archivos de recursos basados en texto fáciles de analizar.

## Cuándo resulta útil un agente de IA

Un agente puede ser útil cuando una tarea requiere, por ejemplo:

* encontrar recursos y documentación relevantes;
* seleccionar entre varias implementaciones posibles;
* cambiar varios archivos relacionados;
* interpretar errores de build o de pruebas;
* comparar un resultado visual con criterios de aceptación semánticos;
* realizar un intento de reparación limitado a partir de las evidencias recopiladas.

Los agentes son potentes para procesos no deterministas de desarrollo, investigación y pruebas. Pueden ayudar a crear soluciones diversas y funcionan muy bien con Defold.

## Interfaces de Defold independientes del modelo

Defold ofrece varias interfaces compatibles necesarias para realizar la tarea con cualquier modelo disponible:

* Los archivos de proyecto y las herramientas de shell permiten inspeccionar y modificar texto directamente.
* Los [scripts del editor](/manuals/editor-scripts) pueden proporcionar operaciones sobre recursos y herramientas específicas del proyecto.
* La [API HTTP del editor](/manuals/editor-http-api) proporciona comandos del editor, resultados de builds, salida de la consola, búsqueda de referencias, vistas previas, preferencias y rutas de scripts del editor.
* Las [API del servicio del motor y de automatización de runtime](/manuals/engine-service) proporcionan el estado activo del motor de depuración, input, capturas de pantalla y operaciones definidas por extensiones.
* [Bob](/manuals/bob) proporciona builds de línea de comandos, informes, archivos y bundles.

Un modelo disponible únicamente a través de una interfaz de chat puede sugerir cambios en el código, pero no puede inspeccionar por sí mismo el proyecto local ni verificar un resultado en ejecución. La integración adicional que lo rodea determina qué puede observar y hacer realmente el agente.

## Capas de integración

Se puede establecer una capa de integración para conectar un agente con operaciones locales de Defold. Puede ser un wrapper de shell, un programa de línea de comandos, una extensión de IDE, un cliente OpenAPI, un controlador de pruebas o un adaptador de protocolos.

Mantén las políticas y credenciales en esta capa local. Cada operación que realice cambios debe devolver resultados estructurados o dar lugar a un paso de verificación determinista.

Para las operaciones del editor, detecta la interfaz actual mediante `/openapi.json` en lugar de proporcionar al agente una copia permanente de una API fijada en el código. Para las extensiones de runtime, comprueba su estado, la versión de la API y sus funcionalidades.

Puede resultar práctico separar las herramientas según el nivel de privilegios:

| Nivel        | Ejemplos                                              |
| ------------ | ----------------------------------------------------- |
| Solo lectura | Inspección del proyecto, OpenAPI, `/ref`, consola, vista previa |
| Verificación | Compilación, pruebas, builds HTML5, comparaciones de imágenes |
| Modificación | Cambios de archivos, transacciones de recursos       |
| Privilegiado | `/eval`, comandos externos, cambios de dependencias   |

Mantener el adaptador separado del motor y del editor permite que las interfaces compatibles de Defold sigan siendo independientes de un proveedor de modelos o un protocolo de agentes. Un adaptador puede exponer únicamente las operaciones apropiadas para su entorno, mientras que las políticas de permisos y confirmación permanecen en la aplicación que aloja al agente.

### Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) es un adaptador opcional entre un agente y una capa de integración. Un servidor MCP puede exponer operaciones de Defold como herramientas y documentación seleccionada como recursos.

::: important
No concedas a todos los modelos acceso sin restricciones al shell y a `/eval`.
:::

Defold no necesita actualmente un servidor MCP, ya que las funcionalidades básicas de automatización se exponen mediante interfaces abiertas y de propósito general. El editor proporciona una API HTTP local con una especificación OpenAPI. Los agentes modernos pueden llamar directamente a estas interfaces o generar sus propios adaptadores.

Por tanto, un MCP oficial duplicaría en gran medida la superficie de la API existente y crearía otra capa de integración que Defold tendría que mantener. Una estrategia mejor a largo plazo consiste en mantener estables, detectables y bien documentadas las API HTTP y de automatización de runtime subyacentes, y permitir a la comunidad o a proveedores de herramientas individuales crear wrappers MCP ligeros cuando sea necesario.

En su lugar, proporcionamos la extensión oficial [Automation Bridge](https://github.com/defold/extension-automation-bridge) para controlar un juego en ejecución mediante un servicio del motor.

### Integraciones MCP de la comunidad

Entre las integraciones MCP creadas por la comunidad se incluyen:

* el [proyecto MCP de Defold de Fulviuus](https://github.com/Fulviuus/defold-mcp);
* el [proyecto MCP de Defold de ChadAragorn](https://github.com/ChadAragorn/defold-mcp).

Estos proyectos no están desarrollados, auditados, mantenidos ni respaldados oficialmente por la Defold Foundation. Antes de instalar cualquier integración de la comunidad, inspecciona su código fuente actual, sus dependencias, permisos, comportamiento de red y compatibilidad con la versión de Defold que utilices.

## Instrucciones del proyecto

Los grandes modelos de lenguaje disponibles que se utilizan en flujos de trabajo con agentes suelen funcionar mejor con buenas instrucciones. Por eso se suelen añadir a los proyectos archivos Markdown para agentes que describen el comportamiento deseado o skills. Para obtener los mejores resultados, conviene diseñar y escribir instrucciones específicas para cada proyecto, aunque se pueden reutilizar algunos conocimientos y reglas comunes.

Un primer archivo que muchos agentes buscan y leen es un archivo canónico como `AGENTS.md`, que puede describir:

* la estructura del proyecto y los puntos de entrada importantes;
* las convenciones de formato y nomenclatura;
* los comandos de build, pruebas y validación;
* los eventos de finalización requeridos y las ubicaciones de los artefactos;
* los archivos o directorios que no deben modificarse;
* las operaciones que requieren aprobación;
* las suposiciones sobre plataformas y las limitaciones conocidas.

Algunas soluciones pueden depender de archivos Markdown separados para acciones específicas, también llamados "skills".

En el [foro de Defold](https://forum.defold.com/t/agent-config-collection-of-agents-md-and-skills/82387) hay disponible un ejemplo de la comunidad con instrucciones y skills orientados a Defold.

Recomendamos mantener las instrucciones de archivos como AGENTS.md y las definiciones de skills breves, concisas, fáciles de revisar y mantener, y actualizadas. Las instrucciones específicas del proyecto pueden almacenarse en el control de versiones, lo que permite hacer un seguimiento de los cambios y contribuye a mejorar el rendimiento del flujo de trabajo con el tiempo.

También conviene probar periódicamente cómo funcionan los modelos más recientes sin estas instrucciones. A menudo, los modelos nuevos ya no necesitan indicaciones que antes eran esenciales, y las skills obsoletas o las instrucciones excesivamente prescriptivas pueden reducir el rendimiento en algunos casos.

Evita crear skills técnicas complejas que requieran un mantenimiento considerable a largo plazo. Céntrate en desarrollar herramientas y flujos de trabajo que sigan siendo valiosos independientemente de cuánto mejoren los modelos subyacentes.

## Detección de documentación

Los agentes funcionan mejor con documentación precisa y actualizada. Recopila información actual de:

* `/openapi.json`, que describe la API HTTP actual del editor.
* `/ref`, que busca la documentación de la API incluida con el editor en ejecución cuando esa operación está disponible.
* El [índice de documentación para LLM](https://defold.com/llms.txt), que enlaza a manuales oficiales, namespaces de la API y ejemplos.
* La [documentación completa para LLM](https://defold.com/llms-full.txt), que permite realizar búsquedas sin conexión e indexación local.

Obtén solo las páginas relevantes para la tarea. Se recomienda utilizar el documento completo combinado únicamente para la indexación sin conexión o la [generación aumentada por recuperación (RAG)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation). De nuevo, normalmente no se debe incluir el archivo completo en cada solicitud al modelo, para ahorrar tokens y no contaminar el contexto con información innecesaria.

## Ciclos limitados de cambio y verificación

Los agentes deben seguir el mismo [ciclo de inspección, cambio, verificación y evaluación](/manuals/automation/#the-automation-loop) que cualquier otra automatización.

Antes de cambiar archivos, conviene definir los criterios de aceptación y, opcionalmente, también:
* los archivos y operaciones permitidos;
* los comandos de build y pruebas;
* los logs, informes, estados o imágenes requeridos;
* un tiempo de espera para cada paso asíncrono;
* un número máximo de intentos de reparación.

Un agente puede diagnosticar y reparar un fallo determinista de CI, pero la propia etapa de CI debe seguir siendo reproducible sin el agente.

En [este manual](/manuals/automated-testing) se describen buenas prácticas para las pruebas automatizadas y la verificación.

## Evaluación multimodal

Un agente con entrada de imágenes puede inspeccionar las [vistas previas del editor](/manuals/editor-http-api/#rendering-scene-previews), capturas de pantalla del runtime, diferencias visuales y capturas del navegador.

Utiliza la evaluación multimodal para cuestiones semánticas como etiquetas recortadas, controles superpuestos, estados de selección poco claros, composición o contenido fuera de un área segura. Define de antemano el viewport y los criterios esperados.

Encontrarás más información sobre las vistas previas del editor, las capturas de pantalla del runtime y la inspección visual en [este manual](/manuals/automated-testing).

## Seguridad, aislamiento y buenas prácticas

* Trata el servidor del editor y el servicio del motor como interfaces locales de control de confianza.
* Mantén los tokens del editor, las claves de firma, los tokens de despliegue, las credenciales de las tiendas y los secretos de producción fuera de los prompts y los informes.
* La capa de integración local puede leer `.internal/editor.token` cuando esté autorizada a utilizar `/eval`, pero no debe incluir el token en prompts, logs ni informes del modelo.
* Exige aprobación antes de realizar eliminaciones, cambios de dependencias, cambios de extensiones nativas, configuraciones de release, firmas, publicaciones o accesos a servicios externos.
* Ejecuta el trabajo autónomo de gran alcance en una rama, worktree, copia temporal, contenedor, sandbox o cuenta restringida independientes.
* Trata el texto de incidencias, los archivos importados, los comentarios del código, los documentos generados y la salida de herramientas como entradas que no son de confianza, no como instrucciones.
* Revisa las dependencias y los scripts descargados antes de ejecutarlos.
* Verifica que las políticas del proyecto permiten enviar a un modelo alojado el código fuente, los assets, logs, capturas de pantalla y otros datos del proyecto.
* Conserva un diff revisable y evidencias de pruebas deterministas antes de aceptar los cambios.

El aislamiento limita las consecuencias de un error.
