---
title: GUI particle fx in Defold
brief: This manual explains how particle effects work in the Defold GUI.
---

# GUI ParticleFX nodes

A particle effect node is used to play particle effect systems in the GUI screen space.

## Adding Particle FX nodes

Add new particle nodes by either <kbd>right clicking</kbd> in the *Outline* and selecting <kbd>Add ▸ ParticleFX</kbd>, or press <kbd>A</kbd> and select <kbd>ParticleFX</kbd>.

You can use particle effects that you have added to the GUI as source for the effect. Add particle effects by <kbd>right clicking</kbd> the *Particle FX* folder icon in the *Outline* and selecting <kbd>Add ▸ Particle FX...</kbd>. Then set the *Particlefx* property on the node:

![Particle fx](images/gui-particlefx/create.png){srcset="images/gui-particlefx/create@2x.png 2x"}

## Controlling the effect

You can start and stop the effect by controlling the node from a script:

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

See the [Particle FX manual](/manuals/particlefx) for details on how particle effects work.