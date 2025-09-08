---
title: Socket 连接
brief: 本手册介绍了如何创建 socket 连接。
---

## Socket 连接

Defold 包含 [LuaSocket 库](https://lunarmodules.github.io/luasocket/) 用于创建 TCP 和 UDP socket 连接。以下是如何创建 socket 连接、发送一些数据并读取响应的示例：

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

这将创建一个 TCP socket，将其连接到 IP 127.0.0.1（本地主机）和端口 8123。它将超时设置为 0 以使 socket 变为非阻塞模式，并通过 socket 发送字符串 "foobar"。它还将从 socket 读取一行数据（以换行符结尾的字节）。请注意，上面的示例不包含任何错误处理。

### API 参考和示例

请参考 [API 参考](/ref/socket/) 以了解有关 LuaSocket 可用功能的更多信息。[官方 LuaSocket 文档](https://lunarmodules.github.io/luasocket/) 也包含许多有关如何使用该库的示例。在 [DefNet 库](https://github.com/britzl/defnet/) 中也有一些示例和辅助模块。
