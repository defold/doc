---
title: Defold のデバイス入力
brief: このマニュアルでは、入力の仕組み、入力アクションの取得方法、操作に反応するスクリプトの作成方法を説明します。
---

# 入力 {#input}

エンジンはユーザーからのすべての入力を取得し、入力フォーカス（input focus）を取得したゲームオブジェクト（game object）内にある、`on_input()` 関数を実装したスクリプトコンポーネント（script component）と GUI スクリプトコンポーネントにアクション（action）として配信します。このマニュアルでは、入力を取得するための入力バインディング（input binding）の設定方法と、入力に反応するコードの作成方法を説明します。

入力システムは、シンプルで強力な概念をいくつか組み合わせており、ゲームに合った方法で入力を管理できます。

![入力バインディング](images/input/overview.png)

デバイス
: コンピューターやモバイルデバイスに内蔵または接続された入力デバイスは、システムレベルの未加工の入力を Defold ランタイムに渡します。次の種類のデバイスがサポートされています。

  1. キーボード（単一のキー入力とテキスト入力）
  2. マウス（位置、ボタンのクリック、マウスホイールの操作）
  3. シングルタッチとマルチタッチ（iOS デバイス、Android デバイス、およびモバイルの HTML5）
  4. ゲームパッド（オペレーティングシステムでサポートされ、[gamepads](/manuals/input-gamepads/#gamepads-settings-file) ファイルでマッピングされているもの）

入力バインディング
: 入力がスクリプトに送信される前に、デバイスからの未加工の入力は、入力バインディングテーブルを通じて意味のある *アクション* に変換されます。

アクション
: アクションは、入力バインディングファイルに列挙した名前（ハッシュ化されたもの）によって識別されます。各アクションには、ボタンが押されたか離されたか、マウスやタッチの座標など、入力に関するデータも含まれます。

入力リスナー（input listener）
: スクリプトコンポーネントや GUI スクリプトは、*入力フォーカスを取得する* ことで入力アクションを受信できます。複数のリスナーを同時にアクティブにできます。

入力スタック（input stack）
: 入力リスナーのリストです。最初にフォーカスを取得したリスナーがスタックの一番下に、最後に取得したリスナーが一番上に置かれます。

入力の消費
: スクリプトは受信した入力を消費することを選択でき、その場合はスタックの下にあるリスナーへの入力の伝播を止めます。

## 入力バインディングの設定 {#setting-up-input-bindings}

入力バインディングはプロジェクト全体に適用されるテーブルです。デバイスからの入力をスクリプトコンポーネントや GUI スクリプトに配信する前に、名前を付けた *アクション* へどう変換するかを指定できます。新しい入力バインディングファイルを作成するには、*Assets* ビュー内の場所を <kbd>右クリック</kbd> し、<kbd>New... ▸ Input Binding</kbd> を選択します。エンジンが新しいファイルを使うようにするには、*game.project* の *Game Binding* 項目を変更します。

![入力バインディングの設定](images/input/setting.png)

すべての新規プロジェクトテンプレートでは、デフォルトの入力バインディングファイルが自動的に作成されるため、通常は新しいバインディングファイルを作成する必要はありません。デフォルトのファイル名は `game.input_binding` で、プロジェクトのルートにある `input` フォルダーにあります。ファイルを <kbd>ダブルクリック</kbd> してエディターで開きます。

![入力バインディングの編集](images/input/input_binding.png)

新しいバインディングを作成するには、該当するトリガーの種類のセクションの下部にある <kbd>+</kbd> ボタンをクリックします。各項目には2つのフィールドがあります。

*Input*
: 受信対象となる未加工の入力です。利用可能な入力のスクロールリストから選択します。

*Action*
: 入力アクションが作成されてスクリプトに配信されるときに付けられるアクション名です。同じアクション名を複数の入力に割り当てることができます。たとえば、<kbd>Space</kbd> キーとゲームパッドの `A` ボタンをアクション `jump` にバインドできます。ただし、残念ながらタッチ入力には他の入力と同じアクション名を付けられないという既知のバグがあります。

## トリガーの種類 {#trigger-types}

デバイスに対応した5種類の入力トリガー（input trigger）を作成できます。

Key Triggers
: キーボードの単一のキー入力です。各キーは、対応するアクションに個別にマッピングされます。詳しくは、[キー入力とテキスト入力のマニュアル](/manuals/input-key-and-text)を参照してください。

Text Triggers
: テキストトリガーは、任意のテキスト入力を読み取るために使います。詳しくは、[キー入力とテキスト入力のマニュアル](/manuals/input-key-and-text)を参照してください。

Mouse Triggers
: マウスのボタンとスクロールホイールからの入力です。詳しくは、[マウス入力とタッチ入力のマニュアル](/manuals/input-mouse-and-touch)を参照してください。

Touch Triggers
: シングルタッチとマルチタッチのトリガーを、iOS デバイスと Android デバイスのネイティブアプリケーションおよび HTML5 バンドルで利用できます。詳しくは、[マウス入力とタッチ入力のマニュアル](/manuals/input-mouse-and-touch)を参照してください。

Gamepad Triggers
: ゲームパッドトリガーを使うと、標準的なゲームパッド入力をゲームの機能にバインドできます。詳しくは、[ゲームパッドのマニュアル](/manuals/input-gamepads)を参照してください。

### 加速度計の入力 {#accelerometer-input}

上記の5種類のトリガーに加えて、Defold は Android と iOS のネイティブアプリケーションで加速度計の入力もサポートしています。*game.project* ファイルの *Input* セクションで *Use Accelerometer* チェックボックスをオンにします。

```lua
function on_input(self, action_id, action)
    if action.acc_x and action.acc_y and action.acc_z then
        -- react to accelerometer data
    end
end
```

## 入力フォーカス {#input-focus}

スクリプトコンポーネントや GUI スクリプトで入力アクションを受信するには、コンポーネントを持つゲームオブジェクトに `acquire_input_focus` メッセージを送信します。

```lua
-- tell the current game object (".") to acquire input focus
msg.post(".", "acquire_input_focus")
```

このメッセージは、ゲームオブジェクト内の入力を受け取れるコンポーネント（スクリプトコンポーネント、GUI コンポーネント、コレクションプロキシ（collection proxy））を *入力スタック* に追加するようエンジンに指示します。ゲームオブジェクトのコンポーネントは入力スタックの上に置かれ、最後に追加されたコンポーネントがスタックの一番上になります。ゲームオブジェクトに入力を受け取れるコンポーネントが複数ある場合は、すべてがスタックに追加される点に注意してください。

![入力スタック](images/input/input_stack.png)

すでに入力フォーカスを取得しているゲームオブジェクトが再度フォーカスを取得すると、そのコンポーネントがスタックの一番上に移動します。


## 入力の配信と on_input() {#input-dispatch-and-on_input}

入力アクションは、入力スタックの順序に従って上から下へ配信されます。

![アクションの配信](images/input/actions.png)

スタック上にあり、`on_input()` 関数を持つコンポーネントでは、そのフレーム内の入力アクションごとに1回、次の引数を指定してその関数が呼び出されます。

`self`
: 現在のスクリプトインスタンスです。

`action_id`
: 入力バインディングで設定されたアクション名のハッシュです。

`action`
: 入力の値、位置（絶対位置と位置の差分）、ボタン入力が `pressed` であったかなど、アクションに関する有用なデータを含むテーブルです。利用可能なアクションのフィールドについて詳しくは、[on_input()](/ref/go#on_input) を参照してください。

```lua
function on_input(self, action_id, action)
  if action_id == hash("left") and action.pressed then
    -- move left
    local pos = go.get_position()
    pos.x = pos.x - 100
    go.set_position(pos)
  elseif action_id == hash("right") and action.pressed then
    -- move right
    local pos = go.get_position()
    pos.x = pos.x + 100
    go.set_position(pos)
  end
end
```


### 入力フォーカスとコレクションプロキシコンポーネント {#input-focus-and-collection-proxy-components}

コレクションプロキシを通じて動的に読み込まれる各ゲームワールド（game world）は、それぞれ独自の入力スタックを持ちます。配信されるアクションが読み込まれたワールドの入力スタックに届くには、プロキシコンポーネントがメインワールドの入力スタック上にある必要があります。読み込まれたワールドのスタック上のすべてのコンポーネントを処理してから、メインスタックの下への配信を続けます。

![プロキシへのアクションの配信](images/input/proxy.png)

::: important
コレクションプロキシコンポーネントを持つゲームオブジェクトに `acquire_input_focus` を送信し忘れるのは、よくある間違いです。この手順を省略すると、読み込まれたワールドの入力スタック上のどのコンポーネントにも入力が届きません。
:::


### 入力の解放 {#releasing-input}

入力アクションの受信を停止するには、ゲームオブジェクトに `release_input_focus` メッセージを送信します。このメッセージは、そのゲームオブジェクトのコンポーネントを入力スタックから取り除きます。

```lua
-- tell the current game object (".") to release input focus.
msg.post(".", "release_input_focus")
```


## 入力の消費 {#consuming-input}

コンポーネントの `on_input()` では、アクションをスタックの下へさらに渡すかどうかを制御できます。

- `on_input()` が `false` を返す場合や、戻り値を省略した場合（この場合は `nil` が返され、Lua では偽の値として扱われます）、入力アクションは入力スタック上の次のコンポーネントに渡されます。
- `on_input()` が `true` を返す場合、入力は消費されます。入力スタックの下にあるコンポーネントは、その入力を受け取りません。これは *すべての* 入力スタックに適用される点に注意してください。プロキシで読み込まれたワールドのスタック上のコンポーネントが入力を消費し、メインスタック上のコンポーネントに入力が届かないようにすることもできます。

![入力の消費](images/input/consuming.png)

入力の消費は、ゲームのさまざまな部分の間で入力の受信先を切り替えるシンプルで強力な方法で、多くの場面で役立ちます。たとえば、一時的にゲーム内で入力を受け取る唯一の部分となるポップアップメニューが必要な場合です。

![入力の消費](images/input/game.png)

ポーズメニューは最初は非表示（無効）になっており、プレイヤーが HUD の `PAUSE` 項目に触れると有効になります。

```lua
function on_input(self, action_id, action)
    if action_id == hash("mouse_press") and action.pressed then
        -- Did the player press PAUSE?
        local pausenode = gui.get_node("pause")
        if gui.pick_node(pausenode, action.x, action.y) then
            -- Tell the pause menu to take over.
            msg.post("pause_menu", "show")
        end
    end
end
```

![ポーズメニュー](images/input/game_paused.png)

ポーズメニューの GUI は入力フォーカスを取得して入力を消費し、ポップアップメニューに関係するもの以外の入力を受け付けなくします。

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("show") then
    -- Show the pause menu.
    local node = gui.get_node("pause_menu")
    gui.set_enabled(node, true)

    -- Acquire input.
    msg.post(".", "acquire_input_focus")
  end
end

function on_input(self, action_id, action)
  if action_id == hash("mouse_press") and action.pressed then

    -- do things...

    local resumenode = gui.get_node("resume")
    if gui.pick_node(resumenode, action.x, action.y) then
        -- Hide the pause menu
        local node = gui.get_node("pause_menu")
        gui.set_enabled(node, false)

        -- Release input.
        msg.post(".", "release_input_focus")
    end
  end

  -- Consume all input. Anything below us on the input stack
  -- will never see input until we release input focus.
  return true
end
```
