---
title: FAQ zur Defold-Engine und zum Editor
brief: Häufig gestellte Fragen zur Game-Engine, zum Editor und zur Plattform Defold.
---

# Häufig gestellte Fragen {#frequently-asked-questions}

## Allgemeine Fragen {#general-questions}

#### Q: Ist Defold wirklich kostenlos? {#q-is-defold-really-free}

A: Ja, die Defold-Engine und der Editor sind mit ihrem gesamten Funktionsumfang völlig kostenlos. Keine versteckten Kosten, Gebühren oder Lizenzgebühren. Einfach kostenlos.


#### Q: Warum um alles in der Welt sollte die Defold Foundation Defold kostenlos bereitstellen? {#q-why-on-earth-would-the-defold-foundation-give-defold-away}

A: Eines der Ziele der [Defold Foundation](/foundation) ist es, sicherzustellen, dass die Defold-Software Entwicklerinnen und Entwicklern weltweit zur Verfügung steht und der Quellcode kostenlos verfügbar ist.


#### Q: Wie lange werdet ihr Defold unterstützen? {#q-how-long-will-you-support-defold}

A: Wir setzen uns mit voller Überzeugung für Defold ein. Die [Defold Foundation](/foundation) wurde so aufgebaut, dass sie garantiert noch viele Jahre als verantwortliche Eigentümerin von Defold bestehen wird. Sie wird nicht verschwinden.


#### Q: Kann ich mich bei der professionellen Entwicklung auf Defold verlassen? {#q-can-i-trust-defold-for-professional-development}

A: Auf jeden Fall. Defold wird von immer mehr professionellen Spieleentwicklern und Spielestudios verwendet. In der [Spielegalerie](/showcase) findest du Beispiele für Spiele, die mit Defold erstellt wurden.


#### Q: Welche Art von Nutzertracking betreibt ihr? {#q-what-kind-of-user-tracking-are-you-doing}

A: Wir protokollieren anonyme Nutzungsdaten unserer Websites und des Defold-Editors, um unsere Dienste und unser Produkt zu verbessern. In den Spielen, die du erstellst, findet kein Nutzertracking statt (es sei denn, du fügst selbst einen Analysedienst hinzu). Mehr dazu erfährst du in unserer [Datenschutzerklärung](/privacy-policy).


#### Q: Wer hat Defold entwickelt? {#q-who-made-defold}

A: Defold wurde von Ragnar Svensson und Christian Murray entwickelt. Sie begannen 2009 mit der Arbeit an der Engine, dem Editor und den Servern. King und Defold gingen 2013 eine Partnerschaft ein, und 2014 übernahm King Defold. Die vollständige Geschichte kannst du [hier](/about) nachlesen.


## Fragen zur Spieleentwicklung {#game-development-questions}

#### Q: Kann ich mit Defold 3D-Spiele erstellen? {#q-can-i-do-3d-games-in-defold}

A: Auf jeden Fall! Die Engine ist eine vollwertige 3D-Engine. Die Werkzeuge sind allerdings für 2D ausgelegt, weshalb du vieles selbst erledigen musst. Eine bessere 3D-Unterstützung ist geplant.


## Fragen zu Programmiersprachen {#programming-language-questions}

#### Q: Mit welcher Programmiersprache arbeite ich in Defold? {#q-what-programming-language-do-i-work-with-in-defold}

A: Die Spiellogik in deinem Defold-Projekt wird hauptsächlich in Lua geschrieben (genauer gesagt Lua 5.1/LuaJIT; Einzelheiten findest du im [Lua-Handbuch](/manuals/lua)). Lua ist eine schlanke dynamische Sprache, die schnell und sehr leistungsfähig ist. Defold unterstützt Transpiler, die Lua-Code erzeugen. Wenn eine Transpiler-Erweiterung installiert ist, kannst du alternative Sprachen wie [Teal](https://github.com/defold/extension-teal) verwenden, um statisch geprüftes Lua zu schreiben. Du kannst auch nativen Code verwenden (je nach Plattform C/C++, Objective-C, Java und JavaScript), um [die Defold-Engine um neue Funktionen zu erweitern](/manuals/extensions/). Beim Erstellen [benutzerdefinierter Materialien](/manuals/material/) werden Vertex- und Fragment-Shader in der Shader-Sprache OpenGL ES SL geschrieben.


#### Q: Kann ich C++ verwenden, um Spiellogik zu schreiben? {#q-can-i-use-c-to-write-game-logic}

A: Die C++-Unterstützung in Defold dient hauptsächlich dazu, native Erweiterungen zu schreiben, die Schnittstellen zu SDKs von Drittanbietern oder plattformspezifischen APIs bereitstellen. Das [dmSDK](https://defold.com/ref/stable/dmGameObject/) (die C++-API für Defold, die in nativen Erweiterungen verwendet wird) wird schrittweise um weitere Funktionen erweitert, sodass sich auf Wunsch die gesamte Spiellogik in C++ schreiben lässt. Lua bleibt die Hauptsprache für die Spiellogik, aber mit der erweiterten C++-API wird es auch möglich sein, Spiellogik in C++ zu schreiben. Die Erweiterung der C++-API besteht hauptsächlich darin, vorhandene private Headerdateien in den öffentlichen Bereich zu verschieben und APIs für die öffentliche Nutzung zu bereinigen.


#### Q: Kann ich TypeScript mit Defold verwenden? {#q-can-i-use-typescript-with-defold}

A: TypeScript wird nicht offiziell unterstützt. Die Community pflegt die Werkzeugsammlung [ts-defold](https://ts-defold.dev/), mit der du TypeScript schreiben und direkt aus VSCode nach Lua transpilieren kannst.


#### Q: Kann ich Haxe mit Defold verwenden? {#q-can-i-use-haxe-with-defold}

A: Haxe wird nicht offiziell unterstützt. Die Community pflegt [hxdefold](https://github.com/hxdefold/hxdefold), mit dem du Haxe schreiben und nach Lua transpilieren kannst.


#### Q: Kann ich C# mit Defold verwenden? {#q-can-i-use-c-with-defold}

A: Die Defold Foundation hat C#-Unterstützung hinzugefügt und als Abhängigkeit von einer Bibliothek verfügbar gemacht. C# ist eine weitverbreitete Programmiersprache. Die Unterstützung erleichtert Studios und Entwicklern, die stark auf C# setzen, den Wechsel zu Defold.


#### Q: Ich befürchte, dass sich die zusätzliche C#-Unterstützung negativ auf Defold auswirkt. Muss ich mir Sorgen machen? {#q-i-am-concerned-that-adding-c-support-will-have-a-negative-impact-on-defold-should-i-be-worried}

Defold wendet sich NICHT von Lua als primärer Skriptsprache ab. C# wird als neue Sprache für Erweiterungen hinzugefügt. Das wirkt sich nur dann auf die Engine aus, wenn du dich dafür entscheidest, C#-Erweiterungen in deinem Projekt zu verwenden.

Die C#-Unterstützung hat ihren Preis (Größe der ausführbaren Datei, Leistung zur Laufzeit usw.), aber diese Entscheidung liegt beim jeweiligen Entwickler oder Studio.

Was C# selbst betrifft, handelt es sich um eine relativ kleine Änderung, da das Erweiterungssystem bereits viele Sprachen unterstützt (C/C++/Java/Objective-C/Zig). Die SDKs werden durch das Generieren der C#-Anbindungen synchron gehalten. So bleiben die Anbindungen mit minimalem Aufwand aktuell.

Die Defold Foundation war zuvor gegen die Aufnahme von C#-Unterstützung in Defold, hat ihre Meinung aber aus mehreren Gründen geändert:

* Studios und Entwickler fragen weiterhin nach C#-Unterstützung.
* Der Umfang der C#-Unterstützung wurde auf Erweiterungen beschränkt (also geringer Aufwand).
* Die Kern-Engine wird nicht beeinträchtigt.
* Die C#-APIs lassen sich mit minimalem Aufwand synchron halten, wenn sie generiert werden.
* Die C#-Unterstützung wird auf DotNet 9 mit NativeAOT basieren und somit statische Bibliotheken erzeugen, gegen die die bestehende Build-Pipeline linken kann (wie bei jeder anderen Defold-Erweiterung).


## Fragen zu Plattformen {#platform-questions}

#### Q: Auf welchen Plattformen läuft Defold? {#q-what-platforms-does-defold-run-on}

A: Für den Editor und die Werkzeuge sowie für die Laufzeitumgebung der Engine werden folgende Plattformen unterstützt:

  | System             | Version            | Architekturen      | Unterstützung      |
  | ------------------ | ------------------ | ------------------ | ------------------ |
  | macOS              | 11 Big Sur         | `x86-64`, `arm-64` | Editor und Engine  |
  | Windows            | Vista              | `x86-32`, `x86-64` | Editor und Engine  |
  | Ubuntu (1)         | 22.04 LTS          | `x86-64`           | Editor             |
  | Linux (2)          | Beliebig           | `x86-64`, `arm-64` | Engine             |
  | iOS                | 15.0               | `arm-64`  `x86_64` | Engine             |
  | Android            | 5.0 (API-Level 21) | `arm-32`, `arm-64` | Engine             |
  | HTML5              |                    | `wasm-web`, `wasm_pthread-web` | Engine       |

  (1 Der Editor wird für 64-Bit-Ubuntu erstellt und getestet. Er sollte auch auf anderen Distributionen funktionieren, aber dafür geben wir keine Garantie.)

  (2 Die Laufzeitumgebung der Engine sollte auf den meisten 64-Bit-Linux-Distributionen laufen, solange die Grafiktreiber aktuell sind. Weitere Informationen zu Grafik-APIs findest du unten.)


#### Q: Für welche Zielplattformen kann ich mit Defold Spiele entwickeln? {#q-what-target-platforms-can-i-develop-games-for-with-defold}

A: Mit einem Klick kannst du für PS4™, PS5™, Nintendo Switch, iOS (64-Bit), Android (32-Bit und 64-Bit) und HTML5 sowie macOS (x86-64 und arm64), Windows (32-Bit und 64-Bit) und Linux (x86-64 und arm64) veröffentlichen. Es ist tatsächlich eine einzige Codebasis mit Unterstützung für mehrere Plattformen.


#### Q: Auf welcher Rendering-API basiert Defold? {#q-what-rendering-api-does-defold-rely-on}

A: Bei der Entwicklung musst du dich nur mit einer einzigen Render-API befassen, die eine [vollständig skriptgesteuerte Rendering-Pipeline](/manuals/render/) verwendet. Die Render-Skript-API von Defold übersetzt Renderoperationen in die folgenden Grafik-APIs:

:[Graphics API](../shared/graphics-api.md)

#### Q: Kann ich herausfinden, welche Version ich verwende? {#q-is-there-a-way-to-know-what-version-im-running}

A: Ja, wähle die Option „About“ im Menü Help. Das Popup zeigt die Defold-Betaversion und vor allem den SHA1-Wert der jeweiligen Veröffentlichung deutlich an. Um die Version zur Laufzeit abzufragen, verwende [`sys.get_engine_info()`](/ref/sys/#sys.get_engine_info).

Die neueste Betaversion, die unter [http://d.defold.com/beta](http://d.defold.com/beta) zum Herunterladen verfügbar ist, kannst du durch Öffnen von [http://d.defold.com/beta/info.json](http://d.defold.com/beta/info.json) ermitteln (dieselbe Datei gibt es auch für stabile Versionen: [http://d.defold.com/stable/info.json](http://d.defold.com/stable/info.json)).


#### Q: Kann ich zur Laufzeit herausfinden, auf welcher Plattform das Spiel läuft? {#q-is-there-a-way-to-know-what-platform-the-game-is-running-on-at-runtime}

A: Ja, sieh dir [`sys.get_sys_info()`](/ref/sys#sys.get_sys_info) an.


## Fragen zum Editor {#editor-questions}
:[Editor FAQ](../shared/editor-faq.md)


## Fragen zu Linux {#linux-questions}
:[Linux FAQ](../shared/linux-faq.md)


## Fragen zu Android {#android-questions}
:[Android FAQ](../shared/android-faq.md)


## Fragen zu HTML5 {#html5-questions}
:[HTML5 FAQ](../shared/html5-faq.md)


## Fragen zu iOS {#ios-questions}
:[iOS FAQ](../shared/ios-faq.md)


## Fragen zu Windows {#windows-questions}
:[Windows FAQ](../shared/windows-faq.md)


## Fragen zu Konsolen {#console-questions}
:[Consoles FAQ](../shared/consoles-faq.md)


## Spiele veröffentlichen {#publishing-games}

#### Q: Ich versuche, mein Spiel im App Store zu veröffentlichen. Wie soll ich die Frage zur IDFA beantworten? {#q-im-trying-to-publish-my-game-to-appstore-how-should-i-respond-to-idfa}

A: Beim Einreichen bietet Apple drei Kontrollkästchen für die drei zulässigen Anwendungsfälle der IDFA an:

  1. Werbung innerhalb der App anzeigen
  2. Installationen Werbeanzeigen zuordnen
  3. Nutzeraktionen Werbeanzeigen zuordnen

  Wenn du Option 1 auswählst, wird bei der App-Prüfung darauf geachtet, ob Werbeanzeigen in der App erscheinen. Wenn dein Spiel keine Werbung anzeigt, kann es abgelehnt werden. Defold selbst verwendet die Werbe-ID nicht.


#### Q: Wie kann ich mein Spiel monetarisieren? {#q-how-do-i-monetize-my-game}

A: Defold unterstützt In-App-Käufe und verschiedene Werbelösungen. In der [Kategorie Monetization im Asset Portal](https://defold.com/tags/stars/monetization/) findest du eine aktuelle Liste der verfügbaren Möglichkeiten zur Monetarisierung.


## Fehler bei der Verwendung von Defold {#errors-using-defold}

#### Q: Ich kann das Spiel nicht starten, und es gibt keinen Build-Fehler. Was stimmt nicht? {#q-i-cant-start-the-game-and-there-is-no-build-error-whats-wrong}

A: In seltenen Fällen erstellt der Build-Vorgang Dateien nicht neu, nachdem zuvor Build-Fehler aufgetreten sind, die du inzwischen behoben hast. Erzwinge einen vollständigen neuen Build, indem du im Menü *Project > Rebuild And Launch* auswählst.



## Spielinhalte {#game-content}

#### Q: Unterstützt Defold Prefabs? {#q-does-defold-support-prefabs}

A: Ja. Sie heißen [Sammlungen](/manuals/building-blocks/#collections) (collections). Damit kannst du komplexe Hierarchien von Spielobjekten (game objects) erstellen und als separate Bausteine speichern, die du im Editor oder zur Laufzeit instanziieren kannst (indem du die Inhalte einer Sammlung dynamisch erzeugst). Für GUI-Knoten werden GUI-Vorlagen unterstützt.


#### Q: Warum kann ich ein Spielobjekt nicht einem anderen Spielobjekt unterordnen? {#q-i-cant-add-a-game-object-as-a-child-to-another-game-object-why}

A: Wahrscheinlich versuchst du, ein untergeordnetes Objekt in der Spielobjektdatei hinzuzufügen, und das ist nicht möglich. Es ist nur in der Sammlungsdatei möglich. Um zu verstehen, warum, musst du dir vor Augen halten, dass Eltern-Kind-Hierarchien ausschließlich eine Transformationshierarchie des _Szenengraphen_ darstellen. Ein Spielobjekt, das noch nicht in einer Szene (Sammlung) platziert oder dynamisch erzeugt wurde, ist kein Teil eines Szenengraphen und kann deshalb auch nicht Teil einer Szenengraphenhierarchie sein. Mit [`go.get_parent()`](https://defold.com/ref/stable/go-lua/#go.get_parent:id) kannst du den Bezeichner des übergeordneten Spielobjekts abrufen.


#### Q: Warum kann ich Nachrichten nicht an alle untergeordneten Objekte eines Spielobjekts senden? {#q-why-cant-i-broadcast-messages-to-all-children-of-a-game-object}

A: Eltern-Kind-Beziehungen drücken ausschließlich die Transformationsbeziehungen im Szenengraphen aus und sollten nicht mit Aggregaten aus der Objektorientierung verwechselt werden. Wenn du dich auf deine Spieldaten konzentrierst und darauf, wie du sie bei Zustandsänderungen deines Spiels am besten veränderst, wirst du wahrscheinlich weniger Bedarf haben, ständig Nachrichten mit Zustandsdaten an viele Objekte zu senden. In den Fällen, in denen du Datenhierarchien benötigst, lassen sich diese in Lua leicht erstellen und verwalten.


#### Q: Warum sehe ich Bildartefakte an den Rändern meiner Sprites? {#q-why-am-i-experiencing-visual-artifacts-around-the-edges-of-my-sprites}

A: Dieses Bildartefakt heißt „Übergreifen benachbarter Texturpixel“ (edge bleeding). Dabei greifen benachbarte Randpixel im Atlas in das Bild über, das deinem Sprite zugewiesen ist. Die Lösung besteht darin, den Rand deiner Atlasbilder um zusätzliche Zeilen und Spalten identischer Pixel zu erweitern. Glücklicherweise kann der Atlas-Editor in Defold dies automatisch erledigen. Öffne deinen Atlas und setze den Wert *Extrude Borders* auf 1.


#### Q: Kann ich meine Sprites einfärben oder transparent machen, oder muss ich dafür einen eigenen Shader schreiben? {#q-can-i-tint-my-sprites-or-make-them-transparent-or-do-i-have-to-write-my-own-shader-for-it}

A: Der integrierte Sprite-Shader, der standardmäßig für alle Sprites verwendet wird, definiert eine Konstante namens „tint“:

  ```lua
  local red = 1
  local green = 0.3
  local blue = 0.55
  local alpha = 1
  go.set("#sprite", "tint", vmath.vector4(red, green, blue, alpha))
  ```


#### Q: Wenn ich die z-Koordinate eines Sprites auf 100 setze, wird es nicht gerendert. Warum? {#q-if-i-set-the-z-coordinate-of-a-sprite-to-100-then-its-not-rendered-why}

A: Die Z-Position eines Spielobjekts steuert die Zeichenreihenfolge. Niedrige Werte werden vor höheren Werten gezeichnet. Im standardmäßigen Render-Skript werden Spielobjekte mit einer Tiefe zwischen -1 und 1 gezeichnet; alles darunter oder darüber wird nicht gezeichnet. Mehr zum Render-Skript erfährst du in der offiziellen [Rendering-Dokumentation](/manuals/render). Bei GUI-Knoten wird der Z-Wert ignoriert und hat keinerlei Einfluss auf die Zeichenreihenfolge. Stattdessen werden Knoten in der Reihenfolge gerendert, in der sie aufgelistet sind, sowie entsprechend den Hierarchien untergeordneter Knoten (und den Ebenen). Mehr über das GUI-Rendering und die Optimierung von Zeichenaufrufen (draw calls) mithilfe von Ebenen erfährst du in der offiziellen [GUI-Dokumentation](/manuals/gui).


#### Q: Würde es die Leistung beeinflussen, wenn ich den Z-Bereich der Ansichtsprojektion auf -100 bis 100 ändere? {#q-would-changing-the-view-projection-z-range-to-100-to-100-impact-performance}

A: Nein. Die einzige Auswirkung betrifft die Genauigkeit. Der Z-Puffer ist logarithmisch und bietet für z-Werte nahe 0 eine sehr feine Auflösung, während die Auflösung mit zunehmendem Abstand von 0 abnimmt. Beispielsweise lassen sich mit einem 24-Bit-Puffer die Werte 10,0 und 10,000005 unterscheiden, 10000 und 10005 dagegen nicht.


#### Q: Warum werden Winkel nicht einheitlich dargestellt? {#q-there-is-no-consistency-to-how-angles-are-represented-why}

A: Tatsächlich ist die Darstellung einheitlich. Überall im Editor und in den Spiel-APIs werden Winkel in Grad angegeben. Die Mathematikbibliotheken verwenden das Bogenmaß. Derzeit weicht die Physikeigenschaft `angular_velocity` von dieser Konvention ab: Sie wird aktuell in Radiant/s angegeben. Das soll sich ändern.


#### Q: Wie wird ein GUI-Box-Knoten gerendert, der nur eine Farbe und keine Textur hat? {#q-when-creating-a-gui-box-node-with-only-color-no-texture-how-will-it-be-rendered}

A: Er ist einfach eine Form mit Vertex-Farben. Denke daran, dass er trotzdem Füllrate beansprucht.


#### Q: Entlädt die Engine Assets automatisch, wenn ich sie im laufenden Betrieb austausche? {#q-if-i-change-assets-on-the-fly-will-the-engine-automatically-unload-them}

A: Für alle Ressourcen wird intern ein Referenzzähler geführt. Sobald der Referenzzähler null erreicht, wird die Ressource freigegeben.


#### Q: Kann ich Audio wiedergeben, ohne eine Audiokomponente zu verwenden, die an ein Spielobjekt angehängt ist? {#q-is-it-possible-to-play-audio-without-the-use-of-an-audio-component-attached-to-a-game-object}

A: Alles basiert auf Komponenten (components). Du kannst ein Spielobjekt ohne grafische Darstellung mit mehreren Klängen erstellen und die Klänge wiedergeben, indem du Nachrichten an das Objekt zur Audiosteuerung sendest.


#### Q: Kann ich die Audiodatei, die einer Audiokomponente zugeordnet ist, zur Laufzeit ändern? {#q-is-it-possible-to-change-the-audio-file-associated-with-an-audio-component-at-run-time}

A: Im Allgemeinen werden alle Ressourcen statisch deklariert. Das hat den Vorteil, dass du die Ressourcenverwaltung ohne weiteren Aufwand erhältst. Mit [Ressourceneigenschaften](/manuals/script-properties/#resource-properties) kannst du ändern, welche Ressource einer Komponente zugewiesen ist.


#### Q: Kann ich auf die Eigenschaften der physikalischen Kollisionsformen zugreifen? {#q-is-there-a-way-to-access-the-physics-collision-shape-properties}

A: Ja, sieh dir die Physik-API an, insbesondere [`physics.get_shape()`](https://defold.com/ref/stable/physics-lua/#physics.get_shape:url-shape) und [`physics.set_shape()`](https://defold.com/ref/stable/physics-lua/#physics.set_shape:url-shape-table). 


#### Q: Gibt es eine schnelle Möglichkeit, die Kollisionsobjekte in meiner Szene zu rendern? (Wie beim Debug-Zeichnen von Box2D) {#q-is-there-any-quick-way-to-render-the-collision-objects-in-my-scene-like-box2ds-debug-draw}

A: Ja, setze das Flag *physics.debug* in *game.project*. (Siehe die offizielle [Dokumentation der Projekteinstellungen](/manuals/project-settings/#debug))


#### Q: Wie wirken sich viele Kontakte und Kollisionen auf die Leistung aus? {#q-what-are-the-performance-costs-of-having-many-contactscollisions}

A: Defold führt im Hintergrund eine angepasste Version von Box2D aus, und der Leistungsaufwand sollte sehr ähnlich sein. Du kannst jederzeit sehen, wie viel Zeit die Engine für die Physik benötigt, indem du den [Profiler](/manuals/debugging) öffnest. Du solltest auch berücksichtigen, welche Arten von Kollisionsobjekten du verwendest. Statische Objekte benötigen beispielsweise weniger Rechenleistung. Weitere Einzelheiten findest du in der offiziellen [Physik-Dokumentation](/manuals/physics) von Defold.


#### Q: Wie wirken sich viele Partikeleffektkomponenten auf die Leistung aus? {#q-whats-the-performance-impact-of-having-many-particle-effect-components}

A: Das hängt davon ab, ob sie abgespielt werden. Ein ParticleFx, der nicht abgespielt wird, beansprucht keine Rechenleistung. Die Auswirkungen eines abgespielten ParticleFx auf die Leistung musst du mit dem Profiler ermitteln, da sie von seiner Konfiguration abhängen. Wie bei den meisten anderen Dingen wird der Speicher im Voraus für die Anzahl an ParticleFx reserviert, die als max_count in *game.project* definiert ist.


#### Q: Wie empfange ich Eingaben in einem Spielobjekt innerhalb einer Sammlung, die über einen Sammlungs-Proxy geladen wurde? {#q-how-do-i-receive-input-to-a-game-object-inside-a-collection-loaded-via-a-collection-proxy}

A: Jede über einen Sammlungs-Proxy (collection proxy) geladene Sammlung hat ihren eigenen Eingabestapel. Eingaben werden vom Eingabestapel der Hauptsammlung über die Proxy-Komponente an die Objekte in der Sammlung weitergeleitet. Deshalb reicht es nicht aus, wenn das Spielobjekt in der geladenen Sammlung den Eingabefokus anfordert. Auch das Spielobjekt, das die Proxy-Komponente _enthält_, muss den Eingabefokus anfordern. Einzelheiten findest du in der [Eingabedokumentation](/manuals/input).


#### Q: Kann ich Skripteigenschaften vom Typ string verwenden? {#q-can-i-use-string-type-script-properties}

A: Nein. Defold unterstützt Eigenschaften vom Typ [hash](/ref/builtins#hash). Damit kannst du Typen, Zustandsbezeichner oder beliebige Schlüssel angeben. Hashes können auch zum Speichern von Spielobjektbezeichnern (Pfaden) verwendet werden. Häufig sind jedoch [url](/ref/msg#msg.url)-Eigenschaften vorzuziehen, da der Editor automatisch eine Auswahlliste mit passenden URLs für dich füllt. Einzelheiten findest du in der [Dokumentation der Skripteigenschaften](/manuals/script-properties).


#### Q: Wie greife ich auf die einzelnen Zellen einer Matrix zu (die mit [`vmath.matrix4()`](/ref/vmath/#vmath.matrix4:m1) oder einer ähnlichen Funktion erstellt wurde)? {#q-how-do-i-access-the-individual-cells-of-a-matrix-created-using-vmathmatrix4refvmathvmathmatrix4m1-or-similar}

A: Du greifst mit `mymatrix.m11`, `mymatrix.m12`, `mymatrix.m21` usw. auf die Zellen zu.


#### Q: Ich erhalte `Not enough resources to clone the node`, wenn ich [gui.clone()](/ref/gui/#gui.clone:node) oder [gui.clone_tree()](/ref/gui/#gui.clone_tree:node) verwende. {#q-i-am-getting-not-enough-resources-to-clone-the-node-when-using-guiclonerefguiguiclonenode-or-guiclone_treerefguiguiclone_treenode}

A: Erhöhe den Wert `Max Nodes` der GUI-Komponente. Du findest diesen Wert im Bereich Properties, wenn du die Wurzel der Komponente in der Ansicht Outline auswählst.


## Das Forum {#the-forum}

#### Q: Darf ich ein Thema erstellen, in dem ich für meine Arbeit werbe? {#q-can-i-post-a-thread-where-i-advertise-my-work}

A: Natürlich! Dafür haben wir eine eigene [Kategorie „Work for hire“](https://forum.defold.com/c/work-for-hire). Wir fördern immer alles, was der Community zugutekommt. Der Community deine Dienste anzubieten – ob gegen Bezahlung oder nicht – ist ein gutes Beispiel dafür.


#### Q: Ich habe ein Thema erstellt und meine Arbeit hinzugefügt. Darf ich weitere Arbeiten ergänzen? {#q-i-made-a-thread-and-added-my-workcan-i-add-more}

A: Damit Themen in „Work for hire“ seltener durch neue Beiträge nach oben rücken, darfst du in deinem eigenen Thema höchstens einmal alle 14 Tage einen Beitrag veröffentlichen (es sei denn, es handelt sich um eine direkte Antwort auf einen Kommentar im Thema; in diesem Fall darfst du antworten). Wenn du innerhalb der 14 Tage weitere Arbeiten zu deinem Thema hinzufügen möchtest, musst du deine bestehenden Beiträge bearbeiten und den zusätzlichen Inhalt dort ergänzen.


#### Q: Darf ich die Kategorie Work for Hire nutzen, um Stellenangebote zu veröffentlichen? {#q-can-i-use-the-work-for-hire-category-to-post-job-offerings}

A: Klar, nur zu! Du kannst dort sowohl Angebote als auch Gesuche veröffentlichen, zum Beispiel: „Programmierer sucht 2D-Pixelkünstler; ich bin reich und bezahle dich gut“.
