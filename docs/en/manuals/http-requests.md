---
title: HTTP Requests
brief: This manual explains how to make HTTP requests.
---

## HTTP requests

Defold can make normal HTTP requests using the `http.request()` function.

### HTTP GET

This is the most basic request to get some data from the server. Example:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

This will make an HTTP GET request to https://www.defold.com. The function is asynchronous and will not block while making the request. Once the request has been made and a server has sent a response it will invoke/call the provided callback function. The callback function will receive the full server response, including status code and response headers.

::: sidenote
HTTP requests are automatically cached in the client to improve network performance. The cached files are stored in an OS specific application support path in a folder named `defold/http-cache`. You usually don't have to care about the HTTP cache but if you need to clear the cache during development you can manually delete the folder containing the cached files. On macOS this folder is located in `%HOME%/Library/Application Support/Defold/http-cache/` and on Windows in `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

When sending data, like a score or some authentication data, to a server it is typically done using a POST requests:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

local headers = {
	["Content-Type"] = "application/x-www-form-urlencoded"
}
local body = "foo=bar"
http.request("https://httpbin.org/post", "POST", handle_response, headers, body)
```


### Other HTTP methods

Defold HTTP requests also support the HEAD, DELETE and PUT methods. The CONNECT method is also supported (see section about proxy connections).


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
	else
		print("File was not written to disk:", response.error)
	end
end

http.request("https://www.foobar.com/myimage.png", "GET", handle_response)
```

Another use-case for loading large amounts of data over the network is sound streaming, when "chunks" of sound data are loaded from a URL and fed into a sound resource. A complete example can be found in the [Sound Streaming manual](/sound-streaming#sound-streaming).


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
