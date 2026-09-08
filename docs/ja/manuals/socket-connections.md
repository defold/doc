---
title: ソケット接続
brief: このマニュアルでは、ソケット接続を作成する方法を説明します。
---

## ソケット接続 {#socket-connections}

Defold には、TCP と UDP のソケット接続（socket connection）を作成するための [LuaSocket ライブラリ](https://lunarmodules.github.io/luasocket/) が含まれています。ソケット接続を作成し、データを送信してレスポンスを読み取る例を示します。

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

このコードは TCP ソケットを作成し、IP アドレス 127.0.0.1（localhost）のポート 8123 に接続します。ソケットをノンブロッキングにするためにタイムアウトを 0 に設定し、ソケット経由で文字列 "foobar" を送信します。また、ソケットから1行のデータ（改行文字で終わるバイト列）を読み取ります。上の例にはエラー処理が一切含まれていないことに注意してください。

### API リファレンスと例 {#api-reference-and-examples}

LuaSocket で利用できる機能の詳細は、[API リファレンス](/ref/socket/)を参照してください。[LuaSocket の公式ドキュメント](https://lunarmodules.github.io/luasocket/)にも、このライブラリの使い方を示す例が多数あります。[DefNet ライブラリ](https://github.com/britzl/defnet/)にも、いくつかの例とヘルパーモジュールがあります。
