---
title: HTTP 请求
brief: 本教程介绍了发布 HTTP 请求的方法.
---

## HTTP 请求

Defold 可以使用 `http.request()` 函数发布普通 HTTP 请求.

### HTTP GET

这是最常见的获得信息的请求类型. 举个例子:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

这段代码向 https://www.defold.com 发送了一个 HTTP GET 请求. 函数是异步的所以不会把游戏卡住. 一接到服务器回复便会调用回调函数. 回调函数里可以获取服务器返回的所有信息, 包括状态码和回复头信息.

::: sidenote
为了提高效率, HTTP 请求会自动缓存在客户端. 缓存文件保存在一个叫 `defold/http-cache` 的文件夹里, 其路径根据操作系统不同而不同. 一般来说不必关心缓存的存在, 除非你需要手动清除缓存文件. macOS 系统路径是 `%HOME%/Library/Application Support/Defold/http-cache/` , Windows 系统路径是 `%APP_DATA%/defold/http-cache`.
:::

### HTTP POST

当需要传输数据, 比如上传分数或者认证信息到服务器时, 通常需要发布 POST 请求:

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

### 其他 HTTP 请求类型

Defold HTTP 请求支持 HEAD, DELETE 和 PUT 类型.

### API 文档

请参考 [API 文档](/ref/http/).

### 扩展

有一个第三方实现的 HTTP 请求扩展库叫做 [TinyHTTP extension](https://defold.com/assets/tinyhttp/).
