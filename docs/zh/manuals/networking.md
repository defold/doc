---
title: Defold 中的网络连接
brief: 本手册介绍了如何连接到远程服务器以及执行其他类型的网络连接。
---

# 网络连接

游戏有某种后端服务连接是很常见的，可能是为了发布分数、处理匹配或在云端存储存档。许多游戏还具有点对点连接，游戏客户端之间直接通信，无需中央服务器参与。网络连接和数据交换可以使用多种不同的协议和标准。了解在 Defold 中使用网络连接的不同方法：

* [HTTP 请求](/manuals/http-requests)
* [Socket 连接](/manuals/socket-connections)
* [WebSocket 连接](/manuals/websocket-connections)
* [在线服务](/manuals/online-services)


## 技术细节

### IPv4 和 IPv6

Defold 支持套接字和 HTTP 请求的 IPv4 和 IPv6 连接。

### 安全连接

Defold 支持套接字和 HTTP 请求的安全 SSL 连接。

Defold 还可以选择性地验证任何安全连接的 SSL 证书。当在 *game.project* 的网络部分的 [SSL 证书设置](/manuals/project-settings/#network)) 字段中提供包含公共 CA 根证书密钥或自签名证书公钥的 PEM 文件时，将启用 SSL 验证。`builtins/ca-certificates` 中包含一个 CA 根证书列表，但建议创建一个新的 PEM 文件，并根据游戏连接到的服务器复制粘贴所需的 CA 根证书。