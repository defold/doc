---
title: Посібник із засобу збирання проєктів Defold
brief: Bob — це засіб командного рядка для збирання проєктів Defold. У цьому посібнику пояснено, як ним користуватися.
---

# Збирач Bob {#bob-the-builder}

Bob — це засіб командного рядка для збирання проєктів Defold поза звичайним робочим процесом редактора.

Bob може збирати дані (це відповідає кроку збирання після вибору пункту меню редактора <kbd>Project ▸ Build</kbd>), створювати архіви даних і автономні пакети застосунків для розповсюдження (це відповідає параметрам пункту меню редактора <kbd>Project ▸ Bundle ▸ ...</kbd>)

Bob розповсюджується як архів Java _JAR_, що містить усе необхідне для збирання. Найновішу версію *bob.jar* можна знайти на [сторінці випусків GitHub](https://github.com/defold/defold/releases). Виберіть випуск, а потім завантажте *bob/bob.jar*. Для запуску вам знадобиться OpenJDK 25.

Дзеркала сумісних версій OpenJDK 25:
* [OpenJDK 25 від Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 від робочої групи Adoptium](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Якщо ви користуєтеся Windows, завантажте інсталятор OpenJDK у форматі `.msi`.

## Використання {#usage}

Bob запускають з оболонки або командного рядка, викликаючи `java` (або `java.exe` у Windows) і передаючи архів Java для Bob як аргумент:

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

`--texture-compression` — це перемикач без значення. Додайте його, щоб увімкнути стиснення, вибране в профілях текстур; не вказуйте його, щоб вимкнути стиснення текстур. Застарілий запис `--texture-compression=true` досі підтримується. Застарілий запис `--texture-compression=false` ігнорується й спричиняє попередження; натомість не вказуйте перемикач.

Доступні команди:

`clean`
: Видаляє зібрані файли з каталогу збирання.

`distclean`
: Видаляє всі файли з каталогу збирання.

`build`
: Збирає граф залежностей, досяжних із вибраних коренів збирання. За замовчуванням коренем є `game.project`; за допомогою `--build-input` і `--build-input-file` можна вказати інші корені. Файли не збираються лише тому, що розташовані в кореневому каталозі проєкту. Коли `game.project` є коренем збирання, додайте `--archive`, щоб створити архів даних гри в каталозі збирання.

`bundle`
: Створює пакет застосунку для певної платформи. Для пакування потрібні готовий архів (`build` із параметром `--archive`) і вказана цільова платформа (за допомогою параметра `--platform`). Bob створює пакет у каталозі виведення, якщо за допомогою параметра `--bundle-output` не вказано інший каталог. Назва пакета відповідає налаштуванню назви проєкту у файлі *game.project*. Параметр `--variant` визначає тип виконуваного файлу, який буде зібрано під час пакування, і разом із параметром `--strip-executable` замінює параметр `--debug`. Якщо `--variant` не вказано, ви отримаєте версію рушія для випуску (без символів на Android та iOS). Якщо встановити для `--variant` значення debug і не вказувати `--strip-executable`, ви отримаєте той самий тип виконуваного файлу, який раніше створювався з параметром `--debug`.

`resolve`
: Розв’язує всі залежності від зовнішніх бібліотек.

Доступні платформи й архітектури:

`x86_64-macos`
: 64-бітна macOS

`arm64-macos`
: macOS на Apple Silicon (ARM)

`x86_64-win32`
: 64-бітна Windows

`x86-win32`
: 32-бітна Windows

`x86_64-linux`
: 64-бітний Linux

`arm64-linux`
: Linux ARM64 для Raspberry Pi та портативних пристроїв на базі Linux.

`x86_64-ios`
: iOS на 64-бітній macOS (симулятор iOS)

`arm64-ios`
: 64-бітна iOS. За замовчуванням значення аргументу `--architectures` — `arm64-ios`.

`armv7-android`
: Android із доступними 32-бітною архітектурою `armv7-android`, 64-бітною `arm64-android` і 64-бітною `x86_64-android`. За замовчуванням значення аргументу `--architectures` — `armv7-android,arm64-android`. Архітектура `x86_64-android` вмикається за бажанням (переважно корисна для емуляторів Android, ChromeOS і Windows Subsystem for Android), і її потрібно додати явно.

`wasm-web`
: HTML5 із доступними архітектурами `wasm-web` і `wasm_pthread-web`. За замовчуванням значення аргументу `--architectures` — `wasm-web`.

За замовчуванням Bob шукає проєкт у поточному каталозі та збирає ресурси, досяжні з `game.project`, у *build/default*. Ресурси, на які немає посилань, не компілюються. Якщо код під час виконання завантажує необроблені файли за шляхом, додайте їх через [налаштування проєкту Custom Resources](/manuals/project-settings/#custom-resources); для інших ресурсів Defold потрібне посилання, досяжне з кореня збирання.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Ви можете поєднувати команди, щоб виконати послідовність завдань за один запуск. У наведеному нижче прикладі розв’язуються залежності від бібліотек, очищується каталог збирання, збираються дані архіву й пакується застосунок macOS (із назвою *My Game.app*):

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
