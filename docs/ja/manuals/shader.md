---
title: Defold のシェーダープログラム
brief: このマニュアルでは、頂点シェーダーとフラグメントシェーダーの詳細、および Defold での使い方を説明します。
---

# シェーダー {#shaders}

シェーダープログラム（shader program）は、グラフィックスのレンダリングの中核を担います。GLSL（GL Shading Language）という C に似た言語で記述されたプログラムで、グラフィックスハードウェア上で実行され、基になる 3D データ（頂点）や、最終的に画面に表示されるピクセル（「フラグメント」）を処理します。シェーダーは、スプライト（sprite）の描画、3D モデル（model）のライティング、フルスクリーンのポストエフェクトの作成など、さまざまな用途に使われます。

このマニュアルでは、Defold のレンダリングパイプライン（rendering pipeline）と GPU シェーダーがどのように連携するかを説明します。コンテンツ用のシェーダーを作成するには、マテリアル（material）の概念とレンダリングパイプラインの仕組みも理解する必要があります。

* レンダリングパイプラインの詳細は、[レンダリングのマニュアル](/manuals/render)を参照してください。
* マテリアルの詳細は、[マテリアルのマニュアル](/manuals/material)を参照してください。
* コンピュートプログラムの詳細は、[コンピュートのマニュアル](/manuals/compute)を参照してください。

OpenGL ES 2.0（OpenGL for Embedded Systems）および OpenGL ES Shading Language の仕様は、[Khronos OpenGL Registry](https://www.khronos.org/registry/gles/)で確認できます。

デスクトップコンピューターでは、OpenGL ES 2.0 では利用できない機能を使ってシェーダーを記述できることに注意してください。グラフィックスカードのドライバーが、モバイルデバイスでは動作しないシェーダーコードを問題なくコンパイルして実行することがあります。


## 概念 {#concepts}

頂点シェーダー
: 頂点シェーダー（vertex shader）は頂点を作成したり削除したりできず、頂点の位置だけを変更できます。頂点シェーダーは通常、頂点の位置を 3D のワールド空間から 2D のスクリーン空間へ変換するために使われます。

  頂点シェーダーの入力は、頂点データ（`attributes` の形式）と、ユニフォーム（uniform）と呼ばれる定数（`uniforms`）です。一般的な定数には、頂点の位置をスクリーン空間に変換して投影するために必要な行列があります。

  頂点シェーダーの出力は、計算された頂点のスクリーン座標（`gl_Position`）です。`varying` 変数を介して、頂点シェーダーからフラグメントシェーダーへデータを渡すこともできます。

フラグメントシェーダー
: 頂点シェーダーの処理が終わると、生成されたプリミティブの各フラグメント（またはピクセル）の色を決める役割をフラグメントシェーダー（fragment shader）が担います。

  フラグメントシェーダーの入力は、定数（`uniforms`）と、頂点シェーダーで設定されたすべての `varying` 変数です。

  フラグメントシェーダーの出力は、対象のフラグメントの色の値（`gl_FragColor`）です。

コンピュートシェーダー
: コンピュートシェーダー（compute shader）は、GPU 上であらゆる種類の処理に使える汎用シェーダーです。グラフィックスパイプラインにはまったく属さず、独立した実行コンテキストで実行され、ほかのシェーダーからの入力に依存しません。

  コンピュートシェーダーの入力は、定数バッファー（`uniforms`）、テクスチャ画像（`image2D`）、サンプラー（sampler、`sampler2D`）、ストレージバッファー（`buffer`）です。

  コンピュートシェーダーの出力は明示的には定義されておらず、頂点シェーダーやフラグメントシェーダーとは異なり、生成しなければならない特定の出力はありません。コンピュートシェーダーは汎用的なため、どのような結果を生成するかはプログラマーが定義します。

ワールド行列
: モデルの形状を構成する頂点の位置は、モデルの原点を基準として保存されます。これは「モデル空間」と呼ばれます。一方、ゲームワールド（game world）は「ワールド空間」であり、各頂点の位置、向き、スケールはワールドの原点を基準として表されます。この2つを分けることで、ゲームエンジンはモデルコンポーネント（component）に保存された元の頂点の値を壊さずに、各モデルを移動、回転、拡大縮小できます。

  モデルをゲームワールドに配置するときは、モデルのローカル頂点座標をワールド座標へ変換する必要があります。この変換には、*ワールド変換行列（world transform matrix）* を使います。この行列は、ゲームワールドの座標系に正しく配置するためにモデルの頂点へ適用する平行移動、回転、スケールを表します。

  ![ワールド変換](images/shader/world_transform.png)

ビュー行列と投影行列
: ゲームワールドの頂点を画面に表示するには、まず各行列の 3D 座標をカメラからの相対座標へ変換します。これには _ビュー行列（view matrix）_ を使います。次に、_投影行列（projection matrix）_ を使って頂点を 2D のスクリーン空間へ投影します。

  ![投影](images/shader/projection.png)

属性
: 個々の頂点に関連付けられた値です。属性（attribute）はエンジンからシェーダーへ渡されます。属性にアクセスするには、シェーダープログラム内で宣言するだけです。コンポーネントの種類ごとに、異なる属性の組み合わせがあります。
  - スプライトには `position` と `texcoord0` があります。
  - タイルグリッド（Tilegrid）には `position` と `texcoord0` があります。
  - GUI ノードには `position`、`textcoord0`、`color` があります。
  - ParticleFX には `position`、`texcoord0`、`color` があります。
  - モデルには `position`、`texcoord0`、`normal` があります。
  - フォントには `position`、`texcoord0`、`face_color`、`outline_color`、`shadow_color` があります。

定数
: シェーダー定数（shader constant）の値は、レンダリングのドローコールが続く間は変わりません。定数はマテリアルファイルの *Constants* セクションに追加し、その後シェーダープログラムで `uniform` として宣言します。サンプラーのユニフォームはマテリアルの *Samplers* セクションに追加し、その後シェーダープログラムで `uniform` として宣言します。頂点シェーダーで頂点を変換するために必要な行列は、定数として利用できます。

  - `CONSTANT_TYPE_WORLD` は、オブジェクトのローカル座標空間からワールド空間へ変換する*ワールド行列*です。
  - `CONSTANT_TYPE_VIEW` は、ワールド空間からカメラ空間へ変換する*ビュー行列*です。
  - `CONSTANT_TYPE_PROJECTION` は、カメラ空間からスクリーン空間へ変換する*投影行列*です。
  - `CONSTANT_TYPE_WORLDVIEW`、`CONSTANT_TYPE_VIEWPROJ`、`CONSTANT_TYPE_WORLDVIEWPROJ` は、それぞれ対応する行列を合成したものを提供します。
  - `CONSTANT_TYPE_WORLD_INVERSE`、`CONSTANT_TYPE_VIEW_INVERSE`、`CONSTANT_TYPE_PROJECTION_INVERSE`、`CONSTANT_TYPE_VIEWPROJ_INVERSE`、`CONSTANT_TYPE_WORLDVIEW_INVERSE`、`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE` は逆行列を提供するため、シェーダーで計算する必要がありません。
  - `CONSTANT_TYPE_TIME` はエンジンが提供する `vec4` で、`.x` はエンジンの起動からの経過時間、`.y` はフレームのデルタ時間、`.z` と `.w` はゼロです。
  - `CONSTANT_TYPE_USER` は、自由に使える `vec4` 型の定数です。

  定数の指定方法は、[マテリアルのマニュアル](/manuals/material)で説明しています。

サンプラー
: シェーダーでは、*サンプラー*型のユニフォーム変数を宣言できます。サンプラーは、画像ソースから値を読み取るために使われます。

  - `sampler2D` は、2D 画像テクスチャからサンプリングします。
  - `sampler2DArray` は、2D 画像の配列テクスチャからサンプリングします。主にページ分割されたアトラス（atlas）で使われます。
  - `samplerCube` は、6枚の画像からなるキューブマップ（cubemap）テクスチャからサンプリングします。
  - `image2D` は、画像オブジェクトのテクスチャデータを読み込みます（書き込むこともあります）。主にコンピュートシェーダーでのデータ格納に使われます。

  サンプラーは、GLSL 標準ライブラリのテクスチャ参照関数でのみ使えます。サンプラーの設定方法は、[マテリアルのマニュアル](/manuals/material)で説明しています。

UV 座標
: 頂点に関連付けられた 2D 座標で、2D テクスチャ上の点に対応します。これにより、頂点の集合で表される形状に、テクスチャの一部または全体を描画できます。

  ![UV 座標](images/shader/uv_map.png)

  UV マップは通常、3D モデリングプログラムで生成され、メッシュ（mesh）に保存されます。各頂点のテクスチャ座標は、属性として頂点シェーダーへ渡されます。その後、`varying` 変数を使って、頂点の値から補間された各フラグメントの UV 座標を求めます。

varying 変数
: `Varying` 型の変数は、頂点ステージとフラグメントステージの間で情報を渡すために使われます。

  1. 頂点シェーダーで、頂点ごとに varying 変数を設定します。
  2. ラスタライズの際に、描画されるプリミティブ上の各フラグメントについてこの値が補間されます。フラグメントと形状の各頂点との距離によって、補間される値が決まります。
  3. フラグメントシェーダーの呼び出しごとに変数が設定され、フラグメントの計算で使えます。

  ![varying の補間](images/shader/varying_vertex.png)

  たとえば、三角形の各頂点で `varying` に `vec3` の RGB 色の値を設定すると、形状全体にわたって色が補間されます。同様に、長方形の各頂点にテクスチャマップの参照座標（*UV 座標*）を設定すると、フラグメントシェーダーで形状の領域全体にわたってテクスチャの色の値を参照できます。

  ![varying の補間](images/shader/varying.png)

## モダンな GLSL シェーダーの記述 {#writing-modern-glsl-shaders}

Defold エンジンは複数のプラットフォームとグラフィックス API をサポートしているため、開発者がどこでも動作するシェーダーを簡単に記述できる必要があります。アセットパイプラインは、主に次の2つの方式（以降、シェーダーパイプライン（`shader pipelines`）と呼びます）でこれを実現します。

1. シェーダーを ES2 互換の GLSL コードで記述する、レガシーパイプラインです。
2. シェーダーを SPIR-v 互換の GLSL コードで記述する、モダンパイプラインです。

Defold 1.9.2 以降では、新しいパイプラインを使うシェーダーの記述を推奨します。そのためには、ほとんどのシェーダーを、バージョン 140（OpenGL 3.1）以降で記述されたシェーダーへ移行する必要があります。シェーダーを移行するには、次の要件を満たしていることを確認してください。

### バージョン宣言 {#version-declaration}
シェーダーの先頭に、少なくとも #version 140 を指定します。

```glsl
#version 140
```

ビルド処理ではこの指定によりシェーダーパイプラインが選択されるため、従来のシェーダーも引き続き使えます。バージョンを指定するプリプロセッサーディレクティブが見つからない場合、Defold はレガシーパイプラインにフォールバックします。

### 属性 {#attributes}
頂点シェーダーでは、`attribute` キーワードを `in` に置き換えます。

```glsl
// instead of:
// attribute vec4 position;
// do:
in vec4 position;
```

注意: フラグメントシェーダー（およびコンピュートシェーダー）は、頂点の入力を一切受け取りません。

### varying 変数 {#varyings}
頂点シェーダーでは、varying 変数の前に `out` を付けます。フラグメントシェーダーでは、varying 変数に `in` を使います。

```glsl
// In a vertex shader, instead of:
// varying vec4 var_color;
// do:
out vec4 var_color;

// In a fragment shader, instead of:
// varying vec4 var_color;
// do:
in vec4 var_color;
```

### ユニフォーム（Defold では定数と呼びます） {#uniforms-called-constants-in-defold}

不透明型のユニフォーム（サンプラー、画像、アトミック、SSBO）は移行が不要で、従来どおり使えます。

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

不透明型ではないユニフォームは、ユニフォームブロック（`uniform block`）内に配置する必要があります。ユニフォームブロックはユニフォーム変数をまとめたもので、`uniform` キーワードを使って宣言します。

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Individual members of the uniform block can be used as-is
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

ユニフォームブロック内のすべてのメンバーは、個々の定数としてマテリアルやコンポーネントから利用できます。レンダリングの定数バッファーや `go.set` と `go.get` の使用にあたっては、移行は不要です。

### 組み込み変数 {#built-in-variables}

フラグメントシェーダーでは、バージョン 140 以降で `gl_FragColor` が非推奨になっています。代わりに `out` を使います。

```glsl
// instead of:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// do:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### テクスチャ関数 {#texture-functions}

`texture2D` や `texture2DArray` などの個別のテクスチャサンプリング関数は、すでに存在しません。代わりに `texture` 関数を使います。

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// instead of:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// do:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### 精度 {#precision}

Defold は、GLSL ES 向けにシェーダーをクロスコンパイルするときに、グローバルなデフォルトの精度修飾子を生成します。デフォルトは、浮動小数点数では `mediump`、整数では `highp` です。これらは[プロジェクト設定](/manuals/project-settings/#shader)の **GLSL ES Default Precision Float**（`shader.glsl_es_default_precision_float`）と **GLSL ES Default Precision Int**（`shader.glsl_es_default_precision_int`）で変更でき、どちらも `mediump` または `highp` を指定できます。

変数、入力、出力に明示的に指定した修飾子は、生成されたグローバルなデフォルトより優先されます。OpenGL ES 2.0 と WebGL 1.0 のフラグメントシェーダーでは、すべてのデバイスが `highp` をサポートしているわけではありません。グローバルなデフォルトとして `highp` を選択すると、Defold は `GL_FRAGMENT_PRECISION_HIGH` でその使用を保護し、サポートしていないデバイスでは `mediump` にフォールバックします。

### すべてを組み合わせる {#putting-it-together}

最後に、これらの規則をすべて適用した例として、組み込みのスプライトシェーダーを新しい形式に変換したものを示します。

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// positions are in world space
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Premultiply alpha since all runtime textures already are
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## シェーダーへのスニペットのインクルード {#including-snippets-into-shaders}

Defold のシェーダーでは、プロジェクト内の拡張子が `.glsl` のファイルからソースコードをインクルードできます。シェーダーから glsl ファイルをインクルードするには、`#include` プラグマを使い、ファイルを二重引用符または山括弧で囲みます。インクルードでは、プロジェクトからの相対パスか、インクルードする側のファイルからの相対パスを指定する必要があります。

```glsl
// In file /main/my-shader.fp

// Absolute path
#include "/main/my-snippet.glsl"
// The file is in the same folder
#include "my-snippet.glsl"
// The file is in a sub-folder on the same level as 'my-shader'
#include "sub-folder/my-snippet.glsl"
// The file is in a sub-folder on the parent directory, i.e /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// The file is on the parent directory, i.e /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

インクルードの処理には、いくつか注意点があります。

  - ファイルはプロジェクトを基準に指定する必要があり、インクルードできるのはプロジェクト内にあるファイルだけです。絶対パスは必ず先頭に `/` を付けて指定します。
  - コードはファイル内のどこにでもインクルードできますが、文の途中にインラインでファイルをインクルードすることはできません。たとえば、`const float #include "my-float-name.glsl" = 1.0` は動作しません。

### ヘッダーガード {#header-guards}

スニペット自体からもほかの `.glsl` ファイルをインクルードできるため、最終的に生成されるシェーダーに同じコードが複数回含まれる可能性があります。ファイルの内容によっては、同じシンボルが複数回宣言され、コンパイル時に問題が発生することがあります。これを避けるには、複数のプログラミング言語で共通して使われる概念である *ヘッダーガード（header guard）* を使えます。次に例を示します。

```glsl
// In my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// In math-functions.glsl
#include "pi.glsl"

// In pi.glsl
const float PI = 3.14159265359;
```

この例では、`PI` 定数が2回定義されるため、プロジェクトの実行時にコンパイラーエラーが発生します。代わりに、ヘッダーガードで内容を保護することをお勧めします。

```glsl
// In pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

`pi.glsl` のコードは `my-shader.vs` 内で2回展開されますが、ヘッダーガードで囲んでいるため PI シンボルは1回だけ定義され、シェーダーを正常にコンパイルできます。

ただし、用途によっては必ずしも必要ではありません。関数内などでコードをローカルに再利用し、値をシェーダーコード全体で利用できるようにする必要がない場合は、ヘッダーガードを使わないほうがよいでしょう。次に例を示します。

```glsl
// In red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// In my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## エディター専用のシェーダーコード {#editor-specific-shader-code}

Defold エディターのビューポートでシェーダーをレンダリングするときは、プリプロセッサー定義 `EDITOR` を利用できます。これにより、エディターで実行するときと実際のゲームエンジンで実行するときで、異なる動作をするシェーダーコードを記述できます。

これは特に、次の用途で役立ちます。
  - エディター内だけで表示するデバッグ用の可視化を追加します。
  - ワイヤーフレームモードやマテリアルプレビューなど、エディター専用の機能を実装します。
  - エディターのビューポートで正しく動作しない可能性があるマテリアルに、フォールバックのレンダリングを用意します。

`#ifdef EDITOR` プリプロセッサーディレクティブを使い、エディター内だけで実行するコードを条件付きでコンパイルします。

```glsl
#ifdef EDITOR
    // This code will only execute when the shader is rendered in the Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Magenta color for editor preview
#else
    // This code will execute when running in the game
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## レンダリングの処理 {#the-rendering-process}

ゲーム用に作成したデータは、画面に表示されるまでに一連の処理を経ます。

![レンダリングパイプライン](images/shader/pipeline.png)

すべてのビジュアルコンポーネント（スプライト、GUI ノード、パーティクルエフェクト、モデル）は、コンポーネントの形状を表す 3D ワールド内の点である頂点から構成されます。この利点は、どの角度や距離からでも形状を見ることができることです。頂点シェーダープログラムの役割は、1つの頂点を受け取り、形状を画面に表示できるようにビューポート内の位置へ変換することです。頂点が4つある形状では、頂点シェーダープログラムが4回、それぞれ並列に実行されます。

![頂点シェーダー](images/shader/vertex_shader.png)

プログラムの入力は、頂点の位置（および頂点に関連付けられたほかの属性データ）です。出力は、新しい頂点の位置（`gl_Position`）と、フラグメントごとに補間するすべての `varying` 変数です。

最も単純な頂点シェーダープログラムは、出力する頂点の位置をゼロに設定するだけです（あまり役には立ちません）。

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

より完全な例として、組み込みのスプライトの頂点シェーダーを示します。

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. ビュー行列と投影行列を乗算した結果を格納するユニフォーム（定数）です。
2. スプライトの頂点の属性です。`position` はすでにワールド空間へ変換されています。`texcoord0` には頂点の UV 座標が格納されています。
3. varying 出力変数を宣言します。この変数は、各頂点に設定された値の間でフラグメントごとに補間され、フラグメントシェーダーへ送られます。
4. `gl_Position` には、投影空間における現在の頂点の出力位置が設定されます。この値は、`x`、`y`、`z`、`w` の4つの成分を持ちます。`w` 成分は、透視投影を正しく反映した補間を計算するために使われます。変換行列を適用する前のこの値は、通常、各頂点で 1.0 です。
5. この頂点の位置に対する varying の UV 座標を設定します。ラスタライズ後にフラグメントごとに補間され、フラグメントシェーダーへ送られます。




頂点シェーダーの処理が終わると、コンポーネントの画面上の形状が決まります。プリミティブの形状が生成され、ラスタライズされます。これは、グラフィックスハードウェアが各形状を*フラグメント*、つまりピクセルに分割することを意味します。その後、フラグメントごとに1回、フラグメントシェーダープログラムを実行します。画面上の画像が 16 × 24 ピクセルの場合、プログラムは384回、それぞれ並列に実行されます。

![フラグメントシェーダー](images/shader/fragment_shader.png)

プログラムの入力は、レンダリングパイプラインと頂点シェーダーから送られるもので、通常はフラグメントの *UV 座標*や色調を指定する色などです。出力は、ピクセルの最終的な色（`gl_FragColor`）です。

最も単純なフラグメントシェーダープログラムは、各ピクセルの色を黒に設定するだけです（これもあまり役に立つプログラムではありません）。

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

ここでも、より完全な例として組み込みのスプライトのフラグメントシェーダーを示します。

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. varying のテクスチャ座標変数を宣言します。この変数の値は、形状の各頂点に設定された値の間で、フラグメントごとに補間されます。
2. `sampler2D` ユニフォーム変数を宣言します。このサンプラーは、補間されたテクスチャ座標とともにテクスチャ参照に使われ、スプライトにテクスチャを正しく適用します。スプライトなので、エンジンはこのサンプラーを、スプライトの *Image* プロパティに設定された画像に割り当てます。
3. マテリアルで `CONSTANT_TYPE_USER` 型の定数を定義し、`uniform` として宣言します。この値により、スプライトの色調を変えられます。デフォルトは純粋な白です。
4. 実行時のテクスチャはすべて乗算済みアルファを含んでいるため、色調を指定する色の値にもアルファ値をあらかじめ乗算します。
5. 補間された座標でテクスチャをサンプリングし、サンプリングした値を返します。
6. `gl_FragColor` には、フラグメントの出力色として、テクスチャの拡散色に色調の値を乗算した結果が設定されます。

得られたフラグメントの値は、その後テストを受けます。一般的なテストに*深度テスト*があり、フラグメントの深度値を、テスト対象のピクセルの深度バッファー値と比較します。テストの結果に応じて、フラグメントが破棄されるか、新しい値が深度バッファーに書き込まれます。このテストの一般的な用途は、カメラに近いグラフィックスで、その奥にあるグラフィックスを隠すことです。

テストの結果、フラグメントをフレームバッファーへ書き込むと判断された場合、バッファーにすでに存在するピクセルデータと*ブレンド*されます。レンダースクリプト（render script）で設定するブレンドのパラメーターにより、ソースの色（フラグメントシェーダーが書き込む値）とデスティネーションの色（フレームバッファー内の画像の色）を、さまざまな方法で組み合わせられます。ブレンドの一般的な用途は、透明なオブジェクトをレンダリングできるようにすることです。

## さらに学ぶには {#further-study}

- [Shadertoy](https://www.shadertoy.com) には、ユーザーが投稿した膨大な数のシェーダーがあります。さまざまなシェーディング技法を学べ、発想を得るための優れた情報源です。サイトで紹介されているシェーダーの多くは、わずかな作業で Defold に移植できます。[Shadertoy チュートリアル](https://www.defold.com/tutorials/shadertoy/)では、既存のシェーダーを Defold 用に変換する手順を説明しています。

- [カラーグレーディングのチュートリアル](https://www.defold.com/tutorials/grading/)では、カラーグレーディング用のカラールックアップテーブルのテクスチャを使い、フルスクリーンのカラーグレーディングエフェクトを作成する方法を説明しています。

- [The Book of Shaders](https://thebookofshaders.com/00/) では、シェーダーをプロジェクトで使い、組み込む方法を学び、パフォーマンスとグラフィックスの品質を向上させられます。
