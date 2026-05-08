---
title: Łączenia fizyczne w Defold
brief: Defold obsługuje łączenia dla fizyki 2D. Ta instrukcja wyjaśnia, jak je tworzyć i jak z nimi pracować.
---

# Łączenia

Defold obsługuje łączenia w fizyce 2D. Łączenie łączy dwa obiekty kolizji za pomocą określonego ograniczenia. Obsługiwane typy łączeń to:

* **Fixed (physics.JOINT_TYPE_FIXED)** - Łączenie linowe ograniczające maksymalną odległość między dwoma punktami. W Box2D nazywa się Rope joint.
* **Hinge (physics.JOINT_TYPE_HINGE)** - Łączenie zawiasowe określa punkt zakotwiczenia na dwóch obiektach kolizji i przesuwa je tak, aby oba obiekty zawsze znajdowały się w tym samym miejscu, przy czym ich względny obrót nie jest ograniczony. Łączenie zawiasowe może włączyć motor o określonym maksymalnym momencie obrotowym i prędkości. W Box2D odpowiada [Revolute joint](https://box2d.org/documentation/group__revolute__joint.html#details).
* **Weld (physics.JOINT_TYPE_WELD)** - Łączenie spawane próbuje ograniczyć cały względny ruch między dwoma obiektami kolizji. Może być zmiękczone jak sprężyna dzięki częstotliwości i współczynnikowi tłumienia. W Box2D odpowiada [Weld joint](https://box2d.org/documentation/group__weld__joint.html#details).
* **Spring (physics.JOINT_TYPE_SPRING)** - Łączenie sprężynowe utrzymuje dwa obiekty kolizji w stałej odległości od siebie. Także może być zmiękczone jak sprężyna dzięki częstotliwości i współczynnikowi tłumienia. W Box2D odpowiada [Distance joint](https://box2d.org/documentation/group__distance__joint.html#details).
* **Slider (physics.JOINT_TYPE_SLIDER)** - Łączenie przesuwne pozwala na względne przesunięcie dwóch obiektów kolizji wzdłuż wskazanej osi i zapobiega ich względnemu obrotowi. W Box2D odpowiada [Prismatic joint](https://box2d.org/documentation/group__prismatic__joint.html#details).
* **Wheel (physics.JOINT_TYPE_WHEEL)** - Łączenie koła ogranicza punkt na `bodyB` do linii na `bodyA`. Zapewnia też sprężynę zawieszenia. W Box2D odpowiada [Wheel joint](https://box2d.org/documentation/group__wheel__joint.html#details).

## Tworzenie łączeń

Łączenia można obecnie tworzyć tylko programowo za pomocą [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Obsługa tworzenia łączeń w edytorze jest planowana, ale nie ustalono jeszcze daty wydania.
:::

```lua
-- połącz dwa obiekty kolizji za pomocą stałego ograniczenia łączenia (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Powyższy przykład tworzy łączenie typu Fixed o id `my_test_joint` pomiędzy obiektami kolizji `obj_a#collisionobject` i `obj_b#collisionobject`. Łączenie jest umieszczone 10 pikseli na lewo od środka `obj_a#collisionobject` i 20 pikseli nad środkiem `obj_b#collisionobject`. Maksymalna długość łączenia wynosi 20 pikseli.

## Niszczenie łączeń

Łączenie można zniszczyć za pomocą [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- zniszcz łączenie wcześniej podłączone do pierwszego obiektu kolizji
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Odczyt i aktualizacja łączeń

Właściwości łączenia można odczytać przez [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id), a ustawić przez [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- zwiększ prędkość motoru o 100 obrotów na sekundę
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```

## Odczyt siły i momentu reakcji łączenia

Siłę reakcji i moment reakcji działające na łączenie można odczytać funkcjami [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) oraz [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
