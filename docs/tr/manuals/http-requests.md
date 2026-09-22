---
title: HTTP istekleri
brief: Bu kılavuz, HTTP isteklerinin nasıl gönderileceğini açıklar.
---

## HTTP istekleri

Defold, `http.request()` işleviyle standart HTTP istekleri (HTTP requests) gönderebilir.

### HTTP GET

Sunucudan veri almak için kullanılan en temel istek türüdür. Örnek:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

Bu kod, https://www.defold.com adresine bir HTTP GET isteği gönderir. İşlev eşzamansızdır (asynchronous) ve isteği gönderirken yürütmeyi engellemez. İstek gönderildikten ve sunucu bir yanıt verdikten sonra, belirtilen geri çağırım (callback) işlevini çağırır. Geri çağırım işlevi, durum kodu ve yanıt üstbilgileri dahil sunucu yanıtının tamamını alır. Yanıt tablosuyla nasıl çalışılacağı hakkında daha fazla bilgi için aşağıya bakın.

::: sidenote
Ağ performansını artırmak için HTTP istekleri istemcide otomatik olarak önbelleğe alınır. Önbelleğe alınan dosyalar, işletim sistemine özgü uygulama destek yolunda `defold/http-cache` adlı bir klasörde saklanır. Genellikle HTTP önbelleğiyle ilgilenmeniz gerekmez, ancak geliştirme sırasında önbelleği temizlemeniz gerekirse önbelleğe alınan dosyaları içeren klasörü elle silebilirsiniz. Bu klasör macOS'ta `%HOME%/Library/Application Support/Defold/http-cache/`, Windows'ta ise `%APP_DATA%/defold/http-cache` konumundadır.
:::

### HTTP POST

Bir sunucuya puan veya kimlik doğrulama verileri gibi veriler gönderilirken genellikle POST isteği kullanılır:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Diğer HTTP yöntemleri

Defold HTTP istekleri HEAD, DELETE ve PUT yöntemlerini de destekler. CONNECT yöntemi de desteklenir (aşağıdaki vekil sunucu bağlantıları bölümüne bakın).

### HTTP yanıtıyla çalışma

Geri çağırımda döndürülen `response` tablosu, yanıtı ayrıntılı olarak işlemek için gereken tüm bilgileri içerir. Temel alanlardan ikisi `status` ve `response` alanlarıdır:

```lua

local function handle_response(self, id, response)
	-- check the response status code. Common response codes:
	-- 200 OK - the request completed successfully
	-- 301 Moved permanently - the requested data has moved, see redirect header
	-- 307 Temporary redirect - same as above
	-- 208 Permanent redirect - same as above
	-- 400 Bad Request - the request was malformed
	-- 401 Unauthorized - the client must authenticate itself
	-- 404 Not Found - the server cannot find the information
	-- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
	if response.status == 200 then
		-- the response data
		-- this can be anything from plain text, json encoded data or binary data
		print(response.response)
		json.decode(response.response)
		sys.save(..., response.response)
	end
end
```

Yanıt, bir görüntü veya müzik parçası gibi büyük bir ikili veri bloğu içeriyorsa veriyi belleğe yüklemek yerine bir dosyaya yazmak mantıklı olabilir:

```lua
-- in this example we download myimage.png and write it directly to a file on disk

local options = {
	path = sys.get_save_file("mygame", "myimage.png")
}

local function handle_response(self, id, response)
	if response.status == 200 then
		print("File was successfully written to:", response.path)
		print("File size:", response.document_size)
		print("File path:", response.path)
	else
		print("File was not written to disk:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response, nil, nil, options)
```

Ağ üzerinden büyük miktarda veri yüklemenin bir başka kullanım alanı da akış yoluyla ses oynatmadır (sound streaming). Bu işlemde, ses verilerinin "parçaları" bir URL adresinden yüklenir ve bir ses kaynağına (sound resource) aktarılır. Eksiksiz bir örneği [Akış yoluyla ses oynatma kılavuzunda](/sound-streaming#sound-streaming) bulabilirsiniz.


### İstek üstbilgileri

İstek gönderirken ek üstbilgiler ayarlayabilirsiniz. Örneğin bu özellik, bir `Authorization` üstbilgisi ayarlamak veya sunucuya istek gövdesinin hangi biçimde olduğunu bildirmek için `Content-Type` üstbilgisini ayarlamak amacıyla kullanılabilir.

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

-- send some form data
local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "key1=value1&key2=value2"
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- send some json encoded data
local headers = {
	["Content-Type"] = "application/json"
}
local body = json.encode({ key1 = value1, key2 = value2 })
http.request("https://www.myserver.com/post", "POST", handle_response, headers, body)

-- request some data which requires authorization to access
local token = ... -- generate an access token (JWT, OAuth etc)
local headers = {
	["Authorization"] = "Bearer " .. token
}
http.request("https://www.myserver.com/content", "GET", handle_response, headers)
```

Defold bazı istek üstbilgilerini otomatik olarak ayarlar:

* `If-None-Match: <etag>`, daha önce önbelleğe alınmış bir yanıt varsa bu yanıtın ETag değeriyle ayarlanır.
* İstek gövdesi 16384 bayttan büyükse `Transfer-Encoding: chunked` ayarlanır.
* `Content-Length`, istek gövdesinin boyutuyla ayarlanır (istek parçalara bölünmüş değilse).
* Örneğin [akış yoluyla ses oynatırken](/sound-streaming#sound-streaming) olduğu gibi kısmi bir yanıt isteniyorsa `Range: bytes=<from>-<to>` ayarlanır.


### Yanıt üstbilgileri

Sunucu yanıtı bir veya daha fazla yanıt üstbilgisi içerebilir. Bunlara `response` tablosundan erişebilirsiniz:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP vekil sunucusu

Bazen bir isteği vekil sunucu (proxy server) üzerinden göndermek isteyebilirsiniz. Bunun için hedef sunucuya bağlanırken kullanılacak bir vekil sunucu belirtin. Vekil sunucu kullanıldığında, hedef sunucuya bağlantı vekil sunucu üzerinden geçen bir HTTP tüneliyle kurulur. HTTP tüneli, CONNECT HTTP yöntemiyle oluşturulur. Örnek:


```lua
-- connect to www.defold.com via localhost proxy on port 8888
local url = "https://www.defold.com:443"
local method = "GET"
local headers = {}
local post_data = nil
local options = {
	proxy = "https://127.0.0.1:8888"
}
http.request(url, method, function(self, id, response)
	pprint(response)
end, headers, post_data, options)
```

### API başvuru belgeleri

Daha fazla bilgi edinmek için [API başvuru belgelerine](/ref/http/) bakın.

### Eklentiler

Alternatif bir HTTP isteği uygulamasını [TinyHTTP eklentisinde](https://defold.com/assets/tinyhttp/) bulabilirsiniz.
