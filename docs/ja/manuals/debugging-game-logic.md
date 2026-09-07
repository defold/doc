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

デバッガーを実行するには、<kbd>Debug ▸ Start/Attach</kbd> を選択します。デバッガーが接続された状態でゲームが起動するか、すでに実行中のゲームにデバッガーが接続されます。

![概要](images/debugging/overview.png)

デバッガーが接続されると、コンソールのデバッガー操作ボタン、または <kbd>Debug</kbd> メニューからゲームの実行を制御できます。

Break
: ![一時停止](images/debugging/pause.svg){width=60px .left}
  ゲームの実行を直ちに中断します。ゲームは現在の実行位置で中断します。その状態でゲームの状態を調べたり、1ステップずつ進めたり、次のブレークポイントまで実行を続けたりできます。現在の実行位置はコードエディターにマークで示されます。

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
Lua コードの1行は、1つの式に対応するわけではありません。デバッガーでのステップ実行は1回に1つの式ずつ進むため、現在の実装では、次の行に進むためにステップボタンを複数回押す必要がある場合があります。
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
: デバッガーが接続され、ゲームがブレークポイントで停止しているときは、現在のコンテキストで Lua ランタイムを利用できます。コンソールの下部に Lua 式を入力し、<kbd>Enter</kbd> を押すと評価できます。

  ![コンソール](images/debugging/console.png)

  現在、この評価機能を通して変数を変更することはできません。

デバッガーの切り離し
: <kbd>Debug ▸ Detach Debugger</kbd> を選択すると、ゲームからデバッガーが切り離されます。ゲームの実行は直ちに再開します。

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
