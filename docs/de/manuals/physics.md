---
title: Physik in Defold
brief: Defold enthält Physik-Engines für 2D und 3D. Damit kannst du Wechselwirkungen nach den Gesetzen der Newtonschen Physik zwischen verschiedenen Arten von Kollisionsobjekten simulieren.
---

# Physik {#physics}

Defold enthält [Box2D](https://box2d.org/) für 2D-Physiksimulationen und Bullet für 3D-Physik. Über die [Einstellung Physics 2D im App Manifest](/manuals/app-manifest/#physics-2d) wählst du **Box2D Version 3**, **Box2D (Legacy Defold version)** oder **None** aus. Die bisherige Implementierung ist der Standard; Box2D 3 musst du ausdrücklich auswählen. Ein Wechsel der Implementierung kann die Simulationsergebnisse verändern und erfordern, dass du die versionsspezifischen [Box2D-Projekteinstellungen](/manuals/project-settings/#box2d) neu abstimmst.

Der komponentenorientierte Arbeitsablauf mit Kollisionsobjekten (collision objects) und das Modul `physics`, die in diesen Handbüchern beschrieben werden, funktionieren mit beiden Box2D-Implementierungen; die Auswahl von **None** entfernt die 2D-Physik. Defold stellt außerdem die APIs [`b2d`](/ref/stable/b2d/), `b2d.body`, `b2d.fixture`, `b2d.shape`, `b2d.joint`, `b2d.chain` und `b2d.world` auf niedrigerer Ebene für den direkten Zugriff auf 2D-Körper, Formen, Gelenke, Ketten und Welten bereit. Nicht jede Funktion auf niedrigerer Ebene ist in beiden Box2D-Implementierungen verfügbar; prüfe in der generierten API-Dokumentation jeder Funktion, ob sie von der im App Manifest ausgewählten Implementierung unterstützt wird.

Die wichtigsten Konzepte der in Defold verwendeten Physik-Engines sind:

* **Kollisionsobjekte** - Ein Kollisionsobjekt ist eine Komponente (component), mit der du einem Spielobjekt (game object) physikalisches Verhalten gibst. Ein Kollisionsobjekt hat physikalische Eigenschaften wie Gewicht, Reibung und Form. [Erfahre, wie du ein Kollisionsobjekt erstellst](/manuals/physics-objects).
* **Kollisionsformen** - Ein Kollisionsobjekt kann entweder mehrere Grundformen oder eine einzelne komplexe Form verwenden, um seine räumliche Ausdehnung zu definieren. [Erfahre, wie du einem Kollisionsobjekt Formen hinzufügst](/manuals/physics-shapes).
* **Kollisionsgruppen** - Alle Kollisionsobjekte müssen einer vordefinierten Gruppe angehören, und jedes Kollisionsobjekt kann eine Liste anderer Gruppen angeben, mit denen es kollidieren kann. [Erfahre, wie du Kollisionsgruppen verwendest](/manuals/physics-groups).
* **Kollisionsnachrichten** - Wenn zwei Kollisionsobjekte kollidieren, sendet die Physik-Engine Nachrichten an die Spielobjekte, zu denen die Komponenten gehören. [Erfahre mehr über Kollisionsnachrichten](/manuals/physics-messages)

Zusätzlich zu den Kollisionsobjekten selbst kannst du auch **Zwangsbedingungen** für Kollisionsobjekte definieren, die meist als **Gelenke** bezeichnet werden. Damit verbindest du zwei Kollisionsobjekte und beschränkst ihre Bewegung oder übst auf andere Weise Kräfte aus, um ihr Verhalten in der Physiksimulation zu beeinflussen. [Erfahre mehr über Gelenke](/manuals/physics-joints).

Du kannst die Physikwelt außerdem entlang eines geraden Strahls untersuchen und auslesen. Das wird als **Strahlabfrage (raycast)** bezeichnet. [Erfahre mehr über Strahlabfragen](/manuals/physics-ray-casts).


## Einheiten der Physiksimulation {#units-used-by-the-physics-engine-simulation}

Die Physik-Engine simuliert Newtonsche Physik und ist darauf ausgelegt, mit den Einheiten Meter, Kilogramm und Sekunde (MKS) gut zu funktionieren. Außerdem ist die Physik-Engine auf bewegliche Objekte mit einer Größe im Bereich von 0,1 bis 10 Metern abgestimmt (statische Objekte können größer sein), und standardmäßig behandelt die Engine 1 Einheit (Pixel) als 1 Meter. Diese Umrechnung zwischen Pixeln und Metern ist auf Simulationsebene praktisch, aus Sicht der Spieleentwicklung aber nicht sehr nützlich. Mit den Standardeinstellungen würde eine Kollisionsform mit einer Größe von 200 Pixeln als 200 Meter groß behandelt. Das liegt weit außerhalb des empfohlenen Bereichs, zumindest für ein bewegliches Objekt.

Im Allgemeinen muss die Physiksimulation skaliert werden, damit sie mit der typischen Größe der Objekte in einem Spiel gut funktioniert. Der Skalierungsfaktor der Physiksimulation lässt sich in *game.project* über die [Einstellung für die Physikskalierung](/manuals/project-settings/#physics) ändern. Wenn du diesen Wert beispielsweise auf 0.02 setzt, werden 200 Pixel als 4 Meter behandelt. Beachte, dass die Schwerkraft (die ebenfalls in *game.project* geändert wird) erhöht werden muss, um die veränderte Skalierung auszugleichen.


## Physikaktualisierungen {#physics-updates}

Es wird empfohlen, die Physik-Engine in regelmäßigen Abständen zu aktualisieren, um eine stabile Simulation sicherzustellen (im Gegensatz zu Aktualisierungen in möglicherweise unregelmäßigen, von der Bildrate abhängigen Abständen). Du kannst die Physik mit einem festen Zeitschritt aktualisieren, indem du die [Einstellung Use Fixed Timestep](/manuals/project-settings/#physics) im Abschnitt Physics der Datei *game.project* aktivierst. Die Aktualisierungsfrequenz wird durch die [Einstellung Fixed Update Frequency](/manuals/project-settings/#engine) im Abschnitt Engine der Datei *game.project* gesteuert. Wenn du für die Physik einen festen Zeitschritt verwendest, wird außerdem empfohlen, über die Lebenszyklusfunktion `fixed_update(self, dt)` mit den Kollisionsobjekten deines Spiels zu interagieren, beispielsweise wenn du Kräfte auf sie ausübst.


## Einschränkungen und häufige Probleme {#caveats-and-common-issues}

Sammlungs-Proxys
: Über Sammlungs-Proxys (collection proxies) kannst du mehr als eine Sammlung (collection) auf oberster Ebene, also eine *Spielwelt*, in die Engine laden. Dabei ist es wichtig zu wissen, dass jede Sammlung auf oberster Ebene eine eigene Physikwelt ist. Physikalische Wechselwirkungen ([Kollisionen, Trigger](/manuals/physics-messages) und [Strahlabfragen](/manuals/physics-ray-casts)) finden nur zwischen Objekten statt, die derselben Welt angehören. Selbst wenn die Kollisionsobjekte zweier Welten optisch genau übereinanderliegen, kann daher keine physikalische Wechselwirkung zwischen ihnen stattfinden.

Kollisionen werden nicht erkannt
: Wenn Kollisionen nicht korrekt behandelt oder erkannt werden, lies den Abschnitt zum [Debugging der Physik im Handbuch zur Fehlersuche](/manuals/debugging-game-logic/#debugging-problems-with-physics).
