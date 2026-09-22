---
title: Effetti particellari nella GUI di Defold
brief: Questo manuale spiega come funzionano gli effetti particellari nella GUI di Defold.
---

# Nodi ParticleFX della GUI {#gui-particlefx-nodes}

Un nodo per effetti particellari permette di riprodurre sistemi di effetti particellari nello spazio dello schermo della GUI.

## Aggiunta di nodi Particle FX {#adding-particle-fx-nodes}

Aggiungi nuovi nodi particellari facendo <kbd>clic con il pulsante destro del mouse</kbd> nella vista *Outline* e selezionando <kbd>Add ▸ ParticleFX</kbd>, oppure premi <kbd>A</kbd> e seleziona <kbd>ParticleFX</kbd>.

Puoi utilizzare come sorgente dell'effetto gli effetti particellari che hai aggiunto alla GUI. Per aggiungere effetti particellari, fai <kbd>clic con il pulsante destro del mouse</kbd> sull'icona della cartella *Particle FX* nella vista *Outline* e seleziona <kbd>Add ▸ Particle FX...</kbd>. Imposta quindi la proprietà *Particlefx* del nodo:

![Effetti particellari](images/gui-particlefx/create.png)

## Controllo dell'effetto {#controlling-the-effect}

Puoi avviare e arrestare l'effetto controllando il nodo da uno script:

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

Consulta il [manuale degli effetti particellari](/manuals/particlefx) per informazioni dettagliate sul funzionamento degli effetti particellari.
