---
title: Defold'da GUI sahneleri
brief: Bu kılavuz Defold GUI düzenleyicisini, çeşitli GUI düğümü türlerini ve GUI betiklerini ele alır.
---

# GUI

Defold, kullanıcı arayüzlerini oluşturmak ve uygulamak için özel olarak tasarlanmış bir GUI düzenleyicisi ve güçlü betik olanakları sunar.

Defold'da grafik kullanıcı arayüzü (GUI), oluşturup bir oyun nesnesine (game object) eklediğiniz ve bir koleksiyona (collection) yerleştirdiğiniz bir bileşendir (component). Bu bileşenin özellikleri şunlardır:

* Kullanıcı arayüzünüzün çözünürlükten ve en boy oranından bağımsız olarak işlenmesini (rendering) sağlayan basit ama güçlü yerleşim özellikleri vardır.
* Bir *GUI betiği (GUI script)* aracılığıyla mantıksal davranış eklenebilir.
* (Varsayılan olarak) kamera görünümünden bağımsız biçimde diğer içeriklerin üzerinde işlenir. Böylece hareketli bir kameranız olsa bile GUI öğeleriniz ekranda sabit kalır. İşleme davranışı değiştirilebilir.

GUI bileşenleri oyun görünümünden bağımsız olarak işlenir. Bu nedenle koleksiyon düzenleyicisinde belirli bir konuma yerleştirilmez ve görsel bir gösterimleri de bulunmaz. Ancak GUI bileşenlerinin, koleksiyon içinde bir konumu olan bir oyun nesnesinde bulunması gerekir. Bu konumu değiştirmenin GUI üzerinde bir etkisi yoktur.

## GUI bileşeni oluşturma

GUI bileşenleri bir GUI sahnesi prototip dosyasından oluşturulur (diğer motorlarda "prefabs" veya "blueprints" olarak da bilinir). Yeni bir GUI bileşeni oluşturmak için *Assets* tarayıcısında bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New ▸ Gui</kbd> seçeneğini seçin. Yeni GUI dosyası için bir ad yazın ve <kbd>Ok</kbd> düğmesine basın.

![Yeni GUI dosyası](images/gui/new_gui_file.png)

Defold şimdi dosyayı otomatik olarak GUI sahne düzenleyicisinde açar.

![Yeni GUI](images/gui/new_gui.png)

*Outline* görünümü GUI'nin tüm içeriğini listeler: düğüm (node) listesini ve tüm bağımlılıklarını (aşağıya bakın).

Ortadaki düzenleme alanı GUI'yi gösterir. Düzenleme alanının sağ üst köşesindeki araç çubuğunda *Move*, *Rotate* ve *Scale* araçlarının yanı sıra bir [yerleşim](/manuals/gui-layouts) seçicisi bulunur.

![Araç çubuğu](images/gui/toolbar.png)

Beyaz bir dikdörtgen, proje ayarlarında belirlenen varsayılan ekran genişliği ve yüksekliğinde, o anda seçili yerleşimin sınırlarını gösterir.

## GUI özellikleri

*Outline* görünümünde "Gui" kök düğümünü seçtiğinizde GUI bileşeninin özellikleri *Properties* panelinde gösterilir:

*Script*
: Bu GUI bileşenine bağlı GUI betiği.

*Material*
: Bu GUI işlenirken kullanılan materyal (material). *Outline* panelinden bir GUI bileşenine birden fazla materyal ekleyip bunları tek tek düğümlere atamak da mümkündür.

*Adjust Reference*
: Her düğümün *Adjust Mode* değerinin nasıl hesaplanacağını belirler:

  - `Per Node`, her düğümü üst düğümün uyarlanmış boyutuna veya yeniden boyutlandırılmış ekrana göre uyarlar.
  - `Disable`, düğüm uyarlama modunu kapatır. Bu, tüm düğümlerin ayarlanmış boyutlarını korumasını zorunlu kılar.

*Current Nodes*
: Bu GUI'de şu anda kullanılan düğüm sayısı.

*Max Nodes*
: Bu GUI'de bulunabilecek en fazla düğüm sayısı.

*Max Dynamic Textures*
: Bu GUI bileşeninin izlediği en fazla dinamik doku sayısıdır; varsayılan değeri `128`'dir. Buna [`gui.new_texture()`](/ref/stable/gui/#gui.new_texture:texture_id-width-height-type-buffer-flip) ile oluşturulan dokular ve `go.set(..., "textures", ...)` veya `gui.set(msg.url(), "textures", ...)` ile GUI'ye atanan harici dokular dahildir. Çok sayıda harici dokuyu değiştiren projelerde bu sınırın artırılması gerekebilir.


## Çalışma sırasında değiştirme

GUI özelliklerini çalışma sırasında bir betik bileşeninden `go.get()` ve `go.set()` kullanarak değiştirebilirsiniz:

Fonts
: GUI'de kullanılan bir yazı tipini alın veya ayarlayın.

![Yazı tipini alma ve ayarlama](images/gui/get_set_font.png)

```lua
go.property("mybigfont", resource.font("/assets/mybig.font"))

function init(self)
  -- get the font file currently assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /builtins/fonts/default.font

  -- set the font with id 'default' to the font file assigned to the resource property 'mybigfont'
  go.set("#gui", "fonts", self.mybigfont, { key = "default" })

  -- get the new font file assigned to the font with id 'default'
  print(go.get("#gui", "fonts", { key = "default" })) -- /assets/mybig.font
end
```

Materials
: GUI'de kullanılan bir materyali alın veya ayarlayın.

![Materyali alma ve ayarlama](images/gui/get_set_material.png)

```lua
go.property("myeffect", resource.material("/assets/myeffect.material"))

function init(self)
  -- get the material file currently assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /effect.material

  -- set the material id 'effect' to the material file assigned to the resource property 'myeffect'
  go.set("#gui", "materials", self.myeffect, { key = "effect" })

  -- get the new material file assigned to the material with id 'effect'
  print(go.get("#gui", "materials", { key = "effect" })) -- /assets/myeffect.material
end
```

Textures
: GUI'de kullanılan bir dokuyu (atlas) alın veya ayarlayın.

![Dokuyu alma ve ayarlama](images/gui/get_set_texture.png)

```lua
go.property("mytheme", resource.atlas("/assets/mytheme.atlas"))

function init(self)
  -- get the texture file currently assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /theme.atlas

  -- set the texture with id 'theme' to the texture file assigned to the resource property 'mytheme'
  go.set("#gui", "textures", self.mytheme, { key = "theme" })

  -- get the new texture file assigned to the texture with id 'theme'
  print(go.get("#gui", "textures", { key = "theme" })) -- /assets/mytheme.atlas
end
```

## Bağımlılıklar

Defold oyunlarında kaynak ağacı sabittir; bu nedenle GUI düğümleri için gereken tüm bağımlılıkların bileşene eklenmesi gerekir. *Outline* görünümü tüm bağımlılıkları türlerine göre "klasörler" altında gruplar:

![Bağımlılıklar](images/gui/dependencies.png)

Yeni bir bağımlılık eklemek için bağımlılığı *Asset* bölmesinden düzenleyici görünümüne sürükleyip bırakın.

Alternatif olarak *Outline* görünümündeki "Gui" köküne <kbd>sağ tıklayın</kbd> ve açılan bağlam menüsünden <kbd>Add ▸ [type]</kbd> seçeneğini seçin.

Eklemek istediğiniz türün klasör simgesine <kbd>sağ tıklayıp</kbd> <kbd>Add ▸ [type]</kbd> seçeneğini de seçebilirsiniz.

## Düğüm türleri {#node-types}

GUI bileşeni bir düğüm kümesinden oluşur. Düğümler basit öğelerdir. Düzenleyicide ya da çalışma sırasında betiklerle dönüşümleri değiştirilebilir (taşınabilir, ölçeklenebilir ve döndürülebilir) ve üst-alt düğüm hiyerarşilerinde sıralanabilirler. Şu düğüm türleri bulunur:

Kutu düğümü
: ![Kutu düğümü](images/icons/gui-box-node.png){.left}
  Kutu düğümü (box node), tek bir renk, doku veya kare dizisi animasyonu (flip-book animation) içeren dikdörtgen düğümdür. Ayrıntılar için [kutu düğümü belgelerine](/manuals/gui-box) bakın.

<div style="clear: both;"></div>

Metin düğümü
: ![Metin düğümü](images/icons/gui-text-node.png){.left}
  Metin düğümü (text node), metin gösterir. Ayrıntılar için [metin düğümü belgelerine](/manuals/gui-text) bakın.

<div style="clear: both;"></div>

Daire dilimi düğümü
: ![Daire dilimi düğümü](images/icons/gui-pie-node.png){.left}
  Daire dilimi düğümü (pie node), kısmen doldurulabilen veya ters çevrilebilen, daire ya da elipsoit biçiminde bir düğümdür. Ayrıntılar için [daire dilimi düğümü belgelerine](/manuals/gui-pie) bakın.

<div style="clear: both;"></div>

Şablon düğümü
: ![Şablon düğümü](images/icons/gui.png){.left}
  Şablon düğümleri (template node), başka GUI sahne dosyalarına dayalı örnekler (instance) oluşturmak için kullanılır. Ayrıntılar için [şablon düğümü belgelerine](/manuals/gui-template) bakın.

<div style="clear: both;"></div>

ParticleFX düğümü
: ![ParticleFX düğümü](images/icons/particlefx.png){.left}
  Bir parçacık efekti oynatır. Ayrıntılar için [ParticleFX düğümü belgelerine](/manuals/gui-particlefx) bakın.

<div style="clear: both;"></div>

Düğüm eklemek için *Nodes* klasörüne sağ tıklayın ve önce <kbd>Add ▸</kbd>, ardından <kbd>Box</kbd>, <kbd>Text</kbd>, <kbd>Pie</kbd>, <kbd>Template</kbd> veya <kbd>ParticleFx</kbd> seçeneğini seçin.

![Düğüm ekleme](images/gui/add_node.png)

<kbd>A</kbd> tuşuna basıp GUI'ye eklemek istediğiniz türü de seçebilirsiniz.

## Düğüm özellikleri {#node-properties}

Her düğümün, görünümünü belirleyen kapsamlı bir özellik kümesi vardır:

Id
: Düğümün kimliği. Bu ad, GUI sahnesi içinde benzersiz olmalıdır.

Position, Rotation ve Scale
: Düğümün konumunu, yönelimini ve esnemesini belirler. Bu değerleri değiştirmek için *Move*, *Rotate* ve *Scale* araçlarını kullanabilirsiniz. Değerlere betikle animasyon uygulanabilir ([daha fazla bilgi](/manuals/property-animation)).

Size (kutu, metin ve daire dilimi düğümleri)
: Düğümün boyutu varsayılan olarak otomatiktir, ancak *Size Mode* değerini `Manual` olarak ayarlayarak boyutu değiştirebilirsiniz. Boyut, düğümün sınırlarını tanımlar ve girdiyle düğüm seçerken kullanılır. Bu değere betikle animasyon uygulanabilir ([daha fazla bilgi](/manuals/property-animation)).

Size Mode (kutu ve daire dilimi düğümleri)
: `Automatic` olarak ayarlandığında düzenleyici düğümün boyutunu belirler. `Manual` olarak ayarlandığında boyutu kendiniz belirleyebilirsiniz.

Enabled
: İşaretli değilse düğüm işlenmez, düğüme animasyon uygulanmaz ve düğüm `gui.pick_node()` ile seçilemez. Bu özelliği program yoluyla değiştirmek ve kontrol etmek için `gui.set_enabled()` ve `gui.is_enabled()` kullanın.

Visible
: İşaretli değilse düğüm işlenmez; ancak düğüme animasyon uygulanabilir ve düğüm `gui.pick_node()` ile seçilebilir. Bu özelliği program yoluyla değiştirmek ve kontrol etmek için `gui.set_visible()` ve `gui.get_visible()` kullanın.

Text (metin düğümleri)
: Düğümde gösterilecek metin.

Line Break (metin düğümleri)
: Metnin düğüm genişliğine göre satırlara kaydırılması için işaretleyin.

Font (metin düğümleri)
: Metin işlenirken kullanılacak yazı tipi.

Texture (kutu ve daire dilimi düğümleri)
: Düğüm üzerine çizilecek doku. Bu, bir atlas veya karo kaynağındaki (tile source) görüntüye ya da animasyona başvurudur.

Material (kutu, daire dilimi, metin ve particlefx düğümleri)
: Düğüm çizilirken kullanılacak materyal. *Outline* görünümünün Materials bölümüne eklenmiş bir materyal seçilebilir veya GUI bileşenine atanmış varsayılan materyali kullanmak için boş bırakılabilir.

Slice 9 (kutu düğümleri)
: Düğüm yeniden boyutlandırıldığında, düğümün dokusunun kenarlarındaki piksel boyutunu korumak için ayarlayın. Ayrıntılar için [kutu düğümü belgelerine](/manuals/gui-box) bakın.

Inner Radius (daire dilimi düğümleri)
: Düğümün X ekseni boyunca ifade edilen iç yarıçapı. Ayrıntılar için [daire dilimi düğümü belgelerine](/manuals/gui-pie) bakın.

Outer Bounds (daire dilimi düğümleri)
: Dış sınırların davranışını belirler. Ayrıntılar için [daire dilimi düğümü belgelerine](/manuals/gui-pie) bakın.

Perimeter Vertices (daire dilimi düğümleri)
: Şekli oluşturmak için kullanılacak parça sayısı. Ayrıntılar için [daire dilimi düğümü belgelerine](/manuals/gui-pie) bakın.

Pie Fill Angle (daire dilimi düğümleri)
: Daire diliminin ne kadarının doldurulacağı. Ayrıntılar için [daire dilimi düğümü belgelerine](/manuals/gui-pie) bakın.

Template (şablon düğümleri)
: Düğüm için şablon olarak kullanılacak GUI sahne dosyası. Ayrıntılar için [şablon düğümü belgelerine](/manuals/gui-template) bakın.

ParticleFX (particlefx düğümleri)
: Bu düğümde kullanılacak parçacık efekti. Ayrıntılar için [ParticleFX düğümü belgelerine](/manuals/gui-particlefx) bakın.

Color
: Düğümün rengi. Düğüm dokuluysa renk, dokuya renk çarpanı olarak uygulanır. Renge betikle animasyon uygulanabilir ([daha fazla bilgi](/manuals/property-animation)).

Alpha
: Düğümün saydamlığı. Alfa değerine betikle animasyon uygulanabilir ([daha fazla bilgi](/manuals/property-animation)).

Inherit Alpha
: Bu onay kutusunu işaretlemek, düğümün üst düğümün alfa değerini devralmasını sağlar. Düğümün alfa değeri, üst düğümün alfa değeriyle çarpılır.

Leading (metin düğümleri)
: Satır aralığı için ölçekleme katsayısı. `0` değeri satır aralığı bırakmaz. `1` (varsayılan değer) normal satır aralığı sağlar.

Tracking (metin düğümleri)
: Harf aralığı için ölçekleme katsayısı. Varsayılan değeri 0'dır.

Layer
: Düğüme bir katman (layer) atandığında normal çizim sırasının yerine katman sırası kullanılır. Ayrıntılar için aşağıya bakın.

Blend mode
: Düğümün grafiklerinin arka plan grafikleriyle nasıl harmanlanacağını belirler:
  - `Alpha`, düğümün piksel değerlerini arka planla alfa harmanlaması kullanarak birleştirir. Bu, grafik yazılımlarındaki "Normal" harmanlama moduna karşılık gelir.
  - `Add`, düğümün piksel değerlerini arka plan değerlerine ekler. Bu, bazı grafik yazılımlarındaki "Linear dodge" moduna karşılık gelir.
  - `Multiply`, düğümün piksel değerlerini arka plan değerleriyle çarpar.
  - `Screen`, düğümün piksel değerlerini arka plan değerleriyle ters çarpar. Bu, grafik yazılımlarındaki "Screen" harmanlama moduna karşılık gelir.

Pivot
: Düğümün dayanak noktasını (pivot) belirler. Bu nokta, düğümün "merkez noktası" olarak düşünülebilir. Her türlü döndürme, ölçekleme veya boyut değişikliği bu noktanın çevresinde gerçekleşir.

  Olası değerler `Center`, `North`, `South`, `East`, `West`, `North West`, `North East`, `South West` veya `South East` değerleridir.

  ![Dayanak noktası](images/gui/pivot.png)

  Düğümün dayanak noktasını değiştirirseniz düğüm, yeni dayanak noktası düğümün konumunda olacak şekilde taşınır. Metin düğümleri, `Center` metni ortaya, `West` sola ve `East` sağa hizalayacak şekilde hizalanır.

X Anchor, Y Anchor
: Sabitleme (anchoring), sahne sınırları veya üst düğümün sınırları fiziksel ekran boyutuna sığacak şekilde esnetildiğinde düğümün dikey ve yatay konumunun nasıl değişeceğini belirler.

  ![Sabitleme uygulanmadan önce](images/gui/anchoring_unadjusted.png)

  Şu sabitleme modları kullanılabilir:

  - `None` (hem *X Anchor* hem de *Y Anchor* için), düğümün üst düğümün veya sahnenin merkezine göre konumunu, bunların *uyarlanmış* boyutuna oranla korur.
  - `Left` veya `Right` (*X Anchor*), düğümün yatay konumunu ölçekleyerek üst düğümün veya sahnenin sol ve sağ kenarlarına göre konumunu aynı yüzdede tutar.
  - `Top` veya `Bottom` (*Y Anchor*), düğümün dikey konumunu ölçekleyerek üst düğümün veya sahnenin üst ve alt kenarlarına göre konumunu aynı yüzdede tutar.

  ![Sabitleme](images/gui/anchoring.png)

Adjust Mode
: Düğümün uyarlama modunu (adjust mode) belirler. Uyarlama modu ayarı, sahne sınırları veya üst düğümün sınırları fiziksel ekran boyutuna sığacak şekilde uyarlandığında düğüme ne olacağını belirler.

  Mantıksal çözünürlüğün tipik bir yatay ekran çözünürlüğü olduğu sahnede oluşturulmuş bir düğüm:

  ![Uyarlanmamış](images/gui/unadjusted.png)

  Sahneyi dikey bir ekrana sığdırmak, sahnenin esnetilmesine neden olur. Her düğümün sınırlayıcı kutusu da benzer şekilde esnetilir. Ancak uyarlama modu ayarlanarak düğüm içeriğinin en boy oranı korunabilir. Şu modlar kullanılabilir:

  - `Fit`, düğüm içeriğini esnetilmiş sınırlayıcı kutunun genişliği veya yüksekliğinden küçük olanına eşit olacak şekilde ölçekler. Başka bir deyişle içerik, düğümün esnetilmiş sınırlayıcı kutusunun içine sığar.
  - `Zoom`, düğüm içeriğini esnetilmiş sınırlayıcı kutunun genişliği veya yüksekliğinden büyük olanına eşit olacak şekilde ölçekler. Başka bir deyişle içerik, düğümün esnetilmiş sınırlayıcı kutusunu tamamen kaplar.
  - `Stretch`, düğüm içeriğini düğümün esnetilmiş sınırlayıcı kutusunu dolduracak şekilde esnetir.

  ![Uyarlama modları](images/gui/adjusted.png)

  GUI sahnesinin *Adjust Reference* özelliği `Disabled` olarak ayarlanmışsa bu ayar yok sayılır.

Clipping Mode (kutu ve daire dilimi düğümleri)
: Düğümün kırpma modunu belirler:

  - `None`, düğümü her zamanki gibi işler.
  - `Stencil`, düğümün sınırlarının, düğümün alt düğümlerini kırpmak için kullanılan bir şablon maskesi tanımlamasını sağlar.

  Ayrıntılar için [GUI kırpma kılavuzuna](/manuals/gui-clipping) bakın.

Clipping Visible (kutu ve daire dilimi düğümleri)
: Düğümün içeriğini şablon alanında işlemek için işaretleyin. Ayrıntılar için [GUI kırpma kılavuzuna](/manuals/gui-clipping) bakın.

Clipping Inverted (kutu ve daire dilimi düğümleri)
: Şablon maskesini ters çevirir. Ayrıntılar için [GUI kırpma kılavuzuna](/manuals/gui-clipping) bakın.


## Pivot, Anchors ve Adjust Mode

Pivot, Anchors ve Adjust Mode özelliklerinin birleşimi, GUI tasarımında büyük esneklik sağlar; ancak somut bir örneğe bakmadan bunların birlikte nasıl çalıştığını anlamak biraz zor olabilir. 640x1136 boyutunda bir ekran için oluşturulmuş bu GUI taslağını örnek alalım:

![](images/gui/adjustmode_example_original.png)

Kullanıcı arayüzü, X ve Y Anchors değerleri None olarak ayarlanarak oluşturulmuştur ve her düğümün Adjust Mode ayarı, varsayılan Fit değerinde bırakılmıştır. Üst panelin Pivot noktası North, alt panelinki South, üst paneldeki çubukların dayanak noktaları ise West olarak ayarlanmıştır. Diğer düğümlerin dayanak noktaları Center olarak ayarlanmıştır. Pencereyi daha geniş olacak şekilde yeniden boyutlandırırsak şu sonuç ortaya çıkar:

![](images/gui/adjustmode_example_resized.png)

Peki, üst ve alt çubukların her zaman ekran kadar geniş olmasını istersek ne yapabiliriz? Üstteki ve alttaki gri arka plan panellerinin Adjust Mode değerini Stretch olarak değiştirebiliriz:

![](images/gui/adjustmode_example_resized_stretch.png)

Bu daha iyi oldu. Gri arka plan panelleri artık her zaman pencere genişliğine kadar esnetilir; ancak üst paneldeki çubuklar ve alttaki iki kutu doğru konumlandırılmamıştır. Üstteki çubukların solda kalmasını istiyorsak X Anchor değerini None yerine Left olarak değiştirmemiz gerekir:

![](images/gui/adjustmode_example_top_anchor_left.png)

Üst panel için tam olarak istediğimiz sonuç budur. Üst paneldeki çubukların Pivot noktaları zaten West olarak ayarlanmıştı. Bu nedenle çubuklar, sol/batı kenarları (Pivot) üst panelin sol kenarına (X Anchor) sabitlenmiş olarak düzgün biçimde konumlanır.

Şimdi soldaki kutunun X Anchor değerini Left, sağdaki kutunun X Anchor değerini Right olarak ayarlarsak şu sonucu elde ederiz:

![](images/gui/adjustmode_example_bottom_anchor_left_right.png)

Bu, tam olarak beklenen sonuç değildir. İki kutunun, üst paneldeki iki çubuk gibi sol ve sağ kenarlara yakın kalması gerekir. Bunun nedeni Pivot noktasının yanlış olmasıdır:

![](images/gui/adjustmode_example_bottom_pivot_center.png)

Her iki kutunun Pivot noktası da Center olarak ayarlanmıştır. Bu, ekran genişlediğinde kutuların merkez noktasının (dayanak noktasının) kenarlardan aynı oransal uzaklıkta kalacağı anlamına gelir. Soldaki kutu, ilk 640x1136 boyutundaki pencerede sol kenardan %17 uzaklıktaydı:

![](images/gui/adjustmode_example_original_ratio.png)

Ekran yeniden boyutlandırıldığında soldaki kutunun merkez noktası sol kenardan yine %17 uzaklıkta kalır:

![](images/gui/adjustmode_example_resized_stretch_ratio.png)

Pivot noktasını soldaki kutu için Center yerine West, sağdaki kutu için de East olarak değiştirip kutuları yeniden konumlandırırsak ekran yeniden boyutlandırıldığında bile istediğimiz sonucu elde ederiz:

![](images/gui/adjustmode_example_bottom_pivot_west_east.png)


## Çizim sırası

Tüm düğümler "Nodes" klasörü altında listelendikleri sırayla işlenir. Listenin en üstündeki düğüm önce çizilir ve bu nedenle diğer tüm düğümlerin arkasında görünür. Listedeki son düğüm en son çizilir; yani diğer tüm düğümlerin önünde görünür. Bir düğümün Z değerini değiştirmek, çizim sırasını belirlemez; ancak Z değerini işleme betiğinizin işleme aralığı dışında bir değere ayarlarsanız düğüm artık ekrana işlenmez. Düğümlerin indeks sıralamasını katmanlarla geçersiz kılabilirsiniz (aşağıya bakın).

![Çizim sırası](images/gui/draw_order.png)

Düğümü yukarı veya aşağı taşıyarak indeks sırasını değiştirmek için bir düğüm seçin ve <kbd>Alt + Up/Down</kbd> tuşlarına basın.

Çizim sırası betikte değiştirilebilir:

```lua
local bean_node = gui.get_node("bean")
local shield_node = gui.get_node("shield")

if gui.get_index(shield_node) < gui.get_index(bean_node) then
  gui.move_above(shield_node, bean_node)
end
```

## Üst-alt düğüm hiyerarşileri

Bir düğümü başka bir düğümün alt düğümü yapmak için onu, üst düğümü olmasını istediğiniz düğümün üzerine sürükleyin. Üst düğümü olan bir düğüm, üst düğümün dayanak noktasına göre üst düğüme uygulanan dönüşümü (konum, dönme ve ölçek) devralır.

![Üst ve alt düğüm](images/gui/parent_child.png)

Üst düğümler alt düğümlerinden önce çizilir. Üst ve alt düğümlerin çizim sırasını değiştirmek ve düğümlerin işlenmesini optimize etmek için katmanları kullanın (aşağıya bakın).


## Katmanlar ve çizim çağrıları {#layers-and-draw-calls}

Katmanlar, düğümlerin nasıl çizileceği üzerinde ayrıntılı denetim sağlar ve motorun bir GUI sahnesini çizmek için oluşturması gereken çizim çağrılarının (draw call) sayısını azaltmak için kullanılabilir. Motor, bir GUI sahnesinin düğümlerini çizerken bunları aşağıdaki koşullara göre çizim çağrısı gruplarında toplar:

- Düğümler aynı türde olmalıdır.
- Düğümler aynı atlası veya karo kaynağını kullanmalıdır.
- Düğümler aynı harmanlama moduyla işlenmelidir.
- Aynı yazı tipini kullanmalıdırlar.

Bir düğüm bu noktalardan herhangi birinde önceki düğümden farklıysa grubu böler ve başka bir çizim çağrısı oluşturur. Kırpma düğümleri her zaman grubu böler; her şablon kapsamı da grubu böler.

Düğümleri hiyerarşilerde düzenleyebilmek, düğümleri yönetilebilir birimler halinde gruplamayı kolaylaştırır. Ancak farklı düğüm türlerini karıştırırsanız hiyerarşiler toplu çizimi (batch rendering) bölebilir:

![Toplu çizimi bölen hiyerarşi](images/gui/break_batch.png)

İşleme hattı düğüm listesinde ilerlerken, türleri farklı olduğu için her düğüm için ayrı bir grup oluşturmak zorunda kalır. Sonuç olarak bu üç düğme toplam altı çizim çağrısı gerektirir.

Düğümlere katmanlar atayarak düğümleri farklı bir sıraya koyabilirsiniz; böylece işleme hattı düğümleri daha az çizim çağrısında gruplayabilir. Önce gereken katmanları sahneye ekleyin. *Outline* görünümündeki "Layers" klasör simgesine <kbd>sağ tıklayın</kbd> ve <kbd>Add ▸ Layer</kbd> seçeneğini seçin. Yeni katmanı seçin ve *Properties* görünümünde *Name* özelliğine bir değer atayın.

![Katmanlar](images/gui/layers.png)

Ardından her düğümün *Layer* özelliğini ilgili katmana ayarlayın. Katman çizim sırası, normal indeksli düğüm sırasından önce gelir; bu nedenle düğme grafiklerini oluşturan kutu düğümlerini "graphics", düğme metin düğümlerini ise "text" katmanına ayarlamak şu çizim sırasını oluşturur:

* Önce "graphics" katmanındaki tüm düğümler, en üstten başlayarak:

  1. "button-1"
  2. "button-2"
  3. "button-3"

* Ardından "text" katmanındaki tüm düğümler, en üstten başlayarak:

  4. "button-text-1"
  5. "button-text-2"
  6. "button-text-3"

Düğümler artık altı yerine iki çizim çağrısında gruplanabilir. Büyük bir performans kazanımı!

Katmanı ayarlanmamış bir alt düğümün, üst düğümünün katman ayarını örtük olarak devraldığını unutmayın. Bir düğümün katmanını ayarlamamak, onu örtük olarak diğer tüm katmanlardan önce çizilen "null" katmanına ekler.
