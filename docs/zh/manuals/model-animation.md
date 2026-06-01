---
title: Defold 3D模型动画
brief: 本手册介绍了如何在 Defold 中使用 3D 模型动画。
---

# 3D 模型动画

模型组件可以播放从 glTF 文件导入的骨骼动画和变形目标动画。骨骼动画使用模型的骨骼对模型中的顶点应用变形。变形目标动画，也称为混合形状动画，通过对备用顶点位置的权重进行动画处理来改变模型的形状。

关于如何将 3D 数据导入到模型中以进行动画的详细信息，请参阅[模型文档](/manuals/model)。

  ![Blender animation](images/animation/blender_animation.png)
  ![Wiggle loop](images/animation/suzanne.gif)


## 播放动画

模型使用[`model.play_anim()`](/ref/model#model.play_anim)函数进行动画处理：

```lua
function init(self)
    -- 在 #model 上来回播放 "wiggle" 动画
    model.play_anim("#model", "wiggle", go.PLAYBACK_LOOP_PINGPONG)
end
```

::: important
Defold 目前仅支持烘焙的骨骼动画。骨骼动画需要为每个动画骨骼的每个关键帧设置矩阵，而不是将位置、旋转和缩放作为单独的键。

动画也是线性插值的。如果您进行更高级的曲线插值，动画需要从导出器进行预烘焙。
:::

### 变形目标 {#morph-targets}

变形目标是同一网格的替代形状。每个目标都会存储位置、法线和切线增量，并且每个目标都有一个混合权重，用来控制应用该形状的程度。权重为 `0` 表示该目标没有效果，权重为 `1` 表示应用完整的目标形状。如果着色器和资源按此方式制作，超出该范围的值也可用于夸张效果。

Defold 会从 glTF 模型数据导入变形目标和初始变形权重。对变形权重进行动画处理的 glTF 动画会导入到模型动画集中，并且可以像骨骼动画一样使用 [`model.play_anim()`](/ref/model#model.play_anim) 播放：

```lua
function init(self)
    model.play_anim("#model", "smile", go.PLAYBACK_LOOP_FORWARD)
end
```

变形目标数据可以单独使用，也可以与骨骼动画一起使用，但一个模型组件一次只能播放一个模型动画。这意味着不能使用 `model.play_anim()` 同时播放一个骨骼动画和一个单独的变形目标动画。如果模型包含动画数据但没有骨架，则只会使用变形目标动画数据。

仍然可以将骨骼动画播放与来自其他来源的变形目标变化结合，例如从脚本中使用 `model.set_blend_weights()` 设置变形目标权重。

也可以从脚本读取并覆盖变形目标权重。[`model.get_blend_weights()`](/ref/model#model.get_blend_weights) 会返回模型中第一个带有变形目标的网格的当前权重。[`model.set_blend_weights()`](/ref/model#model.set_blend_weights) 会将脚本覆盖应用到模型中每个带变形的网格：

```lua
function init(self)
    local weights = model.get_blend_weights("#model")
    weights[1] = 0.75
    weights[2] = 0.25
    model.set_blend_weights("#model", weights)
end
```

权重表使用 Lua 从 1 开始的索引，顺序与网格中的变形目标相同。额外的值会被忽略；对于变形目标数量多于表中值数量的网格，缺失的值会按零处理。脚本覆盖会在每帧动画之后应用，直到被清除：

```lua
model.set_blend_weights("#model")     -- clear the override
model.set_blend_weights("#model", nil) -- also clears the override
```

### 着色器支持

要渲染变形目标，模型材质的顶点着色器需要采样生成的 `morph_targets` 纹理，并将加权增量应用到顶点数据。变形目标纹理是一个 2D 数组纹理，每个变形目标使用三个数组层：位置增量、法线增量和切线增量。

引擎会把当前的变形权重提供给名为 `morph_targets_weights` 的顶点着色器 uniform。每个 `vec4` 存储四个权重，因此 `morph_targets_weights[2]` 可以容纳八个变形目标。

下面的示例展示了非实例化模型材质中相关的顶点着色器部分：

```glsl
#version 140

in highp vec4 position;
in mediump vec2 texcoord0;
in mediump vec3 normal;
in mediump vec4 tangent;

out mediump vec2 var_texcoord0;
out mediump vec3 var_normal;
out mediump vec4 var_tangent;

uniform vs_uniforms
{
    mediump mat4 mtx_worldview;
    mediump mat4 mtx_proj;
    mediump mat4 mtx_normal;
    // Each vec4 stores four blend weights. Use morph_targets_weights[1]
    // for up to 4 morph targets, [2] for up to 8, [3] for up to 12, etc.
    mediump vec4 morph_targets_weights[2];
};

uniform sampler2DArray morph_targets;

vec2 get_morph_uv(int vertex_index, int width, int height)
{
    int x = vertex_index % width;
    int y = vertex_index / width;
    return vec2(
        (float(x) + 0.5) / float(width),
        (float(y) + 0.5) / float(height)
    );
}

void apply_morph_target(vec2 uv, float weight, int target,
    inout vec3 position_delta, inout vec3 normal_delta, inout vec3 tangent_delta)
{
    if (weight == 0.0) {
        return;
    }

    int position_layer = target * 3 + 0;
    int normal_layer = target * 3 + 1;
    int tangent_layer = target * 3 + 2;

    position_delta += weight * texture(morph_targets, vec3(uv, position_layer)).xyz;
    normal_delta += weight * texture(morph_targets, vec3(uv, normal_layer)).xyz;
    tangent_delta += weight * texture(morph_targets, vec3(uv, tangent_layer)).xyz;
}

void get_morph_target_data(int vertex_index,
    out vec3 position_delta, out vec3 normal_delta, out vec3 tangent_delta)
{
    position_delta = vec3(0.0);
    normal_delta = vec3(0.0);
    tangent_delta = vec3(0.0);

#ifndef EDITOR
    ivec3 texture_size = textureSize(morph_targets, 0);
    vec2 uv = get_morph_uv(vertex_index, texture_size.x, texture_size.y);

    apply_morph_target(uv, morph_targets_weights[0].x, 0, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].y, 1, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].z, 2, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[0].w, 3, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].x, 4, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].y, 5, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].z, 6, position_delta, normal_delta, tangent_delta);
    apply_morph_target(uv, morph_targets_weights[1].w, 7, position_delta, normal_delta, tangent_delta);
#endif
}

void main()
{
    vec3 position_delta;
    vec3 normal_delta;
    vec3 tangent_delta;
    get_morph_target_data(gl_VertexIndex, position_delta, normal_delta, tangent_delta);

    vec3 morphed_position = position.xyz + position_delta;
    vec3 morphed_normal = normalize(normal + normal_delta);
    vec3 morphed_tangent = normalize(tangent.xyz + tangent_delta);

    var_texcoord0 = texcoord0;
    var_normal = normalize((mtx_normal * vec4(morphed_normal, 0.0)).xyz);
    var_tangent = vec4(normalize((mtx_normal * vec4(morphed_tangent, 0.0)).xyz), tangent.w);

    gl_Position = mtx_proj * mtx_worldview * vec4(morphed_position, 1.0);
}
```

这里需要 `#ifndef EDITOR` 包装，因为编辑器中尚不支持模型动画预览，所以生成的变形目标纹理数据只在运行时可用。如果网格包含更多变形目标，请增大 `morph_targets_weights` 数组大小，并添加更多 `apply_morph_target()` 调用。

::: important
上面的着色器示例使用了 `textureSize()`，不适用于 OpenGL ES 2.0。
:::

### 骨骼层级

模型骨架中的骨骼在内部表示为游戏对象。

您可以在运行时检索骨骼游戏对象的实例 id。函数[`model.get_go()`](/ref/model#model.get_go)返回指定骨骼的游戏对象的 id。

```lua
-- 获取我们 wiggler 模型的中间骨骼游戏对象
local bone_go = model.get_go("#wiggler", "Bone_002")

-- 现在可以对游戏对象做一些有用的操作...
```

### 游标动画

除了使用`model.play_anim()`来推进模型动画外，*Model*组件还公开了一个"游标"属性，可以使用`go.animate()`进行操作（有关[属性动画](/manuals/property-animation)的更多信息）：

```lua
-- 在 #model 上设置动画但不启动它
model.play_anim("#model", "wiggle", go.PLAYBACK_NONE)
-- 将游标设置为动画的开头
go.set("#model", "cursor", 0)
-- 使用 in-out quad 缓动在 0 和 1 之间对游标进行 pingpong 补间。
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_INOUTQUAD, 3)
```

## 完成回调

模型动画`model.play_anim()`支持一个可选的 Lua 回调函数作为最后一个参数。当动画播放到结束时将调用此函数。对于循环动画，或者当动画通过`go.cancel_animations()`手动取消时，永远不会调用该函数。回调可用于在动画完成时触发事件或将多个动画链接在一起。

```lua
local function wiggle_done(self, message_id, message, sender)
    -- 动画完成
end

function init(self)
    model.play_anim("#model", "wiggle", go.PLAYBACK_ONCE_FORWARD, nil, wiggle_done)
end
```

## 播放模式

动画可以播放一次或循环播放。动画的播放方式由播放模式决定：

* `go.PLAYBACK_NONE`
* `go.PLAYBACK_ONCE_FORWARD`
* `go.PLAYBACK_ONCE_BACKWARD`
* `go.PLAYBACK_ONCE_PINGPONG`
* `go.PLAYBACK_LOOP_FORWARD`
* `go.PLAYBACK_LOOP_BACKWARD`
* `go.PLAYBACK_LOOP_PINGPONG`
