---
title: Defold proje derleyicisi kılavuzu
brief: Bob, Defold projelerini derlemek için kullanılan bir komut satırı aracıdır. Bu kılavuz aracın nasıl kullanılacağını açıklar.
---

# Derleyici Bob

Bob, Defold projelerini normal düzenleyici iş akışının dışında derlemek (build) için kullanılan bir komut satırı aracıdır.

Bob verileri derleyebilir (düzenleyicideki <kbd>Project ▸ Build</kbd> menü öğesini seçerek yapılan derleme adımına karşılık gelir), veri arşivleri oluşturabilir ve bağımsız uygulama dağıtım paketleri (bundle) hazırlayabilir (düzenleyicideki <kbd>Project ▸ Bundle ▸ ...</kbd> menü öğesinin seçeneklerine karşılık gelir)

Bob, derleme için gereken her şeyi içeren bir Java _JAR_ arşivi olarak dağıtılır. En son *bob.jar* dağıtımını [GitHub Releases sayfasında](https://github.com/defold/defold/releases) bulabilirsiniz. Bir sürüm seçin, ardından *bob/bob.jar* dosyasını indirin. Çalıştırmak için OpenJDK 25 gerekir.

Uyumlu OpenJDK 25 dağıtımlarının indirme adresleri:
* [Microsoft tarafından sunulan OpenJDK 25](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [Adoptium Working Group tarafından sunulan OpenJDK 25](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

Windows kullanıyorsanız OpenJDK için `.msi` kurulum dosyasını seçin.

## Kullanım {#usage}

Bob, bir kabuktan veya komut satırından `java` (Windows'ta `java.exe`) çağrılarak ve Bob Java arşivi bağımsız değişken olarak verilerek çalıştırılır:

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

`--texture-compression`, değer almayan bir anahtardır. Doku profillerinde (texture profile) seçilen sıkıştırmayı etkinleştirmek için bu anahtarı ekleyin; doku sıkıştırmayı devre dışı bırakmak için kullanmayın. Eski `--texture-compression=true` biçimi hâlâ kabul edilir. Eski `--texture-compression=false` biçimi yok sayılır ve bir uyarı üretir; bunun yerine anahtarı hiç kullanmayın.

Kullanılabilir komutlar:

`clean`
: Derleme dizinindeki derlenmiş dosyaları siler.

`distclean`
: Derleme dizinindeki tüm dosyaları siler.

`build`
: Seçilen derleme köklerinden (build root) erişilebilen bağımlılık grafını derler. Varsayılan kök `game.project` dosyasıdır; `--build-input` ve `--build-input-file` alternatif kökler belirtmek için kullanılabilir. Dosyalar, yalnızca projenin kök dizini altında bulundukları için derlenmez. `game.project` bir derleme kökü olduğunda, oyun verisi arşivini derleme dizininde oluşturmak için `--archive` seçeneğini ekleyin.

`bundle`
: Platforma özgü bir uygulama dağıtım paketi oluşturur. Paketleme için derlenmiş bir arşivin bulunması (`build` komutu `--archive` seçeneğiyle çalıştırılarak) ve bir hedef platformun belirtilmesi (`--platform` seçeneğiyle) gerekir. Bob, `--bundle-output` seçeneğiyle farklı bir dizin belirtilmedikçe dağıtım paketini çıktı dizininde oluşturur. Dağıtım paketi, *game.project* dosyasındaki proje adı ayarına göre adlandırılır. `--variant`, paketleme sırasında hangi tür yürütülebilir dosyanın derleneceğini belirtir ve `--strip-executable` seçeneğiyle birlikte `--debug` seçeneğinin yerini alır. `--variant` belirtilmezse motorun yayıma yönelik bir sürümünü elde edersiniz (Android ve iOS'ta sembolleri çıkarılmış olarak). `--variant` değerini debug olarak ayarlayıp `--strip-executable` seçeneğini kullanmamak, `--debug` seçeneğinin eskiden ürettiği türde bir yürütülebilir dosya verir.

`resolve`
: Tüm harici kütüphane bağımlılıklarını çözümler.

Kullanılabilir platformlar ve mimariler:

`x86_64-macos`
: 64 bit macOS

`arm64-macos`
: Apple Silicon (ARM) üzerinde macOS

`x86_64-win32`
: 64 bit Windows

`x86-win32`
: 32 bit Windows

`x86_64-linux`
: 64 bit Linux

`arm64-linux`
: Raspberry Pi ve Linux tabanlı el tipi cihazlar için Linux ARM64.

`arm64_sim-ios`
: Apple Silicon Mac'lerde iOS Simulator. Simülatör dağıtım paketleri bir imzalama kimliği veya sağlama profili kullanmaz, bu nedenle `--identity` ve `--mobileprovisioning` yok sayılır.

`arm64-ios`
: 64 bit iOS. Varsayılan olarak `--architectures` bağımsız değişkeninin değeri `arm64-ios` olur.

`armv7-android`
: 32 bit `armv7-android`, 64 bit `arm64-android` ve 64 bit `x86_64-android` mimarilerinin kullanılabildiği Android. Varsayılan olarak `--architectures` bağımsız değişkeninin değeri `armv7-android,arm64-android` olur. `x86_64-android` mimarisi isteğe bağlıdır (esas olarak Android emülatörleri, ChromeOS ve Windows Subsystem for Android için kullanışlıdır) ve açıkça eklenmesi gerekir.

`wasm-web`
: `wasm-web` ve `wasm_pthread-web` mimarilerinin kullanılabildiği HTML5. Varsayılan olarak `--architectures` bağımsız değişkeninin değeri `wasm-web` olur.

Bob varsayılan olarak geçerli dizinde bir proje arar ve `game.project` dosyasından erişilebilen kaynakları (resource) derleyerek *build/default* dizinine yerleştirir. Başvurusu olmayan kaynaklar derlenmez. Kod, çalışma sırasında ham dosyaları yollarını kullanarak yüklüyorsa bunları [Custom Resources proje ayarı](/manuals/project-settings/#custom-resources) aracılığıyla projeye dahil edin; diğer Defold kaynakları için bir derleme kökünden erişilebilen bir başvuru gerekir.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

Bir dizi görevi tek seferde gerçekleştirmek için komutları art arda yazabilirsiniz. Aşağıdaki örnek kütüphaneleri çözümler, derleme dizinini temizler, arşiv verilerini derler ve (*My Game.app* adlı) bir macOS uygulaması için dağıtım paketi oluşturur:

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
