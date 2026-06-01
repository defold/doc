---
title: Defold HTTP请求
brief: 本手册解释了如何进行HTTP请求。
---

## HTTP请求

Defold可以使用`http.request()`函数进行常规HTTP请求。

### HTTP GET

这是从服务器获取一些数据的最基本请求。示例：

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

这将向https://www.defold.com发出HTTP GET请求。该函数是异步的，在发出请求时不会阻塞。一旦请求完成并收到服务器响应，它将调用提供的回调函数。回调函数将接收完整的服务器响应，包括状态码和响应头。关于如何处理 response 表，请参阅下面的更多信息。

::: sidenote
HTTP请求会自动缓存在客户端以提高网络性能。缓存的文件存储在操作系统特定的应用程序支持路径中，位于名为`defold/http-cache`的文件夹中。您通常不需要关心HTTP缓存，但如果在开发过程中需要清除缓存，可以手动删除包含缓存文件的文件夹。在macOS上，此文件夹位于`%HOME%/Library/Application Support/Defold/http-cache/`，在Windows上位于`%APP_DATA%/defold/http-cache`。
:::

### HTTP POST

当向服务器发送数据（例如分数或某些认证数据）时，通常使用 POST 请求：

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```

### 其他HTTP方法

Defold HTTP请求还支持HEAD、DELETE和PUT方法。也支持 CONNECT 方法（请参阅下面关于代理连接的章节）。

### 如何处理 HTTP 响应

回调中返回的 `response` 表包含实现细粒度响应处理所需的全部信息。其中两个关键字段是 `status` 和 `response`：

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

当响应包含大量二进制数据（例如图片或音乐曲目）时，将数据写入文件而不是加载到内存中可能更合适：

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

通过网络加载大量数据的另一个用例是声音流式传输，即从 URL 加载声音数据的“块”并将其送入声音资源。完整示例可在[声音流式传输手册](/sound-streaming#sound-streaming)中找到。

### 请求头

发送请求时可以设置额外的请求头。例如，可以用它来设置授权头，或者设置内容类型来告诉服务器所发送数据的格式。

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

Defold 会自动设置几个请求头：

* `If-None-Match: <etag>` 会使用任何之前缓存响应的 ETag 进行设置。
* `Transfer-Encoding: chunked` 会在请求体大于 16384 字节时设置。
* `Content-Length` 会设置为请求体大小（除非请求使用分块传输）。
* `Range: bytes=<from>-<to>` 会在请求部分响应时设置，例如[流式传输声音](/sound-streaming#sound-streaming)时。


### 响应头

服务器响应可以包含一个或多个响应头。它们可以在 `response` 表中访问：

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP 代理

有时需要通过代理服务器发送请求。可以通过指定连接目标服务器时使用的代理服务器来实现。使用代理时，会通过代理使用 HTTP 隧道建立到目标服务器的连接。HTTP 隧道使用 CONNECT HTTP 方法建立。示例：


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

### API参考

请参考[API参考](/ref/http/)了解更多。

### 扩展

替代的HTTP请求实现可以在[TinyHTTP扩展](https://defold.com/assets/tinyhttp/)中找到。
