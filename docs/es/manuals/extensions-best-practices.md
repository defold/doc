---
title: Extensiones nativas - Buenas prácticas
brief: Este manual describe las buenas prácticas al desarrollar extensiones nativas.
---

# Buenas prácticas

Escribir código multiplataforma puede ser difícil, pero hay algunas formas de facilitar tanto el desarrollo como el mantenimiento de ese código.


## Estructura del proyecto

Al crear una extensión, hay algunas cosas que ayudan tanto a desarrollarla como a mantenerla.

### API Lua

Solo debería haber una API Lua y una implementación de ella. Esto hace que sea mucho más fácil tener el mismo comportamiento en todas las plataformas.

Si la plataforma en cuestión no debe soportar la extensión, se recomienda simplemente no registrar ningún módulo Lua. De esa forma puedes detectar el soporte comprobando si es `nil`:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Estructura de carpetas

La siguiente estructura de carpetas se usa con frecuencia para extensiones:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Ten en cuenta que `myextension.mm` y `myextension_android.cpp` solo son necesarios si haces llamadas nativas específicas para esa plataforma.

#### Carpetas de plataforma

En ciertos lugares, la arquitectura de la plataforma se usa como nombre de carpeta para saber qué archivos usar al compilar/empaquetar la aplicación. Tienen esta forma:

    <architecture>-<platform>

La lista actual es:

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32

Por ejemplo, coloca las bibliotecas específicas de plataforma en:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Escribir código nativo

En el código fuente de Defold, C++ se usa con mucha moderación y la mayor parte del código es muy similar a C. Casi no hay templates, excepto algunas clases contenedoras, ya que los templates tienen un costo en los tiempos de compilación y en el tamaño del ejecutable.

### Versión de C++

Al compilar el motor principal, usamos C++11, pero en Windows usamos C++14. Las compilaciones para consolas generalmente requieren C++14 o superior actualmente.

Para las extensiones nativas, no usamos una versión de C++ fija, sino que dependemos de la versión predeterminada de la cadena de herramientas de la plataforma.

El código fuente de Defold evita usar las últimas funcionalidades o versiones de C++. Principalmente porque no hacen falta funcionalidades nuevas al crear un motor de videojuegos, pero también porque seguir las últimas funcionalidades de C++ lleva mucho tiempo, y dominar realmente esas funcionalidades requerirá mucho tiempo valioso.

También tiene el beneficio adicional para los desarrolladores de extensiones de que Defold mantiene una ABI estable. También vale la pena señalar que usar las últimas funcionalidades de C++ puede impedir que el código compile en distintas plataformas debido a diferencias de soporte.

### Sin excepciones de C++

Defold no usa excepciones en el motor. Las excepciones generalmente se evitan en los motores de videojuegos, ya que los datos se conocen (en su mayoría) de antemano durante el desarrollo. Eliminar el soporte para excepciones de C++ reduce el tamaño del ejecutable y mejora el rendimiento en runtime.

### Standard Template Libraries - STL

Como el motor Defold no usa código STL, excepto algunos algoritmos y matemáticas (`std::sort`, `std::upper_bound`, etc.), puede que te funcione usar STL en tu extensión.

De nuevo, ten en cuenta que las incompatibilidades de ABI pueden dificultar el uso de tu extensión junto con otras extensiones o bibliotecas de terceros.

Evitar las bibliotecas STL (con mucho uso de templates) también mejora nuestros tiempos de build y, más importante, el tamaño del ejecutable.

#### Strings

En el motor Defold se usa `const char*` en lugar de `std::string`. El uso de `std::string` es una trampa común al mezclar distintas versiones de C++ o versiones de compilador, ya que puede provocar una incompatibilidad de ABI. Usar `const char*` y algunas funciones auxiliares evitará esto.

### Hacer que las funciones estén ocultas

Usa la palabra clave `static` en funciones locales a tu unidad de compilación si es posible. Esto permite que el compilador haga algunas optimizaciones y puede mejorar el rendimiento y reducir el tamaño del ejecutable.

## Bibliotecas de terceros

Al elegir una biblioteca de terceros para usarla (independientemente del lenguaje), considera lo siguiente:

* Funcionalidad - ¿Resuelve el problema concreto que tienes?
* Rendimiento - ¿Implica un costo de rendimiento en runtime?
* Tamaño de la biblioteca - ¿Cuánto más grande será el ejecutable final? ¿Es aceptable?
* Dependencias - ¿Requiere bibliotecas extra?
* Soporte - ¿En qué estado está la biblioteca? ¿Tiene muchos issues abiertos? ¿Todavía se mantiene?
* Licencia - ¿Está bien usarla para este proyecto?


## Dependencias open source

Asegúrate siempre de tener acceso a tus dependencias. Por ejemplo, si dependes de algo en GitHub, nada impide que ese repositorio sea eliminado, o que cambie repentinamente de rumbo o de propietario. Puedes mitigar este riesgo haciendo fork del repositorio y usando tu fork en lugar del proyecto upstream.

Recuerda que el código de la biblioteca se inyectará en tu juego, así que asegúrate de que la biblioteca haga lo que se supone que debe hacer, ¡y nada más!
