---
title: Die Bausteine von Defold
brief: Dieses Handbuch erklärt im Detail, wie Spielobjekte, Komponenten und Sammlungen funktionieren.
---

#  Bausteine {#building-blocks}

Der Aufbau von Defold beruht auf einigen Konzepten, die du gut verstehen solltest. Dieses Handbuch erklärt, woraus die Bausteine von Defold bestehen. Lies anschließend das [Handbuch zur Adressierung](/manuals/addressing) und das [Handbuch zur Nachrichtenübermittlung](/manuals/message-passing). Außerdem stehen dir direkt im Editor eine Reihe von [Tutorials](/tutorials/getting-started) zur Verfügung, die dir einen schnellen Einstieg ermöglichen.

![Bausteine](images/building_blocks/building_blocks.png)

Es gibt drei grundlegende Arten von Bausteinen, mit denen du ein Defold-Spiel aufbaust:

Sammlung
: Eine Sammlung (collection) ist eine Datei, mit der du dein Spiel strukturierst. In Sammlungen baust du Hierarchien aus Spielobjekten (game objects) und weiteren Sammlungen auf. Üblicherweise strukturierst du damit Spiellevels, Gegnergruppen oder Figuren, die aus mehreren Spielobjekten bestehen.

Spielobjekt
: Ein Spielobjekt ist ein Container mit einem Bezeichner (ID), einer Position, einer Drehung und einer Skalierung. Es dient dazu, Komponenten (components) aufzunehmen. Spielobjekte werden üblicherweise verwendet, um Spielfiguren, Geschosse, das Regelsystem des Spiels oder eine Funktion zum Laden von Levels zu erstellen.

Komponente
: Komponenten sind Einheiten, die du in Spielobjekte einfügst, um ihnen im Spiel eine visuelle, akustische und/oder logische Darstellung zu geben. Üblicherweise erstellst du damit Sprites für Figuren und Skriptdateien oder fügst Soundeffekte oder Partikeleffekte hinzu.

## Sammlungen {#collections}

Sammlungen sind Baumstrukturen, die Spielobjekte und weitere Sammlungen enthalten. Eine Sammlung wird immer in einer Datei gespeichert.

Beim Start lädt die Defold-Engine eine einzelne _Startsammlung (bootstrap collection)_, die in der Einstellungsdatei *game.project* festgelegt ist. Die Startsammlung heißt häufig "main.collection", du kannst aber jeden beliebigen Namen verwenden.

Eine Sammlung kann Spielobjekte und weitere Sammlungen enthalten, die als Referenz auf die Datei der jeweiligen Untersammlung eingebunden sind. Du kannst sie beliebig tief verschachteln. Hier siehst du eine Beispieldatei namens "main.collection". Sie enthält ein Spielobjekt (mit der ID "can") und eine Untersammlung (mit der ID "bean"). Die Untersammlung enthält wiederum zwei Spielobjekte: "bean" und "shield".

![Sammlung](images/building_blocks/collection.png)

Beachte, dass die Untersammlung mit der ID "bean" in einer eigenen Datei namens "/main/bean.collection" gespeichert ist und in "main.collection" lediglich referenziert wird:

![Sammlung bean](images/building_blocks/bean_collection.png)

Du kannst Sammlungen selbst nicht adressieren, da es zur Laufzeit keine Objekte gibt, die den Sammlungen "main" und "bean" entsprechen. Manchmal musst du jedoch den Bezeichner einer Sammlung als Teil des _Pfads_ zu einem Spielobjekt verwenden (Einzelheiten findest du im [Handbuch zur Adressierung](/manuals/addressing)):

```lua
-- file: can.script
-- get position of the "bean" game object in the "bean" collection
local pos = go.get_position("bean/bean")
```

Eine Sammlung wird einer anderen Sammlung immer als Referenz auf eine Sammlungsdatei hinzugefügt:

Führe einen <kbd>Rechtsklick</kbd> auf die Sammlung in der Ansicht *Outline* aus und wähle <kbd>Add Collection File</kbd>.

## Spielobjekte {#game-objects}

Spielobjekte sind einfache Objekte, die während der Ausführung deines Spiels jeweils eine eigene Lebensdauer haben. Spielobjekte besitzen eine Position, eine Drehung und eine Skalierung, die du jeweils zur Laufzeit verändern und animieren kannst.

```lua
-- animate X position of "can" game object
go.animate("can", "position.x", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_LINEAR, 1.0)
```

Du kannst Spielobjekte leer verwenden, etwa als Positionsmarkierungen. Üblicherweise sind sie jedoch mit verschiedenen Komponenten wie Sprites, Audiokomponenten, Skripten, Modellen, Fabriken (factory) und weiteren ausgestattet. Spielobjekte werden entweder im Editor erstellt und in Sammlungsdateien platziert oder zur Laufzeit dynamisch durch _Fabrikkomponenten_ erzeugt.

Spielobjekte werden entweder direkt in eine Sammlung eingefügt (in-place) oder einer Sammlung als Referenz auf eine Spielobjektdatei hinzugefügt:

Führe einen <kbd>Rechtsklick</kbd> auf die Sammlung in der Ansicht *Outline* aus und wähle <kbd>Add Game Object</kbd> (direkt einfügen) oder <kbd>Add Game Object File</kbd> (als Dateireferenz einfügen).


## Komponenten {#components}

:[components](../shared/components.md)

Eine Liste aller verfügbaren Komponententypen findest du in der [Komponentenübersicht](/manuals/components/).

## Objekte direkt oder als Referenz hinzufügen {#objects-added-in-place-or-by-reference}

Wenn du eine _Datei_ für eine Sammlung, ein Spielobjekt oder eine Komponente erstellst, legst du damit einen sogenannten Prototyp an (in anderen Engines auch als „Prefabs“ oder „Blueprints“ bekannt). Dadurch wird lediglich eine Datei zur Dateistruktur des Projekts hinzugefügt. Deinem laufenden Spiel wird nichts hinzugefügt. Um eine Instanz einer Sammlung, eines Spielobjekts oder einer Komponente auf Grundlage einer Prototypdatei hinzuzufügen, fügst du eine Instanz davon in eine deiner Sammlungsdateien ein.

In der Ansicht Outline kannst du sehen, auf welcher Datei eine Objektinstanz beruht. Die Datei "main.collection" enthält drei Instanzen, die auf Dateien beruhen:

1. Die Untersammlung "bean".
2. Die Skriptkomponente "bean" im Spielobjekt "bean" in der Untersammlung "bean".
3. Die Skriptkomponente "can" im Spielobjekt "can".

![Instanz](images/building_blocks/instance.png)

Der Vorteil von Prototypdateien wird deutlich, wenn du mehrere Instanzen eines Spielobjekts oder einer Sammlung hast und alle ändern möchtest:

![Spielobjektinstanzen](images/building_blocks/go_instance.png)

Wenn du die Prototypdatei änderst, wird jede Instanz, die diese Datei verwendet, sofort aktualisiert.

![Prototyp eines Spielobjekts ändern](images/building_blocks/go_change_blueprint.png)

Hier wird das Sprite-Bild der Prototypdatei geändert, und sofort werden alle Instanzen aktualisiert, die diese Datei verwenden:

![Aktualisierte Spielobjektinstanzen](images/building_blocks/go_instance2.png)

## Spielobjekte einem übergeordneten Spielobjekt zuordnen {#childing-game-objects}

In einer Sammlungsdatei kannst du Hierarchien von Spielobjekten aufbauen, sodass ein oder mehrere Spielobjekte einem einzelnen übergeordneten Spielobjekt untergeordnet sind. Wenn du ein Spielobjekt auf ein anderes <kbd>ziehst</kbd> und dort <kbd>ablegst</kbd>, wird das gezogene Spielobjekt dem Zielobjekt untergeordnet:

![Spielobjekte einem übergeordneten Spielobjekt zuordnen](images/building_blocks/childing.png)

Eltern-Kind-Hierarchien von Objekten sind dynamische Beziehungen, die beeinflussen, wie Objekte auf Transformationen reagieren. Jede Transformation (Bewegung, Drehung oder Skalierung), die auf ein Objekt angewendet wird, wird wiederum auch auf dessen untergeordnete Objekte angewendet, sowohl im Editor als auch zur Laufzeit:

![Transformation eines untergeordneten Objekts](images/building_blocks/child_transform.png)

Umgekehrt erfolgen Verschiebungen eines untergeordneten Objekts im lokalen Koordinatensystem des übergeordneten Objekts. Im Editor kannst du wählen, ob du ein untergeordnetes Spielobjekt im lokalen Koordinatensystem oder im Weltkoordinatensystem bearbeitest. Wähle dazu <kbd>Edit ▸ World Space</kbd> (die Standardeinstellung) oder <kbd>Edit ▸ Local Space</kbd>.

Du kannst das übergeordnete Objekt auch zur Laufzeit ändern, indem du eine `set_parent`-Nachricht an das Objekt sendest.

```lua
local parent = go.get_id("bean")
msg.post("child_bean", "set_parent", { parent_id = parent })
```

::: important
Ein häufiges Missverständnis ist, dass sich die Position eines Spielobjekts in der Sammlungshierarchie ändert, wenn es Teil einer Eltern-Kind-Hierarchie wird. Dabei handelt es sich jedoch um zwei sehr unterschiedliche Dinge. Eltern-Kind-Hierarchien verändern den Szenengraphen dynamisch, sodass Objekte visuell miteinander verbunden werden können. Die Adresse eines Spielobjekts wird ausschließlich durch seine Position in der Sammlungshierarchie bestimmt. Sie bleibt während der gesamten Lebensdauer des Objekts unverändert.
:::
