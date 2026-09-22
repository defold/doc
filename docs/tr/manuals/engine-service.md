---
title: Motor hizmeti ve çalışma zamanı HTTP API'leri
brief: Bu kılavuz, çalışan bir Defold hata ayıklama motorundaki geliştirme HTTP hizmetini ve çalışma zamanı eklentilerinin veya harici araçların bu hizmeti nasıl kullanabileceğini açıklar.
---

# Motor hizmeti ve çalışma zamanı HTTP API'leri

Bir projeyi Debug modunda çalıştırmak, motorun belirli bir çalışma zamanı örneği (runtime instance) için oyununuzu ve özel bir motor hizmetini (engine service) içeren bir süreç oluşturur. Bu hizmete geliştirme ve profil çıkarma altyapısı, çalışma zamanı mantığı ve iletileri, motor durumu ve eklentiler için erişilebilir.

Motor hizmeti, çalışan bir hata ayıklama motoruna (`dmengine`) ait bir geliştirme HTTP hizmetidir.

Defold düzenleyicisine ait olan ve açık projeyi kontrol eden [düzenleyici sunucusundan](/manuals/editor-http-api) ayrıdır.

İki hizmet farklı bağlantı noktaları kullanır. Düzenleyicinin bağlantı noktasına bağlanan bir araç, orada çalışma zamanı eklentilerinin rotalarını çağıramaz; bunun tersi de geçerlidir - motor hizmetine bağlanan bir araç düzenleyici işlemlerini çağıramaz.

Motor hizmeti, hata ayıklama, geliştirme ve profil çıkarma altyapısının bir parçasıdır. Release motor örnekleri bu hizmeti oluşturmaz.

## Kullanılabilirlik ve bağlantı noktası keşfi

Düzenleyici bir hata ayıklama motoru başlatırken dinamik olarak atanan bir hizmet bağlantı noktası ister. Motor, seçilen bağlantı noktasını `Console` görünümünde (`bir CLI üzerinden çalıştırılıyorsa günlüğünde de) bildirir:

![Defold hata ayıklama derlemesinde motor hizmetinin bağlantı noktası bilgisi](images/automation/engine-service.png)

```text
INFO:ENGINE: Engine service started on port <port>
```

Oyun düzenleyiciden başlatıldığında bu satır düzenleyici konsolunda görünür. Basit bir yerel denetleyici bu satırı ayrıştırabilir, ancak yeniden kullanılabilir bir tümleştirmede motor örneğini ve kayıtlı bağlantı noktasını düzenleyicinin veya onun sarmalayıcısının takip etmesi önerilir. Bu, eski bir bağlantı noktasının yeni başlatılmış veya yeniden kullanılan bir süreçle karıştırılmasını önler.

Motor, desteklenen platformlarda hizmet keşfi (service discovery) aracılığıyla geliştirme hedeflerini de duyurur. Bu mekanizma öncelikle Defold araçları tarafından kullanılır; bunun yerine koda kalıcı olarak sabitlenmiş bir bağlantı noktası kullanılması önerilmez.

Sunucuya yerel makinede, localhost (`127.0.0.1`) adresinde belirli bir bağlantı noktası üzerinden erişilebilir:

![Motor sunucusuna erişim](images/automation/engine-server.png)

## Yerleşik uç noktalar

Mevcut hata ayıklama motoru az sayıda temel rota kaydeder.

| Uç nokta | Amaç |
| --- | --- |
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

## Eklentilerin tanımladığı çalışma zamanı rotaları

Hata ayıklama derlemelerinde, yerel kod eklentisi (native extension) SDK'sı motorun web sunucusuna erişim sağlayabilir. Bir eklenti bu sunucuda bir rota öneki kaydedebilir ve çalışma zamanı verilerine bağlı işlemler sunabilir.

Bu, geliştirme araçları için yararlıdır; çünkü bir eklenti başka bir HTTP sunucusu açmak yerine mevcut motor hizmetini paylaşabilir.

Bir eklentinin tanımladığı çalışma zamanı otomasyon API'sinin şunları yapması önerilir:

* ayrı, sürümlendirilmiş bir rota öneki kullanmak;
* desteklenen yetenekleri sunmak;
* yapılandırılmış hatalar döndürmek;
* kullanılamayan platform veya motor özelliklerini açıkça ele almak;
* işlemleri yerel geliştirme ve test ortamlarıyla sınırlamak;
* yayıma yönelik derlemelerden çıkarılıp çıkarılmadığını belgelemek.

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

### Düzenleyici ve çalışma zamanı istemcileri

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

## Sınırlamalar ve güvenlik

Motor hizmeti ve eklentilerin tanımladığı rotalar geliştirme araçlarıdır ve buna uygun şekilde ele alınmaları önerilir.

::: important
Motor hizmeti şu anda bir OpenAPI belgesi yayımlamaz. Tümleştirmelerin belgelenmiş davranışlarla veya bir eklentinin sürümlendirilmiş API'siyle sınırlı kalması önerilir.
:::

Çalışma zamanı betikleri, fizik, girdi, dinamik olarak oluşturulan nesneler ve platforma özgü işleme, çalışan bir motor gerektirir ve [otomatik çalışma zamanı testleri](/manuals/automated-testing) aracılığıyla doğrulanmaları önerilir.

* Hizmeti bir yönlendirici, genel erişime açık bir arayüz veya güvenilmeyen bir tünel üzerinden yayımlamayın.
* Motor hizmeti rotalarının kimlik doğrulama gerektirdiğini varsaymayın.
* Çalışma zamanı rotaları, eklenti sürümüne, platforma, grafik arka ucuna ve motor yeteneklerine göre değişebilir.
* Eklentilerin tanımladığı güncel API'ler için sürüm veya yetenek uzlaşması kullanın.
