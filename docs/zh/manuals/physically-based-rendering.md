---
title: Defold 中的基于物理渲染
brief: 本手册介绍如何在 Defold 中使用内置 PBR 材质并自定义基于物理的着色。
---

# 基于物理渲染 (PBR) {#physically-based-rendering-pbr}

基于物理的渲染（PBR）是一种根据物理原理模拟光与表面交互的着色方法。基础颜色、金属度和粗糙度等材质属性描述表面本身，与场景光照相互独立。

内置 glTF 材质提供 PBR 光照。Defold 还向自定义着色器暴露导入的 glTF 2.0 材质属性以及支持的 Khronos 扩展数据。

## 内置 PBR 材质 {#built-in-pbr-materials}

将 glTF 或 GLB 文件分配给[模型组件](/manuals/model)的 *Scene* 属性。当编辑器提示填充材质和纹理时，选择 <kbd>Auto Fill</kbd> 应用场景生成的材质绑定，并替换已有绑定。这些材质使用内置 glTF 着色器，可以直接引用内嵌图像。选择 <kbd>Keep Current</kbd> 则保留绑定，并手动分配材质和纹理。浏览内嵌资源和选择单个网格的方法请参阅[模型导入流程](/manuals/importing-models/#using-a-model)。

`/builtins/materials/` 中提供以下材质。请选择与模型及其是否使用实例化相匹配的变体：

| 模型类型 | 材质 |
|---|---|
| 静态、非实例化 | `gltf.material` |
| 静态、实例化 | `gltf_instanced.material` |
| 蒙皮（动画）、非实例化 | `gltf_skinned.material` |
| 蒙皮（动画）、实例化 | `gltf_skinned_instanced.material` |

四种材质均使用局部顶点空间和同一个 `gltf.fp` 片段着色器。蒙皮变体在 GPU 上执行蒙皮。GPU 蒙皮和实例化要求请参阅[模型材质要求](/manuals/model/#material)。

手动绑定纹理时，内置材质使用以下采样器名称：

| 纹理 | 采样器 | 使用的数据 |
|---|---|---|
| 基础颜色 | `PbrMetallicRoughness_baseColorTexture` | RGB 颜色和 alpha |
| 金属度/粗糙度 | `PbrMetallicRoughness_metallicRoughnessTexture` | G 通道为粗糙度，B 通道为金属度 |
| 法线 | `PbrMaterial_normalTexture` | RGB 中的切线空间法线 |
| 遮蔽 | `PbrMaterial_occlusionTexture` | R 通道中的遮蔽 |
| 自发光 | `PbrMaterial_emissiveTexture` | RGB 颜色 |

设置[摄像机](/manuals/camera/#using-the-camera)，并添加[光源组件](/manuals/light)来照亮模型。着色器使用方向光、点光和聚光灯进行直接光照，并用环境光提供简单的环境贡献。这些材质带有 `model` 标签，默认渲染脚本会绘制它们。自定义渲染脚本必须绘制匹配的谓词。

### 内置着色器行为 {#built-in-shader-behavior}

内置着色器实现了金属度/粗糙度着色、基础颜色和顶点颜色、有切线数据时的法线贴图、遮蔽，以及包含自发光强度的自发光。基础颜色和自发光纹理会从 sRGB 解码用于光照计算，最终颜色再转换回 sRGB。金属度/粗糙度、法线和遮蔽贴图包含线性数据。

着色器遵循无光照材质和 alpha 遮罩设置，并为双面表面调整法线。渲染状态仍然很重要：

- 对于双面材质，在相应渲染通道中禁用面剔除，使背面能够进入着色器。
- 对于 alpha 混合，着色器输出非预乘 alpha。使用 `graphics.BLEND_FACTOR_SRC_ALPHA` 和 `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` 启用混合，并在渲染脚本中管理透明对象的绘制顺序和深度写入。默认模型通道不会自动启用混合。

内置环境光贡献是近似值，不包含环境贴图光照或阴影。清漆、透射、绒面光泽、虹彩，以及镜面反射/光泽度工作流等效果需要自定义着色；导入这些参数并不会在 `gltf.fp` 中启用相应效果。

## 材质属性概览 {#material-properties-overview}

以下属性从分配给模型组件的 glTF 2.0 源文件中解析。此列表描述可用的材质数据；内置光照使用的是上文说明的子集。并非所有属性都是标准属性，其中一些来自可选的 glTF 扩展，导出 glTF 文件的工具可能包含，也可能不包含它们。下方属性名称后的括号注明相关扩展。

Metallic roughness
: 描述光如何与材质交互。这是默认 PBR 模型。

Specular glossiness (KHR_materials_pbrSpecularGlossiness)
: 金属度/粗糙度模型的替代方案，常见于较旧的资源。

Clearcoat (KHR_materials_clearcoat)
: 添加一个透明涂层，该涂层有自己的粗糙度和法线贴图。

Ior (KHR_materials_ior)
: 添加折射率。

Specular (KHR_materials_specular)
: 添加专用的高光强度和颜色通道。

Iridescence (KHR_materials_iridescence)
: 模拟肥皂泡或珍珠等材质中的薄膜干涉效果。

Sheen (KHR_materials_sheen)
: 模拟类似织物的微表面反射。

Transmission (KHR_materials_transmission)
: 模拟透明或玻璃类材质的光线透射。

Volume (KHR_materials_volume)
: 支持厚度和衰减等体积效果。

Emissive strength (KHR_materials_emissive_strength)
: 控制不受基础颜色影响的自发光亮度。

Normal map
: 用于表面细节的法线贴图。

Occlusion map
: 环境遮蔽贴图。

Emissive map
: 用于发光表面的自发光纹理。

Emissive factor
: 自发光强度的 RGB 乘数。

Alpha cutoff
: 遮罩透明的阈值。

Alpha mode
: 不透明、遮罩或混合透明模式。

Double sided
: 请求渲染表面的两侧。渲染通道必须允许背面进入着色器。

Unlit
: 如果为 true，则材质跳过光照计算。

## 着色器集成 {#shader-integration}

以下各节介绍自定义着色器。将适合的内置 `.material` 资源和 `gltf.fp` 复制到项目中，再将复制后材质的 *Fragment Program* 指向您的着色器。除非同时替换相关接口，否则请保留匹配的 glTF 顶点程序、采样器名称和局部顶点空间。

内置辅助函数将纹理采样与表面准备、BRDF 计算和光照分离。`gltf_sampling.glsl` 读取原始 `PbrMaterial` uniform 块，并生成包含已解析线性材质输入的 `PBRMaterial` 值。`gltf_lighting.glsl` 提供直接和环境光照，并合并它们的贡献。大小写区别用于区分原始 uniform 块与采样后的材质结构体。

### 着色器示例 {#example-shader}

以下片段着色器提高最小粗糙度，同时保留内置光照。它适用于四种 glTF 材质变体使用的顶点程序：

```glsl
#version 140

#include "/builtins/materials/gltf_sampling.glsl"
#include "/builtins/materials/gltf_lighting.glsl"

out vec4 out_fragColor;

void main()
{
    PBRMaterial inputs = pbr_sample_material(var_texcoord0, var_color);
    inputs.roughness = max(inputs.roughness, 0.35);

    // Sample textures, including the normal map, before discarding fragments.
    PBRSurface surface = pbr_sample_surface(inputs, var_texcoord0);
    if ((!inputs.doubleSided && !gl_FrontFacing) || pbr_should_discard_alpha(inputs))
    {
        discard;
    }

    // Derive BRDF values after editing the material inputs.
    MaterialInfo material = pbr_create_material_info(inputs);
    PBRLighting lighting = pbr_create_lighting();
    if (!inputs.unlit)
    {
        lighting.direct = pbr_evaluate_direct_lighting(material, surface, var_view);
        lighting.indirect = pbr_evaluate_ambient_lighting(material, ambient_light());
    }

    vec3 color = pbr_compose_lighting(inputs, lighting, inputs.occlusion, inputs.occlusion);
    out_fragColor = vec4(pbr_linear_to_srgb(color), pbr_get_alpha(inputs));
}
```

在调用 `pbr_create_material_info()` 前修改采样后的材质输入。如果改变表面的视图空间位置或法线，请调用 `pbr_finalize_surface(surface, var_view)` 更新派生的世界空间字段。对于自定义 BRDF 或各光源的独立贡献，可以使用或替换内置辅助函数中的 `pbr_evaluate_brdf()` 和 `pbr_evaluate_light()`。

可以用自己的环境光照或全局光照替换 `lighting.indirect`。其漫反射和镜面反射贡献是线性的出射光，因此不要再次应用材质的 BRDF。将阴影可见性应用到相应的直接光贡献；`pbr_compose_lighting()` 的可见性参数只影响间接光照。对于 HDR 管线，应将线性颜色写入中间目标，并在最终通道中进行 sRGB 转换。

### 原始材质数据 {#raw-material-data}

对于完全自定义的着色器，声明名为 `PbrMaterial` 的 uniform 块，并使用可识别的成员名称和类型。Defold 会根据源 glTF 材质填充匹配字段。以下声明描述可用的功能结构体；只包含着色器所需的部分。声明结构体只提供数据，采样和光照行为仍需由着色器实现。

包含 `gltf_sampling.glsl` 时，不要重新声明 uniform 块或 `PbrMetallicRoughness`，因为该文件已声明它们。以下声明是供自行管理材质输入的着色器使用的替代方案。

```glsl
struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

struct PbrSpecularGlossiness
{
    vec4 diffuseFactor;
    // RGB: specular (Default=1.0), A: glossiness (Default=1.0)
    vec4 specularAndSpecularGlossinessFactor;
    // R: use diffuseTexture, G: use specularGlossinessTexture
    vec4 specularGlossinessTextures;
};

struct PbrClearCoat
{
    // R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
    vec4 clearCoatAndClearCoatRoughnessFactor;
    // R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
    vec4 clearCoatTextures;
};

struct PbrTransmission
{
    // R: transmission (Default=0.0)
    vec4 transmissionFactor;
    // R: use transmissionTexture
    vec4 transmissionTextures;
};

struct PbrIor
{
    // R: ior (Default=0.0)
    vec4 ior;
};

struct PbrSpecular
{
    // RGB: specularColor, A: specularFactor (Default=1.0);
    vec4 specularColorAndSpecularFactor;
    // R: use specularTexture, G: use specularColorTexture
    vec4 specularTextures;
};

struct PbrVolume
{
    // R: thicknessFactor (Default=0.0), GBA: attenuationColor
    vec4 thicknessFactorAndAttenuationColor;
    // R: attenuationDistance (Default=-1.0)
    vec4 attenuationDistance;
    // R: use thicknessTexture
    vec4 volumeTextures;
};

struct PbrSheen
{
    // RGB: sheenColor, A: sheenRoughnessFactor (Default=0.0)
    vec4 sheenColorAndRoughnessFactor;
    // R: use sheenColorTexture, G: use sheenRoughnessTexture
    vec4 sheenTextures;
};

struct PbrEmissiveStrength
{
    // R: emissiveStrength (Default=1.0)
    vec4 emissiveStrength;
};

struct PbrIridescence
{
    // R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
    vec4 iridescenceFactorAndIorAndThicknessMinMax;
    // R: use iridescenceTexture, G: use iridescenceThicknessTexture
    vec4 iridescenceTextures;
};
```

公共属性和功能结构体是 uniform 块的成员。打包的分量如下：

```glsl
uniform PbrMaterial
{
    // X: alpha cutoff, Y: double-sided, Z: unlit,
    // W: alpha mode (0 = opaque, 1 = mask, 2 = blend)
    vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
    // X: has normal texture, Y: has occlusion texture, Z: has emissive texture
    vec4 pbrCommonTextures;
    // RGB: emissive factor, W: emissive strength
    vec4 pbrEmissiveFactorAndStrength;
    // X: normal scale, Y: occlusion strength
    vec4 pbrNormalScaleAndOcclusionStrength;

    PbrMetallicRoughness pbrMetallicRoughness;
    PbrSpecularGlossiness pbrSpecularGlossiness;
    PbrClearCoat pbrClearCoat;
    PbrTransmission pbrTransmission;
    PbrIor pbrIor;
    PbrSpecular pbrSpecular;
    PbrVolume pbrVolume;
    PbrSheen pbrSheen;
    PbrEmissiveStrength pbrEmissiveStrength;
    PbrIridescence pbrIridescence;
};
```

从块中省略未使用的功能成员。如果缺少该块或某项功能的可识别字段，就不会提供对应数据。纹理存在标志描述源材质的纹理引用；自定义材质仍需要为实际采样的贴图声明匹配的采样器并绑定纹理。

### 常量 {#constants}

功能字段使用 `pbrMetallicRoughness.baseColorFactor` 等名称，公共字段使用 `pbrEmissiveFactorAndStrength` 等名称。引擎从导入的材质填充这些常量；模型没有材质数据时，则使用默认材质。在 `.material` 资源中设置默认值不会覆盖导入的值。

要自定义内置着色，请像上面的示例一样，在推导 BRDF 值前修改采样后的 `PBRMaterial`。如需额外的运行时控制，请声明自己的着色器常量，并使用[模型材质常量 API](/manuals/model/#material-constants)。

## 下一步 {#next-steps}

对于标准 glTF 金属度/粗糙度工作流，请使用内置材质。需要不同的 BRDF、环境光照、阴影或额外 glTF 材质效果时，可以扩展着色器辅助函数或提供自己的材质。

另请参阅：

* [光源手册](/manuals/light)
* [材质手册](/manuals/material)
* [着色器手册](/manuals/shader)
* [渲染手册](/manuals/render)
* [glTF 2.0 规范](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
