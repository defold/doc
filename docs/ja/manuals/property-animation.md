---
title: Defold のプロパティアニメーションマニュアル
brief: 本マニュアルでは、Defold でプロパティアニメーション（property animation）を使う方法を説明します。
---

# プロパティアニメーション {#property-animation}

数値型（`numbers`、`vector3`、`vector4`、クォータニオン）のすべてのプロパティ（property）とシェーダー定数（shader constant）は、組み込みのアニメーションシステムで `go.animate()` 関数を使ってアニメーション化できます。エンジンは、指定した再生モードとイージング（easing）関数に従ってプロパティを自動的に「補間（tween）」します。独自のイージング関数を指定することもできます。

  ![プロパティアニメーション](images/animation/property_animation.png)
  ![バウンスのループ](images/animation/bounce.gif)

## プロパティアニメーション {#property-animation}

ゲームオブジェクト（game object）やコンポーネント（component）のプロパティをアニメーション化するには、`go.animate()` 関数を使います。GUI ノード（GUI node）のプロパティに対応する関数は `gui.animate()` です。

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

指定したプロパティのアニメーションをすべて停止するには、`go.cancel_animations()` を呼び出します。GUI ノードの場合は `gui.cancel_animations()` を呼び出します。

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

`position` のように複数の成分からなるプロパティのアニメーションをキャンセルすると、その各成分（`position.x`、`position.y`、`position.z`）のアニメーションもすべてキャンセルされます。

[プロパティのマニュアル](/manuals/properties)には、ゲームオブジェクト、コンポーネント、GUI ノードで利用できるすべてのプロパティが記載されています。

## GUI ノードのプロパティアニメーション {#gui-node-property-animation}

GUI ノードのほぼすべてのプロパティをアニメーション化できます。たとえば、ノードの `color` プロパティを完全に透明に設定して見えなくし、その後、色を白（色調を変えない色）にアニメーション化してフェードインさせることができます。

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## 完了コールバック {#completion-callbacks}

プロパティアニメーション関数 `go.animate()` と `gui.animate()` では、最後の引数に Lua コールバック（callback）関数を任意で指定できます。この関数は、アニメーションが最後まで再生されたときに呼び出されます。ループするアニメーションでは呼び出されず、`go.cancel_animations()` または `gui.cancel_animations()` でアニメーションを手動でキャンセルした場合にも呼び出されません。このコールバックを使うと、アニメーションの完了時にイベントを発生させたり、複数のアニメーションを連続して実行したりできます。

## イージング {#easing}

イージングは、アニメーション化する値が時間の経過とともにどのように変化するかを定義します。以下の画像は、イージングを実現するために時間に応じて適用される関数を示しています。

`go.animate()` で使えるイージングの値は次のとおりです。

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

`gui.animate()` で使えるイージングの値は次のとおりです。

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![線形補間](images/properties/easing_linear.png)
![バックのイーズイン](images/properties/easing_inback.png)
![バックのイーズアウト](images/properties/easing_outback.png)
![バックのイーズイン・アウト](images/properties/easing_inoutback.png)
![バックのイーズアウト・イン](images/properties/easing_outinback.png)
![バウンスのイーズイン](images/properties/easing_inbounce.png)
![バウンスのイーズアウト](images/properties/easing_outbounce.png)
![バウンスのイーズイン・アウト](images/properties/easing_inoutbounce.png)
![バウンスのイーズアウト・イン](images/properties/easing_outinbounce.png)
![エラスティックのイーズイン](images/properties/easing_inelastic.png)
![エラスティックのイーズアウト](images/properties/easing_outelastic.png)
![エラスティックのイーズイン・アウト](images/properties/easing_inoutelastic.png)
![エラスティックのイーズアウト・イン](images/properties/easing_outinelastic.png)
![サインのイーズイン](images/properties/easing_insine.png)
![サインのイーズアウト](images/properties/easing_outsine.png)
![サインのイーズイン・アウト](images/properties/easing_inoutsine.png)
![サインのイーズアウト・イン](images/properties/easing_outinsine.png)
![指数関数のイーズイン](images/properties/easing_inexpo.png)
![指数関数のイーズアウト](images/properties/easing_outexpo.png)
![指数関数のイーズイン・アウト](images/properties/easing_inoutexpo.png)
![指数関数のイーズアウト・イン](images/properties/easing_outinexpo.png)
![円弧のイーズイン](images/properties/easing_incirc.png)
![円弧のイーズアウト](images/properties/easing_outcirc.png)
![円弧のイーズイン・アウト](images/properties/easing_inoutcirc.png)
![円弧のイーズアウト・イン](images/properties/easing_outincirc.png)
![2次関数のイーズイン](images/properties/easing_inquad.png)
![2次関数のイーズアウト](images/properties/easing_outquad.png)
![2次関数のイーズイン・アウト](images/properties/easing_inoutquad.png)
![2次関数のイーズアウト・イン](images/properties/easing_outinquad.png)
![3次関数のイーズイン](images/properties/easing_incubic.png)
![3次関数のイーズアウト](images/properties/easing_outcubic.png)
![3次関数のイーズイン・アウト](images/properties/easing_inoutcubic.png)
![3次関数のイーズアウト・イン](images/properties/easing_outincubic.png)
![4次関数のイーズイン](images/properties/easing_inquart.png)
![4次関数のイーズアウト](images/properties/easing_outquart.png)
![4次関数のイーズイン・アウト](images/properties/easing_inoutquart.png)
![4次関数のイーズアウト・イン](images/properties/easing_outinquart.png)
![5次関数のイーズイン](images/properties/easing_inquint.png)
![5次関数のイーズアウト](images/properties/easing_outquint.png)
![5次関数のイーズイン・アウト](images/properties/easing_inoutquint.png)
![5次関数のイーズアウト・イン](images/properties/easing_outinquint.png)

## カスタムイージング {#custom-easing}

一連の値を持つ `vector` を定義し、上記の定義済みイージング定数の代わりにそのベクトルを渡すと、独自のイージングカーブを作成できます。ベクトルの値は、開始値（`0`）から目標値（`1`）までのカーブを表します。ランタイムはベクトルから値をサンプリングし、ベクトルで表される点と点の間の値を計算するときには線形補間します。

たとえば、次のベクトルを使うと、

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

以下のカーブになります。

![独自のカーブ](images/animation/custom_curve.png)

次の例では、矩形波のカーブに従って、ゲームオブジェクトの y 位置が現在の位置と 200 の間で切り替わります。

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![矩形波のカーブ](images/animation/square_curve.png)
