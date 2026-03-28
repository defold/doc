---
title: HTTP Requests
brief: This manual explains how to make HTTP requests.
---

## HTTP requests

Defold can make normal HTTP requests using the `http.request()` function.

### HTTP GET

This is the most basic request to get some data from the server. Example:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

This will make an HTTP GET request to https://www.defold.com. The function is asynchronous and will not block while making the request. Once the request has been made and a server has sent a response it will invoke/call the provided callback function. The callback function will receive the full server response, including status code and response headers. See below for additional information about how to work with the response table.

::: sidenote
HTTP requests are automatically cached in the client to improve network performance. The cached files are stored in an OS specific application support path in a folder named `defold/http-cache`. You usually don't have to care about the HTTP cache but if you need to clear the cache during development you can manually delete the folder containing the cached files. On macOS this folder is located in `%HOME%/Library/Application Support/Defold/http-cache/` and on Windows in `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

When sending data, like a score or some authentication data, to a server it is typically done using a POST requests:

```lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local body = "12345"
http.request("https://www.myserver.com/score", "POST", handle_response, nil, body)
```


### Other HTTP methods

Defold HTTP requests also support the HEAD, DELETE and PUT methods. The CONNECT method is also supported (see section about proxy connections below).

### How to work with the HTTP response

The `response` table returned in the callback contains all of the information necessary to implement granular reponse handling. Two of the key fields are `status` and `response`:

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

When the response contains a large blob of binary data such as an image or a music track it might make sense to write the data to a file instead of loading it into memory:

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

http.request("https://www.foobar.com/myimage.png", "GET", handle_response)
```

Another use-case for loading large amounts of data over the network is sound streaming, when "chunks" of sound data are loaded from a URL and fed into a sound resource. A complete example can be found in the [Sound Streaming manual](/sound-streaming#sound-streaming).


### Request headers

It is possible to set additional headers when sending a request. This can for instance be used to set an authorization header or content type to tell the server which format the 

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

Defold will automatically set a couple of request headers:

* `If-None-Match: <etag>` will be set with the ETag of any previously cached response.
* `Transfer-Encoding: chunked` will be set if the request body is larger than 16384 bytes.
* `Content-Length` will be set with the size of the request body (unless the request is chunked).
* `Range: bytes=<from>-<to>` will be set if requesting a partial response, for instance when [streaming sounds](/sound-streaming#sound-streaming).


### Response headers

The server response may contain one or more response headers. These are available on the `response` table:

```lua
local function handle_response(self, id, response)
	for header,value in pairs(response.headers) do
		print(header, value)
	end
end

http.request("https://www.defold.com", "GET", handle_response)
```


### HTTP Proxy

It is sometimes desirable to send a request through a proxy server. This can be done by specifying a proxy server to use when connecting to the destination server. When a proxy is used the connection to the destination server is established using an a HTTP tunnel through the proxy. The HTTP tunnel is established using the CONNECT HTTP method. Example:


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

### API Reference

Refer to the [API reference](/ref/http/) to learn more.

### Extensions

An alternative HTTP request implementation can be found in the [TinyHTTP extension](https://defold.com/assets/tinyhttp/).
