---
title: Manuel de l'outil de build de projets Defold
brief: Bob est un outil en ligne de commande qui permet de compiler des projets Defold. Ce manuel explique comment utiliser cet outil.
---

# Bob, l'outil de build {#bob-the-builder}

Bob est un outil en ligne de commande qui permet de compiler des projets Defold en dehors du flux de travail habituel de l'éditeur.

Bob permet de compiler les données (ce qui correspond à l'étape de build lancée en sélectionnant <kbd>Project ▸ Build</kbd> dans le menu de l'éditeur), de créer des archives de données et de créer des bundles d'application autonomes et distribuables (ce qui correspond aux options du menu <kbd>Project ▸ Bundle ▸ ...</kbd> de l'éditeur)

Bob est distribué sous la forme d'une archive Java _JAR_ contenant tout le nécessaire pour effectuer un build. Vous trouverez la dernière distribution de *bob.jar* sur la [page des versions de GitHub](https://github.com/defold/defold/releases). Sélectionnez une version, puis téléchargez *bob/bob.jar*. Vous aurez besoin d'OpenJDK 25 pour l'exécuter.

Miroirs compatibles d'OpenJDK 25 :
* [OpenJDK 25 de Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 du groupe de travail Adoptium](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Si vous utilisez Windows, choisissez le programme d'installation OpenJDK au format `.msi`.

## Utilisation {#usage}

Bob s'exécute depuis un shell ou en ligne de commande en appelant `java` (ou `java.exe` sous Windows) et en fournissant l'archive Java de Bob en argument :

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

`--texture-compression` est une option sans valeur. Ajoutez-la pour activer la compression sélectionnée par les profils de texture ; omettez-la pour désactiver la compression des textures. L'ancienne forme `--texture-compression=true` est toujours acceptée. L'ancienne forme `--texture-compression=false` est ignorée et produit un avertissement ; omettez plutôt l'option.

Commandes disponibles :

`clean`
: Supprime les fichiers compilés du répertoire de build.

`distclean`
: Supprime tous les fichiers du répertoire de build.

`build`
: Compile le graphe de dépendances accessible à partir des racines de build sélectionnées. Par défaut, la racine est `game.project` ; `--build-input` et `--build-input-file` permettent de spécifier d'autres racines. Les fichiers ne sont pas compilés du seul fait de leur présence sous la racine du projet. Lorsque `game.project` est une racine de build, ajoutez `--archive` pour générer l'archive des données du jeu dans le répertoire de build.

`bundle`
: Crée un bundle d'application propre à une plateforme. La création d'un bundle nécessite la présence d'une archive générée (`build` avec l'option `--archive`) et la spécification d'une plateforme cible (avec l'option `--platform`). Bob crée le bundle dans le répertoire de sortie, sauf si vous spécifiez un autre répertoire avec l'option `--bundle-output`. Le bundle est nommé selon le paramètre de nom du projet dans *game.project*. L'option `--variant` spécifie le type d'exécutable à générer lors de la création du bundle et remplace, avec l'option `--strip-executable`, l'option `--debug`. Si vous ne spécifiez pas `--variant`, vous obtiendrez une version de publication du moteur (sans symboles sur Android et iOS). Définir `--variant` sur debug et omettre `--strip-executable` produit le même type d'exécutable que l'ancienne option `--debug`.

`resolve`
: Résout toutes les dépendances envers des bibliothèques externes.

Plateformes et architectures disponibles :

`x86_64-macos`
: macOS 64 bits

`arm64-macos`
: macOS sur Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bits

`x86-win32`
: Windows 32 bits

`x86_64-linux`
: Linux 64 bits

`arm64-linux`
: Linux ARM64 pour Raspberry Pi et les appareils portables sous Linux.

`arm64_sim-ios`
: Simulateur iOS sur les Mac Apple Silicon. Les bundles pour le simulateur n'utilisent ni identité de signature ni profil de provisionnement ; `--identity` et `--mobileprovisioning` sont donc ignorées.

`arm64-ios`
: iOS 64 bits. Par défaut, la valeur de l'argument `--architectures` est `arm64-ios`.

`armv7-android`
: Android avec les architectures disponibles `armv7-android` 32 bits, `arm64-android` 64 bits et `x86_64-android` 64 bits. Par défaut, la valeur de l'argument `--architectures` est `armv7-android,arm64-android`. L'architecture `x86_64-android` est facultative (principalement utile pour les émulateurs Android, ChromeOS et Windows Subsystem for Android) et doit être ajoutée explicitement.

`wasm-web`
: HTML5 avec les architectures disponibles `wasm-web` et `wasm_pthread-web`. Par défaut, la valeur de l'argument `--architectures` est `wasm-web`.

Par défaut, Bob recherche un projet dans le répertoire courant et compile les ressources accessibles à partir de `game.project` dans *build/default*. Les ressources non référencées ne sont pas compilées. Si le code charge des fichiers bruts à partir de leur chemin à l'exécution, incluez-les au moyen du [paramètre de projet Custom Resources](/manuals/project-settings/#custom-resources) ; les autres ressources Defold nécessitent une référence accessible à partir d'une racine de build.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Vous pouvez enchaîner les commandes pour effectuer une série de tâches en une seule fois. L'exemple suivant résout les bibliothèques, vide le répertoire de build, génère les données de l'archive et crée le bundle d'une application macOS (nommée *My Game.app*) :

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
