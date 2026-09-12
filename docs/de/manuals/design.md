---
title: Das Design von Defold
brief: Die Philosophie hinter dem Design von Defold
---

# Das Design von Defold {#the-design-of-defold}

Defold wurde mit den folgenden Zielen entwickelt:

- Eine vollständige, professionelle und sofort einsatzbereite Produktionsplattform für Spieleentwicklungsteams zu sein.
- Einfach und klar zu sein und eindeutige Lösungen für häufige Probleme bei der Architektur und den Arbeitsabläufen in der Spieleentwicklung bereitzustellen.
- Eine blitzschnelle Entwicklungsplattform zu sein, die sich ideal für die iterative Spieleentwicklung eignet.
- Zur Laufzeit eine hohe Leistung zu bieten.
- Wirklich plattformübergreifend zu sein.

Editor und Engine sind sorgfältig darauf ausgelegt, diese Ziele zu erreichen. Einige Designentscheidungen des Defold-Teams unterscheiden sich möglicherweise von dem, was du gewohnt bist, wenn du Erfahrung mit anderen Plattformen hast, zum Beispiel:

- Defold erfordert eine statische Deklaration des Ressourcenbaums (resource tree) und aller Namen. Das erfordert anfangs etwas Aufwand von dir, hilft dem Entwicklungsprozess aber auf lange Sicht enorm.
- Das Defold-Team empfiehlt die Nachrichtenübermittlung (message passing) zwischen einfachen, gekapselten Einheiten.
- Es gibt keine objektorientierte Vererbung.
- Die APIs von Defold sind asynchron.
- Die Rendering-Pipeline wird durch Code gesteuert und ist vollständig anpassbar.
- Alle Ressourcendateien von Defold liegen in einfachen Klartextformaten vor, die für Zusammenführungen mit Git sowie für den Import und die Verarbeitung mit externen Werkzeugen optimal strukturiert sind.
- Ressourcen können geändert und per Hot Reload in ein laufendes Spiel geladen werden, was extrem schnelle Iterationen und Experimente ermöglicht.
