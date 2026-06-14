---
title: GUI particle fx no Defold
brief: Este manual explica como efeitos de partículas funcionam na GUI do Defold.
---

# Nodes GUI ParticleFX

Um node de efeito de partículas é usado para reproduzir sistemas de efeitos de partículas no espaço de tela da GUI.

## Adicionando nodes Particle FX

Adicione novos nodes de partículas clicando com o botão direito no *Outline* e selecionando <kbd>Add ▸ ParticleFX</kbd>, ou pressione <kbd>A</kbd> e selecione <kbd>ParticleFX</kbd>.

Você pode usar efeitos de partículas adicionados à GUI como fonte para o efeito. Adicione efeitos de partículas clicando com o botão direito no ícone da pasta *Particle FX* no *Outline* e selecionando <kbd>Add ▸ Particle FX...</kbd>. Em seguida, defina a propriedade *Particlefx* no node:

![Particle fx](images/gui-particlefx/create.png)

## Controlando o efeito {#controlling-the-effect}

Você pode iniciar e parar o efeito controlando o node a partir de um script:

```lua
-- inicia o efeito de partículas
local particles_node = gui.get_node("particlefx")
gui.play_particlefx(particles_node)
```

```lua
-- para o efeito de partículas
local particles_node = gui.get_node("particlefx")
gui.stop_particlefx(particles_node)
```

Consulte o [manual de Particle FX](/manuals/particlefx) para detalhes sobre como efeitos de partículas funcionam.
