---
title: Defold project builder manual
brief: Bob is a command line tool for building Defold projects. This manual explains how to use the tool.
---

# Bob the builder

Bob is a command line tool for building Defold projects outside of the normal editor workflow.

Bob is able to build data (corresponding to the build step of selecting the editor menu item <kbd>Project ▸ Build</kbd>), create data archives and create standalone, distributable application bundles (corresponding to the editor menu item <kbd>Project ▸ Bundle ▸ ...</kbd> options)

Bob is distributed as a Java _JAR_ archive containing everything needed to build. You find the latest *bob.jar* distribution on the [GitHub Releases page](https://github.com/defold/defold/releases). Select a release, then download *bob/bob.jar*. You will need OpenJDK 25 to run it.

Compatible OpenJDK 25 mirrors:
* [OpenJDK 25 by Microsoft](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)
* [OpenJDK 25 by Adoptium Working Group](https://github.com/adoptium/temurin25-binaries/releases) / [Adoptium.net](https://adoptium.net/)

If you are on Windows you want the `.msi` file installer for OpenJDK.

## Usage

Bob is run from a shell or from the command line by invoking `java` (or `java.exe` on Windows) and providing the bob java archive as argument:

```text
$ java -jar bob.jar --help
usage: bob [options] [commands]
 -a,--archive                            DEPRECATED! Accepted and ignored
    --all-packages                       Build or bundle Base and all
                                         external packages
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
    --bundle-report-html <arg>           Filepath where to save a standalone
                                         archive package report after bundling
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
    --download-size-report <arg>         Filepath where to save the
                                         estimated Google Play download
                                         size as JSON (Android)
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
 -l,--liveupdate <arg>                   DEPRECATED! Use --all-packages or
                                         --package instead
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
    --package <arg>                      Build or bundle a named package.
                                         May be repeated
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

`--texture-compression` is a switch with no value. Include it to enable the compression selected by the texture profiles; omit it to disable texture compression. The legacy `--texture-compression=true` form is still accepted. The legacy `--texture-compression=false` form is ignored and produces a warning; omit the switch instead.

Available commands:

`clean`
: Delete built files in the build directory.

`distclean`
: Delete all files in the build directory.

`build`
: Compiles resources reachable from the selected build roots and saves their dependency graph as `game.graph.json` in the build output directory. The default root is `game.project`. Use `--build-input` or `--build-input-file` for alternative roots. With an [archive manifest](/manuals/live-update/#archive-manifests), package rules can also select resources. The `build` command produces compiled resources for `bundle` to archive.

`bundle`
: Creates archives from compiled resources and produces a platform-specific application bundle. Specify the target with `--platform`. Bob names the application using the project title and places it in the build output directory, or in the directory given by `--bundle-output`. The engine variant defaults to `release`. Use `--variant debug` for a debug executable. Use `--exclude-archive` for a contentless application.

`resolve`
: Resolve all external library dependencies.

Available platforms and architectures:

`x86_64-macos`
: macOS 64 bit

`arm64-macos`
: macOS Apple Silicon (ARM)

`x86_64-win32`
: Windows 64 bit

`x86_64-linux`
: Linux 64 bit

`arm64-linux`
: Linux ARM64 for Raspberry Pi and Linux-based handheld devices.

`arm64_sim-ios`
: iOS Simulator on Apple Silicon Macs. Simulator bundles do not use a signing identity or provisioning profile, so `--identity` and `--mobileprovisioning` are ignored.

`arm64-ios`
: iOS 64 bit. By default, `--architectures` argument value is `arm64-ios`.

`armv7-android`
: Android with available 32 bit `armv7-android`, 64 bit `arm64-android` and 64 bit `x86_64-android` architectures. By default, `--architectures` argument value is `armv7-android,arm64-android`. The `x86_64-android` architecture is opt-in (mainly useful for Android emulators, ChromeOS and Windows Subsystem for Android) and must be added explicitly.

`wasm-web`
: HTML5 with available `wasm-web` and `wasm_pthread-web` architectures. By default, `--architectures` argument value is `wasm-web`.

By default, Bob looks in the current directory for a project and builds resources reachable from `game.project` into *build/default*. Unreferenced resources are not compiled. If code loads raw files by path at runtime, include them through the [Custom Resources project setting](/manuals/project-settings/#custom-resources); other Defold resources need a reference reachable from a build root.

```sh
$ cd /Applications/Defold-beta/branches/14/4/main
$ java -jar bob.jar
100%
$
```

You can run several commands together. This example resolves libraries, clears the build output, compiles resources, and bundles the macOS application:

```sh
java -jar bob.jar --platform x86_64-macos resolve distclean build bundle
```

### Separate build and bundle stages

Keep the build output directory, including `game.graph.json`, when running the commands in separate processes or CI stages. Use the same project, build output directory, platform, architectures, variant, and compiler settings for both commands. The bundle step reads the current archive manifest and uses the saved graph. Run `build` again when a rule selects resources absent from the graph or when source assets change.

```sh
java -jar bob.jar --platform x86_64-linux build
java -jar bob.jar --platform x86_64-linux --bundle-output dist bundle
```

When using `--experimental-path-minification`, pass it to both commands and keep `minified_paths.json` with the build output. Bob validates the saved mapping and reports when a rebuild is required.

### Selecting archive packages

Use the same selection for `build` and `bundle` when running them separately. See [Live Update](/manuals/live-update/#archive-manifests) for how to define packages.

| Selection | Bundle output |
| --- | --- |
| No selection flags | A self-contained application whose Base includes external-package content. |
| `--all-packages` | An application with the split Base, plus every external package. |
| `--package base` | An application with the split Base only. Startup-required resources stay in Base. |
| `--package common --package halloween` | Only the named external packages. Add `--package base` if you also need the application. |

`--all-packages` takes no value. Use it by itself or repeat `--package <name>` to select packages. `--package` is incompatible with `--all-packages`, `--build-input`, and `--build-input-file`. Selective builds keep other compiled results. Bundling recreates the selected packages and preserves the output of other packages.

`--archive` (`-a`) is deprecated and ignored. `--liveupdate yes` selects all packages and `--liveupdate no` keeps the default selection. Both values emit a deprecation warning. Explicit package selection takes precedence. Projects using legacy Live Update settings can select their external content with `--package liveupdate`.

Use `--bundle-report-html <file>` with `bundle` for the package contents and output sizes. `--build-report-html` and `--build-report-json` report on compiled resources during `build`. See [build and bundle reports](/manuals/profiling/#build-reports).


## Build server

Bob selects the default native extension build server from the release channel of its distribution:

| Bob release channel | Default build server |
|---|---|
| `stable` | `https://build.defold.com` |
| Any other channel, including `beta` and `alpha` | `https://build-stage.defold.com` |

Run `java -jar bob.jar --version` to display the release channel together with Bob's version and build information. The `--variant` option controls the engine build variant and does not change this release channel.

Pass `--build-server <url>` to select a server explicitly, including a [self-hosted Extender server](/manuals/extender-local-setup/). This option overrides the default for every release channel.

## HLSL output in custom shader compiler integrations

Integrations that call Bob's shader compiler pipeline can select plaintext HLSL when a downstream compiler is responsible for producing the final shader binary. This is a compiler API option, not a Bob command-line option. The existing `--debug-output-hlsl` flag selects HLSL output for the build; it does not select plaintext source instead of binary output.

Pass `ShaderCompilePipeline.Options` to the common compiler factory and set `hLSLOutputMode`:

```java
import com.dynamo.bob.Platform;
import com.dynamo.bob.pipeline.Shaderc;
import com.dynamo.bob.pipeline.ShaderCompilers;
import com.dynamo.bob.pipeline.shader.ShaderCompilePipeline;

ShaderCompilePipeline.Options options = new ShaderCompilePipeline.Options();
options.hLSLOutputMode = Shaderc.HLSLOutputMode.HLSL_OUTPUT_MODE_SOURCE;
var compiler = ShaderCompilers.GetCommonShaderCompiler(Platform.X86_64Win32, options);
```

Use the returned compiler through the normal shader build integration. `HLSL_OUTPUT_MODE_BINARY` is the default and retains the normal HLSL binary compilation path. `HLSL_OUTPUT_MODE_SOURCE` skips that binary stage and returns HLSL text for downstream compilation. It also skips binary root-signature generation in the common compiler while preserving vertex/fragment stage interface normalization. The option does not change GLSL, MSL, WGSL or SPIR-V output.

For integrations using the lower-level APIs, set `Shaderc.ShaderCompilerOptions.hLSLOutputMode` in Java or `dmShaderc::ShaderCompilerOptions::m_HLSLOutputMode` in C++. These compiler APIs are part of the engine/build tooling, separate from the runtime extension SDK. Source output still needs downstream compilation before it can replace the binary expected by the DX12 runtime.

See the [shader pipeline options](https://github.com/defold/defold/blob/6cdae55239d20fe3fe6918bf7ffb11aa0917fd4f/com.dynamo.cr/com.dynamo.cr.bob/src/com/dynamo/bob/pipeline/shader/ShaderCompilePipeline.java) and [native compiler options](https://github.com/defold/defold/blob/6cdae55239d20fe3fe6918bf7ffb11aa0917fd4f/engine/shaderc/src/shaderc.h) for the interfaces introduced by this change.
