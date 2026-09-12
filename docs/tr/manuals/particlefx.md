---
title: Defold'da parçacık efektleri
brief: Bu kılavuz, parçacık efekti bileşeninin nasıl çalıştığını ve görsel parçacık efektleri oluşturmak için nasıl düzenleneceğini açıklar.
---

# Parçacık efektleri

Parçacık efektleri (particle effects), oyunların görsel etkisini artırmak için kullanılır. Bunları patlamalar, kan sıçramaları, izler, hava olayları veya başka efektler oluşturmak için kullanabilirsiniz.

![ParticleFX düzenleyicisi](images/particlefx/editor.png)

Parçacık efektleri, bir dizi yayıcıdan ve isteğe bağlı değiştiricilerden oluşur:

Yayıcı
: Yayıcı (emitter), belirli bir konuma yerleştirilen ve parçacıkları şekli boyunca eşit dağılımla yayan bir şekildir. Yayıcı, parçacıkların oluşturulmasını ve her bir parçacığın görüntüsünü veya animasyonunu, yaşam süresini, rengini, şeklini ve hızını denetleyen özellikler içerir.

Değiştirici
: Değiştirici (modifier), oluşturulan parçacıkların hızını etkileyerek bunların belirli bir yönde hızlanmasını veya yavaşlamasını, radyal olarak hareket etmesini ya da bir noktanın etrafında dönmesini sağlar. Değiştiriciler, tek bir yayıcının parçacıklarını veya belirli bir yayıcıyı etkileyebilir.

## Efekt oluşturma

*Assets* tarayıcısındaki bağlam menüsünden <kbd>New... ▸ Particle FX</kbd> seçeneğini seçin. Yeni parçacık efekti dosyasına bir ad verin. Düzenleyici, dosyayı [Scene Editor](/manuals/editor/#the-scene-editor) görünümünde açar.

*Outline* bölmesinde varsayılan yayıcı gösterilir. Özelliklerini aşağıdaki *Properties* bölmesinde görmek için yayıcıyı seçin.

![Varsayılan parçacıklar](images/particlefx/default.png)

Efekte yeni bir yayıcı eklemek için *Outline* görünümünün köküne <kbd>sağ tıklayın</kbd> ve bağlam menüsünden <kbd>Add Emitter ▸ [type]</kbd> seçeneğini seçin. Yayıcının türünü yayıcı özelliklerinden değiştirebileceğinizi unutmayın.

Yeni bir değiştirici eklemek için *Outline* görünümünde değiştiricinin yer alacağı konuma (efektin köküne veya belirli bir yayıcıya) <kbd>sağ tıklayın</kbd> ve <kbd>Add Modifier</kbd> seçeneğini, ardından değiştirici türünü seçin.

![Değiştirici ekleme](images/particlefx/add_modifier.png)

![Eklenecek değiştiriciyi seçme](images/particlefx/add_modifier_select.png)

Efektin kökünde bulunan (bir yayıcıya alt öğe olarak bağlanmamış) bir değiştirici, efektteki tüm parçacıkları etkiler.

Bir yayıcıya alt öğe olarak eklenen değiştirici yalnızca o yayıcıyı etkiler.

## Efekti önizleme

* Efekti önizlemek için menüden <kbd>View ▸ Play</kbd> seçeneğini seçin. Efekti düzgün görebilmek için kamerayı uzaklaştırmanız gerekebilir.
* Efekti duraklatmak için <kbd>View ▸ Play</kbd> seçeneğini yeniden seçin.
* Efekti durdurmak için <kbd>View ▸ Stop</kbd> seçeneğini seçin. Tekrar oynattığınızda efekt başlangıç durumundan yeniden başlar.

Bir yayıcıyı veya değiştiriciyi düzenlediğinizde, efekt duraklatılmış olsa bile sonuç düzenleyicide hemen görünür:

![Parçacıkları düzenleme](images/particlefx/rotate.gif)

## Yayıcı özellikleri

Id
: Yayıcı tanımlayıcısı; belirli yayıcılar için işleme (rendering) sabitleri ayarlanırken kullanılır.

Position/Rotation
: Yayıcının ParticleFX bileşenine (component) göre dönüşümü.

Play Mode
: Yayıcının nasıl oynatılacağını denetler:
  - `Once`, süresi dolduğunda yayıcıyı durdurur.
  - `Loop`, süresi dolduğunda yayıcıyı yeniden başlatır.

Size Mode
: Kare dizisi animasyonlarının (flipbook animation) nasıl boyutlandırılacağını denetler:
  - `Auto`, her kare dizisi animasyonu karesinin boyutunu kaynak görüntünün boyutunda tutar.
  - `Manual`, parçacık boyutunu boyut özelliğine göre ayarlar.

Emission Space
: Oluşturulan parçacıkların bulunacağı geometrik uzay:
  - `World`, parçacıkları yayıcıdan bağımsız olarak hareket ettirir.
  - `Emitter`, parçacıkları yayıcıya göre hareket ettirir.

Duration
: Yayıcının kaç saniye boyunca parçacık yayacağı.

Start Delay
: Yayıcının parçacık yaymaya başlamadan önce kaç saniye bekleyeceği.

Start Offset
: Yayıcının parçacık simülasyonunda kaçıncı saniyeden başlayacağı; başka bir deyişle, efekt için ne kadar süre ön simülasyon yapacağı.

Image
: Parçacıklara doku ve animasyon uygulamak için kullanılacak görüntü dosyası (karo kaynağı veya atlas).

Animation
: *Image* dosyasından parçacıklarda kullanılacak animasyon.

Material
: Parçacıkların gölgelendirilmesinde kullanılacak materyal (material).

Blend Mode
: Kullanılabilir harmanlama modları `Alpha`, `Add` ve `Multiply` seçenekleridir.

Max Particle Count
: Bu yayıcının oluşturduğu parçacıklardan aynı anda en fazla kaç tanesinin var olabileceği.

Emitter Type
: Yayıcının şekli
  - `Circle`, bir dairenin içindeki rastgele konumlardan parçacık yayar. Parçacıklar merkezden dışarı doğru yönlendirilir. Dairenin çapı *Emitter Size X* ile tanımlanır.

  - `2D Cone`, düz bir koninin (bir üçgenin) içindeki rastgele konumlardan parçacık yayar. Parçacıklar koninin üst kısmından dışarı doğru yönlendirilir. *Emitter Size X* üst kısmın genişliğini, *Y* ise yüksekliği tanımlar.

  - `Box`, bir kutunun içindeki rastgele konumlardan parçacık yayar. Parçacıklar kutunun yerel Y ekseni boyunca yukarı doğru yönlendirilir. *Emitter Size X*, *Y* ve *Z* sırasıyla genişliği, yüksekliği ve derinliği tanımlar. 2B bir dikdörtgen için Z boyutunu sıfırda tutun.

  - `Sphere`, bir kürenin içindeki rastgele konumlardan parçacık yayar. Parçacıklar merkezden dışarı doğru yönlendirilir. Kürenin çapı *Emitter Size X* ile tanımlanır.

  - `Cone`, 3B bir koninin içindeki rastgele konumlardan parçacık yayar. Parçacıklar koninin üst diskinden dışarı doğru yönlendirilir. *Emitter Size X* üst diskin çapını, *Y* ise koninin yüksekliğini tanımlar.

  ![Yayıcı türleri](images/particlefx/emitter_types.png)

Particle Orientation
: Yayılan parçacıkların nasıl yönlendirileceği:
  - `Default`, yönelimi birim yönelime ayarlar
  - `Initial Direction`, yayılan parçacıkların başlangıç yönelimini korur.
  - `Movement Direction`, parçacıkların yönelimini hızlarına göre ayarlar.

Inherit Velocity
: Yayıcının hızının ne kadarının parçacıklara aktarılacağını belirleyen ölçek değeri. Bu değer yalnızca *Space* özelliği `World` olarak ayarlandığında kullanılabilir. Yayıcının hızı her karede tahmin edilir.

Stretch With Velocity
: Parçacıklardaki uzamayı hareket yönünde ölçeklemek için işaretleyin.

### Harmanlama modları
:[blend-modes](../shared/blend-modes.md)

## Anahtar kare atanabilen yayıcı özellikleri

Bu özelliklerin iki alanı vardır: değer ve sapma. Sapma, oluşturulan her parçacığa rastgele uygulanan bir değişimdir. Örneğin, değer 50 ve sapma 3 ise oluşturulan her parçacık 47 ile 53 arasında (50 +/- 3) bir değer alır.

![Özellik](images/particlefx/property.png)

Anahtar düğmesini işaretlediğinizde, özelliğin değeri yayıcının süresi boyunca bir eğriyle denetlenir. Anahtar kare atanmış bir özelliği sıfırlamak için anahtar düğmesinin işaretini kaldırın.

![Anahtar kare atanmış özellik](images/particlefx/key.png)

Eğriyi değiştirmek için alt görünümdeki sekmeler arasında bulunan *Curve Editor* kullanılır. Anahtar kare atanmış özellikler *Properties* görünümünde düzenlenemez; yalnızca *Curve Editor* içinde düzenlenebilir. Eğrinin şeklini değiştirmek için noktaları ve teğetleri <kbd>tıklayıp sürükleyin</kbd>. Kontrol noktaları eklemek için eğriye <kbd>çift tıklayın</kbd>. Bir kontrol noktasını kaldırmak için üzerine <kbd>çift tıklayın</kbd>.

![ParticleFX için Curve Editor](images/particlefx/curve_editor.png)

Curve Editor görünümünün yakınlaştırma düzeyini tüm eğrileri gösterecek şekilde otomatik ayarlamak için <kbd>F</kbd> tuşuna basın.

Aşağıdaki özelliklere yayıcının oynatma süresi boyunca anahtar kareler atanabilir:

Spawn Rate
: Saniyede yayılacak parçacık sayısı.

Emitter Size X/Y/Z
: Yayıcı şeklinin boyutları; yukarıdaki *Emitter Type* açıklamasına bakın.

Particle Life Time
: Oluşturulan her parçacığın saniye cinsinden yaşam süresi.

Initial Speed
: Oluşturulan her parçacığın başlangıç hızı.

Initial Size
: Oluşturulan her parçacığın başlangıç boyutu. *Size Mode* özelliğini `Automatic` olarak ayarlar ve görüntü kaynağı olarak bir kare dizisi animasyonu kullanırsanız bu özellik yok sayılır.

Initial Red/Green/Blue/Alpha
: Parçacıkların başlangıçtaki renk bileşeni çarpan değerleri.

Initial Rotation
: Parçacıkların başlangıçtaki dönme değerleri (derece cinsinden).

Initial Stretch X/Y
: Parçacıkların başlangıçtaki uzama değerleri (birim cinsinden).

Initial Angular Velocity
: Oluşturulan her parçacığın başlangıç açısal hızı (derece/saniye cinsinden).

Aşağıdaki özelliklere parçacıkların yaşam süresi boyunca anahtar kareler atanabilir:

Life Scale
: Her parçacığın yaşamı boyunca ölçek değeri.

Life Red/Green/Blue/Alpha
: Her parçacığın yaşamı boyunca renk bileşeni çarpan değeri.

Life Rotation
: Her parçacığın yaşamı boyunca dönme değeri (derece cinsinden).

Life Stretch X/Y
: Her parçacığın yaşamı boyunca uzama değeri (birim cinsinden).

Life Angular Velocity
: Her parçacığın yaşamı boyunca açısal hızı (derece/saniye cinsinden).

## Değiştiriciler

Parçacıkların hızını etkileyen dört tür değiştirici bulunur:

`Acceleration`
: Genel bir yönde ivmelenme.

`Drag`
: Parçacıkların ivmesini, parçacık hızıyla orantılı olarak azaltır.

`Radial`
: Parçacıkları bir konuma doğru çeker veya o konumdan uzağa iter.

`Vortex`
: Parçacıkları kendi konumunun etrafında dairesel veya sarmal bir yönde etkiler.

  ![Değiştiriciler](images/particlefx/modifiers.png)

## Değiştirici özellikleri

Position/Rotation
: Değiştiricinin üst öğesine göre dönüşümü.

Magnitude
: Değiştiricinin parçacıklar üzerindeki etkisinin miktarı.

Max Distance
: Parçacıkların bu değiştiriciden etkilenebileceği en uzak mesafe. Yalnızca Radial ve Vortex için kullanılır.

## Parçacık efektini denetleme

Bir betikten parçacık efektini başlatmak ve durdurmak için:

```lua
-- start the effect component "particles" in the current game object
particlefx.play("#particles")

-- stop the effect component "particles" in the current game object
particlefx.stop("#particles")
```

Bir GUI betiğinden parçacık efektini başlatma ve durdurma hakkında daha fazla bilgi için [GUI parçacık efektleri kılavuzuna](/manuals/gui-particlefx#controlling-the-effect) bakın.

::: sidenote
Bir parçacık efekti, efekt bileşeninin ait olduğu oyun nesnesi (game object) silinse bile parçacık yaymaya devam eder.
:::
Daha fazla bilgi için [Particle FX başvuru belgelerine](/ref/particlefx) bakın.

## Materyal sabitleri

Varsayılan parçacık efekti materyalinin, `particlefx.set_constant()` ile değiştirilebilen ve `particlefx.reset_constant()` ile sıfırlanabilen aşağıdaki sabitleri vardır (ayrıntılar için [Materyal kılavuzuna](/manuals/material/#vertex-and-fragment-constants) bakın):

`tint`
: Parçacık efektinin renk çarpanı (`vector4`). vector4, x, y, z ve w bileşenleri sırasıyla kırmızı, yeşil, mavi ve alfa renk çarpanlarına karşılık gelecek şekilde renk çarpanını temsil etmek için kullanılır. Bir örnek için [API başvuru belgelerine](/ref/particlefx/#particlefx.set_constant:url-constant-value) bakın.


## Proje yapılandırması

*game.project* dosyasında parçacıklarla ilgili birkaç [proje ayarı](/manuals/project-settings#particle-fx) bulunur.
