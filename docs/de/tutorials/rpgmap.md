---
title: Beispiel einer RPG-Karte
brief: In diesem Beispielprojekt lernst du eine Methode kennen, mit der du sehr große RPG-Karten erstellst.
---
# RPG-Karte - Beispielprojekt {#rpg-map-sample-project}

In diesem Beispielprojekt, das du [im Editor öffnen](/manuals/project-setup/) oder [von GitHub herunterladen](https://github.com/defold/sample-rpgmap) kannst, zeigen wir eine Methode zum Erstellen sehr großer RPG-Karten in Defold. Der Entwurf beruht auf den folgenden Annahmen:

1. Die Welt wird Bildschirmabschnitt für Bildschirmabschnitt dargestellt. Dadurch kann das Spiel Gegner und NPC-Figuren auf natürliche Weise innerhalb der Grenzen eines einzelnen Bildschirmabschnitts halten. Der Leveldesigner hat volle Kontrolle darüber, wie die Welt auf dem Bildschirm des Spielers dargestellt wird.
2. Die Spielfigur sollte beliebig weit reisen können, ohne dass im Spiel Probleme mit der Genauigkeit von Gleitkommazahlen auftreten. Diese führen typischerweise dazu, dass Objekte merkwürdig zittern, wenn sie sich weit vom Ursprung entfernen.
3. Die Bewegung des Spielers wird durch Hindernisse auf der Karte eingeschränkt, sodass der Leveldesigner den Spieler mit Bäumen, Felsen, Wasser und anderen Hindernissen zwischen Bildschirmabschnitten führen kann.
4. Es sollte möglich sein, Kachelkarten (tile maps), Sprites und andere visuelle Inhalte miteinander zu kombinieren.

Starte zunächst das Beispiel und durchquere die 3x3 Bildschirmabschnitte große Welt, um ein Gefühl für den Aufbau des Beispiels zu bekommen. Du steuerst die Figur mit den Pfeiltasten.

## Die Hauptsammlung {#the-main-collection}

Öffne "/main/main.collection", um die Startsammlung (bootstrap collection) dieses Beispiels anzusehen.

![](images/rpgmap/main_collection.png)

Diese Sammlung (collection) enthält das Spielobjekt (game object) der Spielfigur, das mit den Pfeiltasten in 8 Richtungen gesteuert wird, sowie ein zweites Spielobjekt namens "game", das den Spielablauf steuert. Das Objekt "game" besteht aus einem Skript und einer Sammlungsfabrik (collection factory) für jeden Bildschirmabschnitt im Spiel. Die Sammlungsfabriken werden nach dem Benennungsschema des Bildschirmabschnittsrasters benannt.

Das Skript "/main/game.script" verfolgt, in welchem Bildschirmabschnitt sich der Spieler gerade befindet. Das Skript reagiert außerdem auf eine benutzerdefinierte Nachricht namens "load_screen". Diese Nachricht lädt einen neuen Bildschirmabschnitt und tauscht ihn in der Bewegungsrichtung des Helden gegen den aktuellen Bildschirmabschnitt aus. Zu Beginn wird ein Bildschirmabschnitt in die Mitte des Bildschirms geladen, und es gibt keinen anderen Bildschirmabschnitt, mit dem er den Platz tauschen könnte.

## Bildschirmabschnitte wechseln {#changing-screens}

Der Held wird durch das Skript "/main/hero.script" gesteuert. Das Skript prüft, ob sich das Spielobjekt des Helden über eine obere, untere, linke oder rechte Linie nahe dem Bildschirmrand hinausbewegt:

![](images/rpgmap/change_screen.png)

1. Wenn sich der Held einem Bildschirmrand weit genug nähert, wird eine Nachricht an das Skript des Objekts "game" gesendet, um den nächsten Bildschirmabschnitt zu laden.
2. Die Sammlung des nächsten Bildschirmabschnitts wird durch den Aufruf von `factory.create()` für die passende collectionfactory-Komponente (component) dynamisch erzeugt. Der Inhalt der Sammlung wird außerhalb des Bildschirms positioniert.
3. Der nächste Bildschirmabschnitt wird in die Mitte des Sichtbereichs gescrollt und der aktuelle Bildschirmabschnitt in die entgegengesetzte Richtung hinausgescrollt. Auch die Spielfigur wird über dieselbe Strecke und mit derselben Geschwindigkeit gescrollt.
4. Der bisherige aktuelle Bildschirmabschnitt, der sich nun außerhalb des Bildschirms befindet, wird gelöscht, und der nächste Bildschirmabschnitt wird zum neuen aktuellen Bildschirmabschnitt.
5. Der Held bewegt sich mit einer Animation in den sichtbaren Bereich des neuen Bildschirmabschnitts, und der Spieler erhält die Kontrolle zurück.

All dies geschieht innerhalb einer Sekunde, sodass der Übergang flüssig ist und den Spielablauf nicht unterbricht.

## Bildschirmabschnitte {#screens}

Jeder Bildschirmabschnitt der Spielwelt wird in einer separaten Sammlung aufgebaut, die die Kachelkarte, das Kollisionsobjekt (collision object) und weitere Spielobjekte enthält, die nur zu diesem Bildschirmabschnitt gehören. Um die Verwaltung und das Laden der Bildschirmabschnitte zu erleichtern, werden ihre Sammlungen nach einem einfachen Schema benannt:

![](images/rpgmap/screens.png)

Jede Sammlung eines Bildschirmabschnitts wird nach ihrer Position im Weltraster benannt. Die erste Zahl ist die X-Position im Raster und die zweite die Y-Position im Raster.

Navigiere in der Ansicht *Assets* zur Sammlung "/main/screens/0-0.collection" und öffne sie. Sie beschreibt den Bildschirmabschnitt in der linken unteren Ecke der Karte:

![](images/rpgmap/screen_collection.png)

Beachte das Spielobjekt namens "root", dem alle Inhalte des Bildschirmabschnitts untergeordnet sind. Dies ist eine weitere Konvention des Beispiels, die einen sehr wichtigen Zweck erfüllt: Wenn ein Bildschirmabschnitt in den sichtbaren Bereich gebracht wird, muss nur das Spielobjekt "root" bewegt werden. Alle untergeordneten Objekte werden automatisch mit dem obersten übergeordneten Objekt mitbewegt. Besondere Spielobjekte in einem Bildschirmabschnitt können ebenfalls frei animiert werden, da ihre Bewegung relativ zu diesem obersten übergeordneten Objekt erfolgt. Wenn der Bildschirmabschnitt hinein- oder hinausgescrollt wird, bewegen sich diese untergeordneten Objekte mit ihm. Spezieller Code ist nur erforderlich, wenn sich ein Objekt zwischen Bildschirmabschnitten bewegen muss.

Die Bienen im Bildschirmabschnitt 0-1 veranschaulichen diese Idee auf einfache Weise:

![](images/rpgmap/bees.png)

## Bildschirmabschnitte im Zusammenhang mit der Welt bearbeiten {#editing-screens-in-the-world-context}

Jeder Bildschirmabschnitt hat eine eigene Kachelkarte, die im integrierten Kachelkarteneditor bearbeitet werden kann. Der größte Nachteil beim isolierten Bearbeiten einzelner Bildschirmabschnitte ist jedoch, dass sich nicht ohne Weiteres erkennen lässt, wie sie an ihre Nachbarabschnitte anschließen. Dies ist ein wichtiger Aspekt, um eine zusammenhängende Spielwelt zu schaffen.

Aus diesem Grund wurde eine besondere Sammlung erstellt. Öffne "/main/map/test_layout.collection", um diese Sammlung mit dem Testlayout der Welt anzusehen:

![](images/rpgmap/test_layout.png)

Diese Sammlung dient ausschließlich als Bearbeitungswerkzeug während der Entwicklung. Wenn du einen bestimmten Bildschirmabschnitt neben der Sammlung mit dem Testlayout bearbeitest, siehst du ihn im Zusammenhang mit seiner Umgebung, und die Bearbeitung ist viel angenehmer:

![](images/rpgmap/side_by_side.png)

Alle Änderungen an der Kachelkarte des Bildschirmabschnitts (hier im rechten Bereich) werden sofort in der Testsammlung (im linken Bereich) angezeigt. Beachte außerdem, dass die Sammlung mit dem Testlayout nicht zur statischen Hierarchie hinzugefügt wird und deshalb automatisch von allen Builds ausgeschlossen ist.

## Zusammenfassung {#summary}

Wie du gesehen hast, wurde dieses Beispiel unter bestimmten Einschränkungen hinsichtlich der Spielwelt und der Bewegung des Helden durch diese Welt aufgebaut. Wenn dein Spiel andere Anforderungen hat, musst du wahrscheinlich eine andere Lösung finden. Soll sich die Kamera in deinem Spiel beispielsweise nahtlos über die Weltkarte bewegen, brauchst du eine andere Aufteilung deiner Inhalte, einen anderen Lademechanismus und auch andere Werkzeuge, die dir beim Erstellen deiner Spielwelt helfen.

Damit endet die Einführung in das Beispiel einer RPG-Karte. Wie immer kannst du die Inhalte des Beispiels nach Belieben verwenden. Wenn du mehr über Defold erfahren möchtest, findest du auf unseren [Dokumentationsseiten](https://defold.com/learn) weitere Beispiele, Tutorials, Handbücher und API-Dokumentation.

Wenn du auf Schwierigkeiten stößt oder Fragen hast, [besuche unser Forum](https://forum.defold.com/).

Viel Spaß mit Defold!
