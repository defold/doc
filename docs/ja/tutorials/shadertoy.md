---
brief: このチュートリアルでは、shadertoy.com のシェーダーを Defold 用に変換します。
layout: tutorial
locale: ja
title: Shadertoy から Defold への変換チュートリアル
---

# Shadertoy チュートリアル {#shadertoy-tutorial}

[Shadertoy.com](https://www.shadertoy.com/) は、ユーザーが投稿した GL シェーダー（shader）を集めたサイトです。シェーダーコードやアイデアを探すのに役立ちます。このチュートリアルでは、Shadertoy のシェーダーを Defold で動作させます。シェーダーに関する基本的な知識があることを前提としています。予備知識が必要な場合は、[シェーダーマニュアル](/manuals/shader/) から読み始めるとよいでしょう。

使用するシェーダーは、Pablo Andrioli 氏（Shadertoy でのユーザー名は「Kali」）の [Star Nest](https://www.shadertoy.com/view/XlfGRj) です。数学の魔法のような手続き的な計算だけで、見事な星々のエフェクトを描画するフラグメントシェーダー（fragment shader）です。

![Star Nest](../images/shadertoy/starnest.png)

このシェーダーは、わずか65行のかなり複雑な GLSL コードで構成されていますが、心配はいりません。いくつかの単純な入力に応じて処理するブラックボックスとして扱います。ここでの作業は、Shadertoy の代わりに Defold と連携するようシェーダーを変更することです。

## テクスチャを付ける対象 {#something-to-texture}

Star Nest シェーダーはフラグメントシェーダーだけで構成されているので、シェーダーでテクスチャ（texture）を付ける対象さえあれば十分です。スプライト（sprite）、タイルマップ（tilemap）、GUI、モデル（model）など、いくつかの選択肢があります。このチュートリアルでは単純な 3D モデルを使用します。モデルの描画を簡単にフルスクリーンのエフェクトにできるためです。たとえば、画面にポストプロセスを適用する場合には、このような描画が必要になります。

空のプロジェクトから始められます。

1. Defold を開き、Create From の *Templates* を選択します。
2. *Empty Project* を選択します。
3. *Title* を設定し、ディスク上の *Location* を選択します。
4. <kbd>Create New Project</kbd> をクリックします。

![開始](../images/shadertoy/empty_project.png)

`builtins/assets/meshes` にある組み込みの `quad.gltf` メッシュ（mesh）を使用できます。

必要に応じて、Blender などの 3D モデリングソフトで正方形の平面メッシュを作成することもできます。扱いやすいように、4つの頂点の座標は X 軸の -1 と 1、Y 軸の -1 と 1 に配置します。Blender ではデフォルトで Z 軸が上を向くので、メッシュを X 軸の周りに90°回転させる必要があります。また、メッシュの UV 座標が正しく生成されていることも確認してください。Blender でメッシュを選択した状態で *Edit Mode* に入り、<kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd> を選択します。

<div class='sidenote' markdown='1'>
Blender は無料のオープンソース 3D ソフトウェアで、[blender.org](https://www.blender.org) からダウンロードできます。
</div>

![Blender の四角形](../images/shadertoy/quad_blender.png)

1. Defold で「main.collection」ファイルを開き、「star-nest」という新しいゲームオブジェクト（game object）を作成します。
2. 「star-nest」ゲームオブジェクトに *Model* コンポーネント（component）を追加します。
3. *Mesh* プロパティに、用意した `quad.gltf` を設定します。
4. モデルのマテリアル（material）を設定する必要があるので、ここでは組み込みの `model.material` を選択します。

シーンエディターにモデルが表示されますが、全体が黒く描画されます。これは、まだテクスチャが設定されていないためです。

![Defold の四角形](../images/shadertoy/quad_default_material.png)

## マテリアルの作成 {#creating-the-material}

1. `Assets` ペインの `main` フォルダーを <kbd>右クリック</kbd> し、<kbd>New</kbd>-><kbd>Material</kbd> を選択して `star-nest` と名付け、新しいマテリアルファイル *`star-nest.material`* を作成します。

 ![マテリアル](../images/shadertoy/new_material.png)

2. 同じように、頂点シェーダー（vertex shader）プログラム `star-nest.vp` とフラグメントシェーダープログラム `star-nest.fp` を作成します。
3. *star-nest.material* を開きます。
4. *Vertex Program* に `star-nest.vp` を設定します。
5. *Fragment Program* に `star-nest.fp` を設定します。
6. *Vertex Constant* を追加して「`view_proj`」と名付け、型を `Viewproj`（「ビュー投影」の意味）にします。
8. *Tags* に「tile」というタグを追加します。これにより、スプライトとタイルを描画する際のレンダーパスに四角形が含まれます。

 ![マテリアル](../images/shadertoy/material.png)

### 頂点プログラム {#vertex-program}

1. 頂点シェーダープログラムのファイル `star-nest.vp` を開きます。次のコードが含まれているはずです。

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

### フラグメントプログラム {#fragment-program}

1. フラグメントシェーダープログラムのファイル `star-nest.fp` を開き、UV 座標（`var_texcoord0`）の X 座標と Y 座標に基づいてフラグメントの色を設定するようコードを変更します。これにより、モデルが正しく設定されていることを確認します。

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. `main.collection` の `star-nest` ゲームオブジェクトにあるモデルコンポーネントの `Material` プロパティを、作成したばかりの `star-nest` マテリアルに設定します。

これでエディターは新しいシェーダーでモデルを描画するので、UV 座標が正しいかどうかを明確に確認できます。左下の角は黒 (0, 0, 0)、左上の角は緑 (0, 1, 0)、右上の角は黄 (1, 1, 0)、右下の角は赤 (1, 0, 0) になるはずです。

![Defold の四角形](../images/shadertoy/quad_material.png)

## カメラ {#camera}

これでプロジェクトを実行できます（<kbd>Project</kbd>-><kbd>Build</kbd>、またはショートカットの <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd>）。しかし、黒い画面が表示されます（左下の角に小さな1ピクセルが見えるかもしれませんが、ほぼ真っ黒です）。これはカメラ（camera）がなく、デフォルトのレンダースクリプト（render script）が単純なフォールバックとして広大な 2D 空間を表示する一方、モデルは位置 (0,0,0) にあり、幅がわずか1しかないためです。

カメラコンポーネントを持つゲームオブジェクトを追加し、ゲームで見える範囲を定めます。

1. `camera` という名前のゲームオブジェクトを位置 (0,0,1) に追加します。（デフォルトの 2D 設定では Z 軸が手前を向いているので、このゲームオブジェクトがモデルの手前に来るよう、Z 座標を1に設定することが重要です）。
2. `Camera` コンポーネントを追加すると、四角形が映ったカメラのプレビューが表示されます。この構成では幸い、デフォルトのプロパティを変更しなくても正しい結果が見えるはずです。ただし、カメラの視錐台をそこまで大きくする必要はないので、`Far Z` を `2` に減らせます。

![カメラ](../images/shadertoy/camera.png)

必要に応じて、`Orthographic Projection` を `true` に設定してカメラの種類を変更し、`Orthographic Zoom` も600程度に調整できます。ただし、この場合はアスペクト比が自動で調整されないため、モデルが画面全体を埋めることはありません。

## Star Nest シェーダー {#the-star-nest-shader}

準備が整ったので、実際のシェーダーコードに取りかかります。まず、元のコードを見てみましょう。いくつかの部分で構成されています。

![Star Nest シェーダーのコード](../images/shadertoy/starnest_code.png)

GLSL バージョン140を使用する新しいパイプラインを使います。そのため、ファイルの先頭で `#version 140` によりバージョンを宣言します。

1. 5--18行目では、いくつかの定数を定義しています。これらはそのままでかまいません。通常の GLSL 定数であり、Shadertoy や Defold に特有のものではないためです。

2. 21行目と63行目には、入力フラグメントのスクリーン空間における X、Y テクスチャ座標（`in vec2 fragCoord`）と、出力フラグメントの色（`out vec4 fragColor`）があります。

    Defold は、補間される変数を通じて、テクスチャ座標を頂点シェーダーからフラグメントシェーダーへ UV 座標（0--1の範囲）として渡します。今回の頂点シェーダーでは、これを `out` 修飾子で宣言しています。

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     フラグメントシェーダーでは、同じ値を `in` 修飾子で受け取ります。

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    次に、GLSL 140 では、`out` 修飾子を使ってフラグメント出力を明示的に宣言します。

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    つまり、元の Shadertoy コードが `fragColor` に書き込むところを、Defold のシェーダーでは `out_fragColor` に書き込みます。

3. 23--27行目では、テクスチャの寸法、移動方向、スケールを適用した時間を設定しています。Shadertoy では、シェーダーは `fragCoord` を通じてピクセル位置を受け取り、ビューポートまたはテクスチャの解像度は `uniform vec3 iResolution` として渡されます。シェーダーは、フラグメント座標と解像度から、正しいアスペクト比を持つ UV 形式の座標を計算します。見栄えのよい構図にするために、解像度に基づくオフセットも適用します。

    Defold ではピクセル座標から計算を始めません。代わりに、頂点シェーダーから `var_texcoord0` を通じて正規化された UV 座標を受け取っています。この座標は、描画する四角形全体で `0.0` から `1.0` の範囲になります。

    Defold 版では、`var_texcoord0` の UV 座標を使うようにこれらの計算を変更する必要があります。
    一般的な変換は次のようになります。

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    `aspect` の具体的な値は、サンプルの構成によって異なります。既知の画面サイズでフルスクリーンの四角形にエフェクトを描画する場合は、このチュートリアルではアスペクト比を固定値としてコードに記述できます。任意のウィンドウサイズに対応する必要がある場合は、解像度をフラグメント定数として渡し、GLSL 140 のユニフォーム（uniform）ブロック内に配置します。

    ここでは時間も設定します。時間は `uniform float iGlobalTime` としてシェーダーに渡されます。Defold は1.12.3以降、特別な `Time` 定数を通じてシェーダーに時間を提供しているので、これを使用します。

    現在の Defold では、不透明型以外のユニフォームをユニフォームブロック内で宣言します。
    フラグメントシェーダーでは、次のように宣言します。

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    次に、`star-nest.material` に `time` という名前の Fragment Constant を追加し、型を `Time` に設定します。

    すると、その値を次のように使用できます。

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    ここで、`time.x` はエンジン起動からの時間、`time.y` は前フレームからの経過時間です。

4. 29--39行目では、ボリュームレンダリングの回転を設定し、マウス位置が回転に影響するようにしています。マウス座標は `uniform vec4 iMouse` としてシェーダーに渡されます。

    このチュートリアルではマウス入力を省略します。

5. 41--62行目がシェーダーの中心部分です。このコードはそのままにしておけます。

## 変更後の Star Nest シェーダー {#the-modified-star-nest-shader}

上記の各部分に必要な変更を加えると、次のシェーダーコードになります。読みやすくするために少し整理しています。Defold 版と Shadertoy 版の違いに注釈を付けています。

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

1. Defold の新しい GLSL パイプラインを使うため、ファイルの先頭で #version 140 を宣言します。続く定義はそのまま残します。
2. 頂点シェーダーは var_texcoord0 を通じてフラグメントシェーダーに UV 座標を渡します。GLSL 140 では、フラグメントシェーダーは in 修飾子でこの補間された値を受け取ります。
3. GLSL 140 では、フラグメントシェーダーは gl_FragColor に書き込むのではなく、出力変数を明示的に宣言する必要があります。ここでは out vec4 out_fragColor を使用します。
4. Defold の Time マテリアル定数は、ユニフォームブロックを通じてシェーダーに公開されます。star-nest.material に time という名前の Fragment Constant を追加し、型を Time に設定します。
5. Shadertoy は mainImage(out vec4 fragColor, in vec2 fragCoord) を使用します。Defold では通常の void main() エントリーポイントを使用し、var_texcoord0 から補間された UV 座標を読み取り、最終的な色を out_fragColor に書き込みます。
6. このチュートリアルでは、描画用の解像度とアスペクト比を固定値として定義します。現在のモデルは正方形なので、vec2 res = vec2(1.0, 1.0); を使用できます。サイズが1280×720の長方形モデルの場合は、代わりに vec2 res = vec2(1.78, 1.0); を使用し、その値を UV 座標に乗算することで正しいアスペクト比を保てます。
7. 元の Shadertoy シェーダーは iGlobalTime を使用します。この Defold 版では、time.x にエンジン起動からの時間が格納されているので、これをローカル変数 iGlobalTime に代入し、星々の中を移動するカメラのアニメーションに使用します。
8. このチュートリアルを単純にするために、iMouse の値をすべて取り除きます。ボリュームレンダリングにおける見た目の対称性を抑えるため、回転そのものは残します。
9. 最後に、シェーダーは得られたフラグメントの色を out_fragColor に書き込みます。

フラグメントシェーダープログラムを保存します。これでシーンエディターでも実行時でも、モデルに星々のテクスチャが美しく描画されるはずです。

![Star Nest を描画した四角形](../images/shadertoy/quad_starnest.png)


## アニメーション {#animation}

最後の仕上げは、時間を導入して星々を動かすことです。Defold は1.12.3以降、`Time` 型のフラグメント定数を通じて、この時間を自動的に提供します。

1. *star-nest.material* を開きます。
2. *Fragment Constant* を追加し、「time」と名付けます。
3. *Type* を `Time` に設定します。

![時間の定数](../images/shadertoy/time_constant.png)

これだけです！フラグメントシェーダーでは、この `time` をすでに処理しています。これで完成です！

## 演習 {#exercises}

続きの楽しい演習として、元のマウス移動入力をシェーダーに追加してみましょう。新しい Fragment Constant を作成し、今回は型を `User` にする必要があります。マウスの移動を検出するスクリプトの `on_input` 内で、`go.set()` 関数を使って新しい定数に入力座標を設定し、更新します。

Defold を楽しんでください！
