---
title: Defold für Flash-Nutzer
brief: Dieses Handbuch stellt Defold als Alternative für die Entwicklung von Flash-Spielen vor. Es behandelt einige der wichtigsten Konzepte der Spieleentwicklung mit Flash und erläutert die entsprechenden Werkzeuge und Methoden in Defold.
---

# Defold für Flash-Nutzer {#defold-for-flash-users}

Dieses Handbuch stellt Defold als Alternative für die Entwicklung von Flash-Spielen vor. Es behandelt einige der wichtigsten Konzepte der Spieleentwicklung mit Flash und erläutert die entsprechenden Werkzeuge und Methoden in Defold.

## Einführung {#introduction}

Zu den wichtigsten Vorteilen von Flash gehörten seine Zugänglichkeit und die niedrige Einstiegshürde. Neue Nutzer konnten das Programm schnell erlernen und mit geringem Zeitaufwand einfache Spiele erstellen. Defold bietet einen ähnlichen Vorteil durch eine Reihe von Werkzeugen, die speziell für die Spieleentwicklung gedacht sind. Gleichzeitig können erfahrene Entwickler fortgeschrittene Lösungen für komplexere Anforderungen erstellen, beispielsweise indem sie das standardmäßige Render-Skript bearbeiten.

Flash-Spiele werden in ActionScript programmiert (wobei 3.0 die neueste Version ist), während Skripte in Defold in Lua geschrieben werden. Dieses Handbuch geht nicht auf einen detaillierten Vergleich von Lua und ActionScript 3.0 ein. Das [Defold-Handbuch](/manuals/lua) bietet eine gute Einführung in die Lua-Programmierung in Defold und verweist auf das äußerst hilfreiche Buch [Programming in Lua](https://www.lua.org/pil/) (erste Auflage), das kostenlos online verfügbar ist.

Ein Artikel von Jesse Warden bietet einen [grundlegenden Vergleich von ActionScript und Lua](http://jessewarden.com/2011/01/lua-for-actionscript-developers.html), der als guter Ausgangspunkt dienen kann. Beachte jedoch, dass sich der Aufbau von Defold und Flash grundlegender unterscheidet, als es auf der Sprachebene sichtbar ist. ActionScript und Flash sind im klassischen Sinn objektorientiert, mit Klassen und Vererbung. Defold hat weder Klassen noch Vererbung. Es enthält das Konzept eines *Spielobjekts* (game object), das audiovisuelle Darstellung, Verhalten und Daten enthalten kann. Operationen an Spielobjekten werden mit *Funktionen* ausgeführt, die in den Defold-APIs verfügbar sind. Darüber hinaus fördert Defold die Verwendung von *Nachrichten* zur Kommunikation zwischen Objekten. Nachrichten sind ein Konstrukt auf einer höheren Abstraktionsebene als Methodenaufrufe und sind nicht dafür gedacht, wie solche verwendet zu werden. Diese Unterschiede sind wichtig und erfordern etwas Eingewöhnung, werden in diesem Handbuch aber nicht im Detail behandelt.

Stattdessen untersucht dieses Handbuch einige der wichtigsten Konzepte der Spieleentwicklung in Flash und zeigt, welche Entsprechungen ihnen in Defold am nächsten kommen. Gemeinsamkeiten und Unterschiede werden ebenso wie häufige Stolperfallen erläutert, damit dir der Wechsel von Flash zu Defold zügig gelingt.

## Movieclips und Spielobjekte {#movie-clips-and-game-objects}

Movieclips sind ein zentraler Bestandteil der Spieleentwicklung mit Flash. Es handelt sich um Symbole, die jeweils eine eigene Zeitleiste enthalten. Das ähnlichste Konzept in Defold ist ein Spielobjekt.

![Spielobjekt und Movieclip](images/flash/go_movieclip.png)

Anders als Flash-Movieclips haben Defold-Spielobjekte keine Zeitleisten. Stattdessen besteht ein Spielobjekt aus mehreren Komponenten (components). Zu den Komponenten gehören unter anderem Sprites, Audiokomponenten und Skripte (weitere Informationen zu den verfügbaren Komponenten findest du in der [Dokumentation zu den Bausteinen](/manuals/building-blocks) und den zugehörigen Artikeln). Das Spielobjekt in der folgenden Bildschirmaufnahme besteht aus einem Sprite und einem Skript. Mit der Skriptkomponente steuerst du das Verhalten und das Aussehen von Spielobjekten während ihres gesamten Lebenszyklus:

![Skriptkomponente](images/flash/script_component.png)

Während Movieclips andere Movieclips enthalten können, können Spielobjekte keine Spielobjekte *enthalten*. Spielobjekte können jedoch anderen Spielobjekten *untergeordnet werden*. Dadurch entstehen Hierarchien, die gemeinsam verschoben, skaliert oder gedreht werden können.

## Flash—Movieclips manuell erstellen {#flashmanually-creating-movie-clips}

In Flash kannst du Instanzen von Movieclips manuell zu deiner Szene hinzufügen, indem du sie aus der Bibliothek auf die Zeitleiste ziehst. Das zeigt die folgende Bildschirmaufnahme, in der jedes Flash-Logo eine Instanz des Movieclips `logo` ist:

![Manuell erstellte Movieclips](images/flash/manual_movie_clips.png)

## Defold—Spielobjekte manuell erstellen {#defoldmanually-creating-game-objects}

Wie bereits erwähnt, gibt es in Defold kein Konzept einer Zeitleiste. Stattdessen werden Spielobjekte in Sammlungen (collections) organisiert. Sammlungen sind Container (oder Prefabs), die Spielobjekte und andere Sammlungen enthalten. Im einfachsten Fall kann ein Spiel aus nur einer Sammlung bestehen. Häufiger verwenden Defold-Spiele mehrere Sammlungen, die entweder manuell zur Startsammlung (bootstrap collection) `main` hinzugefügt oder über [Sammlungs-Proxys](/manuals/collection-proxy) (collection proxies) dynamisch geladen werden. Für dieses Konzept, „Level“ oder „Bildschirme“ zu laden, gibt es keine direkte Entsprechung in Flash.

Im folgenden Beispiel enthält die Sammlung `main` drei Instanzen (rechts im Fenster *Outline* aufgelistet) des Spielobjekts `logo` (links im Browserfenster *Assets* zu sehen):

![Manuell erstellte Spielobjekte](images/flash/manual_game_objects.png)

## Flash—manuell erstellte Movieclips referenzieren {#flashreferencing-manually-created-movie-clips}

Um manuell erstellte Movieclips in Flash zu referenzieren, benötigst du einen manuell festgelegten Instanznamen:

![Instanzname in Flash](images/flash/flash_instance_name.png)

## Defold—Spielobjekt-ID {#defoldgame-object-id}

In Defold werden alle Spielobjekte und Komponenten über eine Adresse referenziert. In den meisten Fällen genügt ein einfacher Name oder eine Kurzform. Zum Beispiel:

- `"."` adressiert das aktuelle Spielobjekt.
- `"#"` adressiert die aktuelle Komponente (das Skript).
- `"logo"` adressiert das Spielobjekt mit dem Bezeichner (ID) `logo`.
- `"#script"` adressiert die Komponente mit der ID `script` im aktuellen Spielobjekt.
- `"logo#script"` adressiert die Komponente mit der ID `script` im Spielobjekt mit der ID `logo`.

Die Adresse manuell platzierter Spielobjekte wird durch die zugewiesene Eigenschaft *Id* bestimmt (siehe unten rechts in der Bildschirmaufnahme). Die ID muss innerhalb der Sammlungsdatei, in der du gerade arbeitest, eindeutig sein. Der Editor legt automatisch eine ID für dich fest, aber du kannst sie für jede Spielobjektinstanz ändern, die du erstellst.

![Spielobjekt-ID](images/flash/game_object_id.png)

::: sidenote
Du kannst die ID eines Spielobjekts ermitteln, indem du den folgenden Code in seiner Skriptkomponente ausführst: `print(go.get_id())`. Dadurch wird die ID des aktuellen Spielobjekts in der Konsole ausgegeben.
:::

Das Adressierungsmodell und die Nachrichtenübermittlung sind zentrale Konzepte der Spieleentwicklung mit Defold. Das [Handbuch zur Adressierung](/manuals/addressing) und das [Handbuch zur Nachrichtenübermittlung](/manuals/message-passing) erläutern sie ausführlich.

## Flash—Movieclips dynamisch erstellen {#flashdynamically-creating-movie-clips}

Um Movieclips in Flash dynamisch zu erstellen, musst du zunächst ActionScript Linkage einrichten:

![ActionScript Linkage](images/flash/actionscript_linkage.png)

Dadurch wird eine Klasse erstellt (in diesem Fall `Logo`), von der du anschließend neue Instanzen erzeugen kannst. Eine Instanz der Klasse `Logo` könntest du wie folgt zur Bühne hinzufügen:

```as
var logo:Logo = new Logo();
addChild(logo);
```

## Defold—Spielobjekte mit Fabriken erstellen {#defoldcreating-game-objects-using-factories}

In Defold werden Spielobjekte mithilfe von *Fabriken* (factories) dynamisch erzeugt. Fabriken sind Komponenten, mit denen du Kopien eines bestimmten Spielobjekts dynamisch erzeugst. In diesem Beispiel wurde eine Fabrik mit dem Spielobjekt `logo` als Prototyp erstellt:

![Fabrik für das Logo](images/flash/logo_factory.png)

Beachte, dass Fabriken wie alle Komponenten einem Spielobjekt hinzugefügt werden müssen, bevor du sie verwenden kannst. In diesem Beispiel haben wir ein Spielobjekt namens `factories` erstellt, das unsere Fabrikkomponente enthält:

![Fabrikkomponente](images/flash/factory_component.png)

Um eine Instanz des Spielobjekts `logo` zu erzeugen, rufst du diese Funktion auf:

```lua
local logo_id = factory.create("factories#logo_factory")
```

Die URL ist ein erforderlicher Parameter von `factory.create()`. Zusätzlich kannst du optionale Parameter angeben, um Position, Drehung, Eigenschaften und Skalierung festzulegen. Weitere Informationen zur Fabrikkomponente findest du im [Handbuch zu Fabriken](/manuals/factory). Beachte, dass der Aufruf von `factory.create()` die ID des erstellten Spielobjekts zurückgibt. Diese ID kannst du für spätere Zugriffe in einer Tabelle speichern (die in Lua einem Array entspricht).

## Flash—Bühne {#flashstage}

In Flash kennen wir die Timeline (im oberen Bereich der folgenden Bildschirmaufnahme) und die Stage (unterhalb der Timeline sichtbar):

![Zeitleiste und Bühne](images/flash/stage.png)

Wie oben im Abschnitt über Movieclips erläutert, ist die Bühne im Wesentlichen der oberste Container eines Flash-Spiels und wird bei jedem Export eines Projekts erstellt. Standardmäßig hat die Bühne ein untergeordnetes Objekt, die *`MainTimeline`*. Jeder im Projekt erzeugte Movieclip hat eine eigene Zeitleiste und kann als Container für andere Symbole dienen (einschließlich Movieclips).

## Defold—Sammlungen {#defoldcollections}

Die Entsprechung zur Flash-Bühne in Defold ist eine Sammlung. Beim Start erstellt die Engine anhand des Inhalts einer Sammlungsdatei eine neue Spielwelt. Standardmäßig heißt diese Datei `main.collection`. Du kannst aber ändern, welche Sammlung beim Start geladen wird, indem du die Einstellungsdatei *game.project* im Stammverzeichnis jedes Defold-Projekts öffnest:

![game.project](images/flash/game_project.png)

Sammlungen sind Container, mit denen du im Editor Spielobjekte und andere Sammlungen organisierst. Der Inhalt einer Sammlung kann auch per Skript zur Laufzeit mithilfe einer [Sammlungsfabrik](/manuals/collection-factory/#spawning-a-collection) (collection factory) dynamisch erzeugt werden. Sie funktioniert genauso wie eine normale Spielobjektfabrik. Das ist beispielsweise nützlich, um Gruppen von Gegnern oder eine Anordnung einsammelbarer Münzen dynamisch zu erzeugen. In der folgenden Bildschirmaufnahme haben wir zwei Instanzen der Sammlung `logos` manuell in der Sammlung `main` platziert.

![Sammlung](images/flash/collection.png)

In manchen Fällen möchtest du eine völlig neue Spielwelt laden. Mit der Komponente [Sammlungs-Proxy](/manuals/collection-proxy/) kannst du anhand des Inhalts einer Sammlungsdatei eine neue Spielwelt erstellen. Das ist beispielsweise beim Laden neuer Spiellevel, Minispiele oder Zwischensequenzen nützlich.

## Flash—Zeitleiste {#flashtimeline}

Die Flash-Zeitleiste wird hauptsächlich für Animationen verwendet, mit verschiedenen Einzelbildtechniken oder Form- und Bewegungs-Tweens. Die allgemeine Einstellung der Bildrate des Projekts in Bildern pro Sekunde (FPS) legt fest, wie lange ein Einzelbild angezeigt wird. Erfahrene Nutzer können die allgemeine Bildrate des Spiels oder sogar die einzelner Movieclips ändern.

Form-Tweens ermöglichen die Interpolation von Vektorgrafiken zwischen zwei Zuständen. Das ist meist nur für einfache Formen und Anwendungen nützlich, wie das folgende Beispiel zeigt, in dem ein Quadrat durch Form-Tweening in ein Dreieck übergeht:

![Zeitleiste](images/flash/timeline.png)

Bewegungs-Tweens ermöglichen die Animation verschiedener Eigenschaften eines Objekts, darunter Größe, Position und Drehung. Im folgenden Beispiel wurden alle aufgeführten Eigenschaften verändert.

![Bewegungs-Tween](images/flash/tween.png)

## Defold—Eigenschaftsanimation {#defoldproperty-animation}

Defold arbeitet mit Pixelbildern statt mit Vektorgrafiken und hat daher keine Entsprechung zum Form-Tweening. Für Bewegungs-Tweening gibt es jedoch mit der [Eigenschaftsanimation](/ref/go/#go.animate) eine leistungsfähige Entsprechung. Sie wird per Skript mit der Funktion `go.animate()` ausgeführt. Die Funktion `go.animate()` interpoliert eine Eigenschaft (etwa Farbe, Skalierung, Drehung oder Position) vom Anfangswert zum gewünschten Endwert und verwendet dabei eine der vielen verfügbaren Easing-Funktionen (einschließlich benutzerdefinierter Funktionen). Während du fortgeschrittene Easing-Funktionen in Flash selbst implementieren musstest, sind in Defold [viele Easing-Funktionen](/manuals/property-animation/#easing) direkt in die Engine integriert.

Während Flash Grafiken mithilfe von Schlüsselbildern (keyframes) auf einer Zeitleiste animiert, gehört die Flipbook-Animation importierter Bildfolgen zu den wichtigsten Methoden der Grafikanimation in Defold. Animationen werden in einer Spielobjektkomponente namens Atlas organisiert. In diesem Fall haben wir einen Atlas für eine Spielfigur mit einer Animationssequenz namens `run`. Sie besteht aus einer Reihe von PNG-Dateien:

![Flipbook-Animation](images/flash/flipbook.png)

## Flash—Tiefenindex {#flashdepth-index}

In Flash bestimmt die Anzeigeliste, was in welcher Reihenfolge dargestellt wird. Die Reihenfolge von Objekten in einem Container (beispielsweise der Bühne) wird über einen Index verwaltet. Objekte, die du einem Container mit der Methode `addChild()` hinzufügst, belegen automatisch die oberste Position im Index. Dieser beginnt bei 0 und wird mit jedem weiteren Objekt erhöht. In der folgenden Bildschirmaufnahme haben wir drei Instanzen des Movieclips `logo` erzeugt:

![Tiefenindex](images/flash/depth_index.png)

Die Positionen in der Anzeigeliste sind durch die Zahlen neben jeder Instanz von `logo` angegeben. Ohne den Code für die x/y-Position der Movieclips zu berücksichtigen, könnte das obige Ergebnis wie folgt erzeugt worden sein:

```as
var logo1:Logo = new Logo();
var logo2:Logo = new Logo();
var logo3:Logo = new Logo();

addChild(logo1);
addChild(logo2);
addChild(logo3);
```

Ob ein Objekt über oder unter einem anderen Objekt angezeigt wird, hängt von ihren relativen Positionen im Index der Anzeigeliste ab. Das lässt sich gut veranschaulichen, indem du die Indexpositionen zweier Objekte vertauschst, zum Beispiel:

```as
swapChildren(logo2,logo3);
```

Das Ergebnis sähe wie folgt aus (mit aktualisierter Indexposition):

![Tiefenindex](images/flash/depth_index_2.png)

## Defold—z-Position

Die Positionen von Spielobjekten in Defold werden durch Vektoren mit drei Variablen dargestellt: x, y und z. Die z-Position bestimmt die Tiefe eines Spielobjekts. Im standardmäßigen [Render-Skript](/manuals/render) liegen die verfügbaren z-Positionen im Bereich von -1 bis 1.

::: sidenote
Spielobjekte mit einer z-Position außerhalb des Bereichs von -1 bis 1 werden nicht gerendert und sind daher nicht sichtbar. Das ist eine häufige Stolperfalle beim Einstieg in Defold. Denke daran, wenn ein Spielobjekt nicht sichtbar ist, obwohl du es erwartest.
:::

Anders als in Flash, wo der Editor die Tiefenindizierung nur indirekt darstellt (und Änderungen mit Befehlen wie *Bring Forward* und *Send Backward* ermöglicht), kannst du in Defold die z-Position von Objekten direkt im Editor festlegen. In der folgenden Bildschirmaufnahme siehst du, dass `logo3` ganz oben dargestellt wird und eine z-Position von 0,2 hat. Die anderen Spielobjekte haben die z-Positionen 0,0 und 0,1.

![z-Reihenfolge](images/flash/z_order.png)

Beachte, dass die z-Position eines Spielobjekts, das in einer oder mehreren Sammlungen verschachtelt ist, durch seine eigene z-Position zusammen mit denen aller übergeordneten Objekte bestimmt wird. Stell dir beispielsweise vor, die obigen Spielobjekte `logo` wären in einer Sammlung `logos` platziert, die wiederum in `main` liegt (siehe folgende Bildschirmaufnahme). Hätte die Sammlung `logos` eine z-Position von 0,9, wären die z-Positionen der enthaltenen Spielobjekte 0,9, 1,0 und 1,1. Daher würde `logo3` nicht gerendert werden, da seine z-Position größer als 1 ist.

![z-Reihenfolge](images/flash/z_order_outline.png)

Die z-Position eines Spielobjekts kannst du natürlich per Skript ändern. Gehe davon aus, dass sich der folgende Code in der Skriptkomponente eines Spielobjekts befindet:

```lua
local pos = go.get_position()
pos.z  = 0.5
go.set_position(pos)
```

## Kollisionserkennung in Flash mit `hitTestObject` und `hitTestPoint` {#flash-hittestobject-and-hittestpoint-collision-detection}

Eine grundlegende Kollisionserkennung in Flash erreichst du mit der Methode `hitTestObject()`. In diesem Beispiel haben wir zwei Movieclips: `bullet` und `bullseye`. Sie sind in der folgenden Bildschirmaufnahme zu sehen. Das blaue Begrenzungsrechteck wird sichtbar, wenn du die Symbole im Flash-Editor auswählst. Diese Begrenzungsrechtecke bestimmen das Ergebnis der Methode `hitTestObject()`.

![Trefferprüfung](images/flash/hittest.png)

Die Kollisionserkennung mit `hitTestObject()` erfolgt so:

```as
bullet.hitTestObject(bullseye);
```

Die Verwendung der Begrenzungsrechtecke wäre in diesem Fall ungeeignet, da im folgenden Szenario ein Treffer registriert würde:

![Trefferprüfung mit Begrenzungsrechteck](images/flash/hitboundingbox.png)

Eine Alternative zu `hitTestObject()` ist die Methode `hitTestPoint()`. Diese Methode hat einen Parameter `shapeFlag`, mit dem Trefferprüfungen anhand der tatsächlichen Pixel eines Objekts statt anhand seines Begrenzungsrechtecks durchgeführt werden können. Die Kollisionserkennung mit `hitTestPoint()` könnte so erfolgen:

```as
bullseye.hitTestPoint(bullet.x, bullet.y, true);
```

Diese Zeile würde die x- und y-Position des Geschosses (in diesem Szenario oben links) gegen die Form des Ziels prüfen. Da `hitTestPoint()` einen Punkt gegen eine Form prüft, ist die Auswahl des zu prüfenden Punktes (oder der Punkte!) eine wesentliche Überlegung.

## Defold—Kollisionsobjekte {#defoldcollision-objects}

Defold enthält eine Physik-Engine, die Kollisionen erkennen kann und ein Skript darauf reagieren lässt. Die Kollisionserkennung in Defold beginnt damit, dass du Spielobjekten Kollisionsobjekte (collision objects) als Komponenten zuweist. In der folgenden Bildschirmaufnahme haben wir dem Spielobjekt `bullet` ein Kollisionsobjekt hinzugefügt. Das Kollisionsobjekt wird als rotes transparentes Rechteck dargestellt (das nur im Editor sichtbar ist):

![Kollisionsobjekt](images/flash/collision_object.png)

Defold enthält eine modifizierte Version der Physik-Engine Box2D, die realistische Kollisionen automatisch simulieren kann. Dieses Handbuch geht von der Verwendung kinematischer Kollisionsobjekte aus, da diese der Kollisionserkennung in Flash am nächsten kommen. Mehr über dynamische Kollisionsobjekte erfährst du im [Physikhandbuch](/manuals/physics) von Defold.

Das Kollisionsobjekt hat die folgenden Eigenschaften:

![Eigenschaften des Kollisionsobjekts](images/flash/collision_object_properties.png)

Wir haben eine Rechteckform verwendet, da sie am besten zur Grafik des Geschosses passt. Die andere Form für 2D-Kollisionen, die Kugel, wird für das Ziel verwendet. Wenn du den Typ auf Kinematic setzt, verarbeitet dein Skript die Kollisionen anstelle der integrierten Physik-Engine (weitere Informationen zu den anderen Typen findest du im [Physikhandbuch](/manuals/physics)). Die Eigenschaften *Group* und *Mask* bestimmen, zu welcher Kollisionsgruppe das Objekt gehört beziehungsweise mit welcher Kollisionsgruppe es auf Kollisionen geprüft werden soll. Die aktuelle Konfiguration bedeutet, dass ein `bullet` nur mit einem `target` kollidieren kann. Stell dir vor, die Konfiguration wird wie folgt geändert:

![Kollisionsgruppe und Kollisionsmaske](images/flash/collision_groupmask.png)

Jetzt können Geschosse mit Zielen und anderen Geschossen kollidieren. Zum Vergleich haben wir ein Kollisionsobjekt für das Ziel eingerichtet, das wie folgt aussieht:

![Kollisionsobjekt des Geschosses](images/flash/collision_object_bullet.png)

Beachte, dass die Eigenschaft *Group* auf `target` und *Mask* auf `bullet` gesetzt ist.

In Flash findet die Kollisionserkennung nur statt, wenn das Skript sie ausdrücklich aufruft. In Defold läuft die Kollisionserkennung fortlaufend im Hintergrund, solange ein Kollisionsobjekt aktiviert bleibt. Bei einer Kollision werden Nachrichten an alle Komponenten eines Spielobjekts gesendet (vor allem an die Skriptkomponenten). Das sind die Nachrichten [`collision_response` und `contact_point_response`](/manuals/physics-messages), die alle Informationen enthalten, um die Kollision wie gewünscht zu verarbeiten.

Der Vorteil der Kollisionserkennung in Defold besteht darin, dass sie fortgeschrittener als die von Flash ist und mit sehr geringem Einrichtungsaufwand Kollisionen zwischen relativ komplexen Formen erkennen kann. Die Kollisionserkennung erfolgt automatisch. Du musst also nicht die verschiedenen Objekte in den unterschiedlichen Kollisionsgruppen in Schleifen durchlaufen und ausdrücklich Trefferprüfungen ausführen. Der größte Nachteil ist, dass es keine Entsprechung zum Flash-Parameter `shapeFlag` gibt. Für die meisten Anwendungsfälle reichen jedoch Kombinationen der grundlegenden Rechteck- und Kugelformen aus. Für komplexere Szenarien [sind benutzerdefinierte Formen möglich](//forum.defold.com/t/does-defold-support-only-three-shapes-for-collision-solved/1985).

## Flash—Ereignisverarbeitung {#flashevent-handling}

Ereignisobjekte und die zugehörigen Listener werden verwendet, um verschiedene Ereignisse (z. B. Mausklicks, Tastendrücke oder das Laden von Clips) zu erkennen und als Reaktion Aktionen auszulösen. Es stehen zahlreiche Ereignisse zur Verfügung.

## Defold—Callback-Funktionen und Nachrichtenübermittlung {#defoldcall-back-functions-and-messaging}

Die Defold-Entsprechung zum Ereignisverarbeitungssystem von Flash besteht aus mehreren Aspekten. Zunächst enthält jede Skriptkomponente eine Reihe von Callback-Funktionen, die bestimmte Ereignisse erkennen. Diese sind:

init
:   Wird aufgerufen, wenn die Skriptkomponente initialisiert wird. Entspricht der Konstruktorfunktion in Flash.

final
:   Wird aufgerufen, wenn die Skriptkomponente zerstört wird (z. B. wenn ein dynamisch erzeugtes Spielobjekt entfernt wird).

update
:   Wird in jedem Frame aufgerufen. Entspricht `enterFrame` in Flash.

on_message
:   Wird aufgerufen, wenn die Skriptkomponente eine Nachricht empfängt.

on_input
:   Wird aufgerufen, wenn eine Nutzereingabe (z. B. von Maus oder Tastatur) an ein Spielobjekt mit [Eingabefokus](/ref/go/#acquire_input_focus) gesendet wird. Eingabefokus bedeutet, dass das Objekt alle Eingaben empfängt und darauf reagieren kann.

on_reload
:   Wird aufgerufen, wenn die Skriptkomponente neu geladen wird.

Die oben aufgeführten Callback-Funktionen sind alle optional und können entfernt werden, wenn du sie nicht verwendest. Einzelheiten zum Einrichten der Eingabe findest du im [Eingabehandbuch](/manuals/input). Bei der Arbeit mit Sammlungs-Proxys gibt es eine häufige Stolperfalle. Weitere Informationen dazu findest du in [diesem Abschnitt](/manuals/input/#input-dispatch-and-on_input) des Eingabehandbuchs.

Wie im Abschnitt zur Kollisionserkennung erläutert, werden Kollisionsereignisse verarbeitet, indem Nachrichten an die beteiligten Spielobjekte gesendet werden. Ihre jeweiligen Skriptkomponenten empfangen die Nachricht in ihren Callback-Funktionen `on_message`.

## Flash—Schaltflächensymbole {#flashbutton-symbols}

Flash verwendet einen eigenen Symboltyp für Schaltflächen. Schaltflächen nutzen bestimmte Ereignishandler-Methoden (z. B. `click` und `buttonDown`), um Aktionen auszuführen, wenn eine Nutzerinteraktion erkannt wird. Die grafische Form einer Schaltfläche im Bereich „Hit“ des Schaltflächensymbols bestimmt ihren Trefferbereich.

![Schaltfläche](images/flash/button.png)

## Defold—GUI-Szenen und Skripte {#defoldgui-scenes-and-scripts}

Defold enthält keine native Schaltflächenkomponente. Auch lassen sich Klicks auf die Form eines bestimmten Spielobjekts nicht so einfach erkennen, wie es bei Schaltflächen in Flash der Fall ist. Die Verwendung einer [GUI](/manuals/gui)-Komponente ist die häufigste Lösung, unter anderem, weil die Positionen der GUI-Komponenten in Defold nicht von der Kamera im Spiel beeinflusst werden (falls eine verwendet wird). Die GUI-API enthält außerdem Funktionen, mit denen du erkennen kannst, ob Nutzereingaben wie Klicks und Berührungsereignisse innerhalb der Grenzen eines GUI-Elements liegen.

## Debugging

In Flash ist der Befehl `trace()` dein Helfer bei der Fehlersuche. Die Entsprechung in Defold ist `print()` und wird genauso wie `trace()` verwendet:

```lua
print("Hello world!"")
```

Du kannst mit einem Aufruf der Funktion `print()` mehrere Variablen ausgeben:

```lua
print(score, health, ammo)
```

Es gibt auch eine Funktion `pprint()` (formatierte Ausgabe), die beim Arbeiten mit Tabellen hilfreich ist. Diese Funktion gibt den Inhalt von Tabellen einschließlich verschachtelter Tabellen aus. Betrachte das folgende Skript:

```lua
factions = {"red", "green", "blue"}
world = {name = "Terra", teams = factions}
pprint(world)
```

Es enthält eine Tabelle (`factions`), die in einer Tabelle (`world`) verschachtelt ist. Der normale Befehl `print()` würde die eindeutige ID der Tabelle ausgeben, aber nicht ihren eigentlichen Inhalt:

```
DEBUG:SCRIPT: table: 0x7ff95de63ce0
```

Die Verwendung der Funktion `pprint()` wie oben gezeigt liefert aussagekräftigere Ergebnisse:

```
DEBUG:SCRIPT:
{
  name = Terra,
  teams = {
    1 = red,
    2 = green,
    3 = blue,
  }
}
```

Wenn dein Spiel Kollisionserkennung verwendet, kannst du das Physik-Debugging durch Senden der folgenden Nachricht umschalten:

```lua
msg.post("@system:", "toggle_physics_debug")
```

Du kannst das Physik-Debugging auch in den Projekteinstellungen aktivieren. Bevor wir das Physik-Debugging einschalten, sieht unser Projekt so aus:

![Ohne Debugging](images/flash/no_debug.png)

Wenn du das Physik-Debugging einschaltest, werden die Kollisionsobjekte angezeigt, die wir unseren Spielobjekten hinzugefügt haben:

![Mit Debugging](images/flash/with_debug.png)

Bei Kollisionen leuchten die betreffenden Kollisionsobjekte auf. Zusätzlich wird der Kollisionsvektor angezeigt:

![Kollision](images/flash/collision.png)

Informationen zur Überwachung der CPU-Auslastung und des Speicherverbrauchs findest du schließlich in der [Profiler-Dokumentation](/ref/profiler/). Weitere Informationen zu fortgeschrittenen Debugging-Techniken findest du im [Abschnitt zum Debugging](/manuals/debugging) des Defold-Handbuchs.

## Wie es weitergeht {#where-to-go-from-here}

- [Defold-Beispiele](/examples)
- [Tutorials](/tutorials)
- [Handbücher](/manuals)
- [Referenz](/ref/go)
- [FAQ](/faq/faq)

Wenn du Fragen hast oder nicht weiterkommst, sind die [Defold-Foren](//forum.defold.com) eine gute Anlaufstelle für Hilfe.
