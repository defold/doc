---
title: Defold でのデバッグ
brief: このマニュアルでは、Defold に備わっているデバッグ機能について説明します。
---

# ゲームロジックのデバッグ {#debugging-game-logic}

Defold には、状態を調べる機能を備えた Lua デバッガーが統合されています。組み込みの[プロファイリングツール](/manuals/profiling)と合わせて、ゲームロジックの不具合の原因を見つけたり、パフォーマンスの問題を分析したりするのに役立つ強力なツールです。

## 出力と描画によるデバッグ {#print-and-visual-debugging}

Defold でゲームをデバッグする最も簡単な方法は、[プリントデバッグ](http://en.wikipedia.org/wiki/Debugging#Techniques)です。`print()` や [`pprint()`](/ref/builtins#pprint) 文を使って、変数を確認したり、実行の流れを表示したりします。スクリプトのないゲームオブジェクト（game object）が不自然に動作する場合は、デバッグだけを目的としたスクリプトを取り付けることもできます。いずれの出力関数も、エディターの *Console* ビューと[ゲームログ](/manuals/debugging-game-and-system-logs)に出力します。

出力に加えて、エンジンはデバッグ用のテキストや直線を画面に描画することもできます。これには、`@render` ソケット（socket）にメッセージを送信します。

```lua
-- Draw value of "my_val" with debug text on the screen
msg.post("@render:", "draw_text", { text = "My value: " .. my_val, position = vmath.vector3(200, 200, 0) })

-- Draw colored text on the screen
local color_green = vmath.vector4(0, 1, 0, 1)
msg.post("@render:", "draw_debug_text", { text = "Custom color", position = vmath.vector3(200, 180, 0), color = color_green })

-- Draw debug line between player and enemy on the screen
local start_p = go.get_position("player")
local end_p = go.get_position("enemy")
local color_red = vmath.vector4(1, 0, 0, 1)
msg.post("@render:", "draw_line", { start_point = start_p, end_point = end_p, color = color_red })
```

描画によるデバッグ用のメッセージは、レンダリングパイプラインにデータを追加します。このデータは通常のレンダリングパイプラインの一部として描画されます。

* `"draw_line"` は、レンダースクリプト（render script）の `render.draw_debug3d()` 関数で描画するデータを追加します。
* `"draw_text"` は、`/builtins/fonts/debug/always_on_top_font.material` マテリアル（material）を使う `/builtins/fonts/debug/always_on_top.font` で描画されます。
* `"draw_debug_text"` は `"draw_text"` と同じですが、指定した色で描画されます。

このデータは毎フレーム更新したい場合が多いため、`update()` 関数内でメッセージを送信するとよいでしょう。

## デバッガーの実行 {#running-the-debugger}

Lua デバッガーは、ネイティブのデバッグビルドとヘッドレスビルドで利用できます。エディターと同じ Defold バージョンのエンジンを使ってください。リリースビルドと Web ビルドにはデバッガーを接続できません。

デバッガーを実行するには、<kbd>Debug ▸ Start/Attach</kbd> を選択します。デバッガーを接続した状態でゲームを起動するか、すでに実行中のゲームに接続します。デバッグ用にゲームを起動するときは、起動時のスクリプトが実行される前に、エディターが有効なブレークポイントを設定します。そのため、起動前に `init()` にブレークポイントを設定できます。

デバイスに接続するには、<kbd>Project ▸ Targets</kbd> でデバイスを選択し、<kbd>Debug ▸ Start/Attach</kbd> を選びます。接続すると、次の Lua 行で一時停止します。対応するローカルおよびリモートのターゲットでは、エディターがデバッガー接続を自動的に設定します。接続要件は[リモートターゲット](#remote-targets)を、外部デバッガーの接続方法は[ネイティブ DAP 接続](#native-dap-connections)を参照してください。

![概要](images/debugging/overview.png)

デバッガーが接続されると、コンソールのデバッガー操作ボタン、または <kbd>Debug</kbd> メニューからゲームの実行を制御できます。

Break
: ![一時停止](images/debugging/pause.svg){width=60px .left}
  次のソース行で Lua の実行を一時停止します。ゲームの状態を調べたり、1ステップずつ実行したり、次のブレークポイントまで実行を続けたりできます。現在の実行位置は、コードエディターに表示されます。

  ![スクリプト](images/debugging/script.png)

Continue
: ![再開](images/debugging/play.svg){width=60px .left}
  ゲームの実行を再開します。一時停止を押すか、設定したブレークポイントに到達するまで、ゲームのコードは実行を続けます。設定したブレークポイントで実行が中断すると、コードエディターではブレークポイントのマーカーに重ねて実行位置が示されます。

  ![実行の中断](images/debugging/break.png)

Stop
: ![停止](images/debugging/stop.svg){width=60px .left}
  デバッガーを停止します。このボタンを押すと、デバッガーは直ちに停止してゲームから切り離され、実行中のゲームも終了します。

Step Over
: ![ステップオーバー](images/debugging/step_over.svg){width=60px .left}
  プログラムの実行を1ステップ進めます。その実行に別の Lua 関数の呼び出しが含まれる場合は、_関数の内部にはステップインせず_ に実行を続け、関数呼び出しの次の行で停止します。この例で「step over」を押すと、デバッガーはコードを実行し、関数 `nextspawn()` の呼び出しがある行の下の `end` 文で停止します。

  ![ステップ実行](images/debugging/step.png)

::: sidenote
ステップ実行は Lua のソース行に従います。ループの繰り返しなどで同じ行に戻ることがあるため、ファイルの次の行へ進むとは限りません。
:::

Step Into
: ![ステップイン](images/debugging/step_in.svg){width=60px .left}
  プログラムの実行を1ステップ進めます。その実行に別の Lua 関数の呼び出しが含まれる場合は、_関数の内部にステップインします_ 。関数を呼び出すと、コールスタックにエントリーが追加されます。コールスタックのリストで各エントリーをクリックすると、エントリーポイントと、そのクロージャ内のすべての変数の内容を確認できます。ここでは、関数 `nextspawn()` の内部にステップインしています。

  ![関数へのステップイン](images/debugging/step_into.png)

Step Out
: ![ステップアウト](images/debugging/step_out.svg){width=60px .left}
  現在の関数から戻るまで実行を続けます。関数の内部にステップインした場合、「step out」ボタンを押すと、関数から戻るまで実行が続きます。

ブレークポイントの設定と解除
: Lua コードには任意の数のブレークポイントを設定できます。デバッガーを接続してゲームを実行すると、次に到達したブレークポイントで実行が停止し、次の操作を待ちます。

  ![ブレークポイントの追加](images/debugging/add_breakpoint.png)

  ブレークポイントを設定または解除するには、コードエディターの行番号のすぐ右にある列をクリックします。メニューから <kbd>Edit ▸ Toggle Breakpoint</kbd> を選択することもできます。

ブレークポイントの無効化と有効化
: ブレークポイントは削除せずに一時的に無効化できます。無効なブレークポイントは実行中に無視されますが、いつでも再度有効化できます。コードエディターの行番号付近にあるブレークポイントを右クリックし、`Enabled` チェックボックスを切り替えます。無効なブレークポイントは中抜きで表示され、無効な状態であることを示します。

  ![ブレークポイントの無効化](images/debugging/disable_breakpoint.png)

条件付きブレークポイントの設定
: ブレークポイントに条件を設定し、その条件の評価結果が true になる場合にだけ実行を停止させることができます。この条件からは、コードの実行時にその行で利用できるローカル変数にアクセスできます。

  ![ブレークポイントの編集](images/debugging/edit_breakpoint.png)

  ブレークポイントの条件を編集するには、コードエディターの行番号のすぐ右にある列を右クリックするか、メニューから <kbd>Edit ▸ Edit Breakpoint</kbd> を選択します。

Lua 式の評価
: ゲームを一時停止した状態で *Call Stack* のフレームを選択し、コンソールの下部に Lua の式または文を入力して <kbd>Enter</kbd> を押します。選択したフレームのローカル変数、アップバリュー、グローバル変数を使って評価します。テーブルの結果には、入れ子になった内容も含まれます。

  ![コンソール](images/debugging/console.png)

  `self` を使用できるフレームで `self.score = 100` とするなど、代入によって値を変更することもできます。評価したコードは、ゲームが実行するコードと同じようにゲームの状態に影響します。

変数の調査
: *Call Stack* のフレームを選択すると、*Variables* ビューでそのローカル変数とアップバリューを調べられます。`_G` を展開するとグローバル変数を、テーブルや `self` を展開するとそのフィールドを調べられます。ステップ実行、フレームの切り替え、評価後の更新では、エディターは展開したパス、選択状態、スクロール位置を保ちながら、現在の値を取得します。

デバッガーの切り離し
: <kbd>Debug ▸ Detach Debugger</kbd> を選択すると、ゲームからデバッガーが切断されます。ゲームはすぐに実行を再開します。ゲームを再起動せずに再接続するには、<kbd>Debug ▸ Start/Attach</kbd> を使います。

## ネイティブ DAP 接続 {#native-dap-connections}

エンジンには、TCP 経由のネイティブ Debug Adapter Protocol（DAP）サーバーがあります。外部の DAP クライアントを使う場合は、ネイティブの Defold デバッグエンジンまたはヘッドレスエンジンでリスナーを起動し、エンジンのアドレスとポートにクライアントを接続します。<kbd>Debug ▸ Start/Attach</kbd> を使う場合は、エディターがリスナーを自動的に設定します。

現在のエディターは、MobDebug にのみ対応する古いエンジンには接続できません。現在のバージョンでは `require "builtins.scripts.mobdebug"` を呼び出す必要はなく、利用することもできません。

### リスナーの起動 {#starting-the-listener}

まずプロジェクトをビルドします。`build/default/game.projectc` があるプロジェクトディレクトリから、以下の[起動時の設定上書き](/manuals/project-settings/#setting-config-values-on-engine-startup)を指定して、ネイティブのデバッグエンジンを実行します。

```sh
dmengine --config=debugger.enabled=1 \
  --config=debugger.port=8172 --config=debugger.wait=1
```

DAP クライアントを `127.0.0.1:8172` に接続します。エンジンは、クライアントがブレークポイントを設定するまで、起動時のスクリプトを実行せずに待機します。

| 設定 | デフォルト | 用途 |
| --- | --- | --- |
| `debugger.enabled` | `0` | `1` に設定すると、エンジンの起動時にリスナーを起動します。 |
| `debugger.address` | `127.0.0.1` | 待ち受ける IPv4 アドレス。デフォルトでは同じコンピューターからの接続を受け入れます。 |
| `debugger.port` | `8172` | 待ち受ける TCP ポート。`0` を指定すると、使用可能なポートを選択します。 |
| `debugger.wait` | `0` | `1` に設定すると、起動時のスクリプトを実行する前に、デバッガークライアントの設定を待機します。 |

これらの値は、[game.project の Debugger セクション](/manuals/project-settings/#debugger)にも追加できます。<kbd>Debug ▸ Start/Attach</kbd> ではエディターがリスナーを自動的に設定するため、手動設定が必要なのは自分でリスナーを起動する場合だけです。

エンジンのログには、選択されたアドレスとポートが表示されます。`debugger.wait=0` ではゲームがすぐに起動し、後から接続できます。`debugger.wait=1` では、ブレークポイントを含むセッションの設定をクライアントが完了するまで待機します。ローカルでデバッグ起動する場合、エディターは使用可能なポートを自動的に選択します。

クライアントを切断すると実行を再開し、リスナーは別の接続を受け付けられる状態を保ちます。起動時の設定を待機中に切断した場合も、エンジンの待機は解除されます。リスナーを起動できない場合、エンジンはエラーを記録して起動を続けます。Lua から `debugger.start(0)` を呼び出すと、使用可能なポートを選択して再試行できます。

### 実行中にリスナーを有効にする {#enabling-the-listener-while-running}

ゲームを再起動せず、スクリプトからリスナーを有効にするには、次のようにします。

```lua
if debugger then
    local port = debugger.start(0)
    print("DAP listener port:", port)
end
```

`debugger.start([port [, address]])` は待ち受けるポートをすぐに返します。クライアントを待機したり、ゲームを一時停止したりしません。引数を省略すると `debugger.port` と `debugger.address` を使い、`0` を渡すと使用可能なポートを選択します。繰り返し呼び出すと、既存のリスナーのポートを返し、アドレスやポートは変更しません。`debugger` モジュールは、ネイティブのデバッグエンジンとヘッドレスエンジンが提供します。

ポートは `0` から `65535` までの整数である必要があります。アドレスだけを上書きするには、第1引数に `nil` を渡します。不正な引数やリスナーのバインド失敗は、Lua エラーを発生させます。

### リモートターゲット {#remote-targets}

別のコンピューターから直接接続するには、デバイスの IPv4 インターフェースまたは `0.0.0.0`（すべての IPv4 インターフェース）にリスナーをバインドします。たとえば `debugger.start(8172, "0.0.0.0")` を使うか、上記の起動コマンドに `--config=debugger.address=0.0.0.0` を追加します。クライアントはデバイスの実際の IP アドレスに接続し、待ち受けポートへの TCP アクセスを許可します。`0.0.0.0` はバインド用のアドレスであり、クライアントに入力する接続先アドレスではありません。

Defold エディターは、このリモート用のバインドを自動的に要求し、リモートターゲットにはポート `8172 + project.instance_index` を使います。動的に選択されたリモートポートは検出できません。リモートのリスナーを localhost または別のポートですでに起動した場合は、エディターから接続する前にエンジンを再起動してください。

デバッガーは Lua を評価でき、認証機能を持ちません。リモートアクセスは、信頼できる開発用ネットワークでのみ有効にしてください。

### 外部クライアント {#external-clients}

TCP 経由で DAP サーバーに直接接続できるクライアントを使います。ソースマッピングを、`game.project` があるフォルダー（DAP の attach 引数 `localRoot`）に設定します。先にエンジンのリスナーを起動し、その後クライアントを接続します。

#### VS Code {#vs-code}

[Lua Debug 拡張](https://marketplace.visualstudio.com/items?itemName=actboy168.lua-debug)（`actboy168.lua-debug`）をインストールし、`game.project` があるフォルダーを VS Code で開いて、`.vscode/launch.json` に次の設定を追加します。

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Defold Lua",
      "type": "lua",
      "request": "attach",
      "address": "127.0.0.1:8172",
      "debugServer": 8172,
      "localRoot": "${workspaceFolder}",
      "stopOnEntry": false
    }
  ]
}
```

VS Code が `.script`、`.gui_script`、`.render_script` ファイルをプレーンテキストとして開く場合は、ブレークポイントを設定する前に、ステータスバーの言語表示から **Lua** を選択してください。

スクリプトの `init()` 関数などにブレークポイントを設定します。[上記の起動コマンド](#starting-the-listener)でエンジンを起動し、VS Code の **Run and Debug** ビューで **Attach to Defold Lua** を選択します。`debugger.wait=1` では、クライアントがブレークポイントを設定してから、エンジンが起動時のスクリプトを実行します。接続後の次の Lua 行でも一時停止するには、`stopOnEntry` を `true` に設定します。

VS Code の [`debugServer` 設定](https://code.visualstudio.com/api/extension-guides/debugger-extension#development-setup-for-mock-debug)は、エンジンのローカル TCP リスナーに直接接続します。`address` フィールドは Lua Debug 拡張の接続設定で必須です。リスナーポートを変更する場合は、両方のフィールドを更新します。`localRoot` は、エンジンの Lua ソース名をファイルに対応付けられるよう、プロジェクトフォルダーを指す必要があります。

リモートエンジンの場合は、DAP ポートを localhost に転送して、両方のフィールドに転送先のポートを指定するか、リモートホストに直接接続する DAP クライアントを使います。

## Breakpoints タブ {#breakpoints-tab}

  ![Breakpoints タブ](images/debugging/breakpoints_tab.png)

  複数のスクリプトにわたって複数のブレークポイントを扱う場合は、Breakpoints タブですべてのブレークポイントを1か所にまとめて管理できます。

##### 個々のブレークポイントの操作 {#individual-breakpoint-controls}

  個々のブレークポイントに対して、次の操作ができます。
  - 赤いごみ箱アイコンをクリックすると、ブレークポイントを削除します
  - 行内の条件欄以外の場所をダブルクリックすると、Code View の該当行に移動します
  - 条件のセルをダブルクリックするか、ペンのアイコンをクリックすると、条件付きブレークポイントを編集できます
  - 条件のセルにポインターを合わせたときに表示される X ボタンをクリックすると、条件を消去します

##### 一括操作 {#batch-operations}

  Ctrl/Cmd+click または Shift+click で複数のブレークポイントを選択し、右クリックすると、一括操作を実行できます。複数のブレークポイントの条件を同時に編集したり、有効と無効を切り替えたり、完全に削除したりできます。

  ツールバーのボタンを使うと、すべてのブレークポイントを一度に有効化、無効化、または切り替えることができます。ブレークポイントの位置を残したまま、ゲームを停止させずに実行したいときに便利です。デバッグセッションが終わったら、すべて削除することもできます。

## Lua のデバッグライブラリ {#lua-debug-library}

Lua にはデバッグライブラリが付属しており、特に Lua 環境の内部を調べる必要がある場合などに役立ちます。詳しくは、[Lua マニュアルのデバッグライブラリの章](http://www.lua.org/pil/contents.html#23)を参照してください。

## デバッグのチェックリスト {#debugging-checklist}

エラーが発生した場合や、ゲームが期待どおりに動作しない場合は、次のデバッグのチェックリストを確認してください。

1. コンソール出力を確認し、実行時エラーがないことを確かめます。

2. コードに `print` 文を追加し、コードが実際に実行されていることを確かめます。

3. コードが実行されていない場合は、実行に必要な設定をエディターで正しく行ったか確認します。スクリプトは正しいゲームオブジェクトに追加されていますか？スクリプトは入力フォーカス（input focus）を取得していますか？入力トリガー（input trigger）は正しいですか？シェーダーのコードはマテリアルに追加されていますか？これらの点などを確認します。

4. コードが変数の値に依存している場合（たとえば if 文内）は、その値を使用または確認する場所で `print` するか、デバッガーで調べます。

不具合の発見は難しく、時間がかかることがあります。コードを少しずつたどり、すべてを確認しながら問題のあるコードを絞り込み、エラーの原因となる箇所を除いていく必要があります。この作業には「分割統治」と呼ばれる方法が適しています。

1. コードのどちらの半分（またはそれより狭い範囲）に不具合が含まれているはずかを特定します。
2. その半分のさらにどちらの半分に、不具合が含まれているはずかを特定します。
3. 不具合が見つかるまで、その原因となるはずのコードの範囲を絞り込み続けます。

不具合探しがうまくいきますように！

## 物理の問題のデバッグ {#debugging-problems-with-physics}

物理に問題があり、衝突が期待どおりに動作しない場合は、物理のデバッグを有効にすることをお勧めします。*game.project* ファイルの *Physics* セクションにある *Debug* チェックボックスをオンにします。

![物理のデバッグ設定](images/debugging/physics_debug_setting.png)

このチェックボックスを有効にすると、Defold はすべてのコリジョン形状（collision shape）と衝突の接触点を描画します。

![物理のデバッグ表示](images/debugging/physics_debug_visualisation.png)
