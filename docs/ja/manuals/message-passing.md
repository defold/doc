---
title: Defold のメッセージパッシング
brief: メッセージパッシングは、疎結合のオブジェクト間で通信するために Defold が使用する仕組みです。このマニュアルでは、この仕組みを詳しく説明します。
---

# メッセージパッシング {#message-passing}

メッセージパッシング（message passing）は、Defold のゲームオブジェクト（game object）同士がメッセージで通信する仕組みです。このマニュアルでは、Defold の [アドレス指定の仕組み](/manuals/addressing) と [基本構成要素](/manuals/building-blocks) を基本的に理解していることを前提とします。

Defold では、Java、C++、C# のように、継承やオブジェクトのメンバー関数を使ったクラス階層を構築してアプリケーションを定義するという意味でのオブジェクト指向は採用していません。その代わりに、シンプルで強力なオブジェクト指向設計によって Lua を拡張しています。この設計では、オブジェクトの状態はスクリプトコンポーネント（script component）の内部に保持され、`self` 参照を通じてアクセスできます。さらに、オブジェクト間の通信手段として非同期のメッセージパッシングを使うことで、オブジェクト同士の結合を完全になくせます。


## 使用例 {#usage-examples}

まず、簡単な使用例をいくつか見てみましょう。次の要素で構成されるゲームを作るとします。

1. 起動時に読み込まれるメインのブートストラップコレクション（bootstrap collection）には、GUI コンポーネントを持つゲームオブジェクトが含まれます（GUI はミニマップとスコアカウンターで構成されます）。ID が「level」のコレクション（collection）もあります。
2. 「level」という名前のコレクションには、主人公のプレイヤーキャラクターと敵の2つのゲームオブジェクトが含まれます。

![メッセージパッシングの構造](images/message_passing/message_passing_structure.png)

::: sidenote
この例の内容は、2つの別々のファイルに保存されています。メインのブートストラップコレクションのファイルが1つ、ID が「level」のコレクションのファイルが1つです。ただし、Defold ではファイル名は _重要ではありません_。重要なのは、インスタンスに割り当てる識別子です。
:::

このゲームには、オブジェクト間の通信が必要な簡単な仕組みがいくつかあります。

![メッセージパッシング](images/message_passing/message_passing.png)

① 主人公が敵を殴る
: この仕組みの一部として、「hero」のスクリプトコンポーネントから「enemy」のスクリプトコンポーネントに `"punch"` メッセージを送信します。両方のオブジェクトはコレクション階層の同じ場所にあるため、相対アドレスでの指定を推奨します。

  ```lua
  -- Send "punch" from the "hero" script to "enemy" script
  msg.post("enemy#controller", "punch")
  ```

  このゲームのパンチの強さは1種類だけなので、メッセージには「punch」という名前以外の情報を含める必要がありません。

  敵のスクリプトコンポーネントに、メッセージを受信する関数を作成します。

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("punch") then
      self.health = self.health - 100
    end
  end
  ```

  この場合、コードが確認するのはメッセージの名前だけです（`message_id` パラメーターでハッシュ化された文字列として送信されます）。メッセージデータや送信元は確認しないため、 *誰が* 「punch」メッセージを送信しても、かわいそうな敵はダメージを受けます。

② 主人公がスコアを獲得する
: プレイヤーが敵を倒すたびに、プレイヤーのスコアが増えます。同時に、「hero」ゲームオブジェクトのスクリプトコンポーネントから「interface」ゲームオブジェクトの「gui」コンポーネントに `"update_score"` メッセージを送信します。

  ```lua
  -- Enemy defeated. Increase score counter by 100.
  self.score = self.score + 100
  msg.post("/interface#gui", "update_score", { score = self.score })
  ```

  この場合、「interface」は命名階層のルートにあり、「hero」はルートにないため、相対アドレスを使えません。メッセージの送信先である GUI コンポーネントにはスクリプトが割り当てられているため、メッセージに応じた処理ができます。スクリプト、GUI スクリプト、レンダースクリプトの間では自由にメッセージを送信できます。

  `"update_score"` メッセージにはスコアデータを添えます。データは `message` パラメーターで Lua テーブルとして渡されます。

  ```lua
  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    end
  end
  ```

③ ミニマップ上の敵の位置
: プレイヤーが敵の位置を把握して追跡できるように、画面上にミニマップを表示します。それぞれの敵は、「interface」ゲームオブジェクトの「gui」コンポーネントに `"update_minimap"` メッセージを送信して、自身の位置を知らせます。

  ```lua
  -- Send the current position to update the interface minimap
  local pos = go.get_position()
  msg.post("/interface#gui", "update_minimap", { position = pos })
  ```

  GUI スクリプトのコードは各敵の位置を追跡する必要があり、同じ敵が新しい位置を送信した場合は古い位置を置き換える必要があります。位置を格納する Lua テーブルのキーとして、メッセージの送信元（`sender` パラメーターで渡されます）を使えます。

  ```lua
  function init(self)
    self.minimap_positions = {}
  end

  local function update_minimap(self)
    for url, pos in pairs(self.minimap_positions) do
      -- update position on map
      ...
    end
  end

  function on_message(self, message_id, message, sender)
    if message_id == hash("update_score") then
      -- set the score counter to new score
      local score_node = gui.get_node("score")
      gui.set_text(score_node, "SCORE: " .. message.score)
    elseif message_id == hash("update_minimap") then
      -- update the minimap with new positions
      self.minimap_positions[sender] = message.position
      update_minimap(self)
    end
  end
  ```

## メッセージの送信 {#sending-messages}

上で見たように、メッセージを送信する仕組みはとても簡単です。`msg.post()` 関数を呼び出すと、メッセージがメッセージキューに追加されます。その後、エンジンはフレームごとにキューを処理し、各メッセージを送信先のアドレスに届けます。一部のシステムメッセージ（`"enable"`、`"disable"`、`"set_parent"` など）は、エンジンのコードが処理します。エンジン自身もシステムメッセージ（物理衝突時の `"collision_response"` など）を生成して、オブジェクトに届けます。スクリプトコンポーネントに送られたユーザー定義メッセージの場合、エンジンは `on_message()` という名前の Defold 固有の Lua 関数を呼び出すだけです。

既存の任意のオブジェクトやコンポーネントに任意のメッセージを送信でき、そのメッセージに応答するかどうかは受信先のコードに任されています。スクリプトコンポーネントにメッセージを送信し、そのスクリプトのコードがメッセージを無視しても問題ありません。メッセージを処理する責任は、すべて受信側にあります。

エンジンはメッセージの送信先アドレスを確認します。不明な受信先にメッセージを送信しようとすると、Defold はコンソールにエラーを表示します。

```lua
-- Try to post to a non existing object
msg.post("dont_exist#script", "hello")
```

```txt
ERROR:GAMEOBJECT: Instance '/dont_exists' could not be found when dispatching message 'hello' sent from main:/my_object#script
```

`msg.post()` 呼び出しの完全な形式は次のとおりです。

`msg.post(receiver, message_id, [message])`

receiver
: 送信先のコンポーネントまたはゲームオブジェクトの ID です。ゲームオブジェクトを送信先に指定すると、そのゲームオブジェクト内のすべてのコンポーネントにメッセージが一斉送信されます。

message_id
: メッセージの名前を表す文字列、またはハッシュ化された文字列です。

[message]
: メッセージデータをキーと値のペアで格納する、省略可能な Lua テーブルです。メッセージの Lua テーブルには、ほぼすべての型のデータを含められます。数値、文字列、真偽値、URL、ハッシュ、入れ子のテーブルを渡せます。関数は渡せません。

  ```lua
  -- Send table data containing a nested table
  local inventory_table = { sword = true, shield = true, bow = true, arrows = 9 }
  local stats = { score = 100, stars = 2, health = 4, inventory = inventory_table }
  msg.post("other_object#script", "set_stats", stats)
  ```

::: sidenote
`message` パラメーターのテーブルサイズには、2キロバイトという上限があります。現在、テーブルが消費する正確なメモリサイズを簡単に調べる方法はありませんが、テーブルを挿入する前後に `collectgarbage("count")` を使うと、メモリ使用量を確認できます。
:::

### 省略形 {#shorthands}

Defold には、完全な URL を指定せずにメッセージを送信できる、便利な2つの省略形があります。

:[Shorthands](../shared/url-shorthands.md)


## メッセージの受信 {#receiving-messages}

メッセージを受信するには、送信先のスクリプトコンポーネントに `on_message()` という名前の関数を用意します。この関数は4つのパラメーターを受け取ります。

`function on_message(self, message_id, message, sender)`

`self`
: スクリプトコンポーネント自身への参照です。

`message_id`
: メッセージの名前を格納します。名前は _ハッシュ化されています_。

`message`
: メッセージデータを格納します。これは Lua テーブルです。データがない場合、テーブルは空です。

`sender`
: 送信元の完全な URL を格納します。

```lua
function on_message(self, message_id, message, sender)
    print(message_id) --> hash: [my_message_name]

    pprint(message) --> {
                    -->   score = 100,
                    -->   value = "some string"
                    --> }

    print(sender) --> url: [main:/my_object#script]
end
```

## ゲームワールド間のメッセージ通信 {#messaging-between-game-worlds}

コレクションプロキシ（collection proxy）コンポーネントを使って新しいゲームワールド（game world）をランタイムに読み込む場合、ゲームワールド間でメッセージをやり取りすることがあるでしょう。プロキシ経由でコレクションを読み込み、そのコレクションの *Name* プロパティが「level」に設定されているとします。

![コレクションの名前](images/message_passing/collection_name.png)

コレクションの読み込み、初期化、有効化が完了すると、受信先アドレスの「socket」フィールドにゲームワールド名を指定することで、新しいワールド内の任意のコンポーネントやオブジェクトにメッセージを送信できます。

```lua
-- Send a message to the player in the new game world
msg.post("level:/player#controller", "wake_up")
```
プロキシの仕組みについて詳しくは、[コレクションプロキシ](/manuals/collection-proxy) のドキュメントを参照してください。

## メッセージチェーン {#message-chains}

送信されたメッセージが実際に配送されると、受信先の `on_message()` が呼び出されます。メッセージに応答するコードが新しいメッセージを送信し、それがメッセージキューに追加されることはよくあります。

エンジンが配送を開始すると、メッセージキューを順に処理して、各メッセージの受信先の `on_message()` 関数を呼び出し、キューが空になるまで処理を続けます。配送処理を1巡する間にキューに新しいメッセージが追加された場合、もう1巡処理します。ただし、エンジンがキューを空にしようとする回数には上限があるため、実質的に、1フレーム内ですべてのメッセージを配送できるメッセージチェーンの長さにも制限があります。次のスクリプトを使うと、各 `update()` の間にエンジンが配送処理を何回繰り返すかを簡単に確認できます。

```lua
function init(self)
    -- We’re starting a long message chain during object init
    -- and keeps it running through a number of update() steps.
    print("INIT")
    msg.post("#", "msg")
    self.updates = 0
    self.count = 0
end

function update(self, dt)
    if self.updates < 5 then
        self.updates = self.updates + 1
        print("UPDATE " .. self.updates)
        print(self.count .. " dispatch passes before this update.")
        self.count = 0
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("msg") then
        self.count = self.count + 1
        msg.post("#", "msg")
    end
end
```

このスクリプトを実行すると、次のような出力が表示されます。

```txt
DEBUG:SCRIPT: INIT
INFO:ENGINE: Defold Engine 1.2.36 (5b5af21)
DEBUG:SCRIPT: UPDATE 1
DEBUG:SCRIPT: 10 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 2
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 3
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 4
DEBUG:SCRIPT: 75 dispatch passes before this update.
DEBUG:SCRIPT: UPDATE 5
DEBUG:SCRIPT: 75 dispatch passes before this update.
```

この Defold エンジンのバージョンでは、`init()` から最初の `update()` 呼び出しまでの間に、メッセージキューの配送処理が10回実行されることがわかります。その後は、各更新ループで75回実行されます。
