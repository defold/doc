---
title: ホットリロード
brief: このマニュアルでは、Defold のホットリロード機能について説明します。
---

# リソースのホットリロード {#hot-reloading-resources}

Defold では、リソース（resource）のホットリロード（hot reload）ができます。この機能は、ゲーム開発時の特定の作業を大幅に高速化するのに役立ちます。ゲームを実行したまま、そのコードやコンテンツを変更できます。主な用途は次のとおりです。

- Lua スクリプトでゲームプレイのパラメーターを調整します。
- グラフィック要素（パーティクルエフェクト（particle effect）や GUI 要素など）を編集、調整して、実際に使われる場面で結果を確認します。
- シェーダー（shader）のコードを編集、調整して、実際に使われる場面で結果を確認します。
- ゲームを停止せずにレベルを再起動したり、状態を設定したりして、ゲームのテストをしやすくします。

## ホットリロードの方法 {#how-to-hot-reload}

エディターからゲームを起動します（<kbd>Project ▸ Build</kbd>）。

その後、更新したリソースをリロードするには、メニュー項目の <kbd>File ▸ Hot Reload</kbd> を選択するか、対応するキーボードショートカットを押します。

![リソースのリロード](images/hot-reload/menu.png)

## デバイス上でのホットリロード {#hot-reloading-on-device}

ホットリロードは、デスクトップだけでなくデバイス上でも動作します。デバイス上で使用するには、モバイルデバイスでゲームのデバッグビルドまたは[開発用アプリ](/manuals/dev-app)を実行し、エディターでそのデバイスをターゲットとして選択します。

![ターゲットデバイス](images/hot-reload/target.png)

ここでビルドして実行すると、エディターはデバイス上で動作しているアプリにすべてのアセットをアップロードし、ゲームを起動します。それ以降、ホットリロードしたファイルはすべてデバイス上で更新されます。

たとえば、スマートフォンで実行中のゲームに表示されている GUI にボタンを2つ追加するには、GUI ファイルを開きます。

![GUI のリロード](images/hot-reload/gui.png)

新しいボタンを追加し、GUI ファイルを保存してホットリロードします。これでスマートフォンの画面に新しいボタンが表示されます。

![リロード後の GUI](images/hot-reload/gui-reloaded.png)

ファイルをホットリロードすると、エンジンはリロードした各リソースファイルをコンソールに出力します。

## スクリプトのリロード {#reloading-scripts}

リロードされた Lua スクリプトファイルはすべて、実行中の Lua 環境で再実行されます。

```lua
local my_value = 10

function update(self, dt)
    print(my_value)
end
```

`my_value` を 11 に変更してファイルをホットリロードすると、すぐに反映されます。

```text
...
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
DEBUG:SCRIPT: 10
INFO:RESOURCE: /main/hunter.scriptc was successfully reloaded.
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
DEBUG:SCRIPT: 11
...
```

ホットリロードによってライフサイクル関数の実行が変わることはない点に注意してください。たとえば、ホットリロード時に `init()` は呼び出されません。ただし、ライフサイクル関数を再定義すると、新しいバージョンが使用されます。

## Lua モジュールのリロード {#reloading-lua-modules}

モジュールファイル内のグローバルスコープに変数を追加していれば、そのファイルをリロードすると、これらのグローバル変数が変更されます。

```lua
--- my_module.lua
my_module = {}
my_module.val = 10
```

```lua
-- user.script
require "my_module"

function update(self, dt)
    print(my_module.val) -- hot reload "my_module.lua" and the new value will print
end
```

Lua モジュール（Lua module）でよく使われるパターンは、ローカルテーブルを作成し、値を設定してから返す方法です。

```lua
--- my_module.lua
local M = {} -- a new table object is created here
M.val = 10
return M
```

```lua
-- user.script
local mm = require "my_module"

function update(self, dt)
    print(mm.val) -- will print 10 even if you change and hot reload "my_module.lua"
end
```

`my_module.lua` を変更してリロードしても、`user.script` の動作は _変わりません_。その理由と、この落とし穴を避ける方法については、[モジュールのマニュアル](/manuals/modules)を参照してください。

## on_reload() 関数 {#the-on_reload-function}

すべてのスクリプトコンポーネント（script component）で `on_reload()` 関数を定義できます。この関数が存在する場合、スクリプトがリロードされるたびに呼び出されます。これは、データの確認や変更、メッセージの送信などに役立ちます。

```lua
function on_reload(self)
    print(self.velocity)

    msg.post("/level#controller", "setup")
end
```

## シェーダーコードのリロード {#reloading-shader-code}

頂点シェーダーとフラグメントシェーダーをリロードすると、GLSL コードがグラフィックスドライバーによって再コンパイルされ、GPU にアップロードされます。GLSL は非常に低水準で記述されるため、シェーダーコードによるクラッシュは起こりやすく、その場合はエンジンも停止します。
