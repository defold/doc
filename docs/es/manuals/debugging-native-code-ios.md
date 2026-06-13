---
title: Depuración en iOS/macOS
brief: Este manual describe cómo depurar una build usando Xcode.
---

# Depuración en iOS/macOS

Aquí describimos cómo depurar una build usando [Xcode](https://developer.apple.com/xcode/), el IDE preferido de Apple para desarrollar para macOS e iOS.

## Xcode

* Crea el bundle de la app usando bob, con la opción `--with-symbols` ([más información](/manuals/debugging-native-code/#symbolicate-a-callstack)):

```sh
$ cd myproject
$ wget http://d.defold.com/archive/<sha1>/bob/bob.jar
$ java -jar bob.jar --platform armv7-darwin build --with-symbols --variant debug --archive bundle -bo build/ios -mp <app>.mobileprovision --identity "iPhone Developer: Your Name (ID)"
```

* Instala la app, ya sea con `Xcode`, `iTunes` o [ios-deploy](https://github.com/ios-control/ios-deploy)

```sh
$ ios-deploy -b <AppName>.ipa
```

* Obtén la carpeta `.dSYM` (es decir, los símbolos de depuración)

	* Si no usas extensiones nativas (Native Extensions), puedes descargar el archivo `.dSYM` desde [d.defold.com](http://d.defold.com)

	* Si estás usando una extensión nativa, la carpeta `.dSYM` se genera cuando haces la build con [bob.jar](https://www.defold.com/manuals/bob/). Solo es necesario hacer la build (sin archive ni bundling):

```sh
$ cd myproject
$ unzip .internal/cache/arm64-ios/build.zip
$ mv dmengine.dSYM <AppName>.dSYM
$ mv <AppName>.dSYM/Contents/Resources/DWARF/dmengine <AppName>.dSYM/Contents/Resources/DWARF/<AppName>
```

### Crear proyecto

Para depurar correctamente, necesitamos tener un proyecto y el código fuente mapeado.
No usamos este proyecto para hacer builds, solo para depurar.

* Crea un proyecto nuevo de Xcode y elige la plantilla `Game`

	![project_template](images/extensions/debugging/ios/project_template.png)

* Elige un nombre (por ejemplo, `debug`) y la configuración predeterminada

* Elige una carpeta donde guardar el proyecto

* Agrega tu código a la app

	![add_files](images/extensions/debugging/ios/add_files.png)

* Asegúrate de que "Copy items if needed" esté desmarcado.

	![add_source](images/extensions/debugging/ios/add_source.png)

* Este es el resultado final

	![added_source](images/extensions/debugging/ios/added_source.png)


* Desactiva el paso `Build`

	![edit_scheme](images/extensions/debugging/ios/edit_scheme.png)

	![disable_build](images/extensions/debugging/ios/disable_build.png)

* Configura la versión de `Deployment target` para que ahora sea mayor que la versión de iOS de tu dispositivo

	![deployment_version](images/extensions/debugging/ios/deployment_version.png)

* Selecciona el dispositivo objetivo

	![select_device](images/extensions/debugging/ios/select_device.png)


### Iniciar el depurador

Tienes varias opciones para depurar una app

1. Puedes elegir `Debug` -> `Attach to process...` y seleccionar la app desde allí

2. O elegir `Attach to process by PID or Process name`

	![select_device](images/extensions/debugging/ios/attach_to_process_name.png)

3. Inicia la app en el dispositivo

4. En `Edit Scheme`, agrega la carpeta <AppName>.app como ejecutable

### Símbolos de depuración

**Para usar lldb, la ejecución debe estar pausada**

* Agrega la ruta de `.dSYM` a lldb

```
(lldb) add-dsym <PathTo.dSYM>
```

	![add_dsym](images/extensions/debugging/ios/add_dsym.png)

* Verifica que `lldb` haya leído los símbolos correctamente

```
(lldb) image list <AppName>
```

### Mapeos de rutas

* Agrega el código fuente del motor (cámbialo según tus necesidades)

```
(lldb) settings set target.source-map /Users/builder/ci/builds/engine-ios-64-master/build /Users/mathiaswesterdahl/work/defold
(lldb) settings append target.source-map /private/var/folders/m5/bcw7ykhd6vq9lwjzq1mkp8j00000gn/T/job4836347589046353012/upload/videoplayer/src /Users/mathiaswesterdahl/work/projects/extension-videoplayer-native/videoplayer/src
```

* Es posible obtener la carpeta de trabajo desde el ejecutable. La carpeta de trabajo se llama `job1298751322870374150`, cada vez con un número aleatorio.

```sh
$ dsymutil -dump-debug-map <executable> 2>&1 >/dev/null | grep /job

```

* Verifica los mapeos de código fuente

```
(lldb) settings show target.source-map
```

Puedes comprobar de qué archivo fuente proviene un símbolo usando

```
(lldb) image lookup -va <SymbolName>
```

### Breakpoints

* Abre un archivo en la vista del proyecto y define un breakpoint

	![breakpoint](images/extensions/debugging/ios/breakpoint.png)

## Notas

### Comprobar el UUID del binario

Para que el depurador acepte la carpeta `.dSYM`, el UUID debe coincidir con el UUID del ejecutable que se está depurando. Puedes comprobar el UUID así:

```sh
$ dwarfdump -u <PathToBinary>
```
