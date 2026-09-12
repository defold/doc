---
title: Atlas kılavuzu
brief: Bu kılavuz, Atlas kaynaklarının Defold'da nasıl çalıştığını açıklar.
---

# Atlas

Sprite bileşenlerinde (sprite components) kaynak olarak çoğu zaman tek tek görüntüler kullanılsa da performans nedeniyle görüntülerin atlas adı verilen daha büyük görüntü kümelerinde birleştirilmesi gerekir. Küçük görüntü kümelerinin atlaslarda birleştirilmesi, özellikle bellek ve işlem gücünün masaüstü bilgisayarlara veya oyun konsollarına göre daha sınırlı olduğu mobil cihazlarda önemlidir.

Defold'da atlas kaynağı (atlas resource), otomatik olarak daha büyük bir görüntüde birleştirilen ayrı görüntü dosyalarının listesidir.

## Atlas oluşturma

*Assets* tarayıcısındaki bağlam menüsünden <kbd>New... ▸ Atlas</kbd> seçeneğini seçin. Yeni atlas dosyasına bir ad verin. Düzenleyici dosyayı atlas düzenleyicisinde açar. Atlas özellikleri, düzenleyebilmeniz için
*Properties* bölmesinde gösterilir (ayrıntılar için aşağıya bakın).

Bir atlası, sprite ve ParticleFX gibi nesne bileşenleri için grafik kaynağı olarak kullanmadan önce atlasa görüntüler veya animasyonlar eklemeniz gerekir.

Görüntülerinizi projeye eklediğinizden emin olun (görüntü dosyalarını *Assets* tarayıcısında uygun konuma sürükleyip bırakın)

Tek tek görüntüler ekleme

: Görüntüleri *Asset* bölmesinden düzenleyici görünümüne sürükleyip bırakın.
  
  Alternatif olarak, *Outline* bölmesindeki kök Atlas öğesine <kbd>sağ tıklayın</kbd>.

  Tek tek görüntüler eklemek için açılan bağlam menüsünden <kbd>Add Images</kbd> seçeneğini seçin.

  Atlasa eklemek istediğiniz görüntüleri bulup seçebileceğiniz bir iletişim kutusu açılır. Görüntü dosyalarını filtreleyebilir ve aynı anda birden fazla dosya seçebilirsiniz.

  ![Atlas oluşturma, görüntü ekleme](images/atlas/add.png)

  Eklenen görüntüler *Outline* görünümünde listelenir ve atlasın tamamı ortadaki düzenleyici görünümünde görülebilir. Seçimi görünüm alanına sığdırmak için <kbd>F</kbd> tuşuna basmanız (menüden <kbd>View ▸ Frame Selection</kbd>) gerekebilir.

  ![Eklenen görüntüler](images/atlas/single_images.png)

Kare dizisi animasyonları ekleme
: *Outline* bölmesindeki kök Atlas öğesine <kbd>sağ tıklayın</kbd>.

  Bir kare dizisi animasyonu (flipbook animation) grubu oluşturmak için açılan bağlam menüsünden <kbd>Add Animation Group</kbd> seçeneğini seçin.

  Atlasa varsayılan ada (`New Animation`) sahip yeni, boş bir animasyon grubu eklenir.

  Görüntüleri seçili gruba eklemek için *Asset* bölmesinden düzenleyici görünümüne sürükleyip bırakın.
  
  Alternatif olarak, yeni gruba <kbd>sağ tıklayın</kbd> ve bağlam menüsünden <kbd>Add Images</kbd> seçeneğini seçin.

  Animasyon grubuna eklemek istediğiniz görüntüleri bulup seçebileceğiniz bir iletişim kutusu açılır.

  ![Atlas oluşturma, görüntü ekleme](images/atlas/add_animation.png)

  Animasyon grubu seçiliyken önizlemek için <kbd>Space</kbd> tuşuna, önizlemeyi kapatmak için <kbd>Ctrl/Cmd+T</kbd> tuşlarına basın. Animasyonun *Properties* bölmesindeki özelliklerini gerektiği gibi ayarlayın (aşağıya bakın).

  ![Animasyon grubu](images/atlas/animation_group.png)

Outline görünümündeki görüntüleri seçip <kbd>Alt + Up/down</kbd> tuşlarına basarak yeniden sıralayabilirsiniz. Outline görünümündeki görüntüleri kopyalayıp yapıştırarak kolayca çoğaltabilirsiniz (<kbd>Edit</kbd> menüsünü, sağ tıklama bağlam menüsünü veya klavye kısayollarını kullanarak).

## Atlas özellikleri

Her atlas kaynağının bir dizi özelliği vardır. *Outline* görünümündeki kök öğeyi seçtiğinizde bu özellikler *Properties* bölmesinde gösterilir.

Size
: Oluşturulan doku kaynağının (texture resource) hesaplanan toplam boyutunu gösterir. Genişlik ve yükseklik, ikinin en yakın kuvvetine ayarlanır. Doku sıkıştırmayı etkinleştirdiğinizde bazı biçimlerin kare dokular gerektirdiğini unutmayın. Bu durumda kare olmayan dokular, kare haline getirilmek için yeniden boyutlandırılır ve boş alanla doldurulur. Ayrıntılar için [Doku profilleri kılavuzuna](/manuals/texture-profiles/) bakın.

Margin
: Görüntülerin arasına eklenecek piksel sayısı.

Inner Padding
: Her görüntünün çevresine dolgu olarak eklenecek boş piksel sayısı.

Extrude Borders
: Her görüntünün çevresine tekrar tekrar dolgu olarak eklenecek kenar pikseli sayısı. Parça gölgelendiricisi (fragment shader), bir görüntünün kenarındaki pikselleri örneklerken aynı atlas dokusundaki komşu görüntünün pikselleri taşabilir. Kenarları genişletmek bu sorunu çözer.

Max Page Size
: Çok sayfalı bir atlasta bir sayfanın en büyük boyutu. Bu özellik, tek bir çizim çağrısı kullanmayı sürdürürken atlas boyutunu sınırlamak için atlası birden fazla sayfaya bölmek amacıyla kullanılabilir. Bu özelliğin, `/builtins/materials/*_paged_atlas.material` konumunda bulunan ve çok sayfalı atlas desteği etkin olan materyallerle (materials) birlikte kullanılması gerekir.

![Çok sayfalı atlas](images/atlas/multipage_atlas.png)

Rename Patterns
: Her birinin `search=replace` biçiminde olduğu, virgülle (´,´) ayrılmış arama ve değiştirme desenleri listesi.
Her görüntünün özgün adı (dosyanın uzantısız adı) bu desenler kullanılarak dönüştürülür. (Örneğin, `hat=cat,_normal=` deseni, `hat_normal` adlı bir görüntüyü `cat` olarak yeniden adlandırır). Bu, atlaslar arasında animasyonları eşleştirirken kullanışlıdır.

Aşağıda, bir atlasa 64x64 boyutunda dört kare görüntü eklendiğinde farklı özellik ayarlarının sonuçlarını gösteren örnekler verilmiştir. Görüntüler 128x128 alana sığmadığı anda atlasın 256x256 boyutuna çıktığına ve bunun doku alanının büyük ölçüde boşa harcanmasına neden olduğuna dikkat edin.

![Atlas özellikleri](images/atlas/atlas_properties.png)

## Görüntü özellikleri

Bir atlastaki her görüntünün bir dizi özelliği vardır:

Id
: Görüntünün kimliği (salt okunur).

Size
: Görüntünün genişliği ve yüksekliği (salt okunur).

Pivot
: Görüntünün dayanak noktası (pivot), birim cinsinden belirtilir. Sol üst köşe (0,0), sağ alt köşe (1,1) konumundadır. Varsayılan değer (0.5, 0.5) şeklindedir. Dayanak noktası 0-1 aralığının dışında olabilir. Dayanak noktası, görüntü örneğin bir sprite bileşeninde kullanıldığında merkezleneceği noktadır. Düzenleyici görünümündeki dayanak noktası tutamacını sürükleyerek bu noktayı değiştirebilirsiniz. Tutamaç yalnızca tek bir görüntü seçili olduğunda görünür. Sürüklerken <kbd>Shift</kbd> tuşunu basılı tutarak yapışmayı etkinleştirebilirsiniz.

Sprite Trim Mode
: Sprite bileşeninin nasıl işlendiğini (rendering) belirtir. Varsayılan olarak sprite dikdörtgen şeklinde işlenir (Sprite Trim Mode özelliği Off olarak ayarlanır). Sprite çok sayıda saydam piksel içeriyorsa 4 ile 8 arasında köşe kullanarak dikdörtgen olmayan bir şekil olarak işlemek daha verimli olabilir. Sprite kırpmanın, dokuz parçalı ölçekleme (slice-9) kullanan sprite bileşenleriyle birlikte çalışmadığını unutmayın.

Image
: Görüntünün kendisine giden yol.

![Görüntü özellikleri](images/atlas/image_properties.png)

## Animasyon özellikleri

Bir animasyon grubundaki görüntülerin listesine ek olarak bir dizi özellik bulunur:

Id
: Animasyonun adı.

Fps
: Animasyonun saniyedeki kare sayısı (FPS) olarak ifade edilen oynatma hızı.

Flip horizontal
: Animasyonu yatay olarak çevirir.

Flip vertical
: Animasyonu dikey olarak çevirir.

Playback
: Animasyonun nasıl oynatılacağını belirtir:

  - `None` animasyonu hiç oynatmaz, ilk görüntü gösterilir.
  - `Once Forward` animasyonu ilk görüntüden son görüntüye kadar bir kez oynatır.
  - `Once Backward` animasyonu son görüntüden ilk görüntüye kadar bir kez oynatır.
  - `Once Ping Pong` animasyonu ilk görüntüden son görüntüye ve ardından ilk görüntüye geri dönerek bir kez oynatır.
  - `Loop Forward` animasyonu ilk görüntüden son görüntüye kadar tekrar tekrar oynatır.
  - `Loop Backward` animasyonu son görüntüden ilk görüntüye kadar tekrar tekrar oynatır.
  - `Loop Ping Pong` animasyonu ilk görüntüden son görüntüye ve ardından ilk görüntüye geri dönerek tekrar tekrar oynatır.

## Çalışma sırasında doku ve atlas oluşturma

Çalışma sırasında bir doku ve bir atlas oluşturmak mümkündür.

### Çalışma sırasında doku kaynağı oluşturma

Yeni bir doku kaynağı oluşturmak için [`resource.create_texture(path, params)`](https://defold.com/ref/stable/resource/#resource.create_texture:path-table) işlevini kullanın:

```lua
  local params = {
    width  = 128,
    height = 128,
    type   = graphics.TEXTURE_TYPE_2D,
    format = graphics.TEXTURE_FORMAT_RGBA,
  }
  local my_texture_id = resource.create_texture("/my_custom_texture.texturec", params)
```

Doku oluşturulduktan sonra dokunun piksellerini ayarlamak için [`resource.set_texture(path, params, buffer)`](https://defold.com/ref/stable/resource/#resource.set_texture:path-table-buffer) işlevini kullanabilirsiniz:

```lua
  local width = 128
  local height = 128
  local buf = buffer.create(width * height, { { name=hash("rgba"), type=buffer.VALUE_TYPE_UINT8, count=4 } } )
  local stream = buffer.get_stream(buf, hash("rgba"))

  for y=1, height do
      for x=1, width do
          local index = (y-1) * width * 4 + (x-1) * 4 + 1
          stream[index + 0] = 0xff
          stream[index + 1] = 0x80
          stream[index + 2] = 0x10
          stream[index + 3] = 0xFF
      end
  end

  local params = { width=width, height=height, x=0, y=0, type=graphics.TEXTURE_TYPE_2D, format=graphics.TEXTURE_FORMAT_RGBA, num_mip_maps=1 }
  resource.set_texture(my_texture_id, params, buf)
```

::: sidenote
`resource.set_texture()` işlevini, dokunun bir alt bölgesini güncellemek için de kullanabilirsiniz. Bunun için dokunun tam boyutundan daha küçük genişlik ve yüksekliğe sahip bir arabellek kullanın ve `resource.set_texture()` işlevine verilen x ve y parametrelerini değiştirin.
:::

Doku, `go.set()` kullanılarak doğrudan bir [model bileşeninde](/manuals/model/) kullanılabilir:

```lua
  go.set("#model", "texture0", my_texture_id)
```

### Çalışma sırasında atlas oluşturma

Dokunun bir [sprite bileşeninde](/manuals/sprite/) kullanılması için önce bir atlas tarafından kullanılması gerekir. Bir atlas oluşturmak için [`resource.create_atlas(path, params)`](https://defold.com/ref/stable/resource/#resource.create_atlas:path-table) işlevini kullanın:

```lua
  local params = {
    texture = texture_id,
    animations = {
      {
        id          = "my_animation",
        width       = width,
        height      = height,
        frames      = { 1 },
      }
    },
    geometries = {
      {
        vertices  = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        uvs = {
          0,     0,
          0,     height,
          width, height,
          width, 0
        },
        indices = {0,1,2,0,2,3}
      }
    }
  }
  local my_atlas_id = resource.create_atlas("/my_atlas.texturesetc", params)

  -- assign the atlas to the 'sprite' component on the same go
  go.set("#sprite", "image", my_atlas_id)

  -- play the "animation"
  sprite.play_flipbook("#sprite", "my_animation")

```

`frames` öğeleri, `geometries` tablosuna başvuran ve 1'den başlayan indislerdir. Bir liste geometrileri yeniden kullanabilir, yeniden sıralayabilir veya atlayabilir; kullanımı artık önerilmeyen `frame_start` ve `frame_end` aralık alanlarıyla bunlar temsil edilemez. `resource.get_atlas()` işlevi `frames` döndürür; atlas verilerini `resource.set_atlas()` veya `resource.create_atlas()` işlevine aktarırken aynı gösterimi kullanın. Aralık alanları, uyumluluk için ayarlama ve oluşturma işlevleri tarafından hâlâ kabul edilir, ancak yeni kodda `frames` kullanılması önerilir.
