---
brief: Bu öğreticide shadertoy.com sitesindeki bir gölgelendiriciyi Defold için dönüştüreceksiniz.
layout: tutorial
locale: tr
title: Shadertoy'dan Defold'a dönüştürme öğreticisi
---

# Shadertoy öğreticisi

[Shadertoy.com](https://www.shadertoy.com/), kullanıcıların katkıda bulunduğu GL gölgelendiricilerini (shader) bir araya getiren bir sitedir. Gölgelendirici kodu bulmak ve ilham almak için harika bir kaynaktır. Bu öğreticide Shadertoy'dan bir gölgelendirici alıp Defold'da çalışır hâle getireceğiz. Gölgelendiriciler hakkında temel bilgiye sahip olduğunuz varsayılır. Konuyu öğrenmeniz gerekiyorsa [Gölgelendirici kılavuzu](/manuals/shader/) iyi bir başlangıç noktasıdır.

Kullanacağımız gölgelendirici, Pablo Andrioli tarafından (Shadertoy'daki kullanıcı adı "Kali") oluşturulan [Star Nest](https://www.shadertoy.com/view/XlfGRj). Tamamen prosedürel çalışan, matematiği kara büyüyü andıran bir parça gölgelendiricisidir (fragment shader); işleme (rendering) yoluyla gerçekten etkileyici bir yıldız alanı efekti oluşturur.

![Star Nest](../images/shadertoy/starnest.png)

Gölgelendirici, oldukça karmaşık yalnızca 65 satırlık GLSL kodundan oluşuyor; ancak endişelenmeyin. Onu, birkaç basit girdiye göre işini yapan bir kara kutu olarak ele alacağız. Buradaki işimiz, gölgelendiriciyi Shadertoy yerine Defold ile iletişim kuracak şekilde değiştirmek.

## Doku uygulanacak bir nesne

Star Nest gölgelendiricisi yalnızca bir parça gölgelendiricisidir; bu nedenle gölgelendiricinin doku (texture) uygulayacağı bir nesneye ihtiyacımız var. Bunun için birkaç seçenek bulunur: bir sprite bileşeni, karo haritası (tilemap), GUI veya model. Bu öğreticide basit bir 3B model kullanacağız. Bunun nedeni, modelin işlenmesini kolayca tam ekran efektine dönüştürebilmemizdir---örneğin görsel son işleme yapmak istiyorsak buna ihtiyacımız olur.

Boş bir projeyle başlayabiliriz.

1. Defold'u açın ve Create From bölümünde *Templates* seçeneğini seçin.
2. *Empty Project* seçeneğini seçin.
3. *Title* değerini ayarlayın ve diskinizdeki *Location* konumunu seçin.
4. <kbd>Create New Project</kbd> düğmesine tıklayın.

![başlangıç](../images/shadertoy/empty_project.png)

`builtins/assets/meshes` içindeki yerleşik `quad.gltf` örgüsünü (mesh) kullanabilirsiniz.

İsteğe bağlı olarak Blender'da veya başka bir 3B modelleme programında kare bir düzlem örgüsü de oluşturabilirsiniz --- kolaylık olması için 4 köşenin koordinatları X ekseninde -1 ve 1, Y ekseninde ise -1 ve 1 olacak şekilde ayarlanır. Blender'da Z ekseni varsayılan olarak yukarı yönlüdür; bu nedenle örgüyü X ekseni etrafında 90° döndürmeniz gerekir. Ayrıca örgü için doğru UV koordinatları oluşturduğunuzdan emin olmalısınız. Blender'da örgü seçiliyken *Edit Mode* moduna geçin, ardından <kbd>Mesh ▸ UV unwrap... ▸ Unwrap</kbd> seçeneğini seçin.

<div class='sidenote' markdown='1'>
Blender, [blender.org](https://www.blender.org) adresinden indirilebilen ücretsiz ve açık kaynaklı bir 3B yazılımıdır.
</div>

![Blender'da dörtgen](../images/shadertoy/quad_blender.png)

1. Defold'da "main.collection" dosyanızı açın ve "star-nest" adlı yeni bir oyun nesnesi (game object) oluşturun.
2. "star-nest" oyun nesnesine bir *Model* bileşeni (component) ekleyin.
3. *Mesh* özelliğini `quad.gltf` olarak ayarlayın.
4. Modelin materyalini (material) ayarlamamız gerekiyor; şimdilik yerleşik `model.material` dosyasını seçin.

Model sahne düzenleyicisinde görünmelidir, ancak tamamen siyah işlenir. Bunun nedeni, henüz bir dokusunun ayarlanmamış olmasıdır:

![Defold'da dörtgen](../images/shadertoy/quad_default_material.png)

## Materyali oluşturma

1. `Assets` bölmesindeki `main` klasörüne <kbd>Right Mouse Button</kbd> ile tıklayıp <kbd>New</kbd>-><kbd>Material</kbd> seçeneğini seçin ve `star-nest` adını vererek yeni bir *`star-nest.material`* materyal dosyası oluşturun.

 ![materyal](../images/shadertoy/new_material.png)

2. Aynı şekilde `star-nest.vp` adlı bir köşe gölgelendiricisi (vertex shader) programı ve `star-nest.fp` adlı bir parça gölgelendiricisi programı oluşturun:
3. *star-nest.material* dosyasını açın.
4. *Vertex Program* değerini `star-nest.vp` olarak ayarlayın.
5. *Fragment Program* değerini `star-nest.fp` olarak ayarlayın.
6. Bir *Vertex Constant* ekleyin ve adını "`view_proj`", türünü de `Viewproj` ("görünüm izdüşümü" için) olarak ayarlayın.
8. *Tags* bölümüne "tile" etiketini ekleyin. Böylece dörtgen, sprite bileşenleri ve karolar çizilirken yapılan işleme geçişine dahil edilir.

 ![materyal](../images/shadertoy/material.png)

### Köşe programı

1. `star-nest.vp` köşe gölgelendiricisi program dosyasını açın. Aşağıdaki kodu içermelidir:

    ```glsl
    #version 140

    // positions are in world space
    in vec4 position;
    in vec2 texcoord0;

    out vec2 var_texcoord0;

    uniform vertex_inputs
    {
        mat4 view_proj;
    };

    void main()
    {
        gl_Position = view_proj * vec4(position.xyz, 1.0);
        var_texcoord0 = texcoord0;
    }
    ```

### Parça programı

1. `star-nest.fp` parça gölgelendiricisi program dosyasını açın ve kodu, parça rengi UV koordinatlarının (`var_texcoord0`) X ve Y koordinatlarına göre ayarlanacak şekilde değiştirin. Bunu, modeli doğru kurduğumuzdan emin olmak için yapıyoruz:

    ```glsl
    #version 140

    in vec2 var_texcoord0;

    out vec4 out_fragColor;

    void main()
    {
        out_fragColor = vec4(var_texcoord0.xy, 0.0, 1.0);
    }
    ```

2. `main.collection` içindeki `star-nest` oyun nesnesinin model bileşeninde, `Material` özelliğini yeni oluşturduğumuz `star-nest` materyaline ayarlayın.

Artık düzenleyici modeli yeni gölgelendiriciyle işlemelidir ve UV koordinatlarının doğru olup olmadığını açıkça görebiliriz; sol alt köşe siyah (0, 0, 0), sol üst köşe yeşil (0, 1, 0), sağ üst köşe sarı (1, 1, 0) ve sağ alt köşe kırmızı (1, 0, 0) olmalıdır:

![Defold'da dörtgen](../images/shadertoy/quad_material.png)

## Kamera

Artık projeyi çalıştırabiliriz (<kbd>Project</kbd>-><kbd>Build</kbd> veya <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>B</kbd> kısayolu), ancak siyah bir ekran göreceğiz (aslında neredeyse tamamen siyah; sol alt köşede belki tek bir küçük piksel olabilir). Bunun nedeni, bir kameranın bulunmaması ve varsayılan işleme betiğinin (render script), çok geniş bir 2B uzayı gösteren basit bir yedek yöntem kullanmasıdır; oysa modelimiz (0,0,0) konumunda ve yalnızca 1 birim genişliğindedir.

Oyunda ne göreceğimizi belirlemek için kamera bileşeni olan bir oyun nesnesi ekleyelim.

1. (0,0,1) konumunda `camera` adlı bir oyun nesnesi ekleyin. (Z koordinatını 1 olarak ayarlamak önemlidir; böylece bu oyun nesnesi modelimizin önünde olur, çünkü varsayılan 2B kurulumda Z ekseni bize doğru bakar).
2. Bir `Camera` bileşeni ekleyin; içinde dörtgenimizin bulunduğu bir kamera önizlemesi göreceksiniz. Bu kurulumda varsayılan özellikler sayesinde hiçbir şeyi değiştirmeden doğru sonucu görebiliriz; tek bir şey hariç: bu kadar büyük bir kamera görüş hacmine (view frustum) ihtiyacımız yok, bu nedenle `Far Z` değerini `2` olarak azaltabiliriz.

![kamera](../images/shadertoy/camera.png)

İsteğe bağlı olarak `Orthographic Projection` değerini `true` yaparak kamera türünü değiştirebilir, ardından `Orthographic Zoom` değerini 600 gibi bir değere ayarlayabiliriz. Ancak bu durumda en boy oranı otomatik olarak ayarlanmaz ve modelimiz ekranı doldurmaz.

## Star Nest gölgelendiricisi

Artık her şey hazır olduğuna göre asıl gölgelendirici kodu üzerinde çalışmaya başlayalım. Önce özgün koda bakalım. Kod birkaç bölümden oluşuyor:

![Star Nest gölgelendiricisinin kodu](../images/shadertoy/starnest_code.png)

GLSL sürüm 140 ile modern bir işleme hattı kullanacağız. Bunun için dosyanın en başında `#version 140` ile sürümü bildireceğiz.

1. 5--18. satırlar bir dizi sabit tanımlar. Bunları olduğu gibi bırakabiliriz. Bunlar, özellikle Shadertoy veya Defold'a bağımlı olmayan sıradan GLSL sabitleridir.

2. 21. ve 63. satırlar, girdi parçasının ekran uzayındaki X ve Y doku koordinatlarını (`in vec2 fragCoord`) ve çıktı parçasının rengini (`out vec4 fragColor`) içerir.

    Defold, doku koordinatlarını köşe gölgelendiricisinden parça gölgelendiricisine ara değerleri hesaplanan bir değişken aracılığıyla UV koordinatları (0--1 aralığında) olarak aktarır. Köşe gölgelendiricimizde bu değişken `out` niteleyicisiyle bildirilir:

    ```glsl
    // in star-nest.vp
    out vec2 var_texcoord0;
    ```

     Parça gölgelendiricisinde aynı değer `in` niteleyicisiyle alınır:

    ```glsl
    // in star-nest.fp
    in vec2 var_texcoord0;
    ```

    Ardından GLSL 140'ta `out` niteleyicisiyle açık bir parça çıktısı bildiririz:

    ```glsl
    // in star-nest.fp
    out vec4 out_fragColor;
    ```

    Böylece, özgün Shadertoy kodunun `fragColor` değişkenine yazdığı yerde Defold gölgelendiricimiz `out_fragColor` değişkenine yazar.

3. 23--27. satırlar dokunun boyutlarını, hareket yönünü ve ölçeklenmiş zamanı ayarlar. Shadertoy'da gölgelendirici, piksel konumunu `fragCoord` aracılığıyla alır ve görüntü alanının/dokunun çözünürlüğü gölgelendiriciye `uniform vec3 iResolution` olarak aktarılır. Gölgelendirici, parça koordinatlarından ve çözünürlükten doğru en boy oranına sahip UV tarzı koordinatlar hesaplar. Daha güzel bir kadraj elde etmek için çözünürlüğe bağlı bazı kaydırmalar da yapılır.

    Defold'da piksel koordinatlarından başlamayız. Bunun yerine, köşe gölgelendiricisinden `var_texcoord0` aracılığıyla zaten normalleştirilmiş UV koordinatları alırız. Bu koordinatlar, işlenen dörtgen boyunca `0.0` ile `1.0` aralığındadır.

    Defold sürümünde, bu hesaplamaların `var_texcoord0` içindeki UV koordinatlarını kullanacak şekilde değiştirilmesi gerekir.
    Tipik bir dönüşüm şöyle görünür:

    ```glsl
    vec2 uv = var_texcoord0.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= aspect;
    ```
    `aspect` değerinin tam olarak ne olacağı, örneğin nasıl kurulduğuna bağlıdır. Efekt, ekran boyutu bilinen tam ekran bir dörtgen üzerinde işleniyorsa öğretici için en boy oranı kodda sabit bir değer olarak yazılabilir. Efektin herhangi bir pencere boyutunu desteklemesi gerekiyorsa çözünürlüğü bir parça sabiti olarak aktarın ve GLSL 140 uniform bloğunun içine yerleştirin.

    Zaman da burada ayarlanır. Gölgelendiriciye `uniform float iGlobalTime` olarak aktarılır. Defold (1.12.3 sürümünden itibaren), gölgelendiricilere zamanı kullanacağımız özel bir `Time` sabiti aracılığıyla sağlar.

    Modern Defold sürümlerinde, opak olmayan uniform değişkenleri uniform bloklarının içinde bildirilir.
    Parça gölgelendiricisinde bunu şöyle bildiririz:

    ```glsl
    uniform fragment_inputs
    {
        vec4 time;
    };
    ```

    Ardından `star-nest.material` dosyasında `time` adlı bir Fragment Constant ekleyip türünü `Time` olarak ayarlayacağız.

    Değer daha sonra şöyle kullanılabilir:

    ```glsl
    float iGlobalTime = time.x;
    float dt = time.y;
    ```
    Burada `time.x`, motor başlatıldığından beri geçen süredir; `time.y` ise önceki kareden bu yana geçen süredir.

4. 29--39. satırlar hacimsel işlemenin dönmesini ayarlar; fare konumu bu dönmeyi etkiler. Fare koordinatları gölgelendiriciye `uniform vec4 iMouse` olarak aktarılır.

    Bu öğreticide fare girdisini atlayacağız.

5. 41--62. satırlar gölgelendiricinin temel bölümüdür. Bu kodu olduğu gibi bırakabiliriz.

## Değiştirilmiş Star Nest gölgelendiricisi

Yukarıdaki bölümleri inceleyip gerekli değişiklikleri yaptığımızda aşağıdaki gölgelendirici kodunu elde ederiz. Daha kolay okunması için kod biraz düzenlenmiştir. Defold ve Shadertoy sürümleri arasındaki farklar işaretlenmiştir:

```glsl
#version 140 // <1>

// Star Nest by Pablo Román Andrioli
// This content is under the MIT License.

#define iterations 17
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.010

#define brightness 0.0015
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

in vec2 var_texcoord0; // <2>

out vec4 out_fragColor; // <3>

uniform fragment_inputs // <4>
{
	vec4 time;
};

void main() // <5>
{
	// get coords and direction
	vec2 res = vec2(1.0, 1.0); // <6>
	vec2 uv = var_texcoord0.xy * res.xy - 0.5;
	vec3 dir = vec3(uv * zoom, 1.0);

	float iGlobalTime = time.x; // <7>
	float shader_time = iGlobalTime * speed;

	float a1 = 0.5; // <8>
	float a2 = 0.8;
	mat2 rot1 = mat2(cos(a1), sin(a1), -sin(a1), cos(a1));
	mat2 rot2 = mat2(cos(a2), sin(a2), -sin(a2), cos(a2));

	dir.xz *= rot1;
	dir.xy *= rot2;

	vec3 from = vec3(1.0, 0.5, 0.5);
	from += vec3(shader_time * 2.0, shader_time, -2.0);
	from.xz *= rot1;
	from.xy *= rot2;

	// volumetric rendering
	float s = 0.1;
	float fade = 1.0;
	vec3 v = vec3(0.0);

	for (int r = 0; r < volsteps; r++) {
		vec3 p = from + s * dir * 0.5;

		// tiling fold
		p = abs(vec3(tile) - mod(p, vec3(tile * 2.0)));

		float pa = 0.0;
		float a = 0.0;

		for (int i = 0; i < iterations; i++) {
			// the magic formula
			p = abs(p) / dot(p, p) - formuparam;

			// absolute sum of average change
			a += abs(length(p) - pa);
			pa = length(p);
		}

		// dark matter
		float dm = max(0.0, darkmatter - a * a * 0.001);

		a *= a * a;

		// dark matter, don't render near
		if (r > 6) {
			fade *= 1.0 - dm;
		}

		v += fade;

		// coloring based on distance
		v += vec3(s, s * s, s * s * s * s) * a * brightness * fade;

		fade *= distfading;
		s += stepsize;
	}

	// color adjust
	v = mix(vec3(length(v)), v, saturation);

	out_fragColor = vec4(v * 0.01, 1.0); // <9>
}
```

1. Defold'un modern GLSL işleme hattını kullanmak için dosyanın en başında #version 140 bildiririz. Ardından define tanımlarını olduğu gibi bırakırız.
2. Köşe gölgelendiricisi, UV koordinatlarını var_texcoord0 aracılığıyla parça gölgelendiricisine aktarır. GLSL 140'ta parça gölgelendiricisi, ara değerleri hesaplanan bu değeri in niteleyicisiyle alır.
3. GLSL 140'ta parça gölgelendiricisinin, gl_FragColor değişkenine yazmak yerine açık bir çıktı değişkeni bildirmesi önerilir. Burada out vec4 out_fragColor kullanıyoruz.
4. Defold'un Time materyal sabiti, bir uniform bloğu aracılığıyla gölgelendiriciye sunulur. star-nest.material dosyasında time adlı bir Fragment Constant ekleyin ve türünü Time olarak ayarlayın.
5. Shadertoy, mainImage(out vec4 fragColor, in vec2 fragCoord) kullanır. Defold'da normal void main() giriş noktasını kullanır, ara değerleri hesaplanan UV koordinatlarını var_texcoord0 değişkeninden okur ve son rengi out_fragColor değişkenine yazarız.
6. Bu öğreticide işleme için sabit bir çözünürlük/en boy oranı değeri tanımlarız. Model şu anda kare olduğundan vec2 res = vec2(1.0, 1.0); kullanabiliriz. 1280×720 boyutunda dikdörtgen bir modelde ise vec2 res = vec2(1.78, 1.0); kullanabilir ve doğru en boy oranını korumak için UV koordinatlarını bununla çarpabiliriz.
7. Özgün Shadertoy gölgelendiricisi iGlobalTime kullanır. Bu Defold sürümünde time.x, motor başlatıldığından beri geçen süreyi içerir; dolayısıyla bu değeri yerel bir iGlobalTime değişkenine atar ve yıldız alanı boyunca kamera hareketini canlandırmak için kullanırız.
8. Bu öğreticiyi basit tutmak için iMouse değerlerini tamamen kaldırırız. Dönmenin kendisi ise korunur, çünkü hacimsel işlemedeki görsel simetriyi azaltır.
9. Son olarak gölgelendirici, ortaya çıkan parça rengini out_fragColor değişkenine yazar.

Parça gölgelendiricisi programını kaydedin. Model artık Scene düzenleyicisinde ve çalışma sırasında bir yıldız alanı dokusuyla güzel bir şekilde kaplanmış olmalıdır:

![Star Nest ile kaplanmış dörtgen](../images/shadertoy/quad_starnest.png)


## Animasyon {#animation}

Bulmacanın son parçası, yıldızları hareket ettirmek için zamanı devreye sokmaktır. Defold (1.12.3 sürümünden itibaren) bunu `Time` türündeki bir parça sabiti aracılığıyla otomatik olarak sağlar.

1. *star-nest.material* dosyasını açın.
2. Bir *Fragment Constant* ekleyin ve adını "time" olarak ayarlayın.
3. *Type* değerini `Time` olarak ayarlayın.

![zaman sabiti](../images/shadertoy/time_constant.png)

İşte bu kadar! Parça gölgelendiricisinde bu `time` değerini zaten kullanıyoruz. İşimiz tamam!

## Alıştırmalar

Eğlenceli bir devam alıştırması olarak gölgelendiriciye özgün fare hareketi girdisini ekleyebilirsiniz. Bu kez `User` türünde yeni bir Fragment Constant oluşturmanız gerekir. Fare hareketini algılayan bir betiğin `on_input` işlevinde, `go.set()` işlevini kullanarak girdi koordinatlarını bu yeni sabite atayın ve sabiti güncelleyin.

Defold ile keyifli çalışmalar!
