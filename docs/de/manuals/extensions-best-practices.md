---
title: Native Erweiterungen - Bewährte Vorgehensweisen
brief: Dieses Handbuch beschreibt bewährte Vorgehensweisen bei der Entwicklung nativer Erweiterungen.
---

# Bewährte Vorgehensweisen {#best-practices}

Plattformübergreifenden Code zu schreiben kann schwierig sein. Es gibt jedoch einige Möglichkeiten, sowohl die Entwicklung als auch die Wartung solchen Codes zu erleichtern.


## Projektstruktur {#project-structure}

Beim Erstellen einer nativen Erweiterung (native extension) gibt es einige Dinge, die sowohl bei der Entwicklung als auch bei der Wartung helfen.

### Lua-API

Es sollte nur eine Lua-API und eine Implementierung davon geben. Dadurch lässt sich auf allen Plattformen wesentlich leichter dasselbe Verhalten erreichen.

Wenn die betreffende Plattform die Erweiterung nicht unterstützen soll, empfiehlt es sich, überhaupt kein Lua-Modul zu registrieren. So kannst du die Unterstützung erkennen, indem du auf `nil` prüfst:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Ordnerstruktur {#folder-structure}

Die folgende Ordnerstruktur wird häufig für Erweiterungen verwendet:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

Beachte, dass `myextension.mm` und `myextension_android.cpp` nur benötigt werden, wenn du spezielle native Aufrufe für die jeweilige Plattform ausführst.

#### Plattformordner {#platform-folders}

An bestimmten Stellen wird die Plattformarchitektur als Ordnername verwendet, um festzulegen, welche Dateien beim Kompilieren und bei der Bundle-Erstellung der Anwendung verwendet werden. Diese Namen haben die Form:

    <architecture>-<platform>

Die aktuelle Liste lautet:

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Lege plattformspezifische Bibliotheken also beispielsweise hier ab:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Nativen Code schreiben {#writing-native-code}

Im Defold-Quellcode wird C++ sehr sparsam eingesetzt, und der Großteil des Codes ähnelt stark C. Abgesehen von einigen Containerklassen gibt es kaum Templates, da sie sowohl die Kompilierungszeiten als auch die Größe der ausführbaren Datei erhöhen.

### C++-Version

Beim Erstellen der Kern-Engine verwendet das Defold-Team C++11, unter Windows jedoch C++14. Konsolen-Builds erfordern inzwischen im Allgemeinen C++14 oder neuer.

Für native Erweiterungen verwendet das Defold-Team keine festgelegte C++-Version, sondern verlässt sich auf die Standardversion der Toolchain der jeweiligen Plattform.

Der Defold-Quellcode vermeidet die neuesten Sprachmerkmale oder Versionen von C++. Das liegt vor allem daran, dass neue Sprachmerkmale beim Entwickeln einer Game-Engine nicht benötigt werden. Außerdem ist es zeitaufwendig, die neuesten Sprachmerkmale von C++ zu verfolgen, und sie wirklich zu beherrschen erfordert viel wertvolle Zeit.

Für die Entwicklung von Erweiterungen hat dies den zusätzlichen Vorteil, dass Defold eine stabile ABI beibehält. Beachte auch, dass die Verwendung der neuesten C++-Sprachmerkmale aufgrund unterschiedlicher Unterstützung verhindern kann, dass der Code auf verschiedenen Plattformen kompiliert werden kann.

### Keine C++-Ausnahmen {#no-c-exceptions}

Defold verwendet in der Engine keine Ausnahmen. In Game-Engines werden Ausnahmen im Allgemeinen vermieden, da die Daten während der Entwicklung bereits größtenteils bekannt sind. Das Entfernen der Unterstützung für C++-Ausnahmen verringert die Größe der ausführbaren Datei und verbessert die Leistung zur Laufzeit.

### Standard-Template-Bibliotheken - STL {#standard-template-libraries-stl}

Da die Defold-Engine abgesehen von einigen Algorithmen und mathematischen Funktionen (`std::sort`, `std::upper_bound` usw.) keinen STL-Code verwendet, kann die Verwendung von STL in deiner Erweiterung funktionieren.

Bedenke auch hier, dass ABI-Inkompatibilitäten Probleme verursachen können, wenn du deine Erweiterung zusammen mit anderen Erweiterungen oder Bibliotheken von Drittanbietern verwendest.

Der Verzicht auf die STL-Bibliotheken, die stark auf Templates setzen, verkürzt außerdem die Build-Zeiten von Defold und verringert vor allem die Größe der ausführbaren Datei.

#### Zeichenfolgen {#strings}

In der Defold-Engine wird `const char*` anstelle von `std::string` verwendet. Die Verwendung von `std::string` ist eine häufige Fehlerquelle, wenn verschiedene C++-Versionen oder Compilerversionen kombiniert werden, da dies zu einer ABI-Inkompatibilität führen kann. Die Verwendung von `const char*` und einigen Hilfsfunktionen vermeidet dieses Problem.

### Funktionen verbergen {#make-functions-hidden}

Verwende nach Möglichkeit das Schlüsselwort `static` für Funktionen, die nur innerhalb deiner Kompilierungseinheit verwendet werden. Dadurch kann der Compiler einige Optimierungen vornehmen, die sowohl die Leistung verbessern als auch die Größe der ausführbaren Datei verringern können.

## Bibliotheken von Drittanbietern {#3rd-party-libraries}

Berücksichtige bei der Auswahl einer Bibliothek von Drittanbietern unabhängig von der Sprache Folgendes:

* Funktionalität - Löst sie dein konkretes Problem?
* Leistung - Verursacht sie Leistungseinbußen zur Laufzeit?
* Bibliotheksgröße - Um wie viel größer wird die endgültige ausführbare Datei? Ist das akzeptabel?
* Abhängigkeiten - Benötigt sie zusätzliche Bibliotheken?
* Unterstützung - In welchem Zustand befindet sich die Bibliothek? Hat sie viele offene Issues? Wird sie noch gepflegt?
* Lizenz - Darfst du sie für dieses Projekt verwenden?


## Open-Source-Abhängigkeiten {#open-source-dependencies}

Stelle immer sicher, dass du Zugriff auf deine Abhängigkeiten hast. Wenn du beispielsweise von etwas auf GitHub abhängig bist, gibt es nichts, was verhindert, dass das Repository entfernt wird oder sich plötzlich seine Ausrichtung oder seine Eigentümerschaft ändert. Du kannst dieses Risiko verringern, indem du einen Fork des Repositorys erstellst und diesen anstelle des Ursprungsprojekts verwendest.

Denke daran, dass der Code der Bibliothek in dein Spiel eingebunden wird. Stelle also sicher, dass die Bibliothek genau das tut, was sie tun soll, und nichts darüber hinaus!
