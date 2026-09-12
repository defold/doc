---
title: Defold'da akış yoluyla ses oynatma
brief: Bu kılavuz, seslerin Defold oyun motoruna akış yoluyla nasıl aktarılacağını açıklar
---

# Akış yoluyla ses oynatma

Varsayılan davranış ses verisini bütünüyle yüklemek olsa da, veriyi kullanılmadan önce parçalar hâlinde yüklemek de yararlı olabilir. Bu yöntem genellikle "akış" (streaming) olarak adlandırılır.

Akış yoluyla ses oynatmanın bir yararı, çalışma sırasında daha az belleğe ihtiyaç duyulmasıdır. Bir diğer yararı ise, örneğin bir http URL adresinden içerik akışı yapıyorsanız içeriği istediğiniz zaman güncelleyebilmeniz ve ilk indirme işleminden de kaçınabilmenizdir.

### Örnek

Bu kurulumu gösteren bir örnek proje bulunmaktadır: [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming)

## Akış yoluyla ses oynatmayı etkinleştirme

### Kolay yol

Akış yoluyla ses oynatmanın en basit yolu, *game.project* dosyasındaki [`sound.stream_enabled` ayarını](https://defold.com/manuals/project-settings/#stream-enabled) etkinleştirmektir. Bu seçenek etkinleştirildiğinde motor, sesleri akış yoluyla yüklemeye başlar.

Not: Aynı anda çok sayıda ses dosyası yüklüyse `sound.stream_cache_size` değerini artırmanız gerekebilir (aşağıya bakın).

### Çalışma zamanı kaynakları

Yeni bir ses verisi kaynağı (resource) oluşturup bunu bir ses bileşenine (component) de atayabilirsiniz.

Bunun için:
* Ses dosyası verisinin ilk bölümünü yükleyin
    * Not: Bu, ogg/wav üstbilgisini de içeren ham ses dosyasıdır
* [`resource.create_sound_data()`](/ref/resource/#resource.create_sound_data) işlevini çağırarak yeni bir ses verisi kaynağı oluşturun.
* [`go.set()`](/ref/go#go.set) işlevini kullanarak yeni ses verisi kaynağını ses bileşenine atayın

Aşağıda, ses dosyasının ilk bölümünü almak için bir `http.request()` çağrısı kullanan örnek projeden bir bölüm yer alıyor.

::: sidenote
Gerçek bir akış için web sunucusunun [HTTP aralık isteklerini](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests) yerine getirmesi ve `206` durum kodunu döndürmesi gerekir. Sunucu `Range` üstbilgisini yok sayıp `200` durum kodunu döndürürse aşağıdaki örnek, bunun yerine yanıtın tamamından akış kullanmayan normal bir kaynak oluşturur.
:::

```lua
local function play_sound(self, hash)
    go.set(self.component, "sound", hash) -- override the resource data on the component
    sound.play(self.component)            -- start playing the sound
end

local function parse_content_range(value)
    if not value then
        return nil
    end
    local rstart, rend, filesize = value:match("^bytes%s+(%d+)%-(%d+)/(%d+)$")
    return tonumber(rstart), tonumber(rend), tonumber(filesize)
end

-- Callback for the http response.
local function http_result(self, _id, response)
    if response.status ~= 200 and response.status ~= 206 then
        return
    end

    local options = {
        data = response.response,
    }

    if response.status == 206 then
        local rstart, _, filesize = parse_content_range(response.headers["content-range"])
        if rstart ~= 0 or not filesize then
            print("Invalid Content-Range response")
            return
        end

        -- A partial resource enables streaming. filesize is the size of the
        -- complete file, not only the returned range.
        if #response.response < filesize then
            options.filesize = filesize
            options.partial = true
        end
    end

    local relative_path = self.filename
    print("Creating resource", relative_path)
    local resource_hash = resource.create_sound_data(relative_path, options)
    play_sound(self, resource_hash)
end

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end
```

## Kaynak sağlayıcıları

Ses dosyasının ilk parçasını yüklemek için başka yöntemler de kullanabilirsiniz. Unutulmaması gereken önemli nokta, kalan parçaların kaynak sisteminden ve onun kaynak sağlayıcılarından yüklendiğidir. Bu örnekte, [liveupdate.add_mount()](/ref/liveupdate/#liveupdate.add_mount) işlevini çağırıp bir Live Update bağlama noktası (mount) ekleyerek yeni bir (http) dosya sağlayıcısı ekliyoruz.

Çalışan bir örneği [https://github.com/defold/example-sound-streaming](https://github.com/defold/example-sound-streaming) adresinde bulabilirsiniz.

```lua
-- See http_result() from above example

local function load_web_sound(base_url, relative_path)
    local url = base_url .. "/" .. relative_path
    local headers = {}
    -- Request the initial part of the file
    headers['Range'] = string.format("bytes=%d-%d", 0, 16384-1)

    http.request(url, "GET", http_result, headers, nil, { ignore_cache = true })
end

function init(self)
    self.base_url = "http://my.server.com"
    self.filename = "/path/to/sound.ogg"

    liveupdate.add_mount("webmount", self.base_url, 100, function (_self, _name, _uri, _result)
                    -- once the mount is ready, we can start our request for downloading the first chunk
                    load_web_sound(self.base_url, self.filename)
                end)
end

function final(self)
    liveupdate.remove_mount("webmount")
end
```

## Ses parçası önbelleği

Seslerin çalışma sırasında tükettiği bellek miktarı, *game.project* dosyasındaki [`sound.stream_cache_size` ayarıyla](https://defold.com/manuals/project-settings/#stream-cache-size) denetlenir. Yüklenen ses verisi hiçbir zaman bu sınırı aşmaz.

Her ses dosyasının ilk parçası önbellekten çıkarılamaz ve kaynaklar yüklü olduğu sürece önbellekte yer kaplar. İlk parçanın boyutu, *game.project* dosyasındaki [`sound.stream_preload_size` ayarıyla](https://defold.com/manuals/project-settings/#stream-preload-size) denetlenir.

*game.project* dosyasındaki [`sound.stream_chunk_size` ayarını](https://defold.com/manuals/project-settings/#stream-chunk-size) değiştirerek her ses parçasının boyutunu da denetleyebilirsiniz. Aynı anda çok sayıda ses dosyası yüklüyse bu, ses önbelleğinin boyutunu daha da küçültmenize yardımcı olabilir. Ses parçası boyutundan küçük ses dosyaları akış yoluyla yüklenmez ve yeni bir parça önbelleğe sığmazsa en eski parça önbellekten çıkarılır

::: important
Ses parçası önbelleğinin toplam boyutunun, yüklü ses dosyası sayısı ile akış parçası boyutunun çarpımından büyük olması önerilir. Aksi takdirde her karede yeni parçaların önbellekten çıkarılması riski oluşur ve sesler düzgün oynatılmaz
:::
