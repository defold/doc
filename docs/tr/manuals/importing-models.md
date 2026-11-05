---
title: Modelleri içe aktarma
brief: Bu kılavuz, model bileşeninin kullandığı 3B modellerin nasıl içe aktarılacağını açıklar.
---

# 3B modelleri içe aktarma {#importing-3d-models}
Defold, glTF 2.0 (GL Transmission Format) biçimindeki modelleri, iskeletleri (skeleton) ve animasyonları destekler. 3B modeller için *.gltf* veya *.glb* dosyalarını kullanın. glTF, oyun motorlarında ve gerçek zamanlı uygulamalarda 3B verilerin aktarılması ve yüklenmesi için tasarlanmış modern bir biçimdir.

3B modeller oluşturmak veya bunları glTF biçimine dönüştürmek için Maya, 3ds Max, SketchUp ve Blender gibi araçlar kullanabilirsiniz.

Blender, güçlü ve popüler bir 3B modelleme, animasyon ve işleme (rendering, görüntü oluşturma) programıdır. Windows, macOS ve Linux üzerinde çalışır ve [https://www.blender.org](https://www.blender.org) adresinden ücretsiz olarak edinilebilir.

![Blender'da model](images/model/blender_gltf.png)

## Defold'a içe aktarma {#importing-to-defold}
Bir modeli içe aktarmak için *.gltf* veya *.glb* dosyasını Defold düzenleyicisinin *Assets bölmesine* sürükleyip bırakın.

glTF yaygın olarak iki şekilde saklanabilir:

* *.glb* tek bir ikili dosyadır. Model verilerini içerir ve paketlenmiş doku (texture) görüntülerini de içerebilir. Modeli tek bir dosya olarak taşımak veya saklamak istediğinizde bu kullanışlıdır.
* *.gltf* metin tabanlı bir JSON dosyasıdır. Genellikle örgü (mesh) verileri için ayrı bir *.bin* dosyasına ve *.png*, *.jpg* veya *.ktx2* gibi ayrı doku görüntülerine başvurur. Bu çeşidi kullanırken başvurulan tüm dosyaları projeye ekleyin ve göreli yollarını koruyun.

Gömülü görüntüler, ayrı varlıklara çıkarılmadan doğrudan glTF veya GLB dosyasından kullanılabilir. Harici görüntü ve arabellek dosyaları yine de göreli yolları korunarak modelle birlikte içe aktarılmalıdır.

::: sidenote
Defold, içe aktarılan glTF dosyasındaki konumları ve dönüşümleri (transform) korur ve içe aktarma sırasında modeli otomatik olarak yeniden merkezlemez. Düzenleyici önizlemesi ve çalışma zamanı, içe aktarılan dönüşümleri tutarlı biçimde kullanır: iskelete bağlanmış (skinned) veya bir kemiğe alt nesne olarak bağlanmış örgüler, iskelete göre yerel dönüşümlerini korurken rijit örgüler, hiyerarşisi düzleştirilmiş dünya yerleşimlerini korur.

Bir [model bileşeni](/manuals/model/#model-properties), içe aktarılan sahneden tek bir adlandırılmış örgü seçebilir. *Mesh* alanını boş bırakmak tüm sahneyi kullanır ve yukarıda açıklanan dönüşümleri korur. Bir örgü seçmek, glTF düğüm dönüşümleri olmadan örgünün yerel geometrisini kullanır; bu nedenle örgüyü model bileşeninin veya oyun nesnesinin (game object) dönüşümünü kullanarak yerleştirin.

Defold'un eski bir sürümüyle oluşturulmuş bir modelin konumu veya yönelimi yeniden içe aktarıldıktan sonra değişirse Blender'da veya başka bir içerik oluşturma aracında dönüşümü düzeltin ve *.gltf* veya *.glb* dosyasını yeniden dışa aktarın.
:::

### Sıkıştırılmış geometri {#compressed-geometry}

*.gltf* ve *.glb* kaynakları Draco veya Meshopt ile sıkıştırılmış geometri içerebilir. Desteklenen glTF sıkıştırma eklentileri şunlardır:

| Sıkıştırma | glTF eklentisi |
| --- | --- |
| Draco | `KHR_draco_mesh_compression` |
| Meshopt | `EXT_meshopt_compression` ve `KHR_meshopt_compression` |

glTF 2.0 varlığınızı bu eklentilerden biriyle dışa aktarın veya optimize edin, ardından sıkıştırılmamış bir modelle aynı adımları kullanarak içe aktarın. Harici arabellekleri ve dokuları ekleyin ve göreli yollarını koruyun. İçe aktarılan dosyayı her zamanki gibi Model bileşeninin *Scene* özelliğine atayın.

Defold, sıkıştırılmış geometriyi içe aktarma ve derleme sırasında çözer. Ortaya çıkan model, Defold'un normal çalışma zamanı geometri gösterimini kullanır. Bu destek, çalışan motorda Draco veya Meshopt sıkıştırmasını etkinleştirmez; daha küçük bir kaynak dosyası daha küçük bir oyun paketi garanti etmez.

### İçe aktarılan sahneye göz atma {#browsing-the-imported-scene}

Örgülerine, oluşturulan materyallerine ve gömülü görüntülerine göz atmak için *Assets* panelinde bir *.gltf* veya *.glb* dosyasını genişletin. Sahneyi açmak, tanımlı materyalleri ve dokularıyla önizlemesini gösterir. Önizleme için tek bir örgüyü de açabilirsiniz.

Dosyanın içinde sunulan kaynaklar salt okunurdur. Bir örgü için düzenlenebilir Model kaynağı oluşturmak üzere örgüyü kopyalayıp bir proje klasörüne yapıştırın. Ortaya çıkan *.model* dosyası, içe aktarılan glTF veya GLB dosyasına başvurmaya devam eder. Kaynak geometrisini veya gömülü görüntüleri değiştirmek için varlığı içerik oluşturma aracınızda düzenleyip yeniden dışa aktarın.

Düzenleyici betikleri bu kaynakları `editor.resource_children(path)` ile listeleyebilir. Klasörlerin ve glTF/GLB dosyalarının içindeki kaynakları özyinelemeli olarak ziyaret eden bir örnek için [Proje kaynaklarını dolaşma](/manuals/editor-scripts/#traversing-project-resources) bölümüne bakın.

### KTX2 dokuları {#ktx2-textures}

Model dokuları, harici dosyalar veya bir *.gltf* ya da *.glb* dosyasına gömülmüş görüntüler biçiminde *.ktx2* kaynakları kullanabilir. Harici dosyaları modelle birlikte içe aktarın. Gömülü KTX2 görüntüleri *Assets* panelinde sahnenin altında görünür ve doğrudan materyal doku alanlarına veya <kbd>Auto Fill</kbd> aracılığıyla atanabilir.

[Doku profilleri](/manuals/texture-profiles/#ktx2-source-textures), KTX2 kaynak biçiminin korunacağını mı yoksa yapılandırılmış çıktı biçimlerine dönüştürüleceğini mi belirler. **Keep KTX2 Format**, doku sıkıştırması etkin olduğunda kaynağın kodlama biçimini korur; ancak görüntü işleme yine de yeniden kodlama gerektirebilir. Hedef cihazlarınızın biçimi desteklediğini kontrol edin ve zaten sıkıştırılmış bir dokuyu yeniden sıkıştırırken olası ek kalite kaybını hesaba katın. [KTX2 girdi biçimleri ve önizlemeler](/manuals/importing-graphics/#ktx2-textures) bölümüne bakın.

## Model kullanma {#using-a-model}
Modeli içe aktardıktan sonra bir [model bileşeninde](/manuals/model) kullanın:

1. *Assets* bölmesinde <kbd>New... ▸ Model</kbd> ile bir Model dosyası oluşturun veya <kbd>Add Component ▸ Model</kbd> ile doğrudan bir oyun nesnesine model bileşeni ekleyin.
2. *Scene* özelliğini içe aktarılan *.gltf* veya *.glb* dosyasına ayarlayın.
3. *Auto Fill Model Fields?* iletişim kutusu göründüğünde sahnenin oluşturulan materyallerini ve başvurulan dokularını atamak için <kbd>Auto Fill</kbd> seçeneğini seçin. Bu işlem mevcut materyal ve doku eşlemelerini değiştirir. Eşlemelerinizi korumak için <kbd>Keep Current</kbd> seçeneğini seçin; yeni sahne seçimi yine de uygulanır.
4. Tüm sahneyi kullanmak için *Mesh* alanını boş bırakın veya yalnızca yerel geometrisini kullanmak için adlandırılmış bir örgü seçin. Örgü seçimini değiştirmek aynı iletişim kutusunu gösterebilir: bir örgü seçmek onun materyallerini, seçimi temizlemek ise sahnedeki tüm materyalleri önerir. <kbd>Keep Current</kbd>, yeni örgü seçimini uygularken eşlemeleri korur.
5. Animasyonlu bir model için *Skeleton* özelliğini iskeleti içeren *.gltf* veya *.glb* dosyasına ayarlayın. Örgü, iskelet ve animasyonlar birlikte dışa aktarıldığında bu genellikle *Scene* için kullanılan dosyayla aynıdır.
6. Animasyonlar için bir *Animation Set* dosyası oluşturun ve bunu *Animations* özelliğine atayın. Bir animasyonun otomatik olarak başlamasını istiyorsanız *Default Animation* özelliğini ayarlayın.

Seçilen glTF veya GLB kaynağı materyaller sunduğunda düzenleyici eşlemeleri doldurmayı önerir. Hem gömülü görüntüleri hem de harici görüntü başvurularını çözümler. Oluşturulan materyaller, yerleşik glTF gölgelendiricilerini kullanır; aydınlatma ve desteklenen materyal efektleri için [PBR kılavuzuna](/manuals/physically-based-rendering/#built-in-pbr-materials) bakın.

### Materyalleri ve dokuları elle atama {#assigning-materials-and-textures-manually}

<kbd>Keep Current</kbd> seçeneğini seçerseniz veya özel gölgelendirmeye ihtiyaç duyarsanız her *Material* özelliğini uygun bir materyale ayarlayın. Yerleşik `gltf` materyalleri PBR gölgelendirmesi sağlar; yerleşik `model` materyallerini ve kendi materyallerinizi de kullanabilirsiniz. Statik, iskelete bağlı ve örnekler hâlinde çizilen çeşitler ve gereksinimleri için [Model kılavuzuna](/manuals/model/#material) bakın.

Her dokuyu ilgili materyal doku alanına atayın. *Assets* panelinde glTF veya GLB dosyasının altında sunulan gömülü bir görüntüyü veya projedeki ayrı bir görüntü varlığını kullanabilirsiniz. Birden çok örnekleyicisi olan materyallerde her dokuyu amaçlanan örnekleyicisiyle eşleyin; [PBR kılavuzu yerleşik glTF örnekleyici adlarını listeler](/manuals/physically-based-rendering/#built-in-pbr-materials).


## glTF biçimine dışa aktarma {#exporting-to-gltf}
Dışa aktarılan *.gltf* veya *.glb* dosyası, modeli oluşturan tüm köşeleri, kenarları ve yüzleri, tanımladıysanız _UV koordinatlarını_ (doku görüntüsünün hangi bölümünün örgünün belirli bir bölümüne eşlendiğini), iskeletteki kemikleri ve animasyon verilerini içerir.

* Çokgen örgülerle ilgili ayrıntılı bir açıklamayı http://en.wikipedia.org/wiki/Polygon_mesh adresinde bulabilirsiniz.

* UV koordinatları ve UV eşleme http://en.wikipedia.org/wiki/UV_mapping adresinde açıklanır.

Defold, dışa aktarılan animasyon verilerine bazı kısıtlamalar getirir:

* Defold şu anda yalnızca önceden hesaplanmış (baked) animasyonları destekler. Animasyonlarda her anahtar karede animasyon uygulanan her kemik için matrisler bulunmalıdır; konum, dönme ve ölçek ayrı anahtarlar olarak bulunmamalıdır.

* Animasyonlara doğrusal ara değerleme (interpolation) de uygulanır. Daha gelişmiş eğri ara değerlemesi yapıyorsanız animasyonların dışa aktarma aracı tarafından önceden hesaplanması gerekir.

### Gereksinimler {#requirements}
Bir modeli dışa aktarırken glTF desteğinin araçlar ve motorlar arasında farklılık gösterebileceğini unutmayın. glTF 2.0 kullanın ve model doku kullanıyorsa doğru UV koordinatlarına sahip olduğundan emin olun. Görüntüler glTF veya GLB dosyasına gömülebilir veya sahnenin başvurduğu ayrı dosyalarda saklanabilir. Modeli Defold'a içe aktarırken tüm harici görüntü ve arabellek dosyalarını ekleyin.

Amacımız glTF biçimini tam olarak desteklemek olsa da henüz bu noktaya ulaşamadık.
Eksik bir özellik varsa lütfen [depomuzda](https://github.com/defold/defold/issues) bu özellik için istekte bulunun

### Bir dokuyu dışa aktarma {#exporting-a-texture}
Elle bir doku görüntüsü oluşturmak istiyorsanız Blender'dan UV yerleşimini şablon olarak dışa aktarabilirsiniz. Örgüyü ve tüm köşelerini seçerek başlayın:

![Tümünü seçme](images/model/blender_select_all_vertices.png)

Tüm köşeler seçildiğinde UV yerleşimini elde etmek için örgünün UV açılımını yapın:

![Örgünün UV açılımını yapma](images/model/blender_unwrap_mesh.png)

Ardından UV yerleşimini doku olarak kullanılabilecek bir görüntüye dışa aktarabilirsiniz:

![UV yerleşimini dışa aktarma](images/model/blender_export_uv_layout.png)

![UV yerleşimini dışa aktarmanın sonucu](images/model/blender_export_uv_layout_result.png)

### Blender ile dışa aktarma {#exporting-using-blender}
Modelinizi Blender'dan <kbd>File ▸ Export ▸ glTF 2.0 (.glb/.gltf)</kbd> ile dışa aktarın.

![Blender ile dışa aktarma](images/model/export_gltf.png)

Dışa aktarmadan önce nesneyi veya nesneleri seçin ve yalnızca seçimi dışa aktarmak istiyorsanız *Selected Objects* seçeneğini etkinleştirin.

*Format* seçeneklerinden birini seçin:

* *glTF Binary (.glb)* tek bir dosya oluşturur. Modelin tek bir varlık olarak kolayca taşınabilmesini veya saklanabilmesini istediğinizde bunu kullanın.
* *glTF Separate (.gltf + .bin + textures)* model açıklaması, ikili veriler ve dokular için ayrı dosyalar oluşturur. Doku görüntülerini düzenlemek veya Defold'da ayrı olarak atamak istediğinizde bunu kullanın.

Model animasyonlar içeriyorsa animasyon dışa aktarmayı etkinleştirin ve animasyonların önceden hesaplandığından emin olun. Model doku kullanıyorsa örgünün UV açılımının yapıldığından ve doku görüntülerinin PNG veya JPEG gibi Defold'un içe aktarabileceği bir biçimde dışa aktarıldığından emin olun.

![Blender ile dışa aktarma](images/model/export_settings.png)
