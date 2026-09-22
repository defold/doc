---
title: Defold の GUI パイノード
brief: このマニュアルでは、Defold の GUI シーンでパイノードを使用する方法を説明します。
---

# GUI パイノード {#gui-pie-nodes}

パイノード（pie node）は、単純な円から扇形や四角いドーナツ形まで、円形または楕円形のオブジェクトを作成するために使用します。

## パイノードの作成 {#creating-a-pie-node}

*Outline* の *Nodes* セクションを <kbd>右クリック</kbd> し、<kbd>Add ▸ Pie</kbd> を選択します。新しいパイノードが選択され、そのプロパティを変更できます。

![パイノードの作成](images/gui-pie/create.png)

パイノード固有のプロパティは次のとおりです。

Inner Radius
: ノードの内側の半径です。X 軸に沿った値で表します。

Outer Bounds
: ノードの外周の形状です。

  - `Ellipse` は、ノードを外側の半径まで広げます。
  - `Rectangle` は、ノードをそのバウンディングボックス（bounding box）まで広げます。

Perimeter Vertices
: 形状の構成に使用するセグメント数です。ノードの360度の外周全体を囲むために必要な頂点数として表します。

Pie Fill Angle
: パイの塗りつぶす範囲です。右方向を起点とし、反時計回りの角度で表します。

![プロパティ](images/gui-pie/properties.png)

ノードにテクスチャを設定すると、テクスチャ画像が平面的に貼り付けられ、テクスチャの各隅はノードのバウンディングボックスの各隅に対応します。

## 実行時のパイノードの変更 {#modify-pie-nodes-at-runtime}

パイノードでは、サイズ、ピボット（pivot）、色などを設定する汎用のノード操作関数をすべて使用できます。パイノード専用の関数やプロパティもいくつかあります。

```lua
local pienode = gui.get_node("my_pie_node")

-- get the outer bounds
local fill_angle = gui.get_fill_angle(pienode)

-- increase perimeter vertices
local vertices = gui.get_perimeter_vertices(pienode)
gui.set_perimeter_vertices(pienode, vertices + 1)

-- change outer bounds
gui.set_outer_bounds(pienode, gui.PIEBOUNDS_RECTANGLE)

-- animate the inner radius
gui.animate(pienode, "inner_radius", 100, gui.EASING_INOUTSINE, 2, 0, nil, gui.PLAYBACK_LOOP_PINGPONG)
```
