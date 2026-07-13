---
title: Defold 中的 Light 组件
brief: 本手册介绍如何使用环境光、方向光、点光源和聚光灯，以及如何在着色器中访问光源数据。
---

# Light 组件

Light 组件表示集合中的一个光源。Defold 目前支持四种光源资源类型：

- 环境光（`.ambient_light`）
- 方向光（`.directional_light`）
- 点光源（`.point_light`）
- 聚光灯（`.spot_light`）

与其他组件资源一样，光源资源也会添加到游戏对象中。你可以直接在游戏对象下创建 Light 组件，也可以先在 *Assets* 浏览器中创建光源资源，再在 *Outline* 视图中将其作为组件添加到游戏对象。

Defold 不会自动为每种材质应用光照。引擎会收集光源，并通过内置光源缓冲区将其提供给着色器。如何使用光源数据由材质着色器决定。

下面的示例使用同一个场景来展示不同光源类型对最终结果的影响：

![无光源的场景](images/light/no_light.png)

## 光源属性

所有光源颜色都是 RGB 值。光源资源不使用 alpha 通道。

### 环境光

环境光为场景添加恒定的光照。它不受游戏对象的位置、旋转或缩放影响。例如，可以用它提供整体的背景照明，或让对象看起来不受光照影响。

在编辑器中，环境光组件显示为箭头指向中心的图标。图标颜色与其 `color` 属性相同。

![较低强度的环境光](images/light/ambient_light_less_intensity.png)

属性：

`color`
: 环境光的 RGB 颜色。

`intensity`
: 乘以环境光颜色的强度系数。

![较高强度的环境光](images/light/ambient_light_full_intensity.png)

环境光会在着色器光源缓冲区中累加为单个环境光颜色 `light_info.xyz`，不会占用 `lights[]` 数组中的条目。场景中的多个环境光组件只会生成一个输出颜色，即所有环境光混合后的结果。

### 方向光

方向光表示来自某个方向的光线，例如阳光。它不使用游戏对象的位置或缩放；光照方向通过将游戏对象的世界旋转应用于局部前向 `(0, 0, -1)` 得出。

在编辑器中，方向光组件显示为带颜色的太阳图标，并带有指示其方向的 3D 箭头。

![方向光](images/light/directional_light.png)

属性：

`color`
: 方向光的 RGB 颜色。

`intensity`
: 乘以方向光颜色的强度系数。


方向光通常与环境光结合使用，以免背向方向光的表面变得完全漆黑。

![方向光和环境光](images/light/directional_and_ambient_light.png)

### 点光源

点光源从游戏对象的世界位置向外发光。点光源的位置取自游戏对象的世界位置。

在编辑器中，点光源组件显示为一个向四周发出射线的点，图标颜色表示其 `color` 属性，圆圈表示其 `range`。

![点光源](images/light/point_light.png)

属性：

`color`
: 点光源的 RGB 颜色。

`intensity`
: 乘以点光源颜色的强度系数。

`range`
: 以世界单位表示的光照半径。

有效范围会乘以游戏对象世界缩放各轴绝对值中的最小值。

![点光源范围](images/light/point_light_range.png)

改变光源颜色会为点光源的光照贡献着色，而范围则控制光线能够传播到离光源多远的位置。

![绿色的点光源范围](images/light/point_ight_range_green_color.png)

### 聚光灯

聚光灯从游戏对象的世界位置以锥形发光。其方向通过将游戏对象的世界旋转应用于 `(0, 0, -1)` 得出。

在编辑器中，聚光灯组件显示为带颜色的灯具图标，并带有显示外锥和内锥的辅助线。

![聚光灯](images/light/spot_light.png)

属性：

`color`
: 聚光灯的 RGB 颜色。

`intensity`
: 乘以聚光灯颜色的强度系数。

`range`
: 以世界单位表示的光照半径。

`inner_cone_angle`
: 编辑器中以度为单位的内锥角。此锥体内的像素会获得完整的聚光灯光照贡献。

`outer_cone_angle`
: 编辑器中以度为单位的外锥角。光照会在内锥和外锥之间逐渐衰减。

有效范围会乘以游戏对象世界缩放各轴绝对值中的最小值。锥角在编辑器中以度为单位进行编辑，并在编译后的光源资源中转换为弧度。

![聚光灯辅助图形](images/light/spot_light_gizmos.png)

## 验证

构建管线会验证并规范化光源资源数据：

- `color` 必须恰好包含三个数字。
- `intensity` 会限制为不小于 `0`。
- 对于点光源和聚光灯，`range` 会限制为不小于 `0`。
- 聚光灯锥角会限制在 `0..180` 度之间。
- `inner_cone_angle` 会受到限制，确保它永远不会超过 `outer_cone_angle`。

## 项目限制

Light 组件的最大数量由 `light.max_count` 项目设置控制。默认值为 `64`。

环境光不会占用着色器 `lights[]` 数组中的条目，但它仍是 Light 组件，因此会计入 `light.max_count`。方向光、点光源和聚光灯在处于活动状态时会占用 `lights[]` 中的条目。

如果 Light 组件的数量超过 `light.max_count`，引擎会报告组件缓冲区已满错误。

## 着色器中的光源缓冲区

着色器可以通过声明一个名为 `LightBuffer`、采用内置布局的 uniform 块来访问活动光源。引擎会检测这个块，并自动为使用它的材质和计算程序绑定光源数据。

![光源缓冲区着色器](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz：世界位置，w：未使用
    vec4 color;           // rgb：颜色，a：未使用
    vec4 direction_range; // xyz：规范化的世界方向，w：范围
    vec4 params;          // x：类型，y：强度，z：内锥角，w：外锥角
};

uniform LightBuffer
{
    // xyz：累积的环境光颜色，w：活动的非环境光数量
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

光源类型存储在 `lights[i].params.x` 中：

| 类型 | 值 |
|------|-------|
| 方向光 | `0` |
| 点光源 | `1` |
| 聚光灯 | `2` |

着色器可以声明较小的 `lights[]` 数组（小于 `light.max_count`），但不能声明更大的数组。光源循环始终要受声明的数组大小限制：

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // 方向光
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // 点光源
        {
            result += light_color;
        }
        else if (type == 2) // 聚光灯
        {
            result += light_color;
        }
    }

    return result;
}
```

上面的示例展示了缓冲区的访问模式。实际的点光源或聚光灯着色器还应计算从着色点到 `lights[i].position.xyz` 的向量，使用 `lights[i].direction_range.w` 应用距离衰减；对于聚光灯，还要使用 `lights[i].params.z` 和 `lights[i].params.w` 作为以弧度表示的锥角。

## 内置光照辅助文件

Defold 在 `/builtins/materials/lighting.glsl` 提供了一个着色器辅助文件。定义 `MAX_LIGHT_COUNT`，提供辅助文件所需的 varying 变量，然后在片段着色器中包含它：

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

该辅助文件定义了 `LIGHT_DIRECTIONAL`、`LIGHT_POINT` 和 `LIGHT_SPOT` 常量，提供 `ambient_light()`，并为缓冲区中的光源提供 Lambert 漫反射函数。

## 另请参阅

- [着色器手册](/manuals/shader)
- [材质手册](/manuals/material)
- [渲染手册](/manuals/render)
