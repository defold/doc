---
title: Handbuch zum Beschneiden in der GUI
brief: Dieses Handbuch beschreibt, wie du GUI-Knoten erstellst, die andere Knoten mithilfe von Stencil-Masken beschneiden.
---

# Beschneiden {#clipping}

GUI-Knoten können als Knoten zum *Beschneiden* (Clipping) verwendet werden---Masken, die steuern, wie andere Knoten gerendert werden. Dieses Handbuch erklärt, wie diese Funktion arbeitet.

## Einen Knoten zum Beschneiden erstellen {#creating-a-clipping-node}

Knoten der Typen Box, Text und Pie können zum Beschneiden verwendet werden. Um einen beschneidenden Knoten zu erstellen, füge deiner GUI einen Knoten hinzu und lege seine Eigenschaften entsprechend fest:

Clipping Mode
: Der Modus, der zum Beschneiden verwendet wird.
  - `None` rendert den Knoten, ohne dass ein Beschneiden stattfindet.
  - `Stencil` bewirkt, dass der Knoten in die aktuelle Stencil-Maske schreibt.

Clipping Visible
: Aktiviere dieses Kontrollkästchen, um den Inhalt des Knotens zu rendern.

Clipping Inverted
: Aktiviere dieses Kontrollkästchen, um die Umkehrung der Knotenform in die Maske zu schreiben.

Füge anschließend die Knoten, die du beschneiden möchtest, als untergeordnete Knoten des beschneidenden Knotens hinzu.

![Beschneiden einrichten](images/gui-clipping/create.png)

## Stencil-Maske {#stencil-mask}

Das Beschneiden funktioniert, indem Knoten in einen *Stencil-Puffer* schreiben. Dieser Puffer enthält Beschneidemasken: Informationen, die der Grafikkarte mitteilen, ob ein Pixel gerendert werden soll oder nicht.

- Ein Knoten, der keinen übergeordneten beschneidenden Knoten hat und dessen Beschneidemodus auf `Stencil` gesetzt ist, schreibt seine Form (oder deren Umkehrung) in eine neue Beschneidemaske, die im Stencil-Puffer gespeichert wird.
- Hat ein beschneidender Knoten einen übergeordneten beschneidenden Knoten, beschneidet er stattdessen dessen Beschneidemaske. Ein untergeordneter beschneidender Knoten kann die aktuelle Beschneidemaske niemals _erweitern_, sondern nur weiter beschneiden.
- Knoten, die selbst nicht beschneiden und beschneidenden Knoten untergeordnet sind, werden mit der Beschneidemaske gerendert, die durch die Hierarchie der übergeordneten Knoten entsteht.

![Hierarchie beim Beschneiden](images/gui-clipping/setup.png)

Hier sind drei Knoten in einer Hierarchie angeordnet:

- Sowohl das Sechseck als auch das Quadrat sind beschneidende Stencil-Knoten.
- Das Sechseck erstellt eine neue Beschneidemaske, das Quadrat beschneidet sie weiter.
- Der kreisförmige Knoten ist ein gewöhnlicher Kreissektor-Knoten und wird daher mit der Beschneidemaske gerendert, die seine übergeordneten beschneidenden Knoten erstellen.

Für diese Hierarchie sind vier Kombinationen aus normalen und invertierten beschneidenden Knoten möglich. Der grüne Bereich markiert den Teil des Kreises, der gerendert wird. Der Rest wird maskiert:

![Stencil-Masken](images/gui-clipping/modes.png)

## Einschränkungen von Stencil-Masken {#stencil-limitations}

- Die Gesamtzahl beschneidender Stencil-Knoten darf 256 nicht überschreiten.
- Die maximale Verschachtelungstiefe untergeordneter _Stencil_-Knoten beträgt 8 Ebenen. (Es zählen nur Knoten, die mit Stencil-Masken beschneiden.)
- Die maximale Anzahl von Stencil-Knoten auf derselben Ebene mit demselben übergeordneten Knoten beträgt 127. Mit jeder tieferen Ebene in einer Stencil-Hierarchie halbiert sich diese Obergrenze.
- Invertierte Knoten verursachen einen höheren Aufwand. Es sind höchstens 8 invertierte beschneidende Knoten möglich, und jeder halbiert die maximale Anzahl nicht invertierter beschneidender Knoten.
- Stencils rendern eine Stencil-Maske aus der _Geometrie_ des Knotens (nicht aus der Textur). Du kannst die Maske invertieren, indem du die Eigenschaft *Inverted clipper* aktivierst.


## Ebenen {#layers}

Mit Ebenen kannst du die Renderreihenfolge (und die Bündelung von Zeichenoperationen, Batching) von Knoten steuern. Wenn du Ebenen und beschneidende Knoten verwendest, wird die übliche Ebenenreihenfolge überschrieben. Die Ebenenreihenfolge hat immer Vorrang vor der Beschneidereihenfolge---wenn Ebenenzuweisungen mit beschneidenden Knoten kombiniert werden, kann das Beschneiden in der falschen Reihenfolge erfolgen, falls ein übergeordneter Knoten mit aktiviertem Beschneiden zu einer höheren Ebene als seine untergeordneten Knoten gehört. Untergeordnete Knoten ohne zugewiesene Ebene halten sich weiterhin an die Hierarchie und werden daher nach dem übergeordneten Knoten gezeichnet und beschnitten.

::: sidenote
Ein beschneidender Knoten und seine Hierarchie werden zuerst gezeichnet, wenn ihm eine Ebene zugewiesen ist, und in der regulären Reihenfolge, wenn ihm keine Ebene zugewiesen ist.
:::

![Ebenen und Beschneiden](images/gui-clipping/layers.png)

In diesem Beispiel verwenden die beiden beschneidenden Knoten „`Donut BG`“ und „`BG`“ dieselbe Ebene 1. Ihre Renderreihenfolge entspricht ihrer Reihenfolge in der Hierarchie, in der „`Donut BG`“ vor „`BG`“ gerendert wird. Der untergeordnete Knoten „`Donut Shadow`“ ist jedoch Ebene 2 zugewiesen, die in der Ebenenreihenfolge höher liegt, und wird deshalb nach den beiden beschneidenden Knoten gerendert. In diesem Fall lautet die Renderreihenfolge:

- `Donut BG`
- `BG`
- `BG Frame`
- `Donut Shadow`

Hier siehst du, dass das Objekt „`Donut Shadow`“ aufgrund der Ebenenzuweisung von beiden beschneidenden Knoten beschnitten wird, obwohl es nur einem von ihnen untergeordnet ist.
