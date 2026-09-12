---
title: Defold özellik animasyonları kılavuzu
brief: Bu kılavuz, Defold'da özellik animasyonlarının nasıl kullanılacağını açıklar.
---

# Özellik animasyonu

Tüm sayısal özelliklere (`numbers`, `vector3`, `vector4` ve kuaterniyonlar (quaternion)) ve gölgelendirici (shader) sabitlerine, `go.animate()` işlevini kullanarak yerleşik animasyon sistemiyle animasyon uygulanabilir. Motor, verilen oynatma modlarına ve geçiş eğrisi (easing) işlevlerine göre özelliklere otomatik olarak "ara geçiş animasyonu" (tween) uygular. Özel geçiş eğrisi işlevleri de belirtebilirsiniz.

  ![Özellik animasyonu](images/animation/property_animation.png)
  ![Sıçrama döngüsü](images/animation/bounce.gif)

## Özellik animasyonu

Bir oyun nesnesinin (game object) veya bileşenin (component) özelliğine özellik animasyonu (property animation) uygulamak için `go.animate()` işlevini kullanın. GUI düğümü (GUI node) özellikleri için karşılık gelen işlev `gui.animate()` işlevidir.

```lua
-- Set the position property y component to 200
go.set(".", "position.y", 200)
-- Then animate it
go.animate(".", "position.y", go.PLAYBACK_LOOP_PINGPONG, 100, go.EASING_OUTBOUNCE, 2)
```

Belirli bir özelliğin tüm animasyonlarını durdurmak için `go.cancel_animations()` işlevini, GUI düğümleri için ise `gui.cancel_animations()` işlevini çağırın:

```lua
-- Stop euler z rotation animation on the current game object
go.cancel_animations(".", "euler.z")
```

`position` gibi bileşik bir özelliğin animasyonunu iptal ederseniz alt bileşenlerin (`position.x`, `position.y` ve `position.z`) tüm animasyonları da iptal edilir.

[Özellikler kılavuzu](/manuals/properties), oyun nesnelerinde, bileşenlerde ve GUI düğümlerinde kullanılabilen tüm özellikleri içerir.

## GUI düğümü özellik animasyonu

GUI düğümü özelliklerinin neredeyse tamamına animasyon uygulanabilir. Örneğin, bir düğümün `color` özelliğini tam saydamlığa ayarlayarak onu görünmez yapabilir, ardından rengi animasyonla beyaza (yani renklendirme uygulanmayan duruma) dönüştürerek düğümü yavaşça görünür hâle getirebilirsiniz.

```lua
local node = gui.get_node("button")
local color = gui.get_color(node)
-- Animate the color to white
gui.animate(node, gui.PROP_COLOR, vmath.vector4(1, 1, 1, 1), gui.EASING_INOUTQUAD, 0.5)
-- Animate the outline red color component
gui.animate(node, "outline.x", 1, gui.EASING_INOUTQUAD, 0.5)
-- And move to x position 100
gui.animate(node, hash("position.x"), 100, gui.EASING_INOUTQUAD, 0.5)
```

## Tamamlanma geri çağırımları

Özellik animasyonu işlevleri `go.animate()` ve `gui.animate()`, son bağımsız değişken olarak isteğe bağlı bir Lua geri çağırım (callback) işlevini destekler. Bu işlev, animasyon sonuna kadar oynatıldığında çağrılır. Döngüde oynatılan animasyonlarda veya bir animasyon `go.cancel_animations()` ya da `gui.cancel_animations()` aracılığıyla elle iptal edildiğinde bu işlev hiçbir zaman çağrılmaz. Geri çağırım, animasyon tamamlandığında olayları tetiklemek veya birden çok animasyonu birbirine zincirlemek için kullanılabilir.

## Geçiş eğrileri {#easing}

Geçiş eğrisi, animasyon uygulanan değerin zaman içinde nasıl değiştiğini tanımlar. Aşağıdaki görüntüler, geçiş eğrisini oluşturmak için zaman içinde uygulanan işlevleri gösterir.

`go.animate()` için geçerli geçiş eğrisi değerleri şunlardır:

|---|---|
| `go.EASING_LINEAR` | |
| `go.EASING_INBACK` | `go.EASING_OUTBACK` |
| `go.EASING_INOUTBACK` | `go.EASING_OUTINBACK` |
| `go.EASING_INBOUNCE` | `go.EASING_OUTBOUNCE` |
| `go.EASING_INOUTBOUNCE` | `go.EASING_OUTINBOUNCE` |
| `go.EASING_INELASTIC` | `go.EASING_OUTELASTIC` |
| `go.EASING_INOUTELASTIC` | `go.EASING_OUTINELASTIC` |
| `go.EASING_INSINE` | `go.EASING_OUTSINE` |
| `go.EASING_INOUTSINE` | `go.EASING_OUTINSINE` |
| `go.EASING_INEXPO` | `go.EASING_OUTEXPO` |
| `go.EASING_INOUTEXPO` | `go.EASING_OUTINEXPO` |
| `go.EASING_INCIRC` | `go.EASING_OUTCIRC` |
| `go.EASING_INOUTCIRC` | `go.EASING_OUTINCIRC` |
| `go.EASING_INQUAD` | `go.EASING_OUTQUAD` |
| `go.EASING_INOUTQUAD` | `go.EASING_OUTINQUAD` |
| `go.EASING_INCUBIC` | `go.EASING_OUTCUBIC` |
| `go.EASING_INOUTCUBIC` | `go.EASING_OUTINCUBIC` |
| `go.EASING_INQUART` | `go.EASING_OUTQUART` |
| `go.EASING_INOUTQUART` | `go.EASING_OUTINQUART` |
| `go.EASING_INQUINT` | `go.EASING_OUTQUINT` |
| `go.EASING_INOUTQUINT` | `go.EASING_OUTINQUINT` |

`gui.animate()` için geçerli geçiş eğrisi değerleri şunlardır:

|---|---|
| `gui.EASING_LINEAR` | |
| `gui.EASING_INBACK` | `gui.EASING_OUTBACK` |
| `gui.EASING_INOUTBACK` | `gui.EASING_OUTINBACK` |
| `gui.EASING_INBOUNCE` | `gui.EASING_OUTBOUNCE` |
| `gui.EASING_INOUTBOUNCE` | `gui.EASING_OUTINBOUNCE` |
| `gui.EASING_INELASTIC` | `gui.EASING_OUTELASTIC` |
| `gui.EASING_INOUTELASTIC` | `gui.EASING_OUTINELASTIC` |
| `gui.EASING_INSINE` | `gui.EASING_OUTSINE` |
| `gui.EASING_INOUTSINE` | `gui.EASING_OUTINSINE` |
| `gui.EASING_INEXPO` | `gui.EASING_OUTEXPO` |
| `gui.EASING_INOUTEXPO` | `gui.EASING_OUTINEXPO` |
| `gui.EASING_INCIRC` | `gui.EASING_OUTCIRC` |
| `gui.EASING_INOUTCIRC` | `gui.EASING_OUTINCIRC` |
| `gui.EASING_INQUAD` | `gui.EASING_OUTQUAD` |
| `gui.EASING_INOUTQUAD` | `gui.EASING_OUTINQUAD` |
| `gui.EASING_INCUBIC` | `gui.EASING_OUTCUBIC` |
| `gui.EASING_INOUTCUBIC` | `gui.EASING_OUTINCUBIC` |
| `gui.EASING_INQUART` | `gui.EASING_OUTQUART` |
| `gui.EASING_INOUTQUART` | `gui.EASING_OUTINQUART` |
| `gui.EASING_INQUINT` | `gui.EASING_OUTQUINT` |
| `gui.EASING_INOUTQUINT` | `gui.EASING_OUTINQUINT` |

![Doğrusal ara değerleme](images/properties/easing_linear.png)
![Başlangıçta geri taşma](images/properties/easing_inback.png)
![Bitişte geri taşma](images/properties/easing_outback.png)
![Başlangıçta ve bitişte geri taşma](images/properties/easing_inoutback.png)
![Bitişte ve başlangıçta geri taşma](images/properties/easing_outinback.png)
![Başlangıçta sıçrama](images/properties/easing_inbounce.png)
![Bitişte sıçrama](images/properties/easing_outbounce.png)
![Başlangıçta ve bitişte sıçrama](images/properties/easing_inoutbounce.png)
![Bitişte ve başlangıçta sıçrama](images/properties/easing_outinbounce.png)
![Başlangıçta esnek geçiş](images/properties/easing_inelastic.png)
![Bitişte esnek geçiş](images/properties/easing_outelastic.png)
![Başlangıçta ve bitişte esnek geçiş](images/properties/easing_inoutelastic.png)
![Bitişte ve başlangıçta esnek geçiş](images/properties/easing_outinelastic.png)
![Başlangıçta sinüs geçişi](images/properties/easing_insine.png)
![Bitişte sinüs geçişi](images/properties/easing_outsine.png)
![Başlangıçta ve bitişte sinüs geçişi](images/properties/easing_inoutsine.png)
![Bitişte ve başlangıçta sinüs geçişi](images/properties/easing_outinsine.png)
![Başlangıçta üstel geçiş](images/properties/easing_inexpo.png)
![Bitişte üstel geçiş](images/properties/easing_outexpo.png)
![Başlangıçta ve bitişte üstel geçiş](images/properties/easing_inoutexpo.png)
![Bitişte ve başlangıçta üstel geçiş](images/properties/easing_outinexpo.png)
![Başlangıçta dairesel geçiş](images/properties/easing_incirc.png)
![Bitişte dairesel geçiş](images/properties/easing_outcirc.png)
![Başlangıçta ve bitişte dairesel geçiş](images/properties/easing_inoutcirc.png)
![Bitişte ve başlangıçta dairesel geçiş](images/properties/easing_outincirc.png)
![Başlangıçta ikinci dereceden geçiş](images/properties/easing_inquad.png)
![Bitişte ikinci dereceden geçiş](images/properties/easing_outquad.png)
![Başlangıçta ve bitişte ikinci dereceden geçiş](images/properties/easing_inoutquad.png)
![Bitişte ve başlangıçta ikinci dereceden geçiş](images/properties/easing_outinquad.png)
![Başlangıçta üçüncü dereceden geçiş](images/properties/easing_incubic.png)
![Bitişte üçüncü dereceden geçiş](images/properties/easing_outcubic.png)
![Başlangıçta ve bitişte üçüncü dereceden geçiş](images/properties/easing_inoutcubic.png)
![Bitişte ve başlangıçta üçüncü dereceden geçiş](images/properties/easing_outincubic.png)
![Başlangıçta dördüncü dereceden geçiş](images/properties/easing_inquart.png)
![Bitişte dördüncü dereceden geçiş](images/properties/easing_outquart.png)
![Başlangıçta ve bitişte dördüncü dereceden geçiş](images/properties/easing_inoutquart.png)
![Bitişte ve başlangıçta dördüncü dereceden geçiş](images/properties/easing_outinquart.png)
![Başlangıçta beşinci dereceden geçiş](images/properties/easing_inquint.png)
![Bitişte beşinci dereceden geçiş](images/properties/easing_outquint.png)
![Başlangıçta ve bitişte beşinci dereceden geçiş](images/properties/easing_inoutquint.png)
![Bitişte ve başlangıçta beşinci dereceden geçiş](images/properties/easing_outinquint.png)

## Özel geçiş eğrileri

Bir değer kümesi içeren bir `vector` tanımlayarak özel geçiş eğrileri oluşturabilir, ardından yukarıdaki önceden tanımlanmış geçiş eğrisi sabitlerinden biri yerine bu vektörü verebilirsiniz. Vektör değerleri, başlangıç değerinden (`0`) hedef değere (`1`) uzanan bir eğriyi ifade eder. Çalışma zamanı ortamı, vektörden değerleri örnekler ve vektörde belirtilen noktalar arasındaki değerleri hesaplarken doğrusal ara değerleme (interpolation) uygular.

Örneğin şu vektör:

```lua
local values = { 0, 0.4, 0.2, 0.2, 0.5, 1 }
local my_easing = vmath.vector(values)
```

aşağıdaki eğriyi oluşturur:

![Özel eğri](images/animation/custom_curve.png)

Aşağıdaki örnek, bir oyun nesnesinin y konumunun kare dalga biçimindeki bir eğriye göre geçerli konum ile 200 arasında sıçramasını sağlar:

```lua
local values = { 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 1, 1, 1, 1, 1, 1 }
local square_easing = vmath.vector(values)
go.animate("go", "position.y", go.PLAYBACK_LOOP_PINGPONG, 200, square_easing, 2.0)
```

![Kare dalga eğrisi](images/animation/square_curve.png)
