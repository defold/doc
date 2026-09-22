---
title: Defold のタイルマップマニュアル
brief: このマニュアルでは、Defold のタイルマップ対応について詳しく説明します。
---

# タイルマップ {#tile-map}

*タイルマップ（Tile Map）* は、*タイルソース（Tile Source）* のタイルを広いグリッド領域に組み合わせて配置したり、描画したりできるコンポーネント（component）です。タイルマップは、ゲームのレベル環境を構築するためによく使われます。また、タイルソースの *コリジョン形状（Collision Shapes）* をマップで使用し、衝突判定や物理シミュレーションに利用できます（[例](/examples/tilemap/collisions/)）。

タイルマップを作成するには、まずタイルソースを作成する必要があります。タイルソースの作成方法については、[タイルソースマニュアル](/manuals/tilesource)を参照してください。

## タイルマップの作成 {#creating-a-tile-map}

新しいタイルマップを作成するには、次の手順に従います。

- *Assets* ブラウザー内の場所を <kbd>右クリック</kbd> し、<kbd>New... ▸ Tile Map</kbd> を選択します。
- ファイルに名前を付けます。
- 新しいタイルマップがタイルマップエディターで自動的に開きます。

  ![新しいタイルマップ](images/tilemap/tilemap.png)

- *Tile Source* プロパティに、準備したタイルソースファイルを設定します。

タイルマップにタイルを描画するには、次の手順に従います。

1. *Outline* ビューで、描画先の *Layer* を選択または作成します。
2. ブラシとして使用するタイルを選択します（<kbd>Space</kbd> を押すとタイルパレットが表示されます）。または、パレット内でクリックしてドラッグし、複数のタイルを選択して、複数タイルで構成される長方形のブラシを作成します。

   ![パレット](images/tilemap/palette.png)

3. 選択したブラシで描画します。タイルを消すには、空のタイルを選んでブラシとして使用するか、消しゴム（<kbd>Edit ▸ Select Eraser</kbd>）を選択します。

   ![タイルの描画](images/tilemap/paint_tiles.png)

レイヤーから直接タイルを選び、選択範囲をブラシとして使用できます。<kbd>Shift</kbd> を押しながらタイルをクリックすると、そのタイルを現在のブラシとして選択できます。また、<kbd>Shift</kbd> を押しながらクリックしてドラッグすると、タイルのまとまりを選択して、より大きなブラシとして使用できます。同様に、<kbd>Shift+Ctrl</kbd> を押しながら操作するとタイルを切り取り、<kbd>Shift+Alt</kbd> を押しながら操作するとタイルを消すこともできます。

ブラシを時計回りに回転するには、<kbd>Z</kbd> を使用します。ブラシを水平方向に反転するには <kbd>X</kbd> を、垂直方向に反転するには <kbd>Y</kbd> を使用します。

![タイルの選択](images/tilemap/pick_tiles.png)

## ゲームへのタイルマップの追加 {#adding-a-tile-map-to-your-game}

ゲームにタイルマップを追加するには、次の手順に従います。

1. タイルマップコンポーネントを格納するゲームオブジェクト（game object）を作成します。ゲームオブジェクトはファイル内に置くことも、コレクション（collection）内に直接作成することもできます。
2. ゲームオブジェクトのルートを右クリックし、<kbd>Add Component File</kbd> を選択します。
3. タイルマップファイルを選択します。

![タイルマップの使用](images/tilemap/use_tilemap.png)

## 実行時の操作 {#runtime-manipulation}

さまざまな関数やプロパティを使って、実行時にタイルマップを操作できます（使用方法については [API ドキュメント](/ref/tilemap/)を参照してください）。

### スクリプトからのタイルの変更 {#changing-tiles-from-script}

ゲームの実行中に、タイルマップの内容を動的に読み書きできます。これには、[`tilemap.get_tile()`](/ref/tilemap/#tilemap.get_tile) 関数と [`tilemap.set_tile()`](/ref/tilemap/#tilemap.set_tile) 関数を使用します。

```lua
local tile = tilemap.get_tile("/level#map", "ground", x, y)

if tile == 2 then
    -- Replace grass-tile (2) with dangerous hole tile (number 4).
    tilemap.set_tile("/level#map", "ground", x, y, 4)
end
```

## タイルマップのプロパティ {#tilemap-properties}

*Id*、*Position*、*Rotation*、*Scale* に加えて、次のコンポーネント固有のプロパティがあります。

*Tile Source*
: タイルマップに使用するタイルソースのリソース（resource）です。

*Material*
: タイルマップのレンダリングに使用するマテリアル（material）です。

*Blend Mode*
: タイルマップのレンダリング時に使用するブレンドモード（blend mode）です。

### ブレンドモード {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

### プロパティの変更 {#changing-properties}

タイルマップには、`go.get()` と `go.set()` を使って操作できるさまざまなプロパティがあります。

`tile_source`
: タイルマップのタイルソース（`hash`）です。タイルソースのリソースプロパティと `go.set()` を使って変更できます。[API リファレンスの例](/ref/tilemap/#tile_source)を参照してください。

`material`
: タイルマップのマテリアル（`hash`）です。マテリアルのリソースプロパティと `go.set()` を使って変更できます。[API リファレンスの例](/ref/tilemap/#material)を参照してください。

### マテリアル定数 {#material-constants}

{% include shared/material-constants.md component='tilemap' variable='tint' %}

`tint`
: タイルマップの色調（`vector4`）です。`vector4` で色調を表し、x、y、z、w がそれぞれ赤、緑、青、アルファの色調に対応します。

## プロジェクト設定 {#project-configuration}

*game.project* ファイルには、タイルマップに関連する[プロジェクト設定](/manuals/project-settings#tilemap)がいくつかあります。

## 外部ツール {#external-tools}

Defold のタイルマップに直接エクスポートできる外部のマップ／レベルエディターがあります。

### Tiled

[Tiled](https://www.mapeditor.org/) は、直交、アイソメトリック、六角形のマップに対応した、よく知られた広く使われているマップエディターです。Tiled は幅広い機能を備えており、[Defold に直接エクスポート](https://doc.mapeditor.org/en/stable/manual/export-defold/)できます。タイルマップのデータや追加のメタデータをエクスポートする方法については、[Defold ユーザー「goeshard」によるこちらのブログ記事](https://goeshard.org/2025/01/01/using-tiled-object-layers-with-defold-tilemaps/)を参照してください。


### Tilesetter

[Tilesetter](https://www.tilesetter.org/docs/exporting#defold) を使うと、シンプルな基本タイルから完全なタイルセットを自動作成できます。また、Defold に直接エクスポートできるマップエディターも備えています。



