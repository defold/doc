---
title: カラーグレーディングシェーダーのチュートリアル
brief: このチュートリアルでは、Defold で画面全体に適用するポストエフェクトを作成します。
---

# カラーグレーディングのチュートリアル {#grading-tutorial}

このチュートリアルでは、画面全体にカラーグレーディング（color grading）を適用するポストエフェクトを作成します。ここで使う基本的なレンダリング方法は、ぼかし、残像、グロー、色調整など、さまざまな種類のポストエフェクトに幅広く応用できます。

Defold エディターの操作に慣れており、GL シェーダー（shader）と Defold のレンダリングパイプライン（rendering pipeline）の基礎を理解していることを前提とします。これらについて学ぶ必要がある場合は、[シェーダーマニュアル](/manuals/shader/)と[レンダリングマニュアル](/manuals/render/)を参照してください。

## レンダーターゲット {#render-targets}

デフォルトのレンダースクリプト（render script）では、スプライト、タイルマップ、パーティクルエフェクト、GUI などの各表示コンポーネント（component）がグラフィックスカードの *フレームバッファー（frame buffer）* に直接描画されます。その後、ハードウェアがグラフィックスを画面に表示します。コンポーネントのピクセルを実際に描画するのは、GL の *シェーダープログラム（shader program）* です。Defold には、ピクセルデータを変更せずに画面へ描画するデフォルトのシェーダープログラムが、コンポーネントの種類ごとに付属しています。通常はこれが望ましい動作です。画像は、元々意図したとおりに画面に表示される必要があります。

コンポーネントのシェーダープログラムは、ピクセルデータを変更するものや、プログラムでまったく新しいピクセルの色を作り出すものに置き換えられます。その方法は [Shadertoy チュートリアル](/tutorials/shadertoy)で説明しています。

ここで、ゲーム全体を白黒で描画したいとします。考えられる方法の1つは、コンポーネントの種類ごとにシェーダープログラムを変更し、各シェーダーでピクセルの彩度を取り除くことです。現在、Defold には6つの組み込みマテリアル（material）と、頂点シェーダー（vertex shader）およびフラグメントシェーダー（fragment shader）のプログラムの組が6組付属しているため、かなりの作業が必要になります。さらに、その後の変更やエフェクトの追加も、各シェーダープログラムに対して行う必要があります。

代わりに、レンダリングを次の2つのステップに分けると、はるかに柔軟に対応できます。

![レンダーターゲット](images/grading/render_target.png)

1. すべてのコンポーネントを通常どおり描画します。ただし、通常のフレームバッファーの代わりに、オフスクリーンバッファーに描画します。これは、*レンダーターゲット（render target）* と呼ばれるものに描画することで実現します。
2. 正方形のポリゴンをフレームバッファーに描画し、レンダーターゲットに保存されたピクセルデータを、そのポリゴンのテクスチャ（texture）のソースとして使用します。また、正方形のポリゴンが画面全体を覆うように引き伸ばします。

この方法では、描画結果のデータを読み取り、画面に表示される前に変更できます。上記のステップ2にシェーダープログラムを追加すれば、画面全体のエフェクトを簡単に実現できます。Defold での設定方法を見ていきましょう。

## カスタムレンダラーの設定 {#setting-up-a-custom-renderer}

組み込みレンダースクリプトを変更して、新しいレンダリング機能を追加する必要があります。デフォルトのレンダースクリプトは出発点として適しているので、まずコピーします。

1. */builtins/render/default.render_script* をコピーします。*Asset* ビューで *default.render_script* を右クリックし、<kbd>Copy</kbd> を選択します。次に *main* を右クリックし、<kbd>Paste</kbd> を選択します。コピーを右クリックして <kbd>Rename...</kbd> を選択し、「grade.render_script」などの適切な名前を付けます。
2. *Asset* ビューで *main* を右クリックし、<kbd>New ▸ Render</kbd> を選択して、*/main/grade.render* という新しいレンダーファイルを作成します。
3. *grade.render* を開き、*Script* プロパティを「/main/grade.render_script」に設定します。

   ![grade.render](images/grading/grade_render.png)

4. *game.project* を開き、*Render* を「/main/grade.render」に設定します。

   ![game.project](images/grading/game_project.png)

これで、変更可能な新しいレンダリングパイプラインでゲームが実行されるようになりました。エンジンがコピーしたレンダースクリプトを使用しているか確認するには、ゲームを実行し、見た目に変化が出るようにレンダースクリプトを変更してから、スクリプトを再読み込みします。たとえば、タイルとスプライトの描画を無効にしてから <kbd>⌘ + R</kbd> を押すと、この「壊した」レンダースクリプトを実行中のゲームにホットリロードできます。

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. すべてのスプライトとタイルを含む「tile」述語の描画をコメントアウトします。このコード行は、レンダースクリプトファイルの33行目前後にあります。

この簡単なテストでスプライトとタイルが消えれば、ゲームがこのレンダースクリプトを実行していることを確認できます。すべてが期待どおりに動作したら、レンダースクリプトへの変更を元に戻せます。

## オフスクリーンターゲットへの描画 {#drawing-to-an-off-screen-target}

次に、フレームバッファーの代わりにオフスクリーンのレンダーターゲットに描画するよう、レンダースクリプトを変更します。まず、レンダーターゲットを作成する必要があります。

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 1)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 1)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. レンダーターゲットのカラーバッファーのパラメーターを設定します。ゲームの目標解像度を使用します。
2. カラーバッファーのパラメーターを使ってレンダーターゲットを作成します。

あとは、元のレンダリングコードを次のように `render.set_render_target()` で挟みます。

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. レンダーターゲットを有効にします。これ以降、`render.draw()` を呼び出すたびに、オフスクリーンのレンダーターゲットのバッファーに描画されます。
2. `update()` 内の元の描画コードはすべてそのままにします。ただし、ビューポートはレンダーターゲットの解像度に設定します。
3. この時点で、ゲームのグラフィックスはすべてレンダーターゲットに描画されています。デフォルトのレンダーターゲットに設定して、オフスクリーンのレンダーターゲットを無効にします。

必要な作業はこれだけです。ここでゲームを実行すると、すべてがレンダーターゲットに描画されます。ただし、フレームバッファーには何も描画していないため、画面は黒一色になります。

## 画面を埋めるものを用意する {#something-to-fill-the-screen-with}

レンダーターゲットのカラーバッファーにあるピクセルを画面に描画するには、そのピクセルデータをテクスチャとして適用できるものを用意する必要があります。そのために、平らな正方形の3D モデルを使用します。

1. *`main.collection`* を開き、「`grade`」という新しいゲームオブジェクト（game object）を作成します。
2. 「`grade`」ゲームオブジェクトに Model コンポーネントを追加します。
3. モデルコンポーネントの *Mesh* プロパティを、`builtins/assets/meshes` にある *`quad.gltf`* ファイルに設定します。

ゲームオブジェクトは拡大縮小せず、原点に置いたままにします。後でこのクワッドを描画する際、画面全体を埋めるように投影します。まずは、クワッド用のマテリアルとシェーダープログラムを用意する必要があります。

1. *Asset* ビューで *main* を右クリックし、<kbd>New ▸ Material</kbd> を選択して、新しいマテリアルを作成します。名前を *`grade.material`* にします。
2. *Asset* ビューで *main* を右クリックし、<kbd>New ▸ Vertex program</kbd> と <kbd>New ▸ Fragment program</kbd> を選択して、*`grade.vp`* という頂点シェーダープログラムと、*`grade.fp`* というフラグメントシェーダープログラムを作成します。
3. *grade.material* を開き、*Vertex program* と *Fragment program* の各プロパティを、新しいシェーダープログラムのファイルに設定します。
4. 型が `CONSTANT_TYPE_VIEWPROJ` で、名前が「`view_proj`」の *Vertex constant* を追加します。これは、クワッドの頂点を処理する頂点プログラムで使用するビュー行列と投影行列です。
5. 「`original`」という *Sampler* を追加します。これは、オフスクリーンのレンダーターゲットのカラーバッファーからピクセルをサンプリングするために使用します。
6. 「`grade`」という *Tag* を追加します。クワッドを描画するため、レンダースクリプトに、このタグに一致する新しい *レンダー述語（render predicate）* を作成します。

   ![grade.material](images/grading/grade_material.png)

7. *`main.collection`* を開き、ゲームオブジェクト「`grade`」のモデルコンポーネントを選択して、*Material* プロパティを「`/main/grade.material`」に設定します。

   ![モデルのプロパティ](images/grading/model_properties.png)

8. 頂点シェーダープログラムは、基本テンプレートから作成したままにできます。

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. フラグメントシェーダープログラムでは、サンプリングした色の値をそのまま `gl_FragColor` に設定する代わりに、簡単な色の操作を行います。主な目的は、ここまでの処理がすべて期待どおりに動作することを確認することです。

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturate the color sampled from the original texture
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

これで、マテリアルとシェーダーを備えたクワッドモデルが用意できました。あとは、画面のフレームバッファーに描画するだけです。

## オフスクリーンバッファーをテクスチャとして使う {#texturing-with-the-off-screen-buffer}

クワッドモデルを描画できるよう、レンダースクリプトにレンダー述語を追加する必要があります。*`grade.render_script`* を開き、`init()` 関数を編集します。

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. *`grade.material`* で設定した「grade」タグに一致する新しい述語を追加します。

`update()` でレンダーターゲットのカラーバッファーへの描画を終えたら、クワッドモデルが画面全体を埋めるよう、ビューと投影を設定します。その後、レンダーターゲットのカラーバッファーをクワッドのテクスチャとして使用します。

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. フレームバッファーをクリアします。それまでの `render.clear()` の呼び出しが作用するのは、画面のフレームバッファーではなく、レンダーターゲットであることに注意してください。
2. ビューポートをウィンドウサイズに合わせます。
3. ビューを単位行列に設定します。これは、カメラが原点にあり、Z 軸に沿ってまっすぐ向いていることを意味します。投影も単位行列に設定して、クワッドが画面全体に平らに投影されるようにします。
4. テクスチャスロット0をレンダーターゲットのカラーバッファーに設定します。*`grade.material`* ではサンプラー（sampler）「original」がスロット0にあるため、フラグメントシェーダーはレンダーターゲットからサンプリングします。
5. 「grade」タグを持つすべてのマテリアルに一致するように作成した述語で描画します。クワッドモデルは、このタグが設定されている *`grade.material`* を使用しているため、クワッドが描画されます。
6. 描画が終わったら、テクスチャスロット0はもう使わないので無効にします。

ゲームを実行して、結果を見てみましょう。

![彩度を取り除いたゲーム](images/grading/desaturated_game.png)

## カラーグレーディング {#color-grading}

色は3つの成分値で表され、それぞれの成分が、その色に含まれる赤、緑、青の量を決めます。黒から、赤、緑、青、黄、ピンクを経て白に至るすべての色は、立方体の形に収められます。

![カラーキューブ](images/grading/color_cube.png)

画面に表示できる色はすべて、このカラーキューブの中にあります。カラーグレーディングの基本的な考え方は、このようなカラーキューブの色を変更し、3D の *ルックアップテーブル（lookup table）* として使用することです。

各ピクセルについて、次の処理を行います。

1. カラーキューブ内で、そのピクセルの色の位置を調べます（赤、緑、青の値に基づきます）。
2. グレーディングしたキューブのその位置に、どの色が保存されているかを *読み取ります*。
3. 元の色の代わりに、読み取った色でピクセルを描画します。

フラグメントシェーダーでは、次のように実行できます。

1. オフスクリーンバッファー内の各ピクセルの色の値をサンプリングします。
2. カラーグレーディング済みのカラーキューブで、サンプリングしたピクセルの色の位置を調べます。
3. 出力するフラグメントの色を、調べて得られた値に設定します。

![レンダーターゲットへのカラーグレーディング](images/grading/render_target_grading.png)

## ルックアップテーブルの表現 {#representing-the-lookup-table}

Open GL ES 2.0 は3D テクスチャをサポートしていないため、3D のカラーキューブを別の方法で表現する必要があります。一般的な方法は、Z 軸（青）に沿ってキューブをスライスし、各スライスを2次元のグリッドに横並びで配置することです。16枚のスライスには、それぞれ16⨉16ピクセルのグリッドが含まれます。これをテクスチャに保存し、フラグメントシェーダー内でサンプラーを使って読み取れるようにします。

![ルックアップテクスチャ](images/grading/lut.png)

こうしてできるテクスチャには16個のセルがあり、青の各強度に1つずつ対応します。各セル内には、X 軸に沿って16段階の赤、Y 軸に沿って16段階の緑が並びます。このテクスチャは、1600万色からなる RGB 色空間全体を、わずか4096色、色深度にしてわずか4ビットで表します。ほとんどの基準では低品質ですが、GL グラフィックスハードウェアの機能により、非常に高い色精度を取り戻せます。その方法を見ていきましょう。

## 色の参照 {#looking-up-colors}

色を参照するには、青成分を確認し、どのセルから赤と緑の値を取得するかを判断します。適切な赤と緑の色の組を含むセルを求める式は、次のとおりです。

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

ここで `B` は0から1の間の青成分の値で、`N` はセルの総数です。この例ではセル番号の範囲は `0`--`15` になります。セル `0` には青成分が `0` の色がすべて含まれ、セル `15` には青成分が `1` の色がすべて含まれます。

たとえば、RGB 値 `(0.63, 0.83, 0.4)` は、青の値が `0.4` の色をすべて含むセル、つまりセル番号6にあります。これが分かれば、緑と赤の値に基づいて最終的なテクスチャ座標を求めるのは簡単です。

![ルックアップテーブル](images/grading/lut_lookup.png)

赤と緑の値 `(0, 0)` は左下のピクセルの *中心* にあり、値 `(1.0, 1.0)` は右上のピクセルの *中心* にあるものとして扱う必要があることに注意してください。

::: sidenote
左下のピクセルの中心から右上のピクセルの中心までの範囲で読み取るのは、現在のセルの外にあるピクセルが、サンプリングした値に影響しないようにするためです。フィルタリングについては、以下を参照してください。
:::

テクスチャ上のこの座標でサンプリングすると、ちょうど4つのピクセルの間になります。では、GL はその点の色として、どの値を返すのでしょうか？

![ルックアップテーブルのフィルタリング](images/grading/lut_filtering.png)

答えは、マテリアルでサンプラーの *フィルタリング* をどのように指定したかによって決まります。

- サンプラーのフィルタリングが `NEAREST` の場合、GL は最も近いピクセルの色の値を返します（位置の値を切り捨てます）。上の例では、GL は位置 `(0.60, 0.80)` の色の値を返します。この4ビットのルックアップテクスチャでは、色の値が合計わずか4096色に量子化されることになります。

- サンプラーのフィルタリングが `LINEAR` の場合、GL は *補間された* 色の値を返します。GL は、サンプリング位置から周囲のピクセルまでの距離に基づいて色を混ぜます。上の例では、サンプリング点を囲む4つのピクセルの色をそれぞれ25%ずつ混ぜた色を返します。

このように、線形フィルタリングを使用すると色の量子化をなくし、かなり小さいルックアップテーブルから非常に高い色精度を得られます。

## 参照処理の実装 {#implementing-the-lookup}

フラグメントシェーダーに、テクスチャを参照する処理を実装しましょう。

1. *`grade.material`* を開きます。
2. 「`lut`」（ルックアップテーブルを意味します）という2つ目のサンプラーを追加します。
3. *`Filter min`* プロパティを `FILTER_MODE_MIN_LINEAR` に、*`Filter mag`* プロパティを `FILTER_MODE_MAG_LINEAR` に設定します。

    ![ルックアップテーブルのサンプラー](images/grading/material_lut_sampler.png)

4. 次のルックアップテーブルのテクスチャ（*`lut16.png`*）をダウンロードし、プロジェクトに追加します。

    ![16色のルックアップテーブル](images/grading/lut16.png)

5. *`main.collection`* を開き、*`lut`* テクスチャプロパティを、ダウンロードしたルックアップテクスチャに設定します。

    ![クワッドモデルのルックアップテーブル](images/grading/quad_lut.png)

6. 最後に *`grade.fp`* を開き、色を参照する処理を追加します。

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. サンプラー `lut` を宣言します。
    2. 色の最大値（0から始めるので15）、チャンネルごとの色数、ルックアップテクスチャの幅と高さを定数として定義します。
    3. 元のテクスチャ（オフスクリーンのレンダーターゲットのカラーバッファー）から、ピクセルの色（`px` と呼びます）をサンプリングします。
    4. `px` の青チャンネルの値に基づいて、色を読み取るセルを計算します。
    5. ピクセルの中心から読み取るように、半ピクセル分のオフセットを計算します。
    6. `px` の赤と緑の値に基づいて、テクスチャ上の X と Y のオフセットを計算します。
    7. ルックアップテクスチャ上の最終的なサンプリング位置を計算します。
    8. ルックアップテクスチャから結果の色をサンプリングします。
    9. クワッドのテクスチャの色を、得られた色に設定します。

現時点では、ルックアップテーブルのテクスチャは、参照した値と同じ色の値を返すだけです。そのため、ゲームは元の色で描画されるはずです。

![ゲームワールドの元の外観](images/grading/world_original.png)

ここまではすべて正しくできているように見えますが、表面には見えない問題が潜んでいます。グラデーションのテスト用テクスチャを使ったスプライトを追加するとどうなるか、見てみましょう。

![青のバンディング](images/grading/blue_banding.png)

青のグラデーションに、ひどく目立つ帯状の段差（バンディング）が現れています。なぜでしょうか？

## 青チャンネルの補間 {#interpolating-the-blue-channel}

青チャンネルにバンディングが生じるのは、GL がテクスチャから色を読み取る際に、青チャンネルの補間をまったく行えないためです。青の値に基づいて読み取るセルをあらかじめ選び、それ以上は何もしていません。たとえば、青チャンネルの値が `0.400`--`0.466` の範囲にある場合、その範囲内のどの値であっても、最終的な色は必ず青チャンネルが `0.400` のセル番号6からサンプリングされます。

青チャンネルの解像度を上げるには、補間を自分で実装できます。青の値が隣接する2つのセルの値の間にあれば、両方のセルからサンプリングして色を混ぜられます。たとえば青の値が `0.420` なら、セル番号6 *と* セル番号7からサンプリングし、その色を混ぜるようにします。

つまり、次の2つのセルから読み取ります。

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

もう一方は、次の式で求めます。

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

次に、各セルから色の値をサンプリングし、次の式に従って色を線形補間します。

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

ここで `color`~low~ は値が小さい側（左端）のセルからサンプリングした色で、`color`~high~ は値が大きい側（右端）のセルからサンプリングした色です。GLSL の `mix()` 関数が、この線形補間を行います。

上記の値 `C~frac~` は、青チャンネルの値を `0`--`15` の色の範囲にスケーリングしたときの小数部分です。

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

値の小数部分を取得する GLSL 関数もあり、`frac()` という名前です。フラグメントシェーダー（*`grade.fp`*）の最終的な実装は、次のようにシンプルです。

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. 読み取る隣接した2つのセルを計算します。
2. 各セルに1つずつ、2つの参照位置を個別に計算します。
3. それぞれのセルの位置から、2つの色をサンプリングします。
3. スケーリングした青の値である `cell` の小数部分に応じて、色を線形に混ぜます。

テスト用テクスチャを使ってゲームをもう一度実行すると、はるかに良い結果になります。青チャンネルのバンディングはなくなっています。

![バンディングのない青](images/grading/blue_no_banding.png)

## ルックアップテクスチャのグレーディング {#grading-the-lookup-texture}

元のゲームワールドとまったく同じ見た目で描画するために、ずいぶん手間をかけました。しかし、この仕組みがあれば、とても面白いことができます。ここからが本番です！

1. エフェクトを適用していない状態のゲームのスクリーンショットを撮ります。
2. 好みの画像編集ソフトでスクリーンショットを開きます。
3. 色の調整（明るさ、コントラスト、トーンカーブ、ホワイトバランス、露出など）を好きなだけ適用します。

![Affinity で表示したゲームワールド](images/grading/world_graded_affinity.png)

4. ルックアップテーブルのテクスチャファイル（*`lut16.png`*）にも、同じ色の調整を適用します。
5. 色を調整したルックアップテーブルのテクスチャファイルを保存します。
6. Defold プロジェクトで使用しているテクスチャ *`lut16.png`* を、色を調整したものに置き換えます。
7. ゲームを実行します！

![グレーディングしたゲームワールド](images/grading/world_graded.png)

やりました！
