---
title: スクリプトでゲームロジックを書く
brief: このマニュアルでは、スクリプトコンポーネントを使ってゲームロジックを追加する方法を説明します。
---

# スクリプト {#scripts}

スクリプトコンポーネント（script component）を使うと、[Lua プログラミング言語](/manuals/lua)でゲームロジックを作成できます。


## スクリプトの種類 {#script-types}

Defold には3種類の Lua スクリプトがあり、それぞれ利用できる Defold ライブラリが異なります。

ゲームオブジェクトのスクリプト
: 拡張子は _.script_ です。このスクリプトは、ほかの[コンポーネント（component）](/manuals/components)と同じようにゲームオブジェクト（game object）に追加します。Defold は、エンジンのライフサイクル関数の一部として Lua コードを実行します。ゲームオブジェクトのスクリプトは通常、ゲームオブジェクトの制御と、レベルの読み込みやゲームルールなど、ゲーム全体をつなぐロジックに使います。ゲームオブジェクトのスクリプトからは、[GO](/ref/go) 関数と、[GUI](/ref/gui) および [Render](/ref/render) 関数を除くすべての Defold ライブラリ関数にアクセスできます。


GUI スクリプト
: 拡張子は _.gui_script_ です。GUI コンポーネントによって実行され、通常はヘッドアップディスプレイやメニューなどの GUI 要素を表示するために必要なロジックを記述します。Defold は、エンジンのライフサイクル関数の一部として Lua コードを実行します。GUI スクリプトからは、[GUI](/ref/gui) 関数と、[GO](/ref/go) および [Render](/ref/render) 関数を除くすべての Defold ライブラリ関数にアクセスできます。


レンダースクリプト
: 拡張子は _.render_script_ です。レンダリングパイプラインによって実行され、アプリケーションやゲームのすべてのグラフィックスを毎フレーム描画するために必要なロジックを記述します。レンダースクリプト（render script）は、ゲームのライフサイクルにおいて特別な位置を占めます。詳細は[アプリケーションのライフサイクルのドキュメント](/manuals/application-lifecycle)を参照してください。レンダースクリプトからは、[Render](/ref/render) 関数と、[GO](/ref/go) および [GUI](/ref/gui) 関数を除くすべての Defold ライブラリ関数にアクセスできます。


## スクリプトの実行、コールバック、self {#script-execution-callbacks-and-self}

Defold は、エンジンのライフサイクルの一部として Lua スクリプトを実行し、あらかじめ定義された一連のコールバック関数を通じてライフサイクルを公開します。スクリプトコンポーネントをゲームオブジェクトに追加すると、そのスクリプトはゲームオブジェクトとそのコンポーネントのライフサイクルの一部になります。スクリプトは読み込まれると Lua コンテキスト内で評価され、その後、エンジンは次の関数を実行し、現在のスクリプトコンポーネントのインスタンスへの参照をパラメーターとして渡します。この `self` 参照を使って、コンポーネントのインスタンスに状態を保存できます。

::: important
`self` は Lua テーブルのように動作する `userdata` オブジェクトですが、`pairs()` や `ipairs()` で反復処理することはできず、`pprint()` で出力することもできません。
:::

#### `init(self)`
コンポーネントが初期化されるときに呼び出されます。

```lua
function init(self)
  -- These variables are available through the lifetime of the component instance
  self.my_var = "something"
  self.age = 0
end
```

#### `final(self)`
コンポーネントが削除されるときに呼び出されます。たとえば、コンポーネントの削除時に削除する必要があるゲームオブジェクトを生成している場合など、後片付けに役立ちます。

```lua
function final(self)
  if self.my_var == "something" then
      -- do some cleanup
  end
end
```

#### `fixed_update(self, dt)`
フレームレートに依存しない更新です。パラメーター `dt` には、前回の更新からの経過時間が入ります。この関数は、フレームの時間と固定更新の頻度に応じて `0-N` 回呼び出されます。*game.project* で `Physics`-->`Use Fixed Timestep` が有効になっていて、`Engine`-->`Fixed Update Frequency` が0より大きい場合にのみ呼び出されます。安定した物理シミュレーションを実現するために、一定の間隔で物理オブジェクトを操作したいときに役立ちます。

```lua
function fixed_update(self, dt)
  msg.post("#co", "apply_force", {force = vmath.vector3(1, 0, 0), position = go.get_world_position()})
end
```

#### `update(self, dt)`
すべてのスクリプトの `fixed_update` コールバックの後に（Fixed Timestep が有効な場合）、毎フレーム1回呼び出されます。パラメーター `dt` には、前フレームからの経過時間が入ります。

```lua
function update(self, dt)
  self.age = self.age + dt -- increase age with the timestep
end
```

#### `late_update(self, dt)`
すべてのスクリプトの `update` コールバックの後、描画の直前に、毎フレーム1回呼び出されます。パラメーター `dt` には、前フレームからの経過時間が入ります。

```lua
function late_update(self, dt)
  go.set_position("/camera", self.final_camera_position)
end
```

#### on_message(self, message_id, message, sender)
[`msg.post()`](/ref/msg#msg.post) を通じてスクリプトコンポーネントにメッセージが送信されると、エンジンは受信先コンポーネントのこの関数を呼び出します。メッセージによる通信の詳細は、[メッセージパッシング（message passing）](/manuals/message-passing)を参照してください。

```lua
function on_message(self, message_id, message, sender)
    if message_id == hash("increase_score") then
        self.total_score = self.total_score + message.score
    end
end
```

#### `on_input(self, action_id, action)`
このコンポーネントが入力フォーカス（input focus）を取得している場合（[`acquire_input_focus`](/ref/go/#acquire_input_focus) を参照）、入力が検出されるとエンジンはこの関数を呼び出します。詳細は[入力処理](/manuals/input)を参照してください。

```lua
function on_input(self, action_id, action)
    if action_id == hash("touch") and action.pressed then
        print("Touch", action.x, action.y)
    end
end
```

#### `on_reload(self)`
この関数は、エディターのホットリロード（hot reload）機能（<kbd>Edit ▸ Reload Resource</kbd>）でスクリプトを再読み込みしたときに呼び出されます。デバッグ、テスト、微調整に非常に役立ちます。詳細は[ホットリロード](/manuals/hot-reload)を参照してください。

```lua
function on_reload(self)
  print(self.age) -- print the age of this game object
end
```


## リアクティブなロジック {#reactive-logic}

スクリプトコンポーネントを持つゲームオブジェクトには、何らかのロジックが実装されています。多くの場合、そのロジックは外部の要因に依存します。たとえば、敵の AI はプレイヤーがその AI から一定の半径内にいることに反応し、ドアはプレイヤーの操作によって解錠されて開く、といった具合です。

`update()` 関数を使うと、毎フレーム実行されるステートマシンとして定義した複雑な動作を実装できます。この方法が適切な場合もあります。しかし、`update()` を呼び出すたびにコストが発生します。この関数が本当に必要でなければ削除し、代わりにロジックを _リアクティブ（reactive）に_ 構築してみることをお勧めします。反応の対象となるデータを求めてゲームワールドを能動的に調べるよりも、反応のきっかけとなるメッセージを受動的に待つほうが、コストが低くなります。さらに、設計上の問題をリアクティブな方法で解決すると、設計と実装がより明快で安定したものになることもよくあります。

具体例を見てみましょう。スクリプトコンポーネントが初期化された2秒後にメッセージを送信するとします。その後、特定の応答メッセージを待ち、応答を受信した5秒後に別のメッセージを送信する必要があります。リアクティブでないコードは、次のようになります。

```lua
function init(self)
    -- Counter to keep track of time.
    self.counter = 0
    -- We need this to keep track of our state.
    self.state = "first"
end

function update(self, dt)
    self.counter = self.counter + dt
    if self.counter >= 2.0 and self.state == "first" then
        -- send message after 2 seconds
        msg.post("some_object", "some_message")
        self.state = "waiting"
    end
    if self.counter >= 5.0 and self.state == "second" then
        -- send message 5 seconds after we received "response"
        msg.post("another_object", "another_message")
        -- Nil the state so we don’t reach this state block again.
        self.state = nil
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("response") then
        -- “first” state done. enter next
        self.state = "second"
        -- zero the counter
        self.counter = 0
    end
end
```

このようにごく単純な場合でも、ロジックはかなり入り組んでしまいます。モジュール内のコルーチン（下記参照）を使って読みやすくすることもできますが、ここではリアクティブな形にして、組み込みのタイミング機構を使ってみましょう。

```lua
local function send_first()
	msg.post("some_object", "some_message")
end

function init(self)
	-- Wait 2s then call send_first()
	timer.delay(2, false, send_first)
end

local function send_second()
	msg.post("another_object", "another_message")
end

function on_message(self, message_id, message, sender)
	if message_id == hash("response") then
		-- Wait 5s then call send_second()
		timer.delay(5, false, send_second)
	end
end
```

こちらのほうが明快で、処理の流れも追いやすくなっています。ロジック全体を通して追うのが難しく、気付きにくいバグの原因にもなる内部の状態変数を取り除けます。また、`update()` 関数も完全に取り除けます。これにより、何もしていないときにも1秒に60回スクリプトを呼び出す負担から、エンジンを解放できます。


## プリプロセス {#preprocessing}

Lua プリプロセッサーと特別なマークアップを使うと、ビルドバリアントに応じて条件付きでコードを組み込めます。例:

```lua
-- Use one of the following keywords: RELEASE, DEBUG or HEADLESS
--#IF DEBUG
local lives_num = 999
--#ELSE 
local lives_num = 3
--#ENDIF
```

このプリプロセッサーはビルド拡張として利用できます。インストール方法と使い方の詳細は、[GitHub の拡張機能ページ](https://github.com/defold/extension-lua-preprocessor)を参照してください。


## エディターのサポート {#editor-support}

Defold エディターは、構文の色分けと自動補完による Lua スクリプトの編集をサポートしています。Defold の関数名を補完するには、*Ctrl+Space* を押すと、入力中の文字列に一致する関数の一覧が表示されます。

![自動補完](images/script/completion.png)
