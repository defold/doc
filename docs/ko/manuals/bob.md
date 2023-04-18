---
title: Defold manual
---

# Bob the builder
Bob은 에디터 외부에서 Defold 프로젝트를 빌드하기 위한 도구입니다. 이 메뉴얼은 이 도구를 사용하는 방법에 대해 설명합니다.

## Overview
Bob은 데이터를 빌드(에디터에서  **Project ▸ Build And Launch** 선택하는 것에 해당함)하고 압축하고 독립(standalone) 및 배포 가능한 어플리케이션 번들을 생성(에디터에서 **Project ▸ Bundle ▸ \*** 을 선택하는 것에 해당함)할 수 있습니다.

Bob은 빌드에 필요한 모든 것을 포함하는 Java JAR 파일 형식으로 배포됩니다. http://d.defold.com 에서 최신 "bob.jar" 배포본을 찾을 수 있습니다. 원하는 Releases 버전을 선택해서 "bob/bob.jar" 파일을 다운로드 합니다. Bob 도구를 실행하려면 컴퓨터에 Java 8 이 설치되어야 합니다. Javas는 https://www.java.com 에서 다운로드 할 수 있습니다.

## Usage
Bob은 쉘이나 커맨드 라인에서 "java"(또는 Windows에서는 "java.exe") 호출시 bob java 파일을 인수로 넘겨서 실행할 수 있습니다.

```
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
 -br,--build-report <arg>                DEPRECATED in Defold 1.4.6! Use
                                         --build-report-json instead
 -brhtml,--build-report-html <arg>       Filepath where to save a build
                                         report as HTML
 -brjson,--build-report-json <arg>       Filepath where to save a build
                                         report as JSON
    --build-artifacts <arg>              If left out, will default to
                                         build the engine. Choices:
                                         'engine', 'plugins'. Comma
                                         separated list.
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
    --defoldsdk <arg>                    What version of the defold sdk
                                         (sha1) to use
 -e,--email <arg>                        User email
 -ea,--exclude-archive                   Exclude resource archives from
                                         application bundle. Use this to
                                         create an empty Defold
                                         application for use as a build
                                         target
    --exclude-build-folder <arg>         Comma separated list of folders
                                         to exclude from the build
 -h,--help                               This help message
 -i,--input <arg>                        Source directory. Default is
                                         current directory
    --identity <arg>                     Sign identity (iOS)
 -k,--keep-unused                        Keep unused resources in archived
                                         output
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
                                         file. More than one occurrance
                                         are allowed. The settings files
                                         are applied left to right.
    --strip-executable                   Strip the dmengine of debug
                                         symbols (when bundling iOS or
                                         Android)
 -tc,--texture-compression <arg>         Use texture compression as
                                         specified in texture profiles
 -tp,--texture-profiles <arg>            DEPRECATED! Use
                                         --texture-compression instead
 -u,--auth <arg>                         User auth token
    --use-async-build-server             Use an async build process for
                                         the build server (when using
                                         native extensions)
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

### Available commands:

#### clean
빌드 디렉토리에서 빌드된 파일들을 삭제합니다.
#### distclean
빌드 디렉토리에서 모든 파일들을 삭제합니다.
#### build
모든 프로젝트 데이터를 빌드합니다. "--archive" 옵션을 추가해서 압축 파일(빌드 디렉토리의 "game.darc")로 빌드할 수 있습니다.
#### bundle
특정 플랫폼의 어플리케이션 번들을 생성합니다. 번들 작업을 하려면 빌드된 압축 파일("build"에서 "--archive" 옵션을 사용해서)이 있어야 하며 타겟 플랫폼을 지정("--platform" 옵션을 사용해서)해야 합니다. Bob은 "--bundle-output" 옵션을 사용하여 지정된 출력 디렉토리에서 번들을 생성할 수 있습니다. 이 번들은 *game.project*의 프로젝트 이름 설정값에 따라 이름이 정해집니다.
#### resolve
모든 외부 라이브러리 종속성을 처리합니다.

### Available platforms:

#### x86-darwin
macOS
#### x86_64-macos
macOS 64 bit
#### x86-win32
Windows
#### x86-linux
Linux
#### armv7-darwin
iOS
#### armv7-android
Android
#### js-web
HTML5

기본적으로 Bob은 현재 디렉토리에서 빌드할 프로젝트를 찾습니다. 만약 현재 디렉토리를 Defold 프로젝트로 변경하고 bob을 호출하면, 기본 출력 디렉토리인 "build/default" 에서 프로젝트를 빌드합니다.

```
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

한방에 일련의 작업들을 수행하려면 명령들을 함께 나열하면 됩니다. 아래 예제는 라이브러리 종속성을 처리하고, 빌드 디렉토리를 지우고, 번들과 데이터를 macOS용 어플리케이션(이름은 "My Game.app")으로 빌드합니다.

```
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
