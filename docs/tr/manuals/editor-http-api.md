---
title: Defold düzenleyicisini HTTP ile otomatikleştirme
brief: Bu kılavuz, harici araçların Defold düzenleyicisinde açık olan bir projenin yerel HTTP API'sini nasıl keşfedip kullanabileceğini açıklar.
---

# Defold düzenleyicisini otomatikleştirme

Defold düzenleyicisi otomatik işlemler için özel bir sunucu açar. HTTP API'si açık projeyi denetler. Bunu düzenleyici komutları, proje derleme işlemleri, proje kaynakları (resource), önizlemeler, tercihler, konsol çıktısı, belge arama veya düzenleyici betiği (editor script) tümleştirmeleri için kullanın. Çalışan oyunu incelemek veya denetlemek için ise [motor hizmetini ya da bir çalışma zamanı otomasyon API'sini](/manuals/engine-service) kullanın.

::: important
Düzenleyici HTTP API'si deneyseldir ve Defold sürümleri arasında değişebilir. Kullanılabilir işlemler ve şemalar için çalışan düzenleyicinin ürettiği `/openapi.json` belgesi esas alınır.
:::

## Düzenleyiciyi harici bir araçtan başlatma

Harici bir araç, düzenleyicinin yürütülebilir dosyasına ve projenin `game.project` dosyasının mutlak yoluna ihtiyaç duyar.

Kurulu Defold sürümlerinin konumları, [Düzenleyici kılavuzunda](/manuals/editor/#editor-installation-metadata) açıklandığı gibi `installations.json` aracılığıyla bulunabilir. Bu dosyanın `launcherPath` alanı, başlatılacak yürütülebilir dosyayı içerir. Projeyi doğrudan açmak için `game.project` yolunu ilk konumsal bağımsız değişken olarak geçirin.

İsteğe bağlı `--port` veya `-p` bağımsız değişkeni, düzenleyici sunucusunun bağlantı noktasını seçer. Bu bağımsız değişkeni belirtmezseniz Defold kullanılabilir bir bağlantı noktası seçer; birden fazla projenin açık olabileceği durumlarda genellikle bu tercih edilir.

```sh
# Linux
/path/to/Defold/Defold --port 8181 /absolute/path/to/project/game.project
```

```sh
# macOS
/path/to/Defold.app/Contents/MacOS/Defold --port 8181 /absolute/path/to/project/game.project
```

```powershell
# Windows
C:\path\to\Defold\Defold.exe --port 8181 C:\absolute\path\to\project\game.project
```

Düzenleyici, grafik arayüzü olan bir masaüstü uygulamasıdır. Ekrana erişimi olan etkileşimli bir kullanıcı oturumunda başlatın. Grafik arayüzü olmadan çalışan sürekli tümleştirme (CI) ortamlarında olduğu gibi grafik oturumun kullanılamadığı durumlarda veya bağımsız dağıtım paketleri (bundle) oluşturmak için [Bob](/manuals/bob) kullanın. Açık bir düzenleyici, `/command/compile` aracılığıyla yalnızca kod derleyen otomasyonu da destekler.

Düzenleyiciyi başlattıktan sonra projenin açılmasını ve `.internal/editor.port` dosyasının oluşmasını bekleyin. Ardından geçerli bir belge dönene kadar `/openapi.json` yolunu düzenli aralıklarla sorgulayın. Sürecin oluşturulmasının projenin hazır olduğu anlamına geldiğini varsaymayın.

## Düzenleyici sunucusunu bulma

Düzenleyici, bir proje açıkken yerel bir HTTP sunucusu başlatır. Ana sayfasını varsayılan tarayıcıda açmak için <kbd>Help ▸ Open Editor Server</kbd> seçeneğini seçin:

![Yerel düzenleyici sunucusunun ana sayfası](images/automation/editor_server.png)

Seçilen bağlantı noktası, proje içinde şu dosyaya yazılır:

```text
.internal/editor.port
```

Bu kılavuzdaki örnekler ve komutlar bundan sonra şu kabuk değişkenlerine başvuracaktır:

```sh
PORT="$(cat .internal/editor.port)"
BASE_URL="http://127.0.0.1:$PORT"
```

Bağlantı noktası dosyası geçerli düzenleyici oturumuna aittir. Düzenleyiciyi yeniden başlattıktan sonra dosyayı yeniden okuyun.

::: important
Düzenleyici sunucusu, güvenilir bir yerel denetim arayüzüdür. Herkese açık bir adres, bağlantı noktası yönlendirmesi veya güvenilmeyen bir tünel üzerinden erişime açmayın.
:::

## OpenAPI aracılığıyla işlemleri keşfetme

Harici bir aracın ihtiyaç duyması gereken Defold'a özgü başlangıç bilgileri yalnızca düzenleyicinin bağlantı noktası ve OpenAPI belgesidir:

```sh
curl -sS "http://127.0.0.1:$(cat .internal/editor.port)/openapi.json"
```

Dönen OpenAPI 3.0.3 belgesi, çalışan düzenleyici sürümünün desteklediği işlemleri; yollar, yöntemler, parametreler, komut adları, istek biçimleri, yanıtlar, durum kodları ve kimlik doğrulama gereksinimleri dahil olmak üzere açıklar.

Belgelenmiş yolları listeleyin:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[]'
```

Belgelenmiş düzenleyici komut yollarını listeleyin:

```sh
curl -sS "$BASE_URL/openapi.json" |
  jq -r '.paths | keys[] | select(startswith("/command/"))'
```

Defold 1.13.2 ve sonraki sürümlerde, her komutun OpenAPI belgesinde kendine ait bir yolu vardır. Önceki sürümler komutları `/command/{command}` yolu ve komut adlarını içeren bir numaralandırma türü (enum) aracılığıyla tanımlar.

Sürümü dikkate alan bir tümleştirmenin, gerekli her işlemi doğrulaması ve istekleri dönen şemaya göre yapılandırması önerilir. Uç nokta veya komut adlarının eksiksiz olduğu varsayılan bir kopyasını tutmanızı önermiyoruz; bu kopya güncelliğini yitirebilir.

Projede tanımlanan rotalar, düzenleyici betikleri bir OpenAPI işlem açıklaması sağladığında `/openapi.json` belgesinde de görünür.

## Düzenleyici komutlarını yürütme

Düzenleyici komutlarını, komutun belgelenmiş yoluna bir `POST` isteği göndererek çağırın; örneğin:

```text
POST /command/compile
POST /command/run
```

Projeyi çalıştırmadan kodunu derlemek için:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/compile" |
  jq
```

Projenin kodunu derlemek ve projeyi çalıştırmak için:

```sh
curl -sS \
  -X POST \
  "$BASE_URL/command/run" |
  jq
```

Bu komut zincirleri yanıt gövdesini görüntüler. Otomasyon betiklerinde, [HTML5 için derleme](#building-html5) bölümündeki örüntüyü kullanarak HTTP durumunu ve `success` değerini de kontrol edin.

::: sidenote
Defold 1.13.2 sürümünden itibaren `/command/build`, `/command/run` için kullanımı artık önerilmeyen bir uyumluluk takma adıdır ve OpenAPI içinde listelenmez. Yeni tümleştirmelerde `/command/run` kullanın.
:::

Başarılı bir kod derleme işlemi, yapılandırılmış bir sonuçla birlikte `200` HTTP durumunu döndürür:

```json
{
  "success": true,
  "issues": []
}
```

Başarısız bir proje derleme işlemi, aşağıdaki gibi sorunlarla birlikte `422` HTTP durumunu döndürür:

```json
{
  "success": false,
  "issues": [
    {
      "message": "Example compiler message",
      "severity": "error",
      "resource": "/main/player.script",
      "range": {
        "start": {
          "line": 12,
          "character": 4
        },
        "end": {
          "line": 12,
          "character": 17
        }
      }
    }
  ]
}
```

Kullanılabilir alanlar hataya bağlıdır. Varsa kaynak yolunu ve kaynak kod aralığını kullanın; ancak yalnızca bir ileti içeren sorunları da işleyin.

Çalışan düzenleyici tarafından listelendiklerinde genellikle yararlı olan komutlar şunlardır:

`compile`
: Projeyi çalıştırmadan kodunu derleyin.

`run`
: Projenin kodunu derleyin ve projeyi çalıştırın.

`clean-build`
: Derleme önbelleğini temizleyin, ardından kodu derleyip projeyi çalıştırın. Bunu yalnızca normal bir derleme tutarsız davrandığında veya değişiklikleri atlıyor gibi göründüğünde kullanın.

`build-html5`
: Projeyi HTML5 için derleyin ve çıktıyı düzenleyici sunucusu üzerinden kullanılabilir hâle getirin.

`fetch-libraries`
: Proje bağımlılıklarını indirin ve yeniden yükleyin.

`hot-reload`
: Değiştirilen kaynakları çalışan bir oyuna yeniden yükleyin.

`reload-extensions`
: Düzenleyici betiklerini yeniden yükleyin.

`debugger-start`, `debugger-stop` ve hata ayıklayıcının adım komutları
: Bir hata ayıklama oturumunu ve çalışan projeyi denetleyin.

Tam adlar ve kullanılabilirlik, düzenleyici sürümüne ve düzenleyicinin geçerli durumuna bağlıdır; bunları `/openapi.json` üzerinden keşfedin.

Proje kaynakları üzerinde çalışan komutlar, yürütülmeden önce harici dosya değişikliklerini eşitler.

### Komut yanıtları ve eşzamansız işlemler

Yanıtlar komuta bağlıdır. Defold 1.13.2 ve sonraki sürümlerde `compile`, `run`, `clean-build`, `build-html5`, `debugger-start` ve `hot-reload`, komutun tamamlanmasını bekler ve yukarıda gösterildiği gibi `success` ve `issues` içeren yapılandırılmış bir sonuç döndürür. Başarılı bir sonuç HTTP `200` döndürür; derleme veya doğrulama başarısızlığı `422` döndürür.

Diğer komutlar, örneğin `debugger-break`, hâlâ `202` döndürebilir. Geçerli OpenAPI şemasındaki işlemi inceleyin ve dönen gerçek HTTP yanıt durumunu işleyin:

| Durum | Anlamı |
| --- | --- |
| `200` | Komut tamamlandı ve bir sonuç döndürdü |
| `202` | Komut kabul edildi ve eşzamansız olarak devam ediyor |
| `403` | Komut, düzenleyicinin geçerli durumunda etkin değil |
| `404` | Komut kullanılamıyor |
| `422` | Derleme veya doğrulama başarısız oldu |
| `500` | Düzenleyicinin içinde bir hata oluştu |

Bir HTTP `202` yanıtı, istenen sonucun mevcut olduğunu kanıtlamaz. İlgili çıktıyı, kaynağı, konsol işaretini veya sunulan URL adresini bekleyin ve bir zaman aşımı uygulayın.

### HTML5 için derleme {#building-html5}

Geçerli OpenAPI belgesinde `/command/build-html5` listeleniyorsa komutu bu yol üzerinden çağırın. Bir kabuk betiğinde HTTP durumunu yanıt gövdesinden ayrı olarak alın ve istek veya derleme başarısız olduğunda durun:

```sh
build_response_file="$(mktemp)" || exit 1
if ! build_http_status="$(curl -sS \
  -X POST \
  -o "$build_response_file" \
  -w '%{http_code}' \
  "$BASE_URL/command/build-html5")"; then
  cat "$build_response_file"
  rm -f "$build_response_file"
  exit 1
fi

cat "$build_response_file"
if [ "$build_http_status" != "200" ] ||
   ! jq -e '.success == true' "$build_response_file" > /dev/null; then
  rm -f "$build_response_file"
  exit 1
fi
rm -f "$build_response_file"
```

Defold 1.13.2 ve sonraki sürümlerde bu istek, derlemenin bitmesini bekler ve yapılandırılmış bir sonuç döndürür. Örnek, derleme sorunları dahil yanıt gövdesini yazdırır ve yalnızca HTTP `200` ile `success: true` döndüğünde devam eder. Başarılı bir derlemeden sonra düzenleyici oyunu bir tarayıcıda açar ve şu adreste sunar:

```text
http://127.0.0.1:<editor-port>/html5/
```

Derlemenin tamamlanması, oyunun tarayıcıya yüklenmesinin bittiği anlamına gelmez. Girdi göndermeden veya oynanışı kontrol etmeden önce tuvalin ve uygulamanın hazır olmasını bekleyin. Daha fazla bilgi için [HTML5 için tarayıcı testleri](/manuals/automated-testing/#browser-tests-for-html5) bölümüne bakın.

## API belgelerinde arama

`/openapi.json` belgesinde yer aldığında `/ref` işlemi, çalışan düzenleyici sürümüyle birlikte gelen API belgelerinde arama yapar. Bu sürümle eşleşen adları ve imzaları sağlar.

Örneğin bir işlevi aramak için şunu kullanın:

```sh
curl -sS \
  --get \
  --data-urlencode "q=go.animate" \
  "$BASE_URL/ref" |
  jq
```

Ortama ve dile göre filtreleyin:

```sh
curl -sS \
  --get \
  --data-urlencode "environment=runtime" \
  --data-urlencode "language=Lua" \
  --data-urlencode "q=collision message|raycast" \
  "$BASE_URL/ref" |
  jq
```

Arama parametreleri şunlardır:

`environment`
: `editor`, `runtime` veya virgülle ayrılmış değerler.

`language`
: `Lua`, `C`, `C++` veya virgülle ayrılmış değerler.

`q`
: Büyük/küçük harfe duyarlı olmayan bir ifade. Boşluk karakterleri VE anlamına gelirken `|`, VEYA anlamına gelir.

Yoğunlaştırılmış belge kaynakları da vardır: [LLM belge dizini](https://defold.com/llms.txt), resmî kılavuzlara, API ad alanlarına ve örneklere bağlantılar verir; [tam LLM belgeleri](https://defold.com/llms-full.txt) ise çevrimdışı aramayı ve yerel dizinlemeyi desteklemek için belgelerin tamamını listeler.

Yapay zekâ ajanlarının, yalnızca bir API veya ileti gerektiğinde tüm bir başvuru kaynağını getirmek yerine hedefi belirli aramaları tercih etmesi önerilir; böylece token kullanımını azaltabilir ve görev için daha iyi hazırlanmış, temiz bir bağlam elde edebilirler.

## Konsol çıktısını okuma {#reading-console-output}

Düzenleyici konsolunu JSON olarak okuyun:

```sh
curl -sS "$BASE_URL/console" | jq
```

Yanıt, `lines` içinde konsol metnini ve `regions` içinde hatalar, değerlendirme sonuçları ve kaynak başvuruları dahil anlamsal bölgeleri içerir.

Konsol çıktısını sürekli izlemek için şunu kullanın:

```sh
curl -N "$BASE_URL/console/stream"
```

Akış, mevcut konsol satırlarını içerir ve ardından yeni çıktılar için açık kalır. Bir tamamlanma işareti veya hata aldıktan, sürecin sonlandığını algıladıktan ya da bir zaman aşımına veya satır sınırına ulaştıktan sonra kapatın.

Test sonuçlarını diğer çıktılardan ayırma ve başarısızlıkları sınıflandırma hakkında bilgi için [Otomatik test ve doğrulama](/manuals/automated-testing/#structured-test-results) bölümüne bakın.

## Sahne önizlemelerini işleme {#rendering-scene-previews}

Defold düzenleyicisi (1.13.1 sürümünden itibaren), `/preview/{path}` komutuyla işleme (rendering) yaparak desteklenen bir sahne kaynağının "ekran görüntüsünü" PNG biçiminde oluşturabilir:

```sh
mkdir -p build/automation

curl -sS \
  "$BASE_URL/preview/main/main.collection?width=1280&height=720" \
  --output build/automation/main-preview.png
```

Bu işlem, açık Basic 3D şablon projesindeki ana koleksiyonu (collection) varsayılan başlangıç görünümünde işler:

![Ana koleksiyonun düzenleyicide işlenmiş önizlemesi](images/automation/main-preview.png)

Görsel sahne düzenleyicisini kullanan kaynakların önizlemelerini almak için işlemeden yararlanabilirsiniz. Örneğin bir model bileşenini (component) aynı şekilde işleyerek görünümünü veya gölgelendiricinin doğruluğunu kontrol edebilirsiniz:

```sh
curl -sS \
  "$BASE_URL/preview/assets/models/cube.model?width=1280&height=720" \
  --output build/automation/cube-preview.png
```

![Küp modelinin düzenleyicide işlenmiş önizlemesi](images/automation/cube-preview.png)

`/preview/` sonrasındaki yol, başında eğik çizgi içermez. İsteğe bağlı boyutlar varsayılan olarak projenin ekran boyutudur ve `1` ile `4096` arasında olmalıdır.

| Durum | Anlamı |
| --- | --- |
| `200` | Önizleme işlendi |
| `400` | Boyutlar geçersiz |
| `404` | Kaynak bulunamadı |
| `422` | Kaynak yüklenmemiş veya sahne önizlemelerini desteklemiyor |

Önizlemeler; bölüm yerleşimlerini, GUI yerleşimlerini, gölgelendirici ve aydınlatma kurulumunu ya da görsel gerilemeleri kontrol etmek gibi projenin görsel analizi için veya belgeler için küçük resimler oluşturmakta çok yararlı olabilir.

::: important
Düzenleyici önizlemesi, çalışan oyunun ekran görüntüsü değildir. Dinamik olarak oluşturulan nesneleri, çalışma sırasındaki son işlemeyi veya platforma özgü işlemeyi doğrulamaz. Bu öğeler gerektiğinde [çalışan oyundan alınan bir ekran görüntüsünü](/manuals/automated-testing/#editor-previews-and-runtime-screenshots) kullanın.
:::

## Düzenleyicide Lua yürütme

Kimlik doğrulaması gerektiren `POST /eval` işlemi, Lua kodunu düzenleyici eklenti ortamında yürütür. Her oturuma ait taşıyıcı belirteç (bearer token) şu dosyada saklanır:

```text
.internal/editor.token
```

Belirteci okuyun ve kodu yürütün:

```sh
TOKEN="$(cat .internal/editor.token)"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary 'print(editor.version) return editor.platform' \
  "$BASE_URL/eval"
```

Yazdırılan çıktı ve dönüş değerleri metin olarak döndürülür. Tipik yanıtlar şunlardır:

| Durum | Anlamı |
| --- | --- |
| `200` | Kod yürütüldü |
| `401` | Taşıyıcı belirteç eksik veya geçersiz |
| `422` | Lua kodu ayrıştırılamadı veya yürütülemedi |
| `503` | Düzenleyici eklenti ortamı hazır değil |

Bir istemci `503` yanıtından sonra yeniden deneyebilir, ancak deneme sayısını sınırlaması önerilir. `422` döndüren bir isteği yinelemeden önce kodu düzeltin.

Değerlendirilen kod, [Düzenleyici API'sini](https://defold.com/ref/editor-lua/) ve düzenleyici betik ortamını kullanabilir. Çalışan bir oyunu değiştirmek için `go.*` gibi oyun çalışma zamanı API'lerini kullanamaz. Oynanış için bir çalışma zamanı testi, hata ayıklayıcı, tarayıcı testi veya [çalışma zamanı otomasyon API'si](/manuals/engine-service/#automation-bridge-extension) kullanın.

### Kaynakları ve dosyaları değiştirme

Birçok Defold kaynak dosyası metin biçimlerini kullanır ve herhangi bir metin düzenleme aracıyla düzenlenebilir. Defold projesinin yapılandırılmış kaynaklarını değiştirmek için düzenleyici işlemlerini (editor transaction) tercih edin.

| Değişiklik | Tercih edilen yöntem |
| --- | --- |
| Lua, gölgelendirici, JSON veya bilinen başka bir metin biçimi | Dosyayı doğrudan değiştirme |
| Açık bir düzenleyici sekmesindeki kaydedilmemiş metin | `editor.get()` ve `editor.transact()` |
| Koleksiyon, oyun nesnesi (game object), GUI, atlas veya başka bir yapılandırılmış kaynak | Düzenleyici işlemi |
| Tekrar tekrar üretilen içerik | Bağımsız üretici |
| Tekrarlanabilir proje işlemi | Düzenleyici komutu veya özel HTTP uç noktası |
| Yalnızca CI ortamında yapılan dönüşüm | Bob'dan önce çalıştırılan bağımsız betik |

Bir kaynağı değiştirmeden önce inceleyin:

```sh
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/plain" \
  --data-binary '
    local path = "/game.project"
    pprint(editor.properties(path))
    return editor.get(path, "path")
  ' \
  "$BASE_URL/eval"
```

Bir işlem gerçekleştirmeden önce `editor.can_get()`, `editor.can_set()` ve diğer `editor.can_*()` işlevlerini kontrol edin.

Bir biçimlendirici, doğrulayıcı veya üretici çalıştırmak için düzenleyici Lua ortamında `editor.execute()` kullanın:

```lua
local output = editor.execute(
  "python3",
  "scripts/generate_levels.py",
  {
    out = "capture"
  }
)

print(output)
```

Komut proje kaynaklarını değiştirmiyorsa gereksiz bir yeniden yüklemeden kaçınmak için `reload_resources = false` ayarını kullanın.

::: important
`.internal/` içindeki dosyaları veya `build/` içindeki üretilmiş içeriği değiştirmeyin.
:::

## Tercihler

Düzenleyici tercihleri, OpenAPI içinde belgelenen ve şu anda `/prefs/{path}` olan yol üzerinden okunabilir ve yazılabilir.

Örneğin ayarlanmış kod yazı tipi boyutunu okuyabilirsiniz:

```sh
curl -sS "$BASE_URL/prefs/code/font/size" | jq
```

Veya örneğin 16 olarak ayarlayabilirsiniz:

```sh
curl -sS \
  -X POST \
  -H "Content-Type: application/json" \
  --data '16' \
  "$BASE_URL/prefs/code/font/size"
```

Düzenleyici, değeri tercih şemasına göre doğrular. Geçersiz bir yol veya değer HTTP `400` döndürür.

Tercihler, `game.project` dosyasında saklanan proje yapılandırması değil, kalıcı kullanıcı ayarları veya projeye özgü kullanıcı ayarlarıdır. Otomasyonun bir tercihi geçici olarak değiştirmesi gerekiyorsa önceki değeri kaydedin ve sonrasında geri yükleyin.

## Projede tanımlanan rotalar

Düzenleyici betikleri, [`get_http_server_routes()`](/manuals/editor-scripts/#http-server) ile ek rotalar tanımlayabilir. İsteğe bağlı bir OpenAPI işlem tablosu, bir rotayı yerleşik işlemlerle aynı `/openapi.json` belgesi üzerinden sunar.

Projede tanımlanan rotalar; içerik üretimi, doğrulama, raporlar, yerelleştirme kontrolleri, kaynak analizi, projeye özgü testler veya bir IDE ya da harici denetleyici için daha küçük bir arayüz sağlayabilir.

İyi bir rotanın, adı açıkça belirtilmiş tek bir işlem gerçekleştirmesi, girdisini doğrulaması, yapılandırılmış bir sonuç döndürmesi, mümkün olduğunda tekrarlandığında ek etki oluşturmaması (idempotent olması) ve yüksek maliyetli işlemleri sınırlaması önerilir.

Projede tanımlanan rotalar `/eval` belirteciyle otomatik olarak korunmaz. Bir rota hassas işlemler gerçekleştiriyorsa projeye özgü kimlik doğrulama ve güvenlik kontrolleri ekleyin.

## Yaşam döngüsü kancaları {#lifecycle-hooks}

Yaşam döngüsü kancaları (lifecycle hook), derlemelerden ve dağıtım paketi oluşturmadan önce ve sonra, ayrıca bir oyun süreci başlatıldığında veya sonlandığında çalıştırılabilen işlevlerdir. Bir projenin kök dizininde bir adet `hooks.editor_script` dosyası bulunabilir. Bu olayları yalnızca kök dizindeki kanca dosyası alır; böylece proje, olayların sırasını tek bir yerde tanımlayabilir.

```lua
local M = {}

local function validate_project()
  print(editor.execute(
    "python3",
    "scripts/validate_project.py",
    {
      out = "capture",
      reload_resources = false
    }
  ))
end

function M.on_build_started(opts)
  validate_project()
end

function M.on_build_finished(opts)
  print("Build successful:", opts.success)
end

return M
```

`on_build_started()` işlevinin ürettiği bir hata, düzenleyici derlemesini durdurur. Yaşam döngüsü kancaları yalnızca düzenleyicide çalışır; ortak doğrulama ve üretim mantığını, CI ortamından da çağrılabilen bağımsız betiklere yerleştirin.

## Güvenlik ve uyumluluk

Düzenleyici sunucusunun tamamını güvenilir bir yerel arayüz olarak ele alın:

* Bağlantı noktasını herkese açık erişime açmayın.
* `.internal/editor.token` dosyasını koruyun; bu dosya geçerli oturum için `/eval` yetkisi verir.
* Dışarıya sınırsız `/eval` erişimi vermeyin.
* Belirteci istemlerde, raporlarda veya günlüklerde değil, yerel tümleştirme katmanında tutun.
* Projede tanımlanan rotaların `/eval` kimlik doğrulamasını devralmadığını unutmayın.
* Güncel `/openapi.json` belgesini kullanın.
* Eşzamansız otomatik komutlar ve düzenleyicinin başlatılması için sınırlı bekleme süreleri kullanın.

## Motor sunucusu

Düzenleyici sunucusu, düzenleyici sürecine aittir. Çalışan bir oyunun, [motor hizmeti ve çalışma zamanı HTTP API kılavuzunda](/manuals/engine-service) açıklanan farklı bir bağlantı noktası ve farklı sorumlulukları vardır.
