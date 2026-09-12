---
title: Texturfilterung
brief: Dieses Handbuch beschreibt die verfügbaren Optionen für die Texturfilterung beim Rendern von Grafiken.
---

# Texturfilterung und Abtastung {#texture-filtering-and-sampling}

Die Texturfilterung (texture filtering) bestimmt das sichtbare Ergebnis, wenn ein _Texel_ (ein Pixel in einer Textur) nicht genau mit einem Bildschirmpixel übereinstimmt. Das passiert, wenn du ein Grafikelement, das die Textur enthält, um weniger als ein Pixel bewegst. Die folgenden Filtermethoden sind verfügbar:

Nächster Nachbar (Nearest)
: Das nächstgelegene Texel wird ausgewählt, um das Bildschirmpixel einzufärben. Du solltest diese Abtastmethode wählen, wenn du eine exakte Eins-zu-eins-Zuordnung zwischen den Pixeln deiner Texturen und den Pixeln auf dem Bildschirm möchtest. Bei der Nächster-Nachbar-Filterung springt bei Bewegungen alles von Pixel zu Pixel. Das kann ruckelig aussehen, wenn sich das Sprite langsam bewegt.

Linear
: Der Farbwert des Texels wird mit den Farbwerten seiner Nachbarn gemittelt, bevor das Bildschirmpixel eingefärbt wird. Dadurch wirken langsame, kontinuierliche Bewegungen flüssig, da die Farbe eines Sprites allmählich in die Pixel einfließt, bevor sie diese vollständig einfärbt--so lässt sich ein Sprite um weniger als ein ganzes Pixel bewegen.

Die Einstellung für die verwendete Filterung wird in der Datei mit den [Projekteinstellungen](/manuals/project-settings/#graphics) gespeichert. Es gibt zwei Einstellungen:

default_texture_min_filter
: Die Filterung bei Verkleinerung wird angewendet, wenn das Texel kleiner als das Bildschirmpixel ist.

default_texture_mag_filter
: Die Filterung bei Vergrößerung wird angewendet, wenn das Texel größer als das Bildschirmpixel ist.

Beide Einstellungen akzeptieren die Werte `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` oder `linear_mipmap_linear`. Zum Beispiel:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Wenn du nichts angibst, sind beide standardmäßig auf `linear` gesetzt.

Beachte, dass die Einstellung in *game.project* von den Standard-Samplern verwendet wird. Wenn du Sampler in einem benutzerdefinierten Material angibst, kannst du die Filtermethode für jeden Sampler gesondert festlegen. Einzelheiten findest du im [Handbuch zu Materialien](/manuals/material/).
