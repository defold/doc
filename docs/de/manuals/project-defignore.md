---
title: Ignorieren von Dateien in Defold-Projekten
brief: Dieses Handbuch beschreibt, wie du Dateien und Ordner in Defold ignorierst.
---

# Dateien ignorieren {#ignoring-files}

Du kannst den Defold-Editor und die Werkzeuge so konfigurieren, dass sie Dateien und Ordner in einem Projekt ignorieren. Das kann nützlich sein, wenn das Projekt Dateien enthält, deren Dateierweiterungen mit den von Defold verwendeten Dateierweiterungen in Konflikt stehen. Ein Beispiel dafür sind Dateien der Programmiersprache Go mit der Dateierweiterung `.go`, die der Editor auch für Dateien für Spielobjekte (game objects) verwendet.

## Die Datei `.defignore` {#the-defignore-file}
Die auszuschließenden Dateien und Ordner werden in einer Datei namens `.defignore` im Stammverzeichnis des Projekts festgelegt. Die Datei sollte die auszuschließenden Dateien und Ordner mit jeweils einem Eintrag pro Zeile auflisten. Beispiel:

```
/path/to/file.png
/otherpath
```

Dadurch werden die Datei `/path/to/file.png` und alle Inhalte unter dem Pfad `/otherpath` ausgeschlossen.

## Die Datei `.defunload` {#the-defunload-file}

Bei bestimmten großen Projekten, die mehrere voneinander unabhängige Module enthalten, möchtest du möglicherweise Teile vom Laden ausschließen, um den Speicherverbrauch und die Ladezeiten im Editor zu verringern. Dazu kannst du die Pfade, die vom Laden ausgeschlossen werden sollen, in einer Datei namens `.defunload` unterhalb des Projektverzeichnisses auflisten.

Einfach gesagt ermöglicht dir die Datei `.defunload`, Teile des Projekts im Editor auszublenden, ohne dass Referenzen auf die ausgeblendeten Ressourcen einen Build-Fehler verursachen.

Für die Muster in `.defunload` gelten dieselben Regeln wie für die Datei `.defignore`. Entladene Sammlungen (collections) und Spielobjekte verhalten sich so, als wären sie leer, wenn geladene Ressourcen sie referenzieren. Andere Ressourcen, die den Mustern in `.defunload` entsprechen, befinden sich in einem entladenen Zustand und können im Editor nicht angezeigt werden. Wenn jedoch eine geladene Ressource von ihnen abhängt, werden die entladenen Ressourcen und ihre Abhängigkeiten automatisch geladen.

Wenn beispielsweise ein Sprite von Bildern in einem Atlas abhängt, müssen wir den Atlas laden, sonst wird das fehlende Bild als Fehler gemeldet. In diesem Fall warnt dich eine Benachrichtigung vor dieser Situation und gibt an, welche entladene Ressource von welcher Stelle aus referenziert wurde.

Der Editor verhindert, dass du von geladenen Ressourcen aus Referenzen auf `.defunloaded`-Ressourcen hinzufügst. Daher tritt diese Situation nur auf, wenn Ressourcen von der Festplatte gelesen werden.

Im Gegensatz zur Datei `.defignore` musst du den Editor nach dem Bearbeiten der Datei `.defunload` neu starten, damit die Änderungen wirksam werden.
