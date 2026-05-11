---
title: Conexões de socket
brief: Este manual explica como criar conexões de socket.
---

## Conexões de socket

O Defold inclui a [biblioteca LuaSocket](https://lunarmodules.github.io/luasocket/) para criar conexões de socket TCP e UDP. Exemplo de como criar uma conexão de socket, enviar alguns dados e ler uma resposta:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Isso criará um socket TCP, conectará ao IP 127.0.0.1 (localhost) e à porta 8123. O timeout será definido como 0 para tornar o socket não bloqueante, e a string "foobar" será enviada pelo socket. O exemplo também lerá uma linha de dados (bytes terminados por um caractere de nova linha) do socket. Observe que o exemplo acima não contém nenhum tipo de tratamento de erro.

### Referência da API e exemplos

Consulte a [referência da API](/ref/socket/) para saber mais sobre a funcionalidade disponível via LuaSocket. A [documentação oficial do LuaSocket](https://lunarmodules.github.io/luasocket/) também contém muitos exemplos de como trabalhar com a biblioteca. Também há alguns exemplos e módulos auxiliares na [biblioteca DefNet](https://github.com/britzl/defnet/).
