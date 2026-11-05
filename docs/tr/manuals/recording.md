---
title: Defold'da video kaydı
brief: Bu kılavuz, Lua veya motorun HTTP hizmeti aracılığıyla oyun penceresini MP4 olarak kaydetmeyi açıklar.
---

# Video kaydı {#video-recording}

Defold, [`recorder` Lua modülü](/ref/recorder/) veya [motorun HTTP hizmeti](/manuals/engine-service/#recording-endpoints) aracılığıyla oyun penceresini bir MP4 dosyasına H.264 video olarak kaydedebilir. İki arayüz de aynı kaydediciyi paylaşır; bu nedenle aynı anda yalnızca bir kayıt başlatılabilir, çalışabilir veya sonlandırılabilir.

## Kullanılabilirlik {#availability}

Kayıt, masaüstü **hata ayıklama** motorlarında bulunur. Yayıma yönelik, görüntüsüz (headless), mobil ve web derlemelerinde bulunmaz. Bir [App Manifest](/manuals/app-manifest/#exclude-record) içinde **Exclude Record** seçeneğini etkinleştirmek de Lua modülünü ve HTTP rotalarını kaldırır.

| Platform | Video gereksinimleri | Uygulama sesi |
| --- | --- | --- |
| macOS | ScreenCaptureKit kullanan macOS 15 veya sonrası | Desteklenir |
| Windows | Windows Graphics Capture ve Media Foundation kullanan Windows 10 sürüm 1903 veya sonrası | Windows derleme 20348 veya sonrasında desteklenir |
| Linux | Kare arabelleği yakalama kullanan OpenGL, OpenGL ES veya Vulkan | Desteklenmez |

Video ve ses desteği ayrı ayrı kontrol edilir. HTTP istemcileri `/recording/capabilities` sonucunu inceleyebilir; Lua çağrıları, istenen yakalama desteklenmiyorsa hata alır. İşletim sistemi izinleri ve yakalama cihazı arızaları da başlatma isteği kabul edildikten sonra eşzamansız hataya yol açabilir.

Kaydedici, oyun penceresinin içeriğini fiziksel piksel cinsinden özgün boyutunda yakalar. Çift sayılı video boyutları elde etmek için bir satır veya sütunu kırpabilir. Pencereyi yeniden boyutlandırmak veya piksel yoğunluğunu değiştirmek kaydı durdurur ve sonlandırır. Yakalama hızı saniyede 1–60 karedir; varsayılan 30'dur.

## Lua ile kayıt {#recording-from-lua}

Yazılabilir bir çıktı yolu ve geri çağırımla [`recorder.start()`](/ref/recorder/#recorder.start) kullanın. Üst dizin mevcut olmalıdır; [`sys.get_save_file()`](/ref/sys/#sys.get_save_file) uygun bir uygulama kayıt yolu sağlar. Mevcut çıktı dosyasının üzerine yazılabilir. Lua kayıtları çağırana aittir ve motor kapandıktan sonra diskte kalır.

Yollar, Lua dosya girdisi/çıktısında olduğu gibi Windows'ta Windows ANSI kod sayfasını, diğer platformlarda UTF-8 kullanır. Geri çağırımın `result.path` alanı, `recorder.start()` işlevine verilen yolu korur.

Bu `.script` örneği, yakalama başladıktan sonra beş saniye kayıt yapar:

```lua
local function on_recording_event(self, event, result)
    if event == recorder.EVENT_STARTED then
        self.recording = true
        timer.delay(5, false, function(self)
            if self.recording then
                local ok, err = recorder.stop()
                if not ok then
                    print("Could not stop recording:", err)
                end
            end
        end)
    elseif event == recorder.EVENT_STOPPED then
        self.recording = false
        print("MP4 ready:", result.path)
    elseif event == recorder.EVENT_ERROR then
        self.recording = false
        print("Recording failed:", result.error)
    end
end

function init(self)
    self.recording = false
    if not recorder then
        print("Recording is not included in this engine build")
        return
    end

    local ok, err = recorder.start({
        path = sys.get_save_file("recording_example", "capture.mp4"),
        fps = 30,
        audio = false,
    }, on_recording_event)
    if not ok then
        print("Could not start recording:", err)
    end
end
```

`recorder.start()` ve [`recorder.stop()`](/ref/recorder/#recorder.stop), istek kabul edildiğinde `true`, reddedildiğinde `nil, error` döndürür. Kabul edilmesi, yakalamanın veya dosya sonlandırmanın bittiği anlamına gelmez. Geçersiz seçenekler Lua hatalarına yol açar.

Geri çağırımlar motor güncellemeleri sırasında çalışır:

| Olay | Anlam |
| --- | --- |
| `recorder.EVENT_STARTED` | Yakalama etkindir; artık durdurulabilir. |
| `recorder.EVENT_STOPPED` | MP4 sonlandırılmıştır ve okunmaya hazırdır. Yeniden boyutlandırma nedeniyle otomatik durdurmadan sonra da oluşur. |
| `recorder.EVENT_ERROR` | Yakalama başarısız olmuştur; `result.error` alanını inceleyin. Başlangıç hatası, `EVENT_STARTED` olmadan bu olayı üretebilir. |

Sonuç ayrıca `path`, `width`, `height`, `fps` ve `audio` içerir. Çıktıyı yalnızca `EVENT_STOPPED` sonrasında okuyun veya yükleyin. Geri çağırımı alabilmek için başlatan betiği canlı tutun: betiği silmek yakalamayı durdurmadan geri çağırımları atar. Motorun kapanması, Lua geri çağırımlarını çağırmadan yakalamayı sonlandırır.

Ses, **Lua'da varsayılan olarak devre dışıdır**. Desteklenen bir platformda uygulama sesini istemek için `audio = true` ayarlayın. Desteklenmeyen sesin istenmesi hata döndürür.

### Kaydediciyi HTTP istemcileriyle paylaşma {#sharing-the-recorder-with-http-clients}

`recorder.stop()`, HTTP üzerinden başlatılmış olanlar dahil geçerli paylaşılan kaydı hedefler. Bir işlem bekliyorken veya etkin kayıt yokken hata döndürür. Bir HTTP istemcisi Lua kaydını durdurursa özgün Lua geri çağırımı yine tamamlanma olayını alır. HTTP üzerinden başlatmak Lua geri çağırımı oluşturmaz; tamamlanmayı izlemek için HTTP durumunu kullanın.

HTTP durumu bir Lua kaydını açıklayabilir, ancak `file` alanı `null` olur: hizmet yalnızca HTTP üzerinden başlatılan kayıtlar için indirme hazırlar. Lua kaydını `EVENT_STOPPED` sonrasında `result.path` yolundan okuyun.

## HTTP üzerinden kayıt {#recording-through-http}

Kayıt rotaları, oyun günlüğünde yazdırılan motor hizmeti bağlantı noktasını kullanır. Bunları [motor hizmeti kılavuzunda](/manuals/engine-service/#discovering-operations-through-openapi) açıklandığı gibi `/openapi.json` üzerinden keşfedin. Görüntüsüz veya yayıma yönelik motor bu rotaları sunmaz.

Aşağıdaki komutlar POSIX kabuğu, `curl` ve `jq` kullanır; indirme doğrulama adımı ayrıca Python 3 kullanır. Bunları aynı kabukta çalıştırın ve `<port>` yerine çalışan motorun bağlantı noktasını yazın. Önce yetenekleri sorgulayın ve hizmet kimliğini saklayın:

```sh
set -eu
ENGINE_URL="http://127.0.0.1:<port>"
CAPABILITIES=$(curl -fsS "$ENGINE_URL/recording/capabilities")
printf '%s\n' "$CAPABILITIES" | jq
INSTANCE_ID=$(printf '%s\n' "$CAPABILITIES" | jq -er 'select(.supported) | .instance_id')
```

Yalnızca `supported` değeri `true` ise devam edin; değilse `unsupported_reason` ve `minimum_platform_version` alanlarını inceleyin. `audio` alanı ses desteğini bildirir. Lua'dan farklı olarak **HTTP kaydı, arka uç desteklediğinde sesi varsayılan olarak etkinleştirir**. Aşağıdaki örnek sesi açıkça devre dışı bırakır.

### Kaydı başlatma ve inceleme {#start-and-inspect-the-recording}

`fps` ve/veya `audio` içeren isteğe bağlı bir JSON nesnesiyle başlatın. Çıktı dosyasını hizmet seçer; yol, genişlik, yükseklik veya ölçek kabul etmez.

```sh
START=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data '{"fps":30,"audio":false}' \
    "$ENGINE_URL/recording/start")
OPERATION_ID=$(printf '%s\n' "$START" | jq -er '.operation_id')
printf '%s\n' "$START" | jq
```

HTTP 202, isteğin kabul edildiğini belirtir. `pending` değeri `false`, `active` değeri `true` olana kadar aşağıdaki durum komutunu yeniden çalıştırın. Kontrol, başka bir işleme ait yanıtı reddeder ve yakalama veya dosya hazırlama hatalarını bildirir. Otomatik durdurma kaydı zaten sonlandırdıysa indirmeden önce [sonlandırma](#stop-and-wait-for-finalization) adımına devam edin.

```sh
STATUS=$(curl -fsS \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL/recording/status")
printf '%s\n' "$STATUS" | jq -e --argjson id "$OPERATION_ID" '
    if .operation_id != $id then error("Recording operation changed")
    elif .state == "failed" then error(.failure)
    elif .file.state == "failed" then error("Recording file preparation failed")
    else . end'
```

Kaydetmek istediğiniz süre boyunca oyunun çalışmasına izin verin, ardından durdurma isteği gönderin. Pencere yeniden boyutlandırılmış ve kayıt zaten tamamlanmışsa durdurma isteğini atlayıp aşağıdaki sonlandırma adımına geçin.

### Durdurma ve sonlandırmayı bekleme {#stop-and-wait-for-finalization}

Başlatma yanıtından kimliğini sakladığınız işlemi durdurun:

```sh
STOP_BODY=$(jq -n --argjson id "$OPERATION_ID" '{operation_id: $id}')
STOP=$(curl -fsS -X POST \
    -H 'Content-Type: application/json' \
    -H "X-Recording-Instance: $INSTANCE_ID" \
    --data "$STOP_BODY" \
    "$ENGINE_URL/recording/stop")
printf '%s\n' "$STOP" | jq
```

HTTP 202 yalnızca durdurma isteğini kabul eder. `pending` değeri `false`, `finalized` değeri `true` ve `file.state` değeri `complete` olana kadar durum komutunu yineleyin. Hizmet, yerel yakalama bittikten sonra dosya boyutunu ve SHA-256 değerini hazırlar; bu nedenle yalnızca `state: "complete"` ve `finalized: true`, indirmenin hazır olduğu anlamına gelmez. `state` veya `file.state`, `failed` olursa beklemeyi bırakın; durumu `pending` ya da `failed` olan dosyayı indirmeyin.

Otomatik bir istemcinin gecikme ve zaman aşımı kullanarak sorgulaması ve her yanıtta saklanan işlem kimliğini kontrol etmesi önerilir. Yakalama ve sonlandırma beklenirken motorun güncellenmeye devam etmesine izin verin.

### Dosyayı indirme ve hizmetteki kopyasını silme {#download-and-release-the-file}

Tamamlanmış dosyanın durum yanıtındaki göreli URL adresini kullanın. Aşağıdaki kontrol, yanıtın hâlâ işleminize ait olduğunu da doğrular:

```sh
FILE_URL=$(printf '%s\n' "$STATUS" | jq -er --argjson id "$OPERATION_ID" \
    'select(.operation_id == $id and .pending == false and .finalized == true and .file.state == "complete") | .file.url')
curl -fsS -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL" -o capture.mp4
printf '%s\n' "$STATUS" > capture.json
```

Tamamlanmış durum kaydını MP4 ile birlikte `capture.json` içinde saklayın. `/recording/status`, geçerli işlemi açıklar; bu nedenle önceki HTTP dosyaları kullanılabilir durumda kalsa bile sonraki bir kayıt durum yanıtını değiştirir.

İndirilen dosyayı kullanmadan veya hizmetteki kopyasını silmeden önce bayt cinsinden boyutunu ve SHA-256 değerini doğrulayın:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

receipt = json.loads(Path("capture.json").read_text(encoding="utf-8"))
capture = Path("capture.mp4")
if capture.stat().st_size != receipt["file"]["size"]:
    raise SystemExit("Recording download size mismatch")

digest = hashlib.sha256()
with capture.open("rb") as stream:
    for chunk in iter(lambda: stream.read(65536), b""):
        digest.update(chunk)
if digest.hexdigest() != receipt["file"]["sha256"]:
    raise SystemExit("Recording download SHA-256 mismatch")
print("Verified capture.mp4")
PY
```

`Range` üstbilgisi olmayan bir GET, MP4 dosyasının tamamını indirir. İstemci kısmi indirmeye ihtiyaç duyarsa hizmet `Range: bytes=0-1023` gibi iki ucu belirtilmiş bayt aralıklarını da destekler. Birleştirilen dosyayı aynı durum kaydıyla doğrulayın.

Dosyayı indirip doğruladıktan sonra hizmetin sakladığı kopyayı silebilirsiniz:

```sh
curl -fsS -X DELETE -H "X-Recording-Instance: $INSTANCE_ID" \
    "$ENGINE_URL$FILE_URL"
```

HTTP kayıt dosyaları açıkça silinene veya motor kapanana ya da yeniden başlatılana kadar kullanılabilir kalır. Motoru kapatmadan önce indirin. Hizmet en fazla 128 dosya saklar; yeni kayıtlara yer açmak için kaydettiğiniz tamamlanmış dosyaları silin.

### İşlem kimliklerini birlikte tutma {#keeping-operation-identities-together}

Her POST ve DELETE, `X-Recording-Instance` gerektirir. Örnekler, önceki motorun yerine geçen bir motorun yanıtlarını reddetmek için durum ve indirme isteklerinde de bu üstbilgiyi gönderir. `instance_id`, `operation_id` ve dosya bilgilerini bir arada tutun: yeniden başlatmada hizmet kimliği değişir ve yeni bir süreç işlem numaralarını yeniden kullanabilir.

Eksik kimlik HTTP 400 döndürür. Güncelliğini yitirmiş kimlik, güncelliğini yitirmiş durdurma işlemi veya silinmiş dosya HTTP 410 döndürür. Yeni bir kimlik alıp eski işlemi yeniden denemek için kullanmayın. Bunun yerine yeni hizmeti keşfedin ve yeni bir kayıt başlatın.

### HTTP hatalarını ele alma {#handling-http-failures}

Reddedilen istekler `error.code` ve `error.message` içeren JSON döndürür. Sorun giderme için tekil `curl` isteğini `-i` ile ve `-f` olmadan çalıştırarak HTTP durumunu ve hata gövdesini görün.

| HTTP durumu | Kontrol edilecekler |
| --- | --- |
| 409 | Başka bir kayıt etkin veya beklemede, geçerli kayıt durdurulmaya hazır değil ya da dosya hâlâ hazırlanıyor. Yeniden denemeden önce durumu okuyun. |
| 500 | Kayıt başlangıcı, depolama başlatma veya dosya hazırlama/okuma başarısız oldu. Hata iletisini inceleyin; başarısız yakalama ayrıca durum içinde `failure` bildirir. |
| 501 | Video veya istenen ses desteklenmiyor. Yetenekleri inceleyin; yalnızca ses kullanılamıyorsa `audio: false` kullanın. |
| 507 | Hizmetin saklanan dosya sınırına ulaşıldı. Başka kayıt başlatmadan önce tamamlanmış dosyaları indirip silin. |
