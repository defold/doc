---
title: Defold の衝突イベント
brief: 衝突イベントの処理は、`physics.set_event_listener()` を使って、衝突や相互作用に関するすべてのメッセージを指定した1つの関数に送ることで一元化できます。
---

# Defold の物理イベント処理 {#defold-physics-event-handling}

Defold では、`physics.set_event_listener()` 関数を使って物理イベント（physics event）の処理を一元化できます。この関数で独自のリスナーを設定すると、物理的な相互作用によるすべてのイベントを1か所で処理できるため、コードを整理し、効率を向上できます。

## 物理ワールドのリスナーの設定 {#setting-the-physics-world-listener}

Defold では、各コレクションプロキシ（collection proxy）がそれぞれ独立した物理ワールド（physics world）を作成します。そのため、複数のコレクションプロキシを使う場合は、それぞれに関連付けられた別々の物理ワールドを管理する必要があります。各ワールドで物理イベントを正しく処理するには、各コレクションプロキシのワールドに対して個別に物理ワールドのリスナーを設定する必要があります。

この仕組みでは、プロキシが表すコレクション（collection）のコンテキスト内から、物理イベントのリスナーを設定する必要があります。これにより、リスナーが対応する物理ワールドに直接関連付けられ、物理イベントを正確に処理できます。

コレクションプロキシ内で物理ワールドのリスナーを設定する例を次に示します。

```lua
function init(self)
    -- Assuming this script is attached to a game object within the collection loaded by the proxy
    -- Set the physics world listener for the physics world of this collection proxy
    physics.set_event_listener(physics_world_listener)
end
```

この方法を実装すると、コレクションプロキシが生成する各物理ワールドに専用のリスナーが設定されます。これは、複数のコレクションプロキシを使うプロジェクトで物理イベントを効果的に処理するために不可欠です。

::: important
リスナーを設定すると、そのリスナーを設定した物理ワールドでは[物理メッセージ](/manuals/physics-messages)が送信されなくなります。
:::

## イベントのデータ構造 {#event-data-structure}

リスナーは `self` と `events` テーブルを引数として呼び出されます。`events` テーブルは、コールバック用に収集されたすべての物理イベントを含む配列です。各要素はイベントテーブルで、ハッシュ化されたイベント名を格納する `type` フィールドと、そのイベントの種類に固有の追加フィールドを含みます。

イベントテーブルには、次のデータが含まれます。

1. **接触点イベント（`contact_point_event`）:**
このイベントは、2つのコリジョンオブジェクト（collision object）間の接触点を通知します。衝撃力の計算や、衝突に対する独自の応答処理など、詳細な衝突処理に役立ちます。

   - `applied_impulse`: 接触によって生じた力積。
   - `distance`: オブジェクト間のめり込み距離。
   - `a` と `b`: 衝突している実体を表すオブジェクトで、それぞれ次のフィールドを含みます。
     - `position`: 接触点のワールド座標（vector3）。
     - `instance_position`: ゲームオブジェクト（game object）のインスタンスのワールド座標（vector3）。
     - `id`: インスタンス ID（hash）。
     - `group`: コリジョングループ（hash）。
     - `relative_velocity`: 相手のオブジェクトに対する相対速度（vector3）。
     - `mass`: キログラム単位の質量（number）。
     - `normal`: 相手のオブジェクトからこちらに向かう接触法線（vector3）。

2. **衝突イベント（`collision_event`）:**
このイベントは、2つのオブジェクト間で衝突が発生したことを示します。接触点イベントと比べて、より概括的なイベントであり、接触点の詳細な情報を必要とせずに衝突を検出する場合に適しています。

   - `a` と `b`: 衝突している実体を表すオブジェクトで、それぞれ次のフィールドを含みます。
     - `position`: ワールド座標（vector3）。
     - `id`: インスタンス ID（hash）。
     - `group`: コリジョングループ（hash）。

3. **トリガーイベント（`trigger_event`）:** 
このイベントは、オブジェクトがトリガーオブジェクトと相互作用したときに送信されます。オブジェクトが入ったり出たりしたときに何かを発生させる領域をゲーム内に作成する際に役立ちます。

   - `enter`: 相互作用が進入（true）か退出（false）かを示します。
   - `a` と `b`: トリガーイベントに関わるオブジェクトで、それぞれ次のフィールドを含みます。
     - `id`: インスタンス ID（hash）。
     - `group`: コリジョングループ（hash）。

4. **レイキャスト応答（`ray_cast_response`）:**
このイベントはレイキャストへの応答として送信され、レイがヒットしたオブジェクトに関する情報を提供します。

   - `group`: ヒットしたオブジェクトのコリジョングループ（hash）。
   - `request_id`: レイキャストリクエストの識別子（number）。
   - `position`: ヒット位置（vector3）。
   - `fraction`: ヒット位置までの距離がレイの長さ全体に占める割合（number）。
   - `normal`: ヒット位置の法線（vector3）。
   - `id`: ヒットしたオブジェクトのインスタンス ID（hash）。

5. **レイキャスト未ヒット（`ray_cast_missed`）:**
このイベントは、レイキャストがどのオブジェクトにもヒットしなかったときに送信されます。

   - `request_id`: ヒットしなかったレイキャストリクエストの識別子（number）。

## 使用例 {#example-usage}

```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            -- Handle detailed contact point data
            pprint(event)
        elseif event.type == hash("collision_event") then
            -- Handle general collision data
            pprint(event)
        elseif event.type == hash("trigger_event") then
            -- Handle trigger interaction data
            pprint(event)
        elseif event.type == hash("ray_cast_response") then
            -- Handle raycast hit data
            pprint(event)
        elseif event.type == hash("ray_cast_missed") then
            -- Handle raycast miss data
            pprint(event)
        end
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```

## 制約 {#limitations}

リスナーはイベントが発生した時点で同期的に呼び出されます。この呼び出しはタイムステップの途中で行われるため、物理ワールドはロックされています。そのため、`physics.create_joint()` など、物理ワールドのシミュレーションに影響する可能性のある関数は使用できません。

これらの制約を回避する短い例を次に示します。
```lua
local function physics_world_listener(self, events)
    for _,event in ipairs(events) do
        if event.type == hash("contact_point_event") then
            local position_a = event.a.normal * SIZE
            local position_b =  event.b.normal * SIZE
            local url_a = msg.url(nil, event.a.id, "collisionobject")
            local url_b = msg.url(nil, event.b.id, "collisionobject")
            -- fill the message in the same way arguments should be passed to `physics.create_joint()`
            local message = {physics.JOINT_TYPE_FIXED, url_a, "joind_id", position_a, url_b, position_b, {max_length = SIZE}}
            -- send message to the object itself
            msg.post(".", "create_joint", message)
        end
    end
end

function on_message(self, message_id, message)
    if message_id == hash("create_joint") then
        -- unpack message with function arguments
        physics.create_joint(unpack(message))
    end
end

function init(self)
    physics.set_event_listener(physics_world_listener)
end
```
