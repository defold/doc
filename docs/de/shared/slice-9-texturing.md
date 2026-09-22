## Texturierung mit Neun-Segment-Skalierung {#slice-9-texturing}

GUI-Box-Knoten (box nodes) und Sprite-Komponenten (sprite components) stellen manchmal Elemente dar, deren Größe vom jeweiligen Kontext abhängt: Bereiche und Dialogfelder, deren Größe an den enthaltenen Inhalt angepasst werden muss, oder eine Lebensanzeige, deren Größe die verbleibende Gesundheit eines Gegners widerspiegeln muss. Dabei können Darstellungsprobleme entstehen, wenn du den in seiner Größe angepassten Knoten oder das Sprite mit einer Textur versiehst.

Normalerweise skaliert die Engine die Textur so, dass sie in die rechteckigen Grenzen passt. Durch das Festlegen von Randbereichen für die Neun-Segment-Skalierung (9-slice) kannst du jedoch einschränken, welche Teile der Textur skaliert werden sollen:

![GUI-Skalierung](../shared/images/gui_slice9_scaling.png)

Die Einstellung *Slice9* des Box-Knotens besteht aus 4 Zahlen. Sie geben jeweils die Anzahl der Pixel für den linken, oberen, rechten und unteren Rand an, die nicht auf die übliche Weise skaliert werden sollen:

![Eigenschaften der Neun-Segment-Skalierung](../shared/images/gui_slice9_properties.png)

Die Ränder werden im Uhrzeigersinn festgelegt, beginnend am linken Rand:

![Bereiche der Neun-Segment-Skalierung](../shared/images/gui_slice9.png)

- Ecksegmente werden niemals skaliert.
- Randsegmente werden entlang einer einzelnen Achse skaliert. Die linken und rechten Randsegmente werden vertikal skaliert. Die oberen und unteren Randsegmente werden horizontal skaliert.
- Der mittlere Texturbereich wird nach Bedarf horizontal und vertikal skaliert.

Die oben beschriebene Texturskalierung mit *Slice9* wird nur angewendet, wenn du die Größe des Box-Knotens oder des Sprites änderst:

![Größe des GUI-Box-Knotens](../shared/images/gui_slice9_size.png)

![Größe des Sprites](../shared/images/sprite_slice9_size.png)

::: important
Wenn du den Skalierungsparameter des Box-Knotens, des Sprites oder des Spielobjekts (game object) änderst, werden der Knoten oder das Sprite und die Textur skaliert, ohne die Parameter von *Slice9* anzuwenden.
:::

::: important
Wenn du die Texturierung mit Neun-Segment-Skalierung für Sprites verwendest, muss [Sprite Trim Mode des Bildes](https://defold.com/manuals/atlas/#image-properties) auf Off gesetzt sein.
:::


### Mipmaps und Neun-Segment-Skalierung {#mipmaps-and-slice-9}
Aufgrund der Funktionsweise von Mipmapping im Renderer können beim Skalieren von Textursegmenten manchmal Artefakte auftreten. Das geschieht, wenn du Segmente gegenüber der ursprünglichen Texturgröße _verkleinerst_. Der Renderer wählt dann für das Segment eine Mipmap mit geringerer Auflösung aus, was zu sichtbaren Artefakten führt.

![Mipmapping bei der Neun-Segment-Skalierung](../shared/images/gui_slice9_mipmap.png)

Um dieses Problem zu vermeiden, stelle sicher, dass die zu skalierenden Segmente der Textur klein genug sind, sodass sie niemals verkleinert, sondern nur vergrößert werden müssen.
