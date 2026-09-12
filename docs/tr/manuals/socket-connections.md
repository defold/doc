---
title: Soket bağlantıları
brief: Bu kılavuz, soket bağlantılarının nasıl oluşturulduğunu açıklar.
---

## Soket bağlantıları

Defold, TCP ve UDP soket (socket) bağlantıları oluşturmak için [LuaSocket kütüphanesini](https://lunarmodules.github.io/luasocket/) içerir. Aşağıdaki örnek, bir soket bağlantısının nasıl oluşturulduğunu, nasıl veri gönderildiğini ve yanıtın nasıl okunduğunu gösterir:

```Lua
local client = socket.tcp()
client:connect("127.0.0.1", 8123)
client:settimeout(0)
client:send("foobar")
local response = client:receive("*l")
```

Bu kod bir TCP soketi oluşturur ve onu 127.0.0.1 (localhost) IP adresindeki 8123 bağlantı noktasına bağlar. Soketin yürütmeyi engellememesi (non-blocking) için zaman aşımını 0 olarak ayarlar ve soket üzerinden "foobar" dizesini gönderir. Ayrıca soketten bir satırlık veri (yeni satır karakteriyle biten baytlar) okur. Yukarıdaki örnekte hiçbir hata işleme mekanizması bulunmadığını unutmayın.

### API başvurusu ve örnekler

LuaSocket üzerinden sunulan işlevler hakkında daha fazla bilgi edinmek için [API başvurusuna](/ref/socket/) bakın. [Resmî LuaSocket belgelerinde](https://lunarmodules.github.io/luasocket/) de kütüphanenin nasıl kullanılacağına dair birçok örnek bulunur. [DefNet kütüphanesinde](https://github.com/britzl/defnet/) de bazı örnekler ve yardımcı modüller vardır.
