---
title: Defold のフリップブックアニメーションマニュアル
brief: このマニュアルでは、Defold でフリップブックアニメーションを使う方法を説明します。
---

# フリップブックアニメーション {#flip-book-animation}

フリップブックアニメーションは、静止画像を順番に表示して作るアニメーションです。従来のセルアニメーション（http://en.wikipedia.org/wiki/Traditional_animation を参照）に非常によく似た手法です。各フレームを個別に加工できるため、表現の可能性は無限にあります。ただし、多数の異なる画像を保存すると、大量のテクスチャメモリが必要になることがあります。アニメーションの滑らかさは1秒間に表示する画像数にも左右されますが、画像数を増やすと通常は制作の作業量も増えます。Defold のフリップブックアニメーションは、[アトラス](/manuals/atlas)に追加した個々の画像、または[タイルソース](/manuals/tilesource)内のタイルとして保存します。タイルソースのアニメーションでは、*Frames* リストで画像グリッドからタイルを選択し、繰り返しを含む任意の順序を指定できます。

  ![アニメーションシート](images/animation/animsheet.png){.inline}
  ![走る動作のループ](images/animation/runloop.gif){.inline}

## フリップブックアニメーションの再生 {#playing-flip-book-animations}

スプライト（sprite）と GUI ボックスノード（GUI box node）ではフリップブックアニメーションを再生でき、実行時に細かく制御できます。

スプライト
: 実行時にアニメーションを再生するには、[`sprite.play_flipbook()`](/ref/sprite/?q=play_flipbook#sprite.play_flipbook:url-id-[complete_function]-[play_properties]) 関数を使います。以下の例を参照してください。

GUI ボックスノード
: 実行時にアニメーションを再生するには、[`gui.play_flipbook()`](/ref/gui/?q=play_flipbook#gui.play_flipbook:node-animation-[complete_function]-[play_properties]) 関数を使います。以下の例を参照してください。

::: sidenote
再生モード `Once Ping Pong` は、アニメーションを最後のフレームまで再生してから順序を逆にし、最初のフレームではなく **2番目** のフレームまで戻って再生します。これは、アニメーションをつなげやすくするためです。
:::

### スプライトの例 {#sprite-example}

ゲームに、特定のボタンを押すとプレイヤーが回避できる「dodge」機能があるとします。この機能の状態を視覚的に伝えるために、4つのアニメーションを作成しました。

"idle"
: プレイヤーキャラクターが待機しているループアニメーションです。

"dodge_idle"
: プレイヤーキャラクターが回避姿勢のまま待機しているループアニメーションです。

"start_dodge"
: プレイヤーキャラクターが立った状態から回避姿勢に移る、1回だけ再生する遷移アニメーションです。

"stop_dodge"
: プレイヤーキャラクターが回避姿勢から立った状態に戻る、1回だけ再生する遷移アニメーションです。

次のスクリプトでロジックを実装します。

```lua

local function play_idle_animation(self)
    if self.dodge then
        sprite.play_flipbook("#sprite", hash("dodge_idle"))
    else
        sprite.play_flipbook("#sprite", hash("idle"))
    end
end

function on_input(self, action_id, action)
    -- "dodge" is our input action
    if action_id == hash("dodge") then
        if action.pressed then
            sprite.play_flipbook("#sprite", hash("start_dodge"), play_idle_animation)
            -- remember that we are dodging
            self.dodge = true
        elseif action.released then
            sprite.play_flipbook("#sprite", hash("stop_dodge"), play_idle_animation)
            -- we are not dodging anymore
            self.dodge = false
        end
    end
end
```

### GUI ボックスノードの例 {#gui-box-node-example}

ノードのアニメーションや画像を選択すると、実際には画像ソース（アトラスまたはタイルソース）とデフォルトのアニメーションを同時に割り当てています。画像ソースはノードに静的に設定されますが、現在再生するアニメーションは実行時に変更できます。静止画像は1フレームのアニメーションとして扱われるため、実行時に画像を変更することは、そのノードで別のフリップブックアニメーションを再生することと同じです。

```lua
function init(self)
    local character_node = gui.get_node("character")
    -- This requires that the node has a default animation in the same atlas or tile source as
    -- the new animation/image we're playing.
    gui.play_flipbook(character_node, "jump_left")
end
```


## 完了コールバック {#completion-callbacks}

`sprite.play_flipbook()` 関数と `gui.play_flipbook()` 関数は、最後の引数に省略可能な Lua コールバック関数を指定できます。この関数は、アニメーションが最後まで再生されたときに呼び出されます。ループアニメーションでは呼び出されません。このコールバックを使って、アニメーションの完了時にイベントを発生させたり、複数のアニメーションをつなげたりできます。以下に例を示します。

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    sprite.play_flipbook("#character", "jump_left", flipbook_done)
end
```

```lua
local function flipbook_done(self)
    msg.post("#", "jump_completed")
end

function init(self)
    gui.play_flipbook(gui.get_node("character"), "jump_left", flipbook_done)
end
```
