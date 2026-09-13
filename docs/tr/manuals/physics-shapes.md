---
title: Çarpışma şekilleri
brief: Çarpışma nesneleri temel şekiller, zarflar veya üçgen örgüleri içerebilir ya da karo haritası ve dışbükey şekil kaynaklarını kullanabilir.
---

# Çarpışma şekilleri

Bir çarpışma nesnesi (collision object) birden çok gömülü şekil içerebilir. 3B fizikte bunlar glTF veya GLB dosyalarından gelen zarfları (hull) ve üçgen örgülerini (triangle mesh) içerebilir. Çarpışma nesnesinin *Collision Shape* özelliği aracılığıyla bir karo haritası (tilemap) veya dışbükey şekil (convex shape) kaynağı da kullanabilirsiniz.

### Temel şekiller
Temel şekiller (primitive shapes) *kutu*, *küre* ve *kapsül* şekilleridir. Çarpışma nesnesine <kbd>sağ tıklayıp</kbd> <kbd>Add Shape</kbd> seçeneğini seçerek temel bir şekil ekleyebilirsiniz:

![Temel bir şekil ekleme](images/physics/add_shape.png)

## Kutu şekli
Bir kutunun konumu, dönmesi ve boyutları (genişlik, yükseklik ve derinlik) vardır:

![Kutu şekli](images/physics/box.png)

## Küre şekli
Bir kürenin konumu, dönmesi ve çapı vardır:

![Küre şekli](images/physics/sphere.png)

## Kapsül şekli
Bir kapsülün konumu, dönmesi, çapı ve yüksekliği vardır:

![Küre şekli](images/physics/capsule.png)

::: important
Kapsül şekilleri yalnızca 3B fizik kullanılırken desteklenir (*game.project* dosyasının Physics bölümünde yapılandırılır).
:::

### Karmaşık şekiller
Karmaşık şekiller karo haritası geometrisini veya dışbükey zarf (convex hull) verilerini kullanabilir. Defold 1.13.2 sürümünden itibaren 3B çarpışma nesneleri glTF veya GLB sahnelerindeki örgülerden zarf ve üçgen örgüsü şekilleri de oluşturabilir.

## 3B fizikte zarf ve örgü şekilleri {#hull-and-mesh-shapes-in-3d}

Bir örgünün dışbükey bir yaklaşımını oluşturmak için *Hull* şeklini; çarpışmaların, bölüm geometrisindeki açıklıklar gibi içbükey alanlar da dahil olmak üzere örgünün üçgenlerini izlemesi gerektiğinde ise *Mesh* şeklini kullanın.

1. *game.project* dosyasında **Physics → Type** ayarını `3D` olarak belirleyin.
2. *Outline* görünümünde çarpışma nesnesine sağ tıklayın ve <kbd>Add Shape ▸ Hull</kbd> veya <kbd>Add Shape ▸ Mesh</kbd> seçeneğini seçin.
3. Yeni şekli seçin ve *Scene* özelliğini bir *.gltf* veya *.glb* dosyasına ayarlayın.
4. *Mesh* alanından adlandırılmış bir örgü seçin. Örgü listede yoksa modelleme aracınızda örgüye bir ad verin ve sahneyi yeniden dışa aktarın.
5. Şekli, oyun nesnesinin (game object) görünür geometrisiyle hizalayacak şekilde konumlandırın ve döndürün. Gerekirse daha fazla şekil eklemek için bu adımları tekrarlayın.

Seçilen örgü, kendi yerel geometrisini sağlar; glTF düğüm dönüşümleri uygulanmaz. Örgü çarpışma şekilleri, statik ve statik olmayan çarpışma nesneleri de dahil olmak üzere Bullet 3D arka ucu tarafından desteklenir. 2B fizik arka uçları tarafından desteklenmezler.

Üçgen örgüsü geometrisi, çalışma zamanı şekil API'leri üzerinden yalnızca okunabilir. Üçgenlerini değiştirmek için kaynak örgüyü düzenleyin ve projeyi yeniden derleyin. Oyun nesnesinin ölçeği için [çarpışma şekillerini ölçekleme](#scaling-collision-shapes) bölümüne bakın.

## Karo haritası çarpışma şekli
Defold, bir karo haritasının kullandığı karo kaynağı (tile source) için kolayca fizik şekilleri oluşturmanızı sağlayan bir özellik içerir. [Karo kaynağı kılavuzu](/manuals/tilesource/#tile-source-collision-shapes), bir karo kaynağına çarpışma gruplarının nasıl ekleneceğini ve karoların çarpışma gruplarına nasıl atanacağını açıklar ([örnek](/examples/tilemap/collisions/)).

Bir karo haritasına çarpışma eklemek için:

1. Oyun nesnesine <kbd>sağ tıklayıp</kbd> <kbd>Add Component File</kbd> seçeneğini seçerek karo haritasını oyun nesnesine ekleyin. Karo haritası dosyasını seçin.
2. Oyun nesnesine <kbd>sağ tıklayıp</kbd> <kbd>Add Component ▸ Collision Object</kbd> seçeneğini seçerek oyun nesnesine bir çarpışma nesnesi bileşeni (component) ekleyin.
3. Bileşene şekiller eklemek yerine *Collision Shape* özelliğini *tilemap* dosyasına ayarlayın.
4. Çarpışma nesnesi bileşeninin *Properties* ayarlarını her zamanki gibi yapılandırın.

![Karo kaynağı çarpışması](images/physics/collision_tilemap.png)

::: important
Çarpışma grupları karo haritasının karo kaynağında tanımlandığı için burada *Group* özelliğinin **kullanılmadığını** unutmayın.
:::

## Dışbükey zarf şekli
3B fizikte [yukarıdaki düzenleyici iş akışını](#hull-and-mesh-shapes-in-3d) kullanarak doğrudan bir örgüden zarf oluşturabilirsiniz. Eski `.convexshape` kaynağı da desteklenir ve harici bir düzenleyici kullanılarak noktalardan oluşturulabilir:

1. Harici bir düzenleyici kullanarak dışbükey zarf şekli dosyası (`.convexshape` dosya uzantısıyla) oluşturun.
2. Dosyayı bir metin düzenleyici veya harici araç kullanarak elle düzenleyin (aşağıya bakın)
3. Çarpışma nesnesi bileşenine şekiller eklemek yerine *Collision Shape* özelliğini *dışbükey şekil* dosyasına ayarlayın.

### Dosya biçimi
Dışbükey zarf dosya biçimi, diğer tüm Defold dosyalarıyla aynı veri biçimini, yani protobuf metin biçimini kullanır. Bir dışbükey zarf şekli, zarfın noktalarını tanımlar. 2B fizikte noktaların saat yönünün tersine sıralanarak verilmesi önerilir. 3B fizik modunda soyut bir nokta bulutu kullanılır. 2B örneği:

```
shape_type: TYPE_HULL
data: 200.000
data: 100.000
data: 0.0
data: 400.000
data: 100.000
data: 0.0
data: 400.000
data: 300.000
data: 0.0
data: 200.000
data: 300.000
data: 0.0
```

Yukarıdaki örnek bir dikdörtgenin dört köşesini tanımlar:

```
 200x300   400x300
    4---------3
    |         |
    |         |
    |         |
    |         |
    1---------2
 200x100   400x100
```

## Harici araçlar

Çarpışma şekilleri oluşturmak için kullanılabilecek çeşitli harici araçlar vardır:

* CodeAndWeb'in [Physics Editor](https://www.codeandweb.com/physicseditor/tutorials/how-to-create-physics-shapes-for-defold) aracı, sprite bileşenleri ve bunlarla eşleşen çarpışma şekilleri içeren oyun nesneleri oluşturmak için kullanılabilir.
* [Defold Polygon Editor](https://rossgrams.itch.io/defold-polygon-editor), dışbükey zarf şekilleri oluşturmak için kullanılabilir.
* [Physics Body Editor](https://selimanac.github.io/physics-body-editor/), dışbükey zarf şekilleri oluşturmak için kullanılabilir.


# Çarpışma şekillerini ölçekleme {#scaling-collision-shapes}
Çarpışma nesnesi ve şekilleri, oyun nesnesinin ölçeğini devralır. Bu davranışı devre dışı bırakmak için *game.project* dosyasının Physics bölümündeki [Allow Dynamic Transforms](/manuals/project-settings/#allow-dynamic-transforms) onay kutusunun işaretini kaldırın. Yalnızca tüm eksenlerde aynı oranda ölçeklemenin desteklendiğini ve ölçek tüm eksenlerde aynı değilse en küçük ölçek değerinin kullanılacağını unutmayın.

# Çarpışma şekillerini yeniden boyutlandırma
Temel şekiller, çalışma sırasında `physics.set_shape()` kullanılarak yeniden boyutlandırılabilir. Bu işlev, zarfın köşelerini veya üçgen örgüsü geometrisini değiştirmez. Örnek:

```lua
-- set capsule shape data
local capsule_data = {
  type = physics.SHAPE_TYPE_CAPSULE,
  diameter = 10,
  height = 20,
}
physics.set_shape("#collisionobject", "my_capsule_shape", capsule_data)

-- set sphere shape data
local sphere_data = {
  type = physics.SHAPE_TYPE_SPHERE,
  diameter = 10,
}
physics.set_shape("#collisionobject", "my_sphere_shape", sphere_data)

-- set box shape data
local box_data = {
  type = physics.SHAPE_TYPE_BOX,
  dimensions = vmath.vector3(10, 10, 5),
}
physics.set_shape("#collisionobject", "my_box_shape", box_data)
```

::: sidenote
Belirtilen kimliğe sahip ve doğru türde bir şekil, çarpışma nesnesinde zaten bulunmalıdır.
:::

# Çarpışma şekillerini döndürme

## 3B fizikte çarpışma şekillerini döndürme
3B fizikte çarpışma şekilleri tüm eksenler etrafında döndürülebilir.


## 2B fizikte çarpışma şekillerini döndürme
2B fizikte çarpışma şekilleri yalnızca z ekseni etrafında döndürülebilir. x veya y ekseni etrafında döndürme yanlış sonuçlar verir ve bundan kaçınmanız önerilir; buna, şekli x veya y ekseni boyunca ters çevirmek için 180 derece döndürme de dahildir. Bir fizik şeklini ters çevirmek için [`physics.set_hlip(url, flip)`](/ref/stable/physics/?#physics.set_hflip:url-flip) ve [`physics.set_vlip(url, flip)`](/ref/stable/physics/?#physics.set_vflip:url-flip) kullanılması önerilir.


# Hata ayıklama
Çalışma sırasında çarpışma şekillerini görmek için [fizik hata ayıklamasını etkinleştirebilirsiniz](/manuals/debugging-game-logic/#debugging-problems-with-physics).
