---
title: Manual do construtor de projetos do Defold
brief: Bob é uma ferramenta de linha de comando para compilar projetos Defold. Este manual explica como usar a ferramenta.
---

# Bob the builder

Bob é uma ferramenta de linha de comando para compilar projetos Defold fora do fluxo normal de trabalho do editor.

Bob é capaz de compilar dados (correspondendo à etapa de build de selecionar o item de menu do editor <kbd>Projeto ▸ Compilar</kbd>), criar arquivos de dados e criar pacotes de aplicação independentes e distribuíveis (correspondendo às opções do item de menu do editor <kbd>Projeto ▸ Empacotar ▸ ...</kbd>).

Bob é distribuído como um arquivo Java _JAR_ contendo tudo o que é necessário para compilar. Você encontra a distribuição mais recente de *bob.jar* na [página GitHub Releases](https://github.com/defold/defold/releases). Selecione uma release e baixe *bob/bob.jar*. Se estiver usando Defold 1.12.0 ou mais recente, você precisará do OpenJDK 25 para executá-lo. Para versões mais antigas do Defold, você precisará do OpenJDK 21.

Mirrors compatíveis do OpenJDK 25 (a partir do Defold 1.12.0):
* [OpenJDK 25 by Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 by Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

No Windows, use o instalador `.msi` do OpenJDK.

## Uso

Bob é executado a partir de um shell ou da linha de comando chamando `java` (ou `java.exe` no Windows) e fornecendo o arquivo Java do Bob como argumento:

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

Comandos disponíveis:

`clean`
: Exclui os arquivos gerados no diretório de build.

`distclean`
: Exclui todos os arquivos no diretório de build.

`build`
: Compila todos os dados do projeto. Adicione a opção `--archive` para gerar um arquivo de dados ("`game.darc`" no diretório de build).

`bundle`
: Cria um pacote de aplicação específico para uma plataforma. O empacotamento exige que um arquivo já tenha sido gerado (`build` com a opção `--archive`) e que uma plataforma-alvo seja especificada (com a opção `--platform`). Bob cria o pacote no diretório de saída, a menos que um diretório diferente seja especificado com a opção `--bundle-output`. O pacote é nomeado de acordo com a configuração de nome do projeto em *game.project*. A opção `--variant` especifica qual tipo de executável compilar durante o empacotamento e, junto com a opção `--strip-executable`, substitui a opção `--debug`. Se nenhum `--variant` for especificado, você receberá uma versão release da engine (com símbolos removidos no Android e iOS). Definir `--variant` como debug e omitir `--strip-executable` produz o mesmo tipo de executável que `--debug` produzia antes.

`resolve`
: Resolve todas as dependências de bibliotecas externas.

Plataformas e arquiteturas disponíveis:

`x86_64-darwin` (Defold 1.3.5 e anterior)
`x86_64-macos` (Defold 1.3.6 e mais recente)
: macOS 64 bit

`arm64-macos` (Defold 1.5.0 e anterior)
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bit

`x86-win32`
: Windows 32 bit

`x86_64-linux`
: Linux 64 bit

`x86_64-ios`
: iOS macOS 64 bit (iOS Simulator)

`armv7-darwin` (Defold 1.3.5 e anterior)
`armv7-ios` (Defold 1.3.6 e mais recente)
: iOS com arquiteturas disponíveis de 32 bits `armv7-darwin` e 64 bits `arm64-darwin`. Por padrão, o valor do argumento `--architectures` é `armv7-darwin,arm64-darwin`.

`armv7-android`
: Android com arquiteturas disponíveis de 32 bits `armv7-android` e 64 bits `arm64-android`. Por padrão, o valor do argumento `--architectures` é `armv7-android,arm64-android`.

`js-web`
: HTML5 com arquiteturas disponíveis `js-web`, `wasm-web` e `wasm_pthread-web`. Por padrão, o valor do argumento `--architectures` é `js-web,wasm-web`.

Por padrão, Bob procura no diretório atual por um projeto para compilar. Se você mudar o diretório atual para um projeto Defold e chamar Bob, ele compila os dados do projeto no diretório de saída padrão *build/default*.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Você pode encadear comandos para executar uma sequência de tarefas de uma só vez. O exemplo a seguir resolve bibliotecas, limpa o diretório de build, compila dados de arquivo e empacota uma aplicação macOS (chamada *My Game.app*):

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
