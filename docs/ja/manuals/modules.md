---
title: Defold の Lua モジュール
brief: Lua モジュールを使うと、プロジェクトを構造化し、再利用できるライブラリコードを作成できます。このマニュアルでは、Defold でその方法を説明します。
---

# Lua モジュール {#lua-modules}

Lua モジュール（Lua module）を使うと、プロジェクトを構造化し、再利用できるライブラリコードを作成できます。一般に、プロジェクト内の重複は避けることをお勧めします。Defold では、Lua のモジュール機能を使って、スクリプトファイルを別のスクリプトファイルに読み込めます。これにより、機能（およびデータ）を外部のスクリプトファイルにカプセル化し、ゲームオブジェクト（game object）のスクリプトファイルや GUI スクリプトファイルで再利用できます。

## Lua ファイルの読み込み {#requiring-lua-files}

ゲームプロジェクト内にある、拡張子が `.lua` のファイルに保存された Lua コードは、`require` を使ってスクリプトファイルや GUI スクリプトファイルに読み込めます。新しい Lua モジュールファイルを作成するには、*Assets* ビューで作成先のフォルダーを右クリックし、<kbd>New... ▸ Lua Module</kbd> を選択します。ファイルに一意の名前を付け、<kbd>Ok</kbd> を押します。

![新しいファイル](images/modules/new_name.png)

ファイル「`main/anim.lua`」に次のコードを追加したとします。

```lua
function direction_animation(direction, char)
    local d = ""
    if direction.x > 0 then
        d = "right"
    elseif direction.x < 0 then
        d = "left"
    elseif direction.y > 0 then
        d = "up"
    elseif direction.y < 0 then
        d = "down"
    end
    return hash(char .. "-" .. d)
end
```

すると、どのスクリプトからでも `require` でこのファイルを読み込み、関数を使えます。

```lua
require "main.anim"

function update(self, dt)
    -- update position, set direction etc
    ...

    -- set animation
    local anim = direction_animation(self.dir, "player")
    if anim ~= self.current_anim then
        sprite.play_flipbook("#sprite", anim)
        self.current_anim = anim
    end
end
```

`require` 関数は、指定されたモジュールを読み込みます。まず `package.loaded` テーブルを調べ、そのモジュールがすでに読み込まれているかを確認します。読み込み済みであれば、`require` は `package.loaded[module_name]` に格納された値を返します。そうでなければ、ローダーを通じてファイルを読み込み、評価します。

`require` に渡すファイル名の文字列には、少し特殊な構文を使います。Lua は、ファイル名の文字列にある `.` をパスの区切り文字に置き換えます。macOS と Linux では `/`、Windows では `\\` です。

上の例のように、グローバルスコープを使って状態を保存したり、関数を定義したりすることは、通常は避けてください。名前が衝突したり、モジュールの状態が外部に公開されたり、モジュールを利用するコード同士の結合が生じたりするおそれがあります。

## モジュール {#modules}

Lua は、データと関数をカプセル化するために _モジュール_ を使います。Lua モジュールは、関数とデータを格納する通常の Lua テーブルです。グローバルスコープを汚染しないよう、テーブルをローカルとして宣言します。

```lua
local M = {}

-- private
local message = "Hello world!"

function M.hello()
    print(message)
end

return M
```

これでモジュールを使えます。ここでも、ローカル変数に代入することをお勧めします。

```lua
local m = require "mymodule"
m.hello() --> "Hello world!"
```

## モジュールのホットリロード {#hot-reloading-modules}

次のような単純なモジュールを考えます。

```lua
-- module.lua
local M = {} -- creates a new table in the local scope
M.value = 4711
return M
```

このモジュールを利用するコードは次のとおりです。 

```lua
local m = require "module"
print(m.value) --> "4711" (even if "module.lua" is changed and hot reloaded)
```

モジュールファイルをホットリロード（hot reload）するとコードが再実行されますが、`m.value` は変わりません。なぜでしょうか？

まず、`module.lua` のテーブルはローカルスコープに作成され、そのテーブルへの _参照_ が呼び出し元に返されます。`module.lua` を再読み込みすると、モジュールのコードが再び評価されます。しかし、`m` が参照するテーブルが更新されるのではなく、ローカルスコープに新しいテーブルが作成されます。

次に、Lua は `require` で読み込んだファイルをキャッシュします。ファイルを初めて読み込むと、そのファイルは [`package.loaded`](/ref/package/#package.loaded) テーブルに格納され、以降の `require` 呼び出しでより速く読み込めるようになります。ファイルのエントリーを `nil` に設定すると、ディスクから強制的に再読み込みできます。`package.loaded["my_module"] = nil` とします。

モジュールを正しくホットリロードするには、モジュールを再読み込みし、キャッシュをリセットしてから、そのモジュールを使うすべてのファイルを再読み込みする必要があります。これは効率的とはいえません。

そこで、_開発中_ に使う回避策を検討できます。ファイルが評価されるたびに新しいテーブルを作成する代わりに、モジュールのテーブルをグローバルスコープに置き、`M` からそのグローバルテーブルを参照します。こうすると、モジュールの再読み込みによってグローバルテーブルの内容が変更されます。

```lua
--- module.lua

-- Replace with local M = {} when done
uniquevariable12345 = uniquevariable12345 or {}
local M = uniquevariable12345

M.value = 4711
return M
```

## モジュールと状態 {#modules-and-state}

状態を持つモジュールは、そのモジュールを利用するすべてのコードで共有する内部状態を保持します。シングルトンに相当するものと考えられます。

```lua
local M = {}

-- all users of the module will share this table
local state = {}

function M.do_something(foobar)
    table.insert(state, foobar)
end

return M
```

一方、状態を持たないモジュールは、内部状態を一切保持しません。代わりに、モジュールを利用するコードのローカルスコープにある別のテーブルに、状態を外部化する仕組みを提供します。これを実装する方法をいくつか紹介します。

状態テーブルを使う
: 最も簡単と思われる方法は、状態だけを格納した新しいテーブルを返すコンストラクター関数を使うことです。状態テーブルを操作するすべての関数で、最初のパラメーターとして状態をモジュールに明示的に渡します。

  ```lua
  local M = {}
  
  function M.alter_state(the_state, v)
      the_state.value = the_state.value + v
  end
  
  function M.get_state(the_state)
      return the_state.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return state
  end
  
  return M
  ```
  
  モジュールは次のように使います。
  
  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  m.alter_state(my_state, 1)
  print(m.get_state(my_state)) --> 43
  ```

メタテーブルを使う
: もう1つの方法は、呼び出されるたびに、状態とモジュールの公開関数を持つ新しいテーブルを返すコンストラクター関数を使うことです。

  ```lua
  local M = {}
  
  function M:alter_state(v)
      -- self is added as first argument when using : notation
      self.value = self.value + v
  end
  
  function M:get_state()
      return self.value
  end
  
  function M.new(v)
      local state = {
          value = v
      }
      return setmetatable(state, { __index = M })
  end
  
  return M
  ```

  モジュールは次のように使います。

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state:alter_state(1) -- "my_state" is added as first argument when using : notation
  print(my_state:get_state()) --> 43
  ```

クロージャを使う
:  3つ目の方法は、すべての状態と関数を含むクロージャを返すことです。メタテーブルを使う場合のように、インスタンスを引数として渡す必要はありません（明示的に渡す必要も、コロン演算子で暗黙的に渡す必要もありません）。また、この方法では関数呼び出しが `__index` メタメソッドを経由する必要がないため、メタテーブルを使う場合よりも多少速くなります。ただし、各クロージャがメソッドのコピーをそれぞれ保持するため、メモリ消費量は増えます。

  ```lua
  local M = {}
  
  function M.new(v)
      local state = {
          value = v
      }
  
      state.alter_state = function(v)
          state.value = state.value + v
      end
  
      state.get_state = function()
          return state.value
      end
  
      return state
  end
  
  return M
  ```

  モジュールは次のように使います。

  ```lua
  local m = require "main.mymodule"
  local my_state = m.new(42)
  my_state.alter_state(1)
  print(my_state.get_state()) 
  ```
