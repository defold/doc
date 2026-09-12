---
title: GUI-Box-Knoten in Defold
brief: Dieses Handbuch erklärt, wie du GUI-Box-Knoten verwendest.
---

# GUI-Box-Knoten {#gui-box-nodes}

Ein Box-Knoten (box node) ist ein Rechteck, das mit einer Farbe, einer Textur oder einer Animation gefüllt ist.

## Box-Knoten hinzufügen {#adding-box-nodes}

Füge neue Box-Knoten hinzu, indem du in der Ansicht *Outline* einen <kbd>Rechtsklick</kbd> ausführst und <kbd>Add ▸ Box</kbd> wählst, oder drücke <kbd>A</kbd> und wähle <kbd>Box</kbd>.

Du kannst Bilder und Animationen aus Atlanten oder Kachelquellen (tile sources) verwenden, die der GUI hinzugefügt wurden. Du fügst Texturen hinzu, indem du in der Ansicht *Outline* einen <kbd>Rechtsklick</kbd> auf das Ordnersymbol *Textures* ausführst und <kbd>Add ▸ Textures...</kbd> wählst. Lege anschließend die Eigenschaft *Texture* des Box-Knotens fest:

![Texturen](images/gui-box/create.png)

Beachte, dass die Farbe des Box-Knotens die Grafik einfärbt. Die Farbe für die Einfärbung wird mit den Bilddaten multipliziert. Wenn du die Farbe auf Weiß (den Standardwert) setzt, wird daher keine Einfärbung angewendet.

![Eingefärbte Textur](images/gui-box/tinted.png)

Box-Knoten werden immer gerendert, auch wenn ihnen keine Textur zugewiesen ist, ihr Alpha auf `0` gesetzt ist oder ihre Größe `0, 0, 0` beträgt. Box-Knoten sollten immer eine Textur zugewiesen bekommen, damit der Renderer ihre Zeichenoperationen korrekt bündeln (Batching) und die Anzahl der Zeichenaufrufe (draw calls) verringern kann.

## Animationen abspielen {#playing-animations}

Box-Knoten können Animationen aus Atlanten oder Kachelquellen abspielen. Weitere Informationen findest du im [Handbuch zur Flipbook-Animation](/manuals/flipbook-animation).

:[Slice-9](../shared/slice-9-texturing.md)
