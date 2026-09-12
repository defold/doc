---
title: Refactoring
brief: Dieses Handbuch erklärt, wie du die Struktur deines Projekts mithilfe der leistungsfähigen Refactoring-Funktionen leicht ändern kannst.
---

# Refactoring

Refactoring bezeichnet die Umstrukturierung von vorhandenem Code und Assets. Während der Entwicklung eines Projekts ergibt sich häufig die Notwendigkeit, Dinge zu ändern oder zu verschieben: Namen müssen geändert werden, um Namenskonventionen einzuhalten oder die Verständlichkeit zu verbessern, und Code- oder Asset-Dateien müssen an eine sinnvollere Stelle in der Projekthierarchie verschoben werden.

Defold unterstützt dich beim effizienten Refactoring, indem es nachverfolgt, wie Assets verwendet werden. Referenzen auf Assets, die umbenannt und/oder verschoben werden, aktualisiert Defold automatisch. Bei deiner Entwicklungsarbeit solltest du frei entscheiden können. Dein Projekt hat eine flexible Struktur, die du nach Belieben ändern kannst, ohne befürchten zu müssen, dass alles nicht mehr funktioniert und auseinanderfällt.

::: important
Automatisches Refactoring funktioniert nur, wenn du Änderungen innerhalb des Editors vornimmst. Wenn du eine Datei außerhalb des Editors umbenennst oder verschiebst, werden Referenzen auf diese Datei nicht automatisch geändert.
:::

Wenn du allerdings eine Referenz ungültig machst, indem du beispielsweise ein Asset löschst, kann der Editor das Problem nicht beheben. Er gibt dir aber hilfreiche Hinweise auf Fehler. Wenn du zum Beispiel eine Animation aus einem Atlas löschst und diese Animation irgendwo verwendet wird, meldet Defold einen Fehler, sobald du versuchst, das Spiel zu starten. Der Editor markiert außerdem die Stellen, an denen Fehler auftreten, damit du das Problem schnell finden kannst:

![Refactoring-Fehler](images/workflow/delete_error.png)

Build-Fehler werden im Bereich *Build Errors* am unteren Rand des Editors angezeigt. Ein <kbd>Doppelklick</kbd> auf einen Fehler führt dich zur Stelle, an der das Problem auftritt.
