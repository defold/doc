---
title: Modelleri içe aktarma
brief: Bu kılavuz, model bileşeninin kullandığı 3B modellerin nasıl içe aktarılacağını açıklar.
---

# 3B modelleri içe aktarma
Defold, glTF 2.0 (GL Transmission Format) biçimindeki modelleri, iskeletleri (skeleton) ve animasyonları destekler. 3B modeller için *.gltf* veya *.glb* dosyalarını kullanın. glTF, oyun motorlarında ve gerçek zamanlı uygulamalarda 3B verilerin aktarılması ve yüklenmesi için tasarlanmış modern bir biçimdir.

3B modeller oluşturmak veya bunları glTF biçimine dönüştürmek için Maya, 3ds Max, SketchUp ve Blender gibi araçlar kullanabilirsiniz.

Blender, güçlü ve popüler bir 3B modelleme, animasyon ve işleme (rendering, görüntü oluşturma) programıdır. Windows, macOS ve Linux üzerinde çalışır ve [https://www.blender.org](https://www.blender.org) adresinden ücretsiz olarak edinilebilir.

![Blender'da model](images/model/blender_gltf.png)

## Defold'a içe aktarma
Bir modeli içe aktarmak için *.gltf* veya *.glb* dosyasını Defold düzenleyicisinin *Assets bölmesine* sürükleyip bırakın.

glTF yaygın olarak iki şekilde saklanabilir:

* *.glb* tek bir ikili dosyadır. Model verilerini içerir ve paketlenmiş doku (texture) görüntülerini de içerebilir. Modeli tek bir dosya olarak taşımak veya saklamak istediğinizde bu kullanışlıdır.
* *.gltf* metin tabanlı bir JSON dosyasıdır. Genellikle örgü (mesh) verileri için ayrı bir *.bin* dosyasına ve *.png* veya *.jpg* gibi ayrı doku görüntülerine başvurur. Bu çeşidi kullanırken başvurulan tüm dosyaları projeye ekleyin ve göreli yollarını koruyun.

Modelin Defold'da bir doku kullanması gerekiyorsa doku görüntüsünü ayrı bir varlık (asset) olarak içe aktarın. Kaynak glTF/GLB dosyası gömülü görüntüler içerse bile dokular, bileşen materyalinin (material) doku özellikleri aracılığıyla model bileşenine (model component) atanmalıdır.

![İçe aktarılan model varlıkları](images/model/assets_gltf.png)

::: sidenote
Defold 1.13.0 sürümünden itibaren Defold, içe aktarılan glTF dosyasındaki konumları ve dönüşümleri (transform) korur ve içe aktarma sırasında modeli otomatik olarak yeniden merkezlemez. Düzenleyici önizlemesi ve çalışma zamanı, içe aktarılan dönüşümleri tutarlı biçimde kullanır: iskelete bağlanmış (skinned) veya bir kemiğe alt nesne olarak bağlanmış örgüler, iskelete göre yerel dönüşümlerini korurken rijit örgüler, hiyerarşisi düzleştirilmiş dünya yerleşimlerini korur.

Defold 1.13.2 sürümünden itibaren bir [model bileşeni](/manuals/model/#model-properties), içe aktarılan sahneden tek bir adlandırılmış örgü seçebilir. *Mesh* alanını boş bırakmak tüm sahneyi kullanır ve yukarıda açıklanan dönüşümleri korur. Bir örgü seçmek, glTF düğüm dönüşümleri olmadan örgünün yerel geometrisini kullanır; bu nedenle örgüyü model bileşeninin veya oyun nesnesinin (game object) dönüşümünü kullanarak yerleştirin.

Defold'un eski bir sürümüyle oluşturulmuş bir modelin konumu veya yönelimi yeniden içe aktarıldıktan sonra değişirse Blender'da veya başka bir içerik oluşturma aracında dönüşümü düzeltin ve *.gltf* veya *.glb* dosyasını yeniden dışa aktarın.
:::

## Model kullanma
Modeli içe aktardıktan sonra bir [model bileşeninde](/manuals/model) kullanın:

1. *Assets* bölmesinde <kbd>New... ▸ Model</kbd> ile bir Model dosyası oluşturun veya <kbd>Add Component ▸ Model</kbd> ile doğrudan bir oyun nesnesine model bileşeni ekleyin.
2. *Scene* özelliğini içe aktarılan *.gltf* veya *.glb* dosyasına ayarlayın. Tüm sahneyi kullanmak için *Mesh* alanını boş bırakın veya yalnızca yerel geometrisini kullanmak için adlandırılmış bir örgü seçin.
3. Animasyonlu bir model için *Skeleton* özelliğini iskeleti içeren *.gltf* veya *.glb* dosyasına ayarlayın. Örgü, iskelet ve animasyonlar birlikte dışa aktarıldığında bu genellikle *Scene* için kullanılan dosyayla aynıdır.
4. Animasyonlar için bir *Animation Set* dosyası oluşturun ve bunu *Animations* özelliğine atayın. Bir animasyonun otomatik olarak başlamasını istiyorsanız *Default Animation* özelliğini ayarlayın.
5. *Material* özelliğini modele uygun bir materyale ayarlayın. Yerleşik *model.material*, *model_instanced.material*, *model_skinned.material* ve *model_skinned_instanced.material* dosyaları yararlı başlangıç noktalarıdır. İskelete bağlı modellerin materyalleri, iskelete bağlama (skinning) işleminin GPU üzerinde çalışabilmesi için yerel köşe uzayını kullanır; GPU üzerinde iskelete bağlanan veya örnekler hâlinde çizilen (instanced) modeller için özel materyaller de yerel köşe uzayını kullanmalıdır. Grafik bağdaştırıcısı gereksinimi için [model kılavuzuna](/manuals/model/#material) bakın.
6. *Texture* gibi materyal doku özelliklerini içe aktarılan doku görüntüsü dosyalarına ayarlayın. Materyal birden çok doku kullanıyorsa her dokuyu ilgili materyal doku alanına atayın.


## glTF biçimine dışa aktarma
Dışa aktarılan *.gltf* veya *.glb* dosyası, modeli oluşturan tüm köşeleri, kenarları ve yüzleri, tanımladıysanız _UV koordinatlarını_ (doku görüntüsünün hangi bölümünün örgünün belirli bir bölümüne eşlendiğini), iskeletteki kemikleri ve animasyon verilerini içerir.

* Çokgen örgülerle ilgili ayrıntılı bir açıklamayı http://en.wikipedia.org/wiki/Polygon_mesh adresinde bulabilirsiniz.

* UV koordinatları ve UV eşleme http://en.wikipedia.org/wiki/UV_mapping adresinde açıklanır.

Defold, dışa aktarılan animasyon verilerine bazı kısıtlamalar getirir:

* Defold şu anda yalnızca önceden hesaplanmış (baked) animasyonları destekler. Animasyonlarda her anahtar karede animasyon uygulanan her kemik için matrisler bulunmalıdır; konum, dönme ve ölçek ayrı anahtarlar olarak bulunmamalıdır.

* Animasyonlara doğrusal ara değerleme (interpolation) de uygulanır. Daha gelişmiş eğri ara değerlemesi yapıyorsanız animasyonların dışa aktarma aracı tarafından önceden hesaplanması gerekir.

### Gereksinimler
Bir modeli dışa aktarırken glTF desteğinin araçlar ve motorlar arasında farklılık gösterebileceğini unutmayın. glTF 2.0 kullanın, model doku kullanıyorsa doğru UV koordinatlarına sahip olduğundan emin olun ve bir model bileşenine atanacak doku görüntülerini ayrı olarak içe aktarın.

Amacımız glTF biçimini tam olarak desteklemek olsa da henüz bu noktaya ulaşamadık.
Eksik bir özellik varsa lütfen [depomuzda](https://github.com/defold/defold/issues) bu özellik için istekte bulunun

### Bir dokuyu dışa aktarma
Modeliniz için henüz bir dokunuz yoksa Blender ile doku oluşturabilirsiniz. Bunu, modelden fazladan materyalleri kaldırmadan önce yapmanız önerilir. Örgüyü ve tüm köşelerini seçerek başlayın:

![Tümünü seçme](images/model/blender_select_all_vertices.png)

Tüm köşeler seçildiğinde UV yerleşimini elde etmek için örgünün UV açılımını yapın:

![Örgünün UV açılımını yapma](images/model/blender_unwrap_mesh.png)

Ardından UV yerleşimini doku olarak kullanılabilecek bir görüntüye dışa aktarabilirsiniz:

![UV yerleşimini dışa aktarma](images/model/blender_export_uv_layout.png)

![UV yerleşimini dışa aktarmanın sonucu](images/model/blender_export_uv_layout_result.png)

### Blender ile dışa aktarma
Modelinizi Blender'dan <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd> ile dışa aktarın.

![Blender ile dışa aktarma](images/model/export_gltf.png)

Dışa aktarmadan önce nesneyi veya nesneleri seçin ve yalnızca seçimi dışa aktarmak istiyorsanız *Selected Objects* seçeneğini etkinleştirin.

*Format* seçeneklerinden birini seçin:

* *glTF Binary (.glb)* tek bir dosya oluşturur. Modelin tek bir varlık olarak kolayca taşınabilmesini veya saklanabilmesini istediğinizde bunu kullanın.
* *glTF Separate (.gltf + .bin + textures)* model açıklaması, ikili veriler ve dokular için ayrı dosyalar oluşturur. Doku görüntülerini düzenlemek veya Defold'da ayrı olarak atamak istediğinizde bunu kullanın.

Model animasyonlar içeriyorsa animasyon dışa aktarmayı etkinleştirin ve animasyonların önceden hesaplandığından emin olun. Model doku kullanıyorsa örgünün UV açılımının yapıldığından ve doku görüntülerinin PNG veya JPEG gibi Defold'un içe aktarabileceği bir biçimde dışa aktarıldığından emin olun.

![Blender ile dışa aktarma](images/model/export_settings.png)
