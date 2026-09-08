---
title: Manuale dello strumento di build per progetti Defold
brief: Bob è uno strumento a riga di comando per creare build di progetti Defold. Questo manuale spiega come usarlo.
---

# Bob il costruttore {#bob-the-builder}

Bob è uno strumento a riga di comando per creare build di progetti Defold al di fuori del normale flusso di lavoro dell'editor.

Bob può creare una build dei dati (operazione che corrisponde alla selezione della voce di menu <kbd>Project ▸ Build</kbd> nell'editor), creare archivi di dati e creare bundle di applicazioni autonomi e distribuibili (operazione che corrisponde alle opzioni della voce di menu <kbd>Project ▸ Bundle ▸ ...</kbd> nell'editor)

Bob viene distribuito come archivio Java _JAR_ che contiene tutto il necessario per creare una build. Trovi la versione più recente di *bob.jar* nella [pagina delle release su GitHub](https://github.com/defold/defold/releases). Seleziona una release, quindi scarica *bob/bob.jar*. Per eseguirlo è necessario OpenJDK 25.

Mirror compatibili di OpenJDK 25:
* [OpenJDK 25 di Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 di Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Se usi Windows, scegli il programma di installazione di OpenJDK in formato `.msi`.

## Utilizzo {#usage}

Bob si esegue da una shell o dalla riga di comando, richiamando `java` (o `java.exe` su Windows) e passando l'archivio Java di Bob come argomento:

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
                                         Comma separated list
    --build-input <arg>                  Project resource path to build
                                         instead of game.project. May be
                                         specified more than once. More
                                         than one occurrence is allowed
    --build-input-file <arg>             File containing project resource
                                         paths to build instead of
                                         game.project. May be specified
                                         more than once. More than one
                                         occurrence is allowed
    --build-server <arg>                 The build server (when using
                                         native extensions)
    --build-server-header <arg>          Additional build server header to
                                         set. More than one occurrence is
                                         allowed
 -ce,--certificate <arg>                 DEPRECATED! Use --keystore
                                         instead
 -d,--debug                              DEPRECATED! Use --variant=debug
                                         instead
    --debug-ne-upload                    Outputs the files sent to build
                                         server as upload.zip
    --debug-output-glsl <arg>            Force build GLSL shaders
    --debug-output-hlsl <arg>            Force build HLSL shaders
    --debug-output-msl <arg>             Force build Metal shaders
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
    --experimental-path-minification     Minimizes resource path names in
                                         order to save bundle size.
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
                                         is allowed
    --ne-output-name <arg>               Specify a library target name
 -o,--output <arg>                       Output directory. Default is
                                         "build/default"
 -p,--platform <arg>                     Platform (when building and
                                         bundling)
 -pk,--private-key <arg>                 DEPRECATED! Use --keystore
                                         instead
 -r,--root <arg>                         Build root directory. Default is
                                         current directory
    --resource-cache-local <arg>         Path to local resource cache
    --resource-cache-remote <arg>        URL to remote resource cache
    --resource-cache-remote-pass <arg>   Password/token to authenticate
                                         access to the remote resource
                                         cache
    --resource-cache-remote-user <arg>   Username to authenticate access
                                         to the remote resource cache
    --settings <arg>                     Path to a game project settings
                                         file. The settings files are
                                         applied left to right. More than
                                         one occurrence is allowed
    --strip-executable                   Strip the dmengine of debug
                                         symbols (when bundling iOS or
                                         Android)
 -tc,--texture-compression               Use texture compression as
                                         specified in texture profiles
 -tp,--texture-profiles <arg>            DEPRECATED! Use
                                         --texture-compression instead
 -u,--auth <arg>                         User auth token
    --use-async-build-server             DEPRECATED! Asynchronous build is
                                         now the default
    --use-lua-bytecode-delta             Use byte code delta compression
                                         when building for multiple
                                         architectures
    --use-uncompressed-lua-source        Use uncompressed and unencrypted
                                         Lua source code instead of byte
                                         code
    --use-vanilla-lua                    DEPRECATED! Use
                                         --use-uncompressed-lua-source
                                         instead
 -v,--verbose                            Verbose output
    --variant <arg>                      Specify debug, release or
                                         headless version of dmengine
                                         (when bundling)
    --version                            Prints the version number to the
                                         output
    --with-sha1                          Generate (and verify) sha1
                                         signatures from build artifacts
                                         (when bunding for web)
    --with-symbols                       Generate the symbol file (if
                                         applicable)
```

`--texture-compression` è un'opzione senza valore. Includila per attivare la compressione selezionata dai profili delle texture; omettila per disattivare la compressione delle texture. La vecchia forma `--texture-compression=true` è ancora accettata. La vecchia forma `--texture-compression=false` viene ignorata e genera un avviso; al suo posto, ometti l'opzione.

Comandi disponibili:

`clean`
: Elimina i file generati dalla build nella directory di build.

`distclean`
: Elimina tutti i file nella directory di build.

`build`
: Crea la build del grafo delle dipendenze raggiungibile dalle radici di build selezionate. Per impostazione predefinita, la radice è `game.project`; `--build-input` e `--build-input-file` permettono di specificare radici alternative. I file non vengono inclusi nella build per il solo fatto di trovarsi sotto la radice del progetto. Quando `game.project` è una radice di build, aggiungi `--archive` per creare l'archivio dei dati di gioco nella directory di build.

`bundle`
: Crea un bundle di applicazione specifico per la piattaforma. Per creare il bundle è necessario che sia presente un archivio già generato (`build` con l'opzione `--archive`) e che sia specificata una piattaforma di destinazione (con l'opzione `--platform`). Bob crea il bundle nella directory di output, a meno che non venga specificata una directory diversa con l'opzione `--bundle-output`. Il bundle prende il nome dall'impostazione del nome del progetto in *game.project*. L'opzione `--variant` specifica il tipo di eseguibile da generare durante la creazione del bundle e, insieme all'opzione `--strip-executable`, sostituisce l'opzione `--debug`. Se non specifichi `--variant`, ottieni una versione di release del motore (priva di simboli su Android e iOS). Impostando `--variant` su debug e omettendo `--strip-executable`, ottieni lo stesso tipo di eseguibile che in precedenza si otteneva con `--debug`.

`resolve`
: Risolve tutte le dipendenze da librerie esterne.

Piattaforme e architetture disponibili:

`x86_64-macos`
: macOS a 64 bit

`arm64-macos`
: macOS su Apple Silicon (ARM)

`x86_64-win32`
: Windows a 64 bit

`x86-win32`
: Windows a 32 bit

`x86_64-linux`
: Linux a 64 bit

`arm64-linux`
: Linux ARM64 per Raspberry Pi e dispositivi portatili basati su Linux.

`arm64_sim-ios`
: Simulatore iOS su Mac con Apple Silicon. I bundle per il simulatore non usano un’identità di firma né un profilo di provisioning, quindi `--identity` e `--mobileprovisioning` vengono ignorati.

`arm64-ios`
: iOS a 64 bit. Per impostazione predefinita, il valore dell'argomento `--architectures` è `arm64-ios`.

`armv7-android`
: Android con le architetture disponibili `armv7-android` a 32 bit, `arm64-android` a 64 bit e `x86_64-android` a 64 bit. Per impostazione predefinita, il valore dell'argomento `--architectures` è `armv7-android,arm64-android`. L'architettura `x86_64-android` è facoltativa (utile principalmente per emulatori Android, ChromeOS e Windows Subsystem for Android) e deve essere aggiunta esplicitamente.

`wasm-web`
: HTML5 con le architetture disponibili `wasm-web` e `wasm_pthread-web`. Per impostazione predefinita, il valore dell'argomento `--architectures` è `wasm-web`.

Per impostazione predefinita, Bob cerca un progetto nella directory corrente e genera la build delle risorse raggiungibili da `game.project` in *build/default*. Le risorse prive di riferimenti non vengono compilate. Se il codice carica file grezzi tramite il loro percorso durante l'esecuzione, includili tramite l'[impostazione del progetto Custom Resources](/manuals/project-settings/#custom-resources); le altre risorse Defold devono avere un riferimento raggiungibile da una radice di build.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Puoi concatenare più comandi per eseguire una sequenza di operazioni in una sola volta. L'esempio seguente risolve le dipendenze delle librerie, svuota la directory di build, crea l'archivio dei dati e genera il bundle di un'applicazione macOS (denominata *My Game.app*):

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
