---
brief: 在本教程中，您将把 shadertoy.com 上的着色器转换到 Defold。
layout: tutorial
locale: zh
title: Shadertoy 到 Defold 教程
---

# Shadertoy 教程

[Shadertoy.com](https://www.shadertoy.com/) 是一个汇集用户贡献 GL 着色器的网站。它是寻找着色器代码和灵感的绝佳资源。在本教程中，我们将从 Shadertoy 取一个着色器并让它在 Defold 中运行。本教程假设您对着色器有基本了解。如果需要补充知识，[着色器手册](/manuals/shader/)是很好的起点。

我们将使用 Pablo Andrioli（Shadertoy 用户名为 "Kali"）创作的 [Star Nest](https://www.shadertoy.com/view/XlfGRj)。这是一个纯程序化、数学黑魔法般的片段着色器，可以渲染非常酷的星场效果。

![Star Nest](../images/shadertoy/starnest.png)

这个着色器只有 65 行相当复杂的 GLSL 代码，但不用担心。我们会把它当作一个黑盒，只根据几个简单输入完成自己的效果。这里的任务是修改着色器，让它对接 Defold 而不是 Shadertoy。

## 需要贴图的对象

Star Nest 着色器是纯片段着色器，所以我们只需要某个可以被着色器贴图的对象。有多种选择：精灵、瓦片地图、GUI 或模型。本教程会使用一个简单的 3D 模型。原因是我们可以很容易把模型渲染成全屏效果，例如做视觉后处理时就需要这样。

我们可以从空项目开始。

1. 打开 Defold 并选择 Create From *Templates*。
2. 选择 *Empty Project*。
3. 设置项目的 *Title*，并在磁盘上选择 *Location*。
4. 点击 <kbd>Create New Project</kbd>。

![start](../images/shadertoy/empty_project.png)

您可以使用 `builtins/assets/meshes` 中内置的 `quad.gltf` 网格。

也可以选择在 Blender 或其他 3D 建模程序中创建一个方形平面网格。为方便起见，4 个顶点坐标在 X 轴上为 -1 和 1，在 Y 轴上为 -1 和 1。Blender 默认 Z 轴向上，因此需要将网格绕 X 轴旋转 90°。还应确保为网格生成正确的 UV 坐标。在 Blender 中，选中网格进入 *Edit Mode*，然后选择 <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd>。

<div class='sidenote' markdown='1'>
Blender 是免费的开源 3D 软件，可从 [blender.org](https://www.blender.org) 下载。
</div>

![quad in Blender](../images/shadertoy/quad_blender.png)

1. 在 Defold 中打开 "main.collection" 文件，并创建一个名为 "star-nest" 的新游戏对象。
2. 向 "star-nest" 游戏对象添加一个 *Model* 组件。
3. 将 *Mesh* 属性设置为我们的 `quad.gltf`。
4. 需要为模型设置材质，因此暂时选择内置的 `model.material`。

模型应出现在场景编辑器中，但会渲染为全黑。这是因为它还没有设置纹理：

![quad in Defold](../images/shadertoy/quad_default_material.png)

## 创建材质

1. 在 `Assets` 面板中对 `main` 文件夹点击 <kbd>Right Mouse Button</kbd>，选择 <kbd>New</kbd>-><kbd>Material</kbd>，并命名为 `star-nest`，创建新的材质文件 *`star-nest.material`*。

 ![material](../images/shadertoy/new_material.png)

2. 用同样方式创建顶点着色器程序 `star-nest.vp` 和片段着色器程序 `star-nest.fp`：
3. 打开 *star-nest.material*。
4. 将 *Vertex Program* 设置为 `star-nest.vp`。
5. 将 *Fragment Program* 设置为 `star-nest.fp`。
6. 添加一个 *Vertex Constant*，将其命名为 "`view_proj`"，类型为 `Viewproj`（表示“view projection”）。
8. 向 *Tags* 添加标签 "tile"。这样在绘制精灵和瓦片时，该 quad 会被包含在渲染阶段中。

 ![material](../images/shadertoy/material.png)

### 顶点程序

1. 打开顶点着色器程序文件 `star-nest.vp`。它应包含以下代码：

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### 片段程序

1. 打开片段着色器程序文件 `star-nest.fp`，并修改代码，让片段颜色基于 UV 坐标（`var_texcoord0`）的 X 和 Y 坐标设置。这样做是为了确认模型设置正确：

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. 在 `main.collection` 中，选择 `star-nest` 游戏对象上的模型组件，将 `Material` 属性设置为新创建的 `star-nest` 材质。

现在编辑器应该会用新着色器渲染模型，并且可以清楚看到 UV 坐标是否正确：左下角应为黑色（0, 0, 0），左上角为绿色（0, 1, 0），右上角为黄色（1, 1, 0），右下角为红色（1, 0, 0）：

![quad in Defold](../images/shadertoy/quad_material.png)

## 摄像机

现在可以运行项目（<kbd>Project</kbd>-><kbd>Build</kbd>，或快捷键 <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>），但我们会看到黑屏（几乎是黑屏，可能只有左下角一个很小的像素）。这是因为没有摄像机，默认渲染脚本会使用简单的回退方式，显示一个巨大的 2D 空间，而我们的模型位于 (0,0,0)，宽度只有 1。

让我们添加一个带摄像机组件的游戏对象，定义游戏中能看到什么。

1. 添加一个名为 `camera` 的游戏对象，位置设为 (0,0,1)。（Z 坐标设为 1 很重要，这样在默认 2D 设置中，由于 Z 轴朝向我们，该游戏对象会位于模型前方）。
2. 添加一个 `Camera` 组件，您会看到一个摄像机预览，里面包含我们的 quad。默认属性在这样的设置中刚好不需要改动，应该已经能看到正确结果，只有一点例外：我们不需要这么大的摄像机视锥，所以可以将 `Far Z` 降低到 `2`。

![camera](../images/shadertoy/camera.png)

可选地，也可以将 `Orthographic Projection` 设置为 `true` 来更改摄像机类型，并将 `Orthographic Zoom` 调整到类似 600 的值。不过在这种情况下不会自动保持宽高比，因此模型不会填满屏幕。

## Star Nest 着色器

现在一切准备就绪，让我们开始处理真正的着色器代码。先看原始代码，它由几个部分组成：

![Star Nest shader code](../images/shadertoy/starnest_code.png)

我们将使用 GLSL 版本 140 的现代管线。为此，在文件顶部用 `#version 140` 声明版本。

1. 第 5--18 行定义了一组常量。可以保持不变。它们是普通 GLSL 常量，不依赖 Shadertoy 或 Defold。

2. 第 21 行和第 63 行包含输入片段 X/Y 屏幕空间纹理坐标（`in vec2 fragCoord`）以及输出片段颜色（`out vec4 fragColor`）。

    Defold 会通过插值变量，把纹理坐标从顶点着色器以 UV 坐标（范围 0--1）传给片段着色器。在我们的顶点着色器中，它用 `out` 限定符声明：

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     在片段着色器中，相同值用 `in` 限定符接收：

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    然后，在 GLSL 140 中，我们用 `out` 限定符声明显式片段输出：

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    因此，原始 Shadertoy 代码写入 `fragColor` 的地方，我们的 Defold 着色器会写入 `out_fragColor`。

3. 第 23--27 行设置纹理尺寸、移动方向和缩放后的时间。在 Shadertoy 中，着色器通过 `fragCoord` 接收像素位置，视口/纹理分辨率通过 `uniform vec3 iResolution` 传入着色器。着色器根据片段坐标和分辨率计算带正确宽高比的 UV 风格坐标。它还会做一些分辨率偏移，让画面构图更好。

    在 Defold 中，我们不从像素坐标开始。相反，我们已经通过 `var_texcoord0` 从顶点着色器接收归一化 UV 坐标。这些坐标覆盖渲染 quad 的 `0.0` 到 `1.0` 范围。

    Defold 版本需要修改这些计算，改用来自 `var_texcoord0` 的 UV 坐标。
    典型转换如下：

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    具体 aspect 值取决于示例如何设置。如果效果渲染在已知显示尺寸的全屏 quad 上，本教程可以硬编码宽高比。如果效果需要支持任意窗口大小，请把分辨率作为片段常量传入，并将它放入 GLSL 140 uniform block。

    时间也在这里设置。Shadertoy 通过 `uniform float iGlobalTime` 传给着色器。Defold（自 1.12.3 起）通过一个特殊的 `Time` 常量向着色器提供时间，我们会使用它。

    在现代 Defold 中，非 opaque uniform 会声明在 uniform block 内。
    在片段着色器中我们这样声明：

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    然后，在 `star-nest.material` 中，添加名为 `time` 的 Fragment Constant，并将类型设为 `Time`。

    随后可以这样使用该值：

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    其中 `time.x` 是自引擎启动以来的时间，`time.y` 是上一帧以来的 delta time。

4. 第 29--39 行设置体积渲染的旋转，其中鼠标位置会影响旋转。鼠标坐标通过 `uniform vec4 iMouse` 传给着色器。

    本教程会跳过鼠标输入。

5. 第 41--62 行是着色器核心。可以保持这段代码不变。

## 修改后的 Star Nest 着色器

按照上面的各部分进行必要修改后，得到以下着色器代码。为了更好的可读性，它做了一些清理。Defold 和 Shadertoy 版本之间的差异已标注：

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. 我们在文件顶部声明 #version 140，以使用 Defold 的现代 GLSL 管线。然后保留这些 defines。
2. 顶点着色器通过 var_texcoord0 将 UV 坐标传给片段着色器。在 GLSL 140 中，片段着色器用 in 限定符接收这个插值值。
3. 在 GLSL 140 中，片段着色器应声明显式输出变量，而不是写入 gl_FragColor。这里我们使用 out vec4 out_fragColor。
4. Defold 的 Time 材质常量通过 uniform block 暴露给着色器。在 star-nest.material 中添加名为 time 的 Fragment Constant，并将类型设为 Time。
5. Shadertoy 使用 mainImage(out vec4 fragColor, in vec2 fragCoord)。在 Defold 中使用普通的 void main() 入口点，从 var_texcoord0 读取插值后的 UV 坐标，并把最终颜色写入 out_fragColor。
6. 本教程为渲染定义静态分辨率/宽高比值。当前模型是正方形，因此可以使用 vec2 res = vec2(1.0, 1.0);。如果使用大小为 1280×720 的矩形模型，则可以改用 vec2 res = vec2(1.78, 1.0); 并用它乘以 UV 坐标以保持正确宽高比。
7. 原始 Shadertoy 着色器使用 iGlobalTime。在此 Defold 版本中，time.x 包含自引擎启动以来的时间，因此我们把它赋给本地 iGlobalTime 变量，并用它驱动星场中的摄像机移动动画。
8. 我们通过完全移除 iMouse 值来保持本教程简单。旋转本身仍然保留，因为它能减少体积渲染中的视觉对称性。
9. 最后，着色器将结果片段颜色写入 out_fragColor。

保存片段着色器程序。现在模型应该会在场景编辑器和运行时中显示漂亮的星场纹理：

![quad with starnest](../images/shadertoy/quad_starnest.png)


## 动画

最后一块拼图是引入时间，让星星运动。Defold（自 1.12.3 起）会通过 `Time` 类型的片段常量自动提供这一点。

1. 打开 *star-nest.material*。
2. 添加一个 *Fragment Constant* 并命名为 "time"。
3. 将其 *Type* 设置为 `Time`。

![time constant](../images/shadertoy/time_constant.png)

就是这样！我们已经在片段着色器中处理了这个 `time`。完成了！

## 练习

一个有趣的后续练习是把原始鼠标移动输入添加到着色器。您需要创建一个新的 Fragment Constant，这次类型为 `User`，并在某个检测鼠标移动的脚本的 `on_input` 中使用 `go.set()` 函数更新它，将输入坐标设置到这个新常量上。

祝您使用 Defold 愉快！
