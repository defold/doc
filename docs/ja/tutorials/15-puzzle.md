---
title: Defold で15パズルゲームを作る
brief: Defold を初めて使う方に向けて、いくつかの基本構成要素を試し、スクリプトのロジックを実行する方法を説明するガイドです。
---

# 定番の15パズル {#the-classic-15-puzzle}

このよく知られたパズルは、1870年代にアメリカで人気を集めました。パズルの目的は、盤面のタイルを横方向や縦方向に滑らせて、正しい順序に並べることです。パズルはタイルがばらばらに並んだ状態から始まります。

最も一般的なものでは、タイルに1--15の数字が書かれています。ただし、各タイルを1枚の画像の一部にすると、パズルを少し難しくできます。作り始める前に、パズルを解いてみましょう。空きマスに隣接するタイルをクリックすると、そのタイルが空きマスに移動します。

## プロジェクトの作成 {#creating-the-project}

1. Defold を起動します。
2. 左側の *New Project* を選択します。
3. *From Template* タブを選択します。
4. *Empty Project* を選択します。
5. ローカルドライブ上でプロジェクトの保存場所を選択します。
6. *Create New Project* をクリックします。

設定ファイル *game.project* を開き、ゲームのサイズを512⨉512に設定します。これは、これから使用する画像のサイズと一致します。

![画面の設定](images/15-puzzle/display_settings.png)

次に、パズルに適した画像をダウンロードします。正方形の画像ならどれでもかまいませんが、必ず512⨉512ピクセルに拡大または縮小してください。画像を探す手間を省きたい場合は、こちらを使えます。

![モナ・リザ](images/15-puzzle/monalisa.png)

画像をダウンロードしてから、プロジェクトの *main* フォルダーにドラッグします。

## グリッドの表現 {#representing-the-grid}

Defold には、パズルの盤面を表示するのにぴったりな *タイルマップ（Tilemap）* コンポーネント（component）が組み込まれています。タイルマップでは個々のタイルを設定したり読み取ったりできるので、このプロジェクトに必要な機能がすべて揃っています。

ただし、タイルマップを作成する前に、タイルマップがタイル画像を取得するための *タイルソース（Tilesource）* が必要です。

*main* フォルダーを <kbd>右クリック</kbd> し、<kbd>New ▸ Tile Source</kbd> を選択します。新しいファイルに `monalisa.tilesource` という名前を付けます。

タイルの *Width* プロパティと *Height* プロパティを128に設定します。これにより、512⨉512ピクセルの画像が16枚のタイルに分割されます。タイルマップに配置するとき、タイルには1--16の番号が付きます。

![タイルソース](images/15-puzzle/tilesource.png)

次に、*main* フォルダーを <kbd>右クリック</kbd> し、<kbd>New ▸ Tile Map</kbd> を選択します。新しいファイルに "grid.tilemap" という名前を付けます。

Defold ではグリッドを初期化する必要があります。そのためには、"layer1" レイヤーを選択し、原点のすぐ右上に4⨉4のタイルのグリッドを描きます。どのタイルを配置するかは、特に重要ではありません。少し後で、これらのタイルの内容を自動的に設定するコードを書きます。

![タイルマップ](images/15-puzzle/tilemap.png)

## 各要素の組み合わせ {#putting-the-pieces-together}

*main.collection* を開きます。*Outline* のルートノードを <kbd>右クリック</kbd> し、<kbd>Add Game Object</kbd> を選択します。新しいゲームオブジェクト（game object）の *Id* プロパティを "game" に設定します。

ゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component File</kbd> を選択します。ファイル *grid.tilemap* を選択します。*Id* プロパティを "tilemap" に設定します。

ゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component ▸ Label</kbd> を選択します。ラベル（label）の *Id* プロパティを "done" に、*Text* プロパティを "Well done" に設定します。ラベルをタイルマップの中央に移動します。

ラベルがグリッドより手前に描画されるように、ラベルの Z 座標を1に設定します。

![メインコレクション](images/15-puzzle/main_collection.png)

次に、パズルのロジックを記述する Lua スクリプトファイルを作成します。*main* フォルダーを <kbd>右クリック</kbd> し、<kbd>New ▸ Script</kbd> を選択します。新しいファイルに "game.script" という名前を付けます。

続いて、*main.collection* 内の "game" というゲームオブジェクトを <kbd>右クリック</kbd> し、<kbd>Add Component File</kbd> を選択します。ファイル *game.script* を選択します。

ゲームを実行します。描いたとおりのグリッドが表示され、その手前に "Well done" というメッセージのラベルが表示されるはずです。

## パズルのロジック {#the-puzzle-logic}

これですべての要素が揃ったので、チュートリアルの残りではパズルのロジックを組み立てていきます。

スクリプトでは、タイルマップとは別に、盤面のタイルを表す独自のデータを保持します。こうすると、タイルをより扱いやすい形にできます。タイルは2次元配列ではなく、Lua テーブル内の1次元リストとして格納します。このリストには、グリッドの左上隅から右下隅までのタイルの番号が順に並びます。

```lua
-- The completed board looks like this:
self.board = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}
```

このようなタイルのリストを受け取り、タイルマップに描画するコードはとても単純ですが、リスト内の位置を x 座標と y 座標に変換する必要があります。

```lua
-- Draw a table list of tiles onto a 4x4 tilemap
local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4) -- <1>
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end
```
1. タイルマップでは、x の値が1、y の値が1のタイルは左下にあります。そのため、y 座標を反転する必要があります。

テスト用の `init()` 関数を作成すると、この関数が意図したとおりに動作するか確認できます。

```lua
function init(self)
    -- An inverted board, for test
    self.board = {15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}
    draw(self.board)
end
```

タイルを Lua テーブルのリストに格納しておけば、順序をばらばらにするのはとても簡単です。コードでは、リストの各要素を順に処理し、各タイルをランダムに選んだ別のタイルと入れ替えるだけです。

```lua
-- Swap two items in a table list
local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

-- Randomize the order of a the elements in a table list
local function scramble(t)
    local n = #t
    for i = 1, n - 1 do
        t = swap(t, i, math.random(i, n))
    end
    return t
end
```

先に進む前に、15パズルについて必ず考慮すべき点があります。上記のようにタイルの順序をランダムにすると、50%の確率でパズルを解くことが *不可能* になります。

これは困ったことです。プレイヤーに解けないパズルを出すことは、絶対に避けたいからです。

幸い、ある配置が解けるかどうかは判定できます。その方法を説明します。

## 解けるかどうかの判定 {#solvability}

4⨉4のパズルの配置が解けるかどうかを判定するには、2つの情報が必要です。

1. 配置に含まれる「転倒（inversion）」の数です。転倒とは、あるタイルが、それより小さい数字のタイルよりも前にあることをいいます。たとえば、リスト `{1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 11, 10, 13, 14, 15, 0}` には、3つの転倒があります。

    - 12の後ろには11と10があるため、転倒は2つです。
    - 11の後ろには10があるため、転倒がさらに1つあります。

    （パズルが解けた状態の転倒数は0です。）

2. 空きマスがある行です（リストでは `0` で表します）。

この2つの数値は、次の関数で計算できます。

```lua
-- Count the number of inversions in a list of tiles
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then -- <1>
                inv = inv + 1
            end
        end
    end
    return inv
end
```
1. 空きマスは数に含めません。

```lua
-- Find the x and y position of a given tile
local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4) -- <1>
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end
```
1. 下から数えた Y 座標です。

この2つの数値があれば、パズルの状態が解けるかどうかを判定できます。4⨉4の盤面の状態は、次のいずれかの条件を満たすと *解くことができます*。

- 空きマスが *奇数* 行（下から数えて1行目または3行目）にあり、転倒数が *偶数* である場合。
- 空きマスが *偶数* 行（下から数えて2行目または4行目）にあり、転倒数が *奇数* である場合。

## この仕組みが成り立つ理由 {#how-does-this-work}

ルールに従った移動では、タイルと空きマスの位置を横方向または縦方向に入れ替えます。

タイルを横方向に移動しても、転倒数は変わらず、空きマスがある行の番号も変わりません。

一方、タイルを縦方向に移動すると、転倒数の偶奇が変わります（奇数から偶数、または偶数から奇数になります）。空きマスがある行の偶奇も変わります。

次の例を見てください。

![タイルの移動](images/15-puzzle/slide.png)

この移動によって、タイルの順序は次の状態から、

`{ ... 0, 11, 2, 13, 6 ... }`

次の状態に変わります。

`{ ... 6, 11, 2, 13, 0 ... }`

新しい状態では、次のように転倒数が3つ増えます。

- 6の転倒が1つ増えます（2が6の後ろになります）。
- 11の転倒が1つ減ります（6が11の前になります）。
- 13の転倒が1つ減ります（6が13の前になります）。

縦方向の移動による転倒数の変化は、±1または±3です。

縦方向の移動による空きマスの行番号の変化は、±1です。

パズルの完成状態では、空きマスは右下隅（*奇数* の1行目）にあり、転倒数は *偶数* の0です。ルールに従った移動では、この2つの値はどちらも変わらないか（横方向の移動）、どちらも偶奇が切り替わります（縦方向の移動）。ルールに従って移動する限り、転倒数と空きマスの行番号の偶奇が *奇数* と *奇数*、または *偶数* と *偶数* になることはありません。

したがって、この2つの数値が両方とも奇数、または両方とも偶数であるパズルの状態は、解くことが不可能です。

解けるかどうかを判定するコードを以下に示します。

```lua
-- Is the given table list of 4x4 tiles solvable?
local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end
```

## ユーザー入力 {#user-input}

残る作業は、パズルを操作できるようにすることだけです。

上で作成した関数を使って、実行時に必要な設定をすべて行う `init()` 関数を作成します。

```lua
function init(self)
    msg.post(".", "acquire_input_focus") -- <1>
    math.randomseed(socket.gettime()) -- <2>
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0}) -- <3>
    while not solvable(self.board) do -- <4>
        self.board = scramble(self.board)
    end
    draw(self.board) -- <5>
    self.done = false -- <6>
    msg.post("#done", "disable") -- <7>
end
```
1. このゲームオブジェクトが入力を受け取るようにエンジンに伝えます。
2. 乱数生成器のシードを設定します。
3. 盤面のランダムな初期状態を作成します。
4. その状態が解けない場合は、もう一度並べ替えます。
5. 盤面を描画します。
6. 勝利した状態を追跡するため、完成フラグを設定します。
7. 完成メッセージのラベルを無効にします。

*/input/game.input_bindings* を開き、新しい *Mouse Trigger* を追加します。アクションの名前を "press" に設定します。

![入力](images/15-puzzle/input.png)

スクリプトに戻り、`on_input()` 関数を作成します。

```lua
-- Deal with user input
function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then -- <1>
        local x = math.ceil(action.x / 128) -- <2>
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0) -- <3>
        if math.abs(x - ex) + math.abs(y - ey) == 1 then -- <4>
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x) -- <5>
            draw(self.board) -- <6>
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then -- <7>
            self.done = true
            msg.post("#done", "enable")
        end
    end
end
```
1. マウスボタンが押され、ゲームがまだ進行中であれば、次の処理を行います。
2. ユーザーがクリックしたマスの x 座標と y 座標を計算します。
3. 空きマス（0）の現在の位置を見つけます。
4. クリックされたマスが空きマスのすぐ上、下、左、または右にあれば、次の処理を行います。
5. クリックされたマスのタイルと空きマスを入れ替えます。
6. 更新した盤面を描画し直します。
7. 盤面の転倒数が0、つまりすべてが正しい順序に並んでおり、空きマスが一番右の列にあれば（転倒数が0になるには、空きマスが最終行にある必要があります）、パズルは解けているので、次の処理を行います。
8. 完成フラグを設定します。
9. 完成メッセージを有効にして表示します。

これで作業は終わりです。パズルゲームが完成しました！

## スクリプト全体 {#the-complete-script}

参考として、スクリプトのコード全体を以下に示します。

```lua
local function inversions(t)
    local inv = 0
    for i=1, #t do
        for j=i+1, #t do
            if t[i] > t[j] and t[j] ~= 0 then
                inv = inv + 1
            end
        end
    end
    return inv
end

local function find(t, tile)
    for i=1, #t do
        if t[i] == tile then
            local y = 5 - math.ceil(i/4)
            local x = i - (math.ceil(i/4) - 1) * 4
            return x,y
        end
    end
end

local function solvable(t)
    local x,y = find(t, 0)
    if y % 2 == 1 and inversions(t) % 2 == 0 then
        return true
    end
    if y % 2 == 0 and inversions(t) % 2 == 1 then
        return true
    end
    return false    
end

local function scramble(t)
    for i=1, #t do
        local tmp = t[i]
        local r = math.random(#t)
        t[i] = t[r]
        t[r] = tmp
    end
    return t
end

local function swap(t, i, j)
    local tmp = t[i]
    t[i] = t[j]
    t[j] = tmp
    return t
end

local function draw(t)
    for i=1, #t do
        local y = 5 - math.ceil(i/4)
        local x = i - (math.ceil(i/4) - 1) * 4
        tilemap.set_tile("#tilemap","layer1",x,y,t[i])
    end
end

function init(self)
    msg.post(".", "acquire_input_focus")
    math.randomseed(socket.gettime())
    self.board = scramble({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0})   
    while not solvable(self.board) do
        self.board = scramble(self.board)
    end
    draw(self.board)
    self.done = false
    msg.post("#done", "disable")
end

function on_input(self, action_id, action)
    if action_id == hash("press") and action.pressed and not self.done then
        local x = math.ceil(action.x / 128)
        local y = math.ceil(action.y / 128)
        local ex, ey = find(self.board, 0)
        if math.abs(x - ex) + math.abs(y - ey) == 1 then
            self.board = swap(self.board, (4-ey)*4+ex, (4-y)*4+x)
            draw(self.board)
        end
        ex, ey = find(self.board, 0)
        if inversions(self.board) == 0 and ex == 4 then
            self.done = true
            msg.post("#done", "enable")
        end
    end
end

function on_reload(self)
    self.done = false
    msg.post("#done", "disable")
end
```

## 追加の練習課題 {#further-exercises}

1. 5⨉5のパズルを作り、次に6⨉5のパズルを作ってください。解けるかどうかの判定が、さまざまな盤面で正しく動作するようにしてください。
2. タイルが滑るアニメーションを追加してください。タイルはタイルマップとは別に移動できないため、その解決方法を考える必要があります。移動するタイルだけを含む別のタイルマップを使う方法はどうでしょうか？
