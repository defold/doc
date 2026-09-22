---
title: Defold におけるキネマティックオブジェクトの衝突解決
brief: このマニュアルでは、キネマティックオブジェクトの物理的な衝突を解決する方法を説明します。
---

# キネマティックオブジェクトの衝突解決 {#resolving-kinematic-collisions}

キネマティックコリジョンオブジェクト（kinematic collision object）を使う場合は、自分で衝突を解決し、その応答としてオブジェクトを移動する必要があります。衝突している2つのオブジェクトを分離する単純な実装は、次のようになります。

```lua
function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    local newpos = go.get_position() + message.normal * message.distance
    go.set_position(newpos)
  end
end
```

このコードは、キネマティックオブジェクトを、めり込んでいる他の物理オブジェクトから分離します。ただし、分離のための移動量が過剰になることが多く、多くの場合に小刻みな揺れが見られます。この問題をよりよく理解するために、プレイヤーキャラクターが2つのオブジェクト *A* と *B* に衝突した次の例を考えてみます。

![物理的な衝突](images/physics/collision_multi.png)

物理エンジンは、衝突が発生したフレームに複数の `"contact_point_response"` メッセージを送信します。オブジェクト *A* について1つ、オブジェクト *B* について1つです。上記の単純なコードのように、それぞれのめり込みに応じてキャラクターを移動すると、次のように分離されます。

- めり込み距離（黒い矢印）に従って、キャラクターをオブジェクト *A* の外へ移動します。
- めり込み距離（黒い矢印）に従って、キャラクターをオブジェクト *B* の外へ移動します。

この順序は任意ですが、どちらの順序でも結果は同じです。分離のための移動量の合計は、*個々のめり込みベクトルの和* になります。

![単純な方法による物理オブジェクトの分離](images/physics/separation_naive.png)

キャラクターをオブジェクト *A* と *B* から適切に分離するには、各接触点（contact point）のめり込み距離を処理し、それ以前の分離によって、分離がすでに全体的または部分的に解決されていないかを確認する必要があります。

最初の接触点メッセージがオブジェクト *A* から届き、*A* のめり込みベクトルだけキャラクターを外へ移動したとします。

![物理オブジェクトの分離の手順1](images/physics/separation_step1.png)

この時点で、キャラクターは *B* からもすでに部分的に分離されています。オブジェクト *B* から完全に分離するために必要な最後の補償量を、上図の黒い矢印で示しています。補償ベクトルの長さは、*A* のめり込みベクトルを *B* のめり込みベクトルに射影することで計算できます。

![射影](images/physics/projection.png)

```
l = vmath.project(A, B) * vmath.length(B)
```

補償ベクトルは、*B* の長さを *l* だけ減らすことで求められます。任意の数のめり込みについてこれを計算するには、長さがゼロの補正ベクトルから始めて、接触点ごとに次の処理を行い、必要な補正量をベクトルに累積します。

1. 現在の補正ベクトルを、その接触点のめり込みベクトルに射影します。
2. めり込みベクトルから、残りの補償量を計算します（上記の式に従います）。
3. 補償ベクトルだけオブジェクトを移動します。
4. 補償量を累積された補正量に加えます。

完全な実装は次のようになります。

```lua
function init(self)
  -- correction vector
  self.correction = vmath.vector3()
end

function update(self, dt)
  -- reset correction
  self.correction = vmath.vector3()
end

function on_message(self, message_id, message, sender)
  -- Handle collision
  if message_id == hash("contact_point_response") then
    -- Get the info needed to move out of collision. We might
    -- get several contact points back and have to calculate
    -- how to move out of all of them by accumulating a
    -- correction vector for this frame:
    if message.distance > 0 then
      -- First, project the accumulated correction onto
      -- the penetration vector
      local proj = vmath.project(self.correction, message.normal * message.distance)
      if proj < 1 then
        -- Only care for projections that does not overshoot.
        local comp = (message.distance - message.distance * proj) * message.normal
        -- Apply compensation
        go.set_position(go.get_position() + comp)
        -- Accumulate correction done
        self.correction = self.correction + comp
      end
    end
  end
end
```
