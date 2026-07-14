---
title: Defold 프로젝트 빌더 매뉴얼
brief: Bob은 Defold 프로젝트를 빌드하기 위한 커맨드 라인 도구입니다. 이 매뉴얼은 이 도구를 사용하는 방법을 설명합니다.
---

# Bob the builder

Bob은 일반적인 에디터 워크플로우 밖에서 Defold 프로젝트를 빌드하기 위한 커맨드 라인 도구입니다.

Bob은 데이터 빌드(에디터 메뉴 항목 <kbd>Project ▸ Build</kbd>를 선택하는 빌드 단계에 해당), 데이터 아카이브 생성, 그리고 독립 실행 및 배포 가능한 어플리케이션 번들 생성(에디터 메뉴 항목 <kbd>Project ▸ Bundle ▸ ...</kbd> 옵션에 해당)을 할 수 있습니다.

Bob은 빌드에 필요한 모든 것을 포함하는 Java _JAR_ 아카이브로 배포됩니다. 최신 *bob.jar* 배포본은 [GitHub Releases 페이지](https://github.com/defold/defold/releases)에서 찾을 수 있습니다. 릴리스를 선택한 다음 *bob/bob.jar*를 다운로드하세요. 실행하려면 OpenJDK 25가 필요합니다.

호환되는 OpenJDK 25 미러:
* [OpenJDK 25 by Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 by Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Windows를 사용한다면 OpenJDK용 `.msi` 파일 설치 관리자를 사용하면 됩니다.

## 사용법 {#usage}

Bob은 쉘이나 커맨드 라인에서 `java`(Windows에서는 `java.exe`)를 호출하고 bob Java 아카이브를 인자로 제공하여 실행합니다.

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

`--texture-compression`은 값을 받지 않는 스위치입니다. 텍스쳐 프로파일에서 선택한 압축을 활성화하려면 포함하고, 텍스쳐 압축을 비활성화하려면 생략하세요. 이전 형식인 `--texture-compression=true`도 계속 허용됩니다. 이전 형식인 `--texture-compression=false`는 무시되고 경고가 표시되므로, 대신 스위치를 생략하세요.

사용 가능한 명령:

`clean`
: 빌드 디렉토리에서 빌드된 파일을 삭제합니다.

`distclean`
: 빌드 디렉토리의 모든 파일을 삭제합니다.

`build`
: 선택한 빌드 루트에서 도달할 수 있는 종속성 그래프를 빌드합니다. 기본 루트는 `game.project`이며, `--build-input`과 `--build-input-file`로 다른 루트를 지정할 수 있습니다. 파일이 프로젝트 루트 아래에 존재한다는 이유만으로 빌드되지는 않습니다. `game.project`가 빌드 루트일 때 게임 데이터 아카이브를 빌드 디렉토리에 만들려면 `--archive`를 추가하세요.

`bundle`
: 플랫폼별 어플리케이션 번들을 생성합니다. 번들링하려면 빌드된 아카이브(`--archive` 옵션을 사용한 `build`)가 있어야 하며 타겟 플랫폼(`--platform` 옵션 사용)이 지정되어야 합니다. `--bundle-output` 옵션으로 다른 디렉토리를 지정하지 않으면 Bob은 출력 디렉토리에 번들을 생성합니다. 번들 이름은 *game.project*의 프로젝트 이름 설정값에 따라 정해집니다. `--variant`는 번들링할 때 빌드할 실행 파일의 종류를 지정하며, `--strip-executable` 옵션과 함께 `--debug` 옵션을 대체합니다. `--variant`를 지정하지 않으면 엔진의 release 버전(Android와 iOS에서는 심볼이 제거된 버전)을 얻게 됩니다. `--variant`를 debug로 설정하고 `--strip-executable`을 생략하면 예전의 `--debug`와 같은 종류의 실행 파일이 생성됩니다.

`resolve`
: 모든 외부 라이브러리 종속성을 처리합니다.

사용 가능한 플랫폼과 아키텍처:

`x86_64-macos`
: macOS 64 bit

`arm64-macos`
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bit

`x86-win32`
: Windows 32 bit

`x86_64-linux`
: Linux 64 bit

`arm64-linux`
: Raspberry Pi 및 Linux 기반 휴대용 기기용 Linux ARM64

`x86_64-ios`
: iOS macOS 64 bit (iOS Simulator)

`arm64-ios`
: iOS 64 bit. 기본적으로 `--architectures` 인자 값은 `arm64-ios`입니다.

`armv7-android`
: 사용 가능한 32 bit `armv7-android` 및 64 bit `arm64-android` 아키텍처가 있는 Android입니다. 기본적으로 `--architectures` 인자 값은 `armv7-android,arm64-android`입니다.

`wasm-web`
: 사용 가능한 `wasm-web` 및 `wasm_pthread-web` 아키텍처가 있는 HTML5입니다. 기본적으로 `--architectures` 인자 값은 `wasm-web`입니다.

기본적으로 Bob은 현재 디렉토리에서 프로젝트를 찾고, `game.project`에서 도달할 수 있는 리소스를 *build/default*에 빌드합니다. 참조되지 않은 리소스는 컴파일되지 않습니다. 코드가 런타임에 원시 파일을 경로로 로드한다면 [Custom Resources 프로젝트 설정](/manuals/project-settings/#custom-resources)을 통해 포함하세요. 그 밖의 Defold 리소스는 빌드 루트에서 도달할 수 있는 참조가 필요합니다.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

여러 명령을 이어서 한 번에 일련의 작업을 수행할 수 있습니다. 다음 예제는 라이브러리 종속성을 처리하고, 빌드 디렉토리를 비우고, 아카이브 데이터를 빌드한 다음 macOS 어플리케이션(*My Game.app*이라는 이름)을 번들링합니다.

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
