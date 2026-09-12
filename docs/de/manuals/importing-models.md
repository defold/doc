---
title: Modelle importieren
brief: Dieses Handbuch beschreibt, wie du 3D-Modelle importierst, die von der Modellkomponente verwendet werden.
---

# 3D-Modelle importieren {#importing-3d-models}
Defold unterstützt Modelle, Skelette und Animationen im Format glTF 2.0 (GL Transmission Format). Verwende für 3D-Modelle Dateien im Format *.gltf* oder *.glb*. glTF ist ein modernes Format, das für die Übertragung und das Laden von 3D-Daten in Game-Engines und Echtzeitanwendungen entwickelt wurde.

Du kannst Werkzeuge wie Maya, 3ds Max, SketchUp und Blender verwenden, um 3D-Modelle zu erstellen oder in glTF zu konvertieren.

Blender ist ein leistungsfähiges und beliebtes Programm für 3D-Modellierung, Animation und Rendering. Es läuft unter Windows, macOS und Linux und ist kostenlos unter [https://www.blender.org](https://www.blender.org) verfügbar.

![Modell in Blender](images/model/blender_gltf.png)

## In Defold importieren {#importing-to-defold}
Um ein Modell zu importieren, ziehe die Datei im Format *.gltf* oder *.glb* in den Bereich *Assets* des Defold-Editors und lege sie dort ab.

glTF kann auf zwei gängige Arten gespeichert werden:

* *.glb* ist eine einzelne Binärdatei. Sie enthält die Modelldaten und kann auch eingebettete Texturbilder enthalten. Das ist praktisch, wenn du ein Modell als eine Datei verschieben oder speichern möchtest.
* *.gltf* ist eine textbasierte JSON-Datei. Sie verweist normalerweise auf eine separate Datei im Format *.bin* für Mesh-Daten und separate Texturbilder, etwa im Format *.png* oder *.jpg*. Wenn du diese Variante verwendest, füge dem Projekt alle referenzierten Dateien hinzu und behalte ihre relativen Pfade bei.

Wenn das Modell in Defold eine Textur verwenden soll, importiere das Texturbild als separates Asset. Auch wenn die glTF-/GLB-Quelldatei eingebettete Bilder enthält, müssen Texturen der Modellkomponente (model component) über die Materialtextureigenschaften der Komponente zugewiesen werden.

![Importierte Modell-Assets](images/model/assets_gltf.png)

::: sidenote
Ab Defold 1.13.0 behält Defold die Positionen und Transformationen aus der importierten glTF-Datei bei und zentriert das Modell beim Import nicht mehr automatisch neu. Die Editorvorschau und die Laufzeitumgebung verwenden die importierten Transformationen einheitlich: Meshes mit Skinning oder mit einem Knochen als übergeordnetem Objekt behalten ihre lokalen, auf das Skelett bezogenen Transformationen bei, während starre Meshes ihre nach dem Auflösen der Hierarchie resultierende Platzierung in Weltkoordinaten behalten.

Seit Defold 1.13.2 kann eine [Modellkomponente](/manuals/model/#model-properties) ein einzelnes benanntes Mesh aus der importierten Szene auswählen. Wenn du ihr Feld *Mesh* leer lässt, wird die gesamte Szene verwendet und die oben beschriebenen Transformationen bleiben erhalten. Wenn du ein Mesh auswählst, wird seine lokale Geometrie ohne die Transformationen der glTF-Knoten verwendet. Platziere es daher mithilfe der Transformation der Modellkomponente oder des Spielobjekts (game object).

Wenn sich die Position oder Ausrichtung eines Modells, das mit einer älteren Defold-Version erstellt wurde, nach einem erneuten Import ändert, korrigiere die Transformation in Blender oder einem anderen Erstellungswerkzeug und exportiere die Datei im Format *.gltf* oder *.glb* erneut.
:::

## Ein Modell verwenden {#using-a-model}
Nachdem du das Modell importiert hast, verwende es in einer [Modellkomponente](/manuals/model):

1. Erstelle im Bereich *Assets* mit <kbd>New... ▸ Model</kbd> eine Model-Datei oder füge einem Spielobjekt mit <kbd>Add Component ▸ Model</kbd> direkt eine Modellkomponente hinzu.
2. Setze die Eigenschaft *Scene* auf die importierte Datei im Format *.gltf* oder *.glb*. Lass *Mesh* leer, um die gesamte Szene zu verwenden, oder wähle ein benanntes Mesh aus, um nur seine lokale Geometrie zu verwenden.
3. Setze bei einem animierten Modell die Eigenschaft *Skeleton* auf die Datei im Format *.gltf* oder *.glb*, die das Skelett enthält. Dies ist häufig dieselbe Datei, die für *Scene* verwendet wird, wenn Mesh, Skelett und Animationen zusammen exportiert werden.
4. Erstelle für die Animationen eine Datei vom Typ *Animation Set* und weise sie der Eigenschaft *Animations* zu. Lege *Default Animation* fest, wenn eine Animation automatisch starten soll.
5. Setze die Eigenschaft *Material* auf ein für das Modell geeignetes Material. Die integrierten Dateien *model.material*, *model_instanced.material*, *model_skinned.material* und *model_skinned_instanced.material* sind nützliche Ausgangspunkte. Die Materialien für Skinning verwenden lokale Vertex-Koordinaten, damit das Skinning auf der GPU ausgeführt werden kann. Benutzerdefinierte Materialien für Modelle mit GPU-Skinning oder Instancing sollten ebenfalls lokale Vertex-Koordinaten verwenden. Die Anforderung an den Grafikadapter findest du im [Handbuch zu Modellen](/manuals/model/#material).
6. Setze die Materialtextureigenschaften, etwa *Texture*, auf die importierten Texturbilddateien. Wenn das Material mehrere Texturen verwendet, weise jede Textur im entsprechenden Texturfeld des Materials zu.


## Nach glTF exportieren {#exporting-to-gltf}
Die exportierte Datei im Format *.gltf* oder *.glb* enthält alle Vertices, Kanten und Flächen, aus denen das Modell besteht, sowie _UV-Koordinaten_ (welcher Teil des Texturbildes auf einen bestimmten Teil des Meshes abgebildet wird), falls du diese definiert hast, die Knochen des Skeletts und Animationsdaten.

* Eine ausführliche Beschreibung von Polygon-Meshes findest du unter http://en.wikipedia.org/wiki/Polygon_mesh.

* UV-Koordinaten und UV-Abbildung werden unter http://en.wikipedia.org/wiki/UV_mapping beschrieben.

Defold legt einige Einschränkungen für exportierte Animationsdaten fest:

* Defold unterstützt derzeit nur vorberechnete Animationen (baked animations). Animationen müssen für jeden animierten Knochen in jedem Schlüsselbild (keyframe) Matrizen enthalten, statt Position, Drehung und Skalierung als separate Schlüsselwerte zu speichern.

* Animationen werden außerdem linear interpoliert. Wenn du eine komplexere Kurveninterpolation verwendest, müssen die Animationen vom Exporter vorberechnet werden.

### Anforderungen {#requirements}
Beachte beim Export eines Modells, dass sich die glTF-Unterstützung zwischen Werkzeugen und Engines unterscheiden kann. Verwende glTF 2.0, stelle sicher, dass das Modell korrekte UV-Koordinaten hat, wenn es Texturen verwendet, und importiere Texturbilder separat, wenn sie einer Modellkomponente zugewiesen werden sollen.

Unser Ziel ist es, das glTF-Format vollständig zu unterstützen, aber dieses Ziel haben wir noch nicht ganz erreicht.
Wenn eine Funktion fehlt, reiche bitte einen Funktionswunsch in [unserem Repository](https://github.com/defold/defold/issues) ein.

### Eine Textur exportieren {#exporting-a-texture}
Wenn du noch keine Textur für dein Modell hast, kannst du mit Blender eine Textur erzeugen. Das solltest du tun, bevor du zusätzliche Materialien aus dem Modell entfernst. Wähle zunächst das Mesh und alle seine Vertices aus:

![Alle auswählen](images/model/blender_select_all_vertices.png)

Wenn alle Vertices ausgewählt sind, wickle das Mesh ab, um das UV-Layout zu erhalten:

![Mesh abwickeln](images/model/blender_unwrap_mesh.png)

Anschließend kannst du das UV-Layout als Bild exportieren, das als Textur verwendet werden kann:

![UV-Layout exportieren](images/model/blender_export_uv_layout.png)

![Ergebnis des UV-Layout-Exports](images/model/blender_export_uv_layout_result.png)

### Mit Blender exportieren {#exporting-using-blender}
Exportiere dein Modell aus Blender mit <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd>.

![Mit Blender exportieren](images/model/export_gltf.png)

Wähle vor dem Export das Objekt oder die Objekte aus und aktiviere *Selected Objects*, wenn du nur die Auswahl exportieren möchtest.

Wähle eine der Optionen unter *Format*:

* *glTF Binary (.glb)* erstellt eine Datei. Verwende diese Option, wenn sich das Modell als einzelnes Asset leicht verschieben oder speichern lassen soll.
* *glTF Separate (.gltf + .bin + textures)* erstellt separate Dateien für die Modellbeschreibung, Binärdaten und Texturen. Verwende diese Option, wenn du Texturbilder bearbeiten oder sie in Defold separat zuweisen möchtest.

Wenn das Modell Animationen enthält, aktiviere den Animationsexport und stelle sicher, dass die Animationen vorberechnet sind. Wenn das Modell Texturen verwendet, stelle sicher, dass das Mesh für UV-Koordinaten abgewickelt wurde und die Texturbilder in einem Format exportiert werden, das Defold importieren kann, etwa PNG oder JPEG.

![Mit Blender exportieren](images/model/export_settings.png)
