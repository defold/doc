---
title: Doku filtreleme
brief: Bu kılavuz, grafiklerin işlenmesi (rendering) sırasında doku filtreleme için kullanılabilen seçenekleri açıklar.
---

# Doku filtreleme ve örnekleme

Doku filtreleme (texture filtering), bir _teksel_ (texel; dokudaki bir piksel) ekran pikseliyle tam olarak hizalanmadığında ortaya çıkan görsel sonucu belirler. Bu durum, dokuyu içeren bir grafik öğesini bir pikselden daha az hareket ettirdiğinizde ortaya çıkar. Aşağıdaki filtreleme yöntemleri kullanılabilir:

En yakın komşu (Nearest)
: Ekran pikselini renklendirmek için en yakın teksel seçilir. Dokularınızdaki piksellerle ekranda gördüğünüz pikseller arasında tam olarak bire bir eşleme istiyorsanız bu örnekleme (sampling) yöntemini seçin. En yakın komşu filtrelemede her şey hareket ederken pikselden piksele atlar. Sprite bileşeni yavaş hareket ediyorsa bu, titrek görünebilir.

Doğrusal (Linear)
: Ekran pikseli renklendirilmeden önce teksel ile komşularının renklerinin ortalaması alınır. Bu, yavaş ve sürekli hareketlerde akıcı bir görünüm sağlar; çünkü sprite bileşeninin rengi, pikselleri tamamen renklendirmeden önce onlara yayılmaya başlar. Böylece sprite bileşenini bir tam pikselden daha az hareket ettirmek mümkün olur.

Hangi filtrelemenin kullanılacağını belirleyen ayar, [Proje ayarları](/manuals/project-settings/#graphics) dosyasında saklanır. İki ayar vardır:

default_texture_min_filter
: Küçültme filtrelemesi, teksel ekran pikselinden daha küçük olduğunda uygulanır.

default_texture_mag_filter
: Büyütme filtrelemesi, teksel ekran pikselinden daha büyük olduğunda uygulanır.

Her iki ayar da `linear`, `nearest`, `nearest_mipmap_nearest`, `nearest_mipmap_linear`, `linear_mipmap_nearest` veya `linear_mipmap_linear` değerlerini kabul eder. Örneğin:

```ini
[graphics]
default_texture_min_filter = nearest
default_texture_mag_filter = nearest
```

Hiçbir değer belirtmezseniz her ikisi de varsayılan olarak `linear` değerine ayarlanır.

*game.project* dosyasındaki ayarın varsayılan örnekleyicilerde (sampler) kullanıldığını unutmayın. Özel bir materyalde (material) örnekleyiciler tanımlarsanız her örnekleyici için filtreleme yöntemini ayrı ayrı ayarlayabilirsiniz. Ayrıntılar için [Materyaller kılavuzuna](/manuals/material/) bakın.
