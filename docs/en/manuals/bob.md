---
title: Defold project builder manual
brief: Bob is a command line tool for building Defold projects. This manual explains how to use the tool.
---

# Bob the builder

Bob is a command line tool for building Defold projects outside of the normal editor workflow.

Bob is able to build data (corresponding to the build step of selecting the editor menu item <kbd>Project ▸ Build</kbd>), create data archives and create standalone, distributable application bundles (corresponding to the editor menu item <kbd>Project ▸ Bundle ▸ ...</kbd> options)

Bob is distributed as a Java _JAR_ archive containing everything needed to build. You find the latest *bob.jar* distribution on the [Defold Download page](http://d.defold.com) and the [GitHub Releases page](https://github.com/defold/defold/releases). Select a release, then download *bob/bob.jar*. To run the Bob tool, you need [OpenJDK 11 installed on your computer](https://openjdk.java.net/projects/jdk/11/).

## Usage

Bob is run from a shell or from the command line by invoking `java` (or `java.exe` on Windows) and providing the bob java archive as argument:

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
 -a,--archive                        Build archive
 -ar,--architectures <arg>           comma separated list of architectures
                                     to include for the platform, for example "arm64-android,armv7-android"
    --binary-output <arg>            Location where built engine binary
                                     will be placed. Default is
                                     "<build-output>/<platform>/"
 -bo,--bundle-output <arg>           Bundle output directory
 -br,--build-report <arg>            Filepath where to save a build report
                                     as JSON
 -brhtml,--build-report-html <arg>   Filepath where to save a build report
                                     as HTML
    --build-server <arg>             The build server (when using native
                                     extensions)
 -d,--debug                          Use debug version of dmengine (when
                                     bundling). Deprecated, use --variant
                                     instead
    --defoldsdk <arg>                What version of the defold sdk (sha1)
                                     to use
 -e,--email <arg>                    User email
 -h,--help                           This help message
 -i,--input <arg>                    Source directory. Default is current
                                     directory
    --identity <arg>                 Sign identity (iOS)
 -k,--keep-unused                    Keep unused resources in archived
                                     output
 -l,--liveupdate <arg>               yes if liveupdate content should be
                                     published
 -mp,--mobileprovisioning <arg>      mobileprovisioning profile (iOS)
 -o,--output <arg>                   Output directory. Default is
                                     "build/default"
 -p,--platform <arg>                 Platform (when bundling)
 -r,--root <arg>                     Build root directory. Default is
                                     current directory
    --settings <arg>                 a path to a game project settings
                                     file. more than one occurrance are
                                     allowed. the settings files are
                                     applied left to right.
    --strip-executable               Strip the dmengine of debug symbols
                                     (when bundling iOS or Android)
 -tc,--texture-compression <arg>     Use texture compression as specified
                                     in texture profiles
 -tp,--texture-profiles <arg>        Use texture profiles (deprecated)
 -u,--auth <arg>                     User auth token
    --use-vanilla-lua                Only ships vanilla source code (i.e.
                                     no byte code)
 -v,--verbose                        Verbose output
    --variant <arg>                  Specify debug, release or headless
                                     version of dmengine (when bundling)
    --version                        Prints the version number to the
                                     output
    --with-symbols                   Generate the symbol file (if
                                     applicable)
    --bundle-format <apk|aab>        Which format to generate Android bundle in.
    --keystore <arg>                 Which keystore file to use when signing the
                                     Android bundle.
    --keystore-pass <arg>            Path to file with keystore password used to
                                     when bundling for Android.
    --keystore-alias <arg>           Name of alias from provided keystore to use
                                     when bundling for Android.
```

Available commands:

`clean`
: Delete built files in the build directory.

`distclean`
: Delete all files in the build directory.

`build`
: Builds all project data. Add the `--archive` option to build a data archive file ("game.darc" in the build directory).

`bundle`
: Creates a platform specific application bundle. Bundling requires that a built archive is present (`build` with the `--archive` option) and that a target platform is specified (with the `--platform` option). Bob creates the bundle in the output directory unless a different directory is specified with the `--bundle-output` option. The bundle is named according to the project name setting in *game.project*. The `--variant` specifies which type of executable to build when bundling and it together with the `--strip-executable` option replaces the `--debug` option. If no `--variant` is specified you will get a release version of the engine (stripped of symbols on Android and iOS). Setting `--variant` to debug and omitting `--strip-executable` yields the same type of executable as `--debug` used to do.

`resolve`
: Resolve all external library dependencies.

Available platforms and architectures:

`x86_64-darwin`
: macOS 64 bit

`x86_64-win32`
: Windows 64 bit

`x86-win32`
: Windows 32 bit

`x86_64-linux`
: Linux 64 bit

`x86_64-ios`
: iOS macOS 64 bit (iOS Simulator)

`armv7-darwin`
: iOS with available 32-bit `armv7-darwin` and 64-bit `arm64-darwin` architectures. By default, `--architectures` argument value is `armv7-darwin,arm64-darwin`.

`armv7-android`
: Android with available 32 bit `armv7-android` and 64 bit `arm64-android` architectures. By default, `--architectures` argument value is `armv7-android,arm64-android`.

`js-web` : HTML5 with available `js-web` and `wasm-web` architectures. By default, `--architectures` argument value is `js-web,wasm-web`.

By default, Bob looks in the current directory for a project to build. If you change the current dir to a Defold project and invoke bob, it builds the data for the project in the default output directory *build/default*.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

You can string commands together to perform a sequence of tasks in one go. The following example resolves libraries, wipes the build directory, builds archive data and bundles a macOS application (named *My Game.app*):

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
