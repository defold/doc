---
title: Defold'da GUI parçacık efektleri
brief: Bu kılavuz, parçacık efektlerinin Defold GUI içinde nasıl çalıştığını açıklar.
---

# GUI ParticleFX düğümleri

Parçacık efekti düğümü (particle effect node), GUI ekran uzayında (screen space) parçacık efekti sistemlerini oynatmak için kullanılır.

## Parçacık efekti düğümleri ekleme

Yeni parçacık düğümleri eklemek için *Outline* görünümünde <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ ParticleFX</kbd> seçeneğini seçin ya da <kbd>A</kbd> tuşuna basıp <kbd>ParticleFX</kbd> seçeneğini seçin.

GUI içine eklediğiniz parçacık efektlerini efektin kaynağı olarak kullanabilirsiniz. Parçacık efektleri eklemek için *Outline* görünümündeki *Particle FX* klasör simgesine <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Particle FX...</kbd> seçeneğini seçin. Ardından düğümün *Particlefx* özelliğini ayarlayın:

![Parçacık efekti](images/gui-particlefx/create.png)

## Efekti denetleme {#controlling-the-effect}

Düğümü bir betikten denetleyerek efekti başlatabilir ve durdurabilirsiniz:

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

Parçacık efektlerinin nasıl çalıştığıyla ilgili ayrıntılar için [Parçacık efektleri kılavuzuna](/manuals/particlefx) bakın.
