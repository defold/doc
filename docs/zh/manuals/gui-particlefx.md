---
title: Defold中的GUI粒子特效
brief: 本手册解释了Defold GUI中粒子特效的工作原理。
---

# GUI ParticleFX节点

粒子特效节点用于在GUI屏幕空间中播放粒子特效系统。

## 添加ParticleFX节点

通过在*Outline*中<kbd>右键点击</kbd>并选择<kbd>Add ▸ ParticleFX</kbd>，或按<kbd>A</kbd>并选择<kbd>ParticleFX</kbd>来添加新的粒子节点。

您可以使用已添加到GUI中的粒子特效作为效果的源。通过在*Outline*中的*Particle FX*文件夹图标上<kbd>右键点击</kbd>并选择<kbd>Add ▸ Particle FX...</kbd>来添加粒子特效。然后在节点上设置*Particlefx*属性：

![Particle fx](images/gui-particlefx/create.png)

## 控制效果

您可以通过脚本控制节点来启动和停止效果：

```lua
-- 启动粒子特效
local particles_node = gui.get_node("particlefx")
gui.play_particlefx(particles_node)
```

```lua
-- 停止粒子特效
local particles_node = gui.get_node("particlefx")
gui.stop_particlefx(particles_node)
```

有关粒子特效工作原理的详细信息，请参阅[粒子特效手册](/manuals/particlefx)。