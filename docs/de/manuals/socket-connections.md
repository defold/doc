---
title: Socket-Verbindungen
brief: Dieses Handbuch erklärt, wie du Socket-Verbindungen herstellst.
---

## Socket-Verbindungen {#socket-connections}

Defold enthält die [LuaSocket-Bibliothek](https://lunarmodules.github.io/luasocket/) zum Herstellen von TCP- und UDP-Socket-Verbindungen. Das folgende Beispiel zeigt, wie du eine Socket-Verbindung herstellst, Daten sendest und eine Antwort liest:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Dadurch wird ein TCP-Socket erstellt und mit der IP-Adresse 127.0.0.1 (localhost) und Port 8123 verbunden. Der Wert für die Zeitüberschreitung wird auf 0 gesetzt, damit der Socket nicht blockiert, und die Zeichenfolge "foobar" wird über den Socket gesendet. Außerdem wird eine Datenzeile (Bytes, die mit einem Zeilenumbruchzeichen enden) aus dem Socket gelesen. Beachte, dass das obige Beispiel keinerlei Fehlerbehandlung enthält.

### API-Referenz und Beispiele {#api-reference-and-examples}

In der [API-Referenz](/ref/socket/) erfährst du mehr über die Funktionen, die LuaSocket bereitstellt. Die [offizielle LuaSocket-Dokumentation](https://lunarmodules.github.io/luasocket/) enthält außerdem viele Beispiele für die Arbeit mit der Bibliothek. Weitere Beispiele und Hilfsmodule findest du in der [DefNet-Bibliothek](https://github.com/britzl/defnet/).
