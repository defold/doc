---
title: Offline arbeiten
brief: Dieses Handbuch beschreibt, wie du in Projekten mit Abhängigkeiten und insbesondere nativen Erweiterungen offline arbeitest.
---

# Offline arbeiten {#working-offline}

Defold benötigt in den meisten Fällen keine Internetverbindung, um zu funktionieren. In einigen Situationen ist jedoch eine Internetverbindung erforderlich:

* Automatische Updates
* Probleme melden
* Abhängigkeiten herunterladen
* Builds für native Erweiterungen erstellen


## Automatische Updates {#automatic-updates}

Defold prüft regelmäßig, ob neue Updates verfügbar sind. Dazu fragt Defold die [offizielle Download-Seite](https://d.defold.com) ab. Wenn ein Update gefunden wird, wird es automatisch heruntergeladen.

Wenn du nur zeitweise eine Internetverbindung hast und nicht warten möchtest, bis das automatische Update startet, kannst du neue Versionen von Defold manuell von der [offiziellen Download-Seite](https://d.defold.com) herunterladen.


## Probleme melden {#reporting-issues}

Wenn im Editor ein Problem erkannt wird, kannst du es an die Problemverwaltung von Defold melden. Die Problemverwaltung wird [auf GitHub gehostet](https://www.github.com/defold/editor2-issues), sodass du eine Internetverbindung benötigst, um das Problem zu melden.

Wenn du offline auf ein Problem stößt, kannst du es später manuell über die [Option Report Issue im Menü Help](/manuals/getting-help/#report-a-problem-from-the-editor) des Editors melden.


## Abhängigkeiten herunterladen {#fetching-dependencies}

Defold unterstützt ein System, mit dem Entwickler Code und Assets über sogenannte [Bibliotheksprojekte (Library Projects)](/manuals/libraries/) teilen können. Bibliotheken sind ZIP-Dateien, die überall im Internet gehostet werden können. Du findest Defold-Bibliotheksprojekte üblicherweise auf GitHub und in anderen Online-Repositorys für Quellcode.

Du kannst eine Bibliothek als [Projektabhängigkeit in den Projekteinstellungen](/manuals/project-settings/#dependencies) hinzufügen. Abhängigkeiten werden heruntergeladen oder aktualisiert, wenn das Projekt geöffnet wird oder wenn du die Option *Fetch Libraries* im Menü *Project* auswählst.

Wenn du offline und in mehreren Projekten arbeiten musst, kannst du Abhängigkeiten im Voraus herunterladen und sie anschließend über einen lokalen Server gemeinsam nutzen. Abhängigkeiten auf GitHub findest du üblicherweise auf der Registerkarte Releases des Projekt-Repositorys:

![URL einer Bibliothek auf GitHub](images/libraries/libraries_library_url_github.png)

Mit Python kannst du ganz einfach einen lokalen Server erstellen:

    python -m SimpleHTTPServer

Dadurch wird im aktuellen Verzeichnis ein Server erstellt, der Dateien unter `localhost:8000` bereitstellt. Wenn das aktuelle Verzeichnis heruntergeladene Abhängigkeiten enthält, kannst du sie deiner Datei *game.project* hinzufügen:

    http://localhost:8000/extension-fbinstant-4.1.1.zip


## Builds für native Erweiterungen erstellen {#building-native-extensions}

Defold unterstützt ein System namens [native Erweiterungen (Native Extensions)](/manuals/extensions/), mit dem Entwickler nativen Code hinzufügen können, um die Funktionalität der Engine zu erweitern. Mit einer cloudbasierten Build-Lösung ermöglicht Defold den Einstieg in native Erweiterungen ohne Einrichtungsaufwand.

Wenn du zum ersten Mal einen Build eines Projekts erstellst und das Projekt eine native Erweiterung enthält, wird der native Code auf den Build-Servern von Defold zu einer angepassten Game-Engine von Defold kompiliert und an deinen PC zurückgesendet. Die angepasste Engine wird in deinem Projekt zwischengespeichert und für nachfolgende Builds wiederverwendet, solange du keine nativen Erweiterungen hinzufügst, entfernst oder änderst und den Editor nicht aktualisierst.

Wenn du offline arbeiten musst und dein Projekt native Erweiterungen enthält, musst du sicherstellen, dass du mindestens einmal erfolgreich einen Build erstellst, damit dein Projekt eine zwischengespeicherte Kopie der angepassten Engine enthält.
