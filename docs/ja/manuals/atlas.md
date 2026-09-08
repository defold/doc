---
title: アトラスマニュアル
brief: このマニュアルでは、Defold のアトラスリソースの仕組みを説明します。
---

# アトラス {#atlas}

スプライト（sprite）の元画像には個別の画像がよく使われますが、パフォーマンスのために、画像をアトラス（atlas）と呼ばれる大きな画像の集合にまとめる必要があります。小さな画像の集合をアトラスにまとめることは、デスクトップマシンや専用ゲーム機よりもメモリや処理能力が限られるモバイルデバイスでは特に重要です。

Defold のアトラスリソース（atlas resource）は、個別の画像ファイルのリストです。これらの画像は自動的に1つの大きな画像にまとめられます。

## アトラスの作成 {#creating-an-atlas}

*Assets* ブラウザーのコンテキストメニューから <kbd>New... ▸ Atlas</kbd> を選択します。新しいアトラスファイルに名前を付けます。エディターがそのファイルをアトラスエディターで開きます。アトラスのプロパティは
*Properties* ペインに表示され、編集できます（詳細は後述します）。

スプライトや ParticleFX など、オブジェクトのコンポーネント（component）のグラフィックスソースとして使用するには、先にアトラスに画像やアニメーションを追加する必要があります。

画像がプロジェクトに追加されていることを確認します（画像ファイルを *Assets* ブラウザーの適切な場所にドラッグ＆ドロップします）。

個別の画像の追加

: *Asset* ペインからエディタービューに画像をドラッグ＆ドロップします。
  
  または、*Outline* ペインのルートの Atlas 項目を <kbd>右クリック</kbd> します。

  表示されるコンテキストメニューから <kbd>Add Images</kbd> を選択して、個別の画像を追加します。

  ダイアログが開き、アトラスに追加する画像を探して選択できます。画像ファイルを絞り込んだり、複数のファイルを一度に選択したりできます。

  ![アトラスの作成と画像の追加](images/atlas/add.png)

  追加した画像は *Outline* に一覧表示され、中央のエディタービューでアトラス全体を確認できます。選択した項目を画面に収めるには、<kbd>F</kbd> を押す必要がある場合があります（メニューの <kbd>View ▸ Frame Selection</kbd>）。

  ![追加された画像](images/atlas/single_images.png)

フリップブックアニメーションの追加
: *Outline* ペインのルートの Atlas 項目を <kbd>右クリック</kbd> します。

  表示されるコンテキストメニューから <kbd>Add Animation Group</kbd> を選択して、フリップブックアニメーション（flipbook animation）のグループを作成します。

  既定の名前（`New Animation`）を持つ、新しい空のアニメーショングループがアトラスに追加されます。

  *Asset* ペインからエディタービューに画像をドラッグ＆ドロップすると、現在選択しているグループに追加されます。
  
  または、新しいグループを <kbd>右クリック</kbd> し、コンテキストメニューから <kbd>Add Images</kbd> を選択します。

  ダイアログが開き、アニメーショングループに追加する画像を探して選択できます。

  ![アトラスの作成と画像の追加](images/atlas/add_animation.png)

  アニメーショングループを選択した状態で <kbd>Space</kbd> を押すとプレビューでき、<kbd>Ctrl/Cmd+T</kbd> でプレビューを閉じます。必要に応じて、アニメーションの *Properties* を調整します（後述します）。

  ![アニメーショングループ](images/atlas/animation_group.png)

Outline で画像を選択して <kbd>Alt + Up/down</kbd> を押すと、画像の順序を変更できます。また、Outline 内の画像をコピーして貼り付けると、簡単に複製を作成できます（<kbd>Edit</kbd> メニュー、右クリックのコンテキストメニュー、またはキーボードショートカットを使います）。

## アトラスのプロパティ {#atlas-properties}

各アトラスリソースには、一連のプロパティがあります。*Outline* ビューでルート項目を選択すると、*Properties* ペインに表示されます。

Size
: 生成されるテクスチャ（texture）リソースの合計サイズを、計算結果として表示します。幅と高さは、最も近い2の累乗に設定されます。テクスチャ圧縮を有効にすると、一部の形式では正方形のテクスチャが必要になります。その場合、正方形ではないテクスチャはサイズを変更し、空の領域を埋めて正方形にします。詳細は [テクスチャプロファイルマニュアル](/manuals/texture-profiles/) を参照してください。

Margin
: 各画像の間に追加するピクセル数です。

Inner Padding
: 各画像の周囲に余白として追加する空のピクセル数です。

Extrude Borders
: 各画像の周囲に、端のピクセルを繰り返して追加するピクセル数です。フラグメントシェーダーが画像の端のピクセルをサンプリングすると、同じアトラステクスチャ上にある隣の画像のピクセルがにじむことがあります。境界を押し出すことで、この問題を解決します。

Max Page Size
: 複数ページのアトラスにおける、1ページの最大サイズです。アトラスを同じアトラスの複数のページに分割し、ドローコールを1回に保ちながらアトラスのサイズを制限できます。この機能は、`/builtins/materials/*_paged_atlas.material` にある、複数ページのアトラスに対応したマテリアル（material）と組み合わせて使う必要があります。

![複数ページのアトラス](images/atlas/multipage_atlas.png)

Rename Patterns
: 検索・置換パターンをカンマ（´,´）で区切ったリストです。各パターンは `search=replace` という形式です。
各画像の元の名前（ファイルのベース名）は、これらのパターンで変換されます（たとえば、`hat=cat,_normal=` というパターンは、`hat_normal` という名前の画像を `cat` に変更します）。これは、アトラス間でアニメーションの名前を一致させる場合に便利です。

以下は、64x64 の正方形の画像を4枚アトラスに追加し、各プロパティをさまざまな値に設定した例です。画像が 128x128 に収まらなくなると、アトラスはすぐに 256x256 に拡大し、テクスチャ内に多くの無駄な空き領域が生じる点に注目してください。

![アトラスのプロパティ](images/atlas/atlas_properties.png)

## 画像のプロパティ {#image-properties}

アトラス内の各画像には、一連のプロパティがあります。

Id
: 画像の識別子です（読み取り専用）。

Size
: 画像の幅と高さです（読み取り専用）。

Pivot
: 画像のピボット点です（単位座標で指定）。左上は (0,0)、右下は (1,1) です。既定値は (0.5, 0.5) です。ピボットは 0-1 の範囲外でもかまいません。ピボット点は、スプライトなどで使用したときに画像の中心となる位置です。エディタービューでピボットハンドルをドラッグして、ピボット点を変更できます。ハンドルは、画像を1枚だけ選択している場合にのみ表示されます。ドラッグ中に <kbd>Shift</kbd> を押すと、スナップを有効にできます。

Sprite Trim Mode
: スプライトの描画方法です。既定ではスプライトを矩形として描画します（Sprite Trim Mode が Off に設定されている場合）。スプライトに透明なピクセルが多く含まれている場合は、4～8個の頂点を使った矩形以外の形状として描画すると、効率がよくなることがあります。スプライトのトリミングは、slice-9 スプライトとは併用できません。

Image
: 画像自体のパスです。

![画像のプロパティ](images/atlas/image_properties.png)

## アニメーションのプロパティ {#animation-properties}

アニメーショングループに含まれる画像のリストに加えて、次のプロパティを設定できます。

Id
: アニメーションの名前です。

Fps
: アニメーションの再生速度を、1秒あたりのフレーム数（FPS）で指定します。

Flip horizontal
: アニメーションを水平方向に反転します。

Flip vertical
: アニメーションを垂直方向に反転します。

Playback
: アニメーションの再生方法を指定します。

  - `None` は再生せず、最初の画像を表示します。
  - `Once Forward` は、最初の画像から最後の画像までアニメーションを1回再生します。
  - `Once Backward` は、最後の画像から最初の画像までアニメーションを1回再生します。
  - `Once Ping Pong` は、最初の画像から最後の画像まで進み、その後最初の画像に戻るアニメーションを1回再生します。
  - `Loop Forward` は、最初の画像から最後の画像までアニメーションを繰り返し再生します。
  - `Loop Backward` は、最後の画像から最初の画像までアニメーションを繰り返し再生します。
  - `Loop Ping Pong` は、最初の画像から最後の画像まで進み、その後最初の画像に戻るアニメーションを繰り返し再生します。

## 実行時のテクスチャとアトラスの作成 {#runtime-texture-and-atlas-creation}

テクスチャとアトラスは、実行時に作成できます。

### 実行時のテクスチャリソースの作成 {#creating-a-texture-resource-at-runtime}

[`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) を使って、新しいテクスチャリソースを作成します。

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

テクスチャを作成したら、[`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) を使ってテクスチャのピクセルを設定できます。

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
バッファーの幅と高さをテクスチャ全体のサイズより小さくし、`resource.set_texture()` に渡す x と y のパラメーターを変更すると、`resource.set_texture()` でテクスチャの一部分だけを更新することもできます。
:::

テクスチャは、`go.set()` を使って [モデルコンポーネント](/manuals/model/) に直接使用できます。

```lua
  go.set("#model", "texture0", my_texture_id)
```

### 実行時のアトラスの作成 {#creating-an-atlas-at-runtime}

テクスチャを [スプライトコンポーネント](/manuals/sprite/) で使用するには、先にアトラスでそのテクスチャを使う必要があります。[`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) を使ってアトラスを作成します。

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

`frames` の各要素は、`geometries` テーブルを参照する1始まりのインデックスです。リストではジオメトリを再利用したり、順序を入れ替えたり、スキップしたりできます。これらは、非推奨の範囲フィールド `frame_start` と `frame_end` では表現できません。`resource.get_atlas()` は `frames` を返します。`resource.set_atlas()` や `resource.create_atlas()` にアトラスのデータを渡すときも、同じ表現を使ってください。互換性のため、設定関数と作成関数は引き続き範囲フィールドを受け付けますが、新しいコードでは `frames` を使うことを推奨します。
