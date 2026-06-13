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

Si la plataforma en cuestión no debe soportar la extensión, se recomienda simplemente no registrar ningún módulo Lua. De esa forma puedes detectar el soporte comprobando si es nil:

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
        /main                            -- Todos los archivos del proyecto de ejemplo real
            /...
        /myextension                     -- La carpeta raíz real de la extensión
            ext.manifest
            /include                     -- Includes externos, usados por otras extensiones
            /libs
                /<platform>              -- Bibliotecas externas para todas las plataformas soportadas
            /src
                myextension.cpp          -- La API Lua de la extensión y las funciones del ciclo de vida de la extensión
                                            También contiene implementaciones genéricas de tus funciones de API Lua.
                myextension_private.h    -- Tu API interna que cada plataforma implementará (por ejemplo, `myextension_Init`, etc.)
                myextension.mm           -- Si se necesitan llamadas nativas para iOS/macOS. Implementa `myextension_Init`, etc. para iOS/macOS
                myextension_android.cpp  -- Si se necesitan llamadas JNI para Android. Implementa `myextension_Init`, etc. para Android
                /java
                    /<platform>          -- Cualquier archivo java necesario para Android
            /res                         -- Cualquier recurso necesario para una plataforma
            /external
                README.md                -- Notas/scripts sobre cómo crear o empaquetar cualquier biblioteca externa
        /bundleres                       -- Recursos que deben empaquetarse (ver game.project y la [opción bundle_resources]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Cualquier información extra de configuración de la app
```

Ten en cuenta que `myextension.mm` y `myextension_android.cpp` solo son necesarios si haces llamadas nativas específicas para esa plataforma.

#### Carpetas de plataforma

En ciertos lugares, la arquitectura de la plataforma se usa como nombre de carpeta para saber qué archivos usar al compilar/empaquetar la aplicación. Tienen esta forma:

    <architecture>-<platform>

La lista actual es:

    arm64-ios, armv7-ios, x86_64-ios, arm64-android, armv7-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Por ejemplo, coloca las bibliotecas específicas de plataforma en:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Escribir código nativo

En el código fuente de Defold, C++ se usa con mucha moderación y la mayor parte del código es muy similar a C. Casi no hay templates, excepto algunas clases contenedoras, ya que los templates tienen un costo en los tiempos de compilación y en el tamaño del ejecutable.

### Versión de C++

El código fuente de Defold se compila con la versión de C++ predeterminada de cada compilador. El propio código fuente de Defold no usa ninguna versión de C++ superior a C++98. Aunque es posible usar una versión superior para compilar una extensión, una versión superior podría traer cambios de ABI. Esto podría hacer imposible usar una extensión junto con extensiones del motor o del [Asset Portal](/assets).

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
