---
title: エディタースクリプト
brief: このマニュアルでは、Lua を使ってエディターを拡張する方法を説明します。
---

# エディタースクリプト {#editor-scripts}

特別な拡張子 `.editor_script` を持つ Lua ファイルを使うと、独自のメニュー項目やエディターのライフサイクルフック（lifecycle hook）を作成できます。このエディタースクリプト（editor script）の仕組みを使ってエディターを調整し、開発ワークフローを改善できます。

## エディタースクリプトのランタイム {#editor-script-runtime}

エディタースクリプトは、エディター内で Java VM によってエミュレートされた Lua VM 上で実行されます。すべてのスクリプトが1つの環境を共有するため、互いにやり取りできます。`.script` ファイルと同じように Lua モジュールを `require` できますが、エディター内で動作する Lua のバージョンは異なるため、共有するコードに互換性があることを確認してください。エディターでは Lua バージョン 5.2.x、具体的には [luaj](https://github.com/luaj/luaj) ランタイムを使用しています。これは現在、JVM 上で Lua を実行するための唯一の実用的な方法です。さらに、次の制限があります。
- `debug` パッケージはありません。
- `os.execute` はありませんが、類似の `editor.execute()` が用意されています。
- `os.tmpname` と `io.tmpfile` はありません。現在、エディタースクリプトがアクセスできるファイルはプロジェクトディレクトリ内のものだけです。
- `os.rename` は現在ありませんが、Defold では追加したいと考えています。
- `os.exit` と `os.setlocale` はありません。
- エディターがスクリプトからの即時の応答を必要とするコンテキストでは、一部の実行に時間がかかる関数は使用できません。詳しくは[実行モード](#execution-modes)を参照してください。

エディタースクリプトで定義されたエディター拡張はすべて、プロジェクトを開くときに読み込まれます。依存するライブラリに新しいエディタースクリプトが含まれている可能性があるため、ライブラリを取得すると拡張が再読み込みされます。この再読み込みでは、自分のエディタースクリプトへの変更は反映されません。編集中である可能性があるためです。自分のスクリプトも再読み込みするには、**Project → Reload Editor Scripts** コマンドを実行してください。

## `.editor_script` の構成 {#anatomy-of-editor_script}

各エディタースクリプトは、次のようにモジュールを返すようにします。
```lua
local M = {}

function M.get_commands()
  -- TODO - define editor commands
end

function M.get_language_servers()
  -- TODO - define language servers
end

function M.get_prefs_schema()
  -- TODO - define preferences
end

return M
```
エディターは、プロジェクトとライブラリで定義されたすべてのエディタースクリプトを収集して1つの Lua VM に読み込み、必要に応じて呼び出します。詳しくは、[コマンド](#commands)と[ライフサイクルフック](#lifecycle-hooks)の節を参照してください。

## エディター API {#editor-api}

次の API を定義する `editor` パッケージを使って、エディターとやり取りできます。
- `editor.platform` — 文字列です。Windows では `"x86_64-win32"`、macOS では `"x86_64-macos"`、Linux では `"x86_64-linux"` です。
- `editor.version` — Defold のバージョン名を表す文字列です。例: `"1.4.8"`
- `editor.engine_sha1` — Defold エンジンの SHA1 を表す文字列です。
- `editor.editor_sha1` — Defold エディターの SHA1 を表す文字列です。
- `editor.get(node_id, property)` — エディター内のノード（node）の値を取得します。エディターのノードは、スクリプトやコレクション（collection）のファイル、コレクション内のゲームオブジェクト（game object）、リソース（resource）として読み込まれた JSON ファイルなど、さまざまな実体を表します。`node_id` は、エディターからエディタースクリプトに渡されるユーザーデータです。ノード ID の代わりに、たとえば `"/main/game.script"` のようなリソースパスを渡すこともできます。`property` は文字列です。現在、次のプロパティ（property）がサポートされています。
  - `"path"` — ファイルやディレクトリとして存在する実体である*リソース*について、プロジェクトフォルダーからのファイルパスを表します。戻り値の例: `"/main/game.script"`
  - `"children"` — ディレクトリリソースの子リソースのパスのリストです。
  - `"parent"` — 親を持つ Outline ノードの親エディターノードです。
  - `"text"` — スクリプトファイルや JSON など、テキストとして編集できるリソースのテキスト内容です。戻り値の例: `"function init(self)\nend"`。ファイルは保存せずに編集でき、その編集内容は `"text"` プロパティにアクセスした場合にのみ取得できるため、`io.open()` でファイルを読み込むこととは異なる点に注意してください。
  - アトラス（atlas）: `images`（アトラス内の画像のエディターノードのリスト）と `animations`（アニメーションノードのリスト）です。
  - アトラスのアニメーション: `images`（アトラスの `images` と同じ）です。
  - タイルマップ（tilemap）: `layers`（タイルマップ内のレイヤーのエディターノードのリスト）です。
  - タイルマップのレイヤー: `tiles`（境界のない 2D タイルグリッド）です。詳しくは `tilemap.tiles.*` を参照してください。
  - パーティクルエフェクト（particle effect）: エミッター（emitter）のエディターノードのリスト `emitters` と、モディファイアー（modifier）のエディターノードのリスト `modifiers` です。
  - パーティクルエフェクトのエミッター: `modifiers`（モディファイアーのエディターノードのリスト）です。
  - コリジョンオブジェクト（collision object）: `shapes`（コリジョン形状のエディターノードのリスト）です。
  - GUI ファイル: `layers`、`fonts`、`materials`、`textures`、`particlefxs`、`nodes`、`layouts` などのノードリストです。
  - Outline ビューで何かを選択したときに Properties ビューに表示される一部のプロパティです。次の型のアウトラインプロパティがサポートされています。
    - `strings`
    - `booleans`
    - `numbers`
    - `vec2`/`vec3`/`vec4`
    - `resources`
    - `curves`
    これらのプロパティには、読み取り専用のものや、コンテキストによって使用できないものがあります。そのため、読み取る前に `editor.can_get` を使い、エディターに設定させる前に `editor.can_set` を使ってください。Properties ビューでプロパティ名にマウスポインターを合わせると、エディタースクリプトでのプロパティ名を示すツールチップが表示されます。リソースプロパティに `""` という値を指定すると、`nil` に設定できます。
- `editor.properties(node_id)` — ノードから読み取れるプロパティ名を、コンテキストに応じたソート済みのリストで返します。例: `pprint(editor.properties("/game.project"))`。リストにあるプロパティについて、変更、リセット、内容の追加、並べ替えもできるかを確認するには、`editor.can_*` 関数を使います。
- `editor.can_get(node_id, property)` — `editor.get()` がエラーを発生させずに、このプロパティを取得できるかを確認します。
- `editor.can_set(node_id, property)` — このプロパティに対する `editor.tx.set()` トランザクション（transaction）のステップがエラーを発生させないかを確認します。
- `editor.create_directory(resource_path)` — ディレクトリが存在しない場合に作成し、存在しない親ディレクトリもすべて作成します。
- `editor.create_resources(resources)` — テンプレートから、または独自の内容を指定して、1つ以上のリソースを作成します。
- `editor.delete_directory(resource_path)` — ディレクトリが存在する場合に削除し、その中の子ディレクトリとファイルもすべて削除します。
- `editor.execute(cmd, [...args], [options])` — シェルコマンドを実行します。必要に応じて、その出力を取得できます。
- `editor.save()` — 保存していないすべての変更をディスクに保存します。
- `editor.transact(txs)` — `editor.tx.*` 関数で作成した1つ以上のトランザクションステップを使って、メモリ内のエディターの状態を変更します。
- `editor.ui.*` — UI に関連する各種関数です。[UI マニュアル](/manuals/editor-scripts-ui)を参照してください。
- `editor.prefs.*` — エディターの環境設定（preferences）とやり取りする関数です。[環境設定](#preferences)を参照してください。

エディター API リファレンスの全体は[こちら](/ref/stable/editor/)で確認できます。

## コマンド {#commands}

エディタースクリプトのモジュールで `get_commands()` を定義すると、拡張の再読み込み時に呼び出されます。返されたコマンドは、`locations` に応じて、メニューバーのメニューや、Assets、Outline、Scene、Code のコンテキストメニューに表示できます。例:

```lua
local M = {}

function M.get_commands()
  return {
    {
      label = "Remove Comments",
      locations = {"Edit", "Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        local path = editor.get(opts.selection, "path")
        return ends_with(path, ".lua") or ends_with(path, ".script")
      end,
      run = function(opts)
        local text = editor.get(opts.selection, "text")
        editor.transact({
          editor.tx.set(opts.selection, "text", strip_comments(text))
        })
      end
    },
    {
      label = "Minify JSON",
      locations = {"Assets"},
      query = {
        selection = {type = "resource", cardinality = "one"}
      },
      active = function(opts)
        return ends_with(editor.get(opts.selection, "path"), ".json")
      end,
      run = function(opts)
        local path = editor.get(opts.selection, "path")
        editor.execute("./scripts/minify-json.sh", path:sub(2))
      end
    }
  }
end

return M
```
エディターは、`get_commands()` がテーブルの配列を返すことを想定しています。各テーブルは、個別のコマンドを記述します。コマンドの記述は、次の要素で構成されます。

- `label`（必須）— ユーザーに表示されるメニュー項目のテキストです。
- `locations`（必須）— このコマンドを使用できる場所を記述する配列です。サポートされる値は、対応するメニューバーのメニューを表す `"Edit"`、`"View"`、`"Project"`、`"Debug"`、`"Help"`、**Project → Bundle** サブメニューを表す `"Bundle"`、および対応するコンテキストメニューを表す `"Assets"`、`"Outline"`、`"Scene"`、`"Code"` です。
- `query` — コマンドが関連情報をエディターに問い合わせ、操作するデータを定義するための仕組みです。`query` テーブルの各キーには、`active` と `run` のコールバックが引数として受け取る `opts` テーブル内のキーが対応します。サポートされるキーは次のとおりです。
  - `selection` は、何かが選択されている場合にこのコマンドが有効で、その選択対象を操作することを意味します。
    - `type` は、コマンドが対象とする選択ノードの型です。現在、次の型を指定できます。
      - `"resource"` — Assets と Outline では、対応するファイルを持つ選択項目です。メニューバー（Edit または View）では、現在開いているファイルです。
      - `"outline"` — Outline に表示できるものです。Outline では選択項目を表し、メニューバーでは現在開いているファイルを表します。
      - `"scene"` — Scene に描画できるものです。
    - `cardinality` は、選択項目がいくつ必要かを定義します。`"one"` の場合、コマンドのコールバックに渡される選択対象は単一のノード ID です。`"many"` の場合、1つ以上のノード ID の配列が渡されます。
  - `active_view` は、アクティブなエディタービューが要求された型と一致する場合に、このコマンドが有効であることを意味します。アクティブなビューは `opts.active_view` としてコマンドのコールバックに渡されます。
    - `type` は、コマンドが対象とするアクティブなビューの型で、`"code"`、`"scene"`、`"html"`、`"form"` のいずれかです。
    - アクティブなビューでは、`"type"`、`"resource"`、`"dirty"` プロパティがサポートされています。ビューに表示されているリソースを取得するには `editor.get(view, "resource")` を使い、未保存の変更があるかを確認するには `editor.get(view, "dirty")` を使います。
  - `argument` — コマンドの引数です。現在、引数を受け取るのは `"Bundle"` の場所にあるコマンドだけです。バンドル（bundle）コマンドを明示的に選択した場合は `true`、再バンドルの場合は `false` です。
- `id` - コマンドを識別する文字列です。たとえば、最後に使用したバンドルコマンドを `prefs` に保存するために使います。
- `active` - コマンドがアクティブかどうかを確認するために実行されるコールバックで、真偽値を返すことが想定されています。`locations` に `"Assets"`、`"Scene"`、`"Outline"` が含まれる場合、コンテキストメニューを表示するときに `active` が呼び出されます。場所に `"Edit"` または `"View"` が含まれる場合、キーボード入力やマウスクリックなど、ユーザーが操作するたびに active が呼び出されるため、`active` は比較的短時間で処理を終えるようにしてください。
- `run` - ユーザーがメニュー項目を選択したときに実行されるコールバックです。

### コマンドを使ってメモリ内のエディターの状態を変更する {#use-commands-to-change-the-in-memory-editor-state}

`run` ハンドラー内では、メモリ内のエディターの状態を取得、変更できます。状態の取得には `editor.get()` 関数を使い、ファイルや選択対象（`query = {selection = ...}` を使っている場合）の現在の状態をエディターに問い合わせます。テキストとして編集できるリソースの `"text"` プロパティや、Properties ビューに表示される一部のプロパティを取得できます。プロパティ名にマウスポインターを合わせると、エディタースクリプトでのプロパティ名を示すツールチップが表示されます。エディターの状態の変更には `editor.transact()` を使い、1つ以上の変更を、元に戻せる1つのステップにまとめます。たとえば、ゲームオブジェクトのトランスフォーム（transform）をリセットできるようにするには、次のようなコマンドを書けます。
```lua
{
  label = "Reset transform",
  locations = {"Outline"},
  query = {selection = {type = "outline", cardinality = "one"}},
  active = function(opts)
    local node = opts.selection
    return editor.can_set(node, "position") 
       and editor.can_set(node, "rotation") 
       and editor.can_set(node, "scale")
  end,
  run = function(opts)
    local node = opts.selection
    editor.transact({
      editor.tx.set(node, "position", {0, 0, 0}),
      editor.tx.set(node, "rotation", {0, 0, 0}),
      editor.tx.set(node, "scale", {1, 1, 1})
    })
  end
}
```

### アクティブなエディタービューでコマンドを使う {#use-commands-with-the-active-editor-view}

`"View"` などのメニューの場所にあるコマンドは、現在アクティブなエディタービューを問い合わせることができます。ユーザーが現在見ているファイルやシーンをコマンドで操作したい場合に役立ちます。

```lua
editor.command({
  label = "Print Active View",
  locations = {"View"},
  query = {active_view = {type = "code"}},
  run = function(opts)
    local view = opts.active_view
    local resource = editor.get(view, "resource")
    print(editor.get(view, "type"))
    print(editor.get(resource, "path"))
    print(editor.get(view, "dirty"))
  end
})
```

#### アトラスの編集 {#editing-atlases}

アトラスのプロパティの読み書きに加えて、アトラスの画像やアニメーションを読み取り、変更できます。アトラスには `images` と `animations` のノードリストプロパティが定義され、アニメーションには `images` ノードリストプロパティが定義されています。これらのプロパティには、`editor.tx.add`、`editor.tx.remove`、`editor.tx.clear` のトランザクションステップを使えます。

たとえば、アトラスに画像を追加するには、コマンドの `run` ハンドラーで次のコードを実行します。
```lua
editor.transact({
    editor.tx.add("/main.atlas", "images", {image="/assets/hero.png"})
})
```
アトラス内のすべての画像の集合を取得するには、次のコードを実行します。
```lua
local all_images = {} ---@type table<string, true>
-- first, collect all "bare" images
local image_nodes = editor.get("/main.atlas", "images")
for i = 1, #image_nodes do
    all_images[editor.get(image_nodes[i], "image")] = true
end
-- second, collect all images used in animations
local animation_nodes = editor.get("/main.atlas", "animations")
for i = 1, #animation_nodes do
    local animation_image_nodes = editor.get(animation_nodes[i], "images")
    for j = 1, #animation_image_nodes do
        all_images[editor.get(animation_image_nodes[j], "image")] = true
    end
end
pprint(all_images)
-- {
--     ["/assets/hero.png"] = true,
--     ["/assets/enemy.png"] = true,
-- }}
```
アトラス内のすべてのアニメーションを置き換えるには、次のようにします。
```lua
editor.transact({
    editor.tx.clear("/main.atlas", "animations"),
    editor.tx.add("/main.atlas", "animations", {
        id = "hero_run",
        images = {
            {image = "/assets/hero_run_1.png"},
            {image = "/assets/hero_run_2.png"},
            {image = "/assets/hero_run_3.png"},
            {image = "/assets/hero_run_4.png"}
        }
    })
})
```

#### タイルソースの編集 {#editing-tilesources}

タイルソース（tile source）には、アウトラインプロパティに加えて、次のプロパティが定義されています。
- `animations` - タイルソースのアニメーションノードのリストです。
- `collision_groups` - タイルソースのコリジョングループノードのリストです。
- `tile_collision_groups` - タイルソース内のタイルに対するコリジョングループの割り当てを表すテーブルです。

たとえば、タイルソースは次のように設定できます。
```lua
local tilesource = "/game/world.tilesource"
editor.transact({
    editor.tx.add(tilesource, "animations", {id = "idle", start_tile = 1, end_tile = 1}),
    editor.tx.add(tilesource, "animations", {id = "walk", start_tile = 2, end_tile = 6, fps = 10}),
    editor.tx.add(tilesource, "collision_groups", {id = "player"}),
    editor.tx.add(tilesource, "collision_groups", {id = "obstacle"}),
    editor.tx.set(tilesource, "tile_collision_groups", {
        [1] = "player",
        [7] = "obstacle",
        [8] = "obstacle"
    })
})
```

#### タイルマップの編集 {#editing-tilemaps}

タイルマップには、タイルマップレイヤーのノードリストである `layers` プロパティが定義されています。各レイヤーには、そのレイヤー上の境界のない 2D タイルグリッドを保持する `tiles` プロパティも定義されています。エンジンとは異なり、タイルには境界がなく、負の座標を含めてどこにでも追加できます。タイルを編集するために、エディタースクリプト API には次の関数を持つ `tilemap.tiles` モジュールが定義されています。
- `tilemap.tiles.new()` は、境界のない 2D タイルグリッドを保持する新しいデータ構造を作成します（エンジンとは異なり、エディターのタイルマップには境界がなく、座標は負の値にもなります）。
- `tilemap.tiles.get_tile(tiles, x, y)` は、指定した座標のタイルインデックスを取得します。
- `tilemap.tiles.get_info(tiles, x, y)` は、指定した座標のタイルの完全な情報を取得します（データの形式はエンジンの `tilemap.get_tile_info` 関数と同じです）。
- `tilemap.tiles.iterator(tiles)` は、タイルマップ内のすべてのタイルを巡回するイテレーターを作成します。
- `tilemap.tiles.clear(tiles)` は、タイルマップからすべてのタイルを削除します。
- `tilemap.tiles.set(tiles, x, y, tile_or_info)` は、指定した座標にタイルを設定します。
- `tilemap.tiles.remove(tiles, x, y)` は、指定した座標のタイルを削除します。

たとえば、タイルマップ全体の内容は次のように出力できます。
```lua
local layers = editor.get("/level.tilemap", "layers")
for i = 1, #layers do
    local layer = layers[i]
    local id = editor.get(layer, "id")
    local tiles = editor.get(layer, "tiles")
    print("layer " .. id .. ": {")
    for x, y, tile in tilemap.tiles.iterator(tiles) do
        print("  [" .. x .. ", " .. y .. "] = " .. tile)
    end
    print("}")
end
```

タイルのあるレイヤーをタイルマップに追加する例を示します。
```lua
local tiles = tilemap.tiles.new()
tilemap.tiles.set(tiles, 1, 1, 2)
editor.transact({
    editor.tx.add("/level.tilemap", "layers", {
        id = "new_layer",
        tiles = tiles
    })
})
```

#### パーティクルエフェクトの編集 {#editing-particlefx}

`modifiers` と `emitters` プロパティを使って、パーティクルエフェクトを編集できます。たとえば、加速度モディファイアーを持つ円形エミッターは次のように追加します。
```lua
editor.transact({
    editor.tx.add("/fire.particlefx", "emitters", {
        type = "emitter-type-circle",
        modifiers = {
          {type = "modifier-type-acceleration"}
        }
    })
})
```
パーティクルエフェクトの多くのプロパティは、カーブ（curve）またはカーブスプレッド（curve spread、カーブにランダム化の値を加えたもの）です。カーブは、空でない `points` のリストを持つテーブルとして表現されます。各ポイントは次のプロパティを持つテーブルです。
- `x` - ポイントの x 座標です。0で始まり、1で終わるようにします。
- `y` - ポイントの値です。
- `tx`（0から1）と `ty`（-1から1）- ポイントの接線です。たとえば角度が80度の場合、`tx` は `math.cos(math.rad(80))`、`ty` は `math.sin(math.rad(80))` にします。
カーブスプレッドには、数値の `spread` プロパティもあります。 

たとえば、既存のエミッターに対し、パーティクルの寿命にわたるアルファ値のカーブを次のように設定できます。
```lua
local emitter = editor.get("/fire.particlefx", "emitters")[1]
editor.transact({
    editor.tx.set(emitter, "particle_key_alpha", { points = {
        {x = 0,   y = 0, tx = 0.1, ty = 1}, -- start at 0, go up quickly
        {x = 0.2, y = 1, tx = 1,   ty = 0}, -- reach 1 at 20% of a lifetime
        {x = 1,   y = 0, tx = 1,   ty = 0}  -- slowly go down to 0
    }})
})
```
エミッターを作成するときに、テーブルで `particle_key_alpha` キーを使うこともできます。また、代わりに単一の数値を使って「静的な」カーブを表現できます。

#### コリジョンオブジェクトの編集 {#editing-collision-objects}

コリジョンオブジェクトには、既定のアウトラインプロパティに加えて、`shapes` ノードリストプロパティが定義されています。新しいコリジョン形状は次のように追加します。
```lua
editor.transact({
    editor.tx.add("/hero.collisionobject", "shapes", {
        type = "shape-type-box" -- or "shape-type-sphere", "shape-type-capsule"
    })
})
```
形状の `type` プロパティは作成時に必須で、形状を追加した後は変更できません。形状には3つの型があります。
- `shape-type-box` - `dimensions` プロパティを持つボックス形状です。
- `shape-type-sphere` - `diameter` プロパティを持つ球形状です。
- `shape-type-capsule` - `diameter` と `height` プロパティを持つカプセル形状です。

#### GUI ファイルの編集 {#editing-gui-files}

GUI ファイルには、アウトラインプロパティに加えて、いくつかのノードリストプロパティが定義されています。

- `layers` — レイヤーのエディターノードのリストです（並べ替え可能）。
- `fonts` — フォントのエディターノードのリストです。
- `materials` — マテリアル（material）のエディターノードのリストです。
- `textures` — テクスチャ（texture）のエディターノードのリストです。
- `particlefxs` — パーティクルエフェクトのエディターノードのリストです。
- `nodes` — GUI ノードのエディターノードのリストです。
- `layouts` — GUI レイアウトのエディターノードのリストです。

エディターの `layers` プロパティを使って、GUI レイヤーを編集できます。例:
```lua
editor.transact({
    editor.tx.add("/main.gui", "layers", {name = "foreground"}),
    editor.tx.add("/main.gui", "layers", {name = "background"})
})
```
また、レイヤーを並べ替えることもできます。
```lua
local fg, bg = table.unpack(editor.get("/main.gui", "layers"))
editor.transact({
    editor.tx.reorder("/main.gui", "layers", {bg, fg})
})
```
同様に、`fonts`、`materials`、`textures`、`particlefxs` プロパティを使って、フォント、マテリアル、テクスチャ、パーティクルエフェクトを編集します。
```lua
editor.transact({
    editor.tx.add("/main.gui", "fonts", {font = "/main.font"}),
    editor.tx.add("/main.gui", "materials", {name = "shine", material = "/shine.material"}),
    editor.tx.add("/main.gui", "particlefxs", {particlefx = "/confetti.particlefx"}),
    editor.tx.add("/main.gui", "textures", {texture = "/ui.atlas"})
})
```
これらのプロパティは並べ替えをサポートしていません。

最後に、`nodes` リストプロパティを使って GUI ノードを編集できます。例:
```lua
editor.transact({
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-box",
        position = {20, 20, 20}
    }),
    editor.tx.add("/main.gui", "nodes", {
        type = "gui-node-type-template",
        template = "/button.gui"
    }),
})
```
組み込みのノード型は次のとおりです。
- `gui-node-type-box`
- `gui-node-type-particlefx`
- `gui-node-type-pie`
- `gui-node-type-template`
- `gui-node-type-text`

Spine 拡張を使用している場合は、`gui-node-type-spine` ノード型も使えます。

GUI ファイルでレイアウトが定義されている場合、`layout:property` 構文を使ってレイアウトの値を取得、設定できます。例:
```lua
local node = editor.get("/main.gui", "nodes")[1]

-- GET:
local position = editor.get(node, "position")
pprint(position) -- {20, 20, 20}
local landscape_position = editor.get(node, "Landscape:position")
pprint(landscape_position) -- {20, 20, 20}

-- SET:
editor.transact({
    editor.tx.set(node, "Landscape:position", {30, 30, 30})
})
pprint(editor.get(node, "Landscape:position")) -- {30, 30, 30}
```

設定したレイアウトプロパティは、`editor.tx.reset` を使って既定値にリセットできます。
```lua
print(editor.can_reset(node, "Landscape:position")) -- true
editor.transact({
    editor.tx.reset(node, "Landscape:position")
})
```
テンプレートノードツリーは読み取りはできますが、編集はできません。テンプレートノードツリー内のノードのプロパティだけを設定できます。
```lua
local template = editor.get("/main.gui", "nodes")[2]
print(editor.can_add(template, "nodes")) -- false
local node_in_template = editor.get(template, "nodes")[1]
editor.transact({
    editor.tx.set(node_in_template, "text", "Button text")
})
print(editor.can_reset(node_in_template, "text")) -- true (overrides a value in the template)
```

#### ゲームオブジェクトの編集 {#editing-game-objects}

エディタースクリプトを使って、ゲームオブジェクトファイルのコンポーネント（component）を編集できます。コンポーネントには、参照として追加するものと埋め込むものの2種類があります。参照として追加するコンポーネントは `component-reference` 型を使い、他のリソースへの参照として機能します。上書きできるのは、スクリプトで定義された go プロパティだけです。埋め込みコンポーネントは `sprite`、`label` などの型を使い、そのコンポーネント型に定義されているすべてのプロパティを編集できます。また、コリジョンオブジェクトの形状などのサブコンポーネントを追加できます。たとえば、次のコードを使ってゲームオブジェクトを設定できます。
```lua
editor.transact({
    editor.tx.add("/npc.go", "components", {
        type = "sprite",
        id = "view"
    }),
    editor.tx.add("/npc.go", "components", {
        type = "collisionobject",
        id = "collision",
        shapes = {
            {
                type = "shape-type-box",
                dimensions = {32, 32, 32}
            }
        }
    }),
    editor.tx.add("/npc.go", "components", {
        type = "component-reference",
        path = "/npc.script",
        id = "controller",
        __hp = 100 -- set a go property defined in the script
    })
})
```

#### コレクションの編集 {#editing-collections}
エディタースクリプトを使ってコレクションを編集できます。ゲームオブジェクト（埋め込み、または参照）と、コレクション（参照）を追加できます。例:
```lua
local coll = "/char.collection"
editor.transact({
    editor.tx.add(coll, "children", {
        -- embbedded game object
        type = "go",
        id = "root",
        children = {
            {
                -- referenced game object
                type = "go-reference",
                path = "/char-view.go",
                id = "view"
            },
            {
                -- referenced collection
                type = "collection-reference",
                path = "/body-attachments.collection",
                id = "attachments"
            }
        },
        -- embedded gos can also have components
        components = {
            {
                type = "collisionobject",
                id = "collision",
                shapes = {
                    {type = "shape-type-box", dimensions = {2.5, 2.5, 2.5}}
                }
            },
            {
                type = "component-reference",
                id = "controller",
                path = "/char.script",
                __hp = 100 -- set a go property defined in the script
            }
        }
    })
})
```

エディターと同じように、参照として追加するコレクションは、編集しているコレクションのルートにのみ追加できます。また、ゲームオブジェクトは、埋め込みまたは参照として追加されたゲームオブジェクトにのみ追加でき、参照として追加されたコレクションや、そのコレクション内のゲームオブジェクトには追加できません。

### シェルコマンドを使う {#use-shell-commands}

`run` ハンドラー内では、`io` モジュールを使ってファイルに書き込んだり、`editor.execute()` コマンドを使ってシェルコマンドを実行したりできます。シェルコマンドを実行する際には、その出力を文字列として取得し、コード内で利用できます。たとえば、グローバルにインストールされた [`jq`](https://jqlang.github.io/jq/) を外部プロセスとして呼び出して JSON を整形するコマンドを作るには、次のように記述します。
```lua
{
  label = "Format JSON",
  locations = {"Assets"},
  query = {selection = {type = "resource", cardinality = "one"}},
  action = function(opts)
    local path = editor.get(opts.selection, "path")
    return path:match(".json$") ~= nil
  end,
  run = function(opts)
    local text = editor.get(opts.selection, "text")
    local new_text = editor.execute("jq", "-n", "--argjson", "data", text, "$data", {
      reload_resources = false, -- don't reload resources since jq does not touch disk
      out = "capture" -- return text output instead of nothing
    })
    editor.transact({ editor.tx.set(opts.selection, "text", new_text) })
  end
}
```
このコマンドはシェルプログラムを読み取り専用の方法で呼び出し、そのことを `reload_resources = false` でエディターに通知するため、この操作を元に戻せるという利点があります。

::: sidenote
エディタースクリプトをライブラリとして配布する場合は、エディターの各プラットフォーム用のバイナリプログラムを依存ライブラリに同梱するとよいでしょう。具体的な方法は、[ライブラリ内のエディタースクリプト](#editor-scripts-in-libraries)を参照してください。
:::

## ライフサイクルフック {#lifecycle-hooks}

特別な扱いを受けるエディタースクリプトファイルとして、プロジェクトのルートにある、*game.project* と同じディレクトリの `hooks.editor_script` があります。エディターからライフサイクルイベントを受け取るのは、このエディタースクリプトだけです。このファイルの例を示します。
```lua
local M = {}

function M.on_build_started(opts)
  local file = io.open("assets/build.json", "w")
  file:write('{"build_time": "' .. os.date() .. '"}')
  file:close()
end

return M
```
ライフサイクルフックを1つのエディタースクリプトファイルに限定したのは、新しいビルドステップを追加する手軽さよりも、ビルドフックの実行順序のほうが重要だからです。コマンドは互いに独立しており、最終的にはユーザーが選択した特定のコマンドを実行するため、メニューに表示される順序はあまり問題になりません。一方、異なるエディタースクリプトでビルドフックを指定できると、フックをどの順序で実行するかという問題が生じます。たとえば、コンテンツのチェックサムは圧縮した後で作成したいでしょう。各ステップの関数を明示的に呼び出してビルドステップの順序を定める1つのファイルを用意することで、この問題を解決できます。

`/hooks.editor_script` に指定できる既存のライフサイクルフックは、次のとおりです。
- `on_build_started(opts)` — Project Build または Debug Start のオプションを使って、ローカルまたはリモートのターゲットで実行するためにゲームをビルドするときに実行されます。ここでの変更は、ビルドされたゲームに反映されます。このフックからエラーを発生させると、ビルドは中止されます。`opts` は次のキーを含むテーブルです。
  - `platform` — ビルド対象のプラットフォームを表す、`%arch%-%os%` 形式の文字列です。現在は常に `editor.platform` と同じ値です。
- `on_build_finished(opts)` — 成功したか失敗したかにかかわらず、ビルドが終了したときに実行されます。`opts` は次のキーを持つテーブルです。
  - `platform` — `on_build_started` と同じです。
  - `success` — ビルドが成功したかどうかを表す、`true` または `false` です。
- `on_bundle_started(opts)` — バンドルを作成するとき、または Build HTML5 でゲームの HTML5 版をビルドするときに実行されます。`on_build_started` と同じように、このフックによる変更はバンドルに反映され、エラーが発生するとバンドルの作成は中止されます。`opts` は次のキーを持ちます。
  - `output_directory` — バンドルの出力先ディレクトリを指すファイルパスです。**Project ▸ Build HTML5** は、`build/default` 以下にある通常の Build の出力とは別に、たとえば `"/path/to/project/build/default_html5/__htmlLaunchDir"` のような独自の成果物ツリーを使います。
  - `platform` — ゲームのバンドルを作成する対象のプラットフォームです。指定できるプラットフォームの値の一覧は、[Bob マニュアル](/manuals/bob)を参照してください。
  - `variant` — バンドルバリアントです。`"debug"`、`"release"`、`"headless"` のいずれかです。
- `on_bundle_finished(opts)` — 成功したかどうかにかかわらず、バンドルの作成が終了したときに実行されます。`opts` は `on_bundle_started` の `opts` と同じデータに加えて、ビルドが成功したかどうかを示す `success` キーを持つテーブルです。
- `on_target_launched(opts)` — ユーザーがゲームを起動し、正常に開始したときに実行されます。`opts` には、起動したエンジンサービス（engine service）を指す `url` キーが含まれます。例: `"http://127.0.0.1:35405"`
- `on_target_terminated(opts)` — 起動したゲームが閉じられたときに実行されます。opts は `on_target_launched` と同じです。

ライフサイクルフックは現在、エディター専用の機能です。コマンドラインからバンドルを作成するときには、Bob は実行しない点に注意してください。

## 言語サーバー {#language-servers}

エディターは、[Language Server Protocol](https://microsoft.github.io/language-server-protocol/) の機能の一部をサポートしています。対応するのは、診断（lint）、補完、ホバー情報、Structure ペインのドキュメントシンボル、定義への移動、参照の検索、シンボルの名前変更です。シンボルにマウスポインターを合わせると、言語サーバー（language server）からの情報が表示されます。シンボルにカーソルを置き、<kbd>F2</kbd> で名前を変更し、<kbd>F12</kbd> で定義に移動し、<kbd>Shift+F12</kbd> で参照を検索します。これらの操作は <kbd>Edit</kbd> メニューからも実行できます。

言語サーバーを定義するには、エディタースクリプトの `get_language_servers` 関数を次のように編集する必要があります。

```lua
function M.get_language_servers()
  local command = 'build/plugins/my-ext/plugins/bin/' .. editor.platform .. '/lua-lsp'
  if editor.platform == 'x86_64-win32' then
    command = command .. '.exe'
  end
  return {
    {
      languages = {'lua'},
      watched_files = {
        { pattern = '**/.luacheckrc' }
      },
      command = {command, '--stdio'}
    }
  }
end
```
エディターは、指定された `command` を使って言語サーバーを起動し、サーバープロセスの標準入力と標準出力を使って通信します。

言語サーバーの定義テーブルには、次の項目を指定できます。
- `languages`（必須）— サーバーが対象とする言語のリストです。[こちら](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers)で定義された値を使います（ファイルの拡張子も使用できます）。
- `command`（必須）- コマンドとその引数の配列です。
- `watched_files` - `pattern` キー（glob パターン）を持つテーブルの配列です。サーバーの[監視対象ファイルの変更](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles)通知を発生させます。

## HTTP サーバー {#http-server}

実行中のエディターの各インスタンスでは、HTTP サーバーが動作しています。このサーバーはエディタースクリプトを使って拡張できます。エディター HTTP サーバーを拡張するには、エディタースクリプトに `get_http_server_routes` 関数を追加する必要があります。この関数は追加するルートを返します。
```lua
print("My route: " .. http.server.url .. "/my-extension")

function M.get_http_server_routes()
  return {
    http.server.route("/my-extension", "GET", function(request)
      return http.server.response(200, "Hello world!")
    end)
  }
end
```
エディタースクリプトを再読み込みすると、コンソールに `My route: http://0.0.0.0:12345/my-extension` という出力が表示されます。このリンクをブラウザーで開くと、`"Hello world!"` というメッセージが表示されます。

入力として受け取る `request` 引数は、リクエストに関する情報を含む単純な Lua テーブルです。`path`（`/` で始まる URL のパス要素）、リクエストの `method`（例: `"GET"`）、`headers`（小文字のヘッダー名を持つテーブル）といったキーを含み、必要に応じて `query`（クエリー文字列）や `body`（ルートで本文の解釈方法を定義している場合）も含みます。たとえば、JSON の本文を受け取るルートを作るには、コンバーターのパラメーターに `"json"` を指定して定義します。
```lua
http.server.route("/my-extension/echo-request", "POST", "json", function(request)
  return http.server.json_response(request)
end)
```
コマンドラインで `curl` と `jq` を使って、このエンドポイントをテストできます。
```sh
curl 'http://0.0.0.0:12345/my-extension/echo-request?q=1' -X POST --data '{"input": "json"}' | jq
{
  "path": "/my-extension/echo-request",
  "method": "POST",
  "query": "q=1",
  "headers": {
    "host": "0.0.0.0:12345",
    "content-type": "application/x-www-form-urlencoded",
    "accept": "*/*",
    "user-agent": "curl/8.7.1",
    "content-length": "17"
  },
  "body": {
    "input": "json"
  }
}
```
ルートのパスはパターンをサポートしています。リクエストパスから抽出した値を、リクエストの一部としてハンドラー関数に渡せます。例:
```lua
http.server.route("/my-extension/setting/{category}.{key}", function(request)
  return http.server.response(200, tostring(editor.get("/game.project", request.category .. "." .. request.key)))
end)
```
この状態で、たとえば `http://0.0.0.0:12345/my-extension/setting/project.title` を開くと、`/game.project` ファイルから取得したゲームのタイトルが表示されます。

単一のパス要素のパターンに加えて、`{*name}` 構文を使って URL パスの残りの部分にも一致させることができます。たとえば、次のコードはプロジェクトのルートからファイルを配信する単純なファイルサーバーのエンドポイントです。
```lua
http.server.route("/my-extension/files/{*file}", function(request)
  local attrs = editor.external_file_attributes(request.file)
  if attrs.is_file then
    return http.server.external_file_response(request.file)
  else
    return 404
  end
end)
```
この状態で、たとえば `http://0.0.0.0:12345/my-extension/files/main/main.collection` をブラウザーで開くと、`main/main.collection` ファイルの内容が表示されます。

## ライブラリ内のエディタースクリプト {#editor-scripts-in-libraries}

コマンドを含むライブラリを公開して他の人に使ってもらうことができ、それらのコマンドはエディターが自動的に読み込みます。一方、フックはプロジェクトのルートフォルダーにあるファイルで定義する必要がありますが、ライブラリが公開するのはサブフォルダーだけなので、自動的には読み込まれません。これはビルド処理をより細かく制御できるようにするためです。ライフサイクルフックを `.lua` ファイル内の通常の関数として作成することはできるため、ライブラリのユーザーは自分の `/hooks.editor_script` から require して使用できます。

また、依存ライブラリは Assets ビューに表示されますが、ファイルとしては存在しません（zip アーカイブ内のエントリーです）。エディターに、依存ライブラリ内の一部のファイルを `build/plugins/` フォルダーへ展開させることができます。そのためには、ライブラリのフォルダーに `ext.manifest` ファイルを作成し、その `ext.manifest` ファイルと同じフォルダーに `plugins/bin/${platform}` フォルダーを作成します。このフォルダー内のファイルは `/build/plugins/${extension-path}/plugins/bin/${platform}` フォルダーへ自動的に展開されるため、エディタースクリプトから参照できます。

## 環境設定 {#preferences}

エディタースクリプトでは環境設定を定義して使用できます。環境設定は、ユーザーのコンピューターに永続的に保存され、コミットされないデータです。次の3つの主な特徴があります。
- 型付き: 各環境設定には、データ型と、既定値などのメタデータを含むスキーマ定義があります。
- スコープ付き: 環境設定には、プロジェクト単位またはユーザー単位のスコープがあります。
- 入れ子構造: 各環境設定のキーはドットで区切った文字列で、最初のパス要素はエディタースクリプトを識別し、残りの要素は 

すべての環境設定は、スキーマを定義して登録する必要があります。
```lua
function M.get_prefs_schema()
  return {
    ["my_json_formatter.jq_path"] = editor.prefs.schema.string(),
    ["my_json_formatter.indent.size"] = editor.prefs.schema.integer({default = 2, scope = editor.prefs.SCOPE.PROJECT}),
    ["my_json_formatter.indent.type"] = editor.prefs.schema.enum({values = {"spaces", "tabs"}, scope = editor.prefs.SCOPE.PROJECT}),
  }
end
```
このようなエディタースクリプトを再読み込みすると、エディターがこのスキーマを登録します。その後、エディタースクリプトで環境設定を取得、設定できます。例:
```lua
-- Get a specific preference
editor.prefs.get("my_json_formatter.indent.type")
-- Returns: "spaces"

-- Get an entire preference group
editor.prefs.get("my_json_formatter")
-- Returns:
-- {
--   jq_path = "",
--   indent = {
--     size = 2,
--     type = "spaces"
--   }
-- }

-- Set multiple nested preferences at once
editor.prefs.set("my_json_formatter.indent", {
    type = "tabs",
    size = 1
})
```

## 実行モード {#execution-modes}

エディタースクリプトのランタイムには、 **即時（immediate）** と **長時間実行（long-running）** という2つの実行モードがあります。エディタースクリプトでは、ほとんどの場合、その違いを意識する必要はありません。 

**即時**モードは、エディターがスクリプトからの応答をできるだけ早く受け取る必要がある場合に使われます。たとえば、メニューコマンドの `active` コールバックは即時モードで実行されます。これは、ユーザーのエディター操作に応じてエディターの UI スレッド上で確認処理が行われ、同じフレーム内に UI を更新する必要があるためです。 

**長時間実行**モードは、エディターがスクリプトから瞬時の応答を必要としない場合に使われます。たとえば、メニューコマンドの `run` コールバックは**長時間実行**モードで実行されるため、スクリプトは処理の完了までにより多くの時間を使えます。

エディタースクリプトで使える関数の中には、実行に多くの時間がかかるものがあります。たとえば、`editor.execute("git", "status", {reload_resources=false, out="capture"})` は、十分に大きなプロジェクトでは最大1秒かかることがあります。エディターの応答性とパフォーマンスを維持するため、時間がかかる可能性のある関数は、エディターが即時の応答を必要とするコンテキストでは使用できません。即時のコンテキストでそのような関数を使おうとすると、`Cannot use long-running editor function in immediate context` というエラーが発生します。このエラーを解消するには、即時のコンテキストでこれらの関数を使わないようにしてください。

次の関数は長時間実行の関数とみなされ、即時モードでは使用できません。
- `editor.create_directory()`、`editor.create_resources()`、`editor.delete_directory()`、`editor.save()`、`os.remove()`、`file:write()`: これらの関数はディスク上のファイルを変更するため、エディターはメモリ内のリソースツリーをディスクの状態と同期します。大規模なプロジェクトでは、この処理に数秒かかることがあります。
- `editor.execute()`: シェルコマンドの実行には、予測できない長さの時間がかかることがあります。
- `editor.transact()`: 広範囲から参照されているノードに対する大きなトランザクションには数百ミリ秒かかることがあり、UI の応答性を保つには遅すぎます。

次のコード実行コンテキストでは、即時モードを使います。
- メニューコマンドの `active` コールバック: エディターは同じ UI フレーム内にスクリプトからの応答を必要とします。
- エディタースクリプトのトップレベル: エディタースクリプトを再読み込みするという操作自体には、副作用がないことを想定しています。

## アクション {#actions}

::: sidenote
以前は、エディターが Lua VM とブロッキング方式でやり取りしていました。一部のやり取りはエディターの UI スレッドから行う必要があるため、エディタースクリプトはブロックしてはいけないという厳格な要件がありました。このため、たとえば `editor.execute()` や `editor.transact()` は存在しませんでした。代わりに、フックやコマンドの `run` ハンドラーから「アクション（action）」の配列を返すことで、スクリプトの実行やエディターの状態の変更を開始していました。

現在、エディターは Lua VM とノンブロッキング方式でやり取りするため、これらのアクションは不要になりました。`editor.execute()` などの関数を使うほうが便利で簡潔であり、より多くのことを実現できます。アクションは現在**非推奨**ですが、削除する予定はありません。
:::

エディタースクリプトは、コマンドの `run` 関数や `/hooks.editor_script` のフック関数からアクションの配列を返すことができます。その後、これらのアクションをエディターが実行します。

アクションは、エディターが行う処理を記述するテーブルです。各アクションには `action` キーがあります。アクションには、元に戻せるものと元に戻せないものの2種類があります。

### 元に戻せるアクション {#undoable-actions}

::: sidenote
`editor.transact()` の使用を推奨します。
:::

元に戻せるアクションは、実行後に元に戻すことができます。コマンドが複数の元に戻せるアクションを返した場合、それらはまとめて実行され、元に戻す際にもまとめて戻されます。可能であれば、元に戻せるアクションを使ってください。欠点は、制限が多いことです。

元に戻せる既存のアクションは、次のとおりです。
- `"set"` — エディター内のノードのプロパティに値を設定します。例:
  ```lua
  {
    action = "set",
    node_id = opts.selection,
    property = "text",
    value = "current time is " .. os.date()
  }
  ```
  `"set"` アクションには、次のキーが必要です。
  - `node_id` — ノード ID のユーザーデータです。エディターから受け取ったノード ID の代わりに、たとえば `"/main/game.script"` のようなリソースパスを使うこともできます。
  - `property` — 設定するノードのプロパティです。例: `"text"`
  - `value` — プロパティの新しい値です。`"text"` プロパティの場合は文字列である必要があります。

### 元に戻せないアクション {#non-undoable-actions}

::: sidenote
`editor.execute()` の使用を推奨します。
:::

元に戻せないアクションは、元に戻す操作の履歴を消去します。そのため、このようなアクションを元に戻すには、バージョン管理などの別の手段を使う必要があります。

元に戻せない既存のアクションは、次のとおりです。
- `"shell"` — シェルスクリプトを実行します。例:
  ```lua
  {
    action = "shell",
    command = {
      "./scripts/minify-json.sh",
      editor.get(opts.selection, "path"):sub(2) -- trim leading "/"
    }
  }
  ```
  `"shell"` アクションには、コマンドとその引数の配列である `command` キーが必要です。

### アクションと副作用を組み合わせる {#mixing-actions-and-side-effects}

元に戻せるアクションと元に戻せないアクションを組み合わせることができます。アクションは順番に実行されるため、その順序によっては、コマンドの一部の処理を元に戻せなくなります。

アクションを返すことが想定されている関数からアクションを返す代わりに、`io.open()` を使ってファイルを直接読み書きすることもできます。これによりリソースが再読み込みされ、元に戻す操作の履歴が消去されます。
