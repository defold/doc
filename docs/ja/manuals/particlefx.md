---
title: Defold のパーティクルエフェクト
brief: このマニュアルでは、パーティクルエフェクトコンポーネントの仕組みと、視覚的なパーティクルエフェクトを作成するための編集方法を説明します。
---

# パーティクルエフェクト {#particle-fx}

パーティクルエフェクト（particle effect）は、ゲームの視覚表現を豊かにするために使います。爆発、血しぶき、軌跡、天候など、さまざまなエフェクトを作成できます。

![ParticleFX エディター](images/particlefx/editor.png)

パーティクルエフェクトは、いくつかのエミッター（emitter）と、必要に応じてモディファイアー（modifier）で構成されます。

エミッター
: エミッターは、位置を持つ形状で、その形状全体に均等に分布するパーティクルを放出します。エミッターには、パーティクルの生成に加え、個々のパーティクルの画像やアニメーション、寿命、色、形状、速度を制御するプロパティがあります。

モディファイアー
: モディファイアーは、生成されたパーティクルの速度に影響を与え、特定の方向に加速または減速させたり、放射状に移動させたり、ある点の周りで渦を巻くように動かしたりします。モディファイアーは、1つのエミッターのパーティクル、または特定のエミッターに影響を与えられます。

## エフェクトの作成 {#creating-an-effect}

*Assets* ブラウザーのコンテキストメニューから <kbd>New... ▸ Particle FX</kbd> を選択します。新しいパーティクルエフェクトファイルに名前を付けます。エディターは [シーンエディター](/manuals/editor/#the-scene-editor)でファイルを開きます。

*Outline* ペインには、デフォルトのエミッターが表示されます。エミッターを選択すると、下の *Properties* ペインにプロパティが表示されます。

![デフォルトのパーティクル](images/particlefx/default.png)

エフェクトに新しいエミッターを追加するには、*Outline* のルートを <kbd>右クリック</kbd> し、コンテキストメニューから <kbd>Add Emitter ▸ [type]</kbd> を選択します。エミッターの種類は、エミッターのプロパティで変更できます。

新しいモディファイアーを追加するには、*Outline* でモディファイアーを配置する場所（エフェクトのルートまたは特定のエミッター）を <kbd>右クリック</kbd> し、<kbd>Add Modifier</kbd> を選択してから、モディファイアーの種類を選択します。

![モディファイアーの追加](images/particlefx/add_modifier.png)

![追加するモディファイアーの選択](images/particlefx/add_modifier_select.png)

エフェクトのルートにある（エミッターの子ではない）モディファイアーは、エフェクト内のすべてのパーティクルに影響を与えます。

エミッターの子として追加したモディファイアーは、そのエミッターだけに影響を与えます。

## エフェクトのプレビュー {#previewing-an-effect}

* メニューから <kbd>View ▸ Play</kbd> を選択して、エフェクトをプレビューします。エフェクトを適切に表示するには、カメラをズームアウトする必要がある場合があります。
* もう一度 <kbd>View ▸ Play</kbd> を選択すると、エフェクトが一時停止します。
* <kbd>View ▸ Stop</kbd> を選択すると、エフェクトが停止します。再度再生すると、初期状態から再開します。

エミッターやモディファイアーを編集すると、エフェクトを一時停止していても、その結果がすぐにエディターに表示されます。

![パーティクルの編集](images/particlefx/rotate.gif)

## エミッターのプロパティ {#emitter-properties}

Id
: エミッターの識別子です（特定のエミッターにレンダー定数を設定するときに使います）。

Position/Rotation
: ParticleFX コンポーネント（component）を基準にしたエミッターのトランスフォーム（transform）です。

Play Mode
: エミッターの再生方法を制御します。
  - `Once` は、指定した継続時間に達するとエミッターを停止します。
  - `Loop` は、指定した継続時間に達するとエミッターを再開します。

Size Mode
: 連続した画像を切り替えるフリップブックアニメーション（flipbook animation）のサイズの決め方を制御します。
  - `Auto` は、フリップブックアニメーションの各フレームのサイズを元の画像と同じに保ちます。
  - `Manual` は、サイズプロパティに従ってパーティクルのサイズを設定します。

Emission Space
: 生成されたパーティクルが存在する座標空間です。
  - `World` は、エミッターとは独立してパーティクルを移動させます。
  - `Emitter` は、エミッターを基準にしてパーティクルを移動させます。

Duration
: エミッターがパーティクルを放出する秒数です。

Start Delay
: エミッターがパーティクルを放出する前に待機する秒数です。

Start Offset
: パーティクルシミュレーションの開始から何秒経過した時点でエミッターを開始するかを指定します。つまり、エミッターがエフェクトを事前にシミュレーションする秒数です。

Image
: パーティクルのテクスチャとアニメーションに使う画像ファイル（タイルソース（tile source）またはアトラス（atlas））です。

Animation
: パーティクルに使う、*Image* ファイル内のアニメーションです。

Material
: パーティクルのシェーディングに使うマテリアル（material）です。

Blend Mode
: 使用できるブレンドモードは `Alpha`、`Add`、`Multiply` です。

Max Particle Count
: このエミッターから生成されたパーティクルが、同時に存在できる数です。

Emitter Type
: エミッターの形状です。
  - `Circle` は、円の内部のランダムな位置からパーティクルを放出します。パーティクルは中心から外側へ向かいます。円の直径は *Emitter Size X* で定義します。

  - `2D Cone` は、平面の円錐（三角形）の内部のランダムな位置からパーティクルを放出します。パーティクルは円錐の上部から外に向かいます。*Emitter Size X* は上部の幅を、*Y* は高さを定義します。

  - `Box` は、直方体の内部のランダムな位置からパーティクルを放出します。パーティクルは、直方体のローカル Y 軸に沿って上に向かいます。*Emitter Size X*、*Y*、*Z* は、それぞれ幅、高さ、奥行きを定義します。2D の長方形にするには、Z のサイズをゼロに保ちます。

  - `Sphere` は、球の内部のランダムな位置からパーティクルを放出します。パーティクルは中心から外側へ向かいます。球の直径は *Emitter Size X* で定義します。

  - `Cone` は、3D の円錐の内部のランダムな位置からパーティクルを放出します。パーティクルは、円錐の上部の円盤を通って外に向かいます。*Emitter Size X* は上部の円盤の直径を、*Y* は円錐の高さを定義します。

  ![エミッターの種類](images/particlefx/emitter_types.png)

Particle Orientation
: 放出されたパーティクルの向きを決める方法です。
  - `Default` は、向きを回転のない状態に設定します。
  - `Initial Direction` は、放出されたパーティクルの初期の向きを保ちます。
  - `Movement Direction` は、パーティクルの速度に応じて向きを調整します。

Inherit Velocity
: パーティクルがエミッターの速度をどの程度継承するかを示すスケール値です。この値は、*Space* が `World` に設定されている場合にのみ使用できます。エミッターの速度は毎フレーム推定されます。

Stretch With Velocity
: チェックを入れると、パーティクルの引き伸ばし量を移動方向に拡大縮小します。

### ブレンドモード {#blend-modes}
:[blend-modes](../shared/blend-modes.md)

## キーフレームを設定できるエミッターのプロパティ {#keyable-emitter-properties}

これらのプロパティには、値とばらつきの2つのフィールドがあります。ばらつきは、生成されるパーティクルごとにランダムに適用される変動幅です。たとえば、値が50でばらつきが3の場合、生成される各パーティクルには47から53（50 +/- 3）の間の値が設定されます。

![プロパティ](images/particlefx/property.png)

キーボタンにチェックを入れると、プロパティの値をエミッターの継続時間にわたるカーブで制御できます。キーフレームを設定したプロパティをリセットするには、キーボタンのチェックを外します。

![キーフレームを設定したプロパティ](images/particlefx/key.png)

カーブの変更には、下部ビューのタブにある *Curve Editor* を使います。キーフレームを設定したプロパティは *Properties* ビューでは編集できず、*Curve Editor* でのみ編集できます。ポイントと接線を <kbd>クリックしてドラッグ</kbd> すると、カーブの形状を変更できます。カーブ上を <kbd>ダブルクリック</kbd> すると、制御点を追加できます。制御点を削除するには、その点を <kbd>ダブルクリック</kbd> します。

![ParticleFX のカーブエディター](images/particlefx/curve_editor.png)

Curve Editor を自動的にズームしてすべてのカーブを表示するには、<kbd>F</kbd> を押します。

次のプロパティは、エミッターの再生時間にわたってキーフレームを設定できます。

Spawn Rate
: 1秒あたりに放出するパーティクルの数です。

Emitter Size X/Y/Z
: エミッターの形状の寸法です。上記の *Emitter Type* を参照してください。

Particle Life Time
: 生成される各パーティクルの寿命です。単位は秒です。

Initial Speed
: 生成される各パーティクルの初期速度です。

Initial Size
: 生成される各パーティクルの初期サイズです。*Size Mode* を `Automatic` に設定し、画像ソースとしてフリップブックアニメーションを使う場合、このプロパティは無視されます。

Initial Red/Green/Blue/Alpha
: パーティクルの各色成分の初期色調値です。

Initial Rotation
: パーティクルの初期回転値です。単位は度です。

Initial Stretch X/Y
: パーティクルの初期の引き伸ばし量です。単位はユニットです。

Initial Angular Velocity
: 生成される各パーティクルの初期角速度です。単位は度/秒です。

次のプロパティは、パーティクルの寿命にわたってキーフレームを設定できます。

Life Scale
: 各パーティクルの寿命にわたるスケール値です。

Life Red/Green/Blue/Alpha
: 各パーティクルの寿命にわたる各色成分の色調値です。

Life Rotation
: 各パーティクルの寿命にわたる回転値です。単位は度です。

Life Stretch X/Y
: 各パーティクルの寿命にわたる引き伸ばし量です。単位はユニットです。

Life Angular Velocity
: 各パーティクルの寿命にわたる角速度です。単位は度/秒です。

## モディファイアー {#modifiers}

パーティクルの速度に影響を与えるモディファイアーには、4つの種類があります。

`Acceleration`
: ある方向への加速です。

`Drag`
: パーティクルの速度に比例して、パーティクルの加速度を減らします。

`Radial`
: ある位置に向かってパーティクルを引き寄せるか、その位置から遠ざかるように押し出します。

`Vortex`
: 自身の位置を中心として、円やらせんを描く方向にパーティクルを動かします。

  ![モディファイアー](images/particlefx/modifiers.png)

## モディファイアーのプロパティ {#modifier-properties}

Position/Rotation
: 親を基準にしたモディファイアーのトランスフォームです。

Magnitude
: モディファイアーがパーティクルに与える影響の大きさです。

Max Distance
: パーティクルがこのモディファイアーの影響を受ける最大距離です。Radial と Vortex でのみ使います。

## パーティクルエフェクトの制御 {#controlling-a-particle-effect}

スクリプトからパーティクルエフェクトを開始、停止するには、次のようにします。

```lua
-- start the effect component "particles" in the current game object
particlefx.play("#particles")

-- stop the effect component "particles" in the current game object
particlefx.stop("#particles")
```

GUI スクリプトからパーティクルエフェクトを開始、停止する方法については、[GUI パーティクルエフェクトのマニュアル](/manuals/gui-particlefx#controlling-the-effect)を参照してください。

::: sidenote
パーティクルエフェクトコンポーネントが属していたゲームオブジェクト（game object）が削除されても、パーティクルエフェクトはパーティクルを放出し続けます。
:::
詳しくは、[Particle FX リファレンスドキュメント](/ref/particlefx)を参照してください。

## マテリアル定数 {#material-constants}

デフォルトのパーティクルエフェクトマテリアルには、`particlefx.set_constant()` で変更し、`particlefx.reset_constant()` でリセットできる次の定数があります（詳しくは、[マテリアルのマニュアル](/manuals/material/#vertex-and-fragment-constants)を参照してください）。

`tint`
: パーティクルエフェクトの色調（`vector4`）です。vector4 は色調を表すために使い、x、y、z、w が、それぞれ赤、緑、青、アルファの色調に対応します。[API リファレンスの例](/ref/particlefx/#particlefx.set_constant:url-constant-value)を参照してください。


## プロジェクト設定 {#project-configuration}

*game.project* ファイルには、パーティクルに関連する[プロジェクト設定](/manuals/project-settings#particle-fx)がいくつかあります。
