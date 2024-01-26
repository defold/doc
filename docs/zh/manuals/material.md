---
title: Defold 材质教程
brief: 本教程介绍了如何使用材质, 着色器常量和采样.
---

# 材质

材质用以表达可视元素 (sprite, tilemap, font, GUI node, model 等等) 应该如何被渲染.

材质包含 _tags_, 用来在渲染过程中作为选择渲染对象的依据. 材质还具有 _shader programs_ 这是通过显卡驱动编译好并上传至显卡每帧渲染时要使用的程序.

* 关于渲染过程, 详情请见 [渲染教程](/manuals/render).
* 关于着色器, 详情请见 [着色器教程](/manuals/shader).

## 创建材质

要创建材质, 在 *Assets* 浏览器里目标文件夹上 <kbd>右键点击</kbd> 然后选择 <kbd>New... ▸ Material</kbd>. (还可以从菜单选择 <kbd>File ▸ New...</kbd> , 再选择 <kbd>Material</kbd>). 给材质命名并点击 <kbd>Ok</kbd>.

![Material file](images/materials/material_file.png){srcset="images/materials/material_file@2x.png 2x"}

新材质会在 *材质编辑器* 里打开.

![Material editor](images/materials/material.png){srcset="images/materials/material@2x.png 2x"}

材质文件包含以下信息:

Name
: 材质的 id. 此名称将列于材质 *渲染* 资源内并编译进游戏中. 渲染 API 函数 `render.enable_material()` 也是使用这个名称. 此名称不能与其他名称重名.

Vertex Program
: 顶点着色器程序 (*.vp*) 在渲染材质时使用. 顶点着色器运行于 GPU 以渲染每个组件的顶点. 它会计算顶点的屏幕位置然后经过插值输出 "变化后" 的变量输入给片元着色器程序.

Fragment Program
: 片元着色器程序 (*.fp*) 在渲染材质时使用. 片元着色器运行于 GPU 以渲染每个组件的片元 (像素) 其目的是决定片元的颜色. 通常使用采样纹理或者基于输入变量 (可变变量或常量) 计算的方法得到结果.

Vertex Constants
: 传输给顶点着色器程序的数据. 有效常量列表见下文.

Fragment Constants
:  传输给片元着色器程序的数据. 有效常量列表见下文.

Samplers
: 你也可以在材质文件里指定采样器. 添加采样器, 赋予其在着色器程序里使用的名字再在链接上设置包裹和过滤.

Tags
: 标签与材质相关. 标签在引擎内部表现为 _bitmask_ 并由 [`render.predicate()`](/ref/render#render.predicate) 来收集需要渲染的组件. 如何渲染请见 [Render documentation](/manuals/render). 每个项目最多可以使用32个标签.

## Attributes

Shader 属性 (也叫 vertex streams), 是一个 GPU 从内存获取顶点来渲染几何图形的机制. 顶点着色器使用 `attribute` 关键字指定一系列流而且多数情况下 Defold 在流名称上自动创建并绑定数据. 然而, 有些情况下你会想传递顶点数据来实现一个引擎没有的特效. 顶点属性有如下配置:

Name
: 属性名. 与着色器常量类似, 属性配置只在顶点程序里匹配指定属性的时候使用.

Semantic type
: 语义类型是指属性 *是什么* 或者 *如何* 在编辑器中显示的语义. 例如, 指定属性为 `SEMANTIC_TYPE_COLOR` 会在编辑器中显示一个颜色拾取器, 同时数据会从引擎原样发送至着色器.

  - `SEMANTIC_TYPE_NONE` 默认语义类型. 除了给属性传送材质数据到顶点缓存以外没有其他效果.
  - `SEMANTIC_TYPE_POSITION` 给属性创建每个顶点位置数据. 可以连同坐标空间一起告诉引擎位置应该如何计算.
  - `SEMANTIC_TYPE_TEXCOORD` 给属性创建每个顶点的纹理坐标.
  - `SEMANTIC_TYPE_PAGE_INDEX` 给属性创建每个顶点的页码.
  - `SEMANTIC_TYPE_COLOR` 决定编辑器如何解释属性. 如果属性被配置为颜色语义, 则会在检视面板上显示一个颜色拾取器.

::: sidenote
材质系统会在运行时基于特定属性名给属性分配默认语义: position, texcoord0, page_index. 如果材质中有这些名字, 则默认语义类型会覆盖你在材质编辑器的手动配置!
:::

Data type
: 属性数据类型.

  - `TYPE_BYTE` 有符号 8 位值
  - `TYPE_UNSIGNED_BYTE` 无符号 8 位值
  - `TYPE_SHORT` 有符号 16 位短值
  - `TYPE_UNSIGNED_SHORT` 无符号 16 位短值
  - `TYPE_INT` 有符号整数
  - `TYPE_UNSIGNED_INT` 无符号整数
  - `TYPE_FLOAT` 浮点值

Count
: 属性的 *元素数*, 比如属性值的个数. 着色器里一个 `vec4` 有四个元素, 一个 `float` 有一个元素. 注意: 即使在着色器里制定了属性是一个 `vec4`, 你还是能给它指定元素更少的值, 这可以帮助减少内存占用.

Normalize
: 如果是 true, 属性值会被 GPU 驱动程序规范化. 当你不需要全精度, 又想在不知特定范围情况下计算时会很有用. 比如一个颜色向量一般只需 0..255 的 byte 值同时在着色器里被当作 0..1 的值.

Coordinate space
: 有些语义类型支持在不同坐标空间里提供数据. 要给 sprite 实现一个 billboarding 效果, 一般需要本地坐标系的位置属性加上世界坐标系的位置属性以实现更有效的合批.

Value
: 属性值. 可以基于每个组件覆盖属性值, 但除此之外, 这就是顶点属性的默认值. 注意: 对于 *默认* 属性 (position, texture coordinates 和 page indices) 该值被忽略.

::: sidenote
自定义属性也可以在 CPU 和 GPU 上帮助减少内存占用, 方法是重构流以使用更小的数据类型, 或更少的元素.
:::

::: important
自定义属性从 Defold 1.4.8 版本开始可用!
:::

## 顶点和片元常量

着色器常量, 或称 "uniforms" 是从引擎传输给顶点和片元着色器程序的数据. 要使用常量,您可以在材质文件中将其定义为一个 *顶点常量* 属性或 *片元常量* 属性.需要在着色器程序中定义相应的 `uniform` 变量.材质中可以设置以下常量：

CONSTANT_TYPE_WORLD
: 世界矩阵. 用来把顶点转换为世界坐标. 有的组件类型, 由于合批的应用它们到达顶点着色程序时已经是世界坐标的了. 在这些情况下,用着色器程序把世界矩阵再乘一遍就会产生错误的结果.

CONSTANT_TYPE_VIEW
: 视图矩阵. 用于转换顶点为视口（相机）空间坐标.

CONSTANT_TYPE_PROJECTION
: 映射矩阵. 用于将顶点转换为屏幕空间坐标.

CONSTANT_TYPE_VIEWPROJ
: 视口与其映射矩阵相乘后的矩阵.

CONSTANT_TYPE_WORLDVIEW
: 世界与视口映射矩阵相乘后的矩阵.

CONSTANT_TYPE_WORLDVIEWPROJ
: 世界, 视口与映射矩阵相乘后的矩阵.

CONSTANT_TYPE_NORMAL
: 用于计算法方向的矩阵. 世界移动转换可能包含非等比缩放, 这样会打破世界-视口转换的正交性. 变换法线时使用发方向可以避免这个问题. (法矩阵是世界-视口矩阵的转置逆).

CONSTANT_TYPE_USER
: 一个 vector4 常量用以向你的着色程序传递自定义数据. 定义时可以赋初值, 可以通过各组件 (`sprite`, `model`, `spine`, `particlefx` 和 `tilemap`) 的 `.set_constant()` 和 `.reset_constant()` 函数来改变其值. 改变单个组件实例的材质参数会 [打破合批增加drawcall](/manuals/render/#Draw call 与合批).

举例:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

CONSTANT_TYPE_USER_MATRIX4
: 一个 matrix4 常量用以向你的着色器程序传递用户自定义数据. 在常量定义时可以赋初值, 而其值可以通过 [go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 修改. 还可以通过 [go.get()](/ref/stable/go/#go.get) 获取其值. 改变单一组件实例得材质常量会 [打断渲染合批导致更多得 draw call](/manuals/render/#draw-calls-and-batching).

举例:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

::: sidenote
要使 `CONSTANT_TYPE_USER` 或 `CONSTANT_TYPE_MATRIX4` 类型的常量能使用 `go.get()` 和 `go.set()` 存取, 在着色器程序中必须使用到该常量. 如果常量在材质中定义了却没在着色器程序中使用, 它将被自动删除无法在运行时使用.
:::

## 采样器

采样器用于从纹理 (瓷砖图源或者图集) 中取得颜色数据. 颜色数据用于在着色器程序中参与计算.

Sprite, tilemap, GUI 和 particle effect 组件自动获得 `sampler2D` 集. 着色程序里第一个声明的 `sampler2D` 与可视组件所引用的图片自动绑定. 也就是说这些组件不用特地指定材质文件. 而且目前这些组件只支持一个纹理. (如需在着色器中使用多纹理, 可以使用 [`render.enable_texture()`](/ref/render/#render.enable_texture) 在渲染脚本中手动设置采样器.)

![Sprite sampler](images/materials/sprite_sampler.png){srcset="images/materials/sprite_sampler@2x.png 2x"}

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

在材质文件中添加取样器名就指定了一个采样器. 要是材质文件里没有指定, 会使用项目全局设置里的 *graphics* 设置.

![Sampler settings](images/materials/my_sampler.png){srcset="images/materials/my_sampler@2x.png 2x"}

对于3D模型组件, 还要在材质文件里设置采样器属性. 之后编辑器会让你选择使用该材质的3D模型纹理:

![Model samplers](images/materials/model_samplers.png){srcset="images/materials/model_samplers@2x.png 2x"}

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

![Model](images/materials/model.png){srcset="images/materials/model@2x.png 2x"}

## 采样器设置

Name
: 采样器名. 需要与片元着色器中定义的 `sampler2D` 变量名相匹配.

Wrap U/V
: U V 轴向上的包裹模式:

  - `WRAP_MODE_REPEAT` [0,1] 范围之外重复纹理.
  - `WRAP_MODE_MIRRORED_REPEAT` [0,1] 范围之外重复纹理, 但是再次重复时使用镜像的纹理.
  - `WRAP_MODE_CLAMP_TO_EDGE` 把大于 1.0 的值设置为 1.0, 小于 0.0 的值设置为 0.0---也就是说边缘的纹理会扩展开去.

Filter Min/Mag
: 缩放过滤. 就近过滤比线性插值过滤省资源, 但是可能产生不良效果. 一般线性插值过滤结果比较平滑:

  - `FILTER_MODE_NEAREST` 使用位于像素中心最近的图素.
  - `FILTER_MODE_LINEAR` 使用位于像素中心最近的的2x2图素矩阵的加权线性平均值.
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` 使用位于单个mipmap上最近的图素值.
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` 在最近的两个mipmap中选出最近的两个图素再进行线性插值.
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` 在单个mipmap里线性插值.
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` 使用线性插值分别计算两个mipmap再把两个结果进行线性插值.

Max Anisotropy
: 各异相性过滤是一种多重采样, 然后混合结果的高级技术. 该参数控制纹理采样器的各异相性级别. 如果 GPU 不支持各异相性过滤则该参数无效, 该参数默认值为 1.

## 常量缓存

渲染管线工作时, 默认会从系统常量缓存中拉取数据. 也可以建立自定义缓存再把着色器参数在渲染脚本里填充进缓存里去:

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. 新建常量缓存
2. 设置 `tint` 常量为白色
3. 使用自定义常量进行渲染

注意常量缓存就是一个普通的 Lua 表, 只是不能使用 `pairs()` 或 `ipairs()` 来进行迭代.
