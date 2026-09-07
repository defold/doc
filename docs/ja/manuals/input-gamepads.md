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
ゲームパッド入力の設定では、ゲームパッドの機種ごとに個別のマッピングファイルを使います。特定のゲームパッド機種用のマッピングは、*gamepads* ファイルで設定します。Defold には、一般的なゲームパッドの設定を収録した組み込みの gamepads ファイルが付属しています。

![ゲームパッドの設定](images/input/gamepads.png)

新しいゲームパッド設定ファイルを作成する必要がある場合に役立つ、簡単なツールを用意しています。

[クリックして gdc.zip をダウンロード](https://forum.defold.com/t/big-thread-of-gamepad-testing/56032)。

Windows、Linux、macOS 用のバイナリが含まれています。コマンドラインから実行します。

```sh
./gdc
```

このツールは、接続されているコントローラーのさまざまなボタンを押すように指示します。その後、コントローラーに適したマッピングを含む新しい gamepads ファイルを出力します。新しいファイルを保存するか、既存の gamepads ファイルに統合してから、*game.project* の設定を更新します。

![ゲームパッドの設定](images/input/gamepad_setting.png)

### 識別されないゲームパッド {#unidentified-gamepads}

ゲームパッドを接続したときに、そのゲームパッド用のマッピングが存在しない場合、そのゲームパッドは `connected`、`disconnected`、`raw` アクションのみを生成します。この場合は、ゲームパッドの生データをゲーム内のアクションへ手動でマッピングする必要があります。

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

ゲームパッドは Android ビルドでサポートされ、ほかのプラットフォームと同じ入力イベントを生成します。ゲームパッドのサポートは、[キーイベントとモーションイベントを扱う Android の入力システム](https://developer.android.com/training/game-controllers/controller-input)に基づいています。Android の入力イベントは、前述したものと同じ *gamepad* ファイルを使って、Defold のゲームパッドイベントに変換されます。

Android でゲームパッドのバインディングを追加するときは、次の対応表を使って Android の入力イベントを *gamepad* ファイルの値に変換できます。

| キーイベントからボタンインデックスへの対応   | インデックス |
|-----------------------------|-------|
| `AKEYCODE_BUTTON_A`           | 0     |
| `AKEYCODE_BUTTON_B`           | 1     |
| `AKEYCODE_BUTTON_C`           | 2     |
| `AKEYCODE_BUTTON_X`           | 3     |
| `AKEYCODE_BUTTON_L1`          | 4     |
| `AKEYCODE_BUTTON_R1`          | 5     |
| `AKEYCODE_BUTTON_Y`           | 6     |
| `AKEYCODE_BUTTON_Z`           | 7     |
| `AKEYCODE_BUTTON_L2`          | 8     |
| `AKEYCODE_BUTTON_R2`          | 9     |
| `AKEYCODE_DPAD_CENTER`        | 10    |
| `AKEYCODE_DPAD_DOWN`          | 11    |
| `AKEYCODE_DPAD_LEFT`          | 12    |
| `AKEYCODE_DPAD_RIGHT`         | 13    |
| `AKEYCODE_DPAD_UP`            | 14    |
| `AKEYCODE_BUTTON_START`       | 15    |
| `AKEYCODE_BUTTON_SELECT`      | 16    |
| `AKEYCODE_BUTTON_THUMBL`      | 17    |
| `AKEYCODE_BUTTON_THUMBR`      | 18    |
| `AKEYCODE_BUTTON_MODE`        | 19    |
| `AKEYCODE_BUTTON_1`           | 20    |
| `AKEYCODE_BUTTON_2`           | 21    |
| `AKEYCODE_BUTTON_3`           | 22    |
| `AKEYCODE_BUTTON_4`           | 23    |
| `AKEYCODE_BUTTON_5`           | 24    |
| `AKEYCODE_BUTTON_6`           | 25    |
| `AKEYCODE_BUTTON_7`           | 26    |
| `AKEYCODE_BUTTON_8`           | 27    |
| `AKEYCODE_BUTTON_9`           | 28    |
| `AKEYCODE_BUTTON_10`          | 29    |
| `AKEYCODE_BUTTON_11`          | 30    |
| `AKEYCODE_BUTTON_12`          | 31    |
| `AKEYCODE_BUTTON_13`          | 32    |
| `AKEYCODE_BUTTON_14`          | 33    |
| `AKEYCODE_BUTTON_15`          | 34    |
| `AKEYCODE_BUTTON_16`          | 35    |

（[Android の `KeyEvent` の定義](https://developer.android.com/ndk/reference/group/input#group___input_1gafccd240f973cf154952fb917c9209719)）

| モーションイベントから軸インデックスへの対応  | インデックス |
|-----------------------------|-------|
| `AMOTION_EVENT_AXIS_X`        | 0     |
| `AMOTION_EVENT_AXIS_Y`        | 1     |
| `AMOTION_EVENT_AXIS_Z`        | 2     |
| `AMOTION_EVENT_AXIS_RZ`       | 3     |
| `AMOTION_EVENT_AXIS_LTRIGGER` | 4     |
| `AMOTION_EVENT_AXIS_RTRIGGER` | 5     |
| `AMOTION_EVENT_AXIS_HAT_X`    | 6     |
| `AMOTION_EVENT_AXIS_HAT_Y`    | 7     |

（[Android の `MotionEvent` の定義](https://developer.android.com/ndk/reference/group/input#group___input_1ga157d5577a5b2f5986037d0d09c7dc77d)）

この対応表を Google Play Store のゲームパッドテストアプリと組み合わせて使い、ゲームパッドの各ボタンがどのキーイベントにマッピングされているかを調べます。
