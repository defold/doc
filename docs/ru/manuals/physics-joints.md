---
title: Физика сочленений
brief: Defold поддерживает сочленения (joints) для 2D-физики. Данное руководство объясняет как создавать и работать с сочленениями.
---

# Физика сочленений

Defold поддерживает сочленения для 2D-физики. Сочленение соединяет два объекта столкновения задействуя некоторые виды ограничителей. Поддерживаемые типы сочленений:

* **Fixed (physics.JOINT_TYPE_FIXED)** --- Сочленение-веревка, которое ограничивает максимальное расстояние между двумя точками. В Box2D оно также известно как Rope joint.
* **Hinge (physics.JOINT_TYPE_HINGE)** --- Шарнирное сочленение задает точку-якорь на два объекта столкновения и двигает их таким образом, что два объекта столкновения всегда зафиксированы в одном и том же месте, но относительное вращение объектов столкновения не ограничивается. Шарнирное сочленение позволяет сделать двигатель с максимальным заданным крутящим моментом двигателя и скоростью. В Box2D оно также известно как Revolute joint.
* **Weld (physics.JOINT_TYPE_WELD)** --- Сварное сочленение пытается ограничить любое относительное движение между двумя объектами столкновения. Сварное сочленение можно сделать мягким как пружина с частотой и коэффициентом амортизации. В Box2D оно также известно как Weld joint.
* **Spring (physics.JOINT_TYPE_SPRING)** --- Рессорное сочленение удерживает два объекта столкновения на постоянном расстоянии друг от друга. Рессорное сочленение можно сделать мягким как пружина с частотой и коэффициентом амортизации. В Box2D оно также известно как Distance joint.
* **Slider (physics.JOINT_TYPE_SLIDER)** --- Сочленение-слайдер позволяет относительный сдвиг двух объектов вдоль заданной оси, но блокирует относительное вращение. В Box2D оно также известно как Prismatic joint.
* **Wheel (physics.JOINT_TYPE_WHEEL)** --- Колёсное сочленение ограничивает точку на `bodyB` перемещением вдоль линии на `bodyA`. Также оно обеспечивает эффект пружинной подвески. В Box2D известно как [Wheel joint](https://box2d.org/documentation/group__wheel__joint.html#details).

## Создание сочленений

На данный момент сочленения могут быть созданы только программно вызовом [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Поддержка создания сочленений в редакторе есть в планах, но дата релиза пока не обговорена.
:::

```lua
-- соединить два объекта столкновения фиксированным ограничителем сочленения (веревка)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Код выше создаст фиксированное сочленение с идентификатором `my_test_joint` соединенным между `obj_a#collisionobject` и `obj_b#collisionobject`. Сочленение присоединено в 10 пикселях левее центра объекта столкновения `obj_a#collisionobject` и 20 пикселями выше центра объекта столкновения `obj_b#collisionobject`. Максимальная длина сочленения --- 20 пикселей.

## Уничтожение сочленений

Сочленение можно уничтожить вызовом [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- уничтожить сочленение, ранее присоединенное к первому объекту столкновения
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Считывание и обновление сочленений

Свойства сочленения могут быть считаны вызовом [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id), а установлены вызовом [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties)::

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- увеличить скорость двигателя на 100 оборотов в секунду
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Получение силы реакции сочленения и крутящего момента

Примененные к сочленению сила реакции и крутящий момент могут быть считаны вызовами [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) и [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
