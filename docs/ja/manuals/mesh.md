---
title: Defold の 3D メッシュ
brief: このマニュアルでは、ゲームの実行時に 3D メッシュを作成する方法を説明します。
---

# メッシュコンポーネント {#mesh-component}

Defold は、その根幹において 3D エンジンです。2D の素材だけを扱う場合でも、すべての描画は 3D で行われ、画面には正投影されます。Defold では、実行時にコレクション（collection）内で 3D メッシュ（mesh）を追加、作成することで、3D コンテンツを全面的に活用できます。3D アセットだけを使って完全な 3D ゲームを作成することも、3D と 2D のコンテンツを自由に組み合わせることもできます。

## メッシュコンポーネントの作成 {#creating-a-mesh-component}

メッシュコンポーネントは、ほかのゲームオブジェクト（game object）のコンポーネント（component）と同じように作成します。作成方法は2つあります。

- *Assets* ブラウザー内の場所を <kbd>右クリック</kbd> し、<kbd>New... ▸ Mesh</kbd> を選択して、*メッシュファイル* を作成します。
- *Outline* ビューでゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component ▸ Mesh</kbd> を選択して、ゲームオブジェクトに直接埋め込まれたコンポーネントを作成します。

![ゲームオブジェクト内のメッシュ](images/mesh/mesh.png)

メッシュを作成したら、いくつかのプロパティを指定する必要があります。

### メッシュのプロパティ {#mesh-properties}

*Id*、*Position*、*Rotation* の各プロパティに加えて、次のコンポーネント固有のプロパティがあります。

*Material*
: メッシュの描画に使用するマテリアル（material）です。

*Vertices*
: ストリームごとのメッシュデータを記述するバッファーファイルです。

*Primitive Type*
: Lines、Triangles、Triangle Strip のいずれかです。

*Position Stream*
: このプロパティには *position* ストリームの名前を指定します。このストリームは、頂点シェーダーへの入力として自動的に渡されます。

*Normal Stream*
: このプロパティには *normal* ストリームの名前を指定します。このストリームは、頂点シェーダーへの入力として自動的に渡されます。

*tex0*
: メッシュに使用するテクスチャを設定します。

## エディターでの操作 {#editor-manipulation}

メッシュコンポーネントを配置したら、通常の *Scene Editor* ツールでコンポーネントや、それを含むゲームオブジェクトを自由に編集、操作し、メッシュを好きなように移動、回転、拡大縮小できます。

## 実行時の操作 {#runtime-manipulation}

Defold のバッファーを使って、実行時にメッシュを操作できます。次の例では、トライアングルストリップから立方体を作成します。

```Lua

-- cube
local vertices = {
	0, 0, 0,
	0, 1, 0,
	1, 0, 0,
	1, 1, 0,
	1, 1, 1,
	0, 1, 0,
	0, 1, 1,
	0, 0, 1,
	1, 1, 1,
	1, 0, 1,
	1, 0, 0,
	0, 0, 1,
	0, 0, 0,
	0, 1, 0
}

-- create a buffer with a position stream
local buf = buffer.create(#vertices / 3, {
	{ name = hash("position"), type=buffer.VALUE_TYPE_FLOAT32, count = 3 }
})

-- get the position stream and write the vertices
local positions = buffer.get_stream(buf, "position")
for i, value in ipairs(vertices) do
	positions[i] = vertices[i]
end

-- set the buffer with the vertices on the mesh
local res = go.get("#mesh", "vertices")
resource.set_buffer(res, buf)
```

メッシュコンポーネントの使い方に関する詳細や、サンプルプロジェクト、コード例については、[フォーラムの告知投稿](https://forum.defold.com/t/mesh-component-in-defold-1-2-169-beta/65137)を参照してください。

## 視錐台カリング {#frustum-culling}

メッシュコンポーネントは動的であり、位置データがどのようにエンコードされているかを確実に知ることができないため、自動的にはカリングされません。メッシュをカリングするには、6つの浮動小数点数（AABB の最小値と最大値）を使って、メッシュの軸平行バウンディングボックス（axis-aligned bounding box）をバッファーのメタデータに設定する必要があります。

```lua
buffer.set_metadata(buf, hash("AABB"), { 0, 0, 0, 1, 1, 1 }, buffer.VALUE_TYPE_FLOAT32)
```

## マテリアル定数 {#material-constants}

{% include shared/material-constants.md component='mesh' variable='tint' %}

`tint`
: メッシュの色調（`vector4`）です。`vector4` で色調を表し、x、y、z、w がそれぞれ赤、緑、青、アルファ値の色調に対応します。

## 頂点のローカル空間とワールド空間 {#vertex-local-vs-world-space}
メッシュのマテリアルの Vertex Space 設定が Local Space に設定されている場合、データはそのままシェーダーに渡されるため、通常どおり GPU 上で頂点や法線を変換する必要があります。

メッシュのマテリアルの Vertex Space 設定が World Space に設定されている場合は、デフォルトの `position` と `normal` ストリームを指定するか、メッシュの編集時にドロップダウンから選択する必要があります。これにより、エンジンがデータをワールド空間に変換し、ほかのオブジェクトとバッチ処理できるようになります。
