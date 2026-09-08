---
title: HTTP リクエスト
brief: このマニュアルでは、HTTP リクエストの送信方法を説明します。
---

## HTTP リクエスト {#http-requests}

Defold では、`http.request()` 関数を使って通常の HTTP リクエストを送信できます。

### HTTP GET

これは、サーバーからデータを取得するための最も基本的なリクエストです。例を示します。

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

これにより、https://www.defold.com に HTTP GET リクエストを送信します。この関数は非同期で動作し、リクエストの処理中も実行をブロックしません。リクエストを送信し、サーバーからレスポンスが返されると、指定したコールバック関数が呼び出されます。コールバック関数は、ステータスコードとレスポンスヘッダーを含む、サーバーのレスポンス全体を受け取ります。レスポンステーブルの扱い方については、後述の説明を参照してください。

::: sidenote
HTTP リクエストは、ネットワークのパフォーマンスを向上させるため、クライアント側で自動的にキャッシュされます。キャッシュされたファイルは、OS ごとのアプリケーションサポート用パス内にある `defold/http-cache` というフォルダーに保存されます。通常は HTTP キャッシュを気にする必要はありませんが、開発中にキャッシュを消去する必要がある場合は、キャッシュされたファイルを含むフォルダーを手動で削除できます。このフォルダーは、macOS では `%HOME%/Library/Application Support/Defold/http-cache/`、Windows では `%APP_DATA%/defold/http-cache` にあります。
:::

### HTTP POST

スコアや認証データなどのデータをサーバーへ送信する場合は、通常 POST リクエストを使います。

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### その他の HTTP メソッド {#other-http-methods}

Defold の HTTP リクエストは、HEAD、DELETE、PUT メソッドにも対応しています。CONNECT メソッドにも対応しています（後述のプロキシ接続のセクションを参照してください）。

### HTTP レスポンスの扱い方 {#how-to-work-with-the-http-response}

コールバックで返される `response` テーブルには、レスポンスをきめ細かく処理するために必要な情報がすべて含まれています。主要なフィールドのうち2つが、`status` と `response` です。

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

レスポンスに画像や音楽トラックなどのサイズの大きいバイナリデータが含まれる場合は、メモリへ読み込む代わりにファイルへ書き込むほうが適していることがあります。

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

ネットワーク経由で大量のデータを読み込む別の用途として、サウンドストリーミングがあります。これは、音声データの「チャンク」を URL から読み込み、サウンドリソース（sound resource）に渡すものです。完全な例は、[サウンドストリーミングのマニュアル](/sound-streaming#sound-streaming)で確認できます。


### リクエストヘッダー {#request-headers}

リクエストの送信時には、追加のヘッダーを設定できます。たとえば、`Authorization` ヘッダーを設定したり、`Content-Type` を設定してリクエスト本文の形式をサーバーへ伝えたりできます。

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

Defold は、いくつかのリクエストヘッダーを自動的に設定します。

* `If-None-Match: <etag>` には、以前にキャッシュされたレスポンスの ETag が設定されます。
* リクエスト本文が 16384 バイトを超える場合、`Transfer-Encoding: chunked` が設定されます。
* `Content-Length` には、リクエスト本文のサイズが設定されます（リクエストがチャンク形式の場合を除きます）。
* [サウンドのストリーミング](/sound-streaming#sound-streaming)など、部分的なレスポンスを要求する場合は、`Range: bytes=<from>-<to>` が設定されます。


### レスポンスヘッダー {#response-headers}

サーバーのレスポンスには、1つ以上のレスポンスヘッダーが含まれることがあります。これらは `response` テーブルから取得できます。

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP プロキシ {#http-proxy}

プロキシサーバー経由でリクエストを送信したい場合があります。接続先サーバーへの接続時に使うプロキシサーバーを指定すると、これを実現できます。プロキシを使う場合、接続先サーバーへの接続は、プロキシを通る HTTP トンネルを使って確立されます。この HTTP トンネルは、HTTP の CONNECT メソッドを使って確立されます。例を示します。


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

### API リファレンス {#api-reference}

詳しくは、[API リファレンス](/ref/http/)を参照してください。

### 拡張機能 {#extensions}

別の HTTP リクエスト実装として、[TinyHTTP 拡張（extension）](https://defold.com/assets/tinyhttp/)があります。
