---
title: Defold の衝突メッセージ
brief: 2つのオブジェクトが衝突すると、エンジンはイベントコールバックを呼び出すか、メッセージをブロードキャストします。
---

# 衝突メッセージ {#collision-messages}

2つのオブジェクトが衝突すると、エンジンはイベントコールバックにイベントを送信するか、両方のオブジェクトにメッセージをブロードキャストします。

## イベントのフィルタリング {#event-filtering}

生成するイベントの種類は、各オブジェクトのフラグで制御できます。

* "Generate Collision Events"
* "Generate Contact Events"
* "Generate Trigger Events"

これらはすべて既定で `true` です。
2つのコリジョンオブジェクト（collision object）が相互作用するとき、これらのチェックボックスに基づいて、ユーザーにメッセージを送信するかどうかを判定します。

たとえば、"Generate Contact Events" チェックボックスの場合は次のようになります。

`physics.set_event_listener()` を使用する場合:

| コンポーネント（component） A | コンポーネント B | メッセージの送信 |
|-------------|-------------|--------------|
| ✅︎          | ✅︎          | はい          |
| ❌          | ✅︎          | はい          |
| ✅︎          | ❌          | はい          |
| ❌          | ❌          | いいえ           |

既定のメッセージハンドラーを使用する場合:

| コンポーネント A | コンポーネント B | メッセージの送信（複数の場合あり）   |
|-------------|-------------|-------------------|
| ✅︎          | ✅︎          | はい (A,B) + (B,A) |
| ❌          | ✅︎          | はい (B,A)         |
| ✅︎          | ❌          | はい (A,B)         |
| ❌          | ❌          | いいえ                |

## 衝突への応答 {#collision-response}

`"collision_response"` メッセージは、衝突するオブジェクトの一方の種類が "dynamic"、"kinematic"、または "static" のときに送信されます。次のフィールドが設定されます。

`other_id`
: コリジョンオブジェクトが衝突した相手のインスタンスの ID（`hash`）

`other_position`
: コリジョンオブジェクトが衝突した相手のインスタンスのワールド位置（`vector3`）

`other_group`
: 相手のコリジョンオブジェクトのコリジョングループ（collision group）（`hash`）

`own_group`
: このコリジョンオブジェクトのコリジョングループ（`hash`）

`collision_response` メッセージは、オブジェクトが実際に交差している部分の詳細を必要としない衝突の処理にのみ適しています。たとえば、弾丸が敵に当たったかどうかを検出する場合です。衝突するオブジェクトの各ペアについて、このメッセージは1フレームにつき1つだけ送信されます。

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("collision_response") then
        -- take action
        print("I collided with", message.other_id)
    end
end
```

## 接触点への応答 {#contact-point-response}

`"contact_point_response"` メッセージは、衝突するオブジェクトの一方の種類が "dynamic" または "kinematic" で、もう一方の種類が "dynamic"、"kinematic"、または "static" のときに送信されます。次のフィールドが設定されます。

`position`
: 接触点（contact point）のワールド位置（`vector3`）。

`normal`
: 接触点のワールド空間での法線です。相手のオブジェクトからこのオブジェクトに向かう方向を指します（`vector3`）。

`relative_velocity`
: 相手のオブジェクトから見た、このコリジョンオブジェクトの相対速度（`vector3`）。

`distance`
: オブジェクト間のめり込み距離です。0以上の値です（`number`）。

`applied_impulse`
: 接触によって生じた力積（`number`）。

`life_time`
: （ *現在は使用されていません！* ）接触の生存期間（`number`）。

`mass`
: このコリジョンオブジェクトの質量。単位は kg です（`number`）。

`other_mass`
: 相手のコリジョンオブジェクトの質量。単位は kg です（`number`）。

`other_id`
: このコリジョンオブジェクトが接触している相手のインスタンスの ID（`hash`）。

`other_position`
: 相手のコリジョンオブジェクトのワールド位置（`vector3`）。

`other_group`
: 相手のコリジョンオブジェクトのコリジョングループ（`hash`）。

`own_group`
: このコリジョンオブジェクトのコリジョングループ（`hash`）。

オブジェクトを完全に分離する必要があるゲームやアプリケーションでは、`"contact_point_response"` メッセージから必要な情報をすべて取得できます。ただし、衝突の状況によっては、衝突する1組のオブジェクトについて、1フレームで複数の `"contact_point_response"` メッセージを受信することがあります。詳しくは[衝突の解決](/manuals/physics-resolving-collisions)を参照してください。

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("contact_point_response") then
        -- take action
        if message.other_mass > 10 then
            print("I collided with something weighing more than 10 kilos!")
        end
    end
end
```

## トリガーへの応答 {#trigger-response}

`"trigger_response"` メッセージは、衝突するオブジェクトの一方の種類が "trigger" のときに送信されます。このメッセージは、衝突が最初に検出されたときに1回送信され、オブジェクトが衝突しなくなったときにもう1回送信されます。次のフィールドがあります。

`other_id`
: コリジョンオブジェクトが衝突した相手のインスタンスの ID（`hash`）。

`enter`
: トリガー（trigger）への進入であれば `true`、退出であれば `false` です（`boolean`）。

`other_group`
: 相手のコリジョンオブジェクトのコリジョングループ（`hash`）。

`own_group`
: このコリジョンオブジェクトのコリジョングループ（`hash`）。

```Lua
function on_message(self, message_id, message, sender)
    -- check for the message
    if message_id == hash("trigger_response") then
        if message.enter then
            -- take action for entry
            print("I am now inside", message.other_id)
        else
            -- take action for exit
            print("I am now outside", message.other_id)
        end
    end
end
```
