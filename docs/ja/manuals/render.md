---
title: Defold のレンダリングパイプライン
brief: このマニュアルでは、Defold のレンダリングパイプラインの仕組みと、そのプログラミング方法を説明します。
---

# レンダリング {#render}

エンジンが画面に表示するスプライト（sprite）、モデル（model）、タイル、パーティクル、GUI ノード（GUI node）などのすべてのオブジェクトは、レンダラーによって描画されます。レンダラーの中心にあるのが、レンダリングパイプライン（render pipeline）を制御するレンダースクリプト（render script）です。デフォルトでは、すべての 2D オブジェクトが適切なビットマップを使い、指定されたブレンドと適切な Z 深度で描画されます。そのため、描画順序と単純なブレンド以外は、レンダリングについて考える必要がないかもしれません。ほとんどの 2D ゲームではデフォルトのパイプラインで十分に機能しますが、ゲームによっては特別な要件があるかもしれません。そのような場合、Defold では要件に合わせたレンダリングパイプラインを記述できます。

### レンダリングパイプライン — 何を、いつ、どこに描画するか？ {#render-pipeline-what-when-and-where}

レンダリングパイプラインは、何を、いつ、どこに描画するかを制御します。何を描画するかは[レンダー述語（render predicate）](#render-predicates)で制御します。述語の描画タイミングは[レンダースクリプト](#the-render-script)で制御し、述語の描画先は[ビュープロジェクション](#default-view-projection)で制御します。また、レンダリングパイプラインは、レンダー述語で描画されるグラフィックスのうち、定義されたバウンディングボックスや視錐台（frustum）の外側にあるものをカリングできます。この処理を視錐台カリング（frustum culling）と呼びます。


## デフォルトのレンダリング {#the-default-render}

レンダーファイルには、現在のレンダースクリプトへの参照と、そのレンダースクリプトで使用できるようにするカスタムのマテリアル（material）が含まれます（[`render.enable_material()`](/ref/render/#render.enable_material) で使用します）。

レンダリングパイプラインの中心にあるのが、_レンダースクリプト_ です。これは `init()`、`update()`、`on_message()` 関数を持つ Lua スクリプトで、主に基盤となるグラフィックス API とのやり取りに使われます。レンダースクリプトは、ゲームのライフサイクルの中で特別な位置を占めています。詳しくは、[アプリケーションのライフサイクルのドキュメント](/manuals/application-lifecycle)を参照してください。

プロジェクトの「Builtins」フォルダーには、デフォルトのレンダーリソース（「default.render」）とデフォルトのレンダースクリプト（「default.render_script」）があります。

![組み込みのレンダリング](images/render/builtin.png)

カスタムレンダラーを設定するには、次の手順を実行します。

1. 「default.render」と「default.render_script」のファイルを、プロジェクト階層内の任意の場所にコピーします。もちろん、レンダースクリプトを最初から作成することもできますが、特に Defold やグラフィックスプログラミングに慣れていない場合は、デフォルトのスクリプトのコピーから始めることをお勧めします。

2. コピーした「default.render」ファイルを編集し、*Script* プロパティがコピーしたレンダースクリプトを参照するように変更します。

3. *game.project* 設定ファイルの *Render* プロパティ（*bootstrap* 内）が、コピーした「default.render」ファイルを参照するように変更します。


## レンダー述語 {#render-predicates}

オブジェクトの描画順序を制御するには、レンダー _述語_ を作成します。述語は、選択したマテリアルの _タグ_ に基づいて、何を描画するかを宣言します。

画面に描画される各オブジェクトには、画面への描画方法を制御するマテリアルが割り当てられています。マテリアルには、そのマテリアルに関連付ける1つ以上の _タグ_ を指定します。

そのうえで、レンダースクリプトに*レンダー述語*を作成し、その述語に含めるタグを指定できます。述語を描画するようエンジンに指示すると、その述語に指定したすべてのタグを含むマテリアルを持つ各オブジェクトが描画されます。

```
Sprite 1        Sprite 2        Sprite 3        Sprite 4
Material A      Material A      Material B      Material C
  outlined        outlined        greyscale       outlined
  tree            tree            tree            house
```

```lua
-- a predicate matching all sprites with tag "tree"
local trees = render.predicate({"tree"})
-- will draw Sprite 1, 2 and 3
render.draw(trees)

-- a predicate matching all sprites with tag "outlined"
local outlined = render.predicate({"outlined"})
-- will draw Sprite 1, 2 and 4
render.draw(outlined)

-- a predicate matching all sprites with tags "outlined" AND "tree"
local outlined_trees = render.predicate({"outlined", "tree"})
-- will draw Sprite 1 and 2
render.draw(outlined_trees)
```


マテリアルの仕組みについて詳しくは、[マテリアルのドキュメント](/manuals/material)を参照してください。


## デフォルトのビュープロジェクション {#default-view-projection}

デフォルトのレンダースクリプトは、2D ゲームに適した正投影（orthographic projection）を使うように設定されています。`Stretch`（デフォルト）、`Fixed Fit`、`Fixed` の3種類の正投影が用意されています。デフォルトのレンダースクリプトにある正投影の代わりに、カメラコンポーネント（camera component）が提供する投影行列を使うこともできます。

### ストレッチ投影 {#stretch-projection}

ストレッチ投影は、ウィンドウのサイズが変更されても、常に *game.project* に設定した寸法と等しい範囲のゲームを描画します。アスペクト比が変わると、ゲームの表示内容が縦または横に引き伸ばされます。

![ストレッチ投影](images/render/stretch_projection.png)

*元のウィンドウサイズでのストレッチ投影*

![サイズ変更時のストレッチ投影](images/render/stretch_projection_resized.png)

*ウィンドウを横に引き伸ばしたときのストレッチ投影*

ストレッチ投影はデフォルトの投影方式です。別の方式に変更した後で元に戻すには、レンダースクリプトにメッセージを送信します。

```lua
msg.post("@render:", "use_stretch_projection", { near = -1, far = 1 })
```

### 固定フィット投影 {#fixed-fit-projection}

ストレッチ投影と同様に、固定フィット投影は常に *game.project* に設定した寸法と等しい範囲のゲームを表示します。ただし、ウィンドウのサイズが変更されてアスペクト比が変わった場合は、ゲームの表示内容は元のアスペクト比を維持し、縦または横にゲームの追加の範囲が表示されます。

![固定フィット投影](images/render/fixed_fit_projection.png)

*元のウィンドウサイズでの固定フィット投影*

![サイズ変更時の固定フィット投影](images/render/fixed_fit_projection_resized.png)

*ウィンドウを横に引き伸ばしたときの固定フィット投影*

![縮小時の固定フィット投影](images/render/fixed_fit_projection_resized_smaller.png)

*ウィンドウを元のサイズの 50% に縮小したときの固定フィット投影*

固定フィット投影を有効にするには、レンダースクリプトにメッセージを送信します。

```lua
msg.post("@render:", "use_fixed_fit_projection", { near = -1, far = 1 })
```

### 固定投影 {#fixed-projection}

固定投影は、元のアスペクト比を維持し、一定のズーム倍率でゲームの内容を描画します。つまり、ズーム倍率が 100% 以外に設定されている場合、*game.project* の寸法で定義されたゲームの範囲よりも広い範囲、または狭い範囲が表示されます。

![固定投影](images/render/fixed_projection_zoom_2_0.png)

*ズームを 2 に設定した固定投影*

![固定投影](images/render/fixed_projection_zoom_0_5.png)

*ズームを 0.5 に設定した固定投影*

![固定投影](images/render/fixed_projection_zoom_2_0_resized.png)

*ズームを 2 に設定し、ウィンドウを元のサイズの 50% に縮小した固定投影*

固定投影を有効にするには、レンダースクリプトにメッセージを送信します。

```lua
msg.post("@render:", "use_fixed_projection", { near = -1, far = 1, zoom = 2 })
```

### カメラ投影 {#camera-projection}

デフォルトのレンダースクリプトを使用していて、プロジェクトに有効な[カメラコンポーネント](/manuals/camera)がある場合、そのカメラはレンダースクリプトで設定されたほかのビューや投影より優先されます。レンダースクリプトでのカメラコンポーネントの使い方について詳しくは、[カメラのドキュメント](/manuals/camera)を参照してください。

正投影カメラは、ウィンドウへのカメラの適応方法を制御する `Orthographic Mode` に対応しています。
- `Fixed` は、カメラの `Orthographic Zoom` の値を使います。
- `Auto Fit`（全体を収める）は、デザイン領域全体が見える状態を保ちます。
- `Auto Cover`（全体を覆う）は、ウィンドウ全体を埋めますが、一部が切り取られることがあります。

モードはエディターで切り替えるか、実行時に Camera API を使って切り替えられます。

```lua
-- Use auto-fit behavior with an orthographic camera
camera.set_orthographic_mode("main:/go#camera", camera.ORTHO_MODE_AUTO_FIT)
-- Query current mode
local mode = camera.get_orthographic_mode("main:/go#camera")
```

## 視錐台カリング {#frustum-culling}

Defold のレンダー API を使うと、開発者は視錐台カリングと呼ばれる処理を実行できます。視錐台カリングが有効な場合、定義されたバウンディングボックスや視錐台の外側にあるグラフィックスはすべて無視されます。一度に一部分だけが表示される大きなゲームワールドでは、視錐台カリングによって、描画のために GPU に送信する必要があるデータ量を大幅に削減できます。その結果、パフォーマンスが向上し、モバイルデバイスではバッテリーの消費を抑えられます。バウンディングボックスの作成には、一般的にカメラのビューと投影を使います。デフォルトのレンダースクリプトは、カメラのビューと投影を使って視錐台を計算します。

ドローコール（draw call）の視錐台カリングを有効にするには、`render.draw()` の `frustum` オプションにビュープロジェクション行列を渡します。

```lua
local frustum = self.proj * self.view
render.draw(predicates.particle, { frustum = frustum })
```

カメラコンポーネントを使って描画する場合、`render.set_camera()` により、後続のドローコールでカメラのビュープロジェクション行列を自動的に使えます。

```lua
render.set_camera("main:/go#camera", { use_frustum = true })
render.draw(predicates.particle)
render.set_camera()
```

どちらの方法を使った場合も、Particle FX のエミッターは自身の境界に基づいてカリングされます。

エンジンには、コンポーネント（component）の種類ごとに視錐台カリングが実装されています。現在の対応状況は次のとおりです。

| コンポーネント | 対応状況 |
|-------------|-----------|
| スプライト | 対応 |
| モデル | 対応 |
| メッシュ | 対応 (1) |
| ラベル | 対応 |
| Spine | 対応 |
| パーティクルエフェクト | 対応 |
| タイルマップ | 対応 |
| Rive | 未対応 |

1 = メッシュのバウンディングボックスは、開発者が設定する必要があります。[詳しくはこちら](/manuals/mesh/#frustum-culling)を参照してください。


::: sidenote
Defold 1.13.0 以降、コンポーネントのプリミティブでは頂点が反時計回りに並び、プリミティブの法線はカメラの方向を向きます。スプライト、GUI ノード、タイルマップ（タイルグリッド）、Particle FX は、ほかのコンポーネントの種類と同じ頂点順序を使うため、すべてのコンポーネントに同じフェイスカリング設定を使えます。

これは、モデル以外のコンポーネントにフェイスカリングを設定しているプロジェクトに影響する可能性があります。コンポーネントが予期せずカリングされる場合は、`render.set_cull_face(graphics.FACE_TYPE_BACK)` で背面が選択されていることを確認するか、`render.set_cull_face()` の呼び出しを削除して、デフォルトの `graphics.FACE_TYPE_BACK` モードを使ってください。
:::

## 座標系 {#coordinate-systems}

コンポーネントの描画について説明する際は、通常、どの座標系で描画するかを取り上げます。ほとんどのゲームでは、一部のコンポーネントをワールド空間（world space）に、ほかのコンポーネントをスクリーン空間（screen space）に描画します。

GUI コンポーネントとそのノードは、通常、スクリーン座標で描画されます。画面の左下隅の座標は (0,0)、右上隅は（画面の幅, 画面の高さ）です。スクリーン座標系がカメラによってオフセットされたり、ほかの形で平行移動されたりすることはありません。そのため、ワールドの描画方法にかかわらず、GUI ノードは常に画面上に描画されます。

ゲームワールドに存在するゲームオブジェクト（game object）が使うスプライト、タイルマップ、その他のコンポーネントは、通常、ワールド座標系で描画されます。レンダースクリプトを変更せず、ビュープロジェクションを変更するカメラコンポーネントも使わない場合、この座標系はスクリーン座標系と同じです。ただし、カメラを追加して移動させるか、ビュープロジェクションを変更すると、2つの座標系は異なるものになります。カメラが移動すると、画面の左下隅の座標は (0, 0) からオフセットされ、ワールドの別の部分が描画されます。投影を変更すると、座標は平行移動（つまり 0, 0 からオフセット）されるとともに、スケール係数によって変更されます。


## レンダースクリプト {#the-render-script}

以下は、組み込みのレンダースクリプトを少し変更したカスタムレンダースクリプトのコードです。

init()
: `init()` 関数は、述語、ビュー、クリアカラーを設定するために使います。これらの変数は、実際のレンダリングで使われます。

```lua
function init(self)
    -- Define the render predicates. Each predicate is drawn by itself and
    -- that allows us to change the state of OpenGL between the draws.
    self.predicates = create_predicates("tile", "gui", "text", "particle", "model")

    -- Create and fill data tables will be used in update()
    local state = create_state()
    self.state = state
    local camera_world = create_camera(state, "camera_world", true)
    init_camera(camera_world, get_stretch_projection)
    local camera_gui = create_camera(state, "camera_gui")
    init_camera(camera_gui, get_gui_projection)
    update_state(state)
end
```

update()
: `update()` 関数は、毎フレーム1回呼び出されます。その役割は、基盤となる OpenGL ES API（OpenGL Embedded Systems API）を呼び出して実際の描画を行うことです。`update()` 関数の処理を正しく理解するには、OpenGL の仕組みを理解する必要があります。OpenGL ES については、優れた資料が数多くあります。最初に読む資料として公式サイトが適しています。https://www.khronos.org/opengles/ にあります。

  この例には、3D モデルの描画に必要な設定が含まれています。`init()` 関数で `self.predicates.model` という述語を定義しています。別の場所には「model」タグを持つマテリアルが作成されており、そのマテリアルを使うモデルコンポーネントもあります。

```lua
function update(self)
    local state = self.state
     if not state.valid then
        if not update_state(state) then
            return
        end
    end

    local predicates = self.predicates
    -- clear screen buffers
    --
    render.set_depth_mask(true)
    render.set_stencil_mask(0xff)
    render.clear(state.clear_buffers)

    local camera_world = state.cameras.camera_world
    render.set_viewport(0, 0, state.window_width, state.window_height)
    render.set_view(camera_world.view)
    render.set_projection(camera_world.proj)


    -- render models
    --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_CULL_FACE)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_depth_mask(true)
    render.draw(predicates.model_pred)
    render.set_depth_mask(false)
    render.disable_state(graphics.STATE_DEPTH_TEST)
    render.disable_state(graphics.STATE_CULL_FACE)

     -- render world (sprites, tilemaps, particles etc)
     --
    render.set_blend_func(graphics.BLEND_FACTOR_SRC_ALPHA, graphics.BLEND_FACTOR_ONE_MINUS_SRC_ALPHA)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.enable_state(graphics.STATE_BLEND)
    render.draw(predicates.tile)
    render.draw(predicates.particle)
    render.disable_state(graphics.STATE_STENCIL_TEST)
    render.disable_state(graphics.STATE_DEPTH_TEST)

    -- debug
    render.draw_debug3d()

    -- render GUI
    --
    local camera_gui = state.cameras.camera_gui
    render.set_view(camera_gui.view)
    render.set_projection(camera_gui.proj)
    render.enable_state(graphics.STATE_STENCIL_TEST)
    render.draw(predicates.gui, camera_gui.frustum)
    render.draw(predicates.text, camera_gui.frustum)
    render.disable_state(graphics.STATE_STENCIL_TEST)
end
```

ここまでは、単純で分かりやすいレンダースクリプトです。毎フレーム、同じ方法で描画します。ただし、レンダースクリプトに状態を持たせ、その状態に応じて異なる処理を実行したい場合もあります。また、ゲームコードのほかの部分からレンダースクリプトと通信したい場合もあります。

on_message()
: レンダースクリプトには `on_message()` 関数を定義でき、ゲームやアプリのほかの部分からメッセージを受信できます。外部のコンポーネントがレンダースクリプトに情報を送る一般的な例が、_カメラ_ です。カメラフォーカスを取得したカメラコンポーネントは、毎フレーム、自身のビューと投影をレンダースクリプトに自動的に送信します。このメッセージの名前は `"set_view_projection"` です。

```lua
local MSG_CLEAR_COLOR =         hash("clear_color")
local MSG_WINDOW_RESIZED =      hash("window_resized")
local MSG_SET_VIEW_PROJ =       hash("set_view_projection")

function on_message(self, message_id, message)
    if message_id == MSG_CLEAR_COLOR then
        -- Someone sent us a new clear color to be used.
        update_clear_color(state, message.color)
    elseif message_id == MSG_SET_VIEW_PROJ then
        -- The camera component that has camera focus will sent set_view_projection
        -- messages to the @render socket. We can use the camera information to
        -- set view (and possibly projection) of the rendering.
        camera.view = message.view
        self.camera_projection = message.projection or vmath.matrix4()
        update_camera(camera, state)
    end
end
```

ただし、どのスクリプトや GUI スクリプトからでも、特別な `@render` ソケットを通じてレンダースクリプトにメッセージを送信できます。

```lua
-- Change the clear color.
msg.post("@render:", "clear_color", { color = vmath.vector4(0.3, 0.4, 0.5, 0) })
```

## レンダーリソース {#render-resources}
特定のエンジンリソースをレンダースクリプトに渡すには、プロジェクトに割り当てられた `.render` ファイルの `Render Resources` テーブルに追加します。

![レンダーリソース](images/render/render_resources.png)

これらのリソースをレンダースクリプトで使う例です。

```lua
-- "my_material" will now be used for all draw calls associated with the predicate
render.enable_material("my_material")
-- anything drawn by the predicate will end up in "my_render_target"
render.set_render_target("my_render_target")
render.draw(self.my_full_screen_predicate)
render.set_render_target(render.RENDER_TARGET_DEFAULT)
render.disable_material()

-- bind the render target result texture to whatever is getting rendered via the predicate
render.enable_texture(0, "my_render_target", graphics.BUFFER_TYPE_COLOR0_BIT)
render.draw(self.my_tile_predicate)
```

::: sidenote
現在、Defold が参照可能なレンダーリソースとして対応しているのは `Materials` と `Render Targets` のみですが、今後はこの仕組みで対応するリソースの種類が増える予定です。
:::

## テクスチャハンドル {#texture-handles}

Defold のテクスチャ（texture）は、内部ではハンドル（handle）で表されます。ハンドルは実質的には数値で、エンジン内のどこでもテクスチャオブジェクトを一意に識別するためのものです。つまり、レンダリングシステムとゲームオブジェクトのスクリプトとの間でこのハンドルを渡すことで、ゲームオブジェクト側とレンダリング側をつなぐことができます。たとえば、ゲームオブジェクトに割り当てられたスクリプトでテクスチャを動的に作成してレンダラーに送り、描画コマンドでグローバルテクスチャとして使えます。

`.script` ファイル内では、次のようにします。

```lua
local my_texture_resource = resource.create_texture("/my_texture.texture", tparams)
-- note: my_texture_resource is a hash to the resource path, which can't be used as a handle!
local my_texture_handle = resource.get_texture_info(my_texture_resource)
-- my_texture_handle contains information about the texture, such as width, height and so on
-- it does also contain the handle, which is what we are after
msg.post("@render:", "set_texture", { handle = my_texture_handle.handle })
```

`.render_script` ファイル内では、次のようにします。

```lua
function on_message(self, message_id, message)
    if message_id == hash("set_texture") then
        self.my_texture = message.handle
    end
end

function update(self)
    -- bind the custom texture to the draw state
    render.enable_texture(0, self.my_texture)
    -- do drawing..
end
```

::: sidenote
現在、リソースが参照するテクスチャを変更する方法はありません。このようにハンドルを直接使えるのは、レンダースクリプト内だけです。
:::

## 対応するグラフィックス API {#supported-graphics-apis}
Defold のレンダースクリプト API は、描画操作を次のグラフィックス API に変換します。

:[Graphics API](../shared/graphics-api.md)


## システムメッセージ {#system-messages}

`"set_view_projection"`
: このメッセージは、カメラフォーカスを取得したカメラコンポーネントから送信されます。

`"window_resized"`
: ウィンドウのサイズが変わると、エンジンがこのメッセージを送信します。このメッセージを受信することで、対象のウィンドウサイズが変わったときにレンダリングを変更できます。デスクトップでは実際のゲームウィンドウのサイズが変更されたことを意味し、モバイルデバイスでは画面の向きが変わるたびにこのメッセージが送信されます。

```lua
local MSG_WINDOW_RESIZED =      hash("window_resized")

function on_message(self, message_id, message)
  if message_id == MSG_WINDOW_RESIZED then
    -- The window was resized. message.width and message.height contain the new dimensions.
    ...
  end
end
```

`"draw_line"`
: デバッグ用の線を描画します。`ray_casts`、ベクトルなどの可視化に使います。線は `render.draw_debug3d()` の呼び出しで描画されます。

```lua
-- draw a white line
local p1 = vmath.vector3(0, 0, 0)
local p2 = vmath.vector3(1000, 1000, 0)
local col = vmath.vector4(1, 1, 1, 1)
msg.post("@render:", "draw_line", { start_point = p1, end_point = p2, color = col } )  
```

`"draw_text"`
: デバッグ用のテキストを描画します。デバッグ情報の表示に使います。テキストは、組み込みの `always_on_top.font` フォントで描画されます。このシステムフォントには `debug_text` タグを持つマテリアルが割り当てられており、デフォルトのレンダースクリプトではほかのテキストとともに描画されます。

```lua
-- draw a text message
local pos = vmath.vector3(500, 500, 0)
msg.post("@render:", "draw_text", { text = "Hello world!", position = pos })  
```

`@system` ソケットに `"toggle_profile"` メッセージを送信して表示するビジュアルプロファイラーは、スクリプトで制御可能なレンダラーには含まれません。レンダースクリプトとは別に描画されます。


## ドローコールとバッチ処理 {#draw-calls-and-batching}

ドローコールとは、テクスチャとマテリアルを使い、必要に応じて追加の設定を行って、画面にオブジェクトを描画するよう GPU を準備する処理を指す用語です。この処理は通常、多くのリソースを必要とするため、ドローコールの回数をできるだけ少なくすることをお勧めします。[組み込みのプロファイラー](/manuals/profiling/)を使うと、ドローコールの回数と、それらの描画にかかる時間を測定できます。

Defold は、以下の規則に従って描画操作をバッチ処理（batching）し、ドローコールの回数を減らそうとします。規則は、GUI コンポーネントと、それ以外のすべてのコンポーネントの種類とで異なります。


### GUI 以外のコンポーネントのバッチ処理規則 {#batch-rules-for-non-gui-components}

各 `render.draw()` 呼び出しは、条件に一致する描画項目のうち、ワールドの描画順序が適用される項目のソート方法を制御します。デフォルトは `render.SORT_BACK_TO_FRONT` です。近くから遠くへ描画するには `render.SORT_FRONT_TO_BACK` を使い、追加された順序を保つには `render.SORT_NONE` を使います。

```lua
render.draw(self.opaque_predicate, {
    sort_order = render.SORT_FRONT_TO_BACK
})
render.draw(self.transparent_predicate, {
    sort_order = render.SORT_BACK_TO_FRONT
})
```

選択した順序によって、どの描画項目が隣り合うかが決まるため、バッチ処理に影響する可能性があります。この順序付きリストでは、以下の条件を満たす各オブジェクトが、直前のオブジェクトと同じドローコールにまとめられます。

* 同じコレクションプロキシ（collection proxy）に属する
* コンポーネントの種類が同じである（スプライト、パーティクルエフェクト、タイルマップなど）
* 同じテクスチャを使っている（アトラス（atlas）またはタイルソース（tile source））
* 同じマテリアルを持つ
* 同じシェーダー定数（shader constant）を持つ（色調など）

つまり、同じコレクションプロキシ内の2つのスプライトコンポーネントが、選択した順序でソートされた後に隣り合っていて、同じテクスチャ、マテリアル、定数を使っている場合、それらは同じドローコールにまとめられます。


### GUI コンポーネントのバッチ処理規則 {#batch-rules-for-gui-components}

GUI コンポーネント内のノードは、ノードリストの上から下へ順に描画されます。リスト内の各ノードは、以下の条件を満たす場合、直前のノードと同じドローコールにまとめられます。

* 種類が同じである（ボックス、テキスト、パイなど）
* 同じテクスチャを使っている（アトラスまたはタイルソース）
* 同じブレンドモードを持つ。
* 同じフォントを持つ（テキストノードのみ）
* 同じステンシル設定を持つ

::: sidenote
ノードの描画はコンポーネントごとに行われます。つまり、異なる GUI コンポーネントのノードがバッチ処理されることはありません。
:::

ノードを階層に配置できるため、管理しやすい単位にまとめるのは簡単です。ただし、階層内に異なる種類のノードを混在させると、バッチ描画が分断されることがあります。GUI レイヤーを使うと、ノード階層を維持しながら GUI ノードをより効率的にバッチ処理できます。GUI レイヤーと、それがドローコールに与える影響について詳しくは、[GUI マニュアル](/manuals/gui#layers-and-draw-calls)を参照してください。
