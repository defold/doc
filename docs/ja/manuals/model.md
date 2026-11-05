---
title: Defold の 3D モデル
brief: このマニュアルでは、3D モデル、スケルトン、アニメーションをゲームに取り込む方法を説明します。
---

# モデルコンポーネント {#model-component}

Defold は基本的に 3D エンジンです。2D 素材だけを扱う場合でも、レンダリングはすべて 3D で行われ、画面には正投影されます。Defold では、3D アセット、つまり _モデル（model）_ をコレクション（collection）に追加することで、完全な 3D コンテンツを利用できます。3D アセットだけを使って完全に 3D のゲームを作成することも、3D と 2D のコンテンツを自由に組み合わせることもできます。

## モデルコンポーネントの作成 {#creating-a-model-component}

モデルコンポーネントは、ほかのゲームオブジェクト（game object）のコンポーネント（component）と同じ方法で作成します。次の2つの方法があります。

- *Assets* ブラウザー内の場所を <kbd>右クリック</kbd> し、<kbd>New... ▸ Model</kbd> を選択して、*モデルファイル* を作成します。
- *Outline* ビューでゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component ▸ Model</kbd> を選択して、ゲームオブジェクトに直接埋め込まれたコンポーネントを作成します。

![ゲームオブジェクト内のモデル](images/model/model_gltf.png)

モデルを作成したら、いくつかのプロパティを指定する必要があります。

### モデルのプロパティ {#model-properties}

*Id*、*Position*、*Rotation* のほかに、次のコンポーネント固有のプロパティがあります。

*Scene*
: モデルのジオメトリを含む glTF の *.gltf* または *.glb* ファイルです。モーフターゲットが含まれている場合は、シーンと一緒にインポートします。このプロパティの以前の名前は *Mesh* でした。

*Mesh*
: 選択した *Scene* 内の、任意の名前付きメッシュです。空にすると、インポートしたトランスフォームを使ってシーン全体を描画します。メッシュを選択すると、glTF ノードのトランスフォームなしに、そのメッシュをローカル座標で1回描画します。選択したメッシュを配置するには、Model コンポーネントまたはゲームオブジェクトの位置、回転、スケールを変更します。

*Create GO Bones*
: チェックを入れると、モデルの各ボーン（bone）に対してゲームオブジェクトが作成されます。これらのゲームオブジェクトを使って、手のボーンに武器などの別のゲームオブジェクトを取り付けることができます。 

*Skeleton*
: このプロパティには、アニメーションに使用するスケルトン（skeleton）を含む glTF *.gltf* または *.glb* ファイルを指定します。Defold では、階層内にルートボーンが1つだけ必要であることに注意してください。

*Animations*
: モデルで使用するアニメーションを含む *Animation Set File* を指定します。

*Default Animation*
: モデルで自動的に再生される、アニメーションセット（animation set）内のアニメーションです。

上記のプロパティに加えて、モデルの各メッシュにマテリアル（material）を割り当てるフィールドもあります。

*Material*
: モデルに適したマテリアルを設定します。glTF マテリアルのプロパティを物理ベースで描画するには組み込みの `gltf` マテリアルを、一般的なモデルのシェーディングには組み込みの `model` マテリアルを使います。独自のカスタムマテリアルも使えます。[以下のマテリアルの種類](#material)と [PBR マニュアル](/manuals/physically-based-rendering/#built-in-pbr-materials)を参照してください。

マテリアルに応じて、1つ以上のテクスチャプロパティがあります。

*Texture*
: オブジェクトに適用するテクスチャ画像を指定します。独立したプロジェクトアセットでも、*Assets* ペインの glTF または GLB ファイル内に公開される埋め込み画像でもかまいません。

glTF または GLB の *Scene* を選択したり、その *Mesh* 選択を変更したりすると、マテリアルとテクスチャの割り当てを提案することがあります。<kbd>Auto Fill</kbd> は既存の割り当てをソースの内容で置き換えます。<kbd>Keep Current</kbd> は、新しいシーンやメッシュの選択を反映しながら、現在の割り当てを保持します。[モデルのインポート手順](/manuals/importing-models/#using-a-model)を参照してください。


## エディターでの操作 {#editor-manipulation}

モデルコンポーネントを配置したら、通常の *Scene Editor* ツールでコンポーネントやそれを含むゲームオブジェクトを自由に編集、操作し、モデルを必要に応じて移動、回転、拡大縮小できます。

## 実行時の操作 {#runtime-manipulation}

さまざまな関数やプロパティを使って、実行時にモデルを操作できます（使い方は [API ドキュメント](/ref/model/)を参照してください）。

![ゲーム内の Wiggler](images/model/runtime.png)

### 実行時のアニメーション {#runtime-animation}

Defold は、実行時にアニメーションを制御するための強力な機能を備えています。詳しくは[モデルアニメーションのマニュアル](/manuals/model-animation)を参照してください。

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

アニメーションの再生カーソルは、手動でもプロパティアニメーションシステムでもアニメーションできます。

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

モデルでは、glTF のモーフターゲットアニメーションも使用できます。モーフターゲットのウェイトは、ほかのモデルアニメーションと同様に `model.play_anim()` でアニメーションし、実行時に [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) と [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) を使って読み取りや上書きができます。詳しくは、モデルアニメーションのマニュアルの[モーフターゲットのセクション](/manuals/model-animation#morph-targets)を参照してください。

### プロパティの変更 {#changing-properties}

モデルには、`go.get()` と `go.set()` で操作できるさまざまなプロパティもあります。

`animation`
: 現在のモデルアニメーション（`hash`）（読み取り専用）です。アニメーションを変更するには `model.play_anim()` を使います（上記を参照）。

`cursor`
: 正規化されたアニメーションカーソル（`number`）です。

`material`
: モデルのマテリアル（`hash`）です。マテリアルのリソースプロパティと `go.set()` を使って変更できます。例については [API リファレンス](/ref/model/#material)を参照してください。

`playback_rate`
: アニメーションの再生速度（`number`）です。

`textureN`
: モデルのテクスチャ（`hash`）です。N は 0-15 です。これらのプロパティは `go.get()` で読み取り、テクスチャのリソースプロパティと `go.set()` を使って変更できます。Defold は1回の描画で最大16個のテクスチャをサポートしますが、テクスチャサンプラーの上限が低いグラフィックスアダプターでは、シェーダーで使用できる数がこれより少ない場合があります。


## マテリアル {#material}

3D ソフトウェアでは通常、オブジェクトの頂点に色やテクスチャなどの属性を設定できます。この情報は、3D ソフトウェアからエクスポートする glTF *.gltf* または *.glb* ファイルに格納されます。ゲームの要件に応じて、オブジェクトに適した _性能の高い_ マテリアルを選択したり作成したりする必要があります。マテリアルは、_シェーダープログラム_ と、オブジェクトのレンダリングに使う一連のパラメーターを組み合わせたものです。

`/builtins/materials/` には、次の組み込みマテリアルがあります。

| モデルの種類 | 一般的なモデルのシェーディング | glTF PBR シェーディング |
|---|---|---|
| 静的、インスタンシングなし | `model.material` | `gltf.material` |
| 静的、インスタンシングあり | `model_instanced.material` | `gltf_instanced.material` |
| スキニング（アニメーション）、インスタンシングなし | `model_skinned.material` | `gltf_skinned.material` |
| スキニング（アニメーション）、インスタンシングあり | `model_skinned_instanced.material` | `gltf_skinned_instanced.material` |

`gltf` マテリアルは、インポートした glTF マテリアルデータを使い、組み込みのメタリック・ラフネスのライティングを提供します。テクスチャの割り当て、ライト、カスタムシェーダーは、[PBR マニュアル](/manuals/physically-based-rendering/#built-in-pbr-materials)を参照してください。

これらの組み込みマテリアルは、すべてローカル頂点空間を使います。スキニング付きモデルでは、ローカル頂点空間を使うことで、頂点シェーダーがボーン行列テクスチャを用いて GPU 上でスキニングを実行できます。モデルのインスタンシングにも、ローカル頂点空間が必要です。そのため、GPU スキニングやインスタンシング用のカスタムマテリアルは、頂点空間を *Local* に設定してください。

ボーン行列キャッシュは `RGBA32F` テクスチャを使用します。使用中のグラフィックスアダプターがこのテクスチャ形式をサポートしていない場合、Defold はローカル空間のマテリアルを使用するアニメーション付きモデルコンポーネントを作成できません。そのため、OpenGL ES 2.0 と WebGL 1.0 では、サポートの有無はアダプターの浮動小数点テクスチャ拡張に依存します。この拡張を持たないアダプターとの互換性を確保するには、ワールド空間のカスタムマテリアルを使います。このマテリアルは CPU スキニングを使用し、モデルのインスタンシングは使用できません。キャッシュの寸法は、[Model のプロジェクト設定](/manuals/project-settings/#model)で調整できます。

モデル用のカスタムマテリアルを作成する必要がある場合は、[マテリアルのドキュメント](/manuals/material)を参照してください。[シェーダーのマニュアル](/manuals/shader)では、シェーダープログラムの仕組みを説明しています。


### マテリアル定数 {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: モデルの色調（`vector4`）です。`vector4` を使って色調を表し、x、y、z、w はそれぞれ赤、緑、青、アルファの色調に対応します。


## レンダリング {#rendering}

デフォルトのレンダースクリプトは、組み込みの model と glTF マテリアルを含め、`model` タグのあるマテリアルを描画します。カスタムレンダースクリプトでは、一致する述語を作成し、シーンに適したビューと射影で描画します。例:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

レンダースクリプトの仕組みについて詳しくは、[レンダリングのドキュメント](/manuals/render)を参照してください。
