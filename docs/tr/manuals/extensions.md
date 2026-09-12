---
title: Defold için yerel kod eklentileri yazma
brief: Bu kılavuz, Defold oyun motoru için yerel kod eklentisi yazmayı ve kurulum gerektirmeyen bulut derleme araçlarıyla eklentinin kodunu derlemeyi açıklar.
---

# Yerel kod eklentileri

Lua'nın yeterli olmadığı durumlarda harici yazılım veya donanımla düşük düzeyde özel bir etkileşim kurmanız gerekiyorsa Defold SDK, hedef platforma bağlı olarak motor için C, C++, C#, Objective-C, Java veya JavaScript ile eklentiler yazmanıza olanak tanır. Yerel kod eklentilerinin (native extension) yaygın kullanım alanları şunlardır:

- Belirli donanımlarla, örneğin cep telefonlarının kamerasıyla etkileşim.
- Harici düşük düzeyli API'lerle, örneğin Luasocket kullanılabilecek ağ API'leri üzerinden etkileşime izin vermeyen reklam ağı API'leriyle etkileşim.
- Yüksek performanslı hesaplamalar ve veri işleme.

::: sidenote
C# desteği deneyseldir ve Defold betik bileşenleri (script component) için değil, yerel kod eklentileri için tasarlanmıştır. Statik bir kütüphane üretmek için .NET 9 NativeAOT kullanır; eklentinin `src` klasörüne `.cs` kaynak dosyalarını eklediğinizde derleme hizmeti proje dosyasını oluşturur. Hedef desteği, NativeAOT ve derleme hizmetinin mevcut yeteneklerine bağlıdır. Güncel iş akışı ve test edilmiş kurulum için resmî [yerel kod eklentisi dil örneğine](https://github.com/defold/example-languages) bakın.
:::

## Derleme sunucusu

Defold, bulut tabanlı bir derleme çözümüyle yerel kod eklentilerini kullanmaya kurulum gerektirmeden başlamanızı sağlar. Geliştirilip bir oyun projesine doğrudan veya bir [kütüphane projesi](/manuals/libraries/) aracılığıyla eklenen her yerel kod eklentisi, olağan proje içeriğinin bir parçası olur. Motorun özel sürümlerini derleyip ekip üyelerine dağıtmanız gerekmez; bu işlem otomatik olarak yapılır---projeyi derleyip çalıştıran her ekip üyesi, motorun tüm yerel kod eklentilerini içeren, projeye özgü yürütülebilir dosyasını alır.

![Bulutta derleme](images/extensions/cloud_build.png)

Defold, bulut derleme sunucusunu herhangi bir kullanım kısıtlaması olmadan ücretsiz sunar. Sunucu Avrupa'da barındırılır ve yerel kodun gönderildiği URL, [düzenleyici tercihleri penceresinde](/manuals/editor-preferences/#extensions) veya [bob](/manuals/bob/#usage) aracının `--build-server` komut satırı seçeneğiyle yapılandırılır. Kendi sunucunuzu kurmak istiyorsanız lütfen [bu yönergeleri izleyin](/manuals/extender-local-setup).

## Proje düzeni

Yeni bir eklenti oluşturmak için projenin kök dizininde bir klasör oluşturun. Bu klasör, eklentiyle ilişkili tüm ayarları, kaynak kodu, kütüphaneleri ve kaynakları içerecektir. Eklenti derleme aracı klasör yapısını tanır ve tüm kaynak dosyaları ile kütüphaneleri toplar.

```
 myextension/
 │
 ├── ext.manifest
 │
 ├── src/
 │
 ├── include/
 │
 ├── lib/
 │   └──[platforms]
 │
 ├── manifests/
 │   └──[platforms]
 │
 └── res/
     └──[platforms]

```
*ext.manifest*
: Eklenti klasörü bir *ext.manifest* dosyası _içermek zorundadır_. Bu dosya, tek bir eklenti derlenirken kullanılan bayrakları ve tanımları içeren bir yapılandırma dosyasıdır. Dosya biçiminin tanımını [Eklenti bildirimi kılavuzunda](https://defold.com/manuals/extensions-ext-manifests/) bulabilirsiniz.

*src*
: Bu klasörün tüm kaynak kod dosyalarını içermesi önerilir.

*include*
: Bu isteğe bağlı klasör, dahil etme (include) dosyalarını içerir.

*lib*
: Bu isteğe bağlı klasör, eklentinin bağımlı olduğu derlenmiş kütüphaneleri içerir. Kütüphane dosyalarının, kütüphanelerinizin desteklediği mimarilere bağlı olarak `platform` veya `architecture-platform` biçiminde adlandırılan alt klasörlere yerleştirilmesi önerilir.

  :[platforms](../shared/platforms.md)

*manifests*
: Bu isteğe bağlı klasör, derleme veya paketleme sürecinde kullanılan ek dosyaları içerir. Ayrıntılar için aşağıya bakın.

*res*
: Bu isteğe bağlı klasör, eklentinin bağımlı olduğu ek kaynakları içerir. Kaynak dosyalarının, `lib` alt klasörlerinde olduğu gibi `platform` veya `architecture-platform` biçiminde adlandırılan alt klasörlere yerleştirilmesi önerilir. Tüm platformlar için ortak kaynak dosyaları içeren `common` adlı bir alt klasöre de izin verilir.

### Bildirim dosyaları

Bir eklentinin isteğe bağlı *manifests* klasörü, derleme ve paketleme sürecinde kullanılan ek dosyaları içerir. Dosyaların `platform` biçiminde adlandırılan alt klasörlere yerleştirilmesi önerilir:

* `android` - Bu klasör, ana uygulamayla birleştirilecek bir bildirim parçası dosyası kabul eder ([burada açıklandığı gibi](/manuals/extensions-manifest-merge-tool)).
  * Klasör, [Gradle tarafından çözümlenecek](/manuals/extensions-gradle) bağımlılıkları içeren bir `build.gradle` dosyası da içerebilir.
  * Java kodu içeren eklentilerin, çalışma sırasında ihtiyaç duydukları sınıflar için bir [R8 koruma kuralı dosyası](#r8-keep-rules-for-android) (`.keep`) içermesi önerilir.
* `ios` - Bu klasör, ana uygulamayla birleştirilecek bir bildirim parçası dosyası kabul eder ([burada açıklandığı gibi](/manuals/extensions-manifest-merge-tool)).
  * Klasör, [Cocoapods tarafından çözümlenecek](/manuals/extensions-cocoapods) bağımlılıkları içeren bir `Podfile` dosyası da içerebilir.
* `osx` - Bu klasör, ana uygulamayla birleştirilecek bir bildirim parçası dosyası kabul eder ([burada açıklandığı gibi](/manuals/extensions-manifest-merge-tool)).
* `web` - Bu klasör, ana uygulamayla birleştirilecek bir bildirim parçası dosyası kabul eder ([burada açıklandığı gibi](/manuals/extensions-manifest-merge-tool)).


### Android için R8 koruma kuralları {#r8-keep-rules-for-android}

Eklentinin `manifests/android` dizinine, `build.gradle` dosyasının yanına bir `.keep` dosyası ekleyin. Örneğin `/myextension/manifests/android/myextension.keep`, aşağıdaki kuralla eklentinin Java sınıflarını koruyabilir:

```proguard
-keep,allowoptimization class com.example.myextension.** { *; }
```

`com.example.myextension` yerine eklentinizin Java sınıflarını içeren paketi yazın. Bu kural, R8'in kodlarını optimize etmesine izin verirken sınıfları ve üyelerini korur. R8 bu kullanımları otomatik olarak keşfedemeyebileceğinden, Java Native Interface (JNI) veya yansıma (reflection) aracılığıyla erişilen diğer sınıflar için de kurallar ekleyin.

Eklenti çalışma sırasında ek açıklamalara (annotation) dayanıyorsa şunu da ekleyin:

```proguard
-keepattributes *Annotation*
```

Bu kurallar, [R8 etkinleştirildiğinde](/manuals/android/#enabling-r8) projenin seçilen koruma dosyasıyla birleştirilir.


## Özel kaynaklar {#custom-resources}

Bir eklenti, `ext.manifest` dosyasının yanındaki bir `ext.properties` dosyasında özel kaynaklar (custom resource) tanımlayarak oyun arşivine veri dahil edebilir:

```ini
[project]
custom_resources.default = /myextension/data
```

Örneğin `/myextension/data/settings.json` konumuna bir JSON dosyası yerleştirin. Yol, eklenti klasörünü de içerir ve projenin kök dizinine göredir. Eklentiyi kütüphane olarak paylaşırken, kütüphaneyi kullanan projelerin eklentiyi ve verilerini alması için kütüphanenin [Include Dirs](/manuals/libraries/#setting-up-library-sharing) ayarına `myextension` ekleyin.

Bu yollar, *game.project* dosyasındaki `project.custom_resources` ve diğer eklentilerin eklediği kaynaklarla birleştirilir. Projede özel kaynaklar ayarlamak, eklentilerin eklediği kaynakların yerini almaz. Hem düzenleyicide yapılan derlemeler hem de Bob arşivleri, çalışma sırasında yüklenebilen bu dosyaları içerir:

```lua
local data, err = sys.load_resource("/myextension/data/settings.json")
if data then
    local settings = json.decode(data)
    pprint(settings)
else
    print(err)
end
```

Özel kaynakların dağıtım paketine eklenen kaynaklardan nasıl farklılaştığını öğrenmek için [dosya erişimi](/manuals/file-access/#custom-resources) bölümüne bakın.

## Eklenti paylaşma

Eklentiler, projenizdeki diğer varlıklarla aynı şekilde ele alınır ve aynı şekilde paylaşılabilir. Bir yerel kod eklentisi klasörü, kütüphane klasörü olarak eklenirse paylaşılabilir ve başkaları tarafından proje bağımlılığı olarak kullanılabilir. Daha fazla bilgi için [Kütüphane projesi kılavuzuna](/manuals/libraries/) bakın.


## Basit bir eklenti örneği

Çok basit bir eklenti oluşturalım. Önce kök dizinde yeni bir *`myextension`* klasörü oluşturup eklentinin "`MyExtension`" adını içeren bir *`ext.manifest`* dosyası ekliyoruz. Adın bir C++ simgesi olduğunu ve `DM_DECLARE_EXTENSION` makrosunun ilk bağımsız değişkeniyle eşleşmesi gerektiğini unutmayın (aşağıya bakın).

![Bildirim](images/extensions/manifest.png)

```yaml
# C++ symbol in your extension
name: "MyExtension"
```

Eklenti, "`src`" klasöründe oluşturulan tek bir C++ dosyasından, *`myextension.cpp`* dosyasından oluşur.

![C++ dosyası](images/extensions/cppfile.png)

Eklentinin kaynak dosyası aşağıdaki kodu içerir:

```cpp
// myextension.cpp
// Extension lib defines
#define LIB_NAME "MyExtension"
#define MODULE_NAME "myextension"

// include the Defold SDK
#include <dmsdk/sdk.h>

static int Reverse(lua_State* L)
{
    // The number of expected items to be on the Lua stack
    // once this struct goes out of scope
    DM_LUA_STACK_CHECK(L, 1);

    // Check and get parameter string from stack
    char* str = (char*)luaL_checkstring(L, 1);

    // Reverse the string
    int len = strlen(str);
    for(int i = 0; i < len / 2; i++) {
        const char a = str[i];
        const char b = str[len - i - 1];
        str[i] = b;
        str[len - i - 1] = a;
    }

    // Put the reverse string on the stack
    lua_pushstring(L, str);

    // Return 1 item
    return 1;
}

// Functions exposed to Lua
static const luaL_reg Module_methods[] =
{
    {"reverse", Reverse},
    {0, 0}
};

static void LuaInit(lua_State* L)
{
    int top = lua_gettop(L);

    // Register lua names
    luaL_register(L, MODULE_NAME, Module_methods);

    lua_pop(L, 1);
    assert(top == lua_gettop(L));
}

dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
    // Init Lua
    LuaInit(params->m_L);
    printf("Registered %s Extension\n", MODULE_NAME);
    return dmExtension::RESULT_OK;
}

dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
    return dmExtension::RESULT_OK;
}

dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
    return dmExtension::RESULT_OK;
}


// Defold SDK uses a macro for setting up extension entry points:
//
// DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)

// MyExtension is the C++ symbol that holds all relevant extension data.
// It must match the name field in the `ext.manifest`
DM_DECLARE_EXTENSION(MyExtension, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, 0, 0, FinalizeMyExtension)
```

Eklenti kodundaki çeşitli giriş noktalarını tanımlamak için kullanılan `DM_DECLARE_EXTENSION` makrosuna dikkat edin. İlk bağımsız değişken olan `symbol`, *ext.manifest* dosyasında belirtilen adla eşleşmelidir. Bu basit örnekte `update` veya `on_event` giriş noktalarına gerek olmadığından, makroya bu konumlarda `0` verilir.

Şimdi geriye yalnızca projeyi derlemek kalıyor (<kbd>Project ▸ Build</kbd>). Bu işlem, eklentiyi eklenti derleme aracına gönderir; araç da yeni eklentiyi içeren özel bir motor üretir. Derleme aracı herhangi bir hatayla karşılaşırsa derleme hatalarını içeren bir iletişim kutusu gösterilir.

Eklentiyi test etmek için bir oyun nesnesi (game object) oluşturun ve test kodu içeren bir betik bileşeni ekleyin:

```lua
local s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local reverse_s = myextension.reverse(s)
print(reverse_s) --> ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba
```

İşte bu kadar! Tamamen çalışan bir yerel kod eklentisi oluşturduk.


## Eklentinin yaşam döngüsü

Yukarıda gördüğümüz gibi, `DM_DECLARE_EXTENSION` makrosu eklenti kodundaki çeşitli giriş noktalarını tanımlamak için kullanılır:

`DM_DECLARE_EXTENSION(symbol, name, app_init, app_final, init, update, on_event, final)`

Giriş noktaları, eklentinin yaşam döngüsünün çeşitli aşamalarında kod çalıştırmanıza olanak tanır:

* Motorun başlatılması
  * Motor sistemleri başlatılır
  * Eklentinin `app_init` giriş noktası
  * Eklentinin `init` giriş noktası - Tüm Defold API'lerinin başlangıç işlemleri tamamlanmıştır. Eklenti yaşam döngüsünde, eklenti koduna yönelik Lua bağlarının (binding) oluşturulması için önerilen aşama budur.
  * Betiğin başlangıç işlemleri - Betik dosyalarının `init()` işlevi çağrılır.
* Motor döngüsü
  * Motorun güncellenmesi
    * Eklentinin `update` giriş noktası
    * Betiğin güncellenmesi - Betik dosyalarının `update()` işlevi çağrılır.
  * Motor olayları (pencereyi küçültme/büyütme vb.)
    * Eklentinin `on_event` giriş noktası
* Motorun kapatılması (veya yeniden başlatılması)
  * Betiğin sonlandırma işlemleri - Betik dosyalarının `final()` işlevi çağrılır.
  * Eklentinin `final` giriş noktası
  * Eklentinin `app_final` giriş noktası

## Tanımlanan platform tanımlayıcıları

Aşağıdaki tanımlayıcılar, ilgili platformların her birinde derleme aracı tarafından tanımlanır:

* `DM_PLATFORM_WINDOWS`
* `DM_PLATFORM_OSX`
* `DM_PLATFORM_IOS`
* `DM_PLATFORM_ANDROID`
* `DM_PLATFORM_LINUX`
* `DM_PLATFORM_HTML5`

## Derleme sunucusu günlükleri {#build-server-logs}

Proje yerel kod eklentileri kullanıyorsa derleme sunucusu günlüklerine erişilebilir. Derleme sunucusu günlüğü (`log.txt`), proje derlenirken özel motorla birlikte indirilir ve `.internal/%platform%/build.zip` dosyasının içinde saklanır; ayrıca arşivden çıkarılarak projenizin derleme klasörüne yerleştirilir.

## Eklenti örnekleri

* [Temel eklenti örneği](https://github.com/defold/template-native-extension) (bu kılavuzdaki eklenti)
* [Android eklentisi örneği](https://github.com/defold/extension-android)
* [HTML5 eklentisi örneği](https://github.com/defold/extension-html5)
* [macOS, iOS ve Android video oynatıcı eklentisi](https://github.com/defold/extension-videoplayer)
* [macOS ve iOS kamera eklentisi](https://github.com/defold/extension-camera)
* [iOS ve Android uygulama içi satın alma eklentisi](https://github.com/defold/extension-iap)
* [iOS ve Android Firebase Analytics eklentisi](https://github.com/defold/extension-firebase-analytics)

[Defold Asset Portal](https://www.defold.com/assets/) ayrıca birden çok yerel kod eklentisi içerir.
