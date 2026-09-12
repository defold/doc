---
title: Yerel kod eklentileri - En iyi uygulamalar
brief: Bu kılavuz, yerel kod eklentileri geliştirirken izlenebilecek en iyi uygulamaları açıklar.
---

# En iyi uygulamalar

Birden çok platformda çalışan kod yazmak zor olabilir, ancak bu tür kodları hem geliştirmeyi hem de bakımını yapmayı kolaylaştırmanın bazı yolları vardır.


## Proje yapısı

Bir yerel kod eklentisi (native extension) oluştururken, hem geliştirme hem de bakım sürecinde yardımcı olan birkaç nokta vardır.

### Lua API

Yalnızca bir Lua API'si ve bunun tek bir uygulaması olmalıdır. Bu, tüm platformlarda aynı davranışı sağlamayı çok daha kolaylaştırır.

Söz konusu platform eklentiyi desteklememeliyse, Lua modülünü hiç kaydetmemeniz önerilir. Böylece `nil` kontrolü yaparak desteği saptayabilirsiniz:

```lua
    if myextension ~= nil then
        myextension.do_something()
    end
```

### Klasör yapısı

Eklentiler için aşağıdaki klasör yapısı sıkça kullanılır:

```
    /root
        /input
        /main                            -- All the files for the actual example project
            /...
        /myextension                     -- The actual root folder of the extension
            ext.manifest
            /include                     -- External includes, used by other extensions
            /libs
                /<platform>              -- External libraries for all supported platforms
            /src
                myextension.cpp          -- The extension Lua api and the extension life cycle functions
                                            Also contains generic implementations of your Lua api functions.
                myextension_private.h    -- Your internal api that each platform will implement (I.e. `myextension_Init` etc)
                myextension.mm           -- If native calls are needed for iOS/macOS. Implements `myextension_Init` etc for iOS/macOS
                myextension_android.cpp  -- If JNI calls are needed for Android. Implements `myextension_Init` etc for Android
                /java
                    /<platform>          -- Any java files needed for Android
            /res                         -- Any resources needed for a platform
            /external
                README.md                -- Notes/scripts on how to build or package any external libraries
        /bundleres                       -- Resources that should be bundles for (see game.project and the [bundle_resources setting]([physics scale setting](/manuals/project-settings/#project))
            /<platform>
        game.project
        game.appmanifest                 -- Any extra app configuration info
```

`myextension.mm` ve `myextension_android.cpp` dosyalarının yalnızca ilgili platforma özgü yerel kod çağrıları yapıyorsanız gerekli olduğunu unutmayın.

#### Platform klasörleri

Belirli yerlerde, uygulamanın kodunu derlerken veya uygulamayı paketlerken hangi dosyaların kullanılacağını belirlemek için platform mimarisi klasör adı olarak kullanılır. Bu adlar şu biçimdedir:

    <architecture>-<platform>

Güncel liste şöyledir:

    arm64-ios, arm64_sim-ios, arm64-android, armv7-android, x86_64-android, x86_64-linux, x86_64-osx, x86_64-win32, x86-win32

Örneğin, platforma özgü kütüphaneleri şu klasörlerin altına yerleştirin:

    /libs
        /arm64-ios
                            /libFoo.a
        /arm64-android
                            /libFoo.a


## Yerel kod yazma

Defold kaynak kodunda C++ çok sınırlı kullanılır ve kodun büyük bölümü C'ye çok benzer. Birkaç kapsayıcı sınıf dışında neredeyse hiç şablon (template) kullanılmaz; çünkü şablonlar hem kod derleme sürelerini hem de yürütülebilir dosya boyutunu artırır.

### C++ sürümü

Çekirdek motoru derlerken C++11 kullanıyoruz, ancak Windows'ta C++14 kullanıyoruz. Konsol derlemeleri artık genellikle C++14 veya üzerini gerektiriyor.

Yerel kod eklentileri için sabitlenmiş bir C++ sürümü kullanmıyoruz; platformun araç zincirinin varsayılan sürümüne dayanıyoruz.

Defold kaynak kodunda C++ dilinin en yeni özelliklerini veya sürümlerini kullanmaktan kaçınılır. Bunun temel nedeni, bir oyun motoru geliştirirken yeni özelliklere ihtiyaç duyulmamasıdır. Ayrıca C++ dilinin en yeni özelliklerini takip etmek zaman alan bir iştir ve bu özelliklere tam olarak hâkim olmak çok fazla değerli zaman gerektirir.

Bunun eklenti geliştiricileri için ek bir yararı da Defold'un kararlı bir ABI sağlamasıdır. Ayrıca en yeni C++ özelliklerini kullanmanın, destek düzeylerinin değişmesi nedeniyle kodun farklı platformlarda derlenmesini engelleyebileceğini de belirtmek gerekir.

### C++ özel durumları kullanılmaz

Defold, motorda hiçbir özel durum (exception) kullanmaz. Oyun motorlarında özel durumlardan genellikle kaçınılır; çünkü veriler (çoğunlukla) geliştirme sırasında önceden bilinir. C++ özel durum desteğini kaldırmak, yürütülebilir dosya boyutunu küçültür ve çalışma zamanı performansını iyileştirir.

### Standart şablon kütüphaneleri - STL

Defold motoru bazı algoritmalar ve matematik işlemleri (`std::sort`, `std::upper_bound` vb.) dışında STL kodu kullanmadığından, eklentinizde STL kullanmak sizin için işe yarayabilir.

Yine de eklentinizi diğer eklentiler veya üçüncü taraf kütüphanelerle birlikte kullanırken ABI uyumsuzluklarının size engel olabileceğini unutmayın.

Yoğun biçimde şablon kullanan STL kütüphanelerinden kaçınmak, derleme sürelerimizi de kısaltır ve daha da önemlisi yürütülebilir dosya boyutunu küçültür.

#### Dizeler

Defold motorunda `std::string` yerine `const char*` kullanılır. Farklı C++ sürümlerini veya derleyici sürümlerini bir arada kullanırken `std::string` kullanımı sık karşılaşılan bir tuzaktır; çünkü ABI uyumsuzluğuna yol açabilir. `const char*` ve birkaç yardımcı işlev kullanmak bunu önler.

### İşlevleri gizleyin

Mümkünse yalnızca kendi derleme birimi içinde kullanılan işlevlerde `static` anahtar sözcüğünü kullanın. Bu, derleyicinin bazı optimizasyonlar yapmasını sağlar ve hem performansı iyileştirebilir hem de yürütülebilir dosya boyutunu küçültebilir.

## Üçüncü taraf kütüphaneler

Kullanılacak bir üçüncü taraf kütüphanesi seçerken (dilinden bağımsız olarak) aşağıdakileri göz önünde bulundurun:

* İşlevsellik - Yaşadığınız belirli sorunu çözüyor mu?
* Performans - Çalışma sırasında performans maliyeti oluşturuyor mu?
* Kütüphane boyutu - Son yürütülebilir dosya ne kadar büyüyecek? Bu kabul edilebilir mi?
* Bağımlılıklar - Ek kütüphaneler gerektiriyor mu?
* Destek - Kütüphane ne durumda? Çok sayıda açık sorunu var mı? Bakımı hâlâ yapılıyor mu?
* Lisans - Bu projede kullanılmasına izin veriliyor mu?


## Açık kaynak bağımlılıkları

Bağımlılıklarınıza erişiminiz olduğundan her zaman emin olun. Örneğin, GitHub'daki bir projeye bağımlıysanız, o deponun kaldırılmasını, aniden yön değiştirmesini veya el değiştirmesini engelleyen bir şey yoktur. Depoyu çatallayıp (fork) asıl proje yerine kendi çatalınızı kullanarak bu riski azaltabilirsiniz.

Kütüphanedeki kodun oyununuza ekleneceğini unutmayın; bu nedenle kütüphanenin yalnızca yapması gerekeni yaptığından emin olun!
