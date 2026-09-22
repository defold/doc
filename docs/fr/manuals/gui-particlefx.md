---
title: Effets de particules dans l'interface graphique de Defold
brief: Ce manuel explique le fonctionnement des effets de particules dans l'interface graphique de Defold.
---

# Nœuds ParticleFX d'interface graphique {#gui-particlefx-nodes}

Un nœud d'effet de particules sert à jouer des systèmes d'effets de particules dans l'espace écran de l'interface graphique.

## Ajout de nœuds Particle FX {#adding-particle-fx-nodes}

Pour ajouter de nouveaux nœuds de particules, faites un <kbd>clic droit</kbd> dans la vue *Outline* et sélectionnez <kbd>Add ▸ ParticleFX</kbd>, ou appuyez sur <kbd>A</kbd> et sélectionnez <kbd>ParticleFX</kbd>.

Vous pouvez utiliser les effets de particules que vous avez ajoutés à l'interface graphique comme source de l'effet. Ajoutez des effets de particules en faisant un <kbd>clic droit</kbd> sur l'icône du dossier *Particle FX* dans la vue *Outline*, puis en sélectionnant <kbd>Add ▸ Particle FX...</kbd>. Définissez ensuite la propriété *Particlefx* du nœud :

![Effet de particules](images/gui-particlefx/create.png)

## Contrôle de l'effet {#controlling-the-effect}

Vous pouvez démarrer et arrêter l'effet en contrôlant le nœud depuis un script :

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

Consultez le [manuel sur les effets de particules](/manuals/particlefx) pour plus de détails sur le fonctionnement des effets de particules.
