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
* *.gltf* ist eine textbasierte JSON-Datei. Sie referenziert gewöhnlich eine separate *.bin*-Datei für Mesh-Daten und separate Texturbilder wie *.png*, *.jpg* oder *.ktx2*. Füge bei dieser Variante alle referenzierten Dateien zum Projekt hinzu und erhalte ihre relativen Pfade.

Eingebettete Bilder können direkt aus einer glTF- oder GLB-Datei verwendet werden, ohne sie in separate Assets zu extrahieren. Externe Bild- und Pufferdateien müssen weiterhin zusammen mit dem Modell importiert werden; ihre relativen Pfade müssen erhalten bleiben.

::: sidenote
Defold erhält Positionen und Transformationen aus der importierten glTF-Datei und zentriert das Modell beim Import nicht automatisch neu. Editorvorschau und Laufzeit verwenden die importierten Transformationen einheitlich: Meshes mit Skinning oder einem Knochen als Elternobjekt behalten ihre lokalen, skelettrelativen Transformationen; starre Meshes behalten ihre zusammengefasste Platzierung im Weltkoordinatensystem.

Eine [Modellkomponente](/manuals/model/#model-properties) kann ein einzelnes benanntes Mesh aus der importierten Szene auswählen. Ein leeres Feld *Mesh* verwendet die gesamte Szene und erhält die oben beschriebenen Transformationen. Die Auswahl eines Meshes verwendet dessen lokale Geometrie ohne glTF-Knotentransformationen; platziere es daher über die Transformation der Modellkomponente oder des Spielobjekts.

Wenn sich die Position oder Ausrichtung eines Modells, das mit einer älteren Defold-Version erstellt wurde, nach einem erneuten Import ändert, korrigiere die Transformation in Blender oder einem anderen Erstellungswerkzeug und exportiere die Datei im Format *.gltf* oder *.glb* erneut.
:::

### Komprimierte Geometrie {#compressed-geometry}

*.gltf*- und *.glb*-Quellen können mit Draco oder Meshopt komprimierte Geometrie enthalten. Folgende glTF-Komprimierungserweiterungen werden unterstützt:

| Komprimierung | glTF-Erweiterung |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` und `KHR_meshopt_compression` |

Exportiere oder optimiere dein glTF-2.0-Asset mit einer dieser Erweiterungen und importiere es anschließend wie ein unkomprimiertes Modell. Beziehe externe Puffer und Texturen ein und erhalte ihre relativen Pfade. Weise die importierte Datei wie gewohnt der Eigenschaft *Scene* einer Modellkomponente zu.

Defold dekodiert die komprimierte Geometrie beim Import und Build. Das resultierende Modell verwendet Defolds normale Geometriedarstellung zur Laufzeit. Diese Unterstützung aktiviert keine Draco- oder Meshopt-Komprimierung in der laufenden Engine, und eine kleinere Quelldatei garantiert kein kleineres Spiel-Bundle.

### Die importierte Szene durchsuchen {#browsing-the-imported-scene}

Klappe eine *.gltf*- oder *.glb*-Datei im Bereich *Assets* auf, um ihre Meshes, erzeugten Materialien und eingebetteten Bilder zu durchsuchen. Beim Öffnen der Szene wird sie mit ihren definierten Materialien und Texturen angezeigt. Du kannst auch einzelne Meshes für eine Vorschau öffnen.

Die innerhalb der Datei bereitgestellten Ressourcen sind schreibgeschützt. Um eine bearbeitbare Modellressource für ein Mesh zu erstellen, kopiere das Mesh und füge es in einen Projektordner ein. Die resultierende *.model*-Datei referenziert weiterhin die importierte glTF- oder GLB-Datei. Bearbeite das Asset in deinem Erstellungswerkzeug und exportiere es erneut, um Quellgeometrie oder eingebettete Bilder zu ändern.

Editorskripte können diese Ressourcen mit `editor.resource_children(path)` auflisten. Unter [Projektressourcen durchlaufen](/manuals/editor-scripts/#traversing-project-resources) findest du ein Beispiel, das Ressourcen in Ordnern und glTF-/GLB-Dateien rekursiv besucht.

### KTX2-Texturen {#ktx2-textures}

Modelltexturen können *.ktx2*-Quellen verwenden, entweder als externe Dateien oder als in *.gltf*- oder *.glb*-Dateien eingebettete Bilder. Importiere externe Dateien zusammen mit dem Modell. Eingebettete KTX2-Bilder erscheinen unter der Szene im Bereich *Assets* und können direkt den Texturfeldern von Materialien oder über <kbd>Auto Fill</kbd> zugewiesen werden.

[Texturprofile](/manuals/texture-profiles/#ktx2-source-textures) bestimmen, ob das KTX2-Quellformat erhalten oder in die konfigurierten Ausgabeformate umgewandelt wird. **Keep KTX2 Format** erhält das Kodierungsformat der Quelle bei aktivierter Texturkomprimierung; Bildverarbeitung kann dennoch eine erneute Kodierung erfordern. Prüfe die Formatunterstützung auf deinen Zielgeräten und berücksichtige mögliche zusätzliche Qualitätsverluste bei erneuter Komprimierung einer bereits komprimierten Textur. Siehe [KTX2-Eingabeformate und Vorschau](/manuals/importing-graphics/#ktx2-textures).

## Ein Modell verwenden {#using-a-model}
Nachdem du das Modell importiert hast, verwende es in einer [Modellkomponente](/manuals/model):

1. Erstelle im Bereich *Assets* mit <kbd>New... ▸ Model</kbd> eine Model-Datei oder füge einem Spielobjekt mit <kbd>Add Component ▸ Model</kbd> direkt eine Modellkomponente hinzu.
2. Setze die Eigenschaft *Scene* auf die importierte *.gltf*- oder *.glb*-Datei.
3. Wähle im Dialog *Auto Fill Model Fields?* <kbd>Auto Fill</kbd>, um die erzeugten Materialien und referenzierten Texturen der Szene zuzuweisen. Dies ersetzt vorhandene Material- und Texturbindungen. Wähle <kbd>Keep Current</kbd>, um deine Bindungen zu behalten; die neue Szenenauswahl wird trotzdem übernommen.
4. Lasse *Mesh* leer, um die gesamte Szene zu verwenden, oder wähle ein benanntes Mesh, um nur dessen lokale Geometrie zu nutzen. Beim Ändern der Mesh-Auswahl kann derselbe Dialog erscheinen: Die Auswahl eines Meshes bietet dessen Materialien an; beim Leeren der Auswahl werden alle Materialien der Szene angeboten. <kbd>Keep Current</kbd> erhält die Bindungen und übernimmt dabei die neue Mesh-Auswahl.
5. Setze bei einem animierten Modell *Skeleton* auf die *.gltf*- oder *.glb*-Datei mit dem Skelett. Oft ist dies dieselbe Datei wie bei *Scene*, wenn Mesh, Skelett und Animationen gemeinsam exportiert werden.
6. Erstelle eine Datei *Animation Set* für die Animationen und weise sie der Eigenschaft *Animations* zu. Setze *Default Animation*, wenn eine Animation automatisch starten soll.

Der Editor bietet das Ausfüllen der Bindungen an, wenn die ausgewählte glTF- oder GLB-Quelle Materialien bereitstellt. Dabei löst er sowohl eingebettete Bilder als auch externe Bildreferenzen auf. Die erzeugten Materialien verwenden die integrierten glTF-Shader; Informationen zu Beleuchtung und unterstützten Materialeffekten findest du im [PBR-Handbuch](/manuals/physically-based-rendering/#built-in-pbr-materials).

### Materialien und Texturen manuell zuweisen {#assigning-materials-and-textures-manually}

Wenn du <kbd>Keep Current</kbd> wählst oder eigene Schattierung benötigst, setze jede Eigenschaft *Material* auf ein geeignetes Material. Die integrierten `gltf`-Materialien bieten PBR-Schattierung; außerdem stehen die integrierten `model`-Materialien und eigene Materialien zur Verfügung. Das [Modellhandbuch](/manuals/model/#material) beschreibt Varianten für statische, geskinte und instanzierte Modelle sowie deren Anforderungen.

Weise jede Textur dem entsprechenden Texturfeld des Materials zu. Du kannst ein eingebettetes Bild unter der glTF- oder GLB-Datei im Bereich *Assets* oder ein separates Bild-Asset im Projekt verwenden. Ordne bei Materialien mit mehreren Samplern jede Textur dem vorgesehenen Sampler zu; das [PBR-Handbuch listet die integrierten glTF-Samplernamen auf](/manuals/physically-based-rendering/#built-in-pbr-materials).


## Nach glTF exportieren {#exporting-to-gltf}
Die exportierte Datei im Format *.gltf* oder *.glb* enthält alle Vertices, Kanten und Flächen, aus denen das Modell besteht, sowie _UV-Koordinaten_ (welcher Teil des Texturbildes auf einen bestimmten Teil des Meshes abgebildet wird), falls du diese definiert hast, die Knochen des Skeletts und Animationsdaten.

* Eine ausführliche Beschreibung von Polygon-Meshes findest du unter http://en.wikipedia.org/wiki/Polygon_mesh.

* UV-Koordinaten und UV-Abbildung werden unter http://en.wikipedia.org/wiki/UV_mapping beschrieben.

Defold legt einige Einschränkungen für exportierte Animationsdaten fest:

* Defold unterstützt derzeit nur vorberechnete Animationen (baked animations). Animationen müssen für jeden animierten Knochen in jedem Schlüsselbild (keyframe) Matrizen enthalten, statt Position, Drehung und Skalierung als separate Schlüsselwerte zu speichern.

* Animationen werden außerdem linear interpoliert. Wenn du eine komplexere Kurveninterpolation verwendest, müssen die Animationen vom Exporter vorberechnet werden.

### Anforderungen {#requirements}
Beachte beim Exportieren eines Modells, dass sich die glTF-Unterstützung zwischen Werkzeugen und Engines unterscheiden kann. Verwende glTF 2.0 und stelle bei texturierten Modellen korrekte UV-Koordinaten sicher. Bilder können in die glTF- oder GLB-Datei eingebettet oder als separate, von der Szene referenzierte Dateien gespeichert werden. Importiere alle externen Bild- und Pufferdateien zusammen mit dem Modell in Defold.

Unser Ziel ist es, das glTF-Format vollständig zu unterstützen, aber dieses Ziel haben wir noch nicht ganz erreicht.
Wenn eine Funktion fehlt, reiche bitte einen Funktionswunsch in [unserem Repository](https://github.com/defold/defold/issues) ein.

### Eine Textur exportieren {#exporting-a-texture}
Wenn du ein Texturbild manuell erstellen möchtest, kannst du das UV-Layout aus Blender als Vorlage exportieren. Wähle zunächst das Mesh und alle seine Vertices aus:

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
