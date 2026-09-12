---
title: コリジョン形状
brief: コリジョンオブジェクトにはプリミティブ形状、凸包、三角形メッシュを含められるほか、タイルマップや凸形状のリソースを使用できます。
---

# コリジョン形状 {#collision-shapes}

コリジョンオブジェクト（collision object）には、複数の埋め込み形状を含められます。3D 物理では、glTF または GLB ファイルの凸包や三角形メッシュも含められます。また、コリジョンオブジェクトの *Collision Shape* プロパティを通じて、タイルマップや凸形状のリソースを使用できます。

### プリミティブ形状 {#primitive-shapes}
プリミティブ形状（primitive shape）には、 *ボックス（box）* 、 *球（sphere）* 、 *カプセル（capsule）* があります。衝突判定や物理特性を持つコンポーネントであるコリジョンオブジェクト（collision object）を <kbd>右クリック</kbd> し、<kbd>Add Shape</kbd> を選択すると、プリミティブ形状を追加できます。

![プリミティブ形状の追加](images/physics/add_shape.png)

## ボックス形状 {#box-shape}
ボックスには位置、回転、寸法（幅、高さ、奥行き）があります。

![ボックス形状](images/physics/box.png)

## 球形状 {#sphere-shape}
球には位置、回転、直径があります。

![球形状](images/physics/sphere.png)

## カプセル形状 {#capsule-shape}
カプセルには位置、回転、直径、高さがあります。

![球形状](images/physics/capsule.png)

::: important
カプセル形状は、3D 物理を使用する場合にのみサポートされます（*game.project* ファイルの Physics セクションで設定します）。
:::

### 複雑な形状 {#complex-shapes}
複雑な形状には、タイルマップ（tilemap）のジオメトリや凸包（convex hull）のデータを使えます。Defold 1.13.2 以降では、3D コリジョンオブジェクトで、glTF または GLB シーンのメッシュから凸包や三角形メッシュの形状を作成することもできます。

## 3D の Hull 形状と Mesh 形状 {#hull-and-mesh-shapes-in-3d}

メッシュを凸形状で近似するには *Hull* 形状を使います。レベルのジオメトリの開口部などの凹領域を含め、メッシュの三角形に沿った衝突判定が必要な場合は *Mesh* 形状を使います。

1. *game.project* で **Physics → Type** を `3D` に設定します。
2. *Outline* でコリジョンオブジェクトを右クリックし、<kbd>Add Shape ▸ Hull</kbd> または <kbd>Add Shape ▸ Mesh</kbd> を選択します。
3. 新しい形状を選択し、*Scene* プロパティに *.gltf* または *.glb* ファイルを設定します。
4. *Mesh* フィールドで名前付きメッシュを選択します。一覧にない場合は、モデリングツールでメッシュに名前を付け、シーンを再度エクスポートします。
5. 形状の位置と回転を調整し、ゲームオブジェクトの表示ジオメトリに合わせます。必要に応じて同じ手順を繰り返し、形状を追加します。

選択したメッシュはローカルジオメトリを提供し、glTF ノードのトランスフォームは適用されません。Mesh コリジョン形状は、静的および非静的なコリジョンオブジェクトを含め、Bullet 3D バックエンドでサポートされています。2D 物理バックエンドではサポートされていません。

実行時の形状 API では、三角形メッシュのジオメトリは読み取り専用です。三角形を変更するには元のメッシュを編集し、再ビルドしてください。ゲームオブジェクトのスケールについては、[コリジョン形状の拡大縮小](#scaling-collision-shapes)を参照してください。

## タイルマップのコリジョン形状 {#tilemap-collision-shape}
Defold には、タイルマップで使用するタイルソース（tile source）の物理形状を簡単に生成する機能があります。[タイルソースのマニュアル](/manuals/tilesource/#tile-source-collision-shapes)では、タイルソースにコリジョングループ（collision group）を追加し、タイルをコリジョングループに割り当てる方法を説明しています（[例](/examples/tilemap/collisions/)）。

タイルマップに衝突判定を追加するには、次の手順に従います。

1. ゲームオブジェクト（game object）を <kbd>右クリック</kbd> し、<kbd>Add Component File</kbd> を選択して、ゲームオブジェクトにタイルマップを追加します。タイルマップファイルを選択します。
2. ゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component ▸ Collision Object</kbd> を選択して、ゲームオブジェクトにコリジョンオブジェクトコンポーネントを追加します。
3. コンポーネントに形状を追加する代わりに、*Collision Shape* プロパティに *tilemap* ファイルを設定します。
4. コリジョンオブジェクトコンポーネントの *Properties* を通常どおり設定します。

![タイルソースの衝突判定](images/physics/collision_tilemap.png)

::: important
コリジョングループはタイルマップのタイルソースで定義されるため、ここでは *Group* プロパティを **使用しません**。
:::

## 凸包形状 {#convex-hull-shape}
3D 物理では、[上記のエディターでの手順](#hull-and-mesh-shapes-in-3d)に従い、メッシュから凸包を直接作成できます。従来の `.convexshape` リソースもサポートされており、外部エディターを使って点から作成できます。

1. 外部エディターを使用して、凸包形状ファイル（拡張子 `.convexshape`）を作成します。
2. テキストエディターまたは外部ツール（下記参照）を使用して、ファイルを手動で編集します。
3. コリジョンオブジェクトコンポーネントに形状を追加する代わりに、*Collision Shape* プロパティに *凸形状* ファイルを設定します。

### ファイル形式 {#file-format}
凸包のファイル形式は、ほかのすべての Defold ファイルと同じデータ形式である protobuf テキスト形式を使用します。凸包形状では、凸包の点を定義します。2D 物理では、点を反時計回りの順序で指定することをお勧めします。3D 物理モードでは、抽象的な点群を使用します。2D の例を示します。

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

上の例では、長方形の4つの角を定義しています。

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## 外部ツール {#external-tools}

コリジョン形状の作成に使用できる外部ツールはいくつかあります。

* CodeAndWeb の [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) は、スプライト（sprite）とそれに合ったコリジョン形状を持つゲームオブジェクトの作成に使用できます。
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor) は、凸包形状の作成に使用できます。
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/) は、凸包形状の作成に使用できます。


# コリジョン形状の拡大縮小 {#scaling-collision-shapes}
コリジョンオブジェクトとその形状は、ゲームオブジェクトのスケールを継承します。この動作を無効にするには、*game.project* の Physics セクションで [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) チェックボックスをオフにします。均等な拡大縮小のみがサポートされ、スケールが均等でない場合は、最も小さいスケール値が使用されます。

# コリジョン形状のサイズ変更 {#resizing-collision-shapes}
プリミティブ形状は、`physics.set_shape()` を使用して実行時にサイズを変更できます。この関数は、凸包の頂点や三角形メッシュのジオメトリを置き換えません。例を示します。

```lua
-- set capsule shape data
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- set sphere shape data
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- set box shape data
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
指定した ID を持つ正しい種類の形状が、コリジョンオブジェクトにすでに存在している必要があります。
:::

# コリジョン形状の回転 {#rotating-collision-shapes}

## 3D 物理でのコリジョン形状の回転 {#rotating-collision-shapes-in-3d-physics}
3D 物理のコリジョン形状は、すべての軸を中心に回転できます。


## 2D 物理でのコリジョン形状の回転 {#rotating-collision-shapes-in-2d-physics}
2D 物理のコリジョン形状は、z 軸を中心にのみ回転できます。x 軸または y 軸を中心に回転すると誤った結果になるため、避けてください。形状を x 軸または y 軸に沿って実質的に反転させるために180度回転する場合も同様です。物理形状を反転するには、[`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) と [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip) の使用をお勧めします。


# デバッグ {#debugging}
[物理のデバッグを有効にする](/manuals/debugging-game-logic/#debugging-problems-with-physics)と、実行時にコリジョン形状を確認できます。
