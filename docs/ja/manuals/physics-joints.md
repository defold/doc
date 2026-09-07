---
title: Defold の物理ジョイント
brief: Defold は 2D 物理シミュレーションでジョイントをサポートしています。このマニュアルでは、ジョイントの作成方法と使い方を説明します。
---

# ジョイント {#joints}

Defold は 2D 物理シミュレーションでジョイント（joint）をサポートしています。ジョイントは、何らかの拘束（constraint）を使って2つのコリジョンオブジェクト（collision object）を接続します。サポートされているジョイントの種類は次のとおりです。

* **固定（Fixed） (physics.JOINT_TYPE_FIXED)** - 2点間の最大距離を制限するロープジョイントです。Box2D ではロープジョイント（Rope joint）と呼ばれます。
* **ヒンジ（Hinge） (physics.JOINT_TYPE_HINGE)** - ヒンジジョイントは、2つのコリジョンオブジェクト上にアンカーポイントを指定し、2つのコリジョンオブジェクトが常に同じ位置にあるように移動させます。コリジョンオブジェクト間の相対回転は制限されません。ヒンジジョイントでは、最大モータートルクと速度を定義したモーターを有効にできます。Box2D では[回転ジョイント（Revolute joint）](https://box2d.org/documentation/group__revolute__joint.html#details)と呼ばれます。
* **溶接（Weld） (physics.JOINT_TYPE_WELD)** - 溶接ジョイントは、2つのコリジョンオブジェクト間の相対的な動きをすべて拘束しようとします。周波数と減衰比を設定することで、溶接ジョイントをばねのように柔らかくできます。Box2D では[溶接ジョイント（Weld joint）](https://box2d.org/documentation/group__weld__joint.html#details)と呼ばれます。
* **スプリング（Spring） (physics.JOINT_TYPE_SPRING)** - スプリングジョイントは、2つのコリジョンオブジェクト間の距離を一定に保ちます。周波数と減衰比を設定することで、スプリングジョイントをばねのように柔らかくできます。Box2D では[距離ジョイント（Distance joint）](https://box2d.org/documentation/group__distance__joint.html#details)と呼ばれます。
* **スライダー（Slider） (physics.JOINT_TYPE_SLIDER)** - スライダージョイントは、指定した軸に沿った2つのコリジョンオブジェクトの相対的な平行移動を許可し、相対回転を防ぎます。Box2D では[直動ジョイント（Prismatic joint）](https://box2d.org/documentation/group__prismatic__joint.html#details)と呼ばれます。
* **ホイール（Wheel） (physics.JOINT_TYPE_WHEEL)** - ホイールジョイントは、`bodyB` 上の点を `bodyA` 上の直線に拘束します。ホイールジョイントにはサスペンション用のばねもあります。Box2D では[ホイールジョイント（Wheel joint）](https://box2d.org/documentation/group__wheel__joint.html#details)と呼ばれます。

## ジョイントの作成 {#creating-joints}

現在、ジョイントは [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) を使ってプログラムからのみ作成できます。
::: sidenote
エディターでのジョイント作成のサポートは予定されていますが、リリース日は決まっていません。
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

上記のコードは、2つのコリジョンオブジェクト `obj_a#collisionobject` と `obj_b#collisionobject` の間に、ID が `my_test_joint` の固定ジョイントを作成します。ジョイントは、コリジョンオブジェクト `obj_a#collisionobject` の中心から左に10ピクセルの位置と、コリジョンオブジェクト `obj_b#collisionobject` の中心から上に20ピクセルの位置に接続されます。ジョイントの最大長は20ピクセルです。

## ジョイントの破棄 {#destroying-joints}

ジョイントは [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) を使って破棄できます。

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## ジョイントの読み取りと更新 {#reading-from-and-updating-joints}

ジョイントのプロパティは、[`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) を使って読み取り、[`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) を使って設定できます。

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- increase motor speed by 100 revolutions per second
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## ジョイントの反力とトルクの取得 {#get-joint-reaction-force-and-torque}

ジョイントに加わる反力とトルクは、[`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) と [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id) を使って読み取れます。
