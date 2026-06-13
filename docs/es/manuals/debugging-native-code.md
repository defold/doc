---
title: Depuración de código nativo en Defold
brief: Este manual explica cómo depurar código nativo en Defold.
---

# Depuración de código nativo {#debugging-native-code}

Defold está bien probado y, en circunstancias normales, debería crashear muy rara vez. Sin embargo, es imposible garantizar que nunca crashee, especialmente si tu juego usa extensiones nativas. Si tienes problemas con crashes o con código nativo que no se comporta como esperas, hay varias formas de avanzar:

* Usa un depurador para avanzar paso a paso por el código
* Usa depuración con print
* Analiza un log de crash
* Simboliza un callstack


## Usar un depurador {#use-a-debugger}

La forma más común es ejecutar el código mediante un `debugger`. Te permite avanzar paso a paso por el código, definir `breakpoints` y detendrá la ejecución si ocurre un crash.

Hay varios depuradores para cada plataforma.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Cada herramienta puede depurar ciertas plataformas:

* Visual studio - Windows + plataformas compatibles con gdbserver (p. ej. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + plataformas compatibles con gdbserver
* Xcode -  macOS, iOS ([más información](/manuals/debugging-native-code-ios))
* Android Studio - Android ([más información](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (mediante lldb)


## Usar depuración con print {#use-print-debugging}

La forma más simple de depurar tu código nativo es usar [depuración con print](http://en.wikipedia.org/wiki/Debugging#Techniques). Usa las funciones del [namespace `dmLog`](/ref/stable/dmLog/) para observar variables o indicar el flujo de ejecución. Usar cualquiera de las funciones de log imprimirá en la vista *Console* del editor y en el [log del juego](/manuals/debugging-game-and-system-logs).


## Analizar un log de crash {#analyze-a-crash-log}

El motor Defold guarda un archivo `_crash` si ocurre un crash severo. El archivo de crash contendrá información sobre el sistema y sobre el crash. La [salida del log del juego](/manuals/debugging-game-and-system-logs) escribirá dónde se encuentra el archivo de crash (varía según el sistema operativo, el dispositivo y la aplicación).

Puedes usar el [módulo crash](https://www.defold.com/ref/crash/) para leer este archivo en la sesión siguiente. Se recomienda leer el archivo, recopilar la información, imprimirla en la consola y enviarla a un [servicio de analytics](/tags/stars/analytics/) que soporte la recopilación de logs de crash.

::: important
En Windows también se genera un archivo `_crash.dmp`. Este archivo es útil al depurar un crash.
:::

### Obtener el log de crash desde un dispositivo {#getting-the-crash-log-from-a-device}

Si ocurre un crash en un dispositivo móvil, puedes elegir descargar el archivo de crash a tu propia computadora y analizarlo localmente.

#### Android

Si la app es [debuggable](/manuals/project-settings/#android), puedes obtener el log de crash usando la [herramienta Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) y el comando `adb shell`:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

En iTunes, puedes ver/descargar el contenedor de una app.

En la ventana `Xcode -> Devices`, también puedes seleccionar los logs de crash


## Simbolizar un callstack {#symbolicate-a-callstack}

Si obtienes un callstack desde un archivo `_crash` o desde un [archivo de log](/manuals/debugging-game-and-system-logs), puedes simbolizarlo. Esto significa traducir cada dirección del callstack a un nombre de archivo y número de línea, lo que a su vez ayuda a encontrar la causa raíz.

Es importante que hagas coincidir el motor correcto con el callstack; de lo contrario, es muy probable que termines depurando cosas incorrectas. Usa la opción [`--with-symbols`](https://www.defold.com/manuals/bob/) al crear el bundle con [bob](https://www.defold.com/manuals/bob/) o marca el checkbox "Generate debug symbols" en el diálogo de bundle del editor:

* iOS - la carpeta `dmengine.dSYM.zip` en `build/arm64-ios` contiene los símbolos de depuración para builds de iOS.
* macOS - la carpeta `dmengine.dSYM.zip` en `build/x86_64-macos` contiene los símbolos de depuración para builds de macOS.
* Android - la carpeta de salida del bundle `projecttitle.apk.symbols/lib/` contiene los símbolos de depuración para las arquitecturas objetivo.
* Linux - el ejecutable contiene los símbolos de depuración.
* Windows - el archivo `dmengine.pdb` en `build/x86_64-win32` contiene los símbolos de depuración para builds de Windows.
* HTML5 - el archivo `dmengine.js.symbols` en `build/wasm-web` contiene los símbolos de depuración para builds de HTML5.

::: important
Es muy importante que guardes los símbolos de depuración en algún lugar para cada release pública que hagas de tu juego y que sepas a qué release pertenecen esos símbolos de depuración. No podrás depurar ningún crash nativo si no tienes los símbolos de depuración. Además, deberías conservar una versión sin strip (`unstripped`) del motor. Esto permite la mejor simbolización del callstack.
:::


### Subir símbolos a Google Play {#uploading-symbols-to-google-play}
Puedes [subir los símbolos de depuración a Google Play](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems) para que cualquier crash registrado en Google Play muestre callstacks simbolizados. Comprime en un zip el contenido de la carpeta de salida del bundle `projecttitle.apk.symbols/lib/`. La carpeta incluye una o más subcarpetas con nombres de arquitectura como `arm64-v8a` y `armeabi-v7a`.


### Simbolizar un callstack de Android {#symbolicate-an-android-callstack}

1. Obtén el motor desde tu carpeta de build

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Descomprime en una carpeta:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Busca la dirección del callstack

	P. ej., en el callstack sin simbolizar podría verse así

	`#00 pc 00257224 libmy_game_name.so`

	Donde *`00257224`* es la dirección

4. Resuelve la dirección

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Nota: Si obtienes un stack trace desde los [logs de Android](/manuals/debugging-game-and-system-logs), podrías simbolizarlo usando [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html)

### Simbolizar un callstack de iOS {#symbolicate-an-ios-callstack}

1. Si usas extensiones nativas (Native Extensions), el servidor puede proporcionarte los símbolos (`.dSYM`) (pasa `--with-symbols` a bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# producirá Contents/Resources/DWARF/dmengine
```

2. Si no usas extensiones nativas (Native Extensions), descarga los símbolos vanilla:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Simboliza usando la dirección de carga

	Por alguna razón, poner simplemente la dirección del callstack no funciona (es decir, dirección de carga 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Especificar la dirección de carga directamente tampoco funciona

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Sumar la dirección de carga a la dirección funciona:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
