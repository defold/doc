Komponenten (components) verleihen Spielobjekten (game objects) eine bestimmte Darstellung und/oder Funktionalität. Komponenten müssen in Spielobjekten enthalten sein und werden durch die Position, Drehung und Skalierung des Spielobjekts beeinflusst, das sie enthält:

![Komponenten](../shared/images/components.png)

Viele Komponenten haben typspezifische Eigenschaften, die du ändern kannst. Außerdem gibt es typspezifische Funktionen für die Interaktion mit ihnen zur Laufzeit:

```lua
-- disable the can "body" sprite
msg.post("can#body", "disable")

-- play "hoohoo" sound on "bean" in 1 second
sound.play("bean#hoohoo", { delay = 1, gain = 0.5 } )
```

Komponenten werden entweder direkt in ein Spielobjekt eingefügt (in-place) oder einem Spielobjekt als Referenz auf eine Komponentendatei hinzugefügt:

<kbd>Klicke mit der rechten Maustaste</kbd> auf das Spielobjekt in der Ansicht *Outline* und wähle <kbd>Add Component</kbd> (direkt einfügen) oder <kbd>Add Component File</kbd> (als Dateireferenz einfügen).

In den meisten Fällen ist es am sinnvollsten, Komponenten direkt im Spielobjekt zu erstellen. Die folgenden Komponententypen müssen jedoch in separaten Ressourcendateien erstellt werden, bevor du sie einem Spielobjekt als Referenz hinzufügst:

* Script
* GUI
* Particle FX
* Tile Map
