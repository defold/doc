---
title: Manual del constructor de proyectos Defold
brief: Bob es una herramienta de línea de comando para crear builds de proyectos Defold. Este manual explica cómo usar la herramienta.
---

# Bob el constructor

Bob es una herramienta de línea de comando para crear builds de proyectos Defold fuera del flujo de trabajo normal del editor.

Bob puede crear datos (correspondientes al paso de build al seleccionar el elemento de menú del editor <kbd>Project ▸ Build</kbd>), crear archivos de datos y crear bundles de aplicación independientes y distribuibles (correspondientes a las opciones del elemento de menú del editor <kbd>Project ▸ Bundle ▸ ...</kbd>)

Bob se distribuye como un archivo _JAR_ de Java que contiene todo lo necesario para hacer la build. Puedes encontrar la distribución más reciente de *bob.jar* en la [página de GitHub Releases](https://github.com/defold/defold/releases). Selecciona un release y luego descarga *bob/bob.jar*. Necesitarás OpenJDK 25 para ejecutarlo.

Mirrors compatibles de OpenJDK 25:
* [OpenJDK 25 by Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 by Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Si estás en Windows, necesitas el instalador de archivo `.msi` para OpenJDK.

## Uso {#usage}

Bob se ejecuta desde una shell o desde la línea de comando invocando `java` (o `java.exe` en Windows) y proporcionando el archivo Java de bob como argumento:

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
 -a,--archive                            Build archive
 -ar,--architectures <arg>               Comma separated list of
                                         architectures to include for the
                                         platform
    --archive-resource-padding <arg>     The alignment of the resources in
                                         the game archive. Default is 4
 -bf,--bundle-format <arg>               Which formats to create the
                                         application bundle in. Comma
                                         separated list. (Android: 'apk'
                                         and 'aab')
    --binary-output <arg>                Location where built engine
                                         binary will be placed. Default is
                                         "<build-output>/<platform>/"
 -bo,--bundle-output <arg>               Bundle output directory
 -br,--build-report <arg>                DEPRECATED! Use
                                         --build-report-json instead
 -brhtml,--build-report-html <arg>       Filepath where to save a build
                                         report as HTML
 -brjson,--build-report-json <arg>       Filepath where to save a build
                                         report as JSON
    --build-artifacts <arg>              If left out, will default to
                                         build the engine. Choices:
                                         'engine', 'plugins', 'library'.
                                         Comma separated list.
    --build-server <arg>                 The build server (when using
                                         native extensions)
    --build-server-header <arg>          Additional build server header to
                                         set
 -ce,--certificate <arg>                 DEPRECATED! Use --keystore
                                         instead
 -d,--debug                              DEPRECATED! Use --variant=debug
                                         instead
    --debug-ne-upload                    Outputs the files sent to build
                                         server as upload.zip
    --debug-output-spirv <arg>           Force build SPIR-V shaders
    --debug-output-wgsl <arg>            Force build WGSL shaders
    --defoldsdk <arg>                    What version of the defold sdk
                                         (sha1) to use
 -e,--email <arg>                        User email
 -ea,--exclude-archive                   Exclude resource archives from
                                         application bundle. Use this to
                                         create an empty Defold
                                         application for use as a build
                                         target
    --exclude-build-folder <arg>         DEPRECATED! Use '.defignore' file
                                         instead
 -h,--help                               This help message
 -i,--input <arg>                        DEPRECATED! Use --root instead
    --identity <arg>                     Sign identity (iOS)
 -kp,--key-pass <arg>                    Password of the deployment key if
                                         different from the keystore
                                         password (Android)
 -ks,--keystore <arg>                    Deployment keystore used to sign
                                         APKs (Android)
 -ksa,--keystore-alias <arg>             The alias of the signing key+cert
                                         you want to use (Android)
 -ksp,--keystore-pass <arg>              Password of the deployment
                                         keystore (Android)
 -l,--liveupdate <arg>                   Yes if liveupdate content should
                                         be published
    --max-cpu-threads <arg>              Max count of threads that bob.jar
                                         can use
 -mp,--mobileprovisioning <arg>          mobileprovisioning profile (iOS)
    --ne-build-dir <arg>                 Specify a folder with includes or
                                         source, to build a specific
                                         library. More than one occurrence
                                         is allowed.
    --ne-output-name <arg>               Specify a library target name
 -o,--output <arg>                       Output directory. Default is
                                         "build/default"
 -p,--platform <arg>                     Platform (when building and
                                         bundling)
 -pk,--private-key <arg>                 DEPRECATED! Use --keystore
                                         instead
 -r,--root <arg>                         Build root directory. Default is
                                         current directory
    --resource-cache-local <arg>         Path to local resource cache.
    --resource-cache-remote <arg>        URL to remote resource cache.
    --resource-cache-remote-pass <arg>   Password/token to authenticate
                                         access to the remote resource
                                         cache.
    --resource-cache-remote-user <arg>   Username to authenticate access
                                         to the remote resource cache.
    --settings <arg>                     Path to a game project settings
                                         file. More than one occurrence is
                                         allowed. The settings files are
                                         applied left to right.
    --strip-executable                   Strip the dmengine of debug
                                         symbols (when bundling iOS or
                                         Android)
 -tc,--texture-compression <arg>         Use texture compression as
                                         specified in texture profiles
 -tp,--texture-profiles <arg>            DEPRECATED! Use
                                         --texture-compression instead
 -u,--auth <arg>                         User auth token
    --use-async-build-server             DEPRECATED! Asynchronous build is
                                         now the default.
    --use-lua-bytecode-delta             Use byte code delta compression
                                         when building for multiple
                                         architectures
    --use-uncompressed-lua-source        Use uncompressed and unencrypted
                                         Lua source code instead of byte
                                         code
    --use-vanilla-lua                    DEPRECATED! Use
                                         --use-uncompressed-lua-source
                                         instead.
 -v,--verbose                            Verbose output
    --variant <arg>                      Specify debug, release or
                                         headless version of dmengine
                                         (when bundling)
    --version                            Prints the version number to the
                                         output
    --with-symbols                       Generate the symbol file (if
                                         applicable)
```

Comandos disponibles:

`clean`
: Elimina los archivos construidos en el directorio de build.

`distclean`
: Elimina todos los archivos en el directorio de build.

`build`
: Construye todos los datos del proyecto. Agrega la opción `--archive` para crear un archivo de datos ("`game.darc`" en el directorio de build).

`bundle`
: Crea un bundle de aplicación específico de la plataforma. Crear un bundle requiere que haya un archivo construido presente (`build` con la opción `--archive`) y que se especifique una plataforma objetivo (con la opción `--platform`). Bob crea el bundle en el directorio de salida salvo que se especifique un directorio diferente con la opción `--bundle-output`. El nombre del bundle se toma de la configuración del nombre del proyecto en *game.project*. `--variant` especifica qué tipo de ejecutable construir al crear el bundle y, junto con la opción `--strip-executable`, reemplaza la opción `--debug`. Si no se especifica `--variant`, obtendrás una versión release del motor (sin símbolos en Android e iOS). Definir `--variant` como debug y omitir `--strip-executable` produce el mismo tipo de ejecutable que antes producía `--debug`.

`resolve`
: Resuelve todas las dependencias de bibliotecas externas.

Plataformas y arquitecturas disponibles:

`x86_64-macos`
: macOS 64 bits

`arm64-macos`
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bits

`x86-win32`
: Windows 32 bits

`x86_64-linux`
: Linux 64 bits

`x86_64-ios`
: iOS macOS 64 bits (iOS Simulator)

`arm64-ios`
: iOS 64 bits. De forma predeterminada, el valor del argumento `--architectures` es `arm64-ios`.

`armv7-android`
: Android con las arquitecturas disponibles `armv7-android` de 32 bits y `arm64-android` de 64 bits. De forma predeterminada, el valor del argumento `--architectures` es `armv7-android,arm64-android`.

`wasm-web`
: HTML5 con las arquitecturas disponibles `wasm-web` y `wasm_pthread-web`. De forma predeterminada, el valor del argumento `--architectures` es `wasm-web`.

De forma predeterminada, Bob busca en el directorio actual un proyecto para construir. Si cambias el directorio actual a un proyecto Defold e invocas bob, construye los datos del proyecto en el directorio de salida predeterminado *build/default*.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Puedes encadenar comandos para realizar una secuencia de tareas de una sola vez. El siguiente ejemplo resuelve bibliotecas, limpia el directorio de build, crea datos de archivo y crea el bundle de una aplicación macOS (llamada *My Game.app*):

```sh
$ java -jar bob.jar --archive --platform x86_64-macos resolve distclean build bundle
100%
$ ls -al build/default/
total 70784
drwxr-xr-x   13 sicher  staff       442  1 Dec 10:15 .
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 ..
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 My Game.app
drwxr-xr-x    8 sicher  staff       272  1 Dec 10:15 builtins
-rw-r--r--    1 sicher  staff    140459  1 Dec 10:15 digest_cache
drwxr-xr-x    4 sicher  staff       136  1 Dec 10:15 fonts
-rw-r--r--    1 sicher  staff  35956340  1 Dec 10:15 game.darc
-rw-r--r--    1 sicher  staff       735  1 Dec 10:15 game.projectc
drwxr-xr-x  223 sicher  staff      7582  1 Dec 10:15 graphics
drwxr-xr-x    3 sicher  staff       102  1 Dec 10:15 input
drwxr-xr-x   20 sicher  staff       680  1 Dec 10:15 logic
drwxr-xr-x   27 sicher  staff       918  1 Dec 10:15 sound
-rw-r--r--    1 sicher  staff    131926  1 Dec 10:15 state
$
```
