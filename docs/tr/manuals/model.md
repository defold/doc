---
title: Defold'da 3B modeller
brief: Bu kılavuz, 3B modelleri, iskeletleri ve animasyonları oyununuza nasıl aktaracağınızı açıklar.
---

# Model bileşeni

Defold temelde bir 3B motordur. Yalnızca 2B içerikle çalışırken bile tüm işleme (rendering) 3B olarak yapılır, ancak ekrana ortografik izdüşümle yansıtılır. Defold, 3B varlıkları (asset), yani _modelleri_ (model) koleksiyonlarınıza (collection) ekleyerek tamamen 3B içerik kullanmanıza olanak tanır. Yalnızca 3B varlıklarla tamamen 3B oyunlar geliştirebilir veya 3B ve 2B içeriği istediğiniz gibi birleştirebilirsiniz.

## Model bileşeni oluşturma

Model bileşenleri (model component), diğer oyun nesnesi (game object) bileşenleri gibi oluşturulur. Bunu iki şekilde yapabilirsiniz:

- *Assets* tarayıcısında bir konuma <kbd>sağ tıklayın</kbd> ve <kbd>New... ▸ Model</kbd> seçeneğini seçerek bir *Model dosyası* oluşturun.
- *Outline* görünümünde bir oyun nesnesine <kbd>sağ tıklayın</kbd> ve <kbd>Add Component ▸ Model</kbd> seçeneğini seçerek bileşeni doğrudan oyun nesnesine gömülü olarak oluşturun.

![Oyun nesnesindeki model](images/model/model_gltf.png)

Modeli oluşturduktan sonra bazı özellikleri belirtmeniz gerekir:

### Model özellikleri {#model-properties}

*Id*, *Position* ve *Rotation* özelliklerine ek olarak bileşene özgü şu özellikler bulunur:

*Scene*
: Modelin geometrisini içeren glTF *.gltf* veya *.glb* dosyası. Dosya biçim hedefleri (morph target) içeriyorsa bunlar sahneyle birlikte içe aktarılır. Bu özelliğin adı Defold 1.13.2 öncesinde *Mesh* idi.

*Mesh*
: Seçili *Scene* içindeki isteğe bağlı, adlandırılmış bir örgü (mesh); Defold 1.13.2 sürümünden beri kullanılabilir. Sahnenin tamamını içe aktarılan dönüşümleriyle işlemek için bu alanı boş bırakın. Bir örgüyü glTF düğüm dönüşümleri olmadan kendi yerel koordinatlarında bir kez işlemek için o örgüyü seçin. Seçilen örgüyü yerleştirmek için model bileşenini veya oyun nesnesini konumlandırın, döndürün ve ölçekleyin.

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
: Bu özellik için dokulu bir 3B nesneye uygun olacak şekilde oluşturduğunuz bir materyal seçin. Başlangıç noktası olarak kullanabileceğiniz birkaç yerleşik materyal vardır:

  * Örnek oluşturma (instancing) kullanılmayan statik modeller için *model.material* kullanın
  * Örnek oluşturma kullanılan statik modeller için *model_instanced.material* kullanın
  * İskelete bağlı (animasyonlu), örnek oluşturma kullanılmayan modeller için *model_skinned.material* kullanın
  * İskelete bağlı (animasyonlu), örnek oluşturma kullanılan modeller için *model_skinned_instanced.material* kullanın

Materyale bağlı olarak bir veya daha fazla doku (texture) özelliği bulunur:

*Texture*
: Bu özelliğin, nesneye uygulamak istediğiniz doku görüntüsü dosyasını göstermesi önerilir.


## Düzenleyicide değiştirme

Model bileşenini ekledikten sonra standart *Scene Editor* araçlarıyla bileşeni ve/veya onu içeren oyun nesnesini düzenleyip değiştirebilir, modeli istediğiniz gibi taşıyabilir, döndürebilir ve ölçekleyebilirsiniz.

## Çalışma sırasında değiştirme

Modelleri çalışma sırasında çeşitli işlevler ve özellikler aracılığıyla değiştirebilirsiniz (kullanım için [API belgelerine](/ref/model/) bakın).

![Oyun içinde Wiggler](images/model/runtime.png)

### Çalışma sırasında animasyon

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

### Özellikleri değiştirme

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

Başlangıç noktası olarak kullanabileceğiniz birkaç yerleşik materyal vardır:

  * Örnek oluşturma (instancing) kullanılmayan statik modeller için *model.material* kullanın
  * Örnek oluşturma kullanılan statik modeller için *model_instanced.material* kullanın
  * İskelete bağlı (animasyonlu), örnek oluşturma kullanılmayan modeller için *model_skinned.material* kullanın
  * İskelete bağlı (animasyonlu), örnek oluşturma kullanılan modeller için *model_skinned_instanced.material* kullanın

Yerleşik model materyalleri yerel köşe uzayını (local vertex space) kullanır. İskelete bağlı modellerde yerel köşe uzayı, köşe gölgelendiricisinin bir kemik matrisi dokusu kullanarak GPU üzerinde iskelete bağlama (skinning) işlemini gerçekleştirmesini sağlar; model örneği oluşturma işlemi için de yerel köşe uzayı gereklidir. Bu nedenle, GPU üzerinde iskelete bağlanan veya örnek oluşturma kullanılan modeller için tasarlanan özel bir materyalin *Local* köşe uzayı ayarını kullanması önerilir.

Kemik matrisi önbelleği bir `RGBA32F` dokusu kullanır. Etkin grafik bağdaştırıcısı bu doku biçimini desteklemiyorsa Defold, yerel uzay materyali kullanan animasyonlu bir Model bileşeni oluşturamaz. Bu nedenle OpenGL ES 2.0 ve WebGL 1.0 üzerindeki destek, bağdaştırıcının kayan noktalı doku uzantısına bağlıdır. Bu uzantıya sahip olmayan bir bağdaştırıcıyla uyumluluk için, CPU üzerinde iskelete bağlama yapan ve model örneği oluşturmayı desteklemeyen özel bir dünya uzayı materyali kullanın. Önbellek boyutları [Model proje ayarları](/manuals/project-settings/#model) ile ayarlanabilir.

Modelleriniz için özel materyaller oluşturmanız gerekiyorsa bilgi için [Materyal belgelerine](/manuals/material) bakın. [Gölgelendirici kılavuzu](/manuals/shader), gölgelendirici programlarının nasıl çalıştığı hakkında bilgi içerir.


### Materyal sabitleri

{% include shared/material-constants.md component='model' variable='tint' %}

`tint`
: Modelin renk çarpanı (`vector4`). Renk çarpanı `vector4` ile temsil edilir; x, y, z ve w sırasıyla kırmızı, yeşil, mavi ve alfa renk çarpanlarına karşılık gelir.


## İşleme

Varsayılan işleme betiği (render script), 2B oyunlar için özel olarak hazırlanmıştır ve 3B modellerle çalışmaz. Ancak varsayılan işleme betiğini kopyalayıp betiğe birkaç satır kod ekleyerek modellerinizin işlenmesini etkinleştirebilirsiniz. Örneğin:

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
