---
title: Defold のライトコンポーネント
brief: このマニュアルでは、アンビエントライト、ディレクショナルライト、ポイントライト、スポットライトの使い方と、シェーダーからライトデータにアクセスする方法を説明します。
---

# ライトコンポーネント {#light-component}

ライトコンポーネント（Light component）は、コレクション（collection）内の光源を表します。Defold は現在、4種類のライトリソースをサポートしています。

- アンビエントライト（ambient light） (`.ambient_light`)
- ディレクショナルライト（directional light） (`.directional_light`)
- ポイントライト（point light） (`.point_light`)
- スポットライト（spot light） (`.spot_light`)

ライトリソースは、ほかのコンポーネントリソースと同様にゲームオブジェクト（game object）に追加します。ゲームオブジェクトの直下にライトコンポーネントを作成することも、*Assets* ブラウザーでライトリソースを作成し、*Outline* ビューでゲームオブジェクトにコンポーネントとして追加することもできます。

Defold は、すべてのマテリアル（material）にライティングを自動適用するわけではありません。エンジンはライトを収集し、組み込みのライトバッファーを通じてシェーダー（shader）から利用できるようにします。ライトデータをどのように使用するかは、マテリアルのシェーダーで決定します。

以下の例では同じシーンを使用し、ライトの種類によって最終結果がどのように変わるかを示します。

![ライトのないシーン](images/light/no_light.png)

## ライトのプロパティ {#light-properties}

すべてのライトの色は RGB 値です。ライトリソースではアルファチャンネルを使用しません。

### アンビエントライト {#ambient-light}

アンビエントライトは、シーンに一定の光を加えます。ゲームオブジェクトの位置、回転、スケールの影響は受けません。たとえば、全体的な背景の照明や、オブジェクトをライティングされていないように見せるために使用できます。

アンビエントライトコンポーネントは、エディターでは中心に向かう矢印のアイコンで表示されます。アイコンの色は、その `color` プロパティと同じです。 

![強度の低いアンビエントライト](images/light/ambient_light_less_intensity.png)

プロパティ:

`color`
: アンビエントライトの RGB 色です。

`intensity`
: アンビエントライトの色に乗算します。

![強度の高いアンビエントライト](images/light/ambient_light_full_intensity.png)

アンビエントライトは、シェーダーのライトバッファー内で単一のアンビエント色 `light_info.xyz` に合算されます。`lights[]` 配列のエントリーは使用しません。シーンに複数のアンビエントライトコンポーネントがある場合、それらをすべてブレンドした1つの色だけが出力されます。

### ディレクショナルライト {#directional-light}

ディレクショナルライトは、太陽光のように一定方向から来る光を表します。ゲームオブジェクトの位置やスケールは使用しませんが、光の方向は、ローカルの前方方向 `(0, 0, -1)` にゲームオブジェクトのワールド回転を適用して求めます。

ディレクショナルライトコンポーネントは、エディターでは色付きの太陽のアイコンと、方向を示す 3D の矢印で表示されます。

![ディレクショナルライト](images/light/directional_light.png)

プロパティ:

`color`
: ディレクショナルライトの RGB 色です。

`intensity`
: ディレクショナルライトの色に乗算します。


ディレクショナルライトは、光源と反対側を向いた面が完全に暗くならないように、アンビエントライトと組み合わせて使用されることがよくあります。

![ディレクショナルライトとアンビエントライト](images/light/directional_and_ambient_light.png)

### ポイントライト {#point-light}

ポイントライトは、ゲームオブジェクトのワールド位置から外側へ光を放ちます。ポイントライトの位置は、ゲームオブジェクトのワールド位置から取得します。

ポイントライトコンポーネントは、エディターでは周囲に光線を放つ点で表示され、その色は `color` プロパティを表します。また、`range` を表す円も表示されます。

![ポイントライト](images/light/point_light.png)

プロパティ:

`color`
: ポイントライトの RGB 色です。

`intensity`
: ポイントライトの色に乗算します。

`range`
: ワールド単位で表したライトの半径です。

実際の範囲には、ゲームオブジェクトのワールドスケールの各軸の値の絶対値のうち、最小の値が乗算されます。

![ポイントライトの範囲](images/light/point_light_range.png)

ライトの色を変更するとポイントライトが与える光の色が変わり、範囲を変更すると光源から光が届く距離が変わります。

![緑色のポイントライトの範囲](images/light/point_ight_range_green_color.png)

### スポットライト {#spot-light}

スポットライトは、ゲームオブジェクトのワールド位置から円錐状に光を放ちます。方向は、`(0, 0, -1)` にゲームオブジェクトのワールド回転を適用して求めます。

スポットライトコンポーネントは、エディターでは色付きのランプのアイコンと、外側および内側の円錐を示すガイド線で表示されます。

![スポットライト](images/light/spot_light.png)

プロパティ:

`color`
: スポットライトの RGB 色です。

`intensity`
: スポットライトの色に乗算します。

`range`
: ワールド単位で表したライトの半径です。

`inner_cone_angle`
: エディターで度単位で指定する内側の円錐の角度です。この円錐内のピクセルには、スポットライトの寄与が完全に適用されます。

`outer_cone_angle`
: エディターで度単位で指定する外側の円錐の角度です。光は内側の円錐と外側の円錐の間で減衰します。

実際の範囲には、ゲームオブジェクトのワールドスケールの各軸の値の絶対値のうち、最小の値が乗算されます。円錐の角度は度単位で編集し、コンパイルされたライトリソースではラジアンに変換されます。

![スポットライトのギズモ](images/light/spot_light_gizmos.png)

## 検証 {#validation}

ビルドパイプラインは、ライトリソースのデータを検証して正規化します。

- `color` には、ちょうど3つの数値が含まれている必要があります。
- `intensity` は `0` 以上に制限されます。
- ポイントライトとスポットライトの `range` は `0` 以上に制限されます。
- スポットライトの円錐の角度は `0..180` 度に制限されます。
- `inner_cone_angle` は、`outer_cone_angle` を超えないように制限されます。

## プロジェクトの上限 {#project-limit}

ライトコンポーネントの最大数は、プロジェクト設定の `light.max_count` で制御します。既定値は `64` です。

アンビエントライトはシェーダーの `lights[]` 配列のエントリーを使用しませんが、ライトコンポーネントであるため `light.max_count` の数に含まれます。ディレクショナルライト、ポイントライト、スポットライトは、アクティブな間は `lights[]` のエントリーを使用します。

ライトコンポーネントの数が `light.max_count` を超えると、エンジンはコンポーネントバッファーが満杯であることを示すエラーを報告します。

## シェーダー内のライトバッファー {#light-buffer-in-shaders}

シェーダーは、組み込みのレイアウトを持つ `LightBuffer` という名前のユニフォーム（uniform）ブロックを宣言することで、アクティブなライトにアクセスできます。エンジンはこのブロックを検出し、これを使用するマテリアルとコンピュートプログラムにライトデータを自動的にバインドします。

![ライトバッファーを使用するシェーダー](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: world position, w: unused
    vec4 color;           // rgb: color, a: unused
    vec4 direction_range; // xyz: normalized world direction, w: range
    vec4 params;          // x: type, y: intensity, z: inner cone, w: outer cone
};

uniform LightBuffer
{
    // xyz: accumulated ambient color, w: active non-ambient light count
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

ライトの種類は `lights[i].params.x` に格納されます。

| 種類 | 値 |
|------|-------|
| ディレクショナル | `0` |
| ポイント | `1` |
| スポット | `2` |

シェーダーでは、`light.max_count` より小さい `lights[]` 配列を宣言できますが、それより大きい配列は宣言できません。ライトを処理するループの範囲は、常に宣言した配列のサイズに制限してください。

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

        if (type == 0) // Directional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Point
        {
            result += light_color;
        }
        else if (type == 2) // Spot
        {
            result += light_color;
        }
    }

    return result;
}
```

上の例は、バッファーへのアクセス方法を示しています。実際のポイントライトやスポットライトのシェーダーでは、シェーディング対象の点から `lights[i].position.xyz` へのベクトルも計算し、`lights[i].direction_range.w` を使って距離による減衰を適用することをお勧めします。また、スポットライトでは `lights[i].params.z` と `lights[i].params.w` をラジアン単位の円錐の角度として使用することをお勧めします。

## 組み込みのライティングヘルパー {#built-in-lighting-helper}

Defold には、`/builtins/materials/lighting.glsl` にシェーダーヘルパーが用意されています。`MAX_LIGHT_COUNT` を定義し、ヘルパーが必要とする varying 変数を用意してから、フラグメントシェーダーでヘルパーをインクルードします。

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

このヘルパーは定数 `LIGHT_DIRECTIONAL`、`LIGHT_POINT`、`LIGHT_SPOT` を定義し、`ambient_light()` を公開するとともに、バッファー内のライトに対する Lambert 拡散反射関数を提供します。

## 関連項目 {#see-also}

- [シェーダーマニュアル](/manuals/shader)
- [マテリアルマニュアル](/manuals/material)
- [レンダリングマニュアル](/manuals/render)
