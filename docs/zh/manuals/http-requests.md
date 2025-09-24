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

这将向https://www.defold.com发出HTTP GET请求。该函数是异步的，在发出请求时不会阻塞。一旦请求完成并收到服务器响应，它将调用提供的回调函数。回调函数将接收完整的服务器响应，包括状态码和响应头。

::: sidenote
HTTP请求会自动缓存在客户端以提高网络性能。缓存的文件存储在操作系统特定的应用程序支持路径中，位于名为`defold/http-cache`的文件夹中。您通常不需要关心HTTP缓存，但如果在开发过程中需要清除缓存，可以手动删除包含缓存文件的文件夹。在macOS上，此文件夹位于`%HOME%/Library/Application Support/Defold/http-cache/`，在Windows上位于`%APP_DATA%/defold/http-cache`。
:::

### HTTP POST

当向服务器发送数据，如分数或某些认证数据时，通常使用POST请求：

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

### 其他HTTP方法

Defold HTTP请求还支持HEAD、DELETE和PUT方法。

### API参考

请参考[API参考](/ref/http/)了解更多。

### 扩展

替代的HTTP请求实现可以在[TinyHTTP扩展](https://defold.com/assets/tinyhttp/)中找到。
