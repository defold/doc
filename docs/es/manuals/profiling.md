---
title: Profiling en Defold
brief: Este manual explica las herramientas de profiling presentes en Defold.
---

# Profiling

Defold incluye herramientas de profiling integradas con el motor y el pipeline de build. Ayudan a encontrar problemas de rendimiento, memoria y uso de recursos. Los datos de profiling en runtime pueden utilizarse mediante varias funciones:

* El profiler básico y el profiler visual dentro del juego están disponibles en todas las plataformas.
* El [profiler Remotery](https://github.com/Celtoys/Remotery) y el profiler web interactivo de frames están disponibles en plataformas de escritorio y móviles.
* Las builds de depuración de macOS que usan Metal pueden guardar [trazas de GPU](#metal-gpu-trace-capture) para inspeccionarlas en Xcode.
* Las builds HTML5 pueden publicar los scopes de Defold en la API Web Performance del navegador.

El ajuste **Profiler** del [manifiesto de la aplicación](/manuals/app-manifest/#profiler) controla si el código del profiler se enlaza con una build. **Debug Only** es el valor predeterminado, **None** lo excluye y **Always** lo incluye tanto en builds debug como release. Los ajustes de `profiler` en *game.project* controlan el comportamiento en runtime, pero no vuelven a enlazar con la build código de profiler que se haya excluido. En particular, **Track CPU** controla el muestreo de uso de CPU; es independiente de la opción del manifiesto de la aplicación.

## El profiler visual en runtime {#the-runtime-visual-profiler}

Las builds que incluyen soporte para el profiler disponen de un profiler visual en runtime que muestra información en vivo superpuesta sobre la aplicación en ejecución:

```lua
function on_reload(self)
    -- Activa o desactiva el profiler visual al hacer hot reload.
    profiler.enable_ui(true)
end
```

![Visual profiler](images/profiling/visual_profiler.png)

El profiler visual proporciona varias funciones diferentes que se pueden usar para cambiar cómo presenta sus datos:

```lua

profiler.set_ui_mode()
profiler.set_ui_view_mode()
profiler.view_recorded_frame()
```

Consulta la [referencia de la API del profiler](/ref/profiler/) para obtener más información sobre las funciones del profiler.

## El profiler web {#the-web-profiler}
Mientras se ejecuta una build de escritorio o móvil que incluya soporte para el profiler, se puede acceder desde un navegador a profilers interactivos de frames y recursos.

### Profiler de frames Remotery {#remotery-frame-profiler}
El Frame profiler te permite muestrear tu juego mientras se ejecuta y analizar frames individuales en detalle. Para acceder al profiler:

1. Inicia tu juego en tu dispositivo objetivo.
2. Selecciona el menú <kbd>Debug ▸ Open Web Profiler</kbd>.

El frame profiler está dividido en varias secciones que ofrecen distintas vistas del juego en ejecución. Pulsa el botón Pause en la esquina superior derecha para detener temporalmente la actualización de las vistas del profiler.

![Web profiler](images/profiling/webprofiler_page.png)

::: sidenote
Cuando usas varios objetivos simultáneamente, puedes cambiar manualmente entre ellos modificando el campo Connection Address en la parte superior de la página para que coincida con la URL del profiler Remotery que se muestra en la consola cuando se inició el objetivo:

```
INFO:ENGINE: Defold Engine 1.3.4 (80b1b73)
INFO:DLIB: Initialized Remotery (ws://127.0.0.1:17815/rmt)
INFO:ENGINE: Loading data from: build/default
```
:::

Sample Timeline
: Sample Timeline mostrará los frames de datos capturados en el motor, una línea de tiempo horizontal por Thread. Main es el thread principal donde se ejecutan toda la lógica del juego y la mayor parte del código del motor. Remotery corresponde al propio profiler y Sound al thread de mezcla y reproducción de sonido. Puedes acercar y alejar (con la rueda del ratón) y seleccionar frames individuales para ver los detalles de un frame en la vista Frame Data.

  ![Sample Timeline](images/profiling/webprofiler_sample_timeline.png)


Frame Data
: La vista Frame Data es una tabla donde todos los datos del frame seleccionado actualmente se desglosan en detalle. Puedes ver cuántos milisegundos se gastan en cada scope del motor.

  ![Frame data](images/profiling/webprofiler_frame_data.png)


Global Properties
: La vista Global Properties muestra una tabla de contadores. Facilitan, por ejemplo, rastrear el número de draw calls o el número de componentes de cierto tipo.

  ![Global Properties](images/profiling/webprofiler_global_properties.png)

::: sidenote
El valor LuaMem es la cantidad de memoria en kilobytes usada por la VM de Lua según lo informado por el recolector de basura de Lua. Memory es la cantidad de memoria en kilobytes usada por el motor.
:::

::: important
El [ajuste Max Sample Count](/manuals/project-settings/#max-sample-count) limita el número de muestras del profiler registradas por thread y por frame. Si el profiler indica que se ha superado el límite, comprueba primero que el código de profiling de las extensiones nativas no tenga un par de inicio/fin de scope sin correspondencia. Aumenta el límite solo cuando un frame legítimo contenga más scopes que el límite configurado.
:::

### Resource profiler
El Resource profiler te permite inspeccionar tu juego mientras se ejecuta y analizar el uso de recursos en detalle. Para acceder al profiler:

1. Inicia una build de depuración de tu juego en el dispositivo objetivo.
2. Abre la [dirección del servicio del motor](/manuals/engine-service/#availability-and-port-discovery) en un navegador: `http://<address>:<port>/`. Usa la dirección y el puerto que el motor en ejecución indica en la consola.

El resource profiler está dividido en 2 secciones: una muestra una vista jerárquica de las colecciones, objetos de juego y componentes instanciados actualmente en tu juego, y la otra muestra todos los recursos cargados actualmente.

![Resource profiler](images/profiling/webprofiler_resources_page.png)

Collection view
: La vista de colecciones muestra una lista jerárquica de todos los objetos de juego y componentes instanciados actualmente en el juego, y de qué colección provienen. Es una herramienta muy útil cuando necesitas examinar y entender qué has instanciado en tu juego en un momento dado y de dónde provienen los objetos.

Resources view
: La vista de recursos muestra todos los recursos cargados actualmente en memoria, su tamaño y el número de referencias a cada recurso. Esto resulta útil al optimizar el uso de memoria en tu aplicación cuando necesitas entender qué está cargado en memoria en un momento dado.

#### Tiempos de carga de recursos {#resource-loading-times}

También puedes inspeccionar cuánto tarda en cargarse cada recurso. Activa [Resource → Profile](/manuals/project-settings/#profile) en *game.project* antes de lanzar el juego. En la vista de texto, este ajuste es:

```ini
[resource]
profile = 1
```

El ajuste está desactivado de forma predeterminada. Reinicia el juego después de activarlo para medir las cargas de inicio. Cada carga completada o fallida escribe una entrada de log de nivel INFO con la ruta del recurso, el tiempo total y los tiempos de las etapas de precarga, lectura, creación, poscreación, cola y espera. Los aciertos de caché no generan nuevos registros de carga.

En el profiler de recursos, haz click en **Capture** y después en **Show load times** para mostrar las columnas de tiempos. **Capture** actualiza la vista de las mediciones conservadas; no activa el profiling ni mide cargas anteriores de forma retroactiva.

| Columna | Significado |
| --- | --- |
| **Load (ms)** | Tiempo total transcurrido durante la carga inicial, incluidas las dependencias, el trabajo de poscreación, las colas y las esperas. |
| **Preload (ms)** | Tiempo dedicado a preparar el recurso en su callback de precarga. |
| **Read (ms)** | Tiempo dedicado a leer los datos del recurso. |
| **Create (ms)** | Tiempo dedicado a crear el recurso de runtime en su callback de creación. |

Mostrar los tiempos de carga ordena la tabla por el tiempo total, con los recursos más lentos primero. Haz click en el encabezado de una columna de tiempos para ordenar por esa etapa y vuelve a hacer click para invertir el orden. Las barras de la columna **Load** muestran cada total en relación con el recurso visible más lento. Haz click en **Hide load times** para volver a ocultar las columnas.

Los tiempos de carga y de callbacks incluyen el trabajo de dependencias anidadas. No sumes los totales de distintos recursos para calcular el tiempo de inicio, porque el mismo trabajo puede aparecer en la medición de más de un recurso. Las columnas **Preload**, **Read** y **Create** tampoco representan todo el tiempo total de carga; el log proporciona las etapas adicionales.

Una raya (`—`) significa que no hay una medición completada disponible, por ejemplo porque el profiling estaba desactivado o la carga inicial no ha terminado. Un cero medido se muestra como `0.000`. Las mediciones describen la carga inicial: los aciertos de caché y las recargas en caliente no las modifican, y descargar un recurso elimina su medición conservada.

## Captura de trazas de GPU Metal {#metal-gpu-trace-capture}

El [servicio HTTP del motor](/manuals/engine-service/#metal-gpu-trace-endpoint) puede capturar comandos de GPU Metal en un documento *.gputrace* en macOS. Abre la traza completada en Xcode para inspeccionar los frames capturados. Esta funcionalidad está integrada en el motor de depuración.

### Lanzar y comprobar la compatibilidad {#launch-and-check-support}

Crea un [bundle Debug](/manuals/bundling/#release-vs-debug) de macOS que incluya el backend gráfico nativo Metal. Si usas un App Manifest, selecciona una opción **Graphics (macOS)** que incluya Metal; consulta [backends gráficos](/manuals/app-manifest/#graphics).

Lanza el ejecutable del bundle desde una terminal con `METAL_CAPTURE_ENABLED=1` y selecciona el adaptador Metal. Sustituye la ruta del bundle y el nombre del ejecutable en este ejemplo:

```sh
METAL_CAPTURE_ENABLED=1 \
    "/absolute/path/MyGame.app/Contents/MacOS/MyGame" --graphics-adapter=metal
```

La variable de ambiente debe estar definida al iniciar el motor. Establecerla solo en una terminal usada para solicitudes HTTP no activa la captura en un motor que ya se está ejecutando.

En una segunda terminal, usa el [puerto del servicio del motor que aparece en el log](/manuals/engine-service/#availability-and-port-discovery). Los siguientes ejemplos usan `curl` y `jq`:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq '.paths["/profiler/gputrace"]'
curl -sS -i "$ENGINE_URL/profiler/gputrace"
```

La ruta solo se registra en macOS. Una entrada `null` en el documento OpenAPI significa que este motor no la expone. Aunque la ruta esté presente, la compatibilidad con la captura depende del adaptador gráfico y del entorno de lanzamiento. `GET /profiler/gputrace` devuelve HTTP 501 con `error.code: "gputrace_unsupported"` cuando la captura Metal no está disponible. Comprueba que el motor use Metal y se haya lanzado con `METAL_CAPTURE_ENABLED=1` antes de continuar. Una solicitud compatible devuelve HTTP 200 con el estado de captura.

### Capturar e inspeccionar frames {#capture-and-inspect-frames}

Elige una ruta de salida absoluta con permiso de escritura que termine en `.gputrace`, con un directorio padre existente y sin una traza ya guardada en ella. La ruta pertenece a la computadora que ejecuta el motor. Para un motor local, este ejemplo crea un directorio temporal nuevo y solicita un frame:

```sh
GPU_TRACE_DIR=$(mktemp -d /tmp/defold-gputrace.XXXXXX)
GPU_TRACE_PATH="$GPU_TRACE_DIR/frame.gputrace"
GPU_TRACE_REQUEST=$(jq -n --arg path "$GPU_TRACE_PATH" '{path: $path, frames: 1}')
curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    --data "$GPU_TRACE_REQUEST" \
    "$ENGINE_URL/profiler/gputrace" | jq
```

`frames` es opcional, vale `1` de forma predeterminada y acepta enteros entre `1` y `10000`. La captura comienza antes del siguiente frame renderizado y termina después de enviar el número solicitado de frames completos. Mantén el juego renderizando mientras esperas. Solo puede haber una captura pendiente o activa; otra solicitud de inicio devuelve HTTP 409 con `error.code: "gputrace_active"`.

`POST` devuelve HTTP 200 con `ok: true` y `data.state: "pending"` cuando se programa la captura. Las solicitudes de estado posteriores indican cuándo termina. Repite la solicitud de estado hasta que `data.state` sea `complete`, `canceled` o `failed`:

```sh
curl -fsS "$ENGINE_URL/profiler/gputrace" | jq
```

| `data.state` | Significado |
| --- | --- |
| `idle` | No se ha programado ninguna captura. |
| `pending` | La captura espera a que comience el renderizado. |
| `capturing` | La captura está activa; `data.frames_captured` indica los frames completados. |
| `complete` | La captura ha terminado y la traza puede abrirse. |
| `canceled` | Una captura pendiente se canceló antes de empezar. |
| `failed` | La captura no pudo iniciarse; inspecciona `data.error` para conocer el error nativo. |

`GET` describe la captura actual o más reciente. Comprueba que `data.path` coincida con la ruta solicitada. Una captura fallida sigue devolviendo HTTP 200 con `ok: true`; inspecciona `data.state` y `data.error` para determinar el resultado. En un cliente automatizado, consulta el estado con una pausa entre solicitudes y un tiempo límite.

Cuando el estado sea `complete`, abre la traza en Xcode en el Mac del motor:

```sh
open -a Xcode "$GPU_TRACE_PATH"
```

El endpoint HTTP devuelve el estado; la traza se guarda en `data.path` en el host del motor. Si el motor es remoto, recupera el documento completado desde ese host antes de abrirlo localmente.

### Cancelar o detener una captura {#cancel-or-stop-a-capture}

Para cancelar una captura pendiente o terminar antes una captura activa:

```sh
curl -fsS -X DELETE "$ENGINE_URL/profiler/gputrace" | jq
```

Una captura pendiente cambia a `canceled`. En una captura activa, `data.stop_requested` pasa a ser `true`, y la captura termina después de enviar el frame que se está renderizando. Sigue consultando `GET` hasta alcanzar un estado final. `DELETE` conserva cualquier traza ya escrita en disco. Si no hay ninguna captura pendiente o activa, devuelve HTTP 409 con `error.code: "gputrace_inactive"`.

## Línea de tiempo de rendimiento del navegador en HTML5 {#html5-browser-performance-timeline}

HTML5 usa la API Web Performance en lugar de Remotery para su línea de tiempo del navegador. Para registrar los scopes de Defold:

1. Asegúrate de que el modo del profiler seleccionado en el manifiesto de la aplicación incluya soporte para el profiler en la variante de build que estás ejecutando.
2. Activa **Performance Timeline Enabled** (`profiler.performance_timeline_enabled`) en *game.project*.
3. Inicia la build HTML5 y abre las herramientas para desarrolladores del navegador.
4. Graba una sesión en el panel **Performance** del navegador e inspecciona los scopes de Defold en la línea de tiempo resultante.

Esta línea de tiempo del navegador es independiente tanto del profiler visual dentro del juego como del profiler web interactivo Remotery.


## Reportes de build {#build-reports}
Al crear un bundle de tu juego hay una opción para crear un reporte de build. Esto es muy útil para entender el tamaño de todos los assets que forman parte del bundle de tu juego. Simplemente marca la casilla *Generate build report* al crear el bundle del juego.

![reporte de build](images/profiling/build_report.png)

El builder producirá un archivo llamado `report.html` junto al bundle del juego. Abre el archivo en un navegador web para inspeccionar el reporte:

![reporte de build](images/profiling/build_report_html.png)

*Overview* ofrece un desglose visual general del tamaño del proyecto basado en el tipo de recurso.

*Resources* muestra una lista detallada de recursos que puedes ordenar por tamaño, relación de compresión, cifrado, tipo y nombre de directorio. Usa el campo "search" para filtrar las entradas de recursos mostradas.

La sección *Structure* muestra tamaños según cómo están organizados los recursos en la estructura de archivos del proyecto. Las entradas están codificadas por color desde verde (ligero) hasta azul (pesado), de acuerdo con el tamaño relativo del contenido de archivos y directorios.


## Herramientas externas {#external-tools}
Además de las herramientas integradas, hay una amplia variedad de herramientas gratuitas de tracing y profiling de alta calidad disponibles. Esta es una selección:

ProFi (Lua)
: No incluimos ningún profiler de Lua integrado, pero hay bibliotecas externas que son bastante fáciles de usar. Para encontrar dónde tus scripts gastan tiempo, inserta tú mismo mediciones de tiempo en tu código o usa una biblioteca de profiling de Lua como [ProFi](https://github.com/jgrahamc/ProFi).

  Ten en cuenta que los profilers de Lua puro añaden bastante sobrecarga con cada hook que instalan. Por este motivo, debes tener cierta cautela con los perfiles de tiempos que obtengas de una herramienta así. Los perfiles de conteo sí son suficientemente precisos.

Instruments (macOS e iOS)
: Este es un analizador y visualizador de rendimiento que forma parte de Xcode. Te permite trazar e inspeccionar el comportamiento de una o más apps o procesos, examinar funcionalidades específicas del dispositivo (como Wi-Fi y Bluetooth) y mucho más.

  ![instruments](images/profiling/instruments.png)

OpenGL profiler (macOS)
: Forma parte del paquete "Additional Tools for Xcode" que puedes descargar de Apple (selecciona <kbd>Xcode ▸ Open Developer Tool ▸ More Developer Tools...</kbd> en el menú de Xcode).

  Esta herramienta te permite inspeccionar una aplicación Defold en ejecución y ver cómo usa OpenGL. Te permite hacer trazas de llamadas a funciones de OpenGL, definir breakpoints en funciones de OpenGL, investigar recursos de la aplicación (texturas, programas, shaders, etc.), revisar contenidos de buffers y comprobar otros aspectos del estado de OpenGL.

  ![opengl profiler](images/profiling/opengl.png)

Android Profiler (Android)
: https://developer.android.com/studio/profile/android-profiler.html

  Un conjunto de herramientas de profiling que captura datos en tiempo real de la actividad de CPU, memoria y red de tu juego. Puedes realizar trazado de métodos basado en muestras de la ejecución del código, capturar heap dumps, ver asignaciones de memoria e inspeccionar los detalles de los archivos transmitidos por la red. Usar la herramienta requiere que establezcas `android:debuggable="true"` en `AndroidManifest.xml`.

  ![android profiler](images/profiling/android_profiler.png)

  Nota: Desde Android Studio 4.1 también es posible [ejecutar las herramientas de profiling sin iniciar Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Esta es una colección de herramientas que te permite inspeccionar, ajustar y reproducir llamadas de una aplicación a un driver gráfico. Usar la herramienta requiere que establezcas `android:debuggable="true"` en `AndroidManifest.xml`.

  ![graphics api debugger](images/profiling/gapid.png)
