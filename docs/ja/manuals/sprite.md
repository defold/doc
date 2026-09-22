---
title: 2D 画像の表示
brief: このマニュアルでは、スプライトコンポーネントを使って 2D 画像やアニメーションを表示する方法を説明します。
---

# スプライト {#sprites}

スプライト（sprite）は、単純な画像や、連続した画像を切り替えるフリップブックアニメーション（flipbook animation）を画面に表示するコンポーネント（component）です。

![スプライト](images/graphics/sprite.png)

スプライトコンポーネントのグラフィックスには、[アトラス（atlas）](/manuals/atlas) または [タイルソース（tile source）](/manuals/tilesource) を使用できます。

## スプライトのプロパティ {#sprite-properties}

*Id*、*Position*、*Rotation* の各プロパティに加えて、次のコンポーネント固有のプロパティがあります。

*Image*
: シェーダー（shader）にサンプラーが1つだけある場合、このフィールドの名前は `Image` になります。それ以外の場合、各スロットにはマテリアル（material）内のテクスチャサンプラーの名前が付きます。
各スロットには、そのテクスチャサンプラーでスプライトに使用するアトラスまたはタイルソースのリソースを指定します。

*Default Animation*
: スプライトに使用するアニメーションです。アニメーションの情報は、最初のアトラスまたはタイルソースから取得します。

*Material*
: スプライトの描画に使用するマテリアルです。

*Blend Mode*
: スプライトの描画に使用するブレンドモード（blend mode）です。

*Size Mode*
: `Automatic` に設定すると、エディターがスプライトのサイズを設定します。`Manual` に設定すると、自分でサイズを設定できます。

*Slice 9*
: スプライトのサイズ変更時に、テクスチャの縁の部分のピクセルサイズを保持するよう設定します。

:[Slice-9](../shared/slice-9-texturing.md)

### ブレンドモード {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## 実行時の操作 {#runtime-manipulation}

各種の関数やプロパティを使って、実行時にスプライトを操作できます（使い方は [API ドキュメント](/ref/sprite/) を参照してください）。次の関数があります。

* `sprite.play_flipbook()` - スプライトコンポーネントでアニメーションを再生します。
* `sprite.set_hflip()` と `sprite.set_vflip()` - スプライトのアニメーションの水平反転と垂直反転を設定します。

スプライトには、`go.get()` と `go.set()` を使って操作できる各種のプロパティもあります。

`cursor`
: 正規化されたアニメーションカーソルです（`number`）。

`image`
: スプライトの画像です（`hash`）。アトラスまたはタイルソースのリソースプロパティと `go.set()` を使って変更できます。例は [API リファレンス](/ref/sprite/#image) を参照してください。

`material`
: スプライトのマテリアルです（`hash`）。マテリアルのリソースプロパティと `go.set()` を使って変更できます。例は [API リファレンス](/ref/sprite/#material) を参照してください。

`playback_rate`
: アニメーションの再生速度です（`number`）。

`scale`
: スプライトの非均一なスケールです（`vector3`）。

`size`
: スプライトのサイズです（`vector3`）。スプライトの `Size Mode` が `Manual` に設定されている場合にのみ変更できます。

## マテリアル定数 {#material-constants}

{% include shared/material-constants.md component='sprite' variable='tint' %}

`tint`
: スプライトの色調です（`vector4`）。`vector4` を使って色調を表し、`x`、`y`、`z`、`w` がそれぞれ赤、緑、青、アルファ値の色調に対応します。

## マテリアルの属性 {#material-attributes}

スプライトでは、現在割り当てられているマテリアルの頂点属性（vertex attribute）をオーバーライドできます。これらの属性はコンポーネントから頂点シェーダーへ渡されます（詳しくは [マテリアルのマニュアル](/manuals/material/#attributes) を参照してください）。

マテリアルに指定された属性は、インスペクターに通常のプロパティとして表示され、個々のスプライトコンポーネントで設定できます。いずれかの属性をオーバーライドすると、オーバーライドされたプロパティとして表示され、ディスク上のスプライトファイルに保存されます。

![スプライトの属性](../images/graphics/sprite-attributes.png)

## プロジェクトの設定 {#project-configuration}

*game.project* ファイルには、スプライトに関する [プロジェクト設定](/manuals/project-settings#sprite) がいくつかあります。

## 複数のテクスチャを使用するスプライト {#multi-textured-sprites}

スプライトで複数のテクスチャを使用する場合は、いくつかの注意点があります。

### アニメーション {#animations}

現在、アニメーションデータ（fps、フレーム名）は最初のテクスチャから取得します。これを「基準となるアニメーション（driving animation）」と呼びます。

基準となるアニメーションの画像 ID を使って、別のテクスチャ内の画像を検索します。
そのため、テクスチャ間でフレーム ID が一致していることが重要です。

たとえば、`diffuse.atlas` に次のような `run` アニメーションがあるとします。

```
run:
    /main/images/hero_run_color_1.png
    /main/images/hero_run_color_2.png
    ...
```

この場合、フレーム ID は `run/hero_run_color_1` のようになりますが、たとえば次のような `normal.atlas` には見つからないでしょう。

```
run:
    /main/images/hero_run_normal_1.png
    /main/images/hero_run_normal_2.png
    ...
```

そこで、[アトラス](/manuals/material/) の `Rename patterns` を使って名前を変更します。
対応するアトラスにそれぞれ `_color=` と `_normal=` を設定すると、両方のアトラスでフレーム名が次のようになります。

```
run/hero_run_1
run/hero_run_2
...
```

### UV 座標 {#uvs}

UV 座標は最初のテクスチャから取得します。頂点の組は1つしかないため、2つ目以降のテクスチャの UV 座標がより多い場合や形状が異なる場合には、
適切な対応を保証できません。

これは重要な注意点です。画像の形状を十分に近いものにしてください。そうしないと、テクスチャのにじみが生じる可能性があります。

各テクスチャ内の画像の寸法は異なっていてもかまいません。
