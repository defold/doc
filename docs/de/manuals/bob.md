---
title: Handbuch zum Erstellen von Defold-Projekten
brief: Bob ist ein Kommandozeilenwerkzeug zum Erstellen von Builds für Defold-Projekte. Dieses Handbuch erklärt, wie du das Werkzeug verwendest.
---

# Bob, der Baumeister {#bob-the-builder}

Bob ist ein Kommandozeilenwerkzeug, mit dem du Builds von Defold-Projekten außerhalb des üblichen Arbeitsablaufs im Editor erstellen kannst.

Bob kann Builds der Daten erstellen (entspricht dem Build-Schritt beim Auswählen des Editor-Menüeintrags <kbd>Project ▸ Build</kbd>), Datenarchive erzeugen und eigenständige, verteilbare Anwendungsbundles erstellen (entspricht den Optionen unter dem Editor-Menüeintrag <kbd>Project ▸ Bundle ▸ ...</kbd>)

Bob wird als Java-_JAR_-Archiv bereitgestellt, das alles enthält, was für einen Build benötigt wird. Die neueste Version von *bob.jar* findest du auf der [GitHub-Seite mit den Releases](https://github.com/defold/defold/releases). Wähle ein Release aus und lade dann *bob/bob.jar* herunter. Zum Ausführen benötigst du OpenJDK 25.

Kompatible Bezugsquellen für OpenJDK 25:
* [OpenJDK 25 von Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 von der Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Unter Windows benötigst du das Installationsprogramm für OpenJDK als `.msi`-Datei.

## Verwendung {#usage}

Du führst Bob in einer Shell oder über die Kommandozeile aus, indem du `java` (unter Windows `java.exe`) aufrufst und das Java-Archiv von Bob als Argument übergibst:

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

`--texture-compression` ist ein Schalter ohne Wert. Gib ihn an, um die in den Texturprofilen (texture profiles) gewählte Komprimierung zu aktivieren; lasse ihn weg, um die Texturkomprimierung zu deaktivieren. Die ältere Form `--texture-compression=true` wird weiterhin akzeptiert. Die ältere Form `--texture-compression=false` wird ignoriert und erzeugt eine Warnung; lasse stattdessen den Schalter weg.

Verfügbare Befehle:

`clean`
: Löscht die beim Build erstellten Dateien im Build-Verzeichnis.

`distclean`
: Löscht alle Dateien im Build-Verzeichnis.

`build`
: Erstellt einen Build für den Abhängigkeitsgraphen, der von den ausgewählten Ausgangspunkten für den Build aus erreichbar ist. Standardmäßig ist der Ausgangspunkt `game.project`; mit `--build-input` und `--build-input-file` kannst du alternative Ausgangspunkte angeben. Dateien werden nicht allein deshalb in den Build einbezogen, weil sie unterhalb des Projektstammverzeichnisses liegen. Wenn `game.project` ein Ausgangspunkt für den Build ist, füge `--archive` hinzu, um das Spieldatenarchiv im Build-Verzeichnis zu erstellen.

`bundle`
: Erstellt ein plattformspezifisches Anwendungsbundle. Die Bundle-Erstellung setzt voraus, dass ein erstelltes Archiv vorhanden ist (`build` mit der Option `--archive`) und eine Zielplattform angegeben wird (mit der Option `--platform`). Bob erstellt das Bundle im Ausgabeverzeichnis, sofern du mit der Option `--bundle-output` kein anderes Verzeichnis angibst. Das Bundle wird entsprechend der Einstellung für den Projektnamen in *game.project* benannt. Mit der Option `--variant` legst du fest, welcher Typ ausführbarer Datei bei der Bundle-Erstellung erzeugt wird. Zusammen mit der Option `--strip-executable` ersetzt sie die Option `--debug`. Wenn du `--variant` nicht angibst, erhältst du eine Release-Version der Engine (unter Android und iOS ohne Symbole). Wenn du `--variant` auf debug setzt und `--strip-executable` weglässt, erhältst du denselben Typ ausführbarer Datei wie früher mit `--debug`.

`resolve`
: Löst alle Abhängigkeiten von externen Bibliotheken auf.

Verfügbare Plattformen und Architekturen:

`x86_64-macos`
: macOS mit 64 Bit

`arm64-macos`
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows mit 64 Bit

`x86-win32`
: Windows mit 32 Bit

`x86_64-linux`
: Linux mit 64 Bit

`arm64-linux`
: Linux ARM64 für Raspberry Pi und Handheld-Geräte mit Linux.

`arm64_sim-ios`
: iOS Simulator auf Macs mit Apple Silicon. Simulator-Bundles verwenden weder eine Signierungsidentität noch ein Bereitstellungsprofil, daher werden `--identity` und `--mobileprovisioning` ignoriert.

`arm64-ios`
: iOS mit 64 Bit. Standardmäßig ist der Wert des Arguments `--architectures` auf `arm64-ios` gesetzt.

`armv7-android`
: Android mit den verfügbaren Architekturen `armv7-android` mit 32 Bit, `arm64-android` mit 64 Bit und `x86_64-android` mit 64 Bit. Standardmäßig ist der Wert des Arguments `--architectures` auf `armv7-android,arm64-android` gesetzt. Die Architektur `x86_64-android` ist optional (vor allem für Android-Emulatoren, ChromeOS und Windows Subsystem for Android nützlich) und muss ausdrücklich hinzugefügt werden.

`wasm-web`
: HTML5 mit den verfügbaren Architekturen `wasm-web` und `wasm_pthread-web`. Standardmäßig ist der Wert des Arguments `--architectures` auf `wasm-web` gesetzt.

Standardmäßig sucht Bob im aktuellen Verzeichnis nach einem Projekt und erstellt einen Build der von `game.project` aus erreichbaren Ressourcen (resources) in *build/default*. Nicht referenzierte Ressourcen werden nicht kompiliert. Wenn dein Code zur Laufzeit Rohdateien über ihren Pfad lädt, binde sie über die [Projekteinstellung Custom Resources](/manuals/project-settings/#custom-resources) ein; andere Defold-Ressourcen benötigen eine Referenz, die von einem Ausgangspunkt für den Build aus erreichbar ist.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Du kannst Befehle aneinanderreihen, um mehrere Aufgaben nacheinander in einem Durchgang auszuführen. Das folgende Beispiel löst Bibliotheksabhängigkeiten auf, leert das Build-Verzeichnis, erstellt die Archivdaten und erzeugt ein Bundle für eine macOS-Anwendung (mit dem Namen *My Game.app*):

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
