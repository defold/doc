---
title: Debugging - Spiel- und Systemprotokolle
brief: Dieses Handbuch erklärt, wie du Spiel- und Systemprotokolle liest.
---

# Spiel- und Systemprotokoll {#game-and-system-log}

Das Spielprotokoll zeigt alle Ausgaben der Engine, nativer Erweiterungen (native extensions) und deiner Spiellogik an. Mit den Befehlen [print()](/ref/stable/base/#print:...) und [pprint()](/ref/stable/builtins/?q=pprint#pprint:v) kannst du aus deinen Skripten und Lua-Modulen Informationen im Spielprotokoll anzeigen. Mit den Funktionen im [Namensraum `dmLog`](/ref/stable/dmLog/) kannst du aus nativen Erweiterungen in das Spielprotokoll schreiben. Das Spielprotokoll kannst du im Editor, in einem Terminalfenster, mit plattformspezifischen Werkzeugen oder aus einer Protokolldatei lesen.

Systemprotokolle werden vom Betriebssystem erzeugt und können zusätzliche Informationen liefern, die dir helfen, ein Problem einzugrenzen. Die Systemprotokolle können Stacktraces zu Abstürzen und Warnungen bei knappem Arbeitsspeicher enthalten.

::: important
Die Protokollierung in der Konsole bzw. auf dem Bildschirm zeigt nur in Debug-Builds Informationen an. In Release-Builds ist das Konsolenprotokoll leer. Du kannst die Dateiprotokollierung für Release-Builds jedoch aktivieren, indem du die Projekteinstellung „Write Log File“ auf „Always“ setzt. Einzelheiten findest du weiter unten.
:::

## Das Spielprotokoll im Editor lesen {#reading-the-game-log-from-the-editor}

Wenn du dein Spiel lokal aus dem Editor oder über eine Verbindung zur [mobilen Entwicklungs-App](/manuals/dev-app) ausführst, werden alle Ausgaben im Konsolenbereich des Editors angezeigt:

![Editor 2](images/editor/editor2_overview.png)

## Das Spielprotokoll im Terminal lesen {#reading-the-game-log-from-the-terminal}

Wenn du ein Defold-Spiel aus dem Terminal startest, wird das Protokoll direkt im Terminalfenster angezeigt. Unter Windows und Linux gibst du den Namen der ausführbaren Datei im Terminal ein, um das Spiel zu starten. Unter macOS musst du die Engine aus der .app-Datei heraus starten:

```
$ > ./mygame.app/Contents/MacOS/mygame
```

## Spiel- und Systemprotokolle mit plattformspezifischen Werkzeugen lesen {#reading-game-and-system-logs-using-platform-specific-tools}

### HTML5

Du kannst Protokolle mit den Entwicklerwerkzeugen lesen, die die meisten Browser bereitstellen.

* [Chrome](https://developers.google.com/web/tools/chrome-devtools/console) - Menu > More Tools > Developer Tools
* [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) - Tools > Web Developer > Web Console
* [Edge](https://docs.microsoft.com/en-us/microsoft-edge/devtools-guide/console)
* [Safari](https://support.apple.com/guide/safari-developer/log-messages-with-the-console-dev4e7dedc90/mac) - Develop > Show JavaScript Console

### Android

Mit dem Werkzeug Android Debug Bridge (ADB) kannst du das Spiel- und Systemprotokoll anzeigen.

:[Android ADB](../shared/android-adb.md)

Verbinde nach der Installation und Einrichtung dein Gerät per USB, öffne ein Terminal und führe Folgendes aus:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat
```

Das Gerät gibt dann sämtliche Ausgaben einschließlich der Ausgaben des Spiels im aktuellen Terminal aus.

Wenn du nur die Ausgaben der Defold-Anwendung sehen möchtest, verwende diesen Befehl:

```txt
$ cd <path_to_android_sdk>/platform-tools/
$ adb logcat -s defold
--------- beginning of /dev/log/system
--------- beginning of /dev/log/main
I/defold  ( 6210): INFO:ENGINE: Defold Engine 1.2.50 (8d1b912)
I/defold  ( 6210): INFO:ENGINE: Loading data from:
I/defold  ( 6210): INFO:ENGINE: Initialized sound device 'default'
I/defold  ( 6210):
D/defold  ( 6210): DEBUG:SCRIPT: Hello there, log!
...
```

### iOS

Unter iOS hast du mehrere Möglichkeiten, Spiel- und Systemprotokolle zu lesen:

1. Du kannst das [Werkzeug Console](https://support.apple.com/guide/console/welcome/mac) verwenden, um das Spiel- und Systemprotokoll zu lesen.
2. Du kannst den LLDB-Debugger mit einem Spiel verbinden, das auf einem Gerät läuft. Um ein Spiel zu debuggen, muss es mit einem „Apple Developer Provisioning Profile“ signiert sein, das das Gerät einschließt, auf dem du debuggen möchtest. Erstelle im Editor ein Bundle des Spiels und gib das Bereitstellungsprofil im Dialogfeld für die Bundle-Erstellung an (die Bundle-Erstellung für iOS ist nur unter macOS verfügbar).

Um das Spiel zu starten und den Debugger damit zu verbinden, benötigst du ein Werkzeug namens [ios-deploy](https://github.com/phonegap/ios-deploy). Installiere und debugge dein Spiel, indem du Folgendes in einem Terminal ausführst:

```txt
$ ios-deploy --debug --bundle <path_to_game.app> # NOTE: not the .ipa file
```

Dadurch wird die App auf deinem Gerät installiert und gestartet, und ein LLDB-Debugger wird automatisch mit ihr verbunden. Wenn du LLDB noch nicht kennst, lies [Erste Schritte mit LLDB](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html).


## Das Spielprotokoll aus der Protokolldatei lesen {#reading-the-game-log-from-the-log-file}

Mit der Projekteinstellung „Write Log File“ in *game.project* steuerst du die Dateiprotokollierung:

- „Never“: Keine Protokolldatei schreiben.
- „Debug“: Nur für Debug-Builds eine Protokolldatei schreiben.
- „Always“: Sowohl für Debug- als auch für Release-Builds eine Protokolldatei schreiben.

Wenn die Dateiprotokollierung aktiviert ist, werden alle Spielausgaben in eine Datei namens „`log.txt`“ auf dem Datenträger geschrieben. So extrahierst du die Datei, wenn du das Spiel auf einem Gerät ausführst:

iOS
: Verbinde dein Gerät mit einem Computer, auf dem macOS und Xcode installiert sind.

  Öffne Xcode und gehe zu <kbd>Window ▸ Devices and Simulators</kbd>.

  Wähle dein Gerät in der Liste aus und wähle dann die entsprechende App in der Liste *Installed Apps* aus.

  Klicke auf das Zahnradsymbol unter der Liste und wähle <kbd>Download Container...</kbd>.

  ![Container herunterladen](images/debugging/download_container.png)

  Sobald der Container extrahiert wurde, wird er im *Finder* angezeigt. Klicke mit der rechten Maustaste auf den Container und wähle <kbd>Show Package Content</kbd>. Suche die Datei „`log.txt`“, die sich in „`AppData/Documents/`“ befinden sollte.

Android(
: Ob du die Datei „`log.txt`“ extrahieren kannst, hängt von der Betriebssystemversion und dem Hersteller ab. Hier findest du eine kurze und einfache [Schritt-für-Schritt-Anleitung](https://stackoverflow.com/a/48077004/129360).
