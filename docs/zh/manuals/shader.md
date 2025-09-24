---
title: Defold 中的着色器编程
brief: 本手册详细介绍了顶点和片段着色器以及如何在 Defold 中使用它们。
---

# 着色器

着色器程序是图形渲染的核心。它们是用一种称为 GLSL（GL 着色语言）的类 C 语言编写的程序，由图形硬件运行，用于对底层的 3D 数据（顶点）或最终显示在屏幕上的像素（"片段"）执行操作。着色器可用于绘制精灵、为 3D 模型添加光照、创建全屏后期效果等等。

本手册描述了 Defold 的渲染管线如何与 GPU 着色器接口。为了为您的内容创建着色器，您还需要理解材质的概念，以及渲染管线的工作原理。

* 有关渲染管线的详细信息，请参阅[渲染手册](/manuals/render)。
* 有关材质的详细信息，请参阅[材质手册](/manuals/material)。
* 有关计算程序的详细信息，请参阅[计算手册](/manuals/compute)。

OpenGL ES 2.0（嵌入式系统 OpenGL）和 OpenGL ES 着色语言的规范可在 [Khronos OpenGL 注册表](https://www.khronos.org/registry/gles/)中找到。

请注意，在台式计算机上，可以使用 OpenGL ES 2.0 不可用的功能编写着色器。您的显卡驱动程序可能会愉快地编译和运行在移动设备上无法工作的着色器代码。


## 概念

顶点着色器
: 顶点着色器不能创建或删除顶点，只能改变顶点的位置。顶点着色器通常用于将顶点的位置从 3D 世界空间转换到 2D 屏幕空间。

  顶点着色器的输入是顶点数据（以 `attributes` 的形式）和常量（`uniforms`）。常见的常量是将顶点位置转换和投影到屏幕空间所需的矩阵。

  顶点着色器的输出是顶点的计算出的屏幕位置（`gl_Position`）。也可以通过 `varying` 变量将数据从顶点着色器传递到片段着色器。

片段着色器
: 顶点着色器完成后，片段着色器的工作是决定结果图元的每个片段（或像素）的颜色。

  片段着色器的输入是常量（`uniforms`）以及由顶点着色器设置的任何 `varying` 变量。

  片段着色器的输出是特定片段的颜色值（`gl_FragColor`）。

计算着色器
: 计算着色器是一种通用着色器，可用于在 GPU 上执行任何类型的工作。它完全不属于图形管线的一部分，计算着色器在单独的执行上下文中运行，不依赖于来自任何其他着色器的输入。

  计算着色器的输入是常量缓冲区（`uniforms`）、纹理图像（`image2D`）、采样器（`sampler2D`）和存储缓冲区（`buffer`）。

  计算着色器的输出没有明确定义，与顶点和片段着色器不同，没有需要产生的特定输出。由于计算着色器是通用的，由程序员定义计算着色器应该产生什么类型的结果。

世界矩阵
: 模型形状的顶点位置是相对于模型原点存储的。这被称为"模型空间"。然而，游戏世界是一个"世界空间"，其中每个顶点的位置、方向和缩放都是相对于世界原点表达的。通过将这些分开，游戏引擎能够移动、旋转和缩放每个模型，而不会破坏存储在模型组件中的原始顶点值。

  当模型放置在游戏世界中时，模型的局部顶点坐标必须转换为世界坐标。这种转换是通过*世界变换矩阵*完成的，它告诉应该对模型的顶点应用什么转换（移动）、旋转和缩放，以便正确放置在游戏世界的坐标系中。

  ![World transform](images/shader/world_transform.png)

视图和投影矩阵
: 为了将游戏世界的顶点放到屏幕上，每个矩阵的 3D 坐标首先被转换为相对于摄像机的坐标。这是通过_视图矩阵_完成的。其次，顶点通过_投影矩阵_投影到 2D 屏幕空间上：

  ![Projection](images/shader/projection.png)

属性
: 与单个顶点关联的值。属性由引擎传递给着色器，如果您想访问属性，只需在着色器程序中声明它。不同组件类型有不同的属性集：
  - 精灵有 `position` 和 `texcoord0`。
  - 瓦片网格有 `position` 和 `texcoord0`。
  - GUI 节点有 `position`、`textcoord0` 和 `color`。
  - 粒子特效有 `position`、`texcoord0` 和 `color`。
  - 模型有 `position`、`texcoord0` 和 `normal`。
  - 字体有 `position`、`texcoord0`、`face_color`、`outline_color` 和 `shadow_color`。

常量
: 着色器常量在渲染绘制调用的持续时间内保持不变。常量被添加到材质文件的*常量*部分，然后在着色器程序中声明为 `uniform`。采样器 uniform 被添加到材质的*采样器*部分，然后在着色器程序中声明为 `uniform`。在顶点着色器中执行顶点变换所需的矩阵可作为常量使用：

  - `CONSTANT_TYPE_WORLD` 是*世界矩阵*，将对象从局部坐标空间映射到世界空间。
  - `CONSTANT_TYPE_VIEW` 是*视图矩阵*，将世界空间映射到摄像机空间。
  - `CONSTANT_TYPE_PROJECTION` 是*投影矩阵*，将摄像机空间映射到屏幕空间。
  - 预乘的 $world * view$、$view * projection$ 和 $world * view$ 矩阵也可用。
  - `CONSTANT_TYPE_USER` 是一个 `vec4` 类型常量，您可以按需使用。

  [材质手册](/manuals/material)解释了如何指定常量。

采样器
: 着色器可以声明*采样器*类型的 uniform 变量。采样器用于从图像源读取值：

  - `sampler2D` 从 2D 图像纹理中采样。
  - `sampler2DArray` 从 2D 图像数组纹理中采样。这主要用于分页图集。
  - `samplerCube` 从 6 图像立方体贴图纹理中采样。
  - `image2D` 将（并可能存储）纹理数据加载到图像对象。这主要用于计算着色器的存储。

  您只能在 GLSL 标准库的纹理查找函数中使用采样器。[材质手册](/manuals/material)解释了如何指定采样器设置。

UV 坐标
: 2D 坐标与顶点关联，它映射到 2D 纹理上的一个点。因此，纹理的一部分或整个部分可以绘制到由一组顶点描述的形状上。

  ![UV coordinates](images/shader/uv_map.png)

  UV 图通常在 3D 建模程序中生成并存储在网格中。每个顶点的纹理坐标作为属性提供给顶点着色器。然后使用 varying 变量来查找每个片段的 UV 坐标，这些坐标是从顶点值插值的。

Varying 变量
: Varying 类型的变量用于在顶点阶段和片段阶段之间传递信息。

  1. 在顶点着色器中为每个顶点设置 varying 变量。
  2. 在光栅化期间，为正在渲染的图元上的每个片段插值此值。片段到形状顶点的距离决定了插值。
  3. 该变量为每次对片段着色器的调用设置，可用于片段计算。

  ![Varying interpolation](images/shader/varying_vertex.png)

  例如，在三角形的每个角上将 varying 设置为 `vec3` RGB 颜色值将在整个形状上插值颜色。类似地，在矩形中的每个顶点上设置纹理贴图查找坐标（或*UV 坐标*）允许片段着色器为形状的整个区域查找纹理颜色值。

  ![Varying interpolation](images/shader/varying.png)

## 编写现代 GLSL 着色器

由于 Defold 引擎支持多个平台和图形 API，开发人员必须能够简单地在任何地方编写有效的着色器。资源管线主要通过两种方式实现这一点（从现在起表示为`着色器管线`）：

1. 传统管线，其中着色器使用与 ES2 兼容的 GLSL 代码编写。
2. 现代管线，其中着色器使用与 SPIR-v 兼容的 GLSL 代码编写。

从 Defold 1.9.2 开始，鼓励编写利用新管线的着色器，为此，大多数着色器需要迁移到至少版本 140（OpenGL 3.1）编写的着色器。要迁移着色器，请确保满足这些要求：

### 版本声明
在着色器顶部至少放置 #version 140：

```glsl
#version 140
```

这就是构建过程中选择着色器管线的方式，这就是为什么您仍然可以使用旧着色器。如果没有找到版本预处理器，Defold 将回退到传统管线。

### 属性
在顶点着色器中，将 `attribute` 关键字替换为 `in`：

```glsl
// 而不是：
// attribute vec4 position;
// 应该：
in vec4 position;
```

注意：片段着色器（和计算着色器）不接受任何顶点输入。

### Varyings
在顶点着色器中，varyings 应该以 `out` 为前缀。在片段着色器中，varyings 变为 `in`：

```glsl
// 在顶点着色器中，而不是：
// varying vec4 var_color;
// 应该：
out vec4 var_color;

// 在片段着色器中，而不是：
// varying vec4 var_color;
// 应该：
in vec4 var_color;
```

### Uniform（在 Defold 中称为常量）

不透明的 uniform 类型（采样器、图像、原子、SSBO）不需要任何迁移，您可以像今天一样使用它们：

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

对于非不透明的 uniform 类型，您需要将它们放在 `uniform 块`中。uniform 块只是 uniform 变量的集合，使用 `uniform` 关键字声明：

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // uniform 块的各个成员可以按原样使用
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

uniform 块中的所有成员都作为单独的常量暴露给材质和组件。使用渲染常量缓冲区或 `go.set` 和 `go.get` 不需要迁移。

### 内置变量

在片段着色器中，从版本 140 开始，`gl_FragColor` 已被弃用。使用 `out` 代替：

```glsl
// 而不是：
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// 应该：
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### 纹理函数

特定的纹理采样函数，如 `texture2D` 和 `texture2DArray` 不再存在。相反，只需使用 `texture` 函数：

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// 而不是：
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// 应该：
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### 精度

以前需要为变量、输入、输出等设置显式精度，以符合 OpenGL ES 上下文。这不再是必需的，现在对于支持它的平台自动设置精度。

### 整合

作为应用所有这些规则的最终示例，这里是转换为新格式的内置精灵着色器：

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// 位置在世界空间中
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // 预乘 alpha，因为所有运行时纹理都已经预乘了
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## 在着色器中包含代码片段

Defold 中的着色器支持从项目中具有 `.glsl` 扩展名的文件中包含源代码。要从着色器包含 glsl 文件，请使用 `#include` pragma，使用双引号或方括号。包含必须具有相对于项目的路径或相对于包含文件的路径：

```glsl
// 在文件 /main/my-shader.fp 中

// 绝对路径
#include "/main/my-snippet.glsl"
// 文件在同一文件夹中
#include "my-snippet.glsl"
// 文件在 'my-shader' 同一级的子文件夹中
#include "sub-folder/my-snippet.glsl"
// 文件在父目录的子文件夹中，即 /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// 文件在父目录中，即 /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

关于如何拾取包含有一些注意事项：

  - 文件必须是相对于项目的，意味着您只能包含位于项目内的文件。任何绝对路径必须以 `/` 开头指定
  - 您可以在文件中的任何位置包含代码，但不能在语句中内联包含文件。例如 `const float #include "my-float-name.glsl" = 1.0` 将不起作用

### 头文件保护

片段本身可以包含其他 `.glsl` 文件，这意味着最终生成的着色器可能多次包含相同的代码，根据文件的内容，您可能最终会因为多次声明相同的符号而导致编译问题。为了避免这种情况，您可以使用*头文件保护*，这是几种编程语言中的常见概念。示例：

```glsl
// 在 my-shader.vs 中
#include "math-functions.glsl"
#include "pi.glsl"

// 在 math-functions.glsl 中
#include "pi.glsl"

// 在 pi.glsl 中
const float PI = 3.14159265359;
```

在这个例子中，`PI` 常量将被定义两次，这将在运行项目时导致编译器错误。您应该使用头文件保护来保护内容：

```glsl
// 在 pi.glsl 中
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

来自 `pi.glsl` 的代码将在 `my-shader.vs` 中扩展两次，但由于您已经用头文件保护包装了它，PI 符号将只被定义一次，着色器将成功编译。

然而，根据用例，这并不总是严格必要的。如果您想在本地函数中重用代码或在不需要值在着色器代码中全局可用的其他地方，您可能不应该使用头文件保护。示例：

```glsl
// 在 red-color.glsl 中
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// 在 my-shader.fp 中
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## 编辑器特定的着色器代码

当在 Defold 编辑器视口中渲染着色器时，预处理器定义 `EDITOR` 可用。这允许您编写在编辑器中运行与在实际游戏引擎中运行时行为不同的着色器代码。

这对于以下情况特别有用：
  - 添加只应在编辑器中显示的调试可视化。
  - 实现编辑器特定功能，如线框模式或材质预览。
  - 为在编辑器视口中可能无法正常工作的材质提供回退渲染。

使用 `#ifdef EDITOR` 预处理器指令有条件地编译只应在编辑器中运行的代码：

```glsl
#ifdef EDITOR
    // 此代码仅在着色器在 Defold 编辑器中渲染时执行
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // 编辑器预览的洋红色
#else
    // 此代码在游戏中运行时执行
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## 渲染过程

在最终显示在屏幕上之前，您为游戏创建的数据会经过一系列步骤：

![Render pipeline](images/shader/pipeline.png)

所有视觉组件（精灵、GUI 节点、粒子效果或模型）都由顶点组成，这些顶点是描述组件形状的 3D 世界中的点。这样做的好处是可以从任何角度和距离查看形状。顶点着色器程序的工作是获取单个顶点并将其转换为视口中的位置，以便形状可以最终显示在屏幕上。对于具有 4 个顶点的形状，顶点着色器程序运行 4 次，每次都是并行的。

![vertex shader](images/shader/vertex_shader.png)

程序的输入是顶点位置（以及与顶点关联的其他属性数据），输出是新的顶点位置（`gl_Position`）以及应该为每个片段插值的任何 `varying` 变量。

最简单的顶点着色器程序只是将输出的位置设置为零顶点（这不是很有用）：

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

一个更完整的例子是内置的精灵顶点着色器：

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. 包含视图和投影矩阵相乘的 uniform（常量）。
2. 精灵顶点的属性。`position` 已经被转换为世界空间。`texcoord0` 包含顶点的 UV 坐标。
3. 声明一个 varying 输出变量。这个变量将为每个片段在每个顶点设置的值之间进行插值，并发送到片段着色器。
4. `gl_Position` 被设置为投影空间中当前顶点的输出位置。这个值有 4 个组件：`x`、`y`、`z` 和 `w`。`w` 组件用于计算透视校正插值。在任何变换矩阵应用之前，这个值通常对于每个顶点都是 1.0。
5. 为这个顶点位置设置 varying UV 坐标。光栅化后，它将为每个片段进行插值，并发送到片段着色器。



顶点着色后，组件的屏幕形状已经确定：生成基本图元并进行光栅化，这意味着图形硬件将每个形状分割成*片段*，或像素。然后它运行片段着色器程序，每个片段一次。对于屏幕上 16x24 像素大小的图像，程序运行 384 次，每次都是并行的。

![fragment shader](images/shader/fragment_shader.png)

程序的输入是渲染管线和顶点着色器发送的任何内容，通常是片段的*uv 坐标*、染色颜色等。输出是像素的最终颜色（`gl_FragColor`）。

最简单的片段着色器程序只是将每个像素的颜色设置为黑色（同样，不是很有用的程序）：

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

同样，一个更完整的例子是内置的精灵片段着色器：

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. 声明 varying 纹理坐标变量。这个变量将基于形状的顶点为每个片段进行插值。
2. 声明 `sampler2D` uniform 变量。采样器，连同插值的纹理坐标，用于精灵的纹理采样。对于精灵，引擎会自动将采样的纹理映射到精灵的*图像*属性上。
3. 定义 `CONSTANT_TYPE_USER` 材质常量并声明为 `uniform`。用于为精灵设置染色颜色。默认值为纯白色。
4. 将染色颜色与其不透明度相乘，因为运行时纹理颜色都是经过不透明度预乘的。
5. 在插值坐标处采样并返回颜色值。
6. `gl_FragColor` 代表片段的最终颜色结果：漫反射纹理颜色与其染色颜色的乘积。

获得片段的最终颜色后，它还要经过一系列测试。常见的是*深度测试*，看片段的深度值是否与像素深度缓冲区匹配。经过测试后，片段可能被丢弃或深度缓冲区被赋予新值。这个测试通常用于计算远离摄像机物体的渲染剔除工作。

如果这个片段被保留下来，它还要与早先进入帧缓冲区的像素数据进行*混合*。渲染脚本基于混合参数将源颜色（片段着色器输出颜色）与目标颜色（帧缓冲区中已有颜色）进行混合计算。混合计算常见用法如显示半透明图像等。

## 深入学习

- [Shadertoy](https://www.shadertoy.com) 上有大量开发者开源着色器。可以通过学习各种着色技术作为自己的灵感源泉。其中很多着色器改改就能应用到 Defold 中去。[Shadertoy 教程](https://www.defold.com/tutorials/shadertoy/) 介绍了把网站着色器用于 Defold 的具体步骤。

- [渐变教程](https://www.defold.com/tutorials/grading/) 介绍了使用纹理采样进行全屏颜色渐变效果的编写方法。

- [The Book of Shaders](https://thebookofshaders.com/00/) 介紹了將著色器應用於項目的方法, 有利於提高性能和視覺效果。
