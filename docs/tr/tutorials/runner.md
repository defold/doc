---
title: Sonsuz koşu oyunu öğreticisi
brief: Bu öğreticide boş bir projeyle başlayıp animasyonlu bir karakter, fiziksel çarpışmalar, toplanabilir nesneler ve puanlama içeren eksiksiz bir koşu oyunu oluşturacaksınız.
---

# Koşu oyunu öğreticisi

Bu öğreticide boş bir projeyle başlayıp animasyonlu bir karakter, fiziksel çarpışmalar, toplanabilir nesneler ve puanlama içeren eksiksiz bir koşu oyunu oluşturacağız.

Yeni bir oyun motorunu öğrenirken kavranması gereken çok şey vardır; bu öğreticiyi başlamanıza yardımcı olmak için hazırladık. Motorun ve düzenleyicinin nasıl çalıştığını adım adım anlatan, oldukça kapsamlı bir öğreticidir. Programlamaya biraz aşina olduğunuzu varsayıyoruz.

Lua programlamaya giriş yapmak istiyorsanız [Defold'da Lua kılavuzumuza](/manuals/lua) göz atın.

Bu öğreticinin başlangıç için biraz fazla kapsamlı olduğunu düşünüyorsanız farklı zorluk düzeylerinde öğreticiler sunduğumuz [öğreticiler sayfamıza](//www.defold.com/tutorials) göz atın.

Video öğreticileri izlemeyi tercih ediyorsanız [YouTube'daki video sürümüne](https://www.youtube.com/playlist?list=PLXsXu5srjNlxtYPQ_YJQSxJG2AN9OVS5b) göz atın.

Diğer iki öğreticideki oyun varlıklarını (asset) küçük değişikliklerle kullanıyoruz. Öğretici, her biri bizi tamamlanmış oyuna önemli ölçüde yaklaştıran birkaç adıma ayrılmıştır.

Sonuçta, bir ortamda koşarak paraları toplayan ve engellerden kaçınan bir kahraman karakteri kontrol ettiğiniz bir oyun elde edeceksiniz. Kahraman sabit süratle koşar; oyuncu tek bir düğmeye basarak (veya mobil cihazda ekrana dokunarak) yalnızca kahramanın zıplamasını kontrol eder. Bölüm, üzerine zıplanacak platformların ve toplanacak paraların sonsuz akışından oluşur.

Bu öğreticinin herhangi bir yerinde veya oyununuzu oluştururken takılırsanız [Defold Forum](//forum.defold.com) üzerinden bizden yardım istemekten çekinmeyin. Forumda Defold hakkında konuşabilir, Defold ekibinden yardım isteyebilir, diğer oyun geliştiricilerinin sorunlarını nasıl çözdüğünü görebilir ve yeni fikirler bulabilirsiniz. Hemen başlayın.

::: sidenote
Öğretici boyunca kavramların ayrıntılı açıklamaları ve belirli işlemlerin nasıl yapılacağı bu paragraftaki gibi işaretlenmiştir. Bu bölümlerin fazla ayrıntıya girdiğini düşünüyorsanız onları atlayabilirsiniz.
:::

Öyleyse başlayalım. Bu öğreticiyi uygularken çok eğlenmenizi ve Defold'a başlamanıza yardımcı olmasını umuyoruz.

> Bu öğreticinin varlıklarını [buradan](https://github.com/defold/sample-runner/tree/main/def-runner) indirin.

## Adım 1 - Kurulum ve hazırlık

İlk adım, [şu dosyaları indirmektir](https://github.com/defold/sample-runner/tree/main/def-runner).

Defold düzenleyicisini henüz indirip kurmadıysanız şimdi bunu yapma zamanı:

:[install](../shared/install.md)

Düzenleyici kurulup başlatıldıktan sonra yeni bir proje oluşturup hazırlama zamanı gelmiştir. "Empty Project" şablonundan [yeni bir proje](/manuals/project-setup/#creating-a-new-project) oluşturun.

::: sidenote
Bu öğretici [Spine Extension](https://github.com/defold/extension-spine) içindeki Spine özelliklerini kullanır. Eklentiyi *game.project* dosyasının bağımlılıklar bölümüne ekleyin.
:::

## Düzenleyici

Düzenleyiciyi ilk kez başlattığınızda hiçbir proje açık olmadan boş olarak açılır; bu yüzden menüden <kbd>Open Project</kbd> seçeneğini seçip yeni oluşturduğunuz projeyi açın. Ayrıca proje için bir "dal" (branch) oluşturmanız istenecektir.

Artık *Assets* bölmesinde projenin parçası olan bütün dosyaları göreceksiniz. "main/main.collection" dosyasına çift tıklarsanız dosya ortadaki düzenleyici görünümünde açılır:

![Düzenleyiciye genel bakış](images/runner/1/editor2_overview.png)

Düzenleyici şu ana alanlardan oluşur:

Assets bölmesi
: Projenizdeki bütün dosyaları gösterir. Farklı dosya türlerinin farklı simgeleri vardır. Bir dosyayı, türüne uygun düzenleyicide açmak için dosyaya çift tıklayın. Salt okunur özel *builtins* klasörü bütün projeler için ortaktır; varsayılan bir işleme betiği, bir yazı tipi, çeşitli bileşenlerin görüntüsünü oluşturmak için kullanılan işleme (rendering) materyalleri ve başka yararlı öğeler içerir.

Ana düzenleyici görünümü
: Düzenlediğiniz dosya türüne göre bu görünümde o türe uygun bir düzenleyici gösterilir. En sık kullanılanı, burada gördüğünüz Scene düzenleyicisidir. Açık olan her dosya ayrı bir sekmede gösterilir.

Changed Files
: Geçerli Git commit'ine göre yerelde eklenen, değiştirilen, yeniden adlandırılan veya silinen dosyaları içerir. Değiştirilmiş veya yeniden adlandırılmış metin dosyalarının farklarını tek seferde bir dosya için görüntüleyebilirsiniz; seçtiğiniz yerel değişiklikleri burada geri alabilirsiniz. Uzak depoyla eşitlemek için haricî bir Git istemcisi veya komut satırını kullanın.

Outline
: Düzenlenmekte olan dosyanın içeriğini hiyerarşik olarak gösterir. Bu görünüm üzerinden oyun nesnelerini (game object) ve bileşenleri (component) ekleyebilir, silebilir, değiştirebilir ve seçebilirsiniz.

Properties
: Seçili nesne veya bileşen üzerinde ayarlanmış özelliklerdir.

Console
: Oyun çalışırken bu görünüm, oyun motorunun çıktısını (günlükler, hatalar, hata ayıklama bilgileri vb.) ve betiklerinizdeki özel `print()` ve `pprint()` hata ayıklama iletilerini yakalar. Uygulamanız veya oyununuz başlamıyorsa ilk kontrol etmeniz gereken yer konsoldur. Konsolun arkasında hata bilgilerini gösteren sekmeler ve parçacık efektleri oluştururken kullanılan bir eğri düzenleyicisi bulunur.

## Oyunu çalıştırma

"Empty" proje şablonu gerçekten tamamen boştur. Yine de projeyi derleyip oyunu başlatmak için <kbd>Project ▸ Build</kbd> seçeneğini seçin.

![Derleme](images/runner/1/build_and_launch.png)

Siyah bir ekran pek heyecan verici olmayabilir, ancak bu çalışan bir Defold oyun uygulamasıdır ve onu kolayca daha ilgi çekici bir şeye dönüştürebiliriz. Öyleyse bunu yapalım.

::: sidenote
Defold düzenleyicisi dosyalar üzerinde çalışır. *Assets* bölmesindeki bir dosyaya çift tıklayarak onu uygun bir düzenleyicide açarsınız. Ardından dosyanın içeriği üzerinde çalışabilirsiniz.

Bir dosyayı düzenlemeyi bitirdiğinizde onu kaydetmeniz gerekir. Ana menüden <kbd>File ▸ Save</kbd> seçeneğini seçin. Düzenleyici, kaydedilmemiş değişiklikler içeren her dosyanın sekmesindeki dosya adına bir yıldız '\*' ekleyerek bunu belirtir.

![Kaydedilmemiş değişiklikler içeren dosya](images/runner/1/file_changed.png)
:::

## Projeyi hazırlama

Başlamadan önce projemizin birkaç ayarını yapalım. `Assets Pane` içinden *game.project* varlığını açın ve Display bölümüne kadar aşağı kaydırın. Projenin `width` ve `height` değerlerini sırasıyla `1280` ve `720` olarak ayarlayın.

Kahraman karakteri canlandırabilmemiz için projeye Spine eklentisini de eklemeniz gerekir. Spine eklentisinin, kurduğunuz Defold düzenleyicisi sürümüyle uyumlu bir sürümünü ekleyin. Kullanılabilir Spine sürümlerini burada görebilirsiniz:

[https://github.com/defold/extension-spine/releases](https://github.com/defold/extension-spine/releases)

Kullanmak istediğiniz sürümün zip dosyası bağlantısına sağ tıklayın:

![Sağ tıklayıp sürüm bağlantısını kopyalama](images/runner/extension-spine-releases.png)

Sürüm bağlantısını [game.project bağımlılıkları](/manuals/libraries/#setting-up-library-dependencies) listenize ekleyin. Spine eklentisi eklendikten sonra, eklentiyle birlikte gelen düzenleyici entegrasyonunu etkinleştirmek için düzenleyiciyi yeniden başlatmanız da gerekir.


## Adım 2 - Zemini oluşturma

İlk küçük adımları atıp karakterimiz için bir alan, daha doğrusu kayan bir zemin parçası oluşturalım. Bunu birkaç adımda yapacağız.

1. "ground01.png" ve "ground02.png" görüntü dosyalarını (varlık paketindeki "level-images" alt klasöründen) projede uygun bir konuma, örneğin "main" klasörünün içindeki "images" klasörüne sürükleyerek görüntü varlıklarını projeye aktarın.
2. Zemin dokularını tutmak için yeni bir *Atlas* dosyası oluşturun (*Assets* bölmesinde uygun bir klasöre, örneğin *main* klasörüne sağ tıklayıp <kbd>New ▸ Atlas File</kbd> seçeneğini seçin). Atlas dosyasına *level.atlas* adını verin.

  ::: sidenote
  Bir *atlas* (Atlas), ayrı görüntüleri tek ve daha büyük bir görüntü dosyasında birleştiren bir dosyadır. Bunun amacı yerden tasarruf etmek ve performansı artırmaktır. Atlaslar ve diğer 2B grafik özellikleri hakkında daha fazla bilgiyi [2B grafik belgelerinde](/manuals/2dgraphics) bulabilirsiniz.
  :::

3. *Outline* görünümünde atlasın köküne sağ tıklayıp <kbd>Add Images</kbd> seçeneğini seçerek zemin görüntülerini yeni atlasa ekleyin. İçe aktardığınız görüntüleri seçip *OK* düğmesine tıklayın. Artık atlastaki her görüntüye sprite bileşenlerinde, parçacık efektlerinde ve diğer görsel öğelerde kullanılacak tek karelik bir animasyon (durağan görüntü) olarak erişilebilir. Dosyayı kaydedin.

  ![Yeni atlas oluşturma](images/runner/1/new_atlas.png)

  ![Atlasa görüntü ekleme](images/runner/1/add_images_to_atlas.png)

  ::: sidenote
  *Neden çalışmıyor!?* Defold'a yeni başlayanların sık yaşadığı bir sorun kaydetmeyi unutmaktır! Bir atlasa görüntü ekledikten sonra bu görüntüye erişebilmek için dosyayı kaydetmeniz gerekir.
  :::

4. Zemin için *ground.collection* adlı bir koleksiyon (collection) dosyası oluşturup içine 7 oyun nesnesi ekleyin (*Outline* görünümünde koleksiyonun köküne sağ tıklayıp <kbd>Add Game Object</kbd> seçeneğini seçin). *Properties* görünümündeki *Id* özelliğini değiştirerek nesnelere "ground0", "ground1", "ground2" vb. adlar verin. Defold'un yeni oyun nesnelerine otomatik olarak benzersiz bir tanımlayıcı atadığını unutmayın.

5. Her nesneye bir sprite bileşeni ekleyin (*Outline* görünümünde oyun nesnesine sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin, ardından *Sprite* seçeneğini seçip *OK* düğmesine tıklayın), sprite bileşeninin *Image* özelliğini az önce oluşturduğunuz atlasa ayarlayın ve sprite bileşeninin varsayılan animasyonunu iki zemin görüntüsünden birine ayarlayın. _Sprite bileşeninin_ (oyun nesnesinin değil) X konumunu 190, Y konumunu 40 yapın. Görüntünün genişliği 380 piksel olduğundan ve onu bunun yarısı kadar piksel yana kaydırdığımızdan, oyun nesnesinin dayanak noktası sprite görüntüsünün en sol kenarında olacaktır.

  ![Zemin koleksiyonu oluşturma](images/runner/1/ground_collection.png)

6. Kullandığımız grafikler biraz fazla büyük olduğundan her oyun nesnesini %60'a ölçekleyin (X ve Y için 0.6 ölçeği, 228 piksel genişliğinde zemin parçaları verir).

  ![Zemini ölçekleme](images/runner/1/scale_ground.png)

7. Bütün _oyun nesnelerini_ yan yana dizin. _Oyun nesnelerinin_ (sprite bileşenlerinin değil) X konumlarını 0, 228, 456, 684, 912, 1140 ve 1368 (228 piksel genişliğin katları) olarak ayarlayın.

  ::: sidenote
  Muhtemelen en kolayı, sprite bileşeni eklenmiş ve ölçeği ayarlanmış tek bir oyun nesnesi oluşturup onu kopyalamaktır. Nesneyi *Outline* görünümünde seçin, ardından <kbd>Edit ▸ Copy</kbd> ve sonra <kbd>Edit ▸ Paste</kbd> seçeneğini seçin.

  Daha büyük veya daha küçük karolar istiyorsanız yalnızca ölçeği değiştirebilirsiniz. Ancak bunu yaptığınızda bütün zemin oyun nesnelerinin X konumlarını da yeni genişliğin katlarına ayarlamanız gerekir.
  :::

8. Dosyayı kaydedin, ardından *ground.collection* dosyasını *main.collection* dosyasına ekleyin: önce *main.collection* dosyasına çift tıklayın, ardından *Outline* görünümünde kök nesneye sağ tıklayıp <kbd>Add Collection From File</kbd> seçeneğini seçin. İletişim kutusunda *ground.collection* dosyasını seçip *OK* düğmesine tıklayın. *ground.collection* koleksiyonunu 0, 0, 0 konumuna yerleştirdiğinizden emin olun; aksi halde görüntüde kaymış olacaktır. Kaydedin.

9. Her şeyin yerinde olduğunu görmek için oyunu başlatın (<kbd>Project ▸ Build</kbd>).

  ![Durağan zemin](images/runner/1/still_ground.png)

Şimdiye kadar oluşturduğumuz bütün bu şeylerin aslında ne olduğu konusunda kafanız karışmış olabilir. Bu yüzden biraz durup herhangi bir Defold projesindeki en temel yapı taşlarına bakalım:

Oyun nesneleri
: Çalışan oyunda var olan öğelerdir. Her oyun nesnesinin 3B uzayda bir konumu, dönmesi ve ölçeği vardır. Görünür olması gerekmez. Bir oyun nesnesi; grafikler (sprite bileşenleri, karo haritaları, modeller, Spine modelleri ve parçacık efektleri), sesler, fizik, fabrikalar (factory; çalışma sırasında nesne oluşturmak için) ve daha fazlası gibi yetenekler ekleyen, istenen sayıda _bileşen_ barındırır. Oyun nesnesine davranış kazandırmak için Lua _betik bileşenleri_ de eklenebilir. Oyunlarınızda var olan her oyun nesnesinin, ileti aktarımı yoluyla onunla iletişim kurmak için ihtiyaç duyduğunuz bir *id* değeri vardır.

Koleksiyonlar
: Koleksiyonlar, çalışan bir oyunda kendi başlarına var olmaz; oyun nesnelerinin statik olarak adlandırılmasını ve aynı zamanda aynı oyun nesnesinin birden çok örneğinin oluşturulmasını sağlamak için kullanılır. Uygulamada koleksiyonlar, oyun nesneleri ve diğer koleksiyonlar için kapsayıcı olarak kullanılır. Koleksiyonları, oyun nesneleri ve koleksiyonlardan oluşan karmaşık hiyerarşilerin prototipleri (diğer motorlarda "prefab" veya "blueprint" olarak da bilinir) gibi kullanabilirsiniz. Motor başlangıçta bir ana koleksiyon yükler ve içine koyduğunuz her şeyi hayata geçirir. Varsayılan olarak bu, projenizin *main* klasöründeki *main.collection* dosyasıdır; ancak bunu proje ayarlarından değiştirebilirsiniz.

Şimdilik bu açıklamalar muhtemelen yeterlidir. Yine de bu konuların çok daha kapsamlı bir incelemesini [Yapı taşları kılavuzunda](/manuals/building-blocks) bulabilirsiniz. Defold'un nasıl çalıştığını daha derinden anlamak için daha sonra bu kılavuzu okumanız iyi olacaktır.

## Adım 3 - Zemini hareket ettirme

Bütün zemin parçaları yerinde olduğuna göre onları hareket ettirmek oldukça basittir. Fikir şu: parçaları sağdan sola taşıyın; bir parça ekranın dışındaki en sol kenara ulaştığında onu en sağdaki konuma taşıyın. Bütün bu oyun nesnelerini hareket ettirmek için bir Lua betiği gerekir; öyleyse bir tane oluşturalım:

1. *Assets* bölmesinde *main* klasörüne sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin. Yeni dosyaya *ground.script* adını verin.
2. Lua betik düzenleyicisini açmak için yeni dosyaya çift tıklayın.
3. Dosyanın varsayılan içeriğini silip aşağıdaki Lua kodunu içine kopyalayın, ardından dosyayı kaydedin.

```lua
-- ground.script
local pieces = { "ground0", "ground1", "ground2", "ground3",
                    "ground4", "ground5", "ground6" } -- <1>

function init(self) -- <2>
    self.speed = 360  -- Speed in pixels/s
end

function update(self, dt) -- <3>
    for i, p in ipairs(pieces) do -- <4>
        local pos = go.get_position(p)
        if pos.x <= -228 then -- <5>
            pos.x = 1368 + (pos.x + 228)
        end
        pos.x = pos.x - self.speed * dt -- <6>
        go.set_position(pos, p) -- <7>
    end
end
```
1. Zemin oyun nesnelerinin tanımlayıcılarını, üzerlerinde dolaşabilmek için bir Lua tablosunda saklayın.
2. `init()` işlevi, oyun nesnesi oyunda hayata geçtiğinde çağrılır. Zeminin süratini tutan, bu nesneye özgü bir üye değişkenine başlangıç değeri atıyoruz.
3. `update()` her karede bir kez, genellikle saniyede 60 kez çağrılır. `dt`, son çağrıdan bu yana geçen saniye sayısını içerir.
4. Bütün zemin oyun nesneleri üzerinde dolaşın.
5. Geçerli konumu yerel bir değişkende saklayın; ardından geçerli nesne en sol kenardaysa onu en sağ kenara taşıyın.
6. Geçerli X konumunu ayarlanan süratle azaltın. Piksel/s cinsinden, kare hızından bağımsız bir sürat elde etmek için `dt` ile çarpın.
7. Nesnenin konumunu yeni süratle güncelleyin.

::: sidenote
Defold, verilerinizi ve oyun nesnelerinizi yöneten hızlı bir motor çekirdeğidir. Oyununuz için gereken her türlü mantık veya davranış Lua dilinde oluşturulur. Lua, oyun mantığı yazmaya çok uygun, hızlı ve hafif bir programlama dilidir. Dili öğrenmek için [Programming in Lua](http://www.lua.org/pil/) kitabı ve resmî [Lua başvuru kılavuzu](http://www.lua.org/manual/5.3/) gibi harika kaynaklar bulunur.

Defold, Lua'nın üzerine bir dizi API ve oyun nesneleri arasındaki iletişimi programlamanızı sağlayan bir _ileti aktarımı_ (message passing) sistemi ekler. Bunun nasıl çalıştığına ilişkin ayrıntılar için [İleti aktarımı kılavuzuna](/manuals/message-passing) bakın.
:::

::: sidenote
Düzenleyicinin Assets Pane, Console ve Outline bölümlerini sırasıyla <kbd>F6</kbd>, <kbd>F7</kbd> ve <kbd>F8</kbd> tuşlarıyla açıp kapatabilirsiniz
:::

Artık bir betik dosyamız olduğuna göre bir oyun nesnesindeki bileşene bu dosyanın başvurusunu eklememiz gerekir. Böylece betik, oyun nesnesinin yaşam döngüsünün bir parçası olarak yürütülür. Bunun için *ground.collection* içinde yeni bir oyun nesnesi oluşturup bu nesneye, az önce oluşturduğumuz Lua betik dosyasına başvuran bir *Script* bileşeni ekleyeceğiz:

1. Koleksiyonun köküne sağ tıklayıp <kbd>Add Game Object</kbd> seçeneğini seçin. Nesnenin *id* değerini "controller" olarak ayarlayın.
2. "controller" nesnesine sağ tıklayıp <kbd>Add Component from file</kbd> seçeneğini seçin, ardından *ground.script* dosyasını seçin.

![Zemin denetleyicisi](images/runner/1/ground_controller.png)

Artık oyunu çalıştırdığınızda "controller" oyun nesnesi, *Script* bileşenindeki betiği çalıştırarak zeminin ekran boyunca akıcı biçimde kaymasını sağlayacaktır.

## Adım 4 - Bir kahraman karakter oluşturma

Kahraman karakter, şu bileşenlerden oluşan bir oyun nesnesi olacak:

Bir *Spine Model*
: Bize, vücut parçaları akıcı biçimde (ve düşük işlem maliyetiyle) canlandırılabilen, kâğıt bebeğe benzeyen küçük bir kahraman karakter sağlar.

Bir *Collision Object*
: Bu çarpışma nesnesi (collision object), kahraman karakter ile bölümde üzerine koşabileceği, tehlikeli olan veya toplanabilen şeyler arasındaki çarpışmaları algılar.

Bir *Script*
: Kullanıcı girdisini alıp ona tepki verir, kahraman karakteri zıplatır, canlandırır ve çarpışmaları ele alır.

Vücut parçalarının görüntülerini içe aktararak başlayın; ardından bunları *hero.atlas* adını vereceğimiz yeni bir atlasa ekleyin:

1. *Assets* bölmesine sağ tıklayıp <kbd>New ▸ Folder</kbd> seçeneğini seçerek yeni bir klasör oluşturun. Tıklamadan önce bir klasör seçmediğinizden emin olun; aksi halde yeni klasör, seçili klasörün içinde oluşturulur. Klasöre "hero" adını verin.
2. *hero* klasörüne sağ tıklayıp <kbd>New ▸ Atlas File</kbd> seçeneğini seçerek yeni bir atlas dosyası oluşturun. Dosyaya *hero.atlas* adını verin.
3. *hero* klasöründe *images* adlı yeni bir alt klasör oluşturun. *hero* klasörüne sağ tıklayıp <kbd>New ▸ Folder</kbd> seçeneğini seçin.
4. Varlık paketindeki *hero-images* klasöründe bulunan vücut parçası görüntülerini, *Assets* bölmesinde az önce oluşturduğunuz *images* klasörüne sürükleyin.
5. *hero.atlas* dosyasını açın, *Outline* görünümündeki kök düğüme sağ tıklayıp <kbd>Add Images</kbd> seçeneğini seçin. Bütün vücut parçası görüntülerini seçip *OK* düğmesine tıklayın.
6. Atlas dosyasını kaydedin.

![Kahraman atlası](images/runner/2/hero_atlas.png)

Spine animasyon verilerini de içe aktarıp bunlar için bir *Spine Scene* hazırlamamız gerekir:

1. *hero.spinejson* dosyasını (varlık paketine dahildir) *Assets* bölmesindeki *hero* klasörüne sürükleyin.
2. Bir *Spine Scene* dosyası oluşturun. *hero* klasörüne sağ tıklayıp <kbd>New ▸ Spine Scene File</kbd> seçeneğini seçin. Dosyaya *hero.spinescene* adını verin.
3. *Spine Scene* dosyasını açıp düzenlemek için yeni dosyaya çift tıklayın.
4. *spine_json* özelliğini, içe aktarılan *hero.spinejson* JSON dosyasına ayarlayın. Özelliğe tıklayın, ardından kaynak tarayıcısını açmak için *...* dosya seçici düğmesine tıklayın.
5. *atlas* özelliğini, *hero.atlas* dosyasına başvuracak şekilde ayarlayın.
6. Dosyayı kaydedin.

![Kahramanın Spine sahnesi](images/runner/2/hero_spinescene.png)

::: sidenote
*hero.spinejson* dosyası Spine JSON biçiminde dışa aktarılmıştır. Bu tür dosyalar oluşturabilmek için Spine animasyon yazılımına ihtiyacınız vardır. Başka bir animasyon yazılımı kullanmak istiyorsanız animasyonlarınızı sprite sayfaları olarak dışa aktarabilir ve bunları *Tile Source* veya *Atlas* kaynaklarından kare dizisi animasyonları (flip-book animation) olarak kullanabilirsiniz. Daha fazla bilgi için [Animasyon](/manuals/animation) kılavuzuna bakın.
:::

### Oyun nesnesini oluşturma

Artık kahramanın oyun nesnesini oluşturmaya başlayabiliriz:

1. *hero.go* adlı yeni bir dosya oluşturun (*hero* klasörüne sağ tıklayıp <kbd>New ▸ Game Object File</kbd> seçeneğini seçin).
2. Oyun nesnesi dosyasını açın.
3. İçine bir *Spine Model* bileşeni ekleyin. (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin, ardından "Spine Model" seçeneğini seçin.)
4. Bileşenin *Spine Scene* özelliğini, az önce oluşturduğunuz *hero.spinescene* dosyasına ayarlayın ve varsayılan animasyon olarak "run_right" seçeneğini seçin (animasyonu daha sonra gerektiği gibi düzenleyeceğiz)
5. Dosyayı kaydedin.

![Spine modeli özellikleri](images/runner/2/spinemodel_properties.png)

Şimdi çarpışmanın çalışması için fizik ekleme zamanı:

1. Kahraman oyun nesnesine bir *Collision Object* bileşeni ekleyin. (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin, ardından "Collision Object" seçeneğini seçin)
2. Yeni bileşene sağ tıklayıp <kbd>Add Shape</kbd> seçeneğini seçin. Karakterin vücudunu kaplayacak iki şekil ekleyin. Bir küre ve bir kutu yeterli olacaktır.
3. Şekillere tıklayın ve onları uygun konumlara taşımak için *Move Tool* aracını (<kbd>Scene ▸ Move Tool</kbd>) kullanın.
4. *Collision Object* bileşenini seçip *Type* özelliğini "Kinematic" olarak ayarlayın.

::: sidenote
Kinematik çarpışma ("Kinematic"), çarpışmaların algılanmasını istediğimiz, ancak fizik motorunun çarpışmaları otomatik olarak çözmeyeceği ve nesnelerin simülasyonunu yapmayacağı anlamına gelir. Fizik motoru birkaç farklı çarpışma nesnesi türünü destekler. Bunlar hakkında daha fazla bilgiyi [Fizik belgelerinde](/manuals/physics) bulabilirsiniz.
:::

Çarpışma nesnesinin nelerle etkileşime girmesi gerektiğini belirtmemiz önemlidir:

1. *Group* özelliğini "hero" adlı yeni bir çarpışma grubuna ayarlayın.
2. *Mask* özelliğini, bu çarpışma nesnesinin çarpışmalarını algılayacağı diğer grup olan "geometry" olarak ayarlayın. "geometry" grubunun henüz var olmadığını, ancak yakında bu gruba ait çarpışma nesneleri ekleyeceğimizi unutmayın.

Son olarak yeni bir *hero.script* dosyası oluşturup oyun nesnesine ekleyin.

1. *Assets* bölmesindeki *hero* klasörüne sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin. Yeni dosyaya *hero.script* adını verin.
2. Yeni dosyayı açın, ardından aşağıdaki kodu betik dosyasına kopyalayıp yapıştırın ve kaydedin. (Kahramanın çarpışma şeklini çarpıştığı nesneden ayıran çözücü dışında kod oldukça basittir. Bu işlemi `handle_geometry_contact()` işlevi yapar.)

![Kahraman oyun nesnesi](images/runner/2/hero_game_object.png)

::: sidenote
Çarpışmayı kendimiz ele almamızın nedeni şudur: karakterin çarpışma nesnesinin türünü dinamik olarak ayarlasaydık motor, ilgili cisimler için Newton mekaniğine dayalı bir simülasyon yapardı. Bunun gibi bir oyunda böyle bir simülasyon en uygun çözüm olmaktan uzaktır; bu nedenle çeşitli kuvvetlerle fizik motoruyla uğraşmak yerine kontrolü tamamen ele alıyoruz.

Bunu yapmak ve çarpışmaları doğru biçimde ele almak için biraz vektör matematiği gerekir. Kinematik çarpışmaların nasıl çözüleceğine ilişkin ayrıntılı bir açıklama [Fizik belgelerinde](/manuals/physics-resolving-collisions/) bulunur.
:::

```lua
-- gravity pulling the player down in pixel units/sˆ2
local gravity = -20

-- take-off speed when jumping in pixel units/s
local jump_takeoff_speed = 900

function init(self)
    -- this tells the engine to send input to on_input() in this script
    msg.post(".", "acquire_input_focus")

    -- save the starting position
    self.position = go.get_position()

    -- keep track of movement vector and if there is ground contact
    self.velocity = vmath.vector3(0, 0, 0)
    self.ground_contact = false
end

function final(self)
    -- Return input focus when the object is deleted
    msg.post(".", "release_input_focus")
end

function update(self, dt)
    local gravity = vmath.vector3(0, gravity, 0)

    if not self.ground_contact then
        -- Apply gravity if there's no ground contact
        self.velocity = self.velocity + gravity
    end

    -- apply velocity to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    -- reset volatile state
    self.correction = vmath.vector3()
    self.ground_contact = false
end

local function handle_geometry_contact(self, normal, distance)
    -- project the correction vector onto the contact normal
    -- (the correction vector is the 0-vector for the first contact point)
    local proj = vmath.dot(self.correction, normal)
    -- calculate the compensation we need to make for this contact point
    local comp = (distance - proj) * normal
    -- add it to the correction vector
    self.correction = self.correction + comp
    -- apply the compensation to the player character
    go.set_position(go.get_position() + comp)
    -- check if the normal points enough up to consider the player standing on the ground
    -- (0.7 is roughly equal to 45 degrees deviation from pure vertical direction)
    if normal.y > 0.7 then
        self.ground_contact = true
    end
    -- project the velocity onto the normal
    proj = vmath.dot(self.velocity, normal)
    -- if the projection is negative, it means that some of the velocity points towards the contact point
    if proj < 0 then
        -- remove that component in that case
        self.velocity = self.velocity - proj * normal
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("contact_point_response") then
        -- check if we received a contact point message. One message for each contact point
        if message.group == hash("geometry") then
            handle_geometry_contact(self, message.normal, message.distance)
        end
    end
end

local function jump(self)
    -- only allow jump from ground
    if self.ground_contact then
        -- set take-off speed
        self.velocity.y = jump_takeoff_speed
    end
end

local function abort_jump(self)
    -- cut the jump short if we are still going up
    if self.velocity.y > 0 then
        -- scale down the upwards speed
        self.velocity.y = self.velocity.y * 0.5
    end
end

function on_input(self, action_id, action)
    if action_id == hash("jump") or action_id == hash("touch") then
        if action.pressed then
            jump(self)
        elseif action.released then
            abort_jump(self)
        end
    end
end
```

1. Betiği kahraman nesnesine bir *Script* bileşeni olarak ekleyin (*Outline* görünümünde *hero.go* dosyasının köküne sağ tıklayıp <kbd>Add Component from File</kbd> seçeneğini seçin, ardından *hero.script* dosyasını seçin).

İsterseniz şimdi kahraman karakteri geçici olarak ana koleksiyona ekleyip oyunu çalıştırmayı deneyerek karakterin dünyanın içinden geçip düştüğünü görebilirsiniz.

Kahramanın işlevsel olması için gereken son şey girdidir. Yukarıdaki betik, "jump" ve "touch" (dokunmatik ekranlar için) eylemlerine yanıt veren bir `on_input()` işlevi zaten içerir. Bu eylemler için girdi eşlemeleri (input binding) ekleyelim.

1. "input/game.input_bindings" dosyasını açın
2. "KEY_SPACE" için bir tuş tetikleyicisi ekleyip eyleme "jump" adını verin
3. "TOUCH_MULTI" için bir dokunma tetikleyicisi ekleyip eyleme "touch" adını verin. (Eylem adlarını istediğiniz gibi seçebilirsiniz, ancak betiğinizdeki adlarla eşleşmeleri gerekir. Birden çok tetikleyicide aynı eylem adını kullanamayacağınızı unutmayın)
4. Dosyayı kaydedin.

![Girdi eşlemeleri](images/runner/2/input_bindings.png)

## Adım 5 - Bölümü yeniden yapılandırma

Kahraman karakteri çarpışma dahil her şeyiyle hazırladığımıza göre, çarpışabileceği (veya üzerinde koşabileceği) bir şey olması için zemine de çarpışma eklememiz gerekir. Birazdan bunu yapacağız; ancak önce küçük bir yeniden yapılandırma yapıp bölümle ilgili her şeyi ayrı bir koleksiyona yerleştirelim ve dosya yapısını biraz düzenleyelim:

1. Yeni bir *level.collection* dosyası oluşturun (*Assets* bölmesinde *main* klasörüne sağ tıklayıp <kbd>New ▸ Collection File</kbd> seçeneğini seçin).
2. Yeni dosyayı açın, *Outline* görünümündeki köke sağ tıklayıp <kbd>Add Collection from File</kbd> seçeneğini seçin ve *ground.collection* dosyasını seçin.
3. *level.collection* içinde *Outline* görünümündeki köke sağ tıklayıp <kbd>Add Game Object File</kbd> seçeneğini seçin ve *hero.go* dosyasını seçin.
4. Şimdi proje kökünde *level* adlı yeni bir klasör oluşturun (*game.project* dosyasının altındaki beyaz alana sağ tıklayıp <kbd>New ▸ Folder</kbd> seçeneğini seçin), ardından şimdiye kadar oluşturduğunuz bölüm varlıklarını buraya taşıyın: *level.collection* ve *level.atlas* dosyalarını, bölüm atlasının görüntülerini tutan "images" klasörünü, *ground.collection* ve *ground.script* dosyalarını.
5. *main.collection* dosyasını açın, *ground.collection* koleksiyonunu silin ve yerine artık *ground.collection* koleksiyonunu içeren *level.collection* koleksiyonunu ekleyin (sağ tıklayıp <kbd>Add Collection from File</kbd> seçeneğini seçin). Koleksiyonu 0, 0, 0 konumuna yerleştirdiğinizden emin olun.

::: sidenote
Şimdiye kadar fark etmiş olabileceğiniz gibi, *Assets* bölmesinde görünen dosya hiyerarşisi, koleksiyonlarınızda oluşturduğunuz içerik yapısından bağımsızdır. Koleksiyon ve oyun nesnesi dosyalarından tek tek dosyalara başvurulur, ancak bu dosyaların konumları tamamen size bağlıdır.

Bir dosyayı yeni bir konuma taşımak istediğinizde Defold, dosyaya yapılan başvuruları otomatik olarak güncelleyerek (yeniden yapılandırma) yardımcı olur. Oyun gibi karmaşık bir yazılım geliştirirken, proje büyüyüp değiştikçe yapısını değiştirebilmek son derece yararlıdır. Defold bunu destekler ve süreci kolaylaştırır; bu yüzden dosyalarınızı taşımaktan çekinmeyin!
:::

Bölüm koleksiyonuna, betik bileşeni olan bir denetleyici oyun nesnesi de eklememiz gerekir:

1. Yeni bir betik dosyası oluşturun. *Assets* bölmesindeki *level* klasörüne sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin. Dosyaya *controller.script* adını verin.
2. Betik dosyasını açın, aşağıdaki kodu içine kopyalayın ve dosyayı kaydedin:

    ```lua
    -- controller.script
    go.property("speed", 360) -- <1>

    function init(self)
        msg.post("ground/controller#ground", "set_speed", { speed = self.speed })
    end
    ```
    1. Bu bir betik özelliğidir. Ona varsayılan bir değer atıyoruz; ancak yerleştirilmiş herhangi bir betik örneği, doğrudan düzenleyicinin özellikler görünümünde bu değeri geçersiz kılabilir.

3. *level.collection* dosyasını açın.
4. *Outline* görünümündeki köke sağ tıklayıp <kbd>Add Game Object</kbd> seçeneğini seçin.
5. *Id* değerini "controller" olarak ayarlayın.
6. *Outline* görünümündeki "controller" oyun nesnesine sağ tıklayıp <kbd>Add Component from File</kbd> seçeneğini seçin ve *level* klasöründeki *controller.script* dosyasını seçin.
7. Dosyayı kaydedin.

![Betik özelliği](images/runner/2/script_property.png)

::: sidenote
"controller" oyun nesnesi ayrı bir dosyada bulunmaz; bölüm koleksiyonunda yerinde (in-place) oluşturulur. Bu, oyun nesnesi örneğinin yerinde tanımlanmış verilerden oluşturulduğu anlamına gelir. Bu nesne gibi tek bir amaca hizmet eden oyun nesneleri için bu uygundur. Bir oyun nesnesinin birden çok örneğine ihtiyacınız varsa ve her örneği oluşturmak için kullanılan prototipi/şablonu değiştirebilmek istiyorsanız, bir oyun nesnesi dosyası oluşturup oyun nesnesini dosyadan koleksiyona eklemeniz yeterlidir. Bu işlem, dosyaya prototip/şablon olarak başvuran bir oyun nesnesi oluşturur.

Bu "controller" oyun nesnesinin amacı, çalışan bölümle ilgili her şeyi kontrol etmektir. Yakında bu betik, kahramanın etkileşime gireceği platformları ve paraları oluşturmakla sorumlu olacak; ancak şimdilik yalnızca bölümün süratini ayarlayacaktır.
:::

Bölüm denetleyicisi betiğinin `init()` işlevi, zemin denetleyicisi nesnesinin betik bileşenine, tanımlayıcısıyla adresleyerek bir ileti gönderir:

```lua
msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
```

Denetleyici oyun nesnesi "ground" koleksiyonunda bulunduğundan tanımlayıcısı `"ground/controller"` olarak ayarlanır. Ardından nesne tanımlayıcısını bileşen tanımlayıcısından ayıran `"#"` karakterinden sonra `"controller"` bileşen tanımlayıcısını ekleriz. Zemin betiğinde henüz `set_speed` iletisine tepki verecek kod bulunmadığını unutmayın; bu yüzden *ground.script* dosyasına bir `on_message()` işlevi ve bunun için gereken mantığı eklememiz gerekir.

1. *ground.script* dosyasını açın.
2. Aşağıdaki kodu ekleyip dosyayı kaydedin:

```lua
-- ground.script
function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then -- <1>
        self.speed = message.speed -- <2>
    end
end
```
1. Bütün iletilerin gönderildiklerinde dahili olarak karma değerleri alınır ve karşılaştırma karma değeriyle yapılmalıdır.
2. İleti verisi, iletiyle birlikte gönderilen verileri içeren bir Lua tablosudur.

![Zemin kodunu ekleme](images/runner/insert_ground_code.png)

## Adım 6 - Zemin fiziği ve platformlar

Bu noktada zemine fiziksel çarpışma eklememiz gerekir:

1. *ground.collection* dosyasını açın.
2. Uygun bir oyun nesnesine yeni bir *Collision Object* bileşeni ekleyin. Zemin betiği çarpışmalara tepki vermediğinden (bu mantığın tamamı kahraman betiğindedir) bileşeni herhangi bir _hareketsiz_ oyun nesnesine koyabiliriz (zemin karolarının nesneleri hareketsiz değildir; bu yüzden onları kullanmayın). "controller" oyun nesnesi uygun bir adaydır, ancak isterseniz bunun için ayrı bir nesne oluşturabilirsiniz. Oyun nesnesine sağ tıklayıp <kbd>Add Component</kbd> seçeneğini, ardından *Collision Object* seçeneğini seçin.
3. *Collision Object* bileşenine sağ tıklayıp <kbd>Add Shape</kbd> seçeneğini, ardından *Box* seçeneğini seçerek bir kutu şekli ekleyin.
4. Kutunun bütün zemin karolarını kaplamasını sağlamak için *Move Tool* ve *Scale Tool* araçlarını (<kbd>Scene ▸ Move Tool</kbd> ve <kbd>Scene ▸ Scale Tool</kbd>) kullanın.
5. Zeminin fizik nesnesi hareket etmeyeceğinden çarpışma nesnesinin *Type* özelliğini "Static" olarak ayarlayın.
6. Çarpışma nesnesinin *Group* özelliğini "geometry", *Mask* özelliğini ise "hero" olarak ayarlayın. Artık kahramanın çarpışma nesnesi ile bu nesne, aralarındaki çarpışmaları algılayacaktır.
7. Dosyayı kaydedin.

![Zemin çarpışması](images/runner/2/ground_collision.png)

Artık oyunu çalıştırmayı deneyebilirsiniz (<kbd>Project ▸ Build</kbd>). Kahraman karakterin zeminde koşması ve <kbd>Space</kbd> tuşuyla zıplayabilmesi gerekir. Oyunu mobil cihazda çalıştırırsanız ekrana dokunarak zıplayabilirsiniz.

Oyun dünyamızdaki hayatı biraz daha az sıkıcı hale getirmek için üzerine zıplanacak platformlar eklemeliyiz.

1. Varlık paketindeki *rock_planks.png* görüntü dosyasını *level/images* alt klasörüne sürükleyin.
2. *level.atlas* dosyasını açıp yeni görüntüyü atlasa ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Images</kbd> seçeneğini seçin).
3. Dosyayı kaydedin.
4. *level* klasöründe *platform.go* adlı yeni bir *Game Object* dosyası oluşturun. (*Assets* bölmesindeki *level* klasörüne sağ tıklayıp <kbd>New ▸ Game Object File</kbd> seçeneğini seçin.)
5. Oyun nesnesine bir *Sprite* bileşeni ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini, ardından *Sprite* seçeneğini seçin).
6. *Image* özelliğini *level.atlas* dosyasına başvuracak şekilde ayarlayıp *Default Animation* değerini "rock_planks" yapın. Kolaylık olması için bölüm nesnelerini "level/objects" adlı bir alt klasörde tutun.
7. Platform oyun nesnesine bir *Collision Object* bileşeni ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin).
8. Bileşenin *Type* değerini "Kinematic", *Group* ve *Mask* değerlerini ise sırasıyla "geometry" ve "hero" olarak ayarladığınızdan emin olun.
9. *Collision Object* bileşenine bir *Box Shape* ekleyin. (*Outline* görünümündeki bileşene sağ tıklayıp <kbd>Add Shape</kbd> seçeneğini seçin, ardından *Box* seçeneğini seçin).
10. *Collision Object* bileşenindeki şeklin platformu kaplamasını sağlamak için *Move Tool* ve *Scale Tool* araçlarını (<kbd>Scene ▸ Move Tool</kbd> ve <kbd>Scene ▸ Scale Tool</kbd>) kullanın.
11. *platform.script* adlı bir *Script* dosyası oluşturun (*Assets* bölmesine sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin) ve aşağıdaki kodu dosyaya yerleştirip kaydedin:

    ```lua
    -- platform.script
    function init(self)
        self.speed = 540      -- Default speed in pixels/s
    end

    function update(self, dt)
        local pos = go.get_position()
        if pos.x < -500 then
            go.delete() -- <1>
        end
        pos.x = pos.x - self.speed * dt
        go.set_position(pos)
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("set_speed") then
            self.speed = message.speed
        end
    end
    ```
    1. Platform ekranın sağ kenarının dışına taşındığında onu silmeniz yeterlidir

12. *platform.go* dosyasını açıp yeni betiği bir bileşen olarak ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component From File</kbd> seçeneğini seçin ve *platform.script* dosyasını seçin).
13. *platform.go* dosyasını yeni bir dosyaya kopyalayın (*Assets* bölmesindeki dosyaya sağ tıklayıp <kbd>Copy</kbd> seçeneğini seçin, ardından tekrar sağ tıklayıp <kbd>Paste</kbd> seçeneğini seçin) ve yeni dosyaya *platform_long.go* adını verin.
14. *platform_long.go* dosyasını açıp ikinci bir *Sprite* bileşeni ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin). Alternatif olarak mevcut *Sprite* bileşenini kopyalayabilirsiniz.
15. *Sprite* bileşenlerini yan yana yerleştirmek için *Move Tool* aracını (<kbd>Scene ▸ Move Tool</kbd>) kullanın.
16. *Collision Object* bileşenindeki şeklin her iki platformu da kaplamasını sağlamak için *Move Tool* ve *Scale Tool* araçlarını kullanın.

![Platform](images/runner/2/platform_long.png)

::: sidenote
Hem *platform.go* hem de *platform_long.go* dosyasının aynı betik dosyasına başvuran *Script* bileşenleri bulunduğunu unutmayın. Bu iyi bir durumdur; çünkü betik dosyasında yaptığımız her değişiklik hem normal hem de uzun platformların davranışını etkileyecektir.
:::

## Çalışma sırasında platform oluşturma

Oyunun fikri, basit bir sonsuz koşu oyunu olmasıdır. Bu, platform oyun nesnelerinin düzenleyicide bir koleksiyona yerleştirilemeyeceği anlamına gelir. Onları çalışma sırasında dinamik olarak oluşturmamız gerekir:

1. *level.collection* dosyasını açın.
2. "controller" oyun nesnesine iki *Factory* bileşeni ekleyin (nesneye sağ tıklayıp <kbd>Add Component</kbd> seçeneğini, ardından *Factory* seçeneğini seçin)
3. Bileşenlerin *Id* özelliklerini "platform_factory" ve "platform_long_factory" olarak ayarlayın.
4. "platform_factory" bileşeninin *Prototype* özelliğini */level/objects/platform.go* dosyasına ayarlayın.
5. "platform_long_factory" bileşeninin *Prototype* özelliğini */level/objects/platform_long.go* dosyasına ayarlayın.
6. Dosyayı kaydedin.
7. Bölümü yöneten *controller.script* dosyasını açın.
8. Betiği aşağıdaki içeriğe sahip olacak şekilde değiştirin ve dosyayı kaydedin:

```lua
-- controller.script
go.property("speed", 360)

local grid = 460
local platform_heights = { 100, 200, 350 } -- <1>

function init(self)
    msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
    self.gridw = 0
end

function update(self, dt) -- <2>
    self.gridw = self.gridw + self.speed * dt

    if self.gridw >= grid then
        self.gridw = 0

        -- Maybe spawn a platform at random height
        if math.random() > 0.2 then
            local h = platform_heights[math.random(#platform_heights)]
            local f = "#platform_factory"
            if math.random() > 0.5 then
                f = "#platform_long_factory"
            end

            local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
            msg.post(p, "set_speed", { speed = self.speed })
        end
    end
end
```
1. Platformların oluşturulacağı Y konumu için önceden tanımlanmış değerler.
2. `update()` işlevi her karede bir kez çağrılır; bunu, belirli aralıklarla (üst üste binmeyi önlemek için) ve yüksekliklerde normal veya uzun bir platform oluşturup oluşturmayacağımıza karar vermek için kullanırız. Farklı oynanışlar oluşturmak için çeşitli oluşturma algoritmalarını denemek kolaydır.

Şimdi oyunu çalıştırın (<kbd>Project ▸ Build</kbd>).

Vay canına, bu (neredeyse) oynanabilir bir şeye dönüşmeye başlıyor...

![Oyunu çalıştırma](images/runner/2/run_game.png)

## Adım 7 - Animasyon ve ölüm

İlk yapacağımız şey, kahraman karaktere hayat vermek. Şu anda zavallı karakter bir koşu döngüsüne takılıp kalmış durumda; zıplamalara veya başka şeylere iyi tepki vermiyor. Varlık paketinden eklediğimiz Spine dosyası aslında tam da bunun için bir dizi animasyon içeriyor.

1. *hero.script* dosyasını açın ve aşağıdaki işlevleri mevcut `update()` işlevinden _önce_ ekleyin:

```lua
    -- hero.script
    local function play_animation(self, anim)
        -- only play animations which are not already playing
        if self.anim ~= anim then
            -- tell the spine model to play the animation
            local anim_props = { blend_duration = 0.15 }
            spine.play_anim("#spinemodel", anim, go.PLAYBACK_LOOP_FORWARD, anim_props)
            -- remember which animation is playing
            self.anim = anim
        end
    end

    local function update_animation(self)
        -- make sure the right animation is playing
        if self.ground_contact then
            play_animation(self, hash("run"))
        else
            play_animation(self, hash("jump"))

        end
    end
```

2. `update()` işlevini bulup bir `update_animation` çağrısı ekleyin:

```lua
    ...
    -- apply it to the player character
    go.set_position(go.get_position() + self.velocity * dt)

    update_animation(self)
    ...
  ```

![Kahraman kodunu ekleme](images/runner/insert_hero_code.png)

::: sidenote
Lua'da yerel değişkenler için "sözcüksel kapsam" (lexical scope) vardır ve `local` işlevleri yerleştirdiğiniz sıra önemlidir. `update()` işlevi, yerel `update_animation()` ve `play_animation()` işlevlerini çağırır; yani çalışma zamanı ortamının bu yerel işlevleri çağırabilmesi için onları önceden görmüş olması gerekir. Bu yüzden işlevleri `update()` işlevinden önce koymalıyız. İşlevlerin sırasını değiştirirseniz hata alırsınız. Bunun yalnızca `local` değişkenler için geçerli olduğunu unutmayın. Lua'nın kapsam kuralları ve yerel işlevler hakkında daha fazla bilgiyi http://www.lua.org/pil/6.2.html adresinde bulabilirsiniz
:::

Kahramana zıplama ve düşme animasyonları eklemek için gerekenlerin hepsi bu kadar. Oyunu çalıştırırsanız oynamanın çok daha iyi hissettirdiğini fark edeceksiniz. Ne yazık ki platformların kahramanı ekranın dışına itebildiğini de fark edebilirsiniz. Bu, çarpışmaların ele alınışının bir yan etkisidir; ancak çözümü kolaydır: biraz şiddet ekleyip platformların kenarlarını tehlikeli hale getirin!

1. Varlık paketindeki *spikes.png* dosyasını *Assets* bölmesindeki "level/images" klasörüne sürükleyin.
2. *level.atlas* dosyasını açıp görüntüyü ekleyin (sağ tıklayıp <kbd>Add Images</kbd> seçeneğini seçin).
3. *platform.go* dosyasını açıp birkaç *Sprite* bileşeni ekleyin. *Image* değerini *level.atlas*, *Default Animation* değerini ise "spikes" olarak ayarlayın.
4. Dikenleri platformun kenarlarına yerleştirmek için *Move Tool* ve *Rotate Tool* araçlarını kullanın.
5. Dikenlerin platformun arkasında işlenmesini sağlamak için diken sprite bileşenlerinin *Z* konumunu -0.1 olarak ayarlayın.
6. Platformlara yeni bir *Collision Object* bileşeni ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin). *Group* özelliğini "danger" olarak ayarlayın. *Mask* değerini de "hero" yapın.
7. *Collision Object* bileşenine bir kutu şekli ekleyin (sağ tıklayıp <kbd>Add Shape</kbd> seçeneğini seçin). *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) ve *Scale Tool* araçlarını kullanarak şekli, kahraman karakter platforma yandan veya alttan çarptığında "danger" nesnesiyle çarpışacak biçimde yerleştirin.
8. Dosyayı kaydedin.

    ![Platform dikenleri](images/runner/3/danger_edges.png)

9. *hero.go* dosyasını açın, *Collision Object* bileşenini seçip *Mask* özelliğine "danger" adını ekleyin. Ardından dosyayı kaydedin.

    ![Kahraman çarpışması](images/runner/3/hero_collision.png)

10. *hero.script* dosyasını açın ve kahraman karakter bir "danger" kenarına çarptığında tepki alabilmek için `on_message()` işlevini değiştirin:

    ```lua
    -- hero.script
    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then
            self.velocity = vmath.vector3(0, 0, 0)
            self.correction = vmath.vector3()
            self.ground_contact = false
            self.anim = nil
            go.set(".", "euler.z", 0)
            go.set_position(self.position)
            msg.post("#collisionobject", "enable")

        elseif message_id == hash("contact_point_response") then
            -- check if we received a contact point message
            if message.group == hash("danger") then
                -- Die and restart
                play_animation(self, hash("death"))
                msg.post("#collisionobject", "disable")
                -- <1>
                go.animate(".", "euler.z", go.PLAYBACK_ONCE_FORWARD, 160, go.EASING_LINEAR, 0.7)
                go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
                    function()
                        msg.post("#", "reset")
                    end)
            elseif message.group == hash("geometry") then
                handle_geometry_contact(self, message.normal, message.distance)
            end
        end
    end
    ```
    1. Kahraman ölürken dönme ve düşme hareketi ekleyin. Bu çok daha iyi hale getirilebilir!

11. Nesnenin başlangıç işlemlerini yapmak için `init()` işlevini bir "reset" iletisi gönderecek şekilde değiştirin, ardından dosyayı kaydedin:

    ```lua
    -- hero.script
    function init(self)
        -- this lets us handle input in this script
        msg.post(".", "acquire_input_focus")
        -- save position
        self.position = go.get_position()
        msg.post("#", "reset")
    end
    ```

## Adım 8 - Bölümü sıfırlama

Oyunu şimdi denerseniz sıfırlama mekanizmasının çalışmadığı hemen anlaşılır. Kahraman doğru biçimde sıfırlanır; ancak sıfırlama sizi anında bir platform kenarına düşüp yeniden öldüğünüz bir duruma kolayca sokabilir. İstediğimiz, ölüm gerçekleştiğinde bütün bölümü düzgün biçimde sıfırlamaktır. Bölüm yalnızca çalışma sırasında oluşturulan bir dizi platformdan oluştuğu için, oluşturulan bütün platformları takip edip sıfırlama sırasında silmemiz yeterlidir:

1. *controller.script* dosyasını açıp oluşturulan bütün platformların tanımlayıcılarını saklayacak şekilde kodu düzenleyin:

    ```lua
    -- controller.script
    go.property("speed", 360)

    local grid = 460
    local platform_heights = { 100, 200, 350 }

    function init(self)
        msg.post("ground/controller#controller", "set_speed", { speed = self.speed })
        self.gridw = 0
        self.spawns = {} -- <1>
    end

    function update(self, dt)
        self.gridw = self.gridw + self.speed * dt

        if self.gridw >= grid then
            self.gridw = 0

            -- Maybe spawn a platform at random height
            if math.random() > 0.2 then
                local h = platform_heights[math.random(#platform_heights)]
                local f = "#platform_factory"
                if math.random() > 0.5 then
                    f = "#platform_long_factory"
                end

                local p = factory.create(f, vmath.vector3(1600, h, 0), nil, {}, vmath.vector3(0.6, 0.6, 1))
                msg.post(p, "set_speed", { speed = self.speed })
                table.insert(self.spawns, p) -- <1>
            end
        end
    end

    function on_message(self, message_id, message, sender)
        if message_id == hash("reset") then -- <2>
            -- Tell the hero to reset.
            msg.post("hero#hero", "reset")
            -- Delete all platforms
            for i,p in ipairs(self.spawns) do
                go.delete(p)
            end
            self.spawns = {}
        elseif message_id == hash("delete_spawn") then -- <3>
            for i,p in ipairs(self.spawns) do
                if p == message.id then
                    table.remove(self.spawns, i)
                    go.delete(p)
                end
            end
        end
    end
    ```
    1. Oluşturulan bütün platformları saklamak için bir tablo kullanıyoruz
    2. "reset" iletisi, tabloda saklanan bütün platformları siler
    3. "delete_spawn" iletisi, belirli bir platformu silip tablodan kaldırır

2. Dosyayı kaydedin.
3. *platform.script* dosyasını açıp en sol kenara ulaşan bir platformu yalnızca silmek yerine, bölüm denetleyicisine platformun kaldırılmasını isteyen bir ileti gönderecek şekilde değiştirin:

    ```lua
    -- platform.script
    ...
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    ...
    ```

    ![Platform kodunu ekleme](images/runner/insert_platform_code.png)

4. Dosyayı kaydedin.
5. *hero.script* dosyasını açın. Şimdi yapmamız gereken son şey, bölüme sıfırlama yapmasını söylemektir. Kahramanın sıfırlanmasını isteyen iletiyi bölüm denetleyicisinin betiğine taşıdık. Sıfırlama kontrolünü bu şekilde merkezîleştirmek mantıklıdır; çünkü örneğin daha uzun süreli bir ölüm dizisi eklememizi kolaylaştırır:

```lua
-- hero.script
...
go.animate(".", "position.y", go.PLAYBACK_ONCE_FORWARD, go.get_position().y - 200, go.EASING_INSINE, 0.5, 0.2,
    function()
        msg.post("controller#controller", "reset")
    end)
...
```

![Kahraman kodunu ekleme](images/runner/insert_hero_code_2.png)

Artık temel yeniden başlama ve ölme döngüsü hazır!

Sırada uğruna yaşayacak bir şey var: paralar!

## Adım 9 - Toplanacak paralar

Fikir, oyuncunun toplaması için bölüme paralar yerleştirmektir. İlk sorulması gereken, bunları bölüme nasıl yerleştireceğimizdir. Örneğin platform oluşturma algoritmasıyla bir şekilde uyumlu bir oluşturma düzeni geliştirebiliriz. Ancak sonunda çok daha kolay bir yaklaşım seçtik ve paraları platformların kendisinin oluşturmasını sağladık:

1. Varlık paketindeki *coin.png* görüntüsünü *Assets* bölmesindeki "level/images" klasörüne sürükleyin.
2. *level.atlas* dosyasını açıp görüntüyü ekleyin (sağ tıklayıp <kbd>Add Images</kbd> seçeneğini seçin).
3. *level* klasöründe *coin.go* adlı bir *Game Object* dosyası oluşturun (*Assets* bölmesindeki *level* klasörüne sağ tıklayıp <kbd>New ▸ Game Object File</kbd> seçeneğini seçin).
4. *coin.go* dosyasını açıp bir *Sprite* bileşeni ekleyin (*Outline* görünümünde sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin). *Image* değerini *level.atlas*, *Default Animation* değerini ise "coin" olarak ayarlayın.
5. Bir *Collision Object* ekleyin (*Outline* görünümünde sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin)
ve görüntüyü kaplayan bir *Sphere* şekli ekleyin (bileşene sağ tıklayıp <kbd>Add Shape</kbd> seçeneğini seçin).
6. Kürenin para görüntüsünü kaplamasını sağlamak için *Move Tool* (<kbd>Scene ▸ Move Tool</kbd>) ve *Scale Tool* araçlarını kullanın.
7. Çarpışma nesnesinin *Type* değerini "Kinematic", *Group* değerini "pickup" ve *Mask* değerini "hero" olarak ayarlayın.
8. *hero.go* dosyasını açın ve *Collision Object* bileşeninin *Mask* özelliğine "pickup" ekleyin, ardından dosyayı kaydedin.
9. *coin.script* adlı yeni bir betik dosyası oluşturun (*Assets* bölmesindeki *level* klasörüne sağ tıklayıp <kbd>New ▸ Script File</kbd> seçeneğini seçin). Şablon kodunu aşağıdakiyle değiştirin:

    ```lua
    -- coin.script
    function init(self)
        self.collected = false
    end

    function on_message(self, message_id, message, sender)
        if self.collected == false and message_id == hash("collision_response") then
            self.collected = true
            msg.post("#sprite", "disable")
        elseif message_id == hash("start_animation") then
            pos = go.get_position()
            go.animate(go.get_id(), "position.y", go.PLAYBACK_LOOP_PINGPONG, pos.y + 24, go.EASING_INOUTSINE, 0.75, message.delay)
        end
    end
    ```

10. Betik dosyasını para nesnesine bir *Script* bileşeni olarak ekleyin (*Outline* görünümündeki köke sağ tıklayıp <kbd>Add Component from File</kbd> seçeneğini seçin).

    ![Para oyun nesnesi](images/runner/3/coin.png)

Plan, paraları platform nesnelerinden oluşturmaktır; bu yüzden *platform.go* ve *platform_long.go* dosyalarına paralar için fabrikalar yerleştirin.

1. *platform.go* dosyasını açıp bir *Factory* bileşeni ekleyin (*Outline* görünümünde sağ tıklayıp <kbd>Add Component</kbd> seçeneğini seçin).
2. *Factory* bileşeninin *Id* değerini "coin_factory", *Prototype* değerini ise *coin.go* dosyası olarak ayarlayın.
3. Şimdi *platform_long.go* dosyasını açıp aynı özelliklere sahip bir *Factory* bileşeni oluşturun.
4. Her iki dosyayı kaydedin.

![Para fabrikası](images/runner/3/coin_factory.png)

Şimdi *platform.script* dosyasını, paraları oluşturup silecek şekilde değiştirmemiz gerekir:

```lua
-- platform.script
function init(self)
    self.speed = 540     -- Default speed in pixels/s
    self.coins = {}
end

function final(self)
    for i,p in ipairs(self.coins) do
        go.delete(p)
    end
end

function update(self, dt)
    local pos = go.get_position()
    if pos.x < -500 then
        msg.post("/level/controller#controller", "delete_spawn", { id = go.get_id() })
    end
    pos.x = pos.x - self.speed * dt
    go.set_position(pos)
end

function create_coins(self, params)
    local spacing = 56
    local pos = go.get_position()
    local x = pos.x - params.coins * (spacing*0.5) - 24
    for i = 1, params.coins do
        local coin = factory.create("#coin_factory", vmath.vector3(x + i * spacing , pos.y + 64, 1))
        msg.post(coin, "set_parent", { parent_id = go.get_id() }) -- <1>
        msg.post(coin, "start_animation", { delay = i/10 }) -- <2>
        table.insert(self.coins, coin)
    end
end

function on_message(self, message_id, message, sender)
    if message_id == hash("set_speed") then
        self.speed = message.speed
    elseif message_id == hash("create_coins") then
        create_coins(self, message)
    end
end
```
1. Oluşturulan paranın üst nesnesini (parent) platform olarak ayarlarsanız para platformla birlikte hareket eder.
2. Animasyon, paraların artık üst nesneleri olan platforma göre yukarı aşağı dans etmesini sağlar.

::: sidenote
Üst-alt nesne ilişkileri yalnızca _sahne grafını_ (scene graph) değiştirir. Alt nesne (child), üst nesnesiyle birlikte dönüşüme uğrar (taşınır, ölçeklenir veya döndürülür). Oyun nesneleri arasında ek "sahiplik" ilişkilerine ihtiyacınız varsa bunları kodda ayrıca takip etmeniz gerekir.
:::

Bu öğreticinin son adımı, *controller.script* dosyasına birkaç satır eklemektir:

```lua
-- controller.script
...
local platform_heights = { 100, 200, 350 }
local coins = 3 -- <1>
...
```
1. Normal bir platformda oluşturulacak para sayısı.

```lua
-- controller.script
...
local coins = coins
if math.random() > 0.5 then
    f = "#platform_long_factory"
    coins = coins * 2 -- Twice the number of coins on long platforms
end
...
```

```lua
-- controller.script
...
msg.post(p, "set_speed", { speed = self.speed })
msg.post(p, "create_coins", { coins = coins })
table.insert(self.spawns, p)
...
```

![Denetleyici kodunu ekleme](images/runner/insert_controller_code.png)

Artık basit ama işlevsel bir oyunumuz var! Buraya kadar geldiyseniz kendi başınıza devam edip şunları eklemek isteyebilirsiniz:

1. Puan ve can sayaçları
2. Nesne toplama ve ölüm için parçacık efektleri
3. Güzel arka plan görüntüleri

> Projenin tamamlanmış sürümünü [buradan](images/runner/sample-runner.zip) indirin

Bu giriş öğreticisi burada sona eriyor. Şimdi Defold'u keşfetmeye devam edin. Size yol göstermek için hazırladığımız pek çok [kılavuz ve öğretici](//www.defold.com/learn) var; takılırsanız [foruma](//forum.defold.com) bekleriz.

Defold ile iyi çalışmalar!
