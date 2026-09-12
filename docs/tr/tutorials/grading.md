---
title: Renk düzenleme gölgelendiricisi öğreticisi
brief: Bu öğreticide Defold'da tam ekran bir son işlem efekti oluşturacaksınız.
---

# Renk düzenleme öğreticisi

Bu öğreticide renk düzenleme (color grading) yapan bir tam ekran son işlem efekti (post effect) oluşturacağız. Görüntü oluşturmak için kullanılan temel işleme (rendering) yöntemi bulanıklaştırma, izler, parlama, renk ayarları gibi çeşitli son işlem efektlerine de uygulanabilir.

Defold düzenleyicisini kullanmayı bildiğiniz ve GL gölgelendiricileri (shader) ile Defold işleme hattı (rendering pipeline) hakkında temel bilginiz olduğu varsayılır. Bu konuları öğrenmeniz gerekiyorsa [Gölgelendirici kılavuzumuza](/manuals/shader/) ve [İşleme kılavuzuna](/manuals/render/) göz atın.

## İşleme hedefleri

Varsayılan işleme betiğiyle (render script), her görsel bileşen (component; sprite bileşeni, karo haritası, parçacık efekti, GUI vb.) doğrudan grafik kartının *kare arabelleğine (frame buffer)* işlenir. Ardından donanım, grafiklerin ekranda görünmesini sağlar. Bir bileşenin piksellerinin asıl çizimini bir GL *gölgelendirici programı (shader program)* yapar. Defold, her bileşen türü için piksel verilerini değiştirmeden ekrana çizen varsayılan bir gölgelendirici programıyla gelir. Normalde istediğiniz davranış budur: görüntüleriniz ekranda ilk tasarlandıkları hâliyle görünmelidir.

Bir bileşenin gölgelendirici programını, piksel verilerini değiştiren veya program yoluyla tamamen yeni piksel renkleri oluşturan bir programla değiştirebilirsiniz. [Shadertoy öğreticisi](/tutorials/shadertoy) bunu nasıl yapacağınızı öğretir.

Şimdi oyununuzun tamamını siyah beyaz işlemek istediğinizi varsayalım. Olası çözümlerden biri, her bileşen türünün kendi gölgelendirici programını, piksel renklerinin doygunluğunu kaldıracak şekilde değiştirmektir. Defold şu anda 6 yerleşik materyal ve 6 köşe ve parça gölgelendiricisi program çiftiyle geldiğinden bu epey çalışma gerektirir. Ayrıca daha sonraki her değişikliğin veya efekt eklemesinin de her gölgelendirici programına uygulanması gerekir.

Çok daha esnek bir yaklaşım, işlemeyi iki ayrı adımda yapmaktır:

![İşleme hedefi](images/grading/render_target.png)

1. Tüm bileşenleri her zamanki gibi çizin, ancak olağan kare arabelleği yerine ekran dışı bir arabelleğe çizin. Bunu *işleme hedefi (render target)* adı verilen bir hedefe çizim yaparak gerçekleştirirsiniz.
2. Kare arabelleğine kare biçiminde bir çokgen çizin ve işleme hedefinde saklanan piksel verilerini çokgenin doku kaynağı olarak kullanın. Ayrıca kare çokgenin tüm ekranı kaplayacak şekilde gerildiğinden emin olun.

Bu yöntemle, oluşan görsel verileri ekrana ulaşmadan önce okuyabilir ve değiştirebiliriz. Yukarıdaki 2. adıma gölgelendirici programları ekleyerek kolayca tam ekran efektler elde edebiliriz. Bunun Defold'da nasıl kurulacağını görelim.

## Özel bir işleyici kurma

Yerleşik işleme betiğini değiştirip yeni işleme işlevini eklememiz gerekiyor. Varsayılan işleme betiği iyi bir başlangıç noktasıdır; bu nedenle onu kopyalayarak başlayın:

1. */builtins/render/default.render_script* dosyasını kopyalayın: *Asset* görünümünde *default.render_script* dosyasına sağ tıklayıp <kbd>Copy</kbd> seçeneğini seçin, ardından *main* klasörüne sağ tıklayıp <kbd>Paste</kbd> seçeneğini seçin. Kopyaya sağ tıklayıp <kbd>Rename...</kbd> seçeneğini seçin ve "grade.render_script" gibi uygun bir ad verin.
2. *Asset* görünümünde *main* klasörüne sağ tıklayıp <kbd>New ▸ Render</kbd> seçeneğini seçerek */main/grade.render* adlı yeni bir işleme dosyası oluşturun.
3. *grade.render* dosyasını açın ve *Script* özelliğini "/main/grade.render_script" olarak ayarlayın.

   ![grade.render](images/grading/grade_render.png)

4. *game.project* dosyasını açın ve *Render* ayarını "/main/grade.render" olarak ayarlayın.

   ![game.project](images/grading/game_project.png)

Oyun artık değiştirebileceğimiz yeni bir işleme hattıyla çalışacak şekilde ayarlandı. Motorun işleme betiği kopyamızı kullandığını sınamak için oyununuzu çalıştırın, ardından işleme betiğinde görsel bir sonuç verecek bir değişiklik yapıp betiği yeniden yükleyin. Örneğin, karoların ve sprite bileşenlerinin çizimini devre dışı bırakabilir, ardından <kbd>⌘ + R</kbd> tuşlarına basarak "bozuk" işleme betiğini çalışan oyunda yeniden yükleyebilirsiniz (hot reload):

```lua
...

render.set_projection(vmath.matrix4_orthographic(0, render.get_width(), 0, render.get_height(), -1, 1))

-- render.draw(self.tile_pred) -- <1>
render.draw(self.particle_pred)
render.draw_debug3d()

...
```
1. Tüm sprite bileşenlerini ve karoları içeren "tile" yükleminin çizim satırını yorum satırı hâline getirin. Bu kod satırı, işleme betiği dosyasında yaklaşık 33. satırda bulunur.

Bu basit sınamada sprite bileşenleri ve karolar kaybolursa oyunun sizin işleme betiğinizi çalıştırdığını anlarsınız. Her şey beklendiği gibi çalışıyorsa işleme betiğinde yaptığınız değişikliği geri alabilirsiniz.

## Ekran dışı bir hedefe çizim yapma

Şimdi işleme betiğini, kare arabelleği yerine ekran dışı işleme hedefine çizecek şekilde değiştirelim. Önce işleme hedefini oluşturmamız gerekiyor:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})

    self.clear_color = vmath.vector4(0, 0, 0, 1)
    self.clear_color.x = sys.get_config_number("render.clear_color_red", 0)
    self.clear_color.y = sys.get_config_number("render.clear_color_green", 0)
    self.clear_color.z = sys.get_config_number("render.clear_color_blue", 0)
    self.clear_color.w = sys.get_config_number("render.clear_color_alpha", 1)

    self.view = vmath.matrix4()

    local color_params = { format = graphics.TEXTURE_FORMAT_RGBA,
                       width = render.get_width(),
                       height = render.get_height() } -- <1>
    local target_params = {[graphics.BUFFER_TYPE_COLOR0_BIT] = color_params }

    self.target = render.render_target("original", target_params) -- <2>
end
```
1. İşleme hedefinin renk arabelleği parametrelerini ayarlayın. Oyunun hedef çözünürlüğünü kullanıyoruz.
2. İşleme hedefini renk arabelleği parametreleriyle oluşturun.

Şimdi yalnızca özgün işleme kodunun başına ve sonuna şu şekilde `render.set_render_target()` çağrıları eklememiz gerekiyor:

```lua
function update(self)
  render.set_render_target(self.target) -- <1>

  render.set_depth_mask(true)
  render.set_stencil_mask(0xff)
  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color, [graphics.BUFFER_TYPE_DEPTH_BIT] = 1, [graphics.BUFFER_TYPE_STENCIL_BIT] = 0})

  render.set_viewport(0, 0, render.get_width(), render.get_height()) -- <2>
  render.set_view(self.view)
  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT) -- <3>
end
```
1. İşleme hedefini etkinleştirin. Bundan sonra her `render.draw()` çağrısı ekran dışı işleme hedefimizin arabelleklerine çizecektir.
2. İşleme hedefinin çözünürlüğüne ayarlanan görüntü alanı dışında, `update()` içindeki tüm özgün çizim kodu olduğu gibi bırakılır.
3. Bu noktada oyunun tüm grafikleri işleme hedefine çizilmiştir. Dolayısıyla varsayılan işleme hedefine geçerek onu devre dışı bırakmanın zamanı gelmiştir.

Yapmamız gerekenlerin hepsi bu. Oyunu şimdi çalıştırırsanız her şeyi işleme hedefine çizecektir. Ancak artık kare arabelleğine hiçbir şey çizmediğimiz için yalnızca siyah bir ekran göreceğiz.

## Ekranı dolduracak bir nesne

İşleme hedefinin renk arabelleğindeki pikselleri ekrana çizmek için piksel verilerini doku olarak uygulayabileceğimiz bir şey hazırlamamız gerekiyor. Bu amaçla düz, kare biçiminde bir 3B model kullanacağız.

1. *`main.collection`* dosyasını açın ve "`grade`" adlı yeni bir oyun nesnesi (game object) oluşturun.
2. "`grade`" oyun nesnesine bir Model bileşeni ekleyin.
3. Model bileşeninin *Mesh* özelliğini, `builtins/assets/meshes` içinde bulunan *`quad.gltf`* dosyasına ayarlayın.

Oyun nesnesini ölçeklemeden başlangıç noktasında bırakın. Daha sonra, kareyi işlerken tüm ekranı dolduracak şekilde izdüşümünü alacağız. Ancak önce kare için bir materyal ve gölgelendirici programları gerekiyor:

1. *Asset* görünümünde *main* klasörüne sağ tıklayıp <kbd>New ▸ Material</kbd> seçeneğini seçerek yeni bir materyal oluşturun ve *`grade.material`* adını verin.
2. *Asset* görünümünde *main* klasörüne sağ tıklayıp <kbd>New ▸ Vertex program</kbd> ve <kbd>New ▸ Fragment program</kbd> seçeneklerini seçerek *`grade.vp`* adlı bir köşe gölgelendiricisi programı ve *`grade.fp`* adlı bir parça gölgelendiricisi programı oluşturun.
3. *grade.material* dosyasını açın ve *Vertex program* ile *Fragment program* özelliklerini yeni gölgelendirici programı dosyalarına ayarlayın.
4. `CONSTANT_TYPE_VIEWPROJ` türünde "`view_proj`" adlı bir *Vertex constant* ekleyin. Bu, kare köşeleri için köşe programında kullanılan görünüm ve izdüşüm matrisidir.
5. "`original`" adlı bir *Sampler* ekleyin. Bu, ekran dışı işleme hedefinin renk arabelleğinden pikselleri örneklemek için kullanılacaktır.
6. "`grade`" adlı bir *Tag* ekleyin. Kareyi çizmek için işleme betiğinde bu etiketle eşleşen yeni bir *işleme yüklemi (render predicate)* oluşturacağız.

   ![grade.material](images/grading/grade_material.png)

7. *`main.collection`* dosyasını açın, "`grade`" oyun nesnesindeki model bileşenini seçin ve *Material* özelliğini "`/main/grade.material`" olarak ayarlayın.

   ![Model özellikleri](images/grading/model_properties.png)

8. Köşe gölgelendiricisi programı, temel şablondan oluşturulduğu hâliyle bırakılabilir:

    ```glsl
    // grade.vp
    uniform mediump mat4 view_proj;

    // positions are in world space
    attribute mediump vec4 position;
    attribute mediump vec2 texcoord0;

    varying mediump vec2 var_texcoord0;

    void main()
    {
      gl_Position = view_proj * vec4(position.xyz, 1.0);
      var_texcoord0 = texcoord0;
    }
    ```

9. Parça gölgelendiricisi programında, `gl_FragColor` değerini doğrudan örneklenen renk değerine ayarlamak yerine basit bir renk değişikliği yapalım. Bunu esas olarak buraya kadar her şeyin beklendiği gibi çalıştığından emin olmak için yapıyoruz:

    ```glsl
    // grade.fp
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;

    void main()
    {
      vec4 color = texture2D(original, var_texcoord0.xy);
      // Desaturate the color sampled from the original texture
      float grey = color.r * 0.3 + color.g * 0.59 + color.b * 0.11;
      gl_FragColor = vec4(grey, grey, grey, 1.0);
    }
    ```

Artık kare modelimiz, materyali ve gölgelendiricileriyle birlikte hazır. Yalnızca onu ekranın kare arabelleğine çizmemiz gerekiyor.

## Ekran dışı arabelleği doku olarak kullanma

Kare modeli çizebilmek için işleme betiğine bir işleme yüklemi eklememiz gerekiyor. *`grade.render_script`* dosyasını açın ve `init()` işlevini düzenleyin:

```lua
function init(self)
    self.tile_pred = render.predicate({"tile"})
    self.gui_pred = render.predicate({"gui"})
    self.text_pred = render.predicate({"text"})
    self.particle_pred = render.predicate({"particle"})
    self.grade_pred = render.predicate({"grade"}) -- <1>

    ...
end
```
1. *`grade.material`* dosyasında belirlediğimiz "grade" etiketiyle eşleşen yeni bir yüklem ekleyin.

`update()` içinde işleme hedefinin renk arabelleği doldurulduktan sonra, kare modelin tüm ekranı doldurmasını sağlayan bir görünüm ve izdüşüm ayarlarız. Ardından işleme hedefinin renk arabelleğini karenin dokusu olarak kullanırız:

```lua
function update(self)
  render.set_render_target(self.target)

  ...

  render.set_render_target(render.RENDER_TARGET_DEFAULT)

  render.clear({[graphics.BUFFER_TYPE_COLOR0_BIT] = self.clear_color}) -- <1>

  render.set_viewport(0, 0, render.get_window_width(), render.get_window_height()) -- <2>
  render.set_view(vmath.matrix4()) -- <3>
  render.set_projection(vmath.matrix4())

  render.enable_texture(0, self.target, graphics.BUFFER_TYPE_COLOR0_BIT) -- <4>
  render.draw(self.grade_pred) -- <5>
  render.disable_texture(0, self.target) -- <6>
end
```
1. Kare arabelleğini temizleyin. Önceki `render.clear()` çağrısının ekranın kare arabelleğini değil, işleme hedefini etkilediğini unutmayın.
2. Görüntü alanını pencere boyutuyla eşleşecek şekilde ayarlayın.
3. Görünümü birim matrise ayarlayın. Bu, kameranın başlangıç noktasında olduğu ve doğrudan Z ekseni boyunca baktığı anlamına gelir. Ayrıca izdüşümü de birim matrise ayarlayarak karenin tüm ekranı kaplayacak şekilde düz olarak yansıtılmasını sağlayın.
4. 0 numaralı doku yuvasını işleme hedefinin renk arabelleğine ayarlayın. *`grade.material`* dosyamızın 0 numaralı yuvasında "original" örnekleyicisi bulunduğundan, parça gölgelendiricisi işleme hedefinden örnekleme yapacaktır.
5. "grade" etiketine sahip herhangi bir materyalle eşleşen, oluşturduğumuz yüklemi çizin. Kare model, bu etiketi belirleyen *`grade.material`* materyalini kullanır; böylece kare çizilecektir.
6. Çizimden sonra, işimiz bittiği için 0 numaralı doku yuvasını devre dışı bırakın.

Şimdi oyunu çalıştırıp sonucu görelim:

![Renk doygunluğu kaldırılmış oyun](images/grading/desaturated_game.png)

## Renk düzenleme

Renkler, her biri rengin ne kadar kırmızı, yeşil veya maviden oluştuğunu belirleyen üç bileşen değeriyle ifade edilir. Siyahtan kırmızı, yeşil, mavi, sarı ve pembeye, oradan beyaza uzanan tüm renk tayfı bir küp biçimine sığdırılabilir:

![Renk küpü](images/grading/color_cube.png)

Ekranda gösterilebilen her renk bu renk küpünde bulunabilir. Renk düzenlemenin temel fikri, böyle bir renk küpünü renklerini değiştirerek 3B bir *arama tablosu (lookup table)* olarak kullanmaktır.

Her piksel için:

1. Renginin renk küpündeki konumunu (kırmızı, yeşil ve mavi değerlerine göre) bulun.
2. Renkleri düzenlenmiş küpte o konumda hangi rengin saklandığını *okuyun*.
3. Pikseli özgün rengi yerine okunan renkte çizin.

Bunu parça gölgelendiricimizde yapabiliriz:

1. Ekran dışı arabellekteki her pikselin renk değerini örnekleyin.
2. Örneklenen pikselin renk konumunu, renkleri düzenlenmiş bir renk küpünde bulun.
3. Çıktı parçasının rengini aramayla bulunan değere ayarlayın.

![İşleme hedefinde renk düzenleme](images/grading/render_target_grading.png)

## Arama tablosunu temsil etme

Open GL ES 2.0, 3B dokuları desteklemediğinden 3B renk küpünü temsil etmenin başka bir yolunu bulmamız gerekiyor. Bunun yaygın bir yolu, küpü Z ekseni (mavi) boyunca dilimlemek ve her dilimi iki boyutlu bir ızgarada yan yana yerleştirmektir. 16 dilimin her biri 16⨉16 piksellik bir ızgara içerir. Bunu, parça gölgelendiricisinde bir örnekleyiciyle okuyabileceğimiz bir dokuda saklarız:

![Arama dokusu](images/grading/lut.png)

Elde edilen doku 16 hücre (her mavi renk yoğunluğu için bir hücre) ve her hücre içinde X ekseni boyunca 16 kırmızı renk, Y ekseni boyunca da 16 yeşil renk içerir. Doku, 16 milyon renkli RGB renk uzayının tamamını yalnızca 4096 renkle, yani sadece 4 bit renk derinliğiyle temsil eder. Çoğu ölçüte göre bu berbat olsa da GL grafik donanımının bir özelliği sayesinde çok yüksek renk doğruluğunu geri kazanabiliriz. Nasıl olduğunu görelim.

## Renkleri arama

Bir rengi bulmak için mavi bileşeni kontrol edip kırmızı ve yeşil değerlerin hangi hücreden alınacağını belirlemek gerekir. Doğru kırmızı-yeşil renk kümesine sahip hücreyi bulmanın formülü basittir:

```math
cell = \left \lfloor{B \times (N - 1)} \right \rfloor
```

Burada `B`, 0 ile 1 arasındaki mavi bileşen değeri; `N` ise toplam hücre sayısıdır. Bizim durumumuzda hücre numarası `0`--`15` aralığında olacaktır. `0` numaralı hücre mavi bileşeni `0` olan tüm renkleri, `15` numaralı hücre ise mavi bileşeni `1` olan tüm renkleri içerir.

Örneğin, `(0.63, 0.83, 0.4)` RGB değeri, mavi değeri `0.4` olan tüm renklerin bulunduğu hücrede, yani 6 numaralı hücrede bulunur. Bunu bildikten sonra yeşil ve kırmızı değerlere göre son doku koordinatlarını bulmak basittir:

![Arama tablosu](images/grading/lut_lookup.png)

Kırmızı ve yeşil değerler olan `(0, 0)` değerlerini sol alt pikselin *merkezinde*, `(1.0, 1.0)` değerlerini ise sağ üst pikselin *merkezinde* kabul etmemiz gerektiğine dikkat edin.

::: sidenote
Sol alt pikselin merkezinden başlayıp sağ üst pikselin merkezine kadar okumamızın nedeni, geçerli hücrenin dışındaki hiçbir pikselin örneklenen değeri etkilemesini istemememizdir. Aşağıdaki filtreleme açıklamasına bakın.
:::

Dokunun bu belirli koordinatlarında örnekleme yaptığımızda, tam 4 pikselin ortasına denk geldiğimizi görürüz. Peki GL bu noktanın renk değeri olarak bize ne söyleyecek?

![Arama tablosunda filtreleme](images/grading/lut_filtering.png)

Yanıt, materyalde örnekleyicinin *filtrelemesini* nasıl belirlediğimize bağlıdır.

- Örnekleyicinin filtrelemesi `NEAREST` ise GL, en yakın pikselin renk değerini döndürür (konum değeri aşağı yuvarlanır). Yukarıdaki durumda GL, `(0.60, 0.80)` konumundaki renk değerini döndürür. 4 bitlik arama dokumuz için bu, renk değerlerini toplamda yalnızca 4096 renge nicemleyeceğimiz anlamına gelir.

- Örnekleyicinin filtrelemesi `LINEAR` ise GL, *ara değerlemeyle (interpolation) hesaplanmış* renk değerini döndürür. GL, örnekleme konumunun çevresindeki piksellere olan uzaklığa göre bir renk karışımı oluşturur. Yukarıdaki durumda GL, örnekleme noktasının çevresindeki 4 pikselin her birinden %25 içeren bir renk döndürür.

Böylece doğrusal filtreleme kullanarak renk nicemlemesini ortadan kaldırır ve oldukça küçük bir arama tablosundan çok iyi renk hassasiyeti elde ederiz.

## Aramayı uygulama

Parça gölgelendiricisinde doku aramasını uygulayalım:

1. *`grade.material`* dosyasını açın.
2. Arama tablosu (lookup table) için "`lut`" adlı ikinci bir örnekleyici ekleyin.
3. *`Filter min`* özelliğini `FILTER_MODE_MIN_LINEAR`, *`Filter mag`* özelliğini ise `FILTER_MODE_MAG_LINEAR` olarak ayarlayın.

    ![Arama tablosu örnekleyicisi](images/grading/material_lut_sampler.png)

4. Aşağıdaki arama tablosu dokusunu (*`lut16.png`*) indirip projenize ekleyin.

    ![16 renkli arama tablosu](images/grading/lut16.png)

5. *`main.collection`* dosyasını açın ve *`lut`* doku özelliğini indirdiğiniz arama dokusuna ayarlayın.

    ![Kare modelin arama tablosu](images/grading/quad_lut.png)

6. Son olarak, renk arama desteğini ekleyebilmemiz için *`grade.fp`* dosyasını açın:

    ```glsl
    varying mediump vec4 position;
    varying mediump vec2 var_texcoord0;

    uniform lowp sampler2D original;
    uniform lowp sampler2D lut; // <1>

    #define MAXCOLOR 15.0 // <2>
    #define COLORS 16.0
    #define WIDTH 256.0
    #define HEIGHT 16.0

    void main()
    {
        vec4 px = texture2D(original, var_texcoord0.xy); // <3>

        float cell = floor(px.b * MAXCOLOR); // <4>

        float half_px_x = 0.5 / WIDTH; // <5>
        float half_px_y = 0.5 / HEIGHT;

        float x_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
        float y_offset = half_px_y + px.g * (MAXCOLOR / COLORS); // <6>

        vec2 lut_pos = vec2(cell / COLORS + x_offset, y_offset); // <7>

        vec4 graded_color = texture2D(lut, lut_pos); // <8>

        gl_FragColor = graded_color; // <9>
    }
    ```
    1. `lut` örnekleyicisini bildirin.
    2. En büyük renk değeri (0'dan başladığımız için 15), kanal başına renk sayısı ve arama dokusunun genişliği ile yüksekliği için sabitler.
    3. Özgün dokudan (ekran dışı işleme hedefinin renk arabelleğinden) bir piksel rengini (`px` adıyla) örnekleyin.
    4. `px` değerinin mavi kanal değerine göre rengin hangi hücreden okunacağını hesaplayın.
    5. Piksel merkezlerinden okumak için yarım piksellik kaydırmaları hesaplayın.
    6. `px` değerinin kırmızı ve yeşil değerlerine göre doku üzerindeki X ve Y kaydırmalarını hesaplayın.
    7. Arama dokusundaki son örnekleme konumunu hesaplayın.
    8. Arama dokusundan sonuç rengini örnekleyin.
    9. Karenin dokusundaki rengi sonuç rengine ayarlayın.

Şu anda arama tablosu dokusu, aradığımız renk değerlerini olduğu gibi döndürüyor. Bu, oyunun özgün renkleriyle işlenmesi gerektiği anlamına gelir:

![Dünyanın özgün görünümü](images/grading/world_original.png)

Buraya kadar her şeyi doğru yapmışız gibi görünüyor, ancak yüzeyin altında gizlenen bir sorun var. Degrade test dokusuna sahip bir sprite bileşeni eklediğimizde neler olduğuna bakın:

![Mavide bantlaşma](images/grading/blue_banding.png)

Mavi degradede gerçekten çirkin bantlaşmalar görülüyor. Bunun nedeni ne?

## Mavi kanalda ara değerleme

Mavi kanaldaki bantlaşma sorunu, GL'nin rengi dokudan okurken mavi kanalda herhangi bir ara değerleme yapamamasından kaynaklanır. Mavi renk değerine göre okunacak belirli bir hücreyi önceden seçeriz ve işlem burada biter. Örneğin, mavi kanal `0.400`--`0.466` aralığında herhangi bir değer içeriyorsa değerin tam olarak ne olduğu önemli değildir: son rengi her zaman mavi kanalın `0.400` olarak ayarlandığı 6 numaralı hücreden örnekleriz.

Mavi kanalda daha iyi çözünürlük elde etmek için ara değerlemeyi kendimiz uygulayabiliriz. Mavi değer iki komşu hücrenin değeri arasındaysa bu hücrelerin her ikisinden de örnekleme yapıp renkleri karıştırabiliriz. Örneğin, mavi değer `0.420` ise 6 numaralı hücreden *ve* 7 numaralı hücreden örnekleme yapıp ardından renkleri karıştırmalıyız.

Dolayısıyla iki hücreden okumalıyız:

```math
cell_{low} = \left \lfloor{B \times (N - 1)} \right \rfloor
```

ve:

```math
cell_{high} = \left \lceil{B \times (N - 1)} \right \rceil
```

Ardından bu hücrelerin her birinden renk değerlerini örnekleyip şu formüle göre renkler arasında doğrusal ara değerleme yaparız:

```math
color = color_{low} \times (1 - C_{frac}) + color_{high} \times C_{frac}
```

Burada `color`~low~, daha düşük numaralı (en soldaki) hücreden örneklenen renk; `color`~high~ ise daha yüksek numaralı (en sağdaki) hücreden örneklenen renktir. GLSL'nin `mix()` işlevi bu doğrusal ara değerlemeyi bizim için yapar.

Yukarıdaki `C~frac~` değeri, mavi kanal değerinin `0`--`15` renk aralığına ölçeklenmiş hâlinin kesirli kısmıdır:

```math
C_{frac} = B \times (N - 1) - \left \lfloor{B \times (N - 1)} \right \rfloor
```

Bir değerin kesirli kısmını veren bir GLSL işlevi de vardır. Bu işlev `frac()` olarak adlandırılır. Parça gölgelendiricisindeki (*`grade.fp`*) son uygulama oldukça basittir:

```glsl
varying mediump vec4 position;
varying mediump vec2 var_texcoord0;

uniform lowp sampler2D original;
uniform lowp sampler2D lut;

#define MAXCOLOR 15.0
#define COLORS 16.0
#define WIDTH 256.0
#define HEIGHT 16.0

void main()
{
  vec4 px = texture2D(original, var_texcoord0.xy);

    float cell = px.b * MAXCOLOR;

    float cell_l = floor(cell); // <1>
    float cell_h = ceil(cell);

    float half_px_x = 0.5 / WIDTH;
    float half_px_y = 0.5 / HEIGHT;
    float r_offset = half_px_x + px.r / COLORS * (MAXCOLOR / COLORS);
    float g_offset = half_px_y + px.g * (MAXCOLOR / COLORS);

    vec2 lut_pos_l = vec2(cell_l / COLORS + r_offset, g_offset); // <2>
    vec2 lut_pos_h = vec2(cell_h / COLORS + r_offset, g_offset);

    vec4 graded_color_l = texture2D(lut, lut_pos_l); // <3>
    vec4 graded_color_h = texture2D(lut, lut_pos_h);

    // <4>
    vec4 graded_color = mix(graded_color_l, graded_color_h, fract(cell));

    gl_FragColor = graded_color;
}
```

1. Okunacak iki komşu hücreyi hesaplayın.
2. Her hücre için bir tane olmak üzere iki ayrı arama konumu hesaplayın.
3. Hücre konumlarından iki rengi örnekleyin.
3. Ölçeklenmiş mavi renk değeri olan `cell` değerinin kesirli kısmına göre renkleri doğrusal olarak karıştırın.

Oyunu test dokusuyla yeniden çalıştırmak artık çok daha iyi sonuçlar verir. Mavi kanaldaki bantlaşma kaybolmuştur:

![Mavide bantlaşma yok](images/grading/blue_no_banding.png)

## Arama dokusunun renklerini düzenleme

Pekâlâ, özgün oyun dünyasıyla tamamen aynı görünen bir şey çizmek için epey uğraştık. Ancak bu düzenek gerçekten harika bir şey yapmamızı sağlıyor. Sıkı durun!

1. Oyunun üzerinde değişiklik yapılmamış hâlinin ekran görüntüsünü alın.
2. Ekran görüntüsünü tercih ettiğiniz görüntü düzenleme programında açın.
3. İstediğiniz sayıda renk ayarı (parlaklık, karşıtlık, renk eğrileri, beyaz dengesi, pozlama vb.) uygulayın.

![Affinity'de dünya](images/grading/world_graded_affinity.png)

4. Aynı renk ayarlarını arama tablosu dokusu dosyasına (*`lut16.png`*) uygulayın.
5. Renkleri ayarlanmış arama tablosu dokusu dosyasını kaydedin.
6. Defold projenizde kullanılan *`lut16.png`* dokusunu renkleri ayarlanmış olanla değiştirin.
7. Oyunu çalıştırın!

![Renkleri düzenlenmiş dünya](images/grading/world_graded.png)

İşte bu!
