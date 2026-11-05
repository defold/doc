---
title: Motor hizmeti ve çalışma zamanı HTTP API'leri
brief: Bu kılavuz, çalışan bir Defold hata ayıklama motorundaki geliştirme HTTP hizmetini ve çalışma zamanı eklentilerinin veya harici araçların bu hizmeti nasıl kullanabileceğini açıklar.
---

# Motor hizmeti ve çalışma zamanı HTTP API'leri {#the-engine-service-and-runtime-http-apis}

Bir projeyi Debug modunda çalıştırmak, motorun belirli bir çalışma zamanı örneği (runtime instance) için oyununuzu ve özel bir motor hizmetini (engine service) içeren bir süreç oluşturur. Bu hizmete geliştirme ve profil çıkarma altyapısı, çalışma zamanı mantığı ve iletileri, motor durumu ve eklentiler için erişilebilir.

Motor hizmeti, çalışan bir hata ayıklama veya görüntüsüz (headless) motora (`dmengine` veya `dmengine_headless`) ait bir geliştirme HTTP hizmetidir.

Defold düzenleyicisine ait olan ve açık projeyi kontrol eden [düzenleyici sunucusundan](/manuals/editor-http-api) ayrıdır.

İki hizmet farklı bağlantı noktaları kullanır. Düzenleyicinin bağlantı noktasına bağlanan bir araç, orada çalışma zamanı eklentilerinin rotalarını çağıramaz; bunun tersi de geçerlidir - motor hizmetine bağlanan bir araç düzenleyici işlemlerini çağıramaz.

Motor hizmeti, hata ayıklama, geliştirme ve profil çıkarma altyapısının bir parçasıdır. Release motor örnekleri bu hizmeti oluşturmaz.

## Kullanılabilirlik ve bağlantı noktası keşfi {#availability-and-port-discovery}

Düzenleyici bir hata ayıklama motoru başlatırken dinamik olarak atanan bir hizmet bağlantı noktası ister. Motor, seçilen bağlantı noktasını *Console* görünümünde ve bir CLI üzerinden çalıştırıldığında günlüğünde bildirir:

![Defold hata ayıklama derlemesinde motor hizmetinin bağlantı noktası bilgisi](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Motor, gerçek adresini ve atanmış bağlantı noktasını kullanarak tam OpenAPI keşif URL adresini de günlüğe yazar:

```text
INFO:ENGINE: OpenAPI: http://<address>:<port>/openapi.json
```

Oyun düzenleyiciden başlatıldığında bu satırlar düzenleyici konsolunda görünür. Basit bir yerel denetleyici bunları ayrıştırabilir, ancak yeniden kullanılabilir bir tümleştirmede motor örneğini ve kayıtlı bağlantı noktasını düzenleyicinin veya onun sarmalayıcısının takip etmesi önerilir. Bu, eski bir bağlantı noktasının yeni başlatılmış veya yeniden kullanılan bir süreçle karıştırılmasını önler.

Motor, desteklenen platformlarda hizmet keşfi (service discovery) aracılığıyla geliştirme hedeflerini de duyurur. Bu mekanizma öncelikle Defold araçları tarafından kullanılır; bunun yerine koda kalıcı olarak sabitlenmiş bir bağlantı noktası kullanılması önerilmez.

Sunucuya yerel makinede, localhost (`127.0.0.1`) adresinde belirli bir bağlantı noktası üzerinden erişilebilir:

![Motor sunucusuna erişim](images/automation/engine-server.png)

## OpenAPI aracılığıyla işlemleri keşfetme {#discovering-operations-through-openapi}

`GET /openapi.json`, çalışma zamanı HTTP API'sini açıklayan bir OpenAPI 3.0.3 belgesi döndürür. Günlükteki motor hizmeti bağlantı noktasını kullanın. Yerel bir motor için aşağıdaki `<port>` yer tutucusunu bu bağlantı noktasıyla değiştirin:

```sh
ENGINE_URL="http://127.0.0.1:<port>"
curl -fsS "$ENGINE_URL/openapi.json" | jq
```

Belge, OpenAPI üst verisi sağlayan yerel kod eklentileri dahil, o anda kayıtlı işleyicilerin sağladığı yolları, yöntemleri, parametreleri, istek gövdelerini ve yanıtları açıklar. İşleyiciler eklendiğinde veya kaldırıldığında belgenin `paths` nesnesi değişir. Profil çıkarıcı ve eklenti rotaları, çalışan motorun platformuna, yapılandırmasına ve kayıtlı eklentilerine bağlıdır; bu nedenle belgeyi kullandığınız örnekten alın.

OpenAPI üst verisi olmadan kaydedilen işleyiciler çağrılabilir, ancak belgede görünmez. Belgelenmiş bir rota da bir yeteneğin kullanılamadığını bildirebilir; platforma bağlı işlemleri kullanmadan önce yanıt açıklamalarını ve varsa yetenek uç noktasını inceleyin.

Düzenleyicinin kendi bağlantı noktasında ayrı bir [OpenAPI belgesi](/manuals/editor-http-api/#discovering-operations-through-openapi) bulunur. Çalışma zamanı işlemleri için motorun belgesini kullanın.

## Yerleşik uç noktalar {#built-in-endpoints}

Mevcut hata ayıklama motoru az sayıda temel rota kaydeder.

| Uç nokta | Amaç |
| --- | --- |
| `GET /openapi.json` | OpenAPI üst verisi sağlayan, o anda kayıtlı çalışma zamanı HTTP işlemlerini keşfetmek |
| `GET /ping` | Motor hizmetinin yanıt verdiğini kontrol etmek |
| `GET /info` | Motor sürümünü, platformu, derleme tanımlayıcısını ve günlük hizmeti bilgilerini okumak |
| `GET /state` | Defold araçlarının kullandığı geliştirme bağlantısı durumunu okumak |
| `POST /post/<socket>/<message-type>` | Adlandırılmış bir motor soketine Protobuf ile kodlanmış bir Defold iletisi göndermek |

Örneğin:

```sh
curl -sS "$ENGINE_URL/ping"
curl -sS "$ENGINE_URL/info" | jq
curl -sS "$ENGINE_URL/state" | jq
```

`/post` rotası çalışma sırasında yeniden yükleme (hot reload), yeniden başlatma, yeniden boyutlandırma ve süreç kontrolü gibi geliştirme işlemleri tarafından kullanılır. Gövdesi, rotada adı belirtilen türde bir ikili Protobuf iletisidir; bu bir JSON ileti API'si değildir. Protobuf iletisinin serileştirilmiş hâli 1024 bayttan büyük olamaz; aksi takdirde `400 Too large message` döndürülür.

Bu rotalar geliştirme altyapısını oluşturur; motorun kodunda ek profil çıkarıcı ve kaynak inceleme rotaları da bulunur.

## Kayıt uç noktaları {#recording-endpoints}

Masaüstü hata ayıklama motorları, aşağıdaki rotalar üzerinden yerel MP4 kaydı da sunar. Bu rotalar yayıma yönelik, görüntüsüz, mobil ve web derlemelerinde ve [Uygulama bildiriminde](/manuals/app-manifest/#exclude-record) **Exclude Record** etkin olduğunda bulunmaz.

| Uç nokta | Amaç |
| --- | --- |
| `GET /recording/capabilities` | Video/ses desteğini, arka uç gereksinimlerini ve kayıt hizmetinin `instance_id` değerini keşfetmek |
| `GET /recording/status` | Geçerli işlemi, eşzamansız ilerlemeyi ve sonlandırılmış dosya bilgilerini okumak |
| `POST /recording/start` | Kayıt istemek ve kaydın `operation_id` değerini almak |
| `POST /recording/stop` | Belirtilen işlem için durdurma ve sonlandırma istemek |
| `GET /recording/files/{id}` | Sonlandırılmış bir MP4 dosyasını indirmek |
| `DELETE /recording/files/{id}` | Hizmetin sakladığı tamamlanmış bir dosyayı silmek |

Bu rotaları `/openapi.json` üzerinden keşfedin, ardından geçerli platformun desteğini öğrenmek için `/recording/capabilities` sonucunu kontrol edin. Kaydı değiştiren işlemler `X-Recording-Instance` üstbilgisini gerektirir; durdurma işlemi ayrıca kabul edilen `operation_id` değerini de gerektirir. Başlatma ve durdurma eşzamansızdır; dosyayı indirmeden önce sonlandırmayı bekleyin. İş akışının tamamı için [kayıt kılavuzuna](/manuals/recording/#recording-through-http) bakın.

HTTP hizmeti kaydediciyi Lua ile paylaşır. HTTP üzerinden başlatma, desteklendiğinde uygulama sesini varsayılan olarak etkinleştirir; Lua üzerinden başlatma varsayılan olarak yalnızca video kaydeder. Yalnızca HTTP üzerinden başlatılan kayıtlar, indirilebilir dosyayı tanımlayan bir `file` kaydına sahiptir. İndirmeden önce `pending: false`, `finalized: true` ve `file.state: "complete"` olmasını bekleyin, ardından [dosyanın boyutunu ve SHA-256 değerini doğrulayın](/manuals/recording/#download-and-release-the-file). Lua ve HTTP istemcilerini birlikte kullanırken [kaydediciyi paylaşma](/manuals/recording/#sharing-the-recorder-with-http-clients) bölümüne bakın.

## Metal GPU izleme uç noktası {#metal-gpu-trace-endpoint}

macOS'ta hata ayıklama motorları, Metal GPU izlerini yakalamak için `/profiler/gputrace` yolunu sunar. Bu rota `/openapi.json` içinde yalnızca macOS'ta görünür. Yakalama, yerel Metal bağdaştırıcısını ve motorun başlatma ortamında `METAL_CAPTURE_ENABLED=1` değerini gerektirir. Yakalama kullanılamıyorsa istek, `error.code: "gputrace_unsupported"` ile HTTP 501 döndürür.

| Uç nokta | Amaç |
| --- | --- |
| `POST /profiler/gputrace` | Yazılabilir bir mutlak `.gputrace` yoluna yakalama zamanlamak; `frames` varsayılan olarak `1` değerindedir ve `1`–`10000` arasında olabilir. |
| `GET /profiler/gputrace` | Geçerli veya en son yakalamanın durumunu, yolunu ve kare sayılarını okumak. |
| `DELETE /profiler/gputrace` | Bekleyen yakalamayı iptal etmek veya etkin yakalamayı işlenen geçerli kareden sonra bitirmek; izi diskte tutmak. |

Kabul edilen istekler `ok: true` ve bir `data` nesnesiyle HTTP 200 döndürür. Yakalama eşzamansız ilerler: `data.state` değeri `complete`, `canceled` veya `failed` olana kadar `GET` ile sorgulayın. Yerel başlatma hataları `data.error` içinde bildirilir. İz, motorun çalıştığı makineye yazılır. Başlatma komutları, destek keşfi, yakalama örnekleri ve sonucu Xcode'da açma hakkında bilgi için [Metal GPU izi yakalama kılavuzuna](/manuals/profiling/#metal-gpu-trace-capture) bakın.

## Eklentilerin tanımladığı çalışma zamanı rotaları {#extension-defined-runtime-routes}

Hata ayıklama derlemelerinde, yerel kod eklentisi (native extension) SDK'sı motorun web sunucusuna erişim sağlayabilir. Bir eklenti bu sunucuda bir rota öneki kaydedebilir ve çalışma zamanı verilerine bağlı işlemler sunabilir.

Bu, geliştirme araçları için yararlıdır; çünkü bir eklenti başka bir HTTP sunucusu açmak yerine mevcut motor hizmetini paylaşabilir.

Bir eklentinin tanımladığı çalışma zamanı otomasyon API'sinin şunları yapması önerilir:

* ayrı, sürümlendirilmiş bir rota öneki kullanmak;
* desteklenen yetenekleri sunmak;
* yapılandırılmış hatalar döndürmek;
* kullanılamayan platform veya motor özelliklerini açıkça ele almak;
* işlemleri yerel geliştirme ve test ortamlarıyla sınırlamak;
* yayıma yönelik derlemelerden çıkarılıp çıkarılmadığını belgelemek.

### Eklenti işlemlerini OpenAPI'de yayımlama {#publishing-extension-operations-in-openapi}

Yerel kod eklentisinin uygulama başlangıç geri çağırımında `dmEngine::GetWebServer(app_params)` ile sunucuyu alın ve yalnızca döndürülen tanıtıcı null değilse işleyicileri kaydedin. Geri çağırım kurulumu için [eklenti yaşam döngüsüne](/manuals/extensions/#extension-lifecycle) bakın.

Dört bağımsız değişkenli `dmWebServer::AddHandler()` aşırı yüklemesi, JSON dizesi olarak bir OpenAPI 3.0.3 Paths Object kabul eder. Nesnenin en üst düzey anahtarları rota yollarıdır. Her yol kayıtlı önekle başlamalı ve başka bir işleyici tarafından önceden belgelenmemiş olmalıdır. Satır içi şemalar veya ortaya çıkan belgedeki yollara başvurular kullanın.

Örneğin bu yardımcı işlev bir geri çağırımı ve durum uç noktasının açıklamasını kaydeder:

```cpp
#include <dmsdk/dlib/webserver.h>

static const char STATUS_OPENAPI[] = R"json(
{
  "/example/v1/status": {
    "get": {
      "summary": "Get extension status",
      "responses": {
        "200": {
          "description": "Current extension status",
          "content": {
            "text/plain": {
              "schema": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
)json";

dmWebServer::Result RegisterStatusHandler(dmWebServer::HServer server,
                                        dmWebServer::Handler callback,
                                        void* context)
{
    dmWebServer::HandlerParams params;
    params.m_Handler = callback;
    params.m_Userdata = context;
    return dmWebServer::AddHandler(
        server, "/example/v1", &params, STATUS_OPENAPI);
}
```

`GET /example/v1/status` işlemini uygulayan ve belgelenen `text/plain` yanıtını döndüren bir geri çağırım verin. İstek yollarını ve yöntemlerini kontrol etmek ve yanıtları üretmek geri çağırımın sorumluluğunda kalır. Kayıt sonucunu kontrol edin: geçersiz veya çakışan üst veriler `dmWebServer::RESULT_ERROR_INVAL` döndürür.

Sunucu, dizeyi kopyalamadan JSON işaretçisini saklar. İşleyici `dmWebServer::RemoveHandler()` ile kaldırılana veya sunucu yok edilene kadar işaret edilen depolama alanını değişmeden ve geçerli tutun. Örnekteki `static const char` dizisi bu gereksinimi karşılar. İşleyiciyi kaldırmak, sonraki `/openapi.json` yanıtlarından onun yollarını da kaldırır.

Üç bağımsız değişkenli `dmWebServer::AddHandler(server, prefix, &params)` aşırı yüklemesi desteklenmeye devam eder. Bu, dördüncü bağımsız değişken olarak `0` vermeye eşdeğerdir: işleyici OpenAPI üst verisi olmadan kaydedilir ve keşifte gösterilmez.

## Automation Bridge eklentisi {#automation-bridge-extension}

Resmî Defold [Automation Bridge](https://github.com/defold/extension-automation-bridge) eklentisi, motor hizmeti üzerine kurulmuş ve yalnızca hata ayıklama derlemelerinde kullanılan bir yerel kod eklentisidir. Şu adres altında sürümlendirilmiş bir çalışma zamanı otomasyon API'si kaydeder:

```text
http://127.0.0.1:<engine-service-port>/automation-bridge/v1
```

Çalışma zamanı API'si sahne ve düğüm inceleme, girdi, ekran bilgisi, ekran görüntüleri, kayıt, yaşam döngüsü bilgisi ve isteğe bağlı olarak uygulamanın tanımladığı eşzamanlama gibi yetenekler sağlar. Bazı işlemler şunlardır:

| İşlem | Eylem |
| --- | --- |
| `GET  /automation-bridge/v1/health` | sağlık raporu, API yetenekleri ve uyumluluk |
| `POST /automation-bridge/v1/input/click` | çalışma sırasındaki girdi etkileşimleri için |
| `GET  /automation-bridge/v1/screenshot` | çalışma sırasında ekran görüntüleri almak için |

Eklentinin projede kurulu sürümüne ait [yerel API belgelerini](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge) ve [Python yardımcı araçları belgelerini](https://github.com/defold/extension-automation-bridge/tree/master/automation_bridge/automation-bridge-python) kullanın.

Automation Bridge, yayıma yönelik derlemelerde ne HTTP API'sini ne de Lua modülünü sunar.

### Düzenleyici ve çalışma zamanı istemcileri {#editor-and-runtime-clients}

Automation Bridge Python yardımcı araçları, iki istemcili mimariyi gösterir. `editor.open_project()` işlevi bir düzenleyici proje istemcisi, `project.build_and_run()` ise ayrı bir motor istemcisi döndürür.

| İstemci | Amaç |
| --- | --- |
| Proje | Düzenleyici HTTP API'si, komutlar, hata ayıklayıcı, konsol, tercihler, başvuru belgeleri, önizlemeler, proje derleme ve bağlantı noktası keşfi |
| Oyun - motor hizmeti | Sahne, girdi, ekran görüntüleri, çalışma zamanı durumu ve eşzamanlama |

`project` ve `game` arasındaki ayrım, süreç sınırını açıkça ortaya koyar. Düzenleyici işlemleri düzenleyici sunucusunda kalırken çalışan oyuna yönelik gözlemler ve eylemler motor hizmetinde kalır.

```python
from automation_bridge import editor

project = editor.open_project(".")
game = project.build_and_run()
```

## Sınırlamalar ve güvenlik {#limitations-and-security}

Motor hizmeti ve eklentilerin tanımladığı rotalar geliştirme araçlarıdır ve buna uygun şekilde ele alınmaları önerilir.

::: important
Defold 1.14.1 ve sonraki sürümlerde keşif için çalışan motorun `/openapi.json` belgesini kullanın. Önceki motorlar bu uç noktayı sağlamaz. OpenAPI üst verisi olmadan kaydedilmiş işleyiciler için eklentinin sürümlendirilmiş API belgelerine başvurun.
:::

Çalışma zamanı betikleri, fizik, girdi, dinamik olarak oluşturulan nesneler ve platforma özgü işleme, çalışan bir motor gerektirir ve [otomatik çalışma zamanı testleri](/manuals/automated-testing) aracılığıyla doğrulanmaları önerilir.

* Hizmeti bir yönlendirici, genel erişime açık bir arayüz veya güvenilmeyen bir tünel üzerinden yayımlamayın.
* Motor hizmeti rotalarının kimlik doğrulama gerektirdiğini varsaymayın.
* Çalışma zamanı rotaları, eklenti sürümüne, platforma, grafik arka ucuna ve motor yeteneklerine göre değişebilir.
* Eklentilerin tanımladığı güncel API'ler için sürüm veya yetenek uzlaşması kullanın.
