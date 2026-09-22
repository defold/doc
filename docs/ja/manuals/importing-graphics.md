---
title: 2D グラフィックスのインポートと使用
brief: このマニュアルでは、2D グラフィックスをインポートして使用する方法を説明します。
---

# 2D グラフィックスのインポート {#importing-2d-graphics}

Defold は、2D ゲームでよく使われるさまざまな種類の描画用コンポーネント（component）をサポートしています。Defold では、静止したスプライト（sprite）やアニメーションするスプライト、UI コンポーネント、パーティクルエフェクト（particle effect）、タイルマップ（tile map）、ビットマップフォント（bitmap font）を作成できます。これらの描画用コンポーネントを作成するには、まず使用するグラフィックスを含む画像ファイルをインポートする必要があります。画像ファイルをインポートするには、コンピューター上のファイルシステムからファイルをドラッグし、Defold エディターの *Assets ペイン* 内の適切な場所にドロップするだけです。

![ファイルのインポート](images/graphics/import.png)

::: sidenote
Defold は PNG 形式と JPEG 形式の画像をサポートしています。ほかの形式の画像は、使用する前に変換する必要があります。
:::


## Defold アセットの作成 {#creating-defold-assets}

Defold に画像をインポートすると、その画像を使って Defold 固有のアセット（asset）を作成できます。

![アトラス](images/icons/atlas.png){.icon} アトラス
: アトラス（atlas）には個別の画像ファイルのリストが含まれ、それらの画像はより大きなテクスチャ画像に自動的にまとめられます。アトラスには静止画像と、連続した画像を切り替えるフリップブックアニメーション（flipbook animation）を構成する画像の集合である *アニメーショングループ（Animation Groups）* を含められます。

  ![アトラス](images/graphics/atlas.png)

アトラスリソースについて詳しくは、[アトラスのマニュアル](/manuals/atlas)を参照してください。

![タイルソース](images/icons/tilesource.png){.icon} タイルソース
: タイルソース（tile source）は、小さな画像を均一なグリッドに並べて構成した画像ファイルを参照します。このように複数の画像をまとめた画像は、一般に _スプライトシート（sprite sheet）_ とも呼ばれます。タイルソースには、アニメーションの最初と最後のタイルで定義するフリップブックアニメーションを含められます。また、画像を使ってタイルにコリジョン形状（collision shape）を自動的に付加することもできます。

  ![タイルソース](images/graphics/tilesource.png)

タイルソースリソースについて詳しくは、[タイルソースのマニュアル](/manuals/tilesource)を参照してください。

![ビットマップフォント](images/icons/font.png){.icon} ビットマップフォント
: ビットマップフォントは、PNG 形式のフォントシートにグリフ（glyph）を格納します。この種類のフォントは、TrueType または OpenType のフォントファイルから生成したフォントと比べてパフォーマンスは向上しませんが、任意のグラフィックス、色、影を画像に直接含められます。

ビットマップフォントについて詳しくは、[フォントのマニュアル](/manuals/font/#bitmap-bmfonts)を参照してください。

  ![BMfont](images/font/bm_font.png)


## Defold アセットの使用 {#using-defold-assets}

画像をアトラスファイルとタイルソースファイルに変換すると、それらを使ってさまざまな種類の描画用コンポーネントを作成できます。

![スプライト](images/icons/sprite.png){.icon}
: スプライトは、画面に表示する静止画像またはフリップブックアニメーションです。

  ![スプライト](images/graphics/sprite.png)

スプライトについて詳しくは、[スプライトのマニュアル](/manuals/sprite)を参照してください。

![タイルマップ](images/icons/tilemap.png){.icon} タイルマップ
: タイルマップコンポーネントは、タイルソースから取得したタイル（画像とコリジョン形状）を組み合わせてマップを作成します。タイルマップではアトラスをソースとして使用できません。

  ![タイルマップ](images/graphics/tilemap.png)

タイルマップについて詳しくは、[タイルマップのマニュアル](/manuals/tilemap)を参照してください。

![パーティクルエフェクト](images/icons/particlefx.png){.icon} パーティクルエフェクト
: パーティクルエミッター（particle emitter）から生成されるパーティクルは、アトラスまたはタイルソースの静止画像またはフリップブックアニメーションで構成されます。

  ![パーティクル](images/graphics/particles.png)

パーティクルエフェクトについて詳しくは、[パーティクルエフェクトのマニュアル](/manuals/particlefx)を参照してください。

![GUI](images/icons/gui.png){.icon} GUI
: GUI のボックスノード（box node）と、円や扇形を表示するパイノード（pie node）では、アトラスやタイルソースの静止画像とフリップブックアニメーションを使用できます。

  ![GUI](images/graphics/gui.png)

GUI について詳しくは、[GUI のマニュアル](/manuals/gui)を参照してください。
