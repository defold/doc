---
title: Defold'da fizik
brief: Defold, 2B ve 3B fizik motorları içerir. Bu motorlar, farklı türdeki çarpışma nesneleri arasındaki Newton fiziği etkileşimlerini simüle etmenizi sağlar.
---

# Fizik

Defold, iki boyutlu (2B) fizik simülasyonları için [Box2D](https://box2d.org/), üç boyutlu (3B) fizik için ise Bullet içerir. [App Manifest içindeki Physics 2D ayarı](/manuals/app-manifest/#physics-2d), **Box2D Version 3**, **Box2D (Legacy Defold version)** veya **None** seçeneğini belirler. Eski uygulama varsayılandır; Box2D 3'ü kullanmak için ayrıca seçmeniz gerekir. Uygulamayı değiştirmek simülasyon sonuçlarını değiştirebilir ve sürüme özgü [Box2D proje ayarlarını](/manuals/project-settings/#box2d) yeniden düzenlemenizi gerektirebilir.

Bu kılavuzlarda açıklanan bileşen (component) odaklı çarpışma nesnesi (collision object) iş akışı ve `physics` modülü, her iki Box2D uygulamasıyla da çalışır; **None** seçeneğini seçmek 2B fiziği kaldırır. Defold ayrıca 2B cisimlere, şekillere, eklemlere, zincirlere ve dünyalara doğrudan erişim için daha düşük düzeyli [`b2d`](/ref/stable/b2d/), `b2d.body`, `b2d.fixture`, `b2d.shape`, `b2d.joint`, `b2d.chain` ve `b2d.world` API'lerini sunar. Her düşük düzeyli işlev, her iki Box2D uygulamasında da mevcut değildir; her işlevin oluşturulan API belgelerini App Manifest içinde seçilen uygulamaya göre kontrol edin.

Defold'da kullanılan fizik motorlarının temel kavramları şunlardır:

* **Çarpışma nesneleri** - Çarpışma nesnesi, bir oyun nesnesine (game object) fiziksel davranış kazandırmak için kullandığınız bir bileşendir. Çarpışma nesnesinin ağırlık, sürtünme ve şekil gibi fiziksel özellikleri vardır. [Çarpışma nesnesi oluşturmayı öğrenin](/manuals/physics-objects).
* **Çarpışma şekilleri (collision shapes)** - Bir çarpışma nesnesi, uzayda kapladığı alanı tanımlamak için birkaç temel şekil veya tek bir karmaşık şekil kullanabilir. [Çarpışma nesnesine şekil eklemeyi öğrenin](/manuals/physics-shapes).
* **Çarpışma grupları (collision groups)** - Tüm çarpışma nesneleri önceden tanımlanmış bir gruba ait olmalıdır ve her çarpışma nesnesi, çarpışabileceği diğer grupların listesini belirtebilir. [Çarpışma gruplarını kullanmayı öğrenin](/manuals/physics-groups).
* **Çarpışma iletileri (collision messages)** - İki çarpışma nesnesi çarpıştığında fizik motoru, bileşenlerin ait olduğu oyun nesnelerine iletiler gönderir. [Çarpışma iletileri hakkında daha fazla bilgi edinin](/manuals/physics-messages)

Çarpışma nesnelerinin yanı sıra, daha yaygın olarak **eklem (joint)** adıyla bilinen çarpışma nesnesi **kısıtları (constraints)** da tanımlayabilirsiniz. Bunlar iki çarpışma nesnesini birbirine bağlamanızı ve nesneleri sınırlayarak veya başka şekillerde kuvvet uygulayarak fizik simülasyonundaki davranışlarını etkilemenizi sağlar. [Eklemler hakkında daha fazla bilgi edinin](/manuals/physics-joints).

Ayrıca **ışın sorgusu (ray cast)** olarak bilinen işlemle fizik dünyasını doğrusal bir ışın boyunca sorgulayabilir ve okuyabilirsiniz. [Işın sorguları hakkında daha fazla bilgi edinin](/manuals/physics-ray-casts).


## Fizik motoru simülasyonunda kullanılan birimler

Fizik motoru Newton fiziğini simüle eder ve metre, kilogram ve saniye (MKS) birimleriyle iyi çalışacak şekilde tasarlanmıştır. Ayrıca fizik motoru, boyutu 0,1 ile 10 metre arasında olan hareketli nesnelerle iyi çalışacak şekilde ayarlanmıştır (statik nesneler daha büyük olabilir) ve varsayılan olarak 1 birimi (pikseli) 1 metre olarak kabul eder. Piksel ile metre arasındaki bu dönüşüm, simülasyon düzeyinde kullanışlıdır, ancak oyun oluşturma açısından pek yararlı değildir. Varsayılan ayarlarla, 200 piksel boyutundaki bir çarpışma şekli 200 metre boyutunda kabul edilir. Bu değer, en azından hareketli bir nesne için, önerilen aralığın oldukça dışındadır.

Genel olarak fizik simülasyonunun, bir oyundaki nesnelerin tipik boyutlarıyla iyi çalışabilmesi için ölçeklendirilmesi gerekir. Fizik simülasyonunun ölçeği, *game.project* dosyasındaki [fizik ölçeği ayarı](/manuals/project-settings/#physics) aracılığıyla değiştirilebilir. Örneğin bu değeri 0.02 olarak ayarlamak, 200 pikselin 4 metre olarak kabul edilmesi anlamına gelir. Ölçekteki değişikliğe uyum sağlamak için yerçekiminin de (yine *game.project* dosyasında değiştirilir) artırılması gerektiğini unutmayın.


## Fizik güncellemeleri {#physics-updates}

Kararlı bir simülasyon sağlamak için fizik motorunu, kare hızına bağlı ve düzensiz olabilecek aralıklarla güncellemek yerine düzenli aralıklarla güncellemeniz önerilir. *game.project* dosyasının Physics bölümündeki [Use Fixed Timestep ayarını](/manuals/project-settings/#physics) işaretleyerek fizik için sabit aralıklı güncelleme kullanabilirsiniz. Güncelleme sıklığı, *game.project* dosyasının Engine bölümündeki [Fixed Update Frequency ayarı](/manuals/project-settings/#engine) ile denetlenir. Fizik için sabit zaman adımı kullanırken, oyununuzdaki çarpışma nesneleriyle etkileşim kurmak, örneğin onlara kuvvet uygulamak için `fixed_update(self, dt)` yaşam döngüsü işlevini kullanmanız da önerilir.


## Dikkat edilmesi gerekenler ve yaygın sorunlar

Koleksiyon vekilleri
: Koleksiyon vekilleri (collection proxies) aracılığıyla motora birden fazla en üst düzey koleksiyon (collection) veya *oyun dünyası (game world)* yüklemek mümkündür. Bunu yaparken her en üst düzey koleksiyonun ayrı bir fizik dünyası olduğunu bilmek önemlidir. Fizik etkileşimleri ([çarpışmalar, tetikleyiciler](/manuals/physics-messages) ve [ışın sorguları](/manuals/physics-ray-casts)) yalnızca aynı dünyaya ait nesneler arasında gerçekleşir. Dolayısıyla, iki dünyadaki çarpışma nesneleri görsel olarak tam üst üste dursa bile aralarında herhangi bir fizik etkileşimi gerçekleşemez.

Çarpışmaların algılanmaması
: Çarpışmaların düzgün işlenmemesi veya algılanmamasıyla ilgili sorun yaşıyorsanız [Hata ayıklama kılavuzundaki fizik hatalarını ayıklama bölümünü](/manuals/debugging-game-logic/#debugging-problems-with-physics) mutlaka okuyun.
