---
title: Assets zwischenspeichern
brief: Dieses Handbuch erklärt, wie du mit dem Asset-Cache Builds beschleunigst.
---

# Assets zwischenspeichern {#caching-assets}

Builds von Spielen, die mit Defold erstellt wurden, dauern normalerweise nur wenige Sekunden. Mit der Größe eines Projekts wächst jedoch auch die Anzahl der Assets. Das Kompilieren von Schriftressourcen und das Komprimieren von Texturen kann in einem großen Projekt viel Zeit in Anspruch nehmen. Der Asset-Cache beschleunigt Builds, indem nur geänderte Assets neu erstellt werden. Für unveränderte Assets werden bereits kompilierte Assets aus dem Cache verwendet.

Defold verwendet einen dreistufigen Cache:

1. Projekt-Cache
2. Lokaler Cache
3. Entfernter Cache


## Projekt-Cache {#project-cache}

Defold speichert kompilierte Assets standardmäßig im Ordner `build/default` eines Defold-Projekts zwischen. Der Projekt-Cache beschleunigt nachfolgende Builds, da nur geänderte Assets neu kompiliert werden müssen, während unveränderte Assets aus dem Projekt-Cache verwendet werden. Dieser Cache ist immer aktiviert und wird sowohl vom Editor als auch von den Kommandozeilenwerkzeugen verwendet.

Du kannst den Projekt-Cache manuell löschen, indem du die Dateien in `build/default` löschst oder den Befehl `clean` mit dem [Kommandozeilen-Build-Werkzeug Bob](/manuals/bob) ausführst.


## Lokaler Cache {#local-cache}

Der lokale Cache ist ein optionaler zweiter Cache, in dem kompilierte Assets an einem externen Speicherort auf demselben Computer oder auf einem Netzlaufwerk gespeichert werden. Dank dieses externen Speicherorts bleibt der Inhalt des Caches beim Bereinigen des Projekt-Caches erhalten. Er kann außerdem von mehreren Entwicklern, die am selben Projekt arbeiten, gemeinsam genutzt werden. Der Cache ist derzeit nur verfügbar, wenn du Builds mit den Kommandozeilenwerkzeugen erstellst. Du aktivierst ihn über die Option `resource-cache-local`:

```sh
java -jar bob.jar --resource-cache-local /Users/john.doe/defold_local_cache
```

Auf kompilierte Assets im lokalen Cache wird anhand einer berechneten Prüfsumme zugegriffen. Diese berücksichtigt die Version der Defold-Engine, die Namen und Inhalte der Quell-Assets sowie die Build-Optionen des Projekts. Dadurch wird sichergestellt, dass zwischengespeicherte Assets eindeutig sind und der Cache von mehreren Versionen von Defold gemeinsam genutzt werden kann.

::: sidenote
Dateien im lokalen Cache werden auf unbestimmte Zeit gespeichert. Für das manuelle Entfernen alter oder ungenutzter Dateien bist du selbst verantwortlich.
:::


## Entfernter Cache {#remote-cache}

Der entfernte Cache ist ein optionaler dritter Cache, in dem kompilierte Assets auf einem Server gespeichert werden und auf den über HTTP-Anfragen zugegriffen wird. Der Cache ist derzeit nur verfügbar, wenn du Builds mit den Kommandozeilenwerkzeugen erstellst. Du aktivierst ihn über die Option `resource-cache-remote`:

```sh
java -jar bob.jar --resource-cache-remote http://192.168.0.100/
```

Wie beim lokalen Cache wird auf alle Assets im entfernten Cache anhand einer berechneten Prüfsumme zugegriffen. Der Zugriff auf zwischengespeicherte Assets erfolgt über die HTTP-Anfragemethoden GET, PUT und HEAD. Defold stellt den Server für den entfernten Cache nicht bereit. Du musst ihn selbst einrichten. Ein Beispiel für [einen einfachen Python-Server findest du hier](https://github.com/britzl/httpserver-python).
