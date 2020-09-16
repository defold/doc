---
title: Defold 的粒子特效
brief: 本教程介绍了粒子特效组件的使用以及特效的编辑方法.
---

# 粒子特效

粒子特效用以为游戏呈现视觉效果.可以用来表现爆炸, 喷血, 拖尾, 天气等等效果.

![ParticleFX Editor](images/particlefx/editor.png){srcset="images/particlefx/editor@2x.png 2x"}

粒子特效包含一些发射器以及可选的修改器:

Emitter
: 发射器是任意放置的的形状，可发射均匀分布在该形状上的粒子。发射器包含控制粒子生成的属性，比如各个粒子的图像或动画，生命周期，颜色，形状和速度。

Modifier
: 修改器会影响生成的粒子的速度，以使其在特定方向上加速或减速，径向移动或绕点旋转。修改器可以影响单个的粒子或者整个发射器。

## 新建粒子特效

在  *Assets* 浏览器菜单栏选择 <kbd>New... ▸ Particle FX</kbd>. 为新建粒子特效命名. 编辑器会为其自动打开 [场景编辑器](/manuals/editor/#the-scene-editor).

在 *Outline* 面板中显示出默认粒子发射器. 点选发射器 *Properties* 面板会对应更新.

![Default particles](images/particlefx/default.png){srcset="images/particlefx/default@2x.png 2x"}

新建发射器, <kbd>右键点击</kbd> *Outline* 视图, 从上下文菜单中选择 <kbd>Add Emitter ▸ [type]</kbd>. 其中发射器类型可以创建后在属性里更改.

新建修改器, <kbd>右键点击</kbd> *Outline* 视图里的发射器, 从上下文菜单中选择 <kbd>Add Modifier</kbd>, 再选择修改器类型.

![Add modifier](images/particlefx/add_modifier.png){srcset="images/particlefx/add_modifier@2x.png 2x"}

![Add modifier select](images/particlefx/add_modifier_select.png){srcset="images/particlefx/add_modifier_select@2x.png 2x"}

在根节点 (而不是发射器子级) 上添加的修改器会作用域所有粒子.

作为在发射器子集添加的修改器只会作用域该发射器的粒子.

## 预览效果

* 菜单栏选择 <kbd>View ▸ Play</kbd>. 配合摄像机缩放进行预览.
* 再次选择 <kbd>View ▸ Play</kbd> 会暂停效果预览.
* 选择 <kbd>View ▸ Stop</kbd> 结束预览. 再次预览时会重新初始化粒子效果.

在发射器和修改器上做的属性修改会立即反映在预览之中, 即使是在暂停状态:

![Edit particles](images/particlefx/rotate.gif)

## 发射器属性

Id
: 发射器名 (为发射器设置渲染常量时会用到).

Position/Rotation
: 基于粒子特效组件的位置/旋转.

Play Mode
: 用于控制播放模式:
  - `Once` 播放结束后即停止.
  - `Loop` 播放结束后再次播放.

Size Mode
: 用于控制逐帧动画的大小:
  - `Auto` 基于图片大小.
  - `Manual` 基于 size 设置.

Emission Space
: 把粒子发射在哪里:
  - `World` 世界空间.
  - `Emitter` 发射器空间.

Duration
: 多少秒发射一次粒子.

Start Delay
: 发射前等待多少秒.

Start Offset
: 起始效果偏移秒数, 换句话说就是发射器发射粒子的预热时间.

Image
: 粒子使用的图片 (来自瓷砖图源或者图集资源).

Animation
: 粒子用的基于 *图片* 的逐帧动画资源文件.

Material
: 粒子材质.

Blend Mode
: 混合模式, 可以选择 `Alpha`, `Add` 或者 `Multiply`.

Max Particle Count
: 当前发射器允许同时存在的最多粒子数量.

Emitter Type
: 发射器形状
  - `Circle` 从圆的内部随机位置发射粒子. 发射方向背向圆心. 圆直径基于 *发射器 Size 的X值*.

  - `2D Cone` 从锥形(三角形)的内部随机位置发射粒子. 发射方向为锥顶到锥底. 宽度基于 *发射器 Size 的X值*, 高度基于 *Y值*.

  - `Box` 从盒子的内部随机位置发射粒子. 发射方向延盒子本地 Y 轴方向. *发射器 Size 的X值*, *Y值* 和 *Z值* 分别定义宽度, 高度和长度. 如果需要2D矩形, 把Z值设置为0即可.

  - `Sphere` 从球体的内部随机位置发射粒子. 发射方向背向球心. 球体的直径基于 *发射器 Size 的X值*.

  - `Cone` 从锥体的内部随机位置发射粒子. 发射方向为锥顶到锥底. 宽度基于 *发射器 Size 的X值*, 高度基于 *Y值*.

  ![emitter types](images/particlefx/emitter_types.png){srcset="images/particlefx/emitter_types@2x.png 2x"}

Particle Orientation
: 粒子移动方向:
  - `Default` 元向量方向
  - `Initial Direction` 粒子初始化方向.
  - `Movement Direction` 速度向量方向.

Inherit Velocity
: 粒子继承发射器速度的比例. 仅当 *Space* 设置为 `World` 时有效. 发射器速度每帧更新.

Stretch With Velocity
: 延移动方向拉伸粒子.

### 混合模式
:[blend-modes](../shared/blend-modes.md)

## 发射器非固定属性

这种属性分为两个部分: 一个数值和一个抖动. 抖动就是施加于粒子上的随机数值. 比如数值是 50 抖动是 3, 则最终值的范围就是 47 到 53 (50 +/- 3).

![Property](images/particlefx/property.png){srcset="images/particlefx/property@2x.png 2x"}

点击关键帧按钮, 则属性值由一条曲线决定. 恢复数值加抖动模式, 取消点选关键帧按钮即可.

![Property keyed](images/particlefx/key.png){srcset="images/particlefx/key@2x.png 2x"}

*曲线编辑器* (位于视口下方) 用以修改曲线. 这种属性不会显示在 *属性* 视图中, 只能显示在 *曲线编辑器* 中. 通过 <kbd>点击拖动</kbd> 控制点与其切线来修改曲线形状. <kbd>双击</kbd> 曲线添加控制点. <kbd>双击</kbd> 控制点可以删除它.

![ParticleFX Curve Editor](images/particlefx/curve_editor.png){srcset="images/particlefx/curve_editor@2x.png 2x"}

自动缩放显示完整曲线快捷键为 <kbd>F</kbd>.

以下属性都可以基于发射器发射时间周期用曲线表示:

Spawn Rate
: 每秒发射粒子数.

Emitter Size X/Y/Z
: 发射器大小, 参考上述 *Emitter Type*.

Particle Life Time
: 粒子生存周期, 单位是秒.

Initial Speed
: 粒子初始速度.

Initial Size
: 粒子初始大小. 如果把 *Size Mode* 设置为 `Automatic` 并且粒子使用基于图片大小的逐帧动画的话, 此属性无效.

Initial Red/Green/Blue/Alpha
: 粒子初始颜色及其不透明度.

Initial Rotation
: 粒子初始角度 (角度制).

Initial Stretch X/Y
: 粒子初始拉伸.

Initial Angular Velocity
: 粒子初始角速度 (度/每秒).

以下属性都可以基于粒子的生命周期用曲线表示:

Life Scale
: 粒子缩放.

Life Red/Green/Blue/Alpha
: 粒子颜色及其不透明度.

Life Rotation
: 粒子旋转角度 (角度制).

Life Stretch X/Y
: 粒子拉伸.

Life Angular Velocity
: 粒子角速度 (度/每秒).

## 修改器

粒子的速度受以下四种修改器影响:

`Acceleration`
: 在某方向上加速.

`Drag`
: 在粒子方向上的阻尼.

`Radial`
: 在径向方向上吸引或排斥.

`Vortex`
: 让粒子圆周运动或者漩涡式弧线运动.

  ![modifiers](images/particlefx/modifiers.png){srcset="images/particlefx/modifiers@2x.png 2x"}

## 修改器属性

Position/Rotation
: 修改器相对父级的位移.

Magnitude
: 修改器对粒子的影响强度.

Max Distance
: 受修改器影响的粒子最远距离. 仅支持 Radial 和 Vortex.

## 控制粒子特效

开始/停止粒子特效播放的脚本命令:

```lua
-- 开始当前游戏对象上的粒子特效组件 "particles" 的播放
particlefx.play("#particles")

-- 停止当前游戏对象上的粒子特效组件 "particles" 的播放
particlefx.stop("#particles")
```

::: 注意
即使粒子特效组件依附的游戏对象被删除, 粒子效果也不会停止播放.
:::
详情请见 [粒子特效索引文档](/ref/particlefx).

## 材质常量

粒子特效默认的材质常量可以使用 `particlefx.set_constant()` 和 `particlefx.reset_constant()` 进行设置和重置 (详情请见 [材质教程](/manuals/material/#vertex-and-fragment-constants)):

`tint`
: 粒子特效染色 (`vector4`). 四元组的 x, y, z, 和 w 分别对应红, 绿, 蓝和不透明度. 详情请见 [API 文档上的示例](/ref/particlefx/#particlefx.set_constant:url-constant-value

## 相关项目配置

在 *game.project* 文件里有些关于粒子效果的 [设置项目](/manuals/project-settings#particle-fx).
