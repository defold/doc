---
brief: Defold を初めて使う方に向けて、スクリプトのロジックと Defold の基本構成要素の一部を学びながら、スネークゲームを一から作成するガイドです。
layout: tutorial
title: Defold でスネークゲームを作る
difficulty: Beginner
---

# スネーク {#snake}

このチュートリアルでは、再現に挑戦できる定番ゲームの1つを作る手順を説明します。このゲームには多くのバリエーションがありますが、ここでは「食べ物」を食べ、食べたときにだけ体が伸びるヘビが登場します。このヘビは、障害物のあるプレイフィールドを進みます。

![サムネイル](images/snake/thumbnail.png)

### 学べること {#what-youll-learn}

このチュートリアルでは、次の方法を学びます。
- Defold でゲームを一から作成する
- 入力を設定して処理する
- タイルマップ（tile map）を作成し、実行時に変更する
- Lua でスクリプトを書く

### 初心者の方へ {#a-note-for-beginners}

このチュートリアルは初心者向けですが、Defold もゲーム開発もまったく初めての方には、まず入門マニュアル、特に [Defold の基本構成要素](/manuals/building-blocks/)と[用語集](/manuals/glossary/)を読むことをお勧めします。まだ Defold をダウンロードしていない場合は、[インストールマニュアル](/manuals/install/)を確認してください。エディター自体にすぐに慣れるために、[エディターの概要](/manuals/editor/)も確認することをお勧めします。このチュートリアルでも、各手順のスクリーンショットを掲載しています。

## プロジェクトの作成 {#creating-the-project}

Defold を起動し、次の操作をします。

1. 左側の *Create From* ▸ *Templates* を選択します。
2. *Empty Project* を選択します。
3. *Title* フィールドにプロジェクト名を入力します。
4. プロジェクトの *Location* を選択します。
5. *Create New Project* をクリックします。

![起動画面](images/snake/1.png)

<input type="checkbox"/> 完了！

## プロジェクト設定 {#project-settings}

まず、ゲームの解像度を定義します。

1. エディターが開いたら、左側の *Assets* ペインで `game.project` ファイルを探します。ダブルクリックして開きます。
2. `game.project` ファイルの *Display* セクションに移動します。
3. ゲームの寸法（`Width` と `Height`）を 768⨉768、またはほかの16の倍数に設定します。

![画面設定](images/snake/2.png)

この設定にするのは、各マスが 16x16 ピクセルのグリッド上にゲームを描画するためです。こうすることで、ゲーム画面の端でマスの一部が切れるのを防げます。`game.project` ファイルには、プロジェクトの重要な設定がすべて含まれています。各設定については、[プロジェクト設定マニュアル](/manuals/project-settings/)で確認できます。

<input type="checkbox"/> 完了！

## Assets ペインに新しいフォルダーを作成する {#creating-new-folders-in-the-assets-pane}

最小限のスネークゲームに必要なグラフィックスは、ごくわずかです。ヘビの体を構成する 16⨉16 の緑色のパーツ、障害物用の白いブロック、食べ物を表す少し小さな赤いブロックが、それぞれ1つあれば足ります。

まず、Defold エディターでアセット用のディレクトリを作成します。

1. `main` フォルダーを<kbd>右クリック</kbd>します。
2. `New Folder` を選択します。
3. 名前を入力するポップアップが表示されるので、`assets` と入力して `Create Folder` をクリックします。

![新しいフォルダー](images/snake/3.png)

<input type="checkbox"/> 完了！

## ゲームにグラフィックスを追加する {#adding-graphics-to-the-game}

必要なアセットは、次の画像だけです。

![スネークのスプライト](images/snake/snake.png)

1. 上の画像を<kbd>右クリック</kbd>して、ローカルディスクに保存します。次に、ダウンロードした画像を、先ほどプロジェクトフォルダー内に作成した場所へドラッグ＆ドロップ（またはコピー＆ペースト）します。

![新しいフォルダー](images/snake/4.png)

アセットのインポートについて詳しくは、[こちら](/manuals/importing-graphics/)も参照してください。

<input type="checkbox"/> 完了！

## タイルソースの追加 {#adding-a-tile-source}

Defold には組み込みの[タイルマップ](/manuals/tilemap/)コンポーネント（component）があり、これを使って、*タイル*をグリッド状に並べたプレイフィールドを作成します。タイルマップでは個々のタイルを設定したり読み取ったりできるため、このゲームにぴったりです。タイルマップのグラフィックスは[タイルソース（tile source）](/manuals/tilesource/)から取得するので、タイルソースを作成する必要があります。

1. `assets` フォルダーを<kbd>右クリック</kbd>します。
2. 「Resources」セクションの `New` ▸ `Tile Source` を選択します。
3. 新しいファイルに「snake」という名前を付けます（エディターは `snake.tilesource` として保存します）。

![新しいタイルソース](images/snake/5.png)

タイルソースは、この種類のファイル専用のタイルソースエディターで開きます。タイルソースを使えるようにするため、画像の指定を求められます。右側に `Properties` ペインがあります。

4. `Image` プロパティに、先ほどインポートしたグラフィックスファイルを設定します。
![タイルソース](images/snake/6.png)

5. `Width` と `Height` プロパティは、16（既定値）のままにします。これにより、32⨉32 ピクセルの画像が、1–4 の番号が付いた4つのタイルに分割されます。

![タイルソースのプロパティ](images/snake/7.png)

*Extrude Borders* プロパティが2ピクセルに設定されていることに注目してください。これは、端までグラフィックスが描かれているタイルの周囲に、表示の乱れが生じるのを防ぐためです。

ファイルを変更すると、タブのファイル名の横にアスタリスク `*` が表示されます。`File` ▸ `Save All` を選択するか、ショートカットの <kbd>Ctrl</kbd>+<kbd>S</kbd>（Mac では <kbd>⌘Cmd</kbd> + <kbd>S</kbd>）を使って、すべてのファイルを保存します。

<input type="checkbox"/> 完了！

## プレイフィールドのタイルマップを作成する {#creating-the-playfield-tile-map}

タイルソースの準備ができたので、プレイフィールドのタイルマップコンポーネントを作成します。

1. `main` フォルダーを<kbd>右クリック</kbd>して、「Components」セクションの <kbd>New</kbd> ▸ <kbd>Tile Map</kbd> を選択します。新しいファイルに「grid」という名前を付けます（エディターは「grid.tilemap」として保存します）。
![タイルマップの追加](images/snake/8.png)

2. タイルマップエディターが開き、**Tile Source** が必要であることが強調表示されます。*Tile Source* プロパティに、先ほど作成した「snake.tilesource」を設定します。
![タイルソースの設定](images/snake/9.png)

<input type="checkbox"/> 完了！

## タイルマップにタイルを描く {#drawing-tiles-in-the-tile-map}

Defold は、タイルマップの実際に使われている領域だけを保存します。そのため、画面の境界を埋めるだけのタイルを追加する必要があります。

1. 右側の `Outline` ペインで `layer1` レイヤーを選択します。
2. メニューの `Edit` ▸ `Select Tile...` またはショートカットの <kbd>Space</kbd> を選択してタイルパレットを表示し、描画に使うタイルをクリックします。
![タイルマップ](images/snake/10.png)

3. 画面の端を囲む枠と、いくつかの障害物を描きます。
![完成したタイルマップ](images/snake/11.png)

ゲーム画面を埋めるには、48x48 タイルのタイルマップが必要です（画面の大きさは 768、タイルの大きさは 16px なので、768/16 = 48 です）。

描き終えたら、タイルマップを保存します。

<input type="checkbox"/> 完了！

## ゲームにタイルマップを追加する {#adding-the-tile-map-to-the-game}

次に、タイルマップをゲームに追加する必要があります。Defold の基本構成要素をご存じなら、コンポーネントがゲームオブジェクト（game object）の一部であり、ゲームオブジェクトをコレクション（collection）内に定義できることをご存じでしょう。

1. `Assets` ペインで `main.collection` をダブルクリックして開きます。これは Empty Project テンプレートの既定のブートストラップコレクション（bootstrap collection）で、エンジンの起動時に読み込まれるコレクションです。

2. `Outline` のルートを<kbd>右クリック</kbd>し、`Add Game Object` を選択します。ゲーム開始時に読み込まれるコレクション内に、新しいゲームオブジェクトが作成されます。
![ゲームオブジェクトの追加](images/snake/12.png)

3. 新しいゲームオブジェクトを<kbd>右クリック</kbd>して、`Add Component File` を選択します。先ほど作成した「grid.tilemap」ファイルを選びます。
![コンポーネントの追加](images/snake/13.png)

これで、ゲームのコレクションにタイルマップが追加されました。エディターからゲームを実行すると、表示されるはずです。

1. `Project` ▸ `Build` を選択するか、ショートカットの <kbd>Ctrl</kbd> + <kbd>B</kbd>（Mac では <kbd>⌘Cmd</kbd> + <kbd>B</kbd>）を使います。

![ゲームの実行](images/snake/14.png)

<input type="checkbox"/> 完了！

## ゲームにスクリプトを追加する {#adding-a-script-to-the-game}

1. `Assets` ブラウザーで `main` フォルダーを<kbd>右クリック</kbd>し、Scripts セクションの `New` ▸ `Script` を選択します。新しいスクリプトファイルに「snake」という名前を付けます（「snake.script」として保存されます）。このファイルに、ゲームのすべてのロジックを記述します。
![スクリプトの追加](images/snake/15.png)

2. *main.collection* に戻り、タイルマップを持つゲームオブジェクトを<kbd>右クリック</kbd>します。<kbd>Add&nbsp;Component&nbsp;File</kbd> を選択し、「snake.script」ファイルを選びます。

![メインコレクション](images/snake/16.png)

これで、タイルマップコンポーネントとスクリプトが揃いました。

<input type="checkbox"/> 完了！

## ゲームのスクリプト {#the-game-script}

これから書くスクリプトで、ゲーム全体を動かします。機能を1つずつ追加していきます。

### 単純な移動アルゴリズム {#simple-movement-algorithm}

次のような仕組みで動かします。

1. スクリプトで、ヘビが現在占めているタイルの位置のリストを保持します。
2. プレイヤーが方向キーを押したら、ヘビが進む方向を保存します。
3. 一定の間隔で、現在の移動方向にヘビを1マス進めます。

### 初期化 {#initialization}

*snake.script* を開き、`init()` 関数を探します。この関数は、ゲーム開始時にスクリプトが初期化されるときにエンジンから呼び出されます。コードを次のように変更します。

```lua
function init(self)
    self.segments = { -- <1>
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0} -- <2>
    self.speed = 7.0 -- <3>
    self.time = 0 -- <4>
end
```

このコードでは、次の処理をします。

1. ヘビの体を構成する各パーツを、`self.segments` という Lua テーブル（table）に保存します。このテーブルは、各パーツの X と Y の位置を保持するテーブルのリストです。
2. 現在の方向を、X と Y の方向を保持する `self.dir` というテーブルに保存します。
3. 現在の移動速度を `self.speed` に保存します。速度は1秒あたりのタイル数で表します。
4. 移動速度の管理に使うタイマーの値を `self.time` に保存します。

上のスクリプトコードは Lua 言語で書かれています。コードについて知っておきたいことがいくつかありますが、以下の内容がまだわからなくても心配はいりません。そのまま読み進め、試しながら時間をかければ、やがて理解できるようになります。今は、`init()` でこれから使う変数を初期化したことを覚えておけば十分です。

- Defold には、スクリプトコンポーネント（script component）の生存期間中に呼び出される、組み込みのコールバック（callback）*関数*があらかじめ用意されています。これらはメソッド*ではなく*、通常の関数です。
- ランタイムは、`self` パラメーターを通じて、現在のスクリプトコンポーネントのインスタンス（instance）への参照を渡します。`self` 参照は、インスタンスのデータを保存するために使います。
- `self` 参照は、データを保存できる Lua テーブルとして使えます。ほかのテーブルと同じように、`self.data = "value"` のようなドット記法を使うだけです。この参照は、スクリプトの生存期間を通して有効です。この場合は、ゲームの開始から終了までです。
- Lua のテーブルリテラルは、波括弧 `{}` で囲んで記述します。
- テーブルの要素には、キーと値のペア（`{x = 10, y = 20}`）、入れ子になった Lua テーブル（`{ {a = 1}, {b = 2} }`）、またはほかのデータ型を使えます。

<input type="checkbox"/> 完了！

### 更新 {#update}

`init()` 関数は、実行中のゲーム内にスクリプトコンポーネントのインスタンスが作成されるときに、ちょうど1回呼び出されます。一方、`update()` 関数は**毎フレーム**1回呼び出されます。そのため、この関数はリアルタイムのゲームロジックに適しています。

更新処理では、設定した間隔で次の処理をします。

1. ヘビの頭の位置を調べ、その隣の、現在の移動方向にずらした位置に新しい頭を作ります。たとえば、ヘビの移動方向が X=1、Y=0 で、現在の頭の位置が X=0、Y=0 なら、新しい頭の位置は X=1、Y=0 になります。
2. 新しい頭の位置を、ヘビの体を構成するパーツのリストに保存します。
3. パーツのテーブルから尻尾の位置を取得します。
4. その位置にある尻尾のタイルを消します。
5. テーブル内の位置に、ヘビのすべてのパーツ（タイル）を描画します。

![アルゴリズム](images/snake/17.png)

:::sidenote
ヘビの頭はテーブルの末尾にあり、尻尾は先頭にあることを覚えておいてください。
:::

1. *snake.script* の `update()` 関数を探し、コードを次のように変更します。

```lua
function update(self, dt)
    self.time = self.time + dt -- <1>
    if self.time >= 1.0 / self.speed then -- <2>
        local head = self.segments[#self.segments] -- <3>

        local newhead = {
            x = head.x + self.dir.x,
            y = head.y + self.dir.y
        } -- <4>

        table.insert(self.segments, newhead) -- <5>

        local tail = table.remove(self.segments, 1) -- <6>

        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0) -- <7>

        for i, s in ipairs(self.segments) do -- <8>
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2) -- <9>
        end

        self.time = 0 -- <10>
    end
end
```

このコードでは、次の処理をします。

1. 前回 `update()` が呼び出されてからの経過時間（delta time）、つまり `dt` の秒数だけタイマーを進めます。
2. タイマーが十分に進んだら、次の処理をします。
3. 現在の頭の位置を取得します。`#` は、テーブルを配列として使っている場合に、その長さを取得する演算子です。今回もこれに該当し、すべてのパーツがキーを指定しないテーブルの値になっています。
4. 現在の頭の位置と移動方向（`self.dir`）に基づいて、新しい頭のパーツを作成します。
5. パーツのテーブルの末尾に、新しい頭を追加します。
6. パーツのテーブルの先頭から、尻尾を取り除きます。
7. 取り除いた尻尾の位置にあるタイルを消します。ここで使うタイルマップ `#grid` には、`layer1` というレイヤーが1つだけあります。
8. パーツのテーブルの要素を順に処理します。各反復で、`i` にはテーブル内の位置（1から始まります）が、`s` には現在のパーツが設定されます。
9. パーツの位置にあるタイルを値2（ヘビの緑色のタイル）に設定します。
10. 処理が終わったら、タイマーをゼロにリセットします。

ここでゲームを実行すると、4つのパーツからなるヘビがプレイフィールドを左から右へ進む様子が見えるはずです。

![ゲームの実行](images/snake/snake_run_1.png)

<input type="checkbox"/> 完了！

## プレイヤーの入力 {#player-input}

プレイヤーの入力に反応するコードを追加する前に、入力の対応付けを設定する必要があります。

### 入力バインディング {#input-bindings}

1. `input` フォルダー内の `game.input_binding` ファイルを探し、<kbd>ダブルクリック</kbd>して開きます。
2. 上下左右への移動に使う、一連の *Key Trigger* 入力バインディング（input binding）を追加します。*Input* 列でキーボードのキーを選択し、*Action* 列にアクション名を入力します。

![入力](images/snake/18.png)

入力バインディングファイルは、実際のユーザー入力（キー、マウスの移動など）を、アクションの*名前*に対応付けます。この名前は、入力を要求したスクリプトに渡されます。

<input type="checkbox"/> 完了！

### 入力フォーカスの取得 {#acquiring-input-focus}

バインディングを設定したら、*snake.script* を開き、入力フォーカス（input focus）を取得するために、`init()` 関数の先頭に次の行を追加します。

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0
end
```

追加した行では、次の処理をします。
1. 現在のゲームオブジェクト（「.」は現在のゲームオブジェクトの省略形です）にメッセージを送信し、エンジンからの入力の受信を開始するよう伝えます。

次に `on_input` 関数を探し、次のコードを入力します。

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then -- <1>
        self.dir.x = 0 -- <2>
        self.dir.y = 1
    elseif action_id == hash("down") and action.pressed then
        self.dir.x = 0
        self.dir.y = -1
    elseif action_id == hash("left") and action.pressed then
        self.dir.x = -1
        self.dir.y = 0
    elseif action_id == hash("right") and action.pressed then
        self.dir.x = 1
        self.dir.y = 0
    end
end
```

これらの `if...elseif...` 分岐では、次の処理をします。
1. 入力バインディングで設定した入力アクション（input action）「up」を受信し、`action` テーブルの `pressed` フィールドが `true`（プレイヤーがキーを押した）であれば、次の処理をします。
2. 移動方向を設定します。

ゲームをもう一度実行し、ヘビを操作できることを確認します。

<input type="checkbox"/> 完了！

### 入力処理の改善 {#improving-input-handling}

2つのキーを同時に押すと、それぞれのキー入力に対して1回ずつ、合計2回 `on_input()` が呼び出されることに注目してください。上のコードでは、後から呼び出された `on_input()` が `self.dir` の値を上書きするため、最後の呼び出しだけがヘビの方向に影響します。

また、ヘビが左に進んでいるときに <kbd>right</kbd> キーを押すと、ヘビが自分の体に向かって進んでしまうことにも注意してください。*一見*わかりやすい解決策は、`on_input()` の `if` 節に追加の条件を入れることです。

```lua
if action_id == hash("up") and self.dir.y ~= -1 and action.pressed then
    ...
elseif action_id == hash("down") and self.dir.y ~= 1 and action.pressed then
    ...
```

しかし、ヘビが左に進んでいるときに、次の移動が起こる前にプレイヤーが <kbd>up</kbd>、続いて <kbd>right</kbd> を*素早く*押すと、<kbd>right</kbd> の入力だけが反映され、ヘビは自分の体に向かって進んでしまいます。上に示した条件を `if` 節に追加すると、その入力は無視されます。*これでは困ります！*

この問題を適切に解決するには、入力をキューに保存し、ヘビが移動するたびに、そのキューから要素を取り出します。

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.speed = 7.0
    self.time = 0

    self.dirqueue = {} -- <1>
end
```

今回は、次の変更を加えます。
1. 空のテーブルとして初期化する変数 `self.dirqueue` を追加します。

`update()` 関数に次の処理を追加します。

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed then
        local newdir = table.remove(self.dirqueue, 1) -- <1>
        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y -- <2>
            if not opposite then
                self.dir = newdir -- <3>
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tail = table.remove(self.segments, 1)
        tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 0)

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)
        end

        self.time = 0
    end
end
```

1. 方向のキューから先頭の要素を取り出します。
2. 要素がある場合（`newdir` が null でない場合）、`newdir` が `self.dir` と反対方向を指しているかどうかを確認します。
3. 反対方向を指していない場合にだけ、新しい方向を設定します。

そして、現在の入力をキューに保存するように `on_input` を変更します。

```lua
function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1}) -- <1>
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

1. `self.dir` を直接設定する代わりに、入力された方向を方向のキューに追加します。

ゲームを起動し、期待どおりにプレイできることを確認します。

<input type="checkbox"/> 完了！

## 食べ物と障害物への衝突 {#food-and-collision-with-obstacles}

ヘビの体が伸びて移動速度が上がるように、マップ上に食べ物が必要です。食べ物を追加しましょう！

### 食べ物の生成 {#spawning-the-food}

`init()` 関数の上に、新しい関数を追加します。

```lua
local function put_food(self) -- <1>
    self.food = {x = math.random(2, 47), y = math.random(2, 47)} -- <2>
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3) -- <3>
end
```

この関数では、次の処理をします。
1. マップ上に食べ物を1つ配置する、`put_food()` という新しい関数を宣言します。
2. ランダムな X と Y の位置を、`self.food` という変数に保存します。
3. X と Y の位置にあるタイルを、食べ物のグラフィックスを表す値3に設定します。

次に、`init()` 関数の末尾でこの関数を呼び出します。
```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    math.randomseed(socket.gettime()) -- <1>
    put_food(self) -- <2>
end
```

1. `math.random()` で乱数の取得を始める前に、乱数のシードを設定します。設定しなければ、同じ乱数列が生成されます。このシードは1回だけ設定するようにします。
2. ゲーム開始時に `put_food()` 関数を呼び出し、マップ上に食べ物がある状態でプレイを始められるようにします。

<input type="checkbox"/> 完了！

### 食べ物を食べる {#eating-the-food}

ヘビが何かに衝突したかどうかを検出するには、ヘビの進む先のタイルマップに何があるかを調べて、対応する処理をするだけです。

ヘビが生きているかどうかを管理する変数を追加します。

```lua
function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true -- <1>

    math.randomseed(socket.gettime())
    put_food(self)
end
```

1. ヘビが生きているかどうかを表すフラグです。

次に、壁や障害物、食べ物との衝突を判定するロジックを追加します。

```lua
function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then -- <1>
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y) -- <2>

        if tile == 2 or tile == 4 then
            self.alive = false -- <3>
        elseif tile == 3 then
            self.speed = self.speed + 1 -- <4>
            put_food(self)
        else
            local tail = table.remove(self.segments, 1) -- <5>
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end
```

1. ヘビが生きている場合にだけ、ヘビを進めます。
2. タイルマップに描画する前に、ヘビの新しい頭の位置に何があるかを読み取ります。
3. タイルが障害物かヘビの体の別の部分であれば、ゲームオーバーです！
4. タイルが食べ物であれば、速度を上げ、新しい食べ物を配置します。
5. 尻尾を取り除くのは、衝突がなかった場合だけであることに注目してください。つまり、プレイヤーが食べ物を食べた場合は、その移動では尻尾を取り除かないので、ヘビの体がパーツ1つ分伸びます。

ゲームを試し、うまくプレイできることを確認しましょう！

チュートリアルはこれで終わりですが、引き続きゲームでいろいろ試し、以下の練習問題にも取り組んでみてください！

<input type="checkbox"/> 完了！

## スクリプト全体 {#the-complete-script}

参考として、スクリプトのコード全体を示します。

```lua
local function put_food(self)
    self.food = {x = math.random(2, 47), y = math.random(2, 47)}
    tilemap.set_tile("#grid", "layer1", self.food.x, self.food.y, 3)        
end

function init(self)
    msg.post(".", "acquire_input_focus")

    self.segments = {
        {x = 7, y = 24},
        {x = 8, y = 24},
        {x = 9, y = 24},
        {x = 10, y = 24}
    }
    self.dir = {x = 1, y = 0}
    self.dirqueue = {}
    self.speed = 7.0
    self.time = 0

    self.alive = true

    math.randomseed(socket.gettime())
    put_food(self)
end

function update(self, dt)
    self.time = self.time + dt
    if self.time >= 1.0 / self.speed and self.alive then
        local newdir = table.remove(self.dirqueue, 1)

        if newdir then
            local opposite = newdir.x == -self.dir.x or newdir.y == -self.dir.y
            if not opposite then
                self.dir = newdir
            end
        end

        local head = self.segments[#self.segments]
        local newhead = {x = head.x + self.dir.x, y = head.y + self.dir.y}

        table.insert(self.segments, newhead)

        local tile = tilemap.get_tile("#grid", "layer1", newhead.x, newhead.y)

        if tile == 2 or tile == 4 then
            self.alive = false
        elseif tile == 3 then
            self.speed = self.speed + 1
            put_food(self)
        else
            local tail = table.remove(self.segments, 1)
            tilemap.set_tile("#grid", "layer1", tail.x, tail.y, 1)
        end

        for i, s in ipairs(self.segments) do
            tilemap.set_tile("#grid", "layer1", s.x, s.y, 2)            
        end

        self.time = 0
    end
end

function on_input(self, action_id, action)
    if action_id == hash("up") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = 1})
    elseif action_id == hash("down") and action.pressed then
        table.insert(self.dirqueue, {x = 0, y = -1})
    elseif action_id == hash("left") and action.pressed then
        table.insert(self.dirqueue, {x = -1, y = 0})
    elseif action_id == hash("right") and action.pressed then
        table.insert(self.dirqueue, {x = 1, y = 0})
    end
end
```

## 練習問題 {#exercises}

次の改良を実装してみると、よい練習になります。

1. ゲームオーバーになったときに、キー入力でゲームを再開する処理を追加します。
2. 得点の計算とスコア表示を追加します。ラベルコンポーネント（label component）だけを使う方法（より簡単です）でも、GUI 全体を作る方法でもかまいません。
3. put_food() 関数は、ヘビの位置も障害物も考慮していません。空いている場所にだけ食べ物が生成されるように修正します。
4. ゲームオーバーになったら「Game Over」メッセージを表示し、プレイヤーがもう一度挑戦できるようにします。
5. 追加の課題: プレイヤーが操作するヘビをもう1匹追加します。
