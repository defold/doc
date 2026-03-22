---
title: Podręcznik narzędzia Bob do budowania projektów w Defold
brief: Bob to narzędzie wiersza poleceń do budowania projektów w Defold. Ta instrukcja wyjaśnia, jak korzystać z tego narzędzia.
---

# Bob, narzędzie do budowania

Bob to narzędzie wiersza poleceń służące do budowania projektów w Defold poza standardowym przepływem pracy w edytorze.

Bob potrafi budować dane projektu (co odpowiada działaniu <kbd>Project ▸ Build</kbd> w edytorze), tworzyć archiwa danych oraz tworzyć samodzielne, gotowe do dystrybucji pakiety aplikacji (co odpowiada opcjom z menu edytora <kbd>Project ▸ Bundle ▸ ...</kbd>).

Bob jest dystrybuowany jako archiwum Java _JAR_ zawierające wszystko, co potrzebne do budowania. Najnowszą wersję *bob.jar* znajdziesz na [stronie wydań GitHub Releases](https://github.com/defold/defold/releases). Wybierz wydanie, a następnie pobierz *bob/bob.jar*. Jeśli używasz Defold 1.12.0 lub nowszego, do uruchomienia potrzebujesz OpenJDK 25. Dla starszych wersji Defold potrzebujesz OpenJDK 21.

Zgodne dystrybucje OpenJDK 25 (dla Defold 1.12.0 i nowszego):
* [OpenJDK 25 firmy Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 od Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Jeśli korzystasz z systemu Windows, wybierz instalator `.msi` dla OpenJDK.

## Użycie

Bob uruchamia się z powłoki lub z wiersza poleceń, wywołując `java` (lub `java.exe` w Windows) i podając archiwum JAR Boba jako argument:

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
    --manifest-private-key <arg>         Private key to use when signing
                                         manifest and archive.
    --manifest-public-key <arg>          Public key to use when signing
                                         manifest and archive.
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

Dostępne polecenia:

`clean`
: Usuwa pliki wygenerowane w katalogu build.

`distclean`
: Usuwa wszystkie pliki z katalogu build.

`build`
: Buduje wszystkie dane projektu. Dodaj opcję `--archive`, aby zbudować archiwum danych (`game.darc` w katalogu build).

`bundle`
: Tworzy pakiet aplikacji dla konkretnej platformy. Utworzenie pakietu wymaga obecności zbudowanego archiwum (`build` z opcją `--archive`) oraz wskazania platformy docelowej za pomocą opcji `--platform`. Bob tworzy pakiet w katalogu wyjściowym, chyba że podasz inny katalog opcją `--bundle-output`. Nazwa pakietu wynika z ustawienia nazwy projektu w *game.project*. Opcja `--variant` określa, jaki typ pliku wykonywalnego zbudować podczas tworzenia pakietu, a razem z opcją `--strip-executable` zastępuje opcję `--debug`. Jeśli nie podasz `--variant`, otrzymasz wersję `release` silnika, która na Android i iOS jest pozbawiona symboli. Ustawienie `--variant` na `debug` przy pominięciu `--strip-executable` daje ten sam typ pliku wykonywalnego, jaki wcześniej zapewniała opcja `--debug`.

`resolve`
: Rozwiązuje wszystkie zależności bibliotek zewnętrznych.

Dostępne platformy i architektury:

`x86_64-darwin` (Defold 1.3.5 i starsze)
`x86_64-macos` (Defold 1.3.6 i nowsze)
: macOS 64-bit

`arm64-macos` (Defold 1.5.0 i starsze)
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64-bit

`x86-win32`
: Windows 32-bit

`x86_64-linux`
: Linux 64-bit

`x86_64-ios`
: iOS na macOS 64-bit (symulator iOS)

`armv7-darwin` (Defold 1.3.5 i starsze)
`armv7-ios` (Defold 1.3.6 i nowsze)
: iOS z dostępnymi 32-bitowymi architekturami `armv7-darwin` i 64-bitowymi `arm64-darwin`. Domyślnie wartość argumentu `--architectures` to `armv7-darwin,arm64-darwin`.

`armv7-android`
: Android z dostępnymi 32-bitowymi architekturami `armv7-android` i 64-bitowymi `arm64-android`. Domyślnie wartość argumentu `--architectures` to `armv7-android,arm64-android`.

`js-web`
: HTML5 z dostępnymi architekturami `js-web`, `wasm-web` i `wasm_pthread-web`. Domyślnie wartość argumentu `--architectures` to `js-web,wasm-web`.

Domyślnie Bob szuka projektu do zbudowania w bieżącym katalogu. Jeśli przejdziesz do katalogu projektu Defold i uruchomisz Boba, zbuduje dane projektu w domyślnym katalogu wyjściowym *build/default*.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Możesz łączyć polecenia, aby jednym uruchomieniem wykonać sekwencję zadań. W poniższym przykładzie najpierw rozwiązywane są zależności bibliotek, potem czyszczony jest katalog build, budowane jest archiwum danych, a na końcu tworzony jest pakiet aplikacji na macOS (o nazwie *My Game.app*):

```sh
$ java -jar bob.jar --archive --platform x86-darwin resolve distclean build bundle
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
