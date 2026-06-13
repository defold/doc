---
title: Desarrollo Defold para la plataforma HTML5
brief: Este manual describe el proceso de creación de un juego HTML5, junto con problemas y limitaciones conocidos.
---

# Desarrollo HTML5

Defold permite crear builds de juegos para la plataforma HTML5 mediante el menú de bundling habitual, igual que para otras plataformas. Además, el juego resultante se incrusta en una página HTML normal que se puede estilizar mediante un sistema sencillo de plantillas.

El archivo *game.project* contiene la configuración específica de HTML5:

![Configuración del proyecto](images/html5/html5_project_settings.png)

## Tamaño del heap

El soporte de Defold para HTML5 se basa en Emscripten (consulta http://en.wikipedia.org/wiki/Emscripten). En resumen, crea un sandbox de memoria para el heap en el que opera la aplicación. Por defecto, el motor asigna una cantidad generosa de memoria (256 MB). Esto debería ser más que suficiente para un juego típico. Como parte de tu proceso de optimización, puedes elegir usar un valor menor. Para hacerlo, sigue estos pasos:

1. Define *heap_size* con el valor que prefieras. Debe expresarse en megabytes.
2. Crea tu bundle HTML5 (consulta más abajo).

## Probar una build HTML5

Para probarla, una build HTML5 necesita un servidor HTTP. Defold crea uno por ti si eliges <kbd>Project ▸ Build HTML5</kbd>.

![Build HTML5](images/html5/html5_build_launch.png)

Si quieres probar tu bundle, súbelo a tu servidor HTTP remoto o crea un servidor local, por ejemplo, usando python en la carpeta del bundle.
Python 2:

```sh
python -m SimpleHTTPServer
```

Python 3:

```sh
python -m http.server
```

o

```sh
python3 -m http.server
```

::: important
No puedes probar el bundle HTML5 abriendo el archivo `index.html` en un navegador. Esto requiere un servidor HTTP.
:::

::: important
Si ves un error `"wasm streaming compile failed: TypeError: Failed to execute ‘compile’ on ‘WebAssembly’: Incorrect response MIME type. Expected ‘application/wasm’."` en la consola, debes asegurarte de que tu servidor use el tipo MIME `application/wasm` para los archivos `.wasm`.
:::

## Crear un bundle HTML5

Crear contenido HTML5 con Defold es sencillo y sigue el mismo patrón que todas las demás plataformas soportadas: selecciona <kbd>Project ▸ Bundle... ▸ HTML5 Application...</kbd> en el menú:

![Crear bundle HTML5](images/html5/html5_bundle.png)

Puedes elegir incluir una versión `asm.js` y una versión WebAssembly (wasm) del motor Defold en el bundle HTML5. En la mayoría de los casos basta con elegir WebAssembly, ya que [todos los navegadores modernos soportan WebAssembly](https://caniuse.com/wasm).

::: important
Aunque incluyas las versiones `asm.js` y `wasm` del motor, el navegador descargará solo una de ellas al iniciar el juego. La versión WebAssembly se descargará si el navegador soporta WebAssembly, y la versión `asm.js` se usará como fallback en el caso poco frecuente de que WebAssembly no sea soportado.
:::

Cuando hagas click en el botón <kbd>Create bundle</kbd>, se te pedirá que selecciones una carpeta en la que crear tu aplicación. Cuando el proceso de exportación termine, encontrarás todos los archivos necesarios para ejecutar la aplicación.

## Problemas conocidos y limitaciones

* Hot Reload - Hot Reload no funciona en builds HTML5. Las aplicaciones Defold deben ejecutar su propio servidor web en miniatura para recibir actualizaciones desde el editor, lo que no es posible en una build HTML5.
* Internet Explorer 11
  * Audio - Defold maneja la reproducción de audio usando _WebAudio_ de HTML5 (consulta http://www.w3.org/TR/webaudio), que actualmente no es soportado por Internet Explorer 11. Las aplicaciones usarán como fallback una implementación de audio nula al usar este navegador.
  * WebGL - Microsoft no ha terminado el trabajo de implementación de la API _WebGL_ (consulta https://www.khronos.org/registry/webgl/specs/latest/). Por lo tanto, no rinde tan bien como otros navegadores.
  * Full screen - El modo de pantalla completa no es fiable en el navegador.
* Chrome
  * Builds debug lentas - En builds debug de HTML5 verificamos todas las llamadas gráficas de WebGL para detectar errores. Lamentablemente, esto es muy lento al probar en Chrome. Es posible desactivarlo definiendo el campo *Engine Arguments* de *game.project* como `--verify-graphics-calls=false`.
* Soporte para gamepad - [Consulta la documentación de Gamepad](/manuals/input-gamepads/#gamepads-in-html5) para conocer consideraciones especiales y pasos que quizá debas seguir en HTML5.

## Personalizar el bundle HTML5

Cuando generas una versión HTML5 de tu juego, Defold proporciona una página web por defecto. Esta hace referencia a recursos de estilo y script que determinan cómo se presenta tu juego.

Cada vez que se exporta la aplicación, este contenido se crea de nuevo. Si quieres personalizar cualquiera de estos elementos, debes hacer modificaciones en la configuración de tu proyecto. Para hacerlo, abre *game.project* en el editor Defold y desplázate hasta la sección *html5*:

![Sección HTML5](images/html5/html5_section.png)

Hay más información sobre cada opción disponible en el [manual de configuración del proyecto](/manuals/project-settings/#html5).

::: important
No puedes modificar los archivos de la plantilla html/css por defecto en la carpeta `builtins`. Para aplicar tus modificaciones, copia/pega el archivo necesario desde `builtins` y define este archivo en *game.project*.
:::

::: important
El canvas no debería estilizarse con ningún borde ni padding. Si lo haces, las coordenadas de input del mouse serán incorrectas.
:::

En *game.project* es posible desactivar el botón `Fullscreen` y el enlace `Made with Defold`.
Defold proporciona un tema oscuro y uno claro para `index.html`. El tema claro está definido por defecto, pero es posible cambiarlo cambiando el archivo `Custom CSS`. También hay cuatro modos de escala predefinidos para elegir en el campo `Scale Mode`.

::: important
Los cálculos de todos los modos de escala incluyen el DPI actual de la pantalla si activas la opción `High Dpi` en *game.project* (sección `Display`).
:::

### Downscale Fit y Fit

En el modo `Fit`, el tamaño del canvas se cambiará para mostrar todo el canvas del juego en la pantalla con las proporciones originales. La única diferencia en `Downscale Fit` es que cambia el tamaño solo si el tamaño interno de la página web es menor que el canvas original del juego, pero no escala hacia arriba cuando una página web es mayor que el canvas original del juego.

![Sección HTML5](images/html5/html5_fit.png)

### Stretch

En el modo `Stretch`, el tamaño del canvas se cambiará para llenar por completo el tamaño interno de la página web.

![Sección HTML5](images/html5/html5_stretch.png)

### No Scale

Con el modo `No Scale`, el tamaño del canvas es exactamente el mismo que predefiniste en el archivo *game.project*, sección `[display]`.

![Sección HTML5](images/html5/html5_no_scale.png)

## Tokens

Usamos el [lenguaje de plantillas Mustache](https://mustache.github.io/mustache.5.html) para crear el archivo `index.html`. Cuando haces una build o un bundle, los archivos HTML y CSS pasan por un compilador que puede reemplazar ciertos tokens por valores que dependen de la configuración de tu proyecto. Estos tokens siempre están encerrados entre llaves dobles o triples (`{{TOKEN}}` o `{{{TOKEN}}}`), dependiendo de si las secuencias de caracteres deben escaparse o no. Esta funcionalidad puede ser útil si haces cambios frecuentes en la configuración de tu proyecto o si tienes intención de reutilizar el material en otros proyectos.

::: sidenote
Hay más información sobre el lenguaje de plantillas Mustache disponible en el [manual](https://mustache.github.io/mustache.5.html).
:::

Cualquier valor de *game.project* puede ser un token. Por ejemplo, si quieres usar el valor `Width` de la sección `Display`:

![Sección Display](images/html5/html5_display.png)

Abre *game.project* como texto y revisa `[section_name]` y el nombre del campo que quieres usar. Luego puedes usarlo como token: `{{section_name.field}}` o `{{{section_name.field}}}`.

![Sección Display](images/html5/html5_game_project.png)

Por ejemplo, en la plantilla HTML en JavaScript:

```javascript
function doSomething() {
    var x = {{display.width}};
    // ...
}
```

También tenemos los siguientes tokens personalizados:

DEFOLD_SPLASH_IMAGE
: Escribe el nombre de archivo de la imagen splash o `false` si `html5.splash_image` en *game.project* está vacío.


```css
{{#DEFOLD_SPLASH_IMAGE}}
		background-image: url("{{DEFOLD_SPLASH_IMAGE}}");
{{/DEFOLD_SPLASH_IMAGE}}
```

exe-name
: El nombre del proyecto sin símbolos no aceptados.


DEFOLD_CUSTOM_CSS_INLINE
: Este es el lugar donde insertamos en línea el archivo CSS especificado en la configuración de *game.project*.


```html
<style>
{{{DEFOLD_CUSTOM_CSS_INLINE}}}
</style>
```

::: important
Es importante que este bloque en línea aparezca antes de que se cargue el script principal de la aplicación. Como incluye etiquetas HTML, esta macro debe aparecer entre llaves triples `{{{TOKEN}}}` para evitar que las secuencias de caracteres se escapen.
:::

DEFOLD_SCALE_MODE_IS_DOWNSCALE_FIT
: Este token es `true` si `html5.scale_mode` es `Downscale Fit`.

DEFOLD_SCALE_MODE_IS_FIT
: Este token es `true` si `html5.scale_mode` es `Fit`.

DEFOLD_SCALE_MODE_IS_NO_SCALE
: Este token es `true` si `html5.scale_mode` es `No Scale`.

DEFOLD_SCALE_MODE_IS_STRETCH
: Este token es `true` si `html5.scale_mode` es `Stretch`.

DEFOLD_HEAP_SIZE
: Tamaño del heap especificado en `html5.heap_size` de *game.project*, convertido a bytes.

DEFOLD_ENGINE_ARGUMENTS
: Argumentos del motor especificados en `html5.engine_arguments` de *game.project*, separados por el símbolo `,`.

build-timestamp
: Marca de tiempo de la build actual en segundos.


## Parámetros extra

Si creas tu plantilla personalizada, puedes redefinir el conjunto de parámetros para el cargador del motor. Para lograrlo, debes agregar una sección `<script>` y redefinir los valores dentro de `CUSTOM_PARAMETERS`.
::: important
Tu `<script>` personalizado debe colocarse después de la sección `<script>` con la referencia a `dmloader.js`, pero antes de la llamada a la función `EngineLoader.load`.
:::
Por ejemplo:

```
    <script id='custom_setup' type='text/javascript'>
        CUSTOM_PARAMETERS['disable_context_menu'] = false;
        CUSTOM_PARAMETERS['unsupported_webgl_callback'] = function() {
            console.log("Oh-oh. WebGL not supported...");
        }
    </script>
```

`CUSTOM_PARAMETERS` puede contener los siguientes campos:

```
'archive_location_filter':
    Filter function that will run for each archive path.

'unsupported_webgl_callback':
    Function that is called if WebGL is not supported.

'engine_arguments':
    List of arguments (strings) that will be passed to the engine.

'custom_heap_size':
    Number of bytes specifying the memory heap size.

'disable_context_menu':
    Disables the right-click context menu on the canvas element if true.

'retry_time':
    Pause in seconds before retry file loading after error.

'retry_count':
    How many attempts we do when trying to download a file.

'can_not_download_file_callback':
    Function that is called if you can't download file after 'retry_count' attempts.

'resize_window_callback':
    Function that is called when resize/orientationchanges/focus events happened

'start_success':
    Function that is called just before main is called upon successful load.

'update_progress':
    Function that is called as progress is updated. Parameter progress is updated 0-100.
```

## Operaciones de archivo en HTML5

Las builds HTML5 soportan operaciones de archivo como `sys.save()`, `sys.load()` e `io.open()`, pero la forma en que estas operaciones se manejan internamente es diferente a la de otras plataformas. Cuando JavaScript se ejecuta en un navegador, no existe un concepto real de sistema de archivos y el acceso a archivos locales está bloqueado por motivos de seguridad. En su lugar, Emscripten (y por lo tanto Defold) usa [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB), una base de datos dentro del navegador usada para almacenar datos de forma persistente, para crear un sistema de archivos virtual en el navegador. La diferencia importante con el acceso al sistema de archivos en otras plataformas es que puede haber un pequeño retraso entre escribir en un archivo y que el cambio se almacene realmente en la base de datos. La consola de desarrollador del navegador normalmente te permite inspeccionar el contenido de IndexedDB.


## Pasar argumentos a un juego HTML5

A veces es necesario proporcionar argumentos adicionales a un juego antes de que se inicie o mientras se inicia. Esto podría ser, por ejemplo, un id de usuario, un token de sesión o qué nivel cargar cuando el juego se inicia. Esto se puede lograr de varias formas distintas, algunas de las cuales se describen aquí.

### Argumentos del motor

Es posible especificar argumentos adicionales del motor cuando este se configura y se carga. Estos argumentos extra del motor se pueden recuperar en tiempo de ejecución usando `sys.get_config_string()`. Para agregar los pares clave-valor, modifica el campo `engine_arguments` del objeto `extra_params` que se pasa al motor cuando se carga en `index.html`:


```
    <script id='engine-setup' type='text/javascript'>
    var extra_params = {
        ...,
        engine_arguments: ["--config=foo1=bar1","--config=foo2=bar2"],
        ...
    }
```

También puedes agregar `--config=foo1=bar1, --config=foo2=bar2` al campo de argumentos del motor en la sección HTML5 de *game.project* y se inyectará en el archivo `index.html` generado.

En tiempo de ejecución obtienes los valores así:

```lua
local foo1 = sys.get_config_string("foo1")
local foo2 = sys.get_config_string("foo2")
print(foo1) -- bar1
print(foo2) -- bar2
```


### Argumentos de query en la URL

Puedes pasar argumentos como parte de los parámetros de query en la URL de la página y leerlos en tiempo de ejecución:

```
https://www.mygame.com/index.html?foo1=bar1&foo2=bar2
```

```lua
local url = html5.run("window.location")
print(url)
```

Una función auxiliar completa para obtener todos los parámetros de query como una tabla de Lua:

```lua
local function get_query_parameters()
    local url = html5.run("window.location")
    -- obtiene la parte de query de la url (lo que va después de ?)
    local query = url:match(".*?(.*)")
    if not query then
        return {}
    end

    local params = {}
    -- itera sobre todos los pares clave-valor
    for kvp in query:gmatch("([^&]+)") do
        local key, value = kvp:match("(.+)=(.+)")
        params[key] = value
    end
    return params
end

function init(self)
    local params = get_query_parameters()
    print(params.foo1) -- bar1
end
```

## Optimizaciones

Los juegos HTML5 suelen tener requisitos estrictos de tamaño de descarga inicial, tiempo de arranque y uso de memoria para asegurar que carguen rápido y funcionen bien en dispositivos de gama baja y conexiones lentas a internet. Para optimizar un juego HTML5, se recomienda centrarse en las siguientes áreas:

* [Uso de memoria](/manuals/optimization-memory)
* [Tamaño del motor](/manuals/optimization-size)
* [Tamaño del juego](/manuals/optimization-size)

## FAQ
:[HTML5 FAQ](../shared/html5-faq.md)
