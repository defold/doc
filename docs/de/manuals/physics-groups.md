---
title: Kollisionsgruppen in Defold
brief: Die Physik-Engine ermöglicht dir, deine Physikobjekte zu gruppieren und durch Filter festzulegen, wie sie miteinander kollidieren sollen.
---

# Gruppe und Maske {#group-and-mask}

Die Physik-Engine ermöglicht dir, deine Physikobjekte zu gruppieren und durch Filter festzulegen, wie sie miteinander kollidieren sollen. Dafür werden benannte _Kollisionsgruppen_ (collision groups) verwendet. Bei jedem Kollisionsobjekt (collision object), das du erstellst, steuern zwei Eigenschaften, wie das Objekt mit anderen Objekten kollidiert: *Group* und *Mask*.

Damit eine Kollision zwischen zwei Objekten registriert wird, müssen beide Objekte im Feld *Mask* jeweils die Gruppe des anderen Objekts angeben.

![Kollisionsgruppe der Physik-Engine](images/physics/collision_group.png)

Das Feld *Mask* kann mehrere Gruppennamen enthalten und ermöglicht dadurch komplexe Interaktionsszenarien.

## Kollisionen erkennen {#detecting-collisions}
Wenn zwei Kollisionsobjekte mit zueinander passenden Gruppen und Masken kollidieren, erzeugt die Physik-Engine [Kollisionsnachrichten](/manuals/physics-messages), die du in Spielen verwenden kannst, um auf Kollisionen zu reagieren.
