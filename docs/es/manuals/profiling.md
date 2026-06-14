---
title: Profiling en Defold
brief: Este manual explica las herramientas de profiling presentes en Defold.
---

# Profiling

Defold incluye un conjunto de herramientas de profiling integradas con el motor y el pipeline de build. Están diseñadas para ayudar a encontrar problemas de rendimiento y uso de memoria. Los profilers integrados solo están disponibles en builds de depuración. El profiler de frames que se usa en Defold es el [profiler Remotery de Celtoys](https://github.com/Celtoys/Remotery).

## El profiler visual en runtime

Las builds de depuración incluyen un profiler visual en runtime que muestra información en vivo renderizada superpuesta sobre la aplicación en ejecución:

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

Consulta la [referencia de la API del profiler](/ref/stable/profiler/) para obtener más información sobre las funciones del profiler.

## El profiler web
Mientras se ejecuta una build de depuración del juego, se puede acceder a un profiler interactivo basado en web desde un navegador.

### Frame profiler
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

### Resource profiler
El Resource profiler te permite inspeccionar tu juego mientras se ejecuta y analizar el uso de recursos en detalle. Para acceder al profiler:

1. Inicia tu juego en tu dispositivo objetivo.
2. Abre un navegador y ve a http://localhost:8002

El resource profiler está dividido en 2 secciones: una muestra una vista jerárquica de las colecciones, objetos de juego y componentes instanciados actualmente en tu juego, y la otra muestra todos los recursos cargados actualmente.

![Resource profiler](images/profiling/webprofiler_resources_page.png)

Collection view
: La vista de colecciones muestra una lista jerárquica de todos los objetos de juego y componentes instanciados actualmente en el juego, y de qué colección provienen. Es una herramienta muy útil cuando necesitas examinar y entender qué has instanciado en tu juego en un momento dado y de dónde provienen los objetos.

Resources view
: La vista de recursos muestra todos los recursos cargados actualmente en memoria, su tamaño y el número de referencias a cada recurso. Esto resulta útil al optimizar el uso de memoria en tu aplicación cuando necesitas entender qué está cargado en memoria en un momento dado.


## Reportes de build {#build-reports}
Al crear un bundle de tu juego hay una opción para crear un reporte de build. Esto es muy útil para entender el tamaño de todos los assets que forman parte del bundle de tu juego. Simplemente marca la casilla *Generate build report* al crear el bundle del juego.

![reporte de build](images/profiling/build_report.png)

El builder producirá un archivo llamado "report.html" junto al bundle del juego. Abre el archivo en un navegador web para inspeccionar el reporte:

![reporte de build](images/profiling/build_report_html.png)

*Overview* ofrece un desglose visual general del tamaño del proyecto basado en el tipo de recurso.

*Resources* muestra una lista detallada de recursos que puedes ordenar por tamaño, relación de compresión, cifrado, tipo y nombre de directorio. Usa el campo "search" para filtrar las entradas de recursos mostradas.

La sección *Structure* muestra tamaños según cómo están organizados los recursos en la estructura de archivos del proyecto. Las entradas están codificadas por color desde verde (ligero) hasta azul (pesado), de acuerdo con el tamaño relativo del contenido de archivos y directorios.


## Herramientas externas
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

  Un conjunto de herramientas de profiling que captura datos en tiempo real de la actividad de CPU, memoria y red de tu juego. Puedes realizar trazado de métodos basado en muestras de la ejecución del código, capturar heap dumps, ver asignaciones de memoria e inspeccionar los detalles de los archivos transmitidos por la red. Usar la herramienta requiere que establezcas `android:debuggable="true"` en "AndroidManifest.xml".

  ![android profiler](images/profiling/android_profiler.png)

  Nota: Desde Android Studio 4.1 también es posible [ejecutar las herramientas de profiling sin iniciar Android Studio](https://developer.android.com/studio/profile/android-profiler.html#standalone-profilers).

Graphics API Debugger (Android)
: https://github.com/google/gapid

  Esta es una colección de herramientas que te permite inspeccionar, ajustar y reproducir llamadas de una aplicación a un driver gráfico. Usar la herramienta requiere que establezcas `android:debuggable="true"` en "AndroidManifest.xml".

  ![graphics api debugger](images/profiling/gapid.png)
