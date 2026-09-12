---
title: Den Speicherverbrauch eines Defold-Spiels optimieren
brief: Dieses Handbuch beschreibt, wie du den Speicherverbrauch eines Defold-Spiels optimierst.
---

# Den Speicherverbrauch optimieren {#optimizing-memory-usage}

## Texturkomprimierung {#texture-compression}
Texturkomprimierung verringert nicht nur die Größe der Ressourcen im Archiv deines Spiels. Komprimierte Texturen können auch den benötigten GPU-Speicher reduzieren.

## Dynamisches Laden {#dynamic-loading}
Die meisten Spiele haben zumindest einige Inhalte, die nur selten verwendet werden. Aus Sicht des Speicherverbrauchs ist es nicht sinnvoll, solche Inhalte ständig im Speicher zu halten. Stattdessen solltest du sie bei Bedarf laden und wieder entladen, wenn sie nicht mehr benötigt werden. Dabei musst du natürlich abwägen: Du kannst Inhalte sofort verfügbar halten, was zur Laufzeit Speicher kostet, oder sie bei Bedarf laden, was Ladezeit kostet.

Defold bietet mehrere Möglichkeiten, Inhalte dynamisch zu laden:

* [Sammlungs-Proxys (collection proxies)](/manuals/collection-proxy/)
* [Dynamische Sammlungsfabriken (collection factories)](/manuals/collection-factory/#dynamic-loading-of-factory-resources)
* [Dynamische Fabriken (factories)](/manuals/factory/#dynamic-loading-of-factory-resources)
* [Live Update](/manuals/live-update/)

## Komponentenzähler optimieren {#optimize-component-counters}
Defold reserviert den Speicher für Komponenten (components) und Ressourcen einmalig beim Erstellen einer Sammlung (collection), um die Speicherfragmentierung zu verringern. Die reservierte Speichermenge hängt von der Konfiguration verschiedener Komponentenzähler in *game.project* ab. Verwende den [Profiler](/manuals/profiling/), um die genaue Nutzung von Komponenten und Ressourcen zu ermitteln, und konfiguriere dein Spiel mit Maximalwerten, die näher an der tatsächlichen Anzahl der Komponenten und Ressourcen liegen. Dadurch verringert sich der Speicherverbrauch deines Spiels (siehe die Informationen zur [Optimierung der maximalen Komponentenanzahl](/manuals/project-settings/#component-max-count-optimizations)).

## Anzahl der GUI-Knoten optimieren {#optimize-gui-node-count}
Optimiere die Anzahl der GUI-Knoten (GUI nodes), indem du die maximale Knotenanzahl in der GUI-Datei auf die tatsächlich benötigte Anzahl setzt. Das Feld `Current Nodes` in den [Eigenschaften der GUI-Komponente](https://defold.com/manuals/gui/#gui-properties) zeigt die Anzahl der von der GUI-Komponente verwendeten Knoten an.

:[HTML5 Optimizations](../shared/optimization-memory-html5.md)

