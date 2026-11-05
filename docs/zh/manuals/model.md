---
title: Defold 3D模型
brief: 本手册介绍了如何将3D模型、骨骼和动画带入您的游戏之中。
---

# 模型组件 {#model-component}

Defold 本质上是一个3D引擎。即使您只使用2D材质，所有渲染也是在3D中完成的，只是正交投影到屏幕上。Defold允许您通过在集合中包含3D资产或_模型_来充分利用完整的3D内容。您可以仅使用3D资产构建纯3D游戏，或者根据需要混合3D和2D内容。

## 创建模型组件 {#creating-a-model-component}

模型组件的创建方式与任何其他游戏对象组件一样。您可以通过两种方式完成：

- 在*Assets*浏览器中<kbd>右键单击</kbd>一个位置，然后选择<kbd>新建... ▸ 模型</kbd>来创建*模型文件*。
- 在*Outline*视图中<kbd>右键单击</kbd>一个游戏对象，然后选择<kbd>添加组件 ▸ 模型</kbd>，将组件直接嵌入到游戏对象中。

![游戏对象中的模型](images/model/model_gltf.png)

创建模型后，您需要指定多个属性：

### 模型属性 {#model-properties}

除了*Id*、*位置*和*旋转*属性外，还存在以下组件特定属性：

*Scene*
: 包含模型几何体的 glTF *.gltf* 或 *.glb* 文件。如果文件包含变形目标，它们会与场景一起导入。此属性以前名为 *Mesh*。

*Mesh*
: 所选 *Scene* 中的可选命名网格。将此字段留空可使用导入的变换渲染整个场景。选择一个网格会在其局部坐标中渲染一次该网格，不应用 glTF 节点变换。通过移动、旋转和缩放模型组件或其游戏对象来放置选定的网格。

*Create GO Bones*
: 勾选此项会为模型的每根骨骼创建一个游戏对象。您可以使用这些游戏对象将其他游戏对象附加到骨骼上，例如把武器附加到手部骨骼等。

*Skeleton*
: 此属性应引用包含用于动画的骨架的 glTF *.gltf* 或 *.glb* 文件。请注意，Defold 要求您的层次结构中有一个单一的根骨骼。

*Animations*
: 将此设置为包含您想要在模型上使用的动画的*动画集文件*。

*Default Animation*
: 这是将自动在模型上播放的动画（来自动画集）。

除了上述属性之外，还会有一个字段用于为模型的每个网格指定材质：

*Material*
: 将此属性设为适合模型的材质。使用内置 `gltf` 材质可对 glTF 材质属性进行基于物理的渲染，内置 `model` 材质适合常规模型着色，也可以使用自定义材质。请参阅[下方的材质变体](#material)和 [PBR 手册](/manuals/physically-based-rendering/#built-in-pbr-materials)。

根据材质的不同，会有一个或多个纹理属性：

*Texture*
: 此属性应指向要应用到对象的纹理图像。它可以是独立的项目资源，也可以是 *Assets* 面板中 glTF 或 GLB 文件下暴露的内嵌图像。

选择 glTF 或 GLB *Scene*，或改变其 *Mesh* 选择时，可能会提示填充材质和纹理绑定。<kbd>Auto Fill</kbd> 用源文件的绑定替换现有绑定；<kbd>Keep Current</kbd> 则在应用新的场景或网格选择时保留绑定。请参阅[模型导入流程](/manuals/importing-models/#using-a-model)。


## 编辑器操作 {#editor-manipulation}

有了模型组件后，您就可以自由地使用常规的*场景编辑器*工具编辑和操作组件和/或封装游戏对象，以按照您的喜好移动、旋转和缩放模型。

## 运行时操作 {#runtime-manipulation}

您可以通过多种不同的函数和属性在运行时操作模型（有关用法请参阅[API文档](/ref/model/)）。

![游戏中的Wiggler](images/model/runtime.png)

### 运行时动画 {#runtime-animation}

Defold为在运行时控制动画提供了强大的支持。更多内容请参阅[模型动画手册](/manuals/model-animation)：

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

动画播放游标可以手动或通过属性动画系统进行动画处理：

```lua
-- 设置运行动画
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- 为游标设置动画
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

模型也可以使用 glTF 变形目标动画。变形目标权重会像其他模型动画一样通过 `model.play_anim()` 进行动画处理，并且可以在运行时使用 [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) 和 [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) 读取或覆盖。详情请参阅模型动画手册中的[变形目标部分](/manuals/model-animation#morph-targets)。

### 更改属性 {#changing-properties}

模型还有许多不同的属性，可以使用`go.get()`和`go.set()`进行操作：

`animation`
: 当前模型动画（`hash`）（只读）。您使用`model.play_anim()`更改动画（见上文）。

`cursor`
: 标准化的动画游标（`number`）。

`material`
: 模型材质（`hash`）。您可以使用材质资源属性和`go.set()`更改此设置。有关示例，请参阅[API参考](/ref/model/#material)。

`playback_rate`
: 动画播放速率（`number`）。

`textureN`
: 模型纹理，其中 N 为 0-15（`hash`）。您可以使用 `go.get()` 读取这些属性，并使用纹理资源属性和 `go.set()` 更改它们。Defold 每次绘制最多支持 16 个纹理，但在纹理采样器限制较低的图形适配器上，着色器可用的数量可能更少。


## 材质 {#material}

3D软件通常允许您在对象顶点上设置属性，比如着色和纹理。这些信息会进入您从3D软件导出的 glTF *.gltf* 或 *.glb* 文件中。根据您游戏的需求，您必须为您的对象选择和/或创建合适的_高性能_材质。材质将_着色器程序_与一组用于对象渲染的参数结合起来。

`/builtins/materials/` 中提供以下内置材质：

| 模型类型 | 常规模型着色 | glTF PBR 着色 |
|---|---|---|
| 静态、非实例化 | `model.material` | `gltf.material` |
| 静态、实例化 | `model_instanced.material` | `gltf_instanced.material` |
| 蒙皮（动画）、非实例化 | `model_skinned.material` | `gltf_skinned.material` |
| 蒙皮（动画）、实例化 | `model_skinned_instanced.material` | `gltf_skinned_instanced.material` |

`gltf` 材质使用导入的 glTF 材质数据提供内置的金属度/粗糙度光照。纹理绑定、光源和自定义着色器请参阅 [PBR 手册](/manuals/physically-based-rendering/#built-in-pbr-materials)。

所有这些内置材质都使用局部顶点空间。对于蒙皮模型，局部顶点空间允许顶点着色器通过骨骼矩阵纹理在 GPU 上执行蒙皮；模型实例化也要求局部顶点空间。因此，用于 GPU 蒙皮或实例化模型的自定义材质应将顶点空间设为 *Local*。

骨骼矩阵缓存使用 `RGBA32F` 纹理。如果当前图形适配器不支持该纹理格式，Defold 将无法创建使用局部空间材质的动画 Model 组件。因此，在 OpenGL ES 2.0 和 WebGL 1.0 上，支持情况取决于适配器的浮点纹理扩展。为兼容缺少该扩展的适配器，请使用自定义世界空间材质；它使用 CPU 蒙皮，且不能使用模型实例化。可通过[模型项目设置](/manuals/project-settings/#model)调整缓存尺寸。

如果您需要为模型创建自定义材质，请参阅[材质文档](/manuals/material)获取信息。[着色器手册](/manuals/shader)包含有关着色器程序如何工作的信息。


### 材质常量 {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: 模型的颜色色调（`vector4`）。`vector4`用于表示色调，x、y、z和w分别对应红色、绿色、蓝色和alpha色调。


## 渲染 {#rendering}

默认渲染脚本会绘制带 `model` 标签的材质，包括内置 model 和 glTF 材质。要在自定义渲染脚本中渲染它们，请创建匹配的谓词，并使用适合场景的视图和投影矩阵绘制。例如：

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- 正交投影
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

有关渲染脚本如何工作的详细信息，请参阅[渲染文档](/manuals/render)。
