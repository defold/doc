---
title: Defold sahne düzenleyicisi
brief: Sahne düzenleyicisinde koleksiyonları, oyun nesnelerini, GUI'leri, parçacık efektlerini ve diğer görsel varlıkları düzenlersiniz. Bu kılavuz seçimi, araçları ve serbest kamera modu ile kamera ayarları dahil olmak üzere sahne görünümünde 2B ve 3B gezinmeyi açıklar.
---

# Defold sahne düzenleyicisi

**Sahne düzenleyicisi (Scene Editor)**, koleksiyonlar (collection), oyun nesneleri (game object) ve diğer görsel varlıklar (asset) gibi sahneleri oluşturmak ve düzenlemek için kullanılan görsel düzenleyicidir.

Başlangıçtaki kamera görünümü kaynağa (resource) bağlıdır. Modeller ve glTF sahneleri gibi 3B kaynaklarda varsayılan olarak **perspektif (perspective)**, sprite bileşenleri, karo haritaları ve GUI sahneleri gibi 2B kaynaklarda ise **ortografik (orthographic)** izdüşüm kullanılır. Kamera yönelimini, izdüşümü ve ızgarayı sahne araç çubuğundan değiştirebilirsiniz.

## Sahne düzenleyicisini açma

Sahne düzenleyicisini açmak için *Assets* bölmesinde aşağıdakiler gibi bir görsel kaynağa çift tıklayın:

- **Sahne yapısı** — koleksiyonlar (`.collection`), oyun nesneleri (`.go`)
- **2B varlıklar** — atlas (`.atlas`), karo haritaları (`.tilemap`), sprite bileşenleri (`.sprite`), karo kaynakları (`.tilesource`)
- **3B varlıklar** — modeller (`.model`, `.glb`, `.gltf`)
- **Kullanıcı arayüzü (UI)** — GUI sahneleri (`.gui`)
- **Efektler** — parçacık efektleri (particle effect) (`.particlefx`)
- Ve diğerleri

## Hatırlanan sahne görünümleri

Düzenleyici, bir sahne kaynağının sekmesi kapatıldığında veya düzenleyiciden çıkıldığında o kaynağın kamera durumunu hatırlar. Aynı kaynağı yeniden açmak görünümünü geri yükler; böylece farklı koleksiyonlar veya modeller farklı kamera konumlarını, yönelimlerini ve izdüşümlerini koruyabilir.

Görünürlük filtreleri de her sahne için ayrı ayrı hatırlanır. Bir sahnede modelleri veya bileşen kılavuzlarını gizlemek, başka bir sahnede aynı filtreleri kullanmanızı gerektirmez. Bunlar düzenleyicinin görünüm ayarlarıdır ve oyunun kamerasını veya çalışma sırasındaki görünürlüğü değiştirmez.

Kaydedilmiş kamera durumu olmayan kaynaklarda model, örgü (mesh) ve glTF kaynakları perspektif görünümde başlar. Çarpışma nesnelerinin görünümü projenin 2B/3B fizik ayarına göre seçilir; koleksiyonların ve oyun nesnelerinin başlangıç görünümü ise sahne geometrilerine göre seçilir.

## Sahne görünümünde gezinme (kamera denetimleri)

Sahne düzenleyicisinin kamerası fare ve klavyeyle denetlenebilir. Kullanılabilir denetimler, standart kamera gezinmesini mi yoksa **serbest kamera modunu (Free Camera Mode)** mu kullandığınıza bağlıdır.

### Standart gezinme (tüm görsel düzenleyiciler)

Görsel düzenleyicilerde şu denetimler kullanılabilir:

- **Kaydırma**
  - <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Yakınlaştırma/uzaklaştırma**
  - <kbd>Mouse Wheel</kbd> veya
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> + <kbd>Left Mouse Button</kbd>
- **Seçimin etrafında döndürme/dolanma (3B)**
  - <kbd>Ctrl</kbd>/<kbd>^ Control</kbd> + <kbd>Left Mouse Button</kbd>

Kamerayı geçerli seçime odaklamak için **Frame Selection** (<kbd>F</kbd>) komutunu da kullanabilirsiniz.

## 2B ve 3B sahne yönelimi {#2d-and-3d-scene-orientation}

Sahne görünümü hem 2B hem de 3B iş akışlarında kullanılabilir:

- **2B** çalışırken genellikle 2B yönelimli bir ızgaraya sahip ortografik görünüm kullanırsınız.
- **3B** çalışırken genellikle:
  - Görünümü 3B yönelime yeniden hizalarsınız,
  - **Perspektif** kamera kullanırsınız,
  - Uygun bir ızgara düzlemi seçersiniz ("zemin" için genellikle **Y**).

Bu işlevlere araç çubuğundan ve **View** menüsünden erişebilirsiniz.

![3B sahne düzenleyicisi](images/editor/3d_scene.png)

## Araç çubuğuna genel bakış

Sahne görünümünün sağ üst köşesinde, sık kullanılan araçları ve görünüm seçeneklerini içeren bir araç çubuğu bulunur (soldan sağa):

- **Move tool** (<kbd>W</kbd>)
- **Rotate tool** (<kbd>E</kbd>)
- **Scale tool** (<kbd>R</kbd>)
- **Grid Settings** (`▦`)
- **Align/Realign Camera 2D/3D** (`2D`) — 2B ve 3B yönelim arasında geçiş yapar (kısayol <kbd>.</kbd>)
- **Camera Perspective/Orthographic**
- **Visibility Filters** (`👁`)

![Araç çubuğu](images/editor/toolbar.png)

## Nesneleri seçme ve değiştirme {#manipulating-objects}

### Nesneleri seçme

Nesneleri seçmek için ana pencerede üzerlerine <kbd>farenin sol düğmesiyle tıklayın</kbd>. Düzenleyici görünümünde nesneyi çevreleyen dikdörtgen (veya dikdörtgenler prizması), hangi öğenin seçildiğini belirtmek için camgöbeği renkle vurgulanır. Seçilen nesne, yukarıdaki resimde olduğu gibi `Outline` görünümünde de vurgulanır.

  Nesneleri şu yollarla da seçebilirsiniz:

- <kbd>Farenin sol düğmesiyle tıklayın</kbd> ve seçim bölgesindeki tüm nesneleri seçmek için <kbd>sürükleyin</kbd>.
- <kbd>Farenin sol düğmesiyle tıklayarak</kbd> `Outline` görünümündeki nesneleri seçin; <kbd>⇧ Shift</kbd> tuşunu basılı tutarken seçimi genişletebilir veya <kbd>Ctrl</kbd>/<kbd>⌘ Cmd</kbd> tuşunu basılı tutarken tıkladığınız nesneleri seçebilir ya da seçimden çıkarabilirsiniz.

#### Taşıma aracı

![Taşıma aracı](images/editor/icon_move.png){.left}

Nesneleri taşımak için *Move Tool* aracını kullanın. Aracı sahne düzenleyicisinin sağ üst köşesindeki araç çubuğunda bulabilir veya <kbd>W</kbd> tuşuna basarak seçebilirsiniz.

![Nesneyi taşıma](images/editor/move.png){.inline}![Nesneyi 3B taşıma](images/editor/move_3d.png){.inline}

Dönüşüm denetimi (gizmo) değişerek kareler ve oklardan oluşan bir dizi tutamaç gösterir (seçili tutamaç turuncuya döner). Taşımak için bu tutamaçları <kbd>sürükleyebilirsiniz</kbd>:

- ortadaki camgöbeği kare tutamaç, nesneyi yalnızca ekran uzayında (screen space) taşır,
- her eksen boyunca uzanan kırmızı, yeşil ve mavi 3 ok, nesneyi yalnızca ilgili X, Y veya Z ekseni boyunca taşır.
- kırmızı, yeşil ve mavi 3 kare tutamaç (dış çizgileri görünür, içleri saydam), nesneyi yalnızca ilgili düzlemde taşır; örneğin X-Y (mavi) düzleminde ve (kamera 3B olarak döndürüldüğünde görünen) X-Z (yeşil) ve Y-Z (kırmızı) düzlemlerinde.

#### Döndürme aracı

![Döndürme aracı](images/editor/icon_rotate.png){.left}

Nesneleri döndürmek için araç çubuğundan *Rotate Tool* aracını seçin veya <kbd>E</kbd> tuşuna basın.

![Nesneyi döndürme](images/editor/rotate.png){.inline}![Nesneyi 3B döndürme](images/editor/rotate_3d.png){.inline}

Bu araç, döndürmek için <kbd>sürükleyebileceğiniz</kbd> dört dairesel tutamaçtan oluşur (seçili tutamaç turuncuya döner):

- camgöbeği tutamaç (dıştaki, en büyük daire), nesneyi ekran uzayında döndürür
- daha küçük kırmızı, yeşil ve mavi 3 dairesel tutamaç, X, Y ve Z eksenlerinin her biri etrafında ayrı ayrı döndürmeye olanak tanır. 2B ortografik görünümde bunlardan ikisi X ve Y eksenlerine dik olduğundan, daireler yalnızca nesnenin içinden geçen iki çizgi olarak görünür.

#### Ölçekleme aracı

![Ölçekleme aracı](images/editor/icon_scale.png){.left}

Nesneleri ölçeklemek için araç çubuğundan *Scale Tool* aracını seçin veya <kbd>R</kbd> tuşuna basın.

![Nesneyi ölçekleme](images/editor/scale.png){.inline}![Nesneyi 3B ölçekleme](images/editor/scale_3d.png){.inline}

Bu araç, ölçeklemek için <kbd>sürükleyebileceğiniz</kbd> kare/küp şeklindeki bir dizi tutamaçtan oluşur (seçili tutamaç turuncuya döner):

- ortadaki camgöbeği küp, nesneyi tüm eksenlerde (Z dahil) aynı oranda ölçekler.
- kırmızı, mavi ve yeşil 3 küp tutamaç, nesneyi X, Y ve Z eksenlerinin her biri boyunca ayrı ayrı ölçekler.
- kırmızı, yeşil ve mavi 3 kare tutamaç (dış çizgileri görünür, içleri saydam), nesneyi X-Y, X-Z veya Y-Z düzlemlerinde ayrı ayrı ölçekler.

### Görünürlük filtreleri {#visibility-filters}

Çeşitli bileşen (component) türlerinin yanı sıra sınırlayıcı kutuların ve kılavuz çizgilerinin görünürlüğünü açıp kapatmak için araç çubuğundaki **görünürlük göz simgesine** (`👁`) tıklayın (`Component Guides` veya <kbd>Ctrl</kbd> + <kbd>H</kbd> (Win/Linux) ya da <kbd>^ Ctrl</kbd> + <kbd>⌘ Cmd</kbd> + <kbd>H</kbd>(Mac) kısayolu).

![Görünürlük filtreleri](images/editor/visibilityfilters.png)

## Izgara ayarları {#grid-settings}

Izgara, iş akışınıza uyacak şekilde özelleştirilebilir (özellikle 3B çalışırken yararlıdır). Izgara ayarları açılır penceresini açmak için **Grid Settings** düğmesine (`▦`) tıklayın.

Düzenleyici, 2B ve 3B görünümler için ayrı ızgara ayarları tutar. İstediğiniz mod etkinken boyutu, düzlemi ve görünümü ayarlayın; mod değiştirdiğinizde o modun ızgara ayarları geri yüklenir. **Reset to Defaults**, etkin modun ayarlarını sıfırlar.

![Izgara ayarları](images/editor/grid_popup.png)

Ayarlar şunları içerir:

- **Grid size (X/Y/Z)**
  Her eksen boyunca ızgara çizgileri arasındaki aralığı ayarlar. Küçük nesneleri hassas biçimde yerleştirmek için daha küçük, daha geniş bir genel görünüm için daha büyük değerler kullanın.
- **Active plane (X/Y/Z)**
  Izgaranın hangi düzlemde çizileceğini seçer. 2B iş akışlarında bu genellikle **Z** düzlemidir (varsayılan X-Y düzlemi). 3B iş akışlarında, zemin/taban düzlemini temsil etmek için yaygın olarak **Y** kullanılır.
- **Grid color**
  Izgara çizgilerinin rengini ayarlar. Farklı sahne arka planlarıyla karşıtlık oluşturmak için yararlıdır.
- **Grid opacity**
  Izgara çizgilerinin ne kadar saydam olduğunu denetler. Düşük değerler, ızgaranın referans sağlamayı sürdürürken daha az dikkat dağıtmasını sağlar.
- **Reset to Defaults** düğmesi
  Tüm ızgara ayarlarını özgün değerlerine geri yükler.

## Kamera türü: perspektif ve ortografik

Sahne düzenleyicisi her ikisini de destekler:

- **Ortografik** kamera (2B iş akışlarında yaygındır)
- **Perspektif** kamera (3B iş akışlarında yaygındır)

Aralarında geçiş yapmak için araç çubuğundaki kamera düğmesini kullanın. 3B sahnelerde perspektif görünümde gezinmek genellikle daha doğal hissettirir.

## Serbest kamera modu {#free-camera-mode}

Sahne düzenleyicisi, 3B sahnelerde hızlı gezinmek için birinci şahıs / "FPS tarzı" bir kamera olan **serbest kamera modunu (Free Camera Mode)** sunar.

### Serbest kamera modunu etkinleştirme

- <kbd>Right Mouse Button</kbd> düğmesini basılı tutun — serbest kamera modu, düğme basılı tutulduğu sürece etkindir
- <kbd>Shift</kbd> + <kbd>`</kbd> (ters tırnak) — serbest kamera modunu açar ve tuşlar bırakıldıktan sonra da etkin tutar

::: sidenote
Bazı klavye düzenlerinde (ör. İsveççe) ters tırnak tuşu bir ölü tuştur ve kısayolu beklendiği gibi tetiklemeyebilir. Bu kısayolu
`File ▸ Preferences ▸ Keys` bölümünde yeniden atayabilir ve `Scene -> Free Camera -> Activate` için bir kısayol girebilirsiniz
:::

Serbest kamera modu etkinken sahne görünümü, kenarları boyunca uzanan bir çizgiyle vurgulanır.

### Serbest kamera modundan çıkma

- <kbd>Right Mouse Button</kbd> düğmesini bırakın (basılı tutarak etkinleştirildiğinde) veya
- Serbest kamera modu açılıp kapanabilen bir mod olarak etkinleştirildiyse <kbd>Left Mouse Button</kbd> veya <kbd>Right Mouse Button</kbd> düğmesine basıp bırakın ya da <kbd>Esc</kbd> tuşuna basın.

### Etrafa bakma (fareyle bakış)

Serbest kamera modu etkinken aşağıdaki tuşlar (düzenleyici araçları yerine) kamera hareketini denetler:

- **Yatay dönüşü (yaw)** (sol/sağ) ve **dikey dönüşü (pitch)** (yukarı/aşağı) denetlemek için fareyi hareket ettirin
- Kameranın ters dönmesini önlemek için dikey dönüş sınırlandırılır

İsteğe bağlı olarak Y eksenini tersine de çevirebilirsiniz (aşağıdaki **Serbest kamera ayarları** bölümüne bakın).

### Hareket etme

Serbest kamera modu etkinken:

- <kbd>W</kbd> — ileri
- <kbd>S</kbd> — geri
- <kbd>A</kbd> — sol
- <kbd>D</kbd> — sağ
- <kbd>E</kbd> — yukarı
- <kbd>Q</kbd> — aşağı

::: sidenote
Tüm hareket tuşları `File ▸ Preferences ▸ Keys` bölümünden yeniden atanabilir. Ardından `Scene -> Free Camera` ifadesini arayın
:::

Hızı değiştiren tuşlar:

- <kbd>Shift</kbd> tuşunu basılı tutun — daha hızlı hareket edin
- <kbd>Alt</kbd>/<kbd>⌥ Option</kbd> tuşunu basılı tutun — daha yavaş / daha hassas hareket edin

### Yürüme modu (isteğe bağlı)

Serbest kamera modu, **Walking Mode** özelliğini destekler.

Etkinleştirildiğinde:
- Yukarı/aşağı hareket, bir zemin düzleminde yere basarak birinci şahıs bakış açısıyla yürümeye daha çok benzeyecek şekilde kısıtlanır.
- Bu, bir bölümü keşfederken tutarlı bir "yere basma" hareketi istediğinizde yararlıdır.

## Kamera ayarları açılır penceresi

Araç çubuğundaki perspektif kamera düğmesinde, kamerayla ilgili tercihleri içeren bir açılır pencere bulunur.

![Perspektif kamera ayarları](images/editor/camera_popup.png)

Açılır pencere şunları içerir:

- **Move Speed**
  Serbest kameranın hareket hızını ayarlar.

- **Look Sensitivity**
  Kameranın fare hareketine tepki olarak ne kadar hızlı döndüğünü ayarlar.

- **Invert Y**
  Fareyle dikey bakış yönünü tersine çevirir.

- **Walking Mode**
  Zeminde gezinmeye benzer bir hareket sağlamak için hareketi kısıtlar.

- **Reset to Defaults**
  Varsayılan kamera ayarlarını geri yükler.
