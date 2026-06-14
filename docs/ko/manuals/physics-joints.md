---
title: Defold의 물리 조인트
brief: Defold는 2D 물리용 조인트를 지원합니다. 이 매뉴얼에서는 조인트를 만들고 사용하는 방법을 설명합니다.
---

# 조인트

Defold는 2D 물리용 조인트를 지원합니다. 조인트는 어떤 종류의 제약 조건을 사용해 두 충돌 오브젝트를 연결합니다. 지원되는 조인트 타입은 다음과 같습니다:

* **Fixed (physics.JOINT_TYPE_FIXED)** - 두 점 사이의 최대 거리를 제한하는 로프 조인트입니다. Box2D에서는 Rope joint라고 합니다.
* **Hinge (physics.JOINT_TYPE_HINGE)** - 힌지 조인트는 두 충돌 오브젝트의 앵커 포인트를 지정하고, 두 충돌 오브젝트의 앵커 포인트가 항상 같은 위치에 오도록 이동시키며, 충돌 오브젝트의 상대 회전은 제한하지 않습니다. 힌지 조인트는 정의된 최대 모터 토크와 속도를 가진 모터를 활성화할 수 있습니다. Box2D에서는 [Revolute joint](https://box2d.org/documentation/group__revolute__joint.html#details)라고 합니다.
* **Weld (physics.JOINT_TYPE_WELD)** - 용접 조인트는 두 충돌 오브젝트 사이의 모든 상대 이동을 제한하려고 시도합니다. 용접 조인트는 주파수와 감쇠비를 사용해 스프링처럼 부드럽게 만들 수 있습니다. Box2D에서는 [Weld joint](https://box2d.org/documentation/group__weld__joint.html#details)라고 합니다.
* **Spring (physics.JOINT_TYPE_SPRING)** - 스프링 조인트는 두 충돌 오브젝트가 서로 일정한 거리를 유지하게 합니다. 스프링 조인트는 주파수와 감쇠비를 사용해 스프링처럼 부드럽게 만들 수 있습니다. Box2D에서는 [Distance joint](https://box2d.org/documentation/group__distance__joint.html#details)라고 합니다.
* **Slider (physics.JOINT_TYPE_SLIDER)** - 슬라이더 조인트는 지정된 축을 따라 두 충돌 오브젝트가 상대적으로 병진 이동할 수 있게 하고 상대 회전은 방지합니다. Box2D에서는 [Prismatic joint](https://box2d.org/documentation/group__prismatic__joint.html#details)라고 합니다.
* **Wheel (physics.JOINT_TYPE_WHEEL)** - 휠 조인트는 `bodyB`의 한 점을 `bodyA`의 한 선에 제한합니다. 휠 조인트는 서스펜션 스프링도 제공합니다. Box2D에서는 [Wheel joint](https://box2d.org/documentation/group__wheel__joint.html#details)라고 합니다.

## 조인트 만들기

현재 조인트는 [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties])를 사용해 프로그래밍 방식으로만 만들 수 있습니다:
::: sidenote
에디터에서 조인트를 만드는 기능은 계획되어 있지만, 릴리스 날짜는 아직 정해지지 않았습니다.
:::

```lua
-- 두 충돌 오브젝트를 고정 조인트 제약 조건(로프)으로 연결합니다
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

위 코드는 두 충돌 오브젝트 `obj_a#collisionobject`와 `obj_b#collisionobject` 사이에 연결된 id `my_test_joint`의 고정 조인트를 만듭니다. 이 조인트는 충돌 오브젝트 `obj_a#collisionobject` 중심에서 왼쪽으로 10픽셀, 충돌 오브젝트 `obj_b#collisionobject` 중심에서 위로 20픽셀 떨어진 위치에 연결됩니다. 조인트의 최대 길이는 20픽셀입니다.

## 조인트 삭제하기

[`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id)를 사용해 조인트를 삭제할 수 있습니다:

```lua
-- 이전에 첫 번째 충돌 오브젝트에 연결된 조인트를 삭제합니다
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## 조인트 읽기 및 업데이트하기

조인트의 프로퍼티는 [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id)로 읽고 [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties)로 설정할 수 있습니다:

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- 모터 속도를 초당 100회전만큼 증가시킵니다
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## 조인트 반작용력과 토크 얻기

조인트에 적용되는 반작용력과 토크는 [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id)와 [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id)로 읽을 수 있습니다.
