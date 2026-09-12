---
title: Bir Defold oyununda pil kullanımını optimize etme
brief: Bu kılavuz, bir Defold oyununda pil kullanımının nasıl optimize edileceğini açıklar.
---

# Pil kullanımını optimize etme
Pil kullanımı, özellikle mobil/elde taşınan cihazları hedefliyorsanız önem taşır. Yüksek CPU veya GPU kullanımı pili hızla tüketir ve cihazın aşırı ısınmasına neden olur.

CPU ve GPU kullanımını azaltmayı öğrenmek için bir oyunun [çalışma zamanı (runtime) performansını optimize etme](/manuals/optimization-speed) konulu kılavuzlara bakın.

## İvmeölçeri devre dışı bırakma
Cihazın ivmeölçerini (accelerometer) kullanmayan bir mobil oyun oluşturuyorsanız, üretilen girdi olaylarının (input events) sayısını azaltmak için [ivmeölçeri *game.project* dosyasında devre dışı bırakmanız](/manuals/project-settings/#use-accelerometer) önerilir.

# Platforma özgü optimizasyonlar

## Android Device Performance Framework

Android Dynamic Performance Framework, oyunların Android cihazların güç ve termal sistemleriyle daha doğrudan etkileşim kurmasını sağlayan bir API kümesidir. Android sistemlerindeki dinamik davranışı izlemek ve oyun performansını cihazları aşırı ısıtmayan, sürdürülebilir bir düzeyde optimize etmek mümkündür. Android cihazlar için geliştirdiğiniz Defold oyununda performansı izlemek ve optimize etmek için [Android Dynamic Performance Framework eklentisini](https://defold.com/extension-adpf/) kullanın.