---
title: Defold のマウスとタッチ入力
brief: このマニュアルでは、マウスとタッチ入力の仕組みを説明します。
---

::: sidenote
Defold の入力の基本的な仕組み、入力の受信方法、スクリプトファイルで入力を受信する順序を理解しておくことをお勧めします。入力システムの詳細は、[入力の概要マニュアル](/manuals/input)を参照してください。
:::

# マウストリガー {#mouse-triggers}
マウストリガー（mouse trigger）を使用すると、マウスボタンやスクロールホイールからの入力をゲームのアクションにバインドできます。

![](images/input/mouse_bindings.png)

::: sidenote
マウスボタン入力の `MOUSE_BUTTON_LEFT`、`MOUSE_BUTTON_RIGHT`、`MOUSE_BUTTON_MIDDLE` は、それぞれ `MOUSE_BUTTON_1`、`MOUSE_BUTTON_2`、`MOUSE_BUTTON_3` と同等です。
:::

::: important
以下の例では、上の画像に示すアクションを使用します。ほかの入力と同様に、入力アクション（input action）の名前は自由に付けられます。
:::

## マウスボタン {#mouse-buttons}
マウスボタンは `pressed`、`released`、`repeated` イベントを生成します。次の例は、マウスの左ボタンが押された、または離されたことを検出する方法を示しています。

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") then
        if action.pressed then
            -- left mouse button pressed
        elseif action.released then
            -- left mouse button released
        end
    end
end
```

::: important
`MOUSE_BUTTON_LEFT`（または `MOUSE_BUTTON_1`）の入力アクションは、シングルタッチ入力でも送信されます。
:::

### マウスクリックとタッチの区別 {#distinguishing-mouse-clicks-from-touch}

`action.source` は、最初の押下を含め、物理マウスの押下とタッチが模擬するクリックを区別します。`MOUSE_BUTTON_LEFT` を `mouse_button_left` に割り当て、スクリプトまたは GUI スクリプトで以下を使います。

```lua
function init(self)
    msg.post(".", "acquire_input_focus")
end

function on_input(self, action_id, action)
    if action_id == hash("mouse_button_left") and action.pressed then
        if action.source == hash("mouse") then
            print("Mouse pressed at:", action.x, action.y)
        elseif action.source == hash("touch") then
            print("Touch pressed at:", action.x, action.y)
        end
    end
end
```

タッチをマウスクリックとして模擬する場合、別の Touch Trigger がなくても `hash("touch")` を報告します。タップを識別するために、`action.touch` テーブルや、先行する移動イベントは必要ありません。すべての入力元の値と、複数のバインディングがアクション名を共有する場合の動作は、[入力デバイスの種類](/manuals/input/#input-device-source)を参照してください。

iOS でこの区別を機能させるには、カスタムの `Info.plist` で `UIApplicationSupportsIndirectInputEvents` を有効にする必要があります。組み込みのマニフェストでは、すでに有効になっています。

## マウスホイール {#mouse-wheel}
マウスホイール入力はスクロール操作を検出します。ホイールがスクロールされた場合、`action.value` フィールドは `1` になり、それ以外の場合は `0` になります。（スクロール操作は、ボタンを押す操作と同じように扱われます。現在、Defold はタッチパッドでの細かなスクロール入力をサポートしていません。）

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_wheel_up") then
        if action.value == 1 then
            -- mouse wheel is scrolled up
        end
    end
end
```

## マウスの移動 {#mouse-movement}
マウスの移動は別個に処理されます。入力バインディング（input binding）に少なくとも1つのマウストリガーを設定しない限り、マウスの移動イベントは受信されません。

ポインター移動はアクション名に割り当てられません。`action_id` は `nil` で、`action` テーブルにはポインターの位置と移動差分が含まれます。入力元は、物理マウスなら `hash("mouse")`、タッチから模擬した移動なら `hash("touch")` です。加速度センサーのサンプルも `action_id == nil` を使うため、[入力デバイスの種類](/manuals/input/#input-device-source)の例のように入力元を確認して区別します。

```lua
function on_input(self, action_id, action)
    if action_id == nil and
        (action.source == hash("mouse") or action.source == hash("touch")) then
        -- let game object follow mouse/touch movement
        local pos = vmath.vector3(action.x, action.y, 0)
        go.set_position(pos)
    end
end
```

# タッチトリガー {#touch-triggers}
シングルタッチ型とマルチタッチ型のトリガーは、iOS および Android デバイスのネイティブアプリケーションと HTML5 バンドルで使用できます。

![](images/input/touch_bindings.png)

## シングルタッチ {#single-touch}
シングルタッチ型のトリガーは、入力バインディングの Touch Triggers セクションでは設定しません。代わりに、 **`MOUSE_BUTTON_LEFT` または `MOUSE_BUTTON_1` のマウスボタン入力を設定すると、シングルタッチトリガーが自動的に設定されます**。

## マルチタッチ {#multi-touch}
マルチタッチ型のトリガーは、アクションテーブル内の `touch` というテーブルにデータを格納します。このテーブルの要素には、`1`--`N` の整数インデックスが付けられます。`N` はタッチ点の数です。テーブルの各要素には、入力データを持つフィールドが含まれます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch_multi") then
        -- Spawn at each touch point
        for i, touchdata in ipairs(action.touch) do
            local pos = vmath.vector3(touchdata.x, touchdata.y, 0)
            factory.create("#factory", pos)
        end
    end
end
```

::: important
マルチタッチには、`MOUSE_BUTTON_LEFT` または `MOUSE_BUTTON_1` のマウスボタン入力と同じアクションを割り当ててはいけません。同じアクションを割り当てると、実質的にシングルタッチが上書きされ、シングルタッチイベントを一切受信できなくなります。
:::

::: sidenote
[Defold-Input アセット](https://defold.com/assets/defoldinput/)を使用すると、マルチタッチに対応したボタンやアナログスティックなど、画面上の仮想コントロールを簡単に設定できます。
:::


## オブジェクトのクリックやタップの検出 {#detecting-click-or-tap-on-objects}
表示されるコンポーネント（component）をユーザーがクリックまたはタップしたことを検出するのは、多くのゲームで必要になる、ごく一般的な操作です。ボタンなどの UI 要素への操作や、ストラテジーゲームでプレイヤーが操作するユニット、ダンジョン探索ゲームのレベル内にある宝物、RPG でクエストを依頼するキャラクターといったゲームオブジェクト（game object）への操作が考えられます。使用する方法は、表示するコンポーネントの種類によって異なります。

### GUI ノードへの操作の検出 {#detecting-interaction-with-gui-nodes}
UI 要素には `gui.pick_node(node, x, y)` 関数を使用できます。この関数は、指定した座標が GUI ノード（GUI node）の範囲内にあるかどうかに応じて `true` または `false` を返します。詳細は、[API ドキュメント](/ref/gui/#gui.pick_node:node-x-y)、[ポインターを重ねる例](/examples/gui/pointer_over/)、[ボタンの例](/examples/gui/button/)を参照してください。

### ゲームオブジェクトへの操作の検出 {#detecting-interaction-with-game-objects}
ゲームオブジェクトの場合は、カメラの平行移動やレンダースクリプト（render script）の投影などが必要な計算に影響するため、操作の検出がより複雑になります。ゲームオブジェクトへの操作を検出するには、大きく分けて2つの方法があります。

  1. ユーザーが操作できるゲームオブジェクトの位置とサイズを追跡し、マウスまたはタッチの座標がいずれかのオブジェクトの範囲内にあるかを確認します。
  2. ユーザーが操作できるゲームオブジェクトにコリジョンオブジェクト（collision object）を取り付け、マウスまたは指に追従するコリジョンオブジェクトを1つ用意し、それらの間の衝突を確認します。

::: sidenote
コリジョンオブジェクトを使ってユーザー入力を検出する、ドラッグとクリックに対応したすぐに使える実装が、[Defold-Input アセット](https://defold.com/assets/defoldinput/)にあります。
:::

どちらの場合も、マウスまたはタッチイベントのスクリーン座標と、ゲームオブジェクトのワールド座標の間で変換する必要があります。これにはいくつかの方法があります。

  * レンダースクリプトが使用するビューと投影を手動で追跡し、それらを使ってワールド空間との間で座標を変換します。[カメラマニュアルの例](/manuals/camera/#converting-mouse-to-world-coordinates)を参照してください。
  * [サードパーティーのカメラ実装](/manuals/camera/#third-party-camera-solutions)を使用し、提供されているスクリーン座標からワールド座標への変換関数を利用します。
