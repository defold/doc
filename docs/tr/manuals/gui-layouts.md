---
title: Defold'da GUI yerleşimleri
brief: Defold, mobil cihazlarda ekran yönelimi değişikliklerine otomatik olarak uyum sağlayan GUI'leri destekler. Bu belge, özelliğin nasıl çalıştığını açıklar.
---

# Yerleşimler

Defold, mobil cihazlarda ekran yönelimi değişikliklerine otomatik olarak uyum sağlayan grafik kullanıcı arayüzlerini (GUI) destekler. Bu özelliği kullanarak çeşitli ekran boyutlarının yönelimine ve en boy oranına uyum sağlayan GUI tasarlayabilirsiniz. Belirli cihaz modellerine uyan yerleşimler (layout) oluşturmak da mümkündür.

## Ekran profilleri oluşturma {#creating-display-profiles}

Varsayılan olarak *game.project* ayarları, ekran profilleri (display profiles) için yerleşik bir ayar dosyasının ("builtins/render/default.display_profiles") kullanılacağını belirtir. Varsayılan profiller "Landscape" (1280 piksel genişlik ve 720 piksel yükseklik) ve "Portrait" (720 piksel genişlik ve 1280 piksel yükseklik) olarak tanımlanmıştır. Profillerde herhangi bir cihaz modeli ayarlanmadığından bu profiller her cihazla eşleşir.

Yeni bir profil ayar dosyası oluşturmak için "builtins" klasöründeki dosyayı kopyalayın veya *Assets* görünümünde uygun bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Display Profiles</kbd> seçeneğini seçin. Yeni dosyaya uygun bir ad verin ve <kbd>Ok</kbd> düğmesine tıklayın.

Düzenleyici şimdi yeni dosyayı düzenlemek üzere açar. *Profiles* listesindeki <kbd>+</kbd> düğmesine tıklayarak yeni profiller ekleyin. Her profile bir *niteleyici* (qualifier) kümesi ekleyin:

Width
: Niteleyicinin piksel cinsinden genişliği.

Height
: Niteleyicinin piksel cinsinden yüksekliği.

Device Models
: Virgülle ayrılmış cihaz modelleri listesi. Cihaz modeli, cihaz modeli adının başlangıcıyla eşleştirilir; örneğin `iPhone10`, "iPhone10,\*" modelleriyle eşleşir. Virgül içeren model adları tırnak içine alınmalıdır; örneğin `"iPhone10,3", "iPhone10,6"`, iPhone X modelleriyle eşleşir ([iPhone vikisine](https://www.theiphonewiki.com/wiki/Models) bakın). `sys.get_sys_info()` çağrıldığında cihaz modeli bildiren tek platformların Android ve iOS olduğunu unutmayın. Diğer platformlar boş bir dize döndürür ve bu nedenle cihaz modeli niteleyicisi olan bir ekran profilini hiçbir zaman seçmez.

![Yeni ekran profilleri](images/gui-layouts/new_profiles.png)

Motorun yeni profillerinizi kullanması gerektiğini de belirtmeniz gerekir. *game.project* dosyasını açın ve *display* altındaki *Display Profiles* ayarında ekran profilleri dosyasını seçin:

![Ayarlar](images/gui-layouts/settings.png)

Cihaz döndürüldüğünde motorun dikey ve yatay yerleşimler arasında otomatik geçiş yapmasını istiyorsanız *Dynamic Orientation* kutusunu işaretleyin. Motor, eşleşen bir yerleşimi dinamik olarak seçer ve cihazın yönelimi değişirse seçimi de değiştirir.

### Auto Layout Selection (Display Profiles)

Display Profiles kaynağında "Auto Layout Selection" seçeneği bulunur (varsayılan olarak ON). ON olduğunda motor, hem sahne oluşturulduğunda hem de pencere/ekran boyutu değiştiğinde en iyi eşleşen GUI yerleşimini otomatik olarak seçer. OFF olduğunda motor yerleşimleri otomatik olarak değiştirmez; yerleşimler arasında elle geçiş yapmak için GUI betiğinizden `gui.set_layout()` işlevini kullanın. Bu ayar Display Profiles dosyasında saklanır ve tüm GUI sahnelerini etkiler.

## GUI yerleşimleri

Geçerli ekran profilleri kümesi, GUI düğümü (GUI node) düzeninizin yerleşim çeşitlerini oluşturmak için kullanılabilir. Bir GUI sahnesine yeni bir yerleşim eklemek için *Outline* görünümündeki *Layouts* simgesine sağ tıklayın ve <kbd>Add ▸ Layout ▸ ...</kbd> seçeneğini seçin:

![Sahneye yerleşim ekleme](images/gui-layouts/add_layout.png)

Bir GUI sahnesi düzenlenirken tüm düğümler belirli bir yerleşimde düzenlenir. O anda seçili yerleşim, araç çubuğundaki GUI sahnesi yerleşimi açılır listesinde gösterilir. Hiçbir yerleşim seçilmemişse düğümler *Default* yerleşiminde düzenlenir.

![Yerleşimler araç çubuğu](images/gui-layouts/toolbar.png)

![Dikey yerleşimi düzenleme](images/gui-layouts/portrait.png)

Bir yerleşim seçiliyken bir düğüm özelliğinde yaptığınız her değişiklik, özelliğin *Default* yerleşimindeki değerini o yerleşim için _geçersiz kılar_ (override). Geçersiz kılınan özellikler maviyle işaretlenir. Geçersiz kılınan özellikleri olan düğümler de maviyle işaretlenir. Geçersiz kılınan herhangi bir özelliği özgün değerine döndürmek için yanındaki sıfırlama düğmesine tıklayabilirsiniz.

![Yatay yerleşimi düzenleme](images/gui-layouts/landscape.png)

Bir yerleşim düğümleri silemez veya yeni düğüm oluşturamaz; yalnızca özellikleri geçersiz kılabilir. Bir düğümü bir yerleşimden kaldırmanız gerekiyorsa düğümü ekran dışına taşıyabilir veya betik mantığıyla silebilirsiniz. O anda seçili yerleşime de dikkat etmeniz önerilir. Projenize bir yerleşim eklerseniz yeni yerleşim, o anda seçili yerleşime göre ayarlanır. Ayrıca düğümler kopyalanıp yapıştırılırken, hem kopyalama *hem de* yapıştırma sırasında o anda seçili yerleşim dikkate alınır.

## Dinamik profil seçimi

Auto Layout Selection etkinleştirildiğinde motor, en iyi eşleşen yerleşimi otomatik olarak seçer. Dinamik yerleşim eşleştirmesi, her ekran profili niteleyicisine aşağıdaki kurallara göre bir puan verir:

1. Ayarlanmış bir cihaz modeli yoksa veya cihaz modeli eşleşiyorsa niteleyici için bir puan (S) hesaplanır.

2. Puan (S); ekranın alanı (A), niteleyicideki alan (A_Q), ekranın en boy oranı (R) ve niteleyicinin en boy oranı (R_Q) kullanılarak hesaplanır:

<img src="https://latex.codecogs.com/svg.latex?\inline&space;S=\left|1&space;-&space;\frac{A}{A_Q}\right|&space;&plus;&space;\left|1&space;-&space;\frac{R}{R_Q}\right|" title="S=\left|1 - \frac{A}{A_Q}\right| + \left|1 - \frac{R}{R_Q}\right|" />

3. Niteleyicinin yönelimi (yatay veya dikey) ekranla eşleşiyorsa en düşük puanlı niteleyiciye sahip profil seçilir.

4. Aynı yönelimde bir niteleyicisi olan profil bulunamazsa diğer yönelimdeki en iyi puanlı niteleyiciye sahip profil seçilir.

5. Hiçbir profil seçilemezse yedek *Default* profili kullanılır.

Daha iyi eşleşen bir yerleşim yoksa çalışma sırasında yedek olarak *Default* yerleşimi kullanılır. Bu nedenle bir "Landscape" yerleşimi eklerseniz bir "Portrait" yerleşimi de ekleyene kadar "Landscape", *tüm* yönelimler için en iyi eşleşme olur.

## Yerleşim değişikliği iletileri

Yerleşim değiştiğinde GUI bileşeninin (component) betiğine bir `layout_changed` iletisi gönderilir. Bu, motor yerleşimi otomatik olarak değiştirdiğinde (Auto Layout Selection ON) veya betiğiniz `gui.set_layout()` işlevini çağırıp yerleşim gerçekten değiştiğinde gerçekleşir. İleti, yerleşimin karma değeri alınmış tanımlayıcısını (hashed identifier) içerir; böylece betik, hangi yerleşimin seçildiğine bağlı olarak mantık çalıştırabilir:

```lua
function on_message(self, message_id, message, sender)
  if message_id == hash("layout_changed") and message.id == hash("My Landscape") then
    -- switching layout to landscape
  elseif message_id == hash("layout_changed") and message.id == hash("My Portrait") then
    -- switching layout to portrait
  end
end
```

Ayrıca görüntü oluşturma akışını yöneten geçerli işleme betiği (render script), pencere (oyun görünümü) her değiştiğinde bir ileti alır; buna yönelim değişiklikleri de dahildir.

```lua
function on_message(self, message_id, message)
  if message_id == hash("window_resized") then
    -- The window was resized. message.width and message.height contain the
    -- new dimensions of the window.
  end
end
```

Yönelim değiştiğinde GUI yerleşim yöneticisi, GUI düğümlerini yerleşiminize ve düğüm özelliklerine göre otomatik olarak ölçekler ve yeniden konumlandırır. Oyun içi içerik ise (varsayılan olarak) ayrı bir geçişte, geçerli pencereye gerilerek sığdırılan bir izdüşümle işlenir. Bu davranışı değiştirmek için kendi değiştirilmiş işleme betiğinizi sağlayın veya bir kamera [kütüphanesi](/assets/) kullanın.

## Elle yerleşim seçimi (Lua)

Kullanılan Display Profiles için Auto Layout Selection OFF olduğunda motor yerleşimleri otomatik olarak değiştirmez. Yerleşimleri elle yönetmek için bir GUI betiğinden şu işlevleri kullanın:

### gui.set_layout(layout)

- Bir dize veya karma değeri (yerleşim tanımlayıcısı) kabul eder.
- Mantıksal değer (boolean) döndürür: Yerleşim sahnede varsa ve uygulandıysa `true`; aksi durumda `false`.
- Yerleşim Display Profiles içinde varsa sahne çözünürlüğünü profilin genişliği/yüksekliğiyle günceller.
- Yerleşim gerçekten değiştiğinde `layout_changed` iletisini gönderir.

Örnek:

```lua
function init(self)
    -- Manually apply the "Portrait" layout
    local ok = gui.set_layout("Portrait")
    if not ok then
        print("Portrait layout not found in this scene")
    end
end
```

### gui.get_layouts()

- Her yerleşim tanımlayıcısının karma değerini `vmath.vector3(width, height, 0)` değerine eşleyen bir tablo döndürür.
- Varsayılan yerleşim için geçerli sahne çözünürlüğünü döndürür.

Örnek:

```lua
local layouts = gui.get_layouts()
for id, size in pairs(layouts) do
    print(id, size.x, size.y)
end
```

Not: Bir GUI yerleşimi sahnede var ama Display Profiles içinde bulunmuyorsa `gui.set_layout()`, yerleşime özgü düğüm özelliklerinin geçersiz kılınmasını yine de uygular, ancak sahne çözünürlüğünü değiştirmez.
