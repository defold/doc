---
title: Nativen Code in Defold debuggen
brief: Dieses Handbuch erklärt, wie du nativen Code in Defold debuggst.
---

# Nativen Code debuggen {#debugging-native-code}

Defold ist gut getestet und sollte unter normalen Umständen nur sehr selten abstürzen. Es lässt sich jedoch nicht garantieren, dass es niemals abstürzt, insbesondere wenn dein Spiel native Erweiterungen (native extensions) verwendet. Wenn du Probleme mit Abstürzen oder nativem Code hast, der sich nicht wie erwartet verhält, gibt es verschiedene Vorgehensweisen:

* Einen Debugger verwenden, um den Code schrittweise auszuführen
* Debugging mit Protokollausgaben verwenden
* Ein Absturzprotokoll analysieren
* Einen Aufrufstapel symbolisieren


## Einen Debugger verwenden {#use-a-debugger}

Am häufigsten wird der Code mit einem `Debugger` ausgeführt. Damit kannst du den Code schrittweise ausführen und `Haltepunkte` setzen. Bei einem Absturz hält der Debugger die Ausführung an.

Für jede Plattform gibt es mehrere Debugger.

* Visual studio - Windows
* VSCode - Windows, macOS, Linux
* Android Studio - Windows, macOS, Linux
* Xcode - macOS
* WinDBG - Windows
* lldb / gdb - macOS, Linux, (Windows)
* ios-deploy - macOS

Jedes Werkzeug kann bestimmte Plattformen debuggen:

* Visual studio - Windows + Plattformen, die gdbserver unterstützen (z. B. Linux/Android)
* VSCode - Windows, macOS (lldb), Linux (lldb/gdb) + Plattformen, die gdbserver unterstützen
* Xcode -  macOS, iOS ([mehr erfahren](/manuals/debugging-native-code-ios))
* Android Studio - Android ([mehr erfahren](/manuals/debugging-native-code-android))
* WinDBG - Windows
* lldb/gdb - macOS, Linux, (iOS)
* ios-deploy - iOS (über lldb)


## Debugging mit Protokollausgaben verwenden {#use-print-debugging}

Die einfachste Möglichkeit, deinen nativen Code zu debuggen, ist [Debugging mit Protokollausgaben](http://en.wikipedia.org/wiki/Debugging#Techniques). Verwende die Funktionen im [Namensraum `dmLog`](/ref/stable/dmLog/), um Variablen zu beobachten oder den Ausführungsfluss sichtbar zu machen. Alle Protokollfunktionen geben Meldungen in der Ansicht *Console* im Editor und im [Spielprotokoll](/manuals/debugging-game-and-system-logs) aus.


## Ein Absturzprotokoll analysieren {#analyze-a-crash-log}

Die Defold-Engine speichert bei einem schweren Absturz eine Datei namens `_crash`. Die Absturzdatei enthält Informationen über das System sowie über den Absturz. Die [Ausgabe des Spielprotokolls](/manuals/debugging-game-and-system-logs) gibt an, wo sich die Absturzdatei befindet (dies hängt vom Betriebssystem, dem Gerät und der Anwendung ab).

Du kannst das [crash-Modul](https://www.defold.com/ref/crash/) verwenden, um diese Datei in der nächsten Sitzung zu lesen. Es wird empfohlen, die Datei zu lesen, die Informationen zusammenzutragen, sie auf der Konsole auszugeben und an einen [Analysedienst](/tags/stars/analytics/) zu senden, der das Sammeln von Absturzprotokollen unterstützt.

::: important
Unter Windows wird außerdem eine Datei namens `_crash.dmp` erzeugt. Diese Datei ist beim Debuggen eines Absturzes hilfreich.
:::

### Das Absturzprotokoll von einem Gerät abrufen {#getting-the-crash-log-from-a-device}

Wenn ein Absturz auf einem Mobilgerät auftritt, kannst du die Absturzdatei auf deinen eigenen Computer herunterladen und lokal auswerten.

#### Android

Wenn die App [debuggbar](/manuals/project-settings/#android) ist, kannst du das Absturzprotokoll mit dem [Werkzeug Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb.html) und dem Befehl `adb shell` abrufen:

```
$ adb shell "run-as com.defold.example sh -c 'cat /data/data/com.defold.example/files/_crash'" > ./_crash
```

#### iOS

In iTunes kannst du den Container einer App anzeigen/herunterladen.

Im Fenster `Xcode -> Devices` kannst du auch die Absturzprotokolle auswählen


## Einen Aufrufstapel symbolisieren {#symbolicate-a-callstack}

Wenn du einen Aufrufstapel (call stack) aus einer Datei namens `_crash` oder einer [Protokolldatei](/manuals/debugging-game-and-system-logs) erhältst, kannst du ihn symbolisieren. Dabei wird jede Adresse im Aufrufstapel in einen Dateinamen und eine Zeilennummer umgewandelt, was dabei hilft, die eigentliche Ursache zu finden.

Es ist wichtig, dass du die zum Aufrufstapel passende Engine verwendest. Andernfalls wirst du bei der Fehlersuche sehr wahrscheinlich an der falschen Stelle suchen! Verwende die Option [`--with-symbols`](https://www.defold.com/manuals/bob/), wenn du mit [bob](https://www.defold.com/manuals/bob/) ein Bundle erstellst, oder aktiviere im Dialogfeld zur Bundle-Erstellung im Editor das Kontrollkästchen „Generate debug symbols“:

* iOS - Der Ordner `dmengine.dSYM.zip` in `build/arm64-ios` enthält die Debug-Symbole für iOS-Builds.
* macOS - Der Ordner `dmengine.dSYM.zip` in `build/x86_64-macos` enthält die Debug-Symbole für macOS-Builds.
* Android - Der Ausgabeordner des Bundles `projecttitle.apk.symbols/lib/` enthält die Debug-Symbole für die Zielarchitekturen.
* Linux - Die ausführbare Datei enthält die Debug-Symbole.
* Windows - Die Datei `dmengine.pdb` in `build/x86_64-win32` enthält die Debug-Symbole für Windows-Builds.
* HTML5 - Das Verzeichnis `<project_name>_symbols` neben dem HTML5-Bundle enthält `<project_name>_wasm.js.symbols` und, wenn die Architektur `wasm_pthread-web` ausgewählt ist, `<project_name>_pthread_wasm.js.symbols`.

::: important
Es ist sehr wichtig, dass du die Debug-Symbole für jede öffentliche Veröffentlichung deines Spiels an einem geeigneten Ort speicherst und weißt, zu welcher Veröffentlichung sie gehören. Ohne die Debug-Symbole kannst du keine Abstürze in nativem Code debuggen! Außerdem solltest du eine `unstripped`-Version der Engine aufbewahren. Damit lässt sich der Aufrufstapel bestmöglich symbolisieren.
:::


### Symbole auf Google Play hochladen {#uploading-symbols-to-google-play}
Du kannst [die Debug-Symbole auf Google Play hochladen](https://developer.android.com/studio/build/shrink-code#android_gradle_plugin_version_40_or_earlier_and_other_build_systems), damit alle in Google Play protokollierten Abstürze symbolisierte Aufrufstapel anzeigen. Packe den Inhalt des Ausgabeordners des Bundles `projecttitle.apk.symbols/lib/` in ein ZIP-Archiv. Der Ordner enthält einen oder mehrere Unterordner mit Architekturnamen wie `arm64-v8a`, `armeabi-v7a` und `x86_64`.


### Einen Android-Aufrufstapel symbolisieren {#symbolicate-an-android-callstack}

1. Hole die Engine aus deinem Build-Ordner

```sh
	$ ls <project>/build/<platform>/[lib]dmengine[.exe|.so]
```

2. Entpacke sie in einen Ordner:

```sh
	$ unzip dmengine.apk -d dmengine_1_2_105
```

3. Ermittle die Adresse im Aufrufstapel

	In einem nicht symbolisierten Aufrufstapel könnte sie beispielsweise so aussehen

	`#00 pc 00257224 libmy_game_name.so`

	Dabei ist *`00257224`* die Adresse

4. Löse die Adresse auf

```sh
    $ arm-linux-androideabi-addr2line -C -f -e dmengine_1_2_105/lib/armeabi-v7a/libdmengine.so _address_
```

Hinweis: Wenn du einen Stacktrace aus den [Android-Protokollen](/manuals/debugging-game-and-system-logs) erhältst, kannst du ihn möglicherweise mit [ndk-stack](https://developer.android.com/ndk/guides/ndk-stack.html) symbolisieren

### Einen iOS-Aufrufstapel symbolisieren {#symbolicate-an-ios-callstack}

1. Wenn du native Erweiterungen verwendest, kann der Server dir die Symbole (.dSYM) bereitstellen (übergib `--with-symbols` an bob.jar)

```sh
	$ unzip <project>/build/arm64-darwin/build.zip
	# it will produce a Contents/Resources/DWARF/dmengine
```

2. Wenn du keine nativen Erweiterungen verwendest, lade die Standardsymbole herunter:

```sh
	$ wget http://d.defold.com/archive/<sha1>/engine/arm64-darwin/dmengine.dSYM
```

3. Symbolisiere mit der Ladeadresse

	Aus irgendeinem Grund funktioniert es nicht, nur die Adresse aus dem Aufrufstapel anzugeben (d. h. mit der Ladeadresse 0x0)

```sh
		$ atos -arch arm64 -o Contents/Resources/DWARF/dmengine 0x1492c4
```

	# Neither does specifying the load address directly

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp -l0x100000000 0x1492c4
```

	Es funktioniert, wenn du die Ladeadresse zur Adresse addierst:

```sh
		$ atos -arch arm64 -o MyApp.dSYM/Contents/Resources/DWARF/MyApp 0x1001492c4
		dmCrash::OnCrash(int) (in MyApp) (backtrace_execinfo.cpp:27)
```
