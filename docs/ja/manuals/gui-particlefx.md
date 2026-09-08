---
title: Defold の GUI パーティクルエフェクト
brief: このマニュアルでは、Defold の GUI でパーティクルエフェクトがどのように動作するかを説明します。
---

# GUI ParticleFX ノード {#gui-particlefx-nodes}

パーティクルエフェクトノード（particle effect node）は、GUI のスクリーン空間でパーティクルエフェクトシステムを再生するために使用します。

## パーティクルエフェクトノードの追加 {#adding-particle-fx-nodes}

新しいパーティクルノードを追加するには、*Outline* 内で <kbd>右クリック</kbd>して <kbd>Add ▸ ParticleFX</kbd> を選択するか、<kbd>A</kbd> を押して <kbd>ParticleFX</kbd> を選択します。

GUI に追加したパーティクルエフェクトを、エフェクトのソースとして使用できます。パーティクルエフェクトを追加するには、*Outline* 内の *Particle FX* フォルダーアイコンを <kbd>右クリック</kbd>して <kbd>Add ▸ Particle FX...</kbd> を選択します。次に、ノードの *Particlefx* プロパティを設定します:

![パーティクルエフェクト](images/gui-particlefx/create.png)

## エフェクトの制御 {#controlling-the-effect}

スクリプトからノードを制御することで、エフェクトを開始および停止できます:

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

パーティクルエフェクトの動作の詳細については、[パーティクルエフェクトマニュアル](/manuals/particlefx)を参照してください。
