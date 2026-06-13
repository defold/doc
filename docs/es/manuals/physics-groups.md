---
title: Grupos de colisión en Defold
brief: El motor de físicas te permite agrupar tus objetos físicos y filtrar cómo deben colisionar.
---

# Grupo y máscara

El motor de físicas te permite agrupar tus objetos físicos y filtrar cómo deben colisionar. Esto se gestiona mediante _grupos de colisión_ con nombre. Para cada objeto de colisión que creas, dos propiedades controlan cómo colisiona el objeto con otros objetos: *Group* y *Mask*.

Para que se registre una colisión entre dos objetos, ambos objetos deben especificar mutuamente los grupos del otro en el campo *Mask*.

![Grupo de colisión de físicas](images/physics/collision_group.png)

El campo *Mask* puede contener varios nombres de grupo, lo que permite escenarios de interacción complejos.

## Detección de colisiones
Cuando dos objetos de colisión con grupos y máscaras coincidentes colisionan, el motor de físicas generará [mensajes de colisión](/manuals/physics-messages) que se pueden usar en los juegos para reaccionar ante las colisiones.
