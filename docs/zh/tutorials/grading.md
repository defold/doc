---
title: 色彩分级着色器教程
brief: 在本教程中，您将在Defold中创建一个全屏后处理效果。
---

# 色彩分级教程

在本教程中，我们将创建一个色彩分级全屏后处理效果。所使用的基本渲染方法广泛适用于各种类型的后处理效果，如模糊、拖尾、发光、颜色调整等。

假设您已经熟悉Defold编辑器，并且对GL着色器和Defold渲染管线有基本了解。如果您需要学习这些主题，请查看[我们的着色器手册](/manuals/shader/)和[渲染手册](/manuals/render/)。

## 渲染目标

使用默认渲染脚本时，每个视觉组件（精灵、瓦片地图、粒子效果、GUI等）都直接渲染到显卡的*帧缓冲区*。然后硬件使图形显示在屏幕上。组件像素的实际绘制由GL*着色器程序*完成。Defold为每种组件类型提供了默认着色器程序，将像素数据原样绘制到屏幕上。通常，这正是您想要的行为——您的图像应该按照原始设计显示在屏幕上。

您可以用修改像素数据或以编程方式创建全新像素颜色的着色器程序替换组件的着色器程序。[Shadertoy教程](/tutorials/shadertoy)教您如何做到这一点。

现在假设您想要将整个游戏渲染为黑白。一种可能的解决方案是修改每种组件类型的单独着色器程序，使每个着色器都对像素颜色进行去饱和处理。目前，Defold提供了6种内置材质和6种顶点和片段着色器程序对，因此需要相当多的工作。此外，任何后续更改或效果添加都必须对每个着色器程序进行。

一种更灵活的方法是将渲染分为两个单独的步骤：

![渲染目标](images/grading/render_target.png)

1. 像往常一样绘制所有组件，但将它们绘制到离屏缓冲区而不是通常的帧缓冲区。您可以通过绘制到称为*渲染目标*的东西来实现这一点。
2. 将一个方形多边形绘制到帧缓冲区，并使用存储在渲染目标中的像素数据作为多边形的纹理源。同时确保方形多边形被拉伸以覆盖整个屏幕。

通过这种方法，我们能够在图形数据到达屏幕之前读取并修改它。通过向上面的步骤2添加着色器程序，我们可以轻松实现全屏效果。让我们看看如何在Defold中设置它。

## 设置自定义渲染器

我们需要修改内置渲染脚本并添加新的渲染功能。默认渲染脚本是一个很好的起点，因此首先复制它：

1. 复制*/builtins/render/default.render_script*：在*资产*视图中，右键单击*default.render_script*，选择<kbd>复制</kbd>，然后右键单击*main*并选择<kbd>粘贴</kbd>。右键单击副本并选择<kbd>重命名...</kbd>，给它一个合适的名称，如"grade.render_script"。
2. 通过右键单击*资产*视图中的*main*并选择<kbd>新建 ▸ 渲染</kbd>，创建一个名为*/main/grade.render*的新渲染文件。
3. 打开*grade.render*并将其*脚本*属性设置为"/main/grade.render_script"。

   ![grade.render](images/grading/grade_render.png)

4. 打开*game.project*并将*渲染*设置为"/main/grade.render"。

   ![game.project](images/grading/game_project.png)

现在游戏已设置为使用我们可以修改的新渲染管线运行。为了测试引擎是否使用了我们的渲染脚本副本，请运行您的游戏，然后对渲染脚本进行修改以产生视觉结果，然后重新加载脚本。例如，您可以禁用瓦片和精灵的绘制，然后按<kbd>⌘ + R</kbd>将"损坏的"渲染脚本热重载到运行的游戏中：

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. 注释掉"tile"谓词的绘制，包括所有精灵和瓦片。这行代码可以在渲染脚本文件的第33行左右找到。

如果通过这个简单的测试精灵和瓦片消失了，您就知道游戏正在运行您的渲染脚本。如果一切都按预期工作，您可以撤消对渲染脚本的更改。

## 绘制到离屏目标

现在，让我们修改渲染脚本，使其绘制到离屏渲染目标而不是帧缓冲区。首先我们需要创建渲染目标：

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 0)
    self.clear_color.x = sys.get_config("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config("render.clear_color_alpha", 0)

    self.view = vmath.matrix4()

    local color_params = { format = render.FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[render.BUFFER_COLOR_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. 为渲染目标设置颜色缓冲区参数。我们使用游戏的目标分辨率。
2. 使用颜色缓冲区参数创建渲染目标。

现在我们只需要用`render.set_render_target()`包装原始渲染代码，如下所示：

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color, [render.BUFFER_DEPTH_BIT] = 1, [render.BUFFER_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. 启用渲染目标。从现在开始，每次调用`render.draw()`都将绘制到我们的离屏渲染目标的缓冲区。
2. 除了设置为渲染目标分辨率的视口外，`update()`中的所有原始绘制代码都保持不变。
3. 此时，所有游戏图形都已绘制到渲染目标。所以是时候通过设置为默认渲染目标来禁用它。

这就是我们需要做的全部。如果您现在运行游戏，它将把所有内容绘制到渲染目标。但由于我们现在没有向帧缓冲区绘制任何内容，我们将只能看到一个黑屏。

## 填充屏幕的内容

要将渲染目标颜色缓冲区中的像素绘制到屏幕上，我们需要设置一些可以用像素数据进行纹理处理的东西。为此，我们将使用一个平坦的方形3D模型。

在Blender（或任何其他3D建模程序）中创建一个方形平面网格。将顶点坐标在X轴上设置为-1和1，在Y轴上设置为-1和1。Blender默认Z轴向上，因此您需要将网格绕X轴旋转90°。您还应确保为网格生成正确的UV坐标。在Blender中，选择网格后进入编辑模式，然后选择<kbd>网格 ▸ UV展开... ▸ 展开</kbd>。

![game.project](images/grading/quad_blender.png)

1. 将模型导出为名为*`quad.dae`*的Collada文件，并将其拖到Defold项目中。
2. 打开*`main.collection`*并创建一个名为"`grade`"的新游戏对象。
3. 向"`grade`"游戏对象添加一个模型组件。
3. 将模型组件的*网格*属性设置为*`quad.dae`*文件。

将游戏对象保持原始大小并放在原点。稍后，当我们渲染四边形时，我们将将其投影以填充整个屏幕。但首先我们需要四边形的材质和着色器程序：

1. 通过右键单击*资产*视图中的*main*并选择<kbd>新建 ▸ 材质</kbd>，创建一个名为*`grade.material`*的新材质。
2. 通过右键单击*资产*视图中的*main*并选择<kbd>新建 ▸ 顶点程序</kbd>和<kbd>新建 ▸ 片段程序</kbd>，创建一个名为*`grade.vp`*的顶点着色器程序和一个名为*`grade.fp`*的片段着色器程序。
3. 打开*grade.material*并将*顶点程序*和*片段程序*属性设置为新的着色器程序文件。
4. 添加一个名为"`view_proj`"的*顶点常量*，类型为`CONSTANT_TYPE_VIEWPROJ`。这是用于四边形顶点的顶点程序中的视图和投影矩阵。
5. 添加一个名为"`original`"的*采样器*。这将用于从离屏渲染目标颜色缓冲区采样像素。
6. 添加一个名为"`grade`"的*标签*。我们将在渲染脚本中创建一个新的*渲染谓词*，匹配此标签以绘制四边形。

   ![grade.material](images/grading/grade_material.png)

7. 打开*`main.collection`*，选择游戏对象"`grade`"中的模型组件，并将其*材质*属性设置为"`/main/grade.material`"。

   ![模型属性](images/grading/model_properties.png)

8. 顶点着色器程序可以保留为从基础模板创建的状态：

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // 位置在世界空间中
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. 在片段着色器程序中，不要直接将`gl_FragColor`设置为采样颜色值，而是执行一个简单的颜色操作。我们这样做主要是为了确保到目前为止一切都按预期工作：

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // 对从原始纹理采样的颜色进行去饱和处理
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

现在我们已经有了带有材质和着色器的四边形模型。我们只需要将其绘制到屏幕帧缓冲区。

## 使用离屏缓冲区进行纹理处理

我们需要在渲染脚本中添加一个渲染谓词，以便我们可以绘制四边形模型。打开*`grade.render_script`*并编辑`init()`函数：

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. 添加一个匹配我们在*`grade.material`*中设置的"grade"标签的新谓词。

在`update()`中填充渲染目标的颜色缓冲区后，我们设置一个视图和投影，使四边形模型填充整个屏幕。然后我们使用渲染目标的颜色缓冲区作为四边形的纹理：

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[render.BUFFER_COLOR_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, render.BUFFER_COLOR_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. 清除帧缓冲区。请注意，之前对`render.clear()`的调用会影响渲染目标，而不是屏幕帧缓冲区。
2. 将视口设置为匹配窗口大小。
3. 将视图设置为单位矩阵。这意味着相机位于原点，沿Z轴直视。同时将投影设置为单位矩阵，使四边形投影到整个屏幕上。
4. 将纹理槽0设置为渲染目标的颜色缓冲区。我们在*`grade.material`*的槽0中有采样器"original"，因此片段着色器将从渲染目标采样。
5. 绘制我们创建的匹配任何带有"grade"标签的材质的谓词。四边形模型使用*`grade.material`*，它设置了该标签——因此将绘制四边形。
6. 绘制后，禁用纹理槽0，因为我们已经完成使用它进行绘制。

现在让我们运行游戏并查看结果：

![去饱和游戏](images/grading/desaturated_game.png)

## 色彩分级

颜色表示为三个分量值，其中每个分量决定颜色中红色、绿色或蓝色的数量。从黑色、红色、绿色、蓝色、黄色和粉色到白色的完整颜色光谱可以适合立方体形状：

![颜色立方体](images/grading/color_cube.png)

屏幕上可以显示的任何颜色都可以在这个颜色立方体中找到。色彩分级的基本思想是使用这样的颜色立方体，但使用改变后的颜色，作为3D*查找表*。

对于每个像素：

1. 根据红色、绿色和蓝色值在颜色立方体中查找其颜色的位置。
2. *读取*分级立方体在该位置存储的颜色。
3. 用读取的颜色而不是原始颜色绘制像素。

我们可以在片段着色器中做到这一点：

1. 在离屏缓冲区中为每个像素采样颜色值。
2. 在色彩分级的颜色立方体中查找采样像素的颜色位置。
3. 将输出片段颜色设置为查找的值。

![渲染目标分级](images/grading/render_target_grading.png)

## 表示查找表

Open GL ES 2.0不支持3D纹理，因此我们需要找出另一种方法来表示3D颜色立方体。一种常见的方法是沿Z轴（蓝色）切片立方体，并将每个切片并排放置在2维网格中。每个16个切片包含一个16⨉16像素的网格。我们将其存储在一个纹理中，可以在片段着色器中使用采样器读取：

![查找纹理](images/grading/lut.png)

生成的纹理包含16个单元格（每个蓝色强度一个），每个单元格内X轴上有16种红色，Y轴上有16种绿色。纹理将整个1600万色RGB颜色空间仅表示为4096种颜色——仅为4位颜色深度。按照大多数标准，这很糟糕，但由于GL图形硬件的一个特性，我们可以恢复非常高的颜色准确性。让我们看看如何做到。

## 查找颜色

查找颜色是检查蓝色分量并找出从哪个单元格中选择红色和绿色值的问题。找到具有正确红-绿色集的单元格的公式很简单：

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

这里`B`是0到1之间的蓝色分量值，`N`是单元格总数。在我们的例子中，单元格号将在`0`--`15`范围内，其中单元格`0`包含蓝色分量为`0`的所有颜色，单元格`15`包含蓝色分量为`1`的所有颜色。

例如，RGB值`(0.63, 0.83, 0.4)`可以在包含所有蓝色值为`0.4`的颜色的单元格中找到，即单元格号6。知道了这一点，基于绿色和红色值的最终纹理坐标查找就很简单了：

![查找表](images/grading/lut_lookup.png)

请注意，我们需要将红色和绿色值`(0, 0)`视为在左下角像素的*中心*，并将值`(1.0, 1.0)`视为在右上角像素的*中心*。

::: 旁注
我们从左下角像素的中心开始读取，直到右上角像素的中心的原因是我们不希望当前单元格之外的任何像素影响采样值。请参阅下面的过滤部分。
:::

当在纹理上的这些特定坐标处采样时，我们看到我们最终位于4个像素之间。那么GL会告诉我们该点具有什么颜色值？

![查找表过滤](images/grading/lut_filtering.png)

答案取决于我们如何在材质中指定采样器的*过滤*。

- 如果采样器过滤是`NEAREST`，GL将返回最近像素值的颜色值（位置值向下舍入）。在上述情况下，GL将返回位置`(0.60, 0.80)`的颜色值。对于我们的4位查找纹理，这意味着我们将颜色值量化为总共仅4096种颜色。

- 如果采样器过滤是`LINEAR`，GL将返回*插值的*颜色值。GL将根据到采样位置周围像素的距离混合颜色。在上述情况下，GL将返回一个颜色，该颜色是采样点周围4个像素各25%的混合。

通过使用线性过滤，我们消除了颜色量化，并从一个相当小的查找表中获得了非常好的颜色精度。

## 实现查找

让我们在片段着色器中实现纹理查找：

1. 打开*`grade.material`*。
2. 添加一个名为"`lut`"（查找表）的第二个采样器。
3. 将*`Filter min`*属性设置为`FILTER_MODE_MIN_LINEAR`，将*`Filter mag`*属性设置为`FILTER_MODE_MAG_LINEAR`。

    ![查找表采样器](images/grading/material_lut_sampler.png)

4. 下载以下查找表纹理（*`lut16.png`*）并将其添加到您的项目中。

    ![16色查找表](images/grading/lut16.png)

5. 打开*`main.collection`*并将*`lut`*纹理属性设置为下载的查找表纹理。

    ![四边形模型查找表](images/grading/quad_lut.png)

6. 最后，打开*`grade.fp`*，以便我们可以添加颜色查找支持：

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. 声明采样器`lut`。
    2. 最大颜色常量（15，因为我们从0开始）、每个通道的颜色数以及查找纹理宽度和高度。
    3. 从原始纹理（离屏渲染目标颜色缓冲区）采样像素颜色（称为`px`）。
    4. 根据`px`的蓝色通道值计算从哪个单元格读取颜色。
    5. 计算半像素偏移，以便我们从像素中心读取。
    6. 根据`px`的红色和绿色值计算纹理上的X和Y偏移。
    7. 计算查找纹理上的最终采样位置。
    8. 从查找纹理采样结果颜色。
    9. 将四边形纹理上的颜色设置为结果颜色。

目前，查找表纹理只返回我们查找的相同颜色值。这意味着游戏应该以其原始颜色渲染：

![世界原始外观](images/grading/world_original.png)

到目前为止，看起来我们做的一切都是正确的，但表面下潜伏着一个问题。看看当我们添加一个带有渐变测试纹理的精灵时会发生什么：

![蓝色条带](images/grading/blue_banding.png)

蓝色渐变显示出一些非常难看的条带。为什么会这样？

## 插值蓝色通道

蓝色通道条带的问题在于，当从纹理读取颜色时，GL无法执行任何蓝色通道插值。我们基于蓝色值预先选择一个特定的单元格来读取，仅此而已。例如，如果蓝色通道包含`0.400`--`0.466`范围内的任何值，该值并不重要——我们将始终从蓝色通道设置为`0.400`的单元格号6采样最终颜色。

为了获得更好的蓝色通道分辨率，我们可以自己实现插值。如果蓝色值在两个相邻单元格的值之间，我们可以从这两个单元格中采样，然后混合颜色。例如，如果蓝色值是`0.420`，我们应该从单元格号6*和*单元格号7中采样，然后混合颜色。

因此，我们应该从两个单元格读取：

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

和：

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

然后我们从这些单元格中的每一个采样颜色值，并根据公式线性插值颜色：

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

这里`color`~low~是从较低（最左侧）单元格采样的颜色，`color`~high~是从较高（最右侧）单元格采样的颜色。GLSL函数`mix()`为我们执行这种线性插值。

上面的值`C~frac~`是缩放到`0`--`15`颜色范围的蓝色通道值的小数部分：

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

同样，有一个GLSL函数可以给我们一个值的小数部分。它叫做`frac()`。片段着色器（*`grade.fp`*）中的最终实现非常简单：

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. 计算要读取的两个相邻单元格。
2. 计算两个单独的查找位置，每个单元格一个。
3. 从单元格位置采样两种颜色。
3. 根据`cell`的分数线性混合颜色，这是缩放的蓝色颜色值。

现在再次使用测试纹理运行游戏会产生更好的结果。蓝色通道上的条带消失了：

![蓝色无条带](images/grading/blue_no_banding.png)

## 分级查找表纹理

好的，为了绘制看起来与原始游戏世界完全相同的东西，我们做了很多工作。但这种设置允许我们做一些非常酷的事情。坚持住！

1. 以未受影响的形式截取游戏屏幕截图。
2. 在您喜欢的图像处理程序中打开屏幕截图。
3. 应用任意数量的颜色调整（亮度、对比度、颜色曲线、白平衡、曝光等）。

![Affinity中的世界](images/grading/world_graded_affinity.png)

4. 将相同的颜色调整应用于查找表纹理文件（*`lut16.png`*）。
5. 保存颜色调整后的查找表纹理文件。
6. 将Defold项目中使用的纹理*`lut16.png`*替换为颜色调整后的纹理。
7. 运行游戏！

![分级后的世界](images/grading/world_graded.png)

太棒了！