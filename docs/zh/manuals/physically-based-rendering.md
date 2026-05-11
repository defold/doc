---
title: Defold 中的基于物理渲染
brief: 本手册介绍如何在 Defold 中访问用于基于物理渲染的材质数据。
---

# 基于物理渲染 (PBR)

基于物理渲染（Physically Based Rendering，PBR）是一种着色方法，它根据真实世界的物理原则模拟光线与表面的交互方式。它可以在不同环境中产生一致、逼真的光照效果，并让资源在各种光照条件下都能正确显示。

Defold 的 PBR 实现遵循 glTF 2.0 材质规范以及相关的 Khronos 扩展。当你把 glTF 资源导入 Defold 时，材质属性会被自动解析并保存为结构化材质数据，运行时可在着色器中访问这些数据。

PBR 材质可以包含金属反射、表面粗糙度、透射、清漆层、次表面散射、虹彩等效果。

::: sidenote
Defold 目前会把 PBR 材质数据暴露给着色器，但还没有提供内置的 PBR 光照模型。你可以在自己的光照和反射着色器中使用这些数据来实现基于物理的渲染。默认 PBR 光照模型会在后续阶段加入 Defold。
:::

::: sidenote
Defold 目前不会自动分配 glTF 文件中的嵌入纹理。只有材质参数会暴露给着色器。你仍然可以手动把纹理分配给模型组件，并在着色器中对它们采样。
:::

## 材质属性概览

材质属性从分配给模型组件的 glTF 2.0 源文件中解析而来。并非所有属性都是标准属性。有些属性来自可选的 glTF 扩展，而这些扩展是否存在取决于导出 glTF 文件时使用的工具。下面会在属性名称后的括号中标出相关扩展。

Metallic roughness
: 描述光线如何与材质交互。这是默认的 PBR 模型。

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
: 如果为 true，则渲染表面的两面。

Unlit
: 如果为 true，则材质跳过光照计算。

::: sidenote
这些属性中有一部分只是提示材质应如何渲染。属性数据（alpha cutoff、alpha mode、double sided 和 unlit）可以在着色器中访问，但不会影响 Defold 中材质的实际渲染方式。
:::

## 着色器集成

PBR 材质数据会根据类型和命名约定暴露给着色器。PBR 材质系统通过名为 `PbrMaterial` 的结构化 uniform 块，把所有已解析的材质参数提供给着色器。每个受支持的 glTF 扩展都对应这个块中的一个结构体，并可使用 #define 标志进行条件编译。

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

材质的各项功能在着色器中以固定结构体表示。由于 Defold 内部用 vec4 设置常量，数据会尽可能打包到 vec4 中。对于经过打包的数据，下面每个功能的着色器片段都会在注释中标出：

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
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
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

通用属性设置在材质 uniform 本身上（同样要注意数据会打包到 vec4 中）。

```glsl
// Common textures
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

uniform PbrMaterial
{
	// Common properties:

	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Other properties...
};
```

### 示例着色器

下面是一个包含所有功能的示例着色器，并给出了一套建议的纹理绑定命名方案（这些绑定仍然需要手动处理）。注意，你可以像下面示例中那样，在 PbrMaterial 的各个成员周围使用 define 来关闭功能：

```glsl
// Feature flags, comment or remove these to slim down the shader.
#define PBR_METALLIC_ROUGHNESS
#define PBR_SPECULAR_GLOSSINESS
#define PBR_CLEARCOAT
#define PBR_TRANSMISSION
#define PBR_IOR
#define PBR_SPECULAR
#define PBR_VOLUME
#define PBR_SHEEN
#define PBR_EMISSIVE_STRENGTH
#define PBR_IRIDESCENCE

// Common
uniform sampler2D PbrMaterial_normalTexture;
uniform sampler2D PbrMaterial_occlusionTexture;
uniform sampler2D PbrMaterial_emissiveTexture;

// PbrMetallicRoughness
uniform sampler2D PbrMetallicRoughness_baseColorTexture;
uniform sampler2D PbrMetallicRoughness_metallicRoughnessTexture;

struct PbrMetallicRoughness
{
    vec4 baseColorFactor;
    // R: metallic (Default=1.0), G: roughness (Default=1.0)
    vec4 metallicAndRoughnessFactor;
    // R: use baseColorTexture, G: use metallicRoughnessTexture
    vec4 metallicRoughnessTextures;
};

// PbrSpecularGlossiness
uniform sampler2D PbrSpecularGlossiness_diffuseTexture;
uniform sampler2D PbrSpecularGlossiness_specularGlossinessTexture;

struct PbrSpecularGlossiness
{
	vec4 diffuseFactor;
	// RGB: specular (Default=1.0), A: glossiness (Default=1.0)
	vec4 specularAndSpecularGlossinessFactor;
	// R: use diffuseTexture, G: use specularGlossinessTexture
	vec4 specularGlossinessTextures;
};

// PbrClearCoat
uniform sampler2D PbrClearCoat_clearcoatTexture;
uniform sampler2D PbrClearCoat_clearcoatRoughnessTexture;
uniform sampler2D PbrClearCoat_clearcoatNormalTexture;

struct PbrClearCoat
{
	// R: clearCoat (Default=0.0), G: clearCoatRoughness (Default=0.0)
	vec4 clearCoatAndClearCoatRoughnessFactor;
	// R: use clearCoatTexture, G: use clearCoatRoughnessTexture, B: use clearCoatNormalTexture
	vec4 clearCoatTextures;
};

// PbrTransmission
uniform sampler2D PbrTransmission_transmissionTexture;

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

// PbrSpecular
uniform sampler2D PbrSpecular_specularTexture;
uniform sampler2D PbrSpecular_specularColorTexture;

struct PbrSpecular
{
	// RGB: specularColor, A: specularFactor (Default=1.0);
	vec4 specularColorAndSpecularFactor;
	// R: use specularTexture, G: use specularColorTexture
	vec4 specularTextures;
};

// PbrVolume
uniform sampler2D PbrVolume_thicknessTexture;

struct PbrVolume
{
	// R: thicknessFactor (Default=0.0), RGB: attenuationColor
	vec4 thicknessFactorAndAttenuationColor;
	// R: attentuationDistance (Default=-1.0)
	vec4 attenuationDistance;
	// R: use thicknessTexture
	vec4 volumeTextures;
};

// PbrSheen
uniform sampler2D PbrSheen_sheenColorTexture;
uniform sampler2D PbrSheen_sheenRoughnessTexture;

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

// PbrIridescence
uniform sampler2D PbrEmissive_iridescenceTexture;
uniform sampler2D PbrEmissive_iridescenceThicknessTexture;

struct PbrIridescence
{
	// R: iridescenceFactor (Default=0.0), G: iridescenceIor (Default=1.3), B: iridescenceThicknessMin (Default=100.0), A: iridescenceThicknessMax (Default=400.0)
	vec4 iridescenceFactorAndIorAndThicknessMinMax;
	// R: use iridescenceTexture, G: use iridescenceThicknessTexture
	vec4 iridescenceTextures;
};

uniform PbrMaterial
{
	// Common properties
	// R: alphaCutoff (Default=0.5), G: doubleSided (Default=false), B: unlit (Default=false)
	vec4 pbrAlphaCutoffAndDoubleSidedAndIsUnlit;
	// R: use normalTexture, G: use occlusionTexture, B: use emissiveTexture
	vec4 pbrCommonTextures;

	// Features
#ifdef PBR_METALLIC_ROUGHNESS
	PbrMetallicRoughness  pbrMetallicRoughness;
#endif
#ifdef PBR_SPECULAR_GLOSSINESS
	PbrSpecularGlossiness pbrSpecularGlossiness;
#endif
#ifdef PBR_CLEARCOAT
	PbrClearCoat pbrClearCoat;
#endif
#ifdef PBR_TRANSMISSION
	PbrTransmission pbrTransmission;
#endif
#ifdef PBR_IOR
	PbrIor pbrIor;
#endif
#ifdef PBR_SPECULAR
	PbrSpecular pbrSpecular;
#endif
#ifdef PBR_VOLUME
	PbrVolume pbrVolume;
#endif
#ifdef PBR_SHEEN
	PbrSheen pbrSheen;
#endif
#ifdef PBR_EMISSIVE_STRENGTH
	PbrEmissiveStrength pbrEmissiveStrength;
#endif
#ifdef PBR_IRIDESCENCE
	PbrIridescence pbrIridescence;
#endif
};
```

::: sidenote
如果材质结构体中找不到某些具体数据点，这些功能的数据就不会被设置。例如，如果材质结构体中没有 `pbrClearCoat`，就不会设置清漆层数据。如果找不到 uniform 块，渲染时就不会设置任何数据。
:::

### 常量

每个材质属性都对应 Defold 内部的一个渲染常量。你可以在材质资源本身上定义常量来覆盖默认值，命名模式为 `pbrFeature.structMember`。如果 glTF 材质中缺少匹配数据，这些值会自动应用。

![Material constants](images/physically-based-rendering/material-constants.png)

## 下一步

要把这些材质数据用于基于物理的光照，请在片段着色器中使用 `PbrMaterial` 块提供的参数实现 BRDF。

另请参阅：

* [着色器手册](/manuals/shader)
* [渲染手册](/manuals/render)
* [glTF 2.0 规范](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
