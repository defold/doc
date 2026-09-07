---
title: Defold マテリアルマニュアル
brief: このマニュアルでは、マテリアル、シェーダー定数、サンプラーの使い方を説明します。
---

# マテリアル {#materials}

マテリアル（material）は、スプライト、タイルマップ、フォント、GUI ノード、モデルなど、グラフィックスを扱うコンポーネント（component）の描画方法を指定するために使います。

マテリアルには、描画するオブジェクトをレンダリングパイプライン（rendering pipeline）で選択するための情報である _タグ（tag）_ が含まれます。また、_シェーダープログラム（shader program）_ への参照も含まれます。シェーダープログラムは、利用可能なグラフィックスドライバーを通じてコンパイルされ、グラフィックスハードウェアにアップロードされます。そして、各フレームでコンポーネントが描画されるときに実行されます。

* レンダリングパイプラインについて詳しくは、[レンダリングのドキュメント](/manuals/render)を参照してください。
* シェーダープログラムについて詳しくは、[シェーダーのドキュメント](/manuals/shader)を参照してください。

## マテリアルの作成 {#creating-a-material}

マテリアルを作成するには、*Assets* ブラウザーで対象のフォルダーを<kbd>右クリック</kbd>し、<kbd>New... ▸ Material</kbd> を選択します（メニューから <kbd>File ▸ New...</kbd> を選択し、続いて <kbd>Material</kbd> を選択することもできます）。新しいマテリアルファイルに名前を付け、<kbd>Ok</kbd> を押します。

![マテリアルファイル](images/materials/material_file.png)

新しいマテリアルが *Material Editor* で開きます。

![マテリアルエディター](images/materials/material.png)

マテリアルファイルには、次の情報が含まれます。

Name
: マテリアルを識別する名前です。この名前は、マテリアルをビルドに含めるために *Render* リソースに登録するときに使います。また、レンダー API 関数 `render.enable_material()` でも使います。名前は一意にすることを推奨します。

Vertex Program
: マテリアルを使って描画するときに使用する頂点シェーダー（vertex shader）のプログラムファイル（*`.vp`*）です。頂点シェーダープログラムは、コンポーネントのプリミティブの各頂点に対して GPU 上で実行されます。各頂点のスクリーン座標を計算し、必要に応じて「varying」変数も出力します。これらの変数は補間され、フラグメントプログラムに入力されます。

Fragment Program
: マテリアルを使って描画するときに使用するフラグメントシェーダー（fragment shader）のプログラムファイル（*`.fp`*）です。このプログラムは、プリミティブの各フラグメント（ピクセル）に対して GPU 上で実行され、各フラグメントの色を決定します。通常は、テクスチャ（texture）の参照と、入力変数（varying 変数または定数）に基づく計算によって色を決めます。

Vertex Constants
: 頂点シェーダープログラムに渡すユニフォーム（uniform）です。使用できる定数の一覧は後述します。

Fragment Constants
: フラグメントシェーダープログラムに渡すユニフォームです。使用できる定数の一覧は後述します。

Samplers
: 必要に応じて、マテリアルファイルで個々のサンプラー（sampler）を設定できます。サンプラーを追加し、シェーダープログラムで使う名前に合わせて名前を付け、ラップとフィルターを必要に応じて設定します。

Tags
: マテリアルに関連付けるタグです。エンジン内ではタグを _ビットマスク_ として表し、[`render.predicate()`](/ref/render#render.predicate) がこれを使って一緒に描画するコンポーネントを集めます。方法については、[レンダリングのドキュメント](/manuals/render)を参照してください。1つのプロジェクトで使用できるタグの最大数は32です。

## 属性 {#attributes}

シェーダー属性（頂点ストリーム、または頂点属性（vertex attribute）とも呼びます）は、GPU がジオメトリを描画するためにメモリから頂点を取得する仕組みです。頂点シェーダーは `attribute` キーワードを使ってストリームの集合を指定します。ほとんどの場合、Defold はストリーム名に基づいて内部でデータを自動的に生成し、バインドします。ただし、エンジンが生成しない特定のエフェクトを実現するために、頂点ごとに追加のデータを渡したい場合もあります。頂点属性は、次のフィールドで設定できます。

Name
: 属性名です。シェーダー定数（shader constant）と同様に、この属性の設定は、頂点プログラムで指定した属性と名前が一致する場合にだけ使われます。

Semantic type
: セマンティック型（semantic type）は、その属性が*何を*表すか、エディターで*どのように*表示するか、またはその両方を示します。たとえば、属性に `SEMANTIC_TYPE_COLOR` を指定すると、エディターにカラーピッカーが表示されますが、データはエンジンからシェーダーにそのまま渡されます。

  - `SEMANTIC_TYPE_NONE` 既定のセマンティック型です。その属性のマテリアルデータを頂点バッファーに直接渡す以外に、属性への影響はありません（既定値）。
  - `SEMANTIC_TYPE_POSITION` 属性用に頂点ごとの位置データを生成します。座標空間と組み合わせて、位置の計算方法をエンジンに指定できます。
  - `SEMANTIC_TYPE_TEXCOORD` 属性用に頂点ごとのテクスチャ座標を生成します。
  - `SEMANTIC_TYPE_PAGE_INDEX` 属性用に頂点ごとのページインデックスを生成します。
  - `SEMANTIC_TYPE_COLOR` エディターによる属性の解釈に影響します。属性に色のセマンティック型を設定すると、インスペクターにカラーピッカーウィジェットが表示されます。
  - `SEMANTIC_TYPE_NORMAL` 属性用に頂点ごとの法線データを生成します。
  - `SEMANTIC_TYPE_TANGENT` 属性用に頂点ごとの接線データを生成します。
  - `SEMANTIC_TYPE_WORLD_MATRIX` 属性用に頂点ごとのワールド行列データを生成します。
  - `SEMANTIC_TYPE_NORMAL_MATRIX` 属性用に頂点ごとの法線行列データを生成します。
  - `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D` 属性用に頂点ごとの 3x3 テクスチャ変換行列を生成します。パーティクルコンポーネントでは、コンポーネントの画像プロパティに対応するアトラス（atlas）空間へ座標を変換する行列をエンジンが提供します。スプライトコンポーネントでは、コンポーネントが使用する各画像に対応する行列をエンジンが提供します（マルチテクスチャリングを使う場合）。モデルコンポーネントでは、単位行列が提供されます。

Data type
: 属性の元データのデータ型です。

  - `TYPE_BYTE` 符号付き8ビットの byte 値です。
  - `TYPE_UNSIGNED_BYTE` 符号なし8ビットの byte 値です。
  - `TYPE_SHORT` 符号付き16ビットの short 値です。
  - `TYPE_UNSIGNED_SHORT` 符号なし16ビットの short 値です。
  - `TYPE_INT` 符号付き整数値です。
  - `TYPE_UNSIGNED_INT` 符号なし整数値です。
  - `TYPE_FLOAT` 浮動小数点数値です（既定値）。

Normalize
: true の場合、GPU ドライバーが属性値を正規化します。これは、完全な精度は必要ないものの、具体的な範囲の上限や下限を意識せずに計算したい場合に役立ちます。たとえば、色のベクトルは通常、0..255 の byte 値で十分ですが、シェーダーでは 0..1 の値として扱えます。

Coordinate space
: セマンティック型によっては、異なる座標空間のデータを渡せます。スプライトでビルボードエフェクトを実装する場合、通常はローカル空間の位置属性に加え、バッチ処理の効率を最大限に高めるために、すべての変換を適用したワールド空間の位置が必要になります。

Vector type
: 属性のベクトル型です。

  - `VECTOR_TYPE_SCALAR` 単一のスカラー値です。
  - `VECTOR_TYPE_VEC2` 2D ベクトルです。
  - `VECTOR_TYPE_VEC3` 3D ベクトルです。
  - `VECTOR_TYPE_VEC4` 4D ベクトルです（既定値）。
  - `VECTOR_TYPE_MAT2` 2D 行列です。
  - `VECTOR_TYPE_MAT3` 3D 行列です。
  - `VECTOR_TYPE_MAT4` 4D 行列です。

Step function
: 頂点関数に属性データをどのように渡すかを指定します。これはインスタンシング（instancing）にのみ関係します。

  - `Vertex` 頂点ごとに1回渡します。たとえば、位置属性は通常、メッシュ内の頂点ごとに頂点関数へ渡されます（既定値）。
  - `Instance` インスタンスごとに1回渡します。たとえば、ワールド行列の属性は通常、インスタンスごとに1回、頂点関数へ渡されます。

Value
: 属性の値です。属性値はコンポーネントごとに上書きできますが、上書きしない場合はこの値が頂点属性の既定値になります。注: *既定の*属性（位置、テクスチャ座標、ページインデックス）では、この値は無視されます。

::: sidenote
カスタム属性を使い、より小さいデータ型や異なる要素数を使うようにストリームを再設定すると、CPU と GPU の両方でメモリ占有量を減らすこともできます。
:::

### 既定の属性セマンティクス {#default-attribute-semantics}

マテリアルシステムは、実行時に、特定の属性名に基づいて既定のセマンティック型を自動的に割り当てます。

  - `position` - セマンティック型: `SEMANTIC_TYPE_POSITION`
  - `texcoord0` - セマンティック型: `SEMANTIC_TYPE_TEXCOORD`
  - `texcoord1` - セマンティック型: `SEMANTIC_TYPE_TEXCOORD`
  - `page_index` - セマンティック型: `SEMANTIC_TYPE_PAGE_INDEX`
  - `color` - セマンティック型: `SEMANTIC_TYPE_COLOR`
  - `normal` - セマンティック型: `SEMANTIC_TYPE_NORMAL`
  - `tangent` - セマンティック型: `SEMANTIC_TYPE_TANGENT`
  - `mtx_world` - セマンティック型: `SEMANTIC_TYPE_WORLD_MATRIX`
  - `mtx_normal` - セマンティック型: `SEMANTIC_TYPE_NORMAL_MATRIX`
  - `mtx_texture_transform_2d` - セマンティック型: `SEMANTIC_TYPE_TEXTURE_TRANSFORM_2D`

これらの属性の項目がマテリアルにある場合、既定のセマンティック型は、マテリアルエディターで設定した内容で上書きされます。

### カスタム頂点属性データの設定 {#setting-custom-vertex-attribute-data}

ユーザー定義のシェーダー定数と同様に、`go.get`、`go.set`、`go.animate` を呼び出して、実行時に頂点属性を更新することもできます。

![カスタムマテリアル属性](images/materials/set_custom_attribute.png)

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

ただし、頂点属性の更新にはいくつか注意点があります。コンポーネントがその値を使えるかどうかは、属性のセマンティック型によって異なります。たとえば、スプライトコンポーネントは `SEMANTIC_TYPE_POSITION` をサポートしていますが、このセマンティック型を持つ属性を更新しても、コンポーネントは上書きした値を無視します。このセマンティック型では、データを常にスプライトの位置から生成するように定められているためです。

モデルコンポーネントでも、`go.get()`、`go.set()`、`go.animate()` を通じてカスタムマテリアル属性にアクセスできます。たとえば、モデルのマテリアルに `my_attribute` という名前の属性を定義すると、次のように使えます。

```lua
go.set("#model", "my_attribute", vmath.vector4(1, 0, 0, 1))
go.animate("#model", "my_attribute", go.PLAYBACK_LOOP_PINGPONG,
    vmath.vector4(0, 1, 0, 1), go.EASING_LINEAR, 2)
```

現在、複数のメッシュを持つモデルでこの方法によりアクセスできるのは、最初のメッシュだけです。また、インスタンシングされていない頂点ごとの属性を更新すると、メッシュのサイズに比例する量の頂点データが再構築され、アップロードされることがあります。そのため、大きなメッシュを頻繁に更新すると、処理負荷が高くなる場合があります。

頂点属性がスカラー型、または `Vec4` 以外のベクトル型の場合でも、`go.set` を使ってデータを設定できます。

```lua
-- The last two components in the vec4 will not be used!
go.set("#sprite", "sprite_position_2d", vmath.vector4(my_x,my_y,0,0))
go.animate("#sprite", "sprite_position_2d", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,2,0,0), go.EASING_LINEAR, 2)
```

行列属性でも同様に、属性が `Mat4` 以外の行列型であっても、`go.set` を使ってデータを設定できます。

### カスタム頂点属性の使用例 {#examples-of-using-custom-vertex-attributes}

テクスチャ変換属性を使って、UV 座標をアトラス空間に変換する例です。

```glsl
#version 140

in vec3 position;
in vec4 texcoord0;
in mat3 texture_transform_2d;

out vec2 var_texcoord0;

void main()
{
  // Extract position from the transform
  vec2 atlas_pos = texture_transform_2d[2].xy;
  // Extract the scale from the transform
  vec2 atlas_size = vec2(
      length(texture_transform_2d[0].xy),
      length(texture_transform_2d[1].xy)
  );
  // convert to local UV (0..1)
  vec2 localUV = (texcoord0 - atlas_pos) / atlas_size;

  // Alternatively, if the UV coordinates already are in the 0..1 range,
  // you can transform into atlas space directly by multiplying the transform:
  vec2 transformedUv = texture_transform_2d * texcoord0;

  // Pass the value into the fragment shader
  var_texcoord0 = localUV;

  // ... rest of vertex shader
}
```

### インスタンシング {#instancing}

インスタンシングは、シーン内で同じオブジェクトのコピーを複数、効率よく描画する手法です。オブジェクトを使うたびに別々のコピーを作成する代わりに、グラフィックスエンジンが1つのオブジェクトを作成して、何度も再利用できるようにします。たとえば、大きな森のあるゲームでは、木ごとに個別のモデルを作成する代わりに、インスタンシングを使って1つの木のモデルを作成し、位置やスケールを変えて数百回、数千回と配置できます。これにより、木ごとに個別のドローコール（draw call）を発行する代わりに、1回のドローコールで森を描画できます。

::: sidenote
現在、インスタンシングを使用できるのはモデルコンポーネントだけです。
:::

インスタンシングは、使用できる場合に自動的に有効になります。Defold は描画状態をできるだけまとめてバッチ処理する仕組みを重視しており、インスタンシングが機能するには、いくつかの条件を満たす必要があります。

- すべてのインスタンスで同じマテリアルを使う必要があります。`render.enable_material` でカスタムマテリアルを設定した場合でも、インスタンシングは機能します。
- マテリアルの頂点空間を 'local' に設定する必要があります。
- マテリアルには、インスタンスごとに繰り返される頂点属性が少なくとも1つ必要です。
- すべてのインスタンスで定数値が同じである必要があります。代わりに、定数値をカスタム頂点属性に格納するか、別の方法（テクスチャなど）で保持することもできます。
- テクスチャやストレージバッファーなどのシェーダーリソースは、すべてのインスタンスで同じである必要があります。

頂点属性をインスタンスごとに繰り返すように設定するには、`Step function` を `Instance` に設定する必要があります。一部のセマンティック型では、名前に基づいて自動的に設定されます（上記の `Default attribute semantics` の表を参照してください）。また、マテリアルエディターで `Step function` を `Instance` に設定して、手動で指定することもできます。

簡単な例として、次のシーンには、モデルコンポーネントを1つずつ持つ4つのゲームオブジェクト（game object）があります。

![インスタンシングの構成](images/materials/instancing-setup.png)

マテリアルは、インスタンスごとに繰り返される1つのカスタム頂点属性を持つように、次のとおり設定します。

![インスタンシングのマテリアル](images/materials/instancing-material.png)

頂点シェーダーには、インスタンスごとの属性を複数指定します。

```glsl
// Per vertex attributes
attribute highp vec4 position;
attribute mediump vec2 texcoord0;
attribute mediump vec3 normal;

// Per instance attributes
attribute mediump mat4 mtx_world;
attribute mediump mat4 mtx_normal;
attribute mediump vec4 instance_color;
```

`mtx_world` と `mtx_normal` は、既定でステップ関数に `Instance` を使うように設定されます。マテリアルエディターでこれらの項目を追加し、`Step function` を `Vertex` に設定すると、この動作を変更できます。この場合、属性はインスタンスごとではなく、頂点ごとに繰り返されます。

この例でインスタンシングが機能しているかどうかは、ウェブプロファイラーで確認できます。ボックスのインスタンス間で変わるのはインスタンスごとの属性だけなので、1回のドローコールで描画できます。

![インスタンシングのドローコール](images/materials/instancing-draw-calls.png)

#### 後方互換性 {#backwards-compatibility}

デスクトップの OpenGL 3.1 とモバイルの OpenGL ES 3.0 は、インスタンシングをコア機能として提供しています。古い OpenGL ES や WebGL のコンテキストでも、`ANGLE_instanced_arrays` などの拡張機能を通じて対応している場合がありますが、対応していない古いアダプターもあります。インスタンシングを使用できない場合でも、既定では描画は機能しますが、パフォーマンスが低下することがあります。

`graphics.get_adapter_info()` で対応状況を検出し、必要に応じて処理負荷の低いマテリアルを選択するか、インスタンスを大量に使うコンテンツを省きます。`features` フィールドは、サポートされている機能定数の配列であり、それらの定数をキーとするテーブルではありません。

```lua
local function has_context_feature(feature)
    local adapter_info = graphics.get_adapter_info()
    for _, supported_feature in ipairs(adapter_info.features) do
        if supported_feature == feature then
            return true
        end
    end
    return false
end

local instancing_supported = has_context_feature(
    graphics.CONTEXT_FEATURE_INSTANCING
)
```

## 頂点定数とフラグメント定数 {#vertex-and-fragment-constants}

シェーダー定数、つまり「ユニフォーム」は、エンジンから頂点シェーダープログラムとフラグメントシェーダープログラムに渡される値です。定数を使うには、マテリアルファイル内で *Vertex Constant* プロパティまたは *Fragment Constant* プロパティとして定義します。対応する `uniform` 変数をシェーダープログラム内で定義する必要もあります。マテリアルには、次の定数を設定できます。

`CONSTANT_TYPE_WORLD`
: ワールド行列です。頂点をワールド空間に変換するために使います。コンポーネントの種類によっては、バッチ処理のため、頂点プログラムに渡される時点ですでに頂点がワールド空間にあります。この場合、シェーダー内でワールド行列を掛けると、誤った結果になります。

`CONSTANT_TYPE_VIEW`
: ビュー行列です。頂点をビュー（カメラ）空間に変換するために使います。

`CONSTANT_TYPE_PROJECTION`
: 投影行列です。頂点をスクリーン空間に変換するために使います。

`CONSTANT_TYPE_VIEWPROJ`
: ビュー行列と投影行列をあらかじめ乗算した行列です。

`CONSTANT_TYPE_WORLDVIEW`
: ワールド行列とビュー行列をあらかじめ乗算した行列です。

`CONSTANT_TYPE_WORLDVIEWPROJ`
: ワールド行列、ビュー行列、投影行列をあらかじめ乗算した行列です。

`CONSTANT_TYPE_WORLD_INVERSE`
: ワールド行列の逆行列です。ワールド空間からオブジェクトのローカル空間に戻すために使います。

`CONSTANT_TYPE_VIEW_INVERSE`
: ビュー行列の逆行列です。カメラ空間からワールド空間に戻すために使います。

`CONSTANT_TYPE_PROJECTION_INVERSE`
: 投影行列の逆行列です。クリップ空間からカメラ空間に戻すために使います。

`CONSTANT_TYPE_VIEWPROJ_INVERSE`
: ビュー行列と投影行列を合成した行列の逆行列です。クリップ空間からワールド空間に戻すために使います。

`CONSTANT_TYPE_WORLDVIEW_INVERSE`
: ワールド行列とビュー行列を合成した行列の逆行列です。カメラ空間からオブジェクトのローカル空間に戻すために使います。

`CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`
: ワールド行列、ビュー行列、投影行列を合成した行列の逆行列です。クリップ空間からオブジェクトのローカル空間に戻すために使います。これらの逆行列定数を使うと、シェーダー内で逆行列を計算する必要がなくなります。

`CONSTANT_TYPE_NORMAL`
: 法線の向きを計算する行列です。ワールドトランスフォームには不均一な拡大縮小が含まれることがあり、合成したワールドビュートランスフォームの直交性が失われます。法線行列は、法線を変換するときに方向の問題が生じるのを避けるために使います（法線行列は、ワールドビュー行列の逆行列を転置したものです）。

`CONSTANT_TYPE_TIME`
: エンジンが提供する `vector4` です。`.x` はエンジンの起動からの経過時間、`.y` は前フレームからの経過時間を表し、`.z` と `.w` は現在ゼロです。エンジンがこの値を自動的に更新するため、`go.set()` で更新する必要はありません。使用例は、[Shadertoy チュートリアル](/tutorials/shadertoy/#animation)を参照してください。

  モダン GLSL のユニフォームブロックで、`time` という名前の Time 定数を宣言します。

  ```glsl
  uniform fragment_inputs
  {
      vec4 time;
  };
  ```

`CONSTANT_TYPE_USER`
: シェーダープログラムに渡す任意のカスタムデータに使える vector4 定数です。定数の定義で初期値を設定でき、[go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 関数で変更できます。[go.get()](/ref/stable/go/#go.get) で値を取得することもできます。単一のコンポーネントインスタンスのマテリアル定数を変更すると、[バッチ描画が分割され、追加のドローコールが発生します](/manuals/render/#draw-calls-and-batching)。

例:

```lua
go.set("#sprite", "tint", vmath.vector4(1,0,0,1))

go.animate("#sprite", "tint", go.PLAYBACK_LOOP_PINGPONG, vmath.vector4(1,0,0,1), go.EASING_LINEAR, 2)
```

`CONSTANT_TYPE_USER_MATRIX4`
: シェーダープログラムに渡す任意のカスタムデータに使える matrix4 定数です。定数の定義で初期値を設定でき、[go.set()](/ref/stable/go/#go.set) / [go.animate()](/ref/stable/go/#go.animate) 関数で変更できます。[go.get()](/ref/stable/go/#go.get) で値を取得することもできます。単一のコンポーネントインスタンスのマテリアル定数を変更すると、[バッチ描画が分割され、追加のドローコールが発生します](/manuals/render/#draw-calls-and-batching)。

例:

```lua
go.set("#sprite", "m", vmath.matrix4())
```

### GUI ノードのマテリアル定数 {#gui-node-material-constants}

GUI スクリプト内では、`go` 関数の代わりに `gui.get()` と `gui.set()` を使って、ノードのマテリアル定数を読み書きします。ベクトルの成分、行列定数、定数配列がサポートされています。オプションテーブル内の配列インデックスは1から始まります。

```lua
local node = gui.get_node("button")

local tint = gui.get(node, "tint")
gui.set(node, "tint.x", 0.5)
gui.set(node, "light_matrix", vmath.matrix4())
gui.set(node, "tint_array", vmath.vector4(1, 0, 0, 1), { index = 1 })
```

::: sidenote
`CONSTANT_TYPE_USER` 型または `CONSTANT_TYPE_USER_MATRIX4` 型のマテリアル定数を `go.get()` と `go.set()`、または `gui.get()` と `gui.set()` で利用するには、その定数をシェーダープログラム内で使う必要があります。マテリアルで定義されていてもプログラム内で使われていない定数は、マテリアルから削除され、実行時には利用できなくなります。
:::

## サンプラー {#samplers}

サンプラーは、テクスチャ（タイルソース（tile source）またはアトラス）から色情報をサンプリングするために使います。この色情報は、シェーダープログラム内の計算に使えます。

スプライト、タイルマップ、GUI、パーティクルエフェクトのコンポーネントは、それぞれの画像テクスチャを最初に宣言された `sampler2D` に自動的にバインドします。スプライトコンポーネントは複数のテクスチャもサポートしており、マテリアルで宣言したすべてのサンプラーが、スプライトコンポーネント内の名前付き画像スロットになります。最初のテクスチャは、スプライトのアニメーションデータを提供し、フレームのシーケンスを決定します。各フレームの画像 ID を使って、追加の各テクスチャ内で対応する画像を見つけ、それぞれのテクスチャが自身の UV 座標を提供します。そのため、割り当てるアトラスまたはタイルソースには、一致するフレーム ID と、形が似た画像を含めることを推奨します。ポリゴンパッキングされた形状が異なると、テクスチャのにじみが生じることがあります。詳しくは、[複数のテクスチャを使うスプライト](/manuals/sprite/#multi-textured-sprites)を参照してください。

追加のテクスチャスロットを公開しないコンポーネントやレンダリングのワークフローでは、[`render.enable_texture()`](/ref/render/#render.enable_texture) を使って、レンダースクリプト（render script）から追加のテクスチャサンプラーをバインドします。

![スプライトのサンプラー](images/materials/sprite_sampler.png)

```glsl
-- mysprite.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D MY_SAMPLER;
void main()
{
    gl_FragColor = texture2D(MY_SAMPLER, var_texcoord0.xy);
}
```

マテリアルファイルにサンプラーを名前で追加すると、コンポーネントのサンプラー設定を指定できます。マテリアルファイルでサンプラーを設定しない場合は、プロジェクト全体の *graphics* 設定が使われます。

![サンプラー設定](images/materials/my_sampler.png)

モデルコンポーネントでは、マテリアルファイルにサンプラーを指定し、必要な設定を行う必要があります。すると、そのマテリアルを使う任意のモデルコンポーネントに対して、エディターでテクスチャを設定できるようになります。

![モデルのサンプラー](images/materials/model_samplers.png)

```glsl
-- mymodel.fp
varying mediump vec2 var_texcoord0;
uniform lowp sampler2D TEXTURE_1;
uniform lowp sampler2D TEXTURE_2;
void main()
{
    lowp vec4 color1 = texture2D(TEXTURE_1, var_texcoord0.xy);
    lowp vec4 color2 = texture2D(TEXTURE_2, var_texcoord0.xy);
    gl_FragColor = color1 * color2;
}
```

![モデル](images/materials/model.png)

## サンプラー設定 {#sampler-settings}

Name
: サンプラーの名前です。この名前は、フラグメントシェーダーで宣言した `sampler2D` と一致させることを推奨します。

Wrap U/W
: U 軸と V 軸のラップモードです。

  - `WRAP_MODE_REPEAT` は、範囲 [0,1] の外側でテクスチャデータを繰り返します。
  - `WRAP_MODE_MIRRORED_REPEAT` は、範囲 [0,1] の外側でテクスチャデータを繰り返しますが、1回おきに反転します。
  - `WRAP_MODE_CLAMP_TO_EDGE` は、1.0 より大きい値には 1.0 のテクスチャデータを使い、0.0 より小さい値には 0.0 のテクスチャデータを使います。つまり、境界のピクセルが端まで繰り返されます。

Filter Min/Mag
: 拡大と縮小に使うフィルタリングです。最近傍フィルタリングは線形補間より計算量が少ない一方、エイリアシングによる描画の乱れが生じることがあります。線形補間では、より滑らかな結果が得られることが多くなります。

  - `Default` は、`game.project` ファイルの `Graphics` にある `Default Texture Min Filter` と `Default Texture Mag Filter` で指定した既定のフィルターオプションを使います。
  - `FILTER_MODE_NEAREST` は、ピクセルの中心に最も近い座標のテクセルを使います。
  - `FILTER_MODE_LINEAR` は、ピクセルの中心に最も近い 2x2 のテクセル配列の、重み付き線形平均を設定します。
  - `FILTER_MODE_NEAREST_MIPMAP_NEAREST` は、1つのミップマップ内で最も近いテクセルの値を選びます。
  - `FILTER_MODE_NEAREST_MIPMAP_LINEAR` は、最も適した2つの近いミップマップでそれぞれ最も近いテクセルを選択し、その2つの値の間で線形補間します。
  - `FILTER_MODE_LINEAR_MIPMAP_NEAREST` は、1つのミップマップ内で線形補間します。
  - `FILTER_MODE_LINEAR_MIPMAP_LINEAR` は、2つのミップマップそれぞれの値を線形補間で計算し、その2つの値の間でさらに線形補間します。

Max Anisotropy
: 異方性フィルタリングは、複数のサンプルを取得して結果を混ぜ合わせる高度なフィルタリング手法です。この設定は、テクスチャサンプラーの異方性の度合いを制御します。GPU が異方性フィルタリングをサポートしていない場合、このパラメーターは効果を持たず、既定値の1に設定されます。

## 定数バッファー {#constants-buffers}

レンダリングパイプラインは、描画時に、システムの既定の定数バッファー（constants buffer）から定数値を取得します。カスタム定数バッファーを作成して既定の定数を上書きし、代わりにレンダースクリプトのプログラムでシェーダープログラムのユニフォームを設定できます。

```lua
self.constants = render.constant_buffer() -- <1>
self.constants.tint = vmath.vector4(1, 0, 0, 1) -- <2>
...
render.draw(self.my_pred, {constants = self.constants}) -- <3>
```
1. 新しい定数バッファーを作成します。
2. `tint` 定数を鮮やかな赤色に設定します。
3. カスタム定数を使って、レンダー述語に該当する対象を描画します。

バッファー内の定数要素は通常の Lua テーブルと同じように参照しますが、`pairs()` や `ipairs()` でバッファーを反復処理することはできません。
