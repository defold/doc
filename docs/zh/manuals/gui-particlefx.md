---
title: Defold里的GUI粒子特效
brief: 本教程解释了 Defold GUI 的粒子特效如何工作.
---

# GUI ParticleFX 节点

粒子特效节点用来在 GUI 屏幕空间中实现粒子特效.

## 添加 Particle FX 节点

在 *outline 视图* 中点击 <kbd>鼠标右键</kbd> 选择 <kbd>Add ▸ ParticleFX</kbd>, 或者按 <kbd>A</kbd> 选择 <kbd>ParticleFX</kbd> 来添加新粒子节点.

也可以使用 GUI 里已经存在的资源创建粒子特效. 在 *outline 视图* 的 *Particle FX* 文件夹上点击 <kbd>鼠标右键</kbd> 选择 <kbd>Add ▸ Particle FX...</kbd>. 然后设置节点的 *Particlefx* 属性:

![Particle fx](images/gui-particlefx/create.png)

## 控制特效

可以使用脚本控制节点上的特效:

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

详情请见 [粒子特效教程](/manuals/particlefx).