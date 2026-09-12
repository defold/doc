---
title: Defold'da çarpışma nesneleri
brief: Çarpışma nesnesi, bir oyun nesnesine fiziksel davranış kazandırmak için kullandığınız bir bileşendir. Çarpışma nesnesinin fiziksel özellikleri ve uzamsal bir şekli vardır.
---

# Çarpışma nesneleri

Çarpışma nesnesi (collision object), bir oyun nesnesine (game object) fiziksel davranış kazandırmak için kullandığınız bir bileşendir (component). Çarpışma nesnesinin ağırlık, geri sekme katsayısı ve sürtünme gibi fiziksel özellikleri vardır; uzayda kapladığı bölgeyi, bileşene eklediğiniz bir veya daha fazla _şekil_ belirler. Defold aşağıdaki çarpışma nesnesi türlerini destekler:

Statik nesneler
: Statik nesneler (static objects) hiç hareket etmez, ancak statik bir nesneyle çarpışan dinamik bir nesne sekerek ve/veya kayarak tepki verir. Statik nesneler, hareket etmeyen bölüm geometrisini (örneğin zemin ve duvarları) oluşturmak için çok kullanışlıdır. Ayrıca performans açısından dinamik nesnelerden daha az kaynak tüketirler. Statik nesneleri hareket ettiremez veya başka bir şekilde değiştiremezsiniz.

Dinamik nesneler
: Dinamik nesneler (dynamic objects) fizik motoru tarafından simüle edilir. Motor tüm çarpışmaları çözümler ve ortaya çıkan kuvvetleri uygular. Dinamik nesneler, gerçekçi davranması gereken nesneler için uygundur. Bu nesneleri etkilemenin en yaygın yolu, [kuvvet uygulamak](/ref/physics/#apply_force) veya açısal [sönümleme](/ref/stable/physics/#angular_damping) ve [hız](/ref/stable/physics/#linear_velocity) ile doğrusal [sönümleme](/ref/stable/physics/#linear_damping) ve [hız](/ref/stable/physics/#angular_velocity) değerlerini değiştirmek gibi dolaylı yöntemlerdir. *game.project* dosyasında [Allow Dynamic Transforms ayarı](/manuals/project-settings/#allow-dynamic-transforms) etkinleştirildiğinde dinamik bir nesnenin konumunu ve yönelimini doğrudan değiştirmek de mümkündür.

Kinematik nesneler
: Kinematik nesneler (kinematic objects), diğer fizik nesneleriyle çarpışmaları kaydeder, ancak fizik motoru herhangi bir otomatik simülasyon gerçekleştirmez. Çarpışmaları çözümleme veya yok sayma işi size bırakılır ([daha fazla bilgi edinin](/manuals/physics-resolving-collisions)). Kinematik nesneler, oyuncu karakteri gibi fiziksel tepkileri üzerinde hassas denetim gerektiren, oyuncu veya betik tarafından kontrol edilen nesneler için çok uygundur.

Tetikleyiciler
: Tetikleyiciler (triggers), basit çarpışmaları kaydeden nesnelerdir. Tetikleyiciler, işlem yükü düşük çarpışma nesneleridir. Fizik dünyasıyla etkileşmek yerine onu okumaları bakımından [ışın sorgularına](/manuals/physics-ray-casts) benzerler. Yalnızca bir isabeti kaydetmesi gereken nesneler (mermi gibi) için veya bir nesne belirli bir noktaya ulaştığında belirli eylemleri tetiklemek istediğiniz oyun mantığının bir parçası olarak uygundurlar. Tetikleyiciler, hesaplama açısından kinematik nesnelerden daha az kaynak tüketir ve mümkün olduğunda bunların yerine kullanılmaları önerilir.


## Çarpışma nesnesi bileşeni ekleme

Çarpışma nesnesi bileşeninin *Properties* değerleri, türünü ve fiziksel özelliklerini belirler. Ayrıca fizik nesnesinin bütün şeklini tanımlayan bir veya daha fazla *Shapes* öğesi içerir.

Bir oyun nesnesine çarpışma nesnesi bileşeni eklemek için:

1. *Outline* görünümünde oyun nesnesine <kbd>sağ tıklayın</kbd> ve bağlam menüsünden <kbd>Add Component ▸ Collision Object</kbd> seçeneğini seçin. Bu işlem, hiç şekil içermeyen yeni bir bileşen oluşturur.
2. Yeni bileşene <kbd>sağ tıklayın</kbd> ve <kbd>Add Shape</kbd> seçeneğini seçin, ardından bir şekil seçin: 3B fizik kullanan projelerde <kbd>Box</kbd>, <kbd>Capsule</kbd>, <kbd>Sphere</kbd>, <kbd>Hull</kbd> veya <kbd>Mesh</kbd>; 2B fizik kullanan projelerde <kbd>Box</kbd> veya <kbd>Circle</kbd>. Hull ve Mesh şekilleri Defold 1.13.2 sürümünden beri kullanılabilir ve bir glTF veya GLB sahnesindeki adlandırılmış bir örgüyü (mesh) kullanır. Bileşene birden fazla şekil ekleyebilirsiniz. Ayrıca *Collision Shape* özelliği aracılığıyla bir karo haritası (tilemap) veya `.convexshape` kaynağı kullanabilirsiniz.
3. Şekilleri düzenlemek için taşıma, döndürme ve ölçekleme araçlarını kullanın.
4. Bileşeni *Outline* görünümünde seçin ve çarpışma nesnesinin *Properties* değerlerini düzenleyin.

![Fizik çarpışma nesnesi](images/physics/collision_object.png)


## Çarpışma şekli ekleme

Bir çarpışma bileşeni, 3B fizikte dışbükey zarflar (hulls) ve üçgen örgüler dahil birden fazla gömülü şekil içerebilir veya bir karo haritası ya da dışbükey şekil kaynağı kullanabilir. Çeşitli şekiller ve bunları bir çarpışma bileşenine ekleme hakkında daha fazla bilgi için [Çarpışma şekilleri kılavuzuna](/manuals/physics-shapes) bakın.


## Çarpışma nesnesinin özellikleri

Id
: Bileşenin kimliği.

Collision Shape
: Bir karo haritası veya `.convexshape` kaynağı. Bir glTF veya GLB örgüsü kullanmak için bunun yerine bileşene bir Hull veya Mesh şekli ekleyin ve bu şeklin *Scene* ve *Mesh* özelliklerini ayarlayın. [Daha fazla bilgi için Çarpışma şekilleri kılavuzuna](/manuals/physics-shapes) bakın.

Type
: Çarpışma nesnesinin türü: `Dynamic`, `Kinematic`, `Static` veya `Trigger`. Nesneyi `Dynamic` olarak ayarlarsanız *Mass* özelliğini sıfırdan farklı bir değere ayarlamanız _gerekir_. `Dynamic` veya `Static` nesneler için *Friction* ve *Restitution* değerlerinin kullanım durumunuza uygun olduğunu da kontrol etmeniz önerilir.

Friction
: Sürtünme, nesnelerin birbirlerinin yüzeyinde gerçekçi biçimde kaymasını sağlar. Sürtünme değeri genellikle `0` (sürtünme yoktur---çok kaygan bir nesne) ile `1` (güçlü sürtünme---aşındırıcı bir nesne) arasında ayarlanır. Ancak herhangi bir pozitif değer geçerlidir.

  Sürtünmenin şiddeti, normal kuvvetle orantılıdır (buna Coulomb sürtünmesi denir). İki şekil (`A` ve `B`) arasındaki sürtünme kuvveti hesaplanırken her iki nesnenin sürtünme değerleri geometrik ortalama alınarak birleştirilir:

```math
F = sqrt( F_A * F_B )
```

  Bu, nesnelerden birinin sürtünmesi sıfırsa aralarındaki temasın da sıfır sürtünmeli olacağı anlamına gelir.

Restitution
: Geri sekme katsayısı, nesnenin "sekme özelliğini" belirler. Değer genellikle 0 (esnek olmayan çarpışma—nesne hiç sekmez) ile 1 (tam esnek çarpışma---nesnenin hız vektörü sekme sırasında tam olarak yansıtılır) arasındadır

  İki şeklin (`A` ve `B`) geri sekme katsayıları şu formülle birleştirilir:

```math
R = max( R_A, R_B )
```

  Bir şekil birden fazla noktada temas ettiğinde, Box2D yinelemeli bir çözücü kullandığı için geri sekme yaklaşık olarak simüle edilir. Box2D, sekmeden kaynaklanan titreşimleri önlemek için çarpışma hızı düşük olduğunda esnek olmayan çarpışmalar da kullanır

Linear damping
: Doğrusal sönümleme, cismin doğrusal hızını azaltır. Yalnızca temas sırasında oluşan sürtünmeden farklıdır ve nesnelere, havadan daha yoğun bir ortamda hareket ediyormuş gibi süzülme görünümü vermek için kullanılabilir. Geçerli değerler 0 ile 1 arasındadır.

  Box2D, kararlılık ve performans için sönümlemeyi yaklaşık olarak hesaplar. Küçük değerlerde sönümleme etkisi zaman adımından bağımsızken daha büyük sönümleme değerlerinde bu etki zaman adımına göre değişir. Oyununuzu sabit bir zaman adımıyla çalıştırırsanız bu durum hiçbir zaman sorun oluşturmaz.

Angular damping
: Açısal sönümleme, doğrusal sönümleme gibi çalışır, ancak cismin açısal hızını azaltır. Geçerli değerler 0 ile 1 arasındadır.

Locked rotation
: Bu özellik etkinleştirildiğinde, uygulanan kuvvetler ne olursa olsun çarpışma nesnesinin dönmesi tamamen devre dışı bırakılır.

Bullet
: Bu özellik etkinleştirildiğinde, çarpışma nesnesi ile diğer dinamik çarpışma nesneleri arasında sürekli çarpışma algılama (continuous collision detection, CCD) etkinleştirilir. *Type* değeri `Dynamic` olarak ayarlanmamışsa *Bullet* özelliği yok sayılır.

Group
: Nesnenin ait olması gereken çarpışma grubunun adı. 16 farklı grubunuz olabilir ve bu grupları oyununuz için uygun gördüğünüz şekilde adlandırabilirsiniz. Örneğin `players`, `bullets`, `enemies` ve `world`. *Collision Shape* bir karo haritasına ayarlanmışsa bu alan kullanılmaz; grup adları karo kaynağından alınır. [Çarpışma grupları hakkında daha fazla bilgi edinin](/manuals/physics-groups).

Mask
: Bu nesnenin çarpışması gereken diğer _gruplar_. Bir grubun adını yazabilir veya virgülle ayrılmış bir listede birden fazla grup belirtebilirsiniz. *Mask* alanını boş bırakırsanız nesne hiçbir şeyle çarpışmaz. [Çarpışma grupları hakkında daha fazla bilgi edinin](/manuals/physics-groups).

Generate Collision Events
: Etkinleştirildiğinde bu nesnenin çarpışma olayları göndermesine izin verir

Generate Contact Events
: Etkinleştirildiğinde bu nesnenin temas olayları göndermesine izin verir

Generate Trigger Events
: Etkinleştirildiğinde bu nesnenin tetikleyici olayları göndermesine izin verir


## Çalışma zamanı özellikleri

Bir fizik nesnesinin `go.get()` ve `go.set()` kullanılarak okunabilen ve değiştirilebilen çeşitli özellikleri vardır:

`angular_damping`
: Çarpışma nesnesi bileşeninin açısal sönümleme değeri (`number`). [API başvuru belgeleri](/ref/physics/#angular_damping).

`angular_velocity`
: Çarpışma nesnesi bileşeninin geçerli açısal hızı (`vector3`). [API başvuru belgeleri](/ref/physics/#angular_velocity).

`linear_damping`
: Çarpışma nesnesinin doğrusal sönümleme değeri (`number`). [API başvuru belgeleri](/ref/physics/#linear_damping).

`linear_velocity`
: Çarpışma nesnesi bileşeninin geçerli doğrusal hızı (`vector3`). [API başvuru belgeleri](/ref/physics/#linear_velocity).

`mass`
: Çarpışma nesnesi bileşeninin tanımlı fiziksel kütlesi. SALT OKUNUR. (`number`). [API başvuru belgeleri](/ref/physics/#mass).
