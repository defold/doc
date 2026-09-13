---
title: Defold'da fizik eklemleri
brief: Defold, 2B fizik için eklemleri destekler. Bu kılavuz, eklemlerin nasıl oluşturulacağını ve kullanılacağını açıklar.
---

# Eklemler

Eklem (joint), bir kısıt (constraint) kullanarak iki çarpışma nesnesini (collision object) birbirine bağlar. Defold, farklı API'ler aracılığıyla hem 2B hem de 3B fizikte eklemleri destekler.

Bu kılavuz, `physics` modülünün sunduğu 2B eklemleri açıklar. Defold 1.13.2 sürümünden itibaren 3B projeler, [`bullet3d.constraint`](/ref/beta/bullet3d.constraint/) aracılığıyla menteşeler, kayar eklemler ve yaylar dahil çeşitli kısıtlar oluşturabilir ve bunları kontrol edebilir. Bu API'yi, [`bullet3d.get_rigid_body()`](/ref/beta/bullet3d/#bullet3d.get_rigid_body) aracılığıyla elde edilen katı cisimlerle (rigid body) kullanın.

2B `physics` API'sinde desteklenen eklem türleri şunlardır:

* **Sabit (physics.JOINT_TYPE_FIXED)** - İki nokta arasındaki en büyük mesafeyi sınırlayan bir halat eklemidir (rope joint). Box2D'de halat eklemi (Rope joint) olarak adlandırılır.
* **Menteşe (physics.JOINT_TYPE_HINGE)** - Menteşe eklemi (hinge joint), iki çarpışma nesnesi üzerinde bir bağlantı noktası belirler ve iki çarpışma nesnesi her zaman aynı yerde olacak şekilde onları hareket ettirir; çarpışma nesnelerinin birbirine göre dönmesi kısıtlanmaz. Menteşe eklemi, en yüksek torku ve sürati tanımlanmış bir motoru etkinleştirebilir. Box2D'de [döner eklem (Revolute joint)](https://box2d.org/documentation/group__revolute__joint.html#details) olarak adlandırılır.
* **Kaynak (physics.JOINT_TYPE_WELD)** - Kaynak eklemi (weld joint), iki çarpışma nesnesi arasındaki tüm göreli hareketi kısıtlamaya çalışır. Kaynak eklemi, frekans ve sönümleme oranı belirlenerek yay gibi esnek hale getirilebilir. Box2D'de [kaynak eklemi (Weld joint)](https://box2d.org/documentation/group__weld__joint.html#details) olarak adlandırılır.
* **Yay (physics.JOINT_TYPE_SPRING)** - Yay eklemi (spring joint), iki çarpışma nesnesini birbirinden sabit bir mesafede tutar. Yay eklemi, frekans ve sönümleme oranı belirlenerek yay gibi esnek hale getirilebilir. Box2D'de [mesafe eklemi (Distance joint)](https://box2d.org/documentation/group__distance__joint.html#details) olarak adlandırılır.
* **Kayar (physics.JOINT_TYPE_SLIDER)** - Kayar eklem (slider joint), iki çarpışma nesnesinin belirtilen bir eksen boyunca birbirine göre ötelenmesine izin verir ve göreli dönmeyi önler. Box2D'de [prizmatik eklem (Prismatic joint)](https://box2d.org/documentation/group__prismatic__joint.html#details) olarak adlandırılır.
* **Tekerlek (physics.JOINT_TYPE_WHEEL)** - Tekerlek eklemi (wheel joint), `bodyB` üzerindeki bir noktayı `bodyA` üzerindeki bir doğru üzerinde hareket edecek şekilde kısıtlar. Tekerlek eklemi ayrıca bir süspansiyon yayı sağlar. Box2D'de [tekerlek eklemi (Wheel joint)](https://box2d.org/documentation/group__wheel__joint.html#details) olarak adlandırılır.

## Eklem oluşturma

Burada açıklanan 2B eklemler, [`physics.create_joint()`](/ref/physics/#physics.create_joint:joint_type-collisionobject_a-joint_id-position_a-collisionobject_b-position_b-[properties]) kullanılarak program yoluyla oluşturulur:
::: sidenote
Düzenleyicide eklem oluşturma desteği planlanmaktadır, ancak henüz bir yayımlanma tarihi belirlenmemiştir.
:::

```lua
-- connect two collision objects with a fixed joint constraint (rope)
physics.create_joint(physics.JOINT_TYPE_FIXED, "obj_a#collisionobject", "my_test_joint", vmath.vector3(10, 0, 0), "obj_b#collisionobject", vmath.vector3(0, 20, 0), { max_length = 20 })
```

Yukarıdaki kod, `obj_a#collisionobject` ve `obj_b#collisionobject` çarpışma nesneleri arasında `my_test_joint` tanımlayıcısına sahip sabit bir eklem oluşturur. Eklem, `obj_a#collisionobject` çarpışma nesnesinin merkezinin 10 piksel sağına ve `obj_b#collisionobject` çarpışma nesnesinin merkezinin 20 piksel yukarısına bağlanır. Eklemin maksimum uzunluğu 20 pikseldir.

## Eklem yok etme

Bir eklem, [`physics.destroy_joint()`](/ref/physics/#physics.destroy_joint:collisionobject-joint_id) kullanılarak yok edilebilir:

```lua
-- destroy a joint previously connected to the first collision object
physics.destroy_joint("obj_a#collisionobject", "my_test_joint")
```

## Eklem özelliklerini okuma ve güncelleme

Bir eklemin özellikleri, [`physics.get_joint_properties()`](/ref/physics/#physics.get_joint_properties:collisionobject-joint_id) kullanılarak okunabilir ve [`physics.set_joint_properties()`](/ref/physics/#physics.set_joint_properties:collisionobject-joint_id-properties) kullanılarak ayarlanabilir:

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

## Eklemin tepki kuvvetini ve torkunu alma

Bir ekleme uygulanan tepki kuvveti ve tork, [`physics.get_joint_reaction_force()`](/ref/physics/#physics.get_joint_reaction_force:collisionobject-joint_id) ve [`physics.get_joint_reaction_torque()`](/ref/physics/#physics.get_joint_reaction_torque:collisionobject-joint_id) kullanılarak okunabilir.
