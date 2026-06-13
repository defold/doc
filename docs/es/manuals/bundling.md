---
title: Crear un bundle de una aplicación
brief: Este manual explica cómo crear un bundle de aplicación.
---

# Crear un bundle de una aplicación

Durante el desarrollo de tu aplicación debes acostumbrarte a probar el juego en las plataformas objetivo con la mayor frecuencia posible. Esto ayuda a detectar problemas de rendimiento temprano en el proceso de desarrollo, cuando son mucho más fáciles de corregir. También se recomienda probar en todas las plataformas objetivo para encontrar discrepancias en aspectos como los shaders. Al desarrollar para móviles, tienes la opción de usar la [app de desarrollo móvil](/manuals/dev-app/) para enviar contenido a la app, en lugar de tener que hacer un ciclo completo de crear el bundle y desinstalar/instalar.

Puedes crear un bundle de aplicación para todas las plataformas compatibles con Defold desde el propio editor Defold, sin necesidad de herramientas externas. También puedes crear bundles desde la línea de comando usando nuestras herramientas de línea de comando. La creación de bundles de aplicación requiere una conexión de red si tu proyecto contiene una o más [extensiones nativas](/manuals/extensions).

## Crear bundles desde el editor

Creas un bundle de aplicación desde el menú <kbd>Project</kbd> y la opción <kbd>Bundle</kbd>:

![](images/bundling/bundle_menu.png)

Al seleccionar cualquiera de las opciones del menú, se abrirá el diálogo Bundle para esa plataforma específica.

### Reportes de build

Al crear un bundle de tu juego hay una opción para crear un reporte de build. Esto es muy útil para entender el tamaño de todos los assets que forman parte del bundle de tu juego. Simplemente marca la casilla *Generate build report* al crear el bundle del juego.

![reporte de build](images/profiling/build_report.png)

Para obtener más información sobre los reportes de build, consulta el [manual de profiling](/manuals/profiling/#build-reports).

### Android

La creación de un bundle de aplicación Android (archivo .apk) está documentada en el [manual de Android](/manuals/android/#creating-an-android-application-bundle).

### iOS

La creación de un bundle de aplicación iOS (archivo .ipa) está documentada en el [manual de iOS](/manuals/ios/#creating-an-ios-application-bundle).

### macOS

La creación de un bundle de aplicación macOS (archivo .app) está documentada en el [manual de macOS](/manuals/macos).

### Linux

La creación de un bundle de aplicación Linux no requiere ninguna configuración específica ni configuración opcional específica de la plataforma en el [archivo de configuración del proyecto](/manuals/project-settings/#linux) *game.project*.

### Windows

La creación de un bundle de aplicación Windows (archivo .exe) está documentada en el [manual de Windows](/manuals/windows).

### HTML5

La creación de un bundle de aplicación HTML5, así como la configuración opcional, está documentada en el [manual de HTML5](/manuals/html5/#creating-html5-bundle).

#### Facebook Instant Games

Es posible crear una versión especial de un bundle de aplicación HTML5 específicamente para Facebook Instant Games. Este proceso está documentado en el [manual de Facebook Instant Games](/manuals/instant-games/).

## Crear bundles desde la línea de comando

El editor usa nuestra [herramienta de línea de comando Bob](/manuals/bob/) para crear el bundle de la aplicación.

Durante el desarrollo diario de tu aplicación, es probable que crees builds y bundles desde el editor Defold. En otras circunstancias, quizás quieras generar automáticamente bundles de aplicación, por ejemplo al crear builds por lotes para todos los objetivos al publicar una nueva versión o al crear builds nocturnas de la última versión del juego, quizá en un entorno de CI. La creación de builds y bundles de una aplicación se puede hacer fuera del flujo de trabajo normal del editor usando la [herramienta de línea de comando Bob](/manuals/bob/).

## La estructura del bundle

La estructura lógica del bundle se organiza así:

![](images/bundling/bundle_schematic_01.png)

Un bundle se genera en una carpeta. Según la plataforma, esa carpeta también se puede archivar como zip en un `.apk` o `.ipa`.
El contenido de la carpeta depende de la plataforma.

Además de los archivos ejecutables, nuestro proceso de creación de bundles también recopila los assets requeridos para la plataforma (por ejemplo, los archivos de recurso .xml para Android).

Usando la configuración [bundle_resources](https://defold.com/manuals/project-settings/#bundle-resources), puedes configurar assets que deben colocarse dentro del bundle tal cual.
Puedes controlar esto por plataforma.

Los assets del juego se ubican en el archivo `game.arcd` y se comprimen individualmente usando compresión LZ4.
Usando la configuración [custom_resources](https://defold.com/manuals/project-settings/#custom-resources), puedes configurar assets que deben colocarse (con compresión) dentro de `game.arcd`.
Se puede acceder a estos assets mediante la función [`sys.load_resource()`](https://defold.com/ref/sys/#sys.load_resource).

## Release vs Debug

Al crear un bundle de aplicación tienes la opción de crear un bundle debug o release. Las diferencias entre los dos bundles son pequeñas, pero es importante tenerlas en cuenta:

* Las builds release no incluyen el [profiler](/manuals/profiling)
* Las builds release no incluyen el [grabador de pantalla](/ref/stable/sys/#start_record)
* Las builds release no muestran la salida de ninguna llamada a `print()` ni la salida de ninguna extensión nativa
* Las builds release tienen el valor `is_debug` en `sys.get_engine_info()` establecido en `false`
* Las builds release no harán búsquedas inversas de valores `hash` al llamar a `tostring()`. En la práctica, esto significa que un `tostring()` para un valor de tipo `url` o `hash` devolverá su representación numérica y no la cadena original (`'hash: [/camera_001]'` vs `'hash: [11844936738040519888 (unknown)]'`)
* Las builds release no admiten el targeting desde el editor para [hot-reload](/manuals/hot-reload) y funcionalidades similares
