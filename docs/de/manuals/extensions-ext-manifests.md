---
title: Native Erweiterungen - Erweiterungsmanifeste
brief: Dieses Handbuch beschreibt das Erweiterungsmanifest und seinen Zusammenhang mit dem Anwendungsmanifest und dem Engine-Manifest.
---

# Manifestdateien für Erweiterungen, Anwendungen und die Engine {#extension-application-and-engine-manifest-files}

Das Erweiterungsmanifest (extension manifest) ist eine Konfigurationsdatei mit Optionen und Präprozessor-Definitionen, die beim Erstellen eines Builds für eine einzelne Erweiterung verwendet werden. Diese Konfiguration wird mit einer Konfiguration auf Anwendungsebene und einer Basiskonfiguration für die Defold-Engine selbst kombiniert.

## Anwendungsmanifest {#app-manifest}

Das Anwendungsmanifest (application manifest, Dateierweiterung `.appmanifest`) ist eine Konfiguration auf Anwendungsebene, die festlegt, wie dein Spiel auf den Build-Servern erstellt wird. Mit dem Anwendungsmanifest kannst du Teile der Engine entfernen, die du nicht verwendest. Wenn du keine Physik-Engine benötigst, kannst du sie aus der ausführbaren Datei entfernen, um deren Größe zu reduzieren. Wie du ungenutzte Funktionen ausschließt, erfährst du [im Handbuch zum Anwendungsmanifest](/manuals/app-manifest).

## Engine-Manifest

Die Defold-Engine hat ein Build-Manifest (`build.yml`), das in jeder Veröffentlichung der Engine und des Defold-SDK enthalten ist. Das Manifest legt fest, welche SDK-Versionen verwendet werden, welche Compiler, Linker und anderen Werkzeuge ausgeführt werden und welche standardmäßigen Build- und Linker-Optionen an diese Werkzeuge übergeben werden. Du findest das Manifest unter share/extender/build_input.yml [auf GitHub](https://github.com/defold/defold/blob/dev/share/extender/build_input.yml).

## Erweiterungsmanifest {#extension-manifest}

Das Erweiterungsmanifest (`ext.manifest`) hingegen ist eine Konfigurationsdatei speziell für eine Erweiterung. Das Erweiterungsmanifest legt fest, wie der Quellcode der Erweiterung kompiliert und gelinkt wird und welche zusätzlichen Bibliotheken eingebunden werden. 

Die drei verschiedenen Manifestdateien verwenden alle dieselbe Syntax, sodass sie zusammengeführt werden können und vollständig steuern, wie die Erweiterungen und das Spiel erstellt werden.

Für jede Erweiterung, für die ein Build erstellt wird, werden die Manifeste wie folgt kombiniert:

	manifest = merge(game.appmanifest, ext.manifest, build.yml)

Dadurch kannst du das Standardverhalten der Engine und auch jeder Erweiterung überschreiben. Für den abschließenden Link-Vorgang führen wir das Anwendungsmanifest mit dem Defold-Manifest zusammen:

	manifest = merge(game.appmanifest, build.yml)


### Die Datei ext.manifest {#the-extmanifest-file}

Neben dem Namen der Erweiterung kann die Manifestdatei plattformspezifische Kompilieroptionen, Linker-Optionen, Bibliotheken und Frameworks enthalten. Wenn die Datei *ext.manifest* keinen Abschnitt "platforms" enthält oder eine Plattform in der Liste fehlt, wird der Build für die Plattform, für die du ein Bundle erstellst, trotzdem erstellt, jedoch ohne zusätzliche Optionen.

Hier ist ein Beispiel:

```yaml
name: "AdExtension"

platforms:
    arm64-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]

    arm64_sim-ios:
        context:
            frameworks: ["CoreGraphics", "CFNetwork", "GLKit", "CoreMotion", "MessageUI", "MediaPlayer", "StoreKit", "MobileCoreServices", "AdSupport", "AudioToolbox", "AVFoundation", "CoreGraphics", "CoreMedia", "CoreMotion", "CoreTelephony", "CoreVideo", "Foundation", "GLKit", "JavaScriptCore", "MediaPlayer", "MessageUI", "MobileCoreServices", "OpenGLES", "SafariServices", "StoreKit", "SystemConfiguration", "UIKit", "WebKit"]
            flags:      ["-stdlib=libc++"]
            linkFlags:  ["-ObjC"]
            libs:       ["z", "c++", "sqlite3"]
            defines:    ["MY_DEFINE"]
```

#### Zulässige Schlüssel {#allowed-keys}

Die zulässigen Schlüssel für plattformspezifische Kompilieroptionen sind:

* `frameworks` - Apple-Frameworks, die beim Erstellen eines Builds eingebunden werden sollen (iOS und macOS)
* `weakFrameworks` - Apple-Frameworks, die beim Erstellen eines Builds optional eingebunden werden sollen (iOS und macOS)
* `flags` - Optionen, die an den Compiler übergeben werden sollen
* `linkFlags` - Optionen, die an den Linker übergeben werden sollen
* `libs` - Zusätzliche Bibliotheken, die beim Linken eingebunden werden sollen
* `defines` - Präprozessor-Definitionen, die beim Erstellen eines Builds gesetzt werden sollen
* `aaptExtraPackages` - Zusätzlicher Paketname, der generiert werden soll (Android)
* `aaptExcludePackages` - Reguläre Ausdrücke (oder genaue Namen) der auszuschließenden Pakete (Android)
* `aaptExcludeResourceDirs` - Reguläre Ausdrücke (oder genaue Namen) der auszuschließenden Ressourcenverzeichnisse (Android)
* `excludeLibs`, `excludeJars`, `excludeSymbols` - Diese Optionen dienen dazu, zuvor im Plattformkontext definierte Elemente zu entfernen.

Für alle Schlüsselwörter wenden wir einen Filter mit einer Positivliste an. Dadurch sollen unzulässige Pfadoperationen und Zugriffe auf Dateien außerhalb des Upload-Ordners für den Build verhindert werden.
