---
title: Escribir extensiones nativas para Defold
brief: Este manual explica cómo escribir una extensión nativa para el motor de videojuegos Defold y cómo compilarla mediante los servidores de build en la nube sin configuración.
---

# Extensiones nativas

Si necesitas una interacción personalizada de bajo nivel con software o hardware externo donde Lua no sea suficiente, el SDK de Defold te permite escribir extensiones para el motor en C, C++, Objective C, Java o JavaScript, según la plataforma objetivo. Los casos de uso típicos para las extensiones nativas son:

- Interacción con hardware específico, por ejemplo la cámara de los teléfonos móviles.
- Interacción con API externas de bajo nivel, por ejemplo API de redes publicitarias que no permiten interacción mediante API de red donde podría usarse Luasocket.
- Cálculos de alto rendimiento y procesamiento de datos.

## El servidor de build

Defold proporciona un punto de entrada sin configuración para extensiones nativas con una solución de build basada en la nube. Cualquier extensión nativa que se desarrolle y se agregue a un proyecto de juego, ya sea directamente o mediante un [proyecto de biblioteca](/manuals/libraries/), pasa a formar parte del contenido ordinario del proyecto. No hay necesidad de crear versiones especiales del motor y distribuirlas a los miembros del equipo; eso se gestiona automáticamente: cualquier miembro del equipo que cree y ejecute el proyecto obtendrá un ejecutable del motor específico del proyecto con todas las extensiones nativas incluidas.

![Build en la nube](images/extensions/cloud_build.png)

Defold proporciona el servidor de build en la nube de forma gratuita, sin restricciones de uso. El servidor está alojado en Europa, y la URL a la que se envía el código nativo se configura en la [ventana Editor Preferences](/manuals/editor-preferences/#extensions) o mediante la opción de línea de comando `--build-server` de [bob](/manuals/bob/#usage). Si quieres configurar tu propio servidor, [sigue estas instrucciones](/manuals/extender-local-setup).

## Estructura del proyecto

Para crear una extensión nueva, crea una carpeta en la raíz del proyecto. Esta carpeta contendrá toda la configuración, el código fuente, las librerías y los recursos asociados con la extensión. El builder de extensiones reconoce la estructura de carpetas y recopila cualquier archivo fuente y librería.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: La carpeta de la extensión _debe_ contener un archivo *ext.manifest*. Este archivo es un archivo de configuración con flags y defines usados al crear la build de una extensión individual. La definición del formato de archivo se puede encontrar en el [manual de Extension Manifest](https://defold.com/manuals/extensions-ext-manifests/).

*src*
: Esta carpeta debe contener todos los archivos de código fuente.

*include*
: Esta carpeta opcional contiene cualquier archivo include.

*lib*
: Esta carpeta opcional contiene cualquier librería compilada de la que dependa la extensión. Los archivos de librería deben colocarse en subcarpetas nombradas por `platform` o `architecture-platform`, según las arquitecturas que soporten tus librerías.

  :[platforms](../shared/platforms.md)

*manifests*
: Esta carpeta opcional contiene archivos adicionales usados en el proceso de build o bundling. Consulta los detalles más abajo.

*res*
: Esta carpeta opcional contiene cualquier recurso extra del que dependa la extensión. Los archivos de recursos deben colocarse en subcarpetas nombradas por `platform` o `architecture-platform`, igual que las subcarpetas de "lib". También se permite una subcarpeta `common`, que contiene archivos de recursos comunes para todas las plataformas.

### Archivos de manifest

La carpeta opcional *manifests* de una extensión contiene archivos adicionales usados en el proceso de build y bundling. Los archivos deben colocarse en subcarpetas nombradas por `platform`:

* `android` - Esta carpeta acepta un archivo stub de manifest para fusionarlo con la aplicación principal ([como se describe aquí](/manuals/extensions-manifest-merge-tool)).
  * La carpeta también puede contener un archivo `build.gradle` con dependencias para ser [resueltas por Gradle](/manuals/extensions-gradle).
  * Por último, la carpeta también puede contener cero o más archivos ProGuard (experimental).
* `ios` - Esta carpeta acepta un archivo stub de manifest para fusionarlo con la aplicación principal ([como se describe aquí](/manuals/extensions-manifest-merge-tool)).
  * La carpeta también puede contener un archivo `Podfile` con dependencias para ser [resueltas por Cocoapods](/manuals/extensions-cocoapods).
* `osx` - Esta carpeta acepta un archivo stub de manifest para fusionarlo con la aplicación principal ([como se describe aquí](/manuals/extensions-manifest-merge-tool)).
* `web` - Esta carpeta acepta un archivo stub de manifest para fusionarlo con la aplicación principal ([como se describe aquí](/manuals/extensions-manifest-merge-tool)).


## Compartir una extensión

Las extensiones se tratan igual que cualquier otro asset en tu proyecto y se pueden compartir de la misma manera. Si una carpeta de extensión nativa se agrega como carpeta de Library, puede compartirse y otros pueden usarla como dependencia del proyecto. Consulta el [manual de proyectos de biblioteca](/manuals/libraries/) para obtener más información.


## Un ejemplo sencillo de extensión

Vamos a crear una extensión muy sencilla. Primero, creamos una nueva carpeta raíz *`myextension`* y agregamos un archivo *`ext.manifest`* que contiene el nombre de la extensión "`MyExtension`". Ten en cuenta que el nombre es un símbolo C++ y debe coincidir con el primer argumento de `DM_DECLARE_EXTENSION` (ver más abajo).

![Archivo manifest](images/extensions/manifest.png)

```yaml
# Símbolo C++ en tu extensión
name: "MyExtension"
```

La extensión consta de un único archivo C++, *`myextension.cpp`*, que se crea en la carpeta "`src`".

![Archivo C++](images/extensions/cppfile.png)

El archivo fuente de la extensión contiene el siguiente código:

```cpp
// myextension.cpp
// Defines de la librería de la extensión
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// Incluye el SDK de Defold
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // El número de elementos esperados en la pila de Lua
    // una vez que este struct salga del scope
    DM_LUA_STACK_CHECK(L, 1);

    // Comprueba y obtiene el parámetro string desde la pila
    char* str = (char*)luaL_checkstring(L, 1);

    // Invierte el string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Coloca el string invertido en la pila
    lua_pushstring(L, str);

    // Devuelve 1 elemento
    return 1;
}

// Funciones expuestas a Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Registra nombres Lua
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Inicializa Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// El SDK de Defold usa una macro para configurar los puntos de entrada de la extensión:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension es el símbolo C++ que contiene todos los datos relevantes de la extensión.
// Debe coincidir con el campo name en `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Observa la macro `DM_DECLARE_EXTENSION`, que se usa para declarar los distintos puntos de entrada al código de la extensión. El primer argumento, `symbol`, debe coincidir con el nombre especificado en *ext.manifest*. Para este ejemplo sencillo, no hay necesidad de puntos de entrada "update" ni "on_event", por lo que se proporciona `0` en esas posiciones de la macro.

Ahora solo queda crear la build del proyecto (<kbd>Project ▸ Build</kbd>). Esto subirá la extensión al builder de extensiones, que producirá un motor personalizado con la nueva extensión incluida. Si el builder encuentra errores, se mostrará un diálogo con los errores de build.

Para probar la extensión, crea un objeto de juego y agrega un componente script con algo de código de prueba:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

Eso es todo. Hemos creado una extensión nativa completamente funcional.


## Ciclo de vida de la extensión

Como vimos más arriba, la macro `DM_DECLARE_EXTENSION` se usa para declarar los distintos puntos de entrada al código de la extensión:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Los puntos de entrada te permiten ejecutar código en distintos momentos del ciclo de vida de una extensión:

* Inicio del motor
  * Los sistemas del motor se están iniciando
  * `app_init` de la extensión
  * `init` de la extensión - Se han inicializado todas las API de Defold. Este es el punto recomendado del ciclo de vida de la extensión para crear bindings Lua al código de la extensión.
  * Inicialización de scripts - Se llama a la función `init()` de los archivos script.
* Bucle del motor
  * Actualización del motor
    * `update` de la extensión
    * Actualización de scripts - Se llama a la función `update()` de los archivos script.
  * Eventos del motor (minimizar/maximizar ventana, etc.)
    * `on_event` de la extensión
* Apagado del motor (o reinicio)
  * Finalización de scripts - Se llama a la función `final()` de los archivos script.
  * `final` de la extensión
  * `app_final` de la extensión

## Identificadores de plataforma definidos

El builder define los siguientes identificadores en cada plataforma respectiva:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Logs del servidor de build {#build-server-logs}

Los logs del servidor de build están disponibles cuando el proyecto usa extensiones nativas. El log del servidor de build (`log.txt`) se descarga junto con el motor personalizado cuando se crea la build del proyecto, se almacena dentro del archivo `.internal/%platform%/build.zip` y también se descomprime en la carpeta de build de tu proyecto.

## Extensiones de ejemplo

* [Ejemplo de extensión básica](https://github.com/defold/template-native-extension) (la extensión de este manual)
* [Ejemplo de extensión Android](https://github.com/defold/extension-android)
* [Ejemplo de extensión HTML5](https://github.com/defold/extension-html5)
* [Extensión de reproductor de video para macOS, iOS y Android](https://github.com/defold/extension-videoplayer)
* [Extensión de cámara para macOS y iOS](https://github.com/defold/extension-camera)
* [Extensión In-app Purchase para iOS y Android](https://github.com/defold/extension-iap)
* [Extensión Firebase Analytics para iOS y Android](https://github.com/defold/extension-firebase-analytics)

El [Asset Portal de Defold](https://www.defold.com/assets/) también contiene varias extensiones nativas.
