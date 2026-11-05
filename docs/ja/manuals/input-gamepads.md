---
title: Defold のゲームパッド入力
brief: このマニュアルでは、ゲームパッド入力の仕組みを説明します。
---

::: sidenote
Defold で入力が動作する基本的な仕組み、入力の受信方法、スクリプトファイルで入力を受信する順序を理解しておくことをお勧めします。入力システムについて詳しくは、[入力の概要マニュアル](/manuals/input)をご覧ください。
:::

# ゲームパッド {#gamepads}
ゲームパッドトリガー（gamepad trigger）を使うと、標準的なゲームパッド入力をゲームの機能に割り当てられます。ゲームパッド入力では、次の入力バインディング（input binding）を利用できます。

- 左右のスティック（方向とクリック）
- 左右のデジタルパッド。右側のパッドは通常、Xbox コントローラーの「A」「B」「X」「Y」ボタン、および Playstation コントローラーの「四角」「丸」「三角」「バツ」ボタンに対応します。
- 左右のトリガー
- 左右のショルダーボタン
- Start、Back、Guide ボタン

![](images/input/gamepad_bindings.png)

::: important
以下の例では、上の画像に示すアクションを使います。ほかのすべての入力と同様に、入力アクション（input action）には任意の名前を付けられます。
:::

## デジタルボタン {#digital-buttons}
デジタルボタンは、`pressed`、`released`、`repeated` イベントを生成します。次の例は、デジタルボタンの入力（押された、または離された）を検出する方法を示しています。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lpad_left") then
        if action.pressed then
            -- start moving left
        elseif action.released then
            -- stop moving left
        end
    end
end
```

## アナログスティック {#analog-sticks}
アナログスティックは、ゲームパッド設定ファイル（後述）で定義されたデッドゾーンの外側へ動かすと、入力イベントを連続して生成します。次の例は、アナログスティックの入力を検出する方法を示しています。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") then
        -- left stick was moved down
        print(action.value) -- a value between 0.0 an -1.0
    end
end
```

アナログスティックは、上下左右のいずれかの方向へ一定のしきい値を超えて動かすと、`pressed` イベントと `released` イベントも生成します。これにより、アナログスティックをデジタル方向入力としても簡単に使えます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_lstick_down") and action.pressed then
        -- left stick was moved to its extreme down position
    end
end
```

## 複数のゲームパッド {#multiple-gamepads}
Defold は、ホストのオペレーティングシステムを通じて複数のゲームパッドをサポートします。アクションでは、`action` テーブルの `gamepad` フィールドに、入力元のゲームパッド番号が設定されます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_start") then
        if action.gamepad == 0 then
          -- gamepad 0 wants to join the game
        end
    end
end
```

## 接続と切断 {#connect-and-disconnect}
ゲームパッドの入力バインディングには、`Connected` と `Disconnected` という2つの個別のバインディングもあり、ゲームパッドの接続（最初から接続されているものも含む）と切断を検出できます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("gamepad_connected") then
        if action.gamepad == 0 then
          -- gamepad 0 was connected
        end
    elseif action_id == hash("gamepad_disconnected") then
        if action.gamepad == 0 then
          -- gamepad 0 was disconnected
        end
    end
end
```

## ゲームパッドの生入力 {#raw-gamepads}

ゲームパッドの入力バインディングには、`Raw` という個別のバインディングもあります。これにより、接続された任意のゲームパッドから、フィルターを適用していない（デッドゾーンを適用していない）ボタン、軸、ハット（hat）の入力を取得できます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("raw") then
        pprint(action.gamepad_buttons)
        pprint(action.gamepad_axis)
        pprint(action.gamepad_hats)
    end
end
```

## ゲームパッド設定ファイル {#gamepads-settings-file}

ゲームパッドのマッピングは、コントローラーのボタン、軸、ハットを、入力バインディングが使う標準的な操作に変換します。Defold は、*game.project* の *Input* セクションで設定する2つのマッピングソースを組み合わせます。

| 設定 | マッピング形式 | デフォルト |
| --- | --- | --- |
| [Gamepad Database](/manuals/project-settings/#gamepad-database) | コントローラーの GUID で照合する SDL 形式のテキストデータベース | `/builtins/input/gamecontrollerdb.txt` |
| [Gamepads](/manuals/project-settings/#gamepads) | デバイス名とプラットフォームに対応する従来の `.gamepads` エントリー | `/builtins/input/default.gamepads` |

SDL データベースのマッピングとプラットフォームの自動マッピングは、[Gamepad Deadzone](/manuals/project-settings/#gamepad-deadzone) を使います。従来の `.gamepads` エントリーは独自のデッドゾーンを定義します。Android では、データベースにエントリーがないコントローラーにも、[自動マッピング](#gamepads-on-android)を適用する場合があります。

### 従来の .gamepads マッピング {#legacy-gamepads-mappings}

`.gamepads` ファイルには、複数のコントローラーのマッピングを含められます。既存の従来形式のマッピングも引き続きサポートします。Defold のデフォルトファイルには、一般的なコントローラーのマッピングが含まれます。

![ゲームパッドの設定](images/input/gamepads.png)

デスクトップで従来形式の `.gamepads` マッピングを作成するには、次のツールを利用できます。Android については、[Android のゲームパッド](#gamepads-on-android)を参照してください。

[クリックして gdc.zip をダウンロード](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032)。

Windows、Linux、macOS 用のバイナリが含まれています。コマンドラインから実行します。

```sh
./gdc
```

このツールは、接続されているコントローラーのさまざまなボタンを押すように指示します。その後、コントローラーに適したマッピングを含む新しい gamepads ファイルを出力します。新しいファイルを保存するか、既存の gamepads ファイルに統合してから、*game.project* の設定を更新します。

![ゲームパッドの設定](images/input/gamepad_setting.png)

### 識別されないゲームパッド {#unidentified-gamepads}

設定されたマッピングもプラットフォームの自動マッピングも利用できない場合、ゲームパッドが生成するのは `Connected`、`Disconnected`、`Raw` に割り当てたアクションだけです。コントローラーのマッピングを追加するか、ゲーム内で生の入力を処理できます。

ゲームパッドの入力アクションが未知のゲームパッドからのものかどうかは、`action` の `gamepad_unknown` 値を読み取ることで確認できます。

```lua
function on_input(self, action_id, action)
    if action_id == hash("connected") then
        if action.gamepad_unknown then
            print("The connected gamepad is unidentified and will only generate raw input")
        else
            print("The connected gamepad is known and will generate input actions for buttons and sticks")
        end
    end
end
```

## HTML5 のゲームパッド {#gamepads-in-html5}
ゲームパッドは HTML5 ビルドでサポートされ、ほかのプラットフォームと同じ入力イベントを生成します。ゲームパッドのサポートは、ほとんどのブラウザーがサポートする [Gamepad API](https://www.w3.org/TR/gamepad/) に基づいています（[対応状況の表を参照](https://caniuse.com/?search=gamepad)）。ブラウザーが Gamepad API をサポートしていない場合、Defold はプロジェクト内のすべてのゲームパッドトリガーを通知せずに無視します。ブラウザーが Gamepad API をサポートしているかどうかは、`navigator` オブジェクトに `getGamepads` 関数が存在するかを調べることで確認できます。

```lua
local function supports_gamepads()
    return not html5 or (html5.run('typeof navigator.getGamepads === "function"') == "true")
end

if supports_gamepads() then
    print("Platform supports gamepads")
end
```

ゲームが `iframe` 内で実行される場合は、その `iframe` に `gamepad` 権限が追加されていることも確認する必要があります。

```html
<iframe allow="gamepad"></iframe>
```

### 標準ゲームパッド {#standard-gamepad}

接続されたゲームパッドがブラウザーによって標準ゲームパッドとして識別された場合、[ゲームパッド設定ファイル](/manuals/input-gamepads/#gamepads-settings-file)の `Standard Gamepad` のマッピングを使います（`Standard Gamepad` のマッピングは、`/builtins` 内の `default.gamepads` ファイルに含まれています）。標準ゲームパッドは、16個のボタンと2本のアナログスティックを備え、PlayStation または Xbox コントローラーに似たボタン配置を持つものと定義されています（詳しくは、[W3C の定義とボタン配置](https://w3c.github.io/gamepad/#dfn-standard-gamepad)をご覧ください）。接続されたゲームパッドが標準ゲームパッドとして識別されない場合、Defold はゲームパッド設定ファイルから、そのゲームパッドの機種に一致するマッピングを探します。

## Windows のゲームパッド {#gamepads-on-windows}
Windows では、現在 XBox 360 コントローラーのみがサポートされています。360 コントローラーを Windows マシンに接続するには、[正しく設定されていることを確認してください](http://www.wikihow.com/Use-Your-Xbox-360-Controller-for-Windows)。

## Android のゲームパッド {#gamepads-on-android}

Android ビルドはゲームパッドに対応し、ほかのプラットフォームと同じ入力アクションを生成します。Defold は、設定された[ゲームパッドのマッピング](#gamepads-settings-file)を使い、一致するエントリーがない一部のコントローラーを自動的にマッピングできます。

コントローラーが識別されない、または操作が正しくない場合は、Android デバイスでテストし、マッピングを追加または更新してください。トラブルシューティングは、[未識別のゲームパッド](#unidentified-gamepads)と[生のゲームパッド入力](#raw-gamepads)を参照してください。
