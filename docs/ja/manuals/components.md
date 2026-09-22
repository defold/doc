---
title: ゲームオブジェクトのコンポーネント
brief: このマニュアルでは、コンポーネントの概要と使い方を説明します。
---

#  コンポーネント {#components}

:[components](../shared/components.md)

## コンポーネントの種類 {#component-types}

Defold は、以下の種類のコンポーネント（component）をサポートしています。

* [コレクションファクトリー（collection factory）](/manuals/collection-factory) - コレクション（collection）を生成します
* [コレクションプロキシ（collection proxy）](/manuals/collection-proxy) - コレクションを読み込み、アンロードします
* [コリジョンオブジェクト（collision object）](/manuals/physics) - 2D および 3D の物理演算
* [カメラ（camera）](/manuals/camera) - ゲームワールドのビューポートと投影を変更します
* [ファクトリー（factory）](/manuals/factory) - ゲームオブジェクト（game object）を生成します
* [GUI](/manuals/gui) - グラフィカルユーザーインターフェースを描画します
* [ラベル（label）](/manuals/label) - テキストを描画します
* [ライト（light）](/manuals/light) - シェーダー用のライトデータを追加します
* [メッシュ（mesh）](/manuals/mesh) 3D メッシュを表示します（実行時の作成と操作に対応）
* [モデル（model）](/manuals/model) 3D モデルを表示します（アニメーションは任意）
* [パーティクルエフェクト（Particle FX）](/manuals/particlefx) -  パーティクルを生成します
* [スクリプト（script）](/manuals/script) - ゲームのロジックを追加します
* [サウンド（sound）](/manuals/sound) - 音声や音楽を再生します
* [スプライト（sprite）](/manuals/sprite) - 2D 画像を表示します（フリップブックアニメーションは任意）
* [タイルマップ（tilemap）](/manuals/tilemap) - タイルを格子状に配置して表示します

拡張機能を使用して、さらにコンポーネントを追加できます。

* [Rive モデル](/extension-rive) - Rive アニメーションを描画します
* [Spine モデル](/extension-spine) - Spine アニメーションを描画します


## コンポーネントの有効化と無効化 {#enabling-and-disabling-components}

ゲームオブジェクトのコンポーネントは、そのゲームオブジェクトの作成時に有効になります。コンポーネントを無効にするには、そのコンポーネントに [`disable`](/ref/go/#disable) メッセージを送信します。

```lua
-- disable the component with id 'weapon' on the same game object as this script
msg.post("#weapon", "disable")

-- disable the component with id 'shield' on the 'enemy' game object
msg.post("enemy#shield", "disable")

-- disable all components on the current game object
msg.post(".", "disable")

-- disable all components on the 'enemy' game object
msg.post("enemy", "disable")
```

コンポーネントを再び有効にするには、そのコンポーネントに [`enable`](/ref/go/#enable) メッセージを送信します。

```lua
-- enable the component with id 'weapon'
msg.post("#weapon", "enable")
```

## コンポーネントのプロパティ {#component-properties}

Defold のコンポーネントは、種類ごとに異なるプロパティを持っています。エディターの [Properties ペイン](/manuals/editor/#the-editor-views) には、[Outline ペイン](/manuals/editor/#the-editor-views) で現在選択しているコンポーネントのプロパティが表示されます。使用できるコンポーネントのプロパティについて詳しくは、各種類のコンポーネントのマニュアルを参照してください。

## コンポーネントの位置、回転、スケール {#component-position-rotation-and-scale}

表示用のコンポーネントには、通常、位置と回転のプロパティがあり、多くの場合はスケールのプロパティもあります。これらのプロパティはエディターから変更できますが、ほとんどの場合、実行時には変更できません（唯一の例外はスプライトとラベルのコンポーネントのスケールで、実行時に変更できます）。

コンポーネントの位置、回転、スケールを実行時に変更する必要がある場合は、そのコンポーネントが属するゲームオブジェクトの位置、回転、スケールを変更します。その結果、ゲームオブジェクト上のすべてのコンポーネントに影響が及びます。ゲームオブジェクトにアタッチされている複数のコンポーネントのうち、1つだけを操作したい場合は、対象のコンポーネントを別のゲームオブジェクトに移動し、そのゲームオブジェクトを、コンポーネントが元々属していたゲームオブジェクトの子として追加することをお勧めします。

## コンポーネントの描画順序 {#component-draw-order}

表示用のコンポーネントの描画順序は、次の2つによって決まります。

### レンダースクリプトの述語 {#render-script-predicates}
各コンポーネントには[マテリアル（material）](/manuals/material/)が割り当てられ、各マテリアルには1つ以上のタグがあります。一方、レンダースクリプト（render script）では、1つ以上のマテリアルタグにそれぞれ一致する、いくつかのレンダー述語（render predicate）を定義します。レンダースクリプトの *update()* 関数では、[述語を1つずつ描画し](/manuals/render/#render-predicates)、各述語で定義されているタグに一致するコンポーネントを描画します。デフォルトのレンダースクリプトは、まず1つのパスでスプライトとタイルマップを描画し、次に別のパスでパーティクルエフェクトを描画します。どちらもワールド空間で描画されます。その後、レンダースクリプトは別のパスで GUI コンポーネントをスクリーン空間に描画します。

### コンポーネントの Z 値 {#component-z-value}
すべてのゲームオブジェクトとコンポーネントは3D 空間に配置され、その位置は `vector3` オブジェクトで表されます。ゲームのグラフィックスを2D で表示する場合、X 値と Y 値は「幅」と「高さ」の軸に沿ったオブジェクトの位置を決め、Z 位置は「奥行き」の軸に沿った位置を決めます。Z 位置を使うと、重なり合うオブジェクトの見え方を制御できます。Z 値が1のスプライトは、Z 位置が0のスプライトより手前に表示されます。デフォルトでは、Defold は Z 値に -1 から1までを使用できる座標系を使います。

![モデル](images/graphics/z-order.png)

[レンダー述語](/manuals/render/#render-predicates)に一致するコンポーネントはまとめて描画され、描画される順序はコンポーネントの最終的な Z 値によって決まります。コンポーネントの最終的な Z 値は、コンポーネント自身の Z 値、それが属するゲームオブジェクトの Z 値、すべての親ゲームオブジェクトの Z 値を合計したものです。

::: sidenote
複数の GUI コンポーネントの描画順序は、GUI コンポーネントの Z 値では **決まりません**。GUI コンポーネントの描画順序は、[gui.set_render_order()](/ref/gui/#gui.set_render_order:order) 関数で制御します。
:::

例: A と B の2つのゲームオブジェクトがあります。B は A の子です。B にはスプライトコンポーネントがあります。

| 対象     | Z 値 |
|----------|---------|
| A        | 2       |
| B        | 1       |
| B#sprite | 0.5     |

![](images/graphics/component-hierarchy.png)

上記の階層では、B 上のスプライトコンポーネントの最終的な Z 値は 2 + 1 + 0.5 = 3.5 です。

::: important
2つのコンポーネントの Z 値が完全に同じ場合、順序は未定義です。コンポーネントの前後関係が交互に切り替わってちらついたり、プラットフォームによって描画順序が異なったりする可能性があります。

レンダースクリプトでは、Z 値に対するニアクリップ面とファークリップ面を定義します。Z 値がこの範囲外にあるコンポーネントは描画されません。デフォルトの範囲は -1 から1ですが、[簡単に変更できます](/manuals/render/#default-view-projection)。ニアとファーの限界値が -1 と1の場合、Z 値の数値精度は非常に高くなります。3D アセットを扱う際には、カスタムレンダースクリプトでデフォルトの投影のニアとファーの限界値を変更する必要がある場合があります。詳しくは、[レンダリングのマニュアル](/manuals/render/)を参照してください。
:::


:[Component max count optimizations](../shared/component-max-count-optimizations.md)
