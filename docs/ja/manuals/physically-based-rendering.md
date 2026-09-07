---
title: Defold の物理ベースレンダリング
brief: このマニュアルでは、Defold で物理ベースレンダリング用のマテリアルデータにアクセスする方法の基本を説明します。
---

# 物理ベースレンダリング（PBR） {#physically-based-rendering-pbr}

物理ベースレンダリング（Physically Based Rendering、PBR）は、現実世界の物理法則を使って、光と表面の相互作用をモデル化するシェーディング手法です。異なる環境でも一貫性のあるリアルなライティングを生み出し、幅広い照明条件でアセットを適切な見た目にできます。

Defold の PBR 実装は、glTF 2.0 のマテリアル（material）仕様と関連する Khronos 拡張に従っています。glTF アセットを Defold にインポートすると、マテリアルのプロパティが自動的に解析され、実行時にシェーダー（shader）からアクセスできる構造化されたマテリアルデータとして保存されます。

PBR マテリアルには、金属的な反射、表面の粗さ、透過、クリアコート、表面下散乱、虹色効果などの効果を含められます。

::: sidenote
現在、Defold は PBR マテリアルデータをシェーダーに公開していますが、組み込みの PBR ライティングモデルは提供していません。このデータを独自のライティングや反射のシェーダーで使用して、物理ベースレンダリングを実現できます。デフォルトの PBR ライティングモデルは、今後 Defold に追加される予定です。
:::

::: sidenote
現在、glTF ファイルに埋め込まれたテクスチャは Defold で自動的に割り当てられません。シェーダーに公開されるのはマテリアルのパラメーターのみです。テクスチャをモデルコンポーネント（model component）に手動で割り当て、シェーダーでサンプリングすることはできます。
:::

## マテリアルのプロパティの概要 {#material-properties-overview}

マテリアルのプロパティは、モデルコンポーネントに割り当てられた glTF 2.0 ソースファイルから解析されます。すべてのプロパティが標準仕様に含まれるわけではありません。一部は任意の glTF 拡張によって提供され、glTF ファイルのエクスポートに使用するツールによって、含まれる場合と含まれない場合があります。以下では、プロパティ名の後の括弧内に対応する拡張を示しています。

メタリック・ラフネス
: 光がマテリアルとどのように相互作用するかを記述します。デフォルトの PBR モデルです。

スペキュラー・グロッシネス (KHR_materials_pbrSpecularGlossiness)
: メタリック・ラフネスの代替となるモデルです。古いアセットでよく使用されます。

クリアコート (KHR_materials_clearcoat)
: 独自の粗さと法線マップを持つ透明なコーティング層を追加します。

屈折率 (KHR_materials_ior)
: 屈折率を追加します。

スペキュラー (KHR_materials_specular)
: スペキュラーの強度と色の専用チャンネルを追加します。

虹色効果 (KHR_materials_iridescence)
: シャボン玉や真珠のようなマテリアルの薄膜干渉をシミュレートします。

シーン（Sheen） (KHR_materials_sheen)
: 布のような微細な表面の反射をモデル化します。

透過 (KHR_materials_transmission)
: 透明なマテリアルやガラスのようなマテリアルの光の透過をモデル化します。

ボリューム (KHR_materials_volume)
: 厚みや減衰など、体積に関わる効果に対応します。

発光強度 (KHR_materials_emissive_strength)
: ベースカラーとは独立して発光の明るさを制御します。

法線マップ
: 表面の細部を表現する法線マップです。

オクルージョンマップ
: アンビエントオクルージョンマップです。

発光マップ
: 光る表面のための自己発光テクスチャです。

発光係数
: 発光強度に対する RGB の乗数です。

アルファカットオフ
: マスクによる透過処理のしきい値です。

アルファモード
: Opaque（不透明）、Masked（マスク）、または Blended（ブレンド）による透過モードです。

両面描画
: true の場合、表面の両側が描画されます。

ライティングなし
: true の場合、マテリアルのライティング計算を省略します。

::: sidenote
これらのプロパティの一部は、マテリアルをどのようにレンダリングすべきかを示す情報を提供します。これらのプロパティ（アルファカットオフ、アルファモード、両面描画、ライティングなし）のデータはシェーダーで利用できますが、Defold でのマテリアルのレンダリング方法には影響しません。
:::

## シェーダーとの連携 {#shader-integration}

PBR マテリアルデータは、型と命名規則に基づいてシェーダーに公開されます。PBR マテリアルシステムは、解析したすべてのマテリアルパラメーターを、`PbrMaterial` という名前の構造化されたユニフォーム（uniform）ブロックを通じてシェーダーに提供します。サポートされている各 glTF 拡張は、このブロック内の構造体に対応し、`#define` フラグを使って条件付きコンパイルができます。

```glsl
uniform PbrMaterial
{
	// Material properties
};
```

マテリアルの各種機能は、シェーダー内で決まった構造体として指定されます。データは可能な限り `vec4` にまとめられています。これは、Defold 内部で定数をその形式で設定するためです。データをまとめている場合は、以下の各機能のシェーダーコード例にあるコメントでその配置を示しています。

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

共通のプロパティは、マテリアルのユニフォーム自体に設定されます（ここでもデータを `vec4` にまとめている点に注意してください）。

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

### シェーダーの例 {#example-shader}

以下は、すべての機能と、テクスチャバインディングの命名規則の案を含むシェーダーの例です（繰り返しになりますが、テクスチャバインディングは手動で扱う必要があります）。以下の例のように、`PbrMaterial` 自体の各メンバーを `#define` を使った条件で囲むだけで、機能を無効にできます。

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
マテリアル構造体内で特定のデータ項目が見つからない場合、その機能のデータは設定されません。たとえば、マテリアル構造体内に `pbrClearCoat` がない場合、クリアコートのデータは設定されません。ユニフォームブロックが見つからない場合は、レンダリング時に一切のデータが設定されません。
:::

### 定数 {#constants}

各マテリアルプロパティは、Defold 内部のレンダー定数に対応します。`pbrFeature.structMember` という命名パターンに従ってマテリアルリソース自体に定数を定義すると、デフォルト値を上書きできます。対応するデータが glTF マテリアルに存在しない場合、これらの値が自動的に適用されます。

![マテリアル定数](images/physically-based-rendering/material-constants.png)

## 次のステップ {#next-steps}

物理ベースのライティングにマテリアルデータを使用するには、`PbrMaterial` ブロックで提供されるパラメーターを使って、フラグメントシェーダーに BRDF を実装します。
関連項目:

* [シェーダーマニュアル](/manuals/shader)
* [レンダリングマニュアル](/manuals/render)
* [glTF 2.0 仕様](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
