---
title: Ressourcenverwaltung in Defold
brief: Dieses Handbuch erklärt, wie Defold Ressourcen automatisch verwaltet und wie du das Laden von Ressourcen manuell steuern kannst, um Vorgaben für Speicherbedarf und Bundle-Größe einzuhalten.
---

# Ressourcenverwaltung {#resource-management}

Wenn du ein sehr kleines Spiel entwickelst, bereiten dir die Grenzen der Zielplattform (Speicherbedarf, Bundle-Größe, Rechenleistung und Akkuverbrauch) möglicherweise nie Probleme. Bei größeren Spielen und insbesondere auf tragbaren Geräten gehört der Speicherverbrauch jedoch wahrscheinlich zu den größten Einschränkungen. Ein erfahrenes Team plant die Ressourcenbudgets sorgfältig anhand der Grenzen der Plattform. Defold bietet eine Reihe von Funktionen, mit denen du den Speicherverbrauch und die Bundle-Größe verwalten kannst. Dieses Handbuch gibt einen Überblick über diese Funktionen.

## Der statische Ressourcenbaum {#the-static-resource-tree}

Wenn du einen Build für ein Spiel in Defold erstellst, legst du den Ressourcenbaum statisch fest. Jeder einzelne Teil des Spiels ist mit dem Baum verknüpft, ausgehend von der Startsammlung (bootstrap collection), die üblicherweise "main.collection" heißt. Der Ressourcenbaum folgt jeder Referenz und umfasst alle Ressourcen, die mit diesen Referenzen verbunden sind:

- Daten von Spielobjekten (game objects) und Komponenten (components), etwa Atlanten, Töne usw.
- Prototypen von Fabrikkomponenten (factory components): Spielobjekte und Sammlungen (collections).
- Referenzen von Sammlungs-Proxy-Komponenten (collection proxy components): Sammlungen.
- [Benutzerdefinierte Ressourcen](/manuals/project-settings/#custom-resources), die in *game.project* deklariert sind.

![Ressourcenbaum](images/resource/resource_tree.png)

::: sidenote
Defold kennt außerdem [Bundle-Ressourcen](/manuals/project-settings/#bundle-resources). Bundle-Ressourcen sind im Anwendungs-Bundle enthalten, gehören aber nicht zum Ressourcenbaum. Dabei kann es sich um beliebige Dateien handeln, von plattformspezifischen Hilfsdateien bis hin zu externen Dateien, die [aus dem Dateisystem geladen](/manuals/file-access/#how-to-access-files-bundled-with-the-application) und von deinem Spiel verwendet werden (zum Beispiel FMOD-Soundbanken).
:::

Wenn du ein *Bundle erstellst*, wird nur aufgenommen, was sich im Ressourcenbaum befindet. Alles, auf das im Baum keine Referenz verweist, bleibt außen vor. Du musst nicht manuell auswählen, was in das Bundle aufgenommen oder davon ausgeschlossen werden soll.

Wenn das Spiel *ausgeführt wird*, beginnt die Engine an der Wurzel des Baums, der Startsammlung, und lädt Ressourcen in den Speicher:

- Jede referenzierte Sammlung und ihren Inhalt.
- Spielobjekte und Komponentendaten.
- Prototypen von Fabrikkomponenten (Spielobjekte und Sammlungen).

Die Engine lädt die folgenden Arten referenzierter Ressourcen jedoch nicht automatisch zur Laufzeit:

- Spielweltsammlungen, auf die Sammlungs-Proxys verweisen. Spielwelten sind relativ groß, deshalb musst du ihr Laden und Entladen manuell im Code auslösen. Einzelheiten findest du im [Handbuch zu Sammlungs-Proxys](/manuals/collection-proxy).
- Dateien, die über die Einstellung *Custom Resources* in *game.project* hinzugefügt wurden. Diese Dateien werden manuell mit der Funktion [`sys.load_resource()`](/ref/sys/#sys.load_resource) geladen.

Du kannst das Standardverhalten von Defold beim Erstellen von Bundles und Laden von Ressourcen ändern, um genau zu steuern, wie und wann Ressourcen in den Speicher geladen werden.

![Laden von Ressourcen](images/resource/loading.png)

## Fabrikressourcen dynamisch laden {#dynamically-loading-factory-resources}

Ressourcen, auf die Fabrikkomponenten verweisen, werden normalerweise in den Speicher geladen, wenn die Komponente geladen wird. Die Ressourcen stehen dann zum dynamischen Erzeugen von Objekten im Spiel bereit, sobald die Fabrik (factory) in der Laufzeitumgebung existiert. Um das Standardverhalten zu ändern und das Laden der Fabrikressourcen aufzuschieben, kannst du einfach das Kontrollkästchen *Load Dynamically* der Fabrik aktivieren.

![Dynamisch laden](images/resource/load_dynamically.png)

Wenn dieses Kästchen aktiviert ist, nimmt die Engine die referenzierten Ressourcen weiterhin in das Spiel-Bundle auf, lädt die Fabrikressourcen jedoch nicht automatisch. Stattdessen hast du zwei Möglichkeiten:

1. Rufe [`factory.create()`](/ref/factory/#factory.create) oder [`collectionfactory.create()`](/ref/collectionfactory/#collectionfactory.create) auf, wenn du Objekte dynamisch erzeugen möchtest. Dadurch werden die Ressourcen synchron geladen und anschließend neue Instanzen erzeugt.
2. Rufe [`factory.load()`](/ref/factory/#factory.load) oder [`collectionfactory.load()`](/ref/collectionfactory/#collectionfactory.load) auf, um die Ressourcen asynchron zu laden. Sobald die Ressourcen zum dynamischen Erzeugen von Objekten bereitstehen, wird ein Callback aufgerufen.

Lies das [Handbuch zu Fabriken](/manuals/factory) und das [Handbuch zu Sammlungsfabriken (collection factories)](/manuals/collection-factory), um Einzelheiten zur Funktionsweise zu erfahren.

## Dynamisch geladene Ressourcen entladen {#unloading-dynamically-loaded-resources}

Defold führt Referenzzähler für alle Ressourcen. Wenn der Zähler einer Ressource null erreicht, bedeutet das, dass nichts mehr auf sie verweist. Die Ressource wird dann automatisch aus dem Speicher entladen. Wenn du beispielsweise alle von einer Fabrik erzeugten Objekte und auch das Objekt löschst, das die Fabrikkomponente enthält, werden die Ressourcen aus dem Speicher entladen, auf die die Fabrik zuvor verwiesen hat.

Für Fabriken, bei denen *Load Dynamically* aktiviert ist, kannst du die Funktion [`factory.unload()`](/ref/factory/#factory.unload) oder [`collectionfactory.unload()`](/ref/collectionfactory/#collectionfactory.unload) aufrufen. Dieser Aufruf entfernt die Referenz der Fabrikkomponente auf die Ressource. Wenn nichts anderes auf die Ressource verweist (zum Beispiel, weil alle erzeugten Objekte gelöscht wurden), wird sie aus dem Speicher entladen.

## Ressourcen vom Bundle ausschließen {#excluding-resources-from-bundle}

Mit Sammlungs-Proxys ist es möglich, alle Ressourcen, auf die die Komponente verweist, von der Bundle-Erstellung auszuschließen. Das ist nützlich, wenn du die Bundle-Größe möglichst gering halten musst. Wenn du zum Beispiel Spiele als HTML5 im Web ausführst, lädt der Browser das gesamte Bundle herunter, bevor er das Spiel ausführt.

![Ausschließen](images/resource/exclude.png)

Wenn du bei einem Sammlungs-Proxy *Exclude* aktivierst, wird die referenzierte Ressource nicht in das Spiel-Bundle aufgenommen. Stattdessen kannst du ausgeschlossene Sammlungen in einem ausgewählten Cloud-Speicher ablegen. Das [Handbuch zu Live Update](/manuals/live-update/) erklärt, wie diese Funktion funktioniert.
