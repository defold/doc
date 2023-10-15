---
title: Łączenia fizyczne w Defoldzie
brief: Defold supports joints for 2D physics. This manual explains how to create and work with joints.
---

# Łączenia fizyczne (Joints)

Defold obsługuje łączenia (ang. joints) w fizyce 2D. Łączenie łączy ze sobą dwa obiekty kolizji za pomocą wybranego rodzaju ograniczenia. Obsługiwane rodzaje połączeń to:

* **Fixed (physics.JOINT_TYPE_FIXED)** - łączenie stałe, które ogranicza maksymalną odległość między dwoma punktami. W Box2D jest to znane jako połączenie "lina" (ang. rope joint).
* **Hinge (physics.JOINT_TYPE_HINGE)** - łączenie zawiasowe/osi określa punkt kotwiczenia na dwóch obiektach kolizji i przesuwa je tak, aby obiekty były zawsze w tym samym miejscu, a względna rotacja obiektów kolizyjnych nie była ograniczona. Łączenie zawiasowe można łączyć ze specjalnym silnikiem (ang. motor) zdefiniowanym z maksymalnym momentem obrotowym i prędkością, co umożliwia przykładowo stworzenie koła pojazdu. W Box2D jest to znane jako połączenie obrotowe (ang. revolute joint).
* **Weld (physics.JOINT_TYPE_WELD)** - łączenie spawane stara się ograniczyć wszelkie względne ruchy między dwoma obiektami kolizyji. Łączenie spawane można zrobić miękkie jak sprężyna z częstotliwością i współczynnikiem tłumienia. W Box2D jest to znane również jako połączenie spawane (ang. weld joint).
* **Spring (physics.JOINT_TYPE_SPRING)** - łączenie sprężynowe utrzymuje dwa obiekty kolizyjne w stałej odległości od siebie. Połączenie sprężyny można zrobić miękkie jak sprężyna z częstotliwością i współczynnikiem tłumienia. W Box2D jest znane jako połączenie dystansowe (ang. distance joint).
* **Slider (physics.JOINT_TYPE_SLIDER)** - łączenie przesuwne/suwaka umożliwia względną translację dwóch obiektów kolizji wzdłuż określonej osi i zapobiega względnej rotacji. W Box2D jest znane jako połączenie pryzmatyczne (ang. prismatic joint).

## Tworzenie połączeń

Obecnie połączenia można tworzyć tylko programowo za pomocą funkcji [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]):
::: sidenote
Wsparcie Edytora do tworzenia połączeń jest planowane, ale nie ustalono jeszcze daty wydania.
:::

```lua
-- połącz dwa obiekty kolizyjne za pomocą połączenia liny (fixed joint)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Powyższy kod utworzy stałe połączenie o identyfikatorze `my_test_joint`, połączone między dwoma obiektami kolizyjnymi `obj_a#collisionobject` i `obj_b#collisionobject`. Połączenie jest ustanowione 10 pikseli na lewo od środka obiektu kolizyjnego `obj_a#collisionobject` i 20 pikseli nad środkiem obiektu kolizyjnego `obj_b#collisionobject`. Maksymalna długość połączenia wynosi 20 pikseli.

## Niszczenie połączeń

Połączenie można zniszczyć za pomocą funkcji [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id):

```lua
-- zniszcz połączenie, które było wcześniej podłączone do pierwszego obiektu kolizyjnego
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Odczytywanie i aktualizowanie połączeń

Właściwości połączenia można odczytać za pomocą funkcji [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) i ustawić za pomocą funkcji [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties):

```lua
function update(self, dt)
    if self.accelerating then
        local hinge_props = physics.get_joint_properties("obj_a#collisionobject", "my_hinge")
        -- zwiększ prędkość silnika o 100 obrotów na sekundę
        hinge_props.motor_speed = hinge_props.motor_speed + 100 * 2 * math.pi * dt
        physics.set_joint_properties("obj_a#collisionobject", "my_hinge", hinge_props)
    end
end
```
## Odczytywanie siły i momentu reakcji połączenia

Siłę reakcji i moment reakcji, które zostały zastosowane do połączenia, można odczytać za pomocą funkcji odpowiednio [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) i [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id).
