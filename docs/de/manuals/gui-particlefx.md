---
title: GUI-Partikeleffekte in Defold
brief: Dieses Handbuch erklärt, wie Partikeleffekte in der GUI von Defold funktionieren.
---

# GUI-Partikeleffektknoten {#gui-particlefx-nodes}

Ein Partikeleffektknoten (particle effect node) dient dazu, Partikeleffektsysteme im Bildschirmkoordinatensystem der GUI abzuspielen.

## Partikeleffektknoten hinzufügen {#adding-particle-fx-nodes}

Füge neue Partikelknoten hinzu, indem du in der Ansicht *Outline* einen <kbd>Rechtsklick</kbd> ausführst und <kbd>Add ▸ ParticleFX</kbd> auswählst, oder drücke <kbd>A</kbd> und wähle <kbd>ParticleFX</kbd>.

Du kannst Partikeleffekte, die du der GUI hinzugefügt hast, als Quelle für den Effekt verwenden. Füge Partikeleffekte hinzu, indem du einen <kbd>Rechtsklick</kbd> auf das Ordnersymbol *Particle FX* in der Ansicht *Outline* ausführst und <kbd>Add ▸ Particle FX...</kbd> auswählst. Lege dann die Eigenschaft *Particlefx* des Knotens fest:

![Partikeleffekt](images/gui-particlefx/create.png)

## Den Effekt steuern {#controlling-the-effect}

Du kannst den Effekt starten und stoppen, indem du den Knoten aus einem Skript heraus steuerst:

```lua
-- start the particle effect
local particles_node = gui.get_node("particlefx")
gui.play_particlefx(particles_node)
```

```lua
-- stop the particle effect
local particles_node = gui.get_node("particlefx")
gui.stop_particlefx(particles_node)
```

Weitere Informationen zur Funktionsweise von Partikeleffekten findest du im [Handbuch zu Partikeleffekten](/manuals/particlefx).
