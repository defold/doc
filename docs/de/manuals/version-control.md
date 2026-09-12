---
title: Versionsverwaltung
brief: Dieses Handbuch beschreibt, wie du Git mit Defold-Projekten verwendest und lokale Änderungen im Editor überprüfst.
---

# Versionsverwaltung {#version-control}

Defold-Projekte lassen sich gut mit [Git](https://git-scm.com) verwenden, die Synchronisierung erfolgt jedoch außerhalb des Editors. Verwende deinen bevorzugten Git-Client oder die Befehlszeile zum Klonen sowie für fetch, pull, commit, push, das Erstellen von Branches und das Lösen von Konflikten.

## Geänderte Dateien {#changed-files}

Wenn das Projektverzeichnis das Stammverzeichnis eines Git-Worktrees mit mindestens einem Commit ist, listet Defold im Editorbereich *Changed Files* nicht ignorierte Dateien auf, die als hinzugefügt, geändert, gelöscht oder umbenannt erkannt wurden. Defold ermittelt diese Einträge durch einen direkten Vergleich der Dateien auf dem Datenträger mit dem aktuellen Commit (`HEAD`), sodass das Vormerken einer Änderung im Index die Liste nicht verändert. Löse Merge-Konflikte in einem externen Git-Client.

![Geänderte Dateien](images/workflow/changed_files.png)

Wähle genau eine geänderte oder umbenannte Datei aus und klicke auf <kbd>Diff</kbd>, um ihre Textunterschiede anzuzeigen. Klicke auf <kbd>Revert</kbd>, um die ausgewählten Änderungen im Worktree und im Index zu verwerfen. Nachverfolgte Dateien werden auf den Stand von `HEAD` zurückgesetzt; Dateien, die in `HEAD` fehlen, werden gelöscht, unabhängig davon, ob sie als neu hinzugefügte Dateien im Index vorgemerkt sind; bei Umbenennungen wird der neue Pfad gelöscht und der alte Pfad wiederhergestellt. Dies kann im Editor nicht rückgängig gemacht werden. Erstelle daher einen Commit oder eine Sicherungskopie von Arbeit, die du möglicherweise noch benötigst.

## Git

Git speichert die textbasierten Projektdateien von Defold effizient. Häufige Änderungen an großen binären Assets, etwa PSD-Dateien oder Dateien aus der Audioproduktion, können den Verlauf des Repositorys dennoch schnell anwachsen lassen. Ziehe für große Arbeitsdateien Git LFS oder eine separate Speicher- und Sicherungslösung in Betracht.

Der Bereich *Changed Files* bietet ausschließlich lokale Funktionen zum Anzeigen des Status und von Unterschieden sowie zum Verwerfen von Änderungen. Er weiß nicht, ob Commits bereits an ein entferntes Repository übertragen wurden, und führt weder fetch noch pull, commit oder push aus. Führe diese Vorgänge in einem externen Git-Client oder über die Befehlszeile aus. Standardmäßig lädt Defold externe Änderungen neu und aktualisiert den Bereich, sobald die Anwendung wieder den Fokus erhält. Wenn *Load External Changes on App Focus* deaktiviert ist, wähle *File ▸ Load External Changes*.
