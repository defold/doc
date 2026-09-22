---
title: Handbuch zu GUI-Vorlagen
brief: Dieses Handbuch erklärt das GUI-Vorlagensystem von Defold, mit dem du wiederverwendbare visuelle GUI-Komponenten auf Grundlage gemeinsam genutzter Vorlagen oder „Prefabs“ erstellst.
---

# GUI-Vorlagenknoten {#gui-template-nodes}

GUI-Vorlagenknoten (GUI template nodes) bieten einen leistungsfähigen Mechanismus, um wiederverwendbare GUI-Komponenten (GUI components) auf Grundlage gemeinsam genutzter Vorlagen oder „Prefabs“ zu erstellen. Dieses Handbuch erklärt die Funktion und ihre Verwendung.

Eine GUI-Vorlage (GUI template) ist eine GUI-Szene (GUI scene), die Knoten für Knoten in einer anderen GUI-Szene instanziiert wird. Anschließend kannst du beliebige Eigenschaftswerte der ursprünglichen Vorlagenknoten überschreiben.

## Eine Vorlage erstellen {#creating-a-template}

Eine GUI-Vorlage ist eine gewöhnliche GUI-Szene und wird daher wie jede andere GUI-Szene erstellt. <kbd>Klicke mit der rechten Maustaste</kbd> auf einen Ort im Bereich *Assets* und wähle <kbd>New... ▸ Gui</kbd>.

![Vorlage erstellen](images/gui-templates/create.png)

Erstelle die Vorlage und speichere sie. Beachte, dass die Knoten der Instanz relativ zum Ursprung platziert werden. Daher empfiehlt es sich, die Vorlage an der Position 0, 0, 0 zu erstellen.

## Instanzen aus einer Vorlage erstellen {#creating-instances-from-a-template}

Du kannst beliebig viele Instanzen auf Grundlage der Instanz erstellen. Erstelle oder öffne die GUI-Szene, in der du die Vorlage platzieren möchtest. <kbd>Klicke dann mit der rechten Maustaste</kbd> auf den Abschnitt *Nodes* in *Outline* und wähle <kbd>Add ▸ Template</kbd>.

![Instanz erstellen](images/gui-templates/create_instance.png)

Setze die Eigenschaft *Template* auf die GUI-Szenendatei der Vorlage.

Du kannst beliebig viele Vorlageninstanzen hinzufügen. Für jede Instanz kannst du die Eigenschaften jedes Knotens überschreiben und die Position, Farbgebung, Größe, Textur und weitere Eigenschaften der Instanzknoten ändern.

![Instanzen](images/gui-templates/instances.png)

Jede Eigenschaft, die du änderst, wird im Editor blau markiert. Klicke auf die Schaltfläche zum Zurücksetzen neben der Eigenschaft, um ihren Wert auf den Vorlagenwert zurückzusetzen:

![Eigenschaften](images/gui-templates/properties.png)

Jeder Knoten mit überschriebenen Eigenschaften wird auch in *Outline* blau dargestellt:

![Outline](images/gui-templates/outline.png)

Die Vorlageninstanz wird als einklappbarer Eintrag in der Ansicht *Outline* aufgeführt. Beachte jedoch, dass dieser Eintrag in der Übersicht *kein Knoten ist*. Die Vorlageninstanz existiert auch zur Laufzeit nicht, wohl aber alle Knoten, die zur Instanz gehören.

Knoten, die zu einer Vorlageninstanz gehören, werden automatisch benannt, indem ein Präfix und ein Schrägstrich (`"/"`) vor ihre *Id* gesetzt werden. Das Präfix ist die *Id*, die in der Vorlageninstanz festgelegt ist.

## Vorlagen zur Laufzeit ändern {#modifying-templates-in-runtime}

Skripte, die über den Vorlagenmechanismus hinzugefügte Knoten ändern oder abfragen, müssen lediglich die Benennung der Instanzknoten berücksichtigen und die *Id* der Vorlageninstanz als Präfix des Knotennamens einbeziehen:

```lua
if gui.pick_node(gui.get_node("button_1/button"), x, y) then
    -- Do something...
end
```

Es gibt keinen Knoten, der der Vorlageninstanz selbst entspricht. Wenn du einen Wurzelknoten für eine Instanz benötigst, füge ihn zur Vorlage hinzu.

Wenn einer GUI-Szene als Vorlage ein Skript zugeordnet ist, gehört dieses Skript nicht zum Knotenbaum der Instanz. Du kannst jeder GUI-Szene nur ein einziges Skript zuordnen. Daher muss deine Skriptlogik in der GUI-Szene liegen, in der du deine Vorlagen instanziiert hast.
