---
title: Defold 3D模型
brief: 本手册介绍了如何将3D模型、骨骼和动画带入您的游戏之中。
---

# 模型组件

Defold 本质上是一个3D引擎。即使您只使用2D材质，所有渲染也是在3D中完成的，只是正交投影到屏幕上。Defold允许您通过在集合中包含3D资产或_模型_来充分利用完整的3D内容。您可以仅使用3D资产构建纯3D游戏，或者根据需要混合3D和2D内容。

## 创建模型组件

模型组件的创建方式与任何其他游戏对象组件一样。您可以通过两种方式完成：

- 在*Assets*浏览器中<kbd>右键单击</kbd>一个位置，然后选择<kbd>新建... ▸ 模型</kbd>来创建*模型文件*。
- 在*Outline*视图中<kbd>右键单击</kbd>一个游戏对象，然后选择<kbd>添加组件 ▸ 模型</kbd>，将组件直接嵌入到游戏对象中。

![游戏对象中的模型](images/model/model.png)

创建模型后，您需要指定多个属性：

### 模型属性

除了*Id*、*位置*和*旋转*属性外，还存在以下组件特定属性：

*网格*
: 此属性应引用包含要使用的网格的glTF *.gltf*或Collada *.dae*文件。如果文件包含多个网格，则只读取第一个。

*材质*
: 将此属性设置为您创建的适合纹理3D对象的材质。有一个内置的*model.material*文件，您可以用它作为起点。

*纹理*
: 此属性应指向您想要应用于对象的纹理图像文件。

*骨骼*
: 此属性应引用包含用于动画的骨骼的glTF *.gltf*或Collada *.dae*文件。请注意，Defold要求您的层次结构中有一个单一的根骨骼。

*动画*
: 将此设置为包含您想要在模型上使用的动画的*动画集文件*。

*默认动画*
: 这是将自动在模型上播放的动画（来自动画集）。

## 编辑器操作

有了模型组件后，您就可以自由地使用常规的*场景编辑器*工具编辑和操作组件和/或封装游戏对象，以按照您的喜好移动、旋转和缩放模型。

![游戏中的Wiggler](images/model/ingame.png)

## 运行时操作

您可以通过多种不同的函数和属性在运行时操作模型（有关用法请参阅[API文档](/ref/model/)）。

### 运行时动画

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

### 更改属性

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
: 模型纹理，其中N为0-7（`hash`）。您可以使用纹理资源属性和`go.set()`更改此设置。有关示例，请参阅[API参考](/ref/model/#textureN)。


## 材质

3D软件通常允许您在对象顶点上设置属性，比如着色和纹理。这些信息会进入您从3D软件导出的glTF *.gltf*或Collada *.dae*文件中。根据您游戏的需求，您必须为您的对象选择和/或创建合适的_高性能_材质。材质将_着色器程序_与一组用于对象渲染的参数结合起来。

在内置材质文件夹中有一个简单的3D模型材质可用。如果您需要为模型创建自定义材质，请参阅[材质文档](/manuals/material)获取信息。[着色器手册](/manuals/shader)包含有关着色器程序如何工作的信息。


### 材质常量

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: 模型的颜色色调（`vector4`）。vector4用于表示色调，x、y、z和w分别对应红色、绿色、蓝色和alpha色调。


## 渲染

默认渲染脚本是为2D游戏量身定制的，不适用于3D模型。但是通过复制默认渲染脚本并向渲染脚本添加少量代码行，您就可以启用模型的渲染。例如：

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(render.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

有关渲染脚本如何工作的详细信息，请参阅[渲染文档](/manuals/render)。
