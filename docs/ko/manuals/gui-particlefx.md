---
title: Defold GUI ParticleFX
brief: 이 매뉴얼은 Defold GUI에서 파티클 효과가 작동하는 방식을 설명합니다.
---

# GUI ParticleFX 노드

ParticleFX 노드는 GUI 화면 공간에서 파티클 효과 시스템을 재생하는 데 사용됩니다.

## Particle FX 노드 추가하기

새 파티클 노드를 추가하려면 *Outline*에서 <kbd>마우스 오른쪽 버튼</kbd>을 누르고 <kbd>Add ▸ ParticleFX</kbd>를 선택하거나, <kbd>A</kbd>를 누른 뒤 <kbd>ParticleFX</kbd>를 선택합니다.

GUI에 추가한 파티클 효과를 노드의 효과 소스로 사용할 수 있습니다. 파티클 효과를 추가하려면 *Outline*의 *Particle FX* 폴더 아이콘을 <kbd>마우스 오른쪽 버튼</kbd>으로 누르고 <kbd>Add ▸ Particle FX...</kbd>를 선택합니다. 그런 다음 노드의 *Particlefx* 프로퍼티를 설정합니다:

![Particle fx](images/gui-particlefx/create.png)

## 효과 제어하기 {#controlling-the-effect}

스크립트에서 노드를 제어하여 효과를 시작하고 중지할 수 있습니다:

```lua
-- 파티클 효과 시작
local particles_node = gui.get_node("particlefx")
gui.play_particlefx(particles_node)
```

```lua
-- 파티클 효과 중지
local particles_node = gui.get_node("particlefx")
gui.stop_particlefx(particles_node)
```

파티클 효과가 작동하는 방식에 대한 자세한 내용은 [Particle FX 매뉴얼](/manuals/particlefx)을 참고하세요.
