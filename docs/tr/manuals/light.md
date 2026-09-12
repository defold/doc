---
title: Defold'da ışık bileşeni
brief: Bu kılavuz, ortam ışığının, yönlü, noktasal ve spot ışıklarının nasıl kullanılacağını ve gölgelendiricilerde ışık verilerine nasıl erişileceğini açıklar.
---

# Işık bileşeni

Işık bileşeni (Light component), bir koleksiyondaki (collection) ışık kaynağını temsil eder. Defold şu anda dört ışık kaynağı türünü destekler:

- Ortam ışığı (ambient light) (`.ambient_light`)
- Yönlü ışık (directional light) (`.directional_light`)
- Noktasal ışık (point light) (`.point_light`)
- Spot ışığı (spot light) (`.spot_light`)

Işık kaynakları, diğer bileşen kaynakları gibi oyun nesnelerine (game object) eklenir. Işık bileşenlerini doğrudan bir oyun nesnesinin altında oluşturabilir veya *Assets* tarayıcısında bir ışık kaynağı oluşturup ardından bunu *Outline* görünümünde bir oyun nesnesine bileşen olarak ekleyebilirsiniz.

Defold, her materyale (material) otomatik olarak aydınlatma uygulamaz. Işıklar motor tarafından toplanır ve yerleşik ışık arabelleği (light buffer) aracılığıyla gölgelendiricilerin (shader) kullanımına sunulur. Işık verilerinin nasıl kullanılacağına materyalin gölgelendiricisi karar verir.

Aşağıdaki örneklerde, farklı ışık türlerinin nihai sonucu nasıl etkilediğini göstermek için aynı sahne kullanılır:

![Işıksız sahne](images/light/no_light.png)

## Işık özellikleri

Tüm ışık renkleri RGB değerleridir. Işık kaynaklarında alfa kanalı kullanılmaz.

### Ortam ışığı

Ortam ışıkları sahneye sabit ışık ekler. Oyun nesnesinin konumundan, dönmesinden veya ölçeğinden etkilenmezler. Örneğin genel bir arka plan aydınlatması için veya nesnelerin aydınlatma uygulanmamış gibi görünmesini sağlamak için kullanılabilirler.

Ortam ışığı bileşeni, düzenleyicide okları merkeze doğru dönük bir simgeyle gösterilir. Simgenin rengi, bileşenin `color` özelliğiyle aynıdır. 

![Daha düşük şiddetli ortam ışığı](images/light/ambient_light_less_intensity.png)

Özellikler:

`color`
: Ortam ışığının RGB rengi.

`intensity`
: Ortam ışığının rengini çarpar.

![Daha yüksek şiddetli ortam ışığı](images/light/ambient_light_full_intensity.png)

Ortam ışıkları, gölgelendiricinin ışık arabelleğinde tek bir ortam rengi olan `light_info.xyz` değerinde biriktirilir. `lights[]` dizisinde yer kaplamazlar. Sahnedeki birden fazla ortam ışığı bileşeni, hepsinin harmanından oluşan yalnızca tek bir çıktı rengi üretir.

### Yönlü ışık

Yönlü ışıklar, güneş ışığı gibi tek bir yönden gelen ışığı temsil eder. Oyun nesnesinin konumunu veya ölçeğini kullanmazlar; ışığın yönü, oyun nesnesinin dünya uzayındaki dönmesinin yerel ileri yön olan `(0, 0, -1)` yönüne uygulanmasıyla elde edilir.

Yönlü ışık bileşeni, düzenleyicide yönünü belirten bir 3B ok içeren renkli bir güneş simgesiyle gösterilir.

![Yönlü ışık](images/light/directional_light.png)

Özellikler:

`color`
: Yönlü ışığın RGB rengi.

`intensity`
: Yönlü ışığın rengini çarpar.


Yönlü ışığın tersine bakan yüzeylerin tamamen kararmasını önlemek için yönlü ışıklar genellikle ortam ışığıyla birlikte kullanılır.

![Yönlü ışık ve ortam ışığı](images/light/directional_and_ambient_light.png)

### Noktasal ışık

Noktasal ışıklar, oyun nesnesinin dünya uzayındaki konumundan dışarıya doğru ışık yayar. Noktasal ışığın konumu, oyun nesnesinin dünya uzayındaki konumundan alınır.

Noktasal ışık bileşeni, düzenleyicide etrafına ışınlar yayılan bir noktayla gösterilir. Noktanın rengi `color` özelliğini, çember ise `range` değerini temsil eder.

![Noktasal ışık](images/light/point_light.png)

Özellikler:

`color`
: Noktasal ışığın RGB rengi.

`intensity`
: Noktasal ışığın rengini çarpar.

`range`
: Dünya birimleri cinsinden ışığın yarıçapı.

Etkin menzil, oyun nesnesinin dünya uzayındaki ölçeğinin eksen bileşenleri arasındaki en küçük mutlak değerle çarpılır.

![Noktasal ışığın menzili](images/light/point_light_range.png)

Işığın rengini değiştirmek, noktasal ışığın aydınlatmaya katkısını renklendirir; menzil ise ışığın kaynaktan ne kadar uzağa ulaşacağını belirler.

![Yeşil renkli noktasal ışığın menzili](images/light/point_ight_range_green_color.png)

### Spot ışığı

Spot ışıkları, oyun nesnesinin dünya uzayındaki konumundan koni biçiminde ışık yayar. Yön, oyun nesnesinin dünya uzayındaki dönmesinin `(0, 0, -1)` yönüne uygulanmasıyla elde edilir.

Spot ışığı bileşeni, düzenleyicide renkli bir lamba simgesi ve dış ve iç konileri gösteren kılavuz çizgileriyle gösterilir.

![Spot ışığı](images/light/spot_light.png)

Özellikler:

`color`
: Spot ışığının RGB rengi.

`intensity`
: Spot ışığının rengini çarpar.

`range`
: Dünya birimleri cinsinden ışığın yarıçapı.

`inner_cone_angle`
: Düzenleyicide derece cinsinden iç koni açısı. Bu koninin içindeki pikseller, spot ışığının katkısını tam olarak alır.

`outer_cone_angle`
: Düzenleyicide derece cinsinden dış koni açısı. Işık, iç koni ile dış koni arasında giderek azalır.

Etkin menzil, oyun nesnesinin dünya uzayındaki ölçeğinin eksen bileşenleri arasındaki en küçük mutlak değerle çarpılır. Koni açıları derece cinsinden düzenlenir ve derlenmiş ışık kaynağında radyana dönüştürülür.

![Spot ışığının düzenleme araçları](images/light/spot_light_gizmos.png)

## Doğrulama

Proje derleme hattı, ışık kaynağı verilerini doğrular ve normalleştirir:

- `color` tam olarak üç sayı içermelidir.
- `intensity`, en az `0` olacak şekilde sınırlandırılır.
- Noktasal ve spot ışıklarında `range`, en az `0` olacak şekilde sınırlandırılır.
- Spot koni açıları `0..180` derece aralığıyla sınırlandırılır.
- `inner_cone_angle`, hiçbir zaman `outer_cone_angle` değerini aşmayacak şekilde sınırlandırılır.

## Proje sınırı

En fazla kaç ışık bileşeni olabileceği, `light.max_count` proje ayarıyla belirlenir. Varsayılan değer `64` olur.

Ortam ışıkları, gölgelendiricinin `lights[]` dizisinde yer kaplamaz; ancak yine de ışık bileşeni oldukları için `light.max_count` sınırına dahil edilirler. Yönlü, noktasal ve spot ışıkları, etkin oldukları sürece `lights[]` dizisinde yer kaplar.

Işık bileşenlerinin sayısı `light.max_count` değerini aşarsa motor, bileşen arabelleğinin dolu olduğunu bildiren bir hata verir.

## Gölgelendiricilerde ışık arabelleği

Bir gölgelendirici, yerleşik düzene sahip ve `LightBuffer` adını taşıyan bir uniform bloğu bildirerek etkin ışıklara erişebilir. Motor bu bloğu algılar ve onu kullanan materyaller ile hesaplama programları için ışık verilerini otomatik olarak bağlar.

![Işık arabelleğini kullanan gölgelendirici](images/light/light-buffer-shader.png)

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

struct Light
{
    vec4 position;        // xyz: world position, w: unused
    vec4 color;           // rgb: color, a: unused
    vec4 direction_range; // xyz: normalized world direction, w: range
    vec4 params;          // x: type, y: intensity, z: inner cone, w: outer cone
};

uniform LightBuffer
{
    // xyz: accumulated ambient color, w: active non-ambient light count
    vec4 light_info;
    Light lights[MAX_LIGHT_COUNT];
};
```

Işık türü, `lights[i].params.x` alanında saklanır:

| Tür | Değer |
|------|-------|
| Yönlü | `0` |
| Noktasal | `1` |
| Spot | `2` |

Gölgelendirici, `lights[]` dizisini `light.max_count` değerinden daha küçük bir boyutla bildirebilir, ancak daha büyük bir boyutla bildiremez. Işık döngülerini her zaman bildirilen dizi boyutuyla sınırlandırın:

```glsl
vec3 apply_lights(vec3 normal)
{
    vec3 result = light_info.xyz;
    int active_light_count = int(light_info.w);

    for (int i = 0; i < MAX_LIGHT_COUNT; ++i)
    {
        if (i >= active_light_count)
        {
            break;
        }

        int type = int(lights[i].params.x);
        vec3 light_color = lights[i].color.rgb * lights[i].params.y;

        if (type == 0) // Directional
        {
            vec3 light_dir = normalize(-lights[i].direction_range.xyz);
            result += light_color * max(dot(normal, light_dir), 0.0);
        }
        else if (type == 1) // Point
        {
            result += light_color;
        }
        else if (type == 2) // Spot
        {
            result += light_color;
        }
    }

    return result;
}
```

Yukarıdaki örnek, arabelleğe erişim biçimini gösterir. Gerçek bir noktasal veya spot ışığı gölgelendiricisinin, gölgelendirilen noktadan `lights[i].position.xyz` konumuna uzanan vektörü de hesaplaması, `lights[i].direction_range.w` değerini kullanarak uzaklığa bağlı zayıflamayı uygulaması ve spot ışıklarında `lights[i].params.z` ile `lights[i].params.w` değerlerini radyan cinsinden koni açıları olarak kullanması önerilir.

## Yerleşik aydınlatma yardımcısı

Defold, `/builtins/materials/lighting.glsl` yolunda bir gölgelendirici yardımcısı içerir. `MAX_LIGHT_COUNT` değerini tanımlayın, yardımcının beklediği değişkenleri (varyings) sağlayın ve ardından yardımcıyı parça gölgelendiricinizden dahil edin:

```glsl
#version 140

#define MAX_LIGHT_COUNT 32

in vec3 var_normal;
in vec4 var_position;
in mat4 var_view;

out vec4 color_out;

#include "/builtins/materials/lighting.glsl"

void main()
{
    vec3 normal = normalize(var_normal);
    vec3 ambient = ambient_light();
    vec3 diffuse = diffuse_lambert(normal, var_position.xyz);
    color_out = vec4(ambient + diffuse, 1.0);
}
```

Yardımcı, `LIGHT_DIRECTIONAL`, `LIGHT_POINT` ve `LIGHT_SPOT` sabitlerini tanımlar, `ambient_light()` işlevini kullanıma sunar ve arabellekteki ışıklar için Lambert dağınık yansıma işlevleri sağlar.

## Ayrıca bakınız

- [Gölgelendirici kılavuzu](/manuals/shader)
- [Materyal kılavuzu](/manuals/material)
- [İşleme kılavuzu](/manuals/render)
