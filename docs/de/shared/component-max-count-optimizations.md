## Optimierungen der maximalen Komponentenanzahl {#component-max-count-optimizations}
Die Einstellungsdatei *game.project* enthält viele Werte, die angeben, wie viele Ressourcen eines bestimmten Typs höchstens gleichzeitig existieren können. Häufig wird diese Anzahl pro geladener Sammlung (collection), auch als Welt bezeichnet, gezählt. Die Defold-Engine verwendet diese Höchstwerte, um Speicher für die jeweilige Anzahl im Voraus zu reservieren und so dynamische Speicherzuweisungen und Speicherfragmentierung während der Ausführung des Spiels zu vermeiden.

Die Datenstrukturen, die Defold zur Darstellung von Komponenten (components) und anderen Ressourcen verwendet, sind auf einen möglichst geringen Speicherverbrauch optimiert. Dennoch solltest du die Werte sorgfältig festlegen, um nicht mehr Speicher als tatsächlich nötig zu reservieren.

Um den Speicherverbrauch weiter zu optimieren, analysiert der Build-Vorgang von Defold die Inhalte des Spiels und überschreibt die Höchstwerte, wenn sich die genaue Anzahl mit Sicherheit bestimmen lässt:

* Wenn eine Sammlung keine Fabrikkomponenten (factory components) enthält, wird Speicher für die genaue Anzahl jeder Komponente und der Spielobjekte (game objects) reserviert. Die festgelegten Höchstwerte werden dabei ignoriert.
* Wenn eine Sammlung eine Fabrikkomponente enthält, werden die dynamisch erzeugten Objekte analysiert. Für Komponenten, die durch die Fabriken dynamisch erzeugt werden können, und für Spielobjekte wird der Höchstwert verwendet.
* Wenn eine Sammlung eine Fabrik oder eine Sammlungsfabrik (collection factory) mit aktivierter Option "Dynamic Prototype" enthält, verwendet diese Sammlung die Höchstwerte.
