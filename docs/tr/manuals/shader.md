---
title: Defold'da gölgelendirici programları
brief: Bu kılavuz, köşe ve parça gölgelendiricilerini ve bunların Defold'da nasıl kullanılacağını ayrıntılı olarak açıklar.
---

# Gölgelendiriciler

Gölgelendirici (shader) programları, grafiklerden görüntü oluşturan işleme (rendering) sürecinin temelindedir. Bunlar, GLSL (GL Shading Language) adı verilen C benzeri bir dilde yazılan ve grafik donanımının, temel alınan 3B veriler (köşeler) veya ekranda beliren pikseller ("parçalar") üzerinde işlemler yapmak için çalıştırdığı programlardır. Gölgelendiriciler; sprite bileşenlerini çizmek, 3B modelleri aydınlatmak, tam ekran son işleme efektleri oluşturmak ve daha pek çok şey için kullanılır.

Bu kılavuz, Defold'un işleme hattının (rendering pipeline) GPU gölgelendiricileriyle nasıl etkileşim kurduğunu açıklar. İçeriğiniz için gölgelendiriciler oluşturmak üzere materyal (material) kavramını ve işleme hattının nasıl çalıştığını da anlamanız gerekir.

* İşleme hattıyla ilgili ayrıntılar için [İşleme kılavuzuna](/manuals/render) bakın.
* Materyallerle ilgili ayrıntılar için [Materyal kılavuzuna](/manuals/material) bakın.
* Hesaplama programlarıyla ilgili ayrıntılar için [Hesaplama kılavuzuna](/manuals/compute) bakın.

OpenGL ES 2.0 (OpenGL for Embedded Systems) ve OpenGL ES Shading Language belirtimlerini [Khronos OpenGL Registry](https://www.khronos.org/registry/gles/) sitesinde bulabilirsiniz.

Masaüstü bilgisayarlarda, OpenGL ES 2.0'da bulunmayan özellikleri kullanarak gölgelendiriciler yazmanın mümkün olduğunu unutmayın. Ekran kartı sürücünüz, mobil cihazlarda çalışmayacak gölgelendirici kodunu sorunsuzca derleyip çalıştırabilir.


## Kavramlar

Köşe gölgelendiricisi
: Bir köşe gölgelendiricisi (vertex shader) köşe oluşturamaz veya silemez; yalnızca bir köşenin konumunu değiştirebilir. Köşe gölgelendiricileri genellikle köşelerin konumlarını 3B dünya uzayından 2B ekran uzayına dönüştürmek için kullanılır.

  Bir köşe gölgelendiricisinin girdisi, köşe verileri (`attributes` biçiminde) ve sabitlerdir (`uniforms`). Yaygın kullanılan sabitler, bir köşenin konumunu ekran uzayına dönüştürmek ve izdüşürmek için gereken matrislerdir.

  Köşe gölgelendiricisinin çıktısı, köşenin hesaplanan ekran konumudur (`gl_Position`). Köşe gölgelendiricisinden parça gölgelendiricisine `varying` değişkenleri aracılığıyla veri aktarmak da mümkündür.

Parça gölgelendiricisi
: Köşe gölgelendiricisinin işi bittiğinde, oluşan temel geometrik şekillerin (primitive) her bir parçasının (veya pikselinin) rengini belirlemek parça gölgelendiricisinin (fragment shader) görevidir.

  Bir parça gölgelendiricisinin girdisi, sabitler (`uniforms`) ve köşe gölgelendiricisinin ayarladığı tüm `varying` değişkenleridir.

  Parça gölgelendiricisinin çıktısı, ilgili parçanın renk değeridir (`gl_FragColor`).

Hesaplama gölgelendiricisi
: Bir hesaplama gölgelendiricisi (compute shader), GPU üzerinde her tür işi gerçekleştirmek için kullanılabilen genel amaçlı bir gölgelendiricidir. Grafik hattının bir parçası değildir; hesaplama gölgelendiricileri ayrı bir yürütme bağlamında çalışır ve başka bir gölgelendiriciden gelen girdiye bağımlı değildir.

  Bir hesaplama gölgelendiricisinin girdisi, sabit arabellekleri (`uniforms`), doku görüntüleri (`image2D`), örnekleyiciler (`sampler2D`) ve depolama arabellekleridir (`buffer`).

  Hesaplama gölgelendiricisinin çıktısı açıkça tanımlanmaz; köşe ve parça gölgelendiricilerinden farklı olarak üretilmesi gereken belirli bir çıktı yoktur. Hesaplama gölgelendiricileri genel amaçlı olduğu için hesaplama gölgelendiricisinin ne tür bir sonuç üretmesi gerektiğini tanımlamak programcıya bağlıdır.

Dünya matrisi
: Bir modelin şeklini oluşturan köşelerin konumları, modelin başlangıç noktasına göre saklanır. Buna "model uzayı" (model space) denir. Oyun dünyası ise her köşenin konumunun, yöneliminin ve ölçeğinin dünyanın başlangıç noktasına göre ifade edildiği bir "dünya uzayıdır" (world space). Oyun motoru bunları ayrı tutarak her modeli, model bileşeninde (model component) saklanan özgün köşe değerlerini bozmadan taşıyabilir, döndürebilir ve ölçeklendirebilir.

  Bir model oyun dünyasına yerleştirildiğinde, modelin yerel köşe koordinatlarının dünya koordinatlarına dönüştürülmesi gerekir. Bu dönüşüm, modelin köşelerinin oyun dünyasının koordinat sistemine doğru yerleştirilmesi için hangi öteleme (hareket), dönme ve ölçeğin uygulanması gerektiğini belirten bir *dünya dönüşüm matrisi* (world transform matrix) ile yapılır.

  ![Dünya dönüşümü](images/shader/world_transform.png)

Görünüm ve izdüşüm matrisi
: Oyun dünyasındaki köşeleri ekrana yerleştirmek için önce her matrisin 3B koordinatları kameraya göre koordinatlara dönüştürülür. Bu, bir _görünüm matrisi_ (view matrix) ile yapılır. İkinci olarak, köşeler bir _izdüşüm matrisi_ (projection matrix) ile 2B ekran uzayına izdüşürülür:

  ![İzdüşüm](images/shader/projection.png)

Öznitelikler
: Tek bir köşeyle ilişkili değer. Öznitelikler (attributes) motordan gölgelendiriciye aktarılır; bir özniteliğe erişmek isterseniz onu gölgelendirici programınızda bildirmeniz yeterlidir. Farklı bileşen türlerinin farklı öznitelik kümeleri vardır:
  - Sprite bileşeninde `position` ve `texcoord0` bulunur.
  - Tilegrid bileşeninde `position` ve `texcoord0` bulunur.
  - GUI düğümünde `position`, `textcoord0` ve `color` bulunur.
  - ParticleFX bileşeninde `position`, `texcoord0` ve `color` bulunur.
  - Model bileşeninde `position`, `texcoord0` ve `normal` bulunur.
  - Yazı tipinde `position`, `texcoord0`, `face_color`, `outline_color` ve `shadow_color` bulunur.

Sabitler
: Gölgelendirici sabitleri, işleme çizim çağrısı boyunca sabit kalır. Sabitler, materyal dosyasındaki *Constants* bölümlerine eklenir ve ardından gölgelendirici programında `uniform` olarak bildirilir. Örnekleyici uniform değişkenleri, materyalin *Samplers* bölümüne eklenir ve ardından gölgelendirici programında `uniform` olarak bildirilir. Bir köşe gölgelendiricisinde köşe dönüşümlerini gerçekleştirmek için gereken matrisler sabit olarak sunulur:

  - `CONSTANT_TYPE_WORLD`, bir nesnenin yerel koordinat uzayından dünya uzayına eşleyen *dünya matrisidir*.
  - `CONSTANT_TYPE_VIEW`, dünya uzayından kamera uzayına eşleyen *görünüm matrisidir*.
  - `CONSTANT_TYPE_PROJECTION`, kamera uzayından ekran uzayına eşleyen *izdüşüm matrisidir*.
  - `CONSTANT_TYPE_WORLDVIEW`, `CONSTANT_TYPE_VIEWPROJ` ve `CONSTANT_TYPE_WORLDVIEWPROJ`, ilgili birleşik matrisleri sağlar.
  - `CONSTANT_TYPE_WORLD_INVERSE`, `CONSTANT_TYPE_VIEW_INVERSE`, `CONSTANT_TYPE_PROJECTION_INVERSE`, `CONSTANT_TYPE_VIEWPROJ_INVERSE`, `CONSTANT_TYPE_WORLDVIEW_INVERSE` ve `CONSTANT_TYPE_WORLDVIEWPROJ_INVERSE`, gölgelendiricinin bunları hesaplamasına gerek kalmadan ters matrisleri sağlar.
  - `CONSTANT_TYPE_TIME`, motorun sağladığı bir `vec4` değeridir: `.x` içinde motorun başlangıcından bu yana geçen süre, `.y` içinde kare zaman farkı, `.z` ve `.w` içinde ise sıfır bulunur.
  - `CONSTANT_TYPE_USER`, istediğiniz gibi kullanabileceğiniz `vec4` türünde bir sabittir.

  [Materyal kılavuzu](/manuals/material), sabitlerin nasıl belirtileceğini açıklar.

Örnekleyiciler
: Gölgelendiriciler, *örnekleyici* (sampler) türünde uniform değişkenleri bildirebilir. Örnekleyiciler bir görüntü kaynağından değer okumak için kullanılır:

  - `sampler2D`, 2B görüntü dokusundan örnekleme yapar.
  - `sampler2DArray`, 2B görüntü dizisi dokusundan örnekleme yapar. Bu, çoğunlukla sayfalı atlaslar için kullanılır.
  - `samplerCube`, 6 görüntüden oluşan küp haritası dokusundan örnekleme yapar.
  - `image2D`, doku verilerini bir görüntü nesnesine yükler (ve gerektiğinde kaydeder). Bu, çoğunlukla hesaplama gölgelendiricilerinde depolama için kullanılır.

  Bir örnekleyiciyi yalnızca GLSL standart kütüphanesinin doku arama işlevlerinde kullanabilirsiniz. [Materyal kılavuzu](/manuals/material), örnekleyici ayarlarının nasıl belirtileceğini açıklar.

UV koordinatları
: Bir köşeyle bir 2B koordinat ilişkilendirilir ve bu koordinat 2B dokudaki bir noktaya eşlenir. Böylece dokunun bir kısmı veya tamamı, bir köşe kümesinin tanımladığı şekle boyanabilir.

  ![UV koordinatları](images/shader/uv_map.png)

  UV haritası genellikle 3B modelleme programında oluşturulur ve örgüde (mesh) saklanır. Her köşenin doku koordinatları, köşe gölgelendiricisine bir öznitelik olarak sağlanır. Ardından her parçanın UV koordinatını köşe değerlerinden ara değerleme (interpolation) yoluyla bulmak için bir `varying` değişkeni kullanılır.

Varying değişkenleri
: `Varying` türündeki değişkenler, köşe aşaması ile parça aşaması arasında bilgi aktarmak için kullanılır.

  1. Köşe gölgelendiricisinde her köşe için bir varying değişkeni ayarlanır.
  2. Rasterleştirme (rasterization) sırasında, işlenen temel geometrik şeklin her parçası için bu değerin ara değerlemesi yapılır. Parçanın şeklin köşelerine olan uzaklığı, ara değerlenmiş değeri belirler.
  3. Değişken, parça gölgelendiricisinin her çağrısı için ayarlanır ve parça hesaplamalarında kullanılabilir.

  ![Varying ara değerlemesi](images/shader/varying_vertex.png)

  Örneğin, bir üçgenin her köşesinde bir `varying` değişkenini `vec3` RGB renk değerine ayarlamak, renklerin şeklin tamamı boyunca ara değerlenmesini sağlar. Benzer şekilde, bir dikdörtgenin her köşesinde doku haritası arama koordinatlarını (veya *UV koordinatlarını*) ayarlamak, parça gölgelendiricisinin şeklin tüm alanı için doku renk değerlerini aramasını sağlar.

  ![Varying ara değerlemesi](images/shader/varying.png)

## Modern GLSL gölgelendiricileri yazma

Defold motoru birden çok platformu ve grafik API'sini desteklediği için geliştiricilerin her yerde çalışan gölgelendiriciler yazması basit olmalıdır. Varlık işleme hattı bunu başlıca iki yolla sağlar (bunlar bundan sonra gölgelendirici hatları, yani `shader pipelines` olarak anılacaktır):

1. Gölgelendiricilerin ES2 uyumlu GLSL koduyla yazıldığı eski hat.
2. Gölgelendiricilerin SPIR-v uyumlu GLSL koduyla yazıldığı modern hat.

Defold 1.9.2'den itibaren yeni hattı kullanan gölgelendiriciler yazmanız önerilir; bunu sağlamak için çoğu gölgelendiricinin en az sürüm 140 (OpenGL 3.1) ile yazılmış gölgelendiricilere dönüştürülmesi gerekir. Bir gölgelendiriciyi dönüştürmek için şu gereksinimlerin karşılandığından emin olun:

### Sürüm bildirimi
Gölgelendiricinin en üstüne en az #version 140 yerleştirin:

```glsl
#version 140
```

Proje derleme sürecinde gölgelendirici hattı bu şekilde seçilir; bu nedenle eski gölgelendiricileri kullanmaya devam edebilirsiniz. Sürüm belirten bir önişlemci yönergesi bulunmazsa Defold eski hattı kullanır.

### Öznitelikler
Köşe gölgelendiricilerinde `attribute` anahtar sözcüğünü `in` ile değiştirin:

```glsl
// instead of:
// attribute vec4 position;
// do:
in vec4 position;
```

Not: Parça gölgelendiricileri (ve hesaplama gölgelendiricileri) köşe girdisi almaz.

### Varying değişkenleri
Köşe gölgelendiricilerinde varying değişkenlerinin önüne `out` eklenmelidir. Parça gölgelendiricilerinde varying değişkenleri `in` olur:

```glsl
// In a vertex shader, instead of:
// varying vec4 var_color;
// do:
out vec4 var_color;

// In a fragment shader, instead of:
// varying vec4 var_color;
// do:
in vec4 var_color;
```

### Uniform değişkenleri (Defold'da sabitler olarak adlandırılır)

Opak (opaque) uniform türleri (örnekleyiciler, görüntüler, atomik türler, SSBO'lar) için herhangi bir dönüşüm gerekmez; bunları bugün olduğu gibi kullanabilirsiniz:

```glsl
uniform sampler2D my_texture;
uniform image2D my_image;
```

Opak olmayan uniform türlerini bir uniform bloğuna (`uniform block`) yerleştirmeniz gerekir. Uniform bloğu, uniform değişkenlerinden oluşan bir kümedir ve `uniform` anahtar sözcüğüyle bildirilir:

```glsl
uniform vertex_inputs
{
    mat4 mtx_world;
    mat4 mtx_proj;
    mat4 mtx_view;
    mat4 mtx_normal;
    ...
};

void main()
{
    // Individual members of the uniform block can be used as-is
    gl_Position = mtx_proj * mtx_view * mtx_world * vec4(position, 1.0);
}
```

Uniform bloğundaki tüm üyeler, materyallere ve bileşenlere ayrı sabitler olarak sunulur. İşleme sabit arabelleklerini veya `go.set` ve `go.get` işlevlerini kullanmak için herhangi bir dönüşüm gerekmez.

### Yerleşik değişkenler

Parça gölgelendiricilerinde, sürüm 140'tan itibaren `gl_FragColor` kullanımı önerilmez. Bunun yerine `out` kullanın:

```glsl
// instead of:
// gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
// do:
out vec4 color_out;

void main()
{
    color_out = vec4(1.0, 0.0, 0.0, 1.0);
}
```

### Doku işlevleri

`texture2D` ve `texture2DArray` gibi belirli doku örnekleme işlevleri artık yoktur. Bunların yerine yalnızca `texture` işlevini kullanın:

```glsl
uniform sampler2D my_texture;
uniform sampler2DArray my_texture_array;

// instead of:
// vec4 sampler_2d = texture2D(my_texture, uv);
// vec4 sampler_2d_array = texture2DArray(my_texture_array, vec3(uv, slice));
// do:
vec4 sampler_2d = texture(my_texture, uv);
vec4 sampler_2d_array = texture(my_texture_array, vec3(uv, slice));
```

### Hassasiyet {#precision}

Defold, gölgelendiricileri GLSL ES için çapraz derlerken genel varsayılan hassasiyet niteleyicileri oluşturur. Varsayılanlar, kayan noktalı değerler için `mediump` ve tamsayılar için `highp` değerleridir. Bunlar **GLSL ES Default Precision Float** (`shader.glsl_es_default_precision_float`) ve **GLSL ES Default Precision Int** (`shader.glsl_es_default_precision_int`) [proje ayarlarıyla](/manuals/project-settings/#shader) değiştirilebilir; her ikisi de `mediump` veya `highp` değerini kabul eder.

Bir değişken, girdi veya çıktı üzerindeki açık niteleyici, oluşturulan genel varsayılan değere göre önceliklidir. OpenGL ES 2.0 ve WebGL 1.0 parça gölgelendiricilerinde `highp`, her cihazda desteklenmez. Genel varsayılan olarak `highp` seçildiğinde Defold bunu `GL_FRAGMENT_PRECISION_HIGH` ile korur ve desteklemeyen cihazlarda `mediump` değerine geri döner.

### Hepsini bir araya getirme

Tüm bu kuralların uygulandığı son bir örnek olarak, yeni biçime dönüştürülmüş yerleşik sprite gölgelendiricileri aşağıdadır:

```glsl
#version 140

uniform vx_uniforms
{
    mat4 view_proj;
};

// positions are in world space
in vec4 position;
in vec2 texcoord0;

out vec2 var_texcoord0;

void main()
{
    gl_Position = view_proj * vec4(position.xyz, 1.0);
    var_texcoord0 = texcoord0;
}
```

```glsl
#version 140

in vec2 var_texcoord0;

out vec4 color_out;

uniform sampler2D texture_sampler;

uniform fs_uniforms
{
    vec4 tint;
};

void main()
{
    // Premultiply alpha since all runtime textures already are
    vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);
    color_out = texture(texture_sampler, var_texcoord0.xy) * tint_pm;
}

```

## Gölgelendiricilere kod parçaları dahil etme

Defold'daki gölgelendiriciler, proje içindeki `.glsl` uzantılı dosyalardan kaynak kod dahil etmeyi destekler. Bir gölgelendiriciden glsl dosyası dahil etmek için `#include` pragmasını çift tırnak veya ayraçlarla kullanın. Dahil etme yolları, projeye veya dosyayı dahil eden dosyaya göreli olmalıdır:

```glsl
// In file /main/my-shader.fp

// Absolute path
#include "/main/my-snippet.glsl"
// The file is in the same folder
#include "my-snippet.glsl"
// The file is in a sub-folder on the same level as 'my-shader'
#include "sub-folder/my-snippet.glsl"
// The file is in a sub-folder on the parent directory, i.e /some-other-folder/my-snippet.glsl
#include "../some-other-folder/my-snippet.glsl"
// The file is on the parent directory, i.e /root-level-snippet.glsl
#include "../root-level-snippet.glsl"
```

Dahil edilen dosyaların nasıl bulunacağıyla ilgili dikkat edilmesi gereken bazı noktalar vardır:

  - Dosyalar projeye göreli olmalıdır; yani yalnızca proje içindeki dosyaları dahil edebilirsiniz. Mutlak yolların başında `/` bulunmalıdır
  - Dosyanın herhangi bir yerine kod dahil edebilirsiniz, ancak bir dosyayı bir deyimin içine satır içi olarak dahil edemezsiniz. Örneğin, `const float #include "my-float-name.glsl" = 1.0` çalışmaz

### Başlık koruyucuları

Kod parçaları da başka `.glsl` dosyalarını dahil edebilir; bu, sonunda üretilen gölgelendiricinin aynı kodu birkaç kez içerebileceği anlamına gelir. Dosyaların içeriğine bağlı olarak aynı sembollerin birden fazla kez bildirilmesi nedeniyle kod derleme sorunlarıyla karşılaşabilirsiniz. Bunu önlemek için birçok programlama dilinde yaygın bir kavram olan *başlık koruyucularını* (header guards) kullanabilirsiniz. Örnek:

```glsl
// In my-shader.vs
#include "math-functions.glsl"
#include "pi.glsl"

// In math-functions.glsl
#include "pi.glsl"

// In pi.glsl
const float PI = 3.14159265359;
```

Bu örnekte `PI` sabiti iki kez tanımlanır; bu da projeyi çalıştırırken derleyici hatalarına neden olur. Bunun yerine içeriği başlık koruyucularıyla korumanız önerilir:

```glsl
// In pi.glsl
#ifndef PI_GLSL_H
#define PI_GLSL_H

const float PI = 3.14159265359;

#endif // PI_GLSL_H
```

`pi.glsl` dosyasındaki kod, `my-shader.vs` içinde iki kez açımlanır; ancak başlık koruyucularıyla çevrelediğiniz için PI sembolü yalnızca bir kez tanımlanır ve gölgelendirici başarıyla derlenir.

Ancak kullanım durumuna bağlı olarak bu her zaman kesinlikle gerekli değildir. Kodu bir işlevin içinde veya değerlerin gölgelendirici kodunun genelinde erişilebilir olmasına gerek olmayan başka bir yerde yerel olarak yeniden kullanmak istiyorsanız, büyük olasılıkla başlık koruyucularını kullanmamanız önerilir. Örnek:

```glsl
// In red-color.glsl
vec3 my_red_color = vec3(1.0, 0.0, 0.0);

// In my-shader.fp
vec3 get_red_color()
{
  #include "red-color.glsl"
  return my_red_color;
}

vec3 get_red_color_inverted()
{
  #include "red-color.glsl"
  return 1.0 - my_red_color;
}
```

## Düzenleyiciye özgü gölgelendirici kodu

Gölgelendiriciler Defold düzenleyicisinin görünüm alanında işlendiğinde `EDITOR` önişlemci tanımı kullanılabilir. Bu, düzenleyicide çalışırken asıl oyun motorunda çalıştığından farklı davranan gölgelendirici kodu yazmanızı sağlar.

Bu, özellikle şu amaçlar için kullanışlıdır:
  - Yalnızca düzenleyicide görünmesi gereken hata ayıklama görselleştirmeleri eklemek.
  - Tel kafes modları veya materyal önizlemeleri gibi düzenleyiciye özgü özellikler uygulamak.
  - Düzenleyicinin görünüm alanında düzgün çalışmayabilecek materyaller için yedek işleme sağlamak.

Yalnızca düzenleyicide çalışması gereken kodu koşullu olarak derlemek için `#ifdef EDITOR` önişlemci yönergesini kullanın:

```glsl
#ifdef EDITOR
    // This code will only execute when the shader is rendered in the Defold Editor
    color_out = vec4(1.0, 0.0, 1.0, 1.0); // Magenta color for editor preview
#else
    // This code will execute when running in the game
    color_out = texture(texture_sampler, var_texcoord0) * tint_pm;
#endif
```

## İşleme süreci

Oyununuz için oluşturduğunuz veriler, ekrana ulaşmadan önce bir dizi adımdan geçer:

![İşleme hattı](images/shader/pipeline.png)

Tüm görsel bileşenler (sprite bileşenleri, GUI düğümleri, parçacık efektleri veya modeller), 3B dünyada bileşenin şeklini tanımlayan noktalar olan köşelerden oluşur. Bunun iyi yanı, şekli herhangi bir açıdan ve uzaklıktan görüntülemenin mümkün olmasıdır. Köşe gölgelendirici programının görevi, tek bir köşeyi alıp görünüm alanındaki bir konuma dönüştürerek şeklin ekranda belirmesini sağlamaktır. 4 köşeli bir şekil için köşe gölgelendirici programı, her biri paralel olmak üzere 4 kez çalışır.

![Köşe gölgelendiricisi](images/shader/vertex_shader.png)

Programın girdisi köşe konumu (ve köşeyle ilişkili diğer öznitelik verileri), çıktısı ise yeni bir köşe konumu (`gl_Position`) ve her parça için ara değerlenmesi gereken tüm `varying` değişkenleridir.

En basit köşe gölgelendirici programı, çıktı konumunu yalnızca sıfır koordinatlı bir köşeye ayarlar (bu pek kullanışlı değildir):

```glsl
void main()
{
    gl_Position = vec4(0.0,0.0,0.0,1.0);
}
```

Daha kapsamlı bir örnek, yerleşik sprite köşe gölgelendiricisidir:

```glsl
-- sprite.vp
uniform mediump mat4 view_proj;             // [1]

attribute mediump vec4 position;            // [2]
attribute mediump vec2 texcoord0;

varying mediump vec2 var_texcoord0;         // [3]

void main()
{
  gl_Position = view_proj * vec4(position.xyz, 1.0);    // [4]
  var_texcoord0 = texcoord0;                            // [5]
}
```
1. Görünüm ve izdüşüm matrislerinin çarpımını içeren bir uniform (sabit).
2. Sprite köşesinin öznitelikleri. `position` zaten dünya uzayına dönüştürülmüştür. `texcoord0`, köşenin UV koordinatını içerir.
3. Bir varying çıktı değişkeni bildirin. Bu değişken, her köşe için ayarlanan değerler arasında her parça için ara değerlenir ve parça gölgelendiricisine gönderilir.
4. `gl_Position`, geçerli köşenin izdüşüm uzayındaki çıktı konumuna ayarlanır. Bu değerin 4 bileşeni vardır: `x`, `y`, `z` ve `w`. `w` bileşeni, perspektife uygun ara değerlemeyi hesaplamak için kullanılır. Herhangi bir dönüşüm matrisi uygulanmadan önce bu değer normalde her köşe için 1,0'dır.
5. Bu köşe konumu için varying UV koordinatını ayarlayın. Rasterleştirmeden sonra her parça için ara değerlenir ve parça gölgelendiricisine gönderilir.




Köşe gölgelendirmesinden sonra bileşenin ekrandaki şekli belirlenir: temel geometrik şekiller üretilir ve rasterleştirilir; yani grafik donanımı her şekli *parçalara* veya piksellere böler. Ardından parça gölgelendirici programını her parça için bir kez çalıştırır. Ekranda 16x24 piksel boyutundaki bir görüntü için program, her biri paralel olmak üzere 384 kez çalışır.

![Parça gölgelendiricisi](images/shader/fragment_shader.png)

Programın girdisi, işleme hattının ve köşe gölgelendiricisinin gönderdiği verilerdir; genellikle parçanın *UV koordinatları*, renk çarpanları vb. Çıktı, pikselin son rengidir (`gl_FragColor`).

En basit parça gölgelendirici programı, her pikselin rengini yalnızca siyaha ayarlar (yine pek kullanışlı bir program değildir):

```glsl
void main()
{
    gl_FragColor = vec4(0.0,0.0,0.0,1.0);
}
```

Yine daha kapsamlı bir örnek, yerleşik sprite parça gölgelendiricisidir:

```glsl
// sprite.fp
varying mediump vec2 var_texcoord0;             // [1]

uniform lowp sampler2D DIFFUSE_TEXTURE;         // [2]
uniform lowp vec4 tint;                         // [3]

void main()
{
  lowp vec4 tint_pm = vec4(tint.xyz * tint.w, tint.w);          // [4]
  lowp vec4 diff = texture2D(DIFFUSE_TEXTURE, var_texcoord0.xy);// [5]
  gl_FragColor = diff * tint_pm;                                // [6]
}
```
1. Varying doku koordinatı değişkeni bildirilir. Bu değişkenin değeri, şeklin her köşesi için ayarlanan değerler arasında her parça için ara değerlenir.
2. Bir `sampler2D` uniform değişkeni bildirilir. Örnekleyici, sprite bileşeninin doğru şekilde dokuyla kaplanabilmesi için ara değerlenmiş doku koordinatlarıyla birlikte doku araması yapmak üzere kullanılır. Bu bir sprite bileşeni olduğundan motor, bu örnekleyiciyi sprite bileşeninin *Image* özelliğinde ayarlanan görüntüye atar.
3. Materyalde `CONSTANT_TYPE_USER` türünde bir sabit tanımlanır ve `uniform` olarak bildirilir. Değeri, sprite bileşeninin renk çarpanıyla renklendirilmesini sağlamak için kullanılır. Varsayılan değer saf beyazdır.
4. Çalışma zamanındaki tüm dokular zaten önceden çarpılmış alfa içerdiği için renk çarpanının renk değeri alfa değeriyle önceden çarpılır.
5. Ara değerlenmiş koordinatta dokudan örnekleme yapın ve örneklenen değeri döndürün.
6. `gl_FragColor`, parçanın çıktı rengine ayarlanır: dokudaki dağınık renk, renk çarpanı değeriyle çarpılır.

Elde edilen parça değeri daha sonra testlerden geçer. Yaygın bir test olan *derinlik testinde* (depth test), parçanın derinlik değeri, test edilen pikselin derinlik arabelleği değeriyle karşılaştırılır. Teste bağlı olarak parça atılabilir veya derinlik arabelleğine yeni bir değer yazılır. Bu testin yaygın kullanımlarından biri, kameraya daha yakın grafiklerin daha gerideki grafikleri örtmesini sağlamaktır.

Test, parçanın kare arabelleğine yazılması gerektiği sonucuna varırsa parça, arabellekte zaten bulunan piksel verileriyle *harmanlanır*. İşleme betiğinde (render script) ayarlanan harmanlama parametreleri, kaynak rengin (parça gölgelendiricisinin yazdığı değer) ve hedef rengin (kare arabelleğindeki görüntünün rengi) çeşitli şekillerde birleştirilmesini sağlar. Harmanlamanın yaygın kullanımlarından biri, saydam nesnelerin işlenmesini sağlamaktır.

## İleri okuma

- [Shadertoy](https://www.shadertoy.com), kullanıcıların katkıda bulunduğu çok sayıda gölgelendirici içerir. Çeşitli gölgelendirme tekniklerini öğrenebileceğiniz harika bir ilham kaynağıdır. Sitede sergilenen gölgelendiricilerin birçoğu çok az çalışmayla Defold'a taşınabilir. [Shadertoy öğreticisi](https://www.defold.com/tutorials/shadertoy/), mevcut bir gölgelendiriciyi Defold'a dönüştürme adımlarını anlatır.

- [Renk derecelendirme öğreticisi](https://www.defold.com/tutorials/grading/), derecelendirme için renk arama tablosu dokularını kullanarak tam ekran renk derecelendirme efektinin nasıl oluşturulacağını gösterir.

- [The Book of Shaders](https://thebookofshaders.com/00/), gölgelendiricileri nasıl kullanıp projelerinize dahil edeceğinizi öğreterek projelerinizin performansını ve grafik kalitesini artırmanıza yardımcı olur.
