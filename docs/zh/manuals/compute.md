---
title: Defold 计算着色器手册
brief: 本手册解释了如何使用计算程序、着色器常量和采样器。
---

# 计算程序

::: sidenote
Defold 中的计算着色器支持目前处于*技术预览*状态。
这意味着某些功能尚不完善，并且 API 将来可能会发生变化。
:::

计算着色器是在 GPU 上执行通用计算的强大工具。它们允许您利用 GPU 的并行处理能力来执行物理模拟、图像处理等任务。计算着色器对存储在缓冲区或纹理中的数据进行操作，在许多 GPU 线程上并行执行操作。这种并行性使得计算着色器在密集计算方面非常强大。

* 有关渲染管线的更多信息，请参阅[渲染文档](/manuals/render)。
* 有关着色器程序的深入解释，请参阅[着色器文档](/manuals/shader)。

## 我可以用计算着色器做什么？

由于计算着色器旨在用于通用计算，因此您可以用它们做的事情实际上没有限制。以下是计算着色器通常用于的一些示例：

图像处理
  - 图像过滤：应用模糊、边缘检测、锐化滤镜等。
  - 色彩分级：调整图像的色彩空间。

物理
  - 粒子系统：模拟大量粒子以产生烟雾、火焰和流体动力学等效果。
  - 软体物理：模拟可变形物体，如布料和果冻。
  - 剔除：遮挡剔除、视锥体剔除

程序化生成
  - 地形生成：使用噪声函数创建详细地形。
  - 植被和树叶：创建程序化生成的植物和树木。

渲染效果
  - 全局光照：通过模拟光线在场景中反弹的方式来模拟逼真的照明。
  - 体素化：从网格数据创建 3D 体素网格。

## 计算着色器是如何工作的？

在高层次上，计算着色器通过将一个任务划分为许多可以同时执行的小任务来工作。这是通过`工作组`和`调用`的概念实现的：

工作组
: 计算着色器在`工作组`的网格上运行。每个工作组包含固定数量的调用（或线程）。工作组的大小和调用的数量在着色器代码中定义。

调用
: 每个调用（或线程）执行计算着色器程序。工作组内的调用可以通过共享内存共享数据，允许它们之间进行有效的通信和同步。

GPU 通过在多个工作组上并行启动许多调用来执行计算着色器，为适合的任务提供强大的计算能力。

## 创建计算程序

要创建计算程序，在*资源*浏览器中<kbd>右键单击</kbd>目标文件夹，然后选择<kbd>新建... ▸ 计算</kbd>。（您也可以从菜单中选择<kbd>文件 ▸ 新建...</kbd>，然后选择<kbd>计算</kbd>）。命名新的计算文件并按<kbd>确定</kbd>。

![计算文件](images/compute/compute_file.png)

新的计算将在*计算编辑器*中打开。

![计算编辑器](images/compute/compute.png)

计算文件包含以下信息：

计算程序
: 要使用的计算着色器程序文件（*`.cp`*）。该着色器操作"抽象工作项"，这意味着输入和输出数据类型没有固定定义。程序员需要定义计算着色器应该产生什么。

常量
: 将传递给计算着色器程序的统一变量。有关可用常量的列表，请参见下文。

采样器
: 您可以选择在材质文件中配置特定的采样器。添加采样器，根据着色器程序中使用的名称命名它，并根据您的喜好设置包装和过滤设置。


## 在 Defold 中使用计算程序

与材质不同，计算程序不分配给任何组件，也不属于正常渲染流程的一部分。计算程序必须在渲染脚本中`调度`才能执行任何工作。然而，在调度之前，您需要确保渲染脚本有对计算程序的引用。目前，渲染脚本了解计算程序的唯一方法是将其添加到包含对渲染脚本引用的 .render 文件中：

![计算渲染文件](images/compute/compute_render_file.png)

要使用计算程序，首先需要将其绑定到渲染上下文。这与材质的绑定方式相同：

```lua
render.set_compute("my_compute")
-- 在此处执行计算工作，调用 render.set_compute() 解除绑定
render.set_compute()
```

虽然计算常量将在程序调度时自动应用，但无法从编辑器中将任何输入或输出资源（纹理、缓冲区等）绑定到计算程序。相反，这必须通过渲染脚本完成：

```lua
render.enable_texture("blur_render_target", "tex_blur")
render.enable_texture(self.storage_texture, "tex_storage")
```

要在您决定的工作空间中运行程序，您需要调度该程序：

```lua
render.dispatch_compute(128, 128, 1)
-- dispatch_compute 也接受一个选项表作为最后一个参数
-- 您可以使用此参数表将渲染常量传递给调度调用
local constants = render.constant_buffer()
constants.tint = vmath.vector4(1, 1, 1, 1)
render.dispatch_compute(32, 32, 32, {constants = constants})
```

### 从计算程序写入数据

目前，从计算程序生成任何类型的输出只能通过`存储纹理`完成。存储纹理类似于"常规纹理"，只是它们支持更多功能和可配置性。顾名思义，存储纹理可以用作通用缓冲区，您可以从计算程序中读取和写入数据。然后，您可以将同一缓冲区绑定到不同的着色器程序以进行读取。

要在 Defold 中创建存储纹理，您需要从常规的 .script 文件执行此操作。渲染脚本没有此功能，因为动态纹理需要通过仅在常规 .script 文件中可用的资源 API 创建。

```lua
-- 在 .script 文件中：
function init(self)
    -- 像往常一样创建纹理资源，但添加"storage"标志
    -- 以便它可以用作计算程序的后备存储
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = resource.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = resource.TEXTURE_FORMAT_RGBA32F,
        flags  = resource.TEXTURE_USAGE_FLAG_STORAGE + resource.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    -- 从资源中获取纹理句柄
    local t_backing_handle = resource.get_texture_info(t_backing).handle

    -- 通知渲染器有关后备纹理的信息，以便它可以通过 render.enable_texture 绑定
    msg.post("@render:", "set_backing_texture", { handle = t_backing_handle })
end
```

## 将所有内容整合在一起

### 着色器程序

```glsl
// compute.cp
#version 450

layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;

// 指定输入资源
uniform vec4 color;
uniform sampler2D texture_in;

// 指定输出图像
layout(rgba32f) uniform image2D texture_out;

void main()
{
    // 这不是一个特别有趣的着色器，但它演示了
    // 如何从纹理和常量缓冲区读取并写入存储纹理

    ivec2 tex_coord   = ivec2(gl_GlobalInvocationID.xy);
    vec4 output_value = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 tex_coord_uv = vec2(float(tex_coord.x)/(gl_NumWorkGroups.x), float(tex_coord.y)/(gl_NumWorkGroups.y));
    vec4 input_value = texture(texture_in, tex_coord_uv);
    output_value.rgb = input_value.rgb * color.rgb;

    // 将输出值写入存储纹理
    imageStore(texture_out, tex_coord, output_value);
}
```

### 脚本组件
```lua
-- 在 .script 文件中

-- 这里我们指定稍后将绑定到
-- 计算程序的输入纹理。我们可以将此纹理分配给模型组件，
-- 或在渲染脚本中将其启用到渲染上下文。
go.property("texture_in", resource.texture())

function init(self)
    -- 像往常一样创建纹理资源，但添加"storage"标志
    -- 以便它可以用作计算程序的后备存储
    local t_backing = resource.create_texture("/my_backing_texture.texturec", {
        type   = resource.TEXTURE_TYPE_IMAGE_2D,
        width  = 128,
        height = 128,
        format = resource.TEXTURE_FORMAT_RGBA32F,
        flags  = resource.TEXTURE_USAGE_FLAG_STORAGE + resource.TEXTURE_USAGE_FLAG_SAMPLE,
    })

    local textures = {
        texture_in = resource.get_texture_info(self.texture_in).handle,
        texture_out = resource.get_texture_info(t_backing).handle
    }

    -- 通知渲染器有关输入和输出纹理的信息
    msg.post("@render:", "set_backing_texture", textures)
end
```

### 渲染脚本
```lua
-- 响应消息"set_backing_texture"
-- 为计算程序设置后备纹理
function on_message(self, message_id, message)
    if message_id == hash("set_backing_texture") then
        self.texture_in = message.texture_in
        self.texture_out = message.texture_out
    end
end

function update(self)
    render.set_compute("compute")
    -- 我们可以将纹理绑定到特定的命名常量
    render.enable_texture(self.texture_in, "texture_in")
    render.enable_texture(self.texture_out, "texture_out")
    render.set_constant("color", vmath.vector4(0.5, 0.5, 0.5, 1.0))
    -- 调度计算程序的次数与我们拥有的像素数一样多。
    -- 这构成了我们的"工作组"。着色器将被调用
    -- 128 x 128 x 1 次，或每个像素一次。
    render.dispatch_compute(128, 128, 1)
    -- 当我们完成计算程序后，需要解除绑定
    render.set_compute()
end
```

## 兼容性

Defold 目前支持以下图形适配器中的计算着色器：

- Vulkan
- Metal（通过 MoltenVK）
- OpenGL 4.3+
- OpenGL ES 3.1+

::: sidenote
目前无法检查运行中的客户端是否支持计算着色器。
这意味着如果图形适配器是基于 OpenGL 或 OpenGL ES 的，则无法保证客户端支持运行计算着色器。
Vulkan 和 Metal 从 1.0 版本开始支持计算着色器。要使用 Vulkan，您需要创建自定义清单并选择 Vulkan 作为后端。
:::