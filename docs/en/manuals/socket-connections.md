---
title: Socket connections
brief: This manual explains how to connect to create socket connections.
---

## Socket connections

Defold includes the [LuaSocket library](http://w3.impa.br/~diego/software/luasocket/) for creating TCP and UDP socket connections. Creating a socket connection, sending some data and reading a response is a little bit more involved:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

This will create a TCP socket, connect it to IP 127.0.0.1 (localhost) and port 8123. It will set timeout to 0 to make the socket non-blocking and it will send the string "foobar" over the socket. It will also read a line of data (bytes ending with a newline character) from the socket. Note that the above example doesn't contain any kind of error handling. Refer to the [API reference](/ref/socket/) to learn more about the functionality available via LuaSocket. The [official LuaSocket documentation](http://w3.impa.br/~diego/software/luasocket/) also contains many examples of how to work with the library. There is also some examples and helper modules in the [DefNet library](https://github.com/britzl/defnet/).
