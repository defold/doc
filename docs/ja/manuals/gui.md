---
title: Defold の GUI シーン
brief: このマニュアルでは、Defold の GUI エディター、各種 GUI ノード、GUI スクリプティングについて説明します。
---

# GUI

Defold には、ユーザーインターフェースの構築と実装に特化した専用の GUI エディターと、強力なスクリプティング機能が用意されています。

Defold のグラフィカルユーザーインターフェースは、作成してゲームオブジェクト（game object）に取り付け、コレクション（collection）に配置するコンポーネント（component）です。このコンポーネントには次の特徴があります。

* シンプルで強力なレイアウト機能があり、解像度やアスペクト比に依存せずユーザーインターフェースを描画できます。
* *GUI スクリプト（GUI script）* を通じて、動作のロジックを付けられます。
* デフォルトでは、カメラのビューに関係なく他のコンテンツの手前に描画されるため、カメラが移動しても GUI 要素は画面上の同じ位置に留まります。描画の動作は変更できます。

GUI コンポーネントは、ゲームのビューとは独立して描画されます。そのため、コレクションエディター内の特定の位置には配置されず、コレクションエディター上で視覚的に表示されることもありません。ただし、GUI コンポーネントはコレクション内に位置を持つゲームオブジェクトに含まれている必要があります。その位置を変更しても GUI には影響しません。

## GUI コンポーネントの作成 {#creating-a-gui-component}

GUI コンポーネントは、GUI シーン（GUI scene）のプロトタイプ（prototype）ファイルから作成します。他のエンジンでは「プレハブ（prefabs）」や「ブループリント（blueprints）」とも呼ばれます。新しい GUI コンポーネントを作成するには、*Assets* ブラウザー内の場所を <kbd>右クリック</kbd> し、<kbd>New ▸ Gui</kbd> を選択します。新しい GUI ファイルの名前を入力し、<kbd>Ok</kbd> を押します。

![新しい GUI ファイル](images/gui/new_gui_file.png)

Defold がそのファイルを GUI シーンエディターで自動的に開きます。

![新しい GUI](images/gui/new_gui.png)

*Outline* には、ノード（node）の一覧と依存関係など、GUI のすべての内容が表示されます（後述）。

中央の編集エリアには GUI が表示されます。編集エリアの右上にあるツールバーには、*Move*、*Rotate*、*Scale* ツールと、[レイアウト](/manuals/gui-layouts)の選択機能があります。

![ツールバー](images/gui/toolbar.png)

白い矩形は現在選択されているレイアウトの範囲を示し、デフォルトではプロジェクト設定で指定した表示幅と高さになります。

## GUI のプロパティ {#gui-properties}

*Outline* でルートの「Gui」ノードを選択すると、GUI コンポーネントの *Properties* が表示されます。

*Script*
: この GUI コンポーネントに関連付けられた GUI スクリプトです。

*Material*
: この GUI の描画に使用するマテリアル（material）です。*Outline* パネルから Gui に複数のマテリアルを追加し、個々のノードに割り当てることもできます。

*Adjust Reference*
: 各ノードの *Adjust Mode* の計算方法を制御します。

  - `Per Node` は、調整後の親ノードのサイズ、またはサイズ変更後の画面を基準に、各ノードを調整します。
  - `Disable` は、ノードの調整モード（adjust mode）を無効にします。これにより、すべてのノードは設定されたサイズを維持します。

*Current Nodes*
: この GUI で現在使用されているノードの数です。

*Max Nodes*
: この GUI のノードの最大数です。

*Max Dynamic Textures*
: この GUI コンポーネントが追跡する動的テクスチャの最大数で、デフォルトは `128` です。これには、[`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) で作成したテクスチャと、`go.set(..., "textures", ...)` または `gui.set(msg.url(), "textures", ...)` で GUI に割り当てた外部テクスチャが含まれます。多数の外部テクスチャを置き換えるプロジェクトでは、この上限を引き上げる必要がある場合があります。


## 実行時の操作 {#runtime-manipulation}

スクリプトコンポーネントから `go.get()` と `go.set()` を使用して、実行時に GUI のプロパティを操作できます。

フォント
: GUI で使用するフォントを取得または設定します。

![フォントの取得と設定](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- get the font file currently assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- set the font with id 'default' to the font file assigned to the resource property 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- get the new font file assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

マテリアル
: GUI で使用するマテリアルを取得または設定します。

![マテリアルの取得と設定](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- get the material file currently assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- set the material id 'effect' to the material file assigned to the resource property 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- get the new material file assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

テクスチャ
: GUI で使用するテクスチャ（アトラス（atlas））を取得または設定します。

![テクスチャの取得と設定](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- get the texture file currently assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- set the texture with id 'theme' to the texture file assigned to the resource property 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- get the new texture file assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## 依存関係 {#dependencies}

Defold のゲームのリソースツリーは静的なため、GUI ノードに必要な依存関係はすべてコンポーネントに追加する必要があります。*Outline* では、すべての依存関係が種類ごとの「フォルダー」にまとめられています。

![依存関係](images/gui/dependencies.png)

新しい依存関係を追加するには、*Asset* ペインからエディタービューへドラッグアンドドロップします。

または、*Outline* でルートの「Gui」を <kbd>右クリック</kbd> し、ポップアップのコンテキストメニューから <kbd>Add ▸ [type]</kbd> を選択します。

追加したい種類のフォルダーアイコンを <kbd>右クリック</kbd> して、<kbd>Add ▸ [type]</kbd> を選択することもできます。

## ノードの種類 {#node-types}

GUI コンポーネントは、一連のノードから構成されます。ノードはシンプルな要素です。エディターで、または実行時にスクリプトを通じて、移動、拡大縮小、回転したり、親子階層に配置したりできます。次の種類のノードがあります。

ボックスノード
: ![ボックスノード](images/icons/gui-box-node.png){.left}
  単色、テクスチャ、またはフリップブックアニメーションを表示する矩形のボックスノード（box node）です。詳細は[ボックスノードのドキュメント](/manuals/gui-box)を参照してください。

<div style="clear: both;"></div>

テキストノード
: ![テキストノード](images/icons/gui-text-node.png){.left}
  テキストを表示するテキストノード（text node）です。詳細は[テキストノードのドキュメント](/manuals/gui-text)を参照してください。

<div style="clear: both;"></div>

パイノード
: ![パイノード](images/icons/gui-pie-node.png){.left}
  円や扇形を表示するパイノード（pie node）は、部分的に塗りつぶしたり反転したりできる円形または楕円形のノードです。詳細は[パイノードのドキュメント](/manuals/gui-pie)を参照してください。

<div style="clear: both;"></div>

テンプレートノード
: ![テンプレートノード](images/icons/gui.png){.left}
  テンプレートノード（template node）は、別の GUI シーンファイルを基にインスタンスを作成するために使用します。詳細は[テンプレートノードのドキュメント](/manuals/gui-template)を参照してください。

<div style="clear: both;"></div>

ParticleFX ノード
: ![パーティクルエフェクトノード](images/icons/particlefx.png){.left}
  パーティクルエフェクトを再生します。詳細は[ParticleFX ノードのドキュメント](/manuals/gui-particlefx)を参照してください。

<div style="clear: both;"></div>

ノードを追加するには、*Nodes* フォルダーを右クリックし、<kbd>Add ▸</kbd> を選択してから、<kbd>Box</kbd>、<kbd>Text</kbd>、<kbd>Pie</kbd>、<kbd>Template</kbd>、<kbd>ParticleFx</kbd> のいずれかを選択します。

![ノードの追加](images/gui/add_node.png)

<kbd>A</kbd> を押して、GUI に追加したい種類を選択することもできます。

## ノードのプロパティ {#node-properties}

各ノードには、外観を制御する多くのプロパティがあります。

Id
: ノードの識別名です。この名前は GUI シーン内で一意である必要があります。

Position、Rotation、Scale
: ノードの位置、向き、伸縮を制御します。*Move*、*Rotate*、*Scale* ツールでこれらの値を変更できます。値はスクリプトからアニメーションさせることができます（[詳細](/manuals/property-animation)）。

Size（ボックス、テキスト、パイノード）
: ノードのサイズはデフォルトで自動設定されますが、*Size Mode* を `Manual` に設定すると値を変更できます。サイズはノードの範囲を定義し、入力による選択判定に使用されます。この値はスクリプトからアニメーションさせることができます（[詳細](/manuals/property-animation)）。

Size Mode（ボックス、パイノード）
: `Automatic` に設定すると、エディターがノードのサイズを設定します。`Manual` に設定すると、サイズを自分で設定できます。

Enabled
: チェックを外すと、ノードは描画もアニメーションもされず、`gui.pick_node()` で選択判定できなくなります。このプロパティをプログラムから変更、確認するには、`gui.set_enabled()` と `gui.is_enabled()` を使用します。

Visible
: チェックを外すと、ノードは描画されませんが、引き続きアニメーションと `gui.pick_node()` による選択判定はできます。このプロパティをプログラムから変更、確認するには、`gui.set_visible()` と `gui.get_visible()` を使用します。

Text（テキストノード）
: ノードに表示するテキストです。

Line Break（テキストノード）
: ノードの幅に合わせてテキストを折り返す場合に設定します。

Font（テキストノード）
: テキストの描画に使用するフォントです。

Texture（ボックス、パイノード）
: ノードに描画するテクスチャです。アトラスまたはタイルソース（tile source）内の画像やアニメーションへの参照です。

Material（ボックス、パイ、テキスト、パーティクルエフェクトノード）
: ノードの描画に使用するマテリアルです。*Outline* の Materials セクションに追加したマテリアルを指定するか、空欄のままにして GUI コンポーネントに割り当てられたデフォルトのマテリアルを使用できます。

Slice 9（ボックスノード）
: ノードのサイズを変更した際に、ノードのテクスチャの縁にあるピクセルの大きさを維持する場合に設定します。詳細は[ボックスノードのドキュメント](/manuals/gui-box)を参照してください。

Inner Radius（パイノード）
: X 軸に沿って表す、ノードの内側の半径です。詳細は[パイノードのドキュメント](/manuals/gui-pie)を参照してください。

Outer Bounds（パイノード）
: 外側の境界の動作を制御します。詳細は[パイノードのドキュメント](/manuals/gui-pie)を参照してください。

Perimeter Vertices（パイノード）
: 形状の構築に使用する分割数です。詳細は[パイノードのドキュメント](/manuals/gui-pie)を参照してください。

Pie Fill Angle（パイノード）
: パイをどれだけ塗りつぶすかを指定します。詳細は[パイノードのドキュメント](/manuals/gui-pie)を参照してください。

Template（テンプレートノード）
: ノードのテンプレートとして使用する GUI シーンファイルです。詳細は[テンプレートノードのドキュメント](/manuals/gui-template)を参照してください。

ParticleFX（パーティクルエフェクトノード）
: このノードで使用するパーティクルエフェクトです。詳細は[ParticleFX ノードのドキュメント](/manuals/gui-particlefx)を参照してください。

Color
: ノードの色です。ノードにテクスチャがある場合、この色でテクスチャの色調が変わります。色はスクリプトからアニメーションさせることができます（[詳細](/manuals/property-animation)）。

Alpha
: ノードの半透明度です。アルファ値（alpha）はスクリプトからアニメーションさせることができます（[詳細](/manuals/property-animation)）。

Inherit Alpha
: このチェックボックスを設定すると、ノードは親ノードのアルファ値を継承します。その際、ノードのアルファ値には親のアルファ値が乗算されます。

Leading（テキストノード）
: 行間の倍率です。値を `0` にすると行間がなくなります。`1`（デフォルト）は通常の行間です。

Tracking（テキストノード）
: 字間の倍率です。デフォルトは 0 です。

Layer
: ノードにレイヤー（layer）を割り当てると、通常の描画順序を上書きし、レイヤーの順序に従って描画されます。詳細は後述します。

Blend mode
: ノードのグラフィックスと背景のグラフィックスのブレンド方法を制御します。
  - `Alpha` は、ノードと背景のピクセル値をアルファブレンドします。グラフィックスソフトウェアの「Normal」ブレンドモードに相当します。
  - `Add` は、ノードと背景のピクセル値を加算します。一部のグラフィックスソフトウェアの「Linear dodge」に相当します。
  - `Multiply` は、ノードと背景のピクセル値を乗算します。
  - `Screen` は、ノードと背景のピクセル値を反転して乗算します。グラフィックスソフトウェアの「Screen」ブレンドモードに相当します。

Pivot
: ノードのピボット（pivot）を設定します。ノードの「中心点」と考えることができます。回転、拡大縮小、サイズの変更はすべて、この点を基準に行われます。

  設定できる値は、`Center`、`North`、`South`、`East`、`West`、`North West`、`North East`、`South West`、`South East` です。

  ![ピボット](images/gui/pivot.png)

  ノードのピボットを変更すると、新しいピボットがノードの位置に来るようにノードが移動します。テキストノードでは、`Center` は中央揃え、`West` は左揃え、`East` は右揃えになります。

X Anchor、Y Anchor
: アンカー（anchor）は、シーンの境界または親ノードの境界を実際の画面サイズに合わせて伸縮する際、ノードの縦方向と横方向の位置がどのように変わるかを制御します。

  ![調整前のアンカー](images/gui/anchoring_unadjusted.png)

  次のアンカーモードを使用できます。

  - `None`（*X Anchor* と *Y Anchor* の両方）は、親ノードまたはシーンの中心から見たノードの位置を、*調整後* のサイズに対する相対位置として維持します。
  - `Left` または `Right`（*X Anchor*）は、親ノードまたはシーンの左端と右端からの位置が同じ割合に保たれるように、ノードの横方向の位置を拡大縮小します。
  - `Top` または `Bottom`（*Y Anchor*）は、親ノードまたはシーンの上端と下端からの位置が同じ割合に保たれるように、ノードの縦方向の位置を拡大縮小します。

  ![アンカーの設定](images/gui/anchoring.png)

Adjust Mode
: ノードの調整モードを設定します。調整モードの設定は、シーンの境界または親ノードの境界を実際の画面サイズに合わせて調整する際、ノードに何が起きるかを制御します。

  次は、論理解像度が一般的な横向きの解像度であるシーンに作成したノードです。

  ![調整前](images/gui/unadjusted.png)

  シーンを縦向きの画面に合わせると、シーンが伸縮します。各ノードのバウンディングボックスも同様に伸縮します。ただし、調整モードを設定すると、ノードのコンテンツのアスペクト比をそのまま保つことができます。次のモードを使用できます。

  - `Fit` は、ノードのコンテンツの大きさが、伸縮後のバウンディングボックスの幅と高さのうち小さい方と等しくなるように拡大縮小します。つまり、コンテンツは伸縮後のノードのバウンディングボックス内に収まります。
  - `Zoom` は、ノードのコンテンツの大きさが、伸縮後のバウンディングボックスの幅と高さのうち大きい方と等しくなるように拡大縮小します。つまり、コンテンツは伸縮後のノードのバウンディングボックス全体を覆います。
  - `Stretch` は、伸縮後のノードのバウンディングボックスを埋めるように、ノードのコンテンツを伸縮します。

  ![調整モード](images/gui/adjusted.png)

  GUI シーンのプロパティ *Adjust Reference* が `Disabled` に設定されている場合、この設定は無視されます。

Clipping Mode（ボックス、パイノード）
: ノードのクリッピングモードを設定します。

  - `None` は、通常どおりノードを描画します。
  - `Stencil` は、ノードの境界でステンシルマスクを定義し、そのマスクを使用してノードの子ノードをクリッピングします。

  詳細は [GUI クリッピングのマニュアル](/manuals/gui-clipping)を参照してください。

Clipping Visible（ボックス、パイノード）
: ステンシル領域にノードのコンテンツを描画する場合に設定します。詳細は [GUI クリッピングのマニュアル](/manuals/gui-clipping)を参照してください。

Clipping Inverted（ボックス、パイノード）
: ステンシルマスクを反転します。詳細は [GUI クリッピングのマニュアル](/manuals/gui-clipping)を参照してください。


## ピボット、アンカー、調整モード {#pivot-anchors-and-adjust-mode}

Pivot、Anchors、Adjust Mode の各プロパティを組み合わせると、GUI を非常に柔軟に設計できますが、具体例を見ずに全体の仕組みを理解するのは少し難しいかもしれません。640x1136 の画面向けに作成した、次の GUI モックアップを例に見てみます。

![](images/gui/adjustmode_example_original.png)

この UI では、X Anchor と Y Anchor を None に設定し、各ノードの Adjust Mode はデフォルト値の Fit のままにしています。上部パネルの Pivot は North、下部パネルのピボットは South、上部パネル内のバーのピボットは West に設定しています。それ以外のノードのピボットは Center に設定しています。ウィンドウの幅を広げると、次のようになります。

![](images/gui/adjustmode_example_resized.png)

では、上下のバーを常に画面と同じ幅にするにはどうすればよいでしょうか。上下の灰色の背景パネルの Adjust Mode を Stretch に変更できます。

![](images/gui/adjustmode_example_resized_stretch.png)

これで改善しました。灰色の背景パネルは常にウィンドウの幅に合わせて伸縮するようになりますが、上部パネル内のバーと、下部にある2つのボックスは適切に配置されていません。上部のバーを左側に配置したままにするには、X Anchor を None から Left に変更する必要があります。

![](images/gui/adjustmode_example_top_anchor_left.png)

上部パネルは、これで意図したとおりになりました。上部パネル内のバーの Pivot は、すでに West に設定されていたため、バーの左端、つまり西側の端（Pivot）が親パネルの左端（X Anchor）に固定され、適切に配置されます。

次に、左のボックスの X Anchor を Left に、右のボックスの X Anchor を Right に設定すると、次のようになります。

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

これは期待どおりの結果ではありません。2つのボックスは、上部パネルの2本のバーと同じように、左右の端の近くに留まるはずです。こうなるのは、Pivot の設定が適切でないためです。

![](images/gui/adjustmode_example_bottom_pivot_center.png)

両方のボックスの Pivot は Center に設定されています。つまり、画面の幅が広がると、ボックスの中心点（ピボット）は端からの相対的な距離を維持します。左のボックスの場合、元の 640x1136 のウィンドウでは左端から 17% の位置にありました。

![](images/gui/adjustmode_example_original_ratio.png)

画面のサイズを変更しても、左のボックスの中心点は、左端から 17% という同じ距離に留まります。

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

左のボックスの Pivot を Center から West に、右のボックスの Pivot を East に変更してからボックスの位置を調整すると、画面のサイズを変更しても意図した結果が得られます。

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## 描画順序 {#draw-order}

すべてのノードは、「Nodes」フォルダー内に並んでいる順序で描画されます。一覧の先頭にあるノードが最初に描画されるため、他のすべてのノードの背後に表示されます。一覧の最後にあるノードは最後に描画されるため、他のすべてのノードの手前に表示されます。ノードの Z 値を変更しても描画順序は変わりません。ただし、Z 値をレンダースクリプトの描画範囲外に設定すると、そのノードは画面に描画されなくなります。レイヤーを使用して、ノードのインデックス順序を上書きできます（後述）。

![描画順序](images/gui/draw_order.png)

ノードを選択して <kbd>Alt + Up/Down</kbd> を押すと、ノードを上下に移動し、インデックス順序を変更できます。

描画順序はスクリプトでも変更できます。

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## 親子階層 {#parent-child-hierarchies}

ノードを、親にしたいノードの上にドラッグすると、そのノードの子になります。親を持つノードは、親に適用されたトランスフォーム（transform、位置、回転、スケール）を、親のピボットを基準として継承します。

![親子関係](images/gui/parent_child.png)

親は子より先に描画されます。レイヤーを使用すると、親ノードと子ノードの描画順序を変更し、ノードの描画を最適化できます（後述）。


## レイヤーとドローコール {#layers-and-draw-calls}

レイヤーを使用すると、ノードの描画方法を細かく制御でき、GUI シーンの描画のためにエンジンが生成するドローコール（draw call）の数を減らせます。エンジンは GUI シーンのノードを描画する際、次の条件に基づいて、ノードをドローコールのバッチにまとめます。

- ノードが同じ種類である必要があります。
- ノードが同じアトラスまたはタイルソースを使用している必要があります。
- ノードが同じブレンドモードで描画される必要があります。
- 同じフォントを使用している必要があります。

いずれかの点で直前のノードと異なるノードがあると、バッチが分割され、別のドローコールが生成されます。クリッピングノードは常にバッチを分割し、ステンシルの各スコープでもバッチが分割されます。

ノードを階層に配置できるため、管理しやすい単位にまとめるのは簡単です。ただし、異なる種類のノードを混在させると、その階層によってバッチ描画が分割されてしまいます。

![バッチを分割する階層](images/gui/break_batch.png)

レンダリングパイプラインがノードの一覧を順に処理する際、ノードの種類が異なるため、各ノードに個別のバッチを設定する必要があります。この3つのボタンには、合計6回のドローコールが必要です。

ノードにレイヤーを割り当てると、ノードの順序を変更でき、レンダリングパイプラインがノードをより少ないドローコールにまとめられます。まず、必要なレイヤーをシーンに追加します。*Outline* で「Layers」フォルダーのアイコンを <kbd>右クリック</kbd> し、<kbd>Add ▸ Layer</kbd> を選択します。新しいレイヤーを選択して、*Properties* ビューで *Name* プロパティを設定します。

![レイヤー](images/gui/layers.png)

次に、各ノードの *Layer* プロパティを対応するレイヤーに設定します。レイヤーの描画順序は、通常のノードのインデックス順序より優先されます。そのため、ボタンのグラフィックスを表示するボックスノードを「graphics」に、ボタンのテキストノードを「text」に設定すると、描画順序は次のようになります。

* 最初に「graphics」レイヤー内のすべてのノードを上から順に描画します。

  1. "button-1"
  2. "button-2"
  3. "button-3"

* 次に「text」レイヤー内のすべてのノードを上から順に描画します。

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

これで、ノードを6回ではなく2回のドローコールにまとめられます。パフォーマンスが大幅に向上します。

レイヤーが設定されていない子ノードは、親ノードのレイヤー設定を暗黙的に継承します。ノードにレイヤーを設定しない場合、そのノードは暗黙的に「null」レイヤーに追加され、他のどのレイヤーよりも先に描画されます。
