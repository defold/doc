---
title: Фізичні з’єднання в Defold
brief: Defold підтримує з’єднання для 2D-фізики. У цьому посібнику пояснено, як створювати з’єднання та працювати з ними.
---

# З’єднання {#joints}

Defold підтримує з’єднання (joints) для 2D-фізики. З’єднання сполучає два об’єкти колізій (collision objects) за допомогою певного обмеження. Підтримуються такі типи з’єднань:

* **Фіксоване (physics.JOINT_TYPE_FIXED)** — Мотузкове з’єднання, яке обмежує максимальну відстань між двома точками. У Box2D його називають мотузковим з’єднанням (Rope joint).
* **Шарнірне (physics.JOINT_TYPE_HINGE)** — Шарнірне з’єднання задає точку кріплення на двох об’єктах колізій і переміщує їх так, щоб обидва об’єкти колізій завжди перебували в одному місці, не обмежуючи їхнього відносного обертання. Для шарнірного з’єднання можна ввімкнути двигун із заданими максимальним крутним моментом і швидкістю. У Box2D його називають [обертовим з’єднанням (Revolute joint)](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Зварне (physics.JOINT_TYPE_WELD)** — Зварне з’єднання намагається обмежити будь-який відносний рух між двома об’єктами колізій. Зварне з’єднання можна зробити м’яким, як пружина, задавши частоту та коефіцієнт демпфування. У Box2D його називають [зварним з’єднанням (Weld joint)](https://box2d.org/documentation/group__weld__joint.html#details).
* **Пружинне (physics.JOINT_TYPE_SPRING)** — Пружинне з’єднання утримує два об’єкти колізій на постійній відстані один від одного. Пружинне з’єднання можна зробити м’яким, як пружина, задавши частоту та коефіцієнт демпфування. У Box2D його називають [дистанційним з’єднанням (Distance joint)](https://box2d.org/documentation/group__distance__joint.html#details).
* **Повзункове (physics.JOINT_TYPE_SLIDER)** — Повзункове з’єднання допускає відносне переміщення двох об’єктів колізій уздовж заданої осі та запобігає відносному обертанню. У Box2D його називають [призматичним з’єднанням (Prismatic joint)](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **Колісне (physics.JOINT_TYPE_WHEEL)** — Колісне з’єднання обмежує рух точки на `bodyB` лінією на `bodyA`. Колісне з’єднання також забезпечує пружину підвіски. У Box2D його називають [колісним з’єднанням (Wheel joint)](https://box2d.org/documentation/group__wheel__joint.html#details).

## Створення з’єднань {#creating-joints}

Наразі з’єднання можна створювати лише програмно за допомогою [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Підтримка створення з’єднань у редакторі запланована, але дату випуску ще не визначено.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Наведений вище код створить фіксоване з’єднання з ідентифікатором `my_test_joint` між двома об’єктами колізій `obj_a#collisionobject` і `obj_b#collisionobject`. З’єднання кріпиться на 10 пікселів ліворуч від центра об’єкта колізій `obj_a#collisionobject` і на 20 пікселів вище від центра об’єкта колізій `obj_b#collisionobject`. Максимальна довжина з’єднання становить 20 пікселів.

## Знищення з’єднань {#destroying-joints}

З’єднання можна знищити за допомогою [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Читання й оновлення з’єднань {#reading-from-and-updating-joints}

Властивості з’єднання можна прочитати за допомогою [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) і встановити за допомогою [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

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

## Отримання сили реакції та крутного моменту з’єднання {#get-joint-reaction-force-and-torque}

Силу реакції та крутний момент, прикладені до з’єднання, можна прочитати за допомогою [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) і [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
