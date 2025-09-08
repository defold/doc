---
title: Defold 材质手册
brief: 本手册介绍了如何使用材质、着色器常量和采样器。
---

# 材质

材质用于表达图形组件（精灵、瓦片地图、字体、GUI节点、模型等）应该如何被渲染。

材质包含 _标签_，这些信息在渲染管线中用于选择要渲染的对象。它还包含对 _着色器程序_ 的引用，这些程序通过可用的图形驱动程序编译，并上传到图形硬件，在组件每帧渲染时运行。

* 有关渲染管线的更多信息，请参阅[渲染文档](/manuals/render)。
* 有关着色器程序的深入解释，请参阅[着色器文档](/manuals/shader)。

## 创建材质

要创建材质，在 *Assets* 浏览器中右键点击目标文件夹，然后选择 <kbd>New... ▸ Material</kbd>。（您也可以从菜单中选择 <kbd>File ▸ New...</kbd>，然后选择 <kbd>Material</kbd>）。为新材质文件命名，然后点击 <kbd>Ok</kbd>。

![Material file](images/materials/material_file.png)

新材质将在 *材质编辑器* 中打开。

![Material editor](images/materials/material.png)

材质文件包含以下信息：

Name
: 材质的标识符。此名称用于在 *Render* 资源中列出材质，以将其包含在构建中。该名称也用于渲染 API 函数 `render.enable_material()`。名称应该是唯一的。

Vertex Program
: 使用材质渲染时要使用的顶点着色器程序文件（*`.vp`*）。顶点着色器程序在 GPU 上运行，用于处理组件的每个原始顶点。它计算每个顶点的屏幕位置，并可选地输出"变化"变量，这些变量被插值并输入到片段程序。

Fragment Program
: 使用材质渲染时要使用的片段着色器程序文件（*`.fp`*）。该程序在 GPU 上运行，用于处理每个原始片段（像素），其目的是决定每个片段的颜色。这通常通过纹理查找和基于输入变量（变化变量或常量）的计算来完成。

Vertex Constants
: 将传递给顶点着色器程序的统一变量。有关可用常量的列表，请参见下文。

Fragment Constants
: 将传递给片段着色器程序的统一变量。有关可用常量的列表，请参见下文。

Samplers
: 您可以选择在材质文件中配置特定的采样器。添加采样器，根据着色器程序中使用的名称命名，并根据您的喜好设置包裹和过滤设置。

Tags
: 与材质关联的标签。标签在引擎中表示为 _位掩码_，由 [`render.predicate()`](/ref/render#render.predicate) 用于收集应该一起绘制的组件。有关如何执行此操作，请参阅[渲染文档](/manuals/render)。您可以在项目中使用的最大标签数为 32。

## 属性

着色器属性（也称为顶点流或顶点属性）是一种机制，用于 GPU 如何从内存中检索顶点以渲染几何图形。顶点着色器通过使用 `attribute` 关键字指定一组流，在大多数情况下，Defold 会根据流的名称在后台自动生成和绑定数据。但是，在某些情况下，您可能希望传递每个顶点的更多数据以实现引擎不产生的特定效果。顶点属性可以使用以下字段进行配置：

Name
: 属性名称。与着色器常量类似，只有当属性配置与顶点程序中指定的属性匹配时才会使用。

Semantic type
: 语义类型指示属性的语义含义（*是什么*）和/或*如何在编辑器中显示*。例如，指定具有 `SEMANTIC_TYPE_COLOR` 的属性将在编辑器中显示颜色选择器，而数据仍将原样从引擎传递到着色器。

  - `SEMANTIC_TYPE_NONE` 默认语义类型。除了将属性材质数据直接传递到顶点缓冲区外，对属性没有其他影响（默认）
  - `SEMANTIC_TYPE_POSITION` 为属性生成每个顶点的位置数据。可以与坐标空间一起使用，以告诉引擎位置将如何计算
  - `SEMANTIC_TYPE_TEXCOORD` 为属性生成每个顶点的纹理坐标
  - `SEMANTIC_TYPE_PAGE_INDEX` 为属性生成每个顶点的页索引
  - `SEMANTIC_TYPE_COLOR` 影响编辑器如何解释属性。如果属性配置为颜色语义，将在检查器中显示颜色选择器小部件
  - `SEMANTIC_TYPE_NORMAL` 为属性生成每个顶点的法线数据
  - `SEMANTIC_TYPE_TANGENT` 为属性生成每个顶点的切线数据
  - `SEMANTIC_TYPE_WORLD_MATRIX` 为属性生成每个顶点的世界矩阵数据
  - `SEMANTIC_TYPE_NORMAL_MATRIX` 为属性生成每个顶点的法线矩阵数据

Data type
: 属性后备数据的数据类型。

  - `TYPE_BYTE` 有符号 8 位字节值
  - `TYPE_UNSIGNED_BYTE` 无符号 8 位字节值
  - `TYPE_SHORT` 有符号 16 位短值
  - `TYPE_UNSIGNED_SHORT` 无符号 16 位短值
  - `TYPE_INT` 有符号整数值
  - `TYPE_UNSIGNED_INT` 无符号整数值
  - `TYPE_FLOAT` 浮点值（默认）

Normalize
: 如果为 true，属性值将被 GPU 驱动程序规范化。当您不需要全精度，但想在不知道特定限制的情况下计算某些内容时，这很有用。例如，颜色向量通常只需要 0..255 的字节值，同时在着色器中被视为 0..1 的值。

Coordinate space
: 某些语义类型支持在不同的坐标空间中提供数据。要使用精灵实现广告牌效果，您通常需要本地空间中的位置属性以及世界空间中的完全变换位置，以实现最有效的批处理。

Vector type
: 属性的向量类型。

  - `VECTOR_TYPE_SCALAR` 单个标量值
  - `VECTOR_TYPE_VEC2` 2D 向量
  - `VECTOR_TYPE_VEC3` 3D 向量
  - `VECTOR_TYPE_VEC4` 4D 向量（默认）
  - `VECTOR_TYPE_MAT2` 2D 矩阵
  - `VECTOR_TYPE_MAT3` 3D 矩阵
  - `VECTOR_TYPE_MAT4` 4D 矩阵

Step function
: 指定属性数据应如何呈现给顶点函数。这仅与实例化相关。

  - `Vertex` 每个顶点一次，例如位置属性通常会在网格中每个顶点给出给顶点函数（默认）
  - `Instance` 每个实例一次，例如世界矩阵属性通常会在每个实例给出给顶点函数一次

Value
: 属性的值。属性值可以基于每个组件被覆盖，但否则这将作为顶点属性的默认值。注意：对于*默认*属性（位置、纹理坐标和页索引），该值将被忽略。

::: sidenote
自定义属性也可以通过重新配置流以使用更小的数据类型或不同的元素数来减少 CPU 和 GPU 上的内存占用。
:::

### 默认属性语义

材质系统将根据运行时特定名称的属性名称自动分配默认语义类型：

  - `position` - 语义类型：`SEMANTIC_TYPE_POSITION`
  - `texcoord0` - 语义类型：`SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - 语义类型：`SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - 语义类型：`SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - 语义类型：`SEMANTIC_TYPE_COLOR`
  - `normal` - 语义类型：`SEMANTIC_TYPE_NORMAL`
  - `tangent` - 语义类型：`SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - 语义类型：`SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - 语义类型：`SEMANTIC_TYPE_NORMAL_MATRIX`

如果您在材质中有这些属性的条目，默认语义类型将被您在材质编辑器中配置的任何内容覆盖。

### 设置自定义顶点属性数据

与用户定义的着色器常量类似，您也可以通过调用 go.get、go.set 和 go.animate 在运行时更新顶点属性：

![Custom material attribute](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

然而，更新顶点属性有一些注意事项，组件是否可以使用该值取决于属性的语义类型。例如，精灵组件支持 `SEMANTIC_TYPE_POSITION`，因此如果您更新具有此语义类型的属性，组件将忽略覆盖的值，因为语义类型规定数据应始终由精灵位置生成。

::: sidenote
目前在运行时设置自定义顶点数据仅支持精灵组件。
:::

### 实例化

实例化是一种用于高效绘制场景中同一对象的多个副本的技术。实例化不是每次使用对象时都创建单独的副本，而是允许图形引擎创建单个对象，然后多次重用它。例如，在具有大片森林的游戏中，实例化允许您创建一个树模型，然后以不同的位置和比例放置它数百或数千次，而不是为每棵树创建单独的树模型。现在，森林可以通过单次绘制调用渲染，而不是每棵树的单独绘制调用。

::: sidenote
实例化目前仅适用于模型组件。
:::

实例化在可能的情况下自动启用。Defold 严重依赖尽可能多地批处理绘制状态 - 要使实例化工作，必须满足一些要求：

- 所有实例必须使用相同的材质。如果通过 `render.enable_material` 设置了自定义材质，实例化仍然可以工作
- 材质必须配置为使用 'local' 顶点空间
- 材质必须具有至少一个每个实例重复的顶点属性
- 所有实例的常量值必须相同。常量值可以放入自定义顶点属性或其他后备方法（例如纹理）
- 着色器资源，如纹理或存储缓冲区，对于所有实例必须相同

将顶点属性配置为每个实例重复需要将 `Step function` 设置为 `Instance`。对于某些基于名称的语义类型，这是自动完成的（请参见上面的 `Default attribute semantics` 表），但也可以在材质编辑器中通过将 `Step function` 设置为 `Instance` 来手动设置。

作为一个简单的例子，以下场景有四个游戏对象，每个都有一个模型组件：

![Instancing setup](images/materials/instancing-setup.png)

材质配置如下，具有一个每个实例重复的自定义顶点属性：

![Instancing material](images/materials/instancing-material.png)

顶点着色器指定了多个每个实例的属性：

```glsl
// 每个顶点的属性
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// 每个实例的属性
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

请注意，`mtx_world` 和 `mtx_normal` 默认将配置为使用步骤函数 `Instance`。这可以通过在材质编辑器中为它们添加条目并将 `Step function` 设置为 `Vertex` 来更改，这将使属性每个顶点重复而不是每个实例重复。

要验证在这种情况下实例化是否工作，您可以查看 Web 分析器。在这种情况下，由于盒子实例之间唯一改变的是每个实例的属性，它可以通过单次绘制调用渲染：

![Instancing draw calls](images/materials/instancing-draw-calls.png)

#### 向后兼容性

在基于 OpenGL 的图形适配器上，实例化至少需要桌面版 OpenGL 3.1 和移动版 OpenGL ES 3.0。这意味着使用 OpenGL ES2 或更旧 OpenGL 版本的非常旧的设备可能不支持实例化。在这种情况下，渲染默认仍然可以工作，不需要开发人员任何特殊照顾，但可能不如使用实际实例化那样高效。目前，无法检测是否支持实例化，但此功能将在未来添加，以便可以使用更便宜的材质，或者可以完全跳过通常是实例化良好候选者的东西，如树叶或杂物。

## 顶点和片段常量

着色器常量，或称为"uniforms"，是从引擎传递到顶点和片段着色器程序的值。要使用常量，您在材质文件中将其定义为*顶点常量*属性或*片段常量*属性。需要在着色器程序中定义相应的 `uniform` 变量。材质中可以设置以下常量：

`CONSTANT_TYPE_WORLD`
: 世界矩阵。用于将顶点转换为世界空间。对于某些组件类型，由于批处理，顶点到达顶点程序时已经在世界空间中。在这些情况下，在着色器中与世界矩阵相乘将产生错误的结果。

`CONSTANT_TYPE_VIEW`
: 视图矩阵。用于将顶点转换为视图（相机）空间。

`CONSTANT_TYPE_PROJECTION`
: 投影矩阵。用于将顶点转换为屏幕空间。

`CONSTANT_TYPE_VIEWPROJ`
: 已经相乘的视图和投影矩阵。

`CONSTANT_TYPE_WORLDVIEW`
: 已经相乘的世界和视图矩阵。

`CONSTANT_TYPE_WORLDVIEWPROJ`
: 已经相乘的世界、视图和投影矩阵。

`CONSTANT_TYPE_NORMAL`
: 用于计算法线方向的矩阵。世界变换可能包含非均匀缩放，这会破坏组合世界视图变换的正交性。法线矩阵用于避免变换法线时的方向问题。（法线矩阵是世界视图矩阵的转置逆矩阵）。

`CONSTANT_TYPE_USER`
: 一个 vector4 常量，您可以用于任何想要传递到着色器程序的自定义数据。您可以在常量定义中设置常量的初始值，但它可以通过函数 [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 进行修改。您也可以使用 [go.get()](/ref/stable/go/#go.get) 检索值。更改单个组件实例的材质常量会[破坏渲染批处理并导致额外的绘制调用](/manuals/render/#draw-calls-and-batching)。

示例：

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: 一个 matrix4 常量，您可以用于任何想要传递到着色器程序的自定义数据。您可以在常量定义中设置常量的初始值，但它可以通过函数 [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 进行修改。您也可以使用 [go.get()](/ref/stable/go/#go.get) 检索值。更改单个组件实例的材质常量会[破坏渲染批处理并导致额外的绘制调用](/manuals/render/#draw-calls-and-batching)。

示例：

```lua
go.set("#sprite", "m", vmath.matrix4())
```

::: sidenote
为了使 `CONSTANT_TYPE_USER` 或 `CONSTANT_TYPE_MATRIX4` 类型的材质常量能够使用 `go.get()` 和 `go.set()`，它必须在着色器程序中使用。如果常量在材质中定义但未在程序中使用，它将从材质中删除，并且在运行时将不可用。
:::

## 采样器

采样器用于从纹理（瓦片源或图集）中采样颜色信息。颜色信息然后可以在着色器程序中用于计算。

精灵、瓦片地图、GUI 和粒子效果组件自动获得 `sampler2D` 集。着色器程序中第一个声明的 `sampler2D` 自动绑定到图形组件中引用的图像。因此，目前不需要为这些组件在材质文件中指定任何采样器。此外，这些组件类型目前仅支持单个纹理。（如果您需要在着色器中使用多个纹理，可以使用 [`render.enable_texture()`](/ref/render/#render.enable_texture) 并从渲染脚本手动设置纹理采样器。）

![Sprite sampler](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

您可以通过在材质文件中按名称添加采样器来指定组件的采样器设置。如果您没有在材质文件中设置采样器，将使用全局 *graphics* 项目设置。

![Sampler settings](images/materials/my_sampler.png)

对于模型组件，您需要在材质文件中指定您想要的采样器设置。然后，编辑器将允许您为任何使用该材质的模型组件设置纹理：

![Model samplers](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![Model](images/materials/model.png)

## 采样器设置

Name
: 采样器的名称。此名称应与片段着色器中声明的 `sampler2D` 匹配。

Wrap U/W
: U 和 V 轴的包裹模式：

  - `WRAP_MODE_REPEAT` 将在 [0,1] 范围之外重复纹理数据。
  - `WRAP_MODE_MIRRORED_REPEAT` 将在 [0,1] 范围之外重复纹理数据，但每隔一次重复就会镜像。
  - `WRAP_MODE_CLAMP_TO_EDGE` 将大于 1.0 的纹理数据设置为 1.0，任何小于 0.0 的值设置为 0.0---即边缘像素将重复到边缘。

Filter Min/Mag
: 放大和缩小的过滤。最近过滤需要比线性插值更少的计算，但可能导致锯齿伪影。线性插值通常提供更平滑的结果：

  - `Default` 使用 `game.project` 文件中 `Graphics` 下指定的默认过滤选项作为 `Default Texture Min Filter` 和 `Default Texture Mag Filter`。
  - `FILTER_MODE_NEAREST` 使用坐标最接近像素中心的纹理元素。
  - `FILTER_MODE_LINEAR` 设置最接近像素中心的 2x2 纹理元素数组的加权线性平均值。
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` 选择单个 mipmap 内最近的纹理元素值。
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` 在两个最近的最佳 mipmap 选择中选择最近的纹理元素，然后在这两个值之间线性插值。
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` 在单个 mipmap 内线性插值。
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` 使用线性插值计算两个映射中的每个值，然后在这两个值之间线性插值。

Max Anisotropy
: 各向异性过滤是一种高级过滤技术，它采用多个样本，将结果混合在一起。此设置控制纹理采样器的各向异性级别。如果 GPU 不支持各向异性过滤，该参数将不会做任何事情，并且默认设置为 1。

## 常量缓存

当渲染管线进行绘制时，它会从默认的系统常量缓存中提取常量值。您可以创建一个自定义常量缓存来覆盖默认常量，而是在渲染脚本中以编程方式设置着色器程序统一变量：

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. 创建一个新的常量缓存
2. 将 `tint` 常量设置为亮红色
3. 使用我们的自定义常量绘制谓词

请注意，缓存的常量元素像普通的 Lua 表一样被引用，但您不能使用 `pairs()` 或 `ipairs()` 迭代缓存。
