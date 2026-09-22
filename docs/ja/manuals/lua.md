---
title: Defold での Lua プログラミング
brief: このマニュアルでは、Lua プログラミング全般の基礎と、Defold で Lua を使う際の留意点を簡単に紹介します。
---

# Defold での Lua {#lua-in-defold}

Defold エンジンには、スクリプトを記述するために Lua 言語が組み込まれています。Lua は、強力で高速、かつ組み込みやすい軽量な動的言語です。ビデオゲームのスクリプト言語として広く使われています。Lua のプログラムは、シンプルな手続き型の構文で記述します。動的型付けを採用しており、バイトコードインタープリターで実行されます。また、インクリメンタルなガベージコレクション（garbage collection）による自動メモリ管理を備えています。

このマニュアルでは、Lua プログラミング全般の基礎と、Defold で Lua を使う際の留意点を簡単に紹介します。Python、Perl、Ruby、JavaScript、または同様の動的言語を使った経験があれば、すぐに使い始められるでしょう。プログラミングが初めての場合は、初心者向けの Lua の書籍から始めるとよいかもしれません。選べる書籍は数多くあります。

## Lua のバージョン {#lua-versions}

Defold は、ゲームやその他のパフォーマンスが重要なソフトウェアに適した、高度に最適化された Lua の実装である [LuaJIT](https://luajit.org/) を使用しています。Lua 5.1 に対する完全な上位互換性があり、Lua 標準ライブラリのすべての関数と、Lua/C API のすべての関数をサポートしています。

LuaJIT には、いくつかの[言語拡張](https://luajit.org/extensions.html)と、Lua 5.2 および 5.3 の一部の機能も追加されています。

Defold はすべてのプラットフォームで同じ動作を目指していますが、現在はプラットフォーム間で Lua 言語のバージョンにいくつかの小さな違いがあります。
* iOS では JIT コンパイルが許可されていません。
* Nintendo Switch では JIT コンパイルが許可されていません。
* HTML5 では LuaJIT の代わりに Lua 5.1.4 を使用します。

::: important
サポートされているすべてのプラットフォームでゲームが動作することを保証するため、Lua 5.1 の言語機能のみを使用することを強く推奨します。
:::

### 標準ライブラリと拡張 {#standard-libraries-and-extensions}
Defold には、[Lua 5.1 の標準ライブラリ](http://www.lua.org/manual/5.1/manual.html#5)すべてに加えて、ソケットとビット演算のライブラリが含まれています。

  - base（`assert()`、`error()`、`print()`、`ipairs()`、`require()` など）
  - coroutine
  - package
  - string
  - table
  - math
  - io
  - os
  - debug
  - socket（[LuaSocket](https://github.com/diegonehab/luasocket) 由来）
  - bitop（[BitOp](http://bitop.luajit.org/api.html) 由来）

すべてのライブラリは [API リファレンス](/ref/go)に記載されています。

## Lua の書籍と参考資料 {#lua-books-and-resources}

### オンラインの資料 {#online-resources}
* [Lua プログラミング（Programming in Lua、初版）](http://www.lua.org/pil/contents.html) それ以降の版は書籍として入手できます。
* [Lua 5.1 リファレンスマニュアル](http://www.lua.org/manual/5.1/)
* [15分で学ぶ Lua](http://tylerneylon.com/a/learn-lua/)
* [Awesome Lua のチュートリアルのセクション](https://github.com/LewisJEllis/awesome-lua#tutorials)

### 書籍 {#books}
* [Lua プログラミング（Programming in Lua）](https://www.amazon.com/gp/product/8590379868/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i0) - Programming in Lua は Lua 言語の公式書籍で、Lua を使いたいプログラマーに確かな基礎を提供します。著者は、この言語の主任設計者である Roberto Ierusalimschy です。
* [Lua プログラミングの珠玉の技法（Lua programming gems）](https://www.amazon.com/Programming-Gems-Luiz-Henrique-Figueiredo/dp/8590379841) - この論文集には、Lua で優れたプログラムを書くために蓄積された知識と実践の一部がまとめられています。
* [Lua 5.1 リファレンスマニュアル](https://www.amazon.com/gp/product/8590379833/ref=dbs_a_def_rwt_hsch_vapi_taft_p1_i4) - オンラインでも参照できます（上記参照）。
* [Lua プログラミング入門（Beginning Lua Programming）](https://www.amazon.com/Beginning-Lua-Programming-Kurt-Jung/dp/0470069171)

### 動画 {#videos}
* [1本の動画で学ぶ Lua](https://www.youtube.com/watch?v=iMacxZQMPXs)

## 構文 {#syntax}

プログラムの構文はシンプルで読みやすいものです。文は1行に1つずつ記述し、文の終わりを示す記号は必要ありません。必要に応じて、セミコロン `;` で文を区切ることもできます。コードのブロックはキーワードで区切り、`end` キーワードで終了します。コメントはブロックとして記述することも、行末まで記述することもできます。

```lua
--[[
Here is a block of comments that can run
over several lines in the source file.
--]]

a = 10
b = 20 ; c = 30 -- two statements on one line

if my_variable == 3 then
    call_some_function(true) -- Here is a line comment
else
    call_another_function(false)
end
```

## 変数とデータ型 {#variables-and-data-types}

Lua は動的型付けの言語です。つまり、変数自体には型がなく、値に型があります。 
静的型付けの言語とは異なり、どの変数にも任意の値を自由に代入できます。 

Lua には8つの基本的な型があります。

`nil`
: この型には `nil` という値だけがあります。通常は、値が未代入の変数など、有用な値が存在しないことを表します。

  ```lua
  print(my_var) -- will print 'nil' since 'my_var' is not yet assigned a value
  ```

真偽値（boolean）
: `true` または `false` のいずれかの値を持ちます。条件の値が `false` または `nil` の場合は偽になります。それ以外の値はすべて真になります。

  ```lua
  flag = true
  if flag then
      print("flag is true")
  else
      print("flag is false")
  end

  if my_var then
      print("my_var is not nil nor false!")
  end

  if not my_var then
      print("my_var is either nil or false!")
  end
  ```

数値（number）
: 数値は内部的には、64ビットの _整数_ または64ビットの _浮動小数点数_ として表現されます。Lua は必要に応じてこれらの表現を自動的に変換するため、通常は意識する必要はありません。

  ```lua
  print(10) --> prints '10'
  print(10.0) --> '10'
  print(10.000000000001) --> '10.000000000001'

  a = 5 -- integer
  b = 7/3 -- float
  print(a - b) --> '2.6666666666667'
  ```

文字列（string）
: 文字列は変更できないバイト列で、埋め込まれたゼロ（`\0`）を含む任意の8ビット値を格納できます。Lua は文字列の内容について何も仮定しないため、任意のデータを格納できます。文字列リテラルは単一引用符または二重引用符で囲んで記述します。Lua は実行時に数値と文字列を相互に変換します。文字列は `..` 演算子で連結できます。

  文字列には、次の C 形式のエスケープシーケンスを含めることができます。

  | シーケンス | 文字 |
  | -------- | --------- |
  | `\a`     | ベル       |
  | `\b`     | バックスペース |
  | `\f`     | 改ページ  |
  | `\n`     | 改行    |
  | `\r`     | キャリッジリターン |
  | `\t`     | 水平タブ |
  | `\v`     | 垂直タブ   |
  | `\\`     | バックスラッシュ      |
  | `\"`     | 二重引用符   |
  | `\'`     | 単一引用符   |
  | `\[`     | 左角括弧    |
  | `\]`     | 右角括弧   |
  | `\ddd`   | 数値で指定された文字。`ddd` は最大3桁の _10進数_ の数字列です |

  ```lua
  my_string = "hello"
  another_string = 'world'
  print(my_string .. another_string) --> "helloworld"

  print("10.2" + 1) --> 11.2
  print(my_string + 1) -- error, can't convert "hello"
  print(my_string .. 1) --> "hello1"

  print("one\nstring") --> one
                       --> string

  print("\097bc") --> "abc"

  multi_line_string = [[
  Here is a chunk of text that runs over several lines. This is all
  put into the string and is sometimes very handy.
  ]]
  ```

関数（function）
: Lua の関数は第一級の値です。つまり、関数にパラメーターとして渡したり、値として返したりできます。関数を代入した変数には、その関数への参照が格納されます。変数に無名関数を代入できますが、Lua には便利な構文糖衣（`function name(param1, param2) ... end`）も用意されています。

  ```lua
  -- Assign 'my_plus' to function
  my_plus = function(p, q)
      return p + q
  end

  print(my_plus(4, 5)) --> 9

  -- Convenient syntax to assign function to variable 'my_mult'
  function my_mult(p, q)
      return p * q
  end

  print(my_mult(4, 5)) --> 20

  -- Takes a function as parameter 'func'
  function operate(func, p, q)
      return func(p, q) -- Calls the provided function with parameters 'p' and 'q'
  end

  print(operate(my_plus, 4, 5)) --> 9
  print(operate(my_mult, 4, 5)) --> 20

  -- Create an adder function and return it
  function create_adder(n)
      return function(a)
          return a + n
      end
  end

  adder = create_adder(2)
  print(adder(3)) --> 5
  print(adder(10)) --> 12
  ```

テーブル（table）
: テーブルは、Lua でデータを構造化する唯一の型です。テーブルは連想配列の _オブジェクト_ で、リスト、配列、シーケンス、シンボルテーブル、集合、レコード、グラフ、木などを表すために使用します。テーブルは常に無名であり、テーブルを代入した変数にはテーブルそのものではなく、その参照が格納されます。テーブルをシーケンスとして初期化する場合、最初のインデックスは `1` であり、`0` ではありません。

  ```lua
  -- Initialize a table as a sequence
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}
  print(weekdays[1]) --> "Sunday"
  print(weekdays[5]) --> "Thursday"

  -- Initialize a table as a record with sequence values
  moons = { Earth = { "Moon" },
            Uranus = { "Puck", "Miranda", "Ariel", "Umbriel", "Titania", "Oberon" } }
  print(moons.Uranus[3]) --> "Ariel"

  -- Build a table from an empty constructor {}
  a = 1
  t = {}
  t[1] = "first"
  t[a + 1] = "second"
  t.x = 1 -- same as t["x"] = 1

  -- Iterate over the table key, value pairs
  for key, value in pairs(t) do
      print(key, value)
  end
  --> 1   first
  --> 2   second
  --> x   1

  u = t -- u now refers to the same table as t
  u[1] = "changed"

  for key, value in pairs(t) do -- still iterating over t!
      print(key, value)
  end
  --> 1   changed
  --> 2   second
  --> x   1
  ```

ユーザーデータ（userdata）
: `userdata` は、Lua の変数に任意の C のデータを格納できるように用意されています。Defold は Lua の `userdata` オブジェクトを使って、ハッシュ値（hash）、URL オブジェクト（url）、数学オブジェクト（vector3、vector4、matrix4、quaternion）、ゲームオブジェクト（game object）、GUI ノード（node）、レンダー述語（predicate）、レンダーターゲット（render_target）、レンダー定数バッファー（constant_buffer）を格納します。

スレッド（thread）
: スレッドは独立した実行の流れを表し、コルーチン（coroutine）の実装に使われます。詳しくは後述します。

## 演算子 {#operators}

算術演算子
: 数学の演算子 `+`、`-`、`*`、`/`、単項 `-`（符号反転）、べき乗 `^` です。

  ```lua
  a = -1
  print(a * 2 + 3 / 4^5) --> -1.9970703125
  ```

  Lua は実行時に数値と文字列を自動的に相互変換します。文字列に数値演算を適用すると、その文字列を数値に変換しようとします。

  ```lua
  print("10" + 1) --> 11
  ```

関係演算子と比較演算子
: `<`（より小さい）、`>`（より大きい）、`<=`（以下）、`>=`（以上）、`==`（等しい）、`~=`（等しくない）です。これらの演算子は常に `true` または `false` を返します。型が異なる値は異なるものとみなされます。型が同じ場合は、その値に基づいて比較します。Lua はテーブル、`userdata`、関数を参照で比較します。これらの2つの値は、同じオブジェクトを参照している場合にのみ等しいとみなされます。

  ```lua
  a = 5
  b = 6

  if a <= b then
      print("a is less than or equal to b")
  end

  print("A" < "a") --> true
  print("aa" < "ab") --> true
  print(10 == "10") --> false
  print(tostring(10) == "10") --> true
  ```

論理演算子
: `and`、`or`、`not` です。`and` は第1引数が `false` の場合はその引数を返し、それ以外の場合は第2引数を返します。`or` は第1引数が `false` でない場合はその引数を返し、それ以外の場合は第2引数を返します。

  ```lua
  print(true or false) --> true
  print(true and false) --> false
  print(not false) --> true

  if a == 5 and b == 6 then
      print("a is 5 and b is 6")
  end
  ```

連結
: 文字列は `..` 演算子で連結できます。連結する際、数値は文字列に変換されます。

  ```lua
  print("donkey" .. "kong") --> "donkeykong"
  print(1 .. 2) --> "12"
  ```

長さ
: 単項の長さ演算子 `#` です。文字列の長さは、そのバイト数です。テーブルの長さは、そのシーケンスの長さです。これは、`1` から昇順に番号が付けられ、値が `nil` でないインデックスの数を指します。注意：シーケンスの途中に `nil` 値の「穴」がある場合、長さは `nil` 値の直前にあるいずれかのインデックスになることがあります。

  ```lua
  s = "donkey"
  print(#s) --> 6

  t = { "a", "b", "c", "d" }
  print(#t) --> 4

  u = { a = 1, b = 2, c = 3 }
  print(#u) --> 0

  v = { "a", "b", nil }
  print(#v) --> 2
  ```

## 制御フロー {#flow-control}

Lua には一般的な制御フローの構文が用意されています。

if---then---else
: 条件を評価し、真であれば `then` 部分を実行し、それ以外の場合は省略可能な `else` 部分を実行します。`if` 文を入れ子にする代わりに、`elseif` を使えます。これは Lua にはない switch 文の代わりになります。

  ```lua
  a = 5
  b = 4

  if a < b then
      print("a is smaller than b")
  end

  if a == '1' then
      print("a is 1")
  elseif a == '2' then
      print("a is 2")
  elseif a == '3' then
      print("a is 3")
  else
      print("I have no idea what a is...")
  end
  ```

while
: 条件を評価し、真である間はブロックを実行します。

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 1
  while weekdays[i] do
      print(weekdays[i])
      i = i + 1
  end
  ```

repeat---until
: 条件が真になるまでブロックを繰り返します。条件は本体の実行後に評価されるため、少なくとも1回は実行されます。

  ```lua
  weekdays = {"Sunday", "Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday"}

  -- Print each weekday
  i = 0
  repeat
      i = i + 1
      print(weekdays[i])
  until weekdays[i] == "Saturday"
  ```

for
: Lua には数値形式と汎用形式の2種類の `for` ループがあります。数値形式の `for` は2つまたは3つの数値を受け取ります。一方、汎用形式の `for` は、_イテレーター_ 関数が返すすべての値に対して反復処理を行います。

  ```lua
  -- Print the numbers 1 to 10
  for i = 1, 10 do
      print(i)
  end

  -- Print the numbers 1 to 10 and increment with 2 each time
  for i = 1, 10, 2 do
      print(i)
  end

  -- Print the numbers 10 to 1
  for i=10, 1, -1 do
      print(i)
  end

  t = { "a", "b", "c", "d" }
  -- Iterate over the sequence and print the values
  for i, v in ipairs(t) do
      print(v)
  end
  ```

break と return
: `break` 文を使うと、`for`、`while`、`repeat` ループの内側のブロックから抜けられます。`return` は、関数から値を返す場合や、関数の実行を終了して呼び出し元に戻る場合に使います。`break` と `return` は、ブロックの最後の文としてのみ記述できます。

  ```lua
  a = 1
  while true do
      a = a + 1
      if a >= 100 then
          break
      end
  end

  function my_add(a, b)
      return a + b
  end

  print(my_add(10, 12)) --> 22
  ```

## ローカル変数、グローバル変数、レキシカルスコープ {#locals-globals-and-lexical-scoping}

宣言した変数は既定ですべてグローバル変数となり、Lua ランタイムのコンテキスト全体で利用できます。変数を明示的に `local` として宣言すると、その変数は現在のスコープ（scope）内にのみ存在します。

各 Lua ソースファイルは、それぞれ独立したスコープを定義します。ファイルの最上位で `local` 宣言を行うと、その変数は Lua スクリプトファイル内のローカル変数になります。各関数はさらに入れ子のスコープを作成し、各制御構造のブロックも追加のスコープを作成します。`do` と `end` キーワードを使って、明示的にスコープを作成することもできます。Lua はレキシカルスコープを採用しているため、あるスコープからは、それを囲むスコープの _ローカル_ 変数に自由にアクセスできます。ローカル変数は使用する前に宣言する必要があることに注意してください。

```lua
function my_func(a, b)
    -- 'a' and 'b' are local to this function and available through its scope

    do
        local x = 1
    end

    print(x) --> nil. 'x' is not available outside the do-end scope
    print(foo) --> nil. 'foo' is declared after 'my_func'
    print(foo_global) --> "value 2"
end

local foo = "value 1"
foo_global = "value 2"

print(foo) --> "value 1". 'foo' is available in the topmost scope after declaration.
```

スクリプトファイル内で関数を `local` として宣言する場合は、コードの順序に注意する必要があります。一般的に、関数をローカルに宣言することをお勧めします。互いに呼び出し合う関数がある場合は、前方宣言を使えます。

```lua
local func2 -- Forward declare 'func2'

local function func1(a)
    print("func1")
    func2(a)
end

function func2(a) -- or func2 = function(a)
    print("func2")
    if a < 10 then
        func1(a + 1)
    end
end

function init(self)
    func1(1)
end
```

別の関数の内部に関数を記述した場合、その関数からも外側の関数のローカル変数に自由にアクセスできます。これは非常に強力な構文です。

```lua
function create_counter(x)
    -- 'x' is a local variable in 'create_counter'
    return function()
        x = x + 1
        return x
    end
end

count1 = create_counter(10)
count2 = create_counter(20)
print(count1()) --> 11
print(count2()) --> 21
print(count1()) --> 12
```

## 変数のシャドーイング {#variable-shadowing}

ブロック内で宣言したローカル変数は、それを囲むブロックにある同名の変数を隠します。

```lua
my_global = "global"
print(my_global) -->"global"

local v = "local"
print(v) --> "local"

local function test(v)
    print(v)
end

function init(self)
    v = "apple"
    print(v) --> "apple"
    test("banana") --> "banana"
end
```

## コルーチン {#coroutines}

関数は最初から最後まで実行され、途中で停止する方法はありません。コルーチンでは途中で停止でき、場合によっては非常に便利です。たとえば、ゲームオブジェクトを y 位置 `0` から、フレーム1からフレーム5までの各フレームで指定した y 位置に移動させる、細かく指定したフレーム単位のアニメーションを作りたいとします。`update()` 関数（後述）内のカウンターと、位置のリストを使って実現できます。しかし、コルーチンを使うと、拡張しやすく扱いやすい、すっきりとした実装になります。状態はすべてコルーチン自体の内部に保持されます。

コルーチンが処理を中断して制御を譲ると、呼び出し元に制御が戻ります。その際、実行位置を記憶しているため、後でその位置から処理を再開できます。

```lua
-- This is our coroutine
local function sequence(self)
    coroutine.yield(120)
    coroutine.yield(320)
    coroutine.yield(510)
    coroutine.yield(240)
    return 440 -- return the final value
end

function init(self)
    self.co = coroutine.create(sequence) -- Create the coroutine. 'self.co' is a thread object
    go.set_position(vmath.vector3(100, 0, 0)) -- Set initial position
end

function update(self, dt)
    local status, y_pos = coroutine.resume(self.co, self) -- Continue execution of coroutine.
    if status then
        -- If the coroutine is still not terminated/dead, use its yielded return value as a new position
        go.set_position(vmath.vector3(100, y_pos, 0))
    end
end
```


## Defold の Lua コンテキスト {#lua-contexts-in-defold}

宣言した変数は既定ですべてグローバル変数となり、Lua ランタイムのコンテキスト全体で利用できます。Defold では、*game.project* の *shared_state* 設定でこのコンテキストを制御します。このオプションを設定すると、すべてのスクリプト、GUI スクリプト、レンダースクリプトが同じ Lua コンテキストで評価され、グローバル変数にどこからでもアクセスできます。このオプションを設定しない場合、エンジンはスクリプト、GUI スクリプト、レンダースクリプトを別々のコンテキストで実行します。

![コンテキスト](images/lua/lua_contexts.png)

Defold では、ゲームオブジェクトの複数の別々のコンポーネント（component）で、同じスクリプトファイルを使用できます。ローカルに宣言した変数は、同じスクリプトファイルを実行するコンポーネント間で共有されます。

```lua
-- 'my_global_value' will be available from all scripts, gui_scripts, render script and modules (Lua files)
my_global_value = "global scope"

-- this value will be shared through all component instances that use this particular script file
local script_value = "script scope"

function init(self, dt)
    -- This value will be available on this script component instance
    self.foo = "self scope"

    -- this value will be available inside init() and after it's declaration
    local local_foo = "local scope"
    print(local_foo)
end

function update(self, dt)
    print(self.foo)
    print(my_global_value)
    print(script_value)
    print(local_foo) -- will print nil, since local_foo is only visible in init()
end
```

## パフォーマンスに関する留意点 {#performance-considerations}

滑らかな 60 FPS で動作することを目指す高性能なゲームでは、パフォーマンスに関する小さなミスがプレイ体験に大きく影響することがあります。考慮すべきシンプルで一般的な事項もあれば、一見問題には思えない事項もあります。

まずはシンプルなことから始めましょう。一般的には、不必要なループを含まない、分かりやすいコードを書くことをお勧めします。要素のリストを反復処理する必要があることもありますが、そのリストが大きい場合は注意してください。次の例は、かなり性能のよいノートパソコンでも実行に1ミリ秒強かかります。60 FPS では1フレームの時間はわずか16ミリ秒で、エンジン、レンダースクリプト、物理シミュレーションなどがその一部を消費するため、この時間の差が結果を大きく左右することがあります。

```lua
local t = socket.gettime()
local table = {}
for i=1,2000 do
    table[i] = vmath.vector3(i, i, i)
end
print((socket.gettime() - t) * 1000)

-- DEBUG:SCRIPT: 0.40388
```

パフォーマンスが疑わしいコードを計測するには、`socket.gettime()` が返す値（システムのエポックからの秒数）を使います。

## メモリとガベージコレクション {#memory-and-garbage-collection}

Lua のガベージコレクションは、既定ではバックグラウンドで自動的に実行され、Lua ランタイムが割り当てたメモリを回収します。大量の不要なオブジェクトを回収すると時間がかかる場合があるため、ガベージコレクションの対象となるオブジェクトの数を抑えることをお勧めします。

* ローカル変数自体にはコストがかからず、不要なオブジェクトも発生しません（例：`local v = 42`）。
* _これまで存在しなかった新しい_ 文字列ごとに、新しいオブジェクトが作成されます。`local s = "some_string"` と記述すると、新しいオブジェクトが作成され、それを参照するように `s` が代入されます。ローカル変数 `s` 自体は不要なオブジェクトを発生させませんが、文字列オブジェクトは回収対象となります。同じ文字列を複数回使用しても、追加のメモリコストはかかりません。
* テーブルコンストラクターを実行するたびに（`{ ... }`）、新しいテーブルが作成されます。
* _関数定義文_ を実行すると、クロージャーオブジェクトが作成されます（定義済みの関数を呼び出すことではなく、`function () ... end` という文を実行することです）。
* 可変長引数を持つ関数（`function(v, ...) end`）は、関数が _呼び出される_ たびに、省略記号に対応するテーブルを作成します（バージョン 5.2 より前の Lua、または LuaJIT を使用しない場合）。
* `dofile()` と `dostring()`
* ユーザーデータオブジェクト

多くの場合、新しいオブジェクトの作成を避け、すでにあるオブジェクトを再利用できます。たとえば、各 `update()` の末尾には、よく次のような処理を記述します。

```lua
-- Reset velocity
self.velocity = vmath.vector3()
```

`vmath.vector3()` を呼び出すたびに新しいオブジェクトが作成されることは、忘れがちです。1つの `vector3` が使うメモリ量を調べてみましょう。

```lua
print(collectgarbage("count") * 1024)       -- 88634
local v = vmath.vector3()
print(collectgarbage("count") * 1024)       -- 88704. 70 bytes in total has been allocated
```

`collectgarbage()` の呼び出しの間に70バイト増えていますが、これには `vector3` オブジェクト以外への割り当ても含まれています。`collectgarbage()` の結果を出力するたびに文字列が作成され、それだけで22バイトの不要なオブジェクトが追加されます。

```lua
print(collectgarbage("count") * 1024)       -- 88611
print(collectgarbage("count") * 1024)       -- 88633. 22 bytes allocated
```

したがって、`vector3` のメモリ量は 70-22=48 バイトです。これは多くはありませんが、60 FPS のゲームで毎フレーム _1つ_ 作成すると、毎秒 2.8 kB の不要なオブジェクトが発生することになります。360個のスクリプトコンポーネントがそれぞれ毎フレーム1つの `vector3` を作成すると、毎秒 1 MB の不要なオブジェクトが発生します。合計量は急速に増えていきます。Lua ランタイムがガベージコレクションを行うと、貴重な時間を何ミリ秒も消費することがあります。特にモバイルプラットフォームではその影響が大きくなります。

割り当てを避ける方法の1つは、`vector3` を作成し、その後も同じオブジェクトを使い続けることです。たとえば、`vector3` をリセットするには、次のように記述できます。

```lua
-- Instead of doing self.velocity = vmath.vector3() which creates a new object
-- we zero an existing velocity vector object's components
self.velocity.x = 0
self.velocity.y = 0
self.velocity.z = 0
```

既定のガベージコレクションの方式は、処理時間が重要な一部のアプリケーションには最適でない場合があります。ゲームやアプリで動きが途切れる場合は、Lua の [`collectgarbage()`](/ref/base/#collectgarbage) 関数で、Lua による回収の仕方を調整するとよいかもしれません。たとえば、`step` に小さい値を指定すると、毎フレーム短い時間だけガベージコレクターを実行できます。ゲームやアプリがどれくらいメモリを消費しているかを把握するには、次のようにして現在の回収対象のバイト数を出力できます。

```lua
print(collectgarbage("count") * 1024)
```

## ベストプラクティス {#best-practices}

実装を設計する際によく検討するのが、共通の振る舞いを実装するコードをどのように構成するかという点です。いくつかの方法があります。

モジュール内の振る舞い
: 振る舞いをモジュール（module）にカプセル化すると、異なるゲームオブジェクトのスクリプトコンポーネント間（および GUI スクリプト間）でコードを簡単に共有できます。モジュールの関数を記述する際は、一般的に、厳密に関数型のコードを書くのが最善です。状態の保存や副作用が必要な場合もありますし、その方が設計をすっきりさせられる場合もあります。モジュール内に内部状態を保存する必要がある場合は、コンポーネントが Lua コンテキストを共有することに注意してください。詳しくは[モジュールのドキュメント](/manuals/modules)を参照してください。

  ![モジュール](images/lua/lua_module.png)

  また、モジュールの関数に `self` を渡すことで、モジュールのコードからゲームオブジェクトの内部を直接変更できますが、非常に強い結合が生じるため、この方法は避けることを強くお勧めします。

振る舞いをカプセル化したヘルパーゲームオブジェクト
: スクリプトコードを Lua モジュールに格納できるのと同様に、スクリプトコンポーネントを持つゲームオブジェクトに格納することもできます。ゲームオブジェクトに格納した場合は、メッセージによる通信であるメッセージパッシング（message passing）だけを通じて通信できる点が異なります。

  ![ヘルパー](images/lua/lua_helper.png)

コレクション内でゲームオブジェクトと振る舞いを補助するオブジェクトをグループ化する
: この設計では、あらかじめ決めた名前、または対象のゲームオブジェクトを指す `go.property()` の URL を使って、そのゲームオブジェクトに自動的に作用する、振る舞いを担うゲームオブジェクトを作成できます。名前を使う場合、ユーザーは対象のゲームオブジェクトの名前を一致するように変更する必要があります。

  ![コレクション](images/lua/lua_collection.png)

  この構成の利点は、対象のオブジェクトが含まれるコレクション（collection）に、振る舞いを担うゲームオブジェクトを配置するだけで使えることです。追加のコードは一切必要ありません。

  大量のゲームオブジェクトを管理する必要がある場合は、この設計は望ましくありません。振る舞いを担うオブジェクトがインスタンスごとに複製され、それぞれのオブジェクトがメモリを消費するためです。
