---
title: Defold 中的 3D 模型动画手册
brief: 本手册介绍了如何在 Defold 中使用 3D 模型动画。
---

# 3D 蒙皮动画

3D 模型的骨骼动画使用模型的骨骼对模型中的顶点应用变形。

关于如何将 3D 数据导入到模型中以进行动画的详细信息，请参阅[模型文档](/manuals/model)。

  ![Blender animation](images/animation/blender_animation.png)
  ![Wiggle loop](images/animation/suzanne.gif)


## 播放动画

模型使用[`model.play_anim()`](/ref/model#model.play_anim)函数进行动画处理：

```lua
function init(self)
    -- 在 #model 上来回播放 "wiggle" 动画
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold 目前仅支持烘焙动画。动画需要为每个动画骨骼的每个关键帧设置矩阵，而不是将位置、旋转和缩放作为单独的键。

动画也是线性插值的。如果您进行更高级的曲线插值，动画需要从导出器进行预烘焙。

不支持 Collada 中的动画剪辑。要对每个模型使用多个动画，请将它们导出到单独的 *.dae* 文件中，然后在 Defold 中将这些文件收集到一个 *.animationset* 文件中。
:::

### 骨骼层级

模型骨架中的骨骼在内部表示为游戏对象。

您可以在运行时检索骨骼游戏对象的实例 id。函数[`model.get_go()`](/ref/model#model.get_go)返回指定骨骼的游戏对象的 id。

```lua
-- 获取我们 wiggler 模型的中间骨骼游戏对象
local bone_go = model.get_go("#wiggler", "Bone_002")

-- 现在可以对游戏对象做一些有用的操作...
```

### 游标动画

除了使用`model.play_anim()`来推进模型动画外，*Model*组件还公开了一个"游标"属性，可以使用`go.animate()`进行操作（有关[属性动画](/manuals/property-animation)的更多信息）：

```lua
-- 在 #model 上设置动画但不启动它
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- 将游标设置为动画的开头
go.set("#model", "cursor", 0)
-- 使用 in-out quad 缓动在 0 和 1 之间对游标进行 pingpong 补间。
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## 完成回调

模型动画`model.play_anim()`支持一个可选的 Lua 回调函数作为最后一个参数。当动画播放到结束时将调用此函数。对于循环动画，或者当动画通过`go.cancel_animations()`手动取消时，永远不会调用该函数。回调可用于在动画完成时触发事件或将多个动画链接在一起。

```lua
local function wiggle_done(self, message_id, message, sender)
    -- 动画完成
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## 播放模式

动画可以播放一次或循环播放。动画的播放方式由播放模式决定：

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
