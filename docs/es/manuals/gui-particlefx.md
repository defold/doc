---
title: Particle fx de GUI en Defold
brief: Este manual explica cómo funcionan los efectos de partículas en la GUI de Defold.
---

# Nodos ParticleFX de GUI

Un nodo de efecto de partículas se usa para reproducir sistemas de efectos de partículas en el espacio de pantalla de la GUI.

## Añadir nodos Particle FX

Añade nuevos nodos de partículas haciendo <kbd>click derecho</kbd> en *Outline* y seleccionando <kbd>Add ▸ ParticleFX</kbd>, o presiona <kbd>A</kbd> y selecciona <kbd>ParticleFX</kbd>.

Puedes usar como origen del efecto los efectos de partículas que hayas añadido a la GUI. Añade efectos de partículas haciendo <kbd>click derecho</kbd> en el icono de carpeta *Particle FX* en *Outline* y seleccionando <kbd>Add ▸ Particle FX...</kbd>. Luego configura la propiedad *Particlefx* en el nodo:

![Particle fx](images/gui-particlefx/create.png)

## Controlar el efecto

Puedes iniciar y detener el efecto controlando el nodo desde un script:

```lua
-- iniciar el efecto de partículas
local particles_node = gui.get_node("particlefx")
gui.play_particlefx(particles_node)
```

```lua
-- detener el efecto de partículas
local particles_node = gui.get_node("particlefx")
gui.stop_particlefx(particles_node)
```

Consulta el [manual de Particle FX](/manuals/particlefx) para obtener detalles sobre cómo funcionan los efectos de partículas.
