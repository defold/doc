---
title: El servicio del motor y las API HTTP de runtime
brief: Este manual explica el servicio HTTP de desarrollo de un motor de depuración Defold en ejecución y cómo pueden utilizarlo las extensiones de runtime o las herramientas externas.
---

# El servicio del motor y las API HTTP de runtime {#the-engine-service-and-runtime-http-apis}

Ejecutar un proyecto en modo Debug crea un proceso para una instancia de runtime determinada del motor con tu juego y un servicio especial del motor al que se puede acceder para la infraestructura de desarrollo y profiling, la lógica y los mensajes de runtime, el estado del motor y las extensiones.

El servicio del motor es un servicio HTTP de desarrollo que pertenece a un motor de depuración o headless en ejecución (`dmengine` o `dmengine_headless`).

Es independiente del [servidor del editor](/manuals/editor-http-api), que pertenece al editor Defold y controla el proyecto abierto.

Los dos servicios utilizan puertos distintos. Una herramienta que se conecte al puerto del editor no puede llamar allí a rutas de extensiones de runtime y, a la inversa, una herramienta que se conecte al servicio del motor no puede llamar a operaciones del editor.

El servicio del motor forma parte de la infraestructura de depuración, desarrollo y profiling. Las instancias del motor de release no crean el servicio.

## Disponibilidad y detección del puerto {#availability-and-port-discovery}

Cuando el editor inicia un motor de depuración, solicita un puerto de servicio asignado dinámicamente. El motor indica el puerto seleccionado en *Console* y en su log cuando se ejecuta desde una CLI:

![Información del puerto del servicio del motor en una build de depuración de Defold](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

El motor también registra la URL completa de descubrimiento de OpenAPI con su dirección real y el puerto asignado:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Estas líneas aparecen en la consola del editor cuando el juego se ha lanzado desde él. Un controlador local sencillo puede analizarlas, pero una integración reutilizable debería dejar que el editor o su envoltorio lleven el seguimiento de la instancia del motor y su puerto registrado. Esto evita confundir un puerto antiguo con un proceso recién iniciado o reutilizado.

El motor también anuncia objetivos de desarrollo mediante la detección de servicios en las plataformas compatibles. Este mecanismo lo utilizan principalmente las herramientas de Defold y no debe sustituirse por un puerto fijado permanentemente en el código.

El servidor está disponible en localhost (`127.0.0.1`) en un puerto determinado:

![Acceso al servidor del motor](images/automation/engine-server.png)

## Descubrir operaciones mediante OpenAPI {#discovering-operations-through-openapi}

`GET /openapi.json` devuelve un documento OpenAPI 3.0.3 que describe la API HTTP de runtime. Usa el puerto del servicio del motor indicado en el log. Para un motor local, sustituye `<port>` a continuación por ese puerto:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

El documento describe las rutas, los métodos, los parámetros, los cuerpos de las solicitudes y las respuestas de los manejadores registrados actualmente, incluidas las extensiones nativas que proporcionan metadatos OpenAPI. Su objeto `paths` cambia al agregar o eliminar manejadores. Las rutas del profiler y de las extensiones dependen de la plataforma, la configuración y las extensiones registradas del motor en ejecución, por lo que debes obtener el documento de la instancia que estés usando.

Los manejadores registrados sin metadatos OpenAPI siguen pudiendo llamarse, pero no aparecen en el documento. Una ruta documentada también puede indicar que una funcionalidad no está disponible; revisa las descripciones de sus respuestas y cualquier endpoint de capacidades antes de usar operaciones que dependan de la plataforma.

El editor tiene su propio [documento OpenAPI](/manuals/editor-http-api/#discovering-operations-through-openapi) en el puerto del editor. Usa el documento del motor para las operaciones de runtime.

## Endpoints integrados {#built-in-endpoints}

El motor de depuración actual registra un pequeño conjunto de rutas principales.

| Endpoint | Propósito |
| --- | --- |
| `GET /openapi.json` | Descubrir las operaciones HTTP de runtime registradas actualmente que proporcionan metadatos OpenAPI |
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

## Endpoints de grabación {#recording-endpoints}

Los motores de depuración de escritorio también exponen la grabación nativa de MP4 mediante las siguientes rutas. Se omiten en builds release, headless, móviles y web, y cuando **Exclude Record** está activado en [App Manifest](/manuals/app-manifest/#exclude-record).

| Endpoint | Propósito |
| --- | --- |
| `GET /recording/capabilities` | Descubrir la compatibilidad con video y audio, los requisitos del backend y el `instance_id` del servicio de grabación |
| `GET /recording/status` | Consultar la operación actual, el progreso asíncrono y la información del archivo finalizado |
| `POST /recording/start` | Solicitar una grabación y recibir su `operation_id` |
| `POST /recording/stop` | Solicitar la detención y finalización de la operación especificada |
| `GET /recording/files/{id}` | Descargar un MP4 finalizado |
| `DELETE /recording/files/{id}` | Eliminar un archivo completado que conserva el servicio |

Descubre estas rutas mediante `/openapi.json` y comprueba `/recording/capabilities` para conocer las capacidades de la plataforma actual. Las operaciones de grabación que modifican el estado requieren la cabecera `X-Recording-Instance`, y detener una grabación también requiere el `operation_id` aceptado. El inicio y la detención son asíncronos; espera a que finalice antes de descargar el archivo. Consulta el [manual de grabación](/manuals/recording/#recording-through-http) para conocer el procedimiento completo.

El servicio HTTP comparte el grabador con Lua. Las grabaciones iniciadas por HTTP activan el audio de la aplicación de forma predeterminada si se admite; las iniciadas por Lua solo graban video de forma predeterminada. Solo las grabaciones iniciadas por HTTP tienen un comprobante `file` descargable. Antes de descargarlo, espera a que se cumplan `pending: false`, `finalized: true` y `file.state: "complete"`, y después [verifica el tamaño y el SHA-256 del archivo](/manuals/recording/#download-and-release-the-file). Consulta [cómo compartir el grabador](/manuals/recording/#sharing-the-recorder-with-http-clients) al combinar clientes Lua y HTTP.

## Endpoint de trazas de GPU Metal {#metal-gpu-trace-endpoint}

En macOS, los motores de depuración exponen `/profiler/gputrace` para capturar trazas de GPU Metal. La ruta solo aparece en `/openapi.json` en macOS. La captura requiere el adaptador nativo Metal y `METAL_CAPTURE_ENABLED=1` en el entorno de lanzamiento del motor. Si la captura no está disponible, la solicitud devuelve HTTP 501 con `error.code: "gputrace_unsupported"`.

| Endpoint | Propósito |
| --- | --- |
| `POST /profiler/gputrace` | Programar una captura en una ruta absoluta `.gputrace` con permiso de escritura; `frames` vale `1` de forma predeterminada y puede ser `1`–`10000`. |
| `GET /profiler/gputrace` | Consultar el estado, la ruta y los contadores de frames de la captura actual o más reciente. |
| `DELETE /profiler/gputrace` | Cancelar una captura pendiente o terminar una captura activa después del frame que se está renderizando; conservar la traza en disco. |

Las solicitudes aceptadas devuelven HTTP 200 con `ok: true` y un objeto `data`. La captura avanza de forma asíncrona: consulta `GET` hasta que `data.state` sea `complete`, `canceled` o `failed`. Los fallos del inicio nativo se notifican en `data.error`. La traza se escribe en el host del motor. Consulta la [guía de captura de trazas de GPU Metal](/manuals/profiling/#metal-gpu-trace-capture) para ver comandos de lanzamiento, descubrimiento de compatibilidad, ejemplos de captura y cómo abrir el resultado en Xcode.

## Rutas de runtime definidas por extensiones {#extension-defined-runtime-routes}

En las builds de depuración, el SDK de extensiones nativas puede proporcionar acceso al servidor web del motor. Una extensión puede registrar un prefijo de ruta en ese servidor y exponer operaciones que dependan de datos de runtime.

Esto resulta útil para las herramientas de desarrollo porque una extensión puede compartir el servicio existente del motor en lugar de abrir otro servidor HTTP.

Una API de automatización de runtime definida por una extensión debe:

* utilizar un prefijo de ruta distintivo y versionado;
* exponer las funcionalidades compatibles;
* devolver errores estructurados;
* gestionar de forma explícita las funcionalidades no disponibles de la plataforma o el motor;
* limitar las operaciones al desarrollo y las pruebas;
* documentar si se omite en las builds de release.

### Publicar operaciones de extensiones en OpenAPI {#publishing-extension-operations-in-openapi}

En el callback de inicialización de la aplicación de una extensión nativa, obtén el servidor mediante `dmEngine::GetWebServer(app_params)` y registra manejadores solo cuando el handle devuelto no sea nulo. Consulta el [ciclo de vida de las extensiones](/manuals/extensions/#extension-lifecycle) para configurar el callback.

La sobrecarga de cuatro argumentos de `dmWebServer::AddHandler()` acepta un objeto Paths de OpenAPI 3.0.3 como cadena JSON. El objeto tiene las rutas como claves de primer nivel. Cada ruta debe comenzar con el prefijo registrado y no estar ya documentada por otro manejador. Usa esquemas en línea o referencias a rutas del documento resultante.

Por ejemplo, esta función auxiliar registra un callback y la descripción de su endpoint de estado:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

Pasa un callback que implemente `GET /example/v1/status` y devuelva la respuesta `text/plain` documentada. El callback sigue siendo responsable de comprobar las rutas y los métodos de las solicitudes y de generar las respuestas. Comprueba el resultado del registro: los metadatos no válidos o en conflicto devuelven `dmWebServer::RESULT_ERROR_INVAL`.

El servidor conserva el puntero JSON sin copiar la cadena. Mantén su almacenamiento sin cambios y válido hasta que se elimine el manejador con `dmWebServer::RemoveHandler()` o se destruya el servidor. El array `static const char` del ejemplo cumple este requisito. Al eliminar el manejador también se eliminan sus rutas de las respuestas posteriores de `/openapi.json`.

La sobrecarga de tres argumentos `dmWebServer::AddHandler(server, prefix, &params)` sigue admitiéndose. Equivale a pasar `0` como cuarto argumento: el manejador se registra sin metadatos OpenAPI y se omite del descubrimiento.

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

### Clientes del editor y de runtime {#editor-and-runtime-clients}

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

## Limitaciones y seguridad {#limitations-and-security}

El servicio del motor y las rutas definidas por extensiones son herramientas de desarrollo y deben tratarse como tales.

::: important
Usa el documento `/openapi.json` del motor en ejecución para el descubrimiento en Defold 1.14.1 y versiones posteriores. Los motores anteriores no proporcionan este endpoint. Para los manejadores registrados sin metadatos OpenAPI, consulta la documentación de la API de la versión de la extensión.
:::

Los scripts de runtime, las físicas, el input, los objetos creados dinámicamente y el renderizado específico de la plataforma requieren un motor en ejecución y deben verificarse mediante [pruebas automatizadas de runtime](/manuals/automated-testing).

* No publiques el servicio mediante un router, una interfaz pública o un túnel que no sea de confianza.
* No des por sentado que las rutas del servicio del motor requieren autenticación.
* Las rutas de runtime pueden variar según la versión de la extensión, la plataforma, el backend de gráficos y las funcionalidades del motor.
* Utiliza la negociación de versiones o funcionalidades para las API actualizadas definidas por extensiones.
