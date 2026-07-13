---
title: Depuración - logs del juego y del sistema
brief: Este manual explica cómo leer los logs del juego y del sistema.
---

# Logs del juego y del sistema

El log del juego muestra toda la salida del motor, las extensiones nativas y la lógica de tu juego. Los comandos [print()](/ref/stable/base/#print:...) y [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) se pueden usar desde tus scripts y módulos Lua para mostrar información en el log del juego. Puedes usar las funciones del [namespace `dmLog`](/ref/stable/dmLog/) para escribir en el log del juego desde extensiones nativas. El log del juego se puede leer desde el editor, desde una ventana de terminal, usando herramientas específicas de la plataforma o desde un archivo de log.

Los logs del sistema son generados por el sistema operativo y pueden proporcionar información adicional que ayude a identificar un problema. Los logs del sistema pueden contener trazas de pila de crashes y advertencias de poca memoria.

::: important
El logging en consola/en pantalla solo muestra información en builds Debug. En builds Release, el log de consola está vacío, pero puedes activar el logging en archivo en Release definiendo la opción del proyecto "Write Log File" en "Always". Consulta los detalles a continuación.
:::

## Leer el log del juego desde el editor

Cuando ejecutas tu juego localmente desde el editor o conectado a la [app de desarrollo móvil](/manuals/dev-app), toda la salida se mostrará en el panel de consola del editor:

![Editor 2](images/editor/editor2_overview.png)

## Leer el log del juego desde la terminal

Cuando ejecutas un juego Defold desde la terminal, el log aparecerá en la propia ventana de terminal. En Windows y Linux escribes el nombre del ejecutable en la terminal para iniciar el juego. En macOS necesitas lanzar el motor desde dentro del archivo .app:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Leer logs del juego y del sistema usando herramientas específicas de la plataforma

### HTML5

Los logs se pueden leer usando las herramientas de desarrollo incluidas en la mayoría de los navegadores.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Puedes usar la herramienta Android Debug Bridge (ADB) para ver los logs del juego y del sistema.

:[Android ADB](../shared/android-adb.md)

Una vez instalada y configurada, conecta tu dispositivo por USB, abre una terminal y ejecuta:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

El dispositivo volcará entonces toda la salida en la terminal actual, junto con cualquier salida impresa desde el juego.

Si quieres ver solo la salida de la aplicación Defold, usa este comando:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

Tienes varias opciones para leer logs del juego y del sistema en iOS:

1. Puedes usar la [herramienta Console](https://support.apple.com/guide/console/welcome/mac) para leer logs del juego y del sistema.
2. Puedes usar el depurador LLDB para conectarte a un juego que se está ejecutando en un dispositivo. Para depurar un juego, debe estar firmado con un “Apple Developer Provisioning Profile” que incluya el dispositivo en el que quieres depurar. Crea el bundle del juego desde el editor y proporciona el perfil provisional en el diálogo de bundle (crear bundles para iOS solo está disponible en macOS).

Para lanzar el juego y conectar el depurador necesitarás una herramienta llamada [ios-deploy](https://github.com/phonegap/ios-deploy). Instala y depura tu juego ejecutando lo siguiente en una terminal:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTA: no es el archivo .ipa
```

Esto instalará la app en tu dispositivo, la iniciará y conectará automáticamente un depurador LLDB. Si no conoces LLDB, lee [Getting Started with LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Leer el log del juego desde el archivo de log

Usa la opción del proyecto "Write Log File" en *game.project* para controlar el logging a archivo:

- "Never": No escribir un archivo de log.
- "Debug": Escribir un archivo de log solo para builds Debug.
- "Always": Escribir un archivo de log tanto para builds Debug como Release.

Cuando está activado, cualquier salida del juego se escribirá en disco en un archivo llamado "`log.txt`". Así es como puedes extraer el archivo si ejecutas el juego en un dispositivo:

iOS
: Conecta tu dispositivo a una computadora con macOS y Xcode instalados.

  Abre Xcode y ve a <kbd>Window ▸ Devices and Simulators</kbd>.

  Selecciona tu dispositivo en la lista y luego selecciona la app correspondiente en la lista *Installed Apps*.

  Haz click en el icono de engranaje debajo de la lista y selecciona <kbd>Download Container...</kbd>.

  ![descargar contenedor](images/debugging/download_container.png)

  Una vez que el contenedor se haya extraído, se mostrará en *Finder*. Haz click derecho en el contenedor y selecciona <kbd>Show Package Content</kbd>. Localiza el archivo "`log.txt`", que debería estar ubicado en "`AppData/Documents/`".

Android(
: La capacidad de extraer el "`log.txt`" depende de la versión del sistema operativo y del fabricante. Aquí tienes una [guía paso a paso](https://stackoverflow.com/a/48077004/129360) breve y sencilla.
