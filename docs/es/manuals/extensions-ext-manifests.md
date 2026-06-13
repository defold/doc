---
title: Extensiones nativas - manifiestos de extensión
brief: Este manual describe el manifiesto de extensión y cómo se relaciona con el manifiesto de aplicación y el manifiesto del motor.
---

# Archivos de manifiesto de extensión, aplicación y motor

El manifiesto de extensión es un archivo de configuración con flags y defines que se usan al crear la build de una sola extensión. Esta configuración se combina con una configuración a nivel de aplicación y una configuración base para el propio motor Defold.

## Manifiesto de aplicación

El manifiesto de aplicación (extensión de archivo `.appmanifest`) es una configuración a nivel de aplicación que define cómo crear la build de tu juego en los servidores de build. El manifiesto de aplicación te permite eliminar partes del motor que no usas. Si no necesitas un motor de físicas, puedes eliminarlo del ejecutable para reducir su tamaño. Aprende cómo excluir funcionalidades no usadas [en el manual del manifiesto de aplicación](/manuals/app-manifest).

## Manifiesto del motor

El motor Defold tiene un manifiesto de build (`build.yml`) que se incluye con cada release del motor y del SDK de Defold. El manifiesto controla qué versiones del SDK usar, qué compiladores, enlazadores y otras herramientas ejecutar, y qué flags predeterminados de build y enlace pasar a estas herramientas. El manifiesto se puede encontrar en share/extender/build_input.yml [en GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Manifiesto de extensión

El manifiesto de extensión (`ext.manifest`), por otro lado, es un archivo de configuración específico para una extensión. El manifiesto de extensión controla cómo se compila y enlaza el código fuente de la extensión y qué librerías adicionales incluir.

Los tres archivos de manifiesto distintos comparten la misma sintaxis para poder fusionarse y controlar por completo cómo se crean las builds de las extensiones y del juego.

Para cada extensión que se crea, los manifiestos se combinan de la siguiente manera:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Esto permite al usuario sobrescribir el comportamiento predeterminado del motor y también el de cada extensión. Y, para la etapa final de enlace, fusionamos el manifiesto de aplicación con el manifiesto de Defold:

	manifest = merge(game.appmanifest, build.yml)


### El archivo ext.manifest

Aparte del nombre de la extensión, el archivo de manifiesto puede contener flags de compilación específicos de plataforma, flags de enlace, librerías y frameworks. Si el archivo *ext.manifest* no contiene un segmento "platforms", o falta una plataforma en la lista, la plataforma para la que hagas bundle se seguirá creando, pero sin ningún flag adicional definido.

Aquí hay un ejemplo:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    armv7-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Claves permitidas

Las claves permitidas para flags de compilación específicos de plataforma son:

* `frameworks` - Frameworks de Apple que se deben incluir al crear la build (iOS y macOS)
* `weakFrameworks` - Frameworks de Apple que se pueden incluir opcionalmente al crear la build (iOS y macOS)
* `flags` - Flags que se deben pasar al compilador
* `linkFlags` - Flags que se deben pasar al enlazador
* `libs` - Librerías adicionales que se deben incluir al enlazar
* `defines` - Defines que se deben definir al crear la build
* `aaptExtraPackages` - Nombre de paquete extra que se debe generar (Android)
* `aaptExcludePackages` - Expresión regular (o nombres exactos) de paquetes que se deben excluir (Android)
* `aaptExcludeResourceDirs` - Expresión regular (o nombres exactos) de directorios de recursos que se deben excluir (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Estos flags se usan para eliminar elementos definidos previamente en el contexto de la plataforma.

Para todas las palabras clave, aplicamos un filtro de lista blanca. Esto evita el manejo ilegal de rutas y el acceso a archivos fuera de la carpeta de subida de la build.
