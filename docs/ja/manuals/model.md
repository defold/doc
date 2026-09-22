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
: モデルのジオメトリを含む glTF *.gltf* または *.glb* ファイルです。ファイルにモーフターゲット（morph target）が含まれている場合は、シーンとともにインポートされます。Defold 1.13.2 より前では、このプロパティの名前は *Mesh* でした。

*Mesh*
: 選択した *Scene* 内の、省略可能な名前付きメッシュ（mesh）です。Defold 1.13.2 以降で利用できます。このフィールドを空にすると、インポートしたトランスフォームでシーン全体を描画します。メッシュを選択すると、glTF ノードのトランスフォームを適用せず、ローカル座標でそのメッシュを1回描画します。選択したメッシュを配置するには、モデルコンポーネントまたはそのゲームオブジェクトの位置、回転、スケールを調整します。

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
: このプロパティには、テクスチャを持つ 3D オブジェクトに適した、自分で作成したマテリアルを指定します。出発点として利用できる組み込みマテリアルがいくつかあります。

  * インスタンシングを使用しない静的モデルには *model.material* を使います。
  * インスタンシングを使用する静的モデルには *model_instanced.material* を使います。
  * インスタンシングを使用しないスキニングされた（アニメーションする）モデルには *model_skinned.material* を使います。
  * インスタンシングを使用するスキニングされた（アニメーションする）モデルには *model_skinned_instanced.material* を使います。

マテリアルに応じて、1つ以上のテクスチャプロパティがあります。

*Texture*
: このプロパティには、オブジェクトに適用するテクスチャ画像ファイルを指定します。


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

出発点として利用できる組み込みマテリアルがいくつかあります。

  * インスタンシングを使用しない静的モデルには *model.material* を使います。
  * インスタンシングを使用する静的モデルには *model_instanced.material* を使います。
  * インスタンシングを使用しないスキニングされた（アニメーションする）モデルには *model_skinned.material* を使います。
  * インスタンシングを使用するスキニングされた（アニメーションする）モデルには *model_skinned_instanced.material* を使います。

組み込みのモデルマテリアルは、頂点空間にローカル空間を使用します。スキニングされたモデルでは、頂点空間をローカル空間にすることで、頂点シェーダーがボーン行列テクスチャを使って GPU 上でスキニングを実行できます。また、モデルのインスタンシングにもローカル頂点空間が必要です。そのため、GPU でスキニングするモデルやインスタンシングするモデル用のカスタムマテリアルでは、頂点空間の設定に *Local* を使用することをお勧めします。

ボーン行列キャッシュは `RGBA32F` テクスチャを使用します。使用中のグラフィックスアダプターがこのテクスチャ形式をサポートしていない場合、Defold はローカル空間のマテリアルを使用するアニメーション付きモデルコンポーネントを作成できません。そのため、OpenGL ES 2.0 と WebGL 1.0 では、サポートの有無はアダプターの浮動小数点テクスチャ拡張に依存します。この拡張を持たないアダプターとの互換性を確保するには、ワールド空間のカスタムマテリアルを使います。このマテリアルは CPU スキニングを使用し、モデルのインスタンシングは使用できません。キャッシュの寸法は、[Model のプロジェクト設定](/manuals/project-settings/#model)で調整できます。

モデル用のカスタムマテリアルを作成する必要がある場合は、[マテリアルのドキュメント](/manuals/material)を参照してください。[シェーダーのマニュアル](/manuals/shader)では、シェーダープログラムの仕組みを説明しています。


### マテリアル定数 {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: モデルの色調（`vector4`）です。`vector4` を使って色調を表し、x、y、z、w はそれぞれ赤、緑、青、アルファの色調に対応します。


## レンダリング {#rendering}

デフォルトのレンダースクリプト（render script）は 2D ゲーム向けに作られており、3D モデルでは動作しません。ただし、デフォルトのレンダースクリプトをコピーして数行のコードを追加すれば、モデルをレンダリングできるようになります。たとえば、次のようにします。

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
