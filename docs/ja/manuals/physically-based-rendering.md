---
title: Defold の物理ベースレンダリング
brief: このマニュアルでは、Defold の組み込み PBR マテリアルの使い方と、物理ベースのシェーディングのカスタマイズ方法を説明します。
---

# 物理ベースレンダリング（PBR） {#physically-based-rendering-pbr}

物理ベースレンダリング（Physically Based Rendering、PBR）は、物理法則を使って光と表面の相互作用をモデル化するシェーディング手法です。ベースカラー、メタリック係数、粗さなどのマテリアルプロパティは、シーンの照明とは独立して表面を記述します。

組み込みの glTF マテリアルは、PBR ライティングを提供します。Defold は、インポートした glTF 2.0 マテリアルのプロパティと、対応する Khronos 拡張のデータも、カスタムシェーダーに公開します。

## 組み込みの PBR マテリアル {#built-in-pbr-materials}

[Model コンポーネント](/manuals/model)の *Scene* に、glTF または GLB ファイルを割り当てます。マテリアルとテクスチャの割り当てをエディターが提案したら、<kbd>Auto Fill</kbd> を選ぶと、既存の割り当てを置き換えて、シーンの生成マテリアルの割り当てを適用します。これらのマテリアルは組み込みの glTF シェーダーを使い、埋め込み画像を直接参照できます。割り当てを保持し、マテリアルとテクスチャを手動で設定するには、<kbd>Keep Current</kbd> を選びます。埋め込みリソースの確認と個々のメッシュの選択は、[モデルのインポート手順](/manuals/importing-models/#using-a-model)を参照してください。

`/builtins/materials/` には、次のマテリアルがあります。モデルと、インスタンシングを使うかどうかに応じて選択します。

| モデルの種類 | マテリアル |
|---|---|
| 静的、インスタンシングなし | `gltf.material` |
| 静的、インスタンシングあり | `gltf_instanced.material` |
| スキニング（アニメーション）、インスタンシングなし | `gltf_skinned.material` |
| スキニング（アニメーション）、インスタンシングあり | `gltf_skinned_instanced.material` |

4つともローカル頂点空間と、同じ `gltf.fp` フラグメントシェーダーを使います。スキニング用の種類は、GPU 上でスキニングを行います。GPU スキニングとインスタンシングについては、[モデルのマテリアル要件](/manuals/model/#material)を参照してください。

テクスチャを手動で割り当てる場合、組み込みマテリアルでは次のサンプラー名を使います。

| テクスチャ | サンプラー | 使用するデータ |
|---|---|---|
| ベースカラー | `PbrMetallicRoughness_baseColorTexture` | RGB カラーとアルファ |
| メタリック・ラフネス | `PbrMetallicRoughness_metallicRoughnessTexture` | G に粗さ、B にメタリック |
| 法線 | `PbrMaterial_normalTexture` | RGB に接空間の法線 |
| オクルージョン | `PbrMaterial_occlusionTexture` | R にオクルージョン |
| 発光 | `PbrMaterial_emissiveTexture` | RGB カラー |

[カメラ](/manuals/camera/#using-the-camera)を設定し、[ライトコンポーネント](/manuals/light)を追加してモデルを照らします。シェーダーは、直接光に平行光源、点光源、スポットライトを使い、単純な環境光の寄与にはアンビエントライトを使います。これらのマテリアルには、デフォルトのレンダースクリプトが描画する `model` タグがあります。カスタムレンダースクリプトでは、一致する述語を描画する必要があります。

### 組み込みシェーダーの動作 {#built-in-shader-behavior}

組み込みシェーダーは、メタリック・ラフネスのシェーディング、ベースカラーと頂点カラー、接線データがある場合の法線マッピング、オクルージョン、発光強度を含む発光を実装します。ベースカラーと発光テクスチャは、ライティング用に sRGB からデコードし、最終色を sRGB に戻します。メタリック・ラフネス、法線、オクルージョンのマップは、線形のデータを含みます。

シェーダーは、ライティングなしのマテリアルとアルファマスクを扱い、両面の表面には法線を調整します。レンダーステートも重要です。

- 両面マテリアルでは、裏面がシェーダーに届くよう、該当するレンダーパスでフェイスカリングを無効にします。
- アルファブレンドでは、シェーダーはストレートアルファを出力します。`graphics.BLEND_FACTOR_SRC_ALPHA` と `graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA` でブレンドを有効にし、レンダースクリプトで透明オブジェクトの描画順と深度書き込みを管理します。デフォルトのモデルパスは、自動ではブレンドを有効にしません。

組み込みの環境光の寄与は近似であり、環境マップによる照明や影は含まれません。クリアコート、透過、シーン（sheen）、虹色効果、スペキュラー・グロッシネスの方式にはカスタムシェーディングが必要です。パラメーターをインポートするだけでは、`gltf.fp` でこれらの効果は有効になりません。

## マテリアルのプロパティの概要 {#material-properties-overview}

以下のプロパティは、モデルコンポーネントに割り当てた glTF 2.0 ソースファイルから解析されます。この一覧は利用可能なマテリアルデータを示し、組み込みのライティングは、そのうち上記の一部を使います。すべてのプロパティが標準ではありません。一部は任意の glTF 拡張で提供され、glTF のエクスポートに使ったツールによって含まれる場合と含まれない場合があります。以下では、プロパティ名の後の括弧内に、対応する拡張を示します。

メタリック・ラフネス
: 光とマテリアルの相互作用を記述します。デフォルトの PBR モデルです。

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
: 表面の両側の描画を要求します。レンダーパスでは、裏面がシェーダーに届くようにする必要があります。

ライティングなし
: true の場合、マテリアルのライティング計算を省略します。

## シェーダーとの連携 {#shader-integration}

以下では、カスタムシェーダーを扱います。適切な組み込みの `.material` リソースと `gltf.fp` をプロジェクトにコピーし、コピーしたマテリアルの *Fragment Program* を自分のシェーダーに向けます。対応するインターフェースも置き換える場合を除き、glTF 頂点プログラム、サンプラー名、ローカル頂点空間は保持します。

組み込みのヘルパーは、テクスチャのサンプリングを、表面の準備、BRDF 計算、ライティングから分離しています。`gltf_sampling.glsl` は、生の `PbrMaterial` ユニフォームブロックを読み、解決済みの線形マテリアル入力を含む `PBRMaterial` 値を生成します。`gltf_lighting.glsl` は、直接光と環境光を提供し、それぞれの寄与を組み合わせます。大文字・小文字の違いにより、生のユニフォームブロックと、サンプリングしたマテリアル構造体を区別します。

### シェーダーの例 {#example-shader}

次のフラグメントシェーダーは、組み込みライティングを保ちつつ、粗さの最小値を引き上げます。4種類すべての glTF マテリアルの頂点プログラムで動作します。

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

`pbr_create_material_info()` を呼ぶ前に、サンプリングしたマテリアル入力を編集します。表面のビュー空間の位置や法線を変更した場合は、`pbr_finalize_surface(surface, var_view)` を呼び、派生するワールド空間のフィールドを更新します。独自の BRDF や個々のライトの寄与には、組み込みヘルパーの `pbr_evaluate_brdf()` と `pbr_evaluate_light()` を使うか、置き換えます。

`lighting.indirect` は、独自の環境光やグローバルイルミネーションに置き換えられます。その拡散反射と鏡面反射の寄与は、線形の出射光なので、マテリアルの BRDF を再び適用しないでください。影の可視性は適切な直接光の寄与に適用します。`pbr_compose_lighting()` の可視性引数が影響するのは間接光のみです。HDR パイプラインでは、中間ターゲットに線形色を書き込み、最終パスで sRGB に変換します。

### 生のマテリアルデータ {#raw-material-data}

完全に独自のシェーダーでは、認識されるメンバー名と型を持つ `PbrMaterial` という名前のユニフォームブロックを宣言します。Defold は、ソースの glTF マテリアルから一致するフィールドを設定します。以下の宣言は利用可能な機能の構造体を示します。シェーダーに必要なものだけを含めてください。構造体の宣言はデータを供給しますが、サンプリングとライティングの動作はシェーダー自身で実装する必要があります。

`gltf_sampling.glsl` はすでにユニフォームブロックと `PbrMetallicRoughness` を宣言するため、インクルードする場合は再宣言しないでください。以下の宣言は、マテリアル入力を自分で管理するシェーダー用の別の選択肢です。

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

共通のプロパティと機能の構造体は、ユニフォームブロックのメンバーです。パックされた成分は、次のとおりです。

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

使わない機能のメンバーは、ブロックから省略します。ブロックや、機能の認識対象フィールドがない場合、そのデータは供給されません。テクスチャの存在フラグは、ソースマテリアルのテクスチャ参照を表します。カスタムマテリアルには、サンプリングするマップに対応したサンプラー宣言とテクスチャ割り当てが引き続き必要です。

### 定数 {#constants}

機能のフィールドには `pbrMetallicRoughness.baseColorFactor` のような名前を、共通のフィールドには `pbrEmissiveFactorAndStrength` のような名前を使います。エンジンは、インポートしたマテリアルから、またはモデルにマテリアルデータがない場合はデフォルトマテリアルから、これらの定数を設定します。`.material` リソースでデフォルト値を設定しても、インポートした値は上書きしません。

組み込みのシェーディングをカスタマイズするには、上記の例のように、BRDF 値を導出する前に、サンプリングした `PBRMaterial` を編集します。実行時に追加の制御を行うには、独自のシェーダー定数を宣言し、[モデルのマテリアル定数 API](/manuals/model/#material-constants) を使います。

## 次のステップ {#next-steps}

標準の glTF メタリック・ラフネス方式には、組み込みマテリアルを使います。別の BRDF、環境光、影、追加の glTF マテリアル効果が必要な場合は、シェーダーヘルパーを拡張するか、独自のマテリアルを用意します。

関連項目:

* [ライトマニュアル](/manuals/light)
* [マテリアルマニュアル](/manuals/material)
* [シェーダーマニュアル](/manuals/shader)
* [レンダリングマニュアル](/manuals/render)
* [glTF 2.0 仕様](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
