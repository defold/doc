---
title: Defold のプロパティ
brief: このマニュアルでは、Defold に存在するプロパティの種類と、その使い方およびアニメーションさせる方法について説明します。
---

# プロパティ {#properties}

Defold は、ゲームオブジェクト（game object）、コンポーネント（component）、GUI ノード（GUI node）に対して、読み取り、設定、アニメーションが可能なプロパティ（property）を公開しています。プロパティには次の種類があります。

* システムが定義するゲームオブジェクトのトランスフォーム（transform）（位置、回転、スケール）と、コンポーネント固有のプロパティ（たとえば、スプライト（sprite）のピクセル単位のサイズや、コリジョンオブジェクト（collision object）の質量）
* Lua スクリプトで定義する、スクリプトコンポーネント（script component）のユーザー定義プロパティ（詳細は[スクリプトプロパティのドキュメント](/manuals/script-properties)を参照してください）
* GUI ノードのプロパティ
* シェーダー（shader）とマテリアル（material）ファイルで定義するシェーダー定数（shader constant）（詳細は[マテリアルのドキュメント](/manuals/material)を参照してください）

数値プロパティの入力欄にマウスポインターを合わせると、ドラッグハンドルが表示されます。ハンドルを右または上にドラッグすると値を増やし、左または下にドラッグすると値を減らせます。

プロパティの所在によって、汎用関数またはプロパティ専用の関数を使ってアクセスします。多くのプロパティは自動的にアニメーションさせることができます。パフォーマンスと利便性の両面から、プロパティを自分で（`update()` 関数内で）操作するよりも、組み込みの仕組みでアニメーションさせることを強く推奨します。

`vector3`、`vector4`、`quaternion` 型の複合プロパティは、その成分（`x`、`y`、`z`、`w`）も公開しています。プロパティ名の末尾にドット（`.`）と成分名を付けると、各成分を個別に指定できます。たとえば、ゲームオブジェクトの位置の x 成分を設定するには、次のようにします。

```lua
-- Set the x position of "game_object" to 10.
go.set("game_object", "position.x", 10)
```

`go.get()`、`go.set()`、`go.animate()` 関数は、第1パラメーターに参照、第2パラメーターにプロパティ識別子を受け取ります。参照はゲームオブジェクトまたはコンポーネントを識別するもので、文字列、ハッシュ、URL のいずれかを使えます。URL については[アドレス指定のマニュアル](/manuals/addressing)で詳しく説明しています。プロパティ識別子は、プロパティの名前を表す文字列またはハッシュです。

```lua
-- Set the x-scale of the sprite component
local url = msg.url("#sprite")
local prop = hash("scale.x")
go.set(url, prop, 2.0)
```

GUI ノードの場合は、プロパティ専用の関数、または汎用の `gui.get()` および `gui.set()` 関数の第1パラメーターにノードを渡します。

```lua
-- Get the color of the button
local node = gui.get_node("button")
local color = gui.get_color(node)
local same_color = gui.get(node, "color")
gui.set(node, "color.x", 1)
```

## ゲームオブジェクトとコンポーネントのプロパティ {#game-object-and-component-properties}

すべてのゲームオブジェクトと一部の種類のコンポーネントには、実行時に読み取りや操作ができるプロパティがあります。これらの値は [`go.get()`](/ref/go#go.get) で読み取り、[`go.set()`](/ref/go#go.set) で書き込みます。プロパティの値の型によっては、[`go.animate()`](/ref/go#go.animate) で値をアニメーションさせることができます。読み取り専用のプロパティも少数あります。

`get`{.mark}
: [`go.get()`](/ref/go#go.get) で読み取れます。

`get+set`{.mark}
: [`go.get()`](/ref/go#go.get) で読み取り、[`go.set()`](/ref/go#go.set) で書き込めます。数値は [`go.animate()`](/ref/go#go.animate) でアニメーションさせることができます。

*ゲームオブジェクトのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *position* | ゲームオブジェクトのローカル位置です。 | `vector3`      | `get+set`{.mark} |
| *rotation* | `quaternion` で表される、ゲームオブジェクトのローカル回転です。 | `quaternion` | `get+set`{.mark} |
| *euler*    | オイラー角で表される、ゲームオブジェクトのローカル回転です。 | `vector3` | `get+set`{.mark} |
| *scale*    | ゲームオブジェクトのローカルな非均一スケールです。各成分が各軸に沿った倍率を持つベクトルで表します。Z を変更せずに X と Y のサイズを2倍にするには、`vmath.vector3(2.0, 2.0, 1.0)` を使います。 | `vector3` | `get+set`{.mark} |
| *scale.xy*    | ゲームオブジェクトの X 軸と Y 軸に沿ったローカルな非均一スケールです。Z 方向の拡大縮小を意図しない場合は、このプロパティまたは `go.set_scale_xy()` を使います。 | `vector3` | `get+set`{.mark} |

::: sidenote
ゲームオブジェクトのトランスフォームを操作する専用関数もあります。`go.get_position()`、`go.set_position()`、`go.get_rotation()`、`go.set_rotation()`、`go.get_scale()`、`go.set_scale()`、`go.set_scale_xy()` です。
:::

*スプライトコンポーネントのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *size*     | スプライトのスケール適用前のサイズ、つまり元のアトラス（atlas）から取得したサイズです。 | `vector3` | `get`{.mark} |
| *image* | スプライトのテクスチャパスのハッシュです。 | `hash` | `get`{.mark}|
| *scale* | スプライトの非均一スケールです。 | `vector3` | `get+set`{.mark}|
| *scale.xy* | スプライトの X 軸と Y 軸に沿った非均一スケールです。 | `vector3` | `get+set`{.mark}|
| *material* | スプライトが使うマテリアルです。 | `hash` | `get+set`{.mark}|
| *cursor* | 再生カーソルの位置（0--1 の範囲）です。 | `number` | `get+set`{.mark}|
| *playback_rate* | フリップブックアニメーション（flipbook animation）のフレームレートです。 | `number` | `get+set`{.mark}|

*コリジョンオブジェクトコンポーネントのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *mass*     | コリジョンオブジェクトの質量です。 | `number` | `get`{.mark} |
| *linear_velocity* | コリジョンオブジェクトの現在の並進速度です。 | `vector3` | `get`{.mark} |
| *angular_velocity* | コリジョンオブジェクトの現在の角速度です。 | `vector3` | `get`{.mark} |
| *linear_damping* | コリジョンオブジェクトの並進運動の減衰です。 | `vector3` | `get+set`{.mark} |
| *angular_damping* | コリジョンオブジェクトの回転運動の減衰です。 | `vector3` | `get+set`{.mark} |

*モデル（3D）コンポーネントのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *animation* | 現在のアニメーションです。                | `hash`          | `get`{.mark}     |
| *texture0*--*texture15* | モデル（model）のテクスチャパスのハッシュです。 | `hash` | `get+set`{.mark}|
| *cursor*  | 再生カーソルの位置（0--1 の範囲）です。 | `number`   | `get+set`{.mark} |
| *playback_rate* | アニメーションの再生速度です。アニメーションの再生速度に対する倍率です。 | `number` | `get+set`{.mark} |
| *material* | モデルが使うマテリアルです。 | `hash` | `get+set`{.mark}|

*ラベルコンポーネントのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *scale* | ラベル（label）のスケールです。 | `vector3` | `get+set`{.mark} |
| *scale.xy* | ラベルの X 軸と Y 軸に沿ったスケールです。 | `vector3` | `get+set`{.mark}|
| *color*     | ラベルの色です。 | `vector4` | `get+set`{.mark} |
| *outline* | ラベルの輪郭の色です。 | `vector4` | `get+set`{.mark} |
| *shadow* | ラベルの影の色です。 | `vector4` | `get+set`{.mark} |
| *size* | ラベルのサイズです。改行が有効な場合、このサイズによってテキストの範囲が制限されます。 | `vector3` | `get+set`{.mark} |
| *material* | ラベルが使うマテリアルです。 | `hash` | `get+set`{.mark}|
| *font* | ラベルが使うフォントです。 | `hash` | `get+set`{.mark}|


## GUI ノードのプロパティ {#gui-node-properties}

GUI ノードには、`gui.get_position()` や `gui.set_position()` のような、プロパティ専用の取得関数と設定関数があります。以下に示す組み込みプロパティは、代わりに `gui.get(node, property)` と `gui.set(node, property, value)` でも読み書きできます。それ以外のノードの値には、引き続き専用関数が必要な場合があります。GUI ノードのマテリアル定数にも汎用関数を使います。ベクトルプロパティの1つの成分を指定するには、たとえば `gui.set(node, "color.x", 1)` のように、その成分名を末尾に付けます。

汎用関数とプロパティ専用の関数は、必ずしも同じ値の型を使うわけではありません。`gui.get()` は `position`、`scale`、`size`、`euler` プロパティの値全体を `vector4` として返しますが、対応するプロパティ専用の関数は `vector3` を返します。`gui.set()` は、これらのプロパティに対して `vector3` と `vector4` のどちらも受け付けます。汎用関数の `rotation` プロパティはクォータニオン（quaternion）を使います。回転を度数で設定する場合は `euler` を使ってください。

* `position`（または `gui.PROP_POSITION`）
* `rotation`（または `gui.PROP_ROTATION`）
* `euler`（または `gui.PROP_EULER`）
* `scale`（または `gui.PROP_SCALE`）
* `color`（または `gui.PROP_COLOR`）
* `outline`（または `gui.PROP_OUTLINE`）
* `shadow`（または `gui.PROP_SHADOW`）
* `size`（または `gui.PROP_SIZE`）
* `fill_angle`（または `gui.PROP_FILL_ANGLE`）
* `inner_radius`（または `gui.PROP_INNER_RADIUS`）
* `leading`（または `gui.PROP_LEADING`）
* `tracking`（または `gui.PROP_TRACKING`）
* `slice9`（または `gui.PROP_SLICE9`）

すべての色の値は `vector4` に格納され、各成分が次の RGBA 値に対応することに注意してください。

`x`
: 赤の色成分

`y`
: 緑の色成分

`z`
: 青の色成分

`w`
: アルファ成分

*GUI ノードのプロパティ*

| プロパティ   | 説明                            | 型            |                  |
| ---------- | -------------------------------------- | --------------- | ---------------- |
| *color*   | ノードの面の色です。            | `vector4`      | `gui.get_color()` `gui.set_color()` |
| *outline* | ノードの輪郭の色です。         | `vector4`       | `gui.get_outline()` `gui.set_outline()` |
| *position* | ノードの位置です。 | `vector3` | `gui.get_position()` `gui.set_position()` |
| *rotation* | ノードの回転です。取得関数はクォータニオンを返し、設定関数はクォータニオン、またはベクトルで表したオイラー角を受け付けます。 | `quaternion`、`vector3`、または `vector4` | `gui.get_rotation()` `gui.set_rotation()` |
| *euler* | 度数のオイラー角で表したノードの回転です。 | `vector3` | `gui.get_euler()` `gui.set_euler()` |
| *scale* | 各軸に沿った倍率で表したノードのスケールです。 | `vector3` |`gui.get_scale()` `gui.set_scale()` |
| *shadow* | ノードの影の色です。 | `vector4` | `gui.get_shadow()` `gui.set_shadow()` |
| *size* | ノードのスケール適用前のサイズです。 | `vector3` | `gui.get_size()` `gui.set_size()` |
| *fill_angle* | 反時計回りの度数で表したパイノード（pie node）の塗りつぶし角度です。 | `number` | `gui.get_fill_angle()` `gui.set_fill_angle()` |
| *inner_radius* | パイノードの内側の半径です。 | `number` | `gui.get_inner_radius()` `gui.set_inner_radius()` |
| *leading* | テキストノード（text node）の行間の倍率です。 | `number` | `gui.get_leading()` `gui.set_leading()` |
| *tracking* | テキストノードの字間の倍率です。 | `number` | `gui.get_tracking()` `gui.set_tracking()` |
| *slice9* | 9スライスノード（slice9 node）の各端からの距離です。 | `vector4` | `gui.get_slice9()` `gui.set_slice9()` |
