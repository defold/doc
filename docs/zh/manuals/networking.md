---
title: Defold 联网
brief: 本教程介绍了如何连接远程服务器以建立各种连接.
---

# 联网

如今带后台服务的游戏并不新奇了, 也许需要向后台传送分数, 匹配玩家或者在云端存档. 许多游戏带点对点交流的功能, 以便客户端之间能够直接对话, 而不需要中央服务器. 网络连接与数据交换有许多种协议和标准. 详情请见:

* [HTTP 请求](/manuals/http-requests)
* [Socket 连接](/manuals/socket-connections)
* [WebSocket 连接](/manuals/websocket-connections)
* [Online 服务](/manuals/online-services)


## 技术细节

### IPv4 和 IPv6

Defold 支持套接字和 HTTP 请求的 IPv4 和 IPv6 连接.

### 安全连接

Defold 支持套接字和 HTTP 请求的安全 SSL 连接.

Defold 还可根据需要验证任何连接的 SSL 证书. 当 PEM 文件包含了公开 CA-root 证书密钥或者在 *game.project* 的 Network 部分的 [SSL Certificates setting](/manuals/project-settings/#network)) 选项中提供了自签名的公开证书密钥时, 将激活 SSL 验证. 在 `builtins/ca-certificates` 下包含有一组 CA-root 证书, 但是推荐用户自己新建 PEM 文件并根据游戏服务器需要复制粘贴相应的 CA-root 证书.