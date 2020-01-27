---
title: Networking in Defold
brief: This manual explains how to connect to remote servers and perform other kinds of network connections.
---

# Networking

It is not uncommon for games to have some kind of connection to a backend service, perhaps to post scores, handle match making or store saved games in the cloud. Many games also have peer to peer connections where game clients communicate directly with each other, without involvement of a central server. Network connections and the exchange of data can be made using several different protocols and standards:

* [HTTP Requests](#http-requests)
* [Socket connections](#socket-connections)
* [WebSocket connections](#websocket-connections)


## HTTP requests

Defold can make normal HTTP requests using the `http.request()` function. Example:

```Lua
local function handle_response(self, id, response)
	print(response.status, response.response)
end

http.request("https://www.defold.com", "GET", handle_response)
```

This will make an HTTP GET request to https://www.defold.com. The function is asynchronous and will not block while making the request. Once the request has been made and a server has sent a response it will invoke/call the provided callback function. The callback function will receive the full server response, including status code and response headers. It is also possible to make HTTP POST requests to pass data to the server and to specify request headers. Refer to the [API reference](/ref/http/) to learn more.

::: sidenote
HTTP requests are automatically cached in the client to improve network performance. The cached files are stored in an OS specific application support path in a folder named `defold/http-cache`. You usually don't have to care about the HTTP cache but if you need to clear the cache during development you can manually delete the folder containing the cached files. On macOS this folder is located in `%HOME%/Library/Application Support/Defold/http-cache/` and on Windows in `%APP_DATA%/defold/http-cache`.
:::

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


## WebSocket connections

Defold doesn't contain any out of the box solution for creating WebSocket connections. For WebSocket connectivity it is recommended to use the [Defold-WebSocket extension](https://github.com/britzl/defold-websocket).


# Game services

Using HTTP requests and socket connections allows you to connect to and interact with thousands of different services on the internet, but in most cases there's more to it than simply making an HTTP request. You usually need to use some kind of authentication, the request data may need to be formatted in a certain way and the response may need to be parsed before it can be used. This can of course be done manually by you but there are also extensions and libraries to take care of this sort of thing for you. Below you'll find a list of some extensions that can be used to more easily interact with specific backend services:

* [AWS SDK](https://github.com/britzl/aws-sdk-lua) - Use Amazon Web Services from within your game
* [Colyseus](https://github.com/colyseus/colyseus-defold) - Multiplayer game client
* [Firebase Analytics](https://github.com/defold/extension-firebase-analytics) - Add Firebase Analytics to your game
* [Game Analytics](https://gameanalytics.com/docs/item/defold-sdk) - Add GameAnalytics to your game
* [Google Analytics](https://github.com/britzl/defold-googleanalytics) - Add Google Analytics to your game
* [Google Play Game Services](https://github.com/defold/extension-gpgs) - Use Google Play Game Services to authenticate and use cloud save in your game
* [PlayFab](https://github.com/PlayFab/LuaSdk) - Add authentication, matchmaking, analytics, cloud save and more to your game
* [Steamworks](https://github.com/britzl/steamworks-defold/) - Add Steam support to your game

Check the [Asset Portal](https://www.defold.com/assets/) for even more extensions!
