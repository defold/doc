---
title: Automatizar el editor Defold con HTTP
brief: Este manual explica cómo pueden las herramientas externas detectar y utilizar la API HTTP local de un proyecto abierto en el editor Defold.
---

# Automatizar el editor Defold

El editor Defold abre un servidor especial para realizar acciones automatizadas. La API HTTP controla el proyecto abierto. Utilízala para comandos del editor, builds, recursos del proyecto, vistas previas, preferencias, salida de la consola, búsqueda en la documentación o integraciones con scripts del editor. Para inspeccionar o controlar el juego en ejecución, utiliza en su lugar el [servicio del motor o una API de automatización de runtime](/manuals/engine-service).

::: important
La API HTTP del editor es experimental y puede cambiar entre versiones de Defold. El documento `/openapi.json` generado por el editor en ejecución es la fuente de verdad sobre sus operaciones y esquemas disponibles.
:::

## Iniciar el editor desde una herramienta externa

Una herramienta externa necesita el ejecutable del editor y la ruta absoluta al archivo `game.project` del proyecto.

Las versiones instaladas de Defold se pueden localizar mediante `installations.json`, como se describe en el [manual del editor](/manuals/editor/#editor-installation-metadata). Su campo `launcherPath` contiene el ejecutable que se debe iniciar. Pasa la ruta de `game.project` como primer argumento posicional para abrir ese proyecto directamente.

El argumento opcional `--port` o `-p` selecciona el puerto del servidor del editor. Si se omite, Defold elige un puerto disponible, lo que normalmente resulta preferible cuando puede haber varios proyectos abiertos.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

El editor es una aplicación gráfica de escritorio. Inícialo en una sesión de usuario interactiva con acceso a la pantalla. Utiliza [Bob](/manuals/bob) cuando no haya una sesión gráfica disponible, como en un entorno de CI headless, o para automatizar únicamente la compilación y crear bundles independientes.

Después de iniciar el editor, espera hasta que el proyecto se haya abierto y exista `.internal/editor.port`. A continuación, consulta periódicamente `/openapi.json` hasta que devuelva un documento válido. No des por sentado que el proyecto está listo solo porque se haya creado el proceso.

## Localizar el servidor del editor

El editor inicia un servidor HTTP local mientras hay un proyecto abierto. Selecciona <kbd>Help ▸ Open Editor Server</kbd> para abrir su página principal en el navegador predeterminado:

![Página principal del servidor local del editor](images/automation/editor_server.png)

El puerto seleccionado se escribe dentro del proyecto en:

```text
.internal/editor.port
```

A partir de ahora, los ejemplos y comandos de este manual harán referencia a estas variables de shell:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

El archivo del puerto pertenece a la sesión actual del editor. Vuelve a leerlo después de reiniciar el editor.

::: important
El servidor del editor es una interfaz local de control de confianza. No lo expongas mediante una dirección pública, reenvío de puertos ni un túnel que no sea de confianza.
:::

## Detectar operaciones mediante OpenAPI

La única información de arranque específica de Defold que debería necesitar una herramienta externa es el puerto del editor y el documento OpenAPI:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

El documento OpenAPI 3.0.3 devuelto describe las operaciones compatibles con la versión del editor en ejecución, incluidas rutas, métodos, parámetros, nombres de comandos, formatos de solicitud, respuestas, códigos de estado y requisitos de autenticación.

Muestra las rutas documentadas:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Muestra los comandos disponibles del editor:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '
    .paths["/command/{command}"].post.parameters[]
    | select(.name == "command")
    | .schema.enum[]
  '
```

Una integración que tenga en cuenta la versión debe verificar cada operación necesaria y configurar las solicitudes según el esquema devuelto. No recomendamos mantener una copia supuestamente exhaustiva de los nombres de endpoints o comandos, ya que puede quedar obsoleta.

Las rutas definidas por el proyecto también aparecen en `/openapi.json` cuando sus scripts del editor proporcionan una descripción de la operación OpenAPI.

## Ejecutar comandos del editor

Los comandos del editor se invocan mediante:

```text
POST /command/{command}
```

Por ejemplo, el comando `build` actual compila y ejecuta el proyecto:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build" |
  jq
```

Una build correcta devuelve un resultado estructurado:

```json
{
  "success": true,
  "issues": []
}
```

Una build fallida devuelve el estado HTTP `422` con incidencias como:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Los campos disponibles dependen del error. Utiliza la ruta del recurso y el rango del código fuente cuando estén presentes, pero gestiona también las incidencias que solo contengan un mensaje.

Entre los comandos que suelen resultar útiles, cuando aparecen en el editor en ejecución, se incluyen:

`build`
: Compila y ejecuta el proyecto.

`clean-build`
: Borra la caché de la build y después compila y ejecuta. Utiliza esta opción solo cuando una build normal se comporte de forma incoherente o parezca omitir cambios.

`build-html5`
: Crea una build del proyecto para HTML5 y pone la salida a disposición a través del servidor del editor.

`fetch-libraries`
: Descarga y vuelve a cargar las dependencias del proyecto.

`hot-reload`
: Vuelve a cargar los recursos modificados en un juego en ejecución.

`reload-extensions`
: Vuelve a cargar los scripts del editor.

`debugger-start`, `debugger-stop` y los comandos de paso del debugger
: Controlan una sesión de depuración y el proyecto en ejecución.

Los nombres exactos y su disponibilidad dependen de la versión y del estado actual del editor; detéctalos mediante `/openapi.json`.

Los comandos que operan sobre recursos del proyecto sincronizan los cambios externos de los archivos antes de ejecutarse.

### Respuestas de comandos y trabajo asíncrono

La operación del comando documenta los códigos de respuesta en el esquema OpenAPI actual.

| Estado | Significado |
| --- | --- |
| `200` | El comando finalizó y devolvió un resultado |
| `202` | El comando se aceptó y continúa de forma asíncrona |
| `403` | El comando no está activo en el estado actual del editor |
| `404` | El comando no está disponible |
| `422` | La build o la validación fallaron |
| `500` | Se produjo un error interno del editor |

Una respuesta HTTP `202` no demuestra que el resultado solicitado exista. Espera a que aparezcan la salida, el recurso, el marcador de la consola o la URL servida correspondientes, y establece un tiempo de espera.

### Crear una build HTML5 {#building-html5}

Si el documento OpenAPI actual incluye `build-html5`, invócalo mediante la operación del comando:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/build-html5"
```

El comando se ejecuta de forma asíncrona y normalmente devuelve el estado HTTP `202`. Una vez finalizada la build, el editor la sirve en:

```text
http://127.0.0.1:<editor-port>/html5/
```

Espera a que la URL esté disponible antes de iniciar las pruebas de navegador. Consulta [Pruebas de navegador para HTML5](/manuals/automated-testing/#browser-tests-for-html5) para obtener más detalles.

## Buscar en la documentación de la API

Cuando está presente en `/openapi.json`, la operación `/ref` busca en la documentación de la API incluida con la versión del editor en ejecución. Proporciona nombres y firmas que coinciden con esa versión.

Por ejemplo, para buscar una función, utiliza:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Filtra por entorno y lenguaje:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Los parámetros de búsqueda son:

`environment`
: `editor`, `runtime` o valores separados por comas.

`language`
: `Lua`, `C`, `C++` o valores separados por comas.

`q`
: Una expresión que no distingue entre mayúsculas y minúsculas. Los espacios en blanco representan AND, mientras que `|` representa OR.

También hay recursos de documentación resumidos: el [índice de documentación para LLM](https://defold.com/llms.txt) enlaza a manuales oficiales, namespaces de la API y ejemplos, y la [documentación completa para LLM](https://defold.com/llms-full.txt) contiene toda la documentación para permitir búsquedas sin conexión e indexación local.

No obstante, los agentes de IA deben preferir las búsquedas específicas en vez de obtener una referencia completa cuando solo se necesita una API o un mensaje, para ahorrar tokens y disponer de un contexto más limpio y mejor preparado para una tarea determinada.

## Leer la salida de la consola {#reading-console-output}

Lee la consola del editor como JSON:

```sh
curl -sS "$BASE_URL/console" | jq
```

La respuesta contiene el texto de la consola en `lines` y regiones semánticas en `regions`, incluidos errores, resultados de evaluación y referencias a recursos.

Para seguir la salida de la consola de forma continua, utiliza:

```sh
curl -N "$BASE_URL/console/stream"
```

El stream incluye las líneas existentes de la consola y después permanece abierto para recibir nueva salida. Ciérralo después de recibir un marcador de finalización o un error, detectar que ha terminado el proceso o alcanzar un tiempo de espera o límite de líneas.

Para obtener información sobre el enmarcado de los resultados de pruebas y la clasificación de fallos, consulta [Pruebas automatizadas y verificación](/manuals/automated-testing/#structured-test-results).

## Renderizar vistas previas de escenas {#rendering-scene-previews}

El editor Defold (desde la versión 1.13.1) puede renderizar una "captura de pantalla" de un recurso de escena compatible como PNG mediante el comando `/preview/{path}`:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Esto renderiza la colección principal del proyecto abierto creado a partir de la plantilla Basic 3D en una vista inicial predeterminada:

![Vista previa de la colección principal renderizada por el editor](images/automation/main-preview.png)

Puedes utilizar el renderizado para obtener vistas previas de recursos que usen el editor visual de escenas. Por ejemplo, puedes renderizar un componente de modelo del mismo modo, lo que permite verificar su aspecto o, por ejemplo, que el shader sea correcto:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Vista previa del modelo de cubo renderizada por el editor](images/automation/cube-preview.png)

La ruta situada después de `/preview/` no incluye una barra inicial. Las dimensiones opcionales utilizan de forma predeterminada el tamaño de visualización del proyecto y deben estar entre `1` y `4096`.

| Estado | Significado |
| --- | --- |
| `200` | Se renderizó la vista previa |
| `400` | Las dimensiones no son válidas |
| `404` | No se encontró el recurso |
| `422` | El recurso no está cargado o no admite vistas previas de escenas |

Las vistas previas pueden resultar muy útiles para el análisis visual del proyecto: comprobar layouts de niveles y GUI, la configuración de shaders e iluminación y regresiones visuales, o crear miniaturas para la documentación.

::: important
Una vista previa del editor no es una captura de pantalla del juego en ejecución. No verifica objetos creados dinámicamente, posprocesamiento de runtime ni renderizado específico de la plataforma. Utiliza una [captura de pantalla del runtime](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) cuando necesites esos elementos.
:::

## Ejecutar Lua en el editor

La operación autenticada `POST /eval` ejecuta Lua en el entorno de extensiones del editor. El bearer token de cada sesión se almacena en:

```text
.internal/editor.token
```

Lee el token y ejecuta el código:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

La salida impresa y los valores devueltos se reciben como texto. Las respuestas habituales son:

| Estado | Significado |
| --- | --- |
| `200` | Se ejecutó el código |
| `401` | Falta el bearer token o no es válido |
| `422` | No se pudo analizar o ejecutar el código Lua |
| `503` | El entorno de extensiones del editor no está listo |

Un cliente puede volver a intentarlo después de un `503`, pero debe limitar el número de intentos. Corrige el código antes de repetir una solicitud que haya devuelto `422`.

El código evaluado puede utilizar la [API del editor](https://defold.com/ref/editor-lua/) y el entorno de scripting del editor. No puede utilizar API de runtime del juego como `go.*` para manipular un juego en ejecución. Utiliza una prueba de runtime, el debugger, una prueba de navegador o una [API de automatización de runtime](/manuals/engine-service/#automation-bridge-extension) para el gameplay.

### Modificar recursos y archivos

Muchos recursos de código fuente de Defold utilizan formatos de texto y se pueden editar con cualquier herramienta de edición de texto. Para modificar recursos estructurados de un proyecto de Defold, es preferible utilizar transacciones del editor.

| Cambio | Método preferido |
| --- | --- |
| Lua, shader, JSON u otro formato de texto conocido | Modificación directa del archivo |
| Texto sin guardar en una pestaña abierta del editor | `editor.get()` y `editor.transact()` |
| Colección, objeto de juego, GUI, atlas u otro recurso estructurado | Transacción del editor |
| Contenido generado repetidamente | Generador independiente |
| Operación de proyecto repetible | Comando del editor o endpoint HTTP personalizado |
| Transformación exclusiva de CI | Script independiente ejecutado antes de Bob |

Inspecciona un recurso antes de modificarlo:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Comprueba `editor.can_get()`, `editor.can_set()` y las demás funciones `editor.can_*()` antes de realizar una transacción.

Utiliza `editor.execute()` en Lua del editor para ejecutar un formateador, validador o generador:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Cuando el comando no modifique recursos del proyecto, establece `reload_resources = false` para evitar una recarga innecesaria.

::: important
No modifiques archivos de `.internal/` ni contenido generado de `build/`.
:::

## Preferencias

Las preferencias del editor pueden leerse y escribirse mediante la ruta documentada en OpenAPI, actualmente `/prefs/{path}`.

Por ejemplo, puedes leer el tamaño de fuente configurado para el código:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

O establecerlo, por ejemplo, en 16:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

El editor valida el valor según su esquema de preferencias. Una ruta o un valor no válidos devuelven el estado HTTP `400`.

Las preferencias son configuraciones persistentes del usuario o del usuario del proyecto, no la configuración del proyecto almacenada en `game.project`. Si la automatización necesita cambiar temporalmente una preferencia, guarda el valor anterior y restáuralo después.

## Rutas definidas por el proyecto

Los scripts del editor pueden definir rutas adicionales mediante [`get_http_server_routes()`](/manuals/editor-scripts/#http-server). Una tabla opcional de operaciones OpenAPI expone una ruta mediante el mismo documento `/openapi.json` que las operaciones integradas.

Las rutas definidas por el proyecto pueden proporcionar generación de contenido, validación, informes, comprobaciones de localización, análisis de recursos, pruebas específicas del proyecto o una interfaz más pequeña para un IDE o controlador externo.

Una ruta adecuada debe realizar una operación con un nombre claro, validar su entrada, devolver un resultado estructurado, ser idempotente siempre que sea posible y limitar el trabajo costoso.

Las rutas definidas por el proyecto no están protegidas automáticamente por el token de `/eval`. Añade autenticación y comprobaciones de seguridad específicas del proyecto cuando una ruta realice operaciones sensibles.

## Hooks del ciclo de vida {#lifecycle-hooks}

Los hooks son funciones que se pueden ejecutar antes y después de las builds, antes y después de crear bundles, y cuando se inicia o termina un proceso del juego. Un proyecto puede contener un archivo `hooks.editor_script` en su raíz. Solo el archivo de hooks de la raíz recibe estos eventos, lo que proporciona al proyecto un único lugar donde definir su orden.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

Un error generado desde `on_build_started()` detiene la build del editor. Los hooks del ciclo de vida solo se ejecutan en el editor; coloca la lógica compartida de validación y generación en scripts independientes que también puedan invocarse desde CI.

## Seguridad y compatibilidad

Trata todo el servidor del editor como una interfaz local de confianza:

* No expongas públicamente el acceso al puerto.
* Protege `.internal/editor.token`; autoriza `/eval` durante la sesión actual.
* No concedas acceso externo sin restricciones a `/eval`.
* Mantén el token en la capa de integración local, no en prompts, informes o logs.
* Recuerda que las rutas definidas por el proyecto no heredan la autenticación de `/eval`.
* Utiliza un `/openapi.json` actualizado.
* Utiliza esperas limitadas para los comandos automáticos asíncronos y el inicio del editor.

## Servidor del motor

El servidor del editor pertenece al proceso del editor. Un juego en ejecución tiene un puerto diferente y responsabilidades distintas, descritas en el [manual del servicio del motor y la API HTTP de runtime](/manuals/engine-service).
