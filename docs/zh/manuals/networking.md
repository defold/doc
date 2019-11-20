---
title: Defold 联网
brief: 本教程介绍了如何连接远程服务器以及建立其他各种连接.
---

# 联网

游戏需要连接各种后台服务器的情况很常见, 比如为了记录分数, 匹配对战玩家或者在云端存档. 还有的游戏有点对点交互的功能, 而不必连接中央服务器.


## HTTP 请求

Defold 能使用 `http.request()` 函数来建立 HTTP 请求. 比如:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

这样就建立了一个到 https://www.defold.com 的 HTTP GET 请求. 这个函数是异步的所以请求同时游戏并不卡住等待响应. 当服务器发回响应数据后会进入设置好的回调函数. 回调函数接收了相应包含的所有信息, 包括状态码和响应头. 同样可以建立 HTTP POST 请求来向服务器发送数据也能设置请求头信息. 更多详情请见 [API 教程](/ref/http/).

使用 HTTP 请求可以让你能够和互联网上各种各样的服务器交互, 但是通常不会这么简单的发送 HTTP 请求. 通常你需要做一些认证和数据序列化之类的操作. 当然手动操作也可以，但是我们有很多现成的服务插件可以使用. 使用这些插件能简化许多操作:

* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - 让游戏能够使用 Amazon Web Services
* [Colyseus](https://github.com/colyseus/colyseus-defold) - 网游客户端
* [Firebase Analytics](https://github.com/defold/extension-firebase-analytics) - 让游戏能够使用 Firebase Analytics
* [Google Analytics](https://github.com/britzl/defold-googleanalytics) - 让游戏能够使用 Google Analytics
* [Google Play Game Services](https://github.com/defold/extension-gpgs) - 让游戏能够使用 Google Play Game Services 来进行用户认证和云端存档
* [PlayFab](https://github.com/PlayFab/LuaSdk) - 让游戏能够使用 用户认证, 玩家匹配, 跟踪分析, 云端存档等等功能
* [Steamworks](https://github.com/britzl/steamworks-defold/) - 让游戏能够使用 Steam 支持

可以在 [资源大厅](https://www.defold.com/assets/) 找到更多扩展程序！


## Socket 连接

Defold 包含 [LuaSocket 库](http://w3.impa.br/~diego/software/luasocket/) 用来创建 TCP 和 UDP socket 连接. 创建socket连接, 发送数据和接收响应需要调用这些函数:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

这样就建立好了一个 TCP socket, 连接到了 IP 127.0.0.1 (localhost) 的端口 8123. 把超时设置成 0 就是建立成非阻塞式的socket，然后它在socket上发送了 "foobar" 消息. 最后它读取了一行socket响应数据 (读字节直到出现换行符). 注意此代码没有做错误处理. LuaSocket的更多功能详情请见 [API 文档](/ref/socket/). [官方 LuaSocket 文档](http://w3.impa.br/~diego/software/luasocket/) 同样包含了该库的许多使用实例. 此外这里也有许多实例和工具模块 [DefNet 库](https://github.com/britzl/defnet/).


## WebSocket 连接

Defold 不提供现成的建立 WebSocket 连接的方法. 对于 WebSocket 联网功能推荐使用 [Defold-WebSocket 扩展](https://github.com/britzl/defold-websocket).
