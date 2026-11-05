---
title: Configuración del proyecto Defold
brief: Este manual describe cómo funciona la configuración específica del proyecto en Defold.
---

# Configuración del proyecto {#project-settings}

El archivo *game.project* contiene toda la configuración global del proyecto. Debe permanecer en la carpeta raíz del proyecto y llamarse *game.project*. Lo primero que hace el motor al iniciarse y lanzar tu juego es buscar este archivo.

Cada configuración del archivo pertenece a una categoría. Cuando abres el archivo, Defold muestra todas las configuraciones agrupadas por categoría.

![Configuración del proyecto](images/project-settings/settings.jpg)


## Formato de archivo {#file-format}

La configuración en *game.project* normalmente se cambia desde Defold, pero el archivo también se puede editar en cualquier editor de texto estándar. El archivo sigue el estándar de formato de archivo INI y se ve así:

```ini
[category1]
setting1 = value
setting2 = value
[category2]
...
```

Un ejemplo real es:

```ini
[bootstrap]
main_collection = /main/main.collectionc
```

lo que significa que la configuración *main_collection* pertenece a la categoría *bootstrap*. Cada vez que se usa una referencia de archivo, como en el ejemplo anterior, la ruta debe llevar agregado un carácter 'c', lo que significa que estás referenciando la versión compilada del archivo. Ten en cuenta también que la carpeta que contiene *game.project* será la raíz del proyecto, por eso hay una '/' inicial en la ruta de la configuración.


## Acceso en runtime {#runtime-access}

Es posible leer valores de *game.project* en runtime usando [`sys.get_config_string(key)`](/ref/sys/#sys.get_config_string), [`sys.get_config_number(key)`](/ref/sys/#sys.get_config_number), [`sys.get_config_int(key)`](/ref/sys/#sys.get_config_int) y [`sys.get_config_boolean(key)`](/ref/sys/#sys.get_config_boolean). Ejemplos:

```lua
local title = sys.get_config_string("project.title")
local gravity_y = sys.get_config_number("physics.gravity_y")
local fullscreen = sys.get_config_boolean("display.fullscreen", false)
```

::: sidenote
La clave es una combinación de la categoría y el nombre de la configuración, separados por un punto, y escrita en minúsculas con cualquier carácter de espacio reemplazado por guiones bajos. Ejemplos: el campo "Title" de la categoría "Project" se convierte en `project.title`, y el campo "Gravity Y" de la categoría "Physics" se convierte en `physics.gravity_y`.
:::


## Secciones y configuraciones {#sections-and-settings}

A continuación se muestran todas las configuraciones disponibles, organizadas por categoría.

### Project

#### Title
El título de la aplicación.

#### Version
La versión de la aplicación.

#### Publisher
Nombre del publicador.

#### Developer
Nombre del desarrollador.

#### Write Log File
Controla cuándo el motor escribe un archivo de log. Opciones:

- "Never": no escribir un archivo de log.
- "Debug": escribir un archivo de log solo para builds Debug.
- "Always": escribir un archivo de log tanto para builds Debug como Release.

Si se ejecuta más de una instancia desde el editor, el archivo se llamará *instance_2_log.txt*, donde `2` es el índice de la instancia. Si se ejecuta una sola instancia o desde un bundle, el archivo se llamará *log.txt*. La ubicación del archivo de log será una de las siguientes rutas (se prueban en orden):

1. La ruta especificada en *project.log_dir* (configuración oculta)
2. La ruta de log del sistema:
  * macOS/iOS: `NSDocumentDirectory`
  * Android: `Context.getExternalFilesDir()`
  * Otros: raíz de la aplicación
3. La ruta de soporte de la aplicación
  * macOS/iOS: `NSApplicationSupportDirectory`
  * Windows: `CSIDL_APPDATA` (por ejemplo, `C:\Users\<username>\AppData\Roaming`)
  * Android: `Context.getFilesDir()`
  * Linux: variable de ambiente `HOME`

#### Minimum Log Level
Especifica el nivel mínimo de log para el sistema de logging. Solo se mostrarán los logs de este nivel o superiores.

#### Compress Archive
Activa la compresión de archivos al crear bundles. Ten en cuenta que actualmente esto se aplica a todas las plataformas excepto Android, donde el apk ya contiene todos los datos comprimidos.

#### Dependencies
Una lista de URL a las *Library URL* del proyecto. Consulta el [manual de bibliotecas](/manuals/libraries/) para obtener más información.

#### Dependencies Metadata
`project.dependencies_metadata` incluye metadatos sobre las dependencias de bibliotecas en el bundle de runtime. Desactivado de forma predeterminada. Los metadatos se pueden leer en runtime usando `sys.load_resource("/.internal/dependencies.json")`.

#### Custom Resources
`custom_resources`
:[Custom Resources](../shared/custom-resources.md)

La carga de recursos personalizados se explica con más detalle en el [manual de acceso a archivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

Las rutas aportadas por las extensiones mediante `custom_resources.default` en `ext.properties` se combinan con esta configuración. Consulta [recursos personalizados de las extensiones](/manuals/extensions/#custom-resources) para ver un ejemplo.

#### Bundle Resources
`bundle_resources`
:[Bundle Resources](../shared/bundle-resources.md)

La carga de recursos de bundle se explica con más detalle en el [manual de acceso a archivos](/manuals/file-access/#how-to-access-files-bundled-with-the-application).

#### Bundle Exclude Resources
`bundle_exclude_resources`
Una lista separada por comas de recursos que no deben incluirse en el bundle. Es decir, se eliminan del resultado del paso de recopilación de `bundle_resources`.

---

### Bootstrap

#### Main Collection
Referencia de archivo de la colección que se usará para iniciar la aplicación, `/logic/main.collection` de forma predeterminada.

#### Render
Qué archivo de configuración de render usar, el cual define el pipeline de renderizado, `/builtins/render/default.render` de forma predeterminada.

---

### Library

#### Include Dirs
Una lista de directorios separados por espacios que deben compartirse desde tu proyecto mediante el uso compartido de bibliotecas. Consulta el [manual de bibliotecas](/manuals/libraries/) para obtener más información.

#### Defold Min Version
`library.defold_min_version` especifica la versión mínima de Defold/Bob necesaria para usar este proyecto como biblioteca, por ejemplo, `1.11.2`. Deja el campo vacío para no especificar una versión mínima.

---

### Engine

#### Run While Iconified
Permite que el motor siga ejecutándose mientras la ventana de la aplicación está iconificada (solo plataformas de escritorio).

#### Fixed Update Frequency
La frecuencia de actualización de la función de ciclo de vida `fixed_update(self, dt)`. En Hertz.

#### Max Time Step
Si el paso de tiempo se vuelve demasiado grande durante un solo frame, se limitará a este valor máximo. Segundos.

---

### Display

En plataformas de escritorio, las ventanas del motor abiertas desde el editor pueden restaurar un tamaño guardado en una ejecución anterior. Elige <kbd>Debug ▸ Reset Simulated Resolution</kbd> para borrar los tamaños recordados y volver al tamaño configurado, conservando las posiciones guardadas. Consulta [posición, tamaño y restablecimiento de ventanas del motor](/manuals/editor/#engine-window-placement) para más detalles.

#### Width
El ancho en pixeles de la ventana de la aplicación.

#### Height
La altura en pixeles de la ventana de la aplicación.

#### High Dpi
Crea un back buffer de alta densidad de pixeles en pantallas que lo soportan. Normalmente, el juego se renderizará al doble de la resolución establecida en las configuraciones *Width* y *Height*, que seguirán siendo la resolución lógica usada en scripts y propiedades.

En HTML5, usa [Min Pixel Ratio](#min-pixel-ratio) y [Max Pixel Ratio](#max-pixel-ratio) para limitar la escala de renderizado cuando este ajuste está activado.

#### Samples
Cuántas muestras usar para super sampling anti-aliasing. Define el window hint `GLFW_FSAA_SAMPLES`. Un valor de `0` significa que el anti-aliasing está desactivado.

Esta configuración controla la ventana. Los [render targets con multimuestreo](/manuals/render/#multisampled-render-targets) fuera de pantalla tienen su propio número de muestras.

#### Fullscreen
Marca esta opción si la aplicación debe iniciar en pantalla completa. Si no está marcada, la aplicación se ejecuta en una ventana.

#### Update Frequency
La tasa de frames deseada en Hertz. Define 0 para una tasa de frames variable. Un valor mayor que 0 dará como resultado una tasa de frames fija limitada en runtime hacia la tasa de frames real (lo que significa que no puedes actualizar el loop del juego dos veces en un frame del motor). Usa [`sys.set_update_frequency(hz)`](https://defold.com/ref/sys/?q=set_update_frequency#sys.set_update_frequency:frequency) para cambiar este valor en runtime. Esta configuración también funciona en builds headless.

#### Swap interval
Este valor entero controla cómo la aplicación gestiona vsync. 0 desactiva vsync, y el valor predeterminado es 1. Al usar un adaptador OpenGL, este valor define el número de frames que la ventana debe [actualizar entre intercambios de buffer](https://www.khronos.org/opengl/wiki/Swap_Interval). Para Vulkan no existe un concepto integrado de swap interval; en su lugar, el valor controla si vsync debe estar activado o no.

#### Vsync
Configuración heredada de compatibilidad. Esta configuración está obsoleta; usa **Swap Interval** en proyectos nuevos. Si se desactiva, fuerza el intervalo de intercambio efectivo a `0`. Si se activa, **Swap Interval** determina el valor efectivo.

#### Display Profiles
Especifica qué archivo de perfiles de pantalla usar, `/builtins/render/default.display_profilesc` de forma predeterminada. Aprende más en el [manual de layouts de GUI](/manuals/gui-layouts/#creating-display-profiles).

#### Dynamic Orientation
Marca esta opción si la app debe cambiar dinámicamente entre orientación vertical y horizontal al rotar el dispositivo. Ten en cuenta que la app de desarrollo actualmente no respeta esta configuración.

#### Display Device Info
Muestra información de GPU en la consola al iniciar.

---

### Render

#### Clear Color Red
Canal rojo del color de limpieza, usado por el script de render y cuando se crea la ventana.

#### Clear Color Green
Canal verde del color de limpieza, usado por el script de render y cuando se crea la ventana.

#### Clear Color Blue
Canal azul del color de limpieza, usado por el script de render y cuando se crea la ventana.

#### Clear Color Alpha
Canal alfa del color de limpieza, usado por el script de render y cuando se crea la ventana.

---

### Physics

#### Max Collision Object Count
Número máximo de objetos colisionadores.

#### Type
Qué tipo de físicas usar, `2D` o `3D`.

#### Gravity X
Gravedad del mundo a lo largo del eje x. En metros por segundo.

#### Gravity Y
Gravedad del mundo a lo largo del eje y. En metros por segundo.

#### Gravity Z
Gravedad del mundo a lo largo del eje z. En metros por segundo.

#### Debug
Marca esta opción si las físicas deben visualizarse para depuración.

#### Debug Alpha
Valor del componente alfa para las físicas visualizadas, `0`--`1`.

#### World Count
Número máximo de mundos de físicas concurrentes, `4` de forma predeterminada. Si cargas más de 4 mundos simultáneamente mediante proxies de colección, debes aumentar este valor. Ten presente que cada mundo de físicas asigna una cantidad considerable de memoria.

#### Scale
Indica al motor de físicas cómo escalar los mundos de físicas en relación con el mundo del juego para obtener precisión numérica, `0.01`--`1.0`. Si el valor se define como `0.02`, significa que el motor de físicas verá 50 unidades como 1 metro ($1 / 0.02$).

#### Allow Dynamic Transforms
Marca esta opción si el motor de físicas debe aplicar la transformación de un objeto de juego a cualquier componente de objeto colisionador adjunto. Esto se puede usar para mover, escalar y rotar formas de colisión, incluso las que son dinámicas.

#### Use Fixed Timestep
Marca esta opción si el motor de físicas debe usar actualizaciones de paso de tiempo fijo e independientes del frame rate. Usa esta configuración en combinación con la función de ciclo de vida `fixed_update(self, dt)` y la configuración de proyecto `engine.fixed_update_frequency` para interactuar con el motor de físicas a intervalos regulares. Para proyectos nuevos, la configuración recomendada es `true`.

#### Debug Scale
El tamaño con el que dibujar objetos unitarios en físicas, como tríadas y normales.

#### Max Collisions
Cuántas colisiones se reportarán de vuelta a los scripts.

#### Max Contacts
Cuántos puntos de contacto se reportarán de vuelta a los scripts.

#### Contact Impulse Limit
Ignora impulsos de contacto con valores menores que esta configuración.

#### Ray Cast Limit 2d
El número máximo de solicitudes de ray cast 2D por frame.

#### Ray Cast Limit 3d
El número máximo de solicitudes de ray cast 3D por frame.

#### Trigger Overlap Capacity
El número máximo de triggers de físicas superpuestos.

#### Velocity Threshold
Velocidad mínima que dará lugar a colisiones elásticas.

#### Max Fixed Timesteps
Número máximo de pasos en la simulación al usar paso de tiempo fijo (solo 3D).

---

### Graphics

#### Default Texture Min Filter
Especifica qué filtrado usar para el filtrado de minificación.

#### Default Texture Mag Filter
Especifica qué filtrado usar para el filtrado de magnificación.

#### Max Draw Calls
El número máximo de llamadas de render.

#### Max Characters:
El número de caracteres preasignados en el buffer de renderizado de texto, es decir, el número de caracteres que se pueden mostrar en cada frame.

#### Max Font Batches
El número máximo de lotes de texto que se pueden mostrar en cada frame.

#### Max Debug Vertices
El número máximo de vértices de debug. Se usa, entre otras cosas, para renderizar formas de físicas.

#### Texture Profiles
El archivo de perfiles de textura que se usará para este proyecto, `/builtins/graphics/default.texture_profiles` de forma predeterminada.

#### Verify Graphics Calls
Verifica el valor de retorno después de cada llamada gráfica y reporta cualquier error en el log.

#### WebGL Version Hint
`graphics.webgl_version_hint` selecciona la versión del contexto WebGL que se solicitará en HTML5. Los valores válidos son `1` (WebGL 1) y `2` (WebGL 2, predeterminado). Establécelo en `1` para usar o probar WebGL 1 incluso en un navegador compatible con WebGL 2. Desactiva [Exclude GLES 2.0](#exclude-gles-20) cuando uses WebGL 1 para incluir los shaders necesarios.

#### OpenGL Version Hint
Indicación de versión de contexto OpenGL. Si se selecciona una versión específica, se usará como versión mínima requerida (no se aplica a OpenGL ES).

#### OpenGL Core Profile Hint
Define la indicación de perfil 'core' de OpenGL al crear el contexto. El perfil core elimina todas las funcionalidades obsoletas de OpenGL, como el renderizado en modo inmediato. No se aplica a OpenGL ES.

#### Vulkan Version Major
`graphics.vulkan_version_major` es la indicación de versión mayor del contexto/API de Vulkan. Solo se aplica cuando se selecciona el backend gráfico Vulkan. El valor predeterminado es `1`.

#### Vulkan Version Minor
`graphics.vulkan_version_minor` es la indicación de versión menor del contexto/API de Vulkan. Solo se aplica cuando se selecciona el backend gráfico Vulkan. El valor predeterminado es `0`.

---

### Shader

#### Exclude GLES 2.0
`shader.exclude_gles_sm100` excluye los shaders de OpenGLES 2.0 y WebGL 1.0. Está activado de forma predeterminada (`1`).

Para usar estas API gráficas o permitir recurrir a ellas, desmarca **Shader ▸ Exclude GLES 2.0** en *game.project* o establece:

```ini
[shader]
exclude_gles_sm100 = 0
```

Los proyectos que no establecen esta opción explícitamente usan el valor predeterminado. Establécela en `0` explícitamente si el proyecto necesita compatibilidad con OpenGLES 2.0 o WebGL 1.0.

#### GLSL ES Default Precision Float
`shader.glsl_es_default_precision_float` define el calificador de precisión global predeterminado para valores de punto flotante en shaders GLSL ES compilados de forma cruzada. Los valores válidos son `mediump` y `highp`; el predeterminado es `mediump`.

#### GLSL ES Default Precision Int
`shader.glsl_es_default_precision_int` define el calificador de precisión global predeterminado para valores enteros en shaders GLSL ES compilados de forma cruzada. Los valores válidos son `mediump` y `highp`; el predeterminado es `highp`.

---

### Input

#### Repeat Delay
Segundos que esperar antes de que un input mantenido presionado empiece a repetirse.

#### Repeat Interval
Segundos que esperar entre cada repetición de un input mantenido presionado.

#### Gamepads
Referencia al archivo de configuración de gamepads, que mapea señales de gamepad al sistema operativo, `/builtins/input/default.gamepads` de forma predeterminada.

#### Gamepad Database
`input.gamepad_database` selecciona una base de datos de asignaciones de gamepads en formato SDL (`.txt`). El valor predeterminado es `/builtins/input/gamecontrollerdb.txt`. Sus asignaciones se combinan con el archivo *Gamepads* al compilar el proyecto.

#### Gamepad Deadzone
`input.gamepad_deadzone` define la zona muerta que se aplica en runtime a las asignaciones de la base de datos SDL de gamepads. El valor predeterminado es `0.2`.

#### Game Binding
Referencia al archivo de configuración de input, que mapea inputs de hardware a acciones, `/input/game.input_binding` de forma predeterminada.

#### Use Accelerometer
Marca esta opción para hacer que el motor reciba eventos de input del acelerómetro en cada frame. Desactivar el input del acelerómetro puede dar cierto beneficio de rendimiento.

---

### Resource

#### Http Cache
Si está marcada, se activa una caché HTTP para cargar más rápido recursos por red hacia el motor que se ejecuta en el dispositivo.

#### Uri
Dónde encontrar los datos de build del proyecto, en formato URI.

#### Max Resources
El número máximo de recursos que se pueden cargar al mismo tiempo.

#### Profile
`resource.profile` activa la medición de tiempos de carga de recursos y los logs de nivel INFO para cada carga completada o fallida. Está desactivado de forma predeterminada (`0`). Actívalo (`1`) antes de lanzar el juego para medir las cargas de inicio. El profiler de recursos muestra las mediciones conservadas de carga inicial de los recursos cargados actualmente; haz click en **Capture** y después en **Show load times** para inspeccionarlas. Consulta [Tiempos de carga de recursos](/manuals/profiling/#resource-loading-times) para conocer las columnas y cómo interpretarlas.

---

### Network

#### Http Timeout
El timeout HTTP en segundos. Define `0` para desactivar el timeout.

#### Http Thread Count
El número de worker threads para el servicio HTTP.

#### Http Cache Enabled
Marca esta opción para activar la caché HTTP para solicitudes de red (usando `http.request()`). La caché HTTP almacenará la respuesta asociada con una solicitud y reutilizará la respuesta almacenada para solicitudes posteriores. La caché HTTP soporta los headers de respuesta HTTP `ETag` y `Cache-Control: max-age`.

#### SSL Certificates
Archivo que contiene certificados raíz SSL para usar al verificar la cadena de certificados durante handshakes SSL.

---

### Collection

#### Max Instances
Número máximo de instancias de objetos de juego en una colección, `1024` de forma predeterminada. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Max Input Stack Entries
Número máximo de objetos de juego en la pila de input.

---

### Sound

#### Gain
Ganancia global (volumen), `0`--`1`.

#### Use Linear Gain
Si está activada, la ganancia es lineal. Si está desactivada, usa una curva exponencial.

#### Max Sound Data
Número máximo de recursos de sonido, es decir, el número de archivos de sonido únicos en runtime.

#### Max Sound Buffers
(Actualmente no se usa) Número máximo de buffers de sonido concurrentes.

#### Max Sound Sources
(Actualmente no se usa) Número máximo de sonidos que se reproducen de forma concurrente.

#### Max Sound Instances
Número máximo de instancias de sonido concurrentes, es decir, sonidos reales reproducidos al mismo tiempo.

#### Max Component Count
Número máximo de componentes de sonido por colección.

#### Sample Frame Count
Número de muestras usadas para cada actualización de audio. 0 significa automático (1024 para 48 kHz, 768 para 44.1 kHz).

#### Use Thread
Si está marcada, el sistema de sonido usará threads para la reproducción de sonido y así reducir el riesgo de tirones cuando el thread principal está bajo mucha carga.

#### Stream Enabled
Si está marcada, el sistema de sonido usará streaming para cargar archivos fuente.

#### Stream Cache Size
El tamaño máximo de la caché de chunks de sonido que contiene _todos_ los chunks. `2097152` bytes de forma predeterminada.
Este número debe ser mayor que el número de archivos de sonido cargados multiplicado por el tamaño de chunk de stream.
De lo contrario, corres el riesgo de expulsar chunks nuevos en cada frame.

#### Stream Chunk Size
El tamaño en bytes de cada chunk transmitido por streaming.

#### Stream Preload Size
Determina el tamaño en bytes del chunk inicial para archivos de sonido leídos desde el archivo.

---

### Sprite

#### Max Count
Número máximo de sprites por colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Subpixels
Marca esta opción para permitir que los sprites aparezcan desalineados con respecto a los pixeles.

---

### Tilemap

#### Max Count
Número máximo de tile maps por colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Max Tile Count
Número máximo de tiles visibles concurrentes por colección.

---

### Spine

#### Max Count
Número máximo de componentes de modelo Spine. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### Mesh

#### Max Count
Número máximo de componentes mesh por colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### Model

#### Max Count
Número máximo de componentes de modelo por colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Split Meshes
Divide meshes con más de 65536 vértices en meshes nuevos.

#### Max Bone Matrix Texture Width
Ancho máximo de la textura de matriz de huesos. Solo se usa el tamaño necesario para animaciones, redondeado hacia arriba a la potencia de dos más cercana.

#### Max Bone Matrix Texture Height
Altura máxima de la textura de matriz de huesos. Solo se usa el tamaño necesario para animaciones, redondeado hacia arriba a la potencia de dos más cercana.

#### Max Morph Target Texture Width
`model.max_morph_target_texture_width` define el ancho máximo en píxeles de la textura generada por mesh para las variaciones de posición, normal y tangente de los morph targets. El valor predeterminado es `1024`.

#### Max Morph Target Texture Height
`model.max_morph_target_texture_height` define la altura máxima en píxeles de la textura generada por mesh para las variaciones de posición, normal y tangente de los morph targets. El valor predeterminado es `1024`.

---

### Light

#### Max Count {#light-max-count}
`light.max_count` define el número máximo de componentes de luz, `64` de forma predeterminada. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### GUI

#### Max Count
Número máximo de componentes GUI. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Max Particle Count
El número máximo de partículas concurrentes en GUI.

#### Max Particlefx Count
`gui.max_particlefx_count` define el número máximo de nodos de efectos de partículas por colección. El valor predeterminado es `64`.

#### Max Animation Count
El número máximo de animaciones activas en GUI.

#### Safe Area Mode
`gui.safe_area_mode` selecciona qué márgenes del área segura afectan al ajuste de la GUI:

- `none` (predeterminado): Ignora los márgenes.
- `long`: Aplica los márgenes izquierdo y derecho en orientación horizontal, y los márgenes superior e inferior en orientación vertical.
- `short`: Aplica los márgenes superior e inferior en orientación horizontal, y los márgenes izquierdo y derecho en orientación vertical.
- `both`: Aplica los cuatro márgenes.

Un script GUI puede sobrescribir el modo de su escena con [`gui.set_safe_area_mode()`](/ref/gui/#gui.set_safe_area_mode). Consulta la [guía sobre el área segura](/manuals/porting-guidelines/#mobile-phones-and-notch-and-hole-punch-cameras) para conocer la compatibilidad de las plataformas y cómo crear diseños personalizados.

---

### Label

#### Max Count
Número máximo de labels. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Subpixels
Marca esta opción para permitir que los labels aparezcan desalineados con respecto a los pixeles.

---

### Particle FX

#### Max Count
`particle_fx.max_count` define el número máximo de componentes de efectos de partículas, `64` de forma predeterminada. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

#### Max Emitter Count
`particle_fx.max_emitter_count` define el número máximo de emisores de efectos de partículas concurrentes. El valor predeterminado es `64`.

#### Max Particle Count
El número máximo de partículas concurrentes. Limita el tamaño del buffer de vértices de la GPU, `1024` partículas de forma predeterminada.

#### Max Particle Buffer Count
`particle_fx.max_particle_buffer_count` define el número máximo de partículas por transferencia a la GPU. Limita el buffer de la CPU usado para generar los vértices de las partículas. El valor predeterminado es `1024`.

---

### Box2D

#### Velocity Iterations
Número de iteraciones de velocidad para el solver de físicas Box2D 2.2.

#### Position Iterations
Número de iteraciones de posición para el solver de físicas Box2D 2.2.

#### Sub Step Count
Número de subpasos para el solver de físicas Box2D 3.x.

---

### Collection proxy

#### Max Count
Número máximo de proxies de colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### Collection factory

#### Max Count
Número máximo de factories de colección. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### Factory

#### Max Count
Número máximo de factories de objetos de juego. [(Consulta la información sobre optimizaciones del conteo máximo de componentes)](#component-max-count-optimizations).

---

### iOS

#### Home Indicator Mode
`ios.home_indicator_mode` controla los gestos del sistema en los bordes de la pantalla y si el juego solicita que el indicador de inicio se oculte automáticamente.

| Valor | Gestos del sistema | Solicitar ocultación automática |
|-------|-----------------|--------------------------|
| `deferred` (predeterminado) | Protege todos los bordes de la pantalla aplazando los gestos del sistema. Volver al inicio requiere dos deslizamientos. | No |
| `system` | Usa los gestos normales del sistema y permite volver al inicio con un solo deslizamiento. | No |
| `auto_hide` | Usa los gestos normales del sistema y permite volver al inicio con un solo deslizamiento. | Sí |

iOS controla la visibilidad real del indicador. La ocultación automática es una solicitud, y en iOS 26 y versiones posteriores el sistema puede ocultarlo tanto en modo `system` como `auto_hide`. Consulta [Comportamiento del indicador de inicio](/manuals/ios/#home-indicator-behavior) para ver un ejemplo de configuración.

#### App Icon 57x57--180x180
Archivo de imagen (.png) para usar como icono de la aplicación en las dimensiones de ancho y alto dadas `W` &times; `H`.

#### Launch Screen
Archivo storyboard (.storyboard). Aprende más sobre cómo crear uno en el [manual de iOS](/manuals/ios/#creating-a-storyboard).

#### Icons Asset
El archivo de asset de iconos (.car) que contiene iconos de la app.

#### Prerendered Icons
(iOS 6 y anteriores) Marca esta opción si tus iconos están prerenderizados. Si está desmarcada, se agregará automáticamente un brillo a los iconos.

#### Bundle Identifier
El identificador de bundle permite que iOS reconozca cualquier actualización de tu app. Tu bundle ID debe estar registrado con Apple y ser único para tu app. No puedes usar el mismo identificador para apps de iOS y macOS. Debe constar de dos o más segmentos separados por un punto. Cada segmento debe empezar con una letra. Cada segmento debe contener solo letras alfanuméricas, el guion bajo o el carácter de guion (-) (consulta [`CFBundleIdentifier`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Bundle Name
El nombre corto del bundle (15 caracteres) (consulta [`CFBundleName`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)).

#### Bundle Version
La versión del bundle, ya sea un número o x.y.z. (consulta [`CFBundleVersion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430))

#### Info.plist
Si se especifica, usa este archivo *`Info.plist`* en lugar del manifiesto base integrado de iOS, `/builtins/manifests/ios/Info.plist`, al crear el bundle de tu aplicación. Los proyectos que usan la plantilla integrada reciben las actualizaciones del manifiesto automáticamente; los archivos personalizados deben actualizarse explícitamente.

#### Privacy Manifest
El Apple Privacy Manifest para la aplicación. El campo tendrá como valor predeterminado `/builtins/manifests/ios/PrivacyInfo.xcprivacy`.

#### Custom Entitlements
Si se especifica, los entitlements del perfil provisional suministrado (`.entitlements`, `.xcent`, `.plist`) se fusionarán con los entitlements del perfil provisional suministrado al crear el bundle de la aplicación.

#### Default Language
El idioma usado si la aplicación no tiene el idioma preferido del usuario en la lista `Localizations` (consulta [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Usa el estándar ISO 639-1 de dos letras si el idioma preferido está disponible allí, o ISO 639-2 de tres letras.

#### Localizations
Este campo contiene strings separados por comas que identifican el nombre del idioma o el designador de idioma ISO de las localizaciones soportadas (consulta [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Android

#### App Icon 36x36--192x192
Archivo de imagen (.png) para usar como icono de la aplicación en las dimensiones de ancho y alto dadas `W` &times; `H`.

#### Push Icon Small--LargeXxxhdpi
Archivos de imagen (.png) para usar como icono personalizado de notificaciones push en Android. Los iconos se usarán automáticamente tanto para notificaciones push locales como remotas. Si no se define, se usará el icono de la aplicación de forma predeterminada.

#### Push Field Title
Especifica qué campo JSON del payload debe usarse como título de la notificación. Dejar esta configuración vacía hace que las notificaciones push usen de forma predeterminada el nombre de la aplicación como título.

#### Push Field Text
Especifica qué campo JSON del payload debe usarse como texto de la notificación. Si se deja vacío, se usa el texto del campo `alert`, igual que en iOS.

#### Version Code
Un valor entero que indica la versión de la app. Aumenta el valor para cada actualización posterior.

#### Minimum SDK Version
El API Level mínimo requerido para que la aplicación se ejecute (`android:minSdkVersion`).

#### Target SDK Version
El API Level al que apunta la aplicación (`android:targetSdkVersion`).

#### Package
Identificador de paquete. Debe constar de dos o más segmentos separados por un punto. Cada segmento debe empezar con una letra. Cada segmento debe contener solo letras alfanuméricas o el carácter de guion bajo.

#### GCM Sender Id
Google Cloud Messaging Sender Id. Define esto con el string asignado por Google para activar notificaciones push.

#### FCM Application Id
Firebase Cloud Messaging Application Id.

#### Manifest
Si se define, usa el archivo XML de manifiesto de Android especificado al crear el bundle. Un manifiesto personalizado sustituye el manifiesto base integrado de Defold. Los fragmentos de manifiesto de extensiones nativas todavía se fusionan con él, pero los cambios posteriores del manifiesto base integrado no se heredan automáticamente, por lo que debes comparar los manifiestos personalizados con el manifiesto integrado actual al actualizar. En los juegos, define `android:appCategory="game"` en el elemento `<application>`. En aplicaciones que no sean juegos, define `android:appCategory` solo si una de las [categorías de aplicación](https://developer.android.com/guide/topics/manifest/application-element#appCategory) definidas por Android describe la aplicación con precisión.

#### Iap Provider
Especifica qué tienda usar. Las opciones válidas son `Amazon` y `GooglePlay`. Consulta [extension-iap](/extension-iap/) para obtener más información.

#### Input Method
Especifica qué método usar para obtener input de teclado en dispositivos Android. Las opciones válidas son `KeyEvent` (método antiguo) y `HiddenInputField` (nuevo).

#### Immersive Mode
Si se define, oculta las barras de navegación y estado y permite que tu app capture todos los eventos táctiles en la pantalla.

#### Display Cutout
Extiende la aplicación al display cutout.

#### Debuggable
Indica si la aplicación se puede depurar usando herramientas como [GAPID](https://github.com/google/gapid) o [Android Studio](https://developer.android.com/studio/profile/android-profiler). Esto definirá el flag `android:debuggable` en el manifiesto de Android ([documentación oficial](https://developer.android.com/guide/topics/manifest/application-element#debug)).

<a id="proguard-config"></a>

#### R8 Keep Rules
`android.r8_keep_rules` selecciona un archivo `.keep` para activar la eliminación de código no usado, la optimización y la ofuscación de código Java con R8 en builds de Android. Deja la configuración vacía para usar D8 sin eliminar código.

Con un servidor de build Extender compatible, también elimina recursos Android no usados. Los recursos cargados dinámicamente pueden necesitar [reglas XML de conservación](/manuals/android/#keeping-android-resources) independientes.

Selecciona `/builtins/manifests/android/dmengine.keep` para usar directamente las reglas predeterminadas de Defold. Las extensiones proporcionan sus propias [reglas de conservación](/manuals/extensions/#r8-keep-rules-for-android), que se combinan con este archivo.

Copia el archivo integrado a tu proyecto solo si necesitas agregar reglas específicas del proyecto. Conserva las reglas integradas en la copia: seleccionar un archivo personalizado reemplaza el conjunto completo de reglas del proyecto.

Consulta el [manual de Android](/manuals/android/#shrinking-java-code-with-r8) para activar R8 y conservar su mapa de ofuscación junto a un bundle de release.

#### Extract Native Libraries
Especifica si el instalador del paquete extrae bibliotecas nativas del APK al sistema de archivos. Si se define como `false`, tus bibliotecas nativas se almacenan sin comprimir en el APK. Aunque tu APK puede ser más grande, tu aplicación carga más rápido porque las bibliotecas se cargan directamente desde el APK en runtime. Esto definirá el flag `android:extractNativeLibs` en el manifiesto de Android ([documentación oficial](https://developer.android.com/guide/topics/manifest/application-element#extractNativeLibs)).

---

### macOS

#### App Icon
Archivo de icono de bundle (.icns) para usar como icono de la aplicación en macOS.

#### Info.plist
Si se define, usa el archivo info.plist especificado al crear el bundle.

#### Privacy Manifest
El Apple Privacy Manifest para la aplicación. El campo tendrá como valor predeterminado `/builtins/manifests/osx/PrivacyInfo.xcprivacy`.

#### Bundle Identifier
El identificador de bundle permite que macOS reconozca actualizaciones de tu app. Tu bundle ID debe estar registrado con Apple y ser único para tu app. No puedes usar el mismo identificador para apps de iOS y macOS. Debe constar de dos o más segmentos separados por un punto. Cada segmento debe empezar con una letra. Cada segmento debe contener solo letras alfanuméricas, el guion bajo o el carácter de guion (-).

#### Bundle Name {#osx-bundle-name}
`osx.bundle_name` especifica el nombre corto del bundle (`CFBundleName`), limitado a 15 caracteres.

#### Bundle Version {#osx-bundle-version}
`osx.bundle_version` especifica el número de build (`CFBundleVersion`), ya sea un número o `x.y.z`. El valor predeterminado es `1`.

#### Default Language
El idioma usado si la aplicación no tiene el idioma preferido del usuario en la lista `Localizations` (consulta [`CFBundleDevelopmentRegion`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-130430)). Usa el estándar ISO 639-1 de dos letras si el idioma preferido está disponible allí, o ISO 639-2 de tres letras.

#### Localizations
Este campo contiene strings separados por comas que identifican el nombre del idioma o el designador de idioma ISO de las localizaciones soportadas (consulta [`CFBundleLocalizations`](https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html#//apple_ref/doc/uid/20001431-109552)).

---

### Windows

#### App Icon
Archivo de imagen (.ico) para usar como icono de la aplicación en Windows. Lee más sobre cómo crear un archivo .ico en el [manual de Windows](/manuals/windows).

---

### HTML5

Consulta el [manual de la plataforma HTML5](/manuals/html5/) para obtener más información sobre muchas de estas opciones.

#### Heap Size
Tamaño del heap en megabytes para que lo use Emscripten.

#### .html Shell
Usa el archivo HTML de plantilla especificado al crear el bundle. De forma predeterminada, `/builtins/manifests/web/engine_template.html`.

#### Custom .css
Usa el archivo CSS de tema especificado al crear el bundle. De forma predeterminada, `/builtins/manifests/web/light_theme.css`.

#### Splash Image
Si se define, usa la imagen de splash especificada al iniciar al crear el bundle, en lugar del logo de Defold.

#### Archive Location Prefix
Al crear un bundle para HTML5, los datos del juego se dividen en uno o más archivos de datos. Cuando el motor inicia el juego, estos archivos se leen en memoria. Usa esta configuración para especificar la ubicación de los datos.

#### Archive Location Suffix
Sufijo que se agregará a los archivos de datos. Útil, por ejemplo, para forzar contenido no cacheado desde un CDN (`?version2`, por ejemplo).

#### Engine Arguments
Lista de argumentos que se pasarán al motor.

#### Wasm Streaming
Activa streaming del archivo wasm (más rápido y usa menos memoria, pero requiere el tipo MIME `application/wasm`).

#### Show Fullscreen Button
Activa Fullscreen Button en el archivo `index.html`.

#### Show Made With Defold
Activa el enlace Made With Defold en el archivo `index.html`.

#### Show Console Banner
Cuando está activada, esta opción imprimirá información sobre el motor y la versión del motor en la consola del navegador (usando `console.log()`) cuando el motor arranque.

#### Scale Mode
Especifica qué método usar para escalar el canvas del juego.

#### Min Pixel Ratio
`html5.min_pixel_ratio` establece el número mínimo de píxeles de renderizado del canvas por píxel CSS cuando [High Dpi](#high-dpi) está activado. El valor predeterminado es `0`, que desactiva el límite inferior. Se admiten valores fraccionarios positivos, incluidos los inferiores a `1`.

#### Max Pixel Ratio
`html5.max_pixel_ratio` establece el número máximo de píxeles de renderizado del canvas por píxel CSS cuando [High Dpi](#high-dpi) está activado. El valor predeterminado es `0`, que desactiva el límite superior. Se admiten valores fraccionarios positivos, incluidos los inferiores a `1`.

Ambos límites deben ser números finitos y no negativos. Cuando ambos están activados, el mínimo no debe superar al máximo. Con *High Dpi* desactivado, la relación es `1` y no se aplica ningún límite. Estos límites afectan a la resolución de renderizado sin cambiar el tamaño de visualización CSS del canvas. Consulta [Límites de la relación de píxeles](/manuals/html5/#pixel-ratio-limits) para ver un ejemplo de configuración.

#### Retry Count
El número de reintentos después de una descarga fallida durante el inicio, incluidos errores de red, estados HTTP fallidos y discrepancias de tamaño en el archivo JavaScript o WebAssembly del motor. La solicitud inicial se cuenta por separado. La verificación de archivos del juego tiene su propio límite de reintentos; consulta [verificación de descargas](/manuals/html5/#download-verification) y `Retry Time`.

#### Retry Time
El número de segundos que esperar entre intentos de descargar un archivo cuando la descarga falló (consulta `Retry Count`).

#### Verify Downloaded File Size
`html5.verify_downloaded_file_size` compara los archivos descargados del motor y del archivo del juego con sus tamaños esperados. Está activado de forma predeterminada (`true`). Defínelo como `false` solo si un servidor, proxy o CDN modifica intencionalmente los archivos y cambia sus tamaños. La verificación fallida provoca reintentos de descarga antes de que falle el inicio. Los límites de reintentos son distintos para las descargas del motor y la verificación de archivos del juego; consulta [verificación de descargas](/manuals/html5/#download-verification).

#### Transparent Graphics Context
Marca esta opción si quieres que el contexto gráfico tenga un fondo transparente.

---

### IAP

#### Auto Finish Transactions
Marca esta opción para finalizar automáticamente las transacciones IAP. Si está desmarcada, debes llamar explícitamente a `iap.finish()` después de una transacción exitosa.

---

### Live update

#### Enabled {#liveupdate-enabled}
`liveupdate.enabled` activa el sistema Live update en runtime. Activado de forma predeterminada. Consulta el [manual de Live update](/manuals/live-update/) para saber cómo excluir, descargar y montar recursos.

#### Settings
Archivo de recurso de configuración de Live Update para usar durante la creación de bundles.

---

### Native extension

#### _App Manifest_
Si se define, usa el manifiesto de la aplicación para personalizar la build del motor. Esto te permite eliminar partes no usadas del motor para reducir el tamaño binario final. Aprende cómo excluir funcionalidades no usadas [en el manual del manifiesto de aplicación](/manuals/app-manifest).

---

### Debugger

Estos ajustes controlan las [conexiones del depurador](/manuals/debugging-game-logic/#native-dap-connections) en builds nativas de depuración y headless. Las builds release y web no permiten adjuntarlo. Agrega estos ajustes editando *game.project* como texto o usa [valores de configuración al iniciar el motor](#setting-config-values-on-engine-startup). No se muestran en el formulario de configuración del proyecto. El editor configura la conexión automáticamente cuando usas <kbd>Debug ▸ Start/Attach</kbd>.

Por ejemplo, para iniciar un listener local y esperar a que un cliente configure los breakpoints antes de ejecutar los scripts de inicio:

```ini
[debugger]
enabled = 1
address = 127.0.0.1
port = 8172
wait = 1
```

#### Enabled {#debugger-enabled}
`debugger.enabled` inicia el listener al arrancar el motor cuando vale `1`. Está desactivado de forma predeterminada (`0`). Un juego en ejecución también puede iniciar el listener con [`debugger.start()`](/manuals/debugging-game-logic/#enabling-the-listener-while-running).

#### Address {#debugger-address}
`debugger.address` es la dirección IPv4 en la que el listener acepta conexiones. El valor predeterminado, `127.0.0.1`, solo acepta conexiones locales. Usa una dirección de interfaz del dispositivo o `0.0.0.0` para [conexiones remotas](/manuals/debugging-game-logic/#remote-targets).

#### Port {#debugger-port}
`debugger.port` es el puerto TCP de escucha, entre `0` y `65535`. El valor predeterminado es `8172`. Establécelo en `0` para seleccionar un puerto disponible, que el motor indicará en su log.

#### Wait {#debugger-wait}
`debugger.wait` hace que el motor espere a que el cliente termine de configurar la sesión de depuración, incluidos los breakpoints, antes de ejecutar los scripts de inicio. Está desactivado de forma predeterminada (`0`). Establécelo en `1` junto con `debugger.enabled=1` para depurar código de inicio. Iniciar el listener más adelante con `debugger.start()` no espera ni pausa el juego. Consulta la [guía de inicio y conexión](/manuals/debugging-game-logic/#native-dap-connections).

---

### Profiler

El ajuste **Profiler** del manifiesto de la aplicación controla si el código del profiler se enlaza con las builds debug y release. Los ajustes siguientes controlan el comportamiento en runtime del código del profiler presente en la build seleccionada. Consulta el [manual de profiling](/manuals/profiling/) para más detalles.

#### Enabled
Activa el profiler dentro del juego.

#### Track Cpu
El muestreo de uso de CPU está activado de forma predeterminada en builds debug. Activa este ajuste cuando también necesites muestreo de CPU en una build release que incluya soporte para el profiler mediante el manifiesto de la aplicación.

#### Track Detailed Memory
`profiler.track_detailed_memory` activa el muestreo detallado de memoria en el profiler. Desactivado de forma predeterminada. Puede tener un costo elevado en HTML5.

#### Sleep Between Server Updates
Número de milisegundos que dormir entre actualizaciones del servidor.

#### Performance Timeline Enabled
Activa la línea de tiempo de rendimiento en el navegador (solo HTML5).

#### Max Sample Count
`profiler.max_sample_count` es el número máximo de muestras del profiler registradas por thread y por frame. El valor predeterminado es `4096` y el mínimo es `128`. Auméntalo solo cuando un profile legítimo supere el límite; comprueba primero si el código de profiling de las extensiones nativas tiene llamadas de inicio/fin de scope sin correspondencia.

---

## Definir valores de configuración al iniciar el motor {#setting-config-values-on-engine-startup}

Cuando el motor arranca, es posible proporcionar valores de configuración desde la línea de comando que sobrescriben la configuración de *game.project*:

```bash
# Specify a bootstrap collection
$ dmengine --config=bootstrap.main_collection=/my.collectionc

# Set two custom config values
$ dmengine --config=test.my_value=4711 --config=test2.my_value2=foobar
```

Los valores personalizados pueden, igual que cualquier otro valor de configuración, leerse con la función correspondiente descrita en [Acceso en runtime](#runtime-access):

```lua
local my_value = sys.get_config_number("test.my_value")
local my_value2 = sys.get_config_string("test.my_value2")
local my_flag = sys.get_config_boolean("test.my_flag", false)
```


:[Component max count optimizations](../shared/component-max-count-optimizations.md)


## Configuración personalizada del proyecto {#custom-project-settings}

Es posible definir configuraciones personalizadas para el proyecto principal o para una [extensión nativa](/manuals/extensions/). Las configuraciones personalizadas para el proyecto principal deben definirse en un archivo `game.properties` en la raíz del proyecto. Los archivos llamados `ext.properties` se detectan en cualquier lugar del proyecto y en las dependencias de bibliotecas obtenidas; no necesitan un `ext.manifest` vecino. Primero se combinan todos los metadatos de extensiones detectados y después se aplica el archivo `game.properties` de la raíz, que puede sobrescribirlos.

El archivo de configuración usa el mismo formato INI que *game.project*, y los atributos de propiedad se definen usando una notación con puntos y un sufijo:

```
[my_category]
my_property.private = 1
...
```

El archivo meta predeterminado que siempre se aplica está disponible [aquí](https://github.com/defold/defold/blob/dev/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/meta.properties)

Los siguientes atributos están disponibles actualmente:

```
[my_extension]
// `type` - used for the value string parsing
my_property.type = string // one of the following values: bool, string, number, integer, string_array, resource

// `help` - displayed as a help tooltip in the editor
my_property.help = string

// `default` - value used as default if user didn't set value manually
my_property.default = string

// `private` - private value used during the bundle process but will be removed from the bundle itself
my_property.private = 1 // boolean value 1 or 0

// `label` - editor input label
my_property.label = My Awesome Property

// `minimum` and/or `maximum` - valid range for numeric properties, validated in the editor UI
my_property.minimum = 0
my_property.maximum = 255

// `options` - drop-down choices for the editor UI, comma-separated value[:label] pairs
my_property.options = android: Android, ios: iOS

// `resource` type only:
my_property.filter = jpg,png // allowed file extensions for resource selector dialog
my_property.preserve-extension = 1 // use original resource extension instead of a built one

// deprecation
my_property.deprecated = 1 // mark property as deprecated
my_property.severity-default = warning // if deprecated property is specified, but set to a default value
my_property.severity-override = error  // if deprecated property is specified and set to a non-default value

```
Además, puedes definir los siguientes atributos en una categoría de configuración:
```
[my_extension]
// `group` - game.project category group, e.g. Main, Platforms, Components, Runtime, Distribution
group = Runtime
// `title` - displayed category title
title = My Awesome Extension
// `help` - displayed category help
help = Settings for My Awesome Extension
```


Tanto Bob como el editor analizan estos archivos de metadatos. El editor los usa para crear los campos, opciones, validaciones y tooltips de ayuda correspondientes en el visor de *game.project*.
