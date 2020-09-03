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

Defold HTTP requests also support the HEAD, DELETE and PUT methods.

### API Reference

Refer to the [API reference](/ref/http/) to learn more.

### Extensions

An alternative HTTP request implementation can be found in the [TinyHTTP extension](https://defold.com/assets/tinyhttp/).
