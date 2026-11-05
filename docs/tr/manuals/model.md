---
title: Defold'da 3B modeller
brief: Bu kılavuz, 3B modelleri, iskeletleri ve animasyonları oyununuza nasıl aktaracağınızı açıklar.
---

# Model bileşeni {#model-component}

Defold temelde bir 3B motordur. Yalnızca 2B içerikle çalışırken bile tüm işleme (rendering) 3B olarak yapılır, ancak ekrana ortografik izdüşümle yansıtılır. Defold, 3B varlıkları (asset), yani _modelleri_ (model) koleksiyonlarınıza (collection) ekleyerek tamamen 3B içerik kullanmanıza olanak tanır. Yalnızca 3B varlıklarla tamamen 3B oyunlar geliştirebilir veya 3B ve 2B içeriği istediğiniz gibi birleştirebilirsiniz.

## Model bileşeni oluşturma {#creating-a-model-component}

Model bileşenleri (model component), diğer oyun nesnesi (game object) bileşenleri gibi oluşturulur. Bunu iki şekilde yapabilirsiniz:

- *Assets* tarayıcısında bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Model</kbd> seçeneğini seçerek bir *Model dosyası* oluşturun.
- *Outline* görünümünde bir oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Model</kbd> seçeneğini seçerek bileşeni doğrudan oyun nesnesine gömülü olarak oluşturun.

![Oyun nesnesindeki model](images/model/model_gltf.png)

Modeli oluşturduktan sonra bazı özellikleri belirtmeniz gerekir:

### Model özellikleri {#model-properties}

*Id*, *Position* ve *Rotation* özelliklerine ek olarak bileşene özgü şu özellikler bulunur:

*Scene*
: Modelin geometrisini içeren glTF *.gltf* veya *.glb* dosyası. Dosya biçim hedefleri (morph target) içeriyorsa bunlar sahneyle birlikte içe aktarılır. Bu özelliğin önceki adı *Mesh* idi.

*Mesh*
: Seçili *Scene* içindeki isteğe bağlı, adlandırılmış bir örgü (mesh). Sahnenin tamamını içe aktarılan dönüşümleriyle işlemek için bu alanı boş bırakın. Bir örgüyü glTF düğüm dönüşümleri olmadan kendi yerel koordinatlarında bir kez işlemek için o örgüyü seçin. Seçilen örgüyü yerleştirmek için model bileşenini veya oyun nesnesini konumlandırın, döndürün ve ölçekleyin.

*Create GO Bones*
: Modelin her kemiği için bir oyun nesnesi oluşturmak üzere bu seçeneği işaretleyin. Bu oyun nesnelerini, örneğin silah gibi başka oyun nesnelerini el kemiklerine bağlamak için kullanabilirsiniz. 

*Skeleton*
: Bu özelliğin, animasyonda kullanılacak iskeleti (skeleton) içeren glTF *.gltf* veya *.glb* dosyasına başvurması önerilir. Defold'un hiyerarşinizde tek bir kök kemik gerektirdiğini unutmayın.

*Animations*
: Bunu, modelde kullanmak istediğiniz animasyonları içeren *Animation Set File* dosyasına ayarlayın.

*Default Animation*
: Animasyon kümesinden (animation set) seçilen ve modelde otomatik olarak oynatılacak animasyondur.

Yukarıdaki özelliklere ek olarak modelin her örgüsüne bir materyal (material) atamak için bir alan da bulunur:

*Material*
: Bu özelliği modele uygun bir materyale ayarlayın. glTF materyal özelliklerini fiziksel tabanlı işlemek için yerleşik bir `gltf` materyali, genel model gölgelendirmesi için yerleşik bir `model` materyali veya kendi özel materyalinizi kullanın. [Aşağıdaki materyal çeşitlerine](#material) ve [PBR kılavuzuna](/manuals/physically-based-rendering/#built-in-pbr-materials) bakın.

Materyale bağlı olarak bir veya daha fazla doku (texture) özelliği bulunur:

*Texture*
: Bu özellik, nesneye uygulanmasını istediğiniz doku görüntüsünü göstermelidir. Görüntü, ayrı bir proje varlığı veya *Assets* panelinde bir glTF ya da GLB dosyasının altında sunulan gömülü bir görüntü olabilir.

Bir glTF veya GLB *Scene* seçildiğinde ya da *Mesh* seçimi değiştirildiğinde materyal ve doku eşlemelerini doldurma önerilebilir. <kbd>Auto Fill</kbd>, mevcut eşlemeleri kaynaktakilerle değiştirir; <kbd>Keep Current</kbd>, yeni sahne veya örgü seçimini uygularken eşlemelerinizi korur. [Model içe aktarma iş akışına](/manuals/importing-models/#using-a-model) bakın.


## Düzenleyicide değiştirme {#editor-manipulation}

Model bileşenini ekledikten sonra standart *Scene Editor* araçlarıyla bileşeni ve/veya onu içeren oyun nesnesini düzenleyip değiştirebilir, modeli istediğiniz gibi taşıyabilir, döndürebilir ve ölçekleyebilirsiniz.

## Çalışma sırasında değiştirme {#runtime-manipulation}

Modelleri çalışma sırasında çeşitli işlevler ve özellikler aracılığıyla değiştirebilirsiniz (kullanım için [API belgelerine](/ref/model/) bakın).

![Oyun içinde Wiggler](images/model/runtime.png)

### Çalışma sırasında animasyon {#runtime-animation}

Defold, animasyonu çalışma sırasında kontrol etmek için güçlü destek sunar. [Model animasyonu kılavuzunda](/manuals/model-animation) daha fazla bilgi bulabilirsiniz:

```lua
local play_properties = { blend_duration = 0.1 }
model.play_anim("#model", "jump", go.PLAYBACK_ONCE_FORWARD, play_properties)
```

Animasyon oynatma imleci, elle veya özellik animasyonu (property animation) sistemi aracılığıyla canlandırılabilir:

```lua
-- set the run animation
model.play_anim("#model", "run", go.PLAYBACK_NONE)
-- animate the cursor
go.animate("#model", "cursor", go.PLAYBACK_LOOP_PINGPONG, 1, go.EASING_LINEAR, 10)
```

Modeller glTF biçim hedefi animasyonlarını da kullanabilir. Biçim hedefi ağırlıklarına diğer model animasyonlarında olduğu gibi `model.play_anim()` ile animasyon uygulanır. Bu ağırlıklar çalışma sırasında [`model.get_blend_weights()`](/ref/model#model.get_blend_weights) ve [`model.set_blend_weights()`](/ref/model#model.set_blend_weights) kullanılarak okunabilir veya geçersiz kılınabilir. Ayrıntılar için model animasyonu kılavuzundaki [biçim hedefleri bölümüne](/manuals/model-animation#morph-targets) bakın.

### Özellikleri değiştirme {#changing-properties}

Bir modelin `go.get()` ve `go.set()` kullanılarak değiştirilebilen çeşitli özellikleri de vardır:

`animation`
: Geçerli model animasyonu (`hash`) (SALT OKUNUR). Animasyonu `model.play_anim()` kullanarak değiştirirsiniz (yukarıya bakın).

`cursor`
: Normalleştirilmiş animasyon imleci (`number`).

`material`
: Modelin materyali (`hash`). Bunu bir materyal kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Bir örnek için [API başvuru belgelerine](/ref/model/#material) bakın.

`playback_rate`
: Animasyon oynatma hızı (`number`).

`textureN`
: N değeri 0-15 arasında olan model dokuları (`hash`). Bu özellikleri `go.get()` ile okuyabilir, bir doku kaynak özelliği ve `go.set()` kullanarak değiştirebilirsiniz. Defold, çizim başına en fazla 16 dokuyu destekler; ancak doku örnekleyici sınırı daha düşük olan grafik bağdaştırıcılarında bir gölgelendiricinin (shader) kullanabileceği sayı daha az olabilir.


## Materyal {#material}

3B yazılımlar genellikle nesnenizin köşelerinde (vertex) renklendirme ve doku kaplama gibi özellikler ayarlamanıza olanak tanır. Bu bilgiler, 3B yazılımınızdan dışa aktardığınız glTF *.gltf* veya *.glb* dosyasına yazılır. Oyununuzun gereksinimlerine bağlı olarak nesneleriniz için uygun ve _iyi performans gösteren_ materyaller seçmeniz ve/veya oluşturmanız gerekir. Bir materyal, _gölgelendirici programlarını_ (shader program) nesnenin işlenmesi için kullanılan bir dizi parametreyle birleştirir.

Aşağıdaki yerleşik materyaller `/builtins/materials/` altında bulunur:

| Model türü | Genel model gölgelendirmesi | glTF PBR gölgelendirmesi |
|---|---|---|
| Statik, örnek oluşturma kullanılmayan | `model.material` | `gltf.material` |
| Statik, örnek oluşturma kullanılan | `model_instanced.material` | `gltf_instanced.material` |
| İskelete bağlı (animasyonlu), örnek oluşturma kullanılmayan | `model_skinned.material` | `gltf_skinned.material` |
| İskelete bağlı (animasyonlu), örnek oluşturma kullanılan | `model_skinned_instanced.material` | `gltf_skinned_instanced.material` |

`gltf` materyalleri, içe aktarılan glTF materyal verilerini kullanarak yerleşik metaliklik/pürüzlülük aydınlatması sağlar. Doku eşlemeleri, ışıklar ve özel gölgelendiriciler için [PBR kılavuzuna](/manuals/physically-based-rendering/#built-in-pbr-materials) bakın.

Bu yerleşik materyallerin tümü yerel köşe uzayını (local vertex space) kullanır. İskelete bağlı modellerde yerel köşe uzayı, köşe gölgelendiricisinin bir kemik matrisi dokusu kullanarak GPU üzerinde iskelete bağlama (skinning) işlemini gerçekleştirmesini sağlar; model örneği oluşturma işlemi için de yerel köşe uzayı gereklidir. Bu nedenle, GPU üzerinde iskelete bağlanan veya örnek oluşturma kullanılan modeller için tasarlanan özel bir materyalin *Local* köşe uzayı ayarını kullanması önerilir.

Kemik matrisi önbelleği bir `RGBA32F` dokusu kullanır. Etkin grafik bağdaştırıcısı bu doku biçimini desteklemiyorsa Defold, yerel uzay materyali kullanan animasyonlu bir Model bileşeni oluşturamaz. Bu nedenle OpenGL ES 2.0 ve WebGL 1.0 üzerindeki destek, bağdaştırıcının kayan noktalı doku uzantısına bağlıdır. Bu uzantıya sahip olmayan bir bağdaştırıcıyla uyumluluk için, CPU üzerinde iskelete bağlama yapan ve model örneği oluşturmayı desteklemeyen özel bir dünya uzayı materyali kullanın. Önbellek boyutları [Model proje ayarları](/manuals/project-settings/#model) ile ayarlanabilir.

Modelleriniz için özel materyaller oluşturmanız gerekiyorsa bilgi için [Materyal belgelerine](/manuals/material) bakın. [Gölgelendirici kılavuzu](/manuals/shader), gölgelendirici programlarının nasıl çalıştığı hakkında bilgi içerir.


### Materyal sabitleri {#material-constants}

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: Modelin renk çarpanı (`vector4`). Renk çarpanı `vector4` ile temsil edilir; x, y, z ve w sırasıyla kırmızı, yeşil, mavi ve alfa renk çarpanlarına karşılık gelir.


## İşleme {#rendering}

Varsayılan işleme betiği (render script), yerleşik model ve glTF materyalleri dahil, `model` etiketine sahip materyalleri çizer. Bunları özel bir işleme betiğinde işlemek için eşleşen bir yüklem (predicate) oluşturun ve sahnenize uygun görünüm ve izdüşümle çizin. Örneğin:

  ```lua

  function init(self)
    self.model_pred = render.predicate({"model"})
    ...
  end

  function update()
    ...
    render.set_depth_mask(true)
    render.enable_state(graphics.STATE_DEPTH_TEST)
    render.set_projection(stretch_projection(-1000, 1000))  -- orthographic
    render.draw(self.model_pred)
    render.set_depth_mask(false)
    ...
  end
  ```

İşleme betiklerinin nasıl çalıştığına ilişkin ayrıntılar için [İşleme belgelerine](/manuals/render) bakın.
