---
title: Debugging mit ZeroBrane Studio
brief: Dieses Handbuch erklärt, wie du mit ZeroBrane Studio Lua-Code in Defold debuggen kannst.
---

# Lua-Skripte mit ZeroBrane Studio debuggen {#debugging-lua-scripts-with-zerobrane-studio}

Defold enthält einen integrierten Debugger. Du kannst aber auch die kostenlose Open-Source-Lua-IDE _ZeroBrane Studio_ als externen Debugger verwenden. ZeroBrane Studio muss installiert sein, damit du die Debugging-Funktionen nutzen kannst. Das Programm ist plattformübergreifend und läuft sowohl unter macOS als auch unter Windows.

Lade „ZeroBrane Studio“ von http://studio.zerobrane.com herunter

## ZeroBrane konfigurieren {#zerobrane-configuration}

Damit ZeroBrane die Dateien in deinem Projekt findet, musst du den Pfad zu deinem Defold-Projektverzeichnis angeben. Du kannst diesen Pfad bequem ermitteln, indem du bei einer Datei im Stammverzeichnis deines Defold-Projekts die Option <kbd>Show in Desktop</kbd> verwendest.

1. Klicke mit der rechten Maustaste auf *game.project*
2. Wähle <kbd>Show in Desktop</kbd>

![Im Finder anzeigen](images/zerobrane/show_in_desktop.png)

## ZeroBrane einrichten {#to-set-up-zerobrane}

Um ZeroBrane einzurichten, wähle <kbd>Project ▸ Project Directory ▸ Choose...</kbd>:

![Einrichtung](images/zerobrane/setup.png)

Sobald du hier das Verzeichnis deines aktuellen Defold-Projekts eingestellt hast, solltest du den Verzeichnisbaum des Defold-Projekts in ZeroBrane sehen sowie darin navigieren und Dateien öffnen können.

Weitere empfohlene, aber nicht erforderliche Konfigurationsänderungen findest du weiter unten in diesem Dokument.

## Den Debugging-Server starten {#starting-the-debugging-server}

Bevor du eine Debugging-Sitzung beginnst, musst du den in ZeroBrane integrierten Debugging-Server starten. Den Menüeintrag dafür findest du im Menü <kbd>Project</kbd>. Wähle <kbd>Project ▸ Start Debugger Server</kbd>:

![Debugger starten](images/zerobrane/startdebug.png)

## Deine Anwendung mit dem Debugger verbinden {#connecting-your-application-to-the-debugger}

Du kannst das Debugging jederzeit während der Ausführung der Defold-Anwendung starten, musst es aber ausdrücklich aus einem Lua-Skript heraus einleiten. Der Lua-Code zum Starten einer Debugging-Sitzung sieht so aus:

::: sidenote
Wenn sich dein Spiel beim Aufruf von `dbg.start()` beendet, kann das daran liegen, dass ZeroBrane ein Problem erkannt hat und den Befehl zum Beenden an das Spiel sendet. Aus irgendeinem Grund muss in ZeroBrane eine Datei geöffnet sein, damit die Debugging-Sitzung gestartet werden kann. Andernfalls gibt ZeroBrane Folgendes aus:
"Can't start debugging without an opened file or with the current file not being saved 'untitled.lua')."
Öffne in ZeroBrane die Datei, in die du `dbg.start()` eingefügt hast, um diesen Fehler zu beheben.
:::

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start()
```

Wenn du den obigen Code in die Anwendung einfügst, verbindet sie sich mit dem Debugging-Server von ZeroBrane (standardmäßig über "localhost") und hält bei der nächsten auszuführenden Anweisung an.

```txt
Debugger server started at localhost:8172.
Mapped remote request for '/' to '/Users/my_user/Documents/Projects/Defold_project/'.
Debugging session started in '/Users/my_user/Documents/Projects/Defold_project'.
```

Jetzt kannst du die Debugging-Funktionen von ZeroBrane nutzen: Du kannst den Code schrittweise ausführen, Werte untersuchen, Haltepunkte hinzufügen und entfernen usw.

::: sidenote
Das Debugging wird nur für den Lua-Kontext aktiviert, aus dem es gestartet wird. Wenn du "shared_state" in *game.project* aktivierst, kannst du deine gesamte Anwendung debuggen, unabhängig davon, wo du das Debugging gestartet hast.
:::

![Schrittweise Ausführung](images/zerobrane/code.png)

Falls der Verbindungsversuch fehlschlägt (möglicherweise weil der Debugging-Server nicht läuft), läuft deine Anwendung nach dem Verbindungsversuch wie gewohnt weiter.

## Remote-Debugging

Da das Debugging über gewöhnliche Netzwerkverbindungen (TCP) erfolgt, kannst du auch aus der Ferne debuggen. So kannst du deine Anwendung debuggen, während sie auf einem Mobilgerät läuft.

Du musst dazu nur den Befehl ändern, der das Debugging startet. Standardmäßig versucht `start()`, eine Verbindung zu localhost herzustellen. Für das Remote-Debugging musst du jedoch die Adresse des Debugging-Servers von ZeroBrane manuell angeben, etwa so:

```lua
dbg = require "builtins.scripts.mobdebug"
dbg.start("192.168.5.101")
```

Deshalb musst du sicherstellen, dass vom entfernten Gerät aus eine Netzwerkverbindung möglich ist und alle Firewalls oder ähnliche Programme TCP-Verbindungen über Port 8172 zulassen. Andernfalls kann die Anwendung beim Start hängen bleiben, wenn sie versucht, eine Verbindung zu deinem Debugging-Server herzustellen.

## Weitere empfohlene ZeroBrane-Einstellung {#other-recommended-zerobrane-setting}

Du kannst ZeroBrane so einstellen, dass es während des Debuggings Lua-Skriptdateien automatisch öffnet. Dadurch kannst du in Funktionen in anderen Quelldateien einsteigen, ohne diese Dateien manuell öffnen zu müssen.

Öffne zunächst die Konfigurationsdatei des Editors. Es wird empfohlen, die benutzerspezifische Version dieser Datei zu ändern.

- Wähle <kbd>Edit ▸ Preferences ▸ Settings: User</kbd>
- Füge Folgendes zur Konfigurationsdatei hinzu:

  ```txt
  - to automatically open files requested during debugging
  editor.autoactivate = true
  ```

- Starte ZeroBrane neu

![Weitere empfohlene Einstellungen](images/zerobrane/otherrecommended.png)
