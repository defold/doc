---
title: Beschriftungskomponenten in Defold
brief: Dieses Handbuch erklärt, wie du mit Beschriftungskomponenten Text an Spielobjekten in der Spielwelt verwendest.
---

# Beschriftung {#label}

Eine *Beschriftungskomponente* (Label component) rendert ein Stück Text im Spielraum auf dem Bildschirm. Standardmäßig wird sie zusammen mit allen Sprite- und Kachelgrafiken sortiert und gezeichnet. Die Komponente verfügt über eine Reihe von Eigenschaften, die bestimmen, wie der Text gerendert wird. Die GUI von Defold unterstützt Text, doch es kann schwierig sein, GUI-Elemente in der Spielwelt zu platzieren. Beschriftungen erleichtern dies.

## Eine Beschriftung erstellen {#creating-a-label}

Um eine Beschriftungskomponente zu erstellen, klicke <kbd>mit der rechten Maustaste</kbd> auf das Spielobjekt (game object) und wähle <kbd>Add Component ▸ Label</kbd>.

![Beschriftung hinzufügen](images/label/add_label.png)

(Wenn du mehrere Beschriftungen aus derselben Vorlage instanziieren möchtest, kannst du alternativ eine neue Datei für eine Beschriftungskomponente erstellen: Klicke <kbd>mit der rechten Maustaste</kbd> auf einen Ordner im Browser *Assets* und wähle <kbd>New... ▸ Label</kbd>. Füge die Datei anschließend als Komponente zu beliebigen Spielobjekten hinzu.)

![Neue Beschriftung](images/label/label.png)

Setze die Eigenschaft *Font* auf die Schriftart, die du verwenden möchtest, und stelle sicher, dass die Eigenschaft *Material* auf ein Material gesetzt ist, das zum Schrifttyp passt:

![Schriftart und Material](images/label/font_material.png)

## Eigenschaften der Beschriftung {#label-properties}

Neben den Eigenschaften *Id*, *Position*, *Rotation* und *Scale* gibt es die folgenden komponentenspezifischen Eigenschaften:

*Text*
: Der Textinhalt der Beschriftung.

*Size*
: Die Größe des Begrenzungsrechtecks des Textes. Wenn *Line Break* aktiviert ist, legt die Breite fest, an welcher Stelle der Text umgebrochen werden soll.

*Color*
: Die Farbe des Textes.

*Outline*
: Die Farbe der Kontur.

*Shadow*
: Die Farbe des Schattens.

::: sidenote
Beachte, dass das Rendern von Schatten beim Standardmaterial aus Leistungsgründen deaktiviert ist.
:::

*Leading*
: Ein Skalierungsfaktor für den Zeilenabstand. Ein Wert von 0 ergibt keinen Zeilenabstand. Der Standardwert ist 1.

*Tracking*
: Ein Skalierungsfaktor für den Zeichenabstand. Der Standardwert ist 0.

*Pivot*
: Der Bezugspunkt (pivot) des Textes. Verwende ihn, um die Textausrichtung zu ändern (siehe unten).

*Blend Mode*
: Der Mischmodus, der beim Rendern der Beschriftung verwendet wird.

*Line Break*
: Die Textausrichtung richtet sich nach der Einstellung des Bezugspunkts. Wenn du diese Eigenschaft aktivierst, kann sich der Text über mehrere Zeilen erstrecken. Die Breite der Komponente bestimmt, wo der Text umgebrochen wird. Beachte, dass der Text ein Leerzeichen enthalten muss, damit er umgebrochen werden kann.

*Font*
: Die Schriftressource, die für diese Beschriftung verwendet wird.

*Material*
: Das Material, das zum Rendern dieser Beschriftung verwendet wird. Achte darauf, ein Material auszuwählen, das für den verwendeten Schrifttyp erstellt wurde (Bitmap, Distanzfeld oder BMFont).

### Mischmodi {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### Bezugspunkt und Ausrichtung {#pivot-and-alignment}

Durch das Festlegen der Eigenschaft *Pivot* kannst du die Ausrichtung des Textes ändern.

*Zentriert*
: Wenn der Bezugspunkt auf `Center`, `North` oder `South` gesetzt ist, wird der Text zentriert.

*Linksbündig*
: Wenn der Bezugspunkt auf einen der `West`-Modi gesetzt ist, wird der Text linksbündig ausgerichtet.

*Rechtsbündig*
: Wenn der Bezugspunkt auf einen der `East`-Modi gesetzt ist, wird der Text rechtsbündig ausgerichtet.

![Textausrichtung](images/label/align.png)

## Änderungen zur Laufzeit {#runtime-manipulation}

Du kannst Beschriftungen zur Laufzeit ändern, indem du den Beschriftungstext sowie die verschiedenen anderen Eigenschaften abfragst und festlegst.

`text`
: Der Textinhalt der Beschriftung (`string`). Seit Defold 1.13.2 über `go.get()` und `go.set()` verfügbar.

`color`
: Die Farbe der Beschriftung (`vector4`)

`outline`
: Die Konturfarbe der Beschriftung (`vector4`)

`shadow`
: Die Schattenfarbe der Beschriftung (`vector4`)

`scale`
: Die Skalierung der Beschriftung, entweder eine Zahl (`number`) für eine gleichmäßige Skalierung oder ein `vector3` für eine individuelle Skalierung entlang jeder Achse.

`size`
: Die Größe der Beschriftung (`vector3`)

```lua
function init(self)
    -- Set the text of the "my_label" component in the same game object
    -- as this script.
    go.set("#my_label", "text", "New text")
    local text = go.get("#my_label", "text")
    print(text) -- New text
end
```

::: sidenote
Seit Defold 1.13.2 sind `label.set_text()` und `label.get_text()` zugunsten der Eigenschaft `text` veraltet und zur Ablösung vorgesehen. Die alten Funktionen bleiben aus Kompatibilitätsgründen verfügbar. Die alte Setter-Funktion stellt eine Nachricht in die Warteschlange, während `go.set()` den Text sofort aktualisiert.
:::

```lua
function init(self)
    -- Set the color of the "my_label" component in the same game object
    -- as this script. Color is a RGBA value stored in a vector4.
    local grey = vmath.vector4(0.5, 0.5, 0.5, 1.0)
    go.set("#my_label", "color", grey)

    -- ...and remove the outline, by setting its alpha to 0...
    go.set("#my_label", "outline.w", 0)

    -- ...and scale it x2 along x axis.
    local scale_x = go.get("#my_label", "scale.x")
    go.set("#my_label", "scale.x", scale_x * 2)
end
```

## Projektkonfiguration {#project-configuration}

Die Datei *game.project* enthält einige [Projekteinstellungen](/manuals/project-settings#label) für Beschriftungen.
