---
title: 3D-Meshes in Defold
brief: Dieses Handbuch beschreibt, wie du in deinem Spiel zur Laufzeit 3D-Meshes erstellst.
---

# Mesh-Komponente {#mesh-component}

Defold ist im Kern eine 3D-Engine. Auch wenn du ausschließlich mit 2D-Material arbeitest, erfolgt das gesamte Rendering in 3D, wird aber orthografisch auf den Bildschirm projiziert. Defold ermöglicht dir, vollständige 3D-Inhalte zu nutzen, indem du zur Laufzeit 3D-Meshes in deinen Sammlungen (collections) hinzufügst und erstellst. Du kannst reine 3D-Spiele mit ausschließlich 3D-Assets entwickeln oder 3D- und 2D-Inhalte nach Belieben kombinieren.

## Eine Mesh-Komponente erstellen {#creating-a-mesh-component}

Mesh-Komponenten erstellst du wie jede andere Komponente (component) eines Spielobjekts (game object). Dafür gibt es zwei Möglichkeiten:

- Erstelle eine *Mesh-Datei*, indem du im Browser *Assets* an einer Stelle <kbd>mit der rechten Maustaste klickst</kbd> und <kbd>New... ▸ Mesh</kbd> auswählst.
- Erstelle die Komponente direkt in ein Spielobjekt eingebettet, indem du in der Ansicht *Outline* auf ein Spielobjekt <kbd>mit der rechten Maustaste klickst</kbd> und <kbd>Add Component ▸ Mesh</kbd> auswählst.

![Mesh in einem Spielobjekt](images/mesh/mesh.png)

Nachdem du das Mesh erstellt hast, musst du einige Eigenschaften festlegen:

### Mesh-Eigenschaften {#mesh-properties}

Neben den Eigenschaften *Id*, *Position* und *Rotation* gibt es die folgenden komponentenspezifischen Eigenschaften:

*Material*
: Das Material, mit dem das Mesh gerendert wird.

*Vertices*
: Eine Pufferdatei, die die Mesh-Daten für jeden Datenstrom beschreibt.

*Primitive Type*
: Lines, Triangles oder Triangle Strip.

*Position Stream*
: Diese Eigenschaft sollte den Namen des Datenstroms *position* enthalten. Der Datenstrom wird dem Vertex-Shader automatisch als Eingabe bereitgestellt.

*Normal Stream*
: Diese Eigenschaft sollte den Namen des Datenstroms *normal* enthalten. Der Datenstrom wird dem Vertex-Shader automatisch als Eingabe bereitgestellt.

*tex0*
: Lege hier die Textur fest, die für das Mesh verwendet werden soll.

## Bearbeitung im Editor {#editor-manipulation}

Sobald die Mesh-Komponente vorhanden ist, kannst du die Komponente und/oder das Spielobjekt, das sie enthält, mit den üblichen Werkzeugen des *Scene Editor* bearbeiten und verändern, um das Mesh nach deinen Wünschen zu verschieben, zu drehen und zu skalieren.

## Bearbeitung zur Laufzeit {#runtime-manipulation}

Du kannst Meshes zur Laufzeit mithilfe von Defold-Puffern verändern. Beispiel für das Erstellen eines Würfels aus Dreiecksstreifen:

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

Im [Ankündigungsbeitrag im Forum findest du weitere Informationen](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137) zur Verwendung der Mesh-Komponente, einschließlich Beispielprojekten und Codeausschnitten.

## Aussondern von Geometrie außerhalb des Sichtvolumens {#frustum-culling}

Mesh-Komponenten werden außerhalb des Sichtvolumens nicht automatisch ausgesondert (Frustum Culling), weil sie dynamisch sind und nicht sicher bekannt ist, wie die Positionsdaten codiert sind. Damit ein Mesh ausgesondert werden kann, muss sein achsenparalleler Begrenzungsquader als Metadaten im Puffer mit 6 Gleitkommazahlen (AABB min/max) festgelegt werden:

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## Materialkonstanten {#material-constants}

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: Die Einfärbung des Meshes (`vector4`). Der `vector4` stellt die Einfärbung dar, wobei x, y, z und w den Rot-, Grün-, Blau- und Alphaanteilen entsprechen.

## Vertices im lokalen Koordinatensystem und im Weltkoordinatensystem {#vertex-local-vs-world-space}
Wenn die Einstellung Vertex Space des Mesh-Materials auf Local Space gesetzt ist, werden dir die Daten im Shader unverändert bereitgestellt. Du musst die Vertices und Normalen wie üblich auf der GPU transformieren.

Wenn die Einstellung Vertex Space des Mesh-Materials auf World Space gesetzt ist, musst du entweder Datenströme mit den Standardnamen `position` und `normal` bereitstellen oder sie beim Bearbeiten des Meshes aus der Auswahlliste auswählen. Dadurch kann die Engine die Daten in das Weltkoordinatensystem transformieren, um Zeichenoperationen mit anderen Objekten zu bündeln (Batching).
