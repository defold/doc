---
title: Руководство по сборщику проектов Defold 
brief: Bob - это инструмент командной строки для создания проектов Defold. В этом руководстве объясняется, как использовать инструмент.
---

# Сборщик Bob

Bob - это инструмент командной строки для сборки проектов на Defold вне обычного рабочего процесса в редакторе.

Bob может делать сборки (соответствует этапу сборки при выборе пункта меню редактора <kbd>Project ▸ Build</kbd>), создавать архивы данных и создавать автономные распространяемые бандлы (соответствует пункту меню редактора <kbd> Project ▸ Bundle ▸ ... </kbd>)

Bob распространяется в виде Java _JAR_ архива, содержащего все необходимое для сборки. Вы найдете дистрибутив *bob.jar* последней актуальной версии на [странице загрузки Defold](http://d.defold.com) и на [GitHub странице релизов](https://github.com/defold/defold/releases) . Выберите релиз, затем загрузите *bob/bob.jar*. Чтобы запустить утилиту Bob, вам необходимо [установить на вашем компьютере OpenJDK 11](https://openjdk.java.net/projects/jdk/11/). 

## Применение

Bob запускается из оболочки или из командной строки, вызовом `java` (или` java.exe` в Windows) и передачей файла java-архива утилиты bob в качестве аргумента: 

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
  -a,--archive                       Build archive
 -ar,--architectures <arg>           comma separated list of architectures
                                     to include for the platform, for example
                                     "arm64-android,armv7-android"
  -u,--auth <arg>                    User auth token
     --binary-output <arg>           Location where built engine binary
                                     will be placed. Default is
                                     "<build-output>/<platform>/"
 -br,--build-report <arg>            Filepath where to save a build report
                                     as JSON
 -brhtml,--build-report-html <arg>   Filepath where to save a build report
                                     as HTML
     --build-server <arg>            The build server (when using native
                                     extensions)
 -bo,--bundle-output <arg>           Bundle output directory
     --bundle-format <apk|aab>       Which format to generate Android bundle in
  -d,--debug                         Use debug version of dmengine (when
                                     bundling). Deprecated, use --variant
                                     instead
     --debug-ne-upload               Outputs the files sent to build server as
                                     upload.zip
     --defoldsdk <arg>               What version of the defold sdk (sha1)
                                     to use
     --exclude-build-folder          Comma separated list of folders to exclude
                                     from the build
  -e,--email <arg>                   User email
  -h,--help                          This help message
  -i,--input <arg>                   Source directory. Default is current
                                     directory
     --identity <arg>                Sign identity (iOS)
  -k,--keep-unused                   Keep unused resources in archived
                                     output
     --keystore <arg>                Which keystore file to use when signing the
                                     Android bundle.
     --keystore-pass <arg>           Path to file with keystore password used to
                                     when bundling for Android.
     --keystore-alias <arg>          Name of alias from provided keystore to use
                                     when bundling for Android.
  -l,--liveupdate <arg>              yes if liveupdate content should be
                                     published
 -mp,--mobileprovisioning <arg>      mobileprovisioning profile (iOS)
  -o,--output <arg>                  Output directory. Default is
                                     "build/default"
  -p,--platform <arg>                Platform (when bundling)
  -r,--root <arg>                    Build root directory. Default is
                                     current directory
     --settings <arg>                Path to a game project settings
                                     file. more than one occurrance are
                                     allowed. the settings files are
                                     applied left to right.
     --strip-executable              Strip the dmengine of debug symbols
                                     (when bundling iOS or Android)
 -tc,--texture-compression <arg>     Use texture compression as specified
                                     in texture profiles
 -tp,--texture-profiles <arg>        Use texture profiles (deprecated)
     --use-vanilla-lua               Only ships vanilla source code (i.e.
                                     no byte code)
  -v,--verbose                       Verbose output
     --variant <arg>                 Specify debug, release or headless
                                     version of dmengine (when bundling)
     --version                       Prints the version number to the
                                     output
     --with-symbols                  Generate the symbol file (if
                                     applicable)
```

Доступные команды:

`clean`
: Удалить собранные файлы в каталоге сборки.

`distclean`
: Удалить все файлы в каталоге сборки.

`build`
: Собирает все данные проекта. Добавьте параметр `--archive` для создания файла архива данных («game.darc» в каталоге сборки). 

`bundle`
: Создает бандл под конкретную платформу. Бандлинг требует наличие собранного архива (`билд` с параметром --archive) и указание целевой платформы (ключом `--platform`). Bob создает бандл в каталоге вывода, если другой каталог не указан ключом `--bundle-output`. Бандл будет назван в соответствии с настройкой project name в *game.project*. Ключ `--variant` указывает тип исполняемого файла для сборки при бандлинге и вместе с ключом `--strip-executable` заменяет ключ `--debug`. Если не указан ключ `--variant`, вы получите релизную версию движка (без debug символов для Android и iOS). Установка ключа `--variant` в debug и опускание ключа ` --strip-executable` дает тот же тип исполняемого файла, что и ключ `--debug`. 

`resolve`
: Подтягивание всех зависимостей внешних библиотек. 

Доступные платформы и архитектуры
Available platforms and architectures:

`x86_64-darwin`
: macOS 64 бита 

`x86_64-win32`
: Windows 64 бита

`x86-win32`
: Windows 32 бита

`x86_64-linux`
: Linux 64 бита

`x86_64-ios`
: iOS macOS 64 бита (Эмулятор iOS)

`armv7-darwin`
: iOS с доступной 32-битной архитектурой `armv7-darwin` и 64-битной` arm64-darwin`. По умолчанию значение аргумента `--architectures` - `armv7-darwin,arm64-darwin`. 

`armv7-android`
: Android с доступной 32-битной архитектурой `armv7-android` и 64-битной` arm64-android`. По умолчанию значение аргумента `--architectures` - `armv7-android,arm64-android`. 

`js-web`
: HTML5 с доступными архитектурами `js-web` и `wasm-web`. По умолчанию значение аргумента `--architectures` - `js-web,wasm-web`. 

По умолчанию Bob ищет в текущем каталоге проект, который нужно собрать. Если вы измените текущий каталог на проект Defold и вызовете bob, он соберёт данные для проекта в каталоге вывода по умолчанию *build/default*. 

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Вы можете связывать команды вместе, чтобы выполнить последовательность задач за один раз. В следующем примере выполняются подтягивание библиотек, стирание каталога сборки, сборка данных архива и сборка приложения macOS (с именем *My Game.app*): 

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
