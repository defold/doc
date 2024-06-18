---
title: Socket 连接
brief: 本教程介绍了建立 socket 连接的方法.
---

## Socket 连接

Defold 包含 [LuaSocket 库](https://lunarmodules.github.io/luasocket/) 来建立 TCP 和 UDP socket 连接. 比如说, 上传和读取数据的例子:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

这样就建立了一个 TCP socket 并连接到 IP 127.0.0.1 (localhost) 的 8123 端口. 超时为 0 确保 socket 不会卡住程序, 然后上传 "foobar" 信息数据. 然后再读取一行服务器的回复 (读取字节直到换行符). 注意本例没有考虑错误处理.

### API 文档与示例

请参考 [API 文档](/ref/socket/) 了解 LuaSocket 功能. 在 [官方 LuaSocket 教程](https://lunarmodules.github.io/luasocket/) 中也含有库的许多用例. 在 [DefNet 库](https://github.com/britzl/defnet/) 里也有许多示例和帮助信息.
