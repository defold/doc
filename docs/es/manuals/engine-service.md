---
title: El servicio del motor y las API HTTP de runtime
brief: Este manual explica el servicio HTTP de desarrollo de un motor de depuración Defold en ejecución y cómo pueden utilizarlo las extensiones de runtime o las herramientas externas.
---

# El servicio del motor y las API HTTP de runtime

Ejecutar un proyecto en modo Debug crea un proceso para una instancia de runtime determinada del motor con tu juego y un servicio especial del motor al que se puede acceder para la infraestructura de desarrollo y profiling, la lógica y los mensajes de runtime, el estado del motor y las extensiones.

El servicio del motor es un servicio HTTP de desarrollo que pertenece a un motor de depuración (`dmengine`) en ejecución.

Es independiente del [servidor del editor](/manuals/editor-http-api), que pertenece al editor Defold y controla el proyecto abierto.

Los dos servicios utilizan puertos distintos. Una herramienta que se conecte al puerto del editor no puede llamar allí a rutas de extensiones de runtime y, a la inversa, una herramienta que se conecte al servicio del motor no puede llamar a operaciones del editor.

El servicio del motor forma parte de la infraestructura de depuración, desarrollo y profiling. Las instancias del motor de release no crean el servicio.

## Disponibilidad y detección del puerto

Cuando el editor inicia un motor de depuración, solicita un puerto de servicio asignado dinámicamente. El motor indica el puerto seleccionado en `Console` (y en su log si se ejecuta desde una CLI):

![Información del puerto del servicio del motor en una build de depuración de Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

La línea aparece en la consola del editor cuando el juego se inicia desde el editor. Un controlador local sencillo puede analizarla, pero una integración reutilizable debe permitir que el editor o su wrapper realice el seguimiento de la instancia del motor y del puerto registrado. Esto evita confundir un puerto antiguo con un proceso recién iniciado o reutilizado.

El motor también anuncia objetivos de desarrollo mediante la detección de servicios en las plataformas compatibles. Este mecanismo lo utilizan principalmente las herramientas de Defold y no debe sustituirse por un puerto fijado permanentemente en el código.

El servidor está disponible en localhost (`127.0.0.1`) en un puerto determinado:

![Acceso al servidor del motor](images/automation/engine-server.png)

## Endpoints integrados

El motor de depuración actual registra un pequeño conjunto de rutas principales.

| Endpoint | Propósito |
| --- | --- |
| `GET /ping` | Comprobar que el servicio del motor responde |
| `GET /info` | Leer la versión del motor, la plataforma, el identificador de la build y la información del servicio de logs |
| `GET /state` | Leer el estado de la conexión de desarrollo que utilizan las herramientas de Defold |
| `POST /post/<socket>/<message-type>` | Enviar un mensaje Defold codificado con Protobuf a un socket del motor con nombre |

Por ejemplo:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

La ruta `/post` se utiliza para operaciones de desarrollo como hot reload, reinicio, cambio de tamaño y control de procesos. Su cuerpo es un mensaje binario Protobuf del tipo indicado en la ruta; no es una API de mensajes JSON. El mensaje Protobuf no puede superar los 1024 bytes una vez serializado; de lo contrario, se devolverá `400 Too large message`.

Estas rutas son infraestructura de desarrollo, y existen rutas adicionales de profiler e inspección de recursos en la implementación del motor.

## Rutas de runtime definidas por extensiones

En las builds de depuración, el SDK de extensiones nativas puede proporcionar acceso al servidor web del motor. Una extensión puede registrar un prefijo de ruta en ese servidor y exponer operaciones que dependan de datos de runtime.

Esto resulta útil para las herramientas de desarrollo porque una extensión puede compartir el servicio existente del motor en lugar de abrir otro servidor HTTP.

Una API de automatización de runtime definida por una extensión debe:

* utilizar un prefijo de ruta distintivo y versionado;
* exponer las funcionalidades compatibles;
* devolver errores estructurados;
* gestionar de forma explícita las funcionalidades no disponibles de la plataforma o el motor;
* limitar las operaciones al desarrollo y las pruebas;
* documentar si se omite en las builds de release.

## Extensión Automation Bridge {#automation-bridge-extension}

La [Automation Bridge](https://github.com/defold/extension-automation-bridge) oficial de Defold es una extensión nativa exclusiva para depuración basada en el servicio del motor. Registra una API de automatización de runtime versionada en:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Su API de runtime proporciona funcionalidades como la inspección de escenas y nodos, input, información de la pantalla, capturas de pantalla, grabación, información del ciclo de vida y sincronización opcional definida por la aplicación. Algunas de sus operaciones son:

| Operación | Acción |
| --- | --- |
| `GET  /automation-bridge/v1/health` | Informe de estado, funcionalidades de la API y compatibilidad |
| `POST /automation-bridge/v1/input/click` | Interacciones de input en runtime |
| `GET  /automation-bridge/v1/screenshot` | Capturas de pantalla del runtime |

Consulta la [documentación de la API nativa](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) y la [documentación del helper de Python](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) de la extensión para conocer la versión instalada en el proyecto.

Automation Bridge no expone su API HTTP ni su módulo Lua en las builds de release.

### Clientes del editor y de runtime

Los helpers de Python de Automation Bridge ilustran la arquitectura de dos clientes. La función `editor.open_project()` devuelve un cliente de proyecto del editor y `project.build_and_run()` devuelve un cliente independiente del motor.

| Cliente | Propósito |
| --- | --- |
| Proyecto | API HTTP del editor, comandos, debugger, consola, preferencias, referencia, vistas previas, build y detección del puerto |
| Juego: servicio del motor | Escena, input, capturas de pantalla, estado de runtime y sincronización |

La separación entre `project` y `game` hace explícito el límite entre procesos. Las operaciones del editor permanecen en el servidor del editor, mientras que las observaciones y acciones sobre el juego activo permanecen en el servicio del motor.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Limitaciones y seguridad

El servicio del motor y las rutas definidas por extensiones son herramientas de desarrollo y deben tratarse como tales.

::: important
Actualmente, el servicio del motor no publica un documento OpenAPI. Las integraciones deben limitarse al comportamiento documentado o a la API versionada de una extensión.
:::

Los scripts de runtime, las físicas, el input, los objetos creados dinámicamente y el renderizado específico de la plataforma requieren un motor en ejecución y deben verificarse mediante [pruebas automatizadas de runtime](/manuals/automated-testing).

* No publiques el servicio mediante un router, una interfaz pública o un túnel que no sea de confianza.
* No des por sentado que las rutas del servicio del motor requieren autenticación.
* Las rutas de runtime pueden variar según la versión de la extensión, la plataforma, el backend de gráficos y las funcionalidades del motor.
* Utiliza la negociación de versiones o funcionalidades para las API actualizadas definidas por extensiones.
