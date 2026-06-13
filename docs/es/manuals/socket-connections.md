---
title: Conexiones de socket
brief: Este manual explica cómo crear conexiones de socket.
---

## Conexiones de socket

Defold incluye la [biblioteca LuaSocket](https://lunarmodules.github.io/luasocket/) para crear conexiones de socket TCP y UDP. Ejemplo de cómo crear una conexión de socket, enviar algunos datos y leer una respuesta:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Esto creará un socket TCP, lo conectará a la IP 127.0.0.1 (localhost) y al puerto 8123. Establecerá el timeout en 0 para hacer que el socket sea no bloqueante y enviará la string "foobar" por el socket. También leerá una línea de datos (bytes que terminan con un carácter de nueva línea) desde el socket. Ten en cuenta que el ejemplo anterior no contiene ningún tipo de manejo de errores.

### Referencia de API y ejemplos

Consulta la [referencia de API](/ref/socket/) para aprender más sobre la funcionalidad disponible a través de LuaSocket. La [documentación oficial de LuaSocket](https://lunarmodules.github.io/luasocket/) también contiene muchos ejemplos de cómo trabajar con la biblioteca. También hay algunos ejemplos y módulos de ayuda en la [biblioteca DefNet](https://github.com/britzl/defnet/).
